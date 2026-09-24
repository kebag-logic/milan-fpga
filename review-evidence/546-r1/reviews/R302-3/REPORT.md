[R302] POSITIVE - exact head 0c61d458941088f3847513b7c6fe6589c75b4270

# R302-3 internal independent review: issue #546 / PR #554

- Round: R302-3, cleared-context internal reviewer.
- Exact head: `0c61d458941088f3847513b7c6fe6589c75b4270`, tree `88a5ce9545a23561beae21d3e0323a9d1fb0d051`.
- Source base: `57456af96b3127b9d309a995bbbd35a6113ce52d`. Five commits. Round 3 adds `28b6bfd38` and `0c61d4589` on top of `d04a61678`.
  Both are one-line subjects with no body or trailers.
- Lenses applied at this head: Conformance, RTL, Robustness, Tests, Docs. All five were applied, and all five are clean.
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR is open. Two suggestions carried over from round 2 remain optional, and one new suggestion is added.
- The round-2 MINOR (R302-2-F1 = R303-2-F1) is resolved at this head. So are R303-2 S1 and S2.

## Reconstruction

Read in this order:

1. `AGENTS.md`, `CONTRIBUTING.md` and `docs/README.md`.
2. The issue #546 body (Observed, Authority, Acceptance 1-3).
3. The manager's round-3 assignment [A278] (issue comment 5820794596) and `[A278] REVIEW READY` (5821287408).
4. The round-3 diff `d04a61678..0c61d4589` (5 files, +43/-7), then the whole PR diff `57456af96..0c61d4589` (22 files).
5. The current PR #554 body.
6. The public evidence tree `review-evidence/546-r1` at `148f1a2e`, including `author-r3/`.
7. The exact-head hosted check runs.

Clause texts are the ones this reviewer extracted in round 2 from the primary sources: Milan v1.2 Annex B.1.1 and section 7.4, and IEEE 802.1AS-2011 and -2020 Annex B.1.1. They are republished here as `receipts/clause_texts_from_R302-2.txt`.
The public R303-2 findings were read only after the independent pass over the diff and the probe design were complete.

Frozen acceptance (unchanged since round 1):

1. Discard the CRF rate sample that spans a talker discontinuity (a tu toggle or a step-shaped jump), in simulation, with a failing arm.
2. A GM-change scenario with steps at both ends keeps the servo locked, or produces exactly one counted re-lock.
3. Gates green.

Round-3 assignment items:

1. The RTL comment, `TIME_SYNC.md` and the PR body cite IEEE 802.1AS Annex B.1.1 for the +/-100 ppm LocalClock bound, as the assumption for the media oscillator.
   They cite Milan v1.2 section 7.4 for the +/-50 ppm media-source bound, and keep 100 ppm as a conservative margin.
   The claim that there is no independent media-clock clause is removed.
   The comment-free RTL stays identical, and `TS_JUMP_NS_C` stays 2048.
2. Taken suggestion R303-2 S1: add a U13 resume check that fails for a servo that never resumes PI.
3. Taken suggestion R303-2 S2 (= R302-2 S1): correct the evidence-gate disposition text.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### Suggestions (non-blocking; they do not affect coverage)

- **R302-3 S1, `Docs`, PR #554 body, "Status" section.**
  - The body says "Round 3 is committed locally ... Publication and independent re-review remain pending."
  - At this head the commit is published: the PR head equals `0c61d4589` and the hosted checks ran on it.
  - Optional: refresh the status line when the PR body is next edited, for example at the merge turn.
- **R302-2 S2, retained, `Tests`, `tb/verilator/crf_rx/sim_talker_step.cpp:33-40`.**
  - The six events still run in sequence from one lock, so per-event attribution under a mutant is not independent.
  - The gate verdict is correct.
  - This was optional and was not taken.
- **R302-2 S3, retained, `Tests`, `tb/verilator/crf_rx/mutants.py:19-28`.**
  - Receiver mutants in the default campaign still run only against `sim_discontinuity.cpp`.
  - The connected harness's rejection of detector removal is shown by reviewer probes, not by a gate.
  - This was optional and was not taken. The reviewer probes still show the rejection at this head (see Executed evidence).

## Round-3 items verified

### Item 1: citation fix (resolves R302-2-F1 = R303-2-F1)

- **`hdl/ieee1722/crf/KL_crf_rx.sv:275-277`** reads: "Assume the media oscillator meets IEEE 802.1AS Annex B.1.1's +/-100 ppm LocalClock bound. Milan v1.2 section 7.4 requires media sources better than +/-50 ppm; 100 ppm is a conservative margin."
- **`docs/design/TIME_SYNC.md:191-201`** reads: "LocalClock frequency must stay within +/-100 ppm. See IEEE 802.1AS Annex B.1.1. We assume that bound also applies to the media oscillator. Milan v1.2 section 7.4 constrains media clock sources. Their frequency tolerance must be better than +/-50 ppm. Using 100 ppm therefore adds conservative margin."
- **The PR body, Description, second paragraph**, says the same: the 802.1AS Annex B.1.1 bound is the stated assumption, section 7.4's better-than-50 ppm follows, and 100 ppm "retains conservative margin".
- **Against the clauses** (`receipts/clause_texts_from_R302-2.txt`):
  - 802.1AS-2011 and -2020 B.1.1: "shall be within +/-100 ppm".
  - Milan v1.2 7.4: "frequency tolerance is better than +/-50PPM".
  - All three locations match the clauses and agree with each other.
  - They also agree with the repository's compliance matrix: `docs/reference/MILAN_COMPLIANCE_MATRIX.md:182` (7.4, +/-50 ppm) and `:228` (802.1AS Annex B.1.1, +/-100 ppm).
  - "Milan Annex B.1.1" is now cited only for the tu rule, which is what that clause states (`REGISTER_MAP.md:750`, `KL_ptp_clock_validity.sv:36`).
- **The false claim is gone.** "rather than an independent media-clock clause" appears nowhere in the tree or in the PR body.
- **Comment-free RTL is unchanged** (`receipts/rtl_identity_d04a_to_head.txt`).
  - All 76 tracked HDL files under `hdl/` (`.sv/.v/.svh/.vh`) were compared, comments stripped and whitespace folded, between `d04a61678` and the head. There are 0 mismatches.
  - One file changed at the byte level (`KL_crf_rx.sv`), and it changed in comments only.
  - `KL_mmcm_drp_servo.sv` and `milan_datapath.sv` are byte-identical.
  - The same check from round 1 (`39a0171c8`) to the head also passes (`receipts/rtl_identity_r1_to_head.txt`).
  - Negative control: base `57456af96` against the head reports the 3 real logic changes and exits 1 (`receipts/rtl_identity_negative_control_base_to_head.txt`).
- **Thresholds are unchanged.** Elaborated with the pinned simulator at both `d04a61678` and the head (`receipts/param_elab.txt`): `RATE_DRIFT_NS_C = 601` and `TS_JUMP_NS_C = 2048`.

### Item 2: R303-2 S1, U13 PI-resume check

- **Where it lives.** `tb/verilator/mmcm_servo/sim_main.cpp:598-608`. After validity returns, the check applies a valid +10 ppm offset (`rate_for_ppm(+90)` against the +80 ppm baseline). It requires `trim() > resumed + 5 * 16` (more than 5 ppm at x16) within 24 ms, and that LOCKED holds.
  Restoring the original rate must also keep LOCKED. The header comment at line 29 lists U13.
- **The mutant.** `tb/verilator/crf_rx/mutants.py:98-113`, `servo_never_resumes`, adds a reset-cleared sticky `invalid_seen_r` and ANDs `!invalid_seen_r` into the `pp_run_r` term (`KL_mmcm_drp_servo.sv:572-573`).
  Both anchors are single-match guarded. The mutant runs in the default `make` (`Makefile:53`, `all: run mutants`).
- **Reviewer probes** (`scripts/resume_probes.py`, `receipts/resume/SUMMARY.txt`, overall PASS):

  | Row | Harness | Servo | Result |
  |---|---|---|---|
  | head_clean | head | head | PASS, 85 checks / 0 failures |
  | head_never_resumes | head | shipped mutant | killed. Exactly 1 failure: `[U13] valid offset resumes PI trim` |
  | prior_never_resumes | `d04a61678` | shipped mutant | PASS (82/0). The round-2 U13 could not see this defect, so the new check is what detects it |
  | head_no_offset | head, with the +90 ppm offset replaced by the clean rate | head | fails the resume check. Settling and ripple alone do not satisfy it |
  | head_instrumented | head plus one printf | head | trim 1495 to 1735: delta 240 LSB (15 ppm) against the > 80 LSB requirement, a 3x margin |
  | head_resume_on_idle_only | head | reviewer variant: PI stays off after invalidity until CRF is deselected | killed by the same named check |

- **Shipped default target at this head** (`receipts/crf_rx-make-all.log`): the campaign has 8 checks and 0 failures.
  `servo_never_resumes` is rejected by `[U13] valid offset resumes PI trim`, and `servo_ignores_valid` by `[U13] invalid remote sample holds trim`.

### Item 3: R303-2 S2 = R302-2 S1, disposition text

- `scripts/measure_test_evidence.py:597-600` now reads: "copies the receiver and servo, requiring named failures for tu, jump, refill, accept-edge, ignored-validity and PI-resume defects; no expectations read from RTL".
- That matches `mutants.py` exactly: `tu_ignored`, `jump_removed`, `refill_short`, `accept_edge_late`, `servo_ignores_valid`, `servo_never_resumes`, which read `RTL` and `SERVO`.
- Expectations are named harness checks, not values read from RTL.
- `measure_test_evidence.py --check` passes in the clone (`receipts/doc_source_gates.txt`).

## Lens results (clean lenses in the finding format)

```text
[R302] PASS Conformance - hdl/ieee1722/crf/KL_crf_rx.sv:274-289; docs/design/TIME_SYNC.md:167-229; PR #554 body (Description, Round 3); receipts/clause_texts_from_R302-2.txt; receipts/param_elab.txt; receipts/probes/SUMMARY.txt; receipts/crf_rx-make-all.log; receipts/hosted_check_runs.tsv - the round-3 citations match Milan v1.2 7.4 (+/-50 ppm, better-than) and IEEE 802.1AS-2011/-2020 Annex B.1.1 (+/-100 ppm), and agree with MILAN_COMPLIANCE_MATRIX.md:182,228. The false no-clause claim is gone, and assignment item 1 is met in all three locations. Against acceptance at this head: AC1, detection plus failing arms (disc harness 1658/0; 4 receiver mutants in the default gate; 15 receiver/servo mutants in the reviewer campaign, all killed as expected). AC2, both-end events at 100 ms and 600 ms lag stay LOCKED with one counted local step each (talker_step 69/0; loop lag sweep PASS). AC3, the focused suites pass here, the exact-head hosted contexts are 21 success and 1 skipped, and the manager's source banks are reported passed. IEEE 1722-2016 4.4.4.3/4.4.4.7/10.4.3/10.4.5 citations are unchanged since round 2, where they were checked against the clause text. Scope held: no CSR or counter was added; telemetry stays with #495 by decision.
[R302] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv (all), hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:240-820, hdl/milan/milan_datapath.sv instances; receipts/rtl_identity_d04a_to_head.txt, rtl_identity_r1_to_head.txt, rtl_identity_negative_control_base_to_head.txt, param_elab.txt - the round-3 RTL delta is comment-only across all 76 tracked HDL files (servo and datapath byte-identical), and the checker detects real edits (negative control rc 1). RATE_DRIFT_NS_C 601 and TS_JUMP_NS_C 2048 elaborate identically at d04a61678 and at the head. The logic reviewed clean in round 2 is therefore the logic here: one clock domain (both instances on axis_clk), 64-bit spacing, unsigned bounds, pend/break ordering, accept-edge veto, reset of every new register, and the single crf_rate_valid_i term in pp_run_r. Hosted verilator-lint, elaborate, yosys-elaboration and yosys-portability succeeded at this head.
[R302] PASS Robustness - receipts/probes/SUMMARY.txt (47 rows, campaign PASS, row-for-row identical to R302-2), receipts/probes/clean__jitter.log, clean__loop_*.log; receipts/resume/SUMMARY.txt - the round-2 campaign was re-run unchanged at this head: probe sources and drivers are byte-identical to the R302-2 packet, and only the head guard was retargeted. Results: jitter/drift false-positive probe clean; tu held, tu-only, step inside held tu, 20 us step, listener-first, repeated GM changes, quiet traffic and the 100-500 ms lag sweep all keep LOCKED; seq gap, silence, rebind, STOP, refill +/-1, validity leak on break, uncancelled pending update, threshold x2 and /2, 32-bit spacing, removed lower bound, removed detection and ignored servo validity are each killed. New at this head: invalid-then-valid resume is now guarded; two non-resume servo shapes (sticky latch; resume only after deselection) are both killed by the named U13 check.
[R302] PASS Tests - tb/verilator/mmcm_servo/sim_main.cpp:29,585-609; tb/verilator/crf_rx/mutants.py:1-120; tb/verilator/crf_rx/Makefile:53-79; tb/verilator/mmcm_servo/Makefile:55-61; receipts/crf_rx-make-all.log, mmcm_servo-make.log, resume/*, harness/SUMMARY.txt - default crf_rx rc 0 (13 836/0, 1 658/0, 69/0; campaign 8/8 with named rejections). mmcm_servo rc 0 (85/0 unit including U13, 8/0 rails, 113/0 PHC step). The new U13 check fails for the defect it names, and only through the new check: the shipped mutant escapes the round-2 U13, and with no offset the check fails, so ripple cannot pass it (margin 240 against >80 LSB). Harness-integrity probes re-run unchanged: post-edge sampling, a never-matching boundary predicate and an ignored-invalid-boundary tally are each killed by the named check. Existing regressions stay green. S2 and S3 from round 2 remain optional suggestions.
[R302] PASS Docs - docs/design/TIME_SYNC.md:187-229; hdl/ieee1722/crf/KL_crf_rx.sv:274-285; scripts/measure_test_evidence.py:597-600; docs/testing/TESTING.md:462; PR #554 body; issue #546 comments 5820794596, 5821287408; receipts/doc_source_gates.txt, em_dash_grep.txt - the design page, RTL comment and PR body state the corrected authorities consistently. The disposition names the servo read and all six mutant classes. TESTING.md's "servo-validity mutants" covers both servo mutants. U13's header line and the PR body's description of the check match the code (+10 ppm, >5 ppm, 24 ms, LOCKED held). No added line in 57456af96..head carries U+2014 or U+2013 (889 lines scanned). Local gates: check_doc_style, check_doc_paths, gen_module_matrix --check, measure_test_evidence --check, check_py_idiom and check_cpp_idiom rc 0. gen_toc could not run here (pinned renderer absent); hosted docs-check and docs-check-no-git succeeded at this head. S1 (stale PR status line) is a suggestion only.
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #546 AC1-3, [A278] assignment and #495 decision; `KL_crf_rx.sv:274-289`; `TIME_SYNC.md:167-229`; PR body; Milan v1.2 B.1.1 and 7.4; IEEE 802.1AS-2011/-2020 B.1.1; `MILAN_COMPLIANCE_MATRIX.md:182,228`; threshold elaboration; campaign and default-gate results; hosted runs | R302-3 | `0c61d458941088f3847513b7c6fe6589c75b4270` |
| RTL | CLEAN | Comment-free identity of all 76 HDL files versus `d04a61678` and `39a0171c8`, with a negative control; servo and datapath byte identity; `RATE_DRIFT_NS_C`/`TS_JUMP_NS_C` elaboration at both heads; hosted lint, elaboration and Yosys | R302-3 | `0c61d458941088f3847513b7c6fe6589c75b4270` |
| Robustness | CLEAN | Round-2 campaign re-run unchanged (47 rows, identical to R302-2); U13 resume probes including a second non-resume shape | R302-3 | `0c61d458941088f3847513b7c6fe6589c75b4270` |
| Tests | CLEAN (R302-2 S2, S3 suggestions retained) | `sim_main.cpp` U13, `mutants.py`, both Makefiles; default crf_rx and mmcm_servo targets; 6 resume probe rows; 4 harness-integrity rows | R302-3 | `0c61d458941088f3847513b7c6fe6589c75b4270` |
| Docs | CLEAN (R302-3 S1 suggestion) | `TIME_SYNC.md`, RTL comments, `measure_test_evidence.py` disposition, `TESTING.md:462`, U13 header, PR body, REVIEW READY; local doc/source gates; em-dash scan; hosted docs-check | R302-3 | `0c61d458941088f3847513b7c6fe6589c75b4270` |

All five lenses are banked against the exact head under review. No later commit exists.

## Prior public findings on this PR

| Prior finding | Status at `0c61d4589` | Evidence |
|---|---|---|
| R302-1-F1 = R303-1 F1 MAJOR (Tests, Docs): the connected harness could not fail for the defect | Resolved in round 2; **still resolved** | The `rx_no_detection`, `jump_removed` and `lower_bound_removed` talker rows FAIL and the clean row passes at this head (`receipts/probes/SUMMARY.txt`) |
| R302-1 S2 = R303-1 F3 (Tests, Docs): mutation arm in no gate | Resolved in round 2; **still resolved** | `Makefile:53` `all: run mutants`; the campaign runs 8 controls by default |
| R302-2-F1 = R303-2-F1 MINOR (Conformance, Docs): media bound cites a clause that does not state it | **Resolved** | See item 1. All three locations cite 802.1AS B.1.1 and Milan 7.4 correctly; the no-clause claim is removed; RTL logic and thresholds unchanged |
| R303-2 S1 (Tests): U13 cannot fail for a servo that never resumes PI | **Resolved** | See item 2. The mutant is killed in the default campaign by the new named check, and it escapes the prior U13 |
| R303-2 S2 = R302-2 S1 (Docs): stale disposition text | **Resolved** | See item 3 |
| R302-2 S2, S3 (Tests): per-event attribution; receiver mutant against talker_step in the gate | **Retained as suggestions** (optional, not taken) | See Suggestions |
| R302-1 S4 = R303-1 S1 (Robustness): uncounted discards | **Out of scope by decision** (#495) | Round-2 manager assignment |

## Executed evidence at this head (reviewer-run)

- Tool: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
- All builds ran from `git archive` extractions in disposable scratch trees.
- The clone was only read, apart from the read-only `--check` style gates listed below.
- CPU use was confined to 8 cores (`taskset -c 0-7`). Local paths in receipts are placeholders. Compiler command lines and build-only logs are not published.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/crf_rx` (default: unit, discontinuity, talker_step, mutants) | rc 0 in 9 min 38 s; 13 836/0, 1 658/0, 69/0; campaign 8/8 with named rejections | `receipts/crf_rx-make-all.log` |
| `make -C tb/verilator/mmcm_servo` (default) | rc 0; 85/0 unit including 7 U13 checks; 8/0 rails; 113/0 PHC step | `receipts/mmcm_servo-make.log` |
| U13 resume probes (`scripts/resume_probes.py`) | overall PASS, 6 rows as tabled above | `receipts/resume/` |
| Round-2 campaign, unchanged (`probes/` and `scripts/run_probes_r2.py` byte-identical to R302-2), via `scripts/run_probes_r3.py` (head guard only) | campaign PASS, 47 rows, identical to R302-2 | `receipts/run_probes_r3.stdout`, `receipts/probes/` |
| Harness-integrity probes (`scripts/harness_probes.py`, byte-identical), via `scripts/harness_probes_r3.py` | campaign PASS: clean PASS; 3 of 3 killed by the named check | `receipts/harness_probes.stdout`, `receipts/harness/` |
| RTL identity (`scripts/rtl_identity.py`) | `d04a61678` to head PASS; `39a0171c8` to head PASS; negative control against base FAIL as designed | `receipts/rtl_identity_*.txt` |
| Threshold elaboration (`scripts/param_elab.sh`) | 601 / 2048 at both heads | `receipts/param_elab.txt` |
| Doc and source gates (read-only `--check` modes) | 6 rc 0; gen_toc not runnable (renderer absent) | `receipts/doc_source_gates.txt` |
| Dash scan of added lines | 0 of 889 | `receipts/em_dash_grep.txt` |
| Hosted check runs at the head (read only) | 21 completed success; `Physical gPTP (nightly and manual)` skipped (not executed) | `receipts/hosted_check_runs.tsv` |
| Clone integrity after all probes | HEAD and tree exact; worktree and index clean; index equals tree; no skip or assume flags; 4 gitlinks equal the head tree (and the base); 885 tracked files re-hash equal, modes equal | `receipts/clone_integrity.txt` |

Process note, for transparency:

- The first launch of the round-2 campaign ran past a tool time limit and kept running unseen.
- A second launch overlapped it for about 25 minutes. Both used the same scratch and receipt paths, and both were pinned to the same 8 cores, but together they briefly exceeded 8 worker processes.
- Both runs' outputs were discarded, kept only in unpublished scratch. The second run was stopped. The campaign was then run once alone, and that clean run is the one published.
- The run that was not interrupted also reported campaign PASS.

The informative row `clean loop:subthreshold` is unchanged from rounds 1 and 2, and is a limit, not a finding:

- An unmarked 2 000 ns talker step sits below the 2 048 ns backstop by construction.
- The integrator moved from 30.723 to 28.770 ppm, with no receiver unlock.
- A compliant talker marks a GM change with tu, and the smallest step is 20 us.

## Real limits

- Simulation only. Physical calibration was NOT RUN. No hardware, bench or field result backs this review, and skipped hosted contexts are not hardware proof.
- Timing: `rate_valid_o` still feeds `pp_run_r` combinationally, through a 64-bit subtract and two compares at 100 MHz. No timing closure was run or seen for this head.
- The false-positive probe models bounded uniform timestamp jitter. No foreign talker's CRF timestamp statistics were measured.
- The media-bound derivation rests on two stated assumptions: the media oscillator meets the LocalClock bound, and the remote talker shares this design's PHC envelope. They are now correctly cited and stated, not proven.
- This reviewer did not run the full parent, processor, gPTP, Yosys or builder banks, the lint ratchet, the xvlog gate, or gen_toc. The manager's public source-bank results and the hosted results were read, not reproduced.
- Source validation here is against base `57456af96`. The final candidate against live `dev` (`573f0052a0e4412e81f0845438fcec2086ce5d55`) is not validated by this review.

## Pending manager duties

- Publish this report and the manifest-listed files.
- Obtain the external reviewer's round-3 verdict. Merge needs two independent positive reviews and the full completion bar.
- Build and validate the final candidate against live `dev` at the merge turn, and own act and hosted acceptance for the head that merges.
  Any new commit un-covers the lenses whose scope it touches.
- Optionally refresh the PR body's Status line (R302-3 S1).
- Keep the physical-calibration and timing limits visible in any completion ledger.

R302-3 FINISHED
