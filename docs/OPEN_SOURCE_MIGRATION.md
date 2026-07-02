# De-Xilinx plan — replace XPM/vendor IP with Alex Forencich open cores

Goal: remove every **Xilinx-specific / licensed** primitive from the RTL and
replace it with permissively-licensed (MIT) open cores from
**[github.com/alexforencich](https://github.com/alexforencich)** (and the related
[corundum](https://github.com/corundum/corundum) project). The MAC is *already*
one of these (`eth_mac_1g_rgmii_fifo` from **verilog-ethernet**), so this extends
an established pattern.

## Why do this (the payoff)

1. **Vendor-neutral, open, license-free RTL** — nothing but SelectIO fabric cells
   (which are free) is Xilinx-specific; the design builds on Artix-7, LiteX, or any
   FPGA.
2. **The whole datapath becomes Verilator-simulatable.** Today the leaf blocks are
   unit-tested but the integrating modules (`traffic_classifier`, `traffic_queues`,
   `ptp_ts_top`, `ptp_ts_core`, `milan_top`) **cannot** run in Verilator because they
   instantiate `xpm_fifo_axis` / `axis_switch_*` / `xpm_cdc_*`. Forencich's cores are
   plain synthesizable Verilog with Verilator-friendly sim models — replacing the XPM
   makes the **end-to-end classify→CBS→PTP→MAC path cycle-checkable**, not just the
   leaves.
3. Aligns with the fully-FPGA RISC-V plan ([`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md));
   the PS-replacement there reuses the same core families.

---

## 1. Inventory — what is Xilinx today

| # | Primitive | Instances (file:line) | Role |
|---|-----------|------------------------|------|
| X1 | `xpm_fifo_axis` | `traffic_classifier.sv:73`, `traffic_queues.sv:140`, `ptp_ts_top.sv:281/308/363` (5×) | AXIS FIFOs (buffering, some same-clock, some CDC) |
| X2 | `axis_switch_1in_4out_64b_tdest_2b_tlast` | `traffic_queues.sv:119` | 1→4 AXIS demux by `tdest` (per-queue) |
| X3 | `axis_switch_4in_1out_64b_tlast` | `traffic_queues.sv:174` | 4→1 AXIS mux (queue egress) |
| X4 | `xpm_cdc_pulse` | `ptp_ts_core.sv:133` | SOP pulse CDC (logic→gtx clock) |
| X5 | `xpm_cdc_handshake` | `ptp_ts_core.sv:171` | timestamp value CDC (gtx→logic) |
| X6 | `IOBUF` | `milan_dma_wrapper.v:197` | MDIO bidirectional pad |
| X7 | MAC IO style: `TARGET("XILINX")`, `IODDR_STYLE("IODDR")`, `CLOCK_INPUT_STYLE("BUFR")` | `milan_top.sv:545-547` | RGMII DDR I/O cells (SelectIO — *free*, not licensed) |
| X8 | PS block design: `processing_system7`, `axi_dma`, `smartconnect`, `clk_wiz`, `proc_sys_reset` | `bd/milan-dma.tcl` | host: CPU/DDR/DMA/interconnect/clocks/reset |

X1–X5 block Verilator; X6 is trivial; X7 is free fabric (only matters off-Xilinx);
X8 is the host (already addressed by the RISC-V plan).

---

## 2. Forencich core catalog (the list you asked for)

All **MIT-licensed**. Vendor as git submodules under `third_party/`.

### verilog-axis — AXI-Stream infrastructure  (`github.com/alexforencich/verilog-axis`)
- **FIFOs:** `axis_fifo` (sync), `axis_async_fifo` (dual-clock / **CDC**),
  `axis_fifo_adapter`, `axis_async_fifo_adapter`, `axis_srl_fifo`,
  `axis_pipeline_fifo`.
- **Interconnect / switch:** `axis_switch` (M×N, `tdest`-routed), `axis_crosspoint`,
  `axis_mux` (N→1), `axis_demux` (1→N), `axis_arb_mux` (arbitrated N→1),
  `axis_broadcast` (1→N), `axis_ram_switch`.
- **Adapters / registers:** `axis_adapter` (data-width convert), `axis_register` /
  `axis_pipeline_register` (skid/timing), `axis_frame_length_adjust`,
  `axis_rate_limit`, `axis_stat_counter`, `axis_tap`.
- Helpers: `arbiter`, `priority_encoder`.

### verilog-axi — AXI4 / AXI-Lite infrastructure  (`github.com/alexforencich/verilog-axi`)
- **DMA:** `axi_dma` (`axi_dma_rd` + `axi_dma_wr`, memory↔AXIS, descriptor-driven),
  `axi_dma_desc_mux`, `axi_cdma` (mem↔mem), `axi_vfifo` (virtual FIFO in DRAM).
- **Interconnect:** `axi_crossbar` (AXI4), `axil_crossbar` (AXI-Lite),
  `axi_interconnect`, `axil_interconnect`.
- **Adapters / registers:** `axi_adapter`, `axi_axil_adapter`, `axil_adapter`,
  `axi_register`, `axil_register`, `axil_cdc` (**AXI-Lite CDC**), `axi_fifo`.
- **RAM:** `axi_ram`, `axil_ram`, `axi_dp_ram` (boot ROM / scratch).

### verilog-ethernet — MAC / PHY / PTP  (`github.com/alexforencich/verilog-ethernet`)  *(already used)*
- MAC (in use): `eth_mac_1g_rgmii_fifo`; PHY IF: `rgmii_phy_if`, `ssio_ddr_in/out`,
  `iddr`/`oddr` (target-abstracted DDR cells — replace X7 via `TARGET`).
- **MDIO master:** `mdio_master` (drives `mdc`/`mdio_i/o/t` — replaces the PS GEM1
  MDIO + `IOBUF` handling, X6).
- **PTP:** `ptp_clock` (HW PHC), **`ptp_clock_cdc`** (timestamp CDC — replaces X5),
  `ptp_perout` (1PPS/perout), `ptp_ts_extract`.
- Frame glue: `eth_axis_rx/tx`, `axis_gmii_rx/tx`; CDC helpers `sync_reset`,
  `sync_signal` (replace `proc_sys_reset` / level CDC).

### corundum — full open NIC  (`github.com/corundum/corundum`)  *(optional, for scale-out)*
- High-performance scatter-gather DMA (`dma_if_*`, `dma_client_axis_*`), queue
  management. Relevant only if the DMA needs to scale far beyond the 1 G single-queue
  baseline (ties to NFR-SCUP/SCOUT). Overkill for the baseline.

> Exact module names should be confirmed against the pinned submodule revision — the
> repos evolve; the families above are stable.

---

## 3. Replacement mapping

| Xilinx (X#) | Forencich replacement | Notes |
|-------------|-----------------------|-------|
| X1 `xpm_fifo_axis` (same-clock) | `verilog-axis/axis_fifo` | depth/width params map directly; drop the XPM `USE_ADV_FEATURES` string |
| X1 `xpm_fifo_axis` (dual-clock / CDC) | `verilog-axis/axis_async_fifo` | for the ptp_ts_top TX/RX buffers that cross clock domains |
| X2 1→4 `axis_switch` (tdest) | `verilog-axis/axis_demux` (or `axis_switch` M=1,N=4) | route by `tdest`; identical function |
| X3 4→1 `axis_switch` | `verilog-axis/axis_arb_mux` | round-robin/priority egress mux (fairer than a plain switch) |
| X4 `xpm_cdc_pulse` | in-repo toggle-sync (template: `ptp_csr_sync.sv`) | tiny; already have the pattern in this repo |
| X5 `xpm_cdc_handshake` (timestamp) | `verilog-ethernet/ptp_clock_cdc` **or** `verilog-axis/axis_async_fifo` | ptp_clock_cdc is purpose-built for PTP timestamps |
| X6 `IOBUF` (MDIO) | inferred tristate + `verilog-ethernet/mdio_master` | `assign mdio = t ? 1'bz : o; assign i = mdio;` — Vivado infers IOBUF; Verilator models it |
| X7 RGMII IO style | MAC `TARGET("GENERIC")` for sim / keep `"XILINX"` for the Artix build | SelectIO is *free* on Xilinx; `GENERIC`/`SIM` makes it Verilatable |
| X8 PS (CPU/DDR/DMA/xbar/clk/rst) | **LiteX+NaxRiscv** (primary) *or* Vivado-native: `verilog-axi/axi_dma` + `axi_crossbar`/`axil_crossbar` + MIG (DDR) + NaxRiscv + `sync_reset` | see [`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md) §A |

---

## 4. Migration plan (phased, each phase Verilator-verified)

### Track 1 — datapath de-Xilinx (independent of the host decision; do first)
Highest value: unblocks end-to-end Verilator simulation of the TSN datapath.

1. **T1.1 — vendor the cores.** Add `verilog-axis`, `verilog-axi`, `verilog-ethernet`
   as git submodules under `third_party/`; add their `rtl/` to the Verilator/Vivado
   source lists. *(no RTL change)*
2. **T1.2 — AXIS FIFOs (X1).** Replace the 5 `xpm_fifo_axis` with `axis_fifo`
   (same-clock) / `axis_async_fifo` (CDC) in `traffic_classifier`, `traffic_queues`,
   `ptp_ts_top`. **Verify:** each host module now Verilates → add/extend a harness;
   the existing `cbs`/`cls`/`ptp` leaf tests stay green.
3. **T1.3 — AXIS switch/mux (X2,X3).** Replace the generated `axis_switch_*` in
   `traffic_queues` with `axis_demux` (1→4 by tdest) + `axis_arb_mux` (4→1).
   **Verify:** `traffic_queues` now Verilates → new `tb/verilator/queues` harness
   (per-queue routing + egress arbitration, mirrors the `shaper_core` style).
4. **T1.4 — PTP CDC (X4,X5).** Replace `xpm_cdc_pulse`/`xpm_cdc_handshake` in
   `ptp_ts_core` with the toggle-sync pattern / `ptp_clock_cdc`. **Verify:**
   `ptp_ts_core` now Verilates → extend the `ptp` harness across the CDC.
5. **T1.5 — the big win.** With T1.2–T1.4 done, `traffic_controller_802_1q`,
   `ptp_ts_top`, and the TSN half of `milan_top` are fully Verilatable → add an
   **end-to-end datapath harness** (`tb/verilator/datapath`): inject frames, check
   classification + CBS shaping + PTP timestamps + ADP insertion at the MAC boundary.

### Track 2 — I/O + host de-Xilinx
6. **T2.1 — MDIO (X6,X7).** Replace `IOBUF` with inferred tristate; instantiate
   `verilog-ethernet/mdio_master` as the fabric MDIO master (also closes REQ-MAC-08).
   Set MAC `TARGET("GENERIC")` for sim builds, `"XILINX"` for the Artix bitstream.
7. **T2.2 — host (X8).** Per [`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md):
   LiteX+NaxRiscv (primary), or Vivado-native with `verilog-axi` `axi_dma` +
   `axi_crossbar`/`axil_crossbar` + MIG + NaxRiscv + `sync_reset`. The AXI-Lite CSR
   bus reaches `milan_csr` through `axil_crossbar`/`axil_register`.

### Ordering & risk
- Track 1 is **self-contained and low-risk** (leaf-for-leaf swaps with immediate
  Verilator proof); do it first — it also makes every later change testable.
- Track 2.2 is the big one but is already the subject of the RISC-V migration plan.
- **RGMII IO (X7)** is the only genuinely device-tied piece on a Xilinx target, and it
  is *free* fabric (not licensed IP); `TARGET` abstracts it for sim/other vendors.

## 5. Licensing & vendoring
All Forencich cores + corundum are **MIT** — compatible with this repo's CERN-OHL-W.
Vendor as pinned submodules (`third_party/verilog-axis`, `-axi`, `-ethernet`); do not
copy files in, so upstream fixes flow via submodule bumps. Keep a `THIRD_PARTY.md`
listing each submodule, its commit, and which of our modules use it.

## 6. Definition of done
- No `xpm_*`, no generated `axis_switch_*` IP, no `IOBUF` in `hdl/`.
- `milan_top` (TSN datapath) **elaborates and simulates in Verilator** end-to-end.
- All existing harnesses green + new `queues` / `datapath` harnesses green.
- The only remaining vendor primitives are the free Xilinx SelectIO RGMII cells,
  gated behind the MAC `TARGET` param (absent in `GENERIC`/`SIM` builds).
