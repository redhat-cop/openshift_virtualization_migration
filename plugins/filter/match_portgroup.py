from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
  name: match_portgroup
  short_description: Filters NADs matching a network name in the source-portgroup annotation
  version_added: 1.0.0
  author: ""
  description:
    - Filters a list of NetworkAttachmentDefinitions to find those whose
      source-portgroup annotation contains the given network name.
    - Supports comma-separated values in the annotation for multiple portgroups.
  options:
    _input:
      description: List of NAD objects from Forklift inventory.
      type: list
      required: true
    network_name:
      description: The network name to match against the annotation.
      type: string
      required: true
    annotation_key:
      description: The annotation key to check.
      type: string
      required: true
    namespace:
      description: Optional namespace to filter by.
      type: string
      required: false
"""

EXAMPLES = """
- name: Find NADs matching a portgroup name
  ansible.builtin.set_fact:
    matched: >-
      {{ nads | infra.openshift_virtualization_migration.match_portgroup(
        'VLAN100', 'infra.openshift-virtualization-migration/source-portgroup') }}

- name: Find NADs matching a portgroup name in a specific namespace
  ansible.builtin.set_fact:
    matched: >-
      {{ nads | infra.openshift_virtualization_migration.match_portgroup(
        'VLAN100', 'infra.openshift-virtualization-migration/source-portgroup', 'my-namespace') }}
"""

RETURN = """
  _value:
    description: List of NAD objects whose annotation matches the network name.
    type: list
"""


def match_portgroup(nads, network_name, annotation_key, namespace=""):
    """Filter NADs whose source-portgroup annotation contains the network name.

    Supports both single-value and comma-separated annotations.
    """
    results = []
    for nad in nads:
        try:
            annotations = (
                nad.get("object", {}).get("metadata", {}).get("annotations", {})
            )
            annotation_value = annotations.get(annotation_key, "")
            portgroups = [
                pg.strip() for pg in annotation_value.split(",") if pg.strip()
            ]

            if network_name not in portgroups:
                continue

            if namespace and namespace.strip():
                nad_namespace = (
                    nad.get("object", {}).get("metadata", {}).get("namespace", "")
                )
                if nad_namespace != namespace.strip():
                    continue

            results.append(nad)
        except (AttributeError, TypeError):
            continue
    return results


class FilterModule(object):
    """Filter to match portgroup annotations"""

    def filters(self):
        return {
            "match_portgroup": match_portgroup,
        }
