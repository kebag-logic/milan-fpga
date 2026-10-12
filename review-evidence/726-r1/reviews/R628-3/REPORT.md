[R628] NEGATIVE - exact head e893e4d13d99eb5ba00745f0f5cf74ee847972c2

# R628-3: internal cleared-context review of PR #729 (issue #726)

Reviewed head `e893e4d13d99eb5ba00745f0f5cf74ee847972c2`, tree `0e94807ebc9c4978bfb173c8d3076f9ddfefc4cf`. Source base `c6bd08c6`. Full diff `c6bd08c6..e893e4d1` (12 commits, 32 files). Round 3 delta `37944f8a..e893e4d1`.

**Result.** Two open findings make the verdict NEGATIVE.

- **F2 BLOCKER (Tests, Robustness).** The hosted `verilator-suites` milan_dp shard fails at this head because of this PR's new `counters` target. It also failed at the two earlier published heads. The new standing fixture has never run in hosted CI.
- **F1 MAJOR (Conformance, Tests, Docs).** The notification-window evidence passes only because of how the fixed one-second grid lines up with the notifications. Moving the grid 0.2 ms makes the PR's own `[726 CADENCE]` check fail on the corrected RTL. The run's own window 1 is empty for input 0 at both shapes, and the PR calls that a startup transient.

The production RTL itself reads correctly against the rulings. The RTL lens is clean.

## Reconstruction

I read the sources in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. `docs/README.md`.
3. The issue #726 body, with frozen acceptance items 1-4.
4. The maintainer rulings: the counter law [6125741685](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685), the addendum [6125845117](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125845117), and the window ruling [6126028604](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6126028604) (no processor change, three window bullets).
5. The lane documents: assignment [6125784157](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125784157) (STOP bounds: submodule change, more than +200 LUT, timing or capture miss), round 2 [6129163001](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6129163001), round 3 [6131008329](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6131008329), and the author's REVIEW READY comments.
6. The PR body at this head.
7. The full diff and history.
8. Public evidence at `cf851544:review-evidence/726-r1/author-r3`.

I read prior review findings and fetched their probes only after I had written my own draft verdict and ledger (`receipts/INDEPENDENT-DRAFT.md`, 20:47Z). I found F2 after that draft, while checking hosted state.

## Executed evidence (this round, this head)

All runs used the pinned simulator 5.050 (`receipts/restore_and_identity.txt`), at most 16 jobs, with scratch-only work directories.

| Campaign | Result | Receipt |
|---|---|---|
| Behaviour gate `cd tests && python3 -m behave --no-capture -f plain` | 14 features, 406 scenarios, 1,977 steps, 0 failed or skipped | `receipts/behave.log` |
| Grader `torture_campaign.py --self-test` | 80 tests OK | `receipts/selftest.log` |
| Parent fixture, `uncertain` outputs | shape 1: 98 checks, 0 failures; shape 8: 427, 0 | `receipts/runs/clean{1,8}/run.log` |
| Parent fixture, `frames-only` outputs | shape 1: 110, 0; shape 8: 481, 0. TU/MR counters 0, wire tu/mr 0, one start, no stop | `receipts/runs/fo{1,8}/run.log` |
| `before` baseline (c6bd08c6 engines) | shape 1: 20 failures, all TX/RX/CADENCE; shape 8: 90. The driver accepts both | `receipts/runs/before{1,8}/run.log` |
| The nine PR plants | Each fails only its named group, then rc 0 with that group omitted. tx-interval 6, rx-interval 1, tx-reset 4, aaf-reset 1, crf-reset 1, rx-saturation 1, late 12, rate 32, tx-nodirty 16 (OUTPUT_CADENCE) | `receipts/mut_*.log`, `receipts/runs/mut_*/` |
| Mailbox (F5) path | shapes 1 and 8 rc 0. `late` and `rate` detected (rc 1), escapes rc 0 | `receipts/f5_*.log`, `receipts/runs/f5_*/` |
| Reviewer plants (`scripts/probe_variants.py`) | Restoring only the AAF healthy-traffic dirty guards: 6 CADENCE failures. Restoring only the CRF guard: 6 CADENCE. CRF wipe on both bind edges: RX_RESET "unbind preserves total". FRAMES_TX saturating instead of wrapping: 2 TX failures. All escape with only that group omitted | `receipts/probe_*.log`, `receipts/runs/probe_*/` |
| Reviewer grader-guard plants (`scripts/probe_grader_guards.py`) | Restored zero guard: `test_unpublished_zero_receive_snapshot` fails; escape runs 79 tests OK. Suppressed interval-side findings: both XSIDE/MULTI tests fail; escape runs 78 OK | `receipts/runs/grader_*.log` |
| Unit suites | tkdiag 99/0 plus mcr_mutants 5/5. avtp_rxmon 97/0, NxN 119/0, lockstep N=1 and N=8 36/0 each, lockstep_mutants 5/5. crf_rx 14,287/0, discontinuity 2,201/0, talker_step 69/0, mutants 10/10 | `receipts/unit_*.log` |
| R628-2 `probe_xside_law.py`, unchanged (sha256 matches its manifest) | rc 0. The ruled pair 32000/32000 gives PASS with no findings. 4/32000 gives FAIL with the finding against the talker. 4/4 gives FAIL with one finding per side. Stream sources are accepted | `receipts/probe_xside_law.jsonl` |
| R629-2 `probe_snapshot.py`, published bytes, unchanged | rc 0. Before publication TV=3, TNV=0, FRAMES_RX=0 gives INFO, `ratio: null`. After publication 3 gives PASS | `receipts/probe_snapshot.log`, `receipts/runs/snapshot-rtl.log` |
| R629-1 `reproduce_contract.py` | rc 0; the bind/unbind scenario passes | `receipts/reproduce_contract.log` |
| Docs-workflow gates (46 commands, pinned Markdown renderer, Python 3.12) | All rc 0. These include `measure_naming --check` (95 recorded), `measure_test_evidence --check` (0 unexplained readers), `check_py_idiom`, `check_cpp_idiom`, hygiene, the sv/sh idiom gates, `docs_check`, `check_em_dash --base c6bd08c6`, the `gen_toc` checks, `check_nvm_capture`, `pp_srcs`, `lint_rtl` (90 ≤ 90) and `git diff --check` | `receipts/docs312/docs_gates.tsv` |
| Earlier gate run without the renderer | em_dash and the two gen_toc gates rc 2 ("renderer not installed"), everything else rc 0. This was an environment gap, closed by the run above | `receipts/docs/docs_gates.tsv` |
| Window instrumentation and grid shift (`scripts/probe_fixture_instrumentation.diff`, `run_shift.sh`, `window_drift.py`) | See F1 | `receipts/window_drift_note{1,8}.csv`, `receipts/shift*_*.log` |
| Hosted, exact head | `docs-check` success (job 114991328012). bdd-conformance, rtl-fast, verilator-lint, Yosys shards 0-3, yosys-elaboration, firmware jobs: success. **Verilator shard 4/5 (milan_dp): failure.** Shards 1-3 and `elaborate` were still running at 20:50Z | `hosted_checks_e893e4d1.tsv`, `receipts/hosted_shard4_counters_failure.txt` |
| Code equality | `hdl/` with comments stripped is identical from `7b491e59` to the head. All later commits change comments only | `receipts/hdl_code_equal_acadfacd_head.txt`, `scripts/hdl_code_equal.py` |

## Findings

### F2 - BLOCKER - Tests, Robustness

**Where:**
- `tb/verilator/milan_dp/stream_counters.py:121-122,138-139`: it captures `make -s print-dp-vflags` and `make -s print-srcs` stdout as tool arguments.
- `tb/verilator/milan_dp/Makefile:636` adds `$(MAKE) counters` to `run`.

**Authority and evidence:**
- AGENTS.md section 7 requires exact-head `verilator-suites` evidence after a PR is marked ready. The Tests lens requires that existing regressions stay green.
- The hosted Verilator shard 4/5 runs only `milan_dp`. It concluded `failure` at this head (run 38303342738, merge ref `ed36ebad` = `e893e4d1` into `dc4d06cb`). The suite tally reads "checks: 11956, in-suite failures: 0": every pre-existing leg passed, and the recipe failed afterwards.
- From the artifact `suite-logs-4` (sha256 `83e9d4d4…`, matching the upload digest), `make counters` ends in `CalledProcessError: Command '['verilator', '+incdir+…', 'make[2]:', 'Entering', 'directory', '…/tb/verilator/milan_dp', '--cc', …`, then `make[1]: *** [Makefile:668: counters] Error 1` and `make: *** [Makefile:561: run] Error 2`.
- The same failure occurred at `37944f8a` (run 38292138840) and `acadfacd` (run 38279786076) (`receipts/hosted_shard4_counters_failure.txt`).
- The cause: `scripts/run_all_suites.sh:394` runs `make -C <suite>`, which sets `-w`, and sub-makes inherit it. The driver's own `make -s` then prints "Entering directory" into the captured flags.
- Local reproduction at this head: `MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1` fails the same way. The simulator reports `Cannot find file containing module: 'make:'` (`receipts/repro_makeflags_w.log`).
- The author's direct invocations pass because no `-w` is inherited. Under the documented entry point, the standing fixture has never executed in hosted CI.

**Impact:**
- A required hosted context is red at the exact head, so the PR cannot merge.
- The whole milan_dp suite reports FAIL, which hides any future real regression in its other legs.
- None of the new packet, reset or cadence checks has hosted evidence.

**Required outcome:**
- The `counters` legs run correctly when reached through the suite runner (`make -C tb/verilator/milan_dp run`, which calls `$(MAKE) counters`). Flag and source capture must not depend on inherited print-directory or other make output flags.
- The hosted Verilator shard 4/5 succeeds at the new exact head.
- The PR's validation record names that hosted result.

**Verification:**
- `MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1` passes.
- `make -C tb/verilator/milan_dp counters` passes from the repository root.
- The hosted milan_dp shard concludes success, with the counters legs' `RESULT: PASS` visible in `suite-logs-4`.

### F1 - MAJOR - Conformance, Tests, Docs

**Where:**
- `tb/verilator/milan_dp/stream_counters.hpp:171-188`: a fixed grid from the start of measurement, with only windows 2-4 graded.
- `docs/testing/726_STREAM_COUNTERS.md:51-54,68`.
- The PR body: "Both recipients and every descriptor are measured in windows 2-4. All corrected row-windows contain one notification." and "Windows 0-1 record startup".
- `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:220-230`, which presents the measured window check as closing routine refresh.

**Authority and evidence:**
- Ruling 6126028604 judges item 2 by three bullets. Bullet 1: one notification per changed descriptor in each one-second window. Bullet 2: no two closer than the rate limit. Bullet 3: gaps of at most 1000 ms plus the measured service delay.
- AGENTS.md section 2: a conflict between a requirement and the implementation is published for a decision, not resolved privately. Section 6 (Tests): a test must not merely reproduce implementation assumptions.
- I added per-notification printing and an optional grid shift to a scratch copy of the fixture (`scripts/probe_fixture_instrumentation.diff`). RTL and checks were unchanged.
  - **Shipping shape.** Input 0 to recipient 0 is notified at 0.999742, 2.000742, 3.001742 and 4.002742 s. Window 1 is empty between two notifications 1001.0 ms apart.
  - **Largest shape.** Input 0 is notified at 0.999115 → 2.000115 s (recipient 0) and 0.999896 → 2.000878 s (recipient 1). Window 1 is empty for both recipients (`receipts/window_drift_note{1,8}.csv`).
  - This cadence was already running before t=0, so the empty window is the steady cadence crossing a window edge, not a startup effect. The document's reason for excluding windows 0-1 ("registration and startup transient", `726_STREAM_COUNTERS.md:52`) does not hold for these rows.
- The graded window 2 holds input 0's notification by 0.742 ms at the shipping shape and by 0.115 ms at the largest shape.
- With identical RTL and identical notification times, I moved the window grid later (`receipts/shift*.log`). The PR's own `[726 CADENCE] every complete steady window notified` then fails:
  - 0.8 ms later at the shipping shape: 1 failure.
  - 0.2 ms later at the largest shape: 1 failure.
  - 0.9 ms later at the largest shape: 2 failures.
  - Shifts of 0 and 0.3 ms pass.
- The cause is structural. The unchanged scheduler (`protocol-processor/hdl/aecp/KL_aecp_notify.sv:1100,1449`) waits 1000 ms after the latest recipient's completion. Every gap is therefore over 1000 ms (minimum 1000.982 ms), and each row drifts against any fixed grid. A fixed window is regularly skipped: about once per 700-1,000 windows per row at 1-1.5 ms drift, and more often where gaps reach 1012 ms. Bullet 1 cannot hold indefinitely under the ruling's own "no processor change". Bullets 2 and 3 hold, and they do not depend on the grid.
- R628-2-S1 raised the long-run drift as optional. What is new here:
  - the graded verdict itself depends on sub-millisecond alignment;
  - the check is a standing target in milan_dp `run`, so any change that moves setup timing by about 200 cycles can fail it on correct RTL;
  - the texts still attribute window 1 to startup;
  - no public decision says how bullet 1 applies.

**Impact:**
- The evidence offered for bullet 1 is an artifact of alignment, and the measured run contradicts bullet 1 in its own window 1.
- The merge-turn link-tap check can fail bullet 1 on correct behaviour whenever a capture spans a crossing.
- The standing regression is fragile, and a cold reader is told that every row-window holds one notification.

**Required outcome:**
- The conflict between bullet 1 and the unchanged scheduler's period of more than 1000 ms is published on the issue. A maintainer decides how steady-state windows are judged, for example whether bullets 2-3 govern and how a window skipped by drift is graded.
- The standing grading implements that decision. Its verdict on the corrected RTL must not depend on grid phase, and the `late`, `rate`, `tx-nodirty` and baseline plants must still fail by name.
- `726_STREAM_COUNTERS.md`, the PR body and the audit note describe the drift mechanism and state accurately which windows hold a notification.

**Verification:** at the new head, apply the reviewer instrumentation, then run `run_shift.sh` with shifts of 0, 200, 300, 800 and 900 µs at both shapes. Each shift gives the decided verdict on the corrected RTL, and the plants still fail by name.

### S1 - SUGGESTION - Robustness, RTL (carried from R628-1-S1 and R628-2-S3)

`hdl/ieee1722/crf/KL_crf_rx.sv:487-490` against `:644-665`. A CRF AVTPDU accepted in the exact bind-rise cycle is wiped from the new era's FRAMES_RX. The talker (`KL_talker_diag_ctx.sv:249`, `ftx_r <= {31'd0, ev_f_w[c]}`) and the AAF engine (`KL_avtp_rx_monitor_ctx.sv:1159`) keep the coincident event. The loss is at most one packet per bind, and ordering a coincident packet before the reset is defensible. Optional.

### S2 - SUGGESTION - Tests (carried from R628-2-S2, not taken)

`stream_counters.hpp:171-180` grades gaps over every logged notification, including those after `counter_watch_on` is cleared at `:87`, when service is no longer measured. Optional: grade only up to the end of the measured window.

### S3 - SUGGESTION - Tests (carried from R628-1-S2 and R628-2-S4, not taken)

`tb/verilator/milan_dp/sim_nxn.cpp:2596`: the `10000000L` "below silence timeout" bound is tied to the notify build's default clock. Optional: derive it from the clock parameter.

### R1 - RESIDUE - Docs

The PR body Status still reads "Local source head: `e893e4d1…`" and "The new commits remain local pending authorized publication." The commit is now the published PR head.

Exact fix: change "Local source head" to "Source head". Delete the sentence "The new commits remain local pending authorized publication."

## Clean-lens lines

[R628] PASS RTL - `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:196-257`, `hdl/ieee1722/crf/KL_crf_rx.sv:359-396,455-520,640-698`, `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:329-330,436-460,632-643,943-953,976-985,1153-1175`, `hdl/milan/milan_datapath.sv:3156-3171,3300-3322,7915-7995`, gitlinks at base and head - The production logic was checked against ruling 6125741685 (one FRAMES_TX/RX count per AVTPDU, 32-bit wrap, start and bind resets) and against ruling 6126028604 (healthy updates mark dirty, the scheduler alone limits, no processor change). Findings:
- FRAMES_TX increments on each `ev_f_w`. The start edge takes precedence and keeps a coincident PDU.
- CRF `pdu_count_o` increments per `w_acc`. The bind-rise wipe is on the rising edge only.
- The AAF batch `frx_acc_r`/`frx_add_r` is 32-bit, with the commit at `:642` and no truncation.
- The CRF strobe skid is unchanged and lossless at the documented rates.
- Dirty pulses feed the sticky per-descriptor pending bits, so per-PDU pulses coalesce. The AVB_INTERFACE (`ctr_avb_dirty_w`) and CLOCK_DOMAIN paths are untouched, so the #60 throttle stays.
- All registers are reset. Lint 90 ≤ 90.
- Submodule gitlinks are identical at base and head. Production logic is unchanged since `7b491e59`, and later commits change comments only.
- Area: the author's routed utilization at that logic reads 49,427 LUT, 53,378 FF and 87.5 BRAM, +35 LUT against the author-reported 49,392 base, below the +200 STOP bound. Author-reported WNS/WHS are +0.451/+0.036 ns. I did not reproduce these.

[R628] Robustness UNCLEAN (F2) - covered: the reviewer plants (`crf-unbind-wipe`, `tx-saturate`, `aaf-guard`, `crf-guard`), the PR's reset, saturation and boundary plants (65,534 + 3 packets), the unpublished-zero startup snapshot, the start-coincident PDU, and the no-CRF-sink generate branch (`milan_datapath.sv:7925-7929`). F2 is configuration-dependent behaviour of the new driver. S1 is optional.

[R628] Conformance UNCLEAN (F1) - acceptance items 1 and 4 are met in simulation and in the texts. For item 2, the per-descriptor dirty producers, rate limit and gap bound hold, but the bullet-1 window evidence is invalid (F1). Item 3 and the reference-peer reset comparison are merge-turn bench work.

[R628] Tests UNCLEAN (F1, F2) - the plants and escapes all reproduce, and my four extra plants and two grader-guard plants are detected. The standing target is red in hosted CI (F2), and the cadence grade depends on grid alignment (F1).

[R628] Docs UNCLEAN (F1) - REGISTER_MAP `:145-153,866-872,919,963`, the audit note `:220-230`, the AECP README `:55-65` (COUNTERS bit 3, value 8), the design notes in the four HDL files, the five dated findings notes, `tb/verilator/milan_dp/README.md:465,499-501,587,1158` and the feature law table all match the ruling. `726_STREAM_COUNTERS.md:52,68` and the PR body misstate the windows (F1). R1 is residue.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | four HDL counter engines, datapath arbiter, window fixture and its instrumented runs, rulings 6125741685/6125845117/6126028604 | R628-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| RTL | CLEAN | lines in the RTL PASS line above; lint; code equality since 7b491e59; author routed utilization | R628-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| Robustness | UNCLEAN (F2) | reviewer and PR plants, snapshot probe, driver under an inherited `-w` | R628-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| Tests | UNCLEAN (F1, F2) | behave 406, grader 80, 9+2 PR plants, 4 reviewer RTL plants, 2 grader plants, unit suites and campaigns, hosted shard 4/5 | R628-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |
| Docs | UNCLEAN (F1) | 726_STREAM_COUNTERS.md, REGISTER_MAP, audit, AECP README, milan_dp README, findings notes, feature file, PR body | R628-3 | e893e4d13d99eb5ba00745f0f5cf74ee847972c2 |

## Prior public review findings: status at this head

| Finding | Status and evidence |
|---|---|
| R628-1-F1 / R629-1-F01 (MAJOR, Tests) | Resolved. The era-wipe step checks ten counters and six flags (`counters_contract_steps.py:601-625`). Behave 406/0. `reproduce_contract.py` rc 0. Hosted bdd-conformance success at this head. |
| R629-1-F02 (RESIDUE) | Resolved. The sentence is absent from the PR body. |
| R628-1-F2 (MINOR) | Resolved. The frames-only legs pass at both shapes. tx-nodirty gives 16 OUTPUT_CADENCE failures and escapes. The `before` driver requires the named TX/RX/CADENCE groups. |
| R628-1-F3 (MINOR) | Resolved. The four README passages match the per-AVTPDU law. |
| R628-1-F4 (MINOR) | Resolved. The law table, trap (3) and the grader use Table 7.157. The interval-rate FAIL scenario passes. |
| R628-2-F1 (MAJOR, docs workflow) | Resolved. My 46 gate commands return rc 0 with no budget file changed. Only `scripts/measure_test_evidence_readers.py` changed, adding the `stream_counters.py` disposition. The `dirty_p_o` boundary again names its unit ("one clk_i cycle per update"), and the naming gate records 95 of 95. Hosted docs-check success at this head. |
| R628-2-F2 (MINOR, cross-device helpers) | Resolved. `probe_xside_law.py` (unchanged) gives PASS for the ruled pair and FAIL with the finding against the interval-rate side. My suppression plant is detected (78-test escape). |
| R629-2-F01 (MINOR, unpublished zero) | Resolved. `probe_snapshot.py` (unchanged) passes. The standing scenario and self-test exist. Restoring the guard fails `test_unpublished_zero_receive_snapshot` (79-test escape). |
| R628-2 RS1-RS5 (RESIDUE) | Resolved: README bit 3/value 8, rows [G]/[H] per-run, harness banners, the 131-column banner rewrapped, self-test names. |
| R628-2-S1 (SUGGESTION, window drift) | Superseded by F1 on new evidence (grid-shift failure of the graded check). |
| R628-2-S2, R628-1-S1 / R628-2-S3, R628-1-S2 / R628-2-S4 | Retained as optional S2, S1 and S3. |

None of the prior rounds recorded the hosted milan_dp shard failure (F2), although it was present at `acadfacd` and `37944f8a`.

## Real limits

- No hardware or physical calibration was run. The parent window runs use compressed simulated time, with protocol ms at 1000 cycles and finite five-window runs. Field skips are not hardware proof.
- I ran no Vivado. Area and timing are author-reported; the 49,392-LUT base figure was not reproduced.
- I did not run the full parent, processor, gPTP, Yosys or builder banks. Hosted Verilator shards 1-3 and `elaborate` were still running at 20:50Z.
- These docs-workflow commands were not run locally: `gen_hdl_reference`, the wavedrom checks, the remaining `--selftest` arms, the RV32 SDK and builder steps, `make -C gptp-processor docs` (it would write into the submodule), and `act_ci.py --selftest` (not permitted here). The hosted docs-check success covers the complete workflow.
- The F5 mailbox check exercises the core and adapter with injected `aecp_changed()` calls. The opt-in F5 application layer has no production caller that raises the COUNTERS event (`ctrl_app_aecp_changed` is defined but uncalled). F5 is not the shipping image, so I record this as a limit, not a finding.
- The published `probe_snapshot.py` differs from R629-2's manifest hash (a sanitized `$VALIDATION_TOOLS` placeholder). I ran the published bytes.
- I did not retrieve the standards texts myself. The maintainer rulings govern.

## Pending manager duties

- Publish the F1 conflict for a maintainer decision on bullet 1, before the merge-turn link-tap measurement.
- Accept the exact-head hosted contexts after F2 is fixed, including Verilator shards 1-4 and `elaborate`.
- Build the current-dev merge candidate (source base `c6bd08c6`, live dev `dc4d06cb`) with the builder and native banks, and link their receipts.
- Merge-turn bench work: the controller (la_avdecc or Hive) shows DUT FRAMES_TX at about 8,000/s and Stream Input refresh side by side with the reference peer; the talker-start and bind reset comparison with the peer; per-descriptor intervals on the link tap at both shapes.
- Carry R1 to the residue checklist.

## Restore verification

`receipts/restore_and_identity.txt`:
- HEAD `e893e4d1…`, tree `0e94807e…`.
- Worktree and index match HEAD, with 0 untracked or ignored entries. I removed the Python caches I created, including one in `protocol-processor`.
- The `git ls-files -s` and `ls-tree -r` digests are equal (`6c8c38d6…`).
- The gitlinks for `external`, `gptp-processor`, `protocol-processor`, `third_party/lwSRP` and `third_party/verilog-axis` match the base. The checked-out submodules are clean at their gitlinks.
- All plants and instrumentation ran on scratch copies only.

## Reproduction

The scripts are in `scripts/`:
- `bg.sh` and `wait.sh` launch and wait on campaigns.
- `docs_gates.sh REPO OUT` runs the documentation gates.
- `probe_variants.py REPO VARIANT WORK` runs the extra RTL plants.
- `probe_grader_guards.py REPO SCRATCH` runs the grader-guard plants.
- `probe_fixture_instrumentation.diff` is applied to a copy of `stream_counters.hpp`. Then run `run_shift.sh WORK SHIFT_CYCLES LOG` and `window_drift.py LOG`.
- `hdl_code_equal.py REPO OLD NEW` compares HDL with comments stripped.

For F2: `MAKEFLAGS=" -w" python3 tb/verilator/milan_dp/stream_counters.py --shape 1`.

R628-3 FINISHED
