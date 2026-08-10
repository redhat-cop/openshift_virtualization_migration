# aap_seed

Seeds Ansible Automation Platform with Migration Factory Configuration as Code content.

The role dynamically builds AAP objects from the Ansible inventory at runtime:

- **Credential types** — custom type for source hypervisor environments (with insecure TLS option)
- **Credentials** — one per source (vSphere/RHV) and one per target (OpenShift bearer token)
- **Inventory hosts** — source and target hosts with non-sensitive metadata
- **Inventory groups** — `vm_sources` and `migration_clusters`
- **Project** — SCM-backed project synced from Git
- **Job templates, inventories** — from static CaC definitions in `group_vars/migration_aap/`

Target cluster credentials use the built-in AAP credential type
"OpenShift or Kubernetes API Bearer Token".

## Requirements

- `infra.aap_configuration` collection (>= 4.x)
- `ansible.controller` collection

## Role Variables

### AAP Connection (required)

| Variable | Type | Description |
|----------|------|-------------|
| `aap_seed_hostname` | str | FQDN or URL of the AAP controller API endpoint |
| `aap_seed_username` | str | Username for AAP authentication (mutually exclusive with `aap_seed_token`) |
| `aap_seed_password` | str | Password for AAP authentication (mutually exclusive with `aap_seed_token`) |
| `aap_seed_token` | str | OAuth token for AAP authentication |
| `aap_seed_validate_certs` | bool | Validate TLS certificates (default: `true`) |
| `aap_seed_secure_logging` | bool | Suppress credential loop output (default: `true`; set to `false` for debugging) |

### AAP Content Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `aap_seed_org_name` | `Default` | AAP organization for all objects |
| `aap_seed_project_name` | `OpenShift Virtualization Migration` | SCM project name |
| `aap_seed_project_scm_url` | `https://github.com/redhat-cop/openshift_virtualization_migration.git` | Git URL |
| `aap_seed_project_scm_branch` | `v2` | Git branch or tag |
| `aap_seed_project_sync_timeout` | `120` | SCM sync timeout in seconds |
| `aap_seed_inventory_name` | `OpenShift Virtualization Migration` | AAP inventory name |
| `aap_seed_execution_environment` | `Default execution environment` | Execution environment for job templates |

### Credential and Inventory Group Names

| Variable | Default | Description |
|----------|---------|-------------|
| `aap_seed_source_credential_type` | `Migration Factory - Source Environment` | Custom credential type for sources |
| `aap_seed_target_credential_type` | `OpenShift or Kubernetes API Bearer Token` | Credential type for targets (built-in) |
| `aap_seed_source_inventory_group` | `vm_sources` | Inventory group containing source hosts |
| `aap_seed_target_inventory_group` | `migration_clusters` | Inventory group containing target hosts |

## Inventory Host Variables

### Source hosts (`vm_sources` group)

```yaml
vcenter-prod:
  type: vmware               # vmware or ovirt
  host: vcenter.example.com
  sdk_endpoint: /sdk
  username: administrator@vsphere.local
  password: changeme          # use ansible-vault
  # insecure_skip_tls_verify: true   # default: false
```

### Target hosts (`migration_clusters` group)

Provide one of `openshift_api_key` (permanent) or `openshift_temporary_api_key` (short-lived):

```yaml
ocp-prod:
  openshift_host: https://api.ocp-prod.example.com:6443
  openshift_api_key: sha256~XXXXXXXXXXX
  # openshift_verify_ssl: false      # default: true
  vm_sources:
    - vcenter-prod
  aap_hosts:
    - aap-instance
  mtv_namespace: openshift-mtv
  default_target_namespace: vm-workloads
  configure_mtv: true
```

## Example Playbook

```yaml
---
- name: Seed AAP with Migration Factory content
  hosts: migration_aap
  connection: local
  gather_facts: false

  tasks:
    - name: Sync project and push CaC objects to AAP
      ansible.builtin.import_role:
        name: aap_seed
```

## License

Apache-2.0
