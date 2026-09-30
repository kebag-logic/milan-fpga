<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# DIN frame coherence on the ec0cc0c1 image

Refs #617. Operator [A453], measured 2026-09-30, under the
[bench lane B3 assignment](https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5903384996).

The image carries the frame-atomic capture handoff of
[PR #618](https://github.com/kebag-logic/milan-fpga/pull/618). This page
re-runs the #451 first-light DIN capture on it, with the
[first-light method](451_TDM8_FIRST_LIGHT.md#method), wiring and pattern.

| #617 acceptance | Verdict | Evidence |
|---|---|---|
| 4. A bench re-run of the #451 DIN capture shows 0 torn frames | PASS | 0 torn of 3,360,036 playback frames, and 0 in the whole 4,551,624-frame recording. First light counted 2,267,868 of 3,360,035 (67.5%). See [DIN run](#din-run). |
| DIN slot and channel order, re-verified | PASS, identity | Stream channel `c` carries tag `c + 1` from TDM slot `c` in every playback frame. |
| DOUT slot and channel order, re-verified | PASS, identity | SoC capture channel `c` carries tag `c + 1` in every one of 3,360,000 frames. |
| Render path unchanged (DOUT) | PASS | 0 torn and 0 invalid words, with the first-light discontinuity classes. See [DOUT run](#dout-run). |
| 1 to 3 | Not bench items | Simulation, resources and the render path's RTL, in PR #618. |

These are operator measurements, not review verdicts.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, its identity readback and the bench as found.
- **[Method](#method)** -- The first-light method as re-run, and the torn-frame rule.
- **[DIN run](#din-run)** -- Torn frames, pair offsets, per-channel continuity and the slip counter.
- **[DOUT run](#dout-run)** -- The render direction re-run, graded as at first light.
- **[Comparison with first light](#comparison-with-first-light)** -- The same measurements on the 9e9954e9 image beside these.
- **[Restore](#restore)** -- The bench as left, and the residuals.
- **[Limits](#limits)** -- What this run does not show.
- **[Artifact hashes](#artifact-hashes)** -- Raw capture and tool identities.

## Identity and setup

The image is dev `ec0cc0c1df7d7ab3e25d973958f53f0074393d2c`: dev
`13eda870` plus PRs #616, #619, #618, #620 and #622. Only PR #618 changes
RTL: `KL_chan_map_capture.sv`, `KL_media_grid_align.sv`, `KL_media_nco.sv`
and `milan_datapath.sv`. PR #619 changes builder and tooling scripts, and the
others change documentation. The lane base is the same commit.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Live ENTITY and CONFIGURATION | Byte-equal to the AEM bytes the console dumps from QSPI, `0x110` (312 bytes) and `0x248` (106 bytes); entity `020000fffe000001` |
| NVM | Slot B seq 230 authoritative, `backed=1` |
| UART grader | 10 of 10 |
| ROM CRC32, 53,344 bytes | `acad92b9`, as on `13eda870` |
| QSPI payload CRC32, 3,825,788 bytes | `d178f19a`; `13eda870` read `d84bce7b` |
| Identity gate | PASS |

This is CRC consistency and descriptor identity, not a configuration SHA-256
readback. The build's bitstream was not on the bench host, so the payload CRC
is recorded as read.

As found, all 18 queried stream states were unbound and both DUT audio maps
were empty. The DUT selected clock source 0, INTERNAL, at 48 kHz. `SLIP_TDM`
read 333 duplicates and 0 skips.

The SoC board was on the boot the first-light page describes, with both
audio bridge legs running. Its McASP0 receive DMA completed 1,252 periods of
192 frames in 5.02 s, so bit clock and frame sync arrive.

## Method

Every bench action held the shared lock. Every command ran in the foreground
with an explicit deadline. No flash, power, wiring, instrument or USB function
action occurred.

The two SoC bridge legs were stopped by PID, after checking each command line
against the bridge script's `status`. They were restarted after the two runs
with the script's own command lines.

The pattern is first light's. For tag `t` (1 to 8) and frame ordinal `n`,
bits 31:8 of each word carry `(t << 16) | (n & 0xffff)`. Bits 7:0 are zero.
Channel `c` carries tag `c + 1`.

**DIN.** The SoC board built one 65,536-frame period of the pattern. Its
SHA-256 is first light's. The board played it into McASP0 in a loop for 70 s.
Eight identity mappings on STREAM_PORT_OUTPUT 0 routed cluster `c` to stream
channel `c`. The generated shape puts clusters 0 to 7 on TDM input slots 0
to 7.

A software listener on the controller host probed STREAM_OUTPUT 0 until it
answered SUCCESS. It declared an MSRP Listener Ready and recorded every frame
from the DUT for 95 s. A slave-only gPTP daemon ran on the controller port for
the action. The mappings were removed afterwards and read back empty.

**DOUT.** A software AAF talker on the controller host sent eight-channel
INT32 48 kHz AAF, unicast, six frames per PDU. It was paced on the
gPTP-disciplined NIC clock, with timestamps 2 ms ahead. DUT STREAM_INPUT 0
was bound to it, and eight identity mappings put stream channel `c` on
cluster `c`. The SoC board recorded McASP0 directly for 70 s, and the file
was copied over the USB network link with its SHA-256 checked.

**Torn frame.** #617 defines a torn AAF frame as one carrying samples from two
TDM frames. Under the pattern that is a frame whose valid words carry more than
one ordinal. The count covers every frame of the recording.

## DIN run

<!-- din-run -->
| Run | Recording | AVTP PDUs | Sequence gaps | Playback region | Torn frames, region | Torn frames, whole recording | Invalid words, region | Result |
|---|---|---|---|---|---|---|---|---|
| `din-long` | 4,551,624 frames | 758,604 | 0 | 3,360,036 frames, 70.001 s | 0 | 0 | 0 | PASS |

The playback region runs from the first to the last frame in which all eight
channels carry their own tag. Inside it every word is valid.

| Ordinal offset of pairs 1, 2, 3 against pair 0 | Frames | Share |
|---|---|---|
| 0, 0, 0 | 3,360,036 | 100% |
| any other | 0 | 0% |

The left and right channels of each pair never disagree. No pair carries
another frame's ordinal.

<!-- din-channels -->
| Stream channel | Pattern tag | TDM slot | Valid words | +1 steps | Repeats | Skips | Other steps | Result |
|---|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 1 | 2 | 1 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 2 | 3 | 2 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 3 | 4 | 3 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 4 | 5 | 4 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 5 | 6 | 5 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 6 | 7 | 6 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |
| 7 | 8 | 7 | 3,360,036 | 3,359,999 | 36 | 0 | 0 | In order |

All eight channels repeat at the same 36 frames. Each is one whole-frame
repeat, 93,990 to 93,993 frames apart: the 1.958 s INTERNAL beat. That is the
[TIME_SYNC.md](../design/TIME_SYNC.md#talker-capture-handoff) law: one
whole-frame slip per beat, counted once on `SLIP_TDM`.

| `SLIP_TDM` read | Duplicates | Skips |
|---|---|---|
| Before the listener | 383 | 0 |
| Talker streaming, before playback | 391 | 0 |
| After playback | 427 | 0 |
| After the action | 440 | 0 |

Across the 70 s of playback the counter rose by 36, the repeats in the stream.

Outside the region the recording holds 1,191,588 frames:

- **Before playback and after the stop tail**, every word reads `0xffffff00`.
- **Frame 45,587**, just before the region, reads `ffffff00`, `fffff000`, then
  six zero words.
- **After the region**, 777 frames carry zero words: 776 all zero, then one
  with three zero words and five `ffffff00`. The first is all zero, not torn.

## DOUT run

<!-- dout-run -->
| Run | Frames | Torn | Invalid words | Zero words | Slot order | Beat clusters | Underrun clusters | Result |
|---|---|---|---|---|---|---|---|---|
| `dout-long` | 3,360,000 (70 s) | 0 | 0 | 0 | Identity | 36: 696 repeated, 732 dropped | 23: 12 after logged talker lateness, 11 without | PASS |

<!-- dout-channels -->
| SoC capture channel | Mapped stream channel | TDM slot | Recovered tag | Valid words | Result |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 3,360,000 | In order |
| 1 | 1 | 1 | 2 | 3,360,000 | In order |
| 2 | 2 | 2 | 3 | 3,360,000 | In order |
| 3 | 3 | 3 | 4 | 3,360,000 | In order |
| 4 | 4 | 4 | 5 | 3,360,000 | In order |
| 5 | 5 | 5 | 6 | 3,360,000 | In order |
| 6 | 6 | 6 | 7 | 3,360,000 | In order |
| 7 | 7 | 7 | 8 | 3,360,000 | In order |

Every discontinuity is a whole-frame repeat or drop; no frame is torn.
Discontinuities closer than 50 ms were grouped into clusters.

- **Beat clusters** repeat and drop whole frames and net one drop each. They
  are spaced 93,989 to 93,992 frames.
- **Underrun clusters** repeat frames and then jump forward. Twelve follow a
  talker PDU sent 150 us or more late within 60 ms. The alignment multiple 7
  is the only one under which any underrun lines up with a late PDU; 5, 6, 8
  and 9 give none.

With the stream bound, the DUT listener counted 0 sequence mismatches, 0
unsupported formats, 0 uncertain timestamps and 0 depacketizer drops. Media
stayed locked. The presentation offset read 1.98 ms, and the render stage's
rail count rose from 4 to 134.

## Comparison with first light

The first-light figures are from the
[first-light page](451_TDM8_FIRST_LIGHT.md#din-frame-coherence), image source
`9e9954e9`.

| Measurement | First light, `9e9954e9` | This run, `ec0cc0c1` |
|---|---|---|
| DIN playback frames | 3,360,035 | 3,360,036 |
| DIN torn frames | 2,267,868 (67.5%) | 0 |
| DIN pair offsets 0, 0, 0 | 1,092,167 (32.5%) | 3,360,036 (100%) |
| DIN pair offsets 0, 0, -1 / 0, -1, -1 / -1, -1, -1 | 761,510 / 761,459 / 744,899 | 0 / 0 / 0 |
| DIN repeats and skips per channel | 711 to 736 repeats and 676 to 700 skips, each pair at its own point | 36 repeats and 0 skips, all channels at the same frames |
| DIN beat spacing | 93,990 to 93,993 frames | 93,990 to 93,993 frames |
| DIN first stop-tail frame | Torn: pair 0 zero, pairs 1 to 3 at the last ordinal | All zero |
| DOUT frames, torn, invalid | 3,357,952, 0, 0 | 3,360,000, 0, 0 |
| DOUT beat clusters clear of underruns | 34 | 36 |
| DOUT presentation offset | 1.98 ms | 1.98 ms |

The render direction behaves as at first light. The DIN direction no longer
mixes adjacent TDM frames.

## Restore

| State | As left |
|---|---|
| Stream states, DUT and reference peer | All 18 unbound; the census after the lane equals the start in 33 of 33 entries |
| DUT audio maps | Both empty |
| DUT clock source and control words | Clock source 0 at 48 kHz; every control word read equals the start |
| DUT synchronization | SYNC=1, ASCAPABLE=1, TU=0, grandmaster unchanged |
| SoC audio bridge | Both legs running with the script's command lines; status, PCM states and the fault scan as at the start |
| SoC board | Same boot; USB function configured; no task file left |
| Controller host | No gPTP daemon or task process; NIC clock frequency reads back as found, back on its recorded trajectory within 4.4 us; timestamping as found; staging removed |

Residuals that no permitted command restores:

- The map and bind edits of the method made the DUT persist its saved state.
  NVM commits went from 0 to 6, the slots from seq 229/230 to 235/236, and
  `pend=1` is left set, as is `PP_STAT` bit 11. The live maps and bindings
  equal the start. First light left the same bit set.
- The bridge legs run under new process IDs.

## Limits

- One run per direction, at INTERNAL only. The CRF lock of #617's simulation
  was not exercised on the bench.
- The pattern shows which TDM frame each sample came from. It does not time
  the samples against the wire.
- The DOUT decode detects torn or rotated frames at the SoC pins. Render
  latency is not measured here.

## Artifact hashes

The raw files stay outside the tree and the lane packet. Each is identified by
size and SHA-256.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| DIN talker stream recording, `din-long` | 189654306 | `5f6de7fbe648776c3e0b9d024a8e60d90d05d1c9b96c555573b96e58fedcd4d1` |
| DIN pattern period, built on the SoC board | 2097152 | `b6a92e9724e945354c3f8fc5178cec7bb8fd0e62d52bd9ee7f13ed5347bfa97c` |
| DOUT 70 s SoC capture, `dout-long` | 107520000 | `bfee26618674d17f5eacfb18c36a0860cac37dfcd4bba0a04b84684b6625b040` |

The lane packet `b3-a453` holds the tools, the per-action evidence and the
raw-artifact index. Its grading tools:

| Tool | SHA-256 |
|---|---|
| `grade_617.py` (torn-frame count and pair offsets) | `9e4551453f7ecfbe5dab19f17053556834a4fbf7cd269a2aa03677a37576cea7` |
| `decode_din_pairs.py` (first light, unchanged) | `feaf05c845409e035a8d53cf6bf344374feb85df9cc65863de411f9cd2a3beb9` |
| `decode_capture.py` (first light, unchanged) | `cfb7121b589fe231e139012646fe567b76022e694e08d3bb89d8a7481bda2568` |
| `attribute_dout.py` (first light, unchanged) | `d3d05bb78f2396497167b1aa8c40d552b9afe08750cd240f468cc0a4592ff502` |
