# configure_providers

Create MTV/Forklift source provider custom resources on OpenShift target
clusters. Designed to run from AAP with credential injection.

## Overview

This role creates a Forklift `Provider` CR and its backing `Secret` on a
target OpenShift cluster for a given source environment (vSphere or oVirt).
It is intended to be launched as an AAP job template with `source_name` and
`target_name` survey variables.

For targets with multiple sources (`vm_sources: [vcenter-prod, vcenter-lab]`),
launch the job template once per source-target pair. Each run creates one
provider. The role is idempotent — re-running for the same pair updates in
place.

## Requirements

- MTV (Forklift) operator must be installed on the target OpenShift cluster
- `kubernetes.core` Ansible collection
- AAP credential types:
  - **Migration Factory - Source Environment** (custom) — injects
    `mf_source_username`, `mf_source_password`, `mf_source_certificate`,
    `mf_source_host`, `mf_insecure_skip_tls_verify`
  - **OpenShift or Kubernetes API Bearer Token** (built-in) — injects
    `K8S_AUTH_HOST`, `K8S_AUTH_API_KEY`, `K8S_AUTH_VERIFY_SSL` as env vars

## Role Variables

### Required (survey variables)

| Variable | Description |
|----------|-------------|
| `source_name` | Name of the source environment (must match an AAP inventory host in `vm_sources`) |
| `target_name` | Name of the target OpenShift cluster (must match an AAP inventory host in `migration_clusters`) |

### Optional (role defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `configure_providers_mtv_namespace` | From `hostvars[target_name].mtv_namespace` or `openshift-mtv` | Namespace where MTV is installed |
| `configure_providers_provider_wait` | `true` | Wait for Provider to reach Ready status |
| `configure_providers_provider_wait_timeout` | `120` | Seconds to wait for Ready |
| `configure_providers_provider_wait_poll` | `10` | Seconds between status polls |
| `configure_providers_provider_state` | `present` | Set to `absent` to remove a provider |
| `configure_providers_api_version` | `forklift.konveyor.io/v1beta1` | Forklift API version |

### Source host vars (from AAP inventory)

These are resolved from `hostvars[source_name]` at runtime:

| Variable | Required | Description |
|----------|----------|-------------|
| `type` | Yes | Source type: `vmware` or `ovirt` |
| `host` | Yes | Source hostname or IP |
| `sdk_endpoint` | No (default: `/sdk`) | SDK endpoint path |
| `vddk.image` | No | VDDK init image URL (VMware only) |

### Target host vars (from AAP inventory)

| Variable | Required | Description |
|----------|----------|-------------|
| `mtv_namespace` | No (default: `openshift-mtv`) | Namespace where MTV is installed |
| `vm_sources` | Yes | List of source names mapped to this target |

## Resources Created

For each source-target pair, the role creates:

1. **Secret** (`<source_name>-provider-secret`) — contains source
   credentials (user, password, and optionally cacert or insecureSkipVerify)
2. **Provider** (`<source_name>`) — Forklift Provider CR pointing to the
   source with the secret reference

### VMware Provider Example

```yaml
apiVersion: forklift.konveyor.io/v1beta1
kind: Provider
metadata:
  name: vcenter-prod
  namespace: openshift-mtv
spec:
  type: vsphere
  url: https://vcenter.prod.example.com/sdk
  secret:
    name: vcenter-prod-provider-secret
    namespace: openshift-mtv
  settings:
    vddkInitImage: registry.example.com/vddk:8.0
```

### oVirt Provider Example

```yaml
apiVersion: forklift.konveyor.io/v1beta1
kind: Provider
metadata:
  name: rhv-legacy
  namespace: openshift-mtv
spec:
  type: ovirt
  url: https://rhvm.example.com/ovirt-engine/api
  secret:
    name: rhv-legacy-provider-secret
    namespace: openshift-mtv
```

## Error Handling

If the Provider fails to reach `Ready` status within the timeout, the role:

1. Fetches the Provider CR's current status conditions
2. Displays a structured error with the provider name, type, URL, phase,
   and MTV's reported failure reason
3. Provides troubleshooting guidance (check credentials, verify source
   reachability, TLS settings, MTV operator status)

## AAP Job Template

The `aap_seed` role creates a job template named
**OpenShift Virtualization Migration - Configure MTV** that runs
`playbooks/vmf_configure_providers.yml`. Attach both source and target
credentials when launching.

## License

GPL-3.0-or-later
