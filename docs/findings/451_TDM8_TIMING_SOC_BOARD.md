<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# TDM8 link timing at the SoC board on the ec0cc0c1 image

Refs #451. Operator [A468], 2026-10-01, under the
[bench lane B4 assignment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5924192573).

The last open #451 recipe item reads "Scope BCLK, FSYNC and DOUT at the AM62x
end: 12.288 MHz, a one-BCLK FSYNC pulse at 48 kHz, data starting one BCLK
after it". By owner decision it is measured on the SoC board itself, from the
McASP0 receiver. [#626](https://github.com/kebag-logic/milan-fpga/issues/626)
holds the oscilloscope version.

The first session stopped at the SoC board's console login. The owner then
logged the console in, and the second session ran the timing steps. One McASP0
capture recorded the DUT's DOUT pattern and timed its frames on the SoC board's
own clock. After 475.6 s of a planned 630 s, the bench host lost the SoC
board's USB function. The rules make that a STOP, so the capture of at least
10 minutes is not met. Everything up to the loss was measured and is reported
below.

| #451 timing item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `ec0cc0c1` | PASS | See [Identity and setup](#identity-and-setup) |
| Framing: McASP0 receive configuration and capture parameters | Recorded | `dsp_a`, codec side bit-clock and frame master, eight 32-bit slots, 48 kHz. See [Framing](#framing) |
| Data one BCLK after the frame-sync edge: bit-exact decode in all eight slots, in order | PASS, as far as the SoC board shows | 22,831,104 frames: 0 torn, 0 invalid and 0 zero words. See [Pattern check](#pattern-check) |
| FSYNC at 48 kHz: fs against the SoC board's monotonic clock | 47,997.947 Hz: 48 kHz within the SoC board's clock accuracy | -42.8 ppm against 48 kHz, +-0.12 ppm timing granularity. See [Frequencies](#frequencies) |
| BCLK at 12.288 MHz | 12,287,474 Hz, inferred as 256 x fs | The receiver fixes 256 bit clocks per frame only as a minimum. See [Frequencies](#frequencies) |
| One capture of at least 10 minutes, pattern-checked whole | NOT MET: 475.6 s, then STOP | The bench host lost the USB function. See [Why the run stopped](#why-the-run-stopped) |
| FSYNC pulse width, edge timing, levels and absolute ppm | Not shown by the SoC board | [#626](https://github.com/kebag-logic/milan-fpga/issues/626). See [What the SoC board can and cannot show](#what-the-soc-board-can-and-cannot-show) |

These are operator observations, not review verdicts.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image's identity readback and the bench as found in both sessions.
- **[Method](#method)** -- The DOUT method of the #617 bench page, with the capture streamed off the SoC board and its PCM status sampled.
- **[Framing](#framing)** -- The SoC board's DAI format and clock roles, and the capture's PCM parameters.
- **[Pattern check](#pattern-check)** -- The whole received capture decoded: slots, channels and frame continuity.
- **[Frequencies](#frequencies)** -- fs against the SoC board's monotonic clock, its uncertainty, and BCLK.
- **[Why the run stopped](#why-the-run-stopped)** -- The USB function loss at 475.6 s and what it ended.
- **[What the SoC board can and cannot show](#what-the-soc-board-can-and-cannot-show)** -- What the McASP0 measurement establishes for each part of the item, and what stays with #626.
- **[Bench as left](#bench-as-left)** -- DUT, controller and SoC board state at the end, against the start, and the residuals.
- **[Rerun](#rerun)** -- What the rerun needs, and what this run teaches about it.
- **[Artifact hashes](#artifact-hashes)** -- The raw capture and the lane packet's evidence files.

## Identity and setup

The DUT runs the image of dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`,
installed on 2026-09-30. The first session's gate repeats the
[#617 bench page](617_DIN_FRAME_COHERENCE_BENCH.md#identity-and-setup)'s
readback, and every value equals that page's.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Live ENTITY and CONFIGURATION | Byte-equal to the AEM bytes the console dumps from QSPI (312 and 106 bytes); entity `020000fffe000001` |
| UART grader | 10 of 10 |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d178f19a` |
| Identity gate | PASS |

This is CRC consistency and descriptor identity, not a configuration SHA-256
readback. The second session ran on the same DUT boot. Its start reads equal
the first session's end in `VERSION`, `PP_STAT` and every control word, and
only live counters moved. Its census equals the first session's end in 32 of
33 entries; the other is the live propagation delay.

As found at the second session's start:

- **DUT.** NVM `backed=1`, `dirty=0`, `stale=0`, `pend=0`, 0 commits, slot B
  seq 236 authoritative. `PP_STAT` read `5b000444`. All 18 queried stream
  states were unbound, and both DUT audio maps were empty. The DUT selected
  clock source 0 at 48 kHz, with SYNC=1, ASCAPABLE=1 and TU=0.
- **SoC board.** It had rebooted since lane B3: uptime 67,602 s at
  04:09:49Z. Both bridge legs ran with the recorded command lines. McASP0
  capture was running and McASP0 playback stood in XRUN, as no host played
  audio. The USB function was configured, the fault scan was empty, and taint read
  0.
- **Controller host.** No gPTP daemon ran. The NIC clock read 0 ppb, and
  hardware timestamping was off.

## Method

Every bench action held the shared lock. No flash, reset, power, wiring,
instrument or USB function action occurred. On the SoC board, everything but
the capture, the bridge legs and one 33-byte TCP test to the bench host was a
read of the SoC board's status files, hardware description or system log.

The two SoC bridge legs were stopped by PID, after checking each command line
against the bridge script's `status`. They were restarted after the run with
the script's own command lines.

The DOUT method is the
[#617 bench page's](617_DIN_FRAME_COHERENCE_BENCH.md#method). A software AAF
talker on the controller host sent the first-light pattern, paced on the
gPTP-disciplined NIC clock. DUT STREAM_INPUT 0 was bound to it, and eight
identity mappings put stream channel `c` on cluster `c`. For tag `t` (1 to 8)
and frame ordinal `n`, bits 31:8 of each word carry `(t << 16) | (n & 0xffff)`.
Bits 7:0 are zero. Channel `c` carries tag `c + 1`.

Two things differ from that page:

- **The capture streams off the SoC board.** One direct McASP0 capture,
  `hw:0,0`, was set to record 630 s. The recording, 921.6 MB at full length, exceeds the
  SoC board's temporary storage, and the SoC board has no `nc`. So the recorder
  wrote to a TCP connection through the shell's `/dev/tcp`, over the USB
  network link, to a receiver on the bench host. The receiver hashed the bytes
  as they arrived.
- **The capture's PCM status was sampled.** While the recorder ran, the McASP0
  capture substream's `hw_params` and `sw_params` were read once, and its
  `status` every 5 s. With `tstamp_mode` ENABLE and `tstamp_type` MONOTONIC,
  `status` gives `hw_ptr`, the frames received since the trigger, and
  `tstamp`, the CLOCK_MONOTONIC time at which the audio driver last moved it.

## Framing

The SoC board's hardware description, as its running system reports it:

| Node | Property | Value |
|---|---|---|
| `sound-tdm8` | `compatible` | `simple-audio-card` |
| `sound-tdm8` | `simple-audio-card,format` | `dsp_a` |
| `sound-tdm8` | `bitclock-master`, `frame-master` | The codec DAI, `tdm8-codec`, the DUT side. McASP0 is the clock consumer |
| `sound-tdm8` | Codec and CPU DAI slots | `dai-tdm-slot-num` 8, `dai-tdm-slot-width` 32, on both |
| `sound-tdm8` | Clock or frame inversion | None set |
| McASP0, `audio-controller@2b00000` | `compatible`, `op-mode` | `ti,am33xx-mcasp-audio`, 0 (I2S and TDM) |
| McASP0 | `tdm-slots`, `serial-dir` | 8; AXR0 transmits, AXR1 receives |
| McASP0 | `rx-num-evt`, `tx-num-evt` | 32 words each |
| McASP1, McASP2 | `status` | `disabled` |

The capture's PCM parameters, read while it ran:

| Parameter | Value |
|---|---|
| PCM | `davinci-mcasp.0-kl-tdm8-hifi`, card 0 device 0, capture |
| Access, format, msbits | `RW_INTERLEAVED`, `S32_LE`, 32 |
| Channels, rate | 8, 48000 (48000/1) |
| Period, buffer | 2,048 and 16,384 frames |
| Timestamps | `tstamp_mode` ENABLE, `tstamp_type` MONOTONIC |

In `dsp_a` the McASP receiver takes the first data bit one bit clock after
the frame-sync edge, then eight 32-bit slots. The pattern makes that
checkable. One bit early, every word's tag field doubles, so channel 0 reads
tag 2 or 3 and channels 4 to 7 read tags above 8. One bit late, bit 0 of the
ordinal lands in bits 7:0, so every odd frame's words go invalid. A slot
rotation moves a tag to another channel. The capture shows none of these.

## Pattern check

The decode covers every byte received: the first 475.648 s of the capture.

<!-- timing-run -->
| Run | Frames | Seconds | Torn | Invalid words | Zero words | Slot order | Result |
|---|---|---|---|---|---|---|---|
| `timing-long` | 22,831,104 | 475.648 | 0 | 0 | 0 | Identity | PASS |

<!-- timing-channels -->
| SoC capture channel | TDM slot | Recovered tag | Valid words | Result |
|---|---|---|---|---|
| 0 | 0 | 1 | 22,831,104 | In order |
| 1 | 1 | 2 | 22,831,104 | In order |
| 2 | 2 | 3 | 22,831,104 | In order |
| 3 | 3 | 4 | 22,831,104 | In order |
| 4 | 4 | 5 | 22,831,104 | In order |
| 5 | 5 | 6 | 22,831,104 | In order |
| 6 | 6 | 7 | 22,831,104 | In order |
| 7 | 7 | 8 | 22,831,104 | In order |

A torn frame is the #617 page's: one whose words carry more than one ordinal.
No frame here is torn. Every discontinuity is a whole-frame repeat or a forward
jump, and no frame is silent. The capture itself lost nothing before the
stall: all 95 running samples share one trigger, and the buffer never held
more than 2,048 of its 16,384 frames.

| Ordinal step between frames | Count |
|---|---|
| +1 | 22,768,722 |
| 0, a repeat | 51,873 |
| +2, one frame skipped | 4,954 |
| Forward by more than 2 | 5,554 |
| Backward | 0 |

Discontinuities closer than 50 ms were grouped into 1,221 clusters, with the
#617 page's attribution:

- **189 beat clusters** repeat and skip whole frames: 3,678 repeats and 3,867
  skips. This is the INTERNAL-source beat that page describes.
- **16 underrun clusters** start within 60 ms after a talker PDU sent 150 us
  or more late.
- **1,016 clusters match neither.** They repeat a median of 18 frames, and
  816 of them then jump forward by 5, 5 and 8 to 12. 838 of them start 22,000
  to 26,000 frames after the previous one, about every 0.5 s.

The talker sent 8,330 PDUs 1 ms or more late, and the latest was 31.8 ms. Its
late-PDU list holds at most 5,000 entries and was full at 292 s, so later
clusters could not match a logged lateness. The #617 page's 70 s run had 59
clusters. This page draws no conclusion on the unmatched clusters. They are
whole frames of the rendered stream, so they do not bear on the link's
framing.

## Frequencies

fs is the frames the receiver wrote between two status samples, over the
SoC board's CLOCK_MONOTONIC time between them.

<!-- timing-fs -->
| Run | Samples | Window | Frames in window | fs, first to last sample | fs, least-squares | Against 48 kHz | Against the plan's 47,999.489 Hz | BCLK = 256 x fs |
|---|---|---|---|---|---|---|---|---|
| `timing-long` | 95, 5 s apart | 472.468 s | 22,677,480 | 47,997.947 Hz | 47,997.946 Hz | -42.8 ppm | -32.1 ppm | 12,287,474 Hz |

The timing granularity bounds the figure:

- `hw_ptr` moves in steps of 4 frames, the 32-word receive threshold.
- Against the least-squares line the samples scatter by 25.7 us rms and 52.9
  us at most. That is the pointer step plus the latency from the pointer moving
  to its timestamp.
- The first and last samples' residuals give +-0.006 Hz, +-0.12 ppm. A whole
  step at each end gives +-0.017 Hz, +-0.35 ppm.
- The SoC board's uptime, read at 10 ms resolution with each sample, gives
  47,997.71 Hz, inside its own +-42 ppm.

The SoC board's clock is not calibrated. Its clocksource is the 200 MHz
architected timer, from the board's crystal. #626 puts the crystal at tens of
ppm, and its tolerance is not included above. The system clock was never set.
The board's clock-synchronization service only logged that it was waiting for
a gPTP daemon, and none ran. So nothing steered CLOCK_MONOTONIC during the
capture.

The -32.1 ppm against the plan's
[divider figure](../litex/CLOCK_DOMAINS.md#audio-variants) is the sum of both
boards' clock errors. This lane has no reference that splits it. A wrong
divider, slot count or rate family would sit hundreds of ppm or more away.

BCLK is not measured. The receiver needs at least eight 32-bit slots after
each frame-sync edge, and it does not count bit clocks after the eighth slot.
So 256 x fs assumes the master's frame has no idle bit clocks, as the
[TDM8 geometry](../litex/CLOCK_DOMAINS.md#audio-variants) specifies.

The DUT's own counter agrees with the plan. `SLIP_TDM` rose by 395
duplicates in 774.3 s across the run, 0.510 per second. That is 10.63 ppm
between FSYNC and the DUT's media grid. It is the DUT comparing its own two
clocks, not a SoC board measurement.

## Why the run stopped

The events, in order, on the bench host's clock:

| Time | Event |
|---|---|
| 04:17:05.207Z | First capture bytes arrive; the McASP0 trigger is at 68,038.252 s of the SoC board's uptime |
| 04:25:00.820Z | Last capture bytes arrive |
| About 04:25:00.93Z | The SoC board logs "remote wakeup not configured", at 68,513.970 s of its uptime, 475.7 s after the trigger. The time is mapped through the trigger |
| 04:25:01.084Z | The bench host's USB host controller logs "Set TR Deq Ptr cmd failed due to incorrect slot or ep state" |
| 04:25:01.085Z | The SoC board's USB device disconnects from the bench host |

The SoC board's log holds the same "remote wakeup" line at 667 s and 26,028 s
of its uptime. With the stream stopped, the recorder blocked writing to it, and
McASP0 capture overran 0.42 s after that line. It stayed in XRUN. The USB Audio card and the USB network
interface are gone from the bench host, and they did not come back. The bench
host is a virtual machine, which does not regain the device on its own. The
rules make that a STOP, and the owner must re-attach it.

The cause is not established. The stream had run for 475 s at 1.536 MB/s.
Whether that load contributed is open.

After the STOP the lane only made the bench safe and restored it. The
recorder was the lane's own process. It was ended by two terminate signals to its PID,
after checking its command line. The first was caught and left the write
blocked; the second ended it.

## What the SoC board can and cannot show

- **Data one BCLK after the frame-sync edge: shown.** The receiver is set for
  one bit of data delay, and the whole capture decodes bit-exact in all eight
  slots, in order. A one-bit offset either way would break every class of word
  check.
- **fs: shown on the SoC board's clock.** 47,997.947 Hz, with +-0.12 ppm
  timing granularity, plus the crystal's tolerance. It is 48 kHz at the
  board's accuracy, but it cannot resolve the plan's -10.64 ppm.
- **BCLK: inferred, not measured.** 256 x fs is 12,287,474 Hz, which assumes
  no idle bit clocks after the eighth slot.
- **Not shown by the SoC board,** and left to
  [#626](https://github.com/kebag-logic/milan-fpga/issues/626):
  - the FSYNC pulse width, since the receiver uses only the frame-sync edge;
  - edge timing: setup and hold of DOUT and FSYNC at the AM62x pins, BCLK
    duty cycle, and rise and fall times;
  - signal levels, overshoot and ringing;
  - the absolute frequency, against a calibrated reference.

## Bench as left

| State | As left |
|---|---|
| DUT stream state | Mappings removed and read back empty, stream unbound. The census equals the start in 31 of 33 entries: the DUT's live propagation delay, and the reference peer's GET_SAMPLING_RATE. That answered SUCCESS at the start and ENTITY_LOCKED at the end. This lane sent the peer read commands only |
| DUT control words | `VERSION`, every control word and `AEM` unchanged. `PP_STAT` `5b000444` became `5b000c44`; see the residuals below |
| Controller host | No gPTP daemon. The NIC clock reads 0 ppb and is back on its recorded trajectory, 4.5 us off. Timestamping is off, as found. Staging removed |
| SoC board | Bridge legs running with the recorded command lines, under new PIDs. PCM states as at the start; USB function configured on the SoC board; fault scan empty; `/tmp` as found |
| Bench host | The USB Audio card and the USB network interface are absent. Owner item |

Residuals that no permitted command restores:

- **DUT NVM persistence** advanced through the method's map and bind edits:
  commits 0 to 2, slots seq 237 and 238, `pend=1`, and `PP_STAT` bit 11. Lane
  B3 recorded the same.
- **DUT diagnostic counters.** `SLIP_LB` counted about 340 duplicates and as
  many skips per second from the bind on, and is saturated at `0xFFFF` in both
  halves. The render stage's rail count rose from 0 to 6,264. In lane B3's 70 s
  run they rose about 70 per second and from 4 to 134. The talker also ended
  about 55 s before the unbind, because the stalled capture held the SoC
  board's console until its deadline. Both counters clear only on reset.

## Rerun

The rerun needs the owner to re-attach the SoC board's USB function to the
bench host. The assignment can then run unchanged. This run adds four points:

- The SoC board has no `nc`. The shell's `/dev/tcp` streamed the capture with
  no gap of 100 ms or more for 475 s.
- The talker must outlast the capture plus the console's deadline, so a
  stalled capture cannot unbind a stopped talker late.
- The talker's late-PDU list caps at 5,000 entries. A run of 10 minutes needs
  a larger cap to attribute every underrun.
- If the stream's load is suspected, fs needs no data off the board. A capture
  discarded on the SoC board times its frames the same way, with no USB
  traffic. The pattern check of that same capture still needs the data. Which
  to run is an owner decision.

## Artifact hashes

The raw capture stays outside the packet, on the bench host. It holds every
byte received, which is the first 475.648 s of the capture.

| Raw file | Bytes | SHA-256 |
|---|---|---|
| `timing-long.raw` (8 x S32_LE at 48 kHz, 22,831,104 frames) | 730,595,328 | `dd201b3a926317a9f488b8290123fa235da7733dae06301f2cd21688da2d36cb` |

The lane packet, `b4-a468`, holds the redacted evidence and the tools. Its
manifest covers every retained file except itself.

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `identity/console-identity.txt` (console CRC, NVM and AEM readback) | 3,594 | `64e4bcc457e57809a118ea144f2dcf48287cbfd1dda1c2cc5a8a17dc601c7689` |
| `soc/r2-framing-dt.log` (hardware description of the sound card, codec and McASP0) | 4,672 | `4a4148f9e2f425b1a1b9763b62e77a7e0fe5014d72208f3c8e67f872712bf176` |
| `runs/timing-long/soc-capture.log` (capture parameters and the 5 s status samples) | 33,899 | `1a7e2a5231286a7253ed4c9c84d30a65fcff0750f3461baddf186cb7ab06f0f8` |
| `runs/timing-long/events.jsonl` (run steps, upload size and hash) | 1,355 | `787713e399effb6672a92a61c702f58fc15085e8b551acb5a00d1baf976e6cb5` |
| `runs/timing-long/decode.json` (pattern decode of the raw capture) | 193,423 | `661ccf760100b92f376fecd5b8af2f9216786970b1023d19782f9b020bf6442b` |
| `runs/timing-long/attribution-summary.json` (discontinuity clusters) | 1,335 | `85cf1428f03baf43ce50b3dd47e8a86ba3043def3a6b150eb20b1c0c3bbd8472` |
| `runs/timing-long/fit-fs.json` (fs from the status samples) | 2,081 | `0c77a36860c656813961e6b28d935a29fb16489c3011341d1acb3bc990b178fb` |
| `soc/r2-end-host-view.txt` (the bench host's USB events and cards at the end) | 1,390 | `a4c31c18a0d47fbe7c64b09b262a540814463ecd739eae66905c109354ca26ee` |
| `restore/r2-census-compare.txt` (census, start against end) | 843 | `82240ccecc1360a592cadacc9cba858745c2a0aead5c27492fb0bc2968906c8d` |
| `restore/r2-controller-restore.txt` (NIC clock and timestamping restore) | 922 | `17a3b3ca8fcf225f02053eae668007f224b14a177684daff8a3262ff8bc63582` |
| `summary/summary.json` | 9,561 | `093414244b454322d7075b8516bf56d6d7622330ee276a579c0a80564cebcaf4` |
