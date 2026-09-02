<!-- DOCSIBLE START -->

# 📃 Role overview

## utility_openshift_target_credential



Description: A utility role to manage OpenShift target cluster credentials for migration

| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 2026/09/02 |




<details>
<summary><b>🧩 Argument Specifications in meta/argument_specs</b></summary>

#### Key: main

**Description**: 


**Options**:


  - **utility_openshift_target_credential_openshift_host**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: OpenShift host.
  
  
  

  - **utility_openshift_target_credential_openshift_api_key**
    - **Required**: True
    - **Type**: str
    - **Default**: none
  
    - **Description**: OpenShift API key.
  
  
  

  - **utility_openshift_target_credential_openshift_ca_cert_path**
    - **Required**: False
    - **Type**: str
    - **Default**: none
  
    - **Description**: Path to the OpenShift CA Certificate.
  
  
  

  - **utility_openshift_target_credential_openshift_verify_ssl**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to verify SSL certificates.
  
  
  

  - **utility_openshift_target_credential_resource_name**
    - **Required**: False
    - **Type**: str
    - **Default**: migration-factory-aap-credential
  
    - **Description**: Name applied to the OpenShift target credential resource.
  
  
  

  - **utility_openshift_target_credential_resource_namespace**
    - **Required**: False
    - **Type**: str
    - **Default**: openshift-config
  
    - **Description**: Namespace applied to the OpenShift target credential resource.
  
  
  

  - **utility_openshift_target_credential_cluster_role**
    - **Required**: False
    - **Type**: str
    - **Default**: cluster-admin
  
    - **Description**: Cluster Role applied to the generated OpenShift Service Account.
  
  
  

  - **utility_openshift_target_credential_managed_by_label**
    - **Required**: False
    - **Type**: str
    - **Default**: ansible
  
    - **Description**: Value of the app.kubernetes.io/managed-by label applied to resources.
  
  
  

  - **utility_openshift_target_credential_secure_logging**
    - **Required**: False
    - **Type**: bool
    - **Default**: True
  
    - **Description**: Whether to enable secure logging.
  
  
  

  - **utility_openshift_target_credential_display_credential**
    - **Required**: False
    - **Type**: bool
    - **Default**: False
  
    - **Description**: Whether to display the credential.
  
  
  



</details>




### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|------------|-------------|
| [utility_openshift_target_credential_openshift_host](defaults/main.yml#L7)   | str | `{{ openshift_host }}` |    True  |  OpenShift Host |
| [utility_openshift_target_credential_openshift_api_key](defaults/main.yml#L12)   | str | `<multiline value: folded_strip>` |    True  |  OpenShift API Key |
| [utility_openshift_target_credential_openshift_ca_cert_path](defaults/main.yml#L23)   | str | `{{ openshift_ca_cert_path ¦ default(omit) }}` |    False  |  OpenShift CA Certificate Path |
| [utility_openshift_target_credential_openshift_verify_ssl](defaults/main.yml#L28)   | str | `{{ openshift_verify_ssl ¦ default(true) }}` |    False  |  OpenShift Verify SSL |
| [utility_openshift_target_credential_resource_name](defaults/main.yml#L33)   | str | `migration-factory-aap-credential` |    False  |  Name applied to the OpenShift target credential resource |
| [utility_openshift_target_credential_resource_namespace](defaults/main.yml#L38)   | str | `openshift-config` |    False  |  Namespace applied to the OpenShift target credential resource |
| [utility_openshift_target_credential_cluster_role](defaults/main.yml#L43)   | str | `cluster-admin` |    False  |  Cluster Role applied to the generated OpenShift Service Account |
| [utility_openshift_target_credential_managed_by_label](defaults/main.yml#L48)   | str | `ansible-migration-factory` |    False  |  Managed By Label |
| [utility_openshift_target_credential_secure_logging](defaults/main.yml#L53)   | str | `{{ secure_logging ¦ default(true) }}` |    False  |  Secure Logging |
| [utility_openshift_target_credential_display_credential](defaults/main.yml#L58)   | bool | `False` |    False  |  Display Credential |
<details>
<summary><b>🖇️ Full descriptions for vars in defaults/main.yml</b></summary>
<br>
<table>
<th>Var</th><th>Description</th>
<tr><td><b>utility_openshift_target_credential_openshift_host</b></td><td>OpenShift host.</td></tr>
<tr><td><b>utility_openshift_target_credential_openshift_api_key</b></td><td>OpenShift API key.</td></tr>
<tr><td><b>utility_openshift_target_credential_openshift_ca_cert_path</b></td><td>Path to the OpenShift CA Certificate.</td></tr>
<tr><td><b>utility_openshift_target_credential_openshift_verify_ssl</b></td><td>Whether to verify SSL certificates.</td></tr>
<tr><td><b>utility_openshift_target_credential_resource_name</b></td><td>Name applied to the OpenShift target credential resource.</td></tr>
<tr><td><b>utility_openshift_target_credential_resource_namespace</b></td><td>Namespace applied to the OpenShift target credential resource.</td></tr>
<tr><td><b>utility_openshift_target_credential_cluster_role</b></td><td>Cluster Role applied to the generated OpenShift Service Account.</td></tr>
<tr><td><b>utility_openshift_target_credential_managed_by_label</b></td><td>Value of the app.kubernetes.io/managed-by label applied to resources.</td></tr>
<tr><td><b>utility_openshift_target_credential_secure_logging</b></td><td>Whether to enable secure logging.</td></tr>
<tr><td><b>utility_openshift_target_credential_display_credential</b></td><td>Whether to display the credential.</td></tr>
</table>
<br>
</details>





### Tasks


#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | -------------- |
| Create OpenShift target credential resources | redhat.openshift.k8s | False |
| Display credential | block | True |
| Wait for credential token to be populated | kubernetes.core.k8s_info | False |
| Display credential token which can be used to authenticate to the target OpenShift cluster | ansible.builtin.debug | False |







## Author Information
Unknown Author

#### License

GPL-3.0-only

#### Minimum Ansible Version

2.15.0

#### Platforms

No platforms specified.

#### Dependencies

No dependencies specified.
<!-- DOCSIBLE END -->
