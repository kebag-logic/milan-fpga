<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# plat: the split placement's control firmware on its target (#665 S3)

This directory is the target side of the [control firmware](../README.md).
`mbx_plat_mmio.c` is the mailbox HAL on the bus.
`ctrl_split.ld` and `ctrl_split_start.S` are the image's memory map and reset entry ([split control memory](../../../../docs/design/SPLIT_CONTROL_MEMORY.md)).
The rest is the image's `main` and the platform it composes: the boot sequence, the CSR window, the console and the ports.
`milan_baremetal.c` is read and never edited; this platform ports the duties #397's rule allows into the split image.

## Contents

- **[The boot](#the-boot)** -- The nine steps of Milan v1.2 5.6.1 as the platform runs them, and what a refused stage leaves running.
- **[The CSR window](#the-csr-window)** -- The generated identity and static policy, written as `configure_fabric()` writes them, and the two enables the split never sets.
- **[The console](#the-console)** -- Decision D6's two commands, their lines, and the per-pass bound that keeps the console inside #397's tick rule.
- **[The ports](#the-ports)** -- MAAP's allocation on the CSR window, the ACMP talker sources, SRP's sources and licences, and AECP's two observations.
- **[Generated inputs](#generated-inputs)** -- The policy header from the builder's outputs, and the bus map from the SoC's own `csr.csv`.
- **[Tests and evidence](#tests-and-evidence)** -- The host arms, the trace against `milan_baremetal.c`, the planted defects and the boot simulation.
- **[Not yet done](#not-yet-done)** -- What S3 leaves to later lanes and rulings, by name.

## The boot

[`ctrl_plat.c`](ctrl_plat.c) runs the boot sequence of [the architecture](../../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#2-boot-sequence), which Milan v1.2 5.6.1 orders:

| Step | What the platform does |
|---|---|
| 1 | The bitstream configured the FPGA; `ctrl_split_start.S` sets the stack, copies `.data` and clears `.bss`. |
| 2 | The CSR policy clears `ADP_CTRL[0]` and `PP_CTRL[0]`; the core's ADP and AECP are not started. |
| 3 | The window's ID must be `MILN`; then the generated identity and static product policy are written. MAAP's allocation port then reports "no range", which clears the fabric allocator's enable and the talkers' admission, so the core's MAAP is the only owner from its start. |
| 4 | `aecp_image_load` verifies the generated AEM image's CRC and form. |
| 5 | The application, AECP and contract 2.3's face are composed into one loop, with the console's poll. |
| 6, 7 | `nvm_store_boot` reads and validates the saved state and applies bindings, then the D3 transaction, through the state port; the store's service joins the loop. |
| 8 | The mailbox opens (`ctrl_app_open`, ADP held), SRP attaches, and `ctrl_app_open_aecp` releases AECP only at an accepted terminal with every face acknowledged. |
| 9 | `ctrl_app_release_adp` starts ADP last, once AECP and ACMP accept requests. |

A stage that refuses stops the boot there and prints one line naming it.
Nothing after it runs, ADP never starts, and the loop is never serviced.
Only the console answers, as the all-fabric image keeps its BIOS console when its fabric stays disabled.
`ctrl_plat_main.c` is the target's entry: the generated words, the LiteSPI flash port and the endless `ctrl_plat_step()` loop.

## The CSR window

[`ctrl_plat_csr.c`](ctrl_plat_csr.c) writes `configure_fabric()`'s fifteen writes in its order, from the words `boot_policy.fabric_constants()` derives for the shape:

- `ADP_CTRL` and `PP_CTRL` with bit 0 cleared;
- the entity and model identity, then the station MAC;
- `MAC_CTRL` with the accept-all bit ORed in, then `TCAM_CTRL`;
- `AAF_CTRL`, `LWSRP_VID`, `LWSRP_CTRL` with its two live bits, `MAAP_CTRL` and the CRF talker's `CRFT_CTRL`.

The split never sets `ADP_CTRL[0]` or `PP_CTRL[0]`, where the all-fabric image's `entity_advertise()` does.
The core owns ADP and AECP, and a fabric advertiser or processor enabled beside it would be a second owner (the architecture's section 1).
`LWSRP_CTRL`'s two bits are the datapath's admission gates, not an SRP engine (the register map), so they keep their all-fabric meaning.

The status words are read in `milan_status_handler()`'s order, each 64-bit pair low word first.
The time of day is the snapshot strobe, a spin of at least the BIOS's `cdelay(128)`, then high, low, high until both high words agree, at most three times.

## The console

[`ctrl_plat_console.c`](ctrl_plat_console.c) answers `milan_status` and `milan_gettime`, the two commands `scripts/baremetal_uart_smoke.py` sends, in `milan_baremetal.c`'s lines.
Decision D6 (#665, issuecomment-6409738976) keeps only what the release graders read.
Every other line is answered `?`.
The boot prints one banner line and, at ready, one ready line.

The console is a loop poll and never waits on the UART:

- a pass takes at most 16 bytes from the receive FIFO and stops at a line's end;
- it runs at most one command, and only with room for the longest response (320 bytes) in its 512-byte ring;
- it hands at most 16 bytes to the transmit FIFO, and none while `TXFULL` is set;
- it reports work owed while bytes or a line wait, or after a full slice of input.

So a pass's console share is at most 104 bus accesses and one response's formatting.
The split image defines no `CTRL_MBX_WFI`, so its loop never sleeps and the console runs every pass.

## The ports

- **MAAP.** `maap_csr_allocation` ([MAAP](../maap/README.md#integration)) runs on interface 0's CSR window. The datapath has one window, so another interface's writes are dropped and counted. The platform records each report after the window has it.
- **ACMP's talker sources.** Source *n*'s stream is the entity's MAC and its STREAM_OUTPUT's unique ID (IEEE 1722.1-2021 7.2.3), on the SR class VID, at address base + *n* once MAAP holds its interface's range (Milan v1.2 5.5.4.1).
- **SRP.** Every interface declares every source, with its generated TSpec and class, unallocated at boot. The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
- **AECP.** `random` is the loop's millisecond clock. GET_AS_PATH has no split source at this base and answers unavailable.

## Generated inputs

[`ctrl_plat_gen.py`](ctrl_plat_gen.py) writes both headers; they are never hand-written:

- `policy CONFIG` writes `ctrl_plat_policy_gen.h`: the identity and boot words from `boot_policy.fabric_constants()`, the one derivation `milan_soc.py` and builder gate 35 use; and each talker source's stream from the lwSRP table, the CRF output last at the builder's `CRF_SRP_MAXFRAME_B`.
- `map CSR_CSV` writes `ctrl_plat_map_gen.h`: the `milan_csr` and `ctrl_mbx` regions and the UART's four registers, from the SoC's own `csr.csv`. The map does not depend on the image, so an export with any image gives it. A UART that pops on its `RXTX` read is refused.

`sw/firmware/ctrl/test/ctrl_plat_image.py` links the image with both, through `ctrl_srp_image.py`'s link, audits and bank plan:

```sh
python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
  --csr-csv "$SOC/csr.csv" --output "$OUT" --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

## Tests and evidence

`sw/firmware/ctrl/test/test_ctrl_firmware.py` runs four arms ([`plat_arms.py`](../test/plat_arms.py)):

- `plat`: the CSR window, the console and the MMIO platform on host buses (`test_plat.cpp`, `test_plat_mmio.cpp`);
- `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order;
- `platrv32`: the whole platform cross-compiled freestanding for RV32I;
- `plattrace`: the CSR policy's writes against `milan_baremetal.c`'s own `configure_fabric()`, compiled as builder gate 35 compiles it, for every shipped config, with three planted controls ([`plat_trace.py`](../test/plat_trace.py)).

The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 37 defects, each caught by a named test on its own words.
They include a CSR write skipped, reordered or wrong, and a console that holds the pass past its slice.

The [split boot simulation](../../../../tb/verilator/ctrl_split_boot/README.md) boots the linked image on the split CPU to its ready line, compares its CSR trace with `configure_fabric()`'s and grades the UART with the smoke grader's own parse.

## Not yet done

- **SRP's live stream configuration.** `srp_mbx.c` copies its sources at init, and nothing re-declares a source whose destination MAAP has since allocated. The sources stay unallocated, and declare Talker Failed, until an SRP adapter entry takes the allocation. That entry is in `srp/`, outside this lane's files; it needs a ruling.
- **ACMP's asking-failed source flag** reads false: the SRP adapter exposes no per-source Listener Asking Failed registration.
- **GET_AS_PATH** answers unavailable.
- **F1's flash port** keeps its fixture addresses; lane S4 generates them from the SoC's `csr.csv`.
- **The datapath faces.** At this base the `--ctrl-mailbox` build holds the face acknowledgement idle, so AECP does not open on it; the placement switch (S6) connects it.
