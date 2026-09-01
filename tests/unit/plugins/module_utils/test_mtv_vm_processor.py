from __future__ import absolute_import, division, print_function

__metaclass__ = type

import time

import pytest

from ansible_collections.infra.openshift_virtualization_migration.plugins.module_utils.mtv_vm_processor import (
    batch_into_plans,
    build_exclusion_sets,
    build_folder_exclusion_sets,
    build_folder_index,
    build_vm_index,
    is_folder_excluded,
    is_vm_excluded,
    merge_overrides,
    process_folder_recursive,
    process_vm_entry,
    process_vms,
    resolve_folder,
    resolve_vm,
)


def _make_vm(vm_id, name, path="", is_template=False):
    return {
        "id": vm_id,
        "name": name,
        "path": path or "/dc/vm/%s" % name,
        "isTemplate": is_template,
    }


def _make_folder(folder_id, name, path="", children=None):
    folder = {
        "id": folder_id,
        "name": name,
        "path": path or "/dc/vm/%s" % name,
    }
    if children is not None:
        folder["children"] = children
    return folder


PLAN_SKELETON = {
    "apiVersion": "forklift.konveyor.io/v1beta1",
    "kind": "Plan",
    "metadata": {"name": "", "namespace": "openshift-mtv"},
    "spec": {"vms": []},
}


class TestBuildVmIndex:
    def test_indexes_by_all_keys(self):
        vms = [_make_vm("vm-1", "web1", "/dc/vm/web1"), _make_vm("vm-2", "web2", "/dc/vm/web2")]
        by_id, by_name, by_path = build_vm_index(vms)

        assert "vm-1" in by_id
        assert "vm-2" in by_id
        assert by_name["web1"] == [vms[0]]
        assert "/dc/vm/web2" in by_path

    def test_duplicate_names_indexed_as_list(self):
        vms = [_make_vm("vm-1", "web", "/dc/vm/web1"), _make_vm("vm-2", "web", "/dc/vm/web2")]
        _, by_name, _ = build_vm_index(vms)

        assert len(by_name["web"]) == 2

    def test_empty_inventory(self):
        by_id, by_name, by_path = build_vm_index([])
        assert by_id == {}
        assert by_name == {}
        assert by_path == {}


class TestBuildExclusionSets:
    def test_collects_excluded_entries(self):
        vms = [
            {"name": "excluded-vm", "exclude": True},
            {"name": "included-vm"},
            {"id": "vm-99", "exclude": True},
            {"path": "/dc/vm/skip", "exclude": True},
        ]
        names, ids, paths = build_exclusion_sets(vms)

        assert "excluded-vm" in names
        assert "included-vm" not in names
        assert "vm-99" in ids
        assert "/dc/vm/skip" in paths

    def test_empty_list(self):
        names, ids, paths = build_exclusion_sets([])
        assert names == set()
        assert ids == set()
        assert paths == set()

    def test_exclude_false_not_collected(self):
        vms = [{"name": "vm1", "exclude": False}]
        names, _, _ = build_exclusion_sets(vms)
        assert "vm1" not in names


class TestResolveVm:
    def test_resolve_by_name(self):
        vms = [_make_vm("vm-1", "web1")]
        by_id, by_name, by_path = build_vm_index(vms)
        vm, err = resolve_vm({"name": "web1"}, by_id, by_name, by_path)
        assert err is None
        assert vm["id"] == "vm-1"

    def test_resolve_by_id(self):
        vms = [_make_vm("vm-1", "web1")]
        by_id, by_name, by_path = build_vm_index(vms)
        vm, err = resolve_vm({"id": "vm-1"}, by_id, by_name, by_path)
        assert err is None
        assert vm["name"] == "web1"

    def test_resolve_by_path(self):
        vms = [_make_vm("vm-1", "web1", "/dc/vm/web1")]
        by_id, by_name, by_path = build_vm_index(vms)
        vm, err = resolve_vm({"path": "/dc/vm/web1"}, by_id, by_name, by_path)
        assert err is None
        assert vm["id"] == "vm-1"

    def test_not_found_by_name(self):
        by_id, by_name, by_path = build_vm_index([])
        vm, err = resolve_vm({"name": "missing"}, by_id, by_name, by_path)
        assert vm is None
        assert "Failed to locate VM" in err

    def test_not_found_by_id(self):
        by_id, by_name, by_path = build_vm_index([])
        vm, err = resolve_vm({"id": "missing-id"}, by_id, by_name, by_path)
        assert vm is None
        assert "Failed to locate VM" in err

    def test_duplicate_name_fails(self):
        vms = [_make_vm("vm-1", "web", "/dc/vm/web1"), _make_vm("vm-2", "web", "/dc/vm/web2")]
        by_id, by_name, by_path = build_vm_index(vms)
        vm, err = resolve_vm({"name": "web"}, by_id, by_name, by_path)
        assert vm is None
        assert "Failed to locate VM" in err

    def test_no_identifier_fails(self):
        by_id, by_name, by_path = build_vm_index([])
        vm, err = resolve_vm({}, by_id, by_name, by_path)
        assert vm is None
        assert "not specified" in err

    def test_multiple_identifiers_fails(self):
        vms = [_make_vm("vm-1", "web1")]
        by_id, by_name, by_path = build_vm_index(vms)
        vm, err = resolve_vm({"name": "web1", "id": "vm-1"}, by_id, by_name, by_path)
        assert vm is None
        assert "mutually exclusive" in err


class TestIsVmExcluded:
    def test_excluded_by_name(self):
        vm = _make_vm("vm-1", "web1")
        assert is_vm_excluded(vm, {"web1"}, set(), set())

    def test_excluded_by_id(self):
        vm = _make_vm("vm-1", "web1")
        assert is_vm_excluded(vm, set(), {"vm-1"}, set())

    def test_excluded_by_path(self):
        vm = _make_vm("vm-1", "web1", "/dc/vm/web1")
        assert is_vm_excluded(vm, set(), set(), {"/dc/vm/web1"})

    def test_not_excluded(self):
        vm = _make_vm("vm-1", "web1")
        assert not is_vm_excluded(vm, set(), set(), set())


class TestMergeOverrides:
    def test_simple_merge(self):
        result = merge_overrides({"id": "vm-1", "name": "web1"}, {"hooks": {"before": ["hook1"]}})
        assert result == {"id": "vm-1", "name": "web1", "hooks": {"before": ["hook1"]}}

    def test_precedence_order(self):
        base = {"id": "vm-1", "name": "web1"}
        folder = {"network": "net-a"}
        global_override = {"network": "net-b"}
        per_vm = {"network": "net-c"}
        result = merge_overrides(base, folder, global_override, per_vm)
        assert result["network"] == "net-c"

    def test_deep_merge(self):
        base = {"id": "vm-1", "spec": {"cpu": 2, "memory": "4Gi"}}
        override = {"spec": {"cpu": 4}}
        result = merge_overrides(base, override)
        assert result["spec"]["cpu"] == 4
        assert result["spec"]["memory"] == "4Gi"

    def test_empty_overrides_noop(self):
        base = {"id": "vm-1"}
        result = merge_overrides(base, {}, {}, {})
        assert result == base

    def test_none_overrides_handled(self):
        base = {"id": "vm-1"}
        result = merge_overrides(base, None, None)
        assert result == base


class TestProcessVmEntry:
    def test_basic_processing(self):
        vms = [_make_vm("vm-1", "web1")]
        vm_index = build_vm_index(vms)
        vm_entry, skipped, err = process_vm_entry(
            {"name": "web1"}, vm_index, set(), set(), set(), {}
        )
        assert err is None
        assert skipped is None
        assert vm_entry["id"] == "vm-1"
        assert vm_entry["name"] == "web1"

    def test_template_skipped(self):
        vms = [_make_vm("vm-1", "template-vm", is_template=True)]
        vm_index = build_vm_index(vms)
        vm_entry, skipped, err = process_vm_entry(
            {"name": "template-vm"}, vm_index, set(), set(), set(), {}
        )
        assert err is None
        assert vm_entry is None
        assert skipped["reason"] == "template"

    def test_excluded_vm_skipped(self):
        vms = [_make_vm("vm-1", "web1")]
        vm_index = build_vm_index(vms)
        vm_entry, skipped, err = process_vm_entry(
            {"name": "web1"}, vm_index, {"web1"}, set(), set(), {}
        )
        assert err is None
        assert vm_entry is None
        assert skipped["reason"] == "excluded"

    def test_overrides_applied(self):
        vms = [_make_vm("vm-1", "web1")]
        vm_index = build_vm_index(vms)
        vm_entry, _, _ = process_vm_entry(
            {"name": "web1", "overrides": {"network": "per-vm-net"}},
            vm_index,
            set(),
            set(),
            set(),
            {"network": "global-net"},
            folder_overrides={"network": "folder-net"},
        )
        assert vm_entry["network"] == "per-vm-net"

    def test_folder_overrides_lowest_priority(self):
        vms = [_make_vm("vm-1", "web1")]
        vm_index = build_vm_index(vms)
        vm_entry, _, _ = process_vm_entry(
            {"name": "web1"},
            vm_index,
            set(),
            set(),
            set(),
            {"network": "global-net"},
            folder_overrides={"network": "folder-net"},
        )
        assert vm_entry["network"] == "global-net"


class TestProcessFolderRecursive:
    def test_processes_child_vms(self):
        vms = [_make_vm("vm-1", "web1"), _make_vm("vm-2", "web2")]
        folder = _make_folder(
            "folder-1",
            "myfolder",
            children=[
                {"id": "vm-1", "kind": "VM"},
                {"id": "vm-2", "kind": "VM"},
            ],
        )
        vm_index = build_vm_index(vms)
        folder_index = build_folder_index([folder])
        result_dict = {}
        skipped = []
        err = process_folder_recursive(
            {"name": "myfolder"},
            folder_index,
            vm_index,
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            {},
            result_dict,
            skipped,
        )
        assert err is None
        assert len(result_dict) == 2

    def test_recursive_subfolders(self):
        vms = [_make_vm("vm-1", "deep-vm")]
        subfolder = _make_folder(
            "subfolder-1",
            "sub",
            children=[{"id": "vm-1", "kind": "VM"}],
        )
        parent = _make_folder(
            "folder-1",
            "parent",
            children=[{"id": "subfolder-1", "kind": "Folder"}],
        )
        vm_index = build_vm_index(vms)
        folder_index = build_folder_index([parent, subfolder])
        result_dict = {}
        skipped = []
        err = process_folder_recursive(
            {"name": "parent"},
            folder_index,
            vm_index,
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            {},
            result_dict,
            skipped,
        )
        assert err is None
        assert "vm-1" in result_dict

    def test_excluded_folder_skipped(self):
        vms = [_make_vm("vm-1", "web1")]
        folder = _make_folder(
            "folder-1",
            "skipme",
            children=[{"id": "vm-1", "kind": "VM"}],
        )
        vm_index = build_vm_index(vms)
        folder_index = build_folder_index([folder])
        result_dict = {}
        skipped = []
        err = process_folder_recursive(
            {"name": "skipme"},
            folder_index,
            vm_index,
            set(),
            set(),
            set(),
            {"skipme"},
            set(),
            set(),
            {},
            result_dict,
            skipped,
        )
        assert err is None
        assert len(result_dict) == 0

    def test_folder_overrides_applied_to_children(self):
        vms = [_make_vm("vm-1", "web1")]
        folder = _make_folder(
            "folder-1",
            "myfolder",
            children=[{"id": "vm-1", "kind": "VM"}],
        )
        vm_index = build_vm_index(vms)
        folder_index = build_folder_index([folder])
        result_dict = {}
        skipped = []
        err = process_folder_recursive(
            {"name": "myfolder", "overrides": {"network": "folder-net"}},
            folder_index,
            vm_index,
            set(),
            set(),
            set(),
            set(),
            set(),
            set(),
            {},
            result_dict,
            skipped,
        )
        assert err is None
        assert result_dict["vm-1"]["network"] == "folder-net"


class TestBatchIntoPlans:
    def test_single_plan_no_split(self):
        vms = [{"id": "vm-%d" % i, "name": "vm%d" % i} for i in range(5)]
        plans = batch_into_plans(vms, PLAN_SKELETON, "test-plan", False, 10)
        assert len(plans) == 1
        assert plans[0]["metadata"]["name"] == "test-plan"
        assert len(plans[0]["spec"]["vms"]) == 5

    def test_split_plans(self):
        vms = [{"id": "vm-%d" % i, "name": "vm%d" % i} for i in range(25)]
        plans = batch_into_plans(vms, PLAN_SKELETON, "test-plan", True, 10)
        assert len(plans) == 3
        assert plans[0]["metadata"]["name"] == "test-plan-0"
        assert plans[1]["metadata"]["name"] == "test-plan-1"
        assert plans[2]["metadata"]["name"] == "test-plan-2"
        assert len(plans[0]["spec"]["vms"]) == 10
        assert len(plans[1]["spec"]["vms"]) == 10
        assert len(plans[2]["spec"]["vms"]) == 5

    def test_no_suffix_when_fits_single_plan(self):
        vms = [{"id": "vm-%d" % i, "name": "vm%d" % i} for i in range(5)]
        plans = batch_into_plans(vms, PLAN_SKELETON, "test-plan", True, 10)
        assert len(plans) == 1
        assert plans[0]["metadata"]["name"] == "test-plan"

    def test_empty_vms_returns_empty(self):
        plans = batch_into_plans([], PLAN_SKELETON, "test-plan", False, 10)
        assert plans == []

    def test_skeleton_not_mutated(self):
        import copy

        original = copy.deepcopy(PLAN_SKELETON)
        vms = [{"id": "vm-1", "name": "vm1"}]
        batch_into_plans(vms, PLAN_SKELETON, "test-plan", False, 10)
        assert PLAN_SKELETON == original


class TestProcessVmsIntegration:
    def test_basic_vm_processing(self):
        inventory_vms = [
            _make_vm("vm-1", "web1"),
            _make_vm("vm-2", "web2"),
            _make_vm("vm-3", "db1"),
        ]
        plans, vms, skipped, err = process_vms(
            inventory_vms=inventory_vms,
            inventory_folders=[],
            requested_vms=[{"name": "web1"}, {"name": "web2"}],
            requested_folders=[],
            vm_overrides={},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=False,
            vms_per_plan=10,
        )
        assert err is None
        assert len(plans) == 1
        assert len(vms) == 2
        assert len(skipped) == 0

    def test_folder_and_vm_deduplication(self):
        inventory_vms = [_make_vm("vm-1", "web1"), _make_vm("vm-2", "web2")]
        inventory_folders = [
            _make_folder(
                "folder-1",
                "myfolder",
                children=[
                    {"id": "vm-1", "kind": "VM"},
                    {"id": "vm-2", "kind": "VM"},
                ],
            )
        ]
        plans, vms, skipped, err = process_vms(
            inventory_vms=inventory_vms,
            inventory_folders=inventory_folders,
            requested_vms=[{"name": "web1"}],
            requested_folders=[{"name": "myfolder"}],
            vm_overrides={},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=False,
            vms_per_plan=10,
        )
        assert err is None
        assert len(vms) == 2
        vm_ids = {v["id"] for v in vms}
        assert vm_ids == {"vm-1", "vm-2"}

    def test_exclusions_work(self):
        inventory_vms = [
            _make_vm("vm-1", "web1"),
            _make_vm("vm-2", "web2"),
            _make_vm("vm-3", "template-vm", is_template=True),
        ]
        plans, vms, skipped, err = process_vms(
            inventory_vms=inventory_vms,
            inventory_folders=[],
            requested_vms=[
                {"name": "web1"},
                {"name": "web2", "exclude": True},
                {"name": "template-vm"},
            ],
            requested_folders=[],
            vm_overrides={},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=False,
            vms_per_plan=10,
        )
        assert err is None
        assert len(vms) == 1
        assert vms[0]["name"] == "web1"
        assert len(skipped) == 1

    def test_no_vms_fails(self):
        _, _, _, err = process_vms(
            inventory_vms=[_make_vm("vm-1", "web1")],
            inventory_folders=[],
            requested_vms=[],
            requested_folders=[],
            vm_overrides={},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=False,
            vms_per_plan=10,
        )
        assert err is not None
        assert "No VM" in err

    def test_vm_not_found_fails(self):
        _, _, _, err = process_vms(
            inventory_vms=[_make_vm("vm-1", "web1")],
            inventory_folders=[],
            requested_vms=[{"name": "nonexistent"}],
            requested_folders=[],
            vm_overrides={},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=False,
            vms_per_plan=10,
        )
        assert err is not None
        assert "Failed to locate" in err

    def test_override_precedence_integration(self):
        inventory_vms = [_make_vm("vm-1", "web1")]
        inventory_folders = [
            _make_folder(
                "folder-1",
                "myfolder",
                children=[{"id": "vm-1", "kind": "VM"}],
            )
        ]
        plans, vms, _, err = process_vms(
            inventory_vms=inventory_vms,
            inventory_folders=inventory_folders,
            requested_vms=[{"name": "web1", "overrides": {"tier": "per-vm"}}],
            requested_folders=[{"name": "myfolder", "overrides": {"tier": "folder"}}],
            vm_overrides={"tier": "global"},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=False,
            vms_per_plan=10,
        )
        assert err is None
        vm = next(v for v in vms if v["id"] == "vm-1")
        assert vm["tier"] == "per-vm"

    def test_scale_performance(self):
        num_vms = 1000
        inventory_vms = [_make_vm("vm-%d" % i, "vm%d" % i) for i in range(num_vms)]
        requested_vms = [{"name": "vm%d" % i} for i in range(num_vms)]

        start = time.time()
        plans, vms, _, err = process_vms(
            inventory_vms=inventory_vms,
            inventory_folders=[],
            requested_vms=requested_vms,
            requested_folders=[],
            vm_overrides={},
            plan_skeleton=PLAN_SKELETON,
            plan_base_name="migration",
            split_plans=True,
            vms_per_plan=10,
        )
        elapsed = time.time() - start

        assert err is None
        assert len(vms) == num_vms
        assert len(plans) == 100
        assert elapsed < 1.0, "Processing %d VMs took %.2fs (should be <1s)" % (num_vms, elapsed)
