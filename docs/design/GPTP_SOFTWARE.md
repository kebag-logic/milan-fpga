<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# gPTP in firmware

On the optimisation line, gPTP runs in the split firmware.
The owner decided it on 2026-11-21 ([#872](https://github.com/kebag-logic/milan-fpga/issues/872)).
The fabric gPTP plane is removed there; the hardware timestamps and the PHC stay in fabric.
This page is the design of [#884](https://github.com/kebag-logic/milan-fpga/issues/884) and #665 F6 on that line.
The product line keeps the [fabric plane](GPTP_PLANE.md) until the gPTP qualification passes.

## Contents

- **[Ownership](#ownership)** -- What leaves the fabric, what stays, and who owns each piece.
- **[The timestamp unit](#the-timestamp-unit)** -- The two stamp points, the reconstruction and its guards, the record FIFO.
- **[Contract 2.5](#contract-25)** -- The gptp channel and its ingress trailer, the TIMESTAMP event and the narrowed gPTP publication.
- **[The firmware port](#the-firmware-port)** -- One IEEE 802.1AS end station an interface, behind a HAL, and its place in the platform image.
- **[Memory](#memory)** -- What gPTP in firmware costs each image, and the ledger entries that hold it.
- **[Why not flexPTP as it is](#why-not-flexptp-as-it-is)** -- The measured reasons for a fixed-point core.
- **[Service bounds](#service-bounds)** -- What each gPTP path is held to, and what is provisional.
- **[Verification](#verification)** -- The benches, their planted defects and the closed loop.
- **[Open items](#open-items)** -- What is left on this line, and what the owner decides.

## Ownership

| Piece | Owner on this line | Where |
|---|---|---|
| BMCA, Announce, Sync and Follow_Up, Pdelay, asCapable, the servo | Firmware, one port an interface | `sw/firmware/ctrl/gptp/gptp.c` |
| The mailbox adapter: channel, events, ticks, publication | Firmware | `sw/firmware/ctrl/gptp/gptp_mbx.c` |
| Ingress and egress stamps of event messages | Fabric timestamp unit | `hdl/ieee8021as/gptp_tsu/KL_gptp_tsu.sv` |
| The launch observer on the MAC's transmit stream | Fabric, unchanged | `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv` |
| The PHC: counter, rate, step, settime | Fabric, the CSR's PTP block (REQ-PTP-01..04) | `timestamp_counter`, `ptp_csr_sync` |
| The consumers: clock validity, GM counters, AVB_INFO, AS_PATH | Fabric, unchanged, fed by the firmware's publication | `milan_datapath.sv`, `g_gptp_sw` |

`milan_datapath` selects the owner at elaboration.
`GPTP_PLANE_EN_P` keeps the fabric plane.
`GPTP_SW_EN_P` builds the timestamp unit in its place, split placement only.
`milan_soc.py --sw-gptp` selects it; the image's gPTP owner is then `software`.

Milan v1.2 8.3.4 runs one gPTP time-aware end station an AVB interface, with no bridge between them.
So each AVB interface has its own PHC and its own timestamp unit, one of each a MAC ([#884's ruling of 2026-11-21](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7067495546), item 5).
The [stream engines](MARK_II_STREAM_ENGINES.md) already plan one PHC a port.
The closed loop builds both, a PHC, a launch observer, a timestamp unit and a control tap an interface, and locks each port to its own grandmaster ([Verification](#verification)).
The split SoC has one MAC today, so it builds one of each; the second MAC is an [open item](#open-items).

## The timestamp unit

The unit keeps the plane's stamp points and corrections exactly.
So the plane's published digital bound still holds: ±11.2 ns on GMII, ±12.6 ns on MII.

| Direction | Stamp point | Correction |
|---|---|---|
| Ingress | The PHC on the edge the first tap beat is accepted | Less `INGRESS_LAT_NS_P` |
| Egress | The PHC on the edge a launch record lands | Less the derived 426 ns (GMII) or 3,770 ns (MII), plus `EGRESS_LAT_NS_P` |

An egress record is a measurement only when the frame was whole.
Its cycle distance must be the expected one, with no abort.
The PHC's trajectory must also be inside the model for the whole window.
That guard and the 200 ppm addend envelope are `KL_gptp_txret`'s, carried over.
Every other event-message launch is a record with `OK` clear, counted at `GPTP_DROPE[31:16]`.

What leaves with the plane is the positional ledger.
The firmware pairs each record with its own frame by messageType and sequenceId.
So the unit seals the observer at one generation and re-seals after an observer reset.

The unit's FIFO holds egress records only, 32 a port, more than the 15 frames the gptp channel's transmit ring holds.
A record it cannot hold is counted at `GPTP_DROPW[31:16]`.
A port's event messages run at about twelve a second, so it never fills in service.

An ingress stamp leaves the unit at the frame's last beat, `rx_stamp_o` with `rx_event_o`, and rides with its frame ([the trailer](#contract-25)).

## Contract 2.5

Minor 5 only adds, by the contract's own rule.

| Item | What it carries | Clause |
|---|---|---|
| Channel `gptp`, id 5 | Untagged frames to `01-80-C2-00-00-0E`, EtherType `0x88F7`, both ways; a burst of 7 an interface, one every 10 ms (derived in `mailbox.yaml` from the worst legitimate coincidence of the seven 802.1AS message kinds in one refill window, #884's ruling of 2026-11-22, item 1); each received record ends in an eight-octet trailer | IEEE 802.1AS-2020 11.3.4, 11.3.5 |
| Event `TIMESTAMP`, value 9 | One egress record: sequenceId, messageType, OK, 64-bit ns | IEEE 802.1AS-2020 11.3.9 |
| Publication `GPTP_*`, 3 words an interface | `GPTP_GM_LO`, `GPTP_GM_HI`, `GPTP_STATE` (domain, asCapable, the synchronization verdict, slew, `DISC`, `GEN`) | Milan v1.2 5.4.2.23, Table 5.22 |

**The trailer.** `KL_ctrl_split` (`GPTP_P`) appends the frame's ingress stamp after its last byte, most significant octet first, or all ones when the frame is no event message.
The stamp is taken at the last beat into a stamp FIFO of 64 entries that moves in step with the frame FIFO.
So a frame the mailbox admits carries its own stamp, and a frame it refuses takes its stamp with it: no stamp of a delivered frame is lost however a burst exceeds the channel's admission (ruling item 2).
A gPTP frame that finds the stamp FIFO full is refused at its second beat and counted with the tap's drops.
The adapter reads the trailer, hands an event message's stamp to its port, then the frame without it.

TIMESTAMP is the one event that is not coalesced.
Each record is a measurement, so each is posted once, in the order it was timed.
`KL_mbx_cdc` returns a credit when KL_mbx takes it, so none is overwritten.
The event names no hart: contract 2.6 routes it, with LINK, to gPTP's hart.

**The narrowed publication** (ruling item 7). Under `--sw-gptp` the datapath's consumers read only what fabric logic needs: the grandmaster for the clock validity and the GM counters, asCapable and the verdict for the clock validity, `DISC` for its discontinuity pulse.
The parent, the peer delay and the path trace are no longer published; their CSR reads are zero under `--sw-gptp` ([register map](../reference/REGISTER_MAP.md)).
The firmware writes `GPTP_GM_LO`, `GPTP_GM_HI`, then `GPTP_STATE` with `GEN` moved.
`KL_mbx_cdc` copies the three into its committed bank the cycle after `GEN` moves and crosses that bank, never the live words.
So a word the firmware writes after a commit reaches no delivered snapshot, however long the crossing before it is in flight.
A commit made while one crosses is crossed next; one a later commit overtakes before the crossing is free is not crossed, the later one being whole.
The host model takes its snapshot at the same write (`mbx_model.c`), and `tb/verilator/mbx/tb_cdc_pub.sv` holds the RTL to both.
The words leave KL_mbx on one port, `pub_gptp_o`, and the datapath decodes them onto the plane's own `gptp_pub_*` nets.

GET_AVB_INFO's gPTP fields and GET_AS_PATH are answered by the firmware from the snapshot it published last (`gptp_mbx_snapshot`, `aecp_face_gptp`).
So an answer is the publication the datapath holds, its GEN's state.
The datapath's AVB_INFO and AS_PATH change detectors are off under `--sw-gptp`; the adapter raises both changes to the AECP owner itself (Milan v1.2 Table 5.22).

## The firmware port

`struct gptp_port` holds one port's whole state; nothing is global.
The two ports of a redundant entity are two instances.

It implements the time-aware end station of IEEE 802.1AS-2020 clauses 10 and 11:

- Peer delay as initiator in every state and as responder (11.2.19, 11.2.20).
- neighborRateRatio over four exchanges, a median of three delays.
- Peer delay runs on the LocalClock 802.1AS takes as never stepped (11.2.19.3.3): the PHC less every step the servo has applied to it.
  The port's own t1 and t4, and the t2 and t3 it reports to a peer, are taken on it, so a step of either of two such ports, of any size, moves no rate window and no turnaround, and asCapable holds across it at turnarounds up to 10 ms.
  A step also voids the exchange in flight and completes no response the port owes, whose stamps are the old time.
- For a peer that stamps on a stepped PHC instead: a window whose ratio lies further from 1 than two in-tolerance clocks can (2^-12, 244 ppm; B.1.1) holds the step, so it restarts and the last good ratio stays in use.
  That catches a step larger than about 0.7 ms over a window of three seconds; a smaller one can reach the delay at a long turnaround.
  A turnaround longer than its round trip is no measurement.
- asCapable after two good exchanges with a measured rate (Milan v1.2 4.2.6.2.4).
- The fifth lost response clears it (allowedLostResponses 3); 800 ns is the threshold.
- The Pdelay_Req cease after three successive requests each answered from more than one clock identity, whenever in the request's interval the second answer comes; a link edge or five minutes end it (Milan v1.2 4.2.6.2.5).
  Any second response to a request clears asCapable when it is received (10.2.5.1 c), not when its exchange completes, which a missing Follow_Up or the cease would prevent.
- The BMCA of a one-port end station with path trace (10.3); receipt timeouts (Milan v1.2 Table 4.2).
  The sync receipt timeout restarts only when a Sync and its Follow_Up are consumed as a pair (10.2.8.2.1 c), never on a Sync alone.
- Two-step Sync and Follow_Up as slave and as grandmaster, Announce each second.
  A Follow_Up without its information TLV, or with one cut short or malformed, is refused (11.4.4.1, 11.4.4.3).

Every constant is the fabric engine's protocol table, value for value.

The servo keeps the engine's policy: 20 µs link-up and 100 µs locked step thresholds.
It also keeps the 200 ppm clamp and the slew-active level of gptp-processor #75.
Its PI gains are derived from the PHC's clock and the Sync interval.
Both closed-loop poles sit at 0.6 a pair.
The second pair after a step seeds the integrator with the measured frequency error.

The port uses no floating point and no heap.
It divides 64 bits only on slow paths, by shift and subtract.
The split image refuses libgcc's 64-bit divides on the RV32IM hart.

The HAL is three calls: send a frame, adjust the rate and step the time.
Time enters through `gptp_port_tick`, not the HAL.
On the split, `gptp_mbx.c` sends on the gptp ring and the PHC is the CSR's PTP block.

The adapter binds the gptp channel, an event sink and a centisecond, and no poll.
Each of the three publishes the port it ran, in the pass that ran it, so a pass that runs none of them costs nothing (#884).
The platform's poll table is full besides (eight of eight), so the adapter could take no slot there.

**In the platform image.** `ctrl_plat_image.py --with-gptp` builds `plat/ctrl_plat.c` with `CTRL_PLAT_GPTP`: one port an interface, each the EUI-64 of its interface's MAC (IEEE 802.1AS-2020 8.5.2.2), bound after the saved-state store's centisecond and before the mailbox opens.
Its PHC is the PTP block: the rate is `PTP_ADJ`'s signed addend, a step is `PTP_OFFSET`'s delta at `PTP_CMD`'s adjtime strobe, and the PHC's rate is read from `PTP_INCR`'s reset value, the true clock period, without a divide (`ctrl_plat_csr.c`).
The datapath has one PTP block, interface 0's; a port on another interface steers none until the second MAC.
This is the image an SoC built `--sw-gptp` carries. An image without the flag excludes the firmware gPTP owner.
The shared hot-list relearn changes code layout in both image variants.
Measured by `plat_ledger.py` before the relearn at `a6323318` and after it at `631dc544`, the plain 1x1/1if platform image's `rom` grows from 126,632 to 126,640 B and the plain 8x8/2if image's from 140,952 to 140,960 B; their `sram` and RAMB36 allocations are unchanged ([platform memory](SPLIT_CONTROL_MEMORY.md#5-fit)).

## Memory

Ruling item 4 accepts the gPTP ports' memory at 8x8 and above as debt with a ledger entry; fit and timing gate it ([split control memory](SPLIT_CONTROL_MEMORY.md#3-named-refusals)).

| Image | Without gPTP, RAMB36 | With gPTP, RAMB36 | Ledger entry |
|---|---:|---:|---|
| The size fixture's 8x8, one interface (the harness's `8x8-1if`) | 56.0 | 59.0 | `8x8-one-interface-gptp` |
| The size fixture's 8x8, two interfaces (the harness's `8x8`) | 60.5 | 64.0 | `8x8-two-interfaces-gptp` |
| The platform's 8x8, one interface (the `--sw-gptp` build's) | 58.5 | 62.0 | `platform-8x8-one-interface-gptp` |

A port adds about 12 KB of `rom` and 1 KB of `sram`.

Fit and timing at 8x8/1if, routed at `a6323318` (Vivado 2026.1, the train's recipe, the `--sw-gptp` SoC with the platform's gPTP image at 62.0 RAMB36): 38.1k LUT, 45.9k FF, 95.5 of 135 block RAM tiles and 5 DSP.
All three placement directives meet #818's floor at every signoff corner: ExtraPostPlacementOpt, the best, at WNS +0.292 ns and WHS +0.036 ns; AltSpreadLogic_high at +0.281 ns and +0.036 ns; ExtraTimingOpt at +0.173 ns and +0.067 ns.
The plane, routed at `40bd7738` with the same recipe (ExtraPostPlacementOpt, its image without gPTP at 58.5): 43.2k LUT, 51.3k FF, 11 DSP, the same 95.5 tiles, WNS +0.139 ns.
So the firmware's ports cost the device 3.5 tiles of memory and save it about 5.1k LUT, 5.4k FF and 6 DSP of fabric.
Contract 2.5 itself costs every image a little: the gptp channel's table entries and the face's answer port, 64 B of the platform's `ctrl_plat` and 200 B of `rom` at 8x8 with one interface, which re-measured that entry at 58.5.

## Why not flexPTP as it is

The owner chose flexPTP on #640 for this function.
Its `gptp` branch was measured for the split ISA.
That build is RV32IM, `-Os`, OS-less, every port hook stubbed.

| Property | flexPTP `gptp` branch | This port |
|---|---:|---:|
| Text, bytes | 41,848, before soft-float and libm | 11,674 |
| Static state | 9,525 B, one global instance | 0; about 1 KB a port, the caller's |
| Floating point | `double` and `float` in the servo, rate ratio and BMCA; `exp`, `log2`, `llround` | none |
| Ports | one (`gPtpCoreState`) | one instance an interface |

The split hart has no FPU and its image links no libm.
Two ports would need a donor change to flexPTP's global state.
So this line ports a minimal fixed-point core behind the same HAL.
flexPTP's 802.1AS decisions informed it: asCapable rules, the delay median, the rate window.
Adopting flexPTP itself instead is an owner decision.

## Service bounds

NFR-SCOUT-03 requires each gPTP path to state and test its firmware service bound.
The 10 ms bound and THE SHARE of 2.0 ms are kept by [#884's ruling of 2026-11-21](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7067495546), item 1.

Measured at `631dc544`, the split hot list relearned with the gPTP ports in its image:

| Path | Bound | Basis | 8x8/2if | 8x8/1if |
|---|---|---|---:|---:|
| Pdelay_Req received to Pdelay_Resp committed | 10 ms | IEEE 802.1AS-2011 B.2.3; Milan v1.2 4.2.6.2.6 tolerates 15 ms | 0.292 ms | 0.309 ms |
| A gptp record under the composed load, last released | 10 ms | the gptp family | 7.750 ms | 6.115 ms |
| Sync egress stamp to Follow_Up committed | 125 ms | followUpReceiptTimeout, Milan v1.2 Table 4.2 | one pass | one pass |
| The composed maximum, the gptp burst in every backlog window | THE SHARE, 2.0 ms | `ctrl_loop.h` | 1.657 ms | 1.675 ms |
| A work pass of any group | THE SHARE, 2.0 ms | `share.py` | none over | none over |

The images are built `--with-gptp` and planned at their ledgered points; the CPU is the split's, at 100 MHz.
gPTP takes 0.27 % of it after link-up at 8x8/2if, 0.21 % at 8x8/1if.
Its largest contribution to one work pass is 0.374 ms, in `backlog-owed` at 8x8/2if.
The `gptp` family stays out of THE SHARE, which remains the approved T_svc over ten passes.

A row's defined load covers the channels its image opened, read from the image's `FILTER_EN` write.
An image without gPTP opens five, so every existing row is unchanged; a gPTP image's windows also carry the gptp channel's admitted burst, seven Pdelay_Req records an interface, its dearest ([the harness](../../tb/verilator/ctrl_service_budget/README.md#markers-and-grading)).
With that burst every held-egress row at 8x8/1if is within its egress-ledger figure: `backlog-owed.service.acmp.last.if0` at 62.453 ms against 62.62 (62.640 ms at the provisional burst of 16 that [#884's ruling of 2026-11-22](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7072401468), item 1, replaced by the derived one), and `backlog-owed.service.aecp.last.if0` at 62.123 ms against 62.16.
At 8x8/2if, which has no ledger of its own, the ACMP row is 62.587 ms, and the five owed rows are 63.910 to 64.957 ms, 0.05 to 0.10 ms past the 1if figures.

**The layout.**
Before the relearn, the AECP row was 62.182 ms at `a6323318`, over its figure by 0.022 ms.
The port's code had grown 196 B ahead of `gptp_mbx.c`, and its state by the LocalClock's 8 B.
`gptp_mbx.c` was unchanged and ran in as many passes, yet its cycles over `backlog-owed`'s passes at 8x8/1if rose from 149,287 to 214,320: the cost of where that image placed it against the CPU's caches.
That moved the phase at which the egress hold releases against the passes, and the pass that sends AECP's last record ended 0.100 ms later.
[#884's ruling of 2026-11-22](https://github.com/kebag-logic/milan-fpga/issues/884#issuecomment-7084113326) kept the figure and required the hot list relearned by its recorded procedure with the gPTP ports' and adapter's paths measured into it.
The list is learned so ([`plat/ctrl_split_hot.txt`](../../sw/firmware/ctrl/plat/ctrl_split_hot.txt)), and its 15 entries of `gptp.c` and `gptp_mbx.c` serve the images built with gPTP, which alone compile them.
`gptp_mbx.c`'s cycles over the same passes are now 104,430, and the port's 237,926 (271,145 before).
The relearn reorders the images without gPTP too; at 8x8/1if every held row of theirs is within its figure, the AECP row at 61.840 ms.

## Verification

| Bench | What it proves | Planted defects |
|---|---|---|
| `sw/firmware/ctrl/test/test_gptp.cpp` | The port's clauses on scripted frames; two ports over simulated PHCs, a responder's turnaround up to 10 ms and a step on either side of the link, of any size, inside or across a rate window; the same suite under UndefinedBehaviorSanitizer (the gate's `gptp_ubsan` arm) | 41, `gptp_mutants.py` |
| `tb/verilator/gptp_tsu` | Both stamp points, 426 ns and 3,770 ns, the guard, the seal, the egress FIFO; the trailer read where the mailbox reads it, and an 80-frame flood: 64 kept with their stamps, 16 refused | 24, `tsu_mutants.py` |
| `tb/verilator/milan_dp` (`split-sw`, the suite's last case) | The split datapath built `GPTP_SW_EN_P`: the narrowed words decoded onto the consumers' nets, the detectors off, a commit made while one crosses held whole | the bench's own |
| `tb/verilator/mbx` (`run-cdc-pub`) | `KL_mbx_cdc`'s publication crossing at a datapath clock under and over the mailbox's: every snapshot that lands is one GEN commit's words | 5, `cdc_pub_mutants.py` |
| `tb/verilator/gptp_sw` | The firmware at two interfaces over the mailbox model and two fabric halves; see below | 14, `gptp_sw_mutants.py` |
| `tb/verilator/ctrl_service_budget` | The ports' cycles on the split CPU; the turnaround; the share; at 8x8 the composed rows with the gptp burst | the harness's own |
| `tb/verilator/ctrl_split_boot/plat_ledger.py` | The platform image with gPTP linked and planned at its entry | its nine controls |

The closed loop runs the firmware's ports, adapter, loop and driver on the host mailbox model at two interfaces.
Its fabric half, once an interface, is the PHC counter, the launch observer, the timestamp unit and the split's control tap, in Verilator.
Each peer is an independent model with its own clock, a 300 ns link and Milan's intervals.

- **slave**: each port steps once and locks its own PHC to its own grandmaster within 100 ns by 8 s (about 2.5 s), and the two PHCs stand apart as their grandmasters do.
  Then the published words decode to the snapshot, GET_AVB_INFO and GET_AS_PATH answer the snapshot, and both changes were raised.
  A Pdelay_Req cut short by its last eight octets is refused, not answered; and a grandmaster that falls silent is replaced on its announce receipt timeout, a tick's work, and that change is published.
- **master**: each port is grandmaster and its peer locks to its PHC.
- **flood**: bursts of 32 Pdelay_Req past the channel's admission; the port keeps its lock, the excess is refused or held, and every event message delivered reaches the firmware with its own stamp.
- In every run no pass leaves a port's change unpublished for a later one.

## Open items

- The fabric plane stays buildable on this line for the bench's A/B (ruling item 6); its RTL is deleted only after the in-house qualification passes as slave and as grandmaster (ruling item 3). Its suites and `tb/verilator/gptp_txts`, which grades the plane's ledger, move with it.
- The split SoC's second MAC, and with it the second PHC and timestamp unit in the product build: #962 (cross-referenced to NFR-SCOUT-05); this line keeps one MAC, and the closed loop proves the replication.
- The publication census elaborates the split with the plane; it rules the gPTP ports (`census_split.GPTP_SW_ONLY`). A `GPTP_SW_EN_P` shape is owed before this line merges onward: the census owner rules the rows the sw build ties off, and this line supplies the row list and applies the shape (#884's ruling of 2026-11-22, item 3).
- The rows model counts no gPTP work: `gptp/` links only into a `--with-gptp` image, and no row's image is one.
- The bench qualification of the 802.1AS clauses is owed before this line ships.
