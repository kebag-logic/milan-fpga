<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Media-clock following graded by THD+N, on the ec0cc0c1, bbf704ec and 5603c353 images

Refs #629. Operator [A477], 2026-10-01, under the
[bench lane B6 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5929778646).
Lane B7 repeated the bench on dev `bbf704ec`, after PR #634, on 2026-10-03; its
results are in [Dev bbf704ec, 2026-10-03: lane B7](#dev-bbf704ec-2026-10-03-lane-b7).
Lane B8 followed the same day: the known tone did not reach the peer's talker,
so Direction B's THD+N did not run, and the source switch, the CRF lock loss
and the saved selection across a power cycle did; see
[Dev bbf704ec, 2026-10-03: lane B8](#dev-bbf704ec-2026-10-03-lane-b8).
Lane B15 located the loss on dev `5603c353`: the tone is already absent in the
peer's own talker stream, on the peer's link, and the DUT renders what it
receives sample for sample; see
[Dev 5603c353, 2026-10-10: lane B15](#dev-5603c353-2026-10-10-lane-b15).
In lane B16, the operator tried the reference peer's own loopback as the positive reference
on the same image: the peer cannot bind its listener to its own talker on this
network, because its probe for that talker goes unanswered, so the lane
stopped there; see
[Dev 5603c353, 2026-10-12: lane B16](#dev-5603c353-2026-10-12-lane-b16).
Resumed after the manager's ruling as B16b, the lane found the tone present in
the peer's talker stream and carried sample-exact to the DUT's TDM output. It
graded B0, by THD+N and SNR, and stopped for a decision on B-CRF and B-AAF; see
[B16b: the resume](#b16b-the-resume). As B16c, with the peer on its internal
source by the maintainer's exception, it graded B-CRF and B-AAF at the path's
floor with no discontinuity; see [B16c: the resume](#b16c-the-resume). Its
second findings round corrected figures against their receipts and published
reduced receipts; see
[B16, round 2: reduced receipts](#b16-round-2-reduced-receipts). Its third
added a check that recomputes every figure from its receipt; see
[B16, round 3: figures check](#b16-round-3-figures-check). Its fourth states
where the packet is published and makes the check claim figures inside links
and quoted phrases too; see
[B16, round 4: packet and coverage](#b16-round-4-packet-and-coverage). Its
fifth makes the check account for every digit, and holds a number before its
unit to be a measurement however it is written; see
[B16, round 5: every digit](#b16-round-5-every-digit). Its sixth reads the text as a reader sees it, and lets an identifier stand only before a closed list of what may follow it; see [B16, round 6: the closed list](#b16-round-6-the-closed-list). Its seventh refuses any markup in the text the check reads, instead of dropping comments as a renderer would; see [B16, round 7: no markup](#b16-round-7-no-markup). Its eighth reads that text through the pinned Markdown parser and refuses any construct off a closed allowlist; see [B16, round 8: the parser](#b16-round-8-the-parser). Its ninth judges each construct by the lines its source spans, not by the end the parser reports, and refuses a paragraph whose lines the parser misplaces; see [B16, round 9: source extents](#b16-round-9-source-extents).

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
- **[Dev bbf704ec, 2026-10-03: lane B7](#dev-bbf704ec-2026-10-03-lane-b7)** -- The bench repeated on the image with #634: identity, method changes, all six cases with B-AAF new, the lock-loss and INTERNAL-clock observations, the capture path, the #629 acceptance judged item by item, limits, hashes and where the packet is published.
- **[Dev bbf704ec, 2026-10-03: lane B8](#dev-bbf704ec-2026-10-03-lane-b8)** -- The remaining bench items: the known tone absent at the peer's talker, so Direction B's THD+N not run; the AAF and CRF source switch, the #645 slip after an INTERNAL-to-AAF set, the CRF lock loss and the saved selection across a power cycle; the #629 acceptance re-judged, limits and hashes.
- **[Dev 5603c353, 2026-10-10: lane B15](#dev-5603c353-2026-10-10-lane-b15)** -- Where Direction B's tone is lost: four points captured at once, the tone absent in the peer's own talker stream, the DUT's TDM output equal to what it receives, a positive control on the same taps, the tone source and the peer read only, the #629 acceptance, limits and hashes.
- **[Dev 5603c353, 2026-10-12: lane B16](#dev-5603c353-2026-10-12-lane-b16)** -- The reference peer's own loopback as the positive reference: the bind never forms a stream because the peer's probe of its own talker goes unanswered, so the lane stops at step 2; the tone source read only, with a route changed since lane B15, the controls, the acceptance of #629, limits and hashes. Then B16b, after the ruling: the tone present at the peer's talker and carried sample-exact to the DUT's TDM output, B0's grade by THD+N and SNR, with each loss attributed to a stage, directly inside the taps' overlap and by inference beyond it, the tone source changed during the lane, and B-CRF and B-AAF stopped for a decision. Then B16c, after the second ruling: the peer set to its internal source and back, each read back; B-CRF and B-AAF graded by THD+N and SNR at the four points, every block at the floor, no discontinuity, three of lane B6's four terms met and its timed ratio not run, the following record, the acceptance of #629, limits and hashes. Then round 2: the figures corrected against their receipts, and reduced receipts of the console poll, the tone source's reads and B0's overlap, bound to the raw hashes. Then round 3: a figures check that recomputes every figure of the section from its receipt, and the corrections it found. Then round 4: where the packet is published, and the check's exemptions narrowed to identifiers, with figures inside links and quoted phrases claimed by rows. Then round 5: the check accounts for every digit, and a number before its unit is a measurement that only a row can claim, however it is written. Then round 6: the check reads the text as a reader sees it, an identifier counts only before a closed list of what may follow it, so a unit or any other word directly after an identifier makes it a measurement, and a figure for several cases is recomputed from each case's own receipt. Then round 7: the check refuses any line of its text that holds markup, in code too, and drops nothing, and the section's table markers are removed. Then round 8: the check reads its text through the repository's pinned Markdown parser, judges only the visible text it yields, and refuses any construct off a closed allowlist, in the index row too. Then round 9: each construct judged by the lines its source spans rather than the end the parser reports, a paragraph whose lines the parser misplaces refused, and lines counted as the parser counts them.

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
| `a0/cap-lr.raw` (the tone's two channels) | 190,010,880 | `8143bd4fad5e2ff0deae8372d8d66b99c4b678b2a44e73cff820a93cf337c344` |
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
| B-AAF, the DUT following the peer's AAF stream | PASS | Servo LOCKED 6.6 to 7.1 s after the set and at every read; 0 net steps in 30,131,520 frames; the meter's history never restarted. Three capture-path clusters are disclosed. Outside the criteria, the INTERNAL-to-AAF switch run here is not shown free of undeclared discontinuity: the DUT's listener ring slipped one frame after lock (`SLIP_LB` 386 to 388) and counted 6 dups from before the binds to the window's first read ([#645](https://github.com/kebag-logic/milan-fpga/issues/645)). See [B7: Direction B](#b7-direction-b) |
| B, THD+N of a known signal from the peer's talker | NOT RUN | The known-signal probe was repeated: the peer's talker channels carry -2 to 0 LSB. See [B7: Direction B](#b7-direction-b) |
| (a) Lock loss of the followed AAF stream | Observed as declared | HOLDOVER within 0.56 s, the index kept, one `mr` toggle at the loss and none at the return, LOCKED 5.6 to 6.1 s after the return. See [B7: lock loss of the followed AAF stream](#b7-lock-loss-of-the-followed-aaf-stream) |
| (b) The DUT's INTERNAL media clock | Observed | +5.92 ppm from the reference peer; about -5.1 ppm against gPTP time. See [B7: the DUT's INTERNAL media clock](#b7-the-duts-internal-media-clock) |
| Restore | Done | Every clock source, format, binding and map read back as found. See [B7: bench as left](#b7-bench-as-left) |

These are operator observations, not review verdicts. The judgement of each
#629 acceptance item is in [B7: #629 acceptance](#b7-629-acceptance). Paths
such as `runs/a0/events.jsonl` are in the lane packet;
[B7: artifact hashes](#b7-artifact-hashes) says where it is published.

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

The grading criteria were not fixed before every graded case. The operator's
record (the packet's `HANDOFF.md`, "Grading criteria") wrote them down at 14:50
CEST. The order below supersedes two as-run texts that say otherwise: that
record's heading in the published `author/HANDOFF.md`, "before any case ran",
and the docstring of `grade_b7.py`, "each fixed before any graded case". The
round-2 handoff, `review-evidence/629-b7-r1/author-r2/HANDOFF.md` at the
[pin](#b7-artifact-hashes), carries the corrected heading. A0 started at
14:41:42 and its window ran from 14:42:08 to 14:52:39 (`runs/a0/events.jsonl`),
so they were fixed while A0 was recording. A1, the next case, started at
14:52:53 (`runs/a1/events.jsonl`). The "Fixed" column places each change.
Apart from the 14:50 record and the run logs, the times in this section are
file times on the bench host, which the packet does not carry: the run tool as
run, `run_b7.py`, was last written at 14:37, before the shakedown, and ran
every case unchanged.

| Change | Reason | Fixed |
|---|---|---|
| B0 binds both of the peer's talkers: its CRF to the DUT's STREAM_INPUT 1 and its AAF to STREAM_INPUT 0, with the DUT on INTERNAL | One control for both following cases (lane B6's B INTERNAL bound the CRF only) | 14:37, in the run tool, before A0 |
| B-AAF binds the peer's AAF talker to the DUT's STREAM_INPUT 0 and sets the DUT's CLOCK_DOMAIN to CLOCK_SOURCE 2 (D1 = L1) | The case #634 adds | 14:37, in the run tool, before A0 |
| A0 passes as a control when the listener's net rate is beyond 2 ppm | Lane B6 asked for about 16 ppm. Under A2-a the DUT's stream runs on its physical clock, about 6 ppm from the peer | 14:50, during A0's window |
| A one-frame repeat counts as the DUT's beat only while the DUT's `SLIP_TDM` moves in the window | Lane B6 used `SLIP_TDM` as a cross-check only. With it static every repeat is the listener's, so the change can only make a verdict stricter | 14:50, during A0's window |
| B-AAF adds the design's [bench row](../design/MEDIA_CLOCK_FOLLOWING.md#bench): LOCKED within 15 s of the set and at every read, the CLOCK_DOMAIN counters unchanged in the window, `SLIP_TDM` static, and the meter's history-restart count unchanged | The design's pass criteria for the case | 14:50, during A0's window |
| The DUT's words (servo, AAF meter, CRF sink, slip counters) are read every 30 s through each window, and both entities' GET_COUNTERS at three marks. One DUT read at B0's second mark timed out; see [B7: Direction B](#b7-direction-b) | The servo state through the window | 14:37, in the run tool, before A0 |
| A console poll of two words every 0.5 s times the set to LOCKED | The time from the set to LOCKED | 14:37, in the run tool, before A0 |
| The B-AAF lock-loss observation runs after the window, with the capture still running | Assignment item (a) | 14:37, in the run tool, before A0 |
| The grade's `tone.repeats` and `tone.repeated_frames` no longer subtract the silent inserts twice | A lane B6 summary slip: its A2 `grade.json` reads 139 repeats for 319 less 180. No attribution or verdict used the two fields | 14:55, after A0's window and its first grade; A0 was graded again |

The rest of the 14:50 record repeats lane B6's rules or states thresholds that
lane B6 left implicit, and was fixed at the same time, during A0's window:
A1 and A2 pass with 0 listener discontinuities, the clean blocks at the floor
within 0.01 dB and a fitted offset under 0.001 ppm; B0 passes as a control
beyond 2 ppm counted; B-CRF passes when the servo reads LOCKED, the counted
ratio is within 0.5 ppm of zero, the timed ratio's interval holds zero and the
tone path has 0 listener discontinuities. `b7_tables.py` applies these
thresholds, unchanged from the record. It was last written at 15:40 and
computed every verdict after the last case. One reported field came later
still: the `SLIP_LB` decode, added at 14:58 while A1 ran, which no criterion
uses.

**A0's threshold.** Its basis does not rest on A0's data. Lane B6 counted
McASP0 +6.52 ppm off the peer's output at INTERNAL, and the DUT's beat added
10.6 ppm on top of it at the peer's listener ([Direction A](#direction-a)).
A2-a removes the beat, so A0 was expected near 6.5 ppm, not the about 16 ppm
lane B6 asked for; 2 ppm is B0's bound too. Under lane B6's rule A0 would not
pass. #629's own words for this control are that the metric must show the
mismatch, and A0 meets them whatever the rate threshold: 186 of its 630 blocks
leave the floor, with 470 drops and 291 inserts by the listener, where A1 and
A2 hold none.

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

The tables below are arranged from `summary/tables.md`, which `b7_tables.py`
renders from the grades; every value is unchanged.

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

**One unanswered command, in B0.** At B0's second counter mark, 15:20:58 CEST
inside the window, the DUT's GET_COUNTERS on CLOCK_DOMAIN 0 had no response
within the controller's 1 s timeout (`runs/b0/ctl.jsonl`, `window-mark-1`). It
was not retried: the controller moved on, and the DUT answered the mark's next
command, GET_COUNTERS on STREAM_OUTPUT 0 (seq 22913), and its other three, at
once. The next mark, at 15:25:57, answered, with CLOCK_DOMAIN 0 at 3/2 as at
the window's start. It is the only one of the DUT's 336 AECP commands in the
eight runs that did not answer SUCCESS. Its cause is not analysed. No B0
criterion used that mark: B0 is graded on its counted ratio alone, and the one
criterion that reads CLOCK_DOMAIN counters, in B-AAF, reads the first and the
last mark (`b7_tables.py`).

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
It also counted 6 before that and 2 across the lock-loss observation. The 6
lie between the DUT's read before the binds and the window's first read, 1 s
into the window: an interval that holds both binds, the set, and the 20 s from
the set to the window in which the servo locked. The servo locks frequency
only, and nothing aligns the phase
([#632](https://github.com/kebag-logic/milan-fpga/issues/632)). The design
declares one #386 recentre after a settled source change, within 32,768 ticks
of the aligner engaging
([Switching sources](../design/MEDIA_CLOCK_FOLLOWING.md#switching-sources);
the bound is [TIME_SYNC](../design/TIME_SYNC.md)'s clock-source settle row);
it does not declare this slip. So the INTERNAL-to-AAF
switch run here is not shown free of undeclared discontinuity on the DUT's
followed receive path. The slip is not analysed here;
[#645](https://github.com/kebag-logic/milan-fpga/issues/645) takes it.

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
   listener repeat. The conservative reading counts each missing frame as a
   one-frame listener event: A2 would then hold 3 in its 2 clusters and B-AAF
   3 in its 3 clusters, and both would fail. Two observations argue against
   it. First, a capture stall on the bench host cannot make the peer repeat a
   frame, and the visible audio, about 627 s in each case, holds no listener
   event at all. Second, every off-signature cluster is short, the direction of
   the capture's own drift: over the six windows it delivers 0.54 to 0.93
   frames per second fewer than 48 kHz on the bench host's clock, so its
   packets are shortened by a frame about once a second.
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
| Fabric: recover the media clock from the selected AAF stream through the CRF servo path; gated on the live selection; a switch re-locks with no undeclared discontinuity | Met for recovery and gating. The INTERNAL-to-AAF switch run here is not shown free of undeclared discontinuity ([#645](https://github.com/kebag-logic/milan-fpga/issues/645)); the stream-to-stream switch not run at the bench | B-AAF: the servo LOCKED with trim -6.0 ppm and 0 net steps. The meter reads enabled only while CLOCK_SOURCE 2 is selected: 0 at every read of the other five cases. Each set from INTERNAL to the CRF or the AAF source toggled the DUT's AAF output's `mr` once: its MEDIA_RESET read 1 at every mark of B-CRF and B-AAF, and 0 in the cases without a DUT set. After the INTERNAL-to-AAF switch the DUT's listener ring slipped one frame 14 to 45 s after lock, inside the window (`SLIP_LB` 386 to 388, `runs/baaf/dut-window-0.txt` and `dut-window-1.txt`), and counted 6 dups from before the binds to the window's first read; no declaration covers the slip ([B7: Direction B](#b7-direction-b)). A switch between the AAF and CRF streams, the design's "Switch" bench row, was not in this assignment; it is graded in simulation only (`tb/verilator/milan_dp_mclk`) |
| Lock loss: declared holdover and restart, and `mr` per IEEE 1722-2016 4.4.4.3 | Met for the AAF source | [B7: lock loss of the followed AAF stream](#b7-lock-loss-of-the-followed-aaf-stream). A followed CRF stream's loss was not run at the bench |
| Protocol processor: SET/GET_CLOCK_SOURCE over the longer list, the selection kept as saved state | Met in part at the bench | SET_CLOCK_SOURCE 1 and 2 answered SUCCESS and read back; CLOCK_SOURCE 3 does not exist. The NVM committed 17 times over the method's changes. Restoring the saved index across a power cycle needs a power cycle, which this lane may not do; processor PR 142 grades it as D3C3 (pin `631eeb34`) |
| Simulation: each source in turn; the clock follows within tolerance; switching and lock loss graded by failing mutants | Met by the merged PR's evidence, not re-run here | `tb/verilator/aaf_clock_meter` and `tb/verilator/milan_dp_mclk` with their mutant lists; PR #634's hosted checks at its head `2bc5adc0`: every executed context SUCCESS, 21 of them, `verilator-suites`, `rtl-fast` and `yosys-portability` among them. One context, "Physical gPTP (nightly and manual)", was skipped and not executed |
| Bench, both directions, each followed source: the listener's CLOCK_DOMAIN set and read back, its format adapted, the as-found source restored | Met | A1, A2, B-CRF and B-AAF; [B7: binding rule and clock-source record](#b7-binding-rule-and-clock-source-record) |
| Bench quality metric: THD+N and SNR of a known tone on the selected path, against the INTERNAL control and synthetic slips and drift | Met for Direction A; NOT met for Direction B | Direction A: A0 shows the mismatch, A1 and A2 sit at the floor, and the controls are byte-equal to lane B6's. Direction B: no known signal reaches the peer's talker without a wiring change, so the DUT's selected path carries no known tone; the frame-rate ratio and the tone path stand in for it |
| Owner's A2-a addition: A2 passes at INTERNAL; the INTERNAL clock within +-50 ppm, as an observation | Met; observed | A2 PASS; [B7: the DUT's INTERNAL media clock](#b7-the-duts-internal-media-clock) |

So not every #629 item is met: Direction B's THD+N stays open, the one
switch run here leaves an undeclared slip on the DUT's listener ring (#645),
and the stream-to-stream switch, a followed CRF stream's lock loss and the
saved selection across a power cycle have no bench evidence here.

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
- B-AAF's slip on the DUT's listener ring after lock and B0's one unanswered
  GET_COUNTERS are recorded, not analysed; #645 takes the slip.
- The design's switch row, a followed CRF stream's lock loss and the saved
  selection across a power cycle were not run.
- Printed precision is not calibrated accuracy.

### B7: artifact hashes

The raw files stay outside the lane packet, on the bench host. Each run's
`events.jsonl` records the size and SHA-256 of every raw file of its run,
among them the three per case below and the tone loop: the first 19 rows below.
The packet's `RAW-ARTIFACTS.json` records every raw file, those 19 among them,
and is the only record of the last seven rows, the full grades.

| Raw file | Bytes | SHA-256 |
|---|---|---|
| Tone loop (`b6_tone.py`) | 1,536,000 | `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588` |
| `a0/cap-lr.raw` (the tone's two channels) | 190,630,332 | `a4b15c084dc049fc2253994579f71afdc3509791eec041a967bf3895e78e6115` |
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
identifiers in 227 packet files, the tools among them, because four tools name
the external capture's channel layout. `redaction.json` records each masked
file's original and retained SHA-256. A masked tool is a record of the tool as
run, not a runnable copy.

**Where the packet is.** It is published on branch `629-b7-review-evidence`,
pinned at commit `c6ad37e7d9163b5a85aef935a7d8e7f7f6686f7f`. The packet label
`629-b7-a519` maps to `review-evidence/629-b7-r1/author/` there:
`summary/a1/grade.json` is
`review-evidence/629-b7-r1/author/summary/a1/grade.json`.
`review-evidence/629-b7-r1/MANIFEST.json` gives each file's `original_sha256`,
the lane packet's file, beside the published file's `published_sha256`. The
packet was first published at `95448218`. In the tools, the redaction pass
had masked the external capture's channel count only in the channel-count
assignment of `run_b7.py` and lane B6's `run_b6.py`, and its sample format
nowhere. Two later commits masked the rest, and this page states neither value:

- `d36de704` masked the channel count in the docstrings of four tools,
  `run_b7.py`, `grade_b7.py`, `run_b6.py` and `grade_b6.py`, and the sample
  format in the docstrings of `run_b7.py` and `run_b6.py` and in their code, as
  the format argument of the capture command.
- `c6ad37e7` masked the channel count in the capture file's name, in 19 files:
  `RAW-ARTIFACTS.json`, `runs/<case>/events.jsonl` and `runs/<case>-lock.txt`
  for each of the seven captured runs, the B-AAF shakedown among them, and the
  code of the same four tools.

Both were added on top of the branch, with no force-push: `95448218` and
`d36de704` stay in its history as published.

Every row below equals its file's `published_sha256` at `c6ad37e7`, except the
two masked tools. For those the hash is the tool as run, recorded as
`original_sha256` in the packet's `redaction.json`; the lane packet held them
masked, and `d36de704` and `c6ad37e7` masked them further. Neither commit
changed any other file this table cites. In `RAW-ARTIFACTS.json` and the
runs' `events.jsonl`, `c6ad37e7` changed only the capture file's name, so the
raw rows above are recorded there unchanged.

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

## Dev bbf704ec, 2026-10-03: lane B8

Refs #629. Operator [A521], 2026-10-03, under the
[bench lane B8 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970760794).
The image is lane B7's: the manager's build of dev
`bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`, as flashed for lane B7. The lane
was to run #629's remaining bench items:

1. Direction B graded by the THD+N and SNR of a known tone fed into the
   reference peer's talker inputs;
2. a source switch between the peer's AAF and CRF streams, the DUT as listener;
3. the lock loss of a followed CRF stream;
4. the saved clock-source selection across one cold power cycle of the DUT.

The lane ran in two sessions. The first stopped at item 1's precondition: the
known tone did not reach the peer's talker, which is one of the assignment's
STOP conditions
([STOP](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970982211)).
The manager ruled that item 1 waits for the owner's check of the tone's path
and that items 2 to 4 run
([ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5970994127)).
The second session ran them, the one authorised power cycle included, and
restored everything.

| #629 bench item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `bbf704ec` | PASS, three times | At the start, at the resume and after the power cycle, each verdict byte-equal to lane B7's. See [B8: identity and setup](#b8-identity-and-setup) |
| Analysis tool, synthetic controls | PASS | Re-run after the cases, byte-equal to lanes B6 and B7. See [B8: tool controls](#b8-tool-controls) |
| Format check before every bind | Held | Every listener took the talker's format and read it back; no talker format was set. See [B8: binding rule and clock-source record](#b8-binding-rule-and-clock-source-record) |
| Clock source set on the listener only, read back, restored | Held | Five sets on the DUT's CLOCK_DOMAIN, each read back equal; each case restored INTERNAL and read it back |
| 1. Direction B: B0, B-CRF and B-AAF by THD+N and SNR | NOT RUN | The known tone does not reach the peer's talker. See [B8: the tone proof](#b8-the-tone-proof) |
| 2. Switch AAF to CRF | PASS | LOCKED 2.6 to 3.1 s after the set; one MEDIA_RESET; no slip on the listener ring, the TDM junction or the tone path. See [B8: the source switch](#b8-the-source-switch) |
| 2. Switch CRF to AAF | PASS | LOCKED 6.0 to 6.5 s after the set; as above |
| The INTERNAL-to-AAF set that started item 2 | #645 repeated | The listener ring slipped one frame 2.0 to 3.0 s after the servo first read LOCKED. See [B8: the INTERNAL-to-AAF set and #645](#b8-the-internal-to-aaf-set-and-645) |
| B-CRF repeated, the window before item 3 | PASS | Servo LOCKED at all 797 polls; 0 net steps in 19,261,920 frames |
| 3. Lock loss of a followed CRF stream | Observed as declared | HOLDOVER within 0.56 s, the index and the trim kept, one `mr` toggle, LOCKED 2.7 to 3.2 s after the return. See [B8: lock loss of the followed CRF stream](#b8-lock-loss-of-the-followed-crf-stream) |
| 4. The saved selection across a power cycle | PASS | GET_CLOCK_SOURCE read 2 after the boot, and the servo read LOCKED with no state-changing command sent. See [B8: the saved selection across a power cycle](#b8-the-saved-selection-across-a-power-cycle) |
| Restore | Done | See [B8: bench as left](#b8-bench-as-left) |

These are operator observations, not review verdicts. Paths such as
`runs/sw/events.jsonl` are in the lane packet, published on branch
`629-b8-review-evidence` at `36ee6d8a`;
[B8: artifact hashes](#b8-artifact-hashes) gives the full pin and maps each
path to its place there.

### B8: identity and setup

The gate is lane B7's ([B7: identity and setup](#b7-identity-and-setup)),
against the same build values. It ran three times: at the first session's start
(17:57 CEST), at the resume (18:31) and after the power cycle (18:52). Every
check passed each time, and each verdict file is byte-equal to lane B7's.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM image CRC32, 7,512 bytes | `5ba355eb`, the build's `aem_desc.bin` |
| BIOS ROM CRC32, 53,588 bytes | `2144df1c`, the build's BIOS |
| QSPI bitstream payload CRC32, 3,825,788 bytes | `e6b8febc`, the build's payload |
| Live descriptors over AECP | Lane B7's 11, each byte-equal to the build's AEM image; CLOCK_SOURCE 3 answers NO_SUCH_DESCRIPTOR |
| Clock sources of #629 | CLOCK_SOURCE 0 INTERNAL; 1 INPUT_STREAM on STREAM_INPUT 1, the CRF input; 2 INPUT_STREAM on STREAM_INPUT 0, the AAF input. CLOCK_DOMAIN 0 lists 0, 1 and 2 and reads 0 |
| UART grader | 10 of 10 |
| Identity gate | PASS |

As found, the bench was as lane B7 left it:

- **DUT.** Every stream unbound, both audio maps empty, CLOCK_DOMAIN 0 on
  INTERNAL, STREAM_INPUT 0 at `0205022002006000`. NVM slots seq 17 and 16,
  `VD_OK`, 17 commits since boot.
- **Reference peer.** Every stream unbound, its CLOCK_DOMAIN on INTERNAL, its
  STREAM_INPUT 0 at `0205022001006000`.
- **SoC board.** The boot lane B7 used, both bridge legs running with the
  bridge script's command lines. Its console stood at a root prompt in both
  sessions, and `id` over the board link confirmed it. No credential was typed
  or stored. In each session the two bridge legs were stopped by process ID
  before the bench work and restarted with the recorded command lines after it,
  as in lanes B6 and B7.
- **Controller host.** No gPTP daemon, no staging.

At the resume the bench was as the first session left it: the census of both
entities equal, the DUT's NVM at seq 19 and 18 with 19 commits since boot.

### B8: the tone proof

Item 1's precondition, from the first session. The assignment asks for proof
that the tone reaches the peer's talker before any grading.

**The tone.** Lane B6's two tones, 997 Hz and 9,973 Hz with its start phases,
at -20 dBFS (`b8_tone.py`), were played into the reference peer's talker
inputs by the owner's method. No setting of any instrument was read or
changed. The playback ran from 18:04:59 to 18:06:51
CEST, and through the proof it was running, consuming 48,000 frames a second.

**The probe.** It is lane B7's known-signal probe with one change: McASP0's
recording of the DUT's TDM output is sent over the board link to the bench
host and graded there (`probe_b8.py`, `b8_proof.py`), instead of being reduced
on the board. Under the binding rule the DUT's STREAM_INPUT 0 took the peer
talker's `0205022001006000`, set and read back. Four identity mappings went
on STREAM_PORT_INPUT 0, and the peer's AAF talker was bound to that input:
SUCCESS, connection count 1. McASP0 then recorded 10 s, 480,000 frames, from
18:05:13 CEST. Everything was restored and read back afterwards.

| TDM output channel | Level, dBFS RMS | Range, 24-bit LSB | Power within 5 Hz of 997 Hz | Power within 5 Hz of 9,973 Hz |
|---|---|---|---|---|
| 0 | -141.1 | -2 to 0 | 0.04 % | 0.04 % |
| 1 | -141.1 | -2 to +1 | 0.04 % | 0.04 % |
| 2 | -141.5 | -1 to 0 | 0.03 % | 0.04 % |
| 3 | -141.5 | -1 to 0 | 0.04 % | 0.04 % |
| 4 to 7, unmapped | No signal: every word zero | 0 | - | - |

`b8_proof.py` finds a tone on a channel when over 90 % of the channel's power
lies within 5 Hz of it, at -40 dBFS or more. No channel carries either tone.
The 0.03 to 0.04 % is the share of a flat noise floor in a 10 Hz band, and the
range is lane B6's and lane B7's idle floor.

The stream itself arrived. The DUT's STREAM_INPUT 0 read MEDIA_LOCKED 1 and
MEDIA_UNLOCKED 0 at both of its counter reads, 12.6 s apart around the
recording. Between them FRAMES_RX rose by 103,998, with no interruption, no
sequence mismatch and no late or early timestamp. The DUT's render path was
live: the four mapped channels carry a non-zero floor of a few LSB, while the
four unmapped channels are exactly zero. So the DUT received the peer's talker
stream throughout and rendered it, and that stream carried no tone.

**STOP, and item 1 NOT RUN.** The tone did not reach the peer's talker, so the
first session stopped. Where along the tone's path into the peer it was lost
was not examined: that path is the owner's bench, and no setting of it may be
read or changed. The tone was stopped at 18:06:51 CEST and was not played
again. By the ruling, item 1 waits for the owner, and Direction B's THD+N and
SNR stay NOT RUN.

**One incident, the bench lock.** The playback's first start, at 18:03:16
CEST, left the bench lock held: the detached playback had inherited the lock's
descriptor. Only this lane's own first probe attempt waited on it, and it gave
up after 60 s with nothing done. The playback was stopped by its process ID
shortly before 18:04:59 and started again with the descriptor closed
(`tone_play_b8.sh`, `flock -o`). The lock was free after every later step,
and nothing was left detached in either session.

### B8: method

Items 2 and 3 use lane B7's bench, tone and grading
([B7: method changes](#b7-method-changes)): lane B6's tone loop played into
McASP0 on the SoC board, through the DUT's AAF talker to the peer's listener on
the peer's own clock, recorded by the external capture, with McASP0's timing
sampled on the board. That tone path is the design's "tone at the floor" in its
[Bench](../design/MEDIA_CLOCK_FOLLOWING.md#bench) switch row. No tone was fed
into the peer's talker in the second session.

**The receive path.** The peer's talker carries no known signal, so the audio
the DUT receives cannot be graded for discontinuities. The DUT's followed
receive path is observed instead through four records:

- `SLIP_LB`, the loopback ring's dup and skip counts, fed by the peer's AAF
  stream on STREAM_INPUT 0; two dups are one slipped frame, one per channel
  pair of that stream ([B7: Direction B](#b7-direction-b));
- `SLIP_TDM`, the TDM junction's
  (`0x8D8`, in [the media-boundary slip counters](../reference/REGISTER_MAP.md#0x8d4-----media-boundary-slip-counters--slip-kl_chan_map_capture));
- `RENDER_STAT`'s prefill and converged bits and its rail count for
  STREAM_INPUT 0, the render stage that carries the #386 recentre
  ([0x8DC](../reference/REGISTER_MAP.md#0x8dc-----render-setpoint-state));
- the DUT's two Stream Inputs' GET_COUNTERS.

The recentre count is a simulation tap, not a register, so the bench cannot
count recentres. A recentre on a short queue re-enters prefill and clears the
converged bit until the fill has stayed in band for 100 ms; on a full queue it
moves the read pointer and leaves no trace
(`hdl/ieee1722/aaf/KL_render_setpoint.sv`). A rail would raise the rail count.

**The poll.** One console poll per case reads the servo, the AAF meter, the
CRF sink's lock and rate, `SLIP_LB`, `SLIP_TDM` and `RENDER_STAT` every 0.5 s,
from before the case's binds to after its restore (`console_poll_b8.py`). It
replaces lane B7's 30 s DUT reads, because the console serves one reader. A
change is timed as an interval: from the end of the poll before it to the end
of the poll that saw it. GET_COUNTERS on the DUT's CLOCK_DOMAIN, both of its
talkers and both of its listeners, and on the peer's listener, ran in SW
before each set, at its LOCKED, mid-hold and at the hold's end, and in CRFLL
at three window marks and around the lock loss, each with GET_CLOCK_SOURCE. A
time after a set runs from just before the command was sent.

**The cases.** Each ran as one locked action. Every bench command had to end
within 10 minutes, so the windows are shorter than lane B7's 630 s:

| Case | Item | Set-up | Sequence |
|---|---|---|---|
| SW | 2 | The peer's CRF talker to the DUT's STREAM_INPUT 1 and its AAF talker to STREAM_INPUT 0, as lane B7's B0 | CLOCK_SOURCE 2 (AAF, from INTERNAL), 1 (CRF), 2 (AAF), each read back and held 120, 150 and 150 s after LOCKED; then INTERNAL |
| CRFLL | 3 | The peer's CRF talker to the DUT's STREAM_INPUT 1, as lane B7's B-CRF | CLOCK_SOURCE 1; a 420 s window from 20 s after the set; then lane B7's lock-loss observation with the CRF talker: unbind, 11 s of holdover, rebind under the binding rule, LOCKED and 10 s on |
| PC | 4 | The peer's AAF talker to the DUT's STREAM_INPUT 0 | CLOCK_SOURCE 2, LOCKED and the NVM commit; the power cycle; after the boot, GET_CLOCK_SOURCE first, then the servo with no command; then the restore |

The verdicts compare each observation with a value the design declares, or
with lane B7's B-CRF criteria for the CRF window. No lane threshold was added.
The SW tone path is graded as one span, from 20 s after the first set to the
end of the last hold, so both stream-to-stream switches lie inside it.
`grade_b8.py` is lane B7's `grade_b7.py` with the segment's events as
arguments and its DUT words from the poll; `b8_events.py` decodes the polls and
counters around each set, unbind and rebind.

### B8: tool controls

`b6_thdn.py controls` was re-run on the bench host at 19:00 CEST, after the
cases and their grades: the first session stopped before its controls, and
the second did not run them first. Its output is byte-equal to lanes B6 and
B7's `controls.json`, SHA-256 `7bbefc71...`, and `b6_thdn.py` is byte-equal
to lane B6's, so the tool that graded the cases is the one the controls prove.
Every row of [Tool controls](#tool-controls) holds here.

### B8: binding rule and clock-source record

| Bind or set | Talker format | Listener format read | Set on the listener | Read back |
|---|---|---|---|---|
| DUT AAF to peer STREAM_INPUT 0, SW and CRFLL | `0205022002006000` | `0205022001006000` | `0205022002006000`, SUCCESS | `0205022002006000` |
| Peer CRF to DUT STREAM_INPUT 1, SW, CRFLL and the CRFLL rebind | `041060010000bb80` | `041060010000bb80` | None, equal | `041060010000bb80` |
| Peer AAF to DUT STREAM_INPUT 0, SW, PC and the first session's probe | `0205022001006000` | `0205022002006000` | `0205022001006000`, SUCCESS | `0205022001006000` |
| SW: the DUT's CLOCK_DOMAIN 0 to CLOCK_SOURCE 2, 1, then 2 | - | - | SET_CLOCK_SOURCE SUCCESS each | 2, 1, 2 |
| CRFLL: the DUT's CLOCK_DOMAIN 0 to CLOCK_SOURCE 1 | - | - | SET_CLOCK_SOURCE SUCCESS | 1 |
| PC: the DUT's CLOCK_DOMAIN 0 to CLOCK_SOURCE 2 | - | - | SET_CLOCK_SOURCE SUCCESS | 2 |

Every bind answered SUCCESS with connection count 1, and every unbind
connection count 0. Each case ended with the DUT's CLOCK_SOURCE 0 set and read
back. Every listener format the method set was restored and read back: the
peer's STREAM_INPUT 0 to `0205022001006000` and the DUT's to
`0205022002006000`. The peer's clock source was never set.

### B8: the source switch

Case SW, 18:32:19 to 18:39:59 CEST. The declared behaviour is the design's
[Switching sources](../design/MEDIA_CLOCK_FOLLOWING.md#switching-sources)
(W2) and [`mr`](../design/MEDIA_CLOCK_FOLLOWING.md#mr), the switch row of its
[Bench](../design/MEDIA_CLOCK_FOLLOWING.md#bench), and TIME_SYNC's
clock-source settle row
([Listener render latency](../design/TIME_SYNC.md#listener-render-latency)).
Under W2 a switch between two streams is one `mr` toggle, one #386 recentre
once the grid settles, and a few seconds of HOLDOVER and ACQUIRE: about 3 s
onto CRF, about 6 s onto AAF, with no frame slip.

<!-- b8-switch-servo -->
| Set, CEST | From, to | Answer, read back | Servo after the set | LOCKED, s after the set | AAF meter after the set | Trim, ppm | GET_CLOCK_SOURCE in the hold | Hold after LOCKED |
|---|---|---|---|---|---|---|---|---|
| 18:32:31 | INTERNAL to AAF | SUCCESS, 2 | ACQUIRE by 0.11 s | 6.64 to 7.14 | Locked by 0.11 s; rate valid 4.14 to 4.64 s | 0; -5.63 at LOCKED; -6.06 to -5.81 in the hold | 2 at all 3 reads | 120 s |
| 18:34:38 | AAF to CRF | SUCCESS, 1 | ACQUIRE by 0.09 s, trim -6.06 | 2.62 to 3.12 | Disabled by 0.09 s | -6.06 to -5.94 | 1 at all 3 reads | 150 s |
| 18:37:11 | CRF to AAF | SUCCESS, 2 | ACQUIRE by 0.40 s, trim -6.00 | 5.96 to 6.48 | Locked by 0.40 s; rate valid 3.93 to 4.44 s; history restarts 0 | -6.06 to -5.94 | 2 at all 3 reads | 150 s |

The trim carried across both stream-to-stream switches: it read -6.06 and
-6.00 ppm in ACQUIRE and -6.00 at LOCKED, where W1 would have returned it to 0.
W2's HOLDOVER at a switch lasts while the reference is presented as unlocked,
far below the poll's 0.5 s, and no poll saw it. Through every hold the servo
read LOCKED at every poll: 238, 298 and 298 polls. The meter's rate read
+10.99 to +11.03 ppm, the CRF sink's +10.98 to +11.05 ppm, and the meter's
largest timestamp deviation 29 ns, as in lane B7.

<!-- b8-switch-counters -->
| Counter | Before the first set | After INTERNAL to AAF | After AAF to CRF | After CRF to AAF | Declared |
|---|---|---|---|---|---|
| DUT STREAM_OUTPUT 0 (AAF talker) MEDIA_RESET | 0 | 1 | 2 | 3 | One `mr` toggle per source change |
| Peer STREAM_INPUT 0 MEDIA_RESET (the toggle as received) | 0 | 1 | 2 | 3 | As above |
| DUT CLOCK_DOMAIN 0 LOCKED / UNLOCKED | 6 / 5 | 7 / 6 | 8 / 7 | 9 / 8 | C1: UNLOCKED as the servo leaves LOCKED, LOCKED when it reads LOCKED again; LOCKED is UNLOCKED or UNLOCKED + 1 |
| DUT STREAM_INPUT 0 and 1: MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP, EARLY_TIMESTAMP | 0 each | 0 each | 0 each | 0 each | Neither received stream disrupted |

Each column is the mark at that set's LOCKED; the mid-hold and end-of-hold
marks read the same. The 0 before the first set is the bank reset at the bind.
The restore to INTERNAL toggled MEDIA_RESET once more, to 4.

<!-- b8-switch-receive -->
| Word | Around INTERNAL to AAF | Around AAF to CRF | Around CRF to AAF | Declared |
|---|---|---|---|---|
| `SLIP_LB` dups / skips | 418 to 422 / 0, see [B8: the INTERNAL-to-AAF set and #645](#b8-the-internal-to-aaf-set-and-645) | 422 / 0, static | 422 / 0, static | No frame slip on a switch between two streams |
| `SLIP_TDM` dups / skips | 0 / 0, static | 0 / 0, static | 0 / 0, static | Static: one grid |
| `RENDER_STAT` rail count | 31, static | 31, static | 31, static | No rail |
| `RENDER_STAT` converged | Low at the poll that ended 0.11 s after the set, high again by 0.61 s; prefill never seen | Low at the poll that ended 0.09 s after the set, high again by 0.60 s; prefill never seen | High at every poll | One #386 recentre once the grid settles: 43 ms to 683 ms under following |

The converged bit fell within about 0.1 s after two of the three sets, inside
the settle bound, with no rail counted. That is consistent with the declared
recentre finding the queue short. An underrun leaves the same prefill and
converged trace, and `RENDER_STAT` does not expose the stage's underrun count,
so the bench cannot tell the two apart. After the third set no poll saw it, as
when a recentre finds the queue full, or when the 100 ms low falls between two
polls. So each set left at most the trace one recentre makes, and no rail; the
recentre count itself is not visible to the bench.

<!-- b8-thdn-sw -->
| Span | Tone | Blocks | Blocks at the floor | THD+N there, dB (median / worst) | SNR there, dB (median / worst) | Worst THD+N, all blocks, dB |
|---|---|---|---|---|---|---|
| SW, 18:32:51 to 18:39:48 | 997 Hz | 417 | 416 | -146.06 / -146.06 | 146.07 / 146.07 | -7.28 |
| SW, 18:32:51 to 18:39:48 | 9,973 Hz | 417 | 416 | -145.99 / -145.99 | 145.99 / 145.99 | -1.09 |

<!-- b8-offset-sw -->
| Span | Fitted offset, blocks at the floor, ppm (largest magnitude) | Listener discontinuities | Counted McASP0 to peer ratio, ppm | Timed ratio, ppm (95 % half-width) | DUT `SLIP_TDM` in the span | Capture-path losses: events, clusters, frames | Torn frames | Result |
|---|---|---|---|---|---|---|---|---|
| SW, both switches inside | 1.1e-8 | 0 | 0 (0 net steps in 20,030,400 frames; 1 frame = 0.050) | -0.02 (+-0.57) | 0 in 417 s | 1, 1, 108 | 0 | PASS |

The one block off the floor holds a 108-frame capture-path loss, 48 n + 12
frames with a matching read-time rise. The longest capture read stall in the
span was 31 ms.

**Verdict.** Both stream-to-stream switches behaved as declared: one `mr`
toggle each, at both ends; the CLOCK_DOMAIN counters one pair each; LOCKED
again in the declared time with the trim kept; GET_CLOCK_SOURCE the set index
throughout; and no slip on the listener ring, the TDM junction or the tone
path. The only discontinuity the bench can see at a switch is the converged
bit's fall, consistent with the declared recentre. Item 2 PASSES for AAF to CRF
and CRF to AAF.

### B8: the INTERNAL-to-AAF set and #645

The case's first set, from INTERNAL to AAF, is lane B7's B-AAF set, and the
assignment asks for #645's observation again. `SLIP_LB` at every change, from
the binds to the restore:

<!-- b8-slip-lb -->
| Seconds after the INTERNAL-to-AAF set | `SLIP_LB` dups | Servo | Slipped frames |
|---|---|---|---|
| -2.0, the binds | 414 | IDLE, on INTERNAL | - |
| -1.40 to -0.90 | 416 | IDLE | 1 |
| -0.90 to -0.07 | 418 | IDLE | 1 |
| 2.13 to 2.63 | 420 | ACQUIRE | 1 |
| 6.64 to 7.14 | 420 | LOCKED, first read | - |
| 9.15 to 9.65 | 422 | LOCKED | 1, 2.0 to 3.0 s after the first LOCKED read |
| To 437.3, the restore | 422 | LOCKED, with both stream-to-stream switches | 0 in 428 s |

The 414 is the count earlier lanes left; nothing clears it. The binds ended
2.01 s before the set, with the DUT on INTERNAL. `RENDER_STAT` left prefill
at -1.90 to -1.40 s. The next two polls each saw one slipped frame, at -1.40
to -0.90 and at -0.90 to -0.07 s: two slips within 1.94 s of the binds' end,
at most 1.33 s apart, with no skip counted. Lane B7 measured the DUT's
INTERNAL clock +5.92 ppm off the peer
([B7: the DUT's INTERNAL media clock](#b7-the-duts-internal-media-clock)). A
steady offset of that size slips one frame every 3.52 s
(1 / (48,000 x 5.92e-6)), so it puts at most one slip in 1.94 s. The two slips
before the set are recorded here and not analysed; this lane gives no cause
for them. The third slip fell in ACQUIRE, before the servo locked. The slip
2.0 to 3.0 s after LOCKED is not declared: the design declares one #386 recentre
after a settled source change, and the servo locks frequency only
([#632](https://github.com/kebag-logic/milan-fpga/issues/632)). Lane B7 saw the
same shape: one slip 14.7 to 44.9 s after LOCKED, and 6 dups before its window.
After this slip the ring held for 428 s, through both switches between
streams.

So the INTERNAL-to-AAF switch is again not shown free of undeclared
discontinuity on the DUT's followed receive path. This is #645's observation
repeated, and the data above is for
[#645](https://github.com/kebag-logic/milan-fpga/issues/645). This lane did not
post on #645.

### B8: lock loss of the followed CRF stream

Case CRFLL, 18:40:09 to 18:48:17 CEST. Its window first repeats lane B7's
B-CRF on the shorter window:

<!-- b8-crf-window -->
| Window, CEST | Servo at the 797 polls | Trim, ppm | Set to LOCKED, s | CRF sink rate, ppm | GET_CLOCK_SOURCE | CLOCK_DOMAIN LOCKED / UNLOCKED, start and end | Listener discontinuities | Counted ratio, ppm | Timed ratio, ppm (95 % half-width) | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| 18:40:41 to 18:47:41 | LOCKED | -6.06 to -5.94 | 2.66 to 3.17 | +10.98 to +11.04 | 1 at all 3 marks | 10 / 9, 10 / 9 | 0 | 0 (0 net steps in 19,261,920 frames; 1 frame = 0.052) | -4.67 (+-24.96) | PASS |

The window spans 798 polls. One, poll 618, missed a word, and `b8_events.py`
leaves it out, so the table counts 797.

The window's events span 420.03 s of host time. Of it, 401.29 s of audio was
captured, 19,261,920 frames, and the capture path lost 899,009 frames, 18.73 s
(`capture_lost_frames` in the window's grade, over 48,000 frames a second).
The two sum to 420.02 s. Three read stalls on the bench host, read gaps of
4.12, 4.37 and 9.77 s, made three of the window's nine capture-path clusters,
which lost 18.69 s between them. The clusters begin at 270.9, 284.1 and
285.5 s of captured audio into the window, or about 271, 289 and 295 s
counting the frames lost before each. Each of the nine passed on a read-time
rise matching its loss within 1 ms + 2 %. Two of the three stall clusters are
off the 48 n + 12 signature, as a multi-second overrun can be. The third is
on it, its one skip 2,172 frames, and it also holds a 23,776-frame
capture-path repeat. A listener event inside the stalls could not be seen,
and the timed ratio is wide for the same reason. 391 of the 401 blocks sit at
the floor: THD+N -146.06 and -145.99 dB, SNR 146.07 and 145.99 dB, fitted
offset under 2e-7 ppm.

After the window the peer's CRF talker was unbound from the DUT's
STREAM_INPUT 1, held off for 11.04 s, and rebound under the binding rule. The
poll ran throughout and the external capture kept recording. The declared
behaviour is the design's
[Lock loss, holdover and restart](../design/MEDIA_CLOCK_FOLLOWING.md#lock-loss-holdover-and-restart)
and [`mr`](../design/MEDIA_CLOCK_FOLLOWING.md#mr).

<!-- b8-lockloss-events -->
| Event | Seconds after it | Observed | Declared |
|---|---|---|---|
| Unbind | 0.05 to 0.56 | Servo HOLDOVER, trim held at -6.00 ppm; the CRF sink unlocked | Lock falls 100 ms after the last PDU; HOLDOVER with the trim frozen |
| Through the holdover | to 11.04 | HOLDOVER at all 19 polls, trim -6.00 at each; GET_CLOCK_SOURCE 1 | No timeout, no fallback; the index unchanged |
| Rebind | by 0.14 | The CRF sink locked | The measurement locks after 8 PDUs |
| Rebind | 0.14 to 0.64 | Servo ACQUIRE | The servo re-enters ACQUIRE; the CRF rate is valid 512 ms after the restart |
| Rebind | 2.66 to 3.16 | Servo LOCKED, trim -6.00 ppm; GET_CLOCK_SOURCE 1 | LOCKED after four windows within 2 ppm |

<!-- b8-lockloss-counters -->
| Counter | Before the unbind | In the holdover | After LOCKED again | Declared |
|---|---|---|---|---|
| DUT STREAM_OUTPUT 0 (AAF) MEDIA_RESET | 1 | 2 | 2 | One `mr` toggle per disruption, none on the return |
| Peer STREAM_INPUT 0 MEDIA_RESET (the toggle as received) | 1 | 2 | 2 | As above |
| DUT CLOCK_DOMAIN 0 LOCKED / UNLOCKED | 10 / 9 | 10 / 10 | 11 / 10 | C1: UNLOCKED as the servo leaves LOCKED, LOCKED when it reads LOCKED again; LOCKED is UNLOCKED or UNLOCKED + 1 |
| DUT STREAM_INPUT 1 MEDIA_UNLOCKED | 0 | 1 | 0, the bank reset at the bind | The Stream Input's MEDIA_UNLOCKED |

The 1 before the unbind is the toggle of the set to CLOCK_SOURCE 1. The DUT's
CRF output was not bound and counted nothing. `SLIP_TDM` stayed static. The
tone path through the whole observation, 25.8 s graded as a segment, has no
discontinuity of any kind and 0 net steps, every block at the floor: the
holdover kept the DUT's clock on the peer's rate. With lane B7's AAF
observation, the lock loss is now observed for both kinds of followed source.

### B8: the saved selection across a power cycle

Case PC. The pass is the processor's "the selection kept as saved state":
after a cold boot, GET_CLOCK_SOURCE returns the saved index and the servo
re-locks on it.

<!-- b8-power-cycle -->
| Step, CEST | Observed |
|---|---|
| 18:48:37, as found | CLOCK_SOURCE 0; every stream unbound; NVM image seq 30, 30 commits since boot |
| 18:48:37, set | The peer's AAF talker bound to STREAM_INPUT 0 under the binding rule; SET_CLOCK_SOURCE 2 SUCCESS, read back 2; servo LOCKED 6.67 to 7.17 s after the set |
| 18:48:45, saved | NVM 31 commits, image seq 31 in slot A, `dirty=0` and `commit_busy=0`, but `pend=1`: `nvm_pend`, accepted work that no verified slot holds ([SAVED_STATE_FASTCONNECT 9.1](../design/SAVED_STATE_FASTCONNECT.md#91-the-bits)). It read 1 at every NVM read before the cycle, so the status alone does not show the selection held in a slot; the read of 2 after the cold boot does |
| 18:49:51, the power cycle | The DUT's outlet switched off, 8 s, and on, by the power strip's documented command under the bench lock; the command returned at 18:49:59.7 |
| 18:50:00 to 18:50:08, boot | First console byte 0.3 s after the strip's command returned; BIOS CRC passed; the firmware copied the AEM image (CRC `5ba355eb`) and took NVM slot A seq 31, `VD_OK`, nothing rolled back; its prompt 8.4 s after the first byte |
| 18:51:19, boot verdict | UART grader 10 of 10 at its first run: the boot PASSES |
| 18:51:28, after the boot | GET_CLOCK_SOURCE 2, the first command sent. STREAM_INPUT 0's format `0205022001006000` and its binding to the peer's talker, connection count 1, restored by the DUT itself. Since the boot: CLOCK_DOMAIN LOCKED 1, UNLOCKED 0; STREAM_INPUT 0 MEDIA_LOCKED 1, MEDIA_UNLOCKED 0 |
| 18:51:28, re-lock | Servo LOCKED at the first poll, with no state-changing command sent (only the reads above) |
| 18:51:34, restore | SET_CLOCK_SOURCE 0, read back 0; the unbind; the format restored and read back |
| 18:51:52, identity | The gate PASSES, verdict byte-equal |
| 18:52:41, end | NVM image seq 33, slots 33 and 32, `VD_OK`; 2 commits since the boot |

The saved index survived the cold boot: the first GET_CLOCK_SOURCE after it
read 2, and the domain counted one LOCKED and no UNLOCKED since the boot, so
the servo locked on the restored source and stayed locked. The boot to LOCKED
time was not measured: the first poll came about 89 s after the strip's
command returned. The DUT also restored its listener binding without a
controller, and the peer's AAF talker counted one STREAM_STOP and one
STREAM_START across the cycle. That is recorded, not analysed; it is outside
#629. Item 4 PASSES.

NVM commits: 30 before the set, 31 after it with image seq 31, which the boot
restored; the commit counter restarts at boot, and after the restore it read
1, then 2 at the end, image seq 33. `pend` read 0 at the first read after the
boot, 1 after the restore's first commit and 0 at the end.

### B8: bench as left

| State | As left |
|---|---|
| DUT stream state | All unbound; both audio maps empty, read back |
| DUT clock domain | CLOCK_SOURCE 0, read back |
| DUT STREAM_INPUT 0 format | `0205022002006000`, as found, read back |
| DUT itself | Power-cycled once, as authorised; the same image booted (identity gate PASS) |
| Reference peer | Every stream unbound; its CLOCK_DOMAIN on INTERNAL and its STREAM_INPUT 0 format as found |
| Census, the resume against the end | 43 of 46 entries equal. The other three are the boot's: the DUT talkers' destination addresses, which MAAP allocated again at the boot, and the live propagation delay, 385 ns before and 378 ns after |
| DUT saved state | NVM slots seq 33 and 32, `VD_OK`, 2 commits since the boot |
| The tone | No playback in the second session; none left |
| SoC board | Same boot; both bridge legs running with the script's command lines under new process IDs; PCM states, USB function and fault scan as at the start |
| Controller host | No task process; staging removed |
| Bench host | Both USB audio devices present; the board link's address present; the bench lock free |

Residuals that no permitted command restores:

- **The power cycle.** The DUT's counters and words that clear only on reset
  restarted at the boot. At the end `SLIP_LB` read 6 dups and `RENDER_STAT`
  0 rails. The 6 dups, three slipped frames, were already there at the first
  poll after the boot, 18:51:28, and did not change to the end. They fell
  after the DUT restored its binding to the peer's AAF talker, since a ring
  that is not fed counts nothing, and before that poll, when the servo read
  LOCKED on CLOCK_SOURCE 2. They were not timed, and are offered to
  [#645](https://github.com/kebag-logic/milan-fpga/issues/645) as untimed data.
- **DUT NVM persistence** advanced through the method's format, map and
  clock-source edits, 12 commits before the cycle, and the restore's 2 after.

### B8: #629 acceptance

Lane B8 changes these judgements in [B7: #629 acceptance](#b7-629-acceptance):

| #629 item | Judgement after lane B8 | Evidence |
|---|---|---|
| Fabric: recover the media clock from the selected AAF stream; gated on the live selection; a switch re-locks with no undeclared discontinuity | Met for recovery and gating, and for a switch between the AAF and CRF streams. Not met for the switch from INTERNAL to AAF: its ring slip after LOCKED repeated ([#645](https://github.com/kebag-logic/milan-fpga/issues/645)) | [B8: the source switch](#b8-the-source-switch): both stream-to-stream switches with one `mr` toggle, one CLOCK_DOMAIN pair, LOCKED in the declared time and no slip. [B8: the INTERNAL-to-AAF set and #645](#b8-the-internal-to-aaf-set-and-645): `SLIP_LB` 420 to 422, 2.0 to 3.0 s after LOCKED |
| Lock loss: declared holdover and restart, and `mr` per IEEE 1722-2016 4.4.4.3 | Met for both sources | AAF: [B7: lock loss of the followed AAF stream](#b7-lock-loss-of-the-followed-aaf-stream). CRF: [B8: lock loss of the followed CRF stream](#b8-lock-loss-of-the-followed-crf-stream) |
| Protocol processor: SET/GET_CLOCK_SOURCE over the longer list, the selection kept as saved state | Met at the bench | SET_CLOCK_SOURCE 1 and 2 answer SUCCESS and read back (lanes B7 and B8); the saved index 2 read back after a cold power cycle and the servo re-locked on it ([B8: the saved selection across a power cycle](#b8-the-saved-selection-across-a-power-cycle)) |
| Bench quality metric: THD+N and SNR of a known tone on the selected path | Met for Direction A, by lane B7; NOT met for Direction B | Item 1 NOT RUN: the known tone does not reach the peer's talker ([B8: the tone proof](#b8-the-tone-proof)) |
| Every other item | As judged in [B7: #629 acceptance](#b7-629-acceptance) | - |

So not every #629 item is met. Direction B's THD+N stays open, and the switch
from INTERNAL to AAF keeps #645's undeclared ring slip. #629 stays open.

### B8: limits

- Item 1 did not run: Direction B has no THD+N or SNR on this image.
- The audio the DUT receives is not graded, because the peer's talker carries
  no known signal. The ring, junction and render words and the listener
  counters stand in for it.
- The poll samples every 0.5 s. A HOLDOVER of one reference presentation at a
  stream-to-stream switch, or a converged-bit low under 0.5 s, can fall
  between polls. The recentre count is not readable on silicon.
- The windows are shorter than lane B7's: holds of 120 to 150 s and a 420 s
  CRF window, because each bench command had to end within 10 minutes.
- The CRF window's three host stalls hid 18.7 s of its audio: the capture path
  lost 899,009 frames, and the three stall clusters 18.69 s of them. The
  lock-loss segment had no read stall over 17 ms.
- `mr` toggles are counted at both ends (GET_COUNTERS), not captured on the
  wire.
- The boot-to-LOCKED time after the power cycle was not measured.
- The tool controls ran after the cases.
- One run per item, on one DUT, against one reference peer.
- Printed precision is not calibrated accuracy.

### B8: artifact hashes

The raw files stay outside the lane packet, on the bench host. The SW and
CRFLL runs' `events.jsonl` record the size and SHA-256 of their capture files;
the packet's `RAW-ARTIFACTS.json` records every raw file by run directory, and
is the only record of the tone proof's recording hash, the full grades and the
boot record. Both withhold the size of each run's 10 s all-channel snippet,
because it would state the capture's channel count.

| Run | Raw file | Bytes | SHA-256 |
|---|---|---|---|
| Tone proof | `mcasp-all.raw` (McASP0's 10 s recording, 8 channels) | 15,360,000 | `b1dc772d8fcbce5e417d6777eff9cbe4df2053b9f82b8eda5a8251e3da93ecdd` |
| SW | `cap-lr.raw` (the tone's two channels) | 131,630,514 | `7174b4b371f07a5cacbdaed8c55b6b6a43508b5f34ea14417993a00997e12aba` |
| SW | `cap-ts.bin` (capture read times) | 1,096,824 | `f4ffbc449d1be25d0c165504220b88f97f62339c8abba15f8400d74fa21699cd` |
| SW | `samples.txt` (McASP0 timing samples) | 282,406 | `9fae925f02ef0e90c5c79b4619dc594a89d25c6494231eb45cdc0a92c4437830` |
| SW | `poll-run.jsonl` (the console poll) | 273,517 | `b87415d67a9a02480031c5dcc2329e64a201a7515dcc4f366610ef9d420b772c` |
| SW | `grade-full.json` (`grade_b8.py`) | 261,492 | `781bdce7cbe9fc013a886d5fc9c106e1fd2591870cea81e9ce67fe3988ac8bf1` |
| CRFLL | `cap-lr.raw` | 134,401,140 | `4893d40c9ee2419a0fa2be8dff4519543fe0d8729e2806304efddfb56119c625` |
| CRFLL | `cap-ts.bin` | 1,118,760 | `bc29bd13613aab102d9eda792db1bc1c19929495c287cc9d156d56bc65d68260` |
| CRFLL | `samples.txt` | 300,629 | `d6c64a8c22ce2d95f54ea0ecd8ecd173db2c4190c858725cc033fa130cd7b86f` |
| CRFLL | `poll-run.jsonl` | 279,654 | `56374e82d76deac49cfeadc2514ad09b6b733bcb955b504ffecb8fc6cd57c79b` |
| CRFLL | `grade-full.json` | 259,633 | `2bd5f3b7f3145ad42ca3aa5162cfe2cde1981bce4f10a5b85c3b46970aac732f` |
| CRFLL | `grade-lockloss-full.json` (the lock-loss segment) | 35,316 | `41a0d0fd0b25bc759641fb56c90f69f980d2dc55363a969b7793dd0da73c7e7e` |
| PC | `boot-console.jsonl` (the boot, recorded without typing) | 16,508 | `6b9f5408b06af16039e855cad6b5df2553555bc722887d10721b75532609ef9e` |

The lane packet, `629-b8-a521`, holds the evidence and the tools. Its manifest
covers every retained file except itself. Redaction passes masked private
identifiers in 79 packet files, and `redaction.json` records each masked
file's original and retained SHA-256. Every row below is the retained file.
Four tools are masked: `b8_tone.py` and `tone_play_b8.sh` where they describe
the tone source; `run_b8.py` at one line, an assertion on the capture's
sample-format name; and `grade_b8.py` at one docstring line that stated the
capture's channel count. Each is a record of the tool as run, not a runnable
copy, and `redaction.json` holds its as-run SHA-256. The external capture's
sample-format name and channel count are masked, and this page states
neither. The code that decodes the capture's samples, their byte width and
byte order, is not masked: it is generic and needed to reproduce the grading,
as in lanes B6 and B7
([the manager's ruling](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5971696657)).
The second session's pass masked `tone_play_b8.sh` further, so its retained
SHA-256 is no longer the `9574c591...` that the first session's version of
this section gave.

**Where the packet is.** It is published on branch `629-b8-review-evidence`,
pinned at commit `36ee6d8adca255ad5228c4258a3186a5f0cbc574`. The packet label
`629-b8-a521` maps to `review-evidence/629-b8-r1/author/` there:
`summary/sw/switches.json` is
`review-evidence/629-b8-r1/author/summary/sw/switches.json`.
`review-evidence/629-b8-r1/MANIFEST.json` gives each file's `original_sha256`,
the lane packet's file, beside the published file's `published_sha256`. The
packet was first published at `5bad6a43`, where `grade_b8.py` still stated the
channel count. `36ee6d8a` masked that one line, on top of the branch with no
force-push, and changed no other packet file; `5bad6a43` stays in the branch's
history as published. The publication also masked host identifiers, USB
positions and interface and account names, in eight restore records,
`restore/controller-*.txt` and `restore/host-*.txt`. `MANIFEST.json` alone
records their two hashes, and no row below cites them.

Every row below equals its file's `published_sha256` at `36ee6d8a`. For
`grade_b8.py`, `MANIFEST.json` records the tool as run as its
`original_sha256`. The published `redaction.json` predates that mask; the lane
packet's `redaction.json` records both of its hashes from round 2 on. For the
other three masked tools the lane packet already held them masked, and
`redaction.json` alone holds the as-run hash. Every raw row above is recorded
in `RAW-ARTIFACTS.json` at `36ee6d8a`.

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `summary/sw/switches.json` (`b8_events.py`: every set, its polls and counters) | 23,494 | `6257fcaffb8550c4cc3e1187e3897c35cb77cdf1772e1080dcd0d77bc7561412` |
| `summary/sw/grade.json` (the SW span's grade, reduced) | 33,363 | `63db6f78abd9ea9d24300c363559fce0a45f860a66d5524876df2e6d6bea793a` |
| `summary/crfll/lockloss.json` (`b8_events.py`: the window, the unbind and the rebind) | 17,372 | `a2955d3f264c5987e34066915a1a38816084f28df8b517a976a9d52fd538885c` |
| `summary/crfll/grade.json` (the CRF window's grade, reduced) | 27,112 | `440f971d489ff0c0bd3aeae0dcf1efdcc82c6f4ab5b3df1638d10b449f8de600` |
| `summary/crfll/grade-lockloss.json` (the lock-loss segment's grade, reduced) | 21,764 | `5bdc35226dfa67c1778086617b492d3a345fd22dd12cad006609ff5543302823` |
| `summary/pc/pc.json` (`b8_events.py`: the power cycle) | 6,863 | `437a04a7fa5c665ef2f2997a2653f302e8728a77f2704c1fc26ac90cf40dc031` |
| `runs/sw/events.jsonl` | 43,104 | `9082adeb40c7bd8b7f2d830937581f693ab1d23963091111b8180cb71465ead4` |
| `runs/crfll/events.jsonl` | 29,972 | `fc7c4142fc649bcacba81efd5ed964d680996cd79baecb327bd122029aa1ed58` |
| `runs/pc/events.jsonl` | 13,950 | `8723e4283aeef842a61eac0249e7a549a0ab15eb8a64e523c75a24f1a490953d` |
| `runs/pc/boot-console.txt` (the boot record as text) | 4,834 | `77563cb770ff9eb205b7c0cf2738141d13ed298c34dde1a81b8a50475dfe63ba` |
| `runs/pc/grader-boot-0.txt` (the boot verdict) | 683 | `dd1b55157fa03c12917d1def4acf7f02dd0c1dfc6f79507f1189ec8fcb6f9008` |
| `controls/controls.json` (tool controls) | 17,070 | `7bbefc71fb3c9303a8f1cb843bfcd13dafe55c1f3e1a968e6a3b3cee2350530e` |
| `identity/identity-verdict.txt`, `identity-resume/` and `identity-postboot/` (each byte-equal) | 3,037 | `ff817aca4909f1030c9296cfac3bc6af41994323e7b0a41610a505359d1422d4` |
| `restore/census-compare-r2.txt` (the resume against the end) | 1,565 | `e7ba4858ad1c0b5ad4550ed7d1446f43f53c4107ae5b6d17c2a18191e680a323` |
| `summary/proof/proof.json` (`b8_proof.py`'s grade of the recording) | 1,104 | `6b68262b0b546d2d6f706d86bb422c8622a930d12e3bab0feeca9dd9f3757281` |
| `runs/proof/events.jsonl` (the probe's steps) | 1,851 | `8245bc33f848e7cc4120b2c432d5c949e5307e41d08da65f00749f954630e086` |
| `runs/proof/ctl.jsonl` (the probe's controller transactions) | 15,059 | `e2ce6e8c1724e39f10d7f126909ed09af8bd62e9825704a91c0ffb87404b8ecd` |
| `runs/proof/soc-record.log` (the recording's board transcript) | 624 | `bb554bd49a0e73f6e763662652622f13500fc15f2af5b979f0dc98fd3664637f` |
| `restore/census-compare.txt` (the first session) | 64 | `1bfd339c3dd7dbdaad13ed256feaef4ae27b3bf4d9731d53440ea0868a0889d0` |
| `tools/run_b8.py` (masked; as run `efd07d51...`) | 33,824 | `05a37d7c73907e5c63ba4d1ee18eb268adaa462c171ba9e364f80c1489a9b4f3` |
| `tools/grade_b8.py` (masked; as run `330c14cd...`) | 27,959 | `77949fd1f73000a7cb123a54034dcf92f728e6d53475faba014d74265dcf81cd` |
| `tools/b8_events.py` | 16,325 | `2b848d3e007ddce3eb6ddf0077816e3c306f7bdadb08b71a8b33852b89faafc3` |
| `tools/console_poll_b8.py` | 4,345 | `1912837a1e4cfd6a1f8b3615b4d26924efbfd430aff239ebd18cd4dd2a67d4f7` |
| `tools/pc_b8.py` | 14,053 | `188c08ed957ef777210d47660f5ddcc37c99c7a521b2bf84d2266dd6c91cb020` |
| `tools/pc_cycle_b8.sh` | 2,371 | `f4f8e252585bd3c1088ef4ad5e82921fdccc4d3ffeaac5e04877fce1d756af7b` |
| `tools/console_listen.py` | 1,897 | `f980541a361df87e7b09ce6d20e70a19db60a2d1391b6720f174428ca94df0bb` |
| `tools/b7_decode.py` (unchanged from lane B7) | 10,093 | `a5eb63f29a19d608bbbc25c840943e5da15f3366a4887b62b221cc2d631110f4` |
| `tools/probe_b8.py` | 10,722 | `10bcffd340c3a8653622c0ba1acc005d54b35ccd88297ed1d080a31c01f74749` |
| `tools/b8_proof.py` | 2,809 | `953ee95d064c7d65be980ee7d7c7d53c417e1996830f879ec92a6a557add3f3c` |
| `tools/b8_tone.py` (masked) | 2,262 | `fc7a84c60b1f6a6f01a202b790aa4e22eb06a356c2b509bbbeeb0afcefb6efaa` |
| `tools/tone_play_b8.sh` (masked) | 2,263 | `39678d09809d78739b386907fda744021fd400d7684bec0aea51078b457eb916` |
| `tools/b6_thdn.py` (unchanged from lane B6) | 12,423 | `d4673f55642b850f57601b27d8fc930cc5382c2138f54edb1a7296bb4653a95f` |
| `tools/b6_tone.py` (unchanged from lane B6) | 2,965 | `d188a1a9ac0c3d94a2dab7d7b44ff7487490c87b969ea8c7d1b69382743179ac` |

## Dev 5603c353, 2026-10-10: lane B15

Refs #629. Operator [A588], 2026-10-10, under the
[bench lane B15 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6097827871).
The image is the manager's build of dev `5603c353`, as flashed and booted. No
flash, JTAG reload or power cycle occurred in this lane.

Lanes B8 to B10 stopped at "tone absent": the DUT's STREAM_INPUT 0 locked and
counted frames, but its TDM output carried no tone. Nobody had examined where
along the path the tone was lost. This lane played the known tone, captured
four points of its path at the same time and located the loss:

- (a) the reference peer's own talker stream, on the peer's link, from a
  passive tap there;
- (b) the same stream as it arrives on the DUT's link, from the DUT's tap;
- (c) the DUT's TDM output, recorded by McASP0 on the SoC board;
- (d) the external audio capture, as a control.

| #629 bench item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `5603c353` | PASS | The assignment's ATDECC and console facts. See [B15: identity and setup](#b15-identity-and-setup) |
| Tool controls | PASS | Lanes B6 and B9's controls byte-equal to lane B10's; the new tap decode 5 of 5 and the new alignment 5 of 5. See [B15: the controls](#b15-the-controls) |
| Format check before every bind | Held | Every listener read against its talker; one listener format set, read back and restored. See [B15: method](#b15-method) |
| Where the tone is lost | Upstream of the peer's talker | Absent at (a), (b) and (c) in both runs, at the same idle floor. See [B15: where the tone is lost](#b15-where-the-tone-is-lost) |
| The DUT's receive and render path | Loses nothing | Its TDM output equals the stream it receives, 480,000 of 480,000 frames in both runs. See [B15: the DUT renders what it receives](#b15-the-dut-renders-what-it-receives) |
| Positive control of the same observation chain | PASS | A tone on the DUT's own talker is found on both taps and at the external capture, with THD+N at the loop's 24-bit floor |
| Direction B: B0, B-CRF, B-AAF by THD+N and SNR | NOT RUN | The tone does not reach the DUT; the assignment's branch for "absent at (a)" is a STOP |
| A DUT fix | Not needed | The DUT does not lose the tone |
| Restore | Done | See [B15: bench as left](#b15-bench-as-left) |

These are operator observations, not review verdicts. Paths such as
`runs/pts1/events.jsonl` are in the lane packet, `629-b15-a588`; where it is
published is in [B15: artifact hashes](#b15-artifact-hashes).

### B15: identity and setup

| Identity check | Result |
|---|---|
| Over ATDECC, the live ENTITY descriptor | entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001" |
| Console `milan_status` | ID `4d494c4e`, VERSION `0x00020060` |
| AEM image CRC32 in QSPI, 7,512 bytes | `5ba355eb` |
| Live ENTITY and CONFIGURATION | Byte-equal to the QSPI AEM bytes the console dumps, 312 and 106 bytes |
| Clock sources of #629 | CLOCK_SOURCE 0 INTERNAL; 1 INPUT_STREAM on STREAM_INPUT 1, the CRF input; 2 INPUT_STREAM on STREAM_INPUT 0, the AAF input; CLOCK_SOURCE 3 answers NO_SUCH_DESCRIPTOR; CLOCK_DOMAIN 0 lists 0, 1 and 2 and reads 0 |
| UART grader | 10 of 10 |
| ADP | The DUT with entity model `001bc5c1935893e1` |
| Identity gate | PASS, 15:17:48 to 15:17:54 CEST |

The gate does not read the BIOS ROM or bitstream payload CRCs: the lane holds
no build values for dev `5603c353` to compare them with. The flash record is the
manager's.

As found:

- **DUT.** Every stream unbound. STREAM_INPUT 0 at the peer talker's
  `0205022001006000`; STREAM_PORT_INPUT 0 with four identity mappings and
  STREAM_PORT_OUTPUT 0 with eight. CLOCK_DOMAIN 0 on CLOCK_SOURCE 0. NVM image
  seq 272, 38 commits, `pend=0`.
- **Reference peer.** Its STREAM_INPUT 0 bound to the DUT's AAF talker and its
  CRF input bound to the DUT's CRF talker, with its CLOCK_DOMAIN on the source
  located on that CRF input: lane B7's A2 arrangement. Its STREAM_INPUT 0 at
  `0205022002006000`.
- **SoC board.** Reached only over key-based SSH on its USB network link; its
  serial console was not used. The to-host bridge leg was running and the
  from-host leg was dead, as found. The USB function was configured.
- **Controller host.** No gPTP daemon, no staging.

### B15: method

**The tone.** Lane B9's loop (`b9_tone.py`: lane B6's 997 Hz and 9,973 Hz at
-20 dBFS), SHA-256 `d9684a8f...`, equal to lanes B9 and B10's. It was played
into the reference peer's talker inputs by the owner's method, through the
authorised tone source, from 15:26:59 to 15:35:31 CEST. Starting and stopping
that playback, one read of the tone source's state, passive reads of its meters
and the external capture's recordings were the only instrument actions; no
instrument setting was written.

**The four points.** Each run is one locked action:

- The peer's STREAM_OUTPUT 0, its AAF talker, is bound to the DUT's
  STREAM_INPUT 0 under the binding rule. The DUT's as-found input map holds the
  four identity mappings the method needs, and the tool edits no map.
- Both taps record AVTP frames for 24.5 s.
- The external capture records 16 s.
- McASP0 records the DUT's TDM output for 10 s, eight channels.

The board's to-host bridge leg holds McASP0's capture. It was stopped by the
process ID its `status` names, after a command-line check, and restarted with
its recorded line. Both taps put a 28-byte record header with the direction
port before each frame.

**The decode** (`tone_points_b15.py`). It selects one stream by its stream ID
and the tap's direction port. Each AAF AVTPDU (IEEE 1722-2016 clause 7) is
checked for format, channel count, bit depth and length, and its sequence
numbers, `tv` and `mr` are counted. The 24-bit sample is bits 31:8 of each
big-endian 32-bit word. Per channel, the tool gives the RMS level and the share
of the channel's power within 5 Hz of each tone. A tone is present on a channel
when that share exceeds 0.9 at -40 dBFS or more, lane B8's rule. Lane B6's
`block_metrics` then gives each whole one-second block's level, frequency,
SNR and THD+N.

| Run | Window, CEST | Point (d) | Result |
|---|---|---|---|
| `pts1` | 15:27:19 to 15:27:59, captures from 15:27:28.7 | The peer's STREAM_INPUT 0 bound to its own talker | Tone absent at (a), (b) and (c); (d) unusable, see [B15: the controls](#b15-the-controls) |
| `pts2` | 15:31:03 to 15:31:44, captures from 15:31:13.1 | The as-found binding of the DUT's AAF talker to the peer, with lane B6's loop played into the DUT's TDM input | Tone absent at (a), (b) and (c); the positive control present at both taps and at (d) |

**Binding rule record.**

| Bind or set | Talker format | Listener format read | Set on the listener | Read back |
|---|---|---|---|---|
| Peer AAF to DUT STREAM_INPUT 0, `pts1` and `pts2` | `0205022001006000` | `0205022001006000` | None, equal | - |
| Peer AAF to the peer's STREAM_INPUT 0, `pts1` | `0205022001006000` | `0205022002006000` | `0205022001006000`, SUCCESS | `0205022001006000` |
| DUT AAF to the peer's STREAM_INPUT 0, the as-found bind remade in `pts1` | `0205022002006000` | `0205022002006000` | None, equal | - |

Every bind answered SUCCESS with connection count 1 and every unbind
connection count 0. No clock source was set on either entity. The peer's
STREAM_INPUT 0 format was set back to `0205022002006000` and its as-found bind
remade. Each run ended with every format, clock source, binding and map read
back equal to the run's start, except one flag in `pts1`: the peer's
STREAM_INPUT 0 rx state read flags `0x0002` right after the rebind, against
`0x0082` before. It read `0x0082` again at `pts2`'s start and at the end.

### B15: where the tone is lost

Levels are RMS over the whole capture. "Share" is the channel's power within
5 Hz of the tone.

<!-- b15-points -->
| Run | Point | Channel | Level, dBFS RMS | Range, 24-bit LSB | Share at 997 Hz / 9,973 Hz | Either tone |
|---|---|---|---|---|---|---|
| `pts1` | (a) the peer's talker, on the peer's link | 0 / 1 / 2 / 3 | -141.09 / -141.10 / -141.48 / -141.49 | -2 to +1, -2 to 0, -1 to 0, -1 to 0 | 0.04 % / 0.04 % on every channel | Absent |
| `pts1` | (b) the same stream, on the DUT's link | 0 / 1 / 2 / 3 | -141.09 / -141.10 / -141.48 / -141.49 | As at (a) | 0.04 % / 0.04 % on every channel | Absent |
| `pts1` | (c) the DUT's TDM output | 0 / 1 / 2 / 3 | -141.09 / -141.10 / -141.48 / -141.49 | -2 to 0, -2 to 0, -1 to 0, -1 to 0 | 0.03 to 0.04 % / 0.04 % | Absent |
| `pts1` | (c), the unmapped channels 4 to 7 | 4 to 7 | Every word zero | 0 | - | - |
| `pts1` | (d) the peer's digital output | Its two channels | Every word zero | 0 | - | Absent; the control is unusable |
| `pts2` | (a) the peer's talker, on the peer's link | 0 / 1 / 2 / 3 | -141.09 / -141.10 / -141.48 / -141.48 | -2 to +1, -2 to 0, -1 to 0, -1 to 0 | 0.04 % / 0.04 % on every channel | Absent |
| `pts2` | (b) the same stream, on the DUT's link | 0 / 1 / 2 / 3 | -141.09 / -141.10 / -141.48 / -141.48 | As at (a) | 0.04 % / 0.04 % on every channel | Absent |
| `pts2` | (c) the DUT's TDM output | 0 / 1 / 2 / 3 | -141.09 / -141.10 / -141.48 / -141.48 | -2 to 0, -2 to 0, -1 to 0, -1 to 0 | 0.03 to 0.04 % / 0.04 to 0.05 % | Absent |
| `pts2` | (d) the peer's digital output, carrying the DUT's talker | Its two channels | See the control below | | | The control's tone present |

With no tone, there is no frequency, SNR or THD+N to fit. A flat floor puts
0.04 % of a channel's power in a 10 Hz band.

| Run | Point | AAF PDUs | Sequence gaps | `tv` clear | `mr` toggles | Format, every PDU |
|---|---|---|---|---|---|---|
| `pts1` | (a) | 191,843 | 0 | 0 | 0 | INT_32BIT, 4 channels, 32-bit depth, 96-byte payload, 48 kHz |
| `pts1` | (b) | 191,842 | 0 | 0 | 0 | As at (a) |
| `pts2` | (a) | 191,639 | 0 | 0 | 0 | As at (a) |
| `pts2` | (b) | 191,637 | 0 | 0 | 0 | As at (a) |

The peer's talker carries no tone on its own link. Its four channels hold an
idle floor of one to two LSB of 24 bits, -141 dBFS. That floor is lanes B6 to
B10's at the DUT's output, unchanged. It is the size of digital silence with
dither, not of a converter's analog noise. That is an observation about its
size only; this lane cannot see inside the peer. The same stream arrives on the
DUT's link with no sequence gap, and the DUT renders it, as the next section
shows. The loss is therefore upstream of the peer's talker: in the tone's path
into the peer's talker inputs, or inside the peer. Under the assignment that is
instrument-side, and the lane stops there.

### B15: the DUT renders what it receives

`align_b15.py` compares the DUT's TDM output, (c), with the stream on the DUT's
link, (b), on the four mapped channels. It locates the recording's first
256-frame window in the stream by exact match, then walks every frame.

| Run | First window's matches in the stream | Frames compared | Equal | Slips | Differing frames | Verdict |
|---|---|---|---|---|---|---|
| `pts1` | 1 | 480,000 | 480,000 | 0 | 0 | SAMPLE-EXACT |
| `pts2` | 1 | 480,000 | 480,000 | 0 | 0 | SAMPLE-EXACT |

Every frame of McASP0's 10 s recording equals, on all four channels, a frame of
the stream the DUT received, in order. The DUT ran on INTERNAL and the peer
followed the DUT's CRF, so no slip was expected. The DUT's STREAM_INPUT 0
counters agree:

| Run | MEDIA_LOCKED / UNLOCKED | STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET | TIMESTAMP_NOT_VALID, UNCERTAIN, LATE, EARLY | UNSUPPORTED_FORMAT | FRAMES_RX across the captures |
|---|---|---|---|---|---|
| `pts1` | 1 / 0 at both reads | 0, 0, 0 | 0, 0, 0, 0 | 0 | +191,998 in 24.5 s |
| `pts2` | 1 / 0 at both reads | 0, 0, 0 | 0, 0, 0, 0 | 0 | +199,998 in 24.5 s |

FRAMES_RX counts per committed observation interval of at most 1 s, so the two
increments are 24 and 25 committed intervals, not a frame rate.

So the depacketiser, the channel map, the sample conversion and the TDM render
lose nothing here. No stage of the DUT was localised, no RTL or firmware was
changed and no suite check was added: the assignment's DUT branch did not apply.

### B15: the controls

**Tool controls.** Lanes B6 and B9's and the tap decode's ran before any
capture was graded. The alignment's ran after its first use, as stated below.

| Control | Result |
|---|---|
| `b6_thdn.py controls` | Byte-equal to lane B10's `controls.json`, `7bbefc71...` |
| `b9_thdn.py controls` | Byte-equal to lane B10's `b9-controls.json`, `728a4f0e...` |
| `tone_points_b15.py control`: a synthetic tap capture, the tone pair on channels 0 and 1 and a foreign stream interleaved | Every sample recovered exactly; both tones found at -20.00 dBFS and 0.000 ppm; 0 gaps. PASS |
| The same with the tone on channels 2 and 3 | Found on 2 and 3 only. PASS |
| One PDU dropped | One sequence gap, at that PDU. PASS |
| The stream on the other direction port | Not taken. PASS |
| One LSB of floor only | TONE ABSENT. PASS |
| `align_b15.py control`, on `pts1`'s stream at (b): an exact copy; one frame dropped; one frame repeated; one sample changed by 1 LSB; another stretch with channel 0 negated | SAMPLE-EXACT; one slip of +1; one slip of -1; one differing frame; no match. PASS, 5 of 5 |

A slip's position is exact only up to a run of equal consecutive frames,
because the floor has few values. The alignment control computes that position
from the content. Its first run expected the planted index and failed the drop
case by one frame; the expectation was corrected and all five passed. The two
alignments had already run with the same comparison code, which the correction
did not touch.

**Point (d) in `pts1` is unusable.** The peer's STREAM_INPUT 0 was bound to its
own talker, so that (d) would witness the talker without the DUT. A switch does
not send a frame back out of the port it arrived on, so that listener received
nothing. Its counters stayed 0 and its digital output read exact zero. The run
is recorded as run, and `pts2` gave (d) a working control instead.

**The positive control, `pts2`.** McASP0 played lane B6's loop into the DUT's
TDM input: 997 Hz on channel 0 and 9,973 Hz on channel 1, at -1 dBFS, SHA-256
`566d3dfa...`. The DUT's as-found output map carries it on its AAF talker. The
peer's as-found listener renders it on its digital output. The same taps,
decode and capture then find it:

<!-- b15-control -->
| Point | 997 Hz on the stream's channel 0 | 9,973 Hz on channel 1 | Blocks at the loop's floor |
|---|---|---|---|
| The peer's link tap, the DUT's talker | -1.00 dBFS, 997.0000 Hz, SNR 146.07 dB, THD+N -146.06 dB | -1.00 dBFS, 9,973.0000 Hz, SNR 145.99 dB, THD+N -145.99 dB | 15 of 23 |
| The DUT's link tap, the DUT's talker | As above | As above | 15 of 23 |
| (d) the external capture, the peer's digital output | As above | As above | 13 of 16 |

The figures are the median one-second block. Every block wholly inside the
playback is at the loop's 24-bit floor, so the tone arrived sample-exact at all
three points. The other blocks hold no playback, or its start or end. So the
chain that finds no tone at (a) and (b) finds one where one is.

### B15: the tone source and the peer, read only

Under the assignment's branch for a tone absent at (a), the playback and
routing state was read and nothing was changed.

- **The tone source.** Its state was read once before the playback, and its
  level meters during it, without writing any setting. The tone left it at
  -38.5 dBFS on the outputs that carry it and on no other output. Its playback
  read -20.0 dB, and those outputs' level setting read -18.5 dB; nothing was
  changed. The state read and the meter rows are held privately, as the
  loop's layout is. The packet's only trace of them is `runs/tone-start.txt`.
- **The peer, over ATDECC reads.** The published start survey,
  `restore/peer-descs.jsonl` at 15:19 CEST, read the peer's current
  configuration, 1. GET_AUDIO_MAP on its STREAM_PORT_OUTPUT 0 gives its
  talker's channels 0 to 3 from that port's clusters, base 16, by identity
  mappings. Its CONFIGURATION counts and its AUDIO_UNIT 0 port fields declare
  no JACK_INPUT, no external or internal port, and one CONTROL.
- **The survey's 20 NO_SUCH_DESCRIPTOR answers.** The same survey has 20
  NO_SUCH_DESCRIPTOR answers in configuration 1, to its reads of indices 0 to
  19 meant as the stream ports' clusters. Each of those reads carries
  descriptor type `0x0010` (its `what` field, `desc-peer-1-0x0010-<i>`, and
  its payload). IEEE 1722.1 Table 7.1 gives `0x0010` to EXTERNAL_PORT_INPUT;
  AUDIO_CLUSTER is `0x0014` (`avdecc/aem_descriptors.py:103`). The inherited
  survey's audio-unit walk uses the wrong code, the defect a
  [review on PR #628](https://github.com/kebag-logic/milan-fpga/pull/628#issuecomment-5926558221)
  recorded. So those answers say that the peer has no EXTERNAL_PORT_INPUT 0 to
  19, which agrees with its AUDIO_UNIT fields, and say nothing about its
  clusters.
- **A second read, held privately.** At 15:35:10 CEST the lane read the peer's
  AUDIO_CLUSTER 0 to 19 with type `0x0014`, in configuration 1, the same
  configuration as the survey. Its descriptor payloads are held privately.
  Every read answered SUCCESS, and clusters 16 to 19, STREAM_PORT_OUTPUT 0's,
  each give signal_type AUDIO_UNIT, signal_index 0 and signal_output 0. The two
  reads disagree only because they asked for different descriptor types.
  The same read found one CONTROL, IDENTIFY.

So the path from the peer's physical inputs to its talker's channels is not
described over ATDECC, and this lane cannot read or check it. The lane's
conclusion does not rest on the private read. It rests on the tap decode at
(a) and on the published CONFIGURATION and AUDIO_UNIT fields.

The owner decides any instrument change.

### B15: bench as left

| State | As left |
|---|---|
| DUT stream state | Unbound; STREAM_INPUT 0 at `0205022001006000`; both maps as found; CLOCK_SOURCE 0; all read back |
| Reference peer | Its STREAM_INPUT 0 bound to the DUT's AAF talker at `0205022002006000`, its CRF input bound, its CLOCK_DOMAIN on the same source, all as found |
| Census, start against end | 45 of 46 entries equal; the other is the DUT's live propagation delay, 381 to 387 ns |
| DUT saved state | NVM image seq 276, 42 commits, `pend=0`, `VD_OK` |
| The tone | Stopped by its process ID at 15:35:31; the playback closed |
| SoC board | Same boot; the to-host leg running under a new process ID with its recorded line; the from-host leg dead, as found; USB function configured; no lane file left |
| Controller host | No task process; staging removed |
| Tap host | No capture file left |
| Bench host | Both USB audio devices present; the board link's address present; the bench lock free |

Residuals that no permitted command restores:

- **DUT NVM persistence** advanced through the two binds of STREAM_INPUT 0 and
  their unbinds: commits 38 to 42.
- **`SLIP_LB`** read 146 dups at the start and 152 at the end, 3 slipped
  frames on the loopback ring. The DUT was on INTERNAL while the peer's talker
  was bound, as with lanes B8 and B9's probe. It was not polled, so the slips
  are not timed. They are unexplained: the
  [register map](../reference/REGISTER_MAP.md#0x8d4-----media-boundary-slip-counters--slip-kl_chan_map_capture)
  reads `SLIP_LB` as static under one media clock, and
  [#645](https://github.com/kebag-logic/milan-fpga/issues/645) tracks the
  ring's slips.

**One incident.** In `pts1` the to-host leg was stopped on purpose, by its
process ID, at 15:27:19.7 CEST, so that McASP0 could record. Its restart
checked for a running leg with a `ps` pattern. The pattern matched the SSH
command's own line, so at 15:27:55 the restart printed
`LEG_PRESENT_NOT_STARTED` and the leg was not restarted; that is where the
unintended part began. The leg was restarted at 15:28:23 under the lock, with a
check that reads the bridge's `status`. It was down about 63 s in all, by the
board's uptime in `soc/pts1-legs.log`. `pts2` used the corrected check.

### B15: #629 acceptance

Lane B15 changes no judgement in [B8: #629 acceptance](#b8-629-acceptance). It
adds evidence to one item:

| #629 item | Judgement after lane B15 | Evidence |
|---|---|---|
| Bench quality metric: THD+N and SNR of a known tone on the selected path | Met for Direction A, by lane B7; NOT met for Direction B | The known tone is absent in the peer's own talker stream, on the peer's link, so no Direction B case can be graded on it. The DUT renders the stream it receives sample-exactly. See [B15: where the tone is lost](#b15-where-the-tone-is-lost) |
| Fabric, lock loss, protocol processor | As judged after lane B8, with #645 open | - |
| Every other item | As judged in [B7: #629 acceptance](#b7-629-acceptance) | - |

So not every #629 item is met, and #629 stays open.

### B15: limits

- Two runs, each with 10 s of McASP0 and about 24 s of each tap, on one DUT
  against one reference peer.
- The alignment shows the DUT renders the floor it receives, sample for sample.
  The positive control shows the DUT's own talker and the peer's listener carry
  a tone sample-exact. Neither grades the DUT rendering a tone it receives,
  which needs a tone at (a).
- The peer's path from its inputs to its talker is not observable over ATDECC.
  The floor's size is an observation, not a diagnosis.
- The tone source's routing is shown by its meters, not by a read of its
  routing setting.
- Printed precision is not calibrated accuracy.

### B15: artifact hashes

The raw files stay outside the lane packet, on the bench host. The packet's
`RAW-ARTIFACTS.json` records each one. The external capture's sizes are
withheld there and here, because they would state its channel count.

| Run | Raw file | Bytes | SHA-256 |
|---|---|---|---|
| Tap probe | `b15-tapprobe-peer.pcap` (200 frames) | 54,510 | `5a8bdcecfcfa3fa1091f8fbc163a4b27b7d1b9a2e15796a717495353a05281f3` |
| Tap probe | `b15-tapprobe-dut.pcap` (200 frames) | 54,336 | `9ea90bd6add9a8cf98f6b5e88dd7ac1accaaac71096a5c78cba990709484ec7e` |
| `pts1` | `tap-peer.pcap`, (a) | 36,979,626 | `6abff90594872f7c5fb0cfc13c82f7578d1bb00b22e9d5f0db092e2f5417fae1` |
| `pts1` | `tap-dut.pcap`, (b) | 36,979,440 | `3e1d81ba2e507e0f5d7b9e05304c9cf81e4bb0c6d477bf0dbb0fdb8574008443` |
| `pts1` | `mcasp-all.raw`, (c) | 15,360,000 | `7e059d75bf3c1d0340f9542ca68e3f6ddf3660614d542ffb4f072c176b42fdc7` |
| `pts1` | `extcap.raw`, (d) | Withheld | `7040fae17dc84aaed803b8122608d5bd23e0864928df5e3498230fa0862745b9` |
| `pts2` | `tap-peer.pcap`, (a) and the control | 90,982,432 | `9d408d76279056d9dd64eb0cc6f6fdd6c861629a7813c5a85daea5f1d8af8556` |
| `pts2` | `tap-dut.pcap`, (b) and the control | 90,981,496 | `88c41bc5c8d781517e71a84844ff933b024ed054f7af3be07ad15fcbc8740ff3` |
| `pts2` | `mcasp-all.raw`, (c) | 15,360,000 | `1a331755a46b87868fc941932581f4ee94af6528831ad9b6597b4c02f10869e0` |
| `pts2` | `extcap.raw`, (d) | Withheld | `fa771dccc383b4b463ee3d27684b3d2f8414c86d6a1a6a14461cc2b6c44abeb1` |
| `pts2` | `b6-loop.raw`, the control's loop | 1,536,000 | `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588` |

**Where the packet is.** It is published on branch `629-tone-review-evidence`,
pinned at commit `06148614c910d3986991dd130f95d073b4bbe491`. The packet label
`629-b15-a588` maps to `review-evidence/629-tone-r1/author/` there:
`runs/pts1/events.jsonl` is
`review-evidence/629-tone-r1/author/runs/pts1/events.jsonl`.
`review-evidence/629-tone-r1/MANIFEST.json` gives each file's `original_sha256`,
the lane packet's file, beside the published file's `published_sha256`. The
publication masked three files: the local tool path in `gates/gates.txt`, and
a USB function name and USB position in `restore/host-start.txt` and
`restore/host-end.txt`. `MANIFEST.json` alone records their two hashes, and no
row below cites them.

Every row below equals its file's `published_sha256` at `06148614`, which for
each of them is also its `original_sha256`. The lane packet already held
`tone_points_b15.py` masked, and `redaction.json` alone holds its as-run hash.
Every raw row above is recorded in `RAW-ARTIFACTS.json` at `06148614`.

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/tone_points_b15.py` (the tap decode and the per-point presence verdicts; masked, as run `3adb505f...`) | 16,207 | `a899f2e7a746265338606f1cfd7f41543d6e2f540b02e1c8022d05d13766f608` |
| `tools/align_b15.py` (the SAMPLE-EXACT verdicts) | 6,399 | `701554820de6dcb532caf90052116226d7d80e858daa012ef540b87e07e497a3` |
| `controls/b15-tap-controls.json` (the tap decode's controls) | 924 | `f69bf5cf4002cd0059c938bfa6bac76ce4a398bae223918facd34a2f290e7b7c` |
| `controls/b15-align-controls.json` (the alignment's controls) | 961 | `d46f7bc52148f5f3a3cd82f7000f119d4e27e31150c2c54f4ce55c1cf75b959e` |
| `summary/pts1/align-b-c.json` (`pts1`'s alignment of (c) with (b)) | 340 | `e4b04e3fb99ae69540fee9a4d7535c8b1281df226147fd0390852467e3a9d951` |
| `summary/pts2/align-b-c.json` (`pts2`'s alignment of (c) with (b)) | 340 | `fc0edb9c1774f4464b761bd10a0841815b99bca4de251c5c9362d4ae4d4d58ad` |
| `runs/pts1/events.jsonl` | 6,213 | `063f01784e0b308cdc34cf154d4d603e8f7bf84fa6eb31ec0d7db52b10a851de` |
| `runs/pts2/events.jsonl` | 6,007 | `c81c682006b884e7f3cd3e6cb01df9895df4a6f74b7bbbaa2580e2cf83442db4` |
| `restore/census-compare.txt` (the start against the end) | 369 | `a38dca80e66a1e108f7e9418ba33dba47e56fc6b2c7cd6420dadea3f2ff7164f` |

## Dev 5603c353, 2026-10-12: lane B16

Refs #629. Operator [A603], 2026-10-12, under the
[assignment of bench lane B16](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187).
The image is the manager's build of dev `5603c353`, as flashed and booted. No
flash, JTAG reload or power cycle occurred in this lane.

Lane B15's capture found the known tone absent already in the reference peer's own
talker stream. The maintainer has since reported that the peer's path from
its talker inputs to its talker works in loopback. This lane's first task was
to reproduce that loopback as the positive reference: the peer's own listener
bound to its own talker, the tone played into the peer's talker inputs, and the
peer's output graded at the external capture.

The loopback did not form. The peer's listener, bound to its own talker,
sent its probe for that talker onto the network and never received an
answer, so it never learned the stream and the talker never started. The
external capture read exact zero. Under the assignment that is a STOP, and the
lane stopped at step 2. After the manager's ruling it resumed as B16b; see
[B16b: the resume](#b16b-the-resume). After the second ruling it resumed as
B16c; see [B16c: the resume](#b16c-the-resume). The second findings round,
documents only, is in
[B16, round 2: reduced receipts](#b16-round-2-reduced-receipts), the third
in [B16, round 3: figures check](#b16-round-3-figures-check), the fourth in
[B16, round 4: packet and coverage](#b16-round-4-packet-and-coverage), and the
fifth in [B16, round 5: every digit](#b16-round-5-every-digit), and the sixth in [B16, round 6: the closed list](#b16-round-6-the-closed-list), and the seventh in [B16, round 7: no markup](#b16-round-7-no-markup), and the eighth in [B16, round 8: the parser](#b16-round-8-the-parser), and the ninth in [B16, round 9: source extents](#b16-round-9-source-extents).

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `5603c353` | PASS | The assignment's ATDECC and console facts. See [B16: identity and setup](#b16-identity-and-setup) |
| Tool controls | PASS | Lanes B6 and B9's byte-equal to lane B15's; the tap decode 8 of 8 and the full-value alignment 6 of 6, both with new controls. See [B16: the controls](#b16-the-controls) |
| Step 2, the loopback as the positive reference | TONE ABSENT; no stream formed. STOP | Two runs. The peer's listener never resolved its own talker's stream, and its digital output read exact zero. See [B16: the loopback](#b16-the-loopback) |
| Where this setup and the working loopback differ | At the bind | The peer sends its probe for its own talker to the network, twice, 200 ms apart, and no answer arrives. Lane B15's `pts1` failed at the same step. See [B16: the loopback](#b16-the-loopback) |
| The tone source, read only | Playing, routed as in lane B15's read, and to a second pair | The tone left it on the outputs the documented wiring uses, as in lane B15. It now also leaves on a second pair of outputs, which lane B15's read found silent. See [B16: the tone source, read only](#b16-the-tone-source-read-only) |
| Step 3, the talker stream with the loopback carrying the tone | NOT RUN | No loopback carried the tone. The peer's talker sent no PDU on its link in either run |
| Step 4, Direction B end to end; B0, B-CRF, B-AAF | NOT RUN | The lane stopped at step 2 |
| A DUT fix | Not applicable | No DUT stage was reached |
| Restore | Done | See [B16: bench as left](#b16-bench-as-left) |

These are operator observations, not review verdicts. Paths such as
`runs/loop2/events.jsonl` are in the lane packet, `629-b16-a603`; where it is
published is in [B16: artifact hashes](#b16-artifact-hashes).

### B16: identity and setup

| Identity check | Result |
|---|---|
| Over ATDECC, the live ENTITY descriptor | entity_id `020000fffe000001`, entity name "Milan FPGA 1x1 TDM8", firmware_version "2.96.0", serial "AX7101-0001" |
| Console `milan_status` | ID `4d494c4e`, VERSION `0x00020060` |
| AEM image in QSPI, 7,512 bytes, its CRC32 | `5ba355eb` |
| Live ENTITY and CONFIGURATION | Byte-equal to the QSPI AEM bytes the console dumps, 312 and 106 bytes |
| Clock sources of #629 | CLOCK_SOURCE 0 INTERNAL; 1 INPUT_STREAM on STREAM_INPUT 1; 2 INPUT_STREAM on STREAM_INPUT 0; CLOCK_SOURCE 3 answers NO_SUCH_DESCRIPTOR; CLOCK_DOMAIN 0, which lists 0, 1 and 2 and reads 0 |
| UART grader | 10 of 10 |
| ADP | The DUT with entity model `001bc5c1935893e1` |
| Identity gate | PASS, 05:45:06 to 05:45:12 CEST |

The gate is lane B15's (`identity_b16.sh`, `identity_b15.py`), unchanged but
for its environment and staging. The flash record is the manager's.

As found, at 05:45 CEST, the bench was in lane B15's end state:

- **DUT.** Every stream unbound. STREAM_INPUT 0, at the peer talker's
  `0205022001006000`; STREAM_PORT_INPUT 0, with four identity mappings, and
  STREAM_PORT_OUTPUT 0, with eight. CLOCK_DOMAIN 0, on CLOCK_SOURCE 0. NVM image
  seq 276, 42 commits, `pend=0`. `SLIP_LB` 152 dups.
- **Reference peer.** Its STREAM_INPUT 0, bound to the DUT's AAF talker, at
  `0205022002006000`, and its STREAM_INPUT 8, bound to the DUT's CRF talker. Its
  CLOCK_DOMAIN on the source located on that CRF input. Its STREAM_OUTPUT 0, the
  AAF talker, at `0205022001006000` with connection count 0.
- **SoC board.** Reached only over key-based SSH; its serial console was not
  used. The to-host bridge leg running, the from-host leg dead, and its McASP
  playback closed: no other playback was running. The USB function was
  configured.
- **Controller host.** No gPTP daemon, no staging.

### B16: method

**The tone.** Lane B15's: lane B9's loop (`b9_tone.py`, 997 Hz and 9,973 Hz
at -20 dBFS), SHA-256: `d9684a8f...`, played into the reference peer's talker
inputs through the authorised tone source, from 05:55:37 to 06:01:59 CEST. The
lane only started and stopped that playback, read the source's state twice and
read its meters passively. No instrument setting was written.

**The runs.** Each run is one locked action of `run_b16.py`:

- The peer's STREAM_INPUT 0, as found bound to the DUT's AAF
  talker, is unbound and then bound to the peer's own STREAM_OUTPUT 0, under the binding
  rule. The DUT is not bound.
- For 12 s after the bind, and again after the captures, the listener's
  GET_RX_STATE, its GET_COUNTERS and the talker's GET_TX_STATE are read every
  2 s.
- Both taps and the external capture record.
- Teardown unbinds, restores the listener's format, remakes the as-found bind
  and reads every format, clock source, binding and map back.

| Run | Window, CEST | Captures | Purpose |
|---|---|---|---|
| `loop1` | 05:56:30 to 05:57:30 | Taps 30.6 s and the external capture 22 s, from 05:56:45 | The loopback, as assigned |
| `loop2` | 05:59:18 to 06:00:28 | Taps 52.5 s from 05:59:19, before the bind; the external capture 16 s from 05:59:36 | The same, with the bind's ACMP exchange on record |

`loop2` was added after `loop1`. `loop1`'s taps started after the bind, so
they held none of its messages.

**Binding rule record.**

| Bind | Talker format | Listener format read | Set on the listener | Read back |
|---|---|---|---|---|
| Peer AAF to the peer's STREAM_INPUT 0, `loop1` and `loop2` | `0205022001006000` | `0205022002006000` | `0205022001006000`, SUCCESS | `0205022001006000` |
| DUT AAF to the peer's STREAM_INPUT 0, the as-found bind remade | `0205022002006000` | `0205022002006000`, after its restore | None, equal | - |

Every bind and unbind answered SUCCESS. No clock source was set on either
entity, and the DUT was not bound. Each run ended with every format, clock
source, binding and map read back equal to its start.

**Grading rules, fixed before any capture.** The presence rule is lane B15's
(share of the channel's power within 5 Hz of a tone above 0.9) with one change.
The level floor is -100 dBFS instead of -40 dBFS, because the tone leaves the
source at about -38.5 dBFS and a converted tone could sit below -40 dBFS.
A channel present between -100 and -40 dBFS is flagged, so lane B8's rule can
still be read off. The loopback is graded by THD+N and SNR at the external
capture where a tone is present.

### B16: the loopback

The peer's listener, polled every 2 s after the bind:

| Run | Reads | Listener stream ID and destination | Listener flags | Talker connection count | MEDIA_LOCKED, FRAMES_RX |
|---|---|---|---|---|---|
| `loop1` | 14, over 12 s after the bind and 12 s after the captures | `0000000000000000`, `000000000000` at every read | `0x0002` at every read | 0 at every read | 0, 0 at every read and at both counter marks |
| `loop2` | 14, likewise | The same | The same | The same | The same |

The bind itself answered SUCCESS with connection count 1. The listener never
learned the talker's stream ID or destination, and the talker's connection
count stayed 0.

The bind's ACMP exchange in `loop2`, from the peer's link tap. Times are from
the controller's UNBIND_RX command:

| Time, ms | Direction | Message | Talker, listener | Result |
|---|---|---|---|---|
| 0.0 | Controller to the peer | UNBIND_RX command | The DUT's AAF talker, the peer's STREAM_INPUT 0 | - |
| 0.0 | The peer | UNBIND_RX response | - | SUCCESS, connection count 0 |
| 0.1 | Controller to the peer | BIND_RX command | The peer's STREAM_OUTPUT 0, the peer's STREAM_INPUT 0 | - |
| 99.6 | The peer | BIND_RX response | The same | SUCCESS, connection count 1, stream ID 0 |
| 99.6 | The peer, to the network | PROBE_TX command | The peer's own STREAM_OUTPUT 0 | No response |
| 299.6 | The peer, to the network | PROBE_TX command, again | The same | No response |

Milan's PROBE_TX is IEEE 1722.1's CONNECT_TX. No PROBE_TX response and no
further probe appear in the rest of the capture, 49.6 s after the second probe.

So the peer resolves its own talker over the network, as for any talker, and
nothing answers. A switch does not send a frame back out of the port it
arrived on, and the peer evidently does not answer its own probe internally. Its
listener therefore never learns the stream, never declares it, and the talker
never starts. Neither tap holds a PDU of the peer's talker stream in either
run:


| Run | Point | Content | Either tone |
|---|---|---|---|
| `loop1` | The peer's link, its talker stream | 0 PDUs; the link carries only the DUT's CRF stream to the peer | Absent: no stream |
| `loop1` | The DUT's link, the peer's talker stream | 0 PDUs | Absent: no stream |
| `loop1` | The external capture, the peer's digital output | Its two channels: every word zero, 1,056,000 frames | Absent |
| `loop2` | The peer's link, its talker stream | 0 PDUs; the link carries the DUT's CRF stream to the peer, and its AAF stream until the unbind | Absent: no stream |
| `loop2` | The DUT's link, the peer's talker stream | 0 PDUs | Absent: no stream |
| `loop2` | The external capture, the peer's digital output | Its two channels: every word zero, 768,000 frames | Absent |

With no tone at any point, there is no frequency, SNR or THD+N to fit, and no
point carries the talker for step 3's tap to decode.

Lane B15's `pts1` bound the same listener to the same talker, and lane B15's
record shows the same: its counters stayed 0 and its output read exact zero. That lane
attributed it to the switch not reflecting the talker's frames. Its tap did
not cover the bind. This lane's record places the failure a step earlier:
the stream is never started, because the listener's probe goes unanswered.

So the loopback the maintainer reports working is not this bind on this
network path. It must differ: another network path, a different bind, or a
loop outside ATDECC. The lane cannot tell which, and the owner holds that
setup. Under the assignment's step 2, the lane stops here. The tone was absent
at the loopback's output, the levels below are recorded, and the source's
routing was read read-only.

### B16: the tone source, read only

The tone source's state was read before the playback and again at its end,
at 05:47 and 06:01 CEST. The two reads are identical. Its level meters were
read passively while the tone played. Nothing was written.

The read method changed from lane B15's. Another client of the source's
control service held the reply port that lane B15's read binds. This lane
observed the service's replies passively on the host instead, binding no port.
Each state read sent the service's documented state read request, as lane
B15's did.

| Source outputs | Before the output level setting | Output level setting | Leaving the source | Lane B15 |
|---|---|---|---|---|
| The pair the documented wiring uses | -20.0 dBFS on each | -18.5 dB | -38.5 dBFS on each | The same |
| A second pair | -20.0 dBFS on each | +6.0 dB | -14.0 dBFS on each | Silent, same setting |
| Every other output | Silent: no reading above -135.2 dBFS | - | Silent: no reading above -147.6 dBFS | Silent |

The playback reads -20.0 dBFS, so it reaches the documented pair at 0 dB, as
the owner's condition requires. The second pair is new: lane B15's read found it
silent with the same output setting. So the route from the playback to that
pair changed after lane B15, outside this lane. The documented wiring
does not include that pair, and the lane did not change it.

The two state reads hold 2,262 entries each, all equal. The reduced receipt
`r2/source-receipt.json` carries that comparison, the settings and the meter
levels above; see
[B16, round 2: reduced receipts](#b16-round-2-reduced-receipts).

This is the per-channel record the assignment asks for: the source's two
documented outputs carry the tone at -38.5 dBFS. The peer's output, its talker
stream and the DUT's link carry nothing, because no stream formed.

### B16: the controls

**Tool controls.** All ran before any capture was graded.

| Control | Result |
|---|---|
| `b6_thdn.py controls` | Byte-equal to lane B15's `controls.json`, `7bbefc71...` |
| `b9_thdn.py controls` | Byte-equal to lane B15's `b9-controls.json`, `728a4f0e...` |
| `tone_points_b16.py control`: lane B15's five controls | PASS, 5 of 5, each record equal to lane B15's |
| The same, new: the tone pair at -60 dBFS on a one-LSB floor | Present on both channels, flagged below lane B8's floor, at -60.00 dBFS. PASS |
| The same, new: a -130 dBFS tone alone | Its share is 1.0, but it is below the level floor: absent. PASS |
| The same, new: eight channels with the tone pair on channels 5 and 6 | Found there only. PASS |
| `align_b16.py control synth`: lane B15's five planted cases on a synthetic tone stream | PASS, 5 of 5 |
| The same, new: one sample changed by +256 LSB, its low byte unchanged | One differing frame. PASS. Lane B15's `align_b15.py` reads the same recording SAMPLE-EXACT, because it keys on each sample's low byte |

`align_b16.py` was built for step 4, which did not run. Its new control shows
why lane B15's alignment needed the change for a stream that carries a tone.

**The positive reference itself is the control this lane lacks.** The loopback
was to show the tone through the peer before the DUT was involved. It did not
form, so nothing downstream of the source was graded on a tone.

### B16: bench as left

| State | As left |
|---|---|
| DUT stream state | Unbound; STREAM_INPUT 0, at `0205022001006000`; both maps as found; CLOCK_SOURCE 0, INTERNAL; all read back |
| Reference peer | Its STREAM_INPUT 0, bound to the DUT's AAF talker, at `0205022002006000`, its STREAM_INPUT 8 to the DUT's CRF talker, its CLOCK_DOMAIN on the source on that CRF input, never set; all as found |
| Census, start against end | 44 of 45 reads equal, the census's start record aside; the other is the DUT's live propagation delay, 387 to 377 ns |
| DUT saved state | NVM image seq 276, 42 commits, `pend=0`, `VD_OK`, unchanged: the DUT was not bound |
| The tone | Stopped by its process ID at 06:01:59 CEST; the playback closed |
| SoC board | Same boot; the to-host leg running with the process ID it had as found, never stopped; the from-host leg dead, as found; McASP playback closed; USB function configured |
| Controller host | No task process; staging removed |
| Tap host | No capture file left |
| Bench host | Both USB audio devices present; the board link's address present; the bench lock free |

Residuals that no permitted command restores:

- **The DUT's AAF talker** counted two more stream stops and starts, one per
  run, when the peer's listener was unbound from it and bound back.
- **On the peer's STREAM_INPUT 0, the counters** restarted at the rebind: their
  TIMESTAMP_VALID and FRAMES_RX read lower at the end than at the start.
- **`SLIP_LB`** read 152 dups at both ends, unchanged.

### B16: acceptance of #629

Lane B16's findings change no judgement in [B15: acceptance of #629](#b15-629-acceptance).

| Item of #629 | Judgement after lane B16 | Evidence |
|---|---|---|
| Bench quality metric: THD+N and SNR of a known tone on the selected path | Met for Direction A, by lane B7; NOT met for Direction B | The positive reference could not be formed, and no Direction B case ran. See [B16: the loopback](#b16-the-loopback) |
| Bench, both directions, each followed source | As judged after lane B8 | - |
| Fabric, lock loss, protocol processor | As judged after lane B8, pending #645 | - |
| Every other item | As judged in [B7: acceptance of #629](#b7-629-acceptance) | - |

So #629's items are not all met, and the issue stays open.

### B16: limits

- Two loopback runs, each about a minute, on this bench's reference peer only.
- The loopback was tried as an ATDECC bind on this bench's network only. The
  maintainer's working loopback is not described in public. This lane shows
  only that this bind cannot carry it.
- Whether the peer's talker now carries the tone is not shown: its talker
  never started. The new route of the playback to a second pair of source
  outputs makes that worth checking. A capture with the DUT's listener bound
  to the talker, lane B15's method, would show it; the STOP precedes it.
- The tone source's playback routes are shown by its meters, before and after
  each output's level setting, not by a read of a routing setting.
- Printed precision is not calibrated accuracy.

### B16: artifact hashes

The raw files stay outside the lane packet, on the bench host. The packet's
`RAW-ARTIFACTS.json` records each of them. The external capture's sizes are
withheld there and here, because they would state its channel count.

| Run | Raw file | Bytes | SHA-256 |
|---|---|---|---|
| `loop1` | `tap-peer.pcap`, the peer's link | 1,567,518 | `0f4c6b42f6792dc84d8ba89d93e9edb97add667bf236b2d06833256ba14f1b0b` |
| `loop1` | `tap-dut.pcap`, the DUT's link | 1,567,518 | `a879b24feec3f4cdd4d72522d152afce4a1f6b527ce6a8210213c9779a6d9036` |
| `loop1` | `extcap.raw`, the external capture | Withheld | `afff760831cd795283185c800d86460a1216511be9ebeb90a00baebc2ce8d0e2` |
| `loop2` | `tap-peer.pcap`, the peer's link, with the bind | 8,752,338 | `6e0e1f4271d31495bd4d4c33ca4f5a55d791c9c3c8540a53b584abc505696776` |
| `loop2` | `tap-dut.pcap`, the DUT's link | 8,680,530 | `898242c513f4f30be70d0b3386f983e536f4bc4e5d63eaf341149b47aa6ac276` |
| `loop2` | `extcap.raw`, the external capture | Withheld | `265d9585facf0aa1d6766454a5a0c1a871ae1449e0850e7de7f684b32b03067c` |

The packet's evidence files, as retained after its redaction pass
(`redaction.json` gives each masked file's original and retained hashes):

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/b16-asrun/run_b16.py` (the runs, as run in B16; `tools/run_b16.py` is B16b's extension) | 18,087 | `d1a60cc2be9af3d8a3f81424ce468441ceeae88c960d817c127de5816f27a289` |
| `tools/tone_points_b16.py` (the presence verdicts) | 19,842 | `975645309ecb92d124b28d488c74902a2aea9379470e3eec563f1d93ea20869c` |
| `tools/align_b16.py` (the full-value alignment) | 7,802 | `71fd639b5db4c00f4048c6f2930330ee6880388613459a0d7411d577ab3eac86` |
| `tools/acmp_tap_b16.py` (the ACMP decode) | 2,949 | `8c686a58e5c0288623c50cd7a40b273a6d0336b66af9765f0214a4dffaf57f65` |
| `controls/b16-tap-controls.json` | 1,565 | `77a5995f07b9e300b5d819477e70441ed7ba3a26848e881ec6841219867da8fe` |
| `controls/b16-align-controls-synth.json` | 1,176 | `20ca766eb693b2f2252f6de97efda18c94455ade5d661813a8e26fd604b1d276` |
| `runs/loop1/events.jsonl` | 11,587 | `0390182f646584223bceeaf240e47135be383e47ddd56b4d15950336a441f954` |
| `runs/loop2/events.jsonl` | 11,656 | `cb3a5ffada5c35cdbbbbacc866e3f15abeded2e706754e9b3958479f75a0e2c0` |
| `summary/loop2/acmp-peer-tap.json` (the bind's ACMP exchange) | 8,739 | `ecd9b4589b9508322c587938417550fa7dcb3a6eaee2065261e3ad73dabf6688` |
| `summary/loop1/d-extcap-pair.json` | 664 | `496e6ad34ad164d1b8fea06c92d8ed099e3e831386c58d4b192d7881dfc64704` |
| `summary/loop2/d-extcap-pair.json` | 661 | `17f6c33f990654a1dd6dae8e5277ecd874955337cac66f0cfeb94eac33f549a5` |
| `restore/census-compare.txt` (the start against the end) | 369 | `3a9a17cfc7ab6849571b9b2221c4981e8a19b7f460f1f66c30f9293a43f2de6f` |
| `identity/identity-verdict.txt` | 1,532 | `4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130` |

**Where the packet is.** It is published on branch `629-b16-review-evidence`,
pinned at commit `b84584e4ccb069248909f0fdeb7f8b72a1c41ae4`. There the packet
label `629-b16-a603` maps to a directory per findings round under
`review-evidence/629-b16-r1/`, each a copy of the packet as that round left
it: `author-r1/` for lanes B16, B16b and B16c, archived with this page at
`e20fd282`; `author-r2/` for round 2, at `35e332b6`; and `author-r3/` for
round 3, at `0782c55f`. So `runs/loop2/events.jsonl` is
`review-evidence/629-b16-r1/author-r3/runs/loop2/events.jsonl`. Round 4's
packet is in `author-r4/`, archived with this page at `61ae8641` and published by commit `b83e5d76`; round 5's is in `author-r5/`, archived at `36190193` and published by commit `a73ce5c4`, whose tree holds every directory named here and whose `MANIFEST.json` binds them the same way. Round 6's is in `author-r6/`, archived at `e91a62ee` and published by commit `b616e7ea`, whose `MANIFEST.json` binds every directory the same way. Round 7's is in `author-r7/`, archived at `295ba9d7` and published by commit `fa974c3f`, whose `MANIFEST.json` binds every directory the same way. Round 8's is in `author-r8/`, archived at `b522bb92` and published by commit `b0134c63`, whose `MANIFEST.json` binds every directory the same way. Round 9's packet follows as `author-r9/`, in a later commit on the same branch. `tools/r9_evidence_receipt.py` checks this mapping; see [B16, round 9: source extents](#b16-round-9-source-extents).

`review-evidence/629-b16-r1/MANIFEST.json` at `b84584e4` has 1,680 entries
and SHA-256: `8d417d54b13a264484bfcb0b69f8a643e5cd3bf2819294cea201242a2f67f034`.
For each published file it gives the `original_sha256`, the lane packet's
file, beside the `published_sha256`, with a `path_redacted` flag; the
hashes differ exactly where the flag is set. The publication masked local
paths in 27 author files, 1 in `author-r1/`, 9 in `author-r2/` and 17 in
`author-r3/`: gate logs, gate results and the gate tool `tools/gates_r2.py`.
No hash row in lane B16's section names any of them. Each of the 66
packet-file rows in its tables at `0782c55f`, here, in
[B16b: artifact hashes](#b16b-artifact-hashes),
[B16c: artifact hashes](#b16c-artifact-hashes), round 2's and round 3's,
equals its file's `original_sha256`, its `published_sha256` and the published
file in `author-r3/`, by size and SHA-256. `tools/r4_evidence_receipt.py`
reads all of this from the repository's object store and writes
`r4/evidence-receipt.json`; see
[B16, round 4: packet and coverage](#b16-round-4-packet-and-coverage).

### B16b: the resume

The manager [ruled on the STOP](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117672835).
Lane B15's four-point capture was to run with the DUT's
listener bound to the peer's talker. If the tone was present at the peer's
talker, there followed step 4: B0, B-CRF and B-AAF graded by THD+N and SNR, with
every loss attributed to a stage. The operator, [A603], resumed on the same image,
branch and head, `694d7da6`; the first bench action was at 06:22:23 CEST.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `5603c353`, again | PASS | 06:22:29 to 06:22:34 CEST, every fact as in [B16: identity and setup](#b16-identity-and-setup). The bench was in lane B16's end state: census 44 of 45 reads equal, the other the DUT's live propagation delay |
| (a) The peer's talker stream on the peer's link | TONE PRESENT | 997 Hz on channel 0, and 9,973 Hz on channel 1, in every run, at -14.14 dBFS to 06:28:50 CEST and -14.10 dBFS from 06:31:51. See [B16b: the four points](#b16b-the-four-points) |
| (b) The same stream on the DUT's link | TONE PRESENT | Equal to (a), 0 sequence gaps on both taps |
| (c) The DUT's TDM output on McASP0 | TONE PRESENT | Equal to (a) and (b) sample for sample: 480,000 of 480,000 frames in three runs, and the 34.1 s the taps cover in B0, 0 slips |
| (d) The positive control at the external capture | PRESENT | Lane B6's loop through the DUT's talker and the peer's listener, at -1.00 dBFS with THD+N at the loop's floor. B0's capture holds no discontinuity in 303.8 s. `pts2` holds two 2-frame repeats that neither tap carries |
| The tone source, read only | Changed during the lane, outside it | Its clock setting changed between 06:23 and 06:50 CEST, and with it the tone at (a). See [B16b: the tone source changed during the lane](#b16b-the-tone-source-changed-during-the-lane) |
| Step 4, B0: the DUT on INTERNAL | Graded | THD+N -123.95 dB at 997 Hz and -122.80 dB at 9,973 Hz, median over 300 one-second blocks; 0 discontinuities; 0.0000 ppm. Inside the taps' 34.1 s every impairment is already in the peer's talker stream, shown sample for sample; beyond them it is assigned upstream by inference. See [B16b: B0](#b16b-b0) |
| Step 4, B-CRF and B-AAF | NOT RUN: a decision is needed. STOP | As found, the peer's clock follows the DUT's CRF talker. Either case would have the DUT follow a clock that follows the DUT. See [B16b: B-CRF and B-AAF need a decision](#b16b-b-crf-and-b-aaf-need-a-decision) |
| A DUT fix | Not needed | No DUT stage loses or alters the tone |
| Restore | Done | See [B16b: bench as left](#b16b-bench-as-left) |

These are operator observations, not review verdicts. The packet paths below,
such as `runs/b0-2/events.jsonl`, are in the same lane packet as lane B16's.

### B16b: method

Each run is one locked action of `run_b16.py` through `run_locked_b16.sh`. The
wrapper stops the SoC board's to-host bridge leg by its process ID for the
action, so that McASP0's recording can run, and restarts it with its recorded line.
Before every bind the tool checks that the board's McASP playback is closed:
the owner's music was not playing at any check.

| Run | Mode | Locked, CEST | Binds, at | Captures |
|---|---|---|---|---|
| `pts1` | `dirb` | 06:23:39 to 06:24:28 | The peer's STREAM_OUTPUT 0 to the DUT's STREAM_INPUT 0, 06:23:46 | Both taps 24.5 s from 06:23:58, the external capture 16 s, McASP0's 10 s from 06:24:02 |
| `pts2` | `dira` | 06:28:06 to 06:28:56 | The same, 06:28:13 | Taps as `pts1`, from 06:28:25. McASP0, too, plays lane B6's loop into the DUT's TDM input: the positive control, lane B15's `pts2`. It plays 2 s before it records, so its 10 s start at about 06:28:31.5, 2 s after the capture command at 06:28:29.5 |
| `b0` | `b0` | 06:31:28 to 06:37:05 | The peer's CRF talker, its STREAM_OUTPUT 2, to the DUT's STREAM_INPUT 1, then the AAF bind of `pts1`, 06:31:30 | Taps 40 s from 06:31:50, the external capture 306 s. McASP0's recording failed: an incident, below. B0's grade does not use this run |
| `b0-2` | `b0` | 06:37:31 to 06:43:17 | As `b0`, 06:37:39 | Taps 40 s from 06:37:59, the external capture 306 s. McASP0's recording lasts 300 s while the loop plays: the capture command at 06:38:03.2, then the board's 2 s of playback, so the recording starts at about 06:38:05.2 |
| `pts3` | `dirb` | 06:48:55 to 06:49:45 | As `pts1`, 06:49:02 | As `pts1`, from 06:49:14. Added after `b0-2`, to test whether the tone's change follows the CRF bind |

`dira` and `b0` keep the binding of the peer's STREAM_INPUT 0 to the DUT's AAF talker,
as found. The DUT's eight identity mappings on STREAM_PORT_OUTPUT 0 and four on
STREAM_PORT_INPUT 0: checked, not edited. Lane B6's loop (`b6_tone.py`,
SHA-256: `566d3dfa...`) was copied to the board, checked there and removed after
each run.

**Binding rule record.** Every listener format already equalled its
talker's, so none was set: `0205022001006000` on the DUT's STREAM_INPUT 0 and
`041060010000bb80` on its STREAM_INPUT 1. Every bind and unbind answered
SUCCESS. No clock source was set on either entity. The DUT's clock source read
0, INTERNAL, before and after each window of B0. Each run ended with every format, clock
source, binding and map read back equal to its start.

**Grading.** Lane B16's rules were kept unchanged. `tone_points_b16.py`
grades each point: the presence rule, the fitted level and frequency, and
THD+N and SNR per one-second block. `align_b16.py` compares (c) with (a) and
with (b) on full 24-bit values. `b9_thdn.py grade` grades McASP0's recording
with lane B9's discontinuity detector and phase offset. Its floor is the
path's own: an event-free block within 3 dB of the median. `dloop_b16.py`
decodes lane B6's loop at (d) with lane B6's decoder. SNR equals minus THD+N
within 0.01 dB in every row below.

**B0's window** is 300 s, not lane B7's 630 s, because one locked action
must end within 10 minutes. The capture command ran 24.0 s after the last
bind, and the board played the loop 2 s before it recorded (`run_b16.py`'s mode
`b0`; the board's log shows the playback running before the recording). So the
recording starts about 26 s after the last bind, past lane B7's 20 s.

**One incident.** In `b0` McASP0's recording failed immediately with "Device or
resource busy". The wrapper stopped the to-host leg only for modes `dirb` and
`dira`, and the running leg held McASP0's capture. Nothing else was affected:
the leg kept its process ID, and the binds were undone and read back. B0's grade does
not use `b0`. Its taps and external capture serve only to place the tone
source's change, and its raw files are hashed below. The wrapper then added
mode `b0`, and `b0-2` ran the case again.

### B16b: the four points

The tone in channels 0 and 1 of the peer's talker stream; channels 2 and 3
carry -1 to 0 LSB at every point, and McASP0's channels 4 to 7, unmapped, are
zero. Each THD+N cell is the median over one-second blocks, with the worst
block in brackets.


| Run | Point | Frames | Level, dBFS | 997 Hz: frequency, offset | THD+N, dB | SNR, dB | 9,973 Hz: frequency, offset | THD+N, dB | SNR, dB |
|---|---|---|---|---|---|---|---|---|---|
| `pts1` | (a) | 1,145,034; 190,839 PDUs, 0 gaps | -14.1353 | 997.0069 Hz, +6.94 ppm | -108.74 (-100.95) | 108.74 | 9,973.0692 Hz, +6.94 ppm | -88.87 (-80.97) | 88.87 |
| `pts1` | (b) | 1,149,822; 191,637 PDUs, 0 gaps | -14.1353 | 997.0069 Hz, +6.94 ppm | -107.17 (-100.80) | 107.17 | 9,973.0692 Hz, +6.94 ppm | -87.26 (-80.81) | 87.26 |
| `pts1` | (c) | 480,000 | -14.1353 | 997.0069 Hz, +6.95 ppm | -105.27 (-98.66) | 105.27 | 9,973.0693 Hz, +6.95 ppm | -85.33 (-78.67) | 85.33 |
| `pts2` | (a) | 1,149,828; 191,638 PDUs, 0 gaps | -14.1353 | 997.0069 Hz, +6.96 ppm | -107.72 (-101.02) | 107.72 | 9,973.0694 Hz, +6.96 ppm | -87.82 (-81.05) | 87.82 |
| `pts2` | (b) | 1,149,822; 191,637 PDUs, 0 gaps | -14.1353 | 997.0069 Hz, +6.96 ppm | -108.33 (-100.62) | 108.33 | 9,973.0694 Hz, +6.96 ppm | -88.44 (-80.64) | 88.44 |
| `pts2` | (c) | 480,000 | -14.1353 | 997.0069 Hz, +6.96 ppm | -109.70 (-101.43) | 109.70 | 9,973.0694 Hz, +6.96 ppm | -89.87 (-81.46) | 89.87 |
| `pts3` | (a) | 1,149,834; 191,639 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.93 (-109.28) | 123.94 | 9,973.0000 Hz, 0.000 ppm | -122.47 (-89.43) | 122.48 |
| `pts3` | (b) | 1,149,822; 191,637 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.93 (-109.31) | 123.93 | 9,973.0000 Hz, 0.000 ppm | -122.47 (-89.46) | 122.47 |
| `pts3` | (c) | 480,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.97 (-110.32) | 123.98 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-90.50) | 123.97 |
| `b0-2` | (a) | 1,919,610; 319,935 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.62 (-102.55) | 123.62 | 9,973.0000 Hz, 0.000 ppm | -114.29 (-82.58) | 114.29 |
| `b0-2` | (b) | 1,919,592; 319,932 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.62 (-102.15) | 123.62 | 9,973.0000 Hz, 0.000 ppm | -114.33 (-82.18) | 114.33 |
| `b0-2` | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.95 (-100.47) | 123.95 | 9,973.0000 Hz, 0.000 ppm | -122.80 (-80.48) | 122.80 |

The offsets are against each point's own sample clock: the stream's at (a)
and (b), the DUT's TDM clock at (c).

Point (d), the peer's digital output at the external capture:

| Run | The peer's output | Verdict |
|---|---|---|
| `pts1`, `pts3` | Its two channels at a constant -1 LSB: the DUT's talker carries its idle TDM input, and these modes play nothing into it | No control in this mode |
| `pts2` | Lane B6's loop at -1.00 dBFS, 997.0000 Hz and 9,973.0000 Hz, 0.000 ppm; THD+N -146.06 dB and -145.99 dB, the loop's floor, in 11 of the 13 blocks wholly inside the playback. Of the 16 blocks, 0 and 1 precede the playback and block 2 holds its start. Blocks 6 and 12 each hold a repeat of 2 frames, at 6.131 s and 12.113 s, net -4 frames over 665,599 decoded frames, 0 torn | PRESENT |
| `b0-2` | The loop as in `pts2`, at the floor in all 303 blocks wholly inside the playback; of the 306, blocks 0 and 1 precede it and block 2 holds its start. 0 discontinuities and 0 torn in 14,583,286 decoded frames; `b0` likewise in 14,583,189 | PRESENT |

In `pts2` both taps carry the DUT's AAF talker with the same loop at -1.00
dBFS, THD+N -146.06 dB and -145.99 dB, at the floor in all 15 blocks wholly
inside the playback. Of each tap's 23 blocks, 0 to 2 and 20 to 22 hold no
playback, and blocks 3 and 19 hold its start and end. So `pts2`'s two repeats
at (d) are not on the wire.
They arose after it: in the peer's listener, its output or the external
capture. They stopped with the tone source's change, below. The decode is lane
B6's (`dloop_b16.py`, with a planted control).

(c) against (a) and (b), on full 24-bit values:

| Run | (c) against (b) | (c) against (a) |
|---|---|---|
| `pts1`, `pts2`, `pts3` | SAMPLE-EXACT in each: 480,000 of 480,000 frames, 0 slips | SAMPLE-EXACT in each: 480,000 of 480,000 frames, 0 slips |
| `b0-2` | SAMPLE-EXACT over the 1,637,980 recorded frames the tap covers, 34.1 s, 0 differing, 0 slips | SAMPLE-EXACT over 1,637,452 frames, 34.1 s, 0 differing, 0 slips |

So the tone is in the peer's own talker stream, and the network and the DUT
carry it to the TDM output unchanged. Lane B15's capture found it absent at (a). Its
level at (a), -14.14 dBFS, is the level at which the tone source's meters show
it leaving the second pair of outputs, -14.0 dBFS. It is not the documented
pair's -38.5 dBFS. Lane B15's read found that second pair silent. Which input of the
peer the tone enters is the owner's wiring, not shown here.

### B16b: the tone source changed during the lane

The tone, lane B15's loop `d9684a8f...`, played from 06:23:26 to 06:52:19 CEST.
The source's state was read read-only at 06:23 and 06:50 CEST, and its meters
were read passively at both times. Its meters read as in lane B16, at both:
-38.5 dBFS leaving the documented pair and -14.0 dBFS leaving the second pair.
The later state read caught 1,255 of the 2,262 entries the first held. Of the
1,255 both hold, four differ, and this lane wrote none of them:

- its clock setting;
- the level setting of an output this lane does not use;
- two inputs of a monitoring mix. These differ only in which messages the
  reads caught: the first caught two messages for each address and the second
  one, which the first also caught. All of them are at minus infinity.

So, among the 1,255 entries both reads hold, two settings changed: the clock
setting and that output's level. The later read did not catch the other
1,007. The reduced receipt `r2/source-receipt.json` carries these counts and
classes; see [B16, round 2: reduced receipts](#b16-round-2-reduced-receipts).
The clock setting accounts for the change at (a):

| Runs | Tone at (a) | Offset against the stream | THD+N at (c), event-free blocks within 3 dB of the median | Phase drift at (c) | Discontinuities at (d) |
|---|---|---|---|---|---|
| `pts1`, `pts2`, to 06:28:50 | -14.1353 dBFS | +6.94 to +6.96 ppm | -109.68 and -111.26 dB at 997 Hz; -89.83 and -91.51 dB at 9,973 Hz | +3.00 and +3.01 frames in 10 s, smooth | Two 2-frame repeats in 13.9 s, `pts2` |
| `b0`, `b0-2`, `pts3`, from 06:31:51 | -14.1035 dBFS | 0.000 ppm | `pts3`: -123.98 dB on both tones; `b0-2`: -123.98 dB at 997 Hz and -123.95 dB at 9,973 Hz | 0.0000 frames in 10 s, `pts3`; 0.0005 in 300 s, `b0-2` | None in 303.8 s, `b0` and `b0-2` |

The change fell between `pts2`'s last tap frame at 06:28:50 and `b0`'s first
at 06:31:51. `pts3`, without the CRF bind, reads as `b0-2`, so the CRF bind
did not cause it. In both states `b9_thdn.py` finds no discontinuity at (c) in
any run. The tone at +6.94 to +6.96 ppm advanced smoothly against the stream,
so it was resampled upstream of the peer's talker, not slipped.

The operator's record of the tone's stop (step b17 of `HANDOFF.md`) notes five
underruns in the playback's log, from 06:45:27 to 06:46:38 CEST, while this
host graded `b0-2` offline. That log was not retained: lane B16c's playback
overwrote it, so these figures rest on that record alone. No capture window
falls in that interval: `b0-2` ended at 06:43:09 and `pts3`'s taps started at
06:49:14. Lane B16's playback log, retained privately, holds no underrun
(`r3/playback-logs.json`).

### B16b: B0

B0, as in lanes B7 and B9: the DUT on INTERNAL with both of the peer's talkers
bound, its CRF to the DUT's STREAM_INPUT 1 and its AAF to STREAM_INPUT 0. The
DUT's CRF listener read MEDIA_LOCKED 1 12 s after its bind. The DUT's servo
read IDLE (`MCSRV_STAT` `0x00000020`) before the binds and after the window.
Its clock source read 0 at both marks.

`b0-2`, McASP0's 300 s at (c), graded by `b9_thdn.py`:


| Tone | Blocks | Discontinuities | Blocks at the path's floor | THD+N at the floor, dB, median (worst) | SNR at the floor, dB | THD+N, all blocks, dB, median (worst) | Level | Offset, ppm, median (largest block) |
|---|---|---|---|---|---|---|---|---|
| 997 Hz, channel 0 | 300 | 0 | 169 | -123.98 (-123.91) | 123.98 | -123.95 (-100.47) | -14.10 dBFS | 0.0000 (0.030) |
| 9,973 Hz, channel 1 | 300 | 0 | 169 | -123.95 (-120.18) | 123.95 | -122.80 (-80.48) | -14.10 dBFS | 0.0000 (0.030) |

No skip, repeat, insert, glitch or silent frame. The 997 Hz tone's phase moved
0.0005 frames over the window. The other 131 blocks at (c) hold no event
either; they sit more than 3 dB above the floor in runs of blocks: 0 to 18,
28 to 31, 43 to 44, 46 to 54 and later runs. Both taps' sample comparisons
cover the recording's first 1,637,452 frames, 34.1 s, which hold whole blocks
0 to 33. Of the 131, 23 lie there, blocks 0 to 18 and 28 to 31. There (c)
equals (a) sample for sample, so those 23 are in the peer's talker stream
already: shown directly. The other 108 lie beyond the taps, blocks 43 to 251
in thirteen runs, and include the worst block of each tone. No sample comparison
covers them. `r2/b0-2-receipt.json` lists every run.

Attribution, stage by stage. Inside the taps' 34.1 s each row is shown
directly; beyond them, where (c) has no reference, the attribution is
inference:

| Stage | Loss shown directly, inside the taps' 34.1 s | Beyond the taps, by inference only | Evidence |
|---|---|---|---|
| The tone source and the peer's path into its talker | The path's floor at -124 dB; 23 degraded blocks at (c), down to -100.61 dB and -80.63 dB (block 7); to 06:28:50, the +6.94 to +6.96 ppm offset with a floor 13 to 34 dB higher, in `pts1` and `pts2`, whose whole 10 s at (c) the taps cover | The other 108 degraded blocks at (c), down to -100.47 dB and -80.48 dB (block 224) | Inside: (a) holds each of them, and (c) equals (a). Beyond: the blocks are assigned upstream by their kind, as the 23 inside, with no discontinuity at (c); (a)'s own 39 blocks reach -102.55 dB and -82.58 dB |
| The network, (a) to (b) | None | Not observed: the taps end | 0 sequence gaps on either tap over 40 s; (a) and (b) both equal (c) over the same recorded frames |
| The DUT's listener, map and TDM render, (b) to (c) | None | That the DUT added none of the 108 is inference. Measured over all 300 s: no discontinuity and 0.0005 frames of phase drift | Sample-exact over 34.1 s; carried as received, the idle channels 2 and 3 |
| The DUT's talker, the peer's listener and its output: the positive control | None in B0 | Measured over the whole window | 0 discontinuities in 14,583,286 decoded frames, 0 net steps; all 303 blocks wholly inside the playback at the loop's floor. `pts2`'s two repeats lay after the wire and ended with the tone source's change |

The DUT renders the stream sample for sample in every frame this lane
compared: 3,077,452 against (a) and 3,077,980 against (b), over the four
runs.

**The DUT's words over B0**, from console reads before the binds and after the
window: `SLIP_TDM` 0, static; `SLIP_LB` 158 to 160 dups, one slipped frame,
and 156 to 158 in the incident run. The window at (c) holds no discontinuity,
so whatever the loopback ring slipped did not reach the TDM output inside the
graded window. The slip is not timed; the ring's slips are tracked in
[#645](https://github.com/kebag-logic/milan-fpga/issues/645).

### B16b: B-CRF and B-AAF need a decision

As found, and as the assignment restores it, the peer's CLOCK_DOMAIN follows
its CRF input, which is bound to the DUT's CRF talker. The DUT, on INTERNAL,
is the bench's media clock. Both of the peer's talkers run on the peer's media
clock, which follows the DUT's:

- B-CRF sets the DUT's CLOCK_DOMAIN to follow the peer's CRF talker;
- B-AAF sets it to follow the peer's AAF talker.

Either way, the DUT would follow a clock that follows the DUT. That closed
loop has no independent reference, so it does not test following. Lanes B7
and B8, finding the peer on its internal source, ran their following cases
that way, and lanes B9 and B10's run tools refuse to start otherwise.

The clock-source rule allows a set on the listener's CLOCK_DOMAIN only, never
on the talker's. In both cases the peer is the talker, so the lane cannot put
it on its internal source. A run in the loop would grade something other than
what B-CRF and B-AAF claim. So the lane did not run them, and stops for a
decision between:

1. a set of the peer's CLOCK_DOMAIN to its internal source for B-CRF and
   B-AAF, read back, and restored to the as-found source with a read-back;
2. B-CRF and B-AAF run in the loop as found, reported as loop cases, not as
   following;
3. step 4, closed on B0.

### B16b: bench as left

| State | As left |
|---|---|
| DUT stream state | Both STREAM_INPUTs unbound; STREAM_INPUT 0, at `0205022001006000`, and STREAM_INPUT 1, at `041060010000bb80`; both maps as found; CLOCK_SOURCE 0, INTERNAL; all read back |
| Reference peer | STREAM_INPUT 0, bound to the DUT's STREAM_OUTPUT 0, at `0205022002006000`, STREAM_INPUT 8 to the DUT's STREAM_OUTPUT 1; its CLOCK_DOMAIN on CLOCK_SOURCE 1, never set; all as found |
| Census, B16b's start against its end | 44 of 45 reads equal, the census's start record aside; the other is the DUT's live propagation delay |
| DUT saved state | NVM image seq 276 to 286, commits 42 to 52, `pend=0`, `VD_OK` |
| The tone | Stopped by its process ID at 06:52:19 CEST; the playback closed |
| The tone source | As the owner left it; the lane wrote nothing. Its clock setting differs from the lane's start |
| SoC board | Same boot; McASP playback closed; the to-host leg running with its recorded line under a new process ID; the from-host leg dead, as found; USB function configured; no lane file left |
| Controller host | No task process; staging removed |
| Tap host | No capture file and no capture process |
| Bench host | Both USB audio devices present; the board link's address present; the bench lock free |

Residuals that no permitted command restores:

- **The peer's talkers** counted five more stream starts and stops on its AAF
  talker, one per run that bound the DUT, and two more on its CRF talker.
- **The DUT's listeners'** GET_COUNTERS advanced with the binds. Its talkers'
  starts and stops and its CLOCK_DOMAIN counters did not move.
- **`SLIP_LB`** read 152 dups at the start and 162 at the end: five slipped
  frames over the five runs that bound the DUT's STREAM_INPUT 0. The console
  reads place one in each run of B0, between the read before its binds and the
  read after its window. The others are not placed, and none is timed.

### B16b: acceptance of #629

| Item of #629 | Judgement after lane B16b | Evidence |
|---|---|---|
| Bench quality metric: THD+N and SNR of a known tone on the selected path | Met for Direction A, by lane B7. Direction B: graded with the DUT on INTERNAL; NOT met for the following cases, which wait on a decision | See [B16b: B0](#b16b-b0) and [B16b: B-CRF and B-AAF need a decision](#b16b-b-crf-and-b-aaf-need-a-decision) |
| Bench, both directions, each followed source | As judged after lane B8 | - |
| Fabric, lock loss, protocol processor | As judged after lane B8, pending #645 | `SLIP_LB` counted five slipped frames over five binds of the DUT's AAF listener |
| Every other item | As judged in [B7: acceptance of #629](#b7-629-acceptance) | - |

So #629's items are not all met, and the issue stays open.

### B16b: limits

- Four graded runs, on this bench's DUT and reference peer only. Three had
  10 s at McASP0 and about 24 s of each tap. B0's run had 300 s at McASP0, and 40 s
  of each tap.
- B0's case here is not lane B7's mismatch control. With the peer following the DUT,
  both run on the same clock, so B0's case holds no mismatch for the metric to show.
- The tone source changed during the lane, outside it. `pts1` and `pts2`
  graded it before the change, B0 and `pts3` after it.
- The path's floor and the 23 degraded blocks inside the taps' 34.1 s are
  shown in the peer's talker stream; the other 108 degraded blocks are
  assigned to it by inference. Their cause is not analysed: the source and the
  peer's input path are not observable over ATDECC.
- Printed precision is not calibrated accuracy.

### B16b: artifact hashes

The raw files stay outside the lane packet, on the bench host, and the
packet's `RAW-ARTIFACTS.json` records each of them. The external capture's
sizes are withheld, because they would state its channel count.

| Run | Raw file | Bytes | SHA-256 |
|---|---|---|---|
| `pts1` | `tap-peer.pcap`, the peer's link | 90,602,048 | `b235c4321fc2324cab2412692bd5d1b0642b73ea13549c028c1722ba9dfbc68a` |
| `pts1` | `tap-dut.pcap`, the DUT's link | 90,981,020 | `e0b086473164bf58ba304eb7b2d9e435eb412fcf11da8d246524abd18f4bb083` |
| `pts1` | `mcasp-all.raw`, McASP0 | 15,360,000 | `ff408b45488948294ed1c7bc5ce2ca13725fd0c7613e311d16fbf880f3992dd5` |
| `pts1` | `extcap.raw`, the external capture | Withheld | `02345629d6828ebe193391209b4bda618ff95f1d83b24e164996d8fcefbf75d4` |
| `pts2` | `tap-peer.pcap` | 90,981,358 | `f06bfd1ed8f486f765bce404607e88b0fda7c3e33da6d936cfa9840bfebf8b1b` |
| `pts2` | `tap-dut.pcap` | 90,980,890 | `9c6059d0b7ad9a23fe8176733d087d01b13613d96c0012244f1982a2acbaf75e` |
| `pts2` | `mcasp-all.raw` | 15,360,000 | `f3447f30211ed37e548e9746bf2c9c9e4795797d1e551dc3afae2204f7f0eb6c` |
| `pts2` | `extcap.raw` | Withheld | `08bf83e0eb4a50540517142c82ad0f386852384ae66f89fad1dd3824b9fd31e5` |
| `pts2`, `b0`, `b0-2` | `b6-loop.raw`, lane B6's loop | 1,536,000 | `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588` |
| `b0` | `tap-peer.pcap` | 153,665,476 | `075ff41dfbe12b06673eac87f2b04b78519fbb914fd987e7d6b7af4d3ae42e23` |
| `b0` | `tap-dut.pcap` | 154,049,176 | `ce0f42c6753d8acd2c214d98c9162ffcd12b566ecfab8ba6f2b38bedb67a6737` |
| `b0` | `mcasp-all.raw`, empty: the incident | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `b0` | `extcap.raw` | Withheld | `b0517ab7e64865159ba8aa319fd9084886812d8ddbf1dedbc95889740c9c41c1` |
| `b0-2` | `tap-peer.pcap` | 154,050,970 | `c0efda0683566f3b1a5299fe1ffa97f970585ce51d6ca218c7d9d825c08bbf23` |
| `b0-2` | `tap-dut.pcap` | 154,049,284 | `59bcfef4cfe31f3326360aa3b861e5a5dc7f26f45f00f94afcbc65dce286209d` |
| `b0-2` | `mcasp-all.raw` | 460,800,000 | `9b7072a2ff202841d81ffb4846697a9ebb9240ed72b66610292b4071f83486c1` |
| `b0-2` | `extcap.raw` | Withheld | `52da5d1febaebd5b03617b24f40c52ed381f57a3490ef20c4a2f6ad7a931dc7b` |
| `pts3` | `tap-peer.pcap` | 90,981,956 | `6cdf04d06b9d92d11a9fd748e0a8d94b394f2a5337f8ce7a1da52d7f962c46c0` |
| `pts3` | `tap-dut.pcap` | 90,980,912 | `f759569cdeab83ae2491346826a33cb1c8c015289ea80963400794ed52f5aed0` |
| `pts3` | `mcasp-all.raw` | 15,360,000 | `c99d7fc661f7886da65aa8e7728527699b2ee78d30102baa851ea24163ae2558` |
| `pts3` | `extcap.raw` | Withheld | `5260ce29b7d118595fa61d98435f3bab28a469448000856daa328b01c5565f2a` |

The packet's evidence files for B16b, as retained after its redaction pass
(`redaction.json` gives each masked file's original and retained hashes):

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/run_b16.py` (the runs, with modes `dira` and `b0`) | 25,161 | `424234725a2035ab9ce30512e2da1275495758283f1f483c86d982e008a43be2` |
| `tools/run_locked_b16.sh` (the locked wrapper) | 1,812 | `8694f9b0e3c38814ab55896108abbde59f04e302b9de82f690c12f41646f90fa` |
| `tools/dloop_b16.py` (lane B6's loop decoded at (d)) | 4,122 | `d3bf1a0e81b2b01bd1c12713b5ab7dbca0903c596d3fb33b6ac194e725af1ecf` |
| `controls/b16b-dloop-control.json` (its planted control) | 705 | `fbce8878a37a47b76d67fed3e450eecf57b6b3083c7ec0edc12e789e5bd775fb` |
| `runs/pts1/events.jsonl` | 8,437 | `bcd8663a9cd40acd7c4cf7c933950751527d9088432d153a9306f40ae12031fd` |
| `runs/pts2/events.jsonl` | 9,876 | `d6a68179a3dc2aed3e36a15d2e080922068e476c9163657d4aeacfbe394ac45b` |
| `runs/b0/events.jsonl` (the incident) | 11,877 | `6b9bb18043df40efeb2d93808cbca099d0988b25bfa04a91aefaaf9c3994053a` |
| `runs/b0-2/events.jsonl` | 11,883 | `d5e6d8dd6cc5b349a0aa37adad9394206fded1f221905b0e41f7d82f96dc82ab` |
| `runs/pts3/events.jsonl` | 8,435 | `a53e635e28ca361874eb2b9c5d842d45479ca69722f74ce10e27c31cd8997c40` |
| `summary/pts1/align-a-c.json` | 422 | `11bc737c7af2d4ef1cf77d234dfe275049102e65a801e5cf1ff0e8eb6548fcb3` |
| `summary/pts2/align-a-c.json` | 422 | `9cf3e2f3923e649dc20a34f9f711c4f62f0a772b41a7e7a51f28f0baaa7a8202` |
| `summary/pts3/align-a-c.json` | 422 | `dab152d9ae393ed2f20476b8e79b45d969bc3240c06a2235a49c58f2bc7f41cd` |
| `summary/b0-2/align-a-c.json` | 426 | `a24903924f8a43d07721c366966d7ee9a84a0b70f708612de079438bfb3e0da4` |
| `summary/b0-2/align-b-c.json` | 426 | `141619ca294c004ca02231eab1122a4a93ce6ddd732635c7d2e95bfbaf29bcd2` |
| `summary/b0-2/c-b9-grade.json` (B0's grade at (c)) | 135,813 | `1d554ce3a70dfb4a5ef935d139980ff0bee6cf8eb505ec42fca2781a7ed54078` |
| `summary/pts2/d-loop-decode.json` (the two repeats at (d)) | 563 | `49ce9f4c6487fcc15f41d68e5a25f36a0b83b7f994cee838e0c8204b455a21da` |
| `summary/b0-2/d-loop-decode.json` | 316 | `a58b5ebbe5a15cd3a3d216b18192b4157a5b762baa7b010be901428d9e56fd1b` |
| `restore/census-compare-b16b.txt` (B16b's start against its end) | 481 | `d14071dedb18e5cafc24421ede3cd450289d77e1af6f13f8a48c9d3c26f66648` |
| `identity-b16b/identity-verdict.txt` | 1,532 | `4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130` |

### B16c: the resume

The manager [ruled on the STOP of B16b](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6118365090).
For B-CRF and B-AAF only, the maintainer allows setting the
reference peer's clock source to its internal source over ATDECC: a
SET_CLOCK_SOURCE on the peer's CLOCK_DOMAIN, read back with GET_CLOCK_SOURCE.
After the case the peer returns to following its CRF input, as found, and that
is read back too. Every other part of the clock-source rule stands. The operator,
[A603], resumed on the same image and branch, at head `0d4ff919`. After the
offline dry run below, the first bench action was at 07:48:07 CEST.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate, dev `5603c353`, again | PASS | 07:48:16 to 07:48:22 CEST, every fact as in [B16: identity and setup](#b16-identity-and-setup). The bench was in lane B16b's end state: census 44 of 45 reads equal, the other the DUT's live propagation delay |
| Tool controls | PASS | The new run mode, dry-run offline against stand-ins in 8 of 8 scenarios, and its wrapper's deadline path. See [B16c: method](#b16c-method) |
| The peer's clock source, the ruling's exception | Set and restored, each read back | Set to INTERNAL before each case's binds, and returned to its CRF input after the DUT's binds were undone. See [B16c: clock-source record](#b16c-clock-source-record) |
| B-CRF: the DUT follows the peer's CRF talker | Graded | Servo LOCKED 2.585 to 3.161 s after the set and at all 596 polls of the window. THD+N -123.98 dB at 997 Hz and -123.97 dB at 9,973 Hz, median over 300 one-second blocks, all 300 at the path's floor; 0 discontinuities; 0.0000 ppm. Lane B6's terms: three met, the timed ratio NOT RUN. See [B16c: B-CRF and B-AAF](#b16c-b-crf-and-b-aaf) and [B16c: the following record](#b16c-the-following-record) |
| B-AAF: the DUT follows the peer's AAF talker | Graded | Servo LOCKED 6.602 to 7.180 s after the set and at all 596 polls of the window. THD+N -123.98 dB and -123.97 dB, all 300 blocks at the floor; 0 discontinuities; 0.0000 ppm. Lane B6's terms: three met, the timed ratio NOT RUN |
| The four points | TONE PRESENT at (a), (b) and (c); (d) PRESENT | (c) equals (a) and (b) sample for sample over the 34.2 to 34.3 s the taps cover in both cases. (d), lane B6's loop through the DUT's talker and the peer's listener: 0 discontinuities and 0 net steps in each case |
| Attribution | No loss in the network or the DUT | Every stage at the path's floor. See [B16c: attribution](#b16c-attribution) |
| A DUT fix | Not needed | No DUT stage loses or alters the tone |
| Restore | Done | See [B16c: bench as left](#b16c-bench-as-left) |

These are operator observations, not review verdicts. The packet paths below,
such as `runs/bcrf/events.jsonl`, are in the same lane packet as lane B16's.

### B16c: method

Each case is one locked action of `run_b16c.py` through `run_locked_b16c.sh`.
These are copies of lane B16b's tools with the modes `bcrf` and `baaf`
added. Each mode is lane B16b's `b0` with the following set of lanes B9 and
B10, in `run_b9.py` and `run_b10.py`, in this order:

1. Refuse to start unless the tone plays, the board's McASP playback is
   closed, the DUT is on INTERNAL, and the peer is on CLOCK_SOURCE 1, its
   STREAM_INPUT 8, bound to the DUT's STREAM_OUTPUT 1, as found.
2. Read the DUT's console words, then start lane B9's console poll of the
   servo, slip, meter and CRF words every 0.5 s.
3. Set the peer's CLOCK_DOMAIN to CLOCK_SOURCE 0, INTERNAL, read it back,
   and wait 5 s.
4. Bind the peer's CRF talker to the DUT's STREAM_INPUT 1 and its AAF talker
   to STREAM_INPUT 0, under the binding rule.
5. Set the DUT's CLOCK_DOMAIN to CLOCK_SOURCE 1 for B-CRF or 2 for B-AAF,
   read it back, and wait up to 60 s for the servo to read LOCKED.
6. From 20 s after the set, capture as lane B16b's B0. At McASP0, the
   DUT's TDM output is recorded for 300 s while lane B6's loop plays into the DUT's
   TDM input. The external capture covers the window, and both taps its first
   40 s.
7. Read GET_COUNTERS and GET_CLOCK_SOURCE of both entities 20 s after the
   DUT's set, about 6 s before the window, then at its middle and 15 s before
   its end, and after it.
8. Tear down: the DUT back to INTERNAL, read back; the binds undone; then the
   peer back to CLOCK_SOURCE 1, read back.

No step has each clock following the other. The McASP playback check also ran
just before the peer's set, the binds and the DUT's set; the owner's music was
not playing at any of the eight checks. The SoC board's to-host bridge leg was
stopped by its process ID for each case and restarted with its recorded line.

| Run | Locked, CEST | The peer set to INTERNAL | Binds | The DUT's set | Window at McASP0 | Teardown |
|---|---|---|---|---|---|---|
| `bcrf` | 07:50:00 to 07:56:15 | 07:50:12.3 | 07:50:17.5 | CLOCK_SOURCE 1, 07:50:29.7 | 07:50:55 to 07:55:55, from 26 s after the set | 07:56:00.0 to 07:56:04.0 |
| `baaf` | 07:56:52 to 08:03:07 | 07:57:04.1 | 07:57:09.3 | CLOCK_SOURCE 2, 07:57:21.5 | 07:57:47 to 08:02:47, from 26 s after the set | 08:02:51.7 to 08:02:55.7 |

**Before any bench action** the two modes ran offline against stand-ins for
the controller agent, the DUT's console, the SoC board, the tap host and the
captures (`tools/dryrun_b16c/`). There were eight scenarios:

- B-CRF and B-AAF as intended;
- the DUT's set refused;
- a deadline signal mid-window;
- the owner's music found before the binds;
- no servo lock;
- the peer not found as recorded;
- the controller agent ending at a bind.

Each scenario checks the order of every state-changing request and the end
state; 8 of 8 pass. The wrapper's deadline path passes too: the action's
teardown and the leg's restart finish under the lock. The first dry run
failed on a fault in a stand-in. It also showed that the teardown could not
restore the peer's clock source after the controller agent had ended. The
tool now starts a new agent for each restore step that finds the agent gone;
neither bench case needed it.

**Grading** is lane B16b's, unchanged: `tone_points_b16.py` at (a), (b) and
(c); `align_b16.py` on full 24-bit values; `b9_thdn.py grade` at (c), with
the path's floor an event-free block within 3 dB of the median; and
`dloop_b16.py` at (d). `tables_b16c.py`, new, renders the rows below from the
packet's files. SNR equals minus THD+N within 0.01 dB in every row.

### B16c: clock-source record

| Run | Step | Entity | SET_CLOCK_SOURCE | Status | GET_CLOCK_SOURCE |
|---|---|---|---|---|---|
| `bcrf` | The ruling's exception | The peer | 0, INTERNAL | SUCCESS | 0 |
| `bcrf` | The case | The DUT, the listener | 1, its CRF input | SUCCESS | 1 |
| `bcrf` | Restore | The DUT | 0, INTERNAL | SUCCESS | 0 |
| `bcrf` | Restore, after the DUT's unbinds | The peer | 1, its CRF input, as found | SUCCESS | 1 |
| `baaf` | The ruling's exception | The peer | 0 | SUCCESS | 0 |
| `baaf` | The case | The DUT | 2, its AAF input | SUCCESS | 2 |
| `baaf` | Restore | The DUT | 0 | SUCCESS | 0 |
| `baaf` | Restore, after the DUT's unbinds | The peer | 1 | SUCCESS | 1 |

At the four marks of step 7, GET_CLOCK_SOURCE read 1 or 2 on the DUT and 0 on
the peer: 20 s after the DUT's set, about 6 s before the window; at its
middle; 15 s before its end; and after it. After the restore it read 0 on the
DUT and 1 on the peer.

**Binding rule record.** Every listener format already equalled its talker's,
so none was set: `0205022001006000` on the DUT's STREAM_INPUT 0 and
`041060010000bb80` on its STREAM_INPUT 1. Every bind and unbind answered
SUCCESS. Each run ended with every format, clock source, binding and map read
back equal to its start.

### B16c: B-CRF and B-AAF

The tone sits in channels 0 and 1 of the peer's talker stream. Channels 2 and
3 carry -1 to 0 LSB at every point, and McASP0's channels 4 to 7, unmapped,
are zero. Each THD+N cell is the median over one-second blocks, with the worst
block in brackets. For comparison, the table repeats lane B16b's B0: in it the DUT
was on INTERNAL and the peer followed the DUT's CRF talker.


| Run | Point | Frames | Level, dBFS | 997 Hz: frequency, offset | THD+N, dB | SNR, dB | 9,973 Hz: frequency, offset | THD+N, dB | SNR, dB |
|---|---|---|---|---|---|---|---|---|---|
| `bcrf` | (a) | 1,919,598; 319,933 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.93) | 123.97 |
| `bcrf` | (b) | 1,919,574; 319,929 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.99 (-123.93) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.93) | 123.97 |
| `bcrf` | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.90) | 123.97 |
| `baaf` | (a) | 1,919,598; 319,933 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.98 | 9,973.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.98 |
| `baaf` | (b) | 1,919,580; 319,930 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.92) | 123.98 | 9,973.0000 Hz, 0.000 ppm | -123.98 (-123.93) | 123.98 |
| `baaf` | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.98 (-123.92) | 123.99 | 9,973.0000 Hz, 0.000 ppm | -123.97 (-123.91) | 123.97 |
| `b0-2`, B16b's B0 | (a) | 1,919,610; 319,935 PDUs, 0 gaps | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.62 (-102.55) | 123.62 | 9,973.0000 Hz, 0.000 ppm | -114.29 (-82.58) | 114.29 |
| `b0-2`, B16b's B0 | (c) | 14,400,000 | -14.1035 | 997.0000 Hz, 0.000 ppm | -123.95 (-100.47) | 123.95 | 9,973.0000 Hz, 0.000 ppm | -122.80 (-80.48) | 122.80 |

The offsets are against each point's own sample clock: the stream's at (a)
and (b), the DUT's TDM clock at (c).

McASP0's 300 s at (c), graded by `b9_thdn.py`:


| Run | Tone | Blocks | Discontinuities | Blocks at the path's floor | THD+N at the floor, dB, median (worst) | SNR at the floor, dB | THD+N, all blocks, dB, median (worst) | Level | Offset, ppm, median (largest block) |
|---|---|---|---|---|---|---|---|---|---|
| `bcrf` | 997 Hz, channel 0 | 300 | 0 | 300 | -123.98 (-123.93) | 123.99 | -123.98 (-123.93) | -14.10 dBFS | 0.0000 (0.000) |
| `bcrf` | 9,973 Hz, channel 1 | 300 | 0 | 300 | -123.97 (-123.90) | 123.97 | -123.97 (-123.90) | -14.10 dBFS | 0.0000 (0.000) |
| `baaf` | 997 Hz, channel 0 | 300 | 0 | 300 | -123.98 (-123.92) | 123.99 | -123.98 (-123.92) | -14.10 dBFS | 0.0000 (0.000) |
| `baaf` | 9,973 Hz, channel 1 | 300 | 0 | 300 | -123.97 (-123.91) | 123.97 | -123.97 (-123.91) | -14.10 dBFS | 0.0000 (0.000) |
| `b0-2`, B16b's B0 | 997 Hz, channel 0 | 300 | 0 | 169 | -123.98 (-123.91) | 123.98 | -123.95 (-100.47) | -14.10 dBFS | 0.0000 (0.030) |
| `b0-2`, B16b's B0 | 9,973 Hz, channel 1 | 300 | 0 | 169 | -123.95 (-120.18) | 123.95 | -122.80 (-80.48) | -14.10 dBFS | 0.0000 (0.030) |

In both following cases: no skip, repeat, insert, glitch or silent frame, and
an effective offset of 0 ppm. The 997 Hz tone's phase moved less than 0.000001
frames over the window, against 0.0005 in B0.

(c) against (a) and (b), on full 24-bit values:

| Run | (c) against (b) | (c) against (a) |
|---|---|---|
| `bcrf` | SAMPLE-EXACT over 1,646,473 recorded frames, 34.3 s, 0 differing, 0 slips | SAMPLE-EXACT over 1,647,859 frames, 34.3 s, 0 differing, 0 slips |
| `baaf` | SAMPLE-EXACT over 1,644,390 recorded frames, 34.3 s, 0 differing, 0 slips | SAMPLE-EXACT over 1,641,156 frames, 34.2 s, 0 differing, 0 slips |

Point (d), the peer's digital output at the external capture, carries lane
B6's loop from McASP0, played into the DUT's TDM input:

| Run | Decoded frames | Skips | Repeats | Net steps | Torn | Level and THD+N, both tones | Blocks at the loop's floor |
|---|---|---|---|---|---|---|---|
| `bcrf` | 14,583,391 | 0 | 0 | 0 | 0 | -1.00 dBFS; -146.06 dB and -145.99 dB median | 303 of the 303 wholly inside the playback; of the 306, blocks 0 and 1 precede it and block 2 holds its start |
| `baaf` | 14,585,924 | 0 | 0 | 0 | 0 | -1.00 dBFS; -146.06 dB and -145.99 dB median | 303 of the 303 wholly inside the playback; of the 306, blocks 0 and 1 precede it and block 2 holds its start |

So there were 0 net steps between the DUT's TDM clock and the peer's output
over 303.8 s and 303.9 s. The decode counts a step as small as one frame, as
its planted control shows (`controls/b16b-dloop-control.json`); one frame in
14.58 million would be 0.07 ppm.

### B16c: the following record

From lane B9's console poll, 0.5 s per poll, and the GET_COUNTERS marks. The
reduced receipts `r2/bcrf-poll-receipt.json` and `r2/baaf-poll-receipt.json`
carry each poll figure below; see
[B16, round 2: reduced receipts](#b16-round-2-reduced-receipts).

| Case | Set to LOCKED | Servo at the window's polls | Trim | The followed stream's rate against gPTP | AAF meter in the window | `SLIP_TDM` | DUT CLOCK_DOMAIN LOCKED / UNLOCKED, before the window and near its end |
|---|---|---|---|---|---|---|---|
| B-CRF | 2.585 to 3.161 s; ACQUIRE before it | LOCKED at 596 of 596 | -6.000 to -6.125 ppm | CRF sink +10.60 to +10.65 ppm | Not selected: `AAFM_STAT` 0 | 0, static | 23 / 22 and 23 / 22 |
| B-AAF | 6.602 to 7.180 s; ACQUIRE before it | LOCKED at 596 of 596 | -6.000 to -6.125 ppm | AAF meter +10.60 to +10.63 ppm; the CRF sink, not followed, +10.59 to +10.65 ppm | `AAFM_STAT` `0x001e0007` at every poll: locked, rate valid, enabled, 0 history restarts, largest deviation 30 ns | 0, static | 24 / 23 and 24 / 23 |

Each poll records only its own start and end. Its servo read, the second of
its five console reads, falls between them. So each lock bracket runs from
the start of the last poll that read ACQUIRE to the end of the first that read
LOCKED: polls 44 and 45 in B-CRF, 52 and 53 in B-AAF. The `SLIP_LB` brackets
below use the same rule.

The servo word read `0x...0034` while LOCKED, as in lane B7's read, and
`0x...0074` while the fine-PS actuator was busy: 580 and 16 of the window's
polls in B-CRF, 584 and 12 in B-AAF. The design's
[bench row](../design/MEDIA_CLOCK_FOLLOWING.md#bench) for B AAF asks for:

- LOCKED within 15 s of the set and never left during the capture: met;
- 0 net steps between the DUT's TDM clock and the peer's output: met, at (d);
- tone blocks at the floor outside capture-path losses: met, at (c) and (d);
- `SLIP_TDM` static: met;
- the meter's history-restart count unchanged after lock: met;
- its largest timestamp deviation recorded: 30 ns.

For B CRF the row says "As B6". Lane B6's pass rule has four terms (see
[Method](#method)), and both cases are judged against all four here:

| Lane B6's term | B-CRF | B-AAF | Evidence |
|---|---|---|---|
| The DUT's servo reads LOCKED | Met | Met | LOCKED at 596 of 596 window polls; 2.585 to 3.161 s and 6.602 to 7.180 s after the set |
| The counted frame-rate ratio within 0.5 ppm of zero | Met | Met | 0 net steps at (d) in 14,583,391 and 14,585,924 frames: below one frame in 14.58 million, 0.07 ppm. At (c) 0.0000 ppm |
| The timed ratio's interval holds zero | NOT RUN | NOT RUN | This mode ran no timing sampler at McASP0, so no timed ratio exists |
| 0 listener discontinuities on the tone path | Met | Met | 0 at (c) over 300 s and 0 at (d) |

So B-CRF and B-AAF meet three of lane B6's four terms; the timed ratio was not
run. The counted ratio stands in for it as evidence only. No recorded decision
replaces the timed ratio, so the term stays open.

**`SLIP_LB`**, the DUT's loopback ring, counted 162 dups at the start of B16c and
188 at its end, in steps of two. Each step is timed by the two polls between
which it appears, against the DUT's set. In each case five steps fell in the
12.2 s between the binds and the DUT's set, all with the servo IDLE: from 0.1
s after the binds to 1.4 s before the set. Then the DUT was on INTERNAL and
the peer on its own clock. The steps are consistent with the ring absorbing
the clocks' difference and, for the first, with the one slip per bind
that lane B16b's runs counted; the receipts do not separate these causes. The rest fell
in ACQUIRE, the servo reading ACQUIRE at both polls of each:

- B-CRF: one step, between 2.08 and 2.66 s after the set;
- B-AAF: two steps, between 2.08 and 2.65 s and between 5.10 and 5.68 s after
  the set.

None fell after LOCKED: not up to the window, through it, to the restore or in
the poll's last 12 polls. Lane B8's INTERNAL-to-AAF set slipped 2.0 to 3.0 s
after LOCKED ([#645](https://github.com/kebag-logic/milan-fpga/issues/645));
that did not repeat in either case here.

**MEDIA_RESET.** Both DUT talkers counted MEDIA_RESET 0 at the start of B16c and
4 at its end, as many as the DUT's clock-source sets. The design declares one
per switch (Milan v1.2 Table 5.4). The peer's listener of the DUT's AAF talker
times them at the marks, in each case: one between the mark 5 s after the
peer's set and the first window mark, 20 s after the DUT's set; none from
there to the mark after the captures; and one at the restore.

**CLOCK_DOMAIN counters.** The DUT's LOCKED and UNLOCKED each moved once per
case, between the mark before the binds and the first window mark, and not
from there to the restore. The peer's moved once each at each restore to its
CRF input, and not at the set to INTERNAL.

### B16c: attribution

| Stage | Loss | Evidence |
|---|---|---|
| The tone source and the peer's path into its talker | None beyond the path's floor | At (a), medians are -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block is -123.93 dB. |
| The network, (a) to (b) | None | 0 sequence gaps on either tap; (a) and (b) both equal (c) over the same recorded frames |
| The DUT's listener, its media-clock recovery, map and TDM render, (b) to (c) | None | Sample-exact over 34.2 to 34.3 s. Over 300 s: no discontinuity, every block at the floor, phase drift below 0.000001 frames |
| The DUT's talker, the peer's listener and its output: the positive control | None | 0 discontinuities and 0 net steps in 14.58 million decoded frames each; all 303 blocks wholly inside the playback at the loop's floor |

The DUT renders the stream sample for sample in every frame compared:
3,289,015 against (a) and 3,290,863 against (b).

Beyond the taps' 34 s, (c) is graded on its own. With every block at the
floor and no discontinuity, nothing is left to assign upstream.

**Against B0.** In lane B16b's B0, the peer followed the DUT's CRF talker.
There 131 of the 300 blocks at (c) sat off the floor. Inside the taps' 34.1 s,
23 of them lie, and (a) holds them sample for sample: shown directly. (a)'s
own 39 blocks reach -102.6 dB and -82.6 dB. The other 108 lie beyond the taps
and are assigned to the peer's talker stream by inference only. In B-CRF and
B-AAF the peer ran on its internal source, and no block at (a) or (c) left the
floor. In the entries the reads around them both hold (618 between lane
B16b's last read and B16c's first, 668 within B16c), the tone source's state
read the same for B0 and for both cases here. One run of each, at different
times, does not show that the peer's clock source causes the degraded blocks.
The peer's internals are not observable over ATDECC.

### B16c: the tone source, read only

The tone, lane B15's loop `d9684a8f...`, played from 07:49:29 to 08:03:52
CEST. The lane read the source's state at 07:48 and 08:03 CEST, and its meters
passively at 07:49 and 08:03. The meters read as in lane B16b, at both
times: -38.5 dBFS leaving the documented pair of outputs and -14.0 dBFS
leaving the second pair.

The first state read equals lane B16b's last in all 618 entries both hold.
Between B16c's two reads, two of the 668 entries both hold differ only in
which messages for the same address each read caught: the first read caught
two for each, the second one, which the first also caught. Both reads show
those inputs of a monitoring mix at minus infinity, and the lane wrote
nothing. The reduced receipt `r2/source-receipt.json` carries these counts and
the meter levels; see
[B16, round 2: reduced receipts](#b16-round-2-reduced-receipts).

Lane B9's tone monitor read the playback RUNNING at every 0.2 s read of both
cases, 1,805 and 1,803 reads. It saw one trigger time and a monotonic hardware
pointer: no restart and no underrun (each case's `tone-summary` in its
`events.jsonl`). The playback's own log, retained privately, holds no underrun
either (`r3/playback-logs.json`).

### B16c: bench as left

| State | As left |
|---|---|
| DUT stream state | Both STREAM_INPUTs unbound; STREAM_INPUT 0, at `0205022001006000`, and STREAM_INPUT 1, at `041060010000bb80`; both maps as found; CLOCK_SOURCE 0, INTERNAL; all read back |
| Reference peer | STREAM_INPUT 0, bound to the DUT's STREAM_OUTPUT 0, STREAM_INPUT 8 to the DUT's STREAM_OUTPUT 1; its CLOCK_DOMAIN on CLOCK_SOURCE 1, its CRF input, as found. It was set to 0 and back to 1 once per case, each read back |
| Census, B16c's start against its end | 44 of 45 reads equal, the census's start record aside; the other is the DUT's live propagation delay |
| Counters, B16c's start against its end | Moved only as the method implies; see the residuals |
| DUT saved state | NVM image seq 286 to 292, commits 52 to 58, `pend=0`, `VD_OK` |
| The tone | Stopped by its process ID at 08:03:52 CEST; the playback closed |
| The tone source | As the owner left it; the lane wrote nothing |
| SoC board | Same boot; McASP playback closed; the to-host leg running with its recorded line under a new process ID; the from-host leg dead, as found; USB function configured; no lane file left |
| Controller host | No task process; staging removed |
| Tap host | No capture file and no capture process |
| Bench host | Both USB audio devices present; the board link's address present; the bench lock free |

Residuals that no permitted command restores:

- **The peer's talkers** counted two more stream starts and stops each, one
  per case. Its listeners of the DUT's talkers counted four MEDIA_RESETs each.
- **The DUT's talkers** counted MEDIA_RESET 0 to 4 each; its listeners'
  GET_COUNTERS advanced with the binds.
- **The CLOCK_DOMAIN counters** read LOCKED / UNLOCKED 22 / 21 to 24 / 23 on
  the DUT and 6 / 5 to 8 / 7 on the peer.
- **`SLIP_LB`** read 162 dups at the start and 188 at the end, every step
  before LOCKED.

### B16c: acceptance of #629

| Item of #629 | Judgement after lane B16c | Evidence |
|---|---|---|
| Bench quality metric: THD+N and SNR of a known tone on the selected path, against the INTERNAL control and synthetic slips and drift | Direction A: met, by lane B7. Direction B: graded for both followed sources, B-CRF and B-AAF, against lane B9's synthetic controls (PASS in lane B16). Against lane B6's four pass terms, three are met in each case and the timed ratio was NOT RUN; no recorded decision replaces it. NOT met for the INTERNAL control: B0's run had the peer following the DUT, so it holds no mismatch to show. The ruling's exception covers B-CRF and B-AAF only | [B16c: B-CRF and B-AAF](#b16c-b-crf-and-b-aaf); [B16c: the following record](#b16c-the-following-record); [B16: the controls](#b16-the-controls); [B16b: limits](#b16b-limits) |
| Bench, both directions, each followed source: the listener's CLOCK_DOMAIN set and read back, its format adapted, the as-found source restored | Met, as after lane B7, and held again here for Direction B | [B16c: clock-source record](#b16c-clock-source-record) |
| Fabric: a switch re-locks with no undeclared discontinuity | As judged after lane B8, pending #645. In both INTERNAL-to-following sets here `SLIP_LB` stepped only before LOCKED | [B16c: the following record](#b16c-the-following-record) |
| Every other item | As judged in [B8: acceptance of #629](#b8-629-acceptance) and [B7: acceptance of #629](#b7-629-acceptance) | - |

So #629's items are not all met, and the issue stays open. Direction B's INTERNAL
control would need the same exception for B0, with the peer on its internal
source. Lane B6's timed ratio for B-CRF and B-AAF would need a mode with
McASP0's timing sampler, or a recorded decision.

### B16c: limits

- One graded run per case, on this bench's DUT and reference peer only, each
  with 300 s at McASP0, and 40 s of each tap. Lane B7's windows were 630 s;
  one locked action must end within 10 minutes.
- Lane B6's timed ratio was NOT RUN: this mode ran no timing sampler at
  McASP0. The counted ratio at (d) stands in for it as evidence only; no
  recorded decision replaces the term.
- The peer's internal source is both cases' reference. Its rate is recorded
  through the DUT's meters, +10.59 to +10.65 ppm against gPTP, not graded.
- The servo's status carried bit 4, DRP config mismatch, at every ACQUIRE and
  LOCKED poll in both cases, as in lanes B6 and B7. It is recorded, not
  analysed.
- B0's case with the peer on its internal source was not run, so Direction B has no
  INTERNAL mismatch control on this image.
- The degraded blocks of B0 and their absence here come from one run each.
  In B0, 108 of the 131 lie beyond the taps and are assigned upstream by
  inference.
- Printed precision is not calibrated accuracy.

### B16c: artifact hashes

The raw files stay outside the lane packet, on the bench host, and the
packet's `RAW-ARTIFACTS.json` records each of them. The external capture's
sizes are withheld, because they would state its channel count.

| Run | Raw file | Bytes | SHA-256 |
|---|---|---|---|
| `bcrf` | `tap-peer.pcap`, the peer's link | 154,049,992 | `edad46fe5de09dcace08a19eef8f5ecc5f0e9cab9bf5e506eb3e2f23a6bc97b3` |
| `bcrf` | `tap-dut.pcap`, the DUT's link | 154,048,228 | `4e7013347ec9de4e29c61165f92acee4e22104bbf5e7aa1050225d38ba593d09` |
| `bcrf` | `mcasp-all.raw`, McASP0 | 460,800,000 | `b5e30bb576949c077f3ff611c6226d5bf094e7b65ff2e1f033541c3f9ba1c03f` |
| `bcrf` | `extcap.raw`, the external capture | Withheld | `b4f6a999500c5b1b0e1c058afeaf9788410f1b2f29e4a4e684ba19b1c2f50e4d` |
| `bcrf` | `poll-run.jsonl`, the console poll | 218,420 | `9cfc79bb2ae8ad6c6e8cca028d66af3b6695c0982ffe2a512ea756fb3dc06c03` |
| `bcrf` | `tone-status.jsonl`, the tone monitor | 199,498 | `2a7974d5a6f6548e847844c326e52e59d6cc4b1f6dcfd0a730c673f85865a10c` |
| `baaf` | `tap-peer.pcap` | 154,049,168 | `234a2f0b414dcd0a07e9f2fb9047d417b9d14da77fddc0a0b708e315983ab36d` |
| `baaf` | `tap-dut.pcap` | 154,048,154 | `5a8dbaad272ad1c6bbd18aa146486ed2a78c27d23270a8e9d243207b9269038b` |
| `baaf` | `mcasp-all.raw` | 460,800,000 | `1351272cb679353885983762402caa13ef6e793831463dfc5a2ca242cca3a93e` |
| `baaf` | `extcap.raw` | Withheld | `1eeaad6845cb2ad30de88ffe5eb211518f12acf14fa6fed9bd14a12cdd9c099c` |
| `baaf` | `poll-run.jsonl` | 218,401 | `476a007728d267931a7baf32095afd8342fde5e8c30984f469b857c3841bab73` |
| `baaf` | `tone-status.jsonl` | 200,133 | `40962288e0fe5eca37964b068c2060c005bc39ccbbe470486c41003653ce3a99` |
| `bcrf`, `baaf` | `b6-loop.raw`, lane B6's loop | 1,536,000 | `566d3dfae6eb60a658b8cb0ddf5c833900ccbe4feb41c427a970a5854cc75588` |

The packet's evidence files for B16c, as retained after its redaction pass
(`redaction.json` gives each masked file's original and retained hashes):


| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/run_b16c.py` (the runs, modes `bcrf` and `baaf`) | 41,693 | `8ed6b63f03598f595c6b2aedcfedcdd81f37d3d130cdc2368ba5010962948a3c` |
| `tools/run_locked_b16c.sh` (the locked wrapper) | 2,564 | `6eed98dbba4f6fde2752e185c5406005ad5e0915910c8ca43026231b8aa0cd6f` |
| `tools/tables_b16c.py` (the tables above, from the packet's files) | 6,593 | `95b33b4530062c48e17b0db09019ff18b0fa166938006693947ee3b31408d918` |
| `tools/dryrun_b16c/dryrun_b16c.sh` (the offline dry run) | 1,903 | `699955707f9847b5db9076782d0f4472978c27ea4d85cb45fcedcc8e95b60be7` |
| `tools/dryrun_b16c/check_dryrun_b16c.py` (its checks) | 4,074 | `fdfffe23a65b2e07fd28270128e5832d8f0ce6eb801178bd0de671b216c4a204` |
| `controls/b16c-dryrun-summary.json` (8 of 8 scenarios) | 273 | `685737875fc4df85c27e5e37ac680f373cdc0e02e930da8189da8834a891e336` |
| `controls/b16c-wrapper-deadline.txt` (the wrapper's deadline path) | 617 | `090969eb04c94470e4589d465f960e72d938745fa1c61203570f0ef9fc439677` |
| `runs/bcrf/events.jsonl` | 20,973 | `9e6b07074af7d371cbca8df974a85e9a6d3f6bd73526bd6350c42344a7c88e55` |
| `runs/baaf/events.jsonl` | 20,973 | `2011eca5bb7b5802451342da06268acc88af4b2ac0c161c06edd9d7f7b24ab2f` |
| `summary/bcrf/c-b9-grade.json` (B-CRF's grade at (c)) | 135,192 | `a74f236bb68e333f5dbc8f1a47176badf318048573728e9cec603cc8de5a7e6b` |
| `summary/baaf/c-b9-grade.json` (B-AAF's grade at (c)) | 135,271 | `2b0ee83ea4d80978bc7239cba706e6c14881f77b4a503c89759021c0203efd84` |
| `summary/bcrf/align-a-c.json` | 426 | `80df5a0b1751a209f2b8055409e5399d3648618bd80ca036c913d9045e3721ec` |
| `summary/bcrf/align-b-c.json` | 426 | `e22934e3702eb234534b11342b3710bdee94001dd4ffbc1b446a9d52d7e51cf2` |
| `summary/baaf/align-a-c.json` | 426 | `1c88af889538788a8c7842e79aea5f2e3684802d5d2dbaa5dd293e8003dbfabd` |
| `summary/baaf/align-b-c.json` | 426 | `1a8d61828b3d882136014f6cd2b2eefc69a963b46a33d49c84e047702103c245` |
| `summary/bcrf/d-loop-decode.json` | 316 | `9b238160fb9fda206294b9df90bc52724c6d9d97d262681c8e7a6a011b74fae0` |
| `summary/baaf/d-loop-decode.json` | 316 | `342724e82b1877b12579f04102566a8ae7cba30dd0baea8a55a8cb88acf2e2b9` |
| `summary/b16c-tables.md` (the rendered rows) | 12,847 | `8df9a8ccda5f2bbc143bc2dbcaa8868e3dd5a1d1fab8eb427428c2a7d95a19f8` |
| `restore/census-compare-b16c.txt` (B16c's start against its end) | 481 | `5b0015fd2a63e3aa2a6676842da251196fcb1f1540c7532980f006b7c5f90dcc` |
| `identity-b16c/identity-verdict.txt` | 1,532 | `4634ee944266589d6be3a9a1f90c93cd58c003b4d9fc60a341d43e46d7ff2130` |

### B16, round 2: reduced receipts

The reviews of this section,
[R624-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119236428)
and [R625-1](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119311570),
found figures that did not equal their receipts and figures with no public
receipt. Neither alleged a DUT defect. Under the manager's
[assignment for round 2](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119316763),
the operator, [A603], corrected the text above and published the reduced receipts
below, on 2026-10-12, documents only. Nothing on the bench was touched: no
lock, controller, board or instrument. Every receipt was extracted from files
the lane already retained, and each receipt carries those files' SHA-256.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| B0's floor at (c), `b0-2` | -123.98 dB on both tones | -123.98 dB at 997 Hz and -123.95 dB at 9,973 Hz; `pts3` -123.98 dB on both | `r2/b0-2-receipt.json`, from `summary/b0-2/c-b9-grade.json` |
| B0's degraded runs | 0 to 18, 28 to 31, 43 to 54 and later runs | 0 to 18, 28 to 31, 43 to 44, 46 to 54 and eleven later runs; block 45 is at the floor | `r2/b0-2-receipt.json` |
| B0's recording start | From 06:38:03, 24 s after the last bind | About 06:38:05.2, 26 s after the last bind: the capture command at 06:38:03.2 plus the board's 2 s of playback | `r2/b0-2-receipt.json`, from `runs/b0-2/events.jsonl` and `tools/run_b16.py` |
| `pts2`'s start at McASP0, found by the operator's own check | As `pts1`, from 06:28:25 | About 06:28:31.5, after the same 2 s of playback | `runs/pts2/events.jsonl`, `runs/pts2/soc-record.log` |
| B-CRF and B-AAF against lane B6 | Three terms, all met | All four terms: three met, the timed ratio NOT RUN; no recorded decision replaces it | [B16c: the following record](#b16c-the-following-record) |
| B0's attribution | 131 degraded blocks in the peer's talker stream, reaching (c) unchanged | 131 is the count at (c). 23 lie inside the taps' 34.1 s and are shown in (a) sample for sample; the other 108 are assigned upstream by inference | `r2/b0-2-receipt.json` |
| B16c's first counter mark | At the window's start | 20 s after the DUT's set, about 6 s before the window | `runs/bcrf/events.jsonl`, `runs/baaf/events.jsonl` |
| B16b's state comparison | Four entries differ | Two settings changed; two monitoring-mix entries differ only in which messages each read caught | `r2/source-receipt.json` |
| B16's other source outputs | Silent | No reading above -135.2 dBFS | `r2/source-receipt.json` |
| B16c's `SLIP_LB` steps | 2.66 s, 2.65 s and 5.68 s after the set | Each bracketed by its two polls: 2.08 to 2.66 s, 2.08 to 2.65 s and 5.10 to 5.68 s | `r2/bcrf-poll-receipt.json`, `r2/baaf-poll-receipt.json` |

The receipts:

- **The console poll of each case of B16c.** `r2_poll_b16c.py` reads the raw poll
  and refuses it unless its SHA-256 and size equal the record in the case's
  own `events.jsonl`. It then recomputes the published poll summary from the
  raw poll with the run tool's own rule; it equals the published summary in both
  cases. It decodes each poll by
  [the register map](../reference/REGISTER_MAP.md), cuts spans at the case's
  steps and gives each span's servo states, servo word values, and the minimum
  and maximum of the trim, the CRF and AAF rates, `SLIP_LB` and `SLIP_TDM`. It
  lists every `SLIP_LB` step with its two polls' times and servo states. The
  trace beside each receipt holds every poll's eight raw words and its time
  against the DUT's set, so the extrema can be checked without the raw file.
  It recomputes the run's own LOCKED brackets, 2.657 to 3.161 s and 6.68 to
  7.18 s. Those open at the end of the last poll that read ACQUIRE. That poll
  read the state before it ended, so round 3's brackets open at the poll's
  start instead, 2.585 s and 6.602 s; see
  [B16, round 3: figures check](#b16-round-3-figures-check).
- **The tone source's reads.** `r2_source_b16.py` reads the twelve retained
  reads, four per lane, and a class map. The map says which of the source's
  controls are meters, which meter belongs to which role and which class a
  state entry belongs to. The reads and the map name the source's controls,
  so they stay private; the receipt names none. Per read it gives the time,
  the SHA-256 and, per role, the meter levels. Per compared pair it gives the
  entries each holds, those both hold, those that differ, and each differing
  entry's class. It also gives how many messages each read caught for that
  entry's address, and whether each read's last value is among the other's.
  The receipt holds the map's SHA-256.
- **B0's overlap.** `r2_b0_receipt.py` reads only files in the packet: B0's
  grade, both alignments, (a)'s grade, the run's events and the run tool.

Each tool was checked offline on altered copies before use
(`controls/r2-controls.json`, 6 of 6 PASS): a changed byte in the raw poll is
refused; a changed field in the published summary is reported as a mismatch;
a planted `SLIP_LB` step is listed at its poll with its servo state; a
planted setting and meter level appear in the source receipt; a shortened
overlap moves the inside and beyond counts.

The extraction, from the packet's root with the raw files at their recorded
paths:


- `python3 -I tools/r2_poll_b16c.py {raw}/bcrf/poll-run.jsonl runs/bcrf/events.jsonl r2/bcrf-poll-receipt.json r2/bcrf-poll-trace.tsv`
- `python3 -I tools/r2_poll_b16c.py {raw}/baaf/poll-run.jsonl runs/baaf/events.jsonl r2/baaf-poll-receipt.json r2/baaf-poll-trace.tsv`
- `python3 -I tools/r2_source_b16.py {class map} {list of the twelve reads} r2/source-receipt.json`
- `python3 -I tools/r2_b0_receipt.py . r2/b0-2-receipt.json`


The tone source's twelve reads, now also listed in the packet's
`RAW-ARTIFACTS.json` under `source/`. Their sizes are withheld, because they
would state the source's control layout:

| Read | At, CEST | SHA-256 |
|---|---|---|
| `b16-state-1.json`, state | 05:47:56 | `ce5574185d1c05f8ca0d1d669904eb4c4ea21229f8af7f33b624aa461e56dca0` |
| `b16-meters-1.json`, meters | 05:55:41 | `3a04b34f9fd83de714ba30523a4ed0ee4b09f4fae1e413d4adfc9891ebcfa6ca` |
| `b16-meters-2.json`, meters | 06:01:44 | `5e8e366bd950e2523b57735c4be8c3b672cda416b105b3ddc55ee3d6d18611b2` |
| `b16-state-2.json`, state | 06:01:48 | `f4bcf327c815ec686ec7bb2573551e0ac78cbb6ba03d0862cff7480a65b6bd1e` |
| `b16b-state-1.json`, state | 06:23:06 | `6b4cd4e6a325b389e4be65e43e5109ed903f7ca27b58864e9dbef531b4818c72` |
| `b16b-meters-1.json`, meters | 06:23:30 | `a7c844bddf786fb0eccfd15af94b5c0bc1b5ae55bbe49e5021dedce01a6c2c04` |
| `b16b-meters-2.json`, meters | 06:50:05 | `fb5c6e23143b1379948586545b66fc26a3419827c72eb929ad4b531fcbc273ed` |
| `b16b-state-2.json`, state | 06:50:08 | `b8f0746478b7cd652f3a06234aa7358a4078614f0b0fc64344a9a476b1d25288` |
| `b16c-state-1.json`, state | 07:48:56 | `195d59866d6ccd976e95d79f3833b6ff01c0ab5bac7d04e934b7338a97d54a3a` |
| `b16c-meters-1.json`, meters | 07:49:34 | `f694f3dfdbec41ec48e85fec9bc77019a4168855d2f01f921a88e677af19fbf7` |
| `b16c-meters-2.json`, meters | 08:03:29 | `794b67fe8ab03f3e61c2eaf9245d0988849b1ce73cd26167ab67f8690d5e01ab` |
| `b16c-state-2.json`, state | 08:03:32 | `93cb9240f72ee45779008872da841cb3bec4bb7de527bb05381a91dfac781624` |

The two raw polls are those in [B16c: artifact hashes](#b16c-artifact-hashes):
`9cfc79bb...` (B-CRF) and `476a0077...` (B-AAF).

The round's files in the packet:


| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r2_poll_b16c.py` (the poll receipt) | 10,234 | `14ae199a556bca981cd9898d186efd983609325b93412beb6dd332a0f0276cb2` |
| `tools/r2_source_b16.py` (the source receipt) | 6,604 | `903145f68d3ce8e4e2dc3813b67ac9acfad2b0361a58b146e73b839bec63fa3c` |
| `tools/r2_b0_receipt.py` (B0's receipt) | 4,874 | `cf650fa86179d611ddf63eed2151b5f1062847fd6797b277590e3a5e82cdfcad` |
| `r2/bcrf-poll-receipt.json` | 6,945 | `abb1f853804c23c364b49f2b4263bcae68b928881ccb501d187f78a64c00660f` |
| `r2/bcrf-poll-trace.tsv` | 62,923 | `050aeded3806ec9ec821b19da28b85313a9ae58921fc9d2c86a236d10078f1db` |
| `r2/baaf-poll-receipt.json` | 7,446 | `2f8cc0894cfb8918ff3b066721f8e0b0200c2241ee280375202cf6d6f641c931` |
| `r2/baaf-poll-trace.tsv` | 62,923 | `3e891d0faf7ba65997b8a487ad53f01e86dfc2713fa8b1721ff33c0d1bdfdeea` |
| `r2/source-receipt.json` | 21,276 | `1afbce9cdd27468394bf33265c45f1bb1d1e7a46091e15a715950a2ba4406912` |
| `r2/b0-2-receipt.json` | 2,484 | `8bcab8394d2f8d02890c76ce9bf5f864f53cf195ae4c58bec8bee055c3aba6f7` |
| `controls/r2-controls.json` (6 of 6 PASS) | 1,984 | `dc6f67634197b22e7f30225758d4221f697833472997b0b05a8174d94956b437` |

### B16, round 3: figures check

The reviews of round 2,
[R624-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119878041)
and [R625-2](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6119899949),
found more figures that did not equal their receipts. Neither alleged a DUT
defect or reversed a bench verdict. Under the manager's
[assignment for round 3](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508),
the operator, [A603], corrected the text above and added a figures check to the lane
packet, documents only. Nothing on the bench was touched.

**The check.** `tools/check_b16_figures.py` is in the packet, not the tree. It
holds a row for each quoted figure in this section, in this page's introduction
and Contents entry on lane B16, and in lane B16's part of the page's row in
the [findings index](README.md). A row gives the document line, the figure as shown,
the receipt, the key into it and the displayed precision. The receipt is a
packet file, a repository file, or this page at an earlier commit, for a
figure that a round superseded. The check recomputes each figure from its
receipt, rounds it to the displayed precision and fails on any mismatch.
Receipts are read as exact decimals and rounded half up: `pts3`'s SNR at (a),
stored as 122.475 dB, shows as 122.48. Clock times are cut to the last digit
shown, as a clock shows them: lane B16b's identity gate ended at 06:22:34.993
and shows as 06:22:34.

The check also read the numbers, times, dates, hashes and number words that
its token pattern finds in that text. In round 3, each had to be claimed by a
row or fall in a named category: descriptor and channel indices, step and list
ordinals, tone names, commit names, citations, units, and links and quoted
phrases as a whole. So a figure added without a row failed the check unless it
was written inside a link or a quoted phrase, or in a form the pattern does
not read. Round 4's change closed the first gap, and round 5's the second; see
[B16, round 4: packet and coverage](#b16-round-4-packet-and-coverage) and
[B16, round 5: every digit](#b16-round-5-every-digit).

At round 3's head the check passed. All of its rows equalled their receipts,
and no token was left uncovered. Its output is in the packet:
`r3/figures-rows.tsv`, a line for each row with the recomputed value, and
`r3/figures-coverage.tsv`, every token that a category covers. Their SHA-256
and the check's own are in the packet's `MANIFEST.sha256`, not on this page.
The check holds this page's figures, so this page cannot also hold the
check's hash.

Its controls ran on altered copies (`controls/r3-controls.json`, 5 of 5 PASS,
from `tools/r3_check_controls.py`). Each of these fails the check and is named
in its output: a figure changed on the page, a value changed in a receipt, a
figure added without a row, a row pointing at the wrong line, and a clock time
rounded instead of cut.

The reviews' findings:

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R625-2-F1: B16c's attribution at (a) | -123.98 dB median, worst block -123.93 dB, on both tones in both cases | -123.98/-123.97 dB for B-CRF and -123.98/-123.98 dB for B-AAF (997/9,973 Hz); every worst block -123.93 dB | `summary/bcrf/a-peer-tap.json`, `summary/baaf/a-peer-tap.json` |
| R624-2-F1: the positive control's floor at (d) | 305 of 306 blocks; `pts2` 13 of 16 | All 303 blocks wholly inside the playback; `pts2` 11 of 13, blocks 6 and 12 holding its repeats. Blocks 0 and 1 precede the playback and block 2 holds its start | `summary/b0-2/d-extcap-pair.json` and those of `bcrf`, `baaf` and `pts2` |
| R624-2-F1: the taps in `pts2` | At the floor in every block but the playback's first and last | All 15 blocks wholly inside the playback | `summary/pts2/ctl-dut-talker-dut-tap.json`, `summary/pts2/ctl-dut-talker-peer-tap.json` |
| R624-2-F2: B16c's LOCKED brackets | 2.66 to 3.16 s and 6.68 to 7.18 s, from the end of the last poll that read ACQUIRE | 2.585 to 3.161 s and 6.602 to 7.180 s, from that poll's start | `r2/bcrf-poll-trace.tsv`, `r2/baaf-poll-trace.tsv` and their receipts |
| R624-2-R1: the tone source's state | Two settings changed; the state was the same for B0 and both cases | Each narrowed to the entries both reads hold: 1,255 in lane B16b; 618 and 668 around B16c | `r2/source-receipt.json` |
| R624-2-R2: the five `SLIP_LB` steps before the set | The ring absorbed the clocks' difference | Consistent with that and, for the first, with one slip per bind; the receipts do not separate the two | `r2/bcrf-poll-receipt.json`, `r2/baaf-poll-receipt.json` |
| R624-2-S1: the servo status bit 4 | Not stated | Recorded in [B16c: limits](#b16c-limits) | `r2/bcrf-poll-trace.tsv`, `r2/baaf-poll-trace.tsv` |

The check's own findings, each corrected above:

| Where | Was | Now | Receipt |
|---|---|---|---|
| B16: the identity gate | 05:45:07 to 05:45:13 | 05:45:06 to 05:45:12 | `identity/lock-window.txt` |
| B16: the tone | From 05:55:38 to 06:02:00 | From 05:55:37 to 06:01:59: the first status read less the frames played, and the stop action's start | `runs/tone-start.txt`, `runs/tone-stop.txt` |
| B16: `loop1` and `loop2` | 05:56:31 to 05:57:31; `loop2` to 06:00:29 | 05:56:30 to 05:57:30; `loop2` to 06:00:28 | `runs/loop1-lock.txt`, `runs/loop2-lock.txt` |
| B16: the tap after the probes | The remaining 49 s | 49.6 s after the second probe | `summary/loop2/acmp-peer-tap.json`, `runs/loop2/events.jsonl` |
| B16: lane B15's `pts1` | Flags `0x0002` and stream ID 0, from lane B15's packet | Only what lane B15's section records: counters 0 and output exact zero | [B15: the controls](#b15-the-controls) |
| B16: the state reads | At 05:48 and 06:01 | At 05:47 and 06:01 | `r2/source-receipt.json` |
| B16b: the resume | At 06:20, the operator's note | The first bench action, 06:22:23 | `soc/b16b-precheck-status.log` |
| B16b: the tone's level at (a) | -14.14 dBFS before 06:29 and -14.10 dBFS after | To 06:28:50 and from 06:31:51, the last and first tap frames | `summary/pts2/a-peer-tap.json`, `summary/b0/a-peer-tap.json` |
| B16b: phase drift before the change | +3.00 frames in 10 s | +3.00 and +3.01 frames | `summary/pts1/c-b9-grade.json`, `summary/pts2/c-b9-grade.json` |
| B16b: the offset before the change | +6.95 ppm | +6.94 to +6.96 ppm | The point summaries of `pts1` and `pts2` |
| B16b: the playback's underruns | Five, 0.43 to 1.63 s each, from the private log | Five, from 06:45:27 to 06:46:38, cited to the operator's record; that log was overwritten and is not retained | `HANDOFF.md` step b17; `r3/playback-logs.json` |
| B16c: the resume | At 07:32, the operator's note | The first bench action, 07:48:07 | `soc/b16c-precheck-status.log` |
| B16c: the run table | `bcrf` 07:50:12.4, 07:50:17.6, 07:50:29.8, a window from 07:50:56 to 07:55:56, a teardown to 07:56:04.1; `baaf`'s teardown 08:02:51.8 to 08:02:55.8 | 07:50:12.3, 07:50:17.5, 07:50:29.7, from 07:50:55 to 07:55:55, to 07:56:04.0; 08:02:51.7 to 08:02:55.7 | `runs/bcrf/events.jsonl`, `runs/baaf/events.jsonl` |
| B16c: (d)'s decoded span | 303.8 s in each case | 303.8 s and 303.9 s | `summary/bcrf/d-loop-decode.json`, `summary/baaf/d-loop-decode.json` |
| B16c: the peer's rate | +10.6 ppm | +10.59 to +10.65 ppm | `r2/bcrf-poll-receipt.json`, `r2/baaf-poll-receipt.json` |

Six number words with no receipt were reworded: "plus one change", "one PDU",
"one step earlier", "one request", "the two lanes" and "one route".

The playback's two retained logs are now listed in the packet's
`RAW-ARTIFACTS.json` under `playback/`, their sizes withheld because each log
names the tone source's device. `tools/r3_playback_logs.py` reduces them to
`r3/playback-logs.json`: per log its SHA-256, its modification time, the lines
that report an underrun and its exit line. Lane B16b's log is not retained.

| Log | Modified, CEST | Underrun lines | SHA-256 |
|---|---|---|---|
| `b16-tone-play.log`, lane B16's | 06:02:00 | 0 | `dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b` |
| `b16c-tone-play.log`, lane B16c's | 08:03:53 | 0 | `dab353b5ead02cb68b5ecebc757786c48b7672e6f93a37a152e37aedf9dfe43b` |

The two logs are byte-equal: each holds the playback's setup, the stop
signal and the exit line, and nothing else.

The round's files in the packet:


| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r3_playback_logs.py` (the playback-log receipt) | 1,990 | `27334c6d3106f9305187deef6196a7dcb7e14b10d6fbea08f721029766dcf595` |
| `r3/playback-logs.json` | 795 | `68e905288cf0c01c385a995bf66edc78e6323e041de99c1e0f1f3e4b360f64fe` |
| `tools/r3_check_controls.py` (the check's controls) | 6,541 | `85fc57876334b823cd349a9752bf12581bbb22f9f5c5b2a4d6f68ab948a54157` |
| `controls/r3-controls.json` (5 of 5 PASS) | 1,579 | `6b6f8bc7b99e5ec6843a7c385e681b4bcf4b89b1b56d84dcc10a88889ce6cc05` |

### B16, round 4: packet and coverage

The reviews of round 3,
[R624-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121093801)
and [R625-3](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6121186527),
each found a MINOR. Neither alleged a DUT defect, changed a figure or
reversed a bench verdict. Under the manager's
[assignment for round 4](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6121193402),
the operator, [A603], made the changes below, documents only. Nothing on the bench
was touched.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R624-3-F1: where the packet is | Not stated | The branch, a pinned commit, each round's directory, and the manifest's original and published hash per file; see [B16: artifact hashes](#b16-artifact-hashes) | `r4/evidence-receipt.json` |
| R625-3-F1: a figure inside a link label or a quoted phrase | Exempt with the link or the phrase as a whole | Read as any other text: claimed by a row, or by an identifier category bound to its keyword | `controls/r4-controls.json` |
| R625-3-S1, taken: the census | 45 of 46 entries equal | 44 of 45 reads equal, the census's start record aside | `restore/census-*.jsonl`, `restore/census-compare*.txt` |

**The check's exemptions.** Round 3's check exempted a whole link, label and
target, and a whole quoted phrase, so a figure written inside either needed
no row. R625-3's probe showed it with a figure and its unit added both ways. The check
now exempts only identifiers, each bound to the text that makes it an
identifier:

- commit names, each listed;
- clause numbers: IEEE 1722.1 and Milan v1.2 Table 5.4;
- descriptor, channel, step, round and list-item indices, each after its
  keyword;
- the packet's label, `629-b16-a603`;
- a link's target, the URL or anchor in its parentheses, not its label.

Every other token the pattern finds is claimed by a row that reads a
receipt. Round 3's other categories are gone. The tone frequencies now read
the tone tool and the analyser, the block length and the comparison's bit
width read the run summaries, the decode's smallest step reads its planted
control, and the lane's limit on a locked action reads the operator's record.
The check's tokens now also take a full commit name and the number words for
tens.

A guard sat under the categories. A token followed by a unit, such as dB,
dBFS, ppm, %, s, Hz, frames, samples, blocks, polls, bits or LSB, was a
measurement, and only a row could claim it, whatever category matched. The
guard read only tokens, and allowed at most a single space, non-breaking space
or hyphen before the unit. So a number the pattern does not read, or set
further from its unit, escaped it; round 5's check closes that, see
[B16, round 5: every digit](#b16-round-5-every-digit).

**Its controls.** `tools/r4_check_controls.py` runs each control on an
altered copy (`controls/r4-controls.json`, 8 of 8 PASS). The first five are
round 3's, their code unchanged. The new ones:

- a figure with its unit added inside a quoted phrase on the attribution row
  R625-3's probe used: the check fails and names the figure UNCOVERED;
- the same figure added there as a link label: the check fails the same way;
- a category planted in a copy of the check that matches every token, with
  the figure added in plain text: the check still fails, naming the figure as
  a measurement.

Round 3's own runner, `tools/r3_check_controls.py`, run unchanged against the
new check, passes 5 of 5 too (`controls/r4-rerun-r3-controls.json`).

The unchanged page passes: at this head the check's output,
`r4/figures-rows.tsv` and `r4/figures-coverage.tsv`, has every row OK and no
token uncovered. `tools/r4_figures_build.py` regenerates the check byte for
byte from `tools/r4_figures_spec.py`. As in round 3, the hashes of the check,
its spec and its output are in the packet's `MANIFEST.sha256`, not here.

**Rewording.** Seventeen phrases whose number words only a category covered,
and which state no figure, were reworded: "records each one",
"the published one", "failed at once", "once the controller agent",
"these two cases", "the two cases run", "on one clock", "one state of it",
"two modes added", "the two clocks' difference", "do not separate the two.",
"Two reviews of this section", "Two reviews of round 2",
"one row per quoted figure", "one line per row", "on one reference peer" and
"on one DUT and one reference peer". The date after each ruling's link was
dropped; the section's heading carries it. Each quoted number word above, and
in round 3's list, has a row that finds its phrase on this page as it stood
before the rewording.

The round's files in the packet:


| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r4_evidence_receipt.py` (where the packet is) | 5,191 | `7dca8a53f24c1e7330ed2e154e41f4e30a47012171d68c2a80c138c2834c6164` |
| `r4/evidence-receipt.json` | 38,177 | `1a433cd27edb2632a92e7abbc1f4eebca9ad4d15fae55f23d98a48647ee9805a` |
| `tools/r4_check_controls.py` (the check's controls) | 10,379 | `54d2e1df507cb1b8c8b77214942f49cfcbe3a524f4e52b882ae124384e6d4e0f` |
| `controls/r4-controls.json` (8 of 8 PASS) | 3,116 | `d01b56caf89cf99604dc32ce2d69118618fae457074c7c723eb792ef890b68e5` |
| `controls/r4-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `a0c9a8ed6f768b70208c1c28e6d37c402444a57b2877b882f175c5db4586ce87` |

### B16, round 5: every digit

The reviews of round 4,
[R624-4](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125594896)
and [R625-4](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6125596576),
each found a MINOR in the figures check: it passed a measurement written in a
form its token pattern does not read. Neither alleged a DUT defect, changed a
figure or reversed a bench verdict. Under the manager's
[assignment for round 5](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6125608002),
the operator, [A603], changed the check, documents only. Nothing on the bench was
touched, and no figure above changed.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R624-4-F1: a number written against its unit, such as seconds, dB or milliseconds, and a decimal written with a leading point | Not a token, so never read, and the check passed | A measurement in a spelling no row can claim: the check fails and names it | `controls/r5-controls.json` |
| R625-4-F1: a leading point after a sign, an exponent, a double space before the unit, and a channel index on a continuation line exempted without its keyword | The same, and the continuation exempt by the start of its line | Each fails the check and is named. A channel index is bound to its keyword across the line break | `controls/r5-controls.json` |
| R624-4-S1, taken: this section's opening paragraph | Pointed to rounds 2 and 3 | Points to each findings round | - |

**The rule.** The check no longer decides coverage by token. It reads every
digit in its text, and each must lie in either of these:

- a figure that a row claims and recomputes from its receipt;
- an identifier that a category binds to its keyword in the same sentence,
  across a line break inside that sentence.

Any other digit fails the check, named with its line and the text around it,
in the spelling it was written in: with its sign, a leading point or an
exponent. The token pattern is unchanged and now only finds the figures a row
may claim. A number it does not read can never be claimed, so it always fails;
such a figure is written apart from its unit, as the rest of this page writes
it. A row's figure must also be the whole number on the page, not part of a
longer number, such as a figure after a minus sign the pattern does not read.

**A measurement is never an identifier.** A number followed by a unit is a
measurement, and no category covers its digits: only a row. Between number and
unit may stand nothing, any run of spaces or line breaks (non-breaking, thin
and zero-width ones too), a soft, non-breaking or plain hyphen, emphasis or
code marks, a backslash, a double quote, an opening bracket, or an HTML entity,
tag or comment. A number quoted on its own is a mention: its closing quote does
not join it to a unit, and as no category takes a quoted number, it needs a row
either way. Units are read in either case: percent, dB and dBFS, ppm and ppb,
seconds and their fractions, minutes, hours, Hz, frames, samples, blocks,
bytes, bits, LSB, polls, PDUs, packets, steps, slips, repeats, skips,
discontinuities, entries and reads, with the rest of the list in the check. The
word zero before a unit counts as a number. Round 5's list named units by symbol and a few words: a unit written as another word, or set beyond a comment over a line break, still passed after an identifier, as shown by R624-5 and R625-5; see [B16, round 6: the closed list](#b16-round-6-the-closed-list).

A link's target is an address, not text. Its digits are covered when it
resolves: an anchor of a heading on this page, or an issue, pull request or
comment of this repository. An anchor's hyphens stand for its heading's
spaces and punctuation, so the measurement rule reads the heading where it
stands, not the anchor.

**The identifiers.** Each category holds its keyword with its identifier:

- commit names, each listed, in code or after the word Dev;
- clause numbers: IEEE 1722.1 and Milan v1.2 Table 5.4;
- descriptor, channel, step and round indices after their keyword, and a
  second channel index after "and" or "to", or a second step or round index after "and";
- a list-item index, where its block is an ordered list and the index is the
  item's place in it; a line inside a paragraph that starts with a number is
  text;
- names from closed lists: the lanes and cases, the reviews and their
  findings, the operator, the issue numbers it cites, McASP0, SHA-256 and CRC32, the DUT's entity name and
  serial number, the Python command, the manifest's field names, the packet's
  label, branch and published directories, and this page's markers;
- a path in code that names a file or directory of the packet, or a raw file
  the packet lists;
- a link target that resolves.

**Its controls.** `tools/r5_check_controls.py` runs each control on an
altered copy (`controls/r5-controls.json`, 22 of 22 PASS). Round 3's and
round 4's come first, their code unchanged. Each new control adds a
measurement to the attribution row R625-3's probe used, as the reviews wrote it,
unless stated:

- a number glued to s, to dB and to ms;
- a decimal with a leading point, with and without a sign;
- a number in exponent form;
- a descriptor index before ppm, set off by a double space, a non-breaking
  space or a hyphen;
- R625-4's continuation, applied where the continuation is, since a table row
  cannot hold a line break;
- a Unicode minus before a figure that a row claims, in B16c's grade table;
- a cited path that names no packet file;
- an anchor that names no heading;
- a category planted in a copy of the check that matches every number, with a
  figure and its unit added: the check still names it a measurement.

Each fails the check and names what it added, in the spelling it was written
in. Round 3's runner and round 4's, unchanged, pass against the new check
too: 5 of 5 and 8 of 8 (`controls/r5-rerun-r3-controls.json`,
`controls/r5-rerun-r4-controls.json`). The new runner against round 4's check
and page fails every new control that targets a defect of round 4's check
(`controls/r5-controls-on-r4-check.json`). The descriptor index set off by a
non-breaking space or a hyphen, and the planted category, pass there: round
4's guard already read those.

R624-4's `probe_escape_forms.py` and R625-4's `probe_coverage.py`, unchanged,
detect every form they insert (`r5/r624-4-probe-rerun.json`,
`r5/r625-4-probe-rerun.json`), and so does R625-3's probe
(`r5/r625-3-probe-rerun.json`). Further forms, from `tools/r5_self_probes.py`
(`r5/self-probes.json`), each fail the check and are named: a descriptor index
set off from its unit by a line break, bold, code, brackets, an HTML entity or
comment, or a thin, zero-width or escaped space, or with the unit in capitals;
an identifier glued to a unit or set before a unit; a fullwidth digit, a
fraction, a superscript and a Unicode minus; a path, an anchor, a link off the
repository and a page marker that name nothing real; and a line inside a
paragraph that starts with a number.

With these changes the page passes: every row equals its receipt, and every
digit lies in a claimed figure or a bound identifier. The output,
`r5/figures-rows.tsv` and `r5/figures-coverage.tsv`, lists each identifier
with its category. `tools/r5_figures_build.py` regenerates the check byte for
byte from `tools/r5_figures_spec.py`. As before, the hashes of the check, its
spec and its output are in the packet's `MANIFEST.sha256`, not here.

The round's files in the packet:


| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r5_check_controls.py` (the check's controls) | 16,186 | `bf84a387ebdaae6fee5dc93f9da5b9b06bcb827281ff1c51eac3b7da17a8aa2e` |
| `controls/r5-controls.json` (22 of 22 PASS) | 8,154 | `c22a199aa34ed8fb4d01fe238bf601d45f519cec484fe3035aee833b179a0188` |
| `controls/r5-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r5-rerun-r4-controls.json` (8 of 8 PASS) | 3,116 | `a79d24b9c9e272960eb1ffe528c5ada294571f5a5a63fbe217e8d2c344e4964d` |
| `controls/r5-controls-on-r4-check.json` | 8,165 | `2569e99d4283036b2bc38868812721621330b86b8dbfa735e5ad08fad544391b` |

### B16, round 6: the closed list

The reviews of round 5,
[R624-5](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6126709633)
and [R625-5](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6126763696),
were NEGATIVE on findings rated MINOR. New routes by which an identifier stood
for a measurement were found by R624-5-F2, a unit written as a word, and by
R625-5-F1, a unit set beyond an HTML comment over a line break. Neither review
alleged a DUT defect, changed a figure or reversed a bench verdict. Under the
manager's
[assignment for round 6](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6126774639),
the operator, [A603], changed the check and the wording of the covered text,
documents only. Nothing on the bench was touched, and no figure above changed.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R624-5-F1: the LOCKED counts in lane B6's terms table, a single figure for B-CRF and B-AAF | The row read B-AAF's count for both cases, and named B-CRF's receipt | The row reads each case's count from that case's own receipt and names both files; if the counts differ, it is a MISMATCH that names each | `controls/r6-controls.json` |
| R624-5-F2: a unit written as a word after an identifier | Passed: the guard read units by symbol and a few names | Fails: an identifier counts only before a closed list of what may follow it, and the guard also reads the units' names | `controls/r6-controls.json` |
| R625-5-F1: a unit beyond an HTML comment over a line break | Passed: the guard's separator stopped at the line break | Fails: every comment is dropped before the text is read | `controls/r6-controls.json` |
| R624-5-F3: where round 5's packet is | Not stated | The paragraph maps rounds 4 and 5, each with its commits, and names round 6's directory; see [B16: artifact hashes](#b16-artifact-hashes) | `r6/evidence-receipt.json` |
| R624-5-R1: round 5's list of identifiers | A second index after any keyword, and no issue numbers | The wording given in R624-5-R1, in round 5's list | - |
| R624-5-S1, taken: the rule's limits | Not stated | Stated below | - |

**Normalised first.** The check now reads its text as a reader sees it, before
it matches any token or category. It drops every HTML comment, even a comment over
several lines. A backslash escape gives the character it escapes, and an
HTML entity the character it names. Code is kept as written: a fenced block,
an indented line or a code span, so a comment shown in code stays text. A
comment that holds a blank line is dropped only where it starts a line, as an
HTML block; elsewhere it is not a comment, and the check reads it. The text is
then split into blocks at blank lines. In a block every run of whitespace, a
line break too, is a single space, and soft hyphens and zero-width characters are
dropped. Each character keeps its source, so each line the check names is a
line of this page.

**The closed list.** An identifier now counts only when what follows it is on
a closed list. The check looks past spaces, hyphens and dashes, a slash or
backslash, emphasis and code marks, brackets, quotes and a link's target, and
what stands there must be among these:

- the end of the text;
- a mark that ends a phrase: a full stop, comma, semicolon, colon, question
  or exclamation mark, a table's bar, or a dash set off by spaces; a point or
  comma before a digit is a decimal sign, not such a mark;
- a possessive 's;
- any of the words "and", "or", "to" and "of", unless a measurement follows
  that word, as in a range.

Anything else, any other word, a number or a symbol, makes the identifier's
digits a measurement, which only a row can claim. So a unit is refused after
an identifier whether or not a list names it, and so is any other word. A dash
that touches the number joins it to what follows. A code literal, such as a
packet path, a listed commit or the packet's label, ends with its code word:
the code mark or the space after it inside code ends it. A link's target is
still an address, and the list is read after the link.

**Units by name.** The guard before a unit now reads every hyphen and dash, a
comment over a line break, and the names of the units the ruling lists: per
cent, decibels, hertz and its multiples, parts per million, billion or
trillion, milli-, micro-, nano- and picoseconds, and msec, usec and nsec. Past
an identifier the closed list refuses these anyway; the guard also reads the
digits inside a code literal, which the list does not.

**Rows.** A figure that stands for several cases is recomputed from each
case's own receipt. The LOCKED counts in lane B6's terms table now read
B-CRF's window from B-CRF's receipt and B-AAF's from B-AAF's, and the rows
output names both files; if the counts differ, the row is a MISMATCH that
names each. A row may also name the text around its figure, and it then claims
the figure only where that text stands. The idle channels' indices before the
point tables are such rows: the closed list refuses the verb after them, so
each is recomputed from every run's point summaries, and each holds its
keyword before it and the verb after it.

**Reworded text.** Where the closed list refused the covered text's own
wording, an identifier before a verb or a noun, the sentence was reworded
within its line, with a comma, a colon, a possessive or "of", so no line
moved. No figure, verdict or link target changed. The acceptance headings, of
B16, B16b and B16c, now read "acceptance of #629"; nothing linked to their old
anchors.

**What the rule does not cover** (R624-5-S1, taken). The closed list reads
only what follows an identifier, and a figure a row claims is checked for its
value, not for what follows it. A mark that ends a phrase ends the
identifier's phrase: an identifier followed by a full stop, a comma, a colon
or a dash set off by spaces, and then a unit, passes, unless the guard reads
the unit through the mark, as it reads a dash but not a full stop, comma or
colon. A possessive is on the list. A code literal followed by a word passes,
since its digits are part of its name; only the guard reads them. A comment
is not read, so a figure inside a comment is not checked, as a reader does not
see it. A quantity written in words the token pattern does not list, such as a
dozen or a million, holds no digit and is not read. `tools/r6_self_probes.py`
runs each of these and records it passing.

**Its controls.** `tools/r6_check_controls.py` runs each control on an
altered copy (`controls/r6-controls.json`, 39 of 39 PASS). Round 5's 22 come
first, their code unchanged. Each new control adds a measurement to the
attribution row R625-3's probe used, unless stated:

- a descriptor index before each unit written as a word in R624-5: per cent,
  decibels, hertz, kilohertz, parts per million and per billion, milli-,
  micro- and nanoseconds, msec, usec and nsec;
- R624-5's lane name and clause number before milliseconds;
- a descriptor index before a unit no list names, furlongs;
- R625-5's comment over a line break, on B16c's channels paragraph as in
  R625-5, with every line kept in place;
- B-CRF's window LOCKED count changed in a copy of its receipt: the terms
  table's row is a MISMATCH that names each case's count.

Each fails the check and names what it added, as a measurement; the last
fails on its row. Round 3's, round 4's and round 5's runners, unchanged, pass
against the new check: 5 of 5, 8 of 8 and 22 of 22
(`controls/r6-rerun-r3-controls.json`, `controls/r6-rerun-r4-controls.json`,
`controls/r6-rerun-r5-controls.json`). The new runner against round 5's check
and page fails every new control (`controls/r6-controls-on-r5-check.json`).

The reviews' probes, unchanged, all hold against the new check. R624-4's
`probe_escape_forms.py`, R625-4's `probe_coverage.py` and R625-3's probe
detect every form they insert. R624-5's `probe_row3200.py` turns the LOCKED
row of the terms table into a MISMATCH; its other row there, the window's
poll count, stays OK, since the probe changes only the LOCKED count, as at
B16c's servo table. R624-5's `probe_r624_5_escapes.py` detects every form
it writes with an identifier before a unit or a word but the colon form, as a
colon ends the identifier's phrase; its forms that write a number as a word
hold no digit to detect. R625-5's `probe_comment_separator.py` passes: the
unchanged page passes and both comment forms fail. Their results are in `r6/`, a file per probe.
Further forms, from `tools/r6_self_probes.py` (`r6/self-probes.json`), each
meet what the rule says. Round 5's still fail the check and are named, but
for its page marker, now inside a comment the check drops. Of the forms that
passed in R625-5's own campaign, a small or fullwidth hyphen-minus, an em
dash, a closing bracket and an apostrophe between an identifier and its unit
now fail; a full stop between them still passes, as it ends the phrase. A
word after each kind of identifier fails, and so do an entity, an escape, a
comment in code, a range into a figure a row claims, and a code literal
before a unit.

With these changes the page passes: every row equals its receipt, and every
digit lies in a claimed figure or in an identifier followed by an item of the
closed list. The output, `r6/figures-rows.tsv` and `r6/figures-coverage.tsv`,
lists each identifier with its category. `tools/r6_figures_build.py`
regenerates the check byte for byte from `tools/r6_figures_spec.py`. As
before, the hashes of the check, its spec and its output are in the packet's
`MANIFEST.sha256`, not here.

The round's files in the packet:


| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r6_check_controls.py` (the check's controls) | 21,545 | `789a4f7ca25b8ef0d5b38bae9432d9f6be23434fe69ad20f0db9d7a80eb875de` |
| `controls/r6-controls.json` (39 of 39 PASS) | 14,414 | `a9709363266aaa05cc1a04b2d90cbbb095a426650a9f802325cbf3fe0335f043` |
| `controls/r6-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r6-rerun-r4-controls.json` (8 of 8 PASS) | 3,115 | `cde959a0d411c360f6a2159196d22bc0311006bea9025a863e192b75b3d0d02b` |
| `controls/r6-rerun-r5-controls.json` (22 of 22 PASS) | 8,153 | `d3e0663e86195cf88e45353661cdd9464eb26d1f8622c378fc0abffaf667613f` |
| `controls/r6-controls-on-r5-check.json` | 14,432 | `8f03249c0ec24a6b018122b5be2d45780ab97d145d692d067abd43c2bb141943` |
| `tools/r6_evidence_receipt.py` (where the packet is) | 6,586 | `71d32ba09f2ec1f4ab02bc9adf8085b66e96e5ca35c7243026b25ba10fe1f0bb` |
| `r6/evidence-receipt.json` | 46,562 | `bc3c0e91362f28ebcdc21d13c2e9d2ae875803da60e216b29e9227f79d35a58d` |

### B16, round 7: no markup

The reviews of round 6, POSITIVE in
[R624-6](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6128169977)
and NEGATIVE in
[R625-6](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6128099316),
differ on a finding rated MINOR, R625-6-F1. The short forms of an HTML comment
end where they open in the renderer GitHub uses, but the check's normalisation
read on to the next comment end, so a unit a reader sees vanished from what
the check read. Neither review alleged a DUT defect, changed a figure or
reversed a bench verdict. Under the manager's
[assignment for round 7](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6128175910),
the operator, [A603], changed the check and the section's markup, documents
only. Nothing on the bench was touched, and no figure above changed.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R625-6-F1: a short comment form hid a unit from the check | Passed: the check dropped a comment up to the next comment end, which is not where these forms end | Fails: a line holding any markup is refused, and nothing is dropped | `controls/r7-controls.json` |
| R624-6-S1, taken: an approximate quantity after an identifier | Not stated | Stated as a limit below | `r7/self-probes.json` |

**No markup.** The check no longer reads its text as a renderer would. It
refuses every line of the text it covers that holds a less-than sign directly
followed by a letter, a slash, an exclamation mark or a question mark. So
starts every HTML tag, closing tag, comment, processing instruction,
declaration and CDATA section that CommonMark knows, and an autolink. It
refuses markup inside code too, so no difference between its reading of code
and a renderer's can shelter a tag. The only exception is a line equal, byte
for byte, to a marker a repository generator writes:
`scripts/check_solution_docs.py` writes its markers around the tables it
generates, and the generator of tables of contents writes none. Nothing is
dropped any more, so nothing written on a line can vanish from what the check
reads. The check names each refused line with its markup, as MARKUP, and then
fails, whatever else it finds. It still reads a backslash escape or an entity
as the character it gives, keeps code as written, and splits the text into
blocks at blank lines, with whitespace collapsed across line breaks. Round 8's reading, through the pinned parser, replaced it; see [B16, round 8: the parser](#b16-round-8-the-parser).

**The section's markup.** The section held an HTML comment before each of its
tables, a marker the earlier checks dropped, and a code block wrote its
placeholders in angle brackets. Each marker's line is now blank, so no line
moved and the page renders as before, and the placeholders are in braces. The
authoring aid that writes the point and grade tables' rows found those tables
by their markers; it now finds them by their header rows, and every row is as
it was.

**What the rule does not cover** (R624-6-S1, taken). Round 6's limits stand
but for comments: a comment is now refused, not dropped unread. A word of the
closed list followed by words that hold no number, and then a unit, passes, as
in an approximate quantity after an identifier: "or so", "or more", "and a
half" or "to some" before a unit. So does a bare unit after "of" or "and". A
list marker ends with a full stop, so a numbered item that is only a unit
passes. The check reads only its own lines: another lane's table markers are
not its text, and a block of raw HTML opened elsewhere and left open into the
section is outside what it reads. A less-than sign before a space, a
less-than sign given by an entity, and a fullwidth less-than sign are not
markup, and the check does not refuse them. `tools/r7_self_probes.py` runs
each of these forms and records it passing.

**Its controls.** `tools/r7_check_controls.py` runs each control on an
altered copy (`controls/r7-controls.json`, 50 of 50 PASS). Round 6's 39 come
first, their code unchanged. The new controls:

- R625-6's forms, appended to the attribution row as in R625-6: an ordinary
  comment, each short form before a unit, and a short form before
  furlongs;
- R625-5's comment on its line and over a line break, on B16c's channels
  paragraph, as in R625-5;
- a raw tag between a number and its unit, and a comment inside a code span,
  on the attribution row;
- a former table marker, put back on the blank line it left;
- a generator's marker with a byte changed, appended as the page's last line;
- that marker byte for byte, appended the same way, which must pass.

Each new control but the last fails the check with its line named MARKUP, and
where it adds a digit, that digit is named UNCOVERED there. The last passes:
it names nothing the unchanged page does not, exits as the unchanged page
does, and both appended lines are read. Round 3's, round 4's, round 5's and
round 6's runners, unchanged, pass against the new check: 5 of 5, 8 of 8,
22 of 22 and 39 of 39 (`controls/r7-rerun-r3-controls.json` to
`controls/r7-rerun-r6-controls.json`). The new runner against round 6's check
and page passes the earlier controls and the last, and fails every other new
control (`controls/r7-controls-on-r6-check.json`): round 6's check passed the
short comment forms, the former marker and the changed marker outright.

**The reviews' probes.** Each runs unchanged, with its results in `r7/`, a
file per probe. R625-6's `probe_rendered_comment.py` runs with the
repository's locked renderer: the unchanged page passes, and the plain form and
every comment form fail, each comment form with its line named MARKUP and its
added digit UNCOVERED there. Its last assertion still states the exit statuses
of round 6's check, so the probe itself fails, as R625-6's report said it would.
R625-6's `probe_followers.py`: every comment and tag form now fails. R624-6's
`probe_r624_6_escapes.py` gives each form the exit status in R624-6's record
at round 6's head; the forms it found passing are those stated above as limits.
R624-6's poll-count probe turns the terms table's poll-count row into a
MISMATCH. Round 6's probes, from R624-4, R625-4, R625-3, R624-5 and R625-5,
give what round 6's record shows for them.

**Further forms.** `tools/r7_self_probes.py` (`r7/self-probes.json`) runs
round 5's and round 6's forms, then round 7's: markup of each kind, written
with no digit so that only the refusal can catch it, in a code span and a
fenced block too, and R624-6-S1's forms. All 111 meet what the rule says: 92
fail and are named at their line, and 19 pass as stated. Round 5's page
marker, which round 6's check passed inside a dropped comment, is now refused.

With these changes the page passes: every row equals its receipt, every digit
lies in a claimed figure or in an identifier followed by an item of the closed
list, and no line holds markup. The output, `r7/figures-rows.tsv` and
`r7/figures-coverage.tsv`, lists each identifier with its category.
`tools/r7_figures_build.py` regenerates the check byte for byte from
`tools/r7_figures_spec.py`. As before, the hashes of the check, its spec and
its output are in the packet's `MANIFEST.sha256`, not here.

The round's files in the packet:

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r7_check_controls.py` (the check's controls) | 28,060 | `6a53a284ef5e70910282c3551285d82161d77412804c27830b7c684adc80c8fb` |
| `controls/r7-controls.json` (50 of 50 PASS) | 18,201 | `5b782cd6734c2a637df54b968693dfd230e9210677778f5039d08eb37f39e576` |
| `controls/r7-rerun-r3-controls.json` (5 of 5 PASS) | 1,579 | `4871ef3e84d940d91cc7938ca2ebaf3f904e39b74e21678aa03c602dae7e3560` |
| `controls/r7-rerun-r4-controls.json` (8 of 8 PASS) | 3,115 | `f635748893ab28b258768f74aeede60a58b2ffa3a41abecac5af8b11ce3d1b60` |
| `controls/r7-rerun-r5-controls.json` (22 of 22 PASS) | 8,153 | `cfba195f4842f725385f6a7c7de1449c780050d94b05495bdff0289de32a00e7` |
| `controls/r7-rerun-r6-controls.json` (39 of 39 PASS) | 14,414 | `79e4edf8360106c43474d4bc77807c8beb1296f62fb27d211217c0e89b648946` |
| `controls/r7-controls-on-r6-check.json` | 18,212 | `f288208a13bff378280fd5f9e4cbb1e4e17a137790730bc1d007319d398fa6e3` |
| `tools/r7_evidence_receipt.py` (where the packet is) | 6,919 | `a46c4ad554c6a1448319f7d1e26fdf6e01407aedb0d4868d1fb96bf66d8b099e` |
| `r7/evidence-receipt.json` | 52,808 | `23322f43d94c68a2dcc6da0412007596828c33bcb60fdb522f1a0f4fbf4a128f` |

### B16, round 8: the parser

The reviews of round 7, NEGATIVE in
[R624-7](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6130711392)
and in
[R625-7](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6130634625),
each rate a finding MINOR. In R624-7-F1, image syntax between an identifier's
number and its unit put an exclamation mark into the check's text that a
reader never sees, and the check took it for a mark that ends a phrase, so a
number before its unit passed. In R625-7-F1, markup in the index row, in its
part on lane B16, stopped the check with an exception before it named the
line or wrote its receipts. Neither review alleged a DUT defect, changed a
figure or reversed a bench verdict. Under the manager's
[assignment for round 8](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6130721355),
the operator, [A603], changed how the check reads its text, documents only.
Nothing on the bench was touched, and no figure above changed.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R624-7-F1: image syntax hid a phrase mark from the reader, not from the check | Passed: the check read the image's exclamation mark as a mark that ends a phrase | Fails: the check reads what the pinned parser yields; the image is refused at its line, and the text around it is read without it | `r8/r624-7-escapes-probe-rerun.json` |
| R625-7-F1: markup in the index row, in its part on lane B16, stopped the check | An exception, with no line named and no receipt written | Refused at the index row's line and named MARKUP, with both receipts written | `r8/r625-7-markup-probe-rerun.json` |

**The parser.** The check now parses both documents whole with the
repository's pinned Markdown parser: cmark-gfm, through the cmarkgfm binding,
at the releases `tools/markdown/requirements.txt` pins. It verifies them as
the documentation gates do, with `scripts/gen_toc_renderer.py`, and parses
with that renderer's extensions and options. Without them it does not run: it
names what is missing and fails. It judges only the visible inline text the
parser yields: text, code spans and link text. A code span is read with a code
mark at each end, which every rule of the check looks past, so a code literal
still ends with its code word. Every line it names is the parser's own source
position. No pattern of the check reads code, escapes, entities, comments or
tags any more, and its separators no longer look past a tag, a comment or a
link's target, since none of them can stand in the text it reads.

**A closed allowlist.** The text may hold paragraphs, headings, lists and
their items, tables, block quotes, text, soft and hard line breaks, emphasis,
strong emphasis, links and code spans. Any other construct is refused at the
first line of it that the check covers, named MARKUP by the parser's name for
it, and not read: an image, raw HTML inline or as a block, a fenced or
indented code block, a thematic break, struck text, a footnote or a reference
to a footnote, a task list item, and anything else the parser yields. The
check then fails, whatever else it finds. The only exception is a block of raw
HTML that is a whole line equal, byte for byte, to a marker that
`scripts/check_solution_docs.py` writes. A link is read on its text. Its
target and its title are not text a reader sees, so neither is read, but a
target must still resolve, as since round 5: to an issue or a pull request of
the repository on GitHub, or to a heading's anchor on the page. A target that
does not is read as text of its own, at its line.

**The index row.** Both documents are parsed whole, so the index row is read
where the parser places it, and only its part on lane B16, from that part's
first byte on, by the source columns of the row's text. Markup there is
refused at the row's line as it is on the page, and the check writes both
receipts before it fails.

**The section's code block.** The section held a fenced code block, the
extraction commands of round 2. They are now a list of code spans on the
same lines, so no line moved. A list's numbers are drawn from its structure,
not written as text, so the category for list-item numbers is gone, and so is
the category for link targets.

**What the rule does not cover.** Round 6's and round 7's limits stand, but
for markup. A word of the closed list followed by words that hold no number,
and then a unit, passes, and so does a bare unit after "of" or "and". A
list's numbers are not text, so a numbered item that is only a unit passes.
Code is text a reader sees, so markup written in a code span is read as
written, not refused, and the same holds for a tag that a backslash escapes,
a less-than sign that starts no tag, and an autolink, which is a link. A
link's title, a link's target that resolves, a reference definition and a
footnote that nothing cites show the reader no text, and the check does not
read them. A mark that a reader sees after an identifier still ends its
phrase. A construct that starts above the section and runs into it is refused
at the first line of it that the check covers. Since round 9, that holds whatever end the parser reports; see [B16, round 9: source extents](#b16-round-9-source-extents).

**Earlier expectations.** Each earlier runner keeps its code. A control of
round 4's and a control of round 7's now each fail on a single expectation,
and in both the check still fails the altered page and names the added
number. Round 4's control for a figure written as a link's text before a unit
expects that number not to be named a measurement, since the link's target
stood between it and the unit; a reader sees the number before the unit, and
the check now names it a measurement. Round 7's control for a comment inside
a code span expects the line named MARKUP; a reader sees the comment written
out in the code, and the check now reads it as text, names the number
UNCOVERED and refuses nothing. `tools/r8_check_controls.py` holds both forms
with these expectations. The assignment asks that earlier controls keep their
outcomes, and reading only what the parser yields changes both; the change was
published here, in the pull request and in the post, for the manager's
decision, and the manager's [decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481) accepts both; see [B16, round 9: source extents](#b16-round-9-source-extents).

**Its controls.** `tools/r8_check_controls.py` runs each control on an
altered copy (`controls/r8-controls.json`, 73 of 73 PASS). Round 7's 50 come
first, their code unchanged but for the expectations above. The new
controls:

- R624-7's image forms, appended to the attribution row as in R624-7: each
  fails with its line named MARKUP, an image, and the added number named
  UNCOVERED there;
- R625-7's index cases, appended to the index row's part on lane B16, as in
  R625-7: each fails with the row's line named MARKUP, the added number named
  UNCOVERED where it adds a number, both receipts written and no exception;
- a control per construct off the allowlist, written with no digit, so that
  only the refusal can catch it: an image, raw HTML inline and as a block, a
  fenced and an indented code block, a thematic break, struck text, a
  footnote's reference and its definition, and a task list item, each failing
  with the construct's first line named MARKUP by the parser's name for it;
- the check run by an interpreter without the pinned parser, which fails,
  names the parser and writes no receipt.

Against round 7's check and page, the new runner passes the 48 earlier
controls whose expectations stand and fails the other 25
(`controls/r8-controls-on-r7-check.json`): round 7's check passed every image
form and every new construct, stopped on each index case, and ran without the
parser. Round 3's to round 7's runners, unchanged, against the new check: 5
of 5, 7 of 8, 21 of 22, 38 of 39 and 48 of 50, failing only the controls
above (`controls/r8-rerun-r3-controls.json` to
`controls/r8-rerun-r7-controls.json`), whose expectations the manager's [decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481) supersedes.

**The reviews' probes.** Each runs unchanged under the parser's environment,
with its results in `r8/`, a file per probe. R624-7's
`probe_r624_7_markdown_escapes.py`: no form escapes; the unchanged page and
the stated full stop pass, and every other form fails. R624-7's
`probe_r624_7_invisible.py`: every form fails. R625-7's `probe_markup.py`:
every case but the unchanged page fails, and each index case is refused at the
index row's line, with both receipts written and no exception. The earlier
probes give what round 7's record shows, but for the name each refusal now
carries and for a form of R624-6's that may pass or fail: a link reference
definition with a title, which renders nothing, now passes.

**Further forms.** `tools/r8_self_probes.py` (`r8/self-probes.json`) runs
round 5's, round 6's and round 7's forms, then round 8's: Markdown that
renders no character between a number and its unit, a figure inside each
construct off the allowlist, and forms that show the reader nothing. All 138
meet what the rule says: 108 fail and are named at their lines, and 30 pass
as stated. Five of round 7's forms, which failed there, now pass, each as a
reader sees it: an autolink, a tag in a code span, a comment after a
backslash, an unclosed tag, and angle brackets around a link target that
resolves.

With these changes the page passes: every row equals its receipt, every digit
lies in a claimed figure or in an identifier followed by an item of the closed
list, and no construct is refused. The output, `r8/figures-rows.tsv` and
`r8/figures-coverage.tsv`, lists each identifier with its category.
`tools/r8_figures_build.py` regenerates the check byte for byte from
`tools/r8_figures_spec.py`. As before, the hashes of the check, its spec and
its output are in the packet's `MANIFEST.sha256`, not here.

The round's files in the packet:

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r8_check_controls.py` (the check's controls) | 36,524 | `68f85edf41723ad7e87aa7dd4353182666022bb7286cdfa81cccbbe86fb864d6` |
| `controls/r8-controls.json` (73 of 73 PASS) | 26,053 | `83f791b3819086772ce214262e148c0b8e5e6241f1895cb31acc09cecb7ed64b` |
| `controls/r8-controls-on-r7-check.json` | 26,077 | `ddea3af5efc65645fcadde07c5e38f7d7d70149956d7437ae4d6fcc3949a4b40` |
| `tools/r8_evidence_receipt.py` (where the packet is) | 7,353 | `95c3ca5ea4f5ebda66ea3d5bbeb2584cb7dda9773182ac40b3b9aea4c6a1ebee` |
| `r8/evidence-receipt.json` | 59,920 | `1377b5d575bd0adb974a5cfc5f002a8e3d12d222e8b89ff22cd7f6f14709b502` |

### B16, round 9: source extents

Round 8's reviews were NEGATIVE in
[R624-8](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6132342798)
and in
[R625-8](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6132288182),
each with a finding rated MINOR. In R624-8-F1, a raw HTML block opened on the
uncovered line just above the introduction's covered part and closed on its
first covered line was neither refused nor read, because the parser reports
that block as ending on the line before its last. In R625-8-F1, a decision
was asked for on round 8's changed expectations; the manager's
[decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481)
accepts both. Neither review alleged a DUT defect, changed a figure or
reversed a bench verdict. Under the manager's
[assignment for round 9](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132350672),
the operator, [A603], changed where the check places what it reads, documents
only. Nothing on the bench was touched, and no figure above changed.

| Finding | Was | Now | Receipt |
|---|---|---|---|
| R624-8-F1: a raw HTML block from the line above a covered part to its first covered line | Passed: neither refused nor read | Fails: refused at that covered line, named MARKUP, an html_block | `r9/r624-8-html-block-edge-probe-rerun.json` |
| R625-8-F1: changed expectations of earlier controls | Open, for a decision | Accepted by the manager's decision; the earlier runners keep their code and their recorded outcomes | `controls/r9-rerun-r4-controls.json` to `controls/r9-rerun-r7-controls.json` |

**Source extents.** The check now judges each construct by the lines its
source spans, not by the end the parser reports. The pinned parser reports a
raw HTML block that ends at a closing marker (`</pre>`, `</script>`,
`</style>`, `</textarea>`, `-->`, `?>`, `>` or `]]>`) as ending on the line
before its last, and such a block on a single line as ending above it.
So the check takes such a block's last line from the block's own text, which
holds each of its source lines, never from the reported end. The parser also
reports struck text as ending where it starts, and a link or an image whose
text runs over a line break as starting on its last line. So every node spans
all that it holds, and a link or an image starts as many lines above its
reported line as its text holds line breaks. A construct off the allowlist is
refused at the first covered line its source reaches. A node whose source
reaches no covered line is passed over, with all it holds.

**Text the parser misplaces.** In a paragraph, the parser counts a line break
where it yields a soft break or a hard break of trailing spaces, and inside a
code span or inline HTML. A backslash line break, a link's target, title or
reference label over a line break, an image's title over a line break, and a
reference definition that opens the paragraph each hold a line break it does
not count, and it places all that follows on an earlier line. The
introduction's covered part starts partway through its paragraph, so such a
break above that part moved the text of its covered lines onto earlier lines,
the first onto a line the check does not cover, where it went unread. The check now compares the parser's last
line in each paragraph, heading or table cell with the source's; where they
differ it refuses the whole block at its first covered line, named MARKUP by
the parser's name for it, since nothing in it can be placed.

**Lines.** The check counts a document's lines as the parser does, at a line
feed, a carriage return or both. It used to split the page at every
separator Python's `splitlines` knows, a form feed and the Unicode line
separator among them, which the parser reads as text, so such a character
above a covered region shifted that region's lines from the parser's. The
unchanged page holds none of them. Round 9's reader with round 8's rows, run
on the page at `b522bb92`, gives rows, coverage and output byte-equal to
round 8's (`tools/r9_reader_on_r8.py`, `r9/reader-on-r8.json`).

**What the parser reports.** `tools/r9_parser_extents.py` writes small
documents with the lines each node truly spans and runs the check's own
reader on them (`r9/parser-extents.json`): 37 of 37 cases meet what is
stated. The kinds whose reported lines fall short of their source are raw
HTML blocks, images, links and struck text. Six forms of paragraph are
misplaced, the forms named above. Every other kind tried is reported where it
stands: inline HTML, code spans, emphasis, footnotes and their references,
fenced and indented code blocks, thematic breaks, task list items, setext
headings, table cells, and a paragraph continued lazily in a block quote.

**The decision.** The manager's decision accepts round 8's changed
expectations as the correct results under the parser's reading: round 4's
control for a figure written as a link's text before a unit, now named a
measurement, and round 7's control for a comment inside a code span, now read
as code. It supersedes round 4's expectation, with its copies in the runners
of round 5, round 6 and round 7, and round 7's expectation. Both altered pages
still fail, with the number named at its line and both receipts written. The
earlier runners keep their code and their recorded outcomes. Against the new
check, round 3's to round 8's pass
5 of 5, 7 of 8, 21 of 22, 38 of 39, 48 of 50 and 73 of 73, failing only
those superseded expectations (`controls/r9-rerun-r3-controls.json` to
`controls/r9-rerun-r8-controls.json`); they are not reported as wholly
green.

**Its controls.** `tools/r9_check_controls.py` runs each control on an
altered copy (`controls/r9-controls.json`, 97 of 97 PASS). Round 8's 73 come
first, their code unchanged. Each of the 24 new controls replaces whole
lines, so no line moves:

- R624-8's case: `<pre>` on the line above the introduction's covered part,
  and a figure and the block's end on its first covered line. It fails with
  that line named MARKUP, an html_block;
- the other raw HTML blocks whose end the parser reports early, opened and
  closed the same way with no digit, so that only the refusal can catch them:
  each fails the same way;
- struck text opened above the introduction's covered part and closed on its
  first covered line, and an image whose description runs from the Contents
  entry onto the line below it: each fails with its covered line named MARKUP;
- each way the parser misplaces a paragraph's lines, written above the
  introduction's covered part: each fails with that part's first line named
  MARKUP, a paragraph;
- each separator `splitlines` splits at and the parser does not, written above
  the introduction's covered part with a figure on its first covered line:
  each fails with the figure named UNCOVERED there and no row failing.

Against round 8's check and page, the new runner passes the 73 earlier
controls and fails the 24 new ones (`controls/r9-controls-on-r8-check.json`).

**The reviews' probes.** Each runs unchanged under the parser's environment,
with its results in `r9/`, a file per probe. R624-8's
`probe_r624_8_html_block_edge.py`: its case
`intro_pre_from_line_above_with_figure` fails with the introduction's first
covered line named MARKUP, an html_block; no case escapes, and every other
case keeps its exit status and verdict. The cases at the section's heading and
at the Contents entry now also name their block MARKUP there. The earlier
probes each give what round 8's record shows, but for the line at which a form
of R624-7's names the footnote it appends after the page's last line, which
moves as the page grows.

**Further forms.** `tools/r9_self_probes.py` (`r9/self-probes.json`) runs
round 5's to round 8's forms, then round 9's: constructs that open above a
covered part and close inside it, at the introduction, the section's heading
and the Contents entry; each misplacing break, with a figure where a reader
would see it; and, expected to pass, a hard line break of trailing spaces,
emphasis and a link's text over a line break, and R624-8-S1's emoji
shortcode. All 156 meet what the rule says: 122 fail and are named at their
lines, and 34 pass as stated. No earlier form changed its outcome.

**What the rule does not cover.** Round 8's limits stand. As noted in
R624-8-S1, the check reads what the pinned parser yields, and GitHub changes
some of it after the parser: an emoji shortcode is text to the parser, and
its colon a mark that ends a phrase, while GitHub draws an emoji there; and a
link's title, which the check does not read, shows as a tooltip on the link.

With these changes the page passes: every row equals its receipt, every digit
lies in a claimed figure or in an identifier followed by an item of the closed
list, and no construct is refused. `tools/r9_figures_build.py` regenerates the
check byte for byte from `tools/r9_figures_spec.py`; as before, the hashes of
the check, its spec and its output are in the packet's `MANIFEST.sha256`, not
here.

The round's files in the packet:

| Evidence file | Bytes | SHA-256 |
|---|---|---|
| `tools/r9_check_controls.py` (the check's controls) | 43,115 | `11fc340920756e9e86dbe415f132b1eac204c8c5bcca4ce70114e5be09072c1e` |
| `controls/r9-controls.json` (97 of 97 PASS) | 34,200 | `8b5ec97c1b2da15a1cdc9f0c14f3828c59dc47f2fa234999cf8f05118496a92a` |
| `controls/r9-controls-on-r8-check.json` | 34,224 | `9678b0a74ccaaed2b7b0e4a9ae4e6e2a6541619f4469931fb3dd964dbc06b930` |
| `tools/r9_parser_extents.py` (what the parser reports) | 6,592 | `d26cdd914e6da3916adcc64782e357bed4e22a18192adc5fffa5b2593a078885` |
| `r9/parser-extents.json` | 13,280 | `e165a7f72e18d38a0397f2736d8f99441f55bc6a8e56aaf6e9c1d226b4097a44` |
| `tools/r9_evidence_receipt.py` (where the packet is) | 7,868 | `681dc44a5272671ccbce6d1f87cecbf2d812f4c3f47b3175d674f602881487fb` |
| `r9/evidence-receipt.json` | 65,166 | `98dbaee7054883eed16431ae4f2b7e3fd4aacbc6f1392655196c976683a517ec` |
