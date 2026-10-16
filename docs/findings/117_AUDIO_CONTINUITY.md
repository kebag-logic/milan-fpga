<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Audio continuity against the reference peer on the ec0cc0c1 image

Refs #117. Operator [A472], measured 2026-10-01, under the
[bench lane B5 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609).
Round 2 [A473], analysis only with no bench access, restates the attributions
and publishes their analysis under the
[round 2 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5926598386).
Round 3 [A474], docs only with no bench access, restates the Direction B
reason and names exactly which skips each figure covers, under the
[round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5927406852).
Round 4 [A476], docs only with no bench access, states where the packets are
published and which cited hashes are the masked files' originals, under the
[round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5928569912),
and names the reference peer's streams without counting them, under the
[stream-count ruling](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929406675).
Round 5 [A478], docs only with no bench access, withholds the every-channel
captures' sizes, re-pins the evidence archive and names the one masked input
the reproduction reads, under the
[round 5 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5929901339).

This page measures the audio continuity row of #117 acceptance box 4, end to
end. The [first-light pattern](451_TDM8_FIRST_LIGHT.md#method) enters the
DUT's TDM input from the SoC board's McASP0. The DUT's AAF talker carries it to
the reference peer's listener. An external, hardware-clocked audio capture
records the peer's digital output.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS | Every readback equals lanes B3 and B4. See [Identity and setup](#identity-and-setup). |
| Integrity: stream channels 0 and 1 bit-exact at the captured 24 bits, in order | PASS | 31,569,594 of the window's 31,569,600 frames are pattern frames, 0 torn and 0 invalid. The other six are single zero frames. See [Integrity](#integrity). |
| Continuity over 660 s: silent stretches, repeats and skips | FAIL | 334 repeats at the DUT's documented INTERNAL beat. 520 one-frame drops, one every 1.266 s, six of them with a single zero frame, attributed by inference to the peer's output rate. 117,104 more frames in skips of two frames or more: 236 of the 239 of 60 or more are stall-aligned capture-path loss, and the other three, of 72, 78 and 108 frames, are not stall-aligned; those of 2 to 59 are not separated from a packet-sized drop downstream of the peer's receive counters. See [Continuity](#continuity). |
| Restarts: 30 unbind and rebind cycles, rebind to the first valid sample | PASS, 30 of 30 under 1 s | Median 0.0279 s, maximum 0.1358 s; no growth. See [Restarts](#restarts). |
| Direction B, the peer's talker to the DUT's listener | NOT RUN | It was not established whether a known signal can reach the peer's talker channels without a wiring change. The descriptors naming each cluster's signal source were not read, because the survey walk is defective. See [Direction B](#direction-b). |
| #117 audio continuity row | FAIL as measured | The recorded output drops one frame every 1.266 s, attributed by inference to the peer's output rate. The capture path also loses frames. The skips of 2 to 59 frames, and the three of 72, 78 and 108 frames that are not stall-aligned, are not attributed, so a clean window was not recorded. |

These are operator measurements, not review verdicts.

This page reads the row as follows. Over at least 10 minutes every frame is
bit-exact and in order. No frame is missing, repeated or silent. The one
exception is the INTERNAL beat that
[TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff) documents: one
whole-frame repeat every 1.958 s. The register map's
[slip counters](../reference/REGISTER_MAP.md#0x8d4-----media-boundary-slip-counters--slip-kl_chan_map_capture)
record that beat as the standing free-run rule, slips accepted. The restart
bound is #75's 1 s.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, its identity readback, the bench as found and the bound pair.
- **[Method](#method)** -- The pattern, the DUT routing, the binding rule, the capture, the grading rules, restart timing and the runs.
- **[Binding rule record](#binding-rule-record)** -- Every stream-format read and set before each bind, and the restore.
- **[Integrity](#integrity)** -- Bit-exactness and order of stream channels 0 and 1 over the 660 s window.
- **[Continuity](#continuity)** -- Every repeat, skip and silent stretch in the window, by class and by cause.
- **[Restarts](#restarts)** -- Thirty unbind and rebind cycles: stop, restart distribution, growth and one row per cycle.
- **[Direction B](#direction-b)** -- Why the peer-to-DUT direction was not run.
- **[Restore](#restore)** -- The bench as left and the one residual.
- **[Limits](#limits)** -- What this run does not show.
- **[Artifact hashes](#artifact-hashes)** -- Where the three packets are published, and the raw capture and tool identities.
- **[2026-10-16: bench lane B21 on dev 9ef71772](#2026-10-16-bench-lane-b21-on-dev-9ef71772)** -- The capture-path self-test on the current image, why both directions stopped, where lane B5's losses now stand, and the hashes.

## Identity and setup

The image is dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`, as installed.
Lanes B3 and B4 proved its identity. The lane base is dev
`e4b771f93ee870fb2a93f8360b8677bb0b3e2a3b`.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d178f19a`, as lanes B3 and B4 read it |
| Live ENTITY and CONFIGURATION | Byte-equal to the AEM bytes the console dumps from QSPI, `0x110` (312 bytes) and `0x248` (106 bytes); entity `020000fffe000001` |
| UART grader | 10 of 10, at the start and at the end |
| NVM | Slot B seq 238 authoritative, `backed=1`, `pend=1`, commits 2: lane B4's residual, no reset since |
| Identity gate | PASS |

This is CRC consistency and descriptor identity, not a configuration SHA-256
readback.

As found:

- All 4 DUT stream states and every reference-peer stream state were
  unbound.
- Both DUT audio maps were empty, and the DUT selected clock source 0,
  INTERNAL, at 48 kHz.
- The reference peer was in configuration 1 at 48 kHz, on its clock source 0,
  INTERNAL.
- `SLIP_TDM` read 38,142 duplicates and 0 skips at the start.
- The SoC board was at a root prompt, on the boot lane B4 left. Both bridge
  legs ran with the bridge script's command lines, and its USB function was
  configured.

| Binding | Talker output | Listener input |
|---|---|---|
| Direction A | DUT STREAM_OUTPUT 0, stream `0200000000010000` | Reference peer STREAM_INPUT 0 |

| Stream format | As found | Meaning |
|---|---|---|
| DUT STREAM_OUTPUT 0 | `0205022002006000` | AAF, 48 kHz, INT32, 8 channels, 6 frames per packet |
| Reference peer STREAM_INPUT 0 | `0205022001006000` | The same with 4 channels; the input advertises `0215022002006000`, up to 8 channels |

## Method

Every bench action held the shared lock. Every command ran with an explicit
deadline. No flash, reset, power, wiring, instrument setting or USB function
action occurred. No DUT PHY or CSR register was written.

**Pattern.** For tag `t` and TDM frame ordinal `n`, slot `t - 1` carries the
24-bit sample `(t << 16) | (n & 0xffff)` in bits 31:8, as at first light. The
SoC board built one 65,536-frame period of it. Its SHA-256 matched first
light's, and the board played it into McASP0 in a loop. The two bridge legs
were stopped by PID for the runs, after their command lines were checked.
They were restarted afterwards with the script's own command lines.

**DUT routing.** Eight identity mappings on STREAM_PORT_OUTPUT 0 took cluster
`c` to stream channel `c`. The generated shape puts clusters 0 to 7 on TDM
input slots 0 to 7. Stream channel `c` therefore carries tag `c + 1`.

**Binding rule.** Before every bind the controller read the talker's and the
listener's stream formats. When they differed, it set the listener's format
to the talker's and read it back, then sent `CONNECT_RX`. The talker's format
was never set. See [Binding rule record](#binding-rule-record).

**Capture.** The external capture recorded at 48 kHz and 24 bits. Two of its
channels carry the reference peer's output. They were identified by content: in
a 10 s record of every channel, one carries only tag 1 and one only tag 2, in
all 480,000 frames. No other channel carries a pattern word.

**Grading.** A frame is valid when stream channel 0's word is
`(1 << 16) | n` and channel 1's is `(2 << 16) | n`, with the same `n`. Every
captured bit then matches. A frame with both tags right and two ordinals is
torn. Between consecutive valid frames, the ordinal step is 1 in order, 0 a
whole-frame repeat, and `d` greater than 1 a skip of `d - 1` frames. Steps
are taken modulo 65,536, and one of 32,768 or more is a backward step. In
order means 0 backward steps.

**Restart timing.** The restart runs from the `CONNECT_RX` response to the first
frame of the first run of 480 valid frames, 10 ms.

- The response is timed on the controller host's clock and moved to the bench
  host's clock. The offset comes from the lowest-round-trip ping bracketing it,
  taken through the same session. Ping round trips were 0.15 to 0.23 ms.
- Each captured frame is placed at its arrival on the bench host. A frame's
  time is the earliest read time minus the frames read after it, over the
  neighbouring reads, never across a capture stall.
- A restart is therefore an upper bound by the capture path's latency.

**Runs.**

| Run | Purpose | Result |
|---|---|---|
| `a-try1` | First bind | Bind and format set succeeded and the talker streamed; the tool watched two wrong capture channels and timed out, then restored |
| `diag1` | Every capture channel kept, 15 s bound | Identified the two channels; the peer's listener counted media locked, with no late, early or sequence-mismatch count |
| `a-long` | The measurement: initial bind, 660 s untouched, 30 cycles | Graded on this page |
| `cap-test1` | 40 s with a 125 ms capture period | The capture path lost frames at the same rate |

Each run tore down as `a-long` did: unbind, the peer's format restored and read
back, the DUT mappings removed and read back empty, the playback stopped and
the period removed. A further attempt stopped before any map, bind or
playback.

## Binding rule record

| Bind | Talker format | Listener format read | Set | Listener format after |
|---|---|---|---|---|
| `a-long` initial | `0205022002006000` | `0205022001006000` | `0205022002006000`, SUCCESS | `0205022002006000` |
| `a-long` cycles 1 to 30 | `0205022002006000` | `0205022002006000` | none, equal | `0205022002006000` |
| `a-try1`, `diag1` and `cap-test1` | `0205022002006000` | `0205022001006000` | `0205022002006000`, SUCCESS | `0205022002006000` |

Every bind answered SUCCESS with connection count 1. After each run's final
unbind the listener's format was set back to `0205022001006000` and read back
equal.

## Integrity

Window: from 17 ms after the first valid sample of the initial bind, 660.15 s
on the bench host's clock, untouched.

| Stream channel | Expected tag | Captured words | Words with the expected tag | Other non-zero words | Result |
|---|---|---|---|---|---|
| 0 | 1 | 31,569,600 | 31,569,594 | 0 | Bit-exact, in order |
| 1 | 2 | 31,569,600 | 31,569,594 | 0 | Bit-exact, in order |

| Frames | Valid | Torn | Invalid non-zero | Zero |
|---|---|---|---|---|
| 31,569,600 | 31,569,594 | 0 | 0 | 6 |

The window has 0 backward steps. Across the whole run, 39,356,186 frames,
every non-zero word of channel 0 carries tag 1 and every one of channel 1
tag 2, with no torn frame. The
3,407,496 zero frames are the silence before the first bind, in the holds and
after the last unbind, and the window's six. The lane packet `b5-a473` derives
these counts from the raw pair.

## Continuity

<!-- continuity -->
| Class | Events | Frames | Per second |
|---|---|---|---|
| Whole-frame repeat | 334 | 334 | 0.508 |
| One-frame skip | 526 | 526 | 0.800 |
| Skip of 2 to 59 frames | 521 | 7,176 | 0.792 |
| Skip of 60 frames or more | 239 | 109,928 | 0.363 |
| Silent stretch, one frame each | 6 | 6 | - |

The window holds 657.7 s of captured audio in 660.15 s on the bench host's
clock: the capture delivered 117,653 frames fewer than 48 kHz would. Each cause
below is stated only as strongly as the published analysis carries it. The lane
packet `b5-a473` holds that analysis: `b5_attrib.py`, the derived read record
of the window and the receipts that every figure below comes from. The round 3
packet `b5-a474` adds `b5_round3.py` and the receipts of the figures round 3
adds. As published, the read record is gzip-compressed: restore it with
`gunzip -kf a-long-reads.u16.gz` before running either tool. Where the
packets are published, and the steps, are under
[Artifact hashes](#artifact-hashes).

**Repeats: the DUT's INTERNAL beat.** Counted in content frames, the repeats
fall 93,989 to 93,992 frames apart. That is the 1.958 s beat, one whole-frame
repeat per crossing ([TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff)).
`SLIP_TDM` rose 327 between the window's first and last console reads,
640.47 s apart: 0.511 per second. Four spacings are two beats, where capture
losses hid a repeat: 338 beats in 660.15 s, 0.512 per second.

**How the read-time record places a loss.** The bench host stamped every read
of the capture: one capture period of 480 frames, nominally 10 ms apart. A
frame lost inside the capture path, after the capture samples it, delays every
later read by its duration. The capture's delivery deficit, host time against
the frames delivered at 48 kHz, then steps up by the frames lost. A frame
already missing from the signal the capture samples leaves the deficit as it
was.

- A stall is a read interval over 15 ms, the grader's definition. The window
  holds 220, one every 3.00 s (2.99 to 3.02 s).
- The step across a skip compares the deficit's floor over 11 reads on each
  side, which removes read-to-read jitter. Skips of two frames or more fewer
  than 16 reads apart are taken together, as one cluster.
- Controls: across the 267 beat repeats and the 419 one-frame skips clear of
  other skips, the floor moves by at most 3.2 frames. A planted loss of 6, 12
  or 24 frames is recovered within 5, by construction: the step is linear in
  a loss, so a plant reads back as the floor's own step there plus the plant.
  That control checks where the floor windows sit, not the test's power.
  Over the 51,828 read positions clear of skips of two frames or more, the
  floor moves by more than 4 frames at 9 places, 7 of them by 1 ms, 48
  frames, where no frame is missing.

**Skips of 60 frames or more: 236 of the 239 are stall-aligned capture-path
loss.**

- 236 of the 239, 109,670 frames, fall one or two reads after a stall. Each
  of the 220 stalls is followed by exactly one skip of 240 frames or more.
- The other three, 258 frames, are not stall-aligned, and the stall
  attribution does not cover them. One skip of 72 frames falls 34.0 s into
  the window. Skips of 78 and 108 frames fall on consecutive reads 634.0 s
  in. Each falls in a read interval stretched by 1.8 to 2.1 ms, against 1.50
  to 2.25 ms of audio skipped, and the nearest stall is 125 reads or more
  away.
- The stalls' excess over the 10 ms period sums to 109,069 frames, against
  109,670 in the 236 stall-aligned skips. All 239 hold 109,928.
- The DUT's talker sent 8,000 packets a second throughout, by `AAF_FRAMES`.
  The peer's listener counted no sequence mismatch, late or early timestamp.
- A 125 ms capture period lost frames at the same rate (`cap-test1`).

**Skips of 2 to 59 frames: not separated.** 507 of the 521 are whole multiples
of six frames, 354 exactly six. Six frames is both a USB microframe at 48 kHz
and an AAF packet, so frame counts alone cannot separate a capture loss from a
packet-sized drop.

- 284 of them, 5,386 frames, fall in the 222 clusters that hold a skip of 60
  frames or more. Across those clusters the deficit steps by 116,138 frames in
  all, against 115,314 in their skips. That is consistent with capture-path
  loss, though no single cluster separates its smaller skips.
- The other 237, 1,790 frames, fall in 121 clusters away from any stall. In
  none of them does the deficit step by the frames skipped. In 95, whose skips
  total 12 to 36 frames each, it stays within 3 frames. In 22 it steps by
  1 ms, and in 4 it matches neither.
- The 1 ms steps concentrate at these clusters. At the 51,828 clear read
  positions the floor steps by 1 ms at 7 places. One floor test spans 16
  reads, so that is 7 in about 3,240 windows, and about 0.26 of the 121
  clusters would step by 1 ms by chance, against the 22 observed. This is an
  observation; the page does not attribute it.
- So the record shows no capture-path loss of their size. They are not
  separated from a packet-sized drop downstream of the peer's receive
  counters, or from a drop at the capture's input.

**One-frame skips: attributed to the peer's output rate by inference.** The
526 one-frame skips form 520 slip events, each of which removes one frame.

- 514 events are a single one-frame skip.
- Six take the form skip, zero frame, skip, six frames apart. They are the six
  silent stretches. No other zero frame occurs in the window.
- The grader leaves the two transitions next to each zero frame ungraded, so
  round 3 read those ordinals from the graded pair. Each zero frame sits
  between consecutive ordinals and replaces no pattern frame. Each of these
  six events drops two frames and inserts one zero frame: one frame fewer in
  all, like a single skip.
- Consecutive events fall 60,546 to 60,923 content frames apart, median
  60,768, or 1.266 s. One spacing is two periods, where a capture loss hid an
  event.
- That is one frame in 60,768, a constant rate difference of 16.46 ppm between
  the stream and the recorded output.
- At the 419 clear of other skips the capture's delivery deficit stays within
  3 frames, so the capture path did not lose them after sampling.
- The peer's media clock source is its INTERNAL source, not the stream. An
  output on its own clock that drops one frame each time the stream runs one
  frame ahead fits the period. That is an inference: a drop at the capture's
  input would look the same in this record.

No silent stretch is longer than one frame.

## Restarts

Each cycle took one `DISCONNECT_RX`, a 2 s hold, the binding rule and one
`CONNECT_RX`. The cycle then waited for the first valid run, capped at 30 s,
and 3 s more. A cycle counts as a restart only when no valid frame falls from
the unbind response plus 0.5 s to the bind response.

<!-- restart-distribution -->
| Population | Count | Below 1 s | Min, s | Median, s | p95, s | Max, s |
|---|---|---|---|---|---|---|
| Demonstrated restarts | 30 | 30 | 0.0262 | 0.0279 | 0.0389 | 0.1358 |

| First ten median, s | Last ten median, s | Slope, s per cycle | 95% slope interval, s per cycle | Residual df |
|---|---|---|---|---|
| 0.0274 | 0.0280 | -0.000664 | [-0.001495, +0.000166] | 28 |

The p95 is the nearest-rank 95th percentile, as `grade_a.py` computes it: the
29th of the 30 sorted restarts, cycle 20's. Linear interpolation over the same
30 gives 0.0344 s. The interval uses ordinary least squares and Student's t.
It assumes independent errors with constant variance.

- **Stop.** In every cycle the last valid frame arrived 14.4 to 24.6 ms after
  the `DISCONNECT_RX` response, and the hold stayed silent.
- **Silence before the restart.** Every frame between the rebind and the first
  valid run is zero, so the stream restarts with no partial or invalid frame.
- **Initial bind.** It followed 139 s unbound, after `diag1`, and took
  0.2676 s from the response.
- **Cycle 1.** The slowest, at 0.1358 s, it followed the 660 s window.
- **Cycle 20.** A 19.8 ms capture stall fell inside its restart. Its 0.0389 s
  can be late by up to that stall.
- **Response time.** The `CONNECT_RX` response came 7 to 9 ms after the
  command. Measured from the command, restarts run 34 to 144 ms.

<!-- restart-cycles -->
| Cycle | Hold, s | Stopped in hold | Last valid after unbind, s | Restart, s | From command, s | Capture stall in restart | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2.018 | yes | 0.0150 | 0.1358 | 0.1439 | no | PASS |
| 2 | 2.019 | yes | 0.0150 | 0.0282 | 0.0364 | no | PASS |
| 3 | 2.019 | yes | 0.0155 | 0.0269 | 0.0347 | no | PASS |
| 4 | 2.018 | yes | 0.0152 | 0.0273 | 0.0350 | no | PASS |
| 5 | 2.022 | yes | 0.0246 | 0.0276 | 0.0351 | no | PASS |
| 6 | 2.018 | yes | 0.0151 | 0.0287 | 0.0360 | no | PASS |
| 7 | 2.018 | yes | 0.0147 | 0.0262 | 0.0344 | no | PASS |
| 8 | 2.018 | yes | 0.0145 | 0.0271 | 0.0350 | no | PASS |
| 9 | 2.018 | yes | 0.0145 | 0.0268 | 0.0348 | no | PASS |
| 10 | 2.017 | yes | 0.0154 | 0.0279 | 0.0354 | no | PASS |
| 11 | 2.017 | yes | 0.0154 | 0.0288 | 0.0362 | no | PASS |
| 12 | 2.019 | yes | 0.0147 | 0.0270 | 0.0353 | no | PASS |
| 13 | 2.017 | yes | 0.0148 | 0.0281 | 0.0355 | no | PASS |
| 14 | 2.018 | yes | 0.0155 | 0.0285 | 0.0358 | no | PASS |
| 15 | 2.019 | yes | 0.0149 | 0.0274 | 0.0354 | no | PASS |
| 16 | 2.018 | yes | 0.0148 | 0.0283 | 0.0357 | no | PASS |
| 17 | 2.017 | yes | 0.0155 | 0.0282 | 0.0355 | no | PASS |
| 18 | 2.019 | yes | 0.0155 | 0.0270 | 0.0352 | no | PASS |
| 19 | 2.019 | yes | 0.0152 | 0.0273 | 0.0354 | no | PASS |
| 20 | 2.018 | yes | 0.0156 | 0.0389 | 0.0463 | yes, 19.8 ms | PASS |
| 21 | 2.018 | yes | 0.0144 | 0.0279 | 0.0354 | no | PASS |
| 22 | 2.017 | yes | 0.0154 | 0.0275 | 0.0349 | no | PASS |
| 23 | 2.018 | yes | 0.0150 | 0.0280 | 0.0355 | no | PASS |
| 24 | 2.018 | yes | 0.0146 | 0.0284 | 0.0356 | no | PASS |
| 25 | 2.018 | yes | 0.0151 | 0.0285 | 0.0359 | no | PASS |
| 26 | 2.017 | yes | 0.0145 | 0.0283 | 0.0355 | no | PASS |
| 27 | 2.019 | yes | 0.0153 | 0.0271 | 0.0352 | no | PASS |
| 28 | 2.018 | yes | 0.0148 | 0.0282 | 0.0355 | no | PASS |
| 29 | 2.019 | yes | 0.0152 | 0.0269 | 0.0351 | no | PASS |
| 30 | 2.018 | yes | 0.0145 | 0.0275 | 0.0349 | no | PASS |

## Direction B

NOT RUN. The lane runs Direction B only if a known signal can drive the
reference peer's talker channels without a wiring change, and that was not
established. The peer's dynamic audio map on its STREAM_PORT_OUTPUT 0 takes
the talker's stream channels only from the audio clusters that port owns. Its
AUDIO_UNIT declares no external or internal port and no routing element. Each
AUDIO_CLUSTER descriptor records its cluster's signal source in
its `signal_type`, `signal_index` and `signal_output` fields (IEEE 1722.1
7.2.16). That source need not be a physical input. The repository's own
encoding writes `signal_type` INVALID for a stream input port's cluster and
AUDIO_UNIT for a stream output port's cluster
(`avdecc/aem_descriptors.py:590`, `avdecc/aem_assemble.py:289-294`). A peer
that follows the same convention would name its audio unit, so reading those
descriptors might not settle the question either. They were not read, because
the survey walk is defective, as the next paragraph records. So whether a
known signal can reach the peer's talker channels without a wiring change is
open. The external capture was used as a capture point only.

The survey's walk of the audio unit is defective for reuse. Its code reads
the audio clusters with descriptor type 0x0010 and the maps with 0x0014.
IEEE 1722.1 Table 7.1, as the repository encodes it in
`avdecc/aem_descriptors.py`, gives AUDIO_CLUSTER 0x0014 and AUDIO_MAP 0x0017.
The walk's external port types are each one too high by the same table. What
it sent was one read of type 0x0010, EXTERNAL_PORT_INPUT, at the index of
each cluster the peer's stream ports own, each answered NO_SUCH_DESCRIPTOR. It
sent no map read, because the peer's stream ports declare no static map, and
no external port read, because the audio unit declares no external port. So no
AUDIO_CLUSTER or AUDIO_MAP descriptor was read. The dynamic maps above came
from GET_AUDIO_MAP.

The DUT's STREAM_INPUT 0 lists `0205022002006000` and `0215022002006000`. It
could therefore take the peer's four-channel talker format under the binding
rule.

## Restore

| State | As left |
|---|---|
| Stream states, DUT and reference peer | All unbound; the end census equals the start in every entry but one, the DUT's live propagation delay |
| Reference peer STREAM_INPUT 0 format | `0205022001006000`, as found, read back after every run |
| DUT audio maps | Both empty, read back |
| DUT console words | Equal to the start but for live counters (`AAF_FRAMES`, `AAF_PAIRS`, `SLIP_TDM`, `GPTP_PDELAY`, time) |
| DUT saved state | NVM line unchanged: slots 237/238, commits 2, `pend=1`; no commit in this lane |
| DUT synchronization | SYNC=1, ASCAPABLE=1, TU=0, grandmaster unchanged; UART grader 10 of 10 |
| SoC board | Same boot; both bridge legs running with the script's command lines under new process IDs; PCM states, USB function and the fault scan as at the start; no task file left |
| Controller host | No task process; staging removed |
| Bench host | Both USB audio devices present |

The bridge legs run under new process IDs. No other residual remains.

## Limits

- Skips of two frames or more removed 0.37% of the frames, 0.35% in the 236
  stall-aligned skips of 60 frames or more. A discontinuity inside a lost
  stretch cannot be seen: four beat repeats and one slip event were hidden
  that way.
- The attribution of the one-frame skips to the peer's output rate is an
  inference from their period and the peer's INTERNAL clock source. A drop at
  the capture's input would look the same in this record. A run with the
  peer's media clock following the stream would test it. That needs a clock
  source change on the peer, outside this lane.
- The 237 skips of 2 to 59 frames away from any stall are not attributed. The
  read-time record shows no capture-path loss of their size, but it cannot
  place them between the peer's receive counters and the capture's input.
  Whether a capture path that loses no frames removes them is open.
- The three skips of 72, 78 and 108 frames that are not stall-aligned,
  258 frames, are not attributed either. The stall attribution does not cover
  them.
- The floor test assumes that a frame lost inside the capture path delays
  every later read. It resolves about 4 frames. The 1 ms steps it also finds
  are not explained. They concentrate at the 121 clusters away from any
  stall: 22 of them, against about 0.26 by chance.
- One run, at the DUT's and the peer's INTERNAL clock sources only.
- Only stream channels 0 and 1 are observed.
- The restart is timed to the sample's arrival on the bench host, not to the
  peer's output.
- Printed precision is not calibrated accuracy.

## Artifact hashes

The three packets are public on branch `b5-review-evidence`, pinned at commit
`9006c78e354d5a2f244fd606c55790a825304bd3`:
[`review-evidence/b5-r1`](https://github.com/kebag-logic/milan-fpga/tree/9006c78e354d5a2f244fd606c55790a825304bd3/review-evidence/b5-r1).
The lane packet `b5-a472` is its `author/` directory, the round 2 packet
`b5-a473` is `author-r2/` and the round 3 packet `b5-a474` is `author-r3/`.
Its `MANIFEST.json` records each published file's `original_sha256` and
`published_sha256`, and `path_redacted` marks the files published
label-masked. The steps below run on those three directories at that commit.

The lane packet `b5-a472` holds the tools, per-action evidence, summaries and
the raw-artifact index. Raw files stay outside the tree and the packet, each
identified by SHA-256, and all but the every-channel captures by size too. The
round 2 packet `b5-a473` holds the analysis tools, their receipts and the
window's derived read record:
131,540 bytes, SHA-256
`2183d57f0646cf94405b95aea5547b83f5ff0b9190ac0bd1bdcc87760c919961`, derived
from the `a-long` read times below. As published, the packet carries that
record gzip-compressed, as `a-long-reads.u16.gz`. To reproduce the figures:

1. In the round 2 packet's receipts, run `gunzip -kf a-long-reads.u16.gz`.
   The `-f` replaces the `a-long-reads.u16` published beside it, a copy with
   three bytes masked by the archive step. Then `sha256sum a-long-reads.u16`
   must print the hash above.
2. Run `b5_attrib.py figures` with the lane packet and that receipts
   directory. Its output equals the round 2 packet's `attribution.txt`.
3. Run `b5_round3.py figures` from the round 3 packet `b5-a474` with the same
   two directories. Its output equals that packet's `round3_figures.txt`.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `a-long` graded pair, 24-bit | 236137116 | `2ac666fb5ff6284cc665887758ad6f2754918e5b7932258a06ea7efeeec99bdf` |
| `a-long` read times | 1967832 | `717141923d15fc32f09e998d3af779b9e95d8a263091c039e7165bc3c7728262` |
| `a-long` every channel, 10 s | withheld | `f334406790ef4e769d3b682ff56506568467277b9224acf82e168ab8af838d89` |
| `a-long` full grade | 180433 | `e06fa4602138c30b84f19f7ba78db88b4e394d07bedc8939474dafa2ac07ed88` |
| `diag1` every channel, 25 s | withheld | `b8cc1f50fc54ba4bf5bb803056af6ab229e574798bb337249400879098f341be` |
| `cap-test1` graded pair | 14472180 | `c8d34f62402a0af3a1c20b47325a9c859975cea88426a4a3029dabbddd422616` |
| `a-try1` watched pair | 11474046 | `e23aaf2e9f82fbfdb0d89a72ebeb782ae036692af73eec32c6c8c2aa7c5805dc` |
| Capture as found, every channel, 3 s | withheld | `7eabb3761ba13566ceb3e826d66a742cd865f23f7ca5eebce23af50ea4bf465f` |
| Pattern period, built on the SoC board | 2097152 | `b6a92e9724e945354c3f8fc5178cec7bb8fd0e62d52bd9ee7f13ed5347bfa97c` |

| Tool | Role | SHA-256 |
|---|---|---|
| `run_a.py` | one locked run: playback, routing, binding rule, capture, cycles, teardown | `dcc616aea7842b8b1a574d2e9ba2647e71f344d95ee4473ae2c369802e686ad6` |
| `grade_a.py` | integrity, continuity and restart grade | `37e7dd967a4edf9e88b6b947cc64d5024b99b7e4b891491d955ae258069e8ac9` |
| `b5_tables.py` | summary and page tables | `4f9e79fce9c385f109d7afdf4e5dba42b43b4774b707241fcd36299d5c9ca67a` |
| `b5_ctl.py` | controller transactions: formats, listener-only format set, binds, DUT maps | `47b7387ae4f901ab04a5038e68ee721234b7044f9b61437414cd3f6ff0b73064` |
| `avdecc_ro.py` | raw AVDECC reader, lane B3's copy | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` |
| `console_read.py` | read-only DUT console reader, lane B3's copy | `652d6f839b1dff74c5ddbdfc4fc9fd42c250f0cd2b7e2eeeb5b7cc838a74ee63` |
| [UART grader](../../scripts/baremetal_uart_smoke.py) at the lane base | identity and restore | in the lane packet |

The `run_a.py` and `grade_a.py` hashes above are the unmasked originals',
recorded as `original_sha256` in the archive's `MANIFEST.json`. Their
published copies are label-masked, recorded with `path_redacted`, so check
them against `published_sha256` instead. The mask replaces code constants in
both, so those copies are for reading and do not run as published. The read
record's hash above is likewise its `original_sha256`, and the copy published
beside the `.gz` is recorded with `path_redacted`. In the lane packet,
`HANDOFF.md`, `RAW-ARTIFACTS.json`, `gates/gates.txt`, the two
`restore/host-*.txt`, the `console.txt` and `events.jsonl` of `a-long`, `diag1`
and `cap-test1`, and the `summary.json` of `a-long` and `cap-test1` are
published label-masked too. The page cites no hash of them. Of these,
`b5_attrib.py` and `b5_round3.py` read only the `a-long` `summary.json`, and
both still reproduce their receipts byte for byte at the pinned commit. The
other tool hashes match the published bytes. The masked `RAW-ARTIFACTS.json`
keeps every raw file's SHA-256, and every size but the every-channel
captures', which it withholds, as the table above does.

`a-long` ran the `run_a.py` revision before the capture-period option, whose
default is the value it used. `cap-test1` ran the listed revision.

`b5_ctl.py` is listed at the revision the end snapshot staged and hashed. The
revision that ran the binds and format sets cannot be established from the
packet's records. The start snapshot hashed
`24208ef21e30d6f41d90e39860de8c6272b4e3ad165a33cf5a18f9d572317566`
(8,642 bytes), and its descriptor survey had no audio-unit walk. The survey
70 s later carries that walk, so the controller copy changed with no hash
recorded. The run tool records none either. The binding rule record rests on
the logged exchanges, not on the tool's identity.

Round 2 adds `b5_attrib.py`
(`f1d9b2ba456672cdf00ed86a645b9ab35c4d11fef3bb5ac9363c70885a5dfa40`), which
derives the window's read record and computes the attribution figures. It
also adds `b5_records.py`
(`c68ecf7b47b8bfc7a765b11140bf751b6f90266178dde0448997bdf3a38ac738`), which
checks the controller revision record and the peer's descriptors.

Round 3 adds `b5_round3.py`
(`415ef1b0e7d26cb821235fe22c81b23a42035afb73b4baef3cf24bd08099ac4d`). It
computes the figures round 3 adds from the same published inputs: which skips
the stall alignment covers, the 1 ms steps against clear positions, the
planted control's linearity and the descriptor reads the survey sent. It also
reads the ordinals around the window's zero frames from the local graded pair.

## 2026-10-16: bench lane B21 on dev 9ef71772

Refs #117. Operator [A625], measured 2026-10-16, under the
[bench lane B21 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-6208207821).
The image is dev `9ef71772`, as installed on 2026-10-15 and as lanes B18 and
B19 proved it. It was not flashed, reset or power-cycled. The lane base is
dev `4a9b5a2a74fe793a637745fd3ccf51ad2eaf93b4`.

The lane STOPPED after step 1. The capture-path self-test was not clean in
either 10-minute window, and the SoC board's console stood at a login prompt,
so neither direction ran. The sections above, lane B5's record on the
`ec0cc0c1` image, are unchanged.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS, 11 of 11, at the start and at the end | See [B21: identity and as found](#b21-identity-and-as-found). |
| Step 1, capture-path self-test | NOT CLEAN, in both 630 s windows | The capture path lost 336 and 10,945 frames, every loss a whole number of 1 ms USB frames, inside stall episodes. Lane B5's 3.00 s stall recurrence is absent. See [B21: capture-path self-test](#b21-capture-path-self-test). |
| Step 2, Direction A with both taps and the DUT CSRs | NOT RUN, STOP | Step 1 is not clean, and the pattern source needs a root shell on the SoC board. See [B21: directions A and B](#b21-directions-a-and-b). |
| Step 3, Direction B | NOT RUN, STOP | The same two reasons; its capture point is the SoC board. |
| #117 audio continuity row | Not graded on this image; not passed | Lane B5's losses outside the capture path stay unplaced. See [B21: what a debug trace would need to show](#b21-what-a-debug-trace-would-need-to-show). |

These are operator measurements, not review verdicts.

### B21: identity and as found

Lane B19's identity method ran, with only its environment and staging
changed, at 04:56:04 UTC and again at 05:29:44 UTC. Both passed 11 of 11:

- console `ID=4d494c4e VERSION=00020060`;
- AEM CRC32 `5ba355eb` over its 7,512 bytes;
- live ENTITY and CONFIGURATION byte-equal to the QSPI AEM bytes;
- entity `020000fffe000001`, firmware `2.96.0`;
- clock sources 0 INTERNAL, 1 CRF on STREAM_INPUT 1, 2 on STREAM_INPUT 0;
- UART grader 10 of 10, and ADP model `001bc5c1935893e1`.

As found at 04:56:25 UTC:

| State | As found |
|---|---|
| DUT STREAM_OUTPUT 0 to the reference peer's STREAM_INPUT 0 | Bound, both formats `0205022002006000` |
| DUT STREAM_OUTPUT 1, the CRF talker | Bound to the reference peer's CRF input, which the peer selects as its media clock source |
| Reference peer STREAM_OUTPUT 0 to DUT STREAM_INPUT 0 | Bound, both formats `0205022001006000` |
| DUT clock source | 0, INTERNAL, 48 kHz |
| DUT audio maps | STREAM_PORT_INPUT 0: 4 mappings; STREAM_PORT_OUTPUT 0: 8 identity mappings |
| `SLIP_LB`, `SLIP_TDM`, `RENDER_STAT` | `0x0000FFFF` (dups at the ceiling), `0x00000000`, `0x0000020C` (fill 12, converged, 0 rails) |
| DUT saved state | Image seq 335, `VD_OK`, `pend=0` |
| SoC board console | A `login:` prompt, not a root shell |

The SoC board check is one read-only command through lane B5's console
runner. Its readiness line reached the login prompt as a login name. A 75 s
passive read, which wrote nothing, saw login's own 60 s timeout return the
console to `login:`. No credential was typed, held or stored.

### B21: capture-path self-test

**Method.** No loopback inside the external capture can be set and restored
in software: the capture exposes no mixer control to the bench host. So the
self-test is the deficit-only one the assignment allows.

- The external capture ran alone, with no DUT, peer, SoC board or controller
  action. Its input carried one constant word throughout, so content was not
  graded.
- The reader is lane B5's (`run_a.py`), with its capture format, a period of
  480 frames and a buffer of 24,000. It stamps every read with the frames
  delivered and the bench host's monotonic clock.
- The analysis imports `b5_attrib.py` unchanged for its definitions. A stall
  is a read interval over 15 ms. The delivery deficit is the host time at
  48 kHz less the frames delivered. A loss inside the capture path after
  sampling raises its floor for good. The floor test compares 11 reads on
  each side and resolves about 4 frames.
- Two changes. The deficit counts the frames each read delivered: a read
  after a stall can deliver more than one period, and B5's window held none.
  The drift over one floor test is the median step, which the steps cannot
  pull.
- A sampler read the bench host's CPU counters, steal time included, and
  every interrupt row at 20 Hz. The second run also read the pressure stall
  totals and the compaction and allocation-stall counters.

| Run | Window, UTC | Seconds | Reads | Stalls over 15 ms | Longest read, ms | Stall spacings of 2.99 to 3.02 s | Stall episodes | Losses | Frames lost | 1 ms steps, no loss signature | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `st-long` | 05:01:20 to 05:11:51 | 630.0 | 63,002 | 11 | 23.2 | 0 | 2 | 2 | 336 | 11 | Not clean |
| `st-long2` | 05:15:22 to 05:25:53 | 630.1 | 62,934 | 123 | 88.4 | 0 | 16 | 18 | 10,945 | 13 | Not clean |

Lane B5's window, for comparison, held 220 stalls, one every 3.00 s.

**What the losses are.** Every floor step larger than 1 ms is a whole number
of milliseconds, within 0.02 ms. `st-long` lost 4 and 3 ms. `st-long2` lost
2 to 88 ms per event, 228 ms in all. A millisecond is one USB frame, 48
frames of audio. Every loss falls in a stall episode.

The capture sits on one USB host controller, which interrupts once per USB
frame, 1,000 times a second. Each figure below is that controller's
interrupt shortfall over 2 s around an event, against the count its own rate
predicts. The pressure figures are milliseconds per second, `st-long2` only.

| Event class | `st-long`: events, median shortfall | `st-long2`: events, median shortfall, largest | `st-long2`: I/O full, memory full, CPU some, medians |
|---|---|---|---|
| Losses | 2, +13.6 | 18, +21.3, +103.0 | 5.39, 0.00, 0.45 |
| 1 ms steps | 11, +0.6 | 13, -0.2, +26.8 | 5.90, 0.00, 0.36 |
| Stalls with no step | 10, +6.6 | 82, -0.8, +102.9 | 5.62, 0.00, 0.42 |
| 300 clear control times | +0.6, largest +4.5 | -1.2, largest +7.8 | 5.51, 0.00, 0.28 |

- **The losses belong to the recording side.** Each comes with frame
  interrupts missing from the capture's USB host controller. The bench host's
  CPU, memory and I/O pressure at the losses equal their control values.
  Steal time was 0.003% and 0.008% of CPU time, at most 6 ticks across any
  stall. So the cause lies below the load the bench host can see, for
  example in interrupt delivery to that controller. Its source was not found
  on the bench host, and no host configuration was changed: that change is
  the manager's.
- **No 3.00 s recurrence.** No two stalls are 2.99 to 3.02 s apart. The
  episodes come irregularly, 2 in `st-long` and 16 in `st-long2`.
- **No loss under 1 ms.** In 1,260 s the capture path lost no block smaller
  than one USB frame, though the floor test would see one of 6 frames. A
  drop at the capture's input leaves no deficit trace, so this test cannot
  see one.
- **The 1 ms steps.** They come about every 60 s: in `st-long`, 8 of the 10
  spacings between them are 60.19 to 60.33 s. They carry no interrupt
  shortfall. Lane B5's content saw seven such steps with no frame missing.
  They are not attributed.

Step 1's condition to go on, a clean 10-minute window, was not met.

### B21: directions A and B

NOT RUN. The lane stopped before step 2, for two reasons.

- Step 1's window was not clean, and the assignment goes on only after a
  clean one.
- Direction A plays the first-light pattern into McASP0 from a root shell on
  the SoC board. Direction B records McASP0 there. The board's console stood
  at a login prompt, and the lane holds no credential. The board's USB audio
  bridge resamples, so it cannot carry a bit-exact grade.

Both bindings were in place as found, so neither direction would have needed
a bind. Neither tap was opened.

Two DUT reads frame the lane, 04:56:25 and 05:29:50 UTC, while the as-found
streams ran. `SLIP_TDM` read 0 at both, and `RENDER_STAT` read converged with
0 rails at both. `SLIP_LB` stood at its ceiling and carries no rate. These
are two reads, not a graded window.

| Lane B5 loss class | Placement after B21 |
|---|---|
| Skips of 60 frames or more, 236 stall-aligned | Recording side, as lane B5 inferred. With no DUT or peer in the path, the capture path still loses frames in stall episodes. Today the episodes are irregular and each loss is whole USB frames; lane B5's stalls came every 3.00 s. |
| The three unaligned skips of 72, 78 and 108 frames | Not placed. They are 1.5, 1.625 and 2.25 ms, not whole USB frames, so they do not match the self-test's loss signature. |
| Skips of 2 to 59 frames | Not placed. The capture path lost no block under 1 ms in 1,260 s, so the self-test does not reproduce them. They lie at the capture's input or upstream of it. |
| One-frame drops every 1.266 s | Not re-tested. The peer now follows the DUT's CRF, the state Direction A would test. |
| Whole-frame repeats at the INTERNAL beat | Not graded. `SLIP_TDM` read 0 at both reads. |

### B21: what a debug trace would need to show

Step 5 is the manager's decision. If Direction A runs and a skip is still
unplaced, a trace port would need these records, each time-stamped on the
DUT's gPTP time:

- per AAF PDU the talker sends: stream ID, sequence number, `avtp_timestamp`,
  and the TDM frame ordinal of its first sample at the capture handoff;
- per TDM frame close and media-tick snapshot: the events `SLIP_TDM` counts,
  each with its frame ordinal;
- per AAF PDU the listener receives: sequence number, `avtp_timestamp`, and
  the render stage's prefill, rail and underrun events.

### B21: restore

| State | As left |
|---|---|
| Stream states, formats, maps and clock sources | End census equals the start in 45 of 46 entries; the other is the DUT's live propagation delay |
| DUT console words | Equal to the start but for live counters; `SLIP_TDM` 0, `SLIP_LB` `0x0000FFFF`, NVM line unchanged |
| DUT synchronization | SYNC=1, ASCAPABLE=1, TU=0, grandmaster unchanged; UART grader 10 of 10 |
| Outlets | All on, as found; none switched |
| SoC board | Console at `login:`, as found |
| Controller host | No gPTP daemon or task process; staging removed |
| Taps | Not used |

Everything sent to the DUT and the peer was a read: console reads and
ATDECC reads. Nothing in the controller host's or the bench host's
configuration changed. The SoC board received only the console runner's
carriage return and readiness line, which login took as a name and timed
out.

### B21: limits

- The self-test is deficit-only. Its input was constant, so it shows loss
  inside the capture path, not at its input.
- Two windows on one morning. The stall episodes came irregularly, and their
  rate differed thirtyfold between the windows.
- The interrupt and pressure figures place the losses below the bench host's
  visible load. They do not name the cause.
- No direction ran on this image, so lane B5's figures are the latest graded
  ones.

### B21: artifact hashes

Packet `117-b21-a625` holds the tools, the per-action records, the analysis
outputs, the derived read records, `RAW-ARTIFACTS.json`, `HANDOFF.md` and
`MANIFEST.sha256`; its publication is the manager's. Raw files stay outside
the tree and the packet, each identified by size and SHA-256.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `st-long` read-time record | 1512096 | `7a1876381494ecd0b6ad626c57e7d81da8716d11a07a5b41f7306a12a0ea783a` |
| `st-long` derived read record, uint16 | 126004 | `fc3fcf7e4528652c93b1b13d65d9e7a231bb547ee193f5741d79828d0839f9ad` |
| `st-long` captured pair | 181451676 | `6026490a18c0f769560e17a6f3f48ade47331f0f87dfa26440539330a14e60ca` |
| `st-long` host samples | 301388550 | `5bf9238d04b296673521c4ee1c2d5b389d29db1251d3812b1254f3e200ab2f9b` |
| `st-long2` read-time record | 1510464 | `5f798357ae75af4c089dcc89c3d5308a202eec9661a06e42b90b20fe788435d1` |
| `st-long2` derived read record, uint32 | 251736 | `58a24e98eb74fc9fa3ffd01e5a1d588c68056c324bcc6d1299128921b0561bee` |
| `st-long2` captured pair | 181391256 | `67805c6fedb2b67d4eb07b7f4f590e978db0a8519f844ab04a1d3f11417405e4` |
| `st-long2` host samples | 306299498 | `d96ecf3bdd48228706f8601dee15d709e6ecf3384e8a00a2020d6b8119b34457` |

The `st-long2` record needs uint32, because one read interval reached
88.4 ms. The packet carries it gzip-compressed.

| Tool | Role | SHA-256 |
|---|---|---|
| `selftest_b21.py` | the self-test: lane B5's reader and capture command, the sampler, snapshots | `a2d4c087458e07bcaf9648171b01823b169b07eec7556ae3f01d49d51ce1808f` |
| `host_sampler_b21.py` | the 20 Hz host sampler, as run for `st-long2` | `fac96057c6205ce8a0cb00ded62c482925033ca4245e3de4232d398e1204d6b6` |
| `host_sampler_b21_st-long_asrun.py` | the sampler as run for `st-long`, without the pressure counters | `371903a0e0332afaf0694e4e06696964bfa7430607c99dccb8b79c979f65f1f8` |
| `b21_selftest_ana.py` | the read record, stalls, floor steps, interrupt and pressure classes | `6e95b6b99f63597a182110d6a8343d4bc937d5cc44dc6390a4e4e7b0963b0b98` |
| `b5_attrib.py` | lane B5's definitions, imported unchanged | `f1d9b2ba456672cdf00ed86a645b9ab35c4d11fef3bb5ac9363c70885a5dfa40` |
| `b5_round3.py` | carried from the evidence archive at `9006c78e`; not run, because it grades content | `415ef1b0e7d26cb821235fe22c81b23a42035afb73b4baef3cf24bd08099ac4d` |
| `run_a.py` | lane B5's run tool, whose reader `selftest_b21.py` copies | `dcc616aea7842b8b1a574d2e9ba2647e71f344d95ee4473ae2c369802e686ad6` |
