# aap_seed

Seeds Ansible Automation Platform with Migration Factory Configuration as Code content.

The role dynamically builds all AAP objects from the Ansible inventory and role defaults at runtime:

- **Credential types** -- custom type for source hypervisor environments
- **Credentials** -- one per source (vSphere/RHV), one per target (OpenShift bearer token), and optionally a Git credential for private repos
- **Inventory, hosts, groups** -- source and target hosts with non-sensitive metadata
- **Execution environments** -- optional custom EE definitions
- **Project** -- SCM-backed project synced from Git
- **Job templates** -- default migrate template

Target cluster credentials use the built-in AAP credential type
"OpenShift or Kubernetes API Bearer Token".

## Architecture

All object shapes are defined in `defaults/main.yml` as `aap_seed_controller_*`
lists. During execution the role:

1. Applies `_create` toggles to skip disabled categories
2. Validates inventory host variables
3. Renders credentials from Jinja2 templates in `templates/`
4. Builds hosts and groups by looping over inventory groups
5. Syncs the SCM project
6. Copies `aap_seed_controller_*` to `controller_*` (handoff)
7. Calls `infra.aap_configuration.dispatch`

Users can override any object list by redefining the corresponding
`aap_seed_controller_*` variable, or disable an entire category with its
`_create` toggle.

## Requirements

- `infra.aap_configuration` collection (>= 4.x)
- `ansible.controller` collection

## Role Variables

### AAP Connection

Set these in your inventory under the `migration_aap` host. The role cascades
from generic `aap_*` variables so they can be shared with other roles.

| Inventory Variable | Role Variable | Type | Description |
|--------------------|---------------|------|-------------|
| `aap_hostname` | `aap_seed_hostname` | str | FQDN or URL of the AAP controller API endpoint |
| `aap_username` | `aap_seed_username` | str | Username for AAP authentication (mutually exclusive with token) |
| `aap_password` | `aap_seed_password` | str | Password for AAP authentication (mutually exclusive with token) |
| `aap_token` | `aap_seed_token` | str | OAuth token for AAP authentication |
| `aap_validate_certs` | `aap_seed_validate_certs` | bool | Validate TLS certificates (default: `true`) |
| — | `aap_seed_secure_logging` | bool | Suppress credential loop output (default: `true`; set to `false` for debugging) |

### AAP Content Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `aap_seed_org_name` | `Default` | AAP organization for all objects |
| `aap_seed_project_name` | `OpenShift Virtualization Migration` | SCM project name |
| `aap_seed_project_scm_url` | cascades from `aap_project_scm_url` | Git URL |
| `aap_seed_project_scm_branch` | cascades from `aap_project_scm_branch` | Git branch or tag |
| `aap_seed_project_sync_timeout` | `120` | SCM sync timeout in seconds |
| `aap_seed_project_credential` | cascades from `aap_project_credential` | Name of the Git credential to create and attach to the project (leave empty to skip) |
| `aap_seed_inventory_name` | `OpenShift Virtualization Migration` | AAP inventory name |
| `aap_seed_execution_environment` | `Default execution environment` | Execution environment for job templates |
| `aap_seed_migrate_template_name` | `OpenShift Virtualization Migration - Migrate` | Name of the default job template |
| `aap_seed_migrate_playbook` | `playbooks/vmf_migrate.yml` | Playbook path for the default job template |

### Git Credential (optional)

When `aap_project_credential` (or `aap_seed_project_credential`) is set, the
role creates a Source Control credential in AAP. Provide either
username/password or an SSH key in the inventory.

| Inventory Variable | Role Variable | Default | Description |
|--------------------|---------------|---------|-------------|
| `aap_git_username` | `aap_seed_git_username` | `""` | Git username for HTTPS authentication |
| `aap_git_password` | `aap_seed_git_password` | `""` | Git password or personal access token |
| `aap_git_ssh_key` | `aap_seed_git_ssh_key` | `""` | SSH private key for Git authentication |
| `aap_git_ssh_key_unlock` | `aap_seed_git_ssh_key_unlock` | `""` | Passphrase to unlock the SSH key |

### Credential and Inventory Group Names

| Variable | Default | Description |
|----------|---------|-------------|
| `aap_seed_source_credential_type` | `Migration Factory - Source Environment` | Custom credential type for sources |
| `aap_seed_target_credential_type` | `OpenShift or Kubernetes API Bearer Token` | Credential type for targets (built-in) |
| `aap_seed_source_inventory_group` | `vm_sources` | Inventory group containing source hosts |
| `aap_seed_target_inventory_group` | `migration_clusters` | Inventory group containing target hosts |

### Create Toggles

Set any toggle to `false` to skip that object category entirely.

| Variable | Default | Description |
|----------|---------|-------------|
| `aap_seed_organizations_create` | `true` | Create organizations (only when list is non-empty) |
| `aap_seed_credential_types_create` | `true` | Create custom source credential type |
| `aap_seed_credentials_create` | `true` | Build and push all credentials |
| `aap_seed_inventories_create` | `true` | Create the AAP inventory |
| `aap_seed_hosts_create` | `true` | Build and push inventory hosts and groups |
| `aap_seed_execution_environments_create` | `true` | Create execution environments (only when list is non-empty) |
| `aap_seed_projects_create` | `true` | Create and sync the SCM project |
| `aap_seed_templates_create` | `true` | Create job templates |

### Overridable Object Lists

Override these to completely replace the role's default object definitions.

| Variable | Description |
|----------|-------------|
| `aap_seed_controller_organizations` | Organization definitions (default: `[]`) |
| `aap_seed_controller_credential_types` | Custom credential type definitions |
| `aap_seed_controller_execution_environments` | Execution environment definitions (default: `[]`) |
| `aap_seed_controller_inventories` | AAP inventory definitions |
| `aap_seed_controller_projects` | AAP project definitions |
| `aap_seed_controller_templates` | AAP job template definitions |

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

### Add a custom execution environment

```yaml
aap_seed_controller_execution_environments:
  - name: Migration Factory EE
    image: quay.io/org/migration-factory-ee:latest
```

### Skip specific object types

```yaml
- name: Only push credentials (no project, templates, or inventory)
  hosts: migration_aap
  connection: local
  gather_facts: false

  tasks:
    - name: Push credentials only
      ansible.builtin.import_role:
        name: aap_seed
      vars:
        aap_seed_projects_create: false
        aap_seed_templates_create: false
        aap_seed_inventories_create: false
        aap_seed_hosts_create: false
```

## License

GPL-3.0-or-later
