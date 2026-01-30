<!-- STATIC CONTENT START
Use this section for adding additional content to the README
This will not be overwritten by Docsible -->
# 📃 Role overview

This role manages SSH access to virtual machines on OpenShift cluster.

<!-- STATIC CONTENT END -->
<!-- Everything below will be overwritten by Docsible -->
<!-- DOCSIBLE START -->
## vm_ssh

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
Version - 1.21.4
Repository - https://github.com/redhat-cop/openshift_virtualization_migration
```

Description: Management of SSH keys for Virtual Machines in OpenShift.

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Choices    |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|-------------|
| [`vm_ssh_request`](defaults/main.yml#L7)   | dict   | `{}` |  None  |   True  |  SSH Requests |
| [`vm_ssh_openshift_host`](defaults/main.yml#L26)   | str   | `{{ openshift_host }}` |  None  |   True  |  OpenShift host |
| [`vm_ssh_openshift_api_key`](defaults/main.yml#L31)   | str   | `{{ openshift_api_key }}` |  None  |   True  |  OpenShift API Key |
| [`vm_ssh_openshift_verify_ssl`](defaults/main.yml#L36)   | str   | `{{ openshift_verify_ssl }}` |  None  |   True  |  Verify SSL Certificate |
| [`vm_ssh_default_users`](defaults/main.yml#L41)   | list   | `[]` |  None  |   True  |  List of default SSH users |
| [`vm_ssh_default_users.0`](defaults/main.yml#L42)   | str   | `root` |  None  |   None  |  None |
| [`vm_ssh_kubevirt_api_version`](defaults/main.yml#L47)   | str   | `kubevirt.io/v1` |  None  |   True  |  KubeVirt API Version |

<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<b>`vm_ssh_request`:</b> SSH Requests
<br>
<b>`vm_ssh_openshift_host`:</b> OpenShift host
<br>
<b>`vm_ssh_openshift_api_key`:</b> OpenShift API Key
<br>
<b>`vm_ssh_openshift_verify_ssl`:</b> Variable to enable SSL verification
<br>
<b>`vm_ssh_default_users`:</b> List of default SSH users (default user: root)
<br>
<b>`vm_ssh_default_users.0`:</b> None
<br>
<b>`vm_ssh_kubevirt_api_version`:</b> KubeVirt API Version
<br>
<br>

### Tasks

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Verify OpenShift Connectivity Details Provided | `ansible.builtin.assert` | False |
| Manage Secrets | `block` | True |
| Process Secrets | `ansible.builtin.include_tasks` | False |
| Manage Targets | `block` | True |
| Process Targets | `ansible.builtin.include_tasks` | False |

#### File: tasks/_manage_secret_keys.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _manage_secret_keys ¦ Verify SSH path location or inline content provided | `ansible.builtin.assert` | False |
| _manage_secret_keys ¦ Process Key from Path | `block` | True |
| _manage_secret_keys ¦ Get SSH Key Path information | `ansible.builtin.stat` | False |
| _manage_secret_keys ¦ Verify SSH Key Path Exists | `ansible.builtin.assert` | False |
| _manage_secret_keys ¦ Add 'path' Key to Dict | `ansible.builtin.set_fact` | False |
| _manage_secret_keys ¦ Process Key from Path | `block` | True |
| _manage_secret_keys ¦ Add 'content' Key to Dict | `ansible.builtin.set_fact` | False |

#### File: tasks/_manage_secrets.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _manage_secrets ¦ Verify Secret Namespace and Name Provided | `ansible.builtin.assert` | False |
| _manage_secrets ¦ Initialize SSH Keys Variables | `ansible.builtin.set_fact` | False |
| _manage_secrets ¦ Manage Secret SSH Keys | `ansible.builtin.include_tasks` | True |
| _manage_secrets ¦ Create SSH Key Secret | `redhat.openshift.k8s` | False |

#### File: tasks/_manage_target.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _manage_target ¦ Update VirtualMachine with SSH Configuration | `redhat.openshift.k8s` | False |
| _manage_target ¦ Query VM for Updated Configuration | `kubernetes.core.k8s_info` | False |
| _manage_target ¦ Restart the machine | `block` | True |
| _manage_target ¦ Restart the VirtualMachine | `ansible.builtin.include_role` | False |
| _manage_target ¦ Verify the VirtualMachine restarted | `ansible.builtin.include_role` | False |

#### File: tasks/_manage_targets.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _manage_targets ¦ Verify Namespace and Secret Name Provided | `ansible.builtin.assert` | False |
| _manage_targets ¦ Invoke Collect VM Role | `ansible.builtin.include_role` | False |
| _manage_targets ¦ Update VirtualMachine with SSH Configurations | `ansible.builtin.include_tasks` | False |

## Task Flow Graphs

### Graph for _manage_secret_keys.yml

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

  Start-->|Task| _manage_secret_keys___Verify_SSH_path_location_or_inline_content_provided0[ manage secret keys   verify ssh path location or<br>inline content provided]:::task
  _manage_secret_keys___Verify_SSH_path_location_or_inline_content_provided0-->|Block Start| _manage_secret_keys___Process_Key_from_Path1_block_start_0[[ manage secret keys   process key from path<br>When: **path  in ssh key**]]:::block
  _manage_secret_keys___Process_Key_from_Path1_block_start_0-->|Task| _manage_secret_keys___Get_SSH_Key_Path_information0[ manage secret keys   get ssh key path information]:::task
  _manage_secret_keys___Get_SSH_Key_Path_information0-->|Task| _manage_secret_keys___Verify_SSH_Key_Path_Exists1[ manage secret keys   verify ssh key path exists]:::task
  _manage_secret_keys___Verify_SSH_Key_Path_Exists1-->|Task| _manage_secret_keys___Add__path__Key_to_Dict2[ manage secret keys   add  path  key to dict]:::task
  _manage_secret_keys___Add__path__Key_to_Dict2-.->|End of Block| _manage_secret_keys___Process_Key_from_Path1_block_start_0
  _manage_secret_keys___Add__path__Key_to_Dict2-->|Block Start| _manage_secret_keys___Process_Key_from_Path2_block_start_0[[ manage secret keys   process key from path<br>When: **content  in ssh key**]]:::block
  _manage_secret_keys___Process_Key_from_Path2_block_start_0-->|Task| _manage_secret_keys___Add__content__Key_to_Dict0[ manage secret keys   add  content  key to dict]:::task
  _manage_secret_keys___Add__content__Key_to_Dict0-.->|End of Block| _manage_secret_keys___Process_Key_from_Path2_block_start_0
  _manage_secret_keys___Add__content__Key_to_Dict0-->End
```

### Graph for _manage_secrets.yml

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

  Start-->|Task| _manage_secrets___Verify_Secret_Namespace_and_Name_Provided0[ manage secrets   verify secret namespace and name<br>provided]:::task
  _manage_secrets___Verify_Secret_Namespace_and_Name_Provided0-->|Task| _manage_secrets___Initialize_SSH_Keys_Variables1[ manage secrets   initialize ssh keys variables]:::task
  _manage_secrets___Initialize_SSH_Keys_Variables1-->|Include task| _manage_secrets___Manage_Secret_SSH_Keys__manage_secret_keys_yml_2[ manage secrets   manage secret ssh keys<br>When: **ssh keys  in ssh secret**<br>include_task:  manage secret keys yml]:::includeTasks
  _manage_secrets___Manage_Secret_SSH_Keys__manage_secret_keys_yml_2-->|Task| _manage_secrets___Create_SSH_Key_Secret3[ manage secrets   create ssh key secret]:::task
  _manage_secrets___Create_SSH_Key_Secret3-->End
```

### Graph for _manage_target.yml

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

  Start-->|Task| _manage_target___Update_VirtualMachine_with_SSH_Configuration0[ manage target   update virtualmachine with ssh<br>configuration]:::task
  _manage_target___Update_VirtualMachine_with_SSH_Configuration0-->|Task| _manage_target___Query_VM_for_Updated_Configuration1[ manage target   query vm for updated<br>configuration]:::task
  _manage_target___Query_VM_for_Updated_Configuration1-->|Block Start| _manage_target___Restart_the_machine2_block_start_0[[ manage target   restart the machine<br>When: **resources  in vm ssh update response and vm ssh<br>update response   length   0  and  status  in vm<br>ssh update response resources 0  and  conditions <br>in vm ssh update response resources 0  status and <br>   vm ssh update response resources 0  status<br>conditions     selectattr  type    equalto   <br>restartrequired       list     length   0**]]:::block
  _manage_target___Restart_the_machine2_block_start_0-->|Include role| _manage_target___Restart_the_VirtualMachine_infra_openshift_virtualization_migration_vm_lifecycle_0( manage target   restart the virtualmachine<br>include_role: infra openshift virtualization migration vm<br>lifecycle):::includeRole
  _manage_target___Restart_the_VirtualMachine_infra_openshift_virtualization_migration_vm_lifecycle_0-->|Include role| _manage_target___Verify_the_VirtualMachine_restarted_infra_openshift_virtualization_migration_vm_lifecycle_1( manage target   verify the virtualmachine<br>restarted<br>include_role: infra openshift virtualization migration vm<br>lifecycle):::includeRole
  _manage_target___Verify_the_VirtualMachine_restarted_infra_openshift_virtualization_migration_vm_lifecycle_1-.->|End of Block| _manage_target___Restart_the_machine2_block_start_0
  _manage_target___Verify_the_VirtualMachine_restarted_infra_openshift_virtualization_migration_vm_lifecycle_1-->End
```

### Graph for _manage_targets.yml

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

  Start-->|Task| _manage_targets___Verify_Namespace_and_Secret_Name_Provided0[ manage targets   verify namespace and secret name<br>provided]:::task
  _manage_targets___Verify_Namespace_and_Secret_Name_Provided0-->|Include role| _manage_targets___Invoke_Collect_VM_Role_infra_openshift_virtualization_migration_vm_collect_1( manage targets   invoke collect vm role<br>include_role: infra openshift virtualization migration vm<br>collect):::includeRole
  _manage_targets___Invoke_Collect_VM_Role_infra_openshift_virtualization_migration_vm_collect_1-->|Include task| _manage_targets___Update_VirtualMachine_with_SSH_Configurations__manage_target_yml_2[ manage targets   update virtualmachine with ssh<br>configurations<br>include_task:  manage target yml]:::includeTasks
  _manage_targets___Update_VirtualMachine_with_SSH_Configurations__manage_target_yml_2-->End
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

  Start-->|Task| Verify_OpenShift_Connectivity_Details_Provided0[verify openshift connectivity details provided]:::task
  Verify_OpenShift_Connectivity_Details_Provided0-->|Block Start| Manage_Secrets1_block_start_0[[manage secrets<br>When: **secrets  in vm ssh request   default**]]:::block
  Manage_Secrets1_block_start_0-->|Include task| Process_Secrets__manage_secrets_yml_0[process secrets<br>include_task:  manage secrets yml]:::includeTasks
  Process_Secrets__manage_secrets_yml_0-.->|End of Block| Manage_Secrets1_block_start_0
  Process_Secrets__manage_secrets_yml_0-->|Block Start| Manage_Targets2_block_start_0[[manage targets<br>When: **targets  in vm ssh request   default**]]:::block
  Manage_Targets2_block_start_0-->|Include task| Process_Targets__manage_targets_yml_0[process targets<br>include_task:  manage targets yml]:::includeTasks
  Process_Targets__manage_targets_yml_0-.->|End of Block| Manage_Targets2_block_start_0
  Process_Targets__manage_targets_yml_0-->End
```

## Playbook

```yml
---
- name: Test
  hosts: localhost
  remote_user: root
  roles:
    - vm_ssh
...

```

## Playbook graph

```mermaid
flowchart TD
  hosts[localhost]-->|Role| vm_ssh[vm ssh]
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
