# HANDOFF (round 8) — [A775] lane 895

**Status (15:0x CET 2026-11-15): STOP at `f93317cb` (local, not pushed), posted once on #895 as issuecomment-6895274375 (STOP-COMMENT.md; the posted body checked identical but a trailing blank line).** At 8x8/2if the rule gives `CTRL_LOOP_TX_MS` 105 (tx 104.25 at the restated tables), which would move `SRP_REDECLARE_CS` at two interfaces from 2,029 to 2,030 cs, a wire-visible change. It is not restated. Every 1x1/1if row holds. Round 8's assignment is the ruling #895 issuecomment-6892130675 on round
7B's STOP (issuecomment-6892087027), which overrides round 7's stop list. Start head `0c93071e` (round 7B, local, not
pushed), tree clean. origin/894-tiers `b6f5c638` (#902 round 16).

## Items

| Item | What | State | Commit | Evidence |
|---|---|---|---|---|
| 0 | merge origin/894-tiers b6f5c638; #902's images by hash | done: images identical to the cut head's, 552 of 552 | `1143e3f5` | receipts/identity |
| 1 | AECP_QUEUED_MS (one interface) = the queued rule's figure; FR_NFR 3.4.1 with the row against 125/130/140 | done: 140 (row 135.43 at 950; 136.65 at 900) | `2b7f8428` | |
| 3 | CTRL_LOOP_TX_MS by the rule at both points; SRP_REDECLARE_CS unchanged | by the rule 34 at 1x1/1if (tx 34.00 at the rule's 900 us) and 99 at 8x8/2if (98.99; #902's 99): no change, no commit; SRP_REDECLARE_CS 2,023 / 2,029 cs | none | graders |
| 4 | the slice rule chooses again at the new bound; the pace by its rule | done: 900 us (+0.0086, txL binding; 950 +0.0076); pace 9 | `73388996` | graders |
| 7 | rebuild; every 1x1/1if leg, the 8x8/2if legs; survey; one full pass; margins; the 140 ms per-pass cost | done but the full pass: 1x1 UNDER 0; 8x8 four costs restated; margins and the 278/279 us per-pass cost; full pass not run (STOP) | `b69388c7`, `f93317cb` | receipts |

## Commits (on `0c93071e`)

| Commit | What |
|---|---|
| `1143e3f5` | merge #902's `b6f5c638`. ctrl_loop.h merged clean (#902's 99 ms at two interfaces). Conflicts: aecp_mbx.h's pace comment (mine, with #902's "was 49.69"), the SRP README (mine), FR_NFR 3.4.1 (mine with #902's four history wordings), section 13 (each side's text where it states its own figures) |
| `2b7f8428` | item 1: `aecp_mbx.h` AECP_QUEUED_MS (one interface) 130 -> 140, its comment: the row rounded up to 5 ms, never over 140 (queued_bound.ruled), 135.43 at the composition; FR_NFR 3.4.1: 140 (130 on #894's head), the row against 125 (+10.43), 130 (+5.43) and 140 (-4.57) |
| `73388996` | item 4: `ctrl_loop.h` CTRL_LOOP_SLICE_US (one interface) 950 -> 900, the rule's choice at the 140 ms bound, its comment; harness README, SRP README |
| `b69388c7` | 8x8/2if restatements (reported) by the rule: poll_grade.STATED_US[2] base 325 -> 345 (32,705, N8 notice-every-4) and aecp_long 655 -> 700 (66,481, B8 aecp-largest-notice); load_grade 8x8 events_none 35 -> 40 both columns (3,437, acmp-noresp), donor base 325 -> 345; rows_tiers DATAPATH_US 8x8 AMAP_LIVE_WRITE 25 -> 30 (2,465), comment edited in place (1,000 lines) |
| `f93317cb` | docs: section 13 "The bound and the slice at 140 ms (#895)" (bound, slice, TX figure, sync, legs, rows and margins, the 140 ms per-pass cost, ROM, 8x8/2if's TX conflict), 7B's closing in the past, tiers table, tx paragraph, pace row, closing bullet (R4 13.25); FR_NFR 3.4.1; SRP README tx 34.00 (scripts/docs_r8.py) |

Graders before the rebuild (worktree, the 7B tables, bound 140; /data-2/milan/tmp/895-a775/r8/g-items):
- slice 900: flip PASS, R4 13.25, R5 75.84, R6 73.36, first 14.72, last 136.65 (140), R4L 203.57, ACMP 29.63, ADP 27.86,
  MAAP 27.96, tx 34.00 (34), txL 48.58.
- tier_grid holds 6 of 420 and chooses the built design (+0.0086).
- Self-tests: rows_tiers 1033/1033, flip 585/585, load 26/26.

Identity (receipts/identity): image_sha.py hashes every image ledger.sh links (each ELF's loadable bytes and every
object).
- The cut head `1a917cf1` against the merge `1143e3f5`: 552 of 552 identical.
- The merge against the head `73388996`: 16 differ, all one-interface: ctrl_loop.o and the ELF at 1x1-if1 and
  8x8-if1, fixture and platform and the SoC export's images. No two-interface image changed.

ROM at the head (r8/ledger): equal to the cut head's sizes. The platform 8x8/2if is 131,752, 60.5, with 1,368 B left;
the answering-every-port arm has 60 B left at 59.0.

## The rebuilt image at 1x1/1if (clone r8/L at `73388996`)

Legs R8-A1 (5 parts, merged, 96 groups), N1 (16), W1 (2) and B1 (3): all rc 0, 0 refusals, the 7 known misses, 0
STATED; joins 359, 188.102 to 190.121 ms. Costs equal the cut image's but for event counts, and the fixed part is
2,715 cycles (30 by the rule, 35 stated). save-held's base is 21,094, unchanged.

Survey (r8/costs-1x1): UNDER 0. The ruled AECP record is within (21,187 cycles, 225 against 235). Nothing is
restated, so the bound (140) and the slice (900) settle after the one rebuild.

Rows at the head (receipts/graders/per-pass-threshold.txt; built 900 us, bound 140):

| Row | W, ms | Bound | Margin, ms | Relative |
|---|---:|---:|---:|---:|
| R4 | 13.25 | 20 | 6.75 | +0.3375 |
| R5 | 75.84 | 90 | 14.16 | +0.1573 |
| R6 | 73.36 | 90 | 16.64 | +0.1849 |
| first | 14.72 | 20 | 5.28 | +0.2640 |
| last | 136.65 | 140 | 3.35 | +0.0239 |
| R4L | 203.57 | 238 | 34.43 | +0.1447 |
| ACMP | 29.63 | 30 | 0.37 | +0.0123 |
| ADP | 27.86 | 30 | 2.14 | +0.0713 |
| MAAP | 27.96 | 30 | 2.04 | +0.0680 |
| tx | 34.00 | 49 | 15.00 | +0.3061 |
| txL | 48.58 | 49 | 0.42 | +0.0086 |

The per-pass cost: a pass's own cost (the fixed part 35 plus the polls' base 225) is 260 us. The last queued notice
holds 140 ms up to 278 us (base 243: 137.93 ms) and passes it at 279 (base 244: 141.36), where txL also passes
(49.02). Every row holds to 278 us.

## 8x8/2if on the rebuilt image

Legs R8-A8 (5 parts, merged, 94), N8 16, W8 2, B8 3. A8 and W8 rc 0.
- N8 rc 1 on 16 STATED lines: the polls' base up to 32,705 cycles against 32,500.
- B8 rc 1 on 2 STATED lines: aecp_long 66,481 against 65,500. After `b69388c7` both regrade rc 0 on clone r8/L moved to
  `b69388c7` (the builds record that clone's paths).
- Joins 750, 185.605 to 190.228.
- Share, reported (#890): N8 2 of 15,694 passes, at most 2.018 ms; B8 2 of 458, at most 2.337.

Survey (receipts/survey): UNDER 7 at `73388996`'s tables (the four costs above, in their tables) and UNDER 0 at the
head, both points.

Rows at the head, reported: R4 45.06, R5 209.00, R6 198.71, first 21.11, last 857.77, R4L 211.08, ACMP 68.94, ADP
68.91, MAAP 69.89, tx 104.25, txL 466.85; load 0.798 / 0.756.

THE TRANSMIT figure at 8x8/2if: tx 104.25 against the 99 stated, so tx_statements refuses and the rule gives 105.
SRP_REDECLARE_CS = 2000 + SRP_JOIN_CS (19) + (CTRL_LOOP_TX_MS + 9) / 10 at two interfaces would be 2,030 cs (2,029 at 98
and 99), a withdrawn Talker's changed destination declared 10 ms later. The ruling lists a wire-visible change as a
stop, and the relay asks to show the hold-off unchanged: STOP, not restated. At 1x1/1if it is 2,023 (34 by the rule).

## Graders at the head (clean clone r8/F at `f93317cb`; receipts/graders/g-head)

- flip 1x1 rc 0 (PASS); flip 8x8 rc 1 by design.
- tier_grid rc 0: 6 of 420, CHOSEN built 900 (+0.0086).
- slice_choice (900, +0.0086) = ruled = built; queued statements [].
- pace 9, statements []. tx_statements: ["8x8/2if: CTRL_LOOP_TX_MS states 99 ms, under the built design's tx row 104.25 ms"].
- load 0.517 / 0.514.
- Self-tests: rows_tiers 1032/1033 (ESCAPED "THE TRANSMIT's stated figure under its row"), flip 585/585, load 26/26.
- docs_check 0 findings; doc paths and style, py and cpp idiom rc 0.

## Run history

- 10:10 ruling read; HEAD 0c93071e, clean; origin/894-tiers b6f5c638.
- 10:1x merge 1143e3f5; fixed point at bound 140 on a scratch copy; items 1 and 4 committed; graders.
- 10:15 clone r8/L at 73388996; legs R8-* started (picked ranges and the pool); ledgers at the head and the merge.
- 12:2x the 1x1/1if legs done; A1 merged; survey UNDER 0; margins and the per-pass threshold (per_pass_threshold.py).
- 13:0x N8 and B8 rc 1 (STATED); W8 and B8 started on the pool (light); 13:22 A8 parts done, merged; prelim 8x8 survey UNDER 7.
- 13:3x the 8x8 restatements prepared: the 8x8 tx row 104.25 > 99, rule 105, SRP_REDECLARE_CS 2,029 -> 2,030 at two interfaces: the stop.
- 14:29 W8 done; final 8x8 survey (the same four); `b69388c7`; N8 and B8 regraded rc 0; docs `f93317cb`; graders on clone F; surveys at the head UNDER 0.
- 15:1x receipts INDEX.md (203 files, round8/scripts/index.py); removed builds R7-A8/B8/N8/W8, R7B-C1/K1/X1, R7K-A1/B1/N1/W1
  and the r7, r7b clones and r8/G, G2, G3, docs-dry (22 GB -> 12 GB).

## For the manager

- Push `895-talker-redeclare` at `f93317cb` if wanted: rounds 6 to 8 on `62298ab5`. PR-BODY.md covers rounds 6 to 8.
- The STOP's options (a) to (c) are in the comment, and none is chosen. Under (a) the two-interface images change in
  srp_mbx.o's `SRP_REDECLARE_CS` constant and the static assertion only; the 8x8/2if legs would carry by hash.
- Scratch kept: r8 (L, F, M clones; ledgers), builds R8-*. Superseded 7A/7B builds were removed (see run history). The lane's
  scratch is 12 GB.
- 15:2x STOP posted once: #895 issuecomment-6895274375.
