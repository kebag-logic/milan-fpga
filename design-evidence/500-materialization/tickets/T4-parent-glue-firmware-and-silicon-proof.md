<!-- Draft by A151, revised by A152, A153 and A154, for the manager to file. Repository: kebag-logic/milan-fpga. Under #70; one lane per stage, each after the matching processor pin. -->

# Saved state D3 in the parent: glue, firmware and the cold-cycle proof, per stage

## Objective

Consume each processor stage (T1, T2, T3) and prove it on silicon with a
cold power cycle driven from a controller host.

## Authority

`docs/design/SAVED_STATE_MATERIALIZATION.md` sections 5.2, 5.3, 8, 10;
`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` obligations O1 to O4;
`REQUIREMENTS.md` section 1; issue #70.

## Release conditions, per stage

- No stage is DECLARED SHIPPABLE before #502 is closed: the pending bit must
  be truthful from the first accepted live write for both classes no
  shipped stage materializes (maps and names). A stage may be implemented
  and merged before; it is not a shipped stage until then.
- Stage 3 does not open before #501 records a conforming capacity decision
  (T3).
- No stage is released without the processor prerequisites T8 (the
  port's terminal cause, a bounded binding walk and the listener's
  boot-owned admission) and T9 (response isolation on the descriptor
  store's memory face) in its pin: the restore transaction and the AECP
  availability of the parent's `SAVED_STATE_FASTCONNECT.md` section 9.3
  depend on them.
- Each stage's release notes state the one availability limit that stays:
  a persistence device that never ends an operation the restore abandoned
  keeps the port QUARANTINED until reset. Commands are served and the entity
  is enabled on defaults with restore fail set; every later change reads
  pending, never durable. No reuse of that port is claimed (processor issue
  15's recovery contract is open).

## In scope, per stage

1. The pin bump; `KL_pp_shadow.sv`: `pend_i = (|nvm_unflushed_o) |
   d3_unflushed_o` plus the sticky class-6/7 bit for the classes no stage
   has retired yet (class 7 leaves with stage 2, the bit is deleted with
   stage 3), unless #502 has already replaced its source; `alarm_i` and the
   restore verdicts from the processor's combined outputs, with restore
   blank reported only for a restore that did not fail (a device error that
   loses the one saved record must not read as a clean first boot).
2. Stage 1 only, the firmware (`sw/firmware/milan_baremetal/milan_baremetal.c`):
   `milan_init` loads the AEM image before `nvm_boot` (MANDATORY: without it
   the restore cannot prove its image and ends CLOSED, the entity never
   enabled; the evidence's F01); `nvm_boot` starts the restore walk on
   EVERY path, the persistence-disabled one included, because the processor
   now holds the ACMP listener's work faces until the binding walk's
   drained terminal (T8's S4), AECP dispatch until the D3 walk's terminal
   and the entity enable until both (T1), and a walk never started ends
   none of them;
   the restore wait's timeout and the enable line report that the fabric
   holds the enable, and the boot reports the CLOSED terminal and the
   restore causes. The ledger fact
   `firmware_boot_order`, the order block of
   `docs/integration/BAREMETAL_FIRMWARE.md` and `nvm_boot`'s comment move
   with it (`scripts/check_feature_status.py`).
3. Stage 3 only: the map plane (`milan_datapath.sv` and
   `KL_chan_map_capture.sv`) returns every port to its reset set on the
   processor's roll-back strobe.
4. `tb/verilator/nvm_cosim`: the design's cases for the stage against the
   shipping backend and writer: the clear-rule orderings, the restore cases,
   the transaction and deadline cases of page sections 8.6 and 8.8 on both
   walks, the listener's admission cases with the pinned listener, the
   stage-1 descriptor cases on a stage-1 slot, the tracked-glue controls
   and the grant-cycle collision case; its runner exits non-zero on any
   verdict failure and counts no kill from a run that did not complete.
5. `docs/reference/REGISTER_MAP.md`: PP_STAT restore done, fail and blank
   mean both walks (blank only without fail), a D3 roll-back reads done and
   fail, new rows carry the closed terminal and the causes (D3: 1 torn, 2
   device error, 3 deadline, 4 edit refused, 5 passes disagree, 6 descriptor
   fault, 7 image not proven; binding walk: 1 torn, 2 device error with
   nothing forwarded, 3 deadline), and PP_CTRL[0] and ADP_CTRL[0] request the
   enable, which the fabric releases at the restore's terminal. The enable
   starts ADP advertising and freezes no traffic: the listener's live ACMP
   work starts at T8's S4 release and AECP at the D3 terminal, three
   separate release points (the integration clarification on PR #503,
   comment 5762146376; the page's section 8.1).
   `docs/reference/MILAN_COMPLIANCE_MATRIX.md` section 1.7 and the feature
   ledger move only with the silicon proof.
6. Silicon: set the stage's values from a controller host, read PP_STAT to
   durable (backed 1, dirty 0, stale 0, pend 0), remove power at the outlet
   for 8 s, read every value back with GET commands; set IDENTIFY and prove it
   returns 0; a second cycle after changing a value back.

## Acceptance

The stage's co-simulation green with its mutants red; the full local bar of
`CONTRIBUTING.md`; post-place area at both shipped shapes reported against
the page's section 12 row (an estimate, not a bound); the silicon table of
step 6 recorded on #70 with the build identity.

## Dependencies

The processor pin of the stage and the release conditions above.
