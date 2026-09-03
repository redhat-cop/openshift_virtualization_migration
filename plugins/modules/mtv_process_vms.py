from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: mtv_process_vms
short_description: Process VMs for MTV migration plans
version_added: "1.26.0"
description:
  - Processes VM and folder specifications against a Forklift inventory to
    produce ready-to-apply Plan CRD manifests.
options:
  inventory_vms:
    description: VM inventory list from the Forklift API.
    type: list
    elements: dict
    required: true
  inventory_folders:
    description: Folder inventory list from the Forklift API.
    type: list
    elements: dict
    required: false
    default: []
  requested_vms:
    description: VM specifications from the migration request.
    type: list
    elements: dict
    required: false
    default: []
  requested_folders:
    description: Folder specifications from the migration request.
    type: list
    elements: dict
    required: false
    default: []
  vm_overrides:
    description: Global VM overrides applied to all VMs.
    type: dict
    required: false
    default: {}
  plan_skeleton:
    description: Rendered Plan CRD template to merge VM lists into.
    type: dict
    required: true
  plan_base_name:
    description: Base name for generated plan resources.
    type: str
    required: true
  split_plans:
    description: Whether to split VMs across multiple plans.
    type: bool
    default: false
  vms_per_plan:
    description: Maximum VMs per plan when splitting is enabled.
    type: int
    default: 10
author:
  - Red Hat Community of Practice
"""

EXAMPLES = r"""
- name: Process VMs and generate migration plans
  infra.openshift_virtualization_migration.mtv_process_vms:
    inventory_vms: "{{ _mtv_migrate_mtv_inventory_vms }}"
    inventory_folders: "{{ _mtv_migrate_mtv_inventory_folders | default([]) }}"
    requested_vms: "{{ mtv_plans_migration_request['vms'] | default([]) }}"
    requested_folders: "{{ mtv_plans_migration_request['folders'] | default([]) }}"
    vm_overrides: "{{ mtv_plans_migration_request['vm_overrides'] | default({}) }}"
    plan_skeleton: "{{ _mtv_migrate_mtv_plan_skeleton }}"
    plan_base_name: "{{ _mtv_migrate_mtv_plan_base_name }}"
    split_plans: "{{ _mtv_migrate_mtv_split_plans | bool }}"
    vms_per_plan: "{{ _mtv_migrate_mtv_vms_per_plan | int }}"
  register: _mtv_migrate_process_result
"""

RETURN = r"""
plans:
  description: Fully assembled Plan CRD manifests ready for k8s apply.
  type: list
  elements: dict
  returned: success
vms_to_migrate:
  description: Flat list of processed VMs included in plans.
  type: list
  elements: dict
  returned: success
skipped_vms:
  description: VMs that were excluded or skipped.
  type: list
  elements: dict
  returned: success
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.infra.openshift_virtualization_migration.plugins.module_utils.mtv_vm_processor import (
    process_vms,
)


def main():
    argument_spec = dict(
        inventory_vms=dict(type="list", elements="dict", required=True),
        inventory_folders=dict(type="list", elements="dict", required=False, default=[]),
        requested_vms=dict(type="list", elements="dict", required=False, default=[]),
        requested_folders=dict(type="list", elements="dict", required=False, default=[]),
        vm_overrides=dict(type="dict", required=False, default={}),
        plan_skeleton=dict(type="dict", required=True),
        plan_base_name=dict(type="str", required=True),
        split_plans=dict(type="bool", default=False),
        vms_per_plan=dict(type="int", default=10),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    plans, vms_to_migrate, skipped_vms, error = process_vms(
        inventory_vms=module.params["inventory_vms"],
        inventory_folders=module.params["inventory_folders"],
        requested_vms=module.params["requested_vms"],
        requested_folders=module.params["requested_folders"],
        vm_overrides=module.params["vm_overrides"],
        plan_skeleton=module.params["plan_skeleton"],
        plan_base_name=module.params["plan_base_name"],
        split_plans=module.params["split_plans"],
        vms_per_plan=module.params["vms_per_plan"],
    )

    if error:
        module.fail_json(msg=error)

    module.exit_json(
        changed=False,
        plans=plans,
        vms_to_migrate=vms_to_migrate,
        skipped_vms=skipped_vms,
    )


if __name__ == "__main__":
    main()
