[A787] REVIEW READY

Commit: 9aa55d3b382750353709c3ba9ff6f6416938e83b (`sync-dev-6b66f66d-into-dev-soft-core`, parent `1238a3ee`, on `e2be92b0`; local, nothing pushed; the manager pushes)

Changed: round 6 fixes R854-2-F1 (PR #934 issuecomment-6942847358, NEGATIVE at `e2be92b0`) at its cause. Two commits; harness grading, its self-test and two documents only. No firmware, RTL, testbench, build input, configuration, pin or bound changes.
- **Every owned MRP timer run-out is judged on its owner alone** (`mrpdu_grade.py`): the participant the testbench recorded at the expiry, and that owner's first transmit opportunity from the posted TICKs.
  - **The missing-build deadline** (`horizon`): absent past 49 ms after the owner's opportunity, unresolved where the log ends first. Before, it was the latest of every participant's.
  - **The frames that answer it** (`served`): only the owner's, released or late on the owner's first. A build that sends none of the owner's frames, nothing or only another participant's, is judged as one that sends nothing (`anchor`). Before, it was the first frame's participant's.
  - **The row's start** (`begin`, `start_of`): the owner's opportunity, though the commit carries another participant's MRPDU. Before, it was the earliest of the commit's participants.
  - Another participant's callback, running join timer or frame never defers the deadline, answers the run-out or times its row.
  - Unchanged: empty builds, owed-frame retries (`window`), short logs, the owner's own running join timer, LeaveAll grading, the unowned rule, 49 ms.
- **Findings** name the owner and the owner's opportunity: "the periodic timer's run-out at 1300.001 ms (if0 MSRP): its owner's first frame, or first build, 130.979 ms after the owner's transmit opportunity at 1300.001 ms, past THE TRANSMIT's 49 ms (late)".
- **Three standing controls** (`selftest_leaveall.foreign_checks`), each for both applications on both interfaces:
  - a missing build absent though another participant's join timer runs on, and unresolved in a short log;
  - another participant's MRPDU answering nothing: late past the bound, empty within it, no row on either interface; the owner's own frame released;
  - the row from the owner's opportunity: 10.0 ms, where the earlier rule gave 140.
- **A mutant per residual association**, each caught by its control by name: the latest participant's horizon; the first frame's participant; another participant's frame credited; the commit's earliest opportunity.
- **Docs:** the harness README and FR_NFR.md 3.4.1 state exactly what is proven for every MRP timer's run-out against its owner's first opportunity. The README's mutant table has 23 transmit and LeaveAll rows, each naming its check.

Validation (at `9aa55d3b`):
- **R854-2's `probe_missing_build.py`**, unchanged: **rc 0**.
  - All eight hidden cases fail by the actual owner at its original 1,300.001 ms opportunity: four absent and four late, MSRP and MVRP on interfaces 0 and 1.
  - Its four short-log controls stay unresolved; its absent and empty-late controls hold.
- **R854-2's other scripts:** `probe_ownership.py`, 60 controls, 0 failures; `check_focused_mutants.py`, all 15 caught.
- **Earlier probes:** R853-1's (owned: B fails on if0 MSRP, C0 and C late); R854-1's owned overlap (fails on MSRP at 1,180 ms); round 4's 24-case owner matrix (0 failures).
- **Harness self-test** on a clean clone: rc 0, 0 failures, 882 checks pass, all 265 mutants caught.
- **Docs jobs** on fresh clean clones: every job, 63 steps rc 0, 34 not run with a reason, 0 bad (`verify_wf.py` rc 0).
- **The published regrades**, round 4's thirteen legs with every build attested against the head:
  - every `table.md` is byte-identical to round 5b's, and each rc is round 5b's;
  - every MRPDU row, join interval and LeaveAll is the same;
  - the eleven 8x8/1if phases' 44 owned LeaveAlls are sent; worst rows leaveall 1.64360, periodic 2.96879, join 1.86217 ms, against 20 ms;
  - #901's valid-destinations leg at 1x1/1if: rc 0;
  - the 49 ms bound is unchanged.
- **What moves in the 26 traces:** 73 of the 1,871 MRP run-outs, 46 join and 27 periodic, from released to empty.
  - Each had been credited only to another participant's frame; in none did the owner send a frame of its own in those builds.
  - None becomes late or absent, and no run-out fails.
  - Each move is listed with its owner and the participant that answered it before.

Acceptance criteria:
- met: R854-2-F1 fixed at its cause; the reviewer's probe exits 0 with all eight cases failing by the actual owner at its original opportunity, its short-log controls unresolved; standing controls and a mutant per residual association, caught by name; the ownership controls, the existing mutants and the published regrades re-run; 49 ms unchanged; the text states what is proven; the self-test and docs jobs at the head;
- pending: #898 (merged at `cb96336d`) reaches this sync at composition, the manager's; this head does not include it.

Open risks/questions:
1. **The 8x8/1if `STATED` lines** remain #914's. Every 8x8 leg exits 1 on them alone.
2. **R853-2 POSITIVE at `e2be92b0`** (PR #934 issuecomment-6942941438) predates this round. Round 6 changes `mrpdu_grade.py`, `join_grade.py`, `run.py`, the self-test and the two documents within its lenses, so its coverage needs renewing at `9aa55d3b`.

Found, not fixed (as before): twin and twin-plants (#929); srptx (#916); #840's 1000BASE-T-only advertisement on the split (#919).

Receipts, the handoff and the PR body are in the lane's round-6 output.
