[A773] REVIEW READY
Commit: dd01b0afef87037ec485cd49b40a26b542854bdd (`894-tiers`, 11 commits on round 7's `8a3791e4`; dev-soft-core still `cec88385`; not pushed)

**1x1/1if holds every row by every source** under #894's egress ruling of 2026-11-13 (issuecomment-6867990126). No STOP trigger: 7 ms holds; the last queued notice is within 140 ms; no image is over its cap; the map commands' behaviour is unchanged; the collision case's pass is 96,142 of THE SHARE's 200,000 cycles.

**Rows at 1x1/1if** (`flip_grade.py --check --point 1x1/1if`: PASS; slice 900 us, P = 7 ms, join timer 19 cs):

| Row | ms | Bound | Round 7 |
|---|---:|---:|---|
| R4 | 12.82 | 20 | 12.82 |
| R4L (paced) | 173.37 | 238 | 158.34 of 240 at P 6 |
| ACMP | 28.35 | 30 | |
| ADP | 26.76 | 30 | |
| MAAP | 26.88 | 30 | |
| first queued notice | 14.50 | 20 | |
| R5 | 72.71 | 90 | |
| R6 | 68.62 | 90 | |
| last queued notice | 125.84 | 130 | |
| tx | 29.78 | 49 | of 50 |
| txL | 47.98 | 49 | 49.99 of 50 |

Load 0.513 at the pin and 0.509 with tsn-c-stack#32 (0.70). Images (RAMB36): 1x1/1if fixture 40.5 and platform 42.5; 8x8/1if platform 56.0 (129,208 of 131,072 B); 8x8/2if fixture 59.0 (its ledgered cap) and platform 60.0 (cap 60.5). The map rewrite adds 176 B of rom to each.

**In the ruling's order:**
1. **Item 2, the pace count** (`8ba93f26`). `paced_rows.edits` = ceil((w + 1) / P): the gate compares whole ms against a fresh stamp (`aecp_mbx.c:154-158`, `aecp.c:31-37`), so floor(t[k+1]) >= floor(t[k]) + P. It is held to a simulation of the gate at every window to 120 ms and P to 13; the earlier rule is planted ("counted 1, not the 2 the gate takes"). R837-2's probe, unchanged, prints equal columns for every P.
2. **Item 1, T_egress counted** (`96565297`). `CTRL_LOOP_T_INGRESS_MS` and `CTRL_LOOP_T_EGRESS_MS` (1 ms each) in `ctrl_loop.h`; THE TRANSMIT's bound `(240u - 10u * CTRL_LOOP_JOIN_CS - CTRL_LOOP_T_EGRESS_MS)` = 49 ms; paced R4L 240 - T_ingress - T_egress = 238 ms; the harness join gate 181.0 to 239.0 ms; each derived, the egress-free derivation planted and refused. FR_NFR 3.4.1 (lines 373, 381, 424-426) states the split's figures and cites the ruling.
3. **Item 3, the map commands** (`6c232270`, `44f897ab`). Bounded, linear work for refused and accepted legal-length edits: one slot a key; a mapping its geometry refuses ends the table at its own turn, as an ADD's earlier conflict does; a REMOVE's other values of a key are linked from its first. `Core.MapEditsAreTheirDefinitionRowForRow` is unchanged and passes. A work arm counts the visits: at 63 mappings the collision of one key's values is 127 (bound 2 (n + R) = 128), against 2,080 for the start head's table; the planted walk gives n(n+1)/2 + 2 at 8, 16, 32 and 63 and is refused at each. The AECP campaign catches 269 of 269 plants, the 21 map plants among them.
   - The collision and conflict cases joined `aecp-largest-notice` (550 B, refused BAD_ARGUMENTS). Re-measured at 1x1/1if: the REMOVE of 63 92,766 cycles, the ADD 86,504, the refused edits 23,014 to 79,281. Restated (`197012aa`) at 975 us (+5 %, was 940). On the 8x8 shape 142,634 (1,555 kept).
4. **Item 4, the join grader** (`b6b94d92`). No horizon: each MRP timer's run-out is released, empty, late (past the derived 49 ms), absent or unresolved; late and absent fail the run. The controls span the old 100 ms horizon: 191 and 239 ms hold; 241, 289, 291 and 500 ms fail as late and over (R838-2's probe, unchanged, now counts both). Six new plants are caught.
   - Re-graded: round 7's 14 published legs give 57 intervals, 185.645 to 190.025 ms, none late, absent or unresolved (52 by the earlier grader, which dropped a run-out whose first build sent nothing); its timer-to-MRPDU rows 1.292, 2.245 and 3.440 ms (3.085 before), each within 20 ms.
   - At this head: 57 intervals in 14 group runs, 185.468 to 190.059 ms; 54 in the 13 unplanted runs and 3 in the planted control C-R1's. No run-out is late, absent or unresolved.
5. **The pace.** At 49 and 238 ms and the 975 us record: P 6 txL 53.86; **P 7 txL 47.98, R4L 173.37** (`AECP_PACE_MS 7u`); P 8 47.98 / 188.37; P 9 47.24 / 203.37; P 10 and 11 45.65 / 218.37 and 233.37. The slice rule keeps 900 us and the queued bound 130 ms.
6. **Item 5, docs and residue** (`2763cc06`, `dd01b0af`). R838-2-F3 and R837-2-3: FR_NFR 3.4.1's SRP row (49 ms, 950 to 1050 ms periodic and 9.96 to 15.04 s LeaveAll on the wire), MAILBOX_SPLIT's 0.9 ms slice, the AECP README's 130 ms, `ctrl_loop.h`'s THE TIERS note, SPLIT_CONTROL_MEMORY's stale R4, and the 30 ms rows citing ruling 6844175391. R837-2-4 and R838-2-R1: no issue-comment ID or review label in added source. R837-2-5: the counts above separate the planted control; round 7's `receipts/model/rows-1x1-final.txt` is the rows at `2953091e`, before the build-of-one restatement, and its final rows are `receipts/gates/lane-flip_check_1x1.txt`.

**Validation, the full pass at the head, each part on its own clean clone and never piped:**
- **The sweep, 4 shards:** each exit 0; 65 suites, 2,713,040 checks, 0 failures.
- **Every hosted job step of rtl-fast, rtl, elaborate and docs run locally:** 139 run, 226 not run with a reason. One of the 139, elaborate-gates-1's Standalone LiteX simulation aggregate, was UNKNOWN on its first run: `test_soc_timing_cuts` hit its 900 s wall clock under the pass's load (exit 92, "not a failure"). Run again alone in its job's clean clone at the same 900 s, it passes, 8 of 8 simulations.
- **Firmware jobs:** unit, control, AECP (269 of 269) and SRP mutation campaigns, boundary, Verilator: every step 0.
- **Lane gates:** 41 at 0, and the 4 that exit 1 by design (the reported 8x8/2if: `flip_grade.py --check`, `--point 8x8/2if`, `--design as-built`, `rows_tiers.py --terms`). Harness self-test 0 failures, 246 mutants caught; rows_tiers 971/971, flip 555/555, load 25/25; twin 0 findings, every plant refused; BDD; builder; boot gates.
- **Harness legs:** every 1x1 leg and the four 8x8 groups exit 0; the plant control C-R1 caught; 8x8's `srp` exits 1 on the refuted build of one (#910); the 8x8-1if legs exit 1 (lane 894b's point).

Acceptance criteria (the ruling's items 1 to 5): met, with the evidence above and in the PR body's finding-by-finding table.
Open risks/questions: none blocking. The bench capture of the join intervals on the wire is S12b's; 8x8/1if takes the new bounds in lane 894b after #902 merges (item 6); #908 stays open by its own terms.
