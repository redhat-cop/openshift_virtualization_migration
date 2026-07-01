# ocp_cleanup

Remove OpenShift cluster artifacts created during virtualization migration testing. Handles MTV CRDs, provider secrets, migrated VMs/PVCs, and optionally operator teardown.

## Requirements

- OpenShift cluster access (kubeconfig or API key)
- `kubernetes.core` >= 5.2.0
- `redhat.openshift` >= 4.0.0

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ocp_cleanup_openshift_host` | env lookup | OpenShift API host |
| `ocp_cleanup_openshift_api_key` | env lookup | OpenShift API key |
| `ocp_cleanup_openshift_verify_ssl` | `true` | Validate TLS certificates |
| `ocp_cleanup_mtv_namespace` | `openshift-mtv` | MTV operator namespace |
| `ocp_cleanup_dry_run` | `false` | Query and report only, no deletions |
| `ocp_cleanup_mtv_migrations_remove` | `true` | Remove Migration CRDs |
| `ocp_cleanup_mtv_plans_remove` | `true` | Remove Plan CRDs |
| `ocp_cleanup_mtv_maps_remove` | `true` | Remove NetworkMap/StorageMap CRDs |
| `ocp_cleanup_mtv_providers_remove` | `true` | Remove Provider CRDs |
| `ocp_cleanup_mtv_secrets_remove` | `true` | Remove provider/VDDK secrets |
| `ocp_cleanup_migrated_vms_remove` | `false` | Remove migrated VMs and PVCs (destructive) |
| `ocp_cleanup_target_namespaces_remove` | `false` | Remove target namespaces (destructive) |
| `ocp_cleanup_target_namespaces` | `[]` | List of target namespaces to clean |
| `ocp_cleanup_operators_remove` | `false` | Remove operators (slow to reinstall) |
| `ocp_cleanup_operators` | all 8 | Operator list to remove |
| `ocp_cleanup_providers` | `[vmware, ovirt]` | Provider types to target |

## Deletion Order

Resources are removed respecting Kubernetes finalizer dependencies:

1. MTV Migrations
2. MTV Plans
3. NetworkMaps, StorageMaps
4. Providers
5. Provider/VDDK Secrets
6. Migrated VMs (optional)
7. PVCs (optional)
8. Target Namespaces (optional)
9. Operators: CRs → CSVs → Subscriptions → OperatorGroups → Namespaces (optional)

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - role: infra.openshift_virtualization_migration.ocp_cleanup
      vars:
        ocp_cleanup_dry_run: true
        ocp_cleanup_operators_remove: true
```

## License

GPL-3.0-or-later
