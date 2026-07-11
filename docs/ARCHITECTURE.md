# Milan TSN FPGA  -  architecture & developer guide

This document is the map a new developer should read first. It explains the
datapath, the control plane, the clock domains, how the HDL maps to the Linux
driver and device tree, and **where to change things**. For the *what/why*, see
[`REQUIREMENTS.md`](../REQUIREMENTS.md); for the *ordered work*, see
[`TODO.md`](../TODO.md); for the register ABI, see
[`REGISTER_MAP.md`](REGISTER_MAP.md).

---

## 1. Repository layout

```
milan-fpga/
├─ REQUIREMENTS.md          normative requirements + gap analysis (§3/§4)
├─ TODO.md                  phased, dependency-ordered task list
├─ docs/
│  ├─ ARCHITECTURE.md       this file
│  └─ REGISTER_MAP.md       AXI4-Lite CSR ABI (HDL/driver/DT contract)
├─ hdl/
│  ├─ common/               milan_top, DMA wrapper, AXIS iface, eth pkg, params
│  ├─ csr/                  milan_csr.sv  ← memory-mapped control plane (+ doc/)
│  ├─ 802_1q_traffic_shaper/ classifier + traffic_class_map + FIFOs + CBS + arbiter
│  ├─ ptp_timestamp/        PHC counter + ptp_csr_sync (CDC) + TX/RX ts cores
│  ├─ eth_event_counter/    RMON-style event counters
│  ├─ 1722/ , adp/          AVTP / ADP parsers (not on the NIC datapath)
├─ bd/milan-dma.tcl         Vivado block design (PS + AXI-DMA + interconnect)
├─ constraints/             clocks.xdc, rgmii.xdc, ila.xdc
└─ tb/
   ├─ verilator/            runnable, self-checking harnesses (see its README)
   │  ├─ cbs/               802.1Qav credit-based-shaper verification
   │  └─ csr/               milan_csr AXI4-Lite verification
   ├─ utests/ , itests/     legacy Vivado/xsim testbenches
   └─ avtp_packet_gen_sv/   AVTP stimulus classes
```

## 2. System block diagram

```
              ┌───────────────────────────── Zynq-7020 PS ─────────────────────────────┐
              │  ARM CoreSight/GIC        DDR ctrl        M_AXI_GP0        S_AXI_HP0     │
              └────────┬───────────────────┬─────────────────┬───────────────┬─────────┘
                  IRQ_F2P             (DDR pins)         (AXI-Lite)       (AXI-MM, DMA)
                       │                                     │                 │
        ┌──────────────┴─────────────────────────────────────┴─────────────────┴──────────┐
        │ PL (milan_top)                                     │                              │
        │                                    ┌───────────────┴────────────────┐            │
        │                                    │   milan_csr (AXI4-Lite CSR)     │  ← NEW     │
        │                                    │  ID/CAP/IRQ · MAC · RMON ·      │            │
        │                                    │  classifier · CBS · PTP clock   │            │
        │                                    └───┬───────┬────────┬─────────┬──┘            │
        │           config (o_*) ────────────────┘       │        │         │  status (i_*) │
        │                                                 │        │         └───────────┐   │
        │   axi_dma (eth) ─ m_axis_tx ─►┌───────────────┐ │        │ ┌──────────────┐    │   │
        │                               │ traffic_      │ │        │ │ ptp_ts_top   │    │   │
        │                               │ controller_   │◄┘  CBS/  └►│ (TX + RX     │    │   │
        │                               │ 802_1q        │  classifier│  timestamp)  │    │   │
        │                               │ (classify →   │           │              │    │   │
        │                               │  N FIFOs →    │─ shaped ─► │  ─► MAC ─► RGMII PHY │
        │                               │  CBS arbiter) │   AXIS     │              │    │   │
        │                               └───────────────┘           │  RGMII ─► MAC ┘    │   │
        │   axi_dma (eth) ◄─ s_axis_rx ─────────────────────────────┤ (RX timestamp)     │   │
        │   axi_dma (ts)  ◄─ s_axis_ts_metadata ────────────────────┘  metadata AXIS     │   │
        │                                                                                │   │
        │   eth_event_counter (RMON) ── counts ── i_stats ─►(milan_csr) ─ stats readback │   │
        └────────────────────────────────────────────────────────────────────────────────┘
```

`milan_csr` is **integrated** in `milan_top` (2026-07): its `o_*` config drives
the MAC, classifier, CBS and PHC, and `i_*` status/events flow back to the PS
interrupt. The AXI4-Lite CSR master and its interrupt are brought out of the
block design via `M_AXI_CSR` / `irq_csr` in `bd/milan-dma.tcl` (and mirrored in
the generated `milan_dma_wrapper.v`); regenerating the BD in Vivado finalises the
physical connection. The datapath blocks and the two AXI-DMA engines exist today.

## 3. Datapath (exists today, see `hdl/common/milan_top.sv`)

**TX:** `axi_dma(eth)` → `traffic_controller_802_1q` (classify → per-queue FIFOs →
CBS arbiter) → `ptp_ts_top` (TX timestamp capture) → `eth_mac_1g_rgmii_fifo` →
RGMII PHY.

**RX:** RGMII PHY → `eth_mac_1g_rgmii_fifo` → `ptp_ts_top` (RX timestamp capture)
→ `axi_dma(eth)` → DDR.

**Timestamp metadata:** `ptp_ts_top` emits `{direction, seq_id, timestamp}`
records on a separate AXIS stream → `axi_dma(ts_metadata)` → DDR, for the driver
to correlate with skbs.

## 4. Control plane (the new `milan_csr`)

Everything the driver configures flows through one AXI4-Lite slave on
`M_AXI_GP0` at (suggested) `0x43C0_0000` / 64 KB. It replaces the previous state
where every knob was a compile-time parameter or a tied constant. Register
groups and fields are the ABI in [`REGISTER_MAP.md`](REGISTER_MAP.md); the RTL is
[`../hdl/csr/milan_csr.sv`](../hdl/csr/milan_csr.sv) (documented, TerosHDL
syntax) with a module page at [`../hdl/csr/doc/milan_csr.md`](../hdl/csr/doc/milan_csr.md).

* **Outputs (`o_*`)** carry configuration to the datapath (MAC enables/IFG/
  station-address, classifier PCP→TC map, per-queue CBS idle/hi/lo/enable, PTP
  increment/offset/commands).
* **Inputs (`i_*`)** bring status back (link/speed/duplex, RMON counters, live
  PTP TOD, event pulses).
* **Command strobes** (`o_ptp_cmd_*`, `o_stats_*`) are single-cycle pulses used
  as *apply* signals.
* **Interrupt** `o_irq = |(IRQ_STATUS & IRQ_MASK)` → widen `IRQ_F2P`.

## 5. Clock domains & CDC

| Domain | Freq | Covers |
|--------|------|--------|
| `axis_clk` | 100 MHz | AXIS datapath, DMA, **CSR block**, classifier, CBS |
| `gtx_clk`  | 125 MHz | MAC TX serialiser, **PTP timestamp counter** |
| `rgmii_rx_clk` | 125 MHz (from PHY) | MAC RX |

`milan_csr` is entirely in `axis_clk`. The PTP fields it produces
(`o_ptp_incr/adj/tod_wr/offset` + `o_ptp_cmd_*`) are consumed in `gtx_clk`;
`ptp_csr_sync` performs the crossing (2-FF vector sync for the quasi-static rate
config, toggle-synchronised apply strobes with payload capture for settime/
adjtime, and a toggle-synchronised return path for the gettime snapshot),
satisfying `REQ-CSR-03`. Pure-`axis_clk` fields (MAC/classifier/CBS) stay local  - 
no CDC needed. The PHC (`timestamp_counter`) should be clocked from a fixed
125 MHz source rather than the speed-switched `gtx_clk` (`REQ-PTP-07`).

## 6. HDL ↔ software mapping

| Concern | HDL | Driver (`../kl-linux-drivers`) | Device tree |
|---------|-----|-------------------------------|-------------|
| Bind / probe | `milan_csr` ID/CAP | `of_match` `kl,dma-ether-0.9`, read CAP | `compatible`, `reg` = CSR + DMA |
| Datapath | 2× `axi_dma` | dmaengine/ring + NAPI, N queues | `dmas`/`interrupts` |
| PHC | PTP regs (0x500) | `ptp_clock_info` adjfine/adjtime/gettime |  -  |
| HW timestamp | ts-metadata AXIS + IRQ | `SIOCSHWTSTAMP`, `skb_hwtstamps` | ts interrupt |
| CBS | CBS regs (0x400) | `ndo_setup_tc(CBS/mqprio)` | tc mapping |
| Classifier | classifier regs (0x300) | mqprio TC map |  -  |
| MAC/PHY | MAC regs (0x100) + MDIO | phylib `adjust_link`, `ndo_set_rx_mode` | `phy-handle`, `mdio` subnode |
| Stats | RMON regs (0x200) | `ethtool -S` |  -  |

The device tree is produced by the generator in `../fpga-ps-tools` (reusing the
Xilinx `device-tree-xlnx` dtg) overlaid with the `kl,dma-ether` node
(`REQ-DT-02`).

## 7. Verification

Runnable, self-checking [Verilator](https://verilator.org) harnesses under
`tb/verilator/` (no Xilinx tools needed)  -  see
[`../tb/verilator/README.md`](../tb/verilator/README.md):

* **`cbs/`**  -  802.1Qav credit-based shaper (runtime config) vs a cycle-accurate
  fixed-point replica **and** an ideal continuous model (87 k checks).
* **`shaper_core/`**  -  multi-queue CBS arbiter vs an independent grant model
  (`REQ-VER-02`, 61 k checks).
* **`cls/`**  -  `traffic_class_map` PCP→queue classification vs a reference
  (`REQ-VER-03`, 200 k random configs).
* **`ptp/`**  -  `timestamp_counter` PHC (adjfine/adjtime/settime/gettime) vs a
  128-bit accumulator model (201 k checks).
* **`csr/`**  -  `milan_csr` AXI4-Lite: reset values, RW, W1C IRQ, strobes,
  snapshots, output wiring (44 checks).

The integrating modules (`milan_top`, `traffic_classifier`, `ptp_ts_top`)
instantiate Xilinx XPM/MAC primitives and are validated by Vivado elaboration;
their standards logic is factored into the units above. Legacy Vivado/xsim
testbenches live in `tb/utests` and `tb/itests` (the old CBS/shaper/classifier
unit tests there are superseded by the Verilator harnesses  -  see
`tb/utests/802_1q_traffic_shaper/README.md`).

## 8. Where to change things (maintainability)

| To change… | Edit… | Then… |
|------------|-------|-------|
| A register offset / new field | [`hdl/csr/milan_csr.sv`](../hdl/csr/milan_csr.sv) offset block + read/write decode | update [`REGISTER_MAP.md`](REGISTER_MAP.md) + add a `ck()` in `tb/verilator/csr/sim_main.cpp` |
| Number of HW queues | `NUM_QUEUES` (milan_csr) + `NUMBER_OF_QUEUES` (`ethernet_packet_pkg.sv`) | re-run both harnesses; check `axi_mcdma` channel count |
| CBS default slopes | `CBS_*_RST` in `milan_csr.sv` **and** `IDLE_SLOPE_*`/`calc_*_credit` in `ethernet_packet_pkg.sv` | keep Σ idleSlope ≤ 75 % (`REQ-CBS-03`); re-run `tb/verilator/cbs` |
| PCP→TC classification | `traffic_class_map.sv` decode (fed by `o_cls_*`) | re-run `tb/verilator/cls` |
| PTP rate/offset | `timestamp_counter.sv` (accumulator) + `ptp_csr_sync.sv` CDC | re-run `tb/verilator/ptp`; driver `ptp_clock_info` |
| Add an IRQ source | `milan_csr` IRQ_STATUS/MASK + `bd/milan-dma.tcl` `IRQ_F2P`/`ilconcat` |  -  |

**Conventions:** SystemVerilog with `` `default_nettype none ``, Doxygen/TerosHDL
`//!` comments on every generic/port/signal, named `always_*` processes with a
preceding `//!` description (so TerosHDL generates the module `doc/*.md`).
Reset defaults are chosen so the block powers up compatible with today's tied
constants; software reprograms everything at bring-up.
