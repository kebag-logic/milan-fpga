<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# plat: the split placement's control firmware on its target (#665 S3)

This directory is the target side of the [control firmware](../README.md).
`mbx_plat_mmio.c` is the mailbox HAL on the bus.
`ctrl_cc.h` is the one file of the firmware outside `test/` that names a compiler extension: `noinline` and `may_alias` behind `CTRL_CC_GNU`, with a portable C11 fallback (#665: the firmware ports to a hard core; the `portable` arm holds it).
`ctrl_split.ld` and `ctrl_split_start.S` are the image's memory map and reset entry ([split control memory](../../../../docs/design/SPLIT_CONTROL_MEMORY.md)).
The rest is the image's `main` and the platform it composes: the boot sequence, the CSR window, the console and the ports.
`milan_baremetal.c` is read and never edited; this platform ports the duties #397's rule allows into the split image.

## Contents

- **[The boot](#the-boot)** -- The nine steps of Milan v1.2 5.6.1 as the platform runs them, and what a refused stage leaves running.
- **[The CSR window](#the-csr-window)** -- The generated identity and static policy, written as `configure_fabric()` writes them, and the two enables the split never sets.
- **[The console](#the-console)** -- Decision D6's two commands, their lines, and the per-pass bound that keeps the console inside #397's tick rule.
- **[The ports](#the-ports)** -- MAAP's allocation on the CSR window, the ACMP talker sources, SRP's sources and licences, and AECP's two observations.
- **[Generated inputs](#generated-inputs)** -- The policy header from the builder's outputs, the bus map from the SoC's own `csr.csv`, and the flash map every link needs.
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
| 8 | The mailbox opens with ADP held (`ctrl_app_open_held`), SRP attaches, and `ctrl_app_open_aecp` releases AECP only at an accepted terminal with every face acknowledged. |
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
A command's name is compared only as far as its terminator, so a received NUL (a UART yields 0x00 on a break) ends no command, and nothing past the name is read.

## The ports

- **MAAP.** `maap_csr_allocation` ([MAAP](../maap/README.md#integration)) runs on interface 0's CSR window. The datapath has one window, so another interface's writes are dropped and counted. The platform records each report after the window has it.
  The image draws its first range at random. Only a simulation defines `CTRL_PLAT_MAAP_PREFERRED` to pin it: the two-placement simulation in `tb/verilator/milan_dp` pins both placements at one range.
- **The receive monitor's formats** (#946). The receive monitor judges a PDU of a stream above 0 against its context's format words, LCTX words 2 and 3, which nothing but the CSR stream window writes, and a PDU not in them is UNSUPPORTED_FORMAT and discarded (Milan v1.2 Table 5.6, 4.4.2.2). So every AAF STREAM_INPUT above 0 on AVB_INTERFACE 0 of the configuration in force (`ctrl_plat_csr_sink_context`) takes its current format there: the listener selection of its index, `FMT_LO`, `FMT_HI`, and the selection it held written back (`ctrl_plat_csr_sink_format`; the CSR holds that last write off until the engine took `FMT_HI`). Stream 0 takes its format from the face's publication (`fmt0_i`), and a CRF input has its own receiver. The face itself is unchanged:
  - after the open, every face acknowledged, every input, before ADP starts and so before any probe;
  - after a SET_STREAM_FORMAT of a STREAM_INPUT, in the same call, once its commit is acknowledged, which interface 0 owing nothing after the face's change port means (the platform wraps that port);
  - any other change, and one the face could not commit at once, is owed: the platform's poll, which also runs the console, writes every input once a commit after it is acknowledged, so a change done again after IN_PROGRESS (`aecp.h`, `applied`) and a configuration's move reach the contexts.

  The poll's own share is one comparison a pass, apart from the console's; a write is five window accesses an input, 35 at 8x8, which the split boot simulation's boot write takes in 2,858 bus cycles (28.6 us at 100 MHz).

  A format moves only while its input is unbound (SET_STREAM_FORMAT and SET_CONFIGURATION refuse a bound one), and a stream reaches its context only once its binding's stream_id is published, after the probe's response, so no PDU of a new binding is judged against a format no controller sees. An unbind keeps the format: it is the STREAM_INPUT's, not the binding's. The release's firmware writes none of these words.
- **ACMP's talker sources.** Source *n*'s stream is the entity's MAC and its STREAM_OUTPUT's unique ID (IEEE 1722.1-2021 7.2.3), on the SR class VID, at address base + *n* once MAAP holds its interface's range (Milan v1.2 5.5.4.1).
- **SRP.** Every source is configured on every interface with its generated TSpec and class, and declares nothing until its destination is valid: MAAP's range held and a probe of the last 15 s or a registered Listener, the MAAP adapter's DA gate, which the composition passes to SRP (#895; Milan v1.2 4.3.3.1). It then declares Talker Advertise at base + n on its own interface, and withdraws when the gate closes ([SRP](../srp/README.md)). The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
- **AECP.** `random` is the loop's millisecond clock. Every observation is the face's ([`aecp_face.c`](../aecp/aecp_face.c)), the platform's only `random`.
  GET_AS_PATH reads its AVB interface's GSI window, kind 2: the count, then each ClockIdentity of the path sequence by its ordinal, at most `AECP_PATH_ITEMS`, so it answers SUCCESS with the sequence the datapath serves (IEEE 1722.1-2021 7.4.41; Milan v1.2 5.4.2.24; #897).
  A window that does not answer, or a count past `AECP_PATH_ITEMS`, fails that port, and the core answers as for GET_AVB_INFO's.
  AS_PATH_CHANGED leads to the unsolicited GET_AS_PATH response, which reads the window again (Milan v1.2 Table 5.22).

## Generated inputs

[`ctrl_plat_gen.py`](ctrl_plat_gen.py) writes both headers; they are never hand-written:

- `policy CONFIG` writes `ctrl_plat_policy_gen.h`: the identity and boot words from `boot_policy.fabric_constants()`, the one derivation `milan_soc.py` and builder gate 35 use; and each talker source's stream from the lwSRP table, the CRF output last at the builder's `CRF_SRP_MAXFRAME_B`.
- `map CSR_CSV` writes `ctrl_plat_map_gen.h`: the `milan_csr` and `ctrl_mbx` regions and the UART's four registers, from the SoC's own `csr.csv`. The map does not depend on the image, so an export with any image gives it. A UART that pops on its `RXTX` read is refused.

`sw/firmware/ctrl/test/ctrl_plat_image.py` links the image with both, through `ctrl_srp_image.py`'s link, audits and bank plan.
It also takes the flash map, which puts the saved-state flash port on the split SoC's addresses.
[`gen_flash_port.py`](../../ctrl_nvm/plat/gen_flash_port.py) writes that map from a split export: `milan_soc.py --ctrl-mailbox --ctrl-firmware` for the shape's config, here `$SOC`.

```sh
python3 sw/firmware/ctrl_nvm/plat/gen_flash_port.py --csr-csv "$SOC/csr.csv" \
  --csr-h "$SOC/software/include/generated/csr.h" --out "$FLASH_MAP"
python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
  --csr-csv "$SOC/csr.csv" --flash-map "$FLASH_MAP" --output "$OUT" --libc "$RUNTIME/libc.a" \
  --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

After a run, the [split boot simulation](../../../../tb/verilator/ctrl_split_boot/README.md)'s build directory holds these inputs: the export in `split-soc/mapped/soc`, the same map in `split-soc/flash-map` and the archives in `runtime`.
A link without `--flash-map`, or with a map that lacks `generated/csr.h` or `generated/mem.h`, is refused by name before the compiler is called.
The compiler would otherwise find the port's RV32 stand-ins in their place, with no diagnostic.
On the boot SoC, an image on the stand-in `generated/mem.h`, or with no map, hangs before its banner.
An image on the stand-in `generated/csr.h` alone boots to ready and passes the split boot, so this refusal is the only thing that stops it.
The refusal reads that both headers are there, not what they say.
Only the [boundary gate](../test/ctrl_runs.py)'s compile takes no map. Its archives do not exist, so it stops at its link and makes no ELF.

At 8x8 with two interfaces the image plans 60.5 RAMB36 with the control loop's tiers (#894), SRP's Talker declarations (#895) and GET_AS_PATH's read through the face (#897), 992 B of `rom` past 60.0 at this head (680 B at #901's merge `70f4056f`), and its entry ledgers 60.5, the owner's cap ([#895's ruling of 2026-11-14](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6876349305), item 4, as [#897's ruling of 2026-11-15](https://github.com/kebag-logic/milan-fpga/issues/897#issuecomment-6890824581), item 1, takes it; `ctrl_memory.LEDGERED`), with 1,056 B of `rom` left at this head (1,368 B at `70f4056f`).
The owner's ruling (#665, 6505997821), and since 2026-11-12 the owner's flip decision, ledger that one point, owed to lane S14, so its command adds `--interfaces 2 --ledgered-point platform-8x8-two-interfaces`.
Every other point is within 56 ([split control memory](../../../../docs/design/SPLIT_CONTROL_MEMORY.md#5-fit)).

## Tests and evidence

`sw/firmware/ctrl/test/test_ctrl_firmware.py` runs five arms ([`plat_arms.py`](../test/plat_arms.py)):

- `plat`: the CSR window, the console and the MMIO platform on host buses (`test_plat.cpp`, `test_plat_mmio.cpp`); the CSR window and the console run under AddressSanitizer, whose report fails the test that sent the line;
- `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order, the flash's among them; a controller's bind after ready, written back to the flash by the store's service on the loop's tick; and GET_AS_PATH answered SUCCESS with the sequence the datapath serves (B11, #897);
- `platrv32`: the whole platform cross-compiled freestanding for RV32I, a portability arm; the linked image is the split hart's RV32IM with the record mover (`ctrl_plat_image.py`);
- `plattrace`: the CSR policy's writes against `milan_baremetal.c`'s own `configure_fabric()`, compiled as builder gate 35 compiles it, for every shipped config, with three planted controls ([`plat_trace.py`](../test/plat_trace.py)).
- `platsinks`: the receive monitor's formats (#946) at 8x8/1if, whose AAF inputs 1 to 7 each have a context, and the shipping 1x1/1if, which has none (`test_plat_sinks.cpp`): every input at READY after the open's acknowledged publication; an acknowledged SET_STREAM_FORMAT moving its input's context alone, and a bound input refusing it; nothing written for a commit never acknowledged or while a change waits IN_PROGRESS, and the change done again written once acknowledged; a change of another kind leaving every context at its format in force. `test_plat.cpp`'s C5 and C6 hold the window's writes and which inputs have a context. [`sink_mutants.py`](../test/sink_mutants.py)'s 19 defects are in the control campaign, each caught by a named test on its own words, the shipped firmware's state (nothing written after the open, no change followed) among them.

The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 42 defects, each caught by a named test on its own words.
They include a CSR write skipped, reordered or wrong, a console that holds the pass past its slice, a command compared past its terminator, the saved state read after the mailbox opens, and its service left off the loop.

The [split boot simulation](../../../../tb/verilator/ctrl_split_boot/README.md) boots the linked image on the split CPU to its ready line, compares its CSR trace with `configure_fabric()`'s and grades the UART with the smoke grader's own parse.

The split boot simulation generates F1's flash map from the split SoC's `csr.csv` and passes it to both platform links and boot exports.
Each export checks the placement against that map.
The refusal of a link without the map, or with a map that lacks a header, is a control of [`ctrl_image_selftest.py`](../test/ctrl_image_selftest.py), which the boundary gate runs.

## Not yet done

- **The graders on a split image.** The smoke grader's `fabric-enabled` check and the #396 campaign's one BIOS pass per cold cut cannot hold on a split image, which never sets `ADP_CTRL[0]` or `PP_CTRL[0]` and has no BIOS. The same ruling accepts both as listed differences; the graders' split mode is owed to the bench lane (S12).
- **The largest point's block RAM.** At 8x8 with two interfaces the image plans 60.5 RAMB36 with the control loop's tiers (#894), SRP's Talker declarations (#895) and GET_AS_PATH's read through the face (#897), past the 60.0 the owner's [decision of 2026-11-12](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6824896581) ledgers for the flip, and its entry at 60.5, that decision's cap, by [#895's ruling of 2026-11-14](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6876349305), item 4, as [#897's ruling of 2026-11-15](https://github.com/kebag-logic/milan-fpga/issues/897#issuecomment-6890824581), item 1, takes it, refused at 61.0: ROM debt of 4.5 RAMB36 owed to lane S14 (decision D3), 18,432 B of cold code to move to flash, the cap fully used. [`plat_ledger.py`](../../../../tb/verilator/ctrl_split_boot/plat_ledger.py) links the image at every point against the ledger ([SPLIT_CONTROL_MEMORY.md section 5](../../../../docs/design/SPLIT_CONTROL_MEMORY.md#5-fit)).
- **ACMP's asking-failed source flag** reads false: the SRP adapter exposes no per-source Listener Asking Failed registration.
- **The datapath faces.** At this base the `--ctrl-mailbox` build holds the face acknowledgement idle, so AECP does not open on it; the placement switch (S6) connects it.
