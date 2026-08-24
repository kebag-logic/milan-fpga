[OBSOLETE + 2026-08-17]

<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# Audio streaming — the end-to-end AAF path

How an audio sample travels through this end-station: capture (or a host
PCM ring) → the shared AAF packetizer → the wire as IEEE 1722 AAF-PCM PDUs
carrying presentation time → the listener's monitor/depacketizer → the PCM
DMA ring (ALSA) and the physical render outputs. This is the subsystem
deep-dive for the media plane; the scaling model behind it is
[`NXN_ARCHITECTURE.md`](../NXN_ARCHITECTURE.md), the CSR authority is
[`reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md).

> **THE MEDIA PLANE IS INTACT; ITS CONTROL SURFACE IS THIN (2026-08-13).**
> Nothing in the datapath below changed when this repository's IEEE 1722.1 /
> SRP plane was deleted in favour of the pinned `protocol-processor`
> submodule. The submodule has since landed its **AECP µCPU**, so the earlier
> reading of this page — that the device answers nothing on AECP — is wrong and
> is corrected here. The device is reachable: it **answers `READ_DESCRIPTOR`**
> (`SUCCESS` carrying the configuration index, the reserved field and the
> descriptor; `NO_SUCH_DESCRIPTOR` on a locate miss; `BAD_ARGUMENTS` on a bad
> configuration index, both error paths carrying the IEEE 1722.1 §7.4.5 4-byte
> `{descriptor_type, descriptor_index}` stub), and it **answers every other
> AECP command with a conformant `NOT_IMPLEMENTED` echo** — right
> `message_type`, right length, right `controller_data_length`. Controller
> enumeration is therefore **reachable** once the descriptor image is in DRAM.
> The tracked builder/rootfs handoff supplies it only on an explicit deployment
> transfer; inspection-only/custom flows that skip that handoff remain empty
> (§6).
>
> What did **not** come back is every command that used to configure this media
> plane. An echo is not an implementation, and none of the bullets below is
> softened by one:
>
> * **The presentation-time offset is pinned at the Milan 2 ms default** for
>   every Stream Output. `SET_MAX_TRANSIT_TIME` / `SET_STREAM_INFO`
>   (MSRP_ACC_LAT) was its only writer. That is a DEFAULT, not a zero — 0 ns
>   would be a presentation time in the past and every listener would drop
>   every frame as late (§4).
> * **No `SET_STREAM_FORMAT`, no `SET_SAMPLING_RATE`, no audio-map commands.**
>   The wire format and the channel map are whatever the build elaborated
>   with, plus the CSR debug ports (§2.2, §5).
> * **The CRF media clock can never be SELECTED.** `SET_CLOCK_SOURCE` was the
>   only writer of the live CLOCK_DOMAIN `clock_source_index`, so it is pinned
>   at 0 (INTERNAL) for the life of the build: `KL_mmcm_drp_servo` and the
>   `KL_media_nco` packet-grid servo can never leave idle and `A_MCSRV_STAT`
>   `0x8F8` reads that idle. `KL_crf_rx` still parses, counts and reports —
>   it simply cannot steer anything (§3.2, §9 of
>   [`CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md)).
> * **Milan Table 5.4 per-STREAM_OUTPUT diagnostic counters are live for
>   solicited reads.** `KL_talker_diag_ctx` is instantiated per declared output
>   and GET_COUNTERS serves the compact five-counter layout. The Table 5.22
>   unsolicited producer remains open. **The STREAM_INPUT counters at `0x6B8`
>   remain live too** (§3.2).
>
> Two more facts belong on any page that talks to this control surface. The
> known gap: Milan Δ7 `ACQUIRE_ENTITY` is **not** distinguished from the
> generic echo — a controller gets `NOT_IMPLEMENTED`, not the `NOT_SUPPORTED`
> with `owner_id` = 0 that Milan asks for. And the descriptors that
> `READ_DESCRIPTOR` serves are an **image in DDR3 at a compile-time base** —
> there is no base register, software cannot relocate it, and it must be loaded
> **before the entity is enabled** or every read answers
> `BAD_ARGUMENTS`. On a stock build of this repository it is not loaded,
> because no step here builds or writes it (§6).
>
> ADP, ACMP and SRP are served by the processor, so a stream still gets
> discovered, connected, reserved and paced exactly as described below.

![Audio stream path — talker chain and listener chain with CSR touchpoints and latency taps](../diagrams/audio_stream_path.png)

> The picture above is generated (editable
> [`audio_stream_path.drawio`](../diagrams/audio_stream_path.drawio); regenerate with
> `python3 docs/diagrams/audio_stream_path.gen.py docs/diagrams/audio_stream_path &&
> rsvg-convert -w 2000 docs/diagrams/audio_stream_path.svg -o docs/diagrams/audio_stream_path.png`).

## Contents

- **[1. A stream's life](#1-a-streams-life)** — The shape of a class-A AAF stream in six numbers: 6 samples per PDU, 8000 PDUs/s at 48 kHz, presentation time latched at first-sample capture, and the listener's inverse `ts_delta = avtp_timestamp − ptp_now` readable at CSR `0x6EC`.
- **[2. Talker path — capture to wire](#2-talker-path--capture-to-wire)** — Everything from a microphone or a host ring to the MAC. The one contract all four sources speak, the packetizer's channel math (`42 + 24·C` bytes, always `≡ 2 (mod 8)`), the fractional-N strobe that fixed the 48,828.125 Hz audible pumping, and the egress fact people trip on — the fabric AAF stream is injected *after* the shaper and never queues through CBS.
- **[3. Listener path — wire to render](#3-listener-path--wire-to-render)** — The receive half, with the counter contract spelled out: what UNSUPPORTED_FORMAT suppresses, the 8-PDU settle window, the 100 ms unlock, and that counters reset on not-bound → bound *only*. Also the DRAM-vs-BRAM PCM ring choice and the wire-truth rule that de-interleaves by `channels_per_frame` from the wire, never the AEM store.
- **[4. Latency: presentation offset vs pipeline](#4-latency-presentation-offset-vs-pipeline)** — Two numbers usually conflated, then the measurement: end-to-end equals the presentation offset *exactly* (pto 500 µs, `ts_delta` +384 µs, 0 LATE) while the pipeline is ≈ 116 µs. The per-stage talker breakdown shows why neither dominant term shrinks with a faster clock — they are the 6-sample window and the class-A interval.
- **[5. Channel mapping — 64 in / 64 out](#5-channel-mapping--64-in--64-out)** — One paragraph of orientation: the fabric selects and never composes, and — since the audio-map commands draw a `NOT_IMPLEMENTED` echo rather than an implementation — the CSR `0x900` window is the **only** programmer of the map RAMs.
- **[6. Status (2026-07-26; control-surface addendum 2026-08-13)](#6-status-2026-07-26-control-surface-addendum-2026-08-13)** — What is proven on silicon versus what is only simulated, and then the addendum that reframes it: the audio datapath is intact and the device is enumerable again over `READ_DESCRIPTOR`, but nothing that *sets* this plane came back. Presentation offset pinned at the Milan 2 ms default, no SET_STREAM_FORMAT or SET_SAMPLING_RATE, no audio-map setters, the CRF media clock unselectable, the Table 5.4 talker counters not merely unreadable but uninstantiated — plus the descriptor-image-in-DRAM load order the reads depend on.

## 1. A stream's life

A Milan audio stream on this hardware is a class-A AAF-PCM stream: the
talker groups **6 samples per channel into one PDU**, 8000 PDUs/s at
48 kHz ([`hdl/ieee1722/aaf/KL_aaf_packetizer.sv`](../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv) header; traceability row
[AAF-9](../traceability/ieee1722-2016.md)).

Each PDU's `avtp_timestamp` is the **presentation time**: the gPTP
nanosecond clock latched when the PDU's first sample was captured, plus
the transit offset (packetizer TCTX word `w4 TS`, "latched
presentation time (ptp_ns + transit at first-sample capture)"; row
[AVTP-10](../traceability/ieee1722-2016.md)). That offset was configurable
per Stream Output over AECP and no longer is — `SET_MAX_TRANSIT_TIME` draws a
`NOT_IMPLEMENTED` echo, which changes nothing — so it holds the **Milan 2 ms
default** for the life of the build (banner above, §4).

The listener does the inverse: for every accepted PDU it computes
`ts_delta = avtp_timestamp − ptp_now` (signed; negative = LATE, i.e. the
presentation instant already passed; larger than the presentation offset
plus margin = EARLY — [`hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`](../../hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv),
`tsd_w`/`late_w`/`early_w`).

The last value is readable at CSR `0x6EC` (`A_AVTPRX_TSD`,
[`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv)). The presentation offset is therefore the
*rendering budget* the talker grants the network plus the listener
pipeline.

![AAF class-A pacing — 6-sample epochs, presentation stamped at the first sample, ts_delta at the listener](../diagrams/wd_aaf_pacing.png)

> The chronogram above is generated (editable WaveDrom master
> [`wd_aaf_pacing.json`](../diagrams/wd_aaf_pacing.json); regenerate with
> `~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py docs/diagrams/wd_aaf_pacing.json`
> — it emits the `.svg` and the `.png`).

**NxN** means the whole media plane is one shared engine per function
plus N per-stream BRAM contexts, selected at build time with
`--num-streams` ([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) argparse: "AAF stream contexts
per shared engine").

The deployed shapes are the AX7101 at 8×8 streams and the Arty A7 at 4×4
([`SYSTEMS_ENGINEER_GUIDE.md`](../SYSTEMS_ENGINEER_GUIDE.md) §0 topology
figure). Every stream carries up to 8 channels, so both directions
expose 64 stream-channels ([`CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) §1).

## 2. Talker path — capture to wire

### 2.1 Capture frontends and the pair-stream contract

Every audio source speaks one contract into the packetizer: a
`{pair_valid, pair_slot, pair_l, pair_r}` pulse stream — one pulse per
stereo pair of 24-bit left-justified samples, in the datapath clock.

Serial capture runs in the interface's own bit-clock domain and crosses
through a gray-pointer `cdc_pair_fifo`
([`hdl/ieee1722/aaf/KL_tdm_capture.sv`](../../hdl/ieee1722/aaf/KL_tdm_capture.sv) "INTERFACE CONTRACT (the whole
capture family)"; grounding rows G2/G4 in
[`CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) §0). The sources:

| Source | Module ([`hdl/ieee1722/aaf/`](../../hdl/ieee1722/aaf)) | What it is |
|---|---|---|
| I2S in | `KL_aaf_capture_i2s.sv` | I2S master for the Pmod I2S2 ADC (CS5343): clean registered dividers off the 24.576 MHz audio MMCM (MCLK /2, SCLK /8 = 64 fs, LRCK /512 = 48.000 kHz), 24-bit Philips capture, emits pair slot 0 |
| TDM in | `KL_tdm_capture.sv` | TDM bus slave, 8/16/32 slots × 16/24/32 bit clocks, MSB first; pair k carries TDM slots {2k, 2k+1}; accepts both pulse and 50 %-duty frame syncs, data delay 0/1 |
| ALSA playback | `KL_pcm_tx.sv` | Reads a host-written PCM ring (per-stream sub-rings, S32BE wire byte order) and emits the same pair stream — the playback counterpart of the RX ring, see §2.2 |
| Pilot tone | `KL_tone_gen.sv` | 1 kHz exact-period 48-entry 24-bit sine, table at FULL SCALE (digital THD+N −148.1 dB per the module header); enabled by `TONE_CTRL 0x6DC[0]`, it replaces the ADC samples on both channels. `TONE_CTRL[3:1]` attenuates in −6 dB steps (reset 0 = 0 dBFS), so a capture at amplitude 0.25 means `att = 2` and not a quarter-scale generator. Raising it to 0 dBFS is safe only when the whole path is 48 kHz; through a rate conversion a full-scale sampled sine overshoots between samples (measured +0.91 dB) and clips. See [`../findings/MEDIA_CLOCK_LOCK_0810.md`](../findings/MEDIA_CLOCK_LOCK_0810.md) |

The two serial-bus frontends have exact frame timing worth a picture.
First the I2S frame (capture and render share the same Philips shape —
the render serializer in `KL_i2s_playback.sv` obeys the same 1-bit-delay
rule, where a doubled delay was the historical sign-square failure):

![I2S Philips frame timing — the 1-bit delay after each LRCK edge and the capture latch points](../diagrams/wd_i2s_philips.png)

> The chronogram above is generated (editable WaveDrom master
> [`wd_i2s_philips.json`](../diagrams/wd_i2s_philips.json); regenerate with
> `~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py docs/diagrams/wd_i2s_philips.json`
> — it emits the `.svg` and the `.png`).

And the TDM8 slave frame — the armed-fsync rule, the `DATA_DELAY_P`
offset, and the even-holds/odd-pushes pair cadence:

![TDM8 slave frame — armed fsync edge, DATA_DELAY_P, MSB-first slots and pair pushes](../diagrams/wd_tdm8_frame.png)

> The chronogram above is generated (editable WaveDrom master
> [`wd_tdm8_frame.json`](../diagrams/wd_tdm8_frame.json); regenerate with
> `~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py docs/diagrams/wd_tdm8_frame.json`
> — it emits the `.svg` and the `.png`).

`KL_pcm_tx` deserves its own paragraph because it is the ALSA *playback*
path (roadmap item 7). Its header states the design intent verbatim: "a
drop-in replacement for the physical capture front-end … it emits the
SAME {pair_valid, pair_slot, pair_l, pair_r} contract that
KL_aaf_packetizer consumes, but the samples come from a host-written
DRAM/BRAM ring rather than an ADC" (`KL_pcm_tx.sv` header).

All of the following is from the same header:

- **Ring ABI** — mirrors the RX PCM ring in the read direction (base /
  per-stream length / stride, absolute monotonic `wr_ptr` doorbell per
  stream, published `rd_ptr`).
- **Pacing** — one media tick = one sample for every stream and every
  channel pair, so 6 ticks fill one PDU per stream.
- **Underrun / overrun** — an underrun still emits the pair (repeat-last
  or digital silence, CSR-selected) so the media cadence never skews; a
  host overrun fast-forwards the read pointer one ring lap.
- **De-interleave** — byte-identical to the packetizer payload, so
  ring → packet → wire → depacketizer → ring is byte-exact.

In the SoC it is compiled in with `--aaf-playback`
([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py), `AAF_PLAYBACK_P` generate) and wired two ways
in [`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) (`g_aaf_playback` block): `pb_enable`
swaps it wholesale for the ADC frontend at the packetizer's pair port,
and its raw pair bus is also exposed as the capture mux's RING source
bucket.

### 2.2 The capture mux (channel map, TX side)

[`hdl/ieee1722/aaf/KL_chan_map_capture.sv`](../../hdl/ieee1722/aaf/KL_chan_map_capture.sv) sits between the sources and
the packetizer: a 32-entry map RAM (one 8-bit entry
`{en[7], src[6:4], idx[3:0]}` per TX pair slot) selects, per slot, one
of the buckets ZERO / I2S_IN / TDM_IN / RING / TONE.

Source pairs are latched free-running into hold registers; on each
media tick the engine walks the enabled slots low-to-high and injects
one pair per slot with a settle gap — six ticks fill one PDU per talker
(module header).

The CSR `0x900` window and the AEM audio-map command set share the map RAM
through one arbiter. `GET_AUDIO_MAP`, `ADD_AUDIO_MAPPINGS`, and
`REMOVE_AUDIO_MAPPINGS` are implemented. The command path owns the
authoritative per-port mapping store and projects backed output rows into this
RAM. The CSR is a local maintenance path and is refused while `LOCK_ENTITY` is
held by a controller.

An accepted output edit reserves every referenced AAF stream after its phase-1
streaming recheck. A raw 0-to-1 enable arriving from ACMP, SRP, or the local
bypass remains masked until phase 2 completes or the transaction aborts. An
output already streaming is rejected at phase 1. This closes the interval in
which a local or protocol start could previously occur between validation and
the phase-5 RAM writes.

The host-playback wholesale override (`pb_enable`) outranks the lane mux
either way — an active ALSA session claims the pair source exactly as the
driver contract documents.

### 2.3 The shared packetizer and the channel math

[`hdl/ieee1722/aaf/KL_aaf_packetizer.sv`](../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv) is one framer/serializer with N
talker contexts in a BRAM context RAM (TCTX: enable, channels, VLAN,
DMAC, stream UID, sequence number, latched presentation time, frame
counter) plus a double-banked sample staging RAM; the bank swap is the
6-sample epoch boundary and scheduling is round-robin over pending banks
(header §2.2/§2.3 references into [`NXN_ARCHITECTURE.md`](../NXN_ARCHITECTURE.md)). The channel
math, quoting the header's IEEE 1722-2016 citations:

- `channels_per_frame` is TCTX `w0.chans`, **even 2..8** (the pair
  stream is 2-channel-granular); 0/1 clamp to 2, odd values to the next
  even, > 8 to 8; changing it mid-stream is not supported.
- The pair-slot space is partitioned by a **prefix sum of chans/2**:
  talker *t* owns pair slots `[sum(chans/2 below t), +chans/2)` — with
  all-stereo talkers this degenerates to slot *k* = talker *k*.
- On the wire, `channels_per_frame` is the 10-bit field of Figure 26 at
  frame bytes 35/36 (clause 7.3.3); the payload is 6 samples × C
  channels × 4 octets, format INT_32BIT, clause 7.3.5 chronological
  interleave, network byte order; `stream_data_length` (4.4.4.10)
  = 24·C; the frame is **42 + 24·C bytes ≡ 2 (mod 8)** so the last AXIS
  beat always keeps exactly 2 bytes and the beat count is 3·C + 6.
- C = 2 reproduces the historical 90-byte frame byte-identically, and
  talker 0 aliases the legacy flat CSR config (`AAF_CTRL 0x654` group,
  `milan_csr.sv`) — both gated by golden byte-compare TBs (header
  "no-regression axiom").

Pacing is disciplined by `KL_media_adv.sv`: the binary divider chain
alone would run at 48,828.125 Hz (+1.725 %, outside the listener servo's
±1.56 % capture range — the audible-pumping root cause, measured on the
wire 2026-07-18 as 122,880 ns per 6-sample frame); the fractional-N
advance strobe deletes ~1.7 % of counter advances so the chain averages
true 48 kHz (module header; row
[AVTP-12](../traceability/ieee1722-2016.md)).

### 2.4 Egress: CBS, the post-shaper inject, PTP stamping

The host TX path (Linux frames via kl-eth DMA) runs through
`traffic_controller_802_1q` — 802.1Q classification plus the 802.1Qav
credit-based shaper — and then `ptp_ts_top`, which hardware-timestamps
egress frames (`milan_datapath.sv` "shaper→PTP→ADP arbiter" TX
ordering).

The fabric AAF stream does **not** queue through CBS: it is injected
after the shaper through the `aaf_final_mux` arbiter — the in-tree
comment is explicit: "AAF injected AFTER the shaper (MVP: bypasses CBS
for continuous emission, like ADP; class-A shaping = the is_1g
follow-up)" (`milan_datapath.sv`).

Bandwidth protection instead comes from admission: an SRP reservation
is a precondition for AAF transmit (`FR-SRP-03`), the reservation also
resolves into the class-A CBS idleSlope for the host-side queue, and
`AAF_CTRL[1]` remains the bypass escape hatch
([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) 0x680 SRP section).
That reservation is the **protocol processor's** now — the datapath reads
`sr_admitted` / granted slope / adopted domain off its class-D face every
clock, where it used to read `KL_lwsrp_bw_gate`. The slope-vs-gate ordering
changed shape and not safety; the honest account is in
[`../reference/EGRESS_QUEUE_MAP.md`](../reference/EGRESS_QUEUE_MAP.md).

Per-stream admission for talker t > 0 composes TCTX enable, the
per-stream SRP admission gate and the engine-wide MAAP claim
(`milan_datapath.sv`, `aaf_stream_en_w`); at t = 0 the same terms compose as
`aaf_gate`, where the DA term now lives *inside* the declaration (the
processor's talker cannot declare without a MAAP `ALLOC_DA` success).

Presentation time is **not** stamped at egress — it was latched at
first-sample capture inside the packetizer (§1). The independent
`ptp_ts_top` wire-egress timestamp and the fabric's capture-epoch
register (`TX_EPOCH 0x874`) exist precisely so the two can be
reconciled ([`AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md), TX
pipeline notes).

## 3. Listener path — wire to render

### 3.1 Classification and stream match

RX frames pass the MAC, the `ptp_ts_top` RX timestamp point and the
TCAM DMAC filter; `avtp_stream_parser` observes the RX AXI-Stream
non-intrusively and matches the **wire-truth stream_id** against
`KL_stream_table` — never the DMAC. Table entry 0 aliases the bound record
combinationally (the N = 1 no-regression shape) — that record is now
published by the protocol processor's ACMP listener over the class-D face,
and `bound` is what a reader must take as truth (`ACMPL_STATE` no longer
tracks PROBING/SETTLED); entries 1..N−1 are written through the CSR 0x800 window
([`hdl/ieee1722/avtp/KL_stream_table.sv`](../../hdl/ieee1722/avtp/KL_stream_table.sv) header).

### 3.2 The RX monitor: lock and counter contract

[`hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`](../../hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv) (flat, single-stream) and
`KL_avtp_rx_monitor_ctx.sv` (the shared NxN engine the datapath
instantiates) implement the Milan STREAM_INPUT diagnostic counters
(IEEE 1722.1-2021 Table 7-156 / Milan §5.4.5.3), with the contract
byte-extracted from the PipeWire module-avb reference (module header):

- **UNSUPPORTED_FORMAT**: per-PDU compare of the AAF header fields
  against the current STREAM_INPUT format; such a PDU counts *nothing
  else* — no FRAMES_RX, no lock effect.
- **FRAMES_RX**: every format-valid PDU.
- **MEDIA_LOCKED**: ticks on the first valid PDU while unlocked, then an
  **8-PDU settle window** re-seeds the expected sequence number instead
  of counting the one-time bind/SRP-path-open step.
- **SEQ_NUM_MISMATCH**: any discontinuity after settle;
  **STREAM_INTERRUPTED** additionally when ≥ 2 PDUs were lost.
- **MEDIA_UNLOCKED**: silence > **100 ms** while locked, watched every
  cycle.
- Counters (and lock/settle state) reset on the **not-bound → bound**
  transition only (Milan Table 5.6), never on unbind.
- The ctx engine also computes LATE/EARLY timestamps from `ts_delta`
  against the presentation offset (§1), and for an external clock
  source the media-lock condition additionally requires playback-servo
  convergence (`servo_conv_i` port note — house rule). On this build the
  clock source can never *be* external (`SET_CLOCK_SOURCE` is gone, index
  pinned at 0 = INTERNAL), so that arm of the rule is unreachable and media
  lock is the immediate internal-clock case.

These are the **STREAM_INPUT** counters, and they are untouched by the
control-plane substitution: the `0x6B8` `A_STRMW_CNT` window and the
per-stream Table 7-157 views are live. What died with GET_COUNTERS is the
**STREAM_OUTPUT** side — the Milan Table 5.4 talker counter context is no
longer instantiated at all, because nothing could have read it.

The monitor's `pdu_accept_p` pulse (bound + stream_id + format valid,
fired at parse-complete) is the **commit verdict** for the
depacketizer. CSR view: `0x6B8 AVTPRX_STAT` (low counter bytes +
media-locked level), `0x6BC AVTPRX_FRX`, `0x6C0 AVTPRX_ERR`
([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md)), and per-stream full Table 7-157 counter windows at
`0x830–0x854` in the 0x800 indexed window.

### 3.3 The depacketizer

[`hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv`](../../hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv) taps the RX AXI-Stream
(never backpressuring the datapath), buffers each frame through a
drop-capable FIFO, and emits **only the AAF sample payload** — wire byte
order = S32BE interleaved PCM, one AXIS frame per PDU, always full
8-byte beats, `tuser` = stream index.

Frames without the monitor's accept pulse are dropped at FIFO commit,
"so the ring receives exactly the PDUs FRAMES_RX counts"; payload
realignment strips 38 (untagged) or 42 (C-VLAN) header bytes; Milan
base-format payloads are 8-byte multiples (48 k: 192 B) (module header).

Whole-frame drops and emitted payload counts sit in `PCMRX_CNT 0x6C4`;
the last accepted PDU's `avtp_timestamp` in `PCMRX_TS 0x6C8`
([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md)).

### 3.4 Routing and the PCM DMA ring

[`hdl/ieee1722/aaf/KL_pcm_route.sv`](../../hdl/ieee1722/aaf/KL_pcm_route.sv) gives every stream two independent
flags — `{RENDER, DMA}` — so a stream can render, land in its DMA ring,
both, or neither; exactly one stream renders (lowest index wins); reset
default is stream 0 = RENDER|DMA, bit-identical to the pre-NxN shape
(module header; the flags are LCTX `w4`, CSR `A_STRMW_CTRL 0x810`).

The DMA ring is where ALSA capture reads from:

- **DRAM (default)**: `_PCMRingNxN` in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) — a
  `WishboneDMAWriter` loop ring; per-stream sub-rings at
  `base + s·stride`; the LiteX CSR bank at `0xf0003120`
  (`base/length/enable/loop`, `offset` = the write pointer the consumer
  chases); payload stays full 64-bit words in wire byte order
  ([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) "PCM ring" section).
- **BRAM (option)**: `--pcm-ring bram` swaps in
  [`hdl/ieee1722/aaf/KL_pcm_ring_bram.sv`](../../hdl/ieee1722/aaf/KL_pcm_ring_bram.sv), a dual-port on-chip ring at
  the MMIO window `0x9010_0000` (32 KB) with the **same** CSR ABI, so
  the driver is unchanged. Because a BRAM write completes in one cycle,
  `sink.ready` is constant 1 — no beat can ever be shed and the DRAM
  read artifact cannot exist (`milan_soc.py` `--pcm-ring` help +
  `MILAN_PCM_BRAM_BASE` comment; module header). See §6 for why this
  option exists.

### 3.5 ALSA capture (`snd-kl-milan`)

The ALSA card driver `snd-kl-milan` and the PipeWire
`pw-milan-ring-source` consumer live in the **private test repo**, not
here — see that repo's
`fpga/docs/ALSA_DRIVER_DESIGN.md` (referenced from
[`CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) companions).

The contract it consumes is entirely on this side: the ring ABI of §3.4
(`offset` CSR = the hardware pointer) and the S32BE interleaved word
format. The BRAM option was designed to keep that driver unchanged
([`MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) §2).

### 3.6 Physical render and the wire-truth rule

The RENDER-flagged stream feeds `KL_pcm_lpf` (20 kHz Butterworth biquad,
serial-MAC so it closes timing at 100 MHz, ~12 clk/pair — absorbed by
the playback FIFO) and `KL_i2s_playback` (CS4344 DAC, clean-clock:
plain dividers in the dedicated audio MMCM domain, gray-pointer CDC).

The audio domain free-runs; underrun repeats the last pair, overrun
drops, both rails counted in `I2SPB_STAT 0x6D8`. The DAC serializer's
frame timing is the same Philips shape as the §2.1 chronogram — the
1-bit delay comes from its output-register pipeline.

In parallel, `KL_chan_map_render` clones the depacketizer payload
stream and keeps a latest-sample latch of all 64 (stream, wire-channel)
values, rendering any of them onto 10 physical output channels (I2S L/R
+ TDM8 lane 0) through its map RAM; `KL_tdm_render` serializes the TDM8
output frame (module headers). Since item-7 it keeps a **second**
latest-sample latch over `KL_pcm_tx`'s pair bus, so a map entry with
`SRC = PCM_TX` renders the **host playback ring** onto a physical
output - the only route from an ALSA playback ring to the line-out that
does not go out on the wire and back.

Which of the two sources reaches the DAC, and at what rate, is
`KL_i2s_feed_mux`. Its select was `aecp_dmap_dyn | CHMAP_CTRL[0]`; with no
dynamic-map writer anywhere on the device the first term is a structural 0, so
**`CHMAP_CTRL[0]` alone selects** (0 = the listener render tap passed through
bit- and cycle-identically, LPF override included). Crossbar mode delivers
the phys{0,1} pair on the **48 kHz media tick**, with the
LPF masked because it belongs to the listener tap it filters. The pace
has to move with the source: the listener feed's strobe is an inbound
depacketizer beat and its stride is the listener's channel count, so a
crossbar output clocked by it does not advance at all without an
inbound stream, and gets its L/R swapped whenever an unrelated
listener reports an odd channel count. `PBK_STAT`/`PBK_FEEDS`/
`PBK_RAILS` (`0x8C8`, [`REGISTER_MAP.md`](../reference/REGISTER_MAP.md))
read the chain end to end.

The rendering rule throughout is **wire truth**: de-interleave stride
and channel count follow `channels_per_frame` *from the wire* (the
monitors export `wire_chans` per stream; 0-before-first-accept is
treated as 2), never a declared format. The rule was written against the AEM
store, and a declared format can be readable on this device again — whatever
descriptor image is loaded in DDR3 is what `READ_DESCRIPTOR` serves, so a
controller can once more be told a channel count. That is exactly the input the
rule refuses to trust. The image is authored ahead of the build and no runtime
writer updates it, so it can declare a width the front-end cannot feed just as
easily as a live AEM store could; the fabric keeps de-interleaving by what
arrived on the wire.

The declared-8ch/wire-2ch mismatch produced total silence in the field
and the store-driven stride bug played quarter-rate garbage (rows
[AAF-4](../traceability/ieee1722-2016.md) and
[M-FMT-2](../traceability/milan-v12.md);
`KL_chan_map_render.sv` header).

## 4. Latency: presentation offset vs pipeline

Two different numbers, often conflated:

- The **presentation offset** (transit time) is policy: how far in the
  future the talker stamps each PDU. **On this build the policy is fixed at
  the Milan 2 ms default** — `SET_MAX_TRANSIT_TIME` and the
  `SET_STREAM_INFO(MSRP_ACC_LAT)` sub-command were its only writers, and
  neither is implemented: the µCPU echoes `NOT_IMPLEMENTED` and the offset
  stays where it was. Every measurement below was taken at a
  *chosen* offset (pto 500 µs) on a build that could still be told; the
  relationship it establishes holds, the number a controller can set does
  not.
- The **pipeline latency** is physics: how long capture → wire → ring
  actually takes. Unchanged — no measurement on this page was taken through
  anything that was deleted.

The measured relationship on this bench (2026-07-24/25,
[`SYSTEMS_ENGINEER_GUIDE.md`](../SYSTEMS_ENGINEER_GUIDE.md) §0
"Measured truth"): **end-to-end capture→render equals the presentation
offset exactly** — with pto = 500 µs the listener sees
`ts_delta` +384 µs and **0 LATE**, and the datapath pipeline is
**≈ 116 µs** (AX7101, 100 MHz datapath build).

In other words the pipeline fits comfortably inside the 500 µs budget
and the presentation mechanism, not queueing, sets the delivered
latency. The §1 pacing chronogram draws exactly this: the accept lands
well before the presentation instant, and `ts_delta` is the remaining
margin.

**Where the talker half of that pipeline goes (measured per stage,
2026-07-26, AX7101 `VERSION 0x0001_000B`, 100 MHz datapath):** capture →
first packetizer beat is **≤ 125.04 µs** (the 6-sample accumulation
window at 48 kHz), the packetizer itself is a **constant 110 ns**, and
last beat → MAC egress is **≤ 125.29 µs** (one class-A observation
interval waiting for the shaper slot) — 0 timeouts over 65 k+ frames.
Worst-case fabric TX is therefore **≈ 250 µs** as an envelope bound,
while the live `ts_delta`-derived figure above (≈ 116 µs) is the typical
case; the two are consistent because the two dominant terms are windows
a frame lands *somewhere inside*, not queues it must drain. Neither term
shrinks with a faster clock — they are protocol structure (samples per
frame, class interval). Full per-stage numbers and the reading rules:
[`AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md).

Where those numbers come from:

- [`AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md) — the authoritative
  tap map (roadmap item 11): TX chain CAP → PKT_SOF → PKT_EOF → MAC_TX,
  RX chain MAC_RX → ACCEPT → DEPKT → PCM_RING, each inter-stage delta
  exposed as last/min/max in the CSR `0x870` block
  (`KL_aaf_latency_taps.sv`), deltas in datapath-clock cycles, one
  in-flight reference frame per chain with a 0.5 ms per-stage timeout.
  The diagram at the top of this page marks the same tap names.
- [`LATENCY_HISTORY_RING.md`](../LATENCY_HISTORY_RING.md) — the
  per-sample time series (`KL_lat_history_ring`): every completed delta
  becomes a 16-byte record (gPTP ns, latency, stage_id, stream, seq/gap
  flags) streamed into a DRAM ring with the PCM ring's CSR ABI, for
  jitter histograms and tail latency offline (TB: 84 checks, 0
  failures, per that doc).
- `ts_delta` at CSR `0x6EC` (§1) is the live end-of-chain check: signed
  margin between presentation time and now at PDU accept.

## 5. Channel mapping — 64 in / 64 out

Both directions expose 64 stream-channels (8 streams × up to 8
channels). The fabric **selects, never composes**: the TX side is the
32-pair-slot capture mux of §2.2 (each slot picks a source pair), the RX
side is the render crossbar of §3.6 (any stream-channel to any of 10
physical outputs) plus the per-stream DMA rings that PipeWire composes
in software.

The IEEE 1722.1 dynamic audio-map commands `GET_AUDIO_MAP`,
`ADD_AUDIO_MAPPINGS`, and `REMOVE_AUDIO_MAPPINGS` (command types 43, 44, and
45) are implemented. ADD and REMOVE stage the complete command, validate every
record, recheck output streaming state at commit, and then update the
authoritative mapping store plus any physical RAM projection atomically.
`GET_AUDIO_MAP` reads that authoritative store. The CSR `0x900` window remains
a local maintenance interface under the same arbitration and entity-lock
rules. See the command and ownership contract in
[`CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) section 7.

Deep doc: [`CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) — the normative 64×64
architecture, both map-word formats, the pair-slot widening, and the
CSR-word-vs-RAM-word packing trap that eats an afternoon if you write the
8-bit RAM word into the 16-bit `CHMAP_WORD` field.

## 6. Status (2026-07-26; control-surface addendum 2026-08-13)

Honest state of this subsystem, with evidence:

- **The media plane's own status is unchanged by the 2026-08-13
  substitution** — every result below was measured through blocks that are
  still in the tree. What the substitution removed is the ability to
  *reconfigure* the plane from a controller (banner at the top of this page):
  no format or rate command, no audio-map setter, no transit-time command,
  no clock-source selection, and no STREAM_OUTPUT counters to report with.
  A stream is still discovered, connected, reserved and streamed; it is
  configured by the build and by the CSR plane, over ssh. Enumeration is
  **reachable** again — the processor's AECP µCPU answers `READ_DESCRIPTOR`, so
  a controller can read this entity's model and see the streams it is talking
  to — but see the next bullet before expecting it on a stock build.

- **Bring-up gained a step nothing in this repository performs: load the
  descriptor image before enabling the entity.** The µCPU's descriptor store
  fetches the model from main memory over a read-only master whose base is
  fixed at compile time — no base register, not relocatable, derived by the
  LiteX SoC as the top 1 MiB of `main_ram`. Write the image there first; enable
  the entity second. Get that order wrong, or skip the load entirely, and every
  `READ_DESCRIPTOR` answers `BAD_ARGUMENTS` — an invalid image reports zero
  configurations, and the argument check runs before the locate. That status is
  how you tell the two failures apart: `BAD_ARGUMENTS` everywhere means no image
  (or a corrupt one), while `NO_SUCH_DESCRIPTOR` means the image loaded and that
  descriptor is genuinely absent from the model. **Today it is skipped**: the
  image generator lives in the `protocol-processor` submodule, no step in
  `sw/builder/`, `scripts/`, the SoC builder or the boot path turns an
  `endstation_*.yaml` into it or writes it to DRAM, and the
  `aecp_aem_rom.svh` the builder still emits is an orphan of the deleted
  fabric AEM store, not this image. The failure is at least diagnosable and
  recoverable: a zeroed region fails the header's magic compare (`"AEMI"`,
  layout version 1, plus checksum) so it reads as *image not loaded*, the
  store's watchdog abandons a stalled burst rather than hanging, and a **late
  load heals without a reset** because every locate against an invalid image
  re-arms the header probe.

- **Record path (listener → ALSA): proven on silicon.** E2E
  capture→render = the presentation offset (pto 500 µs, 0 LATE), talker
  wire output bit-exact against the tone table (900/900), full
  board→board→PipeWire→board loop at −72.7 dB THD+N
  ([`SYSTEMS_ENGINEER_GUIDE.md`](../SYSTEMS_ENGINEER_GUIDE.md) §0,
  measured 2026-07-24/25).
- **Playback path (`KL_pcm_tx`): the fabric chain is now continuous and
  TB-proven end to end; SILICON proof still pending.** The engine has
  its own harness (27/27, [`tb/verilator/pcm_tx`](../../tb/verilator/pcm_tx), per
  [`testing/BEHAVE_TEST_PLAN.md`](../testing/BEHAVE_TEST_PLAN.md)) and
  the SoC integration is in-tree behind `--aaf-playback`
  (`milan_datapath.sv` `g_aaf_playback` + the `pb_*` CSR block and
  word-fetch bridge in `milan_soc.py`). Until 2026-07-26 the ring
  reached only the **talker** (packetizer pair port); it had no path to
  the local DAC at all, because the render crossbar had no playback
  source and the DAC feed was strobed by inbound listener traffic.
  [`tb/verilator/pcm_playback`](../../tb/verilator/pcm_playback) now drives host-ring words in and decodes
  the serialized DAC output back with a spec-derived I2S receiver: 40/40
  checks, 41 consecutive ring words replayed bit-exactly on the pin with
  the listener side completely silent, plus the ring under-run /
  over-run / disarmed-map / mid-stream-channel-count negatives. What is
  NOT proven is anything past the RTL: no board has been flashed with
  this gateware and no ALSA sink drives it yet.
- **The DRAM-ring artifact and the BRAM option.**
  [`MILAN_COMPLIANCE_GAPS.md`](../MILAN_COMPLIANCE_GAPS.md) §2 records
  two silicon failure classes on the DRAM ring path: the real-time
  writer **sheds a beat under CPU DRAM contention** (mitigated by the
  CDC-depth 16 → 128 fix, not killed at root) and **I6**, a 1-in-24
  read artifact that survives CDC-128 (write-posting vs OFFSET-CSR
  ambiguity, still open). The `--pcm-ring bram` option (§3.4) kills
  both at the root — always-ready write port, no DRAM
  controller/posting between writer and reader — at ~8 RAMB36 for
  32 KB; DRAM remains the default.
- **Formats family.** Milan §6 base formats:
  [M-FMT-1](../traceability/milan-v12.md) (base audio format set
  declared and accepted) and [M-FMT-2](../traceability/milan-v12.md)
  (listener format adaptation, the wire-truth rule) are both verified.
  The AAF clause-7 rows [AAF-1 … AAF-10](../traceability/ieee1722-2016.md)
  are verified (format, sp, nsr, channels_per_frame, bit_depth,
  packing, channel order, presentation time, cadence, TSpec
  derivation); AAF-11 (AES3) is out of declared scope. The last open
  item in the family's neighborhood,
  [AVTP-3](../traceability/ieee1722-2016.md) (version-field gate), was
  CLOSED on 2026-08-08 — the stream parser now discards a
  non-zero-version PDU whole (1722-2016 4.4.3.4), so a version-1 PDU
  can no longer be parsed as v0 media.
