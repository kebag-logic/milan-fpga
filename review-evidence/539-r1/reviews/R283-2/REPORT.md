[R283] NEGATIVE - exact head 910b4fb5f104ac35e8cc1723a70de0d05672895d

Round R283-2, external independent review of issue #539 / PR #547, tree `9dac4c8295506c4600126e692531c02053fd971c`.

Lenses applied: Conformance, RTL, Robustness, Tests, Docs. Four lenses are clean. One open MINOR under Docs makes the verdict NEGATIVE.

## Summary

- **RTL logic is unchanged since round 1.** `git diff f49b57a6..910b4fb5 -- hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` changes only the detector comment (`:296-303`). The other RTL in that range (`milan_datapath.sv`, `KL_crf_rx.sv`) comes from dev `f86c34fe` (#529/#534) through merge `0df54c1f`, and it does not touch the servo's instance or ports.
- **Both round-1 Tests findings are fixed.** I re-ran my round-1 mutation set unchanged against both harnesses at this head (`scripts/mutate.py`, `probe.sh` and `batch.sh` are byte-identical to round 1, `receipts/round1_scripts_unchanged.txt`).
  - Detector off (M1): U10 now fails. Both landing-edge checks read 0 against [1,3] and 6, and 7 unit checks fail in all.
  - `no_resync` (M8): U11 now fails, reading a 32-tick gap where the check expects 33.
  - The three round-1 survivors named by the optional arms (`no_streak_reset`, `step_ignores_valid`, `no_saturate`) now fail named U12 checks. So does my new `idle_no_clear` mutant.
  - Every mutant killed in round 1 still dies. Each step-suite failure count is identical to round 1 (`receipts/mutation_r1_vs_r2.txt`).
- **The round-2 docs edits are correct.** `GM_LOSS_RECOVERY.md:152`, `:154` and `:181` and `TIME_SYNC.md:147-148` are accurate against the RTL and dev's Step policy section. The grid-aligner row states the #387 part b owner decision (issue 387 comment 5810378282).
- **One stale sibling line remains.** The #540 merge brought `tb/verilator/milan_dp/README.md` into the lane. At `:388` it still says the CRF servo's "step guard gap is #539". Its twin at `GM_LOSS_RECOVERY.md:181` was corrected in this round, and commit `910b4fb5` edited the line directly above it (F1).

## Findings

### F1 - MINOR - lenses: Docs

- **Artifact:** `tb/verilator/milan_dp/README.md:388`, which reads "- The CRF servo. The MMCM DRP answers zero; its step guard gap is #539." It sits in the gmstep leg's "What the leg does not grade" list.
- **Authority/evidence:**
  - AGENTS.md section 6, Docs lens: "Changed contracts are reflected in authoritative docs". Section 7: "authoritative documentation is current".
  - This PR closes #539: the servo now discards a step window (`KL_mmcm_drp_servo.sv:650-670`), which `Vphc_step` grades at 113/113 (`receipts/probes/head_phc.log`). So after merge the line states a gap that no longer exists.
  - The same #540 text in `GM_LOSS_RECOVERY.md:181` ("its DRP answers zero; see #539") was corrected in this round to "`Vphc_step` grades its step discard (#539)". The README's twin was not, although commit `910b4fb5` edited the README's line 387 directly above it.
  - The PR body's Docs section lists the README as updated.
  - Receipt: `receipts/docs_539_refs.txt` (the dev `f86c34fe` text and the head text).
- **Why Docs only:** no check, RTL or requirement depends on the line. It is the leg's scope statement. The gmstep leg's checks are unaffected.
- **Impact:** after merge, a reader of the milan_dp README is told the CRF servo still has an open step-guard gap tracked by #539. #539 will be closed, and `GM_LOSS_RECOVERY.md:154`/`:181` and `TIME_SYNC.md:147` say the opposite. This is the same class of stale statement as R282-1 F2, on a file R282-1 F2 did not name.
- **Required outcome:** `README.md:388` states the current fact, consistent with `GM_LOSS_RECOVERY.md:181`: the leg does not grade the servo because the DRP answers zero, and the step discard is graded by `Vphc_step` (#539). What still reaches the servo (#545, #546) may be named. The pointer in `sim_gmstep.cpp:16`, "(the DRP answers zero; #539)", claims no gap and may stay as it is.
- **Verification:**
  - `git grep -n "step guard gap" -- tb docs` returns nothing at the new head.
  - The README line and `GM_LOSS_RECOVERY.md:181` agree.
  - A Docs re-review at that head. A README-only commit changes nothing in the other four lenses' scope.

No other finding. There is no SUGGESTION this round.

## Lens results (clean lines carry their evidence)

```text
[R283] PASS Conformance - hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:446-462,650-670; receipts/probes/head_phc.log, head_trace150.log, repro_trace150.log - acceptance 1-3 at this head: the pre-fix 150 us step moves the integrator +15680 -> +90700 and drops to ACQUIRE (repro); at the head the same step leaves it +15680 -> +15700, LOCKED, 1 discard; the silicon-scale sweep 21 us to +/-1 s passes 113/113; the detector threshold 4096 ns sits below the Step policy's smallest step (docs/design/TIME_SYNC.md:83-86, 20 us link-up, 100 us locked); detection at ptp_now_i instead of wiring phc_step_we_o accepted as satisfying acceptance 2 (every PHC step source lands there in one cycle; milan_datapath.sv:2811-2833, gtx_clk == axis_clk)
[R283] PASS RTL - KL_mmcm_drp_servo.sv:296-304 against hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv:100-101,109-110,144-145 and milan_datapath.sv:2813-2816 - the round-2 RTL change is comment-only (git diff f49b57a6..HEAD); the incr + adj bound holds (unsigned Q8.24 in 32 bits < 256 ns, signed Q8.24 addend in [-128,128) ns, sum < 384 ns, 4096 ns is 10.7x above); the merged dev RTL (milan_datapath.sv #529 counters, KL_crf_rx.sv comments) leaves the servo instance and ports unchanged (milan_datapath.sv:5525-5529); focused -Wall lint base == head, one pre-existing UNUSEDPARAM (receipts/lint_servo_base.txt, lint_servo_head.txt)
[R283] PASS Robustness - KL_mmcm_drp_servo.sv:451-462,499-502,551,605-613,650-670; receipts/probes/head_unit.log, head_phc.log - reset (ptp_jump_r reset; IDLE clears tally and streak: idle_no_clear killed), maximum (tally saturates at 63, 63+2 fits the 7-bit sum: no_saturate killed), ordering (step and guard on one cycle P3; two steps one edge apart counted once U12: step_ignores_valid killed; boundary cases P2a/b/c), repetition (U10 six-step storm, U12 64-step burst), backward steps (P1 -100/-150 us, -1 s; fwd_only killed, 51 failures), feature-disabled (tally and step block only in ACQUIRE/LOCKED/HOLDOVER, :551), 2^32 ns alias documented at :74-77 and outside the 1 s acceptance range
[R283] PASS Tests - tb/verilator/mmcm_servo/sim_main.cpp:18-28,127-172,378-468,470-578; receipts/mutation_table.txt, mutation_r1_vs_r2.txt - every U10/U11/U12 claim fails for the defect it names: det_off 7 (U10 landing-edge got 0 vs [1,3], storm 0 vs 6), no_resync 2 (U11 33-tick gap reads 32), disc_max3 4, no_streak_reset 2, step_ignores_valid 1, no_saturate 1, idle_no_clear 1, tally_guard_only 7 unit / 15 step suite; the U10 comment now credits trim, LOCKED and count to either guard and claims only the landing-edge timing for the step guard, which is what fails; all 18 mutants die in at least one harness, no round-1 kill regresses, step-suite counts identical to round 1; the U11/U12 phase windows hold for any boundary phase (6th discard at <= 193 of the 224 offset ticks)
[R283] F1 MINOR Docs - tb/verilator/milan_dp/README.md:388 - stale "step guard gap is #539" (see Findings); the other Docs artifacts are correct: GM_LOSS_RECOVERY.md:152,154,181 against the RTL and issue 387 comment 5810378282 (receipts/c387_5810378282.txt); TIME_SYNC.md:147-148 against the Step policy section :75-101 (a <= 100 us slew is not a step and still reaches the integrator, #545); REGISTER_MAP.md:1942 [15:10] against the status_o packing at KL_mmcm_drp_servo.sv:907; TESTING.md:481
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #539 acceptance 1-3 and assignment comments; TIME_SYNC.md Step policy :75-101; KL_mmcm_drp_servo.sv:446-462,650-670; head_phc, head_trace150, repro_trace150 receipts | R283-2 | `910b4fb5f104ac35e8cc1723a70de0d05672895d` |
| RTL | CLEAN | KL_mmcm_drp_servo.sv (diff vs base 26d855a9 and vs f49b57a6); timestamp_counter.sv:100-145; milan_datapath.sv:2811-2833,5525-5529; lint_servo receipts | R283-2 | `910b4fb5f104ac35e8cc1723a70de0d05672895d` |
| Robustness | CLEAN | KL_mmcm_drp_servo.sv:451-462,499-502,551,605-670; U10/U11/U12 and P1-P4 receipts; the idle_no_clear, no_saturate, step_ignores_valid and fwd_only mutants | R283-2 | `910b4fb5f104ac35e8cc1723a70de0d05672895d` |
| Tests | CLEAN | sim_main.cpp (diff vs f49b57a6), sim_phc_step.cpp (unchanged since round 1), Makefile; 48 probe receipts; mutation_table, mutation_r1_vs_r2 | R283-2 | `910b4fb5f104ac35e8cc1723a70de0d05672895d` |
| Docs | UNCLEAN (F1 open) | GM_LOSS_RECOVERY.md:142-186; TIME_SYNC.md:75-151; REGISTER_MAP.md:1942; TESTING.md:481; milan_dp/README.md:385-392; sim_gmstep.cpp:15-19; the PR body; issue 387 comment 5810378282 | R283-2 | `910b4fb5f104ac35e8cc1723a70de0d05672895d` |

## Prior public review findings (read after my own pass over the diff)

- **R283-1 F1 = R282-1 F1, U11 part (Tests): RESOLVED.**
  - U11 now reads the discard gaps off `MCSRV_STAT[15:10]`: 32, 32, 32, 33, 32 (`head_unit.log`).
  - `no_resync` fails U11 and U12 with a 32-tick gap. `disc_max3`, a round-2 addition, also fails.
  - The label, comments and PR body claim only the re-base's one-tick shift.
- **R282-1 F1, U10 part (Tests, Docs): RESOLVED.**
  - `det_off` fails both U10 landing-edge checks. The step is counted on edge 2 at the head and not within 64 edges without the detector.
  - The U10 comment now says the 1024 ppm guard would catch these windows too, and that trim, LOCKED and the count cannot tell the two guards apart. That is true: `storm: one discard per step` still reads 6 under `det_off`.
- **R282-1 F2 (Docs): RESOLVED as named.**
  - `GM_LOSS_RECOVERY.md:152`, `:154` and `:181` and `TIME_SYNC.md:147` are corrected.
  - `git grep "108 to 524"` is empty.
  - The TIME_SYNC loop-table rows combine cleanly with the Step policy section.
  - Its sibling line in the milan_dp README was not in F2's list. It is the new F1 above, not a retention.
- **R283-1 S1/S2 = R282-1 S1 (Tests): RESOLVED.** Streak restart, the open-window rule and saturation each have a U12 arm that fails for its mutant. IDLE clearing is armed too (`idle_no_clear` is killed).
- **R283-1 S3 = R282-1 S2 (RTL, Docs): RESOLVED.** The comment at `KL_mmcm_drp_servo.sv:296-303` now bounds the per-cycle advance by `incr + adj`, below 384 ns. I verified this against `timestamp_counter.sv`.

## Real limits

- **What I ran:** only the three `mmcm_servo` harnesses (unit 78/78, rails 8/8, step suite 113/113), in disposable copies built with `probe.sh`. They use the Makefile's flags and `UNIT_G`, at `-j 1`.
- **Not run by me:**
  - `mmcm_servo_autorepair`, `milan_dp` (aclk, gmstep, the default suite) and `milan_dp_render`.
  - The parent, PP, gPTP, Yosys and builder banks, the docs gates, act, and Vivado timing.
  - The detector's timing cost on silicon is unmeasured.
- **Manager's head-level bank receipts:** the public tree `1363d132 review-evidence/539-r1` holds the round-1 author packet only. I found no head-level receipt of the manager's static, builder and native banks there, and I have not verified that claim.
- **Hosted evidence** (`receipts/hosted_check_runs.tsv`, read during this round): executed jobs are `rtl-fast`, `verilator-lint`, `yosys-elaboration`, `elaborate`, `docs-check`, `docs-check-no-git`, Yosys shards 0-3 and Verilator shards 0-3, all successful. Verilator shard 4/5 was still in progress. `Physical gPTP` was skipped and is not hardware proof.
- **No hardware or physical calibration** was run. The unit harness drives `ptp_now_i` with zero delay at the clock edge. The U10 edge window [1,3] tolerates one edge of skew.
- **Candidate merge result not validated.** I did not build it against live dev `3d2f3e31`. Read-only compare `f86c34fe...3d2f3e31`: 8 commits, docs only. The one `TIME_SYNC.md` change adds a line near `:63` about asymmetry (#511), clear of the rows reviewed here (`receipts/livedev_time_sync_patch.txt`).

## Pending manager duties

- Fix F1 and get a Docs re-review at the new head. The other four lenses stay banked at `910b4fb5` if the fix touches nothing in their scope.
- Build and validate the candidate against live dev `3d2f3e31`.
- Obtain completion of hosted Verilator shard 4/5 and the act replica at the final head.
- Obtain the second positive review, maintainer merge authorisation, post-merge containment, and closure of #539.
- Record the status of physical calibration (NOT RUN).

## Reproduce

Set `VERILATOR` to the pinned 5.050 wrapper (identity in `receipts/tool_identity.txt`, unchanged from round 1). Extract `git archive` trees to `scratch/head`, `scratch/base` (26d855a9), `scratch/r1head` (f49b57a6) and `scratch/repro` (c16cd61e). Then:

- `sh scripts/batch.sh scripts/jobs1.txt` for the baselines.
- `sh scripts/batch.sh scripts/jobs2.txt` for the round-1 mutants. I ran it in 8-line parts.
- `PROBE=probe_r2.sh sh scripts/batch_r2.sh scripts/jobs_r2_extra.txt` for the round-2 additions.
- `python3 scripts/table.py .` and `python3 scripts/compare_r1.py <round-1 table> receipts/mutation_table.txt` for the tables.
- `sh scripts/lint_servo.sh <tree>` for the lint.

After the probes the clone is byte-identical to the head. Index modes and blobs equal the HEAD tree, 879 entries. The worktree and index are clean. The gitlinks are unchanged: gptp-processor e5dcea6e, protocol-processor 424c688f, verilog-axis 48ff7a7e, external efeb541a (`receipts/clone_integrity.txt`).

R283-2 FINISHED
