[A787] REVIEW READY

Commit: 6ceed75374210935cff4f10d014b9a5ef137615e (`sync-dev-6b66f66d-into-dev-soft-core`, local; nothing pushed; the manager pushes)

Changed: round 3 of the dev sync, on the rulings of #665 issuecomment-6930885185. One commit on round 2's `9715a30a`, `6ceed753`: harness grading, its self-test and documentation, and no firmware, RTL or bound change (Q1).
- **THE TRANSMIT's MRPDU row** is timed from the participant's transmit opportunity (IEEE 802.1Q-2018 10.7.4.1). That is the TICK that runs the participant's join timer out, where the timer its last commit armed still runs, and the timer's own TICK otherwise (`mrpdu_grade.opportunity`, `begin`). A participant is an interface and an MRP application, told by its MRPDU's EtherType. Lateness and absence count from it too. The bound is unchanged.
- **The check:** a LeaveAll timer's run-out owes its participant's LeaveAll, read from the MRPDU's VectorHeaders as lwSRP's `mrp_pdu.c` reads them. It must be the participant's first MRPDU after the run-out, and within 49 ms of that opportunity (`mrpdu_grade.leave_alls`). A skipped, late or absent one is named, "(LeaveAll past its first transmit opportunity)", "(LeaveAll late)" or "(LeaveAll absent)", and fails the run.
- **The planted defect:** a participant that sends an MRPDU without the LeaveAll at its first opportunity and the LeaveAll at the next. It is caught by name in `selftest_leaveall.py`, beside checks for:
  - the row from the join timer's run-out (1 ms, where the run-out gives 131 ms);
  - an idle join timer;
  - a late LeaveAll;
  - another application's MRPDU;
  - absent and unresolved;
  - the parser on MSRP, its Listener and MVRP.
- **Eight mutants**, each caught by a named check.
- **The docs:** the harness README and FR_NFR.md 3.4.1 state the start point. FR_NFR's 49 ms was already derived from it.

Validation:
- **Harness self-test** on a clean clone of `6ceed753`: 871 checks pass, 0 failures, all 254 mutants caught, the eight new ones included.
- **Docs jobs** on clean clones of `6ceed753`: every job, 63 steps rc 0, 34 not run with a reason, 0 bad.
- **The eleven LeaveAll phases at 8x8/1if, regraded** from their logs at `6ceed753`'s harness: the ten seeds and the product MAC.
  - **Every phase holds.** All 44 LeaveAlls went out at their first transmit opportunity, and no run-out is late.
  - The worst rows are leaveall 1.64 ms, periodic 2.97 ms and join 1.86 ms, against the unchanged 20 ms; round 2's worst was 160.6 ms.
- **#901's valid-destinations leg at 1x1/1if** now exits rc 0 (round 2: 1).
- **All 13 harness legs** regrade at `6ceed753`, every build accepted.
  - Eleven tables are byte-identical.
  - 8x8/1if parts 1 and 2 change only in their MRPDU rows (160.6 to 0.6 ms, 0 misses).
  - 1x1/1if arm A keeps 0, 0, 0 and 7 (the ruled held-egress rows).
  - The flip and load checks pass.
- **Routes, regraded against #818's floor** (Q3): +0.030 ns setup and 0 ns hold at every corner, on the best of three directives. All fifteen recorded routes, rounds 1 and 2:
  - split 1x1/1if meets on all three directives (best +0.196 / +0.036 ns);
  - split 8x8/1if meets on AltSpreadLogic_high (+0.140 / +0.036 ns); its other two are setup misses (+0.014, -0.595);
  - release AX7101 1x1 meets on all three (best +0.209 / +0.016 ns).
- **Carried from round 2** (`6ceed753` changes harness grading and documentation only):
  - all four workflows at `9715a30a`: 154 steps rc 0, 256 not run with a reason, 0 bad;
  - all 65 suites of the sweep;
  - `split` 84 of 84, `split-mutants` 28 of 28;
  - the images (32 to 40 B more `rom`, no tile moved, no BRAM debt).

Acceptance criteria:
- met: Q1 (the row's start, the check and its planted defect, the regrade of the eleven phases and of the valid-destinations leg); Q3 (every route regraded against #818 and stated); the round-2 bar as carried.
- **not met until #898:** `record_classes.py` refuses one 1x1/1if paced record (Q2).

Open risks/questions:
1. **Q2, the paced record at 1x1/1if.**
   - The accepted SET_CONFIGURATION is 28,700 cycles, 305 us by the rule, against `edit_rows.PACED`'s 300 us.
   - #898 round 7 restates it to 305 us, with `CTRL_LOOP_TX_MS` 35, by the rule (#897 issuecomment-6928240632). #898 lands before this sync.
   - Neither constant changes here, and the sync regrades on #898's merge.
2. **The 8x8/1if `STATED` lines.** They remain: the point is held to 1x1/1if's stated costs, which is #914's scope.

Found, not fixed (as in round 2):
- twin and twin-plants fail identically on `70f4056f` (#929);
- srptx fails as at `70f4056f` (#916);
- #840's 1000BASE-T-only advertisement is not on the split (#919).

Receipts, the handoff and the PR body are in the lane's round-3 output.
