<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Media-clock following graded by THD+N on the ec0cc0c1 image

Refs #629. Operator [A477], 2026-10-01, under the
[bench lane B6 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5929778646).

The question is #629's bench acceptance: when a listener's CLOCK_DOMAIN
follows the talker's stream, is the media clock recovered correctly? The
metric is the owner's: the THD+N and SNR of a known tone on the selected path.
A digital path that follows correctly delivers the tone sample-exact, at the
numeric floor. A listener that does not follow drops or repeats samples, and
the metric must show it.

The first session stopped at a precondition, before any bench action
([STOP](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5929969516)).
The owner fixed it, and the second session ran every step below.

| #629 bench item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `ec0cc0c1` | PASS | See [Identity and setup](#identity-and-setup) |
| Analysis tool, proven on synthetic captures | PASS | A clean tone at the 24-bit floor; one dropped and one repeated frame found at the planted frame; 16 ppm and 1 ppm found both as a resampled rate and as slips. See [Tool controls](#tool-controls) |
| Format check before every bind | Held | Every listener took the talker's format and read it back; no talker format was set. See [Binding rule and clock-source record](#binding-rule-and-clock-source-record) |
| Clock source set on the listener only, read back, restored | Held | Three sets, each read back equal; each restored as found and read back. See [Binding rule and clock-source record](#binding-rule-and-clock-source-record) |
| A0, the reference peer on its as-found source (control) | PASS as a control | The metric shows the mismatch: 519 one-frame listener drops in 629.6 s (17.1 ppm) |
| A1, the peer following the DUT's AAF stream | PASS | 0 listener discontinuities in 617.3 s of captured audio; every block without a discontinuity at the floor |
| A2, the peer following the DUT's CRF stream | FAIL | 494 one-frame drops and 180 silent one-frame inserts by the listener in 616.1 s: the peer follows the DUT's CRF, but at INTERNAL the DUT's AAF stream runs 10.6 ppm off its own CRF. See [A2: the DUT's AAF and CRF outputs disagree at INTERNAL](#a2-the-duts-aaf-and-crf-outputs-disagree-at-internal) |
| B, the DUT on INTERNAL with the peer's CRF bound (control) | PASS as a control | The DUT's TDM clock runs +6.05 ppm off the peer's output, counted; +6.85 +-1.46 ppm timed |
| B, the DUT following the peer's CRF stream | PASS | Servo LOCKED 6.5 s after the set; frame-rate ratio 0 counted (0 net steps in 30,237,600 frames) and -0.01 +-0.65 ppm timed; 0 listener and 0 DUT beat discontinuities |
| B, THD+N of a known signal from the peer's talker | NOT RUN | No known signal reaches the peer's talker channels without a wiring change: they carry 0 to 2 LSB. See [Direction B](#direction-b) |
| B, the DUT following an AAF stream | Not in this image | AAF following on the DUT is #629's work |
| Restore | Done | Every clock source, format, binding and map read back as found; residuals listed in [Bench as left](#bench-as-left) |

These are operator observations, not review verdicts.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image's identity readback and the bench as found.
- **[Method](#method)** -- The tone, the analysis, the bench path, the binding rule, clock sources, the attribution of every discontinuity and the frame-rate ratio.
- **[Tool controls](#tool-controls)** -- The analysis tool on synthetic captures: the floor, a dropped and a repeated frame, 16 ppm and 1 ppm.
- **[Binding rule and clock-source record](#binding-rule-and-clock-source-record)** -- Every format read and set before each bind, and every clock-source set, read-back and restore.
- **[Direction A](#direction-a)** -- The DUT's talker to the reference peer's listener: THD+N, SNR, frequency offset and discontinuities per case.
- **[Direction B](#direction-b)** -- The reference peer's talker to the DUT's listener: the known-signal probe and the frame-rate ratio.
- **[The capture path](#the-capture-path)** -- Losses on the bench host's capture path, reported apart from clock effects.
- **[Bench as left](#bench-as-left)** -- The state at the end against the start, and the residuals.
- **[Limits](#limits)** -- What the measurements do not show.
- **[Artifact hashes](#artifact-hashes)** -- Raw files and the lane packet's evidence files.

## Identity and setup

The DUT runs the image of dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`, as
installed. The gate repeats the readback of lanes B3 to B5, and every value
equals theirs.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Live ENTITY and CONFIGURATION | Byte-equal to the AEM bytes the console dumps from QSPI (312 and 106 bytes); entity `020000fffe000001` |
| UART grader | 10 of 10 |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d178f19a` |
| Identity gate | PASS |

As found:

- **DUT.** NVM slot B seq 238 authoritative, 2 commits, `pend=1`, as lane B5
  left it. All queried stream states unbound, both DUT audio maps empty, and
  CLOCK_DOMAIN 0 on CLOCK_SOURCE 0, INTERNAL. SYNC=1, ASCAPABLE=1, TU=0.
- **Reference peer.** Every queried stream state unbound, its CLOCK_DOMAIN on
  its INTERNAL source. Its AAF stream input carried the 4-channel format
  `0205022001006000`, and it lists the up-to-8-channel `0215022002006000`.
- **SoC board.** Same boot as lane B5 left it. Both bridge legs ran with the
  bridge script's command lines, and the USB function was configured.
- **Controller host.** No gPTP daemon, no staging.

Another terminal on the bench host held the SoC board's serial console open
and consumed what the board printed. It was left alone. So the console was used
for input only. Each command fetched a short script from the bench host over
the board's USB network link, and the script sent its output back over the
same link (`soccon_net.py`). The root shell was confirmed that way with `id`
before any other board action: uid 0, on the console's own login shell. No
credential was typed or stored.

## Method

Every bench action held the shared lock, and every command had an explicit
deadline. No flash, reset, power, wiring, instrument setting or USB function
action occurred. No DUT PHY or CSR register was written. Each case ran as one
locked action of about 11 minutes with a hard deadline.

**Tone.** One loop of 48,000 frames, 1 s, eight channels of S32_LE with the
24-bit sample in bits 31:8, as at first light. Channel 0 carries 997 Hz and
channel 1 9,973 Hz, both at -1 dBFS, with non-zero start phases. Channels 2 to
7 are zero. Both frequencies are primes coprime with 48,000. Each tone
therefore runs a whole number of cycles per loop, and its quantization error
spreads like noise. The (channel 0, channel 1) pair of every frame is unique in
the loop, and no frame is silent. So every captured frame decodes to its loop
ordinal, and consecutive ordinals give every discontinuity with its exact size.
The bench host served the loop to the SoC board, which checked its SHA-256 and
played it into McASP0 in a loop for the whole case.

**Analysis** (`b6_thdn.py`). Per one-second block of 48,000 captured frames
and per tone:

- a four-parameter least-squares sine fit: amplitude and phase, DC, and the
  frequency refined from nominal;
- THD+N: the residual, band-limited to 20 Hz to 20 kHz, over the fitted
  fundamental, in dB;
- SNR: the fundamental over the band-limited residual left after also fitting
  the harmonics below 20 kHz;
- the fitted frequency against nominal, in ppm of the capture's own clock;
- every discontinuity: an ordinal step `e = d - 1`, where `e > 0` is a skip of
  `e` frames and `e < 0` a repeat of `-e` frames. A torn frame is one whose two
  words decode to different nearby frames.

A block of 48,000 consecutive loop frames is a rotation of the loop. Its THD+N
and SNR therefore equal the loop's own 24-bit floor exactly: -146.06 dB and
146.07 dB at 997 Hz, -145.99 dB and 145.99 dB at 9,973 Hz.

**Bench path, Direction A.** McASP0 plays the loop into the DUT's TDM input.
The DUT's STREAM_PORT_OUTPUT 0 takes eight identity mappings, so its AAF talker
carries the tone. The reference peer's AAF listener receives it, and the
peer's digital output goes to the external audio capture on the bench host. Two
of the capture's channels carry the tone, identified by content in every run:
in ten seconds of every channel, one carries only the 997 Hz loop's values and
one only the 9,973 Hz loop's.
McASP0 is the clock consumer of the DUT's TDM clock, so it plays in the DUT's
TDM clock domain.

**Bench path, Direction B.** The peer's CRF talker is bound to the DUT's CRF
input, STREAM_INPUT 1, and the DUT's CLOCK_DOMAIN follows it. The Direction A
tone path stays bound, which keeps the peer's output decodable. McASP0 also
captures the DUT's TDM output on the SoC board and discards it, which keeps its
capture side running for the timing samples. No audio leaves the board.

**Cases.** Each window is 630 s, untouched, from 20 s after the last bind or
clock-source set; for B CRF, from 20 s after the DUT's servo read LOCKED.

| Case | Peer CLOCK_DOMAIN | DUT CLOCK_DOMAIN | Streams bound |
|---|---|---|---|
| A0 | As found, INTERNAL | INTERNAL | DUT AAF to peer |
| A1 | The peer's clock source located on its AAF input | INTERNAL | DUT AAF to peer |
| A2 | The peer's clock source located on its CRF input | INTERNAL | DUT AAF to peer; DUT CRF, STREAM_OUTPUT 1, to peer |
| B INTERNAL | As found, INTERNAL | CLOCK_SOURCE 0, INTERNAL | DUT AAF to peer; peer CRF to DUT STREAM_INPUT 1 |
| B CRF | As found, INTERNAL | CLOCK_SOURCE 1, located on STREAM_INPUT 1 | DUT AAF to peer; peer CRF to DUT STREAM_INPUT 1 |

**Attribution** (`grade_b6.py`). Every discontinuity is put in one class:

- **Capture path.** Skips of two frames or more, grouped when within 300 ms,
  whose frames the bench host's capture path lost. The bench host stamped every
  capture read. A frame lost inside the capture path raises the delivery
  deficit, the read time less the frames received at 48 kHz, by the lost
  duration. A cluster is capture path when that deficit's floor rises across
  it by the cluster's size within 1 ms + 2 %. A loss longer than the 1 s loop
  shows its size modulo 48,000 frames, so whole loops are added to match.
  Where neighbouring events leave too few reads to measure the rise, or a
  neighbouring stall spoils it, the cluster needs a read gap of 11 ms or more
  in the 600 ms before it. Where the rise is spoiled, every skip in the cluster
  must also be 48 n + 12 frames, the size of most losses with a matching rise.
  This is lane B5's read-time method.
- **DUT beat.** At INTERNAL the DUT's talker repeats one whole frame per beat,
  93,990 frames, 1.958 s ([TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff)).
  In source frames, the captured frame plus every earlier step, the beat is a
  single comb: one phase, one period, every tooth present. The comb is the
  densest phase of one-frame repeats, refined by a line fit. Its members within
  50 frames are the beat. The DUT's own `SLIP_TDM` count is the cross-check.
- **Listener.** Everything else: the reference peer's output dropped, repeated
  or, as an insert, carried one silent frame between two consecutive loop
  frames.

**How the attribution was refined.** The rule written before the following
cases ran was simpler:

- a skip of two frames or more was capture path only at a read gap of 11 ms or
  more within three reads;
- a one-frame repeat was the DUT's beat when it lay within 600 frames of a
  whole number of beats from another.

Grading found losses that this rule missed, and the rules above replaced it.
Each change was applied to every case.

| Change | Found in | What it catches |
|---|---|---|
| Clusters within 300 ms, tested by the read-time rise | A0 | A loss that shows in the audio up to 370 ms after its read stall, as the capture buffers 500 ms: a 9,996-frame skip with a 208.0 ms rise |
| Whole loops, and a cluster's net step | A1 | A 12.7 s stall whose loss, 12 loops and 18,626 frames, shows as 18,626 frames, with a rise of 12,387.9 ms; stale audio replayed from one capture buffer back |
| The read gap and size rule where a rise is spoiled | A2 | Losses next to a 13.3 s stall |
| The beat as a single comb | A2 | A listener that slips at the beat's rate, on its own phase |
| Silent inserts | A2 | Listener frames that are silent rather than repeated |

Under the first rule A1 has 4 and B CRF 3 multi-frame events outside the
capture path, and both would fail. Those events are skips of 60, 252 and
18,626 frames and steps back of 23,880 and 24,000 frames. Each lies in a
cluster whose read-time rise matches its loss, or, for one 60-frame skip, after
a 33 ms read stall. A step back of 24,000 frames is exactly the external
capture's 0.5 s buffer. A0, A2 and B INTERNAL keep their verdicts under either
rule.

**Frame-rate ratio.** McASP0 runs on the DUT's TDM clock, and the capture
records the peer's output. Two estimates:

- **Counted.** Between two consecutive captured frames, McASP0 played as many
  frames as the ordinal advanced, while the peer's output produced one. So
  McASP0 against the peer, less 1, is the sum of the non-capture-path steps
  over the captured frames. Audio the capture path lost is left out, with any
  event inside it. One frame is 0.033 ppm of a 630 s window.
- **Timed.** The SoC board read McASP0's PCM status five times a second. The
  read brings `hw_ptr` up to date. It sent each sample line over the board's
  USB network link to a receiver on the bench host, which stamped its arrival
  on `CLOCK_MONOTONIC_RAW`. The capture's reads were stamped on the same clock.
  Each rate is the slope of the lower envelope of the delivery deficit, the
  Theil-Sen median over 10 s segment minima. The capture's read times sit on
  the bench host's USB frame grid, so its deficit floor is a 1 ms sawtooth.
  The 95 % half-width therefore combines the bootstrap interval with half the
  difference between the window's two halves. That definition was set after
  grading A0 and before grading any other case.

**Pass criteria,** fixed before any following case ran:

- A1 and A2 pass with 0 listener discontinuities in the window, every block
  without a discontinuity at the floor within 0.01 dB, and the fitted offset
  on those blocks under 0.001 ppm in magnitude. The set clock source must read
  back.
- B CRF passes when the DUT's servo reads LOCKED, the counted ratio is within
  0.5 ppm of zero, the timed ratio's interval holds zero, and the tone path has
  0 listener discontinuities.
- A0 and B INTERNAL are controls. They pass when the metric shows the DUT and
  the peer apart.

## Tool controls

The tool was run on synthetic captures before any live case (`controls.json`).

| Control | Planted | Found | THD+N of the affected block, 997 Hz / 9,973 Hz, dB | Result |
|---|---|---|---|---|
| Clean, 10 s | Nothing | 0 events; 10 of 10 blocks at the floor within 0.00001 dB; offset 0.000000 ppm | -146.06 / -145.99 | PASS |
| One dropped frame | Frame 216,777 | One skip of 1 frame at frame 216,777; 9 blocks at the floor | -29.72 / -9.45 | PASS |
| One repeated frame | Frame 289,234 | One repeat of 1 frame at frame 289,234; 9 blocks at the floor | -34.03 / -14.40 | PASS |
| 16 ppm, resampled tone, 10 s | Source clock 16 ppm fast | Fitted +16.000000 ppm on both tones; 8 of 480,000 frames decode, where the drift reaches a whole frame | -146.02 / -146.02 | PASS |
| 1 ppm, resampled tone, 10 s | Source clock 1 ppm fast | Fitted +1.000000 ppm on both tones; 1 frame decodes | -145.99 / -146.02 | PASS |
| 16 ppm as slips, 30 s | One frame dropped every 62,500 | 23 one-frame skips, all 62,500 frames apart | -28.48 / -8.10 | PASS |
| 1 ppm as slips, 90 s | One frame dropped every 1,000,000 | 4 one-frame skips, all 1,000,000 frames apart | -28.60 / -8.25 | PASS |

A rate error therefore shows either as a fitted offset, when the source is
resampled, or as discontinuities at its rate, when it slips. Both kinds are
found with their sizes. The 9,973 Hz tone makes a timing error about ten times
larger, and its blocks with one slip sit 20 dB above the 997 Hz tone's.

## Binding rule and clock-source record

Before every bind the controller read the talker's and the listener's current
stream formats. Where they differed it set the listener's format to the
talker's and read it back, then sent `CONNECT_RX`. Clock sources were set only
on the listener's CLOCK_DOMAIN and read back with `GET_CLOCK_SOURCE`.

| Bind or set | Talker format | Listener format read | Set on the listener | Read back |
|---|---|---|---|---|
| DUT AAF to peer, every case | `0205022002006000` | `0205022001006000` | `0205022002006000`, SUCCESS | `0205022002006000` |
| DUT CRF to peer, A2 | `041060010000bb80` | `041060010000bb80` | None, equal | `041060010000bb80` |
| Peer CRF to DUT STREAM_INPUT 1, B INTERNAL and B CRF | `041060010000bb80` | `041060010000bb80` | None, equal | `041060010000bb80` |
| Peer AAF to DUT STREAM_INPUT 0, the Direction B probe | `0205022001006000` | `0205022002006000` | `0205022001006000`, SUCCESS | `0205022001006000` |
| A1: the peer's CLOCK_DOMAIN to its source on its AAF input | - | - | SET_CLOCK_SOURCE SUCCESS | Equal to the set index |
| A2: the peer's CLOCK_DOMAIN to its source on its CRF input | - | - | SET_CLOCK_SOURCE SUCCESS | Equal to the set index |
| B CRF: the DUT's CLOCK_DOMAIN 0 to CLOCK_SOURCE 1 | - | - | SET_CLOCK_SOURCE SUCCESS | 1 |

Every bind answered SUCCESS with connection count 1, and every unbind
connection count 0. Each case ended with its clock source set back to the
as-found source and read back: the peer's in A1 and A2, the DUT's in B CRF.
The peer's AAF input format was set back to `0205022001006000` and the DUT's
STREAM_INPUT 0 to `0205022002006000`, each read back equal.

## Direction A

The tables below cover the windows; `b6_tables.py` renders them from the grades.

<!-- thdn-a -->
| Case | Tone | Blocks | Blocks at the floor | THD+N there, dB | SNR there, dB | Worst THD+N, a block with a listener discontinuity, dB | Worst THD+N, a block with only the DUT's beat, dB |
|---|---|---|---|---|---|---|---|
| A0 | 997 Hz | 629 | 54 | -146.06 | 146.07 | -2.52 | -28.48 |
| A0 | 9,973 Hz | 629 | 54 | -145.99 | 145.99 | +4.70 | -8.10 |
| A1 | 997 Hz | 617 | 291 | -146.06 | 146.07 | None | -28.48 |
| A1 | 9,973 Hz | 617 | 291 | -145.99 | 145.99 | None | -8.10 |
| A2 | 997 Hz | 616 | 1 | -146.06 | 146.07 | +3.13 | -28.48 |
| A2 | 9,973 Hz | 616 | 1 | -145.99 | 145.99 | +17.28 | -8.10 |

A block at the floor holds no discontinuity and no undecodable frame. Its THD+N
equals the loop's floor within 0.0006 dB in every case. A positive THD+N is a
block whose residual exceeds the tone: a capture-path loss inside it.

<!-- offset-a -->
| Case | Fitted offset, blocks at the floor, ppm (largest magnitude, either tone) | Listener drops | Listener silent inserts | DUT beat repeats | Counted McASP0 to peer ratio, ppm |
|---|---|---|---|---|---|
| A0 | 3.1e-7 | 519 | 1 | 321 | +6.519 |
| A1 | 1.9e-7 | 0 | 0 | 315 | -10.631 |
| A2 | 2.2e-7 | 494 | 180 | 316 | -0.068 |

<!-- discontinuities-a -->
| Case | Window of captured audio, s | Beat comb period, frames | Beat teeth expected | DUT `SLIP_TDM`, per s | Capture-path losses: events, clusters, frames | Torn frames | Result |
|---|---|---|---|---|---|---|---|
| A0 | 629.56 | 93,990.39 | 321.8 | 0.5111 | 25, 10, 26,173 | 0 | PASS as a control |
| A1 | 617.32 | 93,990.38 | 321.8 | 0.5111 | 51, 23, 615,026 | 0 | PASS |
| A2 | 616.14 | 93,990.38 | 322.0 | 0.5096 | 143, 61, 686,656 | 0 | FAIL |

The beat comb's members sit within 1.8 frames of its line in every case. Its
rate, 0.5107 per second at 48 kHz, matches the DUT's own `SLIP_TDM` count
within 0.3 %.
Teeth missing from the comb fall inside capture-path losses.

**A0.** The peer, on its INTERNAL source, drops one frame every 1.21 s on
average: 17.1 ppm. The DUT's beat adds one frame every 1.958 s: 10.6 ppm. Net,
McASP0 runs +6.52 ppm off the peer's output, against +6.44 +-0.72 ppm timed.
Lane B5 measured 16.4 ppm of drops at the peer's output and the same beat. The
metric shows the mismatch: 575 of 629 blocks leave the floor, to between -45
and +8 dB.

**A1.** Following the DUT's AAF stream, the peer drops and repeats nothing in
the window. Every non-capture-path discontinuity is the DUT's own beat, on its
comb. The peer's output runs at the stream's rate, so the counted ratio is the
beat itself, -10.63 ppm; timed -12.19 +-2.44 ppm. Every block without the beat
or a capture-path loss is at the floor, with no fitted offset.

### A2: the DUT's AAF and CRF outputs disagree at INTERNAL

Following the DUT's CRF stream, the peer's output runs at the DUT's TDM rate:
the counted ratio is -0.07 ppm, -0.59 +-1.24 ppm timed. The tone does not arrive
sample-exact. Each beat period holds the DUT's repeat and, about 48,000 frames
later, one listener drop. At 180 of those drops the peer dithers, with a silent
one-frame insert. Net, the 494 drops less the 180 inserts equal the DUT's 316
repeats within two frames. Only 1 block of 616 is at the floor.

The DUT's two outputs run on two clocks at INTERNAL. The CRF talker divides the
audio MMCM clock by 512 (`hdl/milan/milan_datapath.sv:445`): the physical
sample grid, 47,999.4893 Hz nominal. The AAF talker's packet grid is the
free-running 48,000.0000 Hz NCO. The two are 10.64 ppm apart, the beat
([TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff)). A listener
that follows the DUT's CRF therefore receives the DUT's AAF stream 10.64 ppm
fast and must drop one frame per beat. The DUT's own talker beat already
repeats one, so the pair nets to zero but leaves two discontinuities per beat.
Under CRF selection the DUT aligns the packet grid to the physical grid, as the
B CRF case shows. This disagreement is therefore specific to INTERNAL.

## Direction B

**Known-signal probe.** The peer's talker carries its own inputs. Whether a
known signal is on them was established from the levels of what it sends,
without a wiring or instrument change. Under the binding rule, the DUT's
STREAM_INPUT 0 took the peer talker's 4-channel format, set, read back and
later restored. With four identity mappings on STREAM_PORT_INPUT 0 and the
bind up, the SoC board recorded 2 s of the DUT's TDM output. It reduced the
recording to per-channel statistics on the board.

| TDM output channel | Frames | Non-zero words | Range, 24-bit LSB | Mean square, LSB squared |
|---|---|---|---|---|
| 0 | 96,000 | 51,004 | -2 to 0 | 0.535 |
| 1 | 96,000 | 50,812 | -2 to 0 | 0.533 |
| 2 | 96,000 | 46,870 | -1 to 0 | 0.488 |
| 3 | 96,000 | 46,825 | -1 to 0 | 0.488 |
| 4 to 7, unmapped | 96,000 | 0 | 0 | 0 |

The talker's channels carry an idle floor of at most 2 LSB, not a known
signal. THD+N grading of Direction B is therefore NOT RUN. Clock following is
graded by the frame-rate ratio of McASP0, in the DUT's TDM clock domain, and
the external capture, recorded at the same time.

<!-- ratio-b -->
| Case | Counted ratio, ppm | Timed ratio, ppm (95 % half-width) | Window halves, timed, ppm | DUT media-clock servo | Listener discontinuities | DUT beat repeats | Blocks at the floor | Result |
|---|---|---|---|---|---|---|---|---|
| B INTERNAL | +6.052 | +6.85 (+-1.46) | +8.70 / +6.43 | IDLE (`MCSRV_STAT` `0x00000020`) | 506 drops, 1 silent insert | 322 | 57 of 629 | PASS as a control |
| B CRF | 0.000 (0 net steps in 30,237,600 frames) | -0.01 (+-0.65) | +0.18 / +1.30 | LOCKED, trim -6.0 ppm (`0xffa00034` to `0xffa10034`) | 0 | 0 | 611 of 629 | PASS |

**B INTERNAL.** The DUT's CRF sink locked on the peer's CRF (`CRF_CTRL[31]`),
but the DUT's CLOCK_DOMAIN stayed on INTERNAL and its servo IDLE. McASP0 then
runs +6.05 ppm off the peer, as in A0. The binding of the CRF input alone does
not move the DUT's clock.

**B CRF.** SET_CLOCK_SOURCE 1 answered SUCCESS and read back 1. The servo read
ACQUIRE 3.3 s after the set and LOCKED 6.5 s after it, and it stayed LOCKED
through the window. Its trim, -6.0 ppm, cancels the +6 ppm the control
measured. Over the window McASP0 and the peer's output advanced frame for frame:
0 net steps in 30,237,600 captured frames. `SLIP_TDM` did not move, and the
DUT's beat is gone. On the same tone path the peer's INTERNAL listener now
receives the DUT's stream at its own rate. It drops and repeats nothing, so 611
of 629 blocks are at the floor. The other 18 hold capture-path losses only. The
servo status also carries bit 4, DRP config mismatch, from ACQUIRE on. It is
recorded here and not analysed.

On the SoC board's own uncalibrated clock McASP0's capture ran at 47,997.91 to
47,997.96 Hz in the INTERNAL cases and at 47,997.67 Hz in B CRF.

## The capture path

The bench host's external capture lost audio in every run, as in lane B5. The
losses sit at stalls of the bench host's capture reads, up to 13.3 s long.
These are separate from every clock effect above.

| Case | Capture reads in the window | Read stalls over 15 ms | Capture-path clusters | Frames lost | Longest read stall |
|---|---|---|---|---|---|
| A0 | 62,844 | 105 | 10 | 26,173 | 576 ms |
| A1 | 61,579 | 232 | 23 | 615,026 | 12.7 s |
| A2 | 61,337 | 316 | 61 | 686,656 | 13.3 s |
| B INTERNAL | 62,851 | 211 | 21 | 15,552 | 212 ms |
| B CRF | 62,923 | 97 | 17 | 12,216 | 81 ms |

- Every capture-path cluster's read-time rise matches its loss within
  1 ms + 2 %, except clusters whose rise is unmeasurable. Those meet the read
  gap and size rule instead: 1 in A0, 2 in A1, 7 in A2, 3 in B INTERNAL and none
  in B CRF.
- 255 of the 265 skips in clusters with a matching rise are 48 n + 12 frames.
  Of the other ten, two are losses longer than a loop and four are the edges of
  stale replays (next item). Two are one frame off the pattern, and two are
  parts of a cluster whose total is 48 n + 12.
- Five clusters also replayed stale audio from about one capture buffer, 24,000
  frames, back: one run of 6 frames in A1, runs of 1 and 2 frames and one
  step back and forth in A2, and in B CRF one cluster that stepped back 24,000
  frames twice. With whole loops added where the rise asks for them, each
  cluster's net step matches its read-time rise.
- A loss longer than the loop hides any event inside it. That is why the beat
  combs miss a few teeth.
- One-frame listener events show no read-time rise. The median is 0.00 ms in
  every case and the largest magnitude 1.0 ms, the host's USB frame step. The
  two exceptions, 2.7 ms and 177 ms, sit next to A2's 13.3 s stall.

## Bench as left

| State | As left |
|---|---|
| DUT stream state | All unbound; both audio maps empty, read back |
| DUT clock domain | CLOCK_SOURCE 0, read back |
| DUT STREAM_INPUT 0 format | `0205022002006000`, as found, read back |
| Reference peer | Its CLOCK_DOMAIN on its as-found source and its AAF input format `0205022001006000`, both read back after every run; every stream unbound |
| Census, start against end | 43 of 46 entries equal. The others: the DUT's live propagation delay, and two of the peer's talker states, which now report a stream ID, destination MAC and VLAN with connection count 0 |
| DUT console words | `VERSION`, control words and AEM unchanged; live counters and words moved: the talker frame counters, `SLIP_TDM`, `RENDER_STAT`, the propagation delay, time, `CRF_RATE` and `CRF_STATUS` |
| DUT saved state | NVM commits 2 to 8, slots seq 243 and 244, `pend=1` |
| SoC board | Same boot; both bridge legs running with the script's command lines under new process IDs; PCM states, USB function and fault scan as at the start; no task file left |
| Controller host | No task process; staging removed |
| Bench host | Both USB audio devices present; the board link's address present |

Residuals that no permitted command restores:

- **DUT NVM persistence** advanced through the method's format, map and
  clock-source edits: commits 2 to 8. Lane B3 recorded the same class.
- **The peer's talker states** keep the stream parameters of the streams it
  sent, with connection count 0.
- **DUT counters** that clear only on reset: `SLIP_TDM`, `RENDER_STAT`, and the
  CRF sink's `CRF_RATE` and `CRF_STATUS`, which hold their last values.

## Limits

- The DUT's AAF following is not in this image. #629's bench acceptance for
  that source stays open.
- Direction B's THD+N is not graded: no known signal reaches the peer's talker
  without a wiring change.
- One run per case, on one DUT, against one reference peer, on two tones.
- Only the tone's two channels are observed at the peer's output.
- The counted ratio leaves out audio the capture path lost and any event inside
  it.
- The A1 and B CRF verdicts rest on the refined capture-path attribution. Under
  the rule as first written both would fail; see
  [Method](#method), "How the attribution was refined".
- The timed ratio depends on the bench host's read-time floor. Its interval
  is wide where the capture stalled for seconds (A1, A2).
- The A2 diagnosis rests on the measured rates and on the code and design
  reference cited. No CRF timestamp was captured on the wire.
- The servo's DRP config mismatch bit is recorded, not analysed.
- Printed precision is not calibrated accuracy.

## Artifact hashes

The raw files stay outside the lane packet, on the bench host. Each run's
`events.jsonl` records the size and SHA-256 of its raw files.

| Raw file | Bytes | SHA-256 |
|---|---|---|
| Tone loop (`b6_tone.py`) | 1,536,000 | `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588` |
| `a0/cap-lr.raw` (the tone's two channels, S24_3LE) | 190,010,880 | `8143bd4fad5e2ff0deae8372d8d66b99c4b678b2a44e73cff820a93cf337c344` |
| `a0/cap-ts.bin` (capture read times) | 1,580,688 | `2d76b8fab56182e900a260244e35ac38180f907df88f2d33ddfb97d2ce04494c` |
| `a0/samples.txt` (McASP0 timing samples) | 389,338 | `9dc07e479c4b79be77f3b6f70c6e684e1d37df02520ad11a1cb90f359deb7abf` |
| `a1/cap-lr.raw` | 186,779,586 | `c837e7bd9bca3a4fe15838cf7a12d246854d856ec2ca92c1e6365ac19b55e14e` |
| `a1/cap-ts.bin` | 1,552,368 | `93f04afd37e01a0c3ba7daaa8ccae64d9b5dcbffbf21a0dd64bc8d696bccf7b9` |
| `a1/samples.txt` | 389,338 | `7210d7c7a3fdd4e35eee676ee2842c3bd6ff1e227274ee51279135d80d672820` |
| `a2/cap-lr.raw` | 186,462,774 | `95e03f6532f6f7fa82ec1da986abd618de3192e2b5babe29e0fc462b50afc0da` |
| `a2/cap-ts.bin` | 1,547,232 | `10d9ffbcae443b505ebaa95bda886d3f85a4761de5187a32c5354b60b982ab5c` |
| `a2/samples.txt` | 389,590 | `c774046c91f9e83ab8bd2d9cdadba48f76ecebe9ff9fd4bccd81d3a6e0f40e65` |
| `bint/cap-lr.raw` | 190,379,676 | `5da6f75f1cdda03f2fc4fb9a97dbe904909bffe144a4b6ff7aa5979356df86a8` |
| `bint/cap-ts.bin` | 1,582,632 | `214fe56d676a16cc75c1291135287bb6c5c550c3b1a12b0bd7d1f3e2a01565f1` |
| `bint/samples.txt` | 389,590 | `6a572c7a2bdead95797e05bd6391bb626d5fad1efae14ae002f0b8a306921ec0` |
| `bcrf/cap-lr.raw` | 190,569,882 | `a4b12957fb4d7be5dc6b88781e1d76ef78052cbd58521875efad5157ead724b6` |
| `bcrf/cap-ts.bin` | 1,586,376 | `95ce2232a73a6c60ec4a5656707eb36bef8604dd2d08d9880047b7f2086e48c9` |
| `bcrf/samples.txt` | 389,594 | `e0a237985893735a32719b7ceb69e85f054d112e37452d2725fc95c73861a95d` |
| `a0/grade-full.json` (full grade, `grade_b6.py`) | 592,109 | `345b207980f843591131efa39beb989ce01d006826327a94ea9fa92bcf6b9449` |
| `a1/grade-full.json` | 462,460 | `cc698b080f3c494036ba3e51790c87449176895070e1ad872e974e567377af1b` |
| `a2/grade-full.json` | 686,336 | `0b076c64514b31fef086795200706815e563b6301229164f67a8fa5932ca2785` |
| `bint/grade-full.json` | 597,288 | `7e54bb7cf2caa25531ef468dddeb2958bc45d7b05e0ec4381a18d216cbe48776` |
| `bcrf/grade-full.json` | 373,090 | `a8c359ee89bca388874dfed7a1e93e0abe7bb1a822086b19e824669f6430b498` |

The lane packet, `b6-a477`, holds the redacted evidence and the tools. Its
manifest covers every retained file except itself.

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `controls/controls.json` (tool controls) | 17,070 | `7bbefc71fb3c9303a8f1cb843bfcd13dafe55c1f3e1a968e6a3b3cee2350530e` |
| `summary/tables.md` (the per-case tables as rendered) | 3,156 | `fa9400b3c27b62c0b3a919bff0576023df6627e1303c3838a0faaa2d825572ca` |
| `summary/a0/grade.json` | 16,014 | `650f0444d2a4a9aef9d1d819909056ba6c4f200c7f5c9b13d0079f9c97b4d09d` |
| `summary/a0/events.csv` | 47,876 | `66166cc1353b12604a5a30d79e2e4b0b54869d5b26c78420861fd51d00951c3a` |
| `summary/a0/blocks.csv` | 43,799 | `c3774b87a546c20a09f94a8d5372446cbfce12b2dd69069df40abdbe4bd30eb5` |
| `summary/a1/grade.json` | 20,990 | `1ab69ed8c43c347b3239dc244c18daf04fd79962a5c6b243447ea63a7ac1ca0f` |
| `summary/a1/events.csv` | 21,561 | `584fda4ff0ffb808f783d057d9fff33021ee209567847b0ec59e9e1771286730` |
| `summary/a1/blocks.csv` | 46,624 | `2dc400e929318d8d891d8a416482c7433ba569f242227835a0bc68c59ab7ea74` |
| `summary/a2/grade.json` | 35,003 | `15058a81cf7640dc942ff7bdf7c3981d9fa54b85660e1df7574069988500243f` |
| `summary/a2/events.csv` | 61,233 | `b08545249716ac830ddbc345f5c8e5e59f9ae188fa01cf5ef8dbc6cb60195b15` |
| `summary/a2/blocks.csv` | 42,236 | `d731a33ecc1b5722261ab34472062b8a8f8c56b3af44f737ac82bd7b53607b18` |
| `summary/bint/grade.json` | 20,603 | `839aa25b7fc366bf2c0597b65f0b005043769ab82a2b8878b593936be1c38dbd` |
| `summary/bint/events.csv` | 47,971 | `19bf182a3c2b658cd41bd46c9d742c9c156a9e7e5f253f9311f70f5f8a6b0f60` |
| `summary/bint/blocks.csv` | 43,773 | `85bbedec1a01f277a6c1a683d049438afa76567bfb7c3e0267d0eb7f6c818e1b` |
| `summary/bcrf/grade.json` | 17,617 | `a0cf772ce6e8d4fe2d3ae79264f17f170f91657091ffb25808d97ff6e7883f2a` |
| `summary/bcrf/events.csv` | 2,823 | `c980c97aae86d2cf95b244062b3d9b95e03a0c24e4f86c29cb6a4f1793950139` |
| `summary/bcrf/blocks.csv` | 51,685 | `96831ea2ea4be0d24be6fbf87ce30b5bc3052835ce25e97f779260dcdc287e62` |
| `runs/a0/events.jsonl` (run steps, raw file hashes) | 9,281 | `a21569eb990726ca57490c4d57f2b71d9649bd55f7b61dddbf4c59ec9d472bfb` |
| `runs/a1/events.jsonl` | 9,609 | `ac8501fe4c4a25450975d7d016b6cf9af82ddb02dd17dea0d89d795fe97e16af` |
| `runs/a2/events.jsonl` | 10,283 | `693a23f80cca8550c36bbdb76e449471135a216852d322a5c5146f51eae82ade` |
| `runs/bint/events.jsonl` | 9,961 | `45229c3131f8e589ed59f97abde037c59465dacae4bff7a8d084a9a17e74d10d` |
| `runs/bcrf/events.jsonl` | 11,223 | `def961ead82e8f42c40694e5c3514deda810e3bbc31ae6518961f10316a3c3c8` |
| `runs/probe/soc-record.log` (the probe's statistics, as the board printed them) | 1,727 | `1b7ac6e8b721a07cf88516782b9240cd55bf96a57a45e3e9297a8f4e7df59ca8` |
| `runs/probe/events.jsonl` | 1,835 | `3a392e80dfd7268fa20d52dc6a802dcdcb1dd5d15a9dcaca0078af8dc2f0fa39` |
| `identity/console-identity.txt` (console CRC, NVM and AEM readback) | 3,594 | `ea8a6d413bc9c7f30eb96b4cebf0a76cd7c9778c348b2e818812da075ebda0c2` |
| `restore/census-compare.txt` (census, start against end) | 1,564 | `5a2fdfc8916d617a112eee6d54adb618a3d3b2c6c97419bce8f0bab644e09b34` |
| `tools/b6_tone.py` | 2,965 | `d188a1a9ac0c3d94a2dab7d7b44ff7487490c87b969ea8c7d1b69382743179ac` |
| `tools/b6_thdn.py` | 12,423 | `d4673f55642b850f57601b27d8fc930cc5382c2138f54edb1a7296bb4653a95f` |
| `tools/grade_b6.py` | 24,348 | `386ac2a62773f573dbe4f04d94b02905065ef15cedbd35a04020ba3f751df456` |
| `tools/run_b6.py` | 27,257 | `7e1701a7657d36453758e67193af0ff0bfc5ef0df92b691c9e82f60c62fa376d` |
| `tools/probe_b6.py` | 9,215 | `176b0e5a37dc6fbfde52886887d6e5657cad69db481d05b30d7c3dba9eaffa13` |
| `tools/soccon_net.py` | 5,097 | `12d135c654d88f3e6be8f9dcc8350498d777766863591ad60122f50d3f4fd4e5` |
| `tools/b6_ctl.py` | 11,624 | `ee10a9f7ac2523148454b683af5fb8315a9c6fd2b93ceebcbe518b914d884c60` |
