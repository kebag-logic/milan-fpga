# Mark II stream engines at 32x32

This page designs the Mark II datapath at 32x32.
It is a proposed design; no RTL implements it yet.

Each figure is marked as a measurement or an estimate.
Measurements name their source; estimates name their basis.

The [owner decisions of 2026-10-31](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545621753) set the shape.
The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md#mark-ii-end-state) sets the ownership.

## Contents

- **[Scope and status](#scope-and-status)** -- What this design covers.
- **[The 32x32 shape and its wire load](#the-32x32-shape-and-its-wire-load)** -- Frames and idleSlope.
- **[Shared engines](#shared-engines)** -- One packetizer, one depacketizer, contexts in RAM.
- **[Talker capture buffer](#talker-capture-buffer)** -- Eight slots, sized by the packet.
- **[Packet-boundary stagger](#packet-boundary-stagger)** -- Phases set by wire time.
- **[Talker latency budget](#talker-latency-budget)** -- One format meets it at 16 reservations.
- **[Listener path and render buffer](#listener-path-and-render-buffer)** -- Sized by offset, per rate.
- **[Redundancy pairing and listener merge](#redundancy-pairing-and-listener-merge)** -- Index parity, time bases, merge.
- **[Per-port MAC, filter and timestamp units](#per-port-mac-filter-and-timestamp-units)** -- What each port adds.
- **[Register maps](#register-maps)** -- Engine registers and both context layouts.
- **[Block RAM ledger at 32x32](#block-ram-ledger-at-32x32)** -- An estimate 23 tiles over.
- **[The 0.5 s save path](#the-05-s-save-path)** -- Append-only, under 360 ms.
- **[Verification](#verification)** -- How each claim gets checked.
- **[Open questions](#open-questions)** -- Decisions the owner still owes.

## Scope and status

The shape is 32x32: 16x16 logical streams, one TDM8 bus.
Each logical stream is redundant on both networks.

So the entity has 32 talker and 32 listener streams.
Each AVB interface carries 16 of each direction.

This page covers the fabric between pins and MACs.
Protocol control is firmware, per the split contract.

It also derives the firmware's 0.5 s save path.
The [area plan](MARK_II_AREA_PLAN.md) owns the LUT and Block RAM totals.

Requirements: [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest), [NFR-LAT-03](../reference/FR_NFR.md#31-performance--real-time) and NFR-REL-03.
Nothing here changes RTL, firmware, a generator or a gate.

## The 32x32 shape and its wire load

Milan v1.2 6.2 fixes the base formats.
They are AAF PCM, 32-bit, with N channels.

N is one of 1, 2, 4, 6 and 8.
The rate is 48, 96 or 192 kHz.

A PDU carries 6, 12 or 24 samples per channel.
Every PDU carries a timestamp, not sparse mode.

IEEE 1722-2016 7.6 keeps that sample count constant.
One TDM8 bus and one media clock fix the rate.

Channel counts may differ from stream to stream.
Milan v1.2 Table 4.4 fixes each reservation.

| Quantity | Value | Derivation |
|---|---:|---|
| AVTPDU, N channels at 48 kHz | 24 + 24N octets | 24-octet AAF header; N x 6 samples x 4 octets |
| Frame on the wire | 24N + 66 octets | AVTPDU + 22 (Ethernet header with VLAN tag, FCS) + 20 (preamble and IFG); Table 4.4 note: at least 68 before the 20 |
| Reservation per stream | 1536N + 4288 kb/s | Table 4.4: MaxFrameSize 24N + 25, the same steps, x 8 bits x 8,000 per s |
| CRF stream, one timestamp per PDU | 88 octets; 5,632 kb/s | Table 4.4: MaxFrameSize 29, padded to 68, plus 20 |
| Class A AAF frames per port | 128,000 per s | 16 streams x 8,000 PDUs per s |
| Frames per s, both ports, each way | 256,000 | 2 ports x 128,000 |

| N at 48 kHz | Frame, octets | Wire time, µs | Reservation, kb/s |
|---:|---:|---:|---:|
| 1 | 90 | 0.720 | 5,824 |
| 2 | 114 | 0.912 | 7,360 |
| 4 | 162 | 1.296 | 10,432 |
| 6 | 210 | 1.680 | 13,504 |
| 8 | 258 | 2.064 | 16,576 |

| 16 eight-channel streams and one CRF per port | 48 kHz | 96 kHz | 192 kHz |
|---|---:|---:|---:|
| Eight-channel frame on the wire | 258 octets, 2.064 µs | 450 octets, 3.600 µs | 834 octets, 6.672 µs |
| Reservation per stream | 16,576 kb/s | 28,864 kb/s | 53,440 kb/s |
| Class A idleSlope per port | 270.848 Mb/s, 27.08 % | 467.456 Mb/s, 46.75 % | 860.672 Mb/s, 86.07 % |
| Within the 75 % class A default | Yes | Yes | No: at most 13 eight-channel streams with a CRF |

IEEE 802.1Q-2022 34.3.1 sets that 75 % default.
Sixteen eight-channel streams per port need 48 or 96 kHz.

These are derived figures, not measurements.

## Shared engines

Replicating today's stream logic cannot meet the target.
#819 measured 1,514 fabric LUTs per stream pair.

Replicated to 32 pairs, that adds about 47k LUTs.
So one engine serves every stream instead.

- One time-multiplexed packetizer builds every talker frame.
- One time-multiplexed depacketizer parses every listener frame.
- Each stream's state lives in a Block RAM context.
- An added stream costs context words, not LUTs.

### Per-stream contexts in Block RAM

A talker context is 16 words of 32 bits.
A listener context is 32 words, counters included.

The render map holds one entry per TDM slot.

The engine reads a context, works, then writes it back.
Firmware writes the configuration words through the engine window.

The [register maps](#register-maps) give both layouts.
Counters update by read-modify-write inside the engine.

### Engine throughput

The datapath runs at 50 MHz with 32-bit beats.
Each engine moves 1,600 Mb/s of beats.

| Step | Cycles at 50 MHz | Basis (estimate) |
|---|---:|---|
| Context read and write | 4 | Two-port Block RAM, pipelined |
| Ethernet and VLAN header | 5 | 18 octets |
| AAF header | 6 | 24 octets |
| Payload | 6N, 12N or 24N | 24N, 48N or 96N octets at 48, 96 or 192 kHz |
| Turnaround | 1 | Frame boundary |
| CRF frame, whole | 22 | Headers, one timestamp and padding |

| Rate | Eight-channel frame | Worst legal load per engine | Mix that reaches it, per port |
|---|---:|---:|---|
| 48 kHz | 64 cycles, 1.28 µs | 33.47 % | 16 eight-channel streams and a CRF |
| 96 kHz | 112 cycles, 2.24 µs | 58.05 % | 16 eight-channel streams and a CRF |
| 192 kHz | 208 cycles, 4.16 µs | 93.18 % | 14 eight-channel streams, no CRF: 748.160 Mb/s reserved |

Each row is the largest load over every legal mix.
Mixes of 1 to 16 streams per port were enumerated.

The 75 % class A default limits the 192 kHz row.
At 16 reservations its maximum is 92.67 %.

The depacketizer has the same per-frame cost.
At 192 kHz both engines run close to full.

## Talker capture buffer

The capture side writes each TDM frame into one ring.
The ring holds eight slots, one per TDM channel.

Its depth follows the packet interval, not the stream count.
A packet needs six samples; the ring keeps sixteen.

```
capture ring = 8 slots x 16 samples x 32 bits = 4,096 bits = 512 octets
             = one RAMB18 at 48 kHz (estimate)
96 kHz:  16 -> 32 samples, 1,024 octets, one RAMB18
192 kHz: 16 -> 64 samples, 2,048 octets, one RAMB18
```

The channel map selects slots per stream channel.
Milan v1.2 5.3.9.1 saves that map.

## Packet-boundary stagger

All talker streams share one media clock.
If every packet closed on one sample, frames would collide.

Sixteen frames per port would then queue at once.
The shaper would start the last about 114 µs later.

So each stream closes its packets on its own phase.
There are 6, 12 or 24 phases per 125 µs.

IEEE 1722-2016 7.5 permits this offset.
Each PDU's timestamp names its own first sample.

IEEE 1722-2016 7.6 needs only a constant sample count.
It sets no common packet boundary across streams.

### The phase rule

Firmware picks the phase when the stream starts.
It takes the phase with the least wire time.

Wire time sums the running streams' frames in that phase.
A CRF stream counts like any other.

Ties go in a fixed spread order.
At 48 kHz it is `0, 3, 1, 4, 2, 5`.

At 96 and 192 kHz the order halves the gaps.
The phase never changes while the stream runs.

IEEE 1722-2016 7.6's constant count forbids that.
Within a phase, smaller frames are built first.

A CRF frame goes last in its phase.
Sixteen equal streams fill the phases `3, 3, 2, 3, 3, 2`.

### What the rule cannot prevent

The rule balances wire time only when a stream starts.
It cannot rebalance when other streams stop.

Heavy frames can then stay clustered among light ones.
idleSlope falls with them, as it sums current reservations.

Starts and stops alone reach this 48 kHz mix:

- Phase 0 holds three eight-channel streams.
- Phase 1 holds five two-channel streams.
- The other eight streams carry one channel each.

Its class idleSlope is 133.120 Mb/s.
Phase 1's last frame waits 53.085 µs for credit.

## Talker latency budget

Start: the packet's last sample at the TDM pin.
End: its frame's first bit on the wire.

[NFR-LAT-03](../reference/FR_NFR.md#31-performance--real-time) sets 65 µs for every talker stream.
The [owner](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545820658) called that target ideal on 2026-10-31.

A CRF stream carries no TDM sample.
So the bound applies to its AAF streams.

### The class A shaper

Milan v1.2 4.3.4 requires both shaping levels.
It cites 34.6.1 of `[802.1Q]`.

Milan v1.2's reference list makes that IEEE 802.1Q-2014.
IEEE 802.1Q-2022 numbers it 34.6.1.1.

That clause sums stream idleSlopes into the class idleSlope.
Assumption: that sum covers the current reservations.

At 32x32 that is 16 AAF streams, plus any CRF.
The per-stream level never holds a frame here.

Frames reach it at their release, 125 µs apart.
Frame bits over stream idleSlope stay under 125 µs.

The CRF's equals 125 µs, so it never holds either.
Clause 8.6.8.2 then fixes the class pacing.

After a frame of L bits, credit is negative.
Credit is back at zero L / idleSlope after the start.

Without interference, credit is never positive at a start.
So the start times follow one queue recursion:

```
start(k) = max(release(k), start(k-1) + L(k-1) / idleSlope)
wait(X)  = max over phases g up to X's own:
             (bits queued ahead of X since phase g) / idleSlope
           - (time from phase g to X's phase)
```

An 8.6.8.2 simulation confirmed it.
It simulated 300 random mixes at each rate.

### Interference

A lower-priority frame may hold the wire first.
IEEE 802.1Q-2022 L.3.1.1 a) bounds it.

It is one maximum frame, or mediumAccessDelay if larger.
Credit gained while blocked lets later frames catch up.

So one such frame bounds every frame's extra wait.
The model checked that against a saturated best-effort queue.

The bound needs two properties of this talker's egress:

- A1: no frame on an AVB port exceeds 1522 octets.
- A2: LPI is never asserted on an AVB port.

IEEE 802.1BA-2011 6.3 caps frames at 2000 octets.
1522 octets is only its basic-header example.

A2 is option a) of IEEE 802.1BA-2011 6.1.
Option b) would allow a 30 µs wake time.

The implementation enforces and tests both.

```
interference with A1 and A2 = (1522 + 20) octets x 8 / 1 Gb/s = 12.336 µs
with 2000-octet frames        = (2000 + 20) octets x 8 / 1 Gb/s = 16.160 µs
```

### The fixed terms

| Term | 48 kHz, µs | 96 kHz, µs | Basis |
|---|---:|---:|---|
| Pin to capture | 18.229 | 9.115 | Release at the TDM frame's end; a stream mapped only to slot 0 waits 7 of 8 slots |
| Capture clock-domain crossing | 0.200 | 0.200 | Four 50 MHz cycles (0.080 µs), rounded up to 0.200 µs (estimate) |
| Packetizer, largest phase, both ports | 8.560 | 9.840 | 2 x (192 + 22) and 2 x (224 + 22) cycles at 50 MHz: three or two eight-channel frames and a CRF (estimate) |
| One interfering frame | 12.336 | 12.336 | A1 and A2 above |
| MAC launch and PHY | 1.000 | 1.000 | 426 ns register stages, 219 ns PHY egress, rest margin (estimate) |
| **Sum of the fixed terms** | **40.325** | **32.491** | |

The packetizer and shaper terms are both counted in full.
A later ready time delays starts by no more.

The packetizer term holds for mixed formats too.
Let j be the stream that joined phase p last.

When j joined, no phase was lighter than p.
Each port runs at most 17 streams, the CRF included.

At 48 kHz, say p held over 4,128 bits.
That is two eight-channel frames, so three or more streams.

The five others held three each: 19 streams, over 17.
With j, p never holds over 6,192 bits.

Eight-channel frames cost the most cycles per bit.
So a phase's AAF frames need at most 192 cycles.

A CRF adds 22 cycles per port.
With both ports, that is 8.560 µs.

At 96 kHz, p held at most one eight-channel frame.
More needs two streams in each of 12 phases.

So a phase needs at most 224 cycles.
With a CRF and both ports: 9.840 µs.

Each fits its phase, 20.833 or 10.417 µs.
So no frame waits on an earlier phase's build.

The pin term takes the worst slot.
Release after each stream's last slot would cut it.

At 192 kHz a frame's packetizer time exceeds a phase.
So the model treats the packetizer there as a queue.

### Results at 16 reservations per port

The model covers every legal base-format mix at each rate.
Where full enumeration was too large, it bounds a superset.

| Rate | Formats on the port | Shaper wait, µs | Derived bound, µs | Against 65 µs | Method |
|---|---|---:|---:|---|---|
| 48 kHz | One format, any N | 23.106 | 63.431 | Met | Exact: all 17,658 states that starts and stops reach |
| 48 kHz | Mixed N | 53.085 reached; at most 55.542 | 92.530 reached; at most 95.867 | Not met | Reached under the exact rule; bounded over a superset of it |
| 96 kHz | One format, any N | 18.802 | 51.293 | Met | Exact: all 351,488 reachable states |
| 96 kHz | Mixed N | 43.215 reached; at most 60.725 | 74.826 reached; at most 93.216 | Not met | As at 48 kHz |
| 192 kHz | One format, N up to 6 | - | 34.861 | Met | Exact: all 34 reachable placements; packetizer as a queue |
| 192 kHz | Mixed N | 57.905 reached; at most 57.905 | 84.319 reached; at most 100.825 | Not met | All 34 placements; formats over a superset; packetizer bounded |

The superset uses a necessary condition of the rule.
When a stream joins a phase, no phase is lighter.

With 16 streams at most, that bounds each phase's content.
The witnesses are reached by the exact rule itself.

At 192 kHz every start finds an empty phase.
It takes the first empty phase in the tie order.

Sixteen streams then fill 16 of its first 17 phases.
A CRF holds the 17th, or it stays empty.

So 34 placements exist, and the model searched each.
A search of every start and stop confirms the set.

Its mixed bound adds 24.827 µs of packetizer delay.
That is the largest over every placement and mix.

```
192 kHz, mixed: 57.905 + 24.827 + 18.093 = 100.825 µs at most
18.093 = pin 4.557 + CDC 0.200 + MAC 1.000 + interference 12.336
```

At 16 reservations, one format per port meets 65 µs.
Mixed formats do not; the [open questions](#open-questions) list it.

With fewer reservations some cases exceed it, as [shown below](#fewer-reservations-on-a-port).

The model is lane evidence, not a gate.
An implementation lane must turn it into a test.

### Fewer reservations on a port

The table above holds at 16 reservations per port.
Fewer reservations make it worse.

idleSlope shrinks with the reservations.
Co-phased streams then wait longer for credit.

| Running eight-channel streams at 48 kHz, no CRF | idleSlope | Last frame's shaper wait | With interference | Total, with every fixed term | Against 65 µs |
|---|---:|---:|---:|---:|---|
| Two in phase 0 only | 33.152 Mb/s | 62.259 µs | 74.595 µs | 102.584 µs | Not met |
| Three in phase 0 only | 49.728 Mb/s | 83.012 µs | 95.348 µs | 123.337 µs | Not met |
| Two, phases 0 and 1 | 33.152 Mb/s | 41.425 µs | 53.761 µs | 81.750 µs | Not met |
| Two, phases 0 and 3 | 33.152 Mb/s | 0.000 µs | 12.336 µs | 40.325 µs | Met |

Totals add the 48 kHz fixed terms, 40.325 µs.

Starts and stops reach each of these rows.
Alone, k co-phased streams wait about `(k - 1) x 125 / k` µs.

Re-phasing a running stream would break IEEE 1722-2016 7.6.
Padding reservations would break Milan v1.2 Table 4.4.

### The latency instrument

The Mark II taps measure the requirement's own interval.
They start at the pin, not at the capture register.

Capture stamps each TDM frame end on both PHCs.
One clock edge latches both stamps.

It subtracts the synchronizer's fixed delay from each stamp.
It also subtracts the slots after the stream's last slot.

That is the pin instant of the packet's last sample.

The end is the launch observer's first-bit time.
The PHY egress constant is added to it.

Each port's launch observer stamps in its own PHC.
So a copy's interval uses its own port's PHC throughout.

Even copies use port 0's PHC; odd copies, port 1's.
No offset between the two PHCs enters the interval.

`SE_TLAT_*` and `TCTX_TLAT_MAX` record that interval.
`SE_TLAT_OVER` counts frames at or above 65 µs on it.

The bench calibrates the reconstruction once.
An external capture of pin and wire is the reference.

## Listener path and render buffer

The depacketizer matches a frame to a listener context.
It compares destination and stream_id against the port's 16 contexts.

Two compares per cycle take eight cycles per frame.
It needs 160 ns; a minimum frame lasts 672 ns.

Only mapped channels are written to the render buffer.
Only eight slots reach the TDM pins.

The buffer is indexed by presentation time.
IEEE 1722-2016 7.5 dates each PDU's first sample.

Milan v1.2 4.4.2.1 sets its size.
It must hold up to 2.126 ms of samples.

Its parts: a 2 ms offset, 125 µs, 1 µs.
IEEE 802.1Q-2022 34.6.1.2 states it generally.

This design keeps 2.25 ms, above that minimum.
It covers the 2 ms default offset and one packet.

A talker adds up to 125 µs more.
Milan v1.2 5.3.7.6 allows that.

So the depth follows the offset, not the stream count.

| Rate | Samples for 2.25 ms | Depth, samples | Buffer, 8 slots x depth x 32 bits | Block RAM (estimate) |
|---|---:|---:|---:|---|
| 48 kHz | 108 | 128, 2.667 ms | 32,768 bits | One RAMB36 |
| 96 kHz | 216 | 256, 2.667 ms | 65,536 bits | Two RAMB36 |
| 192 kHz | 432 | 512, 2.667 ms | 131,072 bits | Four RAMB36 |

NFR-SCUP-01 includes 192 kHz in the rate set.
So the ledger books the 192 kHz size, four RAMB36.

An image without 192 kHz would need one or two.
The buffer serves all 32 listener streams through the map.

The buffer's two ports run on two clocks.
So it also crosses into the audio clock domain.

Today's render path spends three RAMB36 on that crossing.
The shared buffer replaces them.

Offsets above 2.667 ms overflow it at every rate.
They count as `EARLY_TIMESTAMP` (Milan v1.2 5.3.8.10).

## Redundancy pairing and listener merge

Milan v1.2 8.2.2 names the two interfaces.
AVB_INTERFACE 0 is Primary; index 1 is Secondary.

Milan v1.2 8.2.4 binds streams to interfaces.
IEEE 1722.1-2021 7.2.6 carries that as avb_interface_index.

This design pairs descriptors by index parity.
Even indices are primary; odd indices are secondary.

Stream 2k+1 is the secondary partner of stream 2k.
Milan v1.2 8.2.5 defines the pair.

Each descriptor's redundant_streams field (Annex C) names its partner.
The pairing is a builder convention, not a Milan rule.

Milan v1.2 8.3.5.1 requires distinct stream_ids.
Both carry the same samples on separate networks.

### Time domains

Milan v1.2 8.3.4: one gPTP per interface.
So each network has its own time.

IEEE 1722-2016 4.4.4.9 bases avtp_timestamp on gPTP.
So each copy carries its own port's time.

The talker reads the capture once for both copies.
It stamps the even copy in port 0's time.

It stamps the odd copy in port 1's time.
The conversion adds the offset between the two PHCs.

The fabric latches both PHCs on one edge.
It does so every 125 µs.

The media clock follows one port's time, the reference port.
The listener converts the other port's timestamps into it.

It applies the same measured offset in reverse.
Each context's `PORT` bit names its own time base.

### Conversion error bound

The listener compares the two copies of one packet.
After conversion, their times differ by a bounded error.

On each network, talker and listener agree within 1 µs.
IEEE 802.1AS-2020 B.3 sets it, within seven hops.

Milan v1.2 4.4.2.1 assumes it too.
So the two offsets differ by at most 2 µs.

Each offset is up to 125 µs old.
Each grandmaster runs within 100 ppm of nominal.

IEEE 802.1AS-2020 B.1.1 sets that frequency bound.
So an offset drifts at most 25 ns per latch.

Each PHC read adds one granule, at most 40 ns.
IEEE 802.1AS-2020 B.1.2 bounds that granule.

```
E_x = 2 x 1 µs              B.3, one per network
    + 2 x 125 µs x 200 ppm  two latches, two grandmasters
    + 4 x 40 ns             four PHC reads, B.1.2
    = 2.000 + 0.050 + 0.160 = 2.210 µs
```

Assumption A3: both networks meet B.3 in steady state.
A copy with tu set has no such bound.

### The merge

The listener merges each pair into one render stream.
The even context holds the pair's merge state.

That state is a head and a written map.
The head is the newest written packet's time and position.

The map holds one bit per recent packet.
Bit k marks the packet k intervals before the head.

The render buffer spans 2.667 ms, under 22 packets.
So a 22-bit map covers every packet still renderable.

The render point is the time now at the pins.

#### Clean copies

A clean copy's time names its packet.
Its offset from the head is `k = round((t - head) / 125 µs)`.

Each packet's tolerance window is 62.5 µs either side.
Clean partner copies differ by at most 2.210 µs.

Neighbouring packets differ by 125 µs, less drift.
At 200 ppm, 22 packets drift under 0.6 µs.

So a partner always matches; a neighbour never does.

#### Copies with tu set

IEEE 1722-2016 4.4.4.7 covers the tu bit.
A listener may then stop trusting presentation times.

So a tu copy's time names no packet.
Its `sequence_num` places it (IEEE 1722-2016 4.4.4.6).

Each context keeps its last `sequence_num` and that packet's time.
A tu copy's packet is that time plus the count.

The count is a signed 8-bit difference; reordering is safe.
During tu the head advances by that count.

#### Placement

Samples are placed by count from the head.
Packet k lands k packets of samples from the head.

So conversion error never shifts a sample.
A new anchor alone uses its own time.

#### Rules

The first matching rule acts:

| Rule | When | Action | Counter |
|---:|---|---|---|
| 1 | The copy fails a stream check: its format (Milan v1.2 4.4.2.2), or a late or early time (Milan v1.2 5.3.8.10) | Not rendered | That check's Milan v1.2 5.3.8.10 counter |
| 2 | The copy has tu set, and the partner context's `CLEAN_VALID` is set | Discarded | `SE_MERGE_TU` |
| 3 | `HEAD_VALID` is clear, or a tu copy has no valid sequence reference | Rendered at its own time; it anchors the head and clears the map | `SE_MERGE_SEC` if odd |
| 4 | A clean copy while `ANCHOR_TU` is set, or more than 21 packets from the head | Re-anchors, as rule 3 | `SE_MERGE_SEC` if odd |
| 5 | k is 1 or more: newer than the head | Rendered k packets after the head; it becomes the head | `SE_MERGE_SEC` if odd |
| 6 | k is 0 to -21, and map bit -k is clear | Rendered k packets from the head; sets that bit | `SE_MERGE_SEC` if odd |
| 7 | Any other copy: its packet is already written | Discarded as a duplicate | `SE_MERGE_DUP` |

A clean head takes its copy's own time.
A tu head advances by the count, in render-clock time.

No rule drops the only valid copy of a packet.
A tu copy never writes while clean partner data remains.

So uncertain time on one network cannot disturb the other.
The window counts each duplicate once, in `SE_MERGE_DUP`.

Annex D.2 of Milan v1.2 models per-network buffers.
Clean partner data is a non-empty buffer there.

Before any clean copy arrives, a tu copy may anchor.
The first clean copy then re-anchors by rule 4.

#### Reference upkeep

Every copy passing rule 1 updates its reference.
A clean copy also sets `CLEAN_VALID` and `LCTX_CLEAN_PT`.

Every 125 µs a sweep reads every context.
It clears valid bits whose time the render point passed.

Every valid time then stays within 2.667 ms.
Wrapping compares stay exact (IEEE 1722-2016 4.4.4.9).

The sweep uses the context RAM's second port.
So the engines lose no cycles to it.

An unpaired stream applies every rule but rule 2.
For a pair, losing one network loses no samples.

Milan v1.2 Annex D.3 covers losing one network.
Loss plus tu on the other network goes beyond it.

The audio then gaps for up to one presentation offset.

Milan v1.2 8.3.2.1.4 pairs mappings.
Both streams of a pair map the same channels.

## Per-port MAC, filter and timestamp units

Milan v1.2 8.3.1 requires two AVB-capable ports.
Each port gets its own MAC, filter and timestamp unit.

| Unit | Per port | Basis |
|---|---|---|
| MAC | 1 Gb/s GMII MAC on AXI-Stream | LiteX stage 2 replaces LiteEth with a proven core |
| Receive filter | Ternary match on destination, EtherType and VLAN | Today's TCAM measures 494 LUTs placed (2026-10-31) |
| Mailbox ingress filter | Shared, with the interface index in each record | [Product ownership](../../REQUIREMENTS.md#1-product-ownership) already carries the index |
| Timestamp unit | Launch observer, egress return and ingress tap | IEEE 802.1AS-2020 8.4.3 timestamps and latency corrections |
| PHC | One clock per port, disciplined by its gPTP instance | Milan v1.2 8.3.4; one gPTP end station per interface |
| Class A shaper | One per port, idleSlope from that port's reservations | IEEE 802.1Q-2022 8.6.8.2 and 34.6.1.1 |
| Stream frame FIFO | Receive side, absorbs bursts while the engine serves the other port | One RAMB36 (estimate) |
| Egress frame queue | Class A frames waiting for credit | One RAMB36, fifteen frames (estimate) |

The timestamps stay at the GMII boundary today.
So they carry over to the new MAC unchanged.

F6 adds a gPTP mailbox channel carrying them.
After F6, the fabric runs no gPTP state machine.

## Register maps

The maps follow the technical reference manual style.
Offsets are bytes from the block base.

Resets are hexadecimal; `PORT` resets to the index parity.
Every bit and offset is defined or reserved.

Reserved bits read zero; writes to them are ignored.
Access codes: R read-only, RW read-write.

RC clears on read; WS acts on a written 1.
FW means firmware writes it and the engine reads it.

Firmware writes configuration through the engine window.
`milan_csr` exposes the status and counter words read-only.

Every Milan counter is 32 bits and wraps to zero.
Milan's Tables 5.4 and 5.6 require that.

Each counter's reset event is in its row.
An engine reset clears every counter and state word.

### Engine registers

| Offset | Name | Bits | Field | Reset | Access | Description |
|---|---|---|---|---|---|---|
| 0x000 | SE_ID | 31:16 | MAJOR | 0x0001 | R | Engine layout major version |
| | | 15:0 | MINOR | 0x0000 | R | Engine layout minor version |
| 0x004 | SE_CAP | 7:0 | N_TALKER | 0x20 | R | Talker contexts, 32 at 32x32 |
| | | 15:8 | N_LISTENER | 0x20 | R | Listener contexts, 32 at 32x32 |
| | | 20:16 | MAX_PHASE | 0x18 | R | Most phases per class A interval: 24, at 192 kHz |
| | | 21 | TWO_PORT | 0x1 | R | Second AVB interface present |
| | | 31:22 | RESERVED | 0x000 | R | Reads zero; writes ignored |
| 0x008 | SE_CTRL | 0 | TALKER_EN | 0x0 | RW | Enables the packetizer |
| | | 1 | LISTENER_EN | 0x0 | RW | Enables the depacketizer |
| | | 31:2 | RESERVED | 0x0000_0000 | R | Reads zero; writes ignored |
| 0x00C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |
| 0x010 | SE_IDLESLOPE0 | 31:0 | KBPS | 0x0000_0000 | RW | Port 0 class A idleSlope, kb/s: firmware writes the Table 4.4 sum of the port's current reservations (IEEE 802.1Q-2022 34.6.1.1) |
| 0x014 | SE_IDLESLOPE1 | 31:0 | KBPS | 0x0000_0000 | RW | Port 1 class A idleSlope, kb/s, the same way |
| 0x018-0x01C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |
| 0x020 | SE_TLAT_MAX0 | 31:0 | NS | 0x0000_0000 | RC | Port 0 worst pin-to-first-bit interval, ns ([instrument](#the-latency-instrument)); both ends in port 0's PHC time |
| 0x024 | SE_TLAT_MAX1 | 31:0 | NS | 0x0000_0000 | RC | Port 1 worst pin-to-first-bit interval, ns; both ends in port 1's PHC time, no PHC offset applied |
| 0x028 | SE_TLAT_OVER | 15:0 | COUNT0 | 0x0000 | RC | Port 0 frames at or above 65 µs, pin to first bit in port 0's PHC time; saturates at its maximum |
| | | 31:16 | COUNT1 | 0x0000 | RC | Port 1 frames at or above 65 µs, pin to first bit in port 1's PHC time; saturates at its maximum |
| 0x02C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |
| 0x030 | SE_MERGE_DUP | 31:0 | COUNT | 0x0000_0000 | RC | Copies discarded by merge rule 7: their packet was already written; wraps |
| 0x034 | SE_MERGE_SEC | 31:0 | COUNT | 0x0000_0000 | RC | Packets first written from a secondary (odd) copy, merge rules 3 to 6; wraps |
| 0x038 | SE_MERGE_TU | 31:0 | COUNT | 0x0000_0000 | RC | Copies with tu set discarded by merge rule 2: clean partner data remained; wraps |
| 0x03C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |
| 0x040-0x05C | SE_RMAP[0..7] | 4:0 | LCTX | 0x00 | RW | Render slot k at 64 plus 4k: the listener context feeding it; a redundant pair is named by its even context |
| | | 7:5 | CH | 0x0 | RW | The stream channel that feeds slot k |
| | | 8 | VALID | 0x0 | RW | Slot k is mapped; 0 renders silence (Milan v1.2 5.3.10.1: each slot takes at most one stream channel) |
| | | 31:9 | RESERVED | 0x00_0000 | R | Reads zero; writes ignored |
| 0x060-0x7FC | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |
| 0x800-0xFFC | SE_TCTX[0..31] | - | - | - | - | Talker contexts, 64 octets each, below |
| 0x1000-0x1FFC | SE_LCTX[0..31] | - | - | - | - | Listener contexts, 128 octets each, below |

### Talker context

Context n sits at 2,048 plus 64 times n.
The engine owns the state and counter words.

| Offset | Name | Bits | Field | Reset | Access | Description |
|---|---|---|---|---|---|---|
| 0x00 | TCTX_CTRL | 0 | RUN | 0x0 | FW | Stream started (Milan v1.2 5.3.7.3); the engine builds frames while set |
| | | 1 | PORT | 0x0 for even n, 0x1 for odd n | R | 0 primary, 1 secondary: index parity; also the copy's time base |
| | | 6:2 | PHASE | 0x00 | FW | Packet-boundary phase, 0 to 5, 11 or 23 at 48, 96 or 192 kHz |
| | | 7 | RESERVED | 0x0 | R | Reads zero; writes ignored |
| | | 11:8 | NCH | 0x0 | FW | Channels per frame: 1, 2, 4, 6 or 8 (Milan v1.2 6.2); any other value sets ERR |
| | | 13:12 | NSR | 0x0 | FW | 0 is 48 kHz, 1 is 96 kHz, 2 is 192 kHz; 3 sets ERR |
| | | 14 | ERR | 0x0 | R | NCH, NSR, PHASE or a SLOT field is invalid; the stream does not start; cleared by a valid write |
| | | 31:15 | RESERVED | 0x0_0000 | R | Reads zero; writes ignored |
| 0x04 | TCTX_MAP | 31:0 | SLOT[7:0] | 0x7654_3210 | FW | Four bits per stream channel c, at bits 4c+3 to 4c: its TDM capture slot, 0 to 7; 15 means not mapped, sent as zero samples; 8 to 14 set ERR (Milan v1.2 5.3.9.1) |
| 0x08 | TCTX_SID_LO | 31:0 | STREAM_ID | 0x0000_0000 | FW | stream_id bits 31:0 (IEEE 1722-2016 4.4.4.8) |
| 0x0C | TCTX_SID_HI | 31:0 | STREAM_ID | 0x0000_0000 | FW | stream_id bits 63:32 |
| 0x10 | TCTX_DA_LO | 31:0 | DA | 0x0000_0000 | FW | Destination MAC bits 31:0, from MAAP |
| 0x14 | TCTX_DA_HI | 15:0 | DA | 0x0000 | FW | Destination MAC bits 47:32 |
| | | 27:16 | VID | 0x000 | FW | VLAN identifier, 12 bits |
| | | 28 | DEI | 0x0 | FW | Drop eligible indicator |
| | | 31:29 | PCP | 0x0 | FW | Priority code point of the SR class |
| 0x18 | TCTX_PTO | 30:0 | NS | 0x001E_8480 | FW | Presentation time offset, ns; reset is 2 ms (Milan v1.2 5.3.7.6) |
| | | 31 | RESERVED | 0x0 | R | Reads zero; writes ignored |
| 0x1C | TCTX_STATE | 7:0 | SEQ | 0x00 | R | Next sequence_num (IEEE 1722-2016 4.4.4.6) |
| | | 8 | MR | 0x0 | R | Media clock restart toggle (IEEE 1722-2016 4.4.4.3) |
| | | 31:9 | RESERVED | 0x00_0000 | R | Reads zero; writes ignored |
| 0x20 | TCTX_STREAM_START | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.7.7; increments when RUN rises; never cleared by a start |
| 0x24 | TCTX_STREAM_STOP | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.7.7; increments when RUN falls; never cleared by a start |
| 0x28 | TCTX_MEDIA_RESET | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.7.7; cleared when RUN rises, each time the talker starts |
| 0x2C | TCTX_TIMESTAMP_UNCERTAIN | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.7.7; cleared when RUN rises |
| 0x30 | TCTX_FRAMES_TX | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.7.7; cleared when RUN rises |
| 0x34 | TCTX_TLAT_MAX | 31:0 | NS | 0x0000_0000 | RC | This stream's worst pin-to-first-bit interval, ns; both ends in the PHC time of the port `PORT` names |
| 0x38-0x3C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |

Interval counters use observation intervals of at most 1 s.
Milan v1.2 5.3.7.7 sets that limit.

### Listener context

Context n sits at 4,096 plus 128 times n.
The engine owns the state, merge and counter words.

| Offset | Name | Bits | Field | Reset | Access | Description |
|---|---|---|---|---|---|---|
| 0x00 | LCTX_CTRL | 0 | RUN | 0x0 | FW | Bound and started (Milan v1.2 5.3.8.2, 5.3.8.7) |
| | | 1 | PORT | 0x0 for even n, 0x1 for odd n | R | 0 primary, 1 secondary: index parity; also the copy's time base |
| | | 2 | PAIRED | 0x0 | FW | Context n XOR 1 is this stream's redundant partner |
| | | 3 | CNT_CLR | 0x0 | WS | Clears every counter of this context; firmware writes it when the stream input goes from not bound to bound (Milan v1.2 5.3.8.10) |
| | | 7:4 | RESERVED | 0x0 | R | Reads zero; writes ignored |
| | | 11:8 | NCH | 0x0 | FW | Channels per frame: 1, 2, 4, 6 or 8 (Milan v1.2 6.2); any other value sets ERR |
| | | 13:12 | NSR | 0x0 | FW | 0 is 48 kHz, 1 is 96 kHz, 2 is 192 kHz; 3 sets ERR |
| | | 14 | ERR | 0x0 | R | NCH or NSR is invalid; the context matches no frame; cleared by a valid write |
| | | 31:15 | RESERVED | 0x0_0000 | R | Reads zero; writes ignored |
| 0x04 | LCTX_SID_LO | 31:0 | STREAM_ID | 0x0000_0000 | FW | Bound stream_id bits 31:0 |
| 0x08 | LCTX_SID_HI | 31:0 | STREAM_ID | 0x0000_0000 | FW | Bound stream_id bits 63:32 |
| 0x0C | LCTX_DA_LO | 31:0 | DA | 0x0000_0000 | FW | Stream destination MAC bits 31:0 |
| 0x10 | LCTX_DA_HI | 15:0 | DA | 0x0000 | FW | Stream destination MAC bits 47:32 |
| | | 27:16 | VID | 0x000 | FW | Expected VLAN identifier, 12 bits |
| | | 31:28 | RESERVED | 0x0 | R | Reads zero; writes ignored |
| 0x14 | LCTX_STATE | 7:0 | SEQ | 0x00 | R | Last sequence_num seen on this context (IEEE 1722-2016 4.4.4.6); with LCTX_SEQ_PT, the reference that places a copy with tu set |
| | | 8 | LOCKED | 0x0 | R | Media locked on this stream |
| | | 9 | ANCHOR_TU | 0x0 | R | Even context: the head's position came from a copy with tu set; merge rule 4 reads it |
| | | 10 | SEQ_VALID | 0x0 | R | SEQ and LCTX_SEQ_PT are a valid reference; cleared by the sweep when the render point passes LCTX_SEQ_PT |
| | | 11 | CLEAN_VALID | 0x0 | R | This context holds clean data ahead of the render point; the partner's merge rule 2 reads it; cleared by the sweep when the render point passes LCTX_CLEAN_PT |
| | | 31:12 | RESERVED | 0x0_0000 | R | Reads zero; writes ignored |
| 0x18 | LCTX_LAST_PT | 31:0 | NS | 0x0000_0000 | R | Even context: the head's presentation time, render time base; a clean head takes its copy's time, a tu head advances by count |
| 0x1C | LCTX_MERGE | 21:0 | WMAP | 0x00_0000 | R | Even context: bit k set when the packet k intervals before the head is written |
| | | 30:22 | HEAD_POS | 0x000 | R | Even context: render buffer index of the head packet's first sample |
| | | 31 | HEAD_VALID | 0x0 | R | Even context: the head is valid; cleared by the sweep when the render point passes LCTX_LAST_PT |
| 0x20 | LCTX_MEDIA_LOCKED | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x24 | LCTX_MEDIA_UNLOCKED | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x28 | LCTX_STREAM_INTERRUPTED | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x2C | LCTX_SEQ_NUM_MISMATCH | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x30 | LCTX_MEDIA_RESET | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x34 | LCTX_TIMESTAMP_UNCERTAIN | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x38 | LCTX_UNSUPPORTED_FORMAT | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x3C | LCTX_LATE_TIMESTAMP | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x40 | LCTX_EARLY_TIMESTAMP | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x44 | LCTX_FRAMES_RX | 31:0 | COUNT | 0x0000_0000 | R | Milan v1.2 5.3.8.10; cleared by CNT_CLR |
| 0x48 | LCTX_SEQ_PT | 31:0 | NS | 0x0000_0000 | R | Packet time of the copy with SEQ, render time base; counted for a copy with tu set |
| 0x4C | LCTX_CLEAN_PT | 31:0 | NS | 0x0000_0000 | R | Time of this context's newest clean copy, render time base |
| 0x50-0x7C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |

Unbinding keeps the counters, per 5.3.8.10.

Each render slot takes at most one stream channel.
Milan v1.2 5.3.10.1 sets that rule.

A redundant pair renders through its even context.

## Block RAM ledger at 32x32

Of 135 tiles, 121.5 are usable after the reserve.
A RAMB18 counts as half a tile.

Every row below is an estimate unless it says measured.

| Item | Tiles | Basis |
|---|---:|---|
| Talker contexts, 32 x 64 octets | 0.5 | One RAMB18 |
| Listener contexts, 32 x 128 octets | 1.0 | One RAMB36 |
| Talker capture buffer | 0.5 | One RAMB18, above |
| Listener render buffer | 4.0 | Four RAMB36 for 192 kHz, above; replaces three |
| Egress frame queues, two ports | 2.0 | One RAMB36 per port |
| Receive stream FIFOs, two ports | 2.0 | One RAMB36 per port |
| MAC clock-crossing FIFOs, two ports | 4.0 | Two RAMB36 per port, LiteX stage 2 |
| Packet mailboxes | 6.0 | Measured: one RAMB36 and ten RAMB18 ([F0](MAILBOX_SPLIT.md#measured-area)) |
| Timestamp and gPTP receive FIFOs | 1.0 | Two ports |
| Media clock and CRF | 0.5 | Today's CRF listener row |
| `milan_csr` | 1.0 | Measured placed, 2026-10-31: two RAMB18 |
| CPU | 4.5 | Measured placed, 2026-10-31: two RAMB36, five RAMB18 |
| **Fabric subtotal** | **27.0** | |
| Firmware memory, linear extrapolation to 64 streams | 113.0 | From the two measured two-interface points below |
| No whole-image save staging | -11.5 | Append-only save path; extrapolated stage size |
| gPTP daemon allowance | 16.0 | Not measured; F6 measures it |
| **Total** | **144.5** | 23 tiles over the usable 121.5 |

```
measured, split control memory, two interfaces (SPLIT_CONTROL_MEMORY.md section 5):
  1x1 (2 streams):  rom 98,056 B  + sram 57,152 B
  8x8 (16 streams): rom 111,848 B + sram 112,464 B
per stream:  rom 13,792 / 14 = 985 B,  sram 55,312 / 14 = 3,951 B
64 streams:  rom 98,056 + 62 x 985 = 159,126 B
             sram 57,152 + 62 x 3,951 = 302,114 B
total        461,240 B / 4,096 B per RAMB36 = 112.6, so 113 tiles
stage:       3,344 + 62 x (13,264 - 3,344) / 14 = 47,275 B, about 11.5 tiles
```

On these estimates the 32x32 image does not fit.
Firmware memory, not LUTs, binds first.

Candidate reductions, each still to be measured:

- Names served from flash: 14.2 tiles, worst case.
- The descriptor image from flash: about 15, overlapping names.
- Size per-stream pools from the 32x32 model, not linearly.
- Share one CRF stream instead of one per port.

The [area plan](MARK_II_AREA_PLAN.md#mark-ii-block-ram-ledger) carries this ledger.
Its lanes must measure each row before relying on it.

## The 0.5 s save path

[NFR-REL-03](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) bounds a save at 0.5 s worst case.
It runs from the change to durable flash, at 32x32.

The [owner confirmed](https://github.com/kebag-logic/milan-fpga/issues/823#issuecomment-6545924397) that reading on 2026-10-31.
#823 owns the format; #665 F1 owns the writer.

Today a whole-image commit takes 3.07 s at 1x1.
A 64 KiB erase is 3 s of that.

At 32x32 programming alone would take about 1.2 s.
So a save must append, never rewrite or erase.

### Media maxima

The derivation follows the [saved-state deadlines](SAVED_STATE_FASTCONNECT.md#94-the-deadlines).
It uses the N25Q128 datasheet maxima.

| Parameter | Maximum | Source |
|---|---:|---|
| tPP, one page of up to 256 octets | 5 ms | N25Q128 Table 32, AC characteristics |
| tSE, one 64 KiB sector erase | 3 s | Table 32 |
| tSSE, one 4 KiB subsector erase | 2 s | Table 32 |
| Erase suspend latency | 15 µs typical, no maximum given | Table 17, suspend parameters |
| Endurance | over 100,000 cycles per sector | Datasheet features |

Table 17 states no maximum suspend latency.
This design allows 1 ms and must measure it.

Section 9.1.20: a suspended sector erase allows programming.
A suspended subsector erase forbids it.

So background erases use whole 64 KiB sectors.

### Save sequence

1. Firmware applies the change and marks its records dirty.
2. The writer suspends any background sector erase.
3. It appends the dirty records to the active slot.
4. It reads each page back and checks it.
5. The save is durable once its last page checks.
6. The writer resumes the background erase.

A page failing read-back is rewritten to the next page.
Such a retry is a reported fault outside the bound.

Each save suspends and resumes the erase once.
Table 17 gives 40 µs typical from resume to suspend.

Each record carries its own sequence and check.
A torn record fails its check; the older value stands.

A multi-record transaction ends with a commit record.
Boot ignores a transaction without one.

No debounce timer runs on this path.
Changes made during a save join the next save.

### Worst-case derivation

The clock is today's 12.5 MHz single-lane flash clock.
LiteX stage 2 may only shorten the transfer terms.

```
page program command  (1 + 3 + 256) octets x 8 / 12.5 MHz = 0.166 ms
write enable and status polls                              = 0.011 ms (allowance)
tPP maximum                                                = 5.000 ms
page read-back        (1 + 3 + 256) octets x 8 / 12.5 MHz = 0.166 ms
t_page                                                     = 5.344 ms, used as 5.35 ms

per save, at most P_max = 32 pages (8,192 octets)

T_worst = T_svc + (compaction page in flight) + 2 x T_suspend
          + (save in flight) + (this save)
        = 10 ms + 5.35 ms + 2 x 1 ms + 32 x 5.35 ms + 32 x 5.35 ms
        = 359.75 ms  <=  500 ms, margin 140.25 ms (28 %)
```

T_svc is the 10 ms service budget of NFR-SCOUT-03.
The save in flight is one a change just missed.

A save waits for at most one compaction page.
Compaction yields to saves only between pages.

Both saves suspend the erase, so T_suspend counts twice.
Each 1 ms allowance also covers the resume-to-suspend spacing.

#823 and #665 F1 restate `T-NVM-COMMIT-TIMEOUT`, 8,000 ms today.
The [owner's 2026-10-31 direction](https://github.com/kebag-logic/milan-fpga/issues/823#issuecomment-6545894131) requires it.

One save holds about 100 name records or 240 bindings.
Any single AEM command's change fits in two pages.

### Compaction and slot size

At 32x32 the live image is about 60 KB.
That is 240 pages, #823's estimate on 2026-10-31.

A 64 KiB slot would leave too little append space.
So each slot grows to four sectors, 256 KiB.

| Quantity | Value | Basis |
|---|---:|---|
| Slots | 2, of 4 sectors each, 512 KiB in all | Today: 2 x 64 KiB, 128 KiB |
| Pages per slot | 1,024 | 256 KiB / 256 octets |
| Append space per slot | 784 pages | 1,024 - 240 |
| Compaction trigger | 392 pages free | Half the append space |
| Compaction work | 240 pages, 1.28 s at full share; at most 311 pages, within 2.05 s, under S1 and S2 | 240 x 5.35 ms; the [replay bound](#assumptions) below |
| Background erase of the old slot | 12 s | 4 x tSE |
| Boot read of one slot | 168 ms | 256 KiB x 8 / 12.5 MHz |

Compaction copies the live state into the pre-erased standby slot.
It serializes from the live tables, with no staging buffer.

Saves have strict priority at every page boundary.
A pending save always runs before the next compaction page.

So each copy page holds durable values only.
Until the header, saves keep appending to the active slot.

1. Note the active log's end; a replay cursor starts there.
2. Copy the live tables into the standby, page by page.
3. Replay every record from the cursor on, page by page.
4. Once the cursor meets the log end, write the header.
5. From then on, saves append to the new slot.
6. Erase the old slot later; it is the next standby.

Step 4's check and its header page are one step.
No save can run between them.

A save arriving during the header page waits for it.
That wait is the compaction page already in T_worst.

The header carries a higher generation and its own check.
Boot applies the copy, then records in sequence order.

A later record of a key replaces an earlier one.
The cursor replays every record appended since step 1.

So each key's newest durable value comes last.

| A save lands | It appends to | It reaches the slot that survives because |
|---|---|---|
| Before step 1 | The active slot | Its value is durable, so step 2 copies it from the live tables |
| Between copy pages, step 2 | The active slot, after the cursor | Step 3 replays every record from the cursor on |
| Between replay pages, step 3 | The active slot, after the cursor | Step 4 cannot pass until the cursor has replayed it |
| At the boundary after the last replay page | The active slot: strict priority runs it before step 4's check | The check then fails, and step 3 replays it first |
| Between step 4's check and the header page | Impossible: the check and the header page are one step | - |
| During the header page | Nothing until that page ends; then the new slot | The new slot is the one that survives |
| After a header that fails its read-back | The old slot, still active | Compaction erases the standby and restarts from step 1 |
| After the header, before or during step 6 | The new slot | Its generation is higher; the save suspends the erase as any save does |

| Power cut during | Boot uses | Why nothing saved is lost |
|---|---|---|
| A save append, at any step | The slot in use | A torn record fails its check; that save was not yet durable |
| The copy or the replay, steps 2 and 3 | The old slot | The new slot has no valid header; every durable save is in the old slot |
| The header page, step 4 | The old slot | A torn header fails its check; a save waiting on it was not yet durable |
| After the header, before or during step 6 | The new slot | Its generation is higher, and it holds every durable record |

An unfinished standby is erased again after a cut.
Compaction then restarts from step 1.

The layout change belongs to #823.
The generated flash map stays the single source.

### Assumptions

The bound needs two limits on the change rate.

- S1: changes made during one save fit 32 pages.
- S2: sustained saves stay below 10 % of the flash rate.

At datasheet maxima the flash writes 187 pages per second.
S2 allows about 4.8 KB per second, sustained.

The replay bound reads S2 exactly; S1 is its burst.
Strict priority leaves compaction all the remaining flash time.

```
S2 exactly: in any interval t, saves program at most 32 + 0.1 t / p pages
            p = 5.35 ms; their flash time is at most 32 p + 0.1 t
compaction pages done by t  >= (0.9 t - 32 p) / p - 1
compaction needs              240 copy + A replay + 1 header pages
A, appended since step 1    <= 32 + 0.1 t / p
not done at t only if         0.9 t / p - 33 < 273 + 0.1 t / p, so t < 382.5 p
done by                       382.5 x 5.35 ms = 2.046 s
A                           <= 32 + 0.1 x 382.5 = 70.25, so 70 pages
work                        <= 240 + 70 + 1 = 311 pages
```

So step 3 replays at most 70 pages.
Compaction ends within 2.05 s of step 1.

Meanwhile 70 appends cannot fill 392 free pages.

```
after compaction the new slot holds <= 311 pages, so >= 713 are free
next trigger, 392 free, needs >= 321 appended pages: t >= 289 p / 0.1 = 15.46 s
old slot's erase, 12 s of flash: 0.9 x 15.46 - 0.17 - 0.32 = 13.42 s free by then
            (0.32 s: at most 321 saves, each suspending the erase for 1 ms)
```

So the standby is erased before the next compaction starts.
Under S1, every change meets 0.5 s.

A burst beyond S1 drains at the flash's worst-case rate.
Rewriting all 907 names would take about 1.5 s.

That case needs the owner's reading.
The [open questions](#open-questions) list it.

## Verification

| Claim | Method | Evidence still owed |
|---|---|---|
| Engine throughput | Analysis above; RTL simulation at 256,000 frames per s each way | Simulation with both ports at full load |
| Talker latency at 32x32 | Analysis above; the executable model of IEEE 802.1Q-2022 8.6.8.2 at every rate | Mark II taps on all 32 talker streams on the bench, with one format and with mixed formats per port |
| Latency instrument time base | Simulation: an odd context with a non-zero, drifting PHC offset; its recorded interval equals the pin-to-wire time, and so does an even context's | Bench: an external capture of pin and wire on each port, against `TCTX_TLAT_MAX` of an even and an odd context |
| Phase rule | The model's starts and stops | Firmware test: phase chosen by wire time, never moved while running |
| Stagger conformance | IEEE 1722-2016 7.5 and 7.6 inspection | Listener interoperability with the reference peer |
| Listener merge | Simulation of every rule: both copies clean with a jittered conversion error up to 2.210 µs and up to 1.5 ms between networks, either network faster; times 1 µs past a sample boundary; one network cut mid-stream; 1 % frame loss on either network, filled from the later copy; the secondary with tu set, its time skewed by plus or minus 30 µs, plus or minus 200 µs and plus 1 ms, arriving before the primary; a cut, then a grandmaster change on the surviving network. Rendered samples equal the clean stream's, and `SE_MERGE_DUP` counts each packet's second copy once. The test fails with an exact time compare, with each copy placed by its own time, or without rule 2 | Bench cable pull on each network, no lost samples; a grandmaster change on one network with both up, no disturbed samples |
| Conversion error bound | Analysis above (IEEE 802.1AS-2020 B.1.1, B.1.2, B.3) | Bench capture of both copies of each packet; the converted times differ by at most 2.210 µs |
| Port time bases | Simulation: each copy's avtp_timestamp against its own port's PHC | Bench capture of both copies on the two networks |
| Block RAM ledger | Estimate above | Routed image at 32x32 with measured firmware |
| Save bound | Analysis above at datasheet maxima | Host flash model at maxima; bench power cuts |
| Compaction keeps saved changes | Ordering and tables above | Host flash model: one save at every page boundary of a compaction, including the one after the last replay page, one during the header page, and a second save at every boundary; a power cut before, inside and after every page; then commit, erase, reboot and read every saved value. The test fails if a save may run between step 4's check and the header page, or if step 3 is skipped |

The shaper model is lane evidence, not a gate.
An implementation lane must turn it into a self-checking test.

## Open questions

1. **Talker latency with mixed formats or fewer reservations.**
   - At 16 mixed reservations, every rate exceeds 65 µs.
   - At 48 kHz a reached mix needs 92.530 µs.
   - No 16-stream 48 kHz mix exceeds 95.867 µs.
   - Three co-phased streams alone wait 83.012 µs for credit.
   - The owner called 65 µs ideal; the choices include these:
     - accept the derived bounds for those cases;
     - restrict each port to one base format;
     - re-phase a running stream, accepting an audio gap;
     - change the stagger or shape decision.
2. **Save bursts.**
   A burst beyond S1 exceeds 0.5 s at maxima.
   The owner may bound it, accept it or change media.
3. **Block RAM.**
   The 32x32 ledger exceeds the usable tiles by 23.
   The reductions above need measuring before lanes rely on them.
4. **Debounce windows.**
   - Today's 500 ms window uses the whole bound.
   - The 1,000 ms window exceeds it.
   - #823 and F1 must restate them inside the bound.
5. **gPTP on two ports.**
   - The surveyed `flexptpd` fork keeps one global core state.
   - Redundancy needs one instance per port (#665 F6).
   - The owner also confirms the fork's source and licence.
6. **Commit timeout.**
   - `T-NVM-COMMIT-TIMEOUT` is 8,000 ms today.
   - The owner's direction restates it against 359.75 ms.
   - #823 and #665 F1 own the new value.
7. **Engine headroom at 192 kHz.**
   - A legal 192 kHz mix loads each engine 93.18 %.
   - It has 14 eight-channel streams and no CRF.
   - A faster clock or wider beats would restore margin.
