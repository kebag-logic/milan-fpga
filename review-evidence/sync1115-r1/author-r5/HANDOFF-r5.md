# HANDOFF r5: [A787] sync dev 6b66f66d into dev-soft-core, rounds 5 and 5b (#665)

Status: REVIEW READY covering rounds 4 and 5 posted on #665 (issuecomment-6942387001), at head `e2be92b0`. Earlier: round 4's
REVIEW READY #665 issuecomment-6936610025 (head `c10c549e`, on PR #934), and round 5's first REVIEW READY
issuecomment-6940142843 (head `ccc98b11`), which round 5b supersedes. Nothing is pushed; the manager publishes rounds
4 and 5 together.

- **Round 5 (`ccc98b11`)** answers the internal review R853-1 (PR #934 issuecomment-6938623769, NEGATIVE at
  `6ceed753`, two MINOR findings in round 3's grading):
  - F1 is R854-1's finding, which round 4 fixes; it is shown here with the reviewer's own probe;
  - F2 is fixed.
- **Round 5b (`e2be92b0`)** applies the manager's ruling on round 5's one open question: an MRP timer's expiry with
  no recorded owner fails the run by name, as an unowned LeaveAll already does, with no lenient fallback.

## 1. F1: the reviewer's case B at round 4's grader

`leaveall_attribution_probe.py` is R853-1's probe, copied unchanged (its sha256 is in the receipt). Its case B: MSRP's
LeaveAll timer runs out at 1,050 ms. At its first opportunity, 1,180/1,181 ms, MSRP sends an MRPDU without the
LeaveAll, and its LeaveAll follows at 1,371 ms. MVRP's LeaveAll timer runs out at 1,185 ms, and MVRP sends its
LeaveAll at 1,191 ms.

| Probe form | `c10c549e` (round 4) | `ccc98b11` (round 5) | `e2be92b0` (round 5b) |
|---|---|---|---|
| as written: its `ENTRY` lines name no owner, round 3's log format | B fails: both LeaveAll expiries `unowned` | the same | every expiry of A, B, C0 and C `unowned`, failing |
| owned: each timer callback's `ENTRY` names its owner, as the head's testbench prints it (`r853_probe_owned.py`) | **B fails on if0 MSRP**: `skipped` at its 1,180 ms opportunity, its LeaveAll 191 ms after it; MVRP's `sent` | the same | the same |

Receipts: `receipts/budget/probe/r853-probe-{as-written,owned}-at-{c10c549e,ccc98b11,e2be92b0}.txt`.

Round 4 already had a two-participant arm and mutant:
- the arm is the overlap control (`two participants' timers overlapping`);
- the mutant is `leaveall: an expiry bound to the participant whose LeaveAll comes first after it, not its recorded
  owner (earlier rule)`, which that arm catches.

Round 5 adds case B itself as an arm: `a LeaveAll timer's run-out inside another participant's join interval, after
its skipped opportunity, whose LeaveAll goes first`. It names MSRP's run-out "(LeaveAll past its first transmit
opportunity)" at 1,180 ms, 191 ms. The earlier-rule mutant fails both arms
(`receipts/budget/probe/per-check-at-e2be92b0.txt`).

## 2. F2 and the ruling: the change, `ccc98b11` and `e2be92b0`

Two commits on `c10c549e`. They change harness grading, its self-test and two documents, and nothing else: no
firmware, RTL, testbench, build input or bound.

**`ccc98b11`, F2.** A run-out whose first build sends nothing was late only past 49 ms after the last `on_join_timer`
callback between them, of any participant. Another participant's join callback could therefore restart the count, and
the reviewer's case C passed a build 60 ms after its run-out.
- **The anchor** (`mrpdu_grade.py`, `anchor`, `recorded_owner`): that build is late past THE TRANSMIT's 49 ms after
  the first transmit opportunity of the timer's owner. The owner is the participant the testbench recorded at the
  expiry (`grade.Log.owners`, round 4's record, for all three MRP timer callbacks). The opportunity is derived from
  the posted TICKs exactly as `opportunity()` derives it.
  - It is never a join timer's callback, nor another participant's opportunity.
  - A frame's lateness is unchanged: the frame's own participants' earliest opportunity.
- **The finding** (`join_grade.held`): a late build that sends nothing is named from that anchor.
- **The arm** (`selftest_leaveall.anchor_checks`), checked by name. Its cases:
  - the reviewer's C0: late at 59.979 ms;
  - the reviewer's C, with another participant's join callback at 1,330 ms between: late at 59.979 ms;
  - another participant's running join timer: late at 159.979 ms;
  - the owner's own running join timer: it holds.
- **Its mutant**: `transmit: a build that sends nothing late only past the last join callback before it, any
  participant's (earlier rule)`, caught by that arm.

**`e2be92b0`, the ruling.** In round 5, with no owner recorded, the anchor was the latest of the log's participants'
opportunities. In an owner-less log that could lie up to a JoinTime after the run-out.
- **The rule** (`mrpdu_grade.resolve`): every MRP timer's run-out, a join, periodic or LeaveAll timer's, whose owner
  the testbench did not record at the expiry, or recorded unresolved, is `unowned`, whatever its builds sent.
  - `unowned` is in `FAILING`: the run-out prints `STATED`, named "(owner unresolved)" (`run.run_out_miss`), and
    fails the run, as an unowned LeaveAll does.
  - No other participant's opportunity stands in. The fallback is gone from `anchor`.
  - An unowned run-out's frames are still its builds' (`released`), so its rows and join intervals stay visible in
    the failing log.
- **The arm** (`selftest_leaveall.unowned_checks`), checked by name: `an MRP timer's run-out with no owner recorded
  at its expiry, or its owner recorded unresolved, is unowned, named and fails the run whatever its builds sent: no
  other participant's opportunity stands in, and its frames are still its builds'`. Its cases:
  - no owner recorded, an empty build 59.979 ms after the run-out;
  - no owner recorded while another participant's join timer still runs, where the old fallback held the build;
  - the owner recorded unresolved, with its build's MRPDU on time: unowned, and its join interval still graded.
  - The run fails on the finding.
- **Its mutants**, each caught by that arm:
  - `transmit: an expiry with no owner recorded given the participant whose opportunity is latest (the fallback
    restored)`;
  - `transmit: an unowned run-out not failing the run`.
  - They replace round 5's `transmit: a build that sends nothing timed from the latest participant's opportunity, its
    timer's recorded owner ignored`, which under this ruling only made every expiry unowned.
- **The self-test's synthetic logs** carry their timers' owners as the testbench writes them: `selftest_polls`'s join
  intervals and `selftest_notice`'s timer rows.
- **The docs.** The harness README covers:
  - the run-out bullet and the owner's definition;
  - "What this proves": for every MRP timer's run-out, the testbench recorded its owner at the expiry, its first frame
    is committed within 49 ms of that frame's participant's first opportunity, and where its first build sends
    nothing, that build runs within 49 ms of the owner's;
  - the mutant table's 19 transmit and LeaveAll rows.

  FR_NFR.md 3.4.1 states the same and that an expiry with no recorded owner fails the run. The bound is unchanged.

## 3. The regrade at `e2be92b0`

Round 4's thirteen re-simulated legs were graded again with `run.py --reuse-build --regrade` (`r5b_regrade.sh`, into
new result directories with their logs hard-linked, so round 4's results are untouched). Every build attests against
the head's inputs:
- the seed clones carry the head's harness byte for byte (`receipts/budget/seed-harness-at-e2be92b0.txt`);
- the product and valid-destinations legs regrade from their building checkout, moved to `e2be92b0`. A build records
  its inputs under its own checkout, and a regrade from another clone is refused as "inputs never recorded".

Results (`receipts/budget/regrade-at-e2be92b0.md`, `.json`; each leg's table, log and rc under
`receipts/budget/legs-at-e2be92b0/`):
- **Every leg's `table.md` is byte-identical to round 4's.** Every group's MRPDU rows, MRP run-outs by outcome,
  failing run-outs, LeaveAlls by outcome and owner, and every probe value are the same. Each rc is round 4's: `v1` 0,
  each 8x8/1if leg 1 on its #914 `STATED` lines alone, and none names an unowned run-out.
- **The 26 traces still pass the owner rule:** 1,871 MRP run-outs (1,102 released, 769 builds that send nothing), each
  with its owner recorded; none unowned.
- **The eleven LeaveAll phases at 8x8/1if:** 44 LeaveAlls, each `sent` at its recorded owner's first opportunity; none
  skipped, late, absent, unresolved or unowned. The worst rows are unchanged from round 4: leaveall 1.64360 ms (seed
  12102, save-starved), periodic 2.96879 ms (seed 13602, save-starved), join 1.86217 ms (seed 10592, save-held),
  against 20 ms. The 49 ms bound is unchanged (`LATE_MS` 49, from `ctrl_loop.h`).
- **#901's valid-destinations leg at 1x1/1if:** rc 0, both LeaveAlls sent. The 8x8/1if valid-destinations leg: both
  sent, rc 1 on its #914 lines.
- **Builds that send nothing** (769): against round 3's rule, the owner's anchor moves 334 of them, each at most 5 us
  earlier, none later, and changes no outcome. The latest runs 0.832 ms after its owner's opportunity.

**Round 2's other legs** (`receipts/budget/oldlegs-unowned-at-e2be92b0.json`, `.txt`) are an analysis of the logs,
not a regrade: their builds predate round 4's testbench, and the head refuses to reuse them.
- Their 215 group logs carry no owner record.
- **213 of them now fail, as expected:** all 4,122 of their MRP run-outs are `unowned` and named.
- The other 2, the fixture groups, have no MRP run-out.

Round 5's regrade at `ccc98b11` (`receipts/budget/regrade-at-ccc98b11.*`, `legs/`) gave the same tables. Its
old-legs analysis (`oldlegs-empty-builds.*`) measured the fallback that round 5b removes.

## 4. Gates

| Gate | Command | Result | Receipt |
|---|---|---|---|
| harness self-test and its mutants | `run.py --self-test`, clean clone of `e2be92b0` | rc 0, 0 failures, 879 checks pass, all 261 mutants caught, the round-5b ones by the unowned arm and the anchor mutant by the anchor arm | `receipts/budget/selftest-at-e2be92b0.txt` |
| per-check of the LeaveAll and transmit mutants | `per_check.py`, clean clone | each new mutant fails its arm by name; the earlier-rule owner mutant fails both two-participant arms | `receipts/budget/probe/per-check-at-e2be92b0.txt` |
| the reviewers' probes | unchanged and owned, at `c10c549e`, `ccc98b11` and `e2be92b0` | R853-1's B fails on if0 MSRP (owned); C0 and C late (owned) or unowned (as written) at the head. R854-1's overlap fails on MSRP (owned); as written, unowned | `receipts/budget/probe/` |
| docs jobs | `run_wf.py` per job, fresh clean clone each; `verify_wf.py e2be92b0 runs/N docs.yml` | **63 steps rc 0, 34 not run with a reason, 0 bad** | `receipts/workflows/` |
| the regrade | `r5b_regrade.sh`, 13 legs | every table byte-identical to round 4's; rc as round 4; no unowned run-out | `receipts/budget/regrade-at-e2be92b0.*`, `receipts/budget/legs-at-e2be92b0/` |
| quick local checks | `check_py_idiom.py`, `docs_inventory.py --check`, `docs_check.py`, `check_doc_paths.py` (the lane, before each commit) | pass | |

The other gates carry from earlier rounds at their recorded source heads, as round 4's PR body lists them: the four
workflows at `9715a30a`, the sweep, `split` and `split-mutants`, the images and the routes against #818. Rounds 5 and
5b change only the harness's grading Python, its self-test and two documents. Round 5's own gates at `ccc98b11`
(self-test 878 checks and 260 mutants; docs 63 rc 0, 34 not run, 0 bad) are kept in `receipts/` beside these.

## 5. Open items

- **Unchanged, for the record:** a run-out with no build after it is `absent` or `unresolved` against the latest of
  every participant's opportunity, round 3's horizon. With its owner recorded it could be the owner's. It only decides
  absent against unresolved for a log that ends within a JoinTime of such a run-out. Not changed here.
- **Q2 (#898):** the 305 us paced SET_CONFIGURATION and `CTRL_LOOP_TX_MS` 35; `record_classes.py` refuses that one
  1x1/1if record until #898 lands. Neither constant changes here.
- **#914's scope:** the 8x8/1if `STATED` lines.
- **Reported, not fixed:** twin and twin-plants (#929); srptx (#916); #840's 1000BASE-T-only advertisement on the
  split (#919); the 8x8/1if split's thin margin, which meets #818 (#927).
- **Observed, not in scope:** the harness README's mutant table has 54 rows outside THE TRANSMIT's and the LeaveAll's
  whose check column does not match the check the self-test now names, mostly abbreviated, some stale, and 34 of the
  261 mutants have no row. That predates this sync. The 19 transmit and LeaveAll rows match exactly.
- **Process:**
  - The host's 07:25 shutdown cut round 5b's regrade, self-test and docs units. Each sub-unit without an rc was
    treated as cut, its half-written output removed and the sub-unit rerun. That was two regrade legs' logs and
    `docs-gates-0`'s steps.
  - `bgunit.sh`'s fallback now reads the session pool from `cpu_ranges.py`, 64-95 on the 96-CPU host.
  - Every booked range was taken, so the units ran on the session pool at reduced weight.
