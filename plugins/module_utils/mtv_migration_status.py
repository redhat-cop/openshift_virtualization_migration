from __future__ import absolute_import, division, print_function

__metaclass__ = type


def _evaluate_conditions(conditions):
    terminal_map = {}
    running = False

    for condition in conditions:
        cond_type = condition.get("type", "")
        cond_status = condition.get("status", "")

        if cond_type in ("Succeeded", "Failed", "Canceled") and cond_status == "True":
            terminal_map[cond_type] = True
        elif cond_type == "Running" and cond_status == "True":
            running = True

    if "Succeeded" in terminal_map:
        return "Succeeded", True, True
    if "Failed" in terminal_map:
        return "Failed", True, False
    if "Canceled" in terminal_map:
        return "Canceled", True, False
    if running:
        return "Running", False, False

    return "Pending", False, False


def _extract_vm_details(vms):
    details = []
    completed_count = 0
    failed_count = 0
    failed_names = []

    for vm in vms:
        name = vm.get("name", "unknown")

        pipeline_steps = []
        for step in vm.get("pipeline", []):
            pipeline_steps.append({
                "name": step.get("name", ""),
                "phase": step.get("phase", ""),
            })

        detail = {
            "name": name,
            "phase": vm.get("phase", "unknown"),
            "started": vm.get("started", "N/A"),
            "completed": vm.get("completed", "N/A"),
            "pipeline": pipeline_steps,
        }

        error = vm.get("error")
        if error is not None:
            detail["error"] = error
            failed_count += 1
            failed_names.append(name)

        if isinstance(vm.get("completed"), str) and vm["completed"]:
            completed_count += 1

        details.append(detail)

    return details, completed_count, failed_count, failed_names


def interpret_migration_status(resource):
    metadata = resource.get("metadata", {})
    status = resource.get("status", {})
    conditions = status.get("conditions", [])
    vms = status.get("vms", [])

    migration_status, complete, succeeded = _evaluate_conditions(conditions)
    vm_details, completed_vms, failed_vms, failed_vm_names = _extract_vm_details(vms)

    return {
        "migration_name": metadata.get("name", ""),
        "migration_namespace": metadata.get("namespace", ""),
        "status": migration_status,
        "complete": complete,
        "succeeded": succeeded,
        "total_vms": len(vms),
        "completed_vms": completed_vms,
        "failed_vms": failed_vms,
        "failed_vm_names": failed_vm_names,
        "vms": vm_details,
        "conditions": conditions,
    }
