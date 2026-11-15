# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 4, [A781]

Status: REVIEW READY at `98c0b62be911f5cff7a03ebfee7f837c23847d14` (comment text `REVIEW-READY-COMMENT.md`, posted on #894 as issuecomment-6887981011; PR text `PR-BODY.md`). No STOP condition: no regrade fails, no image changed.

- Start head: 716a8ae7979a31315a6e085959dc4dcc8b7ee022 (branch 894-8x8-1if, tree clean, verified 00:0x CET)
- Final head: 98c0b62be911f5cff7a03ebfee7f837c23847d14 (four commits; nothing pushed)
- Base: 894-tiers at 9606b3a9 (#902 OPEN, round 12): not merged, by instruction. dev-soft-core cec88385.
- Reviews answered: R843-1 POSITIVE (issuecomment-6885564795), R844-1 NEGATIVE (issuecomment-6885381555), both
  REPORT.md read in full from 894-review-evidence (review-evidence/894b-r1/reviews/).

## Items

1. R844-1-F1 (MAJOR): the acceptance gate fails any held-egress row over its ledger figure. — DONE in the tree
   (`tb/verilator/ctrl_service_budget/egress_ledger.py`, self-test) and in the packet gate (`scripts/gate_r4.py`,
   which delegates to it); controls 20/20; round 3's six legs regraded: PASS (at the most each logged figure can be:
   63.0835 / 63.3055 / 63.5265 / 63.7475 / 63.9695 / 62.0255 / 61.6805 ms against 63.24 / 63.47 / 63.69 / 63.91 /
   64.20 / 62.18 / 61.83).
2. R844-1-R1 / R843-1-R1 (RESIDUE): 55 added lines reworded; scan of 7398ec0a..worktree: 0 lines. Images: step 1 all
   8 identical (ELF and loadable). — DONE (commit 1); at the head the lane gates' scan and R844-1's audit: 0 lines.
3. R843-1-S1 (SUGGESTION): aecp.h's guarded #error (keyed on the charging unit, AECP_CHARGES_ATTEMPTS, aecp.c with the
   table first) and test_aecp.cpp's static_assert(MBX_N_IF == AECP_TEST_INTERFACES), core arms at two interfaces on
   their own contract. — DONE (commit 2); controls PASS; step 2 images all identical.
4. Gates on clean clones of the final head 98c0b62b. — DONE, all rc 0 (table below).

## Why the gate's ledger logic is in the tree

The ledger rule decides acceptance of every 8x8/1if measurement, and the next one (after the sync onto #902's merge)
needs it, so it belongs beside the other graders with its self-test. Nothing in the tree held it: run.py's
`--record-budget-findings` records every miss and fails none, and round 3's gate waived the seven rows by name. The
rest of the packet gate stays in the packet: it aggregates the legs' own verdicts (run.py's exit status, STATED, JOINS,
END lines) into the lane's report tables, and every failure it adds beyond the ledger mirrors a check the harness
already makes per leg.

## Commits (on 716a8ae7; nothing pushed)

1. `6da0dc7324` — the source-comment rule (item 2): 25 files, 70 lines reworded, line counts kept in every file.
2. `b7feef24d0` — item 3: aecp.h's guard, aecp.c's include order, test_aecp.cpp's assertion, the host arms' contract,
   the two campaign rows, the AECP README.
3. `3bb204c81ab371f2e99161efb1a37c8198ad82cf` — item 1: `egress_ledger.py`, the harness README, section 13, FR_NFR.
4. `98c0b62be911f5cff7a03ebfee7f837c23847d14` (**final head**) — `egress_ledger.py`'s self-test helpers held to the
   Python idiom gate (a helper of seven parameters to six, `controls`' runner annotated, one 121-column line wrapped):
   the full pass's first lane gates at 3bb204c8 found it (py_idiom rc 1: "unannotated public function 1 > ratchet
   0", "too many parameters 8 > ratchet 7", "over-long line 1 > ratchet 0"); my worktree run had passed only because
   the file was still untracked then. The diff: `receipts/source/commit4-egress-ledger-idiom.diff`.

## Changes (file:line at 3bb204c8, reason)

**Item 2 (commit 1).** Each `issuecomment-<id>` in an added line is the issue, the ruling's subject and its item:
`#894's shape ruling` (issuecomment-6867393730: THE SHAPES, the slice cap, the 8x8/1if gate), `#894's held-egress
ruling` (issuecomment-6871343905: (a) the held-egress rows, (b)(i)-(iv) the per-shape costs, (c) the single source;
the name R844-1 and the manager use), `#894's retry-cost ruling` (issuecomment-6878014227) and `#894's map-keying
ruling` (issuecomment-6870437042). poll_grade.py:97-98's "round 2 ruling" is gone with its ID. Section 13
(SPLIT_CONTROL_MEMORY.md:2471, commit 3) maps the four names to their links, where links are allowed. Every C/H/C++
file keeps its line count (so `__LINE__` and the debug-free images cannot move); `rows_grade.py:120`'s docstring is
the keying's own line (its standing restriction allows the keying), docstring only.
Proof of no code change: `receipts/source/commit1-code-unchanged.txt` (`scripts/ast_same.py`): every C/H/C++ file's
token stream with comments removed is identical; every Python file's syntax tree without docstrings is identical, but
five printed check descriptions in selftest_notice.py (1) and selftest_round.py (4), whose text only lost the ID
(no mutant or test reads them: grep of selftest_mutants.py, selftest.py, README).

**Item 3 (commit 2).**
- `sw/firmware/ctrl/aecp/aecp.h:64-70`: `#if defined(AECP_CHARGES_ATTEMPTS) && !defined(CTRL_LOOP_RETRY_ATTEMPT_US)`
  `#error "THE SHAPES: a unit that charges a refused attempt (AECP_ATTEMPT_US) has no shape's table (ctrl_loop.h) in
  force"`. Why keyed on the charging unit: every unit includes aecp.h before the table (aecp.c, aecp_mbx.h,
  aecp_face.h, test_aecp.cpp), and most charge nothing, so an `#ifndef` at the define would break every core unit;
  C cannot test a name at a later use. The define line stays the one `#define AECP_ATTEMPT_US
  CTRL_LOOP_RETRY_ATTEMPT_US` that `shape_costs.retry_findings` requires.
- `sw/firmware/ctrl/aecp/aecp.c:3-8`: `ctrl_loop.h` first, then `#define AECP_CHARGES_ATTEMPTS`, then
  `aecp_internal.h` (was: `aecp_internal.h`, then `ctrl_loop.h`). Every image byte-identical (step 2).
- `sw/firmware/ctrl/test/test_aecp.cpp:37-43`: `#include "mbx_contract.h"` and `static_assert(MBX_N_IF ==
  AECP_TEST_INTERFACES, "THE SHAPES: the host arm's mailbox contract (MBX_N_IF) is not at its interfaces
  (AECP_TEST_INTERFACES)")`.
- `sw/firmware/ctrl/test/aecp_arms.py:111-119`: a core arm with no mailbox group at two interfaces compiles against
  the generated two-interface contract (`srp_arms.prepared`'s variant), so the assertion holds in every arm; the
  debug arm keeps the tracked contract (its test configures one interface whatever the arm's count, and compiles
  test_aecp_debug.cpp, which has no assertion). Only command-line arms reach a core arm at two interfaces with no
  mailbox group (`--core/--nvm/--work --interfaces 2`); every job's arms are at their interfaces' contract already.
  Core.* at two interfaces on its own contract: 83 of 83 pass.
- `sw/firmware/ctrl/test/aecp_retry_mutants.py:11-15, 198-207`: rows `attempt-charged-without-the-shapes` and
  `attempt-charged-before-the-shapes` (Build.refused, the campaign's compile-refusal reader). The campaign grows by 2.
- `sw/firmware/ctrl/aecp/README.md:21-33`: the contract paragraph states the include order, the guard and the
  assertion.

**Item 1 (commit 3).**
- `tb/verilator/ctrl_service_budget/egress_ledger.py` (new): LEDGER (:42) is section 13's table at 8x8/1if;
  `findings` (:139) fails a ledger row over its figure (`over`, :65, in 10 ns units, one bus cycle), never released or
  answered, or with no measured instance; any instance not measured; any other budget miss. Reads results directories
  (exact) or a run's log (`from_log`, :88: held at the printed figure plus half its microsecond; the summary's
  refusals 0 and its misses equal to the BUDGET lines). `--selftest` (:332): 30 controls in process and as a process
  (exit status), 8 mutants.
- `docs/design/SPLIT_CONTROL_MEMORY.md:2528-2536`: the ledger table's third column is `Ledger, ms` (was `Round 1,
  ms`) and its two service rows carry their full probe names, so the tool's self-test reads the table exactly; :2526
  names the tool.
- `tb/verilator/ctrl_service_budget/README.md:156-163`, `docs/reference/FR_NFR.md:394`: the tool documented.
- Packet: `scripts/gate_r4.py` (round 3's gate, its held-egress rows and every miss decided by the tree's
  `egress_ledger`, every instance not measured failing, and `-:LOG` legs read from their logs).

## New checks (planted mutant, failing words)

| Check | Plant | Failing words |
|---|---|---|
| `egress_ledger.py --selftest` (30 controls, in process and as a process) | 8 mutants: the earlier rule (a ledger row waived by name whatever its size); a grade read at 1 us; a row at its figure failing; a new miss waived; a row with no instance passing; a log's figure read as exact; a figure a hundredth over section 13's; a row's name taken in any group | each caught by its own control (receipt) |
| `scripts/gate_controls.py` against `gate_r4.py` | per row: one bus cycle over, and +36.76 ms; R844-1's two inputs | "- the ledger: <row> (backlog-owed): <ms> ms, over its ledger figure <L> ms by <d> ms: a larger miss" |
| AECP campaign `attempt-charged-without-the-shapes` (Build.refused) | aecp.c without `#include "ctrl_loop.h"` | `THE SHAPES: a unit that charges a refused attempt (AECP_ATTEMPT_US) has no shape's table (ctrl_loop.h) in force` |
| AECP campaign `attempt-charged-before-the-shapes` (Build.refused) | aecp.c with the table after aecp.h | the same words |
| test_aecp.cpp static_assert | a two-interface core arm at the tracked one-interface contract (packet plant) | `THE SHAPES: the host arm's mailbox contract (MBX_N_IF) is not at its interfaces (AECP_TEST_INTERFACES)` |

## Gate table (final head 98c0b62b, each part on its own clean clone)

| Gate | Result | Receipt |
|---|---|---|
| Every `run:` step of every rtl-fast, rtl, elaborate and docs job (`run_wf.py`, `verify_wf.py`) | 139 run at rc 0, 226 not run with a reason, 0 bad. `elaborate-gates-1` ran twice: the first run's gate_19 exited 92 (`test_soc_timing_cuts` at its 900 s wall clock under host load, load average about 100: "result UNKNOWN, not a failure"); the second, on a fresh clone, passed every step | `gates/workflows-verify-98c0b62b.md`, `gates/elaborate-gates-1-{first,second}-gate_19.txt`, `gates/not_run.json` |
| Firmware jobs (unit, boundary, control, AECP, SRP campaigns, verilator) | every step 0; campaigns 716, 277, 345 caught, 0 escaped (277 = round 3's 275 and the two new rows); boundary PASS; `aecp_wire.py --every` exit 0; the 8x8/1if mailbox arm ok | `firmware/firmware-jobs-98c0b62b.txt` |
| Lane gates a, b, c (`lane_gates_r4.sh`) | 59 gates, 55 at 0, the four exit-1-by-design at 1; harness self-test 879 checks, 259 caught, 0 failures; ledger self-test PASS; comment scan 0 lines; R844-1 audit 0 lines; rows_tiers 971/971, flip 581/581, load 25/25, table 24/24; load 0.513/0.509 at 1x1/1if, 0.711 at 8x8/1if; 16 diff-check bases; every clone clean after | `gates/lane-gates-98c0b62b.txt` |
| Every image (Q-img) | all 8 identical to 716a8ae7's, ELF and loadable; 56.0 RAMB36 at platform-8x8-1if | `images/img-3-final-against-716a8ae7.txt`, `images/raw-3-final-98c0b62b.txt` |
| counters-f5 (consumer of test_aecp.cpp) | 1x1 and 8x8 rc 0; clone clean | `firmware/counters-f5-98c0b62b.txt` |
| docs_inventory --check | not present at this head or its bases; on dev only | `gates/not_run.json` |
| The sweep, the 8x8/1if measurement, the 1x1 and 8x8/2if legs | carry by image identity | `source/carry-by-identity.txt`, `source/commit1-code-unchanged.txt` |

Before the commit, on the worktree: `egress_ledger.py --selftest`; `gate_controls.py` (20/20); the regrade; `arm_checks.py`
(the campaign rows, the arms, the plant); `shape_costs --check --selftest`; py/cpp idiom, hygiene, TODO ownership,
baremetal-only, docs_check, doc style, doc paths, em-dash, ctrl_hot; steps 1 and 2 of the images.

## Images (loadable-byte sha256)

- Baseline 716a8ae7 (clean clone, this round): all 8 reproduce round 3's receipt exactly (`receipts/images/raw-0-base-716a8ae7.txt`).
- Step 1 (comments reworded, worktree): all 8 identical, ELF and loadable (`raw-1-comments.txt`).
- Step 2 (with item 3, worktree): all 8 identical (`raw-2-guard.txt`, `img-2-against-716a8ae7.txt`).
- The final head 98c0b62b, a clean clone (the full pass's Q-img): all 8 identical (`raw-3-final-98c0b62b.txt`).

## Run history (CET)

- 00:01 start. HEAD 716a8ae7, tree clean. Read R844-1 and R843-1 REPORT.md in full (894-review-evidence ddba6ac4),
  #894's held-egress ruling (6871343905) and the shape, retry-cost, map-keying and egress rulings (scratch).
- 00:1x baseline images: a clean clone of 716a8ae7, all 8 built (qimg.sh, unit on 112-127): reproduce round 3's
  receipt exactly. 00:2x item 2's rewording (55 lines, 25 files); scan 0 lines; step 1 images all identical.
- 00:2x-00:3x item 3: aecp.h guard, aecp.c include order, test_aecp.cpp assertion, aecp_arms.py contract, two campaign
  rows; arm checks unit (r4-arms): first run stopped at the campaign's own table-drift control on a filtered table
  (my script's error), fixed by running the control on the whole table first; second run PASS (receipt). Step 2
  images all identical.
- 00:2x-00:3x item 1: egress_ledger.py + self-test (first run: one control's matcher too strict, fixed; then 60 PASS,
  8 of 8 mutants each caught by its own control); gate_r4.py; gate_controls.py 20 of 20; regrade of round 3's six legs
  from their logs (the group grades were not kept after round 3): PASS.
- 00:3x commits 6da0dc73, b7feef24, 3bb204c8. Picker: no free 8-wide range in 0-95 (124 CPUs busy), so the queue falls
  back to the session CPUs 96-127, at most 4 of its units at once (launchR4.py). 00:36 full pass launched (19 units).
- 00:41 counters-f5 (tb/verilator/milan_dp, which compiles test_aecp.cpp in a one-interface mailbox arm; no workflow
  or sweep case runs it) launched on the clean clone as an extra unit.
- 01:11 the lane gates at 3bb204c8 showed py_idiom rc 1 (above). 01:12 the pass stopped: the eight units (the launcher,
  lane-a/b/c, W-elab-1, W-fw-boundary, W-fw-control, W-rtl-fast) each listed with its command and stopped by its exact
  unit name; no process of the scratch path left. Its partial results are superseded (kept in scratch only).
- 01:13 the fix, with every repository-wide check on the worktree first (py_idiom, hygiene, TODO ownership,
  baremetal-only, docs_check, doc style, doc paths, cpp_idiom, ctrl_hot, the ledger self-test): rc 0 each. Commit
  98c0b62b. 01:15 the full pass relaunched at 98c0b62b on a fresh clean clone (20 units, counters-f5 among them;
  ranges in 0-95 free this time). The gate controls, the regrade and the ledger self-test rerun against 98c0b62b's
  grader: PASS (receipts replaced).
- 01:15-02:47 the full pass at 98c0b62b: every unit rc 0. verify_wf: 1 bad, elaborate-gates-1's gate_19 (rc 92, the
  timing-cuts simulation's wall clock under load); 02:47 that job alone again on a fresh clone (session CPUs; no
  picked range free), 03:30 every step rc 0; verify_wf: 139 run, 226 not run with a reason, 0 bad.
- 03:3x receipts and index; the REVIEW READY comment posted on #894, issuecomment-6887981011, identical to `REVIEW-READY-COMMENT.md` but its final newline (the round's one comment). Then the full pass's clones removed from scratch (7.7 GB left), its logs kept. Nothing pushed; no PR
  created or edited; no merge.
