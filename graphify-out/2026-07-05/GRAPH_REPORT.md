# Graph Report - milan-fpga  (2026-07-05)

## Corpus Check
- 343 files · ~363,104 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 278 nodes · 323 edges · 21 communities
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `04941ffd`
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
- [[_COMMUNITY_Register groups|Register groups]]
- [[_COMMUNITY_PART B — ADP  AVDECC (the complete AVB solution)|PART B — ADP / AVDECC (the complete AVB solution)]]
- [[_COMMUNITY_Protocol validation matrix — every protocol, and every test that validates it|Protocol validation matrix — every protocol, and every test that validates it]]
- [[_COMMUNITY_Single-port throughput on VexiiRiscv — what a second core would (not) buy|Single-port throughput on VexiiRiscv — what a second core would (not) buy]]
- [[_COMMUNITY_Documentation index|Documentation index]]
- [[_COMMUNITY_RX ring DMA — root cause of the large-frame RX loss + the AXI-burst fix|RX ring DMA — root cause of the large-frame RX loss + the AXI-burst fix]]
- [[_COMMUNITY_CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)|CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)]]
- [[_COMMUNITY_Glossary|Glossary]]
- [[_COMMUNITY_MilanSimSoC|MilanSimSoC]]
- [[_COMMUNITY_drain|drain]]

## God Nodes (most connected - your core abstractions)
1. `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` - 20 edges
2. `PART A — Fully-FPGA RISC-V Linux platform` - 16 edges
3. `Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)` - 13 edges
4. `2. Functional Requirements (FR)` - 12 edges
5. `MilanDebug` - 11 edges
6. `PART B — ADP / AVDECC (the complete AVB solution)` - 11 edges
7. `Protocol validation matrix — every protocol, and every test that validates it` - 11 edges
8. `The Full-FPGA Milan Solution — architecture, build, and how to continue` - 10 edges
9. `Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)` - 9 edges
10. `Documentation index` - 9 edges

## Surprising Connections (you probably didn't know these)
- `MilanDebug` --inherits--> `LiteXModule`  [EXTRACTED]
  sw/litex/milan_soc.py →   _Bridges community 0 → community 6_

## Import Cycles
- None detected.

## Communities (21 total, 0 thin omitted)

### Community 0 - "milan_soc.py"
Cohesion: 0.09
Nodes (23): LiteXModule, SoCCore, add_milan_datapath(), _axis_dp_cdc(), _AxisDP, _CRG, main(), MilanDMA (+15 more)

### Community 1 - "PART A — Fully-FPGA RISC-V Linux platform"
Cohesion: 0.08
Nodes (25): 0. Decisions & assumptions (confirm before starting), 1.1 What the PL already owns (reuse as-is), 1.2 What the Zynq PS provides today (must be re-created in fabric), 1.3 The one hard consequence of removing the PS, 1. Why this is a "port the host, keep the datapath" job, 3. Effort, risk, and ordering, 4. What changes in the repo (file-level), 5. Open items to confirm (+17 more)

### Community 2 - "Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)"
Cohesion: 0.10
Nodes (20): 1.1 Baseline (the "small" endpoint), 1.2 Scaling parameters (referenced throughout), 1.3 Actors, 1. Scope, actors, and the baseline system, 3.1 Performance & real-time, 3.2 Time accuracy, 3.3 Scale-**up** (same node, bigger workload), 3.4 Scale-**out** (more than one softcore)  *(the key architectural NFR)* (+12 more)

### Community 3 - "Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix"
Cohesion: 0.10
Nodes (20): Section 10: Yosys / sv2v cannot find axis_mux_rr_2in_1out, Section 11: milan_dp AXI-write BFM did not commit writes, Section 12: Benign Verilator warnings (PINMISSING and SELRANGE), Section 13: traffic_queues silently dropped a frame, Section 14: datapath harness "≥2 queues" assertion failed, Section 15: `--full` fails 100 MHz timing in the CBS credit-shaper, Section 16: clean 100 MHz — run the dense datapath in its own clock domain, Section 17: on-hardware NIC bring-up — DMA works, but no packet on the wire (it's GMII, not RGMII) (+12 more)

### Community 4 - "README.md"
Cohesion: 0.22
Nodes (4): Developers, Maintainers, milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA, Running the testbenches

### Community 5 - "Latency & memory investigation — why single-port TCP caps at 30 Mbit/s (2026-07-05)"
Cohesion: 0.13
Nodes (15): 10. What changed this session, 11. Status & next steps, 1. The contradiction that drove everything, 2. What it is NOT (each ruled out by measurement), 3. The two regimes — flood localises the ceiling, 4.1 Decomposing the 1424 ns — TLB vs DRAM (hugepage A/B), 4. Root cause — memory latency (the 14k-pps ceiling), 5. The poll-CSR cost (why backing off the poll helps +32 %) (+7 more)

### Community 6 - "MilanDebug"
Cohesion: 0.23
Nodes (8): MilanDebug, Memory-mapped observability for the whole TX+RX AXIS pipeline — the numbers a HW, Latch `live` into a shadow on `capture` and expose it as a CSR., frames / beats / stalls at a sys-domain AXIS endpoint. Returns the frame counter, Frame count at an endpoint in clock domain `cd`, brought to sys and captured., Count only frames for which `match` (held over the frame) is asserted at `last`., Count frames whose (untagged) EtherType == `etype`. `ep` must carry `.data`, Σ(cin−cout) per cycle across a segment: avg occupancy = acc/cycles, avg wait = a

### Community 7 - "Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500)"
Cohesion: 0.14
Nodes (14): CPU budget vs the 4-port switch (measured 2026-07-05, xc7a100t = 63,400 LUTs), Decision matrix (2026-07-05, scope: **4× GMII/RGMII copper ports**, MTU fixed 1500), Direction: from the 1-NIC endpoint to a 4-port AVB switch (MTU fixed at 1500), Execution order, Hardware reality, Memory: "would a wider bus help?" (panel ④), Step plan for the executed session (C1/C2/I1), The constraint set (+6 more)

### Community 8 - "The Full-FPGA Milan Solution — architecture, build, and how to continue"
Cohesion: 0.14
Nodes (14): 1. What the full-FPGA solution is (high level), 2. The protocol stack (high level), 3. Status at a glance, 4. Repository map (medium level), 5.1 Control — `milan_csr` (AXI4-Lite), 5.2 Data — `MilanDMA` (§A.6, `--with-dma`), 5.3 MAC — `MilanMAC` (§A.7, `--with-mac`), 5.4 Events — IRQ → PLIC (+6 more)

### Community 9 - "2. Functional Requirements (FR)"
Cohesion: 0.17
Nodes (12): 2.10 Host Linux driver  *(Phase 7 / `REQ-DRV-*`; needs a kernel tree — not buildable in this repo)*, 2.11 Device tree  *(Phase 8 / `REQ-DT-*`; the DT contract the driver binds to)*, 2.1 Discovery — ADP  *(1722.1-2021 §6; Milan v1.2 §5.2)*, 2.2 Enumeration & control — AECP/AEM  *(1722.1-2021 §7,§9; Milan v1.2 §5.3–5.4)*, 2.3 Milan Vendor Unique — MVU  *(Milan v1.2 §5.4.3)*, 2.4 Connection management — ACMP  *(1722.1-2021 §8; Milan v1.2 §5.5)*, 2.5 Addressing & reservation — MAAP, SRP  *(1722 Annex B; 802.1Qat/Qak; Milan §5.6)*, 2.6 Time & media clock — gPTP, CRF  *(802.1AS; 1722-2016 §10; Milan §5.7)* (+4 more)

### Community 10 - "Register groups"
Cohesion: 0.17
Nodes (12): 0x000 — Identification / IRQ, 0x100 — MAC control / status  `(REQ-MAC-01..03)`, 0x200 — Statistics (RMON)  `(REQ-MAC-04)`, 0x300 — 802.1Q classifier  `(REQ-CLS-01..04)`, 0x400 — 802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`, 0x500 — PTP hardware clock  `(REQ-PTP-01..04, 06)`, 0x600 — ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`, 0x700 — RX destination-MAC TCAM filter  `(REQ-MAC-02)` (+4 more)

### Community 11 - "PART B — ADP / AVDECC (the complete AVB solution)"
Cohesion: 0.18
Nodes (11): B.0 — HW/SW split (the key architectural decision), B.1 — Connect the control-frame path into the datapath, B.2 — HW ADP advertiser + discovery FSM (the missing TX side)  ✅ DONE + INTEGRATED, B.3 — AECP (AEM) — enumeration & control (from the JSON entity model), B.4 — ACMP — stream connection management (software), B.5 — MAAP — multicast address allocation (software daemon + HW filter), B.6 — SRP / MSRP / MVRP — reservation plane (software, big), B.7 — (Optional, D5) AVTP talker/listener media datapath (+3 more)

### Community 12 - "Protocol validation matrix — every protocol, and every test that validates it"
Cohesion: 0.18
Nodes (11): 1. L1 / L2 — Ethernet, filtering, stats, 2. Shaping / QoS — 802.1Qav CBS, 3. Timing — gPTP / 802.1AS + PHC, 4. Discovery / control — AVDECC (IEEE 1722.1-2021 + Milan v1.2), 5. Reservation + address allocation, 6. Media transport — AVTP (IEEE 1722), 7. Host / SoC / driver, 8. Test inventory (how to run every automated test today) (+3 more)

### Community 13 - "Single-port throughput on VexiiRiscv — what a second core would (not) buy"
Cohesion: 0.18
Nodes (11): Bottom line for the switch, Levers that *would* move single-flow throughput — and why they're out, Matrix 1 — baseline single flow, Matrix 2 — RX-coalesce (poll-cadence) sweep, Matrix 3 — parallel streams (does the ceiling aggregate?), Reproduce, Root cause — a per-frame *latency* ceiling, not a *throughput* one, Single-port throughput on VexiiRiscv — what a second core would (not) buy (+3 more)

### Community 14 - "Documentation index"
Cohesion: 0.22
Nodes (9): 1 — System overview & architecture, 2 — Design direction & plans, 3 — Contracts: ABI, requirements, validation, 4 — Build, boot & operate, 5 — Findings: bugs cornered and measured on silicon, 6 — Module & verification docs, Conventions, Documentation index (+1 more)

### Community 15 - "RX ring DMA — root cause of the large-frame RX loss + the AXI-burst fix"
Cohesion: 0.22
Nodes (9): How it works (v2 mechanism, end to end), Measured ladder (silicon, night of 2026-07-04/05 — each step verified end-to-end), Related, RX ring DMA — root cause of the large-frame RX loss + the AXI-burst fix, The fix — `RingDMAWriter` v2 (`sw/litex/milan_soc.py`), The measurement chain (how to pin this class of bug fast), The TX mirror — `RingDMAReader` (same night, same disease, same cure), TL;DR (+1 more)

### Community 16 - "CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan)"
Cohesion: 0.25
Nodes (8): CPPI-style DMA redesign — on-chip descriptors, cut-through, zero-copy (plan), Current RX path (silicon-proven `RingDMAWriter`), Net effect on MAC RAM, Phased plan (each phase builds + is sim-verified against `sw/litex/test_ring_*.py`), Relation to the switch, Risk & verification, Target CPPI-style RX path, Why (measured, from LATENCY_INVESTIGATION.md)

### Community 17 - "Glossary"
Cohesion: 0.25
Nodes (8): AVB / TSN / Milan, Ethernet / PHY / wire, FPGA / tooling, Glossary, Linux networking / performance, LiteX / SoC / boot, Project shorthand, This design (datapath, DMA, driver)

### Community 18 - "MilanSimSoC"
Cohesion: 0.40
Nodes (4): SimSoC, main(), MilanSimSoC, SimSoC + the Milan TSN datapath as an AXI4-Lite CSR slave at 0x9000_0000.

### Community 19 - "drain"
Cohesion: 0.60
Nodes (4): drain(), Feed n_frames back-to-back; return (cycles_to_drain, wr, drops, shadow_word)., test_writeback_bandwidth(), test_writeback_correctness()

## Knowledge Gaps
- **173 isolated node(s):** `Running the testbenches`, `Maintainers`, `The constraint set`, `The three endpoint hooks (panel ①/②)`, `The switch data plane (panel ③)` (+168 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Milan on a fully-FPGA RISC-V platform — detailed migration & implementation plan` connect `PART A — Fully-FPGA RISC-V Linux platform` to `PART B — ADP / AVDECC (the complete AVB solution)`, `README.md`?**
  _High betweenness centrality (0.177) - this node is a cross-community bridge._
- **Why does `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` connect `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` to `2. Functional Requirements (FR)`, `README.md`?**
  _High betweenness centrality (0.160) - this node is a cross-community bridge._
- **Why does `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` connect `Troubleshooting — every problem hit bringing up the full-FPGA solution, and its fix` to `README.md`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **What connects `Clock/reset: PLL the 200 MHz board clock down to the system clock.      With `wi`, `The Milan TSN datapath (`milan_datapath.sv`) wired into the SoC.      `milan_dat`, `Instantiate `milan_datapath` and add its RTL sources — the single place the` to the rest of the system?**
  _192 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `milan_soc.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0928030303030303 - nodes in this community are weakly interconnected._
- **Should `PART A — Fully-FPGA RISC-V Linux platform` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `Milan v1.2 endpoint — Functional & Non-Functional Requirements (FR/NFR)` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._