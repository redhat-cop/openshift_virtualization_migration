# Migration validation VMware power-state replacement

Research date: 2026-10-16. Research only; no implementation changes or live VM operations.

## Recommendation

Replace `community.vmware.vmware_guest_powerstate` with
`vmware.vmware.vm_powerstate`. Community 7.0.0 **tombstones** the old name;
its runtime routing recommends the replacement but does not redirect calls.
The release changelog confirms removal. Pinning community below 7 only defers
the migration. [1]

Keep `moid` and `state: powered-off`. Add a real, nonempty `datacenter`,
preserve the per-VM validation gates, and fix error accounting before claiming
successful power-off. Do not claim verified vCenter 6.x support. [2][3]

## Exact contract

| Concern | Verified replacement behavior |
| --- | --- |
| VM identity | `moid` remains `moid`, not `vm`, `vm_id`, or `managed_object_id`. Exactly one of `name`, `uuid`, `moid` is required; they are mutually exclusive. MoIDs are unique only within the connected vCenter. Keep the same host/credential context as the source lookup. [2] |
| State spelling | `powered-off` is valid; `powered_off` is not an argument-spec choice. Internal normalization does not make an invalid input choice valid. [2] |
| Hard stop | `powered-off` calls `self.vm.PowerOff()`. `shutdown-guest` instead calls `ShutdownGuest()`, requires running VMware Tools, and polls for shutdown. These are different operations. Do not substitute guest shutdown for the role's hard-stop contract. [2] |
| Datacenter | A required string even with `moid`. Current validate_migration omits it on mutation and defaults its inventory value to empty. Require/resolve an authentic datacenter before mutation, not `omit`, an empty string, or a fabricated default. In the inspected lookup helper, datacenter formats folder paths; MoID-only lookup does **not** independently validate datacenter membership. [2][3] |
| Credentials | `hostname`, `username`, `password` retain their names; environment fallbacks are `VMWARE_HOST`, `VMWARE_USER`, `VMWARE_PASSWORD`. Username aliases: `user`, `admin`; password aliases: `pass`, `pwd`. Empty connection credentials fail in the client. Explicit role values take precedence over module environment fallback. [4][5] |
| TLS/port | `validate_certs` is a boolean, default `true`; fallback `VMWARE_VALIDATE_CERTS`. `port` defaults to 443, fallback `VMWARE_PORT`. Retain the role's certificate setting and secure-logging variable. Trust the vCenter CA in the executing environment rather than disabling verification. No module-specific CA-file parameter exists in this schema. [4][5] |
| Force/timeout | `force` defaults to `false`; non-on/non-off current states require it. A hard stop does **not** require `force: true`. `timeout` defaults to 3600 seconds and bounds task monitoring. Do not add scheduling or question-answer parameters. [2][6] |

### Idempotency and check mode

For immediate `powered-off`, a VM already off exits with `changed: false`;
an on VM invokes `PowerOff()` and waits for its task. Check mode still connects
and resolves the VM, then predicts `changed: true` without configuring its power
state. `supports_check_mode=True` appears in both the introducing 1.11.0 module
and 2.12.0. It is not an offline connectivity test. Pending VM questions can fail
before the normal state/check-mode exit. [2][7]

Keep role reporting check-mode-aware: a predicted change is not evidence that a
VM powered off. For strongest operational confirmation, read back the actual
power state after a successful mutation; the replacement does not return it. [2]

### Return and error handling

- Success: `changed` plus `vm: {name: ..., moid: ...}`. There is no returned
  `instance.hw_power_status`; keep using the separate guest-info lookup for its
  existing `instance` facts, not the power module's output. [2]
- Explicit module failures use `fail_json(msg=...)`, for example missing VM,
  disallowed source state, pending question, VMware operation exception, or task
  timeout. Those branches do not pass the success `vm` result through. Client
  initialization can instead raise `ApiAccessError`/`MissingLibError`, producing
  executor-level failure/exception output. Do not require one universal error
  dictionary, a VMware error-code field, or a success-shaped `vm` on failure.
  A timeout may follow an issued mutation; failure does not prove nothing
  changed. [2][3][5][6]
- **Existing reporting bug:** `roles/validate_migration/tasks/power_off.yml` sets
  `failed_when: false` on lookup and mutation, then tests `results[*].failed`.
  Ansible overwrites `failed` with the failed-when expression result, including
  false. The summary also classifies successful power-off from pre-mutation
  facts/gates rather than the mutation result, so it can report an attempted,
  failed operation as powered off. This is not fixed by changing the FQCN. [8]
- Proposed approach: remove `failed_when: false`, retain `ignore_errors: true`
  where graceful collection is intended, and classify every registered loop
  result explicitly: skipped, failed, successful, or predicted-only check mode.
  Preserve and test missing/invalid response handling. Require valid lookup
  identity before calling the mutator; match mutation results by source identity.
  Do not log raw failure payloads containing credentials. `ignore_errors` does
  not universally catch undefined-variable, syntax, unreachable, or plugin-loading
  errors; module resolution belongs in a separate deterministic guard. [8]

## Versions, Python, and execution environment

| Version | Verified minimums |
| --- | --- |
| `vmware.vmware` 1.11.0 | First release containing `vm_powerstate`; runtime requires ansible-core >=2.15.0; module test configuration declares Python >=3.9; collection requirements specify pyVmomi >=6.7.1. [7][9] |
| `vmware.vmware` 2.0.0 through inspected 2.12.0 | Core >=2.16.0; module Python >=3.9; pyVmomi >=8.0.3.0.1. Core 2.16 itself requires controller Python >=3.10. Thus a localhost/EE running core 2.16 needs >=3.10, not merely the module's 3.9. [9][10] |
| Local CI | `requirements-ci.txt` pins core 2.20.1; `requirements-dev.txt` requests >=2.20. Core 2.20 requires controller Python >=3.12. [10] |

Local inspection:

- `galaxy.yml` and `requirements-dev.yml` declare community >=5.5.0 and
  vmware_rest >=4.6.0, but no direct `vmware.vmware` dependency, despite existing
  uses in `roles/pre_migration_vm/tasks/enable_cbt.yml`.
- `meta/runtime.yml` advertises core >=2.16.0. This replacement needs no increase
  for the 2.x collection. There is already a broader dependency mismatch:
  community 5.5.0 requires core >=2.17.0, while installed community 7.0.0 requires
  >=2.21.0. Unbounded community resolution cannot validate the advertised core
  floor or the pinned 2.20 CI environment. Resolve that separately, not by
  asserting that the replacement requires core 2.21. [1][11]
- No checked-in `execution-environment.yml` or `extensions/ee/` exists.
  `docs/architecture-v2.md` proposes an EE with unbounded `pyVmomi`, but it is a
  design example, not a build definition. `test-requirements.txt` does not install
  pyVmomi; `tests/integration/requirements.txt` is a placeholder. The devfile's
  moving container tag does not establish installed VMware SDK versions.

**Minimal justified bounds:** add direct `vmware.vmware: ">=1.11.0"` to the
collection and developer requirements; this is the actual module introduction,
not 2.4.0 or 2.12.0. No upper bound is technically established by this research.
If project policy excludes untested majors, an upper bound is a policy decision,
not a demonstrated incompatibility. Lock and test an exact EE combination
(2.12.0 is locally installed and catalog-certified), with pyVmomi
>=8.0.3.0.1 for 2.x. Do not raise this role's collection floor to 2.4 solely for
the shutdown-guest timeout fix: that is not the proposed operation. [9][12]

The exact collection version's full Python requirements must be installed by
the EE build, not by Galaxy alone. At 2.12.0 the collection lists `pyVmomi` and
`vmware-vcenter`; the SOAP client also imports `requests`. A module-specific
minimal environment must ensure both pyVmomi and requests; a full collection EE
must retain the full dependency closure. Do not install the old 1.11 SDK git
requirement blindly into a modern production EE. [5][9]

## vCenter 6.x and certification: evidence boundaries

- The replacement uses pyVmomi `SmartConnect`, not the vmware_rest API. That
  establishes a SOAP implementation, **not official support for every SOAP-era
  vCenter version**. The inspected collection source/docs do not establish a
  vCenter 6.0/6.5/6.7 support matrix. [2][5]
- pyVmomi 8.0.3.0.1 documents backward compatibility with the previous four
  vSphere releases and warns that older versions may work without active
  support. This SDK policy is not a collection certification or an exact
  vCenter 6.x matrix, and unbounded SDK upgrades can change that baseline. [13]
- Upstream has real-vCenter integration tasks for MoID power-off and separate
  unit mocks. The inspected integration workflow targets an environment named
  `eco-vcenter`, without a published vCenter version matrix. Its suite also
  uses REST modules. This proves test coverage exists, not that 6.x was tested
  or officially supported. No live compatibility was verified here. [14]
- Local ansibleize policy ranks `vmware.vmware` as preferred certified content
  above `community.vmware` (reference file, lines 15-53). Independently, Red
  Hat's public Ecosystem Catalog labels `vmware.vmware` **Certified**, provided
  by VMware, and lists certified version **2.12.0**. Upstream's README also
  describes Red Hat Ansible Certified Content support. The Automation Hub URL
  returned only the console shell in this session, so no authenticated Hub
  artifact or historical 1.11.0 certification was verified. Certification does
  not independently establish support for an EOL vCenter. [15]

**Uncertainty to retain:** actual connectivity/behavior on each required 6.x
minor release and patch level, its supported SDK combination, and contractual
Red Hat/Broadcom support remain unverified. Replace existing blanket “covers
vCenter 6.x+” comments with this limitation; obtain vendor confirmation and an
authorized disposable-lab test before making a support claim.

## Minimal proposed mutation task

### Gathering is not a drop-in replacement

The operator requires retaining vCenter 6.x, with the exact minor releases
currently unknown. Do not interpret approval of a full swap as permission to
drop that requirement.

In inspected `vmware.vmware` 2.12.0, `vm_info` inherits `ModuleRestBase`.
Its constructor connects the REST client before creating its SOAP helper;
the REST client calls `create_vsphere_client`. Selecting `schema: vsphere`
does not bypass this initialization. Its output is a `vms` list rather than
the community module's single `instance` mapping, and a missing VM can return
an empty list. A full swap therefore needs API compatibility validation and
explicit response-shape adaptation, not just an FQCN change. [16][17][18]

Ansibleize's certified-first policy does allow justified lower-tier content
when the higher-tier implementation cannot meet a required capability. Pending
confirmation of the legacy baseline, retain the SOAP-only gather as a proposed
compatibility exception; do not claim either module is officially supported on
all 6.x versions. Ask the operator to approve this narrower scope before
implementation. The certified SOAP power-state replacement remains the proposed
mutation path, subject to SDK/vendor compatibility verification.

Scoped audit findings:

- **MUST-FIX — Module hierarchy/compatibility:** replace the tombstoned power
  module and declare the direct dependency. Do not introduce a REST-dependent
  gather without establishing compatibility with the required legacy releases.
- **MUST-FIX — Task result accounting:** preserve real module failures and
  classify mutation results instead of inferring success from pre-action facts.
- **MUST-FIX — Variable validation:** reject missing datacenter before an
  enabled mutation; keep report-only mode read-only.
- **OK — Security contract:** retain toggleable secure logging, certificate
  verification, MoID targeting, and the existing per-VM fail-closed gates.
- **SUGGEST — Testing:** automate installed-module resolution/schema checks and
  mocked failed-mutation reporting; require authorized legacy lab validation
  before advertising compatibility.

Illustrative replacement only. Prevalidation must reject missing datacenter and
record a failed check without mutating. The reporting corrections above remain
required. Keep all existing plan/list/VM/disk gate computation.

```yaml
- name: power_off | Power off validated source VMs (hard stop)
  vmware.vmware.vm_powerstate:
    hostname: "{{ validate_migration_vcenter_hostname }}"
    username: "{{ validate_migration_vcenter_username }}"
    password: "{{ validate_migration_vcenter_password }}"
    validate_certs: "{{ validate_migration_vcenter_validate_certs | bool }}"
    datacenter: "{{ validate_migration_vcenter_datacenter }}"
    moid: "{{ __validate_migration_power_vm.instance.moid }}"
    state: powered-off
  loop: "{{ __validate_migration_power_facts.results | default([]) }}"
  loop_control:
    loop_var: __validate_migration_power_vm
    label: "{{ __validate_migration_power_vm.item | default('unknown') }}"
  when:
    - validate_migration_power_off_source | bool
    - validate_migration_vcenter_datacenter | length > 0
    - __validate_migration_power_gate.get(__validate_migration_power_vm.item, false) | bool
    - not (__validate_migration_power_vm.failed | default(false) | bool)
    - __validate_migration_power_vm.instance.moid is defined
    - __validate_migration_power_vm.instance.moid | length > 0
    - (__validate_migration_power_vm.instance.hw_power_status | default('')) != 'poweredOff'
  register: __validate_migration_power_results
  ignore_errors: true
  no_log: "{{ validate_migration_secure_logging }}"
```

## Deterministic test plan, no live power-off

1. **Resolution/schema guard in CI/pre-commit:** run
   `ansible-doc --json vmware.vmware.vm_powerstate` inside the actual EE and
   parse its JSON. Fail unless the exact FQCN resolves, `moid` is a string,
   `datacenter` is required, `powered-off` is a choice, `powered_off` is not,
   and all task option names exist. Inspect the resolved installed argument
   spec in a mocked module invocation to enforce mutual exclusion, required
   datacenter, accepted types, and check-mode support. Documentation/schema
   resolution alone does not execute validation. Test the lower supported
   collection version and the locked production version; never accept lint's
   mocked-module resolution as this guard.
2. **Mocked module tests:** patch connection/VM lookup/task monitoring before
   entry, and deny real socket access. Assert already-off returns unchanged
   with zero `PowerOff` calls; on-to-off calls it exactly once; check mode makes
   zero mutation calls and predicts change. Assert `ShutdownGuest` and
   `RebootGuest` are never called. Cover suspended state without force, missing
   VM, invalid parameters, pending questions, login/TLS/library errors, VMware
   task exception, and timeout after dispatch. Check actual failure payloads,
   not a success-only stub. Upstream unit tests provide a starting pattern. [14]
3. **Mocked role tests:** intercept the real FQCN and record attempted calls.
   For each false/missing fatal gate, disabled opt-in, failed lookup, empty
   MoID/datacenter, and isolated `--tags poweroff`, assert zero mutations.
   For two VMs with mixed validation outcomes, assert only the validated MoID
   is called. Test failures on both lookup and power-off under Ansible's real
   executor, ensuring the final check fails and never reports “Powered off”.
   Cover skipped loop entries, already-off VMs, partial successes, malformed
   results, and check-mode wording. Verify credentials remain censored.

Executed here: local `ansible-doc --json` successfully resolved the installed
2.12.0 module and confirmed the documented parameters. No mock suite, EE build,
or live power operation ran. Implementation of the proposed guards/tests is
outside this research-only change.

## Live validation addendum (2026-10-16, pool1)

Read-only report-only run against the practice environment (OpenShift +
fake-vCenter emulator), plus an authorized fix-and-rerun of the failed e2e
migration. No credential values were exposed; the source was never mutated
in report-only mode.

Verified live:

- Both `vmware_guest_info` schemas work against the emulator: summary
  (moid, hw_power_status, ipv4) and vsphere
  (`config.hardware.device` → disks carrying `capacityInKB`) — the
  disk-topology shape previously verified only against docs is confirmed
  against a live endpoint.
- All seven checks produced correct verdicts on a failed migration; the
  summary assert failed the play naming the failed checks; report-only mode
  made no mutation and reported the source power state with its MoID.

Two detail-path bugs found by the live run, fixed, and covered by new
offline regression cases (`plan failed`, `plan none` in
`tests/unit/test_validate_migration_power.py`):

- Plan discovery: current forklift embeds the latest run's status snapshot
  in `Plan.status.migration` (a dict, not the Migration CR name). The role
  now discovers the latest Migration CR by `spec.plan.name` and
  `creationTimestamp` instead. `mtv_migrate` knows its Migration name
  because it created the object; validate_migration arrives after the fact and must
  discover it.
- Disks `source_ok` conflated target-VM existence with vCenter lookup
  success; a missing target VM reported "vCenter lookup failed … rotate the
  exposed credential". `source_ok` now reflects only the source lookup, and
  a missing target reports the honest disk-count mismatch.

Environment finding (not a role issue): the pool1 practice nodes are Xeon
E5-2650 v2 (Ivy Bridge, no AVX2 — below the x86-64-v3 baseline). MTV 2.11.7
and 2.12.10 both pass `--no-fstrim` to virt-v2v-inspector, but their shipped
rhel9 v2v images predate the flag, and their rhel10 images require
x86-64-v3 and die with SIGILL (exit 132) on those CPUs — no shipped image
combination can convert on that hardware. Nothing in this collection sets
the original `virt_v2v_image_fqin` pin that masked this. The fix applied on
pool1: `playbooks/utility_v2v_nofstrim_shim.yml` builds a shim image FROM
the installed MTV's own rhel9 v2v image (wrapping virt-v2v-inspector and
virt-v2v to strip only `--no-fstrim`, which the flag only uses to disable
an fstrim pass the rhel9 build never performed), pushes it to the cluster's
integrated registry (switched from Removed to Managed, emptyDir storage),
and pins `ForkliftController.virt_v2v_image_fqin` to it. With the shim the
conversion proceeds normally; the migration succeeds.



[1]: https://github.com/ansible-collections/community.vmware/blob/7.0.0/meta/runtime.yml
[2]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/modules/vm_powerstate.py
[3]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/module_utils/_module_pyvmomi_base.py
[4]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/module_utils/argument_spec.py
[5]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/module_utils/clients/pyvmomi.py
[6]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/module_utils/_vsphere_tasks.py
[7]: https://github.com/ansible-collections/vmware.vmware/blob/1.11.0/plugins/modules/vm_powerstate.py
[8]: https://github.com/ansible/ansible/blob/stable-2.16/lib/ansible/executor/task_executor.py
[9]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/CHANGELOG.rst
[10]: https://github.com/ansible/ansible/blob/stable-2.16/setup.cfg
[11]: https://github.com/ansible-collections/community.vmware/blob/5.5.0/meta/runtime.yml
[12]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/requirements.txt
[13]: https://github.com/vmware/pyvmomi/blob/v8.0.3.0.1/README.rst
[14]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/tests/integration/targets/vm_powerstate/tasks/eco-vcenter.yml
[15]: https://catalog.redhat.com/en/software/collection/vmware/vmware
[16]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/modules/vm_info.py
[17]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/module_utils/_module_rest_base.py
[18]: https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/plugins/module_utils/clients/rest.py

Additional exact-version evidence:

- [Community removal changelog](https://github.com/ansible-collections/community.vmware/blob/7.0.0/CHANGELOG.rst)
- [1.11.0 core minimum](https://github.com/ansible-collections/vmware.vmware/blob/1.11.0/meta/runtime.yml),
  [Python declaration](https://github.com/ansible-collections/vmware.vmware/blob/1.11.0/tests/config.yml),
  [SDK requirements](https://github.com/ansible-collections/vmware.vmware/blob/1.11.0/requirements.txt)
- [2.12.0 core minimum](https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/meta/runtime.yml),
  [Python declaration](https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/tests/config.yml),
  [2.0.0 SDK requirements](https://github.com/ansible-collections/vmware.vmware/blob/2.0.0/requirements.txt)
- [Core 2.20 Python requirement](https://github.com/ansible/ansible/blob/stable-2.20/pyproject.toml),
  [2.20 failure-override implementation](https://github.com/ansible/ansible/blob/stable-2.20/lib/ansible/executor/task_executor.py)
- [Upstream unit tests](https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/tests/unit/plugins/modules/test_vm_powerstate.py),
  [integration workflow](https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/.github/workflows/ansible-integration.yaml)
- [Upstream certification/support statement](https://github.com/ansible-collections/vmware.vmware/blob/2.12.0/README.md),
  [Automation Hub entry](https://console.redhat.com/ansible/automation-hub/repo/published/vmware/vmware/)
