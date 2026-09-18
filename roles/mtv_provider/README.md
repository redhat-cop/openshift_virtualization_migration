<!-- STATIC CONTENT START -->
# mtv_provider

Create MTV/Forklift source provider CRs on OpenShift target clusters.

<!-- STATIC CONTENT END -->
<!-- DOCSIBLE START -->
## mtv_provider

```
Role belongs to infra/openshift_virtualization_migration
Namespace - infra
Collection - openshift_virtualization_migration
Version - 1.25.0
Repository - https://github.com/redhat-cop/openshift_virtualization_migration
```

Description: Create MTV/Forklift source provider CRs on OpenShift target clusters. Designed to run from AAP with credential injection.

### Argument Specifications

<details>
<summary><b>🧩 Argument Specifications in `meta/argument_specs`</b></summary>

#### Key: main

* **Description**: ['Creates a Forklift Provider custom resource and its backing Secret on a target OpenShift cluster for a given source environment.', 'Designed to run from AAP with credential injection. The source credential injects VMWARE_* environment variables and C(source_name) as an extra var. OpenShift connection is provided by the AAP target credential which sets K8S_AUTH_* environment variables and C(target_name) as an extra var.', 'For targets with multiple sources, launch the job template once per source-target pair.']
* **Options**:
  * **mtv_provider_api_version**:
    * **Required**: False
    * **Type**: str
    * **Default**: forklift.konveyor.io/v1beta1
    * **Description**: Forklift API version for Provider CRs.
  * **mtv_provider_auto_retrieve_cert**:
    * **Required**: False
    * **Type**: bool
    * **Default**: True
    * **Description**: Whether to automatically retrieve the source TLS certificate when verify_ssl is true and no certificate is provided.
  * **mtv_provider_managed_by_label**:
    * **Required**: False
    * **Type**: str
    * **Default**: ansible-migration-factory
    * **Description**: Value of the app.kubernetes.io/managed-by label applied to Provider and Secret CRs.
  * **mtv_provider_provider_namespace**:
    * **Required**: False
    * **Type**: str
    * **Default**: openshift-mtv
    * **Description**: Namespace where the provider will be created. Resolved from the target host's mtv_namespace variable by default.
  * **mtv_provider_provider_override**:
    * **Required**: False
    * **Type**: dict
    * **Default**: {}
    * **Description**: Override configuration merged into the Provider CR spec. Allows setting additional properties such as settings or other fields that evolve with the Forklift API.
  * **mtv_provider_provider_state**:
    * **Required**: False
    * **Type**: str
    * **Default**: present
    * **Description**: Desired state of the provider. Set to absent to remove a previously created provider and its secret.
    * **Choices**:
      * present
      * absent
  * **mtv_provider_provider_wait**:
    * **Required**: False
    * **Type**: bool
    * **Default**: True
    * **Description**: Whether to wait for the Provider CR to reach Ready status after creation.
  * **mtv_provider_provider_wait_poll**:
    * **Required**: False
    * **Type**: int
    * **Default**: 10
    * **Description**: Seconds between status polls while waiting for Ready.
  * **mtv_provider_provider_wait_timeout**:
    * **Required**: False
    * **Type**: int
    * **Default**: 120
    * **Description**: Seconds to wait for the Provider to become Ready before failing.
  * **mtv_provider_secure_logging**:
    * **Required**: False
    * **Type**: bool
    * **Default**: True
    * **Description**: Whether to enable secure logging for sensitive tasks.
  * **mtv_provider_source_certificate**:
    * **Required**: False
    * **Type**: str
    * **Default**:
    * **Description**: TLS CA certificate for the source hypervisor. Cascades from C(VMWARE_CA_CERT) env var or C(mf_source_certificate).
  * **mtv_provider_source_password**:
    * **Required**: True
    * **Type**: str
    * **Default**: none
    * **Description**: Password for the source hypervisor. Cascades from C(VMWARE_PASSWORD) env var or C(mf_source_password).
  * **mtv_provider_source_username**:
    * **Required**: True
    * **Type**: str
    * **Default**: none
    * **Description**: Username for the source hypervisor. Cascades from C(VMWARE_USER) env var or C(mf_source_username).
  * **mtv_provider_source_verify_ssl**:
    * **Required**: False
    * **Type**: bool
    * **Default**: True
    * **Description**: Whether to verify TLS certificates for the source hypervisor. Cascades from C(VMWARE_VALIDATE_CERTS) env var; falls back to the inverse of C(mf_insecure_skip_tls_verify) if set, or C(true).
  * **source_name**:
    * **Required**: True
    * **Type**: str
    * **Default**: none
    * **Description**: Name of the source environment (must match an AAP inventory host in the vm_sources group).
  * **target_name**:
    * **Required**: True
    * **Type**: str
    * **Default**: none
    * **Description**: Name of the target OpenShift cluster (must match an AAP inventory host in the migration_clusters group).

</details>

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Choices    |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|-------------|
| [`mtv_provider_api_version`](defaults/main.yml#L39)   | str   | `forklift.konveyor.io/v1beta1` |  None  |   False  |  Forklift API Version |
| [`mtv_provider_auto_retrieve_cert`](defaults/main.yml#L51)   | bool   | `True` |  None  |   False  |  Auto Retrieve Certificate |
| [`mtv_provider_managed_by_label`](defaults/main.yml#L131)   | str   | `ansible-migration-factory` |  None  |   False  |  Managed By Label |
| [`mtv_provider_provider_namespace`](defaults/main.yml#L13)   | str   | `<multiline value: folded_strip>` |  None  |   False  |  Provider Namespace |
| [`mtv_provider_provider_override`](defaults/main.yml#L44)   | dict   | `{}` |  None  |   False  |  Provider Override |
| [`mtv_provider_provider_state`](defaults/main.yml#L34)   | str   | `present` |  None  |   False  |  Provider State |
| [`mtv_provider_provider_wait`](defaults/main.yml#L19)   | bool   | `True` |  None  |   False  |  Wait for Provider Ready |
| [`mtv_provider_provider_wait_poll`](defaults/main.yml#L29)   | int   | `10` |  None  |   False  |  Provider Wait Poll Interval |
| [`mtv_provider_provider_wait_timeout`](defaults/main.yml#L24)   | int   | `120` |  None  |   False  |  Provider Wait Timeout |
| [`mtv_provider_secure_logging`](defaults/main.yml#L6)   | str   | `{{ secure_logging ¦ default(true) }}` |  None  |   False  |  Secure Logging |
| [`mtv_provider_source_certificate`](defaults/main.yml#L96)   | str   | `<multiline value: folded_strip>` |  None  |   False  |  Source Certificate |
| [`mtv_provider_source_host`](defaults/main.yml#L66)   | str   | `<multiline value: folded_strip>` |  None  |   True  |  Source Host |
| [`mtv_provider_source_password`](defaults/main.yml#L85)   | str   | `<multiline value: folded_strip>` |  None  |   True  |  Source Password |
| [`mtv_provider_source_sdk_endpoint`](defaults/main.yml#L120)   | str   | `<multiline value: folded_strip>` |  None  |   False  |  Source SDK Endpoint |
| [`mtv_provider_source_type`](defaults/main.yml#L58)   | str   | `<multiline value: folded_strip>` |  None  |   False  |  Source Type |
| [`mtv_provider_source_username`](defaults/main.yml#L74)   | str   | `<multiline value: folded_strip>` |  None  |   True  |  Source Username |
| [`mtv_provider_source_vddk`](defaults/main.yml#L126)   | str   | `{{ hostvars[source_name]['vddk'] ¦ default({}) }}` |  None  |   False  |  Source VDDK Configuration |
| [`mtv_provider_source_verify_ssl`](defaults/main.yml#L108)   | str   | `<multiline value: folded_strip>` |  None  |   False  |  Source Verify SSL |

<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<b>`mtv_provider_api_version`:</b> Forklift API version for Provider CRs.
<br>
<b>`mtv_provider_auto_retrieve_cert`:</b> >-
<br>
<b>`mtv_provider_managed_by_label`:</b> Value of the app.kubernetes.io/managed-by label applied to CRs.
<br>
<b>`mtv_provider_provider_namespace`:</b> >-
<br>
<b>`mtv_provider_provider_override`:</b> Override configuration merged into the Provider CR spec.
<br>
<b>`mtv_provider_provider_state`:</b> Desired state of the provider — present or absent.
<br>
<b>`mtv_provider_provider_wait`:</b> Whether to wait for the Provider CR to reach Ready status after creation.
<br>
<b>`mtv_provider_provider_wait_poll`:</b> Seconds between status polls while waiting for Ready.
<br>
<b>`mtv_provider_provider_wait_timeout`:</b> Seconds to wait for the Provider to become Ready before failing.
<br>
<b>`mtv_provider_secure_logging`:</b> Whether to enable secure logging for sensitive tasks.
<br>
<b>`mtv_provider_source_certificate`:</b> >-
<br>
<b>`mtv_provider_source_host`:</b> >-
<br>
<b>`mtv_provider_source_password`:</b> >-
<br>
<b>`mtv_provider_source_sdk_endpoint`:</b> SDK endpoint path appended to the source host URL for VMware providers.
<br>
<b>`mtv_provider_source_type`:</b> >-
<br>
<b>`mtv_provider_source_username`:</b> >-
<br>
<b>`mtv_provider_source_vddk`:</b> VDDK configuration dictionary from the source host vars.
<br>
<b>`mtv_provider_source_verify_ssl`:</b> >-
<br>
<br>

### Tasks

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Configure MTV provider for source-target pair | `block` | False |
| Validate inputs and resolve provider variables | `ansible.builtin.include_tasks` | False |
| Create provider secret and CR on target cluster | `ansible.builtin.include_tasks` | False |

#### File: tasks/create_provider.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| create_provider ¦ Ensure provider secret exists | `redhat.openshift.k8s` | False |
| create_provider ¦ Ensure provider CR exists | `redhat.openshift.k8s` | False |
| create_provider ¦ Wait for provider to become Ready | `kubernetes.core.k8s_info` | True |
| create_provider ¦ Provider created successfully | `ansible.builtin.debug` | False |

#### File: tasks/rescue_provider.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| rescue_provider ¦ Fetch provider status | `kubernetes.core.k8s_info` | False |
| rescue_provider ¦ Warn if cluster query failed | `ansible.builtin.debug` | True |
| rescue_provider ¦ Extract error details | `ansible.builtin.set_fact` | True |
| rescue_provider ¦ Display provider error status | `ansible.builtin.debug` | False |
| rescue_provider ¦ Fail with summary | `ansible.builtin.fail` | False |

#### File: tasks/validate.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| validate ¦ Assert required variables are defined | `ansible.builtin.assert` | False |
| validate ¦ Assert target exists in AAP inventory | `ansible.builtin.assert` | False |
| validate ¦ Assert source exists in AAP inventory | `ansible.builtin.assert` | False |
| validate ¦ Assert source is mapped to this target | `ansible.builtin.assert` | False |
| validate ¦ Assert source host variable is defined | `ansible.builtin.assert` | False |
| validate ¦ Assert source credentials are available | `ansible.builtin.assert` | False |
| validate ¦ Assert provider_override does not contain managed keys | `ansible.builtin.assert` | True |
| validate ¦ Assert source type is supported | `ansible.builtin.assert` | False |
| validate ¦ Check Forklift CRD exists on target cluster | `kubernetes.core.k8s_info` | False |
| validate ¦ Assert MTV operator is installed | `ansible.builtin.assert` | False |
| validate ¦ Resolve provider variables | `ansible.builtin.set_fact` | False |
| validate ¦ Retrieve source TLS certificate | `block` | True |
| validate ¦ Retrieve remote certificate from source | `community.crypto.get_certificate` | False |
| validate ¦ Store retrieved certificate | `ansible.builtin.set_fact` | False |
| validate ¦ Resolve effective certificate | `ansible.builtin.set_fact` | False |

## Task Flow Graphs

### Graph for create_provider.yml

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

  Start-->|Task| create_provider___Ensure_provider_secret_exists0[create provider   ensure provider secret exists]:::task
  create_provider___Ensure_provider_secret_exists0-->|Task| create_provider___Ensure_provider_CR_exists1[create provider   ensure provider cr exists]:::task
  create_provider___Ensure_provider_CR_exists1-->|Task| create_provider___Wait_for_provider_to_become_Ready2[create provider   wait for provider to become<br>ready<br>When: **mtv provider provider wait   bool**]:::task
  create_provider___Wait_for_provider_to_become_Ready2-->|Task| create_provider___Provider_created_successfully3[create provider   provider created successfully]:::task
  create_provider___Provider_created_successfully3-->End
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

  Start-->|Block Start| Configure_MTV_provider_for_source_target_pair0_block_start_0[[configure mtv provider for source target pair]]:::block
  Configure_MTV_provider_for_source_target_pair0_block_start_0-->|Include task| Validate_inputs_and_resolve_provider_variables_validate_yml_0[validate inputs and resolve provider variables<br>include_task: validate yml]:::includeTasks
  Validate_inputs_and_resolve_provider_variables_validate_yml_0-->|Include task| Create_provider_secret_and_CR_on_target_cluster_create_provider_yml_1[create provider secret and cr on target cluster<br>include_task: create provider yml]:::includeTasks
  Create_provider_secret_and_CR_on_target_cluster_create_provider_yml_1-.->|End of Block| Configure_MTV_provider_for_source_target_pair0_block_start_0
  Create_provider_secret_and_CR_on_target_cluster_create_provider_yml_1-->|Rescue Start| Configure_MTV_provider_for_source_target_pair0_rescue_start_0[configure mtv provider for source target pair]:::rescue
  Configure_MTV_provider_for_source_target_pair0_rescue_start_0-->|Include task| Gather_provider_error_details_and_fail_rescue_provider_yml_0[gather provider error details and fail<br>include_task: rescue provider yml]:::includeTasks
  Gather_provider_error_details_and_fail_rescue_provider_yml_0-.->|End of Rescue Block| Configure_MTV_provider_for_source_target_pair0_block_start_0
  Gather_provider_error_details_and_fail_rescue_provider_yml_0-->End
```

### Graph for rescue_provider.yml

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

  Start-->|Task| rescue_provider___Fetch_provider_status0[rescue provider   fetch provider status]:::task
  rescue_provider___Fetch_provider_status0-->|Task| rescue_provider___Warn_if_cluster_query_failed1[rescue provider   warn if cluster query failed<br>When: **mtv provider failed result is failed**]:::task
  rescue_provider___Warn_if_cluster_query_failed1-->|Task| rescue_provider___Extract_error_details2[rescue provider   extract error details<br>When: **mtv provider failed result resources   default   <br>   length   0**]:::task
  rescue_provider___Extract_error_details2-->|Task| rescue_provider___Display_provider_error_status3[rescue provider   display provider error status]:::task
  rescue_provider___Display_provider_error_status3-->|Task| rescue_provider___Fail_with_summary4[rescue provider   fail with summary]:::task
  rescue_provider___Fail_with_summary4-->End
```

### Graph for validate.yml

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

  Start-->|Task| validate___Assert_required_variables_are_defined0[validate   assert required variables are defined]:::task
  validate___Assert_required_variables_are_defined0-->|Task| validate___Assert_target_exists_in_AAP_inventory1[validate   assert target exists in aap inventory]:::task
  validate___Assert_target_exists_in_AAP_inventory1-->|Task| validate___Assert_source_exists_in_AAP_inventory2[validate   assert source exists in aap inventory]:::task
  validate___Assert_source_exists_in_AAP_inventory2-->|Task| validate___Assert_source_is_mapped_to_this_target3[validate   assert source is mapped to this target]:::task
  validate___Assert_source_is_mapped_to_this_target3-->|Task| validate___Assert_source_host_variable_is_defined4[validate   assert source host variable is defined]:::task
  validate___Assert_source_host_variable_is_defined4-->|Task| validate___Assert_source_credentials_are_available5[validate   assert source credentials are available]:::task
  validate___Assert_source_credentials_are_available5-->|Task| validate___Assert_provider_override_does_not_contain_managed_keys6[validate   assert provider override does not<br>contain managed keys<br>When: **mtv provider provider override   length   0**]:::task
  validate___Assert_provider_override_does_not_contain_managed_keys6-->|Task| validate___Assert_source_type_is_supported7[validate   assert source type is supported]:::task
  validate___Assert_source_type_is_supported7-->|Task| validate___Check_Forklift_CRD_exists_on_target_cluster8[validate   check forklift crd exists on target<br>cluster]:::task
  validate___Check_Forklift_CRD_exists_on_target_cluster8-->|Task| validate___Assert_MTV_operator_is_installed9[validate   assert mtv operator is installed]:::task
  validate___Assert_MTV_operator_is_installed9-->|Task| validate___Resolve_provider_variables10[validate   resolve provider variables]:::task
  validate___Resolve_provider_variables10-->|Block Start| validate___Retrieve_source_TLS_certificate11_block_start_0[[validate   retrieve source tls certificate<br>When: **mtv provider auto retrieve cert   bool and mtv<br>provider source verify ssl   bool and mtv provider<br>source certificate   trim   length    0**]]:::block
  validate___Retrieve_source_TLS_certificate11_block_start_0-->|Task| validate___Retrieve_remote_certificate_from_source0[validate   retrieve remote certificate from source]:::task
  validate___Retrieve_remote_certificate_from_source0-->|Task| validate___Store_retrieved_certificate1[validate   store retrieved certificate]:::task
  validate___Store_retrieved_certificate1-.->|End of Block| validate___Retrieve_source_TLS_certificate11_block_start_0
  validate___Store_retrieved_certificate1-->|Task| validate___Resolve_effective_certificate12[validate   resolve effective certificate]:::task
  validate___Resolve_effective_certificate12-->End
```

## Author Information

Red Hat

## License

GPL-3.0-only

## Minimum Ansible Version

2.16

## Platforms

No platforms specified.

<!-- DOCSIBLE END -->