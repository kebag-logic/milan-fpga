# The LiteX SoC - `sw/litex/` in depth

`sw/litex/milan_soc.py` (~3600 lines) is "the LiteX line of code": the fully-
FPGA host that replaced the Zynq PS. It builds a RISC-V Linux SoC on the
Alinx AX7101 (Artix-7 `xc7a100t`) with the Milan TSN datapath attached as a
real RTL instance, the ring-DMA engines, the LiteEth GMII MAC, DDR3, QSPI
flash-boot and the telemetry block. This page maps the whole directory and
the SoC's anatomy; the step-by-step build/boot recipe stays in
[`sw/README.md`](../../sw/README.md) and
[../integration/QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md).

---

## 1. Directory map - what each file is

| File | Role | Audience |
|---|---|---|
| `milan_soc.py` | **The SoC.** CRG, CPU (VexiiRiscv/NaxRiscv), DDR3, LiteEth MAC, Milan datapath attach, ring-DMA engines, IRQs, QSPI flash-boot layout, CLI | everyone |
| `platforms/alinx_ax7101.py` | The board: pins (clk200, UART, GMII "e1" + RGMII "e2" RTL8211E PHYs, DDR3 2×MT41J256M16 = 512 MB, N25Q128 QSPI, LEDs), `xc7a100t-fgg484-2`, openFPGALoader programming | board porters |
| `deploy.sh` | Turnkey `build / load / flash / flash-images / console` for the AX7101; **encodes the known-good flag set** (§4) | everyone |
| `milan_sim.py` | Verilator **SoC-level sim**: boots the LiteX BIOS on a softcore with the real `milan_datapath` at `0x9000_0000`, proves the CPU⇄CSR path (reads ID `"MILN"`, milestone M-A2) | everyone |
| `patches/` | LiteX-ecosystem patches + `apply.sh` (§6) | everyone |
| `test_ring_dma.py` (+ `test_ring_bd.py`, `test_ring_tx.py`, `test_ring_writeback.py`, `test_rx_steer.py`, `test_tx_bd.py`) | **Migen behavioral sims** of the DMA engines (self-checking, print `ALL PASS`); `test_ring_dma.py` is the base harness the others import | DMA developers |
| `tools_*.c` (8 files) | On-target microbenchmarks compiled for the board (`lat_mem_rd`, `mapbench`, `recv_ring`, `recv_spin`, `recv_trunc`, `recv_zc`, `tcp_blast`, `wakebench`) - the instruments behind the perf findings | perf work |
| `phase0_measure.sh` | On-board telemetry/iperf sweep script (busybox `devmem`); CSR addresses are build-specific - regenerate before reuse | perf work |
| `poll_cost_model.py` | Analytical model projecting RX pps from measured sweeps | perf work |
| `evidence/` | Captured proof logs (sim + on-silicon `hw_*` logs, the M-A3 write-up). `hw_naxriscv_reads_MILN.log` records the **known-good LiteX commit `a1e1c36`** (§7) | reviewers |
| `milan_rgmii.py` | **Legacy, unused.** An RX-clock-inverted Series-7 RGMII PHY variant from before the board was confirmed GMII-wired; nothing imports it. Kept for reference only | - |

---

## 2. SoC anatomy (`milan_soc.py`)

### 2.1 Clocking (`_CRG`)
`S7PLL` takes the board's 200 MHz to `sys` (100 MHz for the full build - DDR3
requires it), plus `sys4x`/`sys4x_dqs` + 200 MHz `idelay`/`S7IDELAYCTRL` for
the `A7DDRPHY`. With `--milan-clk-freq` the Milan datapath gets its **own
slower clock domain** (`cd_milan`, 50 MHz in the deployed build): the dense
CBS/TCAM/PTP logic leaves the 100 MHz timing budget while a 64-bit datapath
at 50 MHz (3.2 Gb/s) still outruns 1 GbE. The CSR bus crosses via
`AXILiteClockDomainCrossing`, each DMA/MAC AXIS lane via a
`stream.ClockDomainCrossing` FIFO, the IRQ via `MultiReg`.

### 2.2 The datapath attach (`MilanNIC` / `add_milan_datapath()`)
Instantiates `milan_datapath` as **real RTL** (no black box) from the curated
`_MILAN_DATAPATH_SOURCES` list (the same file set the `tb/verilator/milan_dp`
harness and `syn/yosys` use, so the build can't drift from what is verified).
The CSR window is an AXI4-Lite slave at `MILAN_CSR_BASE = 0x9000_0000`
(64 KB, uncached-IO region on these CPUs; the Zynq build used
`0x43C0_0000` - only the base differs, offsets are the ABI in
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md)). It also emits
the CBS slope **multicycle constraint** on Xilinx parts - a porting-relevant
detail explained in [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §4.5.
Interrupts: an `EventManager` with four level sources (`tx`/`rx`/`ts`/`csr`)
folded into one PLIC line - matching the driver's four `interrupt-names`
(the DT encodes the aggregation; see [`sw/dts/README.md`](../../sw/dts/README.md)).

### 2.3 The DMA (`MilanDMA`)
TX is a `RingDMAReader` (native AXI bursts, DRAM → datapath), RX a
`RingDMAWriter` (always-ready ingress, datapath → DRAM, completion-queue
depth 32), TS a `WishboneDMAWriter`. Masters attach to the CPU's **coherent**
`dma_bus` when present - which is why `--coherent-dma` is mandatory (§4).
An optional second RX queue (`--rx-queues 2`) adds an `RxSteer` classifier.
Endianness is `"big"` on purpose: memory order == wire order, so the CPU
never byte-swaps. The BD-format/zero-copy/checksum evolution of these
engines is chronicled in [../fpga/CPPI_DMA_REDESIGN.md](../fpga/CPPI_DMA_REDESIGN.md)
and the [findings log](../findings/README.md).

### 2.4 The MAC (`MilanMAC`)
`LiteEthPHYGMII` + `LiteEthMACCore` (preamble/CRC/padding) + a
store-and-forward `PacketFIFO` + a thin stream↔AXIS adapter. The AX7101's
RTL8211E port is wired **GMII** (not RGMII - see
[../integration/BOARD_PORTING_AX7101.md](../integration/BOARD_PORTING_AX7101.md) §3),
and the TX clock is forwarded **inverted** (`--gtx-tx-invert`, via the LiteEth
patch, §6) because edge-aligned launch off IOB-packed FFs was hold-marginal at
the PHY (25-40 % corrupt frames without it). The Milan datapath keeps all
packet intelligence; the MAC does L1/framing only.

### 2.5 CPU: VexiiRiscv and NaxRiscv - read this before building
`--cpu {naxriscv,vexiiriscv}`; **the CLI default is `naxriscv`**, and
`deploy.sh` does not override it.

* **VexiiRiscv** (`--cpu vexiiriscv`, forced `linux` variant, RV64IMASU,
  sv39) is the core behind the dual-hart SMP Linux results on the project
  scoreboard (`--cpu-count 2`); the perf-campaign docs
  ([findings](../findings/README.md)) all measure this configuration.
* **NaxRiscv** (default, RV64GC) is the earlier bring-up core, retained as a
  pure-NIC option and used by `milan_sim.py`. `--with-fpu`/`--xlen` behave
  as documented in the source (the FPU needs both the toolchain arch *and*
  the scala flags - handled for you).

So: to reproduce the published Linux/perf results build
`--cpu vexiiriscv --cpu-count 2`; a bare `deploy.sh build` gives you a
NaxRiscv SoC. This asymmetry is tracked in
[KNOWN_ISSUES_AND_LIMITATIONS.md](../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md).

### 2.6 QSPI flash-boot
`FLASHBOOT_LAYOUT`/`FLASHBOOT_MANIFESTS` in `milan_soc.py` are the **single
source of truth** for the 16 MB N25Q128 layout (kernel @ `0x00_0000` ≤8.5 MiB,
opensbi @ `0x88_0000`, dtb @ `0x90_0000`, rootfs @ `0x94_0000`); the build
writes `flashboot_layout.json` so gateware and `deploy.sh flash-images` never
drift. Guide: [../integration/QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md).

---

## 3. Building

```sh
cd sw/litex
./milan_soc.py --all-blocks --coherent-dma --milan-clk-freq 50e6 \
               --gtx-tx-invert --timing-opt --cpu vexiiriscv --cpu-count 2
               # add --build to run Vivado P&R; without it, elaboration +
               # gateware/Verilog export runs with NO vendor tools
./milan_soc.py ... --build     # Vivado bitstream
./milan_soc.py ... --load      # openFPGALoader -c ft232 (JTAG -> SRAM)
```

Or just `./deploy.sh` (build + load + console) / `./deploy.sh load` etc. -
`deploy.sh` carries the verified `MILAN_OPTS` and the JTAG/console device
identification for the AX7101.

Vivado is currently the **only P&R backend wired up for this board** (the
platform is instantiated with `toolchain="vivado"`). Elaboration-only runs
need no vendor tools, and re-targeting to another board/toolchain is Route A
in [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §6.1.

## 4. The flags that are not optional

| Flag | Why it is required |
|---|---|
| `--coherent-dma` | **NOT implied by `--all-blocks`.** Without it the DMA masters bypass the CPU's snooping `dma_bus`: RX buffers are never CPU-visible (all-zero skbs, every frame dropped) and TX reads stale data (garbage dst MAC). Hardware-confirmed 2026-07-04 |
| `--gtx-tx-invert` | AX7101/RTL8211E GMII: edge-aligned TX launch is hold-marginal → 25-40 % corrupt frames; inverted (mid-bit) sampling → 0. Needs the LiteEth patch (§6) |
| `--milan-clk-freq 50e6` | Lifts the dense datapath off the 100 MHz sys budget (DDR3 pins sys at 100 MHz); without it the CBS block is the critical path |
| `--all-blocks` | NIC+DMA+MAC+DDR3 in one build; implies `--with-spiflash` |

## 5. Simulation (`milan_sim.py`)

```sh
./milan_sim.py --non-interactive     # Verilator: BIOS boots, reads "MILN"
```

This is the SoC-level layer of the verification stack (RTL harnesses below
it, silicon above it) - see [../testing/TESTING.md](../testing/TESTING.md) and
[../testing/SIMULATION.md](../testing/SIMULATION.md). The sim SoC uses
NaxRiscv and the same `add_milan_datapath()` as the board build.

## 6. Patches (`patches/`)

Applied **in place** to the active Python env's LiteX/LiteEth trees by
`patches/apply.sh` (idempotent; **re-run after every LiteX update**):

| Patch | What it does |
|---|---|
| `0001-milan-linux-flashboot.patch` | Adds the `linux_flashboot` BIOS boot method (runs before serialboot; inert without the `MILAN_FLASHBOOT_*` constants that `--with-spiflash` emits) |
| `0002-liteeth-gmii-tx-clk-invert.patch` | Adds `tx_clk_invert` to `LiteEthPHYGMII` → the `--gtx-tx-invert` flag |
| `0002-vexiiriscv-l2-depth-args.patch` | Exposes VexiiRiscv L2 depth/geometry args used by the perf campaign's L2 experiments. **Not applied by `apply.sh`** - apply manually when building VexiiRiscv with non-default L2 |

Details and re-diff instructions: [`patches/README.md`](../../sw/litex/patches/README.md).

## 7. Reproducibility - versions

There is currently **no pinned requirements file**; patches are diffed
against LiteX `master`. Known-good anchors, recorded from working builds:

* LiteX git `a1e1c36` (from `evidence/hw_naxriscv_reads_MILN.log` - the
  on-silicon M-A2 run).
* openFPGALoader ≥ v1.1.1; Vivado with Artix-7 support for `--build`.
* `verilog-axis` submodule pinned by the gitlink
  (`git submodule update --init third_party/verilog-axis` - required for any
  elaboration).

If `apply.sh` fails after a LiteX upgrade, the patch context moved - re-diff
per `patches/README.md`. This gap (and the plan to pin properly) is tracked
in [KNOWN_ISSUES_AND_LIMITATIONS.md](../limitations/KNOWN_ISSUES_AND_LIMITATIONS.md).

## 8. The Migen DMA sims and on-target tools

The `test_*.py` sims are the regression net for the DMA engines - run them
after touching `RingDMAReader`/`RingDMAWriter`/BD logic:

```sh
cd sw/litex
python3 test_ring_dma.py      # base ring engines
python3 test_ring_bd.py       # BD-mode engines (largest suite)
python3 test_ring_tx.py  ; python3 test_ring_writeback.py
python3 test_rx_steer.py ; python3 test_tx_bd.py
```

Each prints `PASS <name>` per test and `ALL PASS` at the end (no pytest;
plain interpreter from your LiteX venv). The `tools_*.c` benchmarks are
cross-compiled and run **on the board**; they are research instruments, not
part of any build - their measurements live in the
[findings log](../findings/README.md).

---

*Related: [../integration/INTEGRATION_GUIDE.md](../integration/INTEGRATION_GUIDE.md) ·
[../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) ·
[../integration/QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md) ·
[../integration/AXIS_CORES_ON_NAXRISCV.md](../integration/AXIS_CORES_ON_NAXRISCV.md)
(the three-plane attach model) · [../testing/TESTING.md](../testing/TESTING.md).*
