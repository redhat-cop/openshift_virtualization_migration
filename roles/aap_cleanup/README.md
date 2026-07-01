# aap_cleanup

Remove AAP resources seeded by the `aap_seed` role. Discovers resources via the AAP controller API and removes them in reverse dependency order using `infra.aap_configuration.dispatch` (or `infra.controller_configuration.dispatch` for AAP 2.4).

## Requirements

- AAP controller API access (hostname + credentials or token)
- `infra.aap_configuration` >= 3.4.1 (AAP 2.5+) or `infra.controller_configuration` >= 3.1.2 (AAP 2.4)

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aap_cleanup_controller_hostname` | env/var lookup | AAP controller hostname |
| `aap_cleanup_controller_username` | env/var lookup | AAP controller username |
| `aap_cleanup_controller_password` | env/var lookup | AAP controller password |
| `aap_cleanup_controller_token` | env/var lookup | AAP OAuth token (preferred over user/pass) |
| `aap_cleanup_controller_validate_certs` | env/var lookup | Validate TLS certificates |
| `aap_cleanup_aap_org_name` | `aap_org_name` | Organization to clean |
| `aap_cleanup_dry_run` | `false` | Query and report only, no deletions |
| `aap_cleanup_workflows_remove` | `true` | Remove workflow job templates |
| `aap_cleanup_job_templates_remove` | `true` | Remove job templates |
| `aap_cleanup_hosts_remove` | `true` | Remove hosts |
| `aap_cleanup_inventories_remove` | `true` | Remove inventories |
| `aap_cleanup_projects_remove` | `true` | Remove projects |
| `aap_cleanup_execution_environments_remove` | `true` | Remove execution environments |
| `aap_cleanup_credentials_remove` | `true` | Remove credentials |
| `aap_cleanup_credential_types_remove` | `true` | Remove custom credential types |
| `aap_cleanup_organization_remove` | `false` | Remove organization (destructive) |
| `aap_cleanup_job_history_purge` | `false` | Purge completed job history |
| `aap_cleanup_providers` | `[vmware, ovirt]` | Provider-specific resources to target |

## Deletion Order

Resources are removed in reverse creation order to respect dependencies:

1. Workflow Job Templates
2. Job Templates
3. Hosts
4. Inventories
5. Projects
6. Execution Environments
7. Credentials
8. Credential Types
9. Organizations (optional)
10. Job History (optional)

## Example Playbook

```yaml
- hosts: localhost
  roles:
    - role: infra.openshift_virtualization_migration.aap_cleanup
      vars:
        aap_cleanup_dry_run: true  # preview first
```

## License

GPL-3.0-or-later
