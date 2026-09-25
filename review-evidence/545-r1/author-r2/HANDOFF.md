# [A305] Round 2 handoff

Status: all requested local gates pass; ready for independent re-review.
Head: `b94f53cc4e5dbfd9527ba666922a55804515165c`. Initial head: `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4`.
Branch: `545-crf-servo-slew`. Issue #545. PR #563.
Base: `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
Processor pin: `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.

## Scope and public authority

- [Round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5828714628), items 1-5.
- [Round-1 assignment](https://github.com/kebag-logic/milan-fpga/issues/545#issuecomment-5827358783).
- [Internal review R300-1](https://github.com/kebag-logic/milan-fpga/pull/563#issuecomment-5828443172).
- [External review R301-1](https://github.com/kebag-logic/milan-fpga/pull/563#issuecomment-5828686574).
- Public evidence branch `545-review-evidence` at `134b4fcc23146fd58686710a6706087f76483540` supplied the original probes and receipts. It was fetched into temporary bare storage, with no checkout. No private transcripts were read.

All five assignment items are implemented. Product RTL behavior is unchanged in round 2. The only synthesizable-file edit is the requested streak-contract comment. No dev merge, push, PR edit, new PR, hardware action, donor edit or sub-agent was used. Hosted and local workflow-replica acceptance belong to the manager after publication; they have not been run for this unpublished head. This is executor evidence, not review approval.

## Change list

| File:line | Change and finding |
|---|---|
| `tb/verilator/mmcm_servo/Makefile:49` | F1: default retains all four clean harnesses; mutations move to explicit slew-mutants. Header records the two-CPU clean-build wall clock. |
| `tb/verilator/mmcm_servo/sim_phc_step.cpp:518` | F2: S5 stages a step on a held-slew boundary; arming checks prove that edge and require exactly one tally increment. |
| `tb/verilator/mmcm_servo/sim_main.cpp:555` | Streak decision: U15 observes the externally visible 32/33-tick re-base gaps after two pre-slew guard trips. U12 retains step-streak coverage; U14 now names its actual mid-window stimulus. |
| `tb/verilator/mmcm_servo/slew_mutants.py:18` | Six defect controls and two positive controls; exclusion removal fails S5, streak-reset removal fails U15. |
| `tb/verilator/milan_dp/sim_gmstep.cpp:425` | F3: measure the accumulator advance into the staged sample, including fractional ns. The last measured slew increment identifies the release tail, without a fixed delay formula. A tail witness prevents vacuity; a settled-release assertion preserves the prior clearing check. |
| `tb/verilator/milan_dp/gmstep_mutants.py:112` | New control delays only the applied addend by one register; the unchanged four-cycle indication must fail the tail check. --slew now selects three controls; --all selects fourteen. |
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:88` | Comment only: both slew and #539 step discards restart the four-trip guard streak. |
| `docs/design/TIME_SYNC.md:180` | State the decided streak contract beside the four-trip re-base, plus the measured tail oracle and delay control. |
| `docs/testing/TESTING.md:267` | F1/F3: explicit inventories, twelve gmstep plus two option-off controls, six servo controls, trigger files including .phc_slew_active_i and slew_rate_alignment; default suite row retains the step coverage and adds the slew split. |
| `docs/testing/CI_WORKFLOWS.md:162` | Keep the 1800-second budget; identify the historical hosted basis, round-1 timeout, explicit campaign decision and pending hosted acceptance. |
| `tb/verilator/milan_dp/README.md:895` | Describe the PHC-advance oracle and all three slew connection controls. |
| `scripts/measure_test_evidence.py:597` | Update reader dispositions for the two added servo controls and third connection control. The check passes without a budget change. |

## Default wall clocks

| Condition | Base | Round 1 | Round 2 |
|---|---|---|---|
| Clean default target | 516.943 s (rc 0) | 1652.793 s (rc 0) | 952.797 s (rc 0) |
| Revision | `5b73d3f4` | `fc8a719f` | `b94f53cc4e5d` |
| CPU affinity | 8,9 | 8,9 | 10,11 |
| Contents | unit, rails, step | unit, rails, step, slew, campaign | unit, rails, step, slew |

Commands: `taskset -c <pair> make -C <suite>`, recorded in each timing log. Base and round 1 use clean temporary source extracts; round 2 uses the assigned worktree after `make clean`. All use Verilator 5.052, the same compiler and shared host. These are measured two-CPU local runs, not hosted-runner acceptance or a controlled idle-host benchmark. Early static checks overlapped part of the baseline; later checks were restricted away from benchmark CPUs.

Round 2 leaves 847.203 s (47.1%) of the unchanged 1800 s budget.

## Suite results

| Test | Verdict | Receipt |
|---|---|---|
| Unit | 100 checks, 0 failures, including U15 | unit-run.log; timing-round2.log |
| Rails, step, full slew | 8 rails, 113 step, 90 slew checks; no failures | timing-round2.log |
| Receiver | 13836 unit, 1658 discontinuity, 69 talker-step, 8 campaign checks; no failures | crf-rx.log |
| Shadow | Default suite and lifecycle/mutation controls pass | gptp-shadow.log |
| Connected gmstep | 58 checks, 0 failures after the final clearing assertion | gmstep-final.log |
| Behavior tests | 14 features, 344 scenarios, 1739 steps; no failures or skips | behave.log |
| Builder | Exit 0; only board-utilization calibration NOT RUN because the real report is absent. RV32-backed arms ran. | builder.log |

## Mutation verdicts

The explicit servo campaign reports 8 checks, 0 failures: two positive controls pass and each of six defects returns 1 with its named failure. Compilation errors never qualify as kills.

| Servo defect | Verdict | Required named failure |
|---|---|---|
| `discard_removed` | KILLED | `[S1] overlapped window is discarded` |
| `level_tied_low` | KILLED | `[S1] overlapped window is discarded` |
| `partial_tail_trusted` | KILLED | `[S1] overlapped window is discarded` |
| `discard_not_counted` | KILLED | `[S1] discards counted` |
| `step_dedupe_removed` | KILLED | `[S5] coincident step+slew window counted once` |
| `slew_streak_reset_removed` | KILLED | `[U15] four fresh guard trips precede re-base` |

Receipt: [slew-mutants.log](slew-mutants.log).

The full connected campaign reports 16/16: both clean legs pass and all fourteen defects fail their required named check.

| Connected defect | Verdict | Required named failure |
|---|---|---|
| the policy level is tied low at the servo | KILLED | `slew path: the actual servo receives the level` |
| the policy level omits the applied-rate tail | KILLED | `slew path: every staged sample covers the PHC tail` |
| the policy level misses an extra addend stage | KILLED | `slew path: every staged sample covers the PHC tail` |
| the step does not toggle mr | KILLED | `restart: the outgoing mr toggles exactly once` |
| the grandmaster identity re-bases the render stage as well as the step | KILLED | `render: the GM change is one counted re-base event` |
| the step does not re-centre the render stage | KILLED | `render: the GM change is one counted re-base event` |
| the render re-base is keyed to the identity, not the step | KILLED | `render: every counted re-base lands at a PDU end right after the step` |
| tu reaches the talkers four cycles late | KILLED | `tu: set in the first cycle the bank names GM B` |
| the plane's step does not re-arm the holdover | KILLED | `tu: held at least the 0.25 s holdover after the step` |
| tu stops the talker | KILLED | `licence: the talker never pauses beyond four of its intervals` |
| the grandmaster change stops the talker for good | KILLED | `licence: the talker never pauses beyond four of its intervals` |
| the step's re-centre snaps one event off the setpoint | KILLED | `render: every PDU push leaves the target fill across the event` |
| a software settime does not toggle mr | KILLED | `CLKV: the settime toggled mr once more (#387)` |
| the step's mr toggle is gated by the CRF clock-source selection | KILLED | `CLKV: its mr toggled once per PHC step issued so far (#387)` |

Receipt: [gmstep-mutants-final.log](gmstep-mutants-final.log). The added addend stage breaks exactly the PHC-tail check.

## Reviewer-owned probes rerun

| Original probe | Clean verdict | Control verdict / named failure | Receipt |
|---|---|---|---|
| R301 coincide_probe | rc 0; count 1; both arming checks pass | rc 1; count 2; `[C1] coincident step+slew window counted once` | r301-coincide.log |
| R300 step_dedupe_removed_unit | The mutant SURVIVES the 100-check unit-only harness | Recorded survivor, not claimed as a kill. The new killing case is in the full slew harness. | r300-step-dedupe-unit.log |
| R300 step_dedupe_removed_suite | Full new slew harness executed | KILLED, rc 1; `[S5] coincident step+slew window counted once`, 2 versus 1; 90 checks / 1 failure | r300-step-dedupe-suite.log |
| R300 latency, 4 stages | 24 schedules; 492 slewed samples; 0 uncovered; rc 0 | 3 stages: 24 uncovered, rc 1. 2 stages: 42 uncovered, rc 1. | r300-latency-4.log, r300-latency-3.log, r300-latency-2.log |
| R301 tail, 4 stages | 96 slewed samples; 0 violations; rc 0 | 3 stages: 3 violations, rc 1. Probe wrapper exits 0 after recognizing this expected failure. | r301-tail.log |

Probe assertions and stimulus remain the published versions. Environment overrides select this worktree and disposable build directories. The R301 tail launcher reads the current files instead of its hard-coded old revision. The coincidence launcher receives a minimal scratch copy so its extra C++ source never touches the worktree. R300 controls use the recipe's source/build-directory overrides. No reviewer control was weakened. Tail-path RTL is unchanged from the reviewed head.

## Gate table

Exact argv, wall clocks, and every attempt are in [GATE-TABLE.md](GATE-TABLE.md) and [gates.jsonl](gates.jsonl). None of the gate commands was piped. Logs are ordinary foreground stdout/stderr files. The recorder supplies a generous six-hour bound; the datapath chunks allow four hours per command.

| Required gate | Final exit | Seconds | Receipt |
|---|---|---|---|
| Clean default servo, two CPUs | 0 | 952.797 | [timing-round2.log](timing-round2.log) |
| Explicit servo campaign | 0 | 1142.751 | [slew-mutants.log](slew-mutants.log) |
| Receiver suite | 0 | 791.913 | [crf-rx.log](crf-rx.log) |
| Shadow suite, -j8 | 0 | 511.891 | [gptp-shadow.log](gptp-shadow.log) |
| Connected gmstep | 0 | 50.567 | [gmstep-final.log](gmstep-final.log) |
| Full gmstep campaign | 0 | 712.353 | [gmstep-mutants-final.log](gmstep-mutants-final.log) |
| Default datapath commands 0-4 | 0 | 314.424 | [datapath-sweep-00-05.log](datapath-sweep-00-05.log) |
| Default datapath commands 5-19 | 0 | 405.076 | [datapath-sweep-05-20.log](datapath-sweep-05-20.log) |
| Default datapath commands 20-30 | 0 | 596.22 | [datapath-sweep-20-31.log](datapath-sweep-20-31.log) |
| Default datapath commands 31-32 | 0 | 573.356 | [datapath-sweep-31-33.log](datapath-sweep-31-33.log) |
| Final connected leg, sweep command 8 | 0 | 30.37 | [datapath-sweep-final-08.log](datapath-sweep-final-08.log) |
| Final acceptance controls, sweep command 32 | 0 | 183.412 | [datapath-sweep-final-32.log](datapath-sweep-final-32.log) |
| Builder | 0 | 582.767 | [builder.log](builder.log) |
| Docs, Git inventory | 0 | 4.121 | [docs-final.log](docs-final.log) |
| Docs, no-Git CI inventory | 0 | 4.223 | [docs-no-git-head.log](docs-no-git-head.log) |
| Em dash, required base | 0 | 3.023 | [em-dash.log](em-dash.log) |
| Document style | 0 | 0.065 | [doc-style.log](doc-style.log) |
| TOC check | 0 | 2.623 | [toc-final.log](toc-final.log) |
| Anchor check | 0 | 1.67 | [anchors-final.log](anchors-final.log) |
| Document paths | 0 | 0.114 | [doc-paths.log](doc-paths.log) |
| Module matrix | 0 | 0.967 | [matrix.log](matrix.log) |
| Live front-end parse | 0 | 240.432 | [xvlog.log](xvlog.log) |
| RTL source lists | 0 | 1.317 | [source-lists.log](source-lists.log) |
| SV idiom | 0 | 0.416 | [sv-idiom.log](sv-idiom.log) |
| RTL lint | 0 | 14.834 | [lint.log](lint.log) |
| C++ idiom | 0 | 1.166 | [cpp-idiom-final.log](cpp-idiom-final.log) |
| Python idiom | 0 | 9.181 | [py-idiom.log](py-idiom.log) |
| Port contracts | 0 | 4.423 | [ports.log](ports.log) |
| Naming | 0 | 0.466 | [naming.log](naming.log) |
| Test evidence | 0 | 5.83 | [test-evidence-final.log](test-evidence-final.log) |
| Behavior tests | 0 | 1.17 | [behave.log](behave.log) |
| Whitespace | 0 | 0.032 | [diff-final.log](diff-final.log) |
| Area: base servo | 0 | 4.327 | [ooc-base.log](ooc-base.log) |
| Area: current servo | 0 | 5.477 | [ooc-head.log](ooc-head.log) |
| Area: isolated alignment | 0 | 2.674 | [ooc-alignment-final.log](ooc-alignment-final.log) |

The live front-end parse keeps its existing four processor findings and zero first-party findings. No lint, idiom, naming, port or test-evidence budget was raised.

Initial setup retries are retained: TOC/anchors initially refused the missing locked renderer (rc 2); packages were installed under `/tmp`, then both passed. The first no-Git export omitted empty submodule directories (rc 1); restoring the CI checkout's directory shape fixed the broken links. The first isolated area wrapper redeclared its output net (rc 1); replacing that redeclaration with the same continuous assignment fixed the scratch wrapper. None required a product change or weaker gate.

## Datapath default sweep

The 33 commands are the expanded unmodified `make -n run` recipe, with only banner echo commands omitted. [sweep-plan.txt](sweep-plan.txt) and [sweep-plan.json](sweep-plan.json) contain every command. Four foreground chunks preserve command order within each chunk; commands 8 and 32 are rerun after adding the settled-release assertion, with their final exits shown below; independent final controls use separate mutation builds. Every command has its own receipt and exit, retained in [sweep-results.jsonl](sweep-results.jsonl).

| Index | Exit | Seconds | Receipt |
|---|---|---|---|
| 0 | 0 | 0.32 | [sweep-00.log](sweep-00.log) |
| 1 | 0 | 38.26 | [sweep-01.log](sweep-01.log) |
| 2 | 0 | 112.81 | [sweep-02.log](sweep-02.log) |
| 3 | 0 | 44.42 | [sweep-03.log](sweep-03.log) |
| 4 | 0 | 118.5 | [sweep-04.log](sweep-04.log) |
| 5 | 0 | 0.47 | [sweep-05.log](sweep-05.log) |
| 6 | 0 | 0.16 | [sweep-06.log](sweep-06.log) |
| 7 | 0 | 38.55 | [sweep-07.log](sweep-07.log) |
| 8 | 0 | 30.32 | [sweep-08.log](sweep-08.log) |
| 9 | 0 | 35.19 | [sweep-09.log](sweep-09.log) |
| 10 | 0 | 30.63 | [sweep-10.log](sweep-10.log) |
| 11 | 0 | 37.68 | [sweep-11.log](sweep-11.log) |
| 12 | 0 | 27.31 | [sweep-12.log](sweep-12.log) |
| 13 | 0 | 24.65 | [sweep-13.log](sweep-13.log) |
| 14 | 0 | 29.46 | [sweep-14.log](sweep-14.log) |
| 15 | 0 | 23.91 | [sweep-15.log](sweep-15.log) |
| 16 | 0 | 22.3 | [sweep-16.log](sweep-16.log) |
| 17 | 0 | 33.32 | [sweep-17.log](sweep-17.log) |
| 18 | 0 | 33.54 | [sweep-18.log](sweep-18.log) |
| 19 | 0 | 22.88 | [sweep-19.log](sweep-19.log) |
| 20 | 0 | 7.9 | [sweep-20.log](sweep-20.log) |
| 21 | 0 | 15.35 | [sweep-21.log](sweep-21.log) |
| 22 | 0 | 25.72 | [sweep-22.log](sweep-22.log) |
| 23 | 0 | 7.49 | [sweep-23.log](sweep-23.log) |
| 24 | 0 | 9.25 | [sweep-24.log](sweep-24.log) |
| 25 | 0 | 11.89 | [sweep-25.log](sweep-25.log) |
| 26 | 0 | 8.65 | [sweep-26.log](sweep-26.log) |
| 27 | 0 | 6.23 | [sweep-27.log](sweep-27.log) |
| 28 | 0 | 0.67 | [sweep-28.log](sweep-28.log) |
| 29 | 0 | 6.28 | [sweep-29.log](sweep-29.log) |
| 30 | 0 | 496.71 | [sweep-30.log](sweep-30.log) |
| 31 | 0 | 386.1 | [sweep-31.log](sweep-31.log) |
| 32 | 0 | 183.36 | [sweep-32.log](sweep-32.log) |

## Area delta

| Measurement | LUT | FF | DSP | CARRY4 |
|---|---|---|---|---|
| Base servo | 864 | 790 | 1 | 150 |
| Current servo | 871 | 792 | 1 | 150 |
| Servo delta | +7 | +2 | 0 | 0 |
| Isolated release alignment | 1 | 4 | 0 | 0 |

Repository recipe: `syn/yosys/ooc.sh KL_mmcm_drp_servo`, default parameters, `synth_xilinx -family xc7 -flatten`, no seed override, no timing claim. Yosys 0.66 and sv2v 0.0.13. A disposable copy of the same script fixes its repository root and substitutes only the base servo source for the base run. Another adds the verbatim alignment block as a standalone top; its declared output uses a continuous assignment. ROM generation, verification, mapping and report checks remain the repository recipe. No donor or tracked source was swapped. This reproduces the round-1 isolated parent-logic delta; it is not a full-datapath or processor area delta.

## Handoff and limits

- [PR-BODY.md](PR-BODY.md) is the full fetched PR body, updated for round 2; it starts `[A305]` and retains `Closes #545`. It has not been applied to the PR.
- No push or merge was performed. The manager must publish this local head and obtain independent re-review and exact-head hosted acceptance. No author-created clean-lens ledger is claimed.
- The deferred #508/current-dev overlap remains for its authorized later round.
- No hardware run was performed. The builder's absent report arm remains NOT RUN.
- Temporary public evidence, benchmark source extracts, probe builds, renderer packages and synthesis work are removed before the final issue comment. The output directory contains only reports, receipts, command plans, small recorder scripts and the round-2 diff.
