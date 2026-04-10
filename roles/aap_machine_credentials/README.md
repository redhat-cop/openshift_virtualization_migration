<!-- STATIC CONTENT START
Use this section for adding additional content to the README
This will not be overwritten by Docsible -->
# 📃 Role overview

This role enables the management of Ansible Automation Platform _Credentials_.

<!-- STATIC CONTENT END -->
<!-- Everything below will be overwritten by Docsible -->
<!-- DOCSIBLE START -->
## aap_machine_credentials

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
Version - 1.23.0
Repository - https://github.com/redhat-cop/openshift_virtualization_migration
```

Description: Management of Machine Credentials.

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Choices    |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|-------------|
| [`aap_machine_credentials_request`](defaults/main.yml#L7)   | list   | `[]` |  None  |   True  |  List of AAP Credentials |
| [`aap_machine_credentials_organization`](defaults/main.yml#L15)   | str   | `{{ aap_project ¦ default('OpenShift Virtualization Migration', true) }}` |  None  |   True  |  Organization name in AAP host |
| [`aap_machine_credentials_cac_credentials_role`](defaults/main.yml#L20)   | str   | `<multiline value: folded_strip>` |  None  |   True  |  Ansible Automation Platform configuration collection credentials role |

<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<b>`aap_machine_credentials_request`:</b> List of credentials to access AAP provided by _process_machine_credential.yml
<br>
<b>`aap_machine_credentials_organization`:</b> Name of the organization in AAP
<br>
<b>`aap_machine_credentials_cac_credentials_role`:</b> Determines which collection to use for configuring AAP based on the version.
<br>
<br>

### Vars

**These are variables with higher priority**

#### File: vars/main.yml

| Var          | Type         | Value       |
|--------------|--------------|-------------|
| [aap_machine_credentials_input_keys](vars/main.yml#L3)   | list   | `[]` |
| [aap_machine_credentials_input_keys.0](vars/main.yml#L4)   | str   | `username` |
| [aap_machine_credentials_input_keys.1](vars/main.yml#L5)   | str   | `password` |
| [aap_machine_credentials_input_keys.2](vars/main.yml#L6)   | str   | `ssh_key_data` |
| [aap_machine_credentials_input_keys.3](vars/main.yml#L7)   | str   | `ssh_public_key_data` |
| [aap_machine_credentials_input_keys.4](vars/main.yml#L8)   | str   | `ssh_key_unlock` |
| [aap_machine_credentials_input_keys.5](vars/main.yml#L9)   | str   | `become_method` |
| [aap_machine_credentials_input_keys.6](vars/main.yml#L10)   | str   | `become_username` |
| [aap_machine_credentials_input_keys.7](vars/main.yml#L11)   | str   | `become_password` |
| [aap_machine_credentials_input_keys.8](vars/main.yml#L12)   | str   | `state` |
| [aap_machine_credentials_base_keys](vars/main.yml#L14)   | list   | `[]` |
| [aap_machine_credentials_base_keys.0](vars/main.yml#L15)   | dict   | `{}` |
| [aap_machine_credentials_base_keys.0.name](vars/main.yml#L15)   | str   | `name` |
| [aap_machine_credentials_base_keys.1](vars/main.yml#L16)   | dict   | `{}` |
| [aap_machine_credentials_base_keys.1.name](vars/main.yml#L16)   | str   | `description` |
| [aap_machine_credentials_base_keys.2](vars/main.yml#L17)   | dict   | `{}` |
| [aap_machine_credentials_base_keys.2.name](vars/main.yml#L17)   | str   | `organization` |
| [aap_machine_credentials_base_keys.2.default](vars/main.yml#L18)   | str   | `{{ aap_machine_credentials_organization }}` |
| [aap_machine_credentials_base_keys.3](vars/main.yml#L19)   | dict   | `{}` |
| [aap_machine_credentials_base_keys.3.name](vars/main.yml#L19)   | str   | `credential_type` |
| [aap_machine_credentials_base_keys.3.default](vars/main.yml#L20)   | str   | `Machine` |
| [aap_machine_credentials_input_maps](vars/main.yml#L22)   | list   | `[]` |
| [aap_machine_credentials_input_maps.0](vars/main.yml#L23)   | dict   | `{}` |
| [aap_machine_credentials_input_maps.0.src](vars/main.yml#L23)   | str   | `ssh_key_data_path` |
| [aap_machine_credentials_input_maps.0.dest](vars/main.yml#L24)   | str   | `ssh_key_data` |
| [aap_machine_credentials_input_maps.1](vars/main.yml#L25)   | dict   | `{}` |
| [aap_machine_credentials_input_maps.1.src](vars/main.yml#L25)   | str   | `ssh_public_key_data_path` |
| [aap_machine_credentials_input_maps.1.dest](vars/main.yml#L26)   | str   | `ssh_public_key_data` |

### Tasks

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Initialize Variables | `ansible.builtin.set_fact` | False |
| Process Machine Credentials | `ansible.builtin.include_tasks` | False |
| Manage Credentials | `block` | False |
| Verify Config as Code parameters required (for AAP 2.4 and below) | `ansible.builtin.assert` | True |
| Verify Config as Code parameters required (for AAP 2.5 and above) | `ansible.builtin.assert` | True |
| Call credential config as code role | `ansible.builtin.include_role` | True |

#### File: tasks/_map_key_content.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _map_key_content ¦ Verify required variables provided | `ansible.builtin.assert` | False |
| _map_key_content ¦ Check source path content | `ansible.builtin.stat` | False |
| _map_key_content ¦ Verify source path exists | `ansible.builtin.assert` | False |
| _map_key_content ¦ Map Variables | `ansible.builtin.set_fact` | False |

#### File: tasks/_process_machine_credential.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| _process_machine_credential ¦ Initialize Dynamic Map Variable | `ansible.builtin.set_fact` | False |
| _process_machine_credential ¦ Map Credential File Contents | `ansible.builtin.include_tasks` | True |
| _process_machine_credential ¦ Render Machine Credential | `ansible.builtin.set_fact` | False |

## Task Flow Graphs

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

  Start-->|Task| Initialize_Variables0[initialize variables]:::task
  Initialize_Variables0-->|Include task| Process_Machine_Credentials__process_machine_credential_yml_1[process machine credentials<br>include_task:  process machine credential yml]:::includeTasks
  Process_Machine_Credentials__process_machine_credential_yml_1-->|Block Start| Manage_Credentials2_block_start_0[[manage credentials]]:::block
  Manage_Credentials2_block_start_0-->|Task| Verify_Config_as_Code_parameters_required__for_AAP_2_4_and_below_0[verify config as code parameters required  for aap<br>2 4 and below <br>When: **aap version is defined and aap version is version <br>2 5**]:::task
  Verify_Config_as_Code_parameters_required__for_AAP_2_4_and_below_0-->|Task| Verify_Config_as_Code_parameters_required__for_AAP_2_5_and_above_1[verify config as code parameters required  for aap<br>2 5 and above <br>When: **aap version is not defined or aap version is<br>version  2 5**]:::task
  Verify_Config_as_Code_parameters_required__for_AAP_2_5_and_above_1-.->|End of Block| Manage_Credentials2_block_start_0
  Verify_Config_as_Code_parameters_required__for_AAP_2_5_and_above_1-->|Include role| Call_credential_config_as_code_role____aap_machine_credentials_cac_credentials_role____3(call credential config as code role<br>When: **aap machine credentials controller credentials  <br>length   0**<br>include_role:    aap machine credentials cac credentials role   ):::includeRole
  Call_credential_config_as_code_role____aap_machine_credentials_cac_credentials_role____3-->End
```

### Graph for _map_key_content.yml

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

  Start-->|Task| _map_key_content___Verify_required_variables_provided0[ map key content   verify required variables<br>provided]:::task
  _map_key_content___Verify_required_variables_provided0-->|Task| _map_key_content___Check_source_path_content1[ map key content   check source path content]:::task
  _map_key_content___Check_source_path_content1-->|Task| _map_key_content___Verify_source_path_exists2[ map key content   verify source path exists]:::task
  _map_key_content___Verify_source_path_exists2-->|Task| _map_key_content___Map_Variables3[ map key content   map variables]:::task
  _map_key_content___Map_Variables3-->End
```

### Graph for _process_machine_credential.yml

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

  Start-->|Task| _process_machine_credential___Initialize_Dynamic_Map_Variable0[ process machine credential   initialize dynamic<br>map variable]:::task
  _process_machine_credential___Initialize_Dynamic_Map_Variable0-->|Include task| _process_machine_credential___Map_Credential_File_Contents__map_key_content_yml_1[ process machine credential   map credential file<br>contents<br>When: **aap machine credentials input map  src   in aap<br>machine credential**<br>include_task:  map key content yml]:::includeTasks
  _process_machine_credential___Map_Credential_File_Contents__map_key_content_yml_1-->|Task| _process_machine_credential___Render_Machine_Credential2[ process machine credential   render machine<br>credential]:::task
  _process_machine_credential___Render_Machine_Credential2-->End
```

## Playbook

```yml
---
- name: Test
  hosts: localhost
  remote_user: root
  roles:
    - aap_machine_credentials

...

```

## Playbook graph

```mermaid
flowchart TD
  hosts[localhost]-->|Role| aap_machine_credentials[aap machine credentials]
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