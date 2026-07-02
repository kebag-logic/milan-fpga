# Milan on a fully-FPGA RISC-V platform — detailed migration & implementation plan

This document is the step-by-step engineering plan to take the Milan TSN NIC
from its current **Zynq-7000 (hard ARM PS)** host to a **fully-FPGA** design
driven by a **RISC-V softcore with an MMU running Linux**, and then to extend it
into the **complete AVB/TSN solution including ADP / AVDECC**.

It is written to be read top-to-bottom by someone who will actually build it.
Every step names the concrete module, tool, file, signal, and address involved,
and cross-references the current RTL. For *what/why* see
[`REQUIREMENTS.md`](../REQUIREMENTS.md); for the datapath see
[`ARCHITECTURE.md`](ARCHITECTURE.md); for the CSR ABI see
[`REGISTER_MAP.md`](REGISTER_MAP.md).

> **Scope note.** This is a *plan*, not yet implemented RTL/gateware. It is split
> into **Part A** (fully-FPGA RISC-V Linux platform — replaces the PS) and
> **Part B** (ADP/AVDECC — the protocol stack on top). Part B builds on Part A.

---

## 0. Decisions & assumptions (confirm before starting)

| # | Decision | Chosen default | Status |
|---|----------|----------------|--------|
| D1 | Target device / board | **XC7A100T-2FGG484 on Alinx AX7101** | ✅ confirmed |
| D2 | RISC-V softcore + OS | **NaxRiscv RV64GC (Sv39 MMU) + LiteX + Buildroot Linux** | ✅ confirmed (RV64; see §A.4a) |
| D3 | SoC integration framework | **LiteX** (Migen) generating the SoC; Milan RTL integrated as external Verilog | ✅ (Vivado-native alt in §A.14) |
| D4 | ADP / AVDECC depth | **Full AVDECC entity + ADP**, IEEE 1722.1-2021 / **Milan v1.2** | ✅ confirmed |
| D5 | AVTP media talker/listener datapath | **Out of scope** for this plan (NIC + control only) | ⚠️ confirm |

> **D2 — NaxRiscv RV64 vs RV32.** NaxRiscv is chosen (over VexRiscv). Its
> best-supported Linux target is **RV64GC + Sv39 MMU** (the author's Debian/Buildroot
> demos are RV64), and a 64-bit Linux userspace is the standard footing for the
> AVDECC software stack (PipeWire `module-avb`, `la_avdecc`). In LiteX:
> `--cpu-type naxriscv --xlen 64 --with-fpu --with-rvc`. RV32 (`--xlen 32`, Sv32)
> remains a fallback if fabric/timing on `xc7a100t` gets tight — NaxRiscv supports
> both, so this is a one-flag change.

**Board facts to verify against the AX7101 schematic** (used throughout; correct
them if your board differs):

- FPGA: `xc7a100t-2fgg484` (Artix-7, 63 400 LUT6, 126 800 FF, 135 × 36 kb BRAM, 240 DSP).
- DDR3: typically one **Micron MT41J128M16** (256 MB, x16) — LiteDRAM needs the exact part.
- Ethernet: typically **2 × Realtek RTL8211E** Gigabit PHYs on **RGMII** (we use PHY0).
- 200 MHz (or 50 MHz) system oscillator, a user reset button, and a USB-UART (for the Linux console).

> If the AX7101 PHY is RGMII (it is on the standard board), the existing
> `eth_mac_1g_rgmii_fifo` MAC and RGMII timing are reused unchanged — a major win.

---

## 1. Why this is a "port the host, keep the datapath" job

The exploration of the current design shows a clean split. **The PL already owns
the entire TSN datapath**; the PS only provides *host* services. So the migration
is almost entirely about **replacing the PS box**, not the Milan logic.

### 1.1 What the PL already owns (reuse as-is)
- `eth_mac_1g_rgmii_fifo` — custom 1 G RGMII MAC (Forencich-style), 64-bit AXIS, `gtx_clk`/`gtx90_clk` for RGMII DDR (`milan_top.sv:415-464`).
- `traffic_controller_802_1q` — 802.1Q classifier + per-queue 802.1Qav CBS (`milan_top.sv:325-345`).
- `ptp_ts_top` — PTP hardware clock + TX/RX egress timestamp + metadata stream (`milan_top.sv:350-401`).
- `milan_csr` — AXI4-Lite CSR plane @ 64 KB window (`docs/REGISTER_MAP.md`), CDC to `gtx_clk` via `ptp_csr_sync`.
- `ethernet_events` — RMON counters.

### 1.2 What the Zynq PS provides today (must be re-created in fabric)
From the block design (`bd/milan-dma.tcl`) the PS supplies exactly seven services:

| # | PS service | Current source | Fabric replacement (Part A step) |
|---|-----------|----------------|----------------------------------|
| S1 | **DDR3 controller** (32-bit, DDR3-1066, MT41K128M16, HP0 window `0x0–0x2000_0000`) | PS7 hard DDR (`milan-dma.tcl:345,792`) | **LiteDRAM** (or Xilinx MIG) → §A.3 |
| S2 | **Clocks**: FCLK_CLK0 100 MHz → clk_wiz → `gtx_clk`125, `gtx90_clk`125@90°, `axis_clk`100 | PS7 PLL + `clk_wiz_0` (`milan-dma.tcl:872-895`) | **LiteX CRG / S7MMCM** → §A.4 |
| S3 | **Resets**: FCLK_RESET0_N → 2× proc_sys_reset | PS7 (`milan-dma.tcl:857,899`) | **LiteX reset + `proc_sys_reset`-equivalent** → §A.4 |
| S4 | **2× AXI-DMA** (simple mode, 64-bit): eth MM2S+S2MM, ts-metadata S2MM | `axi_dma` (`milan-dma.tcl:846-869`) | **New AXIS↔DRAM DMA** (LiteDRAM frontend) → §A.6 |
| S5 | **AXI4-Lite GP0 control master** → `milan_csr`@`0x43C0_0000` + DMA regs | PS7 M_AXI_GP0 + `axi_smc` (`:826,904`) | **CPU bus → AXI-Lite bridge** → §A.5 |
| S6 | **IRQ_F2P collector** (4 lines: TX-DMA, RX-DMA, ts-DMA, csr) | `ilconcat_0` (`:918`) | **PLIC / interrupt map** → §A.8 |
| S7 | **MDIO/PHY mgmt** via PS GEM1 EMIO; ARM runs the Linux driver | PS7 ENET1 EMIO (`:326-330`) | **Soft MDIO master + RISC-V Linux** → §A.7, §A.11 |

Everything else (RGMII pins, the AXIS datapath, the CSR ABI) is unchanged.

### 1.3 The one hard consequence of removing the PS
Two currently-**deferred** requirements become **mandatory**, because the PS was
silently covering them:
- **REQ-MAC-08 (MDIO in fabric)** — GEM1 EMIO is gone, so we must add a soft MDIO master.
- **REQ-MAC-06 (PHY reset GPIO)** — no more EMIO GPIO; a fabric GPIO drives PHY reset.
- **REQ-PTP-07 (PHC on a fixed 125 MHz)** — worth fixing now while re-doing clocking (§A.4).

---

## PART A — Fully-FPGA RISC-V Linux platform

Target SoC block diagram (text):

```
        ┌──────────────────────── XC7A100T (AX7101) ───────────────────────────┐
        │                                                                       │
  UART ─┼─[LiteX UART]         ┌───────────────┐      ┌──────────────────────┐  │
        │                      │   NaxRiscv    │ AXI  │   LiteDRAM (DDR3)     │──┼─ DDR3 (MT41J128M16)
   200M ┼─[CRG/MMCM]──sys/gtx→ │ RV64GC+Sv39   │◀────▶│   256 MB, ctrl+PHY   │  │
   osc  │      │  gtx90        │  L1$ + PLIC   │      └──────────────────────┘  │
        │      │               └──────┬────────┘                                │
        │      │        Wishbone/AXI-Lite bus (CPU)                             │
        │      │   ┌───────────┬──────┴───────┬──────────────┬──────────────┐   │
        │      │   ▼           ▼              ▼              ▼              ▼   │
        │  [BootROM]   [AXIL→milan_csr]  [DMA ctrl regs]  [MDIO mstr]   [GPIO] │
        │                   │  0x43C0_0000     │             │  PHY mgmt  │PHYrst│
        │                   ▼                  ▼             ▼              ▼   │
        │            ┌──────────────── Milan TSN datapath (unchanged) ───────┐ │
        │  DDR◀─DMA─▶│ classifier+CBS ─ PTP ts ─ eth_mac_1g_rgmii_fifo       │─┼─ RGMII → RTL8211E
        │            └──────────────────────────────────────────────────────┘ │
        └───────────────────────────────────────────────────────────────────────┘
```

### A.1 — Toolchain & repositories (host setup)
Everything here is open-source and needs **no** Xilinx license beyond Vivado for
place-and-route (the AX7101's `xc7a100t` is a free/Standard-tier part, unlike the
Zynq — so once Vivado has Artix-7 installed, synthesis→bitstream is unlicensed).

1. **Vivado** with **Artix-7** device support installed (this repo's box currently
   has Spartan-7 only — add Artix-7 via the AMD installer → *Add Devices*).
2. **RISC-V GCC** newlib + linux toolchains: `riscv64-unknown-elf-` and
   `riscv64-unknown-linux-gnu-` (or `riscv32-*` for RV32). Buildroot can build these.
3. **LiteX** ecosystem (Python/Migen):
   ```bash
   git clone https://github.com/enjoy-digital/litex
   ./litex/litex_setup.py --init --install    # pulls litex, litedram, liteeth,
                                               # litescope, pythondata-cpu-naxriscv, etc.
   ```
4. **NaxRiscv** Linux reference flow. NaxRiscv is a LiteX CPU
   (`--cpu-type naxriscv --xlen 64`); use the LiteX + `buildroot` Linux target
   (the `linux-on-litex-vexriscv` repo also drives NaxRiscv by passing
   `--cpu-type naxriscv`). NaxRiscv itself is SpinalHDL — LiteX fetches the
   generated Verilog via `pythondata-cpu-naxriscv`, so no Scala build is needed.
5. **Buildroot** (rootfs) and the **litex-buildenv**/`pythondata-software-*` packages
   pulled by (3)/(4).

**Deliverable A.1:** a working `litex` env that can build the stock
`linux-on-litex-vexriscv` for a supported board (validate the flow *before*
adding Milan).

### A.2 — LiteX platform file for the AX7101
LiteX needs a `platform` describing the board's pins & part. If a community
`alinx_ax7101.py` platform does not exist, write one (model it on
`litex_boards/platforms/*a7*`). It must declare:
- `device = "xc7a100tfgg484-2"`, `default_clk` (the 200 MHz osc) + `default_clk_period`.
- **DDR3** IOs (address/bank/DQ/DQS/DM/CK/CKE/ODT/CS/RAS/CAS/WE/RESET) with the exact
  FPGA pin names from the AX7101 XDC and the correct `IOSTANDARD` (SSTL15).
- **RGMII** IOs for PHY0: `rgmii_tx_clk/txd[3:0]/tx_ctl`, `rgmii_rx_clk/rxd[3:0]/rx_ctl`,
  `mdc`, `mdio`, `phy_rst_n`.
- **UART** (USB-UART pins), **user reset button**, LEDs.

**Deliverable A.2:** `platform/alinx_ax7101.py` + a `target/alinx_ax7101.py`
`BaseSoC` that builds an empty LiteX SoC (CPU+UART+DRAM) and prints the LiteX BIOS
on the console with a passing memtest. **This proves DDR3 + clocking + CPU before
any Milan logic.**

### A.3 — DDR3 controller (replaces PS S1)
Use **LiteDRAM** generated by LiteX for the AX7101's DDR3:
- Module: `litedram.modules.MT41J128M16` (or the exact board part).
- PHY: `litedram.phy.s7ddrphy.A7DDRPHY`, `nphases=4`, `sys_clk_freq` typically 100 MHz,
  memtype `DDR3`, `iodelay_clk_freq=200e6` (needs the 200 MHz ref for IDELAYCTRL).
- LiteDRAM exposes a **native port** and a Wishbone/AXI port to the CPU; the DMA
  (§A.6) will attach to a **second native/AXI port** for line-rate frame movement.

Alternative (Vivado-native, §A.14): **Xilinx MIG 7-series** IP generating a DDR3
controller with a 64-bit AXI4 slave — reuse the current AXI SmartConnect topology.

**Deliverable A.3:** `litex … --with-sdram` memtest passes at target `sys_clk_freq`.

### A.4 — Clocking & reset (replaces PS S2/S3, fixes REQ-PTP-07)
Recreate the three datapath clocks in a LiteX **CRG** (`S7MMCM`):
- `sys` (CPU/bus) — pick 100 MHz to match today's `axis_clk` so the datapath is unchanged.
- `axis_clk` = `sys` (100 MHz) — feeds classifier/CBS/DMA/CSR (as today).
- `gtx_clk` 125 MHz and `gtx90_clk` 125 MHz @ 90° — RGMII TX DDR (as today).
- **`ptp_clk` = a dedicated free-running 125 MHz** (NOT speed-switched) — connect the
  PTP `timestamp_counter` here to close **REQ-PTP-07**; keep `ptp_csr_sync` CDC between
  `axis_clk` (CSR) and `ptp_clk`.
- `idelay_ref` 200 MHz for LiteDRAM + a `clk200` `IDELAYCTRL`.

Reset: LiteX drives a global `sys_rst`; derive `axis_resetn`, `gtx_reset_n`
equivalents (active-low, synchronized per domain) exactly as the two
`proc_sys_reset` blocks did (`milan-dma.tcl:857,899`). Gate on MMCM `locked`.

**Deliverable A.4:** all four clocks stable, `locked` gating verified in sim + on HW (LED blink per domain).

### A.5 — CPU control bus → `milan_csr` (replaces PS S5)
`milan_csr` is an **AXI4-Lite slave** with `ADDR_WIDTH=16` (64 KB, only low 16 bits
decoded — `milan_top.sv:251`). Attach it to the CPU:
- In LiteX, add an **AXI-Lite bridge** from the CPU bus (Wishbone) using
  `litex.soc.interconnect.axi.Wishbone2AXILite` (or map it as a LiteX region with an
  `axi.AXILiteInterface`). Register it at a MMIO base — **keep `0x43C0_0000`** so the
  existing `docs/REGISTER_MAP.md` ABI and driver offsets are unchanged.
- Expose `milan_csr`'s ports via a LiteX `Instance()` wrapper (the datapath is added
  as external Verilog — §A.9).

**Deliverable A.5:** from the LiteX BIOS, `mem_read 0x43c00000` returns `0x4D494C4E`
("MILN", the `ID` register) — proving the CPU reaches the CSR plane.

### A.6 — DMA: AXIS ↔ DRAM (replaces PS S4 — the biggest new block)
The PS provided two **simple-mode** `axi_dma` engines. In fabric, replace them with
a LiteDRAM-frontend DMA. Two viable designs:

**Option 6a (recommended): LiteDRAM DMA + a thin descriptor/CSR shim.**
- TX (MM2S, DRAM→AXIS): `litedram.frontend.dma.LiteDRAMDMAReader` streaming into the
  `m_axis_tx_eth` path (`milan_top.sv:928` today). Add a small FSM + CSR regs
  (`tx_addr`, `tx_len`, `tx_start`, `tx_done_irq`) mirroring the axi_dma simple-mode
  register semantics the driver already expects.
- RX (S2MM, AXIS→DRAM): `LiteDRAMDMAWriter` fed by `s_axis_rx_eth`; CSR
  (`rx_addr`, `rx_len`, `rx_start`, `rx_done_irq`).
- TS-metadata (S2MM only): a second small `LiteDRAMDMAWriter` for the
  `ts_metadata_axis` stream (`milan_top.sv:104-105`).
- **Width:** keep 64-bit AXIS to match the datapath (`TDATA_WIDTH=64`).

**Option 6b: port the driver to a real SG DMA.** Adopt a scatter-gather engine
(LiteX `LiteDRAMDMA` + descriptor ring, or the open `corundum`-style DMA) and rework
the driver to descriptor rings. Bigger effort but removes the simple-mode 1-frame
bottleneck (aligns with the deferred **Phase 6 multi-channel DMA**).

> Decision: start with **6a** (fastest to Linux bring-up, matches current
> simple-mode driver), then optionally evolve to **6b** for multi-queue CBS/mqprio.

**Deliverable A.6:** a loopback test moves a frame DRAM→MAC→(external loopback)→MAC→DRAM
and both DMA-done IRQs fire.

### A.7 — MDIO master + PHY reset in fabric (replaces PS S7; closes REQ-MAC-06/08)
GEM1 EMIO MDIO is gone. Add:
- A **soft MDIO master**: either LiteEth's `LiteEthPHYMDIO`, or a small clause-22
  MDIO master with CSR regs (`mdio_addr`, `mdio_reg`, `mdio_wdata`, `mdio_rdata`,
  `mdio_start/busy`). Drive the AX7101 PHY0 `mdc`/`mdio` pins.
- A **GPIO** bit for `phy_rst_n` (CSR) → maps to the driver's `phy-reset-gpios`.
- Wire both into `milan_csr`'s MAC group (new offsets in the `0x100` block; update
  `REGISTER_MAP.md`, REQ-MAC-06/08).

**Deliverable A.7:** driver/BIOS reads the PHY ID via MDIO and can assert/deassert PHY reset.

### A.8 — Interrupts (replaces PS S6)
Route the four current IRQ sources to the **NaxRiscv PLIC** (LiteX `add_interrupt`):
- `tx_dma_done`, `rx_dma_done`, `ts_dma_done` (from §A.6),
- `irq_csr` = `milan_csr.o_irq` = `|(IRQ_STATUS & IRQ_MASK)` (tx_ts_ready/link_change/rmon_rollover).

Each gets a PLIC source number recorded in the device tree (§A.12). This replaces
the `ilconcat_0 → IRQ_F2P` collector (`milan-dma.tcl:918-971`).

**Deliverable A.8:** Linux `/proc/interrupts` shows all four lines and they increment.

### A.9 — Integrating the Milan RTL into the LiteX SoC
Add the existing HDL as external sources (no rewrite):
```python
platform.add_source_dir("milan-fpga/hdl")          # all *.sv/*.v/*.svh
self.specials += Instance("traffic_controller_802_1q", ...)   # or a milan_datapath wrapper
```
Recommended: create a **`milan_datapath.sv`** thin wrapper that instantiates
`traffic_controller_802_1q` + `ptp_ts_top` + `eth_mac_1g_rgmii_fifo` +
`ethernet_events` with just AXIS + CSR + RGMII + clock ports — i.e. `milan_top.sv`
*minus* `milan_dma_wrapper` (the PS). LiteX instances that one module. This keeps a
single clean HW/gateware boundary and lets `milan_top.sv` remain the Zynq variant.

**SystemVerilog note:** Vivado (the LiteX Xilinx toolchain backend) handles the SV;
ensure the `read_verilog -sv` path is used. The OOC-synth pass in this repo already
proved these modules synthesize (10/12 clean; the 2 "failures" were an OOC-only
interface-width artifact and the AXIS-switch IP — see the session notes).

> **De-Xilinx first (recommended):** before this, run **Track 1** of
> [`OPEN_SOURCE_MIGRATION.md`](OPEN_SOURCE_MIGRATION.md) — replace the XPM FIFOs /
> `axis_switch` IP / `xpm_cdc_*` with Forencich `verilog-axis`/`-axi`/`-ethernet`
> cores. That makes the whole TSN datapath Verilator-simulatable (not just leaf
> blocks) and removes vendor lock-in, so the LiteX integration here is against clean,
> portable RTL.

**Deliverable A.9:** the full SoC synthesizes and routes on `xc7a100t`; capture the
resource report (budget target below).

**Rough resource budget (xc7a100t = 63 400 LUT):**
| Block | ~LUT | Notes |
|-------|------|-------|
| NaxRiscv RV64GC 1-core +Sv39 +caches +FPU | 12–18 k | RV64 is heavier than RV32; drop FPU/RVC or fall back to `--xlen 32` if tight |
| LiteDRAM (A7DDRPHY+ctrl) | 5–8 k | DDR3 256 MB |
| Milan datapath (MAC+CBS+CLS+PTP+CSR) | 15–25 k | real (in-context) synth, < OOC estimate |
| DMA (3× LiteDRAM frontend + shims) | 2–4 k | |
| UART/MDIO/GPIO/PLIC/interconnect | 2–3 k | |
| **Total** | **~40–55 k** | fits `xc7a100t` (63 400 LUT); **1 core**. If RV64+FPU overflows, use `--xlen 32` (Sv32) — frees ~5–8 k LUT |

### A.10 — Boot & Linux (replaces the ARM boot)
The RISC-V Linux boot chain (as in linux-on-litex-vexriscv):
1. **LiteX BIOS** (in BRAM ROM) — brings up DRAM, loads the next stage from SPI-flash
   or over serial/`litex_term`.
2. **OpenSBI** (RISC-V SBI / M-mode firmware) — `generic` platform for LiteX.
3. **Linux kernel `Image`** (RV32, `CONFIG_MMU=y`, `litex_soc` defconfig-style) + the
   **DTB** (§A.12).
4. **Buildroot rootfs** (initramfs `cpio` or on the SD/flash).

Artifacts land as `opensbi.bin` + `Image` + `rv32.dtb` + `rootfs.cpio`; `litex_term`
uploads them for first bring-up, then flash for standalone boot.

**Deliverable A.10:** Linux boots to a shell on the AX7101 over UART, `uname -a`
shows the RISC-V kernel, DRAM size correct.

### A.11 — Linux driver port (Phase 7, re-hosted)
The tracked driver work (`REQ-DRV-01..08`, currently all not-done) is now written
against a **RISC-V platform device** instead of the Zynq PS. What changes vs the
original plan:
- **Bus/DT model:** the `kl,dma-ether` node lives under the LiteX SoC DT (§A.12), not a
  Zynq `.dtsi`. `reg` points at the CSR (`0x43C0_0000`) + the new fabric DMA regs;
  `interrupts` reference the **PLIC** phandles, not `IRQ_F2P`.
- **DMA:** driver talks to the §A.6 DMA regs. If Option 6a, keep the simple-mode
  per-transfer model; if 6b, use dmaengine/descriptor rings.
- **PHC (`ptp_clock_info`)** against the `0x500` PTP regs — unchanged ABI. The
  `gettimex64` pairing that used the ARM global timer now pairs with the RISC-V
  `rdtime`/CLINT mtime — update the cross-timestamp path.
- **MDIO/phylib:** now points at the **fabric MDIO master** (§A.7) instead of PS GEM1.
- **CBS/mqprio offload, HW timestamping, ethtool_ops** — unchanged CSR ABI, so the
  bulk of `REQ-DRV-05..08` is portable verbatim.

**Required driver feature surface** (`FR-DRV-*` in [`FR_NFR.md`](FR_NFR.md) §2.10):
- **NAPI** RX/TX poll with per-queue contexts over the fabric DMA rings; the N HW
  queues exposed as real netdev queues (so `tc mqprio`/CBS map to hardware).
- **XDP**: `ndo_bpf`/`ndo_xdp_xmit`, all `XDP_*` actions, page-pool RX + headroom;
  **AF_XDP zero-copy** (per-queue `xsk_pool`) for kernel-bypass to the media plane.
- **PTP**: a `ptp_clock_info` PHC on the `0x500` CSRs (`gettimex64` crosstimestamp vs
  RISC-V `rdtime`/CLINT mtime), `SIOCSHWTSTAMP` + TX/RX HW timestamps from the PTP
  metadata stream into `skb_hwtstamps`.
- **ethtool**: `-T` (PHC + HW-timestamp caps), `-S` (RMON CSR stats), `-l/-L`
  (channels), `-g/-G` (rings), `-c/-C` (coalesce), link settings, and `ndo_setup_tc`
  CBS/mqprio offload.
- **RX filter**: `ndo_set_rx_mode` programs the MC_HASH / TCAM (`0x700`) dest-MAC filter.

**Deliverable A.11:** `ip link` shows the netdev with N queues; `ping` over RGMII;
`ethtool -T` advertises the PHC; `ethtool -S` shows RMON; an `XDP_DROP` program
attaches and drops; `ptp4l` locks.

### A.12 — Device tree (Phase 8, re-hosted)
LiteX **auto-generates** most of the SoC DT (`--csr-json` → `litex_json2dts_linux`).
Add the Milan node by hand/overlay:
```dts
eth0: ethernet@43c00000 {
    compatible = "kl,dma-ether-0.9";
    reg = <0x43c00000 0x10000>,          /* milan_csr */
          <0x/*dma_tx*/ 0x100>, <0x/*dma_rx*/ 0x100>, <0x/*dma_ts*/ 0x100>;
    interrupt-parent = <&plic>;
    interrupts = </*tx*/ /*rx*/ /*ts*/ /*csr*/>;
    kl,txq-cnt = <4>; kl,rxq-cnt = <4>;
    phy-handle = <&phy0>; phy-mode = "rgmii-id";
    phy-reset-gpios = <&gpio /*phy_rst bit*/ GPIO_ACTIVE_LOW>;
    local-mac-address = [xx xx xx xx xx xx];
    mdio { phy0: ethernet-phy@1 { reg = <1>; }; };
};
```
This replaces the Xilinx `device-tree-xlnx` (dtg) flow (`REQ-DT-02`) — the
`fpga-ps-tools` dtg dependency **drops entirely** for the fully-FPGA build; the DT is
LiteX-generated + this overlay.

**Deliverable A.12:** DT compiles, driver probes, all four IRQs and the PHC register.

### A.13 — Constraints (XDC) & board bring-up
- Reuse the current RGMII timing constraints (input/output delay on `rgmii_*`) from the
  Zynq XDC, re-pinned to AX7101 PHY0 pins.
- DDR3 pin/IOSTANDARD constraints come from the LiteX platform (auto-emitted).
- Add UART, reset button, `clk200`/osc, PHY reset, MDIO, LEDs.
- Timing closure targets: `sys/axis` 100 MHz, `gtx` 125 MHz, DDR PHY 100→400 MHz.

### A.14 — Alternative: Vivado-native AXI SoC (no LiteX)
If you prefer to stay entirely in Vivado (reusing `axi_dma`, `milan_csr`, and the
block-design flow, only swapping the PS box):
1. Generate **NaxRiscv** as Verilog with an **AXI4** master, Sv39 MMU, PLIC (or
   VexRiscv if you prefer a lighter core here).
2. Add **Xilinx MIG 7-series** DDR3 IP (AXI4 slave) — free on Artix-7.
3. Keep `axi_smc`/`smartconnect` topology; the CPU AXI master replaces `M_AXI_GP0`,
   MIG replaces `S_AXI_HP0`+PS DDR, a **BRAM** holds the boot ROM.
4. Add a soft **CLINT+PLIC** and route the 4 IRQs to the PLIC.
5. Build OpenSBI+Linux+DTB by hand (no LiteX BIOS).
- **Pros:** reuses `axi_dma`, the BD, and this repo's `bd/build.tcl` flow verbatim.
- **Cons:** you hand-build the DRAM calibration bring-up, boot, and DT that LiteX
  automates — more manual, less community support for Linux-on-RISC-V-in-Vivado.

**Recommendation:** LiteX (D3) for the first Linux bring-up; the Vivado-native path is
a fallback if LiteX/AX7101 integration proves troublesome.

### A.15 — Part A milestones & exit criteria
1. **M-A1** LiteX empty SoC: BIOS + DRAM memtest on AX7101. *(§A.2–A.4)*
2. **M-A2** CPU reaches `milan_csr`: reads `ID="MILN"`. *(§A.5)*
3. **M-A3** DMA loopback + IRQs. *(§A.6, A.8)*
4. **M-A4** Linux boots to shell. *(§A.10)*
5. **M-A5** Driver up: `ping` over RGMII, `ethtool -T` PHC, `ptp4l` locks, `tc cbs` shapes. *(§A.11–A.13)*  ← **this is "Milan fully on FPGA"**

---

## PART B — ADP / AVDECC (the complete AVB solution)

Milan is an **AVnu profile of IEEE 1722/1722.1 (AVDECC) over 802.1 TSN**. The TSN
plane (802.1Q/Qav/1588) is done; the **AVDECC control plane and reservation plane
are essentially absent**. Today only two **RX-only, unconnected parser stubs** exist:
- `hdl/adp/KL_adp_parser.sv` — decodes an incoming ADPDU into `entity_info_t`
  (all fields modeled in `adp_pkg.sv:47-66`), asserts one-hot
  `rcv_adp_discover/available/departing`, but **does not transmit or run any FSM**;
  the `adp_advertise_event_t` / `adp_discovery_event_t` structs (`adp_pkg.sv:28-44`)
  are **defined but unused**. Instantiated only in its testbench.
- `hdl/1722/KL_avtp_common_parser.sv` — steers AVTP frames by subtype
  (ADP/AECP/ACMP/MAAP→tdest0, AAF/…→tdest1, CRF→tdest2, else drop); also unconnected.

Target specs: **IEEE 1722.1-2021** (AVDECC) with the **AVnu Milan v1.2** profile.

### B.pre — Prior work to build on (do NOT start from scratch)

Substantial AVDECC design already exists in this repo/tree — the plan below
*continues* it:

- **HW AEM/AECP design:** [`aem-and-aecp.md`](../aem-and-aecp.md) + `aem-and-aecp.pdf`
  specify the FPGA **4-level AEM memory** (L0 ENTITY → L1 config table → L2
  per-type tables → L3 payload, static/semi-static/dynamic split), the generic
  getter/setter keyed by `command_type / configuration_index / descriptor_type /
  descriptor_index`, the AECP validation/parse/response pipeline, timers, and the
  **Milan MVU** (`protocol_id 00-1B-C5-0A-C1-00`; `GET_MILAN_INFO`,
  `GET/SET_SYSTEM_UNIQUE_ID`, `GET/SET_MEDIA_CLOCK_REFERENCE_INFO`).
- **The entity model (data):** [`avdecc/milan-v12-entity.json`](../avdecc/milan-v12-entity.json)
  (+ [`avdecc/README.md`](../avdecc/README.md)) — one Milan v1.2 entity, byte-accurate
  to the reference software entity, with every field tagged `static/semi_static/
  nonvolatile/dynamic` so it feeds **both** the FPGA AEM memory and software. **This
  JSON is the single source of truth for the descriptor tree** (see B.3).
- **Reference software entity:** `srcs/.../module-avb/entity-model-milan-v12.h` +
  `aecp-vendor-unique-milan-v12.h` (PipeWire `module-avb`) — the working
  implementation the JSON mirrors. Reuse it as the SW AVDECC stack (see B.0).
- **Test/interop:** `srcs/the-private-test-repo/controller/avdecc_l2.py` (ADP watch,
  GET_COUNTERS, ACMP connect) and `software-defined-tsn-stack/.../1722_1/aecp/*.yaml`
  (byte-exact AECP PDU specs incl. `milan/aecp_read_descriptor.yaml`) — the
  conformance oracles for B.2–B.4.

### B.0 — HW/SW split (the key architectural decision)
AVDECC control is stateful, table-heavy, and rarely latency-critical → **do it in
software on the RISC-V Linux** (now that Part A gives us Linux). Keep in **hardware**
only what benefits from it:
- **HW:** frame reception + subtype classification (existing parsers), PTP timestamps,
  and a **HW ADP advertiser** (periodic ENTITY_AVAILABLE, low-jitter, survives CPU
  load) — this "implements ADP" in the strong sense the request asks for.
- **SW (Linux):** the full **AVDECC entity model** — AECP/AEM (incl. Milan MVU),
  ACMP, MAAP, descriptor tree. **Primary stack = PipeWire `module-avb`** (already in
  `srcs/.../module-avb`, with the Milan v1.2 entity in `entity-model-milan-v12.h` +
  `aecp-vendor-unique-milan-v12.h`); alternatives are OpenAvnu / avdecc-lib /
  la_avdecc. SW also handles ADP *discovery* bookkeeping (who's on the network).

This mirrors how real Milan endpoints are built and keeps HW small.

> **Optional HW AEM.** If you want the AEM served from the FPGA instead of Linux
> (lower latency, CPU-independent enumeration), implement the **4-level AEM memory +
> AECP pipeline** from [`aem-and-aecp.md`](../aem-and-aecp.md), generating its L0–L3
> image from [`avdecc/milan-v12-entity.json`](../avdecc/milan-v12-entity.json). The
> JSON's `static/semi_static/nonvolatile/dynamic` field classes map directly onto
> that design's factory-NVM / modifiable-overlay / volatile-mirror memories. Start
> with SW (faster) and migrate hot paths to HW later.

### B.1 — Connect the control-frame path into the datapath
Right now AVDECC frames go RX→MAC→PTP→DMA→DRAM like any packet, but nothing routes
them to a control handler. Add a **control tap**:
1. In the RX path, use the **802.1Q classifier** (already present) to send frames with
   AVTP EtherType `0x22F0` (and/or the 1722.1 multicast MACs) to a dedicated **control
   queue** (one of the 4 queues, mapped by a CSR table entry).
2. Feed that queue's AXIS through `KL_avtp_common_parser` (wire it in — today it's
   standalone) to split ADP/AECP/ACMP/MAAP.
3. Deliver control frames to Linux via the existing RX DMA on the control queue (SW
   stack parses them), **and** tee the ADP `discover/available/departing` strobes from
   `KL_adp_parser` to the HW advertiser (§B.2).

**Deliverable B.1:** AVDECC control frames arrive in a dedicated netdev queue and the
`KL_adp_parser` strobes are observable in a CSR.

### B.2 — HW ADP advertiser + discovery FSM (the missing TX side)  ✅ DONE + INTEGRATED
> **Status (implemented, integrated, verified):**
> - [`hdl/adp/adp_advertiser.sv`](../hdl/adp/adp_advertiser.sv) — [`tb/verilator/adp/`](../tb/verilator/adp) **121 checks PASS**.
> - **CSR wiring:** `milan_csr` **0x600 ADP group** (identity/control + `available_index` RO);
>   [`tb/verilator/csr/`](../tb/verilator/csr) extended to **62 checks PASS**; ABI in
>   [`REGISTER_MAP.md`](REGISTER_MAP.md) §0x600.
> - **MAC TX integration:** [`hdl/adp/adp_tx_arbiter.sv`](../hdl/adp/adp_tx_arbiter.sv) merges
>   ADP into the MAC TX between frames — [`tb/verilator/adp_tx/`](../tb/verilator/adp_tx) **26 checks PASS**.
> - **Wired in `milan_top.sv`** (advertiser + arbiter + 1 s tick + link-edge pulses); all ports
>   connectivity-checked; `milan_top` elaborates the ADP modules cleanly. Design docs:
>   [`hdl/adp/doc/adp_advertiser.md`](../hdl/adp/doc/adp_advertiser.md).
>
> Remaining for M-B2 to be *observable*: tie in `rcv_discover_i` (from `KL_adp_parser`, §B.1)
> and `gm_change_i` (gPTP), and real `link_up` (REQ-MAC-03). Full regression: **8 harnesses green**.

Implement the counterpart the repo lacks — an **ADPDU builder + advertise state
machine** realizing `adp_pkg`'s event structs:
- **Advertise FSM** (`adp_advertise_event_t`): on `LINK_UP`/`TMR_ADVERTISE` send
  `ENTITY_AVAILABLE`; re-advertise every `valid_time/2`; increment `available_index`
  on any change; send `ENTITY_DEPARTING` on `SHUTDOWN`/`LINK_DOWN`; respond to
  `RCV_ADP_DISCOVER` (from `KL_adp_parser`) with an immediate advertise.
- **ADPDU serializer:** build the 68-byte ADPDU (Ethernet + AVTP control header +
  `entity_info_t` fields from `adp_pkg.sv:47-66`) into a TX AXIS stream, injected into
  the TX path (arbitrated ahead of/around the CBS shaper on the control queue).
- **CSR:** expose `entity_id`, `entity_model_id`, capabilities, talker/listener counts,
  `valid_time`, `gptp_grandmaster_id`, `available_index`, and an `adp_enable`/`departing`
  control — so Linux/AVDECC-stack owns the entity identity but HW does the timing.
- **Reuse:** `adp_pkg.sv` constants (`0x22F0`, subtype `0xFA`, msg-type codes,
  `CTRL_DATA_LENGTH_C=0x38`) and `entity_info_t` are already defined — build on them.

**Deliverable B.2:** a controller (e.g. Hive/`avdecc` discovery) sees the entity appear
and depart; a Verilator harness checks the ADPDU byte layout + advertise timing +
`available_index` increment (add `tb/verilator/adp/`).

### B.3 — AECP (AEM) — enumeration & control (from the JSON entity model)
The **descriptor tree is defined once** in
[`avdecc/milan-v12-entity.json`](../avdecc/milan-v12-entity.json) and served by the
AEM handler (SW stack, or the HW 4-level AEM per B.0):
- Descriptors covered by the model: `ENTITY`, 1× `CONFIGURATION` (48/96/192 kHz,
  non-redundant), `AUDIO_UNIT`,
  `STREAM_INPUT` (AAF + CRF), `STREAM_OUTPUT`, `AVB_INTERFACE`, 3× `CLOCK_SOURCE`,
  `CLOCK_DOMAIN`, `CONTROL` (IDENTIFY), `LOCALE`/`STRINGS`, `STREAM_PORT_IN/OUT`,
  16× `AUDIO_CLUSTER`, 2× `AUDIO_MAP`.
- AEM commands handled: `READ_DESCRIPTOR`, `ACQUIRE_ENTITY`, `LOCK_ENTITY`,
  `GET/SET_CONFIGURATION`, `GET/SET_STREAM_FORMAT`, `GET/SET_CLOCK_SOURCE`,
  `SET_SAMPLING_RATE`, `SET_NAME`, `SET_CONTROL` (IDENTIFY),
  `ADD/REMOVE_AUDIO_MAPPINGS`, `REGISTER_UNSOLICITED_NOTIFICATION`, `GET_AVB_INFO`,
  `GET_COUNTERS` (reads the HW **RMON** + PTP CSRs — small ABI addition), and the
  **Milan MVU** `GET_MILAN_INFO` (+ `SYSTEM_UNIQUE_ID` / `MEDIA_CLOCK_REFERENCE_INFO`).
- The JSON's field `class` tells the handler what is settable/persisted: `dynamic`
  fields (stream `current_format`, `clock_source_index`, IDENTIFY value, gPTP,
  counters) are backed by live HW/CSR; `nonvolatile` (names, current_config) persist.
- The `GET_AS_PATH` / `GET_AVB_INFO` gPTP fields come from the **PTP** block CSRs.

**Deliverable B.3:** a controller (Hive / `avdecc_l2.py`) enumerates the entity and
every `READ_DESCRIPTOR` matches the JSON; `GET_COUNTERS` matches `ethtool -S`;
`GET_MILAN_INFO` returns Milan v1.2 protocol_version/certification.

### B.4 — ACMP — stream connection management (software)
Implement `CONNECT_TX/RX_COMMAND`, `DISCONNECT_*`, `GET_TX/RX_STATE` in the SW stack.
When a connection is established, ACMP programs:
- the **classifier/queue** mapping for the stream's VLAN/PCP,
- the **CBS** idleSlope/hi/lo for the stream's reservation (existing `0x400` CSRs),
- (if talker/listener media datapath exists — D5) the stream ID / dest MAC filters.

**Deliverable B.4:** a controller connects a talker→listener; the CBS registers change
to match the reserved bandwidth (observable via `ethtool`/CSR).

### B.5 — MAAP — multicast address allocation (software daemon + HW filter)
Run a **MAAP** daemon (OpenAvnu `maap`) to PROBE/DEFEND/ANNOUNCE a dynamic multicast
MAC pool for stream destinations. HW support = the **RX MAC address filter**
(**REQ-MAC-02**, currently not-done) so allocated multicast MACs are accepted.

**Deliverable B.5:** MAAP acquires an address range without conflict; HW filter passes
those multicasts.

### B.6 — SRP / MSRP / MVRP — reservation plane (software, big)
Stream Reservation (802.1Qat MSRP + 802.1Qak MVRP) is a **separate large plane**,
absent from HW. Run it in **software** (OpenAvnu **`mrpd`**):
- MSRP Talker Advertise / Listener Ready, MVRP VLAN registration, MMRP.
- On a successful reservation, `mrpd`→AVDECC→CBS programming (as §B.4) sets the shaper.
- HW hooks: the classifier must honor the reserved VLAN/PCP (already programmable);
  optionally add HW policing later (802.1Qci PSFP — REQ-CLS-09, a MAY).

**Deliverable B.6:** `mrpd` reserves a stream end-to-end against a real bridge; CBS is
programmed from the reservation.

### B.7 — (Optional, D5) AVTP talker/listener media datapath
Only if media streaming (not just NIC+control) is in scope. This is the largest
addition and is **out of scope** by default:
- **Talker:** AAF/CRF/CVF encapsulation, AVTP presentation-time stamping from the PHC,
  media-clock domain.
- **Listener:** de-encapsulation, presentation-time de-jitter, media-clock recovery.
- The existing `KL_avtp_common_parser` only *steers* subtypes and does **not** decode
  payloads — a full talker/listener is new RTL.

### B.8 — Part B milestones
1. **M-B1** Control-frame tap + `KL_avtp_common_parser`/`KL_adp_parser` wired in. *(§B.1)*
2. **M-B2** HW ADP advertiser: entity visible/departing to a controller. *(§B.2)*
3. **M-B3** SW AVDECC (AECP/AEM): entity enumerable + lockable. *(§B.3)*
4. **M-B4** ACMP connect → CBS auto-programmed. *(§B.4)*
5. **M-B5** MAAP + MSRP/MVRP reservation drives the shaper end-to-end. *(§B.5, B.6)*  ← **"ADP/AVDECC implemented"**

---

## 3. Effort, risk, and ordering

| Phase | Work | Rough effort | Main risk |
|-------|------|--------------|-----------|
| A.1–A.4 | LiteX env, AX7101 platform, DRAM+clocks | 1–2 wk | LiteDRAM timing on the exact DDR3 part |
| A.5–A.9 | CSR bridge, DMA, MDIO, IRQ, integrate Milan RTL, synth | 3–5 wk | **new DMA** is the critical path; RGMII/DDR timing closure |
| A.10–A.13 | Linux boot + driver port + DT + bring-up | 3–5 wk | driver DMA + PHC cross-timestamp on RISC-V |
| B.1–B.2 | Control tap + **HW ADP advertiser** (RTL + Verilator) | 2–3 wk | ADPDU byte-exactness, advertise timing |
| B.3–B.6 | SW AVDECC (AECP/ACMP/MAAP) + MSRP via OpenAvnu | 4–8 wk | integrating an AVDECC stack + interop with a real controller |
| B.7 | (optional) AVTP talker/listener media path | 6–10 wk | media-clock recovery, presentation time |

**Critical dependencies:** Part B needs Linux (Part A M-A4). The HW ADP advertiser
(B.2) is the only strictly-new *hardware* protocol block; the rest of AVDECC is
software leveraging OpenAvnu / avdecc-lib.

## 4. What changes in the repo (file-level)
- **New:** `hdl/common/milan_datapath.sv` (PS-less wrapper), `hdl/dma/*` (AXIS↔DRAM DMA),
  `hdl/mdio/mdio_master.sv`, `hdl/adp/adp_advertiser.sv` + `adp_tx_serializer.sv`,
  LiteX `platform/target` Python (NaxRiscv RV64), `sw/` (buildroot + driver DT overlay),
  Verilator harnesses `tb/verilator/adp/`, and (optional HW AEM) `hdl/aecp/*` +
  `tools/aem_gen.py` consuming the entity model.
- **Already added (this work):** `avdecc/milan-v12-entity.json` + `avdecc/README.md`
  (the Milan v1.2 entity model); the AEM/AECP HW design in `aem-and-aecp.{md,pdf}`.
- **Reused unchanged:** classifier, CBS, PTP, MAC, CSR, RMON; the PipeWire `module-avb`
  SW AVDECC stack (`entity-model-milan-v12.h`), `avdecc_l2.py` test controller.
- **Retired for this build:** `bd/milan-dma.tcl` PS7 block design, `milan_dma_wrapper.v`,
  the `device-tree-xlnx` dtg dependency. (`milan_top.sv` stays as the Zynq variant.)
- **Newly-mandatory reqs:** REQ-MAC-02 (RX filter, for MAAP), REQ-MAC-06 (PHY reset),
  REQ-MAC-08 (fabric MDIO), REQ-PTP-07 (fixed 125 MHz PHC).

---

## 5. Open items to confirm
Confirmed: **D1** AX7101/xc7a100t · **D2** NaxRiscv RV64GC + LiteX · **D3** LiteX ·
**D4** full AVDECC entity + ADP, IEEE 1722.1-2021 / Milan v1.2. Remaining:

1. **Media datapath (D5):** AVTP talker/listener assumed **out of scope** (NIC +
   control only) — confirm, or add §B.7.
2. **Board specifics:** exact DDR3 part and Ethernet PHY on your AX7101 (needed for
   LiteDRAM + RGMII timing).
3. **Milan MVU codes** (`avdecc/README.md` open items): confirm the `SYSTEM_UNIQUE_ID`
   / `MEDIA_CLOCK_REFERENCE_INFO` command codes and ADP `valid_time` against the
   Milan v1.2 PDF (only `GET_MILAN_INFO=0x0000` is confirmed in the reference SW).
4. *(resolved)* **Configuration & rates:** single configuration; sample rates
   **48/96/192 kHz** handled via AUDIO_UNIT `sampling_rates` + `SET_SAMPLING_RATE`;
   **redundancy is out of scope** (`configurations_count=1`, `MILAN_REDUNDANCY=0`).
