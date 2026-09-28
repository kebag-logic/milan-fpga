# TDM8 first light, 2026-09-28

[A403] STOP. Refs #451.

DOUT first light is established. Over a 70 s capture, every slot word the SoC
received decodes to the expected channel, in order, with no torn frame.

DIN is not established. While the SoC transmitted the pattern for 70 s, the
DUT's talker stream carried only zero words. With BCLK, FSYNC and DOUT shown
working, that is a wiring or physical question for the owner.

This page replaces the record of the 2026-09-27 attempt, which remains in Git
history at `fba793c0885d091802c96313d5df3234900dce0d`. Bench state was
restored; the residuals are listed under [Restoration](#restoration).

## Contents

- **[Scope and identity](#scope-and-identity)** -- Pin the assignment, the tested image and the live SoC board configuration.
- **[What changed since the attempt](#what-changed-since-the-attempt)** -- The repaired SoC board and the transport corrections that made both directions observable.
- **[Method](#method)** -- How each direction was driven and recovered, and what each observation can and cannot show.
- **[Direction decode](#direction-decode)** -- Per-channel slot and channel order for DOUT, and the all-zero DIN result.
- **[Continuity and rate](#continuity-and-rate)** -- The 70 s windows, every DOUT discontinuity classified, and the frame-rate offset.
- **[Restoration](#restoration)** -- Restored state, the residuals, and one operator error.
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
readback.

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

## What changed since the attempt

1. The owner repaired the SoC board on 2026-09-28. Its software image now
   carries a k3-udma DMA fix for BCDMA cyclic receive: end of packet is restored on receive
   transfers and the static transfer count is kept in bursts. The attempt's
   image wedged the board when the audio bridge restarted capture. This run
   stopped and restarted the bridge without incident.
2. The bench switch runs gPTP toward the controller host's port. With no gPTP
   there, that port stayed outside the SRP domain, so the DUT's SR-class talker
   frames could not reach it. That explains the attempt's empty DIN recordings.
   This run ran a slave-only gPTP daemon on the controller NIC inside each
   bounded action. It never offers itself as grandmaster.
3. The software DOUT talker now answers the DUT listener's PROBE_TX, so the
   DUT arms and matches the stream. Its AAF timestamps come from the
   gPTP-disciplined NIC clock.
4. Captures leave the SoC board over TFTP, which is binary-safe.

The attempt's all-zero DOUT captures were taken on the old SoC board image. This
run does not establish their cause.

## Method

Every bench action held the shared exclusive lock. Every command ran in the
foreground with an explicit deadline. No flash, power, wiring, instrument or
USB gadget action occurred.

The SoC side was checked read-only first. Both audio bridge legs were running,
the USB device controller was configured, and no fault message was logged. With
the bridge running, the McASP0 receive DMA completed 249.7 periods of 192
frames per second; the bridge's capture restarts lose the partial periods. The
two bridge legs were then stopped by PID. A direct 3 s capture returned 144,000
frames in 3.05 s of board time.

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
both ends.

**DIN.** The SoC played the pattern directly into McASP0 for 70 s, streamed
from the host over the SoC board's USB network link. The DUT talker kept its
default front end, the TDM capture master, with no output mapping. A software
listener on the controller host probed STREAM_OUTPUT 0 over ACMP until it
answered SUCCESS. It then declared an MSRP Domain, an MSRP Listener Ready for
the stream and an MVRP VLAN join, and recorded every frame from the DUT. The
DUT admitted a real reservation: a Ready listener registered, the stream gate
open, and an idleSlope of 16,576,000 bit/s.

## Direction decode

These tables separate expectation from observation. Silence cannot establish
slot or channel order.

DOUT: DUT listener stream toward the SoC capture.

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
excludes.

DIN: SoC transmit toward the DUT talker stream.

| SoC playback channel | Pattern tag | Expected TDM slot | Expected stream channel | Recovered words | Result |
|---|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 4,550,280 zero | Not decoded |
| 1 | 2 | 1 | 1 | 4,550,280 zero | Not decoded |
| 2 | 3 | 2 | 2 | 4,550,280 zero | Not decoded |
| 3 | 4 | 3 | 3 | 4,550,280 zero | Not decoded |
| 4 | 5 | 4 | 4 | 4,550,280 zero | Not decoded |
| 5 | 6 | 5 | 5 | 4,550,280 zero | Not decoded |
| 6 | 7 | 6 | 6 | 4,550,280 zero | Not decoded |
| 7 | 8 | 7 | 7 | 4,550,280 zero | Not decoded |

The DUT captured zero in every slot for the whole window, including all 70 s
of playback. The SoC's transmit DMA consumed the pattern at the frame rate:
1,648 period events of 2,048 frames in 70 s. The image connects the `tdm`
resource's `din` pad to the capture master in
[`milan_soc.py`](../../sw/litex/milan_soc.py). The same pad group demonstrably
drives BCLK, FSYNC and DOUT. The open question is therefore confined to the DIN
path: J11.7 to P1.02, the SoC's AXR0 pad on P1.02, or its transmit
configuration.

## Continuity and rate

| Direction | Window | Frames observed | Torn or invalid | Discontinuities | Result |
|---|---|---|---|---|---|
| DOUT | 70 s SoC capture | 3,357,952 | 0 | 2,173 repeated, 2,191 dropped, net 18 dropped | Slot integrity proven; frame continuity bounded as below |
| DIN | 70 s SoC playback in a 94.8 s stream | 4,550,280 | Not measurable, all zero | 0 AVTP sequence gaps in 758,380 PDUs | Content NOT PROVEN |

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

Over the capture window, the DUT listener reported zero sequence mismatches,
zero unsupported formats, zero uncertain timestamps and zero depacketizer drops.
Media stayed locked, with no unlock or interruption. The presentation offset
read 1.98 ms, and the render stage's rail count rose from 3 to 142.

The DUT's `SLIP_TDM` duplicate counter rose from 10,682 to 11,859 over
2,303.7 s, which is 0.5109 per second. That puts FSYNC 10.64 ppm below the
media grid and matches the [divider plan](../litex/CLOCK_DOMAINS.md) of
-10.64 ppm. The counter is the DUT comparing its own two clocks, not a pin
measurement. The beat seen at the SoC pins agrees: one crossing per 93,990
frames is 10.64 ppm. Against gPTP time, the talker's ordinal slope put FSYNC
near -5 ppm, with 10 s blocks spread from -12.5 to 0 ppm. That figure is not
calibrated.

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

A census taken after the run matched the baseline in 28 of 30 entries. The two
differences are the live measured propagation delay (381 to 386 ns) and the
destination address below.

Residuals that no permitted command restores:

- DUT STREAM_OUTPUT 0 now reports its MAAP destination in GET_TX_STATE. The
  address was allocated when it was first probed. The output has zero
  connections and declares nothing.
- `PP_STAT` bit 11, pending persistence work, is set after the mapping and
  binding edits. The live maps and bindings equal the baseline. The attempt
  left the same bit set.
- The controller NIC clock keeps the gPTP daemon's last frequency, with
  hardware timestamping enabled.

One operator error touched the DUT. The first census sent AEM command code
`0x002A` intending GET_AUDIO_MAP; `0x002A` is REBOOT. Two REBOOT commands
reached the DUT and both were refused with NOT_IMPLEMENTED. The DUT did not
reset: its slip counters kept counting and its MAAP offset and status were
unchanged. The tool was corrected before any further command.

## Owner items

| Item | Result |
|---|---|
| DIN path: J11.7 to P1.02, SoC AXR0 pad and transmit setup | OWNER: DIN reaches the DUT as all-zero words |
| Electrical continuity check | NOT RUN, owner item |
| BCLK, FSYNC and DOUT scope measurements | NOT RUN, owner item |
| Same-sample timing, #386 acceptance 4 | NOT RUN, owner item |
| Calibrated listener-audio sequence, #117 | NOT RUN, owner item |
| DOUT slot and channel order | PROVEN, identity |
| DIN slot and channel order | NOT DECODED |
| Sixty seconds of identifiable audio | DOUT met (70 s); DIN not met |

The identity STOP condition did not occur. The SoC saw bit clock and frame
sync, and the USB audio function stayed enumerated. This STOP records the DIN
result for the owner. It does not close #451, #448, #386 or #117.

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
| DIN pattern | 138240000 | `964da880be7d28860640ead49cd3a96ff974a73a61d8dce04c29b845916a9235` |
| DIN 94.8 s talker stream recording | 189598382 | `70a8b6e027d2abf0ac3b833917c63a97c6f8c99a4cd1e873b4900ebe48a9a484` |
| DIN preflight talker stream recording | 79677110 | `ff5cf9afcb396ffe6bc671518aca123fbf7870f5f88e66fcd3db88a470c22ca7` |

Validation commands and results belong to the accompanying packet. They cover
documentation integrity, scope controls and bare-metal policy. They cannot
substitute for the missing DIN evidence.
