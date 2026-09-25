[R300] NEGATIVE - exact head b94f53cc4e5dbfd9527ba666922a55804515165c

# R300-2: internal independent re-review of #545 / PR #563

- Head `b94f53cc4e5dbfd9527ba666922a55804515165c`, tree `2a7274e19b88474411829707fb0581e2861bb015`. It is one commit on `fc8a719f`. Source base is `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
- This is a delta review of `fc8a719f..b94f53cc` (12 files, +166/-37). My R300-1 verdict covered `fc8a719f`.
- Scope was reconstructed from public state only:
  - AGENTS.md and CONTRIBUTING.md.
  - The #545 body.
  - Assignment 5828714628 and its decisions:
    - the slew campaign becomes an explicit target under the #367 rule;
    - the deadline is not raised;
    - no check is trimmed;
    - a slew discard restarts the guard streak, and this is stated and pinned by a test.
  - The [A305] REVIEW READY comment 5829377477.
  - The diff and its history.
  - The author packet `062a0a91:review-evidence/545-r1/author-r2`.
  - The exact-head hosted runs.
- I read the prior public findings only after my own pass: R301-1, comment 5828686574. Each one is resolved or retained below.
- Verdict: **NEGATIVE**.
  - Closed at this head: my round-1 findings F1, F2 and F3 and my suggestion S1, plus R301-1's F2 and F3.
  - The product RTL changed only in a comment.
  - The hosted `mmcm_servo` shard is green inside its deadline.
  - Two new MINOR findings are open. F4: the new streak test cannot fail when a slew discard counts toward the streak, including a re-base with no fresh guard trips. F5: the authoritative 1800 s budget basis is stale against this head's own hosted measurement.

## Round-1 and prior public findings at this head

| Finding | Status at `b94f53cc` | Evidence |
|---|---|---|
| R300-1 F1 MAJOR: the default target overran its deadline | **Closed** | See "R300-1 F1" below the table. |
| R301-1 F1 MAJOR: the same overrun, plus a stale `CI_WORKFLOWS.md:158` basis | Hosted part **closed**. Docs part **retained** as F5. | The row now reads "original hosted basis: at most 548 s". The measured hosted value at this head is 1159.1 s. |
| R300-1 F2 and R301-1 F2 MINOR: the coincident-step dedupe was untested and U14 was misnamed | **Closed** | S5 (`sim_phc_step.cpp:518-535`) passes with a count of 1 (`receipts/servo_default/slew_suite.log`). My unchanged round-1 mutant `step_dedupe_removed_suite` is now **KILLED**, and only S5 fails, with `2 in [1, 1]` (`receipts/mutants_r1/step_dedupe_removed_suite.log`). The unit-only arm still survives, as the author also records: U14 is a mid-window step. U14 is now named `[U14] mid-window step abandons one slew window`, which matches its stimulus. The author's control `step_dedupe_removed` fails S5 by name (`receipts/campaign/part_d.log`). |
| R300-1 F3 MINOR: the TESTING index was stale | **Closed** | `TESTING.md:267` says twelve gmstep controls and two option-off controls. Parsing `gmstep_mutants.py` gives 14 controls: 12 gmstep and 2 option-off, of which 3 run by default for acceptance and 3 are selected by `--slew` (`receipts/inventory_counts.txt`). The triggers name `.phc_slew_active_i`, `slew_rate_alignment`, `phc_adj_ts_w`, `ts_counter`, `ptp_csr_sync.sv` and `timestamp_counter.sv`. `TESTING.md:268` gives six defects and two positive controls, which equals the parsed `slew_mutants.py`. `TESTING.md:484` states the default/explicit split. `measure_test_evidence.py --check` passes (`receipts/measure_test_evidence_check.log`). |
| R300-1 S1 and R301-1 F3: the tail check re-encoded the RTL formula | **Closed** | See "R300-1 S1 and R301-1 F3" below the table. |
| R301-1 S1 SUGGESTION: the streak reset was unstated and untested | Stated, but the pin is **incomplete**. Retained as F4. | The header (`KL_mmcm_drp_servo.sv:88-91`) and `TIME_SYNC.md:180-186` agree with the RTL: `:715` restarts the streak on a slew and `:709-711` on a #539 step. My `step_streak_reset_removed` is KILLED by U12, so the step half of the text is test-backed (`receipts/mutants_r2/step_streak_reset_removed.log`). The slew half is F4. |

### R300-1 F1: evidence

- `Makefile:49` is `all: run`. `run` still executes unit, rails, step and `+slew_suite`. `mutants` and `slew-mutants` are explicit targets.
- My stage timings used the pinned 5.050, one CPU per simulation, and builds at 2 jobs. The receipts are in `receipts/servo_default/`.

  | Stage | Checks / failures | Time |
  |---|---|---|
  | Builds | n/a | 16.1 s |
  | Unit | 100 / 0 | 29.8 s |
  | Rails | 8 / 0 | 19.6 s |
  | Step | 113 / 0 | 338.0 s |
  | Slew | 90 / 0 | 338.7 s |
  | Sequential total | | 742 s |

- The hosted evidence is `rtl-full` 36113401588, shard 2/5 job 108001867446:
  - `PASS mmcm_servo`, from 08:33:57.4 to 08:53:16.4, which is **1159.1 s**. That leaves 640.9 s (35.6%) of the 1800 s budget.
  - The run tested merge `4bb4317`, which is this head on live dev `a3d795ae`.
  - All shards passed. `verilator-suites`, `yosys-portability`, `rtl-fast`, `docs` and `elaborate` succeeded. `Physical gPTP` was skipped (`receipts/hosted_exact_head_runs.txt`).
- The author's recorded wall clocks (516.943 s, 1652.793 s and 952.797 s) are receipted two-CPU runs, each with an `EXIT: 0; WALL_SECONDS` line. They used Verilator 5.052, not the 5.050 pin.

### R300-1 S1 and R301-1 F3: evidence

- The tail check at `sim_gmstep.cpp:420-450,1089-1092` now grades against the counter accumulator's fractional advance into each staged sample. It uses no delay constant.
- The clean leg passes 58/58. The author's `--slew` run passes 1 positive control plus 3 controls caught by name. The added addend stage breaks exactly the tail check (`receipts/gmstep/`).
- My oracle probe shows the check is not vacuous and has no slack (`receipts/gmstep/oracle_probe_[ab].log`):
  - clean: 4 tail samples, 0 errors;
  - one added addend stage: 5 tail samples, 1 error;
  - two added addend stages: 6 tail samples, 2 errors;
  - tail of 3: fails;
  - tail of 5: passes, because it is conservative;
  - level stuck high: fails `servo clears after the PHC tail`.
- My unchanged round-1 latency probe gives 0 of 492 samples uncovered. Tails of 3 and 2 leave 24 and 42 uncovered (`receipts/latency_probe.log`).

## Findings

### F4 MINOR: Tests, Conformance. U15 cannot fail when a slew discard counts toward the guard streak

- **Artifact:**
  - `tb/verilator/mmcm_servo/sim_main.cpp:555-579` (U15), in particular its arming at `:559-560` (`run_noting_discards(12.0, 2, before)`) and its gap check at `:574-576`.
  - The contract it pins: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:88-91,715` and `docs/design/TIME_SYNC.md:180-186` ("Re-basing therefore requires four fresh guard trips after the slew").
- **Authority:**
  - Assignment 5828714628 decides that a slew discard resets the streak, "stated and pinned by a test", because "a re-base needs four clean guard trips after the slew ends".
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
- **Evidence:** reviewer mutants on the shipped unit harness (`scripts/reviewer_mutants_r2.py`, `receipts/mutants_r2/`, `receipts/runlogs/mutants_r2/`).
  - The author's control `slew_streak_reset_removed` is **KILLED** at U15.
  - `slew_discard_extends_streak` sets `disc_run_r <= disc_run_r + 1` on a slew hit. It **SURVIVES**, 100/0.
  - `slew_discard_counts_as_guard_trip` applies the guard path's increment-and-re-base logic to a slew hit. This is the natural "treat a slew window like an implausible window" alternative. It **SURVIVES**, 100/0.
  - The cause is the arming. U15 opens a streak of two, then the slew window and its tainted tail add exactly two. With `DISC_MAX_C = 4`, a counting variant either wraps to 0 or re-bases on the tail. Either way the four measured gaps after the slew read 32 32 32 33, the same as a reset.
  - The guard-like mutant does break the contract under the shipped stimulus. It re-bases on the tail window with no fresh guard trip. The gap from the tail discard to the first fresh trip becomes 33 ticks instead of the clean RTL's 32, yet U15 passes (`receipts/u15_tail_gap/`; the probe only adds a print, `scripts/u15_tail_gap_print.patch`).
  - With U15 armed by one guard trip instead of two (`scripts/u15_one_trip_arming.patch`), the clean RTL still passes, and all three alternatives (removal, increment and guard-like) are **KILLED** (`receipts/u15_one_trip/`).
- **Impact:**
  - A regression that merges slew discards into the guard streak would re-base the window baseline after fewer than four fresh guard trips. It would pass U15 and the explicit campaign.
  - Only the diagnostic and re-base path is affected. Integrator, trim and LOCKED are not.
  - The decided rule is pinned against the "leave it unchanged" alternative, but not against the "count it" alternative, which is the one most likely to be written by mistake.
- **Required outcome:**
  - A shipped check fails for a slew discard that counts toward, or triggers, the streak, while the clean RTL passes it. Either of these would work:
    - arm U15 so the streak is not a multiple of four after the tainted windows, for example with one or three guard trips;
    - also grade the gap from the tail discard to the first fresh trip.
  - The explicit campaign gains a named control for the counting variant, and that control fails the check.
- **Verification:**
  - `reviewer_mutants_r2.py` reports `slew_discard_extends_streak` and `slew_discard_counts_as_guard_trip` KILLED on the shipped harness, and `clean_unit` passes.
  - `make slew-mutants` reports every control with its named rejection.

### F5 MINOR: Docs. The 1800 s suite-budget basis contradicts this head's hosted measurement

- **Artifact:**
  - `docs/testing/CI_WORKFLOWS.md:158` ("original hosted basis: at most 548 s").
  - `docs/testing/CI_WORKFLOWS.md:162-170`, which ends "Hosted acceptance must still pass on the fixing head."
  - `tb/verilator/mmcm_servo/Makefile:19-21`, which gives a local margin of 847.203 s.
- **Authority:**
  - `CI_WORKFLOWS.md:152-153`: "The measured hosted worst case plus a stated margin sets each named entry." The `milan_dp` row shows the form: hosted window, seconds remaining and percentage.
  - AGENTS.md section 6, Docs: "Changed contracts are reflected in authoritative docs."
  - R301-1 F1 already named this basis as stale. This head edited the row and kept 548 s.
- **Evidence:**
  - At this head, hosted shard 2/5 job 108001867446 ran `mmcm_servo` in 1159.1 s, leaving 640.9 s (35.6%). See `receipts/hosted_head_verilator_shard2_job_108001867446.log:265-266`.
  - The base sample was 334.4 s. That runner was about 1.6x faster than this head's on the suites the PR did not change: `ptp_ts` took 77.5 s against 125.5 s, and `render_setpoint` 58.3 s against 91.0 s.
  - So the suite that sets this row's basis now runs at more than twice the documented basis, and the only margin recorded anywhere is a local one that is larger than the hosted margin.
- **Impact:**
  - The next reader planning a default-suite change would see about 70% headroom in the 1800 s row. On the slow runner class the real headroom is 36%. Hidden headroom is what produced F1 in round 1.
  - The forward-looking "must still pass" line in an authoritative page is now outdated.
- **Required outcome:**
  - The 1800 s row, or the `mmcm_servo` paragraph, records the exact-head hosted sample: job, window and remaining margin, in the same form as the `milan_dp` row. This replaces the pending-acceptance sentence.
  - If the Makefile header keeps a margin figure, it says which measurement that figure comes from.
- **Verification:**
  - The text matches the hosted log.
  - `docs_check`, doc style and doc paths pass.
  - `measure_test_evidence.py --check` still passes.

## Lens results

- [R300] UNCLEAN Conformance. F4: the decision requires the streak rule to be "pinned by a test", and the test pins it against only one alternative. Everything else checked out:
  - Assignment 5828714628 items 1-5 are implemented as specified:
    - item 1: explicit target, a TESTING row with triggers, a measured Makefile record, and the full campaign at 8/8;
    - item 2: S5, its control, and the U14 rename;
    - item 3: a PHC-measured oracle and the addend-stage control;
    - item 4: header and TIME_SYNC text, a unit check, and a removal control;
    - item 5: inventories, triggers, and `measure_test_evidence`.
  - There was no dev merge this round: the head's parent is `fc8a719f`.
  - #545 acceptance 3: the hosted exact-head contexts are green (`receipts/hosted_exact_head_runs.txt`).
  - Acceptances 1 and 2 are unchanged from R300-1.
- [R300] PASS RTL - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:88-91,709-715` at `b94f53cc`.
  - `git diff fc8a719f..b94f53cc -- hdl` is 4 comment lines. The comment is correct against `:709-715`: both a step and a slew clear `disc_run_r`.
  - `lint_rtl.py --check` gives 90 <= 90 (`receipts/lint_rtl_check.log`).
  - The shadow lines, the datapath alignment and connection lines, and processor pin `5dce647a` are byte-unchanged. The R300-1 RTL analysis and latency probe therefore still apply, and the probe reproduces exactly (`receipts/latency_probe.log`).
- [R300] PASS Robustness - `tb/verilator/mmcm_servo/sim_phc_step.cpp:518-535` (S5) and `sim_main.cpp:555-579,642-671` (U15, U14) at `b94f53cc`. I checked five cases:
  - a step and a held slew meeting on one boundary sample: counted once;
  - a reset during a slew;
  - tally saturation at 63;
  - a mid-window step inside a slew;
  - the guard streak across a slew, starting from one prior trip and from two.

  The clean RTL follows the contract in all of them, including the one-trip arming (`receipts/u15_one_trip/clean_unit.log`, `receipts/servo_default/`). The feature-off tie-offs are unchanged. The test-strength gap is F4, recorded under Tests.
- [R300] UNCLEAN Tests. F4. Everything else checked out:
  - The default suites pass: 100, 8, 113 and 90 checks.
  - The explicit campaign passes 8/8, each control with its named rejection, graded by the author's own `run_case()` (`receipts/campaign/`).
  - S5 kills my round-1 dedupe mutant.
  - The connected tail oracle is PHC-measured, not vacuous and exact, as the results above show.
- [R300] UNCLEAN Docs. F5. Everything else checked out:
  - These agree with the code and the parsed inventories: `TESTING.md:267-268,484`, `TIME_SYNC.md:180-186,238-242`, `tb/verilator/milan_dp/README.md:893-900`, the servo header, and the `measure_test_evidence.py` dispositions.
  - `CHANGELOG.md` is still accurate, and the PR body is current for this head.
  - Doc style, doc paths, `docs_check` and `git diff --check` pass (`receipts/doc_gates.log`).
  - The em-dash gate could not judge locally. The hosted `docs` context passed.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F4) | #545 acceptance 1-3; assignment 5828714628 items 1-5 and its decisions; hosted exact-head contexts; commit parentage | R300-2 | `b94f53cc4e5dbfd9527ba666922a55804515165c` |
| RTL | CLEAN | servo `:88-91,709-715`; comment-only `hdl` diff; lint ratchet; unchanged alignment and connection lines and pin; latency probe rerun | R300-2 | `b94f53cc4e5dbfd9527ba666922a55804515165c` |
| Robustness | CLEAN | S5, U15, U14; one-trip and two-trip streak arming on the clean RTL; reset, saturation and feature-off unchanged | R300-2 | `b94f53cc4e5dbfd9527ba666922a55804515165c` |
| Tests | UNCLEAN (F4) | servo Makefile, `sim_main.cpp`, `sim_phc_step.cpp`, `slew_mutants.py`; `sim_gmstep.cpp`, `gmstep_mutants.py`; campaign 8/8; round-1 and new mutants; oracle probe | R300-2 | `b94f53cc4e5dbfd9527ba666922a55804515165c` |
| Docs | UNCLEAN (F5) | TESTING, TIME_SYNC, CI_WORKFLOWS, milan_dp README, servo header, Makefile header, `measure_test_evidence.py`, CHANGELOG, PR body | R300-2 | `b94f53cc4e5dbfd9527ba666922a55804515165c` |

What a fix would un-cover:

- A fix for F4 changes `sim_main.cpp` (U15's stimulus) and `slew_mutants.py`. That un-covers Tests, and Robustness for the U15 case.
- A fix for F5 is docs-only and un-covers Docs.
- RTL stays banked at `b94f53cc` provided no `hdl` file changes.
- The planned #508 dev-merge round will change several lens scopes, so its head must be covered again.

## Real limits

- My default-target figure is a sum of stage timings. The simulations ran concurrently, one CPU each, on a shared 16-CPU host with load around 12. In a probe copy, the builds used the servo Makefile with `-j 0` changed to `-j 2` to respect the job cap. This is not a controlled benchmark. The hosted sample is the acceptance.
- The explicit campaign ran as four foreground invocations. Each called the author's `run_case()` unchanged, with the same anchors and named failures. It was not one `make slew-mutants` process.
- The hosted runs built merge `4bb4317`, which is this head on live dev `a3d795ae`, not on the source base. That is the exact-head PR context, but it is not the manager's final candidate.
- Not run by me:
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - the other `milan_dp` legs, and the full `gmstep-mutants --all`;
  - `crf_rx` and `gptp_shadow`;
  - area;
  - the xvlog, idiom, port-contract and naming gates;
  - act or Docker.
- The pinned Markdown renderer is absent here, so the em-dash, TOC and anchor gates could not run. For those I rely on the hosted `docs` success and on the author's and the manager's receipts.
- Physical calibration was not run. Field skips are not hardware proof, and nothing here is bench evidence.

## Pending manager duties

- Disposition F4 and F5. The #508 overlap round, which is already planned, could carry both fixes. Any fix needs re-review at its new head.
- Hosted and act acceptance at any fixing head.
- The final current-dev candidate build at the merge turn, from source base `5b73d3f4` onto live dev.
- The external review (R301-2) remains independent of this one.

R300-2 FINISHED
