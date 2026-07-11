# De-Xilinx plan  -  replace XPM/vendor IP with Alex Forencich open cores

Goal: remove every **Xilinx-specific / licensed** primitive from the RTL and
replace it with permissively-licensed (MIT) open cores from
**[github.com/alexforencich](https://github.com/alexforencich)** (and the related
[corundum](https://github.com/corundum/corundum) project). The MAC is *already*
one of these (`eth_mac_1g_rgmii_fifo` from **verilog-ethernet**), so this extends
an established pattern.

## Why do this (the payoff)

1. **Vendor-neutral, open, license-free RTL**  -  nothing but SelectIO fabric cells
   (which are free) is Xilinx-specific; the design builds on Artix-7, LiteX, or any
   FPGA.
2. **The whole datapath becomes Verilator-simulatable.** Today the leaf blocks are
   unit-tested but the integrating modules (`traffic_classifier`, `traffic_queues`,
   `ptp_ts_top`, `ptp_ts_core`, `milan_top`) **cannot** run in Verilator because they
   instantiate `xpm_fifo_axis` / `axis_switch_*` / `xpm_cdc_*`. Forencich's cores are
   plain synthesizable Verilog with Verilator-friendly sim models  -  replacing the XPM
   makes the **end-to-end classify→CBS→PTP→MAC path cycle-checkable**, not just the
   leaves.
3. Aligns with the fully-FPGA RISC-V plan ([`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md));
   the PS-replacement there reuses the same core families.

---

## 1. Inventory  -  what is Xilinx today

| # | Primitive | Instances (file:line) | Role |
|---|-----------|------------------------|------|
| X1 | `xpm_fifo_axis` | `traffic_classifier.sv:73`, `traffic_queues.sv:140`, `ptp_ts_top.sv:281/308/363` (5×) | AXIS FIFOs (buffering, some same-clock, some CDC) |
| X2 | `axis_switch_1in_4out_64b_tdest_2b_tlast` | `traffic_queues.sv:119` | 1→4 AXIS demux by `tdest` (per-queue) |
| X3 | `axis_switch_4in_1out_64b_tlast` | `traffic_queues.sv:174` | 4→1 AXIS mux (queue egress) |
| X4 | `xpm_cdc_pulse` | `ptp_ts_core.sv:133` | SOP pulse CDC (logic→gtx clock) |
| X5 | `xpm_cdc_handshake` | `ptp_ts_core.sv:171` | timestamp value CDC (gtx→logic) |
| X6 | `IOBUF` | `milan_dma_wrapper.v:197` | MDIO bidirectional pad |
| X7 | MAC IO style: `TARGET("XILINX")`, `IODDR_STYLE("IODDR")`, `CLOCK_INPUT_STYLE("BUFR")` | `milan_top.sv:545-547` | RGMII DDR I/O cells (SelectIO  -  *free*, not licensed) |
| X8 | PS block design: `processing_system7`, `axi_dma`, `smartconnect`, `clk_wiz`, `proc_sys_reset` | `bd/milan-dma.tcl` | host: CPU/DDR/DMA/interconnect/clocks/reset |

X1–X5 block Verilator; X6 is trivial; X7 is free fabric (only matters off-Xilinx);
X8 is the host (already addressed by the RISC-V plan).

---

## 2. Forencich core catalog (the list you asked for)

All **MIT-licensed**. Vendor as git submodules under `third_party/`.

### verilog-axis  -  AXI-Stream infrastructure  (`github.com/alexforencich/verilog-axis`)
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

### verilog-axi  -  AXI4 / AXI-Lite infrastructure  (`github.com/alexforencich/verilog-axi`)
- **DMA:** `axi_dma` (`axi_dma_rd` + `axi_dma_wr`, memory↔AXIS, descriptor-driven),
  `axi_dma_desc_mux`, `axi_cdma` (mem↔mem), `axi_vfifo` (virtual FIFO in DRAM).
- **Interconnect:** `axi_crossbar` (AXI4), `axil_crossbar` (AXI-Lite),
  `axi_interconnect`, `axil_interconnect`.
- **Adapters / registers:** `axi_adapter`, `axi_axil_adapter`, `axil_adapter`,
  `axi_register`, `axil_register`, `axil_cdc` (**AXI-Lite CDC**), `axi_fifo`.
- **RAM:** `axi_ram`, `axil_ram`, `axi_dp_ram` (boot ROM / scratch).

### verilog-ethernet  -  MAC / PHY / PTP  (`github.com/alexforencich/verilog-ethernet`)  *(already used)*
- MAC (in use): `eth_mac_1g_rgmii_fifo`; PHY IF: `rgmii_phy_if`, `ssio_ddr_in/out`,
  `iddr`/`oddr` (target-abstracted DDR cells  -  replace X7 via `TARGET`).
- **MDIO master:** `mdio_master` (drives `mdc`/`mdio_i/o/t`  -  replaces the PS GEM1
  MDIO + `IOBUF` handling, X6).
- **PTP:** `ptp_clock` (HW PHC), **`ptp_clock_cdc`** (timestamp CDC  -  replaces X5),
  `ptp_perout` (1PPS/perout), `ptp_ts_extract`.
- Frame glue: `eth_axis_rx/tx`, `axis_gmii_rx/tx`; CDC helpers `sync_reset`,
  `sync_signal` (replace `proc_sys_reset` / level CDC).

### corundum  -  full open NIC  (`github.com/corundum/corundum`)  *(optional, for scale-out)*
- High-performance scatter-gather DMA (`dma_if_*`, `dma_client_axis_*`), queue
  management. Relevant only if the DMA needs to scale far beyond the 1 G single-queue
  baseline (ties to NFR-SCUP/SCOUT). Overkill for the baseline.

> Exact module names should be confirmed against the pinned submodule revision  -  the
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
| X6 `IOBUF` (MDIO) | inferred tristate + `verilog-ethernet/mdio_master` | `assign mdio = t ? 1'bz : o; assign i = mdio;`  -  Vivado infers IOBUF; Verilator models it |
| X7 RGMII IO style | MAC `TARGET("GENERIC")` for sim / keep `"XILINX"` for the Artix build | SelectIO is *free* on Xilinx; `GENERIC`/`SIM` makes it Verilatable |
| X8 PS (CPU/DDR/DMA/xbar/clk/rst) | **LiteX+NaxRiscv** (primary) *or* Vivado-native: `verilog-axi/axi_dma` + `axi_crossbar`/`axil_crossbar` + MIG (DDR) + NaxRiscv + `sync_reset` | see [`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md) §A |

---

## 4. Migration plan (phased, each phase Verilator-verified)

### Track 1  -  datapath de-Xilinx (independent of the host decision; do first)
Highest value: unblocks end-to-end Verilator simulation of the TSN datapath.

1. **T1.1  -  vendor the cores.** ✅ `verilog-axis` added as a submodule at
   `third_party/verilog-axis` (pinned `48ff7a7`); see [`../THIRD_PARTY.md`](../../THIRD_PARTY.md).
   *(verilog-axi / verilog-ethernet to add in T2.)*
2. **T1.2  -  AXIS FIFOs (X1).** 🟡 IN PROGRESS. All 5 are `common_clock` → `axis_fifo`.
   - ✅ `traffic_classifier`  -  swapped + **fully verified**: [`tb/verilator/classifier/`](../../tb/verilator/classifier)
     (6 checks, PASS) proves it now Verilates and the swap is lossless/byte-exact.
   - ✅ `ptp_ts_top` ×3 (tx/rx/ps ts buffers)  -  swapped; `ptp_ts_top` now parses with
     **only `xpm_cdc_*` missing** (its full harness lands with T1.4).
   - ⏳ `traffic_queues`  -  deferred to **T1.3**: it adds `tdest` + `prog_empty_axis`
     flow-control entangled with its `axis_switch`, so it is swapped there with a
     harness in the same step.
3. **T1.3  -  AXIS switch/mux (X2,X3) + the deferred FIFO.** ✅ DONE. Replaced the
   generated `axis_switch_1in_4out`/`4in_1out` in `traffic_queues` with `axis_demux`
   (1→4 by `tdest`) + `axis_arb_mux` (4→1), and the per-queue `xpm_fifo_axis` with
   `axis_fifo` (`prog_empty` → `status_depth ≤ thresh`). CBS grant suppression is
   reproduced by gating **both** the arbiter input `tvalid` **and** the FIFO `tready`
   with `queue_grant_i` (gating `tvalid` alone lets the arbiter's prefetch drain and
   discard the frame  -  caught by the harness). **Verify:** [`tb/verilator/queues/`](../../tb/verilator/queues)
   (11 checks, PASS) + `traffic_controller_802_1q` now **elaborates end-to-end** in
   Verilator (classifier + queues + CBS, no XPM left in the 802.1Q subtree).
4. **T1.4  -  PTP CDC (X4,X5).** ✅ DONE. Replaced `xpm_cdc_pulse`/`xpm_cdc_handshake`
   in `ptp_ts_core` with two open, FPGA-independent primitives:
   [`cdc_pulse.sv`](../../hdl/common/cdc_pulse.sv) (toggle synchroniser) and
   [`cdc_handshake.sv`](../../hdl/common/cdc_handshake.sv) (4-phase req/ack value
   transfer). **`hdl/` is now completely XPM-free**, and `ptp_ts_top` elaborates
   end-to-end in Verilator. **Verify:** [`tb/verilator/cdc/`](../../tb/verilator/cdc)
   (16 checks, PASS) drives two *independent* clocks (2:3) and checks pulse-count
   preservation + byte-exact value crossing with req/ack.
5. **T1.5  -  the big win.** ✅ DONE. `traffic_controller_802_1q` (classifier +
   Forencich queues + CBS shaper) is fully Verilatable → the **end-to-end datapath
   harness** [`tb/verilator/datapath/`](../../tb/verilator/datapath) (15 checks, PASS)
   injects VLAN frames and proves, through the whole pipeline: byte-exact egress,
   PCP→queue classification (identity map, exact `tdest`), all 4 queues, both
   strict-priority and CBS-shaped modes, and burst delivery. (PTP-timestamp / ADP
   insertion stages have their own harnesses  -  `ptp`, `adp`, `adp_tx`.)

### Track 2  -  I/O + host de-Xilinx
6. **T2.1  -  MDIO (X6,X7).** Replace `IOBUF` with inferred tristate; instantiate
   `verilog-ethernet/mdio_master` as the fabric MDIO master (also closes REQ-MAC-08).
   Set MAC `TARGET("GENERIC")` for sim builds, `"XILINX"` for the Artix bitstream.
7. **T2.2  -  host (X8).** Per [`FULLY_FPGA_RISCV_MIGRATION.md`](FULLY_FPGA_RISCV_MIGRATION.md):
   LiteX+NaxRiscv (primary), or Vivado-native with `verilog-axi` `axi_dma` +
   `axi_crossbar`/`axil_crossbar` + MIG + NaxRiscv + `sync_reset`. The AXI-Lite CSR
   bus reaches `milan_csr` through `axil_crossbar`/`axil_register`.

### Ordering & risk
- Track 1 is **self-contained and low-risk** (leaf-for-leaf swaps with immediate
  Verilator proof); do it first  -  it also makes every later change testable.
- Track 2.2 is the big one but is already the subject of the RISC-V migration plan.
- **RGMII IO (X7)** is the only genuinely device-tied piece on a Xilinx target, and it
  is *free* fabric (not licensed IP); `TARGET` abstracts it for sim/other vendors.

## 5. Licensing & vendoring
All Forencich cores + corundum are **MIT**  -  compatible with this repo's CERN-OHL-W.
Vendor as pinned submodules (`third_party/verilog-axis`, `-axi`, `-ethernet`); do not
copy files in, so upstream fixes flow via submodule bumps. Keep a `THIRD_PARTY.md`
listing each submodule, its commit, and which of our modules use it.

## 6. Open-toolchain synthesis check (device portability)

Being XPM-free is only useful if the RTL actually maps to *other* devices. The
[`syn/yosys/`](../../syn/yosys) flow proves it: **sv2v** converts the SystemVerilog to
Verilog-2005 and **Yosys** runs generic `synth` + `hierarchy -check` (which fails on
any leftover vendor/undefined primitive). **17/17 tops PASS** device-independent
synthesis, and `make ecp5` maps them to a real non-Xilinx FPGA (Lattice ECP5,
e.g. `tcam`→~1.7 k `TRELLIS_FF`). Run: `cd syn/yosys && make` (needs `yosys` + `sv2v`).

## 7. Definition of done
- ✅ No `xpm_*`, no generated `axis_switch_*` IP in `hdl/` (T1.2–T1.4 done). `IOBUF`
  remains only in `milan_dma_wrapper` (the PS wrapper, T2).
- The 802.1Q datapath (`traffic_controller_802_1q`) and `ptp_ts_top` **elaborate in
  Verilator**; `milan_top`'s TSN half follows once the MAC has a `TARGET("GENERIC")`
  sim build (T2.1).
- All Verilator harnesses green (**13**) + Yosys generic synthesis green (**17 tops**).
- The only remaining vendor primitives are the free Xilinx SelectIO RGMII cells,
  gated behind the MAC `TARGET` param (absent in `GENERIC`/`SIM` builds).
