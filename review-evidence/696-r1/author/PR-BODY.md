[A570]

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

GREEN locally, review ready at `030eb98a12685a2ca41cf8d785bb0eb69dc32a98` — `696-maap-annexb` -> `dev`.

The branch merges dev `8b61b709` (merge commit `0df48637`, no rebase). At that merge result:
61/61 parent suites (2,185,905 checks), the parser (0 findings), portability (58/58 tops), lint (90 <= 90),
404 behaviour scenarios, 94 documentation and static commands, and the pinned field campaigns (AAF 164, gPTP 677) all pass.
The MAAP suite passes 171 unit checks and 3 real-datapath checks. Its campaign catches 49/49 planted defects and passes both controls.
Coverage is 215/215 lines, and the differential passes 12/12 cases and catches 17/17 defects.

All three resource endpoints, measured through the recipe at the merge result, pass the gate and are re-recorded:
`route-1x1` LUT 50,230 (-37), FF 54,308 (-105), slice 15,823 (+44), storage and DSP unchanged, WNS +0.114 ns, WHS +0.036 ns, fully routed;
`ooc-1x1` and `ooc-8x8` keep every recorded figure. The MAAP block measures 445 LUT / 340 FF, +6 / +60 against the base, within its ceiling.
The documentation set passes again at the final head.

## Linked Issue / roles

Closes #696

Executor: `[A570]`
Internal cleared-context reviewer: `[R558]`
External reviewer: `[R559]`

## Description

The fabric MAAP allocator (`KL_maap`) closes the Annex B deviations left after #686:

| Item | Clause | Change | Check and planted defect |
|---|---|---|---|
| M4 | B.3.4 NOTE; B.3.6.1 | Seed sampled from the programmed MAC at first enable, not at reset | Real-datapath check: two MACs draw different intervals; `m4_reset_time_sampling` caught |
| M2 | B.3.6.6 | DEFEND echoes the PROBE's requested start and all sixteen count bits | Two named checks; two defects caught |
| M7 | B.4; Table B.9 | A supplied range outside the dynamic pool is refused (bounded draw instead) | Boundary checks; two defects caught |
| M8 | B.2 | Truncated PDUs are discarded with no state, timer or TX effect; counting withdrawn by ruling | Cycle-matched comparison with idle RX; two defects caught |
| M1 | Table B.7 note d; B.3.6.4 | MAC comparison in the rProbe!/PROBE and rDefend!/DEFEND cells | Both cells; two defects caught |
| M5 | B.3.5.9; Table B.7 | Rising link revokes and re-probes; wired from the existing effective link | Unit and real-datapath checks; three defects caught |
| M6 | Table B.7; B.3.6.6 | One shared buffer keeps a DEFEND pending while PROBE or ANNOUNCE drains | Four named checks; five defects caught; one-response capacity documented |
| M3 | B.3.6.1 | 32-bit generator, period 2^32 - 1, seeded at first enable from MAC plus the existing PHC; continues across Release/Begin | Six defects caught, one through the real datapath; pool-fold bias documented |

The firmware differential programs 1,024 MAC identities before first enable and keeps every timing bound and both draw assertions.
A MAC-ignoring generator draws only 5,220..5,710 cycles and fails the unchanged highest-draw check (at least 5,790).

MAAP area with the assignment's instrument (`syn/ooc/milan_datapath_ooc.tcl`, one thread):

| Item | MAAP LUT | MAAP FF | LUT vs base | FF vs base |
|---|---:|---:|---:|---:|
| Base `6aa25dec` | 439 | 280 | 0 | 0 |
| M4 | 460 | 281 | +21 | +1 |
| M2 | 473 | 297 | +34 | +17 |
| M7 | 483 | 297 | +44 | +17 |
| M8 | 498 | 298 | +59 | +18 |
| M1 | 491 | 298 | +52 | +18 |
| M5 | 456 | 299 | +17 | +19 |
| Original M6 (replaced) | 518 | 380 | +79 | +100 |
| Shared-buffer M6 | 457 | 324 | +18 | +44 |
| M3 (lane head before the merge) | 441 | 340 | +2 | +60 |
| Dev `8b61b709`, no lane change | 443 | 280 | +4 | 0 |
| Merge result `0df48637` | 445 | 340 | +6 | +60 |

Ruling 6079087547 sets the ceiling at +60 LUT / +60 FF on `g_maap.maap_engine`; the FF allowance is fully used.
In the routed image the engine uses 425 LUT / 339 FF. Its worst incoming setup path keeps +4.037 ns and its worst outgoing path +6.719 ns.

Resource records: `e6f00121` writes the three merge-result measurements with `record --write`; every policy value is unchanged.
`030eb98a` updates the area budget's record table and adds the re-baseline section to the #234 findings.
Before the merge, the lane head routed at +0.029 ns WNS on a soft-CPU DMA path and was not recorded (ruling 6089712293).
At the merge result the worst path is in the SDRAM controller, at +0.114 ns.

No register-map, filter, mailbox, submodule-pin or state-encoding change.

## Authoritative references

- IEEE 1722-2016 Annex B: B.2, B.2.1, B.2.7, B.2.8, B.3.4, B.3.5.9, B.3.6.1, B.3.6.3, B.3.6.4, B.3.6.6, B.4, Tables B.7 and B.9.
- REQUIREMENTS.md sections 1 and 8; FR-MAAP-01.
- docs/design/MAAP_FABRIC.md; hdl/ieee1722/maap/doc/KL_maap/KL_maap.md.
- Issue #696: assignment 6076750392 and rulings 6076940309, 6079087547, 6079463350, 6080332335 and 6089712293.
- docs/testing/PP_SHADOW_BASELINE_RECIPE.md; docs/design/AREA_BUDGET.md; docs/findings/234_PP_SHADOW_AREA_BASELINE.md.

## How to get into the same state

```sh
git fetch origin
git checkout 696-maap-annexb
git rev-parse HEAD   # 030eb98a12685a2ca41cf8d785bb0eb69dc32a98
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
: "${WORK:?Set an empty disk-backed scratch directory}"
: "${VERILATOR:?Select the pinned 5.050 executable}"
: "${MILAN_RV32_CC:?Select the verified RV32 compiler}"
export TMPDIR="$WORK" VERILATOR VERILATOR_JOBS=2 MILAN_RV32_CC
```

Use the pinned documentation environment and matching coverage reader.
Set `FIELD_GENERATOR` to the clean tsn-gen revision pinned by `.github/workflows/rtl.yml`, with its packet generator built.

## How to validate

```sh
make -j8 -C tb/verilator/maap MDIR="$WORK/unit"
make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration" && "$WORK/integration/maap_integration"
make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage"
python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/differential"
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2
bash scripts/run_all_suites.sh "$WORK/parent-suite-logs"
TSN_GEN_ROOT="$FIELD_GENERATOR" make -j8 -C tb/verilator/tsn_fuzz
bash syn/yosys/run.sh --results "$WORK/portability-results"
python3 scripts/lint_rtl.py --check --self-test --jobs 2
(cd tests && behave --no-capture -f plain)
python3 scripts/xvlog_gate.py --check
python3 scripts/docs_check.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/measure_test_evidence.py --check
python3 syn/ooc/pp_resource_gate.py check-baseline
```

Measure the three endpoints with the [baseline recipe](docs/testing/PP_SHADOW_BASELINE_RECIPE.md), `--single-thread-synthesis`,
and `--integrated-clock` for both standalone runs, with no other heavy job beside Vivado. Then:

```sh
python3 syn/ooc/pp_resource_gate.py check "$ROUTE" --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check "$OOC_1X1" --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check "$OOC_8X8" --endpoint ooc-8x8
```

Expected result / pass criteria: every command exits 0.
- The MAAP suite reports 171 checks and the datapath 3 checks, all with 0 failures.
- The campaign reports 51 rows: 49 defects exit 1 at their named check, and the two clean controls exit 0.
- Coverage is 215/215 lines. The differential passes 12/12 cases and catches 17/17 defects.
- The parent sweep reports 61/61 suites, and its four field-campaign skips are covered by the separate `tsn_fuzz` run.
- Each endpoint check prints `RESULT: PASS` against the committed records.
- The field campaign rewrites only the timestamp line of its two generated result pages; discard that change.

## Known limitations / out of scope

- M6 stores one pending or transmitting response. Further PROBEs while occupied remain unsupported, including during DEFEND.
  Full Table B.7 conformance is not claimed. B.3.6.6 defines the response action; B.3.6.3 defines probe-count decrement.
- M3 corrects period and seeding; the pool mapping remains biased under B.3.6.1.
- M8 counting needs a register-map change and was withdrawn by ruling; truncated PDUs are discarded without effect.
- Tagged MAAP reception remains outside this correction lane.
- The MAAP FF allowance (+60) is fully used; any later FF growth in the engine needs a new decision.
- Acceptance 4 (bench interop with the reference peer) belongs to the post-merge bench lane.
- The processor banks were not rerun: pins and processor sources are unchanged since their last passing run in this lane.
- Hosted checks and the local workflow replica need the pushed head.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (1-3 met; 4 is the post-merge bench lane)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md) (validated locally against dev `8b61b709`)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
