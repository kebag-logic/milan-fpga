[R302] NEGATIVE - exact head d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1

# R302-2 internal independent review: issue #546 / PR #554

- Round: R302-2, cleared-context internal reviewer.
- Exact head: `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1`, tree `6ec524af62e911061e712e43313c27b0c9280561`.
- Source base: `57456af96b3127b9d309a995bbbd35a6113ce52d`. Three commits: `39a0171c8` (round 1), `8f432ba77`, `d04a61678` (round 2).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs. All five were applied at this head.
- Verdict: NEGATIVE. One MINOR is open under `Conformance` and `Docs`. `RTL`, `Robustness` and `Tests` are covered clean.
- The round-1 MAJOR (R302-1-F1 = R303-1 F1) is resolved at this head. The receiver mutation arm is now gated.
  The remaining defect is text only. The threshold value and all behavior are unaffected.

## Reconstruction

Read in this order: `AGENTS.md`, `CONTRIBUTING.md` (verification bar, documentation and citation rules), `docs/README.md`.
Then the issue #546 body (Observed, Authority, Acceptance 1-3), the executor assignment, `[A264] REVIEW READY`, the round-2
assignment `[A271]` (items 1-3, optional suggestions, and the manager decision moving receiver-discard telemetry to #495),
and `[A271] REVIEW READY`. Then the diff `57456af96..d04a61678` (22 files, +831/-29) and the round-2 slice `39a0171c8..d04a61678`
(10 files, +195/-64). Primary sources for the cited clauses: Milan v1.2 consolidated specification (Annex B.1.1, section 7.4),
IEEE 802.1AS-2011 and -2020 (Annex B.1.1), IEEE 1722-2016 (4.4.4.3, 4.4.4.7, 10.4.3, 10.4.5). Then the PR #554 body, the
public evidence tree `review-evidence/546-r1` at `3b8efe4dcc`, and the exact-head hosted check runs.
Prior review findings (R302-1, R303-1) were read only after the independent pass below was complete.

Frozen acceptance used:

1. Discard the CRF rate sample spanning a talker discontinuity (tu toggle or step-shaped jump), in simulation with a failing arm.
2. A GM-change scenario with steps at both ends keeps the servo locked, or gives exactly one counted re-lock.
3. Gates green.

Round-2 required items (assignment): (1) connected harness discriminates with a guaranteed boundary inside the contaminated
interval and samples validity as the servo does; (2) the 100 ppm term's derivation cites what the authority actually states;
(3) the receiver mutation arm runs in a gate and the servo-validity mutant is committed.

## Finding

### R302-2-F1 MINOR, lenses `Conformance` and `Docs`: the media-bound derivation still cites a clause that does not state it

- Location: `hdl/ieee1722/crf/KL_crf_rx.sv:275-276` ("inherits the +/-100 ppm LocalClock bound (Milan Annex B.1.1), rather than an
  independent media-clock clause"); `docs/design/TIME_SYNC.md:191-195` ("See Milan v1.2 Annex B.1.1."); PR #554 body, Description,
  second paragraph ("LocalClock bound from Milan v1.2 Annex B.1.1").
- Authority and evidence (clause excerpts in `receipts/clause_texts.txt`):
  - Milan v1.2 Annex B.1.1 is "tu (timestamp uncertain) field: ... the tu bit shall be set to 1 for the duration of 0.25 seconds".
    It states no frequency bound. The repository itself cites it that way at `docs/reference/REGISTER_MAP.md:750` and
    `hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:36`, and the issue's Authority line uses it for tu.
  - The +/-100 ppm LocalClock frequency accuracy is IEEE 802.1AS Annex B.1.1 (2011 and 2020). That is the row at
    `docs/reference/MILAN_COMPLIANCE_MATRIX.md:228`, which sits under section 4, "IEEE 802.1AS-2011".
  - The comment's premise that there is no independent media-clock clause is not correct. Milan v1.2 section 7.4, "Media Clock
    Source Quality", requires media-clock source oscillators better than +/-50 ppm (per AES11).
  - `CONTRIBUTING.md` section 6: compliance references cite the specification clause. Round-2 assignment item 2 and R303-1 F2 required
    the derivation to cite what the authority actually states.
  - Reviewer note: the round-1 suggestion R302-1 S1 said "the repository reads B.1.1 as the LocalClock bound" without naming the
    802.1AS annex. The round-2 text follows that wording. This finding corrects the imprecision; it does not fault the approach.
- Impact: not functional. The threshold stays at 2048 ns under either correct source.
  With 802.1AS 100 ppm: `ceil(2e6 * 300 / 999900) = 601`, `601 + 768 = 1369`, rounded to 2048.
  With Milan 7.4 50 ppm: `ceil(2e6 * 250 / 999950) = 501`, `501 + 768 = 1269`, still 2048.
  A cold reader who follows the cited clause finds the tu-hold rule. The stated assumption also rests on a false "no media-clock clause" premise.
  So the round's required item 2 (R303-1 F2) is still open, in the authoritative design page and in the RTL comment.
- Required outcome: the RTL comment, `TIME_SYNC.md` and the PR body cite a clause that states the bound used.
  Either IEEE 802.1AS Annex B.1.1 for the +/-100 ppm LocalClock bound, stated as an assumption for the media oscillator,
  or Milan v1.2 section 7.4's +/-50 ppm media-source bound with 100 ppm kept as a conservative margin.
  The "rather than an independent media-clock clause" claim is removed or corrected. The three locations agree.
- Verification: text inspection of the three locations against `receipts/clause_texts.txt`. The comment-stripped RTL stays
  identical to this head, checked the same way as `receipts/rtl-logic-unchanged.txt`. `TS_JUMP_NS_C` stays 2048.

## Suggestions (non-blocking; they do not affect coverage)

- S1 `Docs`, `scripts/measure_test_evidence.py:597-599`: the disposition for `tb/verilator/crf_rx/mutants.py` lists "tu, jump, refill and
  accept-edge defects". At this head the campaign also reads `KL_mmcm_drp_servo.sv` and runs `servo_ignores_valid` (`mutants.py:18,89-97`).
- S2 `Tests`, `tb/verilator/crf_rx/sim_talker_step.cpp:33-40`: the six events run in sequence from one lock. Under a mutant the first
  failing event leaves the servo in ACQUIRE with a displaced integrator, so later events fail too. For example `jump_removed` also
  fails the tu-marked `both_short_pos` event (`receipts/probes/jump_removed__talker.log`). The gate verdict is right; per-event
  attribution is not independent. Re-checking lock and baseline before each event, or per-event verdicts, would make it so.
- S3 `Tests`, `tb/verilator/crf_rx/mutants.py:19-28`: receiver mutants run only against `sim_discontinuity.cpp`. That the connected
  harness rejects detector removal is shown by reviewer probes, not by a gate. An optional `rx_no_detection` row against `talker_step`
  in the default campaign would keep round 2's property from regressing silently.

## Lens results (clean lenses in the finding format)

```text
[R302] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:213,274-290,384-397,514-521,586-605,611-620; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:76-80,254,558-578; hdl/milan/milan_datapath.sv:1725,5448-5449,5488,5532-5534,5547; receipts/rtl-logic-unchanged.txt - round-2 RTL edits are comments only: both files normalize (comments stripped, whitespace folded) to identical hashes at 39a0171c8 and d04a61678. Logic re-read at this head: one clock domain (both instances on axis_clk), 64-bit spacing, both bounds unsigned, pend/break ordering, accept-edge veto in rate_valid_o, every new register reset; the servo change is the single crf_rate_valid_i term in pp_run_r, guards untouched. Hosted verilator-lint, elaborate and yosys-portability succeeded at this head.
[R302] PASS Robustness - receipts/probes/SUMMARY.txt (48 rows, campaign PASS), receipts/probes/clean__jitter.log, clean__loop_*.log - round-1 campaign re-run unchanged at this head: jitter/drift false-positive probe 31/31; tu held, tu-only, step inside held tu, 20 us, listener-first, five overlapping GM changes and a 100-500 ms lag sweep all keep LOCKED with the integrator within 1 ppm; seq gap, silence, rebind, STOP, refill off by one either way, validity leak on break, uncancelled pending update, threshold halved or doubled, 32-bit spacing and removed lower bound are each killed. Receiver-discard telemetry is out of scope by the recorded #495 decision.
[R302] PASS Tests - tb/verilator/crf_rx/sim_talker_step.cpp:19-236, crf_talker_wrap.sv, mutants.py, Makefile:53-79; tb/verilator/mmcm_servo/Makefile:24-62, sim_main.cpp U13; receipts/crf_rx-make-all.log, receipts/probes/*__talker.log, receipts/harness/SUMMARY.txt, receipts/mmcm_servo-make.log - the shipped connected harness now fails for the defect: rx_no_detection 23 failures (talker-only reproduces -115.762 ppm and ACQUIRE), jump_removed 15 and lower_bound_removed 15 (unmarked event reaches +177.188 ppm, lock lost), servo_ignores_valid 5 (held-update check); clean passes 69/69. Validity is read after inputs settle and before the edge, which is what pp_run_r samples; quiet traffic shows 550 post-edge artifacts and zero sampled invalidity. Harness-integrity probes: post-edge sampling, a never-matching boundary predicate and a dropped invalid-boundary tally are each killed by the named check. `make` default now runs the 7-row mutation campaign (7/7), and the sweep verdict reader accepts both logs.
```

`Conformance` and `Docs` were applied in full and are unclean only through R302-2-F1. What else was checked under them:

- Conformance: AC1 met (tu edges, jumps and gaps restart the ring; failing arms gated). AC2 met: both-end events at 100 ms and 600 ms
  lag stay LOCKED on every clock, no receiver unlock, integrator within 0.020 ppm, one counted local step each. AC3: the focused
  suites pass here, the exact-head hosted contexts show 21 success and 1 skipped, and the manager's banks are public.
  IEEE 1722-2016 4.4.4.7, 10.4.5, 4.4.4.3 and 10.4.3 citations match the clause text.
  Scope held: servo guard logic unchanged; no CSR or counter added, per the decision.
- Docs: `GM_LOSS_RECOVERY.md:152,213`, `TESTING.md:462`, `REGISTER_MAP.md:838`, the servo banner and the harness comments describe the
  shipped behavior. The 100 ms cases are labelled guard-interaction evidence only, which matches their zero crossing boundaries.
  The PR body's round-2 figures match this round's receipts. No added line carries an em dash (`receipts/em_dash_grep.txt`).
  The local em-dash gate could not run: its pinned renderer is not installed here. The hosted `docs-check` passed at this head.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R302-2-F1) | Issue #546 AC1-3, both assignments and the #495 decision; `KL_crf_rx.sv:274-286`; `TIME_SYNC.md:167-229`; Milan v1.2 B.1.1 and 7.4; IEEE 802.1AS B.1.1; IEEE 1722-2016 4.4.4.3/4.4.4.7/10.4.3/10.4.5; talker_step and probe results; hosted runs | R302-2 | `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1` |
| RTL | CLEAN | `KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv` (banner, port, window close), `milan_datapath.sv` instances; comment-stripped equality versus `39a0171c8` | R302-2 | `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1` |
| Robustness | CLEAN | Round-1 campaign re-run unchanged: 15 receiver/servo mutants, jitter probe, 9 loop scenarios | R302-2 | `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1` |
| Tests | CLEAN (S2, S3 suggestions only) | `sim_talker_step.cpp`, `crf_talker_wrap.sv`, `mutants.py`, both Makefiles, servo U13; default crf_rx and mmcm_servo targets; talker-row mutants; 3 harness-integrity mutants; sweep verdict reader | R302-2 | `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1` |
| Docs | UNCLEAN (R302-2-F1) | `TIME_SYNC.md`, `GM_LOSS_RECOVERY.md`, `REGISTER_MAP.md`, `TESTING.md`, `MODULE_MATRIX.md`, README-tests, RTL banners/comments, `measure_test_evidence.py` disposition; PR body and both REVIEW READY comments | R302-2 | `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1` |

## Prior public findings on this PR

| Prior finding | Status at `d04a61678` | Evidence |
|---|---|---|
| R302-1-F1 MAJOR (Tests, Docs) = R303-1 F1 MAJOR (Tests): connected harness cannot fail for the defect | **Resolved.** | Verification clause met exactly: `rx_no_detection`, `jump_removed`, `lower_bound_removed` FAIL on `talker`; clean PASS; the quiet artifact no longer satisfies withholding (`receipts/probes/SUMMARY.txt`, `receipts/crf_rx-make-all.log`). Harness comments, `GM_LOSS_RECOVERY.md:213` and the PR body state what each scenario proves. |
| R302-1 S1 = R303-1 F2 MINOR (Conformance, Docs): 100 ppm term's authority | **Retained, open** as R302-2-F1. | The remote-quantization assumption is now explicit (resolves that half). The citation still names Milan Annex B.1.1, which states the tu rule. |
| R302-1 S2 = R303-1 F3 MINOR (Tests, Docs): mutation arm in no gate | **Resolved.** | `Makefile:53` `all: run mutants`; `servo_ignores_valid` committed in `mutants.py:89-97` with `mmcm_servo` `unit-build` hooks; `TESTING.md:462` updated; sweep runs `make -C` default (`run_all_suites.sh:390`). Residual wording is S1 here. |
| R302-1 S3 (Docs): servo banner omits the validity skip | **Resolved.** | `KL_mmcm_drp_servo.sv:76-80`. |
| R302-1 S4 = R303-1 S1 (Robustness): uncounted discards, frozen while LOCKED | **Out of scope by decision.** | The manager's round-2 assignment moved it to the #495 telemetry checklist. |
| R302-1 S5 = R303-1 S2 (Docs): semicolon capital; CRF_RATE meaning dropped | **Resolved.** | `GM_LOSS_RECOVERY.md:152`; `REGISTER_MAP.md:838`. |

## Executed evidence at this head (reviewer-run)

Tool: pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
All builds ran from a `git archive` of the exact head into disposable scratch trees. The clone was never edited.
Local paths in receipts are placeholders. Compiler command lines and build-only logs are not published.

| Run | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/crf_rx` (default `all`: unit, discontinuity, talker_step, mutants) | rc 0 in 8 min 28 s; 13 836/0, 1 658/0, 69/0; mutants 7/7 with named rejections; sweep verdict reader rc 0 | `receipts/crf_rx-make-all.log` |
| `make -C tb/verilator/mmcm_servo` (refactored `unit-build`) | rc 0; 82/0 unit incl. U13, 8/0 rails, 113/0 PHC step; verdict reader rc 0 | `receipts/mmcm_servo-make.log` |
| Round-1 campaign, unchanged probes (`probes/`, hashes equal round 1) via `scripts/run_probes_r2.py` | campaign PASS, 48 rows; 4 talker rows promoted from INFO to FAIL all FAIL | `receipts/run_probes_r2.stdout`, `receipts/probes/` |
| Harness-integrity mutants (`scripts/harness_probes.py`) | campaign PASS: clean PASS; 3 of 3 harness defects killed by the named check | `receipts/harness_probes.stdout`, `receipts/harness/` |
| Round-2 RTL logic identity | comment-stripped hashes equal at `39a0171c8` and `d04a61678` for both RTL files | `receipts/rtl-logic-unchanged.txt` |
| Clause texts | Milan v1.2 B.1.1 and 7.4; IEEE 802.1AS-2011/-2020 B.1.1 | `receipts/clause_texts.txt` |
| Em-dash scan of added lines | 0; local gate not runnable (renderer dependency absent) | `receipts/em_dash_grep.txt`, `receipts/em_dash.log` |
| Hosted check runs at the head (read only) | 21 completed success; `Physical gPTP (nightly and manual)` skipped (not executed) | `receipts/hosted_check_runs.tsv` |
| Clone integrity after all probes | HEAD/tree exact; worktree and index clean; index equals tree; no skip/assume flags; 4 gitlinks equal the head tree; 885 tracked files re-hash equal, modes equal | `receipts/clone_integrity.txt` |

Round-1 probe files `probes/run_probes.py`, `probe_loop.cpp`, `probe_jitter.cpp` have sha256 `e4aa82aa...`, `7d051697...`, `428d051e...`, equal to the
round-1 manifest. `scripts/run_probes_r2.py` only retargets the head guard, promotes the four talker expectations, and adds two recorded talker rows.

Informative row, unchanged from round 1: `clean loop:subthreshold`. An unmarked 2 000 ns talker step is below the 2 048 ns backstop by construction.
The integrator moved 30.723 to 28.770 ppm and the servo left LOCKED, with no receiver unlock. This is a limit, not a finding.
A compliant talker marks a GM change with tu (Milan Annex B.1.1), and the plane's smallest step is 20 us.

## Real limits

- Simulation only. Physical calibration was not run. No hardware, bench or field result backs this review. Skipped hosted contexts are not hardware proof.
- Timing: `rate_valid_o` still feeds `pp_run_r` combinationally through a 64-bit subtract and two compares at 100 MHz. No timing closure was run or seen for this head.
- The false-positive probe models bounded uniform timestamp jitter. No foreign talker's CRF timestamp statistics were measured.
- The full parent, processor, gPTP, Yosys and builder banks, the lint ratchet and the xvlog gate were not run by this reviewer. The manager's public source-bank evidence and the hosted results were read, not reproduced.
- The source validation here is against base `57456af96`. The final candidate against live `dev` (`573f0052`) is not validated by this review.

## Pending manager duties

- Publish this report and the manifest-listed files.
- Route R302-2-F1 to the executor. It is a text change in the RTL comment, `TIME_SYNC.md` and the PR body.
  Re-review `Conformance` and `Docs` at the new head. Any edit to `KL_crf_rx.sv` also un-covers `RTL` there; a comment-only
  identity check like `receipts/rtl-logic-unchanged.txt` is enough to re-cover it.
  `Robustness` and `Tests` stay banked at `d04a61678` only while nothing in their scope changes.
- Build and validate the final candidate against live `dev` at the merge turn; own act and hosted acceptance for the new head.
- Keep the physical-calibration and timing limits visible in any completion ledger.

R302-2 FINISHED
