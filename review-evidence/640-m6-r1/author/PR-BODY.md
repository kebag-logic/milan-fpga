[A591]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `ee0fc6fd9`: full sweep 61 suites, 2,185,957 checks, 0 in-suite failures (one external kill of `crf_rx`'s mutant driver, re-run green); `milan_dp_gptp` 197/0; 59 repository gates rc 0; route gate PASS. `640-m6` -> `dev`.

## Linked Issue / roles

Relates to #640

Lane M6 of the Mark II area plan (L9, media context tables). It must not close #640.

Executor: `[A591]`
Internal cleared-context reviewer: `[R600]`
External reviewer: `[R601]`

## Description

Two of the four L9 blocks change their storage form, with identical function.
The register map, the wire format, every parameter default and the shipping behaviour are unchanged.

| Piece | Change |
|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` | The two waiting PDU bundles and the one in service share one 4-entry LUT-RAM ring with one write port, instead of a 2-entry flop queue plus an in-service flop copy. Capacity is unchanged (`penq_w` still refuses a third waiting bundle). The GET_COUNTERS port reads ONE counter by sink and column (`diag_col_i`, `diag_q_o`) from one `N x 16` write-through LUT-RAM table, instead of presenting all twelve counters of a sink at once. |
| `hdl/milan/milan_datapath.sv` | The STREAM_INPUT GET_COUNTERS quadlet index names a monitor column; quadlet 32 is still `counters_valid` and every other quadlet still reads 0. The word multiplexer is gone: the column is part of the LUT-RAM read address. |
| `hdl/ieee1722/aaf/KL_chan_map_capture.sv` | Every channel resolves through one flat source table (silence, I2S L/R, tone, each TDM pair's L/R, each loopback hold pair's L/R) with one indexed read, instead of a bucket -> pair -> half resolver per channel. The commit skid keeps a 2-bit form and a 2-bit beat slot per entry; a 4-slot LUT-RAM beat bank holds each admitted beat's `{stash-or-0, smp0, smp1}` once. Capacity, order, refusal and flush-kill are unchanged. |
| `hdl/milan/KL_pp_shadow.sv` | One comment names the new port. |
| `tb/verilator/avtp_rxmon` | Lockstep leg against the dev `e8454e27` module (`reference/`, only the name changed) at N=1 and N=8: every output and one GET_COUNTERS read compared every cycle, plus four read-modify-write hazard cases. `lockstep_mutants.py` plants a lost increment, a torn read, a wrong stream index and a missed reset; each must fail its named check. |
| `tb/verilator/chmap_capture` | Lockstep leg against the dev `e8454e27` module at 4 slots/1 loopback stream and 32 slots/8 streams, with source-table and skid cases. `lockstep_mutants.py` plants a wrong row decode, a reused beat slot and a swapped commit form. |
| `tb/verilator/capture_coherence/mutants.py` | Its two TDM junction mutants re-anchored on the source-table line (same defects, same expected break). |
| `scripts/measure_test_evidence_readers.py` | Reader dispositions for the two new mutation campaigns. |
| Docs | `docs/testing/TESTING.md` suite rows; `docs/design/MARK_II_AREA_PLAN.md` "M6 intermediate measurement" and an L9 pointer; `docs/design/AREA_BUDGET.md` note. |

`KL_render_setpoint` is unchanged: its storage is already distributed RAM.
`KL_talker_diag_ctx` is unchanged: its counters all update in parallel at the interval tick, so a RAM form would need a serialising walker and would change timing.

Measured (M0s recipe, one route under the host lock, gate `check --endpoint route-1x1` PASS):

| Measurement | LUT | FF | Slices | RAMB36 / RAMB18 | WNS / WHS, ns |
|---|---:|---:|---:|---:|---|
| Base route, dev `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | +0.299 / +0.031 |
| M6 route, `930340145` | 49,561 | 53,455 | 15,791 | 74 / 27 | +0.141 / +0.018 |
| Routed delta | -706 | -958 | +12 | 0 / 0 | -0.158 / -0.013 |

Saving against the plan's 600 (400-900), honestly:

- reproducible, the two changed blocks: 418 LUT post-synthesis, 468 routed, 839 FF;
- out of context, the changed modules at 1x1: 552;
- whole image: -706 routed, but that includes -333 in the unchanged protocol processor and other untouched blocks moving both ways, which is not credited.

All three figures sit low in the range, below the 600 central estimate. No block-RAM tile is added. The gate record is not re-recorded (D7: M9 re-records).

## Authoritative references

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098405082
- `docs/design/MARK_II_AREA_PLAN.md`, "L9 Media context tables", the ledger and the firmware block-RAM ledger
- `docs/design/AREA_BUDGET.md` (resource gate policy, D7)
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (M0s recipe, resource gate)
- Decisions D1, D3, D7, D8: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268
- Milan v1.2 Tables 5.4 and 5.6, 5.4.2.25 (GET_COUNTERS); IEEE 1722.1-2021 7.4.42

## How to get into the same state

```sh
git fetch origin
git checkout 640-m6
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

The pinned Verilator is 5.050; hosted CI uses CPython 3.12.3 and GNU make 4.3.

## How to validate

```sh
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/chmap_capture
make -C tb/verilator/tkdiag
make -C tb/verilator/render_setpoint
make -C tb/verilator/milan_dp
make -C tb/verilator/capture_coherence
python3 scripts/lint_rtl.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Expected result / pass criteria: every command exits 0. The two lockstep legs print `failures: 0` at both shapes, and each `lockstep_mutants.py` ends with every mutant caught (`5 checks: 5 PASS, 0 FAIL` and `4 checks: 4 PASS, 0 FAIL`).
The integrated route follows the recipe's "Integrated measurements" and "Resource gate" sections; `check --endpoint route-1x1` prints `RESULT: PASS`.

## Known limitations / out of scope

- The saving is below the plan's 600 central figure (418 reproducible). Folding the talker counters' read multiplexer into a column read, as for the monitor, is estimated at 30 to 50 LUT more; it is not in this lane.
- Untouched blocks move by hundreds of LUTs between the two images; that movement is reported and not credited.
- The resource gate record is unchanged (D7).
- The standalone `ooc-1x1` and `ooc-8x8` endpoints were not re-run: their 50-file source set differs from dev `e8454e27` only by one comment line in `KL_pp_shadow.sv`, with all submodule pins unchanged.
- The route measured the export of `930340145`. Later commits change only tests, a test-evidence reader table and docs, so the RTL is identical.
- `tsn_fuzz` declares its four field-campaign skips (tsn-gen absent on the measuring host), as on dev.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (the saving is reported against the estimate, low in its range)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
