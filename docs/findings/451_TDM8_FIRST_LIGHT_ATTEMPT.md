# TDM8 first-light attempt, 2026-09-27

[A382] STOP. Refs #451.

First light and complete restoration remain unproved.
The SoC management shell stopped responding during bridge checks.
Its bridge processes and PID files require owner recovery.
The USB audio function remained enumerated.

The DUT and reference peer were restored.
No flash, power, wiring, or instrument changes occurred.
No USB gadget re-enumeration occurred.

## Contents

- **[Scope and identity](#scope-and-identity)** -- Pin the assignment and tested image.
- **[Method and limitations](#method-and-limitations)** -- Separate transport attempts from physical evidence.
- **[Direction decode](#direction-decode)** -- Record expected slots and actual observations.
- **[Continuity and rate](#continuity-and-rate)** -- Preserve incomplete measurements without claiming continuity.
- **[Restoration](#restoration)** -- Distinguish restored settings from the remaining blocker.
- **[Owner items](#owner-items)** -- Keep physical acceptance explicitly unperformed.
- **[Artifacts and validation](#artifacts-and-validation)** -- Identify retained evidence and local checks.

## Scope and identity

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5859278962)
limits this run to software-side first light.
The [amendment](https://github.com/kebag-logic/milan-fpga/issues/451#issuecomment-5729936674)
defines the four-wire, synchronous SoC variant.

The lane base is `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
The image source is `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.
The required FSYNC fix, `9c423e2c`, precedes that source.
Its RTL matches the lane base.

| Identity observation | Result |
|---|---|
| VERSION | `00020060` |
| ROM CRC32, 52,216 bytes | `9b6576a9` |
| QSPI payload CRC32, 3,825,788 bytes | `3c18c276` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| ENTITY and CONFIGURATION replies | Exact matches to previously verified templates |
| Identity gate | PASS |

This establishes CRC consistency and descriptor identity.
It does not read configuration SHA-256 from silicon.

| Dependency | Image pin |
|---|---|
| Protocol processor | `870ff88ad35bbd532244e4c7e6d7661b9f6e1366` |
| gPTP processor | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` |
| AXIS library | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |
| External dependency | `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5` |

## Method and limitations

Read the [capture and render contracts](../CHANNEL_MAP_64.md).
The [platform resource](../../sw/litex/platforms/alinx_ax7101.py)
defines the corresponding DUT pins.
The [integration contract](../integration/INTEGRATION_GUIDE.md)
defines clock ownership and inactive behavior.

Every bench action used the shared exclusive lock.
Commands ran in the foreground with explicit deadlines.
Large captures remained outside the publication packet.

The live SoC tree selected DSP_A and external clocks.
It specified eight slots, each containing 32 bits.
Serializer 0 transmitted; serializer 1 received.
Initial two-second and three-second direct captures completed.
These establish transfer progress, not calibrated clock frequencies.

Both USB bridge legs initially reported DEAD.
All four SoC PCM endpoints initially reported closed.
The host still enumerated eight-channel USB audio.
Both DUT audio maps were initially empty.

For DIN, direct playback supplied eight distinguishable sample tags.
For channel `c`, the 24-bit sample was:

```text
((c + 1) << 16) | (frame_ordinal & 0xffff)
```

Channels are zero-based throughout this page.
Each sample occupied bits 31:8 of an S32_LE word.
The lower eight bits were zero.

A reference-listener binding produced no captured DUT AAF.
A requested 48 kHz setting returned BAD_ARGUMENTS.
The original 96 kHz setting was subsequently verified.
The temporary binding was removed.

A software listener also failed to obtain DUT AAF.
The DUT reported Listener Asking Failed during that trial.
This does not establish why the recorder saw nothing.

Subsequent trials used the documented AAF diagnostic bypass.
They temporarily changed the fallback destination and MAAP control.
All saved control words and the allocation were restored.
These trials do not establish normal SRP operation.

For DOUT, a software sender generated the same ordinal pattern.
AAF carried six eight-channel frames per packet.
Its format was INT32, nominally 48 kHz, MSB-justified.
The sender used a distinct stream identifier.
Packets reached the DUT through an untagged diagnostic transport.

Eight temporary input mappings selected channels 0 through 7.
GET_AUDIO_MAP confirmed all eight mappings.
The temporary listener binding selected the software stream.
DUT receive, matching, and depacketizer counters advanced.
These counters do not prove physical pin output.

The sender used received CRF timestamps as its initial anchor.
It added two milliseconds to its timestamp schedule.
This was not a calibrated timing measurement.

The sender's maximum scheduling lateness reached 25.375 milliseconds.
Render-state snapshots included changing fill and increasing rails.
This source cannot establish clean real-time transport.

Direct SoC captures contained only zero words.
Consequently, no identifiable DOUT slot was recovered.
No physical fault location is assigned from these observations.

## Direction decode

These tables distinguish expectations from observations.
Silence cannot establish slot or channel order.

DIN: SoC transmit toward the DUT talker.

| SoC channel | Expected slot | Pattern tag | Observed wire channel | Result |
|---|---|---|---|---|
| 0 | 0 | 1 | None | Not decoded |
| 1 | 1 | 2 | None | Not decoded |
| 2 | 2 | 3 | None | Not decoded |
| 3 | 3 | 4 | None | Not decoded |
| 4 | 4 | 5 | None | Not decoded |
| 5 | 5 | 6 | None | Not decoded |
| 6 | 6 | 7 | None | Not decoded |
| 7 | 7 | 8 | None | Not decoded |

DOUT: DUT listener toward the SoC capture endpoint.
The expected source and slot follow the programmed identity map.

| SoC capture channel | Expected source/slot | Recovered tag | Captured word | Result |
|---|---|---|---|---|
| 0 | 0 / 0 | None | `00000000` | Order unproved |
| 1 | 1 / 1 | None | `00000000` | Order unproved |
| 2 | 2 / 2 | None | `00000000` | Order unproved |
| 3 | 3 / 3 | None | `00000000` | Order unproved |
| 4 | 4 / 4 | None | `00000000` | Order unproved |
| 5 | 5 / 5 | None | `00000000` | Order unproved |
| 6 | 6 / 6 | None | `00000000` | Order unproved |
| 7 | 7 / 7 | None | `00000000` | Order unproved |

## Continuity and rate

The planned long run used 66-second DIN excitation.
It requested a 69-second direct DOUT capture.
The software endpoint observed transport for 72 seconds.

| Direction | Long-run evidence | Sixty-second physical continuity |
|---|---|---|
| DIN | Playback connection timed out; zero DUT AAF packets captured | NOT PROVEN |
| DOUT | 567,990 generated AAF packets; partial capture contained only zeros | NOT PROVEN |

The generated packet file contains 3,407,940 audio frames.
Its first-to-last recorder span is 70.998537 seconds.
Offline checks found zero sequence or pattern errors there.
Those checks validate generated input, not the physical output.

The SoC capture exhausted temporary storage.
Earlier captures and the pattern file occupied that storage.
Those operator-created files were transferred, hashed, and removed.
The attempted measurement was not credited as successful.

The partial capture contains 1,126,144 eight-channel frames.
That represents 23.461333 nominal seconds at 48 kHz.
Every captured channel contains zero nonzero samples.
Dropped or misaligned physical frames therefore remain uncountable.

The [divider plan](../litex/CLOCK_DOMAINS.md)
predicts 47,999.4893 Hz and approximately -10.64 ppm.
That offset was not physically measured in this run.
Neither a requested PCM rate nor silence measures it.

## Restoration

All 18 network stream states returned to unbound.
A 51-entry settings and descriptor comparison passed.
DUT clock source 0 and 48 kHz remained unchanged.
Reference clock source 0 and 96 kHz were restored.
Both DUT audio maps returned to their original empty state.

| DUT setting | Restored value |
|---|---|
| AAF control | `00020001` |
| AAF fallback destination low/high | `f000fe01` / `000091e0` |
| MAAP control | `00000201` |
| MAAP allocation | Offset `6817`, count 2, valid |
| Channel-map diagnostic control | `00000000` |
| Final synchronization | SYNC=1, ASCAPABLE=1, TU=0 |

Controller measurement processes ended and temporary files were removed.
No local audio process remained at the cleanup audit.
The bench lock was released.

Full SoC restoration did not complete.
Two foreground bridge-process starts were attempted.
Subsequent management connections timed out.
The serial console echoed input without returning shell output.
A final bounded readiness probe also failed.

The bridge process state consequently remains UNKNOWN.
Its original PID-file contents were 231 and 232.
Restoring those files and stopped processes remains pending.
No gadget down/up, UDC write, or power action occurred.
USB audio remained enumerated at the final local check.

Owner recovery must first restore a responsive management shell.
Then verify and stop only the named bridge processes.
Restore the original PID files and closed PCM state.
No further audio experiment should precede that verification.

## Owner items

| Item | Result |
|---|---|
| Electrical continuity check | NOT RUN, owner item |
| BCLK, FSYNC, and DOUT scope measurements | NOT RUN, owner item |
| Same-sample timing, #386 acceptance 4 | NOT RUN, owner item |
| Calibrated listener-audio sequence, #117 | NOT RUN, owner item |
| Sixty-second identifiable audio in both directions | NOT MET |
| Complete SoC restoration | BLOCKED, owner recovery required |

The identity STOP condition did not occur.
Completed slave captures showed clocked transfer progress.
The USB-disappearance STOP condition did not occur.
This STOP records failed first light and unresolved restoration.
It does not close #451, #448, #386, or #117.

## Artifacts and validation

The publication packet is identified as `451-a382`.
Its manifest covers every retained file except itself.
The raw index records original sizes, hashes, and locations.
Public logs use role labels and documented redactions.
Operational originals remain outside the publication packet.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| Assigned bitstream | 3825992 | `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` |
| Assigned AEM image | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| DIN pattern | 107520000 | `d74da27bf4d7feba8fe3b6019c761dfd73d30427b903f3aa835c30313d94504a` |
| Generated DOUT packet file | 139725564 | `97f153f3383beadec7ab67c03073d0a0359c761051ef6980e092148cd63be04f` |
| Partial DOUT PCM | 36036608 | `1530b5611bc1d0bc08441568a922277a04481391ad51c18e8e1a91bfb55ff905` |
| Empty DIN packet file | 24 | `acc530668c8bc60b2d229281130b1899bfc81d70fdada5c34b3236c628f739c8` |

Validation commands and results belong to the accompanying packet.
They cover documentation integrity, scope controls, and bare-metal policy.
They cannot substitute for the missing physical evidence.
