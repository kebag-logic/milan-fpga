# milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA

A Milan-profile TSN/AVB network interface implemented as a **fully-FPGA softcore
system** (dual-hart SMP VexiiRiscv RV64IMA Linux SoC — NaxRiscv retained as a pure-NIC
option — + TSN datapath on an Alinx AX7101 / Artix-7), now evolving toward a **4-port
AVB switch**. Verified on silicon: ring-DMA networking at line-rate ingest, hardware
802.1Qav CBS, PTP timestamping, ADP advertisement, QSPI flash-boot (zero-upload), and
the 2026-07 **>500 Mbit/s campaign** (TCP TX crossed 500 Mbit/s @ MTU 1500 on the
100 MHz 2-core SoC). Current RX/TX numbers live in the measured ledger —
[CHANGELOG.md](CHANGELOG.md) + [docs/findings/](docs/findings/README.md); any number
quoted elsewhere is a dated snapshot.

The TSN datapath RTL is **vendor-neutral** — no Xilinx primitives, machine-checked by
the [Yosys/ECP5 portability flow](syn/yosys/README.md) — and building it without
Vivado, or on a non-Xilinx board, is a supported, documented path.

**📚 Start with the [documentation index](docs/README.md)** — curated reading
paths (understand the system / integrate into your SoC / port off-Vivado /
board bring-up / tests / driver & ABI) plus a [glossary](docs/GLOSSARY.md).

Quick jumps:

| I want to… | Go to |
|---|---|
| Understand the whole system | [docs/overview/FULL_FPGA_SOLUTION.md](docs/overview/FULL_FPGA_SOLUTION.md) |
| Integrate the datapath into my own SoC | [docs/integration/INTEGRATION_GUIDE.md](docs/integration/INTEGRATION_GUIDE.md) |
| **Build without Vivado / port to a non-Xilinx board** | [docs/integration/PORTING_GUIDE.md](docs/integration/PORTING_GUIDE.md) |
| Understand the LiteX SoC (`sw/litex/`) | [docs/litex/LITEX_SOC.md](docs/litex/LITEX_SOC.md) |
| Build & boot the board | [sw/README.md](sw/README.md) → [docs/integration/QSPI_FLASHBOOT.md](docs/integration/QSPI_FLASHBOOT.md) |
| Program against the registers | [docs/reference/REGISTER_MAP.md](docs/reference/REGISTER_MAP.md) |
| Run the verification suites | [docs/testing/TESTING.md](docs/testing/TESTING.md) |
| Know the limitations & known issues | [docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md](docs/limitations/KNOWN_ISSUES_AND_LIMITATIONS.md) |
| See the direction + measured scoreboard | [docs/overview/AVB_SWITCH_DIRECTION.md](docs/overview/AVB_SWITCH_DIRECTION.md) |

## Running the testbenches

Self-checking Verilator harnesses — 17 suites, no vendor tools needed
(`verilator >= 5.0` + C++17; the full verification map is
[docs/testing/TESTING.md](docs/testing/TESTING.md)):

```sh
git submodule update --init third_party/verilog-axis   # required once
cd tb/verilator
for d in */ ; do ( cd "$d" && make clean >/dev/null && make ) || exit 1; done
# or a single suite:
cd tb/verilator/<suite>   # e.g. cbs, milan_dp, controller_rate …
make                      # builds and runs; exit 0 = PASS
```

Device portability (Yosys generic + Lattice ECP5, 18 tops):

```sh
cd syn/yosys && make && make ecp5
```

Legacy Vivado-xsim testbenches (waveform work only — see
[tb/itests/README.md](tb/itests/README.md) and
[tb/utests/](tb/utests/802_1q_traffic_shaper/README.md)):

```sh
cd tb/itests/ptp_timestamp
vivado -mode tcl -source tb_ptp_ts_top.tcl
```

## Developers

* [Cemal Dogan](https://github.com/cemaldogann)
* [Oguz Kahraman](https://github.com/OguzKahramn)

### Maintainers

* [Alexandre Malki](https://github.com/Mister-M-alt)
