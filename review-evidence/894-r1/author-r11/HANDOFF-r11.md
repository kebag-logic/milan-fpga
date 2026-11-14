# HANDOFF — #894 round 11 ([A773], PR #902, branch 894-tiers)

Assignment: #894 issuecomment-6878230332 (authority 6876349104; bounds 6858269025,
6862465874, 6867990126; direct-index ruling 6870437042). Measurement that opened it:
issuecomment-6878200592.

Start: 2026-11-14 14:50 CET, HEAD 7398ec0a (clean).

## Status

- [x] 1 ATTRIBUTE the one-row REMOVE (27,851) and ADD (22,932) by function and pass
- [x] 2 CUT: ADD 20,595 holds; REMOVE 22,728 (240 by the rule) does not -> amended step 3
- [x] 3 AMENDED (class split, EDIT_RECORD_US 260 / 325) (issuecomment-6878532871, read 15:11): if no cut holds 235, the CLASS SPLIT first (paced edits,
      ceil((w+1)/P) per window, at the edit record's measurement + 5 %; every other AECP record at 235; planted
      control: an unpaced edit charged at the non-edit figure fails by name; LONG_ROWS stays R4L/txL-only). Only if
      cut AND split both fail: restate flat and STOP. TICK at 50 moves no row: restate if not cut.
- [x] 4 TICK attributed, restated 50 (final arm A: 4,612)
- [x] 5 record_classes.py (6 controls) + the final pass
- [x] 6 section 13, FR_NFR 3.4.1, PR-BODY.md
- [x] REVIEW READY posted 2026-11-14 21:30 CET: #894 issuecomment-6883768027 (exactly one; body = REVIEW-READY-COMMENT.md). Nothing pushed; head 9606b3a9 is 10 commits ahead of origin/894-tiers (7398ec0a).

## 1. Attribution (done 15:05)

PC traces (sim_main BUDGET_TRACE_AFTER/PCS) of aecp-fanout on the aecp-check bisect builds, spans reproduced exactly
(REMOVE 17,932 / 25,356 / 27,851; ADD 16,047 / 19,716 / 22,932 at 9d7167bd / 1b70cedd / 7398ec0a). Profiler
round11/scripts/spanprof.py; lines from a -g build of the same code (aecp_map_command 0 differing bytes).
- 9d7167bd -> 1b70cedd (#904's check): +1,643 commits. `memcpy`/`forward` +822 (look()'s `union held x = {*r}` and
  mark()'s `m->rows[kept++] = m->rows[k]`, each a jal memcpy of 8 B, ~120 cycles), `memset` +323 (the 960 B clear),
  `mark` +423.
- 1b70cedd -> head: same commits (4,342 vs 4,321), +2,495 cycles = D-cache misses everywhere (arm, aecp_rx,
  aecp_note, changed, legal, owe).
- Head REMOVE in the command (17,068 of 27,851): clear 2,616, table 2,388, FOUND mark 2,899, turns 425, REMOVE pass
  2,813, notice 2,560, entry 3,355.
- Note: the assignment's "8cc3e5d3's 17,932" is 9d7167bd's figure; 8cc3e5d3's image (12180198) is 19,008.

### Mechanism found (15:20-15:50)
- Caches: fetch L1 128x2x64 B (16 KiB), LSU L1 128x1x64 B (8 KiB direct-mapped). ~580k cycles of other work between
  commands, so each command's path is mostly cold.
- Cycle split (r11/scripts/budget.py): 9d7167bd commits 2,699 / short stalls 7,311 / fetch 6,338 / data 1,584; head
  4,321 / 10,397 / 10,349 / 2,784; exp2 3,236 / 8,605 / 10,467 / 1,633. Refills 114 / 143 / 145, nearly all distinct
  lines (r11/scripts/fetchsets.py). Executed lines 178 -> 184 only: most of the growth is lines cached before
  (changed 1 -> 8 refills, mbx_tx_begin 4 -> 8) that are cold at the new layout.
- mark(): ~35 instructions a row, 4-6 cycle stall on most (load-use, taken branch); key()'s `h->w[input]` (planted)
  goes through the stack.

### Experiments (aecp-fanout REMOVE / ADD; aecp-largest-notice largest)
| exp | change (cumulative) | REMOVE | ADD | long | .text |
|---|---|---:|---:|---:|---:|
| head | - | 27,851 | 22,932 | 91,625 | 97,956 |
| exp1 | assign(): no memcpy call in look(), mark(), the ADD's append | 25,611 | 22,338 | 88,953 | 97,940 |
| exp2 | + clear MAP_DOMAIN slots and next/flags/copies[0,count) | 23,941 | 21,483 | 87,497 | |
| exp3 | + look() words in registers, mark() reads rows/count once, per-mapping clears at the turn, LE #error | 23,793 | 21,214 | 87,685 | 97,928 |
| exp4 | + GET_AUDIO_MAP in map_page(), echo bytes inline, REMOVE skips self-copies | 23,210 | 20,931 | 87,500 | 97,952 |
| exp5 | + REMOVE reach (two loops; look() went out of line) | 23,078 | 20,755 | 86,941 | 98,180 |
| exp6 | exp4 + REMOVE reach in one loop | 22,728 | 20,595 | 86,978 | 98,176 |
| **exp7** | exp6 without map_page() (GCC inlined it anyway): **the cut, committed bc971054** | **22,728** | **20,595** | **86,978** | 98,176 |
| exp8 | exp7 + echo written by the table (+112 B: every other record +300-400, layout) | 23,105 | 20,603 | 86,895 | 98,288 |

Cut verdict: ADD holds 235 (20,595 <= 22,380); REMOVE does not (22,728, 348 over) -> amendment step 2, CLASS SPLIT.
Images at exp7 (qall, r10/scripts/qall.sh): 1x1/1if fixture 110,800 in 112,640 (40.5 -> 41.0 RAMB36, the granule
ruling 6870437042 warned of, within 56); 8x8/2if platform 130,704 in 131,072 (368 B spare), 60.0 tiles; 8x8/1if
platform 56.0 unchanged; sram unchanged.

### Arm B (answering-ports) aecp-fanout, NOT the formal measurement (README: labelled arms never are)
1x1 head / exp7: input REMOVE 27,968 / 22,803, ADD 22,615 / 20,471, output REMOVE 28,456 / 24,360, output ADD
24,013 / 22,480, **SET_CONFIGURATION 33,692 / 33,724 (355 by the rule vs 235)**. 8x8 head / exp7: output REMOVE
43,008 / 30,563 and 42,257 / 29,715 (if1), ADD 37,309 / 28,366, **SET_CONFIGURATION 78,647 / 78,332 (825 vs 265)**.
To report as an open decision (AGENTS.md 2: publish the conflict); not a listed STOP.

exp4: every other record of both groups equals the head's to the cycle (layout after aecp_maps within 4 B).

## TICK (attributed 15:35)
4,617 cycles, 508 commits, 29 refills (r11/an/prof-tick.txt): AECP's sink ~1,400 (its poll transmits: transmit 434,
now 266, arm 205), SRP's on_event 809 in 19 commits (misses), loop/take/face ~2,000. Every TICK without AECP's
transmit is <= 3,241. Cutting needs <= 4,285 (45 by the rule); moving the transmit out of the tick is a behaviour
change. Decision: restate event.TICK 45 -> 50 at 1x1/1if (both columns), amendment says it moves no row (verify).

## Changes (file:line, reason)

- bc971054 `sw/firmware/ctrl/aecp/aecp_maps.c`: assign() (copy a coordinate at a time; whole struct = jal memcpy);
  look() words composed in registers + LE #error; mark() reads rows/count once, FOUND pass holds the reach
  (e->from/to), REMOVE pass looks up only the reach, rows before stay, rows after move down; clear only
  MAP_DOMAIN slots + each mapping's next/flags/copies at its turn; 4/6-byte echo inline; stale() under
  AECP_MAP_WORK only. `test_aecp.cpp`: Core.MapEditWorkReadsOnlyWhatItCleared (work arm),
  Core.MapCommandsEchoTheirDescriptorAndPage. `aecp_map_mutants.py`: 12 rows. `aecp/README.md`: the cut.
- 895f8906 tb: edit_rows.py (EDIT_RECORD_US 240/325, terms, findings, controls: "an unpaced edit charged at the
  non-edit record"), tier1_rows.py (AECP's records apart from 'others' in every row; edit_terms), rows_tiers.py:136
  ('edits' in the records source), :465 (w_ms to tier1_records, None for LONG_ROWS), :174 (two lines merged for the
  import, cap 1000), CONTROLS and controls() + edit_rows; record_classes.py (the pass check: classes, pacing, arm A
  coverage; 6 planted controls), load_grade.ceiling_checks + record_classes.checks() (so run.py --self-test runs
  them); README (bullet + paragraph). Self-tests: rows_tiers 1032/1032, load 25/25, flip 585/585, record classes
  6/6; py_idiom rc 0.
- What-ifs (r11/an/rows/whatif-tick45.txt, round11/scripts/whatif.py): split at 295 reproduces A10's 28.69/127.48/
  48.12 (28.68/127.42/48.09); flat 295 reproduces 33.12/135.06/52.94 (33.10/134.99/52.91). Non-edit at 355 (arm B
  SET_CONFIGURATION): ACMP 35.47, ADP 33.68, MAAP 33.91, last 137.73, txL 54.84, all over.

## New checks (planted mutant, failing words)

All 12 caught by name (r11/rows1, rows2); the 30 existing aecp_maps.c rows re-run, all caught (r11/rows3).
| row | plant | test | words |
|---|---|---|---|
| map-remove-reach-a-row-late | from = k + 1 | EDIT | the edit's map is its definition's, row for row |
| map-remove-reach-a-row-short | to = k | EDIT | same |
| map-remove-rows-past-the-reach-dropped | tail loop removed | EDIT | same |
| map-remove-kept-row-unmoved | kept++ == k | EDIT | same |
| map-row-words-cluster-channel-dropped | w[1] = cluster | EDIT | status for command |
| map-copy-cluster-channel-dropped | assign drops cc | EDIT | row for row |
| map-slots-cleared-a-slot-short | MAP_DOMAIN - 1 | CLEARED | an ADD beside a row at the domain's last position is accepted |
| map-marks-uncleared | flags not cleared | CLEARED | same |
| map-occurrences-uncleared | copies not cleared | CLEARED | a REMOVE of one of two equal rows removes one |
| map-links-uncleared | next not cleared | CLEARED | visits past twice their sum |
| map-echo-page-dropped | k < 4 | ECHO | a map command's response echoes its descriptor and page |
| map-echo-index-short | k < 3 | ECHO | same |

## Commits (head 9fda93a1)
1. bc971054 firmware cut + 2 tests + 12 plants + aecp/README
2. 895f8906 class split (edit_rows, tier1_rows, rows_tiers) + record_classes + load_grade hook + harness README
3. 0a474c6f TICK 45 -> 50 at 1x1/1if, both columns (4,617 at 7398ec0a; same TICK 3,242 under the cut)
4. dd788ed5 EDIT_RECORD_US 1x1 240 -> 260 (arm B output REMOVE 24,360): at 240 + TICK 50 the dropped-term control
   'built 1x1/1if first: the source edits not counted' escaped (10 us term at the 0.01 ms resolution); at 260 1032/1032
5. 9fda93a1 docs: section 13 (rows table row, THE TIERS table, fixture 110,800/41.0, '### The one-row edit'), FR_NFR 3.4.1
Rows at the head 1x1/1if: R4 12.91 R5 73.20 R6 69.06 first 14.54 last 126.89 R4L 188.39 ACMP 28.55 ADP 26.94 MAAP 27.06
tx 29.98 txL 48.12; load 0.513/0.509; tier_grid 18/420 built chosen; 8x8/2if reported R4 42.45 ... txL 446.92.
SET_CONFIGURATION arm B 1x1: 33,533 at 12180198, 33,267 at 9d7167bd, 33,692 at head, 33,724 at the cut: PRE-EXISTING.

6. 3e0ca737 aecp_maps.c: mark()'s locals and the edit's from/to one a line (lane gate cpp_idiom at 9fda93a1 FAILED:
   'multi-declarator declaration 3 > ratchet 0'). 332 of 332 image files identical to 9fda93a1 (r11/img-wt, one
   clone path; control MAP_FLOOR 264: 24 differ). FINAL HEAD 3e0ca737. Re-run at 3e0ca737: quick lane gates
   (r11/gates-out/lane-3e0ca737, unit lane-pre-3e0c) and the six firmware jobs (W-fw-*-3e0c, r11/gates-out/wf-3e0ca737,
   dispatchers 6 on 48-55 and 7 on 32-39). Sweep, RTL/docs jobs, legs and arm A carry by the identity; regrade at
   9fda93a1 (fp-wt), whose tb/ equals the final head's.

## Final pass (started 16:43 at bc971054, clone r11/fp-wt)
- arm A: units r11-A-p1 (96-103), r11-A-p2 (104-111, waits for p1's build), build r11/gates-out/builds/A.
- 13 legs (r11/gates-out/queue-legs.txt) via r11-dispatch on 112-127, MAX 4; log r11/gates-out/dispatch.txt.
- Later: merge + regrade at the final head (tree:firmware unchanged after bc971054 or the builds are stale!).
- DO NOT edit sw/firmware/** after bc971054.
- 13 legs done 17:23 (H-J8, H-J81 rc 1 as round 9: STATED srp build slice; others 0).
- 17:23 gate queue r11/gates-out/queue-final.txt (18 lines, lane-a/b/c + W-*) via r11-dispatch2 on 112-127 MAX 4.
- 17:25 sweep: native-shards.py 894-a773-r11, shards on 8-15, 16-23, 48-55, 80-87 (from show; pick had freed them),
  out r11/gates-out/sweep, clones $LANES/894-a773-r11-shard*.
- After arm A: merge p1+p2 (hard links) -> results-merged, regrade at 9fda93a1 (clone it!), costs.sh/compare,
  record_classes over every leg; verify_wf.py over r11/gates-out/wf.

## Commits 7-10 (FINAL HEAD 9606b3a9)
7. 6ec12ad7 ACMP's owed frame 1x1 50 -> 55 (4,890 in backlog-owed under the cut; 4,723 at 7398ec0a), so the tx row took
   a 17th pass (33.01 > CTRL_LOOP_TX_MS 30): CTRL_LOOP_TX_MS 30 -> 34 (only a _Static_assert reads it; images identical);
   rows_tiers/flip controls re-anchored 34/33; docs.
8. 9106a980 flip_grade control words 'states 29 ms' -> 'states 33 ms' (flip + harness self-tests escaped at 6ec12ad7).
9. 2d579e89 fw_coverage exclusion: aecp_maps.c:296 `} else if (kept++ != k) {` arc 2 of 2 unreachable (reach starts at a
   removed row); fw_coverage --check FAILED at 9fda93a1 and 6ec12ad7 (firmware-unit step 12; verify_wf showed it).
10. 9606b3a9 8x8/2if events_none 30 -> 35 and item.acmp 65 -> 70 (A10 issuecomment-6881287231: check every table at both
   points; compare_point.py over the 8x8 legs). 8x8 reported rows R4 42.62 ... txL 459.40, load 0.794/0.754.
A10 issuecomment-6881004362 (dispatch-build/ untracked): reproduced at every head, not changed (round 9's key_arms).

## Gate table (receipts/final)
| Gate | Head | Result |
|---|---|---|
| full arm A 1x1 (bc971054 fw; regraded, fp-wt at 9fda93a1 + 6ec12ad7's tb diff) | | 96 groups, 0 ref, 7 held-egress misses, 0 of 139,557 over share, joins 188.002-190.022 |
| 13 legs, regraded | | 8 rc 0; 81L/81A/81N/J8/J81 rc 1 = round 9's STATED lines/error |
| record_classes.py all legs | 9606b3a9 | RESULT PASS |
| compare (1x1 arm A, 8x8 legs) | 9606b3a9 | only class lines (+ #910 build_one at 8x8) |
| images 332 | 9fda93a1/3e0ca737/6ec12ad7 | identical; control 24 differ |
| lane a | 9fda93a1 / 6ec12ad7 | 0 but 4 by design; cpp_idiom (fixed 3e0c); flip+harness selftests (fixed 9106) |
| lane b, c | 9fda93a1 / 6ec12ad7 | 0 |
| lane model/text (33) | 9106a980 / 9606b3a9 | 0 but 4 by design |
| verify_wf | 9fda93a1 / 6ec12ad7 | 139 ran / 226 reason / 2 bad / 1 bad (idiom 3e0c, coverage 2d57) |
| fw jobs 6 | 3e0ca737, 6ec12ad7 | all steps 0 but step 12 |
| firmware-unit | 2d579e89 | every step 0, coverage PASS |
| AECP campaign | 6ec12ad7 | 286/286 |
| docs jobs 4 | 2d579e89 / 9606b3a9 | every step 0 (61 at the head) |
| sweep 4 shards (8-15,16-23,48-55,80-87) | 9fda93a1 | each command rc 0 |

## Notes for a successor

- Scratch: /data-2/milan/tmp/894-a773/r11/
- Session pool 96-127; cpu_ranges.py show at 14:50: all 128 booked.
