# Glossary

Domain vocabulary for the openshift-virtualization-migration collection.

## Preflight

The pre-migration validation pass (role `preflight`, playbook `vmf_preflight.yml`). Validates the migration environment before seeding AAP and running a migration: OpenShift API authentication, OpenShift Virtualization and MTV operator health, AAP access, vCenter connectivity, and VDDK init image configuration. Read-only probes; fails the play with an actionable message per failed check.

## Postflight

The post-migration validation pass (role `postflight`, playbook `vmf_postflight.yml`). Runs as a standalone playbook after `vmf_migrate` completes — the operator or an AAP job template invokes it; it is not wired into the MTV pipeline (the in-pipeline hook path is `mtv_hook_invoke_aap`). Validates migration outcomes and performs the source power-off.

## Source VM

The original VMware virtual machine being migrated to OpenShift Virtualization. Queried read-only via the vCenter API.

## Migrated VM

The OpenShift Virtualization virtual machine produced by a migration; the counterpart of one source VM. Verified via the Kubernetes API (VirtualMachine / VirtualMachineInstance status).

## Migration plan

The MTV (Forklift) Plan custom resource that groups source VMs with network and storage maps and drives the migration. Referenced by name and namespace (`mtv_migrate_plan_name`, `mtv_migrate_plan_namespace`).

## Source power-off

The post-migration cutover step of powering off source VMs whose migrated counterparts passed validation — a hard stop via the vCenter API. Performed by postflight, controlled by a toggle (default: on), gated per-VM and fail-closed — see docs/adr/0001-postflight-fail-closed-power-off.md.
