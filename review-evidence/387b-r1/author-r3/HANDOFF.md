[A277] Round 3 author handoff for PR #555

Branch: `387-media-rebase`.
Starting head: `a21cd3585abdd3cdf4ac5774a048361a66fed043`.
Final head: `0f003fab3303858ba4db955ad3c0512e67a8018b`.
Review base: `57456af96b3127b9d309a995bbbd35a6113ce52d`.

Assignment: [issue #387, comment 5820585975](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820585975).
This handoff concerns acceptance 3. Acceptance 4 remains open for the manager's #117 two-board measurement after merge.

## Disposition

| Assigned item | Implemented outcome | Evidence |
|---|---|---|
| R276-5 F1 / R277-4 F2 | `milan_dp` defaults to 3600 seconds. The evidence contract and its mutation use the new value. Hosted shards already allow 120 minutes. | `scripts/run_all_suites.sh`, `scripts/measure_test_evidence.py`, its self-test, `.github/workflows/rtl.yml`; `test-evidence.log`, `test-evidence-selftest.log`, `ci-events.log` |
| R277-4 F1 | Both positive legs suppress directory printing while obtaining recipe inputs. | `tb/verilator/milan_dp/gmstep_mutants.py`; `freshness-make43.log`, `freshness-make44.log`, `freshness-both-legs.log`, `gmstep-mutants.log` |
| R276-5 F2 | CRF selection gates CRF triggers; PHC steps toggle `mr` and count MEDIA_RESET regardless of selection. | FPGA design, compliance matrix, and roadmap diffs; docs receipts |
| R276-5 S1 / R277-4 S1 | The prepared PR body cites the accepted report boundary and control inventory. | `PR-BODY.md`, decision 5819379503 |
| R276-5 S2 | Render-stage summary matches the banner and port contract. | `hdl/ieee1722/aaf/KL_render_setpoint.sv` |
| R277-4 S2 | Comment explains the stop-cycle purpose of `streaming_i[t]`. | `hdl/ieee1722/avtp/KL_media_clock_restart.sv` |
| R276-5 S3 | Four live-CSR settime checks require one render pulse and one executed re-base, remaining singular over 100 later PDUs. | `tb/verilator/milan_dp/sim_aclk.cpp`, `sweep-40.log`; `settime-render-control.log` proves omission fails |

No functional RTL changed in this round. No grid-aligner, CRF-servo, gPTP, submodule, or hardware change was made.

## Decisions and measurements

- [5819379503](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819379503): the engine's boundary is the PDU report. Requests during launch-to-report latency merge. The three acceptance controls remain in default `run`; additional controls remain explicit.
- [5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308): raise the deadline to 3600 seconds. The 2459.9-second hosted window at `a21cd358` left 240.1 seconds (8.9%) previously, and leaves 1140.1 seconds (31.7%) against the new budget. The day's observed spread was 1296-2460 seconds. A future margin below 10% calls for further sharding.
- `hosted-window.log` reproduces the 2459.9- and 1296.1-second endpoints with the reviewer's unchanged measurement script. That script reports margins against its historical 2700-second constant. These samples are historical evidence, not measurements of the corrected head.

## Validation

The full true-ratio leg passed 143/143, including the four new settime checks. The full builder passed with 189/189 applicable mutations rejected and 53/53 RTL variants elaborated. Its two exclusions are compiler-dependent gate 1b instruments and gate 11 physical calibration. The gmstep campaign passed 13/13 under GNU make 4.3, with no stale-rebuild message for either positive leg. tkdiag passed 96/96 and caught all four mutants (5/5 campaign verdict).

The default sweep passed all 44 expanded commands: 9785 checks, 0 failures. Their summed foreground durations were 1475.52 seconds, excluding gaps between chunks. Every assigned gate exited 0.

Documentation passed in Git and no-Git modes. The style, TOC, cited-path, module-matrix, front-end, source-list, C++/Python idiom, behavior, and diff gates all exited 0. The behavior suite passed 344 scenarios and 1739 steps. The em-dash gate passed against the assigned base. The deadline contract passed 101 self-test checks, and the CI contract passed. Full commands and exclusions are retained in the per-gate receipts.

Each gate has a `.log` and a `.json` receipt containing its command, exit status, and duration. `sweep-commands.json` preserves the default `make -n run` expansion at the tested tree, with eight build jobs. `run_sweep_chunk.py` executed each expanded command without a pipeline and stopped on a nonzero exit. The chunks were 1-9, 10-18, 19-40, and 41-44. Three generated prerequisites were already current, so this expansion contains 44 commands rather than the previous round's 47.

The freshness repro is the unchanged reviewer script. Under GNU make 4.3 its diagnostic still demonstrates `make[1]: Entering directory` tokens, while the fixed function reports `is_fresh: True` inside the parent recipe. Additional assertions cover both legs, reject missing/stale executables, and show the old implementation returning False for fresh binaries.

`full_builder_absent.py` runs the complete builder entry point. It uses the repository's compiler audit to hide all RV32 candidates without changing the host toolchain. The full builder's final exclusions are recorded, including compiler-dependent instrumentation and physical report calibration. No skipped arm is hardware evidence.

The settime control uses a temporary datapath source with only software settime removed from the render trigger. It must compile and fail the named new check; the control driver itself exits 0 only when that happens. The unmodified source remains the positive sweep input.

## Public input integrity

The two review packets were fetched read-only into temporary scratch, from branch `387b-review-evidence`:

- R276-5: archive commit `81136f848fbf36360448af8a06a12da6cc0a6650`.
- R277-4: archive commit `b21f44ae0057c232a219aba1abd5e5560a5629dc`.

R276-5's 31 manifest entries matched. R277-4's repro script and all its other checked receipts matched except `receipts/hosted_head_suite_milan_dp.log`, whose committed archive bytes differ from its manifest checksum. The fresh read-only hosted-window reproduction corroborates the timing evidence independently. No private transcript or management output outside this handoff directory was read. Temporary evidence exports and dependencies were removed after validation.

## Manager handoff

`PR-BODY.md` is the full replacement body, ready to apply after publication. This session neither pushed nor edited the PR. The final issue comment provides the corrected head and local evidence summary; it is an author readiness statement, not a review verdict.

Next steps remain publication of this head, exact-head hosted and local workflow evidence, two independent positive reviews and a reviewer-owned lens ledger, current-dev candidate validation, authorized merge, containment, and acceptance 4. The source branch's base was not advanced in this assignment.
