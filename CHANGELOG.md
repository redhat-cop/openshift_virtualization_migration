# CHANGELOG

## v1.24.1 (2026-04-15)

### Chores

- Revise min supported Ansible version
  ([#28](https://github.com/redhat-cop/openshift_virtualization_migration/pull/28),
  [`37de237`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/37de23764a7ab74c5850ff2b9acb6524a6e841ab))

### Documentation

- Add table of contents
  ([#30](https://github.com/redhat-cop/openshift_virtualization_migration/pull/30),
  [`f04a1c6`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/f04a1c6ea820bfb84e0ec13727bd660be59dab6d))


## v1.24.0 (2026-04-14)

### Bug Fixes

- Address review feedback on credential management docs
  ([#23](https://github.com/redhat-cop/openshift_virtualization_migration/pull/23),
  [`97d61c1`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/97d61c10aa935fbf6dab341338a88993cb61c5d2))

- Address review feedback on credential practices doc
  ([#24](https://github.com/redhat-cop/openshift_virtualization_migration/pull/24),
  [`02085bf`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/02085bf5a9737ee003e4a8adcbb90b8ff8ad8188))

- Address review feedback on disconnected environment guide
  ([#20](https://github.com/redhat-cop/openshift_virtualization_migration/pull/20),
  [`3679327`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/3679327ee22a42382d0ccb159c5cb478a2f7d975))

- Remove remaining Migration Factory references
  ([#20](https://github.com/redhat-cop/openshift_virtualization_migration/pull/20),
  [`3679327`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/3679327ee22a42382d0ccb159c5cb478a2f7d975))

- **operator-management**: Use empty targetNamespaces for GitOps operator
  ([#21](https://github.com/redhat-cop/openshift_virtualization_migration/pull/21),
  [`efec86a`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/efec86a7b3b3356e7c622ccd92688ab798522adb))

### Documentation

- Add disconnected environment guide
  ([#20](https://github.com/redhat-cop/openshift_virtualization_migration/pull/20),
  [`3679327`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/3679327ee22a42382d0ccb159c5cb478a2f7d975))

- Add disconnected environment guide for Migration Factory
  ([#20](https://github.com/redhat-cop/openshift_virtualization_migration/pull/20),
  [`3679327`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/3679327ee22a42382d0ccb159c5cb478a2f7d975))

- Add secure credential practices guide
  ([#24](https://github.com/redhat-cop/openshift_virtualization_migration/pull/24),
  [`02085bf`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/02085bf5a9737ee003e4a8adcbb90b8ff8ad8188))

### Features

- Add secure credential management with Ansible Vault
  ([#23](https://github.com/redhat-cop/openshift_virtualization_migration/pull/23),
  [`97d61c1`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/97d61c10aa935fbf6dab341338a88993cb61c5d2))

- Add secure credential management with Vault
  ([#23](https://github.com/redhat-cop/openshift_virtualization_migration/pull/23),
  [`97d61c1`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/97d61c10aa935fbf6dab341338a88993cb61c5d2))

- **operator-management**: Add OpenShift GitOps operator
  ([#21](https://github.com/redhat-cop/openshift_virtualization_migration/pull/21),
  [`efec86a`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/efec86a7b3b3356e7c622ccd92688ab798522adb))

- **operator-management**: Add Red Hat OpenShift GitOps operator
  ([#21](https://github.com/redhat-cop/openshift_virtualization_migration/pull/21),
  [`efec86a`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/efec86a7b3b3356e7c622ccd92688ab798522adb))


## v1.23.0 (2026-04-10)

### Features

- Enhance properties for how AAP is subscribed
  ([#14](https://github.com/redhat-cop/openshift_virtualization_migration/pull/14),
  [`6ee3989`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/6ee3989c5d0ed93c2d1cf89edefd11170467dad2))


## v1.22.0 (2026-04-02)

### Bug Fixes

- Allow skipping VMware certificate validation [skip ci]
  ([#11](https://github.com/redhat-cop/openshift_virtualization_migration/pull/11),
  [`e9d7a01`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/e9d7a01ff0c6a2ede32906f6665275b17183569c))

- Correct bugs due to wrong variable names [skip ci]
  ([`dfb3e0b`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/dfb3e0b418dec037dfadd8fcdfc541c6a083c198))

- Correct jinja2 template to omit cacert
  ([#11](https://github.com/redhat-cop/openshift_virtualization_migration/pull/11),
  [`e9d7a01`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/e9d7a01ff0c6a2ede32906f6665275b17183569c))

- MFG-439 Do not retrieve remote VMware provider certificate when insecureSkipVerify=true
  ([#11](https://github.com/redhat-cop/openshift_virtualization_migration/pull/11),
  [`e9d7a01`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/e9d7a01ff0c6a2ede32906f6665275b17183569c))

- Resolve lint errors
  ([`68daa03`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/68daa038eb13efc7b4f0e57556404bc51070206f))

- Resolve markdown lint errors
  ([`95b340e`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/95b340eec640eaffce8f4dee121df72a25df6613))

- Set collection authors
  ([`cd40aec`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/cd40aece64c1df23b0690992d7a9bc6ebf664448))

### Chores

- Add PR template
  ([`ad283fd`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/ad283fd36dbae527fb93dbe3dc0809de0f8bff69))

- Minor typos
  ([`dfb3e0b`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/dfb3e0b418dec037dfadd8fcdfc541c6a083c198))

- Resolve changelogs issues [skip ci]
  ([`c4900b2`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/c4900b2dad0e64007cb17a02186ea823286c22f5))

- Revise build scripts
  ([`75de825`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/75de8257a17c5f31df023ee2891951cd73a06efe))

- Revise configs, pre-commit hooks
  ([`c7e00dd`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/c7e00dd0a9fe28fe9ed04345e3a8d71bd28677b2))

- Update CODEOWNERS (#12) [skip ci]
  ([`41d35c0`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/41d35c010e2b5bbba4ff1eb55176522a5cb0c0a6))

### Documentation

- Add badges to README
  ([`5c5aa00`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/5c5aa00092ca5726a4bb8ceb4f897e727e11e586))

### Features

- Added retry attach subscription
  ([#13](https://github.com/redhat-cop/openshift_virtualization_migration/pull/13),
  [`e6fc0cc`](https://github.com/redhat-cop/openshift_virtualization_migration/commit/e6fc0cc9947c19922b69aebe2a9863fe05610a42))


## v1.21.1 (2025-07-30)

### Bug Fixes

- Corrected issues in network_mgmt role
- Corrected issues in network_mgmt role

## v1.21.0 (2025-07-14)

### Features

- Added ansible.utils dependency
- Added ansible.utils dependency

## v1.20.5 (2025-07-10)

### Bug Fixes

- Corrected variable when creating VDDK secret
- Corrected variable when creating VDDK secret


## v1.20.4 (2025-07-03)

### Bug Fixes

- Corrected aap_utilities enhancements
- Corrected aap_utilities enhancements
- Galaxy dependency management
- Galaxy dependency management

## v1.20.3 (2025-07-01)

### Bug Fixes

- Readme updated with updated dependencies
- Readme updated with updated dependencies

## v1.20.2 (2025-07-01)

### Bug Fixes

- Remove unused collections from requirements-dev and galaxy.yml
- Remove unused collections from requirements-dev and galaxy.yml

## v1.20.1 (2025-06-27)

### Documentation

- Remove day 2 from README
- Remove day 2 from README

## v1.20.0 (2025-06-27)

### Documentation

- Removal of internal docs from collection
- Removal of internal docs from collection

### Features

- Added support for customizing seed content
- Added support for customizing seed content
- Mfg-433 - add deprecation comment to roles and playbooks migrated to openshift_virtualization_ops
  collection
- Mfg-433 - add deprecation comment to roles and playbooks migrated to openshift_virtualization_ops
  collection

## v1.19.1 (2025-06-19)

### Bug Fixes

- Pipeline ci publish job depends on semantic versioning jobs
- Pipeline ci publish job depends on semantic versioning jobs

## v1.19.0 (2025-06-18)

### Bug Fixes

- Added a delay/retries to applying license file
- Added a delay/retries to applying license file
- Mfg-220 include antsibull-changelog into build script
- Mfg-220 include antsibull-changelog into build script
- Remove limitation on usage from README
- Remove limitation on usage from README

### Docs

- Mfg-338: Ansible roles variables for the hub
- Mfg-338: Ansible roles variables for the hub

### Features

- Added MAC Address Role
- Added MAC Address Role

## v1.18.2 (2025-06-07)

### Bug Fixes

- Corrected issues in aap_seed role
- Corrected issues in aap_seed role

### Fix

- Bug fix in aap_seed role task when using AAP token

## v1.18.1 (2025-06-04)

### Bug Fixes

- Migration_factory_aap playbook typo

## v1.18.0 (2025-05-31)

### Features

- Updated AAP manifest logic
- Updated AAP manifest logic

## v1.17.0 (2025-05-29)

### Features

- Added support for storage hot plugging + compute refactoring
- Added support for storage hot plugging + compute refactoring

## v1.16.1 (2025-05-29)

### Bug Fixes

- Corrected logic to verify migration completion
- Corrected logic to verify migration completion

## v1.16.0 (2025-05-20)

### Features

- Adds support for creating nad without depending on the creation of the nncp

## v1.15.2 (2025-05-16)

### Bug Fixes

- Lint lines too long
- Lint lines too long

## v1.15.1 (2025-05-14)

### Bug Fixes

- Updated variables and documentation for vm_backup_restore role
- Updated variables and documentation for vm_backup_restore role

## v1.15.0 (2025-05-14)

### Features

- Updated aap_machine_credentials role to support 2.5
- Updated aap_machine_credentials role to support 2.5

## v1.14.0 (2025-05-14)

### Features

- Mfg-336 - Added validation AAP components are running after install
- Mfg-336 - Added validation AAP components are running after install

## v1.13.1 (2025-05-13)

### Bug Fixes

- Correct invalid variable in vm_lifecycle role
- Correct invalid variable in vm_lifecycle role

## v1.13.0 (2025-05-13)

### Features

- Added validation for vms_per_plan property
- Added validation for vms_per_plan property

## v1.12.5 (2025-05-08)

### Bug Fixes

- Mfg-332 Resolve Collection Syntax Errors for Automation Hub Submission

### Fix

- Mfg-332 Resolve Collection Syntax Errors for Automation Hub Submission
- Mfg-332 Resolve Collection Syntax Errors for Automation Hub Submission
- Mfg-332 Resolve Collection Syntax Errors for Automation Hub Submission

## v1.12.4 (2025-04-30)

### Bug Fixes

- Prep for Ansible 2.19 data tagging testing and add integration testing for rfc1123 filter plugin
- Prep for Ansible 2.19 data tagging testing and add integration testing for rfc1123 filter plugin

### Fix

- Define default values for roles aap_seed, aap_deploy and create_mf_aap_token when not defined by the inventory

## v1.12.3 (2025-04-11)

### Bug Fixes

- Added repository url to galaxy.yml
- Mfg-322 added repository url to galaxy.yml

## v1.12.2 (2025-04-11)

### Bug Fixes

- Add disclaimer to top of readme file for those interested in collection
- Mfg-325 Add disclaimer to top of readme file for those interested in collection

### Documentation

- Fix an unnecessary line

## v1.12.1 (2025-04-10)

### Bug Fixes

- Annotation fix for migration to new collection name
- Annotation fix for migration to new collection name

## v1.12.0 (2025-04-08)

### Features

- Mfg-280 Added support for vm and folder path
- Mfg-280 Added support for vm and folder path

## v1.11.3 (2025-04-08)

### Bug Fixes

- Mfg-282 fix pyvmomi package name
- Mfg-282 fix pyvmomi package name

## v1.11.2 (2025-04-08)

### Bug Fixes

- Mfg-322 remove unreachable links in galaxy.yml
- Remove unreachable links in galaxy.yml

### Docs

- Remove graph generation from docsible

### Documentation

- Remove graph generation from docsible

## v1.11.1 (2025-04-04)

### Bug Fixes

- Ci upload file location
- Role template naming for namespace

## v1.11.0 (2025-04-04)

### Features

- Triggering pipeline
- Triggering pipeline

## v1.10.0 (2025-04-04)

### Features

- Readme text
- Readme text

## v1.9.0 (2025-04-04)

### Features

- Documentation finalization
- Documentation finalization

## v1.8.0 (2025-04-04)

### Features

- Updated collection documentation
- Updated collection documentation

## v1.7.0 (2025-04-04)

### Features

- Mfg-320 migraion_targets role functinality was moved to aap_seed
- Mfg-320 migraion_targets role functinality was moved to aap_seed

## v1.6.9 (2025-04-04)

### Bug Fixes

- Comments in MR template were being rendered unnecessarily
- Mfg-n/a Comments in MR template were being rendered unnecessarily

### Fix

- Setting the default value for the variables controller_validate_certs and aap_validate_certs to
  true

## v1.6.8 (2025-04-04)

### Bug Fixes

- Added changelog, .ansible-lint and requirements file
- Ignore .py files with ansible-lint, enforce mandatory prod linting on pipeline
- Mfg-282 remove galaxy.yml, add changelog, remove ignores from ansible/yaml lint
- Remove galaxy.yml, add changelog, remove ignores from ansible/yaml lint

## v1.6.7 (2025-04-04)

### Bug Fixes

- Switch package name to include namespace
- Switch package name to include namespace

## v1.6.6 (2025-04-04)

### Bug Fixes

- Mfg-282 move the distlib dep into the build script
- Mfg-282 move the distlib dep into the build script

## v1.6.5 (2025-04-04)

### Bug Fixes

- Distlib missing from the semver job to upload artifact
- Distlib missing from the semver job to upload artifact

## v1.6.4 (2025-04-04)

### Bug Fixes

- Fixed the wrong name on the collection upload job
- Mfg-282 fixed the wrong name on the collection upload job

## v1.6.3 (2025-04-04)

### Bug Fixes

- Mfg-282 Linting cleanup for all roles
- Mfg-282 Linting cleanup for all roles

## v1.6.2 (2025-04-03)

### Bug Fixes

- Variable names linting, skipping markdownlint on bootstrap role
- Variable names linting, skipping markdownlint on bootstrap role

## v1.6.1 (2025-04-03)

### Bug Fixes

- Mfg-282 remove version from role readme, clean up fragments, add antsibull lint,...
- Mfg-282 remove version from role readme, clean up fragments, add antsibull lint,...

## v1.6.0 (2025-04-02)

### Bug Fixes

- Add missing python requirements
- Correct playbook lint errors
- Exclude the .ansible folder from linting
- Force installing collections already in the image to validate requirements accuracy
- Force the install of requirements and ignore fqcn warning produced by redhat.openshift.k8s
- Jmespath python dep missing from tox lint configurations
- Linting issues on vm_ssh role
- Lots of minor fixes to pass ansible-test
- Mfg-282 Lots of minor fixes to pass ansible-test
- Requirements check not failing pipeline when requirements aren't listed
- Requirements file variable being overridden in the include and not installing dependencies
- Requirements-dev missing redhat.openshift_virtualization collection

### Features

- Mgf-320 - Remove deprecated roles

## v1.5.0 (2025-04-02)

### Bug Fixes

- Mfg311 - update operator default vars and lightspeed install

### Features

- Mfg-311 - Rename collection to redhat.openshift_virtualization_migration
- Mfg-311 - Rename collection to redhat.openshift_virtualization_migration

## v1.4.0 (2025-04-01)

### Bug Fixes

- Linting issues on vm_ssh role
- Linting issues on vm_ssh role

### Feat

- Mfg-320 - Remove deprecated roles

### Features

- Mgf-320 - Remove deprecated roles

## v1.3.1 (2025-04-01)

### Bug Fixes

- Correct playbook lint errors
- Correct playbook lint errors

### Fix

- Cleanup more files in migration_targets role
- Cleanup operator_management role
- Cleanup validate_migration role
- Cleanup vm_patching role

## v1.3.0 (2025-03-28)

### Features

- Mfg-282 - Resolve variable omissions from hot_plug and lifecycle roles

## v1.2.0 (2025-03-28)

### Features

- Mfg-295 - nmstate role enhancements
- Mfg-295 - nmstate role enhancements

### Fix

- Add missing python packets
- Inventory and .che lint errors
- Mfg-282 fix cleanup of vm_collect

## v1.1.3 (2025-03-24)

### Bug Fixes

- Mfg-282 remove dependencies in mtv_migrate role
- Mfg-282 remove dependencies in mtv_migrate role

## v1.1.2 (2025-03-21)

### Bug Fixes

- Mfg-289 Corrected mtv_management_migration_namespace variable
- Mfg-289 Corrected mtv_management_migration_namespace variable

## v1.1.1 (2025-03-21)

### Bug Fixes

- Mfg-289 Corrected VDDK variables
- Mfg-289 Corrected VDDK variables

## v1.1.0 (2025-03-20)

### Features

- Mfg-289 Added support for VDDK credentials
- Mfg-289 Added support for VDDK credentials

## v1.0.3 (2025-03-20)

### Bug Fixes

- Migration_factory_aap linting issues

### Feat

- Mfg-276 Updates to support AAP 2.5
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content
- Mfg-282 Standardize Ansible Content

## v1.0.2 (2025-03-18)

### Bug Fixes

- Mfg-279 More polish on CI templates and pre-commit configs
- **ci**: Pyproject.toml update to run shell script build
- **ci**: Remove assets from pyproject.toml and add playbooks to build script
- **ci**: Secret scanner using too much memory with other jobs

## v1.0.1 (2025-03-18)

### Bug Fixes

- Add new AH variables for certified and validated
- Add new AH variables for certified and validated
- Added include for doc generation
- Build and publish collection automatically
- Do not import artifacts in docs generation
- Mfg-294 Correct logic to also include empty properties
- Mfg-294 Correct logic to also include empty properties
- Switched from pip to pip3 in pipeline
- Tweaks to galaxy and fresh start readme
- Update the build process to a shell script
- **ci**: Added placeholder "script" section to rules template
- **ci**: Cleaning up comments and adding changelog fragment
- **ci**: Gitlab can't merge script arrays, switching to after_script
- **ci**: Removed the duplicate rules from .gitlab-ci.yml file
- **ci**: Switch to using reference instead of extends
- **ci**: Test merging in the semver template rather than .gitlab-ci.yml
- **Dev Env**: Clean pre-commit configs
- **pipeline**: Gitleaks - Mark project directory as safe for gitleaks scanning
- **pipeline**: Gitleaks - Mark project directory as safe for gitleaks scanning

### Docs

- Mfg-229 Add default request template

### Documentation

- Added collection tags, build ignore and updated repo links
- Changelog fragment covering the merge request template
- Mfg-229 Added default merge request template
- Removed accidental changes to ci process from other task
- Updated template based on MR feedback
- **Dev Env**: Added changelog for local env script

### Feat

- Mfg-282 Added AAP Machine Credentials role

### Features

- Add docsible to pipeline
- Added environment setup script w/ precommit
- Added target and provider namespace to mtv_management role
- Added target and provider namespace to mtv_management role
- Mfg-233 Add env setup script and pre-commit
- **ci**: Add semver with docsible

### Fix

- Add dependencies to requirements.yml and enable entitled content pulls in pipeline
- Add dependencies to requirements.yml and enable entitled content pulls in pipeline
- Allow out of group forks to run the pipeline for improved collaboration
- Allow the pipeline to pull all content and pass min profile
- Allow the pipeline to pull all content and pass min profile
- Ci: update py semver settings
