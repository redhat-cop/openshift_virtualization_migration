# Disconnected Environment Guide

This guide describes the steps and processes required to leverage the
Ansible for OpenShift Virtualization Migration within a disconnected or
restricted environment from a networking and content management
perspective.

A disconnected (air-gapped) environment has no direct access to the
internet. All software artifacts — container images, Operator catalogs,
Ansible collections, Python packages, and VMware utilities — must be
mirrored to internal registries and repositories before they can be
consumed.

## Prerequisites

- An internal container registry (e.g., a self-hosted Quay, Artifactory,
  or Nexus instance) accessible from all OpenShift clusters.
- An internal HTTP/HTTPS server or Automation Hub instance for hosting
  Ansible collections and Python packages.
- `oc-mirror` CLI plugin installed on a bastion host that has internet
  access (or a sneaker-net transfer mechanism).
- `oc` CLI with cluster-admin access to the target OpenShift clusters.
- A Red Hat account with entitlements for downloading Operator catalog
  indexes and container images.

> **Note:** This guide assumes that an Execution Environment (EE) is used for playbook execution, which satisfies Python package and Ansible collection dependencies at runtime. The mirroring steps below are provided for environments that build custom EEs or run playbooks outside of an EE.

## 1. Operator Lifecycle Manager (OLM) Catalog Mirroring

The Ansible for OpenShift Virtualization Migration depends on the following OLM-managed Operators.
Each must be available in a mirrored CatalogSource on every target
cluster.

| Operator | Package Name | Default Namespace (for reference) |
|---|---|---|
| Migration Toolkit for Virtualization (MTV) | `mtv-operator` | `openshift-mtv` |
| OpenShift Virtualization (CNV) | `kubevirt-hyperconverged` | `openshift-cnv` |
| Advanced Cluster Management (ACM) | `advanced-cluster-management` | `open-cluster-management` |
| OpenShift API for Data Protection (OADP) | `redhat-oadp-operator` | `openshift-adp` |
| Fence Agents Remediation (FAR) | `fence-agents-remediation` | `openshift-workload-availability` |
| NMState | `kubernetes-nmstate-operator` | `openshift-nmstate` |
| Node Healthcheck (NHO) | `node-healthcheck-operator` | `openshift-workload-availability` |
| OpenShift GitOps | `openshift-gitops-operator` | `openshift-gitops` |

### Mirroring with oc-mirror

Create an `ImageSetConfiguration` that includes the required Operator
packages from the `redhat-operators` catalog:

```yaml
apiVersion: mirror.openshift.io/v1alpha2
kind: ImageSetConfiguration
mirror:
  operators:
    - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.x
      packages:
        - name: mtv-operator
        - name: kubevirt-hyperconverged
        - name: advanced-cluster-management
        - name: redhat-oadp-operator
        - name: fence-agents-remediation
        - name: kubernetes-nmstate-operator
        - name: node-healthcheck-operator
        - name: openshift-gitops-operator
```

Replace `v4.x` with the OpenShift version running on your clusters.

Run the mirror:

```bash
oc-mirror --config imageset-config.yaml \
  docker://<internal-registry>/<namespace>
```

After mirroring, `oc-mirror` generates `ImageContentSourcePolicy` (or
`ImageDigestMirrorSet`) and `CatalogSource` resources. Apply them to
each cluster:

```bash
oc apply -f oc-mirror-workspace/results-*/
```

### Configuring the Collection to Use Mirrored CatalogSources

The `operator_management` role supports custom CatalogSources via the
`operator_management_catalogsources` variable. Configure it to point to
the mirrored catalog:

```yaml
operator_management_catalogsources:
  mirrored_redhat_operators:
    metadata:
      name: mirrored-redhat-operators
      namespace: openshift-marketplace
    spec:
      displayName: Mirrored Red Hat Operators
      publisher: Internal
      image: <internal-registry>/<namespace>/redhat-operator-index:v4.x
```

To prevent Operator installations from utilizing the default catalog which are externally hosted, disable the default OperatorHub sources:

```bash
oc patch operatorhub cluster --type merge \
  -p '{"spec":{"disableAllDefaultSources": true}}'
```

## 2. Container Image Mirroring

Beyond the Operator images (handled by `oc-mirror`), the following
workload images must be mirrored to the internal registry.

### Execution Environment Image

The Ansible Automation Platform Execution Environment (EE) used by the
Migration Factory must be available internally. The inventory references
this image via:

```yaml
aap_execution_environment_image: registry.example.com/openshift-virtualization-migration-ee:latest
```

Mirror the EE image from its source to the internal registry:

```bash
skopeo copy \
  docker://source-registry/openshift-virtualization-migration-ee:latest \
  docker://<internal-registry>/openshift-virtualization-migration-ee:latest
```

Update `aap_execution_environment_image` in the inventory to reference
the internal registry path.

> **Tip:** `oc-mirror` can also mirror container images using the `additionalImages` property in the `ImageSetConfiguration`. See the [oc-mirror v2 documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.21/html-single/disconnected_environments/index#about-installing-oc-mirror-v2) for details.

### VDDK Image

VMware migrations require the Virtual Disk Development Kit (VDDK) image.
This image is typically built by the user from the VMware VDDK SDK and
pushed to a container registry. In disconnected environments, ensure the
VDDK image is available in the internal registry:

```yaml
# In migration target configuration
vddk:
  image: <internal-registry>/openshift-virtualization-migration-vddk:latest
  username: "{{ container_username }}"
  password: "{{ container_password }}"
```

### Red Hat Dev Spaces (Optional)

If using Red Hat Dev Spaces for development workflows, mirror the Dev
Spaces Operator images along with the other Operators in the
`ImageSetConfiguration`.

## 3. Ansible Collection Mirroring

The Migration Factory depends on the following Ansible collections.
These must be available from an internal Automation Hub or a local
filesystem path.

### Required Collections

**From Red Hat Certified Content (Automation Hub — Published):**

| Collection | Minimum Version |
|---|---|
| `redhat.openshift_virtualization` | `>=2.1.0` |
| `redhat.openshift` | `>=4.0.0` |
| `vmware.vmware_rest` | `>=4.6.0` |
| `ansible.controller` | `>=4.5.12` |
| `ansible.posix` | `>=1.6.2` |
| `kubernetes.core` | `>=5.2.0` |
| `community.crypto` | `>=2.26.0` |
| `community.general` | `>=10.5.0` |
| `community.vmware` | `>=5.5.0` |
| `ansible.utils` | `>=6.0.0` |

**From Red Hat Validated Content (Automation Hub — Validated):**

| Collection | Minimum Version |
|---|---|
| `infra.aap_utilities` | `>=2.6.0` |
| `infra.aap_configuration` | `>=3.3.0` |
| `infra.controller_configuration` | `>=3.0.2` |

### Syncing Collections to Private Automation Hub

If you are running a Private Automation Hub, configure it to sync
content from the Red Hat Certified and Validated repositories. On a
connected bastion host, download the collection tarballs:

```bash
ansible-galaxy collection download <collection_name> \
  -p /path/to/download/directory
```

Then publish them to the Private Automation Hub:

```bash
ansible-galaxy collection publish \
  /path/to/download/directory/<collection_tarball>.tar.gz \
  --server https://<private-hub>/api/galaxy/content/published/ \
  --token <hub-token>
```

### Configuring AAP to Use Private Automation Hub

Update the Automation Hub credential URLs in the inventory to point to
the internal Private Automation Hub:

```yaml
automation_hub_certified_url: https://<private-hub>/api/galaxy/content/published/
automation_hub_certified_auth_url: https://<private-hub>/auth/token/
automation_hub_certified_token: <hub-token>

automation_hub_validated_url: https://<private-hub>/api/galaxy/content/validated/
automation_hub_validated_auth_url: https://<private-hub>/auth/token/
automation_hub_validated_token: <hub-token>
```

## 4. Python Package Mirroring

The Execution Environment requires the following Python packages at
build time or runtime. These must be available from an internal PyPI
mirror (e.g., Nexus, Artifactory, or devpi).

| Package | Version Constraint |
|---|---|
| `ansible-core` | `>=2.20` |
| `kubernetes` | `>=12.0.0` |
| `PyYAML` | `>=3.11` |
| `omsdk` | `>=1.2.490` |
| `aiohttp` | latest |
| `pyVim` | latest |
| `PyVmomi` | latest |
| `jmespath` | latest |
| `packaging` | `<25.0, >=23.2` |

### Setting Up a PyPI Mirror

Use a tool such as `bandersnatch` or `pip2pi` on a connected host to
download and mirror the required packages:

```bash
pip download -r requirements-dev.txt -d /path/to/packages/
```

Transfer the packages to the disconnected environment and host them on
an internal PyPI-compatible server. Configure pip to use the internal
index:

```ini
# pip.conf or PIP_INDEX_URL environment variable
[global]
index-url = https://<internal-pypi>/simple/
trusted-host = <internal-pypi>
```

When building a custom Execution Environment with `ansible-builder`,
supply the internal PyPI URL in the EE definition:

```yaml
additional_build_steps:
  prepend_base:
    - RUN pip config set global.index-url https://<internal-pypi>/simple/
```

## 5. Git Repository Access

The Ansible for OpenShift Virtualization Migration project source and any GitOps export targets must
be reachable from the Ansible Automation Platform controller. In a
disconnected environment:

- Mirror the collection repository to an internal Git server (e.g.,
  GitLab, Gitea, or Bitbucket).
- Update the `aap_project_repo` inventory variable to point to the
  internal Git URL:

```yaml
aap_project_repo: https://<internal-git>/org/openshift_virtualization_migration.git
aap_project_branch: main
```

- If using the `vm_gitops_export` role (this role is planned to move to the `openshift_virtualization_ops` collection), ensure the target Git repository
  is also hosted internally and accessible from the EE.

## 6. Ansible Automation Platform Deployment

When deploying AAP in a disconnected environment:

- The AAP Operator must be included in the mirrored Operator catalog (assumes AAP is deployed on OpenShift) (it
  is not in the default list above — add the `ansible-automation-platform-operator`
  package to the `ImageSetConfiguration`).
- The AAP controller and hub pods must be able to pull images from the
  internal registry.
- Configure the AAP instance to use the Private Automation Hub as its
  primary content source.
- Ensure the EE image referenced in the inventory is available in the
  internal registry (see Section 2).

## 7. Network and Firewall Considerations

In a restricted (not fully air-gapped) environment, the following
endpoints may need firewall allowlisting:

| Endpoint | Purpose |
|---|---|
| `registry.redhat.io` | Red Hat container images |
| `cloud.redhat.com` | Automation Hub collections |
| `sso.redhat.com` | Automation Hub authentication |
| `quay.io` | Operator index images |
| `cdn.redhat.com` | Red Hat subscriptions |
| vCenter / RHV Manager host | Source hypervisor API access |
| OpenShift API endpoints | Cluster management (port 6443) |
| Internal registry | Mirrored images |
| Internal Git server | Project source code |
| Internal Automation Hub | Ansible collections |

For fully air-gapped environments, none of the external endpoints need
to be reachable — all content must be pre-mirrored.

## 8. Validation Checklist

Before running the Migration Factory in a disconnected environment,
verify the following:

- [ ] All required Operators are installable from the mirrored
      CatalogSource.
- [ ] The EE image is pullable from the internal registry.
- [ ] The VDDK image is pullable from the internal registry.
- [ ] All required Ansible collections are available in the Private
      Automation Hub.
- [ ] All required Python packages are available in the internal PyPI
      mirror (or baked into the EE).
- [ ] The collection Git repository is cloned on the internal Git
      server.
- [ ] AAP can reach the OpenShift API of all hub and spoke clusters.
- [ ] AAP can reach the source hypervisor (vCenter / RHV Manager).
- [ ] `oc-mirror` `ImageContentSourcePolicy` or `ImageDigestMirrorSet`
      resources are applied to all clusters.
- [ ] Default OperatorHub sources are disabled on all clusters.
