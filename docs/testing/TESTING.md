# Testing & verification - the complete map

Every layer of verification in this repo, what it proves, and the exact
command to run it. This page is the map; the per-layer detail stays next to
the tests ([`tb/verilator/README.md`](../../tb/verilator/README.md),
[SIMULATION.md](SIMULATION.md), [RUNNING_TESTS.md](RUNNING_TESTS.md)) and the
protocol-level coverage contract is
[PROTOCOL_VALIDATION_MATRIX.md](PROTOCOL_VALIDATION_MATRIX.md).

> **Suite counts in prose go stale.** The authoritative count is the
> directory listing (`ls tb/verilator/` - **17 suites** as of 2026-07). If a
> doc and the tree disagree, the tree wins.

## 0. Prerequisites

| Layer | Needs |
|---|---|
| Verilator harnesses | `verilator >= 5.0`, a C++17 compiler, **and** `git submodule update --init third_party/verilog-axis` (five suites elaborate Forencich cores) - no vendor tools |
| Yosys portability | `yosys` + [`sv2v`](https://github.com/zachjs/sv2v) on `PATH` + the same submodule |
| Migen DMA sims / SoC sim | a LiteX Python environment ([../litex/LITEX_SOC.md](../litex/LITEX_SOC.md) §7) |
| Legacy utests/itests | Vivado (xsim); `tb/avtp_packet_gen_sv` needs Modelsim/Questa |

## 1. Verilator RTL harnesses - `tb/verilator/` (the live regression)

Self-checking, exit `0` = PASS:

```sh
cd tb/verilator
for d in */ ; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
```

Per-suite DUT/what-it-proves table: [`tb/verilator/README.md`](../../tb/verilator/README.md).
The 17 suites: `adp adp_tx avtp_stream cbs cdc classifier cls controller_rate
csr datapath milan_dp ptp ptp_sync queues rx_filter shaper_core tcam`.
Highlights: `milan_dp` drives the **whole `milan_datapath` wrapper** (the
LiteX integration boundary - CSR ID read, classifier programming, byte-exact
TX/RX); `controller_rate` is the gating regression born from the
[CBS datapath bug](../findings/CBS_DATAPATH_BUG.md); `cbs`/`ptp` check
arithmetic against independent reference models (10⁴-10⁵ checks each).

## 2. Migen DMA-engine sims - `sw/litex/test_*.py`

Behavioral sims of the ring-DMA/BD engines that live in `milan_soc.py`
(the layer the RTL harnesses cannot see, and the SoC sim is too slow to
sweep). Self-checking (`ALL PASS`):

```sh
cd sw/litex
for t in test_ring_dma test_ring_bd test_ring_tx test_ring_writeback \
         test_rx_steer test_tx_bd; do python3 $t.py || exit 1; done
```

## 3. SoC-level simulation - `sw/litex/milan_sim.py`

Boots the real LiteX BIOS on the softcore with the real `milan_datapath`
mapped at `0x9000_0000`, over Verilator - proves the CPU⇄CSR path end to end
(milestone M-A2: BIOS reads ID `"MILN"`).

```sh
cd sw/litex && ./milan_sim.py --non-interactive
```

Detail (incl. what each of the three sim layers can and cannot catch):
[SIMULATION.md](SIMULATION.md).

## 4. Device-portability check - `syn/yosys/`

sv2v + Yosys `synth` + `hierarchy -check` over **18 tops** (fails on any
leftover vendor primitive), plus a concrete non-Xilinx mapping:

```sh
cd syn/yosys
make          # generic, device-independent
make ecp5     # Lattice ECP5 mapping
```

Proves synthesizability off-Xilinx, not behaviour (layer 1 does that) and
not timing. See [../integration/PORTING_GUIDE.md](../integration/PORTING_GUIDE.md) §5.

## 5. Legacy / auxiliary testbenches

| Where | What | Status |
|---|---|---|
| `tb/utests/` | Hand-written SystemVerilog TBs run under Vivado **xsim** (`vivado -mode tcl -source <tb>.tcl` where a `.tcl` exists) | **Superseded** for regression by the Verilator suites (`tb/utests/802_1q_traffic_shaper/README.md` maps old→new); waveform-inspection style, not exit-code gating |
| `tb/itests/` | xsim integration TBs: `ptp_timestamp/` (has `.tcl`, Vivado 2023.1) and `802_1q_traffic_shaper/` (**`.sv` only - no `.tcl` runner**) | Legacy; the Verilator `milan_dp`/`datapath` suites cover the integration seams without vendor tools |
| `tb/avtp_packet_gen_sv/` | Randomized AVTP packet-generator class library for the xsim TBs (Modelsim/Questa: `cd tb/avtp_packet_gen_sv/examples && do run.do`) | Development aid, in-progress |
| `tb/common/` | `axi_stream_driver.svh` - shared AXIS BFM class for the xsim TBs (the Verilator suites have their own C++ BFMs) | - |

## 6. On-silicon validation

Bring-up order and board procedures:
[../integration/BOARD_PORTING_AX7101.md](../integration/BOARD_PORTING_AX7101.md)
(CSR ID read → MAC → DMA), [../integration/QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md)
(boot), [RUNNING_TESTS.md](RUNNING_TESTS.md) (all-layers walkthrough incl.
board), and the in-fabric telemetry that instruments silicon runs:
[../fpga/pipeline-telemetry.md](../fpga/pipeline-telemetry.md). Protocol-by-
protocol validation status: [PROTOCOL_VALIDATION_MATRIX.md](PROTOCOL_VALIDATION_MATRIX.md).
Performance measurements on silicon are logged in the
[findings log](../findings/README.md) with their methodology.

## 7. Known gaps (kept honest)

* **No CI is wired up.** The harnesses are CI-ready (exit codes), but
  nothing runs them automatically - a `.github/workflows` running layers
  1, 2 and 4 is the obvious next step.
* **`avtp_stream_parser` has a Verilator suite but is not in the Yosys tops
  list** - its device portability is unchecked.
* `milan_top` (Zynq variant) is not coverable by the open flows (PS7 + the
  external verilog-ethernet MAC); its TSN content is covered via
  `milan_dp`.
* The legacy xsim TBs test pre-rework interfaces in places; trust the
  Verilator suites where they disagree.
* Check-counts quoted in READMEs are informational; the harnesses print
  their own counts at run time.

## Policy

Every DUT change ships with its harness update **in the same commit** - the
CSR harness is the executable form of
[../reference/REGISTER_MAP.md](../reference/REGISTER_MAP.md), and a new RTL
module is not "done" until it appears in layer 1 (and layer 4 unless it is
vendor-gated).
