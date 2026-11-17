<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# plat: the split placement's control firmware on its target (#665 S3)

This directory is the target side of the [control firmware](../README.md).
`mbx_plat_mmio.c` is the mailbox HAL on the bus.
`ctrl_cc.h` is the one file of the firmware outside `test/` that names a compiler extension: `noinline` and `may_alias` behind `CTRL_CC_GNU`, with a portable C11 fallback (#665: the firmware ports to a hard core; the `portable` arm holds it).
`ctrl_split.ld` and `ctrl_split_start.S` are the image's memory map and reset entry ([split control memory](../../../../docs/design/SPLIT_CONTROL_MEMORY.md)).
The rest is the image's `main` and the platform it composes: the boot sequence, the CSR window, the console and the ports.
`milan_baremetal.c` is read and never edited; this platform ports the duties #397's rule allows into the split image.
`ctrl_plat_phy.c` is the PHY poll (#919).

## Contents

- **[The boot](#the-boot)** -- The nine steps of Milan v1.2 5.6.1 as the platform runs them, and what a refused stage leaves running.
- **[The CSR window](#the-csr-window)** -- The generated identity and static policy, written as `configure_fabric()` writes them, and the two enables the split never sets.
- **[The console](#the-console)** -- Decision D6's two commands, their lines, and the per-pass bound that keeps the console inside #397's tick rule.
- **[The ports](#the-ports)** -- MAAP's allocation on the CSR window, the ACMP talker sources, SRP's sources and licences, and AECP's two observations.
- **[The PHY](#the-phy)** -- The release's PHY poll on THE STEP: one Clause-22 frame a call, its 1000BASE-T-only advertisement, its pace, its half period, and where the published link goes.
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
- **ACMP's talker sources.** Source *n*'s stream is the entity's MAC and its STREAM_OUTPUT's unique ID (IEEE 1722.1-2021 7.2.3), on the SR class VID, at address base + *n* once MAAP holds its interface's range (Milan v1.2 5.5.4.1).
- **SRP.** Every source is configured on every interface with its generated TSpec and class, and declares nothing until its destination is valid: MAAP's range held and a probe of the last 15 s or a registered Listener, the MAAP adapter's DA gate, which the composition passes to SRP (#895; Milan v1.2 4.3.3.1). It then declares Talker Advertise at base + n on its own interface, and withdraws when the gate closes ([SRP](../srp/README.md)). The licences reach the fabric through the publication block (`srp_mbx.c`), and the platform records each.
- **AECP.** `random` is the loop's millisecond clock. GET_AS_PATH has no split source at this base and answers unavailable.

## The PHY

[`ctrl_plat_phy.c`](ctrl_plat_phy.c) is the release's `phy_link_tick` on the split's loop (#919).
It reads the PHY's Clause-22 registers through the SoC's MDIO bit-bang pair (`milan_mac_phy_mdio_w` and `_r`) and publishes the resolved link, speed and duplex to `milan_mac_link_status`, the datapath's link input (REQ-MAC-03).
Without it that word keeps its reset value, link up, and no consumer of the datapath's effective link sees a link change.

- **The poll** is the release's. No PHY found, one address is probed a frame (PHYID1), a miss published link down and the next address probed at once, with no blocking scan. Found, BMSR: a loss it latched while the link was published up is published down first, and a second BMSR read gives the current state, so a loss that recovered between two polls publishes both edges in that poll. A link up is resolved from BMCR (the forced mode with autonegotiation off), then, once negotiation is complete, the 1000BASE-T control and status where the extended status offers it, then the advertisement and the partner's ability. Incomplete negotiation, an unacknowledged read and a master-slave fault stay link down.
- **THE ADVERTISEMENT** (#840, as the release's PHY init applies it). The MAC runs at 1 Gb/s only, so a PHY with 1000BASE-T full duplex ability (BMSR's extended capability, then the extended status) advertises 1000BASE-T full duplex alone. Register 9 keeps its MASTER-SLAVE bits and advertises full duplex, not half. Register 4 drops 10BASE-T, 100BASE-TX, 100BASE-T4 and its reserved bit 14, keeping its pause bits and selector. Register 0 then enables and restarts autonegotiation with reset and isolate clear. A partner without 1000BASE-T then gets no link, published down, rather than a 100 Mb/s link the MAC is silent on. A PHY without that ability is a 10/100 PHY and is never written. It runs in the poll's frames after its first BMSR read and before the current state is resolved, as the release's, so a link the PHY formed before the restart is never published. It runs at boot and again after every link loss, a published link going down (#919): registers 4 and 9 are read, written and read back, and the poll owes it again until the read-back holds it. Negotiation restarts after every write that repaired the advertisement, the registers as read not holding it (a PHY reset to its defaults, a write the PHY dropped), so the abilities in force are always the ones written and verified (IEEE 802.3 28.2.4.1.3), and once at boot whatever the PHY held. A loss where the PHY still holds the advertisement writes it and does not restart, because a restart latches a loss of its own; a PHY that never takes a write is restarted at each try. The release's init writes once at boot. The read-back and the pass after every loss are #919's. An unacknowledged read writes nothing; the next poll retries.
- **THE OUTCOME.** The restart's own write is never read back: its bit clears itself (IEEE 802.3 22.2.4.1.7), so a restart the PHY dropped leaves the negotiation before it in force while registers 4 and 9 read back. So the restart is verified by what it negotiates. A negotiation complete (BMSR bit 5) on a link up that shares no 1000BASE-T mode in registers 9 and 10, while the advertisement is verified, is that earlier negotiation: its link resolves from 4 and 5, which share no mode below 1000 Mb/s, so it is published down, and the next poll owes the advertisement again with its restart taken whatever the PHY holds, counted (`renegotiations`). A poll that restarted negotiation reads BMSR again after the restart and resolves from that, so the check never judges the link a restart has just dropped: it restarts at most once a poll and never during a negotiation. A forced mode is published as the release publishes it. The release's init has the same gap and is not changed here.
- **The pace.** A poll starts `CTRL_PLAT_PHY_POLL_US` after the last one started: the release's `PHY_POLL_NS`, by its own derivation, half the writer's 250 ms heartbeat (`MILAN_NVM_HEARTBEAT_MS`), 125 ms. A probe that misses is due again at once.
- **THE STEP.** A frame is 64 bit periods (`CTRL_PLAT_PHY_FRAME_BITS`): a poll is up to nine reads, and where the advertisement is owed nine more frames, six reads (15, 4, 9, 0, then 4 and 9 back) and three writes (9, 4, 0, the restart's write omitted where the PHY still held the advertisement). A frame is too long to stand beside a pass's records, and MDC has no maximum high or low time (IEEE 802.3 22.2.2.13), so the poll is resumable, one frame a call. `ctrl_plat_phy_store_step` is THE STEP's client the platform binds (`ctrl_loop.h`): the saved-state store's owed step first, unchanged, and the PHY's next frame only in a call whose store took no step of a save (none, or one from `OFF`, `IDLE` or `HELD`), with `CTRL_PLAT_PHY_STEP_US` of the pass's share left. While a poll owes a frame the client owes a step, so under input that never leaves a pass empty the frames ride THE STEP's age limit, in the passes given whole whose store step is an idle one.
- **The half period** is at least 200 ns, so MDC is high and low at least 160 ns each in a period of at least 400 ns (22.2.2.13) and a sample follows the PHY's output delay, at most 300 ns after the rising edge (22.3.4). It is `ceil(CONFIG_CLOCK_FREQUENCY / 5 MHz)` turns of a spin at one cycle a turn, or one turn where arming times a run of 1,024 turns on the flash port's clock and finds a turn alone holds 200 ns. On the split CPU a turn is about 27 cycles, so one.
- **The paths.** The poll is armed past the CSR identity check, so a window that failed it leaves the MDIO pins untouched. Every later stage polls: the ready loop through THE STEP, a refused stage on each turn of its console, as the release publishes the link on every path past its identity check (#70). A SoC whose `csr.csv` has no MDIO pair arms nothing.

The published word reaches every consumer through the datapath's effective link (`milan_datapath.sv`, `eff_link_w`, `link_up` through the SoC's synchroniser and `LINK_CTRL[0]`, which resets 1): the AVB_INTERFACE LINK_UP and LINK_DOWN counters and their GET_COUNTERS notification (the face's COUNTERS_CHANGED, `ctrl_app_aecp.c`), the gPTP plane's port enable, whose toggle ends the Pdelay_Req cease (Milan v1.2 4.2.6.2.5), and the mailbox's LINK level and event, which ADP, MAAP and SRP take.

## Generated inputs

[`ctrl_plat_gen.py`](ctrl_plat_gen.py) writes both headers; they are never hand-written:

- `policy CONFIG` writes `ctrl_plat_policy_gen.h`: the identity and boot words from `boot_policy.fabric_constants()`, the one derivation `milan_soc.py` and builder gate 35 use; and each talker source's stream from the lwSRP table, the CRF output last at the builder's `CRF_SRP_MAXFRAME_B`.
- `map CSR_CSV` writes `ctrl_plat_map_gen.h`: the `milan_csr` and `ctrl_mbx` regions, the UART's four registers and the PHY's three (`milan_mac_phy_mdio_w` and `_r`, `milan_mac_link_status`, all three or none, none written as 0), from the SoC's own `csr.csv`. The map does not depend on the image, so an export with any image gives it. A UART that pops on its `RXTX` read is refused, and so is a `csr.csv` with some but not all of the PHY's rows.

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

At 8x8 with two interfaces the image carries the control loop's tiers (#894), SRP's Talker declarations (#895), and the PHY poll with its advertisement (#919, #840). It plans 61.0 RAMB36, 652 B of `rom` past 60.5 at this head. Its entry ledgers 61.0, with 1,396 B of `rom` left. That is the owner's rule of 2026-11-15, which supersedes the 60.5 cap of [#895's ruling of 2026-11-14](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6876349305) until S14 ([#923's ruling of 2026-11-16](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024); `ctrl_memory.LEDGERED`).
The owner's ruling (#665, 6505997821), and since 2026-11-12 the owner's flip decision, ledger that point, owed to lane S14, so its command adds `--interfaces 2 --ledgered-point platform-8x8-two-interfaces`.
At 8x8 with one interface, a shipping image, the image plans 56.5 RAMB36, 1,132 B of `rom` past 56.0, with 916 B left. A product entry ledgers it by the same rule (`platform-8x8-one-interface`). The product SoC build (`milan_soc.add_ctrl_memory`) and this link without `--ledgered-point` plan it there by its symbols (`ctrl_memory.product_point`). Every image no entry names stays refused past 56.
Every other point is within 56 ([split control memory](../../../../docs/design/SPLIT_CONTROL_MEMORY.md#5-fit)).

## Tests and evidence

`sw/firmware/ctrl/test/test_ctrl_firmware.py` runs four arms ([`plat_arms.py`](../test/plat_arms.py)):

- `plat`: the CSR window, the console and the MMIO platform on host buses (`test_plat.cpp`, `test_plat_mmio.cpp`); the CSR window and the console run under AddressSanitizer, whose report fails the test that sent the line;
- `platboot`: the boot and composition at one and two interfaces on the mailbox model, F1's flash model and the host bus (`test_plat_boot.cpp`), every bus access in one order, the flash's among them; and a controller's bind after ready, written back to the flash by the store's service on the loop's tick. With a pin-level Clause-22 PHY behind that bus (`phy_peer.hpp`), the PHY poll alone (`test_plat_phy.cpp`, P1 to P18: the probe, the pace, the latched loss, every resolved mode, the error paths, the frame, THE STEP's room, the owed report, the half period, the clock's wrap; and the advertisement: its writes at boot, each property by its own name from start values in opposite states as the release's host test grades them, a 10/100 PHY never written, written and read back after every loss with no restart where the PHY held it, a reset PHY, or one that lost register 4 or register 9 alone, restarted once, an advertisement that does not read back owed again and negotiation restarted after each repaired write, an unacknowledged read writing nothing, and P17, the abilities in force latched at each restart by the peer: register 4's writes dropped through a try, at boot and after a loss, a 100BASE-TX-only partner has no link once the repair reads back, the repair's own restart doing it; and THE OUTCOME, P18: a restart write the PHY lost, so the earlier 100 Mb/s negotiation stays in force, is published down and restarted once by the next poll, counted (saturating), one restart a poll until one takes, none while the negotiation is incomplete, none at 1000BASE-T, none on a PHY the advertisement is not for) and composed (`test_plat_boot.cpp`, B11, B12 and L1 to L4: armed past the identity check, THE STEP's client, and the published word's consumers, the datapath's link modelled as the RTL builds it: each edge counted, notified by AECP, and the gPTP plane's port enable rising with the first poll after the link's return);
- `platrv32`: the whole platform cross-compiled freestanding for RV32I, a portability arm; the linked image is the split hart's RV32IM with the record mover (`ctrl_plat_image.py`);
- `plattrace`: the CSR policy's writes against `milan_baremetal.c`'s own `configure_fabric()`, compiled as builder gate 35 compiles it, for every shipped config, with three planted controls ([`plat_trace.py`](../test/plat_trace.py)).

The control campaign plants [`plat_mutants.py`](../test/plat_mutants.py)'s 94 defects, each caught by a named test on its own words.
They include a CSR write skipped, reordered or wrong, a console that holds the pass past its slice, a command compared past its terminator, the saved state read after the mailbox opens, and its service left off the loop. The PHY's 53 (the poll's 22, the link counters' notification, the bus map's 3 and the advertisement's 27) include the four #919 names, each reproducing a bench symptom: no poll, the latched loss not published, an edge not counted (a whole poll in one call, its loss and its recovery in the same turn), and the cease not ended on link-up (the second BMSR read dropped, so the link's return is published a poll late). They also include #840's named defect, 100BASE-TX left advertised, and one per write property and per rule: written once only, restarted after every loss, a PHY that lost register 4 or register 9 alone not restarted, a restart marked taken before the read-back verifies (the repair of a dropped write then never negotiated), not read back, written before its reads are answered; and THE OUTCOME's: unchecked, owing the advertisement without its restart, uncounted, its count wrapping, judging a link at 1000BASE-T or a PHY the advertisement is not for, and resolving from the BMSR read before a restart.

The [split boot simulation](../../../../tb/verilator/ctrl_split_boot/README.md) boots the linked image on the split CPU to its ready line, compares its CSR trace with `configure_fabric()`'s and grades the UART with the smoke grader's own parse. It is the PHY too: it grades the published link word through a probe, a latched loss, a sustained loss and the link's return, MDC's timing, and each frame's cost on the split CPU against `CTRL_PLAT_PHY_STEP_US`. It also grades the advertisement's writes: the boot's three, then two after each loss with no restart, each group read back.

The split boot simulation generates F1's flash map from the split SoC's `csr.csv` and passes it to both platform links and boot exports.
Each export checks the placement against that map.
The refusal of a link without the map, or with a map that lacks a header, is a control of [`ctrl_image_selftest.py`](../test/ctrl_image_selftest.py), which the boundary gate runs.

## Not yet done

- **The graders on a split image.** The smoke grader's `fabric-enabled` check and the #396 campaign's one BIOS pass per cold cut cannot hold on a split image, which never sets `ADP_CTRL[0]` or `PP_CTRL[0]` and has no BIOS. The same ruling accepts both as listed differences; the graders' split mode is owed to the bench lane (S12).
- **The 8x8 images' block RAM.** At 8x8 with two interfaces the image plans 61.0 RAMB36 with the control loop's tiers (#894), SRP's Talker declarations (#895), and the PHY poll and its advertisement (#919, #840). That is past the 60.0 the owner's [decision of 2026-11-12](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6824896581) ledgers for the flip and past that decision's 60.5 cap ([#895's ruling of 2026-11-14](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6876349305), item 4). Its entry is 61.0, refused at 61.5, by the owner's rule of 2026-11-15 ([#923's ruling of 2026-11-16](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024)): ROM debt of 5.0 RAMB36 owed to lane S14 (decision D3), 20,480 B of cold code to move to flash. At 8x8 with one interface the image plans 56.5, and its product entry 56.5 is refused at 57.0: ROM debt of half a tile owed to S14. [`plat_ledger.py`](../../../../tb/verilator/ctrl_split_boot/plat_ledger.py) links the image at every point against the ledger ([SPLIT_CONTROL_MEMORY.md section 5](../../../../docs/design/SPLIT_CONTROL_MEMORY.md#5-fit)).
- **ACMP's asking-failed source flag** reads false: the SRP adapter exposes no per-source Listener Asking Failed registration.
- **GET_AS_PATH** answers unavailable.
- **The datapath faces.** At this base the `--ctrl-mailbox` build holds the face acknowledgement idle, so AECP does not open on it; the placement switch (S6) connects it.
