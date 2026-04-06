# Secure Credential Management

This document describes how the OpenShift Virtualization Migration
Factory manages sensitive credentials and the recommended practices for
keeping them secure.

## Architecture Overview

The Migration Factory uses a layered approach to credential management:

1. **Ansible Vault** — Encrypts sensitive variable files at rest so
   credentials are never stored in plaintext in Git.
2. **AAP Credential Types** — Stores and injects credentials at runtime
   via Ansible Automation Platform's built-in credential management.
3. **Kubernetes Secrets** — Stores cluster-scoped credentials (API
   tokens, service account keys) in OpenShift.
4. **Environment Variable Injection** — AAP custom credential types
   inject secrets as environment variables or extra vars into job
   template execution.

```
┌──────────────────────────────────────────────────┐
│              Ansible Automation Platform          │
│                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │  Machine   │  │  Source     │  │  Custom    │ │
│  │  Creds     │  │  Control   │  │  Cred      │ │
│  │ (SSH keys) │  │  (Git)     │  │  Types     │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘ │
│        │               │               │        │
│        └───────────┬────┘───────────────┘        │
│                    │                             │
│              Injected at runtime                 │
│                    │                             │
│              ┌─────▼──────┐                      │
│              │ Job        │                      │
│              │ Template   │                      │
│              │ Execution  │                      │
│              └────────────┘                      │
└──────────────────────────────────────────────────┘
```

## Credential Inventory

The following credentials are managed by the Migration Factory:

| Credential | Storage Method | Used By |
|---|---|---|
| Red Hat account (username/password) | AAP Credential / Vault | `bootstrap` role |
| OpenShift API token | Kubernetes Secret / AAP | `create_mf_aap_token`, all k8s tasks |
| Git repository (username/password or SSH key) | AAP Source Control Credential | `aap_seed` role, project sync |
| Container registry (host/username/password) | AAP Container Registry Credential | EE image pulls |
| Automation Hub tokens (certified + validated) | AAP Galaxy Credential | Collection sync |
| VMware vCenter (host/username/password) | AAP Custom Credential | `mtv_management` provider tasks |
| oVirt/RHV (host/username/password) | AAP Custom Credential | `mtv_management` provider tasks |
| VDDK registry (username/password) | AAP Custom Credential | `mtv_management` VDDK tasks |
| AAP admin (hostname/username/password/token) | AAP Credential | `aap_seed`, `bootstrap` |
| Machine SSH keys | AAP Machine Credential | `aap_machine_credentials` role |
| iDRAC (username/password) | AAP Custom Credential | Bootstrap bare-metal tasks |

## Using Ansible Vault

Ansible Vault encrypts variable files so that sensitive values are never
stored in plaintext.

### Initial Setup

1. Copy the example vault file and populate it with real values:

   ```bash
   cp inventory.vault.yml.example inventory.vault.yml
   ```

2. Edit `inventory.vault.yml` and replace placeholder values with
   actual credentials.

3. Encrypt the file:

   ```bash
   ansible-vault encrypt inventory.vault.yml
   ```

4. Optionally, create a vault password file (excluded from Git by
   `.gitignore`):

   ```bash
   echo 'your-vault-password' > .vault-password
   chmod 600 .vault-password
   ```

### Running Playbooks with Vault

With a password prompt:

```bash
ansible-playbook -e @inventory.vault.yml \
  playbooks/bootstrap.yml --ask-vault-pass
```

With a password file:

```bash
ansible-playbook -e @inventory.vault.yml \
  playbooks/bootstrap.yml --vault-password-file .vault-password
```

### Editing Encrypted Files

```bash
ansible-vault edit inventory.vault.yml
```

### Re-keying (Rotating the Vault Password)

```bash
ansible-vault rekey inventory.vault.yml
```

## AAP Custom Credential Types

The `aap_seed` role creates the following custom credential types in
AAP. These store secrets in AAP's encrypted database and inject them
into job template runs.

### openshift_virtualization_migration_cac

Config-as-Code credential that stores Migration Factory configuration
including AAP settings, organization, and project details.

**Injected as extra vars:**

- `aap_version`, `aap_instance_name`, `aap_execution_environment`
- `aap_org_name`, `aap_namespace`, `aap_project`, `aap_inventory`
- `aap_job_template_extra_vars`, `migration_targets`

### VMware Migration Target

Per-target VMware credentials for MTV provider configuration.

**Injected as extra vars and environment variables:**

- `VMWARE_HOST`, `VMWARE_USER`, `VMWARE_PASSWORD` (env)
- Target name, host, insecure SSL flag, VDDK image details (extra vars)

### Ovirt Migration Target

Per-target oVirt/RHV credentials for MTV provider configuration.

**Injected as extra vars and environment variables:**

- `OVIRT_HOSTNAME`, `OVIRT_USERNAME`, `OVIRT_PASSWORD` (env)
- Target name, host, insecure SSL flag (extra vars)

## Secure Logging

All tasks that handle sensitive data use the `no_log` directive to
prevent credentials from appearing in Ansible output:

```yaml
- name: Task with sensitive data
  some_module:
    password: "{{ secret_value }}"
  no_log: "{{ secure_logging | default(true) }}"
```

The `secure_logging` variable defaults to `true`. Set it to `false`
only in development environments when debugging credential issues.

## Access Control Recommendations

### AAP Credentials

- Use AAP's role-based access control (RBAC) to restrict credential
  access to specific teams and users.
- Grant the minimum permission level required: **Use** for job template
  execution, **Admin** only for credential managers.
- Audit credential access regularly via AAP's activity stream.

### Ansible Vault

- Use a unique vault password per environment (dev, staging, production).
- Store vault passwords in a secure location (e.g., a password manager
  or secrets management service).
- Never commit vault password files to Git — they are excluded by
  `.gitignore`.
- Rotate vault passwords periodically using `ansible-vault rekey`.

### Kubernetes Secrets

- The `create_mf_aap_token` role creates a ServiceAccount with
  `cluster-admin` privileges. Limit the scope if your environment
  permits.
- Use OpenShift's RBAC to restrict access to the
  `migration-factory-aap-sa-token` secret.
- Rotate service account tokens periodically.

### Git Repositories

- Prefer SSH key authentication over username/password for Git
  operations.
- Use deploy keys with read-only access where possible.
- The `.gitignore` excludes common secret file patterns (`secrets.yml`,
  `*.vault.yml`, `vault-password*`, `.vault-password*`).
- Gitleaks is configured (`.gitleaks.toml`) and integrated into
  pre-commit hooks and CI to detect accidental secret commits.

## Migrating from Plaintext to Vault

If you have an existing `inventory.yml` with real credential values:

1. Extract all sensitive values into `inventory.vault.yml`.
2. Replace the values in `inventory.yml` with variable references:

   ```yaml
   # inventory.yml (safe to commit)
   rh_username: "{{ vault_rh_username }}"
   rh_password: "{{ vault_rh_password }}"
   ```

   ```yaml
   # inventory.vault.yml (encrypted)
   vault_rh_username: "actual-username"
   vault_rh_password: "actual-password"
   ```

3. Encrypt the vault file:

   ```bash
   ansible-vault encrypt inventory.vault.yml
   ```

4. Verify no secrets remain in plaintext:

   ```bash
   gitleaks detect --config .gitleaks.toml --no-git
   ```
