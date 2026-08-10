# Media clock lock: the periodic one sample slip (2026-08-10)

**Status: root caused, fix NOT landed. This is an architecture gap, not a
datapath defect. Do not "fix" the AAF path for it.**

A listener receiving our AAF stream drops or inserts exactly one sample
about every 1.96 seconds, forever. Measured at VERSION 0x0040. The
audible result is a tone that is essentially perfect for two seconds,
then briefly wrong, on repeat.

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
