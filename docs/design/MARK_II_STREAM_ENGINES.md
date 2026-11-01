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

[NFR-LAT-03](../reference/FR_NFR.md#31-performance--real-time) sets a 65 µs target for every talker stream.
The [owner](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545820658) called that target ideal on 2026-10-31.

[Owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030), 2026-11-01: 65 µs is a target.
It does not bind every legal stream setup.

Derived bounds for mixed formats and fewer reservations are accepted.
They stay published below.

No connection is refused because of them.
No restriction to one base format applies.

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
Mixed formats do not; the [owner's decision](#talker-latency-budget) accepts their bounds.

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
Read together, the offsets differ by at most 2 µs.

Each grandmaster runs within 100 ppm of nominal.
IEEE 802.1AS-2020 B.1.1 sets that frequency bound.

So the PHC offset drifts at most 200 ppm.
Talker and listener latch it at different instants.

The talker latches at most 125 µs before stamping.
The listener latches before the copy arrives.

A rendered copy arrives before its presentation time (rule 1).
That is at most capture plus offset plus 125 µs.

Milan v1.2 5.3.7.6 sets that term.
The stamp comes after the capture it reads.

Assumption A4: arrival comes within 2.792 ms of stamping.
Offsets up to the 2.667 ms span meet it.

A larger offset needs queueing and transit within it too.
Class A transit: 2 ms (IEEE 802.1BA-2011 6.5).

So the latches lie at most 2.917 ms apart.
The drift term covers that whole interval.

Each PHC read adds one granule, at most 40 ns.
IEEE 802.1AS-2020 B.1.2 bounds that granule.

The capture stamp and the render point add no term.
One reading serves both copies or both compared sides.

```
latch to latch <= 125 µs + 2.792 ms = 2.917 ms
E_x = 2 x 1 µs              B.3, one per network
    + 200 ppm x 2.917 ms    drift between the latches, 0.5834 µs
    + 4 x 40 ns             four PHC reads, B.1.2
    = 2.000 + 0.584 + 0.160 = 2.744 µs, the drift rounded up
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
Clean partner copies differ by at most 2.744 µs.

Neighbouring packets differ by 125 µs, less drift.
At 200 ppm, 22 packets drift under 0.6 µs.

So a partner always matches; a neighbour never does.

#### Copies with tu set

IEEE 1722-2016 4.4.4.7 covers the tu bit.
A listener may then stop trusting presentation times.

This page fixes no merge mechanism for those copies.
[Open design item 2](#open-design-items) states what the lane must meet.

#### Placement

Samples are placed by count from the head.
Packet k lands k packets of samples from the head.

Under a valid head, conversion error never shifts a sample.
A new anchor alone uses its own time.

Both copies' margins under about 125 µs lapse every head.
The threshold carries the conversion error, so it is approximate.

Interleaved copies can then land one sample apart.
[Open design item 3](#open-design-items) owns that case.

No sample is written outside the render buffer.
[Open design item 1](#open-design-items) covers its edges.

#### Rules

These rules take clean copies.
Rule 1's format check also takes every tu copy.

Open design item 2 owns tu copies past that check.

The first matching rule acts:

| Rule | When | Action | Counter |
|---:|---|---|---|
| 1 | The copy fails a stream check: its format (Milan v1.2 4.4.2.2), or a late or early time (Milan v1.2 5.3.8.10) | Not rendered | That check's Milan v1.2 5.3.8.10 counter |
| 2 | No valid head (`HEAD_VALID` clear, or `LCTX_LAST_PT` passed) | Rendered at its own time; it anchors the head and restarts the map with only bit 0 set | `SE_MERGE_SEC` if odd |
| 3 | More than 21 packets from the head | Re-anchors, as rule 2 | `SE_MERGE_SEC` if odd |
| 4 | k is 1 or more: newer than the head | Rendered k packets after the head; it becomes the head | `SE_MERGE_SEC` if odd |
| 5 | k is 0 to -21, and map bit -k is clear | Rendered k packets from the head; sets that bit | `SE_MERGE_SEC` if odd |
| 6 | Any other copy: its packet is already written | Discarded as a duplicate | `SE_MERGE_DUP` |

The head takes its copy's own time.

Past rule 1, a packet's only clean copy always renders.

The window counts each duplicate once, in `SE_MERGE_DUP`.

Annex D.2 of Milan v1.2 models per-network buffers.
Under a valid head, clean copies keep that external behaviour.

An unpaired stream applies the same rules.

Milan v1.2 Annex D.3 covers losing one network.
While the other stays clean, the pair loses no samples.

Milan v1.2 8.3.2.1.4 pairs mappings.
Both streams of a pair map the same channels.

#### Head upkeep

A time the render point passed counts as invalid.
Each rule checks that when it reads the time.

A stale `HEAD_VALID` is swept, one context per 31.25 ms.
No valid time trails the render point by 1 s.

Wrapping compares stay exact (IEEE 1722-2016 4.4.4.9).
The sweep costs 128 cycles per second.

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
| 0x030 | SE_MERGE_DUP | 31:0 | COUNT | 0x0000_0000 | RC | Clean copies discarded by merge rule 6: their packet was already written; wraps |
| 0x034 | SE_MERGE_SEC | 31:0 | COUNT | 0x0000_0000 | RC | Packets first written from a secondary (odd) clean copy, merge rules 2 to 5; wraps |
| 0x038-0x03C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |
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
| 0x14 | LCTX_STATE | 7:0 | SEQ | 0x00 | R | Last sequence_num seen on this context (IEEE 1722-2016 4.4.4.6) |
| | | 8 | LOCKED | 0x0 | R | Media locked on this stream |
| | | 31:9 | RESERVED | 0x00_0000 | R | Reads zero; writes ignored |
| 0x18 | LCTX_LAST_PT | 31:0 | NS | 0x0000_0000 | R | Even context: the head's presentation time, render time base |
| 0x1C | LCTX_MERGE | 21:0 | WMAP | 0x00_0000 | R | Even context: bit k set when the packet k intervals before the head is written |
| | | 30:22 | HEAD_POS | 0x000 | R | Even context: render buffer index of the head packet's first sample |
| | | 31 | HEAD_VALID | 0x0 | R | Even context: the head is valid while LCTX_LAST_PT is ahead of the render point; the sweep clears it after that |
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
| 0x48-0x7C | RESERVED | 31:0 | - | 0x0000_0000 | R | Reads zero; writes ignored |

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

Any non-header page failing read-back is rewritten further on.
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

Fault-free, a save waits for at most one compaction page.
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

The check is a cursor compare, with no flash access.
So no save is taken between it and the header.

A save arriving during the header page waits for it.
That wait is the compaction page already in T_worst.

#### A header that fails its read-back

A read-back can fail on an intact header.
Boot would then prefer it to later saves.

So saves keep waiting, and the writer zeroes that page.
A program only clears bits (N25Q128 5.1.2).

An all-zero header never passes its check.
#823's header format must ensure that.

A zeroed page can fail its read-back too.
The writer then erases the header's sector, saves still held.

That double fault is reported, outside the bound.

Saves resume once the header reads back zeroed or erased.
They append to the old slot, still active.

Compaction then erases the standby and restarts from step 1.

A failed header read-back is a reported fault.
A waiting save then waits one more page.

That makes 365.10 ms, within 0.5 s.

#### Boot and the surviving slot

The header carries a higher generation and its own check.
Boot applies the copy, then records in sequence order.

A later record of a key replaces an earlier one.
The cursor replays every record appended since step 1.

So each key's newest durable value comes last.

| A save lands | It appends to | It reaches the slot that survives because |
|---|---|---|
| Before step 1 | The active slot | Its value is durable, so step 2 copies it from the live tables |
| While another save is in flight, at any step | The same slot, after that save | Saves run one at a time, strictly before the next compaction page; each then lands as its own row says |
| Between copy pages, step 2 | The active slot, after the cursor | Step 3 replays every record from the cursor on |
| Between replay pages, step 3 | The active slot, after the cursor | Step 4 cannot pass until the cursor has replayed it |
| At the boundary after the last replay page | The active slot: strict priority runs it before step 4's check | The check then fails, and step 3 replays it first |
| Between step 4's check and the header page | Impossible: the check and the header page are one step | - |
| During the header page | Nothing until that page ends; then the new slot | The new slot is the one that survives |
| After a header that fails its read-back | Nothing until the header reads back zeroed or erased; then the old slot, still active | That header now fails its check, so boot keeps the old slot; compaction erases the standby and restarts from step 1 |
| After a header that passes its read-back, before or during step 6 | The new slot | Its generation is higher; the save suspends the erase as any save does |

| Power cut during | Boot uses | Why nothing saved is lost |
|---|---|---|
| A save append, at any step | The slot in use | A torn record fails its check; that save was not yet durable |
| The copy or the replay, steps 2 and 3 | The old slot | The new slot has no valid header; every durable save is in the old slot |
| The header page, step 4 | The old slot, or the new slot if its header programmed whole | A torn header fails its check; either slot holds every durable save, and a save waiting on the header was not yet durable |
| After a failed header read-back, until the header reads back zeroed or erased | Either slot | Saves wait meanwhile, so either slot holds every durable save |
| After that, during the standby's erase | The old slot | The standby's header fails its check; every save since is in the old slot |
| After a header that passes its read-back, before or during step 6 | The new slot | Its generation is higher, and it holds every durable record |

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
| Listener merge, clean copies | Simulation of every rule: both copies clean with a jittered conversion error up to 2.744 µs and up to 1.5 ms between networks, either network faster; times 1 µs past a sample boundary; one network cut mid-stream; 1 % frame loss on either network, filled from the later copy. Rendered samples equal the clean stream's; no sample is written outside the render buffer; `SE_MERGE_DUP` counts each packet's second copy once. The test fails with an exact time compare or with each copy placed by its own time | Bench cable pull on each network, no lost samples |
| Copies with tu set | [Open design item 2](#open-design-items): requirements TU-1 to TU-5 and their named cases | That item's bench cases and recorded results |
| Conversion error bound | Analysis above (IEEE 802.1AS-2020 B.1.1, B.1.2, B.3; Milan v1.2 5.3.7.6; assumptions A3 and A4); a host model that drifts two PHCs at plus and minus 100 ppm, latches each every 125 µs and converts at the stamp and the arrival | Bench capture of both copies of each packet, stamp to arrival within 2.792 ms; the converted times differ by at most 2.744 µs |
| Port time bases | Simulation: each copy's avtp_timestamp against its own port's PHC | Bench capture of both copies on the two networks |
| Block RAM ledger | Estimate above | Routed image at 32x32 with measured firmware |
| Save bound | Analysis above at datasheet maxima | Host flash model at maxima; bench power cuts |
| Compaction keeps saved changes | Ordering and tables above | Host flash model: one save at every page boundary of a compaction, including the one after the last replay page, one during the header page, and a second save at every boundary; a header that programs intact or torn and fails its read-back, with its zeroing passing or failing its own read-back, then a save; a power cut before, inside and after every page and erase step, including before and after the standby's header sector is erased; then commit, erase, reboot and read every saved value. The test fails if a save may run between step 4's check and the header page, if step 3 is skipped, or if a save appends to the old slot before a failed header reads back zeroed or erased |

The shaper model is lane evidence, not a gate.
An implementation lane must turn it into a self-checking test.

### Open design items

The stream-engine lane, [lane 6](MARK_II_AREA_PLAN.md#mark-ii-lane-sequence), owns these.
Each states the requirement it must meet.

| Item | Requirement | Verification |
|---|---|---|
| 1. Render span edges | No sample is written outside the render buffer: not a packet whose samples cross either end of the span, nor a clean copy whose counted position falls a sample behind the render point. The early check and the buffer depth must allow for a whole packet at every rate | Simulation with copies at both span edges at 48, 96 and 192 kHz, the conversion error at its bound; the test fails if any sample lands outside the buffer |
| 2. Copies with tu set | The listener meets TU-1 to TU-5 below. This page fixes no mechanism, register or loss figure for them | The named cases below, in the lane's model, its simulation and on the bench |
| 3. Short margin on both networks | A clean copy's margin is how long before its time it arrives. A margin under about 125 µs on both networks lapses the head before the next packet, so rule 2 places every packet by its own time. The threshold carries the conversion error: within that error of 125 µs, only some packets lapse. When first arrival interleaves between the networks, copies can land one sample apart. The lane states the shift it allows, and the listener stays within it. This page fixes no mechanism or figure for it | Simulation with clean copies on both networks 10 to 50 µs before their time, first arrival interleaved, at 48, 96 and 192 kHz, every grid phase. The test fails on a shift beyond what the lane states. The starting case is the reviewer's [published probe](https://github.com/kebag-logic/milan-fpga/blob/f9cfe08cd3f526acde88e0d2a1c48ed2740583df/review-evidence/640-m9-r1/reviews/R758-5/scripts/probe_margin_r5.py). [Its output](https://github.com/kebag-logic/milan-fpga/blob/f9cfe08cd3f526acde88e0d2a1c48ed2740583df/review-evidence/640-m9-r1/reviews/R758-5/receipts/model/probe_margin_r5.out) reports up to 766 shifts and 383 unwritten samples in 2,000 packets. That is the probe's result, not a design figure |

#### Item 2: copies with tu set

The lane designs the mechanism and adds its registers.
Each listener context keeps 56 reserved octets for them.

| Id | Requirement | Source | Verification |
|---|---|---|---|
| TU-1 | A copy whose tu is set is not trusted for placement by its own presentation time. The listener follows Milan v1.2 4.4.2.3: after tu resets, its media clock free-wheels for a time the lane states | IEEE 1722-2016 4.4.4.7; Milan v1.2 4.4.2.3 | Cases A to D. The test fails if a tu copy's skew alone changes which samples render or where they land, apart from an anchor TU-4 states. A servo simulation fails if the media clock adjusts inside the stated free-wheel time |
| TU-2 | A clean copy on either network is rendered, as the rules above place it. A tu copy never replaces a clean one | Milan v1.2 Annex D.2; IEEE 1722-2016 4.4.4.7 | Case E. For each packet with a clean copy past rule 1, the rendered samples equal the clean stream's. The test fails if a tu copy overwrites clean data, or a tu copy keeps a clean copy from rendering |
| TU-3 | No copy is written outside the render span. A talker restart during tu places no sample at a wrong packet; the lane picks the restart signal | Milan v1.2 4.4.2.1, 5.3.8.10; IEEE 1722-2016 4.4.4.6 | Cases K and L. Every write is checked against the render point. The test fails if a sample lands outside the span, or at a wrong packet |
| TU-4 | A stream that starts with tu, unpaired or on both networks, still renders. The lane states the behaviour: how it places those copies, and what the first clean copy then does | IEEE 1722-2016 4.4.4.6, 4.4.4.7 | Case G. The test compares the rendered stream with the stated behaviour. It fails if a stream receiving every packet renders only isolated packets |
| TU-5 | The loss bound is an output of the lane's model and bench run, recorded in the table below. It covers tu on both networks, one network lost, and a large time skew. The skew is at least the 1.5 s step the [recovery page](GM_LOSS_RECOVERY.md#media-re-base-on-a-phc-step) grades | Milan v1.2 Annex D.3, which covers connectivity loss only; IEEE 1722-2016 4.4.4.7 | Every case below, in the model and on the bench. The model reports samples missing and misplaced per case. The lane records the bound before its review |

| Condition | Loss bound |
|---|---|
| tu on both networks, both delivering | To be set by lane 6 |
| One network lost, tu on the other | To be set by lane 6 |
| Time skew of at least 1.5 s | To be set by lane 6 |

Each case runs at the 2 ms default offset.
Every copy is delivered unless the case says otherwise.

| Case | Setup | Serves |
|---|---|---|
| A. Skew on both, near the check | tu on both from packet 100; both networks 60 to 180 µs; skews of +700, +800, +850 and -2,000 µs, and of plus and minus 1.5 s | TU-1, TU-5 |
| B. Skew across a whole period | tu on both for packets 100 to 600; both networks 60 to 180 µs; skews of +1,000, -1,900 and -2,500 µs | TU-1, TU-5 |
| C. Skew with the networks apart | tu on both from packet 100; secondary 1.1 to 1.5 ms slower; skews of 5 µs, 200 µs and 1 ms, either sign | TU-1, TU-5 |
| D. Only the fast network skewed | tu on both from packet 100; fast primary skew +1,000 µs; slow secondary skew 0 | TU-1, TU-5 |
| E. tu on one network | Secondary tu, skews of plus and minus 30 µs and 200 µs and +1 ms, arriving before the primary; skew 200 µs arriving after it; 1 % frame loss on the clean network; on the bench, a grandmaster change on one network with both up | TU-2, TU-5 |
| F. Network lost, tu on the other | Primary cut; secondary tu for 250 ms, skew +2,500 µs; on the bench, a cable pull then a grandmaster change on the surviving network | TU-5 |
| G. Starting with tu | tu from packet 0 on an unpaired stream; on both networks; on both with the secondary faster; then the first clean copy | TU-4, TU-5 |
| H. Short arrival margin | tu on both from packet 100, no skew; secondary arrives 10 to 50, 50 to 100, 110 to 120 and 150 to 200 µs before its time | TU-5 |
| I. Networks clearing apart | A time step of -200, -300 and -500 µs as tu clears, the slower network first and the faster up to 80 packets later; a step of plus or minus 100 µs to 1 ms with both clearing together | TU-5 |
| J. Onsets and short periods | tu on both with onsets together and 0.5 ms apart either way; a period that ends; tu on one to three packets; on the bench, one talker setting tu on both, both up | TU-5 |
| K. Sequence jump | A jump of plus or minus 40 while the head is valid: on one network, the partner clean or with tu; on both networks; on an unpaired stream | TU-3, TU-5 |
| L. Restart | tu on both, one stream restarting with its sequence stepping by 3; the same unpaired; tu on one network with its clean partner losing frames | TU-3, TU-5 |

A starting point: the [merge model](https://github.com/kebag-logic/milan-fpga/tree/b250a6169a1c70a6d72953c1f384605cb39a5e7b/review-evidence/640-m9-r1/author-r4/evidence/model) and its [earlier form](https://github.com/kebag-logic/milan-fpga/tree/b250a6169a1c70a6d72953c1f384605cb39a5e7b/review-evidence/640-m9-r1/author-r3/evidence/model).
Both are known to fail: [one probe set](https://github.com/kebag-logic/milan-fpga/tree/b250a6169a1c70a6d72953c1f384605cb39a5e7b/review-evidence/640-m9-r1/reviews/R757-4/scripts), [another](https://github.com/kebag-logic/milan-fpga/tree/b250a6169a1c70a6d72953c1f384605cb39a5e7b/review-evidence/640-m9-r1/reviews/R758-4/scripts).

## Open questions

1. **Save bursts.**
   A burst beyond S1 exceeds 0.5 s at maxima.
   The owner may bound it, accept it or change media.
2. **Block RAM.**
   The 32x32 ledger exceeds the usable tiles by 23.
   The reductions above need measuring before lanes rely on them.
3. **Debounce windows.**
   - Today's 500 ms window uses the whole bound.
   - The 1,000 ms window exceeds it.
   - #823 and F1 must restate them inside the bound.
4. **gPTP on two ports.**
   - The surveyed `flexptpd` fork keeps one global core state.
   - Redundancy needs gPTP on both ports (#665 F6). One instance per port is one way.
   - The owner also confirms the fork's source and licence.
5. **Commit timeout.**
   - `T-NVM-COMMIT-TIMEOUT` is 8,000 ms today.
   - The owner's direction restates it against 359.75 ms.
   - #823 and #665 F1 own the new value.
6. **Engine headroom at 192 kHz.**
   - A legal 192 kHz mix loads each engine 93.18 %.
   - It has 14 eight-channel streams and no CRF.
   - A faster clock or wider beats would restore margin.
