# Secure Credential Practices for Developers

This guide defines the secure credential management practices that all
contributors to the Ansible for OpenShift Virtualization Migration project must
follow. It covers the rules for handling secrets in code, the tools
enforcing those rules, and the onboarding process for new team members.

This guide aligns with the Red Hat IT Information Security policy on
secret management. Refer to the authoritative source for organization-
wide requirements:

> See the [Ansible Vault documentation](https://docs.ansible.com/ansible/latest/vault_guide/index.html)
> and [AAP credential management](https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html/automation_controller_user_guide/controller-credentials)
> for industry-standard secret management practices.

## Golden Rules

1. **Never commit real credentials to Git.** No passwords, tokens, API
   keys, certificates, or private keys in any file that is tracked by
   version control — not even temporarily.
2. **Use placeholders in committed files.** Inventory and defaults files
   must use `changeme`, Jinja2 variable references (`{{ variable }}`),
   or empty strings as values for any credential field.
3. **Encrypt sensitive variable files with Ansible Vault.** Any file
   containing real credential values must be encrypted before it
   touches disk. See the `inventory.vault.yml.example` template in the repository root.
4. **Let AAP manage runtime secrets.** Credential values used during
   playbook execution should be stored in AAP credential types, not
   in variable files on the filesystem.
5. **Mark sensitive tasks with `no_log`.** Any task that handles
   credential values must include `no_log: "{{ secure_logging |
   default(true) }}"` to prevent secrets from appearing in logs.

## What Counts as a Secret

| Category | Examples |
|---|---|
| Passwords | `rh_password`, `openshift_password`, `container_password` |
| API tokens | `openshift_api_key`, `automation_hub_certified_token` |
| SSH private keys | `git_ssh_private_key`, machine credential keys |
| Certificates | vCenter CA certificates, TLS private keys |
| Registry credentials | `container_username`/`container_password`, VDDK registry |
| Connection strings | Database URIs with embedded credentials |

If you are unsure whether a value is sensitive, treat it as a secret.

## Tooling Enforcement

### Pre-commit Hook (Gitleaks)

The repository includes a Gitleaks pre-commit hook in
`.pre-commit-config.yaml`. It runs automatically on every commit to
detect secrets before they enter Git history.

**Setup (one-time):**

```bash
pip install pre-commit
pre-commit install
```

**What happens on commit:**

- Gitleaks scans staged changes against the rules in `.gitleaks.toml`.
- If a potential secret is found, the commit is blocked with details
  about the finding.
- Fix the issue (remove or encrypt the secret) and commit again.

**Bypass (emergency only):**

```bash
git commit --no-verify -m "message"
```

Use `--no-verify` only when you have confirmed the finding is a false
positive. Document false positive patterns in `.gitleaks.toml` so they
do not recur.

### CI Workflow (GitHub Actions)

The `.github/workflows/gitleaks.yml` workflow runs Gitleaks on every
push to `main` and on all pull requests. PRs with detected secrets will
fail the check and cannot be merged.

### .gitignore Protections

The following patterns are excluded from version control:

- `secrets.yml` — common name for unencrypted secret files
- `*.vault.yml` — Ansible Vault encrypted files
- `vault-password*`, `.vault-password*` — vault password files
- `.env` — environment variable files

## How to Handle Credentials

### Adding a New Secret to the Project

1. Add the variable name to the appropriate `defaults/main.yml` with a
   `changeme` placeholder or an empty string.
2. Add the variable to `inventory.vault.yml.example` with an empty
   value and a descriptive comment.
3. If the secret is used at runtime by AAP, define it in the
   appropriate AAP custom credential type (see
   `docs/secure_credential_management.md`).
4. In the task that uses the secret, add `no_log: "{{ secure_logging |
   default(true) }}"`.
5. Run `gitleaks detect --config .gitleaks.toml --no-git` to verify
   no real values are present.

### Using Ansible Vault Locally

```bash
# Create and encrypt a vault file from the example
cp inventory.vault.yml.example inventory.vault.yml
# Edit with real values, then encrypt
ansible-vault encrypt inventory.vault.yml

# Run a playbook with the vault file
ansible-playbook -e @inventory.vault.yml playbooks/bootstrap.yml \
  --ask-vault-pass

# Edit an encrypted file
ansible-vault edit inventory.vault.yml

# Rotate the vault password
ansible-vault rekey inventory.vault.yml
```

### Referencing Secrets in Playbooks

Prefer environment variable lookups for credentials that AAP injects:

```yaml
my_api_key: >-
  {{ my_api_key
     | default(lookup('ansible.builtin.env', 'MY_API_KEY')) }}
```

This pattern allows the variable to be set via AAP credential injection
(environment variable) or passed directly as an extra var.

## Code Review Checklist

When reviewing pull requests, verify the following:

- [ ] No real credential values in any committed file.
- [ ] New credential variables use `changeme` or `{{ }}` placeholders.
- [ ] Tasks handling secrets include `no_log`.
- [ ] New secrets are documented in `inventory.vault.yml.example`.
- [ ] Gitleaks CI check passes.
- [ ] Any new `.gitleaks.toml` allowlist entries are justified.

## Onboarding New Team Members

### Day 1 Setup

1. **Install pre-commit hooks:**

   ```bash
   pip install pre-commit
   pre-commit install
   ```

2. **Read this guide** and `docs/secure_credential_management.md`.

3. **Review the credential management documentation:**
   See `docs/secure_credential_management.md` for the project's
   credential architecture and AAP integration details.

4. **Set up local vault file** (if running playbooks locally):

   ```bash
   cp inventory.vault.yml.example inventory.vault.yml
   # Obtain credential values from your team lead or password manager
   ansible-vault encrypt inventory.vault.yml
   ```

5. **Verify Gitleaks works:**

   ```bash
   gitleaks detect --config .gitleaks.toml --no-git
   ```

### Key Concepts to Understand

- How AAP credential types inject secrets into job templates (extra
  vars and environment variables).
- The difference between `defaults/main.yml` (placeholder values,
  committed) and `inventory.vault.yml` (real values, encrypted, never
  committed).
- Why `no_log` is required on tasks that handle secrets.
- How to add a false positive allowlist entry to `.gitleaks.toml` if
  needed.

## Incident Response

If a real credential is accidentally committed to Git:

1. **Rotate the credential immediately.** Assume it has been
   compromised.
2. **Remove the commit** from history using `git filter-repo` or
   `BFG Repo-Cleaner`. A simple revert does not remove the secret
   from Git history.
3. **Force-push** the cleaned history (coordinate with the team).
4. **Add a Gitleaks rule** to `.gitleaks.toml` if the pattern was not
   already covered.
5. **Report the incident** per the Red Hat secret management policy.

### Public Repository Considerations

Since this is a public repository, credential exposure requires
additional community communication:

1. **Post a GitHub Security Advisory** using the repository's Security
   tab to notify watchers of the exposure and any required actions.
2. **Open an issue** (without including the secret) describing what
   was exposed, the timeframe, and what users should do (e.g., rotate
   credentials, update configurations).
3. **Notify downstream users** via any established communication
   channels (mailing lists, Slack, etc.) with clear remediation steps.
4. **Document the incident** in a post-mortem to prevent recurrence
   and update this guide if new patterns need to be covered.
