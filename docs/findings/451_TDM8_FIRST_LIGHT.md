# TDM8 first light, 2026-09-28

[A403] REVIEW READY. Refs #451.

Both directions of the TDM8 link carry identifiable audio in all eight slots,
in order, over at least 60 s each.

- **DOUT.** Every slot word the SoC received over a 70 s capture decodes to
  the expected channel, with no torn frame. A 3 s capture in the second
  session showed no regression.
- **DIN.** Over 70 s of SoC playback, every word of the DUT's talker stream
  decodes to the expected channel. This needed the talker's output map, which
  the first session left empty.

One DUT property is recorded for triage, not as a link fault: the talker can
assemble one AAF frame from two adjacent TDM frames, split between channel
pairs. See [DIN frame coherence](#din-frame-coherence).

The first session stopped with DIN all zero and called it a wiring question.
That inference was wrong; [Between the two sessions](#between-the-two-sessions)
gives the cause. This page replaces the record of the 2026-09-27 attempt,
which remains in Git history at `fba793c0885d091802c96313d5df3234900dce0d`.
Bench state was restored; the residuals are listed under
[Restoration](#restoration).

## Contents

- **[Scope and identity](#scope-and-identity)** -- Pin the assignment, the tested image and the live SoC board configuration.
- **[What changed since the attempt](#what-changed-since-the-attempt)** -- The repaired SoC board and the transport corrections that made both directions observable.
- **[Between the two sessions](#between-the-two-sessions)** -- Why the first session's DIN result was all zero, and what the second session changed.
- **[Method](#method)** -- How each direction was driven and recovered, and what each observation can and cannot show.
- **[Direction decode](#direction-decode)** -- Per-channel slot and channel order for both directions.
- **[DIN frame coherence](#din-frame-coherence)** -- How the talker mixes adjacent TDM frames across channel pairs, and why it is a DUT property.
- **[Continuity and rate](#continuity-and-rate)** -- The 70 s windows, every discontinuity classified, and the frame-rate offset.
- **[Restoration](#restoration)** -- Restored state, the residuals, and the operator errors.
- **[Owner items](#owner-items)** -- What stays NOT RUN and what needs the owner.
- **[Artifacts and validation](#artifacts-and-validation)** -- Raw artifact hashes and the local gates.

## Scope and identity

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5859278962)
limits the run to software-side first light. The
[amendment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5729936674)
defines the four-wire synchronous SoC board variant, and the
[owner's note](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5862732214)
restarts first light under the same rules.

The lane base is `6d5ebd7357c1e468e446f18a61527c5be6118a04`. The image source
is `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`; the required FSYNC fix,
`9c423e2c`, precedes it.

| Identity observation | Result |
|---|---|
| VERSION | `00020060` |
| ROM CRC32, 52,216 bytes | `9b6576a9` |
| QSPI payload CRC32, 3,825,788 bytes | `3c18c276` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| ENTITY and CONFIGURATION replies | Byte-identical to previously verified payloads |
| Identity gate | PASS |

This is CRC consistency and descriptor identity, not a configuration SHA-256
readback. The second session ran on the same DUT boot. Its `SLIP_TDM` counter
continued from the first session's last value at the expected rate, and
`VERSION`, `PP_STAT` and every control word read unchanged.

| Dependency | Image pin |
|---|---|
| Protocol processor | `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` |
| gPTP processor | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` |
| AXIS library | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |
| External dependency | `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` |

The SoC board's live McASP0 configuration was read before any audio. McASP0 runs
`dsp_a` with the codec side as bit-clock and frame master, so McASP0 is the
slave. It carries eight 32-bit slots; serializer 0 transmits and serializer 1
receives. The DUT pins are the `tdm` resource in the
[platform file](../../sw/litex/platforms/alinx_ax7101.py).

The DUT shape is the one-AAF-stream TDM8 end station
([generated shape](../../configs/generated/endstation_ax7101_1x1_tdm8/gen/adp_shape_defaults.svh)):
one AAF and one CRF stream in each direction.

## What changed since the attempt

1. The owner repaired the SoC board on 2026-09-28. Its software image now
   carries a k3-udma DMA fix for BCDMA cyclic receive: end of packet is restored on receive
   transfers and the static transfer count is kept in bursts. The attempt's
   image wedged the board when the audio bridge restarted capture. Both
   sessions stopped and restarted the bridge without incident.
2. The bench switch runs gPTP toward the controller host's port. With no gPTP
   there, that port stayed outside the SRP domain, so the DUT's SR-class talker
   frames could not reach it. That explains why the attempt recorded no DIN
   stream at all.
   This run ran a slave-only gPTP daemon on the controller NIC inside each
   bounded action. It never offers itself as grandmaster.
3. The software DOUT talker now answers the DUT listener's PROBE_TX, so the
   DUT arms and matches the stream. Its AAF timestamps come from the
   gPTP-disciplined NIC clock.
4. Captures leave the SoC board by a binary-safe transfer checked by SHA-256.

The attempt's all-zero DOUT captures were taken on the old SoC board image. This
run does not establish their cause.

## Between the two sessions

The first session recorded the DUT talker stream while the SoC played the
pattern, and every word was zero. It inferred a fault on the DIN wire or the
SoC transmit pad, and the owner then checked the link wiring. The owner
reported checking all five connections; no wiring change is recorded here.

The cause was the DUT configuration. In this image STREAM_PORT_OUTPUT 0 has
a dynamic audio map: `ADP_DMAP_OUT_MASK_C` bit 0 is set in the generated
shape, and GET_AUDIO_MAP on that port answers `number_of_maps` 1. That makes
the capture crossbar feed the talker
([`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv), line 1344). With an
empty map, every talker channel carries digital silence
([channel map, section 4](../CHANNEL_MAP_64.md#4-capture-mux-contract-kl_chmap_capture-phase-1-name)).
The first session's statement that the talker kept its default front end was
wrong.

The second session first repeated the first session's DIN leg unchanged, as
asked, and again recorded all-zero words. It then repeated it with eight
identity mappings on STREAM_PORT_OUTPUT 0, and the pattern decoded in every
slot. With the map routed, the DIN line reads all ones whenever the SoC is not
playing, so a zero word could not have come from the pin.

The SoC board's USB function was not visible on the bench host in the second
session. Neither leg uses it: the pattern period was built on the SoC board,
and the DOUT capture was copied over the SoC board's serial console.

## Method

Every bench action held the shared exclusive lock. Every command ran in the
foreground with an explicit deadline. No flash, power, wiring, instrument or
USB gadget action occurred.

In both sessions the SoC side was checked read-only first. Both audio bridge
legs were running, the USB device controller reported configured, and no fault
message was logged. With the bridge running, the McASP0 receive DMA completed
249.7 periods of 192 frames per second in the first session and 249.8 in the
second. The bridge's capture restarts lose the partial periods. The two bridge
legs were then stopped by PID, after checking each command line.

Both directions used one pattern. For tag `t` (1 to 8) and frame ordinal `n`,
the 24-bit sample is:

```text
(t << 16) | (n & 0xffff)
```

It sits in bits 31:8 of each 32-bit word; bits 7:0 are zero. A word is valid
only if bits 7:0 are zero and the tag is 1 to 8. A frame is torn if its eight
slots disagree on the ordinal. Channels are zero-based and tag `t` belongs to
channel `t - 1`.

**DOUT.** A software AAF talker on the controller host sent eight-channel
INT32 48 kHz AAF, six frames per PDU, 8,000 PDUs per second. It went untagged
and unicast to the DUT: a diagnostic transport, not an SRP reservation. It was
paced on the gPTP-disciplined NIC clock at a nominal 48 kHz, and each
`avtp_timestamp` was the send time plus 2 ms. The DUT's STREAM_INPUT 0 was
bound to it over ACMP. Eight identity mappings on STREAM_PORT_INPUT 0 took
stream channel `c` to cluster `c`, which the
[channel map](../CHANNEL_MAP_64.md) renders on TDM slot `c`. The SoC recorded
McASP0 directly, eight channels S32_LE at 48 kHz, and the file was hashed on
both ends. The first session ran 70 s and moved the file over TFTP. The
second session ran 3 s and printed the file on the serial console as
`gzip | base64`. Its first transfer used `xz`, which the SoC board can only
decompress, so the file was sent again.

**DIN.** The SoC played the pattern directly into McASP0 for 70 s. In the
first session it was streamed from the bench host over the SoC board's USB
network link. In the second, the SoC board built one 65,536-frame period of
the pattern in its own memory. The period's SHA-256 matched the host
pattern's first period, and aplay read it in a loop. The ordinal is 16 bits
wide, so the played bytes equal the first session's source file.

A software listener on the controller host probed STREAM_OUTPUT 0 over ACMP
until it answered SUCCESS. It then declared an MSRP Domain, an MSRP Listener
Ready for the stream and an MVRP VLAN join, and recorded every frame from the
DUT. The DUT admitted a real reservation: a Ready listener registered, the
stream gate open, and an idleSlope of 16,576,000 bit/s.

The routed DIN run added eight identity mappings on STREAM_PORT_OUTPUT 0
before the listener started: stream channel `c` from cluster `c`. The generated
shape's source table puts output clusters 0 to 7 on TDM input slots 0 to 7. The
mappings were removed afterwards, and the map read back empty.

## Direction decode

These tables separate expectation from observation. Silence cannot establish
slot or channel order.

DOUT: DUT listener stream toward the SoC capture, first session, 70 s.

| SoC capture channel | Mapped stream channel | TDM slot | Recovered tag | Recovered stream channel | Valid words | Result |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 3,357,952 | In order |
| 1 | 1 | 1 | 2 | 1 | 3,357,952 | In order |
| 2 | 2 | 2 | 3 | 2 | 3,357,952 | In order |
| 3 | 3 | 3 | 4 | 3 | 3,357,952 | In order |
| 4 | 4 | 4 | 5 | 4 | 3,357,952 | In order |
| 5 | 5 | 5 | 6 | 5 | 3,357,952 | In order |
| 6 | 6 | 6 | 7 | 6 | 3,357,952 | In order |
| 7 | 7 | 7 | 8 | 7 | 3,357,952 | In order |

Slot order is the identity with no rotation, so the one-bit data delay matches.
Each word arrived with its tag in bits 31:24, its ordinal in bits 23:8 and a
zero low byte. No frame was torn and no word failed the pattern test. The only
zero words are each capture's first 2,048-frame DMA period, which the decode
excludes. The second session's 3 s capture repeated this: all 144,000 frames
held their own tag in every channel, with no torn, invalid or zero word.

DIN: SoC transmit toward the DUT talker stream, second session, routed, 70 s.

| SoC playback channel | Pattern tag | TDM slot | Output cluster | Recovered tag | Recovered stream channel | Valid words | Result |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 1 | 0 | 3,360,035 | In order |
| 1 | 2 | 1 | 1 | 2 | 1 | 3,360,035 | In order |
| 2 | 3 | 2 | 2 | 3 | 2 | 3,360,035 | In order |
| 3 | 4 | 3 | 3 | 4 | 3 | 3,360,035 | In order |
| 4 | 5 | 4 | 4 | 5 | 4 | 3,360,035 | In order |
| 5 | 6 | 5 | 5 | 6 | 5 | 3,360,035 | In order |
| 6 | 7 | 6 | 6 | 7 | 6 | 3,360,035 | In order |
| 7 | 8 | 7 | 7 | 8 | 7 | 3,360,035 | In order |

The playback region is the first to the last frame in which all eight stream
channels carry their own tag. It spans 3,360,035 frames, 70.001 s at 48 kHz,
and inside it every word is valid and carries its own channel's tag. Slot
order is the identity with no rotation. Outside the region the SoC was not
playing, and the slot words read `0xffffff00`: the line idles high.

The two all-zero DIN recordings are not decodable, and silence establishes no
order. The first session's recording held 4,550,280 frames and the second
session's unrouted repeat held 4,554,432. Both carried 0 AVTP sequence gaps,
and both covered all 70 s of playback. In each, the SoC transmit DMA consumed
1,648 periods of 2,048 frames in 70 s.

## DIN frame coherence

Inside the DIN playback region, 2,267,868 of 3,360,035 frames (67.5%) are torn
under the pattern rule. The tearing has a fixed shape. The two channels of a
TDM pair (stream channels `2p` and `2p + 1`) never disagree. Pairs 1 to 3
either match pair 0 or carry the previous TDM frame, always in this order:

| Ordinal offset of pairs 1, 2, 3 against pair 0 | Frames | Share | Meaning |
|---|---|---|---|
| 0, 0, 0 | 1,092,167 | 32.5% | Coherent |
| 0, 0, -1 | 761,510 | 22.7% | Pair 3 one frame older |
| 0, -1, -1 | 761,459 | 22.7% | Pairs 2 and 3 one frame older |
| -1, -1, -1 | 744,899 | 22.2% | Pairs 1 to 3 one frame older |

The state cycles through these four in order once per beat, 1.958 s, and
steps back and forth a few times at each change. The longest coherent run is
30,477 frames, and the longest run of each other state is 21,096. Together
they make about one beat, 93,990 frames.

The mechanism is in the capture crossbar. Each TDM pair's hold is written by
its own pair-valid pulse
([`KL_chan_map_capture.sv`](../../hdl/ieee1722/aaf/KL_chan_map_capture.sv),
lines 486 to 487). The media-tick walk reads the latest hold of each pair
(lines 958 to 960), with no frame-wide buffer. The TDM frame runs 10.64 ppm
behind the media grid, so the tick drifts through the TDM frame. It reads each
pair either before or after that pair's update.

This is a DUT capture-path property: the samples of one AAF frame can come
from two TDM frames, one sample period apart. The SoC transmits whole frames,
and the render direction updates atomically (DOUT showed no torn frame). It is
recorded for triage as a separate issue.

## Continuity and rate

| Direction | Window | Frames observed | Torn or invalid | Discontinuities | Result |
|---|---|---|---|---|---|
| DOUT | 70 s SoC capture, first session | 3,357,952 | 0 | 2,173 repeated, 2,191 dropped, net 18 dropped | Slot integrity proven; frame continuity bounded as below |
| DOUT | 3 s SoC capture, second session | 144,000 | 0 | 40 repeated, 42 dropped: two beat clusters, net one drop each | No regression |
| DIN | 70 s SoC playback, routed, second session | 3,360,035 | 0 invalid; 2,267,868 torn between pairs | Per channel only beat clusters; 0 AVTP sequence gaps in 758,870 PDUs | Slot integrity and channel continuity proven; frame coherence not met |

Every DOUT discontinuity is a whole-frame repeat or a whole-frame drop.
Discontinuities closer than 50 ms were grouped into clusters.

| DOUT cluster class | Clusters | Repeated frames | Dropped frames | Cause |
|---|---|---|---|---|
| INTERNAL-source beat | 34 | 657 | 691 | TDM frame against media tick; spacing 93,989 to 93,992 frames (1.958 s); net one drop per crossing |
| Underrun after logged talker lateness | 9 | 975 | 963 | A PDU sent 150 us or more late within the preceding 60 ms |
| Underrun, no host-visible lateness | 8 | 541 | 537 | Same signature; lateness not visible to the sending process |

The beat is documented behaviour at the INTERNAL clock source (see the
[channel map](../CHANNEL_MAP_64.md)). The render stage's constant-latency law
tolerates one PDU interval of lateness
([listener render latency](../design/TIME_SYNC.md#listener-render-latency)),
so the talker's jitter on a general-purpose host shows as underruns. Neither is
a TDM link property.

Over the first session's capture window, the DUT listener reported zero
sequence mismatches, zero unsupported formats, zero uncertain timestamps and
zero depacketizer drops. Media stayed locked, with no unlock or interruption.
The presentation offset read 1.98 ms, and the render stage's rail count rose
from 3 to 142.

DIN continuity was measured per channel, over every frame of the playback
region. Each channel steps by one ordinal per frame, except at beat
crossings. Each pair crosses at its own point in the beat.

| DIN pair (stream channels) | Beat clusters | Cluster spacing (frames) | Repeated | Skipped | First cluster at recording frame |
|---|---|---|---|---|---|
| 0 (0, 1) | 35 | 93,990 to 93,993 | 711 | 676 | 237,364 |
| 1 (2, 3) | 36 | 93,990 to 93,993 | 736 | 700 | 216,211 |
| 2 (4, 5) | 36 | 93,990 to 93,993 | 734 | 698 | 195,061 |
| 3 (6, 7) | 36 | 93,990 to 93,993 | 734 | 698 | 173,908 |

Every cluster nets exactly one repeated frame, and no channel shows any other
step. That is 0.51 repeats per second, the same slip the DUT counts.

The DUT's `SLIP_TDM` duplicate counter rose from 10,682 to 14,893 over
8,244.7 s across both sessions, which is 0.5108 per second. That puts FSYNC
10.64 ppm below the media grid and matches the
[divider plan](../litex/CLOCK_DOMAINS.md) of -10.64 ppm. The counter is the DUT
comparing its own two clocks, not a pin measurement. The beat seen at the SoC
pins and in the talker stream agrees: one crossing per 93,990 frames is
10.64 ppm. Against gPTP time, the first session's talker ordinal slope put
FSYNC near -5 ppm, with 10 s blocks spread from -12.5 to 0 ppm. That figure is
not calibrated.

## Restoration

| State | Restored value |
|---|---|
| DUT and reference peer stream states | All 4 DUT and 14 peer states unbound |
| DUT audio maps, input and output port | Empty |
| DUT and peer clock source and rate | DUT 0 at 48 kHz; peer 0 at 96 kHz |
| DUT AAF control and fallback destination | `00020001`; `f000fe01` / `000091e0` |
| DUT MAAP, channel-map and tone controls | `00000201`; `00000000`; `00000000` |
| DUT synchronization | SYNC=1, ASCAPABLE=1, TU=0, grandmaster unchanged |
| SoC audio bridge | Both legs restarted with the bridge script's own command lines; status reports both running |
| SoC board | USB device controller configured; no fault message; no task file left |
| Controller host | No task process; staging directory removed |

A census taken after each session matched that session's baseline in all
entries but the live propagation delay. The first session had one more
difference, the destination address below. Across the second session, the
DUT read back equal in every control word and in `PP_STAT`.

Residuals that no permitted command restores:

- DUT STREAM_OUTPUT 0 reports its MAAP destination in GET_TX_STATE. The
  address was allocated when it was first probed. The output has zero
  connections and declares nothing.
- `PP_STAT` bit 11, pending persistence work, is set after the mapping and
  binding edits. The live maps and bindings equal the baseline. The attempt
  left the same bit set.
- The controller NIC clock keeps the gPTP daemon's last frequency, with
  hardware timestamping enabled.

Operator errors:

- The first census sent AEM command code `0x002A` intending GET_AUDIO_MAP;
  `0x002A` is REBOOT. Two REBOOT commands reached the DUT and both were
  refused with NOT_IMPLEMENTED. The DUT did not reset: its slip counters kept
  counting and its MAAP offset and status were unchanged. The tool was
  corrected before any further command.
- The first session's DIN method left the talker's output map empty, and its
  STOP attributed the silence to the wiring. See
  [Between the two sessions](#between-the-two-sessions).

## Owner items

| Item | Result |
|---|---|
| DIN path: J11.7 to P1.02, SoC transmit pad and setup | Working: pattern decoded in all eight slots; idle line reads high |
| Electrical continuity check | NOT RUN here; the owner reported checking the wiring between the sessions |
| BCLK, FSYNC and DOUT scope measurements | NOT RUN, owner item |
| Same-sample timing, #386 acceptance 4 | NOT RUN, owner item |
| Calibrated listener-audio sequence, #117 | NOT RUN, owner item |
| DOUT slot and channel order | PROVEN, identity |
| DIN slot and channel order | PROVEN, identity |
| Sixty seconds of identifiable audio | DOUT met (70 s); DIN met (70 s) |
| DIN frame coherence across channel pairs | NOT MET: a DUT capture-path property, for triage as a separate issue |
| SoC board USB function on the bench host | Not visible in the second session; both legs ran without it |

The identity STOP condition did not occur, and the SoC saw bit clock and frame
sync in both sessions. This record does not close #451, #448, #386 or #117.

## Artifacts and validation

The publication packet is identified as `451-a403`. Its manifest covers every
retained file except itself. Raw originals stay outside the packet and are
indexed there by size and hash.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| Assigned bitstream | 3825992 | `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` |
| Assigned AEM image | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| DOUT 70 s SoC capture | 107520000 | `b025b92f13104386edc8897555f7fe2765945ab915683b3e4f27f861efc5963d` |
| DOUT 3 s preflight capture | 4608000 | `f98d4e8280e55d468ae4ac7611eaa53ac439363788b008e50c11ea846235857b` |
| DOUT 3 s second-session capture | 4608000 | `0fce03df6de3a48609c4d5637acf230924581af28ccfd58038f92587b33a2f8a` |
| DIN pattern | 138240000 | `964da880be7d28860640ead49cd3a96ff974a73a61d8dce04c29b845916a9235` |
| DIN pattern period, built on the SoC board | 2097152 | `b6a92e9724e945354c3f8fc5178cec7bb8fd0e62d52bd9ee7f13ed5347bfa97c` |
| DIN 94.8 s talker stream recording, first session | 189598382 | `70a8b6e027d2abf0ac3b833917c63a97c6f8c99a4cd1e873b4900ebe48a9a484` |
| DIN preflight talker stream recording | 79677110 | `ff5cf9afcb396ffe6bc671518aca123fbf7870f5f88e66fcd3db88a470c22ca7` |
| DIN 94.9 s talker stream recording, unrouted repeat | 189771350 | `351f9aaaef6811995b34cd1832e12b988df9455145536ac60c9d4a03c376b692` |
| DIN 94.9 s talker stream recording, routed | 189720730 | `2ab93c0bc7e6c1710b3a2212e0b833d933b5b09529e32e28eae9aebedd5da66d` |

Validation commands and results belong to the accompanying packet. They cover
documentation integrity, scope controls and bare-metal policy.
