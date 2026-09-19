<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# 64-channel fabric map

This document defines the product channel-map topology. Audio remains in the
FPGA from physical capture or an accepted AAF Listener stream through physical
render or an AAF Talker stream. The bare-metal processor owns protocol and
control transactions; it does not carry media samples.

The implementation authorities are:

- [`KL_chan_map_capture.sv`](../hdl/ieee1722/aaf/KL_chan_map_capture.sv) for
  Talker source selection;
- [`KL_chan_map_render.sv`](../hdl/ieee1722/aaf/KL_chan_map_render.sv) for
  Listener-to-physical-output selection;
- [`KL_pcm_route.sv`](../hdl/ieee1722/aaf/KL_pcm_route.sv) for selecting the
  Listener stream presented to the physical render path;
- [`REGISTER_MAP.md`](reference/REGISTER_MAP.md) for the CSR encoding; and
- the generated AEM store for the Stream Port, AUDIO_CLUSTER, and AUDIO_MAP
  descriptor shape.

The related media-clock, persistence, and notification claims are checked
against the [Milan feature status ledger](reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `crf.media-clock-consumption` | `implemented` | - |
| `state.nonvolatile-persistence` | `partial` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. Shape and identity](#1-shape-and-identity)** — The eight-stream, eight-channel bound and its mono-cluster/pair-bus relationship.
- **[2. Wire-data contract](#2-wire-data-contract)** — Sample byte order, channel-position tracking, and changing wire shapes.
- **[3. Render map](#3-render-map)** — Listener selection, reserved zero, atomic tick updates, and physical numbering.
- **[4. Capture mux contract (KL_chmap_capture, phase-1 name)](#4-capture-mux-contract-kl_chmap_capture-phase-1-name)** — Capture-source encodings, loopback queueing, silence fill, and capability rails.
- **[5. Control ownership](#5-control-ownership)** — Atomic protocol updates, diagnostic writes, locking, and render arbitration.
- **[6. CSR window 0x900-0x97F (debug and override)](#6-csr-window-0x900-0x97f-debug-and-override)** — Programming and reading the live fabric stores.
- **[7. Verification and physical acceptance](#7-verification-and-physical-acceptance)** — Digital coverage and the evidence that remains assigned to #117.

## 1. Shape and identity

The maximum product shape is eight AAF Talker streams and eight AAF Listener
streams, each with up to eight channels. That is 64 stream channels or 32
stereo pair slots per direction.

Each generated AUDIO_CLUSTER represents exactly one mono channel. An AUDIO_MAP
entry therefore identifies a stream channel, a cluster offset, and a cluster
channel without relying on parity or vendor-specific grouping. The FPGA keeps
the familiar pair bus internally because the AAF packetizer accepts
`{pair_slot, left, right}`; the per-channel map supplies the two halves of each
pair independently.

## 2. Wire-data contract

AAF samples are 24-bit values carried left-justified in 32-bit big-endian wire
words. The depacketizer emits two consecutive wire samples per 64-bit AXIS
beat, with the Listener stream index in `tuser` and one PDU per AXIS frame.

Both map blocks derive a sample's wire channel from its position modulo the
accepted `channels_per_frame`. The counter resets at `tlast`, so back-to-back
PDUs with different stream identities or channel counts cannot inherit a stale
position. A pre-first-accept channel count of zero is treated as stereo. Wire
channels beyond the elaborated limit are still walked for alignment but are
not stored.

## 3. Render map

`KL_chan_map_render` latches the latest value of every retained
`{Listener stream, wire channel}`. On each 48 kHz media tick it updates the
entire physical-output vector atomically. A map write between ticks is never
partially visible at the pins.

The live render entry is eight bits:

```text
[7]    EN      1 = render this entry; 0 = digital silence
[6]    SRC     0 = accepted AAF Listener channel; 1 = reserved zero
[5:3]  STREAM  Listener stream 0..7 when SRC = 0
[2:0]  CHANNEL wire channel 0..7 when SRC = 0
```

Reserved, disabled, or out-of-range entries render zero. `mapped_mask_o`
asserts only for enabled `SRC=0` entries, so a reserved encoding cannot claim a
working physical route.

The default physical shape has ten channels: I2S left/right at indices 0/1 and
TDM lane 0 slots 0..7 at indices 2..9.

That layout is two named LANES, declared once in `milan_datapath` as
`CHMAP_RPHYS_I2S_BASE_C` / `CHMAP_RPHYS_I2S_N_C` and `CHMAP_RPHYS_TDM_BASE_C` /
`CHMAP_RPHYS_TDM_N_C`, with `CHMAP_PHYS_C` their sum rather than a literal
(#447). `avdecc/aem_assemble.py` and `sw/builder/endstation_builder.py` mirror
the same table as `RENDER_PHYS_LANES`, and a builder gate pins all three
together. The FIRST key of a lane and its COUNT are separate quantities, and
neither is inferred from a channel count: a board's physical input clusters
project to `render_lane_base(cfg) + pool.first + n`, where the lane base is
chosen by the board (the DAC lane when `board.features.i2s_playback` is set,
otherwise the TDM lane) and `pool.first` keeps its one existing meaning, the
audio-interface channel index. Raising a shape's `physical_channels.render`
without the lane base would have projected cluster keys 0..7 onto render keys
0..7, putting two clusters on a DAC lane a TDM-only board prunes and leaving
TDM slots 6 and 7 unreachable.

### 3.1 The TDM render lane on a master bus

`AUDIO_IF_RENDER_SLOTS_P` selects what serializes the TDM key window: 0 prunes
the lane and drives `tdm_dout_o` low, a nonzero width on a MASTER bus
elaborates `KL_tdm_render_master`, and a nonzero width on a codec-driven bus
elaborates the proven slave `KL_tdm_render`. The builder emits it from the same
`audio_interface.physical_channels.render` fact that sizes the advertised
cluster pool, so the width the entity advertises and the width the fabric backs
come from one place, and it is withheld unless the board routes the header the
serializer drives.

There is exactly ONE TDM bus: `bclk` and `fsync` are shared pins, so the render
half does not generate a second frame phase. `KL_tdm_capture_master` stays the
sole timing owner and exports `bclk_rise_o`, `bclk_fall_o` and `frame_pos_o`;
the render master runs in the same `clk_tdm_i` and consumes them. The pin-level
contract that follows is:

- Data starts in bit period 1, so slot k bit b occupies bit period
  `1 + 32k + b`.
- `fsync` is a one-`bclk` pulse CENTRED on the rise that ends bit period 0: it
  is launched on the `bclk` FALLING edge, half a bit period before that rise
  and half a bit period after it (issue #452). A receiver sampling `fsync` on
  the rising edge therefore reads it high across exactly ONE rise, with half a
  bit period of setup and of hold, and samples slot 0's MSB on the rise that
  FOLLOWS it - a one-bit data delay, which is a TI McASP at `RDATDLY = 1`.
  That is the phase the in-tree external codec model of this same master bus
  presents to the capture direction.
- Before #452 `fsync` changed ON the `bclk` rising edge, so it reached a
  rise-sampling receiver with zero nominal setup and zero hold and which rise
  the pulse belonged to was decided by pin skew. The pulse now moves with
  `dout`, and the three registered outputs are packed into their IOB flops
  (`sw/litex/platforms/alinx_ax7101.py`), so the pin-to-pin skew is the
  IOB-to-pad difference alone. An IOB flop takes no inverted D and drives
  nothing but its pad, so the bit clock is a pad flop that copies a fabric
  complement rather than a self-toggling flop, which the placer refused
  (#452), and the internal rise and fall enables read the complement.
- The render master latches the bit for bit period `p + 1` on the rise whose
  pre-edge frame position is `p`, and launches it on the following falling
  edge, so the receiver has half a bit period of setup.

The lane carries a four-phase RENDER EPOCH over retained levels, because both
FIFO sides reset synchronously to their own clock and a reset asserted and
released entirely while `clk_tdm_i` is stopped would otherwise reset one
pointer and leave the other. A HARD serial reset interrupts the frame in flight
and that serial interval is invalid; a GRACEFUL flush (a bind loss, or a reset
release while the clock keeps running) zeroes the active frame at FRAME STARTS
only, so the frame in flight completes whole and every frame after it is
digital silence until the epoch reopens. The serial side reopens at the first
frame start after the request clears, with both FIFO pointers proven zero, and
COMMITS resume later still: only once the bind is restored and the setpoint has
popped a post-flush event for every stream the lane renders.

The handshake is strictly four-phase, and `epochs_o` counts one REOPENING per
epoch event because of it. A request is raised only with the handshake free -
no request standing and no acknowledgement still visible - so a stale
acknowledgement cannot clear a request one cycle after it was raised; an event
that lands on a busy handshake is held and gets a round trip of its own, so two
bind falls inside one round trip are two counted reopenings. The hold is one
bit: a third event arriving while one is already held joins it, which costs a
count and no flush, since the round trip it joins performs exactly the flush it
asked for. The producer's view of the serial side is two levels that change
together only at the acknowledgement, and no decision it takes reconverges
them: the serial-reset condition is a level of its own rather than "flushed and
not acknowledged" rebuilt in the destination, which at a reopening - where the
flush and the acknowledgement clear on ONE serial edge - would depend on which
of two synchronisers happened to answer first.

Surplus is drop-OLDEST and counted: the serializer keeps prefetching while the
CDC is non-empty, so the newest committed frame is the one adopted and the
commit-to-pin delay stays bounded instead of ratcheting. A skip is counted when
a prefetched frame is OVERWRITTEN, which is before the decoded frame whose
ordinal jump exposes it, so a consumer reconciling counts against decoded
frames must allow a counted skip to stay pending until the adoption it affects
is observed.

Three limits are stated rather than assumed:

- A serial clock stopped for longer than the frame CDC's four entries loses
  commits as counted OVERRUNS whatever the surplus policy is, because the
  consumer cannot drain a clock that is not running.
- `SLOT_BITS_P` must be a power of two in the master serializer: its bit
  schedule is a slice of the timing owner's frame position rather than a
  divider of its own, and a non-power-of-two width is refused at elaboration.
- The SLAVE render lane keeps `KL_tdm_render`'s per-side reset behaviour and
  carries no epoch protocol, so a reset asserted and released entirely while
  the EXTERNAL bit clock is stopped remains the exposure that module has always
  had. No tracked config elaborates that arm.

### 3.1.1 Which streams the lane renders, and which clock it follows

The epoch closes on a bind fall, and that fall is STREAM QUALIFIED. The lane's
stream set is a combinational reduction over the render map itself: every
TDM-lane key that is enabled and names the AVB listener bank contributes the
stream index its word carries, so a lane fed only from stream 0 is untouched by
a bind fall on any other stream, and a lane with one key pointed at another
stream watches that stream too. The post-bind freshness gate is over the same
set: the epoch reopens once every stream the lane renders has popped a
post-flush event, which is what stops the crossbar's retained selection from
being re-emitted as though it were fresh audio.

The shipping AX7101 image carries ONE listener stream, so neither half of that
qualification is observable on it, and neither is a legal cluster key with no
physical projection. `tb/verilator/milan_dp_render/gen_tdm8r_multi_shape.py` writes a
second end-station config - the shipping one with a second listener and the
wire-truth cluster policy - and the builder derives its shape header and its
entity image, so the two halves are exercised against each other on a real
elaboration: STREAM_PORT_INPUT 0's eight clusters are the TDM slots and
STREAM_PORT_INPUT 1's eight are honestly nonphysical.

The CLOCK SOURCE does not change the lane's structure, only its rate. Measured
at the pins on the shipping shape, with the commit-to-pin interval taken
between the adapter's registered frame commit and the receiver's sampling edge
of slot 0's MSB:

| Clock source | Commit-to-pin walk | What the lane pays |
|---|---|---|
| INTERNAL | `+10.68` ppm measured, against the divider plan's `+10.6394` ppm closed form | one whole frame of `phi` every ~1.95 s |
| CRF, aligner engaged | `-0.80` ppm measured | nothing: the skip and underrun counters do not move across the window |

The INTERNAL row is the accepted free-run, not a defect: the same `10.64` ppm
the capture junction already publishes. What the pins show at each beat is not
one isolated skip but a CLUSTER of repeat/skip pairs as the commit instant
dithers across the frame boundary - measured on this head as 10 repeats against
11 skips over one crossing, netting exactly one dropped media event per beat
period. The drop-oldest law and the counted-skip accounting hold through it;
what was too smooth was the description "one skip per beat", not the design.

Since #386 the crossbar's clone input is `KL_render_setpoint`, a per-stream
elastic queue of whole media events that pops exactly one event per stream on
every media tick and hands the crossbar a render tick delayed past that pop
schedule. The crossbar therefore renders, on every tick, the event the stage
just handed it, and the accept-to-render delay of the shipping path is the
stage's constant setpoint rather than whatever phase a latest-sample latch
held. The law, its bands and the per-interface constants are in
[Listener render latency](design/TIME_SYNC.md#listener-render-latency). The
stage presents every stream as an even lane count (2 x ceil(N_CH_P / 2): eight
on every in-tree shape) with the lanes beyond the stream's channel count
zeroed, so the crossbar's per-stream channel count is that lane count (the pad
lane of an odd count is a virtual channel the walker never latches) and the
wire truth is de-interleaved once, in the stage. Each event is presented
atomically: the stage decides at a stream's first beat whether it presents
this tick and which row, so a rail, a recentre or a flush inside the pop
window lands between events and the crossbar's single walker never receives a
partial or mixed event.

### 3.1.2 The shipping eight channels, every dimension at once

One row per channel of the shipping AX7101 1x1 TDM8 image, with every semantic
dimension of the path kept DISTINCT (#447 acceptance 2). The table is CHECKED,
not typed: `test_builder.py` gate 16d derives each row from the same sources
the build emits - the generated shape header's `ADP_DMAP_IN_RPHYS_C`, the AEM
overlay the builder produces from `configs/endstation_ax7101_1x1_tdm8.yaml`,
the `RENDER_PHYS_LANES` lane table and the AX7101 platform's own `tdm`
subsignal - and a row that drifts from any of them fails that gate.

| Stream index / channel | Stream Port Input | Cluster offset | Global cluster | AUDIO_CLUSTER name | Physical render key | Audio interface | Package signal |
|---|---|---|---|---|---|---|---|
| 0 / c | 0 | 0 | 0 | `TDM8 Out FL` | 2 (`7'h42`) | TDM lane 0, slot 0 | J11.5, ball A20 |
| 0 / c | 0 | 1 | 1 | `TDM8 Out FR` | 3 (`7'h43`) | TDM lane 0, slot 1 | J11.5, ball A20 |
| 0 / c | 0 | 2 | 2 | `TDM8 Out FC` | 4 (`7'h44`) | TDM lane 0, slot 2 | J11.5, ball A20 |
| 0 / c | 0 | 3 | 3 | `TDM8 Out LFE` | 5 (`7'h45`) | TDM lane 0, slot 3 | J11.5, ball A20 |
| 0 / c | 0 | 4 | 4 | `TDM8 Out RL` | 6 (`7'h46`) | TDM lane 0, slot 4 | J11.5, ball A20 |
| 0 / c | 0 | 5 | 5 | `TDM8 Out RR` | 7 (`7'h47`) | TDM lane 0, slot 5 | J11.5, ball A20 |
| 0 / c | 0 | 6 | 6 | `TDM8 Out SL` | 8 (`7'h48`) | TDM lane 0, slot 6 | J11.5, ball A20 |
| 0 / c | 0 | 7 | 7 | `TDM8 Out SR` | 9 (`7'h49`) | TDM lane 0, slot 7 | J11.5, ball A20 |

How to read the columns, because several of them are commonly conflated:

- STREAM INDEX / CHANNEL. This image binds ONE AAF listener stream, index 0,
  carrying eight wire channels. Which of those channels feeds which cluster is
  not fixed here: it is whatever `ADD_AUDIO_MAPPINGS` assigned, one mapping per
  cluster, so the column reads `0 / c` on every row. `c` is `stream_channel`
  in the mapping and must lie inside the stream's format, 0..7.
- STREAM PORT INPUT and CLUSTER OFFSET. `cluster_offset` is PORT-RELATIVE
  (1722.1-2021 7.2.19), so it means nothing without the port index beside it.
  This shape declares one input port with eight clusters, which is why the
  offset and the global index coincide here and would not on a multi-port
  shape.
- GLOBAL CLUSTER. The AUDIO_CLUSTER descriptor index the entity model
  advertises, `base_cluster + pool.offset + n`.
- PHYSICAL RENDER KEY. The render crossbar destination,
  `render_lane_base(cfg) + pool.first + n`. The generated header spells it
  `{valid, key[5:0]}`, so key 2 is `7'h42`. Keys 0 and 1 are the I2S DAC lane
  this shape PRUNES, and no cluster reaches them.
- AUDIO INTERFACE. The serial position: `AUDIO_IF_RENDER_SLOTS_P` slots of TDM
  lane 0, slot k occupying bit periods `1 + 32k` through `32k + 32` of the
  frame.
- PACKAGE SIGNAL. All eight slots TIME-SHARE one pin. This header carries
  exactly one data output, so the last column is the same ball on every row;
  what separates the channels on the wire is the slot, not a pin.

One corner the table does not show, recorded because it is reachable from the
protocol face. A mapping may point a lane key at a stream that is NOT
delivering - for example a stream whose bind fell while this lane did not
render it, so no epoch was owed and none was raised. The render crossbar keeps
its latest-sample latch per `{stream, channel}` and seeds the destination from
it, so that slot then carries ONE constant sample of that stream's own last
delivered audio until that stream pops again, and the other slots are
untouched. It is a bounded DC re-seed on one slot, never another stream's
audio and never a torn value; the multi-stream leg's M7 arm visits it at the
pins and states exactly that.

## 4. Capture mux contract (KL_chmap_capture, phase-1 name)

`KL_chan_map_capture` owns each Talker channel while the map is armed. It walks
all pair slots on every media tick and injects either the selected samples or
digital silence. Covering disabled slots is required: omitting a pair can stop
the corresponding Talker from completing its six-sample PDU.

The live per-channel entry is 13 bits:

```text
[12]    EN       1 = use the selected source; 0 = digital silence
[11]    HALF     0 = left/even sample; 1 = right/odd sample
[10:8]  SRC      0 zero, 1 I2S input, 2 TDM input,
                  3 reserved zero, 4 pilot tone, 5 AAF loopback,
                  6..7 reserved zero
[7:4]   IDX_HI   Listener stream for SRC=5; ignored otherwise
[3:0]   IDX_LO   pair index within the selected source
```

Physical inputs and the pilot tone are latest-sample sources. AAF loopback is
bursty, so it uses a per-pair elastic queue instead of a latest-only latch. The
queue primes after the first complete PDU, pops one sample event per media
tick, drops the oldest event on overflow, repeats the last event on underflow,
and flushes on bind loss or stream-table eviction. Saturating duplicate and
skip counters expose clock-rate mismatch without changing channel identity.

The loopback de-interleaver pairs wire channels `{2p, 2p+1}`. Odd or mono wire
shapes fill a missing right half with zero. A stream remap cannot replay data
received before its flush.

The map readback includes `loop_mapped` and `loop_fed` capability rails. An
enabled loopback entry that has never received a payload is distinguishable
from a correctly connected but silent source.

## 5. Control ownership

The protocol processor serves `GET_AUDIO_MAP` from the same stores used by the
datapath. `ADD_AUDIO_MAPPINGS` and `REMOVE_AUDIO_MAPPINGS` validate every row
before atomically committing the command. A failed row leaves the live map
unchanged.

The CSR window is a diagnostic override of those stores. Its write path is
blocked while the map is disarmed or `LOCK_ENTITY` is held, and protocol map
transactions exclude CSR writes until commit or abort. This prevents a
diagnostic write from changing the validation baseline mid-command.

`KL_pcm_route` has a separate two-bit Listener route field at LCTX
`CTRL[2:1]`. Bit 1 is the retained `RENDER` flag and bit 0 is reserved zero.
If several streams request render, the lowest index wins. Stream 0 selects
render after reset; every depacketized payload is consumed even when it is not
the selected render stream.

## 6. CSR window 0x900-0x97F (debug and override)

The detailed register authority is
[`REGISTER_MAP.md`](reference/REGISTER_MAP.md#0x900-----channel-map-fabric--section-6-of-docschannel_map_64md-kl_chan_map_render--kl_chan_map_capture).
The core sequence is:

```text
write CHMAP_CTRL = 1
write CHMAP_SEL  = side/index
write CHMAP_WORD = encoded map word

write CHMAP_SNAP = 1
poll  CHMAP_SNAP.busy == 0
read  CHMAP_LOOP
```

| Offset | Register | Product meaning |
|---|---|---|
| `0x900` | `CHMAP_CTRL` | Bit 0 arms the map and diagnostic writes. |
| `0x904` | `CHMAP_SEL` | Bit 8 selects capture; bits 5:0 select the entry. |
| `0x908` | `CHMAP_WORD` | Diagnostic write word; capture fields are repacked into the 13-bit live entry, render fields into the 8-bit live entry. |
| `0x90C` | `CHMAP_STAT` | Commit and refused-write counters. |
| `0x910` | `CHMAP_SNAP` | Readback arm, busy/valid/timeout/unsupported state, capability bits, and the latched selection. |
| `0x914` | `CHMAP_LOOP` | Latched live-store word plus validity and loopback capability evidence. |

`CHMAP_LOOP = 0xDEAD_DEAD` means no valid measurement exists. A real empty map
entry is returned with its `VALID` bit set and must not be confused with that
sentinel. Capture readback can additionally assert `LOOP_SUSPECT` when an entry
selects loopback but no payload has reached that source.

## 7. Verification and physical acceptance

Digital coverage includes:

- all render source/channel selections, reserved-source silence, range guards,
  atomic tick visibility, and readback;
- all capture source buckets and channel halves, a full 64-channel identity
  walk, mono/odd shapes, byte-exact packet output, and reserved-source silence;
- paced loopback replay, overflow/underflow accounting, flush on rebind, and
  negative controls that deliberately swap or invert channel identity; and
- protocol-versus-CSR ownership and whole-command atomicity.

The physical completion record belongs to #117: one AX7101 DUT against the
Milan-validated reference peer, exact image IDs, all eight streams, walking
channel identity, render selection, loopback, and counter snapshots. Digital
success is required but does not replace that evidence.
