<!-- Draft by A151 for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. Opens only after the #500 contract (docs/design/SAVED_STATE_MATERIALIZATION.md in kebag-logic/milan-fpga) is accepted by two independent reviews. -->

# Saved state, stage 1: one record writer for the dynamic-state selectors, sharing the NVM port with the binding manager

## Objective

Materialize the configuration index, sampling rate, clock source, stream
formats in and out and presentation time offset (records `0x00`, `0x02`..,
`0x0A`.., `0x30`.., `0x40`.., `0x50`..: 9 at the parent's 1x1 shape, 30 at
8x8) into F07.8 records through `KL_pp_nvm_port`, and restore them before
`entity_enable`. Today nothing writes them: `aecp_dyn_dirty_o` is a sticky
level with no consumer but the parent's pending bit (issues 61, 63, 83).

## Authority

- The accepted design: kebag-logic/milan-fpga
  `docs/design/SAVED_STATE_MATERIALIZATION.md` sections 3, 5.1, 6, 7, 8,
  and the evidence it cites (branch `500-design-evidence`, commit
  `a21b165ac1c671d10cba7255beaf75cea0f81d18`: the prototype
  `KL_aecp_nvm_writer.proto.sv` and `KL_pp_nvm_mgr_arb.proto.sv`).
- `docs/architecture/07_memory_maps.md` section 5 (F07.8, F07.9).
- Milan v1.2 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.11.1; the configuration
  index is design-affirmative (07 section 5.1).

## In scope

1. `KL_aecp_nvm_writer`, in or beside `KL_aecp_engine`, for selectors 0 to 5:
   the state-bus client, `own` and the dispatch hold-off, the change snoop on
   the uCPU's accepted writes, the per-record dirty bits with the clear rule
   (taint, set wins on the done edge, per group AND index), the debounce
   (`DEB_TICKS_P`), bounded retry and a sticky alarm.
2. `KL_pp_nvm_mgr_arb` in front of `KL_pp_nvm_port`: the binding manager is
   manager 0; `m0_busy` covers the writer's grant cycle (design section 6.4).
3. The two-pass restore for these records after the binding walk: pass 0
   proves no stream torn, pass 1 applies by the SET programs' rules
   (configurations_count, the sampling_rates list, clock_sources_count, the
   gather kind 0 selector 15 "supported" bit, bit 31 of the offset). A
   restore write is not a change.
4. Exports: `d3_unflushed_o`; `nvm_alarm_o` both managers; `restore_done_o`,
   `restore_fail_o`, `restore_blank_o` both walks.
5. If the #500 contract review accepted its UNRESOLVED 1: update F07.9 in
   `07_memory_maps.md` from "COMMIT + NVM_MARK" to the live write, and say
   that the marks stay for notification.

## Out of scope

Names (T2), maps (T3), the parent glue and firmware (milan-fpga T4), any
change to the binding manager's behaviour or to `KL_pp_nvm_port`.

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
- Restore: rows proven cleared before the restore (valid flags 0), a stale
  store control, a refused value falls back to the image default, a
  corrupted record falls back per record, a torn stream applies nothing,
  blank means neither walk validated a record.
- Every mutant of the design's section 7.2 and 8 that applies to these
  records is killed by a named check; deleting the trigger of any one group
  alone reddens a case.
- Obligations O1 to O4 of the snapshot contract hold: the writer writes no
  control-face register, and comes up only after the restore walk.
- Area: out of context at both parent shapes, below the design's section 12
  row for the whole writer (2,312 LUT at 1x1, 2,925 at 8x8, 0 RAMB36).

## Validation

`./scripts/run_suites.sh` exit 0 with the new suite; `./scripts/lint_hdl.sh`
exit 0; the mutation list of the suite each red.

## Dependencies

The #500 contract acceptance. The parent consumes the pin in milan-fpga T4.
No conflict with processor issues 14, 15, 20 or PR 26 lanes beyond the
arbiter in front of the port.

## Unresolved

The writer debounce value (T-NVM-DEBOUNCE is open in the parent's saved-state
page section 14); whether the restore reuses the SET programs by replay
instead of re-coding their rules (#500 UNRESOLVED 4).
