# cluster_healthcheck

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
```

Description: Cluster health validation for OpenShift Virtualization migration environments.

## Requirements

- OpenShift cluster with `kubeconfig` configured
- `kubernetes.core` collection installed
- OpenShift Virtualization (CNV) operator installed
- Migration Toolkit for Virtualization (MTV) operator installed

## Role Variables

### Defaults

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `cluster_healthcheck_checks` | list | See defaults/main.yml | List of health checks to run |
| `cluster_healthcheck_post_migration_vms` | list | `[]` | VMs to check post-migration |
| `cluster_healthcheck_generate_report` | bool | `true` | Generate HTML report |
| `cluster_healthcheck_report_path` | str | `/tmp/cluster_healthcheck_report.html` | Report output path |
| `cluster_healthcheck_mtv_namespace` | str | `openshift-mtv` | MTV operator namespace |
| `cluster_healthcheck_kubevirt_namespace` | str | `openshift-cnv` | KubeVirt operator namespace |
| `cluster_healthcheck_ssh_timeout` | int | `10` | SSH check timeout in seconds |
| `cluster_healthcheck_debug` | bool | `false` | Enable verbose debug output |

### Post-Migration VM Format

```yaml
cluster_healthcheck_post_migration_vms:
  - name: my-vm
    namespace: my-namespace
    check_ssh: true  # optional, default false
```

## Health Checks

| Check | Description |
|-------|-------------|
| `ocp_node_health` | Node Ready status, resource pressure, kubevirt.io/schedulable label |
| `kubevirt_health` | HyperConverged CR, virt-* pods, CDI operator |
| `mtv_health` | ForkliftController, MTV pods, Providers, Plans |
| `storage_health` | StorageClasses, CSI drivers, PV capacity, pending PVCs |
| `network_health` | Multus, NADs, OVN/SDN health, migration network |

## Example Playbook

```yaml
- name: Run cluster healthchecks
  hosts: localhost
  connection: local
  gather_facts: false
  roles:
    - role: infra.openshift_virtualization_migration.cluster_healthcheck
      vars:
        cluster_healthcheck_post_migration_vms:
          - name: rhel9-vm
            namespace: migration-target
```

## License

GPL-3.0-only
