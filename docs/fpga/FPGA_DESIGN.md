# FPGA design reference - every module in `hdl/`, and how they compose

The complete map of the gateware: what each RTL module does, its interfaces
and clock domain, which harness verifies it, and where its detailed doc
lives. Companion pages: [../integration/INTEGRATION_GUIDE.md](../integration/INTEGRATION_GUIDE.md)
(the outside of the boundary), [../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md)
(the CSR ABI), [PIPELINE_STAGES.md](PIPELINE_STAGES.md) (stage-by-stage
datapath prose), [pipeline-telemetry.md](pipeline-telemetry.md) (the
in-fabric observability block).

## Contents

- **[0. Global conventions](#0-global-conventions)** — The four rules every module obeys: 64-bit big-endian AXIS (wire order *is* memory order, so the CPU never byte-swaps), AXI4-Lite CSR decoded in 0x100 groups, house style, no vendor primitives. Also flags one relic — the `AXIS_TDEST_WIDTH 2` define is dead outside the legacy xsim TBs.
- **[1. Top level - two wrappers, one datapath](#1-top-level---two-wrappers-one-datapath)** — What each wrapper adds around the same datapath, and the TX/RX/TS pipeline drawn out. The sentence that changes how you read every other page: only CPU-originated frames traverse the classifier, the queues and the CBS — the fabric engines inject *after* the shaper and the RX media path taps *before* the dest-MAC filter. §1.1 adds the audio chain as composed on main, both new stages defaulting to bypass.
- **[2. Module inventory (from the RTL banners; refreshed 2026-07-26)](#2-module-inventory-from-the-rtl-banners-refreshed-2026-07-26)** — Every module in `hdl/`, one row each, grouped by directory, with descriptions lifted from the RTL banners. It states no total on purpose: the live count belongs to the generated matrix, and `ls hdl/` is the authority.
- **[3. Clock domains & CDC (complete inventory)](#3-clock-domains--cdc-complete-inventory)** — Which of the four domains each block lives in, and the complete crossing list — all plain-FF or handshake, no vendor macros. Explains why the timestamp metadata FIFOs are deliberately same-clock: the crossing already happened upstream in `ptp_ts_core`.
- **[4. What is *not* in hdl/ (and where it lives instead)](#4-what-is-not-in-hdl-and-where-it-lives-instead)** — Four things you will hunt for in the RTL tree and not find. Mainly the ring-DMA engines, which are Migen inside `milan_soc.py` rather than SystemVerilog, and the MAC, which is external by design.
- **[5. Per-module doc regeneration](#5-per-module-doc-regeneration)** — How the `hdl/**/doc/*.md` pages are produced, which three are hand-written exceptions, and the current list of modules with no page at all. Tie-break rule if a page lags: the RTL wins.

## 0. Global conventions

* **AXIS:** 64-bit `tdata`, 8-bit `tkeep`, `tlast`, and `$clog2(NUMBER_OF_QUEUES)`
  = **3**-bit `tdest` where routed (`traffic_controller_802_1q`, since the queue
  count went to 6); big-endian byte order (wire order == memory order, so the CPU
  never swaps). The `` `AXIS_TDEST_WIDTH 2 `` define in
  `hdl/common/parameters.svh` is a relic referenced only by the legacy xsim TBs
  — the live path derives the width from the queue count.
* **CSR:** AXI4-Lite, 16-bit offset (64 KB window), 32-bit data, decoded in
  `milan_csr` in 0x100 groups.
* **Style:** SystemVerilog, `` `default_nettype none ``, TerosHDL `//!`
  comments on every generic/port/signal, named `always_*` processes.
* **No vendor primitives** - see
  [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §2 for
  the audited inventory of the few vendor-*attributes* that remain.

## 1. Top level - two wrappers, one datapath

| Wrapper | File | Host | Contains |
|---|---|---|---|
| `milan_datapath` | `hdl/milan/milan_datapath.sv` | LiteX RISC-V SoC (and the Verilator/Yosys flows) | everything below, MAC-less and PS-less - **the integration boundary** |
| `milan_top` | `hdl/milan/milan_top.sv` | Zynq-7020 PS (`bd/milan-dma.tcl`, `milan_dma_wrapper.v`) | same datapath + the verilog-ethernet `eth_mac_1g_rgmii_fifo` MAC (external source) + PS wiring |

Pipeline (identical in both wrappers):

```
TX: DMA ──► traffic_controller_802_1q ──► ptp_ts_top(TX stamp) ──► adp_tx_arbiter ──► MAC
            (classify ► 5 queues ► CBS)                                ▲
                          fabric engines (AAF talker, ADP/ACMP/AECP,   │
                          MAAP, CRF, lwSRP) inject HERE ───────────────┘
RX: MAC ──► ptp_ts_top(RX stamp) ─┬─► rx_mac_filter(TCAM) ──► DMA        (host copy)
                                  └─► avtp_stream_parser ► stream table ► RX monitor
                                      ► depacketizer ► PCM route ► ring / DAC
TS: ptp_ts_top ──► m_axis_ts (timestamp metadata records) ──► DMA
```

**Only CPU-originated frames traverse the classifier, the queues and the CBS.**
The fabric engines merge in *after* the shaper, and the RX media path taps
*before* the dest-MAC filter. Hop-by-hop, with the CSR to read at each stage:
[DATAPLANE_WALKTHROUGH.md](DATAPLANE_WALKTHROUGH.md).


### 1.1 TX audio chain as composed on main (2026-07-25 merge round)

```mermaid
flowchart LR
    ADC[I2S / tone capture front-end] --> PB{{item-7 playback mux\npb_enable, def 0}}
    RING[KL_pcm_tx DRAM ring] --> PB
    PB --> CM{{chmap capture mux\nCHMAP_CTRL 0x900, def 0}}
    CM --> PKT[KL_aaf_packetizer] --> MERGE[traffic merge + CBS] --> MAC[MilanMAC + PTP stamp] --> WIRE((wire))
    WIRE --> RX[classifier + depacketizer] --> RB[PCM DMA ring _PCMRingNxN] --> ALSA[snd-kl-milan arecord]
    RX --> XBAR[chmap render xbar] --> TDM[KL_tdm_render / I2S out]
```

Both new stages default to bypass: with `pb_enable=0` and `chmap_enable=0`
the packetizer input is bit-identical to the pre-merge datapath.

## 2. Module inventory (from the RTL banners; refreshed 2026-07-26)

Every `module` in `hdl/`, one row each; descriptions are the modules' own banner
lines. **No count is stated here on purpose** — counts in prose go stale.
[`../traceability/MODULE_MATRIX.md`](../traceability/MODULE_MATRIX.md) is
*generated* from the tree, prints the live total, and is gated for drift by
`gen_module_matrix.py --check`; `ls hdl/` is the ultimate authority. Regenerate
this table whenever `hdl/` changes shape.

### `hdl/common/`

| module | description |
|---|---|
| `KL_link_guard` |  |
| `axis_mux_rr_2in_1out` | Slave 0 axis interface |
| `cdc_handshake` | File        : cdc_handshake.sv |
| `cdc_pair_fifo` | Gray-pointer dual-clock FIFO, WIDTH x 2^LOG2D. Flags are conservative |
| `cdc_pulse` | File        : cdc_pulse.sv |

### `hdl/common/csr/`

| module | description |
|---|---|
| `milan_csr` |  |

### `hdl/common/eth_event_counter/`

| module | description |
|---|---|
| `KL_mac_rmon_events` | Derives the `ethernet_events` pulse vector from a soft MAC's boundary signals (AXIS handshakes, bad-frame flag, FCS/preamble counts) — the block that revived RMON at VERSION `0x0013`. |
| `ethernet_events` | This module instantiates multiple `event_counter` modules, one for each |
| `event_counter` | This module implements a simple synchronous event counter. |

### `hdl/common/`

| module | description |
|---|---|
| `tx_ifg_gasket` | File        : tx_ifg_gasket.sv |

### `hdl/ieee1722/aaf/`

| module | description |
|---|---|
| `KL_aaf_capture_i2s` | Audio capture front-end (NXN §2.1 / P4): the I2S/CDC half of the old |
| `KL_aaf_latency_chain` |  |
| `KL_aaf_latency_taps` | Per-stage TX/RX latency tap chains (item-11) feeding the `LTAP` CSR group at `0x870`. |
| `KL_aaf_packetizer` |  |
| `KL_aaf_rx_depacketizer` |  |
| `KL_aes3_rx` | AES3 / S-PDIF biphase-mark receiver (item-4 front-end family): recovered pairs into the capture path. |
| `KL_aes3_tx` | AES3 / S-PDIF biphase-mark transmitter (item-4 front-end family). |
| `KL_chan_map_capture` |  |
| `KL_chan_map_render` |  |
| `KL_i2s_feed_mux` | DAC feed selector: the legacy listener render tap, or the render crossbar paced by the 48 kHz media tick (item-7 playback chain). |
| `KL_i2s_playback` | I2S DAC serializer, clean-clocked: PCM tap (wire-order S32BE interleave, |
| `KL_lat_history_ring` |  |
| `KL_media_adv` | Fractional-N advance strobe: adv_o duty = TICK_HZ / CLK_FREQ_HZ exactly |
| `KL_pcm_lpf` |  |
| `KL_pcm_ring_bram` |  |
| `KL_pcm_route` |  |
| `KL_pcm_tx` |  |
| `KL_tdm_capture` |  |
| `KL_tdm_render` |  |
| `KL_tone_gen` | 1 kHz / 0 dBFS pilot tone: 48-sample exact-period 24-bit sine table |
| `aaf_talker_i2s` | File        : aaf_talker_i2s.sv |

### `hdl/ieee1722/avtp/`

| module | description |
|---|---|
| `KL_avtp_common_parser` |  |
| `KL_avtp_rx_monitor` |  |
| `KL_avtp_rx_monitor_ctx` |  |
| `KL_stream_table` |  |
| `avtp_stream_parser` |  |

### `hdl/ieee1722/crf/`

| module | description |
|---|---|
| `KL_crf_rx` |  |
| `KL_crf_tx` |  |
| `KL_mmcm_drp_servo` |  |

### `hdl/ieee1722/maap/`

| module | description |
|---|---|
| `KL_maap` |  |

### `hdl/ieee17221/acmp/`

| module | description |
|---|---|
| `KL_acmp_listener` | File        : KL_acmp_listener.sv |
| `KL_acmp_lstn_ctx` | File        : KL_acmp_lstn_ctx.sv |
| `KL_acmp_responder` | File        : KL_acmp_responder.sv |
| `KL_acmp_tlkr_ctx` | File        : KL_acmp_tlkr_ctx.sv |

### `hdl/ieee17221/adp/`

| module | description |
|---|---|
| `KL_adp_parser` |  |
| `adp_advertiser` | File        : adp_advertiser.sv |
| `adp_tx_arbiter` | File        : adp_tx_arbiter.sv |

### `hdl/ieee17221/aecp/`

| module | description |
|---|---|
| `KL_aecp_accessor` |  |
| `KL_aecp_aem_dyn_mux` |  |
| `KL_aecp_aem_store` |  |
| `KL_aecp_common_parser` |  |
| `KL_aecp_ingress` |  |
| `KL_aecp_l0_state` |  |
| `KL_aecp_packet_validator` |  |
| `KL_aecp_response_builder` |  |
| `KL_aecp_timers` |  |
| `KL_aecp_top` |  |
| `KL_persist_journal` | `KLJ1` saved-state journal decode + replay (RTL and Verilator-proven; its CSR ingest group `0x7B8`-`0x7C4` is not wired into `milan_csr` yet). |

### `hdl/ieee8021as/ptp_timestamp/`

| module | description |
|---|---|
| `ptp_csr_sync` |  |
| `ptp_ts_core` |  |
| `ptp_ts_top` | MAC-side convention - adp_advertiser.sv, |
| `timestamp_counter` |  |

### `hdl/ieee8021q/filtering/`

| module | description |
|---|---|
| `rx_mac_filter` | File        : rx_mac_filter.sv |
| `tcam` | File        : tcam.sv |

### `hdl/ieee8021q/srp/`

| module | description |
|---|---|
| `KL_lwsrp_bw_gate` | File        : KL_lwsrp_bw_gate.sv |
| `KL_lwsrp_ctx` | File        : KL_lwsrp_ctx.sv |
| `KL_lwsrp_ctx_tx` | File        : KL_lwsrp_ctx_tx.sv |
| `KL_lwsrp_ingress` | File        : KL_lwsrp_ingress.sv |
| `KL_lwsrp_registrar` | File        : KL_lwsrp_registrar.sv |
| `KL_lwsrp_rx` | File        : KL_lwsrp_rx.sv |
| `KL_lwsrp_ta_registrar` | File        : KL_lwsrp_ta_registrar.sv |
| `KL_lwsrp_timers` | File        : KL_lwsrp_timers.sv |
| `KL_lwsrp_top` | File        : KL_lwsrp_top.sv |
| `KL_lwsrp_tx` | File        : KL_lwsrp_tx.sv |
| `KL_lwsrp_walker` | File        : KL_lwsrp_walker.sv |

### `hdl/ieee8021q/ts/`

| module | description |
|---|---|
| `credit_based_shaper` |  |
| `traffic_class_map` |  |
| `traffic_classifier` | This module implements an Ethernet packet classifier that parses incoming AXIS frames and |
| `traffic_controller_802_1q` |  |
| `traffic_queues` | One-hot: indicates granted queue |
| `traffic_shaping_core` |  |

### `hdl/milan/`

| module | description |
|---|---|
| `milan_datapath` | This is the single clean HW/gateware boundary the LiteX SoC (sw/litex/milan_soc.py) |
| `milan_top` |  |

<!-- Count deliberately not stated here: docs/traceability/MODULE_MATRIX.md is
     GENERATED from the tree and prints the live total; `ls hdl/` is authoritative. -->


Each module's authoritative documentation is its own header banner (house
style: `//!` port docs); this table is the index, not the spec.

## 3. Clock domains & CDC (complete inventory)

| Domain | Contents |
|---|---|
| `axis_clk` (100 MHz `cd_milan` in the deployed LiteX build; ~50 MHz only when split via `--milan-clk-freq`) | all of §2 except the PHC |
| `gtx_clk` (125 MHz) | `timestamp_counter` (PHC), MAC-side timestamp capture |
| MAC RX recovered clock | inside the external MAC only |
| host clocks (PS7 / LiteX `sys`, `sys4x`, `idelay`) | outside the datapath |

Crossings - all in-fabric, all `(* ASYNC_REG *)` plain-FF or handshake based
(no vendor macros): `ptp_csr_sync` (CSR commands → PHC, snapshot return),
`cdc_pulse` + `cdc_handshake` inside `ptp_ts_core` (SOP pulse, timestamp
value), the 2-FF `i_mac_speed` sync in the wrappers. Timestamp metadata
FIFOs are same-clock (`axis_clk`) on purpose - the crossing happens in
`ptp_ts_core`/`ptp_csr_sync`, not in the FIFOs. Constraint requirements per
toolchain: [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §4.5.

## 4. What is *not* in `hdl/` (and where it lives instead)

* **The ring-DMA engines** (`RingDMAReader`/`RingDMAWriter`, BD formats,
  header-split, RSC/GRO) are **Migen**, inside `sw/litex/milan_soc.py` -
  design docs: [CPPI_DMA_REDESIGN.md](../../historical_now_obsolete/fpga/CPPI_DMA_REDESIGN.md),
  [HW_GRO_RSC.md](../../historical_now_obsolete/fpga/HW_GRO_RSC.md),
  [HEADER_SPLIT_DESIGN.md](HEADER_SPLIT_DESIGN.md) (includes the hsq12 cut-through chapter); running system view:
  [PIPELINE_STAGES.md](PIPELINE_STAGES.md).
* **The MAC** - external by design (LiteEth on LiteX, verilog-ethernet on
  Zynq).
* **The telemetry block** `milan_tlm` - [pipeline-telemetry.md](pipeline-telemetry.md).
* **The CPU/SoC** - [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md).

## 5. Per-module doc regeneration

The `hdl/**/doc/*.md` pages are TerosHDL-generated from the in-code `//!`
comments (plus a few hand-written ones: [`tcam.md`](../../hdl/ieee8021q/filtering/doc/tcam.md), [`adp_advertiser.md`](../../hdl/ieee17221/adp/doc/adp_advertiser.md),
[`milan_csr.md`](../../hdl/common/csr/doc/milan_csr.md)). Regenerate after RTL changes by running the TerosHDL
documenter on the `.sv` - and treat the RTL as the source of truth if a
generated page lags. Modules currently missing a doc page:
`milan_datapath`/`milan_top` (rich header comments serve instead),
`rx_mac_filter`, `cdc_pulse`/`cdc_handshake`, `ptp_csr_sync`,
`avtp_stream_parser`, `adp_tx_arbiter`, `axis_mux_rr_2in_1out`,
`traffic_class_map`.
