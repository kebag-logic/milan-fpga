[R303] NEGATIVE - exact head d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1

Round R303-2 is the external review of PR #554 (issue #546), done in a cleared context. Head `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1`, tree `6ec524af62e911061e712e43313c27b0c9280561`, source base `57456af96b3127b9d309a995bbbd35a6113ce52d`. All five lenses were applied at this head.

## Summary

Round 2 fixes the test defect that made round 1 negative:

- The connected GM-change harness now fails when the receiver's talker-step isolation is removed. With no detection, the talker-only +150 us case reproduces the issue's excursion: -115.762 ppm, and the servo drops to ACQUIRE.
- It also fails when the jump backstop or its lower bound is removed (+177.188 ppm, ACQUIRE), when the servo ignores validity, and when validity is forced high.
- The talker-only and 600 ms-lag cases require a servo boundary inside the crossing history, and each reaches one.
- Validity is captured before the sampling edge, which is the value the servo registers at that edge.
- The one-clock post-edge artifact still exists at the RTL port, but it can no longer satisfy the withhold check. The clean quiet control counts 550 artifacts and zero sampled invalidity. Reverting the harness to post-edge observation makes the quiet control fail.
- The receiver and servo-validity mutation arms now run in the default `crf_rx` gate. A surviving mutant fails both that gate and the sweep's verdict reader.

The round-2 RTL delta is comments only: the comment-stripped token streams are byte-identical to round 1.

One item stays open. The corrected derivation of the 2048 ns jump threshold still cites a clause that does not say what it is cited for. Milan v1.2 Annex B.1.1 is the rule that `tu` is held for 0.25 s. The +/-100 ppm LocalClock bound is IEEE 802.1AS Annex B.1.1. The RTL comment also says no separate media-clock clause exists, but Milan v1.2 Section 7.4 is one (+/-50 ppm), and the repository's own compliance matrix lists it. The threshold value is unaffected: it is 2048 ns under either bound. This is the round-1 F2 not yet resolved, kept as MINOR, so the verdict is NEGATIVE.

## Findings

### R303-2-F1 - MINOR - Conformance, Docs - the jump threshold's media-clock term still cites an authority that does not state it

- Artifacts:
  - `hdl/ieee1722/crf/KL_crf_rx.sv:275-276`: "The media oscillator inherits the +/-100 ppm LocalClock bound (Milan Annex B.1.1), rather than an independent media-clock clause."
  - `docs/design/TIME_SYNC.md:191-195`: "The media oscillator inherits the +/-100 ppm LocalClock bound. See Milan v1.2 Annex B.1.1. This assumes that LocalClock also bounds the media oscillator."
  - The PR body's Description repeats the same citation.
- Authority/evidence (`receipts/authority_excerpts.txt`):
  - Milan v1.2 Annex B.1.1 is headed "tu (timestamp uncertain) field". It says only: "In case of a change of grandmaster, the tu bit shall be set to 1 for the duration of 0.25 seconds." The repository cites it for exactly that rule elsewhere, for example `docs/reference/REGISTER_MAP.md:750`.
  - The only frequency tolerance anywhere in Milan v1.2 is Section 7.4, "Media Clock Source Quality": "oscillators used as source in a media clock domain shall produce a clock whose frequency tolerance is better than +/-50PPM."
  - The repository records that clause itself: `docs/reference/MILAN_COMPLIANCE_MATRIX.md:182`, under "1.8 Streaming (Section 6) and media clocking (Section 7)", reads "7.4 | media clock source quality ± 50 ppm".
  - The +/-100 ppm LocalClock bound is IEEE 802.1AS Annex B.1.1, "Frequency accuracy", in both the 2011 and 2020 editions. The matrix row at `MILAN_COMPLIANCE_MATRIX.md:228` sits under "4. IEEE 802.1AS-2011".
  - So the new text names the wrong document for the 100 ppm term. It also says there is no separate media-clock clause when Milan has one.
  - The quantisation half of round-1 F2 is resolved: the text now states that the remote talker is assumed to share this design's PHC envelope.
- Impact: this is not a functional defect. `receipts/threshold_sensitivity.txt` shows the drift and threshold under each bound:

  | Media bound | Drift | Plus 768 ns quantisation | Threshold |
  |---|---|---|---|
  | 100 ppm | 601 ns | 1369 ns | 2048 ns |
  | 50 ppm (Section 7.4) | 501 ns | 1269 ns | 2048 ns |

  The defect is traceability, in the one input that round 1 and assignment item 2 asked to correct. A cold reader who follows "Milan v1.2 Annex B.1.1" finds the `tu` hold rule. That reader also finds the authoritative design page and the RTL contradicting the repository's own compliance matrix about whether Milan bounds the media oscillator.
  - Not attributed to `RTL`: the constant `TS_JUMP_NS_C` is correct under either authority.
- Required outcome:
  - The derivation cites a source that states the bound it uses. That means Milan v1.2 Section 7.4 (+/-50 ppm) for the talker's media clock source, or IEEE 802.1AS Annex B.1.1 for the LocalClock, or both.
  - It no longer says that no media-clock clause exists.
  - If the 100 ppm figure is kept, it is stated as a conservative choice against Section 7.4's 50 ppm.
  - `KL_crf_rx.sv`, `TIME_SYNC.md` and the PR body agree.
- Verification: check the text at the named locations against the clauses. The threshold stays 2048 ns, and the RTL token stream stays unchanged if only comments move.

### S1 - SUGGESTION - Tests - U13's resume check cannot fail for a servo that never resumes PI

- `tb/verilator/mmcm_servo/sim_main.cpp:596`: "[U13] clean remote sample resumes locked" checks only `state() == 4`. That state held throughout the invalid run, so a servo that never ran PI again after an invalid sample would pass it.
- The current RTL has no such latch, because `pp_run_r` takes `crf_rate_valid_i` combinationally (`KL_mmcm_drp_servo.sv:572-573`). That is why this is optional.
- Optional: after validity returns, present a valid offset rate and require that the trim responds.

### S2 - SUGGESTION - Docs - evidence-gate disposition for the campaign is stale

- `scripts/measure_test_evidence.py:597-599` records that `mutants.py` "copies the receiver" and names "tu, jump, refill and accept-edge defects".
- Since round 2 the campaign also reads `KL_mmcm_drp_servo.sv` and runs the servo-validity mutant (`tb/verilator/crf_rx/mutants.py:18,89-97`).
- Optional: name the servo read in the recorded reason.

## Lens results

- `[R303] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:213,389-397,445,516-520,589-601; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:254,561-575; hdl/milan/milan_datapath.sv:1725,5488,5547; receipts/rtl_round2_comment_only.txt` - checked against issue #546 acceptance 1 and the servo sampling contract:
  - The round-2 RTL delta (`39a0171c8..d04a61678`) is comments only: the preprocessed, comment-stripped token streams of both modules are byte-identical.
  - The logic reviewed in R303-1 at `39a0171c8` was re-exercised at this head. D1-D10 are all killed again (`receipts/r1_campaign_rerun.txt`):
    - sequence gap;
    - STOP gate;
    - silence and bind invalidation;
    - 32-bit spacing alias;
    - pending-rate cancel;
    - the 4096 and 1024 thresholds;
    - validity kept on break;
    - `tu` rising edge only.
  - Upper-bound removal is also killed by the discontinuity harness (N5, 24 failures).
  - The servo registers `pp_rate_r <= crf_rate_i` and `pp_run_r <= ... && crf_rate_valid_i` on the same boundary edge, so rate and validity are sampled together. The receiver and servo share one clock, so no CDC is involved.
- `[R303] PASS Robustness - probes/probe_talker.cpp at this head (receipts/r1_campaign_rerun.txt, clean_probe); tb/verilator/crf_rx/sim_talker_step.cpp:32-40; receipts/r2_cases/H2_neg_case_without_step.log` - checked against the #546 false-positive and recovery claims:
  - A 300 ms `tu` pulse with no step gives one invalidation episode and stays LOCKED.
  - +/-500 ns timestamp jitter over 4 s gives 0 invalid clocks.
  - +/-1200 ns jitter, outside the derived envelope, holds validity low while the servo stays LOCKED and the integrator frozen. This is the documented choice; discard telemetry was moved to #495 by manager decision.
  - Clean recovery follows.
  - Six events run back to back in one session: +/-150 us talker-only, 100 ms lag and 600 ms lag. All stay LOCKED, with no receiver unlock counted and the recovered rate exactly -40 x 256.
  - Unmarked positive steps are covered by the discontinuity harness (N5).
  - The 0.020 ppm integrator movement in the talker-only negative case also appears with no step at all (H2), so it is ordinary loop quantisation, not leakage.
- `[R303] PASS Tests - tb/verilator/crf_rx/sim_talker_step.cpp:74-142,161-229; tb/verilator/crf_rx/Makefile:53-79; tb/verilator/crf_rx/mutants.py:19-100; tb/verilator/mmcm_servo/Makefile:27-61; tb/verilator/mmcm_servo/sim_main.cpp:584-597` - checked against AGENTS.md section 6 ("each new test can fail for the defect it claims to detect") and the round-2 assignment:
  - Clean: 69/69 checks pass.
  - Connected mutants and their failure counts:

    | Mutant | Failures | Integrator and servo state |
    |---|---|---|
    | receiver detection removed (N1) | 23 | -115.762 ppm, ACQUIRE |
    | jump removed (N2, C2) | 15 | +177.188 ppm, ACQUIRE |
    | lower bound removed (N3) | 15 | +177.188 ppm, ACQUIRE |
    | both detectors removed (C3) | 22 | - |
    | servo ignores validity (C4) | 5 | - |
    | validity forced high (C5) | 11 | - |

  - The talker-only and 600 ms cases each print "crossing boundaries 1, invalid boundaries 1".
  - Post-edge observation (H1) fails the quiet control.
  - The scenario with no step (H2) fails the boundary and withhold checks, so those checks are not vacuous.
  - The default target runs the 7-control campaign (`receipts/crf_rx_default.log`). A deliberately surviving mutant (M1) makes the campaign exit non-zero and the sweep's `suite_tally.py --verdict` exit 1.
  - The U13 servo arm passes clean (82/0), and its committed mutant is killed with the named check.
  - S1 is a suggestion only.
- Conformance: UNCLEAN, R303-2-F1. What was checked:
  - Acceptance 1 is met: the discontinuity harness has failing arms (author 4 of 4 plus servo, reviewer D1-D10 and N5).
  - Acceptance 2 is met, and the connected evidence now discriminates. Steps at both ends (100 ms and 600 ms lag) keep the servo LOCKED, and each counts exactly one local PHC step. With no isolation the servo loses lock.
  - Acceptance 3: the manager's gate receipts are rc 0, and at the exact head 21 hosted contexts succeeded. "Physical gPTP" was skipped, not executed.
  - The `tu` handling (either edge restarts; a held level permits recovery) is consistent with IEEE 1722-2016 4.4.4.7 and 10.4.5 as cited.
- Docs: UNCLEAN, R303-2-F1. What was checked:
  - `TIME_SYNC.md:144-229`.
  - `GM_LOSS_RECOVERY.md:152,154,213`: the talker_step row matches what the harness asserts.
  - `REGISTER_MAP.md:838`: the CRF_RATE meaning is restored.
  - `TESTING.md:462`: the default gate includes the mutants.
  - The servo banner at `KL_mmcm_drp_servo.sv:79-82`.
  - The MODULE_MATRIX and README-tests rows.
  - The PR body.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R303-2-F1) | issue #546 body and assignment comments; `KL_crf_rx.sv:274-397`; `TIME_SYNC.md:144-229`; `MILAN_COMPLIANCE_MATRIX.md:182,228`; `REGISTER_MAP.md:750`; Milan v1.2 Annex B.1.1 and Section 7.4; IEEE 802.1AS-2011/2020 Annex B.1.1; N1-N3, C2-C5 results; hosted check runs | R303-2 | d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1 |
| RTL | CLEAN | `KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv:240-700`, `milan_datapath.sv:1725,5488,5547`; comment-only token-stream proof; D1-D10, N5; servo unit 82/0 | R303-2 | d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1 |
| Robustness | CLEAN (discard telemetry moved to #495 by manager decision) | `probe_talker.cpp` phases B, C, D, E at head; `sim_talker_step.cpp` six-event sequence; `sim_discontinuity.cpp` via D1-D10, N5; H2 | R303-2 | d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1 |
| Tests | CLEAN (S1 suggestion only) | `sim_talker_step.cpp`, `crf_talker_wrap.sv`, `crf_rx/Makefile`, `mutants.py`, `mmcm_servo/Makefile`, `mmcm_servo/sim_main.cpp` U13; default gate; the unchanged round-1 campaign (23 cases); addendum N0-N5, H1, H2, M0, M1; artifact probe | R303-2 | d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1 |
| Docs | UNCLEAN (R303-2-F1) | `TIME_SYNC.md`, `GM_LOSS_RECOVERY.md`, `REGISTER_MAP.md`, `TESTING.md`, `MODULE_MATRIX.md`, README-tests diffs; RTL banners and comments; `measure_test_evidence.py:597-599`; PR body; issue REVIEW READY comments; commit messages (three, one line each, no trailers) | R303-2 | d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1 |

## Executed evidence at this head

All runs used exported copies of the exact head under the private scratch area; the review clone was never built in. Simulator: Verilator 5.050 rev v5.050 through the pinned wrapper, whose sha256 is `905795b9...79e92f`. Exact commands are in `receipts/COMMANDS.txt`.

- **Default `make -C tb/verilator/crf_rx`: rc 0, 511 s.** `suite_tally.py --verdict` rc 0.
  - Unit: 13,836 checks. Discontinuity: 1,658. Talker_step: 69. All pass.
  - The campaign reports 7 checks and 0 failures, including `servo_ignores_valid`, which is rejected by "[U13] invalid remote sample holds trim".
  - Receipts `receipts/crf_rx_default.log` and `.rc`. Local tool paths in that log are replaced by placeholders.
- **Round-1 reviewer campaign re-run unchanged: rc 0, all 23 cases meet expectations.** `probes/mutant_probe.py` is byte-identical to its R303-1 manifest entry, and so are the three probe sources. Receipts: `receipts/r1_campaign_rerun.txt`, `receipts/r1_cases/`.
  - C2, C3 and C4 survived in round 1 and are now killed on the committed harness.
  - C5 is killed.
  - The listener-first probe (O0-O4) behaves as in round 1.
  - D1-D10 are killed.
- **Round-2 addendum, `probes/run_probes_r2.py`.** The manager's named cases (`rx_no_detection`, `jump_removed`, `lower_bound_removed`, clean, quiet artifact) are N1, N2, N3, N0 and H1 here. Receipts: `receipts/r2_probe_batch1..5.txt`, `receipts/r2_cases/`, `receipts/r2_campaign_sweep_reader.txt`.

  | Case | Target | Result |
  |---|---|---|
  | N0 clean | talker_step | PASS 69/0; quiet: 550 post-edge artifacts, 0 sampled invalid |
  | N1 receiver detection removed | talker_step | KILLED, 23 failures; talker_only_pos -115.762 ppm, ACQUIRE; no invalid boundary anywhere |
  | N2 jump removed | talker_step | KILLED, 15; talker_only_neg +177.188 ppm, ACQUIRE |
  | N3 lower bound removed | talker_step | KILLED, 15; same trajectory as N2 |
  | N4 upper bound removed | talker_step | passes, expected: positive steps are marked with `tu` |
  | N5 upper bound removed | discontinuity | KILLED, 24 |
  | H1 harness reads validity after the edge | talker_step | KILLED by both quiet checks |
  | H2 talker-only negative case with 0 ns step | talker_step | fails the boundary and withhold checks; integrator 30.703..30.723 ppm, as with the step |
  | M0 committed campaign | mutants | PASS 7/0 |
  | M1 committed campaign with `jump_removed` made a no-op | mutants | campaign exits non-zero (make rc 2), "checks: 7 failures: 1"; `suite_tally.py --verdict` rc 1 |

- **`probes/probe_artifact.cpp` (round-1 source):** after the accepting edge, 300 of 300 clean PDUs read low on the port and 0 of 300 on the register. The artifact remains at the RTL level; N0 and H1 show that the harness no longer counts it as withholding. Receipt `receipts/probe_artifact.log`.
- **Servo unit harness:** 82 checks, 0 failures, U13 included. Receipt `receipts/mmcm_servo_unit.log`.
- **Hosted check runs at the exact head (read-only):** 21 completed successfully: rtl-fast, verilator-suites and its five shards, yosys-portability and its four shards, docs-check, docs-check-no-git, elaborate, wire-accountability, full-ci-gate and the rest. "Physical gPTP (nightly and manual)" was skipped, not executed. Receipt `receipts/hosted_check_runs.tsv`.
- **Clone integrity after all runs** (`receipts/clone_integrity.txt`):
  - HEAD, tree and index write-tree agree, and the status is empty, ignored files included.
  - All 885 tracked blobs match by content and mode.
  - The four gitlink index records equal the HEAD tree's.
  - `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` are checked out at their gitlinks.
  - `external` has been uninitialised since round start (an empty directory with no `.git`; `git submodule status` shows `-`). The checker's one "MISMATCH" line is that uninitialised path resolving to the superproject, not a change.

## Prior public findings on this PR

I read these only after my own pass over the diff. Disposition at this head:

| Prior item | Status at `d04a61678` | Evidence |
|---|---|---|
| R302-1-F1 = R303-1 F1, MAJOR (Tests; R302 also Docs): the connected harness cannot fail for the defect | **Resolved** | N1, N2, N3, C2-C5 killed; a crossing boundary is required and reached; pre-edge observation; H1; quiet control; GM_LOSS_RECOVERY and PR evidence describe what each scenario proves |
| R303-1 F2 = R302-1 S1 (Conformance, Docs): the 100 ppm term's citation | **Retained as R303-2-F1, MINOR.** The quantisation assumption is now explicit (resolved part). The media term still cites Milan Annex B.1.1, and now also claims that no media-clock clause exists | see R303-2-F1 |
| R303-1 F3 = R302-1 S2 (Tests, Docs): mutation arm in no gate; servo mutant not committed | **Resolved** | `Makefile:53` `all: run mutants`; default log shows 7 controls; M1 fail-closed; `mutants.py:89-97` with the `mmcm_servo` `unit-build` target; `TESTING.md:462` |
| R302-1 S3: servo banner omits the validity skip | **Resolved** | `KL_mmcm_drp_servo.sv:79-82` |
| R302-1 S4 = R303-1 S1: receiver discards are uncounted, and the hold is unbounded under LOCKED | **Out of scope by manager decision** (#495 telemetry item). These were suggestions, so they do not affect coverage | probe phase D reproduces the behaviour at this head |
| R302-1 S5 = R303-1 S2: wording | **Resolved** | `GM_LOSS_RECOVERY.md:152` ("; the receiver"); `REGISTER_MAP.md:838` restores what CRF_RATE measures |

## Limits

- Physical calibration and hardware: not run. Nothing here is hardware evidence, and the skipped physical gPTP context is not a pass.
- Timing closure and area: not evaluated at this head. The RTL logic is token-identical to `39a0171c8`, where R303-1 measured the receiver area.
- Not run by me:
  - the `mmcm_servo` rails and PHC-step legs;
  - `mmcm_servo_autorepair`;
  - `milan_dp`;
  - the full parent, processor, gPTP, Yosys and builder banks;
  - any documentation or idiom gate.

  Those are covered only by the manager's and author's public receipts, which I read but did not reproduce.
- The assignment refers to a round-1 runner `probes/run_probes.py`. My round-1 runner is `probes/mutant_probe.py`, and I re-ran it unchanged. The named cases are supplied by the new `probes/run_probes_r2.py`.
- My first batch-5 run misgraded M1 as "survived". The grader matched the embedded discontinuity tally ("failures: 0") instead of the campaign's own tally line, although the campaign itself had exited non-zero. I fixed the grader to read only the campaign's tally and re-ran batch 5; only that re-run is published. Batches 1-4 use the talker and discontinuity grading branch, which the fix did not touch.
- In the scratch copies only, build parallelism was capped by rewriting `--build -j 0` to `-j 4`. The default gate as committed uses `-j 0`, which uses every host core.
- Authority text comes from layout-preserving PDF text extraction of the local copies of Milan v1.2 (Final Approved, 2023-11-30) and IEEE 802.1AS-2011 and -2020.
- I have no data on real third-party CRF talker timestamp noise. The threshold was checked only against synthetic jitter.

## Pending manager duties

- Route R303-2-F1 to the executor. The fix is comment and documentation text only, and the threshold value does not change.
- Re-review the new head. The fix touches `KL_crf_rx.sv` and `TIME_SYNC.md`, so it un-covers Conformance and Docs, and also RTL by file scope. A comment-stripped token-stream identity check can re-bank RTL cheaply. Tests and Robustness stay banked at `d04a61678` only while their scope is untouched.
- Build and validate the final current-dev candidate at the merge turn (source base `57456af96b3127b9d309a995bbbd35a6113ce52d`, live dev `573f0052a0e4412e81f0845438fcec2086ce5d55`).
- Hosted and `act` acceptance.
- Publish this report and the manifest-listed receipts.
- The #495 telemetry item, per the manager's decision.

R303-2 FINISHED
