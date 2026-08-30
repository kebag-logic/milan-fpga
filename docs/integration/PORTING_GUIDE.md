# Porting guide

Port the LiteX board shell around the vendor-neutral `milan_datapath`; do not
fork the protocol/media RTL.

## Contents

- **[1. Porting layers](#1-porting-layers)** — Which Milan, MAC, audio, and board-shell pieces are reusable and which must be remapped.
- **[2. What is and is not Xilinx-specific in the RTL - the full inventory](#2-what-is-and-is-not-xilinx-specific-in-the-rtl---the-full-inventory)** — The vendor-neutral RTL boundary and the board resources that stay toolchain-specific.
- **[3. Clocking and reset requirements - vendor-independent contract](#3-clocking-and-reset-requirements---vendor-independent-contract)** — The stable clocks, synchronous reset release, PHC increment, and media-rate obligations.
- **[4. Constraints](#4-constraints)** — Primary/generated clocks, I/O timing, reset arcs, and translated CDC exceptions.
- **[5. Proving it - the open-toolchain portability check](#5-proving-it---the-open-toolchain-portability-check)** — The Yosys and source-closure gates to run before a vendor build.
- **[6. Integration routes](#6-integration-routes)** — The supported reference-shell and custom-shell paths to the same datapath boundary.
- **[7. Port checklist](#7-port-checklist)** — A concise bring-up and acceptance list for a new board.

## 1. Porting layers

| Layer | Usually reusable | Board work |
|---|---|---|
| Milan RTL | yes | source closure and constraints |
| protocol/gPTP pins | yes | preserve pinned submodules and generated ROMs |
| MAC adapter | conceptually | map the destination MAC stream and clocks |
| audio I/O | conceptually | map I2S/TDM pins and clock ownership |
| LiteX shell | no | clock/reset, DDR3, QSPI, UART, part, speed grade |

## 2. What is and is not Xilinx-specific in the RTL - the full inventory

The Milan RTL uses SystemVerilog and vendor-recognized `ASYNC_REG` attributes,
but no required Xilinx primitive. The board shell owns PLL/MMCM, DDR, QSPI,
Ethernet PHY, and pin primitives. Replace those through the destination
toolchain while retaining the same logical clocks, reset release, packet
convention, and audio timing.

## 3. Clocking and reset requirements - vendor-independent contract

Provide stable system, timestamp, Ethernet, and audio clocks. Assert resets
asynchronously only where the wrapper documents it and release them
synchronously in each destination domain. Preserve the PHC's nominal
nanosecond increment and the configured media-grid rate.

## 4. Constraints

### 4.1 Primary clocks

Constrain every external and generated clock at its actual frequency.

### 4.2 Generated clocks

Describe MAC-forwarded and audio-MMCM outputs so downstream paths are timed.

### 4.3 I/O timing

Apply PHY and converter setup/hold requirements at the pins selected by the
board configuration.

### 4.4 Reset paths

Keep reset synchronization registers together and exclude only the intended
asynchronous assertion arcs.

### 4.5 Timing constraints - translate, don't skip

Translate every CDC exception to the destination syntax. A crossing is not
safe because a tool failed to time it; the implementation primitive and the
constraint must agree. Regenerate and inspect the CDC census after any clock
or wrapper change.

## 5. Proving it - the open-toolchain portability check

Run `syn/yosys/run.sh` and the RTL source-closure gate before the vendor build.
Then elaborate the exact board shell, inspect unconstrained paths, close placed
timing, and run the external-wire campaign. A generic synthesis pass proves
portable RTL structure, not board electrical correctness.

## 6. Integration routes

### 6.1 Route A - stay on LiteX, swap the board (least work)

Add a LiteX platform with the destination part, clocks, DDR/QSPI/UART, Ethernet
port, and audio pins. Reuse `MilanNIC`, `MilanMAC`, and
`add_milan_datapath()`. Add an end-station YAML, generate its artifacts, and
make the sweep-shape gate cover the new named recipe.

### 6.2 Route B - another SoC shell

Instantiate `milan_datapath` directly and implement the interfaces described in
the [integration guide](INTEGRATION_GUIDE.md). Reuse the generated descriptor and gPTP artifacts, and
provide an equivalent bare-metal boot sequence.

## 7. Port checklist

1. Pin the RTL and processor revisions.
2. Define clocks, resets, MAC byte order, audio pins, and flash layout.
3. Generate identity/time artifacts from one configuration.
4. Pass source closure, focused RTL, integration RTL, and Yosys.
5. Close timing and electrical constraints.
6. Grade UART identity/time state and capture real wire traffic.
