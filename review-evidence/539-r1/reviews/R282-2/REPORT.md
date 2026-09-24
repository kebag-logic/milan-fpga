[R282] NEGATIVE - exact head 910b4fb5f104ac35e8cc1723a70de0d05672895d

# R282-2 internal independent review: issue #539 / PR #547, round 2

- Head `910b4fb5f104ac35e8cc1723a70de0d05672895d`, tree `9dac4c8295506c4600126e692531c02053fd971c`, verified in the review clone (`receipts/clone_integrity.log`).
- Source base `26d855a9176d63625e6635a029a0c44e3d57ce9a`. The lane merged dev `f86c34fe` at `0df54c1f`. The PR-owned delta is `f86c34fe..910b4fb5`: 9 files, +840/-29.
- Round-2 commits: `efad18c7` (docs), `49098290` (unit harness), `10004650` (servo comment), `910b4fb5` (#387 part b owner decision in docs).

## Verdict

**NEGATIVE, on one MINOR (Docs).**

Round 1's two MINORs are resolved at this head:

- **Tests:** the U10 and U11 claims now fail for what they name.
- **Docs:** the `GM_LOSS_RECOVERY.md` rows now describe the fix.

What remains open: the gmstep README's "does not grade" list still says the CRF servo's step-guard gap is #539. That list is the twin of `GM_LOSS_RECOVERY.md:181`, which was corrected. The README line came in through the dev merge, and it goes stale when this PR lands.

The RTL logic is unchanged since round 1. The only servo edit is a comment. Conformance, RTL, Robustness and Tests are covered clean at this head.

## Findings

### F1 - MINOR - lenses: Docs - `tb/verilator/milan_dp/README.md:388` - the gmstep leg's "does not grade" list still says the servo's step-guard gap is open

- **Artifact:** `tb/verilator/milan_dp/README.md:388` at the head reads "The CRF servo. The MMCM DRP answers zero; its step guard gap is #539."
  - It is the README twin of `docs/design/GM_LOSS_RECOVERY.md:181`. That line was corrected in `efad18c7` to "`Vphc_step` grades its step discard (#539)".
  - Line 387, directly above it, was rewritten in `910b4fb5`. Line 388 was not.
  - Blame: `021b2e07b` from #540, carried in by the dev merge `0df54c1f`.
  - Evidence: `receipts/doc_rows.txt`.
- **Authority/evidence:**
  - AGENTS.md section 6, Docs lens: changed contracts are reflected in the docs, and obsolete statements are not carried forward. Section 7 requires that "authoritative documentation is current".
  - The manager's round-2 assignment (issue 539 comment 5809512999) required the #539 pointers inherited from #540 to be corrected.
  - The PR body's Docs section reports the gmstep README list as updated.
  - At this head the servo discards every step window from 4.1 us up. The step suite proves this: `receipts/head_suite.log`, P1 at every size, 113/113. So "its step guard gap is #539" describes a defect this PR closes.
- **Impact:** after merge, the leg's README tells a reader that the CRF servo still has a step-guard gap. That contradicts `GM_LOSS_RECOVERY.md:154`/`:181`, `TIME_SYNC.md:147` and the RTL in the same tree. A cold reader following it would treat #539 as open work.
- **Required outcome:**
  - `README.md:388` states the servo's post-#539 behaviour, consistent with `GM_LOSS_RECOVERY.md:181`: the leg does not grade it because the DRP answers zero, and `Vphc_step` grades the step discard.
  - Optionally, the same wording check for the parallel header comment at `tb/verilator/milan_dp/sim_gmstep.cpp:16` ("the DRP answers zero; #539").
- **Verification:**
  - `git grep -n "step guard gap" -- tb docs` returns nothing.
  - A Docs re-review at the answering head. A README-only change un-covers only Docs.

### S1 - SUGGESTION - lenses: RTL, Docs - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:302` - the "5x below" margin is 4.9x

The corrected comment says 4096 ns sits "5x below" the plane's smallest step of 20 us. 20000 / 4096 = 4.88. The margin is still ample, and the "over 10x above" 384 ns side is right (10.7x). Optional: "nearly 5x", or give the figure. This does not affect coverage.

## What was checked, and the result

### Round-1 findings: re-checked at this head

**R282-1 F1 = R283-1 F1 (Tests): RESOLVED.** I re-ran my round-1 mutant set unchanged. `scripts/mutate.py` is byte-identical to round 1, sha256 `a644e224...`. Both harnesses, at this head:

- **M1 (step detector off)** now fails the unit harness, 7 of 78 (`receipts/mut/M1_detector_off.log`):
  - `[U10] step counted as it lands` got 0 (expected 1..3), at `sim_main.cpp:426`;
  - `[U10] storm: every step counted as it lands` got 0 (expected 6), at `:452`;
  - plus five U12 arms.

  Every U10 trim, LOCKED and count check still passes under M1. That confirms the new comment: at this scale the 1024 ppm guard would also catch these windows, so only the landing-edge timing tells the two guards apart. The step suite fails 66 of 113, as in round 1.
- **M8 (the guard's 4-discard re-base removed)** now fails `[U11] the 4th re-bases: 5th is 33 ticks on` (`:502`) and `[U12] the 4th after the step re-bases` (`:542`). Both read 32 where 33 is expected. Gap lines: `32 32 32 32 32 32` against the head's `32 32 32 33 32 32`.
- Timing claim, checked by hand against the RTL:
  - The step guard counts on the 2nd `clk_i` edge. `ptp_jump_r` rides with `ptp_q_r` (`KL_mmcm_drp_servo.sv:452-455`), and the tally registers on the next edge (`:666-670`).
  - The 1024 ppm guard needs a boundary on the stepped sample (edge 2 at the soonest), then S1 to S4 (`:579-615`), so it counts at edge 6 or later.
  - A reviewer mutant with the verdict three cycles late (M17) counts at edge 5 and fails U10, so the bound check discriminates.
- The labels and header (`sim_main.cpp:19-28`) and the PR body now claim only what these checks fail for.

**R282-1 F2 (Docs): RESOLVED for its named rows. The README twin is carried as F1 above.**

- `GM_LOSS_RECOVERY.md:154`, CRF servo row: the step window is discarded, trim and integrator held, counted in `MCSRV_STAT[15:10]` (#539). The 1024 ppm guard is kept. The slew (#545) and the talker's step (#546) still reach the servo.
- `:152`, grid-aligner row: states the #387 part b owner decision (issue 387 comment 5810378282): no re-centre of its own, the step kept out of the aligner's reference by #539, #545 and #546, and option B only if #545/#546 cannot close. I read the decision comment and the row matches it clause by clause.
- `:181` names `Vphc_step`.
- `git grep "108 to 524" -- docs/design` is empty.
- `TIME_SYNC.md:147-148` combine cleanly with dev's "Step policy" section (`:75-107`):
  - The policy's smallest step (20 us link-up) exceeds the 4096 ns detector.
  - The policy slew (up to 100 us at up to 200 ppm) is correctly called "not a step" that still reaches the integrator (#545).
  - The implausible-window row matches `GUARD_THR_C = 2^19` (1024 ppm at 512 units/ppm) and `DISC_MAX_C = 4`.

**R282-1 S1 = R283-1 S1/S2 (streak restart, open-window rule, saturation): RESOLVED by U12.**

- M12 fails `:539`/`:542` (the re-base follows the 2nd guard discard after the step).
- M13 fails `:557` (two steps one edge apart counted twice).
- M14 fails `:572` (got 23, not 63).
- A new reviewer mutant, M16 (IDLE does not clear the tally), fails `:577` (got 63, expected 0).

**R282-1 S2 = R283-1 S3 (the `incr + adj` bound): RESOLVED.** `KL_mmcm_drp_servo.sv:296-303` now bounds the advance by `incr + adj`, below 384 ns. S1 above is a residual wording nit.

**R283-1 F1 option (a) is what was implemented. It is the same resolution as R282-1 F1.**

### Mutation table at this head (`receipts/mutation_summary.txt`)

| Mutant | Unit fails / 78 | Step suite fails / 113 | Round-1 step-suite count |
|---|---|---|---|
| M1 detector off | 7 | 66 | 66 |
| M2 no abandon | 3 | 53 | 53 |
| M3 no boundary squash | 0 | 19 | 19 |
| M4 unconditional squash | 0 | 1 | 1 |
| M5 1024 ppm guard off | 10 | 7 | 7 |
| M6 single tally | 0 | 1 | 1 |
| M7 guard at 32 ppm | 41 | 3 | 3 |
| M8 no guard re-base | 2 | 0 | 0 |
| M9 detector at 25 us | 0 | 23 | 23 |
| M10 signed detector | 0 | 51 | 51 |
| M11 verdict one cycle late | 0 | 23 | 23 |
| M12 step keeps the streak | 2 | 0 | 0 |
| M13 step counted with no window open | 1 | 0 | 0 |
| M14 tally wraps | 1 | 0 | 0 |
| M15 step not tallied | 7 | 15 | 15 |
| M16 IDLE keeps the tally (round-2 reviewer) | 1 | 0 | n/a |
| M17 verdict three cycles late (round-2 reviewer) | 3 | 20 | n/a |

- Every mutant dies, and none survives.
- Every step-suite count is identical to round 1. The step suite is unchanged in round 2.
- The four round-1 survivors (M8, M12, M13, M14) now fail named unit checks.
- Each mutant anchor matched exactly once. `APPLIED` is the first line of each log.

## Lens results (each clean line carries its evidence)

[R282] PASS Conformance - issue #539 acceptance 1-3; `KL_mmcm_drp_servo.sv:446-462,650-670`; `receipts/head_suite.log`, `receipts/mut/M1_detector_off.log`, `receipts/hosted_check_runs.tsv`

- **Acceptance 1 (reproduction):** with the detector off, which is the pre-fix behaviour below 524 us, a locked +150 us step moves the integrator by 44980 and the written rate by 21780, and drops LOCKED. A -150 us step moves them by -82160 and -51200 (`M1_detector_off.log:142-153`). This is the claim reproduced at the silicon window scale. The base-RTL reproduction was done in round 1, and the servo logic is byte-identical since then except for comments.
- **Acceptance 2:** at the head, every P1 size from 21 us to +/-1 s is counted once, moves the integrator 0 (bound 512), and holds LOCKED on every edge. At 150 us: `head_suite.log:200-205`.
- I accept the interpretation that detecting the pulse's effect at `ptp_now_i` meets "any PHC step (the plane's step pulse) discards the servo window that contains it". The pulse becomes one adjtime in `timestamp_counter`. Per `milan_datapath.sv:2811-2833`, `ptp_now_w` is read synchronously on the servo's `axis_clk`.
- **Acceptance 3:** there are failing arms for the step discard (M1-M4, M9-M11, M15, M17), the guard (M5, M8) and the rate path (M7 fails P4). My focused suites are green. Every executed exact-head hosted context completed success. Physical gPTP was skipped by design and is not hardware proof.

[R282] PASS RTL - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:293-303,441-462,551-670,907`; `git diff f49b57a6..910b4fb5 -- hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` (comment-only, 7+/5-); `receipts/head_suite.log` (0 simulator warnings under `-Wall`)

- Round 2 changes only the detector comment. Its `incr + adj` < 384 ns bound matches `timestamp_counter.sv:142-145`: 32-bit Q8.24, unsigned `incr_i`, signed `adj_i`.
- I re-traced the logic at this head.
  - `ptp_jump_r` is synchronously reset. Its verdict is aligned with `ptp_q_r`. The unreset `ptp_q_r` is masked by `win_valid_r = 0` after reset.
  - `guard_hit_w` equals the previous in-case guard condition.
  - Step writes are placed after the tick branch and the micro-sequence, so they win.
  - A boundary on the stepped sample is squashed only when no sequence is in flight.
  - A coincident S4 guard hit and step count 2 through the 7-bit saturating sum (63 + 2 fits).
  - The tally is updated only in ACQUIRE/LOCKED/HOLDOVER, and IDLE clears it with no conflicting write.
- No port, CDC or clock change. The dev merge did not touch the servo (`git diff 26d855a9 f86c34fe -- <servo>` is empty).

[R282] PASS Robustness - `KL_mmcm_drp_servo.sv:452-462,499-548,650-670`; `timestamp_counter.sv:142-170`; U12 at `sim_main.cpp:539-577`; `receipts/mut/M12..M16*.log`

- Checked:
  - repeated steps: the U10 storm, and two steps one edge apart counted once (`:557`);
  - tally overflow: 64 steps saturate at 63 (`:572`);
  - reset and IDLE: the tally is cleared (`:577`);
  - streak interaction with the 1024 ppm guard: the step restarts the streak (`:539-542`);
  - both signs and the range edges: P1 21 us to +/-1 s;
  - boundary positions P2a/b/c;
  - HOLDOVER: windows run and `pp_run_r` is 0, so a step abandons and counts with no PI effect;
  - VERIFY/REPAIR/FAULT/IDLE: the window block is gated off.
- Only `cmd_load`/`cmd_adjust` move `ptp_now` more than 384 ns in a cycle, so no legitimate time movement trips 4096 ns.
- The documented 32-bit alias near k*2^32 ns falls to the 1024 ppm guard (`:74-77`).

[R282] PASS Tests - `tb/verilator/mmcm_servo/sim_main.cpp:19-28,142-172,372-460,468-510,513-580`; `sim_phc_step.cpp` (unchanged); `receipts/head_suite.log` (78/78, 8/8, 113/113; autorepair 47/47); `receipts/mutation_summary.txt` (17 mutants, 0 survivors)

- Each new or changed check can fail for what it names:
  - U10 landing-edge checks: M1, M15, M17;
  - U11 33-tick gap: M8;
  - U12 streak: M12;
  - U12 open window: M13;
  - U12 saturation: M14;
  - U12 IDLE: M16.
- The arms assert their own preconditions: "two guard discards open a streak", "tally below 63 before the burst", "the step counted as it lands".
- Discard times come from the DUT's own `MCSRV_STAT[15:10]`, not from a model of the implementation.
- Existing regressions stay green, and every round-1 kill still dies with identical step-suite counts.

[R282] UNCLEAN Docs - see F1 (`tb/verilator/milan_dp/README.md:388`).

- Also examined and correct:
  - `GM_LOSS_RECOVERY.md:152,154,181`;
  - `TIME_SYNC.md:147-148` against `:75-107`;
  - `REGISTER_MAP.md:1942` (`[9]` reserved, `[15:10]` saturating discard tally cleared in IDLE, matching `status_o` at `:907`);
  - `TESTING.md:481`;
  - the `Makefile` header and targets;
  - the servo header `:54-77`;
  - the PR body's round-2 table against my mutant receipts. Every unit and step-suite count it gives matches.
- Gates: `docs_check`, `check_em_dash --base f86c34fe` (0 findings, 57/57 arms), `check_doc_style`, `check_doc_paths`, `gen_toc --check` and `git diff --check` all exit 0 (`receipts/static_gates.log`).

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #539 acceptance 1-3; servo `:446-462,650-670`; head step suite P1-P4; M1 reproduction trace; exact-head hosted contexts | R282-2 | 910b4fb5f104ac35e8cc1723a70de0d05672895d |
| RTL | CLEAN | `KL_mmcm_drp_servo.sv:293-303,441-462,551-670,907`; round-2 comment-only diff; `timestamp_counter.sv:142-170`; `milan_datapath.sv:2811-2833` | R282-2 | 910b4fb5f104ac35e8cc1723a70de0d05672895d |
| Robustness | CLEAN | servo `:452-462,499-548,650-670`; U10 storm; U12 arms; P1 range and P2 positions; M12-M16 | R282-2 | 910b4fb5f104ac35e8cc1723a70de0d05672895d |
| Tests | CLEAN | `sim_main.cpp` U10-U12; `sim_phc_step.cpp`; Makefile; 15 round-1 + 2 round-2 mutants on both harnesses; head suites | R282-2 | 910b4fb5f104ac35e8cc1723a70de0d05672895d |
| Docs | UNCLEAN (F1) | `GM_LOSS_RECOVERY.md:152,154,181`; `TIME_SYNC.md:75-107,147-148`; `REGISTER_MAP.md:1942`; `TESTING.md:481`; `milan_dp/README.md:387-388`; `sim_gmstep.cpp:16`; PR body; docs gates | R282-2 | 910b4fb5f104ac35e8cc1723a70de0d05672895d |

## Real limits

- **Not run by this reviewer:**
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - the `milan_dp` legs (`aclk`, `tdm8render`, `gmstep`);
  - Vivado timing;
  - hardware and physical calibration;
  - act and Docker.

  The CRF-leg false-step check on the real PHC (`A_MCSRV_STAT = 0x33`) is round-1 evidence at `f49b57a6`. The servo logic is unchanged since then.
- The base-RTL reproduction was not re-run this round. Acceptance 1 is cited from the detector-off mutant, which reproduces pre-fix behaviour below 524 us, and from round 1.
- **Hosted evidence** (`receipts/hosted_check_runs.tsv`): every executed context at the exact head completed success. "Physical gPTP (nightly and manual)" was skipped, which is not hardware proof. The manager owns hosted and act acceptance.
- Mutant runs used `-j 1` builds, at most 5 concurrent, on a shared host. Timing did not affect results, because the simulations are deterministic.
- `CHANGELOG.md` is not touched by the PR. No rule in CONTRIBUTING.md or the frozen acceptance requires an entry, so this is not a finding.

## Pending manager duties

- Route F1 to the author. A README-only fix un-covers only Docs, and Docs must then be re-covered at the answering head. Conformance, RTL, Robustness and Tests stay covered if nothing under their scope changes.
- The final current-dev candidate build is still to do: source base `26d855a9`, live dev `3d2f3e31`. Candidate-merge validation and post-merge containment remain manager duties.
- Merge requires the second independent positive review and the full section 7 bar.

## Reproduce

All scripts are under `scripts/` and read `scripts/env.sh`. Override `PKT`, `CLONE` or `VERILATOR` to relocate.

- `sh scripts/run_head_suite.sh`: `mmcm_servo` and `mmcm_servo_autorepair` at the head.
- `JOBS=5 sh scripts/run_batch.sh run_mutant.sh M1_detector_off ...`: the round-1 set (`mutate.py`, unchanged).
- `sh scripts/run_batch.sh run_mutant_extra.sh M16_idle_no_clear M17_detect_3_late`: the round-2 reviewer mutants.
- `sh scripts/run_static_gates.sh`: the docs and static gates.
- `sh scripts/clone_integrity.sh`: checks the clone.

The simulator is the pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`).

R282-2 FINISHED
