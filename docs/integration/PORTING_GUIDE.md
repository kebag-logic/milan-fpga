# Porting guide - building the Milan TSN datapath without Vivado, on any vendor's board

This is the vendor-neutral porting guide: what it takes to run this design on a
board that is **not** a Xilinx/Vivado board (Intel/Altera, Lattice, Gowin,
Microchip, or an open Yosys/nextpnr flow), or on a Xilinx board without the
Vivado-generated Zynq block design.

It complements [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) (how to wire
`milan_datapath` into *your* SoC at the bus level). Read that one for the port
list; read this one for the toolchain/board work.

**TL;DR:** the TSN datapath RTL under `hdl/` is deliberately vendor-neutral -
no XPM, no vendor primitives, machine-checked by the
[`syn/yosys/`](../../syn/yosys) flow (generic synth + Lattice ECP5 mapping).
Everything vendor-specific lives in three well-separated places you replace
per board: the **host SoC** (Zynq PS block design *or* LiteX softcore), the
**board I/O layer** (PLLs, DDR PHY, RGMII/GMII I/O cells, pin constraints),
and the **MAC** (attached outside the datapath on purpose).

---

## Contents

- **[1. The three layers, and which ones you rewrite](#1-the-three-layers-and-which-ones-you-rewrite)** -- The scoping table that tells you how big the job is: the datapath RTL recompiles as-is, the host SoC gets replaced, the board I/O layer is normal bring-up. Also why the MAC sits outside the boundary on purpose.
- **[2. What is (and is not) Xilinx-specific in the RTL - the full inventory](#2-what-is-and-is-not-xilinx-specific-in-the-rtl---the-full-inventory)** -- File-and-line audit of every vendor-touching thing left, which is attributes only -- `use_dsp`, `dont_touch`, `mark_debug`, `ASYNC_REG` -- each with what it does off-Xilinx and what to do about it. Section 2.1 lists the sources missing after a plain clone, including the SSH-only submodule you should *not* try to fetch.
- **[3. Clocking and reset requirements (vendor-independent contract)](#3-clocking-and-reset-requirements-vendor-independent-contract)** -- Three clocks, their frequencies and who consumes them. The useful headroom note: 64-bit AXIS at 100 MHz is 6.4 Gb/s against a 1 GbE wire, so running `axis_clk` slower is a legitimate way out of a timing problem.
- **[4. The per-board work list](#4-the-per-board-work-list)** -- The actual bring-up work, in five parts, with a Xilinx→Intel/Lattice/Gowin/Microchip equivalence table for clock generation and DDR I/O. Section 4.5 is the one not to skip: the CBS slope divide is the true critical path at 100 MHz and is closed by a multicycle constraint, not by luck.
- **[5. Proving it: the open-toolchain portability check](#5-proving-it-the-open-toolchain-portability-check)** -- How vendor-neutrality is machine-checked rather than asserted -- `hierarchy -check` fails on any surviving vendor cell, and `make ecp5` maps to real silicon. States plainly what this does *not* prove: synthesizability, not timing, and no off-Xilinx SoC has closed at 100 MHz.
- **[6. Recommended porting routes](#6-recommended-porting-routes)** -- Two routes, cheapest first. Route A is a six-step LiteX board swap that keeps the bring-up order which actually worked: CPU boots → read `"MILN"` at offset 0 → attach MAC → attach DMA.
- **[7. Port-readiness checklist](#7-port-readiness-checklist)** -- Nine tick-boxes to run down before you commit to a target board, ending with the known-limitations page -- MTU, single-port and perf ceilings are easier to learn about now than after the order.

## 1. The three layers, and which ones you rewrite

| Layer | What is in it | Vendor-specific? | Port effort |
|---|---|---|---|
| **Datapath RTL** (`hdl/`, minus `milan_top.sv`/`milan_dma_wrapper.v`) | classify + 802.1Qav CBS, PTP PHC + timestamping, TCAM RX filter, ADP advertiser, RMON counters, CSR block, CDC primitives | **No** - proven by Yosys generic synth + ECP5 map (Section 5) | None (recompile as-is) |
| **Host SoC** | Zynq PS7 flow (`bd/*.tcl`, `milan_top.sv`, `milan_dma_wrapper.v`) *or* LiteX RISC-V flow ([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py)) | Yes (PS7 is Zynq-only; the LiteX target instantiates Series-7 PLL/DDR/IO cores) | Replace host: LiteX re-target (recommended, Section 6.1) or your own SoC ([INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)) |
| **Board I/O** | clock gen, reset, DDR PHY, Ethernet PHY I/O cells, pin/timing constraints (`constraints/*.xdc`, [`sw/litex/platforms/alinx_ax7101.py`](../../sw/litex/platforms/alinx_ax7101.py)) | Yes, always | Redo per board (Section 4) - this is normal board bring-up, not a redesign |

The MAC itself is **outside** the datapath boundary: `milan_datapath` exposes a
MAC-facing 64-bit AXI-Stream pair plus config/status ports, so you attach
whatever MAC suits your host (LiteEth on LiteX, Forencich `verilog-ethernet`,
or a vendor MAC) - see Section 4.3.

---

## 2. What is (and is not) Xilinx-specific in the RTL - the full inventory

The datapath RTL contains **no instantiated vendor primitives**. The
`xpm_fifo_axis` / `xpm_cdc_*` / generated `axis_switch_*` IP that used to block
portability were removed (history: [OPEN_SOURCE_MIGRATION.md (archived)](../../historical_now_obsolete/integration/OPEN_SOURCE_MIGRATION.md));
FIFOs/demux now come from the MIT-licensed
[`third_party/verilog-axis`](../../THIRD_PARTY.md) submodule and the CDC from
in-repo plain-FF primitives ([`hdl/common/cdc_pulse.sv`](../../hdl/common/cdc_pulse.sv),
[`hdl/common/cdc_handshake.sv`](../../hdl/common/cdc_handshake.sv), [`hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv`](../../hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv)).

What remains vendor-*touching* is only attributes and parameters - all of them
harmless or overridable off-Xilinx:

| Where | What | Effect on Xilinx | Effect elsewhere | Action when porting |
|---|---|---|---|---|
| [`hdl/ieee8021q/ts/credit_based_shaper.sv:106`](../../hdl/ieee8021q/ts/credit_based_shaper.sv#L106) | `(* use_dsp = "yes" *)` on the 48-bit credit accumulator | infers DSP48 | ignored; infers LUT/carry logic (works, uses more fabric) | optional: replace with your vendor's DSP-inference attribute (Intel `multstyle`, Gowin `syn_dspstyle`) |
| [`credit_based_shaper.sv:115-116`](../../hdl/ieee8021q/ts/credit_based_shaper.sv#L115-L116) | `(* dont_touch = "true" *)` on the slope registers | keeps regs named for the multicycle constraint (Section 4.5) | generic attribute, widely honored (Synplify/Quartus accept it) | keep; re-express the paired multicycle constraint in your SDC |
| [`hdl/common/eth_event_counter/ethernet_events.sv:60-68`](../../hdl/common/eth_event_counter/ethernet_events.sv#L60-L68) | `(* mark_debug = "true" *)` on RMON counters | Vivado ILA probe hint | ignored | keep or delete |
| [`hdl/milan/milan_datapath.sv:1781`](../../hdl/milan/milan_datapath.sv#L1781), [`milan_top.sv:303`](../../hdl/milan/milan_top.sv#L303), `cdc_pulse.sv`, `cdc_handshake.sv`, `ptp_csr_sync.sv` | `(* ASYNC_REG = "TRUE" *)` on CDC synchronizer FFs | placement + no-SRL-inference for metastability hardening | Xilinx/Intel-recognized; others ignore it | add the equivalent vendor constraint on the same registers (Section 4.5) - functionally safe either way |
| [`hdl/milan/milan_top.sv:132-134`](../../hdl/milan/milan_top.sv#L132-L134) (Zynq top only) | MAC params `MAC_TARGET="XILINX"`, `MAC_IODDR_STYLE="IODDR"`, `MAC_CLK_STYLE="BUFR"` | selects Series-7 DDR I/O cells inside the verilog-ethernet MAC | set `TARGET="GENERIC"` (sim) or your vendor's value | only relevant if you use `milan_top` + verilog-ethernet; `milan_datapath` has no MAC at all |
| [`hdl/milan/milan_dma_wrapper.v:200-201`](../../hdl/milan/milan_dma_wrapper.v#L200-L201) (Zynq wrapper only) | MDIO tristate is *inferred* (`t ? 1'bz : o`) - no `IOBUF` primitive | Vivado infers IOBUF | every toolchain infers its pad tristate | nothing |

Everything else in `hdl/` is plain synthesizable SystemVerilog
(`default_nettype none`, 64-bit AXIS, AXI4-Lite CSR).

### 2.1 Sources you must have present

Two code sources are not in the tree after a plain `git clone`:

1. **[`third_party/verilog-axis`](../../third_party/verilog-axis) is a git submodule** (public, HTTPS). Without it
   nothing elaborates - `axis_fifo`/`axis_demux` are instantiated by the
   classifier, queues and PTP buffers. Run:
   ```sh
   git submodule update --init third_party/verilog-axis
   ```
2. **The `external` submodule** (`fpga-avb-ethernet`) uses an SSH URL and is
   **not required**: no RTL in `hdl/` includes anything from it. Skip it (do
   not use `--recurse-submodules` over anonymous HTTPS; it will fail on this
   one).
3. **`eth_mac_1g_rgmii_fifo` (verilog-ethernet) has no in-tree source.** It is
   only instantiated by the Zynq-variant `milan_top.sv`. If you build that
   variant, vendor [verilog-ethernet](https://github.com/alexforencich/verilog-ethernet)
   yourself; if you build `milan_datapath` (the recommended boundary), you
   don't need it.

---

## 3. Clocking and reset requirements (vendor-independent contract)

The RTL receives clocks as plain inputs; **all clock generation is your
board layer's job**.

| Clock | Frequency | Used by | Notes |
|---|---|---|---|
| `axis_clk` | ~100 MHz (50-112.5 MHz proven on silicon) | whole datapath, AXI4-Lite CSR | 64-bit AXIS @ 100 MHz = 6.4 Gb/s >> 1 GbE, so there is headroom to run it slower; the CBS block is the critical path at 100 MHz (Section 4.5) |
| `gtx_clk` | 125 MHz | PTP PHC + MAC-RX timestamp capture | fixed by 1 GbE; the LiteX build ties it to `axis_clk` (legal - the CDC is still exercised) |
| `gtx90_clk` | 125 MHz, 90° phase | RGMII TX clock forwarding (`milan_top` variant only) | only needed with an RGMII MAC that wants a phase-shifted TX clock |

Resets are synchronous, active-low (`axis_resetn`, `gtx_resetn`). All CDC
between the two domains is inside the RTL (`ptp_csr_sync`, `cdc_pulse`,
`cdc_handshake`, 2-FF speed sync) - you do not add CDC logic, only the
constraints in Section 4.5.

---

## 4. The per-board work list

### 4.1 Pins & I/O standards
Redo from your schematic. The Xilinx references to translate from:
`constraints/rgmii.xdc` (Zynq board: RGMII + MDIO pins, LVCMOS18) and the
`_io` table in [`sw/litex/platforms/alinx_ax7101.py`](../../sw/litex/platforms/alinx_ax7101.py) (AX7101: clk200, UART,
DDR3, GMII+RGMII PHYs, QSPI, LEDs - each pin annotated with its provenance).

### 4.2 Clock generation
Replace the Series-7 pieces with your vendor's:

| Function | Xilinx implementation here | Intel/Altera | Lattice ECP5 | Gowin | Microchip PolarFire |
|---|---|---|---|---|---|
| System PLL | `S7PLL` (`milan_soc.py`) / `clk_wiz` MMCM (`bd/milan-dma.tcl`) | IOPLL/ALTPLL | `EHXPLLL` | `rPLL` | `PF_CCC` |
| RGMII/GMII DDR I/O | `IDDR`/`ODDR` + `BUFG` ([`sw/litex/milan_rgmii.py`](../../sw/litex/milan_rgmii.py) - legacy) or the MAC's `IODDR_STYLE` | `ALTDDIO_IN/OUT` (GPIO IP) | `IDDRX1F`/`ODDRX1F` | `IDDR`/`ODDR` | `PF_IOD` |
| RX-clock centering | AX7101 avoids IDELAY entirely by capturing on the **inverted** RX clock (`BUFG(~rgmii_rxc)`); Zynq board uses PHY delay mode | delay chains or PHY-side delay (`rgmii-id`) | `DELAYF`/DQS logic or PHY-side | IODELAY or PHY-side | PHY-side recommended |
| DDR memory PHY | `A7DDRPHY` (LiteDRAM) | LiteDRAM supports Intel targets; or vendor EMIF | LiteDRAM ECP5 DDR3 PHY (well proven) | vendor DDR IP | vendor DDR IP |

If you go through LiteX (Section 6.1), LiteX's platform/CRG abstractions generate
most of this for you on Intel, Lattice and Gowin targets.

### 4.3 The MAC
Options, in order of least work:
1. **LiteX host: LiteEth** - what the AX7101 build uses (`MilanMAC` in
   `milan_soc.py`: `LiteEthPHYGMII` + `LiteEthMACCore` + store-and-forward
   FIFO + stream↔AXIS adapter). LiteEth has PHY backends for several vendors.
2. **Forencich verilog-ethernet** - `eth_mac_1g_rgmii_fifo` with
   `TARGET="GENERIC"`/vendor value; this is the `milan_top` pattern.
3. **Any vendor MAC** that can present 64-bit AXI-Stream (or a width you
   adapt) with `tkeep`/`tlast`, plus the config/status sideband
   (`o_mac_*`/`i_mac_*`, RMON event pulses) - the exact contract is in
   [Section 3 of INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md#3-source-files-and-includes).

### 4.4 The host CPU/DMA
- **LiteX** (recommended): the whole Zynq-PS role - RISC-V CPU, DDR
  controller, interconnect, the ring-DMA engines, IRQs - is already
  implemented board-agnostically in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py). See Section 6.1.
- **Your own SoC**: drive the AXI4-Lite CSR window + three 64-bit AXIS DMA
  streams yourself - contract in [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md).

### 4.5 Timing constraints (translate, don't skip)
The XDC content to re-express in your SDC/LPF/CST:

1. **Asynchronous clock groups** between `axis_clk`, `gtx_clk` (+ MAC RX
   clock if RGMII): `constraints/clocks.xdc` does it with
   `set_clock_groups -asynchronous`. The design's CDC structures make this
   safe; without the constraint your tools will chase false cross-domain
   paths.
2. **CDC synchronizer hardening** - wherever your vendor has an equivalent of
   `ASYNC_REG` (Intel: `-name SYNCHRONIZER_IDENTIFICATION`; Synplify honors
   `syn_preserve`/`ASYNC_REG`), apply it to the `*_meta`/`*_sync` register
   pairs listed in Section 2.
3. **CBS slope multicycle path** - the credit-based shaper computes wide
   constant divides of quasi-static config (reprogrammed only by `tc cbs`,
   then held for millions of cycles). At 100 MHz this is the design's true
   critical path, and the build declares it multicycle (see
   `add_milan_datapath()` in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py), which emits
   `set_multicycle_path 4 -setup / 3 -hold` onto
   `*idle_slope_per_cycle_r_reg*` / `*send_slope_per_byte_r_reg*`).
   Re-express this in your flow, or run `axis_clk` at ≤ ~66 MHz where it
   closes without help.
4. **False paths across the MAC FIFO reset synchronizers** (only with the
   verilog-ethernet MAC; see `constraints/clocks.xdc`).

---

## 5. Proving it: the open-toolchain portability check

[`syn/yosys/`](../../syn/yosys) machine-checks vendor-neutrality on every push-worthy change:

```sh
git submodule update --init third_party/verilog-axis   # required first
cd syn/yosys
make          # sv2v -> Yosys generic `synth` + `hierarchy -check`, every top -> PASS
              # (the `tops` array in syn/yosys/run.sh is authoritative)
make ecp5     # map every top to a real non-Xilinx device (Lattice ECP5)
```

`hierarchy -check` fails on any undefined/vendor primitive, so PASS means
"fully mapped to generic cells". The `ecp5` target then proves a concrete
non-Xilinx mapping (e.g. `tcam` → ~1.7k `TRELLIS_FF`).

Covered (the [`syn/yosys/run.sh`](../../syn/yosys/run.sh) `tops` array is authoritative): every datapath leaf + `milan_csr` + the flat wrappers +
the vendored Forencich cores + **`milan_datapath` itself** (which pulls in
`ptp_ts_top`/`ptp_ts_core` hierarchically).
**Not covered:** `milan_top` (needs the RGMII SelectIO MAC + PS).
(`avtp_stream_parser` was previously an open gap here; it is now CLOSED -
integrated in the `milan_datapath` top, so the yosys flow covers it
hierarchically.)

Note: Yosys proves *synthesizability*, not timing. Off-Xilinx timing closure
of the full SoC at 100 MHz has not been attempted on silicon; the CBS
multicycle situation (Section 4.5) is the first thing to watch.

### 5.1 Fully open P&R (Yosys + nextpnr)
The datapath maps to ECP5 cells today (`make ecp5`), so a
Yosys+nextpnr-ecp5 flow for the *datapath* is realistic. The full **SoC** via
LiteX on an ECP5 board (e.g. with `--toolchain trellis`) is the natural route -
LiteX supports it - but it has **not been exercised in this repo**; the only
silicon-proven builds are Vivado ones (AX7101). Treat open P&R as supported-
by-design, unproven-in-practice.

---

## 6. Recommended porting routes

### 6.1 Route A - stay on LiteX, swap the board (least work)
1. Write a LiteX platform file for your board (copy
   [`sw/litex/platforms/alinx_ax7101.py`](../../sw/litex/platforms/alinx_ax7101.py), replace the `_io` table, part and
   toolchain - e.g. `toolchain="trellis"` for ECP5, `"oxide"` for Nexus,
   Intel/Gowin equivalents).
2. Adapt `_CRG` in `milan_soc.py`: your PLL class instead of `S7PLL`, drop
   `S7IDELAYCTRL` if your DDR/PHY path doesn't need it.
3. Pick the LiteDRAM PHY for your board's memory, or start DRAM-less
   (`--integrated-main-ram`) to bring up CPU+CSR first.
4. Pick a LiteEth PHY backend for your board's Ethernet PHY (GMII/RGMII/MII).
5. Build with `--no-compile-gateware` first (elaboration + gateware export
   runs with **no vendor tools at all**), then with your toolchain.
6. Keep the bring-up order that worked here: CPU boots → CSR read of
   ID = `"MILN"` at offset `0x0` (milestone M-A2) → MAC attach → DMA attach.
   [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md) is the worked example
   of exactly this sequence on a new board.

### 6.2 Route B - your own SoC/host
Integrate `milan_datapath` directly: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
has the port-by-port contract, minimum-viable attach, and the DMA/MAC
attach order. The Zynq flow (`milan_top` + `bd/`) is the in-repo example of a
non-LiteX host.

---

## 7. Port-readiness checklist

- [ ] `git submodule update --init third_party/verilog-axis`
- [ ] `cd syn/yosys && make` passes on your checkout (sanity: sources complete)
- [ ] Platform/pin file written for your board (Section 4.1)
- [ ] PLL/CRG produces `axis_clk` (and 125 MHz if the MAC needs it) (Section 4.2)
- [ ] MAC chosen and its AXIS width/sideband adapted (Section 4.3)
- [ ] DDR PHY chosen (or DRAM-less bring-up) (Section 4.4)
- [ ] SDC equivalents written: async clock groups, CDC attributes, CBS
      multicycle (Section 4.5)
- [ ] CSR ID readback (`"MILN"` @ base+0x0) plan for first silicon (M-A2)
- [ ] Read the [current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md)
      and [recurring defect patterns](../limitations/RECURRING_DEFECT_PATTERNS.md)
      before committing to targets

---

*Related: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) ·
[OPEN_SOURCE_MIGRATION.md (archived)](../../historical_now_obsolete/integration/OPEN_SOURCE_MIGRATION.md) (how the RTL got
vendor-neutral) · [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md) (worked
board port) · [../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) (the LiteX host in
depth) · [../testing/TESTING.md](../testing/TESTING.md) (what to run after every
step).*
