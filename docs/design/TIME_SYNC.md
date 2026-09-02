<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# Time synchronization — gPTP, the PHC, and the media clock

How time works in this system, top to bottom: what 802.1AS (gPTP) gives us,
where fabric timestamps are made, how the integrated engine disciplines the
PHC, and how media clock recovery works. Since #74 the root consumes the stored
clock-source selection: selecting the CRF source steers the audio clock, while
the power-on INTERNAL state free-runs. Register offsets follow
[`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) (the CSR ABI
authority); status claims carry their in-repo evidence. Updated 2026-09-02 for
VERSION `0x0002_0057` and the live #74 clock-source consumption.

Current command, clock-consumption, and notification claims are checked against
the [Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `crf.media-clock-consumption` | `implemented` | - |
| `gptp.fabric-product-owner` | `implemented` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

![The time-sync clock chain](../diagrams/timesync_chain.png)

> The picture above is generated (editable
> [timesync_chain.drawio](../diagrams/timesync_chain.drawio); regenerate with
> `python3 docs/diagrams/timesync_chain.gen.py docs/diagrams/timesync_chain &&
> rsvg-convert -w 2000 docs/diagrams/timesync_chain.svg -o
> docs/diagrams/timesync_chain.png`).

## Contents

- **[1. Concept -- the three clocks](#1-concept----the-three-clocks)** -- Distinguishes the gPTP-disciplined PHC, the softcore's own timebase, and the physical audio clock, then records that the power-on audio source is INTERNAL and that a CRF selection now steers it.
- **[2. Mechanism -- the hardware timestamp path](#2-mechanism----the-hardware-timestamp-path)** -- Follows the fractional-nanosecond counter, RX and TX timestamp points, fabric consumption and latency corrections at the MAC boundary.
- **[3. The media clock](#3-the-media-clock)** -- How a shared nanosecond timeline becomes a 48 kHz sample edge: the PI servo, the grid-alignment loop, and the `media_clk_resolve` verdict that makes the stored clock-source selection reach them (#74). The section also records the master-role error budget and measured historical loop behavior.
- **[4. Time-related CSRs -- quick table](#4-time-related-csrs----quick-table)** -- Lists every time and media-clock register from the PHC controls through CRF measurements, latency taps, and the servo status.
- **[4a. Centered-FIFO regulation goal (USER 2026-08-07): +/- 125 us](#4a-centered-fifo-regulation-goal-user-2026-08-07---125-us)** -- The standing regulation target: the DAC elasticity FIFO stays centered and its wander holds within one class-A frame period (+/-6 pairs), earned by clock quality rather than buffer depth
- **[4b. Grandmaster loss and recovery](#4b-grandmaster-loss-and-recovery)** -- Pointer to [GM_LOSS_RECOVERY.md](GM_LOSS_RECOVERY.md), the transient story: what a GM hand-off costs at each layer and why it is now one MEDIA_RESET click + ~100 ms with the lock held
- **[5. Status (updated 2026-09-02)](#5-status-updated-2026-09-02)** -- Evidence ledger for PHC/timestamp, gPTP and CRF/media-clock claims, followed by the remaining calibration, BMCA, Pdelay-edge and bench-acceptance gaps

## 1. Concept -- the three clocks

gPTP gives every device on the AVB segment one shared nanosecond timeline.
One node is elected grandmaster (GM); everyone else measures its link delay to
its neighbor (pdelay) and steers a local hardware clock until the shared
timeline agrees to nanoseconds. Milan requires this (it is what makes
presentation times meaningful), and everything below the protocol runs in our
fabric.

Three clocks exist on each board, chained in one direction:

1. **The network clock — the PHC** (PTP Hardware Clock). A 64-bit
   nanosecond counter in the fabric
   ([`hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv`](../../hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv)). This is the clock
   gPTP disciplines and the clock every hardware timestamp is drawn from.
   When the board is GM, the PHC free-runs and everyone else follows it.
2. **The system clock** — the bare-metal softcore's own timebase. Nothing in
   the media path depends on it and it never owns gPTP state.
3. **The media clock:** the 24.576 MHz audio MMCM output, divided to the
   48 kHz sample grid that the I2S/TDM front-ends run on. It is a *physical*
   clock (a DAC cannot consume "nanoseconds"), so it cannot be written like
   the PHC. The recovery hardware steers it from CRF timestamps once a
   controller selects the CRF clock source; the power-on state is INTERNAL
   free-run (section 3).

The current chain, in one sentence: the fabric gPTP engine disciplines the PHC
and timestamps frames, and the stored clock-source selection resolves in the
root — with CRF selected the MMCM servo steers the audio clock and the grid
aligner follows it; with INTERNAL selected the audio MMCM free-runs.

## 2. Mechanism -- the hardware timestamp path

### 2.1 The PHC counter and its CSR group (0x500)

`timestamp_counter.sv` is a fractional-nanosecond phase accumulator
`{ns[63:0], frac[23:0]}`. Each tick adds `PTP_INCR + PTP_ADJ`, both Q8.24
nanoseconds. The fabric engine owns rate and offset adjustment in the product
build; the CSR interface retains direct clock operations for boot diagnostics
and the verification-only option-OFF elaboration (REQ-PTP-01..04):

* **rate** (`adjfine`): `PTP_ADJ` (0x508) is a signed per-tick addend;
* **settime**: `PTP_TOD_WR_*` + `PTP_CMD[0]` loads an absolute time;
* **adjtime**: `PTP_OFFSET_*` + `PTP_CMD[1]` adds a signed delta once;
* **gettime**: `PTP_CMD[2]` latches a snapshot into `PTP_TOD_RD_*`
  (64-bit reads on the 32-bit bus are not atomic — the snapshot latch is the
  coherent-read mechanism, [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md)
  "Notes").

The CSR plane and the PHC live in different clock domains;
`ptp_csr_sync.sv` carries values plus toggle-synchronized apply strobes
across (REQ-CSR-03).

On the fully-FPGA LiteX SoCs the PHC clock (`gtx_clk`) is tied to the
datapath clock ([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py), the
`i_gtx_clk = ClockSignal(milan_cd)` instantiation) — 50 MHz on the Arty and
shipping bare-metal AX7101, 100 MHz on the AX7101 bring-up shape — and
`PTP_INCR` carries the matching ns-per-tick. Since the t532
wire-scale audit its RESET value is DERIVED from the instantiator's
`MILAN_CLK_FREQ_HZ` (Q8.24 of the true clock period: 10.0 ns at 100 MHz,
20.0 ns at 50 MHz; the standalone milan_csr default keeps the historic
125 MHz / 8.0 ns contract, REQ-PTP-07) — a free-run PHC ticks true
nanoseconds on every shape before firmware initialization.

The tie is also what lets every consumer of `ptp_now` - the AAF/CRF talkers,
the latency taps, `KL_gptp_txstamp` and `KL_gptp_shadow` - read the counter
synchronously on the AXIS clock without a crossing.

### 2.2 Where frames get stamped

In the shipped datapath the frames that matter - the fabric gPTP plane's own -
are stamped by the plane: `KL_gptp_txstamp` latches the PHC at the first beat
of an `0x88F7` frame at the TRUE MAC boundary (`tx_axis_to_mac`, armed by the
plane's lane), and `KL_gptp_shadow` stamps committed ingress frames off the
filtered RX tap. Since VERSION `0x0056` `milan_datapath` instantiates only
the PHC (`timestamp_counter` + `ptp_csr_sync`); the `ptp_ts_top` TX/RX record
stampers that used to sit in-line (TX between the CBS shaper and the arbiter,
RX directly after MAC ingress) are gone with the general-data chain, because
their records had no consumer once #259 removed the transmit path. The record
core remains a stand-alone verified block (`ptp_ts` suite) and this is what
it does, per direction (`ptp_ts_core.sv`):

* latches the live PHC value at the frame's **first beat** (SOP);
* parses ethertype (`0x88F7`), PTP `messageType` and `sequenceId` at their
  fixed untagged-gPTP offsets;
* **qualifies at TLAST**: ethertype match AND an **event** message
  (`msgType[3] == 0` — Sync, Delay_Req, Pdelay_Req, Pdelay_Resp). General
  messages (Announce, Follow_Up, Signaling) are never recorded — stamping
  them would only burn record slots and invite seq collisions
  ([`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) row AS-5).

Qualify-at-TLAST is the load-bearing part. The original core decided the
record when a timestamp CDC handshake returned, which raced the ingress beat
rate both ways — first record never emitted on slow MII beats, stale
one-frame-late pairing after, records lost on fast back-to-back frames.

The full root cause, the synchronous redesign, and the netlist-forensics
fallout (LUTRAM-inferred record queues mis-wired by the cross-hierarchy
optimizer, rebuilt as explicit flops) are recorded in
the retired timestamp-metadata finding (#259, in git history).

Both exchanges, as this design stamps them:

![gPTP timelines: peer delay and Sync/Follow_Up with the PHC latch points](../diagrams/wd_gptp_pdelay.png)

> Generated chronogram (master
> [wd_gptp_pdelay.json](../diagrams/wd_gptp_pdelay.json); regenerate with
> `~/litex-milan/venv/bin/python3 scripts/gen_wavedrom.py
> docs/diagrams/wd_gptp_pdelay.json`). The plane's stampers latch the PHC at
> the frame's first beat (event messages only), so
> `t1`/`t4` come from hardware records while the peer's `t2`/`t3` arrive
> inside `Pdelay_Resp`/`Pdelay_Resp_Follow_Up`; the active gPTP owner computes
> `meanLinkDelay = ((t4 - t1) - (t3 - t2)) / 2` (802.1AS 11.2.19) and the
> result is published at CSR 0x6E4 (section 4). Cadences per
> [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) rows
> AS-7/AS-8: pdelay 1/s, Sync+Follow_Up 8/s.

### 2.3 Where stamps are consumed

Only the fabric gPTP plane consumes stamps, and it makes its own:
`KL_gptp_txstamp` captures egress time at the final MAC boundary and
`KL_gptp_shadow` captures committed ingress frames against the same live PHC,
returning the matched event stamps directly to the `gptp-processor` engine.
BMCA, Pdelay and Sync/Follow_Up timing therefore live entirely inside the
fabric plane. There is no record stream any more and `IRQ_STATUS[0]`
(`tx_ts_ready`) is a structural zero ([REGISTER_MAP.md](../reference/REGISTER_MAP.md)).

### 2.4 The ingress/egress latency constants

The taps stamp at the MAC-side AXIS boundary, not at the wire (802.1AS
8.4.3's "reference plane"), so each board carries a constant correction.

No shipping correction is claimed yet. Both correction registers reset to
zero, and #117 owns a fresh reference-plane measurement on the exact product
image before nonzero constants can become release evidence.

Uncompensated, the late RX stamps kept `asCapable` permanently false — the
single biggest gPTP field bug of this project
([`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) row AS-3).

Three honest caveats, tracked as traceability rows: the constants are
not yet established per board *type*, there is no per-unit calibration
procedure, and the ingress/egress split has not been measured separately
(row AS-4, MISSING). `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` (0x540/0x544) are
write-only scratch since `0x0002_0056` - the record taps they corrected are no
longer instantiated - and the gPTP plane captures its own ingress and egress
events at the fabric/MAC boundary. That plane's actual wire offset is
therefore part of #117's physical acceptance and is not inferred here.

### 2.5 Who runs where

The split follows the current architecture
([`../overview/ARCHITECTURE.md`](../overview/ARCHITECTURE.md);
[`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) header).
`GPTP_PLANE_EN_P` defaults on: BMCA, Sync/Follow_Up, Pdelay, the servo and the
public state bank all live in the fabric plane ([GPTP_PLANE.md](GPTP_PLANE.md)).
The option-OFF elaboration is verification-only hardware (#259):
`fabric_gptp: false` is refused for product configurations, and only a direct
`milan_soc.py` run reaches the ownerless form for benches.

| Agent | Where | Job |
|-------|-------|-----|
| `timestamp_counter` + `ptp_csr_sync` | fabric | the PHC: rate/offset/absolute set, snapshot reads |
| `KL_gptp_txstamp` + `KL_gptp_shadow` | fabric | the plane's own egress (MAC boundary) and ingress event stamps; `ptp_ts_top`/`ptp_ts_core` are stand-alone verified blocks, not instantiated since `0x0002_0056` |
| `gptp-processor` + `KL_gptp_shadow` | fabric (default) | BMCA, Announce/Sync/Pdelay, PHC servo, and one atomic GM/parent/pdelay/flags publication bank |
| `KL_ptp_clock_validity` | fabric | derives AVTP `tu` and public asCapable from the engine; same-edge discontinuity plus Annex B.1.1 holdover |

With the option on, writes to retained publication addresses cannot change the
live fabric-owned faces. With it off, the fabric never builds a PTP message and
nothing else does either: publications, sync and asCapable are zero, `tu` is
one, and attempted writes are inert. In both states timestamp pairing remains
a fabric transport property.

## 3. The media clock

### 3.1 The audio MMCM — a clean, integer-derived 24.576 MHz

Sample clocks are made from a dedicated MMCM, not from logic dividers of the
datapath clock: fractional-N edge jitter on MCLK measurably wrecked the
converters (analog THD+N collapsed to -4.5 dB; history in
[`hdl/ieee1722/aaf/KL_i2s_playback.sv`](../../hdl/ieee1722/aaf/KL_i2s_playback.sv)'s header).

The chain is two-stage and **integer-only** ([`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py),
`_CRG`). Two plans exist, selected by `audio_tdm_hz`:

* **Plan A (default, I2S shapes):** 100 MHz -> PLL /2 x23 /37 ->
  31.081081 MHz -> MMCM x34 /43 -> **24.575739 MHz = 24.576 MHz
  -10.64 ppm**.
* **Plan B (TDM-master shapes — the shipping Arty 4x4):** 100 MHz ->
  PLL /2 x23 /67 -> 17.164179 MHz -> MMCM x63 (VCO 1081.343 MHz) ->
  CLKOUT0 /44 -> **24.575984 MHz = -0.66 ppm**, with CLKOUT1 /44 /22 /11
  serving the TDM bit-clock family off the same VCO. The re-derivation
  *improved* the base error (44 divides the new VCO where odd 43 could
  never yield an integer 2x/4x sibling).

Integer dividers are a servo prerequisite: UG472 forbids fractional divide
in fine-phase-shift mode, and the best single-stage integer alternative
lands -186 ppm, beyond the servo's trim budget
([current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md)).

`/512` of this clock is the 48 kHz sample grid; I2S (`MCLK/SCLK/LRCK`) and
TDM front-ends are plain registered dividers of it.

### 3.1.1 How exact is 24.576 MHz? — the master-role error budget

"Exactly 24.576 MHz" is only a meaningful demand in the **slave** role,
where the MMCM-DRP servo must converge on someone else's recovered media
clock. When this end-station is the media-clock **master**, its oscillator
*defines* the timebase — every listener (an input-stream clock domain at
the far end, or our own servo when roles are reversed) tracks whatever
cadence we actually produce. The requirement then relaxes to three weaker
ones: stay inside the nominal-rate tolerance a conformant listener must
capture (±100 ppm class), timestamp honestly (AVTP timestamps and the CRF
grid describe the *real* cadence in gPTP time -- Section 3.2's "the wire carries
the actual audio-MMCM rate"), and stay internally consistent (bclk,
packetizer pacing and timestamping all derive from the one physical
clock).

The actual static error, master role, worst case:

| Contribution | Plan A (I2S) | Plan B (TDM-master) |
|---|---|---|
| Divider-plan synthesis (deterministic) | -10.64 ppm | -0.66 ppm |
| 100 MHz board oscillator (physical, dominant) | +-50 ppm class | +-50 ppm class |
| **Total vs a perfect lab reference** | **~ +-60 ppm** | **~ +-51 ppm** |

At 48 kHz, +-51 ppm is +-2.4 Hz — about 2.4 samples/second of drift
against a perfect reference, invisible to every listener because they
servo on our honest timestamps rather than on nominal 48 kHz. The
synthesis share alone is -0.032 Hz (Plan B). Margins: the total sits well
inside the +-100 ppm capture range a receive servo must handle, and our
own servo's sustained-slew ceiling is provisioned at 254 ppm (Plan B;
260 ppm Plan A) precisely to cover the synthesis base plus a remote
talker's +-100 ppm with >2x margin. MMCM jitter is zero-mean and does not
move the average rate — it is a THD+N concern (the `BANDWIDTH=LOW`
cascade-filter note in `_CRG`), not a rate error.

The boundary between benign and broken is written in this repo's own
history: the audio-pumping defect was a talker at 48,828.125 Hz — a bad
fractional-N derivation ~1.7 % (17,000 ppm) off, far outside any servo's
capture range. Small-ppm inexactness as master is fine *by design*;
wrong-divider inexactness is a defect in any role.

### 3.2 CRF out — `KL_crf_tx`, the media-clock talker

[`hdl/ieee1722/crf/KL_crf_tx.sv`](../../hdl/ieee1722/crf/KL_crf_tx.sv) emits the Milan CRF Media Clock Stream
(Milan v1.2 7.3.1 / IEEE 1722-2016 Clause 10): subtype 4, type
CRF_AUDIO_SAMPLE, pull 0, base_frequency 48000, one 64-bit timestamp per
PDU, timestamp_interval 96 — one PDU per 96 sample events = 500 PDU/s.

The timestamp grid is the **real media clock**: an own `/512` divider of
`clk_audio` counts sample ticks, and every 96th event crosses into the
datapath domain where the live PHC value is latched as that event's gPTP
time. The wire therefore carries the actual audio-MMCM rate as the PHC sees
it — not a synthetic 2 ms accumulator.

Milan applies the stream **presentation time offset to CRF exactly as to
media streams**: every emitted timestamp is `event gPTP time + transit_ns`,
from the same offset source as the AAF framer (SET_STREAM_INFO
accumulated-latency field; reset 2 ms) — see the `transit_ns_i` wiring in
[`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv).

A PDU that would collide with a busy serializer is skipped whole, so emitted
timestamps stay truthful and only the cadence stretches. The stream leaves
untagged on the low-rate control lane until a second lwSRP talker
declaration exists (section 5).

### 3.3 CRF in — `KL_crf_rx`, the measurement half

[`hdl/ieee1722/crf/KL_crf_rx.sv`](../../hdl/ieee1722/crf/KL_crf_rx.sv) validates every CRF PDU of the selected
stream against the Milan 7.3.2 profile constants (wrong pull/base/dlen/
interval/type increments `fmt_err`) and produces the two servo inputs:

* **phase**: `delta = crf_ts - ptp_now` at each accepted PDU (CSR 0x744,
  same signed-delta contract as the AAF `ts_delta` at 0x6EC);
* **frequency**: `rate` (CSR 0x748) = accumulated timestamp advance across a
  256-PDU ring (512 ms) minus the nominal 512 ms — signed ns per window,
  i.e. the talker's media clock measured against gPTP. Implementation
  (2026-07-25): the ring is a 256×32 **single-port READ_FIRST BRAM** —
  storing the truncated 32-bit timestamp is bit-exact because the window
  subtraction is congruent mod 2^32, and one same-port access reads the
  oldest entry and overwrites it in place. `rate` updates one clock after
  the accepted PDU (invisible at any CSR poll rate; pinned by the
  [`tb/verilator/crf_rx`](../../tb/verilator/crf_rx) regression). The previous 256×64 flop file was
  the exact placer-overflow victim of the first 8×8+chmap build;
* **lock**: 8 clean consecutive PDUs to lock, 100 ms of silence (or a
  validation error) to unlock, mirroring the AAF media-lock contract.
  Solicited `GET_COUNTERS` serves the supported CLOCK_DOMAIN bank through the
  processor counter face. Since #74 the resolved selection gates consumption,
  so the served lock pair follows a live CRF selection (section 3.4).
  Its counter-change pulse reaches the Milan Table 5.22 scheduler, so the
  served CLOCK_DOMAIN bank also gets the per-descriptor, at-most-once-per-second
  unsolicited `GET_COUNTERS` path.

The followed stream comes from the CRF sink bind (ACMP listener sink 1 —
the bind wins) with the CSR pair 0x738/0x73C/0x740 as the manual bench
lever (`milan_datapath.sv`, `crf_rx` instance).

### 3.4 The MMCM-DRP servo — `KL_mmcm_drp_servo` (MCSRV 0x8F8/0x8FC)

> 🟢 **THE SELECTION IS LIVE SINCE #74** (it was structurally off
> 2026-08-13 → #74). The protocol processor stores `SET_CLOCK_SOURCE`,
> `KL_pp_shadow.sv` exports it, and `milan_datapath`'s `media_clk_resolve`
> block turns it into one registered verdict — the stored index compared
> against this shape's generated `AEM_CRF_CLKSRC_C`
> (`gen/adp_shape_defaults.svh`; `16'hFFFF` on a shape with no CRF source,
> so the compare is structurally false there). That verdict gates this
> servo, the packet-grid alignment loop (Section 3.5.1) and the `mr` machinery.
> With INTERNAL selected — the power-on state — everything below is
> honestly idle: `A_MCSRV_STAT` `0x8F8` reads IDLE with trim 0 until a
> controller selects the CRF source.

[`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`](../../hdl/ieee1722/crf/KL_mmcm_drp_servo.sv) closes the loop when
the resolved selection names the CRF CLOCK_SOURCE descriptor (this shape's
generated `AEM_CRF_CLKSRC_C`); in every other mode
it is IDLE with zero DRP/PS activity.

The loop error is **differential rate**, not phase: `e = local_rate -
crf_rate`, both in gPTP-ns per 512 ms of media events (the module measures
our own audio clock against the PHC over a matching 512 ms window; 1 ppm =
512 units). `CRF_DELTA` (0x744) is deliberately NOT a loop input — it
contains the arbitrary talker+transit phase constant.

A PI controller (integrator halves the error per window, bounded slew
+-100 ppm/window, bounded authority +-200 ppm) drives two actuators:

* **fine (the real one)**: MMCME2 dynamic fine phase shift — UG472-linear
  steps of `1/(56*F_VCO)` = 16.9 ps, glitch-free, wrap-around — so a
  sustained step *rate* is a permanent frequency trim of the live audio
  clock. The 200 MHz PS clock gives a 260 ppm slew ceiling, > 2x the
  10.6 ppm base + 100 ppm talker budget (`milan_soc.py` `_CRG` comment).
* **coarse (DRP, XAPP888)**: on every activation the engine read-verifies
  the CLKOUT0 divider registers; only with `auto_repair` set (MCSRV_CTRL
  0x8FC bit 1, reset 0, bench-gated) and a mismatch does it reprogram them
  through the full reset-sequenced read-modify-write. DRP fractional fields
  have 1/8 resolution (>= 1953 ppm/LSB) — three orders too coarse for a ppm
  servo, which is exactly why the fine-PS actuator exists.

Hardening from the silicon rounds:

* a **step guard** discards any window whose error exceeds ~1024 ppm (a
  local PHC step — GM reboot — used to wind the integrator to the clamp and
  stick there);
* **HOLDOVER** on CRF unlock freezes the trim but keeps stepping at the
  held rate;
* `ps_invert` (0x8FC bit 0) is the bench polarity knob from the mf51
  bring-up where silicon stepped opposite the TB's UG472 reading.

`MCSRV_STAT` (0x8F8) exposes state
(IDLE/VERIFY/REPAIR/ACQUIRE/LOCKED/HOLDOVER/FAULT), the DRP
verify/mismatch and fault flags, and the **signed applied trim in 1/16 ppm
units** in bits [31:16].

### 3.5 The coherent chain and the media-lock rule

**Coherent chain** means: one audio-MMCM lineage carries every media-rate
element — the ADC capture front-end, the CRF talker's timestamp grid, and
(through the servo) the listener's playback clock.

There is no programmable resampler and no NCO anywhere in the *playback*
path; the old playback NCO was removed by the exact-recovery rule and its
trim output reads 0 (`KL_i2s_playback.sv` header). (The *packet-grid* NCO,
`KL_media_nco`, is a different animal - it paces the capture/packetizer
walk, and Section 3.5.1 owns its phase contract.) When the servo locks, talker and
listener run at the *same* frequency, so the playback FIFO neither drains
nor fills and the drift-glitch class (underrun repeats / overrun drops) ends.

The chain was measured end to end 2026-07-23 at **-83.9 dB loop THD+N — the
CS4344+CS5343 converter datasheet floor**
([current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md); the retired
bench report remains in Git history).

The **media-lock rule** ([`hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`](../../hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv), the
MEDIA_LOCKED engine): with an **internal** clock source
(`clock_source_index == 0`) the stream locks on the first valid PDU — lock
means "buffer position established", and slips are accepted as
underrun/overrun rail events.

With an **external** source (CRF) the stream locks **only once the
recovered clock has converged near nominal** (`servo_conv` — the
playback-FIFO convergence flag: fill inside the mid-window sustained for
100 ms, `KL_i2s_playback.sv`), and losing convergence while locked is an
immediate MEDIA_UNLOCKED event. Internal locks immediately; external must
earn it.

### 3.5.1 The grid phase contract — `clk_tdm_i`, `clk_audio_i`, `media_tick_p` (#74)

Three clocks meet at the capture holds, and #74 gives their relationship a
stated contract instead of an accident:

* **`clk_audio_i`** is 24.576 MHz *by contract* (`KL_crf_tx`'s /512 event
  grid, `KL_i2s_playback`, the MMCM servo's measurement all assume it);
  the MMCM steers it under CRF. On the shipping divider plan its true rate
  is `100e6 * 391/1591` = 24,575,738.53 Hz (Plan A, −10.64 ppm).
* **`clk_tdm_i`** carries the physical grid: the TDM master divides it to
  `fsync` by a pure integer plan (elaboration-guarded), so `fsync` follows
  whatever steers `clk_tdm_i` — and follows *nothing else*.
* **`media_tick_p`** is the packet grid — `KL_media_nco`'s fractional-N
  divider of the datapath clock, exactly 48,000.0000 Hz free-running.

**INTERNAL (the power-on state): the grids free-run apart, by the standing
free-run rule** (internal media clock = free-run, slips accepted). The −10.64 ppm
difference slips one sample every 1.9582 s at the capture holds; since
#74 that slip is *counted* (`KL_chan_map_capture`'s `tdm_dup_cnt_o` /
`tdm_skip_cnt_o` — a frequency-phase detector on the frame marker against
the tick), not hidden. Every bench number on record was measured in this
state and still stands.

**CRF selected: one reference chain, one master per link.**

    CRF ──(KL_mmcm_drp_servo, hardware)──► clk_audio/clk_tdm ──► fsync
        ──(KL_media_grid_align, arithmetic)──► media_tick_p

The MMCM consumes the CRF rate error and publishes its command on
`A_MCSRV_STAT[31:16]` — that slice is the MMCM's alone now. The align loop
consumes the front-end frame marker (already in the datapath clock domain)
and holds the packet grid inside a fraction of a sample of the physical
one: a cycle-resolution phase detector (time-since-tick captured at each
frame, a tracking unwrapper for whole-sample folds) into an overdamped PI
in the same 1/16 ppm units as the servo. A chain rather than a shared
command is what actually removes the divider drift: mirroring the MMCM's
command moved both grids by the same ppm and left their nominal offset
intact.

Each link is separately falsifiable: the servo slice under CRF stimulus
and the loop's own law in `tb/verilator/mmcm_servo` and
`tb/verilator/media_grid_align` (closed-loop over the real NCO at the true
391/1591 ratio, both rate directions, zero junction slips, watchdog,
beyond-authority clamp and recovery); the whole chain at the root in
`tb/verilator/milan_dp`'s `obj_aclk` leg (−10.64 ppm measured at INTERNAL,
|ppm| < 0.5 with CRF selected, zero junction slips, both 4.4.4.3 `mr`
triggers, the 10.4.3 negative); the silicon whole on the bench — AX7101
J11.8 (`tdm_fsync_o`) against J11.9 (`media_lrclk_o`), the acceptance line
that stays open on issue #74.

**Degradation is always toward today's behaviour**: a dead TDM feed
disengages the align loop (watchdog, 4 frame periods) and the NCO
free-runs at nominal; deselecting CRF disengages everything and is itself
a 4.4.4.3 source change (one `mr` toggle, then silence toward received
toggles).

### 3.6 AAF presentation time against the PHC

The same PHC dates the audio itself: the AAF packetizer latches
`avtp_timestamp = ptp_now + transit_ns` at each PDU's first sample pair
([`hdl/ieee1722/aaf/KL_aaf_packetizer.sv`](../../hdl/ieee1722/aaf/KL_aaf_packetizer.sv), `tsw_val_r` assignment), and the
listener-side monitor computes `ts_delta = avtp_timestamp - ptp_now` on
every accepted PDU (CSR 0x6EC), counting LATE (delta < 0) and EARLY (delta
beyond offset + margin) per Milan Table 5.6.

This is the number the latency-equals-pto work steers by, and the per-stage
breakdown of where the time goes lives in
[`../AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md) (the 0x870 tap block
latches `ptp_now` epochs per measured frame).

**Its validity has a hard bound.** `avtp_timestamp` is 32 unsigned bits, so
`ts_delta` is a *modular* difference read with a half-range convention, and it
means what it appears to mean only while the two clocks are within one
4.294967296 s lap of each other. Beyond that it walks, and LATE/EARLY alternate
in blocks instead of biasing — measured on silicon, and drawn out in
[`PRESENTATION_TIME_WRAP.md`](PRESENTATION_TIME_WRAP.md), which is also where
the case for driving `TIMESTAMP_UNCERTAIN` from servo convergence state is
made.

## 4. Time-related CSRs -- quick table

Every row here now has a row in
[`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) — the map is the
ABI authority and meanings below are quoted from it. The `(*)` marker this
table used to carry (2026-07-26 and earlier: "live in `milan_csr.sv`, no map
row yet") is **retired**: `GPTP_PDELAY` `0x6E4`, `AVTPRX_TSD` `0x6EC`,
`AS2_LO/HI` `0x730`/`0x734`, the CRF sink group `0x738`-`0x74C`, the CRF talker
group `0x750`-`0x764` and `MCSRV_CTRL[1]` `auto_repair` are all documented
there.

| Offset | Name | One line |
|--------|------|----------|
| `0x008` | `CAP[9]` | PTP capability present |
| `0x010` | `IRQ_STATUS[0]` | `tx_ts_ready` — structural zero since `0x0002_0056` (no TX record stamper) |
| `0x500` | `PTP_CTRL` | `[0]` PHC counter enable |
| `0x504` | `PTP_INCR` | nominal Q8.24-ns increment per tick |
| `0x508` | `PTP_ADJ` | signed Q8.24-ns adjfine addend added each tick |
| `0x510/0x514` | `PTP_TOD_WR_LO/HI` | settime target (ns) |
| `0x518/0x51C` | `PTP_OFFSET_LO/HI` | adjtime signed delta (ns) |
| `0x520` | `PTP_CMD` | W1S strobes: `[0]` load, `[1]` adjust, `[2]` snapshot |
| `0x530/0x534` | `PTP_TOD_RD_LO/HI` | latched TOD from the snapshot round trip |
| `0x540` | `PTP_INGRESS_LAT` | ingress latency correction, ns (fabric hook — unused today, section 2.4) |
| `0x544` | `PTP_EGRESS_LAT` | egress latency correction, ns (same status) |
| `0x624/0x628` | `ADP_GPTP_GM_LO/HI` | coherent fabric gptp_grandmaster_id; option OFF reads zero and ignores writes |
| `0x62C` | `ADP_GPTP_DOMAIN` | `[7:0]` gptp_domain_number |
| `0x6C8` | `PCMRX_TS` | avtp_timestamp of the last ring-accepted PDU |
| `0x6E4` | `A_GPTP_PDELAY` | selected owner's measured neighbor propagation delay, ns |
| `0x6EC` | `A_AVTPRX_TSD` | signed ts_delta at the last accepted AVTP PDU |
| `0x730/0x734` | `A_AS2_LO/HI` | coherent fabric parent identity; option OFF reads zero and ignores writes |
| `0x7DC/0x7E0` | `ASP_LO/HI` | retired staging slots; reads zero and writes are inert |
| `0x7E4` | `ASP_CMD` | RO live fabric `{generation,count}`; option OFF reads zero; writes are inert |
| `0x738` | `A_CRF_CTRL` | `[0]` CRF sink enable; RO `[31]` locked |
| `0x73C/0x740` | `A_CRF_SIDLO/HI` | CRF sink stream_id |
| `0x744` | `A_CRF_DELTA` | RO signed `crf_ts - ptp_now` (phase) |
| `0x748` | `A_CRF_RATE` | RO signed ns error per 512 ms window (frequency) |
| `0x74C` | `A_CRF_STATUS` | RO `{pdu16, fmt_err8, seq_err8}` |
| `0x750` | `A_CRFT_CTRL` | `[0]` CRF talker enable |
| `0x754/0x758` | `A_CRFT_SIDLO/HI` | CRF talker stream_id |
| `0x75C/0x760` | `A_CRFT_DMLO/HI` | CRF talker destination MAC |
| `0x764` | `A_CRFT_COUNT` | RO CRF PDUs emitted |
| `0x874` / `0x894` | `LTAP_TX_EPOCH` / `LTAP_RX_EPOCH` | gPTP ns latched at the latency-tap reference frames |
| `0x8F8` | `MCSRV_STAT` | servo state/flags + signed trim in 1/16 ppm (`[31:16]`) |
| `0x8FC` | `MCSRV_CTRL` | `[0]` ps_invert (bench sign knob); `[1]` auto_repair — 1 allows the DRP divider repair path, **reset 0** = verify-only. Both bits are in the map row |

## 4a. Centered-FIFO regulation goal (USER 2026-08-07): +/- 125 us

The standing regulation target for the DAC elasticity FIFO: **the fill
stays CENTERED, and its excursion around MID stays within one class-A
frame period - +/- 125 us = +/- 6 sample pairs at 48 kHz.** This is a
clock-regulation-quality goal, not a latency collapse: the FIFO keeps
its centered operating point (MID = 256 pairs), the 0x002A recenter
keeps snapping to MID, and the goal tightens the steady-state wander
band roughly tenfold versus today's convergence windows (enter
MID+/-64, exit +/-128 - i.e. +/-1.3 / 2.7 ms). Holding +/-6 pairs is
earned by clock QUALITY, not buffer depth: the media clocks on both
ends must be unified (the CRF followership chain, or the peer
following our clock), and once the wander genuinely sits inside the
band, the convergence observer's thresholds can be retightened to
match. The per-stage latency taps are the instrument that verifies the
excursion rather than assuming it. Tracked as task #28. (The PTO /
presentation-wait budget is a separate knob - see Section 3.6.)

## 4b. Grandmaster loss and recovery

The transient story - what happens when the GM disappears, changes or
returns, layer by layer with the 08-06/08-07 bench measurements - lives
in its own document: [`GM_LOSS_RECOVERY.md`](GM_LOSS_RECOVERY.md).
Headline: the product path now detects and publishes the transition entirely
in fabric and asserts `tu` on the commit edge. Option OFF is ownerless and
cannot create a clock-valid claim.

## 5. Status (updated 2026-09-02)

Proven, with the evidence next to each claim:

* **PHC + clock ops**: RTL-proven against a 128-bit accumulator model
  (201 k checks) — [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md)
  rows AS-1/AS-2.
* **Per-frame HW timestamps under interference**: RTL interference suite
  green ([`tb/verilator/ptp_ts`](../../tb/verilator/ptp_ts), event frames inside line-rate floods) and
  silicon green 2026-07-13 (hwts5): 0 tx-timestamp timeouts steady-state,
  offset rms 2-5 ns *through* RX/TX/bidirectional floods, **peer delay
  600 us (SW stamps) -> 1.3 us (HW)** —
  the retired timestamp-metadata finding (#259, in git history)
  "Validation status".
* **asCapable + full sync through the reference AVB switch**: pdelay
  handshake both ways, board-as-GM relayed to a hardware-timestamped slave
  at rms 2-4 ns (2026-07-13) —
  the retired RX-pad root-cause finding (#259, in git history).
  Both boards have since run hardware timestamps with zero config overrides
  (row AS-7).
* **CRF end to end**: sink lock on a bound stream proven on silicon (mf40);
  board-to-board CRF locked at **rate +6.7 ppm** (2026-07-21; the retired
  bench report remains in Git history).
* **Media-clock servo silicon-proven**: coherent chain measured **-83.9 dB
  loop THD+N = the converter floor** (2026-07-23) —
  [current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md);
  [historical Milan traceability](../history/v1/traceability/milan-v12.md) row M-DEV-15.
* **Clock-source selection consumed (#74)**: the stored `SET_CLOCK_SOURCE`
  index resolves in `milan_datapath`'s `media_clk_resolve` block and gates the
  servo, the grid aligner and the `mr` machinery (section 3.4/3.5.1). Proven
  at RTL: [`tb/verilator/media_grid_align`](../../tb/verilator/media_grid_align)
  (25 checks, closed-loop over the real NCO at the true 391/1591 ratio), the
  `milan_dp` `obj_aclk` two-phase leg (INTERNAL −10.64 ppm measured; CRF
  selected |ppm| < 0.5 with zero junction slips, the servo reaching ACQUIRE
  through the live select, both 4.4.4.3 `mr` triggers and the 10.4.3
  negative), the `sim_nxn` `[CRF-SEL]` AECP-command round trip, and the
  `chmap_capture` `[T0]` junction-detector arm.

Partial or missing, each with its row id:

* **AS-4 — MISSING**: latency constants are bench-calibrated (3511/1490 ns);
  no per-unit calibration procedure exists and the ingress/egress split was
  never measured separately —
  [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md) row AS-4,
  [current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md). Any
  new PHY/board is wrong by an unknown amount — silently degrading, not
  failing.
* **AS-6 — partial**: the DUT-wins-BMCA recreation is blocked on the bench:
  the reference AVB switch claims priority1 246 / clockClass 248 /
  clockAccuracy 0x20 and outranks every Milan-legal end-station value. The
  shipping priority1 must be 246; the bench 100 override is bench-only —
  row AS-6; [current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md);
  [historical Milan traceability](../history/v1/traceability/milan-v12.md)
  row M-DEV-1.
* **M-DEV-2/3/4 — partial**: the fabric plane has hard
  malformed/stale/foreign-domain pairing,
  multiple-responder and asCapable recovery assertions, but #117 still owns
  its wire evidence - [historical Milan traceability](../history/v1/traceability/milan-v12.md)
  section 1 and [802.1AS traceability](../traceability/ieee8021as.md) AS-8.
* **M-CLK-2 — MISSING**: the CRF stream rides untagged best-effort (an
  SR-tagged unregistered stream would be pruned to zero ports); it needs the
  second lwSRP listener/talker attribute — row M-CLK-2;
  [current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md).
* **M-CLK-3 — CLOSED**: the clock-recovery actuator is built and
  silicon-proven (servo LOCKED, coherent chain −83.9 dB), and the matrix row
  now reads ✅ rather than carrying both "actuator MISSING" and "now BUILT" at
  once - [historical Milan traceability](../history/v1/traceability/milan-v12.md)
  row M-CLK-3. What survives is the two bench-gated knobs in the "Servo
  residuals" bullet below, not a missing function.
* **M-CLK-5 — MISSING**: Milan 7.6 media-clock reference election /
  domain propagation logic on top of the (implemented) command layer —
  row M-CLK-5.
* **AS-10 -- models present, bench replay open**: tsn-gen carries the 802.1AS
  frame models at the CI pin and `tb/verilator/tsn_fuzz/fuzz_ptp.py` grades
  the fabric plane's own Announce/Sync/Follow_Up/Pdelay against them (the
  #123 campaign); replaying the blocked AS-6 BMCA variant on the bench with
  packet_gen as the claimant instead of the switch is still to be wired up --
  [`../traceability/ieee8021as.md`](../traceability/ieee8021as.md).
* **Servo residuals**: `auto_repair` stays 0 until the one-shot ClkReg
  readback is blessed on the bench, and the winning `ps_invert` polarity is
  still a CSR knob rather than the RTL default —
  [current Milan audit](../testing/MILAN_V12_AUDIT_2026-08-16.md).
* **#74 bench probe — OPEN**: the silicon acceptance of the aligned grids is
  still to be taken on the AX7101 — J11.8 (`tdm_fsync_o`) against J11.9
  (`media_lrclk_o`) under a live CRF selection (section 3.5.1). The RTL
  closed-loop evidence above does not stand in for it.
* **Unconsumed map rows**: `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` exist in
  [`../reference/REGISTER_MAP.md`](../reference/REGISTER_MAP.md) but their
  fabric wires are unconsumed (section 2.4) — writing them changes nothing on
  the wire today.
  *(The doc-drift bullet that used to sit here — 0x6E4/0x6EC/0x730-0x764 and
  `MCSRV_CTRL[1]` live in `milan_csr.sv` but absent from the map — is CLOSED:
  all of those rows are in the map now, and section 4's `(*)` marker is
  retired with it.)*
