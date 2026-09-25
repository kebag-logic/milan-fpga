# [A309] Round 2 handoff

Status: implemented and locally validated; ready for independent review.
Branch: `559-capture-copy`.
Initial head: `32076148acb0b9122e8c92a44f8e2ebbc8169280`.
Final local head: `31808e6525a83955bc4322ac8ac6871f9e6b10e6`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112.

## Stop condition and remedy

The maximum over all 32 aligned 50 MHz 8x8 captures is **24.30454 ms**.
It is below 24.5 ms by 0.19546 ms (0.798% of the limit).
The STOP condition did not trigger. The nominal hold remains 50 ms; its free-running millisecond tick guarantees a 49 ms floor. The floor-based margin is **2.0161x**. This remedy is conditional on the measured copy and clock remaining unchanged.

No product firmware, product RTL, configuration YAML, donor or builder census list changed. No push, PR edit, merge, hardware access or delegated work was performed. Hosted checks and independent re-review remain with the manager.

## Measurements

Every row below uses aligned CPU/system rising edges and 16 captures. Both 100 MHz arms are labelled non-contract comparisons. The published maximum includes every arm, not only traffic ON.

| Shape | CPU / system | Traffic | Captures | System cycles, min to max | Maximum ms | 49 ms / maximum |
|---|---|---|---|---|---|---|
| 8x8 | 50 / 100 MHz | ON | 16 | 2,429,322 to 2,430,454 | 24.30454 | 2.0161x |
| 8x8 | 50 / 100 MHz | OFF | 16 | 2,425,516 to 2,426,154 | 24.26154 | 2.0197x |
| 1x1 | 50 / 100 MHz | ON | 16 | 659,822 to 660,642 | 6.60642 | 7.4170x |
| 1x1 | 50 / 100 MHz | OFF | 16 | 658,554 to 658,857 | 6.58857 | 7.4371x |
| 8x8 | 100 / 100 MHz | ON | 16 | 1,899,012 to 1,900,433 | 19.00433 | 2.5784x |
| 8x8 | 100 / 100 MHz | OFF | 16 | 1,978,694 to 1,979,024 | 19.79024 | 2.4760x |

Census: 8x8 = 12,634 closed-record bytes / 156 records; 1x1 = 3,218 / 53. Every ordinary capture attested with zero open ownership and zero destination mismatches. ON counts accepted requests, successful responses and shared descriptor-memory reads; OFF has zero in all three counters. Logs and per-arm JSON receipts are adjacent to this handoff; the committed receipt contains all 96 rows, commands, clocks and hashes.

The offered load produces small measured increases at the contract clock, rather than literally zero effect. Section 18 reports the exact ON/OFF differences; it does not assert the unsupported phrase “does not measurably lengthen”. At 100 MHz the OFF arm is slower. Both arms are therefore graded and included in every published maximum. This wording is an evidence-driven correction to the assignment's proposed characterization, not a change to its acceptance limit.

## Reviewer reproduction

The public evidence branch was fetched read-only into temporary scratch at `39ac477dd8f92b16ccb0e3ab1248a50020d48fd9`; that fetch and its extracted files were deleted after use.

| Reviewer probe | Captures compared | Published maximum ms | Reproduced maximum ms | Result |
|---|---|---|---|---|
| R325-1, original-phase 50 MHz ON | 4 | 24.15248 | 24.15248 | every row field identical |
| R325-1, original-phase 50 MHz OFF | 2 | 24.15108 | 24.15108 | every row field identical |
| R324-1, original-phase 50 MHz ON | 2 | 24.15248 | 24.15248 | every row field identical |
| R324-1, original-phase 50 MHz OFF | 2 | 24.15108 | 24.15108 | every row field identical |
| R324-1, aligned 50 MHz ON | 2 | 24.29902 | 24.29902 | every row field identical |

`reviewer-comparison.json` records each compared row; `reviewer-probe-hashes.json` identifies the public scripts and patches. The R325 shell pipeline was adapted to call its unchanged build/compiler/grader functions with an in-memory clock override. The actual R324 `probe_step.py` was executed through a small adapter with that override and its published C++ phase patch. These setup adaptations avoid forbidden checkout copies and YAML edits. R324's aligned reproduction used its scoped simulator version 5.050; the other probes and the final matrix used 5.052. The CPU netlist and instrumented firmware hashes match the public receipts. See `reviewer-probe-adapter.py`, `r324-probe-adapter.py` and reproduction logs.

## Gate design and controls

`python3 scripts/check_nvm_capture.py` runs in the hosted documentation job. It requires ordinary Python gate dependencies and initialized source dependencies, but no RV32 compiler, LiteX import or simulation.

It regenerates both shapes' tables, derives their framed closed-record byte totals and record counts, and compares them with `measurements.json`'s `measured_for` entries. The explicit contract CPU clock comes from `recipe.py`; the gate separately pins each YAML CPU clock and the system clock. Thus the temporary 50 MHz override cannot hide configuration changes while #565 remains open. Any difference, including shrinkage or speedup, refuses the old measurement. Product firmware and harness source hashes also bind the evidence to its inputs.

The gate regrades every recorded row, checks both arms at all three shape/clock points, and recomputes the published maxima. Timing uses integer system ticks against half the 49 ms floor.

Named input controls: `bytes`, `records`, `clock`, `configured-clock`, `system-clock`. Each changes one live derived value and must fail the real comparison. A slower OFF fixture must set the maximum; a planted grader excluding OFF must fail it. Exactly 24.5 ms passes and one additional system tick fails, including OFF. All controls run before each ordinary verdict. The explicit `--mutation bytes`, `records`, `clock` and `ignore-off-timing` invocations each exit 1 for the intended reason; `capture-control-results.json` records the checks.

The live simulation controls also returned 0: skipped stores left every byte poisoned and were caught; disabled traffic left a correct copy with zero counters and passed the same timing check. Their native exits are 1 and 0 respectively, as required by the control oracles.

## Changes

- `.github/workflows/docs.yml:222`
- `scripts/check_nvm_capture.py:32`
- `tb/verilator/nvm_capture_cpu/recipe.py:5`
- `tb/verilator/nvm_capture_cpu/run.py:51`
- `tb/verilator/nvm_capture_cpu/soc.py:118`
- `tb/verilator/nvm_capture_cpu/sim_main.cpp:127`
- `tb/verilator/nvm_capture_cpu/measurements.json:22`
- `tb/verilator/nvm_capture_cpu/README.md:1`
- `docs/testing/TESTING.md:164`
- `tb/verilator/README.md:79`
- `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557`

The harness adds the clock override, aligned edges and normal ON/OFF timing arms. The new hosted gate binds census and clocks to the measurements. Documentation identifies every substituted model, the manual measurement's Makefile exception, the actual writer clock, the 49 ms floor and #565.

## Gate table

Commands ran in the foreground, without pipelines, with generous timeouts. Simulation build trees and test temporary directories live under `$VALIDATION_STORAGE/559-a309-*`; output holds only documents, scripts and receipts. The SDK was read-only. The Markdown gates used the existing locked renderer packages read-only.

| Gate | Command | rc | Receipt |
|---|---|---|---|
| baremetal | `python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal.log` |
| docs | `python3 -B scripts/docs_check.py` | 0 | `docs.log` |
| docs-no-git | `env GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | `docs-no-git.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| toc | `python3 scripts/gen_toc.py --check` | 0 | `toc.log` |
| anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | `anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog.log` |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| ports | `python3 scripts/check_port_contracts.py` | 0 | `ports.log` |
| naming | `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence.log` |
| diff | `git diff --check` | 0 | `diff.log` |
| nvm-backend | `make -C tb/verilator/nvm_backend` | 0 | `nvm-backend.log` |
| nvm-cosim | `make -C tb/verilator/nvm_cosim` | 0 | `nvm-cosim.log` |
| nvm-hosttest | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | `nvm-hosttest.log` |
| builder-sdk | `python3 $MANAGEMENT/2026-09-23/559-a309/full-builder-sdk.py` | 0 | `builder-sdk.log` |
| builder-absent | `python3 $MANAGEMENT/2026-09-23/559-a309/full-builder-absent.py` | 0 | `builder-absent.log` |
| 8x8-50-on | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir $VALIDATION_STORAGE/559-a309-8x8-50-on` | 0 | `8x8-50-on.log` |
| 8x8-50-off | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir $VALIDATION_STORAGE/559-a309-8x8-50-off` | 0 | `8x8-50-off.log` |
| 1x1-50-on | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir $VALIDATION_STORAGE/559-a309-1x1-50-on` | 0 | `1x1-50-on.log` |
| 1x1-50-off | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 --traffic off --build-dir $VALIDATION_STORAGE/559-a309-1x1-50-off` | 0 | `1x1-50-off.log` |
| control-skip-copy | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation skip-copy --build-dir $VALIDATION_STORAGE/559-a309-control-skip-copy` | 0 | `control-skip-copy.log` |
| control-no-traffic | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation no-traffic --build-dir $VALIDATION_STORAGE/559-a309-control-no-traffic` | 0 | `control-no-traffic.log` |
| 8x8-100-off | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic off --build-dir $VALIDATION_STORAGE/559-a309-8x8-100-off` | 0 | `8x8-100-off.log` |
| 8x8-100-on | `python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 --traffic on --build-dir $VALIDATION_STORAGE/559-a309-8x8-100-on` | 0 | `8x8-100-on.log` |
| diff-cached | `git diff --cached --check` | 0 | `diff-cached.log` |
| capture-gate-none | `python3 scripts/check_nvm_capture.py` | 0 | `capture-gate-none.log` |
| em-dash | `python3 scripts/check_em_dash.py --base a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4` | 0 | `em-dash.log` |

The SDK wrapper is the prescribed manager wrapper with only its audit-file destination changed. It executes the full `sw/builder/test_builder.py --require-rv32`, mapping only the selected compiler argv[0] to the pinned SDK compiler. `builder-sdk-argv.jsonl` records actual invocations. The absent wrapper executes the full default builder after hiding only its three cross-compiler candidates; real host compiler probes remain visible. `builder-absent-argv.jsonl` records the intentional absences.

Both builder modes report the missing historical placement-calibration report as NOT RUN. The compiler-absent mode also intentionally reports its compiled census and dependent controls as NOT RUN. The SDK mode executes those compiler-dependent arms. These skips are not executed passes.

`nvm_cosim` reports 465 PASS, 0 FAIL and 39/39 named mutants killed. `nvm_backend` passes both shapes and all four controls. `nvm_hosttest` passes all five shapes and its controls. The parser gate executes and matches its existing four pinned-source findings; it is not a skipped invocation. OOC is inapplicable because no RTL source changed.

Intermediate checks found a missing docstring and needed Contents navigation; both were corrected without weakening budgets. The input gate correctly refused the old receipt during preflight, then passed with the new measurements. The final table records successful runs; expected failing controls are recorded separately.

## Review and remaining limits

This handoff is author evidence, not a review verdict. Both reviewers must re-review the new head. Exact-head hosted acceptance, the candidate merge and merge authorization remain with the manager. No physical DDR calibration, silicon timing, debounce or physical memory-ordering claim is made. The relative phases are deterministic and aligned, not swept.

`PR-BODY.md` contains the full original PR body structure updated for this head, with a Round 2 section and `Closes #559`. The issue receives the authorized `[A309] REVIEW READY` comment with this head; no PR edit is made.
