<!-- DOCSIBLE START -->

# 📃 Role overview

## mtv_provider



Description: Create MTV/Forklift source provider CRs on OpenShift target clusters. Designed to run from AAP with credential injection.

| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 2026/09/02 |




<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 
- Creates a Forklift Provider custom resource and its backing Secret on a target OpenShift cluster for a given source environment.
- Designed to run from AAP with credential injection. The source credential injects mf_source_username, mf_source_password, and mf_source_certificate as extra vars. OpenShift connection is provided by the AAP OpenShift credential which sets K8S_AUTH_* environment variables.
- For targets with multiple sources, launch the job template once per source-target pair.


**Options**:


  - **source_name**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Name of the source environment (must match an AAP inventory host in the vm_sources group).
  
  
  

  - **target_name**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: Name of the target OpenShift cluster (must match an AAP inventory host in the migration_clusters group).
  
  
  

  - **mtv_provider_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to enable secure logging for sensitive tasks.
  
  
  

  - **mtv_provider_provider_namespace**
    - **Required**: False
    - **Type**: str
    - **Default**: openshift-mtv
  
    - **Description**: Namespace where the provider will be created. Resolved from the target host's mtv_namespace variable by default.
  
  
  

  - **mtv_provider_provider_wait**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to wait for the Provider CR to reach Ready status after creation.
  
  
  

  - **mtv_provider_provider_wait_timeout**
    - **Required**: False
    - **Type**: int
    - **Default**: 120
  
    - **Description**: Seconds to wait for the Provider to become Ready before failing.
  
  
  

  - **mtv_provider_provider_wait_poll**
    - **Required**: False
    - **Type**: int
    - **Default**: 10
  
    - **Description**: Seconds between status polls while waiting for Ready.
  
  
  

  - **mtv_provider_provider_state**
    - **Required**: False
    - **Type**: str
    - **Default**: present
  
    - **Description**: Desired state of the provider. Set to absent to remove a previously created provider and its secret.
  
      - **Choices**:
    
          - present
    
          - absent
    
  
  
  

  - **mtv_provider_api_version**
    - **Required**: False
    - **Type**: str
    - **Default**: forklift.konveyor.io/v1beta1
  
    - **Description**: Forklift API version for Provider CRs.
  
  
  

  - **mtv_provider_provider_override**
    - **Required**: False
    - **Type**: dict
    - **Default**: {}
  
    - **Description**: Override configuration merged into the Provider CR spec. Allows setting additional properties such as settings or other fields that evolve with the Forklift API.
  
  
  

  - **mtv_provider_auto_retrieve_cert**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to automatically retrieve the source TLS certificate when insecureSkipTlsVerify is false and no certificate is provided.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|------------|-------------|
| [mtv_provider_secure_logging](defaults/main.yml#L6)   | str | `{{ secure_logging ¦ default(true) }}` |    False  |  Secure Logging |
| [mtv_provider_provider_namespace](defaults/main.yml#L13)   | str | `<multiline value: folded_strip>` |    False  |  Provider Namespace |
| [mtv_provider_provider_wait](defaults/main.yml#L19)   | bool | `True` |    False  |  Wait for Provider Ready |
| [mtv_provider_provider_wait_timeout](defaults/main.yml#L24)   | int | `120` |    False  |  Provider Wait Timeout |
| [mtv_provider_provider_wait_poll](defaults/main.yml#L29)   | int | `10` |    False  |  Provider Wait Poll Interval |
| [mtv_provider_provider_state](defaults/main.yml#L34)   | str | `present` |    False  |  Provider State |
| [mtv_provider_api_version](defaults/main.yml#L39)   | str | `forklift.konveyor.io/v1beta1` |    False  |  Forklift API Version |
| [mtv_provider_provider_override](defaults/main.yml#L44)   | dict | `{}` |    False  |  Provider Override |
| [mtv_provider_auto_retrieve_cert](defaults/main.yml#L51)   | bool | `True` |    False  |  Auto Retrieve Certificate |
| [mtv_provider_source_type](defaults/main.yml#L58)   | str | `<multiline value: folded_strip>` |    False  |  Source Type |
| [mtv_provider_source_host](defaults/main.yml#L66)   | str | `<multiline value: folded_strip>` |    True  |  Source Host |
| [mtv_provider_source_sdk_endpoint](defaults/main.yml#L72)   | str | `<multiline value: folded_strip>` |    False  |  Source SDK Endpoint |
| [mtv_provider_source_vddk](defaults/main.yml#L78)   | str | `{{ hostvars[source_name]['vddk'] ¦ default({}) }}` |    False  |  Source VDDK Configuration |
| [mtv_provider_managed_by_label](defaults/main.yml#L83)   | str | `ansible-migration-factory` |    False  |  Managed By Label |
<details>
<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<table>
<th>Var</th><th>Description</th>
<tr><td><b>mtv_provider_secure_logging</b></td><td>Whether to enable secure logging for sensitive tasks.</td></tr>
<tr><td><b>mtv_provider_provider_namespace</b></td><td>>-</td></tr>
<tr><td><b>mtv_provider_provider_wait</b></td><td>Whether to wait for the Provider CR to reach Ready status after creation.</td></tr>
<tr><td><b>mtv_provider_provider_wait_timeout</b></td><td>Seconds to wait for the Provider to become Ready before failing.</td></tr>
<tr><td><b>mtv_provider_provider_wait_poll</b></td><td>Seconds between status polls while waiting for Ready.</td></tr>
<tr><td><b>mtv_provider_provider_state</b></td><td>Desired state of the provider — present or absent.</td></tr>
<tr><td><b>mtv_provider_api_version</b></td><td>Forklift API version for Provider CRs.</td></tr>
<tr><td><b>mtv_provider_provider_override</b></td><td>Override configuration merged into the Provider CR spec.</td></tr>
<tr><td><b>mtv_provider_auto_retrieve_cert</b></td><td>>-</td></tr>
<tr><td><b>mtv_provider_source_type</b></td><td>>-</td></tr>
<tr><td><b>mtv_provider_source_host</b></td><td>>-</td></tr>
<tr><td><b>mtv_provider_source_sdk_endpoint</b></td><td>SDK endpoint path appended to the source host URL for VMware providers.</td></tr>
<tr><td><b>mtv_provider_source_vddk</b></td><td>VDDK configuration dictionary from the source host vars.</td></tr>
<tr><td><b>mtv_provider_managed_by_label</b></td><td>Value of the app.kubernetes.io/managed-by label applied to CRs.</td></tr>
</table>
<br>
</details>





### Tasks


#### File: tasks/create_provider.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| create_provider ¦ Ensure provider secret exists | redhat.openshift.k8s | False |
| create_provider ¦ Ensure provider CR exists | redhat.openshift.k8s | False |
| create_provider ¦ Wait for provider to become Ready | kubernetes.core.k8s_info | True |
| create_provider ¦ Provider created successfully | ansible.builtin.debug | False |

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| Configure MTV provider for source-target pair | block | False |
| Validate inputs and resolve provider variables | ansible.builtin.include_tasks | False |
| Create provider secret and CR on target cluster | ansible.builtin.include_tasks | False |

#### File: tasks/rescue_provider.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| rescue_provider ¦ Fetch provider status | kubernetes.core.k8s_info | False |
| rescue_provider ¦ Warn if cluster query failed | ansible.builtin.debug | True |
| rescue_provider ¦ Extract error details | ansible.builtin.set_fact | True |
| rescue_provider ¦ Display provider error status | ansible.builtin.debug | False |
| rescue_provider ¦ Fail with summary | ansible.builtin.fail | False |

#### File: tasks/validate.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| validate ¦ Assert required survey variables are defined | ansible.builtin.assert | False |
| validate ¦ Assert target exists in AAP inventory | ansible.builtin.assert | False |
| validate ¦ Assert source exists in AAP inventory | ansible.builtin.assert | False |
| validate ¦ Assert source is mapped to this target | ansible.builtin.assert | False |
| validate ¦ Assert source host variable is defined | ansible.builtin.assert | False |
| validate ¦ Assert source credentials are injected | ansible.builtin.assert | False |
| validate ¦ Assert provider_override does not contain managed keys | ansible.builtin.assert | True |
| validate ¦ Assert source type is supported | ansible.builtin.assert | False |
| validate ¦ Check Forklift CRD exists on target cluster | kubernetes.core.k8s_info | False |
| validate ¦ Assert MTV operator is installed | ansible.builtin.assert | False |
| validate ¦ Resolve provider variables | ansible.builtin.set_fact | False |
| validate ¦ Retrieve source TLS certificate | block | True |
| validate ¦ Retrieve remote certificate from source | community.crypto.get_certificate | False |
| validate ¦ Store retrieved certificate | ansible.builtin.set_fact | False |
| validate ¦ Resolve effective certificate | ansible.builtin.set_fact | False |







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
