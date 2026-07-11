# FPGA design reference - every module in `hdl/`, and how they compose

The complete map of the gateware: what each RTL module does, its interfaces
and clock domain, which harness verifies it, and where its detailed doc
lives. Companion pages: [../integration/INTEGRATION_GUIDE.md](../integration/INTEGRATION_GUIDE.md)
(the outside of the boundary), [../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md)
(the CSR ABI), [PIPELINE_STAGES.md](PIPELINE_STAGES.md) (stage-by-stage
datapath prose), [pipeline-telemetry.md](pipeline-telemetry.md) (the
in-fabric observability block).

## 0. Global conventions

* **AXIS:** 64-bit `tdata`, 8-bit `tkeep`, `tlast`, 2-bit `tdest` where
  routed (`hdl/common/parameters.svh`); big-endian byte order (wire order ==
  memory order, so the CPU never swaps).
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
| `milan_datapath` | `hdl/common/milan_datapath.sv` | LiteX RISC-V SoC (and the Verilator/Yosys flows) | everything below, MAC-less and PS-less - **the integration boundary** |
| `milan_top` | `hdl/common/milan_top.sv` | Zynq-7020 PS (`bd/milan-dma.tcl`, `milan_dma_wrapper.v`) | same datapath + the verilog-ethernet `eth_mac_1g_rgmii_fifo` MAC (external source) + PS wiring |

Pipeline (identical in both wrappers):

```
TX: DMA ──► traffic_controller_802_1q ──► ptp_ts_top(TX stamp) ──► adp_tx_arbiter ──► MAC
            (classify ► queues ► CBS)                                  ▲
                                                          adp_advertiser┘
RX: MAC ──► ptp_ts_top(RX stamp) ──► rx_mac_filter(TCAM) ──► DMA
TS: ptp_ts_top ──► m_axis_ts (timestamp metadata records) ──► DMA
```

## 2. Module inventory

Columns: **Verified by** names the `tb/verilator/` suite (see
[../testing/TESTING.md](../testing/TESTING.md)); **Doc** is the per-module
reference under `hdl/**/doc/`.

### 2.1 `hdl/802_1q_traffic_shaper/` - classification + 802.1Qav shaping

| Module | Purpose | Clock | Verified by | Doc |
|---|---|---|---|---|
| `traffic_controller_802_1q` | subsystem top: classifier → queues → shaping core, CSR-configured | `axis_clk` | `datapath`, `controller_rate` | [doc](../../hdl/802_1q_traffic_shaper/doc/traffic_controller_802_1q/traffic_controller_802_1q.md) |
| `traffic_classifier` | VLAN/PCP/EtherType parse → per-frame `tdest` sideband (redesigned after the [CBS datapath bug](../findings/CBS_DATAPATH_BUG.md)); buffers via `axis_fifo` | `axis_clk` | `classifier` | [doc](../../hdl/802_1q_traffic_shaper/doc/traffic_classifier/traffic_classifier.md) |
| `traffic_class_map` | 802.1Q PCP→regen→traffic-class→queue decode | `axis_clk` | `cls` | - |
| `traffic_queues` | `axis_demux` (1→4 by `tdest`) → 4× `axis_fifo` (depth 1024 as instantiated) → grant-indexed combinational egress mux | `axis_clk` | `queues` | [doc](../../hdl/802_1q_traffic_shaper/doc/traffic_queues/traffic_queues.md) |
| `traffic_shaping_core` | grant arbiter over N queues: strict priority + CBS gating | `axis_clk` | `shaper_core` | [doc](../../hdl/802_1q_traffic_shaper/doc/traffic_shaping_core/traffic_shaping_core.md) |
| `credit_based_shaper` | per-class 802.1Qav credit accumulator (signed 48-bit; `use_dsp` hint; the 100 MHz critical path - see [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §4.5) | `axis_clk` | `cbs` (87 k checks vs fixed-point + ideal models) | [doc](../../hdl/802_1q_traffic_shaper/doc/credit_based_shaper/credit_based_shaper.md) |

### 2.2 `hdl/ptp_timestamp/` - PTP hardware clock + timestamping

| Module | Purpose | Clock | Verified by | Doc |
|---|---|---|---|---|
| `ptp_ts_top` | subsystem top: PHC + TX/RX stampers + metadata buffering (3× `axis_fifo`, all `axis_clk`) | `axis_clk` + `gtx_clk` | (via `milan_dp`; legacy itest) | [doc](../../hdl/ptp_timestamp/doc/ptp_ts_top.md) |
| `ptp_ts_core` | SOP detect + timestamp capture; crosses domains via `cdc_pulse`/`cdc_handshake` | both | (via `milan_dp`) | [doc](../../hdl/ptp_timestamp/doc/ptp_ts_core.md) |
| `timestamp_counter` | free-running adjustable PHC (Q(INT).FRAC ns: rate, adjfine, settime, adjtime, snapshot) | `gtx_clk` | `ptp` (201 k checks vs 128-bit model) | [doc](../../hdl/ptp_timestamp/doc/timestamp_counter.md) |
| `ptp_csr_sync` | CSR↔PHC command/return CDC (plain-FF `ASYNC_REG` synchronizers, no XPM) | `axis_clk` ↔ `gtx_clk` | `ptp_sync` | - |

### 2.3 `hdl/adp/` - IEEE 1722.1 discovery (ADP)

| Module | Purpose | Clock | Verified by | Doc |
|---|---|---|---|---|
| `adp_advertiser` | byte-exact ADPDU transmit FSM: AVAILABLE/DEPARTING, `available_index`, advertise timer, entity model from CSR group 0x600 | `axis_clk` | `adp` (121 checks) | [doc](../../hdl/adp/doc/adp_advertiser.md) |
| `adp_tx_arbiter` | 2→1 packet arbiter merging ADP into the MAC TX stream | `axis_clk` | `adp_tx` | - |
| `KL_adp_parser` | ADPDU receive parser (discover/available/departing + entity info) | `axis_clk` | (legacy utest) | [doc](../../hdl/adp/doc/kl-adp-parser/KL_adp_parser.md) |
| `adp_pkg` | ADP constants/fields package | - | - | - |

### 2.4 `hdl/1722/` - IEEE 1722 AVTP

| Module | Purpose | Clock | Verified by | Doc |
|---|---|---|---|---|
| `KL_avtp_common_parser` | AVTP common-header parse (subtype, control vs stream) | `axis_clk` | (legacy utest) | [doc](../../hdl/1722/doc/kl-avtp-common-parser/KL_avtp_common_parser.md) |
| `avtp_stream_parser` | RX AVTP stream-header monitor vs a programmable stream-id table (the S1 AVTP-engine foundation) | `axis_clk` | `avtp_stream` (21 checks) | - |
| `avtp_subtype_pkg` | AVTP subtype constants | - | - | - |

### 2.5 `hdl/csr/` - control plane

`milan_csr` (`hdl/csr/milan_csr.sv`): the AXI4-Lite CSR block - ID/IRQ
(0x000), MAC control (0x100), RMON stats (0x200), classifier (0x300), CBS
per-queue (0x400 + q*0x20), PTP clock (0x500), ADP entity model (0x600),
RX filter/TCAM programming (0x700). Verified by `csr` (the executable form of
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md));
doc: [milan_csr.md](../../hdl/csr/doc/milan_csr.md).

### 2.6 `hdl/eth_event_counter/` - RMON

`ethernet_events` instantiates 9× `event_counter` on the MAC's RMON event
pulse lanes (`ethernet_events.svh` enum), with snapshot/reset from CSR
group 0x200 and rollover IRQ. Docs:
[ethernet_events.md](../../hdl/eth_event_counter/doc/ethernet_events.md),
[event_counter.md](../../hdl/eth_event_counter/doc/event_counter.md).

### 2.7 `hdl/common/` - integration, filtering, CDC, utilities

| Module | Purpose | Verified by | Doc |
|---|---|---|---|
| `milan_datapath` / `milan_top` / `milan_dma_wrapper` | the wrappers (§1) | `milan_dp` (wrapper-level) | header comments (extensive) |
| `tcam` | register-based ternary CAM (key/mask/action, priority hit) | `tcam` (19) | [doc](../../hdl/common/doc/tcam.md) |
| `rx_mac_filter` | TCAM-driven dest-MAC RX filter (whitelist/blacklist/range, cut-through) | `rx_filter` (14) | - |
| `cdc_pulse` / `cdc_handshake` | open CDC primitives (toggle-sync pulse; 4-phase req/ack value) that replaced `xpm_cdc_*` | `cdc` (16, two independent clocks) | - |
| `axis_mux_rr_2in_1out` | round-robin 2→1 AXIS packet mux (TS stream merge) | (via `milan_dp`) | - |
| `ethernet_packet_pkg` / `parameters.svh` / `axi_stream_if` | global constants, AXIS defines, SV interface | - | - |

### 2.8 Vendored cores - `third_party/verilog-axis` (submodule)

`axis_fifo`, `axis_demux` (+ `arbiter`, `priority_encoder`; `axis_arb_mux`
is carried in the source list and portability checks but no longer
instantiated in the datapath). MIT-licensed, pinned by gitlink - see
[`THIRD_PARTY.md`](../../THIRD_PARTY.md). **Must be initialized before any
build/sim:** `git submodule update --init third_party/verilog-axis`.

## 3. Clock domains & CDC (complete inventory)

| Domain | Contents |
|---|---|
| `axis_clk` (~100 MHz, or its own 50 MHz `cd_milan` in the deployed LiteX build) | all of §2 except the PHC |
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
  design docs: [CPPI_DMA_REDESIGN.md](CPPI_DMA_REDESIGN.md),
  [HW_GRO_RSC.md](HW_GRO_RSC.md), [HEADER_SPLIT_DESIGN.md](HEADER_SPLIT_DESIGN.md),
  [HSPLIT14_DESIGN.md](HSPLIT14_DESIGN.md); running system view:
  [PIPELINE_STAGES.md](PIPELINE_STAGES.md).
* **The MAC** - external by design (LiteEth on LiteX, verilog-ethernet on
  Zynq).
* **The telemetry block** `milan_tlm` - [pipeline-telemetry.md](pipeline-telemetry.md).
* **The CPU/SoC** - [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md).

## 5. Per-module doc regeneration

The `hdl/**/doc/*.md` pages are TerosHDL-generated from the in-code `//!`
comments (plus a few hand-written ones: `tcam.md`, `adp_advertiser.md`,
`milan_csr.md`). Regenerate after RTL changes by running the TerosHDL
documenter on the `.sv` - and treat the RTL as the source of truth if a
generated page lags. Modules currently missing a doc page:
`milan_datapath`/`milan_top` (rich header comments serve instead),
`rx_mac_filter`, `cdc_pulse`/`cdc_handshake`, `ptp_csr_sync`,
`avtp_stream_parser`, `adp_tx_arbiter`, `axis_mux_rr_2in_1out`,
`traffic_class_map`.
