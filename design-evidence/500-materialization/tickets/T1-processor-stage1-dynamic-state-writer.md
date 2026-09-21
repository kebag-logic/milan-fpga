<!-- Draft by A151, revised by A152, for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. Opens only after the #500 contract (docs/design/SAVED_STATE_MATERIALIZATION.md in kebag-logic/milan-fpga) is accepted by two independent reviews, including its requested amendment of the mark-based wording (page section 15 item 1). -->

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
  prototypes `KL_aecp_nvm_writer.proto.sv` and `KL_pp_nvm_mgr_arb.proto.sv`,
  the run script, its results).
- `docs/architecture/07_memory_maps.md` section 5 (F07.8, F07.9).
- Milan v1.2 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.11.1; the configuration
  index is design-affirmative (07 section 5.1).

## Prerequisites

- The #500 contract acceptance, with the amendment of the mark-based
  wording recorded (page section 15 item 1). Until it is, this ticket's item
  7 cannot land.
- Before this stage is DECLARED SHIPPABLE: kebag-logic/milan-fpga #502,
  truthful pending from the first accepted live write for the two classes
  no stage has materialized yet (maps and names). This ticket may be
  implemented and merged before; it may not be released as a shipped stage.
- Not a prerequisite, and stated so the lane does not rely on it: processor
  issue 15. Without it the binding walk keeps no deadline, so a silent
  device during that walk keeps the entity dark and deaf (fail-closed,
  page section 8.8). This stage's own restore is bounded without it.

## In scope

1. `KL_aecp_nvm_writer`, in or beside `KL_aecp_engine`, for selectors 0 to 5:
   the state-bus client; `own` and the dispatch hold-off, with `own` held
   FROM RESET until the restore's terminal; the change snoop on the uCPU's
   accepted writes; the per-record dirty bits with the clear rule (taint,
   set wins on the done edge, per group AND index); the debounce
   (`DEB_TICKS_P`); bounded retry and a sticky alarm.
2. `KL_pp_nvm_mgr_arb` in front of `KL_pp_nvm_port`: the binding manager is
   manager 0; `m0_busy` covers the writer's grant cycle (page section 6.4);
   the DRAIN of a read the writer abandons (rready held, bytes, done and err
   swallowed, no grant to either manager until the port ends that read).
3. The restore transaction for these records after the binding walk (page
   sections 8.6 and 8.8): pass 0 reads every record whole; pass 1 applies
   by the SET programs' rules (configurations_count, the sampling_rates
   list, clock_sources_count, the gather kind 0 selector 15 "supported" bit,
   bit 31 of the offset); the passes must agree on the records read whole;
   every restore wait bounded by `RS_TMO_CYC_P` without progress; an abort
   in pass 1 rolls back by a scoped reset of `KL_aecp_dyn_state` (a new
   soft-reset input) and ends in DEFAULTS; an abort in pass 0 ends in done
   and fail with nothing applied. A restore write is not a change.
4. The entity enable released by the restore, as F07.9 draws it: the ADP
   engine's `entity_enable_i` becomes the top's `entity_enable_i` AND
   `restore_done_o`, so no enable precedes the terminal of both walks.
5. Exports: `d3_unflushed_o`; `nvm_alarm_o` both managers;
   `restore_done_o`, `restore_fail_o`, `restore_blank_o` both walks; the new
   `restore_rb_o`, `restore_closed_o` and `rs_cause_o[2:0]`.
6. The roll-back strobe `d3_rb_rst_o` exported for the stages that add
   owners (T2 the descriptor store, T3 the parent's map plane).
7. After the amendment is recorded: F07.9 in `07_memory_maps.md` restated
   as the page's section 15 item 1 words it (the live-write trigger, the
   untainted done, the transaction and the release of `entity_enable`).

## Out of scope

Names (T2), maps (T3), the parent glue and firmware (milan-fpga T4), any
change to the binding manager's behaviour or to `KL_pp_nvm_port` (processor
issue 15 owns the port's own deadline).

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
  and a corrupted record fall back per record; a record torn at rest is
  refused by pass 0 with nothing applied.
- Containment, each with its mutant red: a read error early and late in
  EACH pass, after non-default values of every stage-1 group applied, ends
  in DEFAULTS with every row at its reset value; silence, a response just
  before and just after the deadline, in both passes; a header-read error in
  pass 1 (the passes disagree); the entity enable never precedes the
  terminal; no restore write after the terminal; `own` released within
  `RS_TMO_CYC_P` plus the roll-back; a GET and a SET served after the
  recovery, the SET persisting once the port is free.
- Per group, with both format directions separately: deleting the group's
  live-write TRIGGER alone reddens a save test, and deleting its REPLAY
  alone reddens a restore check of value and valid flag. The sampling rate
  needs a test configuration listing two rates; no shipped one does.
- Obligations O1 to O4 of the snapshot contract hold: the writer and the
  drain write no control-face register, and the writer's first device-face
  request is its own restore walk, after the binding walk.
- Area: out of context at both parent shapes, reported against the page's
  section 12 row (2,311 LUT at 1x1, 2,876 at 8x8, 0 RAMB36, for the whole
  prototype writer and arbiter). Those figures are estimates, not bounds; a
  larger figure is explained, not absorbed.

## Validation

`./scripts/run_suites.sh` exit 0 with the new suite; `./scripts/lint_hdl.sh`
exit 0; the mutation list of the suite each red; the suite's runner exits
non-zero on any surviving mutant, unexpected result or case that did not
complete.

## Dependencies

The prerequisites above. The parent consumes the pin in milan-fpga T4. No
conflict with processor issues 14, 20 or PR 26 lanes beyond the arbiter in
front of the port.

## Unresolved

The writer debounce value (T-NVM-DEBOUNCE is open in the parent's saved-state
page section 14); the value of `RS_TMO_CYC_P` at the product clock (the
page's 20 ms model value is a proposal); whether the restore reuses the SET
programs by replay instead of re-coding their rules (#500 UNRESOLVED 7).
