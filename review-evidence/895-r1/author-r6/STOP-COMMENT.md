[A775] STOP — round 6, head `bf0844f19374bfbf7091271dfb50fad7a1f1835d` (local, not pushed)

The head's three commits on round 5's `62298ab5`:
- `df0bc467`: the merge of #902's `9606b3a9` (#894's round 11), item 1.
- `3024e740`: the two costs R835-3-F1's survey finds under their rule figure, restated.
- `bf0844f1`: section 13, section 5, FR_NFR 3.4.1 and the READMEs at this head. These also answer R835-3-F2, R836-3-F1 and both RS1s.

**Why.** At the restated tables two of the round's listed stops hold:
- the slice rule (`rows_tiers.ruled`, `tier_grid.py`) takes **950 us**, not the built 900;
- the built design's last queued notice at 1x1/1if is **134.94 ms, over 130**.

No slice, bound, pace or other figure was chosen. The slice is the maintainer's to decide.

### 1. The sync (item 1)

The merge resolves the conflicting cost table and the three documents. Each cost is the one of the side that moved it from the merge base `7398ec0a`, the larger where both moved it: AECP's timer slot, the 8x8/2if TICK and MAAP's record are #895's; ACMP's owed frame (55 / 70 us) is #894's.

The rule already left the built design at the merged tables, before any re-measure: 950 us at +0.0200 against 900 us at +0.0175. `rows_tiers.py --selftest` then refused the tree (1031 of 1032).

### 2. Every stated cost against this head's legs (R835-3-F1)

The legs: the CPU budget harness at 1x1/1if on the merge's image, on a clean clone. They are arm A (96 groups), `answering-every-port` (16), `valid-destinations` (2), and arm B's `aecp`, `aecp-largest-notice` and `aecp-fanout`.

The survey covers every table the rows read:
- `load_grade.py`, both columns;
- `poll_grade.STATED_US`;
- `whole_grade.stated_us`, i.e. `ctrl_loop.h`'s passes given whole;
- `rows_grade.ROW_COSTS`;
- `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`;
- `edit_rows.EDIT_RECORD_US`.

Each table is held by the rule to round 1's parsers, the harness's own `poll_grade.held` / `whole_grade.held`, and `record_classes.py`. The result is UNDER 4 at the merge's tables and UNDER 0 at the head's.

| Cost, 1x1/1if | Most measured | Rule | Stated | Now |
|---|---:|---:|---:|---:|
| the polls' base (`acmp-cmd`) | 20,282 cycles | 215 us | 205 | 215, both tables |
| a pass's events' fixed part (`notice-burst-0`) | 3,041 cycles | 35 us | 30 | 35, both columns |

Every other cost is within its rule figure. That includes AECP's classes:
- a paced edit: 23,306 cycles, 245 us (260 stated);
- the largest legal command: 86,762 cycles, 915 us (975 stated);
- every other record: 20,525 cycles, 220 us (the ruled 235).

**The polls' base is this lane's Talker work.** The same group's heaviest base on #902's `9606b3a9` is 18,843 cycles (200 us), so this head adds 1,439:
- The pass runs 79 instructions more with 4 instruction refills fewer.
- MAAP's poll +407 and SRP's delivery +378: these carry the declarations and #905's stream_id.
- ACMP's, ADP's and AECP's polls: +320, +198 and +161.

**The fixed part** was 2,623 cycles at round 5's head and is 3,041 here. The cut moves the code's placement (#909); its cause was not traced.

### 3. The graders at the restated tables

By every source, ms. The 950 column is the same tree with only the slice changed, on a scratch export:

| Row | Bound | The merge's tables, 900 | Restated, 900 (built) | Restated, 950 (the rule's) |
|---|---:|---:|---:|---:|
| R4 | 20 | 13.03 | 13.11 | 13.16 |
| R5 / R6 | 90 | 73.88 / 69.73 | 74.47 / 72.53 | 74.52 / 72.58 |
| first queued notice | 20 | 14.62 | 14.65 | 14.70 |
| **last queued notice** | 130 | 127.73 | **134.94** | 127.83 |
| R4L | 238 | 203.49 | 203.53 | 203.58 |
| ACMP / ADP / MAAP | 30 | 29.03 / 27.36 / 27.46 | 29.29 / 27.56 / 27.65 | 29.34 / 27.61 / 27.70 |
| tx (`CTRL_LOOP_TX_MS` 34) | 49 | 33.39 | 33.64 | 33.69 |
| txL | 49 | 47.97 | 48.32 | 48.37 |

The graders on a clean clone of the head:
- **`flip_grade.py --check --point 1x1/1if`: FAIL.** "OVER 1x1/1if last ... 134.94 ms, over its bound 130 ms". Also "aecp_mbx.h states AECP_QUEUED_MS 130 ms, not the 135 ms its row 134.94 ms rules": the amendment's rule rounds the row up to 135, within its 140.
- **The slice rule**: `slice_choice` 950 us at +0.0129 (txL binding); `ruled` 950. The built 900 is at -0.038.
- **`tier_grid.py --point 1x1/1if`**: 12 of 420 hold. CHOSEN 950 us, AECP first, SRP first, the AECP queue, cap 2, +0.0129.
- **The self-tests:**
  - `rows_tiers.py --selftest`: 1031 of 1032, "ESCAPED the built design's slice not the rule's".
  - `flip_grade.py --selftest`: 584 of 585, "ESCAPED AECP_QUEUED_MS not the bound the last queued notice's row rules". `queued_bound.controls` reports this while the tree's 130 is not its rule's 135.
  - `load_grade.py --selftest`: 25 of 25.
- **The pace rule** stays 9 ms: txL is 49.94 at 8 and 48.32 at 9. At 900 us the last queued notice is over 130 at every pace from 7 to 13 ms (135.04 to 134.81).
- **Each restatement alone puts it over**, at 900 and pace 9:
  - the base alone at 215: 133.91 ms;
  - the fixed part alone at 35: 132.72;
  - the fixed part at 35 with the base at 210: 133.91.
- **The load**: 0.517 at the pin and 0.513 with tsn-c-stack#32, 0.696 with every notice the largest legal one. 8x8/2if is reported with its tables unchanged: R4 42.85, R4L 210.91, tx 89.98 (98 stated), txL 399.86, load 0.798 / 0.756.

### 4. R835-3-F2: AMAP_LIVE_WRITE at 8x8/2if

The `datapath-events` group on the merge's image at 8x8/2if measures the take and sinks at 2,367 cycles, i.e. 23.67 us. That is within the 23.80 that 25 holds, so 25 stands. The measure is `eventcost.py`, which #894 states `DATAPATH_US` by (#894 issuecomment-6872978311). At round 5's head it was 2,426.

### 5. The round's other stop conditions

| Condition | At the head |
|---|---|
| no pace up to 11 ms | the pace is 9 |
| tier-1, SRP and tx rows | each within its bound (above) |
| the load | 0.517 / 0.513 |
| join intervals | 365 in 117 group runs, 187.779 to 190.109 ms, every one within 181 to 239 |
| ROM (the merge's images, `plat_ledger.py` PASS) | the platform 8x8/2if at 60.5 with 1,656 B left; the fixture and both harness arms at 59.0 with 656, 348 and 488 B; every other point within 56. #894's cut adds 224 B (1x1) or 208 B (8x8) of rom an image, no sram |
| lwSRP | no change |

Every leg that ran to its end exited rc 0 with 0 refusals and 0 `STATED` lines. Arm A has the seven known held-egress misses.

### 6. Not run, at the stop

- the gates, the full pass on a clean clone, and the Verilator sweep;
- the harness at the final head (its firmware is the merge's, measured above);
- 8x8/2if's arm A, `answering-every-port`, `valid-destinations` and arm B legs. They were dropped once both triggers were settled at 1x1/1if: a restatement only raises a cost, and the rows only grow with their costs. Only `datapath-events` ran at 8x8/2if.

### Options (not chosen here)

- **(a)** The slice at 1x1/1if goes 900 -> 950 us, the slice rule's choice. `ctrl_loop.h:262-277` states the rule's choice as 900; at 950 every 1x1/1if row holds at +0.0129. This is a firmware constant, so the harness would run again on that image.
- **(b)** Cut the composed per-pass cost and measure again. The base's +1,439 cycles over #894's image are the Talker work; the fixed part's +418 is placement (#909). The fixed part alone already puts the last queued notice at 132.72 ms.
- **(c)** The last queued notice's bound: `aecp_mbx.h` states 130 ms; the amendment's rule gives 135 for this row, within its 140.
- **(d)** #901 waits behind the flip.

Recorded for #894, not this lane's: `ctrl_loop.h:278-280` states `CTRL_LOOP_SRP_UNIT_US` (250 us at 1x1/1if) as "the load gate's record.srp", which `load_grade.py` states at 280. No grader reads it.

The receipts are in the round's packet: the legs, the parsers, the survey before and after, the attribution, the graders and the sensitivity script, and the ledger. Nothing was pushed.
