# Milan TSN FPGA - architecture & developer guide

The map a new developer should read first: the datapath, the control plane,
the clock domains, how the HDL maps to the Linux driver and device tree, and
**where to change things**. For the deep-dive companions:
[FULL_FPGA_SOLUTION.md](FULL_FPGA_SOLUTION.md) (build/run/roadmap),
[../fpga/FPGA_DESIGN.md](../fpga/FPGA_DESIGN.md) (every RTL module),
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md) (the ABI),
[`REQUIREMENTS.md`](../../REQUIREMENTS.md) (normative what/why).

The project has **two host variants around one datapath**:

* **Fully-FPGA softcore (primary):** LiteX RISC-V SoC on the Alinx AX7101
  (Artix-7) - CPU, DDR3, ring-DMA engines, LiteEth GMII MAC and the
  `milan_datapath` wrapper, all in fabric. This is where development and the
  performance campaigns happen. ([../litex/LITEX_SOC.md](../litex/LITEX_SOC.md))
* **Zynq-7020 PS (legacy variant):** `milan_top` + Vivado block design
  (`bd/milan-dma.tcl`: PS7 + AXI-DMA + interconnect), RGMII MAC in fabric.
  Kept working, but not the main line. (§9)

---

## 1. Repository layout

```
milan-fpga/
├─ README.md                 landing page + quick jumps
├─ REQUIREMENTS.md           normative requirements + 802.1 gap analysis
├─ TODO.md                   phased task list (partly Zynq-era)
├─ CHANGELOG.md              the measured per-lever performance ledger
├─ docs/                     ← the documentation tree (see docs/README.md)
│  ├─ overview/  integration/  fpga/  litex/  testing/  limitations/
│  ├─ reference/             REGISTER_MAP, FR/NFR, Milan v1.2 matrix
│  └─ findings/              dated bug post-mortems + perf campaigns
├─ hdl/
│  ├─ common/                milan_datapath + milan_top wrappers, TCAM,
│  │                         RX filter, CDC primitives, AXIS iface, pkgs
│  ├─ csr/                   milan_csr.sv ← memory-mapped control plane
│  ├─ 802_1q_traffic_shaper/ classifier + queues + CBS + arbiter
│  ├─ ptp_timestamp/         PHC counter + ptp_csr_sync CDC + TX/RX stampers
│  ├─ eth_event_counter/     RMON event counters
│  ├─ 1722/  adp/            AVTP parsers · ADP advertiser/parser
├─ sw/
│  ├─ litex/                 the LiteX SoC (milan_soc.py), sims, patches, tools
│  ├─ driver/                kl-eth driver contract (source in sibling repo)
│  └─ dts/                   device-tree generator (per-host overlays)
├─ third_party/verilog-axis  vendored AXIS cores (submodule - init required!)
├─ bd/ constraints/          Zynq-variant block design + XDC
├─ syn/yosys/                open-toolchain portability check
└─ tb/
   ├─ verilator/             17 self-checking harnesses (the live regression)
   ├─ utests/ itests/        legacy Vivado/xsim testbenches
   └─ avtp_packet_gen_sv/    AVTP stimulus classes (Questa)
```

## 2. System block diagram (fully-FPGA softcore)

```
   ┌─────────────────────────── Artix-7 fabric (LiteX SoC) ───────────────────────────┐
   │                                                                                   │
   │  VexiiRiscv ×2 (or NaxRiscv)   L2   DDR3 ctrl (LiteDRAM)   QSPI   UART   PLIC     │
   │        │ CPU bus                        │ dma_bus (coherent)                      │
   │        ├────────────────┬───────────────┴───────────────┐                         │
   │   AXI-Lite CSR      LiteX CSRs                  ring-DMA engines                  │
   │   @0x9000_0000     (0xf000_xxxx:                 RingDMAReader (TX, AXI bursts)   │
   │        │            DMA rings, telemetry)        RingDMAWriter (RX, always-ready) │
   │        ▼                                         WishboneDMAWriter (TS)           │
   │  ┌─────────────────────── milan_datapath (hdl/, vendor-neutral) ───────────────┐  │
   │  │ milan_csr ── config/status/IRQ to every block below                         │  │
   │  │ TX: s_axis_tx ─► classify ─► 4 queues ─► CBS ─► PTP-TX ─► ADP arb ─► mac_tx │  │
   │  │ RX: mac_rx ─► PTP-RX ─► TCAM dest-MAC filter ─► m_axis_rx                   │  │
   │  │ TS: {dir, seq_id, timestamp} records ─► m_axis_ts                           │  │
   │  └──────────────────────────────────────────────────────────────────────────┬─┘  │
   │                                                     MilanMAC (LiteEth GMII) │     │
   └──────────────────────────────────────────────────────────────────────────── │ ────┘
                                                                        RTL8211E PHY (GMII)
```

The same `milan_datapath` is what the Zynq variant, the Verilator harnesses
(`tb/verilator/milan_dp`), the SoC sim (`milan_sim.py`) and the Yosys
portability check all build - one boundary, five consumers. Its port-level
contract is [../integration/INTEGRATION_GUIDE.md](../integration/INTEGRATION_GUIDE.md).

## 3. Datapath

**TX:** DMA reader → `traffic_controller_802_1q` (classify → per-queue FIFOs
→ CBS arbiter) → `ptp_ts_top` (TX timestamp capture) → `adp_tx_arbiter`
(merges ADP advertisements) → MAC.

**RX:** MAC → `ptp_ts_top` (RX timestamp capture) → `rx_mac_filter`
(TCAM dest-MAC) → DMA writer.

**Timestamp metadata:** `ptp_ts_top` emits `{direction, seq_id, timestamp}`
records on a separate AXIS stream → TS DMA → DRAM, for the driver to
correlate with skbs.

Stage-by-stage prose with the DMA internals:
[../fpga/PIPELINE_STAGES.md](../fpga/PIPELINE_STAGES.md); per-stage counters
to watch it live: [../fpga/pipeline-telemetry.md](../fpga/pipeline-telemetry.md).

## 4. Control plane (`milan_csr`)

Everything the driver configures flows through one AXI4-Lite slave - a 64 KB
window at `0x9000_0000` on the softcore (`0x43C0_0000` on Zynq; only the
base differs, the offsets are the ABI in
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md)).

* **Outputs (`o_*`)** carry configuration to the datapath (MAC enables/IFG/
  station address, classifier PCP→TC map, per-queue CBS slopes/enables, PTP
  increment/offset/commands, ADP entity model, TCAM entries).
* **Inputs (`i_*`)** bring status back (link/speed/duplex, RMON counters,
  live PTP TOD, event pulses).
* **Command strobes** (`o_ptp_cmd_*`, `o_stats_*`) are single-cycle *apply*
  pulses.
* **Interrupt** `o_irq = |(IRQ_STATUS & IRQ_MASK)` → one PLIC line on the
  softcore (EventManager), `IRQ_F2P` on Zynq.

The ring-DMA engines have their own LiteX-generated CSR space
(`0xf000_xxxx`) - documented in the DMA section of the register map.

## 5. Clock domains & CDC

| Domain | Freq | Covers |
|--------|------|--------|
| `sys` | 100 MHz | CPU, DDR3, DMA engines, MAC core (softcore build) |
| `cd_milan` (= `axis_clk`) | 50 MHz in the deployed build (`--milan-clk-freq`); 100 MHz when not split | the whole `milan_datapath`, incl. the CSR block |
| `gtx_clk` | 125 MHz | PTP timestamp counter + MAC-side capture (tied to `axis_clk` on the softcore build; separate on Zynq) |
| PHY RX clock | 125 MHz | inside the MAC only |

Crossings: `sys ⇄ cd_milan` at the boundary (AXI-Lite async-FIFO CDC, AXIS
stream CDCs, IRQ 2-FF - all generated by `add_milan_datapath()`);
`axis_clk ⇄ gtx_clk` inside the datapath (`ptp_csr_sync` for CSR↔PHC,
`cdc_pulse`/`cdc_handshake` in `ptp_ts_core`). Full inventory:
[../fpga/FPGA_DESIGN.md](../fpga/FPGA_DESIGN.md) §3; constraint rules when
porting: [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §4.5.

## 6. HDL ↔ software mapping

| Concern | HDL / gateware | Driver (`../kl-linux-drivers` kl-eth) | Device tree |
|---------|----------------|----------------------------------------|-------------|
| Bind / probe | `milan_csr` ID/CAP | `of_match` `kl,dma-ether-0.9`, read CAP | `compatible`, `reg` = csr + dma-tx/rx/ts |
| Datapath | ring-DMA engines (`milan_soc.py`) | ring + NAPI | `reg` DMA windows, `interrupt-names` tx-dma/rx-dma/ts-dma/csr |
| PHC | PTP regs (0x500) | `ptp_clock_info` adjfine/adjtime/gettime | - |
| HW timestamp | ts-metadata AXIS + IRQ | `SIOCSHWTSTAMP`, `skb_hwtstamps` | ts interrupt |
| CBS | CBS regs (0x400) | `ndo_setup_tc(CBS/mqprio)` | tc mapping |
| Classifier | classifier regs (0x300) | mqprio TC map | - |
| MAC/PHY | MAC regs (0x100) | phylib `adjust_link`, `ndo_set_rx_mode` | `phy-handle` |
| Stats | RMON regs (0x200) | `ethtool -S` | - |
| ADP | ADP regs (0x600) | entity model programming | - |
| RX filter | TCAM regs (0x700) | dest-MAC filtering | - |

The device tree is **generated** per host by `sw/dts/milan_dt.py` from the
build's `csr.json` (LiteX) or the IR JSON (Zynq) - see
[`sw/dts/README.md`](../../sw/dts/README.md). Driver-side contract and
caveats: [`sw/driver/README.md`](../../sw/driver/README.md).

## 7. Verification

Six layers, one map: [../testing/TESTING.md](../testing/TESTING.md).
Quick version: 17 self-checking Verilator harnesses
([`tb/verilator/README.md`](../../tb/verilator/README.md)) cover every RTL
block through the whole `milan_datapath` wrapper; Migen sims cover the DMA
engines; `milan_sim.py` boots the SoC in Verilator; `syn/yosys` proves
device portability (18 tops, generic + ECP5); the legacy xsim TBs remain
for waveform work; silicon procedures close the loop.

## 8. Where to change things (maintainability)

| To change… | Edit… | Then… |
|------------|-------|-------|
| A register offset / new field | [`hdl/csr/milan_csr.sv`](../../hdl/csr/milan_csr.sv) offset block + decode | update [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) + add a check in `tb/verilator/csr/sim_main.cpp` (same commit) |
| Number of HW queues | `NUM_QUEUES` (milan_csr) + `NUMBER_OF_QUEUES` (`ethernet_packet_pkg.sv`) | re-run `csr`, `queues`, `datapath` harnesses; ring/DMA queue count in `milan_soc.py` |
| CBS default slopes | `CBS_*_RST` in `milan_csr.sv` **and** `IDLE_SLOPE_*`/`calc_*_credit` in `ethernet_packet_pkg.sv` | keep Σ idleSlope ≤ 75 % (`REQ-CBS-03`); re-run `tb/verilator/cbs`; remember the [reset-defaults shaping bug](../findings/CBS_DEFAULT_SHAPING_BUG.md) |
| PCP→TC classification | `traffic_class_map.sv` decode | re-run `tb/verilator/cls` |
| PTP rate/offset | `timestamp_counter.sv` + `ptp_csr_sync.sv` | re-run `ptp`, `ptp_sync`; driver `ptp_clock_info` |
| DMA/BD format | `milan_soc.py` engines | `sw/litex/test_*.py` sims + the driver in lockstep (see the [pairing hazards](../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md)) |
| Add an IRQ source | `milan_csr` IRQ_STATUS/MASK (+ EventManager wiring in `milan_soc.py`, or `bd/milan-dma.tcl` `IRQ_F2P` on Zynq) | DT regeneration |
| Board pins / new board | `sw/litex/platforms/` | [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) |

**Conventions:** SystemVerilog with `` `default_nettype none ``,
TerosHDL/Doxygen `//!` comments on every generic/port/signal, named
`always_*` processes. Register offsets and reset values are defined once in
the RTL, documented in REGISTER_MAP.md, and asserted equal by the CSR
harness. Every DUT change ships with its harness update in the same commit.

## 9. The Zynq-7020 variant (legacy)

`milan_top.sv` wraps the same datapath plus the verilog-ethernet
`eth_mac_1g_rgmii_fifo` MAC (source vendored externally) and hangs off the
PS7 via `milan_dma_wrapper.v` + the `bd/milan-dma.tcl` block design (PS7,
2× AXI-DMA, `clk_wiz`, `smartconnect`; CSR at `0x43C0_0000`, four GIC IRQ
lines). Constraints in `constraints/*.xdc`. `REQUIREMENTS.md` and parts of
`TODO.md` were written in this era - where they talk about `0x43C0_0000`,
`IRQ_F2P` or `device-tree-xlnx`, they describe this variant only. The
migration story from PS to softcore is
[../integration/FULLY_FPGA_RISCV_MIGRATION.md](../integration/FULLY_FPGA_RISCV_MIGRATION.md).
