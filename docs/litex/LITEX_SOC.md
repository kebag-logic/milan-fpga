# LiteX bare-metal SoC

`sw/litex/milan_soc.py` builds the supported target: a cacheless RV32
VexiiRiscv control CPU, LiteEth MAC/PHY glue, optional DDR3 and QSPI, the Milan
fabric datapath, board audio I/O, and one AXI-Lite CSR bridge. The target runs
the firmware in `sw/firmware/milan_baremetal`; no operating system is part of
the product image.

<!-- solution-cpu-contract:start -->
| Invocation | CPU | Harts | XLEN | Firmware | L2 bytes | Datapath clock |
|---|---|---:|---:|---|---:|---:|
| CLI defaults | `vexiiriscv` | `1` | `32` | `baremetal` | `unset` | `unset` |
| `deploy.sh` | `vexiiriscv` | `1` | `32` | `baremetal` | `0` | `50 MHz` |
<!-- solution-cpu-contract:end -->

## Contents

- **[1. Boundary](#1-boundary)** — The four product interfaces and the division between fabric packet work and CPU control work.
- **[2. Components](#2-components)** — Clocking, MAC adaptation, the RV32 control CPU, media I/O, developer alternatives, and QSPI boot.
- **[3. Register access](#3-register-access)** — The AXI-Lite CSR bridge, address window, and bounded firmware access model.
- **[4. The flags that are not optional](#4-the-flags-that-are-not-optional)** — The explicit release-shape arguments that prevent silent build defaults.
- **[5. Build and elaborate](#5-build-and-elaborate)** — Commands for generating and checking the selected SoC without conflating elaboration with implementation.
- **[6. Verification](#6-verification)** — The builder, source, RTL, UART, and external-wire checks for the SoC integration.
- **[7. Reproducibility - versions](#7-reproducibility---versions)** — The pinned tools, submodules, configuration, and generated artifacts needed to reproduce a candidate.

## 1. Boundary

The SoC connects four product surfaces:

- the MAC-facing 64-bit packet stream;
- the AXI-Lite Milan CSR window;
- the descriptor-memory read port used by the protocol processor after the
  firmware verifies and copies the paired AEM image;
- physical I2S/TDM capture and render pins.

Packet generation, reception, time synchronization, and media routing remain
in fabric. The CPU configures policy and identity over CSRs and exposes a
small UART command set; it is not a packet relay.

## 2. Components

### 2.1 Clock/reset generation

`_CRG` owns the board input clock, system clocks, Ethernet clocks, reset
synchronization, and the audio-MMCM controls exported by `milan_datapath`.
When `--milan-clk-freq` differs from `sys`, explicit stream and AXI-Lite clock
crossings isolate the domains.

### 2.2 MilanNIC and MilanMAC

`MilanNIC` calls the single `add_milan_datapath()` integration helper, which
registers the complete transitive RTL source set and wires the fabric boundary.
`MilanMAC` adapts LiteEth's stream convention to the 64-bit wire-order boundary
and supplies the RMON events consumed by the CSR block.

### 2.3 Bare-metal control CPU

The product profile selects one RV32I VexiiRiscv hart in machine mode without
MMU or caches. Firmware initializes the paired descriptor image, establishes
the PHC epoch, enables the protocol/media fabric, and provides diagnostic UART
commands. Wider developer CPU configurations are not release images.

### 2.4 Fabric media I/O

Capture sources feed the AAF packetizer through the capture map. Accepted AAF
listeners feed the render map and physical I2S/TDM outputs. These paths never
round-trip samples through CPU memory.

### 2.5 CPU: VexiiRiscv and developer alternatives

Release configurations use VexiiRiscv RV32. A developer may elaborate another
LiteX-supported core for simulation, but that does not change the product
firmware contract and is not accepted as release evidence.

### 2.6 QSPI flash boot

The generated layout pairs the offset-zero FPGA image with the raw AEM image.
The firmware validates length and CRC before copying the AEM image to the
reserved descriptor window and enabling the entity. Persistent updates use
`deploy.sh flash-pair`, which verifies the installed identity and writes the
new AEM image before committing the new bitstream. See
[`../integration/QSPI_FLASHBOOT.md`](../integration/QSPI_FLASHBOOT.md).

## 3. Register access

The Milan CSR window is the only runtime control contract. Its authoritative
offsets and ownership rules are in
[`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md). Generated
`csr.csv` files describe the enclosing LiteX address map for the exact build.

## 4. The flags that are not optional

Release recipes explicitly select:

- `--software-profile baremetal`;
- `--fabric-gptp`, making fabric the sole time owner;
- the board, Ethernet port, fabric/audio clock, stream count, and physical
  audio interface from the end-station configuration;
- `--with-spiflash --flashboot baremetal` for persistent images;
- RV32 single-hart CPU parameters.

The builder and sweep-shape gate compare the effective command line with the
selected YAML configuration before a build launches. The direct fabric-gPTP
option-OFF shape exists only for verification and is not flashable.

## 5. Build and elaborate

Use `sw/litex/build.sh <config>` for named configurations. The builder emits
the AEM image and fabric-gPTP ROM from the same YAML input. For a quick source
closure check, run `python3 scripts/check_soc_sources.py`; for full release
instructions see [`../integration/BUILDING.md`](../integration/BUILDING.md).

The fixed AX7101 recipe remains directly inspectable and runnable:

```sh
cd sw/litex
./deploy.sh build --dry-run
./deploy.sh build
```

## 6. Verification

The required layers are SoC elaboration, builder tests, source-closure gates,
Verilator integration suites, Yosys synthesis, placed timing/utilization, and
the UART plus external-wire board campaign. Commands are collected in
[`../testing/RUNNING_TESTS.md`](../testing/RUNNING_TESTS.md).

## 7. Reproducibility - versions

Record the superproject commit, both processor pins, end-station YAML, LiteX
and LiteEth revisions, CPU core revision, Python environment, FPGA part and
speed grade, and synthesis-tool version with every candidate. Preserve the
generated build plan, source manifest, timing/utilization reports, bitstream
hash, AEM hash, UART transcript, and packet capture.
