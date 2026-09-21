<!-- Draft by A151, revised by A152, A153 and A154, for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. Opens only after the #500 contract (docs/design/SAVED_STATE_MATERIALIZATION.md in kebag-logic/milan-fpga) is accepted by two independent reviews, including its requested amendment of the mark-based wording (page section 15 item 1), and after its prerequisites T8 and T9. -->

# Saved state, stage 1: one record writer for the dynamic-state selectors, with a contained restore

## Objective

Materialize the configuration index, sampling rate, clock source, stream
formats in and out and presentation time offset (records `0x00`, `0x02`..,
`0x0A`.., `0x30`.., `0x40`.., `0x50`..: 9 at the parent's 1x1 shape, 30 at
8x8) into F07.8 records through `KL_pp_nvm_port`, and restore them as a
transaction before the entity is enabled. Today nothing writes them:
`aecp_dyn_dirty_o` is a sticky level with no consumer but the parent's
pending bit (issues 61, 63, 83).

## Authority

- The accepted design: kebag-logic/milan-fpga
  `docs/design/SAVED_STATE_MATERIALIZATION.md` sections 3, 5.1, 6, 7 and 8
  (8.6 the restore transaction, 8.8 deadlines and containment), and the
  executable evidence the page names (branch `500-design-evidence`: the
  prototypes `KL_aecp_nvm_writer.proto.sv`, `KL_pp_nvm_mgr_arb.proto.sv`,
  `KL_aecp_desc_mem_guard.proto.sv` and `KL_pp_acmp_lsn_admit.proto.sv`, the
  amended prototypes of the port and the binding manager, the pinned
  listener and timer service they run with, the run script, its results).
- `docs/architecture/07_memory_maps.md` section 5 (F07.8, F07.9).
- Milan v1.2 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.11.1; the configuration
  index is design-affirmative (07 section 5.1).

## Prerequisites

- The #500 contract acceptance, with the amendment of the mark-based
  wording recorded (page section 15 item 1). Until it is, this ticket's item
  8 cannot land.
- T8 (a new processor issue, referencing issues 15 and 20): the port's
  terminal cause (S1), the binding manager's bounded read phase (S3) and
  the listener's boot-owned admission (S4), which bounds the preload phase
  and gives the binding walk the drained terminal this stage starts from.
  This stage's restore consumes the cause, and its dispatch hold from reset
  is acceptable only with a binding walk that ends, preload phase included
  (the parent's `SAVED_STATE_FASTCONNECT.md` section 9.3: AECP keeps being
  answered when persistence wedges). The lane may start on T8's reviewed
  interface; it does not merge before T8 lands in the same pin or an
  earlier one.
- T9: response isolation on the descriptor store's memory face (S2). This
  stage's value rules, its roll-back and its re-walk read the descriptor
  store. Same rule as T8.
- The parent's firmware change 1 (milan-fpga T4, stage 1): the AEM image
  loaded before `nvm_boot`. Without it the restore cannot prove its image
  and ends CLOSED, the entity never enabled (the evidence's F01).
- Before this stage is DECLARED SHIPPABLE: kebag-logic/milan-fpga #502,
  truthful pending from the first accepted live write for the two classes
  no stage has materialized yet (maps and names). This ticket may be
  implemented and merged before; it may not be released as a shipped stage.

## In scope

1. `KL_aecp_nvm_writer`, in or beside `KL_aecp_engine`, for selectors 0 to 5:
   the state-bus client; `own` and the dispatch hold-off, with `own` held
   FROM RESET until the restore's terminal; the change snoop on the uCPU's
   accepted writes; the per-record dirty bits with the clear rule (taint,
   set wins on the done edge, per group AND index); the debounce
   (`DEB_TICKS_P`); bounded retry and a sticky alarm.
2. `KL_pp_nvm_mgr_arb` in front of `KL_pp_nvm_port`: the binding manager is
   manager 0; `m0_busy` covers the writer's grant cycle (page section 6.4);
   the DRAIN of a read either manager abandons (rready held, bytes, done
   and err swallowed, no grant to either manager until the port ends that
   read); the port's cause passed to the owning manager with its err.
3. The restore transaction for these records after the binding walk's
   DRAINED terminal, T8's S4 release (page sections 8.6 and 8.8):
   - the image proven first (a validated descriptor store, after a LOCATE of
     ENTITY 0 if needed); if it cannot be, the terminal is CLOSED (cause 7),
     never a restore;
   - pass 0 reads every record whole; a zero-byte err with the cause
     UNFRAMED is an erased or unframed record (its default stays), a DEVICE
     err with or without bytes, or a torn read, aborts;
   - the passes agree RECORD BY RECORD on which records came back whole; a
     difference aborts at that record (cause 5);
   - pass 1 applies by the SET programs' rules (configurations_count, the
     sampling_rates list, clock_sources_count, the gather kind 0 selector 15
     "supported" bit, bit 31 of the offset); a rule or an image-default
     format that cannot be FETCHED (the store's error, or its own
     4,096-cycle watchdog's answer) aborts (cause 6), never refuses the
     value;
   - every restore wait bounded by `RS_TMO_CYC_P` without progress;
   - an abort in pass 1 rolls back by a scoped reset of BOTH
     `KL_aecp_dyn_state` and `KL_aecp_desc_store` (new soft-reset inputs;
     for the store, a re-walk request that also returns its fetch watchdog
     to zero serves as well), held for at least two cycles and while the
     descriptor memory owes a burst (T9's debt: the guard takes the HARD
     reset only, never this one), bounded by the deadline, then proves the
     image by a LOCATE; it ends in DEFAULTS, or CLOSED when the image cannot
     be proven. The store's reset is a STAGE-1 owner, not a stage-2 one:
     after a fetch's response timed out, the pinned store leaves its
     watchdog at its limit, so its next fetch errs at once, and draining the
     debt alone leaves the roll-back's LOCATE failing (round-three review
     R218 R3-F1). Its re-walk also puts the image's names back, which is all
     stage 2 needs of it;
   - an abort in pass 0 ends in done and fail with nothing applied;
   - a restore write is not a change;
   - blank means done WITHOUT fail and no record validated;
   - `rs_cause_o[2:0]`: 1 torn, 2 device error, 3 deadline, 4 edit refused,
     5 passes disagree, 6 descriptor fault, 7 image not proven.
4. The descriptor store's validated-image level becomes a functional output
   (today it is the debug tap `dbg_img_valid_o`).
5. The entity enable released by the restore, as F07.9 draws it: the ADP
   engine's `entity_enable_i` becomes the top's `entity_enable_i` AND
   `restore_done_o`, where `restore_done_o` is the binding walk's drained
   terminal (T8's S4 release) AND this restore's done, so no enable precedes
   the terminal of both walks or the last preload's record write and
   discovery arm. It gates ADP advertising only; the side port's
   image-window lock keeps the top's `entity_enable_i`, as it ships. The
   three release points stay separate (the integration clarification on
   milan-fpga PR #503, comment 5762146376; T8 and the page's section 8.1):
   the listener's live ACMP work from T8's S4 release, AECP dispatch from
   this restore's terminal (`own`, item 1; COMPLETE or DEFAULTS, never
   CLOSED), ADP advertising from the combined enable. The enable is not a
   traffic freeze.
6. Exports: `d3_unflushed_o`; `nvm_alarm_o` both managers;
   `restore_done_o`, `restore_fail_o`, `restore_blank_o` both walks; the new
   `restore_rb_o`, `restore_closed_o`, `rs_cause_o[2:0]` and the binding
   walk's `restore_cause_o[1:0]` (T8).
7. The roll-back strobe `d3_rb_rst_o` exported for the stage that adds an
   owner outside the processor (T3, the parent's map plane).
8. After the amendment is recorded: F07.9 in `07_memory_maps.md` restated
   as the page's section 15 item 1 words it (the live-write trigger, the
   untainted done, the transaction and the release of `entity_enable`).

## Out of scope

Names (T2), maps (T3), the parent glue and firmware (milan-fpga T4). The
port's cause, the binding manager's amendments and the listener's admission
are T8's; the descriptor memory guard is T9's. The descriptor store's
roll-back reset is THIS stage's (item 3), not T2's. Reusable port service
after a device that never ends an abandoned operation is processor issue
15's open recovery contract, and nothing here claims it.

## Acceptance

- A suite (for example `tb/nvm_writer` and `tb/pp_top` arms with the real
  microcode) grades, per record: one change converges; a change during the
  record's WRITE is written again (taint); two changes in one window write
  once; a change to another record of the same group, and to another GROUP,
  while one is in flight both land; a change on the done edge survives; a
  failed write retries, then gives up with the alarm; IDENTIFY never
  triggers.
- The binding manager's request on the writer's grant cycle is issued and
  commits; deleting the grant-cycle term from `m0_busy` reddens that case.
- Restore: every row of selectors 0 to 5, every index, proven cleared before
  the restore (value and valid flag), with the stale-store control; every
  saved record restored with value AND valid flag; unsaved records keep
  their defaults; exact applied, refused and blank counts; a refused value
  (a rate not listed, a clock source past the count) and a corrupted record
  fall back per record with no failure; a record torn at rest is refused by
  pass 0 with nothing applied.
- The output format is graded under the product's own verdict: the declared
  format of an eight-channel output is SET, saved and replayed with its
  valid flag, a narrower one is refused both as a SET and on replay, and
  deleting the replay or the trigger reddens those cases.
- Transport failures, each with its mutant red: a read error early and late
  in EACH pass after non-default values of every stage-1 group applied; a
  DEVICE error on a record's header in both passes, in either pass alone, at
  the first record and on a sole saved record, never reported blank; a
  record whole in one pass and not the other, one difference and two that
  balance the counts; each ends in DEFAULTS with every row at its reset
  value and the cause it names. An erased first boot reports blank with no
  failure (the classification's control).
- Descriptor faults, each with its mutant red: a rule fetch failing once
  after an application rolls back (cause 6), not a refusal; the store's own
  watchdog answering a late fetch rolls back only after the late burst has
  arrived; a late burst past the deadline ends CLOSED; the image failing
  before the restore ends CLOSED (cause 7), never a restore; a descriptor
  memory failing through the roll-back ends CLOSED.
- STAGE 1 ALONE, on a slot holding stage-1 records only (the configuration
  index, a clock source and a presentation offset, every other record
  erased) and with this stage's roll-back scope (the two stores, not the
  map plane): the first rule fetch after an application answered after
  4,000 cycles (COMPLETE), 5,000 and 16,000 cycles (DEFAULTS, the owners
  out of reset only after the late burst, a GET answered on defaults and
  a later SET persisting), 30,000 cycles (CLOSED), one error beat then a
  healthy memory (DEFAULTS); an image that cannot be proven (CLOSED); a
  pass-1 read error (DEFAULTS). Deleting the descriptor store's roll-back
  reset reddens the 5,000- and 16,000-cycle cases (they end CLOSED); the
  guard's debt and its own mutants (T9) stay green and red as before.
- Deadlines: silence, a response just before and just after the deadline,
  in both passes and on the binding walk (with T8); the binding walk's
  preload phase under a held and a finite listener interference, against
  the first and the later sink (with T8's S4); the entity enable never
  precedes the terminal, including an enable requested from reset; no
  restore write after the terminal; `own` released within the deadlines
  plus the roll-back; a GET and a SET served after the recovery, the SET
  persisting once the port is free, and pending, never durable, while a
  device that never answers keeps the port quarantined.
- Per group, with both format directions separately: deleting the group's
  live-write TRIGGER alone reddens a save test, and deleting its REPLAY
  alone reddens a restore check of value and valid flag. The sampling rate
  needs a test configuration listing two rates; no shipped one does.
- Obligations O1 to O4 of the snapshot contract hold: the writer and the
  drain write no control-face register, and the writer's first device-face
  request is its own restore walk, after the binding walk.
- Area: out of context at both parent shapes, reported against the page's
  section 12 rows (the writer and arbiter 2,377 LUT at 1x1 and 3,116 at 8x8,
  0 RAMB36). Those figures are estimates, not bounds; a larger figure is
  explained, not absorbed.

## Validation

`./scripts/run_suites.sh` exit 0 with the new suite; `./scripts/lint_hdl.sh`
exit 0; the mutation list of the suite each red; the suite's runner exits
non-zero on any surviving mutant, unexpected result or case that did not
complete.

## Dependencies

The prerequisites above. The parent consumes the pin in milan-fpga T4. No
conflict with processor issues 14, 15 or 20 or PR 26 lanes beyond the
arbiter in front of the port and T8's amendments.

## Unresolved

The writer debounce value (T-NVM-DEBOUNCE is open in the parent's saved-state
page section 14); the value of `RS_TMO_CYC_P` at the product clock (the
page's 20 ms model value is a proposal, to be sized above the descriptor
store's whole walk); whether the restore reuses the SET programs by replay
instead of re-coding their rules (#500 UNRESOLVED 7).
