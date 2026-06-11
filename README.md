# Ansible for OpenShift Virtualization Migration

![GitHub Release](https://img.shields.io/github/v/release/redhat-cop/openshift_virtualization_migration?include_prereleases&style=flat-square)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/redhat-cop/openshift_virtualization_migration/ci.yml?style=flat-square&label=release)](https://github.com/redhat-cop/openshift_virtualization_migration/actions)
[![Semantic Versioning](https://img.shields.io/badge/semver-2.0.0-blue?style=flat-square)](https://semver.org/)
[![License](https://img.shields.io/github/license/redhat-cop/openshift_virtualization_migration?style=flat-square)](LICENSE)

<!--TOC-->

- [Ansible for OpenShift Virtualization Migration](#ansible-for-openshift-virtualization-migration)
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

## Release Notes

See [CHANGELOG.md](CHANGELOG.md) for release history and changes.

## Roles

This collection includes the following roles for managing OpenShift Virtualization migrations:

<!--ROLES_LIST_START-->
* [aap_deploy](roles/aap_deploy/README.md) - Deploys an instance of Ansible Automation Platform.
* [aap_machine_credentials](roles/aap_machine_credentials/README.md) - Management of Machine Credentials.
* [aap_seed](roles/aap_seed/README.md) - Populates an Ansible Automation Platform instance.
* [bootstrap](roles/bootstrap/README.md) - Initialization of the Ansible for OpenShift Virtualization Migration environment.
* [create_mf_aap_token](roles/create_mf_aap_token/README.md) - create_mf_aap_token
* [mtv_management](roles/mtv_management/README.md) - Management of the Migration Toolkit for Virtualization (MTV).
* [mtv_migrate](roles/mtv_migrate/README.md) - Migration of Virtual Machines from Source to Destination.
* [network_mgmt](roles/network_mgmt/README.md) - Management of network related components.
* [operator_management](roles/operator_management/README.md) - Management of OpenShift Operators.
* [validate_migration](roles/validate_migration/README.md) - Verification of an Ansible for OpenShift Virtualization Migration environment.
* [vm_backup_restore](roles/vm_backup_restore/README.md) - Virtual Machine backup and restore capabilities.
* [vm_collect](roles/vm_collect/README.md) - Collection of Migration Toolkit for Virtualization inventory information.
* [vm_hot_plug](roles/vm_hot_plug/README.md) - Hot Plug Virtual Machine resources.
* [vm_lifecycle](roles/vm_lifecycle/README.md) - Management of the lifecycle activities of Virtual Machines.
* [vm_mac_address](roles/vm_mac_address/README.md) - Management of Virtual Machine MAC Addresses.
* [vm_networking](roles/vm_networking/README.md) - Management of Virtual Machine networking.
* [vm_patching](roles/vm_patching/README.md) - Patching related activities for Virtual Machines.
* [vm_ssh](roles/vm_ssh/README.md) - Management of SSH keys for Virtual Machines in OpenShift.
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

```
ansible-galaxy collection install infra.openshift_virtualization_migration --upgrade
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.openshift_virtualization_migration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

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
