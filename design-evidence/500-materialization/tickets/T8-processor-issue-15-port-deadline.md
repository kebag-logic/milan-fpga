<!-- Draft by A152 for the manager to post as an addendum to the EXISTING processor issue 15 (Mister-M-alt/protocol-processor-control-plane-avb-milan), not a new issue. It records what the #500 D3 contract needs from that issue; it does not change its scope or owner. -->

# Addendum to processor issue 15: what the D3 restore contract needs from a port deadline

## Context

kebag-logic/milan-fpga #500 proposes the D3 materialization contract
(`docs/design/SAVED_STATE_MATERIALIZATION.md`). Its restore is contained
WITHOUT this issue: the D3 writer bounds its own waits, abandons a read the
port is serving, and the arbiter in front of `KL_pp_nvm_port` drains that
read until the device ends it (page section 8.8). Two things stay unbounded
until this issue lands, and the contract says so rather than relying on it:

- The BINDING walk (`KL_acmp_nvm_shadow`) keeps no deadline. A device that
  never answers during it keeps the restore unterminated, so the entity is
  never enabled and AECP dispatch stays held: fail-closed, never an early
  enable.
- A read the D3 writer abandoned keeps the port busy until the device ends
  it. A device that never does keeps the port drained for ever: later
  changes read pending and never durable, which is honest and permanent.

## What a deadline must do to be usable here

1. End a device command that makes no progress within the deadline with a
   timeout the manager can tell from a device error and from an unframed
   record, never with a done.
2. Quarantine the port until the device ends that command (done or err):
   hold `dev_rready_o` for a read, keep `nvm_busy_o` high, accept no new
   operation, and swallow the late bytes and the completion, so an untagged
   late response can only ever end the command it belongs to. A device that
   never ends it keeps the port quarantined and says so; the port is never
   reused on time alone.
3. Report a device error during a HEADER read distinctly from an unframed
   header. Today both end in one err pulse with nothing forwarded, so a
   media or bus error on a record's header lane reads as an erased record,
   and a persistent one restores that record's default without a failure
   verdict (the D3 contract's UNRESOLVED 5).
4. Have the binding manager treat a port timeout during its restore walk as
   a torn walk (fail whole, done with fail), never as a blank record.

## What it would change in the D3 contract

The binding walk would end in bounded time, so the entity comes up on
defaults with restore fail set instead of staying dark; and a permanently
silent device would stop holding the port. The D3 writer's own deadline and
the roll-back would not change.
