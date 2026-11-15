[A775] 7A DONE — round 7, head `4c9757ee` (local, not pushed)

The round follows the ruling on round 6's stop (issuecomment-6886630886). None of the ruling's stops holds, and item 3's cut was not needed.

**Commits on `bf0844f1`:**

| Commit | What |
|---|---|
| `ff943513` | Item 1: the built 1x1/1if slice is the slice rule's choice at the restated tables, **950 us** (`CTRL_LOOP_SLICE_US`; 900 before). `ctrl_loop.h` states the rule. The self-tests hold the figure: `rows_tiers.py`'s control refuses the 900 us header, and `selftest_round.py` holds 950 / 1,300. |
| `6d79b352` | `rows_tiers.py` held to the 1,000-line module ratchet (comment only). |
| `58c99c67` | 8x8/2if: MAAP's timer slot measured 21,120 cycles (225 us by the rule) against 215 stated; restated 215 -> 225, both columns. |
| `4c9757ee` | Section 13 "The rule's slice built (#895)", FR_NFR 3.4.1, and the SRP README at this head. |

**The rebuilt image, measured at both points:**
- **Legs:** every group of arm A (96 at 1x1/1if, 94 at 8x8/2if), `answering-every-port`, `valid-destinations`, and arm B's `aecp`, `aecp-largest-notice` and `aecp-fanout`.
  - Every leg exits rc 0, with 0 refusals and 0 `STATED` lines.
  - Arm A has the seven known held-egress misses at each point.
- **Firmware arms:** port, portable and AECP all PASS at 950 us.
- **Survey of every stated table the rows read, by the rule:**
  - **1x1/1if:** UNDER 0. Every cost equals its round-6 measurement, cycle for cycle; round 6's two restatements stand.
  - **8x8/2if:** UNDER 2 before the restatement (MAAP's timer slot, both columns), UNDER 0 after. AMAP_LIVE_WRITE stays within at 2,367 cycles.

**1x1/1if by every source at 950 us** (ms; `flip_grade.py --check`: PASS):

| Row | Bound | ms |
|---|---:|---:|
| R4 | 20 | 13.16 |
| R5 | 90 | 74.52 |
| R6 | 90 | 72.58 |
| first queued notice | 20 | 14.70 |
| last queued notice | 130 | 127.83 |
| R4L | 238 | 203.58 |
| ACMP | 30 | 29.34 |
| ADP | 30 | 27.61 |
| MAAP | 30 | 27.70 |
| tx | 49 (34 stated) | 33.69 |
| txL | 49 | 48.37 |

**The other graders and the stop checks:**
- **The slice rule** on the rebuilt image's tables: `slice_choice` and `ruled` give 950 us (+0.0129), equal to the built slice. The choice did not move a second time.
- **`tier_grid.py`:** 12 of 420 designs hold, CHOSEN the built design.
- **Self-tests:** `rows_tiers.py --selftest` 1032/1032, `flip_grade.py --selftest` 585/585, `load_grade.py --selftest` 25/25.
- **Pace:** 9 ms (txL 49.99 at 8).
- **Load:** 0.517 at the pin, 0.513 with tsn-c-stack#32, 0.696 with every command the largest legal one.
- **Joins:** 1,109 in 231 group runs, 182.679 to 190.642 ms, every one within 181 to 239.
- **ROM:** each image's size equals round 6's. The platform 8x8/2if is at 60.5 with 1,656 B left; the fixture and both harness arms are at 59.0; every other point is within 56.
- **lwSRP:** no change.

**8x8/2if, reported:**
- R4 42.87, R4L 210.93, tx 94.99 (98 stated), txL 399.88; load 0.798 / 0.756.
- Arm B's `aecp-largest-notice`, run at this point for the first time, puts 2 of its 138 work passes over the per-pass share: the longest is 223,684 cycles (2.237 ms). The share at 8x8/2if belongs to the flip, under #890.

Not run, as the ruling asks for 7A: the gates, the full pass and the sweep. `CTRL_LOOP_SRP_UNIT_US` is unchanged here and arrives with 7B's sync. Nothing was pushed.
