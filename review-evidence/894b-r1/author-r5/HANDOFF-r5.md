# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 5, [A781]

Status: STOP to the maintainer at `0700f09e` (comment text `STOP-COMMENT.md`, posted once on #894 as issuecomment-6892905117): four held-egress
rows over their ledger figures on #902's merged code. PR text `PR-BODY.md`. Nothing pushed.

- Start head: 98c0b62b (round 4's REVIEW READY; R843-2 and R844-2 POSITIVE there), tree clean, verified 07:42 CET.
- Task (manager, round 5): sync onto origin/894-tiers 234bc149 (#902 round 13's review head), re-measure 8x8/1if on
  the merged images, survey every stated table by the rule, final pass, then one REVIEW READY or one STOP on #894.
- Rulings read: #894 6890460677 (#902's round-13 REVIEW READY), 6883864236 (round 12), 6886633874 (the SRP drain),
  6888782796 (round 13); round 4's reviews 6888161058 (R843-2) and 6888161829 (R844-2), their residues.
- Scratch: round 3/4 leftovers deleted first (round 4's lane-c store temp, 7.7 GB; round 4's image dirs).

## Items

1. Sync (merge 234bc149). — DONE: `647d5c4a` (merge), `b2737ba5` (8x8/1if's SRP drain limit), `a15345f7` (residue
   wording). Seven conflicts resolved; #902's interface-keyed one-interface figures go to THE SHAPES' (1,2,2) block.
2. Re-measure 8x8/1if; survey every stated table; restate by the rule; rows by every source; load; joins; rounds;
   held egress by egress_ledger.py. — DONE: every criterion holds but the ledger (STOP); three survey findings, two
   restated (`d09494c4`), one left for the decision; 8x8/1if's record classes held at its own statements (`1a0fedad`).
3. Final pass on clean clones. — NOT RUN: the STOP ends the round (item 4); scripts ready (lane_gates_r5.sh,
   mkqueueR5.sh); quick checks on the clean head pass (receipts/gates/quick-checks-0700f09e.txt).
4. STOP posted once on #894.

## Changes (file:line, reason)

**The merge `647d5c4a`** (#902's 25 commits `7398ec0a..234bc149`: the one-row edit cut, SET_CONFIGURATION's cut and
pace stamp, the paced class, the SRP drain limit at the load gate's record.srp, four 1x1/1if restatements, the slice
rule's 950 us at one interface):
- `ctrl_loop.h`: THE SHAPES kept; the (1,2,2) block takes #902's one-interface figures (slice 950, build of one 735,
  SRP unit 280; build of both 1010 and THE RETRY 85/34 unchanged). #902's `(MBX_N_IF == 1u ? ...)` defines of the
  slice, the SRP unit and the builds are not taken: keyed on the interface count they would give 8x8/1if 1x1/1if's
  figures (slice 950 under its measured build of one, SRP unit 280 under its measured record). 8x8/1if keeps its own.
- `load_grade.py` `srp_unit` and its controls: #902's reader took the first `#define CTRL_LOOP_SRP_UNIT_US`, which
  in THE SHAPES is the (1,2,2) block's, so it read 280 at 8x8/2if; now each point's figure is read at its shape
  (`shape_costs.at`) and the plants are made in that point's block (`unit_planted`).
- `poll_grade.py`: the shape-keyed table kept; #902's ACMP restatements taken (55 at 1x1/1if, 70 at two interfaces).
- `rows_tiers.py`: my point-keyed `built_constants` kept, with `edit_rows` imported beside `shape_costs`; the slice
  rule's control plants the (1,2,2) block at #902's 600 us.
- `selftest_round.py`: #902's check (the slice rule's choice at 1x1/1if), my 8x8/1if slice lines kept.
- Docs: section 13 keeps both #902's new sections and THE SHAPES section (its (1,2,2) row at 950/735/280); the SRP and
  harness READMEs take the 950 us.
- Checks at the merge (worktree): load --check 0.516/0.512, load 26/26, rows_tiers 1033/1033, flip 611/611, shape
  table PASS, record classes 11/11, tier_grid chooses 950 us, docs_check 0, idiom gates 0.

**`b2737ba5`:** 8x8/1if's SRP drain limit at the load gate's record.srp there, 365 us (its records are 8x8/2if's,
NEAREST), by #894's drain ruling (6886633874), which holds it so at the other points; 345 us, its own measured record,
was under that statement, the defect class the ruling names. `load_grade.SRP_UNIT_POINTS` gains 8x8/1if (`stated`,
NEAREST), with a planted control at 345 refused naming 8x8/1if (#902's interface-keyed 280 also refused there).

**`a15345f7`:** round 4's residues RES1 (egress_ledger.py:42 and the first mutant's name) and R844-2-R1 (aecp.h's
guard sentence), wording only.

**`1a0fedad`:** `edit_rows.py:38-46` 8x8/1if's paced class (one-row edit 320, accepted SET_CONFIGURATION 635 us, the
measured 30,277 and 60,027 cycles), `point_of` (:50) keyed on the shape (interfaces, sinks); `rows_tiers.py:134`
LONG_RECORD_US 8x8/1if 1,510 us (143,648 cycles), its comment folded to keep the module at 1,000 lines (the idiom
gate's limit); `record_classes.py` 8x8/1if's legs held at its own statements (`statements` reads record.aecp through
`load_grade.stated`, NEAREST), completeness at each held point (`COMPLETE`, `LABELS`), two controls (13 of 13).

**`25c782a4`:** R843-2-S1 taken: `egress_ledger.run_refusals` (a results directory's `results.json` required, its
refusals fail), two controls, one mutant (9 of 9); the harness README for both tools.

**`d09494c4`:** `poll_grade.EIGHT_ONE` walk 55 and aecp 145 us by the rule (4,905 and 13,572 cycles).

**`0700f09e`:** section 13 (THE SHAPES' 8x8/1if SRP 365, the record classes, the two polls) and FR_NFR 3.4.1.

## Measurement (8x8/1if, on a15345f7's image)

- Images: the six fixed images byte-identical to #902's 234bc149's (fixture and platform at 1x1/1if, 1x1/2if,
  8x8/2if), by ELF and loadable sha256 on clean clones of both; platform-8x8-1if 56.0 RAMB36 (rom 129,624 of 131,072).
- Probes (08:0x-08:28): `srp` (arm A): build of one 138,906 cycles, 1,460 us by the rule, under 1,475; answering-every
  -port (16 groups): rc 0, no STATED line, 0 budget misses, 0 over THE SHARE; arm B `aecp-fanout` and
  `aecp-largest-notice`: rc 0, no STATED line; one pass over THE SHARE (202,546, the largest legal command, reported
  at 8x8/1if as before). So no firmware statement moves; the measurement runs on this image.
- Probe survey (`survey_r5.py`): the notice item 13,572 cycles, 145 by the rule, over EIGHT_ONE's 140; the walk 4,905,
  55, over 50; the long notice 315 within 320. Restated at the end over every leg.
- Not in the tree: `valid-destinations` is #895's arm (`895-talker-redeclare`), not #902's 234bc149.

## The STOP test's reading

The rows by every source at 8x8/1if stay over their bounds, as reported since round 1 (owed to #872): on the merged
tree R5 114.69, R6 109.50, the last queued notice 277.05, ACMP 45.87, ADP 45.85, MAAP 46.55, tx 59.03 and txL 147.39
ms (before restatement). The shape ruling (b) and the held-egress ruling (a) make 8x8/1if's trigger a measured
CPU-decided row over its bound or the load over 0.75, and FR_NFR 3.4.1 reports those rows. The STOP list's "an
8x8/1if CPU-decided row over its bound by any source" is read as a measured row of any arm; the reading is published.

## Measurement result (on a15345f7's image; the head carries it, no firmware change since)

- Legs: M-A0..M-A3 (arm A, 95 groups), P-AE (16), P-B (aecp-fanout, aecp-largest-notice), M-Ba (aecp); M-CTA control
  caught 8 of 8; P-srp probe. 114 groups, 1,717 instances, all measured, every leg rc 0, no STATED line, no refusal.
- Measured rows: AECP 4.860, ACMP 7.231, ADP 6.014 (ENTITY_AVAILABLE 4.629), MAAP 6.255, SRP 10.474, MRPDU 4.114,
  notices 2.168, first queued 2.812, last queued 26.636, largest command 2.547 ms: each within its bound.
- Joins 352 in 113 groups, 187.397 to 190.147 ms; slices SRP 142,809, build 138,906, round 92,744 (147,500); THE RETRY
  2,453,084 rounds, 0 over; load 0.711 / 0.672 (0.75); one pass over THE SHARE (aecp-largest-notice, reported).
- **The ledger: FAIL** (receipts/harness/gate-8x8-1if-a15345f7.txt, ledger-8x8-1if-a15345f7.txt): owed_behind1
  63.73898 (63.69), owed_behind2 63.95746 (63.91), service.acmp.last 62.18386 (62.18), service.aecp.last 61.84625
  (61.83); the other three within. The attribution leg on 647d5c4a gives the same seven to the microsecond
  (receipts/harness/attribution-backlog-owed-647d5c4a.txt): #902's merged code, not this round's commits after it.
- Record classes PASS at 8x8/1if's statements (long 1,510, paced 635, other 265). Survey: notice item 145 > 140 and
  walk 55 > 50 (restated); ADP record 130 > 125 (the #32 column, NEAREST): for the decision (load 0.6720 -> 0.6725).
- Rows by every source (reported): R4 19.82, first 17.83, R4L 192.81 within; R5 126.36, R6 118.28, last 325.90, ACMP
  48.37, ADP 48.33, MAAP 49.03, tx 67.24, txL 134.96 over (owed to #872).

## Gate table (at 0700f09e: quick checks on the clean worktree; the final pass is not run, by the STOP)

| Check | Result | Receipt |
|---|---|---|
| egress_ledger --selftest; record_classes --selftest; shape table; load --selftest/--check; flip --selftest and both points; rows_tiers --selftest; tier_grid; py/cpp idiom; docs_check; diff checks vs 234bc149 and 98c0b62b | all rc 0 | `gates/quick-checks-0700f09e.txt` |
| gate_r5.py controls | 21 of 21 | `gates/gate-r5-controls-0700f09e.txt` |
| Images at a15345f7 against 234bc149 (clean clones) | six fixed identical; 8x8/1if platform 56.0 | `images/` |
| The 8x8/1if gate | FAIL (ledger) | `harness/gate-8x8-1if-a15345f7.txt` |

## Run history (CET)

- 07:42 start; 07:4x scratch cleaned; rulings and reviews read; 07:5x merge, conflicts resolved, checks; commits.
- 07:5x images (both heads); 08:0x probes; 08:29 arm A (4 parts), arm B's `aecp`, the transmit-aged control queued
  (launchM.py; four on picked ranges).
- 08:3x-10:50 grader work beside the legs: record_classes 8x8/1if, edit_rows, survey tools (`survey_r5.py`,
  `compare_8x8_1if.py`, `costs_r5.sh`), gate_r5.py and its controls (21/21), R843-2-S1 in egress_ledger (9 mutants).
- 10:50 arm A complete; the gate FAILS on the ledger (four rows); 10:50-11:02 the attribution leg (backlog-owed on
  647d5c4a): identical rows. 11:0x the survey (as its own unit; it outran a foreground command); restatements;
  commits 1a0fedad, 25c782a4, d09494c4, 0700f09e; receipts; STOP comment, PR body, index; 894-tiers found at 4ae887a1 (eight commits on 234bc149: CTRL_LOOP_TX_MS at
  two interfaces 98 -> 99 ms and documents; not merged, the manager relays), noted in the STOP; STOP posted once
  (issuecomment-6892905117). Nothing pushed; no PR created or edited; no merge beyond the instructed sync.
