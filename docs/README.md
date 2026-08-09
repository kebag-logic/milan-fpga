# Documentation index

Documentation for the Milan TSN FPGA network interface (and its evolution
toward a 4-port AVB switch). The tree is organized by purpose - every
directory below is a bucket with one job. Unsure what a term means? →
[GLOSSARY.md](GLOSSARY.md).

```
docs/
├─ overview/      what the system is (start here)
├─ integration/   make it work in YOUR SoC / on YOUR board (incl. non-Vivado)
├─ litex/         the LiteX softcore host in depth
├─ fpga/          the gateware: every module, DMA/BD design docs, telemetry
├─ design/        protocol subsystem design records (MAAP, talker SM)
├─ testing/       every verification layer + how to run it
├─ traceability/  spec clause ↔ module ↔ test matrices (per standard + generated)
├─ reference/     contracts: register ABI, FR/NFR, Milan v1.2 matrix
├─ limitations/   known issues, limitations, hazards, troubleshooting
├─ findings/      dated bug post-mortems + perf-campaign logs (indexed)
├─ templates/     per-module doc templates (parameters, tests)
└─ diagrams/      generated system diagrams (edit .gen.py/.drawio, never renders)
```

> Superseded and completed-plan docs are moved out of this tree into
> [`../historical_now_obsolete/`](../historical_now_obsolete/README.md) — indexed there.

## ⭐ New here? Start with the guide, then pick your lane

**Two shortcuts before the long form.** If you want to *know what this is* in one page —
block diagram, the standards, the register map, what's proven and what isn't — read
[overview/AT_A_GLANCE.md](overview/AT_A_GLANCE.md). If you want to *run something green in
30 minutes* with no FPGA and no bench access, follow [`../QUICKSTART.md`](../QUICKSTART.md).

**Then everyone starts here → [SYSTEMS_ENGINEER_GUIDE.md](SYSTEMS_ENGINEER_GUIDE.md)** — what
the system is, plus a journey-ordered map of the whole doc set. Then follow the lane below that
matches what you're here to do. Unsure of a term? → [GLOSSARY.md](GLOSSARY.md).

![Where do I start — the reading lanes by role](DOC_MAP.png)

> The picture above is generated (editable [DOC_MAP.drawio](DOC_MAP.drawio); regenerate with
> `python3 docs/DOC_MAP.gen.py docs/DOC_MAP && rsvg-convert -w 2400 docs/DOC_MAP.svg -o docs/DOC_MAP.png`).

### 👩‍💻 Developer — *you write RTL / gateware / firmware*
Goal: add or change a module in the fabric.
1. [SYSTEMS_ENGINEER_GUIDE.md](SYSTEMS_ENGINEER_GUIDE.md) — orient.
2. [overview/ARCHITECTURE.md](overview/ARCHITECTURE.md) — the developer guide; **§8 "where to change things"**.
3. [ARCHITECTURE_HW_SW_SPLIT.md](ARCHITECTURE_HW_SW_SPLIT.md) — fabric vs softcore (decide where your feature belongs).
4. [fpga/FPGA_DESIGN.md](fpga/FPGA_DESIGN.md) — the `hdl/` module map + which TB verifies each (`ls hdl/` is authoritative).
5. [reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) — the CSR/AXI-Lite ABI shared by RTL ⇄ driver ⇄ DT.
6. [testing/TESTING.md](testing/TESTING.md) + [../tb/verilator/README.md](../tb/verilator/README.md) — a DUT change ships its harness in the same commit.

### 🧭 System Engineer — *you reason about the whole system*
Goal: understand it + assess compliance & roadmap.
1. [SYSTEMS_ENGINEER_GUIDE.md](SYSTEMS_ENGINEER_GUIDE.md) — the single best starting doc.
2. [ARCHITECTURE_HW_SW_SPLIT.md](ARCHITECTURE_HW_SW_SPLIT.md) — **normative** plan of record: fabric vs softcore (wins where overview docs conflict).
3. [overview/SYSTEM_DOMAIN_MAP.md](overview/SYSTEM_DOMAIN_MAP.md) — every module by domain/language, one picture.
4. [SPEC_TRACEABILITY.md](SPEC_TRACEABILITY.md) — IEEE/Milan clause → module → test, with status (204 rows).
5. [MILAN_COMPLIANCE_GAPS.md](MILAN_COMPLIANCE_GAPS.md) — what is + isn't compliant, honest gaps.
6. **GitHub Issues** — the current roadmap + open gaps are tracked as issues (not FULL_FPGA_SOLUTION §9).

### 🔧 Integrator — *you make it RUN on hardware*
Goal: build → flash → bring up the board. → **[the pipeline at a glance](BUILD_FLASH_BOOT.png)**.
1. [../sw/README.md](../sw/README.md) — toolchain (riscv64-elf, jdk+sbt, the LiteX venv) + `git submodule update --init third_party/verilog-axis`.
2. [integration/BUILDING.md](integration/BUILDING.md) — `build.sh` configs, the 3×32-thread discipline, WNS gate.
3. [litex/LITEX_SOC.md](litex/LITEX_SOC.md) §4 — the mandatory, non-obvious flags (`--coherent-dma`, `--gtx-tx-invert`, `--with-spiflash --flashboot full`) and why.
4. [integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) — flash layout, `COMPRESS`, **flash a matched image set** (a gateware-only load won't boot).
5. [findings/BENCH_TOPOLOGY.md](findings/BENCH_TOPOLOGY.md) — reach the boards, power, taps, recovery (power-controller `powerstrip off/on <outlet>`; outlet numbers are bench-specific).
6. [limitations/TROUBLESHOOTING.md](limitations/TROUBLESHOOTING.md) — when boot / flash / link goes wrong.

### 🧪 Tester / Validator — *you run the suites + validate*
Goal: prove it works, per spec.
1. [testing/TESTING.md](testing/TESTING.md) — the test taxonomy (Verilator TB · behave · bench).
2. [../tb/verilator/README.md](../tb/verilator/README.md) — run every Verilator TB; `ls tb/verilator/` is the authoritative suite list (the listing wins over any prose count).
3. [../tests/README.md](../tests/README.md) — run the **BDD conformance suite**: `cd tests && behave -f plain` (45 features / 594 scenarios measured 2026-08-06 — the run's own tally is authoritative, prose counts go stale; offline, ~4 s; the `@tsn_gen` tier additionally needs `TSAGEN_DIR` and skips cleanly without it). It is a CI gate and a USER standing order on every verification round.
4. [testing/BEHAVE_TEST_PLAN.md](testing/BEHAVE_TEST_PLAN.md) — the tag taxonomy, tiers, the `@bench` tier (the *bench* suites, which need real hardware, live in the sibling private test repo).
5. [`../harness/README.md`](../harness/README.md) — the **unattended campaign harness**: one entry point, eight phases, days-long runs, `STATUS`/heartbeat/resume, and the 3am operator page. Its item registry lives in the private test repo; the machinery is here.
6. [SPEC_TRACEABILITY.md](SPEC_TRACEABILITY.md) — read the pass/partial/fail matrix (✅ verified · 🟡 partial · ❌ missing · ➖ N/A).
7. [MILAN_COMPLIANCE_GAPS.md](MILAN_COMPLIANCE_GAPS.md) — what is validated vs pending.

### 📦 Product evaluator — *you decide whether to build on this*
Goal: an honest picture of what provably works and what is open.
1. [overview/FULL_FPGA_SOLUTION.md](overview/FULL_FPGA_SOLUTION.md) — what the system is.
2. [SPEC_TRACEABILITY.md](SPEC_TRACEABILITY.md) — clause-level verification status (204 rows).
3. [MILAN_COMPLIANCE_GAPS.md](MILAN_COMPLIANCE_GAPS.md) — what is still missing, and the attack order.
4. [limitations/KNOWN_ISSUES_AND_LIMITATIONS.md](limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) — what bites.
5. [limitations/RECURRING_DEFECT_PATTERNS.md](limitations/RECURRING_DEFECT_PATTERNS.md) — how the bugs that got through actually looked, and why the tests missed them.

### 🎧 Hobbyist — *you want it running on your desk (or you have no board at all)*
Goal: build, flash, hear audio — or get value out of the repo without buying anything.
1. [`../QUICKSTART.md`](../QUICKSTART.md) — the honest on-ramp: track 1 (simulate, no FPGA,
   no vendor tools), track 2 (yosys/ECP5 portability), track 3 (Vivado), track 4 (hardware).
   §4 lists exactly what works with **no board at all**.
2. [integration/BUILDING.md](integration/BUILDING.md) — build a bitstream for your board.
3. [integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) — flash it and boot Linux.
4. [limitations/TROUBLESHOOTING.md](limitations/TROUBLESHOOTING.md) — when it fights back.

## Quick task jumps

| If you want to… | read, in order |
|---|---|
| **Understand the system** (new contributor) | [overview/FULL_FPGA_SOLUTION](overview/FULL_FPGA_SOLUTION.md) → [overview/ARCHITECTURE](overview/ARCHITECTURE.md) → [ARCHITECTURE_HW_SW_SPLIT](ARCHITECTURE_HW_SW_SPLIT.md) (normative HW/SW plan-of-record) → [overview/SYSTEM_DOMAIN_MAP](overview/SYSTEM_DOMAIN_MAP.md) → [GLOSSARY](GLOSSARY.md) |
| **Integrate the datapath into your own SoC** | [integration/INTEGRATION_GUIDE](integration/INTEGRATION_GUIDE.md) → [reference/REGISTER_MAP](reference/REGISTER_MAP.md) → [fpga/FPGA_DESIGN](fpga/FPGA_DESIGN.md) |
| **Build it without Vivado / port to another board** | [integration/PORTING_GUIDE](integration/PORTING_GUIDE.md) → [integration/BOARD_PORTING_AX7101](integration/BOARD_PORTING_AX7101.md) (worked example) |
| **Build / boot / operate the AX7101 board** | [litex/LITEX_SOC](litex/LITEX_SOC.md) → [integration/QSPI_FLASHBOOT](integration/QSPI_FLASHBOOT.md) → [limitations/TROUBLESHOOTING](limitations/TROUBLESHOOTING.md) |
| **Run the tests** | [testing/TESTING.md](testing/TESTING.md) (the map) → [../tb/verilator/README.md](../tb/verilator/README.md) (suite detail) |
| **Know what does NOT work** | [limitations/KNOWN_ISSUES_AND_LIMITATIONS](limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) |
| **See where the project is heading** | [overview/AVB_SWITCH_DIRECTION](overview/AVB_SWITCH_DIRECTION.md) → the GitHub issues (the live roadmap) |
| **Know what the box records when it goes wrong** | [reference/TRACE_EVENTS](reference/TRACE_EVENTS.md) (the 23 logged event types, generated from the ABI) → [design/TRACE_LOGGING](design/TRACE_LOGGING.md) (why, budget, rotation, how to read one) |
| **Debug a datapath problem** | [fpga/pipeline-telemetry](fpga/pipeline-telemetry.md) → [findings/](findings/README.md) (how every past bug was cornered) → [testing/SIMULATION](testing/SIMULATION.md) |
| **Find LUTs / fit a bigger shape** | [design/AREA_BUDGET](design/AREA_BUDGET.md) — where the non-CPU LUTs are, which blocks are optional, and the DDR3/BRAM cascade |
| **Review RTL, or sanity-check a green test run** | [limitations/RECURRING_DEFECT_PATTERNS](limitations/RECURRING_DEFECT_PATTERNS.md) — the eight shapes this project's real bugs keep taking, each with the check that catches it |
| **Write driver / DT / register code** | [reference/REGISTER_MAP](reference/REGISTER_MAP.md) → [`../sw/driver/README.md`](../sw/driver/README.md) + [`../sw/dts/README.md`](../sw/dts/README.md) |

## 1 - overview/ (what the system is)

| Document | Purpose |
|----------|---------|
| [AT_A_GLANCE.md](overview/AT_A_GLANCE.md) | **The whole system on one page** - block diagram, the five standards it implements, the register map at a glance, what is proven by a re-runnable test vs by a bench measurement, and an honest "is this for you?". For someone deciding whether to use it at all. |
| [FULL_FPGA_SOLUTION.md](overview/FULL_FPGA_SOLUTION.md) | **The master guide to the fully-FPGA solution** - high/medium-level architecture, the three datapath boundaries, build/run, roadmap. **Read first.** |
| [ARCHITECTURE.md](overview/ARCHITECTURE.md) | System map: datapath, control plane, clock domains, HDL↔software mapping, where to change things - fully-FPGA primary, Zynq legacy appendix. |
| [RELEASE_0x0013.md](overview/RELEASE_0x0013.md) | **What changed from gateware `0x000B` to `0x0013`, and what you must do about it** — organised by consequence, not by feature: the fixed listener blocker, the breaking six-queue ABI change, control classification by DMAC, RMON's revival + `STATS_CAP`, what landed but is not yet reachable from software, and an upgrade checklist. Read this if you have a board on an older build. |
| [ARCHITECTURE_HW_SW_SPLIT.md](ARCHITECTURE_HW_SW_SPLIT.md) | **Normative HW/SW plan-of-record (rev 2)**: what runs in fabric vs the softcore (lwSRP/AAF/MAAP/ADP/AECP/ACMP all in fabric, silicon-validated; the softcore does linuxptp + PCM ring + provisioning). |
| [architecture/CPU_FPGA_SPLIT.md](architecture/CPU_FPGA_SPLIT.md) | **The CPU and the FPGA — one die, two machines, one contract**: the division of labor enforced by a single 100 MHz hart (per-frame → fabric, per-boot/per-policy → CPU), the two machines, and the three contracts between them. Companion narrative to the normative split above. |
| [SYSTEM_DOMAIN_MAP.md](overview/SYSTEM_DOMAIN_MAP.md) | Which module lives in which domain/language (userspace → kernel → firmware → LiteX → RTL → vendored IP → silicon). Diagram: [SYSTEM_DOMAIN_MAP.svg](SYSTEM_DOMAIN_MAP.svg). |
| [AVB_SWITCH_DIRECTION.md](overview/AVB_SWITCH_DIRECTION.md) | The direction: endpoint → 4-port AVB switch (decision matrix + scoreboard). Diagram: [AVB_SWITCH_DIRECTION.svg](AVB_SWITCH_DIRECTION.svg). |
| [GLOSSARY.md](GLOSSARY.md) | Every term of art in one place. |

## 2 - integration/ (your SoC, your board, your toolchain)

**The build → flash → boot → verify pipeline in one picture** (the flow otherwise spread
across BUILDING / LITEX_SOC / QSPI_FLASHBOOT / BENCH_TOPOLOGY). Editable
[BUILD_FLASH_BOOT.drawio](BUILD_FLASH_BOOT.drawio).

![AX7101 build → flash → boot → verify pipeline](BUILD_FLASH_BOOT.png)


| Document | Purpose |
|----------|---------|
| [INTEGRATION_GUIDE.md](integration/INTEGRATION_GUIDE.md) | **The `milan_datapath` boundary as a contract**: port-by-port tables, minimum-viable attach (M-A2), source list, software contract. |
| [PORTING_GUIDE.md](integration/PORTING_GUIDE.md) | **Vendor-neutral porting**: building without Vivado / off-Xilinx - what is portable (audited), per-vendor translation tables, constraint rules, the Yosys/ECP5 proof, two porting routes. |
| [BOARD_PORTING_AX7101.md](integration/BOARD_PORTING_AX7101.md) | The worked board port: pin extraction, DDR3/LiteDRAM, verification. |
| [BUILDING.md](integration/BUILDING.md) | **Building + flashing bitstreams in the two-board lab** (`build.sh`): named configs (ax7101/arty), parallel launch discipline, the `flash` subcommand per-board QSPI policy interlocks, gates. |
| [QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | Boot Linux from QSPI flash (zero-upload achieved 2026-07-06); flash layout + `deploy.sh flash-images`. |
| [AXIS_CORES_ON_NAXRISCV.md](integration/AXIS_CORES_ON_NAXRISCV.md) | The general pattern: attaching AXI-Stream cores to a LiteX softcore (control/data/event planes). |
| [PIPEWIRE_AVB_PEER.md](integration/PIPEWIRE_AVB_PEER.md) | **Using a PipeWire host as the AVB peer**: the gPTP→core→daemon stack in order, the working-log signals, binding the pilot tone to a stream, and the verified fault dictionary. |
| [`../historical_now_obsolete/`](../historical_now_obsolete/README.md) | The completed migration + de-Xilinx plans (historical); the living porting successor is PORTING_GUIDE above. |
| [`../THIRD_PARTY.md`](../THIRD_PARTY.md) | Vendored third-party code, pins and licenses. |

## 3 - litex/ (the softcore host)

| Document | Purpose |
|----------|---------|
| [LITEX_SOC.md](litex/LITEX_SOC.md) | **[`sw/litex/`](../sw/litex) in depth**: `milan_soc.py` anatomy (CRG, datapath attach, ring-DMA, MAC, flash-boot), the VexiiRiscv/NaxRiscv choice, the mandatory flags, patches, version pins, sims and tools. |

Plus the in-tree quickrefs: [`../sw/README.md`](../sw/README.md) (build/boot
walkthrough), [`../sw/litex/patches/README.md`](../sw/litex/patches/README.md),
[`../sw/dts/README.md`](../sw/dts/README.md), [`../sw/driver/README.md`](../sw/driver/README.md).

## 4 - fpga/ (the gateware)

| Document | Purpose |
|----------|---------|
| [FPGA_DESIGN.md](fpga/FPGA_DESIGN.md) | **Every module in `hdl/`**: purpose, interfaces, clock domain, verifying harness, doc link; the wrappers; the full CDC inventory. |
| [DATAPLANE_WALKTHROUGH.md](fpga/DATAPLANE_WALKTHROUGH.md) | **One AAF frame, hop by hop, in each direction** — the RTL instance and the CSR to read at every stage (classifier → queue → CBS → MAC on egress; MAC → parser → stream table → monitor → depacketizer → ring on ingress), plus the ordered "nothing arrives" fault-finding walk. The best first page for a newcomer to the media plane. |
| [PIPELINE_STAGES.md](fpga/PIPELINE_STAGES.md) | Canonical stage-by-stage pipeline prose (the DMA/BD host engines as running on silicon — the throughput story; the media plane is the walkthrough above). |
| [pipeline-telemetry.md](fpga/pipeline-telemetry.md) | The `milan_tlm` in-fabric observability block: per-stage counters, Little's-law occupancy, sysfs/BIOS access. |
| [HEADER_SPLIT_DESIGN.md](fpga/HEADER_SPLIT_DESIGN.md) | Header-split zero-copy RX design + per-page cut-through delivery. |
| [`../historical_now_obsolete/`](../historical_now_obsolete/README.md) | The DMA design-era logs (CPPI byte-ring→BD-ring, HW-GRO/RSC) — historical; PIPELINE_STAGES is the living reference. |
| [LSU_NONBLOCKING_DCACHE.md](fpga/LSU_NONBLOCKING_DCACHE.md) | VexiiRiscv non-blocking D$ / refill mechanics reference. |
| Per-module TerosHDL pages | `hdl/**/doc/*.md`, linked from [FPGA_DESIGN.md](fpga/FPGA_DESIGN.md) §2; regenerate with the TerosHDL documenter (`//!` comments are the source). |

## 5 - testing/

| Document | Purpose |
|----------|---------|
| [TESTING.md](testing/TESTING.md) | **The map of all six verification layers** + exact commands + known gaps. Start here. |
| [methodology.md](testing/methodology.md) | **Normative for every work lane**: test levels, oracle rules, the honesty rules (RECOMMENDED ≠ SHALL, empty capture ≠ PASS, unreadable CSR = SKIP). |
| [RUNNING_TESTS.md](testing/RUNNING_TESTS.md) | The all-layers walkthrough (elaboration smoke test → Migen sims → harnesses → board). |
| [SIMULATION.md](testing/SIMULATION.md) | The three simulation layers in detail (RTL harnesses, softcore boot, softcore+NIC M-A2). |
| [PROTOCOL_VALIDATION_MATRIX.md](testing/PROTOCOL_VALIDATION_MATRIX.md) | Every protocol × where implemented × the test that validates it. |
| [TORTURE_CAMPAIGN.md](testing/TORTURE_CAMPAIGN.md) | **The standing torture / compliance campaign**: one entry point ([`tb/tools/torture_campaign.py`](../tb/tools/torture_campaign.py)), every stream combination, payload/counter/licence graders. Triage records: [CAMPAIGN_RV32F_TRIAGE.md](testing/CAMPAIGN_RV32F_TRIAGE.md) · [CAMPAIGN_RV32G_TRIAGE.md](testing/CAMPAIGN_RV32G_TRIAGE.md). |
| [MILAN_COMPLIANCE_MATRIX.md](testing/MILAN_COMPLIANCE_MATRIX.md) | The clause-by-clause work list of the compliance-extension round (counters + notifications first); pairs with [MILAN_COMPLIANCE_GAPS.md](MILAN_COMPLIANCE_GAPS.md). |
| **Virtual E2E (boardless) tier** | [VIRTUAL_E2E_HOWTO.md](testing/VIRTUAL_E2E_HOWTO.md) (the copy-paste operator guide) → [VIRTUAL_E2E_QEMU.md](testing/VIRTUAL_E2E_QEMU.md) (the executable roadmap T0–T6) → [VIRTUAL_E2E_TEST_PROCEDURE.md](testing/VIRTUAL_E2E_TEST_PROCEDURE.md) (what PASS/FAIL/BLOCKED mean + the recorded runs) → [TRUE_E2E_REQUIREMENTS.md](testing/TRUE_E2E_REQUIREMENTS.md) (stable requirement IDs) → [VIRTUAL_SWITCH_RESEARCH.md](testing/VIRTUAL_SWITCH_RESEARCH.md) (the AVB-aware virtual wire decision) → [VIRTUAL_E2E_PLAN.md](testing/VIRTUAL_E2E_PLAN.md) (the original proposal) · env inventory: [../tooling/virtual-e2e-env.md](tooling/virtual-e2e-env.md) · evidence: `testing/evidence/` |
| [PDU_GETTER_SETTER_VERIFICATION.md](testing/PDU_GETTER_SETTER_VERIFICATION.md) | Roadmap item 10 decomposed: one verification per AVDECC command, by PDU family and fixture class. |
| [PROTOCOL_SWEEP_PLAN.md](testing/PROTOCOL_SWEEP_PLAN.md) | Full protocol sweep plan: every mandatory command and state machine, verified per clause. |
| [`../harness/README.md`](../harness/README.md) | The **unattended campaign harness** ([`harness/run.sh`](../harness/run.sh)): eight phases, days-long runs, JSONL + `STATUS` + heartbeat + resume, safety rails, the 3am operator page, and an explicit proven-vs-inferred split. |
| [`../tb/verilator/README.md`](../tb/verilator/README.md) | The self-checking harnesses (one dir per suite; `ls tb/verilator/` is authoritative), suite by suite. |
| [`../syn/yosys/README.md`](../syn/yosys/README.md) | The device-portability check (the `run.sh` `tops` array is authoritative; generic + ECP5). |

## 6 - limitations/ (make the problems apparent)

| Document | Purpose |
|----------|---------|
| [KNOWN_ISSUES_AND_LIMITATIONS.md](limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) | **The single page of everything that does not work, is not built, or bites**: scope limits, reproducibility gaps, timing constraints, lethal gateware⇄driver pairings, refuted perf levers, where the real numbers live. |
| [TROUBLESHOOTING.md](limitations/TROUBLESHOOTING.md) | Field log of every bring-up problem: symptom → cause → fix (22 sections; the listing in the file is authoritative). |

## 7 - reference/ (contracts)

| Document | Purpose |
|----------|---------|
| [REGISTER_MAP.md](reference/REGISTER_MAP.md) | The AXI4-Lite CSR ABI (groups 0x000-0x900) + the ring-DMA CSR windows - the HDL/driver/DT contract, asserted by the `csr` harness. |
| [REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | The classification overlay for the register map: every CSR group judged **needed / optional / debug** for a PRODUCTION image, with the rationale per row. |
| [EGRESS_QUEUE_MAP.md](reference/EGRESS_QUEUE_MAP.md) | **The map of record for the five egress queues** (802.1Q order, higher index = higher priority): what lands on q4…q0 and how it is classified, why the sixth queue was dropped, the PCP→TC→queue tables, control classification by reserved DMAC, the CBS reset slopes, why gPTP sits *below* the shaped classes, the FQTSS measurements, and the two-queue RX ingress split. |
| [FR_NFR.md](reference/FR_NFR.md) | Functional / non-functional requirement register (FR-*/NFR-*). |
| [MILAN_V12_DEPENDENCY_MATRIX.md](reference/MILAN_V12_DEPENDENCY_MATRIX.md) | Milan v1.2 → FR/NFR dependency matrix with verification traceability. |
| [`../REQUIREMENTS.md`](../REQUIREMENTS.md) | Normative requirements + the 802.1 gap analysis (REQ-*; partly Zynq-era). |
| [`../TODO.md`](../TODO.md) | Phased, dependency-ordered task list with status. |
| [`design/AEM_AND_AECP.md`](design/AEM_AND_AECP.md) | AVDECC entity-model / AECP design record, reconciled to as-built 2026-07-25 (pairs with [`../avdecc/README.md`](../avdecc/README.md)). |

## 8 - findings/ (the engineering record)

**[findings/README.md](findings/README.md)** indexes every dated post-mortem
and campaign log - the CBS bugs, the TX saga, the ring-DMA rework, the RX
wedges, the latency investigation, the >500 Mbit/s campaign. The
per-lever measured ledger is [`../CHANGELOG.md`](../CHANGELOG.md)
(chart: [perf_campaign.svg](perf_campaign.svg)).

> Current performance numbers live in [`../CHANGELOG.md`](../CHANGELOG.md) and
> [findings/](README.md); numbers quoted anywhere else are dated snapshots (why:
> [limitations/KNOWN_ISSUES_AND_LIMITATIONS.md](limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) §6).

## 9 - traceability/ (spec clause ↔ module ↔ test)

| Document | Purpose |
|----------|---------|
| [SPEC_TRACEABILITY.md](SPEC_TRACEABILITY.md) | **The traceability hub**: the 204-row coverage table across the five standards families, the N/A taxonomy, the attack order. |
| [traceability/ieee1722_1-2021.md](traceability/ieee1722_1-2021.md) · [ieee1722-2016.md](traceability/ieee1722-2016.md) · [ieee8021as.md](traceability/ieee8021as.md) · [ieee8021q.md](traceability/ieee8021q.md) · [milan-v12.md](traceability/milan-v12.md) | Per-standard clause → behavior → module → test tables, each row with a "why it matters". |
| [traceability/MODULE_MATRIX.md](traceability/MODULE_MATRIX.md) | **GENERATED** module ↔ spec ↔ test roll-up (the generator prints the live total — 82 modules on 2026-07-26); regenerate with [gen_module_matrix.py](traceability/gen_module_matrix.py) (`--check` gates drift). |
| [MILAN_COMPLIANCE_GAPS.md](MILAN_COMPLIANCE_GAPS.md) | The live "what's still missing + attack order" narrative. |

## 10 - design records, top-level specs, templates, diagrams

| Where | Purpose |
|----------|---------|
| [design/TIME_SYNC.md](design/TIME_SYNC.md) · [design/AUDIO_STREAMING.md](design/AUDIO_STREAMING.md) · [design/AEM_AND_AECP.md](design/AEM_AND_AECP.md) · [design/MAAP_FABRIC.md](design/MAAP_FABRIC.md) · [design/MILAN_TALKER_SM.md](design/MILAN_TALKER_SM.md) | Protocol subsystem design records: the time-sync deep-dive (gPTP → PHC → media clock, servo, every time CSR), the end-to-end audio path (talker/listener chains + latency taps), the AEM/AECP entity-model record (as-built), the fabric MAAP engine, the Milan talker connection SM. |
| [design/SAVED_STATE_FASTCONNECT.md](design/SAVED_STATE_FASTCONNECT.md) | **Saved-state fast-connect — the persistence journal** (Milan v1.2 §5.5.3.5): the `KLJ1` record format, the QSPI slot map, the torn-write contract, boot replay, and the CSR ingest ABI. The implementation ledger is [`../TODO.md`](../TODO.md) Phase 10. |
| [design/AREA_BUDGET.md](design/AREA_BUDGET.md) · [design/AREA_80_CAMPAIGN.md](design/AREA_80_CAMPAIGN.md) | Where the non-CPU LUTs are, which blocks are optional, the DDR3/BRAM cascade — and the 80% campaign: what may go static, by clause, if the reference builds still fail placement. |
| [design/PRESENTATION_TIME_WRAP.md](design/PRESENTATION_TIME_WRAP.md) | **Why a far-off talker clock alternates EARLY/LATE instead of biasing.** `avtp_timestamp` is 32 unsigned bits of absolute time, so the listener's comparison is modular with a half-range split at 2³¹; past one 4.294967296 s lap the result carries no direction and no magnitude, and drift walks it round the ring. Three generated figures, and the 214.66 s-vs-90.62 s half-period discrepancy left open rather than reconciled. Settles where `TIMESTAMP_UNCERTAIN` must be driven from. |
| [NXN_ARCHITECTURE.md](NXN_ARCHITECTURE.md) · [LWSRP_FPGA_ARCHITECTURE.md](LWSRP_FPGA_ARCHITECTURE.md) · [ENDSTATION_BUILDER.md](ENDSTATION_BUILDER.md) · [CHANNEL_MAP_64.md](CHANNEL_MAP_64.md) · [CHMAP64_AEM_BINDING.md](CHMAP64_AEM_BINDING.md) · [AAF_LATENCY_TAPS.md](AAF_LATENCY_TAPS.md) · [LATENCY_HISTORY_RING.md](LATENCY_HISTORY_RING.md) · [MVP_TALKER.md](MVP_TALKER.md) | Top-level subsystem specs: NxN stream scaling, the lwSRP engine, the end-station builder, the 64-channel map + its AEM binding, the per-stage latency taps + DDR3 history ring, the first AAF talker. |
| [templates/](templates/README-tests.template.md) | Per-module doc templates (parameters, tests) — their rows roll up 1:1 into the traceability matrix. |
| [diagrams/](diagrams/README.md) | Generated system diagrams (the giant single-page system map and friends). Every diagram ships as an editable `.drawio` + rendered `.svg`/`.png`; edit the source (`.gen.py` or the `.drawio`), never the render. |
| [DOC_GENERATION.md](DOC_GENERATION.md) | **How to generate the docs**: the matrix generator, the TerosHDL module pages, the diagram + chronogram pipelines, the gate/CI — commands + the you-changed-X-run-Y cheat sheet. |
| [`../historical_now_obsolete/DOC_AUDIT.md`](../historical_now_obsolete/DOC_AUDIT.md) | The 2026-07-23 doc audit + cleanup record — **archived 2026-07-27**, its own §2 move having been executed 2026-07-25. Kept for reference. |
| [HISTORY_PRE_SHORTEN_0731.md](HISTORY_PRE_SHORTEN_0731.md) | **Commit-message archive (2026-07-31)**: the full messages of `origin/main..main-push` preserved before the ≤10-word history rewrite. Reference record, not living documentation. |
| [SYSTEMS_ENGINEER_GUIDE.md](SYSTEMS_ENGINEER_GUIDE.md) | The journey-ordered front-door guide (also linked at the very top). |

## Conventions

* **RTL:** SystemVerilog, `` `default_nettype none ``, TerosHDL/Doxygen `//!`
  documentation comments on every generic, port and signal; named `always_*`
  processes with a preceding `//!` description.
* **Register maps:** offsets and reset values are defined once in the RTL and
  documented in [reference/REGISTER_MAP.md](reference/REGISTER_MAP.md); the CSR
  harness asserts they agree.
* **Verification:** every DUT change ships with its harness update in the same
  commit.
* **Diagrams:** every `*.svg`/`*.png`/`*.drawio` in this directory is
  generated - edit the sibling `*.gen.py`, never the outputs. All generator
  commands in one page: [DOC_GENERATION.md](DOC_GENERATION.md).
* **Counts:** suite/top counts in prose go stale; the directory listing and
  `run.sh` are authoritative.
* Board-recipe skills for the sibling test rig live out-of-repo in the
  the private test repo repo (`fpga/skills/milan-fpga-nic/SKILL.md` there).
