# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 8, [A781]

Status: STOP to the maintainer at `acfa5601` (comment text `STOP-COMMENT.md`, posted once on #894 as issuecomment-6914891355): six held-egress
rows over their ledger figures on the composed image. PR text `PR-BODY.md`. Nothing pushed; no PR created or edited.

- Start head: d539f162 (round 7's REVIEW READY; the bar met there: R843-4 POSITIVE with R844-3's at the ancestor
  af2c4d7a), tree clean, 03:4x CET. Only the session's own unit running.
- Assignment (manager, round 8, "the sync, and nothing else"): PR #901 merged into dev-soft-core as 70f4056f; one
  --no-ff merge of it, every conflict resolved keeping both sides' behaviour with a resolution table, every bound or
  cost that differs by shape keyed per shape (1x1/1if #901's, 8x8/1if this PR's); re-measure on the composed image
  (the 8x8/1if gate, the 1x1/1if rows, the class grader), restating only by the rule; #918's three stated-cost lines
  at the 8x8-1if harness point resolved or shown not to apply; ROM per image; gates on a clean clone of the final head;
  one REVIEW READY or STOP on #894.

## The merge `d1c9023b` (parents d539f162, 70f4056f)

dev-soft-core 70f4056f carries #902 merged (659d7687, #902's 07ed787e among it) and #901 (52 files, 2,343 lines).
Nine files conflicted: the manager's six and the SRP README, the harness README and poll_grade.py.

| File | This PR's side | #901's (dev-soft-core's) side | Resolution |
|---|---|---|---|
| `ctrl_loop.h` | THE SHAPES: slice, builds, SRP unit, THE RETRY per shape | `CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 900u : 1300u)`, `CTRL_LOOP_SRP_UNIT_US (... 280u : 365u)` and a comment that 8x8/1if takes the one-interface slice | THE SHAPES kept; #901's 900 us in the (1,2,2) block (its other one-interface figures equal that block's); its comment on 8x8/1if dropped (THE SHAPES state 1,475 us there) |
| `aecp_mbx.h` | the retry history plus THE SHAPES sentence on the cold start and attempt | the history rewritten in the past tense under THE TIERS | #901's history and this PR's THE SHAPES sentence |
| `aecp_shape.py` | the key domain under `#ifndef CTRL_SRP_ENTITY_H` | the name runs (`AECP_ENTITY_NAME_RUNS`, `_INIT`) | both: the guard and the runs; generated at build time, nothing tracked |
| `aecp/README.md` | the notices-most sentence (12 / 40 by shape); 130 ms at 1x1/1if | 140 ms at 1x1/1if by the queued rule | #901's 140 at 1x1/1if, this PR's notices sentence, and 130 ms at 8x8/1if stated for its shape |
| `srp/README.md` | the slice one at every point, 1,475 at 8x8/1if by shape | 900 us at 1x1/1if, the tx row at 34.00 ms | #901's text with this PR's 8x8/1if slice by shape |
| harness `README.md` | THE SHAPES section; slice 950 at 1x1/1if | the readers' text without THE SHAPES; slice 900 | this PR's THE SHAPES section with #901's 900 us |
| `poll_grade.py` | the table by shape (ONE, EIGHT_ONE, TWO) | by interface count, base 225 (one) and 345, long notice 700 (two) | the table by shape with #901's figures in ONE and TWO; EIGHT_ONE 8x8/1if's own |
| `SPLIT_CONTROL_MEMORY.md` | tier 2's slice by shape | the slice by interface count, 900 at this head | by shape, 900 us at 1x1/1if |
| `FR_NFR.md` (3 hunks) | 130 ms at 1x1/1if; the 8x8/1if block; THE SHAPES' retry costs; the MRPDU held to `CTRL_LOOP_TX_BOUND_MS` | 140 ms at 1x1/1if; the search in the past tense; the tx figure 34/105 and the hold-off; the MRPDU against T_svc's 20 ms | #901's 140 and hold-off text; this PR's 8x8/1if block, retry costs by shape and the MRPDU at `CTRL_LOOP_TX_BOUND_MS` (`mrpdu_grade.py` is this PR's, unchanged by #901) |

**Keyed per shape in the merge** (no textual conflict, but one shape's figure would reach the other):
- **`AECP_QUEUED_MS`**: #901's `(MBX_N_IF == 1u ? 140u : 62u)` would give 8x8/1if 1x1/1if's 140 (R843-3's and
  R844-3's pending duty). Now `CTRL_LOOP_QUEUED_MS` in every THE SHAPES block, 140 / 130 / 62 / 62, and
  `AECP_QUEUED_MS` is that name. Its readers: `rows_grade.header` (THE SHAPES override), `notice_window.queued_ms`
  (a point's shape), `queued_bound.py` (1x1/1if's block; its plants in that block), `flip_grade.py`'s plant,
  `selftest_notice.py` (140, 130, 62), `shape_costs.py` (the keying held like THE RETRY's, with a control: the bound
  back on the interface count is refused naming 8x8/1if).
- **`CTRL_LOOP_TX_MS`**: #901 makes it a term of a withdrawn Talker's hold-off (`SRP_REDECLARE_CS`, IEEE 802.1Q-2018
  35.2.2.8: two LeaveAllTime periods after the Leave departs). Keyed on the interface count, 8x8/1if would take
  1x1/1if's 34 ms though its own tx row by every source is 67.84 ms, so the hold-off would undercount when its Leave
  departs. Now `CTRL_LOOP_TX_MS` in every block, 34 / 68 / 105 / 105 (8x8/1if: its row rounded up, the rule
  #901 states for the figure), the hold-off 2,023 cs at 1x1/1if, 2,026 at 8x8/1if, 2,030 at two interfaces;
  `ctrl_loop.c`'s assertion holds 1x1/1if alone (keyed on its shape; 8x8/1if's rows by every source are reported, as
  8x8/2if's). Readers: `rows_tiers.built_constants` (THE SHAPES first), its and `flip_grade.py`'s plants
  (`shape_costs.planted_at`, `planted_under`).
- **Not keyed, one figure at every shape on both sides:** `AECP_PACE_MS`, #901's 9 ms; `AECP_QUEUED_FIRST_MS`.
- **Auto-merged, checked:** #901's `load_grade.py` (8x8/2if's columns restated: MAAP's record 155, its event 225,
  AECP's event 115, the TICK 55, events_none 40, base 345; 8x8/1if takes them by NEAREST), `rows_tiers.py`
  (AMAP_LIVE_WRITE 30 at 8x8/2if), `run.py`/`build.py` (the valid-destinations arm, now in this tree).

**Images at the merge** (`qimg.sh`, the working tree against a clean clone of 70f4056f): the six 1x1 and 8x8/2if
images byte-identical (ELF and loadable sha256), so #901's measurement there carries; the two 8x8/1if images moved.

## The restatements (by the rule, on the composed image)

- `84c1704d`: `poll_grade.EIGHT_ONE` base 250 (23,756 cycles, save-held / save-starved), acmp 80 (7,450, backlog-owed);
  `load_grade.OWN['8x8/1if']['record.maap']` 175 (16,323, valid-destinations srp-talker-loss; 8x8/2if's 155 under it).
- `acfa5601`: `rows_tiers.LONG_RECORD_US['8x8/1if']` 1,715 (162,969); `edit_rows.PACED['8x8/1if']` one-row edit 335
  (31,449), accepted SET_CONFIGURATION 685 (65,169); THE SHAPES' 8x8/1if `CTRL_LOOP_TX_MS` 70 for its tx row 69.84
  at the restated costs (the hold-off's (TX + 9) / 10 is 7 at 68 and 70: every image byte-identical to d1c9023b's);
  section 13 (the composed measurement, the ledger pending a ruling, the build coverage, #918's item) and FR_NFR 3.4.1.
- Not restated: the slice and builds at 8x8/1if (arm A's srp group no longer declares Talkers beside its Listener
  Ready since #901; no group composes both; a statement over its measurement is not the defect).

## The measurement (on d1c9023b's image; the head carries it byte-identical)

- Legs: R8-A0..A3 (arm A in four parts), R8-AE (answering-every-port, 16), R8-B (answering-ports aecp, aecp-fanout,
  aecp-largest-notice), R8-VD (valid-destinations, srp-talker and srp-talker-loss), R8-CTA (the transmit-aged control,
  8 of 8, 71.517-71.971 ms). 116 groups, 1,736 instances.
- As run: every leg rc 0 but A1 and A2, each one STATED line (the polls' base 23,756 against 23,500). Regraded at
  84c1704d (run.py --regrade, from the checkout the builds were made in, moved to 84c1704d, which changes graders
  only; a regrade from another checkout path is refused, the build's inputs being recorded by path): every leg rc 0.
- Gate (gate_r8.py): every CPU-decided row within its bound; SRP's Talker rows (a JoinTime's wait) 189.688 of 220;
  queued 2.649 / 25.646; the largest command 3.599; joins 186.613-190.363; slices within 147,500; THE RETRY's
  2,303,370 rounds none over; 0 STATED lines. FAIL: the ledger, six rows over by 0.190-0.273 ms.
- Survey: three costs over their statements (restated above); record classes: long and paced over (restated above).
- Load 0.718 / 0.677 (0.75); 1x1/1if rows hold (flip check), load 0.517 / 0.514 (0.70). Rows by every source at
  8x8/1if reported: R4 20.96 (newly over its 20), R5 129.34, last 347.75, txL 148.97; the all-largest load 1.017.
- Attribution: the 8x8/1if images of the merge against the bare composition (TX 34 there) differ in the hold-off's
  `li a3,2023` -> `li a3,2026` alone (objdump -d and -s), so the growth is the composed code's.
- plat_ledger at 84c1704d: PASS at four points, 7 of 7; 8x8-if1 56 of 56 RAMB36, rom 130,200 B.
- Quick checks on a clean clone of acfa5601: 18 of 18 rc 0 (receipts/gates/quick-checks-acfa5601.txt).
- Not run, by the STOP: item 3's final gates (firmware units and campaigns, fw_coverage --check, the docs jobs, the
  harness self-tests and lane gates, verilator shards 1, 3, 4, 6, 10, 17 of 19, those whose suites build the split
  firmware: mbx, milan_dp's pieces, milan_dp_gm_steps, fw_service_budget).

## Run history (CET)

- 03:41 resume; head d539f162, clean. 03:4x dev-soft-core 70f4056f fetched; the merge started (--no-ff --no-commit);
  nine conflicts resolved; the per-shape keying; tools; docs.
- 03:5x checks on the working tree: shape_costs 25/25 and PASS, flip 612/612 and 1x1/1if PASS, rows_tiers 1033/1033,
  load 28/28 and --check (1x1/1if 0.517 / 0.514 of 0.70; 8x8/1if 0.715 / 0.674 at the stated costs), record classes
  14/14, egress_ledger 13 mutants, docs_check 0, py and cpp idiom; the images (above). Commit d1c9023b.
- 03:59 the measurement on a clean clone of d1c9023b (launchM.py, eight legs: arm A in four parts, the
  answering-every-port arm, the answering-ports arm's aecp, aecp-fanout and aecp-largest-notice, the
  valid-destinations arm, the transmit-aged control; on picked ranges or the session's CPUs, at most 4 there).
- Scratch: round 6's final-pass clones (4.1 GB) removed, their logs kept; 5.9 GB before the legs.
- 04:00-11:26 the legs (A0's save-second the last); 11:1x the survey over the finished legs; 11:2x-11:4x the gate
  (gate_r8.py: SRP's Talker rows held to their own budget), the full survey, the restatements; 11:49 commit 84c1704d.
- 11:50 the regrades refused (another checkout path), stopped by unit name; 11:51 relaunched from r8/cH moved to
  84c1704d: every leg rc 0; the gate fails on the ledger alone.
- 11:58-12:11 the record classes over (long, paced), restated with THE TRANSMIT's figure at 70 ms; 12:11 commit acfa5601; the
  images identical to the measured; plat_ledger (first run on a wrong path, rc 2, rerun: PASS); quick checks 18/18.
- 12:1x receipts, STOP-COMMENT.md, PR-BODY.md, the index; the STOP posted once on #894.
- Slips: a clone given a hand-built full SHA (wrong) failed and was redone with rev-parse; plat_ledger's first run
  named the wrong directory; neither touched any result.
- 12:1x the STOP posted once on #894 (issuecomment-6914891355); the posted text equals the file but for one trailing
  blank line. Nothing pushed; no PR created or edited.
