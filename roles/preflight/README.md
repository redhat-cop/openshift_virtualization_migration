<!-- STATIC CONTENT START -->
# preflight

Validate the migration environment before seeding AAP. Runs every check and reports a summary, then fails the play if any check failed — one run reports everything that needs attention.

Automates the manual "Validate your environment" console checks from the journey documentation:

| Check | What it verifies |
| --- | --- |
| OpenShift API auth | `SelfSubjectReview` probe with the configured token |
| OpenShift Virtualization operator | `kubevirt-hyperconverged` CSV exists and is `Succeeded` |
| MTV operator | `mtv-operator` CSV exists and is `Succeeded` |
| AAP access | `/api/v2/me/` probe with the configured account or token |
| vCenter connectivity | Datacenter listing proves connectivity and authentication (vmware sources only; other source types skip it) |
| VDDK init image | Configured, non-empty, and scheme-less (Forklift rejects scheme'd references with `VDDKInitImageUnavailable`; vmware sources only) |

If any check fails, fix it before you seed. Do not seed to paper over a missing operator.

### Example

```bash
ansible-playbook playbooks/vmf_preflight.yml \
  --inventory inventory-sample.yml
```

From an AAP job template the target credential injects `K8S_AUTH_*`, the source credential injects `VMWARE_*`, and the controller injects `CONTROLLER_HOST`/`CONTROLLER_API_TOKEN` — the same role runs unchanged.

AAP 2.5 platform deployments serve the controller API at `/api/controller/v2/` rather than `/api/v2/` — set `preflight_aap_api_path: /api/controller/v2/` for those environments (a 404 from the AAP check means the path is wrong).

With the sample inventory the connection variables resolve from the target cluster host (`openshift_host`, `openshift_api_key`), the source host (`host`, `username`, `password`, `vddk.image`), and the AAP host (`aap_hostname`, `aap_token`) — selected by `preflight_target_name`, `preflight_source_name`, and `preflight_aap_name`, which default to the `target_name`/`source_name` extra vars (injected by the seeded credentials) or the first host of each group.

All checks run on every invocation, and the summary assert requires every check green — the per-check tags (`openshift`, `cnv`, `mtv`, `aap`, `vcenter`, `vddk`) exist for isolated debugging; the summary asserts only over the checks that ran, so a tagged debug run ends green when the targeted check passed. A source whose `type` is not `vmware` (for example `ovirt`) skips the vCenter and VDDK checks.

<!-- STATIC CONTENT END -->
<!-- DOCSIBLE START -->
## preflight

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
Version - 1.25.0
Repository - https://github.com/redhat-cop/openshift_virtualization_migration
Minimum Ansible Version - 2.16
```

### Argument Specifications

#### Key: main

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| preflight_secure_logging | bool | no | true | Whether to enable secure logging for tasks that handle credentials. Set to false to debug failed probes. Prefer a one-off CLI run (`--tags <check>`) over flipping the toggle on a job template; if you must, rotate the exposed credential (token **or password**) afterwards. |
| preflight_target_name | str | no | n/a | Inventory host whose variables feed the OpenShift checks. Defaults to the target_name extra var or the first migration_clusters host. |
| preflight_source_name | str | no | n/a | Inventory host whose variables feed the vCenter and VDDK checks. Defaults to the source_name extra var or the first vm_sources host. |
| preflight_aap_name | str | no | n/a | Inventory host whose aap_* variables feed the AAP check. Defaults to the first migration_aap host. |
| preflight_openshift_host | str | no | "" | OpenShift API endpoint. Resolves from K8S_AUTH_HOST env var or the openshift_host variable on the target cluster host. Required — the preflight aborts without it. |
| preflight_openshift_api_key | str | no | "" | OpenShift API token. Resolves from K8S_AUTH_API_KEY env var or the openshift_api_key variable on the target cluster host. |
| preflight_openshift_verify_ssl | bool | no | true | Validate the OpenShift API TLS certificate. |
| preflight_vcenter_hostname | str | no | "" | vCenter endpoint for the connectivity check. Resolves from VMWARE_HOST env var or the host variable on the source host. Applies to vmware sources; other source types skip it. |
| preflight_vcenter_username | str | no | "" | vCenter username. Resolves from VMWARE_USER env var or the username variable on the source host. |
| preflight_vcenter_password | str | no | "" | vCenter password. Resolves from VMWARE_PASSWORD env var or the password variable on the source host. |
| preflight_vcenter_validate_certs | bool | no | true | Validate the vCenter TLS certificate. |
| preflight_aap_hostname | str | no | "" | AAP controller URL. Resolves from AAP_HOSTNAME env var, the controller-injected CONTROLLER_HOST, or the aap_hostname variable on the AAP host. |
| preflight_aap_api_path | str | no | /api/v2/ | API base path for the access check. AAP 2.5 platform deployments serve the controller API at /api/controller/v2/ — set that value for those environments. |
| preflight_aap_username | str | no | "" | AAP username for the access check. |
| preflight_aap_password | str | no | "" | AAP password for the access check when no token is set. |
| preflight_aap_token | str | no | "" | AAP OAuth2 token. Resolves from AAP_TOKEN env var, the controller-injected CONTROLLER_API_TOKEN, or the aap_token variable on the AAP host. Takes precedence over username/password. |
| preflight_aap_validate_certs | bool | no | true | Validate the AAP TLS certificate. |
| preflight_cnv_namespace | str | no | openshift-cnv | Namespace holding the OpenShift Virtualization operator CSV. |
| preflight_mtv_namespace | str | no | openshift-mtv | Namespace holding the MTV operator CSV. |
| preflight_vddk_image | str | no | "" | VDDK init image for direct-source migrations. Resolves from the source host's vddk.image dictionary entry or the vddk_image variable. |

### Defaults

#### File: defaults/main.yml

All options resolve from AAP-injected environment variables to inventory host variables (through preflight_target_name, preflight_source_name, and preflight_aap_name) so the role runs identically from an AAP job template and from a controller with the sample inventory. See the argument specification table above.

### Tasks

#### File: tasks/main.yml

- Include pre-validation of required connection variables (always)
- Run preflight checks (block)
  - Include OpenShift API authentication check (openshift, validate)
  - Include OpenShift Virtualization operator check (cnv, validate)
  - Include MTV operator check (mtv, validate)
  - Include AAP access check (aap, validate)
  - Include vCenter connectivity check (vcenter, validate)
  - Include VDDK init image check (vddk, validate)
- Include the preflight summary report (always)

The per-check tags select checks for isolated debugging; the summary report (always) asserts every check green on a full run.

## Author Information

Red Hat

## License

GPL-3.0-only

## Minimum Ansible Version

2.16

## Platforms

- GenericLinux
<!-- DOCSIBLE END -->
