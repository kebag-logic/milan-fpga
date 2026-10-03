<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Media-clock following graded by THD+N, on the ec0cc0c1 and bbf704ec images

Refs #629. Operator [A477], 2026-10-01, under the
[bench lane B6 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5929778646).
Lane B7 repeated the bench on dev `bbf704ec`, after PR #634, on 2026-10-03; its
results are in [Dev bbf704ec, 2026-10-03: lane B7](#dev-bbf704ec-2026-10-03-lane-b7).

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
- **[Method](#method)** -- The tone, the analysis, the shakedown runs, the bench path, the binding rule, clock sources, the attribution of every discontinuity, what it can absorb, and the frame-rate ratio.
- **[Tool controls](#tool-controls)** -- The analysis tool on synthetic captures: the floor, a dropped and a repeated frame, 16 ppm and 1 ppm.
- **[Binding rule and clock-source record](#binding-rule-and-clock-source-record)** -- Every format read and set before each bind, and every clock-source set, read-back and restore.
- **[Direction A](#direction-a)** -- The DUT's talker to the reference peer's listener: THD+N, SNR, frequency offset and discontinuities per case.
- **[Direction B](#direction-b)** -- The reference peer's talker to the DUT's listener: the known-signal probe and the frame-rate ratio.
- **[The capture path](#the-capture-path)** -- Losses on the bench host's capture path, reported apart from clock effects.
- **[Bench as left](#bench-as-left)** -- The state at the end against the start, and the residuals.
- **[Limits](#limits)** -- What the measurements do not show.
- **[Artifact hashes](#artifact-hashes)** -- Raw files, the lane packet's evidence files, and where the packets are published.
- **[Dev bbf704ec, 2026-10-03: lane B7](#dev-bbf704ec-2026-10-03-lane-b7)** -- The bench repeated on the image with #634: identity, method changes, all six cases with B-AAF new, the lock-loss and INTERNAL-clock observations, the capture path, the #629 acceptance judged item by item, limits and hashes.

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

**Shakedown runs.** Before the cases the SoC board's two bridge legs were
stopped by process ID, each command line checked first. At the end they were
restarted with the recorded command lines. Three tool shakedown runs preceded
the cases and are not graded:

- `smoke-a0-clkparse` stopped at the as-found check, before any map, bind or
  playback, because the tool's clock-source parse returned nothing. Nothing
  was set.
- `smoke-a0`, A0 with a 30 s window. The board's timing sampler lost its
  `hw_ptr` line in 107 of 249 samples, and was fixed.
- `smoke2-a0`, A0 with a 90 s window, a check of the fixed tools.

The last two bound the DUT's AAF stream to the peer under the binding rule,
set the peer's format and edited the DUT's map, then restored all of it and
read it back, as the cases did. Their edits are part of the NVM commit count
in [Bench as left](#bench-as-left).

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
clock-source set and its read-back. The tool waits in 0.5 s steps, so the
windows opened 20.0 to 20.5 s after it. B CRF follows the same rule: its
window opened 20.5 s after the clock-source set, which was 14.0 s after the
DUT's servo first read LOCKED.

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

**What the attribution can absorb.** The rules above can hide a listener event
in six ways. For A1 and B CRF each is checked against the grades
(`grade.json`, `events.csv`) and the capture read times:

1. **A one-frame drop at the same step as a capture loss.** The two merge into
   one skip one frame longer than the loss. The rise test's 1 ms + 2 % cannot
   resolve one frame, 0.02 ms. Such a skip is 48 n + 13 frames, and a merged
   repeat 48 n + 11.
   - B CRF: every capture-path skip is 48 n + 12, and its stale replay steps
     back exactly 24,000 frames twice.
   - A1: every capture-path skip is 48 n + 12 but two. One is the 23,880-frame
     edge of its stale replay, which a step back of exactly 23,880 frames
     cancels. The other is the 12.4 s loss at its 12.7 s read stall, twelve
     loops and 18,626 frames, whose size has no pattern. A drop at the very
     edge of that loss cannot be told from lost audio, which every figure
     leaves out with any event inside it.
   - A0 and A2 each hold one 48 n + 13 skip; see
     [The capture path](#the-capture-path).
2. **A one-frame repeat within 50 frames of a beat tooth.** Comb membership is
   a 50-frame window with no check of one member per tooth, so such a repeat
   would count as the DUT's beat.
   - A1: its 315 members sit one per tooth, at least 93,989 frames apart. Each
     lies 75 frames or more from a capture-path event, so none can stand in
     for a beat that lost audio hid. Its 7 missing teeth all fall inside that
     12.4 s loss.
   - B CRF has no one-frame event of any kind.
3. **A capture-loss-sized skip after a read gap, with no loss measured.** Where
   a rise is measured but does not match, the cluster is still capture path
   when a read gap of 11 ms or more precedes it and every skip is 48 n + 12.
   A listener skip of that size after an ordinary read gap would pass.
   - A1 and B CRF have no cluster on this branch. A2 has two.
4. **A skip of 2 to 48 frames with no stall.** Such a skip is 1 ms or less, so
   a rise of zero matches it within 1 ms + 2 %. The read-time floor steps by
   up to 1.0 ms with no loss at all, which widens that band to about 98
   frames.
   - A1 and B CRF: the smallest capture-path loss is 60 frames. Each of their
     seven clusters under 98 frames is one 60-frame skip, 48 n + 12, after a
     read gap of 14.9 ms or more. Six have a measured rise, 0.99 to 1.00 ms,
     at the floor's step, so for them the read gap and the size carry the
     attribution. The seventh, A1's skip after a 33 ms read stall (cluster 9
     in its `grade.json`), has no measurable rise. It passed on the read gap
     alone, the gap-only branch of item 5.
5. **The gap-only branch.** Where the rise is unmeasurable, a read gap of
   11 ms or more in the 600 ms before is enough, with no size check. In these
   windows 16 to 28 % of read positions meet that gap test, so a random
   multi-frame event would often pass.
   - A1: both gap-only clusters have every skip at 48 n + 12. B CRF has none.
6. **A multi-frame listener step within 300 ms of a capture loss.** It joins
   that loss's cluster, and the rise test applies to the cluster's net step,
   within 1 ms + 2 % of the loss: about 249 ms at A1's 12.4 s loss. A one-frame
   event never joins a cluster.
   - A1 and B CRF: the per-step sizes of item 1 exclude it. Every member step
     is 48 n + 12, an exact stale-replay edge, or the 12.4 s loss's own 18,626
     frames, the only step in its cluster.

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

The floor itself was checked without the tool. The loop is exactly periodic,
so a 48,000-point DFT of it has no leakage. Its band, 20 Hz to 20 kHz, gives
the same THD+N and SNR as the tool for both tones within 0.0001 dB. The
analytic floor of a -1 dBFS tone over 24-bit rounding in that band is
-146.05 dB. The controls compare blocks with the tool's own floor, so they
alone would pass a 3 dB error in the band computation. Against these two
checks it would show as 3 dB.

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

The beat comb's members sit within 1.82 frames of its line in every case. Its
rate, 0.5107 per second at 48 kHz, matches the DUT's own `SLIP_TDM` count
within 0.3 %.
Teeth missing from the comb fall inside capture-path losses.

**A0.** The peer, on its INTERNAL source, drops one frame every 1.21 s on
average. The 519 drops are 17.2 ppm of the window, and 17.1 ppm net of the one
silent insert, the figure in the verdict table. The DUT's beat adds one frame
every 1.958 s: 10.6 ppm. Net, McASP0 runs +6.52 ppm off the peer's output,
against +6.44 +-0.72 ppm timed. Lane B5
([PR #628](https://github.com/kebag-logic/milan-fpga/pull/628)) measured
16.46 ppm of drops at the peer's output and the same beat. The
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
audio MMCM clock by 512 (`hdl/ieee1722/crf/KL_crf_tx.sv`, its header from line
20, and the port contract at `hdl/milan/milan_datapath.sv:445`): the physical
sample grid, 47,999.4893 Hz nominal. The AAF talker's packet grid is the
free-running 48,000.0000 Hz NCO. The two are 10.64 ppm apart, the beat
([TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff)). A listener
that follows the DUT's CRF therefore receives the DUT's AAF stream 10.64 ppm
fast and must drop one frame per beat. The DUT's own talker beat already
repeats one, so the pair nets to zero but leaves two discontinuities per beat.
Under CRF selection the DUT aligns the packet grid to the physical grid, as the
B CRF case shows. This disagreement is therefore specific to INTERNAL.

A2's root cause is tracked on #74, "Media clock: select CRF and align the
audio grid", where this measurement is recorded
([#74 comment](https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5932380322)).

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
ACQUIRE 3.3 s after the set and LOCKED 6.5 s after it. It read LOCKED at all
three reads in the window, 5 s, 315 s and 615 s in, while `SLIP_TDM` stayed
static. Its trim, -6.0 ppm, cancels the +6 ppm the control
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
  1 ms + 2 %, except two kinds of cluster. Where the rise is unmeasurable, the
  cluster passed on the read gap alone, the gap-only branch: 1 in A0, 2 in A1,
  5 in A2, 3 in B INTERNAL and none in B CRF. Every skip in these eleven is
  still 48 n + 12. In two A2 clusters a rise was measured and does not match:
  154.5 ms for a 60-frame loss, and -155.8 ms for a 1,020-frame loss just after
  the 13.3 s stall (clusters 17 and 56 in its `grade.json`). These two passed
  on the read gap and size rule, item 3 of
  [Method](#method), "What the attribution can absorb".
- 255 of the 265 skips in clusters with a matching rise are 48 n + 12 frames.
  Of the other ten, two are losses longer than a loop and four are the edges of
  stale replays (next item). Two are parts of a cluster whose total is
  48 n + 12. Two are one frame off the pattern, at 48 n + 13: A0's 1,165-frame
  skip, and a 109-frame skip in an A2 stale-replay cluster. Each may hold a
  one-frame listener drop merged with a capture loss. So A0's 519 and A2's 494
  listener drops may each be one low, and each counted ratio about 0.03 ppm
  low.
- Five clusters also replayed stale audio from about one capture buffer, 24,000
  frames, back: one run of 6 frames in A1, runs of 1 and 2 frames and one
  step back and forth in A2, and in B CRF one cluster that stepped back 24,000
  frames twice. With whole loops added where the rise asks for them, each
  cluster's net step matches its read-time rise.
- A loss longer than the loop hides any event inside it. That is why the beat
  combs miss a few teeth.
- One-frame listener events show no read-time rise. A rise is measurable where
  at least three reads separate the event from each neighbouring event: for
  497 of A0's 520 listener events, 135 of A2's 674 and 485 of B INTERNAL's
  507. A2's other 539 sit too close to a neighbour. In each of those cases the
  median is 0.00 ms and the largest magnitude 1.0 ms, the host's USB frame
  step, with no exception. A1 and B CRF have no listener event.
- The DUT's one-frame beat repeats behave the same, measurable for 300 of 321
  in A0, 312 of 315 in A1, 313 of 316 in A2 and 303 of 322 in B INTERNAL. The
  two exceptions, 2.7 ms and 177 ms, are A2 beat repeats within 0.4 s of its
  13.3 s stall.

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
- The attribution can absorb a listener event in six ways; see
  [Method](#method), "What the attribution can absorb". The checks there
  exclude each in A1 and B CRF, except a one-frame drop at the very edge of
  A1's 12.4 s loss, which lost audio would hide anyway. In A0 and A2 one skip
  each is 48 n + 13, so their listener drop counts may each be one low.
- The timed ratio depends on the bench host's read-time floor. Its interval
  is wide where the capture stalled for seconds (A1, A2).
- The A2 diagnosis rests on the measured rates and on the code and design
  reference cited. No CRF timestamp was captured on the wire. Its root cause
  is tracked on #74.
- In B CRF the servo's status carried bit 4, DRP config mismatch, from ACQUIRE
  on. It was observed and not analysed. It is recorded on #74
  ([comment](https://github.com/kebag-logic/milan-fpga/issues/74#issuecomment-5932538721))
  for when that issue is worked.
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

**Where the packet is.** It is published on branch `b6-review-evidence`, pinned
at commit `422dcf91008a09cb882dcc2b760779ce22e530cd`. The packet label
`b6-a477` maps to `review-evidence/b6-r1/author/` there: `summary/a1/grade.json`
is `review-evidence/b6-r1/author/summary/a1/grade.json`. The archive masks
labels in some files. For the twelve label-masked files below (each
`grade.json`, each graded case's `events.jsonl`, `grade_b6.py` and
`run_b6.py`) the hash is the unmasked original's. It is recorded as
`original_sha256` in `review-evidence/b6-r1/MANIFEST.json`, beside the
published file's `published_sha256`. The raw files' hashes are in the packet's
`RAW-ARTIFACTS.json`.

The round-2 packet, `b6-a480`, is `review-evidence/b6-r1/author-r2/` at the
same commit. Its `floor_check.py` repeats the floor check in
[Tool controls](#tool-controls) from the archive alone. Its
`attribution_checks.py` and receipt hold the checks of items 1 to 5 in "What
the attribution can absorb", including the gap share of item 5. That tool reads
the raw files, which stay on the bench host, and its receipt records their
hashes.

Two commands reproduce the tone loop and the tool controls from the archive.
Run them in a fresh clone or a disposable worktree: the checkout writes the
archive into the working tree and stages it.

```sh
git fetch origin b6-review-evidence
git checkout 422dcf91008a09cb882dcc2b760779ce22e530cd -- review-evidence/b6-r1
cd review-evidence/b6-r1/author/tools
python3 b6_tone.py /tmp/b6-loop.bin && sha256sum /tmp/b6-loop.bin   # the page's tone-loop hash, 566d3dfa...
python3 b6_thdn.py controls /tmp/b6-controls.json && cmp /tmp/b6-controls.json ../controls/controls.json
```

Both exit 0. The first prints the tone loop's hash in the table above, and
`cmp` is silent. They were reproduced at this pin with Python 3.14.7 and NumPy
2.5.3. The versions of the original run were not recorded.

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

## Dev bbf704ec, 2026-10-03: lane B7

Refs #629. Operator [A519], 2026-10-03, under the
[bench lane B7 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5969106115).
The image is the manager's build of dev
`bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`, which merged
[PR #634](https://github.com/kebag-logic/milan-fpga/pull/634): AAF following
through the AAF clock meter, and the grid aligner engaged at INTERNAL (D4 =
A2-a). It was flashed at 13:16 CEST and cold-booted at 14:20 CEST. The bench,
the tone, the tools and the grading rules are lane B6's above, with the changes
in [B7: method changes](#b7-method-changes).

| #629 bench item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `bbf704ec` | PASS | CRCs and live descriptors equal the build's; the clock sources of #629. See [B7: identity and setup](#b7-identity-and-setup) |
| Analysis tool, synthetic controls | PASS | Re-run, byte-equal to lane B6's. See [B7: tool controls](#b7-tool-controls) |
| Format check before every bind | Held | Every listener took the talker's format and read it back; no talker format was set |
| Clock source set on the listener only, read back, restored | Held | Four sets, each read back equal and restored as found. See [B7: binding rule and clock-source record](#b7-binding-rule-and-clock-source-record) |
| A0, the peer on INTERNAL (control) | PASS as a control | 470 one-frame drops and 291 silent inserts by the peer: net +5.92 ppm. The DUT's beat is gone |
| A1, the peer following the DUT's AAF stream | PASS | 0 listener discontinuities in 629.9 s; counted ratio 0 |
| A2, the peer following the DUT's CRF stream | PASS | 0 listener discontinuities in 628.0 s, where lane B6 found 494 drops and 180 inserts. Two capture-path clusters are disclosed in [B7: the capture path and what it can absorb](#b7-the-capture-path-and-what-it-can-absorb) |
| B0, the DUT on INTERNAL with both of the peer's talkers bound (control) | PASS as a control | The DUT's TDM clock runs +5.92 ppm off the peer's output, counted; +5.62 +-0.44 ppm timed |
| B-CRF, the DUT following the peer's CRF stream | PASS | Servo LOCKED 3.1 to 3.6 s after the set and at every read; 0 net steps in 30,169,440 frames |
| B-AAF, the DUT following the peer's AAF stream | PASS | Servo LOCKED 6.6 to 7.1 s after the set and at every read; 0 net steps in 30,131,520 frames; the meter's history never restarted. Three capture-path clusters are disclosed |
| B, THD+N of a known signal from the peer's talker | NOT RUN | The known-signal probe was repeated: the peer's talker channels carry -2 to 0 LSB. See [B7: Direction B](#b7-direction-b) |
| (a) Lock loss of the followed AAF stream | Observed as declared | HOLDOVER within 0.56 s, the index kept, one `mr` toggle at the loss and none at the return, LOCKED 6.1 s after the return. See [B7: lock loss of the followed AAF stream](#b7-lock-loss-of-the-followed-aaf-stream) |
| (b) The DUT's INTERNAL media clock | Observed | +5.92 ppm from the reference peer; about -5.1 ppm against gPTP time. See [B7: the DUT's INTERNAL media clock](#b7-the-duts-internal-media-clock) |
| Restore | Done | Every clock source, format, binding and map read back as found. See [B7: bench as left](#b7-bench-as-left) |

These are operator observations, not review verdicts. The judgement of each
#629 acceptance item is in [B7: #629 acceptance](#b7-629-acceptance).

### B7: identity and setup

The gate compares the DUT with the build's own outputs: its AEM image, its BIOS
and its bitstream payload.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM image CRC32, 7,512 bytes | `5ba355eb`, the build's `aem_desc.bin` (SHA-256 `4fc8d615...`) |
| BIOS ROM CRC32, 53,588 bytes | `2144df1c`, the build's BIOS |
| QSPI bitstream payload CRC32, 3,825,788 bytes | `e6b8febc`, the build's payload (SHA-256 `d1386b86...`) |
| Live descriptors over AECP | ENTITY, CONFIGURATION, STREAM_INPUT 0 and 1, STREAM_OUTPUT 0 and 1, AVB_INTERFACE 0, CLOCK_SOURCE 0 to 2 and CLOCK_DOMAIN 0, each byte-equal to the build's AEM image; entity model `001bc5c1935893e1` |
| Clock sources of #629 | CLOCK_SOURCE 0 INTERNAL; 1 INPUT_STREAM on STREAM_INPUT 1, the CRF input; 2 INPUT_STREAM on STREAM_INPUT 0, the AAF input. CLOCK_SOURCE 3 answers NO_SUCH_DESCRIPTOR. CLOCK_DOMAIN 0 lists 0, 1 and 2 and reads 0 |
| UART grader | 10 of 10 |
| Identity gate | PASS |

As found:

- **DUT.** Both NVM slots `VD_SHAPE`, seq 0, 0 commits: the new image refused
  the earlier saved state once at its first boot, as the design's
  [Limits](../design/MEDIA_CLOCK_FOLLOWING.md#limits) state. All stream states
  unbound, both audio maps empty, CLOCK_DOMAIN 0 on INTERNAL. `MCSRV_STAT`
  read IDLE, the AAF meter words 0 and `SLIP_TDM` 0.
- **Reference peer.** Every stream state unbound, its CLOCK_DOMAIN on its
  INTERNAL source, its clock sources on its AAF and CRF inputs as in lane B6.
- **SoC board.** The same boot as lane B6 left it, both bridge legs running
  with the bridge script's command lines and the USB function configured. Its
  console stood at a root prompt; `id` confirmed it, and no other process held
  the console. No credential was typed or stored.
- **Controller host.** No gPTP daemon, no staging.

### B7: method changes

Each change was fixed at 14:50 CEST, before any graded case ran.

| Change | Reason |
|---|---|
| B0 binds both of the peer's talkers: its CRF to the DUT's STREAM_INPUT 1 and its AAF to STREAM_INPUT 0, with the DUT on INTERNAL | One control for both following cases (lane B6's B INTERNAL bound the CRF only) |
| B-AAF binds the peer's AAF talker to the DUT's STREAM_INPUT 0 and sets the DUT's CLOCK_DOMAIN to CLOCK_SOURCE 2 (D1 = L1) | The case #634 adds |
| A0 passes as a control when the listener's net rate is beyond 2 ppm | Lane B6 asked for about 16 ppm. Under A2-a the DUT's stream runs on its physical clock, about 6 ppm from the peer |
| A one-frame repeat counts as the DUT's beat only while the DUT's `SLIP_TDM` moves in the window | Lane B6 used `SLIP_TDM` as a cross-check only. With it static every repeat is the listener's, so the change can only make a verdict stricter |
| B-AAF adds the design's [bench row](../design/MEDIA_CLOCK_FOLLOWING.md#bench): LOCKED within 15 s of the set and at every read, the CLOCK_DOMAIN counters unchanged in the window, `SLIP_TDM` static, and the meter's history-restart count unchanged | The design's pass criteria for the case |
| The DUT's words (servo, AAF meter, CRF sink, slip counters) are read every 30 s through each window, and both entities' GET_COUNTERS at three marks | The servo state through the window |
| A console poll of two words every 0.5 s times the set to LOCKED | The time from the set to LOCKED |
| The B-AAF lock-loss observation runs after the window, with the capture still running | Assignment item (a) |
| The grade's `tone.repeats` and `tone.repeated_frames` no longer subtract the silent inserts twice | A lane B6 summary slip: its A2 `grade.json` reads 139 repeats for 319 less 180. No attribution or verdict used the two fields |

Unchanged: the tone, the decode, the block metrics, the attribution rules with
lane B6's refinements, the frame-rate ratio and the restore. Each window is
630 s, untouched, from 20 s after the last bind or clock-source set and, where
the DUT follows, after its servo first reads LOCKED. Each case ran as one
locked action with a hard deadline: 1,100 s, and 1,300 s and 1,500 s for B-CRF
and B-AAF.

The SoC board's two bridge legs were stopped by process ID before the cases and
restarted with the recorded command lines at the end, as in lane B6. A B-AAF
shakedown with a 60 s window preceded the cases and is not graded. It ran every
new step, then restored everything and read it back.

### B7: tool controls

`b6_thdn.py controls` was re-run on the bench host before any case. Its output
is byte-equal to lane B6's `controls.json`, SHA-256 `7bbefc71...`. Every row of
[Tool controls](#tool-controls) therefore holds here: a clean tone at the floor,
one dropped and one repeated frame found at the planted frame, and 16 ppm and
1 ppm found both as a resampled rate and as slips. The tone loop's SHA-256 is
again `566d3dfa...`.

### B7: binding rule and clock-source record

| Bind or set | Talker format | Listener format read | Set on the listener | Read back |
|---|---|---|---|---|
| DUT AAF to peer STREAM_INPUT 0, every case | `0205022002006000` | `0205022001006000` | `0205022002006000`, SUCCESS | `0205022002006000` |
| DUT CRF to peer, A2 | `041060010000bb80` | `041060010000bb80` | None, equal | `041060010000bb80` |
| Peer CRF to DUT STREAM_INPUT 1, B0 and B-CRF | `041060010000bb80` | `041060010000bb80` | None, equal | `041060010000bb80` |
| Peer AAF to DUT STREAM_INPUT 0, B0, B-AAF and the probe | `0205022001006000` | `0205022002006000` | `0205022001006000`, SUCCESS | `0205022001006000` |
| Peer AAF to DUT STREAM_INPUT 0, the B-AAF rebind | `0205022001006000` | `0205022001006000` | None, equal | `0205022001006000` |
| A1: the peer's CLOCK_DOMAIN to its source on its AAF input | - | - | SET_CLOCK_SOURCE SUCCESS | Equal to the set index |
| A2: the peer's CLOCK_DOMAIN to its source on its CRF input | - | - | SET_CLOCK_SOURCE SUCCESS | Equal to the set index |
| B-CRF: the DUT's CLOCK_DOMAIN 0 to CLOCK_SOURCE 1 | - | - | SET_CLOCK_SOURCE SUCCESS | 1 |
| B-AAF: the DUT's CLOCK_DOMAIN 0 to CLOCK_SOURCE 2 | - | - | SET_CLOCK_SOURCE SUCCESS | 2 |

Every bind answered SUCCESS with connection count 1, and every unbind
connection count 0. Each case ended with its clock source set back to INTERNAL
and read back: the peer's in A1 and A2, the DUT's in B-CRF and B-AAF. Every
listener format the method set was restored and read back: the peer's
STREAM_INPUT 0 to `0205022001006000` and the DUT's to `0205022002006000`.

### B7: Direction A

`b7_tables.py` renders the tables below from the grades.

<!-- b7-thdn-a -->
| Case | Tone | Blocks | Blocks at the floor | THD+N there, dB (median / worst) | SNR there, dB (median / worst) | Worst THD+N, a block with a listener discontinuity, dB | Worst THD+N, all blocks, dB |
|---|---|---|---|---|---|---|---|
| A0 | 997 Hz | 630 | 444 | -146.06 / -146.06 | 146.07 / 146.07 | -7.19 | -2.22 |
| A0 | 9,973 Hz | 630 | 444 | -145.99 / -145.99 | 145.99 / 145.99 | +1.01 | +23.84 |
| A1 | 997 Hz | 629 | 597 | -146.06 / -146.06 | 146.07 / 146.07 | None | +12.71 |
| A1 | 9,973 Hz | 629 | 597 | -145.99 / -145.99 | 145.99 / 145.99 | None | +21.58 |
| A2 | 997 Hz | 628 | 578 | -146.06 / -146.06 | 146.07 / 146.07 | None | +13.23 |
| A2 | 9,973 Hz | 628 | 578 | -145.99 / -145.99 | 145.99 / 145.99 | None | +19.67 |

<!-- b7-offset-a -->
| Case | Fitted offset, blocks at the floor, ppm (largest magnitude, either tone) | Listener drops | Listener silent inserts | DUT beat repeats | Tone offset, listener only, ppm | Counted McASP0 to peer ratio, ppm |
|---|---|---|---|---|---|---|
| A0 | 2.7e-7 | 470 | 291 | 0 | +5.916 | +5.916 |
| A1 | 2.3e-7 | 0 | 0 | 0 | 0 | 0 (1 frame = 0.033) |
| A2 | 2.1e-7 | 0 | 0 | 0 | 0 | 0 (1 frame = 0.033) |

<!-- b7-discontinuities-a -->
| Case | Window start, CEST | Window of captured audio, s | DUT `SLIP_TDM` in the window | Capture-path losses: events, clusters, frames | Torn frames | Timed ratio, ppm (95 % half-width) | Result |
|---|---|---|---|---|---|---|---|
| A0 | 14:42:08 | 630.31 | 0 in 600 s | 15, 7, 5,058 | 0 | +5.71 (+-0.55) | PASS as a control |
| A1 | 14:53:19 | 629.88 | 0 in 600 s | 37, 32, 5,580 | 0 | -0.28 (+-1.40) | PASS |
| A2 | 15:04:29 | 628.04 | 0 in 600 s | 62, 53, 112,533 | 0 | +2.15 (+-4.42) | PASS |

A block at the floor holds no discontinuity and no undecodable frame. Its THD+N
equals the loop's floor within 0.0006 dB in every case. A positive THD+N is a
block that holds a capture-path loss.

**The DUT's beat is gone.** In every case the DUT's `SLIP_TDM` stayed static
through the window and no one-frame repeat occurred. Lane B6 found 315 to 322
beat repeats per window, one per 1.958 s. Under D4 = A2-a the DUT's AAF stream
runs on its physical audio clock at INTERNAL too.

**A0.** On its INTERNAL source the peer drops 470 frames and inserts 291 silent
ones: net +5.92 ppm, equal to the counted ratio, +5.71 +-0.55 ppm timed. That
is the DUT's physical clock against the peer's, with no beat on top. The metric
shows the mismatch: 186 of 630 blocks leave the floor.

**A1.** Following the DUT's AAF stream, the peer drops and repeats nothing.
McASP0 and the peer's output advance frame for frame: 0 net steps in
30,234,240 captured frames, where lane B6 counted -10.63 ppm, the beat. Every
block without a capture-path loss is at the floor.

**A2.** Following the DUT's CRF stream, the peer drops and repeats nothing
either: 0 listener discontinuities and 0 net steps in 30,145,920 frames. Lane
B6's A2 failed with 494 drops and 180 inserts, because at INTERNAL the DUT's
CRF output and AAF stream ran 10.64 ppm apart. With A2-a they are one clock.
Two capture-path clusters in this window are one and two frames off the
size signature; see
[B7: the capture path and what it can absorb](#b7-the-capture-path-and-what-it-can-absorb).
The DUT's CRF output counted one MEDIA_RESET right after its stream started,
with no source change, and none through the window. It is recorded, not
analysed.

### B7: Direction B

**Known-signal probe.** Lane B6's probe was repeated after the cases, with its
method unchanged: the DUT's STREAM_INPUT 0 took the peer talker's format, four
identity mappings, the bind, and 2 s of the DUT's TDM output reduced on the
SoC board. The peer's talker channels carry -2 to 0 LSB (mean square 0.49 to
0.54), and the unmapped channels 4 to 7 carry zero. That is lane B6's idle
floor again, not a known signal. Direction B is therefore graded by the
frame-rate ratio and the tone path, as in lane B6, and its THD+N is NOT RUN.

<!-- b7-ratio-b -->
| Case | Window start, CEST | Counted ratio, ppm | Timed ratio, ppm (95 % half-width) | Window halves, timed, ppm | Listener discontinuities | Blocks at the floor | `SLIP_TDM` in the window | Result |
|---|---|---|---|---|---|---|---|---|
| B0 | 15:15:42 | +5.924 | +5.62 (+-0.44) | +5.67 / +5.81 | 457 drops, 278 silent inserts | 434 of 629 | 0 in 600 s | PASS as a control |
| B-CRF | 15:26:55 | 0 (0 net steps in 30,169,440 frames) | +1.98 (+-6.52) | -0.60 / +9.14 | 0 | 559 of 628 | 0 in 600 s | PASS |
| B-AAF | 15:38:07 | 0 (0 net steps in 30,131,520 frames) | -1.49 (+-11.64) | +0.16 / -22.60 | 0 | 564 of 627 | 0 in 600 s | PASS |

<!-- b7-servo-b -->
| Case | Servo at the 21 reads in the window | Trim, ppm | Set to LOCKED, s | AAF meter at every read | Meter rate, ppm | Meter history restarts | Meter largest deviation, ns | CRF sink rate, ppm | CLOCK_DOMAIN LOCKED/UNLOCKED, window start and end |
|---|---|---|---|---|---|---|---|---|---|
| B0 | IDLE | 0 | - | Not selected | - | - | - | +11.025 to +11.057 | 3/2, 3/2 |
| B-CRF | LOCKED | -6.00 to -5.94 | 3.1 to 3.6 | Not selected | - | - | - | +11.008 to +11.057 | 4/3, 4/3 |
| B-AAF | LOCKED | -6.00 to -5.94 | 6.6 to 7.1 | Locked, rate valid | +11.018 to +11.043 | 0, 0 | 29 | - | 5/4, 5/4 |

The set-to-LOCKED time lies between the last poll that did not read LOCKED and
the first that did, 0.5 s apart. A rate is the talker's media clock against
gPTP time, in ns of error per 512 ms; positive means the talker's clock is slow
([0x8E0](../reference/REGISTER_MAP.md#0x8e0-----aaf-clock-meter--629-kl_aaf_clock_meter)).

**B0.** With the DUT on INTERNAL its TDM clock runs +5.92 ppm off the peer's
output, counted, as in A0. The DUT's CRF sink locked on the peer's CRF, but the
servo stayed IDLE: binding a stream does not move the DUT's clock. The DUT's own
listener shows the same mismatch. Its loopback ring, fed by the peer's 4-channel
AAF stream, counted 342 dups (`SLIP_LB`) in 600 s. At one dup per channel pair
per slipped frame that is 171 frames, +5.94 ppm.

**B-CRF.** SET_CLOCK_SOURCE 1 answered SUCCESS and read back 1. The servo read
ACQUIRE within 0.6 s and LOCKED 3.1 to 3.6 s after the set, and LOCKED at all
21 reads in the window, with trim -6.0 ppm. McASP0 and the peer's output
advanced frame for frame over the window, and the peer's listener on its own
clock drops and repeats nothing. This repeats lane B6's B CRF.

**B-AAF.** SET_CLOCK_SOURCE 2 answered SUCCESS and read back 2. The meter
locked within 0.6 s of the set, its rate was valid 4.1 to 4.6 s after it
(E8's 4.096 s), and the servo read LOCKED 6.6 to 7.1 s after it, inside the
design's 15 s. Through the window:

- the servo read LOCKED at all 21 reads, with trim -6.0 ppm, which cancels the
  +5.92 ppm the controls measured;
- the CLOCK_DOMAIN's LOCKED and UNLOCKED counters did not move, so the servo
  never left LOCKED between reads (D5 = C1);
- the meter stayed locked with a valid rate, its history never restarted, and
  the peer's timestamps deviated from their group's first by at most 29 ns;
- 0 net steps in 30,131,520 frames, 0 listener discontinuities and
  `SLIP_TDM` static.

The meter's rate, +11.02 to +11.04 ppm, equals the CRF sink's measurement of
the same peer in B0 and B-CRF within 0.05 ppm, and the trim equals B-CRF's.

The timed ratio's interval is wide in B-CRF and B-AAF, where the external
capture's reads stalled for up to 883 ms and 1.2 s. The counted ratio does not
depend on read times.

**The DUT's listener ring, outside the criteria.** In B-AAF the loopback ring's
`SLIP_LB` counted 2 dups, one slipped frame, between 1 s and 31 s into the
window, 14 to 45 s after the servo first read LOCKED. It then held for 570 s.
It also counted 6 between the set and the window and 2 across the lock-loss
observation. The servo locks frequency only, and nothing aligns the phase
([#632](https://github.com/kebag-logic/milan-fpga/issues/632)). This one slip
after lock is recorded here, not analysed.

### B7: lock loss of the followed AAF stream

After B-AAF's window the peer's AAF talker was unbound from the DUT's
STREAM_INPUT 0, which held it for 11.1 s, and then rebound under the binding
rule. A console poll read the servo and the meter every 0.5 s from 1.5 s
before the unbind to 10 s after the servo read LOCKED again. The external
capture kept recording the tone path. The declared behaviour is the design's
[Lock loss, holdover and restart](../design/MEDIA_CLOCK_FOLLOWING.md#lock-loss-holdover-and-restart)
and [`mr`](../design/MEDIA_CLOCK_FOLLOWING.md#mr).

| Event | Seconds after it | Observed | Declared |
|---|---|---|---|
| Unbind | 0.06 to 0.56 | Servo HOLDOVER, trim held at -5.94 ppm; meter unlocked, rate invalid | Lock falls 100 ms after the last PDU; HOLDOVER with the trim frozen |
| Through the holdover | to 11.1 | HOLDOVER; GET_CLOCK_SOURCE 2 | No timeout, no fallback; the index unchanged |
| Rebind | 0.05 to 0.55 | Meter locked; servo ACQUIRE | The meter locks after 8 PDUs; the servo re-enters ACQUIRE |
| Rebind | 4.07 to 4.58 | Meter rate valid | Valid 4.096 s after the restart (E8) |
| Rebind | 5.58 to 6.08 | Servo LOCKED, trim -5.94 ppm; GET_CLOCK_SOURCE 2 | LOCKED after four windows within 2 ppm |

| Counter | Before the unbind | In the holdover | After LOCKED again | Declared |
|---|---|---|---|---|
| DUT STREAM_OUTPUT 0 (AAF) MEDIA_RESET | 1 | 2 | 2 | One `mr` toggle per disruption, none on the return |
| Peer STREAM_INPUT 0 MEDIA_RESET (the toggle as received) | 1 | 2 | 2 | As above |
| DUT CLOCK_DOMAIN 0 LOCKED / UNLOCKED | 5 / 4 | 5 / 5 | 6 / 5 | C1: UNLOCKED as the servo leaves LOCKED, LOCKED when it reads LOCKED again; LOCKED is UNLOCKED or UNLOCKED + 1 |
| DUT STREAM_INPUT 0 MEDIA_UNLOCKED | 0 | 1 | Bank reset at the bind | The Stream Input's MEDIA_UNLOCKED |

The 1 before the unbind is the toggle of the set to CLOCK_SOURCE 2: the DUT's
AAF output counts MEDIA_RESET from its own stream start, and it read 1 at every
mark of the window. The DUT's CRF output was not bound in B-AAF and counted
nothing. The tone path through the whole observation, 30.0 s graded as a
segment, has no discontinuity of any kind and 0 net steps: the holdover kept
the DUT's clock on the peer's rate. The observation covers the AAF source; a
lock loss of a followed CRF stream was not run.

### B7: the DUT's INTERNAL media clock

The owner's A2-a decision asks for this unit's INTERNAL media clock against
Milan v1.2 7.4's +-50 ppm, as an observation
([decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5937848189)).
Under A2-a the INTERNAL media clock is the DUT's physical audio clock, which
McASP0 follows.

| Reference | Offset of the DUT's INTERNAL media clock | Basis |
|---|---|---|
| The reference peer's media clock | +5.92 ppm (A0 +5.916, B0 +5.924 counted; +5.71 +-0.55 and +5.62 +-0.44 timed) | Frame-rate ratio of two hardware-clocked captures |
| gPTP time | about -5.1 ppm | The peer's media clock is 11.02 to 11.06 ppm slow against gPTP (the DUT's CRF sink and AAF meter), and the DUT runs 5.92 ppm faster than the peer |

Both are inside +-50 ppm. Neither reference is a calibrated frequency
standard, and nothing here measures the board oscillator's grade, which stays
the owner's known risk: under A2-a, Milan v1.2 7.4's +-50 ppm holds at INTERNAL
only for an oscillator grade of +-39 ppm or better, and the grade is assumed,
not confirmed ([Limits](../design/MEDIA_CLOCK_FOLLOWING.md#limits)). Lane B6's
beat, two days earlier, put the same clock about -10.6 ppm from gPTP time
then, and the peer about -17.1 ppm. Both moved by about 6 ppm against gPTP
time, so the change lies in the gPTP time base, not in the DUT.

### B7: the capture path and what it can absorb

| Case | Capture reads in the window | Read stalls over 15 ms | Capture-path clusters | Frames lost | Longest read stall | Clusters off the 48 n + 12 signature |
|---|---|---|---|---|---|---|
| A0 | 63,027 | 10 | 7 | 5,058 | 75 ms | 1, 18 frames off |
| A1 | 62,970 | 42 | 32 | 5,580 | 76 ms | 0 |
| A2 | 62,745 | 79 | 53 | 112,533 | 2.15 s | 2: -2 frames (a 2.1 s loss), -1 frame (a 215-frame cluster) |
| B0 | 62,860 | 66 | 19 | 22,404 | 209 ms | 0 |
| B-CRF | 62,699 | 130 | 69 | 74,568 | 883 ms | 0 |
| B-AAF | 62,642 | 112 | 65 | 115,701 | 1.2 s | 3: -1 frame each (a 1.2 s loss, a 155-frame and a 4,331-frame skip) |

Every capture-path cluster in every case passed on a measured read-time rise
that matches its loss within 1 ms + 2 %. None passed on the read gap alone or on
the read gap and size rule, and no multi-frame step stayed outside the capture
path.

`b7_absorb.py` repeats lane B6's six checks of
[Method](#method), "What the attribution can absorb", for every case:

1. **A one- or two-frame listener event merged with a capture loss.** A1, B0
   and B-CRF have none. A2 has two clusters and B-AAF three whose net loss is
   one or two frames short of the 48 n + 12 signature; each could hold a merged
   listener repeat. The conservative reading counts them as listener events:
   A2 would then hold 2 and B-AAF 3 in their windows, and both would fail.
   Two observations argue against it. First, a capture stall on the bench host
   cannot make the peer repeat a frame, and the visible audio, about 627 s in
   each case, holds no listener event at all. Second, every off-signature
   cluster is short, the direction of the capture's own drift: it delivers
   0.54 to 0.84 frames per second fewer than 48 kHz on the bench host's clock,
   so its packets are shortened by a frame about once a second.
2. **A repeat within 50 frames of a beat tooth.** No case attributes any event
   to the DUT's beat.
3. **The read gap and size branch.** No cluster passed on it.
4. **Skips of 2 to 48 frames.** None in any case. The smallest capture-path loss
   is 60 frames. Each of the 47 such clusters has a measured rise of 0.97 to
   2.01 ms after a read gap of 10.7 ms or more.
5. **The gap-only branch.** No cluster passed on it.
6. **A multi-frame listener step within a cluster.** Every member step is
   48 n + 12, one of the off-signature steps of item 1, or a single loss longer
   than half the loop that shows as a step back: 677 ms in B-CRF and 671 ms in
   B-AAF, each 48 n + 12 once the whole loop is added.

A0's one off-signature cluster, 18 frames short over five skips, is a control
and changes no verdict.

### B7: bench as left

| State | As left |
|---|---|
| DUT stream state | All unbound; both audio maps empty, read back |
| DUT clock domain | CLOCK_SOURCE 0, read back |
| DUT STREAM_INPUT 0 format | `0205022002006000`, as found, read back |
| Reference peer | Its CLOCK_DOMAIN on INTERNAL and its STREAM_INPUT 0 format `0205022001006000`, both read back after every run; every stream unbound |
| Census, start against end | 45 of 46 entries equal; the other is the DUT's live propagation delay |
| DUT saved state | NVM from `VD_SHAPE` seq 0 to slots seq 17 and 16, `VD_OK`; 17 commits, 0 failed, `pend=1` |
| SoC board | Same boot; both bridge legs running with the script's command lines under new process IDs; PCM states, USB function and fault scan as at the start; no task file left |
| Controller host | No task process; staging removed |
| Bench host | Both USB audio devices present; the board link's address present; the bench lock free |

Residuals that no permitted command restores:

- **DUT NVM persistence** advanced through the method's format, map and
  clock-source edits: 17 commits on the new image's first saved state.
- **DUT counters** that clear only on reset moved: `SLIP_LB`, `RENDER_STAT`,
  the CRF sink's `CRF_RATE` and `CRF_STATUS`, and `AAFM_RATE`, which hold their
  last values.

### B7: #629 acceptance

Each item of #629 is judged against the evidence named. Only the bench items
rest on this lane's measurements.

| #629 item | Judgement | Evidence |
|---|---|---|
| Requirements: FR-CLK-03, FR-CLK-04 and the #389 record amended | Met | [`FR_NFR.md:156`](../reference/FR_NFR.md) records #389 as reversed by #629; `:238` and `:239` state the selectable set, AAF recovery and the holdover without fallback |
| Model and builder: one INPUT_STREAM source per AAF Stream Input beside INTERNAL and CRF, all listed, exactly one selected | Met on this image | The identity gate: three sources in D1 order, the domain lists 0 to 2, GET_CLOCK_SOURCE answers one index. The builder's gate 33 (`sw/builder/test_builder.py`) grades every shipping configuration; only the AX7101 1x1 TDM8 shape ran on the bench |
| Fabric: recover the media clock from the selected AAF stream through the CRF servo path; gated on the live selection; a switch re-locks with no undeclared discontinuity | Met for recovery and gating; the stream-to-stream switch not run at the bench | B-AAF: the servo LOCKED with trim -6.0 ppm and 0 net steps. The meter reads enabled only while CLOCK_SOURCE 2 is selected: 0 at every read of the other five cases. Each set from INTERNAL to the CRF or the AAF source toggled the DUT's AAF output's `mr` once: its MEDIA_RESET read 1 at every mark of B-CRF and B-AAF, and 0 in the cases without a DUT set. A switch between the AAF and CRF streams, the design's "Switch" bench row, was not in this assignment; it is graded in simulation only (`tb/verilator/milan_dp_mclk`) |
| Lock loss: declared holdover and restart, and `mr` per IEEE 1722-2016 4.4.4.3 | Met for the AAF source | [B7: lock loss of the followed AAF stream](#b7-lock-loss-of-the-followed-aaf-stream). A followed CRF stream's loss was not run at the bench |
| Protocol processor: SET/GET_CLOCK_SOURCE over the longer list, the selection kept as saved state | Met in part at the bench | SET_CLOCK_SOURCE 1 and 2 answered SUCCESS and read back; CLOCK_SOURCE 3 does not exist. The NVM committed 17 times over the method's changes. Restoring the saved index across a power cycle needs a power cycle, which this lane may not do; processor PR 142 grades it as D3C3 (pin `631eeb34`) |
| Simulation: each source in turn; the clock follows within tolerance; switching and lock loss graded by failing mutants | Met by the merged PR's evidence, not re-run here | `tb/verilator/aaf_clock_meter` and `tb/verilator/milan_dp_mclk` with their mutant lists; PR #634's hosted checks, `verilator-suites`, `rtl-fast` and `yosys-portability` among them, all SUCCESS at its head `2bc5adc0` |
| Bench, both directions, each followed source: the listener's CLOCK_DOMAIN set and read back, its format adapted, the as-found source restored | Met | A1, A2, B-CRF and B-AAF; [B7: binding rule and clock-source record](#b7-binding-rule-and-clock-source-record) |
| Bench quality metric: THD+N and SNR of a known tone on the selected path, against the INTERNAL control and synthetic slips and drift | Met for Direction A; NOT met for Direction B | Direction A: A0 shows the mismatch, A1 and A2 sit at the floor, and the controls are byte-equal to lane B6's. Direction B: no known signal reaches the peer's talker without a wiring change, so the DUT's selected path carries no known tone; the frame-rate ratio and the tone path stand in for it |
| Owner's A2-a addition: A2 passes at INTERNAL; the INTERNAL clock within +-50 ppm, as an observation | Met; observed | A2 PASS; [B7: the DUT's INTERNAL media clock](#b7-the-duts-internal-media-clock) |

So not every #629 item is met: Direction B's THD+N stays open, and the
stream-to-stream switch, a followed CRF stream's lock loss and the saved
selection across a power cycle have no bench evidence here.

### B7: limits

- Direction B's THD+N is NOT RUN: no known signal reaches the peer's talker
  without a wiring change.
- One run per case, on one DUT, against one reference peer, on two tones.
- The A2 and B-AAF verdicts rest on lane B6's capture-path attribution. Under
  the conservative reading of item 1 above, both would fail.
- The `mr` toggles are counted at both ends (GET_COUNTERS), not captured on the
  wire.
- The INTERNAL accuracy is relative to the reference peer and to gPTP time,
  neither of them calibrated.
- In B-CRF and B-AAF the servo's status carried bit 4, DRP config mismatch,
  from ACQUIRE on, as in lane B6. It is recorded, not analysed.
- The design's switch row, a followed CRF stream's lock loss and the saved
  selection across a power cycle were not run.
- Printed precision is not calibrated accuracy.

### B7: artifact hashes

The raw files stay outside the lane packet, on the bench host; each run's
`events.jsonl` records the size and SHA-256 of its raw files.

| Raw file | Bytes | SHA-256 |
|---|---|---|
| Tone loop (`b6_tone.py`) | 1,536,000 | `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588` |
| `a0/cap-lr.raw` (the tone's two channels, S24_3LE) | 190,630,332 | `a4b15c084dc049fc2253994579f71afdc3509791eec041a967bf3895e78e6115` |
| `a0/cap-ts.bin` (capture read times) | 1,588,368 | `9d4795fbacdc13257a2ffe0dfe9526b2412b7f474b1eabd5f5a5481f759af304` |
| `a0/samples.txt` (McASP0 timing samples) | 411,416 | `9ef78d996b58a063646bb1895b5045758fb3c553a524f3235d5fc790f3223175` |
| `a1/cap-lr.raw` | 190,437,378 | `4eae153bf2883d0f4193d6bfb12d50aa5984d90e0885abcf49fdddd8f2dc0970` |
| `a1/cap-ts.bin` | 1,586,568 | `fb057d0ac7bb8df9b3ab68362ba2f27c4b0a19f9e74302c378e3927d641a2be0` |
| `a1/samples.txt` | 411,019 | `9c91959addf532957ff642a084d26d8cabb122231ffe91b62bc06d1d7c0f7699` |
| `a2/cap-lr.raw` | 189,962,154 | `b0ff4ccee9d0d890d3e28ec0ad651b22f837bdfbebfcb4de029b5ba24de08a4d` |
| `a2/cap-ts.bin` | 1,581,600 | `59a03837e80869effb7976ee359a7a94e713325a4eaf9a7d1fbc6c930575331f` |
| `a2/samples.txt` | 411,152 | `1705e6fc69cf24e53e477e89765200bc54089a0e0e7aacd593563c5660820619` |
| `b0/cap-lr.raw` | 190,353,624 | `536ebf6eb3b76f904b12a856e36ae1eb91eccec9c38feeb13e2e75e7e82a5bb8` |
| `b0/cap-ts.bin` | 1,584,024 | `1c626979d8cba4812958eee28216ce24ed09308e58226d2857febaf668251a5b` |
| `b0/samples.txt` | 410,886 | `2e3dedfaa4993627d23943807ab198ab5449d278c72d1eb70d756c99316e9c61` |
| `bcrf/cap-lr.raw` | 190,155,072 | `cdd5ec246cef2ed8e63d580ba8bc595fa5182888c0d494bfcc84eb16f771aba2` |
| `bcrf/cap-ts.bin` | 1,579,584 | `a84c4b8212d95a01c9f4431adb1dff7aebc51bcab4b54bb377b587236c6d807f` |
| `bcrf/samples.txt` | 411,420 | `cb60cf59fc3069795e354d93c8dec7dd25a4018195f8f7bffca23a0a49532e40` |
| `baaf/cap-lr.raw` | 198,492,498 | `2ceb03ef48e1fc3c5e058df89fb844013a089286eb54f8b6ccb984084e922233` |
| `baaf/cap-ts.bin` | 1,650,960 | `4dc993f6243493e47c3bfa53f9c7fa903997f78049a7dd5c2a4367af9970c8a4` |
| `baaf/samples.txt` | 430,169 | `3ded42f38d568f66adfac0abdc0e56bdd97ebaaf8e176ca05d7e8572af711870` |
| `a0/grade-full.json` (full grade, `grade_b7.py`) | 589,874 | `ca50cb527fa7c3b43dfc03a10b73a4c34c3541934548f35154db0affcb630a22` |
| `a1/grade-full.json` | 398,819 | `dca238848d2eb8245a942ba5e80526bc5c42146e7c5cda9dd8872a3cc9ade3d9` |
| `a2/grade-full.json` | 416,260 | `d7e1752c45d3576901b9ffcd2bd051293398bc368b5ccd3892232b73bb18bb5d` |
| `b0/grade-full.json` | 598,788 | `cc1a897fcff183ff366a31fd6bb235693d3b2b71c73511c77748cfad22ee9a63` |
| `bcrf/grade-full.json` | 430,950 | `2b627eee5bdbf850bf7099ab73ba39e1c40d9e79f03fbab46f2421fd741e4af1` |
| `baaf/grade-full.json` | 434,897 | `8ad028859600d7476bc946bafb83eab7894229b9c6fb1afc341ee29f6c3aa70a` |
| `baaf/grade-lockloss-full.json` (the lock-loss segment) | 46,510 | `6a12f9bb92e89227f894a2ffbe21f6eb44c020e03b79277630b00facbb700ceb` |

The lane packet, `629-b7-a519`, holds the evidence and the tools. Its manifest
covers every retained file except itself. One redaction pass masked private
identifiers in 227 packet files, the tools among them, because two tools name
the external capture's channel layout. `redaction.json` records each masked
file's original and retained SHA-256. A masked tool is a record of the tool as
run, not a runnable copy. For the two masked tools below the hash is the
original's, as run; every other hash is the retained file's.

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `controls/controls.json` (tool controls) | 17,070 | `7bbefc71fb3c9303a8f1cb843bfcd13dafe55c1f3e1a968e6a3b3cee2350530e` |
| `summary/tables.md` (the per-case tables as rendered) | 4,283 | `81b14a7e9e2a002366e1a510bebd3a7759110dc339292abbee271ca51557c163` |
| `summary/verdicts.json` (every check behind each verdict) | 3,890 | `dfb285ffc3ed284b81998b19e500e34279dd25eeaee72b9e3e76fa6ee9960c7d` |
| `summary/checks/absorb.jsonl` (`b7_absorb.py`) | 7,446 | `317d37b41f2ed207dbd98033a1d3d6e64b0d4084622651cb69b28f0f6744ea3a` |
| `identity/identity-verdict.txt` (`identity_cmp.py`) | 3,037 | `ff817aca4909f1030c9296cfac3bc6af41994323e7b0a41610a505359d1422d4` |
| `identity/expected.json` (the build's values) | 1,068 | `ef6c9c37175e39d8e2919f793967ea95c36f3bd648ee53dcfe41f58ab844142d` |
| `restore/census-compare.txt` | 387 | `88467f637bcffa3195d316974406082bf266ac48565b049cd9f77e7addc24e11` |
| `runs/probe/soc-record.log` (the probe's statistics) | 1,729 | `f12336598f591b9b558a79577000ca8115009f914360a77ee5a3f2680adaa4bf` |
| `tools/run_b7.py` (as run) | 32,321 | `12c2e037d6e9027c3d1f5f2a7138e8771fecf248e672351788975efaa0236b75` |
| `tools/grade_b7.py` (as run) | 27,057 | `fb443c443cae4ad0aaed455fc7376c9531bc4937b996a40c9c763a0870556fd2` |
| `tools/b7_decode.py` | 10,093 | `a5eb63f29a19d608bbbc25c840943e5da15f3366a4887b62b221cc2d631110f4` |
| `tools/b7_tables.py` | 9,936 | `d719764214f4ff745ad33bbab971a9265414262a391d92277a4cc9bd40ac42d2` |
| `tools/b7_absorb.py` | 3,610 | `01caaf4dc27052cc6a589ac96f0b311bfda447742a603381a66ffb706036087d` |
| `tools/console_poll.py` | 3,746 | `7360b7266cc8db507070fc6538f9fd6cf6b8c2d625af9ce14826df443d7b6a34` |
| `tools/b7_ctl.py` | 12,532 | `5232777314b5898778f6bae17f0b5497a8b8c2aa5c4b192e6dfca7d0a75f7fb6` |
| `tools/identity_cmp.py` | 6,748 | `fb14729d9304dd33e6b3559d0987048b478260f04e0206cef0a85b647de62904` |
| `tools/probe_b7.py` | 9,375 | `917e7280e494aafdbc7d40f3188a8c9f27b14647126589c18c1f8cf6f90a0db2` |
| `tools/b6_thdn.py` (unchanged from lane B6) | 12,423 | `d4673f55642b850f57601b27d8fc930cc5382c2138f54edb1a7296bb4653a95f` |
| `tools/b6_tone.py` (unchanged from lane B6) | 2,965 | `d188a1a9ac0c3d94a2dab7d7b44ff7487490c87b969ea8c7d1b69382743179ac` |
