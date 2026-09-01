from __future__ import absolute_import, division, print_function

__metaclass__ = type

import copy


def build_vm_index(inventory_vms):
    by_id = {}
    by_name = {}
    by_path = {}

    for vm in inventory_vms:
        vm_id = vm.get("id", "")
        vm_name = vm.get("name", "")
        vm_path = vm.get("path", "")

        if vm_id:
            by_id[vm_id] = vm
        if vm_name:
            by_name.setdefault(vm_name, []).append(vm)
        if vm_path:
            by_path[vm_path] = vm

    return by_id, by_name, by_path


def build_folder_index(inventory_folders):
    by_id = {}
    by_name = {}
    by_path = {}

    for folder in inventory_folders:
        folder_id = folder.get("id", "")
        folder_name = folder.get("name", "")
        folder_path = folder.get("path", "")

        if folder_id:
            by_id[folder_id] = folder
        if folder_name:
            by_name.setdefault(folder_name, []).append(folder)
        if folder_path:
            by_path[folder_path] = folder

    return by_id, by_name, by_path


def build_exclusion_sets(requested_vms):
    excluded_names = set()
    excluded_ids = set()
    excluded_paths = set()

    for vm in requested_vms:
        if vm.get("exclude", False):
            if "name" in vm:
                excluded_names.add(vm["name"])
            if "id" in vm:
                excluded_ids.add(vm["id"])
            if "path" in vm:
                excluded_paths.add(vm["path"])

    return excluded_names, excluded_ids, excluded_paths


def build_folder_exclusion_sets(requested_folders):
    excluded_names = set()
    excluded_ids = set()
    excluded_paths = set()

    for folder in requested_folders:
        if folder.get("exclude", False):
            if "name" in folder:
                excluded_names.add(folder["name"])
            if "id" in folder:
                excluded_ids.add(folder["id"])
            if "path" in folder:
                excluded_paths.add(folder["path"])

    return excluded_names, excluded_ids, excluded_paths


def resolve_vm(vm_spec, by_id, by_name, by_path):
    has_id = "id" in vm_spec
    has_name = "name" in vm_spec
    has_path = "path" in vm_spec

    if not (has_id or has_name or has_path):
        return None, "'name' or 'id' or 'path' not specified for VM"

    if has_id and not has_name and not has_path:
        vm = by_id.get(vm_spec["id"])
        if vm is None:
            return None, "Failed to locate VM with id of %s" % vm_spec["id"]
        return vm, None

    if has_name and not has_id and not has_path:
        candidates = by_name.get(vm_spec["name"], [])
        if len(candidates) != 1:
            return None, "Failed to locate VM with %s" % vm_spec["name"]
        return candidates[0], None

    if has_path and not has_id and not has_name:
        vm = by_path.get(vm_spec["path"])
        if vm is None:
            return None, "Failed to locate VM with path of %s" % vm_spec["path"]
        return vm, None

    return None, "'name', 'id', and 'path' are mutually exclusive for VM lookup"


def resolve_folder(folder_spec, by_id, by_name, by_path):
    has_id = "id" in folder_spec
    has_name = "name" in folder_spec
    has_path = "path" in folder_spec

    if not (has_id or has_name or has_path):
        return None, "'name' or 'id' or 'path' not specified for Folder"

    if has_id and not has_name and not has_path:
        folder = by_id.get(folder_spec["id"])
        if folder is None:
            return None, "Failed to locate Folder with id of %s" % folder_spec["id"]
        return folder, None

    if has_name and not has_id and not has_path:
        candidates = by_name.get(folder_spec["name"], [])
        if len(candidates) != 1:
            return None, "Failed to locate Folder with %s" % folder_spec["name"]
        return candidates[0], None

    if has_path and not has_id and not has_name:
        folder = by_path.get(folder_spec["path"])
        if folder is None:
            return (
                None,
                "Failed to locate Folder with path of %s" % folder_spec["path"],
            )
        return folder, None

    return None, "'name', 'id', and 'path' are mutually exclusive for Folder lookup"


def is_vm_excluded(vm, excluded_names, excluded_ids, excluded_paths):
    if vm.get("name", "") in excluded_names:
        return True
    if vm.get("id", "") in excluded_ids:
        return True
    if vm.get("path", "") in excluded_paths:
        return True
    return False


def is_folder_excluded(folder, excluded_names, excluded_ids, excluded_paths):
    if folder.get("name", "") in excluded_names:
        return True
    if folder.get("id", "") in excluded_ids:
        return True
    if folder.get("path", "") in excluded_paths:
        return True
    return False


def merge_overrides(base, *override_dicts):
    result = dict(base)
    for overrides in override_dicts:
        if overrides:
            result = _deep_merge(result, overrides)
    return result


def _deep_merge(base, override):
    result = dict(base)
    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def process_vm_entry(
    vm_spec,
    vm_index,
    excluded_names,
    excluded_ids,
    excluded_paths,
    vm_overrides,
    folder_overrides=None,
):
    by_id, by_name, by_path = vm_index
    resolved_vm, error = resolve_vm(vm_spec, by_id, by_name, by_path)
    if error:
        return None, None, error

    if resolved_vm.get("isTemplate", False):
        return None, {"id": resolved_vm["id"], "name": resolved_vm.get("name", ""), "reason": "template"}, None

    if is_vm_excluded(resolved_vm, excluded_names, excluded_ids, excluded_paths):
        return None, {"id": resolved_vm["id"], "name": resolved_vm.get("name", ""), "reason": "excluded"}, None

    vm_entry = {"id": resolved_vm["id"], "name": resolved_vm["name"]}
    vm_entry = merge_overrides(
        vm_entry,
        folder_overrides or {},
        vm_overrides,
        vm_spec.get("overrides", {}),
    )

    return vm_entry, None, None


def process_folder_recursive(
    folder_spec,
    folder_index,
    vm_index,
    excluded_vm_names,
    excluded_vm_ids,
    excluded_vm_paths,
    folder_excluded_names,
    folder_excluded_ids,
    folder_excluded_paths,
    vm_overrides,
    result_dict,
    skipped_list,
):
    by_id, by_name, by_path = folder_index
    resolved_folder, error = resolve_folder(folder_spec, by_id, by_name, by_path)
    if error:
        return error

    if is_folder_excluded(
        resolved_folder,
        folder_excluded_names,
        folder_excluded_ids,
        folder_excluded_paths,
    ):
        return None

    folder_overrides = folder_spec.get("overrides", {})
    children = resolved_folder.get("children", [])

    for child in children:
        if child.get("kind") == "VM":
            child_vm_spec = {"id": child["id"]}
            vm_entry, skipped, err = process_vm_entry(
                child_vm_spec,
                vm_index,
                excluded_vm_names,
                excluded_vm_ids,
                excluded_vm_paths,
                vm_overrides,
                folder_overrides=folder_overrides,
            )
            if err:
                return err
            if skipped:
                skipped_list.append(skipped)
            elif vm_entry:
                result_dict[vm_entry["id"]] = vm_entry

        elif child.get("kind") == "Folder":
            child_folder_spec = {
                "id": child["id"],
                "overrides": folder_overrides,
            }
            err = process_folder_recursive(
                child_folder_spec,
                folder_index,
                vm_index,
                excluded_vm_names,
                excluded_vm_ids,
                excluded_vm_paths,
                folder_excluded_names,
                folder_excluded_ids,
                folder_excluded_paths,
                vm_overrides,
                result_dict,
                skipped_list,
            )
            if err:
                return err

    return None


def batch_into_plans(vms, plan_skeleton, plan_base_name, split_plans, vms_per_plan):
    if not vms:
        return []

    if split_plans and vms_per_plan > 0:
        batches = [vms[i : i + vms_per_plan] for i in range(0, len(vms), vms_per_plan)]
    else:
        batches = [vms]

    plans = []
    needs_suffix = split_plans and len(vms) > vms_per_plan

    for idx, batch in enumerate(batches):
        plan = copy.deepcopy(plan_skeleton)
        plan_name = plan_base_name
        if needs_suffix:
            plan_name = "%s-%d" % (plan_base_name, idx)

        plan.setdefault("metadata", {})["name"] = plan_name
        plan.setdefault("spec", {})["vms"] = batch
        plans.append(plan)

    return plans


def process_vms(
    inventory_vms,
    inventory_folders,
    requested_vms,
    requested_folders,
    vm_overrides,
    plan_skeleton,
    plan_base_name,
    split_plans,
    vms_per_plan,
):
    vm_index = build_vm_index(inventory_vms)
    folder_index = build_folder_index(inventory_folders)

    excluded_vm_names, excluded_vm_ids, excluded_vm_paths = build_exclusion_sets(
        requested_vms
    )
    (
        folder_excluded_names,
        folder_excluded_ids,
        folder_excluded_paths,
    ) = build_folder_exclusion_sets(requested_folders)

    result_dict = {}
    skipped_list = []

    for folder_spec in requested_folders:
        if folder_spec.get("exclude", False):
            continue
        err = process_folder_recursive(
            folder_spec,
            folder_index,
            vm_index,
            excluded_vm_names,
            excluded_vm_ids,
            excluded_vm_paths,
            folder_excluded_names,
            folder_excluded_ids,
            folder_excluded_paths,
            vm_overrides,
            result_dict,
            skipped_list,
        )
        if err:
            return None, None, None, err

    for vm_spec in requested_vms:
        if vm_spec.get("exclude", False):
            continue
        vm_entry, skipped, err = process_vm_entry(
            vm_spec,
            vm_index,
            excluded_vm_names,
            excluded_vm_ids,
            excluded_vm_paths,
            vm_overrides,
        )
        if err:
            return None, None, None, err
        if skipped:
            skipped_list.append(skipped)
        elif vm_entry:
            result_dict[vm_entry["id"]] = vm_entry

    vms_to_migrate = list(result_dict.values())

    if not vms_to_migrate:
        return None, None, None, "No VM's exist in plan"

    plans = batch_into_plans(
        vms_to_migrate, plan_skeleton, plan_base_name, split_plans, vms_per_plan
    )

    return plans, vms_to_migrate, skipped_list, None
