from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: mtv_migration_status
short_description: Interpret the status of an MTV Migration resource
version_added: "1.26.0"
description:
  - Takes a Forklift Migration custom resource dict and returns structured
    status information including overall migration state, per-VM details,
    and completion indicators.
  - Designed to be used with kubernetes.core.k8s_info in an until/retries/delay
    loop for polling migration progress.
options:
  resource:
    description: >-
      The full Migration custom resource dict as returned by
      kubernetes.core.k8s_info (a single resource, not the list).
    type: dict
    required: true
author:
  - Red Hat Community of Practice
"""

EXAMPLES = r"""
- name: Fetch Migration resource
  kubernetes.core.k8s_info:
    api_version: forklift.konveyor.io/v1beta1
    kind: Migration
    name: "{{ migration_name }}"
    namespace: "{{ migration_namespace }}"
  register: _migration_query

- name: Interpret Migration status
  infra.openshift_virtualization_migration.mtv_migration_status:
    resource: "{{ _migration_query.resources | first }}"
  register: _migration_status
  until: _migration_status.complete | bool
  retries: 360
  delay: 20
"""

RETURN = r"""
migration_name:
  description: Name of the Migration resource.
  type: str
  returned: always
migration_namespace:
  description: Namespace of the Migration resource.
  type: str
  returned: always
status:
  description: Overall migration status (Succeeded, Failed, Canceled, Running, Pending).
  type: str
  returned: always
complete:
  description: Whether the migration reached a terminal condition.
  type: bool
  returned: always
succeeded:
  description: Whether the migration completed successfully.
  type: bool
  returned: always
total_vms:
  description: Total number of VMs in the migration.
  type: int
  returned: always
completed_vms:
  description: Number of VMs that completed migration.
  type: int
  returned: always
failed_vms:
  description: Number of VMs that failed migration.
  type: int
  returned: always
failed_vm_names:
  description: Names of VMs that failed.
  type: list
  elements: str
  returned: always
vms:
  description: Per-VM migration details.
  type: list
  elements: dict
  returned: always
conditions:
  description: Raw conditions list from the Migration status.
  type: list
  elements: dict
  returned: always
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.infra.openshift_virtualization_migration.plugins.module_utils.mtv_migration_status import (
    interpret_migration_status,
)


def main():
    argument_spec = dict(
        resource=dict(type="dict", required=True),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    resource = module.params["resource"]

    if not isinstance(resource, dict):
        module.fail_json(msg="resource must be a dict representing a Migration CR")

    result = interpret_migration_status(resource)

    module.exit_json(changed=False, **result)


if __name__ == "__main__":
    main()
