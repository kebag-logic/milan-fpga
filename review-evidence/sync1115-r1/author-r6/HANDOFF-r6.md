# HANDOFF r6: [A787] sync dev 6b66f66d into dev-soft-core, round 6 (#665)

Status: REVIEW READY posted on #665 (issuecomment-6945152485), at head `9aa55d3b`. Rounds 4 and 5 were published at `e2be92b0`
(REVIEW READY #665 issuecomment-6942387001). Round 6 answers the second external review R854-2 (PR #934
issuecomment-6942847358, NEGATIVE at `e2be92b0`, one MAJOR, R854-2-F1). The internal R853-2 published POSITIVE at
`e2be92b0` (PR #934 issuecomment-6942941438) during this round. Round 6 changes artifacts that review covered, so its
coverage needs renewing at `9aa55d3b`. Nothing is pushed.

## 1. R854-2-F1 and its cause

An owned expiry's grading still took two judgements from other participants:
- **a run-out with no build after it** was absent or unresolved against the latest opportunity of every participant,
  so another participant's longer join timer turned a missing build into "unresolved" (`mrpdu_grade.py:214-216` at
  `e2be92b0`);
- **a build that sent frames** was judged by the participant of its first frame, so a late build that sent only
  another participant's MRPDU became "released". It also earned a periodic row on the other interface
  (`:239-242`). `begin()` and the non-LeaveAll rows timed from the commit's participants too.

## 2. The change, `1238a3ee` and `9aa55d3b`

Two commits on `e2be92b0`. They change harness grading, its self-test and two documents, and nothing else: no
firmware, RTL, testbench, build input or bound. `9aa55d3b` adds the four new mutants to the README's table.

Every owned MRP timer run-out is judged on its owner alone, the participant the testbench recorded at the expiry, and
on the owner's first transmit opportunity as `opportunity()` derives it from the posted TICKs (`mrpdu_grade.py`):
- **the missing-build deadline** (`horizon`): absent in a log that runs on past 49 ms after the owner's opportunity,
  unresolved where it ends first. Another participant's running join timer never defers it;
- **the frames that answer it** (`served`): only the owner's, a commit carrying the owner's MRPDU. It is released or
  late on the owner's first frame, against the owner's opportunity. A build that sends none of the owner's frames,
  nothing or only another participant's, is judged as a build that sends nothing: empty within 49 ms, late past it
  (`anchor`);
- **the row's start** (`begin`, `start_of`): the owner's opportunity, though the commit carries another participant's
  MRPDU whose opportunity came earlier. A row is timed on the owner's frames alone.
- `resolve` takes the build search from `window`, unchanged: the builds after the run-out, owed-frame retries
  included. An unowned run-out keeps every participant's frames there, so the failing log still shows them.
- A late or absent run-out is now named with its owner and the owner's opportunity (`run.run_out_miss`, `join_grade.held`):
  "the periodic timer's run-out at 1300.001 ms (if0 MSRP): its owner's first frame, or first build, 130.979 ms after
  the owner's transmit opportunity at 1300.001 ms, past THE TRANSMIT's 49 ms (late)".
- Unchanged: legitimate empty builds, owed-frame retries, genuinely short logs (unresolved), the owner's own running
  join timer, the LeaveAll grading, the unowned rule and the 49 ms bound.

**The controls** (`selftest_leaveall.foreign_checks`), each for both applications on both interfaces, the other
participant being the other application on the other interface:
- `a run-out with no build after it is absent past THE TRANSMIT's bound after its owner's first transmit opportunity,
  though another participant's join timer runs on, for either application on either interface; a log that ends first
  leaves it unresolved`;
- `a build that sends only another participant's MRPDU answers nothing for a run-out: late past the bound after its
  owner's opportunity, empty within it, no row for either interface, for either application on either interface; the
  owner's own MRPDU on time is released and times the owner's row`;
- `a timer's row starts at its owner's first transmit opportunity, for either application on either interface, though
  its commit carries another participant's MRPDU whose opportunity came earlier` (10.0 ms, where the earlier rule gave
  140 ms).

**A mutant per residual association**, each caught by its control by name:
- `transmit: a run-out with no build after it held to the latest of every participant's opportunity (earlier rule)`;
- `transmit: a build's first frame answering a run-out whichever participant's, timed from that participant's
  opportunity (earlier rule)`;
- `transmit: another participant's MRPDU credited to a run-out, timed from its owner`;
- `transmit: a timer's row started at the earliest opportunity of its commit's participants (earlier rule)`.

Two existing self-test fixtures follow the rule:
- `selftest_notice`'s timer row sends an MSRP MRPDU, its owner's, where it sent a frame of neither application;
- two expected findings carry the owner.

**The docs.** The harness README covers the run-out bullet, the row's start, "What this proves" and the mutant table,
now 23 transmit and LeaveAll rows. For every MRP timer's run-out, the grader proves that the testbench recorded its
owner at the expiry. It then proves one of three things against that owner's first opportunity:
- where its builds send the owner's frames, the first is committed within 49 ms of it;
- where they send none of the owner's, the first build runs within 49 ms of it;
- where no build follows, the log ends within 49 ms of it (unresolved), or the run fails (absent).

FR_NFR.md 3.4.1 states the same.

## 3. Verification

- **The reviewer's probe** (`probe_missing_build.py`, unchanged) **exits 0** at `9aa55d3b`.
  - All eight hidden cases fail by the actual owner at its original 1,300.001 ms opportunity: four absent and four late,
    for MSRP and MVRP on interfaces 0 and 1.
  - Its four short-log controls stay unresolved; its absent and empty-late controls hold.
- **The reviewer's other scripts:** `probe_ownership.py`, 60 controls, 0 failures; `check_focused_mutants.py`, all 15
  focused mutations caught, the eight original controls included.
- **Earlier probes:**
  - R853-1's, unchanged and owned: B fails on if0 MSRP, C0 and C late;
  - R854-1's owned overlap: fails on MSRP at 1,180 ms;
  - round 4's 24-case owner matrix: 0 failures.
- **Harness self-test** on a clean clone of `9aa55d3b`: rc 0, 0 failures, 882 checks pass, all 265 mutants caught, none
  escaped. Each new mutant is caught by its control (`receipts/budget/probe/per-check-at-9aa55d3b.txt`). All 23
  transmit and LeaveAll rows of the README table name the check that catches the mutant.
- **The published regrades, at `9aa55d3b`** (`r6_regrade.sh`; `receipts/budget/regrade-at-9aa55d3b.*`,
  `legs-at-9aa55d3b/`). Round 4's thirteen legs, every build attested against the head:
  - every leg's `table.md` is byte-identical to round 5b's, and each rc is round 5b's: `v1` 0, each 8x8/1if leg 1 on
    its #914 `STATED` lines alone, none naming a run-out;
  - every MRPDU row, join interval and LeaveAll outcome is the same. The eleven phases' 44 owned LeaveAlls are sent,
    and the worst rows are unchanged: leaveall 1.64360, periodic 2.96879 and join 1.86217 ms, against 20 ms;
  - **what moves:** 73 of the 1,871 MRP run-outs, 46 join and 27 periodic, from released to empty. Every one had been
    credited to another participant's frame, and in none did the owner send a frame of its own in those builds. None
    becomes late or absent, and no run-out fails. Totals: 1,029 released and 842 empty, all owned. Each move is
    listed with its timer, time, owner and the participant that answered it before (`regrade-at-9aa55d3b.json`).
    Round 5b's rules are reproduced on the same log by restoring the three earlier-rule plants;
  - #901's valid-destinations leg at 1x1/1if: rc 0. The 49 ms bound is unchanged.
- **Docs jobs** on fresh clean clones of `9aa55d3b`: **63 steps rc 0, 34 not run with a reason, 0 bad** (`verify_wf.py` rc 0).
- **Quick local checks** before each commit: `check_py_idiom.py`, `docs_inventory.py --check`, `docs_check.py`,
  `check_doc_paths.py`, pass.

The other gates carry from earlier rounds at their recorded source heads, as the PR body lists them. Round 6 changes
only the harness's grading Python, its self-test and two documents.

## 4. Open items

- **#898** is now merged (`cb96336d`, as R854-2 notes). Its paced SET_CONFIGURATION and `CTRL_LOOP_TX_MS` restatement
  reaches this sync at composition, which is the manager's. This head does not include it and neither constant
  changes here. `record_classes.py` was not re-run this round: its refusal of that one 1x1/1if record is round 3's,
  and nothing it reads has changed since.
- **#914's scope:** the 8x8/1if `STATED` lines.
- **Reported, not fixed:** twin and twin-plants (#929); srptx (#916); #840's 1000BASE-T-only advertisement on the
  split (#919); the 8x8/1if split's thin margin, which meets #818 (#927).
- **Observed, not in scope:** the harness README's mutant table has 54 rows outside THE TRANSMIT's and the LeaveAll's
  whose check column does not match the check the self-test now names, and 34 of the 265 mutants have no row. That
  predates this sync.
