# OpenShift Virtualization Migration Collection

![GitHub Release](https://img.shields.io/github/v/release/redhat-cop/openshift_virtualization_migration?include_prereleases&style=flat-square)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/redhat-cop/openshift_virtualization_migration/ci.yml?style=flat-square&label=release)](https://github.com/redhat-cop/openshift_virtualization_migration/actions)
[![Semantic Versioning](https://img.shields.io/badge/semver-2.0.0-blue?style=flat-square)](https://semver.org/)
[![License](https://img.shields.io/github/license/redhat-cop/openshift_virtualization_migration?style=flat-square)](LICENSE)

<!--TOC-->

- [OpenShift Virtualization Migration Collection](#openshift-virtualization-migration-collection)
  - [Description](#description)
  - [Documentation](#documentation)
  - [Release Notes](#release-notes)
  - [Roles](#roles)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Use Cases](#use-cases)
  - [Testing](#testing)
  - [Support](#support)
  - [License](#license)

<!--TOC-->

## Description

This collection enables the migration journey of Virtual Machine (VM) workloads from existing hypervisors to Red Hat OpenShift Virtualization using Ansible Automation Platform. Additionally it provides content for the management and maintenance of VM workloads within Red Hat OpenShift Virtualization.

## Documentation

* [Contributing Guide](CONTRIBUTING.md)
* [Disconnected Environment Setup](docs/disconnected_environment_guide.md)
* [Secure Credential Management](docs/secure_credential_management.md)
* [Secure Credential Practices](docs/secure_credential_practices.md)
* [Security Policy](SECURITY.md)

## Release Notes

See [CHANGELOG.md](CHANGELOG.md) for release history and changes.

## Roles

This collection includes the following roles for managing OpenShift Virtualization migrations:

<!--ROLES_LIST_START-->
* [aap_seed](roles/aap_seed/README.md) - Seed AAP with Migration Factory Configuration as Code content
* [mtv_plans](roles/mtv_plans/README.md) - Manages MTV migration plans.
* [mtv_provider](roles/mtv_provider/README.md) - Create MTV/Forklift source provider CRs on OpenShift target clusters. Designed to run from AAP with credential injection.
* [mtv_query_inventory](roles/mtv_query_inventory/README.md) - Queries MTV inventory.
* [utility_aap_deploy](roles/utility_aap_deploy/README.md) - Deploys an instance of Ansible Automation Platform.
* [utility_openshift_target_credential](roles/utility_openshift_target_credential/README.md) - A utility role to manage OpenShift target cluster credentials for migration
<!--ROLES_LIST_END-->

## Requirements

The following Ansible Collections are required:

```yaml
---
collections:
  - name: redhat.openshift_virtualization
  - name: redhat.openshift
  - name: vmware.vmware_rest
  - name: ansible.posix
  - name: infra.aap_utilities
  - name: kubernetes.core
  - name: community.crypto
  - name: community.general
  - name: community.vmware

  # AAP <=2.4
  - name: infra.controller_configuration
  - name: ansible.controller
    version: "<=4.5.12"

  # AAP 2.5+
  - name: ansible.platform
  - name: ansible.controller
  - name: infra.aap_configuration
...
```

## Installation

You can install the `infra.openshift_virtualization_migration` collection with the Ansible Galaxy CLI:

```shell
ansible-galaxy collection install infra.openshift_virtualization_migration
```

Note that if you install any collections from Ansible Galaxy, they will not be upgraded automatically when you upgrade the Ansible package.

To upgrade the collection to the latest available version, run the following command:

```shell
ansible-galaxy collection install infra.openshift_virtualization_migration --upgrade
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.openshift_virtualization_migration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
...
```

See
[Using Ansible Collections](https://docs.ansible.com/projects/ansible/latest/collections_guide/index.html)
for more details.

## Use Cases

This collection is ideal for accomplishing the following using Ansible automation:

* Analyzing existing Virtual Machine hypervisor environments.
* Installing and configuring Ansible Automation Platform.
* Preparing OpenShift environments to support Virtual Machines and migrating Virtual Machines from existing hypervisors using the Migration Toolkit for Virtualization (MTV).
* Migrating Virtual Machines using the Migration Toolkit for Virtualization (MTV).

## Testing

[tox](https://tox.wiki) is used to perform tests and verification of this collection.

The following commands can be used to execute the various types of tests implemented:

```shell
tox -av # lists all tests

tox # run them all

tox -e <test name> # run specific one

tox -f sanity --ansible -c tox-ansible.ini     # run tox-ansible that does our ansible-test sanity suite
```

## Support

The [Ansible Forum](https://forum.ansible.com/tag/openshift_migrate) can be used for additional questions and issues related to this collection.

## License

GNU General Public License v3.0 or later.

See the [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) to see the full text.
