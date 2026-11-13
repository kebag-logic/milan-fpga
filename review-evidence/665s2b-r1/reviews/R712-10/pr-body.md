[A683zp]

## Contents

- **[Status](#status)** — REVIEW READY at the head below: round 31, docs only, on round 30.
  - Round 31: the ruling on R711-9 and R712-9, three items, one commit each, in docs and the ledger's reason strings.
  - Round 30: the ruling on round 29's items, and the merge of the TSN stack pin move's round 4 head, which carries `dev-soft-core` `0fb66211`.
  - Each of the round's three STOPs, as ruled: the size fixture at 58.5, the record mover's host port, and the stated costs.
  - The re-grade on the composed image and the full pass, once, on clean clones.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — Rounds 31 and 30 item by item, the re-grade at the merge, and what holds at this head; rounds 29 and 28 as they stood.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result, and the evidence at this head.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner and the manager.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**REVIEW READY at `084cf7a8455e9fa8e24a0e5bcf57c9557816c819`** (`665-s2b-cycles` -> `dev-soft-core`).
- **Round 31** is three ordinary commits on round 30's head `32551422`, the manager's sync merge of `dev-soft-core` `e5f88a8e`, whose tree is `5bea2597`'s. They change `docs/design/SPLIT_CONTROL_MEMORY.md` and two reason strings in `sw/litex/ctrl_memory.py`: no code, cost, bound, ledger figure or gate.
- Round 29's head is `b2d39235`. On it: nine ordinary commits (the ruling's items 1 to 3), then one merge commit of PR #892's round 4 head `8bc1dfc0`, then ten ordinary commits (the three STOPs' rulings and the re-grade).
- No rebase, no force, no amend. The tsn-c-stack submodule stays at `715589c`, with no change to tsn-c-stack, lwSRP or any donor.
- **One RTL change**, ruled into this lane on the second STOP: the record mover's CPU request is tracked to its answer, for `dev-soft-core`'s two-cycle register read. No mailbox-contract change.

**At this head:**
- **1x1/1if: 0.501 at the pin and 0.499 in the column with tsn-c-stack#32**, each held at 0.70 by `load_grade.py --check` (exit 0) on the merge's costs.
- **8x8/2if: 0.822 at the pin**, held by the flip check, which exits 1. The 8x8/2if flip waits on #890.
- **Decision D's tier bounds by every source:** 1x1/1if misses tier 1 at R4, 74.83 ms against 20 ms. The tiers are #894's.
- **THE RETRY's cold start at 8x8/2if is 185 us**, 2.7 % over its most measured cost rather than 5 %, by the ruling on the third STOP. The exception expires at the 8x8/2if flip.
- The full pass ran once at round 30's `5bea2597`, whose tree `32551422` keeps, on clean clones; round 31 ran the gates its change touches ([How to validate](#how-to-validate)).

## Linked Issue / roles

Relates to #665
Relates to #892 (the TSN stack pin move, merged here)
Relates to #894 (the tier rows by every source, model first)
Relates to #890 (the 8x8/2if flip, which this lane's flip check holds, and at which the cold start's margin exception expires)
Relates to #882 (its three acceptance items were met in round 27)
Relates to #891 (the 14-bit AEM command_type the harness works around)
Relates to #823 (the KLJ3 saved state the merge brings, whose journal and container the harness now follows)

Executor: `[A683zp]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 31

**The ruling:** the manager's, maintainer-delegated, on R711-9 (#810 issuecomment-6850590935, POSITIVE, RES-2 as residue) and R712-9 (#810 issuecomment-6850656712, NEGATIVE on two MINOR Docs findings), at `32551422`. Docs only, one commit an item, nothing re-run but the gates the change touches.

| Item | Commit | At this head |
|---|---|---|
| 1. R712-9-F1, the pin move's smallest margins | `f150b8cb` | `SPLIT_CONTROL_MEMORY.md:442` names what `0fb66211` carries as `dev-soft-core` does: #874, #880 (with KLJ3, #823), #889 and #888. `:455-456` state both regions' smallest margins at the pin move's merge, as `6eacd76d` did: 288 B of `rom` at the platform's 1x1/2if (112,352 B in 112,640) and 16 B of `sram` at the platform's 8x8/2if (114,672 B in 56 granules of 2,048), whose next granule would plan 59.5 against the 59.0 its override held there. `git diff e5f88a8e HEAD -- docs/design/SPLIT_CONTROL_MEMORY.md` keeps both statements; it differs only in "that merge" and "held there", the paragraph's framing on the pin move's branch |
| 2. R712-9-F2, section 13's least row margins | `47e44d73` | `:2323` states arm A's least margin at this head from round 30's re-grades: at most 8.162 ms at 8x8/2if (11.838 ms, group `backlog-adp@program-aged2-7`, instance `service.aecp.last.if1`) and at most 9.992 ms at 1x1/1if (10.008 ms, group `backlog-adp@verify-aged2-5`, instance `service.aecp.last.if0`), each the least of the windows opened at the age limit, the figure the re-grade prints. It says round 30 did not re-derive arm A's least over all its rows, nor the `answering-every-port` arm's at either point, since its re-grades print no table of rows, and gives round 29's 6.246, 8.973, 9.080 and 11.006 ms as round 29's. `:2331` points at the two round-30 figures only |
| 3. R711-9 RES-2, the ledger's reason strings | `084cf7a8` | `sw/litex/ctrl_memory.py:257` and `:265`: "ROM debt owed to the hybrid XIP work (#665 decision D3)" in place of "owed to S14". Reason strings only: no symbol, tile or behaviour changes, and `test_ctrl_memory.py` passes |

### Round 30

**The rulings:**
- On round 29: #665 issuecomment-6828629878, on [A683zn]'s round 29 REVIEW READY at `b2d39235` and on R711-8 and R712-8 (both NEGATIVE on two MINOR findings). It applies the owner's decision of 2026-11-12 (#665 issuecomment-6824896581), and round 30 syncs onto PR #892's round 4 head.
- Three STOPs in the round, each ruled:
  - the size fixture's 8x8/2if point at the merge (issuecomment-6831583372: ledger it at 58.5);
  - the record mover's host port at the merge (issuecomment-6835550732: the fix stays in this lane);
  - the firmware-stated costs at the merge (issuecomment-6842347916: option (b) amended).

| Item | At this head |
|---|---|
| 1. F1, the platform ledger | `cd87c3b2`. `ctrl_memory.LEDGERED["platform-8x8-two-interfaces"]` is 60.0 RAMB36, refused at 60.5. Its cause is the owner's decision: ROM debt of 4.0 RAMB36 owed to S14. **A new gate**, `tb/verilator/ctrl_split_boot/plat_ledger.py`, links the target platform's image at every point against its shape's own split export, with the override its point takes, and grades each check apart (`LINK`, `KEY`, `TILES`, `LEDGER`). So a stale `ctrl_plat` key cannot hide a plan past its tiles. Seven planted ledgers give exactly their findings, and end to end the gate fails (rc 1) with round 29's 59.0 and with a stale key. At this head the platform plans 59.5 at 8x8/2if, within its 60.0 |
| 2. F2, the SRP record cut's control | `ef913ca4`, R711-8's option (c). The control measures `notice-every-2` on the planted build and on this tree's unplanted image, and it is caught only where the planted heaviest SRP record apply is more than 5 % dearer (`poll_items.REFERENCE_CONTROLS`, `run.reference_verdict`). No stated cost is lowered. At this head's 8x8/2if image: 34,551 cycles planted against 30,989 unplanted, 11.5 % dearer, caught |
| 3. Suggestions | **S1:** the rows' arrival rules are held at each solved row's W and a microsecond either side of R4's 20 ms bound plus R4's record (`rows_grade.rule_windows`). The "W less two records" plant is refused by a rule finding: at this head at R5's own W at 1x1/1if, 38.25 ms, 50 SRP records ahead against the rule's 51. **R712-8 S2:** driver test T7 (a full completion queue refuses `fan_end` only once the last frame is committed), with its plant. **S5:** `load_grade.py --check` refuses a column bound to the other's table. **S7:** the merged ACMP expiry row names the pin move's kill test through `also`, at its C9 words |
| 4. The sync | `187eeed8`: one merge commit of PR #892's round 4 head `8bc1dfc0`, which carries `dev-soft-core` `0fb66211`. Eleven conflicts, each resolved from the composed tree. The store marks a record by its id with no walk, on KLJ3's counted open set; `nvm_any` leaves the hot list. Both ledger entries are keyed on KLJ3's `nvm_stage` of 13,594 B. `ctrl_plat` is unchanged at the four points |
| The first STOP: the fixture | `a4faefd4`. The size fixture's 8x8/2if entry is 58.5 RAMB36 as ruled, the half tile ROM debt owed to S14. Section 5 states it with the link, and that the owner's cap is now fully used: any further growth at that point is a STOP |
| The second STOP: the record mover | `420d44e4`, `9e6f0141`, `cdc2742e`. `dev-soft-core`'s `KL_mbx` answers a register read two cycles after its request (`3ba76ae7`), and the mover routed the port's ack by a one-cycle rule, so the composed tree did not boot. `cpu_wait_r` now marks a CPU request with `KL_mbx` from its issue to its answer, however long that takes; `cpu_ack_o = host_ack_i && cpu_wait_r`; and the mover's own requests and beats wait while it is set. The flop count is unchanged: synthesised alone for 7-series, 704 flops before and after, LUTs 484 to 487, MUXF7 16 to 13; no route was run. The bench (`tb/verilator/mbx` `run-dma`) follows the merged port and adds D11 (a CPU register read answered at two cycles with its own word, alone, behind a transfer and in a transfer's first cycle; a ring read at one). Three new plants, among them the one-cycle routing, are caught (24 of 24). The split boot runs at both points, at every sync |
| The harness at the merge | `da1869a3`, `3e67f9ca`, `525375d6`. KLJ3 moved the store's journal to 640 KiB at `0xe40000`. The budget harness's flash device now takes writes and journal reads only in the flash map's journal (`flash_test.cpp`'s set-span cases; a plant of the old window fails three). A save's container is the stage less the record header `ctrl_nvm` names, KLJ3's 10 bytes (the self-test pins it; a plant of 8 fails). The save bounds at 8x8 are restated on KLJ3's 13,584-byte container: 12,470 ms (382 steps), and 22,870 ms with a save in flight |
| The third STOP: the stated costs | `6c284a97`, `16eb95fc`. The firmware's stated costs, restated as ruled: `AECP_ROUND_COLD_US` 165 to 185 us at 8x8/2if; `CTRL_LOOP_BUILD_ONE_PASS_US` 405 to 430 and `CTRL_LOOP_BUILD_PASS_US` 900 to 1,010 at 1x1/1if, by the rule. 185 us is 2.7 % over the most measured, 180.16 us, not 5 %, because 186 already fails THE RETRY's search of the first notice's 22 ms. The exception is stated, with its expiry at the 8x8/2if flip (#890 closes only with a measured cold cost of at most 176.1 us, or on a new owner decision), in `aecp_mbx.h`, `FR_NFR.md` 3.4.1 and section 13. The AECP firm cap's test gives the round room for one notice past the cap: at 185 us a share holds 4.97 notices, and the plant `retry-firm-uncapped` had escaped it at `6c284a97`. Before building, every round of every leg was tallied by notices and refusals (trigger 1): no implied cold cost over 183.1 us, and no k=0 or k=1 round over the stated line |
| 5. Unchanged | The bounds, the every-source rule, the tiers (#894), THE DRAIN and `RETAINED_ROWS` |
| The re-grade | `5bea2597` ([below](#the-re-grade-on-the-merge-of-dev-soft-core-0fb66211-round-30)): the tables from every leg's full tally, and section 13's figures |

### The re-grade on the merge of dev-soft-core 0fb66211 (round 30)

How the legs ran:
- **8x8/2if, fresh builds at `6c284a97`.** That image states the round's cold start at 185 us. Each leg was on its own clean clone. Arm A's legs ran with helpers on the same build, and their runs were merged.
- **1x1/1if, at `da1869a3`.** Its image equals `6c284a97`'s, both the ELF and `objcopy -O binary`, and so does one sample group's log on a fresh build.
- **At this head.** Each leg was built fresh again with one sample group: every image and every sample log is byte-identical. Every recorded group was then regraded on that build. This head changes only a test file, the tables and docs after `6c284a97`.

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass, CPU cycles | Least row margin in a window opened at the age limit (round 31: the arm's least is at most this) |
|---|---:|---:|---|---|---|---|
| Arm A, 8x8/2if | 93 | 0 | 7 of 996 instances, 4 of 136 paths | 0 of 244,003 | 180,765 (`backlog`) | 8.162 ms (`backlog-adp@program-aged2-7`) |
| Arm A, 1x1/1if | 94 | 0 | 7 of 945, 4 of 87 | 0 of 147,766 | 158,371 (`backlog-owed`) | 9.992 ms (`backlog-adp@verify-aged2-5`) |
| The `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 13,579 | 183,244 (`notice-burst-2`), 16,756 under | |
| The `answering-every-port` arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 18,170 | 166,127 (`notice-every-6`), 33,873 under | |
| Arm B's `aecp` group, 8x8/2if and 1x1/1if | 1 and 1 | 0 | 0 of 39, 0 of 25 | 0 of 137, 0 of 109 | | |

**The misses and the saves.**
- The seven misses at each arm A point are round 29's: the three egress-held rows of tsn-c-stack#26 and the ACMP command behind the owed input. They run 62.68 to 65.05 ms at 8x8/2if and 61.95 to 63.59 ms at 1x1/1if.
- Each save is durable within its stated worst case, now on KLJ3's container:

| Point | Save | Durable after, ms | Worst case, ms |
|---|---|---:|---:|
| 8x8/2if | `save-second` | 22,829.6 | 22,870 |
| 8x8/2if | `save-starved` | 12,447.0 | 12,470 |
| 1x1/1if | `save-second` | 6,030.3 | 6,070 |
| 1x1/1if | `save-starved` | 4,048.8 | 4,070 |

**The merge moves measured costs:** `KL_mbx` answers a register read a cycle later, KLJ3 changes the store, and the hot list loses `nvm_any`. They are not separated.
- **Firmware-stated costs.** Three were under their measurement, and the ruling on the third STOP restates them:
  - THE TRANSMIT's build pass at 1x1/1if: 96,033 cycles, so 900 to 1,010 us by the rule.
  - Its build-one pass at 1x1/1if: 40,700, so 405 to 430.
  - THE RETRY's cold start at 8x8/2if: its dearest round implies 180.16 us, so 165 to 185, the margin exception.
- **Every round and every pass given whole on the fresh 8x8/2if build** is within its stated cost.
- **The tables** (round 29's rule, each cost the larger of this measurement and the committed table's, with `poll_grade.py`'s rebuild and withdrawal items restated by the same rule as its other items):
  - `poll_grade.py`'s polls base 155 to 205 us at 1x1/1if and 280 to 325 at 8x8/2if;
  - its walk 20 to 35 at 1x1/1if, and its rebuild 630 to 690 at 8x8/2if;
  - at 1x1/1if, in both columns: an SRP record and its retained retry 260 to 280, a centisecond 130 to 150, AECP's timer slot 60 to 65, a TICK 40 to 45, a grandmaster event 35 to 40;
  - at 1x1/1if with tsn-c-stack#32, ACMP's owed frame 120 to 125;
  - at 8x8/2if, AECP's timer slot 100 to 110 in both columns, and a TICK 40 to 85 at the pin and 75 to 85 with tsn-c-stack#32.
- **The four cost controls** are caught on the fresh 8x8/2if image:

| Control | Planted | Stated |
|---|---|---|
| `notice-fan-out-as-it-was` | an AECP item of 31,933 cycles | 27,000 |
| `polls-rebuild-in-the-base` | a polls base of 74,295 | 32,500, restated |
| `polls-rebuild-twice` | a rebuild item of 109,171 | 69,000, restated |
| `srp-compared-by-memcmp` | 34,551, against 30,989 unplanted (11.5 % dearer) | the image's own unplanted record |

**The load at this head** (`load_grade.py --check`, `flip_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.501 | 0.499 | the load gate, 0.70 in both columns, for merge | 1.00x | SRP's channel 0.168, ACMP's records 0.053, the TICK's consumers 0.048 (with tsn-c-stack#32) |
| 8x8/2if | **0.822** | 0.770 | the flip check, 0.70 at the pin | 1.17x at the pin (1.10x with tsn-c-stack#32) | SRP's channel 0.219, ACMP's records 0.088, the timer slots 0.070 (at the pin) |
| 32x32/2if | 2.151 | 1.660 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (with tsn-c-stack#32) |

**The rows by every source at this head** (`flip_grade.py --check`), each W in ms at this tree's pin, bold over its bound:

| Point | R4 (tier 1, 20 ms) | R5 (SRP, 90 ms) | R6 (SRP, 90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **74.83** | 38.25 | 33.65 | 20 | 22 |
| 8x8/2if | **377.98** | **148.68** | **139.23** | **22** | 62 |

**1x1/1if's R4** (66.12 ms at round 29):
- Its largest terms: SRP's records ahead of AECP's 19.32 ms, the other channels' records 10.97, each pass's own cost 8.74, AECP's owed frames 7.98, the retained retries 2.52.
- The independent re-derivation gives every solved row at both points to the hundredth.
- R712-8's "W less two records" plant is refused at R5's own W at 1x1/1if: 38.25 ms, 50 SRP records ahead against the rule's 51.

### What holds at this head (round 30's legs at `5bea2597`, whose tree `32551422` keeps; round 31 changes docs and reason strings only)

The acceptance of this lane's assignment (S2b, #665: the split firmware within T_svc, cycle work in firmware, owner decision D4 a), read at this head:

- **The rows by measurement**, from the CPU budget harness on the composed image: every group of arm A and of the `answering-every-port` arm, and arm B's `aecp` group, at 1x1/1if and 8x8/2if.
  - Every row is within its bound except the three egress-held rows of tsn-c-stack#26 and the ACMP command behind the owed input: 7 misses of 996 probe instances in 93 groups at 8x8/2if, and of 945 in 94 groups at 1x1/1if.
  - 0 refusals and no `STATED` line; every row's response is the one it states.
  - The `answering-every-port` arm: 0 misses of 736 and 280, and every queued notice within its bound. Arm B's `aecp` group: 0 of 39 and 25.
- **The pass share** (2.0 ms): no work pass over it at either point. The heaviest is 183,244 cycles at 8x8/2if (16,756 under) and 166,127 at 1x1/1if (33,873 under).
- **The saves**, on KLJ3's container: each durable within its stated worst case. At 8x8/2if, `save-second` 22,829.6 of 22,870 ms and `save-starved` 12,447.0 of 12,470.
- **The bounds that hold by construction:**
  - The queued notices at `aecp_mbx.h`'s stated bounds, which the loop search holds the loop to, at 185 us for the cold start at 8x8/2if: the first notice at 22 ms there and 20 at 1x1/1if; the last at 62 and 22 ms, within their 70 and 25 ms ceilings.
  - Within its stated cost, each a gate over every group at both points: every pass's polls base and each heavy item, each SRP record's own apply, every round (`round_grade.py`), and every pass given whole (`whole_grade.py`).
- **The long-window load:** 1x1/1if is within its ceiling in both columns, held for merge; 8x8/2if is over it, held by the flip check.
- **Decision D's tier bounds by every source, for the flip:** at 1x1/1if, R5, R6 and both queued notices fit.
- **What does not hold:**
  - 1x1/1if's R4 by every source (74.83 ms against tier 1's 20, #894);
  - at 8x8/2if, R4, R5 and R6 by every source and the first queued notice (22 ms against 20), with #890 and #894;
  - every row at 32x32/2if;
  - the long-window load at 8x8/2if;
  - the cold start's 5 % margin at 8x8/2if (2.7 %, the ruled exception until the flip).

### Round 29 (at `b2d39235`)

**The ruling** (#665 issuecomment-6813183455, on [A683zm]'s round 28 REVIEW READY at `66f71326`): round 29 is the sync onto the TSN stack's pin move, PR #892, and the tier rows go to #894. With it, R711-7's and R712-7's findings on round 28's delta (#810 issuecomment-6813519183 and R712-7), and the pin move's handover (#665 issuecomment-6813799445).

| Item | At this head |
|---|---|
| 1. The merge | `e96b9120`, one merge commit of the pin move's head `bfe7a9d6` into `66f71326` (`git merge --no-ff`), the tsn-c-stack submodule at `715589c`. The seven conflicts #890's lane recorded, each resolved from the composed tree: `ctrl_plat` at each point measured by `ctrl_plat_image.py` in the composed build, 17,472 / 19,008 / 18,112 / 20,288 B (`PLAT_*`; the platform override's key 20,288 B), neither side's; `acmp-expiry-reads-the-clock-twice` anchored on the composed code (715589c's `dirty_if` mark) and refused by `AcmpCore.TimerPortBudgets`; `coverage.ratchet` through `fw_coverage.py --write`; the docs with both sides' facts, the figures restated from the composed headers (`MAILBOX_SPLIT.md`: S2b's one 20 ms bound with the pin's 2,754-access pass; the four-module table and `CTRL_APP_PASS_MAX`, 4,840 and 4,980, from the service-bounds probe); and `__lshrdi3` out of the hot list, in `ctrl_split_hot.txt` (the merge) and in the link script's copy of it (`2cc852fa`), which `ctrl_hot.py` holds equal and which the merge alone left refused (`ORDER`, `LINKED`). No conflict needed a protocol or mailbox-contract change |
| 2. The 8x8/2if size fixture | `459a8d70`. 58.0 RAMB36, its cause stated in the ledger: a TX record's commit judges its own move (+112 to 120 B an image) and, with the pin move, arm A's image is 123,112 B of `rom`, past 57.5's 122,880; at 58.0 it holds 124,928, 1,816 B to spare (the `answering-every-port` arm 123,420 B, 1,508 to spare). `test_ctrl_memory.py` holds the entry, its own image refused at 58.5 |
| 3. The re-grade | Both points at the composed head ([below](#the-re-grade-on-the-composed-image)). The pin carries tsn-c-stack#32 here (its `src/` and `include/` equal the donor's `9043b926`), so each point's legs serve both of the load gate's columns, each kept the larger of the measurement and its own committed costs; the 8x8/2if column with tsn-c-stack#32 that round 28 could not build is measured |
| 4. No tier change | The bounds (20, 90, 125 ms), the every-source rule and THE DRAIN are unchanged; no tier structure. The rows stay red: [#894](https://github.com/kebag-logic/milan-fpga/issues/894) |
| 6, 8 F1. The rows by every source | `446d3310`. SRP's retained retry is charged at its own rule (`srp_mbx.c`: one a centisecond, `retry_spent` given back by the centisecond's consumer): one before the window's first centisecond and one after each it holds, `min(passes, floor(W/10) + 2)` (`rows_grade.retained_retries`). SRP's records ahead of R4's are counted over W less R4's own record (`rows_grade.srp_window`), not less AECP's whole burst. **The scope:** a retained record holds SRP's channel, each up to `SRP_RX_RETRY_MS` (1,000 ms), SRP's storage rule and not the CPU's service, so SRP's own rows, R5 and R6, are solved with no record of theirs refused for storage, and count neither the hold nor the retry; R4's record is AECP's, which no SRP record holds, and counts the retries (`RETAINED_ROWS`). With the hold counted, each of the 31 SRP records ahead of R5's or R6's, refused in turn, would hold it 1,000 ms: no W under 2,000 ms. **The datapath change records** (COUNTERS_CHANGED, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE) are named as excluded with the reason (`EXCLUDED`): no group stages them, so no cost of theirs is stated, and the method charges stated costs only; the notices they mark are counted, and their dispatch is #894's to stage. `rows_grade.rule_findings` holds each rule against the tree (the retry's lines in `srp_mbx.c`, the counts at six windows, every event type of the contract counted or excluded), and the flip self-test plants the earlier rules: the once-a-pass retry, refused and lengthening 1x1/1if's R4, and the shortened SRP window, refused and shortening it; with them a retry counted in an SRP row, the retry's rule planted out of `srp_mbx.c`, and a datapath event dropped from the list (131 of 131 controls; six harness mutants). R4 by every source at 1x1/1if: 66.12 ms; my independent re-derivation (round 29's packet's `receipts/rows/`, its constants from a compiled probe of the headers) gives the same to the hundredth at both points. The reviewers' figures reconcile exactly: R711-7's 58.18 ms is W less the row's own record with `floor(W/10) + 1` retries, R712-7's 58.94 ms the whole W with `floor(W/10) + 1`; neither counts the retry a window can hold before its first centisecond (on round 28's costs that rule gives 59.19 ms) |
| 7, 8 F2. The fan-out's resume and completion | `bdb0ae52`. A refusal is not a loss: `AECP_FAN_REFUSED` means the frame before was delivered, so the walk resumes at the refused frame's own recipient, or, for a completion queue with no room, past the last; `Core.ARefusedFrameIsSentToItsRecipientAndNoOneElseAgain` (a ring full at the second frame, a completion queue full after the last) asserts each recipient has the notice once, in order, at its own sequence_id, and refuses both of R711-7's planted defects. `fan_end` keeps a completion only for a walk that reached its last recipient (`whole`): a walk left owed at a recipient, lost or refused there, keeps none, and the resumed walk's end keeps the notice's one (Milan v1.2 5.4.5.2); `aecp_mbx.c`'s comment is true at the code. Driver test T6 (no completion after a mid-walk loss, exactly one after the resumed walk) and the core test's completion count, each refusing a plant that restores the old rule. The ratchet records `aecp_mbx.c`'s new branch (`6188ab6b`) |
| 8 S1, S2 | The receipts' `INDEX.md` is generated after every redaction and verified against the files present (round 29's packet's `scripts/verify_index_r711.py`, run on that packet: rows 823, bad 0, unlisted 0, as its REVIEW READY records). The load gate refuses `COLUMNS` with a name bound to the other column's table (`a column's name bound to the other's table`; 25 of 25 controls), and a harness mutant swaps them |
| 8 S3 | For #894: noted in the handoff, no change |
| 9. ACMP's poll at 1x1/1if | The pin move's redelivery makes the 1x1/1if ACMP item 11,359 CPU cycles at its heaviest (`backlog-owed`; the pin move measured 10,974), so `poll_grade.py` states it 120 us (65 before), and the load gate and the rows read it there, in both columns (`item.acmp`) |
| The first gate pass | At `7f50ee6a` it found three things this round's changes broke, fixed in `b2d39235`: the firmware-boundary gate refused `flip_grade.py`, which now named the SRP adapter's path (it reads it from `load_grade.RETRY_RULE`, a classified module); the C and C++ idiom gate found one new multi-declarator line in the AECP test's fan model; and the hooks self-test's "the plants apply" refused H-ACMP's two plants, whose anchor the pin move's redelivery had changed (re-anchored on the composed `on_frame`; the self-test shows each applies, 28 of 28 checks; the hooks harness's own run cannot build, at this head as at round 28's, so neither is shown caught by a run: a finding below). The full pass then ran again, once, at this head |
| 5. Gates | The full clean-clone pass at this head ([How to validate](#how-to-validate)) |

### The re-grade on the composed image (round 29, at `2cc852fa`)

The legs at `2cc852fa`, the firmware's final tree (the later commits change only the harness's graders and tables, docs, and nothing a build records), each a fresh build on its own clean clone; then each regraded at this head with its build reused (`--reuse-build`, which refuses unless every recorded input resolves unchanged):

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass, CPU cycles | Least row margin |
|---|---:|---:|---|---|---|---|
| Arm A, 8x8/2if | 93 | 0 | 7 of 996 instances, 4 of 136 paths | 0 of 274,456 | 186,522 (`srp`), 13,478 under | 8.973 ms (11.027 ms, an AECP record in a save's verify window opened at the age limit) |
| Arm A, 1x1/1if | 94 | 0 | 7 of 945, 4 of 87 | 0 of 169,480 | 163,134 (`backlog-owed`) | 11.006 ms |
| The `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,946 | 177,446 (`notice-every-2`) | 6.246 ms (13.754 ms, `notice-burst-2`) |
| The `answering-every-port` arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 20,920 | 168,216 (`notice-every-3`), 31,784 under | 9.080 ms |
| Arm B's `aecp` group, 8x8/2if and 1x1/1if | 1 and 1 | 0 | 0 of 39, 0 of 25 | 0 of 136, 0 of 110 | 118,326 and 61,240 | |

The seven misses at each arm A point are round 28's six egress-held instances and the ACMP command behind the owed input, which the pin move's redelivery now answers (62.57 ms at 8x8/2if and 62.14 at 1x1/1if; unanswered before): the three rows of tsn-c-stack#26. Each save is durable within its stated worst case (8x8/2if `save-second` 22,110 ms against 22,150, `save-starved` 12,089 against 12,110; 1x1/1if 6,030 against 6,070 and 4,048 against 4,070). The heaviest work pass at 8x8/2if is 13,478 cycles under the share, round 16's 6,490 met at this layout (deferred to #890 by the round 28 ruling either way). **The costs** (round 26's parsers; each cost the larger of this measurement and the committed table's; `poll_grade.py`'s held unless a measured instance is over one): at 1x1/1if ACMP's owed frame 65 to 120 us, an SRP record and its retained retry 250 to 260, a centisecond 125 to 130; at 8x8/2if AECP's timer slot 95 to 100; in the column with tsn-c-stack#32, the walk's costs measured here: ACMP's owed frame 35 to 120 at 1x1/1if and 40 to 165 at 8x8/2if, the polls' base 245 to 285 at 8x8/2if. The cost controls: `notice-fan-out-as-it-was`, `polls-rebuild-in-the-base` and `polls-rebuild-twice` refused (an AECP item of 31,747 cycles against 27,000; a polls base of 70,031 against 28,000; a rebuild item of 100,273 against 63,000); `srp-compared-by-memcmp` escapes (below). The legs ran first on the oversubscribed session pool, and when the scratch volume filled, the unfinished groups of two legs ran again on another volume and GA8's `save-second`, whose log the full disk cut, ran again from the start; the evidence packet's handoff states each step.

**The load at this head** (`load_grade.py --check`, `flip_grade.py --check`):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.486 | 0.483 | the load gate, 0.70 in both columns, for merge | 1.00x | SRP's channel 0.156, ACMP's records 0.053, the TICK's consumers 0.047 (with tsn-c-stack#32) |
| 8x8/2if | **0.816** | 0.767 | the flip check, 0.70 at the pin | 1.17x at the pin (1.10x with tsn-c-stack#32) | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (with tsn-c-stack#32) |

**The rows by every source at this head** (`flip_grade.py --check`), each W in ms at this tree's pin, bold over its bound:

| Point | R4 (tier 1, 20 ms) | R5 (SRP, 90 ms) | R6 (SRP, 90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **66.12** | 35.95 | 28.67 | 20 | 22 |
| 8x8/2if | **346.15** | **144.15** | **135.80** | **22** | 62 |

The largest terms of 1x1/1if's R4: SRP's records ahead of AECP's 16.64 ms, the other channels' records 10.58, AECP's owed frames 7.14; the retained retries are 2.08 ms (round 28's model charged 9.00 at its once-a-pass rule). The independent re-derivation gives every solved row at both points to the hundredth (the evidence packet's round 29's packet's `receipts/rows/`).

**Two findings, for the manager:**
- **The target platform's 8x8/2if image plans 59.5 RAMB36 against its ledgered 59.0** (ruling 6505997821), and has since at least round 27: its `rom` needs 128,264 B at this head (127,664 at `66f71326`, 127,544 at `e7e2b744`) against the 126,976 its 59.0 holds. Every link of it was refused first by the stale `ctrl_plat` key, and no gate links that image with its override, so its tiles were never read. The ledger stays 59.0; proposed issue text in the evidence packet (`PLATFORM-LEDGER-FINDING.md`).
- **The cost control `srp-compared-by-memcmp` escapes on this image**: the old comparisons planted give `notice-every-2` an SRP record of 35,908 cycles (37,494 on round 28's image), under the 36,500 its stated 365 us allows; unplanted the same group's is 32,866. The image made the record some 1,500 cycles cheaper, and the table rule keeps round 26's stated cost. Restating it from this image would refuse the plant but lowers a stated cost against the table rule: left for a ruling. The other three controls are refused.

### Round 28 (at `66f71326`)

**The ruling** (issuecomment-6805157674, on R711-6 and R712-6, both NEGATIVE at `e7e2b744`, MINOR only): the last round before S2b's merge, items 1 to 7 and nothing else.

| Item | At this head |
|---|---|
| 1. The merge gate at the pin (R711-6 F1 = R712-6 F1) | `5a19b0ca`. `load_grade.py --check` holds 1x1/1if in both columns, this tree's pin (the image that merges) and with tsn-c-stack#32 (the load the pin move owes), each at most 0.70 (`load_grade.COLUMNS`); a point over its ceiling is named with its column (`1x1/1if: the load L at the pin is over its ceiling 0.70`), and `--check` prints a `HELD` line for each. At this head 0.463 at the pin and 0.450 with tsn-c-stack#32, `RESULT: PASS`. A new control plants a pin-only rise (an ACMP record, a cost the donor's walk may state lower, raised to 2,000 us in the pin's column alone: the pin's load 0.807) and the gate must refuse it naming the pin's column: `--selftest` 24 of 24. R711-6's `probe_1x1_column.py` and R712-6's `probe_pin_1x1.py` now each print the refusal, `1x1/1if: the load ... at the pin is over its ceiling 0.70`. Section 13's margin names both columns |
| 2. Record commits (R712-6 F2) | `71e905fb`. A TX record holds whether the record mover carries it (`TX_MOVED` in `tx_ring.moving`), and its commit waits on the mover and judges its ERR only then: a record the word loop wrote never inherits an earlier ERR, which the mover holds until its next start. A failed move is reported for the record it carried: `mbx_tx_commit` is false, and `mbx_tx_begin`, which commits the record before its own, returns the new `MBX_STATUS_LOST` and starts nothing. The AECP fan port reports it for its frame (`enum aecp_fan`: TAKEN, REFUSED, LOST), from the next `fan` or from `fan_end`, which no longer discards its commit's result and keeps no completion for a lost last frame; `fan_out` resumes the notice at the recipient whose frame was lost and gives back the sequence_id it did not spend (IEEE 1722.1-2021 7.5.2; Milan v1.2 5.4.5.1). `mbx.h` states it. Tests: the driver's T4 (an ERR, then a frame off a word, sent whole and in halves, which must commit; then a frame on a word moved again) and T5 (the fan port over the DMA driver: the fan after a failed move LOST, nothing started; a failed last frame LOST from `fan_end`, no completion; each sent again), T2 extended; the AECP core's `ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain` (a middle frame lost, reported by the next fan, and a last frame lost, reported by `fan_end`). Nine plants, each caught by its test's words (HANDOFF section 3). The image grows 112 to 120 B (8x8/2if arm A 122,328 to 122,440 B, the `answering-every-port` arm 122,636 to 122,748 B, each within its ledger). With tsn-c-stack#32, arm A's 8x8/2if image is 122,896 B, 58 RAMB36 against the 57.5 ledgered there: that column's 8x8/2if leg does not build at this head and keeps its committed costs, and the pin move that carries tsn-c-stack#32 meets the same ledger |
| 3. Round 16's margin at 8x8/2if (R711-6 F2) | Deferred to the 8x8/2if flip under #890, whose owner decision of 2026-11-11 sets that point's flip ceiling to 0.75; section 13 cites it. 1x1/1if keeps the margin: its heaviest work pass at this image is 160,618 cycles (`backlog`), 39,382 under the share. At 8x8/2if this image's heaviest is 192,237 cycles (`backlog`), 7,763 under the share, so the margin holds at this layout (round 26's image gave 193,609, 99 short): it moves with the image, which is why the ruling defers it. `flip_grade.FLIP` keeps 0.70 at this head: #890's decision applies the 0.75 in a change of its own once the pin moves |
| 4. Decision D's tier bounds (R711-6 F3) | `5a19b0ca`. `flip_grade.py --check` holds each point's flip to the rows by every source (`rows_grade.py`): R4 at tier 1's 20 ms, R5 and R6 at SRP's 90 ms, the first queued notice at 20 ms and the last at 125 ms, at 1x1/1if and 8x8/2if (`--point` for one). R4, R5 and R6 are round 22's method on this tree's pin costs (the smallest W in which the record's own work and every source's arrival bound fit, THE DRAIN as `ctrl_loop.h` states it, the grandmaster events at their IEEE 802.1AS-2011 intervals); the queued notices are `aecp_mbx.h`'s derived bounds, which the loop search holds. Self-test controls for each row at each point (over and within its bound), each source left out, the pin's column read, a planted queued-notice derivation and the bounds themselves: 129 of 129, and five harness mutants caught. **The 1x1/1if result, a finding:** R4 is 73.02 ms by every source against tier 1's 20 ms (+53.02 ms; its largest terms SRP's records ahead of AECP's, 16.50 ms, the other channels' records, 10.96 ms, and the retained retries, 9.00 ms): THE DRAIN takes SRP's records first, and round 23's tier design, a tier-1 record served before any tier-2 work, is not built. R5 is 37.19 ms and R6 32.69 ms within SRP's 90; the first queued notice is held at 20 ms, its bound, and the last at 22 ms within 125. So `flip_grade.py --check --point 1x1/1if` exits 1 at this head, and the 1x1/1if flip cannot pass it until R4 fits; the finding is #894's (the tier rows, model first). **Superseded:** these rows charged SRP's retained retry once a pass and cut SRP's window by AECP's whole burst; round 29 corrects both ([Round 29](#round-29)), and 73.02 ms is not this head's figure. The flip at 1x1/1if must pass `flip_grade.py --check --point 1x1/1if`; 8x8/2if stays with #890 (R4 489.97 ms, R5 162.96 and R6 149.57 ms by every source, the first queued notice stated at 22 ms against tier 1's 20 and the last at 62 within 125) |
| 5. Portable C (R711-6 F4) | `24ea9c04`. `_Alignas(64)` for the AECP response buffer (`alignas(64)` where a C++ test reads `aecp.h`, which g++ requires); `noinline` and `may_alias` behind `CTRL_CC_GNU` in `sw/firmware/ctrl/plat/ctrl_cc.h`, outside the protocol code, with a portable C11 fallback (nothing for `CTRL_CC_NOINLINE`, `memcpy` for the pool's link). `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only that header, and a new firmware arm, `portable`, holds it: a scan for `__attribute__` and `__builtin_` outside `test/` but `ctrl_cc.h`, and the port arm's tests built with `CTRL_CC_GNU=0`. A pool test that can fail for an unwritten link (`Pool.P10`) and three plants. The change alone is image-neutral: `e7e2b744` with it builds 8x8/2if arm A's three images byte-identical to round 27's (objcopy sha256 `5b2317d8...`, `be42e7c9...`, `57b60044...`) and its `control` group's log byte for byte, so it restates no cost |
| 6. Docs and residue | R712-6 F3's sentence (152 B at the pin and 160 B with tsn-c-stack#32); the new harness comments' issue-comment IDs and round labels replaced by the issue and the behaviour; #890 and #891 named where this body said "the flip-gate issue" and "its own issue", and at the harness's unknown command (`answers.py`) |
| 7. Gates | The full clean-clone pass at this head, once ([How to validate](#how-to-validate)): every gate rc 0 but the flip check, which exits 1 by design; `elaborate-gates-1` ran twice, its first run's LiteX simulation timing out under the session pool's load |

**The re-grade on round 28's image** (item 7; the legs at `71e905fb`, every group of arm A and of the `answering-every-port` arm at both points, arm B's `aecp` group and the column with tsn-c-stack#32 at 1x1/1if; then regraded at the head):

| Leg | Groups | Refusals | Budget misses | Work passes over the share | Heaviest work pass, CPU cycles | Least row margin |
|---|---:|---:|---|---|---|---|
| Arm A, 8x8/2if | 93 | 0 | 6 of 996 instances, 3 of 136 paths | 0 of 272,475 | 192,237 (`backlog`), 7,763 under | 6.515 ms (13.485 ms, an AECP record in a save's verify window opened at the age limit) |
| Arm A, 1x1/1if | 94 | 0 | 6 of 945, 3 of 87 | 0 of 184,496 | 160,618 (`backlog`) | 10.434 ms |
| The `answering-every-port` arm, 8x8/2if | 16 | 0 | 0 of 736 | 0 of 14,350 | 186,213 (`notice-every-2`) | 4.018 ms (15.982 ms, `notice-burst-6`) |
| The `answering-every-port` arm, 1x1/1if | 16 | 0 | 0 of 280 | 0 of 22,114 | 160,222 (`notice-burst-6`) | 8.349 ms |
| Arm B's `aecp` group, 8x8/2if and 1x1/1if | 1 and 1 | 0 | 0 of 39, 0 of 25 | 0 of 131, 0 of 110 | 119,134 and 63,670 | |
| Arm A with tsn-c-stack#32, 1x1/1if | 19 | 0 | 6 of 141, 3 of 81 | 0 of 10,249 | 156,237 (`backlog-adp`) | |

The six misses at each arm A point and with tsn-c-stack#32 are the three egress-held paths of tsn-c-stack#26, as in round 27. Each save is durable within its stated worst case (8x8/2if `save-second` 22,110 ms against 22,150; 1x1/1if 6,030 against 6,070). **The costs** (round 26's parsers, each cost the larger of this measurement and the committed table's): no cost at the pin moves at either point, nor `poll_grade.py`'s; with tsn-c-stack#32 at 1x1/1if ACMP's timer slot rises 165 to 170 us and THE TRANSMIT's build 910 to 920 (`66f71326`), which leave that column at 0.450. The four cost controls are refused on this image (an AECP item of 29,968 cycles against 27,000; an SRP record's apply of 37,494 against 36,500; a polls base of 74,399 against 28,000; a rebuild item of 113,443 against 63,000).

**The load at round 28's head** (as its gates then stood):

| Point | Load at the pin | Load with tsn-c-stack#32 | Held by | Compute for 0.70 | Its three largest terms |
|---|---:|---:|---|---:|---|
| 1x1/1if | 0.463 | 0.450 | the load gate, 0.70 in both columns, for merge | 1.00x | SRP's channel 0.150, ACMP's records 0.053, the TICK's consumers 0.047 (with tsn-c-stack#32) |
| 8x8/2if | **0.815** | 0.719 | the flip check, 0.70 at the pin | 1.16x at the pin | SRP's channel 0.219, ACMP's records 0.088, ACMP's owed frame 0.070 (at the pin) |
| 32x32/2if | 2.150 | 1.659 | reported: the more-compute image, #872 | 2.37x | SRP's channel 0.519, owed MRPDUs 0.299, THE TRANSMIT's builds 0.150 (with tsn-c-stack#32) |

**The rows by every source at round 28's head** (superseded by round 29's rules):

| Point | R4 (tier 1, 20 ms) | R5 (SRP, 90 ms) | R6 (SRP, 90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | **73.02** | 37.19 | 32.69 | 20 | 22 |
| 8x8/2if | **489.97** | **162.96** | **149.57** | **22** | 62 |

Each W in ms by every source at this tree's pin; bold misses its bound. The largest terms of 1x1/1if's R4: SRP's records ahead of AECP's 16.50 ms, the other channels' records 10.96, the retained retries 9.00.

### What held at round 29's head (`b2d39235`), as it stood

The acceptance of this lane's assignment (S2b, #665: the split firmware within T_svc, cycle work in firmware, owner decision D4 a), read at this head:

- **The rows by measurement** (the CPU budget harness on the composed image, every group of arm A and of the `answering-every-port` arm, and arm B's `aecp` group, at 1x1/1if and 8x8/2if): every row is within its bound except the three egress-held rows of tsn-c-stack#26 (`backlog.owed`, `backlog.owed_behind0` to `3`, `backlog-owed.service.aecp.last`, and the ACMP command behind the owed input, `backlog-owed.service.acmp.last`, which the pin move's redelivery now answers at 62 ms): 7 misses of 996 probe instances in 93 groups at 8x8/2if, and of 945 in 94 groups at 1x1/1if. 0 refusals, no `STATED` line, every row's response the one it states. The `answering-every-port` arm: 16 groups at each point, 0 misses of 736 and 280, every queued notice within its bound. Arm B's `aecp` group: 0 misses of 39 and 25.
- **The pass share** (2.0 ms): 0 of 274,456 work passes over it at 8x8/2if and 0 of 169,480 at 1x1/1if; 0 of 14,946 and 0 of 20,920 in the `answering-every-port` arm. The heaviest at 8x8/2if is 186,522 cycles (`srp`), 13,478 under, round 16's margin met at this layout and deferred to #890 by the round 28 ruling; at 1x1/1if 168,216 (`notice-every-3`), 31,784 under.
- **The bounds that hold by construction:** the queued notices at `aecp_mbx.h`'s stated bounds, which the loop search holds the loop to (the first 22 ms at 8x8/2if and 20 at 1x1/1if; the last 62 and 22 ms within their 70 and 25 ms ceilings); every pass's polls base and each heavy item within its stated cost (`poll_grade.py`), each SRP record's own apply within its retry's, every round within its own (`round_grade.py`), and every pass given whole to a build or an aged step within its own (`whole_grade.py`), each a gate over every group at both points.
- **The long-window load:** 1x1/1if within its ceiling in both columns, held for merge; 8x8/2if over it, held by the flip check.
- **Decision D's tier bounds by every source, for the flip:** at 1x1/1if R5, R6 and both queued notices fit.
- **What does not hold:** 1x1/1if's R4 by every source (66.12 ms against tier 1's 20, #894); at 8x8/2if R4, R5 and R6 by every source and the first queued notice (22 ms against 20), with #890 and #894; every row at 32x32/2if; the long-window load at 8x8/2if; the platform image's 8x8/2if ledger (59.5 against 59.0); and the cost control of the SRP record cut on this image.

### The round histories

Rounds 12 to 27's Description sections, and the decisions their Known limitations listed, are in the evidence packet `evidence/ROUND-HISTORIES.md` (round 27's moved there in this round, as round 28's body gave it).

## Authoritative references

- Round 31: the manager's ruling on R711-9 (#810 issuecomment-6850590935) and R712-9 (#810 issuecomment-6850656712), and `dev-soft-core` `6eacd76d` (in `e5f88a8e`), whose two statements item 1 restores.
- The rulings in round 30:
  - on round 29 (#665 issuecomment-6828629878);
  - on the first STOP (issuecomment-6831583372);
  - on the second (issuecomment-6835550732);
  - on the third (issuecomment-6842347916).
- The owner decision of 2026-11-12 (#665 issuecomment-6824896581).
- The owner decision of 2026-11-13 06:47 (#665 issuecomment-6845315282): 8x8 is a must and the two-interface parts are an option; #810 is not re-scoped.
- R711-8 (#810 issuecomment-6828561870) and R712-8 (#810 issuecomment-6828619213).
- PR #892's round 4 REVIEW READY (#665 issuecomment-6829628610).
- `dev-soft-core` `3ba76ae7` (PR #889, #870: `KL_mbx`'s host port answers a register read two cycles after its request) and #823 (KLJ3).
- The ruling on round 28 (#665 issuecomment-6813183455), R711-7 (#810 issuecomment-6813519183) and R712-7; #894 (the tier rows); #890 and its owner decision of 2026-11-11; #891.
- Decision D (#665 issuecomment-6759183115 and issuecomment-6759193032) and the round 23 ruling (issuecomment-6732443213: tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms; the every-source count is the bound). The 2026-11-08 decision on the first queued notice at 8x8/2if, 22 ms (`FR_NFR.md` 3.4.1).
- IEEE 1722.1-2021 7.5.2 (a notice to each registered controller, its own sequence_id) and 9.2.1.1; Milan v1.2 5.4.5.1 and 5.4.5.2 (the counters' notice and its holdoff).
- The record mover's register contract (`sw/firmware/ctrl/plat/mbx_dma.h`), `hdl/milan/mailbox/KL_mbx_dma.sv` and `KL_mbx.sv`'s host port.
- `sw/firmware/ctrl/srp/srp_mbx.c` (the retained receive and its retry: `retry_spent`, `SRP_RX_RETRY_MS`); `sw/mailbox/mailbox.yaml` (each channel's `rate`, `tick_ms`, `event_types`, `counters_changed`).
- The protocol timers the arrival bounds cite:
  - Milan v1.2 5.5.2.3 and Table 5.26, 5.6.3.5.3, 5.6.3.5.9 and Table 5.50, 5.6.4.5, 5.4.5.2 and Table 5.22, 5.4.5.3;
  - IEEE 1722.1-2021 6.2.2.5;
  - IEEE 1722-2016 B.3.4.1, B.3.4.2 and Table B.8;
  - IEEE 802.1Q-2018 10.7.4.1 and Table 10-7, and Milan v1.2 Table 4.3;
  - IEEE 802.1AS-2011 (+Cor1/Cor2) 10.7.2.2, 10.7.3.2 and 11.5.2.2, the edition Milan v1.2 profiles.
- The docs:
  - `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5 (the ledger) and 13 (the long-window load, the rows by every source, the queued notices at stated costs);
  - `docs/design/MAILBOX_SPLIT.md` (the host port's rule, the ACMP pass bound and the service tables);
  - `docs/reference/FR_NFR.md` 3.4.1;
  - `tb/verilator/ctrl_service_budget/README.md`, `tb/verilator/mbx/README.md` and `tb/verilator/ctrl_split_boot/README.md`;
  - `sw/firmware/ctrl/README.md` and `sw/firmware/ctrl/aecp/README.md`;
  - `sw/firmware/ctrl/aecp/aecp.h` and `aecp_mbx.h`, and `sw/firmware/ctrl/loop/ctrl_loop.h`.

## How to get into the same state

```sh
git fetch origin
git checkout 084cf7a8455e9fa8e24a0e5bcf57c9557816c819
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check
python3 -B sw/firmware/ctrl/test/ctrl_retry_search.py
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
make -C tb/verilator/mbx run-dma dma-mutants
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/plat-ledger --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-notice --variant answering-every-port --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings --record-share-findings
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_em_dash.py --base 325514224bcc356a6b43843f1003c2323f09de25
python3 -B scripts/check_py_idiom.py
python3 -B sw/litex/test_ctrl_memory.py
git diff --check 325514224bcc356a6b43843f1003c2323f09de25 HEAD
git diff e5f88a8e HEAD -- docs/design/SPLIT_CONTROL_MEMORY.md
```

Expected result of round 31's gates at this head, each rc 0, never piped:
- `docs_check.py`: `0 finding(s)`; `check_doc_style.py`: `documentation style: OK`; `check_em_dash.py`: `0 finding(s) over 5 added line(s) in 1 changed Markdown page(s)`; `check_py_idiom.py`: every count at or under its budget; `test_ctrl_memory.py`: `RESULT: PASS`, 0 failures; `git diff --check`: no output.
- `grep -n 'owed to S14' sw/litex/ctrl_memory.py` prints nothing.

Expected result at round 30's head, whose tree this head changes only in docs and two reason strings:
- **`load_grade.py --check`** exits 0 (`RESULT: PASS`) and prints:
  - `HELD 1x1/1if at the pin: the load 0.501, its ceiling 0.70`
  - `HELD 1x1/1if with tsn-c-stack#32: the load 0.499, its ceiling 0.70`
- **Self-tests:** `load_grade.py --selftest` prints `load gate: 25 of 25 planted controls refused`, and `flip_grade.py --selftest` prints `flip check: 132 of 132 planted controls refused`.
- **`flip_grade.py --check --point 1x1/1if`** exits 1 with `OVER 1x1/1if R4: by every source 74.83 ms, over its bound 20 ms; the largest term srp 19.32 ms`; the finding is #894's. `flip_grade.py --check` exits 1 by design, with 8x8/2if's load and rows over: it is no merge gate.
- **`ctrl_retry_search.py`:** `THE RETRY search: every queue within its stated bound`. With `AECP_ROUND_COLD_US` at 186 us at two interfaces it fails: `the first notice at 2 interface(s): 28 ms over AECP_QUEUED_FIRST_MS`.
- **The harness self-test:** `self-test: 0 failures`.
- **The mover's bench:** `checks: 520041 failures: 0`, and `dma-mutants` catches 24 of 24.
- **The split boot:** PASS at 1x1/1if and 8x8 (one and two interfaces).
- **`plat_ledger.py`:** four `POINT ... PASS` lines, and `plat_ledger controls: 7 of 7 as required`.
- **The AECP mutation shard 2/4:** `test_ctrl_firmware: PASS`, with `[ok] retry-firm-uncapped`.
- **The harness runs:** as the re-grade's table above. 0 refusals, no pass over the share, and no `STATED` line. Every row is within its bound but the three egress-held rows of tsn-c-stack#26 and the ACMP command behind the owed input. Every save is durable within its worst case.

The evidence at round 30's head `5bea2597`, whose tree the sync merge `32551422` keeps, each item on a clean clone of it, never piped (round 31 re-ran only its own gates above):

- **Every `run:` step of the four workflows a pull request to `dev-soft-core` triggers**, each job on its own fresh clone: 139 steps ran, every one rc 0, 0 steps without an rc or a reason. 226 are not run, each with its reason: hosted orchestration, artifact upload and collection, apt and sudo installs whose pinned tools this host carries, `physical-gptp` (which runs only on a schedule), and `rtl.yml`'s `verilator-shards` suites, which run here as the full sweep below.
  - `rtl-fast.yml`:
    - `changes`, `verilator-lint`, `yosys-tool`, `yosys-elaboration`, `publication-census`, `split-cdc` (13 checks, 0 failures), `rtl-fast`;
    - `bdd-conformance` (508 scenarios and 2,330 steps passed);
    - `firmware-unit` (`test_ctrl_firmware: PASS`; the saved-state store's coverage run; `fw_coverage.py --check` PASS over 39 files);
    - `firmware-control-mutants` (698 of 698 caught), `firmware-aecp-mutants` (227 `[ok]`, `retry-firm-uncapped` among them), `firmware-srp-mutants` (340 `[ok]`);
    - `firmware-boundary` and `firmware-verilator` (`ctrl_boundary: PASS`).
  - `rtl.yml`: `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4.
  - `elaborate.yml`: `elaborate-gates-0`, `elaborate`, `elaborate-gates-1`.
  - `docs.yml`: `wire-accountability`, `docs-check-no-git` (the job removes `.git`, so the runner's own tree check after it cannot run), `docs-gates-0` to `-2`, `docs-check`.
- **The full sweep**, `scripts/run_all_suites.sh` as four shard units on clean clones and booked ranges, the shard holding `capture_coherence` on four CPUs:
  - 65 suites, 65 passed, 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures;
  - every shard's preflight passes, so no shard ran again;
  - the mailbox suite's record mover mutants 24 of 24, and its mailbox mutants 12 of 12;
  - in one shard the `tsn_fuzz` campaign rewrites the date stamp of two `TEST_RESULTS.md` files in place, as before.
- **The lane's own gates** on clean clones, each rc 0 but the flip check (exit 1 by design):
  - `git diff --check` against the merge base and against round 29's head;
  - the Python and C/C++ idiom gates, `check_baremetal_only.py --check`, `docs_check.py` (0 findings);
  - `ctrl_hot.py --self-test` and `--check`, and the harness self-test (0 failures);
  - `load_grade.py --selftest` and `--check`; `flip_grade.py --selftest`, and `--check` at both points;
  - the rows' independent re-derivation; R711-8's and R712-8's rule, column and fan probes;
  - the hooks and target self-tests, `gen_mailbox.py --check --crosscheck` and `--selftest`, `lint_rtl.py --check`, `test_soc_options.py`, `test_ctrl_memory.py`, `test_builder.py --require-rv32`;
  - `plat_ledger.py --self-test` and the fixtures at four points;
  - `test_ctrl_nvm.py --require-rv32 --self-test` (526 tests; 144 planted defects reddened);
  - the split boot at 1x1/1if, 8x8/1if and 8x8/2if (ready at 26.370, 66.017 and 68.371 ms), its native controls and its plants;
  - `cd tests && behave`, and `make -C tb/verilator/milan_dp twin`.

  Each clone's tree is clean after them.
- **The harness at both points.** This head changes a test file in a tree the harness's builds digest, so each leg was built fresh at this head with one sample group. Every image is byte-identical to the leg's build (objcopy and ELF), and so is every sample log. Every recorded group of arm A, of the `answering-every-port` arm and of arm B's `aecp` group, at 1x1/1if and 8x8/2if, was then regraded against the fresh build:
  - 0 refusals;
  - 7 misses of 996 probe instances (4 of 136 paths) at 8x8/2if and of 945 (4 of 87) at 1x1/1if;
  - no `STATED` line and no work pass over the share;
  - the notice arm 0 of 736 and 0 of 280; arm B 0 of 39 and 0 of 25.

  The four cost controls ran again at this head and are caught.


## Known limitations / out of scope

- **Round 31's section 13 margins:** round 30's re-grades print only the least margin of the windows opened at the age limit, so arm A's least over all its rows and the `answering-every-port` arm's least at either point are not re-derived at this head; section 13 says so. Re-deriving them needs each leg's table of rows, which round 31 does not re-run legs for. The heaviest work passes in section 13 and the round 30 table (183,244 cycles at 8x8/2if, `notice-burst-2`) are round 30's figures, unchanged by round 31; the 8x8/2if one is not in round 30's published verdict lines, which give the longest pass carrying the store's step.
- **The margin exception** (the ruling on the third STOP): THE RETRY's cold start at 8x8/2if is stated at 185 us, 2.7 % over the most measured 180.16 us, because 186 us fails the retry search's 22 ms. It expires at the 8x8/2if flip: #890 closes only with a measured cold cost of at most 176.1 us, or on a new owner decision.
  - GN8's rounds fit roughly 191.6 + 28.3k us, and that fit puts a round with k = 0 or 1 over the stated line.
  - No receipt shows one: in the tally by n and k (trigger 1), the dearest k = 1 round at 8x8/2if (arm A) implies 81.41 us, and the dearest k = 0 round (the `answering-every-port` arm) 45.35 us.
- **The owner decision of 2026-11-13 06:47** (#665 issuecomment-6845315282), posted after this round's last ruling: "8x8 is a must, 2if parts an option, but keep it going." The flip needs at least 8x8/1if as well as 1x1/1if, and a blocker at 2if only may be deferred to #890 as tracked debt. #810 continues in its current scope, so this round changes nothing for it. The flip check must also hold the rows at 8x8/1if, which is #894's next step after its round 4; this head's flip check holds 1x1/1if and 8x8/2if as before.
- **The cause of the merge's cost moves is not separated:** `KL_mbx`'s two-cycle register read, KLJ3, and the hot list without `nvm_any`.
- **The record mover's fix:** synthesised alone for 7-series, its area is the same flops (704); no route was run for its timing.
- **The size fixture's 8x8/2if image** is ledgered at the owner's cap, 58.5 RAMB36. The cap is fully used, so any further growth at that point is a STOP.
- **Round 30's other notes:**
  - The pin move's kill test fails under the ACMP expiry plant at its C9 line in the composed tree, not its C5 line, so the `also` row names C9's words.
  - R712-8's "retries not capped by passes" plant stays equivalent, as both reviewers found.
  - The harness's own GA8 leg ran with helpers on the same build and its runs merged, the merge refusing a group whose scripts differ between runs.
- **Round 29's decisions, where this round leaves them:**
  1. The tier rows stay red (#894): 1x1/1if's R4 by every source is 74.83 ms at this head.
  2. The retained record's hold is out of SRP's rows' scope, unchanged.
  3. The platform image's 8x8/2if ledger is answered by item 1 (60.0, within which it plans 59.5).
  4. The SRP record cut's control is answered by item 2.
  5. The hooks harness's own run cannot build (pre-existing); its self-test, the lane's gate, passes.
  6. 8x8/2if waits on #890: its load (0.822 at the pin), its rows, round 16's margin there and the 0.75 flip ceiling #890's decision sets in a change of its own. This head keeps `flip_grade.FLIP` at 0.70.
- **Suggestions carried, not taken:** R711-7 S2 (a lost notice frame re-sent every pass under a persistent mover ERR, with no bound) for an issue of its own; R711-7 S3 to S5 and R712-7 S3 for #894's itemisation; R711-7 S6 not taken.
- **The datapath change records** (COUNTERS_CHANGED, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE) are excluded from the rows, with the reason: no group stages them, so no cost is stated. #894 stages them.
- **No group stages** a retained record's retry, an owed MRPDU or a registration's probe, nor a failed record move (the driver and AECP tests do). Each is stated at the cost of the measured work that holds it.
- **The three egress-held rows** stay with tsn-c-stack#26.
- **No fabric option outlives the switch-over:** nothing here adds one.
- **The candidate merge** onto live `dev-soft-core` is the manager's.
- The earlier rounds' decisions for the owner and the manager are in `evidence/ROUND-HISTORIES.md`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#665 stays open: this lane is one part of it)
- [x] New or changed behavior has self-checking tests:
  - the platform ledger gate and its seven planted ledgers;
  - the reference control;
  - the rule windows' control;
  - the load gate's binding controls;
  - driver test T7;
  - the mover's D11 and its three plants;
  - the flash device's set-span cases;
  - the container's record header pin;
  - the AECP firm cap's test, with room past the cap.
- [x] Required local verification bar passes (the full pass at this head; the flip check exits 1 by design)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (the tier rows await #894; the 8x8/2if flip awaits #890; the cold start's margin exception is documented and expires at the flip)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

