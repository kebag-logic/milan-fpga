# 894-a773: #894 round 8, HANDOFF

**Status: REVIEW READY at the final head `dd01b0afef87037ec485cd49b40a26b542854bdd`**, posted 03:21 CET 2026-11-14 as #894 issuecomment-6870102413 (text: `REVIEW-READY-COMMENT.md`; PR body for round 8: `PR-BODY.md`, not applied: no PR edits this round). The full pass at the head is clean (section 8). 1x1/1if holds every row by every source under the egress ruling; no STOP trigger fired.

- Start head `8a3791e44533d6b1cc26d486d0b18e7d83470dc1` (round 7's REVIEW READY, issuecomment-6867318907).
- Authority: the ruling #894 issuecomment-6867990126 (round 8; source comments call it "#894's egress ruling of 2026-11-13"). Read with it: R837-2 (PR #902 issuecomment-6867959154), R838-2 (issuecomment-6867751113) and its probes, the 894b step-1 table (issuecomment-6867451690), the ruling 6867393730.
- Nothing pushed. No TAKEN posted.

## 0. Exit (at `dd01b0af`; rows and images equal at `197012aa`)

1x1/1if, `flip_grade.py --check --point 1x1/1if`: RESULT PASS.

| Row | W, ms | Bound | Was (r7) |
|---|---:|---:|---|
| R4 | 12.82 | 20 | 12.82 |
| R4L (paced) | 173.37 | 238 (was 240) | 158.34 at P 6 |
| ACMP | 28.35 | 30 | 28.35 |
| ADP | 26.76 | 30 | 26.76 |
| MAAP | 26.88 | 30 | 26.88 |
| first | 14.50 | 20 | 14.50 |
| R5 | 72.71 | 90 | 72.71 |
| R6 | 68.62 | 90 | 68.62 |
| last | 125.84 | 130 | 125.84 |
| tx | 29.78 | 49 (was 50) | 29.78 |
| txL | 47.98 | 49 (was 50) | 49.99 at P 6 |

- Pace 7 ms (`paced_rows.choice`); slice 900 us (`ruled`, least margin +0.021); queued bound 130 (no statement); load 0.513 / 0.509.
- No STOP trigger: P 7 holds (STOP only if none up to 11); last 125.84 within 140; no image over its cap (section 3); no map-command behaviour change (definition test unchanged and passing, 21 plants caught); the collision case's pass 96,142 cycles at 1x1/1if, under THE SHARE's 200,000.

## 1. Item 2: the pace count (`8ba93f26`)

- `paced_rows.py` `edits(w, P)` = ceil((w + 1) / P) in integer hundredths; `record` uses it. Reason: the gate (`aecp_mbx.c:154-158`) compares whole ms; the stamp is a fresh read (`aecp.c:31-37`, `now()`), the gate's clock never ahead of it, so floor(t[k+1]) >= floor(t[k]) + P.
- `gate_most(w_us, P)`: the gate simulated by its own arithmetic (first take at the ms's last us). `count_findings()`: edits == gate_most for every window 0.01..120 ms step 0.01 and P 1..13; it runs in the flip check (`flip_grade.row_findings`).
- Controls (`paced_rows.count_controls`, names in `paced_rows.CONTROLS`, which `rows_tiers.CONTROLS` splices): "THE PACE's edits not the gate's count"; "THE PACE's edits counted 1 + floor(w / P)": the earlier rule planted must be named by count_findings and must shorten txL at some P and lengthen it at none.
- Table re-solved: `receipts/model/pace-table-P1-13.txt`. Column A (the start head's inputs, bounds 50/240) agrees with R837-2's probe column for every P (P 4 66.50, 8 47.73, 9 47.03, 11 44.96).

## 2. Item 1: T_egress counted (`96565297`)

- `ctrl_loop.h`: `CTRL_LOOP_T_INGRESS_MS 1u`, `CTRL_LOOP_T_EGRESS_MS 1u` (FR_NFR 3.4.1's table); `CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS - CTRL_LOOP_T_EGRESS_MS)` = 49. Read only by `ctrl_loop.c:203`'s static assert, so no image moves.
- Model: `tier1_rows.allowance`, `tx_budget_ms`, `built_value` parses the new derivation; `rows_tiers.TX_BUDGET_MS = tx_budget_ms(...)`; `paced_rows.PACED_BOUNDS = {'R4L': 240 - T_ingress - T_egress}` = 238, `choice` and `statements` read it.
- Harness: `join_grade.LEAST_MS, MOST_MS = 180 + T_egress, 240 - T_egress` = 181.0, 239.0 (`WIRE_MS` stays 180/240 for the bench).
- Controls: `rows_tiers.channel_controls` plants the bound typed 90u and the egress-free `(240u - 10u * CTRL_LOOP_JOIN_CS)`, each refused by `tx_statements` ("CTRL_LOOP_TX_BOUND_MS states 50 ms, not the timer budget's 49"); `flip_grade.channel_controls` pins 49 and 238; selftest plant "joins: the wire's 180.0 to 240.0 ms held at the commit, T_egress uncounted" caught by "a join interval is two MRPDUs ... 181 and 239 ms ... hold".
- FR_NFR 3.4.1: R4L paragraph (238), the MRPDU paragraph (49, the 181.0 to 239.0 gate, the bench's 180 to 240), lines 424-426 (the split's 49 + 1 = 50 ms), each citing the egress ruling.
- `ctrl_configs.OUTSIDE`: `join_grade.py` added; `rows_tiers.py` and `paced_rows.py` reasons updated.

## 3. Item 3: map commands (`6c232270`, `44f897ab`, restated in `197012aa`)

- `aecp_maps.c`: `legal()` (geometry, reads nothing) and `idle()` (the output port's stream read); `topology()` removed (`valid()` calls `legal()`). The decode checks `legal()` per mapping and ends the table at the first illegal one (`ILLEGAL`), as an ADD's `EARLIER` does: that mapping's turn refuses the edit before its port is read, so status, reads and precedence are unchanged. One slot a key (`place`); a REMOVE's other values of a key are linked from the key's first (`next[]`); a map row's lookup walks its key's values (`look`). Hash: stream or cluster + 9 x channel (key words are little-endian): distinct for one stream of up to 256 channels or up to nine streams/clusters of up to 28 channels. `AECP_MAP_WORK` (test-only) counts each slot and held mapping visited; no image counts it.
- Images: +176 B rom each, tiles unchanged (section 8).
- Tests: `Core.MapEditsAreTheirDefinitionRowForRow` unchanged, passing. New `Core.MapKeysThatShareASlotAreTheirOwn` (channels 0 and 256 share a slot). New work arm (`aecp_arms.py` mode `work`, `-DAECP_MAP_WORK`, in `all_arms`): `Core.MapEditWorkIsLinearInItsMappings`, six cases at 8, 16, 32 and 63 mappings, work <= 2 (n + R), collisions < n(n+1)/2.
- Counts (`receipts/item3/work-counts-new.txt`): at 63, the collision of one key's values 127 visits (bound 128), from distinct streams 3; the start head's table (`work-counts-start-head.txt`, match()'s walk counted) 2,080 in both, refused.
- Plants (`aecp_map_mutants.py`), all 21 caught (`receipts/item3/map-plants.txt`): re-anchored map-table-key-unchecked (now caught by the slot-sharing test), map-value-cluster-channel-ignored, map-add-stops-early, map-checked-before-its-read, map-remove-every-copy; new map-illegal-ends-early, map-illegal-unflagged, map-remove-values-rewalked (tail-append walk: 38, 138, 530, 2,018 = n(n+1)/2 + 2, refused at all four, "not under n(n+1)/2"), map-hash-the-stream-alone ("past twice their sum"). `aecp_mutants.campaign` runs a WORK test in the work arm.
- Harness: `long_notice.py` `refused_edits`: collision_indices (REMOVE, distinct first-field indices, the row's key), collision_values (REMOVE, the key's legal values in turn), conflict_last (ADD, the row 62 times then its key with another legal value), each 550 B, BAD_ARGUMENTS.
- Re-measure (`r8/builds/L1L`, `L8L`, `81L` at `44f897ab`): 1x1/1if records REMOVE 92,766, ADD 86,504, collision_indices 23,014, collision_values 78,262, conflict_last 79,281 CPU cycles; their passes 150,004 / 140,498 / 41,545 / 96,142 / 97,172, all under 200,000. 8x8 142,634 (1,500 us by the rule; 1,555 kept). 8x8-1if 151,629 (1,595, reported).
- Restated `LONG_RECORD_US['1x1/1if']` 940 -> 975 us.

## 4. Item 4: the join grader (`b6b94d92`)

- `mrpdu_grade.resolve(log, entry)`: no horizon (`LOOK_MS` removed). The run is the first build after the run-out and each next one with at most one ordinary or idle pass between (a pass's index counts idle passes); a build's frames include what it left owed (sent by a later poll before the next build). Outcomes: released, empty, late (first frame, or first build if none, more than `LATE_MS` = the derived 49 ms after it), absent (no build; the log, by its last MS line, runs on past the bound), unresolved (the log ends first). `FAILING = ('late', 'absent')`.
- `join_grade.held`: adds `runs` (counts by outcome) and `failing`; `run.stated_misses` names late and absent; `print_joins` prints the outcome counts.
- Checks (`selftest_polls.horizon_checks`): 191, 239 hold; 241, 289, 291, 500 fail as late and over; absent vs unresolved; an owed frame; empty. Plants (`selftest_mutants.py`), each caught: the 100 ms horizon (earlier rule), LATE_MS ignored, late not failing, absent taken for unresolved, unresolved taken for empty, an owed frame not its build's.
- Re-grade of round 7's 14 published logs (`receipts/item4/`): the start head's grader 52 intervals; the new grader 57 (the 5 more are MVRP frames the old rule dropped when the run-out's first build was empty), 185.645 to 190.025 ms, no late, absent or unresolved, latest first frame 1.55 ms after its run-out.

## 5. The pace and the rows (`197012aa`)

`AECP_PACE_MS 7u` with its comment (`aecp_mbx.h:38-50`). See section 0.

## 6. Item 5: docs and residue (`f2f92fdc`, `2763cc06`, `dd01b0af`)

| Finding | Fixed at | Now states |
|---|---|---|
| R837-2-3 / R838-2-F3: FR_NFR 3.4.1 SRP/MRP row | `docs/reference/FR_NFR.md:415` | 49 ms at the split (40 at the 200 ms default), the armed 190 ms plus it and `T_egress` within 240 ms, "committed within 49 ms", periodic 950 to 1050 ms and LeaveAll 9.96 to 15.04 s on the wire, 281 ms at 90 |
| R837-2-3 / R838-2-F3: MAILBOX_SPLIT slice | `docs/design/MAILBOX_SPLIT.md:390` | `CTRL_LOOP_SLICE_US`: 0.9 ms at one interface, 1.3 ms at two |
| R837-2-3: THE TIERS' last queued notice | `sw/firmware/ctrl/loop/ctrl_loop.h:206-209` | decision D's 125 ms, at 1x1/1if `AECP_QUEUED_MS`'s 130 ms (the amendment) |
| R838-2-F3: AECP README | `sw/firmware/ctrl/aecp/README.md:120` | 130 ms at 1x1/1if, the amendment cited |
| R837-2-3: "What is left" R4 74.83 | `docs/design/SPLIT_CONTROL_MEMORY.md` "What is left", the load bullet | "before #894's tiers, R4 by every source was 74.83 ms ... under the tiers every 1x1/1if row holds, R4 12.82 ms" |
| R837-2-3: the 30 ms rows cited the question | `docs/reference/FR_NFR.md:374`; `SPLIT_CONTROL_MEMORY.md:361`, `:2355` | the ruling 6844175391, with the owner's confirmation 6844947317 |
| R837-2-4 / R838-2-R1: issue-comment IDs and round labels in source | `aecp_mbx.h`, `ctrl_loop.h`, `ctrl_memory.py:260-261`, `load_grade.py:235`, `notice_window.py:61`, `queued_bound.py:3-4`, `selftest_notice.py:88` (message string), and those rewritten with items 1 to 4 (`flip_grade.py`, `join_grade.py`, `paced_rows.py`, `rows_tiers.py`, `run.py`, `selftest_polls.py`, `tier1_rows.py`) | rulings by name and date; `git diff cec88385..HEAD -U0 -- . ':!*.md' \| grep '^+.*issuecomment-'` is empty |
| R837-2-5: interval count; pre-restatement receipt | this round's REVIEW READY and PR body | intervals counted with and without the planted control; round 7's `receipts/model/rows-1x1-final.txt` is the rows at `2953091e`, before the build-of-one restatement, and its final rows are `receipts/gates/lane-flip_check_1x1.txt` |
| R838-2-R2: round 7's handoff pointer | not rewritten (published packet) | stated here: round 7's final rows are `receipts/gates/lane-flip_check_1x1.txt` (`8a3791e4`, last 125.84, txL 49.99) |

Also with the items: SPLIT_CONTROL_MEMORY section 13 (THE TIERS table row, "The command, under #904", THE PACE, the new "Egress counted" subsection); FR_NFR 3.4.1's R4L, MRPDU, pace and 424-426 paragraphs; the harness README's join and model bullets; the srp README's MRPDU paragraph. `docs_check.py` 0 findings; `check_em_dash.py` 0 over 26 pages.

## 7. New checks, planted mutants and failing words

| Check | Plant | Failing words | Where caught |
|---|---|---|---|
| The pace count is the gate's | `paced_rows.edits` -> 1 + floor(w / P) | "THE PACE's edits in a window of 0.01 ms at 1 ms counted 1, not the 2 the gate takes (aecp_mbx.c, ready)" (`receipts/model/plant-words.txt`), and txL shorter at some P | `rows_tiers --selftest` (CONTROLS "THE PACE's edits counted 1 + floor(w / P)"); the flip check's row findings |
| The count's own check | `count_findings` not empty at the tree | "THE PACE's edits not the gate's count" | `rows_tiers --selftest` |
| MRPDU bound counts T_egress | `(240u - 10u * CTRL_LOOP_JOIN_CS)`, `90u` | "1x1/1if: CTRL_LOOP_TX_BOUND_MS states 50 ms, not the timer budget's 49" | `rows_tiers --selftest` ("THE TRANSMIT's bound not the timer budget's") |
| Bounds pinned | `TX_BUDGET_MS != 49`, `PACED_BOUNDS != {'R4L': 238}` | "a channel row's or THE TRANSMIT's bound not the ruling's" | `flip_grade --selftest` |
| Join gate 181.0 to 239.0 | `joins: the wire's 180.0 to 240.0 ms held at the commit, T_egress uncounted` | "a join interval is two MRPDUs ... 181 and 239 ms ... hold" | harness self-test |
| Map work linear | `map-remove-values-rewalked`; `map-hash-the-stream-alone` | "not under n(n+1)/2"; "past twice their sum" | AECP campaign (work arm) |
| Keys of one slot are their own | `map-table-key-unchecked` | "an ADD of two keys that share a slot adds both" | AECP campaign |
| Illegal mapping ends the table at its turn | `map-illegal-ends-early`; `map-illegal-unflagged` | "status for command" | AECP campaign |
| No horizon | `joins: a run-out's builds sought within 100 ms of it (earlier rule)` | "a run-out's build past THE TRANSMIT's bound is late and named ..." | harness self-test |
| Late is late and fails | `joins: a late build taken for an on-time one`; `joins: a late build's run-out not failing the run` | the same | harness self-test |
| Absent, unresolved, empty told apart | `joins: an absent build taken for an unresolved one`; `joins: an unresolved build taken for one that owes nothing` | "no build after a run-out is absent and named ..." | harness self-test |
| Owed frames | `joins: a frame its build left owed not the build's` | "a frame its build left owed ... is that build's" | harness self-test |

Pre-checks at `197012aa` (lane subset) and `dd01b0af` (firmware suite, legs): harness self-test 0 failures, 246 mutants caught, 0 escaped; rows_tiers 971/971; flip 555/555; load 25/25; hooks 96/96; firmware suite PASS (the work arm `aecp-work-...-if1` ok); 1x1 `srp` and `aecp-largest-notice` legs rc 0.

## 8. Gate table

The full pass at `dd01b0afef87037ec485cd49b40a26b542854bdd`, once, each part on its own clean clone and never piped (receipts `receipts/gates/`; tooling `r8/scripts/`).

| Gate | Result | Receipt |
|---|---|---|
| The sweep, 4 shards (`native-shards.py`, label 894-r8g, CPUs 0-7, 8-15, 16-23, 24-31) | exit 0 each; 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures | `sweep-shard{0..3}.txt` |
| Every hosted job step of rtl-fast, rtl, elaborate and docs (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`) | 139 run, 226 not run with a reason; 1 UNKNOWN on its first run: elaborate-gates-1 gate_19, `test_soc_timing_cuts` past its 900 s wall clock under the pass's load (rc 92). Run again alone in its job's clone at 900 s (`rerun_step.sh`): 8 of 8, rc 0 | `workflows-verify.md`, `elaborate-gate_19-first-run.txt`, `elaborate-gate_19-rerun.txt` |
| Firmware jobs: unit (4 shards' steps), control, AECP and SRP campaigns, boundary, Verilator | every step 0; the AECP campaign 269 of 269 caught, the 21 map plants among them | `workflows-verify.md`, `unit-rcs.txt` |
| Lane gates, part a | 41 at 0; the 4 that exit 1 by design (8x8/2if reported, as-built): `rows_tiers --terms`, `flip --check`, `--point 8x8/2if`, `--design as-built` | `lane-summary.txt`, `lane-*.txt` |
| Harness self-test | 0 failures; 246 mutants caught, 0 escaped | `lane-harness_selftest.summary.txt` |
| `flip_grade.py --check --point 1x1/1if` | PASS (txL 47.98/49, R4L 173.37/238, last 125.84/130) | `lane-flip_check_1x1.txt` |
| rows_tiers, flip and load self-tests; `load_grade.py --check` | 971/971, 555/555, 25/25; 0.513 and 0.509 | `lane-*.txt` |
| `tier_grid.py --point 1x1/1if` | exit 0 | `lane-tier_grid.txt` |
| em-dash, idioms, docs, diff checks (10 bases incl. `8a3791e4`), `ctrl_hot` | 0 | `lane-*.txt` |
| BDD; `make twin`, `make twin-plants` | pass; 0 findings, every plant refused | `lane-behave.summary.txt`, `lane-twin*.summary.txt` |
| Lane parts b and c (builder tests, NVM self-test, boot 1x1, 8x8, native, plants) | 0 | `lane-*.summary.txt` |
| Harness legs at 1x1 (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`) | exit 0; the plant control `acmp-redelivered-every-poll` (C-R1) caught | `harness-head-builds.txt` |
| Harness legs at 8x8/2if | four groups exit 0; `srp` exits 1 on the refuted build of one (138,000 and 147,450 against 121,500; #910) | the same |
| Harness legs at 8x8-1if | exit 1, reported (lane 894b's point): build-one passes over the one-interface 72,500; the answering-every-port arm refuses to build | the same |
| Join intervals, every leg | 57 in 14 group runs (54 in 13 unplanted), 185.468 to 190.059 ms, within 181.0 to 239.0; 195 run-outs, 126 released, 69 empty, 0 late, absent or unresolved | the same |
| Measured inputs from the pass's legs | the record 92,766 (975 us), the long notice 34,370 (365); no item over its stated cost at 1x1 or 8x8 | `receipts/model/measured-inputs-final-pass.txt` |
| Every image at the head (`qall.sh`) | within its caps; each rom +176 B on the start head, sram and tiles equal | `receipts/images/every-image-final.txt` |

## 9. Run history

- 00:57 CET: start; read the ruling, both reports, the probes and the 894b table.
- 00:57-01:05: item 2 (`8ba93f26`).
- 01:05-01:22: item 3 firmware (`6c232270`): the map plants unit (all caught once the slot-sharing test was added); images at the start head reproduce round 7's bytes, the rewrite +176 B.
- 01:22-01:27: item 1 (`96565297`) and the group's refused edits (`44f897ab`); the re-measure legs L1L, L8L, 81L ran 01:24-01:40.
- 01:27-01:38: item 4 (`b6b94d92`); re-grade of round 7's logs.
- 01:40: restatement and P 7 (`197012aa`).
- 01:45-01:50: docs and residue (`f2f92fdc`, `2763cc06`, `dd01b0af`); pre-checks launched (lane subset at `197012aa`, firmware suite and 1x1 `srp` and largest-notice legs at `dd01b0af`).
- 01:52-02:05: pre-checks pass (lane subset, firmware suite, 1x1 legs); #894, #908 and #902 had no new comment, dev-soft-core still `cec88385`, #810's branch `084cf7a8`.
- 02:04: the sweep's first launch put its four shards on one picked range (80-87); stopped one by one, its output moved to `r8/sweep-aborted-shared-cpus` and its clones removed; relaunched at 02:05 on 0-7, 8-15, 16-23, 24-31.
- 02:05: the dispatcher (33 lines). 02:08: stopped after its first 10 and re-spread: 8 workflow lines on 56-87 (MAX 4), 15 legs on 96-127 (MAX 6).
- 02:58: every queue line done; 03:18: the sweep done; gate_19 run again alone, 8 of 8.
- 03:20-03:30: receipts collected; images at the head; PR body and comment completed.

- 03:21: REVIEW READY posted (issuecomment-6870102413), the round's one comment.
