[A775] STOP — round 7B, head `0c93071e` (local, not pushed)

**Why:** after the ruling's one cut (item 3), **no slice from 650 to 1,100 us holds every 1x1/1if row**. The ruling's stops are in #895 issuecomment-6886630886. No slice, bound, pace or other figure was chosen; only measured costs were restated by the rule.

### 1. The sync

`7e3db6b9` merges #902's round-13 review head `234bc149`.
- **Slice code:** the merge takes #902's slice code (#894 issuecomment-6888782796, item 2): `ctrl_loop.h` whole, with the slice rule's 950 us, `CTRL_LOOP_SRP_UNIT_US` at 280 and a build of one at 735; `rows_tiers.py`'s slice control; and `selftest_round.py`. That drops this branch's own slice commits.
- **Costs:** each is the side's that moved it from `9606b3a9`, the larger where both did. At 1x1/1if:
  - AECP's timer slot is this branch's 75 (#894: 70);
  - the TICK, the build of one and the owed MRPDU are #894's (55, 735, 735);
  - MAAP's record, a pass's events' fixed part and the polls' base are this branch's (115, 35, 215).
- **The pace:** the rule gives 9 ms at the composed tables (txL 52.09 at 8, 48.40 at 9).

At the composed tables the built 950 us design's last queued notice is **134.74 ms**, over 130, and it is over at every slice from 650 to 1,100 us. The rule's best is 1,200 us (+0.0004), outside the range, so `ruled` falls back to 800.

The sensitivity at those tables: every row holds at 950 us once the polls' base and a pass's events' fixed part come to 240 us together (205 + 35: last 127.85, +0.0165), and none at 245.

### 2. The polls' base, attributed

`acmp-cmd`'s heaviest base, by `poll_grade`'s own measure:
- #902's `234bc149`: **19,074 cycles** (205 us by the rule);
- the merge: **20,453** (215).

The +1,379 cycles fall in AECP's poll (+625) and its delivery (+840), whose code this branch does not change. The Talker's own polls are cheaper: MAAP's −6, SRP's delivery −290. The pass runs +82 instructions with 17 refills fewer and 145 cycles less in all, so this is placement (#909), not Talker instructions.

### 3. Item 3's cut and the image measured again

`f14e56a9` is the one cut. `srp_mbx_gate`, the Talker's per-pass check, returns at once on the gate and base its last call left. Only init and the entry write what it reads, so it is exactly behaviour-neutral with no wire change.
- Plant `talker-gate-repeat-ignores-its-base` (35 Talker plants) is caught by `Talker.DestinationChangeWhileValidWithdrawsTheOld` and `Talker.ResetKeepsAnUnchangedSourceAndHoldsAMovedOne` at 1 and 2 interfaces.
- The talker, srp-acmp, port, portable and unit arms PASS.

Measured again on the cut's image at 1x1/1if: arm A's 96 groups, `answering-every-port`, `valid-destinations`, and arm B's `aecp`, `aecp-largest-notice` and `aecp-fanout`.
- Every leg exits rc 0 with 0 refusals and 0 `STATED` lines; arm A has its 7 known misses.
- The joins are 359 intervals, 188.102 to 190.121 ms.
- `acmp-cmd`'s base falls to 19,736 (−717). But **`save-held`'s base is 21,094 cycles** (19,793 at 7A's head): 262 instructions fewer, 49 more refills, placement again.
- The survey: **UNDER 2**. The polls' base is restated **215 -> 225** in both tables (`2657af21`); every other cost is within.

### 4. At the final tables (head `0c93071e`, clean clone)

1x1/1if by every source, ms:

| Row | 950 us (built) | Bound |
|---|---:|---:|
| R4 | 13.30 | 20 |
| R5 / R6 | 75.89 / 73.41 | 90 |
| first queued notice | 14.77 | 20 |
| **last queued notice** | **135.43** | 130 |
| R4L | 203.62 | 238 |
| ACMP / ADP / MAAP | 29.68 / 27.91 / 28.01 | 30 |
| tx | 34.05 (`CTRL_LOOP_TX_MS` states 34) | 49 |
| txL | 48.63 | 49 |

- **No grid slice from 650 to 1,100 us holds every row.**
  - The best is 950 us at −0.0418, the last queued notice binding at 135.43 to 167.39 across the range.
  - The rule's best overall is 1,200 us at −0.0043, where txL is 49.21, over 49.
  - `tier_grid.py`: 0 of 420 hold. `rows_tiers.ruled` = 800 (its fallback).
- **The tree's own controls report it:**
  - `flip_grade.py --check`: FAIL.
  - `rows_tiers.py --selftest` 1031/1033: "the built design's slice not the rule's" and "THE TRANSMIT's stated figure under its row" (34 against 34.05; at 8x8/2if 98 against 98.99).
  - `flip_grade.py --selftest` 584/585: the queued bound, which the amendment's rule would put at 140 for 135.43.
- **Not stops:** the pace is 9 ms (≤ 11); the load is 0.517 / 0.514 (≤ 0.70); the joins are within 181 to 239.
- **ROM** (`plat_ledger.py` PASS at the cut's head) is within every entry: the platform 8x8/2if is at 60.5 (1,368 B left); the fixture and both harness arms are at 59.0 (368, 60 and 200 B left); every other point is ≤ 56. There is no lwSRP change.

### 5. Not run, at the stop

- 8x8/2if's legs on the cut's image: its rows are the composed tables', reported.
- The gates, the full pass and the sweep.

### Options (not chosen here)

- **(a)** A placement cut for #909: the heaviest base moves with code placement, and #902's own image is 205 by the rule. That is a second cut, past item 3's one.
- **(b)** A bound or slice-range decision. At the rule's 1,200 us, txL is over too.
- **(c)** Measure #895 again on #902's merged head, in the ruling's order (#902, then #901).

The receipts are in the round's packet (7B/: legs, survey, attribution, graders, ledgers, the cut's arms and its plant). Nothing was pushed.
