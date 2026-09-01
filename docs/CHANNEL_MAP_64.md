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
| `crf.media-clock-consumption` | `missing` | - |
| `state.nonvolatile-persistence` | `missing` | - |
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

The physical completion record belongs to #117: two boards, exact image IDs,
all eight streams, walking channel identity, render selection, loopback, and
counter snapshots. Digital success is required but does not replace that
evidence.
