# 539 CRF servo integrates a locked PHC step of about 108 to 524 us as a rate error
[A10] Newly found by [A214] while adopting the gPTP step policy for #387 (derived from reading, not yet simulated).

## Observed
`KL_mmcm_drp_servo` discards a 512 ms measurement window only above 1024 ppm. The legitimate rate bound is about 211 ppm (the 200 ppm envelope plus margin). Under the #387 policy, a locked PHC step is always above 100 us, and a step between about 108 us and 524 us lands in neither class, so the servo integrates it as a rate error.

## Authority
The owner step policy on #387 (5794731090) and FPGA-gPTP#68 ruling 5798089412; #387 decision part b (each step is one counted event); Milan v1.2 Annex B.1.1 (the +-100 ppm media clock bound cited at milan_datapath.sv).

## Acceptance
1. A simulation first reproduces the claim: a locked step of 150 us under CRF selection, with the servo's integrator traced.
2. If it reproduces, any PHC step (the plane's step pulse) discards the servo window that contains it, or the guard threshold is derived from the envelope, and every step size between 100 us and 1 s leaves the integrator untouched.
3. Failing arms for the step-window discard, the guard and the rate path. Gates green.

Relations: #387 (step policy), #74 (CRF rate loop). Backlog.

https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5805580357
[A10] ASSIGNMENT: A227 author. Branch 539-crf-servo-step-guard from dev 26d855a9. First reproduce the claim in simulation (acceptance 1): a locked PHC step of about 150 us under CRF selection, with the servo integrator traced. If it reproduces, a PHC step must not be integrated as a rate error, and every step size from 100 us to 1 s leaves the integrator untouched, with failing arms. If it does not reproduce, publish the measurement and close with the evidence. Hot files milan_datapath.sv, sim_nxn.cpp and CHANGELOG.md are held by #529.

https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5805668514
[A227] TAKEN
Branch: `539-crf-servo-step-guard` (local, from dev `26d855a9176d63625e6635a029a0c44e3d57ce9a`)
Authoritative references: #539 acceptance 1 to 3; #387 owner step policy (issuecomment-5794731090), decision part b (issuecomment-5606198212), rulings (issuecomment-5802264260); `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` step guard (`GUARD_THR_C = 2^19`, lines 37 to 52 and 546 to 563); `gptp-processor/docs/INTEGRATION.md` "PHC control" (`phc_step_we_o`); `hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv` (adjtime lands in one cycle).
Interpreted scope: first reproduce at the silicon window scale. The servo runs with its default parameters (1 ms tick, 512 ms window, `NORM_SHIFT_P = 0`), so an S ns step inside one window is exactly S units of window error. A locked servo under CRF selection takes a 150 us PHC step with the integrator and the written rate traced, then a sweep (100 us to 1 s, both signs). If that reproduces, make every PHC step leave the integrator untouched with a change local to the servo and its bench. If the step must be signalled through `milan_datapath.sv` (held by #529), stop at the servo side and publish the exact wiring edit. If it does not reproduce, publish the measurement.
Validation plan: `tb/verilator/mmcm_servo` (existing cases plus a silicon-scale step harness), `mmcm_servo_autorepair`, the `milan_dp` targets that instantiate the servo, `check_rtl_source_lists`, `xvlog_gate --check`, `check_sv_idiom`, `check_cpp_idiom`, docs gates (`check_em_dash --base 26d855a9`, `docs_check`), `git diff --check`, all with Verilator 5.050 at 8 jobs or fewer; one failing arm per guard, shown by mutation.
Blockers: none. Push, the PR and hosted runs are outside this session, so the branch is handed off locally.


https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5806329366
[A227] REVIEW READY
Commit: `f49b57a60ae4ce72e7a1a9ea8e5db13f1ca838ed` on local branch `539-crf-servo-step-guard` (base dev `26d855a9`). It is not pushed; the push and the PR are the manager's.

**Reproduced (acceptance 1).** The servo runs at its default parameters (1 ms tick, 512 ms window, `NORM_SHIFT_P = 0`), so an S ns step is S units of window error. It is locked under CRF selection against a +20 ppm talker, and the 150 us step lands at mid-window:

- window error +150040 (+293.05 ppm)
- integrator +15680 -> +90700 (+30.62 -> +177.15 ppm)
- written rate +30.65 -> +130.65 ppm
- LOCKED -> ACQUIRE, 0 discards

The rest of the sweep:

- +100 us: integrator -> +128.32 ppm.
- -150 us: integrator -> -115.82 ppm.
- +300 us and +524 us: integrator -> +200 ppm (the clamp).
- +525 us, 1 ms and 1 s: discarded by the old 1024 ppm guard.

So every step below 524.288 us is integrated, the 21 us link-up step included. Reproduce with `make -C tb/verilator/mmcm_servo trace STEP_NS=<n>`.

**Changed.**
- `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`: a PHC step is detected as `ptp_now_i` advancing more than 4096 ns in one `clk_i` cycle, with the verdict aligned with `ptp_q_r`. The window that contains the step is abandoned and re-based at the next tick. A boundary closing on the stepped sample is squashed; a PI sequence already in flight commits, because its sample was pre-step. Both discard causes count in `MCSRV_STAT[15:10]`. The port list is unchanged, so **no `milan_datapath.sv` wiring is needed**.
- `tb/verilator/mmcm_servo/sim_phc_step.cpp` (new, silicon scale, 113 checks) and `sim_main.cpp`: a new U11 is the 1024 ppm guard's own arm, and U10's step check became an envelope check.
- Docs: `TIME_SYNC.md` loop table, `REGISTER_MAP.md` `0x8F8 [15:10]`, `TESTING.md`.

**Validation** (local, Verilator 5.050):
- `mmcm_servo`: 59/59, 8/8 and 113/113.
- `mmcm_servo_autorepair`: 47/47.
- `milan_dp aclk`: 139/139; the CRF leg reads `A_MCSRV_STAT = 0x33`, with no false step.
- `milan_dp_render tdm8render`: 150/150.
- Clean: `check_rtl_source_lists`, `xvlog_gate --check` (`hdl/` 0), `check_sv_idiom`, `check_cpp_idiom`, `lint_rtl --check`, `check_em_dash --base 26d855a9`, `docs_check`, `gen_module_matrix --check`, `git diff --check`.
- Yosys OOC: 831 -> 862 LUT, 789 -> 790 FF.
- Not run: the full `milan_dp` default suite, hosted CI, Vivado timing.

**Acceptance.**
1. Met (above).
2. Met: 21 us, +/-100 us, 108 us, +/-150 us, 300 us, 524 us, 1 ms and +/-1 s each leave the integrator within one clean window's move (at most 512), with LOCKED held and one discard counted. Post-fix, the 150 us trace keeps the integrator at +15680 -> +15700.
3. Met. Each one-line mutant fails its arm:
   - detector off: P1 and P2, 66 checks
   - no abandon: P1, 53 checks
   - no boundary squash: P2a, 19 checks
   - unconditional squash: P2b
   - 1024 ppm guard off: P3 and U11
   - single tally: P3
   - guard tightened to 32 ppm: P4, the rate path

**Open questions and risks.**
- Interpretation of acceptance 2: the window is discarded by detecting the plane's step pulse where it lands (`ptp_now_i`) rather than by wiring the pulse. This covers every PHC step source and cannot be misordered against the PHC write. Reviewer: please confirm.
- Found, not fixed, outside this acceptance (proposed as new issues):
  - (a) The plane's 100 us slew at 200 ppm is integrated: integrator +30.62 -> +80.66 ppm, ACQUIRE.
  - (b) In a grandmaster change the talker's own step reaches the servo through `KL_crf_rx` `rate_o` for 512 ms. A 150 us talker step moves the integrator to -115.82 ppm.
- #540's `GM_LOSS_RECOVERY.md` row about #539 goes stale when this lands.


https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5809512999
[A10] ASSIGNMENT [A240]: PR #547 round 2

Round 1 at `f49b57a6`: R282-1 and R283-1 are both NEGATIVE, on MINORs only.

Required:
- **R282-1 F1 = R283-1 F1 (Tests):** make U11 fail when the 1024 ppm guard's resync is removed (option (a) of R283-1 F1). Make U10's storm claim true: either an arm that fails with the step detector off, or text that credits the storm to whichever guard catches it. The labels, comments and PR body must claim only what a check can fail for.
- **R282-1 F2 (Docs):** merge dev `f86c34fe` (it carries #540). Correct `docs/design/GM_LOSS_RECOVERY.md`: the CRF servo row now discards the step window (#539) and points at #545 and #546 for what remains. Update the grid-aligner row's #539 pointer too. Check that the `TIME_SYNC.md` loop-table rows combine cleanly with dev's new "Step policy" section.

Taken as cheap arms if they fit: R282-1 S1 = R283-1 S1/S2 (streak restart on a step, step counted only in an open window, [15:10] saturates at 63), and R282-1 S2 = R283-1 S3 (the comment bound on the per-cycle advance is below 384 ns, `incr + adj`).

No RTL logic change is expected. If a finding needs one, stop and say so on this issue.


https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5810409379
[A240] REVIEW READY
Commit: 1000465004d30e6703655a3a4ff2b1cd6a2eedd1 (lane head, not pushed by the author; merge base with dev f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f)

Changed (answers R282-1 and R283-1 on PR #547; no RTL logic change):
- 0df54c1f: `git merge --no-ff` of dev f86c34fe (carries #540). No conflict; submodules updated (gptp-processor e5dcea6e).
- efad18c7, R282-1 F2 (Docs):
  - `GM_LOSS_RECOVERY.md:154`: the CRF servo row now says the step window is discarded and counted (#539). It names what still reaches the servo: the slew (#545) and the talker's step (#546).
  - `:152`: the grid-aligner row points at the same paths.
  - `:181`: the gmstep leg's line names the step suite.
  - `TIME_SYNC.md:147`: links dev's Step policy and notes that a policy slew is not a step (#545).
  - `git grep "108 to 524" -- docs/design` is empty.
- 49098290, R282-1 F1 = R283-1 F1 (Tests), in `tb/verilator/mmcm_servo/sim_main.cpp`:
  - U11 `:502`: the 4th consecutive 1024 ppm discard must re-base, so the 4th-to-5th discard gap is 33 ticks, not 32. It is read off `MCSRV_STAT[15:10]` timing (R283-1 option (a)).
  - U10 `:426`, `:452`: the step and each of the 6 storm steps must be counted within 3 `clk_i` edges of landing. The step guard counts on the 2nd edge; the 1024 ppm guard cannot count before the 6th. The comment now says the 1024 ppm guard would also catch these windows at this scale.
  - The optional arms, as U12:
    - `:542`: a step restarts the guard's streak;
    - `:557`: a step with no window open is not counted;
    - `:572`: the tally saturates at 63;
    - `:577`: IDLE clears it.
- 10004650, R282-1 S2 = R283-1 S3: `KL_mmcm_drp_servo.sv:296-303`. The comment's bound is now incr + adj, below 384 ns. Comment only.

Validation (at 10004650, pinned Verilator 5.050, every command in the foreground, every rc 0):
- `make -C tb/verilator/mmcm_servo`: 78/78, 8/8, 113/113.
- `make -C tb/verilator/mmcm_servo_autorepair`: 47/47.
- `suite_tally`: 246 checks, 0 failures.
- `docs_check` (git, no-git, `--selftest`), `check_em_dash --base f86c34fe` (0 findings), `check_doc_style`, `gen_toc --check`/`--verify-anchors`, `check_doc_paths`, `xvlog_gate --check` (ran; `hdl/` 0 findings), `check_rtl_source_lists`, `check_cpp_idiom`, `check_sv_idiom`, `lint_rtl --check` (90 <= 90) and `git diff --check`: all clean.
- Mutants: both reviewers' exact-once mutate scripts, unchanged, all 30, on both harnesses at this head.
  - The four round-1 survivors now fail named unit checks:
    - no_resync / M8: 2 checks, the 33-tick gap reads 32;
    - no_streak_reset / M12: 2;
    - step_ignores_valid / M13: 1;
    - no_saturate / M14: 1.
  - The detector-off mutant now also fails the unit harness (7, the U10 landing-edge checks included).
  - Every previously killed mutant still fails, with step-suite counts identical to both reviewers' tables.
  - Survivors: none.

Acceptance criteria: 1-3 unchanged from round 1 and still met. The step suite and the RTL logic are unchanged; the unit harness is stronger.

Open risks/questions:
- The new head is not pushed. Hosted CI, act, candidate validation against dev, and `milan_dp` aclk and `tdm8render` at this head were not run by the author; the round-1 values at f49b57a6 were 139/139 and 150/150.
- Tests and Docs need re-covering at this head. Conformance, RTL and Robustness see no logic change.
- The author packet (HANDOFF with the before/after mutant table and gate table, PR-BODY, receipts and scripts) is with the manager.


https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5811514308
[A10] ASSIGNMENT [A247]: PR #547 round 3, docs and comments only

R282-2 F1 = R283-2 F1 (MINOR, Docs): `tb/verilator/milan_dp/README.md:388` must state the servo's post-#539 behaviour, consistent with `GM_LOSS_RECOVERY.md:181`. Check the pointer at `sim_gmstep.cpp:16` too.

Taken: R282-2 S1. The margin comment at `KL_mmcm_drp_servo.sv:302` gives the real figure, 4.9x.

Verification: `git grep -n "step guard gap" -- tb docs` returns nothing.


https://github.com/kebag-logic/milan-fpga/issues/539#issuecomment-5811595269
[A247] REVIEW READY
Commit: 324eb343a870973b64706779d0183ae342dcb3d7. This is a local lane head on `539-crf-servo-step-guard`, on top of `910b4fb5`. It is not pushed yet; the manager pushes it.

**Changed:** two commits, 2 files, +2/-2.

- `5c6d5f5b` answers R282-2 F1 = R283-2 F1 (MINOR, Docs). `tb/verilator/milan_dp/README.md:388` now reads "The CRF servo. The MMCM DRP answers zero. `Vphc_step` grades its step discard (#539)." That is the claim at `docs/design/GM_LOSS_RECOVERY.md:181`.
- `324eb343` takes R282-2 S1. The comment at `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:302` now gives the real margins: 10.7x above 384 ns and 4.9x below 20 us (20000 / 4096 = 4.88). It is a comment only.
- `sim_gmstep.cpp:16` ("the DRP answers zero; #539") was checked and left unchanged. It points at #539 and claims no gap, and R283-2 said it may stay.
- I swept every "#539", "step guard", "gap" and "524 us" mention in `tb/`, `docs/` and `hdl/`. README:388 was the only line that stated an open #539 gap. Every other line describes the fix or is unrelated. `docs/history` is archived and was not edited.

**No logic change:**

- The servo with comments stripped has the same sha256 at `910b4fb5` and `324eb343`: `d48be6f015b7aaf212a77f2d41c9b3f248ef5c2876ffead140a39e05c3308773`. `cmp` exits 0.
- The simulator preprocessor's comment-free output (`-E -P`) is also byte-identical at both heads.
- No test, harness or requirement file is touched.

**Validation at `324eb343`:** each gate was run on its own, and every one exits 0.

- `python3 scripts/docs_check.py`, both with git and in a no-git export of the head. `scripts/check_feature_status.py` also runs in the no-git export.
- `check_em_dash.py --base f86c34fe` (0 findings), `check_doc_style.py`, `gen_toc.py --check` and `check_doc_paths.py`.
- `xvlog_gate.py --check`: `hdl/` 0 findings.
- `git diff --check`, from both `f86c34fe` and `910b4fb5` to the head.
- `git grep -n "step guard gap" -- tb docs` finds no match (rc 1).

**Not run:** the simulation suites, synthesis, act and hosted CI. The servo logic is byte-identical once comments are stripped. The act and hosted runs need the push first.

**Acceptance:** the required outcome of R282-2 F1 and R283-2 F1 is met. README:388 and GM_LOSS_RECOVERY.md:181 agree, and the grep is empty. Issue #539's acceptance criteria 1-3 are unaffected, because no logic or test changed.

**Open risks/questions:** one question for the reviewers. `324eb343` edits one comment line in the servo RTL file, so the RTL lens decides whether its round-2 coverage still holds at this head. `5c6d5f5b` is within the Docs lens's scope.

