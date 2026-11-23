# Networking port from main to v2 (MFG-545)

The port uses `main` commit `f39aa98574aecee921658643eff75914d41b5145`
on top of `v2` commit `0f67e96177860c15746b8f49a421924f174f0648`.
It brings over the networking role and its dependencies, adapting mapping
behavior to V2's `mtv_maps` role. Unrelated V1 enhancements and the rest of
`mtv_management` are outside this change.

## Source traceability

| Source | Behavior carried into V2 |
| --- | --- |
| `roles/network_mgmt` at the source commit | Manual/automatic preparation, linux-bridge, ovs-bridge and OVN layer2 templates, validation and defaults |
| [PR #46](https://github.com/redhat-cop/openshift_virtualization_migration/pull/46) | OVN layer2 NADs without node network policies |
| [PR #85](https://github.com/redhat-cop/openshift_virtualization_migration/pull/85) | Global/per-NAD MTU precedence, omission when unset, validation |
| [PR #102](https://github.com/redhat-cop/openshift_virtualization_migration/pull/102) | Multiple source-portgroup annotations, matching filter, backward-compatible single annotations and explicit NAD override precedence |

The role is copied at the full source baseline, including earlier fixes and
validation. V2 adaptations are the injected credential defaults, configurable
certificate validation (enabled by default), corrected
`network_mgmt_portgroups_to_migrate` spelling, quiet debug output, and native
Ansible discovery transformations rather than JMESPath-specific list handling.
The old `mtv_management` tasks/templates are replaced by equivalent behavior in
`mtv_maps`, not imported alongside it.

## Prepare networks before creating maps

1. Seed/update AAP with `playbooks/vmf_seed_aap.yml` using the normal V2 process.
   The default template list now includes
   **OpenShift Virtualization Migration - Network Management**.
   If you override the entire `aap_seed_controller_templates` list, add the new
   template to that list explicitly.
2. Attach the V2 target environment credential and select `target_name`.
   It supplies `K8S_AUTH_*` connection variables for OpenShift.
3. For automatic VMware discovery also attach the V2 source environment
   credential, which supplies `VMWARE_HOST`, `VMWARE_USER`, `VMWARE_PASSWORD`
   and `VMWARE_VALIDATE_CERTS`. Explicit `network_mgmt_vcenter_*` variables
   remain supported. Trust the appropriate CA on the execution environment;
   certificate verification defaults to enabled. Never store passwords in Git.
4. Run `playbooks/vmf_network_mgmt.yml`, then the existing MTV Maps, Plans and
   Migrate templates as required. This change adds a preparation entry point;
   it does not silently add cluster-changing steps to the existing Maps job.

Example non-secret extra variables for manual network preparation:

```yaml
target_name: ocp-production
network_mgmt_openshift_network_bridge_mode: ovn-layer2
network_mgmt_nad_mtu: 9000
network_mgmt_manual_nad_list:
  - name: shared-app
    namespace: workloads
    portgroups:
      - site-a-app
      - site-b-app
  - name: services
    namespace: workloads
    portgroup: services
    mtu: 1500
```

Manual mode needs no vCenter lookup credentials. Automatic mode requires the
source credential, `network_mgmt_vcenter_datacenter` and
`network_mgmt_vcenter_dvswitch`; the existing physical bridge modes also need
appropriate node uplink/bridge settings. The caller must provide the relevant
permissions and installed NAD/NMState APIs. Review host-network changes before
running the linux/OVS bridge paths on a live cluster.

## V2 mapping variables

| V1 concept | V2 equivalent |
| --- | --- |
| `mtv_management_network_map_overrides` | `mtv_maps_network_map_overrides` |
| `network_attachment_definition` override | `nad: namespace/name`, optionally `destination_type: multus` |
| source network selection | V2 override `id` from MTV inventory |
| source-portgroup annotation | Same annotation key, matched by `match_portgroup` |

For example, an explicit selection remains effective even if annotation matching
finds nothing:

```yaml
mtv_maps_network_map_overrides:
  - id: network-123
    nad: workloads/shared-app
```

`nad` without `destination_type` implies `multus`. An explicitly selected `pod`
or `ignored` destination takes precedence. A network with no matching annotation
and no override retains V2's pod-network fallback. Invalid explicit destinations
fail before mapping. Multiple matching NADs retain V2's first-match warning.

A single `portgroup` and a `portgroups` list are mutually exclusive. Commas are
annotation separators, so source names containing literal commas must use an
explicit V2 map override. That limitation is inherited from the source design.

## Validation and remaining release checks

`tests/unit/roles/test_networking_v2.py` runs the real Ansible role tasks,
validations, templates and V2 destination-resolution tasks. External VMware and
OpenShift modules use local fixtures, including an idempotent local resource
store. The fixtures never contact a real cluster. Filter tests also cover
malformed metadata, exact matching and namespace selection.

Run with the repository's supported Python/Ansible environment:

```shell
python3 -m pytest -o addopts='' tests/unit/roles/test_networking_v2.py -q
ansible-lint -c .ansible-lint-ci --offline roles/network_mgmt \
  playbooks/vmf_network_mgmt.yml \
  roles/mtv_maps/tasks/_resolve_network_destination.yml
ansible-galaxy collection build
```

The full CI configuration still needs actual collection dependencies and any
required private Automation Hub access. The local tests do not prove live
vSphere connectivity, cluster policy readiness, AAP credential injection,
physical networking, guest connectivity, or a complete migration. Review and
merge into `v2`, and validate those behaviors in an authorized test environment
before closing the delivery task. Existing V2 architecture proposals for
NNCP-ready polling and apply retries remain separate hardening work; this port
does not claim to deliver them.
