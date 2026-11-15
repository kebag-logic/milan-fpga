[A775] STOP — round 8, head `f93317cb` (local, not pushed)

**Why: item 3's rule at 8x8/2if would make a wire-visible change.** With 8x8/2if's costs restated by the rule, its tx row is **104.25 ms**, over the 99 `CTRL_LOOP_TX_MS` states there, and `rows_tiers.tx_statements` holds each interface count's figure at or over its row.
- By the rule the figure is **105**.
- `SRP_REDECLARE_CS` at two interfaces (2,000 + 19 + (`CTRL_LOOP_TX_MS` + 9) / 10) would then move from 2,029 to **2,030 cs**. A withdrawn Talker's changed destination would be declared 10 ms later at 8x8/2if.
- That is a wire-visible change, which the ruling (issuecomment-6892130675) lists as a stop and the relay asked to be shown not to happen. So the figure is not restated here.

At 1x1/1if everything holds, and `SRP_REDECLARE_CS` there stays 2,023 cs.

### What round 8 did

| Commit | Item | What |
|---|---|---|
| `1143e3f5` | sync | Merge #902's `b6f5c638` (`CTRL_LOOP_TX_MS` 99 at two interfaces, #902's). By hash: every image `ledger.sh` links (each ELF's loadable bytes and every object, 552 files) is identical to 7B's cut head. #894's own receipt shows `b6f5c638`'s 332 image files identical to `234bc149`'s. |
| `2b7f8428` | 1 | `AECP_QUEUED_MS` at one interface 130 -> **140**, the queued rule's figure for its row. FR_NFR 3.4.1 amended with the row, 135.43 at 950 us: +10.43 over 125, +5.43 over 130, 4.57 within 140. #894's head keeps 130. |
| `73388996` | 4 | At the 140 ms bound the slice rule takes **900 us** (+0.0086, txL binding; 950 is +0.0076, 1,000 +0.0065), and `ruled` agrees. Built there; the row at 900 is 136.65, which rules the same 140. |
| (none) | 3 | At 1x1/1if the tx row at 900 us is 34.00, so the rule gives the stated 34 (950's 35 is not taken), and `SRP_REDECLARE_CS` stays 2,023. At 8x8/2if: see above. |
| `b69388c7` | 7 | 8x8/2if restatements by the rule (reported): the polls' base 325 -> 345 (32,705 cycles, `notice-every-4`), a notice past `AECP_FAN_BYTES` 655 -> 700 (66,481, `aecp-largest-notice`), a pass's events' fixed part 35 -> 40 (3,437), AMAP_LIVE_WRITE 25 -> 30 (2,465). |
| `f93317cb` | 7 | Section 13, FR_NFR 3.4.1 and the SRP README at this head. |

**The rebuilt image** (`73388996`; every later commit changes only Python tables and docs):
- **Identity:** against the merge, 16 image files differ, all one-interface (`ctrl_loop.o` and its ELF). Every two-interface image is identical.
- **1x1/1if:** arm A's 96 groups, `answering-every-port` 16, `valid-destinations` 2 and arm B 3. Every leg is rc 0 with 0 refusals, 0 `STATED` lines and arm A's 7 known misses. The joins are 359 intervals, 188.102 to 190.121 ms.
- **The survey at 1x1/1if: UNDER 0.** The bound and the slice settle after the one rebuild.
- **8x8/2if:** arm A 94, N8 16, W8 2, B8 3.
  - N8 and B8 exited rc 1 on raw `STATED` lines (the base and the long notice); both regrade rc 0 at the restated tables.
  - The joins are 750 intervals, 185.605 to 190.228 ms.
  - The survey was UNDER 7, and UNDER 0 at the head.

**1x1/1if at the head** (900 us, bound 140), by every source, ms, with each margin:

| Row | W | Bound | Margin |
|---|---:|---:|---:|
| R4 | 13.25 | 20 | 6.75 |
| R5 | 75.84 | 90 | 14.16 |
| R6 | 73.36 | 90 | 16.64 |
| first queued notice | 14.72 | 20 | 5.28 |
| last queued notice | 136.65 | 140 | 3.35 |
| R4L | 203.57 | 238 | 34.43 |
| ACMP | 29.63 | 30 | **0.37** |
| ADP | 27.86 | 30 | 2.14 |
| MAAP | 27.96 | 30 | 2.04 |
| tx | 34.00 | 49 | 15.00 |
| txL | 48.58 | 49 | **0.42** |

- **Flip check:** PASS.
- **`tier_grid.py`:** 6 of 420 hold, CHOSEN the built design.
- **Pace:** 9 ms (txL 49.99 at 8).
- **Load:** 0.517 at the pin, 0.514 with tsn-c-stack#32, 0.696 with every command the largest legal one.
- **Self-tests:** `rows_tiers.py --selftest` 1032 of 1033; its one refusal is "THE TRANSMIT's stated figure under its row", this stop. `flip_grade.py --selftest` 585 of 585, `load_grade.py --selftest` 26 of 26. Doc and idiom checks pass.
- **The 140 ms per-pass cost:** a pass's own cost is 260 us (fixed part 35 + polls' base 225). The last queued notice holds 140 ms up to **278 us**. At **279 us** it is 141.36 ms, and txL 49.02, over its 49.
- **ROM:** the cut head's sizes. The platform 8x8/2if is at 60.5 (1,368 B left); the fixture and the harness arms are at 59.0 (368, 60 and 200 B left); every other point is ≤ 56. No lwSRP change.
- **8x8/2if, reported:** R4 45.06, R4L 211.08, tx 104.25, txL 466.85; load 0.798 / 0.756. N8 and B8 each have two passes over the share (at most 2.018 and 2.337 ms), which are #890's.

**Not run, at the stop:** the gates, the full pass and the sweep.

### Options (not chosen here)

- **(a)** Restate 8x8/2if's `CTRL_LOOP_TX_MS` to 105 and accept `SRP_REDECLARE_CS` at 2,030 cs at two interfaces (still over IEEE 802.1Q-2018 35.2.2.8's 2,000 cs). The 8x8/2if images then change in one constant.
- **(b)** Hold 8x8/2if's statement as reported only. The control that holds both interface counts is #902's round-16 addition.
- **(c)** Take the hold-off's TX term at two interfaces from another figure. That is a design change.

Receipts: round 8's packet (legs, surveys before and after, graders, identity hashes, ledgers, the per-pass threshold). Nothing was pushed.
