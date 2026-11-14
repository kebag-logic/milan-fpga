# HANDOFF (round 4) — [A775] lane 895

**Status (11:15 CET 2026-11-14): STOP, posted once on #895: issuecomment-6875758968 (its body equal to STOP-COMMENT.md).** Head `91c3fc0e` (local, not pushed): two sync merges, of #902's head
`5b264bf2` (`a93fceae`) and, after `894-tiers` moved during the round, of its new head `7398ec0a` (`91c3fc0e`). The
composed 1x1/1if flip check fails, and the 8x8/2if platform image plans 60.5 RAMB36 against its 60.0 entry. Both need a
decision (section 3). With the legs' measured costs fed in by section 13's rule the flip check fails further, and
three stated costs move past their statements at 1x1/1if (section 2): the assignment's #909 condition.

New assignment (round 4), not a resume. Round 3 ended in the second STOP at `9e30c2c3` (issuecomment-6864607963),
answered by issuecomment-6864645058 (hold until #902 merges, then a sync round). The manager starts this round on
#902's head `5b264bf2`, not yet merged (PR #902 OPEN all round; its head `7398ec0a` from 07:55 CET).

- Worktree $LANES/895-talker, branch `895-talker-redeclare` (PR #901, base dev-soft-core), not pushed.
- Scratch: /data-2/milan/tmp/895-a775/r4 (T = clean clone of `5b264bf2`; L = clean clone of `a93fceae` the legs ran
  on; G = scratch clone for the fed grading; merge/, grade/, feed/, ledgerM, ledgerM2, ledgerT, units/). Legs under
  /data-2/milan/tmp/895-a775/{builds,legs}/R4-* and T4-* (#902's head).
- Rulings read: #895 6857334948, 6864645058; #894 6867990126 (bounds 49 / 238 ms, the join gate 181-239 ms),
  6867393730 (d), 6870437042 (round 9: the pace rule, item 4), 6871343905 (8x8/1if lane; the held-egress rows),
  6844175391 (item 2: the 59.0 fixture fallback "the final composed fixture or harness image"; STOP trigger "the
  8x8/2if platform image over 60.5"); the owner's decision 6824896581 (platform may plan 60.0, cap 60.5).

## Items

| Item | What | State | Commit | Evidence |
|---|---|---|---|---|
| 1 | sync: merge origin/894-tiers at `5b264bf2`; again when it moved | done: two merge commits | `a93fceae`, `91c3fc0e` | section 1 |
| 2 | CPU-budget harness at every point against the merged figures | done at `a93fceae` (1x1/1if, 8x8/2if; 8x8-1if not run, lane 894b's) | | section 2 |
| 3 | acceptance 4 composed: flip_grade --check --point 1x1/1if; ROM ledger | **FAIL** (flip) and **platform refused at 60.5**: STOP | | section 3 |
| 4 | SPLIT_CONTROL_MEMORY.md section 13, PR body figures; #906, #907 pre-existing | section 13 not restated (waits on the decision); PR-BODY.md for round 4 | | |
| 5 | gates; full pass once at the final head on a clean clone | not run (the STOP) | | |

## 1. The sync merges

**`a93fceae`** (parents `9e30c2c3`, `5b264bf2`; merge base `084cf7a8`). Submodule pins identical. 85 files from #894.
#894 does not carry the names patch (C4-names.patch); this branch carries it once (`a9fd4415`). 8 conflicted files:

| File | Hunks | Resolution |
|---|---:|---|
| `sw/firmware/ctrl/srp/srp_mbx.c` | 1 | #894's `SRP_JOIN_CS CTRL_LOOP_JOIN_CS` (19 cs) and #895's `SRP_REDECLARE_CS` after it; its comment names `CTRL_LOOP_TX_MS` as the built design's MRPDU by every source (rows_tiers.py holds it), no longer "THE TRANSMIT's bound" (now `CTRL_LOOP_TX_BOUND_MS`). 2,022 cs at 1x1/1if (was 2,023), 2,029 at 2if |
| `sw/firmware/ctrl/aecp/aecp_shape.py` | 1 | #894's `*key_domain(blob)` on the constants line and the names patch's `AECP_ENTITY_NAME_RUNS`, tuple ordinals, `AECP_ENTITY_NAME_RUNS_INIT` |
| `sw/firmware/gtest/coverage.ratchet` | 2 | measured on the composed tree (`fw_coverage.py --write`, unit covM): `srp_mbx.c` 736/736, 663/663 (#895 725/651, #894 674/589); every file 100 %; also records #894's aecp.c 615/538, aecp_maps.c 267/336, aecp_mbx.c 136/74, ctrl_plat.c 134/42 as measured |
| `sw/litex/ctrl_memory.py` | 1 | #894's 59.0 entry and reason, then "; SRP's Talker declarations plan within it (#895)" |
| `sw/litex/ctrl_memory_ledger.py` | 1 | `ctrl_plat` as plat_ledger.py measures the composed images: 17,536 / 19,072 / 18,176 / 20,352 |
| `tb/verilator/ctrl_service_budget/load_grade.py` | 2 | no key changed by both sides from `084cf7a8` (merge/tables3.py): each key the side's that moved it, so #894's tables with MAAP's record #895's (115 at 1x1/1if, 150 at 8x8/2if, both columns); comments both sides', "on its merge with THE TIERS (#894) each cost the one of the side that moved it from their merge base 084cf7a8" |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | 2 | #894's 59.0 row and paragraphs, `ctrl_plat` 20,352 B, and #895's sentence restated with the measured sizes (+64 B at two interfaces only, on the tiers' image) |
| `sw/firmware/ctrl/plat/README.md` | 2 | both sides' text with the measured plan: "plans 60.5 RAMB36 ... 184 B of `rom` past the 60.0 its entry ledgers ... which refuses its link until that entry or the image is decided (#895)" |

Semantic conflict, resolved in the merge: #894's `ctrl_transmit_fn (void *ctx, unsigned most)`; `srp_talker.cpp:518`
(`TransmitPublishesWithinItsTermsAfterARefusedJoin`) now `do loop.transmit(loop.transmit_ctx,CTRL_LOOP_BUILD_MOST);
while (adapter.tx_resume!=0u);` (the call as the loop makes it and the slices that resume its build, so the counts stay
the build's); `srp_talker.cpp:571` (`RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt`) passes `CTRL_LOOP_BUILD_MOST`
(refused at its first MRPDU, nothing resumes). Found by armsM (compile refusal); armsM2 PASS.

Anchors (round4/scripts/anchors3.py, each module's literals against its own lineage's files): no real anchor broken
(10 hits, generic literals of modules both sides changed).

**`91c3fc0e`** (parents `a93fceae`, `7398ec0a`; merge base `5b264bf2`). `894-tiers` moved during the round (seen
10:3x): `55b8e621` (the map table's declared slots), `947bd389` (section 13 docs), `7398ec0a` (docs). One conflict,
`SPLIT_CONTROL_MEMORY.md` section 13: #895's two paragraphs kept, then #894's relabelled intro of the load table ("At
the merge of dev-soft-core 0fb66211, round 30's legs"), replacing #895's stale "At this head". Checked on the worktree
before the commit: ledger identical to `a93fceae`'s (ledgerM2); flip identical (rc 1, txL 49.20); `fw_coverage.py
--check` PASS (39 files); `aecp_arms.py --core` 83 tests PASS; arms unit, talker PASS.

## 2. The harness at `a93fceae` (clean clone L), against the merged figures

| Point | Arm | Groups | Refusals | Budget misses | Passes over the share | rc |
|---|---|---:|---:|---|---|---:|
| 1x1/1if | A (5 parts, merged) | 96 | 0 | 7 of 950 (backlog-owed's held-egress seven) | 0 of 134,749 | 0 |
| 8x8/2if | A (5 parts, merged) | 94 | 0 | 7 of 994 (the same seven) | 0 of 230,855 | 0 |
| 1x1/1if | answering-every-port | 16 | 0 | 0 of 280 | 0 of 20,903 | 0 |
| 8x8/2if | answering-every-port | 16 | 0 | 0 of 736 | 0 of 16,050 | 0 |
| 1x1/1if | valid-destinations | 2 | 0 | 0 of 5 | 0 of 2,668 | 0 |
| 8x8/2if | valid-destinations | 2 | 0 | 0 of 20 | 0 of 3,053 | 0 |
| 1x1/1if | B (aecp) | 1 | 0 | 0 of 25 | 0 of 112 | 0 |
| 8x8/2if | B (aecp) | 1 | 0 | 0 of 39 | 0 of 140 | 0 |

- No `STATED` line in any leg. The 1x1/1if valid-destinations leg (round 3's STOP) passes: its longest THE TRANSMIT
  build 48,103 cycles against 725 us (72,500).
- Join intervals: 1,091 in 227 group runs, 185.905 to 190.192 ms; every leg within 181.0 to 239.0.

**Measured costs at 1x1/1if** (round 1's parsers, scripts/costs, over every 1x1 leg; arm A without
aecp-largest-notice for the ordinary record, feed/noL): against the composed tables, three over: `event.AECP` 6,805
cycles (75 us by the rule; stated 65), `event.TICK` 4,385 (50; 45), `record.aecp` 28,173 in `aecp-fanout` (300; 235).
MAAP's record 9,536 (105; 115 stands by the rule).

Like for like with #902's head:
- #894's final-pass groups at `5b264bf2` (its own legs H-L1N, H-L1A, H-J1, H-L1L, H-L1O, read-only) and the same
  groups at the merge, the same parsers (feed/same): no cost dearer at the merge beyond the noise (e.g. event.AECP
  4,660 vs 5,839; record.aecp's largest-notice 92,046 vs 91,625, 970 vs 965 us, within the 975).
- `notice-burst-1` (answering-every-port) at #902's head (leg T4-N1 on T): AECP's timer slot 6,188 cycles (65 us,
  at its statement) vs 6,805 at the merge; the difference is in `aecp_mbx:event` (3,469 -> 4,196), whose code #895
  does not change (the names patch's `aecp_nvm.c` runs on the save path and a name change only): the data-cache
  placement (#909), not traced.
- `backlog-adp@blank-0` (arm A) at #902's head (leg T4-A1): the TICK 3,241 vs 4,385 at the merge; the merge's dearest
  TICK carries AECP's work (`aecp_mbx:event` 1,310, `aecp:transmit` 360), #902's none: the event's composition
  moved, not the same work dearer.
- `aecp-fanout` at #902's head (in-session run on T4-A1's build): an AECP record 27,851 cycles (295 us) vs 28,173 (300) at the merge: the 300 over the table's 235 is #902's own image's too (by these parsers), not this composition's.
- The AECP timer event's pass, both heads (PASS lines): 26,404 vs 26,477 cycles, 4,234 vs 4,321 instructions, instruction refills 106 vs 119 (8,705 vs 9,835 cycles); `aecp_nvm` 146 vs 143 in it: code layout, the instruction side of #909's sensitivity, not traced to a function.
- 8x8/2if (reported): over the composed table, event.AECP 115 (105), event.TICK 55 (40), events_none 35 (30), record.maap 155 (150); not compared with #902's head.
- Fed gradings (clone G, restored each time): the composition's moves alone (MAAP 115, AECP slot 75, TICK 50): txL 49.46, tx 33.20, pace rule 9 (txL 47.86, R4L 203.48); with the AECP record 300 too: txL 53.53, last 135.85, ACMP 33.64, pace 10 and last/ACMP over at any pace.

## 3. The STOP

Analytical graders (grade/):

| Check (1x1/1if) | #902 `5b264bf2` | composed | fed with the merge's legs |
|---|---|---|---|
| `flip_grade.py --check` | PASS: txL 48.09, tx 29.86, last 126.46, ACMP 28.44 | **FAIL**: txL **49.20**, tx **33.01** (CTRL_LOOP_TX_MS 30), last 126.78, ACMP 28.66 | **FAIL**: txL 53.53, tx 36.63, last **135.85** (130), ACMP **33.64** (30), ADP 29.27, MAAP 29.37 |
| `tier_grid.py` | 900 us chosen, 18 of 420 | **0 of 420** | |
| `load_grade.py --check` | 0.513 / 0.509 | 0.514 / 0.510 | 0.528 / 0.510 |
| `paced_rows.choice` | 8 ms | 9 ms (txL 47.60, R4L 203.44) | 10 ms (txL 48.42, R4L 218.48), but last and ACMP stay over |

Cause of the composed failure, isolated: #902's tree with only the composed `load_grade.py` gives the same 49.20 / 33.01;
the tables differ only in MAAP's record (#895's round 2 measurement, 115 us at 1x1/1if; #902 90). Scratch: pace 9 and
CTRL_LOOP_TX_MS 34 pass the unfed check (txL 47.60, tx 33.01 / 34, R4L 203.44).

ROM (ledgerT on #902's clean clone, ledgerM on the merged worktree, ledgerM2 on the second merge: identical):

| Image | #902 `5b264bf2` | composed | delta |
|---|---|---|---:|
| platform 8x8/2if | 130,504 / 114,160, 60.0 | **131,256 / 114,224, 60.5: REFUSED** (184 B past 131,072) | +752 / +64 |
| fixture 8x8/2if | 125,368 / 113,168, 59.0 | 126,112 / 113,232, 59.0 (864 B left) | +744 / +64 |
| arm answering-every-port | 125,676 / 113,232, 59.0 | 126,420 / 113,296, 59.0 (556 B left) | +744 / +64 |
| arm valid-destinations | (none) | 126,280 / 113,232, 59.0 (696 B left) | |
| platform 1x1/1if, 1x1/2if, 8x8/1if | 42.5, 43.5, 56.0 | 43.0, 43.5, 56.0 (1,352 B left) | +1,352, +1,608, +512 |
| fixture 1x1/1if, 1x1/2if, 8x8/1if | 40.5, 41.5, 54.0 | 41.0, 42.5, 54.5 | +1,352, +1,600, +504 |

## 5. Gates

Not run (the STOP). Checks run this round:

| Check | Command | Result | Receipt |
|---|---|---|---|
| firmware arms on the merge | round4/scripts/arms.py unit talker maap maap_if2 acmp acmpif2 srp-acmp-if1 srp-acmp-if2 platboot | PASS (armsM2) | fw/armsM2.log |
| coverage | fw_coverage.py --write (a93fceae), --check (91c3fc0e) | written; PASS 39 files | fw/covM.log, fw/cov-merge2.log |
| AECP core | aecp_arms.py --core (91c3fc0e) | 83 PASS | fw/aecpcore2.log |
| ledger | round4/scripts/ledger.sh | plat_ledger FAIL (8x8-if2 60.5) | ledger/ |
| flip / grid / load | flip_grade.py --check --point 1x1/1if, tier_grid.py --point 1x1/1if, load_grade.py --check | FAIL / FAIL / PASS | graders/ |
| harness | run.py at 1x1 and 8x8, every arm | section 2 | legs/ |

## Changes (file:line, reason)

In section 1 (the merges): `srp_mbx.c:28-35` (the composed JoinTime and hold-off), `aecp_shape.py:105-108`,
`srp_talker.cpp:518-519` and `:571` (the tiers' `most`), `load_grade.py` tables and comments, `coverage.ratchet`,
`ctrl_memory.py` (reason), `ctrl_memory_ledger.py:35` (measured `ctrl_plat`), `SPLIT_CONTROL_MEMORY.md` (section 2
table, ctrl_plat sentence, section 13 intro), `plat/README.md:110`, `:135` (the measured 60.5 plan).

## New checks (planted mutant, failing words)

None this round (no behaviour change; the merges compose both sides').

## Run history

- 07:24 assignment read; skeleton written. Rulings read. 07:2x fetched: `894-tiers` `5b264bf2` (PR #902 OPEN),
  dev-soft-core `cec88385`, inside 894-tiers.
- 07:2x merge started (--no-commit); 8 conflicts resolved.
- 07:30 ledgerM and armsM on the worktree; armsM rc 1 (srp_talker.cpp compile); fixed; armsM2 PASS.
- 07:3x anchors3.py; ledgerT on T; covM (`--write`). Flip, tier_grid, load on both trees; cause isolated; the pace
  option in scratch.
- 07:42 `a93fceae` committed; clean clone L; 07:44 legs R4-* (legs_r4.sh, tick_r4.sh, wait_r4.sh; arm A in five
  parts a point); the host mostly booked by other lanes, the legs started as 8-wide ranges freed (to 09:20).
- 09:30 1x1/1if arm A merged (merge.py), rc 0; feeds; same-group comparison with #894's own legs at `5b264bf2`.
- 10:0x-10:2x legs T4-N1, T4-A1 at #902's head (clone T) for the dearer inputs.
- 10:3x `894-tiers` at `7398ec0a`: second merge, checks, `91c3fc0e` committed 10:5x.
- 10:5x a release hold collecting CPUs: picks hand out nothing; `aecp-fanout` at #902's head run inside the session.
- 11:0x the fed 1x1/1if gradings (clone G, restored); aecp-fanout at #902's head; 8x8/2if arm A merged rc 0;
  8x8 feed. 11:1x receipts, INDEX.md, the STOP comment.
- 11:14 the 8x8 feed's last step (aecp_kinds.py, the AECP kinds at 8x8; costs.txt already written and used) stopped
  by me: PIDs 346780, 257607, 257602, 257584, each listed with its arguments first, all under this lane's scratch.
- 11:15 STOP posted once on #895 (issuecomment-6875758968). `894-tiers` still `7398ec0a`, dev-soft-core `cec88385`,
  #902 OPEN. No unit of this lane runs. Nothing pushed (the remote branch stays at `18300f6e`).
