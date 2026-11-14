[A775] STOP — round 4, head `91c3fc0e8c3daebd586f4fb0b1c0aa9881d9e337` (local, not pushed)

The head is two sync merges of #902's branch `894-tiers`:
- `a93fceae` of `5b264bf2`, which carries dev-soft-core `cec88385`;
- `91c3fc0e` of `7398ec0a`, after the branch moved during the round.

#902 is open.

**Why: the composed 1x1/1if flip check fails, and the 8x8/2if platform image is refused by its ledger entry.** Closing either changes a figure that is not this lane's. No bound, cap, ceiling, ledger entry, pace or stated figure was changed.

### 1. The composed 1x1/1if flip check fails

Ruling 6867393730 (d): #901 must pass this check composed with #902, or wait behind the flip. `flip_grade.py --check --point 1x1/1if`:

| Row | Bound, ms | #902 `5b264bf2` | composed |
|---|---:|---:|---:|
| txL | 49 | 48.09 | **49.20** |
| tx | 49 (`CTRL_LOOP_TX_MS` states 30) | 29.86 | **33.01** |
| R4L | 238 | 188.39 | 188.44 |
| last | 130 | 126.46 | 126.78 |
| ACMP / ADP / MAAP | 30 | 28.44 / 26.83 / 26.95 | 28.66 / 27.05 / 27.15 |

The other graders on the composed tree:
- `tier_grid.py --point 1x1/1if`: 0 of 420 designs hold (#902: 18, 900 us chosen).
- `load_grade.py --check` holds: 0.514 at the pin, 0.510 with tsn-c-stack#32 (#902: 0.513 / 0.509).

The cause is one cost, MAAP's record at 1x1/1if:
- #895 states it at 115 us: round 2's measurement of a range lost to a peer's ANNOUNCE, which restarts the core. #902 states 90.
- No cost key was changed by both sides, so the composed tables are #902's with that one key #895's.
- #902's own tree with only the composed `load_grade.py` gives the same 49.20 / 33.01. The extra 25 us add one pass to tx and txL.
- At this head the legs measure it at 9,536 cycles, 105 us by the rule. Section 13's rule keeps the larger, 115.

#894's pace rule takes **9 ms** on the composed tables (`paced_rows.choice`; ruling 6870437042, item 4). The tx row does not depend on the pace.

| P, ms | txL | R4L |
|---:|---:|---:|
| 8 (stated) | 49.20 | 188.44 |
| 9 | 47.60 | 203.44 |
| 10 | 46.01 | 218.44 |

A scratch check, not committed: `AECP_PACE_MS` 9 with `CTRL_LOOP_TX_MS` 34 at 1x1/1if passes (txL 47.60, tx 33.01 of 34, R4L 203.44).

**The legs' measured costs push it further.** These fall under the assignment's layout (#909) condition, stated and not fixed. They come from round 1's parsers, which predate THE TIERS, compared group by group with #902's head:
- **AECP's timer slot:** 6,805 cycles (75 us; stated 65). The same group at #902's head is 6,188 (65).
  - The difference is inside `aecp_mbx:event` (3,469 -> 4,196). #895 changes neither the AECP core nor its adapter (`aecp.c`, `aecp_mbx.c`); the names patch's `aecp_nvm` takes 143 cycles in that pass against 146.
  - The pass that holds it runs 4,321 instructions against 4,234, and refills the instruction cache 119 times against 106 (+1,130 cycles).
  - So it is the layout moving (code placement), the instruction-side form of what #909 records for data. It was not traced to a function.
- **The TICK:** 4,385 (50; stated 45), against 3,241 at #902's head.
  - The composed head's dearest TICK carries AECP's work (`aecp_mbx:event` 1,310, `aecp:transmit` 360); #902's carries none.
  - So the event's composition moved, not the same work.
- **The AECP record:** 28,173 in `aecp-fanout` (300; stated 235). #902's head measures 27,851 (295) on the same group, so it is not this composition's.

Graded with those fed in by section 13's rule:
- **The composition's own moves alone** (115, 75, 50): txL 49.46 and tx 33.20. The rule's pace is still 9 (txL 47.86, R4L 203.48).
- **Adding the AECP record's 300:** txL 53.53, last 135.85 (130), ACMP 33.64 (30). The rule's pace would be 10, and last and ACMP stay over at any pace.

**Options:**
- **(a)** #901 restates both of #894's figures by #894's own rules: the pace 8 -> 9 ms and `CTRL_LOOP_TX_MS` 30 -> 34 ms at 1x1/1if. With them move FR_NFR 3.4.1's and section 13's 8 ms rows, and `SRP_REDECLARE_CS` by +1 cs.
- **(b)** #895 takes the Talker's work out of the MAAP record (a design change, then re-measured).
- **(c)** #901 waits behind the flip.

Separately, the AECP record that #902's head already measures at 295 us is for #894.

### 2. The 8x8/2if platform image plans 60.5 RAMB36; its 60.0 entry refuses it

- 131,256 B of rom, 184 B past 131,072. #902's is 130,504 B (568 B left); #895 adds +752 B rom and +64 B sram.
- `plat_ledger.py` FAIL: `TILES 8x8-if2: 60.5 RAMB36 past the 60 its override ledgers`.
- The owner's cap is 60.5 ("may plan 60.0, with a cap of 60.5", 6824896581), and ruling 6844175391 stops only "over 60.5". The entry is still 60.0.
- **Options:**
  - raise the entry to 60.5, as the fixture's was raised to its own cap (6831583372);
  - or recover 184 B.

### 3. Stated, not a STOP: the fixture and both harness arms at 8x8/2if are 59.0

| Image | #902 | composed |
|---|---|---|
| fixture | 125,368 B | 126,112 B (864 B left) |
| `answering-every-port` | 125,676 B | 126,420 B (556 B left) |
| `valid-destinations` | (none) | 126,280 B (696 B left) |

- 58.5 is out of reach: #902's own fixture is already 59.0.
- Each is within the 59.0 entry #894 carries by ruling 6844175391 item 2's fallback ("the final composed fixture or harness image"). That is #895's fallback in 6857334948 too.
- Every other point is at most 56:
  - platform 43.0, 43.5, 56.0 (8x8/1if, 1,352 B left);
  - fixture 41.0, 42.5, 54.5.

### The merges

**`a93fceae`.** Eight files conflicted:
- `srp_mbx.c`: #894's `SRP_JOIN_CS CTRL_LOOP_JOIN_CS` (19 cs), with #895's hold-off on it (2,022 cs at 1x1/1if).
- `aecp_shape.py`: #894's key domain, plus the names patch's runs. #894 does not carry the names patch; it is here once.
- `load_grade.py`: each cost from the side that moved it.
- `coverage.ratchet`: measured. `srp_mbx.c` is 736/736 and 663/663; every file is at 100 %.
- `ctrl_memory.py` and `ctrl_memory_ledger.py`: #894's 59.0 entry, and `ctrl_plat` as measured (17,536 / 19,072 / 18,176 / 20,352 B).
- `SPLIT_CONTROL_MEMORY.md` and the platform README: both sides' text, with the measured figures.

One semantic conflict: #894's THE TRANSMIT takes `most`. Two `srp_talker.cpp` calls now make the call as the loop does, and resume its build. Planted-defect anchors: none broken. The firmware arms pass (unit, talker, maap, maap_if2, acmp, acmpif2, the SRP composition at one and two interfaces, platboot).

**`91c3fc0e`.** #902's three new commits: the map table held to its declared slots, its plants, and docs. One conflict, in section 13's intro, composed. Checked before committing:
- ledger and flip identical to `a93fceae`'s;
- `fw_coverage.py --check` PASS;
- `aecp_arms.py --core` 83 PASS;
- arms unit and talker PASS.

### The CPU budget harness

Every group of every arm at 1x1/1if and 8x8/2if, against the merged figures, on a clean clone of `a93fceae`. The second merge changes only the map table and docs. Arm A ran in five parts a point, then was merged and regraded.

| Point | Arm | Groups | Refusals | Budget misses | Passes over the share | rc |
|---|---|---:|---:|---|---|---:|
| 1x1/1if | A | 96 | 0 | 7 of 950 | 0 of 134,749 | 0 |
| 8x8/2if | A | 94 | 0 | 7 of 994 | 0 of 230,855 | 0 |
| 1x1/1if | `answering-every-port` | 16 | 0 | 0 of 280 | 0 of 20,903 | 0 |
| 8x8/2if | `answering-every-port` | 16 | 0 | 0 of 736 | 0 of 16,050 | 0 |
| 1x1/1if | `valid-destinations` | 2 | 0 | 0 of 5 | 0 of 2,668 | 0 |
| 8x8/2if | `valid-destinations` | 2 | 0 | 0 of 20 | 0 of 3,053 | 0 |
| 1x1/1if | B (`aecp`) | 1 | 0 | 0 of 25 | 0 of 112 | 0 |
| 8x8/2if | B (`aecp`) | 1 | 0 | 0 of 39 | 0 of 140 | 0 |

- No `STATED` line anywhere. Round 3's 1x1/1if `valid-destinations` leg passes: its longest build is 48,103 cycles against 725 us.
- The misses are arm A's seven `backlog-owed` held-egress rows (ruling 6871343905 (a)).
- 1,091 join intervals, 185.905 to 190.192 ms, all within 181.0 to 239.0.
- 8x8-1if is not run (lane 894b's).

### Not done this round

- `[TIME]` (#906) and the hold `[TX]` (#907) stay pre-existing and are not fixed.
- Section 13's restatement, the gates and the full pass are not run. They wait on the decisions above.
