# The end-station reset on an AECP REBOOT

Issue [#787](https://github.com/kebag-logic/milan-fpga/issues/787) records this decision and implements it.
A controller's REBOOT of ENTITY 0 (IEEE 1722.1-2021 7.4.43) is the soft reset of the
[#396](https://github.com/kebag-logic/milan-fpga/issues/396) release gate: 50 of its 200 power cycles.
The [owner decision of 2026-10-26](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-6409128703)
chose REBOOT for them and excluded a JTAG warm reload.
The protocol processor answers the command and raises `reboot_req_o` (processor issue #203).
This page decides what the end station then does, and states what that reset touches and what it leaves.

IEEE 1722.1-2021 7.4.43 says the command "is used to power cycle an ATDECC Entity".
The design therefore picks the reset closest to a power cycle that a running device can perform on itself.

## Contents

- **[1. The decision](#1-the-decision)** -- A configuration reload from flash through ICAPE2 IPROG, after the saved state drains and with the PHY held in reset.
- **[2. What each candidate resets](#2-what-each-candidate-resets)** -- The PHY, the GMII clocking and MMCMs, the gPTP timestamping path, the journal and the boot path, under a fabric and CPU soft reset, under the chosen reload and under a power cut.
- **[3. The sequence and its bound](#3-the-sequence-and-its-bound)** -- The four phases of `KL_reboot_ctrl`, the egress wait that lets the last frames reach the wire, the IPROG words on the ICAPE2 bus and the stated bound from the request to the reload.
- **[4. A journal write in progress](#4-a-journal-write-in-progress)** -- Why a commit in flight completes, why one that cannot is abandoned exactly where a power cut would leave it, and why the configuration logic never reads a busy flash.
- **[5. Why the JTAG-reload defect cannot recur](#5-why-the-jtag-reload-defect-cannot-recur)** -- What a JTAG reload leaves unreset, what the chosen reset adds, and the bench check that decides.
- **[6. After the reset](#6-after-the-reset)** -- The four #396 power-area checks, and where each is graded.
- **[7. Evidence](#7-evidence)** -- The suites, the planted mutants and the routed image.

## 1. The decision

**(b), a configuration reload from flash through ICAPE2 IPROG.**
The [assignment's ruling](https://github.com/kebag-logic/milan-fpga/issues/787#issuecomment-6493879824) preferred it, and the evidence below supports it.

The reload re-runs the configuration a power-on runs: the configuration logic reads the bitstream from the QSPI flash at
offset 0, where every profile keeps it ([BUILDING.md section 4](../integration/BUILDING.md#4-after-the-build-load-console-and-bench-roles)).
Global set/reset returns every register to its configured initial value.
Every block RAM and LUT RAM receives its bitstream contents again, and every MMCM and PLL is reconfigured and relocks.
So the fabric, the CPU and its ROM, the gPTP timestamping path and the clocking all start as from a cold boot.

Two things a power cut does are not done by IPROG, and the design adds them:

1. **The PHY is held in reset first.** IPROG does not reset the PHY.
   [`KL_reboot_ctrl`](../../hdl/milan/KL_reboot_ctrl.sv) raises `o_reboot_phy_hold`, and the SoC
   sets the LiteEth PHY reset from it, the `milan_mac_phy_crg_reset` CSR storage that drives the PHY's reset pin
   ([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py), `MilanMAC`).
   The link drops, and the PHY renegotiates after the reload as after a cut.
2. **The saved state drains first.** A power cut cannot wait; a REBOOT can.
   The reset waits, within a bound, until everything accepted is in a journal slot or nobody is left to put it there
   (section 4).

A REBOOT also owes the network its farewell, which a cut does not send: the SUCCESS response, the notification to
the other registered controllers and, where the entity advertises, ENTITY_DEPARTING (Milan v1.2 5.6.3.3,
5.6.3.5.8 and 5.6.3.5.11, Table 5.51; IEEE 1722.1-2021 6.2.4.1.3 and 6.2.5.2.2). The processor raises its request
once the last of them has left its own transmit face, while that frame is still inside the SoC's MAC. So the PHY
hold also waits, within a bound, until every frame given to the MAC has reached its PHY (the egress wait below).

The rejected alternative is **(a), a fabric and CPU soft reset** without reconfiguration.
Section 2 shows it leaves the clocking, the memories and the PHY in their running state.
That is the class of state a power cut clears and a soft reset cannot be shown to clear.

## 2. What each candidate resets

| Item | (a) fabric and CPU soft reset | (b) IPROG with the PHY hold (chosen) | Power cut (the reference) |
|---|---|---|---|
| PHY (the RTL8211E on the GMII port) | Not reset. LiteEth's start-up pulse is 256 `sys` clocks (2.56 us at 100 MHz, `LiteEthPHYHWReset`), and nothing else drives the reset pin | Held in reset through `milan_mac_phy_crg_reset` for at least 3,500 ms before the reload; the link drops and renegotiates | Unpowered; the link drops and renegotiates |
| GMII/RGMII clocking and MMCMs | Not reset: the PLL reset is the board's reset button alone (`milan_soc.py`, `pll.reset.eq(~rst_n)`), so the MMCMs stay locked and the eth clocks keep their phase | Every MMCM and PLL is reconfigured and relocks; the eth clocks restart from the PHY after renegotiation | Same as (b) |
| gPTP timestamping path (the PHC, the plane, `KL_gptp_gmii_launch` and its 125:50 MHz crossing) | Registers with a reset return to it; memories, reset-less flops and the clock phase relation keep their running values | Every flop, memory and crossing starts from the bitstream, against freshly locked clocks and a freshly negotiated link | Same as (b) |
| The persistence journal (the A/B slots) | Whatever the reset interrupts | Drained first (section 4); a commit in flight completes, one that cannot is abandoned at a command boundary | Torn wherever the cut lands; the A/B contract keeps the other slot ([SAVED_STATE_FASTCONNECT.md 7](SAVED_STATE_FASTCONNECT.md#7-durability-the-ab-contract)) |
| The saved-state image in DRAM | Kept, with its validity | Not relied on: the DDR3 keeps power, but the boot path re-trains it and reloads the window from a validated slot | Lost |
| The boot path | The core restarts from its reset vector with the fabric configuration retained, the restart [#366](https://github.com/kebag-logic/milan-fpga/issues/366) records after a flash ([BUILDING.md section 4](../integration/BUILDING.md#4-after-the-build-load-console-and-bench-roles)) | The full power-on path: bitstream, BIOS, SDRAM training and memtest, AEM copy and CRC, `nvm_boot()`, restore walk, entity enable | Same as (b) |
| QSPI flash | Not affected | Keeps power; an operation started before the hold finishes during it | Unpowered |
| `BOOTSTS` | Unchanged | `status_0` records the IPROG attempt and `status_1` the previous configuration | A fresh single configuration |

The last row is the one visible difference of (b) at the device: a `BOOTSTS` read after a REBOOT shows IPROG set,
which [BUILDING.md section 4](../integration/BUILDING.md#4-after-the-build-load-console-and-bench-roles) reads as a fault only after a first boot that no REBOOT preceded.

## 3. The sequence and its bound

[`KL_reboot_ctrl`](../../hdl/milan/KL_reboot_ctrl.sv) is vendor-neutral and lives in `milan_datapath`.
It counts the datapath's millisecond tick and runs four phases on the processor's held request:

| Phase | Ends when | Bound |
|---|---|---|
| DRAIN | `nvm_backed = 0`, or `nvm_dirty = 0` and `nvm_pend = 0`; otherwise at the deadline | at most `REBOOT_DRAIN_MS_P` = 10,000 ms + 1 tick |
| EGRESS | from its first clock the MAC port finishes the frame in progress and starts no other; the phase ends on a tick once every frame the port handed the MAC has left the MAC's PHY interface and one more tick has passed with nothing left; otherwise at the deadline | at most `T_EGRESS_MS_C` + 1 tick, derived from the MAC's statement: 2 ms on the AX7101, 11 ms on the Arty, 28 ms at the datapath's default |
| HOLD | `o_reboot_phy_hold` rises at its start and stays up; the phase lasts its bound | more than `REBOOT_HOLD_MS_P` = 3,500 ms, at most 1 tick more |
| IPROG | eight clocks of ICAPE2 words, CSIB low | 8 clocks; then HOLD again, so the words repeat every 3,500 ms while the device still runs |

**The bound.** From `reboot_req_o` to the clock ICAPE2 takes the IPROG command word: at most
`REBOOT_DRAIN_MS_P` + `T_EGRESS_MS_C` + `REBOOT_HOLD_MS_P` + 3 ms + 8 clocks. That is 13,505 ms and 8 clocks on the
AX7101, 13,514 ms on the Arty and 13,531 ms at the datapath's default statement: the 13,502 ms stated before the
egress wait, grown by its bound and its tick. When the saved state is already durable, the usual case on the bench, it is at most
`T_EGRESS_MS_C` + 3,502 ms and 8 clocks, 3,504 ms on the AX7101; the egress wait itself usually ends on its quiet tick,
one to two milliseconds after the last frame left. The configuration load and the boot that follow are the power-on
path's.

### The egress wait

**Why it exists.** On silicon, a REBOOT of an advertising entity sent its SUCCESS response and its notification, and
then nothing: no ENTITY_DEPARTING ([#787](https://github.com/kebag-logic/milan-fpga/issues/787#issuecomment-6518083444)).
The PHY hold rose two clocks after the request. The processor raises `reboot_req_o` once the DEPARTING's last byte has
left its own transmit face, but the frame still had to cross the `KL_pp_shadow` packer's last beat, the SoC's
`mac_tx_cdc` and store-and-forward `tx_sf`, the LiteEth core's own crossing and pipeline, and the PHY stage. The PHY
reset dropped it there. `tb/verilator/pp_shadow` section `[RB]` reproduces it at the head before the fix: graded at a
MAC model's wire-side output, the DEPARTING never leaves.

**What it observes.** `KL_reboot_ctrl` keeps an account from reset, because a frame in the MAC when the request rises
was handed over before it. The datapath's own MAC port counts a frame in on its last beat. The MAC counts it out:
`MilanMAC` flips a reset-less toggle, `ethtxend_tgl`, on the last octet of every frame at LiteEth's `phy.sink`, the
stream the PHY's transmit register stage consumes and the seam `KL_gptp_gmii_launch` already observes. The toggle
reaches the datapath as `i_ethtxend_tgl` and is synchronised there like the link guard's three toggles. The wait ends
once no frame is half taken at the port and none is in the MAC, after one more whole tick with nothing left, which
covers the PHY's own transmit path. Everything is parent code; LiteEth is used as pinned.

**What it stops.** From the phase's first clock the datapath's MAC port finishes the frame in progress and starts no
other until reset (`mac_tx_stop_o`). The frames the PHY hold waits for are therefore the last the MAC is given, and
the wait is finite even while a talker streams. Frames offered after that, a stream's next PDU or a MAAP probe, stay
in the datapath and are lost with the reload, as at a cut.

**The bound, derived.** A MAC that never finishes, with a stopped transmit clock for example, ends the wait at
`T_EGRESS_MS_C`: the time to send `REBOOT_MAC_TX_OCTETS_P` at `REBOOT_MAC_MIN_MBPS_P`, rounded up to whole
milliseconds, plus the quiet millisecond. The MAC states both through `milan_datapath`'s parameters.
`_mac_tx_egress_octets` in `sw/litex/milan_soc.py` computes the octets from the depths the FIFOs are built with, so
the bound cannot drift from the build. The builder states the same two values by evaluating those definitions out of
the SoC (`reboot_mac_statement` in `sw/builder/endstation_builder.py`). Builder gate 23m requires every config's
Instance to bind exactly what it states, and gate 1f holds the FIFOs to the named depths and the toggle to its seam. It counts every beat of `mac_tx_cdc` (17), `tx_sf` (513) and the core's
crossing and stages (34) at 8 octets. It adds, for every frame those beats can belong to (61: one per beat outside
`tx_sf`, its 8 frame slots and 2 more inside it), padding to 60 octets, the FCS, the preamble and start delimiter,
and the gap: 84 octets. Last comes one maximum envelope frame on the line, 2,020 octets. The total is 11,656 octets
(IEEE 802.3-2022 3.2.1, 3.2.2, Table 4-2). `LiteEthPHYGMII` runs at 1 Gb/s only, so the AX7101's bound is 2 ms;
`LiteEthPHYMII` runs at 10 or 100 Mb/s, so the Arty's is 11 ms. A MAC that states nothing gets the datapath's
default, 32,768 octets at 10 Mb/s, and 28 ms.

**What can lengthen it, and nothing can shorten it.** A frame the MAC takes and never sends leaves the count high, and
the wait then runs to its bound: the MAC's internal loopback, or a reset of one side of the MAC only. The count
saturates and cannot wrap, so it can only make the wait longer. While the link guard holds both the MAC's `sys` side
and its eth side in reset, every frame the MAC held is gone, and the count is cleared.

**The words.** The 7-series IPROG sequence through ICAPE2, as configuration words:

| Clock | Word | Meaning | On the ICAPE2 `I` bus |
|---:|---|---|---|
| 0 | `0xFFFF_FFFF` | dummy word | `0xFFFF_FFFF` |
| 1 | `0xAA99_5566` | sync word | `0x5599_AA66` |
| 2 | `0x2000_0000` | type-1 NOOP | `0x0400_0000` |
| 3 | `0x3002_0001` | type-1 write, one word, to WBSTAR (register `0b10000`) | `0x0C40_0080` |
| 4 | `0x0000_0000` | the warm-boot start address: the bitstream at flash offset 0 | `0x0000_0000` |
| 5 | `0x3000_8001` | type-1 write, one word, to CMD (register `0b00100`) | `0x0C00_0180` |
| 6 | `0x0000_000F` | IPROG (command `0b01111`) | `0x0000_00F0` |
| 7 | `0x2000_0000` | type-1 NOOP | `0x0400_0000` |

The ICAPE2 data bus takes every byte with its bit order reversed, so the module drives the right-hand column.
The 7-series configuration user guide is not in the local standards set, so the words are cited from the tree's own
pinned sources instead: the type-1 header, the register and the command encodings are the pinned LiteX ICAP core's
(`litex/soc/cores/icap.py` at the `sw/litex/litex_pins.txt` revision: `ICAP_SYNC`, `ICAP_NOOP`, `ICAP_WRITE`,
`ICAPRegisters.WBSTAR` and `.CMD`, `ICAPCMDs.IPROG`, and the per-byte bit reversal at its instance).
The vendor's own ICAPE2 simulation model reverses each byte the same way (`bit_revers8`).
Writing WBSTAR explicitly, rather than relying on its power-on value as the LiteX reload does, pins the reload to the
offset-0 bitstream whatever an earlier configuration left there.

The SoC attaches the two ends and adds no logic of its own. `MilanMAC` instantiates `ICAPE2` with `ICAP_WIDTH = X32`,
clocked by the datapath clock the words are generated in (50 MHz on the AX7101, inside the primitive's 100 MHz), with
`RDWRB` tied to write.
The PHY hold crosses into `sys` through a `MultiReg` and sets the PHY reset's CSR storage.
A CPU write to that CSR in the same cycle can clear it for that one cycle, and the hold sets it again on the next.
No firmware writes it.
While the PHY is held its receive clock stops, so [`KL_link_guard`](../../hdl/common/KL_link_guard.sv) declares the
clock dead and holds the MAC's resets, as for any link loss ([clock-domain guide](../litex/CLOCK_DOMAINS.md#reset-ownership)).
The guard's toggles are reset-less observers outside the hold, so it cannot deadlock on it, and the reload follows
before anything waits for the recovery.

**The contract change is one documented reset-control bit, `o_reboot_phy_hold`, the ICAPE2 port that carries the
fixed IPROG words to the primitive, and the MAC's frame-end toggle `i_ethtxend_tgl` with the two parameters by which
the MAC states its transmit side.** No CSR, no register field and no processor port beyond #203's `reboot_req_o` is
added. The [integration contract](../integration/INTEGRATION_GUIDE.md) lists the group. Leaving the outputs open and
the toggle tied 0 is safe: a REBOOT then only takes the entity off the network until the next reset, as the processor
documents, and its egress wait runs to its bound.

## 4. A journal write in progress

The firmware owns the flash; the fabric holds the record image in DRAM behind `KL_nvm_backend`
([SAVED_STATE_FASTCONNECT.md 8](SAVED_STATE_FASTCONNECT.md#8-where-the-image-lives-in-fabric-and-what-it-costs)).
A commit is an erase of the non-authoritative slot, its page programs and a read-back.

**A commit in flight completes.** The drain waits while a live writer (`nvm_backed = 1`) still has committable work
(`nvm_dirty`) or accepted work not yet committable (`nvm_pend`). A capture under commit keeps `nvm_dirty` set until its
acknowledgement, so the drain ends after the read-back of the last commit that matters, with the flash idle.
A change a controller made just before the REBOOT is therefore kept: the producer's 500 ms debounce, the writer's
1,000 ms debounce and T-NVM-COMMIT-TIMEOUT's 8,000 ms all fit inside the 10,000 ms drain
([SAVED_STATE_FASTCONNECT.md 9.4](SAVED_STATE_FASTCONNECT.md#94-the-deadlines)).

**A commit that cannot complete is abandoned exactly as a cut would leave it.** With no live writer (never backed,
held by an unread slot, or revoked by a lapsed deadline, a reported flash failure or the manager alarm), nothing can
make the state durable, so the drain ends at once. A writer that heartbeats but never commits is stopped by the
deadline. Either way the reload abandons the firmware's sequence at a command boundary, which is one of the instants
a cut can land on; the A/B contract keeps the authoritative slot either way.

**The configuration logic never reads a busy flash.** A NOR flash busy with an erase or a program does not return
array data, so a reload then would read no bitstream. The HOLD phase lasts longer than the media's worst-case 64 KiB
sector erase, tSE(max) 3,000 ms, and equals the writer's own pinned erase wait. Any operation that started before the
hold has finished before the IPROG word. A conformant writer starts none during it: it commits only work that is
dirty, and the drain ended because none was. The words also repeat every 3,500 ms while the device is still running.

## 5. Why the JTAG-reload defect cannot recur

A JTAG reload is excluded because it is known to leave TX timestamps wrong (this issue, and the #396 owner decision).
The tree records no root cause for that defect: the [FPGA design reference](../fpga/FPGA_DESIGN.md) at the base of #787 carries no note on it.
So the argument is by difference, and the bench check below decides it.

A JTAG reload and the chosen reload reconfigure the FPGA the same way: global set/reset, memory initialization and the
MMCMs relocking. What a JTAG reload does not do, and a power cut does, is outside the FPGA:

- **The PHY is not reset and the link need not drop.** During any reconfiguration the FPGA releases its pins (high
  impedance, pulled up where the configuration enables that), so nothing holds the PHY's reset pin. The PHY keeps its negotiated state and its receive
  clock, and the link partner may never see a link-down, so its gPTP port keeps its measured neighbour delay and rate
  ratio from before the reload.
- **The image may not be the flash image.** A JTAG load writes a bitstream from the host into the configuration memory;
  [QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md) warns that a different build needs its own descriptor image.

The chosen reset removes both. The PHY is held in reset for 3,500 ms before the reload, so the link drops at both ends
and the partner's gPTP port is disabled while it is down, so its peer-delay state machine starts again as after a
cut (IEEE 802.1AS-2011 11.2.15; 11.2.2 determines asCapable through that mechanism). The image is the one
the flash holds at offset 0, the one a power-on loads. What remains different from a cut is power to the PHY, the
flash and the DDR3; a defect that lived there would be one a JTAG reload and a REBOOT share with no other reset.

**The bench decides.** The #396 `power` area grades, after every soft reset, that asCapable returns and that both ends'
measured link delay, the reference peer's computed from the DUT's Pdelay_Resp transmit timestamp and the DUT's own from
its Pdelay_Req transmit timestamp (802.1AS-2011 11.2.15, 10.2.4.7), stays within a tolerance of its pre-reset value.
A wrong TX timestamp moves one of them.

## 6. After the reset

| #396 power-area check | Clause | Where it is graded |
|---|---|---|
| the eight Milan state items are restored | issue #70's inventory, Milan v1.2 5.3.8.2/5.3.8.3 | `power.state-restored`, every cycle |
| ADP re-advertises within its valid time | Milan v1.2 5.6.2 (valid_time 10, 20 s), 5.6.1 | `power.adp-valid-time`, from T0, the host-timestamped REBOOT command |
| gPTP locks again with correct TX timestamps | IEEE 802.1AS-2011 11.2.2, 11.2.15 | `power.gptp-relock`, every soft reset |
| bound streams rebind inside #75's bound | Milan v1.2 5.5.1.4, 5.5.2.6; #75 | `power.automatic-restore-bound` and `power.rebind-bound` |

The soft reset itself is graded by `power.reboot-reset`: the REBOOT is answered SUCCESS, ENTITY_DEPARTING leaves after
the response (Milan v1.2 5.6.3.3, the SHUTDOWN event), and the DUT's link drops within 11 s of T0, the drain and
egress bounds rounded up. The egress wait is what puts ENTITY_DEPARTING on the wire before the link drops. Before the
reload the device has already left the network: ENTITY_DEPARTING tells every controller, and the processor serves no
command after the response. The ADP budget is 20 s from T0. The reset spends about 3,503 ms of it on a durable state,
and the rest is the power-on path's configuration and boot, as for a cut.

The [UART smoke](../integration/BAREMETAL_FIRMWARE.md#uart-commands) grades the console a REBOOT leaves behind with
`--after-reboot`: one BIOS pass, then the gPTP lock and the measured peer delay it grades after a flash.

## 7. Evidence

| Evidence | What it proves |
|---|---|
| [`tb/verilator/reboot_ctrl`](../../tb/verilator/reboot_ctrl/README.md) | every drain exit; the egress account (frames in the MAC at the request, a frame in progress held back across ticks, a take on the clock of an end, a flush, a stray end) and the port's stop; every bound against the documented and derived values at three tick phases and at two MAC statements, with the stated bound from the request to the IPROG word; the eight words bit-reversed, the PHY hold held through and after them, the retry, a one-clock request, resets during the hold and the words; 33 planted mutants, each caught by its named check |
| [`tb/verilator/pp_shadow`](../../tb/verilator/pp_shadow/README.md) section `[RB]` | the real wiring from an AECP REBOOT on the MAC RX port, graded at a MAC model's wire-side output: SUCCESS, the notification and ENTITY_DEPARTING whole and in order before the PHY hold, the hold more than a tick and at most two after the last frame, no frame started at the port from the egress wait on while KL_maap offers some, the words after the hold and their retry; without advertising, no DEPARTING and the hold after the last frame the port started; with a dead transmit clock, the hold at the egress bound; a refused REBOOT resets nothing; no cycle of the rest of the run holds the PHY or drops CSIB. `make reboot-mutant` plants seven arms, each caught by its named check: the request ignored, an early request, the PHY hold on the request alone, an egress wait that ignores the MAC FIFO or has no bound, the toggle unwired and the stop unwired |
| `sw/builder/test_builder.py` gates 1f and 23m | the FIFOs built from the named depths, the statement from `_mac_tx_egress_octets` and the PHY table, the toggle reset-less in `eth_tx` on `phy.sink`'s last octet, the no-MAC stub's zero toggle, nine cuts each refused by name; every config's Instance binding exactly the builder's evaluated statement |
| The shipping route | the resource gate on `route-1x1`, `ooc-1x1` and `ooc-8x8` ([SUBMODULES.md](../reference/SUBMODULES.md), the #787 adoption record) |
| The bench | the #396 `power` area's 50 soft resets on the shipping image, the manager's step after merge |
