# milan-fpga — IEEE 1722 / 1722.1 / Milan v1.2 on FPGA

A Milan-profile TSN/AVB network interface implemented as a **fully-FPGA softcore
system** (dual-hart SMP VexiiRiscv RV64IMA Linux SoC — NaxRiscv retained as a pure-NIC
option — + TSN datapath on an Alinx AX7101 / Artix-7), now evolving toward a **4-port
AVB switch**. Verified on silicon: ring-DMA networking at line-rate ingest, hardware
802.1Qav CBS, PTP timestamping, ADP advertisement, QSPI flash-boot, and TCP
**RX 46.5 / TX ~59 Mbit/s** @ MTU 1500 on the 100 MHz 2-core SoC (2026-07-07 campaign;
[HW-GRO/RSC](docs/fpga/HW_GRO_RSC.md) toward ≥200 Mbit/s in flight — phases A+B sim-verified).

**📚 Start with the [documentation index](docs/README.md)** — it has curated reading
paths (understand the system / project direction / board bring-up / datapath
debugging / driver & ABI) plus a [glossary](docs/GLOSSARY.md) of every term used.

Quick jumps:

| I want to… | Go to |
|---|---|
| Understand the whole system | [docs/FULL_FPGA_SOLUTION.md](docs/overview/FULL_FPGA_SOLUTION.md) |
| See the direction + measured scoreboard | [docs/AVB_SWITCH_DIRECTION.md](docs/overview/AVB_SWITCH_DIRECTION.md) |
| Build & boot the board | [docs/QSPI_FLASHBOOT.md](docs/integration/QSPI_FLASHBOOT.md) |
| Program against the registers | [docs/REGISTER_MAP.md](docs/reference/REGISTER_MAP.md) |
| Run the verification suites | [tb/verilator/README.md](tb/verilator/README.md) |

## Running the testbenches

Self-checking Verilator harnesses (no vendor tools needed):

```sh
cd tb/verilator/<suite>   # e.g. cbs, classifier, controller_rate, milan_dp …
make                      # builds and runs; exit 0 = PASS
```

Legacy Vivado itests:

```sh
cd tb/itest/<itest_name>
vivado -mode tcl -source <test_name>.tcl
```

## Developers

* [Cemal Dogan](https://github.com/cemaldogann)
* [Oguz Kahraman](https://github.com/OguzKahramn)

### Maintainers

* [Alexandre Malki](https://github.com/Mister-M-alt)
