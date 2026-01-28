<!-- STATIC CONTENT START
Use this section for adding additional content to the README
This will not be overwritten by Docsible -->
# 📃 Role overview

**DEPRECATED:** This role is deprecated here because it was moved to the `openshift_virtualization_ops` collection.

<!-- STATIC CONTENT END -->
<!-- Everything below will be overwritten by Docsible -->
<!-- DOCSIBLE START -->
## vm_networking

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
Version - 1.21.4
Repository - https://github.com/redhat-cop/openshift_virtualization_migration
```

Description: Management of Virtual Machine networking.

### Tasks

## Playbook

```yml
---
- name: Test
  hosts: localhost
  remote_user: root
  roles:
    - vm_networking
...

```

## Playbook graph

```mermaid
flowchart TD
  hosts[localhost]-->|Role| vm_networking[vm networking]
```

## Author Information

OpenShift Virtualization Migration Contributors

## License

GPL-3.0-only

## Minimum Ansible Version

2.15.0

## Platforms

No platforms specified.

<!-- DOCSIBLE END -->