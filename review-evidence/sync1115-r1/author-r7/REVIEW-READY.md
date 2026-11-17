[A787] REVIEW READY

Commit: 544fd72cefbd27379ae756c6ce02ae8b7ba15f2c (`sync-dev-6b66f66d-into-dev-soft-core`, parent `38d89bb0`, on `9aa55d3b`; local, nothing pushed; the manager pushes)

Changed: round 7 fixes R853-3-F1 (PR #934 issuecomment-6945831260, NEGATIVE at `9aa55d3b`) by the preferred route, with no ruling-dependent limit. Two commits; the harness (testbench and grading), its self-test and two documents. No firmware, product RTL, configuration, pin or bound changes. Under the owner's batch rule this is the last delta before #934 freezes.
- **The trace records each MRPDU build's participant at the build itself.** `srp_mbx.c`'s `build_mrpdu(m, i, slot)` builds exactly one participant's MRPDU (slot 2n interface n's MSRP, 2n + 1 its MVRP). The testbench reads the slot from `a2` at the entry, as it reads a timer callback's owner (`sim_main.cpp`'s `builder_of`, `observers.py`'s `build_pc`): `ENTRY <cycle> build_mrpdu if0 MVRP`. The compiled `build_mrpdu` keeps that convention in both measurement images.
- **An owned run-out is settled only by a build that can be its owner's** (`mrpdu_grade.settle`, `candidate`, `builder`), its builds taken in turn:
  - a build recorded as another participant's, or any build before the owner's opportunity, never settles it;
  - the owner's recorded build settles it on the owner's frames (released or late) or as the owner's own build that sends nothing (empty or late);
  - a build with no participant recorded settles it only on the owner's frames, and is never taken for the owner's empty build;
  - with none settling within 49 ms, the first build past the bound makes it late; with no build at all, the owner's horizon decides absent or unresolved.
- **Unchanged:** legitimate empty builds, owed-frame retries, short logs, the owner's own running join timer, LeaveAll grading, the unowned rule, 49 ms (IEEE 802.1Q-2018 10.7.4.1).
- **Three standing controls** (`selftest_leaveall.builder_checks`), each for both applications on both interfaces: R853-3's F and JF; FE; and the owner's own build before its opportunity. `foreign_checks` gains the owner's own empty build with another participant's MRPDU in its run. The synthetic logs record each build's participant, and the join fixtures put each run-out at its owner's opportunity.
- **Four mutants**, each caught by its control by name: build participant ignored; first build of any participant (round 6's rule); an unattributed empty build taken for the owner's; a build before the opportunity settling it.
- **Docs:** the harness README and FR_NFR.md 3.4.1 state exactly what is proven; R853-3-RES-1 is fixed ("a late, absent or unowned run-out, prints `STATED`").

Validation:
- **R853-3's `probe_owner_build.py`**, unchanged:
  - case F is **late for all four owners**: "its owner's first frame or build 130.999 ms after the owner's transmit opportunity at 1300.001 ms, past THE TRANSMIT's 49 ms (late)", with its 131.0 ms row;
  - FE is late; JF is released (row 1.0 ms); O and J keep their results.
- **R854-2's scripts:** `probe_missing_build.py` rc 0; `probe_ownership.py`, 60 controls, 0 failures; `check_focused_mutants.py`, 15 of 15 caught.
- **Earlier probes:** R853-1's and R854-1's owned probes fail on MSRP; round 4's owner matrix, 24 controls, 0 failures.
- **Harness self-test** on a clean clone of `544fd72c`: rc 0, 0 failures, 885 checks pass, all 269 mutants caught.
- **Docs jobs** on fresh clean clones of `544fd72c`: 63 steps rc 0, 34 not run with a reason, 0 bad (`verify_wf.py` rc 0).
- **Image identity**, every round-7 measurement build against round 4's of the same leg, all 13:
  - every firmware ELF is byte-identical;
  - every other firmware, SoC, ROM, runtime and flash-map file is identical, or differs only in rebuild stamps (paths, LiteX dates and comment order, the order of symmetric constraints, archive timestamps with identical members, recorded digests of those). None is unexplained;
  - only the testbench's configuration and native model differ;
  - no product source changes, so the product images are unchanged.
- **Round 4's thirteen legs, re-simulated with the build record at `38d89bb0` and regraded at `544fd72c`:**
  - every trace equals round 4's, line for line, once the build's participant is taken off; all 2,258 builds name their participant, and all 1,061 frame-bearing builds name their own MRPDU's;
  - every `table.md` is byte-identical to round 6's, and each rc is round 6's (`v1` 0; each 8x8/1if leg 1 on its #914 `STATED` lines alone);
  - every MRPDU row, join interval and LeaveAll is the same: 44 owned LeaveAlls sent in the eleven phases; worst rows leaveall 1.64360, periodic 2.96879, join 1.86217 ms, against 20 ms; the 49 ms bound unchanged;
  - **27 of the 1,871 MRP run-outs move, all periodic, from empty to released.** Round 6 settled each on an if0 MSRP build at least 9.5 ms before the owner's opportunity (the owner's own for 15, MSRP's for 12 MVRP-owned). Round 7 skips those, and the owner's own build at its opportunity sends its MRPDU within 1.661 ms. Each move is listed with its cause;
  - no run-out fails. Each of the 815 run-outs graded empty is the owner's own recorded build, within 1.955 ms of its opportunity.

Acceptance criteria:
- met: R853-3-F1 fixed with the build's participant recorded at the build; case F late for each owner at the 1,300.001 ms opportunity, FE and JF likewise; R854-2's and R853-3's other probes pass; a mutant per new association, caught by its control by name; the self-test and docs jobs on a clean clone; the regrade of round 4's 13 legs, every move listed with its cause; the measurement images differing only by the instrumentation; README and FR_NFR 3.4.1 exact;
- pending: #898 (merged at `cb96336d`) reaches this sync at composition, the manager's; this head does not include it.

Open risks/questions:
1. **The 8x8/1if `STATED` lines** remain #914's. Every 8x8 leg exits 1 on them alone.

Found, not fixed (as before): twin and twin-plants (#929); srptx (#916); #840's 1000BASE-T-only advertisement on the split (#919).

Receipts, the handoff and the PR body are in the lane's round-7 output.
