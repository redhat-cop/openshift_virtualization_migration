<!-- DOCSIBLE START -->

# 📃 Role overview

## aap_seed



Description: Seed AAP with Migration Factory Configuration as Code content

| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 2026/09/02 |




<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- Dynamically builds all AAP Configuration as Code objects from the Ansible inventory and role defaults, syncs the SCM project, and pushes everything to AAP via infra.aap_configuration.dispatch.
- Object types managed include credential types, credentials, inventories, hosts, groups, projects, job templates, execution environments, and organizations.
- Target cluster credentials use the built-in AAP credential type "OpenShift or Kubernetes API Bearer Token".
- Each object type can be skipped with a C(_create) toggle or replaced entirely by overriding the corresponding C(aap_seed_controller_*) variable.


**Options**:


  - **aap_seed_hostname**
    - **Required**: False
    - **Type**: str
    - **Default**: none
  
    - **Description**: FQDN or URL of the AAP controller API endpoint. Defaults to C(aap_hostname) from inventory.
  
  
  

  - **aap_seed_username**
    - **Required**: False
    - **Type**: str
    - **Default**: none
  
    - **Description**: Username for AAP controller authentication. Mutually exclusive with I(aap_seed_token). Defaults to C(aap_username) from inventory.
  
  
  

  - **aap_seed_password**
    - **Required**: False
    - **Type**: str
    - **Default**: none
  
    - **Description**: Password for AAP controller authentication. Mutually exclusive with I(aap_seed_token). Defaults to C(aap_password) from inventory.
  
  
  

  - **aap_seed_token**
    - **Required**: False
    - **Type**: str
    - **Default**: none
  
    - **Description**: OAuth token for AAP controller authentication. Mutually exclusive with I(aap_seed_username)/I(aap_seed_password). Defaults to C(aap_token) from inventory.
  
  
  

  - **aap_seed_validate_certs**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to validate TLS certificates when connecting to AAP. Defaults to C(aap_validate_certs) from inventory, or C(true) if unset.
  
  
  

  - **aap_seed_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Suppress task output for credential loops to prevent secrets from leaking to logs.  Set to C(false) when debugging credential construction.
  
  
  

  - **aap_seed_org_name**
    - **Required**: False
    - **Type**: str
    - **Default**: Default
  
    - **Description**: AAP organization that owns the project, inventory, and credentials.
  
  
  

  - **aap_seed_project_name**
    - **Required**: False
    - **Type**: str
    - **Default**: OpenShift Virtualization Migration
  
    - **Description**: Name of the SCM-backed project created in AAP.
  
  
  

  - **aap_seed_project_scm_url**
    - **Required**: False
    - **Type**: str
    - **Default**: https://github.com/redhat-cop/openshift_virtualization_migration.git
  
    - **Description**: Git URL used as the project SCM source. Defaults to C(aap_project_scm_url) from inventory.
  
  
  

  - **aap_seed_project_scm_branch**
    - **Required**: False
    - **Type**: str
    - **Default**: v2
  
    - **Description**: Git branch or tag to checkout for the project. Defaults to C(aap_project_scm_branch) from inventory.
  
  
  

  - **aap_seed_project_sync_timeout**
    - **Required**: False
    - **Type**: int
    - **Default**: 120
  
    - **Description**: Maximum seconds to wait for the SCM project sync to complete.
  
  
  

  - **aap_seed_inventory_name**
    - **Required**: False
    - **Type**: str
    - **Default**: OpenShift Virtualization Migration
  
    - **Description**: Name of the inventory created in AAP. Source and target hosts are added to this inventory.
  
  
  

  - **aap_seed_execution_environment**
    - **Required**: False
    - **Type**: str
    - **Default**: Default execution environment
  
    - **Description**: Execution environment assigned to job templates.
  
  
  

  - **aap_seed_source_credential_type**
    - **Required**: False
    - **Type**: str
    - **Default**: Migration Factory - Source Environment
  
    - **Description**: Name of the custom credential type created in AAP for source hypervisor environments (vSphere, RHV).
  
  
  

  - **aap_seed_target_credential_type**
    - **Required**: False
    - **Type**: str
    - **Default**: OpenShift or Kubernetes API Bearer Token
  
    - **Description**: AAP credential type used for target OpenShift clusters. Defaults to the built-in bearer token type. Each target host should set I(openshift_api_key) or I(openshift_temporary_api_key).
  
  
  

  - **aap_seed_project_credential**
    - **Required**: False
    - **Type**: str
    - **Default**: 
  
    - **Description**: Name of the Git credential to create and attach to the SCM project. Leave empty to skip. Defaults to C(aap_project_credential) from inventory.
  
  
  

  - **aap_seed_git_username**
    - **Required**: False
    - **Type**: str
    - **Default**: 
  
    - **Description**: Git username for HTTPS authentication. Defaults to C(aap_git_username) from inventory.
  
  
  

  - **aap_seed_git_password**
    - **Required**: False
    - **Type**: str
    - **Default**: 
  
    - **Description**: Git password or personal access token. Defaults to C(aap_git_password) from inventory.
  
  
  

  - **aap_seed_git_ssh_key**
    - **Required**: False
    - **Type**: str
    - **Default**: 
  
    - **Description**: SSH private key for Git authentication. Defaults to C(aap_git_ssh_key) from inventory.
  
  
  

  - **aap_seed_git_ssh_key_unlock**
    - **Required**: False
    - **Type**: str
    - **Default**: 
  
    - **Description**: Passphrase to unlock the SSH key. Defaults to C(aap_git_ssh_key_unlock) from inventory.
  
  
  

  - **aap_seed_mtv_provider_template_name**
    - **Required**: False
    - **Type**: str
    - **Default**: OpenShift Virtualization Migration - MTV Provider
  
    - **Description**: Name of the MTV Provider job template created in AAP.
  
  
  

  - **aap_seed_mtv_provider_playbook**
    - **Required**: False
    - **Type**: str
    - **Default**: playbooks/vmf_mtv_provider.yml
  
    - **Description**: Playbook path for the MTV Provider job template.
  
  
  

  - **aap_seed_source_inventory_group**
    - **Required**: False
    - **Type**: str
    - **Default**: vm_sources
  
    - **Description**: Ansible inventory group containing source hypervisor hosts. Each host in this group becomes an AAP inventory host and a source-environment credential.
  
  
  

  - **aap_seed_target_inventory_group**
    - **Required**: False
    - **Type**: str
    - **Default**: migration_clusters
  
    - **Description**: Ansible inventory group containing target OpenShift cluster hosts. Each host in this group becomes an AAP inventory host and a target-cluster credential.
  
  
  

  - **aap_seed_organizations_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Create organizations in AAP. Set to C(false) to skip. Only applies when I(aap_seed_controller_organizations) is non-empty.
  
  
  

  - **aap_seed_credential_types_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Create the custom source credential type in AAP. Set to C(false) to skip.
  
  
  

  - **aap_seed_credentials_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Build and push credentials for source and target hosts. Set to C(false) to skip.
  
  
  

  - **aap_seed_inventories_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Create the AAP inventory. Set to C(false) to skip.
  
  
  

  - **aap_seed_hosts_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Build and push inventory hosts and groups from the Ansible inventory. Set to C(false) to skip.
  
  
  

  - **aap_seed_projects_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Create and sync the SCM project. Set to C(false) to skip.
  
  
  

  - **aap_seed_execution_environments_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Create execution environments in AAP. Set to C(false) to skip.  Only applies when I(aap_seed_controller_execution_environments) is non-empty.
  
  
  

  - **aap_seed_templates_create**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Create job templates. Set to C(false) to skip.
  
  
  

  - **aap_seed_controller_organizations**
    - **Required**: False
    - **Type**: list
    - **Default**: []
  
    - **Description**: List of AAP organization definitions. Empty by default; populate to create organizations before other objects. Each entry follows the C(infra.aap_configuration.gateway_organizations) schema.
  
  
  

  - **aap_seed_controller_execution_environments**
    - **Required**: False
    - **Type**: list
    - **Default**: []
  
    - **Description**: List of AAP execution environment definitions. Empty by default; populate to create custom EEs. Each entry follows the C(infra.aap_configuration.controller_execution_environments) schema (name, image, etc.).
  
  
  

  - **aap_seed_controller_inventories**
    - **Required**: False
    - **Type**: list
    - **Default**: none
  
    - **Description**: List of AAP inventory definitions. Override to replace the default Migration Factory inventory.
  
  
  

  - **aap_seed_controller_projects**
    - **Required**: False
    - **Type**: list
    - **Default**: none
  
    - **Description**: List of AAP project definitions. Override to replace the default SCM project.
  
  
  

  - **aap_seed_controller_templates**
    - **Required**: False
    - **Type**: list
    - **Default**: none
  
    - **Description**: List of AAP job template definitions. Override to replace the default migrate template.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|------------|-------------|
| [aap_seed_hostname](defaults/main.yml#L6)   | str | `{{ aap_hostname }}` |    True  |  AAP Hostname |
| [aap_seed_username](defaults/main.yml#L11)   | str | `{{ aap_username ¦ default(omit) }}` |    False  |  AAP Username |
| [aap_seed_password](defaults/main.yml#L16)   | str | `{{ aap_password ¦ default(omit) }}` |    False  |  AAP Password |
| [aap_seed_token](defaults/main.yml#L21)   | str | `{{ aap_token ¦ default(omit) }}` |    False  |  AAP Token |
| [aap_seed_validate_certs](defaults/main.yml#L26)   | str | `{{ aap_validate_certs ¦ default(true) }}` |    False  |  Validate Certificates |
| [aap_seed_secure_logging](defaults/main.yml#L33)   | bool | `True` |    False  |  Secure Logging |
| [aap_seed_org_name](defaults/main.yml#L38)   | str | `Default` |    False  |  Organization Name |
| [aap_seed_project_name](defaults/main.yml#L43)   | str | `OpenShift Virtualization Migration` |    False  |  Project Name |
| [aap_seed_project_scm_url](defaults/main.yml#L48)   | str | `<multiline value: folded_strip>` |    False  |  Project SCM URL |
| [aap_seed_project_scm_branch](defaults/main.yml#L55)   | str | `{{ aap_project_scm_branch ¦ default('v2') }}` |    False  |  Project SCM Branch |
| [aap_seed_project_sync_timeout](defaults/main.yml#L60)   | int | `120` |    False  |  Project Sync Timeout |
| [aap_seed_inventory_name](defaults/main.yml#L65)   | str | `OpenShift Virtualization Migration` |    False  |  Inventory Name |
| [aap_seed_execution_environment](defaults/main.yml#L70)   | str | `{{ aap_execution_environment ¦ default('Default execution environment') }}` |    False  |  Execution Environment |
| [aap_seed_source_credential_type](defaults/main.yml#L75)   | str | `Migration Factory - Source Environment` |    False  |  Source Credential Type |
| [aap_seed_target_credential_type](defaults/main.yml#L80)   | str | `OpenShift or Kubernetes API Bearer Token` |    False  |  Target Credential Type |
| [aap_seed_source_inventory_group](defaults/main.yml#L85)   | str | `vm_sources` |    False  |  Source Inventory Group |
| [aap_seed_target_inventory_group](defaults/main.yml#L90)   | str | `migration_clusters` |    False  |  Target Inventory Group |
| [aap_seed_project_credential](defaults/main.yml#L95)   | str | `{{ aap_project_credential ¦ default('') }}` |    False  |  Project Credential |
| [aap_seed_git_username](defaults/main.yml#L100)   | str | `{{ aap_git_username ¦ default('') }}` |    False  |  Git Username |
| [aap_seed_git_password](defaults/main.yml#L105)   | str | `{{ aap_git_password ¦ default('') }}` |    False  |  Git Password |
| [aap_seed_git_ssh_key](defaults/main.yml#L110)   | str | `{{ aap_git_ssh_key ¦ default('') }}` |    False  |  Git SSH Key |
| [aap_seed_git_ssh_key_unlock](defaults/main.yml#L115)   | str | `{{ aap_git_ssh_key_unlock ¦ default('') }}` |    False  |  Git SSH Key Unlock |
| [aap_seed_migrate_template_name](defaults/main.yml#L120)   | str | `OpenShift Virtualization Migration - Migrate` |    False  |  Migrate Template Name |
| [aap_seed_migrate_playbook](defaults/main.yml#L125)   | str | `playbooks/vmf_migrate.yml` |    False  |  Migrate Playbook |
| [aap_seed_mtv_provider_template_name](defaults/main.yml#L130)   | str | `OpenShift Virtualization Migration - MTV Provider` |    False  |  MTV Provider Template Name |
| [aap_seed_mtv_provider_playbook](defaults/main.yml#L135)   | str | `playbooks/vmf_mtv_provider.yml` |    False  |  MTV Provider Playbook |
| [aap_seed_common_survey_spec](defaults/main.yml#L142)   | dict | `{}` |    False  |  Common Survey Spec |
| [aap_seed_common_survey_spec.**name**](defaults/main.yml#L143)   | str |  |    None  |  None |
| [aap_seed_common_survey_spec.**description**](defaults/main.yml#L144)   | str |  |    None  |  None |
| [aap_seed_common_survey_spec.**spec**](defaults/main.yml#L145)   | list | `[]` |    None  |  None |
| [aap_seed_common_survey_spec.spec.**0**](defaults/main.yml#L146)   | dict | `{}` |    None  |  None |
| [aap_seed_common_survey_spec.spec.0.**question_name**](defaults/main.yml#L146)   | str | `Source Name` |    None  |  None |
| [aap_seed_common_survey_spec.spec.0.**question_description**](defaults/main.yml#L147)   | str | `<multiline value: folded_strip>` |    None  |  None |
| [aap_seed_common_survey_spec.spec.0.**variable**](defaults/main.yml#L151)   | str | `source_name` |    None  |  None |
| [aap_seed_common_survey_spec.spec.0.**type**](defaults/main.yml#L152)   | str | `text` |    None  |  None |
| [aap_seed_common_survey_spec.spec.0.**required**](defaults/main.yml#L153)   | bool | `True` |    None  |  None |
| [aap_seed_common_survey_spec.spec.**1**](defaults/main.yml#L154)   | dict | `{}` |    None  |  None |
| [aap_seed_common_survey_spec.spec.1.**question_name**](defaults/main.yml#L154)   | str | `Target Name` |    None  |  None |
| [aap_seed_common_survey_spec.spec.1.**question_description**](defaults/main.yml#L155)   | str | `<multiline value: folded_strip>` |    None  |  None |
| [aap_seed_common_survey_spec.spec.1.**variable**](defaults/main.yml#L159)   | str | `target_name` |    None  |  None |
| [aap_seed_common_survey_spec.spec.1.**type**](defaults/main.yml#L160)   | str | `text` |    None  |  None |
| [aap_seed_common_survey_spec.spec.1.**required**](defaults/main.yml#L161)   | bool | `True` |    None  |  None |
| [aap_seed_organizations_create](defaults/main.yml#L166)   | bool | `True` |    False  |  Create Organizations |
| [aap_seed_credential_types_create](defaults/main.yml#L171)   | bool | `True` |    False  |  Create Credential Types |
| [aap_seed_credentials_create](defaults/main.yml#L176)   | bool | `True` |    False  |  Create Credentials |
| [aap_seed_inventories_create](defaults/main.yml#L181)   | bool | `True` |    False  |  Create Inventories |
| [aap_seed_hosts_create](defaults/main.yml#L186)   | bool | `True` |    False  |  Create Hosts |
| [aap_seed_projects_create](defaults/main.yml#L191)   | bool | `True` |    False  |  Create Projects |
| [aap_seed_execution_environments_create](defaults/main.yml#L196)   | bool | `True` |    False  |  Create Execution Environments |
| [aap_seed_templates_create](defaults/main.yml#L201)   | bool | `True` |    False  |  Create Templates |
| [aap_seed_controller_organizations](defaults/main.yml#L206)   | list | `[]` |    False  |  Controller Organizations |
| [aap_seed_controller_credential_types](defaults/main.yml#L213)   | list | `[]` |    False  |  Controller Credential Types |
| [aap_seed_controller_credential_types.**0**](defaults/main.yml#L214)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.**name**](defaults/main.yml#L214)   | str | `{{ aap_seed_source_credential_type }}` |    None  |  None |
| [aap_seed_controller_credential_types.0.**organization**](defaults/main.yml#L215)   | str | `{{ aap_seed_org_name }}` |    None  |  None |
| [aap_seed_controller_credential_types.0.**kind**](defaults/main.yml#L216)   | str | `cloud` |    None  |  None |
| [aap_seed_controller_credential_types.0.**inputs**](defaults/main.yml#L217)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.**fields**](defaults/main.yml#L218)   | list | `[]` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.**0**](defaults/main.yml#L219)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.0.**id**](defaults/main.yml#L219)   | str | `host` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.0.**type**](defaults/main.yml#L220)   | str | `string` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.0.**label**](defaults/main.yml#L221)   | str | `Hostname or IP` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.**1**](defaults/main.yml#L222)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.1.**id**](defaults/main.yml#L222)   | str | `username` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.1.**type**](defaults/main.yml#L223)   | str | `string` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.1.**label**](defaults/main.yml#L224)   | str | `Username` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.**2**](defaults/main.yml#L225)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.2.**id**](defaults/main.yml#L225)   | str | `password` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.2.**type**](defaults/main.yml#L226)   | str | `string` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.2.**label**](defaults/main.yml#L227)   | str | `Password` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.2.**secret**](defaults/main.yml#L228)   | bool | `True` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.**3**](defaults/main.yml#L229)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.3.**id**](defaults/main.yml#L229)   | str | `certificate` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.3.**type**](defaults/main.yml#L230)   | str | `string` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.3.**label**](defaults/main.yml#L231)   | str | `SSL/TLS CA Certificate` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.3.**multiline**](defaults/main.yml#L232)   | bool | `True` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.3.**secret**](defaults/main.yml#L233)   | bool | `True` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.**4**](defaults/main.yml#L234)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.4.**id**](defaults/main.yml#L234)   | str | `insecure_skip_tls_verify` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.4.**type**](defaults/main.yml#L235)   | str | `boolean` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.fields.4.**label**](defaults/main.yml#L236)   | str | `Insecure Skip TLS Verify` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.**required**](defaults/main.yml#L237)   | list | `[]` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.required.**0**](defaults/main.yml#L238)   | str | `host` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.required.**1**](defaults/main.yml#L239)   | str | `username` |    None  |  None |
| [aap_seed_controller_credential_types.0.inputs.required.**2**](defaults/main.yml#L240)   | str | `password` |    None  |  None |
| [aap_seed_controller_credential_types.0.**injectors**](defaults/main.yml#L241)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.injectors.**extra_vars**](defaults/main.yml#L242)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_credential_types.0.injectors.extra_vars.**mf_source_host**](defaults/main.yml#L243)   | str | `{% raw %}{  { host }}{% endraw %}` |    None  |  None |
| [aap_seed_controller_credential_types.0.injectors.extra_vars.**mf_source_username**](defaults/main.yml#L244)   | str | `{% raw %}{  { username }}{% endraw %}` |    None  |  None |
| [aap_seed_controller_credential_types.0.injectors.extra_vars.**mf_source_password**](defaults/main.yml#L245)   | str | `{% raw %}{  { password }}{% endraw %}` |    None  |  None |
| [aap_seed_controller_credential_types.0.injectors.extra_vars.**mf_source_certificate**](defaults/main.yml#L246)   | str | `{% raw %}{  { certificate }}{% endraw %}` |    None  |  None |
| [aap_seed_controller_credential_types.0.injectors.extra_vars.**mf_insecure_skip_tls_verify**](defaults/main.yml#L247)   | str | `{% raw %}{  { insecure_skip_tls_verify }}{% endraw %}` |    None  |  None |
| [aap_seed_controller_inventories](defaults/main.yml#L252)   | list | `[]` |    False  |  Controller Inventories |
| [aap_seed_controller_inventories.**0**](defaults/main.yml#L253)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_inventories.0.**name**](defaults/main.yml#L253)   | str | `{{ aap_seed_inventory_name }}` |    None  |  None |
| [aap_seed_controller_inventories.0.**organization**](defaults/main.yml#L254)   | str | `{{ aap_seed_org_name }}` |    None  |  None |
| [aap_seed_controller_projects](defaults/main.yml#L259)   | list | `[]` |    False  |  Controller Projects |
| [aap_seed_controller_projects.**0**](defaults/main.yml#L260)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_projects.0.**name**](defaults/main.yml#L260)   | str | `{{ aap_seed_project_name }}` |    None  |  None |
| [aap_seed_controller_projects.0.**organization**](defaults/main.yml#L261)   | str | `{{ aap_seed_org_name }}` |    None  |  None |
| [aap_seed_controller_projects.0.**scm_type**](defaults/main.yml#L262)   | str | `git` |    None  |  None |
| [aap_seed_controller_projects.0.**scm_url**](defaults/main.yml#L263)   | str | `{{ aap_seed_project_scm_url }}` |    None  |  None |
| [aap_seed_controller_projects.0.**scm_branch**](defaults/main.yml#L264)   | str | `{{ aap_seed_project_scm_branch }}` |    None  |  None |
| [aap_seed_controller_projects.0.**scm_update_on_launch**](defaults/main.yml#L265)   | bool | `True` |    None  |  None |
| [aap_seed_controller_projects.0.**credential**](defaults/main.yml#L266)   | str | `{{ aap_seed_project_credential ¦ default(omit, true) }}` |    None  |  None |
| [aap_seed_controller_execution_environments](defaults/main.yml#L273)   | list | `[]` |    False  |  Controller Execution Environments |
| [aap_seed_controller_templates](defaults/main.yml#L280)   | list | `[]` |    False  |  Controller Templates |
| [aap_seed_controller_templates.**0**](defaults/main.yml#L281)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_templates.0.**name**](defaults/main.yml#L281)   | str | `{{ aap_seed_migrate_template_name }}` |    None  |  None |
| [aap_seed_controller_templates.0.**organization**](defaults/main.yml#L282)   | str | `{{ aap_seed_org_name }}` |    None  |  None |
| [aap_seed_controller_templates.0.**project**](defaults/main.yml#L283)   | str | `{{ aap_seed_project_name }}` |    None  |  None |
| [aap_seed_controller_templates.0.**playbook**](defaults/main.yml#L284)   | str | `{{ aap_seed_migrate_playbook }}` |    None  |  None |
| [aap_seed_controller_templates.0.**inventory**](defaults/main.yml#L285)   | str | `{{ aap_seed_inventory_name }}` |    None  |  None |
| [aap_seed_controller_templates.0.**execution_environment**](defaults/main.yml#L286)   | str | `{{ aap_seed_execution_environment }}` |    None  |  None |
| [aap_seed_controller_templates.0.**ask_credential_on_launch**](defaults/main.yml#L287)   | bool | `True` |    None  |  None |
| [aap_seed_controller_templates.0.**ask_variables_on_launch**](defaults/main.yml#L288)   | bool | `True` |    None  |  None |
| [aap_seed_controller_templates.0.**verbosity**](defaults/main.yml#L289)   | int | `0` |    None  |  None |
| [aap_seed_controller_templates.0.**survey_enabled**](defaults/main.yml#L290)   | bool | `True` |    None  |  None |
| [aap_seed_controller_templates.0.**survey_spec**](defaults/main.yml#L291)   | str | `{{ aap_seed_common_survey_spec }}` |    None  |  None |
| [aap_seed_controller_templates.**1**](defaults/main.yml#L292)   | dict | `{}` |    None  |  None |
| [aap_seed_controller_templates.1.**name**](defaults/main.yml#L292)   | str | `{{ aap_seed_mtv_provider_template_name }}` |    None  |  None |
| [aap_seed_controller_templates.1.**organization**](defaults/main.yml#L293)   | str | `{{ aap_seed_org_name }}` |    None  |  None |
| [aap_seed_controller_templates.1.**project**](defaults/main.yml#L294)   | str | `{{ aap_seed_project_name }}` |    None  |  None |
| [aap_seed_controller_templates.1.**playbook**](defaults/main.yml#L295)   | str | `{{ aap_seed_mtv_provider_playbook }}` |    None  |  None |
| [aap_seed_controller_templates.1.**inventory**](defaults/main.yml#L296)   | str | `{{ aap_seed_inventory_name }}` |    None  |  None |
| [aap_seed_controller_templates.1.**execution_environment**](defaults/main.yml#L297)   | str | `{{ aap_seed_execution_environment }}` |    None  |  None |
| [aap_seed_controller_templates.1.**ask_credential_on_launch**](defaults/main.yml#L298)   | bool | `True` |    None  |  None |
| [aap_seed_controller_templates.1.**ask_variables_on_launch**](defaults/main.yml#L299)   | bool | `True` |    None  |  None |
| [aap_seed_controller_templates.1.**verbosity**](defaults/main.yml#L300)   | int | `0` |    None  |  None |
| [aap_seed_controller_templates.1.**survey_enabled**](defaults/main.yml#L301)   | bool | `True` |    None  |  None |
| [aap_seed_controller_templates.1.**survey_spec**](defaults/main.yml#L302)   | str | `{{ aap_seed_common_survey_spec }}` |    None  |  None |
<details>
<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<table>
<th>Var</th><th>Description</th>
<tr><td><b>aap_seed_hostname</b></td><td>Hostname of the AAP instance. Cascades from aap_hostname inventory variable.</td></tr>
<tr><td><b>aap_seed_username</b></td><td>Username for AAP authentication. Cascades from aap_username inventory variable.</td></tr>
<tr><td><b>aap_seed_password</b></td><td>Password for AAP authentication. Cascades from aap_password inventory variable.</td></tr>
<tr><td><b>aap_seed_token</b></td><td>OAuth token for AAP authentication. Cascades from aap_token inventory variable.</td></tr>
<tr><td><b>aap_seed_validate_certs</b></td><td>Whether to validate TLS certificates for AAP connections.</td></tr>
<tr><td><b>aap_seed_secure_logging</b></td><td>>-</td></tr>
<tr><td><b>aap_seed_org_name</b></td><td>AAP organization name used for all created objects.</td></tr>
<tr><td><b>aap_seed_project_name</b></td><td>Name of the AAP project created for the migration collection.</td></tr>
<tr><td><b>aap_seed_project_scm_url</b></td><td>Git repository URL for the AAP project. Cascades from aap_project_scm_url.</td></tr>
<tr><td><b>aap_seed_project_scm_branch</b></td><td>Git branch for the AAP project. Cascades from aap_project_scm_branch.</td></tr>
<tr><td><b>aap_seed_project_sync_timeout</b></td><td>Timeout in seconds for AAP project sync operations.</td></tr>
<tr><td><b>aap_seed_inventory_name</b></td><td>Name of the AAP inventory created for migration hosts.</td></tr>
<tr><td><b>aap_seed_execution_environment</b></td><td>Execution environment assigned to job templates. Cascades from aap_execution_environment.</td></tr>
<tr><td><b>aap_seed_source_credential_type</b></td><td>Name of the custom credential type created for source hypervisor environments.</td></tr>
<tr><td><b>aap_seed_target_credential_type</b></td><td>Name of the built-in credential type used for OpenShift target clusters.</td></tr>
<tr><td><b>aap_seed_source_inventory_group</b></td><td>AAP inventory group name containing source hypervisor hosts.</td></tr>
<tr><td><b>aap_seed_target_inventory_group</b></td><td>AAP inventory group name containing target OpenShift cluster hosts.</td></tr>
<tr><td><b>aap_seed_project_credential</b></td><td>Name of the Git credential to attach to the AAP project. Leave empty to skip.</td></tr>
<tr><td><b>aap_seed_git_username</b></td><td>Username for Git authentication (HTTPS). Cascades from aap_git_username.</td></tr>
<tr><td><b>aap_seed_git_password</b></td><td>Password or token for Git authentication (HTTPS). Cascades from aap_git_password.</td></tr>
<tr><td><b>aap_seed_git_ssh_key</b></td><td>SSH private key for Git authentication. Cascades from aap_git_ssh_key.</td></tr>
<tr><td><b>aap_seed_git_ssh_key_unlock</b></td><td>Passphrase to unlock the SSH key. Cascades from aap_git_ssh_key_unlock.</td></tr>
<tr><td><b>aap_seed_migrate_template_name</b></td><td>Name of the migration job template created in AAP.</td></tr>
<tr><td><b>aap_seed_migrate_playbook</b></td><td>Playbook path for the migration job template.</td></tr>
<tr><td><b>aap_seed_mtv_provider_template_name</b></td><td>Name of the MTV provider job template created in AAP.</td></tr>
<tr><td><b>aap_seed_mtv_provider_playbook</b></td><td>Playbook path for the MTV provider job template.</td></tr>
<tr><td><b>aap_seed_common_survey_spec</b></td><td>>-</td></tr>
<tr><td><b>aap_seed_organizations_create</b></td><td>Whether to create organization objects in AAP.</td></tr>
<tr><td><b>aap_seed_credential_types_create</b></td><td>Whether to create custom credential type objects in AAP.</td></tr>
<tr><td><b>aap_seed_credentials_create</b></td><td>Whether to create credential objects in AAP.</td></tr>
<tr><td><b>aap_seed_inventories_create</b></td><td>Whether to create inventory objects in AAP.</td></tr>
<tr><td><b>aap_seed_hosts_create</b></td><td>Whether to create host objects in AAP.</td></tr>
<tr><td><b>aap_seed_projects_create</b></td><td>Whether to create project objects in AAP.</td></tr>
<tr><td><b>aap_seed_execution_environments_create</b></td><td>Whether to create execution environment objects in AAP.</td></tr>
<tr><td><b>aap_seed_templates_create</b></td><td>Whether to create job template objects in AAP.</td></tr>
<tr><td><b>aap_seed_controller_organizations</b></td><td>List of AAP organization definitions.</td></tr>
<tr><td><b>aap_seed_controller_credential_types</b></td><td>>-</td></tr>
<tr><td><b>aap_seed_controller_inventories</b></td><td>List of AAP inventory definitions.</td></tr>
<tr><td><b>aap_seed_controller_projects</b></td><td>List of AAP project definitions.</td></tr>
<tr><td><b>aap_seed_controller_execution_environments</b></td><td>>-</td></tr>
<tr><td><b>aap_seed_controller_templates</b></td><td>>-</td></tr>
</table>
<br>
</details>





### Tasks


#### File: tasks/build_credentials.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| build_credentials ¦ Apply credential type toggle | ansible.builtin.set_fact | False |
| build_credentials ¦ Initialize credential list | ansible.builtin.set_fact | True |
| build_credentials ¦ Build source environment credentials | ansible.builtin.set_fact | True |
| build_credentials ¦ Build target cluster credentials | ansible.builtin.set_fact | True |
| build_credentials ¦ Build Git credential for SCM project | ansible.builtin.set_fact | True |
| build_credentials ¦ Disable credentials when toggle is off | ansible.builtin.set_fact | True |

#### File: tasks/build_hosts.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| build_hosts ¦ Initialize host list | ansible.builtin.set_fact | False |
| build_hosts ¦ Build source environment hosts | ansible.builtin.set_fact | False |
| build_hosts ¦ Build target cluster hosts | ansible.builtin.set_fact | False |
| build_hosts ¦ Build inventory groups | ansible.builtin.set_fact | False |

#### File: tasks/build_objects.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| build_objects ¦ Set organizations | ansible.builtin.set_fact | False |
| build_objects ¦ Set inventories | ansible.builtin.set_fact | False |
| build_objects ¦ Set projects | ansible.builtin.set_fact | False |
| build_objects ¦ Set execution environments | ansible.builtin.set_fact | False |
| build_objects ¦ Set job templates | ansible.builtin.set_fact | False |

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| Seed AAP with Migration Factory content | block | False |
| Build simple AAP objects from defaults | ansible.builtin.include_tasks | False |
| Validate inventory host variables | ansible.builtin.include_tasks | False |
| Build credentials from inventory | ansible.builtin.include_tasks | False |
| Build hosts and groups from inventory | ansible.builtin.include_tasks | True |
| Create project and sync from SCM | block | True |
| Sync SCM project | ansible.builtin.include_tasks | False |
| Copy aap_seed_controller_* to controller_* for dispatch | ansible.builtin.set_fact | False |
| Push CaC content to AAP | ansible.builtin.include_role | False |

#### File: tasks/sync_project.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| sync_project ¦ Create or update the project in AAP | ansible.builtin.include_role | False |
| sync_project ¦ Sync project from SCM and wait for completion | ansible.builtin.include_role | False |

#### File: tasks/validate.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| validate ¦ Target hosts must define a non-empty bearer token | ansible.builtin.assert | False |







## Author Information
Red Hat

#### License

GPL-3.0-or-later

#### Minimum Ansible Version

2.16

#### Platforms

No platforms specified.

#### Dependencies

No dependencies specified.
<!-- DOCSIBLE END -->
