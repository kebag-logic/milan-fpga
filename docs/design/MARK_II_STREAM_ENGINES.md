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
- **[Packet-boundary stagger](#packet-boundary-stagger)** -- Six phases per 125 µs, fixed per stream.
- **[Talker latency budget](#talker-latency-budget)** -- The shaper derivation; 64.25 µs worst.
- **[Listener path and render buffer](#listener-path-and-render-buffer)** -- One RAMB36 sized by offset.
- **[Redundancy pairing and listener merge](#redundancy-pairing-and-listener-merge)** -- Index parity; first copy wins.
- **[Per-port MAC, filter and timestamp units](#per-port-mac-filter-and-timestamp-units)** -- What each port adds.
- **[Register maps](#register-maps)** -- Engine registers and both context layouts.
- **[Block RAM ledger at 32x32](#block-ram-ledger-at-32x32)** -- An estimate 20 tiles over.
- **[The 0.5 s save path](#the-05-s-save-path)** -- Append-only; 353 ms worst.
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

Milan v1.2 6.2 fixes the base format.
It is AAF PCM, 32-bit, one to eight channels.

At 48 kHz each PDU carries six samples per channel.
Every PDU carries a timestamp, not sparse mode.

IEEE 1722-2016 7.6 keeps that sample count constant.
Milan v1.2 Table 4.4 fixes the reservation.

The worst case is eight channels on every stream.
The table below derives one frame and one port's load.

| Quantity | Value | Derivation |
|---|---:|---|
| AAF payload | 192 octets | 8 channels x 6 samples x 4 octets |
| AVTPDU | 216 octets | 24-octet AAF header plus payload (Milan v1.2 Table 4.4: MaxFrameSize = 24N + 24 + 1) |
| Frame on the wire | 258 octets | AVTPDU + 22 (Ethernet header with VLAN tag, FCS) + 20 (preamble and IFG) |
| Wire time | 2.064 µs | 258 x 8 bits at 1 Gb/s |
| Reserved bandwidth per stream | 16,576 kb/s | Table 4.4: 1536 x 8 + 4288 |
| Class A frames per port | 128,000 per s | 16 streams x 8,000 PDUs per s |
| Class A idleSlope per port | 265.216 Mb/s, 26.52 % | 16 x 16,576 kb/s |
| With one CRF stream per port | 270.848 Mb/s, 27.08 % | Table 4.4 CRF: 5,632 kb/s |
| Frames per s, both ports, each way | 256,000 | 2 ports x 128,000 |

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

The engine reads a context, works, then writes it back.
Firmware writes the configuration words through the engine window.

The [register maps](#register-maps) give both layouts.
Counters update by read-modify-write inside the engine.

### Engine throughput

The datapath runs at 50 MHz with 32-bit beats.
Each engine moves 1,600 Mb/s; streams need 528.

| Step | Cycles at 50 MHz | Basis (estimate) |
|---|---:|---|
| Context read and write | 4 | Two-port Block RAM, pipelined |
| Ethernet and VLAN header | 5 | 18 octets |
| AAF header | 6 | 24 octets |
| Payload | 48 | 192 octets |
| Turnaround | 1 | Frame boundary |
| One 8-channel frame | 64, that is 1.28 µs | Sum |
| Load, 256,000 frames per s | 32.8 % | 256,000 x 1.28 µs |

The depacketizer has the same per-frame cost.
Both engines keep at least 67 % idle time.

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
The shaper would start the last about 117 µs later.

So each stream closes its packets on its own phase.
A phase is one of six samples per 125 µs.

IEEE 1722-2016 7.5 permits this offset.
Each PDU's timestamp names its own first sample.

IEEE 1722-2016 7.6 needs only a constant sample count.
It sets no common packet boundary across streams.

The phase is fixed while a stream runs.
Changing it would break the constant sample count.

Firmware assigns the phase when a stream starts.
It picks the phase with the fewest running streams.

Ties go in the order `0, 1, 3, 4, 2, 5`.
At 16 streams that gives `3, 3, 2, 3, 3, 2`.

Stops and restarts can produce any order of those loads.
The budget below covers every one.

## Talker latency budget

Start: the packet's last sample at the TDM pin.
End: its frame's first bit on the wire.

[NFR-LAT-03](../reference/FR_NFR.md#31-performance--real-time) bounds it below 65 µs for every talker stream.
The owner set that target on 2026-10-31.

### The class A shaper

Milan v1.2 4.3.4 requires both shaping levels.
It cites IEEE 802.1Q-2022 34.6.1 for both.

Clause 34.6.1.1 sets the class idleSlope.
It is the sum of the port's stream idleSlopes.

Assumption: idleSlope sums Table 4.4 over reserved streams.
At 32x32: 16 AAF streams and one CRF stream.

Clause 8.6.8.2 then fixes the pacing.
After a frame of L bits, credit is negative.

Credit returns to zero after L / idleSlope minus L / portTransmitRate.
So backlogged frames start L / idleSlope apart.

```
spacing, 8-channel frame  = 2,064 bits / 270.848 Mb/s = 7.621 µs
spacing, CRF frame (88 octets) = 704 bits / 270.848 Mb/s = 2.599 µs
phase period at 48 kHz    = 125 µs / 6 = 20.833 µs
```

A lower-priority frame can be on the wire first.
Annex L.3.1.1 caps it at one frame.

IEEE 802.1BA-2011 6.3 sets it at 1522 octets.
Credit accrued meanwhile lets later frames catch up.

```
interference = (1522 + 20) octets x 8 bits / 1 Gb/s = 12.336 µs
```

### Per-port schedule at 32x32

The schedule assumes a phase's frames are all ready together.
Within a phase the smaller frame goes first.

| Phase | Ready at, µs | Frames | First bits at, µs | Last frame's shaper wait, µs |
|---:|---:|---|---|---:|
| 0 | 0.000 | 3 AAF | 0.000, 7.621, 15.241 | 15.241 |
| 1 | 20.833 | 3 AAF | 22.862, 30.482, 38.103 | 17.269 |
| 2 | 41.667 | CRF, 2 AAF | 45.723, 48.322, 55.943 | 14.276 |
| 3 | 62.500 | 3 AAF | 63.563, 71.184, 78.804 | 16.304 |
| 4 | 83.333 | 3 AAF | 86.425, 94.045, 101.666 | 18.333 |
| 5 | 104.167 | 2 AAF | 109.286, 116.907 | 12.740 |

Phase 5 frees the shaper at 124.527 µs.
That is before 125 µs, so no backlog carries over.

The worst shaper wait is 18.333 µs, phase 4.
A byte-resolution shaper model gives 18.336 µs.

With a saturated best-effort queue it reached 30.632 µs.
That stays within 18.333 + 12.336 = 30.669 µs.

The order matters; the same schedule covers all 90 orders.
The worst, `2, 2, 3, 3, 3, 3`, waits 23.925 µs.

### The complete budget

| Term | Bound, µs | Basis |
|---|---:|---|
| Pin to capture: earliest slot to frame end | 18.229 | 7 of 8 slots x 2.604 µs at 12.288 MHz bit clock |
| Capture clock-domain crossing | 0.200 | Four 50 MHz cycles (estimate) |
| Packetizer, last of 8 frames in a phase | 8.560 | 6 x 1.28 + 2 x 0.44 µs (estimate) |
| Class A shaper wait, preferred order | 18.333 | Schedule above, `3, 3, 2, 3, 3, 2` |
| Class A shaper wait, worst order | 23.925 | Worst of 90 orders: 15 placements of the two light phases, 6 of the CRF |
| One interfering maximum frame | 12.336 | IEEE 802.1Q-2022 L.3.1.1 |
| MAC launch and PHY | 1.000 | 426 ns register stages, 219 ns PHY egress, rest margin (estimate) |
| **Total, preferred order, worst slot** | **58.658** | Below 65 µs by 6.342 µs |
| **Total, worst order, worst slot** | **64.250** | Below 65 µs by 0.750 µs |
| Total, worst order, slot 7 | 46.021 | Without the first term |

The sum counts the packetizer and shaper both in full.
That double count is deliberate and conservative.

The first term assumes release at the TDM frame's end.
Release after the highest mapped slot removes most of it.

The worst order leaves only 0.75 µs of margin.
So the implementation should release per highest mapped slot.

### Fewer reservations on a port

The budget above holds at the 32x32 load.
It does not hold for every smaller load.

With fewer reservations, idleSlope shrinks with them.
Co-phased streams then wait longer for credit.

| Running AAF streams on the port | idleSlope | Last frame's shaper wait | With interference |
|---|---:|---:|---:|
| Two in phase 0 only | 33.152 Mb/s | 62.264 µs | 74.600 µs |
| Three in phase 0 only | 49.728 Mb/s | 83.016 µs | 95.352 µs |
| Two, phases 0 and 1 | 33.152 Mb/s | 41.424 µs | 53.760 µs |
| Two, phases 0 and 3 | 33.152 Mb/s | 0.000 µs | 12.336 µs |

The same byte-resolution shaper model gives these.
Alone, k co-phased streams wait about `(k - 1) x 125 / k` µs.

Re-phasing a running stream would break IEEE 1722-2016 7.6.
Padding reservations would break Milan v1.2 Table 4.4.

So 65 µs is shown at the 32x32 load only.
Below it, the owner must choose a reading.

The [open questions](#open-questions) list the options.

## Listener path and render buffer

The depacketizer matches a frame to a listener context.
It compares destination and stream_id against the port's 16 contexts.

Two compares per cycle take eight cycles per frame.
It needs 160 ns; a minimum frame lasts 672 ns.

Only mapped channels are written to the render buffer.
Only eight slots reach the TDM pins.

The buffer is indexed by presentation time.
IEEE 1722-2016 7.5 dates each PDU's first sample.

Milan v1.2's default presentation offset is 2 ms.
Section 5.3.7.6 adds at most 125 µs.

IEEE 802.1Q-2022 34.6.1.2 sizes listener buffers.
So the depth follows the offset, not the stream count.

```
needed   = 2.000 ms + 0.125 ms + one 0.125 ms packet = 2.250 ms = 108 samples at 48 kHz
depth    = 128 samples (2.667 ms)
buffer   = 8 slots x 128 samples x 32 bits = 32,768 bits = one RAMB36 (estimate)
```

One RAMB36 is one 8-channel stream's worth of offset.
It serves all 32 listener streams through the map.

The buffer's two ports run on two clocks.
So it also crosses into the audio clock domain.

Today's render path spends three RAMB36 on that crossing.
The shared buffer replaces them.

Offsets above 2.667 ms overflow it at 48 kHz.
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

The talker builds both frames from one capture read.
Even contexts use port 0, odd ones port 1.

Milan v1.2 8.3.4 gives each interface gPTP.
So each network has its own time.

The listener merges each pair into one render stream.
It converts a secondary timestamp into the render time.

The conversion adds the measured offset between the two clocks.
The fabric latches both clocks on one edge.

The even context holds the pair's last written presentation time.
A copy not later than that time is discarded.

Compare in wrapping 32-bit time, like avtp_timestamp.
IEEE 1722-2016 4.4.4.9 defines that field.

The first valid copy of each packet wins.
Losing one network then loses no samples.

A copy from an unsynchronized network is discarded.
IEEE 1722-2016 4.4.4.7's tu bit marks it.

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
Offsets are bytes from the block base; resets are hexadecimal.

Access codes: R is read-only, RW is read-write.
RC clears on read; FW means firmware writes it.

Firmware writes configuration through the engine window.
`milan_csr` exposes the status and counter words read-only.

### Engine registers

| Offset | Name | Bits | Field | Reset | Access | Description |
|---|---|---|---|---|---|---|
| 0x000 | SE_ID | 31:16 | MAJOR | 0x0001 | R | Engine layout major version |
| | | 15:0 | MINOR | 0x0000 | R | Engine layout minor version |
| 0x004 | SE_CAP | 7:0 | N_TALKER | 0x20 | R | Talker contexts, 32 at 32x32 |
| | | 15:8 | N_LISTENER | 0x20 | R | Listener contexts, 32 at 32x32 |
| | | 19:16 | N_PHASE | 0x6 | R | Sample phases per class A interval at 48 kHz |
| | | 20 | TWO_PORT | 0x1 | R | Second AVB interface present |
| | | 31:21 | RESERVED | 0x0 | R | Reads zero |
| 0x008 | SE_CTRL | 0 | TALKER_EN | 0x0 | RW | Enables the packetizer |
| | | 1 | LISTENER_EN | 0x0 | RW | Enables the depacketizer |
| | | 31:2 | RESERVED | 0x0 | R | Reads zero |
| 0x010 | SE_IDLESLOPE0 | 31:0 | KBPS | 0x0000_0000 | RW | Port 0 class A idleSlope, kb/s; firmware writes the Table 4.4 sum |
| 0x014 | SE_IDLESLOPE1 | 31:0 | KBPS | 0x0000_0000 | RW | Port 1 class A idleSlope, kb/s |
| 0x020 | SE_TLAT_MAX0 | 31:0 | NS | 0x0000_0000 | RC | Port 0 worst capture-to-first-bit interval, ns |
| 0x024 | SE_TLAT_MAX1 | 31:0 | NS | 0x0000_0000 | RC | Port 1 worst capture-to-first-bit interval, ns |
| 0x028 | SE_TLAT_OVER | 15:0 | COUNT0 | 0x0000 | RC | Port 0 frames at or above 65 µs |
| | | 31:16 | COUNT1 | 0x0000 | RC | Port 1 frames at or above 65 µs |
| 0x030 | SE_MERGE_DUP | 31:0 | COUNT | 0x0000_0000 | R | Redundant copies discarded |
| 0x034 | SE_MERGE_SEC | 31:0 | COUNT | 0x0000_0000 | R | Packets rendered from a secondary copy |
| 0x800 | SE_TCTX[0..31] | - | - | - | FW, R | Talker contexts, 64 octets each |
| 0x1000 | SE_LCTX[0..31] | - | - | - | FW, R | Listener contexts, 128 octets each |

### Talker context

Context n sits at 2,048 plus 64 times n.
The engine owns the state and counter words.

| Offset | Name | Bits | Field | Reset | Access | Description |
|---|---|---|---|---|---|---|
| 0x00 | TCTX_CTRL | 0 | RUN | 0x0 | FW | Stream started (Milan v1.2 5.3.7.3) |
| | | 1 | PORT | n & 1 | R | 0 primary, 1 secondary; index parity |
| | | 4:2 | PHASE | 0x0 | FW | Packet-boundary phase, 0 to 5 |
| | | 11:8 | NCH | 0x0 | FW | Channels per frame, 1 to 8 (Milan v1.2 6.2) |
| | | 13:12 | NSR | 0x0 | FW | 0 is 48 kHz, 1 is 96 kHz, 2 is 192 kHz |
| | | 31:14 | RESERVED | 0x0 | R | Reads zero |
| 0x04 | TCTX_MAP | 31:0 | SLOT[7:0] | 0x7654_3210 | FW | Four bits per stream channel: its TDM slot (Milan v1.2 5.3.9.1) |
| 0x08 | TCTX_SID_LO | 31:0 | STREAM_ID | 0x0000_0000 | FW | stream_id bits 31:0 (IEEE 1722-2016 4.4.4.8) |
| 0x0C | TCTX_SID_HI | 31:0 | STREAM_ID | 0x0000_0000 | FW | stream_id bits 63:32 |
| 0x10 | TCTX_DA_LO | 31:0 | DA | 0x0000_0000 | FW | Destination MAC bits 31:0, from MAAP |
| 0x14 | TCTX_DA_HI | 15:0 | DA | 0x0000 | FW | Destination MAC bits 47:32 |
| | | 31:16 | TCI | 0x0000 | FW | VLAN PCP, DEI and VID |
| 0x18 | TCTX_PTO | 30:0 | NS | 0x001E_8480 | FW | Presentation time offset, ns; reset is 2 ms (Milan v1.2 5.3.7.6) |
| 0x1C | TCTX_STATE | 7:0 | SEQ | 0x00 | R | Next sequence_num (IEEE 1722-2016 4.4.4.6) |
| | | 8 | MR | 0x0 | R | Media clock restart toggle (IEEE 1722-2016 4.4.4.3) |
| | | 31:9 | RESERVED | 0x0 | R | Reads zero |
| 0x20 | TCTX_STREAM_START | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.7.7 |
| 0x24 | TCTX_STREAM_STOP | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.7.7 |
| 0x28 | TCTX_MEDIA_RESET | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.7.7 |
| 0x2C | TCTX_TIMESTAMP_UNCERTAIN | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.7.7 |
| 0x30 | TCTX_FRAMES_TX | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.7.7 |
| 0x34 | TCTX_TLAT_MAX | 31:0 | NS | 0x0 | RC | This stream's worst capture-to-first-bit interval, ns |
| 0x38-0x3C | RESERVED | 31:0 | - | 0x0 | R | Reads zero |

### Listener context

Context n sits at 4,096 plus 128 times n.
The engine owns the state, merge and counter words.

| Offset | Name | Bits | Field | Reset | Access | Description |
|---|---|---|---|---|---|---|
| 0x00 | LCTX_CTRL | 0 | RUN | 0x0 | FW | Bound and started (Milan v1.2 5.3.8.2, 5.3.8.7) |
| | | 1 | PORT | n & 1 | R | 0 primary, 1 secondary; index parity |
| | | 2 | PAIRED | 0x0 | FW | Context n ^ 1 is this stream's redundant partner |
| | | 11:8 | NCH | 0x0 | FW | Channels per frame, 1 to 8 |
| | | 13:12 | NSR | 0x0 | FW | 0 is 48 kHz, 1 is 96 kHz, 2 is 192 kHz |
| | | 31:14 | RESERVED | 0x0 | R | Reads zero |
| 0x04 | LCTX_MAP | 31:0 | SLOT[7:0] | 0x7654_3210 | FW | Four bits per stream channel: its TDM slot (Milan v1.2 5.3.9.1) |
| 0x08 | LCTX_MAPEN | 7:0 | EN | 0x00 | FW | Channels written to the render buffer |
| | | 31:8 | RESERVED | 0x0 | R | Reads zero |
| 0x0C | LCTX_SID_LO | 31:0 | STREAM_ID | 0x0000_0000 | FW | Bound stream_id bits 31:0 |
| 0x10 | LCTX_SID_HI | 31:0 | STREAM_ID | 0x0000_0000 | FW | Bound stream_id bits 63:32 |
| 0x14 | LCTX_DA_LO | 31:0 | DA | 0x0000_0000 | FW | Stream destination MAC bits 31:0 |
| 0x18 | LCTX_DA_HI | 15:0 | DA | 0x0000 | FW | Stream destination MAC bits 47:32 |
| | | 31:16 | VID | 0x0000 | FW | Expected VLAN ID |
| 0x1C | LCTX_STATE | 7:0 | SEQ | 0x00 | R | Last sequence_num seen |
| | | 8 | LOCKED | 0x0 | R | Media locked on this stream |
| | | 31:9 | RESERVED | 0x0 | R | Reads zero |
| 0x20 | LCTX_LAST_PT | 31:0 | NS | 0x0000_0000 | R | Last written presentation time, render clock; the pair's merge key, used in the even context |
| 0x24 | LCTX_MEDIA_LOCKED | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x28 | LCTX_MEDIA_UNLOCKED | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x2C | LCTX_STREAM_INTERRUPTED | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x30 | LCTX_SEQ_NUM_MISMATCH | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x34 | LCTX_MEDIA_RESET | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x38 | LCTX_TIMESTAMP_UNCERTAIN | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x3C | LCTX_UNSUPPORTED_FORMAT | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x40 | LCTX_LATE_TIMESTAMP | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x44 | LCTX_EARLY_TIMESTAMP | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x48 | LCTX_FRAMES_RX | 31:0 | COUNT | 0x0 | R | Milan v1.2 5.3.8.10 |
| 0x4C-0x7C | RESERVED | 31:0 | - | 0x0 | R | Reads zero |

## Block RAM ledger at 32x32

Of 135 tiles, 121.5 are usable after the reserve.
A RAMB18 counts as half a tile.

Every row below is an estimate unless it says measured.

| Item | Tiles | Basis |
|---|---:|---|
| Talker contexts, 32 x 64 octets | 0.5 | One RAMB18 |
| Listener contexts, 32 x 128 octets | 1.0 | One RAMB36 |
| Talker capture buffer | 0.5 | One RAMB18, above |
| Listener render buffer | 1.0 | One RAMB36, above; replaces three |
| Egress frame queues, two ports | 2.0 | One RAMB36 per port |
| Receive stream FIFOs, two ports | 2.0 | One RAMB36 per port |
| MAC clock-crossing FIFOs, two ports | 4.0 | Two RAMB36 per port, LiteX stage 2 |
| Packet mailboxes | 6.0 | Measured: one RAMB36 and ten RAMB18 ([F0](MAILBOX_SPLIT.md#measured-area)) |
| Timestamp and gPTP receive FIFOs | 1.0 | Two ports |
| Media clock and CRF | 0.5 | Today's CRF listener row |
| `milan_csr` | 1.0 | Measured placed, 2026-10-31: two RAMB18 |
| CPU | 4.5 | Measured placed, 2026-10-31: two RAMB36, five RAMB18 |
| **Fabric subtotal** | **24.0** | |
| Firmware memory, linear extrapolation to 64 streams | 113.0 | From the two measured two-interface points below |
| No whole-image save staging | -11.5 | Append-only save path; extrapolated stage size |
| gPTP daemon allowance | 16.0 | Not measured; F6 measures it |
| **Total** | **141.5** | 20 tiles over the usable 121.5 |

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
t_page                                                     = 5.343 ms, used as 5.35 ms

per save, at most P_max = 32 pages (8,192 octets)

T_worst = T_svc + T_suspend + (save in flight) + (this save)
        = 10 ms + 1 ms + 32 x 5.35 ms + 32 x 5.35 ms
        = 353.4 ms  <=  500 ms, margin 146.6 ms (29 %)
```

T_svc is the 10 ms service budget of NFR-SCOUT-03.
The save in flight is one a change just missed.

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
| Compaction work | 240 pages, 1.28 s | 240 x 5.35 ms at full share |
| Background erase of the old slot | 12 s | 4 x tSE |
| Boot read of one slot | 168 ms | 256 KiB x 8 / 12.5 MHz |

Compaction writes the live state into the pre-erased standby slot.
It serializes from the live tables, with no staging buffer.

Saves keep appending to the active slot meanwhile.
Each save preempts compaction between two pages.

When the copy completes, a header commits the new slot.
A power cut before it leaves the old slot whole.

Then the old slot is erased in the background.
It becomes the next pre-erased standby.

The layout change belongs to #823.
The generated flash map stays the single source.

### Assumptions

The bound needs two limits on the change rate.

- S1: changes made during one save fit 32 pages.
- S2: sustained saves stay below 10 % of the flash rate.

At datasheet maxima the flash writes 187 pages per second.
S2 allows about 4.8 KB per second, sustained.

Under S2, compaction and erase finish before the log fills.
Under S1, every change meets 0.5 s.

A burst beyond S1 drains at the flash's worst-case rate.
Rewriting all 907 names would take about 1.5 s.

That case needs the owner's reading.
The [open questions](#open-questions) list it.

## Verification

| Claim | Method | Evidence still owed |
|---|---|---|
| Engine throughput | Analysis above; RTL simulation at 256,000 frames per s each way | Simulation with both ports at full load |
| Talker latency at 32x32 | Analysis above; a byte-resolution model of IEEE 802.1Q-2022 8.6.8.2 | AAF latency taps on all 32 talker streams on the bench |
| Stagger conformance | IEEE 1722-2016 7.5 and 7.6 inspection | Listener interoperability with the reference peer |
| Listener merge | Simulation with one network cut mid-stream | Bench cable pull on each network, no lost samples |
| Block RAM ledger | Estimate above | Routed image at 32x32 with measured firmware |
| Save bound | Analysis above at datasheet maxima | Host flash model at maxima; bench power cuts |

The byte-resolution shaper model is lane evidence, not a gate.
An implementation lane must turn it into a self-checking test.

## Open questions

1. **Talker latency below the 32x32 load.**
   Co-phased streams alone wait up to 83 µs for credit.
   The owner's choices include these:
   - bind 65 µs at the 32x32 load only;
   - accept the derived bound at smaller loads;
   - change the stagger or shape decision.
2. **Save bursts.**
   A burst beyond S1 exceeds 0.5 s at maxima.
   The owner may bound it, accept it or change media.
3. **Block RAM.**
   The 32x32 ledger exceeds the usable tiles by 20.
   The reductions above need measuring before lanes rely on them.
4. **Debounce windows.**
   Today's 500 ms and 1,000 ms windows exceed it.
   #823 and F1 must restate them inside the bound.
5. **gPTP daemon licence.**
   Its source and licence are still unconfirmed (#665 F6).
