# HANDOFF (round 6) — [A775] lane 895

**Status (01:4x CET 2026-11-15): STOP at `bf0844f19374bfbf7091271dfb50fad7a1f1835d` (local, not pushed), posted once on
#895: issuecomment-6886561084 (body = STOP-COMMENT.md).**
- At the restated tables the built design's last queued notice at 1x1/1if is 134.94 ms, over 130.
- The slice rule (`rows_tiers.ruled`, `tier_grid.py`) takes 950 us, not the built 900.
- Both are stops of the ruling #895 issuecomment-6876349305 as the round-6 assignment lists them; the maintainer
  decides.

Background: this was a new assignment, not a resume. Round 5 ended at `62298ab5`, and its two delta reviews were
NEGATIVE: R835-3 (PR #901 issuecomment-6881281833) and R836-3 (issuecomment-6881271637). The push and the PR edit are
the manager's (PR-BODY.md).

- Worktree $LANES/895-talker, branch `895-talker-redeclare`; start head `62298ab5`, tree clean (21:39).
- origin/894-tiers `9606b3a9` (fetched 21:4x); origin/dev-soft-core `cec88385`; review evidence `985065aa`.
- Scratch: /data-2/milan/tmp/895-a775/r6:
  - L: the clean clone of the merge `df0bc467` that the legs ran on.
  - X: the clean clone of #902's `9606b3a9`, for the polls'-base attribution.
  - G: a git-archive export of `df0bc467` with tsn-c-stack and lwSRP, used for what-ifs. Its two tables are edited by
    sensitivity.py.
  - g-merge, g-restated: the graders' outputs. costs-1x1: the parsers' output and the survey.
  - units/: the unit logs.
- Legs: /data-2/milan/tmp/895-a775/{builds,legs}/R6-*; units milan-895-a775-r6-*.
- CPUs: 0-95 were booked by a release hold (`milan-hold911*`) until about 22:28, after which `pick` gave some ranges.
  Until then the legs ran as separate units (MemoryMax 10G) on the session pool 96-127, at most two at a time.

## Commits

| Commit | What |
|---|---|
| `df0bc467` | item 1: merge #902's `9606b3a9`. Conflicts: `load_grade.py` (each cost the side's that moved it from 7398ec0a, the larger where both did: 1x1/1if AECP slot 75, MAAP record 115, TICK 50 (both); 8x8/2if AECP slot 115, TICK 55, MAAP 155, events_none 35 (both); donor ACMP owed frame #894's 55 / 70), `FR_NFR.md` 3.4.1 pace sentence (both), SRP README tx sentence, `SPLIT_CONTROL_MEMORY.md` section 13 (the tiers table, tx paragraph, pace table, both subsections, closing bullet) at the merge's figures |
| `3024e740` | `poll_grade.py:83-94` base 205 -> 215 (1 interface); `load_grade.py` STATED_US 1x1/1if events_none 30 -> 35, STATED_US_DONOR 1x1/1if events_none 30 -> 35 and base 205 -> 215; both tables' comments state the measurement and its attribution |
| `bf0844f1` | docs: section 13 new subsection "The composition measured again (#895)"; the tiers table 1x1 row, tx paragraph, pace table row, closing summary (R4 13.11 = R836-3-F1); two references to "the table above" now name their heads; section 5 plan at this head (the cut's +224 / +208 B), titled and based per R835-3-S3; R836-3-RS1's exact wording (section 13 ROM bullet, section 5); FR_NFR 3.4.1 (pace sentence, queued sentence, SRP row 33.64); SRP README 33.64; plat README 392 B past 60.0, 1,656 left |

## Results

### Survey (R835-3-F1), 1x1/1if, the merge's image

Legs: arm A (96 groups, five parts merged), answering-every-port (16), valid-destinations (2), and arm B (aecp,
aecp-largest-notice, aecp-fanout).
- At the merge's tables (`survey-1x1-merge-df0bc467.txt`): UNDER 4. The base is 20,282 cycles (215 by the rule) against
  205 in poll_grade.STATED_US and STATED_US_DONOR. events_none is 3,041 (35) against 30 in both columns.
- At the restated tables: UNDER 0. The ruled AECP record is within too: every other record is at most 20,525 cycles,
  220 us. AECP's response and probe (aecp_kinds.py) are still running.
- Attribution (receipts/attribution): the heaviest base in acmp-cmd is 18,843 cycles (200 us) on #902's 9606b3a9 and
  20,282 at the merge (+1,439). That pass runs +79 instructions with 4 fewer refills, so the growth is code. By poll:
  MAAP +407, SRP deliver +378, ACMP +320, ADP +198, AECP +161.

### R835-3-F2

8x8/2if datapath-events on the merge's image (leg R6-D8): eventcost.py, #894's measure (#894 6872978311), gives
AMAP_LIVE_WRITE 2,367 cycles = 23.67 us, within 23.80, so 25 stands. AVB 3,575 and ASP 3,421 cycles are within 40.
The one-event-pass measure gives 2,515, but it includes the empty take that events_none charges; it is reported only.

### Graders at the restated tables (worktree; receipts/graders/restated, sensitivity/)

| | 900 (built) | 950 (rule) |
|---|---|---|
| R4 / R5 / R6 | 13.11 / 74.47 / 72.53 | 13.16 / 74.52 / 72.58 |
| first / last | 14.65 / **134.94 (130)** | 14.70 / 127.83 |
| R4L / ACMP / ADP / MAAP | 203.53 / 29.29 / 27.56 / 27.65 | 203.58 / 29.34 / 27.61 / 27.70 |
| tx / txL | 33.64 / 48.32 | 33.69 / 48.37 |

- flip 1x1 rc 1: OVER last; AECP_QUEUED_MS rule 135.
- slice_choice and ruled: 950 (+0.0129).
- tier_grid: 12 of 420, CHOSEN 950.
- rows_tiers selftest: 1031/1032, ESCAPED "the built design's slice not the rule's".
- pace: 9 (txL 49.94 at 8).
- load: 0.517 / 0.513, 0.696 largest.
- 8x8 (reported): unchanged.
- Sensitivity, last at 900: 127.73 at the merge's tables, 133.91 with base 215 alone, 132.72 with events_none 35
  alone, 133.91 with base 210 and events_none 35.
- sensitivity.py runs each configuration in a fresh `-B` interpreter with `__pycache__` removed. The same-size edits
  had been read from stale bytecode in an earlier in-process attempt, and those numbers were discarded.

### STOP checks

| Trigger | Result |
|---|---|
| slice rule not choosing the built design at the restated tables | HIT: 950 against 900 |
| no pace up to 11 ms | the pace is 9 |
| last queued notice over 130 ms | HIT: 134.94 |
| any tier-1, SRP or tx row over its bound | none: R4 13.11, first 14.65, R4L 203.53, ACMP 29.29, ADP 27.56, MAAP 27.65, R5 74.47, R6 72.53, tx 33.64, txL 48.32 |
| the load over 0.70 | 0.517 / 0.513 (0.696 largest) |
| a join interval outside 181-239 ms | 365 at this head, 187.779-190.109 |
| ROM: platform over 60.5, fixture or harness over 59.0, any other point over 56 | 60.5, 59.0 / 59.0 / 59.0, the rest at most 56.0 |
| any lwSRP change | none |

## Legs

| Leg | Point / arm | rc | Notes |
|---|---|---|---|
| R6-A1 (+p1-p4, merged) | 1x1 arm A, 96 groups | 0 | 7 known misses, 0 STATED, joins 286 |
| R6-N1 | 1x1 answering-every-port | 0 | |
| R6-W1 | 1x1 valid-destinations | 0 | |
| R6-B1 | 1x1 answering-ports: aecp, aecp-largest-notice, aecp-fanout | 0 | |
| R6-D8 | 8x8 datapath-events | 0 | F2 |
| R6-X1 | 1x1 acmp-cmd, aecp-fanout on 9606b3a9 | 0 | attribution |
| R6-A8 | 8x8 arm A part 0 | stopped | stopped at 00:1x by its unit name after listing its processes; the other 8x8 legs were dropped from the queue (legs-dropped-8x8.txt) once the stop's triggers were settled |

## ROM (the merge; ledger-merge)

The ledger passes. Platform 8x8/2if 131,464 B, 60.5, 1,656 B left; fixture 8x8/2if 126,320 B, 59.0, 656 B left; the
answering-every-port arm 126,628 B (348 B left); the valid-destinations arm 126,488 B (488 B left); platform 8x8/1if
129,928 B, 56.0. Every image is +224 B (1x1) or +208 B (8x8) of rom against round 5, sram unchanged.

## New checks (planted mutant, failing words)

None in the tree. Round-6 tools (round6/scripts): costs_vs_stated.py, base_attribution.py, sensitivity.py.

## Gates

Not run (STOP), nor the full pass, the sweep or the harness at the final head (its firmware is the merge's).
Graders on a clean clone of the head (receipts/graders/head-bf0844f1):
- flip 1x1 rc 1 (OVER last);
- tier_grid rc 0 (CHOSEN 950);
- load rc 0 (0.517 / 0.513);
- the slice rule 950;
- rows_tiers selftest rc 1 (1031/1032);
- flip selftest rc 1, 584/585 ("ESCAPED AECP_QUEUED_MS not the bound the last queued notice's row rules":
  queued_bound.controls reports the tree's own 130 against the amendment's rule's 135 for the 134.94 row);
- load selftest 25/25;
- check_doc_paths, check_doc_style, docs_check (0 findings), check_py_idiom and check_cpp_idiom: rc 0.

Earlier: Pre-checks at the merge: check_py_idiom, check_cpp_idiom, check_doc_paths, check_doc_style,
check_hygiene, check_solution_docs and check_feature_status, all rc 0. At the worktree before commits 2 and 3:
check_py_idiom rc 0, check_doc_paths and check_doc_style OK, and docs_check.py 0 findings.

## Run history

- 21:39 assignment read; HEAD 62298ab5, tree clean. Both reviews read in full (REPORT.md = the comments).
- 21:47 merge `df0bc467`; graders at the merge: slice rule 950 already.
- 21:49 to 00:56 the legs: A1 and its parts, N1, X1, W1, B1, D8. Pick gave ranges from 22:28.
- 23:23 acmp-cmd at the merge: base 20,282 cycles, so the restatement is certain.
- 00:1x events_none 3,041 found (preliminary survey); what-if: the last is over 130 at 900. The not-yet-started 8x8
  legs were dropped and R6-A8 was stopped.
- 00:33 A1 merged and regraded (rc 0); 00:56 W1 done; 01:0x the survey before and after; restated; graders; docs.
- 01:2x commits `3024e740` (tables) and `bf0844f1` (docs); graders and doc checks on a clean clone of the head;
  surveys at the merge (UNDER 4) and the head (UNDER 0) with aecp_kinds; receipts scrubbed and indexed.
- 01:4x STOP posted once on #895 (issuecomment-6886561084). Nothing pushed.

## For the manager

- Push `895-talker-redeclare` at `bf0844f1` if wanted; it carries the merge, the restatement and the docs. Replace
  PR #901's body with PR-BODY.md; the roles lines take R835-3-RS1's wording.
- The STOP's options (a) to (d) are listed in the comment, and none is chosen. Under (a) the slice at 1x1/1if is a
  firmware constant, so the harness would run again on that image, every point, as would the 8x8/2if legs dropped
  here.
- Receipts: round6/receipts (INDEX.md: 160 files, scrubbed, then indexed and checked: a second scrub changes nothing
  and every hash is its file's bytes). Scripts: round6/scripts.
- Scratch kept: /data-2/milan/tmp/895-a775/{r6,builds/R6-*,legs/R6-*}; no unit of this lane runs.

- `ctrl_loop.h:278-280` states `CTRL_LOOP_SRP_UNIT_US` (250 / 365 us) as "an SRP record's stated cost, the load gate's
  record.srp". `load_grade.STATED_US` states record.srp at 280 / 365, so the slice starts an SRP record only while
  250 us is left at 1x1/1if. The rows do not read it (no harness module does). This is #894's, not this lane's.
- `ctrl_loop.h:262-277` (#894's comment) states the slice rule's choice as 900 us. At this head's restated tables the
  rule takes 950: the decision is the maintainer's.
