<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Listener withdrawal and reconnect restart on the 13eda870 image

Refs #608 and #75. Operator [A440], measured 2026-09-29, under the
[bench lane B2 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413).

The image carries processor pin `c951a9ff`, adopted by [PR #613](https://github.com/kebag-logic/milan-fpga/pull/613).

That pin defers the processor's own LeaveAll aging to transmit acceptance.

| Issue item | Verdict | Evidence |
|---|---|---|
| #608 item 1: attribute cycles 13, 24 and 75 | Not a bench item | PR #604 round 3 and the [A10] analysis on #608. |
| #608 item 2: reproduce in simulation | Not a bench item | PR #613's CRF STREAM_STOP regression. |
| #608 item 3: stop within one PDU of the withdrawal, 100 of 100 | Two readings; see below | Literal text: NOT MET, 99 of 100. Recorded reading, a withdrawal that reaches an IN registrar: PASS, 99 of 99. |
| #608 item 3: STREAM_STOP counts each stop | PASS, 99 of 99 | Every stop counted STREAM_STOP +1; cycle 22 counted +0, matching no stop. |
| #608: non-stop holds | 1 of 100 | Cycle 22. Image `9e9954e9` had 3 of 100. See [Cycle 22](#cycle-22). |
| #75: first valid AVTP PDU within 1 s of a reconnect | PASS, 99 of 99 demonstrated restarts | Maximum 0.139247 s. See [Restart distribution and growth](#restart-distribution-and-growth). |
| #75: restart latency does not grow | PASS | The 95% slope interval includes zero; ten-cycle blocks stay flat. |
| #75: firmware, topology, capture and distribution documented | PASS | This page. |
| #75: at least 100 physical restarts, DUT talker | NOT MET, 99 of 100 | Cycle 22 never stopped, so it is not a restart. |

These are operator measurements, not review verdicts.

**The two readings of #608 item 3 need a decision; this page does not choose.**

The item's text asks for 100 of 100 stops within one PDU period.

The [#608 decision](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5860869482) reads it as withdrawals reaching an IN registrar.

It keeps the documented LV + rLv behavior for a genuine LeaveAll cycle.

Cycle 22 is such a cycle, and its stream ran through the whole 2 s hold.

The [#606 page](606_FIRST_BIND_MEASUREMENT.md) records the same session's first binds.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, the bound pair and the bench as found.
- **[Method](#method)** -- The cycle, the stop and restart predicates, and how the registrar state is read.
- **[Withdrawal and stop](#withdrawal-and-stop)** -- #608: where each withdrawal landed and whether the stream stopped.
- **[Cycle 22](#cycle-22)** -- The one non-stop hold, event by event.
- **[Restart distribution and growth](#restart-distribution-and-growth)** -- #75: restart times, their growth and the MSRP rate.
- **[Per-cycle results](#per-cycle-results)** -- One row per cycle.
- **[Counters and restore](#counters-and-restore)** -- Counter reconciliation and the restored bench.
- **[Limits](#limits)** -- What this bench run does not show.
- **[Artifact hashes](#artifact-hashes)** -- Tool and raw-capture identities.

## Identity and setup

The image is dev `13eda870d1a6cf3f946fc228a98862366b08d102`, seed `eto`.

The identity gate passed before any bind.

VERSION read `0x00020060`, and the ROM, QSPI and AEM CRCs matched.

Those were `acad92b9`, `d84bce7b` and `93742dd2`.

ENTITY and CONFIGURATION matched the AEM image byte for byte.

The UART grader passed 10 of 10.

The [#606 page](606_FIRST_BIND_MEASUREMENT.md#identity-and-setup) gives the full identity and image hashes.

Topology: the DUT, the inline tap, the bench AVB switch, the reference peer.

The switch is the adjacent bridge and the grandmaster.

| Binding | Talker output | Listener input | Format |
|---|---|---|---|
| DUT talker | DUT Stream Output 1, stream `0200000000010001` | Reference peer Stream Input 8 | CRF `041060010000bb80` |

The [#606 page](606_FIRST_BIND_MEASUREMENT.md)'s fifth bind left this pair bound for cycle 1.

Both clock selections stayed INTERNAL; no rate, format or configuration changed.

## Method

The method is [PR #604's](75_RECONNECT_RESTART_MEASUREMENT.md#method), on the DUT-talker pair only.

**Cycle.** Each cycle takes its own bench-lock window.

- Read the DUT console and the controller counters.
- Capture about 3 s of tap; the stream must be flowing.
- Send `DISCONNECT_RX` to the listener; wait 2 s after its success.
- Send `CONNECT_RX`; wait for the first valid PDU, then 3 s more.
- Cap the restart observation at 30 s.
- Read the console and the counters again.

The console must read `SYNC=1 ASCAPABLE=1 TU=0` before and after.

Ten consecutive restarts over 1 s would stop the series; that never happened.

The tap pre-window is not conditioned on any MSRP event.

So each withdrawal falls at a random phase of both LeaveAll timers.

**Withdrawal.** The bridge's Listener `Lv` for the stream is found on the tap.

**#608 stop.** A cycle stops within one PDU when no valid PDU follows `Lv` + 2 ms.

The window ends at the reconnect response.

**Registrar state at the `Lv`.** The processor keeps
[Δ13](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/c951a9ff0cb5851fb159d33e966e5a2a9a188fe3/docs/architecture/10_srp_engine.md) outside a LeaveAll cycle.

There, `Lv` on an IN registrar unregisters at once.

After a Listener-type LeaveAll the registrar is LV until the bridge re-declares.

An `Lv` in that window keeps LV until `T-MRP-LEAVE`, 4.5-7.5 s.

Each cycle is classified from the capture, in event order:

- **IN, observed.** A bridge declaration of the stream follows the last LeaveAll and precedes the `Lv`.
- **IN, inferred.** The capture holds no LeaveAll and no declaration before the `Lv`.
- **LV.** A LeaveAll precedes the `Lv` with no re-declaration between them.
- **LV** also applies when an own LeaveAll frame follows the `Lv` within 1 ms.

That last rule allows for the applicant walk before an own LeaveAll frame.

The inference needs a bound, measured here on every capture.

{{inference}}

**#75 restart.** A restart must first show a stopped stream.

No valid PDU may fall from the disconnect response + 0.5 s to the reconnect response.

The restart interval runs from the tapped `CONNECT_RX` response to the first valid PDU.

The validity predicate is the one on the #606 page.

The tap clock, the unwrap and the 2 ms cadence limit are as there.

## Withdrawal and stop

- **Stops.** {{stop_within}} of 100 cycles stopped within one PDU of the `Lv`.
- The bridge's `Lv` crossed the tap {{lv_range}} s after the disconnect response.
- In stopped cycles the last PDU fell {{last_after_lv}} the `Lv`.
- That is {{last_after_disc}} after the disconnect response.
- No `DISCONNECT_TX` crossed the tap; the bridge's `Lv` precedes each stop.
- **Registrar state.** {{classes}}.
- Every withdrawal that reached an IN registrar stopped within one PDU.
- **Non-stop holds.** One: cycle 22, whose `Lv` reached an LV registrar.

Cycles whose own LeaveAll crossed the tap within 0.25 s of the `Lv`:

{{near}}

- Cycles 20, 21 and 88 sent their own LeaveAll after the `Lv`.
- Each came within one join period, at most 0.24 s.
- So the own timer may have expired before the `Lv`.
- That is the window processor PR 130 moved; all three stopped.
- The tap cannot show when a timer expired.
- Cycles 35, 45, 60 and 73 had own LeaveAlls before the `Lv`.
- In each the bridge re-declared before its `Lv`, so the registrar was IN again.
- Only cycle 22 had no re-declaration between its own LeaveAll and the `Lv`.

## Cycle 22

Seconds after the tapped `DISCONNECT_RX` response.

| Event | Time, s |
|---|---|
| Bridge LeaveAll, with its Listener `JoinMt` for the stream in the same MRPDU | -0.391721 |
| DUT's own MSRP LeaveAll, all four types, with its Talker Advertise `JoinMt` | +0.009401 |
| Bridge Listener `Lv` for the stream | +0.010791 |
| `CONNECT_RX` command | +2.000278 |
| `CONNECT_RX` response | +2.008674 |
| Reference peer's `PROBE_TX`; DUT answers SUCCESS | +2.008700; +2.008708 |
| Bridge Listener `New`, Ready | +2.020318 |

- The own LeaveAll left 1.390 ms before the bridge's `Lv` crossed the tap.
- The DUT's registrar was therefore LV when the `Lv` arrived.
- The stream carried 1,005 valid PDUs from disconnect response to reconnect response.
- Their spacing stayed 2.000012-2.000053 ms, with continuous sequence and timestamps.
- STREAM_START and STREAM_STOP both moved +0.
- The reconnect's `New` re-registered the Listener before any leave timer could expire.
- A stop at `T-MRP-LEAVE`, 4.5-7.5 s after the LeaveAll, is documented, not observed.

## Restart distribution and growth

All values are seconds; p95 uses nearest rank.

{{distribution}}

- Cycles 1, 4 and 44 each followed a pause of more than 15 s.
- In them the DUT withdrew its Talker Advertise in the hold.
- It re-declared after the reconnect probe, adding up to one join period.
- On image `9e9954e9` the median was 0.019175 s and the maximum 0.117736 s.

Growth uses the 99 demonstrated restarts against their original cycle numbers.

{{growth}}

The interval uses ordinary least squares and Student's t.

It assumes independent errors with constant variance.

{{blocks}}

Combined MSRP stays near two PDUs per second; no re-declaration storm appears.

## Per-cycle results

"Hold PDUs" counts valid PDUs from the disconnect response to the reconnect response.

It includes the few before the `Lv`.

"Last PDU minus Lv" in a stopped cycle is the last PDU before the stop.

"DUT TA declared in hold" counts `New`, `JoinIn` or `JoinMt` from the DUT.

{{cycles}}

## Counters and restore

DUT Stream Output 1 STREAM_START and STREAM_STOP, from GET_COUNTERS:

| Point | START / STOP |
|---|---|
| Start census | 11 / 11 |
| Five first binds | +5 / +0 |
| Four unbinds between binds | +0 / +4 |
| 100 cycles | +{{ss_start}} / +{{ss_stop}} |
| Restore unbind | +0 / +1 |
| End census | 115 / 115 |

Every demonstrated restart added one of each; cycle 22 added none.

The AVB_INTERFACE counters did not move over the session.

The DUT kept LINK_UP 12, LINK_DOWN 11 and GPTP_GM_CHANGED 50.

Restore, all proven:

- The pair was unbound on the first attempt; the stream stopped within one PDU.
- All 18 stream states read connection count 0.
- The start and end censuses agree on all 53 non-counter reads.
- A final 16.9 s tap capture carried no CRF PDU.
- The UART grader passed 10 of 10; the reset epoch read 1 throughout.
- The temporary controller and capture scripts were removed.
- The temporary capture module was unloaded and its build removed.
- Outlets read as lane B1 left them; this lane switched none.
- The bench lock was verified free.

## Limits

- The 2 s hold cannot show when an LV registration expires.
- Cycle 22's stop time without a reconnect is therefore not measured.
- The inferred IN class rests on the measured re-declaration bound above.
- Cycle 22 is one LV-window cycle; 100 cycles bound its rate only coarsely.
- The reference peer's own link is behind the bridge and not tapped.
- Only CRF was measured; AAF restart remains unmeasured.
- Printed precision is not a calibrated timestamp accuracy.

## Artifact hashes

The author's bench packet holds scripts, transcripts, analyses and `MANIFEST.sha256`.

`RAW-ARTIFACTS.json` there indexes every raw capture by size and SHA-256.

Raw captures stay outside the packet and the repository.

Tools are listed on the [#606 page](606_FIRST_BIND_MEASUREMENT.md#artifact-hashes).

Retention follows [TESTING section 6b](../testing/TESTING.md#6b-bench-evidence-retention).

{{raw-cycles}}
