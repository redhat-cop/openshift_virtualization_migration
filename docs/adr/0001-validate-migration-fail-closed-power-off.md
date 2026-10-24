# ADR-0001: Migration validation source power-off is per-VM and fail-closed

Date: 2026-10-16
Status: Accepted

## Context

Migration validation (the post-migration validation pass) powers off source VMs by
default after a migration. A power-off is destructive: if the migration
failed or a migrated VM is unhealthy, powering off its source removes the
operator's fallback.

## Decision

The source power-off is per-VM and fail-closed:

- A source VM is powered off only after ITS migrated counterpart passes
  every validate_migration check.
- A failed check leaves that source VM running; the role reports which
  sources stayed on and why.
- The toggle (`validate_migration_power_off_source`, default on) switches the
  action off entirely; in that mode the role reports source power state as
  a read-only check and never mutates.

The power-off is a hard stop via the vCenter API — not a graceful guest
shutdown; the migrated counterpart is already validated at that point. It
is the only sanctioned mutation in validate_migration; every other check is a
read-only probe.

## Consequences

- Partial migrations are safe: the sources of failed VMs stay available
  for retry or rollback.
- The default-on toggle is safe only because of the fail-closed gate —
  the two decisions are paired and must not be separated.
- Operators running with the toggle on must treat a "sources still
  running" summary as the signal to investigate, not as a role failure to
  force through.
