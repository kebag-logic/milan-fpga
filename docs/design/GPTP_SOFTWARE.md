<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# gPTP in firmware

On the optimisation line, gPTP runs in the split firmware.
The owner decided it on 2026-11-21 ([#872](https://github.com/kebag-logic/milan-fpga/issues/872)).
The fabric gPTP plane is removed there; the hardware timestamps and the PHC stay in fabric.
This page is the design of [#884](https://github.com/kebag-logic/milan-fpga/issues/884) and #665 F6 on that line.
The product line keeps the [fabric plane](GPTP_PLANE.md) until the gPTP qualification passes.

## Contents

- **[Ownership](#ownership)** — What leaves the fabric, what stays, and who owns each piece.
- **[The timestamp unit](#the-timestamp-unit)** — The two stamp points, the reconstruction and its guards, the record FIFO.
- **[Contract 2.5](#contract-25)** — The gptp channel, the TIMESTAMP event and the gPTP publication.
- **[The firmware port](#the-firmware-port)** — One IEEE 802.1AS end station an interface, behind a HAL.
- **[Why not flexPTP as it is](#why-not-flexptp-as-it-is)** — The measured reasons for a fixed-point core.
- **[Service bounds](#service-bounds)** — What each gPTP path is held to, and what is provisional.
- **[Verification](#verification)** — The benches, their planted defects and the closed loop.
- **[Open items](#open-items)** — What this round leaves, and what the owner decides.

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

Milan v1.2 8.3.4 runs one gPTP an interface.
So each AVB interface is a one-port end station with its own PHC.
The [stream engines](MARK_II_STREAM_ENGINES.md) already plan one PHC a port.
Today's fabric has one MAC, so one timestamp unit and one PHC exist.

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

The FIFO holds eight records a port.
A record it cannot hold is counted at `GPTP_DROPW[31:16]`.
A port's event messages run at about twelve a second, so it never fills in service.

## Contract 2.5

Minor 5 only adds, by the contract's own rule.

| Item | What it carries | Clause |
|---|---|---|
| Channel `gptp`, id 5 | Untagged frames to `01-80-C2-00-00-0E`, EtherType `0x88F7`, both ways; 16 a burst, one every 10 ms (provisional) | IEEE 802.1AS-2020 11.3.4, 11.3.5 |
| Event `TIMESTAMP`, value 9 | One record: sequenceId, messageType, direction, OK, 64-bit ns | IEEE 802.1AS-2020 11.3.9 |
| Publication `GPTP_*`, 22 words an interface | GM, parent, peer delay, state, eight path entries | Milan v1.2 5.4.2.23, 5.4.2.24 |

TIMESTAMP is the one event that is not coalesced.
Each record is a measurement, so each is posted once, in the order it was timed.
`KL_mbx_cdc` returns a credit when KL_mbx takes it, so none is overwritten.

The firmware writes every `GPTP_*` word, then `GPTP_STATE` with `GEN` moved.
`KL_mbx_cdc` crosses the words when `GEN` moves, as one snapshot.
So a grandmaster identity never crosses half-written.
`DISC` and `PATH_GEN` are counters; the datapath turns each move into its old pulse.

The words leave KL_mbx on one port, `pub_gptp_o`.
The datapath decodes them onto the plane's own `gptp_pub_*` nets.
So every existing consumer keeps its meaning and its RTL.

## The firmware port

`struct gptp_port` holds one port's whole state; nothing is global.
The two ports of a redundant entity are two instances.

It implements the time-aware end station of IEEE 802.1AS-2020 clauses 10 and 11:

- Peer delay as initiator in every state and as responder (11.2.19, 11.2.20).
- neighborRateRatio over four exchanges, a median of three delays.
- asCapable after two good exchanges with a measured rate (Milan v1.2 4.2.6.2.4).
- The fifth lost response clears it (allowedLostResponses 3); 800 ns is the threshold.
- The Pdelay_Req cease after three multi-answered requests, ended by a link edge (Milan v1.2 4.2.6.2.5).
- The BMCA of a one-port end station with path trace (10.3); receipt timeouts (Milan v1.2 Table 4.2).
- Two-step Sync and Follow_Up as slave and as grandmaster, Announce each second.

Every constant is the fabric engine's protocol table, value for value.

The servo keeps the engine's policy: 20 µs link-up and 100 µs locked step thresholds.
It also keeps the 200 ppm clamp and the slew-active level of gptp-processor #75.
Its PI gains are derived from the PHC's clock and the Sync interval.
Both closed-loop poles sit at 0.6 a pair.
The second pair after a step seeds the integrator with the measured frequency error.

The port uses no floating point and no heap.
It divides 64 bits only on slow paths, by shift and subtract.
The split image refuses libgcc's 64-bit divides on the RV32IM hart.

The HAL is four calls: send a frame, adjust the rate, step the time, and the time base.
On the split, `gptp_mbx.c` sends on the gptp ring and the PHC is the CSR's PTP block.

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
So this round ports a minimal fixed-point core behind the same HAL.
flexPTP's 802.1AS decisions informed it: asCapable rules, the delay median, the rate window.
Adopting flexPTP itself instead is an owner decision.

## Service bounds

NFR-SCOUT-03 requires each gPTP path to state and test its firmware service bound.

| Path | Bound | Basis | Measured, 1x1/1if |
|---|---|---|---:|
| Pdelay_Req received to Pdelay_Resp committed | 10 ms, provisional | IEEE 802.1AS-2011 B.2.3; Milan v1.2 4.2.6.2.6 tolerates 15 ms | 0.193 ms |
| Sync egress stamp to Follow_Up committed | 125 ms | followUpReceiptTimeout, Milan v1.2 Table 4.2 | one pass |
| A pass carrying gPTP work | THE SHARE | `ctrl_loop.h` | at most 0.195 ms |

The 10 ms row is a new family, `gptp`, in the harness.
No existing row reads it, and the owner decides it.

## Verification

| Bench | What it proves | Planted defects |
|---|---|---|
| `sw/firmware/ctrl/test/test_gptp.cpp` | The port's clauses on scripted frames; two ports over simulated PHCs | 25, `gptp_mutants.py` |
| `tb/verilator/gptp_tsu` | Both stamp points, 426 ns and 3,770 ns, the guard, the seal, the FIFO | 16, `tsu_mutants.py` |
| `tb/verilator/gptp_sw` | The firmware locks over the mailbox model and the real stamp path, as slave and as grandmaster | none yet |
| `tb/verilator/ctrl_service_budget` | The ports' cycles on the split CPU; the turnaround; the share | the harness's own |

The closed loop runs the firmware's port, adapter, loop and driver on the host mailbox model.
Its fabric half is the PHC counter, the launch observer and the timestamp unit, in Verilator.
Its peer is an independent model with its own clock.

## Open items

- The fabric plane's own suites still build its RTL; they move with the plane's deletion.
- The 8x8 images with gPTP exceed the memory ledger: 58.5 and 63.5 RAMB36.
- A second PHC and timestamp unit come with the second MAC.
- The pad-oracle bench, `tb/verilator/gptp_txts`, still grades the plane's ledger, not the unit.
- The bench qualification of the 802.1AS clauses is owed before this line ships.
