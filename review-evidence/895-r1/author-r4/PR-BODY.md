[A775]

## Contents

- **[Status](#status)** — STOPPED at the sync merge of #902's head: the composed 1x1/1if flip check and the 8x8/2if platform image's ledger entry each need a decision.
- **[Linked Issue / roles](#linked-issue--roles)** — Public tasks, executor, and independent reviewers.
- **[Round 4](#round-4)** — The sync with #902's head, and what each item of the round's assignment found.
- **[The composed 1x1/1if flip check](#the-composed-1x11if-flip-check)** — Every row against #902's head, the cause, and the pace #894's rule takes.
- **[The CPU budget harness at the merge](#the-cpu-budget-harness-at-the-merge)** — Every arm at both points, against the merged figures.
- **[ROM ledger](#rom-ledger)** — Every point, at #902's head and composed.
- **[Description](#description)** — The validity gate and the declarations (rounds 1 and 2), and each source's stream_id (#905).
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this does not do, and the items for a decision.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**STOPPED** at `91c3fc0e8c3daebd586f4fb0b1c0aa9881d9e337` (`895-talker-redeclare` -> `dev-soft-core`), round 4. **Not REVIEW READY.**

The branch history:
- Rounds 1 to 3 to `9e30c2c3`. Round 3 ended in its second STOP, answered by the ruling issuecomment-6864645058: hold until #902 merges, then a sync round.
- Round 4 merges #902's head `5b264bf2` (`894-tiers`, which carries dev-soft-core `cec88385`) by one merge commit, `a93fceae`.
- `894-tiers` moved during the round to `7398ec0a`: the map table held to its declared slots, its plants, and docs. It is merged by a second merge commit, `91c3fc0e`. #902 is open.

No rebase, no force, no amend. No RTL, mailbox-contract, tsn-c-stack, lwSRP or donor change. No bound, cap, ceiling, ledger entry, pace or stated figure was changed: the merge takes each side's.

**Two checks fail on the composed tree, and closing either changes a figure that is not this lane's:**
1. **The composed 1x1/1if flip check fails** ([below](#the-composed-1x11if-flip-check)). txL is 49.20 ms against 49, and the tx row is 33.01 ms against `CTRL_LOOP_TX_MS`'s 30. The one cost behind it is MAAP's record at 1x1/1if, which #895 states at 115 µs and #902 at 90. #894's pace rule takes 9 ms on the composed tables. Ruling 6867393730 (d) has #901 pass this check composed with #902, or wait behind the flip.
2. **The 8x8/2if platform image plans 60.5 RAMB36,** and its 60.0 entry refuses it: 131,256 B of rom, 184 B past 131,072 ([ROM ledger](#rom-ledger)). The owner's cap is 60.5, and ruling 6844175391 stops only "over 60.5"; the entry stays 60.0.

What ran at the merge:
- **The merge's own checks:** the firmware arms (unit, talker, maap, maap_if2, acmp, acmpif2, the SRP composition at one and two interfaces, platboot) PASS; coverage written, every file at 100 %; no planted-defect anchor broken.
- **The CPU budget harness,** every group of every arm at 1x1/1if and 8x8/2if, on a clean clone ([below](#the-cpu-budget-harness-at-the-merge)).
- **The analytical graders** on the composed tree and on #902's clean clone: `flip_grade.py`, `tier_grid.py`, `load_grade.py`.
- **The ROM ledger** on both.

Not run: `SPLIT_CONTROL_MEMORY.md` section 13's restatement, the clean-clone gate pass (workflows, the Verilator sweep, the full firmware campaigns) and act. They wait on the decisions.

## Linked Issue / roles

Relates to #895
Relates to #905 (acceptance 1 to 3 and 5 here; 4 is the bench run)
Relates to #894 (#902 merged here; its names patch carried unchanged)
Relates to #906, #907 (srptx findings, not fixed here)
Relates to #909 (the data-cache placement, not fixed here)
Relates to #896
Relates to #665

Executor: `[A775]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Round 4

| Item | What answers it |
|---|---|
| 1, the sync | One merge commit, `a93fceae`, of #902's head `5b264bf2`; merge base `084cf7a8`; submodule pins equal on both sides. 8 files conflicted, each resolved from the composed tree (table below), and one semantic conflict. #894 does not carry the names patch; this branch carries it once. `894-tiers` then moved to `7398ec0a`, merged as `91c3fc0e`. Its one conflict, section 13's intro, keeps #895's paragraphs and #894's label of the load table. The ledger and the flip check are identical at both merges; coverage `--check`, `aecp_arms.py --core` (83 tests) and the unit and talker arms pass at the second. |
| 2, the harness | Every arm at both points against the merged figures (#902's build of one at 725 µs at one interface, its bounds and costs). The 1x1/1if `valid-destinations` leg, round 3's STOP, now passes: its longest build 48,103 cycles against 72,500. `cd863d40` and `cf5b1441` are kept. |
| 3, acceptance 4 composed | **The 1x1/1if flip check fails** on the composed tables (txL 49.20 / 49). The load holds: 0.514 at the pin, 0.510 with tsn-c-stack#32. The ROM ledger's 8x8/2if platform image is refused at 60.5. The fixture and both harness arms are 59.0, within #894's 59.0 entry; 58.5 cannot be reached, since #902's own fixture is 59.0. Every other point is at most 56. Deltas against #902's head are in each table below. |
| 4, section 13 and the figures | Not restated: they wait on the decisions. `[TIME]` (#906) and the hold `[TX]` (#907) stay recorded as pre-existing in the milan_dp README, unchanged. |
| 5, gates and the full pass | Not run (the STOP). |

The conflicted files:

| File | Resolution |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.c` | #894's `SRP_JOIN_CS CTRL_LOOP_JOIN_CS` (19 cs, the loop's), with #895's `SRP_REDECLARE_CS` on it. Its comment now names `CTRL_LOOP_TX_MS` as the built design's MRPDU by every source, which it is under the tiers. The hold-off is 2,022 cs at 1x1/1if (2,023 before: JoinTime 20 -> 19 cs) and 2,029 at two interfaces. |
| `sw/firmware/ctrl/aecp/aecp_shape.py` | #894's key domain on the constants line, plus the names patch's runs and tuple ordinals. |
| `tb/verilator/ctrl_service_budget/load_grade.py` | No cost key was moved by both sides from `084cf7a8`, so each key takes the side that moved it. The tables are #902's, with MAAP's record #895's: 115 µs at 1x1/1if and 150 at 8x8/2if, in both columns. The comments are both sides'. |
| `sw/firmware/gtest/coverage.ratchet` | Measured on the composed tree (`fw_coverage.py --write`). `srp_mbx.c` is 736/736 lines and 663/663 branches; every file is at 100 %. |
| `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py` | #894's 59.0 fixture entry and reason, with #895's sentence. `ctrl_plat` is 17,536, 19,072, 18,176 and 20,352 B, as `plat_ledger.py` measures the composed images. |
| `docs/design/SPLIT_CONTROL_MEMORY.md`, `sw/firmware/ctrl/plat/README.md` | Both sides' text, with the composed figures. The platform README states the 60.5 plan and its refusal. |

**The semantic conflict.** #894 gives THE TRANSMIT's client a `most` argument, and two `srp_talker.cpp` calls did not compile.
- `TransmitPublishesWithinItsTermsAfterARefusedJoin` now makes the call as the loop does, with `CTRL_LOOP_BUILD_MOST`, and repeats it while the build resumes. Its publication counts stay the whole build's.
- `RefusedWithdrawalIsWithdrawnOnceLwsrpTakesIt` passes `CTRL_LOOP_BUILD_MOST`. Its build is refused at its first MRPDU, so nothing resumes.

## The composed 1x1/1if flip check

`flip_grade.py --check --point 1x1/1if`, on #902's clean clone and on the composed tree:

| Row | Bound, ms | #902 `5b264bf2` | Composed | Delta |
|---|---:|---:|---:|---:|
| R4 | 20 | 12.85 | 12.90 | +0.05 |
| R5 | 90 | 72.91 | 73.19 | +0.28 |
| R6 | 90 | 68.80 | 69.07 | +0.27 |
| first | 20 | 14.51 | 14.57 | +0.06 |
| last | 130 | 126.46 | 126.78 | +0.32 |
| R4L | 238 | 188.39 | 188.44 | +0.05 |
| ACMP / ADP / MAAP | 30 | 28.44 / 26.83 / 26.95 | 28.66 / 27.05 / 27.15 | +0.22 / +0.22 / +0.20 |
| tx | 49 (`CTRL_LOOP_TX_MS` states 30) | 29.86 | **33.01** | +3.15 |
| txL | 49 | 48.09 | **49.20** | +1.11 |
| result | | PASS | **FAIL** | |

- `tier_grid.py --point 1x1/1if`: 0 of 420 designs hold, against #902's 18 (900 µs chosen).
- `load_grade.py --check` holds: 1x1/1if 0.514 at the pin and 0.510 with tsn-c-stack#32 (#902: 0.513 / 0.509). 8x8/2if is 0.793 / 0.753, reported.

**The cause is one cost.** #902's own tree with only the composed `load_grade.py` gives the same 49.20 and 33.01. The composed tables differ from #902's only in MAAP's record:
- #895 states it at 115 µs at 1x1/1if: round 2's measurement on its arms of a range lost to a peer's ANNOUNCE, which restarts the core.
- #902 states it at 90.
- The extra 25 µs add one pass to the tx and txL rows (16 -> 17 and 23 -> 24).

At the merge, the legs measure MAAP's record at **9,536 cycles** (`valid-destinations`' `srp-talker-loss`), **105 µs** by the rule. Section 13's rule takes each cost as the larger of the measurement and the table's, so 115 stands.

**#894's pace rule takes 9 ms on the composed tables.** The rule is `paced_rows.choice`; #894's round 9 ruling, item 4: "the smallest P holding txL at most 49 ms and R4L at most 238 ms".

| P, ms | txL | R4L |
|---:|---:|---:|
| 7 | 49.94 | 173.44 |
| 8 (stated) | 49.20 | 188.44 |
| 9 | 47.60 | 203.44 |
| 10 | 46.01 | 218.44 |

The tx row is 33.01 at every pace. A scratch check, not committed: with `AECP_PACE_MS` 9 and `CTRL_LOOP_TX_MS` 34 at 1x1/1if the check passes (txL 47.60, tx 33.01 of 34, R4L 203.44).

**Options for the decision:**
- (a) #901 restates both of #894's figures by #894's own rules, with what moves with them: FR_NFR 3.4.1's and section 13's 8 ms rows, and `SRP_REDECLARE_CS` by +1 cs.
- (b) #895 takes the Talker's work out of the MAAP record (a design change, then re-measured).
- (c) #901 waits behind the flip.

## The CPU budget harness at the merge

Every group of every arm, at 1x1/1if and 8x8/2if, against the merged figures, on a clean clone of `a93fceae` (`run.py --record-budget-findings --record-share-findings`). Arm A ran in five parts a point, then was merged and regraded as one leg. The second merge, `91c3fc0e`, changes only the map table and docs, and was not run through the legs again.

| Point | Arm | Groups | Refusals | Budget misses | Passes over the share | rc |
|---|---|---:|---:|---|---|---:|
| 1x1/1if | A (5 parts, merged) | 96 | 0 | 7 of 950 | 0 of 134,749 | 0 |
| 8x8/2if | A (5 parts, merged) | 94 | 0 | 7 of 994 | 0 of 230,855 | 0 |
| 1x1/1if | `answering-every-port` | 16 | 0 | 0 of 280 | 0 of 20,903 | 0 |
| 8x8/2if | `answering-every-port` | 16 | 0 | 0 of 736 | 0 of 16,050 | 0 |
| 1x1/1if | `valid-destinations` | 2 | 0 | 0 of 5 | 0 of 2,668 | 0 |
| 8x8/2if | `valid-destinations` | 2 | 0 | 0 of 20 | 0 of 3,053 | 0 |
| 1x1/1if | B (`aecp`) | 1 | 0 | 0 of 25 | 0 of 112 | 0 |
| 8x8/2if | B (`aecp`) | 1 | 0 | 0 of 39 | 0 of 140 | 0 |

- No leg prints a `STATED` line, and every leg exits 0.
- Round 3's STOP, the 1x1/1if `valid-destinations` leg, passes against the merged 725 us build of one: its longest THE TRANSMIT build is 48,103 cycles. At 8x8/2if the longest is 48,811 against the 1,300 us slice.
- 1,091 join intervals in 227 group runs, 185.905 to 190.192 ms.

- **The budget misses** are arm A's seven `backlog-owed` rows, 61.8 to 63.7 ms against 20. The scenario's 60 ms egress hold sets them (ruling 6871343905 (a): recorded misses, the same rows at 1x1/1if and 8x8/2if). No other row misses.
- **Join intervals** hold #894's commit-side gate, 181.0 to 239.0 ms, in every group of every leg.

**The measured costs against the composed tables.** Round 1's parsers (`parts.py`, `eventcost.py`, `costs24.py`, `aecp_kinds.py`, S2b's, unchanged) read every leg; they predate THE TIERS. At 1x1/1if, with the largest legal command's group apart, three costs are over their statement. Each is compared on the same group at #902's head, a leg of that head (`T4-*`) or #894's own final-pass legs:

| Cost, 1x1/1if | Stated | Composed, cycles (us by the rule) | #902's head, same group | What moved |
|---|---:|---|---|---|
| MAAP's record | 115 (#895), 90 (#902) | 9,536 (105), `srp-talker-loss` | (no such arm) | #895's arm; 115 stands by the rule |
| AECP's timer slot | 65 | 6,805 (75), `notice-burst-1` | 6,188 (65) | inside `aecp_mbx:event`, 3,469 -> 4,196; the pass 4,321 against 4,234 instructions, instruction refills 119 against 106: layout, not traced |
| the TICK | 45 | 4,385 (50), `backlog-adp@blank-0` | 3,241 (35) | the dearest TICK now carries AECP's work (`aecp_mbx:event` 1,310, `aecp:transmit` 360): the event's composition |
| an AECP record | 235 | 28,173 (300), `aecp-fanout` | 27,851 (295) | not this composition's |
| the largest legal command's record | 975 | 92,046 (970), `aecp-largest-notice` | 91,625 (965) | within its statement |

- On #894's own final-pass groups (`notice-every-0`, `datapath-events`, `srp`, `aecp-largest-notice`, `backlog-owed`) no cost is dearer at the merge.
- Fed into the tables by section 13's rule, in a scratch copy, not committed:
  - **the composition's moves alone** (MAAP 115, the AECP slot 75, the TICK 50): txL 49.46 and tx 33.20. The rule's pace is still 9 ms (txL 47.86, R4L 203.48), so option (a) above holds with them.
  - **with the AECP record's 300 too:** txL 53.53, last 135.85 (130), ACMP 33.64 (30). The rule's pace would be 10 ms, and last and ACMP stay over at any pace. That 300 is measured at #902's head too, at 295, so it is for #894.
- **At 8x8/2if (reported, not held):** the AECP slot 115 (105), the TICK 55 (40), a pass's events' fixed part 35 (30), MAAP's record 155 (150). Not compared with #902's head.
- Section 13 and the tables are not restated: they wait on the decisions.

## ROM ledger

RV32 images linked by each tree's own `ctrl_srp_image.py` and `ctrl_plat_image.py`, on each shape's split export and runtime (`plat_ledger.py`'s). #902's head was built on a clean clone, the composed tree on the merge's worktree. Figures are rom / sram need in B, then RAMB36.

| Point | Image | Entry or budget | #902 `5b264bf2` | Composed | Delta, rom / sram |
|---|---|---:|---|---|---:|
| 1x1/1if | fixture | 56 | 110,576 / 55,152: 40.5 | 111,928 / 55,184: 41.0 | +1,352 / +32 |
| 1x1/2if | fixture | 56 | 111,872 / 57,312: 41.5 | 113,472 / 57,360: 42.5 | +1,600 / +48 |
| 8x8/1if | fixture | 56 | 124,104 / 96,240: 54.0 | 124,608 / 96,288: 54.5 | +504 / +48 |
| 8x8/2if | fixture | 59.0 | 125,368 / 113,168: 59.0 | 126,112 / 113,232: 59.0 (864 B left) | +744 / +64 |
| 8x8/2if | harness `answering-every-port` | 59.0 | 125,676 / 113,232: 59.0 | 126,420 / 113,296: 59.0 (556 B left) | +744 / +64 |
| 8x8/2if | harness `valid-destinations` | 59.0 | (no such arm) | 126,280 / 113,232: 59.0 (696 B left) | |
| 1x1/1if | platform | 56 | 115,640 / 56,224: 42.5 | 116,992 / 56,224: 43.0 | +1,352 / 0 |
| 1x1/2if | platform | 56 | 116,952 / 58,336: 43.5 | 118,560 / 58,400: 43.5 | +1,608 / +64 |
| 8x8/1if | platform | 56 | 129,208 / 97,264: 56.0 | 129,720 / 97,264: 56.0 (1,352 B left) | +512 / 0 |
| 8x8/2if | platform | 60.0 (cap 60.5) | 130,504 / 114,160: 60.0 | **131,256 / 114,224: 60.5, refused** | +752 / +64 |

- **`ctrl_plat`** is 17,536, 19,072, 18,176 and 20,352 B composed; #902's is 17,536, 19,008, 18,176 and 20,288. At one interface the tiers' 64 B and the Talker's take the same padding.
- **The 8x8/2if fixture and harness arms.** 58.5 cannot be reached: #902's own fixture is 59.0, 440 B past 58.5. Each composed image is within the 59.0 entry #894 carries, by ruling 6844175391 item 2's fallback ("the final composed fixture or harness image"), which is also #895's fallback in 6857334948.
- **The platform's options:** raise its entry to the owner's cap, 60.5, as the fixture's was raised to its cap (ruling 6831583372); or recover 184 B of rom.

## Description

### Validity and the declarations (rounds 1 and 2, unchanged)

A source declares its MSRP Talker only while its SRP parameters are valid: MAAP holds its destination, and a probe of the last 15 s or a registered Listener asks for it (Milan v1.2 4.3.3.1, 5.3.7.4).
- It declares at once, Talker Advertise with base + n and its TSpec, or Talker Failed (code 1) when its bandwidth does not fit.
- A lapse withdraws it, its licence and TALKER_DECL bit first. A Leave lwSRP refuses stays owed until lwSRP takes it.
- An unchanged destination is declared again at once. A changed one waits two LeaveAllTime periods after the Leave (IEEE 802.1Q-2018 35.2.2.8, Table 10-7), plus a JoinTime and THE TRANSMIT's MRPDU by every source, so the count covers the Leave's own lateness. Under the tiers the JoinTime is the loop's, 19 cs.

Under THE TIERS, the declarations ride THE TRANSMIT's slices. A slice that holds one MRPDU makes the MSRP one, and the next makes the MVRP one and that interface's declarations. The Talker's licence still waits for the MVRP commit (Milan v1.2 4.3.2).

### Each source's stream_id (#905, unchanged this round)

The datapath stamps each source's `SRC_SID_HI:SRC_SID_LO` on its AVTPDUs. The contract (`KL_mbx_pkg.sv:345`) says the owner writes both words while the source's `DA_GATE` bit is clear.
- The MAAP adapter (`maap_mbx.c`), which owns `DA_GATE`, writes them through `mbx_pub_src_sid`: every source's at its start, before any pass and any bit opens, and again before each reopening.
- Its state is 8 B of `struct maap_mbx` (`cd863d40`).
- Four `SrpGate.F905A*` tests at 1x1/1if, 1x1/2if and 8x8/2if, five plants, and srptx's `[SID]` check.

## Authoritative references

- #895 rulings issuecomment-6857334948 and issuecomment-6864645058. #894 rulings 6867990126 (the egress bounds: MRPDU 49 ms, paced R4L 238 ms, the join gate 181 to 239 ms), 6867393730 (d), 6870437042 (item 4, the pace rule) and 6844175391 (item 2). The owner's decision issuecomment-6824896581 (#665).
- `hdl/milan/mailbox/KL_mbx_pkg.sv` SRC_SID_LO and SRC_SID_HI (contract 2.4), DA_GATE; `docs/reference/MAILBOX_CONTRACT.md`.
- IEEE 1722-2016 4.4.4.8; IEEE 1722.1-2021 7.2.3 and 9.3.2.6; IEEE 802.1Q-2018 10.7.11, 35.2.2.8, Table 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 4.3.2, 4.3.3.1, 5.3.7.4, 5.3.7.5.
- `docs/design/SPLIT_CONTROL_MEMORY.md` sections 5, 9 and 13; FR_NFR.md 3.4.1; `sw/firmware/ctrl/loop/ctrl_loop.h` (`CTRL_LOOP_TX_MS`, `CTRL_LOOP_JOIN_CS`, `CTRL_LOOP_BUILD_ONE_PASS_US`); `sw/firmware/ctrl/aecp/aecp_mbx.h` (`AECP_PACE_MS`).

## How to get into the same state

```sh
git fetch origin 895-talker-redeclare && git checkout 91c3fc0e8c3daebd586f4fb0b1c0aa9881d9e337
git submodule update --init --recursive
# the product LiteX tree's environment, the pinned RV32 SDK on PATH, Verilator 5.050,
# COURSIER_MODE=offline, SBT_OPTS=-Dsbt.offline=true, PYTHONHASHSEED=0
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # rc 1: txL 49.20 over 49; tx 33.01 over CTRL_LOOP_TX_MS 30
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                   # rc 0: 0.514 / 0.510
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if            # rc 1: 0 of 420 hold
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/pl          # rc 1: TILES 8x8-if2 60.5 past 60
python3 sw/firmware/gtest/fw_coverage.py --check                                    # PASS, 39 files
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant valid-destinations \
  --build-dir /tmp/w1 --record-budget-findings --record-share-findings              # rc 0
```

## Known limitations / out of scope

- **The STOP:** the composed flip check and the platform's ledger entry, above. This lane changes neither #894's figures nor a ledger entry.
- **Layout sensitivity (#909):** the split stack moves with every `.bss` change ([section 9](../docs/design/SPLIT_CONTROL_MEMORY.md#where-the-stack-falls-in-it)); it is not fixed here.
- **Not run this round:** section 13's restatement, the clean-clone gate pass and act.
- **Found before, for their own issues:** srptx `[TIME]` (#906) and the hold `[TX]` path (#907), recorded in the milan_dp README.
- **8x8/1if** is lane 894b's (ruling 6867393730 (b)). Its harness point was not run here: #902's own 8x8-1if legs exit 1 by design.
- **Round 2's items stand:** the Domain's own leave and join on the refused path, and the Domain adoption's in-place VID change, each for its own issue. The bench run (#895 acceptance 6, #905 acceptance 4) is the bench lane's.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#895 acceptance 4 composed: the STOP)
- [x] Required tests pass for the merge's firmware (arms, coverage); the full gate pass is not run
- [ ] Current PR head has a successful `rtl-fast` verdict
- [ ] Exact-head `verilator-suites` and `yosys-portability` after ready
- [x] No undocumented requirement/interface change
- [ ] Internal cleared-context review POSITIVE at the exact head
- [ ] External review POSITIVE at the exact head
- [ ] Every review lens covered clean at the merge candidate
- [ ] Candidate merge validated, post-merge containment clean
