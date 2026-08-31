[OBSOLETE + 2026-08-18]

> Status: Historical
>
> Original path: `docs/findings/MEDIA_CLOCK_LOCK_0810.md`
>
> Archived: 2026-08-31
>
> Relocated: 2026-08-31
>
> Current successor: [open current documentation](../../../design/TIME_SYNC.md)

# Media clock lock: the periodic one sample slip (2026-08-10)

> **UPDATE 2026-08-10 (later the same day). Two things below are wrong, and
> the actuator half of the fix has landed at VERSION 0x0041. Read
> [The correction](#the-correction-2026-08-10-pm) before acting on anything
> in this document.**

**Status: root caused, fix NOT landed. This is an architecture gap, not a
datapath defect. Do not "fix" the AAF path for it.**

A listener receiving our AAF stream drops or inserts exactly one sample
about every 1.96 seconds, forever. Measured at VERSION 0x0040. The
audible result is a tone that is essentially perfect for two seconds,
then briefly wrong, on repeat.

## Contents

- **[The measurement](#the-measurement)** — The numbers the whole page hangs on: 44.56 s of pilot tone through the peer, median residual **-133.85 dB**, and one 50 ms window in every 1.95 s degrading by about 110 dB. The autocorrelation peak at lag 1.950 s (r = 0.755, against about -0.03 at neighbouring lags) is what makes it a period rather than an anecdote; zero-crossing timing on earlier captures agrees at 1.957-1.962 s.
- **[Each event is exactly one 48 kHz sample](#each-event-is-exactly-one-48-khz-sample)** — The step that pins the domain. Slaving the capture interface to a 44.1 kHz source made the same events measure 0.918-0.923 samples, and 44100/48000 = 0.91875 — so the event is exactly one 48 kHz sample, which is 10.65 ppm at a 1.957 s period.
- **[What was ruled out, with evidence](#what-was-ruled-out-with-evidence)** — Six candidates eliminated, each with its evidence rather than an opinion: the capture interface (survives a clock-source change), the bitstream (two builds, same period), our media-tick arithmetic (the Bresenham divider's residual error is zero, not merely small), timestamp-versus-sample incoherence (gPTP and the media tick share one oscillator), wire sample alignment (golden byte compare), and tone level (a runtime attenuation field, not a design constant).
- **[Root cause](#root-cause)** — As concluded that morning: two free-running oscillators 10.65 ppm apart with nothing locking them, so the listener absorbs the difference by slipping one sample every 1.96 s. **Read the correction section below before acting on this** — the afternoon's forensics moved the slip to the loopback queue.
- **[Why a better oscillator is NOT the fix](#why-a-better-oscillator-is-not-the-fix)** — Slip interval is 1/(48000 x delta), so better parts only buy time and one slip is still one click: 20 ppm crystals click every 0.5 s, 1 ppm TCXOs every 10 s, rubidium at both ends every ~24 days. The one case where an external oscillator works is when it is the *same* oscillator feeding both devices — a house word clock, which is precisely what AVB exists to replace.
- **[The fix: one media clock, distributed](#the-fix-one-media-clock-distributed)** — Three routes, cheapest first: the listener recovers media clock from our stream (costs us nothing, the immediate bench fix), CRF as a dedicated clock-reference stream, or both ends deriving 48 kHz from the already network-locked gPTP. Note since 2026-08-13 route 2 needs `SET_CLOCK_SOURCE`, which no longer exists on this build.
- **[The gap on our side](#the-gap-on-our-side)** — Why this device cannot be a media clock *sink*: `media_tick_p` is exact but **structurally unsteerable** (compile-time localparams, no adjust port), the MMCM DRP servo steers the I2S front-end clock and not the AAF/crossbar grid, and `I2SPB_TRIM`'s ~15.3 ppm LSB is too coarse. Proposes making the Bresenham remainder a register — one LSB is 0.01 ppm, a register and an adder, no MMCM involved.
- **[The correction (2026-08-10 pm)](#the-correction-2026-08-10-pm)** — The afternoon's forensics that retract two claims above: the bench was on the **loopback lane**, not a physical front end (the TDM front end cannot appear in the map at all), so the slip is `KL_chan_map_capture`'s LOOP elastic queue rather than two crystals. Includes what landed at `0x0041` and what is still open — chiefly that the loop-queue slip counters exist in fabric but reach no CSR, so software cannot see an event the hardware has been counting all along.
- **[Reproducing the measurement](#reproducing-the-measurement)** — The method, and it depends on one property: the pilot tone is bit-exactly periodic over 48 samples when the path is 48 kHz and bit-transparent, which makes sample-exact forensics possible. Build a template from a window of nine agreeing periods, track phase, cross-check with zero-crossing timing. Two traps that produced wrong answers first: integrating a demodulated phase derivative smears one event across the filter window, and a template taken from a dirty region silently defeats the analysis.
- **[Caution when raising the tone to 0 dBFS](#caution-when-raising-the-tone-to-0-dbfs)** — A 0 dBFS sampled sine overshoots between samples — measured +0.91 dB through a 48 kHz to 44.1 kHz conversion — and the resulting clipping lands directly in the residual metric used above, looking like a quality fault that is not one. At 48 kHz end to end the maxima land on table entries, so 0 dBFS is safe; otherwise attenuate with `TONE_CTRL[3:1]` first.

## The measurement

Capture of the pilot tone through the peer device, 48 kHz, 44.56 seconds,
two channels. Per 50 ms window, residual against a best fit 1 kHz sine:

| quantity | value |
|---|---|
| median residual between events | **-133.85 dB** |
| worst window | -23 dB |
| quality autocorrelation peak | **lag 1.950 s, r = 0.755** |
| r at 2.000 s | +0.168 |
| r at 1.0 / 1.5 / 2.5 / 4.0 s | about -0.03 |
| bad windows | 23 in 44.56 s, median spacing 1.950 s |

Both channels are identical in every metric. So the tone is essentially
perfect for 1.95 seconds, then one 50 ms window degrades by about 110 dB.

Independent confirmation by zero crossing interval timing on the same and
earlier captures gave a period of 1.957 to 1.962 seconds.

## Each event is exactly one 48 kHz sample

This is the step that pins the domain. With the capture interface slaved
to the incoming digital audio its sample rate followed the source to
44.1 kHz, and the same events then measured **0.918 to 0.923 samples**.
One 48 kHz sample seen on a 44.1 kHz grid is 44100/48000 = **0.91875**.

One sample per 1.957 seconds is **10.65 ppm**.

## What was ruled out, with evidence

- **Not the capture interface.** The slip survived changing its clock
  source from free running to slaved, with the period unchanged.
- **Not the gateware build.** The same period appears in captures from
  2026-08-08 (previous bitstream) and 2026-08-10 (VERSION 0x0040).
- **Not our media tick arithmetic.** `milan_datapath.sv` derives
  `media_tick_p` with a Bresenham fractional N divider
  (`MEDIA_TICK_REM_C = MILAN_CLK_FREQ_HZ % 48000`). At 100 MHz the period
  alternates 2083, 2083, 2084, which is 6250 clocks per 3 samples, i.e.
  62.5 us exactly. The residual error is zero, not merely small. The
  older integer floor bug (flat 2083, +160 ppm, avtp_timestamp deltas of
  124,980 ns) is fixed and stayed fixed.
- **Not a timestamp versus sample incoherence on our side.** gPTP and the
  media tick share the same 100 MHz oscillator (`PTP_INCR` reads
  0x0A000000, i.e. 10 ns), so our AVTP timestamps and our samples cannot
  drift apart. A listener that recovers media clock from our stream
  tracks us exactly.
- **Not the sample alignment on the wire.** The packetizer places a
  24 bit sample MSB aligned in the INT_32BIT field by byte position
  (bytes 0 to 2 carry the sample, byte 3 is `8'h00`), which is
  `sample << 8` in network byte order per IEEE 1722-2016 clause 7.3.4.
  Guarded by the golden byte compare in `tb/verilator/aaf/sim_main_nx.cpp`.
- **Not the tone level.** The quarter scale seen in captures was the
  runtime attenuation field `TONE_CTRL[3:1]`, not a design constant. The
  sine table is full scale.

## Root cause

Two free running oscillators, 10.65 ppm apart, with nothing locking them.
Our media clock is exact relative to the board oscillator; the peer's is
exact relative to its own. Neither is disciplined to a shared reference,
so the listener must absorb the difference, and it does so by slipping
one sample every 1.96 seconds.

## Why a better oscillator is NOT the fix

Slip interval = 1 / (48000 x delta). Two independent clocks always drift,
so this is asymptotic and never reaches zero:

| clocks | delta | one click every |
|---|---|---|
| two ordinary 20 ppm crystals | 40 ppm | 0.5 s |
| **measured today** | **10.65 ppm** | **1.96 s** |
| two 1 ppm TCXOs | 2 ppm | 10 s |
| two 0.1 ppm OCXOs | 0.2 ppm | 104 s |
| rubidium both ends | 0.00001 ppm | about 24 days |

Better parts only buy time, and one slip is one click. The single case
where an external oscillator does work is when it is the SAME oscillator
feeding both devices, i.e. a house word clock. That is exactly what AVB
exists to replace: it needs a second cable to every device and does not
survive a network.

## The fix: one media clock, distributed

Cheapest first.

1. **Listener recovers media clock from the stream.** The receiving
   device sets its CLOCK_SOURCE to the input stream and follows our AVTP
   timestamps. Costs us nothing and is the immediate bench fix.
2. **CRF.** A dedicated clock reference stream, one media clock master,
   everyone else locks. We already advertise MEDIA_CLOCK_SOURCE and SINK
   (capabilities 0x4801) and ship `KL_crf_rx` plus the MMCM DRP servo.
   The remaining work is the CRF sink bind chain.
3. **Both ends derive the audio clock from gPTP.** gPTP is already locked
   network wide, so generating 48 kHz from gPTP time instead of a raw
   crystal makes every device agree by construction with no extra stream.

## The gap on our side

To be a media clock **sink** we must be steerable, and today the packet
grid is not:

- `media_tick_p` is exact but **structurally unsteerable**.
  `MEDIA_TICK_DIV_C` and `MEDIA_TICK_REM_C` are compile time localparams
  derived from `MILAN_CLK_FREQ_HZ`; there is no adjust port.
- The MMCM DRP servo steers `clk_audio`, the I2S front end clock, NOT the
  AAF and crossbar grid. So we have a steerable clock and an unsteerable
  grid, and they are different clocks.
- `I2SPB_TRIM` (0x6E0) does carry a signed NCO trim, but it steers the
  playback FIFO drain for the listener direction and its LSB is about
  15.3 ppm, which is coarse for this purpose.

**Proposed fix, small and in the existing structure:** make the Bresenham
remainder a register instead of a localparam and let the servo drive it.
That turns the fixed divider into an NCO. Resolution is excellent:

```
d(clocks per sample)/d(REM) = 1/48000            = 2.08e-5
relative                    = 2.08e-5 / 2083.333 = 1.0e-8 = 0.01 ppm per LSB
```

One LSB is 0.01 ppm. Correcting the measured 10.65 ppm needs a remainder
delta of about 1065 against a range of 0 to 47999 that currently sits at
16000, so it fits comfortably and is roughly a thousand times finer than
required. It costs a register and an adder, needs no MMCM or DRP, and
glitches nothing because it only biases which cycles get the extra clock.

The MMCM DRP servo is still required for the physical I2S and converter
clock, since a converter needs a real clock rather than a tick. Both
mechanisms are driven from one error signal, and per the ONE-GRID rule
already documented in `milan_datapath.sv` they must be steered together
or they will fight.

## The correction (2026-08-10 pm)

Two claims above do not survive.

**1. "Two free running oscillators" is not established, and the bench was on
the loopback lane.** The channels under test were mapped to the loopback
cluster (SRC=5), not to a physical front end — confirmed in the RTL, where
`AEM_ODMAP_CSRC_C` carries only src=3 (host ring), src=4 (tone) and src=5
(loop), and `milan_datapath.sv` ties `.tdm_pair_valid_i (1'b0)`. The TDM
front end cannot appear in the map at all.

That puts the slip in a place the document never considered.
`KL_chan_map_capture`'s LOOP bucket is the only source with an elastic queue,
and its own banner states the failure mode exactly:

> SLIP, HONEST AND BOUNDED: queue empty at a tick (upstream slower) = the hold
> repeats the last event, ONE dup, counted on `lb_dup_cnt_o`. Queue full at a
> push (upstream faster) = the OLDEST event is dropped, ONE skip, counted on
> `lb_skip_cnt_o`. **With locked clocks both stay at ZERO.**

Push rate is the upstream talker's media clock. Pop rate was `media_tick_p`,
our own crystal, unsteerable. One dup or one skip per beat period is the
designed behaviour of a listener that does not recover — not a datapath
defect and not two crystals meeting on a wire.

Two consequences worth keeping:

- `LB_QDEPTH_C` is jitter margin, **not** rate margin. At 10.6 ppm the
  occupancy walks to an end in 1.96 s at any depth.
- A loop-queue dup is a **content** defect. The stream rate stays
  48,000.000 Hz, `avtp_timestamp` deltas stay flat at 125,000 ns, and one
  sample *value* repeats. No timestamp or PDU-cadence analysis can see it,
  which is why the forensics found a flat packet-phase profile and concluded
  the grid was healthy. It was.

**2. "Our timestamps and our samples cannot drift apart" is false.** They
share a net, not a rate. The PHC adds `PTP_INCR + PTP_ADJ` per tick and the servo
writes `PTP_ADJ` (0x508) continuously to discipline us to the grandmaster,
while `media_tick_p` counted raw `axis_clk` and ignored it. Our grid-vs-GM
error is `PTP_ADJ / 0x0A000000 x 1e6` ppm — one register read, and about 1787
would mean 10.65 ppm.

**A near miss worth recording so it is not re-derived.** `clk_audio` really is
`-10.639 ppm` by construction (`milan_soc.py:356,363` PLAN A, and `:5012`
forces the shipping TDM8 shape onto PLAN A), and `clk_audio/512` slips against
an exact 48 kHz grid every 1.9582 s. That matches the measurement to four
figures and is a **coincidence**: `clk_audio` is not in the talker path on
this shape. It does cause a real latent bug elsewhere — `KL_crf_tx` runs on
`clk_audio/512` while declaring `base_frequency` 48000, so our CRF output
advertises a media clock master 10.639 ppm slow.

### What landed at 0x0041

The actuator half, as proposed below, with one correction to the proposal.

- `hdl/ieee1722/crf/KL_media_nco.sv` replaces the inline divider. Same
  Bresenham, plus a signed runtime trim at `1/CLK_FREQ_HZ` relative per LSB
  (0.01 ppm at 100 MHz), clamp **derived** from the shape rather than
  mirrored, elaboration guards that refuse a trim needing a two-step
  accumulator correction.
- `KL_pcm_tx` joins that grid on its `USE_EXT_TICK_P` port — the hook its own
  banner reserved for "the recovered media clock", tied off since it was
  written. The host playback ring and the capture crossbar are now the same
  strobe, not two dividers that agree.
- Both actuators take **one** command: the servo's u (±200 ppm, published in
  1/16 ppm units on `A_MCSRV_STAT[31:16]`) drives the MMCM for `clk_audio` and
  the NCO for the packet grid, negated because the servo's `u > 0` means speed
  up while the NCO's `trim > 0` lengthens the period.
- `clock_source = INTERNAL` forces the trim to zero, and the grid is then
  bit-for-bit the 0x0040 divider. `tb/verilator/media_nco` (214 checks) pins
  that tick-for-tick.

**The correction to the proposal below:** a steerable remainder is a
*frequency* trim, and frequency-locking lengthens the interval between clicks
without removing them. Phase-locking removes them. The grid should ultimately
be a phase accumulator referenced to `ptp_now_w`: one sample is exactly 62,500
thirds of a nanosecond, a gPTP second holds a whole number of them, so the
grid becomes second-aligned and identical on every device that runs it. That
is cheap here because `ptp_ts_top` clocks on `gtx_clk` = `cd_milan` =
`axis_clk`, so `ptp_now_w` is available with no CDC. Keep the trim register
for holdover.

### Still open

- The loop-queue slip counters `lb_dup_cnt_o` / `lb_skip_cnt_o` reach
  `milan_datapath.sv` as a `verilator public_flat_rd` tap and **nowhere else**.
  They are not readable on silicon. The fabric has been counting this exact
  event all along and software cannot see it.
- Nothing yet drives the trim from a recovered reference: the servo only
  engages at `clock_source == 2`, and `SET_CLOCK_SOURCE` still rejects any
  index ≥ 3.
- Whether the two actuators agree in silicon is a bench measurement, not a
  simulation one.

## Reproducing the measurement

The pilot tone is bit exactly periodic over 48 samples when the whole
path is 48 kHz and bit transparent (measured `x[n+48] - x[n]` rms
7.4e-09, which is float32 epsilon at that amplitude). That makes
sample exact forensics possible: build a template from a window where
nine consecutive periods agree, then track the phase and report any
mismatch. Cross check with zero crossing interval timing, which needs no
smoothing.

Two traps that produced wrong answers before the cross check caught them:

- Integrating the derivative of a quadrature demodulated phase smears one
  event across the filter window and double counts it.
- A template window taken from a dirty region silently defeats the whole
  analysis. Pick the window by testing for bit exact periodicity.

## Caution when raising the tone to 0 dBFS

A 0 dBFS sampled sine overshoots between samples. The capture that had a
48 kHz to 44.1 kHz conversion in it peaked at 0.277992 against a 0.25
amplitude, which is +0.91 dB, and at 0 dBFS that would have clipped.
Clipping would land directly in the residual metric used above and look
like a quality fault that is not one. With the path at 48 kHz end to end
the 1 kHz tone is exactly 48 samples, the maxima land on table entries
and there is no overshoot, so 0 dBFS is safe. Reduce with
`TONE_CTRL[3:1]` before measuring through any rate conversion.
