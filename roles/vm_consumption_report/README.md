# vm_consumption_report

Generate consumption reports for OpenShift Virtualization VMs managed
via the `redhat.openshift_virtualization` collection. The report
distinguishes between **directly managed hosts** (contacted via SSH or
WinRM) and **indirectly managed VMs** (automated via the Kubernetes
API), and supports **reconciliation** of hosts that are managed through
both methods.

## Requirements

- `kubernetes.core` collection
- OpenShift API access with permission to list VirtualMachine and
  VirtualMachineInstance resources

## Role Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `vm_consumption_report_request` | yes | `[]` | List of query entries (namespace, names, label_selectors) |
| `vm_consumption_report_direct_hosts` | no | `[]` | List of directly managed hosts for reconciliation |
| `vm_consumption_report_openshift_host` | yes | `{{ openshift_host }}` | OpenShift API endpoint |
| `vm_consumption_report_openshift_api_key` | yes | `{{ openshift_api_key }}` | OpenShift API token |
| `vm_consumption_report_openshift_verify_ssl` | yes | `{{ openshift_verify_ssl }}` | Verify SSL certificates |
| `vm_consumption_report_output_format` | no | `json` | Output format: `json` or `csv` |
| `vm_consumption_report_output_path` | no | `""` | File path to write the report |
| `vm_consumption_report_include_status` | no | `true` | Query VMIs for running status and guest OS info |

## Output

The role sets `vm_consumption_report_result` containing:

- `summary` — Counts of total VMs, indirect-only, direct-only, and reconciled
- `indirect_vms` — List of OpenShift VMs with UUID, namespace, status, guest hostname, and management type
- `direct_only_hosts` — Hosts that are directly managed but not matched to any OpenShift VM

## Reconciliation

When `vm_consumption_report_direct_hosts` is provided, the role
matches direct hosts to OpenShift VMs by:

1. **UUID match** — Direct host UUID matches VM `metadata.uid`
2. **Hostname match** — Direct host hostname matches the guest OS
   hostname reported by the VMI
3. **IP match** — Direct host hostname matches an IP address on a VMI
   network interface

Matched entries are marked `management_type: reconciled`.

## Example

```yaml
vm_consumption_report_request:
  - namespace: production-vms
  - namespace: staging-vms
    label_selectors:
      - app=web

vm_consumption_report_direct_hosts:
  - hostname: web-server-01.example.com
  - hostname: db-server-02.example.com
    uuid: 5a3f8c2e-1234-5678-9abc-def012345678

vm_consumption_report_output_format: json
vm_consumption_report_output_path: /tmp/consumption_report.json
```
