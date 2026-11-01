# Documentation audit

**GENERATED** by `scripts/docs_inventory.py` from the tracked documents.
Do not hand-edit.

Regenerate after any document change, then run the gate.

```sh
python3 scripts/docs_inventory.py --write
python3 scripts/docs_inventory.py --check
```

## Contents

- **[Summary](#summary)** -- Counts by status and by lane.
- **[Status rules](#status-rules)** -- How each status is decided.
- **[Module directories](#module-directories)** -- Which code directories carry a README.
- **[Inventory](#inventory)** -- Every document, grouped by area.
- **[Findings](#findings)** -- Verified contradictions, with their corrections.

## Summary

Statements on D0 pages were checked at dev `1e80128f`.
Other pages wait for their area lane.

| Status | Pages | Lines |
|---|---:|---:|
| current | 178 | 73,956 |
| stale | 13 | 8,047 |
| superseded | 0 | 0 |
| obsolete | 21 | 8,002 |
| **total** | **212** | **90,005** |

| Lane | Pages | Current | Stale | Superseded | Obsolete | Verified by D0 |
|---|---:|---:|---:|---:|---:|---:|
| archive | 22 | 1 | 0 | 0 | 21 | 0 |
| design | 25 | 25 | 0 | 0 | 0 | 0 |
| findings | 23 | 23 | 0 | 0 | 0 | 0 |
| module READMEs | 81 | 81 | 0 | 0 | 0 | 0 |
| overview and guides | 21 | 19 | 2 | 0 | 0 | 12 |
| reference | 22 | 11 | 11 | 0 | 0 | 18 |
| repository contract | 4 | 4 | 0 | 0 | 0 | 0 |
| testing and CI | 14 | 14 | 0 | 0 | 0 | 0 |

## Status rules

| Status | Rule | Evidence shown |
|---|---|---|
| obsolete | The page is in the versioned archive under `docs/history/`. | The archive banner's current successor. |
| superseded | A banner in the first 15 lines names a replacement, or the data file records the judgement. | The banner line or the recorded judgement. |
| stale | The data file records a verified contradiction on the page. A page with an open finding is never current, and the gate fails a committed page that says otherwise. | The finding identifiers. |
| current | None of the above holds. | The page's generator, or no recorded contradiction. |

## Module directories

The README count includes subdirectories.

| Directory | README here | READMEs below |
|---|---|---:|
| `hdl/` | no | 14 |
| `hdl/common/` | yes | 3 |
| `hdl/ieee1722/` | no | 4 |
| `hdl/ieee17221/` | no | 1 |
| `hdl/ieee8021as/` | no | 2 |
| `hdl/ieee8021q/` | no | 2 |
| `hdl/milan/` | yes | 2 |
| `sw/` | yes | 11 |
| `sw/builder/` | yes | 1 |
| `sw/firmware/` | no | 7 |
| `sw/litex/` | no | 1 |
| `sw/mailbox/` | no | 0 |
| `sw/trace/` | yes | 1 |
| `tb/` | no | 28 |
| `tb/avtp_packet_gen_sv/` | yes | 1 |
| `tb/common/` | no | 0 |
| `tb/itests/` | yes | 1 |
| `tb/tools/` | no | 0 |
| `tb/utests/` | no | 1 |
| `tb/verilator/` | yes | 25 |
| `syn/` | no | 2 |
| `syn/ooc/` | no | 0 |
| `syn/resmap/` | no | 0 |
| `syn/yosys/` | yes | 2 |
| `configs/` | no | 0 |
| `configs/generated/` | no | 0 |
| `scripts/` | no | 0 |

## Inventory

Areas follow the directory tree.

- [root](#root) (7)
- [.github](#github) (1)
- [avdecc](#avdecc) (1)
- [docs](#docs) (10)
- [docs/design](#docsdesign) (15)
- [docs/development](#docsdevelopment) (1)
- [docs/diagrams](#docsdiagrams) (1)
- [docs/findings](#docsfindings) (23)
- [docs/fpga](#docsfpga) (2)
- [docs/guides](#docsguides) (10)
- [docs/history](#docshistory) (22)
- [docs/integration](#docsintegration) (7)
- [docs/limitations](#docslimitations) (2)
- [docs/litex](#docslitex) (2)
- [docs/overview](#docsoverview) (3)
- [docs/reference](#docsreference) (10)
- [docs/templates](#docstemplates) (2)
- [docs/testing](#docstesting) (12)
- [docs/traceability](#docstraceability) (3)
- [hdl](#hdl) (36)
- [sw](#sw) (11)
- [syn](#syn) (2)
- [tb](#tb) (28)
- [tests](#tests) (1)

### root

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [AGENTS.md](../AGENTS.md) | 452 | maintainer | AGENTS.md - AI agent operating contract | `scripts`, `hdl`, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | repository contract |
| [CHANGELOG.md](../CHANGELOG.md) | 1067 | maintainer | Milan FPGA product changelog | `tb/verilator/milan_dp`, `tb/verilator/pp_shadow`, `tb/verilator/nvm_cosim`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | repository contract |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 736 | maintainer | Contributing - house rules that keep this repo shippable | `scripts`, `syn/yosys`, `syn/ooc`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | repository contract |
| [QUICKSTART.md](../QUICKSTART.md) | 370 | all readers | QUICKSTART - clone → green test run in 30 minutes | `syn/yosys`, `tb/verilator`, `third_party/verilog-axis`, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | overview and guides |
| [README.md](../README.md) | 482 | all readers | milan-fpga: IEEE 1722 / 1722.1 and Milan on FPGA | `sw/litex`, `scripts`, `syn/yosys`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | stale | 8 finding(s): D0-001, D0-002, D0-003, D0-004, D0-005, D0-023, D0-046, D0-047 | D0 | overview and guides |
| [REQUIREMENTS.md](../REQUIREMENTS.md) | 547 | all readers | TSN/Milan FPGA requirements | `sw/firmware/ctrl_nvm`, `tb/verilator/gptp_txts`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | D0 | reference |
| [THIRD_PARTY.md](../THIRD_PARTY.md) | 59 | integrator | Third-party dependencies | `sw/trace`, `scripts`, `third_party/lwSRP` | current | no recorded contradiction | area lane | reference |

### .github

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [.github/PULL_REQUEST_TEMPLATE.md](../.github/PULL_REQUEST_TEMPLATE.md) | 70 | maintainer | PULL_REQUEST_TEMPLATE.md | -- | current | no recorded contradiction | area lane | testing and CI |

### avdecc

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [avdecc/README.md](../avdecc/README.md) | 19 | integrator | AVDECC model tools | `avdecc`, `configs`, `sw/builder` | current | no recorded contradiction | area lane | module READMEs |

### docs

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/AAF_LATENCY_TAPS.md](AAF_LATENCY_TAPS.md) | 229 | maintainer | AAF end-to-end latency - where every tap sits (roadmap item-11) | `hdl/ieee1722/aaf`, `configs`, `sw/builder`, 1722-2016 | current | no recorded contradiction | area lane | design |
| [docs/ARCHITECTURE_HW_SW_SPLIT.md](ARCHITECTURE_HW_SW_SPLIT.md) | 273 | firmware developer | Fabric and bare-metal firmware ownership | `tb/verilator/milan_dp`, `sw/firmware/ctrl_nvm`, `sw/firmware/ctrl`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | design |
| [docs/CHANNEL_MAP_64.md](CHANNEL_MAP_64.md) | 432 | maintainer | 64-channel fabric map | `hdl/ieee1722/aaf`, `avdecc`, `configs`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | design |
| [docs/DOCUMENTATION_AUDIT.md](DOCUMENTATION_AUDIT.md) | 516 | maintainer | Documentation audit | `scripts` | current | generated by `scripts/docs_inventory.py` | area lane | repository contract |
| [docs/DOC_GENERATION.md](DOC_GENERATION.md) | 358 | maintainer | Generate documentation | `scripts`, `tools/hdl_reference`, `tools/markdown` | current | no recorded contradiction | area lane | overview and guides |
| [docs/ENDSTATION_BUILDER.md](ENDSTATION_BUILDER.md) | 1185 | maintainer | Software-defined End-Station builder - spec basis (roadmap item 4) | `sw/litex`, `avdecc`, `hdl/common/csr`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/GLOSSARY.md](GLOSSARY.md) | 93 | all readers | Glossary | Milan v1.2, 1722.1-2021, 1722-2016, 802.1AS | current | no recorded contradiction | area lane | overview and guides |
| [docs/LATENCY_HISTORY_RING.md](LATENCY_HISTORY_RING.md) | 175 | maintainer | AAF latency history ring (`KL_lat_history_ring`) | `tb/verilator/lat_history_ring` | current | no recorded contradiction | area lane | design |
| [docs/MILAN_V12_ROADMAP.md](MILAN_V12_ROADMAP.md) | 564 | maintainer | Milan v1.2 - the road to full compliance | `protocol-processor`, `tb/verilator/milan_dp`, `avdecc`, Milan v1.2, 1722.1-2021, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/README.md](README.md) | 150 | all readers | Documentation index | `sw/firmware/ctrl`, `sw/firmware/ctrl_nvm`, `sw/firmware/gtest` | current | no recorded contradiction | D0 | overview and guides |

### docs/design

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/design/AREA_BUDGET.md](design/AREA_BUDGET.md) | 601 | maintainer | Area budget | `syn/ooc`, `syn/yosys`, `configs/generated` | current | no recorded contradiction | area lane | design |
| [docs/design/GM_LOSS_RECOVERY.md](design/GM_LOSS_RECOVERY.md) | 346 | maintainer | Grandmaster loss and recovery | `tb/verilator/milan_dp_gm_steps`, 1722-2016, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/design/GPTP_PLANE.md](design/GPTP_PLANE.md) | 620 | maintainer | Fabric gPTP plane | `tb/verilator/milan_dp`, `tb/verilator/gptp_txts`, `sw/litex`, Milan v1.2, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/design/MAAP_FABRIC.md](design/MAAP_FABRIC.md) | 381 | maintainer | MAAP in fabric - design + reference contract (task #18) | `hdl/ieee1722/maap`, `hdl/milan`, `tb/verilator/maap`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | design |
| [docs/design/MAILBOX_SPLIT.md](design/MAILBOX_SPLIT.md) | 1362 | firmware developer | Packet mailbox split: the contract, the HAL and the ADP slice (#665 lane F0) | `sw/firmware/ctrl`, `hdl/milan/mailbox`, `sw/mailbox`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | design |
| [docs/design/MARK_II_AREA_PLAN.md](design/MARK_II_AREA_PLAN.md) | 1469 | maintainer | Mark II area plan | `syn/ooc`, `sw/litex`, `hdl/milan`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/design/MEDIA_CLOCK_FOLLOWING.md](design/MEDIA_CLOCK_FOLLOWING.md) | 2516 | maintainer | Media-clock following: one selected AAF or CRF source | `hdl/ieee1722/crf`, `hdl/milan`, `sw/builder`, Milan v1.2, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | design |
| [docs/design/PRESENTATION_TIME_WRAP.md](design/PRESENTATION_TIME_WRAP.md) | 340 | maintainer | Presentation time, the 4.295 s wrap, and why a far-off clock alternates | `hdl/ieee1722/aaf`, `hdl/ieee1722/avtp`, `hdl/milan`, 1722-2016 | current | no recorded contradiction | area lane | design |
| [docs/design/REBOOT_RESET.md](design/REBOOT_RESET.md) | 257 | maintainer | The end-station reset on an AECP REBOOT | `sw/litex`, `tb/verilator/pp_shadow`, `hdl/milan`, Milan v1.2, 1722.1-2021, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/design/SAVED_STATE_FASTCONNECT.md](design/SAVED_STATE_FASTCONNECT.md) | 1672 | maintainer | Saved state and fast connect - the backing store decision | `scripts`, `hdl/milan`, `sw/litex`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | design |
| [docs/design/SAVED_STATE_MATERIALIZATION.md](design/SAVED_STATE_MATERIALIZATION.md) | 2979 | maintainer | Saved-state materialization: who writes the non-binding records, and how they come back | `hdl`, `tb`, `protocol-processor`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | design |
| [docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md](design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md) | 2029 | maintainer | Saved-state snapshot ownership and acknowledgement identity | `hdl/milan`, `sw/firmware/milan_baremetal`, `tb/verilator/nvm_cosim` | current | no recorded contradiction | area lane | design |
| [docs/design/SPLIT_CONTROL_MEMORY.md](design/SPLIT_CONTROL_MEMORY.md) | 207 | firmware developer | Split placement control memory | `sw/litex`, `sw/firmware/ctrl`, `syn/ooc` | current | no recorded contradiction | area lane | design |
| [docs/design/TIME_SYNC.md](design/TIME_SYNC.md) | 782 | maintainer | Time synchronization | `tb/verilator/capture_coherence`, `tb/verilator/ptp`, `scripts`, Milan v1.2, 1722-2016, 802.1AS | current | no recorded contradiction | area lane | design |
| [docs/design/TRACE_LOGGING.md](design/TRACE_LOGGING.md) | 255 | firmware developer | Fault tracing: bare-metal DRAM ring and workstation bundles | `sw/trace` | current | no recorded contradiction | area lane | design |

### docs/development

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/development/CODE_QUALITY.md](development/CODE_QUALITY.md) | 2880 | maintainer | Code quality - the maintainability contract | `scripts`, `protocol-processor`, `syn/yosys`, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | testing and CI |

### docs/diagrams

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/diagrams/README.md](diagrams/README.md) | 144 | maintainer | Diagram catalog | `scripts` | current | no recorded contradiction | area lane | overview and guides |

### docs/findings

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/findings/117_AUDIO_CONTINUITY.md](findings/117_AUDIO_CONTINUITY.md) | 1349 | bench/qualification | Audio continuity against the reference peer on the ec0cc0c1 image | `avdecc`, `scripts`, 1722.1-2021 | current | no recorded contradiction | area lane | findings |
| [docs/findings/117_GPTP_SILICON_EVIDENCE.md](findings/117_GPTP_SILICON_EVIDENCE.md) | 1104 | bench/qualification | gPTP silicon evidence for issue 117: one AX7101 against the reference peer | `scripts`, `configs`, `tb/tools`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | findings |
| [docs/findings/234_PP_SHADOW_AREA_BASELINE.md](findings/234_PP_SHADOW_AREA_BASELINE.md) | 1426 | bench/qualification | Protocol processor area baseline for issue #234 | `hdl/milan`, `hdl/ieee1722/aaf`, `hdl/ieee1722/maap`, 1722-2016 | current | no recorded contradiction | area lane | findings |
| [docs/findings/387_SOFTWARE_GM_STEP.md](findings/387_SOFTWARE_GM_STEP.md) | 556 | bench/qualification | Software grandmaster steps on a running CRF stream | -- | current | no recorded contradiction | area lane | findings |
| [docs/findings/394_387_E1_SWITCH_CYCLES.md](findings/394_387_E1_SWITCH_CYCLES.md) | 477 | bench/qualification | Ten e1 switch power cycles | `sw/litex`, `hdl/ieee1722/avtp` | current | no recorded contradiction | area lane | findings |
| [docs/findings/397_SERVICE_BUDGET.md](findings/397_SERVICE_BUDGET.md) | 337 | bench/qualification | Firmware service intervals at 50 MHz | `tb/verilator/fw_service_budget`, Milan v1.2 | current | no recorded contradiction | area lane | findings |
| [docs/findings/451_TDM8_FIRST_LIGHT.md](findings/451_TDM8_FIRST_LIGHT.md) | 438 | bench/qualification | TDM8 first light, 2026-09-28 | `configs/generated`, `hdl/ieee1722/aaf`, `hdl/milan` | current | no recorded contradiction | area lane | findings |
| [docs/findings/451_TDM8_TIMING_SOC_BOARD.md](findings/451_TDM8_TIMING_SOC_BOARD.md) | 393 | bench/qualification | TDM8 link timing at the SoC board on the ec0cc0c1 image | -- | current | no recorded contradiction | area lane | findings |
| [docs/findings/451_USB_AUDIO_CAPTURE.md](findings/451_USB_AUDIO_CAPTURE.md) | 224 | bench/qualification | Capture through the USB Audio device on the ec0cc0c1 image | -- | current | no recorded contradiction | area lane | findings |
| [docs/findings/599_394_E1_LINK_CYCLES.md](findings/599_394_E1_LINK_CYCLES.md) | 433 | bench/qualification | Published link state over ten e1 switch power cycles | `scripts` | current | no recorded contradiction | area lane | findings |
| [docs/findings/606_FIRST_BIND_MEASUREMENT.md](findings/606_FIRST_BIND_MEASUREMENT.md) | 350 | bench/qualification | First talker bind on the 13eda870 image | `scripts`, 802.1Q | current | no recorded contradiction | area lane | findings |
| [docs/findings/608_75_WITHDRAWAL_AND_RESTART.md](findings/608_75_WITHDRAWAL_AND_RESTART.md) | 561 | bench/qualification | Listener withdrawal and reconnect restart on the 13eda870 image | Milan v1.2, 802.1Q | current | no recorded contradiction | area lane | findings |
| [docs/findings/617_DIN_FRAME_COHERENCE_BENCH.md](findings/617_DIN_FRAME_COHERENCE_BENCH.md) | 285 | bench/qualification | DIN frame coherence on the ec0cc0c1 image | -- | current | no recorded contradiction | area lane | findings |
| [docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md](findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md) | 5317 | bench/qualification | Media-clock following graded by THD+N, on the ec0cc0c1, bbf704ec and 5603c353 images | `tools`, `scripts`, `hdl/milan`, Milan v1.2, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | findings |
| [docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md](findings/649_RESOURCE_MAP_AND_SENSITIVITY.md) | 1227 | bench/qualification | Whole-image resource map and design-parameter sensitivity for issue #649 | `syn/resmap`, `sw/litex`, `syn/yosys` | current | no recorded contradiction | area lane | findings |
| [docs/findings/653_DISCONNECT_ORDER_BENCH.md](findings/653_DISCONNECT_ORDER_BENCH.md) | 908 | bench/qualification | Disconnect order seen by a controller, on the bbf704ec image | Milan v1.2, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | findings |
| [docs/findings/667_TALKER_START_BENCH.md](findings/667_TALKER_START_BENCH.md) | 510 | bench/qualification | Talker startup and soak observations | Milan v1.2, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | findings |
| [docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md](findings/75_RECONNECT_RESTART_MEASUREMENT.md) | 1287 | bench/qualification | Reconnect restart measurement | `scripts`, `tools` | current | no recorded contradiction | area lane | findings |
| [docs/findings/B14_BENCH_5603C353.md](findings/B14_BENCH_5603C353.md) | 711 | bench/qualification | B14 bench on dev 5603c353, 2026-10-10 | `hdl/ieee1722/avtp`, `hdl/ieee1722/crf`, `hdl/milan`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | findings |
| [docs/findings/CBS_DATAPATH_BUG.md](findings/CBS_DATAPATH_BUG.md) | 173 | bench/qualification | CBS datapath bug - classifier `tdest` mis-timing under back-to-back frames [FIXED] | `tb/verilator/classifier`, `tb/verilator/controller_rate`, `hdl/common/csr`, 802.1Q | current | no recorded contradiction | area lane | findings |
| [docs/findings/COMMERCIAL_TIMING_395.md](findings/COMMERCIAL_TIMING_395.md) | 196 | bench/qualification | Commercial-grade timing measurement for issue 395 | `sw/litex` | current | no recorded contradiction | area lane | findings |
| [docs/findings/PP_SHADOW_BASELINE.md](findings/PP_SHADOW_BASELINE.md) | 605 | bench/qualification | Protocol processor area baseline | -- | current | no recorded contradiction | area lane | findings |
| [docs/findings/README.md](findings/README.md) | 36 | bench/qualification | Findings retained in the bare-metal product tree | `scripts`, Milan v1.2 | current | no recorded contradiction | area lane | findings |

### docs/fpga

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/fpga/DATAPLANE_WALKTHROUGH.md](fpga/DATAPLANE_WALKTHROUGH.md) | 214 | maintainer | One AAF frame, hop by hop | `hdl/milan` | current | no recorded contradiction | area lane | design |
| [docs/fpga/FPGA_DESIGN.md](fpga/FPGA_DESIGN.md) | 424 | maintainer | FPGA design reference - every module in `hdl/`, and how they compose | `hdl/milan`, `hdl/common`, `hdl/common/csr`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | design |

### docs/guides

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/guides/BOARD_DEPLOYMENT.md](guides/BOARD_DEPLOYMENT.md) | 238 | bench/qualification | Board deployment guide | `sw/litex`, `configs`, `sw/builder` | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/IMPLEMENTATION_DEVELOPER.md](guides/IMPLEMENTATION_DEVELOPER.md) | 110 | maintainer | Implementation developer guide | `hdl/milan`, `sw/litex`, `hdl/common/csr` | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/PROJECT_MANAGER.md](guides/PROJECT_MANAGER.md) | 77 | bench/qualification | Project manager guide | -- | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/README.md](guides/README.md) | 48 | all readers | Choose your documentation path | -- | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/SYSTEM_INTEGRATOR.md](guides/SYSTEM_INTEGRATOR.md) | 155 | integrator | System integrator guide | `sw/litex`, `tb/verilator/milan_dp` | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/VERIFICATION_DEVELOPER.md](guides/VERIFICATION_DEVELOPER.md) | 182 | verification | Verification developer guide | `scripts`, `sw/trace`, `protocol-processor` | stale | 2 finding(s): D0-026, D0-027 | D0 | overview and guides |
| [docs/guides/gptp/HDL_DEVELOPER.md](guides/gptp/HDL_DEVELOPER.md) | 102 | maintainer | Fabric gPTP HDL-developer guide | `sw/builder` | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/gptp/MANAGER.md](guides/gptp/MANAGER.md) | 65 | bench/qualification | Fabric gPTP manager guide | -- | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/gptp/SYSTEM_INTEGRATOR.md](guides/gptp/SYSTEM_INTEGRATOR.md) | 95 | integrator | Fabric gPTP system-integrator guide | 802.1AS | current | no recorded contradiction | D0 | overview and guides |
| [docs/guides/gptp/TEST_DEVELOPER.md](guides/gptp/TEST_DEVELOPER.md) | 131 | verification | Fabric gPTP test-developer guide | `tb/verilator/gptp_shadow`, `tb/verilator/gptp_txts`, `gptp-processor` | current | no recorded contradiction | D0 | overview and guides |

### docs/history

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/history/v1/MVP_TALKER.md (historical)](history/v1/MVP_TALKER.md) | 125 | maintainer | MVP Milan Talker (Arty, flash-standalone) | `hdl/ieee1722/crf`, `tb/verilator/aaf`, 1722-2016, 802.1Q | obsolete | versioned archive; successor [docs/fpga/DATAPLANE_WALKTHROUGH.md](fpga/DATAPLANE_WALKTHROUGH.md) | archive | archive |
| [docs/history/v1/NXN_ARCHITECTURE.md (historical)](history/v1/NXN_ARCHITECTURE.md) | 1491 | maintainer | NxN AAF Milan Streams - Shared Engines + Per-Stream Context RAM | `sw/builder`, `hdl/milan`, `configs`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | obsolete | versioned archive; successor [docs/overview/ARCHITECTURE.md](overview/ARCHITECTURE.md) | archive | archive |
| [docs/history/v1/README.md](history/v1/README.md) | 96 | maintainer | Version one history | `tests`, 1722.1-2021, 1722-2016, 802.1AS | current | archive index, held by `scripts/check_archive.py` | archive | archive |
| [docs/history/v1/SPEC_TRACEABILITY.md (historical)](history/v1/SPEC_TRACEABILITY.md) | 556 | maintainer | Spec ↔ test traceability matrix | `hdl/milan`, `protocol-processor`, `sw/builder`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | obsolete | versioned archive; successor [docs/traceability/MODULE_MATRIX.md](traceability/MODULE_MATRIX.md) | archive | archive |
| [docs/history/v1/design/GM_LOSS_RECOVERY.md (historical)](history/v1/design/GM_LOSS_RECOVERY.md) | 194 | maintainer | Grandmaster loss and recovery - one fabric-owned mechanism | 802.1AS | obsolete | versioned archive; successor [docs/design/GM_LOSS_RECOVERY.md](design/GM_LOSS_RECOVERY.md) | archive | archive |
| [docs/history/v1/design/GPTP_PLANE.md (historical)](history/v1/design/GPTP_PLANE.md) | 269 | maintainer | The fabric gPTP plane | `gptp-processor`, `hdl/ieee8021as/gptp_plane`, `tb/verilator/gptp_shadow`, Milan v1.2, 802.1AS | obsolete | versioned archive; successor [docs/design/GPTP_PLANE.md](design/GPTP_PLANE.md) | archive | archive |
| [docs/history/v1/design/MILAN_TALKER_SM.md (historical)](history/v1/design/MILAN_TALKER_SM.md) | 282 | maintainer | Minimal Milan v1.2 talker - ACMP state machine + AECP streaming (design) | `hdl/milan`, `tb/verilator/milan_dp`, `hdl/ieee17221`, Milan v1.2, 1722.1-2021 | obsolete | versioned archive; successor [docs/overview/ARCHITECTURE.md](overview/ARCHITECTURE.md) | archive | archive |
| [docs/history/v1/design/TIME_SYNC.md (historical)](history/v1/design/TIME_SYNC.md) | 694 | maintainer | Time synchronization - gPTP, the PHC, and the media clock | `hdl/ieee1722/crf`, `hdl/ieee1722/aaf`, `sw/litex`, Milan v1.2, 1722-2016, 802.1AS | obsolete | versioned archive; successor [docs/design/TIME_SYNC.md](design/TIME_SYNC.md) | archive | archive |
| [docs/history/v1/findings/ADP_SHAPE_STATIC_0727.md (historical)](history/v1/findings/ADP_SHAPE_STATIC_0727.md) | 246 | maintainer | The 8×8 board advertised the 1×1 shape - and the CRF talker with it | `configs`, `sw/builder`, `sw/litex` | obsolete | versioned archive; successor [docs/ENDSTATION_BUILDER.md](ENDSTATION_BUILDER.md) | archive | archive |
| [docs/history/v1/findings/MEDIA_CLOCK_LOCK_0810.md (historical)](history/v1/findings/MEDIA_CLOCK_LOCK_0810.md) | 294 | maintainer | Media clock lock: the periodic one sample slip (2026-08-10) | `hdl/ieee1722/crf`, `tb/verilator/aaf`, `tb/verilator/media_nco`, 1722-2016 | obsolete | versioned archive; successor [docs/design/TIME_SYNC.md](design/TIME_SYNC.md) | archive | archive |
| [docs/history/v1/findings/PERFORMANCE_GOAL.md (historical)](history/v1/findings/PERFORMANCE_GOAL.md) | 252 | maintainer | Throughput campaign record - >500 Mbit/s RX and TX (closed 2026-07-10/11) | -- | obsolete | versioned archive; successor [docs/overview/FULL_FPGA_SOLUTION.md](overview/FULL_FPGA_SOLUTION.md) | archive | archive |
| [docs/history/v1/findings/PP_SHADOW_AREA_0812.md (historical)](history/v1/findings/PP_SHADOW_AREA_0812.md) | 500 | maintainer | The protocol-processor plane, measured - 2026-08-12 | `syn/ooc`, `syn/yosys`, `configs/generated`, 1722.1-2021 | obsolete | versioned archive; successor [docs/design/AREA_BUDGET.md](design/AREA_BUDGET.md) | archive | archive |
| [docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md (historical)](history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md) | 327 | maintainer | Milan v1.2 → FR/NFR dependency matrix | `hdl/milan`, `avdecc`, `protocol-processor`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | obsolete | versioned archive; successor [docs/reference/FR_NFR.md](reference/FR_NFR.md) | archive | archive |
| [docs/history/v1/reference/PROTOCOL_TRACEABILITY.md (historical)](history/v1/reference/PROTOCOL_TRACEABILITY.md) | 522 | maintainer | Protocol Traceability Map | `hdl/milan`, `hdl/ieee1722/aaf`, `hdl/ieee1722/avtp`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | obsolete | versioned archive; successor [docs/traceability/MODULE_MATRIX.md](traceability/MODULE_MATRIX.md) | archive | archive |
| [docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md (historical)](history/v1/testing/MILAN_COMPLIANCE_MATRIX.md) | 270 | maintainer | Milan v1.2 compliance matrix - counters + notifications first | `hdl/milan`, Milan v1.2, 1722.1-2021 | obsolete | versioned archive; successor [docs/reference/MILAN_FEATURE_STATUS.md](reference/MILAN_FEATURE_STATUS.md) | archive | archive |
| [docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md (historical)](history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md) | 426 | maintainer | Item-10 - PDU getter/setter verification (the plan, and what the AECP half can and cannot run) | `hdl/milan`, `protocol-processor`, `sw/builder`, Milan v1.2, 1722.1-2021 | obsolete | versioned archive; successor [docs/testing/MILAN_V12_AUDIT_2026-08-16.md](testing/MILAN_V12_AUDIT_2026-08-16.md) | archive | archive |
| [docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md (historical)](history/v1/testing/PROTOCOL_SWEEP_PLAN.md) | 342 | maintainer | Full protocol sweep - every mandatory command, every state machine, verified per clause | `tb/verilator/pp_shadow`, `hdl/milan`, `tb/tools`, Milan v1.2, 1722.1-2021, 802.1Q | obsolete | versioned archive; successor [docs/testing/RUNNING_TESTS.md](testing/RUNNING_TESTS.md) | archive | archive |
| [docs/history/v1/tests/CONFORMANCE_TESTING_HOWTO.md (historical)](history/v1/tests/CONFORMANCE_TESTING_HOWTO.md) | 405 | maintainer | BDD Conformance Testing - How It Runs | `tests/features`, `hdl/ieee17221`, `tests`, Milan v1.2, 1722.1-2021 | obsolete | versioned archive; successor [tests/README.md](../tests/README.md) | archive | archive |
| [docs/history/v1/traceability/ieee1722-2016.md (historical)](history/v1/traceability/ieee1722-2016.md) | 144 | maintainer | Traceability - IEEE 1722-2016 (AVTP: common header / AAF / CRF / MAAP) | `hdl/milan`, `hdl/ieee1722`, `hdl/ieee1722/avtp`, Milan v1.2, 1722-2016 | obsolete | versioned archive; successor [docs/traceability/MODULE_MATRIX.md](traceability/MODULE_MATRIX.md) | archive | archive |
| [docs/history/v1/traceability/ieee1722_1-2021.md (historical)](history/v1/traceability/ieee1722_1-2021.md) | 307 | maintainer | Traceability - IEEE 1722.1-2021 (ATDECC: ADP / ACMP / AECP+AEM) | `hdl/milan`, `tb/verilator/pp_shadow`, `avdecc`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1AS | obsolete | versioned archive; successor [docs/testing/MILAN_V12_AUDIT_2026-08-16.md](testing/MILAN_V12_AUDIT_2026-08-16.md) | archive | archive |
| [docs/history/v1/traceability/ieee8021as.md (historical)](history/v1/traceability/ieee8021as.md) | 73 | maintainer | Traceability - IEEE 802.1AS-2020 (gPTP) - hardware-assist scope | `hdl/ieee8021as/gptp_plane`, `tb/verilator/tsn_fuzz`, `hdl/ieee8021as/ptp_timestamp`, Milan v1.2, 802.1AS | obsolete | versioned archive; successor [docs/traceability/ieee8021as.md](traceability/ieee8021as.md) | archive | archive |
| [docs/history/v1/traceability/milan-v12.md (historical)](history/v1/traceability/milan-v12.md) | 283 | maintainer | Traceability - Milan v1.2 (Consolidated, 2023-11-30) - profile deltas | `hdl/milan`, `tb/verilator/pp_shadow`, `protocol-processor`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | obsolete | versioned archive; successor [docs/reference/FR_NFR.md](reference/FR_NFR.md) | archive | archive |

### docs/integration

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md](integration/AXIS_CORES_ON_BAREMETAL_SOC.md) | 50 | integrator | Fabric AXI-Stream cores on the bare-metal SoC | `tb/verilator/milan_dp` | stale | 2 finding(s): D0-033, D0-034 | D0 | reference |
| [docs/integration/BAREMETAL_FIRMWARE.md](integration/BAREMETAL_FIRMWARE.md) | 2335 | firmware developer | Bare-metal AX7101 firmware profile | `sw/litex`, `scripts`, `sw/builder` | stale | 5 finding(s): D0-011, D0-012, D0-013, D0-061, D0-062 | D0 | reference |
| [docs/integration/BOARD_PORTING_AX7101.md](integration/BOARD_PORTING_AX7101.md) | 187 | integrator | Board porting - Alinx AX7101 (XC7A100T-2FGG484I) | `sw/litex` | stale | 3 finding(s): D0-010, D0-038, D0-039 | D0 | reference |
| [docs/integration/BUILDING.md](integration/BUILDING.md) | 742 | integrator | Building bitstreams - the AX7101 build flow | `sw/litex`, `scripts`, `sw/builder` | current | no recorded contradiction | D0 | reference |
| [docs/integration/INTEGRATION_GUIDE.md](integration/INTEGRATION_GUIDE.md) | 205 | integrator | Datapath integration contract | `sw/litex`, `tb/verilator/milan_dp` | current | no recorded contradiction | D0 | reference |
| [docs/integration/PORTING_GUIDE.md](integration/PORTING_GUIDE.md) | 105 | integrator | Porting guide | `syn/yosys` | current | no recorded contradiction | D0 | reference |
| [docs/integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | 219 | integrator | QSPI flash-boot - skip the multi-minute serial upload | `sw/litex`, `scripts` | stale | 5 finding(s): D0-024, D0-025, D0-035, D0-036, D0-037 | D0 | reference |

### docs/limitations

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/limitations/RECURRING_DEFECT_PATTERNS.md](limitations/RECURRING_DEFECT_PATTERNS.md) | 394 | maintainer | Recurring defect patterns - how this project's bugs actually look | `sw/litex`, `scripts`, `sw/builder`, 1722.1-2021 | current | no recorded contradiction | area lane | overview and guides |
| [docs/limitations/TROUBLESHOOTING.md](limitations/TROUBLESHOOTING.md) | 1082 | bench/qualification | Troubleshooting - every problem hit bringing up the full-FPGA solution, and its fix | `tb/verilator/milan_dp`, `hdl/common`, `hdl/milan`, 1722.1-2021, 802.1Q | current | no recorded contradiction | area lane | overview and guides |

### docs/litex

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/litex/CLOCK_DOMAINS.md](litex/CLOCK_DOMAINS.md) | 457 | integrator | Clock domains, resets, and crossings | `sw/litex`, `hdl/common`, `hdl/milan` | current | no recorded contradiction | area lane | design |
| [docs/litex/LITEX_SOC.md](litex/LITEX_SOC.md) | 183 | integrator | LiteX bare-metal SoC | `sw/litex`, `configs`, `scripts` | current | no recorded contradiction | area lane | design |

### docs/overview

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/overview/ARCHITECTURE.md](overview/ARCHITECTURE.md) | 131 | all readers | Architecture | `hdl/common/csr`, `hdl/ieee1722`, `hdl/ieee8021q/ts`, Milan v1.2 | current | no recorded contradiction | area lane | overview and guides |
| [docs/overview/FULL_FPGA_SOLUTION.md](overview/FULL_FPGA_SOLUTION.md) | 129 | all readers | Full FPGA solution | `sw/litex`, Milan v1.2, 802.1AS | current | no recorded contradiction | area lane | overview and guides |
| [docs/overview/SYSTEM_DOMAIN_MAP.md](overview/SYSTEM_DOMAIN_MAP.md) | 41 | all readers | System domain map | `sw/litex`, `sw/firmware`, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | overview and guides |

### docs/reference

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/reference/EGRESS_QUEUE_MAP.md](reference/EGRESS_QUEUE_MAP.md) | 143 | integrator | Egress queue map | `tb/verilator/milan_dp`, 802.1Q | stale | 1 finding(s): D0-028 | D0 | reference |
| [docs/reference/FR_NFR.md](reference/FR_NFR.md) | 630 | all readers | Milan v1.2 endpoint - Functional & Non-Functional Requirements (FR/NFR) | `configs`, `sw/mailbox`, `hdl/milan`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | stale | 3 finding(s): D0-019, D0-020, D0-056 | D0 | reference |
| [docs/reference/MAILBOX_CONTRACT.md](reference/MAILBOX_CONTRACT.md) | 971 | firmware developer | Packet mailbox contract, generated reference | `sw/mailbox`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q | current | generated by `sw/mailbox/gen_mailbox.py` | D0 | reference |
| [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 294 | all readers | Milan v1.2 compliance matrix - all five standards, one page | `tb/verilator/aaf_clock_meter`, `hdl/milan`, `tb/verilator`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | stale | 7 finding(s): D0-021, D0-022, D0-029, D0-030, D0-031, D0-032, D0-045 | D0 | reference |
| [docs/reference/MILAN_FEATURE_STATUS.md](reference/MILAN_FEATURE_STATUS.md) | 146 | all readers | Milan feature status ledger | `scripts`, Milan v1.2 | current | no recorded contradiction | D0 | reference |
| [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 392 | integrator | Processor descriptor ownership and evidence | `avdecc`, `sw/builder`, `scripts`, Milan v1.2, 1722.1-2021 | stale | 6 finding(s): D0-050, D0-051, D0-052, D0-053, D0-054, D0-055 | D0 | reference |
| [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 2580 | integrator | Milan TSN CSR - register map (ABI) | `configs`, `hdl/milan`, `tb/verilator/milan_dp`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | stale | 11 finding(s): D0-006, D0-007, D0-008, D0-014, D0-015, D0-016, D0-017, D0-057, D0-058, D0-059, D0-060 | D0 | reference |
| [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 153 | integrator | Register-map production classes - needed / optional / debug | Milan v1.2, 1722-2016, 802.1AS | stale | 6 finding(s): D0-018, D0-040, D0-041, D0-042, D0-043, D0-044 | D0 | reference |
| [docs/reference/SUBMODULES.md](reference/SUBMODULES.md) | 669 | integrator | Submodule integration map | `sw/firmware/ctrl`, `protocol-processor`, `third_party/lwSRP`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | D0 | reference |
| [docs/reference/TRACE_EVENTS.md](reference/TRACE_EVENTS.md) | 400 | firmware developer | What is being logged - the trace event catalogue | `sw/trace` | stale | 2 finding(s): D0-048, D0-049 | D0 | reference |

### docs/templates

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/templates/README-parameters.template.md](templates/README-parameters.template.md) | 51 | verification | README-parameters - `<module name(s)>` (TEMPLATE) | `hdl`, `configs`, `sw/builder`, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [docs/templates/README-tests.template.md](templates/README-tests.template.md) | 48 | verification | README-tests - `<module name(s)>` (TEMPLATE) | `hdl`, `tb/verilator`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | module READMEs |

### docs/testing

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/testing/726_STREAM_COUNTERS.md](testing/726_STREAM_COUNTERS.md) | 237 | bench/qualification | Stream counter packet counts and notification gaps | `tb/verilator/milan_dp`, `tb/tools`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/ASSERTIONS.md](testing/ASSERTIONS.md) | 301 | verification | Assertion-based verification with bound SVA checkers | `tb/verilator/ptp_ts`, `tb/common`, `hdl/common` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/CI_IMAGE.md](testing/CI_IMAGE.md) | 908 | verification | CI tools image | `ci/image`, `scripts`, `tb/verilator/milan_dp` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/CI_SIGNATURE.md](testing/CI_SIGNATURE.md) | 151 | verification | CI execution signatures | `scripts` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/CI_WORKFLOWS.md](testing/CI_WORKFLOWS.md) | 3414 | verification | CI workflow policy | `scripts`, `sw/builder`, `sw/litex` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/MILAN_V12_AUDIT_2026-08-16.md](testing/MILAN_V12_AUDIT_2026-08-16.md) | 424 | bench/qualification | Milan v1.2 implementation audit, 2026-08-16 | `tb/verilator/milan_dp`, `hdl/milan`, `protocol-processor`, Milan v1.2, 1722.1-2021, 802.1AS | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/PP_SHADOW_BASELINE_RECIPE.md](testing/PP_SHADOW_BASELINE_RECIPE.md) | 641 | verification | Protocol processor baseline recipe | `syn/ooc`, `configs/generated`, `sw/builder` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/RUNNING_TESTS.md](testing/RUNNING_TESTS.md) | 249 | verification | Running the tests | `scripts`, `sw/litex`, `sw/builder` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/SIMULATION.md](testing/SIMULATION.md) | 365 | verification | Simulation - how the Milan design is simulated and verified | `tb/verilator`, `tb/verilator/milan_dp`, `sw/litex`, Milan v1.2, 1722.1-2021, 802.1Q | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/TESTING.md](testing/TESTING.md) | 1927 | verification | Testing & verification - the complete map | `scripts`, `sw/litex`, `tb/verilator`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/evidence/REBASE-REGRESSION-2026-08-01-55a68a45.md](testing/evidence/REBASE-REGRESSION-2026-08-01-55a68a45.md) | 58 | verification | REBASE REGRESSION - targeted gate record against 55a68a45 | `scripts`, `tb/verilator` | current | no recorded contradiction | area lane | testing and CI |
| [docs/testing/methodology.md](testing/methodology.md) | 165 | verification | Testing methodology - levels, oracles, and the rules every lane is bound by | `scripts`, `tb/tools`, `tests` | current | no recorded contradiction | area lane | testing and CI |

### docs/traceability

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [docs/traceability/MODULE_MATRIX.md](traceability/MODULE_MATRIX.md) | 175 | verification | Module ↔ spec ↔ test traceability matrix | 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | reference |
| [docs/traceability/ieee8021as.md](traceability/ieee8021as.md) | 83 | verification | IEEE 802.1AS traceability | 802.1AS | current | no recorded contradiction | area lane | reference |
| [docs/traceability/ieee8021q.md](traceability/ieee8021q.md) | 164 | verification | Traceability - IEEE 802.1Q-2022 (VLAN / FQTSS-CBS / MRP / MSRP / MVRP) | `hdl/milan`, `tb/verilator/pp_shadow`, `hdl/ieee8021q/filtering`, Milan v1.2, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | reference |

### hdl

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [hdl/common/README-tests.md](../hdl/common/README-tests.md) | 19 | verification | `common/common` -- modules & test coverage | `hdl/common` | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/common/csr/README-tests.md](../hdl/common/csr/README-tests.md) | 13 | verification | `common/csr` -- modules & test coverage | `hdl/common/csr` | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/common/csr/doc/milan_csr.md](../hdl/common/csr/doc/milan_csr.md) | 172 | maintainer | Entity: milan_csr | `hdl/common/csr`, `tb/verilator/csr`, `hdl/milan`, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [hdl/common/eth_event_counter/README-tests.md](../hdl/common/eth_event_counter/README-tests.md) | 15 | verification | `common/eth_event_counter` -- modules & test coverage | `hdl/common/eth_event_counter` | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/common/eth_event_counter/doc/ethernet_events.md](../hdl/common/eth_event_counter/doc/ethernet_events.md) | 59 | maintainer | Entity: ethernet_events | `hdl/common/eth_event_counter` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/common/eth_event_counter/doc/event_counter.md](../hdl/common/eth_event_counter/doc/event_counter.md) | 45 | maintainer | Entity: event_counter | `hdl/common/eth_event_counter` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/aaf/README-parameters.md](../hdl/ieee1722/aaf/README-parameters.md) | 71 | maintainer | README-parameters - `KL_i2s_playback` | `hdl/ieee1722/aaf`, `hdl`, `configs` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/aaf/README-tests.md](../hdl/ieee1722/aaf/README-tests.md) | 36 | verification | `ieee1722/aaf` -- modules & test coverage | `hdl/ieee1722/aaf`, 1722-2016 | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee1722/aaf/doc/KL_aaf_rx_depacketizer/KL_aaf_rx_depacketizer.md](../hdl/ieee1722/aaf/doc/KL_aaf_rx_depacketizer/KL_aaf_rx_depacketizer.md) | 58 | maintainer | Entity: KL_aaf_rx_depacketizer | `hdl/ieee1722/aaf`, Milan v1.2, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/aaf/doc/KL_i2s_playback/KL_i2s_playback.md](../hdl/ieee1722/aaf/doc/KL_i2s_playback/KL_i2s_playback.md) | 21 | maintainer | Entity: KL_i2s_playback | `hdl/ieee1722/aaf` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/aaf/doc/TEST_RESULTS.md](../hdl/ieee1722/aaf/doc/TEST_RESULTS.md) | 17 | verification | AAF receive path - test results | `hdl/ieee1722/aaf`, `hdl/ieee1722/avtp`, `tb/verilator/aaf` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/aaf/doc/audio_frontend_family.md](../hdl/ieee1722/aaf/doc/audio_frontend_family.md) | 99 | maintainer | Audio capture front-end family - interface contract | `hdl/ieee1722/aaf`, `sw/builder`, `tb/verilator/aes3` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/avtp/README-tests.md](../hdl/ieee1722/avtp/README-tests.md) | 20 | verification | `ieee1722/avtp` -- modules & test coverage | `hdl/ieee1722/avtp`, 1722-2016 | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee1722/avtp/doc/KL_avtp_rx_monitor/KL_avtp_rx_monitor.md](../hdl/ieee1722/avtp/doc/KL_avtp_rx_monitor/KL_avtp_rx_monitor.md) | 58 | maintainer | Entity: KL_avtp_rx_monitor | `hdl/ieee1722/avtp`, Milan v1.2, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/avtp/doc/TEST_RESULTS.md](../hdl/ieee1722/avtp/doc/TEST_RESULTS.md) | 225 | verification | AAF/AVTP stream field campaign (tsn-gen driven) | `hdl/ieee1722/avtp`, `tb/verilator/tsn_fuzz`, `hdl/ieee1722/aaf` | current | generated page | area lane | module READMEs |
| [hdl/ieee1722/avtp/doc/kl-avtp-common-parser/KL_avtp_common_parser.md](../hdl/ieee1722/avtp/doc/kl-avtp-common-parser/KL_avtp_common_parser.md) | 100 | maintainer | Entity: KL_avtp_common_parser | `hdl/ieee1722/avtp`, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee1722/crf/README-tests.md](../hdl/ieee1722/crf/README-tests.md) | 21 | verification | `ieee1722/crf` -- modules & test coverage | `hdl/ieee1722/crf`, 1722-2016 | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee1722/maap/README-tests.md](../hdl/ieee1722/maap/README-tests.md) | 13 | verification | `ieee1722/maap` -- modules & test coverage | `hdl/ieee1722/maap`, 1722-2016 | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee1722/maap/doc/KL_maap/KL_maap.md](../hdl/ieee1722/maap/doc/KL_maap/KL_maap.md) | 38 | maintainer | Entity: KL_maap | `hdl/ieee1722/maap`, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee17221/adp/README-tests.md](../hdl/ieee17221/adp/README-tests.md) | 13 | verification | `ieee17221/adp` -- modules & test coverage | `hdl/ieee17221/adp`, 1722.1-2021 | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee8021as/gptp_plane/README-tests.md](../hdl/ieee8021as/gptp_plane/README-tests.md) | 16 | verification | `ieee8021as/gptp_plane` -- modules & test coverage | `hdl/ieee8021as/gptp_plane`, 802.1AS | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md](../hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md) | 772 | verification | gPTP/802.1AS field campaign (tsn-gen driven) | `hdl/ieee8021as/gptp_plane`, `gptp-processor`, `tb/verilator/tsn_fuzz`, Milan v1.2, 802.1AS | current | generated page | area lane | module READMEs |
| [hdl/ieee8021as/ptp_timestamp/README-tests.md](../hdl/ieee8021as/ptp_timestamp/README-tests.md) | 17 | verification | `ieee8021as/ptp_timestamp` -- modules & test coverage | `hdl/ieee8021as/ptp_timestamp`, 802.1AS | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee8021as/ptp_timestamp/doc/ptp_ts_core.md](../hdl/ieee8021as/ptp_timestamp/doc/ptp_ts_core.md) | 108 | maintainer | Entity: ptp_ts_core | `hdl/ieee8021as/ptp_timestamp`, `hdl/common` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021as/ptp_timestamp/doc/ptp_ts_top.md](../hdl/ieee8021as/ptp_timestamp/doc/ptp_ts_top.md) | 84 | maintainer | Entity: ptp_ts_top | `hdl/ieee8021as/ptp_timestamp` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021as/ptp_timestamp/doc/timestamp_counter.md](../hdl/ieee8021as/ptp_timestamp/doc/timestamp_counter.md) | 40 | maintainer | Entity: timestamp_counter | `hdl/ieee8021as/ptp_timestamp` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021q/filtering/README-tests.md](../hdl/ieee8021q/filtering/README-tests.md) | 14 | verification | `ieee8021q/filtering` -- modules & test coverage | `hdl/ieee8021q/filtering`, 802.1Q | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee8021q/filtering/doc/tcam.md](../hdl/ieee8021q/filtering/doc/tcam.md) | 98 | maintainer | `tcam` - ternary CAM destination-MAC database (design doc) | `hdl/ieee8021q/filtering`, `tb/verilator/tcam` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021q/ts/README-tests.md](../hdl/ieee8021q/ts/README-tests.md) | 18 | verification | `ieee8021q/ts` -- modules & test coverage | `hdl/ieee8021q/ts`, 802.1Q | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/ieee8021q/ts/doc/credit_based_shaper/credit_based_shaper.md](../hdl/ieee8021q/ts/doc/credit_based_shaper/credit_based_shaper.md) | 55 | maintainer | Entity: credit_based_shaper | `hdl/ieee8021q/ts` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021q/ts/doc/traffic_classifier/traffic_classifier.md](../hdl/ieee8021q/ts/doc/traffic_classifier/traffic_classifier.md) | 89 | maintainer | Entity: traffic_classifier | `hdl/ieee8021q/ts` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021q/ts/doc/traffic_controller_802_1q/traffic_controller_802_1q.md](../hdl/ieee8021q/ts/doc/traffic_controller_802_1q/traffic_controller_802_1q.md) | 56 | maintainer | Entity: traffic_controller_802_1q | `hdl/ieee8021q/ts`, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021q/ts/doc/traffic_queues/traffic_queues.md](../hdl/ieee8021q/ts/doc/traffic_queues/traffic_queues.md) | 96 | maintainer | Entity: traffic_queues | `hdl/ieee8021q/ts` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/ieee8021q/ts/doc/traffic_shaping_core/traffic_shaping_core.md](../hdl/ieee8021q/ts/doc/traffic_shaping_core/traffic_shaping_core.md) | 48 | maintainer | Entity: traffic_shaping_core | `hdl/ieee8021q/ts` | current | no recorded contradiction | area lane | module READMEs |
| [hdl/milan/README-tests.md](../hdl/milan/README-tests.md) | 17 | verification | `milan/milan` -- modules & test coverage | `hdl/milan` | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |
| [hdl/milan/mailbox/README-tests.md](../hdl/milan/mailbox/README-tests.md) | 20 | verification | `milan/mailbox` -- modules & test coverage | `hdl/milan/mailbox` | current | generated by `docs/traceability/gen_module_matrix.py` | area lane | module READMEs |

### sw

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [sw/README.md](../sw/README.md) | 64 | integrator | `sw/` - build the bare-metal Milan SoC | `sw`, `sw/litex`, `scripts` | current | no recorded contradiction | area lane | module READMEs |
| [sw/builder/README-parameters.md](../sw/builder/README-parameters.md) | 245 | integrator | End-station builder parameters | `sw/builder`, `configs`, `scripts`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/ctrl/README.md](../sw/firmware/ctrl/README.md) | 742 | firmware developer | ctrl: the bare-metal control-plane firmware (#665) | `sw/firmware/ctrl`, `tests`, `third_party/tsn-c-stack`, Milan v1.2, 1722.1-2021, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/ctrl/aecp/README.md](../sw/firmware/ctrl/aecp/README.md) | 218 | firmware developer | AECP firmware owner | `sw/firmware/ctrl`, `sw/firmware/gtest`, `tb/verilator/milan_dp`, Milan v1.2, 1722.1-2021 | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/ctrl/maap/README.md](../sw/firmware/ctrl/maap/README.md) | 226 | firmware developer | Bare-metal MAAP | `sw/firmware/ctrl`, `sw/firmware/gtest`, `third_party/tsn-c-stack`, Milan v1.2, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/ctrl/srp/README.md](../sw/firmware/ctrl/srp/README.md) | 384 | firmware developer | Bare-metal MSRP and MVRP | `sw/firmware/ctrl`, `configs`, `sw/firmware/gtest`, Milan v1.2, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/ctrl_nvm/README.md](../sw/firmware/ctrl_nvm/README.md) | 510 | firmware developer | ctrl_nvm: the bare-metal saved-state store (#665 F1) | `sw/firmware/ctrl_nvm`, `sw/firmware/ctrl`, `scripts` | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/gtest/README.md](../sw/firmware/gtest/README.md) | 454 | firmware developer | gtest: the host unit tests of the bare-metal firmware (#665 lane FT) | `sw/firmware/gtest`, `sw/firmware/ctrl_nvm`, `sw/firmware/ctrl` | current | no recorded contradiction | area lane | module READMEs |
| [sw/firmware/nvm_hosttest/README.md](../sw/firmware/nvm_hosttest/README.md) | 328 | firmware developer | nvm_hosttest: the saved-state writer on a host model | `sw/firmware/nvm_hosttest`, `scripts`, `sw/firmware/milan_baremetal` | current | no recorded contradiction | area lane | module READMEs |
| [sw/litex/patches/README.md](../sw/litex/patches/README.md) | 52 | maintainer | LiteX ecosystem patches | `sw/litex`, `scripts` | current | no recorded contradiction | area lane | module READMEs |
| [sw/trace/README.md](../sw/trace/README.md) | 118 | firmware developer | `sw/trace/` - the CTF fault log | `sw/trace` | current | no recorded contradiction | area lane | module READMEs |

### syn

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [syn/yosys/README.md](../syn/yosys/README.md) | 533 | maintainer | Open-toolchain synthesis check (Yosys) - device portability | `syn/yosys`, `scripts`, `tb/verilator`, 1722.1-2021, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [syn/yosys/bench/README.md](../syn/yosys/bench/README.md) | 330 | maintainer | Yosys single-process bench | `syn/yosys`, `protocol-processor` | current | no recorded contradiction | area lane | module READMEs |

### tb

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [tb/avtp_packet_gen_sv/README.md](../tb/avtp_packet_gen_sv/README.md) | 26 | verification | Docs | `tb/avtp_packet_gen_sv` | current | no recorded contradiction | area lane | module READMEs |
| [tb/itests/README.md](../tb/itests/README.md) | 16 | verification | Integration testbenches (legacy, Vivado xsim) | `tb/itests`, `tb/avtp_packet_gen_sv`, `tb/common` | current | no recorded contradiction | area lane | module READMEs |
| [tb/utests/802_1q_traffic_shaper/README.md](../tb/utests/802_1q_traffic_shaper/README.md) | 16 | verification | Legacy 802.1Q traffic-shaper unit tests (Vivado xsim) | `tb/utests`, `tb/verilator`, `tb/verilator/cbs`, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/README.md](../tb/verilator/README.md) | 151 | verification | Verilator verification harnesses | `tb/verilator`, `scripts`, `syn/yosys`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/aaf/README.md](../tb/verilator/aaf/README.md) | 108 | verification | AAF talker checks | `tb/verilator/aaf`, Milan v1.2, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/avtp_parser/README.md](../tb/verilator/avtp_parser/README.md) | 111 | verification | avtp_parser - the listener ACCEPT VERDICT, at every shipping shape | `tb/verilator/avtp_parser`, `hdl/ieee1722/avtp`, `tb/verilator/avtp_stream`, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/avtp_stream/README.md](../tb/verilator/avtp_stream/README.md) | 16 | verification | avtp_stream - AVTP stream parser verification | `tb/verilator/avtp_stream`, `hdl/ieee1722/avtp` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/cbs/README.md](../tb/verilator/cbs/README.md) | 119 | verification | CBS verification harness (IEEE 802.1Qav credit-based shaper) | `tb/verilator/cbs`, `hdl/common`, `hdl/ieee8021q/ts`, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/controller_rate/README.md](../tb/verilator/controller_rate/README.md) | 22 | verification | controller_rate - CBS end-to-end shaping/interference regression (bug FIXED; gating) | `tb/verilator/controller_rate`, `tb/verilator/classifier` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/csr/README.md](../tb/verilator/csr/README.md) | 106 | verification | CSR verification harness (`milan_csr` AXI4-Lite control plane) | `tb/verilator/csr`, `hdl/common/csr`, `tb/common` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/fw_service_budget/README.md](../tb/verilator/fw_service_budget/README.md) | 271 | verification | Firmware service-budget measurement | `tb/verilator/fw_service_budget`, `tb/verilator/nvm_capture_cpu`, Milan v1.2 | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/gptp_plane/README.md](../tb/verilator/gptp_plane/README.md) | 65 | verification | gptp_plane -- the time-sync plane against the real PHC | `tb/verilator/gptp_plane`, `tb/verilator/gptp_shadow`, `hdl/ieee8021as/ptp_timestamp`, 802.1AS | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/gptp_shadow/README.md](../tb/verilator/gptp_shadow/README.md) | 135 | verification | gptp_shadow -- the fabric slice, wide faces, loop closed in fabric | `tb/verilator/gptp_shadow`, `tb/verilator/gptp_plane`, `third_party/verilog-axis` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/gptp_tables/README.md](../tb/verilator/gptp_tables/README.md) | 108 | verification | gptp_tables -- per-table lockstep of the fabric gPTP plane | `tb/verilator/gptp_tables`, `scripts`, `tb/verilator/gptp_shadow` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/gptp_txts/README.md](../tb/verilator/gptp_txts/README.md) | 89 | verification | `gptp_txts` - the gPTP egress timestamp closed loop | `tb/verilator/gptp_txts`, `sw/litex`, `hdl/common` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/mbx/README.md](../tb/verilator/mbx/README.md) | 345 | verification | mbx: the packet-mailbox fabric skeleton, through both bus adapters | `tb/verilator/mbx`, `sw/mailbox`, `sw/firmware/ctrl`, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/media_grid_align/README.md](../tb/verilator/media_grid_align/README.md) | 78 | verification | media_grid_align - the #74 grid-alignment loop, closed over the real NCO | `tb/verilator/media_grid_align`, `tb/verilator/milan_dp` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/media_nco/README.md](../tb/verilator/media_nco/README.md) | 146 | verification | `media_nco` - the steerable media sample grid | `tb/verilator/media_nco`, `hdl/ieee1722/crf`, `tb/verilator/capture_coherence`, Milan v1.2 | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/milan_dp/README.md](../tb/verilator/milan_dp/README.md) | 1688 | verification | milan_dp - the `milan_datapath` integration suite | `tb/verilator/milan_dp`, `scripts`, `tb/verilator/milan_dp_gm_steps`, Milan v1.2, 1722.1-2021, 802.1Q, 802.1AS | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/milan_dp_gm_steps/README.md](../tb/verilator/milan_dp_gm_steps/README.md) | 126 | verification | milan_dp_gm_steps: the GM step leg and its controls (#387, #602, #621) | `tb/verilator/milan_dp_gm_steps`, `tb/verilator/milan_dp` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/milan_dp_gptp/README.md](../tb/verilator/milan_dp_gptp/README.md) | 44 | verification | AX7101 physical gPTP integration suite | `tb/verilator/milan_dp_gptp`, `scripts`, `tb/verilator/milan_dp` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/milan_dp_mclk/README.md](../tb/verilator/milan_dp_mclk/README.md) | 114 | verification | milan_dp_mclk: media-clock following at the root (#629) | `tb/verilator/milan_dp_mclk`, `tb/verilator/milan_dp`, `tb/verilator/follow_ring`, 1722-2016 | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/nvm_backend/README.md](../tb/verilator/nvm_backend/README.md) | 144 | verification | nvm_backend -- the saved-state backing store, graded on bytes | `tb/verilator/nvm_backend`, `scripts`, `hdl/milan` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/nvm_capture_cpu/README.md](../tb/verilator/nvm_capture_cpu/README.md) | 195 | verification | Product CPU capture measurement | `tb/verilator/nvm_capture_cpu`, `scripts`, `sw/litex` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/nvm_cosim/README.md](../tb/verilator/nvm_cosim/README.md) | 202 | verification | nvm_cosim -- the saved-state snapshot ownership co-simulation | `tb/verilator/nvm_cosim`, `hdl/milan`, `scripts` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/pp_shadow/README.md](../tb/verilator/pp_shadow/README.md) | 502 | verification | pp_shadow - milan_datapath with the protocol processor AS the control plane | `tb/verilator/pp_shadow`, `hdl/ieee17221`, `hdl/ieee17221/adp`, Milan v1.2, 1722.1-2021, 802.1Q | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/reboot_ctrl/README.md](../tb/verilator/reboot_ctrl/README.md) | 98 | verification | reboot_ctrl -- the end-station reset on an AECP REBOOT | `tb/verilator/reboot_ctrl`, `hdl/milan`, `tb/verilator/pp_shadow` | current | no recorded contradiction | area lane | module READMEs |
| [tb/verilator/tsn_fuzz/README.md](../tb/verilator/tsn_fuzz/README.md) | 456 | verification | `tsn_fuzz` - IEEE 1722 field-validation campaign | `tb/verilator/tsn_fuzz`, `scripts`, `hdl/ieee1722/avtp`, Milan v1.2, 1722.1-2021, 1722-2016, 802.1AS | current | no recorded contradiction | area lane | module READMEs |

### tests

| Page | Lines | Audience | Purpose | Describes | Status | Evidence | Verified | Lane |
|---|---:|---|---|---|---|---|---|---|
| [tests/README.md](../tests/README.md) | 185 | verification | AECP Test Strategy | `tests`, `tb/tools`, `scripts`, 1722.1-2021, 1722-2016, 802.1Q | current | no recorded contradiction | area lane | module READMEs |

## Findings

Each statement is quoted exactly from its page.
Its area lane fixes it and removes the entry.

| ID | Page | Line | Statement | Contradicted by | Correction |
|---|---|---:|---|---|---|
| D0-001 | [README.md](../README.md) | 60 | ADP, ACMP, AECP, MAAP and SRP default to bare-metal firmware. | `sw/litex/milan_soc.py` lines 2854-2856 and line 4097: `--ctrl-mailbox` defaults off and the default build carries no mailbox; the same section says all-fabric is the shipping default | Say that the Mark II split placement moves ADP, ACMP, AECP, MAAP and SRP into bare-metal firmware, and that the default build keeps all of them in fabric. |
| D0-002 | [README.md](../README.md) | 142 | clock-source selection now reaches the media plane's wrapper but nothing there | `hdl/milan/milan_datapath.sv` lines 734-750: the stored CLOCK_SOURCE is resolved in `media_clk_resolve` and consumed by the INTERNAL, CRF and AAF followers (#74, #629) | State that SET_CLOCK_SOURCE selects the followed media clock (INTERNAL, CRF or one AAF input), and link the media-clock following design. |
| D0-003 | [README.md](../README.md) | 419 | Stream restart latency after an ACMP rebind (2026-08, OPEN) | #75 is closed; the measurement is `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md`; the roadmap figure repeats it as open (12 to 90 s) | Retire section P1.6 and the roadmap bullet, and point at the #75 finding. |
| D0-004 | [README.md](../README.md) | 441 | **Not the index-bus narrowing** in `KL_lwsrp_ctx.sv` | Commit `eff99a9c` (2026-08-13) deleted the fabric SRP context; no `KL_lwsrp_ctx.sv` is tracked, and `JOIN_TIME_MS_C` (line 447) has no definition in the tree | Remove the analysis of the deleted module with section P1.6. |
| D0-005 | [README.md](../README.md) | 471 | is **steerability**. `media_tick_p` is a compile-time constant with no | `hdl/ieee1722/crf/KL_media_nco.sv` (steerable media grid, 2026-08-10) and `hdl/ieee1722/crf/KL_media_grid_align.sv` (#74) replaced the constant divider | Rewrite P1.7 as the current media-clock status (#629, #74) with a link to the media-clock following design, or retire it. |
| D0-023 | [README.md](../README.md) | 41 | \| TSN datapath in fabric \| MAC · 802.1Qav CBS · gPTP | Same as D0-019: CAP.CBS reads 0 and no shaper is instantiated since 0x0056 | Remove CBS from the shipping datapath row, or mark it as an earlier measurement on an older image. |
| D0-046 | [README.md](../README.md) | 348 | proof (#394) | #394 closed on 2026-09-29; the one-port link loss and return proof is recorded in `docs/findings/599_394_E1_LINK_CYCLES.md`, and the same figure marks the closed #389 as done | Mark the #394 link-loss and return proof done, with a pointer to the finding, as the figure does for #389. |
| D0-047 | [README.md](../README.md) | 383 | open is the write side. See the mandatory gaps in | `docs/reference/milan_feature_status.json` `missing_mandatory_aem_operations` is empty and the README's own gated block (lines 136-139) says every mandated operation is served since 0x0002_0054, the setters included (`docs/reference/MILAN_COMPLIANCE_MATRIX.md` rows 5.4.2.5 to 5.4.2.16) | Name what is still open instead (the saved-state cold cycles, Auto Connect, the media plane's adoption of the sampling rate) and link the feature ledger. |
| D0-026 | [docs/guides/VERIFICATION_DEVELOPER.md](guides/VERIFICATION_DEVELOPER.md) | 32 | Migen scripts lack one aggregate runner. | `scripts/run_litex_sims.sh` lines 99-108 (`INVENTORY`) and line 150 (`run_aggregate`) run every standalone Migen simulation as one aggregate and refuse a missing or unlisted member; the page itself names the runner at line 23 | Say that `scripts/run_litex_sims.sh` is the aggregate runner of the standalone Migen simulations. |
| D0-027 | [docs/guides/VERIFICATION_DEVELOPER.md](guides/VERIFICATION_DEVELOPER.md) | 49 | C has no general harness framework. | `sw/firmware/gtest/README.md` lines 3-13: the bare-metal control-plane firmware and its saved-state store are unit-tested on the host with GoogleTest and GoogleMock through one shared harness, graded by `sw/firmware/ctrl/test/test_ctrl_firmware.py` and `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py` | Name the shared host harness `sw/firmware/gtest/` for the control-plane firmware's C, and keep the trace round-trip as the check of the shipping trace producer. |
| D0-033 | [docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md](integration/AXIS_CORES_ON_BAREMETAL_SOC.md) | 23 | Its default is bare-metal control; all-fabric remains supported. | Same as D0-001: `sw/litex/milan_soc.py` lines 2854-2856, `--ctrl-mailbox` defaults off and the default build carries no mailbox; the page's next line says all-fabric is the shipping default | Say that the Mark II split placement puts the selected functions in bare-metal firmware and that the default build keeps all five in fabric. |
| D0-034 | [docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md](integration/AXIS_CORES_ON_BAREMETAL_SOC.md) | 18 | may cross clock domains only with a complete-packet asynchronous FIFO. | `sw/litex/milan_soc.py` lines 1553-1583 and 1871-1873: the shipping MAC adapter crosses each direction with a 16-beat buffered `stream.ClockDomainCrossing` (`_AXIS_CDC_DEPTH`, line 1413), not a complete-packet FIFO; the store-and-forward `PacketFIFO` (`tx_sf`, line 1810) is a separate transmit stage in the sys domain, and `configs/endstation_ax7101_1x1_tdm8.yaml` lines 43-44 put the datapath at 50 MHz against a 100 MHz sys clock, so the crossing is live | State the shipping crossing: a 16-beat buffered asynchronous FIFO per direction, with a store-and-forward packet FIFO before the MAC core on transmit; say what a port must preserve instead of naming a FIFO type the shipping SoC does not use. |
| D0-011 | [docs/integration/BAREMETAL_FIRMWARE.md](integration/BAREMETAL_FIRMWARE.md) | 215 | pending #403, which decides the receive-filter posture | #403 closed as completed on 2026-09-26; `sw/litex/boot_policy.py` line 58 generates `MILAN_MAC_CTRL_SET` (bit 3), written at `sw/firmware/milan_baremetal/milan_baremetal.c` line 1827 | Name the generated `MILAN_MAC_CTRL_SET` word and drop the pending reference. |
| D0-012 | [docs/integration/BAREMETAL_FIRMWARE.md](integration/BAREMETAL_FIRMWARE.md) | 218 | `srp.talker_declare_at_reset`, pending #400 | #400 closed as completed on 2026-09-26; the firmware writes `MILAN_LWSRP_CTRL_RESET \| 3u` at `sw/firmware/milan_baremetal/milan_baremetal.c` line 1833 | Drop the pending reference and state the forced bits as the shipped behaviour. |
| D0-013 | [docs/integration/BAREMETAL_FIRMWARE.md](integration/BAREMETAL_FIRMWARE.md) | 219 | block count `MILAN_N_TALKERS` + 1 in `[15:8]` | `sw/litex/boot_policy.py` line 56: `MILAN_MAAP_CTRL_BOOT` is `len(stream_outputs) << 8 \| 1`, so the extra block exists only when the CRF output is declared | Write the generated `MILAN_MAAP_CTRL_BOOT`: one block per declared AAF output, plus one when the CRF output is enabled. |
| D0-061 | [docs/integration/BAREMETAL_FIRMWARE.md](integration/BAREMETAL_FIRMWARE.md) | 200 | writes these words in this order and no others | `sw/firmware/milan_baremetal/milan_baremetal.c` line 1828: `configure_fabric()` also writes `MILAN_TCAM_CTRL` (0x700) with `MILAN_TCAM_CTRL_BOOT` = 1 (`sw/litex/boot_policy.py` line 59), right after `MAC_CTRL`; the table has no `TCAM_CTRL` row | Add the `TCAM_CTRL` (`0x700`) row between `MAC_CTRL` and `AAF_CTRL`: value `MILAN_TCAM_CTRL_BOOT` (1), the existing accept-all posture. |
| D0-062 | [docs/integration/BAREMETAL_FIRMWARE.md](integration/BAREMETAL_FIRMWARE.md) | 2286 | record below is the shipping option-on measurement; an elaboration estimate | The record below measures commit `1e80a106` (2026-08-19, line 2291): 15,849 of 15,850 slices and +0.033 ns WNS. The shipping route has moved since: the #787 re-pin record in `docs/reference/SUBMODULES.md` lines 511-517 and `docs/design/AREA_BUDGET.md` lines 149-150 gives +0.365 ns WNS with 63 of 15,850 slices free at processor `a9e84b66`, and the resource records live in `docs/design/AREA_BUDGET.md` | Call the table the first option-on record (commit `1e80a106`) and point at the current shipping route record instead of naming this one the shipping measurement. |
| D0-010 | [docs/integration/BOARD_PORTING_AX7101.md](integration/BOARD_PORTING_AX7101.md) | 110 | acceptance remains on [#599](https://github.com/kebag-logic/milan-fpga/issues/599). | #599 closed as completed on 2026-09-29; the bench result is `docs/findings/599_394_E1_LINK_CYCLES.md` | Point at the #599 link-cycle finding instead of an open issue. |
| D0-038 | [docs/integration/BOARD_PORTING_AX7101.md](integration/BOARD_PORTING_AX7101.md) | 81 | `s7ddrphy.A7DDRPHY` + `add_sdram(module=MT41J256M16, l2_cache_size=8192)` behind a new | `sw/litex/milan_soc.py` lines 3270-3274: `add_staged_sdram(..., l2_cache_size = 0)` with the comment "The product profile is cacheless end to end"; line 4301 refuses any `--l2-bytes` in the bare-metal profile | Write `l2_cache_size=0` and say the product SoC is cacheless. |
| D0-039 | [docs/integration/BOARD_PORTING_AX7101.md](integration/BOARD_PORTING_AX7101.md) | 88 | `./sw/litex/milan_soc.py --full --xlen 64` elaborates and **exports a P&R-ready | `sw/litex/milan_soc.py` lines 3963-3966 make `baremetal` the only `--software-profile`, and lines 4298-4300 refuse it unless `--xlen 32`, so the command exits with an argument error instead of elaborating | Give the current elaboration command (RV32, the bare-metal profile) or mark section 4 as the dated record of an earlier RV64 build; the Contents entry repeats the same command. |
| D0-024 | [docs/integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | 60 | was deleted 2026-08-13 with this repository's own AECP/AEM engine, so nothing | `sw/firmware/milan_baremetal/milan_baremetal.c` lines 329-331 put saved-state slots A and B in `MILAN_FLASH_JOURNAL_OFFSET`, the `journal` range of `sw/litex/milan_soc.py` line 173; `nvm_commit()` (line 1405) erases, programs and verifies the alternate slot, and `nvm_boot()` (line 1656, called at line 1914) judges both slots at every boot | Say that the `journal` range holds the bare-metal firmware's two 64 KiB saved-state slots, written alternately and judged at every boot, which is why a reflash must not erase it; the `user` range stays reserved and unused. |
| D0-025 | [docs/integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | 62 | the protocol processor's NVM face is answered by a blank-flash responder, so a | `hdl/milan/KL_pp_shadow.sv` line 1128 instantiates `KL_nvm_backend` behind the processor's NVM face; `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163 records the binding surviving a cold power cycle on silicon since 2026-09-21 (#70) | State that the restore walk reads the saved records back from the journal and that the binding survives a power cycle on silicon (#70); keep separate what is still owed physically: no board cold cycle grades the names or the channel maps yet (`docs/design/SAVED_STATE_MATERIALIZATION.md` lines 15-16 and 23). |
| D0-035 | [docs/integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | 96 | The AEM copy goes through the BIOS's `copy_image_from_flash_to_ram`, so the | `sw/firmware/milan_baremetal/milan_baremetal.c` lines 1860-1892: `load_aem_image()` checks the `AEMI` magic, copies `MILAN_AEM_IMAGE_BYTES` with its own loop and then compares the CRC32 with the compiled-in `MILAN_AEM_IMAGE_CRC32`; nothing under `sw/` calls `copy_image_from_flash_to_ram` | Name `load_aem_image()` and its three checks (magic, compiled-in length, CRC32 after the copy), and keep the consequence: a failed check leaves the entity disabled. |
| D0-036 | [docs/integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | 162 | reachable with the standard quad read (`READ_1_1_4`, 0x6B). `mode="4x"` drives all four DQ, | `sw/litex/milan_soc.py` lines 3287-3302: the AX7101 uses `N25Q128A13(SpiCodes.READ_1_1_1_FAST)` with `add_spi_flash(mode="1x", clk_freq=int(12.5e6))`, because the quad read CRC-failed non-deterministically on silicon (2026-07-08); line 3309 skips the BIOS frequency calibration | State the single-lane fast read (0x0B, 1-1-1) at the 12.5 MHz request with `SPIFLASH_SKIP_FREQ_INIT`, and why the quad read was dropped. |
| D0-037 | [docs/integration/QSPI_FLASHBOOT.md](integration/QSPI_FLASHBOOT.md) | 108 | `ax8x8` and `arty` differ from `ax7101` only in dataplane shape: | `sw/litex/build.sh` lines 382-399: `ax8x8` has never produced a bitstream, and `arty` is a retired DUT on another board (datapath 50 MHz, sys 83.333 MHz); `sw/litex/milan_soc.py` lines 3282-3288 give the Arty an S25FL128S on `READ_1_1_1` | Say that the named configs share the {bitstream, AEM} manifest, that `ax8x8` differs in dataplane shape and has not been built, and that `arty` is a retired DUT on another board. |
| D0-028 | [docs/reference/EGRESS_QUEUE_MAP.md](reference/EGRESS_QUEUE_MAP.md) | 38 | \| q3 \| gPTP classification target \| disabled \| | `hdl/common/ethernet_packet_pkg.sv` lines 220-221: `GPTP_CLASS = 3'd2` (q2) and `SRB_CLASS = 3'd3` (q3); the reset `CLS_TCQ` word `0x004898C0` (`hdl/common/csr/milan_csr.sv` line 2008) maps TC2 to q3, and the page's own slope table (lines 56-57) agrees | Swap the two rows: q3 is class B (disabled until configured) and q2 is the gPTP classification target (disabled). |
| D0-019 | [docs/reference/FR_NFR.md](reference/FR_NFR.md) | 173 | \| **FR-QOS-01..03** \| **MET** \| Classifier + CBS untouched; | `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8 and `hdl/common/csr/milan_csr.sv` lines 1996-2000 (CAP.CBS = 0): since VERSION 0x0056 `milan_datapath` instantiates no classifier or shaper; the same page says so at lines 50 and 228-230 | Mark FR-QOS-01 and FR-QOS-02 not met in the product (the blocks exist and are verified, but are not instantiated), and keep FR-QOS-03 as the processor's admission ceiling. |
| D0-020 | [docs/reference/FR_NFR.md](reference/FR_NFR.md) | 277 | 802.1Q / 802.1Qav *(already in HW)* | Same as D0-019: the classifier and CBS are not instantiated in the shipping datapath | Drop the already-in-HW marker, or say the blocks are verified but not instantiated. |
| D0-056 | [docs/reference/FR_NFR.md](reference/FR_NFR.md) | 77 | Its default is bare-metal control over packet mailboxes. | Same as D0-001 and D0-033: `sw/litex/milan_soc.py` lines 2854-2856, `--ctrl-mailbox` defaults off and the default build carries no mailbox; the paragraph's first and fifth lines say all-fabric is the shipping default | Say that the Mark II split placement puts the selected functions in bare-metal firmware and that the default build keeps all five in fabric. |
| D0-021 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 265 | \| 8.6.8.1 \| strict priority (non-CBS queues) \| fabric \| implemented | `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8: `milan_datapath` does not instantiate the shaper since 0x0056; the page describes the shipping image (line 3) | Mark the row as verified RTL that is not instantiated in the shipping image. |
| D0-022 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 266 | \| 8.6.8.2 \| credit-based shaper: idleSlope/sendSlope, transmitAllowed | Same as D0-021 | Mark the row as verified RTL that is not instantiated in the shipping image. |
| D0-029 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 262 | \| 9.4 / 9.6 \| C-TAG TPID 0x8100; TCI = PCP·DEI·VID \| fabric \| implemented | `hdl/milan/milan_datapath.sv` lines 684-694: the classifier the row cites as evidence is not instantiated since VERSION 0x0056; the shipping C-TAG is written by `KL_aaf_packetizer` (`hdl/ieee1722/aaf/KL_aaf_packetizer.sv` line 514) and `KL_crf_tx` (`hdl/ieee1722/crf/KL_crf_tx.sv` line 514) and read by `avtp_stream_parser` (`hdl/ieee1722/avtp/avtp_stream_parser.sv` line 159), all instantiated in `milan_datapath` | Cite the instantiated framers and stream parser as the evidence instead of the uninstantiated classifier. |
| D0-030 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 263 | \| 6.9.3 / 6.9.4 \| PCP encoding on transmit; priority regeneration on receive \| fabric \| implemented | `hdl/milan/milan_datapath.sv` lines 684-694: receive priority regeneration is the classifier's (`CLS_PRIO_REGEN`), which `milan_datapath` does not instantiate since VERSION 0x0056; `git grep` finds no instance of `traffic_classifier` outside its own sources | Keep the transmit half (AAF and CRF TCI bytes) as implemented and mark receive priority regeneration as verified RTL that is not instantiated in the shipping image. |
| D0-031 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 264 | \| 8.6.6 + Table 8-4 \| queue per traffic class \| fabric \| implemented | Same as D0-030: no per-class queue bank (`traffic_queues`) is instantiated in `milan_datapath`, and `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-8 say so | Mark the row as verified RTL that is not instantiated in the shipping image. |
| D0-032 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 267 | granted slope drives the class-A queue's idleSlope | `hdl/milan/milan_datapath.sv` lines 8583-8589: no shaper reads the slope or the verdict; the granted slope reaches only the `LWSRP_STATUS[9]` and `LWSRP_SLOPE` (0x698) diagnostics | Say that the granted slope reaches only the two diagnostics and that no shaper consumes it in the shipping image; keep the TSpec half. |
| D0-045 | [docs/reference/MILAN_COMPLIANCE_MATRIX.md](reference/MILAN_COMPLIANCE_MATRIX.md) | 242 | \| 8.4.2.2 / 8.4.3 \| event messages timestamped at the reference plane; general messages never \| fabric (`ptp_ts_core/top`) \| | `hdl/milan/milan_datapath.sv` lines 684-687: the `ptp_ts_top` TX/RX record stampers left the datapath with the retired target (#259); the shipping event timestamps are the gPTP plane's RX-tap stamp and its reconstructed launch (`hdl/milan/milan_datapath.sv` lines 8843-8849, #360; `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv`) | Name the gPTP plane's RX tap and launch reconstruction as the owner and its suites (`tb/verilator/gptp_txts`, `tb/verilator/gptp_shadow`) as the evidence. |
| D0-050 | [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 119 | \| arty_current \| 32 \| 5792 \| 2 / 1 \| 1 / 1 \| 16 / 1 \| 1 / 2 \| | `python3 scripts/audit_pp_descriptors.py --output <file>` at this head measures 33 descriptors and 5952 bytes for arty_current, 68/10728 for arty_4x4, 100/15976 for arty_8ch, 42/7512 for ax7101_1x1_tdm8 and 124/19520 for ax7101_8x8; the CLOCK_DOMAIN offsets are 4008, 7120, 10320, 4928 and 12576 (the page's second table says 3920, 6768, 9968, 4840, 11872): the tables predate one INPUT_STREAM clock source per AAF input (#629) | Regenerate both measurement tables from the audit receipt at the head the page states. |
| D0-051 | [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 129 | All singleton counts are one; CLOCK_SOURCE count is two. | The same audit: the CONFIGURATION descriptor counts 3 CLOCK_SOURCEs on arty_current and ax7101_1x1_tdm8, 6 on arty_4x4 and arty_8ch, 10 on ax7101_8x8 (INTERNAL, CRF and one per AAF input, #629; the page's own row L6 at line 91 says so) | State the CLOCK_SOURCE count as 2 plus the AAF input count, per configuration. |
| D0-052 | [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 140 | Every domain's source list is exactly `[0,1]`. | The same audit: the CLOCK_DOMAIN source lists are [0..2] (arty_current, ax7101_1x1_tdm8), [0..5] (arty_4x4, arty_8ch) and [0..9] (ax7101_8x8), with lengths 82, 88 and 96 | Give the measured source lists and lengths, and the AAF-input entries the CRF-only text omits. |
| D0-053 | [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 288 | \| arty_current \| `0x001BC50AC1000005` \| pin \| | The same audit: the entity_model_id values are 0x001BC50AC1000006 (arty_current, pin), 0x001BC549808B210C (arty_4x4), 0x001BC55491CCAA9B (arty_8ch), 0x001BC5C1935893E1 (ax7101_1x1_tdm8) and 0x001BC5572467AF35 (ax7101_8x8), all five different from the table | Regenerate the identity table from the audit receipt, or state the head it was measured at. |
| D0-054 | [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 308 | On arty_4x4, image byte 6741 changes; the ID remains unchanged. | The same audit's identity probe at this head: the reset_time control changes image byte 7093 and the model ID stays 0x001BC549808B210C (the page's next line quotes 0x001BC557FC6ABBC8); the residue it reproduces (#495) still holds | Update the byte offset and the quoted ID from the audit receipt. |
| D0-055 | [docs/reference/PP_DESCRIPTOR_OWNERSHIP.md](reference/PP_DESCRIPTOR_OWNERSHIP.md) | 246 | Each accepted; no semantic refusal | `python3 scripts/audit_pp_descriptors.py` at this head: the packer probes for L10 (nine rate words, offset 143, count/extent mismatch, one byte short), L6 (source list reversed), L4 (buffer 2125999 ns, 47 formats) and L1, L2, L7, L8, L9 and ADP are all refused, by the processor's default model lint that #661 adopted (processor PR #144; the page's own lines 28 and 183 say so); the table records the earlier audit pin | Regenerate the processor rows from the current receipt, or mark the table as the record of the earlier pin and drop the PP60 defence-in-depth sentence that the lint has discharged. |
| D0-006 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 1226 | attribute's 802.1Q 35.2.2.7.4 FourPackedEvents value | IEEE 802.1Q-2022 (and 802.1Q-2018) define MSRP FourPackedEvents in 35.2.2.7.2 with Table 35-3; there is no 35.2.2.7.4 | Cite IEEE 802.1Q 35.2.2.7.2 (Table 35-3). |
| D0-007 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 1286 | (STREAM_INPUT[0], Milan Table 7-156) | Table 7-156 is IEEE 1722.1-2021's STREAM_INPUT counters_valid table; Milan v1.2 lists the Stream Input counters in Table 5.6 (5.3.8.10) | Write IEEE 1722.1-2021 Table 7-156 (Milan v1.2 Table 5.6). |
| D0-008 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 199 | The Milan Table 7-156 stream counters | Same as D0-007: Table 7-156 belongs to IEEE 1722.1-2021 | Write the IEEE 1722.1-2021 Table 7-156 stream counters, in the section description and its Contents entry. |
| D0-014 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 1427 | \| `0x7D4` \| `AEMP_CTRL` \| W1S / RO \| | `hdl/common/csr/milan_csr.sv` lines 885-897 (`A_ETH_GUARD` at 0x7D8), 1578 (reset armed), 1731 (write rule), 2389 (readback); the map has no 0x7D8 row, against REQ-CSR-01's acceptance | Add `0x7D8 ETH_GUARD`: RW, reset 1 (armed); writing 0x554E4C4B disarms, any other write re-arms; while armed PHY_RESET writes are dropped and LINK_CTRL[1] is masked; the link guard's own recovery is not gated. |
| D0-015 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 419 | `[0]` phy_reset_n (0 = hold PHY in reset) | `hdl/common/csr/milan_csr.sv` line 2692 drives `o_phy_reset_n` and line 1688 drops writes while ETH_GUARD is armed; `sw/litex/milan_soc.py` never connects the datapath's `o_phy_reset_n`; the pin is driven by LiteEth's CRG reset CSR (`sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch`, `pads.rst_n` from `self._reset`) | Document PHY_RESET as inert in the shipping SoC, and document `milan_mac_phy_crg_reset` (LiteX CSR) as the reset that reaches the PHY for the `--eth-port` the image is built for. |
| D0-016 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 752 | `[1]` manual mac_reinit (hold MAC sys-side in reset) | `hdl/common/csr/milan_csr.sv` lines 1726-1730: while ETH_GUARD is armed a LINK_CTRL write stores bit 1 as 0 | Add that bit 1 is masked to 0 while ETH_GUARD (0x7D8) is armed. |
| D0-017 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 416 | \| `0x110` \| `MAC_STATUS` \| RO \| – \| | `sw/litex/milan_soc.py` lines 1958-1972 and 2184-2185: MAC_STATUS is the LiteX `milan_mac_link_status` CSR, reset link up, 1000 Mb/s on GMII (100 on MII), full duplex | State the reset value, and that the bits follow the PHY once firmware publishes them: `nvm_boot()` arms the poll (`sw/firmware/milan_baremetal/milan_baremetal.c` line 1671, polled at lines 1099-1102 and 1106), and a CSR identity mismatch returns before it (lines 1900-1903), which leaves the reset value. Point to LINKG_STAT (0x774) and the AVB_INTERFACE LINK_UP/LINK_DOWN counters. |
| D0-057 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 137 | presentation-time offset is pinned at the Milan 2 ms | `docs/reference/REGISTER_MAP.md`'s own 0x0053 note (lines 351-356): SET_STREAM_INFO is served and "the stored offset feeds the framers' transit entries"; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` row 5.3.7.6 / 4.4.2.1: the 2 ms default is settable via SET_STREAM_INFO and the stamp adds the offset as set | Say that 2 ms is the default and that SET_STREAM_INFO sets each Stream Output's offset, which the framers apply. |
| D0-058 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 1327 | **Nothing in this device persists a binding across a power cycle.** The | `hdl/milan/KL_pp_shadow.sv` line 1128 instantiates `KL_nvm_backend` behind the processor's NVM face (the blank-flash responder is gone; the page's own `PP_STAT` notes at lines 2390-2406 describe `nvm_backed` and the firmware journal writer); `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70) | Keep the 0x7A0 port a dead CSR face, and say that bindings persist through the processor's restore walk and `KL_nvm_backend`, pointing at the `PP_NVM_*` and `PP_STAT` rows. |
| D0-059 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 1374 | is **not met by this build**. The | Same as D0-058: the bound state is saved and restored by the processor's walk over `KL_nvm_backend` and the firmware's A/B journal, and survives a cold cycle on silicon (#70); only this retired 0x7B8 ingest face is dead (`hdl/milan/milan_datapath.sv` lines 6709-6710) | Say that this CSR face is retired and that Milan v1.2 5.3.8.2 is served by the saved-state store, with the open physical items (#70). |
| D0-060 | [docs/reference/REGISTER_MAP.md](reference/REGISTER_MAP.md) | 1578 | and the shipping AX7101 shape is 8 | `sw/litex/build.sh` line 378: the shipping AX7101 recipe is `endstation_ax7101_1x1_tdm8`, and lines 382-384 say the 8x8 recipe has never produced a bitstream; `configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh` declares 2 talker sources and 2 listener sinks (one AAF stream each way plus CRF) | Say the shipping AX7101 (`endstation_ax7101_1x1_tdm8`) is the one-AAF-stream shape and that `endstation_ax7101_8x8.yaml` declares 8 of each. |
| D0-018 | [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 101 | \| `0x7C8–0x7D4` \| AEM saved-state write master \| | `hdl/common/csr/milan_csr.sv` line 897 allocates `A_ETH_GUARD` at 0x7D8, between the 0x7C8-0x7D4 and 0x7DC-0x7E4 rows; the page judges every CSR group | Add a 0x7D8 ETH_GUARD row with its production class. |
| D0-040 | [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 100 | **Nothing in this device persists a binding across a power cycle** | `docs/design/SAVED_STATE_MATERIALIZATION.md` line 163: the binding survives a cold power cycle on silicon since 2026-09-21 (#70), through `KL_nvm_backend` (`hdl/milan/KL_pp_shadow.sv` line 1128) and the firmware journal writer (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1405 and 1656); only this retired journal-ingest CSR face is a structural zero (`hdl/milan/milan_datapath.sv` line 6709) | Keep the row a structural zero for its CSR face and point at the saved-state store that does persist bindings (`PP_NVM_*`, 0x934-0x93C). |
| D0-041 | [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 84 | `S50milan` writes these every boot. | `S50milan` was an init script of the retired operating-system image (#259): `scripts/check_baremetal_only.py` line 1625 forbids its init.d path as a target service, and the test benches call its write "the retired S50milan poke" (`tb/verilator/milan_dp/sim_main.cpp` line 464); the bare-metal `configure_fabric()`, called by `milan_init()`, writes the identity and enables (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 1818-1821) | Say that the bare-metal firmware writes these words at every boot. |
| D0-042 | [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 83 | \| `0x4xx` \| CBS queue window, classifier map \| **needed** \| live \| | `docs/reference/EGRESS_QUEUE_MAP.md` lines 3-12 and `hdl/milan/milan_datapath.sv` lines 684-694: no classifier, queue or shaper is instantiated since VERSION 0x0056, so the 0x4xx words are write-only scratch and `CAP.CBS` reads 0 (`hdl/common/csr/milan_csr.sv` lines 1996-2000) | Mark the group write-only scratch with no consumer in the shipping image, and drop "boot software programs it" as production configuration. |
| D0-043 | [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 109 | Saved-state restoration remains absent | `docs/design/SAVED_STATE_MATERIALIZATION.md` lines 19-23 and 203: since #637 `milan_datapath` writes channel-map records 0x60 and 0x70 and restores them after the D3 walk's COMPLETE terminal | Say that the channel maps are saved and restored by the parent (#637), and that their board cold cycle is still owed. |
| D0-044 | [docs/reference/REGISTER_MAP_CLASSES.md](reference/REGISTER_MAP_CLASSES.md) | 131 | persistence remains absent. | Same as D0-043 and D0-040: bindings, scalar records and channel maps are written to and restored from the journal | Replace with the implemented saved state and what still lacks physical evidence (names and channel maps across a board cold cycle). |
| D0-048 | [docs/reference/TRACE_EVENTS.md](reference/TRACE_EVENTS.md) | 7 | Every event type the bare-metal end-station can write into its DRAM | Nothing outside `sw/trace/` includes `milan_trace.h` or calls `MILAN_TRACE`; `sw/firmware/milan_baremetal/Makefile` line 6 builds `milan_baremetal.o` alone, so the shipping image writes no trace record; `docs/design/TRACE_LOGGING.md` lines 246-250 leave the integration to the board | Say the catalogue is the ABI of the producer in `sw/trace/`, which the shipping bare-metal image does not link yet (the text comes from `sw/trace/gen_trace_events.py` line 117). |
| D0-049 | [docs/reference/TRACE_EVENTS.md](reference/TRACE_EVENTS.md) | 262 | Saved-state journal: 0x7C0 verdict + 0x7C4 SEQ, and the A/B slot decision on the write side. | `hdl/milan/milan_datapath.sv` lines 6709-6710 tie `jnl_stat_w` and `jnl_seq_w` (0x7C0, 0x7C4) to zero: the journal-ingest CSR face is a structural zero, and the saved-state verdicts now live in the firmware's slot judgement (`sw/firmware/milan_baremetal/milan_baremetal.c` lines 463-465, 1656-1694) | Describe the journal event from the firmware's slot verdicts (`nvm_verdict_a`/`_b`, the chosen slot) instead of the retired CSR pair; the text comes from `sw/trace/milan_trace.yaml`. |
