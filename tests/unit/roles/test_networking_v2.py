"""Exercise the ported role and V2 map tasks without a live cluster.

Only external VMware/OpenShift API modules are replaced with local fixtures.
Ansible executes the real roles, includes, validations, templates and filters.
"""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
ANNOTATION = "infra.openshift-virtualization-migration/source-portgroup"
SPEC = importlib.util.spec_from_file_location(
    "match_portgroup", ROOT / "plugins/filter/match_portgroup.py"
)
FILTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FILTER)


def nad(name="shared", groups="site-a, site-b", namespace="workloads"):
    return {
        "object": {
            "metadata": {"name": name, "namespace": namespace, "annotations": {ANNOTATION: groups}}
        }
    }


@pytest.mark.parametrize("name", ["site-a", "site-b"])
def test_match_multiple_portgroups(name):
    entry = nad()
    assert FILTER.match_portgroup([entry], name, ANNOTATION) == [entry]


def test_match_single_namespace_and_malformed_entries():
    entry = nad(groups="legacy")
    entries = [None, {}, {"object": None}, nad(groups=None), entry]
    assert FILTER.match_portgroup(entries, "legacy", ANNOTATION, " workloads ") == [entry]
    assert FILTER.match_portgroup(entries, "legacy", ANNOTATION, "other") == []
    assert FILTER.match_portgroup(entries, "leg", ANNOTATION) == []
    assert FILTER.match_portgroup([nad()], "site-a, site-b", ANNOTATION) == []


@pytest.fixture
def runner(tmp_path):
    collections = tmp_path / "collections" / "ansible_collections"
    own = collections / "infra" / "openshift_virtualization_migration"
    own.parent.mkdir(parents=True)
    own.symlink_to(ROOT, target_is_directory=True)
    modules = collections / "redhat" / "openshift" / "plugins" / "modules"
    modules.mkdir(parents=True)
    (modules / "k8s.py").write_text("""
import json
import os
from ansible.module_utils.basic import AnsibleModule
module = AnsibleModule(argument_spec={
    "state": {"default": "present"}, "definition": {"type": "dict", "required": True},
    "host": {}, "api_key": {"no_log": True}, "validate_certs": {"type": "bool"},
    "apply": {"type": "bool"}}, supports_check_mode=True)
path = os.environ["NETWORK_TEST_STATE"]
try:
    with open(path) as stream:
        state = json.load(stream)
except FileNotFoundError:
    state = {}
obj = module.params["definition"]
key = obj["kind"] + "/" + obj["metadata"].get("namespace", "") + "/" + obj["metadata"]["name"]
changed = state.get(key) != obj
if not module.check_mode:
    state[key] = obj
    with open(path, "w") as stream:
        json.dump(state, stream)
module.exit_json(changed=changed, result=obj)
""")
    # Automatic mode discovery is also isolated from real VMware endpoints.
    vmware = collections / "community" / "vmware" / "plugins" / "modules"
    vmware.mkdir(parents=True)
    responses = {
        "vmware_dvswitch_info": {
            "distributed_virtual_switches": [
                {
                    "configure": {
                        "name": "switch",
                        "settings": {"properties": {"advanced": {"maxMtu": 1500}}},
                    }
                }
            ]
        },
        "vmware_dvs_portgroup_info": {
            "dvs_portgroup_info": {
                "switch": [
                    {
                        "portgroup_name": "site-a",
                        "dvswitch_name": "switch",
                        "vlan_info": {"vlan_id": 100, "trunk": False},
                        "active_uplinks": ["uplink1"],
                        "standby_uplinks": [],
                    }
                ]
            }
        },
    }
    for name, response in responses.items():
        (vmware / (name + ".py")).write_text(
            "from ansible.module_utils.basic import AnsibleModule\n"
            'm = AnsibleModule(argument_spec={"hostname": {}, "username": {}, '
            '"password": {"no_log": True}, "validate_certs": {"type": "bool"}, '
            '"datacenter": {}, "show_vlan_info": {"type": "bool"}})\n'
            "m.exit_json(changed=False, **" + repr(response) + ")\n"
        )
    state_path = tmp_path / "state.json"
    config = tmp_path / "ansible.cfg"
    config.write_text("[defaults]\ninterpreter_python=auto_silent\n")
    env = dict(
        os.environ,
        ANSIBLE_COLLECTIONS_PATH=str(collections.parent),
        ANSIBLE_ROLES_PATH=str(ROOT / "roles"),
        ANSIBLE_CONFIG=str(config),
        ANSIBLE_LOCAL_TEMP=str(tmp_path / "local"),
        ANSIBLE_REMOTE_TEMP=str(tmp_path / "remote"),
        NETWORK_TEST_STATE=str(state_path),
        ANSIBLE_NOCOLOR="1",
    )

    def run(tasks, variables=None, success=True):
        play = [
            {
                "name": "Networking regression",
                "hosts": "localhost",
                "connection": "local",
                "gather_facts": False,
                "vars": variables or {},
                "tasks": tasks,
            }
        ]
        path = tmp_path / "test.yml"
        path.write_text(yaml.safe_dump(play, sort_keys=False))
        result = subprocess.run(
            [sys.executable, "-m", "ansible.cli.playbook", "-i", "localhost,", str(path)],
            env=env,
            capture_output=True,
            text=True,
            timeout=90,
        )
        if success:
            assert result.returncode == 0, result.stdout + result.stderr
        else:
            assert result.returncode != 0, result.stdout + result.stderr
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        return result, state

    return run


ROLE = [
    {
        "name": "Prepare networks",
        "ansible.builtin.include_role": {
            "name": "infra.openshift_virtualization_migration.network_mgmt"
        },
    }
]


@pytest.mark.parametrize(
    "mode,kind",
    [
        ("ovn-layer2", "ovn-k8s-cni-overlay"),
        ("linux-bridge", "cnv-bridge"),
        ("ovs-bridge", "ovn-k8s-cni-overlay"),
    ],
)
def test_manual_role_modes_and_repeat_run(runner, mode, kind):
    variables = {
        "network_mgmt_openshift_network_bridge_mode": mode,
        "network_mgmt_manual_localnet_name": "physical",
        "network_mgmt_manual_nad_list": [
            {
                "name": "shared",
                "namespace": "workloads",
                "portgroups": ["site-a", "site-b"],
                "vlan": {"vlan_id": 100},
            }
        ],
    }
    _, state = runner(ROLE, variables)
    obj = state["NetworkAttachmentDefinition/workloads/shared"]
    assert obj["metadata"]["annotations"][ANNOTATION] == "site-a,site-b"
    assert json.loads(obj["spec"]["config"])["type"] == kind
    assert all(not key.startswith("NodeNetworkConfigurationPolicy/") for key in state)
    result, repeated = runner(ROLE, variables)
    assert repeated == state
    assert "changed=0" in result.stdout


@pytest.mark.parametrize(
    "global_mtu,override,expected",
    [(None, None, None), (9000, None, 9000), (9000, 1500, 1500), (None, 1500, 1500)],
)
def test_layer2_mtu_precedence(runner, global_mtu, override, expected):
    entry = {"name": "mtu-test", "portgroup": "legacy"}
    variables = {
        "network_mgmt_openshift_network_bridge_mode": "ovn-layer2",
        "network_mgmt_manual_nad_list": [entry],
    }
    if global_mtu is not None:
        variables["network_mgmt_nad_mtu"] = global_mtu
    if override is not None:
        entry["mtu"] = override
    _, state = runner(ROLE, variables)
    cfg = json.loads(state["NetworkAttachmentDefinition/default/mtu-test"]["spec"]["config"])
    assert cfg.get("mtu") == expected
    assert ("mtu" in cfg) == (expected is not None)


@pytest.mark.parametrize(
    "extra,entry",
    [
        ({"network_mgmt_nad_mtu": 67}, {"name": "bad"}),
        ({}, {"name": "bad", "mtu": 9001}),
        ({}, {"name": "bad", "portgroup": "one", "portgroups": ["two"]}),
        ({}, {"name": "bad", "portgroups": ["name,with-comma"]}),
    ],
)
def test_invalid_inputs_fail_before_cluster_changes(runner, extra, entry):
    variables = {
        "network_mgmt_openshift_network_bridge_mode": "ovn-layer2",
        "network_mgmt_manual_nad_list": [entry],
        **extra,
    }
    _, state = runner(ROLE, variables, success=False)
    assert state == {}


def test_automatic_layer2_creation(runner):
    _, state = runner(
        ROLE,
        {
            "network_mgmt_openshift_network_bridge_mode": "ovn-layer2",
            "network_mgmt_vcenter_hostname": "fixture.invalid",
            "network_mgmt_vcenter_datacenter": "datacenter",
            "network_mgmt_vcenter_dvswitch": "switch",
            "network_mgmt_nad_mtu": 1500,
        },
    )
    assert list(state) == ["NetworkAttachmentDefinition/default/site-a"]
    assert json.loads(next(iter(state.values()))["spec"]["config"])["mtu"] == 1500


def test_v2_mapping_shared_network_explicit_override_and_no_match(runner):
    resolve = str(ROOT / "roles/mtv_maps/tasks/_resolve_network_destination.yml")
    cases = [
        ("site-a", {"type": "multus", "name": "shared", "namespace": "workloads"}),
        ("site-b", {"type": "multus", "name": "shared", "namespace": "workloads"}),
        ("explicit", {"type": "multus", "name": "chosen", "namespace": "custom"}),
        ("pod", {"type": "pod"}),
        ("skip", {"type": "ignored"}),
        ("unmatched", {"type": "pod"}),
    ]
    expected = [{"source": {"id": name, "name": name}, "destination": dest} for name, dest in cases]
    tasks = [
        {
            "name": "Resolve networks",
            "ansible.builtin.include_tasks": resolve,
            "loop": [{"id": name, "name": name} for name, _ in cases],
            "loop_control": {"loop_var": "_net"},
        },
        {
            "name": "Assert resulting destinations",
            "ansible.builtin.assert": {"that": ["_mtv_maps_network_map_entries == expected"]},
        },
    ]
    runner(
        tasks,
        {
            "_mtv_maps_nads": [nad()],
            "_mtv_maps_network_map_entries": [],
            "mtv_maps_nad_source_annotation": ANNOTATION,
            "expected": expected,
            "mtv_maps_network_map_overrides": [
                {"id": "explicit", "nad": "custom/chosen"},
                {"id": "pod", "destination_type": "pod"},
                {"id": "skip", "destination_type": "ignored"},
            ],
        },
    )


@pytest.mark.parametrize(
    "override",
    [
        {"destination_type": "multus"},
        {"destination_type": "invalid"},
        {"destination_type": "multus", "nad": "ns/"},
    ],
)
def test_invalid_explicit_destination_does_not_fall_back(runner, override):
    runner(
        [
            {
                "name": "Resolve invalid destination",
                "ansible.builtin.include_tasks": str(
                    ROOT / "roles/mtv_maps/tasks/_resolve_network_destination.yml"
                ),
            }
        ],
        {
            "_net": {"id": "bad", "name": "bad"},
            "_mtv_maps_network_map_entries": [],
            "mtv_maps_network_map_overrides": [{"id": "bad", **override}],
        },
        success=False,
    )
