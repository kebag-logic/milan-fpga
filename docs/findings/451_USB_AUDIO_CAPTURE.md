<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Capture through the USB Audio device on the ec0cc0c1 image

Refs #451. Operator [A453], measured 2026-09-30, under the
[bench lane B3 assignment](https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5903384996).

[TDM8 first light](451_TDM8_FIRST_LIGHT.md) decoded both directions at the
SoC board's McASP0, without its USB function. This page records the
checklist's capture through the USB Audio device. The DUT's rendered pattern
crosses the SoC board's audio bridge and is recorded on the bench host's USB
Audio card.

| #451 item | Verdict | Evidence |
|---|---|---|
| Capture through the USB Audio device: slot and channel order | FAIL | Two 75 s captures: 0 of 3,600,000 frames pass the pattern rule in either. The eight tags arrive as a cyclic rotation of the slot order, and the rotation changes 2,833 and 238 times. The slot order holds in 9.6% and 11.9% of frames. See [Per-run results](#per-run-results). |
| Capture through the USB Audio device: continuity | FAIL | 327,339 silent frames in 2,420 stretches, and 3,244 in 4. Of 4,588 and 500 joins across a class change, 5 each continue the ordinal. |
| Capture stall after one period, or the card disappearing | Not observed | Both captures ran their full 75 s, and the card stayed present. No STOP condition occurred. |
| Identifiable samples through the USB Audio device, playback direction | NOT RUN | Not part of this assignment. |
| Continuity check: J11 pins 1, 37 and 38 to ground, pin-1 end | NOT RUN | It needs a meter on the unpowered boards. See [Continuity check](#continuity-check). |
| Scope measurements; calibrated items (#386 acceptance 4, #117) | NOT RUN, owner items | Instrument work, outside this lane. |
| Reference: the direct McASP0 path on the same image | PASS | Both directions bit-exact and in order, 0 torn frames: [DIN frame coherence](617_DIN_FRAME_COHERENCE_BENCH.md). |

These are operator measurements, not review verdicts.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, the bridge as found and the capture point.
- **[Method](#method)** -- How the pattern reached the USB Audio card, and how it was graded.
- **[Per-run results](#per-run-results)** -- Both captures, graded against the first-light pattern.
- **[What the USB Audio card receives](#what-the-usb-audio-card-receives)** -- Interpolated words, a rotating channel order and silent stretches.
- **[Continuity check](#continuity-check)** -- Why it cannot run in this lane, and what the signal data does show.
- **[Restore](#restore)** -- The bridge and the stream state as left.
- **[Limits](#limits)** -- What these captures do not show.
- **[Artifact hashes](#artifact-hashes)** -- Raw capture and tool identities.

## Identity and setup

The DUT runs dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`. Its identity
gate passed: VERSION `0x00020060`, AEM CRC32 `93742dd2`, entity
`020000fffe000001`. The [#617 page](617_DIN_FRAME_COHERENCE_BENCH.md#identity-and-setup)
holds the full readback. The DUT selected clock source 0, INTERNAL, at 48 kHz.

The SoC board is the PocketBeagle 2 of the
[amendment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5729936674),
on the boot the first-light page describes. Its USB function presents an
eight-channel, 32-bit, 48 kHz audio device and a network link to the bench
host.

The bridge has two legs, one copy process per direction. The to-host leg
copies McASP0 receive, the DUT's DOUT, to the USB Audio function. The
from-host leg copies the other way. Both run with sample-rate-converting
synchronisation, `-S samplerate`. As found, both legs were running and the USB
function was configured. With no reader on the bench host, the to-host leg
restarted its McASP0 capture about 6.2 times per second.

The two #617 runs stopped the legs by PID and restarted them with the bridge
script's own command lines. These captures ran on the restarted legs, 34 s and
7.2 min after the restart.

## Method

Every bench action held the shared lock. Every command ran in the foreground
with an explicit deadline. No flash, power, wiring, instrument or USB function
action occurred, and nothing on the SoC board was started, stopped or changed
in these two actions.

**DUT side.** The first-light DOUT method, unchanged: a software AAF talker on
the controller host, DUT STREAM_INPUT 0 bound to it, and eight identity
mappings from stream channel `c` to cluster `c`. The rendered pattern leaves
the DUT on DOUT, TDM slot `c` carrying tag `c + 1`.

**Capture point.** The bench host recorded the USB Audio card's capture
endpoint for 75 s: eight channels, 32-bit little-endian, 48 kHz, 6,000-frame
periods. The SoC console took read-only bridge status before and after each
capture. The mappings were removed and the stream unbound afterwards.

**Grading.** The strict rule is the first-light decoder's. Each word carries
tag `t` in bits 31:24 and a 16-bit frame ordinal in bits 23:8, with a zero low
byte. Channel `c` carries tag `c + 1`, and all eight carry one ordinal.

A second decoder explains the failures. It reads bits 31:8 as the recipe's
24-bit sample and reports the low byte separately. It classifies each frame
by its tags:

- **in order**: channel `c` carries tag `c + 1`;
- **rotated by `k` words**: channel `c` carries tag `((c + k) mod 8) + 1`;
- **other**: a zero word, a tag outside 1 to 8, or tags that are not a
  rotation;
- **silent**: all eight words zero.

Runs of one class are segments. Inside each, the step between frame ordinals
is graded; a rotated frame's wrapped channels belong to the next frame.

## Per-run results

<!-- usb-runs -->
| Run | Capture | Frames | Pass the pattern rule | Silent frames (stretches) | Slot order kept | Rotated by 1 to 7 words | Other | Rotation changes | Longest run in one rotation | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| `usb-long` | 75.116 s, rc 0 | 3,600,000 | 0 | 327,339 (2,420) | 344,438 (9.6%) | 2,919,511 | 8,712 | 2,833 | 2,922 frames | FAIL |
| `usb-long2` | 75.108 s, rc 0 | 3,600,000 | 0 | 3,244 (4) | 428,820 (11.9%) | 3,166,358 | 1,578 | 238 | 95,998 frames | FAIL |

A rotation run spans consecutive frames in one rotation. It bridges "other"
and silent frames inside it, which the pattern's ordinal wrap produces every
65,536 frames (next section).

<!-- usb-detail -->
| Run | Words with a non-zero low byte | Frames spread one ordinal or more | Steps inside one rotation: +1, repeat, skip, other | Joins across a class change | Joins that continue the ordinal |
|---|---|---|---|---|---|
| `usb-long` | 25,484,975 of 26,163,422 (97.4%) | 636,231 | 3,248,176, 2,825, 601, 7,758 | 4,588 | 5 |
| `usb-long2` | 28,102,227 of 28,773,277 (97.7%) | 188,754 | 3,589,776, 3,269, 743, 889 | 500 | 5 |

Per channel, the slot order is the same statement eight times. USB Audio
channel `c` carries its own tag `c + 1` only in the in-order frames, 9.6% and
11.9%. In the other frames it carries tag `((c + k) mod 8) + 1` of the frame's
rotation `k`. Every rotation from 1 to 7 occurs in both runs.

| Rotation `k`, frames | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| `usb-long` | 344,438 | 261,347 | 263,025 | 989,413 | 349,663 | 348,215 | 348,547 | 359,301 |
| `usb-long2` | 428,820 | 445,811 | 479,780 | 479,809 | 465,939 | 432,171 | 431,325 | 431,523 |

| Run | Bridge side during the capture | DUT side, bound |
|---|---|---|
| `usb-long` | McASP0 receive 250.0 periods/s; 5 capture restarts; USB function configured; fault scan 0 | 0 sequence mismatches, 0 depacketizer drops, media locked; render rails 135 to 349 |
| `usb-long2` | McASP0 receive 250.0 periods/s; 5 capture restarts; USB function configured; fault scan 0 | 0 sequence mismatches, 0 depacketizer drops, media locked; render rails 456 to 692 |

The McASP0 receive rate is the count of the receive DMA's 192-frame periods
between the bridge status reads before and after each capture. The interval
runs between the same uptime read of the two logs, so the bracket is
consistent: 18,942 and 18,957 periods in about 75.8 s (75.78 s and 75.83 s).
That is 250.0 periods/s, or 47,992 and 47,999 frames/s: the nominal rate.

In `usb-long`, 1,315 of the 2,833 rotation changes follow a silent stretch.
In `usb-long2`, 4 of 238 do.

## What the USB Audio card receives

**Interpolated words.** The words are not copies of the pattern. The first
non-silent frame of `usb-long`, frame 1,632, carries the right tags in order.
Its low bytes rise with the tag, from `0x20` at tag 1 to `0xc0` at tag 8. That
fits a gain slightly above one, with the excess below one 24-bit LSB. Over
both runs the low bytes cover the whole range: most words lie between two
pattern words, as a sample-rate converter's output does. The resulting
spread is under one ordinal in most frames, and one or more in 636,231 and
188,754 frames. The pattern's ordinal wraps from `0xffff` to 0 every 65,536
frames. The converter smears that step over a few frames, which read as
"other".

**A rotating channel order.** Inside a rotation the ordinal steps by one per
frame almost everywhere. The channel order moves by whole 32-bit words, not
whole frames. So the frame boundary is lost somewhere the stream is handled at
a finer grain than one eight-channel frame.

**Silent stretches.** `usb-long` opens with 1,632 silent frames and holds
2,420 silent stretches, the longest 2,459 frames (51 ms). `usb-long2` holds 4,
the longest 2,441 frames.

**Where it arises.** The same DUT output recorded directly at McASP0 is
bit-exact and in order: the
[#617 page's DOUT run](617_DIN_FRAME_COHERENCE_BENCH.md#dout-run). During both
captures McASP0 received at the full rate, and the DUT listener counted no
error. The loss therefore arises between McASP0 receive and the bench host's
capture buffer. It lies in the bridge leg, the USB Audio function or the bench
host's USB path. This lane changes nothing on the SoC board, so it does not
locate it further.

## Continuity check

The #451 recipe asks for a continuity check of AX7101 J11 pins 1, 37 and 38
to ground, with the pin-1 end confirmed against the silkscreen. The amendment
adds per-wire readings on the unpowered boards: about 33 ohm per signal wire,
and every signal open to every other and to ground.

It is NOT RUN. It needs a meter at both headers with both boards unpowered.
This lane may not power down either board or change any instrument or wiring.

What this lane's signal data shows instead: BCLK, FSYNC, DOUT and DIN carry
bit-exact data in both directions, in slot order. The conductors join the
right signal pins; the ground pins and wire resistances are not measured. The
[owner report](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5872564358)
of an end-to-end wiring check remains the recorded wiring evidence.

## Restore

| State | As left |
|---|---|
| SoC audio bridge | Both legs running with the bridge script's command lines, under new process IDs; status, PCM states and fault scan as at the start |
| SoC board | Same boot; USB function configured; no task file left |
| USB Audio card on the bench host | Present and closed; no task process |
| DUT stream state | STREAM_INPUT 0 unbound; STREAM_PORT_INPUT 0 map read back empty after each capture |

The [#617 page](617_DIN_FRAME_COHERENCE_BENCH.md#restore) records the lane's
full restore and its residuals.

## Limits

- Only the capture direction through the USB Audio device ran. The playback
  direction and a capture with the bridge's rate conversion disabled were not
  assigned; the bridge was not changed.
- Two captures, at INTERNAL only, both on one restart of the bridge legs.
- The capture shows what reaches the bench host's buffer. It cannot tell the
  bridge leg, the USB Audio function and the bench host's USB path apart.

## Artifact hashes

The raw files stay outside the tree and the lane packet. Each is identified by
size and SHA-256.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| USB Audio capture, `usb-long` | 115200000 | `7995b44a5f6529a54092eaa5b94e0e85b701cf85bab0d4bbd55a853bf9ccd7ca` |
| USB Audio capture, `usb-long2` | 115200000 | `fa79d7055a4a0fb4e696787e49130428ed31c50012dfd9b9494b5dbe0b5e6178` |

The lane packet holds the tools, the per-action evidence and the raw-artifact
index. Its redacted copy is `review-evidence/b3-r1/author/` on branch
`b3-review-evidence`, where `RAW-ARTIFACTS.json` indexes every raw file by size
and SHA-256. Its grading tools:

| Tool | SHA-256 |
|---|---|
| `grade_usb.py` (strict rule, rotation classes, segments) | `505e506aa98f3ba1ff2aed274befa56f775b31ec9a195b464abaa63b3f4f176c` |
| `decode_capture.py` (first light, unchanged) | `cfb7121b589fe231e139012646fe567b76022e694e08d3bb89d8a7481bda2568` |
