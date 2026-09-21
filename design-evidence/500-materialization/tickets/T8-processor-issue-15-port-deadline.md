<!-- Draft by A152, rewritten by A153 and revised by A154 for the manager to file as a NEW processor issue (Mister-M-alt/protocol-processor-control-plane-avb-milan) that references issues 15 and 20. It closes neither, amends neither issue's criteria, and changes neither's scope or owner. The file keeps its name so existing citations resolve. -->

# Prerequisites of D3 stage 1: the port's terminal cause, a bounded binding walk and the listener's boot-owned admission

## Why this is a prerequisite

kebag-logic/milan-fpga #500 proposes the D3 materialization contract
(`docs/design/SAVED_STATE_MATERIALIZATION.md`). Its restore is a transaction:
a transport failure in either pass ends with complete defaults and a failure
verdict. Three pinned facts break that, and the contract makes their fixes
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
3. The binding walk's PRELOAD phase waits on `KL_pp_acmp_listener`'s
   `pre_ready_o`, which the listener lowers while a START/STOP request, a
   dispatch transaction, a pending timer expiry or a talker event is present
   (its X_IDLE ranks them all above the preload). A talker event held as a
   level keeps the walk, and with it every AECP command, waiting for ever
   with an idle persistence port (round-three review R217 R3-F1). Every
   listener walk also ends in a record write-back the binding manager
   captures as a live change: during the restore, even a read-only
   GET_RX_STATE of a sink whose record was stored and not yet preloaded
   withdraws its restored binding, and the unbound record is flushed over
   the saved one.

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

## S3: a bounded binding walk, its read phase

The binding manager bounds the READ phase of its restore walk (waiting for
the port idle in `H_RS_REQ`, and for a byte, done or err in
`H_RS_STREAM`) by a no-progress deadline, `RS_TMO_CYC_P` cycles. Expiry
fails the whole walk as above and, when a read was issued, abandons it:
`nvm_abort_o` pulses and the manager arbiter in front of the port (the D3
contract's `KL_pp_nvm_mgr_arb`) DRAINS it, holding rready, swallowing the
late bytes and the done or err, and granting no manager until the device
ends that read. A new `restore_cause_o[1:0]` reports 1 torn, 2 a device error
with nothing forwarded, 3 the deadline.

## S4: the listener's boot-owned admission, the walk's preload phase

A new `KL_pp_acmp_lsn_admit` in `protocol_processor_top`, in front of the
listener's four work faces; the listener itself is unchanged:

- It OWNS the faces from the hard reset (`rst_n`) and RELEASES them once,
  when the binding manager's walk is at its terminal (`restore_done_o`, done
  whether it failed or not), no preload is presented, the listener is idle
  (`dbg_busy_o` low) and its last A4 discovery strobe (`act_disc_arm_o`) has
  left. The manager never walks again before a reset, so the gate never
  owns the faces again before one.
- While it owns them, the dispatch transaction and the event router's
  talker event are HELD at their producers: the valid towards the listener
  AND the ready towards the producer are masked, so the ACMP head stays in
  its dispatch queue (and is not admitted to the scoreboard) and the
  router's sticky latch stays set; nothing is consumed that the listener
  did not see. On those two faces ready is an acceptance, so both sides
  are masked.
- The AECP engine's START/STOP request has its VALID masked, and the
  listener's completion (`strm_set_ready_o`, `strm_set_error_o`) passes to
  the engine unmasked. That face is not an acceptance handshake: the engine
  holds its request until the completion, which the listener raises once
  the record commit or the no-op check is done (error when its bounded wait
  expires), and the listener captures a presented request into its holder
  in any state. The holder and its done and fail flags reset to 0 and fill
  only from a presented request. The gate and the listener take the same
  hard reset and neither takes the D3 roll-back, so from reset to the
  release the holder stays empty and no completion can fire: a passed
  completion never answers a request the listener did not capture, and
  masking it as well would change nothing while the gate owns the faces.
  In the product the engine presents no START/STOP request before the D3
  terminal anyway, because the D3 writer holds AECP dispatch from reset.
- The timer expiry bus does not reach the listener, and every expiry of a
  listener owner that arrives is counted: none can be legitimate, because
  the listener arms timers only in the walks the gate holds off and the
  timer service's armed bits reset to 0.
- `released_o` is the binding walk's END: the listener's live ACMP work
  and the D3 writer's walk start on it, and `restore_done_o` (both walks),
  which releases the entity enable, takes it. No enable can therefore
  precede the last preload's record write and discovery arm.

What follows from it: from reset to the release the listener's only
reachable states are X_INIT, X_IDLE and X_PRELOAD, so `pre_ready_o` is 1 in
every X_IDLE cycle and a preload is taken in the cycle it is presented. The
preload phase lasts at most four cycles a sink plus four, the release at
most four cycles after the manager's terminal. An ACMP command, a talker
event or a START/STOP request that arrives before the release is served
after it, ordered after the restored image: a live change still
wins, by coming later, and a read-only command no longer withdraws a
restored binding. A boot that never starts the binding walk leaves the
listener owned until reset, as it leaves AECP dispatch; the parent's
firmware starts the walk on every boot path (milan-fpga T4).

Three release points, each its own (the integration clarification on the
contract, milan-fpga PR #503 comment 5762146376), stated the same in T1,
T4 and the page's section 8.1:

- S4's release, the binding walk's drained terminal, releases the
  listener's four work faces. From it the listener does LIVE ACMP work
  while the D3 walk runs and before the entity is enabled: the held and
  later ACMP commands, ADP's talker events, the expiries of the timers its
  live walks arm, and START/STOP requests once AECP runs. Its record
  write-backs, which the binding manager persists as live changes, its
  discovery arms and its PDUs are live service on the restored image, not
  late restore actions: no preload is presented after the release, and
  every preload's record write and discovery arm precede it.
- The D3 terminal, COMPLETE or DEFAULTS, releases the state bus and with it
  AECP dispatch (T1). CLOSED releases neither it nor the enable, and does
  not take the listener's faces back.
- The entity enable, the top's `entity_enable_i` AND `restore_done_o`,
  releases the ADP engine: advertising may start (F07.9). It gates nothing
  else. In `KL_adp_engine` it holds the advertise state machines in DOWN;
  the talker-discovery state machines, which feed the listener's talker
  events, are a separate path. It is not a traffic freeze.

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
- S4 promises no ACMP listener service before its release, and no
  fairness among the listener's sources after it: the listener's own
  priorities apply again at the release. A request is held, never
  consumed and dropped; what a producer does with arrivals behind a held
  head is that producer's own queue policy, unchanged.

## Evidence (design-level, the D3 evidence branch)

The branch `500-design-evidence` carries amended prototypes of both pinned
modules, each generated from its pinned source by declared amendments only
(`KL_pp_nvm_port.amended.proto.sv`, `KL_acmp_nvm_shadow.amended.proto.sv`),
the new `KL_pp_acmp_lsn_admit.proto.sv`, the PINNED listener and timer
service in its harness, and the cases, each at the commit the page names:

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
- L00 to L13 (S4), on the first and the last sink bound, at both shipped
  shapes, graded on what the LISTENER took and did: R217's held and finite
  talker-event level (L01, L02) and the same level against the later sink
  (L03); a queued EVT_TK_DISCOVERED (L03b), a polled GET_RX_STATE (L04), a
  read-only GET_RX_STATE between a sink's store and its preload (L05), a
  held STOP (L06) and START/STOP back to back (L06b), expiries every cycle
  (L07), a power cut after the first sink's preload (L08a, L08b), a BIND to
  another talker (L09), a request presented in the last owned, the first
  released and the next cycle (L10), the level with the binding read near
  and past its deadline (L11, L12), and a D3 roll-back keeping the bindings
  (L13). Every preload is taken in the cycle it is presented, the release
  follows the terminal by at most two cycles, and every held request is
  taken exactly once, after it. LG01 (the gate deleted: the pinned wiring) is
  killed by L01, where the preload waits 3,229,969 cycles until the case's
  own later GET_RX_STATE write-backs withdraw both preloads, and by L05,
  where the restored binding is flushed unbound; LG02 (ready masked, valid
  admitted), LG03 (valid masked, ready passed), LG04 (expiries admitted)
  and LG05 (START/STOP admitted) are each killed. The tracked build (the
  pinned wiring) fails L01's bound and L05's binding survival, as it must.

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
- The admission, with the REAL listener and the real binding manager (the
  `acmp_nvm` suite's wrap, or `pp_top`): a talker-event level, a polled and
  a single transaction, a START/STOP request and listener-owner expiries,
  each from reset and against the later sink, never delay a preload offer
  by more than a cycle and never leave the walk without its terminal; no
  listener state but X_INIT, X_IDLE and X_PRELOAD and no timer arm, TX
  allocation, RX free, settle, teardown, disarm or notify while owned; each
  held request is popped by its producer exactly when the listener takes
  it, all at or after the release, including a request presented in the
  last owned cycle; a read-only GET_RX_STATE between a sink's store and its
  preload leaves its saved binding in NVM; a power cut inside the preload
  phase writes nothing; the release follows the last preload's record
  write and discovery arm; no START/STOP request is captured and no
  completion fires while owned, and one held from reset completes once,
  after the release; the listener serves a command after the release and
  before the D3 terminal and the enable; deleting the gate, or masking only
  one side of a transaction or talker-event handshake, or admitting
  expiries or START/STOP, reddens a case.

## Cost (out-of-context estimates, the page's section 12)

The amended port measures 201 LUT and 118 FF against the pinned 197 and
116; the amended binding manager 1,147 LUT and 1,115 FF against 1,040 and
1,081 at 1x1, and 1,222 and 1,157 against 1,119 and 1,123 at 8x8. The
admission gate alone measures 13 LUT and 17 FF at 1x1 and 14 and 17 at 8x8,
16 of those flops its diagnostic count of refused expiries; the pinned
listener with the gate in front measures 2,187 LUT and 1,547 FF against the
listener alone's 2,174 and 1,530 at 1x1, and 2,276 and 1,574 against 2,268
and 1,557 at 8x8. The increments, +4/+2, about +105/+34 and +13/+17 or
+8/+17, are differences of two out-of-context syntheses: estimates, not
bounds.
