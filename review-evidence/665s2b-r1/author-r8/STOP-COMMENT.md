[A683j] STOP

Head: `59038a1d7c8ec65417fc74d7fb64804d7075e3fe` on `665-s2b-cycles` (local, not pushed): ten commits on round 7's `17d32e81`, whose commits stay. RTL changed: the split CPU's fetch L1, and a new block on the split hart's mailbox path. The mailbox contract and both stack pins are unchanged.

**The STOP condition holds.** At 100 MHz the 8x8 last AECP and SRP records still miss T_svc: 14.47 to 16.39 ms, with both repository drafts staged or not. So the scope question (a 1x1-only split for Mark II) goes to the owner. At 1x1 every row the CPU decides fits with the drafts. Without them, only arm A's last SRP record misses, at 10.41 ms.

**Owner decision item 1, the fetch L1** (`6ba67356`):
- 16 KiB, two-way, 64-byte lines, one refill at a time: `CTRL_FETCH_L1 = (128, 2)`. The generator's pseudo-LRU is exact LRU at two ways.
- The data cache and RV32M stay; the all-fabric CPU keeps exactly `--xlen=32`. The option test kills five other geometries.
- NFR-SCOUT-01 carries the owner's text in `FR_NFR.md`, `ARCHITECTURE_HW_SW_SPLIT.md`, `MARK_II_AREA_PLAN.md` and `SPLIT_CONTROL_MEMORY.md` (`7ac3e52e`); `docs/history` is untouched.
- **Out of context at 100 MHz** (the split CPU and its firmware memory, CPU and bus at 10 ns, round 5's recipe):

| Split CPU | CPU WNS / WHS, ns | Bus WNS / WHS, ns | LUT | FF | The CPU's block RAM |
|---|---:|---:|---:|---:|---:|
| 4 KiB direct-mapped fetch L1 (round 5) | +0.952 / +0.041 | +2.440 / +0.070 | 3,902 | 6,828 | 6 RAMB36 + 11 RAMB18 (11.5 tiles) |
| 16 KiB two-way fetch L1 | +0.659 / +0.031 | +2.660 / +0.072 | 3,948 | 6,879 | 9 RAMB36 + 11 RAMB18 (14.5 tiles) |

  No routing errors. The worst path is the generator's memory bridge into its read pipe (8.93 ns).
- **The block RAM against the 224 KB budget:** +3 RAMB36 of cache data. It is CPU memory outside the firmware allocation, so no image's plan changes (35.0 / 38.5 / 48.5 / 55.0 tiles of 56 / 56 / 56 / 57.5). The area ledger goes to 124 tiles, 2.5 over its 121.5 ceiling: 125 with every bank in block RAM, 126 at the full 56-tile allocation.

**Item 2, the firmware and bus-path round:**
- **(a) `ctrl_mem`** (`c7690363`): it was already word-wise. Aligned copies and fills now move eight words a turn and the rest by its bits (four words, two, one, a halfword, a byte). Six planted defects are caught and coverage stays 100 %. At 8x8, `memset` runs 15 % fewer instructions and `forward` 6 % fewer; their time is mostly data-cache refills.
- **(b) The record mover**, `KL_mbx_dma` (`cf5ae260`, `caddc237`, `39aba024`), sits on the split hart's mailbox host port, between `KL_mbx_wb` and `KL_mbx`. It moves a record's payload between its ring and memory through the CPU's coherent DMA port, in AXI4 bursts inside one 64-byte line.
  - The mailbox contract is unchanged: the same ring words in the same order, the header words, counters and doorbells stay the driver's, and its four registers are a CSR bank of their own. `gen_mailbox.py --check --crosscheck --selftest` and the census pass.
  - The split image's `mbx_rx_take` and `mbx_tx_send` use it (a transmit frame off a word keeps the word loop); every other build keeps the loops.
  - Out of context at 100 MHz it takes 395 LUTs, 700 FFs and no block RAM, with +4.086 ns of slack.
  - Its own bench has 360,473 checks against a driver's word loop written from the contract, and 17 planted defects, all caught. The bench caught two defects of the first draft.
  - At 8x8 the driver's instructions halved: `mbx_tx_send` went from about 1.0 to 0.4 ms a window, `mbx_rx_take` from 0.9 to 0.7.
- **(c) lwSRP's receive path:** a draft for kebag-logic/lwSRP, not pushed, with two exact changes:
  - `mrp_reclaim` skips its walk while no attribute can be reclaimed: 0.7 ms to 0.18 ms of an 8x8 SRP window;
  - the validation parse pass no longer clears each decoded value.
  - Three tests and six planted defects; lwSRP's unit suite (26,690 assertions) and scenarios pass.
  - The parent's side is the pin: the gitlink with `ctrl_arms.LWSRP_REV`, which the image builder also reads. The SRP adapter needs no source change, because its reclaim flag still saves the call.

**Item 3:** round 7's TSN stack wire-halves draft, staged as round 7 did.

**Every composed row at 100 MHz** (worst over the four backlog groups, ms, arm A / arm B, bold misses T_svc; before = round 7's head):

| Row | 1x1 before | 1x1 the fetch L1 alone | 1x1 after | 1x1 after, both drafts | 8x8 before | 8x8 the fetch L1 alone | 8x8 after | 8x8 after, both drafts |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, last | 6.62 / 6.76 | 5.66 / 5.43 | 5.09 / 5.02 | 4.41 / 4.55 | **10.69** / **10.70** | 9.10 / 9.10 | 8.51 / 8.94 | 8.62 / 8.28 |
| ADP record, last | 4.94 / 5.06 | 4.02 / 3.88 | 3.77 / 3.56 | 3.22 / 3.24 | 8.13 / 8.14 | 6.91 / 6.91 | 6.68 / 6.86 | 6.64 / 6.52 |
| MAAP record, last | 4.93 / 5.09 | 4.06 / 3.92 | 3.81 / 3.60 | 3.25 / 3.27 | 8.12 / 8.13 | 6.89 / 6.89 | 6.66 / 6.84 | 6.63 / 6.50 |
| AECP record, last | **13.45** / **14.37** | **10.52** / **10.42** | 9.56 / 9.93 | 8.64 / 9.00 | **19.26** / **19.73** | **15.88** / **16.16** | **14.92** / **15.89** | **14.47** / **15.22** |
| SRP record, last | **15.30** / **14.84** | **11.03** / **10.71** | **10.41** / 9.91 | 9.11 / 9.26 | **21.76** / **21.07** | **16.89** / **16.64** | **16.30** / **16.39** | **15.81** / **15.19** |
| ACMP command behind a full ring | 5.44 / 5.40 | 4.19 / 4.14 | 3.91 / 3.69 | 3.44 / 3.44 | 9.85 / 9.86 | 8.42 / 8.42 | 7.87 / 8.29 | 7.98 / 7.63 |
| ENTITY_AVAILABLE behind a full ADP ring | 3.63 / 3.86 | 3.04 / 2.97 | 2.88 / 2.72 | 2.46 / 2.48 | 5.45 / 5.34 | 4.52 / 4.42 | 4.23 / 4.32 | 4.24 / 4.38 |
| The owed row, the commands behind it, the owed window's last AECP record | miss | miss | miss | miss | miss | miss | miss | miss |

The first records, an event behind 15 others and the refilling bucket fit everywhere.

**I$ refills per window** (the work passes overlapping each group's composed window, arm A / B):

| Window | before | the fetch L1 alone | after | after, both drafts |
|---|---:|---:|---:|---:|
| 1x1, the four groups | 5,539 to 11,698 (4.9 to 10.4 ms) | 1,497 to 4,216 (1.3 to 3.7 ms) | 1,488 to 4,488 (1.3 to 4.0 ms) | 1,529 to 3,995 (1.3 to 3.5 ms) |
| 8x8, the four groups | 9,029 to 12,592 (8.0 to 11.3 ms) | 3,569 to 4,314 (3.2 to 3.9 ms) | 3,922 to 4,642 (3.5 to 4.2 ms) | 3,972 to 4,522 (3.6 to 4.1 ms) |

The fetch L1 takes 60 to 70 % of the refills out of every window. Per group in `receipts/rows/irefills-*.md`.

**Behaviour** with the timing removed (16 group logs per pair, both points and arms): the mover and the primitives give identical egress and register sequences in every part. The other differences are timing alone: MAAP's clock-seeded addresses at 1x1, as round 7 found, and with the drafts the cross-channel `SEQ` of four transmit records in one 8x8 run. Every egress frame is identical.

**What holds the 8x8 rows** (both drafts staged): each window over T_svc runs 266,000 to 311,000 instructions. It waits 3.0 to 4.0 ms on instruction refills and has a data-cache refill outstanding for 2.5 to 3.7 ms. The work is spread over lwSRP (2.4 to 3.5 ms), ACMP's core (2.3 to 2.6), the memory primitives (2.0 to 2.5), AECP, the SRP adapter and the mailbox driver (1.1 to 2.0 each). No function holds 1.3 ms. Round 6's fetch-cache model was 0.8 to 1.6 ms optimistic about these rows at this geometry.

**Decisions needed:**
- the owner: scope, a 1x1-only split for Mark II;
- the ledger: 124 tiles is 2.5 over its ceiling, so per the area plan the manager commissions the redesign;
- the two drafts: lwSRP's and the TSN stack's reviews, then their pin moves.

**Risk:** the CI command table does not yet record the mailbox suite's new Verilator build form. Its checker needs the CI image's pinned shell parser, which this host lacks, so it did not run.

**Gates** (logs in `receipts/gates/` and `receipts/sweep/`; the head each ran at, the code being the final head's or what changed since named in HANDOFF section 6):
- **Full sweep**, four shard units at `b7c30969`: 64 / 64 suites, 2,551,847 checks, 0 in-suite failures, 0 timed out; the union tally rc 0. The mover's 360,473 checks and 17 of 17 plants are in it.
- **Firmware self-test**, four shards, `PASS`: shard 1 has `546 of 546` control plants caught, the six new memory plants among them. That needed `4e037d33`: one plant did not compile under `-Werror`.
- **Coverage** 100 % on both changed files; the RV32 self-test passes.
- `gen_mailbox.py --check --crosscheck --selftest` rc 0; the census rc 0 with the pinned tools.
- The lint ratchet, xvlog and the mover's Yosys row pass.
- The CPU option test, the builder (`ALL GATES PASS EXCEPT 1 NOT RUN`, the historical Arty report) and the harness self-test pass.
- The 96 docs, idiom, bare-metal and `behave` gates are rc 0 at the final head. The bare-metal gate first refused the retired name `DMA_RING`, renamed in `59038a1d`. After that rename the images are byte-identical, and the harness reproduces the measured leg exactly.
- rtl-fast's firmware-boundary step gives its known refusal of S2's harness files, byte-identical to rounds 5 to 7, and passes with S2's `e0e1b464`. The firmware-verilator step passes.

Handoff, PR body and receipts: the lane's output directory (HANDOFF.md, PR-BODY.md, receipts/INDEX.md).
