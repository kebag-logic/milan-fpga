# HANDOFF (round 7) — [A775] lane 895

**Status (10:4x CET 2026-11-15): 7B STOP at `0c93071e` (local, not pushed), posted once on #895 (issuecomment-6892087027); 7A DONE was at `4c9757ee` (issuecomment-6888794008).** 7A's comment body is 7A-DONE-COMMENT.md and 7B's is 7B-STOP-COMMENT.md. Round 7's assignment is the ruling #895 issuecomment-6886630886 on
round 6's STOP (issuecomment-6886561084), which overrides round 6's stop list. Start head `bf0844f1` (round 6, local,
not pushed), tree clean.

- Worktree $LANES/895-talker, branch `895-talker-redeclare`.
- Scratch /data-2/milan/tmp/895-a775/r7:
  - L: the clean clone of `6d79b352` that the legs, the ledger and the firmware arms ran on.
  - F: the clean clone of the head `4c9757ee`, for the graders and surveys.
  - costs-1x1, costs-8x8: the parsers and the surveys.
  - g-item1, g-restated, g-head: the graders. units/: the unit logs.
- Legs: /data-2/milan/tmp/895-a775/{builds,legs}/R7-*; units milan-895-a775-r7-*. No unit of this lane runs.

## 7A

| Item | What | State | Commit | Evidence |
|---|---|---|---|---|
| 1 | the built 1x1/1if slice = the slice rule's choice at the head's restated tables (950 us), `ctrl_loop.h` states the rule, the self-tests hold the figure; round 6's two restatements stand | done | `ff943513`, `6d79b352` | graders/g-item1, g-head |
| 2 | rebuild; every 1x1/1if leg and the 8x8/2if legs; survey both points; restate; rows, pace, load, tier_grid, joins | done: 1x1/1if UNDER 0 (every cost round 6's, cycle for cycle); 8x8/2if MAAP's timer slot restated 215 -> 225; every 1x1/1if row holds at 950; the rule chooses 950 again | `58c99c67`, `4c9757ee` | legs, costs, survey, graders/g-head |
| 3 | one behaviour-neutral cut, only if no grid slice in 650-1,100 holds every row | not needed: 950 holds every row (+0.0129) | | |

### Commits (on `bf0844f1`)

| Commit | What (file:line, reason) |
|---|---|
| `ff943513` | item 1. `ctrl_loop.h:262-281`: the comment states the rule (the built slice is the rule's choice at the tree's stated costs, #895's ruling of 2026-11-15 item 1), and `CTRL_LOOP_SLICE_US` at 1x1/1if goes 900 -> 950. `rows_tiers.py` tree control: the stated line is now 950, with 900 (the slice built before) planted, refused "the built design's slice not the rule's". `selftest_round.py:108` holds [950, 1300]. The harness README (the slice_grade line and the self-test table row) and the SRP README state 950. |
| `6d79b352` | `rows_tiers.py` back to 1,000 lines with the comment on two lines. check_py_idiom's long module was 11 > 10 at `ff943513`: my command chain ran the commit past the failed check. Behaviour unchanged; selftest 1032/1032. |
| `58c99c67` | `load_grade.py` STATED_US and STATED_US_DONOR 8x8/2if `event.MAAP` 215 -> 225: MAAP's timer slot, 21,120 CPU cycles in arm A's save group at 8x8/2if (TIMER#4; 19,993 at #895's merge with the tiers), 225 by the rule; comments in both columns. |
| `4c9757ee` | docs: section 13 gets the tiers definition (950 at one interface), the slice paragraph, the tiers table, the tx paragraph, the pace table row, round 6's closing summary in the past tense, a new subsection "The rule's slice built (#895)", and the closing bullet (R4 13.16). Round 5's TRANSMIT bullet reads 33.69 / 94.99 at this head. FR_NFR 3.4.1 (the pace sentence, the queued sentence, the SRP row 33.69); SRP README tx 33.69. |

### Checks of item 1 (planted, failing words)

- `rows_tiers.py --selftest` plants a header with 900 us. It is refused, so "the built design's slice not the rule's"
  is caught: 1032 of 1032. At round 6's head that control escaped at 1031 of 1032, with the tree at 900.
- `selftest_round.py`: "each point's slice is ctrl_loop.h's stated length at it, 950 us at 1x1/1if and 1,300 us at
  8x8/2if" holds [950, 1300]. The harness self-test was not run in 7A; it is part of 7B's gates.
- Firmware arms at 950 on the clean clone (receipts/arms): unit PASS; port, portable and AECP (`test_port_loop.cpp`,
  `test_aecp.cpp`, which use the slice) PASS.

### Legs (clean clone of `6d79b352`; receipts/legs/summary.txt)

| Leg | Point / arm | Groups | rc | Notes |
|---|---|---:|---|---|
| R7-A1 (5 parts, merged) | 1x1 arm A | 96 | 0 | 7 known misses, 0 STATED, joins 286 |
| R7-N1 | 1x1 answering-every-port | 16 | 0 | |
| R7-W1 | 1x1 valid-destinations | 2 | 0 | |
| R7-B1 | 1x1 arm B: aecp, aecp-largest-notice, aecp-fanout | 3 | 0 | |
| R7-A8 (5 parts, merged) | 8x8 arm A | 94 | 0 | 7 known misses, joins 587 (182.679 the shortest) |
| R7-N8 | 8x8 answering-every-port | 16 | 0 | |
| R7-W8 | 8x8 valid-destinations | 2 | 0 | |
| R7-B8 | 8x8 arm B: aecp, aecp-largest-notice, aecp-fanout | 3 | 0 | 2 of 451 passes over the share, in aecp-largest-notice, the longest 223,684 cycles (2.237 ms); 8x8/2if's share is deferred to #890 (round 28 ruling, item 3), reported |

Joins: 1,109 in 231 group runs, 182.679 to 190.642 ms, all within 181 to 239.

### Survey (receipts/survey)

| Point | 6d79b352's tables | head 4c9757ee |
|---|---|---|
| 1x1/1if | UNDER 0: every cost equals round 6's (`costs.txt` the same key for key but one event count) | UNDER 0 |
| 8x8/2if | UNDER 2: `event.MAAP`, 21,120 cycles, 225 by the rule, against 215 in both columns | UNDER 0 |

8x8/2if: AMAP_LIVE_WRITE 2,367 cycles (25, within). The survey now reads interface 1's datapath events: eventcost
keys them by type + 0x100. Each is below interface 0's: 2,936 / 2,990 / 2,365. The ruled AECP record: every other
record is at most 20,525 cycles (1x1, 220) and 18,551 (8x8, 195).

### Graders at the head (clean clone F; receipts/graders/g-head)

1x1/1if by every source at 950 us: R4 13.16, R5 74.52, R6 72.58, first 14.70, last 127.83 (130), R4L 203.58, ACMP
29.34, ADP 27.61, MAAP 27.70, tx 33.69 (34), txL 48.37. flip PASS.
- slice_choice and ruled both give 950 (+0.0129), equal to the built slice: the choice does not move a second time.
- tier_grid: 12 of 420 hold, CHOSEN the built design.
- pace 9 (txL 49.99 at 8).
- load 0.517 / 0.513, 0.696 with every command the largest legal one.
- Self-tests: rows_tiers 1032/1032, flip 585/585, load 25/25.
- docs_check 0 findings; doc paths, doc style, py idiom and cpp idiom rc 0.
- 8x8/2if (reported, rc 1 by design): R4 42.87, R5 196.35, R6 186.60, first 20.50, last 667.92, R4L 210.93, ACMP
  66.08, ADP 66.19, MAAP 67.16, tx 94.99 (98 stated), txL 399.88; load 0.798 / 0.756.

### ROM (receipts/ledger, at `6d79b352`)

Every image's size is round 6's: the platform 8x8/2if is 131,464 B, 60.5, with 1,656 B left; the fixture and both
harness arms are at 59.0 (656 / 348 / 488 B left); the platform 8x8/1if is at 56.0 and the rest are below. plat_ledger
passes.

### STOP checks (the ruling's list)

| Trigger | Result |
|---|---|
| after item 3's cut, no slice in 650-1,100 holds every 1x1/1if row, or the load over 0.70 | no cut was needed: 950 holds every row; load 0.517 |
| the rule's choice moves a second time on a rebuilt image | no: 950 on the rebuilt image's tables |
| no pace up to 11 ms; a join outside 181-239 | pace 9; joins 182.679 to 190.642 |
| ROM over 60.5 / 59.0 / 56 | 60.5 / 59.0 / 56.0, each within |
| any lwSRP change; a cut needing a wire-visible change | none; no cut |

### Run history

- 01:32 ruling read; HEAD bf0844f1, clean.
- 01:3x item 1 committed (`ff943513`); idiom failure found after it and fixed (`6d79b352`); graders at the round-6
  tables at 950 all PASS.
- 01:3x round 5's scratch removed (my own; /data-2 21 -> 34 GB free); clone r7/L; legs started 01:36 (pool, then
  picked ranges from 01:49); ledger 01:40; firmware arms 01:41-01:53.
- 03:31 1x1/1if legs done but W1; 04:17 W1; 04:31 8x8/2if arm A; 04:34 W8; merges rc 0.
- 04:4x surveys: 1x1 UNDER 0, 8x8 UNDER 2 (MAAP's slot) -> `58c99c67`; graders; docs `4c9757ee`; graders and surveys at
  the head; receipts indexed (205 files).
- 05:0x 7A DONE posted once on #895 (issuecomment-6888794008). Nothing pushed. Session ends for the 7B relay.

### For the manager

- Push `895-talker-redeclare` at `4c9757ee` if wanted (rounds 6 and 7A, six commits on `62298ab5`). PR-BODY.md is
  round 7A's.
- 7B: sync onto #902's round-12 review head, survey, restate, the rule chooses again, then the single final pass with
  gates and sweep. `CTRL_LOOP_SRP_UNIT_US` arrives with that sync, and it is not changed here.
- The 8x8/2if arm B's `aecp-largest-notice` passes over the share (above) are for #890's flip, reported.

## 7B (STOP)

Relay: #902's round-13 review head, origin/894-tiers `234bc149` (REVIEW READY #894 issuecomment-6890460677; #894
ruling issuecomment-6888782796 item 2: #895 takes #902's slice at its sync and drops its own). Start `4c9757ee`, clean.

| Commit | What |
|---|---|
| `7e3db6b9` | merge `234bc149`. Taken from #902: `ctrl_loop.h` whole (950 slice rule text, `CTRL_LOOP_SRP_UNIT_US` 280, build of one 735), `rows_tiers.py` slice control (header-derived, 600 planted), `selftest_round.py` (holds `rows_tiers.ruled`), the harness README's slice lines. That drops my 7A slice commits' duplicate (`ff943513`, `6d79b352`). Costs, each by the side that moved it from `9606b3a9`, the larger where both did: 1x1/1if AECP slot 75 (mine; #902 70), TICK 55 (#902), MAAP record 115, fixed part 35, base 215 (mine), mrpdu and build of one 735 (#902); 8x8/2if MAAP record 155, MAAP slot 225, AECP slot 115 (mine). `AECP_PACE_MS` 9: mine, and the pace rule's at the composed tables (txL 52.09 at 8, 48.40 at 9). Docs: both sides, at the composed tables' figures. |
| `f14e56a9` | item 3's cut: `srp_mbx_gate` returns at once when the gate and base equal its last call's (`srp_mbx.h` `gate_seen`, `gate_base`). Only init and the entry write the gate and the sources' destinations, so it is exactly neutral. Plant `talker-gate-repeat-ignores-its-base` (35 Talker plants), caught by Talker.DestinationChangeWhileValidWithdrawsTheOld and Talker.ResetKeepsAnUnchangedSourceAndHoldsAMovedOne at 1 and 2 interfaces. SRP README. Arms talker, srp-acmp-if1/if2, port, portable, unit PASS on the worktree. |
| `1a917cf1` | `rows_tiers.py`'s control comment back to #902's (it now equals #902's file) |
| `2657af21` | the polls' base at 1x1/1if 215 -> 225, both tables (`poll_grade.py:83-97`, `load_grade.py` donor 1x1 and its comment): 21,094 cycles in save-held on the cut's image, by the rule (survey UNDER 2 -> 0) |
| `0c93071e` | docs: section 13 "The composition with #894's SET_CONFIGURATION cut (#895)", 7A's closing summary in the past tense, the tiers table, the pace table row, the closing bullet (R4 13.30, last 135.43); FR_NFR 3.4.1; SRP README tx 34.05 |

Composed tables at `7e3db6b9` (graders, worktree; receipts g7b-merge):
- 1x1/1if at 950: last queued notice 134.74, over 130; flip FAIL. R4 13.25, R5 74.98, R6 73.04, first 14.75, R4L
  203.59, ACMP 29.51, ADP 27.78, MAAP 27.88, tx 33.88, txL 48.40.
- slice_choice 1200 (+0.0004), outside 650-1,100, so ruled falls back to 800. tier_grid holds 2 of 420, CHOSEN 1200.
- No grid slice in 650-1,100 holds every row: last >= 134.74 at every one.
- rows_tiers selftest 1032/1033 ("the built design's slice not the rule's"); flip selftest 584/585 (queued bound).
- Load 0.517 / 0.514. 8x8/2if tx 99.32 against its stated 98.
- Sensitivity at those tables: a per-pass base + fixed part of 240 us or less makes 950 the rule's choice with every
  row holding (base 205, fixed part 35: last 127.85, +0.0165). 245 does not (last 132.84).

The polls' base, `acmp-cmd`'s heaviest (receipts attribution-7b):
- #902 `234bc149`: 19,074 cycles, 205 by the rule.
- The merge `7e3db6b9`: 20,453, 215 by the rule. The +1,379 falls in AECP's poll (+625) and delivery (+840), not in
  the Talker's own polls (MAAP -6, SRP deliver -290): placement. The pass has +82 instructions and 17 refills fewer.
- The cut `1a917cf1`: 19,736 (-717), 210 by the rule, over the 19,523 that 205 allows.

ROM at `7e3db6b9` (ledger.sh): platform 8x8/2if 131,688 B, 60.5 (1,432 B left); fixture 8x8/2if 59.0 (432 left);
the answering-every-port arm 59.0 (124 left); valid-destinations 59.0 (272 left); platform 8x8/1if 56.0 (928 left);
platform 1x1/2if 44.0; fixture 8x8/1if 55.0. All within.

Legs:
- The merge's 1x1/1if legs and all 8x8/2if legs were stopped at 08:2x-08:31 as superseded by the cut (my units,
  listed first; .stopped files). Only R7B-B1, C1 (acmp-cmd at the merge) and X1 (acmp-cmd at #902's head) ran to
  their end.
- The cut image's 1x1/1if set R7K-* (clone r7b/K at `1a917cf1`) started 08:31.

Disk: round 6's legs and scratch, and rounds 3-4's r3/r4/gates3/gates3h, removed (my own); /data-2/milan/tmp/895-a775
33 -> 12 GB.

### Final (head `0c93071e`, clean clone r7b/F; receipts/7B/graders/g-head)

Cut image 1x1/1if legs R7K-* (clone r7b/K at `1a917cf1`): A1 96 groups merged, N1 16, W1 2, B1 3. All rc 0, 0 refusals,
7 known misses, 0 STATED; joins 359, 188.102 to 190.121. Survey (receipts/7B/survey): base 21,094 in save-held, 225 by
the rule, UNDER 2 against 215; every other cost within (the fixed part 2,449, AECP response 2,465 cycles).

At the final tables, 1x1/1if at 950: R4 13.30, R5 75.89, R6 73.41, first 14.77, **last 135.43 (130)**, R4L 203.62, ACMP
29.68, ADP 27.91, MAAP 28.01, tx 34.05 (49; 34 stated), txL 48.63.
- No slice in 650-1,100 holds every row: the best is 950 at -0.0418; 650 to 1,100 run from last 167.39 to 135.59.
- 1,200 is at -0.0043 (txL 49.21).
- tier_grid holds 0 of 420; ruled 800 (fallback); flip FAIL.
- rows_tiers selftest 1031/1033 (the built slice not the rule's; THE TRANSMIT's stated figure under its row, 34 against
  34.05 and 98 against 98.99 at 8x8/2if); flip selftest 584/585 (queued bound: the amendment's rule 140); load
  selftest 26/26.
- pace 9 (txL 52.34 at 8); load 0.517 / 0.514.
- docs_check 0 findings; doc paths and style, py and cpp idiom rc 0.

ROM at the cut's head `1a917cf1` (receipts/7B/ledger-cut): platform 8x8/2if 131,752, 60.5, 1,368 B left; fixture
8x8/2if 126,608, 59.0, 368 left; the answering-every-port arm 126,916, 59.0, **60 left**; valid-destinations 126,776,
200 left; platform 8x8/1if 130,200, 56.0, 872 left; fixture 8x8/1if 55.0; platform 1x1/2if 44.0. Within every cap.

STOP checks (#895 issuecomment-6886630886):

| Trigger | Result |
|---|---|
| after item 3's cut, no slice in 650-1,100 holds every 1x1/1if row | **HIT**: the last queued notice is over 130 at every one |
| the load over 0.70 | 0.517 |
| the rule's choice moves a second time on a rebuilt image | the rule has no holding slice in range (ruled 800 by fallback) |
| no pace up to 11; a join outside 181-239 | pace 9; joins within |
| ROM over 60.5 / 59.0 / 56 | within |
| lwSRP change; a cut needing a wire-visible change | none; the cut is behaviour-neutral |

Not run, at the stop: the gates, the full pass, the sweep, the firmware campaigns, and 8x8/2if's legs on the cut's image.

STOP posted once on #895: issuecomment-6892087027 (body = 7B-STOP-COMMENT.md); PR-BODY.md is round 7 in full.

### For the manager (7B)

- Push `895-talker-redeclare` at `0c93071e` if wanted: round 6, 7A and 7B, twelve commits on `62298ab5`.
- The stop's options (a) to (c) are in the comment, and none is chosen.
- The placement figures (#909): `acmp-cmd` 19,074 on #902's head against 20,453 at the merge and 19,736 at the cut;
  `save-held` 19,793 at 7A's head against 21,094 at the cut.
- Scratch kept: r7b (L = merge, K = cut, F = head, X = #902's head, P = the plant), builds R7K-*, R7B-C1 and R7B-X1, and
  7A's 8x8/2if builds R7-A8, R7-N8, R7-W8, R7-B8 (the last 8x8/2if measurement). Superseded scratch was removed.
