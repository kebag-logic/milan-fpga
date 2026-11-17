[A787] REVIEW READY

Commit: e2be92b0e0f9a8f0529dea252f23ed44a21e050a (`sync-dev-6b66f66d-into-dev-soft-core`; local, nothing pushed; the manager pushes)

This covers rounds 4 and 5, which the manager publishes together. It supersedes round 5's first REVIEW READY (issuecomment-6940142843, `ccc98b11`). Three commits on round 3's `6ceed753`; harness, its self-test and documents only. No firmware, product RTL, configuration, pin or bound changes.

Changed:
- **Round 4, `c10c549e` (R854-001, PR #934 issuecomment-6932841237):** the testbench records each MRP timer expiry's owner at the expiry, its interface and application. It reads the callback's argument from the CPU's register file, bound at the participant's creation. The grader binds each LeaveAll expiry to that owner for its opportunity, first MRPDU, LeaveAll, late or absent output and row. An unowned LeaveAll fails.
- **Round 5, `ccc98b11` (R853-1, PR #934 issuecomment-6938623769):**
  - F1 is R854-001; the reviewer's case B is added as a self-test arm;
  - F2: a build that sends nothing is late past 49 ms after its timer's owner's first transmit opportunity, derived from the posted TICKs, never from any participant's join callback (`mrpdu_grade.anchor`).
- **Round 5b, `e2be92b0` (the manager's ruling on round 5's open question):**
  - every MRP timer's run-out, join, periodic or LeaveAll, whose owner the testbench did not record at the expiry, or recorded unresolved, is `unowned` whatever its builds sent;
  - it is named "(owner unresolved)" and fails the run, as an unowned LeaveAll does;
  - no other participant's opportunity stands in: round 5's fallback is removed.
- **Docs:** the harness README and FR_NFR.md 3.4.1 state exactly what the grader proves. The README's mutant table carries the 19 transmit and LeaveAll rows as the self-test names their checks.

Validation (at `e2be92b0` unless stated):
- **R854-1's overlap**, with owners recorded: fails on if0 MSRP at its 1,180 ms opportunity, 191 ms; the clean and reordered overlaps pass. As written, without owners, every expiry is unowned and fails.
- **R853-1's probe**, copied unchanged:
  - case B fails on if0 MSRP, `skipped` at 1,180 ms, at `c10c549e`, `ccc98b11` and here, once its entries carry owners;
  - C0 and C fail as late (59.979 ms), where C passed at `c10c549e`;
  - as written, without owners, every case fails as unowned.
- **Harness self-test** on a clean clone: rc 0, 0 failures, 879 checks pass, all 261 mutants caught. Each new mutant is caught by its named arm:
  - the anchor from any join callback;
  - the fallback restored;
  - an unowned run-out not failing;
  - round 4's owner mutants, and the earlier-rule owner mutant on both two-participant arms.
- **Docs jobs** on fresh clean clones: every job, 63 steps rc 0, 34 not run with a reason, 0 bad (`verify_wf.py` rc 0).
- **Round 4's thirteen re-simulated legs, regraded** (`--reuse-build --regrade`, every build attested against the head):
  - every leg's table is byte-identical to round 4's, and each rc is round 4's;
  - the 26 traces' 1,871 MRP run-outs all have their owner recorded; none is unowned;
  - the eleven 8x8/1if LeaveAll phases: 44 owned LeaveAlls sent at their first opportunity; none skipped, late, absent, unresolved or unowned;
  - worst rows unchanged: leaveall 1.64360 ms, periodic 2.96879 ms, join 1.86217 ms, against 20 ms;
  - #901's valid-destinations leg at 1x1/1if: rc 0;
  - the 49 ms bound is unchanged.
- **Builds that send nothing** (769 in the traces): the owner's anchor moves 334 of them earlier by at most 5 us, none later, and changes no outcome.
- **Round 2's owner-less logs**, read but not regraded (the head refuses their builds): 213 of 215 now fail, as expected. All 4,122 of their run-outs are unowned; the other two logs have no MRP run-out.

Acceptance criteria:
- met: R854-001 fixed and held by arms and mutants; R853-1 F1 shown with case B, with an arm and a mutant; F2 fixed, with C0 and C late, an arm and a mutant; the ruling implemented, with an arm and a mutant (the fallback restored) caught by name; the eleven phases and the valid-destinations leg regraded with the bound unchanged; the docs state what the grader proves; the self-test and docs jobs at the head;
- **not met until #898:** `record_classes.py` refuses one 1x1/1if paced record (Q2).

Open risks/questions:
1. **The 8x8/1if `STATED` lines** remain #914's. Every 8x8 leg exits 1 on them alone.
2. **For the record, unchanged:** a run-out with no build after it is absent or unresolved against the latest of every participant's opportunity, round 3's horizon. With its owner recorded it could be the owner's. It only decides absent against unresolved for a log ending within a JoinTime of such a run-out.

Found, not fixed (as before): twin and twin-plants (#929); srptx (#916); #840's 1000BASE-T-only advertisement on the split (#919).

Receipts, the handoff and the PR body are in the lane's round-5 output.
