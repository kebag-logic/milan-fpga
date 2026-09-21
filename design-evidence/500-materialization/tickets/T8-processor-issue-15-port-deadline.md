<!-- Draft by A152, rewritten by A153 for the manager to file as a NEW processor issue (Mister-M-alt/protocol-processor-control-plane-avb-milan) that references issues 15 and 20. It closes neither, amends neither issue's criteria, and changes neither's scope or owner. The file keeps its name so existing citations resolve. -->

# Prerequisites of D3 stage 1: the port's terminal cause and a bounded binding walk

## Why this is a prerequisite

kebag-logic/milan-fpga #500 proposes the D3 materialization contract
(`docs/design/SAVED_STATE_MATERIALIZATION.md`). Its restore is a transaction:
a transport failure in either pass ends with complete defaults and a failure
verdict. Two pinned facts break that, and the contract makes their fixes
prerequisites of the stage-1 implementation lane and of every shippable
stage:

1. `KL_pp_nvm_port` ends every HEADER-phase failure in one err with nothing
   forwarded: a device error, a header read the device ended short, and a
   header the device delivered whole that fails the magic or length gate
   (an erased or unframed record). A manager cannot tell a failing device
   from an erased record, so a device error that recurs on a header in both
   passes restored that record's default with no failure verdict (round-two
   reviews R217 R2-F1, R218 F1). Processor issue 20's manager-only split
   cannot fix it: an erased header is ALSO err with zero bytes, so treating
   every zero-byte err as a fault fails every first boot.
2. The D3 writer holds AECP dispatch from reset until the restore's terminal,
   and the restore starts after the binding walk. `KL_acmp_nvm_shadow` has
   no deadline, so a silent device during the binding walk would hold every
   AECP command for ever. `SAVED_STATE_FASTCONNECT.md` section 9.3 requires
   the entity to keep answering AECP when persistence wedges (R217 R2-F3).

## S1: the port's terminal cause

Add `nvm_err_cause_o[1:0]`, valid with `nvm_err_o` and 0 otherwise:

| Code | Name | Produced when |
|---|---|---|
| 1 | DEVICE | the device reported an error in any state, or ended the 8-byte header read short |
| 2 | UNFRAMED | the device COMPLETED the header read (done, no error) and the header failed the port's magic or length gate; or the manager's own commit header failed that gate |
| 3 | reserved | a deadline, if issue 15's accepted contract adds one; never produced by this ticket |

UNFRAMED means the device answered with a header that is not a record. It
does not prove erased media (issue 15's readiness report: eight 0xFF bytes
do not prove the span erased), and nothing here claims it does: an UNFRAMED
record keeps its default, and a walk that validated no record reports blank.

## S1 in the binding manager (processor issue 20's defect)

`rs_empty_w` (the per-record vendor default) takes a zero-byte err only
when the cause is UNFRAMED, and a clean done with zero bytes as today. A
zero-byte DEVICE err fails the WHOLE walk as a torn read does: restore fail,
done, no preload, every uncaptured sink at its vendor default.

## S3: a bounded binding walk

The binding manager bounds the READ phase of its restore walk (waiting for
the port idle in `H_RS_REQ`, and for a byte, done or err in
`H_RS_STREAM`) by a no-progress deadline, `RS_TMO_CYC_P` cycles. Expiry
fails the whole walk as above and, when a read was issued, abandons it:
`nvm_abort_o` pulses and the manager arbiter in front of the port (the D3
contract's `KL_pp_nvm_mgr_arb`) DRAINS it, holding rready, swallowing the
late bytes and the done or err, and granting no manager until the device
ends that read. A new `restore_cause_o[1:0]` reports 1 torn, 2 a device error
with nothing forwarded, 3 the deadline. The preload phase waits on the
on-chip listener and is not watched.

## What this ticket does NOT do, stated so no lane relies on it

- It does not give the PORT a deadline, and it releases nothing on time.
- A device that never ends the abandoned read keeps the port QUARANTINED FOR
  EVER. Nothing here makes that port reusable: every later binding or D3
  change reads pending and never durable, until a reset. Commands are
  still served (the binding walk and then the D3 walk end at their
  deadlines, on defaults, and the entity is enabled).
- A device that ends the read late ends the drain, and the port serves the
  next operation. That is the ONLY route back to persistence service here.
- Reusable port service after a permanently silent device needs a real
  cancellation or device-reset acknowledgement, which is issue 15's open
  recovery contract. Issue 15's criterion 2 ("the port serves the next
  request") remains undelivered and its proposed amendment unaccepted; this
  ticket does not deliver, amend or close it. If issue 15's accepted
  contract supplies a bounded terminal notification with quarantine at the
  port, the binding manager's own deadline may be replaced by it, provided
  every property above still holds.

## Evidence (design-level, the D3 evidence branch)

The branch `500-design-evidence` carries amended prototypes of both pinned
modules, each generated from its pinned source by declared amendments only
(`KL_pp_nvm_port.amended.proto.sv`, `KL_acmp_nvm_shadow.amended.proto.sv`),
and the cases, each at the commit the page names:

- H1 to H8 and V18: a device error on a record's header lane in both
  passes, in one pass, at the first record, a map record, the last name,
  and on a sole saved record; the D3 walk aborts (cause 2) to complete
  defaults, never blank. C01 (a zero-byte err read as blank), C02 (the port
  reporting UNFRAMED for every err, the pinned port's information) and C03
  (UNFRAMED read as a device error, which fails the blank first boot V10)
  are killed.
- W16: a device error on the binding record's header fails the binding walk
  (cause 2), nothing preloaded; B02 (issue 20's defect) is killed. B04 (an
  UNFRAMED binding header failing the walk) is killed by V10.
- W13: the binding walk's first read silent for ever: the binding walk ends
  within its deadline (cause 3), the D3 walk ends at its own deadline on
  defaults, commands are served, the port stays quarantined and the later
  SET pending. W13b: released just before the deadline, the binding comes
  back. W13c: released just after, drained, nothing preloaded, the later
  SET persists. W15: released after the entity was enabled, drained, no
  preload after enable. B01 (no deadline) and B03 (the abandoned binding
  read not drained) are killed.

## Acceptance

- The processor's port suite: each header-phase error path (grant error,
  device error during the header, short header, device error while waiting)
  reports DEVICE; an erased and a corrupted header delivered whole report
  UNFRAMED; a commit whose header fails the gate reports UNFRAMED; done
  reports 0. Deleting the cause register, or collapsing it, reddens a case.
- The binding manager's suite: a zero-byte DEVICE err fails the walk whole
  with no preload; a zero-byte UNFRAMED err keeps the per-record default and
  the walk completes (the existing A2, F4 and G2 arms stay green); silence
  in `H_RS_REQ` and `H_RS_STREAM` fails the walk within `RS_TMO_CYC_P`
  cycles with the cause 3 and abandons an issued read; a response one cycle
  before the deadline completes the walk; one after it is drained.
- The drain in the arbiter is exercised with the binding manager: a late
  response after the abandonment reaches no manager, and the port serves
  the next operation only after the device ends the drained one.

## Cost (out-of-context estimates, the page's section 12)

The amended port measures 201 LUT and 118 FF against the pinned 197 and
116; the amended binding manager 1,147 LUT and 1,115 FF against 1,040 and
1,081 at 1x1, and 1,222 and 1,157 against 1,119 and 1,123 at 8x8. The
increments, +4/+2 and about +105/+34, are differences of two out-of-context
syntheses: estimates, not bounds.
