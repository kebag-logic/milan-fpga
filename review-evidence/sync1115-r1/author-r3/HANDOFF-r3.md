# HANDOFF r3: [A787] sync dev 6b66f66d into dev-soft-core, round 3 (#665)

Status: REVIEW READY posted on #665 (issuecomment-6932432594). Round 2: REVIEW READY #665 issuecomment-6930817036, handoff and receipts in round2/.
Rulings on it: #665 issuecomment-6930885185 (Q1 THE TRANSMIT's row from the transmit opportunity, with a LeaveAll
check; Q2 the paced record and `CTRL_LOOP_TX_MS` come with #898; Q3 the timing floor is #818's).

## 1. The change (Q1), `6ceed753`

One commit on `9715a30a`: harness grading only, plus its self-test and documentation; no firmware, RTL or bound moves.
- **The row's start** (`mrpdu_grade.py`):
  - `opportunity` (`:131`) gives the participant's first transmit opportunity at or after a timer's run-out. Where
    the join timer its last commit armed still runs, it is the `CTRL_LOOP_JOIN_CS`-th TICK after that commit's build;
    otherwise it is the run-out itself (IEEE 802.1Q-2018 10.7.4.1).
  - A participant is an interface and an MRP application, told by its MRPDU's EtherType (`participant`, `:73`).
  - `begin` (`:148`) starts each row at the deadline of that opportunity.
  - `resolve` (`:192`) holds the first frame to THE TRANSMIT's 49 ms after the opportunity. An empty build is held
    from the last join timer's run-out before it, and "absent" counts from every participant's opportunity.
  - The row's budget and THE TRANSMIT's bound are unchanged.
- **The check** (`leave_alls`, `:237`): every LeaveAll timer's run-out owes its participant's LeaveAll. That is the
  first MRPDU after the run-out whose VectorHeader declares one, read as lwSRP's `mrp_pdu.c` reads an MRPDU
  (`leave_all`, `:79`). It must be the participant's first MRPDU after the run-out and come within 49 ms of that
  opportunity.
  - Outcomes: `sent`, `skipped` (an MRPDU without it first: a transmit opportunity skipped), `late`, `absent`,
    `unresolved`.
  - `join_grade.held` counts them on the `JOINS` line. A skipped, late or absent LeaveAll is named by
    `run.leave_all_miss` (`run.py:186`): "(LeaveAll past its first transmit opportunity)", "(LeaveAll late)",
    "(LeaveAll absent)". It fails the run.
- **The planted defect and the self-test** (`selftest_leaveall.py`, from `selftest_polls.py`): synthetic held logs
  with a TICK every centisecond. The checks:
  - a LeaveAll whose join timer still runs is timed from that timer's run-out: 1 ms, where the run-out gives 131 ms;
  - a LeaveAll with its join timer idle is timed from its own TICK;
  - **the planted skip**: the participant sends an MRPDU without the LeaveAll at its first opportunity and the LeaveAll
    at the next. It is caught by name, and so is a late one;
  - another application's MRPDU skips nothing;
  - absent and unresolved;
  - the parser on MSRP (past its AttributeListLength and a Listener's FourPackedEvents) and MVRP;
  - a skipped LeaveAll fails a run.
- **Mutants** (`selftest_mutants.py`), each caught by a named check:
  - the row from the run-out (the earlier rule);
  - the join timer a centisecond short;
  - a skipped LeaveAll not failing;
  - a late LeaveAll not failing;
  - any MRPDU taken for the LeaveAll;
  - the applications not told apart;
  - the Listener's FourPackedEvents not skipped;
  - an absent LeaveAll taken for an unresolved one.
- **Documentation:** the harness README (the join section, the MRPDU row, the mutant table) and FR_NFR.md 3.4.1, both
  citing the ruling. FR_NFR's 49 ms was already derived from the transmit opportunity (240 ms less the armed join
  time and `T_egress`). The harness had been timing the row from the timer's own expiry.

## 2. The regrade (Q1)

Every log graded again, from its existing trace (`--reuse-build --regrade`), with the harness at `6ceed753`.
- **The eleven LeaveAll phases at 8x8/1if** (receipts/budget/leaveall-spread-after.md):
  - the ten seeds are the sync seed clones of round 2 (`10b2fe21` with their 8x8 config's MAC), given `6ceed753`'s
    harness diff (receipts/budget/regrade-seeds.txt). The harness is identical between `10b2fe21` and `9715a30a`;
  - the product MAC's phase is arm A's parts 1 and 2;
  - **every phase holds.** Every LeaveAll went out at its participant's first transmit opportunity (44 of 44 `sent`,
    two in each group), and no MRP run-out is late. The worst rows are `leaveall` 1.64 ms, `periodic` 2.97 ms and
    `join` 1.86 ms, against the unchanged 20 ms; round 2's worst was 160.6 ms;
  - each seed still exits 1, on the poll base's `STATED` line alone: the 8x8/1if point held to 1x1/1if's stated
    costs, #914's scope as in rounds 1 and 2.

| First LeaveAll drawn, MSRP / MVRP, ms | MAC in the 8x8 config | leaveall.if0, ms | periodic.if0, ms | join.if0, ms |
|---:|---|---:|---:|---:|
| 10,092 / 10,492 | 02:4b:4c:00:01:51 | 0.59 | 1.75 | 0.91 |
| 10,592 / 10,992 | 02:4b:4c:00:01:5f | 0.60 | 2.61 | 1.86 |
| 11,102 / 14,142 | 02:4b:4c:00:00:06 | 0.54 | 1.80 | 0.64 |
| 11,602 / 14,212 | 02:4b:4c:00:00:14 | 0.65 | 1.67 | 0.62 |
| 12,102 / 10,152 | 02:4b:4c:00:00:22 | 1.64 | 1.57 | 1.64 |
| 12,602 / 10,222 | 02:4b:4c:00:00:30 | 0.64 | 1.67 | 0.63 |
| 13,102 / 10,722 | 02:4b:4c:00:00:3e | 0.64 | 1.96 | 1.66 |
| 13,602 / 11,652 | 02:4b:4c:00:00:4c | 1.33 | 2.97 | 1.79 |
| 14,092 / 14,922 | 02:4b:4c:4b:4c:01 (the product's) | 0.58 | 1.82 | 0.56 |
| 14,602 / 12,652 | 02:4b:4c:00:00:68 | 0.65 | 1.77 | 0.64 |
| 15,032 / 14,632 | 02:4b:4c:00:00:88 | 0.53 | 1.74 | 0.81 |

- **#901's valid-destinations leg at 1x1/1if** exits **rc 0** (round 2: 1). `srp-talker`'s two LeaveAlls are sent at
  their first opportunity, and the leg's table is byte-identical: the late run-out was a failing outcome, not a row.
- **The 13 legs, regraded at `6ceed753`** (receipts/budget/regrade-legs-at-6ceed753.txt). Every build is accepted
  against the head's inputs.
  - Eleven legs' tables are byte-identical.
  - 8x8/1if parts 1 and 2 change only in their MRPDU rows: `save-held.mrpdu.leaveall.if0` 160.557 to 0.557 ms and
    `save-starved`'s 160.506 to 0.506 ms, 0 misses each (receipts/budget/legs/).
  - Each rc is as before, but 1x1/1if valid-destinations, now 0.
  - 1x1/1if arm A keeps its 7 ruled held-egress rows in q4.
  - 8x8/1if's valid-destinations leg exits 1 on `STATED` build-one lines alone (#914's scope); its two LeaveAlls are
    sent.

## 3. Q2: the paced record

Changed here: nothing. `record_classes.py` at `6ceed753` still refuses the 1x1/1if paced class: 28,700 cycles, 305 us
by the rule, against `edit_rows.PACED`'s 300 us (receipts/budget/record-classes-at-6ceed753.txt). #898 round 7
restates it to 305 us, with `CTRL_LOOP_TX_MS` 35 at 1x1/1if, by the rule (#897 issuecomment-6928240632). #898 lands
before this sync, and the sync regrades on #898's merge.

## 4. Q3: every route against #818

#818's floor is +0.030 ns setup and 0 ns hold at every signoff corner, on the best of the recipe's three directives.
All fifteen routes recorded in rounds 1 and 2 are regraded against it from their signoff receipts
(receipts/route/floor-818.md):

| Round | Image | ExtraPostPlacementOpt | ExtraTimingOpt | AltSpreadLogic_high | Best of three |
|---|---|---|---|---|---|
| 1 | split 1x1/1if | +0.128 / +0.036 meets | +0.067 / +0.036 meets | +0.399 / +0.036 meets | **meets** |
| 1 | split 8x8/1if | -0.595 / +0.036 setup | +0.014 / +0.036 setup | +0.140 / +0.036 meets | **meets** |
| 2 | split 1x1/1if | +0.189 / +0.036 meets | +0.196 / +0.036 meets | +0.118 / +0.036 meets | **meets** |
| 2 | split 8x8/1if | -0.595 / +0.036 setup | +0.014 / +0.036 setup | +0.140 / +0.036 meets | **meets** |
| 2 | release AX7101 1x1 | +0.108 / +0.016 meets | +0.071 / +0.014 meets | +0.209 / +0.016 meets | **meets** |

Each cell is the worst setup and hold over the four corners. Every image meets #818, and every miss is a true setup
miss. The release route's hold of +0.014 to +0.016 ns passes. The routes ran at `10b2fe21`, whose RTL, firmware and
build inputs the head keeps (round 2's handoff, section 2); `6ceed753` changes harness grading and documentation only.

## 5. Gates (clean clones of `6ceed753`)

The ruling names the gates this change touches: the harness self-test and its mutants, and the docs jobs.

| Gate | Command | Result | Receipt |
|---|---|---|---|
| harness self-test and its mutants | `run.py --self-test` | **0 failures**: 871 checks pass, the 7 new ones included; all 254 mutants caught, the 8 new ones each by the check the README's table names | receipts/budget/selftest-at-6ceed753.txt |
| docs jobs | `run_wf.py` per job: wire-accountability, docs-check-no-git, docs-gates-0, -1 and -2, docs-check; `verify_wf.py 6ceed753 runs/K docs.yml` | **63 steps rc 0, 34 not run with a reason, 0 bad** | receipts/workflows/verify-docs-at-6ceed753.md |
| harness model gates | flip, load, tier grid, their self-tests (`models2.sh`) | PASS, as at `9715a30a` | receipts/budget/models-at-6ceed753/ |
| harness legs, regraded | `run.py --reuse-build --regrade`, the harness checkout at `6ceed753` | every build accepted; 11 of 13 tables byte-identical, 8x8/1if parts 1 and 2 changed in their MRPDU rows alone; 1x1/1if valid-destinations now rc 0 | receipts/budget/regrade-legs-at-6ceed753.txt |
| record classes | `record_classes.py` over the 13 legs | RESULT FAIL on the 1x1/1if paced record alone (Q2) | receipts/budget/record-classes-at-6ceed753.txt |
| quick local checks | `check_py_idiom.py`, `docs_inventory.py --check`, `docs_check.py`, `check_doc_paths.py` (the lane, before the commit) | pass | |

The other gates carry from round 2. All four workflows at `9715a30a` gave 154 steps rc 0 and 256 not run with a reason;
the sweep's 65 suites, `split`, `split-mutants` and the routes also carry. `6ceed753` changes only the harness's
grading Python, its self-test and two documents: no firmware, RTL, harness build input or bench source.

## 6. Open items

- **Q2:** `record_classes.py` refuses the 1x1/1if paced record until #898's restatement (305 us, `CTRL_LOOP_TX_MS` 35)
  lands. The sync then regrades on #898's merge. Neither constant changes here.
- **#914's scope, unchanged:** the 8x8/1if `STATED` lines (the point held to 1x1/1if's stated costs).
- **Reported, not fixed:**
  - twin and twin-plants fail as at `70f4056f` (#929);
  - srptx fails as at `70f4056f` (#916);
  - #840's 1000BASE-T-only advertisement is not on the split (#919);
  - the 8x8/1if split margin is thin, but meets #818 (#927, after the flip).

The seed-run scratch (round 2's clones, builds and logs) is kept, since the regrade read it. Scratch stays under 20 GB.
