<!-- Draft by A151 for the manager to file. Repository: kebag-logic/milan-fpga. Under #70; one lane per stage, each after the matching processor pin. -->

# Saved state D3 in the parent: glue, firmware order and the cold-cycle proof, per stage

## Objective

Consume each processor stage (T1, T2, T3) and prove it on silicon with a
cold power cycle driven from a controller host.

## Authority

`docs/design/SAVED_STATE_MATERIALIZATION.md` sections 5.2, 5.3, 8, 10;
`docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` obligations O1 to O4;
`REQUIREMENTS.md` section 1; issue #70.

## In scope, per stage

1. The pin bump; `KL_pp_shadow.sv`: `pend_i = (|nvm_unflushed_o) |
   d3_unflushed_o` plus the sticky class-6/7 bit for the classes no stage has
   retired yet (class 7 leaves with stage 2, the bit is deleted with stage
   3); `alarm_i` and the restore verdicts from the processor's combined
   outputs.
2. Stage 1 only: `milan_init` loads the AEM image before `nvm_boot`; the
   ledger fact `firmware_boot_order`, the order block of
   `docs/integration/BAREMETAL_FIRMWARE.md` and `nvm_boot`'s comment move with
   it (`scripts/check_feature_status.py`).
3. `tb/verilator/nvm_cosim`: the design's cases for the stage against the
   shipping backend and writer (the clear rule orderings, the restore cases,
   the tracked-glue controls), and the grant-cycle collision case.
4. `docs/reference/REGISTER_MAP.md` PP_STAT rows: restore done, fail and blank
   mean both walks; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` section 1.7
   and the feature ledger move only with the silicon proof.
5. Silicon: set the stage's values from a controller host, read PP_STAT to
   durable (backed 1, dirty 0, stale 0, pend 0), remove power at the outlet
   for 8 s, read every value back with GET commands; set IDENTIFY and prove it
   returns 0; a second cycle after changing a value back.

## Acceptance

The stage's co-simulation green with its mutants red; the full local bar of
`CONTRIBUTING.md`; post-place area at both shipped shapes against the
design's section 12 row; the silicon table of step 5 recorded on #70 with the
build identity.

## Dependencies

The processor pin of the stage. T5 decides the 8x8 map record before stage 3
claims 8x8 map persistence.
