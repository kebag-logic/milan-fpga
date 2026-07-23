# Systems Engineer's Guide to milan-fpga

**If you read one doc first, read this one.** It tells you what the system is and hands you an
annotated, journey-ordered map of the whole doc set: Overview → Architecture / HW-SW split →
Subsystem specs → Register map / ABI → Build & deploy → Test & verify → Compliance status →
Historical findings.

Status: current as of **2026-07-23**. Where a linked doc is mid-refresh, the current fact is
stated here so this guide is accurate *today*; the doc audit (`DOC_AUDIT.md`) tracks the fixes.

---

## 1. What this system is

**milan-fpga is a fully-FPGA AVB/TSN Milan end-station.** It is a RISC-V/LiteX softcore SoC with
a custom TSN network datapath in fabric, running Linux, that behaves as an AVnu **Milan v1.2**
audio end-station (talker + listener) on the wire.

- **The end-station**: a 1 Gb Ethernet NIC whose *data plane* (MAC, classifier, CBS shaper,
  PTP timestamp unit, AVTP/AAF/CRF streaming, ADP/AECP/ACMP control, MAAP, lightweight SRP) is
  implemented as SystemVerilog gateware, and whose *control/policy plane* (linuxptp, PipeWire
  AVB, provisioning, the kl-eth driver) runs on the softcore under Linux.
- **The dividing principle** (normative, `docs/ARCHITECTURE_HW_SW_SPLIT.md` rev 2):
  per-frame / line-rate / liveness work → **fabric**; negotiation / policy / provisioning →
  **softcore**. This is the plan of record; where older overview docs say "AVDECC/SRP is future
  software", they are superseded — ADP/AECP/ACMP/MAAP/lwSRP are in fabric and silicon-validated.
- **Standards implemented**: IEEE 1722-2016 (AVTP/AAF/CRF/MAAP), IEEE 1722.1-2021 (ATDECC:
  ADP/AECP/ACMP/AEM), IEEE 802.1AS-2020 (gPTP), IEEE 802.1Q-2022 (VLAN/PCP, CBS credit-based
  shaper, MSRP/MVRP), all under the **AVnu Milan v1.2** profile.
- **Direction**: a 1-NIC end-station today, evolving toward a 4-port AVB switch; the
  NaxRiscv→VexiiRiscv softcore migration that this direction drove is now as-built.

### The two boards (ship pair, both CERT 63/63)

| Board | SoC | Role |
|---|---|---|
| **ALINX AX7101** (xc7a100t) | VexiiRiscv **1-hart** + `--l2-bytes 32768`, DDR3-800 512 MB, GMII MAC @100 MHz datapath | Full end-station. QSPI self-boot. |
| **ARTY** (`asl_milanfinal53e`, VERSION 0x000A) | small VexiiRiscv end-station, MII | Small end-station; flash-boot full images. |

> **The single most important framing fact**: the ship CPU is **1-hart**. Much of the
> 2026-07 perf campaign (RX ~223-381 Mbit, TX 582-646 Mbit) was measured on a **2-hart +
> L2-64K** config that is now a **superseded perf-lineage variant**. Any doc presenting
> "dual-hart / 2-core / L2-64K" as the ship or published shape is stale — read those numbers as
> perf-campaign peaks, not shipped-SoC behaviour.

### Current top-line state (2026-07-23)

- Both boards **CERT 63/63**.
- Compliance matrix: **163 verified / 17 partial / 7 MISSING / 17 N-A** (204 rows).
- **Media-clock servo (MMCM-DRP) silicon-proven**: coherent-chain analog loop **-83.9 dB** =
  the CS4344+CS5343 converter power-sum floor. (A "-73.4 dB" loop figure anywhere is the stale
  pre-servo NCO-era number.)
- **ALSA**: record works on silicon (arecord byte-exact); playback (`KL_pcm_tx`) is a validated
  scaffold, not yet integrated.
- **PCM ring** can now target on-chip BRAM (`--pcm-ring bram`); DRAM ring remains default.
- **AX42** (e2 MAC-TX link-bounce wedge) fix landed this session (guard `eth_rst` now covers the
  PHY-side `eth_tx`/gtx path); sim + full-SoC elaboration validated, silicon bench pending.
- Toolchain: Vivado 2026.1 with **Artix-7 + Zynq installed** (`/home/alex/Xilinx*`); both boards
  build and run. (Docs saying "only Spartan-7 / `--build` blocked here" are stale.)
- 12-item USER roadmap: **items 1-4, 6, 8, 9 DONE**; 5 partial (8x8 pending), 7 partial
  (playback pending), 10 in progress (the behave suite), 11/12 pending.

---

## 2. The reading path (annotated doc map)

Each entry: the doc and **when to read it**. `→` marks the doc to start each stage with.

### Stage 0 — Orientation
- **`docs/SYSTEMS_ENGINEER_GUIDE.md`** (this doc) — start here.
- **`README.md`** (repo root) — one-paragraph description + quick jumps. *(Front door; being
  refreshed for the 1-hart / CERT-63 state.)*
- **`docs/README.md`** — the documentation nav hub: directory-purpose map + curated reading
  paths + per-doc one-liners. Read when you want a different slice than this guide's.
- **`docs/GLOSSARY.md`** — every term of art (AVB/TSN, PHY, LiteX/SoC, datapath/DMA, cache).
  The doc other docs defer to for definitions; keep it open in a tab.

### Stage 1 — Overview: WHAT the system is
- → **`docs/overview/FULL_FPGA_SOLUTION.md`** — the master "read first" overview: high/mid-level
  architecture, the three datapath boundaries (CSR / DMA / MAC), the CSR/DMA/IRQ ABI, build/run,
  status, roadmap. *(Note: its "AVDECC/SRP is future SW" and RGMII framing are stale — see the
  HW/SW split doc and "GMII not RGMII" below.)*
- **`docs/overview/ARCHITECTURE.md`** — the by-**flow** architecture map: datapath, control
  plane, clock domains, the HDL⇄driver/DT mapping table, and the "where to change things" matrix.
  Read when you need to locate a feature end-to-end. *(hdl/ tree in §1 predates the spec-aligned
  reorg; trust the live tree.)*
- **`docs/overview/SYSTEM_DOMAIN_MAP.md`** — the by-**domain**/by-language partition
  (userspace → kernel → firmware → SoC → RTL → vendored IP → silicon → host tooling). Read to
  answer "what language/where does layer X live". Accurate and stable.
- **`docs/overview/AVB_SWITCH_DIRECTION.md`** — WHY the project is going 4-port-switch and WHY
  VexiiRiscv is the core (that CPU decision is now as-built). Read for design rationale; ignore
  its embedded scoreboard (dated snapshot).

### Stage 2 — Architecture & the HW/SW split
- → **`docs/ARCHITECTURE_HW_SW_SPLIT.md`** — **normative** (USER rev 2). The plan-of-record
  dividing principle + per-function fabric-vs-softcore placement table + boundary contracts.
  **This wins where overview docs conflict** on what is HW vs SW. Read before deciding where any
  new function belongs.
- **`aem-and-aecp.md`** (currently at repo root; relocating to `docs/architecture/`) — the
  AEM+AECP subsystem design rationale: the 4-level block-memory descriptor scheme, the
  getter/setter accessor model, the AECP parse→respond→unsolicited pipeline. Read for AEM/AECP
  internals; cross-check dynamic behaviour against `traceability/ieee1722_1-2021.md §3` +
  `REGISTER_MAP` (some accessor rows have drifted).
- **`docs/integration/AXIS_CORES_ON_NAXRISCV.md`** — the clearest "how the CPU talks to fabric"
  mental model (control AXI-Lite/CSR, data AXIS↔DMA, events IRQ→PLIC). Read before wiring any
  new core. (Mechanics hold for the shipped VexiiRiscv too.)

### Stage 3 — Subsystem specs (by protocol)

**Datapath / DMA / performance**
- → **`docs/fpga/PIPELINE_STAGES.md`** — the flagship living, stage-by-stage prose reference for
  the whole NIC datapath (RX R1-R8, TX T1-T3): what each stage does, where its code lives, which
  knob changes what, BD/CQ/full-gate/cut-through mechanics. **Read this first for the datapath.**
- **`docs/fpga/FPGA_DESIGN.md`** — the hdl/ gateware module map: every SV module, its clock
  domain, its TB, its doc. Read to learn the RTL structure.
- **`docs/fpga/HEADER_SPLIT_DESIGN.md`** — the header-split zero-copy RX design + full silicon
  bring-up history (hsq4-hsq12); BD v2/v3 encodings are the **live driver ABI**. Read for the
  detailed history behind PIPELINE_STAGES' RX prose.
- **`docs/fpga/LSU_NONBLOCKING_DCACHE.md`** — the VexiiRiscv non-blocking L1 D-cache / 8 refill
  slots mechanism (why RX is cold-read bound; how MLP arises on an in-order core). Evergreen CPU
  reference; the mlp3 results table is perf-peak (2-hart), not ship.
- **`docs/fpga/pipeline-telemetry.md`** — the in-fabric observability block (`milan_tlm`):
  per-stage counters, Little's-law inflight, the kl-eth telemetry sysfs group. Read when you
  need "where did the frame go?".
- **`docs/findings/PERFORMANCE_GOAL.md`** — the perf-campaign record (>500 Mbit RX+TX north-star
  + the forced-march evidence log). *(Consolidation home for the RX/TX/headroom campaign narrative;
  numbers are perf-lineage on 2-hart.)*
- **`docs/findings/PERF_ON_MILAN.md`** — the durable **profiling method** (cross-built perf,
  timer sampling, offline System.map symbolization, cluster-reading). Clock/hart-agnostic; read
  before profiling this SoC.
- **`docs/findings/LATENCY_INVESTIGATION.md`** — the deep memory-latency root cause: 1424 ns/miss
  = 713 ns TLB-walk + 716 ns DRAM floor, the DDR3-800-vs-900 tradeoff, the reset false-path
  lesson. Timeless; read to understand the single-port ceiling.
- **`docs/findings/RX_PERF_TUNING_MAP.md`** (+ the `.drawio`) — the maintainer's how-to for the
  three-lane gateware/driver/kernel knob map. **Read the LETHAL pairing hazards** (`hs_pgsz` ==
  `--hs-page-bytes`; BD-256 needs the hsq6+ drain gate — mismatch DMA-overruns kernel memory)
  before touching any perf knob.

**gPTP (time)**
- → **`docs/findings/GPTP_RXPAD_ROOTCAUSE.md`** — the RX-pad root cause + the operative
  switch-behaviour matrix (the bench switch does per-port pdelay but never masters Sync/Announce
  into board ports → why es-1.1/1.2 BMCA variants are switch-gated). Read for why gPTP behaves
  as it does on this bench.
- **`docs/findings/PTP_TS_METADATA_FIX.md`** — the HW-timestamp DMA "Record contract v2.1"
  (beat0 ns / beat1 {seq,msgType,marker,dir}); this is the driver-matched ABI. Read when
  touching timestamping.

**SRP / lwSRP (reservation)**
- → **`docs/LWSRP_FPGA_ARCHITECTURE.md`** — the canonical single-stream lightweight-SRP engine
  spec + byte-exact MRPDU/MVRP wire contract + CSR group (0x680-0x6A0). Read for reservation.
- **`docs/NXN_ARCHITECTURE.md`** — how the shared-engine-per-function + N per-stream BRAM
  contexts scale lwSRP (and AAF/CRF) to NxN streams (roadmap item 5). Read for the scaling model.

**AVDECC / AECP / ACMP (control)**
- → **`docs/traceability/ieee1722_1-2021.md`** — per-clause ATDECC map (ADP/ACMP/AECP/AEM +
  commands); the authoritative "which clause is verified where" for the control plane.
- **`docs/design/MILAN_TALKER_SM.md`** — the shipped talker connection model (ACMP PROBE_TX SM,
  GET/SET_STREAM_INFO byte rules, stream_id = {mac,uid}). *(Its "out of scope" list is stale —
  lwSRP/MAAP/listener all landed.)*
- **`aem-and-aecp.md`** — AEM/AECP internals (see Stage 2).
- **`docs/findings/ADP_DORMANCY.md`** — the ADP-dormancy incident post-mortem: the self-re-arm
  fix, A_ADP_DIAG 0x668, and the "always pass MILAN_CLK_FREQ_HZ to the Instance()" trap. Read
  before touching ADP timing.

**AAF (audio streaming) + CRF / media-clock**
- → **`docs/traceability/ieee1722-2016.md`** — per-clause AVTP/AAF/CRF/MAAP map. *(CRF-8 still
  says the servo is "not built" — stale: the MMCM-DRP servo IS built and silicon-proven.)*
- **`docs/MVP_TALKER.md`** — the AAF-PCM talker: the 90-byte frame format, the CSR 0x654 group,
  silicon bring-up. *(Its headline "media clock not locked" caveat is superseded by the servo;
  the frame/CSR content is still live.)*
- **Media-clock servo** — silicon-proven MMCM-DRP servo (`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`,
  MCSRV_STAT/CTRL at 0x8F8/0x8FC), coherent chain, -83.9 dB. Documented in
  `MILAN_COMPLIANCE_GAPS.md` item 6 and the register map; the traceability rows are being updated.

**MAAP (address allocation)**
- → **`docs/design/MAAP_FABRIC.md`** — the fabric MAAP engine design + byte-exact PDU contract
  (from pipewire maap.c) + the 0x4B GET_DYNAMIC_INFO appendix. *(Reframe plan→as-built; the CSR
  sketch has drifted from REGISTER_MAP — trust REGISTER_MAP: 0x6D0 STAT0 / 0x6D4 STAT1.)*

**QoS / CBS shaper**
- → **`docs/traceability/ieee8021q.md`** — per-clause VLAN/PCP + MRP + MSRP/MVRP map (the QoS/CBS
  verification view).
- **`docs/findings/CBS_DEFAULT_SHAPING_BUG.md`** — the permanent finding that CBS shapes reserved
  SR classes only (CBS_EN_RST=0000); read to understand why plain TCP is not credit-paced.
- **`docs/findings/CBS_DATAPATH_BUG.md`** — the classifier/arbiter tdest-timing fix (distinct bug
  from the reset-default one); read for the CBS/classifier datapath internals.

**End-station composition**
- **`docs/ENDSTATION_BUILDER.md`** — the software-defined end-station builder (roadmap item 4):
  D1-D5 decisions + the 27-row config-schema→AEM-descriptor mapping (config → SoC argv / AEM
  overlay / DT). Read to understand how a declared end-station drives gateware + AEM + lwSRP.

### Stage 4 — Register map / ABI
- → **`docs/reference/REGISTER_MAP.md`** — **the CSR/ABI authority** shared by HDL (`milan_csr.sv`),
  the kl-eth driver, and the device tree: group-by-group offsets/access/reset/fields for
  0x000-0x8FC + the LiteX DMA/PCM-ring CSR space. Actively maintained (link-guard, servo, VERSION
  0x000A). Any driver/gateware/DT author joins on this doc.
- **`docs/integration/INTEGRATION_GUIDE.md`** — the port-by-port contract for wiring
  `hdl/milan/milan_datapath.sv` (AXI-Lite CSR, 3 DMA AXIS, MAC-facing AXIS, sideband, one IRQ)
  into any SoC. The single clean boundary of the whole project. Read to attach the datapath.
- **`docs/reference/FR_NFR.md`** — the functional/non-functional requirements bible (FR/NFR +
  RFC-2119 priorities + verification-method letters + the 12-step Milan procedure). The
  requirements contract; read to know WHAT is required.
- **`REQUIREMENTS.md`** (root) — the normative REQ-* spec + the 60-gap audit. *(Add the
  platform migration preamble: Zynq/RGMII/0x43C0 → full-FPGA/GMII/0x9000; REQ-* IDs unchanged.)*
- **`THIRD_PARTY.md`** (root) — vendored RTL provenance (submodule, license, pinned commit).
  Read before building or redistributing.

### Stage 5 — Build & deploy
- → **`docs/integration/BUILDING.md`** — the canonical two-board build flow via `sw/litex/build.sh`
  (named `cfg_ax7101`/`cfg_arty`, the 32-thread/3-build parallel discipline, how to add a config).
  *(Refresh cfg paragraphs to 1-hart+L2-32K / flashboot-full / strip-probes.)*
- **`docs/litex/LITEX_SOC.md`** — the in-depth `sw/litex/` + `milan_soc.py` anatomy (CRG,
  VexiiRiscv/NaxRiscv, DDR3, ring-DMA, LiteEth GMII MAC, QSPI flashboot, the mandatory flags).
  Read for the LiteX host internals. *(Refresh CPU/clock to 1-hart+L2-32K@100e6.)*
- **`docs/integration/QSPI_FLASHBOOT.md`** — how QSPI flash-boot works (bitstream@0 +
  Image.xz via the xz_embedded BIOS decoder, the 16 MB constraint, deploy.sh flash-images).
  Canonical flashboot reference.
- **`docs/integration/BOARD_PORTING_AX7101.md`** — the worked "how a new board gets ported"
  story (pin provenance, the RGMII→**GMII** strap correction, 512 MB DDR3). Read before a new board.
- **`docs/integration/PORTING_GUIDE.md`** — vendor-neutral porting (Intel/Lattice/Gowin/open-PnR):
  the 3 replaceable layers, the vendor-touching-attribute inventory, the Yosys/ECP5 proof.
- **`THIRD_PARTY.md`** — provenance (also Stage 4).

### Stage 6 — Test & verify
- → **`docs/testing/TESTING.md`** — the top-level verification map/index: every layer, what it
  proves, the exact command. *(Trust `ls tb/verilator/` for the harness list, not the hardcoded
  count — the tree has ~41 harness dirs, ~39 Yosys tops.)*
- **`docs/testing/RUNNING_TESTS.md`** — the layered how-to-run runbook (cheapest-first: smoke →
  migen sims → verilator → yosys → P&R → silicon) with time budgets and the traps that bit.
- **`docs/testing/SIMULATION.md`** — the conceptual explainer of the three sim layers + the M-A2
  "CPU reads MILN" evidence walk. Read to understand what each sim layer can/can't catch.
- **`docs/testing/PROTOCOL_VALIDATION_MATRIX.md`** — the protocol × module × test coverage view
  ("which harness proves protocol X"). *(Status glyphs are a pre-silicon snapshot — many rows are
  now CERT/silicon-done.)*
- **`docs/testing/BEHAVE_TEST_PLAN.md`** — the live plan (roadmap item 10) turning the 204-row
  traceability matrix into a tag-taxonomy'd behave suite. Dated today; the active compliance-test
  bridge. Read for the executable-compliance direction.
- **`docs/templates/README-parameters.template.md`** / **`README-tests.template.md`** — the
  per-leaf-module doc templates; the tests template's row format rolls up 1:1 into
  SPEC_TRACEABILITY. Use when documenting a new module.
- **`docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md`** — the honest page of open limitations,
  **lethal gateware⇄driver pairings, and refuted perf levers (measured, do-not-retry)**. Read to
  avoid known dead ends. *(cpu-count line + reconciled-date being refreshed.)*
- **`docs/limitations/TROUBLESHOOTING.md`** — the field log of every real problem hit
  (symptom→cause→fix) across toolchain / LiteX / Verilator / synth / P&R / on-hardware bring-up.
  Durable; the first place to look when something breaks.

### Stage 7 — Compliance status
- → **`docs/SPEC_TRACEABILITY.md`** — the traceability hub: the reconciled coverage table
  (204 rows = **163✅/17🟡/7❌/17➖**, reconciled today), the N/A taxonomy, the module→family map,
  the top-MISSING attack order. Start here to find which clause is verified where.
- **Per-standard family files** (under `docs/traceability/`):
  `ieee1722_1-2021.md` (ATDECC), `ieee1722-2016.md` (AVTP/AAF/CRF/MAAP),
  `ieee8021as.md` (gPTP), `ieee8021q.md` (802.1Q QoS+SRP), `milan-v12.md` (Milan overlay).
  Read the one for the protocol you're auditing.
- **`docs/reference/MILAN_V12_DEPENDENCY_MATRIX.md`** — the ⇄ companion of FR_NFR: WHY each Milan
  requirement forces each FR/NFR + the verification artifact per area. Read paired with FR_NFR.
- **`docs/MILAN_COMPLIANCE_GAPS.md`** — the live narrative "what's still missing/approximate" +
  the USER-ordered 12-item attack order. The best "what's left and why" orientation; read next
  to SPEC_TRACEABILITY.

### Stage 8 — Current ops + historical findings
- → **`docs/findings/HANDOVER_SMALL.md`** — **the current (07-23) live-state handover**: ship
  boards, what was proven this session, the 12-item roadmap status table, prioritized open items.
  Read to know the state right now.
- **`docs/findings/BENCH_TOPOLOGY.md`** — the "read this first" bench-ops reference: machines,
  consoles, repos, the build→flash→verify pipeline, pw0 wire tooling, CERT privacy rules, the CSR
  quick-map, standing rules. High value for operating the bench. *(Its §9 live-state has drifted;
  the infra content is stable.)*
- **`docs/findings/HANDOVER.md`** — the deep accumulated session-history log (109 KB). The
  irreplaceable campaign trail; **history, not current live state** (that's HANDOVER_SMALL).
- **`docs/findings/README.md`** — the findings-directory index (symptom→measurement→root-cause→
  fix→verification framing). *(Being extended to list the handovers + control-plane post-mortems.)*
- **Fixed-bug post-mortems** (all silicon-validated, evergreen teaching docs):
  `kl-eth-tx-debug.md` (the definitive TX bring-up saga + "never trust dst-MAC-keyed counters as
  TX proof"), `CBS_DATAPATH_BUG.md`, `CBS_DEFAULT_SHAPING_BUG.md`, `ADP_DORMANCY.md`,
  `GPTP_RXPAD_ROOTCAUSE.md`, `PTP_TS_METADATA_FIX.md`.
- **`CHANGELOG.md`** (root) — the per-lever measured ledger (lever → build → before→after Mbit/s)
  + the refuted-levers list. The single canonical lever→effect table for the perf campaign.
- **`TODO.md`** (root) — the original Phase 0-9 NIC bring-up plan; largely done/superseded by the
  12-item roadmap, but still the open-REQ checkbox ledger.
- **`docs/archive/README.md`** — the index of the 15 **superseded / historical** docs (the
  byte-ring/CPPI/RSC DMA-origin docs, the completed migration & de-Xilinx plans, the 07-11
  SESSION_HANDOFF, the early perf snapshots). Each is marked in place with a `⚠️ SUPERSEDED`
  banner + its living successor (they stay at their paths to preserve inbound links). Read
  only for deep history.

---

## 3. Fast lookups ("I need to…")

| I need to… | Go to |
|---|---|
| Understand the whole system in 20 min | this guide §1 → `overview/FULL_FPGA_SOLUTION.md` |
| Decide if a function goes in HW or SW | `docs/ARCHITECTURE_HW_SW_SPLIT.md` (normative) |
| Find a CSR offset / add a register | `docs/reference/REGISTER_MAP.md` |
| Attach the datapath to a SoC | `docs/integration/INTEGRATION_GUIDE.md` |
| Understand the RX/TX datapath | `docs/fpga/PIPELINE_STAGES.md` |
| Build a bitstream for a board | `docs/integration/BUILDING.md` |
| Port to a new board / non-Xilinx | `BOARD_PORTING_AX7101.md` / `PORTING_GUIDE.md` |
| Run the tests | `docs/testing/RUNNING_TESTS.md` |
| Check what's compliant | `docs/SPEC_TRACEABILITY.md` |
| Know today's live state | `docs/findings/HANDOVER_SMALL.md` |
| Avoid a known dead end / lethal pairing | `docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md` |
| Debug a bring-up failure | `docs/limitations/TROUBLESHOOTING.md` |
| Look up a term | `docs/GLOSSARY.md` |

---

## 4. Watch-outs when reading older docs (2026-07-23 reconciliation)

Several docs predate recent changes. When you hit these phrasings, substitute the current fact:

- "dual-hart / 2-core / L2-64K" as ship config → **ship is 1-hart + L2-32K**; 2-hart numbers are
  perf-campaign peaks.
- "-73.4 dB" as the analog loop record → **-83.9 dB** (servo silicon-proven).
- "162 verified / 18 partial" → **163 / 17** (204-row matrix, reconciled today).
- "17 Verilator harnesses" / "18 Yosys tops" → **~41 harness dirs / ~39 tops** (the directory
  listing is authoritative).
- "RGMII" for the board MAC → **GMII** (the AX7101 strap correction).
- CSR base "0x43C0_0000" (Zynq PS) → **0x9000_0000** (softcore IO region).
- "only Spartan-7 installed / `--build` blocked" → **Vivado 2026.1 has Artix-7 + Zynq**; both
  boards build and run.
- "AVDECC / SRP is future software" → **ADP/AECP/ACMP/MAAP/lwSRP are in fabric, silicon-validated**
  (per `ARCHITECTURE_HW_SW_SPLIT.md` rev 2).
- The media-clock servo described as a "future MMCM-DRP servo" / "actuator not built" → **built
  and silicon-proven**.

The full list of which doc says what and the planned fixes lives in
[`docs/DOC_AUDIT.md`](DOC_AUDIT.md).
