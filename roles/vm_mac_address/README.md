<!-- STATIC CONTENT START
Use this section for adding additional content to the README
This will not be overwritten by Docsible -->
# 📃 Role overview

<!-- STATIC CONTENT END -->
<!-- Everything below will be overwritten by Docsible -->
<!-- DOCSIBLE START -->
## vm_mac_address

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
Version - 1.21.3
Repository - https://github.com/redhat-cop/openshift_virtualization_migration
```

Description: Management of Virtual Machine MAC Addresses.

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Choices    |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|-------------|
| [`vm_mac_address_request`](defaults/main.yml#L7)   | list   | `[]` |  None  |   True  |  MAC Address Request |
| [`vm_mac_address_openshift_host`](defaults/main.yml#L17)   | str   | `{{ openshift_host }}` |  None  |   True  |  OpenShift Host |
| [`vm_mac_address_api_key`](defaults/main.yml#L21)   | str   | `{{ openshift_api_key }}` |  None  |   True  |  OpenShift API Key |
| [`vm_mac_address_openshift_verify_ssl`](defaults/main.yml#L25)   | str   | `{{ openshift_verify_ssl }}` |  None  |   True  |  Verify SSL Certificate |
| [`vm_mac_address_kubevirt_api_version`](defaults/main.yml#L29)   | str   | `kubevirt.io/v1` |  None  |   True  |  KubeVirt API Version |

<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<b>`vm_mac_address_request`:</b> List of MAC Address Requests
<br>
<b>`vm_mac_address_openshift_host`:</b> OpenShift Host
<br>
<b>`vm_mac_address_api_key`:</b> OpenShift API Key
<br>
<b>`vm_mac_address_openshift_verify_ssl`:</b> Verify SSL Certificate
<br>
<b>`vm_mac_address_kubevirt_api_version`:</b> KubeVirt API Version
<br>
<br>

### Tasks

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Verify vm_mac_address_request Variable Provided | `ansible.builtin.assert` | False |
| Verify Required Properties Provided | `ansible.builtin.assert` | False |
| Process MAC Address VM | `ansible.builtin.include_tasks` | False |

#### File: tasks/_compute_patch.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _compute_patch ¦ Verify Valid MAC Address Provided | `ansible.builtin.assert` | False |
| _compute_patch ¦ Locate Interface Index | `ansible.builtin.set_fact` | False |
| _compute_patch ¦ Create Patch Item | `ansible.builtin.set_fact` | True |

#### File: tasks/_process_vm.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _process_vm ¦ Initialize Variables | `ansible.builtin.set_fact` | False |
| _process_vm ¦ Query for Virtual Machine | `kubernetes.core.k8s_info` | False |
| _process_vm ¦ Verify Virtual Machine Exists | `ansible.builtin.assert` | False |
| _process_vm ¦ Compute Patch for Interface | `ansible.builtin.include_tasks` | True |
| _process_vm ¦ Update VM MAC Address | `kubernetes.core.k8s_json_patch` | True |

## Task Flow Graphs

### Graph for _compute_patch.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| _compute_patch___Verify_Valid_MAC_Address_Provided0[ compute patch   verify valid mac address provided]:::task
  _compute_patch___Verify_Valid_MAC_Address_Provided0-->|Task| _compute_patch___Locate_Interface_Index1[ compute patch   locate interface index]:::task
  _compute_patch___Locate_Interface_Index1-->|Task| _compute_patch___Create_Patch_Item2[ compute patch   create patch item<br>When: **vm mac address interface idx   length   0 and <br>macaddress  not in  vm mac address vm interfaces <br>vm mac address interface idx 0   or     <br>macaddress  in  vm mac address vm interfaces  vm<br>mac address interface idx 0   and    vm mac<br>address vm interfaces  vm mac address interface<br>idx 0   macaddress       vm mac address interface<br>macaddress**]:::task
  _compute_patch___Create_Patch_Item2-->End
```

### Graph for _process_vm.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| _process_vm___Initialize_Variables0[ process vm   initialize variables]:::task
  _process_vm___Initialize_Variables0-->|Task| _process_vm___Query_for_Virtual_Machine1[ process vm   query for virtual machine]:::task
  _process_vm___Query_for_Virtual_Machine1-->|Task| _process_vm___Verify_Virtual_Machine_Exists2[ process vm   verify virtual machine exists]:::task
  _process_vm___Verify_Virtual_Machine_Exists2-->|Include task| _process_vm___Compute_Patch_for_Interface__compute_patch_yml_3[ process vm   compute patch for interface<br>When: **vm mac address interface name   default     true <br>  length   0 and  vm mac address interface<br>macaddress   default     true    string   length  <br>0**<br>include_task:  compute patch yml]:::includeTasks
  _process_vm___Compute_Patch_for_Interface__compute_patch_yml_3-->|Task| _process_vm___Update_VM_MAC_Address4[ process vm   update vm mac address<br>When: **vm mac address interfaces patch   length   0**]:::task
  _process_vm___Update_VM_MAC_Address4-->End
```

### Graph for main.yml

```mermaid
flowchart TD
Start
classDef block stroke:#3498db,stroke-width:2px;
classDef task stroke:#4b76bb,stroke-width:2px;
classDef includeTasks stroke:#16a085,stroke-width:2px;
classDef importTasks stroke:#34495e,stroke-width:2px;
classDef includeRole stroke:#2980b9,stroke-width:2px;
classDef importRole stroke:#699ba7,stroke-width:2px;
classDef includeVars stroke:#8e44ad,stroke-width:2px;
classDef rescue stroke:#665352,stroke-width:2px;

  Start-->|Task| Verify_vm_mac_address_request_Variable_Provided0[verify vm mac address request variable provided]:::task
  Verify_vm_mac_address_request_Variable_Provided0-->|Task| Verify_Required_Properties_Provided1[verify required properties provided]:::task
  Verify_Required_Properties_Provided1-->|Include task| Process_MAC_Address_VM__process_vm_yml_2[process mac address vm<br>include_task:  process vm yml]:::includeTasks
  Process_MAC_Address_VM__process_vm_yml_2-->End
```

## Playbook

```yml
---
- name: Test
  hosts: localhost
  remote_user: root
  roles:
    - vm_mac_address
...

```

## Playbook graph

```mermaid
flowchart TD
  hosts[localhost]-->|Role| vm_mac_address[vm mac address]
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