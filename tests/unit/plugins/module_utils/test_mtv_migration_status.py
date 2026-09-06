from __future__ import absolute_import, division, print_function

__metaclass__ = type

import pytest

from ansible_collections.infra.openshift_virtualization_migration.plugins.module_utils.mtv_migration_status import (
    interpret_migration_status,
)


def _make_resource(conditions=None, vms=None, name="test-migration", namespace="openshift-mtv"):
    resource = {
        "metadata": {"name": name, "namespace": namespace},
        "status": {},
    }
    if conditions is not None:
        resource["status"]["conditions"] = conditions
    if vms is not None:
        resource["status"]["vms"] = vms
    return resource


def _make_condition(cond_type, status="True"):
    return {"type": cond_type, "status": status}


def _make_vm(name, phase="Completed", started="2025-01-01T00:00:00Z",
             completed=None, pipeline=None, error=None):
    vm = {"name": name, "phase": phase, "started": started}
    if completed is not None:
        vm["completed"] = completed
    if pipeline is not None:
        vm["pipeline"] = pipeline
    if error is not None:
        vm["error"] = error
    return vm


class TestInterpretMigrationStatusConditions:

    def test_succeeded(self):
        resource = _make_resource(conditions=[_make_condition("Succeeded")])
        result = interpret_migration_status(resource)
        assert result["status"] == "Succeeded"
        assert result["complete"] is True
        assert result["succeeded"] is True

    def test_failed(self):
        resource = _make_resource(conditions=[_make_condition("Failed")])
        result = interpret_migration_status(resource)
        assert result["status"] == "Failed"
        assert result["complete"] is True
        assert result["succeeded"] is False

    def test_canceled(self):
        resource = _make_resource(conditions=[_make_condition("Canceled")])
        result = interpret_migration_status(resource)
        assert result["status"] == "Canceled"
        assert result["complete"] is True
        assert result["succeeded"] is False

    def test_running(self):
        resource = _make_resource(conditions=[_make_condition("Running")])
        result = interpret_migration_status(resource)
        assert result["status"] == "Running"
        assert result["complete"] is False
        assert result["succeeded"] is False

    def test_pending_no_conditions(self):
        resource = _make_resource(conditions=[])
        result = interpret_migration_status(resource)
        assert result["status"] == "Pending"
        assert result["complete"] is False
        assert result["succeeded"] is False

    def test_pending_missing_conditions(self):
        resource = _make_resource()
        result = interpret_migration_status(resource)
        assert result["status"] == "Pending"
        assert result["complete"] is False

    def test_condition_with_false_status_ignored(self):
        resource = _make_resource(conditions=[
            _make_condition("Succeeded", status="False"),
            _make_condition("Running"),
        ])
        result = interpret_migration_status(resource)
        assert result["status"] == "Running"
        assert result["complete"] is False

    def test_succeeded_takes_priority_over_failed(self):
        resource = _make_resource(conditions=[
            _make_condition("Failed"),
            _make_condition("Succeeded"),
        ])
        result = interpret_migration_status(resource)
        assert result["status"] == "Succeeded"
        assert result["succeeded"] is True

    def test_failed_takes_priority_over_canceled(self):
        resource = _make_resource(conditions=[
            _make_condition("Canceled"),
            _make_condition("Failed"),
        ])
        result = interpret_migration_status(resource)
        assert result["status"] == "Failed"

    def test_terminal_takes_priority_over_running(self):
        resource = _make_resource(conditions=[
            _make_condition("Running"),
            _make_condition("Succeeded"),
        ])
        result = interpret_migration_status(resource)
        assert result["status"] == "Succeeded"
        assert result["complete"] is True


class TestInterpretMigrationStatusVMs:

    def test_vm_counts(self):
        vms = [
            _make_vm("vm-1", completed="2025-01-01T01:00:00Z"),
            _make_vm("vm-2", completed="2025-01-01T01:00:00Z"),
            _make_vm("vm-3", phase="Running"),
        ]
        resource = _make_resource(conditions=[_make_condition("Running")], vms=vms)
        result = interpret_migration_status(resource)
        assert result["total_vms"] == 3
        assert result["completed_vms"] == 2
        assert result["failed_vms"] == 0
        assert result["failed_vm_names"] == []

    def test_failed_vm_tracking(self):
        vms = [
            _make_vm("vm-1", completed="2025-01-01T01:00:00Z"),
            _make_vm("vm-2", error="disk transfer failed"),
            _make_vm("vm-3", error="network timeout"),
        ]
        resource = _make_resource(conditions=[_make_condition("Failed")], vms=vms)
        result = interpret_migration_status(resource)
        assert result["failed_vms"] == 2
        assert result["failed_vm_names"] == ["vm-2", "vm-3"]

    def test_vm_details_extraction(self):
        pipeline = [
            {"name": "DiskTransfer", "phase": "Completed"},
            {"name": "Cutover", "phase": "Running"},
        ]
        vms = [_make_vm("vm-1", phase="Running", started="2025-01-01T00:00:00Z", pipeline=pipeline)]
        resource = _make_resource(conditions=[_make_condition("Running")], vms=vms)
        result = interpret_migration_status(resource)

        assert len(result["vms"]) == 1
        vm = result["vms"][0]
        assert vm["name"] == "vm-1"
        assert vm["phase"] == "Running"
        assert vm["started"] == "2025-01-01T00:00:00Z"
        assert vm["completed"] == "N/A"
        assert len(vm["pipeline"]) == 2
        assert vm["pipeline"][0] == {"name": "DiskTransfer", "phase": "Completed"}
        assert vm["pipeline"][1] == {"name": "Cutover", "phase": "Running"}
        assert "error" not in vm

    def test_vm_with_error_includes_error_field(self):
        vms = [_make_vm("vm-1", error="something broke")]
        resource = _make_resource(conditions=[_make_condition("Failed")], vms=vms)
        result = interpret_migration_status(resource)
        assert result["vms"][0]["error"] == "something broke"

    def test_empty_vms(self):
        resource = _make_resource(conditions=[_make_condition("Running")], vms=[])
        result = interpret_migration_status(resource)
        assert result["total_vms"] == 0
        assert result["completed_vms"] == 0
        assert result["failed_vms"] == 0
        assert result["vms"] == []

    def test_missing_vms(self):
        resource = _make_resource(conditions=[_make_condition("Running")])
        result = interpret_migration_status(resource)
        assert result["total_vms"] == 0
        assert result["vms"] == []


class TestInterpretMigrationStatusMetadata:

    def test_metadata_extraction(self):
        resource = _make_resource(name="my-migration", namespace="my-ns")
        result = interpret_migration_status(resource)
        assert result["migration_name"] == "my-migration"
        assert result["migration_namespace"] == "my-ns"

    def test_missing_metadata(self):
        resource = {"status": {}}
        result = interpret_migration_status(resource)
        assert result["migration_name"] == ""
        assert result["migration_namespace"] == ""

    def test_missing_status(self):
        resource = {"metadata": {"name": "test", "namespace": "ns"}}
        result = interpret_migration_status(resource)
        assert result["status"] == "Pending"
        assert result["complete"] is False
        assert result["total_vms"] == 0
