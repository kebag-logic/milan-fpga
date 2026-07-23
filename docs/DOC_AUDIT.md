# Documentation Audit & Restructure Plan

Date: 2026-07-23
Scope: full 79-doc corpus (the milan-fpga repo, all `*.md`).
Nature: **planning + drafting only** — no existing doc is edited, moved, or deleted by this
audit. It records the cleanup decisions and the proposed target structure so the moves can be
executed in a later pass. USER rule: OBSOLETE docs are **archived** (moved to `docs/archive/`
with a forward pointer), never deleted — history is preserved.

Companion deliverable: [`SYSTEMS_ENGINEER_GUIDE.md`](SYSTEMS_ENGINEER_GUIDE.md) — the new
top-level, journey-ordered reading guide a fresh systems engineer should be handed first.

---

## 0. Ground-truth system state used to detect STALE content (2026-07-23)

- Compliance matrix reconciled TODAY to **163 verified / 17 partial / 7 MISSING / 17 N-A**
  (204 rows). Any doc saying "162 verified / 18 partial" is STALE.
- **Servo (MMCM-DRP media-clock) is SILICON-PROVEN**: analog loop **-83.9 dB** = CS4344+CS5343
  converter power-sum floor. Any doc citing "-73.4 dB" as the *loop* figure is the STALE
  pre-servo NCO-era number.
- **Ship CPU shape = VexiiRiscv 1-hart + `--l2-bytes 32768`** on xc7a100t (AX7101). The
  2-hart / L2-64K SMP variant is a **superseded perf-lineage** config. Any doc presenting
  "dual-hart / 2-core / L2-64K" as the ship/published config is STALE.
- **Both boards CERT 63/63.** Ship pair: ARTY `asl_milanfinal53e` (VERSION 0x000A) +
  ALINX `AX39`. Arty is a small MII endstation.
- **AX42** (e2 MAC-TX link-bounce wedge) fix LANDED this session (guard `eth_rst` now covers
  the PHY-side `eth_tx`/gtx path); sim + full-SoC elaboration validated, silicon bench pending.
- **PCM ring can target on-chip BRAM** (`--pcm-ring bram`); DRAM ring is still the default.
- **ALSA**: record works on silicon (arecord byte-exact); playback (`KL_pcm_tx`) is a validated
  scaffold, not integrated.
- **Vivado 2026.1 (Artix-7 + Zynq) IS installed** at `/home/alex/Xilinx*`. Any doc saying "only
  Spartan-7 installed / `--build` blocked here" is STALE.
- **Harness/top counts drifted repo-wide**: `tb/verilator/` now has ~41 harness dirs (not 17);
  `syn/yosys/run.sh` now drives ~39 tops (not 18). Prefer "the directory listing is
  authoritative" over any hardcoded count.
- 12-item USER roadmap: items 1-4, 6, 8, 9 DONE; 5 partial (8x8 pending), 7 partial (playback
  pending), 10 in progress (`docs/testing/BEHAVE_TEST_PLAN.md`), 11/12 pending.

---

## 1. Full audit table (every doc: status, action, rationale)

Status = content freshness (CURRENT / STALE / OBSOLETE / DUPLICATE).
Action = KEEP / UPDATE / MERGE / ARCHIVE.

| Path | Status | Action | One-line rationale |
|---|---|---|---|
| `README.md` | STALE | UPDATE | Repo front door; fix dual-hart→1-hart, drop 2-core >500 headline, refresh counts, surface CERT 63/63 + servo. |
| `docs/README.md` | STALE | UPDATE | Doc nav hub; sound, but add ARCHITECTURE_HW_SW_SPLIT to reading paths; fix harness count. |
| `docs/SYSTEMS_ENGINEER_GUIDE.md` | NEW | CREATE | New journey-ordered entry point (this audit's companion). |
| `docs/GLOSSARY.md` | CURRENT | KEEP | Accurate, already uses post-reorg paths + VexiiRiscv-current framing. Definitions authority. |
| `REQUIREMENTS.md` | STALE | UPDATE | REQ-* spec still normative; add Zynq→full-FPGA / RGMII→GMII / 0x43C0→0x9000 migration preamble. |
| `TODO.md` | STALE | UPDATE | Phase 0-9 plan largely done/superseded; keep open-REQ ledger, point to 12-item roadmap + BEHAVE plan. |
| `CHANGELOG.md` | STALE | UPDATE | Canonical perf lever→effect ledger; add 07-10/11 header-split closing rows + "perf-lineage, ship=1-hart" banner. |
| `THIRD_PARTY.md` | STALE | UPDATE | Add `external` (fpga-avb-ethernet) submodule row; move verilog-ethernet Planned→Vendored. |
| `aem-and-aecp.md` | STALE | UPDATE + RELOCATE | AEM/AECP design rationale; relocate root→`docs/architecture/`; reconcile to as-built (small↔full entity, static AUDIO_MAP, NOT_IMPLEMENTED cmds). |
| `docs/overview/FULL_FPGA_SOLUTION.md` | STALE | UPDATE | Master "read first" overview; fix CPU config, RGMII→GMII contradiction, AVDECC-in-fabric status, counts. |
| `docs/overview/ARCHITECTURE.md` | STALE | UPDATE | By-flow arch map; fix hdl/ tree (spec-aligned reorg), 1-hart, harness/top counts. Near-dup pair w/ FULL_FPGA_SOLUTION. |
| `docs/overview/SYSTEM_DOMAIN_MAP.md` | CURRENT | KEEP | By-domain/by-language partition; accurate, ideal "where does X live". |
| `docs/overview/AVB_SWITCH_DIRECTION.md` | STALE | UPDATE | WHY 4-port-switch + WHY VexiiRiscv (validated as-built); demote embedded scoreboard to pointer. |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md` | STALE | UPDATE | **Normative** HW/SW plan-of-record (rev 2); refresh shipped rows (lwSRP/AAF/MAAP/servo); index it in docs/README. |
| `docs/fpga/PIPELINE_STAGES.md` | STALE | UPDATE | Flagship living datapath prose; add "records are 2-hart perf-peak, ship=1-hart" note. |
| `docs/fpga/FPGA_DESIGN.md` | STALE | UPDATE | Top-level gateware module map; fix axis_clk 50→100 MHz; repoint sec4 links on archive/merge. |
| `docs/fpga/HEADER_SPLIT_DESIGN.md` | CURRENT | KEEP | Designated header-split silicon history; live BD v2/v3 driver ABI. **Merge target for HSPLIT14.** |
| `docs/fpga/HSPLIT14_DESIGN.md` | OBSOLETE | MERGE→HEADER_SPLIT_DESIGN | hsq12 cut-through continuation of same story; fold in as the cut-through chapter. |
| `docs/fpga/LSU_NONBLOCKING_DCACHE.md` | STALE | UPDATE | Evergreen CPU/cache mechanism ref; add one-line ship-shape reconciling note (mlp3 = perf-peak not ship). |
| `docs/fpga/pipeline-telemetry.md` | CURRENT | KEEP | Version-independent observability (milan_tlm) reference. |
| `docs/fpga/CPPI_DMA_REDESIGN.md` | OBSOLETE | ARCHIVE | DESIGN-ERA byte-ring→BD-ring log; running system moved past it (PIPELINE_STAGES). Keep lview.sh method via pointer. |
| `docs/fpga/HW_GRO_RSC.md` | OBSOLETE | ARCHIVE | Single-slot RSC + 07-07 TX≥200 campaign log; ABI survives in HEADER_SPLIT_DESIGN/PIPELINE_STAGES. |
| `docs/reference/REGISTER_MAP.md` | CURRENT | KEEP | The CSR/ABI authority (HDL⇄driver⇄DT); actively maintained through 07-23. |
| `docs/reference/FR_NFR.md` | CURRENT | KEEP | Requirements bible (FR/NFR + RFC-2119 + 12-step). Read-first for compliance. |
| `docs/reference/MILAN_V12_DEPENDENCY_MATRIX.md` | STALE | UPDATE | Milan→FR/NFR why-map; drop `vtb:adp = to add` (adp harness now exists). |
| `docs/SPEC_TRACEABILITY.md` | CURRENT | KEEP | Traceability hub (204 rows, reconciled TODAY 163/17/7/17). Refresh 2 watch-items next pass. |
| `docs/traceability/ieee1722_1-2021.md` | CURRENT | KEEP | ATDECC per-clause (72 rows); consistent w/ today's reconciliation. |
| `docs/traceability/ieee1722-2016.md` | STALE | UPDATE | AVTP/AAF/CRF/MAAP; CRF-8 wrongly says servo "not built" — move ❌→✅/🟡 SILICON. |
| `docs/traceability/ieee8021as.md` | CURRENT | KEEP | gPTP per-clause (11 rows); AS-4/AS-6 correctly open. |
| `docs/traceability/ieee8021q.md` | CURRENT | KEEP | 802.1Q QoS+SRP (31 rows); SRP-8/9 correctly open. |
| `docs/traceability/milan-v12.md` | STALE | UPDATE | Milan overlay (52 rows); M-CLK-3 servo now built; drop legacy -73.4 dB. |
| `docs/MILAN_COMPLIANCE_GAPS.md` | STALE | UPDATE | Live "what's left + attack order"; bump date header, reconcile -73.4 residuals, mark AX42 logic-done. |
| `docs/findings/HANDOVER_SMALL.md` | STALE | UPDATE | **Current 07-23 handover** (ship pair, servo, ALSA, roadmap); fix one row: 162/18→163/17. |
| `docs/findings/HANDOVER.md` | STALE | UPDATE | Deep session-history log (109 KB); add "SUPERSEDED for live state by HANDOVER_SMALL; this = history" banner. |
| `docs/findings/BENCH_TOPOLOGY.md` | STALE | UPDATE | Best bench-ops onboarding doc; move §9 live-state out, fix loop -73.4→-83.9, ship pair, QSPI rule. |
| `docs/findings/README.md` | STALE | UPDATE | findings index; add the 6 missing docs (2 handovers, bench, ADP/gPTP/HWTS post-mortems). |
| `docs/findings/PERF_ON_MILAN.md` | CURRENT | KEEP | Durable profiling method (cross-perf, timer sampling, offline symbolize). Only worked example is perf-era. |
| `docs/findings/PERFORMANCE_GOAL.md` | STALE | UPDATE (+MERGE TARGET) | Surviving perf-campaign record; fix scoreboard + forward-pointer; absorb RX_TX_PERFORMANCE + GIGABIT_HEADROOM. |
| `docs/findings/RX_TX_PERFORMANCE.md` | DUPLICATE | MERGE→PERFORMANCE_GOAL | Same campaign/scoreboard, more pedagogical; false "authoritative current-state" claim. |
| `docs/findings/GIGABIT_HEADROOM_ANALYSIS.md` | STALE | MERGE→PERFORMANCE_GOAL | Preserve cycles/byte budget model + "silicon data-plane already gigabit, rest is socket API" verdict. |
| `docs/findings/RX_FANOUT_AND_TX_CEILING.md` | OBSOLETE | ARCHIVE | 07-07 snapshot (TX 186/RX 223); datapath-probe takeaways survive in PIPELINE_STAGES. |
| `docs/findings/CAMPAIGN_500_PLAN.md` | OBSOLETE | ARCHIVE | Completed/superseded gated plan (self-declares SUPERSEDED); outcomes in PERFORMANCE_GOAL/CHANGELOG. |
| `docs/findings/SESSION_HANDOFF.md` | OBSOLETE | ARCHIVE | 07-11 live-state; HANDOVER.md labels it "(historical)"; content now in HANDOVER + BENCH_TOPOLOGY. |
| `docs/findings/SINGLE_PORT_PERF.md` | DUPLICATE | MERGE→LATENCY_INVESTIGATION | Prequel that explicitly defers to LATENCY_INVESTIGATION; same 07-05 investigation. |
| `docs/findings/LATENCY_INVESTIGATION.md` | STALE | KEEP (absorb SINGLE_PORT_PERF) | Most durable historical doc: 1424 ns/miss memory-latency decomposition, timeless. |
| `docs/findings/RX_MEMORY_HIERARCHY_PLAN.md` | OBSOLETE | ARCHIVE (extract table first) | Completed L2 disambiguation; extract evergreen latency-cliff table to LATENCY_INVESTIGATION/LSU doc before archiving. |
| `docs/findings/RX_OVERLOAD_WEDGE.md` | OBSOLETE | ARCHIVE | [FIXED] RX-storm post-mortem; contract survives in test_ring_bd.py + PIPELINE_STAGES R5. |
| `docs/findings/RX_RING_DMA.md` | OBSOLETE | ARCHIVE | Byte-ring era (<=07-05); byte-ring now folded out of default builds. |
| `docs/findings/TX_READER_PREFETCH_PLAN.md` | OBSOLETE | ARCHIVE | Completed-and-rejected plan (measure-before-build exemplar); Appendix-A counters worth linking. |
| `docs/findings/RX_PERF_TUNING_MAP.md` | STALE | KEEP | Operational how-to for the drawio knob map; keep for the LETHAL pairing hazards; mark point-in-time lines. |
| `docs/findings/ADP_DORMANCY.md` | CURRENT | KEEP | Silicon-proven fixed-bug post-mortem; A_ADP_DIAG 0x668 + MILAN_CLK_FREQ_HZ trap still valid. |
| `docs/findings/CBS_DATAPATH_BUG.md` | CURRENT | KEEP | [FIXED] classifier/arbiter post-mortem; sibling (distinct bug) of CBS_DEFAULT_SHAPING_BUG. |
| `docs/findings/CBS_DEFAULT_SHAPING_BUG.md` | CURRENT | KEEP | [FIXED] CBS_EN_RST=0000 reset-default; carries own superseded banner. |
| `docs/findings/GPTP_RXPAD_ROOTCAUSE.md` | CURRENT | KEEP | RX-pad fix + live switch-behavior matrix (why es-1.1/1.2 are switch-gated). |
| `docs/findings/kl-eth-tx-debug.md` | CURRENT | KEEP | Definitive TX bring-up teaching doc; reword one stale "OPEN" header→CLOSED. |
| `docs/findings/PTP_TS_METADATA_FIX.md` | CURRENT | KEEP | HW-timestamp DMA "Record contract v2.1" ABI reference. |
| `docs/design/MAAP_FABRIC.md` | STALE | UPDATE | MAAP byte-exact contract; reframe plan→as-built, reconcile CSR block (0x6D0 STAT0/STAT1) to REGISTER_MAP. |
| `docs/design/MILAN_TALKER_SM.md` | STALE | UPDATE | Talker connection SM (shipped); refresh "out of scope" (lwSRP/MAAP/listener all landed). |
| `docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md` | STALE | UPDATE | Known-issues + lethal-pairings + refuted-levers; fix cpu-count line + reconciled-date. |
| `docs/limitations/TROUBLESHOOTING.md` | CURRENT | KEEP | Durable symptom→fix runbook; well-maintained superseded-notes. |
| `docs/integration/INTEGRATION_GUIDE.md` | CURRENT | KEEP | milan_datapath port-by-port contract; accurate to RTL. |
| `docs/integration/AXIS_CORES_ON_NAXRISCV.md` | CURRENT | KEEP | "How CPU talks to fabric" model; add 1-line VexiiRiscv-now note (nicety). |
| `docs/integration/BOARD_PORTING_AX7101.md` | CURRENT | KEEP | Canonical new-board port story; minor e1/e2 GMII wording touch-up. |
| `docs/integration/QSPI_FLASHBOOT.md` | CURRENT | KEEP | Canonical flashboot mechanism + field notes. |
| `docs/integration/BUILDING.md` | STALE | UPDATE | Only doc for build.sh two-board flow; refresh cfg_ax7101/cfg_arty paragraphs + handover cross-ref. |
| `docs/integration/PORTING_GUIDE.md` | STALE | UPDATE | Living vendor-neutrality inventory; fix tops count + closed avtp_stream_parser gap. |
| `docs/integration/FULLY_FPGA_RISCV_MIGRATION.md` | OBSOLETE | ARCHIVE | Completed migration plan; as-built truth in LITEX_SOC + BOARD_PORTING + AVDECC docs. |
| `docs/integration/OPEN_SOURCE_MIGRATION.md` | OBSOLETE | ARCHIVE | Completed de-Xilinx plan; successor is PORTING_GUIDE §2. Preserve Forencich catalog + X#→map. |
| `docs/litex/LITEX_SOC.md` | STALE | UPDATE | Best LiteX-host description; refresh CPU/clock/build to 1-hart+L2-32K@100e6; add build.sh pointer. |
| `docs/MVP_TALKER.md` | STALE | UPDATE | AAF frame/CSR still live; headline media-clock caveat superseded by servo — add status banner. |
| `docs/ENDSTATION_BUILDER.md` | CURRENT | KEEP | Fresh (07-22) SW-defined end-station builder design; item-4-DONE. |
| `docs/NXN_ARCHITECTURE.md` | CURRENT | KEEP | Normative NxN AAF architecture (item 5); P12 estimator note current. |
| `docs/LWSRP_FPGA_ARCHITECTURE.md` | CURRENT | KEEP | Canonical single-stream lwSRP engine spec; light refresh (listener half done, defer counts). |
| `docs/testing/TESTING.md` | STALE | UPDATE | Top-level verification index; drop hardcoded 17-name list for "ls tb/verilator/ is authoritative". |
| `docs/testing/RUNNING_TESTS.md` | STALE | UPDATE | Layered test runbook; refresh harness/top counts. |
| `docs/testing/SIMULATION.md` | STALE | UPDATE | Sim-layers explainer; fix 15-vs-17 inconsistency, add VexiiRiscv-now note. |
| `docs/testing/PROTOCOL_VALIDATION_MATRIX.md` | STALE | UPDATE | module×test coverage view; roll status glyphs forward to CERT/silicon, fix counts, H-10 Vivado-installed. |
| `docs/testing/BEHAVE_TEST_PLAN.md` | CURRENT | KEEP | Dated TODAY; live bridge SPEC_TRACEABILITY→behave (item 10 active). |
| `docs/templates/README-parameters.template.md` | CURRENT | KEEP | Per-module parameter template; load-bearing for the builder. |
| `docs/templates/README-tests.template.md` | CURRENT | KEEP | Per-module test template; row format rolls up into SPEC_TRACEABILITY. |
| `docs/diagrams/README.md` | CURRENT | KEEP | Diagrams catalog; add the 3 perf-campaign diagrams to make it complete (minor). |

Totals: **31 KEEP, 33 UPDATE, 4 MERGE (sources), 11 ARCHIVE, 1 NEW** = 79 existing + 1 new.

---

## 2. OBSOLETE → ARCHIVE list

Move each to `docs/archive/` (create the dir), leaving a one-line stub/pointer at the old path
so inbound links resolve. All are completed plans or point-in-time snapshots whose durable
content already lives in a designated living doc.

| Archive | Superseded by (living successor) | Preserve on the way out |
|---|---|---|
| `docs/findings/RX_FANOUT_AND_TX_CEILING.md` | PIPELINE_STAGES.md, PERFORMANCE_GOAL.md | TX-is-datapath/shaper-bound + datapath-probe method |
| `docs/findings/CAMPAIGN_500_PLAN.md` | PERFORMANCE_GOAL.md, CHANGELOG.md | measurement-contract discipline |
| `docs/findings/SESSION_HANDOFF.md` | HANDOVER.md, BENCH_TOPOLOGY.md | final campaign scoreboard (already summarized in HANDOVER) |
| `docs/findings/RX_MEMORY_HIERARCHY_PLAN.md` | PIPELINE_STAGES.md, RX_TX_PERFORMANCE(merged) | **extract latency-cliff table (L1 ~36 ns / L2-32K 227 ns / DRAM 340-409 ns / 1424 ns/miss) into LATENCY_INVESTIGATION or LSU_NONBLOCKING_DCACHE first** |
| `docs/findings/RX_OVERLOAD_WEDGE.md` | test_ring_bd.py DriverModel, PIPELINE_STAGES R5 | "completion BDs pop in posted-buffer order; drops never pop" contract |
| `docs/findings/RX_RING_DMA.md` | PIPELINE_STAGES.md (byte-ring folded) | burst-DMA fix + measurement-chain method + SVG/drawio assets |
| `docs/findings/TX_READER_PREFETCH_PLAN.md` | PIPELINE_STAGES.md | Appendix-A reader latency/starve counters (link from pipeline-telemetry.md) |
| `docs/fpga/CPPI_DMA_REDESIGN.md` | PIPELINE_STAGES.md, HEADER_SPLIT_DESIGN.md | CPPI motivation + lview.sh layer-per-layer debug method |
| `docs/fpga/HW_GRO_RSC.md` | PIPELINE_STAGES.md R3, HEADER_SPLIT_DESIGN.md | RSC merge-rules concept (BD-v2 ABI kept accurately downstream) |
| `docs/integration/FULLY_FPGA_RISCV_MIGRATION.md` | LITEX_SOC.md, BOARD_PORTING_AX7101.md, INTEGRATION_GUIDE.md, OPEN_SOURCE_MIGRATION(archived), AVDECC docs | PS→fabric S1-S7 decomposition narrative |
| `docs/integration/OPEN_SOURCE_MIGRATION.md` | PORTING_GUIDE.md §2 | **Forencich core catalog (§2) + X#→replacement mapping (§3) verbatim** |

Link-repair required when these land:
- `docs/fpga/FPGA_DESIGN.md` sec4 → CPPI_DMA_REDESIGN, HW_GRO_RSC (repoint to archive), HSPLIT14 (repoint to HEADER_SPLIT_DESIGN).
- `docs/integration/PORTING_GUIDE.md` + FULLY_FPGA_RISCV_MIGRATION → OPEN_SOURCE_MIGRATION (repoint to archive path).
- `docs/fpga/RX_MEMORY_HIERARCHY_PLAN.md` referrers: RX_TX_PERFORMANCE (being merged), LSU_NONBLOCKING_DCACHE (fix pointer).

---

## 3. MERGE groups (target ← sources)

### Merge A — Perf/DMA campaign consolidation → `docs/findings/PERFORMANCE_GOAL.md`
- **Target**: `docs/findings/PERFORMANCE_GOAL.md` (the HANDOVER-designated surviving perf-lineage landing doc).
- **Sources folded in**: `docs/findings/RX_TX_PERFORMANCE.md` (plain-language RX explanation + diagram links), `docs/findings/GIGABIT_HEADROOM_ANALYSIS.md` (cycles/byte budget model + "silicon data-plane already gigabit; the rest is the socket API" verdict).
- **Rationale**: These three froze the same >500 campaign scoreboard at different dates with
  conflicting numbers (RX 298 vs 316 vs 381; TX 452 vs 525-536 vs 582-646). Consolidating gives
  one source of truth. End-state of the perf cluster: **PERFORMANCE_GOAL = campaign record;
  CHANGELOG = lever ledger; PERF_ON_MILAN = method; LATENCY_INVESTIGATION = memory root-cause.**
  On merge, add a closing banner: "campaign closed; ship shape is 1-hart, these are
  perf-lineage records." Fix the stale forward-pointer (points at RX_TX_PERFORMANCE, itself
  superseded) and update the final scoreboard.

### Merge B — Single-port prequel → `docs/findings/LATENCY_INVESTIGATION.md`
- **Target**: `docs/findings/LATENCY_INVESTIGATION.md`.
- **Source folded in**: `docs/findings/SINGLE_PORT_PERF.md` ("second core won't help single-flow" conclusion).
- **Rationale**: SINGLE_PORT_PERF explicitly defers to LATENCY_INVESTIGATION for the deeper
  story; same 07-05 30-Mbit/s investigation. Fold the conclusion in and archive/stub the prequel.

### Merge C — Header-split cut-through chapter → `docs/fpga/HEADER_SPLIT_DESIGN.md`
- **Target**: `docs/fpga/HEADER_SPLIT_DESIGN.md` (designated header-split silicon-history home; live BD v2/v3 ABI).
- **Source folded in**: `docs/fpga/HSPLIT14_DESIGN.md` (hsq12/hsplit14 per-page cut-through; v3 fill_len/hdr_idx).
- **Rationale**: HSPLIT14 is the direct hsq12 continuation of HEADER_SPLIT_DESIGN's hsq4-10
  narrative — same subsystem. Fold in as the cut-through chapter so the whole header-split
  history lives in one file; preserve its RTL/driver-level detail. Repoint FPGA_DESIGN.md sec4.

---

## 4. UPDATE list — per-doc stale-fact fixes

Recurring themes (apply the same reconciliation everywhere it appears): **dual-hart → 1-hart +
L2-32K** ship shape (2-hart = superseded perf variant); **-73.4 dB → -83.9 dB** loop
(servo silicon-proven); **162/18 → 163/17** matrix; **17 harnesses → ~41 dirs**, **18 tops →
~39 tops** (prefer "listing is authoritative"); **Vivado Artix-7 installed / CERT 63/63**;
**RGMII → GMII**; **CSR base 0x43C0_0000 → 0x9000_0000**.

| Path | Fixes |
|---|---|
| `README.md` | dual-hart→1-hart+L2-32K; drop "2-core >500 campaign" as current capability; 17→~41, 18→~39; surface CERT 63/63 + servo-proven + ALSA record. |
| `docs/README.md` | fix harness count; add `docs/ARCHITECTURE_HW_SW_SPLIT.md` to a reading path + bucket table. |
| `REQUIREMENTS.md` | add platform preamble: Zynq-7020/RGMII → full-FPGA VexiiRiscv/Artix-7/GMII; CSR base 0x43C0→0x9000; driver now in the-private-test-repo, DT via LiteX. Leave REQ-* IDs untouched. |
| `TODO.md` | mark Zynq-BD phases (bd/milan-dma.tcl, axi_mcdma, IRQ_F2P) superseded; note driver/DT delivered via kl-eth+LiteX (CERT 63/63); point to 12-item roadmap + BEHAVE plan; keep open-REQ ledger. |
| `CHANGELOG.md` | add 07-10/11 header-split closing rows (TX 582-646, RX 381/374, no-copy 585-594); fix "Where the goal stands"; DDIO measured DEAD; "ship=1-hart, perf-lineage records" banner. |
| `THIRD_PARTY.md` | add `external`/fpga-avb-ethernet submodule row; verilog-ethernet Planned→Vendored (verilog-axis 48ff7a7 pin is correct). |
| `aem-and-aecp.md` | relocate root→docs/architecture/; small↔full entity split (not Raki 48/96/192); STATIC AUDIO_MAP default; WRITE_DESCRIPTOR/GET_SET_ASSOCIATION_ID → NOT_IMPLEMENTED; resolve TODO callouts; fix drawio/kebag-logic links. |
| `docs/overview/FULL_FPGA_SOLUTION.md` | CPU 2→1-hart+L2-32K; RGMII→GMII (own §9 contradicts); AVDECC/SRP now in fabric (per ARCHITECTURE_HW_SW_SPLIT rev 2); 17→~41, 18→~39. |
| `docs/overview/ARCHITECTURE.md` | hdl/ tree → spec-aligned (ieee1722/ ieee17221/ ieee8021as/ ieee8021q/ + hdl/milan/ + hdl/common); 2-hart→1-hart; 17→~40 harness dirs; 18→~39 tops. |
| `docs/overview/AVB_SWITCH_DIRECTION.md` | demote Production scoreboard (NaxRiscv 62/66, Vexii 27/30) to pointer at CHANGELOG/HANDOVER; note S1/I-series/servo landed. |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md` | refresh status cells: lwSRP/AAF/MAAP have RTL+harnesses; PHC/gPTP servo silicon-proven; add to docs/README reading path. |
| `docs/fpga/PIPELINE_STAGES.md` | R6/R8: add "records are perf-campaign-peak on 2-hart+L2-64K; ship = 1-hart + L2-32K." |
| `docs/fpga/FPGA_DESIGN.md` | axis_clk deployed 50→100 MHz; repoint sec4 links (CPPI/HW_GRO_RSC→archive, HSPLIT14→HEADER_SPLIT_DESIGN). |
| `docs/fpga/LSU_NONBLOCKING_DCACHE.md` | add ship-shape note: mlp3 (2-hart+L2-64K) = perf-peak, not shipped SoC. |
| `docs/litex/LITEX_SOC.md` | §2.5/§3: 2-hart → 1-hart+L2-32K@100e6 cert shape; example --milan-clk-freq 50→100e6 (+cert flags); add build.sh pointer. |
| `docs/integration/BUILDING.md` | cfg_ax7101 = 1-hart+L2-32K, ~83% (not 91%); cfg_arty = --with-spiflash --flashboot full + --strip-probes; handover cross-ref SESSION_HANDOFF→HANDOVER.md; cbse TX "regression" resolved. |
| `docs/integration/PORTING_GUIDE.md` | 18→~39 tops; avtp_stream_parser gap closed (now in milan_datapath top). |
| `docs/MVP_TALKER.md` | add banner: media-clock caveat superseded by silicon servo (-83.9 dB coherent chain); reframe as milestone record; keep frame/CSR content. |
| `docs/design/MAAP_FABRIC.md` | plan→as-built (KL_maap silicon-proven); reconcile CSR to REGISTER_MAP (0x6D0 STAT0/0x6D4 STAT1, no ADDR_LO/HI; MAAP_CTRL reset 0x0800). |
| `docs/design/MILAN_TALKER_SM.md` | refresh out-of-scope (lwSRP/MAAP/ACMP-listener all landed); fix stale pointer to LWSRP CSR (now 0x680-0x6A0). |
| `docs/reference/MILAN_V12_DEPENDENCY_MATRIX.md` | drop `vtb:adp = to add` (adp harness exists, cited ✅ RTL adp). |
| `docs/MILAN_COMPLIANCE_GAPS.md` | bump status date (07-21→07-23); reconcile §1/§2 -73.4 residuals to -83.9 (item 6 already correct); AX42 item 0 → logic done, silicon pending. |
| `docs/traceability/ieee1722-2016.md` | CRF-8 ❌ MISSING → ✅/🟡 SILICON (KL_mmcm_drp_servo built, -83.9 dB); drops family MISSING toward 0. |
| `docs/traceability/milan-v12.md` | M-CLK-3 servo built (roadmap item 6 not 5); M-DEV-15 -73.4→-83.9. |
| `docs/findings/HANDOVER_SMALL.md` | roadmap item 3: 162✅/18🟡/7❌ → 163/17/7 (+17 N-A). |
| `docs/findings/HANDOVER.md` | top banner: SUPERSEDED for live state by HANDOVER_SMALL (07-23); drop "true NOW"; loop -73.4→-83.9; servo DONE; ship pair mf53e/AX39; add AX42/ALSA/BRAM-ring. |
| `docs/findings/BENCH_TOPOLOGY.md` | move §9 live-state to handover; loop -73.4→-83.9; ship pair mf53e(0x000A)/AX39; servo DONE; score 43/43→63/63; AX QSPI self-boot (reconcile §10 rule vs §2); PCM-ring BRAM option. |
| `docs/findings/README.md` | add HANDOVER, HANDOVER_SMALL, BENCH_TOPOLOGY, ADP_DORMANCY, GPTP_RXPAD_ROOTCAUSE, PTP_TS_METADATA_FIX; add control-plane/bench/handover section. |
| `docs/findings/PERFORMANCE_GOAL.md` | fix line-3 forward-pointer; premise dual→1-hart; final scoreboard (TX 582-646, RX 381/374, no-copy 585-594); DDIO refuted; (also receives Merge A). |
| `docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md` | §2 cpu-count 2→1-hart+L2-32K; reconciled-date 07-11→07-23 (servo/AX42/BRAM/ALSA not yet reflected). |
| `docs/testing/TESTING.md` | drop hardcoded 17-name list → "ls tb/verilator/ authoritative"; 18→~39 tops. |
| `docs/testing/RUNNING_TESTS.md` | 17→41 harness dirs; 18→~39 tops. |
| `docs/testing/SIMULATION.md` | fix 15-vs-17 internal inconsistency (→ tree wins); 18→~39; add VexiiRiscv-current/NaxRiscv-historical note. |
| `docs/testing/PROTOCOL_VALIDATION_MATRIX.md` | 17→41, 18→~39; H-10 Vivado Artix-7 installed + CERT 63/63; roll glyphs forward (T-5 gPTP lock, A-5/7/8 AECP/ACMP/MVU, M-1/2 AVTP, L2-1/H-6 CERT). |

---

## 5. Proposed target structure (`docs/` tree for a systems engineer)

Physical directories can stay largely as-is; the value is the **logical reading order** the new
`SYSTEMS_ENGINEER_GUIDE.md` imposes. The one structural move worth doing is creating
`docs/archive/` and (optionally) `docs/architecture/` for the two homeless design docs.

```
docs/
  SYSTEMS_ENGINEER_GUIDE.md        # NEW — the single entry point (journey-ordered)
  DOC_AUDIT.md                     # this file — cleanup record
  README.md                        # doc nav hub (UPDATE)
  GLOSSARY.md                      # terms authority (KEEP)

  overview/                        # 1. WHAT the system is
    FULL_FPGA_SOLUTION.md          #   master read-first (UPDATE)
    ARCHITECTURE.md                #   by-flow map (UPDATE)
    SYSTEM_DOMAIN_MAP.md           #   by-domain/where-does-X-live (KEEP)
    AVB_SWITCH_DIRECTION.md        #   why 4-port switch + why VexiiRiscv (UPDATE)

  architecture/                    # 2. HW/SW split + deep architecture  (NEW dir)
    ARCHITECTURE_HW_SW_SPLIT.md    #   MOVE from docs/ — normative plan-of-record (UPDATE)
    aem-and-aecp.md                #   MOVE from repo root — AEM/AECP subsystem design (UPDATE)

  fpga/                            # 3a. Datapath / gateware subsystem specs
    PIPELINE_STAGES.md             #   flagship living datapath prose (UPDATE)
    FPGA_DESIGN.md                 #   gateware module map (UPDATE)
    HEADER_SPLIT_DESIGN.md         #   header-split silicon history (KEEP; ← HSPLIT14)
    LSU_NONBLOCKING_DCACHE.md      #   CPU/cache mechanism (UPDATE)
    pipeline-telemetry.md          #   milan_tlm observability (KEEP)

  design/                          # 3b. Protocol subsystem design records
    MAAP_FABRIC.md  MILAN_TALKER_SM.md            (both UPDATE)
  LWSRP_FPGA_ARCHITECTURE.md  NXN_ARCHITECTURE.md  ENDSTATION_BUILDER.md  MVP_TALKER.md

  reference/                       # 4. Register map / ABI + requirements
    REGISTER_MAP.md                #   CSR/ABI authority (KEEP)
    FR_NFR.md  MILAN_V12_DEPENDENCY_MATRIX.md
  REQUIREMENTS.md (root)  TODO.md (root)  THIRD_PARTY.md (root)

  integration/ litex/              # 5. Build & deploy
    INTEGRATION_GUIDE.md AXIS_CORES_ON_NAXRISCV.md BOARD_PORTING_AX7101.md
    QSPI_FLASHBOOT.md BUILDING.md PORTING_GUIDE.md  litex/LITEX_SOC.md

  testing/                         # 6. Test & verify
    TESTING.md RUNNING_TESTS.md SIMULATION.md PROTOCOL_VALIDATION_MATRIX.md
    BEHAVE_TEST_PLAN.md  templates/*.template.md
  limitations/ KNOWN_ISSUES_AND_LIMITATIONS.md TROUBLESHOOTING.md

  SPEC_TRACEABILITY.md             # 7. Compliance status
    traceability/ieee1722_1-2021.md ieee1722-2016.md ieee8021as.md ieee8021q.md milan-v12.md
  MILAN_COMPLIANCE_GAPS.md

  findings/                        # 8a. CURRENT ops/handover
    HANDOVER_SMALL.md (current)  HANDOVER.md (history)  BENCH_TOPOLOGY.md  README.md
    # fixed-bug post-mortems (KEEP): ADP_DORMANCY, CBS_DATAPATH_BUG, CBS_DEFAULT_SHAPING_BUG,
    #   GPTP_RXPAD_ROOTCAUSE, kl-eth-tx-debug, PTP_TS_METADATA_FIX
    # perf lineage: PERFORMANCE_GOAL (record, ← RX_TX_PERFORMANCE + GIGABIT_HEADROOM),
    #   PERF_ON_MILAN (method), LATENCY_INVESTIGATION (← SINGLE_PORT_PERF), RX_PERF_TUNING_MAP
  CHANGELOG.md (root — perf lever ledger)

  archive/                         # 8b. NEW — historical, superseded (pointers preserved)
    RX_FANOUT_AND_TX_CEILING.md CAMPAIGN_500_PLAN.md SESSION_HANDOFF.md
    RX_MEMORY_HIERARCHY_PLAN.md RX_OVERLOAD_WEDGE.md RX_RING_DMA.md TX_READER_PREFETCH_PLAN.md
    fpga/CPPI_DMA_REDESIGN.md fpga/HW_GRO_RSC.md
    integration/FULLY_FPGA_RISCV_MIGRATION.md integration/OPEN_SOURCE_MIGRATION.md
```

Cross-lane reconciliations applied in this audit:
- The 6-doc perf duplication cluster (surfaced by the `RX_TX_PERFORMANCE.md_NOTE` placeholder,
  which is not a file) is resolved by Merge A + the archive list, leaving 4 clearly-scoped
  survivors.
- `LATENCY_INVESTIGATION.md` classified STALE by freshness but action KEEP (durable root-cause);
  it absorbs SINGLE_PORT_PERF rather than being archived.
- `RX_PERF_TUNING_MAP.md` / `PIPELINE_STAGES.md` / `LSU_NONBLOCKING_DCACHE.md` are STALE only in
  CPU-topology framing — KEEP/UPDATE, never archive (operational + evergreen value).
- CBS_DATAPATH_BUG and CBS_DEFAULT_SHAPING_BUG are a sibling PAIR covering DIFFERENT bugs — NOT
  duplicates; both KEEP.
