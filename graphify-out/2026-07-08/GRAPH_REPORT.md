# Graph Report - milan-fpga  (2026-07-08)

## Corpus Check
- 358 files · ~407,950 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 615 nodes · 802 edges · 31 communities (29 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0a1f3063`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_milan_soc.py|milan_soc.py]]
- [[_COMMUNITY_H|H]]
- [[_COMMUNITY_Milan v1.2 endpoint — Functional & Non-Functional Requirements (FRNFR)|Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)]]
- [[_COMMUNITY_Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix|Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_Latency & memory investigation — why single-port TCP caps at 30 Mbits (2026-07-05)|Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)]]
- [[_COMMUNITY_MilanDebug|MilanDebug]]
- [[_COMMUNITY_Direction from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)|Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)]]
- [[_COMMUNITY_TX RingDMAReader prefetch — design plan (roadmap step 1, primary TX lever)|TX RingDMAReader prefetch — design plan (roadmap step 1, primary TX lever)]]
- [[_COMMUNITY_2. Functional Requirements (FR)|2. Functional Requirements (FR)]]
- [[_COMMUNITY_MilanDebug|MilanDebug]]
- [[_COMMUNITY_PART B — ADP  AVDECC (the complete AVB solution)|PART B — ADP / AVDECC (the complete AVB solution)]]
- [[_COMMUNITY_Protocol validation matrix — every protocol, and every test that validates it|Protocol validation matrix — every protocol, and every test that validates it]]
- [[_COMMUNITY_RX fan-out & the TX throughput ceiling (2026-07-07)|RX fan-out & the TX throughput ceiling (2026-07-07)]]
- [[_COMMUNITY_Documentation index|Documentation index]]
- [[_COMMUNITY_PART A — Fully-FPGA RISC-V Linux platform|PART A — Fully-FPGA RISC-V Linux platform]]
- [[_COMMUNITY_CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)|CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)]]
- [[_COMMUNITY_Glossary|Glossary]]
- [[_COMMUNITY_MilanSimSoC|MilanSimSoC]]
- [[_COMMUNITY_drain|drain]]
- [[_COMMUNITY_Throughput goal — ≥200 Mbits RX and TX, reach for 1 Gbits|Throughput goal — ≥200 Mbit/s RX *and* TX, reach for 1 Gbit/s]]
- [[_COMMUNITY_HW-GRORSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)|HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)]]
- [[_COMMUNITY_sim_main.cpp|sim_main.cpp]]
- [[_COMMUNITY_milan_csr.sv|milan_csr.sv]]
- [[_COMMUNITY_Register groups|Register groups]]
- [[_COMMUNITY_RX overload wedge — completion-order inversion under RSC + ACK-merge FIXED in sim|RX overload wedge — completion-order inversion under RSC + ACK-merge [FIXED in sim]]]
- [[_COMMUNITY_CBS default-shaping bug — reset config paced ALL best-effort TX at 300 Mbs FIXED|CBS default-shaping bug — reset config paced ALL best-effort TX at 300 Mb/s [FIXED]]]
- [[_COMMUNITY_RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision|RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision]]
- [[_COMMUNITY_tools_lat_mem_rd.c|tools_lat_mem_rd.c]]
- [[_COMMUNITY_milan_soc.py|milan_soc.py]]

## God Nodes (most connected - your core abstractions)
1. `BDHarness` - 27 edges
2. `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` - 20 edges
3. `Harness` - 18 edges
4. `MilanDebug` - 17 edges
5. `Campaign plan: >500 Mbit/s TX *and* RX — every step gated by a gateware measurement` - 16 edges
6. `PART A — Fully-FPGA RISC-V Linux platform` - 16 edges
7. `BDHarness` - 15 edges
8. `Throughput goal — >500 Mbit/s RX *and* TX, reach for 1 Gbit/s` - 13 edges
9. `Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)` - 13 edges
10. `RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision` - 12 edges

## Surprising Connections (you probably didn't know these)
- `MilanDebug` --inherits--> `LiteXModule`  [EXTRACTED]
  sw/litex/milan_soc.py →   _Bridges community 0 → community 10_
- `BDHarness` --inherits--> `Harness`  [EXTRACTED]
  sw/litex/test_ring_bd.py →   _Bridges community 9 → community 6_

## Import Cycles
- None detected.

## Communities (31 total, 2 thin omitted)

### Community 0 - "milan_soc.py"
Cohesion: 0.07
Nodes (30): LiteXModule, SimSoC, SoCCore, main(), MilanSimSoC, SimSoC + the Milan TSN datapath as an AXI4-Lite CSR slave at 0x9000_0000., add_milan_datapath(), _axis_dp_cdc() (+22 more)

### Community 1 - "H"
Cohesion: 0.35
Nodes (7): arp_frame(), H, reassemble queue qi's beats into frames (bytes)., ref_hash(), tcp_frame(), test_nonip_and_bypass(), test_route_and_consistency()

### Community 2 - "Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)"
Cohesion: 0.06
Nodes (32): 1.1 Baseline (the "small" endpoint), 1.2 Scaling parameters (referenced throughout), 1.3 Actors, 1. Scope, actors, and the baseline system, 2.10 Host Linux driver  *(Phase 7 / `REQ-DRV-*`; needs a kernel tree — not buildable in this repo)*, 2.11 Device tree  *(Phase 8 / `REQ-DT-*`; the DT contract the driver binds to)*, 2.1 Discovery — ADP  *(1722.1-2021 §6; Milan v1.2 §5.2)*, 2.2 Enumeration & control — AECP/AEM  *(1722.1-2021 §7,§9; Milan v1.2 §5.3–5.4)* (+24 more)

### Community 3 - "Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix"
Cohesion: 0.06
Nodes (31): 1. L1 / L2 — Ethernet, filtering, stats, 2. Shaping / QoS — 802.1Qav CBS, 3. Timing — gPTP / 802.1AS + PHC, 4. Discovery / control — AVDECC (IEEE 1722.1-2021 + Milan v1.2), 5. Reservation + address allocation, 6. Media transport — AVTP (IEEE 1722), 7. Host / SoC / driver, 8. Test inventory (how to run every automated test today) (+23 more)

### Community 4 - "README.md"
Cohesion: 0.22
Nodes (8): AVB / TSN / Milan, Ethernet / PHY / wire, FPGA / tooling, Glossary, Linux networking / performance, LiteX / SoC / boot, Project shorthand, This design (datapath, DMA, driver)

### Community 5 - "Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)"
Cohesion: 0.13
Nodes (15): 10. What changed this session, 11. Status & next steps, 1. The contradiction that drove everything, 2. What it is NOT (each ruled out by measurement), 3. The two regimes — flood localises the ceiling, 4.1 Decomposing the 1424 ns — TLB vs DRAM (hugepage A/B), 4. Root cause — memory latency (the 14k-pps ceiling), 5. The poll-CSR cost (why backing off the poll helps +32 %) (+7 more)

### Community 6 - "MilanDebug"
Cohesion: 0.12
Nodes (27): Harness, BDHarness, _csum_ref(), _fold_nc(), _ip_check(), _lanes(), _mk_template(), v2 realign: segment addresses at every offset 0..7 (Ethernet's skb->data is (+19 more)

### Community 7 - "Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)"
Cohesion: 0.08
Nodes (23): CPU budget vs the 4-port switch (measured 2026-07-05, xc7a100t = 63,400 LUTs), Decision matrix (2026-07-05, scope: **4× GMII/RGMII copper ports**, MTU fixed 1500), Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500), Execution order, Hardware reality, Memory: "would a wider bus help?" (panel ④), Step plan for the executed session (C1/C2/I1), The constraint set (+15 more)

### Community 8 - "TX RingDMAReader prefetch — design plan (roadmap step 1, primary TX lever)"
Cohesion: 0.12
Nodes (16): Campaign plan: >500 Mbit/s TX *and* RX — every step gated by a gateware measurement, DECISION (2026-07-08): stay at 100 MHz; next lever = L2/memory, Existing gateware measurement surface (validated this campaign), Gate summary (the plan on one line each), Phase M1 — instrumentation build (FIRST: the probes the plan needs), Phase R0 — full re-baseline on the instrumented, storm-proof gateware, Phase R1 — RX 2-queue fan-out at 100 MHz (the mandatory RX lever), Phase R2 — RX per-aggregate cost: RSC geometry + delivery tuning (+8 more)

### Community 9 - "2. Functional Requirements (FR)"
Cohesion: 0.05
Nodes (65): BDHarness, csum_ref(), DriverModel, _mk_overload_harness(), Seeded silicon-realistic RSC storm vs invariants I1/I2/I3., Storm at REAL silicon geometry: 1448-byte MSS segs (183 beats — deep multi-burst, THE parallel-storm delivery death (silicon 2026-07-08, decoded off the dead, M1 telemetry (CAMPAIGN_500_PLAN): the close-reason counters + coalesce ratio (+57 more)

### Community 10 - "MilanDebug"
Cohesion: 0.12
Nodes (14): MilanDebug, Memory-mapped observability for the whole TX+RX AXIS pipeline — the numbers a HW, Latch `live` into a shadow on `capture` and expose it as a CSR., frames / beats / stalls at a sys-domain AXIS endpoint. Returns the frame counter, busy/stall/starve/cyc at a datapath-input endpoint in domain `cd`, to sys., Frame count at an endpoint in clock domain `cd`, brought to sys and captured., Count only frames for which `match` (held over the frame) is asserted at `last`., Count frames whose (untagged) EtherType == `etype`. `ep` must carry `.data` (+6 more)

### Community 11 - "PART B — ADP / AVDECC (the complete AVB solution)"
Cohesion: 0.06
Nodes (36): 0. Decisions & assumptions (confirm before starting), 1.1 What the PL already owns (reuse as-is), 1.2 What the Zynq PS provides today (must be re-created in fabric), 1.3 The one hard consequence of removing the PS, 1. Why this is a "port the host, keep the datapath" job, 3. Effort, risk, and ordering, 4. What changes in the repo (file-level), 5. Open items to confirm (+28 more)

### Community 12 - "Protocol validation matrix — every protocol, and every test that validates it"
Cohesion: 0.14
Nodes (14): 1. What the full-FPGA solution is (high level), 2. The protocol stack (high level), 3. Status at a glance, 4. Repository map (medium level), 5.1 Control — `milan_csr` (AXI4-Lite), 5.2 Data — `MilanDMA` (§A.6, `--with-dma`), 5.3 MAC — `MilanMAC` (§A.7, `--with-mac`), 5.4 Events — IRQ → PLIC (+6 more)

### Community 13 - "RX fan-out & the TX throughput ceiling (2026-07-07)"
Cohesion: 0.17
Nodes (11): Artifacts, Direct proof the datapath is the TX limit (datapath-input probe), Effort 01 — Hardware header-generation TSO, Effort 02 — the single-flow ceiling (profiled), Effort 03 — the RX fan-out (RX −P2 = 223), Effort 04 — the 100 MHz datapath fix (measured on silicon), Ops notes, RX fan-out & the TX throughput ceiling (2026-07-07) (+3 more)

### Community 14 - "Documentation index"
Cohesion: 0.08
Nodes (24): 1 — System overview & architecture, 2 — Design direction & plans, 3 — Contracts: ABI, requirements, validation, 4 — Build, boot & operate, 5 — Findings: bugs cornered and measured on silicon, 6 — Module & verification docs, Conventions, Documentation index (+16 more)

### Community 15 - "PART A — Fully-FPGA RISC-V Linux platform"
Cohesion: 0.38
Nodes (3): capture(), reset_ctrs(), phase0_measure.sh script

### Community 16 - "CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)"
Cohesion: 0.13
Nodes (15): 2026-07-06 addendum — batching + a false-parity retraction, 2026-07-07 campaign — SMP, the three-copies profile, copybreak RX, stall verdict, Bring-up log & current state (2026-07-05, end of session), CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan), Current RX path (silicon-proven `RingDMAWriter`), Layer-per-layer debug method (use `lview.sh`), Net effect on MAC RAM, P5 v1 TX-BD — silicon results (2026-07-06) (+7 more)

### Community 17 - "Glossary"
Cohesion: 0.20
Nodes (12): frame(), Harness, Wait until nothing is buffered AND wr_ptr has been stable for `settle` cycles, Ones-complement sum of 16-bit LE lanes — what the ingress must deliver., Walk `count` committed frames from ring offset rd; return (frames, seqs, rd)., One DUT + AXI-slave memory model + always-ready monitor, driven per scenario., test_4k_split(), test_basic() (+4 more)

### Community 18 - "MilanSimSoC"
Cohesion: 0.13
Nodes (14): 2026-07-06: zero-upload ACHIEVED — the sizes that made "full" fit, Build a flash-boot bitstream, Caveats, Flash layout (`FLASHBOOT_LAYOUT` in `milan_soc.py`), Flash the kernel once (partial mode), Getting to zero-upload, How the boot works, Iterate (the fast loop) (+6 more)

### Community 19 - "drain"
Cohesion: 0.60
Nodes (4): drain(), Feed n_frames back-to-back; return (cycles_to_drain, wr, drops, shadow_word)., test_writeback_bandwidth(), test_writeback_correctness()

### Community 21 - "Throughput goal — ≥200 Mbit/s RX *and* TX, reach for 1 Gbit/s"
Cohesion: 0.05
Nodes (36): Detailed investigations (read these for the evidence), Ground rules for this campaign, (original T1 notes below), Phase X MEASURED (2026-07-08) — clock uplift REFUTES the linear projection, Phase X status + T2 latency decomposition (2026-07-08), R0 baseline (signed, 2026-07-08, `build_dp100_m1` WNS +0.056 — CAMPAIGN_500_PLAN), R1 result (2026-07-08, `build_dp100_m1`, hash_sel=0 — 2-queue fan-out LIVE), Roadmap toward >500 Mbit/s, then 1 Gbit/s (ordered, each independently measurable) (+28 more)

### Community 22 - "HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)"
Cohesion: 0.10
Nodes (20): ACK-run merging — LIVE on silicon (2026-07-07): TX 109 → 121, As-built rules — where the implementation pins down (or diverges from) the spec text, BD format v2 (16 B, LE) — merged aggregates, Buffer/write path, Driver contract, Driver robustness (the-private-test-repo `85122fa`), HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07), Implementation status (2026-07-07) — phases A+B DONE, sim-verified (+12 more)

### Community 23 - "sim_main.cpp"
Cohesion: 0.73
Nodes (5): axi_read(), axi_write(), ck(), main(), posedge()

### Community 25 - "Register groups"
Cohesion: 0.17
Nodes (12): 0x000 — Identification / IRQ, 0x100 — MAC control / status  `(REQ-MAC-01..03)`, 0x200 — Statistics (RMON)  `(REQ-MAC-04)`, 0x300 — 802.1Q classifier  `(REQ-CLS-01..04)`, 0x400 — 802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`, 0x500 — PTP hardware clock  `(REQ-PTP-01..04, 06)`, 0x600 — ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`, 0x700 — RX destination-MAC TCAM filter  `(REQ-MAC-02)` (+4 more)

### Community 26 - "RX overload wedge — completion-order inversion under RSC + ACK-merge [FIXED in sim]"
Cohesion: 0.17
Nodes (11): Defense in depth (driver, kl-eth `83aa7ec`), Lessons, RX overload wedge — TWO bugs: BD-order inversion + drops/v2-marker alias [FIXED, silicon-validated], Silicon forensics — "delivery dead, hardware healthy", Status — silicon results (2026-07-08, `build_dp100_wfix`, WNS +0.092), Symptom (silicon), The contract, stated, The fix (`09e3a09`) — BD order == pop order by construction (+3 more)

### Community 27 - "CBS default-shaping bug — reset config paced ALL best-effort TX at 300 Mb/s [FIXED]"
Cohesion: 0.29
Nodes (6): CBS default-shaping bug — reset config paced ALL best-effort TX at 300 Mb/s [FIXED], Lessons, Root cause — two defaults contradicting each other, Symptom, The fix, Verification on silicon (before fixing)

### Community 28 - "RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision"
Cohesion: 0.15
Nodes (12): Architecture finding (2026-07-08) — why a network *scratchpad* is the wrong lever HERE, BRAM budget (the shared constraint — L2 and network-SRAM compete), Branch A — capacity-bound: grow / partition the L2, Branch B — cold / bandwidth-bound: the dedicated network cache, Decision tree (one glance), Gates & rule, Phase L2 RESULT (2026-07-08) — CAPACITY-bound CONFIRMED; L2 is the lever, RX memory-hierarchy plan — cold vs capacity, and the dedicated-network-cache decision (+4 more)

### Community 30 - "milan_soc.py"
Cohesion: 0.14
Nodes (13): 0. Why this exists, 1. The LSU and its L1 D-cache at a glance, 2. The load pipeline and what "miss" means, 3. The refill engine — the "8 refills", 4. The L1↔L2 bus: where the parallelism is spent, 5. The honest part: how MLP actually arises on an *in-order* core, 6. Timeline picture, 7. What we built and MEASURED on silicon (2026-07-08) (+5 more)

## Knowledge Gaps
- **299 isolated node(s):** `0. Why this exists`, `1. The LSU and its L1 D-cache at a glance`, `2. The load pipeline and what "miss" means`, `Lifecycle of one refill`, `The one line that defines "blocking" vs "non-blocking"` (+294 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Milan on a fully-FPGA RISC-V platform — detailed migration & implementation plan` connect `PART B — ADP / AVDECC (the complete AVB solution)` to `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `BDHarness` connect `2. Functional Requirements (FR)` to `MilanDebug`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **What connects `0. Why this exists`, `1. The LSU and its L1 D-cache at a glance`, `2. The load pipeline and what "miss" means` to the rest of the system?**
  _372 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `milan_soc.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06765327695560254 - nodes in this community are weakly interconnected._
- **Should `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` be split into smaller, more focused modules?**
  _Cohesion score 0.06060606060606061 - nodes in this community are weakly interconnected._
- **Should `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` be split into smaller, more focused modules?**
  _Cohesion score 0.05873015873015873 - nodes in this community are weakly interconnected._
- **Should `Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._