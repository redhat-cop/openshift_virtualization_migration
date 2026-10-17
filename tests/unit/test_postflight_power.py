"""Exercise the real Ansible executor with network-free VMware module doubles.

The temporary collection overrides both VMware FQCNs. Doubles contain no SDK
or connection code; no credentials or customer endpoints are used. These are
role orchestration tests, NOT vCenter/emulator compatibility evidence.
"""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest


ROOT = Path(__file__).resolve().parents[2]
LOOKUP = """
from ansible.module_utils.basic import AnsibleModule
import json
import os
m = AnsibleModule(argument_spec=dict(
    hostname=dict(type='str'), username=dict(type='str'),
    password=dict(type='str', no_log=True), validate_certs=dict(type='bool'),
    name=dict(type='str'), datacenter=dict(type='str'),
    schema=dict(type='str', default='summary'), properties=dict(type='list', elements='str'),
), supports_check_mode=True)
name = m.params['name']
fixture = json.loads(os.environ['POSTFLIGHT_TEST_FIXTURE'])
kind = fixture.get('lookup', {}).get(name, 'on')
if kind == 'failure':
    m.fail_json(msg='mock private failure payload')
if kind == 'malformed':
    m.exit_json(changed=False, instance={})
if kind == 'unknown':
    m.exit_json(changed=False, instance={'moid': 'id-' + name, 'hw_power_status': 'unknown'})
if m.params['schema'] == 'vsphere':
    m.exit_json(changed=False, instance={'config': {'hardware': {
        'device': [{'capacityInKB': 1024}, {'label': 'network adapter'}]}}})
m.exit_json(changed=False, instance={
    'moid': 'id-' + name, 'hw_power_status': 'poweredOff' if kind == 'off' else 'poweredOn',
    'ipv4': '192.0.2.10',
})
"""
POWER = """
from ansible.module_utils.basic import AnsibleModule
import json
import os
m = AnsibleModule(argument_spec=dict(
    hostname=dict(type='str'), username=dict(type='str'),
    password=dict(type='str', no_log=True), validate_certs=dict(type='bool'),
    datacenter=dict(type='str', required=True), moid=dict(type='str'),
    state=dict(type='str', choices=['powered-off']),
), supports_check_mode=True)
fixture = json.loads(os.environ['POSTFLIGHT_TEST_FIXTURE'])
kind = fixture.get('action', {}).get(m.params['moid'], 'success')
if kind == 'failure':
    m.fail_json(msg='mock private failure payload')
if kind == 'malformed':
    m.exit_json(changed=True)
m.exit_json(changed=True, vm={'moid': m.params['moid']}, postflight_mock=True)
"""
K8S = """
from ansible.module_utils.basic import AnsibleModule
import json
import os
m = AnsibleModule(argument_spec=dict(
    host=dict(type='str'), api_key=dict(type='str', no_log=True),
    validate_certs=dict(type='bool'), api_version=dict(type='str'),
    kind=dict(type='str'), namespace=dict(type='str'), name=dict(type='str'),
), supports_check_mode=True)
fixture = json.loads(os.environ.get('POSTFLIGHT_TEST_FIXTURE', '{}'))
kind = m.params['kind']
if kind == 'VirtualMachine':
    # MTV references migrated disks as persistentVolumeClaim (the bound
    # DataVolume's PVC); dataVolume-style is the in-flight form.
    m.exit_json(changed=False, resources=[{'metadata': {'name': 'a'},
        'status': {'printableStatus': 'Running'},
        'spec': {'template': {'spec': {'volumes': [
            {'name': 'vol-0', 'persistentVolumeClaim': {'claimName': 'disk'}}]}}}}])
if kind == 'VirtualMachineInstance':
    m.exit_json(changed=False, resources=[{'metadata': {'name': 'a'}, 'status': {
        'guestOSInfo': {'name': 'fixture'}, 'interfaces': [{'ipAddress': '192.0.2.10'}]}}])
if kind == 'Plan':
    m.exit_json(changed=False, resources=[
        {'metadata': {'name': 'a-plan', 'namespace': 'fixture'}}])
if kind == 'Migration':
    if fixture.get('no_migrations'):
        m.exit_json(changed=False, resources=[])
    m.exit_json(changed=False, resources=[
        {'metadata': {'name': 'mig-old', 'creationTimestamp': '2026-01-01T00:00:00Z'},
         'spec': {'plan': {'name': 'a-plan', 'namespace': 'fixture'}},
         'status': {'conditions': [{'type': 'Succeeded', 'status': 'True'}], 'vms': []}},
        {'metadata': {'name': 'mig-new', 'creationTimestamp': '2026-01-02T00:00:00Z'},
         'spec': {'plan': {'name': 'a-plan', 'namespace': 'fixture'}},
         'status': {'conditions': [{'type': 'Failed', 'status': 'True'}],
                    'vms': [{'id': 'vm-a', 'name': 'a', 'phase': 'Completed',
                             'conditions': [{'type': 'Failed', 'status': 'True'}]}]}},
    ])
m.exit_json(changed=False, resources=[])
"""


class PostflightPowerTests(unittest.TestCase):
    def test_offline_power_paths(self):
        cases = [
            # name, fixture, overrides, expected passed, expected actions, detail
            ("success", {}, {}, True, 1, "power-off completed"),
            ("action failure", {"action": {"id-a": "failure"}}, {}, False, 0, "power-off failed"),
            ("malformed action", {"action": {"id-a": "malformed"}}, {}, False, 1, "unconfirmed"),
            ("lookup failure", {"lookup": {"a": "failure"}}, {}, False, 0, "lookup failed"),
            ("malformed lookup", {"lookup": {"a": "malformed"}}, {}, False, 0, "lookup failed"),
            ("unknown state", {"lookup": {"a": "unknown"}}, {}, False, 0, "unsupported source facts"),
            ("already off", {"lookup": {"a": "off"}}, {}, True, 0, "already off"),
            ("read only", {}, {"postflight_power_off_source": False,
                               "postflight_vcenter_datacenter": ""}, True, 0, "read-only"),
            ("missing datacenter", {}, {"postflight_vcenter_datacenter": ""}, False, 0, "datacenter required"),
            ("plan failed", {}, {"__postflight_result_plan": {"ran": True, "passed": False}},
             True, 0, "source stays on"),
            ("plan absent", {}, {"__postflight_result_plan": {}}, True, 0, "source stays on"),
            ("list failed", {}, {"__postflight_result_list": {"ran": True, "passed": False}},
             True, 0, "source stays on"),
            ("missing target", {}, {"__postflight_vms_state": {"a": {"present": False, "running": False}}},
             True, 0, "source stays on"),
            ("target stopped", {}, {"__postflight_vms_state": {"a": {"present": True, "running": False}}},
             True, 0, "source stays on"),
            ("disk mismatch", {}, {"__postflight_disks_state": {
                "a": {"source_ok": True, "source_disks": 2, "target_volumes": 1}}},
             True, 0, "source stays on"),
            ("disk lookup failed", {}, {"__postflight_disks_state": {
                "a": {"source_ok": False, "source_disks": 1, "target_volumes": 1}}},
             True, 0, "source stays on"),
            ("absent facts", {}, {"__postflight_vms_state": {}, "__postflight_disks_state": {}},
             True, 0, "source stays on"),
            ("mixed gates", {}, {"postflight_vm_list": ["a", "b"]}, True, 1, "b (id-b): source stays on"),
            ("partial failure", {"lookup": {"b": "failure"}}, {"postflight_vm_list": ["a", "b"]},
             False, 1, "power-off completed"),
            ("check mode", {"check": True}, {}, True, 0, "would power off"),
            ("plan failed", {"tasks_from": "validate_plan.yml"},
             {"postflight_plan_name": "a-plan", "postflight_plan_namespace": "fixture"},
             False, 0, "is Failed"),
            ("plan none", {"tasks_from": "validate_plan.yml", "no_migrations": True},
             {"postflight_plan_name": "a-plan", "postflight_plan_namespace": "fixture"},
             False, 0, "no Migration object"),
            ("disk map", {"tasks_from": "validate_disks.yml"}, {}, True, 0, "Disk topology matches"),
            ("disk failure", {"tasks_from": "validate_disks.yml", "lookup": {"a": "failure"}},
             {}, False, 0, "vCenter lookup failed"),
            ("disk malformed", {"tasks_from": "validate_disks.yml", "lookup": {"a": "malformed"}},
             {}, False, 0, "vCenter lookup failed"),
            ("IP map", {"tasks_from": "validate_ip.yml"}, {}, True, 0, "every VM reports"),
            ("IP lookup failure", {"tasks_from": "validate_ip.yml", "lookup": {"a": "failure"}},
             {}, False, 0, "vCenter lookup failed"),
            ("VM map", {"tasks_from": "validate_vms.yml"}, {}, True, 0, "present and Running"),
            ("agent map", {"tasks_from": "validate_agent.yml"}, {}, True, 0, "Guest agent responsive"),
        ]
        with tempfile.TemporaryDirectory(prefix="postflight-offline-") as tmp:
            base = Path(tmp)
            collections = base / "collections" / "ansible_collections"
            infra = collections / "infra/openshift_virtualization_migration"
            infra.parent.mkdir(parents=True)
            # Whole collection: the postflight role AND the real
            # mtv_migration_status module with its module_utils.
            infra.symlink_to(ROOT, target_is_directory=True)
            for collection, module, source in [
                ("community/vmware", "vmware_guest_info", LOOKUP),
                ("vmware/vmware", "vm_powerstate", POWER),
                ("kubernetes/core", "k8s_info", K8S),
            ]:
                modules = collections / collection / "plugins/modules"
                modules.mkdir(parents=True)
                (modules / f"{module}.py").write_text(textwrap.dedent(source))
            config = base / "ansible.cfg"
            config.write_text("[defaults]\nretry_files_enabled = False\nhost_key_checking = True\n")
            for name, fixture, overrides, passed, actions, detail in cases:
                with self.subTest(name=name):
                    variables = {
                        "postflight_vcenter_hostname": "offline.invalid",
                        "postflight_vcenter_username": "fixture",
                        "postflight_vcenter_password": "fixture",
                        "postflight_vcenter_datacenter": "fixture-dc",
                        "postflight_vm_list": ["a"],
                        "postflight_openshift_host": "https://offline.invalid",
                        "postflight_openshift_api_key": "fixture",
                        "postflight_target_namespace": "fixture",
                        "__postflight_result_plan": {"ran": True, "passed": True},
                        "__postflight_result_list": {"ran": True, "passed": True},
                        "__postflight_vms_state": {"a": {"present": True, "running": True}},
                        "__postflight_disks_state": {
                            "a": {"source_ok": True, "source_disks": 1, "target_volumes": 1}},
                    }
                    variables.update(overrides)
                    tasks_from = fixture.get("tasks_from", "power_off.yml")
                    checks = [
                        "__postflight_power_gate is mapping",
                        "__postflight_result_power.passed | bool == " + str(passed).lower(),
                        json.dumps(detail) + " in __postflight_result_power.detail",
                        "'mock private failure payload' not in __postflight_result_power.detail",
                        "(__postflight_power_results.results | selectattr('changed', 'equalto', true)"
                        f" | list | length) == {actions}",
                        "(__postflight_power_results.results | selectattr('vm', 'defined')"
                        " | map(attribute='vm.moid') | list | difference(['id-a']) | length) == 0",
                    ]
                    if tasks_from == "validate_plan.yml":
                        # The check sets its own result fact; drop the
                        # play-var shadows so set_fact is observable.
                        for key in ("__postflight_result_plan", "__postflight_result_list",
                                    "__postflight_vms_state", "__postflight_disks_state"):
                            variables.pop(key, None)
                        checks = [
                            "__postflight_result_plan.passed | bool == " + str(passed).lower(),
                            json.dumps(detail) + " in __postflight_result_plan.detail",
                        ]
                        if not fixture.get("no_migrations"):
                            checks.append("__postflight_migration_name == 'mig-new'")
                    elif tasks_from != "power_off.yml":
                        check, state = {
                            "validate_disks.yml": ("disks", "disks_state"),
                            "validate_ip.yml": ("ip", "ip_state"),
                            "validate_vms.yml": ("vms", "vms_state"),
                            "validate_agent.yml": ("agent", "agents"),
                        }[tasks_from]
                        # Exercise task-produced maps, not pre-populated facts.
                        variables.pop("__postflight_vms_state", None)
                        variables.pop("__postflight_disks_state", None)
                        checks = [
                            f"__postflight_{state} is mapping",
                            f"__postflight_result_{check}.passed | bool == " + str(passed).lower(),
                            json.dumps(detail) + f" in __postflight_result_{check}.detail",
                        ]
                        if check == "disks":
                            checks.append("__postflight_disks_mismatched is not string")
                    play = [{"hosts": "localhost", "gather_facts": False, "connection": "local",
                             "vars": variables, "tasks": [
                                 {"ansible.builtin.include_role": {
                                     "name": "infra.openshift_virtualization_migration.postflight",
                                     "tasks_from": tasks_from}},
                                 {"ansible.builtin.assert": {"that": checks}},
                             ]}]
                    runner = base / "play.json"
                    runner.write_text(json.dumps(play))
                    env = os.environ.copy()
                    env.update({"ANSIBLE_CONFIG": str(config),
                                "ANSIBLE_COLLECTIONS_PATH": str(collections.parent),
                                # Determinism insurance: resolve only the fake
                                # collections, never a sys-path copy.
                                "ANSIBLE_COLLECTIONS_SCAN_SYS_PATH": "false",
                                "POSTFLIGHT_TEST_FIXTURE": json.dumps(fixture),
                                "ANSIBLE_NOCOLOR": "1"})
                    command = ["ansible-playbook", "--inventory", "localhost,", str(runner)]
                    if fixture.get("check"):
                        command.append("--check")
                    result = subprocess.run(command, env=env, cwd=base, capture_output=True,
                                            text=True, timeout=90)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
