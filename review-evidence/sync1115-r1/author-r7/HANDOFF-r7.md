# HANDOFF r7: [A787] sync dev 6b66f66d into dev-soft-core, round 7 (#665)

Status: REVIEW READY posted on #665 (issuecomment-6950748861), at head `544fd72c`. Round 6 was published at `9aa55d3b`: R854-3
POSITIVE (PR #934 issuecomment-6945503288); R853-3 NEGATIVE on one MAJOR, R853-3-F1 (issuecomment-6945831260).
Round 7 fixes R853-3-F1 by the preferred route: the trace records each build's participant. Under the owner's batch
rule this is the last delta before #934 freezes. Nothing is pushed.

## 1. R853-3-F1 and its cause

An owned run-out whose owner sent nothing in the first build after it was still settled by that build, whichever
participant's it was (`mrpdu_grade.py:228-234` at `9aa55d3b`). So another participant's build within 49 ms graded it
`empty`, and the owner's own MRPDU 131 ms later got no finding and no row: R853-3's case F, for all four owners, and
FE and JF. The trace named no participant for a build, so the grader could not tell whose a build was.

## 2. The change, `38d89bb0` and `544fd72c`

Two commits on `9aa55d3b`. `544fd72c` lists the four new mutants in the README's table. Harness and documents only:
no firmware, RTL, configuration, pin or bound changes.

**The trace records each build's participant at the build itself** (`sim_main.cpp`'s `builder_of`, `observers.py`'s
`build_pc` hook), as it records a timer callback's owner:
- `srp_mbx.c`'s `build_mrpdu(m, i, slot)` builds exactly one participant's MRPDU: slot 2n is interface n's MSRP,
  2n + 1 its MVRP (`participant`, `srp_mbx.c:1091-1099`);
- the testbench reads the slot from `a2` at the entry and prints `ENTRY <cycle> build_mrpdu if<n> MSRP|MVRP`, or
  `unresolved` with the slot;
- the compiled `build_mrpdu` keeps that calling convention in both measurement images: `a2` is the slot at both call
  sites, and its low bit selects MVRP at the entry.

**An owned run-out is settled only by a build that can be its owner's** (`mrpdu_grade.settle`, `candidate`, `builder`,
`run_from`). The builds after the run-out are taken in turn:
- **never settles it:** a build recorded as another participant's, or any build before the owner's first transmit
  opportunity;
- **the owner's recorded build:** settles it on the owner's frames of its run (`served`), released, or late past
  49 ms. With none of the owner's frames, it is the owner's own build that sends nothing: empty within 49 ms, late
  past it (`anchor`);
- **a build with no participant recorded:** settles it only on the owner's frames. It is never taken for the owner's
  empty build;
- **no settling build:** if none settles it within 49 ms of the owner's opportunity, the first build past that bound
  makes it late, named "no frame or build of its owner's within THE TRANSMIT's 49 ms of the owner's transmit
  opportunity, a build N ms after it". With no build after it at all, the owner's horizon decides absent or
  unresolved, unchanged;
- **unchanged:** legitimate empty builds (the owner's own), owed-frame retries (the build's run), short logs
  (unresolved), the owner's own running join timer (the opportunity), LeaveAll grading, the unowned rule and the 49 ms
  bound (IEEE 802.1Q-2018 10.7.4.1).

**The controls** (`selftest_leaveall.builder_checks`), each for both applications on both interfaces:
- `another participant's build never settles a run-out ...`: R853-3's F (late, 131 ms, named, with its row) and JF
  (released);
- `a build whose participant the testbench did not record, sending nothing, is never taken for the owner's ...`:
  R853-3's FE (late);
- `the owner's own build before its transmit opportunity settles nothing ...`: its MRPDU at the opportunity is
  released.
- `foreign_checks` gains a `shared` case: the owner's own empty build, with another participant's MRPDU in its run,
  is empty with no row. Its `within` case, a timely build of another participant only, is now `absent`: the owner
  never built.

**Four mutants**, one per new association, each caught by its control by name:
- `transmit: a build's recorded participant ignored, every build from the owner's opportunity taken for the owner's`;
- `transmit: a run-out settled by the first build after it, whichever participant's (earlier rule)`, round 6's rule;
- `transmit: a build with no participant recorded that sends nothing taken for the owner's`;
- `transmit: the owner's own build before its transmit opportunity settling its run-out`.

**The self-test's synthetic logs** record each build's participant as the testbench does:
- builds of one millisecond take successive cycles, MSRP before MVRP;
- `selftest_polls`'s join-interval fixtures put each join run-out at its owner's opportunity; their edge cases arm the
  join timer from an earlier build, as consistent timing requires. Its periodic-timer control again catches
  `joins: a periodic or LeaveAll timer's MRPDU taken for a join's`, which the inconsistent fixture let escape under
  the owner rule.

**The docs:** the harness README (the trace's build record, the run-out bullets, "What this proves", the mutant table
of 27 transmit and LeaveAll rows) and FR_NFR.md 3.4.1 state exactly what is proven. R853-3-RES-1 is fixed (README:
"or a late, absent or unowned run-out, prints `STATED`"). SUG-1 (an optional note on two re-caught mutants) is not
taken.

## 3. Verification

- **R853-3's `probe_owner_build.py`**, unchanged, at `38d89bb0`:
  - **case F** is late for all four owners: "its owner's first frame or build 130.999 ms after the owner's transmit
    opportunity at 1300.001 ms, past THE TRANSMIT's 49 ms (late)", with the 131.0 ms row;
  - **FE** is late likewise; **JF** is released, row 1.0 ms;
  - controls O (late) and J (released) keep their results.
- **R854-2's scripts:** `probe_missing_build.py` rc 0, all eight cases failing by the owner; `probe_ownership.py`, 60
  controls, 0 failures; `check_focused_mutants.py`, 15 of 15 caught.
- **Earlier probes:** R853-1's (B fails on if0 MSRP; C0 and C late); R854-1's owned overlap (fails on MSRP at
  1,180 ms); round 4's owner matrix, 24 controls, 0 failures.
- **Harness self-test** on a clean clone of `544fd72c`: rc 0, 0 failures, 885 checks pass, all 269 mutants caught, none escaped; all 27 transmit and LeaveAll rows of the README table name the check that catches the mutant (`receipts/budget/selftest-at-544fd72c.txt`).
- **Docs jobs** on fresh clean clones of `544fd72c`: **63 steps rc 0, 34 not run with a reason, 0 bad** (`verify_wf.py` rc 0).
- **Image identity** (`receipts/budget/image-identity-at-38d89bb0.json`, `r7_identity.py`): every round-7 measurement
  build against round 4's build of the same leg, all 13 legs.
  - **Every firmware ELF is byte-identical.**
  - Every other file of `image/`, `gateware/`, `runtime/` and `split-soc/` is identical, or differs only in what a
    rebuild stamps: build paths and LiteX's generation dates (1,554 files), LiteX's generated comments with the
    Verilog identical (5), the order of the same constraints (11), archive member timestamps with members identical
    (78), and digests recorded of such files (104). The builders' own run logs (104) are listed, not compared.
  - None is unexplained. Only the testbench's configuration (`budget_config.hpp`: the new `build_pc`) and native model
    differ.
  - No product source changes (`git diff 9aa55d3b 544fd72c`: harness and documents only), so the product images are
    unchanged.
- **The build record** (`r7_buildcheck.py`, then `r7_compare.py`, all 2,258 builds in the 26 new traces carry their participant, 1,129 MSRP and 1,129 MVRP, none unresolved or unrecorded; all 1,061 that commit an MRPDU of their own name that MRPDU's participant, none disagreeing. Each trace equals round 4's, all 39,950,921 lines, once the build's participant is taken off.).
- **Re-simulation and regrade of round 4's thirteen legs** (`r7_legs.sh`, new builds at `38d89bb0`; `r7_regrade.sh`
  at `544fd72c`): every build attested against the head.
  - Each rc is round 6's: `v1` 0; each 8x8/1if leg 1 on its #914 `STATED` lines alone, none naming a run-out.
  - **Every `table.md` is byte-identical to round 6's.** Every MRPDU row, join interval and LeaveAll is the same: the
    eleven phases' 44 owned LeaveAlls (48 with both valid-destinations legs) are sent, and the worst rows are
    unchanged, leaveall 1.64360, periodic 2.96879 and join 1.86217 ms, against 20 ms. #901's valid-destinations leg at
    1x1/1if: rc 0. The 49 ms bound is unchanged.
  - **What moves:** 27 of the 1,871 MRP run-outs, all periodic (15 if0 MSRP, 12 if0 MVRP), from `empty` to
    `released`.
    - Round 6's rule settled each on an if0 MSRP build at least 9.5 ms before the owner's opportunity: the owner's
      own early build for the 15, MSRP's build for the 12.
    - Round 7 skips those builds. Each is settled by the owner's own build at its opportunity, sending the owner's
      MRPDU within 1.661 ms of it; their rows are within the unchanged worst rows.
    - Each move is listed with its owner and the build that settled it under each rule (`regrade-at-544fd72c.json`).
  - **No outcome moves to `empty`, `late`, `absent` or `unowned`, and no run-out fails.** Of the 815 run-outs graded
    `empty`, each is settled by the owner's own recorded build, at most 1.955 ms after the owner's opportunity.
  - Totals: 1,056 released and 815 empty, all owned..

## 4. Open items

- **#898** is merged (`cb96336d`) and reaches this sync at composition, the manager's. This head does not include it.
- **#914's scope:** the 8x8/1if `STATED` lines.
- **Reported, not fixed:** twin and twin-plants (#929); srptx (#916); #840's 1000BASE-T-only advertisement on the
  split (#919); the 8x8/1if split's thin margin, which meets #818 (#927).
- **Observed, not in scope:** the harness README's mutant table has rows outside THE TRANSMIT's and the LeaveAll's
  whose check column does not match the check the self-test now names, as reported in rounds 5 and 6. That predates
  this sync.
