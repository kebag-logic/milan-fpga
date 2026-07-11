# Graph Report - milan-fpga  (2026-07-06)

## Corpus Check
- 346 files · ~375,478 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 396 nodes · 521 edges · 21 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e633032c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_milan_soc.py|milan_soc.py]]
- [[_COMMUNITY_PART A — Fully-FPGA RISC-V Linux platform|PART A — Fully-FPGA RISC-V Linux platform]]
- [[_COMMUNITY_Milan v1.2 endpoint — Functional & Non-Functional Requirements (FRNFR)|Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)]]
- [[_COMMUNITY_Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix|Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix]]
- [[_COMMUNITY_README|README.md]]
- [[_COMMUNITY_Latency & memory investigation — why single-port TCP caps at 30 Mbits (2026-07-05)|Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)]]
- [[_COMMUNITY_MilanDebug|MilanDebug]]
- [[_COMMUNITY_Direction from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)|Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)]]
- [[_COMMUNITY_The Full-FPGA Milan Solution — architecture, build, and how to continue|The Full-FPGA Milan Solution — architecture, build, and how to continue]]
- [[_COMMUNITY_2. Functional Requirements (FR)|2. Functional Requirements (FR)]]
- [[_COMMUNITY_MilanDebug|MilanDebug]]
- [[_COMMUNITY_PART B — ADP  AVDECC (the complete AVB solution)|PART B — ADP / AVDECC (the complete AVB solution)]]
- [[_COMMUNITY_Protocol validation matrix — every protocol, and every test that validates it|Protocol validation matrix — every protocol, and every test that validates it]]
- [[_COMMUNITY_Single-port throughput on VexiiRiscv — what a second core would (not) buy|Single-port throughput on VexiiRiscv — what a second core would (not) buy]]
- [[_COMMUNITY_Documentation index|Documentation index]]
- [[_COMMUNITY_CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)|CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)]]
- [[_COMMUNITY_Glossary|Glossary]]
- [[_COMMUNITY_MilanSimSoC|MilanSimSoC]]
- [[_COMMUNITY_drain|drain]]
- [[_COMMUNITY_HW-GRORSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)|HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)]]

## God Nodes (most connected - your core abstractions)
1. `BDHarness` - 22 edges
2. `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` - 20 edges
3. `Harness` - 18 edges
4. `PART A — Fully-FPGA RISC-V Linux platform` - 16 edges
5. `BDHarness` - 14 edges
6. `Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)` - 13 edges
7. `2. Functional Requirements (FR)` - 12 edges
8. `MilanDebug` - 11 edges
9. `tcp_frame()` - 11 edges
10. `HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)` - 11 edges

## Surprising Connections (you probably didn't know these)
- `BDHarness` --inherits--> `Harness`  [EXTRACTED]
  sw/litex/test_ring_bd.py →   _Bridges community 6 → community 9_

## Import Cycles
- None detected.

## Communities (21 total, 0 thin omitted)

### Community 0 - "milan_soc.py"
Cohesion: 0.07
Nodes (31): LiteXModule, SoCCore, add_milan_datapath(), _axis_dp_cdc(), _AxisDP, _CRG, main(), MilanDebug (+23 more)

### Community 1 - "PART A — Fully-FPGA RISC-V Linux platform"
Cohesion: 0.12
Nodes (16): A.10 — Boot & Linux (replaces the ARM boot), A.11 — Linux driver port (Phase 7, re-hosted), A.12 — Device tree (Phase 8, re-hosted), A.13 — Constraints (XDC) & board bring-up, A.14 — Alternative: Vivado-native AXI SoC (no LiteX), A.15 — Part A milestones & exit criteria, A.1 — Toolchain & repositories (host setup), A.2 — LiteX platform file for the AX7101 (+8 more)

### Community 2 - "Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)"
Cohesion: 0.06
Nodes (32): 1.1 Baseline (the "small" endpoint), 1.2 Scaling parameters (referenced throughout), 1.3 Actors, 1. Scope, actors, and the baseline system, 2.10 Host Linux driver  *(Phase 7 / `REQ-DRV-*`; needs a kernel tree — not buildable in this repo)*, 2.11 Device tree  *(Phase 8 / `REQ-DT-*`; the DT contract the driver binds to)*, 2.1 Discovery — ADP  *(1722.1-2021 §6; Milan v1.2 §5.2)*, 2.2 Enumeration & control — AECP/AEM  *(1722.1-2021 §7,§9; Milan v1.2 §5.3–5.4)* (+24 more)

### Community 3 - "Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix"
Cohesion: 0.10
Nodes (20): Section 10: Yosys / sv2v cannot find axis_mux_rr_2in_1out, Section 11: milan_dp AXI-write BFM did not commit writes, Section 12: Benign Verilator warnings (PINMISSING and SELRANGE), Section 13: traffic_queues silently dropped a frame, Section 14: datapath harness "≥2 queues" assertion failed, Section 15: `--full` fails 100 MHz timing in the CBS credit-shaper, Section 16: clean 100 MHz — run the dense datapath in its own clock domain, Section 17: on-hardware NIC bring-up — DMA works, but no packet on the wire (it's GMII, not RGMII) (+12 more)

### Community 4 - "README.md"
Cohesion: 0.22
Nodes (8): AVB / TSN / Milan, Ethernet / PHY / wire, FPGA / tooling, Glossary, Linux networking / performance, LiteX / SoC / boot, Project shorthand, This design (datapath, DMA, driver)

### Community 5 - "Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)"
Cohesion: 0.13
Nodes (15): 10. What changed this session, 11. Status & next steps, 1. The contradiction that drove everything, 2. What it is NOT (each ruled out by measurement), 3. The two regimes — flood localises the ceiling, 4.1 Decomposing the 1424 ns — TLB vs DRAM (hugepage A/B), 4. Root cause — memory latency (the 14k-pps ceiling), 5. The poll-CSR cost (why backing off the poll helps +32 %) (+7 more)

### Community 6 - "MilanDebug"
Cohesion: 0.19
Nodes (16): Harness, BDHarness, _csum_ref(), v2 realign: segment addresses at every offset 0..7 (Ethernet's skb->data is, 16-bit LE-lane ones-complement sum, folded (the engine's convention)., v2b HW checksum-insert: BD w1 {en<<63, off<<16}; the engine pre-passes the     s, cs-across-BDs (soft-TSO enabler): w1 {en,off} on the chain's FIRST BD makes, Cross-BD continuity: mid-segments of ARBITRARY length (the old %8 contract is (+8 more)

### Community 7 - "Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)"
Cohesion: 0.08
Nodes (23): CPU budget vs the 4-port switch (measured 2026-07-05, xc7a100t = 63,400 LUTs), Decision matrix (2026-07-05, scope: **4× GMII/RGMII copper ports**, MTU fixed 1500), Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500), Execution order, Hardware reality, Memory: "would a wider bus help?" (panel ④), Step plan for the executed session (C1/C2/I1), The constraint set (+15 more)

### Community 8 - "The Full-FPGA Milan Solution — architecture, build, and how to continue"
Cohesion: 0.14
Nodes (14): 1. What the full-FPGA solution is (high level), 2. The protocol stack (high level), 3. Status at a glance, 4. Repository map (medium level), 5.1 Control — `milan_csr` (AXI4-Lite), 5.2 Data — `MilanDMA` (§A.6, `--with-dma`), 5.3 MAC — `MilanMAC` (§A.7, `--with-mac`), 5.4 Events — IRQ → PLIC (+6 more)

### Community 9 - "2. Functional Requirements (FR)"
Cohesion: 0.13
Nodes (31): BDHarness, csum_ref(), Multi-burst frame LARGER than the BD ring: every payload byte must land intact., Driver-reload regression (silicon bug 2026-07-05): buffers posted by a previous, Minimal eth+IPv4+TCP frame as 64-bit LE words (RSC parser test vector)., RSC phase A: with rsc_en=1 the head beats detour through the regfile —     the d, SYN and non-TCP frames must parse as ineligible., Phase B: three in-order same-flow segments -> ONE buffer, ONE v2 BD.     Buffer (+23 more)

### Community 10 - "MilanDebug"
Cohesion: 0.40
Nodes (4): SimSoC, main(), MilanSimSoC, SimSoC + the Milan TSN datapath as an AXI4-Lite CSR slave at 0x9000_0000.

### Community 11 - "PART B — ADP / AVDECC (the complete AVB solution)"
Cohesion: 0.10
Nodes (20): 0. Decisions & assumptions (confirm before starting), 1.1 What the PL already owns (reuse as-is), 1.2 What the Zynq PS provides today (must be re-created in fabric), 1.3 The one hard consequence of removing the PS, 1. Why this is a "port the host, keep the datapath" job, 3. Effort, risk, and ordering, 4. What changes in the repo (file-level), 5. Open items to confirm (+12 more)

### Community 12 - "Protocol validation matrix — every protocol, and every test that validates it"
Cohesion: 0.08
Nodes (23): 1. L1 / L2 — Ethernet, filtering, stats, 2. Shaping / QoS — 802.1Qav CBS, 3. Timing — gPTP / 802.1AS + PHC, 4. Discovery / control — AVDECC (IEEE 1722.1-2021 + Milan v1.2), 5. Reservation + address allocation, 6. Media transport — AVTP (IEEE 1722), 7. Host / SoC / driver, 8. Test inventory (how to run every automated test today) (+15 more)

### Community 13 - "Single-port throughput on VexiiRiscv — what a second core would (not) buy"
Cohesion: 0.17
Nodes (11): Bottom line for the switch, Levers that *would* move single-flow throughput — and why they're out, Matrix 1 — baseline single flow, Matrix 2 — RX-coalesce (poll-cadence) sweep, Matrix 3 — parallel streams (does the ceiling aggregate?), Reproduce, Root cause — a per-frame *latency* ceiling, not a *throughput* one, Single-port throughput on VexiiRiscv — what a second core would (not) buy (+3 more)

### Community 14 - "Documentation index"
Cohesion: 0.14
Nodes (13): 1 — System overview & architecture, 2 — Design direction & plans, 3 — Contracts: ABI, requirements, validation, 4 — Build, boot & operate, 5 — Findings: bugs cornered and measured on silicon, 6 — Module & verification docs, Conventions, Documentation index (+5 more)

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

### Community 22 - "HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07)"
Cohesion: 0.13
Nodes (15): As-built rules — where the implementation pins down (or diverges from) the spec text, BD format v2 (16 B, LE) — merged aggregates, Buffer/write path, Driver contract, HW-GRO/RSC — receive-side coalescing in the RX BD engine (design, 2026-07-07), Implementation status (2026-07-07) — phases A+B DONE, sim-verified, Merge rules (v1), Phase C — DONE (commit `18fcec3`, 16/16 sims) (+7 more)

## Knowledge Gaps
- **203 isolated node(s):** `Merge rules (v1)`, `Buffer/write path`, `BD format v2 (16 B, LE) — merged aggregates`, `Driver contract`, `RTL integration points (RingDMAWriter, BD mode only)` (+198 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Milan on a fully-FPGA RISC-V platform — detailed migration & implementation plan` connect `PART B — ADP / AVDECC (the complete AVB solution)` to `PART A — Fully-FPGA RISC-V Linux platform`, `Protocol validation matrix — every protocol, and every test that validates it`?**
  _High betweenness centrality (0.059) - this node is a cross-community bridge._
- **Why does `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` connect `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` to `Protocol validation matrix — every protocol, and every test that validates it`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` connect `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` to `Protocol validation matrix — every protocol, and every test that validates it`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Clock/reset: PLL the 200 MHz board clock down to the system clock.      With `wi`, `The Milan TSN datapath (`milan_datapath.sv`) wired into the SoC.      `milan_dat`, `Instantiate `milan_datapath` and add its RTL sources — the single place the` to the rest of the system?**
  _244 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `milan_soc.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0673758865248227 - nodes in this community are weakly interconnected._
- **Should `PART A — Fully-FPGA RISC-V Linux platform` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` be split into smaller, more focused modules?**
  _Cohesion score 0.0625 - nodes in this community are weakly interconnected._