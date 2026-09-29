<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# First talker bind on the 13eda870 image

Refs #606. Operator [A440], measured 2026-09-29, under the
[bench lane B2 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413).

The image carries processor pin `c951a9ff`, adopted by [PR #613](https://github.com/kebag-logic/milan-fpga/pull/613).

That pin retries a refused destination-address allocation every 100 ms.

| #606 item | Verdict | Evidence |
|---|---|---|
| 1. When a talker must declare Talker Advertise | Not a bench item | Answered by the [A10 analysis](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5860869610) on #606. The declaration gate is observed here; see [Declaration gate on the wire](#declaration-gate-on-the-wire). |
| 2. Reproduce and attribute in simulation | Not a bench item | The [A10] analysis and PR #613's first-probe regression. |
| 3. First bind on the bench, against 1 s | PASS, 5 of 5 | 0.059-0.229 s from the `CONNECT_RX` response to the first valid CRF PDU. See [Per-bind results](#per-bind-results). |
| 3. Long-hold connect on the bench, against 1 s | PASS, 4 of 4 | Binds 2-5 follow 36.9-39.3 s unbound, each after the DUT withdrew its Talker Advertise. |
| 3. Periodic refresh and LeaveAll kept | Observed, not graded | DUT MSRP refresh stays at 1.000 s. A DUT LeaveAll crossed every pre-bind window. |

These are operator measurements, not review verdicts.

The post-reset allocation path is not exercised; see [Limits](#limits).

The [#608 and #75 page](608_75_WITHDRAWAL_AND_RESTART.md) records the same session's 100 cycles.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, its identity readback, the bound pair and the bench as found.
- **[Method](#method)** -- What makes a bind fresh, how it is reached without a reset, and the timing anchors.
- **[Per-bind results](#per-bind-results)** -- Five first binds and the four unbinds between them.
- **[Declaration gate on the wire](#declaration-gate-on-the-wire)** -- When the DUT declares and withdraws its Talker Advertise.
- **[Comparison with the 9e9954e9 first bind](#comparison-with-the-9e9954e9-first-bind)** -- The PR #604 first bind beside these five.
- **[Limits](#limits)** -- What this bench run does not show.
- **[Restore](#restore)** -- The bench as left.
- **[Artifact hashes](#artifact-hashes)** -- Image, tool and raw-capture identities.

## Identity and setup

The image is dev `13eda870d1a6cf3f946fc228a98862366b08d102`, seed `eto`.

Lane B1 identified the same image in [PR #620](https://github.com/kebag-logic/milan-fpga/pull/620).

The lane base is the same commit, so no source differs.

| Identity check | Result |
|---|---|
| VERSION | `0x00020060` |
| ROM CRC32, 53,344 bytes | `acad92b9` |
| QSPI payload CRC32, 3,825,788 bytes | `d84bce7b`, the `eto` seed; `eppo` reads `bf44ccc9`, `asl` reads `809fcffa` |
| AEM CRC32, 7,352 bytes | `93742dd2` |
| Live ENTITY and CONFIGURATION | Byte-exact to the AEM image at `0x110` (312 bytes) and `0x248` (106 bytes); entity `020000fffe000001` |
| UART grader | 10 of 10, exit 0 |
| Reset epoch | 1, before and after every action |

Readback proves CRC consistency, not a configuration SHA-256.

The [identity method](117_GPTP_SILICON_EVIDENCE.md#candidate-image-and-identity-proof) was repeated.

Topology: the DUT, the inline tap, the bench AVB switch, the reference peer.

The switch is the adjacent bridge and the grandmaster.

The controller host shares the AVB network behind it.

| Binding | Talker output | Listener input | Format |
|---|---|---|---|
| DUT talker | DUT Stream Output 1, stream `0200000000010001` | Reference peer Stream Input 8 | CRF `041060010000bb80` |

As found, all 18 queried stream states were unbound.

The DUT selected clock source 0, INTERNAL.

The reference peer was in configuration 1 at 48 kHz, as PR #620 found.

Neither setting changed in this lane.

Both DUT Stream Outputs already held MAAP-range destinations.

Output 0 (`91:e0:f0:00:e5:11`) was never bound in this lane.

On image `9e9954e9` both outputs read all-zero at the #75 start census.

That matches processor PR 129's automatic acquisition.

The acquisition itself happened before this lane and was not observed.

## Method

**Fresh state.** A bind is fresh when the DUT declares no Talker Advertise for the stream.

The runner checks at least 16 s of tap before sending `CONNECT_RX`.

That window must contain a DUT MSRP LeaveAll.

A declaring applicant re-declares its attributes after its own LeaveAll.

Only `New`, `JoinIn` and `JoinMt` count as declarations.

The window must also carry no bridge Listener declaration and no stream PDU.

The runner refuses to bind otherwise; it refused none of the five.

**Reaching it without a reset.** The processor's talker declares under a gate.

It declares while a probe is under 15 s old, or while a listener is registered.

The gate is `T-SRP-DAFRESH` in the processor's
[ACMP engine design](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/c951a9ff0cb5851fb159d33e966e5a2a9a188fe3/docs/architecture/05_acmp_engine.md), section 6bis.

So after an unbind the DUT sends `Lv` once the last probe is 15 s old.

The unbind action waits for that `Lv`, then 10 s more.

The next bind's 16 s window follows, so its `CONNECT_RX` comes at least 26 s after the `Lv`.

That exceeds the 802.1Q LeaveTime of 0.6-1.0 s and the processor's 4.5-7.5 s in its
[timer table](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/c951a9ff0cb5851fb159d33e966e5a2a9a188fe3/docs/architecture/08_timing.md).

Bind 1 followed more than 30 minutes unbound, since lane B1's restore.

The DUT was never reset, rebooted, flashed or power-cycled.

**Timing.** Each bind is one `CONNECT_RX` from the controller host.

The successful response crossing the tap starts the interval.

The first valid CRF PDU of the stream ends it.

The validity predicate is [PR #604's](75_RECONNECT_RESTART_MEASUREMENT.md#method):

- EtherType `0x22f0`, subtype `0x04`, at least 28 bytes;
- `sv=1`, version 0, type 1, 48 kHz with pull 0;
- eight bytes of data per 96 samples;
- VLAN 2 with PCP 3, the bound stream ID;
- the DUT's tap port and source address;
- the settled binding's destination address;
- the next PDU advancing sequence and timestamp.

The tap stamps both directions on one hardware clock.

Its nanosecond word is unwrapped against the capture host's timestamps.

Host clock offsets do not enter any interval.

CRF PDUs come every 2 ms, which bounds when streaming could start.

**Other records.** Each action read the DUT console before and after.

The reads were `milan_status` and six read-only CSR words.

The controller read AVB_INTERFACE and stream counters before and after.

Every action held the bench lock for its own duration only.

An offline replay of every capture reproduces each live interval exactly.

## Per-bind results

All times are seconds after the tapped `CONNECT_RX` response.

{{binds}}

- The reference peer's `PROBE_TX` crossed the tap 27-83 us after the response.
- The DUT answered each with SUCCESS 7 us later.
- The DUT's first Talker Advertise was a `JoinMt`, inside one 0.2 s join period.
- The bridge's first MRPDU was its Listener Ready (`New`) each time.
- No bridge LeaveAll came between the response and that Ready.
- The first valid PDU followed Ready by 0.6-1.8 ms.
- DUT Stream Output 1 counted STREAM_START +1 per bind.

Unbinds between binds, seconds after the tapped `DISCONNECT_RX` response:

{{unbinds}}

"After bind response" is on the controller host's clock; the rest are tap times.

Every unbind stopped the stream within one PDU of the bridge's Listener `Lv`.

## Declaration gate on the wire

- Unbind 1 came 25.7 s after its bind; the DUT withdrew 21 ms after the response.
- Unbinds 2-4 came 7.9-8.1 s after their binds.
- Their withdrawals came 7.1-7.2 s later, 15.07-15.17 s after the bind.
- That is the 15 s probe freshness of the gate.
- Before each bind the DUT sent only `Mt` for the stream, never a declaration.
- DUT MSRP PDUs kept a 1.000 s spacing in the baseline and final captures.

## Comparison with the 9e9954e9 first bind

The earlier record is PR #604's `talker-setup` capture, with [A10]'s analysis on #606.

| Event after the `CONNECT_RX` response | `9e9954e9`, one bind | `13eda870`, binds 1-5 |
|---|---|---|
| First `PROBE_TX` response | status 3, `TALKER_DEST_MAC_FAILED` | SUCCESS, 5 of 5 |
| First DUT Talker Advertise | 0.079 s | 0.000337-0.172822 s |
| Bridge's first MRPDU | LeaveAll at 6.080 s | Listener Ready at 0.057989-0.227724 s |
| Bridge Listener Ready | 6.888605 s | 0.057989-0.227724 s |
| First valid CRF PDU | 6.889398 s | 0.059352-0.229360 s |

The old first bind waited for the peer's second probe after a refused one.

Here the first probe succeeds and no LeaveAll is involved.

## Limits

- **The post-reset path is not exercised.** The #606 cause was a refused startup allocation.
- Reaching it needs a DUT reset, which this lane forbids.
- The DUT's destinations were already held, so no allocation ran here.
- PR #613's first-probe regression remains that branch's evidence.
- The reference peer's own link is behind the bridge and not tapped.
- Only CRF was measured; AAF remains unmeasured.
- Printed precision is not a calibrated timestamp accuracy.

## Restore

- The pair was unbound on the first attempt; all 18 stream states read connection count 0.
- The start and end censuses agree on all 53 non-counter reads.
- The DUT still selects INTERNAL; the peer is unchanged.
- A final 16.9 s tap capture carried no CRF PDU.
- The UART grader passed 10 of 10; the reset epoch read 1.
- The temporary controller and capture scripts were removed.
- The temporary capture module was unloaded and its build removed.
- The capture host's interface set is as found.
- Outlets read as B1 left them; this lane switched none.
- The bench lock was verified free.

The [#608 and #75 page](608_75_WITHDRAWAL_AND_RESTART.md#counters-and-restore) gives the counter reconciliation.

## Artifact hashes

The author's bench packet holds scripts, transcripts, analyses and `MANIFEST.sha256`.

`RAW-ARTIFACTS.json` there indexes every raw capture by size and SHA-256.

Raw captures stay outside the packet and the repository.

Retention follows [TESTING section 6b](../testing/TESTING.md#6b-bench-evidence-retention).

| Image artifact | Bytes | SHA-256 |
|---|---|---|
| `gateware/alinx_ax7101.bit` | 3825992 | `690d87e407bbb7f7bba52bbe7a7e0dc85cd264df2db5eec87bfaf85f99bda24b` |
| bitstream payload | 3825788 | `6597f7a601ddb3dbba1bf058c38716277e8feb1147fb89edcf1d39e755dc369f` |
| `aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `csr.csv` | 9033 | `7723d0b8129df7b77b3b49980366f18c91adb15f8c38526f48a5ebd32d1207a2` |

{{tools}}

The baseline observation ran an earlier `b2_action.py`, whose pre-window wait counted host time.

Every bind, unbind, cycle and restore ran the revision above.

{{raw-binds}}
