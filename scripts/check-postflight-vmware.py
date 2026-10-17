#!/usr/bin/env python3
"""Fail early if the real installed VMware module contract is unavailable.

Guards both vCenter modules the postflight role dispatches:
- vmware.vmware.vm_powerstate (the mutation) — its hard-stop contract
- community.vmware.vmware_guest_info (the SOAP-only gather) — the same
  tombstone risk class that removed vmware_guest_powerstate in
  community.vmware 7.0.0

Prints the resolved module paths so a stub tree is visible in the output.
"""

import json
import os
from pathlib import Path
import subprocess
import sys


def powerstate_assertions(options):
    required = {"hostname", "username", "password", "validate_certs",
                "datacenter", "moid", "state"}
    return [
        (required <= options.keys(), "vm_powerstate: missing task parameters"),
        (options["datacenter"].get("required"),
         "vm_powerstate: datacenter contract changed"),
        (options["moid"].get("type") == "str",
         "vm_powerstate: MoID must be a string"),
        ("powered-off" in options["state"]["choices"],
         "vm_powerstate: hard-stop state unavailable"),
        ("powered_off" not in options["state"]["choices"],
         "vm_powerstate: review changed state schema"),
    ]


def guest_info_assertions(options):
    required = {"hostname", "username", "password", "validate_certs",
                "name", "datacenter", "schema", "properties"}
    return [
        (required <= options.keys(),
         "vmware_guest_info: missing gather parameters"),
        ({"summary", "vsphere"} <= set(options["schema"].get("choices", [])),
         "vmware_guest_info: summary/vsphere schemas unavailable"),
        (options["properties"].get("type") == "list",
         "vmware_guest_info: properties must be a list"),
    ]


def check_module(env, root, fqcn, assertions):
    """Return the resolved module filename, or raise on contract drift."""
    result = subprocess.run(
        ["ansible-doc", "--json", fqcn], env=env, cwd=root,
        capture_output=True, text=True, check=True,
    )
    doc = json.loads(result.stdout)[fqcn]["doc"]
    options = doc["options"]
    problems = [message for valid, message in assertions(options) if not valid]
    if problems:
        raise ValueError("; ".join(problems))
    return doc.get("filename", "unknown path")


def main():
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    local = root / ".ansible" / "collections"
    if local.is_dir() and not env.get("ANSIBLE_COLLECTIONS_PATH"):
        env["ANSIBLE_COLLECTIONS_PATH"] = os.pathsep.join(
            [str(local), str(Path.home() / ".ansible/collections")]
        )
    # Fail closed: verify THE required collection, not whichever version
    # happens to sit on sys.path. ansible-doc honors this env var. The
    # resolved module path is printed so a caller-set stub tree is visible.
    env["ANSIBLE_COLLECTIONS_SCAN_SYS_PATH"] = "false"
    checks = [
        ("vmware.vmware.vm_powerstate", powerstate_assertions),
        ("community.vmware.vmware_guest_info", guest_info_assertions),
    ]
    try:
        resolved = [(fqcn, check_module(env, root, fqcn, assertions))
                    for fqcn, assertions in checks]
    except (OSError, subprocess.CalledProcessError, ValueError,
            KeyError, TypeError) as error:
        print(f"VMware module contract check failed: {error}", file=sys.stderr)
        print("Install the collections (requirements-dev.yml, or"
              " 'ansible-galaxy collection install vmware.vmware"
              " community.vmware'); do not rely on lint mocks.", file=sys.stderr)
        return 1
    for fqcn, path in resolved:
        print(f"Verified installed module contract: {fqcn} ({path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
