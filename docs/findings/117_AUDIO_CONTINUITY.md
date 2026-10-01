<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Audio continuity against the reference peer on the ec0cc0c1 image

Refs #117. Operator [A472], measured 2026-10-01, under the
[bench lane B5 assignment](https://github.com/kebag-logic/milan-fpga/issues/117#issuecomment-5925737609).

This page measures the audio continuity row of #117 acceptance box 4, end to
end. The [first-light pattern](451_TDM8_FIRST_LIGHT.md#method) enters the
DUT's TDM input from the SoC board's McASP0. The DUT's AAF talker carries it to
the reference peer's listener. An external, hardware-clocked audio capture
records the peer's digital output.

| Item | Verdict | Evidence |
|---|---|---|
| Identity gate | PASS | Every readback equals lanes B3 and B4. See [Identity and setup](#identity-and-setup). |
| Integrity: stream channels 0 and 1 bit-exact at the captured 24 bits, in order | PASS | 31,569,594 of the window's 31,569,600 frames are pattern frames, 0 torn and 0 invalid. The other six are single zero frames. See [Integrity](#integrity). |
| Continuity over 660 s: silent stretches, repeats and skips | FAIL | 334 repeats at the DUT's documented INTERNAL beat. At the peer's output, 520 one-frame drops, one every 1.266 s, six of them with a single zero frame. The capture path lost 117,104 more frames. See [Continuity](#continuity). |
| Restarts: 30 unbind and rebind cycles, rebind to the first valid sample | PASS, 30 of 30 under 1 s | Median 0.0279 s, maximum 0.1358 s; no growth. See [Restarts](#restarts). |
| Direction B, the peer's talker to the DUT's listener | NOT RUN | No known signal reaches the peer's talker channels without an instrument or wiring change. See [Direction B](#direction-b). |
| #117 audio continuity row | FAIL as measured | The peer's output drops one frame every 1.266 s. The capture path also loses frames, so a clean window was not recorded. |

These are operator measurements, not review verdicts.

This page reads the row as follows. Over at least 10 minutes every frame is
bit-exact and in order. No frame is missing, repeated or silent. The one
exception is the INTERNAL beat that
[TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff) documents: one
whole-frame repeat every 1.958 s. The restart bound is #75's 1 s.

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
- **[Artifact hashes](#artifact-hashes)** -- Raw capture and tool identities.

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

- All 4 DUT and 14 reference-peer stream states were unbound.
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
whole-frame repeat, and `d` greater than 1 a skip of `d - 1` frames.

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

Across the whole run, 39,356,186 frames, every non-zero word of channel 0
carries tag 1 and every one of channel 1 tag 2, with no torn frame. The
3,407,496 zero frames are the silence before the first bind, in the holds and
after the last unbind.

## Continuity

<!-- continuity -->
| Class | Events | Frames | Per second |
|---|---|---|---|
| Whole-frame repeat | 334 | 334 | 0.508 |
| One-frame skip | 526 | 526 | 0.800 |
| Skip of 2 to 59 frames | 521 | 7,176 | 0.792 |
| Skip of 60 frames or more | 239 | 109,928 | 0.363 |
| Silent stretch, one frame each | 6 | 6 | - |

The window holds 657.7 s of captured audio in 660.15 s, because the capture
path lost 2.4 s. The classes separate by cause.

**Repeats: the DUT's INTERNAL beat.** Counted in content frames, the repeats
fall 93,989 to 93,992 frames apart. That is the 1.958 s beat, one whole-frame
repeat per crossing ([TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff)).
`SLIP_TDM` rose 327 between the window's first and last console reads,
640.47 s apart: 0.511 per second. Four spacings are two beats, where capture
losses hid a repeat: 338 beats in 660.15 s, 0.512 per second.

**Skips of two frames or more: the capture path.** These are frames the
bench host's USB path never delivered.

- 236 of the 239 skips of 60 frames or more line up with a capture stall.
  The read interval stretches beyond its 10 ms period by the lost duration:
  for example 10.51 ms for 10.62 ms lost, and 16.28 ms for 16.88 ms. The
  stalls recur about every 2.99 s. The other three, 72 to 108 frames, fall
  in read intervals stretched by 1.8 to 2.1 ms.
- The stalls' excess sums to 109,069 frames, against 109,928 in those skips.
- The captured frame count fell behind the bench host's clock by 115,614
  frames over the window. That also covers most of the 7,176 frames in the
  smaller skips.
- The DUT's talker sent 8,000 packets a second throughout, by `AAF_FRAMES`.
  The peer's listener counted no sequence mismatch, late or early timestamp.
- Each lost USB microframe holds six frames at 48 kHz. That is also the AAF
  packet size, so frame counts alone cannot separate the two.
- A 125 ms capture period lost frames at the same rate (`cap-test1`).

**One-frame skips: the peer's output rate.** A capture loss cannot drop one
frame, because each USB microframe carries about six. The 526 one-frame skips
form 520 slip events, each of which removes one frame.

- 514 events are a single one-frame skip.
- Six take the form skip, zero frame, skip, six frames apart. They are the six
  silent stretches. No other zero frame occurs in the window.
- Consecutive events fall 60,546 to 60,923 content frames apart, median
  60,768, or 1.266 s. One spacing is two periods, where a capture loss hid an
  event.
- That is a constant rate difference of 16.4 ppm between the stream and the
  peer's output.
- On the bench host's clock, uncalibrated, the stream carries its samples at
  0.8 ppm below 48 kHz, and the peer's output runs 17.3 ppm below. The window's
  end times bound both to about 2 ppm.
- The peer's media clock source is its INTERNAL source, not the stream. So it
  drops one frame each time the stream runs one frame ahead of its output.

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

The interval uses ordinary least squares and Student's t. It assumes
independent errors with constant variance.

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

NOT RUN. The reference peer's talker channels carry its own physical inputs:
its STREAM_PORT_OUTPUT 0 map takes them from its input clusters. No known
signal drives those inputs. Driving one would need an instrument output or a
wiring change, and this lane allows neither. The external capture was used as
a capture point only.

The DUT's STREAM_INPUT 0 lists `0205022002006000` and `0215022002006000`. It
could therefore take the peer's four-channel talker format under the binding
rule.

## Restore

| State | As left |
|---|---|
| Stream states, DUT and reference peer | All 18 unbound; the end census equals the start in 45 of 46 entries, the other being the DUT's live propagation delay |
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

- The capture path lost 0.37% of the frames. A discontinuity inside a lost
  stretch cannot be seen: four beat repeats and one slip event were hidden
  that way.
- The attribution of the one-frame skips to the peer's output rate rests on
  their period and on the bench host's uncalibrated clock. A run with the
  peer's media clock following the stream would test it. That needs a clock
  source change on the peer, outside this lane.
- One run, at the DUT's and the peer's INTERNAL clock sources only.
- Only stream channels 0 and 1 are observed.
- The restart is timed to the sample's arrival on the bench host, not to the
  peer's output.
- Printed precision is not calibrated accuracy.

## Artifact hashes

The lane packet `b5-a472` holds the tools, per-action evidence, summaries and
the raw-artifact index. Raw files stay outside the tree and the packet, each
identified by size and SHA-256.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `a-long` graded pair, 24-bit | 236137116 | `2ac666fb5ff6284cc665887758ad6f2754918e5b7932258a06ea7efeeec99bdf` |
| `a-long` read times | 1967832 | `717141923d15fc32f09e998d3af779b9e95d8a263091c039e7165bc3c7728262` |
| `a-long` every channel, 10 s | 28800000 | `f334406790ef4e769d3b682ff56506568467277b9224acf82e168ab8af838d89` |
| `a-long` full grade | 180433 | `e06fa4602138c30b84f19f7ba78db88b4e394d07bedc8939474dafa2ac07ed88` |
| `diag1` every channel, 25 s | 72116580 | `b8cc1f50fc54ba4bf5bb803056af6ab229e574798bb337249400879098f341be` |
| `cap-test1` graded pair | 14472180 | `c8d34f62402a0af3a1c20b47325a9c859975cea88426a4a3029dabbddd422616` |
| `a-try1` watched pair | 11474046 | `e23aaf2e9f82fbfdb0d89a72ebeb782ae036692af73eec32c6c8c2aa7c5805dc` |
| Capture as found, every channel, 3 s | 8640000 | `7eabb3761ba13566ceb3e826d66a742cd865f23f7ca5eebce23af50ea4bf465f` |
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

`a-long` ran the `run_a.py` revision before the capture-period option, whose
default is the value it used. `cap-test1` ran the listed revision.
