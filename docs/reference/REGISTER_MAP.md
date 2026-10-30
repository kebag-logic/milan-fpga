# Milan CSR register reference

**GENERATED** by `scripts/gen_register_reference.py` from `hdl/common/csr/milan_csr.sv` and a builder export.
Do not hand-edit.

Regenerate after any CSR change, then run the gate.

```sh
python3 scripts/gen_register_reference.py --write
python3 scripts/gen_register_reference.py --check
```

The SoC facts come from the `endstation_ax7101_1x1_tdm8` export, recorded in `scripts/register_map_soc.json`.

Production classes are in [REGISTER_MAP_CLASSES.md](REGISTER_MAP_CLASSES.md).

## Contents

| Section | What it holds |
|---|---|
| [Reading this page](#reading-this-page) | Verdicts, history notes and how to read the tables. |
| [Memory map](#memory-map) | Regions and windows of the shipping SoC. |
| [Access types](#access-types) | The access and reset codes the tables use. |
| [Build parameters](#build-parameters) | The parameters the shipping build elaborates. |
| [0x000 - Identification / IRQ](#0x000-----identification--irq) | Identification, capabilities and the interrupt registers. |
| [0x100 - MAC control / status (REQ-MAC-01..03)](#0x100-----mac-control--status--req-mac-0103) | MAC control, link status and the inert PHY reset. |
| [0x200 - Statistics (RMON) (REQ-MAC-04)](#0x200-----statistics-rmon--req-mac-04) | RMON counter snapshot and its capability mask. |
| [0x300 - 802.1Q classifier (REQ-CLS-01..04)](#0x300-----8021q-classifier--req-cls-0104) | Retained classifier words; no logic reads them. |
| [0x400 - 802.1Qav CBS (per queue) (REQ-CBS-01..03)](#0x400-----8021qav-cbs-per-queue--req-cbs-0103) | Retained per-queue CBS words; nothing reads them. |
| [0x500 - PTP hardware clock (REQ-PTP-01..04, 06)](#0x500-----ptp-hardware-clock--req-ptp-0104-06) | PTP hardware clock control, time access and PPS alarm. |
| [0x600 - ADP advertiser (IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)](#0x600-----adp-advertiser--ieee-17221-2021--milan-v12-fr-disc-0104) | ADP identity words, the advertise strobes and status. |
| [0x648 - AECP/ACMP status + AAF talker (IEEE 1722.1 / Milan v1.2)](#0x648-----aecpacmp-status--aaf-talker--ieee-17221--milan-v12) | AECP and ACMP status, and the flat AAF talker words. |
| [0x680 - lwSRP engine (802.1Q MSRP/MVRP, Milan v1.2 Section 5.6, FR-SRP-*)](#0x680-----lwsrp-engine--8021q-msrpmvrp-milan-v12-section-56-fr-srp-) | SRP control and the processor's SRP status. |
| [0x6A4 - ACMP listener SM (Milan v1.2 Section 5.5 listener, FR-CONN-01)](#0x6a4-----acmp-listener-sm--milan-v12-section-55-listener-fr-conn-01) | Listener bind record, AVTP RX, MAAP and audio diagnostics. |
| [0x700 - RX destination-MAC TCAM filter (REQ-MAC-02)](#0x700-----rx-destination-mac-tcam-filter--req-mac-02) | RX destination-MAC filter programming. |
| [0x71C - Link guard / MAC recovery (VERSION minor ≥ 0x0006)](#0x71c-----link-guard--mac-recovery-version-minor--0x0006) | Link guard controls and the reset canary. |
| [0x724 - identity / playback / 802.1AS overlay](#0x724-----identity--playback--8021as-overlay) | Entity name overlay, playback filter and gPTP parent. |
| [0x738 - CRF media-clock sink (Milan v1.2 7.3, KL_crf_rx)](#0x738-----crf-media-clock-sink--milan-v12-73-kl_crf_rx) | CRF media-clock sink control and measurements. |
| [0x750 - CRF media-clock talker (Milan v1.2 7.3.1, KL_crf_tx)](#0x750-----crf-media-clock-talker--milan-v12-731-kl_crf_tx) | CRF media-clock talker control and counters. |
| [0x768 - AECP GET_DYNAMIC_INFO scan forensics (BDBG) -- 🔴 STRUCTURAL ZERO, and the link-guard status](#0x768-----aecp-get_dynamic_info-scan-forensics-bdbg-----structural-zero-and-the-link-guard-status) | Retired scan forensics and the live link-guard status. |
| [0x778 - Clock validity: the AVTP tu verdict (VERSION minor >= 0x0016), TX arbiter and SRP domain](#0x778-----clock-validity-the-avtp-tu-verdict-version-minor--0x0016-tx-arbiter-and-srp-domain) | Clock validity, TX arbiter supervision and the SRP domain. |
| [0x7A0 - ACMP bind-restore (saved-state fast-connect E1, Milan 5.5.3.5.2)](#0x7a0-----acmp-bind-restore--saved-state-fast-connect-e1-milan-55352) | Retired bind-restore port, kept as an ABI. |
| [0x7B8 - Persistence-journal ingest (saved-state fast-connect E3)](#0x7b8-----persistence-journal-ingest--saved-state-fast-connect-e3) | Retired journal ingest port, kept as an ABI. |
| [0x7C8 - AEM dynamic-state patch port (saved-state fast-connect E4)](#0x7c8-----aem-dynamic-state-patch-port--saved-state-fast-connect-e4) | Retired AEM patch port, kept as an ABI. |
| [0x7D8 - Ethernet guard](#0x7d8-----ethernet-guard) | The Ethernet guard kill switch. |
| [0x7DC - retired AS_PATH compatibility addresses](#0x7dc-----retired-as_path-compatibility-addresses) | Retired AS_PATH addresses and the live PathTrace status. |
| [0x7E8 - gPTP plane drop diagnostics](#0x7e8-----gptp-plane-drop-diagnostics) | gPTP plane drop counters. |
| [0x7F0 - applied gPTP timestamp latency corrections](#0x7f0-----applied-gptp-timestamp-latency-corrections) | The timestamp corrections the gPTP plane applies. |
| [0x800 - Indexed per-stream window](#0x800-----indexed-per-stream-window) | Indexed window onto one stream's context. |
| [0x870 - AAF per-stage latency taps (roadmap item-11, KL_aaf_latency_taps)](#0x870-----aaf-per-stage-latency-taps--roadmap-item-11-kl_aaf_latency_taps) | AAF per-stage latency taps. |
| [0x8B4 - RX stream-parser probe (APRB, avtp_stream_parser + milan_datapath)](#0x8b4-----rx-stream-parser-probe--aprb-avtp_stream_parser--milan_datapath) | The RX stream parser's pre-match view. |
| [0x8C8 - reserved target-media compatibility words](#0x8c8-----reserved-target-media-compatibility-words) | Retired telemetry words that read zero. |
| [0x8D4 - media-boundary slip counters (SLIP, KL_chan_map_capture)](#0x8d4-----media-boundary-slip-counters--slip-kl_chan_map_capture) | Media-boundary slip counters. |
| [0x8DC - render presentation state](#0x8dc-----render-presentation-state) | Presentation state of the selected listener. |
| [0x8E0 - AAF clock meter (#629, KL_aaf_clock_meter)](#0x8e0-----aaf-clock-meter--629-kl_aaf_clock_meter) | AAF media clock meter. |
| [0x8F8 - MMCM-DRP media-clock servo (Milan v1.2 7.3.4, KL_mmcm_drp_servo)](#0x8f8-----mmcm-drp-media-clock-servo--milan-v12-734-kl_mmcm_drp_servo) | MMCM DRP media-clock servo. |
| [0x900 - channel-map fabric (Section 6 of docs/CHANNEL_MAP_64.md, KL_chan_map_render / KL_chan_map_capture)](#0x900-----channel-map-fabric--section-6-of-docschannel_map_64md-kl_chan_map_render--kl_chan_map_capture) | Channel-map debug write port and map RAM readback. |
| [0x920 - protocol-processor control plane (KL_pp_shadow, VERSION major 2)](#0x920-----protocol-processor-control-plane--kl_pp_shadow-version-major-2) | Protocol-processor control plane and the saved-state window. |
| [SoC CSR banks](#soc-csr-banks) | The LiteX CSR banks beside the Milan block. |
| [Feature status](#feature-status) | Machine-checked status rows for this page. |

## Reading this page

| Note |
|---|
| Production classification (needed / optional / debug, with rationale): [REGISTER_MAP_CLASSES.md](REGISTER_MAP_CLASSES.md). |

### READ THIS FIRST -- the control plane was replaced (VERSION major 2, 2026-08-13)

| Note |
|---|
| This repository's own IEEE 1722.1 / SRP control-plane RTL is **deleted**: the ADP advertiser and parser, the whole AECP/AEM engine, the ACMP talker and listener, and the lwSRP applicant. There is **no parameter, no fallback and no shadow arm** -- the user's instruction was "remove the old code AECP/ACMP/ADP the lwSRP shall be removed as well. Only use the uCPU code" and "do not leave the option, remove everything out of the code base that is legacy". The git history keeps all of it. |
| What serves the control plane now is [`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv), the consumer-side wrapper around the pinned `protocol-processor` submodule, which [`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) instantiates **unconditionally**. It owns ADP, ACMP (talker and listener) and SRP, publishes a class-D wire face the fabric consumes every clock, and its packed TX rides the control lane. MAAP stays in this fabric (`KL_maap`), bridged by [`hdl/milan/KL_pp_maap_shim.sv`](../../hdl/milan/KL_pp_maap_shim.sv). Those two file banners are the authoritative statement; this page is their CSR projection. |
| **THE AECP SURFACE, STATED PLAINLY: this entity serves the processor's declared command inventory, including `READ_DESCRIPTOR` and `GET_COUNTERS`.** The processor's AECP uCPU drives solicited responses onto the wire. Unsupported commands receive the conformant fallback with the correct message type, length and control data length. Invalid targets and response-as-input cases are silently refused as required. The inventory is synchronized between `tests/steps/aecp_engine_steps.py` and the RTL dispatch. |
| The command-change notifications, root-observed Milan Table 5.22 triggers, and departing-controller monitor are live since 0x0055. Remaining gaps include the root-level IDENTIFY indication, saved-state persistence, and commands outside the served inventory. The declared CRF Stream Input's counter bank is served and pushed since #529 (see the `0x738` group). Milan Delta 7 `ACQUIRE_ENTITY` receives the command-specific `NOT_SUPPORTED` response with a zero owner. |
| The processor gitlink is a required build input, not vendored source. A release candidate must pin a commit reachable from the donor's durable default branch; the fact that a feature-branch-only object can currently be fetched is not durability evidence. After any repin, validate this parent at the new exact head. |
| Machine-checked status rows are defined by the [Milan feature status ledger](MILAN_FEATURE_STATUS.md): |
| **The AEM descriptor tree is no longer a fabric ROM and has no CSR here.** The processor's descriptor store fetches it from main memory over a **read-only master** -- `milan_datapath`'s `o_desc_mem_*`/`i_desc_mem_*`, bridged to DRAM by the LiteX SoC -- at a **compile-time base** (`PP_DESC_BASE_P`, derived by the builder as the top 1 MiB of `main_ram`, never a literal). **There is no base register on this page and never will be**: software cannot relocate the image at runtime, it can only write the image there before enabling the entity. A region that fails the image header's magic/version/checksum reads as "image not loaded" -- it reports a configuration count of zero, which the microprogram's `configuration_index` check rejects before any locate -- so every `READ_DESCRIPTOR` then answers `BAD_ARGUMENTS`, not `NO_SUCH_DESCRIPTOR`. That is a clean refusal, not a hang -- the store's watchdog abandons a stalled burst -- and a late load heals without a reset, because each locate against an invalid image re-arms the header probe. |
| The tracked build supplies this image. The end-station builder emits `aem_desc.bin`, `aem_desc.json`, and `aem_desc.map`; the bare-metal firmware verifies and copies the paired image before entity enable. A custom integration must preserve that boot-time copy-before-enable ordering. |
| **The AECP counters are not on this page.** The engine's command, response, drop and locate-miss tallies, plus its last status, last length, image-valid and image-fault bits, live in the **protocol processor's side-port snapshot window**, reached through `KL_pp_shadow`'s diagnostic side-port adapter -- not at `0x648`, which keeps those counter fields at structural zero. `AECP_STAT0[16]` is the exception: it carries the processor's live `LOCK_ENTITY` level. |

### How to read this page now: three verdicts, and why the distinction matters

| Note |
|---|
| **No register was removed.** The map is an ABI and shrinking it would break every board script, so every word below still decodes and every RW word still stores. What changed is what a value *means*, and each affected word is marked with one of three verdicts: |

| Verdict | What it means | How software must treat it |
|---|---|---|
| **STRUCTURAL ZERO** | The source of this word is deleted and has no replacement. It reads `0` because there is nothing behind it, **not** because nothing happened | Never read it as a measurement. A word that read a plausible value instead would be a defect -- "engine idle" and "no engine" must not be confusable |
| **Readable, inert scratch** (legacy label: **WRITE-ONLY SCRATCH**) | The register still reads back exactly what software wrote, but the value **no longer reaches the wire** | Writing it changes nothing observable. Do not infer from a successful readback that the setting took effect |
| **LIVE, REPOINTED** | Still real, now sourced from the protocol processor's class-D face instead of a deleted engine | Read it normally; the meaning is unchanged |

| Note |
|---|
| Two structural changes that break existing decoders and are called out at their own registers below: |
| **`A_TXARB_DIAG` `0x784` lane numbering changed.** Major 2 collapsed the old eight-mux cascade to four; minor `0x0055` adds lane 4 for `gptp_ctl_mux`, making five in fabric-gPTP builds. Anything decoding that word by the old lane numbers now reads the **wrong mux**. |
| **The entity enable is now two bits ORed.** `PP_CTRL[0]` at `0x920` **or** the historic `ADP_CTRL[0]` at `0x600` enables the entity -- either one, because `ADP_CTRL.en` is the bit every existing board script writes and there is only one control plane left to enable. |
| Three functional losses have no register of their own and are recorded here so they are not discovered by surprise: |
| *(closed by #74)* **The CRF media clock IS selectable at the root.** The processor stores AECP `SET_CLOCK_SOURCE`, `KL_pp_shadow.sv` exports it, and `milan_datapath`'s `media_clk_resolve` compares it against the shape's generated `AEM_CRF_CLKSRC_C` into one registered verdict gating `KL_mmcm_drp_servo`, the `KL_media_grid_align` packet-grid chain and the CRF triggers of the 4.4.4.3 `mr` machinery (the disruption and the received toggle). A PHC-only re-base preserves `mr` under either selection. It adds no Table 5.4 MEDIA_RESET ([#602 ruling](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355)). Source changes and selected-CRF causes still request restarts. At the INTERNAL power-on state `A_MCSRV_STAT` `0x8F8` still reads idle - nothing is followed, not a tie-off - while the grid aligner runs at INTERNAL too since #629 (A2-a). Since `0x0058` junction slips are counted where software can read them, `SLIP_LB`/`SLIP_TDM` at `0x8D4`/`0x8D8`. |
| **Every Stream Output's presentation-time offset defaults to the Milan 2 ms value**, and SET_STREAM_INFO sets each Stream Output's offset, which the framers apply (`SET_MAX_TRANSIT_TIME` is gone). That is a **default, not a zero**: 0 ns would be a presentation time in the past and every listener would drop every frame as late. |
| **Milan Table 5.4 per-STREAM_OUTPUT diagnostic counters are live for solicited reads and notifications.** `KL_talker_diag_ctx` is instantiated per declared output, GET_COUNTERS serves the compact five-counter layout, and each dirty pulse reaches the rate-limited Table 5.22 scheduler through the root's lossless descriptor arbiter. Every declared STREAM_INPUT bank is live the same way, the CRF Media Clock Input's complete Table 5.16 bank included since #529 (see the `0x738` group), and a stopped CRF sink keeps observing and counting (#97). Under the 2026-10-12 #726 ruling, FRAMES_TX and FRAMES_RX count AVTPDUs with 32-bit wrap. TX resets at talker start; RX resets on not-bound to bound and survives unbind. Healthy counter updates also mark their descriptor dirty. See the [counter measurements](../testing/726_STREAM_COUNTERS.md) for the per-recipient spacing check and fixed 1025 ms refresh bound. |
| Memory-mapped control/status registers for the Milan TSN NIC. This is the **stable ABI** shared by the HDL ([`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv)), the bare-metal firmware, and every bench tool that pokes this window. Satisfies `REQ-CSR-05`; implements the control surface for `REQ-CSR/PTP/CBS/CLS/ MAC/*` in [`REQUIREMENTS.md`](../../REQUIREMENTS.md). |
| **Bus:** AXI4-Lite, 32-bit data, little-endian. The LiteX product maps the 64 KiB window at **`0x9000_0000`**; the register offsets below are fixed. |
| **Access:** `RO` read-only, `RW` read-write, `W1C` write-1-to-clear, `W1S` write-1-to-set (self-clearing command strobe), `ROc` read latches/clears. |
| Unused bits read 0; writes to `RO` fields are ignored; unmapped offsets read 0 and `SLVERR` is **not** raised (OKAY) to keep firmware access simple. |
| **Timing (2026-07-16 config-in-RAM read path):** plain-RW readback is served from a write-through shadow BRAM -- reads complete one clock later than the original mux (AXI4-Lite handshake absorbs it; no firmware change). After reset the block holds `*READY` low for ~513 clocks while the defaults ROM is swept into the shadow, so soft-reset readback values are identical to before. |
| `N` = `NUMBER_OF_QUEUES` (from `CAP.num_queues`, default **5** since VERSION `0x0014`; it was 6 from `0x0011` to `0x0013`). Queue **4 is the highest priority**, queue 0 the lowest (802.1Q order) -- see [EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md). |

### A group can be STRUCTURALLY absent (optional-block prunes, 2026-07-27)

| Note |
|---|
| Six `milan_datapath` blocks are now behind **elaboration-time prune parameters** ([docs/design/AREA_BUDGET.md](../design/AREA_BUDGET.md) tier 1). **Every one defaults to PRESENT**, so a shipping build's map is exactly what this page describes. A build that pulls a lever keeps the *register window* -- the address still decodes, RW words still store and read back -- but the block behind it is gone and its RO words read a **structural zero**, which is not a measurement: |

| Parameter | Reads 0 structurally | Other effect |
|---|---|---|
| `MCSERVO_P = 0` | `0x8F8 MCSRV_STAT` | `0x8FC MCSRV_CTRL` still RW; MMCM DRP/PS pins never move |
| `LTAP_P = 0` | `0x874`-`0x8B0`; `0x870 LTAP_CTRL` reads `0x2` (enable bit only, no status) | -- |
| `MAAP_P = 0` | `0x6D0 MAAP_STAT0`, `0x6D4 MAAP_STAT1` | `MAAP_CTRL.en` becomes effectively **reserved**: setting it pins AAF admission shut |
| `I2SPB_P = 0` | `0x6D8 I2SPB_STAT`, `0x6E0 I2SPB_TRIM`, `0x6F0 I2SPB_DBG` | the four `i2s_dac_*` pins park at 0 |
| `RXFILT_P = 0` | -- | the whole `0x700` TCAM group still stores; **nothing reads it** and the port is PROMISCUOUS |
| `LPF_P = 0` | -- | `0x72C LPF_CTRL` still RW with no filter behind it |

| Note |
|---|
| There is deliberately **no capability bit** for these (unlike `STATS_CAP 0x204` for the RMON lanes): adding one would be a CSR contract change owing a `VERSION` bump at default settings, which the prune round did not spend. The declaration lives in the build config (`board.features`) and in the generated `build_plan.md`. **Consequence for a reader:** at `0x8F8` you cannot tell "no servo built" from "servo idle at internal clock", and at `0x870` you cannot tell "no taps built" from "taps never armed" -- check the build plan, not the register. |
| The VERSION row below is a chronological landing record, not the canonical current feature verdict. Issue #97 supersedes the `0x004F` note's claim that every stopped Stream Input remains observable. Use the machine-checked rows at the top of this page for current support status. |

### Notes

| Note |
|---|
| All command strobes (`STATS_CTRL[0]`, `PTP_CMD[*]`) read back 0 (self-clearing). |
| Multi-word 64-bit reads (TOD, MAC addr) are **not** atomic on the bus; for TOD use the snapshot latch, for others read hi/lo with the field stable. |
| The map is versioned by `VERSION`; additive changes bump minor and breaking changes bump major plus the integration ABI tag. |

## Memory map

![Memory map of the shipping SoC](../../docs/diagrams/memory_map.svg)

| Region | Start address | End address | Size | Description |
|---|---|---|---|---|
| `rom` | `0x00000000` | `0x0001FFFF` | 131,072 (128 KiB) | Boot ROM holding the bare-metal firmware image. |
| `spiflash` | `0x01000000` | `0x01FFFFFF` | 16,777,216 (16 MiB) | Memory-mapped QSPI flash (read path). |
| `spiflash` AEM image slot | `0x01400000` | `0x0140FFFF` | 65,536 (64 KiB) | Flash slot of the AEM entity image. |
| `spiflash` saved-state journal | `0x01EE0000` | `0x01EFFFFF` | 131,072 (128 KiB) | Flash slots of the saved-state journal (A and B); a reflash must not erase it. |
| `spiflash` user range | `0x01F00000` | `0x01FFFFFF` | 1,048,576 (1 MiB) | Reserved user flash range. |
| `sram` | `0x10000000` | `0x10001FFF` | 8,192 (8 KiB) | On-chip SRAM: the firmware's stack and data. |
| `main_ram` | `0x40000000` | `0x7FFFFFFF` | 1,073,741,824 (1 GiB) | DDR3 main memory. |
| `main_ram` processor window | `0x7F700000` | `0x7F7FFFFF` | 1,048,576 (1 MiB) | The protocol processor's reserved main-memory window. |
| `main_ram` descriptor image | `0x7F700000` | `0x7F7DEFFF` | 913,408 (892 KiB) | AEM descriptor image, read by the processor. |
| `main_ram` saved-state stage | `0x7F7DF000` | `0x7F7EEFFF` | 65,536 (64 KiB) | Saved-state private stage, written by the firmware only. |
| `main_ram` saved-state live window | `0x7F7EF000` | `0x7F7FEFFF` | 65,536 (64 KiB) | Saved-state live window the backend reads and writes. |
| `main_ram` AECP response buffer | `0x7F7FF000` | `0x7F7FFFFF` | 4,096 (4 KiB) | AECP response buffer, written by the processor. |
| `milan_csr` | `0x90000000` | `0x9000FFFF` | 65,536 (64 KiB) | The Milan CSR block this page documents. |
| `csr` | `0xF0000000` | `0xF000FFFF` | 65,536 (64 KiB) | LiteX CSR banks. |
| `clint` | `0xF0010000` | `0xF001FFFF` | 65,536 (64 KiB) | RISC-V core-local interruptor. |
| `plic` | `0xF0C00000` | `0xF0FFFFFF` | 4,194,304 (4 MiB) | RISC-V platform-level interrupt controller. |

### Milan CSR modules

| Module | Start address | End address | Size | Description |
|---|---|---|---|---|
| [0x000 - Identification / IRQ](#0x000-----identification--irq) | `0x90000000` | `0x900000FF` | 256 | Identification, capabilities and the interrupt registers. |
| [0x100 - MAC control / status (REQ-MAC-01..03)](#0x100-----mac-control--status--req-mac-0103) | `0x90000100` | `0x900001FF` | 256 | MAC control, link status and the inert PHY reset. |
| [0x200 - Statistics (RMON) (REQ-MAC-04)](#0x200-----statistics-rmon--req-mac-04) | `0x90000200` | `0x900002FF` | 256 | RMON counter snapshot and its capability mask. |
| [0x300 - 802.1Q classifier (REQ-CLS-01..04)](#0x300-----8021q-classifier--req-cls-0104) | `0x90000300` | `0x900003FF` | 256 | Retained classifier words; no logic reads them. |
| [0x400 - 802.1Qav CBS (per queue) (REQ-CBS-01..03)](#0x400-----8021qav-cbs-per-queue--req-cbs-0103) | `0x90000400` | `0x900004FF` | 256 | Retained per-queue CBS words; nothing reads them. |
| [0x500 - PTP hardware clock (REQ-PTP-01..04, 06)](#0x500-----ptp-hardware-clock--req-ptp-0104-06) | `0x90000500` | `0x900005FF` | 256 | PTP hardware clock control, time access and PPS alarm. |
| [0x600 - ADP advertiser (IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)](#0x600-----adp-advertiser--ieee-17221-2021--milan-v12-fr-disc-0104) | `0x90000600` | `0x90000647` | 72 | ADP identity words, the advertise strobes and status. |
| [0x648 - AECP/ACMP status + AAF talker (IEEE 1722.1 / Milan v1.2)](#0x648-----aecpacmp-status--aaf-talker--ieee-17221--milan-v12) | `0x90000648` | `0x9000067F` | 56 | AECP and ACMP status, and the flat AAF talker words. |
| [0x680 - lwSRP engine (802.1Q MSRP/MVRP, Milan v1.2 Section 5.6, FR-SRP-*)](#0x680-----lwsrp-engine--8021q-msrpmvrp-milan-v12-section-56-fr-srp-) | `0x90000680` | `0x900006A3` | 36 | SRP control and the processor's SRP status. |
| [0x6A4 - ACMP listener SM (Milan v1.2 Section 5.5 listener, FR-CONN-01)](#0x6a4-----acmp-listener-sm--milan-v12-section-55-listener-fr-conn-01) | `0x900006A4` | `0x900006FF` | 92 | Listener bind record, AVTP RX, MAAP and audio diagnostics. |
| [0x700 - RX destination-MAC TCAM filter (REQ-MAC-02)](#0x700-----rx-destination-mac-tcam-filter--req-mac-02) | `0x90000700` | `0x9000071B` | 28 | RX destination-MAC filter programming. |
| [0x71C - Link guard / MAC recovery (VERSION minor ≥ 0x0006)](#0x71c-----link-guard--mac-recovery-version-minor--0x0006) | `0x9000071C` | `0x90000723` | 8 | Link guard controls and the reset canary. |
| [0x724 - identity / playback / 802.1AS overlay](#0x724-----identity--playback--8021as-overlay) | `0x90000724` | `0x90000737` | 20 | Entity name overlay, playback filter and gPTP parent. |
| [0x738 - CRF media-clock sink (Milan v1.2 7.3, KL_crf_rx)](#0x738-----crf-media-clock-sink--milan-v12-73-kl_crf_rx) | `0x90000738` | `0x9000074F` | 24 | CRF media-clock sink control and measurements. |
| [0x750 - CRF media-clock talker (Milan v1.2 7.3.1, KL_crf_tx)](#0x750-----crf-media-clock-talker--milan-v12-731-kl_crf_tx) | `0x90000750` | `0x90000767` | 24 | CRF media-clock talker control and counters. |
| [0x768 - AECP GET_DYNAMIC_INFO scan forensics (BDBG) -- 🔴 STRUCTURAL ZERO, and the link-guard status](#0x768-----aecp-get_dynamic_info-scan-forensics-bdbg-----structural-zero-and-the-link-guard-status) | `0x90000768` | `0x90000777` | 16 | Retired scan forensics and the live link-guard status. |
| [0x778 - Clock validity: the AVTP tu verdict (VERSION minor >= 0x0016), TX arbiter and SRP domain](#0x778-----clock-validity-the-avtp-tu-verdict-version-minor--0x0016-tx-arbiter-and-srp-domain) | `0x90000778` | `0x9000079F` | 40 | Clock validity, TX arbiter supervision and the SRP domain. |
| [0x7A0 - ACMP bind-restore (saved-state fast-connect E1, Milan 5.5.3.5.2)](#0x7a0-----acmp-bind-restore--saved-state-fast-connect-e1-milan-55352) | `0x900007A0` | `0x900007B7` | 24 | Retired bind-restore port, kept as an ABI. |
| [0x7B8 - Persistence-journal ingest (saved-state fast-connect E3)](#0x7b8-----persistence-journal-ingest--saved-state-fast-connect-e3) | `0x900007B8` | `0x900007C7` | 16 | Retired journal ingest port, kept as an ABI. |
| [0x7C8 - AEM dynamic-state patch port (saved-state fast-connect E4)](#0x7c8-----aem-dynamic-state-patch-port--saved-state-fast-connect-e4) | `0x900007C8` | `0x900007D7` | 16 | Retired AEM patch port, kept as an ABI. |
| [0x7D8 - Ethernet guard](#0x7d8-----ethernet-guard) | `0x900007D8` | `0x900007DB` | 4 | The Ethernet guard kill switch. |
| [0x7DC - retired AS_PATH compatibility addresses](#0x7dc-----retired-as_path-compatibility-addresses) | `0x900007DC` | `0x900007E7` | 12 | Retired AS_PATH addresses and the live PathTrace status. |
| [0x7E8 - gPTP plane drop diagnostics](#0x7e8-----gptp-plane-drop-diagnostics) | `0x900007E8` | `0x900007EF` | 8 | gPTP plane drop counters. |
| [0x7F0 - applied gPTP timestamp latency corrections](#0x7f0-----applied-gptp-timestamp-latency-corrections) | `0x900007F0` | `0x900007FF` | 16 | The timestamp corrections the gPTP plane applies. |
| [0x800 - Indexed per-stream window](#0x800-----indexed-per-stream-window) | `0x90000800` | `0x9000086F` | 112 | Indexed window onto one stream's context. |
| [0x870 - AAF per-stage latency taps (roadmap item-11, KL_aaf_latency_taps)](#0x870-----aaf-per-stage-latency-taps--roadmap-item-11-kl_aaf_latency_taps) | `0x90000870` | `0x900008B3` | 68 | AAF per-stage latency taps. |
| [0x8B4 - RX stream-parser probe (APRB, avtp_stream_parser + milan_datapath)](#0x8b4-----rx-stream-parser-probe--aprb-avtp_stream_parser--milan_datapath) | `0x900008B4` | `0x900008C7` | 20 | The RX stream parser's pre-match view. |
| [0x8C8 - reserved target-media compatibility words](#0x8c8-----reserved-target-media-compatibility-words) | `0x900008C8` | `0x900008D3` | 12 | Retired telemetry words that read zero. |
| [0x8D4 - media-boundary slip counters (SLIP, KL_chan_map_capture)](#0x8d4-----media-boundary-slip-counters--slip-kl_chan_map_capture) | `0x900008D4` | `0x900008DB` | 8 | Media-boundary slip counters. |
| [0x8DC - render presentation state](#0x8dc-----render-presentation-state) | `0x900008DC` | `0x900008DF` | 4 | Presentation state of the selected listener. |
| [0x8E0 - AAF clock meter (#629, KL_aaf_clock_meter)](#0x8e0-----aaf-clock-meter--629-kl_aaf_clock_meter) | `0x900008E0` | `0x900008F7` | 24 | AAF media clock meter. |
| [0x8F8 - MMCM-DRP media-clock servo (Milan v1.2 7.3.4, KL_mmcm_drp_servo)](#0x8f8-----mmcm-drp-media-clock-servo--milan-v12-734-kl_mmcm_drp_servo) | `0x900008F8` | `0x900008FF` | 8 | MMCM DRP media-clock servo. |
| [0x900 - channel-map fabric (Section 6 of docs/CHANNEL_MAP_64.md, KL_chan_map_render / KL_chan_map_capture)](#0x900-----channel-map-fabric--section-6-of-docschannel_map_64md-kl_chan_map_render--kl_chan_map_capture) | `0x90000900` | `0x9000091F` | 32 | Channel-map debug write port and map RAM readback. |
| [0x920 - protocol-processor control plane (KL_pp_shadow, VERSION major 2)](#0x920-----protocol-processor-control-plane--kl_pp_shadow-version-major-2) | `0x90000920` | `0x9000093F` | 32 | Protocol-processor control plane and the saved-state window. |

## Access types

A field's code reads as access, then reset value.

| Code | Meaning |
|---|---|
| `R` | Read-only. Writes are ignored. |
| `W` | Write-only. The written value is used; a read returns 0. |
| `R/W` | Read and write. A read returns the stored value. |
| `W1C` | Write 1 to clear. Writing 0 has no effect. |
| `R/W1C` | A read returns the latched bit; writing 1 clears it. |
| `W1S` | Write 1 to trigger a one-cycle action. The bit self-clears and reads 0. |
| `R/W1S` | A read returns the bit's status; writing 1 triggers the action. |
| `RC` | Read clears. No register of this block clears on read. |
| `WO` | Write-only word whose write is the action. This block shows such words as W. |

| Reset code | Meaning |
|---|---|
| `X` | Set by the block that drives this input, not by the register file. |
| `0`, `5h` | The reset value in hexadecimal; `h` marks hex digits. |

Reserved fields read as `R-0`.

A reserved `R/W` field stores bits that drive nothing.

## Build parameters

Some reset values depend on these parameters.

`milan_datapath` sets them; the export supplies its values.

| Parameter | Set from | Value |
|---|---|---|
| `NUM_QUEUES` | `NUMBER_OF_QUEUES` | 5 |
| `ADDR_WIDTH` | `16` | 16 |
| `N_LISTENERS_P` | `N_STREAMS` | 1 |
| `N_TALKERS_P` | `N_STREAMS` | 1 |
| `SRP_LSN0_ROW_P` | `SRP_LSN0_ROW_C` | 2 |
| `GPTP_PLANE_EN_P` | `GPTP_PLANE_EN_P` | 1 |
| `MILAN_CLK_FREQ_HZ_P` | `MILAN_CLK_FREQ_HZ` | 50,000,000 |
| `CHMAP_RDBK_P` | `3` | 3 |
| `PPS_P` | `PPS_P` | 0 |
| `PPS_WIDTH_CYC_P` | `PPS_WIDTH_CYC_P` | 50,000 |

## 0x000  -  Identification / IRQ

Identification, capabilities and the interrupt registers.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x000` | `ID` | Identification | `0x4D494C4E` | [section](#id-register-offset-0x000-reset--0x4d494c4e) |
| `0x004` | `VERSION` | Gateware version | `0x00020060` | [section](#version-register-offset-0x004-reset--0x00020060) |
| `0x008` | `CAP` | Capabilities | `0x00407E05` | [section](#cap-register-offset-0x008-reset--0x00407e05) |
| `0x00C` | `SCRATCH` | Scratch | `0x00000000` | [section](#scratch-register-offset-0x00c-reset--0x00000000) |
| `0x010` | `IRQ_STATUS` | Interrupt status | `0x00000000` | [section](#irq_status-register-offset-0x010-reset--0x00000000) |
| `0x014` | `IRQ_MASK` | Interrupt mask | `0x00000000` | [section](#irq_mask-register-offset-0x014-reset--0x00000000) |
| `0x018` | `IRQ_RAW` | Raw interrupt status | `0x00000000` | [section](#irq_raw-register-offset-0x018-reset--0x00000000) |

| Note |
|---|
| Group summary Identification / IRQ (global) |
| **0x0056: the verification-only gPTP form is ownerless.** The fabric plane is the sole product owner. With the plane disabled, GM, parent, PathTrace, peer-delay, sync and asCapable are zero and `tu` is one. The retained CLKV and publication addresses acknowledge writes but cannot create live state. No new CSR addresses. |
| **0x0056 also retires the general-data TX chain.** `milan_datapath` no longer instantiates the 802.1Q classifier / per-queue FIFOs / 802.1Qav CBS shaper (`traffic_controller_802_1q`) or the `ptp_ts_top` TX/RX record stampers: their only packet source was the transmit path that #259 removed, and every product source joins the trunk after the point they occupied. No address moved. The words that configured them store and read back exactly as before and reach no logic: `CLS_*` (`0x300`) and the CBS window (`0x400`-`0x49F`) are 🟡 **WRITE-ONLY SCRATCH**, and `PTP_INGRESS/EGRESS_LAT` (`0x540`/`0x544`) are readable, inert scratch (plain RW, the last written value returned; #375). Those two stay inert even now that the product APPLIES ingress and egress latency corrections (#358): the fabric gPTP plane owns them as elaboration constants and publishes what it applies at `GPTP_LAT` (`0x7F0`), because a correction two layers could each apply is a correction applied twice. Two status bits are 🔴 **STRUCTURAL ZERO**: `CAP[8]` and `IRQ_STATUS[0]`. `TXARB_DIAG` lane 1 (`aaf_final`) is a structural zero too, unrenumbered. The blocks themselves stay verified stand-alone (see [EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md)). |
| **0x0055: Table 5.22 notifications and the controller monitor are live (issue #69).** Every successful state-changing command pushes its unsolicited response to each registered controller except the requester, and a SET that stores the value already held is silent (Milan 5.4.5.2). The observed triggers feed the same scheduler: the fabric's per-descriptor counter changes reach the processor through a lossless round-robin (one push per descriptor per second), every field of the GET_AVB_INFO answer the root serves is snapshot-compared into that trigger -- the grandmaster identity, the effective propagation delay (`GPTP_PDELAY` 0x6E4, consumed for the first time), the gPTP domain number (0x62C) and the asCapable flag -- with none of the four conditioned on grandmaster presence, so a domain or delay update in the startup or GM-loss window is announced like any other; the SR class-A priority and VLAN ID are detected by the processor off the same wires it publishes. GET_AS_PATH has its own selected-owner sequence comparator and never uses the wider ADP strobe. In product fabric mode that sequence is empty without a GM, and otherwise is the committed engine pathTrace, up to eight identities from entry 0 (see 0x7DC below). The 0x7DC addresses are inert in both elaborations. The response snapshots the canonical selected path before gathering entries, so it stays on one coherent generation. Count one is `{thisClock}`, this station's own path before a peer is elected (FPGA-gPTP #82); a received sequence gains thisClock, so an explicit one-entry `[GM]` PathTrace is count two (FPGA-gPTP #85). GM=0 publications and an identical publish are silent. The `GPTP_GM_CHANGED` counter, and therefore the AVB_INTERFACE GET_COUNTERS push, move on the grandmaster identity edge alone. A write to 0x62C with a stable grandmaster is a GET_AVB_INFO trigger and an ADP re-advertise, and is neither a path-sequence change nor a gPTP GM change. Silent controllers are probed with CONTROLLER_AVAILABLE 30 to 60 s after their last command, retried once, and removed with a targeted DEREGISTER notification (5.4.5.3). No new CSRs. |
| **0x0054: generated names are live and coherent.** SET_NAME and GET_NAME serve all semantic names in the generated AEM model. The fixed response body is cdl 84 on success and refusal, SET/GET/READ_DESCRIPTOR observe one writable overlay, and generated shape data supplies the exact table capacity. Reboot persistence and unsolicited delivery remain tracked separately. No new CSRs. |
| **0x0053: the stream setters land and the fabric consumes them.** SET_STREAM_FORMAT (both directions, the per-row format verdict with mapping survival) and SET_STREAM_INFO (the Milan 5.4.2.9 sub-command at the 2021 shape) are served; the stored offset feeds the framers' transit entries and the stored format is served as current and drives the acceptance filter. No new CSRs. |
| **0x0052: start/stop completes at the record, and a stopped CRF sink observes.** START_STREAMING and STOP_STREAMING report success only after the binding-record commit or a confirmed no-op. A stopped, bound CRF sink keeps matching, validating, and counting traffic while media-clock consumption, lock progress, and restart signaling remain gated. The ACMP response validator also selects the unique_id of the consuming engine, which fixes listener responses whose talker and listener ids differ. No new CSRs. |
| The PS IRQ line = `\|(IRQ_STATUS & IRQ_MASK)`. |

### `VERSION` is also what every ATDECC controller is told (2026-07-28)

| Note |
|---|
| `0x004` is not only a version probe. It is the **single source of truth** for this gateware's version, and the ENTITY descriptor's `firmware_version` field (IEEE 1722.1-2021 7.2.1 Table 7-2, offset 116, 64 octets) is **derived** from it -- [`avdecc/gen_aem_store.py`](../../avdecc/gen_aem_store.py) `firmware_version_string()` parses the `parameter logic [31:0] VERSION` out of [`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv) and the end-station builder stamps the result into the descriptor ROM. The mapping is this table's own field split, rendered decimal, plus one component the register does not carry: |

| ATDECC `firmware_version` | source |
|---|---|
| **major** | `VERSION[31:16]` |
| **minor** | `VERSION[15:0]` -- one flat ABI ordinal, which is how this row's changelog and every `VERSION minor >=` feature gate already read it |
| **rev** | `entity.firmware_rev` in `configs/endstation_*.yaml`, optional, default `0` -- a firmware respin that changes no CSR ABI |

| Note |
|---|
| So `VERSION = 0x0002_0060` is advertised as **`2.96.0`**, and the UART `milan_status` VERSION beside Hive's entity page is the independent live check. No config declares a firmware version; the builder **refuses** the key (`entity.firmware_version`), because a second declaration is a second answer and it is the one controllers get: until 2026-07-28 all three configs said `"0.1.0"` while the fabric was at `0x0001_0016`, so every board we ship reported firmware 0.1.0 to Hive, la_avdecc and anything else enumerating it. IEEE 1722.1-2021 6.2.2.8 excludes `firmware_version` from the fields that make an entity model "changed", so bumping `VERSION` does **not** move any `entity_model_id` -- including `endstation_arty_current`'s pinned deployed identity. [`scripts/check_entity_shape.py`](../../scripts/check_entity_shape.py) is the gate. |

### ID register (offset 0x000) [reset = 0x4D494C4E]

Constant magic word that identifies the Milan CSR block.

RTL name: `A_ID`.

![ID bit fields](../../docs/diagrams/regmap/ident/ID.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ID` | R | 4D494C4Eh | Magic `"MILN"`; firmware/integration probe |

### VERSION register (offset 0x004) [reset = 0x00020060]

Major and minor version of this CSR block's ABI.

This build's VERSION is `0x0002_0060`.

RTL name: `A_VERSION`.

![VERSION bit fields](../../docs/diagrams/regmap/ident/VERSION.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `VERSION` | R | 20060h |  |

| Note |
|---|
| `[31:16]` major, `[15:0]` minor. **Versioning policy (2026-08-11): MAJOR = entire redesign of blocks -- 0x0002 opens the scenario-B era (the protocol-processor architecture of record, `protocol-processor/` submodule, replaces this plane by direct substitution at parity); MINOR = compliance fixes, flat and continuous across majors (this changelog and every `>=` feature gate key on it); the firmware string's third component (`entity.firmware_rev`) = the patch, bug-fix respins that change no CSR ABI.** Minor changelog (top entries; the RTL parameter comment in `milan_csr.sv` carries the newest) (****0x0054 = GENERATED NAMES ARE LIVE AND COHERENT. SET_NAME and GET_NAME serve every semantic name in the generated AEM model. ENTITY supports indices 0 and 1, while every other named descriptor supports index 0. Responses use the full fixed cdl 84 body on success and refusal, a locked SET returns the current name, and SET, GET, and READ_DESCRIPTOR observe one writable overlay. Generated shape data sizes the table and the store loads large tables in bounded bursts. Persistence remains issue 70; unsolicited delivery remains issue 69, with change triggers exported. NO new CSRs. Prior: 0x0053 = THE STREAM SETTERS LAND, AND THE FABRIC CONSUMES THEM. Issue 67's remainder: SET_STREAM_FORMAT (0x0008, both stream directions) and SET_STREAM_INFO (0x000E, Milan 5.4.2.9's one sub-command: a Stream Output with exactly MSRP_ACC_LAT_VALID) are served with every clause refusal -- the per-descriptor STREAM_IS_RUNNING route at dispatch (a bound Stream Input or a streaming Stream Output, 5.4.2.7/5.4.2.9), whole-command NOT_SUPPORTED on any other sub-flag, BAD_ARGUMENTS on a bit-31 offset, and ONE integrator gather that judges the PROPOSED format against the ADDRESSED ROW's declared base (the 48 kHz family for inputs, the row's own declared shape for outputs, the advertised CRF formats per direction for the CRF rows, AND every mapping-referenced channel surviving, Milan 5.4.2.7's shall) with every refusal carrying the CURRENT format. The fabric CONSUMES the settings: a set presentation offset folds into the per-STREAM_OUTPUT transit entries the AAF and CRF framers stamp (entry k is the processor's row k, the CRF output included), GET_STREAM_INFO's latency word reads the same folded entry, the served current format is the setting when one exists, and STREAM_INPUT 0's RX acceptance follows the set format. The verdict's mapping reduction sweeps the AEM dynamic-map store one key per cycle (inputs) and reads the stream-channel-keyed capture map combinationally (outputs). The wire framers do not re-shape from a stored format yet -- the SET_CONFIGURATION deferral pattern, recorded in the audit. NO new CSRs. Prior: 0x0052 = START/STOP COMPLETES AT THE RECORD, AND A STOPPED CRF SINK OBSERVES. Both halves of issue 97: START/STOP_STREAMING SUCCESS follows the ACMP binding-record commit or the confirmed no-op (a request the walker cannot start answers ENTITY_MISBEHAVING inside a bounded window, with no record side effect), and the CRF Media Clock Input's stopped state moves off the frame strobe onto KL_crf_rx's own stop port -- a stopped, bound sink keeps matching, validating and counting every Table 5.6 event while consumption gates: no settle/lock progress, the lock times out as if silent, the 10.4.3 restart echo never pulses, and the silence reset spares the sequence cursor, ring fill and mr reference so a restart fakes neither SEQ_NUM_MISMATCH nor MEDIA_RESET. CSR-observable: the 0x738 group counts on a stopped bound sink where it froze, and 0x74C's locked bit cannot rise while stopped. SAME MINOR, WIRE-FACING (found by this minor's own CRF leg): the processor's RX validator keyed every ACMP message's operand unique_id on the talker field except messages 6-11, so the TX-family RESPONSES the listener itself originates - PROBE_TX_RESPONSE above all - carried talker_unique_id instead of the listener_unique_id that addresses the record. Every prior bind used tuid == luid, masking it; the first distinct pair (the CRF sink, tuid 0x00F0 against listener uid N) had its probe answers silently consumed as out-of-range, so the bind could never SETTLE its wire identity - and a small distinct tuid would have walked the WRONG sink's record. The operand now carries the CONSUMING engine's uid: the talker for its command set, the listener for everything else, mirroring the pop steer term for term. NO new CSRs. Prior: 0x0051 = GET_DYNAMIC_INFO BATCHES FIXED GETTERS. The complete record list is validated before execution, each record reports an independent status, legal unsupported getters copy their command data, oversized responses are omitted without stopping later records, and Milan GET_STREAM_INFO records carry the required 56-byte command data. NO new CSRs. Prior: 0x0050 = AUDIO MAPPING EDITS ARE ATOMIC. ADD_AUDIO_MAPPINGS and REMOVE_AUDIO_MAPPINGS now stage and validate the complete variable-length command before any routing state changes. Input geometry, output source ownership, current stream-channel bounds, static-map scope, lock ownership, running-state restrictions, idempotent ADD, duplicate REMOVE, exact notification bodies and NVM dirty signaling are enforced. Generated topology tables keep the AEM model, protocol readback and live map projections in one coordinate system. NO new CSRs. Prior: 0x004F = STARTED/STOPPED HAS ONE SOURCE OF TRUTH, AND THE DATAPATH READS IT. Milan v1.2 SS5.3.8.7 puts two shalls on a Stream Input - a started one "shall process the incoming stream data", a stopped one "shall DISCARD the Stream AVTPDUs it receives" - and NEITHER was implemented: `aecp_strm_started_o` reached `milan_datapath` and was read by nothing, while the bit behind it lived in a dynamic-store row that had a writer and no lifecycle. The state is a property of the BINDING (the clause calls it "undefined when the Stream Input is not bound"), so it now lives in the ACMP binding record and nowhere else - cleared on unbind, captured by the NVM shadow, restored through the boot preload - PLUMBING, not the shall: `KL_pp_shadow` sets `NVM_BACKED_C = 1'b0` behind a blank-flash stub, so Section 5.3.8.7's third sentence ("saved in a non-volatile memory and restored after a power cycle") is NOT met on any shipping build. Two of the clause's three shalls land here; the persistence one waits on issue 70 - and the dynamic store's selector 6 is RETIRED rather than reused, so a second writable copy cannot return by accident. START_STREAMING (0x0022) and STOP_STREAMING (0x0023) are served for the first time (SS5.4.2.19/.20): a Stream Output, and every other descriptor type, answers NOT_SUPPORTED as the clause requires, a nonexistent index answers NO_SUCH_DESCRIPTOR through the ordinary locate, a different controller under lock answers ENTITY_LOCKED, and every arm - success and refusal alike - carries IEEE Figure 7-59's four bytes at cdl 16, because only NOT_IMPLEMENTED may answer at the command's own size. They reach the record through a WRITE-ONLY microISA state-port region (0x3) that stores nothing and hands the engine backpressure, so a request issued while the ACMP walker is busy is delayed rather than dropped. The holder is ONE DEEP: the wait is deferred, not bounded, and a second request arriving before the first drains still waits - a dropped one would be a false SUCCESS, the command having already settled its status. The bind is what DEFINES the state: a BIND_RX carrying STREAMING_WAIT lands stopped and one without it lands started, which is IEEE SS7.4.35's own premise (START_STREAMING exists for a stream "connected via ACMP with the STREAMING_WAIT flag set") and is what Milan Table 5.9 bit 28 reports back - 1 only for a sink that is "bound and stopped". WIRE-FACING on every board: a stopped Stream Input still RECEIVES, still matches and still counts - Table 5.6 defines FRAMES_RX and its neighbours on frames "received on this Stream Input", and the clause's own verb is discard, not ignore - while the listener ACCEPT pulse that feeds the depacketizer is gated, so the media path gets nothing. The discard is deliberately NOT at the classification table: that forges a not-bound->bound edge on the next START, and Table 5.6 makes that edge the counter RESET event, so a stop/start pair would wipe all ten counters on a sink that never unbound. And GET_STREAM_INFO's STREAMING_WAIT flag stops being a hardcoded 0 justified as "bound = started" - true only while stopped was unreachable - and reads the same bit the admission gate does, so the answer and the behaviour cannot disagree. The CRF Media Clock Input is covered too: it has no classification-table entry (`KL_crf_rx` keys on subtype), so it carries the stopped predicate on its own frame strobe, guarded on the sink existing so a shape with `crf_sink: false` cannot alias it onto AAF sink 0. Stopping that descriptor therefore unlocks the media clock after KL_crf_rx's silence timeout, which is what the clause asks for and is worth knowing before a controller sends it. COVERAGE, stated: the direction that matters for every shipping build - that the gate does NOT fire in normal operation - is held by 20+ milan_dp checks that go red if the predicate is forced true. The stop direction is NOT yet exercised: no suite binds and then stops that sink, because the sim carrying the AECP transactor does not inject CRF receive traffic. Read the claim as 'the predicate reaches it', not 'the stop has been demonstrated on it'. Two things a reader upgrading needs: the ACMP saved-binding record's LAYOUT_VER_P moves 0x01 -> 0x02, so every binding persisted by earlier firmware is REFUSED on restore rather than fast-connected into silence (those records all carry started = 0, because nothing ever wrote the bit); and the IEEE 7.5.2 unsolicited RESPONSE for these two opcodes is NOT sent - Milan Table 5.22's GET_STREAM_INFO push on a started/stopped change IS, and the 7.5.2 half is the same systemic gap the SET_* family has, tracked as issue 69. NO new CSRs.** Prior: **0x0023 SINK 0 OWNS A REAL lwSRP LISTENER ROW** -- the legacy flat pair (row 0, the `0x694` word) is the talker-0/software-owned attribute, and ACMP sink 0's TA coupling read THAT row's registrar, so a bind on sink 0 could never see the peer's Talker Advertise register against its own stream: the SM re-probed forever, no Listener Ready was ever declared, and the 5.3.7.3 licence never opened -- the 07-28..08-05 return-leg cluster, root-caused live at the inline tap. The attribute table grows ONE dedicated listener-0 row at index `L+T-1` (`SRP_LSN0_ROW_C`), fabric-provisioned by the same rotating requester the k>0 sinks use (want = ACMP-bound & engine-on & ~software-owned), declared at bind time with the DERIVED sid `{talker_entity_id, talker_unique_id}` (the probe answer re-provisions the same row with the authoritative sid/dmac per Milan v1.2 5.5.3.5.18), and sink 0's SETTLED_RSV_OK promotion (5.5.3.5.27) now reads its own row. `A_STRM_SEL` gains bit `[9]` -- the listener-0 row select (`{dir=0, idx=0}` is the park state and cannot carry the meaning) -- and `A_STRMW_SRP`'s idx-0 hard alias of `0x694` yields to it. Same pass, wire-facing on wide shapes: `KL_lwsrp_ctx_tx`'s batch walker kept a 4-bit row cursor whose `4'hF` doubled as both no-more-rows and REAL LANE 15, so any build whose extension-lane count reached 16 -- the 0x0023 8×8 + CRF + listener-0 = 17 rows -- could never serialize its top lane's attribute and re-emitted a stale row's sid in its place (found by the `milan_dp` 4c leg: the dedicated row provisioned, registered and promoted while the wire carried a two-tests-old stream_id); the sentinel moved outside the lane space (`6'd63`) and every row index in the ctx/walker path widened to 5 bits behind a ≤32-row elaboration guard. Prior: **0x0022 THE AEM STORE HAS A SECOND WRITE MASTER** -- Milan v1.2 puts eleven unconditional persistence SHALLs on a PAAD-AE, and every one of them could already be *read*; most could not be *put back*, because `KL_aecp_aem_store`'s write port had exactly one master, `KL_aecp_response_builder`'s `SET_*` write-back. No CSR reached it, and a self-addressed AECP command cannot reach it either -- the parser taps the RX path, and a unicast frame the board sends to its own MAC is never forwarded back to the sending port. The new group `0x7C8-0x7D4` is that master. Software names a **descriptor and a field**, never a byte address, and the fabric resolves the range from the same generated `WB_STRIN_FMT_ADDR_C` / `WB_STROUT_FMT_ADDR_C` / `WB_SAMPLING_RATE_C` / `WB_CLOCK_SRC_IDX_C` tables `SET_STREAM_FORMAT` itself uses, so regenerating a config can never leave a boot script pointing at a stale offset. The payload runs through the **same acceptance the AECP setter applies**, because a restore that installs a format the entity does not declare as supported is a worse conformance break than the revert it fixes. And the whole group is **refused -- never queued** -- while `ADP_CTRL[0]` is set, which turns "replay before the entity advertises" from an init-script convention into a property of the hardware. Closes 5.3.8.1, 5.3.7.1, 5.3.5.1 and the descriptor half of 5.3.11.1; 5.3.7.6 and 5.3.13 answer `VD_FIELD` by name because they live in response-builder register files with no slave port yet; 5.3.4.1 / 5.3.4.2 -- which require the **opposite**, being cleared by a power cycle -- are unreachable by construction, since no field code resolves to either. Prior: **0x0021 THE TSPEC DESCRIBES THE FRAME THIS BUILD EMITS** -- `0x0020` made the Talker TSpec *arithmetic* Milan's; this minor fixes its *input*. `milan_datapath` derives every talker row's MaxFrameSize from `tctx_chans_r`, a shadow of the TCTX w0 `chans` field -- and no board software writes that window, because the rows are provisioned by the fabric (`srp_fab_rec_mux`). The shadow reset to `4'd2` while `KL_aaf_packetizer` reset its own per-talker `chans_r` to the elaborated `WIRE_CHANS_C`, so on the shipping 4-channel Arty the wire carried a 120-octet AAF AVTPDU while talkers 1..N-1 **declared 73** -- 7.36 Mb/s reserved for a stream occupying 10.368, and CBS grants credit against the declaration, so the shortfall surfaces as drops under load rather than as an error anywhere. Talker 0 escaped it because the fabric mux loop starts at `s=1` and slot 0 keeps `cfg_lwsrp_max_frame` -- the same index-0-works / 1..N-1-broken signature as `0x001F`. The reset is now `aaf_chn_clamp(TALKER_WIRE_CHANS_P)`, the same parameter the framer is handed, so reservation and wire agree by construction at 2, 4 or 8 channels and a CSR write still overrides. [`tb/verilator/milan_dp`](../../tb/verilator/milan_dp) gained an `obj_nxn4c` leg elaborating the shipping Arty shape (4 streams × 4 wire channels over the TDM8+I2S blend): nothing in the suite had ever elaborated a build whose framer width differed from the shadow's reset, which is why two equal numbers hid a defect. Same pass, in [`sw/builder`](../../sw/builder): `srp_frame_geometry` gained Table 4.4's `+1` headroom octet and `srp_idle_slope_bps` now runs the clause's four steps rather than a folded `+42`, so the tool that computes the class-A ceiling and emits `cfg_lwsrp_max_frame` matches `KL_lwsrp_bw_gate`; the CRF row declares the table's 29; and the MRP LeaveTime default moved 600 → 5000 ms (Milan 4.2.7.1.1 Table 4.3), which the generated CSR defaults would otherwise have programmed back over the RTL reset. Prior: **0x0020 THE TSPEC IS MILAN'S TABLE 4.4** -- MaxFrameSize gains the octet the table mandates for sample-clock tolerance (`24*N + 24 + 1`), and the bandwidth gate runs the clause's four-step recipe including its step 2 minimum-frame clamp (`if F < 68 then F = 68`), which a folded `+42` constant had silently dropped; both errors UNDER-reserved, worst on CRF (5376 kbps against the mandated 5632). Prior: **0x001F EVERY AAF TALKER EGRESSES, WITH ITS OWN IDENTITY** -- the companion to `0x001E`: that round gave every talker row an lwSRP *declaration* and the streams still never left, because two more pieces of per-talker state had the same root cause (only the `0x800` window writes them, and no board software drives it). (1) **admission** ANDed a TCTX `CTRL[0]` shadow that reset to 0, so no talker above 0 could ever egress -- deleted, not inverted, because Milan v1.2 5.3.7.3/5.4.2.19/5.4.2.20/5.5.4.1 leave no room for a per-stream software enable on a Stream Output; `AAF_CTRL[0]` is now the one enable for every talker and the per-stream lwSRP gate is REQUIRED for t>0 (t0's `~lwsrp_enable` escape is deliberately not mirrored: `LWSRP_CTRL` resets to engine-OFF, so mirroring it would admit unpaced PROBE_TX-only streams out of reset). (2) **identity** -- the packetizer read dmac/VID/unique_id for t>0 only from that same never-written window, so an armed talker framed to dmac `00:00:00:00:00:00` on VID 0 with stream_id `{station_mac, uid 0}`, colliding with t0 and reaching no listener, while its own SRP row declared `{station_mac, uid t}` and the ACMP answer promised dmac base+t. It now DERIVES the same identity the other two publish, with software-named-wins per field. Prior: **0x001E EVERY AAF TALKER ROW IS ADVERTISED** -- the lwSRP provisioning port had exactly two writers, this `0x800` window (which **no board software drives**) and the fabric's CRF Media Clock Output row, so no AAF talker row above 0 ever held a reservation. Measured twice: `A_STRMW_SRP` `0x85C` read `0x0000_037E` at talker idx 0 -- a live hard alias of the legacy flat row, which is exactly why idx-0-only reads looked healthy -- and `0x0000_0000` at idx 1/2/3 on a 4×4 board; and a ProfiShark capture inline on the board link with a licensed stream running showed MSRP declaring a Talker Advertise for exactly `{02:00:00:00:00:02, uid 0x0000}` and `{…, uid 0x0004}` (uid 4 = `N_STREAMS` = the CRF output) and **nothing** for uid 1/2/3 -- the two stream_ids on the wire were precisely the two rows that had a provisioner. Milan v1.2 5.3.7.3 conditions streaming on declaring a Talker Advertise **and** receiving a Listener Ready/Ready Failed, so an unadvertised stream can never be licensed: no talker but 0 could stream, whatever the registrar computed. Every AAF talker row now has a fabric requester of its own -- see "AAF talker-row provisioning is FABRIC-OWNED" under the `0x800` window for the want, the derived identity and the arbitration. **Software-visible**: `SRP` and `SID_*` at talker idx>0 read a fabric-provisioned row instead of `0`, and the lwSRP provisioning record now obeys the same `{dir, idx}` staging guard the stream-table side has carried since `0x000F`, 0x001D ADP liveness is readable -- new RO `ADP_DIAG2` 0x674 (egressed-ADPDU count, discovers seen vs accepted, last message_type, `{send_pending, busy, disc_pend, available}`), because `ADP_DIAG` 0x668 reads the same `0` for a healthy advertiser and a stalled one and a 2026-07-30 bench session needed a wire capture to tell them apart; the discover-response random delay also now scales with `valid_time` per 6.2.4.2.2 (unchanged for `valid_time >= 4`, i.e. every shipped config). SAME MINOR, WIRE-FACING: the ADP re-announce period is now `MIN(5, MAX(1, valid_time/2))` seconds, the FASTER of Milan v1.2 Table 5.50 (TMR_ADVERTISE "a timer with a fixed value of 5 seconds", restarted per send by 5.6.3.5.9) and IEEE 1722.1-2021 Figure 6-2 (`MAX(1, valid_time/2)` s) -- it was `valid_time` seconds, i.e. **10.000 s measured on the wire** at the bench value and 31 s at this register's own reset value, which is why a 5 s passive discovery pass saw the entity on a coin flip; the advertised `valid_time` FIELD is unchanged. Arming is now a LEVEL (Milan 5.6.3.5.2 / 5.6.3.5.3), so an enabled entity on a live link advertises with **no pulse, no tick and no CSR toggle** and `ADP_CTRL[0] = 0` is Table 5.49 DOWN -- hence `ADP_DIAG[15:8]` rearm_cnt reads **1 after a clean boot** (the STARTUP arm) and counts the enable 0→1 recovery too. Milan Table 5.50 GM_CHANGE (5.6.3.5.7, IEEE Figure 6-5 UPDATE GM) is implemented in fabric for the first time: `gm_change_i` was tied to `1'b0`, so a grandmaster election only reached the wire at the next periodic**, 0x0002 ADP, 0x0003 TCAM, 0x0005 CRF talker, 0x0006 link guard, 0x0007 robustness round, 0x0008 indexed per-stream window 0x800, 0x0009 P12: window engine-backed, 0x000A saved-state fast-connect: bind-restore 0x7A0 + window 0x860-0x868, 0x000B chmap64 AEM projector + wire_chans fan-out + tdm_dout, 0x000C N-context ACMP talker responder -- probes answered per uid 0..N-1 with dmac = MAAP base+uid, t>0 admission mirrors t0 term-by-term, talker-window honesty + the 0xDEADDEAD not-backed rule, LTAP same-cycle cascade, 0x000D RX stream-parser probe group 0x8B4-0x8C4 -- the first pre-match listener view, 0x000E reserved in the current product, 0x000F fabric-listener blocker fix -- window sid staging is qualified by the index it was staged for, and an eviction carrying the ZERO sid is RELEASE-TO-ALIAS (entry 0 returns to the ACMP bound record at runtime), 0x0010 lwSRP attribute rows sized L+T-1 instead of max(L,T) -- every t>0 talker row was above `N_CTX_P` and refused; out-of-range rows read `0xDEAD` instead of aliasing row 0, `LWSRP_STATUS[11]` is the sticky shortfall flag, talker rows derive MaxFrameSize `24 + 24*C` from their own TCTX chans, and the CRF media clock output is a bindable ACMP talker source at `talker_unique_id = N_STREAMS`, 0x0011 **six egress queues in 802.1Q order** (higher index = higher priority): q5 CBS SR class A, q4 CBS SR class B, q3 gPTP, q2 MAAP/MSRP/MVRP + 1722.1 ADP/ACMP/AECP, q1 spare, q0 best effort -- the CBS window runs to `0x4BF`, `CAP.num_queues` reads 6, the CBS reset slopes are re-derived per queue, `CLS_TC_QUEUE_MAP` packs 3 bits/entry and resets to `0x006D2B00`, and `LWSRP_CTRL`'s class-A queue field widens to `[4:2]` with reset 5, **0x0012 the q2 `CONTROL_CLASS` row is implemented, keyed on the DESTINATION MAC** -- MAAP, MSRP, MVRP and 1722.1 ADP/ACMP/AECP are untagged link-local PDUs carrying no PCP, so at the `0x0011` reset configuration they fell through `CLS_DEFAULT_PCP` into the tables and landed on best effort; `traffic_class_map` now holds a table of reserved control group addresses (`01-80-C2-00-00-0E`, `01-80-C2-00-00-21`, `91-E0-F0-01-00-00`, `91-E0-F0-00-FF-00`) with **no EtherType precondition**, the EtherType splitting only the shared `01-80-C2-00-00-0E` (gPTP `0x88F7` → q3, MSRP `0x22EA` → q2), AECP covered by the one unicast+`0x22F0` arm, a **tagged `0x22F0` still riding the shaped SR queues**, and a new `CLS_CTRL[2]` `ctrl_class` enable that **resets to 1** so `CLS_CTRL` reads `0x5`, **0x0013 RMON is alive and self-declaring** -- `KL_mac_rmon_events` synthesises the `ethernet_events` pulse vector at the SoC's MAC boundary (frame AXIS handshakes, the MAC's per-frame bad-frame flag, and its FCS / preamble error counts), so `RX_ERROR_BAD_FCS`, `RX_ERROR_BAD_FRAME` and `RX_FIFO_BAD_FRAME` now count on LiteEth builds instead of reading a hardwired zero; the four MAC-internal lanes that genuinely have no source are declared **unsupported** in the new RO `STATS_CAP` (`0x204`) rather than faked, and `AVTPRX_STAT` / `AVTPRX_ERR` **saturate** their packed views of the 32-bit STREAM_INPUT counters instead of wrapping, **0x0014 FIVE egress queues, compactly renumbered** -- the six-queue map did not fit the xc7a100t (three Vivado seeds failed placement identically at 11955 slices required vs 11673 available, 282 short, LUTs at 99.84 % of capacity and flip-flops at 42 %), so the queue that carried no traffic -- q1, the deliberate spare -- was dropped: q4 CBS SR class A, q3 CBS SR class B, q2 gPTP, q1 MAAP/MSRP/MVRP + 1722.1 ADP/ACMP/AECP, q0 best effort. Every class keeps its rank, its shaping and its bandwidth share; gPTP still sits below both shaped classes and all queues still power up unshaped. The CBS window runs to `0x49F` and `0x4A0` reads 0, `CAP.num_queues` reads 5, the reset idleSlopes sum to 725 Mb/s = 72.5 %, `CLS_TC_QUEUE_MAP` still packs 3 bits/entry and resets to `0x004898C0`, and `LWSRP_CTRL[4:2]` keeps its width with its reset dropping from 5 to 4, **0x0015 the ADP shape registers are READ-ONLY** -- `ADP_TALKER` (`0x618`) and `ADP_LISTENER` (`0x61C`) were plain RW words resetting to zero, so the entity's advertised `talker_stream_sources` / `listener_stream_sinks` came from a hand-typed boot script; on silicon 2026-07-27 the 8×8 AX7101 advertised **1 source / 2 sinks** -- the numbers that were true at 1×1 -- beside a reference device advertising 4/10 and a peer host advertising 8/8, so every controller could see and bind ONE of its eight streams, and the CRF Media Clock Output at `talker_unique_id = N_STREAMS` was outside the advertised range and invisible to ATDECC while its PDUs were on the wire every 2 ms. Both words are now **software-DEFINED, not software-writable**: their values come from `gen/adp_shape_defaults.svh`, generated from `configs/endstation_*.yaml` by the end-station builder in the same pass that emits this shape's AEM descriptor ROM -- `0x618` = `{ADP_TALKER_CAPS_C, ADP_TALKER_SRC_C}`, `0x61C` = `{ADP_LISTENER_CAPS_C, ADP_LISTENER_SINK_C}`. There is no parameter and no register. `milan_datapath` `` `include ``-s the **same file** and sizes its ACMP talker/listener context arrays from those constants, so the advertised range is the addressable range is the descriptor set; writes are silently ignored like `CAP` and `VERSION`. The listener context count also changes from `max(N_STREAMS, 2)` -- which reserved the CRF sink only up to N = 2 and then silently dropped it -- to whatever the config says (`N + 1`); and `talker_capabilities` loses `MEDIA_CLOCK_SOURCE` at 1×1 (`0x4801` → `0x4001`) because that config has no CRF STREAM_OUTPUT to back it. [`scripts/check_entity_shape.py`](../../scripts/check_entity_shape.py) is the gate, and `build.sh`/`sweep.sh` refuse to launch unless the tracked entity definition is the config being built, **0x0017 the channel-map RAMs are READABLE** -- `CHMAP_WORD` `0x908` always read back `milan_csr`'s **own shadow** of the last word software wrote, and both map RAMs' read ports were tied off in `milan_datapath` (`map_rd_en_i = 1'b0`, `map_rd_data_o ()`), so nothing about the deployed channel map was observable from software -- a capture slot that is mapped but has never been fed emits `24'd0`, bit-identical to a slot that is working and quiet, which is exactly the structural zero that must read UNSUPPORTED instead. New `CHMAP_SNAP` `0x910` (W1S arm + busy/valid/timeout/unsupported/armed, the `CHMAP_RDBK_P` capability in `[9:8]`, and a **constant `0xC5`** tag so a read of 0 means the gateware predates the register) and `CHMAP_LOOP` `0x914` (the word the RAM actually holds, with `[18]` `LOOP_SUSPECT` = mapped & ~fed). The un-armed state is **`0xDEADDEAD`, not 0** -- `0` is a legal map entry, so the `0x800` window's "reads 0 until SNAP is armed" trap is deliberately not repeated. New elaboration parameter `CHMAP_RDBK_P` defaults to 0 ("no readback port in this build"), and a 15-clock watchdog holds that declaration to the wire: a side declared present that does not answer sets timeout and leaves the data word poisoned, **0x0016 the AVTP `tu` bit is driven and the 0x778 clock-validity group exists to drive it** -- until this minor every talker stamped `tu = 0` unconditionally, measured on 2026-07-27 streaming 31 M AAF frames from a PHC 216,446 s out of the gPTP domain while telling the listener the timestamps were fine; Milan v1.2 5.3.7.3 forbids stopping the Stream Output and IEEE 1722-2016 7.5 forbids `tv = 0` on AAF at `sp = 0`, so `tu` is the only conformant lever and Milan v1.2 4.3.5.2 makes setting it a **shall**. New: `CLKV_CTRL` `0x778`, `CLKV_STAT` `0x77C`, `CLKV_TUCNT` `0x780`. **Behaviour change on every board**: the reset state is `tu = 1`, so a build whose software never leases the sync claim emits `tu = 1` on every AAF and CRF frame -- deliberate, because unknown clock state means NOT valid), **0x0018 `AAF_CTRL` resets `0x0002_0002` → `0x0002_0000`** -- bit 1 is `cfg_aaf_bypass` and it ORs past BOTH qualifying terms of the AAF admission gate, so its set-at-reset state made every board stream unconditionally from power-on before any software ran; Milan v1.2 5.3.7.3's licence is CONDITIONAL ("as long as … RECEIVING A LISTENER READY …") and the repo's own traceability had flattened the clause into the unconditional half, so the defect and its justification were one mis-restated sentence -- a legacy bring-up build must now ASK for the bypass (measured on silicon: bypass set with nothing bound = 15,503 tagged AAF frames in 6 s, cleared = 0, bound = 18,012 -- gating costs a bound stream nothing), **0x0019 the compliance round that closes the 07-27/28 silicon findings in fabric** -- the saved-state journal-ingest group `A_JNL_CTRL/DATA/STAT/SEQ` `0x7B8-0x7C4` (Milan 5.3.8.2/.3: boot replay pushes a CRC-32-verified image through `0x7B8` and the FABRIC refuses torn/foreign/stale images whole), the 5.3.7.3 silence fill (a bound talker frames zero-carrying pairs wherever the audio interface does not feed it, so "no ADC on this board" is no longer "no frames"), per-index Milan GET_COUNTERS (Table 5.4 talker blocks from `KL_talker_diag_ctx`, every sink's Table 5.16 set from the all-context mirror), the CRF Media Clock Output as a REAL class-A stream (C-TAG + shaped queue + fabric-provisioned lwSRP talker row), the SRP-only talker licence (5.5.2.7: a registered Listener Ready starts streaming with NO ACMP involvement), and `CBS_QUEUES_MASK_P` (see the `0x400` note), **0x001C dynamic audio mapping on EVERY listener stream port** -- Milan v1.2 5.3.3.9 is a shall and it is plural ("The Stream Port Input of a Configuration shall not contain any AUDIO_MAP descriptor. Note: this means that a PAAD-AE implements dynamic mappings on all of its Stream Port Inputs"), but the fabric engine served exactly one port (`STREAM_PORT_INPUT[0]`) and no shipped config armed it, so every listener port advertised a static `AUDIO_MAP` and `ADD_AUDIO_MAPPINGS` (`0x2C`) / `REMOVE_AUDIO_MAPPINGS` (`0x2D`) answered `NOT_SUPPORTED` everywhere -- a controller could not re-route a received channel at runtime at all. The `` `AEM_DYNMAP `` store is now keyed by the GLOBAL cluster index (the addressed port's `base_cluster` + the record's port-relative `mapping_cluster_offset`), which is exactly the render crossbar's map-RAM address, so the model, the fabric and the `0x900` debug window share one index space; `GET_AUDIO_MAP` pages each port's own fixed partition, an entry carries `mapping_stream_index` (1722.1-2021 Table 7-33: any Stream Input may feed any port) and the 5.4.2.27 channel bound follows THAT stream's current format. [`configs/endstation_arty_4x4.yaml`](../../configs/endstation_arty_4x4.yaml) and [`configs/endstation_ax7101_8x8.yaml`](../../configs/endstation_ax7101_8x8.yaml) now ship `map_mode: dynamic` on every listener, so those images advertise `number_of_maps=0` per `STREAM_PORT_INPUT` and **their render crossbar powers up unmapped** (no non-volatile plane behind the list -- 5.3.10.1's restore-after-power-cycle is a recorded deviation); `endstation_arty_current` stays static so the tracked entity definition is byte-identical. Same pass: the projector's write into the render map RAM is now GATED on `addr < CHMAP_PHYS_C` instead of truncated to `$clog2(CHMAP_PHYS_C)` bits -- with 64 keys against 10 physical channels, key 16 would have aliased onto the I2S L channel) |

### CAP register (offset 0x008) [reset = 0x00407E05]

Constant capability flags and the queue-window geometry.

RTL name: `A_CAP`.

![CAP bit fields](../../docs/diagrams/regmap/ident/CAP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:24 | `RESERVED` | R | 0 | Reserved. |
| 23:16 | `BITS23_16` | R | 40h | ts_width |
| 15 | `BIT15` | R | 0 |  |
| 14 | `BIT14` | R | 1h | LWSRP |
| 13 | `BIT13` | R | 1h | TCAM |
| 12 | `BIT12` | R | 1h | ADP |
| 11 | `BIT11` | R | 1h | RX-filter |
| 10 | `BIT10` | R | 1h | STATS |
| 9 | `BIT9` | R | 1h | PTP |
| 8 | `BIT8` | R | 0 | CBS - 🔴 **STRUCTURAL ZERO** since `0x0056`: no shaper is elaborated |
| 7:4 | `RESERVED` | R | 0 | Reserved. |
| 3:0 | `NUM_QUEUES` | R | 5h | num_queues (the retained `0x400` window geometry, 5) |

### SCRATCH register (offset 0x00C) [reset = 0x00000000]

Read/write word for bus liveness tests.

RTL name: `A_SCRATCH`.

![SCRATCH bit fields](../../docs/diagrams/regmap/ident/SCRATCH.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `SCRATCH` | R/W | 0 | R/W scratch (bus liveness test) |

### IRQ_STATUS register (offset 0x010) [reset = 0x00000000]

Latched interrupt events, cleared by writing 1.

RTL name: `A_IRQ_STATUS`.

![IRQ_STATUS bit fields](../../docs/diagrams/regmap/ident/IRQ_STATUS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:3 | `RESERVED` | R | 0 | Reserved. |
| 2 | `EVT_RMON_ROLLOVER` | R/W1C | 0 |  |
| 1 | `EVT_LINK_CHANGE` | R/W1C | 0 |  |
| 0 | `RESERVED` | R | 0 | Reserved. |

| Note |
|---|
| `[0]` tx_ts_ready - 🔴 **STRUCTURAL ZERO** since `0x0056` (the TX record stamper that pulsed it is gone; the bit never sets and its W1C is inert), `[1]` link_change, `[2]` rmon_rollover |

### IRQ_MASK register (offset 0x014) [reset = 0x00000000]

Enables each interrupt source onto the IRQ line.

RTL name: `A_IRQ_MASK`.

![IRQ_MASK bit fields](../../docs/diagrams/regmap/ident/IRQ_MASK.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `IRQ_MASK` | R/W | 0 | 1 = interrupt enabled; masked bits still visible in `IRQ_RAW` |

### IRQ_RAW register (offset 0x018) [reset = 0x00000000]

Latched interrupt events before masking.

RTL name: `A_IRQ_RAW`.

![IRQ_RAW bit fields](../../docs/diagrams/regmap/ident/IRQ_RAW.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:3 | `RESERVED` | R | 0 | Reserved. |
| 2 | `EVT_RMON_ROLLOVER` | R | 0 |  |
| 1 | `EVT_LINK_CHANGE` | R | 0 |  |
| 0 | `RESERVED` | R | 0 | Reserved. |

| Note |
|---|
| Latched event bits before masking |

## 0x100  -  MAC control / status  `(REQ-MAC-01..03)`

MAC control, link status and the inert PHY reset.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x100` | `MAC_CTRL` | MAC control | `0x00000013` | [section](#mac_ctrl-register-offset-0x100-reset--0x00000013) |
| `0x104` | `MAC_IFG` | MAC inter-frame gap | `0x0000000C` | [section](#mac_ifg-register-offset-0x104-reset--0x0000000c) |
| `0x108` | `MAC_ADDR_LO` | Station MAC address, low word | `0x00000000` | [section](#mac_addr_lo-register-offset-0x108-reset--0x00000000) |
| `0x10C` | `MAC_ADDR_HI` | Station MAC address, high word | `0x00000000` | [section](#mac_addr_hi-register-offset-0x10c-reset--0x00000000) |
| `0x110` | `MAC_STATUS` | MAC link status | `0x0000000X` | [section](#mac_status-register-offset-0x110-reset--0x0000000x) |
| `0x114` | `MC_HASH_LO` | Multicast hash, low word | `0x00000000` | [section](#mc_hash_lo-register-offset-0x114-reset--0x00000000) |
| `0x118` | `MC_HASH_HI` | Multicast hash, high word | `0x00000000` | [section](#mc_hash_hi-register-offset-0x118-reset--0x00000000) |
| `0x11C` | `PHY_RESET` | PHY reset (inert) | `0x00000001` | [section](#phy_reset-register-offset-0x11c-reset--0x00000001) |

| Note |
|---|
| Group summary MAC control / status |
| `MAC_CTRL` reset `0x13` = tx_en+rx_en+is_1g (preserves today's tied constants). |
| Bare-metal firmware publishes PHY state into LiteX `milan_mac.link_status`, but only while the saved-state writer runs (`phy_link_tick()` runs inside `nvm_heartbeat_tick()`); otherwise MAC_STATUS keeps its reset value: link up, 1000 Mb/s, full duplex. It reads Clause-22 link, speed and duplex over bit-bang MDIO. The existing CDC carries this publication to MAC_STATUS. Fabric LINK_UP and LINK_DOWN counters consume the resulting link edges. The PHY polling budget is documented in the [firmware contract](../integration/BAREMETAL_FIRMWARE.md#saved-state-the-flash-writer). Physical switch-cycle acceptance is recorded in the [#599 link-cycle finding](../findings/599_394_E1_LINK_CYCLES.md). |
| **Link rate (REQ-MAC-03).** The effective `is_1g` follows the MAC's reported speed (`MAC_STATUS[2:1] == 2`) unless `MAC_CTRL[5]` is set. `MAC_CTRL[4]`'s reset value is 1, so before 2026-07-26 a 100 Mb/s port reported gigabit to every `is_1g` consumer until software wrote the register - and `is_1g` sets the lwSRP bandwidth-gate admission limit (750 vs 75 Mb/s) and the CBS sendSlope denominator, so a 100 Mb/s port admitted reservations against a 10x-too-large budget. `MAC_CTRL[5]` exists to pin the rate by hand when the MAC's speed report cannot be trusted. |
| **RX address filter (REQ-MAC-02).** `promisc`/`allmulti`/`MAC_ADDR_*`/`MC_HASH_*` are consumed by `rx_mac_filter` in the RX AXIS path, but only once `TCAM_CTRL[1]` (`addr_filter_en`, reset 0) is set - a build that never sets it keeps the legacy blanket `TCAM_CTRL[0]` miss policy. Decision order per frame: |
| a 1-beat runt is always swallowed; |
| `promisc` → accept (it outranks even an explicit TCAM drop entry - a capture must see the wire, and filtering is exactly what promiscuous mode switches off); |
| a TCAM hit → `ACTION[0]` decides; |
| `addr_filter_en` → broadcast accepted; **group** address accepted if `allmulti` **or** its hash bucket is set; **unicast** accepted only on an exact match with `MAC_ADDR_HI/LO`; |
| otherwise `TCAM_CTRL[0]`. |
| **Multicast hash function.** Bucket = a 6-bit XOR fold of the 48-bit destination MAC in standard notation, MSB-aligned groups of six bits: `bucket = a[47:42] ^ a[41:36] ^ a[35:30] ^ a[29:24] ^ a[23:18] ^ a[17:12] ^ a[11:6] ^ a[5:0]`. Bare-metal firmware must compute the same fold (`01-80-C2-00-00-0E` → `0x0180C200000E` → bucket 23, i.e. `MC_HASH_LO` bit 23). The hash is approximate by design (many addresses share a bucket); the `0x700` TCAM is the exact alternative. |

### MAC_CTRL register (offset 0x100) [reset = 0x00000013]

MAC enables, receive filtering modes and the link-rate override.

RTL name: `A_MAC_CTRL`.

![MAC_CTRL bit fields](../../docs/diagrams/regmap/mac/MAC_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:6 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 5 | `MAC_IS_1G_SELECT` | R/W | 0 |  |
| 4 | `MAC_IS_1G` | R/W | 1h |  |
| 3 | `MAC_ALLMULTI` | R/W | 0 |  |
| 2 | `MAC_PROMISC` | R/W | 0 |  |
| 1 | `MAC_RX_EN` | R/W | 1h |  |
| 0 | `MAC_TX_EN` | R/W | 1h |  |

| Note |
|---|
| `[0]` tx_en, `[1]` rx_en, `[2]` promisc, `[3]` allmulti, `[4]` is_1g (only consulted when `[5]` is set), `[5]` speed_manual (0 = derive the link rate from `MAC_STATUS` speed, 1 = use `[4]` verbatim - REQ-MAC-03, reset 0) |

### MAC_IFG register (offset 0x104) [reset = 0x0000000C]

Inter-frame gap in bytes.

RTL name: `A_MAC_IFG`.

![MAC_IFG bit fields](../../docs/diagrams/regmap/mac/MAC_IFG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:8 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 7:0 | `MAC_IFG` | R/W | Ch | inter-frame gap (bytes), default 12 |

### MAC_ADDR_LO register (offset 0x108) [reset = 0x00000000]

Station MAC address bits 31 to 0.

RTL name: `A_MAC_ALO`.

![MAC_ADDR_LO bit fields](../../docs/diagrams/regmap/mac/MAC_ADDR_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `MAC_ADDR` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| station MAC `[31:0]` - **LSB-first**: wire byte 0 in `[7:0]`, byte 3 in `[31:24]` (a plain `memcpy` of the 6-byte address into two LE words) |

### MAC_ADDR_HI register (offset 0x10C) [reset = 0x00000000]

Station MAC address bits 47 to 32.

RTL name: `A_MAC_AHI`.

![MAC_ADDR_HI bit fields](../../docs/diagrams/regmap/mac/MAC_ADDR_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `MAC_ADDR` | R/W | 0 | Bits [47:32] of the RTL value. |

| Note |
|---|
| station MAC `[47:32]` in `[15:0]` - wire byte 4 in `[7:0]`, byte 5 in `[15:8]` |

### MAC_STATUS register (offset 0x110) [reset = 0x0000000X]

Link, speed and duplex as the SoC publishes them.

RTL name: `A_MAC_STATUS`.

![MAC_STATUS bit fields](../../docs/diagrams/regmap/mac/MAC_STATUS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:4 | `RESERVED` | R | 0 | Reserved. |
| 3 | `FULL_DUPLEX` | R | X | full_duplex |
| 2:1 | `SPEED` | R | X | speed (0=10,1=100,2=1000) |
| 0 | `LINK_UP` | R | X | link_up |

| Note |
|---|
| The three bits mirror the LiteX `milan_mac_link_status` CSR, synchronised into the datapath clock (`sw/litex/milan_soc.py`, the `link_status` CSRStorage). Its reset value is link up, 1000 Mb/s on GMII (100 on MII) and full duplex, so this word reads `0x0000000D` on the AX7101 until firmware writes the CSR. |
| Firmware writes that CSR from MDIO only while the saved-state writer runs; otherwise the reset value stays. The word does not follow the link on its own. For the link, read `LINKG_STAT` (0x774), the AVB_INTERFACE LINK_UP and LINK_DOWN counters, or the PHY's BMSR over MDIO. |

### MC_HASH_LO register (offset 0x114) [reset = 0x00000000]

Multicast hash filter buckets 0 to 31.

RTL name: `A_MC_LO`.

![MC_HASH_LO bit fields](../../docs/diagrams/regmap/mac/MC_HASH_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `MC_HASH` | R/W | 0 | multicast hash filter, buckets 0-31 (bit `n` = bucket `n`) Bits [31:0] of the RTL value. |

### MC_HASH_HI register (offset 0x118) [reset = 0x00000000]

Multicast hash filter buckets 32 to 63.

RTL name: `A_MC_HI`.

![MC_HASH_HI bit fields](../../docs/diagrams/regmap/mac/MC_HASH_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `MC_HASH` | R/W | 0 | multicast hash filter, buckets 32-63 Bits [63:32] of the RTL value. |

### PHY_RESET register (offset 0x11C) [reset = 0x00000001]

Stored PHY reset bit that the shipping SoC leaves unconnected.

RTL name: `A_PHY_RST`.

![PHY_RESET bit fields](../../docs/diagrams/regmap/mac/PHY_RESET.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. A write is dropped while `ETH_GUARD[0]` is 1. |
| 0 | `PHY_RESET_N` | R/W | 1h | Drives `o_phy_reset_n` (0 = reset asserted). The shipping SoC leaves that datapath output unconnected, so this bit resets nothing. The PHY reset that reaches the pin is the LiteX `milan_mac_phy_crg_reset` CSR (the PHY clock/reset block's `_reset` storage, `sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch`), for the port the image is built for (`--eth-port`). A write is dropped while `ETH_GUARD[0]` is 1. |

## 0x200  -  Statistics (RMON)  `(REQ-MAC-04)`

RMON counter snapshot and its capability mask.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x200` | `STATS_CTRL` | Statistics control | `0x00000000` | [section](#stats_ctrl-register-offset-0x200-reset--0x00000000) |
| `0x204` | `STATS_CAP` | Statistics capability | `0xXXXXXXXX` | [section](#stats_cap-register-offset-0x204-reset--0xxxxxxxxx) |
| `0x210` | `STATn` | RMON counter snapshot | `0x00000000` | [section](#statn-registers-offset-0x210-to-0x230-stride-0x4-reset--0x00000000) |

| Note |
|---|
| Group summary Statistics (RMON) |
| Counters mirror `ethernet_events`. Software writes `STATS_CTRL[0]=1` to latch a **coherent snapshot** of all counters into the read window, then reads them. |
| **Invalidate-on-MAC-reset (2026-07-22):** a MAC reinit (link-guard episode or `LINK_CTRL[1]`) restarts the MAC path *without* a CSR-domain reset, so a pre-reset snapshot would keep serving stale counts (the 2026-07-19 "CSR plane lies until live counters tick" forensics). |
| The reinit **release** edge now zeroes `STAT0..8` in hardware; all-zero means "no valid snapshot" - software re-arms with a fresh `STATS_CTRL[0]` write. Plain-RW config registers are unaffected (they are not MAC-domain state; the aresetn-swept defaults ROM already covers full fabric resets). |
| Order follows the `ethernet_events_t` enum in [`hdl/common/eth_event_counter/ethernet_events.svh`](../../hdl/common/eth_event_counter/ethernet_events.svh); `STAT`*n* is counter lane *n* (`counts_o[n*32 +: 32]`) at offset `0x210 + 4*n`, so the HW packing and the ABI stay 1:1. |
| **READ `STATS_CAP` (`0x204`) BEFORE BELIEVING A ZERO.** A zero STAT word means one of two very different things, and until VERSION `0x0013` software could not tell them apart: |
| the lane counted, and nothing went wrong -- good news; |
| the lane has **no event source in this build** -- no news at all. |
| `STATS_CAP` bit *n* = 1 says lane *n* at `0x210 + 4n` is real. Bit *n* = 0 says it is structurally silent, and a UI must render it "not supported", never "0 errors". This is the register that would have made the 2026-07-22 defect visible from software on day one: with `i_mac_events` tied to `0`, *every* lane read zero on both boards for months while every testbench passed. |
| **Lane sources.** Two lanes are derived *inside* `milan_datapath` from its MAC AXIS boundary handshake (one accepted `tlast` beat = one frame) -- the matching bits of the `i_mac_events` port are ignored, so an external MAC can never double-count them, and those two lanes are supported on every integration by construction. The rest arrive through `i_mac_events`, which on the LiteX/LiteEth SoCs is now driven by `KL_mac_rmon_events` ([`hdl/common/eth_event_counter/KL_mac_rmon_events.sv`](../../hdl/common/eth_event_counter/KL_mac_rmon_events.sv)) from what LiteEth actually exposes at that boundary: |

| lane | source | in `STATS_CAP` on a LiteEth build |
|---|---|---|
| `TX_FIFO_GOOD_FRAME` | datapath MAC-TX AXIS accepted `tlast` | ✅ |
| `RX_FIFO_GOOD_FRAME` | datapath MAC-RX AXIS accepted `tlast` | ✅ |
| `RX_ERROR_BAD_FCS` | LiteEth `crc_errors` (CRC32 checker) | ✅ |
| `RX_ERROR_BAD_FRAME` | LiteEth `preamble_errors` (preamble/alignment) | ✅ |
| `RX_FIFO_BAD_FRAME` | frames delivered with LiteEth's `error` flag set -- FCS failure **or** undersize runt | ✅ |
| `TX_ERROR_UNDERFLOW` | none -- MAC-internal, not exposed | ❌ |
| `TX_FIFO_OVERFLOW` | none -- MAC-internal, not exposed | ❌ |
| `TX_FIFO_BAD_FRAME` | none -- MAC-internal, not exposed | ❌ |
| `RX_FIFO_OVERFLOW` | none -- MAC-internal, not exposed | ❌ |

| Note |
|---|
| The four unsupported lanes are deliberately **not** synthesised from AXIS backpressure: `rx_tvalid & ~rx_tready` is the datapath stalling the MAC, which is the *precursor* to an RX FIFO overflow rather than an overflow, and counting it as one would swap a lying zero for a lying count. |
| A CSR-only / simulation elaboration with no MAC attached reports `STATS_CAP` `0x108` (the two derived good-frame lanes only); a board build with the LiteEth MAC reports `0x1B8`. |
| Note `RX_FIFO_GOOD_FRAME` counts every frame crossing the boundary, including ones `RX_FIFO_BAD_FRAME` flags -- the datapath's derivation has no visibility of the MAC's verdict, so *good* here means *delivered*, and the two lanes are a superset/subset pair rather than a partition. |

### STATS_CTRL register (offset 0x200) [reset = 0x00000000]

Snapshot and reset strobes for the RMON counters.

RTL name: `A_STATS_CTRL`.

![STATS_CTRL bit fields](../../docs/diagrams/regmap/stats/STATS_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `RESERVED` | R | 0 | Reserved. |
| 1 | `STATS_RESET` | W1S | 0 | reset-counters |
| 0 | `STATS_SNAPSHOT` | W1S | 0 | snapshot (W1S, self-clear) |

### STATS_CAP register (offset 0x204) [reset = 0xXXXXXXXX]

Marks which RMON counter lanes have a real source.

RTL name: `A_STATS_CAP`.

![STATS_CAP bit fields](../../docs/diagrams/regmap/stats/STATS_CAP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STATS_CAP` | R | X |  |

| Note |
|---|
| `[8:0]` per-lane capability mask, lane *n* = `STAT` word at `0x210 + 4n`; 1 = real counter, 0 = structurally silent. **Live**, not snapshot-latched: `STATS_CTRL[0]` does not affect it. `[31:9]` reserved 0 |

### STATn registers (offset 0x210 to 0x230, stride 0x4) [reset = 0x00000000]

Snapshot of one RMON counter, latched by STATS_CTRL.

RTL name: `A_STATS_BASE to A_STATS_END (stat_snap)`.

![STATn bit fields](../../docs/diagrams/regmap/stats/STATn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STAT_SNAP` | R | 0 |  |

| n | Offset | Name | Producer reset | Description |
|---|---|---|---|---|
| 0 | `0x210` | `STAT_TX_ERROR_UNDERFLOW` | `0` | TX underflow -- no source, see `STATS_CAP` |
| 1 | `0x214` | `STAT_TX_FIFO_OVERFLOW` | `0` | TX FIFO overflow -- no source, see `STATS_CAP` |
| 2 | `0x218` | `STAT_TX_FIFO_BAD_FRAME` | `0` | TX FIFO bad frame -- no source, see `STATS_CAP` |
| 3 | `0x21C` | `STAT_TX_FIFO_GOOD_FRAME` | `0` | frames transmitted OK |
| 4 | `0x220` | `STAT_RX_ERROR_BAD_FRAME` | `0` | RX preamble/alignment errors |
| 5 | `0x224` | `STAT_RX_ERROR_BAD_FCS` | `0` | RX FCS errors |
| 6 | `0x228` | `STAT_RX_FIFO_OVERFLOW` | `0` | RX FIFO overflow -- no source, see `STATS_CAP` |
| 7 | `0x22C` | `STAT_RX_FIFO_BAD_FRAME` | `0` | RX frames delivered flagged bad (FCS failure or runt) |
| 8 | `0x230` | `STAT_RX_FIFO_GOOD_FRAME` | `0` | frames received OK |

## 0x300  -  802.1Q classifier  `(REQ-CLS-01..04)`

Retained classifier words; no logic reads them.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x300` | `CLS_CTRL` | Classifier control (scratch) | `0x00000005` | [section](#cls_ctrl-register-offset-0x300-reset--0x00000005) |
| `0x304` | `CLS_DEFAULT_PCP` | Classifier default PCP (scratch) | `0x00000000` | [section](#cls_default_pcp-register-offset-0x304-reset--0x00000000) |
| `0x308` | `CLS_PCP_TC_MAP` | PCP to traffic-class map (scratch) | `0x00FAC688` | [section](#cls_pcp_tc_map-register-offset-0x308-reset--0x00fac688) |
| `0x30C` | `CLS_PRIO_REGEN` | Priority regeneration (scratch) | `0x00FAC688` | [section](#cls_prio_regen-register-offset-0x30c-reset--0x00fac688) |
| `0x310` | `CLS_TC_QUEUE_MAP` | Traffic-class to queue map (scratch) | `0x004898C0` | [section](#cls_tc_queue_map-register-offset-0x310-reset--0x004898c0) |

| Note |
|---|
| Group summary 802.1Q classifier |
| 🟡 **WRITE-ONLY SCRATCH since VERSION `0x0056`.** The classifier is not instantiated in the shipping datapath (the general-data TX chain left with the transmit path, #259 - see the `0x000` note), so every word below stores and reads back exactly as documented and reaches no logic. The tables describe the retained `traffic_class_map`/`traffic_classifier` blocks, which the `classifier`/`cls` suites verify stand-alone. |
| \* `0xFAC688` is the **identity** PCP→TC map (TC `p` = `p`), so at reset the traffic class *is* the PCP and `CLS_TC_QUEUE_MAP` alone decides the queue. The Table 8-5 collapse for a station with fewer than 8 classes is the integrator's to program via `tc mqprio` (see `REQ-CLS-04`). |
| **These tables only route TAGGED traffic.** An untagged frame has no PCP, so `eff_pcp` is `CLS_DEFAULT_PCP` -- one value for the whole port. The control protocols (gPTP, MSRP, MVRP, 1722.1 ADP/ACMP/AECP, MAAP) are untagged link-local frames and are therefore **not** classified here at all; they are classified on their reserved **destination MAC address**. Do not read the q2/q1 rows of [EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md) as PCP assignments. |
| **gPTP fast path.** EtherType `0x88F7` short-circuits the tables and always lands on `GPTP_CLASS` = **q2**, i.e. *below* the CBS-shaped q4/q3. That is deliberate and is a correctness requirement, not a preference -- see [the "Why gPTP sits below the shaped classes" section of EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md#why-gptp-sits-below-the-shaped-classes). With `CLS_CTRL[1]` set the fast path also demands the reserved DMAC (`REQ-CLS-07`). |
| **Control fast path (`REQ-CLS-10`, `CLS_CTRL[2]`, reset 1).** An **untagged** frame addressed to one of the reserved control group addresses `01-80-C2-00-00-0E` (MSRP), `01-80-C2-00-00-21` (MVRP), `91-E0-F0-01-00-00` (ADP/ACMP) or `91-E0-F0-00-FF-00` (MAAP) short-circuits the tables to `CONTROL_CLASS` = **q1**, in both classifier modes. A table row hit needs **no EtherType** -- that is deliberate, so that RSTP (Bridge Group Address `01-80-C2-00-00-00`, and no EtherType at all: a BPDU is an 802.3/LLC frame) can later be added as a row rather than a redesign. The EtherType refines exactly one address: `01-80-C2-00-00-0E` carries gPTP *and* MSRP, and the gPTP arm wins first so `0x88F7` goes to q2 while `0x22EA` stays on q1. AECP has no group address (it is addressed to the peer entity's unicast MAC), so it is covered by one EtherType-keyed arm -- untagged `0x22F0` to an individual address. A **tagged** `0x22F0` is an AVTP stream and is untouched by all of this: it keeps its PCP and rides q4/q3. Full argument, including why the bit ships **on**, in [EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md). |

### CLS_CTRL register (offset 0x300) [reset = 0x00000005]

Retained classifier control word; no logic reads it.

RTL name: `A_CLS_CTRL`.

![CLS_CTRL bit fields](../../docs/diagrams/regmap/cls/CLS_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLS_CTRL` | R/W | 5h |  |

| Note |
|---|
| `[0]` use_pcp (1 = classify by PCP table, 0 = legacy EtherType), `[1]` dmac_check (1 = the 0x88F7 gPTP fast path also demands DMAC `01-80-C2-00-00-0E`; a spoofed 0x88F7 then falls to the PCP tables / BEST_EFFORT instead of taking the priority queue - REQ-CLS-07, **reset 0**), `[2]` ctrl_class (1 = untagged frames to a reserved control group address, and untagged `0x22F0` to a unicast address, take `CONTROL_CLASS` = q1 - REQ-CLS-10, **reset 1**; clearing it restores VERSION `0x0011` wire behaviour bit-for-bit, modulo the `0x0014` renumbering) |

### CLS_DEFAULT_PCP register (offset 0x304) [reset = 0x00000000]

Retained default-priority word; no logic reads it.

RTL name: `A_CLS_DPCP`.

![CLS_DEFAULT_PCP bit fields](../../docs/diagrams/regmap/cls/CLS_DEFAULT_PCP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLS_DPCP` | R/W | 0 |  |

| Note |
|---|
| `[2:0]` default port priority for untagged frames |

### CLS_PCP_TC_MAP register (offset 0x308) [reset = 0x00FAC688]

Retained PCP to traffic-class map; no logic reads it.

RTL name: `A_CLS_MAP`.

![CLS_PCP_TC_MAP bit fields](../../docs/diagrams/regmap/cls/CLS_PCP_TC_MAP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLS_MAP` | R/W | FAC688h | PCP→traffic-class, 8×3 bits: TC of PCP `p` = `[3p+2:3p]` |

### CLS_PRIO_REGEN register (offset 0x30C) [reset = 0x00FAC688]

Retained priority regeneration map; no logic reads it.

RTL name: `A_CLS_REGEN`.

![CLS_PRIO_REGEN bit fields](../../docs/diagrams/regmap/cls/CLS_PRIO_REGEN.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLS_REGEN` | R/W | FAC688h | priority regeneration, 8×3 bits (ingress PCP→internal prio). Reset was `0x688FAC` until 2026-07-05 - a half-swap (0..3↔4..7) that misrouted every tagged SR frame; fixed to identity. |

### CLS_TC_QUEUE_MAP register (offset 0x310) [reset = 0x004898C0]

Retained traffic-class to queue map; no logic reads it.

RTL name: `A_CLS_TCQ`.

![CLS_TC_QUEUE_MAP bit fields](../../docs/diagrams/regmap/cls/CLS_TC_QUEUE_MAP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLS_TCQ` | R/W | 4898C0h | TC→queue, 8×`ceil(log2 N)` bits. At `N`=5 that is still 3 bits/entry and the reset is the 5-queue map: TC0/1→q0, TC2→**q3** (SR class B), TC3→**q4** (SR class A), TC4/5→q1 (control), TC6/7→q2 (gPTP). Every queue is mapped -- there is no spare. An entry naming a queue ≥ `N` is **clamped to q0** by `traffic_class_map` (without the clamp `axis_demux` would silently drop the frame -- `select >= M_COUNT`); 5 is not a power of two either, so the clamp is still load-bearing. |

## 0x400  -  802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`

Retained per-queue CBS words; nothing reads them.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x400` | `CBS_IDLE_SLOPEn` | CBS idleSlope (scratch) | `see table` | [section](#cbs_idle_slopen-registers-offset-0x400-to-0x480-stride-0x20-reset--see-table) |
| `0x404` | `CBS_HI_CREDITn` | CBS hiCredit (scratch) | `see table` | [section](#cbs_hi_creditn-registers-offset-0x404-to-0x484-stride-0x20-reset--see-table) |
| `0x408` | `CBS_LO_CREDITn` | CBS loCredit (scratch) | `see table` | [section](#cbs_lo_creditn-registers-offset-0x408-to-0x488-stride-0x20-reset--see-table) |
| `0x40C` | `CBS_CTRLn` | CBS control (scratch) | `0x00000000` | [section](#cbs_ctrln-registers-offset-0x40c-to-0x48c-stride-0x20-reset--0x00000000) |

Reset image per queue, from `CBS_IDLE_RST`, `CBS_HI_RST`, `CBS_LO_RST` and `CBS_EN_RST`.

| q | class | idleSlope | % of 1 Gb/s | hiCredit | loCredit | shaped |
|---|---|---|---|---|---|---|
| 4 | SR class A (CBS) | 450 Mb/s | 45 % | 684 | -837 | 0 |
| 3 | SR class B (CBS) | 150 Mb/s | 15 % | 228 | -1293 | 0 |
| 2 | gPTP | 50 Mb/s | 5 % | 76 | -1445 | 0 |
| 1 | control (MAAP/MSRP/MVRP, ADP/ACMP/AECP) | 50 Mb/s | 5 % | 76 | -1445 | 0 |
| 0 | best effort | 25 Mb/s | 2.5 % | 38 | -1483 | 0 |

| Note |
|---|
| Group summary 802.1Qav CBS (per-queue, stride `0x20`; `0x400`-`0x49F` at `N`=5) |
| 🟡 **WRITE-ONLY SCRATCH since VERSION `0x0056`.** No `credit_based_shaper` is elaborated in the shipping datapath (`CAP[8]` reads 0): the window keeps its five-queue geometry, its documented reset image and its readback so no board script breaks, and nothing consumes it. The semantics below are the retained `traffic_shaping_core`'s, verified by the `cbs`/`shaper_core` suites. |
| Per queue `q ∈ [0,N)` at `0x400 + q*0x20`: |
| From VERSION `0x0019` to `0x0055` the shipped builds elaborated `CBS_QUEUES_MASK_P = 0x10` (derived by the builder from `srp.class_queue`): only the class-A queue carried a `credit_based_shaper` instance. Since `0x0056` the parameter and its `--cbs-queues-mask` knob are gone with the chain; every row is inert the way the masked rows always were, and the `shaper_core` suite's dual-core oracle still proves a masked queue bit-identical to an unshaped built one for the retained block. |
| Reset defaults (`milan_csr` `CBS_*_RST`, mirroring `ethernet_packet_pkg.sv`). **Indexed by queue**, so row 0 is q0 = best effort and row 4 is q4 = SR class A -- the table used to run the other way round, because q0 used to be the highest-priority queue: |

| q | class | idleSlope | % of 1 Gb/s | hiCredit | loCredit | shaped |
|---|---|---|---|---|---|---|
| 4 | SR class A (CBS) | 450 Mb/s | 45 % | 684 | −837 | 0 |
| 3 | SR class B (CBS) | 150 Mb/s | 15 % | 228 | −1293 | 0 |
| 2 | gPTP | 50 Mb/s | 5 % | 76 | −1445 | 0 |
| 1 | control (MAAP/MSRP/MVRP, ADP/ACMP/AECP) | 50 Mb/s | 5 % | 76 | −1445 | 0 |
| 0 | best effort | 25 Mb/s | 2.5 % | 38 | −1483 | 0 |

| Note |
|---|
| Σ idleSlope = 725 Mb/s = 72.5 % of the 1 Gb/s port rate, under the 75 % `REQ-CBS-03` ceiling; the two shaped classes alone are 600 Mb/s = 60 %, which is the figure 802.1Q-2018 Section 34.3.1 actually constrains. Every class keeps the share it had in the 6-queue map -- the 2.5 % that belonged to the dropped spare is deliberately left **unallocated** rather than reassigned, because `REQ-CBS-03` is a ceiling and moving it would change a live class's provisioning for no reason. hi/lo are `calc_hi/lo_credit(idleSlope, 1e9)` for MAX_FRAME_SIZE = 1522. The 100 Mb/s table (`IDLE_SLOPE_100M`) is the same shares of 100 Mb/s. |
| **ALL queues power up unshaped** (`CBS_EN_RST = 0b00000`): the default class map routes untagged/BE traffic to q0, and shaping q0 at reset silently paced all best-effort TX to ~250 Mbit/s (measured on silicon 2026-07-07, see [CBS_DATAPATH_BUG.md](../findings/CBS_DATAPATH_BUG.md)). Software opts a queue in via `CBS_CTRL[0]` (REQ-CBS-02: SR classes only, never BE). |
| Write semantics: |
| The HW clamps credit down immediately if a write lowers hiCredit below the current credit, so shrinking a burst allowance takes effect at once. |
| An `CBS_IDLE_SLOPE` write takes effect within two slope-engine passes, at most 200 datapath cycles = 4 us in the shipping 50 MHz profile (2 us in the 100 MHz AX bring-up profile) (`credit_based_shaper.sv slope_engine`, sequential divider since 2026-07-11); hiCredit/loCredit/shaped-enable act on the next cycle. |
| Configuration must keep Σ idleSlope of the *shaped* queues ≤ 75 % of the port rate. |
| **Shaping applies per queue, not globally.** A frame is credit-based-shaped **only when both** hold: |
| its PCP maps - through `CLS_PRIO_REGEN` → `CLS_PCP_TC_MAP` → `CLS_TC_QUEUE_MAP` - to a queue, **and** |
| that queue's `CBS_CTRL[0]` shaped-enable is **1**. |
| A queue with `CBS_CTRL[0]=0` (or a PCP that maps to it) is **strict priority / unshaped** (`allow_transmit` forced 1 in `credit_based_shaper.sv`). At reset **no queue is shaped** (`CBS_EN_RST = 0b00000`, see the reset-defaults note above). Software chooses which queues are SR/shaped (subject to the 75 % Σ idleSlope budget) by programming the PCP→queue map and the per-queue enables together - e.g. `tc mqprio` + `tc cbs offload`. |

### CBS_IDLE_SLOPEn registers (offset 0x400 to 0x480, stride 0x20) [reset = see table]

Retained idleSlope word for one queue; nothing reads it.

RTL name: `A_CBS_BASE + 0x0 + 0x20 * q (CBS_IDLE_RST)`.

![CBS_IDLE_SLOPEn bit fields](../../docs/diagrams/regmap/cbs/CBS_IDLE_SLOPEn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CBS_IDLE` | R/W | see table | idleSlope, bits/s (sendSlope = idleSlope − portRate, derived in HW) |

| n | Offset | Reset |
|---|---|---|
| 0 | `0x400` | `0x017D7840` |
| 1 | `0x420` | `0x02FAF080` |
| 2 | `0x440` | `0x02FAF080` |
| 3 | `0x460` | `0x08F0D180` |
| 4 | `0x480` | `0x1AD27480` |

### CBS_HI_CREDITn registers (offset 0x404 to 0x484, stride 0x20) [reset = see table]

Retained hiCredit word for one queue; nothing reads it.

RTL name: `A_CBS_BASE + 0x4 + 0x20 * q (CBS_HI_RST)`.

![CBS_HI_CREDITn bit fields](../../docs/diagrams/regmap/cbs/CBS_HI_CREDITn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CBS_HI` | R/W | see table | hiCredit, signed bytes |

| n | Offset | Reset |
|---|---|---|
| 0 | `0x404` | `0x00000026` |
| 1 | `0x424` | `0x0000004C` |
| 2 | `0x444` | `0x0000004C` |
| 3 | `0x464` | `0x000000E4` |
| 4 | `0x484` | `0x000002AC` |

### CBS_LO_CREDITn registers (offset 0x408 to 0x488, stride 0x20) [reset = see table]

Retained loCredit word for one queue; nothing reads it.

RTL name: `A_CBS_BASE + 0x8 + 0x20 * q (CBS_LO_RST)`.

![CBS_LO_CREDITn bit fields](../../docs/diagrams/regmap/cbs/CBS_LO_CREDITn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CBS_LO` | R/W | see table | loCredit, signed bytes |

| n | Offset | Reset |
|---|---|---|
| 0 | `0x408` | `0xFFFFFA35` |
| 1 | `0x428` | `0xFFFFFA5B` |
| 2 | `0x448` | `0xFFFFFA5B` |
| 3 | `0x468` | `0xFFFFFAF3` |
| 4 | `0x488` | `0xFFFFFCBB` |

### CBS_CTRLn registers (offset 0x40C to 0x48C, stride 0x20) [reset = 0x00000000]

Retained shaping enable for one queue; nothing reads it.

RTL name: `A_CBS_BASE + 0xC + 0x20 * q (CBS_EN_RST)`.

![CBS_CTRLn bit fields](../../docs/diagrams/regmap/cbs/CBS_CTRLn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R | 0 | Reserved. |
| 0 | `CBS_EN` | R/W | 0 | shaped-enable (0 = strict priority, credit forced eligible) |

## 0x500  -  PTP hardware clock  `(REQ-PTP-01..04, 06)`

PTP hardware clock control, time access and PPS alarm.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x500` | `PTP_CTRL` | PTP clock control | `0x00000001` | [section](#ptp_ctrl-register-offset-0x500-reset--0x00000001) |
| `0x504` | `PTP_INCR` | PTP increment | `0x14000000` | [section](#ptp_incr-register-offset-0x504-reset--0x14000000) |
| `0x508` | `PTP_ADJ` | PTP fine adjustment | `0x00000000` | [section](#ptp_adj-register-offset-0x508-reset--0x00000000) |
| `0x510` | `PTP_TOD_WR_LO` | PTP settime target, low word | `0x00000000` | [section](#ptp_tod_wr_lo-register-offset-0x510-reset--0x00000000) |
| `0x514` | `PTP_TOD_WR_HI` | PTP settime target, high word | `0x00000000` | [section](#ptp_tod_wr_hi-register-offset-0x514-reset--0x00000000) |
| `0x518` | `PTP_OFFSET_LO` | PTP adjtime offset, low word | `0x00000000` | [section](#ptp_offset_lo-register-offset-0x518-reset--0x00000000) |
| `0x51C` | `PTP_OFFSET_HI` | PTP adjtime offset, high word | `0x00000000` | [section](#ptp_offset_hi-register-offset-0x51c-reset--0x00000000) |
| `0x520` | `PTP_CMD` | PTP command | `0x00000000` | [section](#ptp_cmd-register-offset-0x520-reset--0x00000000) |
| `0x530` | `PTP_TOD_RD_LO` | PTP time snapshot, low word | `0x00000000` | [section](#ptp_tod_rd_lo-register-offset-0x530-reset--0x00000000) |
| `0x534` | `PTP_TOD_RD_HI` | PTP time snapshot, high word | `0x00000000` | [section](#ptp_tod_rd_hi-register-offset-0x534-reset--0x00000000) |
| `0x540` | `PTP_INGRESS_LAT` | Ingress latency (scratch) | `0x00000000` | [section](#ptp_ingress_lat-register-offset-0x540-reset--0x00000000) |
| `0x544` | `PTP_EGRESS_LAT` | Egress latency (scratch) | `0x00000000` | [section](#ptp_egress_lat-register-offset-0x544-reset--0x00000000) |
| `0x548` | `PTP_PPS_CTRL` | PPS alarm control | `0x00000000` | [section](#ptp_pps_ctrl-register-offset-0x548-reset--0x00000000) |
| `0x54C` | `PTP_PPS_TGT_LO` | PPS target, low word | `0x00000000` | [section](#ptp_pps_tgt_lo-register-offset-0x54c-reset--0x00000000) |
| `0x550` | `PTP_PPS_TGT_HI` | PPS target, high word | `0x00000000` | [section](#ptp_pps_tgt_hi-register-offset-0x550-reset--0x00000000) |
| `0x554` | `PTP_PPS_RD_LO` | PPS live target, low word | `0xXXXXXXXX` | [section](#ptp_pps_rd_lo-register-offset-0x554-reset--0xxxxxxxxx) |
| `0x558` | `PTP_PPS_RD_HI` | PPS live target, high word | `0xXXXXXXXX` | [section](#ptp_pps_rd_hi-register-offset-0x558-reset--0xxxxxxxxx) |
| `0x55C` | `PTP_PPS_WIDTH` | PPS pulse width | `0xXXXXXXXX` | [section](#ptp_pps_width-register-offset-0x55c-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary PTP hardware clock |
| `PTP_PPS_*` is a PURE COMPARATOR in the PHC's own clock domain (issue #260), not an engine product: `hit = (phc_ns >= target)`, and on a hit the target advances by **exactly** `1e9` rather than by "now + 1e9". That is what keeps the error from integrating - each rising edge lands within one counter increment of its second boundary, and the residue of one edge is not carried into the next. That bound is on the compare's own sample. The pin is a register on the far side of it, so the edge at the pad is a further clock period late (under 16 ns in all at 125 MHz) plus the pad and trace delay. Those terms are a fixed offset to calibrate out once, not a term that grows per pulse. Only the rising edge carries time. The alarm is **two separate gates**: `PPS_P` decides whether the logic exists at all (default off, ~150-200 LUT when on), and `PTP_PPS_CTRL[0]` decides whether a built comparator ever fires. Arming a target that is already in the past is defined, not undefined: the comparator hits every tick and the target catches up at `1e9` ns per tick until it passes the clock. |
| Both latency words reset to 0 = uncorrected, and both were the register half of REQ-PTP-06 for the record stampers the retired target consumed. The fabric gPTP plane stamps its own frames (`KL_gptp_gmii_launch` at the MAC's own transmit stream since #360, `KL_gptp_shadow` off the RX tap) and does not read these words; its reference-plane offset is #117's physical measurement, not a CSR constant (gh #64: the ingress/egress SPLIT was never measured, only their sum). |

### PTP_CTRL register (offset 0x500) [reset = 0x00000001]

Enables the PTP hardware clock counter.

RTL name: `A_PTP_CTRL`.

![PTP_CTRL bit fields](../../docs/diagrams/regmap/ptp/PTP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 0 | `PTP_ENABLE` | R/W | 1h | counter enable |

### PTP_INCR register (offset 0x504) [reset = 0x14000000]

Nominal clock increment per tick, Q8.24 nanoseconds.

RTL name: `A_PTP_INCR`.

![PTP_INCR bit fields](../../docs/diagrams/regmap/ptp/PTP_INCR.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_INCR` | R/W | 14000000h |  |

| Note |
|---|
| nominal increment per tick, **Q8.24** ns: `[31:24]` integer ns, `[23:0]` fractional ns. Reset value = the true PHC clock period, derived from `MILAN_CLK_FREQ_HZ_P` (`0x14000000` = 20.0 ns in the shipping 50 MHz Milan domain; `0x0A000000` = 10.0 ns in the 100 MHz AX bring-up shape; the standalone-default 125 MHz gives the historic `0x08000000`) |

### PTP_ADJ register (offset 0x508) [reset = 0x00000000]

Signed addend applied on every tick.

RTL name: `A_PTP_ADJ`.

![PTP_ADJ bit fields](../../docs/diagrams/regmap/ptp/PTP_ADJ.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_ADJ` | R/W | 0 | signed Q8.24-ns adjfine addend added to `PTP_INCR` each tick (rate discipline) |

### PTP_TOD_WR_LO register (offset 0x510) [reset = 0x00000000]

Time-of-day target for settime, bits 31 to 0.

RTL name: `A_PTP_TWLO`.

![PTP_TOD_WR_LO bit fields](../../docs/diagrams/regmap/ptp/PTP_TOD_WR_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_TOD_WR` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| settime target `[31:0]` (ns) |

### PTP_TOD_WR_HI register (offset 0x514) [reset = 0x00000000]

Time-of-day target for settime, bits 63 to 32.

RTL name: `A_PTP_TWHI`.

![PTP_TOD_WR_HI bit fields](../../docs/diagrams/regmap/ptp/PTP_TOD_WR_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_TOD_WR` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| settime target `[63:32]` |

### PTP_OFFSET_LO register (offset 0x518) [reset = 0x00000000]

Signed adjtime delta, bits 31 to 0.

RTL name: `A_PTP_OFLO`.

![PTP_OFFSET_LO bit fields](../../docs/diagrams/regmap/ptp/PTP_OFFSET_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_OFFSET` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| adjtime signed delta `[31:0]` |

### PTP_OFFSET_HI register (offset 0x51C) [reset = 0x00000000]

Signed adjtime delta, bits 63 to 32.

RTL name: `A_PTP_OFHI`.

![PTP_OFFSET_HI bit fields](../../docs/diagrams/regmap/ptp/PTP_OFFSET_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_OFFSET` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| adjtime signed delta `[63:32]` |

### PTP_CMD register (offset 0x520) [reset = 0x00000000]

Strobes that apply settime, adjtime or a time snapshot.

RTL name: `A_PTP_CMD`.

![PTP_CMD bit fields](../../docs/diagrams/regmap/ptp/PTP_CMD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:3 | `RESERVED` | R | 0 | Reserved. |
| 2 | `PTP_CMD_SNAPSHOT` | W1S | 0 | snapshot (latch TOD for gettime) - self-clearing pulses |
| 1 | `PTP_CMD_ADJUST` | W1S | 0 | adjust (apply adjtime) |
| 0 | `PTP_CMD_LOAD` | W1S | 0 | load (apply settime) |

### PTP_TOD_RD_LO register (offset 0x530) [reset = 0x00000000]

Time of day latched by the last snapshot, low word.

RTL name: `A_PTP_TRLO`.

![PTP_TOD_RD_LO bit fields](../../docs/diagrams/regmap/ptp/PTP_TOD_RD_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_TOD_RD` | R | 0 |  |

| Note |
|---|
| latched TOD `[31:0]` (updated when the PHC snapshot returns) |

### PTP_TOD_RD_HI register (offset 0x534) [reset = 0x00000000]

Time of day latched by the last snapshot, high word.

RTL name: `A_PTP_TRHI`.

![PTP_TOD_RD_HI bit fields](../../docs/diagrams/regmap/ptp/PTP_TOD_RD_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_TOD_RD` | R | 0 |  |

| Note |
|---|
| latched TOD `[63:32]` |

### PTP_INGRESS_LAT register (offset 0x540) [reset = 0x00000000]

Readable inert scratch; corrections are published at GPTP_LAT.

RTL name: `A_PTP_ILAT`.

![PTP_INGRESS_LAT bit fields](../../docs/diagrams/regmap/ptp/PTP_INGRESS_LAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_ILAT` | R/W | 0 | 🟡 **Readable, inert scratch since `0x0056`.** A read returns the last written value; no timestamp-correction consumer reads the word at this VERSION. The live owner since `0x005E` is the fabric gPTP plane, which applies its board's correction as an elaboration constant and publishes the applied pair at `GPTP_LAT` (`0x7F0`); this word stays scratch so the same correction cannot be applied by two owners (#358). Ingress latency correction, ns, that the `ptp_ts_core` RX tap **SUBTRACTED** from its captures; that tap is no longer instantiated |

### PTP_EGRESS_LAT register (offset 0x544) [reset = 0x00000000]

Readable inert scratch; corrections are published at GPTP_LAT.

RTL name: `A_PTP_ELAT`.

![PTP_EGRESS_LAT bit fields](../../docs/diagrams/regmap/ptp/PTP_EGRESS_LAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PTP_ELAT` | R/W | 0 | 🟡 **Readable, inert scratch since `0x0056`.** A read returns the last written value; no timestamp-correction consumer reads the word at this VERSION. The live owner since `0x005E` is the fabric gPTP plane, which applies its board's correction as an elaboration constant and publishes the applied pair at `GPTP_LAT` (`0x7F0`); this word stays scratch so the same correction cannot be applied by two owners (#358). Egress latency correction, ns, that the TX tap **ADDED**; that tap is no longer instantiated |

### PTP_PPS_CTRL register (offset 0x548) [reset = 0x00000000]

PPS enable, arm strobe and the built capability bit.

RTL name: `A_PPS_CTRL`.

![PTP_PPS_CTRL bit fields](../../docs/diagrams/regmap/ptp/PTP_PPS_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:17 | `RESERVED` | R | 0 | Reserved. |
| 16 | `PPS_P` | R | 0 |  |
| 15:2 | `RESERVED` | R | 0 | Reserved. |
| 1 | `PPS_ARM` | W1S | 0 |  |
| 0 | `PPS_ENABLE` | W | 0 |  |

| Note |
|---|
| PPS alarm control, minor >= `0x0059`. `[0]` **RW** runtime enable - 0 = the comparator is idle and the pin stays low. `[1]` **W1S** arm: load `PTP_PPS_TGT_{HI,LO}` into the live target, self-clearing, reads 0. `[16]` **RO** *built*: 1 only when the gateware elaborated the comparator (`PPS_P`). Read `[16]` before believing `[0]` - on a pruned build `[0]` reads back 0 however it is written, so "no pulses" is diagnosable without a scope. Setting `[1]` and `[0]` in one word is the normal sequence and emits no pulse before the armed boundary: the two bits reach the PHC domain by different crossings and enable arrives first, so the comparator is gated on having been armed |

### PTP_PPS_TGT_LO register (offset 0x54C) [reset = 0x00000000]

Absolute PPS target to arm, bits 31 to 0.

RTL name: `A_PPS_TGLO`.

![PTP_PPS_TGT_LO bit fields](../../docs/diagrams/regmap/ptp/PTP_PPS_TGT_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PPS_TARGET_NS` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| Target to arm, `[31:0]` (ns). Write a multiple of 1 000 000 000 in PHC time, i.e. a TAI second boundary; the hardware does no modulo and will happily fire on whatever it is given |

### PTP_PPS_TGT_HI register (offset 0x550) [reset = 0x00000000]

Absolute PPS target to arm, bits 63 to 32.

RTL name: `A_PPS_TGHI`.

![PTP_PPS_TGT_HI bit fields](../../docs/diagrams/regmap/ptp/PTP_PPS_TGT_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PPS_TARGET_NS` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| Target to arm, `[63:32]` |

### PTP_PPS_RD_LO register (offset 0x554) [reset = 0xXXXXXXXX]

Target the PHC publishes back, bits 31 to 0.

RTL name: `A_PPS_RDLO`.

![PTP_PPS_RD_LO bit fields](../../docs/diagrams/regmap/ptp/PTP_PPS_RD_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PPS_TARGET_RD_NS` | R | X | Bits [31:0] of the RTL value. |

| Note |
|---|
| **Live** target `[31:0]`, published back from the PHC clock domain. Advances by exactly `1e9` on every pulse, so two reads a second apart are the drift measurement. Structural 0 when `PPS_CTRL[16]` is 0 |

### PTP_PPS_RD_HI register (offset 0x558) [reset = 0xXXXXXXXX]

Target the PHC publishes back, bits 63 to 32.

RTL name: `A_PPS_RDHI`.

![PTP_PPS_RD_HI bit fields](../../docs/diagrams/regmap/ptp/PTP_PPS_RD_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PPS_TARGET_RD_NS` | R | X | Bits [63:32] of the RTL value. |

| Note |
|---|
| **Live** target `[63:32]` |

### PTP_PPS_WIDTH register (offset 0x55C) [reset = 0xXXXXXXXX]

PPS pulse width in PHC clock cycles.

RTL name: `A_PPS_WIDTH`.

![PTP_PPS_WIDTH bit fields](../../docs/diagrams/regmap/ptp/PTP_PPS_WIDTH.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PPS_WIDTH` | R | X | Pulse width in PHC clock **cycles**, not seconds: `width_s = PTP_PPS_WIDTH / f_PHC`, and `f_PHC` is the period `PTP_INCR` already reports. Elaborated as one millisecond of the datapath clock (`100 000` in the 100 MHz shape, `125 000` at the recommended 125 MHz). 0 when the comparator was not built |

## 0x600  -  ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`

ADP identity words, the advertise strobes and status.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x600` | `ADP_CTRL` | ADP control | `0x00000A00` | [section](#adp_ctrl-register-offset-0x600-reset--0x00000a00) |
| `0x604` | `ADP_ENTITY_ID_LO` | Entity ID, low word | `0x00000000` | [section](#adp_entity_id_lo-register-offset-0x604-reset--0x00000000) |
| `0x608` | `ADP_ENTITY_ID_HI` | Entity ID, high word | `0x00000000` | [section](#adp_entity_id_hi-register-offset-0x608-reset--0x00000000) |
| `0x60C` | `ADP_MODEL_ID_LO` | Entity model ID, low word | `0x00000000` | [section](#adp_model_id_lo-register-offset-0x60c-reset--0x00000000) |
| `0x610` | `ADP_MODEL_ID_HI` | Entity model ID, high word | `0x00000000` | [section](#adp_model_id_hi-register-offset-0x610-reset--0x00000000) |
| `0x614` | `ADP_ENTITY_CAPS` | Entity capabilities (scratch) | `0x00000000` | [section](#adp_entity_caps-register-offset-0x614-reset--0x00000000) |
| `0x618` | `ADP_TALKER` | ADP talker shape | `0x48010002` | [section](#adp_talker-register-offset-0x618-reset--0x48010002) |
| `0x61C` | `ADP_LISTENER` | ADP listener shape | `0x48010002` | [section](#adp_listener-register-offset-0x61c-reset--0x48010002) |
| `0x620` | `ADP_CONTROLLER_CAPS` | Controller capabilities (scratch) | `0x00000000` | [section](#adp_controller_caps-register-offset-0x620-reset--0x00000000) |
| `0x624` | `ADP_GPTP_GM_LO` | gPTP grandmaster, low word | `0xXXXXXXXX` | [section](#adp_gptp_gm_lo-register-offset-0x624-reset--0xxxxxxxxx) |
| `0x628` | `ADP_GPTP_GM_HI` | gPTP grandmaster, high word | `0xXXXXXXXX` | [section](#adp_gptp_gm_hi-register-offset-0x628-reset--0xxxxxxxxx) |
| `0x62C` | `ADP_GPTP_DOMAIN` | gPTP domain | `0x00000000` | [section](#adp_gptp_domain-register-offset-0x62c-reset--0x00000000) |
| `0x630` | `ADP_IDX0` | ADP indices 0 | `0x00000000` | [section](#adp_idx0-register-offset-0x630-reset--0x00000000) |
| `0x634` | `ADP_IDX1` | ADP indices 1 (scratch) | `0x00000000` | [section](#adp_idx1-register-offset-0x634-reset--0x00000000) |
| `0x638` | `ADP_ASSOC_ID_LO` | Association ID, low word (scratch) | `0x00000000` | [section](#adp_assoc_id_lo-register-offset-0x638-reset--0x00000000) |
| `0x63C` | `ADP_ASSOC_ID_HI` | Association ID, high word (scratch) | `0x00000000` | [section](#adp_assoc_id_hi-register-offset-0x63c-reset--0x00000000) |
| `0x640` | `ADP_CMD` | ADP command | `0x00000000` | [section](#adp_cmd-register-offset-0x640-reset--0x00000000) |
| `0x644` | `ADP_STATUS` | ADP status | `0xXXXXXXXX` | [section](#adp_status-register-offset-0x644-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary ADP identity (served by the protocol processor; five ADPDU fields are write-only scratch) |
| Identity and control for the ADP transmit engine -- which is now the protocol processor's `KL_adp_engine`, reached through [`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv). This repository's `adp_advertiser.sv` and `KL_adp_parser.sv` are deleted. The software AVDECC stack still programs the entity identity here, matching the selected [`configs/endstation_*.yaml`](../../configs) definition and builder-generated ENTITY descriptor. The hardware still owns the advertise timing and `available_index`. `station MAC` (source MAC / entity_id seed) comes from `MAC_ADDR_{LO,HI}`, not this group. |
| **Three things changed in this group and none of them is cosmetic.** |
| **`ADP_CTRL[0]` still enables the entity, and it is now ORed with `PP_CTRL[0]` at `0x920`.** Either bit starts the plane. `ADP_CTRL.en` is the bit every board script and bring-up recipe in this repository writes, and it used to start the ADP advertiser, the AECP listener and both ACMP halves at once; demanding the new bit as well would have stranded every existing script, and honouring only the new bit would have silently ignored the old one. |
| **Five ADPDU fields are now beyond software's reach** -- a real loss, not a tidy-up. `entity_capabilities`, `valid_time`, `association_id`, `controller_capabilities` and `interface_index` are **constants inside the processor's `KL_adp_engine`**, which exposes no port for them. Their registers below are **WRITE-ONLY SCRATCH**: the write is accepted, the readback is faithful, and the ADPDU on the wire carries the processor's value regardless. Closing that needs a new port on the submodule, which is pinned. |
| **The advertise/depart command strobes at `0x640` are also write-only scratch.** The processor takes `link_up` as a *level* and runs its own timer service, so this file no longer synthesises an edge for it; the one event that still reaches the processor is a **grandmaster change**. By default that edge comes from the fabric publication bank; in the option-off comparison it comes from the committed `0x624`/`0x628` software pair (IEEE 1722.1-2021 6.2.6 makes a gPTP grandmaster change a re-advertise event). |
| The processor emits an 82-byte ADPDU (dst `91:E0:F0:01:00:00`, EtherType `0x22F0`, subtype `0xFA`). It reaches the wire through the control lane -- `ctl_tx_mux` merges the processor's packed TX with MAAP, and `adp_tx_mux` puts the result on the MAC boundary between data frames. |
| `available_index` increments after EVERY transmitted ENTITY_AVAILABLE: periodic re-advertise and discover response alike (controllers treat a repeated index as an incoherent entity; bump-on-change-only was silicon-diagnosed 2026-07-12). An ENTITY_DEPARTING carries the current value, and the index then resets to 0 (IEEE 1722.1-2021 Section 6.2.2.15, as processor PR #152 notes), so the next ENTITY_AVAILABLE carries 0. |
| A frozen `ADP_STATUS` therefore still means no ADPDUs are leaving at all -- a retired incident signature preserved in Git history, and now the *only* liveness read in the group, because the counters that used to corroborate it are structural zeros (see `ADP_DIAG` / `ADP_DIAG2` in the `0x648` group below). |

### ADP_CTRL register (offset 0x600) [reset = 0x00000A00]

Entity enable and the advertised valid time.

RTL name: `A_ADP_CTRL`.

![ADP_CTRL bit fields](../../docs/diagrams/regmap/adp/ADP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:13 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 12:8 | `ADP_VALID_TIME` | R/W | Ah | valid_time (units of 2 s; reset 10 per Milan 5.6.2 ⇒ 20 s validity) is 🟡 **WRITE-ONLY SCRATCH** -- the processor holds valid_time as an internal constant and the ADPDU carries that, not this |
| 7:1 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 0 | `ADP_ENABLE` | R/W | 0 | advertise-enable -- **LIVE, and ORed with `PP_CTRL[0]` (`0x920`): either bit enables the entity**. |

### ADP_ENTITY_ID_LO register (offset 0x604) [reset = 0x00000000]

entity_id bits 31 to 0.

RTL name: `A_ADP_EIDLO`.

![ADP_ENTITY_ID_LO bit fields](../../docs/diagrams/regmap/adp/ADP_ENTITY_ID_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ENTITY_ID` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| entity_id `[31:0]` (EUI-64) |

### ADP_ENTITY_ID_HI register (offset 0x608) [reset = 0x00000000]

entity_id bits 63 to 32.

RTL name: `A_ADP_EIDHI`.

![ADP_ENTITY_ID_HI bit fields](../../docs/diagrams/regmap/adp/ADP_ENTITY_ID_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ENTITY_ID` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| entity_id `[63:32]` |

### ADP_MODEL_ID_LO register (offset 0x60C) [reset = 0x00000000]

entity_model_id bits 31 to 0.

RTL name: `A_ADP_MIDLO`.

![ADP_MODEL_ID_LO bit fields](../../docs/diagrams/regmap/adp/ADP_MODEL_ID_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ENTITY_MODEL_ID` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| entity_model_id `[31:0]` |

### ADP_MODEL_ID_HI register (offset 0x610) [reset = 0x00000000]

entity_model_id bits 63 to 32.

RTL name: `A_ADP_MIDHI`.

![ADP_MODEL_ID_HI bit fields](../../docs/diagrams/regmap/adp/ADP_MODEL_ID_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ENTITY_MODEL_ID` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| entity_model_id `[63:32]` |

### ADP_ENTITY_CAPS register (offset 0x614) [reset = 0x00000000]

Stored and read back; the processor supplies the ADPDU field.

RTL name: `A_ADP_ECAPS`.

![ADP_ENTITY_CAPS bit fields](../../docs/diagrams/regmap/adp/ADP_ENTITY_CAPS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ENTITY_CAPS` | R/W | 0 | 🟡 **WRITE-ONLY SCRATCH**: entity_capabilities (e.g. `0xC588` for a Milan PAAD). Stored and read back; the ADPDU carries the processor's internal constant (`ADP_ENTITY_CAPS_C` in `pp_adp_pkg.sv`). Writing it changes nothing observable. **Nothing writes it**: the bare-metal firmware no longer writes its stale `0x8588` copy (#398), so the word reads back its reset `0` |

### ADP_TALKER register (offset 0x618) [reset = 0x48010002]

Constant talker sources and capabilities from the build config.

RTL name: `A_ADP_TALK`.

![ADP_TALKER bit fields](../../docs/diagrams/regmap/adp/ADP_TALKER.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_TALK` | R | 48010002h |  |

| Note |
|---|
| `[15:0]` talker_stream_sources, `[31:16]` talker_capabilities. **Hardwired from the end-station config, writes ignored** (VERSION `0x0015`). The values live in [`hdl/common/gen/adp_shape_defaults.svh`](../../hdl/common/gen/adp_shape_defaults.svh), GENERATED from `configs/endstation_*.yaml` by [`sw/builder/endstation_builder.py`](../../sw/builder/endstation_builder.py) in the same pass that emits this shape's AEM descriptor ROM. `ADP_TALKER_SRC_C` = the `STREAM_OUTPUT` descriptor count = the AAF talkers plus the CRF Media Clock Output when the config has one, and `milan_datapath` sizes its ACMP talker context array from **the same constant**, so the advertised range is the addressable range. `1` at 1×1, `N+1` at N×N. `ADP_TALKER_CAPS_C` = `IMPLEMENTED` \| `AUDIO_SOURCE` \| `MEDIA_CLOCK_SOURCE` **only when a CRF output exists** → `0x4001` at 1×1, `0x4801` at N×N |

### ADP_LISTENER register (offset 0x61C) [reset = 0x48010002]

Constant listener sinks and capabilities from the build config.

RTL name: `A_ADP_LIST`.

![ADP_LISTENER bit fields](../../docs/diagrams/regmap/adp/ADP_LISTENER.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_LIST` | R | 48010002h |  |

| Note |
|---|
| `[15:0]` listener_stream_sinks, `[31:16]` listener_capabilities. Same generated include, same rule: `ADP_LISTENER_SINK_C` = the `STREAM_INPUT` descriptor count = the AAF sinks plus the CRF sink → `2` at 1×1, `N+1` at N×N, and it sizes the ACMP listener context array. `ADP_LISTENER_CAPS_C` = `0x4801` wherever a CRF sink exists |

### ADP_CONTROLLER_CAPS register (offset 0x620) [reset = 0x00000000]

Stored and read back; the processor supplies the ADPDU field.

RTL name: `A_ADP_CCAPS`.

![ADP_CONTROLLER_CAPS bit fields](../../docs/diagrams/regmap/adp/ADP_CONTROLLER_CAPS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_CONTROLLER_CAPS` | R/W | 0 | 🟡 **WRITE-ONLY SCRATCH** -- controller_capabilities. Stored and read back; never reaches the wire |

### ADP_GPTP_GM_LO register (offset 0x624) [reset = 0xXXXXXXXX]

Grandmaster identity bits 31 to 0, coherent with GMHI.

RTL name: `A_ADP_GMLO`.

![ADP_GPTP_GM_LO bit fields](../../docs/diagrams/regmap/adp/ADP_GPTP_GM_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `GPTP_GM_RD_SNAP` | R | X |  |

| Note |
|---|
| gptp_grandmaster_id `[31:0]`. Fabric mode snapshots the complete live 64-bit identity on the first half read and holds it through the complementary half, in either order. From reset release until a peer is elected, fabric mode reads thisClock, this instance's own clockIdentity (IEEE 802.1AS-2011 10.3.12.1.4 b), with Cor1-2013, FPGA-gPTP #82). Option OFF reads zero; writes are inert. |

### ADP_GPTP_GM_HI register (offset 0x628) [reset = 0xXXXXXXXX]

Grandmaster identity bits 63 to 32, coherent with GMLO.

RTL name: `A_ADP_GMHI`.

![ADP_GPTP_GM_HI bit fields](../../docs/diagrams/regmap/adp/ADP_GPTP_GM_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `GPTP_GM_RD_SNAP` | R | X |  |

| Note |
|---|
| gptp_grandmaster_id `[63:32]`. Fabric mode is the other half of the coherent snapshot, thisClock's high half before any peer. Option OFF reads zero; writes are inert. |

### ADP_GPTP_DOMAIN register (offset 0x62C) [reset = 0x00000000]

The gPTP domain number, a structural zero.

RTL name: `A_ADP_DOMAIN`.

![ADP_GPTP_DOMAIN bit fields](../../docs/diagrams/regmap/adp/ADP_GPTP_DOMAIN.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_DOMAIN` | R | 0 |  |

| Note |
|---|
| `[7:0]` gptp_domain_number - ADPDU byte 48. At `VERSION=0x0002_0060` this is a structural domain `0` in both fabric mode and the ownerless verification-only option-OFF build. All writes are inert; no startup publication step owns this word. |

### ADP_IDX0 register (offset 0x630) [reset = 0x00000000]

Current configuration and identify-control indices.

RTL name: `A_ADP_IDX0`.

![ADP_IDX0 bit fields](../../docs/diagrams/regmap/adp/ADP_IDX0.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `ADP_IDENTIFY_INDEX` | R/W | 0 | identify_control_index |
| 15:0 | `ADP_CURRENT_CONFIG` | R/W | 0 | current_configuration_index the ADPDU carries until a SET_CONFIGURATION or D3 restore writes the processor's configuration row, and again after a D3 roll-back (from processor pin `631eeb34`) |

### ADP_IDX1 register (offset 0x634) [reset = 0x00000000]

Stored interface index; never reaches the wire.

RTL name: `A_ADP_IDX1`.

![ADP_IDX1 bit fields](../../docs/diagrams/regmap/adp/ADP_IDX1.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `ADP_INTERFACE_INDEX` | R/W | 0 |  |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH** -- `[15:0]` interface_index. Stored and read back; never reaches the wire |

### ADP_ASSOC_ID_LO register (offset 0x638) [reset = 0x00000000]

Stored association_id bits 31 to 0; never reaches the wire.

RTL name: `A_ADP_ASLO`.

![ADP_ASSOC_ID_LO bit fields](../../docs/diagrams/regmap/adp/ADP_ASSOC_ID_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ASSOCIATION_ID` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH** -- association_id `[31:0]`. Stored and read back; never reaches the wire |

### ADP_ASSOC_ID_HI register (offset 0x63C) [reset = 0x00000000]

Stored association_id bits 63 to 32; never reaches the wire.

RTL name: `A_ADP_ASHI`.

![ADP_ASSOC_ID_HI bit fields](../../docs/diagrams/regmap/adp/ADP_ASSOC_ID_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_ASSOCIATION_ID` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH** -- association_id `[63:32]`. Stored and read back; never reaches the wire |

### ADP_CMD register (offset 0x640) [reset = 0x00000000]

Advertise-now and depart strobes.

RTL name: `A_ADP_CMD`.

![ADP_CMD bit fields](../../docs/diagrams/regmap/adp/ADP_CMD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `RESERVED` | R | 0 | Reserved. |
| 1 | `ADP_DEPART` | W1S | 0 |  |
| 0 | `ADP_ADVERTISE` | W1S | 0 |  |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH** -- `[0]` advertise-now, `[1]` depart. Both strobes are accepted, self-clear as before, and land nowhere: the processor runs its own advertise timer off a `link_up` LEVEL and there is no port to command a send. A selected-owner GM change triggers the live re-advertise path directly |

### ADP_STATUS register (offset 0x644) [reset = 0xXXXXXXXX]

The available_index the processor advertises.

RTL name: `A_ADP_STATUS`.

![ADP_STATUS bit fields](../../docs/diagrams/regmap/adp/ADP_STATUS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ADP_AVAILABLE_INDEX` | R | X |  |

| Note |
|---|
| 🟢 **LIVE, REPOINTED** -- `[31:0]` available_index, published by the protocol processor (`adp_next_avail_index_o`) and equal to the value on the wire. This is the one word of the ADP diagnostics that still measures something |

## 0x648  -  AECP/ACMP status + AAF talker  `(IEEE 1722.1 / Milan v1.2)`

AECP and ACMP status, and the flat AAF talker words.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x648` | `AECP_STAT0` | AECP status 0 | `0x000XXXXX` | [section](#aecp_stat0-register-offset-0x648-reset--0x000xxxxx) |
| `0x64C` | `AECP_STAT1` | AECP status 1 | `0xXXXXXXXX` | [section](#aecp_stat1-register-offset-0x64c-reset--0xxxxxxxxx) |
| `0x650` | `ACMP_STAT` | ACMP status | `0xXXXXXXXX` | [section](#acmp_stat-register-offset-0x650-reset--0xxxxxxxxx) |
| `0x654` | `AAF_CTRL` | AAF talker control | `0x00000000` | [section](#aaf_ctrl-register-offset-0x654-reset--0x00000000) |
| `0x658` | `AAF_DMLO` | AAF destination MAC, low word | `0xF000FE01` | [section](#aaf_dmlo-register-offset-0x658-reset--0xf000fe01) |
| `0x65C` | `AAF_DMHI` | AAF destination MAC, high word | `0x000091E0` | [section](#aaf_dmhi-register-offset-0x65c-reset--0x000091e0) |
| `0x660` | `AAF_FRAMES` | AAF frames sent | `0xXXXXXXXX` | [section](#aaf_frames-register-offset-0x660-reset--0xxxxxxxxx) |
| `0x664` | `AAF_PAIRS` | AAF pairs captured | `0xXXXXXXXX` | [section](#aaf_pairs-register-offset-0x664-reset--0xxxxxxxxx) |
| `0x668` | `ADP_DIAG` | ADP diagnostics | `0x000XXXXX` | [section](#adp_diag-register-offset-0x668-reset--0x000xxxxx) |
| `0x66C` | `ACMP_TALKER` | ACMP talker state | `0x0000000X` | [section](#acmp_talker-register-offset-0x66c-reset--0x0000000x) |
| `0x670` | `ACMP_LOBS` | Listener-observed override | `0x00000000` | [section](#acmp_lobs-register-offset-0x670-reset--0x00000000) |
| `0x674` | `ADP_DIAG2` | ADP liveness diagnostics | `0xXX00XXXX` | [section](#adp_diag2-register-offset-0x674-reset--0xxx00xxxx) |

| Note |
|---|
| Group summary AECP/ACMP status (**AECP counters are structural zeros; lock is live**) + AAF talker (flat stream-0 registers) |
| The AECP and ACMP *counter* words of this group are now **structural zeros**. The entity-lock level, AAF talker configuration, and one ACMP level are live. Read the verdict column, not the register name. |
| **The AECP lock level is live; its legacy counters and configuration field remain structural zeros.** The processor's AECP uCPU accepts and answers its declared command inventory. `ACQUIRE_ENTITY` returns Milan Delta 7 `NOT_SUPPORTED` with no owner, and configuration operations are served inside the processor. `AECP_STAT0[16]` publishes the authoritative `LOCK_ENTITY` level used to gate local map writes. Current configuration and the command and response count fields are not exported into this CSR group. Processor command, response, drop, locate-miss, last-status, last-length, image-valid, and image-fault diagnostics instead live in the **side-port snapshot window**, read through `KL_pp_shadow`'s integration bridge. Do not read a zero here as "the engine saw nothing". |
| **The ADP dormancy forensics are structural zeros too** -- depart count, re-arm count, depart cause, ADPDUs egressed, ENTITY_DISCOVERs accepted and seen, last message type and advertiser state. The processor publishes no equivalent through its class-D face, and a plausible-looking count here would be a mirror of nothing. `ADP_STATUS` `0x644` (available_index) is the surviving liveness read. |
| **`ACMP_TALKER[1]` talker_active IS live** -- it is the processor's `acmp_declaring_o`, and the DA gate is still the talker gate: it asserts only after a MAAP `ALLOC_DA` success through `KL_pp_maap_shim`, so AAF admission is still "a destination address exists AND the source is declaring". |
| **`ACMP_TALKER[0]` probe_armed is a structural zero** -- it was the deleted talker SM's "a probe window is open" level and the class-D face has no equivalent. |
| The legacy flat AAF talker configuration for stream 0 is untouched (talker index 0 of the `0x800` window is a hard alias of these -- see the alias rule there). Stream semantics: [`../overview/ARCHITECTURE.md`](../overview/ARCHITECTURE.md) and [`../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md). |

### AECP_STAT0 register (offset 0x648) [reset = 0x000XXXXX]

Entity lock level and a retired command count.

RTL name: `A_AECP_STAT0`.

![AECP_STAT0 bit fields](../../docs/diagrams/regmap/aecp/AECP_STAT0.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:17 | `RESERVED` | R | 0 | Reserved. |
| 16 | `AECP_LOCKED` | R | X |  |
| 15:0 | `AECP_CMD_COUNT` | R | X |  |

| Note |
|---|
| Mixed: `[16]` is the processor's live `LOCK_ENTITY` level. `[15:0]` is a 🔴 **STRUCTURAL ZERO** because the processor command count is not exported here |

### AECP_STAT1 register (offset 0x64C) [reset = 0xXXXXXXXX]

Retired AECP response count and configuration index.

RTL name: `A_AECP_STAT1`.

![AECP_STAT1 bit fields](../../docs/diagrams/regmap/aecp/AECP_STAT1.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `AECP_RESP_COUNT` | R | X |  |
| 15:0 | `AECP_CURRENT_CONFIG` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was `[31:16]` AECP responses sent and `[15:0]` live current configuration index. The processor sends responses and stores configuration state, but neither field is connected here |

### ACMP_STAT register (offset 0x650) [reset = 0xXXXXXXXX]

Retired ACMP command and response counts.

RTL name: `A_ACMP_STAT`.

![ACMP_STAT bit fields](../../docs/diagrams/regmap/aecp/ACMP_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `ACMP_RESP_COUNT` | R | X |  |
| 15:0 | `ACMP_CMD_COUNT` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was the ACMP responder's `[31:16]` responses sent / `[15:0]` commands accepted. ACMP itself is **alive** -- the processor answers CONNECT_TX/PROBE_TX/GET_TX_STATE and runs the BIND_RX ladder -- but it publishes a bind RECORD, not PDU counters, so these two fields have no source. Take `ACMPL_STATE[3]` bound (`0x6A4`) and `ACMP_TALKER[1]` (`0x66C`) as the truth instead |

### AAF_CTRL register (offset 0x654) [reset = 0x00000000]

AAF talker enable, gate bypass and stream VID.

RTL name: `A_AAF_CTRL`.

![AAF_CTRL bit fields](../../docs/diagrams/regmap/aecp/AAF_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:28 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 27:16 | `AAF_VID` | R/W | 0 |  |
| 15:2 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 1 | `AAF_BYPASS` | R/W | 0 |  |
| 0 | `AAF_ENABLE` | R/W | 0 |  |

| Note |
|---|
| Neutral disabled reset, including VID. Firmware owns the generated active word `MILAN_AAF_CTRL_BOOT`: `[0]` enable, `[1]` diagnostic bypass (boot clear), `[27:16]` startup VID 2. Runtime diagnostic writes remain supported. Domain adoption selects the operational tag independently. |

### AAF_DMLO register (offset 0x658) [reset = 0xF000FE01]

AAF stream destination MAC bits 31 to 0.

RTL name: `A_AAF_DMLO`.

![AAF_DMLO bit fields](../../docs/diagrams/regmap/aecp/AAF_DMLO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AAF_DEST_MAC` | R/W | F000FE01h | Bits [31:0] of the RTL value. |

| Note |
|---|
| AAF stream dest MAC `[31:0]` (reset = MAAP-range `91:E0:F0:00:FE:01`). Fallback value: while `MAAP_CTRL[0]` is set and `MAAP_STAT1[2]` addr_valid, the datapath streams to the MAAP-claimed DMAC instead (`eff_aaf_dmac` mux) |

### AAF_DMHI register (offset 0x65C) [reset = 0x000091E0]

AAF stream destination MAC bits 47 to 32.

RTL name: `A_AAF_DMHI`.

![AAF_DMHI bit fields](../../docs/diagrams/regmap/aecp/AAF_DMHI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `AAF_DEST_MAC` | R/W | 91E0h | Bits [47:32] of the RTL value. |

| Note |
|---|
| dest MAC `[47:32]` in `[15:0]` |

### AAF_FRAMES register (offset 0x660) [reset = 0xXXXXXXXX]

AAF frames the talker has sent.

RTL name: `A_AAF_FRAMES`.

![AAF_FRAMES bit fields](../../docs/diagrams/regmap/aecp/AAF_FRAMES.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AAF_FRAMES` | R | X | AAF frames sent (the window `PDUS` word latches this at talker idx 0) |

### AAF_PAIRS register (offset 0x664) [reset = 0xXXXXXXXX]

Audio sample pairs the talker front end captured.

RTL name: `A_AAF_PAIRS`.

![AAF_PAIRS bit fields](../../docs/diagrams/regmap/aecp/AAF_PAIRS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AAF_PAIRS` | R | X | I2S sample pairs captured by the talker front-end |

### ADP_DIAG register (offset 0x668) [reset = 0x000XXXXX]

Retired ADP depart and re-arm counters.

RTL name: `A_ADP_DIAG`.

![ADP_DIAG bit fields](../../docs/diagrams/regmap/aecp/ADP_DIAG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:18 | `RESERVED` | R | 0 | Reserved. |
| 17:16 | `ADP_DEPART_SRC` | R | X |  |
| 15:8 | `ADP_REARM_CNT` | R | X |  |
| 7:0 | `ADP_DEPART_CNT` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was the ADP dormancy forensics: `[7:0]` depart events, `[15:8]` dormancy self-re-arms, `[17:16]` last depart cause. The advertiser that produced them is deleted and the processor exposes no equivalent, so this reads `0` on a healthy entity and on a dead one alike -- which is exactly why it must not be read as a measurement. Use `ADP_STATUS` `0x644` (available_index) moving across two reads a re-advertise period apart |

### ACMP_TALKER register (offset 0x66C) [reset = 0x0000000X]

Talker probe, active, observed and gate bits.

RTL name: `A_ACMP_TALKER`.

![ACMP_TALKER bit fields](../../docs/diagrams/regmap/aecp/ACMP_TALKER.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:4 | `RESERVED` | R | 0 | Reserved. |
| 3 | `AAF_GATE` | R | X |  |
| 2 | `ACMP_LOBS` | R | X |  |
| 1 | `ACMP_TALKER_ACTIVE` | R | X |  |
| 0 | `ACMP_PROBE_ARMED` | R | X |  |

| Note |
|---|
| Mixed: `[0]` probe_armed is a 🔴 **STRUCTURAL ZERO** (the deleted talker SM's probe-window level; no class-D equivalent). `[1]` talker_active is 🟢 **LIVE, REPOINTED** -- the processor's `acmp_declaring_o`, which asserts only after a MAAP ALLOC_DA success. `[2]` mirror of the `ACMP_LOBS[0]` manual override, `[3]` resolved AAF admission gate -- both still real, and `[3]` is still the composed gate the datapath admits frames on |

### ACMP_LOBS register (offset 0x670) [reset = 0x00000000]

Manual listener_observed override for the AAF gate.

RTL name: `A_ACMP_LOBS`.

![ACMP_LOBS bit fields](../../docs/diagrams/regmap/aecp/ACMP_LOBS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 0 | `ACMP_LOBS` | R/W | 0 | manual listener_observed override -- OR-ed with the lwSRP-sourced listener_observed (the lwSRP socket, see the 0x680 group) |

### ADP_DIAG2 register (offset 0x674) [reset = 0xXX00XXXX]

Retired ADP liveness and discover counters.

RTL name: `A_ADP_DIAG2`.

![ADP_DIAG2 bit fields](../../docs/diagrams/regmap/aecp/ADP_DIAG2.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:28 | `ADP_STATE` | R | X |  |
| 27:24 | `ADP_LAST_MSG` | R | X |  |
| 23:16 | `ADP_DISC_SEEN_CNT` | R | 0 |  |
| 15:8 | `ADP_DISC_RX_CNT` | R | X |  |
| 7:0 | `ADP_SENT_CNT` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was ADP liveness in one read: ADPDUs egressed, ENTITY_DISCOVERs accepted and seen on the wire, last `message_type`, advertiser state. Every one of those came from `adp_advertiser.sent_cnt_o` and `KL_aecp_ingress.adp_disc_seen_o`, both deleted. The 2026-07-30 diagnosis this register was built for -- telling a stalled advertiser from a healthy one that never departed -- must now be made from `ADP_STATUS` `0x644` and a wire capture |

## 0x680  -  lwSRP engine  `(802.1Q MSRP/MVRP, Milan v1.2 Section 5.6, FR-SRP-*)`

SRP control and the processor's SRP status.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x680` | `LWSRP_CTRL` | SRP control | `0x00000010` | [section](#lwsrp_ctrl-register-offset-0x680-reset--0x00000010) |
| `0x684` | `LWSRP_VID` | SRP VID | `0x00000002` | [section](#lwsrp_vid-register-offset-0x684-reset--0x00000002) |
| `0x688` | `LWSRP_DMAC_LO` | SRP destination MAC, low word (scratch) | `0xF000FE01` | [section](#lwsrp_dmac_lo-register-offset-0x688-reset--0xf000fe01) |
| `0x68C` | `LWSRP_DMAC_HI` | SRP destination MAC, high word (scratch) | `0x000091E0` | [section](#lwsrp_dmac_hi-register-offset-0x68c-reset--0x000091e0) |
| `0x690` | `LWSRP_TSPEC` | SRP TSpec (scratch) | `0x000100E0` | [section](#lwsrp_tspec-register-offset-0x690-reset--0x000100e0) |
| `0x694` | `LWSRP_STATUS` | SRP status | `0xXXXXXXXX` | [section](#lwsrp_status-register-offset-0x694-reset--0xxxxxxxxx) |
| `0x698` | `LWSRP_SLOPE` | SRP granted slope | `0xXXXXXXXX` | [section](#lwsrp_slope-register-offset-0x698-reset--0xxxxxxxxx) |
| `0x69C` | `LWSRP_CNT` | SRP PDU counts | `0xXXXXXXXX` | [section](#lwsrp_cnt-register-offset-0x69c-reset--0xxxxxxxxx) |
| `0x6A0` | `LWSRP_LATENCY` | SRP accumulated latency | `0x00000000` | [section](#lwsrp_latency-register-offset-0x6a0-reset--0x00000000) |

| Note |
|---|
| Group summary SRP status (802.1Q MSRP/MVRP, Milan v1.2 Section 5.6) -- repointed to the protocol processor; PDU counters are structural zeros |
| **The lwSRP engine is deleted.** The whole hdl/ieee8021q/srp tree is gone -- the applicant, the registrar, the TA registrar, the walker, the ingress/RX path, the context table, the MRPDU serialiser, the timers and the bandwidth gate. SRP is now the protocol processor's, reached through [`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv): it declares Talker Advertise and Listener Ready, registers the bridge's answers, adopts the Domain and publishes the result on its class-D face, which `milan_datapath` wires straight into the words below. |
| **This group is therefore split.** The *state* words are LIVE and repointed; the *PDU accounting* and the *provisioning inputs the deleted applicant read* are not: |
| 🟢 **LIVE, REPOINTED** -- the Domain word (`LWSRP_DOM` adopted / priority / VID), the granted idleSlope (`LWSRP_SLOPE`), the over-limit bit, the stream gate, the raw admission-verdict bit, the listener/talker declaration and registration levels, and the MSRP failure code. |
| 🔴 **STRUCTURAL ZERO** -- MRPDU transmit and receive counts and ingress FIFO drops (`LWSRP_CNT`, `LWSRP_STATUS[31:24]`). That accounting lived in the deleted serialiser/ingress pair; the processor emits and consumes MRPDUs internally and publishes no counters. Also the attribute-row shortfall bit `LWSRP_STATUS[11]`: there is no attribute-row table in this fabric any more. |
| 🟡 **WRITE-ONLY SCRATCH** -- `LWSRP_DMAC_LO`/`_HI`, `LWSRP_TSPEC` (MaxFrameSize + MaxIntervalFrames) and the declare-always bypass `LWSRP_CTRL[5]`. The applicant that read them is deleted. The processor derives its own MaxFrameSize from the width the framer was elaborated with, and its own destination address from MAAP. Writing these changes nothing observable. |
| **The licence requires ACTIVE and the real per-source grant (#551).** ACTIVE includes the processor's three-published-round optimistic admission term. The real grant excludes that optimistic term. Every declaration clears its registered Listener first. An early Listener Ready can raise ACTIVE before admission completes. |
| **Admitted.** The licence opens once both terms hold. A later Listener Ready adds no admission delay. |
| **Refused, including changed TSpecs.** `LWSRP_STATUS[7]` reports ceiling refusal. ACTIVE can pulse, but the licence remains closed. No STREAM_START/STREAM_STOP pair or Table 5.4 counter reset follows. The refused re-declaration emits no PDU. ACTIVE falls when optimism expires; Talker Failed follows. |
| The processor now evaluates the current TSpec before granting admission. Every declaration clears its source's grant until that evaluation completes. A round that meets any pending declaration publishes nothing. Other grants, the slope sum and over-limit retain their published values. This follows [processor #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112), adopted through #508. |
| `CRFT_CTRL[6]`/`[7]` require the CRF source's real grant. `LWSRP_STATUS[8]` requires source 0's real grant. `LWSRP_STATUS[6]` remains raw ACTIVE ORed across sources. That raw bit can rise while every licence stays closed. The `0x82C` snapshot gate bit [3] follows the selected licence. Its lobs bit [2] follows that licence above index 0. Index 0's lobs still reports its registered Listener instead. At index 0, [27:19] mirrors `LWSRP_STATUS[8:0]`. Thus [27] requires the grant; [25] remains raw \|ACTIVE. |
| `LWSRP_STATUS[9]` remains the OR of real admission grants. `LWSRP_SLOPE` reports their sum from the last published round. After withdrawal, the sum updates at the next published round. Neither diagnostic programs a shaper; none is instantiated. See [EGRESS_QUEUE_MAP.md](EGRESS_QUEUE_MAP.md#credit-based-shaping). |
| While enabled the plane declares MSRP Domain (+ TalkerAdvertise) and the MVRP VID, registers the bridge's Listener attribute for our StreamID, and resolves the reservation into the talker gates (ACTIVE AND the real grant) and the status words above. No slope mux exists, so `LWSRP_CTRL[4:2]` selects nothing and the `0x400` CBS window stays write-only scratch. |
| While enabled it also: |
| sources ACMP `listener_observed` (OR-ed with the manual `A_ACMP_LOBS` override at 0x670), and |
| makes a reservation a PRECONDITION for AAF transmit (`FR-SRP-03`; `AAF_CTRL[1]` bypass remains the escape hatch, and since VERSION `0x0018` it is **CLEAR at reset**, so the precondition IS in force on a board nobody has told otherwise; see the `0x654` row and the [current audit](../testing/MILAN_V12_AUDIT_2026-08-16.md)). |
| `LWSRP_STATUS[8]` is the licence Milan v1.2 5.3.7.3 defines, and it is honest: it reads 0 when no Listener Ready / Ready Failed is registered. That is true since #530: until then it read the processor's raw admission verdict, which the Talker Advertise declaration alone raises. `ACMP_TALKER 0x66C[3]` is the *resolved* admission gate that actually admits frames. **When those two disagree, the bypass is engaged** -- on 2026-07-28 both boards read `0x66C = 0x08` (admission 1) beside `0x694 = 0x30` (licence 0), which is the signature to look for. |
| **`LWSRP_CTRL[5]` (declare-always bypass) is 🟡 WRITE-ONLY SCRATCH.** The per-talker declaration validity gate it bypassed lived in the deleted applicant. The processor runs its own Milan v1.2 4.3.3.1 declaration logic and takes no bypass input, so setting this bit changes nothing observable. `[0]` engine enable and `[1]` talker declare remain live gates in `milan_datapath`'s own admission terms, and `[4:2]` still selects which `0x400` queue the slope mux drives. |
| MSRP frames go to `01:80:C2:00:00:0E`/`0x22EA`, MVRP to `01:80:C2:00:00:21`/`0x88F5` (link-local, never forwarded by bridges) -- the protocol processor emits them on the control lane, and they are two of the three frame classes its RX tap classifies in (the third is EtherType `0x22F0`). `CAP[14]` advertises the group. **The MRP timers are the processor's now** and are not the deleted engine's Join 200 ms / Leave 600 ms / LeaveAll 10 s trio; read the submodule's timer map rather than this page for their values. |

### LWSRP_CTRL register (offset 0x680) [reset = 0x00000010]

SRP admission enable and talker admission arm.

RTL name: `A_LWSRP_CTRL`.

![LWSRP_CTRL bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:6 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 5 | `LWSRP_DECL_BYPASS` | R/W | 0 |  |
| 4:2 | `RESERVED` | R/W | 4h | Reserved; stored and read back, drives nothing. |
| 1 | `LWSRP_TALKER_EN` | R/W | 0 |  |
| 0 | `LWSRP_ENABLE` | R/W | 0 |  |

| Note |
|---|
| `[0]` live admission enable, `[1]` live talker admission arm. Generated cold-reset bits may differ; firmware ORs both on for normal boot. They do not enable the processor SRP engine. `[4:2]` legacy queue-selection scratch (default 4); `[5]` legacy declare-always scratch. |

### LWSRP_VID register (offset 0x684) [reset = 0x00000002]

Software-owned default SR VID.

RTL name: `A_LWSRP_VID`.

![LWSRP_VID bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_VID.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:12 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 11:0 | `LWSRP_VID` | R/W | 2h |  |

| Note |
|---|
| Software-owned diagnostic/default VID. Startup reset and firmware share `srp.vid=2` with the generated processor default parameter. Manual writes do not program that elaboration parameter; operational Domain adoption is published at `0x788`. |

### LWSRP_DMAC_LO register (offset 0x688) [reset = 0xF000FE01]

Retained stream destination MAC bits 31 to 0.

RTL name: `A_LWSRP_DMLO`.

![LWSRP_DMAC_LO bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_DMAC_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LWSRP_DEST_MAC` | R/W | F000FE01h | Bits [31:0] of the RTL value. |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH** -- stream dest MAC `[31:0]` (same packing as `AAF_DM*`). The applicant that read it is deleted; the processor takes its destination address from MAAP |

### LWSRP_DMAC_HI register (offset 0x68C) [reset = 0x000091E0]

Retained stream destination MAC bits 47 to 32.

RTL name: `A_LWSRP_DMHI`.

![LWSRP_DMAC_HI bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_DMAC_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `LWSRP_DEST_MAC` | R/W | 91E0h | Bits [47:32] of the RTL value. |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH** -- stream dest MAC `[47:32]` |

### LWSRP_TSPEC register (offset 0x690) [reset = 0x000100E0]

Retained MaxFrameSize and MaxIntervalFrames words.

RTL name: `A_LWSRP_TSPEC`.

![LWSRP_TSPEC bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_TSPEC.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `LWSRP_INTERVAL` | R/W | 1h |  |
| 15:0 | `LWSRP_MAX_FRAME` | R/W | E0h |  |

| Note |
|---|
| 🟡 **WRITE-ONLY SCRATCH**: `[15:0]` MaxFrameSize, `[31:16]` MaxIntervalFrames. The applicant that read them is deleted. The processor declares each source's Milan v1.2 4.3.3.2 Table 4.4 MaxFrameSize as the fabric derives it from that source's framer (an AAF talker's wire width, the CRF output's PDU shape, #774), so the declaration and the frame cannot disagree, and it derives its interval from the SR class. Writing this changes nothing observable |

### LWSRP_STATUS register (offset 0x694) [reset = 0xXXXXXXXX]

SRP registrar and declaration status from the processor.

RTL name: `A_LWSRP_STATUS`.

![LWSRP_STATUS bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_STATUS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LWSRP_STATUS` | R | X |  |

| Note |
|---|
| Mixed. 🟢 **LIVE, REPOINTED** from the processor's class-D face. **`[3:0]` describes ONE subject: the Listener attribute REGISTERED on talker SOURCE 0** (the processor's `lstn_reg_state[0]`), which is the subject it had before the control plane was substituted and the subject it has again since VERSION `0x005C`. `[1:0]` is that attribute's 802.1Q 35.2.2.7.2 (Table 35-3) FourPackedEvents value (0 none/ignore, 1 asking-failed, 2 ready, 3 ready-failed); `[2]` listener registered = the value is not 0, **asking-failed INCLUDED** (the field answers "does anyone want this stream", and an asking-failed Listener does: it must still see our TalkerAdvertise or it can never become Ready); `[3]` listener ready = the value is ready or ready-failed, the Milan v1.2 5.3.7.3 pair. From the substitution to VERSION `0x005B` this nibble mixed two subjects and misread both: `[1:0]` carried sink 0's OWN Listener declaration, `[2]` read bit 1 of the registered value (so a registered asking-failed Listener reported 0) and `[3]` compared the sink's declaration against the asking-failed code (so it read 1 while this station declared asking-failed and 0 while it declared ready). `[4]` talker declared, `[5]` domain ok, `[6]` reservation ACTIVE ORed over sources, the CRF output included, `[7]` **over the 75 % gate**, `[8]` stream gate open: source 0's ACTIVE AND real grant (#551), `[9]` the processor's raw admission verdict, ORed over sources: status only, since no shaper is instantiated to read it; raw ACTIVE can lead it during optimism, but licences require the real grant (#551), `[10]` TalkerFailed seen, `[23:16]` MSRP failure code. 🔴 **STRUCTURAL ZERO**: `[11]` attribute-row shortfall (there is no attribute-row table in this fabric any more) and `[31:24]` ingress FIFO frame drops (that ingress path is deleted; the protocol processor's own control-frame FIFO drop counter lives at `PP_DIAG` `0x930[15:8]`). `[15:12]` reserved 0 |

### LWSRP_SLOPE register (offset 0x698) [reset = 0xXXXXXXXX]

Granted idleSlope summed across admitted sources.

RTL name: `A_LWSRP_SLOPE`.

![LWSRP_SLOPE bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_SLOPE.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LWSRP_SLOPE` | R | X | 🟢 **LIVE, REPOINTED**: the granted idleSlope in bits/s, now the processor's **sum across admitted sources** (which is what a single shaped queue's idleSlope must be), not a single stream's `MaxIntervalFrames × (MaxFrameSize+42) × 8 × 8000`. Status only: no shaper is instantiated to consume it, licences require ACTIVE AND the real grant (#551) |

### LWSRP_CNT register (offset 0x69C) [reset = 0xXXXXXXXX]

Retired MRPDU counters, a structural zero.

RTL name: `A_LWSRP_CNT`.

![LWSRP_CNT bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_CNT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LWSRP_CNT` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was `[31:16]` MRPDUs received / `[15:0]` MRPDUs sent. The serialiser and ingress path that counted them are deleted; the processor exchanges MRPDUs and publishes no PDU counters. Reservations still form -- read `LWSRP_STATUS` and `LWSRP_DOM`, not this |

### LWSRP_LATENCY register (offset 0x6A0) [reset = 0x00000000]

TalkerAdvertise AccumulatedLatency in nanoseconds.

RTL name: `A_LWSRP_LAT`.

![LWSRP_LATENCY bit fields](../../docs/diagrams/regmap/lwsrp/LWSRP_LATENCY.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LWSRP_LATENCY` | R/W | 0 | TalkerAdvertise AccumulatedLatency, ns -- still LIVE: `milan_datapath` passes it to the processor as `cfg_acc_lat_ns_i` |

## 0x6A4  -  ACMP listener SM  `(Milan v1.2 Section 5.5 listener, FR-CONN-01)`

Listener bind record, AVTP RX, MAAP and audio diagnostics.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x6A4` | `ACMPL_STATE` | ACMP listener state | `0xXXXXXXXX` | [section](#acmpl_state-register-offset-0x6a4-reset--0xxxxxxxxx) |
| `0x6A8` | `ACMPL_TALKER_LO` | Bound talker, low word | `0xXXXXXXXX` | [section](#acmpl_talker_lo-register-offset-0x6a8-reset--0xxxxxxxxx) |
| `0x6AC` | `ACMPL_TALKER_HI` | Bound talker, high word | `0xXXXXXXXX` | [section](#acmpl_talker_hi-register-offset-0x6ac-reset--0xxxxxxxxx) |
| `0x6B0` | `ACMPL_CNT` | ACMP listener counts | `0xXXXXXXXX` | [section](#acmpl_cnt-register-offset-0x6b0-reset--0xxxxxxxxx) |
| `0x6B4` | `ACMPL_TUID` | ACMP listener talker ID | `0xXXXXXXXX` | [section](#acmpl_tuid-register-offset-0x6b4-reset--0xxxxxxxxx) |
| `0x6B8` | `AVTPRX_STAT` | AVTP RX status (saturating views) | `0xXXXXXXXX` | [section](#avtprx_stat-register-offset-0x6b8-reset--0xxxxxxxxx) |
| `0x6BC` | `AVTPRX_FRX` | AVTP RX frames received | `0xXXXXXXXX` | [section](#avtprx_frx-register-offset-0x6bc-reset--0xxxxxxxxx) |
| `0x6C0` | `AVTPRX_ERR` | AVTP RX errors (saturating views) | `0xXXXXXXXX` | [section](#avtprx_err-register-offset-0x6c0-reset--0xxxxxxxxx) |
| `0x6C4` | `PCMRX_CNT` | AAF RX depacketizer counts | `0xXXXXXXXX` | [section](#pcmrx_cnt-register-offset-0x6c4-reset--0xxxxxxxxx) |
| `0x6C8` | `PCMRX_TS` | AAF RX last timestamp | `0xXXXXXXXX` | [section](#pcmrx_ts-register-offset-0x6c8-reset--0xxxxxxxxx) |
| `0x6CC` | `MAAP_CTRL` | MAAP control | `0x00000000` | [section](#maap_ctrl-register-offset-0x6cc-reset--0x00000000) |
| `0x6D0` | `MAAP_STAT0` | MAAP status 0 | `0xXXXXXXXX` | [section](#maap_stat0-register-offset-0x6d0-reset--0xxxxxxxxx) |
| `0x6D4` | `MAAP_STAT1` | MAAP status 1 | `0xXXXXXXXX` | [section](#maap_stat1-register-offset-0x6d4-reset--0xxxxxxxxx) |
| `0x6D8` | `I2SPB_STAT` | I2S playback drift rails | `0xXXXXXXXX` | [section](#i2spb_stat-register-offset-0x6d8-reset--0xxxxxxxxx) |
| `0x6DC` | `TONE_CTRL` | Pilot tone control | `0x00000000` | [section](#tone_ctrl-register-offset-0x6dc-reset--0x00000000) |
| `0x6E0` | `I2SPB_TRIM` | I2S playback trim | `0xXXXXXXXX` | [section](#i2spb_trim-register-offset-0x6e0-reset--0xxxxxxxxx) |
| `0x6E4` | `GPTP_PDELAY` | gPTP neighbor delay | `0xXXXXXXXX` | [section](#gptp_pdelay-register-offset-0x6e4-reset--0xxxxxxxxx) |
| `0x6E8` | `ACMPL_DBG` | Listener walker forensics | `0xXXXXXXXX` | [section](#acmpl_dbg-register-offset-0x6e8-reset--0xxxxxxxxx) |
| `0x6EC` | `AVTPRX_TSD` | AVTP RX timestamp delta | `0xXXXXXXXX` | [section](#avtprx_tsd-register-offset-0x6ec-reset--0xxxxxxxxx) |
| `0x6F0` | `I2SPB_DBG` | I2S DAC forensics | `0xXXXXXXXX` | [section](#i2spb_dbg-register-offset-0x6f0-reset--0xxxxxxxxx) |
| `0x6F4` | `CTLR_DIAG` | Controller diagnostics | `0xXXXXXXXX` | [section](#ctlr_diag-register-offset-0x6f4-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary ACMP listener **bind record** (the SM fields are structural zeros) + AVTP RX / MAAP / audio diagnostics |
| The ACMP listener for the STREAM_INPUT[0] sink (BIND_RX/UNBIND_RX/GET_RX_STATE + the talker-probe ladder, per the Milan v1.2 ACMP contract). `KL_acmp_listener` and `KL_acmp_lstn_ctx` are **deleted**; the ladder runs inside the protocol processor now, and it publishes a **bind RECORD, not a state machine**. |
| 🔴 **`ACMPL_STATE` no longer tracks PROBING / SETTLED -- take `bound` as the truth.** The fields that described the ladder -- SM state `[2:0]`, probing status `[14:13]`, last ACMP status `[12:8]`, talker ADP-visible `[15]`, Listener attribute declared `[5]` -- are structural zeros: the processor runs the ladder internally and exposes none of it. What is still real in that word is `[3]` **bound**, `[4]` **stream active** (which now simply follows bound), `[27:16]` the bound stream's VLAN, `[31]` **CRF sink bound**, and the two per-sink SRP registrar bits `[6]` **TalkerAdvertise registered** and `[7]` **TalkerFailed registered**, which the class-D face does publish for sink 0 -- `[6]` as the sink's registered Talker attribute code compared against ADVERTISE (1, of 0 NONE / 1 ADVERTISE / 2 FAILED), `[7]` as its registered TalkerFailed code. Both were listed here as structural zeros until VERSION `0x005C`, and `[6]` additionally read bit 1 of the code, which is the FAILED bit. `ACMPL_TALKER_LO/HI`, `ACMPL_CNT`, `ACMPL_TUID`'s unique-id field and `ACMPL_DBG` are structural zeros for the same reason. |
| **Bound really is the truth, not a consolation prize.** The bind record carries the bound stream_id, DMAC and VLAN, and the fabric consumes those as wires every clock -- the stream table, the RX classifier and the CRF sink all key off it. A sink reading `bound = 1` is a sink whose frames are being classified. |
| The group tail carries the RW MAAP/tone/pdelay knobs, all unaffected. The STREAM_INPUT counter words (`AVTPRX_*`, `PCMRX_*`) are unaffected and **still live** -- they are the AVTP RX monitor's, not the control plane's. |

| Offset | Register | Access | Fields |
|---|---|---|---|
| `0x6F8` | -- | -- | **reserved**, free. Claim it here before wiring it |
| `0x6FC` | -- | -- | **reserved**, free -- the last word of this group. The next group starts at `0x700` (`TCAM_CTRL`) |

| Note |
|---|
| `CTLR_DIAG` (0x6F4) is **STRUCTURAL ZERO**. Its source was deleted; this word has no replacement source. It reads `0` because nothing backs it, not because nothing happened. Never read it as a measurement. |
| The departing-controller monitor (Milan v1.2 Section 5.4.5.3) lives in the protocol processor's `KL_aecp_notify` and `KL_aecp_ca_originator`. The processor exports no probe, reply or eviction count. The parent ties `aecp_ctlr_diag` to `32'd0`, preserving the address. Zero cannot establish controller presence, silence or eviction. The `milan_dp` timed notification leg checks this after controller traffic. |
| Timers per the reference: probe response 200 ms ×2, retry 4 s, no-talker 10 s, random pre-probe delay 0..1023 ms (LFSR). |

### ACMPL_STATE register (offset 0x6A4) [reset = 0xXXXXXXXX]

Bound state of listener sink 0 and its SRP bits.

RTL name: `A_ACMPL_STATE`.

![ACMPL_STATE bit fields](../../docs/diagrams/regmap/acmpl/ACMPL_STATE.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMPL_STATE` | R | X |  |

| Note |
|---|
| 🔴 Mixed, see above. **Still real:** `[3]` bound, `[4]` stream active (follows bound), `[27:16]` stream VLAN from the bind record, `[31]` CRF sink bound. Also real, both read from the processor's per-SINK SRP face for **sink 0** (these flat words always described sink 0): `[6]` TalkerAdvertise registered = sink 0's registered Talker attribute equals the ADVERTISE code (`tk_reg_state[0]`, a code and not a one-hot: 0 NONE, 1 ADVERTISE, 2 FAILED), `[7]` TalkerFailed registered = sink 0 carries an MSRP TalkerFailed failure code (the same source as `ACMPL_TUID[23:16]`). `[6]` was documented as a structural zero and read bit 1 of the code until VERSION `0x005C`, i.e. it reported a registered Talker FAILED as an ADVERTISE and a registered ADVERTISE as nothing. **STRUCTURAL ZERO:** `[2:0]` SM state (the 0-7 UNBOUND/PRB_*/SETTLED_* ladder no longer exists here and this field pins at 0, a reader that waits for SETTLED waits forever), `[5]` Listener attr declared, `[12:8]` last ACMP status, `[14:13]` probing status, `[15]` bound talker ADP-visible |

### ACMPL_TALKER_LO register (offset 0x6A8) [reset = 0xXXXXXXXX]

Retired bound talker entity ID, a structural zero.

RTL name: `A_ACMPL_TKLO`.

![ACMPL_TALKER_LO bit fields](../../docs/diagrams/regmap/acmpl/ACMPL_TALKER_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMPL_TALKER_LO` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was the bound talker entity id `[31:0]`. The processor keeps the bound entity id internally; the class-D face this fabric consumes publishes the bound stream_id, DMAC and VLAN, not the talker's entity id |

### ACMPL_TALKER_HI register (offset 0x6AC) [reset = 0xXXXXXXXX]

Retired bound talker entity ID, a structural zero.

RTL name: `A_ACMPL_TKHI`.

![ACMPL_TALKER_HI bit fields](../../docs/diagrams/regmap/acmpl/ACMPL_TALKER_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMPL_TALKER_HI` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was the bound talker entity id `[63:32]` |

### ACMPL_CNT register (offset 0x6B0) [reset = 0xXXXXXXXX]

Retired listener command counts, a structural zero.

RTL name: `A_ACMPL_CNT`.

![ACMPL_CNT bit fields](../../docs/diagrams/regmap/acmpl/ACMPL_CNT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMPL_CNT` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO**. Was `[31:16]` PROBE_TX commands sent / `[15:0]` listener commands accepted. The processor answers and probes; it publishes no PDU counters |

### ACMPL_TUID register (offset 0x6B4) [reset = 0xXXXXXXXX]

Retired talker unique ID and the live failure code.

RTL name: `A_ACMPL_TUID`.

![ACMPL_TUID bit fields](../../docs/diagrams/regmap/acmpl/ACMPL_TUID.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMPL_TUID` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO** for `[15:0]` bound talker unique id. `[23:16]` MSRP TalkerFailed code for the bound stream is 🟢 **LIVE, REPOINTED** -- it is the processor's per-sink SRP failure code |

### AVTPRX_STAT register (offset 0x6B8) [reset = 0xXXXXXXXX]

Stream Input 0 lock and interruption counters.

RTL name: `A_AVTPRX_STAT`.

![AVTPRX_STAT bit fields](../../docs/diagrams/regmap/acmpl/AVTPRX_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AVTPRX_STAT` | R | X |  |

| Note |
|---|
| AVTP RX monitor (STREAM_INPUT[0], IEEE 1722.1-2021 Table 7-156, Milan v1.2 Table 5.6): `[31:24]` STREAM_INTERRUPTED, `[23:16]` MEDIA_UNLOCKED, `[15:8]` MEDIA_LOCKED, `[0]` media-locked level. The three byte fields are **saturating** narrow views of 32-bit counters (VERSION `0x0013`, same rule as `AVTPRX_ERR`): `0xFF` = "at least 255", full width at `A_STRMW_CNT` `0x830 + 4k` |

### AVTPRX_FRX register (offset 0x6BC) [reset = 0xXXXXXXXX]

Stream Input 0 FRAMES_RX, a full 32-bit counter.

RTL name: `A_AVTPRX_FRX`.

![AVTPRX_FRX bit fields](../../docs/diagrams/regmap/acmpl/AVTPRX_FRX.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AVTPRX_FRX` | R | X | STREAM_INPUT[0] FRAMES_RX (full 32-bit counter) |

### AVTPRX_ERR register (offset 0x6C0) [reset = 0xXXXXXXXX]

Stream Input 0 sequence, format and timestamp counters.

RTL name: `A_AVTPRX_ERR`.

![AVTPRX_ERR bit fields](../../docs/diagrams/regmap/acmpl/AVTPRX_ERR.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AVTPRX_ERR` | R | X |  |

| Note |
|---|
| `[31:16]` SEQ_NUM_MISMATCH, `[15:8]` UNSUPPORTED_FORMAT, `[7:0]` TIMESTAMP_UNCERTAIN. **Narrow SATURATING views** of 32-bit counters (VERSION `0x0013`): all-ones means "**at least** this many", not "exactly this many" -- read the full-width value at `A_STRMW_CNT` (`0x830 + 4k`; SEQ_NUM_MISMATCH = `0x83C`). Before `0x0013` these fields TRUNCATED, i.e. counted down again after the roll: silicon 2026-07-26 read SEQ_NUM_MISMATCH `51,523` on a board up 81 h, 79 % of the way to a 16-bit wrap that would have made a degrading link look like a healing one. Values below the ceiling are unchanged |

### PCMRX_CNT register (offset 0x6C4) [reset = 0xXXXXXXXX]

Frames dropped and payloads emitted by the depacketizer.

RTL name: `A_PCMRX_CNT`.

![PCMRX_CNT bit fields](../../docs/diagrams/regmap/acmpl/PCMRX_CNT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PCMRX_CNT` | R | X |  |

| Note |
|---|
| AAF RX depacketizer: `[31:16]` whole frames dropped (FIFO overflow), `[15:0]` PDU payloads emitted to the fabric |

### PCMRX_TS register (offset 0x6C8) [reset = 0xXXXXXXXX]

avtp_timestamp of the last depacketized PDU.

RTL name: `A_PCMRX_TS`.

![PCMRX_TS bit fields](../../docs/diagrams/regmap/acmpl/PCMRX_TS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PCMRX_TS` | R | X | `avtp_timestamp` of the last depacketized PDU (media-clock recovery hook) |

### MAAP_CTRL register (offset 0x6CC) [reset = 0x00000000]

MAAP enable, seed and block count.

RTL name: `A_MAAP_CTRL`.

![MAAP_CTRL bit fields](../../docs/diagrams/regmap/acmpl/MAAP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `MAAP_SEED_OFFSET` | R/W | 0 |  |
| 15:8 | `MAAP_COUNT` | R/W | 0 |  |
| 7:2 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 1 | `MAAP_SEED_VALID` | R/W | 0 |  |
| 0 | `MAAP_ENABLE` | R/W | 0 |  |

| Note |
|---|
| Neutral disabled reset `0`: `[0]` enable, `[1]` seed_valid, `[15:8]` block count, `[31:16]` seed offset. Firmware writes generated `MILAN_MAAP_CTRL_BOOT`, claiming exactly the declared AAF outputs plus one only when CRF output exists. |

### MAAP_STAT0 register (offset 0x6D0) [reset = 0xXXXXXXXX]

MAAP conflicts, defends and the claimed offset.

RTL name: `A_MAAP_STAT0`.

![MAAP_STAT0 bit fields](../../docs/diagrams/regmap/acmpl/MAAP_STAT0.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `MAAP_STAT0` | R | X |  |

| Note |
|---|
| `[31:24]` conflicts (re-address events), `[23:16]` DEFENDs sent, `[15:0]` claimed offset |

### MAAP_STAT1 register (offset 0x6D4) [reset = 0xXXXXXXXX]

MAAP state and address-valid flag.

RTL name: `A_MAAP_STAT1`.

![MAAP_STAT1 bit fields](../../docs/diagrams/regmap/acmpl/MAAP_STAT1.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `MAAP_STAT1` | R | X |  |

| Note |
|---|
| `[2]` addr_valid (= ANNOUNCE state; DMAC = 91:E0:F0:00 + offset), `[1:0]` state (0 idle / 1 probe / 2 announce) |

### I2SPB_STAT register (offset 0x6D8) [reset = 0xXXXXXXXX]

Underrun and overrun counts, each half cleared on write.

RTL name: `A_I2SPB_STAT`.

![I2SPB_STAT bit fields](../../docs/diagrams/regmap/acmpl/I2SPB_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `I2SPB_CLR_UNDER` | R/W1C | X |  |
| 15:0 | `I2SPB_CLR_OVER` | R/W1C | X |  |

| Note |
|---|
| I2S playback drift rails: `[31:16]` underruns (silence frames), `[15:0]` overruns (pairs dropped). They measure free-running-48k drift; at the power-on INTERNAL selection that drift free-runs by the standing free-run rule, and since #74 a CRF selection engages the servo chain that retires it. Both rails saturate at `0xFFFF`; **W1C per half (2026-07-22, gaps 5b)**: a write with any bit of a half set restarts that half's counter (the other half is untouched; a zero write is inert; readback stays the live count). W1C was chosen over clear-on-bind: the rails are engine diagnostics, not Milan Table 5.6 stream counters. A bind-triggered clear would erase evidence mid-diagnosis and add a bind-path dependency, while W1C leaves the observation window entirely under software control |

### TONE_CTRL register (offset 0x6DC) [reset = 0x00000000]

Pilot tone enable and attenuation.

RTL name: `A_TONE_CTRL`.

![TONE_CTRL bit fields](../../docs/diagrams/regmap/acmpl/TONE_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:4 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 3:1 | `TONE_ATT` | R/W | 0 | **attenuation**, −6 dB steps applied as `TONE_TAB_C[idx] >>> att` (0 = 0 dBFS full scale, 7 = −42 dB); reset is `0`, so the power-on tone is 0 dBFS and any smaller amplitude was dialled in at the bench. A capture at amplitude 0.25 means `att = 2`, not a quarter-scale table: `8388607 >>> 2 = 2097151`, and `2097151 / 2^23 = 0.24999988`. Reduce before measuring through a sample-rate conversion or an analog stage, because a 0 dBFS sampled sine overshoots between samples (measured +0.91 dB through a 48 kHz to 44.1 kHz conversion) and would clip; at 48 kHz end to end the maxima land on table entries and 0 dBFS is safe. See the [obsolete historical media-clock finding](../history/v1/findings/MEDIA_CLOCK_LOCK_0810.md) |
| 0 | `TONE_ENABLE` | R/W | 0 | pilot tone enable: 1 kHz exact-period 48×24-bit sine replaces the I2S ADC on both talker channels (digital THD+N −148.1 dB; E2E acceptance ≤ −120 dBFS at the physical Listener output). |

### I2SPB_TRIM register (offset 0x6E0) [reset = 0xXXXXXXXX]

Media-clock recovery trim and FIFO fill.

RTL name: `A_I2SPB_TRIM`.

![I2SPB_TRIM bit fields](../../docs/diagrams/regmap/acmpl/I2SPB_TRIM.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `I2SPB_TRIM` | R | X |  |

| Note |
|---|
| media-clock recovery servo: `[31:16]` signed NCO trim (LSB ≈ 15.3 ppm; fill-level servo steers playback rate to the talker), `[15:0]` FIFO fill (pairs). Rail events count MEDIA_RESET |

### GPTP_PDELAY register (offset 0x6E4) [reset = 0xXXXXXXXX]

Measured gPTP neighbor propagation delay in nanoseconds.

RTL name: `A_GPTP_PDELAY`.

![GPTP_PDELAY bit fields](../../docs/diagrams/regmap/acmpl/GPTP_PDELAY.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `GPTP_PDELAY_NS` | R | X | reset `0`: fabric-owned measured gPTP neighbor propagation delay in ns. Option OFF reads zero; writes are inert. GET_AVB_INFO consumes this value. |

### ACMPL_DBG register (offset 0x6E8) [reset = 0xXXXXXXXX]

Retired listener walker counters, a structural zero.

RTL name: `A_ACMPL_DBG`.

![ACMPL_DBG bit fields](../../docs/diagrams/regmap/acmpl/ACMPL_DBG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMPL_DBG` | R | X | 🔴 **STRUCTURAL ZERO**. Was the listener walker forensics -- CLASSIFY entries, ACMP-subtype classifies, the flag bundle at the last ACMP classify, ACMP-base + listener-command hits. The walker is deleted. The protocol processor's own RX accounting (control frames in, FIFO drops, frames out) is at `PP_DIAG` `0x930` |

### AVTPRX_TSD register (offset 0x6EC) [reset = 0xXXXXXXXX]

Signed timestamp delta at the last accepted PDU.

RTL name: `A_AVTPRX_TSD`.

![AVTPRX_TSD bit fields](../../docs/diagrams/regmap/acmpl/AVTPRX_TSD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AVTPRX_TSD` | R | X | signed ts_delta = `avtp_timestamp - ptp_now` (ns) at the last accepted STREAM_INPUT[0] PDU -- the stream-sync error signal (LATE counts when delta < 0, EARLY beyond offset + margin; [presentation validity](../design/TIME_SYNC.md#presentation-validity)) |

### I2SPB_DBG register (offset 0x6F0) [reset = 0xXXXXXXXX]

Serial bits of the last left half-frame at the DAC.

RTL name: `A_I2SPB_DBG`.

![I2SPB_DBG bit fields](../../docs/diagrams/regmap/acmpl/I2SPB_DBG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `I2SPB_DBG` | R | X | DAC-serial forensics: the exact 32 serial bits of the last LEFT half-frame as sent at the DAC pin (CDC-latched) |

### CTLR_DIAG register (offset 0x6F4) [reset = 0xXXXXXXXX]

Retired controller counter, a structural zero.

RTL name: `A_CTLR_DIAG`.

![CTLR_DIAG bit fields](../../docs/diagrams/regmap/acmpl/CTLR_DIAG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CTLR_DIAG` | R | X | 🔴 **STRUCTURAL ZERO**. Reads `0`; never read it as a measurement. The deleted local monitor's probe, reply and eviction counters have no replacement source for this word. The departing-controller monitor lives in the protocol processor |

## 0x700  -  RX destination-MAC TCAM filter  `(REQ-MAC-02)`

RX destination-MAC filter programming.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x700` | `TCAM_CTRL` | TCAM control | `0x00000001` | [section](#tcam_ctrl-register-offset-0x700-reset--0x00000001) |
| `0x704` | `TCAM_KEY_LO` | TCAM key, low word | `0x00000000` | [section](#tcam_key_lo-register-offset-0x704-reset--0x00000000) |
| `0x708` | `TCAM_KEY_HI` | TCAM key, high word | `0x00000000` | [section](#tcam_key_hi-register-offset-0x708-reset--0x00000000) |
| `0x70C` | `TCAM_MASK_LO` | TCAM mask, low word | `0x00000000` | [section](#tcam_mask_lo-register-offset-0x70c-reset--0x00000000) |
| `0x710` | `TCAM_MASK_HI` | TCAM mask, high word | `0x00000000` | [section](#tcam_mask_hi-register-offset-0x710-reset--0x00000000) |
| `0x714` | `TCAM_ACTION` | TCAM action | `0x00000000` | [section](#tcam_action-register-offset-0x714-reset--0x00000000) |
| `0x718` | `TCAM_CMD` | TCAM command | `0x00000000` | [section](#tcam_cmd-register-offset-0x718-reset--0x00000000) |

| Note |
|---|
| Group summary RX destination-MAC TCAM filter |
| A ternary CAM (`tcam.sv`) in the RX path (`rx_mac_filter`) that accepts/drops frames by destination MAC - exact **or** wildcard/range (per-bit `mask`). Precise alternative to the approximate `MC_HASH` hash filter. Software programs one indexed entry per commit: write the KEY/MASK/ACTION shadows, then `TCAM_CMD`. Reset: `default_pass=1` (accept-all until entries are installed - safe bring-up). |
| The 48-bit `key`/`mask` = `{HI[15:0], LO}` and are compared MSB-first against the destination MAC in standard notation (`01-80-C2-00-00-0E` → `0x0180C200000E`). Whitelist: `default_pass=0` + accept entries (`ACTION[0]=0`). Blacklist: `default_pass=1` + drop entries (`ACTION[0]=1`). Example ternary entry: reserved multicast block `01-80-C2-00-00-0x` = key `0x0180C2000000`, mask `0xFFFFFFFFFFF0`. See [`../hdl/ieee8021q/filtering/doc/tcam.md`](../../hdl/ieee8021q/filtering/doc/tcam.md). |

### TCAM_CTRL register (offset 0x700) [reset = 0x00000001]

Default pass and address-filter enable for the RX filter.

RTL name: `A_TCAM_CTRL`.

![TCAM_CTRL bit fields](../../docs/diagrams/regmap/tcam/TCAM_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 1 | `TCAM_ADDR_FILT_EN` | R/W | 0 |  |
| 0 | `TCAM_DEFAULT_PASS` | R/W | 1h |  |

| Note |
|---|
| `[0]` default_pass (1 = accept frames that miss the table), `[1]` addr_filter_en (1 = a TCAM miss falls to the 802.3 station address filter of the `0x100` group instead of `[0]` - REQ-MAC-02, reset 0) |

### TCAM_KEY_LO register (offset 0x704) [reset = 0x00000000]

Match key bits 31 to 0 for the next commit.

RTL name: `A_TCAM_KLO`.

![TCAM_KEY_LO bit fields](../../docs/diagrams/regmap/tcam/TCAM_KEY_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `TCAM_WR_KEY` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| match key `[31:0]` (dest MAC, MSB-first: byte0 in `[31:24]`? no - see note) |

### TCAM_KEY_HI register (offset 0x708) [reset = 0x00000000]

Match key bits 47 to 32 for the next commit.

RTL name: `A_TCAM_KHI`.

![TCAM_KEY_HI bit fields](../../docs/diagrams/regmap/tcam/TCAM_KEY_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `TCAM_WR_KEY` | R/W | 0 | Bits [47:32] of the RTL value. |

| Note |
|---|
| match key `[47:32]` in `[15:0]` |

### TCAM_MASK_LO register (offset 0x70C) [reset = 0x00000000]

Care mask bits 31 to 0 for the next commit.

RTL name: `A_TCAM_MLO`.

![TCAM_MASK_LO bit fields](../../docs/diagrams/regmap/tcam/TCAM_MASK_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `TCAM_WR_MASK` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| care mask `[31:0]` (1 = compare, 0 = wildcard) |

### TCAM_MASK_HI register (offset 0x710) [reset = 0x00000000]

Care mask bits 47 to 32 for the next commit.

RTL name: `A_TCAM_MHI`.

![TCAM_MASK_HI bit fields](../../docs/diagrams/regmap/tcam/TCAM_MASK_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `TCAM_WR_MASK` | R/W | 0 | Bits [47:32] of the RTL value. |

| Note |
|---|
| care mask `[47:32]` in `[15:0]` |

### TCAM_ACTION register (offset 0x714) [reset = 0x00000000]

Action byte for the next commit.

RTL name: `A_TCAM_ACT`.

![TCAM_ACTION bit fields](../../docs/diagrams/regmap/tcam/TCAM_ACTION.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:8 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 7:0 | `TCAM_WR_ACTION` | R/W | 0 |  |

| Note |
|---|
| `[0]` drop-on-match (else accept), `[7:1]` steer tag |

### TCAM_CMD register (offset 0x718) [reset = 0x00000000]

Commits one TCAM entry: index, add or remove.

RTL name: `A_TCAM_CMD`.

![TCAM_CMD bit fields](../../docs/diagrams/regmap/tcam/TCAM_CMD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:17 | `RESERVED` | R | 0 | Reserved. |
| 16 | `TCAM_WR_EN` | W1S | 0 | commit (self-clearing) - latches KEY/MASK/ACTION shadows into the entry |
| 15:9 | `RESERVED` | R | 0 | Reserved. |
| 8 | `TCAM_WR_VALID` | W | 0 | valid (1 = add/update, 0 = remove) |
| 7:5 | `RESERVED` | R | 0 | Reserved. |
| 4:0 | `TCAM_WR_INDEX` | W | 0 | entry index |

## 0x71C  -  Link guard / MAC recovery (VERSION minor ≥ 0x0006)

Link guard controls and the reset canary.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x71C` | `LINK_CTRL` | Link control | `0x00000001` | [section](#link_ctrl-register-offset-0x71c-reset--0x00000001) |
| `0x720` | `RST_EPOCH` | Reset epoch | `0x000000XX` | [section](#rst_epoch-register-offset-0x720-reset--0x000000xx) |

| Note |
|---|
| Group summary Link guard / MAC recovery (`LINK_CTRL`, `RST_EPOCH`, `LINKG_STAT` 0x774) |
| The L1/L2 link-bounce supervisor ([`hdl/common/KL_link_guard.sv`](../../hdl/common/KL_link_guard.sv)) and firmware recovery strobes. (Added 2026-07-23 -- these were live in RTL but undocumented here, which caused a false "0x774 = TCAM" reading; TCAM is 0x700–0x718 only.) |

### LINK_CTRL register (offset 0x71C) [reset = 0x00000001]

Firmware link qualification and link-guard controls.

RTL name: `A_LINK_CTRL`.

![LINK_CTRL bit fields](../../docs/diagrams/regmap/link/LINK_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:4 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 3 | `LINKG_FREEZE` | R/W | 0 | linkg_freeze (test hook: fake eth clock death drills the full FSM with no cable) |
| 2 | `LINKG_DIS` | R/W | 0 | linkg_dis (1 = guard disabled) |
| 1 | `MAC_REINIT` | R/W | 0 | manual mac_reinit (hold MAC sys-side in reset) A write stores 0 here while `ETH_GUARD[0]` is 1. |
| 0 | `SW_LINK` | R/W | 1h | firmware link qualification (assumed up at reset) |

### RST_EPOCH register (offset 0x720) [reset = 0x000000XX]

Count of datapath reset releases, the reset canary.

RTL name: `A_RST_EPOCH`.

![RST_EPOCH bit fields](../../docs/diagrams/regmap/link/RST_EPOCH.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:8 | `RESERVED` | R | 0 | Reserved. |
| 7:0 | `RST_EPOCH` | R | X |  |

| Note |
|---|
| datapath reset-release count -- the shadow-lie canary (a live tick proves a real reset happened, e.g. so a CSR-wipe is not mistaken for an unbind) |

## 0x724  -  identity / playback / 802.1AS overlay

Entity name overlay, playback filter and gPTP parent.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x724` | `ENT_NAME_LO` | Entity name overlay, characters 0 to 3 | `0x00000000` | [section](#ent_name_lo-register-offset-0x724-reset--0x00000000) |
| `0x728` | `ENT_NAME_HI` | Entity name overlay, characters 4 to 7 | `0x00000000` | [section](#ent_name_hi-register-offset-0x728-reset--0x00000000) |
| `0x72C` | `LPF_CTRL` | Playback filter control | `0x00000001` | [section](#lpf_ctrl-register-offset-0x72c-reset--0x00000001) |
| `0x730` | `AS2_LO` | gPTP parent, low word | `0xXXXXXXXX` | [section](#as2_lo-register-offset-0x730-reset--0xxxxxxxxx) |
| `0x734` | `AS2_HI` | gPTP parent, high word | `0xXXXXXXXX` | [section](#as2_hi-register-offset-0x734-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary Identity / playback / 802.1AS overlay words |
| Bare-metal firmware may write the board-name overlay. The fabric gPTP owner publishes live parent topology directly; option OFF is ownerless and reads zero ([Clock ownership](../design/TIME_SYNC.md#clock-ownership)). |

### ENT_NAME_LO register (offset 0x724) [reset = 0x00000000]

Board-name overlay characters 0 to 3.

RTL name: `A_ENT_NAME_LO`.

![ENT_NAME_LO bit fields](../../docs/diagrams/regmap/overlay/ENT_NAME_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:24 | `ENTITY_NAME8_31_24` | R/W | 0 | Bits [39:32] of the RTL value. |
| 23:16 | `ENTITY_NAME8_23_16` | R/W | 0 | Bits [47:40] of the RTL value. |
| 15:8 | `ENTITY_NAME8_15_8` | R/W | 0 | Bits [55:48] of the RTL value. |
| 7:0 | `ENTITY_NAME8_7_0` | R/W | 0 | Bits [63:56] of the RTL value. |

| Note |
|---|
| entity_name chars 0-3, `[7:0]` = char 0 (board-name overlay; all-zero = keep the ROM name) |

### ENT_NAME_HI register (offset 0x728) [reset = 0x00000000]

Board-name overlay characters 4 to 7.

RTL name: `A_ENT_NAME_HI`.

![ENT_NAME_HI bit fields](../../docs/diagrams/regmap/overlay/ENT_NAME_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:24 | `ENTITY_NAME8_31_24` | R/W | 0 | Bits [7:0] of the RTL value. |
| 23:16 | `ENTITY_NAME8_23_16` | R/W | 0 | Bits [15:8] of the RTL value. |
| 15:8 | `ENTITY_NAME8_15_8` | R/W | 0 | Bits [23:16] of the RTL value. |
| 7:0 | `ENTITY_NAME8_7_0` | R/W | 0 | Bits [31:24] of the RTL value. |

| Note |
|---|
| entity_name chars 4-7 |

### LPF_CTRL register (offset 0x72C) [reset = 0x00000001]

Enables the playback low-pass filter.

RTL name: `A_LPF_CTRL`.

![LPF_CTRL bit fields](../../docs/diagrams/regmap/overlay/LPF_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 0 | `LPF_ENABLE` | R/W | 1h | playback biquad LPF enable (`KL_pcm_lpf`), on by default |

### AS2_LO register (offset 0x730) [reset = 0xXXXXXXXX]

Parent clockIdentity bits 31 to 0, coherent with AS2_HI.

RTL name: `A_AS2_LO`.

![AS2_LO bit fields](../../docs/diagrams/regmap/overlay/AS2_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `GPTP_PARENT_RD_SNAP` | R | X |  |

| Note |
|---|
| parent clockIdentity `[31:0]`. Fabric mode snapshots the complete live 64-bit parent on the first half read and holds it through the complementary half, in either order. Option OFF reads zero; writes are inert. |

### AS2_HI register (offset 0x734) [reset = 0xXXXXXXXX]

Parent clockIdentity bits 63 to 32, coherent with AS2_LO.

RTL name: `A_AS2_HI`.

![AS2_HI bit fields](../../docs/diagrams/regmap/overlay/AS2_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `GPTP_PARENT_RD_SNAP` | R | X |  |

| Note |
|---|
| parent clockIdentity `[63:32]`. Fabric mode is the other half of the coherent snapshot. Option OFF reads zero; writes are inert. GET_AS_PATH consumes only the fabric publication. |

## 0x738  -  CRF media-clock sink  `(Milan v1.2 7.3, KL_crf_rx)`

CRF media-clock sink control and measurements.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x738` | `CRF_CTRL` | CRF sink control | `0xX0000000` | [section](#crf_ctrl-register-offset-0x738-reset--0xx0000000) |
| `0x73C` | `CRF_SIDLO` | CRF sink stream ID, low word | `0x00000000` | [section](#crf_sidlo-register-offset-0x73c-reset--0x00000000) |
| `0x740` | `CRF_SIDHI` | CRF sink stream ID, high word | `0x00000000` | [section](#crf_sidhi-register-offset-0x740-reset--0x00000000) |
| `0x744` | `CRF_DELTA` | CRF timestamp delta | `0xXXXXXXXX` | [section](#crf_delta-register-offset-0x744-reset--0xxxxxxxxx) |
| `0x748` | `CRF_RATE` | CRF rate | `0xXXXXXXXX` | [section](#crf_rate-register-offset-0x748-reset--0xxxxxxxxx) |
| `0x74C` | `CRF_STATUS` | CRF status | `0xXXXXXXXX` | [section](#crf_status-register-offset-0x74c-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary CRF media-clock sink (Milan v1.2 7.3, `KL_crf_rx`) |
| The measurement half of the CRF clock-recovery loop: `KL_crf_rx` validates every PDU of the followed CRF stream against the Milan 7.3.2 profile constants and produces the servo's phase/frequency inputs; the MMCM-DRP actuator status lives at `0x8F8`. Loop semantics: [Media boundary](../design/TIME_SYNC.md#media-boundary); servo internals and bench history: [historical Section 3.4](../history/v1/design/TIME_SYNC.md#34-the-mmcm-drp-servo--kl_mmcm_drp_servo-mcsrv-0x8f80x8fc) |
| The followed stream normally comes from the CRF sink bind (ACMP listener sink 1 -- the bind wins); the SID pair here is the manual lever, and the bind-restore group notes that this sink re-arms via `0x738`. |
| Those three are the only CRF input counters exported into the local CSR plane, and only as the documented truncated slices. AECP carries all ten Table 5.16 counters `KL_crf_rx` keeps. `milan_datapath.sv` serves them full width, each wrapping at 32 bits, on the solicited GET_COUNTERS gather face for the declared CRF Media Clock Input at STREAM_INPUT index `N_STREAMS`. It also delivers the engine's dirty pulse to the rate-limited Table 5.22 scheduler as that same descriptor (#529). FRAMES_RX counts every accepted AVTPDU, including routine healthy traffic, under IEEE 1722.1-2021 Table 7.157 and the #726 ruling. It resets on not-bound to bound and retains its value on unbind. The six anomaly counters keep their observation intervals. STREAM_INTERRUPTED counts an accepted PDU that shows two or more lost PDUs, and since #762 the 100 ms silence that unlocks a bound input (Milan v1.2 5.3.8.10 Table 5.6). The AAF inputs' `KL_avtp_rx_monitor_ctx` and the CRF input's `KL_crf_rx` apply one rule, the [#762 scope ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6260976223) and its [extension to sequence gaps](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6265746720): |
| a silence on a started input counts once; |
| a silence on a stopped input counts nothing, because a stopped input has no playback to interrupt (5.3.8.7, and 5.4.2.20 makes STOP_STREAMING the change to stopped); the lock still falls and MEDIA_UNLOCKED counts it; |
| STOP with live traffic counts nothing; |
| after START (5.4.2.19), a later silence counts again; |
| a sequence gap of two or more lost PDUs on a started input counts once; |
| a sequence gap on a stopped input counts nothing, for the same reason; it still counts SEQ_NUM_MISMATCH and unlocks nothing; |
| after START, a sequence gap counts again; |
| a Controller Unbind never counts, as Table 5.6 excludes it. |
| The silence's expiry is the one event boundary: an Unbind or a STOP that arrives after it leaves the silence counted, and one that arrives on or before it leaves none. A gap's boundary is its PDU's accept verdict: the gap counts when the input is started on that edge, and a STOP or a START after it changes nothing for that gap. |

| Quadlet (block offset) | Counter | `KL_crf_rx` output |
|---|---|---|
| 0 (`@0`) | MEDIA_LOCKED | `cnt_locked_o` |
| 1 (`@4`) | MEDIA_UNLOCKED | `cnt_unlocked_o` |
| 2 (`@8`) | STREAM_INTERRUPTED | `cnt_intr_o` |
| 3 (`@12`) | SEQ_NUM_MISMATCH | `seq_err_o` |
| 4 (`@16`) | MEDIA_RESET | `mr_cnt_o` |
| 5 (`@20`) | TIMESTAMP_UNCERTAIN | `tu_cnt_o` |
| 8 (`@32`) | UNSUPPORTED_FORMAT | `fmt_err_o` |
| 9 (`@36`) | LATE_TIMESTAMP | `late_cnt_o` |
| 10 (`@40`) | EARLY_TIMESTAMP | `early_cnt_o` |
| 11 (`@44`) | FRAMES_RX | `pdu_count_o` |

| Note |
|---|
| `counters_valid` is `0x00000F3F`: the ten at their IEEE 1722.1-2021 Table 7-157 offsets. Milan keeps the IEEE Stream Input layout; only the Stream Output layout (Table 5.17) is compacted. TIMESTAMP_VALID and TIMESTAMP_NOT_VALID (quadlets 6 and 7) stay unclaimed because `KL_crf_rx` keeps no tally for them, while the AAF inputs claim all twelve (`0x00000FFF`). A shape that declares no CRF sink serves no such row, and an undeclared index still answers NO_SUCH_DESCRIPTOR with the empty body. |

### Closure criteria for the CRF Stream Input counter gap

| Note |
|---|
| Closed by #529. Each criterion is quoted as it was frozen, followed by the evidence that closes it. Every `[CTRS-CRF]` check named here runs on the 4x4, divergent 4x4, 8x8 and shipping Arty 4x4 `tb/verilator/milan_dp` legs. |
| *"Connect the complete `KL_crf_rx` Table 5.16 bank to the root solicited gather face for STREAM_INPUT index `N_STREAMS`."* All ten outputs are connected, and two `[CTRS-CRF]` arms grade the two halves of each path. The signature arm writes a distinct full-width value into each root tally wire by name and reads every quadlet back through the processor's response. It grades the gather mux, wire to quadlet, and cannot see which engine output drives a wire. The event arm seeds no tally. It moves each of the ten through its own `KL_crf_rx` event to a count no other tally shares: real PDUs of the followed stream, and for MEDIA_UNLOCKED the engine's own 100 ms silence timeout (the harness advances that timeout counter to its last millisecond, which runs for real). So each quadlet in the table above is shown to carry the output it names. |
| *"Return the correct compact valid mask and counter words for that declared descriptor while preserving the empty response for undeclared indices."* The compact mask is Milan Table 5.16 at the IEEE Table 7-157 offsets, `0xF3F` (above). `[CTRS-CRF]` grades the SUCCESS response (cdl 148) from reset, and the mask `0xF3F` with every unclaimed quadlet zero from reset, after the not-bound to bound wipe and after the event arm. It drives the 32-bit wrap of FRAMES_RX (per-AVTPDU law) and STREAM_INTERRUPTED (per-event law) with real PDUs, and requires NO_SUCH_DESCRIPTOR with an empty body at `N_STREAMS + 1`. |
| *"Connect the CRF dirty source to the rate-limited Table 5.22 scheduler."* `[CTRS-CRF]` sees the bind edge reach the descriptor arbiter as {STREAM_INPUT, `N_STREAMS`} and as nothing else. The harness records every tuple the arbiter hands over in that window, of any type and at any index. No other STREAM_INPUT row, no STREAM_OUTPUT row (the CRF Media Clock Output's at the same index included), neither AVB_INTERFACE 0 nor CLOCK_DOMAIN 0, and no tuple of any other type or index may appear. On the timed `obj_notify` leg, `[NOTIFY-CRF]` sees the push reach both registered controllers, each copy byte-identical from the body on to the solicited answer. A second change is withheld until the one-second limit releases it, and the next two seconds without a change bring no further push. |
| *"Add root-wire tests for reset, wrap, descriptor isolation, and controller decoding before treating the CRF input counter duty as closed."* The checks above cover each. Each of these wiring mutations turns at least one of them red: the row removed, two quadlets permuted, a 16-bit slice, a claimed tv pair, the dirty source removed, the CRF row answering for the AAF inputs, the AAF guard answering for the CRF input, one tally unwired, the row's pending bit never cleared, and the CRF pulse also raising the AAF inputs, STREAM_OUTPUT `N_STREAMS`, AVB_INTERFACE 0, CLOCK_DOMAIN 0 or a tuple at an undeclared index. Each of the 45 pairwise exchanges of the ten `KL_crf_rx` output bindings at the instance turns both of its quadlets red on the 4x4 and 8x8 legs. Confirmation by a Milan controller on silicon follows the merge (#117). |

### CRF_CTRL register (offset 0x738) [reset = 0xX0000000]

CRF sink enable and the locked flag.

RTL name: `A_CRF_CTRL`.

![CRF_CTRL bit fields](../../docs/diagrams/regmap/crf/CRF_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31 | `CRF_LOCKED` | R | X | locked (RO live). Eight clean consecutive PDUs establish lock. No consumed accepted PDU for 100 ms clears lock. So does an unbind (enable and ACMP bind both low). Each counts one MEDIA_UNLOCKED (#653). A profile validation error retains lock and breaks settling. It does not refresh the timeout. Each observation interval containing errors increments `UNSUPPORTED_FORMAT` (`fmt_err_o`) once. `CRF_STATUS[15:8]` (`0x74C`) exposes its low eight bits. GET_COUNTERS exposes all 32 bits. |
| 30:1 | `RESERVED` | R | 0 | Reserved. |
| 0 | `CRF_EN` | R/W | 0 | CRF sink enable (RW) |

### CRF_SIDLO register (offset 0x73C) [reset = 0x00000000]

Followed CRF stream_id bits 31 to 0.

RTL name: `A_CRF_SIDLO`.

![CRF_SIDLO bit fields](../../docs/diagrams/regmap/crf/CRF_SIDLO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRF_SID` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| followed CRF stream_id `[31:0]` |

### CRF_SIDHI register (offset 0x740) [reset = 0x00000000]

Followed CRF stream_id bits 63 to 32.

RTL name: `A_CRF_SIDHI`.

![CRF_SIDHI bit fields](../../docs/diagrams/regmap/crf/CRF_SIDHI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRF_SID` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| stream_id `[63:32]` |

### CRF_DELTA register (offset 0x744) [reset = 0xXXXXXXXX]

Signed crf_ts minus ptp_now at the last PDU.

RTL name: `A_CRF_DELTA`.

![CRF_DELTA bit fields](../../docs/diagrams/regmap/crf/CRF_DELTA.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRF_DELTA` | R | X | signed `crf_ts - ptp_now` (ns) at each accepted PDU -- phase, same signed-delta contract as `AVTPRX_TSD` (0x6EC); carries the talker+transit constant, deliberately NOT a servo input |

### CRF_RATE register (offset 0x748) [reset = 0xXXXXXXXX]

Talker media clock rate measured against gPTP.

RTL name: `A_CRF_RATE`.

![CRF_RATE bit fields](../../docs/diagrams/regmap/crf/CRF_RATE.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRF_RATE` | R | X | The talker's media clock measured against gPTP, the servo frequency input. Signed ns error per 512 ms window (256-PDU ring); 1 ppm = 512 units. Holds the last clean value during discontinuity refill. Internal validity gates servo sampling; this CSR does not expose validity |

### CRF_STATUS register (offset 0x74C) [reset = 0xXXXXXXXX]

CRF PDUs accepted, format errors and sequence errors.

RTL name: `A_CRF_STATUS`.

![CRF_STATUS bit fields](../../docs/diagrams/regmap/crf/CRF_STATUS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRF_STATUS` | R | X |  |

| Note |
|---|
| `[31:16]` PDUs accepted, `[15:8]` format errors (subtype, #765, and the 7.3.2 pull/base/dlen/interval/type check), `[7:0]` sequence errors |

## 0x750  -  CRF media-clock talker  `(Milan v1.2 7.3.1, KL_crf_tx)`

CRF media-clock talker control and counters.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x750` | `CRFT_CTRL` | CRF talker control | `0xXXXXXXXX` | [section](#crft_ctrl-register-offset-0x750-reset--0xxxxxxxxx) |
| `0x754` | `CRFT_SIDLO` | CRF talker stream ID, low word | `0x00000000` | [section](#crft_sidlo-register-offset-0x754-reset--0x00000000) |
| `0x758` | `CRFT_SIDHI` | CRF talker stream ID, high word | `0x00000000` | [section](#crft_sidhi-register-offset-0x758-reset--0x00000000) |
| `0x75C` | `CRFT_DMLO` | CRF talker destination MAC, low word | `0x00000000` | [section](#crft_dmlo-register-offset-0x75c-reset--0x00000000) |
| `0x760` | `CRFT_DMHI` | CRF talker destination MAC, high word | `0x00000000` | [section](#crft_dmhi-register-offset-0x760-reset--0x00000000) |
| `0x764` | `CRFT_COUNT` | CRF talker PDU count | `0xXXXXXXXX` | [section](#crft_count-register-offset-0x764-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary CRF media-clock talker (`KL_crf_tx`) |
| Emits the CRF AUDIO_SAMPLE stream (subtype 4, pull 0, base_frequency 48000, timestamp_interval 96 ⇒ 500 PDU/s), timestamped from the real audio-MMCM sample grid: every 96th `/512` sample event latches the live PHC value, so the wire carries the actual audio-clock rate as the PHC sees it. A PDU that would collide with a busy serializer is skipped whole -- timestamps stay truthful, only the cadence stretches ([historical CRF talker section](../history/v1/design/TIME_SYNC.md#32-crf-out--kl_crf_tx-the-media-clock-talker)). |

### CRFT_CTRL register (offset 0x750) [reset = 0xXXXXXXXX]

CRF talker enable, class-A declare and live status.

RTL name: `A_CRFT_CTRL`.

![CRFT_CTRL bit fields](../../docs/diagrams/regmap/crft/CRFT_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `CRFT_STAT` | R | X | Bits [31:2] of the RTL value. |
| 1 | `CRFT_CLASS_A` | R/W | 0 |  |
| 0 | `CRFT_EN` | R/W | 0 |  |

| Note |
|---|
| `[0]` CRF talker enable; `[1]` **class-A declare + tag** (Milan v1.2 7.3.3: "An AVB Class A Stream Reservation *shall* be used to transmit [the] CRF Media Clock Stream"): the fabric provisions its own lwSRP talker row and derives the C-TAG (PCP 3, VID = `LWSRP_VID`, or the **operational adopted pair** whenever `LWSRP_DOM[24]` is set, Milan 4.2.7.2.1) from that row's *validity*, so tagged-but-undeclared is unreachable; with `[1]` clear the stream falls back to the untagged control-lane shape (flooded by the bridge, but alive). Since the substitution the reservation is the protocol processor's, not a fabric-provisioned lwSRP row. Live read: `[4]` 🔴 **STRUCTURAL ZERO** (was "the fabric provisioned this stream's TA row valid"; there is no row to provision), `[5]` frames leaving tagged, `[6]` reservation active: this output's ACTIVE AND real admission grant (#551; Milan v1.2 5.3.7.3), `[7]` emission licensed now (`[0]` and `[6]` while SRP policing is on). Until #530 `[6]` read the processor's raw admission verdict, which the declaration alone raises, so a declared output with no Listener read `[6]` = `[7]` = 1 and streamed. `[19:8]` VID, `[22:20]` PCP (both = the pair on the frames, one wire with the declaration). **Boot value**: the bare-metal firmware writes `MILAN_CRF_TX_CTRL_BOOT`, generated from `clocking.crf_output.enabled`: `0x3` when the config declares the CRF Media Clock Output, `0x0` when it does not, so an undeclared output is neither transmitted nor declared (#398) |

### CRFT_SIDLO register (offset 0x754) [reset = 0x00000000]

CRF talker stream_id bits 31 to 0.

RTL name: `A_CRFT_SIDLO`.

![CRFT_SIDLO bit fields](../../docs/diagrams/regmap/crft/CRFT_SIDLO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRFT_SID` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| CRF talker stream_id `[31:0]`. Reset 0 selects AUTO in multi-stream builds: the fabric uses `{station MAC, N_STREAMS}`, matching the CRF Media Clock Output context described by the [end-station builder](../ENDSTATION_BUILDER.md). A non-zero pair wins outright |

### CRFT_SIDHI register (offset 0x758) [reset = 0x00000000]

CRF talker stream_id bits 63 to 32.

RTL name: `A_CRFT_SIDHI`.

![CRFT_SIDHI bit fields](../../docs/diagrams/regmap/crft/CRFT_SIDHI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRFT_SID` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| stream_id `[63:32]`, same AUTO rule (the pair is tested together) |

### CRFT_DMLO register (offset 0x75C) [reset = 0x00000000]

CRF talker destination MAC bits 31 to 0.

RTL name: `A_CRFT_DMLO`.

![CRFT_DMLO bit fields](../../docs/diagrams/regmap/crft/CRFT_DMLO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRFT_DEST_MAC` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| CRF stream dest MAC `[31:0]` (same packing as `AAF_DM*`). **Reset 0 = AUTO:** the MAAP block slot `base + N_STREAMS`, one past the audio talkers -- when CRF output is declared, `MAAP_CTRL` claims `N_STREAMS+1`; otherwise it claims exactly `N_STREAMS`. A non-zero pair wins outright |

### CRFT_DMHI register (offset 0x760) [reset = 0x00000000]

CRF talker destination MAC bits 47 to 32.

RTL name: `A_CRFT_DMHI`.

![CRFT_DMHI bit fields](../../docs/diagrams/regmap/crft/CRFT_DMHI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `CRFT_DEST_MAC` | R/W | 0 | Bits [47:32] of the RTL value. |

| Note |
|---|
| dest MAC `[47:32]` in `[15:0]`, same AUTO rule |

### CRFT_COUNT register (offset 0x764) [reset = 0xXXXXXXXX]

CRF PDUs emitted since reset.

RTL name: `A_CRFT_COUNT`.

![CRFT_COUNT bit fields](../../docs/diagrams/regmap/crft/CRFT_COUNT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CRFT_COUNT` | R | X | Raw CRF PDUs emitted since reset. GET_COUNTERS FRAMES_TX counts the same transmitted AVTPDUs but resets at every talker start; both wrap at 32 bits. IEEE 1722.1-2021 7.4.42.2.5 Table 7.159 and the [2026-10-12 ruling](https://github.com/kebag-logic/milan-fpga/issues/726#issuecomment-6125741685) replace the former occupied-interval interpretation. MEDIA_RESET and TIMESTAMP_UNCERTAIN retain their interval law. |

## 0x768  -  AECP GET_DYNAMIC_INFO scan forensics (BDBG) -- 🔴 STRUCTURAL ZERO, and the link-guard status

Retired scan forensics and the live link-guard status.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x768` | `BDBG0` | Scan forensics 0 | `0xXXXXXXXX` | [section](#bdbg0-register-offset-0x768-reset--0xxxxxxxxx) |
| `0x76C` | `BDBG1` | Scan forensics 1 | `0xXXXXXXXX` | [section](#bdbg1-register-offset-0x76c-reset--0xxxxxxxxx) |
| `0x770` | `BDBG2` | Scan forensics 2 | `0xXXXXXXXX` | [section](#bdbg2-register-offset-0x770-reset--0xxxxxxxxx) |
| `0x774` | `LINKG_STAT` | Link guard status | `0xXXXXXXXX` | [section](#linkg_stat-register-offset-0x774-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary AECP GET_DYNAMIC_INFO scan forensics (BDBG) -- **all three words structural zeros** |
| **All three words are STRUCTURAL ZEROS.** They belonged to the deleted fabric AECP response builder. The processor now implements `GET_DYNAMIC_INFO` and its own internal batch scanner, but the scanner exposes no BDBG connection to this legacy CSR group. The words keep their addresses because the map is an ABI. Their zero means "legacy forensics not connected", not "the latest scan found nothing" and not "GET_DYNAMIC_INFO is unavailable". |

### BDBG0 register (offset 0x768) [reset = 0xXXXXXXXX]

Retired AECP scan forensics, a structural zero.

RTL name: `A_BDBG0`.

![BDBG0 bit fields](../../docs/diagrams/regmap/bdbg/BDBG0.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `BDBG0` | R | X | 🔴 STRUCTURAL ZERO. Was: the four record-header bytes as scanned `{dlen_hi, dlen_lo, cmd_hi, cmd_lo}` |

### BDBG1 register (offset 0x76C) [reset = 0xXXXXXXXX]

Retired AECP scan forensics, a structural zero.

RTL name: `A_BDBG1`.

![BDBG1 bit fields](../../docs/diagrams/regmap/bdbg/BDBG1.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `BDBG1` | R | X |  |

| Note |
|---|
| 🔴 STRUCTURAL ZERO. Was: `[30:16]` record command_type, `[15:0]` record data length, at the verdict |

### BDBG2 register (offset 0x770) [reset = 0xXXXXXXXX]

Retired AECP scan forensics, a structural zero.

RTL name: `A_BDBG2`.

![BDBG2 bit fields](../../docs/diagrams/regmap/bdbg/BDBG2.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `BDBG2` | R | X |  |

| Note |
|---|
| 🔴 STRUCTURAL ZERO. Was: `[24:16]` scan pointer, `[8:0]` payload end (bytes) |

### LINKG_STAT register (offset 0x774) [reset = 0xXXXXXXXX]

Live link-guard state, flags and bounce count.

RTL name: `A_LINKG_STAT`.

![LINKG_STAT bit fields](../../docs/diagrams/regmap/bdbg/LINKG_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LINKG_STAT` | R | X |  |

| Note |
|---|
| `KL_link_guard` `stat_o`: `[31:16]` bounce_cnt (saturating), `[9]` freeze, `[8]` dis, `[7]` act_recent (RX activity within the last 2^27 guard clock cycles: 2.7 s at the 50 MHz Milan clock, 1.3 s at 100 MHz), `[6]` guard_rst (reinit held), `[5:4]` state (0 RUN, 1 HOLD, 2 SETTLE), `[2]` eth_rst (sequenced eth-CDC reset, minor ≥ 0x0007), `[1]` tx_alive, `[0]` rx_alive |

## 0x778  -  Clock validity: the AVTP `tu` verdict `(VERSION minor >= 0x0016)`, TX arbiter and SRP domain

Clock validity, TX arbiter supervision and the SRP domain.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x778` | `CLKV_CTRL` | Clock validity control (inert) | `0x00000000` | [section](#clkv_ctrl-register-offset-0x778-reset--0x00000000) |
| `0x77C` | `CLKV_STAT` | Clock validity status | `0xXXXXXXXX` | [section](#clkv_stat-register-offset-0x77c-reset--0xxxxxxxxx) |
| `0x780` | `CLKV_TUCNT` | Timestamp-uncertain count | `0xXXXXXXXX` | [section](#clkv_tucnt-register-offset-0x780-reset--0xxxxxxxxx) |
| `0x784` | `TXARB_DIAG` | TX arbiter diagnostics | `0xXXXXXXXX` | [section](#txarb_diag-register-offset-0x784-reset--0xxxxxxxxx) |
| `0x788` | `LWSRP_DOM` | SRP operational domain | `0xXXXXXXXX` | [section](#lwsrp_dom-register-offset-0x788-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary Clock validity -- the AVTP `tu` verdict (`CLKV_CTRL`/`STAT`/`TUCNT`, minor ≥ `0x0016`) |
| **Why this group exists (2026-07-27).** This end station streamed 31 M AAF frames whose presentation times came from a PHC **216,446 s (60 h)** away from the gPTP domain, at full rate, with the AVTP `tu` bit hard-wired to 0 the whole time. The receiving Milan device counted **99.4 %** of them LATE or EARLY and had no way to defend itself, because the one field that exists to warn it said the timestamps were good (the retired reference-listener sweep of 2026-07-27 (#259, in git history)). |
| **What the standard requires, and what it forbids.** Not stopping: Milan v1.2 5.3.7.3 says a talker with a Listener Ready "**shall be streaming** AVTP packets. This specification excludes the possibility for a Stream Output to be stopped (STREAMING_WAIT shall not be implemented)." Not `tv = 0` either: IEEE 1722-2016 7.5 makes `tv = 1` mandatory on **every** AAF AVTPDU when `sp = 0`, which is our shape. The lever is `tu` -- Milan v1.2 4.3.5.2 ("A Talker PAAD **shall** set the AVTP `tu` bit as described in [AVTP, Clause 4.4.4.7]") and Annex B.1.1 (on a grandmaster change, `tu` **shall** be 1 for 0.25 s). |
| **Default owner at VERSION `0x0002_0060`.** The integrated engine directly publishes synchronized and asCapable levels. A GM change or a healthy-to- unhealthy sync commit asserts a same-edge discontinuity pulse; PHC settime and adjtime remain fabric-visible discontinuities. `tu` is the OR of not-synced, the live discontinuity edge and the Annex B.1.1 holdover. There is no CLKV lease or second runtime owner. |
| **The option-OFF arm fails safe by construction.** It is verification-only hardware with zero gPTP owners: sync and asCapable are zero, all public gPTP publication fields are zero, and `tu` is one. A local PHC set/adjust can still assert the safety holdover indicator; it cannot establish sync or clear `tu`. Writes to the retained addresses are acknowledged but inert, so no test or future software can manufacture a clock-valid claim. |
| **Reading it.** In fabric mode, `CLKV_STAT[1]` and `[16]` are the live engine sync/asCapable levels; `[15:4]` and `[2]` are zero. In option-OFF mode sync and asCapable stay zero and `tu` stays one; `[3]` may transiently report a local PHC set/adjust holdover. `CLKV_TUCNT` moving means `tu=1` was observed during at least one one-second observation interval; frozen at zero with `CLKV_STAT[1]` set and `[0]` clear is a healthy fabric-owned clock. |
| **What the state field and the two reset bits do over one episode** -- *in what order are the two resets released, and why does that order matter?* |
| ![Link-guard reset sequence](../diagrams/wd_linkguard_reset.svg) |
| `[5:4]` walks `RUN → HOLD → SETTLE → RUN`, but the two reset bits do **not** move together: `eth_rst` (`[2]`) drops **half-way through SETTLE**, `guard_rst` (`[6]`) only at the end of it. That ordering is the whole point -- the eth halves get at least `SETTLE_CYC_C/2` clean *clocked* reset cycles while the sys side is still held, so both CDC pointer sets restart matched. Reading `[6]` alone and concluding "the guard has released" is therefore wrong for the middle of an episode. A re-death inside SETTLE falls back to HOLD and re-arms `eth_rst`; a manual `LINK_CTRL[1]` edge runs the *same* sequence but deliberately does not bump `bounce_cnt`, which stays a true cable-event counter. Master: [`wd_linkguard_reset.json`](../diagrams/wd_linkguard_reset.json). |
| `PTP_CMD` strobes cross into the `gtx_clk` PTP domain via `ptp_csr_sync` (value + toggle-synchronised apply strobe, `REQ-CSR-03`). `gettime` is asynchronous: writing `PTP_CMD[2]` pulses the snapshot command into the PHC; the sampled TOD returns across the CDC and lands in `PTP_TOD_RD_{LO,HI}` a few cycles later (firmware reads it after the round trip). `PTP_INCR`/`PTP_ADJ` are the Q8.24-ns rate controls consumed by `timestamp_counter`. |

### CLKV_CTRL register (offset 0x778) [reset = 0x00000000]

Retained address; reads zero and writes change nothing.

RTL name: `A_CLKV_CTRL`.

![CLKV_CTRL bit fields](../../docs/diagrams/regmap/clkv/CLKV_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLKV_CTRL` | R | 0 | Retained address-map slot. Writes are acknowledged and discarded in both elaborations; reads return zero. Clock validity comes only from the fabric publication bank. |

### CLKV_STAT register (offset 0x77C) [reset = 0xXXXXXXXX]

The tu verdict and the fabric sync and asCapable state.

RTL name: `A_CLKV_STAT`.

![CLKV_STAT bit fields](../../docs/diagrams/regmap/clkv/CLKV_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLKV_STAT` | R | X |  |

| Note |
|---|
| `[0]` `tu` as currently stamped on every outgoing stream frame, `[1]` fabric sync_ok, `[3]` inside a discontinuity holdover, and `[16]` fabric **asCapable**. `[2]` and `[15:4]` are structural zero. In option OFF, `[0]` is one, `[1]` and `[16]` are zero, and `[3]` may pulse after a local PHC set/adjust; it cannot clear `tu` or manufacture health. `[16]` is the exact bit `GET_AVB_INFO` serves as `AS_CAPABLE` (IEEE 1722.1-2021 7.4.40.2 flags bit 0), so a controller's solicited view and this register cannot disagree. |

### CLKV_TUCNT register (offset 0x780) [reset = 0xXXXXXXXX]

Seconds in which the talkers stamped tu.

RTL name: `A_CLKV_TUCNT`.

![CLKV_TUCNT bit fields](../../docs/diagrams/regmap/clkv/CLKV_TUCNT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CLKV_TUCNT` | R | X | Milan v1.2 Table 5.4 / Table 5.6 `TIMESTAMP_UNCERTAIN` for the talker side: one increment per **1 s observation interval** in which `tu` was set at least once -- **not** one per frame and **not** one per `tu` edge (that is the IEEE 1722.1-2021 Table 7-159 reading, which Milan overrides for a PAAD). Engine-wide: one PHC, so the value serves every STREAM_OUTPUT |

### TXARB_DIAG register (offset 0x784) [reset = 0xXXXXXXXX]

TX trunk arbiter lock supervision per lane.

RTL name: `A_TXARB_DIAG`.

![TXARB_DIAG bit fields](../../docs/diagrams/regmap/clkv/TXARB_DIAG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `TXARB_DIAG` | R | X |  |

| Note |
|---|
| (minor ≥ `0x001B`) TX-trunk arbiter lock supervision. `[7:0]` locked-now, `[15:8]` abort-sticky (a granted source abandoned its frame mid-packet; the arbiter closed the frame with one injected `tlast` beat and released the lock), `[23:16]` stall-sticky (a presented beat was refused downstream for the mux's watchdog window), `[31:24]` constant tag `0xA7` (a zero read means the gateware predates the register). 🔴 **THE LANE NUMBERS CHANGED at VERSION major 2 -- anything decoding this word by the old numbers reads the WRONG MUX.** Major 2 first collapsed the old eight-mux cascade to four; minor `0x0055` added the fabric-gPTP control merge as lane 4. **Current lane order, LSB-first: `0` `ctl_tx` (protocol processor + MAAP), `1` `aaf_final` - 🔴 **structural zero since `0x0056`** (that merge joined the shaped general-data lane to AAF; the chain is gone and AAF enters `crf_dp` directly, and the lane is NOT renumbered), `2` `crf_dp`, `3` `adp_tx` (the MAC-boundary mux), `4` `gptp_ctl_mux` (gPTP + the gasketed control branch).** Lane 4 is live with fabric gPTP and structural zero option off; bits `7:5` of each field are structural zero. It **was**, before major 2: 0 `aecp_acmp`, 1 `ctl_tx`, 2 `srp_ctl`, 3 `lstn_ctl`, 4 `maap_ctl`, 5 `aaf_final`, 6 `crf_dp`, 7 `adp_tx`. Watchdog windows stay staggered shortest-upstream: lane 0 is 2^15, lanes 1/2/4 are 2^16, and MAC-boundary lane 3 is 2^17, so only the true origin of a cascade starvation fires. Stickies clear only on reset -- this register is forensics for the 07-29 wedge class (all TX dead, RX perfect), which by definition outlives every soft recovery path. Lane **3** retains the MAC-boundary verdict: its abort names an upstream trunk abort and its **stall** names the `mac_tx_cdc`/MAC side (H1), which `LINK_CTRL[1]`'s widened reinit scope (minor `0x001B`) resets |

### LWSRP_DOM register (offset 0x788) [reset = 0xXXXXXXXX]

Operational SR class-A VID and priority.

RTL name: `A_LWSRP_DOM`.

![LWSRP_DOM bit fields](../../docs/diagrams/regmap/clkv/LWSRP_DOM.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LWSRP_DOM` | R | X |  |

| Note |
|---|
| Processor operational Domain: `[11:0]` VID, `[23:16]` priority, `[24]` adopted. Startup and Link Up select generated defaults `{3,2}`. Network Domain declarations may adopt another pair. Admission-control writes do not reset the SRP engine. Diagnostic `LWSRP_VID` and `AAF_CTRL` writes remain independent; they do not rewrite the processor default. Adopted tags feed AAF and CRF. |

## 0x7A0  -  ACMP bind-restore  `(saved-state fast-connect E1, Milan 5.5.3.5.2)`

Retired bind-restore port, kept as an ABI.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7A0` | `REST_TK_LO` | Bind-restore talker, low word | `0x00000000` | [section](#rest_tk_lo-register-offset-0x7a0-reset--0x00000000) |
| `0x7A4` | `REST_TK_HI` | Bind-restore talker, high word | `0x00000000` | [section](#rest_tk_hi-register-offset-0x7a4-reset--0x00000000) |
| `0x7A8` | `REST_META` | Bind-restore metadata | `0x00000000` | [section](#rest_meta-register-offset-0x7a8-reset--0x00000000) |
| `0x7AC` | `REST_CTLR_LO` | Bind-restore controller, low word | `0x00000000` | [section](#rest_ctlr_lo-register-offset-0x7ac-reset--0x00000000) |
| `0x7B0` | `REST_CTLR_HI` | Bind-restore controller, high word | `0x00000000` | [section](#rest_ctlr_hi-register-offset-0x7b0-reset--0x00000000) |
| `0x7B4` | `REST_CMD` | Bind-restore command | `0x00000000` | [section](#rest_cmd-register-offset-0x7b4-reset--0x00000000) |

| Note |
|---|
| Group summary ACMP bind-restore (E1) -- **dead port: writes accepted, ack never asserts** |
| 🔴 **DEAD PORT. Writes are accepted; the ack never asserts and nothing is ever restored.** The ACMP listener context table this group injected into is deleted along with the rest of the legacy plane, so a commit is issued into a port with no engine behind it: `REST_CMD[31]` busy sets and never clears, and `REST_CMD[30]` done never rises. |
| **This CSR port persists nothing; bindings persist through the processor's restore walk and `KL_nvm_backend` (see `PP_NVM_*` at 0x934 and `PP_STAT` at 0x924), and the binding survives a cold power cycle on silicon since 2026-09-21 (#70).** The paragraph below is the record from before that backend landed: The processor has its own NVM restore walk, but the device face behind it is a BLANK-FLASH responder inside `KL_pp_shadow` -- reads return `0xFF`, writes are accepted and discarded, erase completes -- which is the processor's documented no-saved-binding path. A restore walk therefore always finds blank flash and completes with zero records. Milan v1.2 5.3.8.2 ("The current bound state shall be saved in a non-volatile memory and restored after a power cycle") is **not met**, and this build says so structurally rather than through a zeroed counter. |
| The `0xA5C35A3C` write/readback probe still works because `0x7A0` is a plain RW word, but it is not a licence to commit. Bare-metal firmware must gate on `VERSION` major: at major 2 this port is dead. |
| The register layout below is preserved verbatim because the map is an ABI, not because any of it acts. |
| The retired implementation refused rather than merged a commit when the context was already bound (5.5.1.2: only a controller changes a bound state). That refusal path is moot now: with no engine attached a commit stays busy forever, which is exactly the failure mode the old VERSION-gate warning described for TB ties -- except that it is the shipping build's behaviour, not a testbench artefact. |

### REST_TK_LO register (offset 0x7A0) [reset = 0x00000000]

Saved talker_entity_id bits 31 to 0.

RTL name: `A_REST_TKLO`.

![REST_TK_LO bit fields](../../docs/diagrams/regmap/rest/REST_TK_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMP_REST_TALKER` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| saved talker_entity_id `[31:0]` (doubles as the feature probe word) |

### REST_TK_HI register (offset 0x7A4) [reset = 0x00000000]

Saved talker_entity_id bits 63 to 32.

RTL name: `A_REST_TKHI`.

![REST_TK_HI bit fields](../../docs/diagrams/regmap/rest/REST_TK_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMP_REST_TALKER` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| saved talker_entity_id `[63:32]` |

### REST_META register (offset 0x7A8) [reset = 0x00000000]

Saved talker_unique_id and VLAN.

RTL name: `A_REST_META`.

![REST_META bit fields](../../docs/diagrams/regmap/rest/REST_META.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 15:0 | `ACMP_REST_TUID` | R/W | 0 |  |

| Note |
|---|
| `[15:0]` talker_unique_id; `[27:16]` saved VLAN -- informational only, **ignored on load** (5.5.2.6 step 1 re-probes it) |

### REST_CTLR_LO register (offset 0x7AC) [reset = 0x00000000]

Saved controller_entity_id bits 31 to 0.

RTL name: `A_REST_CTLO`.

![REST_CTLR_LO bit fields](../../docs/diagrams/regmap/rest/REST_CTLR_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMP_REST_CTLR` | R/W | 0 | Bits [31:0] of the RTL value. |

| Note |
|---|
| saved controller_entity_id `[31:0]` |

### REST_CTLR_HI register (offset 0x7B0) [reset = 0x00000000]

Saved controller_entity_id bits 63 to 32.

RTL name: `A_REST_CTHI`.

![REST_CTLR_HI bit fields](../../docs/diagrams/regmap/rest/REST_CTLR_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ACMP_REST_CTLR` | R/W | 0 | Bits [63:32] of the RTL value. |

| Note |
|---|
| saved controller_entity_id `[63:32]` |

### REST_CMD register (offset 0x7B4) [reset = 0x00000000]

Commit and status of the retired bind-restore port.

RTL name: `A_REST_CMD`.

![REST_CMD bit fields](../../docs/diagrams/regmap/rest/REST_CMD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31 | `REST_PEND` | R/W1S | 0 | A write takes effect only when `!rest_pend_r`. |
| 30 | `REST_DONE` | R | 0 |  |
| 29:24 | `RESERVED` | R | 0 | Reserved. |
| 23:10 | `REST_FLAGS` | W | 0 | A write takes effect only when `!rest_pend_r`. |
| 9:8 | `REST_STAT` | R/W | 0 | A write takes effect only when `!rest_pend_r`. A write sets REST_FLAGS; a read returns this field. |
| 7:4 | `RESERVED` | R | 0 | Reserved. |
| 3:0 | `REST_IDX` | R/W | 0 | A write takes effect only when `!rest_pend_r`. |

| Note |
|---|
| Write: `[31]` commit (accepted only while idle), `[23:8]` binding flags (bit 3 = STREAMING_WAIT), `[3:0]` target sink index (listener_unique_id). Read (live): `[31]` busy (commit in flight), `[30]` done (a commit completed since reset), `[9:8]` status of the last commit -- `0` injected, `1` refused: target context OCCUPIED (not `LSM_UNBOUND_S`; record untouched), `2` refused: bad index (>= N sinks, or a record-only context without the probe SM -- the CRF sink re-arms via `0x738`), `[3:0]` last committed index |

## 0x7B8  -  Persistence-journal ingest  `(saved-state fast-connect E3)`

Retired journal ingest port, kept as an ABI.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7B8` | `JNL_CTRL` | Journal ingest control | `0xX0000000` | [section](#jnl_ctrl-register-offset-0x7b8-reset--0xx0000000) |
| `0x7BC` | `JNL_DATA` | Journal ingest data | `0x00000000` | [section](#jnl_data-register-offset-0x7bc-reset--0x00000000) |
| `0x7C0` | `JNL_STAT` | Journal ingest status | `0xXXXXXXXX` | [section](#jnl_stat-register-offset-0x7c0-reset--0xxxxxxxxx) |
| `0x7C4` | `JNL_SEQ` | Journal ingest sequence | `0xXXXXXXXX` | [section](#jnl_seq-register-offset-0x7c4-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary Persistence-journal ingest (E3) -- **writes accepted and discarded; nothing is restored** |
| 🔴 **UNWIRED AGAIN AT VERSION MAJOR 2. Writes are accepted and DISCARDED; `JNL_STAT` `0x7C0` and `JNL_SEQ` `0x7C4` read STRUCTURAL ZEROS.** The journal engine (`KL_persist_journal`) is deleted along with the rest of the AECP plane, and the E1 restore port it drove is dead (see `0x7A0` above), so no image is ever verified and no binding is ever restored. Software may still push a whole slot image through `JNL_DATA`; every word lands nowhere and the verdict never comes. The `0x0019`-era trap is now permanent rather than a legacy-gateware caveat: `0x7C0` reading `0` is indistinguishable from "idle, no verdict", so software **must** gate on `VERSION` and never on a read of this group. At major 2 the gate's answer is "this port does nothing". Milan v1.2 5.3.8.2 -- "The current bound state shall be saved in a non-volatile memory and restored after a power cycle" -- is no longer served by this retired CSR face; the saved-state store serves it, with the open physical items on #70. The verification below is preserved as the record of what the port checked when it was live, and as the specification any future implementation must satisfy. |
| Software pushes ONE journal slot image (32-bit little-endian words, verbatim from flash) through this port. The fabric verifies magic / format major / shape / length / CRC-32 / owning `entity_id` / `SEQ` monotonicity and only THEN issues the E1 bind-restore transactions above - one per journal record. **A torn, truncated, foreign or stale image produces ZERO restores**: the CRC-32 trailer is the last word of the image, so a half-applied context table is not representable, not merely avoided. |
| Verdicts in `0x7C0[7:4]`: `0` none · `1` ACCEPT · `2` MAGIC (not a journal slot, or an erased one) · `3` VERSION (format major this build cannot read) · `4` SHAPE (`rec_words` != 6, or `n_rec` 0 / above capacity) · `5` LENGTH (truncated or overlong transfer) · `6` CRC (**torn write / bit rot**) · `7` ENTITY (journal belongs to another `entity_id` - a cloned image) · `8` STALE (`SEQ` does not beat the accepted watermark). |
| Structural verdicts are ordered before the CRC so an operator gets a naming diagnosis (an erased slot reads as MAGIC, not CRC), but nothing that is **trusted for action** - the entity id, the `SEQ` watermark, any record word - is consulted until the CRC has closed. |

### JNL_CTRL register (offset 0x7B8) [reset = 0xX0000000]

Start, end and abort strobes of the retired journal ingest.

RTL name: `A_JNL_CTRL`.

![JNL_CTRL bit fields](../../docs/diagrams/regmap/jnl/JNL_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:30 | `JNL_STAT` | R | X | Bits [31:30] of the RTL value. |
| 29:3 | `RESERVED` | R | 0 | Reserved. |
| 2 | `JNL_ABORT` | W1S | 0 |  |
| 1 | `JNL_END` | W1S | 0 |  |
| 0 | `JNL_START` | W1S | 0 |  |

| Note |
|---|
| Write: `[0]` start a slot image, `[1]` image complete -> verify (+ replay), `[2]` abort back to idle. Read (live): `[31]` busy, `[30]` done (a verdict produced since reset) |

### JNL_DATA register (offset 0x7BC) [reset = 0x00000000]

Next journal word for the retired journal ingest.

RTL name: `A_JNL_DATA`.

![JNL_DATA bit fields](../../docs/diagrams/regmap/jnl/JNL_DATA.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `JNL_DATA` | W | 0 | next 32-bit journal word, little-endian exactly as read from flash. Reads `0` |

### JNL_STAT register (offset 0x7C0) [reset = 0xXXXXXXXX]

Retired journal engine status, a structural zero.

RTL name: `A_JNL_STAT`.

![JNL_STAT bit fields](../../docs/diagrams/regmap/jnl/JNL_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `JNL_STAT` | R | X |  |

| Note |
|---|
| `[2:0]` state (0 idle, 1 load, 2 verify, 3/4/5 replay, 6 done), `[7:4]` verdict, `[11:8]` records in the accepted image, `[15:12]` records the ACMP engine injected, `[23:16]` per-record refusal bitmap (bit r = record r came back with a nonzero E1 status), `[30]` done, `[31]` busy |

### JNL_SEQ register (offset 0x7C4) [reset = 0xXXXXXXXX]

Retired accepted-image sequence, a structural zero.

RTL name: `A_JNL_SEQ`.

![JNL_SEQ bit fields](../../docs/diagrams/regmap/jnl/JNL_SEQ.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `JNL_SEQ` | R | X | `SEQ` of the last **accepted** image; 0 = none accepted this boot. A rejected image never advances it, which is what makes the A/B fall-back to an older intact slot admissible |

## 0x7C8  -  AEM dynamic-state patch port  `(saved-state fast-connect E4)`

Retired AEM patch port, kept as an ABI.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7C8` | `AEMP_SEL` | AEM patch select | `0x00000000` | [section](#aemp_sel-register-offset-0x7c8-reset--0x00000000) |
| `0x7CC` | `AEMP_FIELD` | AEM patch field | `0x00000000` | [section](#aemp_field-register-offset-0x7cc-reset--0x00000000) |
| `0x7D0` | `AEMP_DATA` | AEM patch data | `0x00000000` | [section](#aemp_data-register-offset-0x7d0-reset--0x00000000) |
| `0x7D4` | `AEMP_CTRL` | AEM patch control | `0xXXXXXXXX` | [section](#aemp_ctrl-register-offset-0x7d4-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary AEM dynamic-state patch port (E4) -- **writes accepted and discarded** |
| 🔴 **UNWIRED AT VERSION MAJOR 2. Writes are accepted and DISCARDED; `0x7D4` reads a STRUCTURAL ZERO.** The patch engine and the AEM store it wrote are both deleted. The current AECP uCPU owns volatile dynamic state and accepts several setters, but this port is not connected to that state. Writes cannot replay a saved value into the processor or change what a controller reads. |
| This was the write master for the deleted AEM store. The current processor has volatile dynamic state, but neither saving that state nor restoring it through this port is implemented. A reset therefore loses accepted changes. |
| The register layout and the verdict codes below are preserved as the ABI and as the specification a future implementation must satisfy. Reading `0x7D4` tells software nothing: `0` is what an idle port, a refused commit and an absent engine all produce. |
| Verdicts in `0x7D4[7:4]`: `0` none · `1` ACCEPT · `2` **ADP** (refused -- the entity is advertising) · `3` DESC (no such descriptor or index) · `4` FIELD (this port does not serve that field) · `5` LENGTH (wrong `AEMP_DATA` word count for the field) · `6` VALUE (payload failed the same acceptance the AECP setter applies). |
| Three properties are worth reading as design decisions rather than details: |
| **Descriptor-addressed, never byte-addressed.** Software names a descriptor and a field; the *fabric* resolves the byte range from the same generated `WB_STRIN_FMT_ADDR_C` / `WB_STROUT_FMT_ADDR_C` / `WB_SAMPLING_RATE_C` / `WB_CLOCK_SRC_IDX_C` tables `SET_STREAM_FORMAT` uses. A byte offset in a boot script would be a second copy of a generated constant, and the AEM ROM is regenerated on every config change. It also means the port physically cannot write outside a field it knows the name of. |
| **Validation is the same test, not a second one.** A restore is checked against that descriptor's own generated reference -- the supported-format family rule for an AAF sink, exact match for a CRF sink or any Stream Output, the advertised rate table, the `0..2` clock-source bound. Installing a format the entity does not declare would be a worse conformance break than the revert it fixes. |
| **Ordering is structural.** Every write is refused while `ADP_CTRL[0]` is set, and a transfer straddling an enable is dropped rather than resumable. "Replay before you advertise" is enforced by the hardware. |
| **What it deliberately does not reach.** Milan 5.3.4.1 (locked state) and 5.3.4.2 (registered controllers) require the *opposite* of persistence -- both are cleared by a power cycle. Neither has a field code or a table entry here, so the refusal is not a policy someone can forget to apply; it is the absence of a mechanism. |
| **What remains open after the control-plane substitution.** Presentation-time offset changes and names remain outside the served inventory. The mandatory audio-map writers now commit through the root transaction store. The processor stores `SET_CLOCK_SOURCE` and the media plane consumes it since #74 (`media_clk_resolve`). The remainder are current command or integration gaps, not evidence that the processor has no dynamic state. |

### AEMP_SEL register (offset 0x7C8) [reset = 0x00000000]

Descriptor selection for the retired AEM patch port.

RTL name: `A_AEMP_SEL`.

![AEMP_SEL bit fields](../../docs/diagrams/regmap/aemp/AEMP_SEL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AEMP_WDATA` | W | 0 | `{descriptor_type[31:16], descriptor_index[15:0]}` -- WHAT to patch. Reads `0`: the selection is engine state, not a shadow register, and a read-back would invite software to believe a selection survived a refusal it did not survive |

### AEMP_FIELD register (offset 0x7CC) [reset = 0x00000000]

Field selection for the retired AEM patch port.

RTL name: `A_AEMP_FIELD`.

![AEMP_FIELD bit fields](../../docs/diagrams/regmap/aemp/AEMP_FIELD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AEMP_WDATA` | W | 0 |  |

| Note |
|---|
| `[2:0]` which field of that descriptor: `0` stream format, `1` sampling rate, `2` clock source. `3` (presentation time offset) and `4` (name) are **registered and refused** -- see the verdict note below. Reads `0` |

### AEMP_DATA register (offset 0x7D0) [reset = 0x00000000]

Payload word for the retired AEM patch port.

RTL name: `A_AEMP_DATA`.

![AEMP_DATA bit fields](../../docs/diagrams/regmap/aemp/AEMP_DATA.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AEMP_WDATA` | W | 0 | next payload word, **MSW first**, as a left-aligned big-endian byte stream in descriptor order. Push `ceil(len/4)` words: 2 for a format, 1 for a sampling rate or a clock source. Reads `0` |

### AEMP_CTRL register (offset 0x7D4) [reset = 0xXXXXXXXX]

Commit and abort strobes of the retired AEM patch port.

RTL name: `A_AEMP_CTRL`.

![AEMP_CTRL bit fields](../../docs/diagrams/regmap/aemp/AEMP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `AEMP_STAT` | R | X |  |
| 1 | `AEMP_ABORT` | R/W1S | X | A read returns AEMP_STAT. |
| 0 | `AEMP_COMMIT` | R/W1S | X | A read returns AEMP_STAT. |

| Note |
|---|
| Write: `[0]` commit, `[1]` abort. Read (live): `[2:0]` state, `[7:4]` verdict, `[11:8]` bytes written by the last ACCEPT, `[14:12]` words staged, `[18:16]` field, `[19]` **ADP gate** (1 = writes are being refused), `[30]` done, `[31]` busy |

## 0x7D8  -  Ethernet guard

The Ethernet guard kill switch.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7D8` | `ETH_GUARD` | Ethernet guard | `0x00000001` | [section](#eth_guard-register-offset-0x7d8-reset--0x00000001) |

### ETH_GUARD register (offset 0x7D8) [reset = 0x00000001]

Kill switch that refuses the CPU's Ethernet disruption levers.

RTL name: `A_ETH_GUARD`.

![ETH_GUARD bit fields](../../docs/diagrams/regmap/guard/ETH_GUARD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R | 0 | Reserved. A write compares the whole word with the unlock key. |
| 0 | `ETH_GUARD` | R/W | 1h | 1 = guarded: the reset state, armed at power-on. Software may re-arm it before risky work. The link guard's own automatic recovery is not gated. The SoC exports the level (`o_eth_guard`), but at this head nothing in `sw/litex/milan_soc.py` consumes it, so the LiteX `milan_mac_phy_crg_reset` CSR is NOT gated. Writing exactly `0x554E4C4B` (ASCII `UNLK`) clears it; any other written value sets it. While it is 1, writes to `PHY_RESET` are dropped; `LINK_CTRL[1]` (MAC_REINIT) is stored as 0. |

| Note |
|---|
| The readback is the guard flop itself, so a refused write never reads back as accepted. The RTL comments on the `o_eth_guard` port and on `A_ETH_GUARD` in `hdl/common/csr/milan_csr.sv` say the guard also gates the LiteX PHY reset chain; the SoC does not implement that gating at this head (issue #797 records the decision it needs). |

## 0x7DC  -  retired AS_PATH compatibility addresses

Retired AS_PATH addresses and the live PathTrace status.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7DC` | `ASP_LO` | AS_PATH staging, low word (retired) | `0x00000000` | [section](#asp_lo-register-offset-0x7dc-reset--0x00000000) |
| `0x7E0` | `ASP_HI` | AS_PATH staging, high word (retired) | `0x00000000` | [section](#asp_hi-register-offset-0x7e0-reset--0x00000000) |
| `0x7E4` | `ASP_CMD` | AS_PATH status | `0x000000XX` | [section](#asp_cmd-register-offset-0x7e4-reset--0x000000xx) |

| Note |
|---|
| Group summary inert AS_PATH compatibility addresses; the product serves the engine's bounded PathTrace (0x0056) |
| `GET_AS_PATH` (IEEE 1722.1-2021 7.4.41.2) returns the fabric engine's atomic, bounded pathTrace publication, entry 0 first. The engine publishes eight identities from entry 0 and their count (FPGA-gPTP #87, #88); entry 0 is served as published, never replaced by the grandmaster identity. |
| IEEE 802.1AS-2011 10.3.10.2.1 d), the edition Milan v1.2 profiles, writes pathTrace only from a received path trace TLV: its pathSequence is copied as received and thisClock appended (FPGA-gPTP #85), so the count includes thisClock. The copy keeps the received head, which need not be the grandmaster, and an empty pathSequence gives `{thisClock}` (FPGA-gPTP #88). When the selected Announce carries no TLV, nothing is written and pathTrace keeps its previous value (FPGA-gPTP #87): `{thisClock}` after reset or mastership (10.3.12.1.1, 10.3.12.1.4 i), with Cor1-2013, FPGA-gPTP #82), and otherwise the last path copied from a TLV, even across a grandmaster change. |
| The publication holds eight identities, which bounds that append. At eight or more received entries the served sequence is the first eight received entries, the count stays 8 and thisClock is not appended (FPGA-gPTP #86). Up to seven received entries always gain thisClock. |
| The three addresses below remain allocated so the public map does not shift. The staging pair is always zero and all writes are discarded. `ASP_CMD` is a read-only view of the selected fabric owner's `{generation,count}` in product mode and reads zero in option OFF. None of these addresses can change `GET_AS_PATH`, its Table 5.22 edge, or any generation counter. Option OFF therefore has an empty path and zero runtime owners. |

### ASP_LO register (offset 0x7DC) [reset = 0x00000000]

Retired AS_PATH address; reads zero.

RTL name: `A_ASP_LO`.

![ASP_LO bit fields](../../docs/diagrams/regmap/asp/ASP_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ASP_LO` | R | 0 | Retired slot; reads zero and writes are discarded. |

### ASP_HI register (offset 0x7E0) [reset = 0x00000000]

Retired AS_PATH address; reads zero.

RTL name: `A_ASP_HI`.

![ASP_HI bit fields](../../docs/diagrams/regmap/asp/ASP_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `ASP_HI` | R | 0 | Retired slot; reads zero and writes are discarded. |

### ASP_CMD register (offset 0x7E4) [reset = 0x000000XX]

Generation and length of the fabric's selected PathTrace.

RTL name: `A_ASP_CMD`.

![ASP_CMD bit fields](../../docs/diagrams/regmap/asp/ASP_CMD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:8 | `RESERVED` | R | 0 | Reserved. |
| 7:4 | `ASP_GEN` | R | X | fabric publication generation |
| 3:0 | `ASP_COUNT` | R | X | path count; option OFF reads zero and all writes are discarded. |

## 0x7E8  -  gPTP plane drop diagnostics

gPTP plane drop counters.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7E8` | `GPTP_DROPW` | gPTP wire drops | `0xXXXXXXXX` | [section](#gptp_dropw-register-offset-0x7e8-reset--0xxxxxxxxx) |
| `0x7EC` | `GPTP_DROPE` | gPTP event drops | `0xXXXXXXXX` | [section](#gptp_drope-register-offset-0x7ec-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary gPTP plane drop diagnostics: tap/parser/event drop counts, RO live (#207) |
| A field failure must distinguish silence on the link from traffic the plane refused inside (issue #207). The plane's three drop counters reach software here: frames the tap FIFO shed, frames the parser refused, and events the dispatch queue lost. Each source is a 16-bit free-running counter clocked in the plane; it wraps and is never cleared by a read or a write, so software computes deltas. The words are served live from the wires - no snapshot, no selector - and each 32-bit read is coherent for the pair it carries. Reset zeroes the counters with the plane. Option OFF reads defined zeros from the parameter gate itself, never a floating count, and every write is discarded. |

### GPTP_DROPW register (offset 0x7E8) [reset = 0xXXXXXXXX]

gPTP frames lost at the tap or the parser.

RTL name: `A_GPTP_DROPW`.

![GPTP_DROPW bit fields](../../docs/diagrams/regmap/gptpd/GPTP_DROPW.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `GPTP_TAP_DROP` | R | X | tap-FIFO drop count |
| 15:0 | `GPTP_RX_DROP` | R | X | parser refusal count; both 16-bit wrapping; option OFF reads zero. |

### GPTP_DROPE register (offset 0x7EC) [reset = 0xXXXXXXXX]

Lost launch records and refused gPTP events.

RTL name: `A_GPTP_DROPE`.

![GPTP_DROPE bit fields](../../docs/diagrams/regmap/gptpd/GPTP_DROPE.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `GPTP_TXTS_LOST` | R | X | `GPTP_TXTS_LOST` (issue #360): egress launch records that closed with NO timestamp - an admitted frame whose entry a barrier cancelled, a record the launch observer aborted, or a reconstruction refused because the PHC trajectory across the interval was outside the model. Nonzero here is the plane saying which frames it could not time, rather than publishing a plausible one. |
| 15:0 | `GPTP_EV_DROP` | R | X | events the dispatch queue refused - a full queue, or an announce arriving without its frozen capture context. Both 16-bit wrapping; option OFF reads zero. |

## 0x7F0  -  applied gPTP timestamp latency corrections

The timestamp corrections the gPTP plane applies.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x7F0` | `GPTP_LAT` | gPTP latency corrections | `0xXXXXXXXX` | [section](#gptp_lat-register-offset-0x7f0-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary applied gPTP timestamp latency corrections, RO live (#358) |
| The board's own ingress and egress timestamp latency corrections, as the fabric gPTP plane is **actually applying them** (issue #358). They are elaboration constants: declared per board in the `gptp:` section of the end-station configuration, carried by the builder into `GPTP_INGRESS_LAT_NS_P` / `GPTP_EGRESS_LAT_NS_P`, and republished here so a controller host and the UART `milan_status` line read what the gateware is doing rather than what a configuration file elsewhere says it should be. The plane SUBTRACTS the ingress value from every arrival stamp and ADDS the egress value to every reconstructed launch. |
| One word, because a reader must never pair one build's ingress with another's egress. Sixteen bits per direction is the applied range: the builder and `KL_gptp_shadow` both refuse a wider value rather than let an applied correction read back truncated. |
| **This is the only live latency-correction publication.** `PTP_INGRESS_LAT` (`0x540`) and `PTP_EGRESS_LAT` (`0x544`) remain readable, inert scratch with no timestamp consumer, and that is deliberate: one owner cannot be two, and a correction applied twice is worse than one applied nowhere. See the [gPTP plane](../design/GPTP_PLANE.md#timestamp-boundaries) for what each correction absorbs and for the open bound on the split between them. |

### GPTP_LAT register (offset 0x7F0) [reset = 0xXXXXXXXX]

Ingress and egress timestamp corrections the plane applies.

RTL name: `A_GPTP_LAT`.

![GPTP_LAT bit fields](../../docs/diagrams/regmap/gptpl/GPTP_LAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `GPTP_LAT_NS` | R | X |  |

| Note |
|---|
| `[31:16]` ingress correction, nanoseconds, SUBTRACTED from every arrival timestamp; `[15:0]` egress correction, nanoseconds, ADDED to every reconstructed launch timestamp. Elaboration constants, so the value is fixed for the bitstream and a write changes nothing. Option OFF reads zero. The shipping AX7101 build reads `0x0290_00DB` = 656 ns and 219 ns, whose sum is the 875 ns of total stamp error an inline tap measured on 2026-09-20; the Arty builds read `0` because no one has measured them on this plane. |

## 0x800  -  Indexed per-stream window

Indexed window onto one stream's context.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x800` | `STRM_SEL` | Stream window select | `0x00000000` | [section](#strm_sel-register-offset-0x800-reset--0x00000000) |
| `0x804` | `STRM_SNAP` | Stream window snapshot | `0x00000000` | [section](#strm_snap-register-offset-0x804-reset--0x00000000) |
| `0x810` | `STRMW_CTRL` | Stream window control | `0xXXXXXXXX` | [section](#strmw_ctrl-register-offset-0x810-reset--0xxxxxxxxx) |
| `0x814` | `STRMW_SID_LO` | Stream window stream ID, low word | `0xXXXXXXXX` | [section](#strmw_sid_lo-register-offset-0x814-reset--0xxxxxxxxx) |
| `0x818` | `STRMW_SID_HI` | Stream window stream ID, high word | `0xXXXXXXXX` | [section](#strmw_sid_hi-register-offset-0x818-reset--0xxxxxxxxx) |
| `0x81C` | `STRMW_DMAC_LO` | Stream window destination MAC, low word | `0xXXXXXXXX` | [section](#strmw_dmac_lo-register-offset-0x81c-reset--0xxxxxxxxx) |
| `0x820` | `STRMW_DMAC_HI` | Stream window destination MAC, high word | `0xXXXXXXXX` | [section](#strmw_dmac_hi-register-offset-0x820-reset--0xxxxxxxxx) |
| `0x824` | `STRMW_FMT_LO` | Stream window format, low word | `0xXXXXXXXX` | [section](#strmw_fmt_lo-register-offset-0x824-reset--0xxxxxxxxx) |
| `0x828` | `STRMW_FMT_HI` | Stream window format, high word | `0xXXXXXXXX` | [section](#strmw_fmt_hi-register-offset-0x828-reset--0xxxxxxxxx) |
| `0x82C` | `STRMW_STATE` | Stream window state | `0xXXXXXXXX` | [section](#strmw_state-register-offset-0x82c-reset--0xxxxxxxxx) |
| `0x830` | `STRMW_CNTn` | Stream window counter | `0xXXXXXXXX` | [section](#strmw_cntn-registers-offset-0x830-to-0x854-stride-0x4-reset--0xxxxxxxxx) |
| `0x858` | `STRMW_PDUS` | Stream window PDU count | `0xXXXXXXXX` | [section](#strmw_pdus-register-offset-0x858-reset--0xxxxxxxxx) |
| `0x85C` | `STRMW_SRP` | Stream window SRP status | `0xXXXXXXXX` | [section](#strmw_srp-register-offset-0x85c-reset--0xxxxxxxxx) |
| `0x860` | `STRMW_CTLR_LO` | Stream window controller, low word | `0xXXXXXXXX` | [section](#strmw_ctlr_lo-register-offset-0x860-reset--0xxxxxxxxx) |
| `0x864` | `STRMW_CTLR_HI` | Stream window controller, high word | `0xXXXXXXXX` | [section](#strmw_ctlr_hi-register-offset-0x864-reset--0xxxxxxxxx) |
| `0x868` | `STRMW_BIND` | Stream window binding | `0xXXXXXXXX` | [section](#strmw_bind-register-offset-0x868-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary Indexed per-stream window (NxN streams, SEL/SNAP + 0x810-0x868) |
| One SELECT register plus ONE decoded word block views any of the N listener / N talker stream contexts -- decode area is O(1) in N instead of the O(N) flat replication (~500 words at 8x8). The reader is bare-metal firmware: SEL-then-read sequencing costs nothing. |
| 🔴 **TWO PORTS OF THIS WINDOW ARE DEAD AT VERSION MAJOR 2.** * **The ACMP context-table read.** There is no ACMP context table in this fabric any more -- the protocol processor keeps its bind state internally and publishes only the bound record -- so the window's grant **never asserts** and the record reads a **structural zero**. That covers `A_STRMW_CTLR_LO/HI` (`0x860`/`0x864`) and `A_STRMW_BIND` (`0x868`), the E2 saved-state words. * **The SRP attribute-row port.** There is no attribute-row table either. No grant is ever issued, `i_srp_ctx_stolen` never asserts, and the readback is a structural zero: **a write to the provisioning port is accepted by the CSR and lands nowhere.** `A_STRMW_SRP` (`0x85C`) reads a structural zero at every index. Everything else in this window -- the stream table, the listener and talker context words, the per-stream counters, the format and identity words -- is unaffected and still live. The prose below describing the lwSRP row map, fabric-owned talker-row provisioning, the arbitration rules and the `0xDEADDEAD` not-backed sentinel is preserved as the record of what that port did and as the specification a replacement must meet; none of it acts today. The SRP state a reader actually wants is published by the processor's class-D face and appears in the `0x680` group (`LWSRP_STATUS`, `LWSRP_SLOPE`, `LWSRP_DOM`). |
| `N_LISTENERS_P` / `N_TALKERS_P` are elaboration parameters of `milan_csr`. **They both default to 1 in the RTL, and the shipping AX7101 (`endstation_ax7101_1x1_tdm8`) is the one-AAF-stream shape**; `endstation_ax7101_8x8.yaml` declares 8 of each -- `milan_datapath` drives both from its own `N_STREAMS`, which the builder sets to `max(listeners, talkers)` from the config, and [`configs/endstation_ax7101_8x8.yaml`](../../configs/endstation_ax7101_8x8.yaml) declares 8 of each (`test_builder.py` gate 2 pins `--num-streams 8` for that board). The Arty config declares one of each, so that board *is* the N = 1 shape and every window word there is the flat alias described below. **Read the count off the build, never off this page**: the index is only 4 bits wide and an out-of-range selection reads 0, which is indistinguishable from a real zero at a glance. |
| **The `0xDEADDEAD` not-backed rule (0x000C).** A window word that does not exist for the selected direction/index reads the POISON value `0xDEADDEAD`, never 0 -- firmware or a diagnostic master can tell "this word is not backed here" from a true zero at first glance. Out-of-range index reads stay 0 (a different condition: the selection itself is invalid). |
| **The alias rule (N=1 bit-compat axiom).** The legacy flat registers remain the authority and index 0 of the window is a HARD ALIAS of them -- never a copy: |
| talker idx 0 `CTRL[0]`/`DMAC_LO`/`DMAC_HI` are the same storage as `AAF_CTRL[0]`/`AAF_DMLO`/`AAF_DMHI` (a window write is visible at the flat address and vice versa; the `CTRL` alias merges bit 0 only), |
| `SRP` idx 0 is the live `0x694` word, and |
| the listener idx-0 SNAP latches the flat `AVTPRX_*`/`PCMRX_CNT`/`ACMPL_STATE` sources (`CNT0..3/5/6` mirror today's truncated 8/16-bit flat counters -- the idx-0 SNAP deliberately keeps the flat sources in P12 too, which IS the alias axiom; extra contexts read the full 32-bit LCTX words). |
| Every pre-window CSR TB passes unchanged. `PCMRX_CNT` (0x6C4) stays the SHARED depacketizer's global `{drops,pdus}` across all streams; per-stream pdus live in the window `PDUS` word. |
| **SNAP atomicity ([M-5.4.2.25] GET_COUNTERS).** A SNAP latches `STATE` + `CNT0..9` + `PDUS` as one coherent set. Index 0 latches all flat sources in a single cycle. Extra contexts run an engine-arbitrated burst on the context RAM's port B; `busy` covers the whole burst; the latched words serve reads until the next SNAP (they do NOT track live counters). Firmware GET_COUNTERS = `SEL`, `SNAP`, poll `busy`, read the block. |
| **P12 coherence level (engine-backed, VERSION 0x0009).** The live engines serve each burst word only when fully event-drained, so every latched WORD is event-atomic and reflects a completely-applied event state; the engines do not freeze across the whole burst, so a block whose fetch straddles an in-flight event is bounded by the burst's start/end states (counters are monotonic, reset only on that stream's bind edge). |
| Engine-backed CFG words (`CTRL`/`FMT` listener side, `CTRL`/`DMAC` extra talker contexts) are "slow" reads served live from the context RAM (>= 4 AXI-stalled cycles, longer while the engine walks an event). A listener `CTRL` commit at any idx also writes the classification stream-table entry `{sid staged via SID_LO/HI, en}` and the route field. |
| **Listener route (`CTRL[2:1]`, `KL_pcm_route`).** The two-bit ABI remains, but only `CTRL[2]` is implemented: it selects the stream as a physical-render candidate. `CTRL[1]` is reserved, is masked on write, and reads zero. If several streams request render, the lowest index wins deterministically. The monitor and depacketizer still consume every accepted stream whether or not it is selected for render. |
| Reset default: stream 0 = `0b10`, others `0b00`. |
| **Talker t>0 arming (`aaf_stream_en_w`, mirrored since 0x000C).** Talker stream 0's admission is the flat `aaf_gate` unchanged (`AAF_CTRL` en/bypass, MAAP claim, ACMP talker-active, lwSRP row-0 gate). A talker idx>0 arms with the SAME composition, term by term: |
| `AAF_CTRL[0]` -- the SAME flat enable stream 0 uses. **Since `0x001F` there is no per-context arming bit.** TCTX `CTRL[0]` used to be ANDed here, and it reset to 0 with no board-software writer, so on a shape-static build (`0x0015`+) *no talker above 0 could ever egress* -- measured on silicon m001g as the bind soak's `t0` leg fully green while `t1/t2/t3` sat at zero frames despite `CONNECT` SUCCESS, declared SRP rows and `tu=0`. It was **removed rather than inverted**: 1722.1-2021 Table 8-4 bit 12 makes `STREAMING_WAIT` an *option*, Milan v1.2 5.4.2.19/5.4.2.20 require `NOT_SUPPORTED` for `START_`/`STOP_STREAMING` on a Stream Output, 5.3.7.3 "excludes the possibility for a Stream Output to be stopped", and 5.5.4.1 says a Talker "shall always stream AVTP packets as long as bandwidth is reserved" -- a per-stream software enable is not ours to have. The word still carries chans/VID; bit 0 is simply no longer consulted by anything. AND |
| the engine-wide MAAP term (`~MAAP_CTRL[0] \| addr_valid` -- ONE claim engine claims a BLOCK of N addresses; stream j transmits and answers probes with base+j) AND |
| `AAF_CTRL[1]` bypass OR (per-stream ACMP talker_active AND the per-stream lwSRP bw-gate with the `~LWSRP_CTRL[0]` escape). |
| The per-stream ACMP term comes from `KL_acmp_tlkr_ctx` at `N_SRC_P = N_STREAMS` (0x000C): CONNECT_TX/PROBE_TX answers SUCCESS for every `talker_unique_id` 0..N-1 (stream_id `{station MAC, uid}`, dest_mac `MAAP base + uid`), each uid keeping its own Milan Section 4.3.3.1 15 s probe window; `talker_active[j>0]` = probe window open OR that stream's reservation row live (a granted per-stream reservation implies a ready listener); `A_ACMP_LOBS[0]` overrides every stream. Note the sample-source reality: the PHYSICAL I2S capture front-end emits slot 0 only -- an armed t>0 emits frames when the chmap capture crossbar ([Sections 4/5 of `../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md#4-capture-mux-contract-kl_chmap_capture-phase-1-name)) feeds its pair slots (any source, TONE included). |
| **AAF talker-row provisioning is FABRIC-OWNED (2026-07-30).** The lwSRP provisioning port used to have exactly two writers -- this window and the fabric's CRF Media Clock Output row -- and **no board software drives this window**, so no AAF talker row above 0 ever held a reservation. Measured twice: |
| CSR, live read through `A_STRM_SEL` `0x100+idx`: `A_STRMW_SRP` (`0x85C`) = `0x0000_037E` at talker idx 0 and `0x0000_0000` at idx 1/2/3 on a 4×4 board. Idx 0 is a live hard alias of the legacy flat row, which is exactly why idx-0-only reads looked healthy. |
| WIRE, ProfiShark inline on the board link with a licensed stream running: MSRP declared a Talker Advertise for exactly `{02:00:00:00:00:02, uid 0x0000}` and `{…, uid 0x0004}` -- uid 4 is `N_STREAMS`, i.e. the CRF output -- and **nothing** for uid 1/2/3. The two stream_ids on the wire were precisely the two rows that had a provisioner. |
| Milan v1.2 Section 5.3.7.3 conditions streaming on declaring a Talker Advertise AND receiving a Listener Ready/Ready Failed, so an unadvertised stream can never be licensed: no talker but 0 could stream. Every AAF talker row now has a fabric requester of its own (`milan_datapath` `aaf_srp_prov`), modelled on the CRF one and sharing one rotating arbiter with it: |
| the **want** is `TCTX CTRL[0]` (this window's `0x810` en) AND `LWSRP_CTRL[0]` AND `LWSRP_CTRL[1]`. Upstream terms only -- the per-stream bw-gate is an *output* of the engine, so wanting on it deadlocks. It deliberately does NOT include ACMP talker-active: Milan Section 5.5.2.7 licences a stream on SRP alone, so the advertisement has to exist BEFORE a controller binds or fast-connect (Section 5.5.3.5.3) finds no reservation to register against; |
| the **identity** is derived: stream_id `{station MAC, uid = idx}` and DMAC = MAAP block base+idx, the same values the ACMP responder answers a `PROBE_TX` for that `talker_unique_id` with, so the declaration and the answer cannot disagree. TSpec `MaxFrameSize` = `24 + 24*C` from that row's own TCTX `CTRL` chans field; `MaxIntervalFrames` stays shared (an SR-class property); |
| clearing `CTRL[0]` **withdraws** the row (valid → 0, one LV PDU if the attribute was on the wire), and re-enabling re-declares it; |
| **software still wins if it names a stream_id** -- the `CRFT_SID` precedent applied per row. A `CTRL` commit carrying a non-zero sid staged for THAT selection takes the row and the fabric stands down without withdrawing it; a commit naming none (which is what every plain enable is) is retaken by the fabric, because a row holding the zero sid is a reservation for a stream this station does not emit. |
| Arbitration, for anyone adding a third fabric writer: a pending CSR **write** masks every fabric grant (a write is a discrete committed operation), the CSR **poll** does not (it is level-high forever while a non-zero row is selected -- gating on it pinned the first fabric requester off permanently), a yielded poll beat is marked stale through `i_srp_ctx_stolen`, and the fabric slots rotate so a served slot becomes the lowest priority. |
| **Bench warning (2026-07-26 silicon).** With `LWSRP_CTRL[0]` cleared the CBS slope mux disengages, so an admitted talker stream transmits UNPACED (measured ≈56 k frames/s against the paced 10.4 k/s on the AX 8×8) -- a 100M listener port drowns in minutes. Open t>0 admission through real per-stream reservations (or keep windows short) -- never leave the engine off with armed extra talkers. |
| **Engine-backed words + read timing.** Window reads of LCTX/TCTX-backed words (`CTRL`/`FMT` listener side, `CTRL`/`DMAC` extra talker contexts) are served from the context RAM's second port -- the AXI read simply stretches a few clocks (handshake absorbs it, like the config-shadow reads). |
| While the lane-K engines are not connected, those inputs are tied inert at the SoC (`i_lctx_rd_data=0`, `i_lctx_snap_ok=1`, same for TCTX, `i_acmp_tbl_*=0` -- allowlisted in [`scripts/check_tied_inputs.sh`](../../scripts/check_tied_inputs.sh)), so engine-backed words read 0 and SNAP completes immediately; the index-0 aliases are fully live today. During a SNAP burst, engine-backed word reads return 0 (poll busy first). |
| **lwSRP provisioning through the window.** For idx>0, writing `SID_LO/HI` (+ `DMAC_LO/HI` for talkers) stages the record and a `CTRL` write commits it to the live lwSRP attribute-context port (`KL_lwsrp_top ctx_*`): `en`=1 provisions (TalkerAdvertise or Listener declaration per dir), `en`=0 withdraws. |
| Row map: listener idx k → ctx row k, talker idx t → ctx row `N_LISTENERS_P-1+t`; row 0 is the legacy pair (read-only, served by the flat aliases). PriorityAndRank is the class-A constant; TSpec/latency come from the shared `LWSRP_TSPEC`/`LWSRP_LATENCY` registers until per-stream TSpec words exist. |
| **Out-of-range rule.** idx ≥ `N_LISTENERS_P` (dir 0) / `N_TALKERS_P` (dir 1): every window word reads 0, writes are ignored (no alias, no engine strobes, no provisioning), SNAP latches zeros and completes. `A_STRM_SEL` / `A_STRM_SNAP` themselves always decode. |

### STRM_SEL register (offset 0x800) [reset = 0x00000000]

Selects the stream the 0x810 to 0x868 words view.

RTL name: `A_STRM_SEL`.

![STRM_SEL bit fields](../../docs/diagrams/regmap/strm/STRM_SEL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:10 | `RESERVED` | R | 0 | Reserved. |
| 9 | `STRM_LSN0` | W | 0 |  |
| 8 | `STRM_DIR` | R/W | 0 |  |
| 7:4 | `RESERVED` | R | 0 | Reserved. |
| 3:0 | `STRM_IDX` | R/W | 0 |  |

| Note |
|---|
| `[3:0]` stream index, `[8]` dir (0 = listener, 1 = talker), `[9]` **listener-0 row select (since VERSION `0x0023`)**: 1 = the window serves sink 0's dedicated lwSRP row (`SRP_LSN0_ROW_C = L+T-1`); `[8]`/`[3:0]` are ignored while set. `{dir=0, idx=0}` is the PARK state. Only these bits are stored/read back. Writing SEL invalidates the ACMP/SRP read snapshots. Until a re-poll lands, snapshot-served words read zero, meaning "not fresh yet", not "no bind". Firmware must read until a value repeats if another firmware task may move SEL; see [TROUBLESHOOTING Section 21](../limitations/TROUBLESHOOTING.md). |

### STRM_SNAP register (offset 0x804) [reset = 0x00000000]

Latches the selected stream's state and counters.

RTL name: `A_STRM_SNAP`.

![STRM_SNAP bit fields](../../docs/diagrams/regmap/strm/STRM_SNAP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R | 0 | Reserved. |
| 0 | `SNAP_BUSY` | R/W1S | 0 |  |

| Note |
|---|
| Write `[0]`=1: latch the selected stream's `STATE` + `CNT0..9` + `PDUS` into the window shadow as ONE coherent block. Read: `[0]` busy. Poll busy=0 before reading the latched words |

### STRMW_CTRL register (offset 0x810) [reset = 0xXXXXXXXX]

Enable and route flags of the selected stream.

RTL name: `A_STRMW_CTRL`.

![STRMW_CTRL bit fields](../../docs/diagrams/regmap/strm/STRMW_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `STRMW_CTRL_31_1` | R/W | X | A write takes effect only when `win_in_range_w !strm_dir_r`. A write takes effect only when `win_in_range_w not !strm_dir_r not strm_idx_r == 4'd0`. |
| 0 | `STRMW_CTRL_0` | R/W | X | A write takes effect only when `win_in_range_w !strm_dir_r`. A write takes effect only when `win_in_range_w not !strm_dir_r not strm_idx_r == 4'd0`. A write takes effect only when `win_in_range_w not !strm_dir_r strm_idx_r == 4'd0`. |

| Note |
|---|
| listener: `[0]` en, `[2:1]` route flags `{[2] RENDER, [1] reserved-zero}`; only the render route is implemented (LCTX w4). Talker idx 0: `[0]` en = **hard alias of `AAF_CTRL[0]`** (merge write -- VID/bypass bits untouched); talker idx>0: TCTX w0 (`[0]` en arms the stream -- the per-stream admission composition, see the talker t>0 paragraph). A CTRL write at idx>0 also COMMITS the lwSRP provisioning record (see below). **Staging rule (VERSION ≥ `0x000F`): a CTRL commit overrides the stream table only when a stream_id was staged FOR THIS INDEX** via `A_STRMW_SID_LO/HI` -- staging for one index then committing another no longer arms the second with the first's sid. **`[0]`=0 with no sid staged for this index is RELEASE-TO-ALIAS**: it commits the zero sid, which disarms the override so entry 0 returns to the live ACMP bound record. An eviction that *does* carry a staged sid is a deliberate disable and keeps the override armed. **The SAME staging guard now covers the lwSRP provisioning record (2026-07-30)** -- it used to take the staging set unconditionally, and those four words are ONE register set shared by every index, so a sid staged for one selection was written into whatever row was committed next (measured at the desk: talker idx2's attribute row read back the sid staged for listener idx2, i.e. a Talker Advertise for a stream this station does not emit). A commit that names **no** sid for this selection provisions the row with a ZERO sid, which for an AAF talker row idx>0 is RELEASE-TO-FABRIC (see the talker-row provisioning paragraph). Ownership is by SELECTION, not spent by the commit: repeated `CTRL` writes at the index a sid was staged for keep that sid |

### STRMW_SID_LO register (offset 0x814) [reset = 0xXXXXXXXX]

stream_id bits 31 to 0 of the selected stream.

RTL name: `A_STRMW_SID_LO`.

![STRMW_SID_LO bit fields](../../docs/diagrams/regmap/strm/STRMW_SID_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_SID_LO` | R/W | X | A write takes effect only when `win_in_range_w`. A write takes effect only when `win_in_range_w !strm_dir_r`. |

| Note |
|---|
| stream_id `[31:0]`. listener: RO from the ACMP bind context (tbl port); talker idx 0: RO derived `{station MAC, uid=0}`; talker idx>0: RO from the lwSRP row snapshot, which since 2026-07-30 reads the FABRIC-derived `{station MAC, uid=idx}` unless software named a sid for this selection. Writes stage the provisioning sid (and forward to LCTX w0 for listeners); the staging set is bound to the `{dir, idx}` it was written under. **A talker's word is the ID it starts with, not its current one:** after a MAAP conflict the processor moves a declared source to a new Stream ID (processor #202, #799). The current ID is the one its frames carry and `PROBE_TX`, `GET_TX_STATE` and `GET_STREAM_INFO` answer; this word does not follow it |

### STRMW_SID_HI register (offset 0x818) [reset = 0xXXXXXXXX]

stream_id bits 63 to 32 of the selected stream.

RTL name: `A_STRMW_SID_HI`.

![STRMW_SID_HI bit fields](../../docs/diagrams/regmap/strm/STRMW_SID_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_SID_HI` | R/W | X | A write takes effect only when `win_in_range_w`. A write takes effect only when `win_in_range_w !strm_dir_r`. |

| Note |
|---|
| stream_id `[63:32]`, same rules (LCTX w1) |

### STRMW_DMAC_LO register (offset 0x81C) [reset = 0xXXXXXXXX]

Destination MAC bits 31 to 0 of the selected stream.

RTL name: `A_STRMW_DMAC_LO`.

![STRMW_DMAC_LO bit fields](../../docs/diagrams/regmap/strm/STRMW_DMAC_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_DMAC_LO` | R/W | X | A write takes effect only when `win_in_range_w`. A write takes effect only when `win_in_range_w strm_dir_r not strm_idx_r == 4'd0`. A write takes effect only when `win_in_range_w strm_dir_r strm_idx_r == 4'd0`. |

| Note |
|---|
| stream DMAC `[31:0]`. listener: RO ACMP bind context; talker idx 0: **hard alias of `AAF_DMLO`** (RW, exact); talker idx>0: TCTX w1 (engine-backed). Writes stage the provisioning DMAC |

### STRMW_DMAC_HI register (offset 0x820) [reset = 0xXXXXXXXX]

Destination MAC bits 47 to 32 of the selected stream.

RTL name: `A_STRMW_DMAC_HI`.

![STRMW_DMAC_HI bit fields](../../docs/diagrams/regmap/strm/STRMW_DMAC_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_DMAC_HI` | R/W | X | A write takes effect only when `win_in_range_w`. A write takes effect only when `win_in_range_w strm_dir_r not strm_idx_r == 4'd0`. A write takes effect only when `win_in_range_w strm_dir_r strm_idx_r == 4'd0`. |

| Note |
|---|
| DMAC `[47:32]` in `[15:0]`; talker idx 0 = **hard alias of `AAF_DMHI`**; talker idx>0: TCTX w2, whose `[31:16]` unique ID the integrated framer no longer stamps: every AAF talker's stream_id is the processor's current one (`KL_aaf_packetizer` `SID_PP_P`, processor #202, #799) |

### STRMW_FMT_LO register (offset 0x824) [reset = 0xXXXXXXXX]

Current stream format bits 31 to 0.

RTL name: `A_STRMW_FMT_LO`.

![STRMW_FMT_LO bit fields](../../docs/diagrams/regmap/strm/STRMW_FMT_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_FMT_LO` | R/W | X | A write takes effect only when `win_in_range_w && !strm_dir_r`. |

| Note |
|---|
| current stream format `[31:0]` (LCTX w2, engine-backed; talker side is AECP-owned -- reads `0xDEADDEAD`, writes ignored) |

### STRMW_FMT_HI register (offset 0x828) [reset = 0xXXXXXXXX]

Current stream format bits 63 to 32.

RTL name: `A_STRMW_FMT_HI`.

![STRMW_FMT_HI bit fields](../../docs/diagrams/regmap/strm/STRMW_FMT_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_FMT_HI` | R/W | X | A write takes effect only when `win_in_range_w && !strm_dir_r`. |

| Note |
|---|
| format `[63:32]` (LCTX w3; talker side reads `0xDEADDEAD`) |

### STRMW_STATE register (offset 0x82C) [reset = 0xXXXXXXXX]

Snapshot-latched state word of the selected stream.

RTL name: `A_STRMW_STATE`.

![STRMW_STATE bit fields](../../docs/diagrams/regmap/strm/STRMW_STATE.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_STATE` | R | X |  |

| Note |
|---|
| Snap-latched pack. listener: `[2:0]` ACMP lsm state, `[4:3]` probing, `[9:5]` acmp_status, `[10]` media_locked, `[18:11]` wire_chans, `[27:19]` SRP bits (= low 9 bits of `A_STRMW_SRP`). talker (LIVE per-stream since 0x000C: bits `[3:0]` at idx>0 were hardwired 0 before, the 2026-07-26 window-honesty fix): `[0]` probe_armed, `[1]` talker_active, `[2]` lobs (`A_ACMP_LOBS`, or with `LWSRP_CTRL[0]` set: at idx 0 source 0's registered Listener Ready or Ready Failed, at idx > 0 that source's ACTIVE since #530), `[3]` composed admission (`aaf_stream_en[idx]`; idx 0 = `aaf_gate`), `[27:19]` SRP bits |

### STRMW_CNTn registers (offset 0x830 to 0x854, stride 0x4) [reset = 0xXXXXXXXX]

One of the ten snapshot-latched Stream Input counters.

RTL name: `A_STRMW_CNT0..9 (A_STRMW_CNT0 to A_STRMW_CNT_END)`.

![STRMW_CNTn bit fields](../../docs/diagrams/regmap/strm/STRMW_CNTn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `SNAP_SHADOW` | R | X | The 10 Milan Table 5.6 / 1722.1-2021 Table 7-157 STREAM_INPUT counters at the Table 7-157 word offsets 0..36: MEDIA_LOCKED, MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP, FRAMES_RX. **Full 32-bit** -- this is the authoritative width; the flat `AVTPRX_STAT`/`AVTPRX_ERR` words are saturating 8/16-bit summaries of these. Until VERSION `0x0013` the index-0 words were re-derived from those packed views and inherited their truncation (and MEDIA_RESET / LATE / EARLY_TIMESTAMP read a hard 0 while the monitor was counting them), so there was **no** full-width path anywhere. Talker contexts read `0xDEADDEAD` (the not-backed rule below). **The two Milan 1.3 5.3.8.10 additions -- TIMESTAMP_VALID / TIMESTAMP_NOT_VALID (per-frame tv-bit tallies, LCTX words 26/27, `TV + TNV == FRAMES_RX`) -- are NOT window-exposed** (the `0x858+` words were already claimed); they are served by AECP GET_COUNTERS at the 1722.1-2021 block offsets 24/28 under valid mask `0xFFF` (was `0xF3F`), and a bench read can fetch LCTX w26/w27 through the raw `lctx` read port if ever needed |

### STRMW_PDUS register (offset 0x858) [reset = 0xXXXXXXXX]

Snapshot-latched PDU and drop counts of the selected stream.

RTL name: `A_STRMW_PDUS`.

![STRMW_PDUS bit fields](../../docs/diagrams/regmap/strm/STRMW_PDUS.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_PDUS` | R | X | listener: `{drops[31:16], pdus[15:0]}` (= `PCMRX_CNT` at idx 0); talker: per-stream frames_sent (idx 0 = `AAF_FRAMES`; idx>0 = the packetizer ctx FRAMES word, snap-fetched through the TCTX port) |

### STRMW_SRP register (offset 0x85C) [reset = 0xXXXXXXXX]

SRP status of the selected stream.

RTL name: `A_STRMW_SRP`.

![STRMW_SRP bit fields](../../docs/diagrams/regmap/strm/STRMW_SRP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_SRP` | R | X | 🔴 **STRUCTURAL ZERO at every index.** There is no lwSRP attribute-row table in this fabric any more, so the window's SRP port is never granted and this word reads 0 -- including at idx 0, whose live hard alias of `LWSRP_STATUS` (`0x694`) went with the port. Read `LWSRP_STATUS` `0x694` directly instead: it carries the processor's class-D declaration/registration levels for the whole plane. Was: `{valid, dir, declared, registered, ready, failed, decl[1:0], fail_code[7:0]}` from the selected context row, with `0xDEAD` for a row above `N_CTX_P` |

### STRMW_CTLR_LO register (offset 0x860) [reset = 0xXXXXXXXX]

Retired binding controller ID, a structural zero.

RTL name: `A_STRMW_CTLR_LO`.

![STRMW_CTLR_LO bit fields](../../docs/diagrams/regmap/strm/STRMW_CTLR_LO.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_CTLR_LO` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO.** Was the binding controller_entity_id `[31:0]` from the ACMP bind context (E2, 5.5.3.5.3 step 2). The processor publishes a bound record -- stream_id, DMAC, VLAN -- and not the binding controller's identity, so there is no source for this word |

### STRMW_CTLR_HI register (offset 0x864) [reset = 0xXXXXXXXX]

Retired binding controller ID, a structural zero.

RTL name: `A_STRMW_CTLR_HI`.

![STRMW_CTLR_HI bit fields](../../docs/diagrams/regmap/strm/STRMW_CTLR_HI.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_CTLR_HI` | R | X |  |

| Note |
|---|
| 🔴 **STRUCTURAL ZERO.** Was controller_entity_id `[63:32]` |

### STRMW_BIND register (offset 0x868) [reset = 0xXXXXXXXX]

Retired binding flags and talker ID, a structural zero.

RTL name: `A_STRMW_BIND`.

![STRMW_BIND bit fields](../../docs/diagrams/regmap/strm/STRMW_BIND.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `STRMW_BIND` | R | X | 🔴 **STRUCTURAL ZERO.** Was `{flags[31:16], tuid[15:0]}` from the ACMP bind context. `0x86C` (window hole) still reads `0xDEADDEAD` |

## 0x870  -  AAF per-stage latency taps  `(roadmap item-11, KL_aaf_latency_taps)`

AAF per-stage latency taps.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x870` | `LTAP_CTRL` | Latency tap control | `0xXXXXXXXX` | [section](#ltap_ctrl-register-offset-0x870-reset--0xxxxxxxxx) |
| `0x874` | `LTAP_Wn` | Latency tap readback | `0xXXXXXXXX` | [section](#ltap_wn-registers-offset-0x874-to-0x8b0-stride-0x4-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary AAF per-stage latency taps (item-11, `KL_aaf_latency_taps`) |
| **Pipeline diagram of where every tap sits:** [`../AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md) (TX CAP→SOF→EOF→MAC_TX, RX MAC_RX→ACCEPT→DEPKT→FABRIC_RENDER, each mapped to its trigger and CSR). Per-sample DDR3 history: [`../LATENCY_HISTORY_RING.md`](../LATENCY_HISTORY_RING.md). |
| Per-stage TX/RX AAF pipeline latency, measured in **axis_clk cycles** (divide by the datapath clock - 50 MHz Arty and shipping AX7101 / 100 MHz AX7101 bring-up - for seconds). Two independent chains each latch a free-running cycle count at the documented pipeline points and expose the inter-stage deltas (last / min / max, saturating 16-bit) plus the gPTP epoch of the measured reference frame: |
| **TX**: `CAP` (fabric/I2S pair in) `->` `PKT_SOF` (packetizer first beat) `->` `PKT_EOF` (packetizer last beat) `->` `MAC_TX` (frame egresses the MAC boundary). Deltas d0 = CAP→SOF, d1 = SOF→EOF, d2 = EOF→MAC. |
| **RX**: `MAC_RX` (frame ingress) `->` `ACCEPT` (AVTP monitor parse-complete / accept pulse) `->` `DEPKT` (payload last beat) `->` `FABRIC_RENDER` (selected payload accepted by the physical render path). Deltas d0 = MAC_RX→ACCEPT, d1 = ACCEPT→DEPKT, d2 = DEPKT→FABRIC_RENDER. |
| **Measurement model.** Each chain follows ONE tagged reference frame at a time: it arms on a stage-0 edge (latching the epoch cycle + gPTP time), takes the next edge at each later stage as that frame's progress, and on the final stage records the deltas + publishes the epoch + increments `samples`. |
| A per-stage timeout (`TIMEOUT_C` ≈ 0.5 ms) aborts and re-arms a stuck token (`timeouts++`), so a dropped frame never wedges the chain. The token is followed by ORDER, not a threaded frame id, so under mixed traffic a shared boundary (`MAC_TX`/`MAC_RX`) may catch a nearer non-AAF edge - min/last/max therefore characterise the latency ENVELOPE rather than one exact frame. |
| The I2S-out playout stage is FIFO-fill dominated (the CDC pair FIFO decouples PDUs from DAC frames) and stays observed via `I2SPB_STAT` fill/converged; a **DDR3 per-sample history ring is the documented follow-up**. |
| Both the `LTAP_CTRL` status word and the 16 RO readback words live at `>= 0x800`, so - exactly like the servo - they need the `rd_in_window` carve-out or they read 0. Per-delta packing: word `2d` = `{max16, last16}`, word `2d+1` = `{16'd0, min16}`. |

### LTAP_CTRL register (offset 0x870) [reset = 0xXXXXXXXX]

Latency tap enable, clear strobe and live status.

RTL name: `A_LTAP_CTRL`.

![LTAP_CTRL bit fields](../../docs/diagrams/regmap/ltap/LTAP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `LTAP_STATUS` | R | X |  |
| 1 | `LTAP_EN` | R/W | 1h | A read returns the OR with LTAP_STATUS. |
| 0 | `LTAP_CLR` | R/W1S | X | A read returns LTAP_STATUS. |

| Note |
|---|
| W: `[1]` enable (measure; reset 1), `[0]` W1S clear all stats. R: `[1]` enable, `[8]` tx_active, `[11:9]` tx stage awaited, `[12]` rx_active, `[15:13]` rx stage awaited. Since 0x000C the chain walk consumes SAME-CYCLE stage pulses as 0-cycle hops (combinational stages -- e.g. the `KL_pcm_route` DEPKT→FABRIC_RENDER pass-through -- no longer strand the token; RX D2 legitimately reads min=0) |

### LTAP_Wn registers (offset 0x874 to 0x8B0, stride 0x4) [reset = 0xXXXXXXXX]

One packed readback word of the AAF latency taps.

RTL name: `A_LTAP_BASE to A_LTAP_END (i_ltap_regs)`.

![LTAP_Wn bit fields](../../docs/diagrams/regmap/ltap/LTAP_Wn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `LTAP_REGS` | R | X |  |

| n | Offset | Name | Producer reset | Description |
|---|---|---|---|---|
| 0 | `0x874` | `LTAP_TX_EPOCH` | `0` | gPTP ns (`ptp_now[31:0]`) latched at the last completed TX frame's CAP stage |
| 1 | `0x878` | `LTAP_TX_INFO` | `0` | `[15:0]` samples (completed TX frames, saturating), `[31:16]` timeouts (aborted tokens) |
| 2 | `0x87C` | `LTAP_TX_D0` | `0` | CAP→SOF: `[15:0]` last, `[31:16]` max (cycles) |
| 3 | `0x880` | `LTAP_TX_D0_MIN` | `0xFFFF` | CAP→SOF: `[15:0]` min (cycles) |
| 4 | `0x884` | `LTAP_TX_D1` | `0` | SOF→EOF: `[15:0]` last, `[31:16]` max |
| 5 | `0x888` | `LTAP_TX_D1_MIN` | `0xFFFF` | SOF→EOF: `[15:0]` min |
| 6 | `0x88C` | `LTAP_TX_D2` | `0` | EOF→MAC_TX: `[15:0]` last, `[31:16]` max |
| 7 | `0x890` | `LTAP_TX_D2_MIN` | `0xFFFF` | EOF→MAC_TX: `[15:0]` min |
| 8 | `0x894` | `LTAP_RX_EPOCH` | `0` | gPTP ns latched at the last completed RX frame's MAC_RX stage |
| 9 | `0x898` | `LTAP_RX_INFO` | `0` | `[15:0]` samples, `[31:16]` timeouts |
| 10 | `0x89C` | `LTAP_RX_D0` | `0` | MAC_RX→ACCEPT: `[15:0]` last, `[31:16]` max |
| 11 | `0x8A0` | `LTAP_RX_D0_MIN` | `0xFFFF` | MAC_RX→ACCEPT: `[15:0]` min |
| 12 | `0x8A4` | `LTAP_RX_D1` | `0` | ACCEPT→DEPKT: `[15:0]` last, `[31:16]` max |
| 13 | `0x8A8` | `LTAP_RX_D1_MIN` | `0xFFFF` | ACCEPT→DEPKT: `[15:0]` min |
| 14 | `0x8AC` | `LTAP_RX_D2` | `0` | DEPKT→FABRIC_RENDER: `[15:0]` last, `[31:16]` max |
| 15 | `0x8B0` | `LTAP_RX_D2_MIN` | `0xFFFF` | DEPKT→FABRIC_RENDER: `[15:0]` min |

## 0x8B4  -  RX stream-parser probe  `(APRB, avtp_stream_parser + milan_datapath)`

The RX stream parser's pre-match view.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x8B4` | `APRB_Wn` | Stream parser probe | `0xXXXXXXXX` | [section](#aprb_wn-registers-offset-0x8b4-to-0x8c4-stride-0x4-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary RX stream-parser probe (the pre-match listener view) |
| **Why this group exists (2026-07-26).** Every other listener-side counter in this design -- `AVTPRX_*`, `PCMRX_*`, the `0x800` window `CNT0..9`, the RX latency taps -- lives **downstream of the stream-table match**. When a bound listener accepts nothing they all read 0 in unison and none of them can say *why*: frames never arrived, or arrived and matched nothing, or matched and were rejected. These five words are the view **upstream** of the match, and they were the missing instrument in the fabric-listener accept blocker ([the troubleshooting guide's blocker section](../limitations/TROUBLESHOOTING.md#section-21-acmp-says-success-the-listener-declares-itself-bound---and-not-one-frame-is-accepted-root-caused-and-fixed-version-0x000f-mechanism-confirmed-on-silicon-2026-07-26)). The counters already existed inside `avtp_stream_parser`; this group is what finally wires them out. |
| The `SID`/`INFO` latch only follows **stream** subtypes (`subtype[7] = 0`: AAF, CRF, CVF, 61883). Control traffic -- ADP/ACMP/AECP/MAAP, which is continuous on a live fabric -- is deliberately excluded so it cannot overwrite the media evidence between two diagnostic reads. All words are live RO (no arm, no snapshot) and free-running from reset; read them twice to get a rate. |
| **Reading the three failure modes** (listener bound, nothing accepted): |

| `PARSED` | `MATCHED` | verdict |
|---|---|---|
| static | static | frames are not reaching the parser at all -- look upstream (MAC, filter, classify), not at the listener |
| climbing | static | the parser sees them and the compare misses -- diff `APRB_SID_*` against the bind record (`0x814`/`0x818`) and check `INFO[23:16]` is non-zero (a table with **no armed entry** matches nothing) |
| climbing | climbing | the match is fine; the loss is downstream -- `AVTPRX_ERR` (format), then depacketizer and fabric render |

### APRB_Wn registers (offset 0x8B4 to 0x8C4, stride 0x4) [reset = 0xXXXXXXXX]

One readback word of the RX stream-parser probe.

RTL name: `A_APRB_BASE to A_APRB_END (i_aprb_regs)`.

![APRB_Wn bit fields](../../docs/diagrams/regmap/aprb/APRB_Wn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `APRB_REGS` | R | X |  |

| n | Offset | Name | Producer reset | Description |
|---|---|---|---|---|
| 0 | `0x8B4` | `APRB_PARSED` | `0` | AVTP frames the RX parser fully parsed (32-bit free-running, all subtypes) |
| 1 | `0x8B8` | `APRB_MATCHED` | `0` | of those, frames whose `stream_id` matched an ARMED stream-table entry |
| 2 | `0x8BC` | `APRB_SID_LO` | `0` | `stream_id[31:0]` **as lifted off the wire** for the last stream-subtype frame |
| 3 | `0x8C0` | `APRB_SID_HI` | `0` | `stream_id[63:32]` of that frame |
| 4 | `0x8C4` | `APRB_INFO` | `0` | `[7:0]` that frame's AVTP subtype, `[8]` it matched, `[15:12]` matched entry index, `[23:16]` stream-table entries currently armed |

## 0x8C8  -  reserved target-media compatibility words

Retired telemetry words that read zero.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x8C8` | `RSVD_GAPn` | Reserved compatibility word | `0x00000000` | [section](#rsvd_gapn-registers-offset-0x8c8-to-0x8d0-stride-0x4-reset--0x00000000) |

| Note |
|---|
| Group summary Reserved target-media compatibility words (structural zero) |
| The former `0x8C8`, `0x8CC`, and `0x8D0` telemetry words are retired. They read structural zero, ignore writes, and cannot be used as liveness evidence. `0x8D4` and `0x8D8` carry the media-boundary slip counters since `0x0058` (next section); `0x8DC` carries `RENDER_STAT` (#443). `0x8E0` and `0x8E4` carry `AAFM_STAT` and `AAFM_RATE` since #629 ([below](#0x8e0-----aaf-clock-meter--629-kl_aaf_clock_meter)); `0x8E8` to `0x8F4` remain unmapped and read zero. Physical-render diagnostics use the retained channel-map readback, Listener/depacketizer counters, I2S status, and pin-level evidence instead. |

### RSVD_GAPn registers (offset 0x8C8 to 0x8D0, stride 0x4) [reset = 0x00000000]

Retired telemetry word; reads zero and ignores writes.

RTL name: `A_RSVD_GAP_BASE to A_RSVD_GAP_END`.

![RSVD_GAPn bit fields](../../docs/diagrams/regmap/gap/RSVD_GAPn.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `RESERVED` | R | 0 | Reserved. |

## 0x8D4  -  media-boundary slip counters  `(SLIP, KL_chan_map_capture)`

Media-boundary slip counters.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x8D4` | `SLIP_LB` | Loopback slip counters | `0xXXXXXXXX` | [section](#slip_lb-register-offset-0x8d4-reset--0xxxxxxxxx) |
| `0x8D8` | `SLIP_TDM` | TDM slip counters | `0xXXXXXXXX` | [section](#slip_tdm-register-offset-0x8d8-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary Media-boundary slip counters (`SLIP_LB` / `SLIP_TDM`, RO live, minor >= `0x0058`) |
| **Why this pair exists (2026-09-10, #390).** Two 48 kHz grids meet at the capture crossbar: the physical front-end grid (fsync, `clk_audio/512`) and the packet grid (`media_tick_p`). `KL_chan_map_capture` counts every slip at each junction - the LOOP bucket's elastic queue (pushed at the upstream talker's rate, popped on the media tick) and the TDM frame bank (a whole frame published at each frame's close on the fsync grid, taken by the talker walk's snapshot in the media tick's cycle) - and until `0x0058` those counts reached only a simulation tap. Since #617 the TDM half keys on exactly those two events, so it counts the talker's own repeated and skipped TDM frames (`tb/verilator/capture_coherence` grades it walk by walk). Before #629 the INTERNAL grids free-ran and slipped one sample every 1.958 s on the shipping divider plan (-10.64 ppm, the free-run rule of that time, slips accepted). Since #629 (D4 = A2-a) the align chain holds the packet grid on fsync at INTERNAL as under a followed CRF or AAF source, and both pairs stop climbing (`tb/verilator/milan_dp` `obj_aclk`, the [RING-INT] / [RING-CRF] phases). Nothing clears them, so a pair that counted before the aligner engaged reads a static NON-ZERO word afterwards, not a zero: the reading table below grades the pair static, never absolute. These two words are that evidence on silicon. |
| **The counting law, and the ceiling.** A loopback pair is *fed* by its first accepted beat and *primed* at its stream's first accepted `tlast`; both stay set until a bind wipe (the stream's bind falling) or reset. From then on the pair counts one dup on **every** media tick that finds its queue empty, whether the upstream talker is slow by 10.64 ppm or has stopped: an upstream pause, a pulled cable or a talker that stops without an unbind counts `LB_PAIRS_C` x 48000 dups per second. The TDM half has the same shape: once the first frame has been seen, every snapshot without a fresh frame close is a dup, so a stopped front-end clock counts 48000 per second. Both halves saturate at `0xFFFF` and nothing but reset clears them; a bind wipe un-primes and un-feeds the pair without touching the count (`tb/verilator/chmap_capture` [SAT] ticks a starved pair to the ceiling and through a wipe). `0xFFFF` therefore means "at least 65535, spent", never a rate. Time to the ceiling: |

| event | `SLIP_LB` dups | `SLIP_TDM` dups |
|---|---|---|
| upstream paused, four fed pairs (the shipping 1x1x8 lane) | 65535 / 192000 per second = 0.34 s | - |
| upstream paused, 32 fed pairs (an 8x8 elaboration with the lane) | 65535 / 1536000 per second = 43 ms | - |
| TDM front-end clock stopped | - | 65535 / 48000 per second = 1.4 s |
| an unaligned packet grid against a disciplined peer (one slip per 1.958 s: INTERNAL before #629) | 8.9 h on four pairs, 1.1 h on 32 | 35.6 h at one dup per slip; sooner when a wider marker dither adds dup/skip pairs |

| Note |
|---|
| Live RO, no arm, no snapshot (the same `>= 0x800` carve-out as `0x8F8`); writes land nowhere. Read twice and difference for a rate while both halves are below the ceiling; a half at `0xFFFF` carries no rate information until reset. |
| **Structural zero, and telling "no lane" from "one grid".** `SLIP_LB` reads `0` on a shape built without the loopback lane (`LOOPBACK_P = 0`: the Arty shapes, and the 8x8 product shape where the lane was refused for area; the loop feed strobe folds to a constant 0 and the ring's counters are pruned with it), and that zero is indistinguishable from a present, healthy ring: the word carries no presence bit. This is the REQ-CSR-05 / methodology R5 tension, decided on #390 as a *documented* structural zero, so establish the lane before reading the word: the build's config sets `cluster_mapping.fabric.loopback_lane` (the builder's `--loopback-lane`, which is what sets `LOOPBACK_P`; without it the AEM model's loopback clusters are model-only), and on a `CHMAP_RDBK_P` build a mapped loopback entry reads `CHMAP_LOOP[17]` fed = 1 (`0x914`, in the 0x900 section) once audio has reached it, in a word that is not `0xDEADDEAD`. That second half is not optional: `0xDEADDEAD` is the house not-a-measurement sentinel this register reads un-armed, timed out or refused (the 0x900 section), its bit `[17]` is 0, and a reader who takes it for an answer reads "no measurement" as "no lane". Both ring legs of `tb/verilator/milan_dp` execute the instruction in that order rather than only stating it: each grades the WHOLE `0x914` word against `0xDEADDEAD`, and `CHMAP_SNAP[1]` valid with it, BEFORE it projects anything, because the projection cannot do it (the poison's `{mask_valid, valid, fed}` is 1, 1, 0, the pruned leg's own answer; the bits that separate it are `[31:28]`, zero on every valid word, which the projection drops). Behind those two grades the capture-side readback answers `{mask_valid, valid, fed}` = 1, 1, 1 on `obj_aclk`, whose lane is built and fed, and 1, 1, 0 on `obj_prune` beside the `SLIP_LB` zero above, so the pair separates a MEASURED absent lane from an UNMEASURED word, and a readback left un-armed fails `obj_prune` instead of passing it. `SLIP_TDM` counts on every shape with a physical capture front end, but only once the first frame has been seen: a front end that never frames (a TDM slave with no codec clock) reads 0 like an aligned one, so a `SLIP_TDM` zero is evidence only beside proof that the front end frames. A frame close and a walk snapshot in the same cycle count nothing: the snapshot takes the frame already pending, if there is one, and the coincident close pends in its place; with none pending the snapshot takes the coincident frame, and the walk reads exactly that frame (its bank loads one cycle late). From the first frame on and below the ceiling, dups minus skips therefore follows snapshots minus closes to within the one pending frame, so the NET count is the slip count: +1 per slow free-running passage across the tick, -1 per fast one. In this section "marker" is the frame close and "tick" the snapshot's cycle. Each half alone counts once per passage while the marker dithers between two adjacent cycles on its way across, which is what `tb/verilator/media_grid_align` [G9] grades (one dup slow, one skip fast, no delivery jitter). A wider dither on the way through, such as the one edge of marker delivery jitter that suite models for the root's capture FIFO, adds balanced dup/skip pairs: both halves climb, and only their difference is the slip. Before #74 item 2 that coincidence dropped the pending marker: a marker dithering across the tick counted about a dozen dups per slip, read a skip-direction slip as dups, and a CRF lock parked with the marker on the tick chattered thousands of dups per 0.2 s. Under a CRF selection the align loop now also clamps the engagement capture that becomes its lock target into [`LOCK_KEEPOFF_CYC_P`, `DIV_C - LOCK_KEEPOFF_CYC_P`] cycles after its tick (`KL_media_grid_align`; the module default keep-off is `DIV_C/128`, 16 cycles at 100 MHz, just under 1/128 sample). The marker then dithers around that target, so its clearance from every tick at lock is the keep-off less the lock's own dither and the delivery jitter: [G7] and [G8], engaged on the tick and just before it with one edge of delivery jitter, grade that clearance at 12 cycles or more and count no dup and no skip over their lock windows, and at the [G7] lock a held frame is exactly one dup and a surplus frame exactly one skip. |
| **The guarded crossing (#617).** `milan_datapath` hands the aligner the same frame close this word counts as its marker, `media_tick_p` one cycle late as its tick - which puts the lock-target split on the walk's crossing, so no engagement is pulled across it - and a keep-off of `MGA_KEEPOFF_CYC_C` = 256 cycles (a quarter sample on a compressed-clock test elaboration). The default 1/128 sample would hold a settled lock off the crossing, but not the loop's acquisition: an unpulled engagement's transient moves the close about 3 cycles per ppm of relative rate (149 at 50 ppm), and a raced one, pulled a keep-off away at 64 ppm, sits 4 cycles per ppm short of its target, a margin of 256 - 4 x the rate. That rate is the TDM frame against the local axis clock, which a +/-50 ppm Milan source does not bound (the local oscillator may run +/-100 ppm off). With the guard no settled lock slips: `tb/verilator/capture_coherence` sees no slip while the lock converges, to +/-100 ppm, and recorded 150,000-column runs see none once it has converged, to +/-150 ppm. What this word counts while an engagement acquires, by relative rate ([the guarded crossing](../design/TIME_SYNC.md#the-guarded-crossing)): |
| below the 64 ppm pull, and above nominal to about 67 ppm, where the pull stops outrunning the rate: only an engagement whose close lands on the crossing itself, one dup and one skip - by column 57 within +/-50 ppm (every sub-cycle phase measured); above nominal by column 8 through 66 ppm, below nominal later as the rate nears the pull (column 181 at 60 ppm, 426 at 63); |
| past it: above nominal an engagement near the crossing is carried across and back while the integrator settles; below nominal there is no sharp limit, and the same pair comes later with the rate (column 1,323 at 66 ppm, 2,918 at 70); on either side one dup and one skip (by column 6,300 at 80 ppm); |
| past the transient limit, about 86 ppm: also an engagement up to 256 cycles off, as its transient crosses and returns (by column 13,100 at 100 ppm). |
| Each counts once and nets zero, and the settled lock then counts nothing. Keyed on the slot-0 strobe, as it was before #617, the keep-off guarded an instant three TDM8 pair periods from the crossing: a lock could sit on the crossing and repeat and skip frames for as long as it held, while this word, keyed on that same slot-0 strobe, read static. Until #617 round 3 the media NCO could also lose two ticks when an aligner trim update landed on its terminal count, which an engagement dwelling on the crossing makes likely; `KL_media_nco`'s monotone terminal compare removed that. |
| **Reading them** (the lane established, a loopback pair fed and mapped, the listener bound, both halves below `0xFFFF`; the rates assume the upstream talker runs at the physical grid's rate, the disciplined peer `obj_aclk` models): |

| `SLIP_LB` | `SLIP_TDM` | verdict |
|---|---|---|
| static | static | one grid: the packet grid follows the selected source and the upstream talker rides the same media clock. Under CRF a static `SLIP_TDM` is a talker that repeats and skips no TDM frame: the aligner holds the frame close 256 cycles off the walk's crossing at every settled lock phase (the guarded crossing above); an engagement's acquisition may add one dup and one skip, once |
| dups climbing 0.51/s per fed pair (about 2/s on the shipping four-pair lane, 16/s on 32 pairs) | dups minus skips climbing 0.51/s (dups alone at 0.51/s while the marker dithers over two adjacent cycles; a wider dither adds skips and as many extra dups) | the packet grid is not aligned to the front end: the -10.64 ppm plan. At INTERNAL this was the rule before #629; since #629 (A2-a) the aligner runs at every source, so on a current image look for a dead TDM feed (the aligner's watchdog disengages it) |
| climbing | static | our own front end is aligned but the upstream talker's clock is not this media clock: look at the peer's clock source |
| `0xFFFF` in either half | any | the half is spent: an upstream pause, cable pull or talker stop-without-unbind (a stopped front-end clock for `SLIP_TDM`) pegged it in under two seconds, and it says nothing about the present rate; a saturated word is not evidence of one grid. Reset to re-arm, then read again; a bind wipe un-primes the pair but does not clear the word |

### SLIP_LB register (offset 0x8D4) [reset = 0xXXXXXXXX]

Loopback-ring duplicate and skip counts.

RTL name: `A_SLIP_LB`.

![SLIP_LB bit fields](../../docs/diagrams/regmap/slip/SLIP_LB.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `SLIP_LB` | R | X |  |

| Note |
|---|
| `[15:0]` loopback-ring dups (a media tick finds a pair's queue empty: the hold repeats the last event), `[31:16]` loopback-ring skips (queue full at a push: the oldest event dropped). The unit is one dup per fed and primed pair per tick, so a lane of `LB_PAIRS_C` pairs counts `LB_PAIRS_C` per slipped beat (4 on the shipping 1x1x8 lane, 32 on an 8x8 elaboration); a lane never fed counts nothing. The #645 settle recentre's own held pops or dropped events count in neither half: it is the declared discontinuity of a source change, a pull-in or a listener bind at INTERNAL ([design](../design/MEDIA_CLOCK_FOLLOWING.md#settle-recentre)), so a word static from it on is the acceptance state |

### SLIP_TDM register (offset 0x8D8) [reset = 0xXXXXXXXX]

TDM-junction duplicate and skip counts.

RTL name: `A_SLIP_TDM`.

![SLIP_TDM bit fields](../../docs/diagrams/regmap/slip/SLIP_TDM.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `SLIP_TDM` | R | X |  |

| Note |
|---|
| `[15:0]` TDM-junction dups (a walk snapshot with no frame closed since the last one: the talker repeats a TDM frame), `[31:16]` TDM-junction skips (a frame close over an unread frame: no talker walk reads it). One event per frame, gated on the first physical frame. The frame close is the strobe of the frame's last pair (`CMAP_TDM_FRAME_PAIRS_C`); before #617 the marker was the slot-0 strobe and the consume the tick |

## 0x8DC  -  render presentation state

Presentation state of the selected listener.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x8DC` | `RENDER_STAT` | Render presentation state | `0xXXXXXXXX` | [section](#render_stat-register-offset-0x8dc-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary `RENDER_STAT`: RO live selected-listener presentation state and the global refused-PDU count; structural zero without the stage. VERSION minor remains `0x0060`; the release step owns the bump |
| Issue #443 claims this previously unmapped debug-group word. Issue #632 re-defines its fields for the presentation stage, `KL_render_queue`, which replaced the #386 setpoint stage. |
| VERSION remains `0x0002_0060` under [the recorded deferral](https://github.com/kebag-logic/milan-fpga/issues/443#issuecomment-5826779078). The release step owns the minor bump. Before that bump, VERSION alone cannot identify this addition. Verify the build's source revision includes #443's register decode, and #632's field meanings. |
| `STRM_SEL[3:0]` selects the listener, with `STRM_SEL[8]=0`. Talker selections and indices outside `N_LISTENERS_P` read zero. `STRM_SEL[9]` does not change this word's selection. The listed reset assumes a present stage and listener 0. That is `STRM_SEL`'s reset selection. Writing this shared selector invalidates the window's ACMP/SRP snapshots. Another task moving it changes which listener this word reports. Diagnostic readers must coordinate access and restore the previous selection. |

| Bits | Width | Source | Meaning | Reset |
|---|---|---|---|---|
| `[7:0]` | 8 | selected `lead_o` byte | Frames queued past the frame every interface has read: the newest frame the stream wrote, less that one; 0 with none queued; saturates at 255 (the queue is 128 frames deep at 48 kHz) | 0 |
| `[8]` | 1 | selected `idle_o` bit | Interface 0's last read of the stream found no sample: before the stream's first presentation time, after it ends, or in a gap; level, no counter | 1 |
| `[9]` | 1 | selected `converged_o` bit | The stream has presented a sample on every read for 100 ms running; level, no counter | 0 |
| `[15:10]` | 6 | constant | Reserved zero | 0 |
| `[31:16]` | 16 | `refused_o` | Global count of PDUs with a refused event, once per PDU: late (an event at or before the frame every interface has read) or too early (an event beyond the queue). Each event is judged on its own frame, so a counted PDU's other events may still be presented; saturates at `0xFFFF`, never wraps | 0 |

| Note |
|---|
| The widths preserve the stage's taps without truncation. The refused count aggregates every listener, including unselected streams. Reset clears it; bind flushes do not. Neither reading nor writing clears it; writes are ignored. All fields are sampled together by the live CSR read. No snapshot arm or cross-clock transfer is involved. |
| **STRUCTURAL ZERO** applies when the stage is absent. Such integrations must tie `i_render_status` to zero. That zero means no source, never a measured healthy stage. The current datapath instantiates the stage unconditionally. Neither parked TDM pins nor disabled I2S imply its absence. Check the elaborated build before interpreting any zero. |
| Refused PDUs and slips do not raise `STREAM_INTERRUPTED`. That is [#443's manager decision](https://github.com/kebag-logic/milan-fpga/issues/443#issuecomment-5789749713), kept by #632. The untimed-PDU and slip counters (`untimed_o`, `slips_o`) remain verification taps. The law, its rules and its counters are the [design's](../design/MEDIA_CLOCK_FOLLOWING.md#the-listener-each-sample-at-its-presentation-time-632). |
| Proof: `make -C tb/verilator/milan_dp aclk` reads the taps. `make -C tb/verilator/milan_dp render-csr-controls` checks absence and mutation. |

### RENDER_STAT register (offset 0x8DC) [reset = 0xXXXXXXXX]

Presentation state of the selected listener.

RTL name: `A_RENDER_STAT`.

![RENDER_STAT bit fields](../../docs/diagrams/regmap/render/RENDER_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `RENDER_STAT` | R | X | Selected listener's presentation state and the global refused-PDU count |

## 0x8E0  -  AAF clock meter  `(#629, KL_aaf_clock_meter)`

AAF media clock meter.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x8E0` | `AAFM_STAT` | AAF clock meter status | `0xXXXXXXXX` | [section](#aafm_stat-register-offset-0x8e0-reset--0xxxxxxxxx) |
| `0x8E4` | `AAFM_RATE` | AAF clock meter rate | `0xXXXXXXXX` | [section](#aafm_rate-register-offset-0x8e4-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary AAF clock meter (`AAFM_STAT` / `AAFM_RATE`, RO live, #629); structural zero on a shape without an AAF clock source. VERSION minor remains `0x0060`; the release step owns the bump |
| Issue #629 claims the first free pair above `RENDER_STAT`. The meter measures the selected AAF Stream Input's media clock. It reads the presentation timestamps, as the [media-clock following design](../design/MEDIA_CLOCK_FOLLOWING.md) states. Its rate is the servo's reference while an AAF source is selected. |
| VERSION remains `0x0002_0060`, as for `0x8DC`. The release step owns the minor bump. Before that bump, VERSION alone cannot identify this addition. Verify the build's source revision includes #629's register decode. |

| Bits | Width | Meaning | Reset |
|---|---|---|---|
| `[0]` | 1 | Locked: 8 clean consumed PDUs; 100 ms without one unlocks | 0 |
| `[1]` | 1 | Rate valid: 2,048 group intervals (4.096 s) since the history last restarted | 0 |
| `[2]` | 1 | Enabled: an AAF clock source is selected | 0 |
| `[3]` | 1 | Reserved zero | 0 |
| `[7:4]` | 4 | The followed AAF listener; zero while no AAF source is selected | 0 |
| `[15:8]` | 8 | Data-caused history restarts: a `tu` edge, a deviation beyond 4,096 ns, a pick spacing outside its bound; wraps | 0 |
| `[31:16]` | 16 | Largest timestamp deviation in a group, ns; saturates at `0xFFFF` | 0 |

| Note |
|---|
| `[15:8]` is the bench's measure of a talker's regularity. Only reset clears it; a source change does not. `[31:16]` clears at every era start: a selection change, a bind edge or the 100 ms timeout. While no AAF source is selected, `[2:0]` and `[31:16]` read zero. |
| `AAFM_RATE` is the talker's media clock against gPTP, as `CRF_RATE` (`0x748`). It is signed ns of error per 512 ms; 1 ppm is 512 units. It updates every 512 ms and holds its last value between updates. It is meaningful only while `AAFM_STAT[1]` reads 1. |
| **STRUCTURAL ZERO** applies when the shape offers no AAF clock source. Then no meter is elaborated and both words read zero. Each word has its own term in the `>= 0x800` read window. Without it the word would read zero on every build, as `0x8F8` once did. |
| Proof: `make -C tb/verilator/aaf_clock_meter` grades the meter and its fields. The root CSR read is graded in `tb/verilator/milan_dp_mclk`. |

### AAFM_STAT register (offset 0x8E0) [reset = 0xXXXXXXXX]

AAF clock meter status and diagnostics.

RTL name: `A_AAFM_STAT`.

![AAFM_STAT bit fields](../../docs/diagrams/regmap/aafm/AAFM_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AAFM_STAT` | R | X | Meter status and diagnostics |

### AAFM_RATE register (offset 0x8E4) [reset = 0xXXXXXXXX]

Signed AAF media rate in CRF_RATE units.

RTL name: `A_AAFM_RATE`.

![AAFM_RATE bit fields](../../docs/diagrams/regmap/aafm/AAFM_RATE.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `AAFM_RATE` | R | X | Signed rate in `CRF_RATE`'s units |

## 0x8F8  -  MMCM-DRP media-clock servo  `(Milan v1.2 7.3.4, KL_mmcm_drp_servo)`

MMCM DRP media-clock servo.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x8F8` | `MCSRV_STAT` | Media-clock servo status | `0xXXXXXXXX` | [section](#mcsrv_stat-register-offset-0x8f8-reset--0xxxxxxxxx) |
| `0x8FC` | `MCSRV_CTRL` | Media-clock servo control | `0x00000000` | [section](#mcsrv_ctrl-register-offset-0x8fc-reset--0x00000000) |

| Note |
|---|
| Group summary MMCM-DRP media-clock servo (Milan v1.2 7.3.4) |
| 🟢 **THE SERVO ENGAGES ON THE LIVE SELECTION SINCE #74.** It engages when the stored CLOCK_DOMAIN `clock_source_index` selects the CRF descriptor or, since #629, one AAF Stream Input's INPUT_STREAM descriptor: the processor stores AECP `SET_CLOCK_SOURCE`, `KL_pp_shadow.sv` exports it, and `milan_datapath`'s `media_clk_resolve` decodes the live index through the shape's generated clock-source tables. Its reference is `KL_crf_rx` under CRF and the AAF clock meter (`0x8E0`) under an AAF source. With INTERNAL selected - the power-on state - `0x8F8` reads IDLE with trim 0, honestly. The servo's command slice `[31:16]` is the MMCM's ALONE: the packet-grid NCO no longer mirrors it. The packet grid follows the PHYSICAL fsync grid through `KL_media_grid_align` (one reference chain, each link separately falsifiable - [media boundary](../design/TIME_SYNC.md#media-boundary), measured in the [historical Section 3.5.1](../history/v1/design/TIME_SYNC.md#351-the-grid-phase-contract--clk_tdm_i-clk_audio_i-media_tick_p-74)), which is what actually removes the -10.64 ppm divider drift a mirrored command could never close. Since #632 the servo also holds the domain's media event on a followed CRF stream's timing points: a type-2 phase term in its integrator, slew-limited to 0.5 ppm. `[9]` reads the phase settled; the phase word itself reaches no CSR ([phase alignment](../design/MEDIA_CLOCK_FOLLOWING.md#phase-alignment)). An IDLE reading still has two possible causes - the servo pruned at elaboration (`MCSERVO_P = 0`), or built with INTERNAL selected. Only the build plan distinguishes the first. |
| The CRF clock-recovery ACTUATOR (status word + control knobs; loop semantics in the [media boundary](../design/TIME_SYNC.md#media-boundary), internals in the [historical Section 3.4](../history/v1/design/TIME_SYNC.md#34-the-mmcm-drp-servo--kl_mmcm_drp_servo-mcsrv-0x8f80x8fc)). Parked at the map TAIL (after the 0x800-0x85C window) on purpose: parallel feature lanes are extending the 0x700 group, so a tail slot cannot collide on merge; `0x8FC` next to it holds the servo control knobs. |

### MCSRV_STAT register (offset 0x8F8) [reset = 0xXXXXXXXX]

MMCM DRP servo state, trim and flags.

RTL name: `A_MCSRV_STAT`.

![MCSRV_STAT bit fields](../../docs/diagrams/regmap/mcsrv/MCSRV_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `MCSRV_STAT` | R | X |  |

| Note |
|---|
| `[2:0]` state (0 IDLE, 1 VERIFY, 2 REPAIR, 3 ACQUIRE, 4 LOCKED, 5 HOLDOVER, 6 FAULT), `[3]` DRP config verified, `[4]` DRP config mismatch (read-verify failed; repaired only when `MCSRV_CTRL[1]` is set), `[5]` MMCM LOCKED (synced), `[6]` fine-PS actuator busy, `[7]` PSDONE-watchdog fault (sticky), `[8]` DRP relock-timeout fault, `[9]` phase settled (#632): under a followed CRF stream the servo's phase term is engaged, and the window phase and every sample of the window (each timing point against the domain media event, folded) have sat inside +/-5 % of a sample period (IEEE 1722-2016 10.8) for four full windows running; 0 at INTERNAL, under an AAF source, from any hold of the phase term until four clean full windows, and while re-acquiring ([phase alignment](../design/MEDIA_CLOCK_FOLLOWING.md#phase-alignment)), `[15:10]` discarded rate windows, saturating at 63: a window whose error exceeds 1024 ppm, one a PHC step landed in (#539), or one overlapping the policy-slew level (#545; cleared in IDLE). Slew overlap counts once at the boundary, including the partial tail; a coincident step counts that same window once, `[31:16]` **signed** applied frequency trim in 1/16 ppm units (e.g. `+0x06E9` = +110.6 ppm). The servo engages only when the stored `clock_source` selects this shape's CRF descriptor or an AAF INPUT_STREAM descriptor (the generated `AEM_CLKSRC_KIND_C` table); a change between two followed sources passes HOLDOVER into ACQUIRE with the trim kept; at INTERNAL this word reads state IDLE with trim 0 and the servo generates **zero** DRP/PS activity |

### MCSRV_CTRL register (offset 0x8FC) [reset = 0x00000000]

Servo direction knob and repair enable.

RTL name: `A_MCSRV_CTRL`.

![MCSRV_CTRL bit fields](../../docs/diagrams/regmap/mcsrv/MCSRV_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 1 | `MCSRV_AUTO_REPAIR` | R/W | 0 |  |
| 0 | `MCSRV_PS_INVERT` | R/W | 0 |  |

| Note |
|---|
| `[0]` ps_invert: flips the servo fine-PS direction mapping (bench sign knob - 2026-07-23 mf51 silicon stepped opposite the UG472 reading and rails went 25x worse under the servo; settle the polarity on silicon via this bit, then bake the winner as the RTL default); `[1]` auto_repair: 1 = allow the DRP divider repair path (a `[4]` mismatch triggers the full reset-sequenced read-modify-write reprogram), default 0 = verify-only (bench-gated). NOTE both 0x8F8/0x8FC needed the rd_in_window >=0x800 carve-out - 0x8F8 read 0 on every build before 2026-07-23 |

## 0x900  -  channel-map fabric  `([Section 6 of docs/CHANNEL_MAP_64.md](../CHANNEL_MAP_64.md#6-csr-window-0x900-0x97f-debug-and-override), KL_chan_map_render / KL_chan_map_capture)`

Channel-map debug write port and map RAM readback.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x900` | `CHMAP_CTRL` | Channel map control | `0x00000000` | [section](#chmap_ctrl-register-offset-0x900-reset--0x00000000) |
| `0x904` | `CHMAP_SEL` | Channel map select | `0x00000000` | [section](#chmap_sel-register-offset-0x904-reset--0x00000000) |
| `0x908` | `CHMAP_WORD` | Channel map word | `0x00000000` | [section](#chmap_word-register-offset-0x908-reset--0x00000000) |
| `0x90C` | `CHMAP_STAT` | Channel map status | `0x00000000` | [section](#chmap_stat-register-offset-0x90c-reset--0x00000000) |
| `0x910` | `CHMAP_SNAP` | Channel map snapshot | `0xC5000300` | [section](#chmap_snap-register-offset-0x910-reset--0xc5000300) |
| `0x914` | `CHMAP_LOOP` | Channel map readback | `0xXXXXXXXX` | [section](#chmap_loop-register-offset-0x914-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary Channel-map fabric debug window (chmap64) -- write port + bypass arm, and the `0x910`/`0x914` **map-RAM readback** |
| Diagnostic write port + bypass arm for the 64x64 render/capture map stores. Same dedicated-arm carve-out as MCSRV (NOT in `is_plain_rw` - a 0x900 shadow write would alias word 0x100 - plus its own `rd_in_window` 0x900-0x93F term, or every read here would be the 0x8F8 dead-read trap). |
| `CHMAP_CTRL[0]` = 0 (reset) selects the fixed capture/render paths. Setting it to 1 selects the programmable crossbars and moves the DAC's pace onto the 48 kHz media grid. **This window is the direct diagnostic programmer of the map stores.** The processor serves `GET_AUDIO_MAP` from the same stores, and successful `ADD_AUDIO_MAPPINGS` or `REMOVE_AUDIO_MAPPINGS` transactions update the live map after whole-command validation. The transaction excludes CSR writes until commit or abort, so the validation baseline cannot change underneath it. The CSR writer is also refused whenever `LOCK_ENTITY` is held. This protects both map stores and the authoritative protocol ownership state from non-ATDECC edits. |
| On a shape with dynamic maps, each dynamic direction's store and crossbar hold the #658 power-on map from boot: stream channel c on the port's cluster c. The parent's boot writer fills the crossbars from reset until one sweep after the restore's terminal (`PP_STAT` done or CLOSED). After a COMPLETE terminal the parent's map restore (#637) then puts back the saved lists, and holds the maps until it ends. The CSR writer is refused for that long, as it is during a transaction. `CHMAP_STAT` cannot see either refusal: it counts such a write in `[15:0]` as a commit. |

| Offset | Name | Acc | Reset | Description |
|---|---|---|---|---|
| `0x918`-`0x91C` | - | - | `0` | reserved to this feature (read 0, never shadow-aliased). **`0x920`-`0x93C` are the protocol-processor window**, see the next section |

### `0x904` - the render side writes by CLUSTER key and reads by PHYSICAL key

| Note |
|---|
| This asymmetry is a property of the existing register map, made visible for the first time by the AX7101 1x1 TDM8 shape (#447). The `0x908` WRITE arm treats `CHMAP_SEL[5:0]` as a GLOBAL CLUSTER key and projects it through the generated `ADP_DMAP_IN_RPHYS_C` table before it reaches the crossbar. The `0x910`/`0x914` READBACK treats the same field as a PHYSICAL render key with no projection at all, which is what keeps the readback a raw RAM dump: the two crossbar keys no cluster reaches stay dumpable. On every shape shipped so far the two coincided; on this shape they differ by the TDM lane base, so a write to cluster key 4 lands at physical key 6 and must be read back at physical key 6. |
| Two behaviours that follow, and are preserved rather than changed: |
| A write whose cluster key has NO valid projection is SUPPRESSED at the crossbar write gate: no render RAM word changes. That is a CSR behaviour and is not an AECP status. |
| The same write still MIRRORS into the AECP protocol store whenever the key is in range, the entity is unlocked and no conflicting map transaction is active, exactly as it did before. The suppression gates the crossbar write, not the store, so `GET_AUDIO_MAP` continues to report an in-range CSR write. |
| Those are THREE key classes, not two, and each answers the two observations - the render RAM and the protocol store - differently: |

| Cluster key | Render RAM | AECP protocol store |
|---|---|---|
| in range, PROJECTED | written at the projected physical key | mirrored |
| in range, NONPHYSICAL (a declared cluster whose `ADP_DMAP_IN_RPHYS_C` entry is invalid) | UNCHANGED | mirrored, and listed by `GET_AUDIO_MAP` for the port that owns the cluster |
| OUT OF RANGE (past the model's declared cluster keys) | UNCHANGED | not written; nothing appears in any port's page |

| Note |
|---|
| The middle row is the one that needs a shape to exist at all: every cluster the shipping AX7101 TDM8 image declares is projected, so its unprojected key is one PAST the declared block, which is the third row and a different defect class. The multi-stream verification shape described in [the channel map](../CHANNEL_MAP_64.md) supplies a genuinely nonphysical in-range key, and all three rows are graded there on both observations. |

### `0x910`/`0x914` - reading the map RAM, and why the un-armed state is not zero

| Note |
|---|
| `CHMAP_WORD` `0x908` has never been able to answer "what does the map RAM hold?". Its readback is `milan_csr`'s **own shadow** of the last word software wrote, and until `VERSION` `0x0017` both RAM read ports were tied off in `milan_datapath` (`map_rd_en_i = 1'b0`, `map_rd_data_o ()`), so there was no path to the truth at all. Two consequences, both measured rather than theoretical: the AEM audio-map projector can rewrite the render map underneath software without `0x908` moving, and a **capture slot that is mapped but has never been fed emits `24'd0` -- bit-identical to a slot that is working and quiet**. On a board that routes no audio pins that ambiguity is the whole diagnosis, and the fallback ("frames are counting but the payload is all zeros") cannot separate the two either. |
| `CHMAP_LOOP[18]` `LOOP_SUSPECT` is the separation: `mapped = 1, fed = 0` is a slot the map advertises that no audio has ever reached. |
| **Sequence** (the `0x800` window's discipline, deliberately): |

```text
1. write CHMAP_SEL  0x904 = {side[8], index[5:0]}
2. write CHMAP_SNAP 0x910 = 1                     # arm
3. poll  CHMAP_SNAP 0x910 until [0] busy == 0     # bounded: <= 16 clocks
4. read  CHMAP_LOOP 0x914
```

| Note |
|---|
| **ARMING, AND THE TRAP THIS REGISTER REFUSES TO REPEAT.** The `0x800` window's data words read **`0`** until their `SNAP` is armed, which is indistinguishable from a dead block -- a real trap that has cost time on this bench. `CHMAP_LOOP` cannot do that, because `0` is a *legal* map entry (`EN = 0`). So: |
| **un-armed, timed out, or refused → `CHMAP_LOOP` reads `0xDEADDEAD`**, the house not-a-measurement sentinel (same rule as the `0x800` window's not-backed `CNT` words). It is never `0`. |
| every word that *is* a measurement carries `[26]` `VALID = 1`, so even a genuinely-empty map entry at index 0 reads `0x0400_0000`, not `0`. |
| `[27]` `MASK_VALID` says whether `[18:16]` are a measurement. Only the **capture** RAM's readback carries `{loop_fed, loop_mapped}`; on the render side those three bits are structurally 0 and must not be read as "unmapped, never fed" (that entry's own `EN` bit is raw `[7]`). Same rule as `STATS_CAP` `0x204` -- a capability bit is what separates a silent lane from a measured zero. |
| `CHMAP_SNAP[31:24]` is a **constant `0xC5`**. `0x910` used to be in the reserved-reads-0 range, so `CHMAP_SNAP == 0` is an unambiguous "this gateware predates the register" probe (the `0xA5C35A3C` pattern at `0x7A0`, same idea). `0x918` and up still read 0. |
| **Declared vs. wired.** `CHMAP_SNAP[9:8]` publishes the `CHMAP_RDBK_P` elaboration parameter, whose default is **0 = no readback port in this build** -- the honest default, and the state `milan_datapath` actually shipped in. An arm against a side whose bit is clear is **refused** (`[3]` unsup) and no request reaches the fabric. That is a declaration, so a watchdog holds it to the wire: a side that is declared present and does not answer within 15 clocks sets `[2]` timeout and leaves `CHMAP_LOOP` poisoned, rather than latching whatever the bus happened to hold. |
| **No standard is cited here on purpose.** IEEE 1722.1 and Milan v1.2 say nothing about a vendor debug register. The standard view is `GET_AUDIO_MAP` over AECP, which the current integration serves from the live map stores. This register exposes one raw RAM word and its fabric-specific capability flags. |
| **Hardware acceptance (desk-verified only; no bitstream built for this):** |
| Read `CHMAP_SNAP` at offset `0x910`; expect the `0xC5` tag. |
| Confirm capability bits `[9:8]` match the generated shape. |
| For capture indices 0 through 31, write `{side=1,index}` to `CHMAP_SEL` (`0x904`), write one to `CHMAP_SNAP` to arm, poll until busy clears, and read `CHMAP_LOOP` (`0x914`). Perform the sequence through the bare-metal diagnostic transport or a JTAG AXI master and retain the raw transcript. |
| Read each `CHMAP_LOOP`: `0xDEADDEAD` means no measurement (check `CHMAP_SNAP[3:2]` for refused vs. silent); bit `[18]` set means **that slot is in the map and nothing has ever fed it**, which on a talker that is streaming is the mis-wired-loopback signature and is why its AAF payload is all zeros. Expect bit `[18]` clear on every enabled slot of a healthy 8x8 talker. |

### CHMAP_CTRL register (offset 0x900) [reset = 0x00000000]

Arms the channel-map debug write window.

RTL name: `A_CHMAP_CTRL`.

![CHMAP_CTRL bit fields](../../docs/diagrams/regmap/chmap/CHMAP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:1 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 0 | `CHMAP_ENABLE` | R/W | 0 | map arm. While 0 the default capture/render paths drive bit-identically; set 1 to select the CSR-programmed crossbars. It also gates the `CHMAP_WORD` write window (refusals counted in `CHMAP_STAT[23:16]`) |

### CHMAP_SEL register (offset 0x904) [reset = 0x00000000]

Map side and entry index for writes and readback.

RTL name: `A_CHMAP_SEL`.

![CHMAP_SEL bit fields](../../docs/diagrams/regmap/chmap/CHMAP_SEL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:9 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 8 | `CHMAP_WR_SIDE` | R/W | 0 | side (0 = RMAP/render phys channel 0..9, 1 = CMAP/capture **stream-channel key** `port*8 + sc`, 0..`2*N_SLOTS_P-1` -- per-channel since 0x0027). Selects the target of the next `CHMAP_WORD` write |
| 7:6 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 5:0 | `CHMAP_WR_ADDR` | R/W | 0 | map entry index |

### CHMAP_WORD register (offset 0x908) [reset = 0x00000000]

Map word committed through the shared write port.

RTL name: `A_CHMAP_WORD`.

![CHMAP_WORD bit fields](../../docs/diagrams/regmap/chmap/CHMAP_WORD.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `RESERVED` | R | 0 | Reserved. A write takes effect only when `chmap_ctrl[0] && !i_aecp_locked`. |
| 15:0 | `CHMAP_WR_DATA` | R/W | 0 | A write takes effect only when `chmap_ctrl[0] && !i_aecp_locked`. |

| Note |
|---|
| `[15:0]` the Section 5 map word `{EN[15], SRC[14:12], rsvd[11:9], HALF[8], IDX_HI[7:4], IDX_LO[3:0]}`. Write commits through the shared map write port when `CHMAP_CTRL[0]` = 1 and `LOCK_ENTITY` is not held; otherwise it is refused. Readback is the last committed word. **Render side (RMAP)**: `SRC[12]` is 0 for an AAF Listener channel and 1 for reserved zero; `IDX[5:0]` is `{stream[2:0], channel[2:0]}` and `[8]` is unused. **Capture side (CMAP)**: composes the addressed channel's 13-bit entry `{EN, HALF, SRC[2:0], IDX_HI, IDX_LO}`; source 3 and 6..7 resolve to zero, and `HALF` selects the source pair's L or R sample |

### CHMAP_STAT register (offset 0x90C) [reset = 0x00000000]

Committed and refused map-word writes.

RTL name: `A_CHMAP_STAT`.

![CHMAP_STAT bit fields](../../docs/diagrams/regmap/chmap/CHMAP_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:24 | `RESERVED` | R | 0 | Reserved. |
| 23:16 | `CHMAP_REFUSED` | R | 0 | CSR writes refused while disarmed or entity-locked (saturates) |
| 15:0 | `CHMAP_COMMITS` | R | 0 | map commits (currently CSR only, wraps) |

### CHMAP_SNAP register (offset 0x910) [reset = 0xC5000300]

Arms a map RAM readback and reports its status.

RTL name: `A_CHMAP_SNAP`.

![CHMAP_SNAP bit fields](../../docs/diagrams/regmap/chmap/CHMAP_SNAP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:24 | `CHMAP_SNAP_TAG` | R | C5h |  |
| 23 | `RESERVED` | R | 0 | Reserved. |
| 22 | `CMRD_SIDE` | R | 0 |  |
| 21:16 | `CMRD_ADDR` | R | 0 |  |
| 15:10 | `RESERVED` | R | 0 | Reserved. |
| 9:8 | `CHMAP_RDBK` | R | 3h |  |
| 7:5 | `RESERVED` | R | 0 | Reserved. |
| 4 | `CMRD_ARMED` | R | 0 |  |
| 3 | `CMRD_UNSUP` | R | 0 |  |
| 2 | `CMRD_TO` | R | 0 |  |
| 1 | `CMRD_VALID` | R | 0 |  |
| 0 | `CMRD_BUSY` | R/W1S | 0 |  |

| Note |
|---|
| **W** `[0]` arm a readback of the entry named by `CHMAP_SEL` (ignored while busy). **R** `[0]` busy, `[1]` valid -- the LAST snapshot carries fabric data, `[2]` timeout -- the LAST snapshot ended without the fabric answering, `[3]` unsupported -- the LAST arm was refused because this side has no readback port in this build, `[4]` armed -- a snapshot has been armed since reset, `[9:8]` capability (`[8]` render port wired, `[9]` capture port wired **and** carrying the `{loop_fed, loop_mapped}` mask), `[22:16]` `{side, index}` latched at the last arm, `[31:24]` **constant `0xC5`** |

### CHMAP_LOOP register (offset 0x914) [reset = 0xXXXXXXXX]

The map word the RAM holds, or 0xDEADDEAD.

RTL name: `A_CHMAP_LOOP`.

![CHMAP_LOOP bit fields](../../docs/diagrams/regmap/chmap/CHMAP_LOOP.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `CHMAP_LOOP_RD` | R | X |  |

| Note |
|---|
| The map word **the RAM actually holds**. `[15:0]` raw fabric readback word -- capture side `{1'b0, loop_fed[14], loop_mapped[13], entry[12:0]}` where the entry is the per-channel word `{en[12], half[11], src[10:8], idxh[7:4], idx[3:0]}` (one entry per stream channel since 0x0027). NOTE the two formats: the `CHMAP_WORD` you WRITE is `{EN[15], SRC[14:12], rsvd, HALF[8], IDXH, IDXL}`; the ENTRY you read BACK here re-packs those fields -- e.g. word `0xB000` reads back as entry `0x1300`, and mistaking the packing for corruption cost a bench session. `loop_fed`/`loop_mapped`/`LOOP_SUSPECT` grade the LOOP source only, never general slot health, render side `{8'd0, entry[7:0]}`; `[16]` mapped, `[17]` fed, `[18]` **`LOOP_SUSPECT` = mapped & ~fed** (extracted from the raw word's canonical flag bits, stable here whatever the raw layout), `[19]` side, `[25:20]` index, `[26]` **VALID** (this word is a measurement), `[27]` **MASK_VALID** (`[18:16]` are a measurement -- capture side only). **`0xDEADDEAD` = there is no measurement behind this word** |

## 0x920  -  protocol-processor control plane  `(KL_pp_shadow, VERSION major 2)`

Protocol-processor control plane and the saved-state window.

| Offset | Acronym | Register name | Reset | Section |
|---|---|---|---|---|
| `0x920` | `PP_CTRL` | Processor control | `0x00000000` | [section](#pp_ctrl-register-offset-0x920-reset--0x00000000) |
| `0x924` | `PP_STAT` | Processor status | `0x5BXXXXXX` | [section](#pp_stat-register-offset-0x924-reset--0x5bxxxxxx) |
| `0x928` | `PP_SPADDR` | Processor side-port address | `0x00000000` | [section](#pp_spaddr-register-offset-0x928-reset--0x00000000) |
| `0x92C` | `PP_SPDATA` | Processor side-port data | `0x00000000` | [section](#pp_spdata-register-offset-0x92c-reset--0x00000000) |
| `0x930` | `PP_DIAG` | Processor frame diagnostics | `0xXXXXXXXX` | [section](#pp_diag-register-offset-0x930-reset--0xxxxxxxxx) |
| `0x934` | `PP_NVM_SEL` | Saved-state window select | `0x00000000` | [section](#pp_nvm_sel-register-offset-0x934-reset--0x00000000) |
| `0x938` | `PP_NVM_DATA` | Saved-state window data | `0xXXXXXXXX` | [section](#pp_nvm_data-register-offset-0x938-reset--0xxxxxxxxx) |
| `0x93C` | `PP_NVM_STAT` | Saved-state status and strobes | `0xXXXXXXXX` | [section](#pp_nvm_stat-register-offset-0x93c-reset--0xxxxxxxxx) |

| Note |
|---|
| Group summary **Protocol-processor control plane** (`PP_CTRL`/`STAT`/`SPADDR`/`SPDATA`/`DIAG`) -- always decoded at VERSION major 2 |
| **The control plane's own window, and at VERSION major 2 it is always present.** It used to sit behind `milan_csr`'s `PP_PLANE_P` elaboration parameter, with the whole group folded away -- registers inside a generate, read term a constant 0 -- on a build without the shadow plane. **That parameter is gone.** The processor is not an option, it *is* the control plane, so there is no plane-absent arm to fold and the window is unconditionally decoded on every build. |
| `PP_STAT[31:24]` still carries the constant presence tag `0x5B`, and it is still **the register software must read first**: a read of `0` at `0x924` means the gateware predates this group entirely, and can never be confused with "the plane is present and idle". Same rule as `STATS_CAP` `0x204`. |
| **The entity enable is two bits, ORed.** `PP_CTRL[0]` is this plane's own enable; `ADP_CTRL[0]` at `0x600` is the historic one that every board script and bring-up recipe in this repository writes. **Either one enables the entity.** Demanding both would strand every existing script; honouring only the new bit would silently ignore the old one. There is exactly one control plane now, so there is exactly one thing for either bit to start. |
| **THE RESTORE VERDICT IS FOUR BITS, AND UNTIL `0x0045` IT WAS A LIE.** `restore_done` means the boot walk reached its end. It does *not* mean state came back. Every per-record arm of the processor's restore, including the one that fires when a region is blank or unframed, ends the walk with `restore_done` set and `restore_fail` clear, so a device with **no non-volatile media at all** published the identical status word to one that had genuinely restored every sink: `0x5B00_0004`. A Milan 5.3.8.2 / 5.3.8.3 checklist reading that register passed on a restore that never happened, and the failure surfaced only on a bench that cycled the power. Read the four bits together: |

| `nvm_backed` `[6]` | `nvm_blank` `[7]` | `restore_fail` `[3]` | Meaning |
|---|---|---|---|
| `1` | `0` | `0` | **A restore genuinely completed**: the writer is live and the walk read records out of a validated image |
| `1` | `1` | `0` | **Blank media behind a validated image**: the store is real but held nothing this walk could use. Not a failure: Milan permits an entity that has never been bound |
| `0`/`1` | `0`/`1` | `1` | **Torn read-back, or a BLIND walk**: the walk aborted and the whole image was discarded, or at some cycle of the walk no validated image stood behind the device face, so what it read was the blank answer. The blind verdict is latched per walk in `KL_pp_shadow.sv`: validating the image after the walk does not restore anything, so it cannot clear it |
| `0` | `1` | `1` | **No writer has answered and the walk ran blind**: what a build whose firmware has not configured the backing store reports, `0x5B00_008C` |

| Note |
|---|
| `restore_fail` is deliberately raised in the last two rows rather than a new code being invented for it: `fail` is the bit every reader of this register already treats as not-successful, so software that predates `[6]` and `[7]` still grades an unbacked build correctly. `nvm_backed` is **fabric evidence, never a knob**: `KL_nvm_backend` raises it when the firmware answers and drops it when a deadline lapses or a failure is reported, and no CSR write can set it, which is the property that made it a localparam beside the old blank-flash responder and survives it being live. The backend behind the face is `hdl/milan/KL_nvm_backend.sv` and its control face is `0x934`-`0x93C` below. The bare-metal firmware is the writer ([firmware page](../integration/BAREMETAL_FIRMWARE.md#saved-state-the-flash-writer)): at boot it validates the two journal slots, stages the accepted container or an all-erased one in the reserved window, configures and validates the image through this face and then starts the walk, so a blank board reads the second row above rather than the last one; a build whose firmware predates the writer still reads `0x5B00_008C`. |
| **Since processor pin `d352bbaa` the restore is two walks, and it can end CLOSED.** The binding walk is followed by the D3 walk, which restores the scalar records (configuration, sampling rates, clock sources, both stream formats, presentation offsets) after proving the AEM image they are judged against ([D3 page](../design/SAVED_STATE_MATERIALIZATION.md) sections 5.2, 6.2 and 8.7). The bits above now combine both walks: `restore_done` `[2]` is both walks at COMPLETE or DEFAULTS, `restore_fail` `[3]` is either walk failing (or the blind latch above), and `nvm_blank` `[7]` is a restore that neither walk failed and in which neither validated a record, so a device error that loses the one saved record never reads blank; only a BLIND walk still reads blank beside fail. The D3 walk's third terminal is **CLOSED** `[16]`: the image could not be proven, or a pass-1 roll-back could not prove it again. It is fail and never done, and AECP stays held and ADP stays dark until reset. `[17]` says a pass-1 abort rolled the stores back to DEFAULTS, and `[20:18]` and `[22:21]` carry the D3 walk's and the binding walk's first abort causes. |
| **Since #637 the parent's map restore follows the D3 walk**, and these bits cover it too ([D3 page](../design/SAVED_STATE_MATERIALIZATION.md) sections 5.2 and 18.4). It restores the channel-map records `0x60`/`0x70` after a COMPLETE terminal, in one read pass, while the map faces and the entity enable wait. `restore_busy` `[1]` stays up until it ends and `restore_done` `[2]` rises only then. `restore_fail` `[3]` also reads 1 when it rolled every map back to its reset set. It adds no cause of its own: `[20:18]` reads `0`, since it runs only after a D3 walk that ended with none, and `[22:21]` keeps the binding walk's. `nvm_blank` `[7]` also needs it to have read no framed, crc-clean map record. So saved maps lost to a device error read fail, and restored maps never read blank. AECP is held from reset until the D3 terminal; while it is held one AECP command waits in the ingress and every further one is dropped and counted in side-port snapshot word 37 (host word `0x20025`, `[15:0]`), so ACMP, ADP and MAAP keep their slots. The AEM image must be loaded and CRC-checked before `PP_CTRL[1]`, or the walk cannot prove it and ends CLOSED. `PP_CTRL[0]` and `ADP_CTRL[0]` REQUEST the entity enable; ADP advertises only from `restore_done`. VERSION minor remains `0x0060`; the release step owns the bump. |
| **The side port is POSTED, and one access is outstanding at a time.** The processor's side port is a fabric walk behind a request/ack, and an AXI read must never wait on it -- the bus would stall for as long as the processor takes to answer. So: write `PP_SPADDR` to arm a read, poll `PP_STAT[0]` (`sp_busy`), then read `PP_SPDATA`. A write to `PP_SPDATA` posts a side-port **write** to the address already in `PP_SPADDR`. A request offered while busy is **refused, not queued**, so software can never read one address's answer believing it asked for another. |
| **Why an RX drop counter exists here at all.** `protocol_processor_top` eats a 1 byte/clk stream, which at 100 MHz is 100 MB/s against gigabit's 125 MB/s: a byte serialiser fed from the raw tap cannot keep up with line rate, and would corrupt frames by lagging rather than by dropping them. So the tap classifies first -- EtherType `0x22F0` on any destination address, plus the two MRP pairs (`01:80:C2:00:00:0E` + `0x22EA` MSRP, `01:80:C2:00:00:21` + `0x88F5` MVRP) -- and only control frames enter the frame FIFO ahead of the serialiser. Control traffic is orders of magnitude below the serialiser's rate, so `[15:8]` should be flat; a moving drop count is a real signal, not background. |
| **When this window says the entity model is broken, it cannot say why.** The descriptor-store and response-buffer faults reached through the side-port snapshot (`img_valid = 0`, fault 8 `FAULT_TIMEOUT`, fault 1 `FAULT_WTMO`) are the processor's view of *its* two main-memory bridges, and the processor cannot see the bus those bridges ride: a bridge that never issued a read and a bridge whose read was never answered produce the identical fault here. That distinction cost a board week in August 2026. It is now one read away, in the LiteX CSR space rather than this window because both bridges are SoC-side masters (`milan_soc.py`) with no port into `milan_csr` -- see [Protocol-processor memory bridges](#protocol-processor-memory-bridges-litex-csr-bank-0xf000f800) at the end of this page. |

### PP_CTRL register (offset 0x920) [reset = 0x00000000]

Entity enable and the restore-walk start.

RTL name: `A_PP_CTRL`.

![PP_CTRL bit fields](../../docs/diagrams/regmap/pp/PP_CTRL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:2 | `RESERVED` | R/W | 0 | Reserved; stored and read back, drives nothing. |
| 1 | `PP_RESTORE_GO` | R/W | 0 | `restore_go`: start the NVM boot-restore walk against the saved-state backing store (`KL_nvm_backend` behind the processor's NVM device face, [design page](../design/SAVED_STATE_FASTCONNECT.md) sections 4, 8 and 9). Until firmware has configured AND validated a record image through `PP_NVM_SEL`/`PP_NVM_DATA` the face answers blank flash (reads `0xFF`, writes accepted and discarded, erase completes), so the walk completes with **zero records** and `restore_fail` set. **Validate the image first, then set this bit**: the verdict is latched per walk, and validating afterwards restores nothing. **Set it on every boot** (processor pin `a8f8ce81`, its issue 92): the processor holds its ACMP listener from reset until the walk ends, so a boot that never sets it never answers an ACMP listener command. Since processor pin `d352bbaa` it also holds AECP until the D3 walk's terminal, and that walk proves the AEM image first: **load and CRC-check the AEM image before this bit**, or the restore ends CLOSED (`PP_STAT[16]`) and AECP stays held until reset. Every restore wait is bounded by `NVM_RS_TMO_CYC_P` (20 ms) and the whole restore by `NVM_RS_AGG_CYC_P` (1,000 ms from this bit), both derived from the clock, so a device face that never answers ends the walks with `restore_fail` set; wait for `restore_done` OR `PP_STAT[16]`, since CLOSED never raises done |
| 0 | `PP_ENABLE` | R/W | 0 | **entity enable**, ORed with `ADP_CTRL[0]` (`0x600`); either bit starts the plane. |

### PP_STAT register (offset 0x924) [reset = 0x5BXXXXXX]

Presence tag, saved-state verdict and side-port status.

RTL name: `A_PP_STAT`.

![PP_STAT bit fields](../../docs/diagrams/regmap/pp/PP_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:24 | `PP_PRESENT_TAG` | R | 5Bh |  |
| 23 | `RESERVED` | R | 0 | Reserved. |
| 22:21 | `PP_RESTORE_CAUSE` | R | X |  |
| 20:18 | `PP_RS_CAUSE` | R | X |  |
| 17 | `PP_RESTORE_RB` | R | X |  |
| 16 | `PP_RESTORE_CLOSED` | R | X |  |
| 15:12 | `PP_NVM_VERDICT` | R | X |  |
| 11 | `PP_NVM_PEND` | R | X |  |
| 10 | `PP_NVM_IMG_VALID` | R | X |  |
| 9 | `PP_NVM_STALE` | R | X |  |
| 8 | `PP_NVM_DIRTY` | R | X |  |
| 7 | `PP_NVM_BLANK` | R | X |  |
| 6 | `PP_NVM_BACKED` | R | X |  |
| 5 | `PP_ERR` | R | 0 |  |
| 4 | `PP_NVM_ALARM` | R | X |  |
| 3 | `PP_RESTORE_FAIL` | R | X |  |
| 2 | `PP_RESTORE_DONE` | R | X |  |
| 1 | `PP_RESTORE_BUSY` | R | X |  |
| 0 | `PP_BUSY` | R | 0 |  |

| Note |
|---|
| `[0]` `sp_busy`, a side-port access is outstanding, `[1]` `restore_busy`, either walk is running, or the parent's map restore that follows the D3 terminal (#637), `[2]` `restore_done`, both boot walks **sequenced** to COMPLETE or DEFAULTS and the parent's map restore ended, which is not the same as succeeded (never after CLOSED), `[3]` `restore_fail`, either walk failed, or a walk ran blind, or the parent's map restore rolled every map back to its reset set (a device error, a short read, a deadline, or a port that refused to give up or take back its reset set; it adds no cause of its own: `[20:18]` then reads 0, since it runs only after a D3 walk that ended with none, and `[22:21]` keeps the binding walk's) (#637), `[4]` `nvm_alarm`, a record producer (the binding manager, the D3 writer, or the parent map writer of records `0x60`/`0x70` (#637)) exhausted its three write attempts, 500 ms apart; reset-sticky, `[5]` `sp_err`, the last side-port access returned an error, `[6]` `nvm_backed`, **live fabric evidence, never a knob**: a writer heartbeat or completed transaction answered within `T-NVM-WRITER-ALIVE` (2000 ms) and no unrevoked failure is outstanding (design page 9.2), `[7]` `nvm_blank`, the completed restore validated **zero** records (neither walk nor the parent's map restore read a framed, crc-clean record) and none of them failed; beside `[3]` only for a blind walk, `[8]` `nvm_dirty`, the image holds committed changes no flash slot yet holds, `[9]` `nvm_stale`, `nvm_backed` was true since reset and is now false and the loss has not been made good, `[10]` `nvm_img_valid`, firmware validated the image in the window, `[11]` `nvm_pend`, **accepted work that no verified slot holds and `nvm_dirty` does not report**: a change a producer still holds (a binding, a scalar record the D3 writer has not yet written, a map record the parent's map writer has not yet written (#637), an accepted name write), a record whose logical write has not completed, or -- from reset until the boot window load is accepted -- every record, because none is known yet. The durable reading of design page 9.3 is therefore `(backed 1, dirty 0, stale 0)` **and this bit `0`** (snapshot-ownership page 6.1), `[15:12]` `nvm_verdict`, the section 6.2 verdict code of the last image offered, `[16]` `restore_closed`, the D3 walk ended CLOSED: fail, never done, AECP held until reset, `[17]` `restore_rb`, a pass-1 abort rolled the stores back to DEFAULTS, `[20:18]` `rs_cause`, the D3 walk's first abort cause, valid with `[3]` (`1` torn, `2` device error, `3` deadline, `5` the two passes disagree, `6` descriptor fault, `7` image not proven), `[22:21]` `restore_cause`, the binding walk's (`1` torn, `2` device error, `3` deadline), `[23]` reserved `0`, `[31:24]` **constant presence tag `0x5B`**. A read of `0` here means the gateware predates the group |

### PP_SPADDR register (offset 0x928) [reset = 0x00000000]

Side-port word address; a write posts a read.

RTL name: `A_PP_SPADDR`.

![PP_SPADDR bit fields](../../docs/diagrams/regmap/pp/PP_SPADDR.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:20 | `RESERVED` | R | 0 | Reserved. |
| 19:0 | `PP_SPADDR` | R/W | 0 |  |

| Note |
|---|
| `[19:0]` side-port **word** address. **A write here POSTS A READ** at that address (ignored while `sp_busy`); the answer lands in `PP_SPDATA`. Readback = the armed address. Snapshot word 37, `0x20025`, `[15:0]` counts the AECP frames dropped at the ingress slot gate while the D3 writer holds AECP |

### PP_SPDATA register (offset 0x92C) [reset = 0x00000000]

Posted read data; a write posts a side-port write.

RTL name: `A_PP_SPDATA`.

![PP_SPDATA bit fields](../../docs/diagrams/regmap/pp/PP_SPDATA.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PP_SPRDATA` | R/W | 0 | **Read**: the data of the last posted read. **Write**: posts a side-port WRITE of this value to the address already in `PP_SPADDR` (ignored while `sp_busy`) A write takes effect only when `!pp_busy_r`. A write sets PP_WDATA; a read returns this field. |

### PP_DIAG register (offset 0x930) [reset = 0xXXXXXXXX]

Control frames sent, received and dropped.

RTL name: `A_PP_DIAG`.

![PP_DIAG bit fields](../../docs/diagrams/regmap/pp/PP_DIAG.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:16 | `PP_TX_FRAMES` | R | X |  |
| 15:8 | `PP_RX_DROPS` | R | X |  |
| 7:0 | `PP_RX_FRAMES` | R | X | Bits [7:0] of the RTL value. |

| Note |
|---|
| Shadow evidence, and the only frame accounting the control plane now publishes: `[31:16]` control frames transmitted, `[15:8]` **RX drops** -- control frames lost to a full ingress FIFO, counted rather than silently absorbed, `[7:0]` control frames received. This replaces the per-plane PDU counters at `0x648`, `0x69C` and `0x6B0`, all of which are structural zeros |

### PP_NVM_SEL register (offset 0x934) [reset = 0x00000000]

Index of the backend word PP_NVM_DATA reads or writes.

RTL name: `A_PP_NVM_SEL`.

![PP_NVM_SEL bit fields](../../docs/diagrams/regmap/pp/PP_NVM_SEL.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:6 | `RESERVED` | R | 0 | Reserved. |
| 5:0 | `PP_NVM_SEL` | R/W | 0 |  |

| Note |
|---|
| `[5:0]` the backing store's word index that the next `PP_NVM_DATA` access names (design page section 8.2: a control tuple, never a data window). `0` image base, the byte address of the KLJ2 record image in main memory, 8-byte aligned; `1` image length in bytes, `0` = unconfigured, which is the blank-flash behaviour (a write to word `0` or `1` clears `img_valid`); `2` the sequence number of the image in the window, firmware's to keep; `3` status/verdict, write `[3:0]` verdict and `[4]` `img_valid`; `4` the strobe word, write-only, `[0]` heartbeat, `[1]` commit acknowledged with the capture identity in `[31:16]`, `[2]` commit started, `[3]` **ARM** a capture, `[4]` **ATTEST** it, `[5]` **RELEASE** it, `[6]` **RELOAD** the window (snapshot-ownership page 5.1); `5` the **capture identity**, 16 bits, advanced only by an accepted ARM, so it names captures and not attempts; `8`-`15` the **record ownership vector**, one bit per allocated record id, word `8 + k` holding ids `32k` to `32k + 31`, `1` = OPEN, the record's logical write has not completed and its last verified bytes stand; `0x20`+port the INPUT channel-map table, `0x30`+port the OUTPUT one, each entry `{framed length[31:16], byte prefix inside the group[15:0]}` for that STREAM_PORT. Readback = the index |

### PP_NVM_DATA register (offset 0x938) [reset = 0xXXXXXXXX]

The backend word PP_NVM_SEL names.

RTL name: `A_PP_NVM_DATA`.

![PP_NVM_DATA bit fields](../../docs/diagrams/regmap/pp/PP_NVM_DATA.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PP_NVM_CSR_RDATA` | R/W | X | the word `PP_NVM_SEL` names. Words `0`-`3` and both tables read back what was written; word `4` reads `0` (strobes have no state to read); words `5` and `8`-`15` are read-only fabric state A write sets PP_NVM_CSR_WDATA; a read returns this field. |

### PP_NVM_STAT register (offset 0x93C) [reset = 0xXXXXXXXX]

Backend status word on read, strobe word on write.

RTL name: `A_PP_NVM_STAT`.

![PP_NVM_STAT bit fields](../../docs/diagrams/regmap/pp/PP_NVM_STAT.svg)

| Bit | Field | Type | Reset | Description |
|---|---|---|---|---|
| 31:0 | `PP_NVM_CSR_RDATA` | R/W | X | A write sets PP_NVM_CSR_WDATA; a read returns this field. |

| Note |
|---|
| **Read** the backing store's status word. `[31:24]` **contract tag `0xC3`**, the register to read first here: `0` means the gateware predates the snapshot-ownership contract and a writer of that contract must disable itself rather than acknowledge under an older rule. `[23]` `unres`, at least one record is open (diagnostic; the ids are words `8`-`15`), `[22]` `nvm_pend`, the pending bit itself -- the same wire `PP_STAT[11]` carries, `[21]` **arm refused**, the last ARM was not accepted (a capture already open, an unconfigured or unvalidated image, a mutating request this backend already deferred still waiting, or no RELOAD accepted since reset), `[20]` **ack refused**, `[19]` **attested**, `[18]` **valid**, no mutating grant since the arm, `[17]` **hold**, mutating requests are being deferred, `[16]` **open**, a capture is open. `[15:12]` verdict (`0` `VD_OK` to `10` `VD_INCOMPLETE` are the section 6.2 codes of the last slot the firmware judged; `11` `VD_ERASE`, `12` `VD_PROGRAM` and `13` `VD_VERIFY` are the writer's transaction verdicts, published when a commit fails at that stage and left unacknowledged; a reported one **revokes `nvm_backed` when it is reported**, not eight seconds later at the commit deadline), `[11]` **reload refused**, the last RELOAD strobe was refused, `[10]` `commit_busy`, a commit is inside its `T-NVM-COMMIT-TIMEOUT` (8000 ms) bracket, `[9]` `nvm_stale`, `[8]` `nvm_dirty`, now the **committable** image work that drives a commit, `[7]` `img_valid`, `[6]` `nvm_backed`, `[5]` `img_cfg`, an image length is set, `[4]` `dev_busy`, a record operation is in flight on the device face, the processor's or, since #637, the parent map writer's (its restore reads records `0x60`/`0x70` right after the D3 terminal), `[3]` **load pending**, a boot window load MAY STILL BE ACCEPTED -- read it as that, not as "no RELOAD has been accepted": it falls both on an accepted RELOAD and the first time the window goes live, and `[2]` tells the two apart, `[2]` **load accepted**, a RELOAD HAS been accepted since reset; **while it is `0` the backend arms no capture**, so nothing in that boot can be captured, committed or retired. **Write** the strobe word (word `4`): `[0]` heartbeat re-arms `T-NVM-WRITER-ALIVE`, `[1]` commit acknowledged, whose `[31:16]` must quote the capture identity of word `5` and which retires only that capture's work, `[2]` commit started opens the bracket, `[3]` ARM, `[4]` ATTEST, `[5]` RELEASE, `[6]` RELOAD. A loss in the same cycle as a heartbeat wins, a completion in the same cycle as an acknowledgement stays owned (design page 9.2, snapshot-ownership page 5 and 6) |

## SoC CSR banks

LiteX assigns these banks; each spans one CSR page.

| Bank | Start address | End address | Size | Description |
|---|---|---|---|---|
| `ctrl` | `0xF0000000` | `0xF00007FF` | 2,048 (2 KiB) | SoC control: reset, scratch, bus errors. |
| `ddrphy` | `0xF0000800` | `0xF0000FFF` | 2,048 (2 KiB) | DDR3 PHY. |
| `identifier_mem` | `0xF0001000` | `0xF00017FF` | 2,048 (2 KiB) | SoC identifier string. |
| `milan_mac` | `0xF0001800` | `0xF0001FFF` | 2,048 (2 KiB) | Milan MAC wrapper: PHY reset, MDIO, MAC counters, loopback, link status. |
| `sdram` | `0xF0002000` | `0xF00027FF` | 2,048 (2 KiB) | DDR3 controller software interface. |
| `spiflash` | `0xF0002800` | `0xF0002FFF` | 2,048 (2 KiB) | QSPI flash controller. |
| `timer0` | `0xF0003000` | `0xF00037FF` | 2,048 (2 KiB) | Timer 0. |
| `uart` | `0xF0003800` | `0xF0003FFF` | 2,048 (2 KiB) | UART. |
| `ppmem` | `0xF000F800` | `0xF000FFFF` | 2,048 (2 KiB) | Protocol-processor memory-bridge observers, pinned to the last CSR page. |

### Milan registers in the LiteX banks

| Address | Register | Words | Mode | Description |
|---|---|---|---|---|
| `0xF0001800` | `milan_mac_phy_crg_reset` | 1 | RW | PHY reset of the port the image is built for (`--eth-port`): the PHY clock/reset block's `_reset` storage, which drives the PHY reset pin. This is the PHY reset; `PHY_RESET` (0x11C) is inert. `ETH_GUARD` does not gate it at this head. |
| `0xF0001804` | `milan_mac_phy_mdio_w` | 1 | RW | Software bit-bang MDIO write register (clock, output enable, data). |
| `0xF0001808` | `milan_mac_phy_mdio_r` | 1 | RO | Software bit-bang MDIO read register. |
| `0xF000180C` | `milan_mac_core_preamble_crc` | 1 | RO | LiteEth status, reset 1: the MAC core inserts and checks preamble and CRC. |
| `0xF0001810` | `milan_mac_core_rx_datapath_preamble_errors` | 1 | RO | LiteEth RX preamble error count. |
| `0xF0001814` | `milan_mac_core_rx_datapath_crc_errors` | 1 | RO | LiteEth RX CRC error count. |
| `0xF0001818` | `milan_mac_loopback` | 1 | RW | 1 = internal MAC TX to MAC RX loopback. |
| `0xF000181C` | `milan_mac_link_status` | 1 | RW | Link, speed and duplex published by firmware; mirrored into `MAC_STATUS` (0x110). Reset: link up, 1000 Mb/s on GMII (100 on MII), full duplex. |
| `0xF000F800` | `ppmem_desc_req` | 1 | RO | descriptor-image read bridge: `[31:16]` accesses **ISSUED** (one per bus access, counted at its start, not per held cycle), `[15:0]` accesses the bus **ACKED** without `err` |
| `0xF000F804` | `ppmem_desc_fault` | 1 | RO | `[31:16]` accesses answered with **err**, `[15:0]` accesses the watchdog **abandoned** with no answer at all |
| `0xF000F808` | `ppmem_resp_req` | 1 | RO | AECP response-buffer read+write bridge, same two fields. This face writes as well as reads: a write that faults voids the response rather than putting a half-written one on the wire |
| `0xF000F80C` | `ppmem_resp_fault` | 1 | RO | same two fields as `desc_fault`, for the response bridge |
| `0xF000F810` | `ppmem_stat` | 1 | RO | live state, not counts: `[0]` descriptor bridge **poisoned** (a timed-out access is still owed an answer; the next answer it collects is discarded), `[1]` descriptor bridge is driving `cyc`/`stb` **right now**, `[2]` response bridge poisoned, `[3]` response bridge driving `cyc`/`stb`, `[4]` the **LiteDRAM DFI hand-off has been seen** (see below), `[31:24]` constant presence tag `0x5B` -- the same tag as `PP_STAT`, and the register to read first: `0` here means the gateware predates this bank, which is otherwise indistinguishable from four zeroed counters |

### Protocol-processor memory bridges (LiteX CSR bank, `0xf000f800`)

| Note |
|---|
| **Read this when the entity answers `ENTITY_MISBEHAVING` and `PP_STAT` says the image is invalid.** The protocol processor fetches its descriptor tree, and writes its AECP responses through two Wishbone masters (`milan_desc_mem` and `milan_resp_mem`, both in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py)). They live on the SoC side of the `milan_datapath` boundary with no port into `milan_csr`; their instrumentation is therefore a generated SoC CSR bank and not part of the `0x9000_0000` window. |
| **Why the bank exists (2026-08-13).** On the flashed build both bridges wedged on an access the memory never acked, and every AECP command came back `ENTITY_MISBEHAVING`. The processor reported `img_valid = 0` with descriptor fault 8 and response fault 1, which is the same thing it reports when the bridges are never asked for anything at all. Nothing anywhere separated the two readings, and they have opposite causes: one is a dead request path inside the fabric, the other is the bus. Finding that out took a board, a week and several wrong hypotheses. These five words are that week. Priced on the shipping AX shape, the observer alone (yosys `synth_xilinx`, out of context): 130 flops and 46 LUTs, plus 8 INV, 32 CARRY4 and 6 MUXF7 / 2 MUXF8 for the eight increments and their saturation compares. Whole-SoC delta against the same elaboration one commit back: **+177 flops as migen emits them, +162 after `opt_clean`** (20,218 -> 20,380 flop bits) and no register anywhere resized or removed. The 177 break down exactly: 130 the counters (8 counters x 16 bits, plus the two edge-detect flops), 32 the new bank's own read register, and 15 CSR strobe flops (a `_re` and a `_we` per register, plus 5 `wr_stb`) that are dead on a read-only bank and that any synthesiser drops - which is the 177-versus-162. Registers are the slack resource here (45.8% used against slices at 99.9%), which is why the counters are flops and not a LUT-built structure. |
| **The verdict table.** Read `desc_req` and `desc_fault` (or the `resp_` pair) and compare: |

| ISSUED | ACKED + ERRORED + TIMED OUT | verdict |
|---|---|---|
| `0` | `0`, `stat[4]` = `0` | the bridges are **held off the bus**: the BIOS has not handed the DFI back to the LiteDRAM controller yet, so both answer `err` without touching the bus. Expected between FPGA configuration and the end of `sdram_init`, and a standing `0` here means the BIOS never got that far |
| `0` | `0`, `stat[4]` = `1` | the bridge **never asked the bus**. The bus is not the fault: look at the processor's request face (`PP_DIAG` `0x930`, the side-port snapshot) |
| `> 0` | equal to ISSUED | every access completed. If the image is still invalid the fault is upstream of the bus: the descriptor image itself, or its base |
| `> 0` | one short of ISSUED | an access is **outstanding right now**. `stat[1]`/`stat[3]` say which face is still holding `cyc`/`stb`; it will become a `timed_out` when the watchdog expires |
| `> 0` | ERRORED > 0 | the interconnect answered `err` (LiteX raises `err` **with** `ack`, so a failed access is an answer, not a silence). A descriptor fetched this way is refused, never served |
| `> 0` | TIMED OUT > 0 | the access was **never answered** and the watchdog abandoned it. `stat[0]`/`stat[2]` show the master poisoned until the memory pays the answer it still owes |

| Note |
|---|
| All five words are live RO, free-running from reset, and every counter **saturates at `0xFFFF`** -- `0xFFFF` means "at least 65,535", never "none". A fault counter must not wrap to a small number at exactly the moment it matters. |
| **Know the ceiling before you read the table.** ISSUED and ACKED are the two rails a healthy bus advances, and on a busy entity they peg. One controller enumeration walks the whole descriptor tree as 64-bit beats, so a pass costs hundreds to a few thousand accesses (not measured here -- count it off ISSUED across one enumeration if you need the real figure), which puts 65,535 tens to hundreds of enumerations away: days under a compliance campaign, not years. Once both rails read `0xFFFF` the **subtraction is dead** -- the "one short of ISSUED" row above cannot be evaluated at all, and `stat[1]` / `stat[3]` are the only live reading of an outstanding access. The two rows that survive saturation are the two that matter most, because the fault counters do not advance on a healthy bus: `ISSUED = 0` still means *never asked*, and `TIMED OUT > 0` still means *asked and never answered*. There is no clear: these words answer "has this ever happened", never "is it happening now". |
| **What `stat[4]` measures, and what it does not.** It is `sw_seen & sel` on LiteDRAM's DFI select (`litedram/dfii.py` `DFIInjector`, whose `sel` **resets to 1**), so it reads 1 once the BIOS has taken the DFI to software control and handed it back, i.e. once it got past `sdram_init`. It is a **proxy for the boot's progress, not a readiness signal for the path the bridges use**: the main-memory interconnect and memory controller sit beyond the bridge observer, and nothing in this bank observes their final destination. A build without DDR3 ties the bit to 1. Its **position is the two-face shape's**: the flag is appended after the per-face pairs, so a third bridge would move it to `[6]`. |
| **The bank is pinned to the LAST page of the CSR window** (`n_locs - 1`), not auto-allocated. LiteX hands out the lowest free page at the moment a module is added, and an auto-allocated bank here lands on `sdram`'s page and pushes `sdram` **and** `spiflash` up `0x800` -- moving the LiteSPI bank whose master port at bank+`0x10` is a write path to the boot flash, under anything that hard-codes it. Verified by csr.csv diff: no existing bank moved. The absolute base is still the build's own `csr.csv`, exactly like every other address in this section. |

## Feature status

These rows come from the feature status ledger.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gateware.current-version` | `implemented` | `0x0002_0060` |
| `aaf.media-clock-following` | `implemented` | - |
| `gptp.fabric-product-owner` | `implemented` | - |
| `aem.served-command-set` | `implemented` | - |
| `aem.acquire-entity-refusal` | `not-supported` | - |
| `aem.mandatory-missing-set` | `implemented` | - |
| `stream-input.start-stop` | `implemented` | - |
| `stream-input.stopped-crf-observation` | `implemented` | - |
| `stream-format.set` | `implemented` | - |
| `stream-info.set-acc-lat` | `implemented` | - |
| `crf.media-clock-consumption` | `implemented` | - |
| `state.nonvolatile-persistence` | `partial` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->
