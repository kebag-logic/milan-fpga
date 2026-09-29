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
| #608 item 3: stop within one PDU of the withdrawal | 99 of 99 withdrawals that reached an IN registrar stopped; qualified | Graded under the [corrected ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5886425487). Cycle 22's LV registrar is attributed to the processor #108 deviation. Met without qualification only after the pin adoption of processor PR #133 and a bench re-run. |
| #608 item 3: STREAM_STOP counts each stop | PASS, 99 of 99 | Every stop counted STREAM_STOP +1; cycle 22 counted +0, matching no stop. |
| #608: non-stop holds | 1 of 100 | Cycle 22. Image `9e9954e9` had 3 of 100. See [Cycle 22](#cycle-22). |
| #75: first valid AVTP PDU within 1 s of a reconnect | PASS, 99 of 99 demonstrated restarts | Maximum 0.139247 s. See [Restart distribution and growth](#restart-distribution-and-growth). |
| #75: restart latency does not grow | PASS | The 95% slope interval includes zero; ten-cycle blocks stay flat. |
| #75: firmware, topology, capture and distribution documented | PASS | This page. |
| #75: at least 100 physical cycles resume within 1 s, DUT talker | Met under the ruling: 100 cycles, 99 of 99 demonstrated restarts | Cycle 22 never stopped, so it is not a restart. The [#608 ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887) requires no additional cycle. |

These are operator measurements, not review verdicts.

**The reading of #608 item 3 is decided.**

- The [ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887) sets the bar at a withdrawal that reaches an IN registrar.
- Its [correction](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5886425487) grades this image: 99 of 99 such withdrawals stopped within one PDU.
- Cycle 22's non-stop is attributed to the processor [#108](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/108) deviation, not accepted as standard behavior.
- Processor [PR #133](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/133) implements the leavealltimer restart that #108 lacks.
- #608 item 3 is met without qualification only after the pin adoption of #133 and a 100-cycle re-run.
- Processor [#134](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/134) grades the LV-registrar stop in simulation.
- It stands after #133, because a peer can also open an LV window.

History: read literally, the item's text asks for 100 of 100; this run is 99 of 100.

The earlier [#608 decision](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5860869482) first stated the IN-registrar reading.

It kept the documented LV + rLv behavior for a genuine LeaveAll cycle.

Cycle 22 is a LeaveAll cycle, but not a genuine one in that sense.

A conformant participant would have suppressed the DUT LeaveAll that opened it; see [Cycle 22](#cycle-22).

The [#606 page](606_FIRST_BIND_MEASUREMENT.md) records the same session's first binds.

## Contents

- **[Identity and setup](#identity-and-setup)** -- The image, the bound pair and the bench as found.
- **[Method](#method)** -- The cycle, the stop and restart predicates, and how the registrar state is read.
- **[Withdrawal and stop](#withdrawal-and-stop)** -- #608: where each withdrawal landed and whether the stream stopped.
- **[Cycle 22](#cycle-22)** -- The one non-stop hold, event by event, and the processor deviation that opened its LV window.
- **[Restart distribution and growth](#restart-distribution-and-growth)** -- #75: restart times, their growth and the MSRP rate.
- **[Per-cycle results](#per-cycle-results)** -- One row per cycle.
- **[Counters and restore](#counters-and-restore)** -- Counter reconciliation, the restored bench and the DUT's saved-state layer.
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

The bridge re-declared the stream within 0.088 s of every Listener-type LeaveAll seen while registered.

That covers 110 LeaveAlls: 53 own and 57 from the bridge; none went unanswered.

Every capture holds at least 2.742 s before its `Lv`.

So an `Lv` with no LeaveAll in its capture came long after the last re-declaration.

**#75 restart.** A restart must first show a stopped stream.

No valid PDU may fall from the disconnect response + 0.5 s to the reconnect response.

The restart interval runs from the tapped `CONNECT_RX` response to the first valid PDU.

The validity predicate is the one on the #606 page.

The tap clock, the unwrap and the 2 ms cadence limit are as there.

## Withdrawal and stop

- **Stops.** 99 of 100 cycles stopped within one PDU of the `Lv`.
- The bridge's `Lv` crossed the tap 0.008466-0.098486 s after the disconnect response.
- In stopped cycles the last PDU fell between 1.974 ms before and 0.001 ms after the `Lv`.
- That is 0.006858-0.097036 s, median 0.008363 s, after the disconnect response.
- No `DISCONNECT_TX` crossed the tap; the bridge's `Lv` precedes each stop.
- **Registrar state.** 42 IN observed, 57 IN inferred and 1 LV.
- Every withdrawal that reached an IN registrar stopped within one PDU.
- **Non-stop holds.** One: cycle 22, whose `Lv` reached an LV registrar.

Cycles whose own LeaveAll crossed the tap within 0.25 s of the `Lv`:

| Cycle | Own LeaveAll minus bridge Lv, s | Registrar at Lv | Stop |
|---|---|---|---|
| 20 | +0.202894 | IN (observed) | stop within one PDU |
| 21 | +0.118613 | IN (observed) | stop within one PDU |
| 22 | -0.001391 | LV | non-stop hold |
| 35 | -0.099666 | IN (observed) | stop within one PDU |
| 45 | -0.242494 | IN (observed) | stop within one PDU |
| 60 | -0.191188 | IN (observed) | stop within one PDU |
| 73 | -0.091847 | IN (observed) | stop within one PDU |
| 88 | +0.199699 | IN (observed) | stop within one PDU |

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

**Why the registrar was LV.** A DUT-side deviation opened the LV window.

- The bridge's LeaveAll at -0.391721 s carried its Listener `JoinMt`, so the registrar was IN after it.
- The DUT's own LeaveAll, for all four types, followed 0.401121 s later.
- 802.1Q-2014 Table 10-5 (10.7.9) maps a received LeaveAll to "Start leavealltimer".
- Clause 10.6: that restart suppresses multiple LeaveAll messages on one LAN.
- A participant's leavealltimer draws 10-15 s, ± 0.5 s (Milan v1.2 Table 4.3).
- So a conformant participant sends no LeaveAll within 9.5 s of a received one.
- The processor at `c951a9ff` re-arms its own timer only at its own expiry; a received LeaveAll does not restart it.
- Its [SRP engine design](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/c951a9ff0cb5851fb159d33e966e5a2a9a188fe3/docs/architecture/10_srp_engine.md), section 6.5, records this as an open deviation.
- Processor [#108](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/108) tracks it.
- A conformant DUT would not have sent this LeaveAll.
- The `Lv` would then have met an IN registrar, and Δ13 would have stopped the stream.
- The rLv in LV that followed is standard behavior (802.1Q-2014 Table 10-4); the LV state came from the deviation.

The deviation recurs across the session:

- 67 DUT LeaveAlls, in 64 of the 112 captures, came less than 10 s after a received bridge LeaveAll.
- The gaps ran 0.199564-4.807277 s, median 1.997469 s; 14 were under 1 s.
- Only pairs inside one capture are seen, so these counts are lower bounds.
- Processor PR #133 adds the restart; processor #134 grades the LV-registrar stop.

## Restart distribution and growth

All values are seconds; p95 uses nearest rank.

| Population | Count | Below 1 s | Min, s | Median, s | p95, s | Max, s |
|---|---|---|---|---|---|---|
| Demonstrated restarts | 99 | 99 | 0.011239 | 0.013195 | 0.081912 | 0.139247 |
| DUT Talker Advertise held through the hold | 96 | 96 | 0.011239 | 0.013143 | - | 0.101353 |
| DUT Talker Advertise withdrawn in the hold | 3 | 3 | 0.105876 | 0.126519 | - | 0.139247 |

- Cycles 1, 4 and 44 each followed a pause of more than 15 s.
- In them the DUT withdrew its Talker Advertise in the hold.
- It re-declared after the reconnect probe, adding up to one join period.
- On image `9e9954e9` the median was 0.019175 s and the maximum 0.117736 s.

Growth uses the 99 demonstrated restarts against their original cycle numbers.

| First ten median, s | Last ten median, s | Slope, s per cycle | 95% slope interval, s per cycle | Residual df |
|---|---|---|---|---|
| 0.013168 | 0.013255 | -0.000082801 | [-0.000234887, +0.000069285] | 97 |

The interval uses ordinary least squares and Student's t.

It assumes independent errors with constant variance.

| Cycles | Demonstrated restarts | Median, s | Max, s | Combined MSRP PDUs/s |
|---|---|---|---|---|
| 1-10 | 10 | 0.013168 | 0.126519 | 1.914 |
| 11-20 | 10 | 0.013282 | 0.014413 | 2.023 |
| 21-30 | 9 | 0.013361 | 0.014128 | 1.887 |
| 31-40 | 10 | 0.012941 | 0.013640 | 1.947 |
| 41-50 | 10 | 0.013580 | 0.139247 | 2.068 |
| 51-60 | 10 | 0.013396 | 0.081912 | 1.900 |
| 61-70 | 10 | 0.012278 | 0.015254 | 2.025 |
| 71-80 | 10 | 0.013289 | 0.015567 | 1.933 |
| 81-90 | 10 | 0.012856 | 0.014272 | 1.764 |
| 91-100 | 10 | 0.013255 | 0.101353 | 2.037 |

Combined MSRP stays near two PDUs per second; no re-declaration storm appears.

## Per-cycle results

"Hold PDUs" counts valid PDUs from the disconnect response to the reconnect response.

It includes the few before the `Lv`.

"Last PDU minus Lv" in a stopped cycle is the last PDU before the stop.

"DUT TA declared in hold" counts `New`, `JoinIn` or `JoinMt` from the DUT.

| Cycle | Bridge Lv after disconnect, s | Registrar at Lv | Last PDU minus Lv, ms | Hold PDUs | START / STOP | DUT TA declared in hold | Restart, s | #608 stop | #75 restart |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.008466 | IN (inferred) | -0.525 | 4 | +1 / +1 | no | 0.105876 | PASS | PASS |
| 2 | 0.009184 | IN (inferred) | -1.176 | 5 | +1 / +1 | yes | 0.014236 | PASS | PASS |
| 3 | 0.009582 | IN (inferred) | -1.385 | 5 | +1 / +1 | yes | 0.012014 | PASS | PASS |
| 4 | 0.009435 | IN (inferred) | -0.897 | 5 | +1 / +1 | no | 0.126519 | PASS | PASS |
| 5 | 0.009216 | IN (observed) | -0.601 | 5 | +1 / +1 | yes | 0.013848 | PASS | PASS |
| 6 | 0.009562 | IN (inferred) | -0.763 | 5 | +1 / +1 | yes | 0.012657 | PASS | PASS |
| 7 | 0.008820 | IN (inferred) | -1.962 | 4 | +1 / +1 | yes | 0.012462 | PASS | PASS |
| 8 | 0.009189 | IN (inferred) | -0.137 | 5 | +1 / +1 | yes | 0.013260 | PASS | PASS |
| 9 | 0.009597 | IN (inferred) | -0.360 | 5 | +1 / +1 | yes | 0.013076 | PASS | PASS |
| 10 | 0.009612 | IN (inferred) | -0.183 | 5 | +1 / +1 | yes | 0.012888 | PASS | PASS |
| 11 | 0.009171 | IN (observed) | -1.678 | 4 | +1 / +1 | yes | 0.013670 | PASS | PASS |
| 12 | 0.013235 | IN (observed) | -0.553 | 7 | +1 / +1 | yes | 0.014413 | PASS | PASS |
| 13 | 0.008929 | IN (inferred) | -0.184 | 5 | +1 / +1 | yes | 0.012221 | PASS | PASS |
| 14 | 0.009328 | IN (inferred) | -1.399 | 4 | +1 / +1 | yes | 0.014034 | PASS | PASS |
| 15 | 0.008671 | IN (inferred) | -0.548 | 5 | +1 / +1 | yes | 0.011846 | PASS | PASS |
| 16 | 0.008856 | IN (inferred) | -0.669 | 5 | +1 / +1 | yes | 0.011662 | PASS | PASS |
| 17 | 0.026166 | IN (inferred) | -0.664 | 13 | +1 / +1 | yes | 0.013470 | PASS | PASS |
| 18 | 0.009703 | IN (observed) | -0.138 | 5 | +1 / +1 | yes | 0.014279 | PASS | PASS |
| 19 | 0.009080 | IN (observed) | -1.323 | 4 | +1 / +1 | yes | 0.013093 | PASS | PASS |
| 20 | 0.009355 | IN (observed) | -0.537 | 5 | +1 / +1 | yes | 0.012903 | PASS | PASS |
| 21 | 0.008708 | IN (observed) | -0.706 | 5 | +1 / +1 | yes | 0.013730 | PASS | PASS |
| 22 | 0.010791 | LV | +1997.430 | 1005 | +0 / +0 | yes | none: no stop | LV window, no stop | NOT RESTART |
| 23 | 0.009307 | IN (observed) | -0.048 | 5 | +1 / +1 | yes | 0.013361 | PASS | PASS |
| 24 | 0.009690 | IN (inferred) | -0.245 | 5 | +1 / +1 | yes | 0.013176 | PASS | PASS |
| 25 | 0.009062 | IN (inferred) | -1.425 | 4 | +1 / +1 | yes | 0.013987 | PASS | PASS |
| 26 | 0.009425 | IN (observed) | -1.603 | 4 | +1 / +1 | yes | 0.013804 | PASS | PASS |
| 27 | 0.009251 | IN (observed) | -0.357 | 5 | +1 / +1 | yes | 0.013016 | PASS | PASS |
| 28 | 0.009478 | IN (observed) | -0.522 | 5 | +1 / +1 | yes | 0.012834 | PASS | PASS |
| 29 | 0.009428 | IN (inferred) | -1.276 | 5 | +1 / +1 | yes | 0.014128 | PASS | PASS |
| 30 | 0.008830 | IN (inferred) | -0.491 | 5 | +1 / +1 | yes | 0.011938 | PASS | PASS |
| 31 | 0.009656 | IN (inferred) | -0.255 | 5 | +1 / +1 | yes | 0.013640 | PASS | PASS |
| 32 | 0.009566 | IN (inferred) | -1.974 | 4 | +1 / +1 | yes | 0.013450 | PASS | PASS |
| 33 | 0.008950 | IN (inferred) | -1.169 | 4 | +1 / +1 | yes | 0.013227 | PASS | PASS |
| 34 | 0.009357 | IN (inferred) | -0.500 | 5 | +1 / +1 | yes | 0.013037 | PASS | PASS |
| 35 | 0.098486 | IN (observed) | -1.450 | 49 | +1 / +1 | yes | 0.012844 | PASS | PASS |
| 36 | 0.009333 | IN (observed) | -0.111 | 5 | +1 / +1 | yes | 0.012653 | PASS | PASS |
| 37 | 0.009327 | IN (inferred) | -0.034 | 5 | +1 / +1 | yes | 0.013394 | PASS | PASS |
| 38 | 0.008689 | IN (inferred) | -0.212 | 5 | +1 / +1 | yes | 0.012207 | PASS | PASS |
| 39 | 0.009069 | IN (inferred) | -0.402 | 5 | +1 / +1 | yes | 0.012027 | PASS | PASS |
| 40 | 0.009323 | IN (observed) | -0.594 | 5 | +1 / +1 | yes | 0.012802 | PASS | PASS |
| 41 | 0.008713 | IN (observed) | -0.794 | 4 | +1 / +1 | yes | 0.011607 | PASS | PASS |
| 42 | 0.009168 | IN (observed) | -1.059 | 5 | +1 / +1 | yes | 0.013442 | PASS | PASS |
| 43 | 0.009451 | IN (inferred) | -1.271 | 5 | +1 / +1 | yes | 0.016165 | PASS | PASS |
| 44 | 0.008967 | IN (observed) | -0.183 | 5 | +1 / +1 | no | 0.139247 | PASS | PASS |
| 45 | 0.008790 | IN (observed) | -0.810 | 4 | +1 / +1 | yes | 0.013574 | PASS | PASS |
| 46 | 0.009342 | IN (observed) | -1.173 | 5 | +1 / +1 | yes | 0.014273 | PASS | PASS |
| 47 | 0.008519 | IN (inferred) | -0.292 | 5 | +1 / +1 | yes | 0.012084 | PASS | PASS |
| 48 | 0.010018 | IN (inferred) | -1.598 | 5 | +1 / +1 | yes | 0.013863 | PASS | PASS |
| 49 | 0.009335 | IN (inferred) | -1.852 | 4 | +1 / +1 | yes | 0.013587 | PASS | PASS |
| 50 | 0.010345 | IN (observed) | -1.669 | 5 | +1 / +1 | yes | 0.012280 | PASS | PASS |
| 51 | 0.009191 | IN (inferred) | -1.329 | 4 | +1 / +1 | yes | 0.013069 | PASS | PASS |
| 52 | 0.009676 | IN (inferred) | -1.621 | 5 | +1 / +1 | yes | 0.011782 | PASS | PASS |
| 53 | 0.008948 | IN (inferred) | -0.825 | 5 | +1 / +1 | yes | 0.013597 | PASS | PASS |
| 54 | 0.011162 | IN (inferred) | -0.838 | 6 | +1 / +1 | yes | 0.014363 | PASS | PASS |
| 55 | 0.009709 | IN (observed) | -0.338 | 5 | +1 / +1 | yes | 0.013110 | PASS | PASS |
| 56 | 0.009082 | IN (observed) | -0.522 | 5 | +1 / +1 | yes | 0.081912 | PASS | PASS |
| 57 | 0.009568 | IN (observed) | -1.814 | 4 | +1 / +1 | yes | 0.013605 | PASS | PASS |
| 58 | 0.008813 | IN (inferred) | -0.998 | 4 | +1 / +1 | yes | 0.011382 | PASS | PASS |
| 59 | 0.009083 | IN (inferred) | -0.205 | 5 | +1 / +1 | yes | 0.013195 | PASS | PASS |
| 60 | 0.085791 | IN (observed) | -1.849 | 42 | +1 / +1 | yes | 0.013936 | PASS | PASS |
| 61 | 0.009797 | IN (observed) | -1.789 | 5 | +1 / +1 | yes | 0.011733 | PASS | PASS |
| 62 | 0.009195 | IN (inferred) | +0.001 | 5 | +1 / +1 | yes | 0.013428 | PASS | PASS |
| 63 | 0.009404 | IN (inferred) | -0.147 | 5 | +1 / +1 | yes | 0.015254 | PASS | PASS |
| 64 | 0.009701 | IN (inferred) | -1.375 | 5 | +1 / +1 | yes | 0.012037 | PASS | PASS |
| 65 | 0.009125 | IN (inferred) | -0.613 | 5 | +1 / +1 | yes | 0.011839 | PASS | PASS |
| 66 | 0.009334 | IN (inferred) | -0.763 | 5 | +1 / +1 | yes | 0.012665 | PASS | PASS |
| 67 | 0.008673 | IN (inferred) | -0.030 | 5 | +1 / +1 | yes | 0.012370 | PASS | PASS |
| 68 | 0.009701 | IN (observed) | -0.870 | 5 | +1 / +1 | yes | 0.012187 | PASS | PASS |
| 69 | 0.009301 | IN (observed) | -1.410 | 4 | +1 / +1 | yes | 0.014001 | PASS | PASS |
| 70 | 0.008739 | IN (inferred) | -0.652 | 5 | +1 / +1 | yes | 0.011782 | PASS | PASS |
| 71 | 0.009255 | IN (inferred) | -0.109 | 5 | +1 / +1 | yes | 0.013502 | PASS | PASS |
| 72 | 0.009444 | IN (inferred) | -0.106 | 5 | +1 / +1 | yes | 0.013312 | PASS | PASS |
| 73 | 0.047490 | IN (observed) | -1.082 | 24 | +1 / +1 | yes | 0.014509 | PASS | PASS |
| 74 | 0.009539 | IN (observed) | -1.068 | 5 | +1 / +1 | yes | 0.012334 | PASS | PASS |
| 75 | 0.008913 | IN (inferred) | -1.253 | 4 | +1 / +1 | yes | 0.015142 | PASS | PASS |
| 76 | 0.009172 | IN (inferred) | -1.449 | 4 | +1 / +1 | yes | 0.012948 | PASS | PASS |
| 77 | 0.009661 | IN (observed) | -0.873 | 5 | +1 / +1 | yes | 0.012757 | PASS | PASS |
| 78 | 0.008820 | IN (observed) | -0.844 | 4 | +1 / +1 | yes | 0.015567 | PASS | PASS |
| 79 | 0.009175 | IN (inferred) | -0.137 | 5 | +1 / +1 | yes | 0.013266 | PASS | PASS |
| 80 | 0.009483 | IN (inferred) | -0.377 | 5 | +1 / +1 | yes | 0.013048 | PASS | PASS |
| 81 | 0.008858 | IN (inferred) | -0.565 | 5 | +1 / +1 | yes | 0.011778 | PASS | PASS |
| 82 | 0.009700 | IN (inferred) | -1.338 | 5 | +1 / +1 | yes | 0.012085 | PASS | PASS |
| 83 | 0.009205 | IN (observed) | -1.656 | 4 | +1 / +1 | yes | 0.013783 | PASS | PASS |
| 84 | 0.008795 | IN (inferred) | -1.068 | 4 | +1 / +1 | yes | 0.013326 | PASS | PASS |
| 85 | 0.009089 | IN (inferred) | -0.301 | 5 | +1 / +1 | yes | 0.012139 | PASS | PASS |
| 86 | 0.009296 | IN (observed) | -0.450 | 5 | +1 / +1 | yes | 0.012952 | PASS | PASS |
| 87 | 0.008618 | IN (observed) | -1.577 | 4 | +1 / +1 | yes | 0.012761 | PASS | PASS |
| 88 | 0.008830 | IN (observed) | -1.852 | 4 | +1 / +1 | yes | 0.013567 | PASS | PASS |
| 89 | 0.009413 | IN (observed) | -1.121 | 5 | +1 / +1 | yes | 0.014272 | PASS | PASS |
| 90 | 0.009698 | IN (inferred) | -1.340 | 5 | +1 / +1 | yes | 0.012087 | PASS | PASS |
| 91 | 0.009120 | IN (observed) | -0.573 | 5 | +1 / +1 | yes | 0.011862 | PASS | PASS |
| 92 | 0.010473 | IN (observed) | -0.864 | 5 | +1 / +1 | yes | 0.013592 | PASS | PASS |
| 93 | 0.008951 | IN (observed) | -1.150 | 4 | +1 / +1 | yes | 0.101353 | PASS | PASS |
| 94 | 0.009105 | IN (inferred) | -1.243 | 4 | +1 / +1 | yes | 0.013109 | PASS | PASS |
| 95 | 0.008945 | IN (inferred) | -1.008 | 4 | +1 / +1 | yes | 0.013400 | PASS | PASS |
| 96 | 0.009328 | IN (inferred) | -1.204 | 5 | +1 / +1 | yes | 0.014195 | PASS | PASS |
| 97 | 0.008826 | IN (observed) | -0.515 | 5 | +1 / +1 | yes | 0.011917 | PASS | PASS |
| 98 | 0.008930 | IN (observed) | -1.679 | 4 | +1 / +1 | yes | 0.012731 | PASS | PASS |
| 99 | 0.009393 | IN (observed) | -0.954 | 5 | +1 / +1 | yes | 0.014426 | PASS | PASS |
| 100 | 0.008779 | IN (inferred) | -1.149 | 4 | +1 / +1 | yes | 0.011239 | PASS | PASS |

## Counters and restore

DUT Stream Output 1 STREAM_START and STREAM_STOP, from GET_COUNTERS:

| Point | START / STOP |
|---|---|
| Start census | 11 / 11 |
| Five first binds | +5 / +0 |
| Four unbinds between binds | +0 / +4 |
| 100 cycles | +99 / +99 |
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
- The DUT's saved-state layer read the same at start and end; see [Saved-state layer](#saved-state-layer).

### Saved-state layer

The census compares AEM state only; the DUT's saved-state status read the same at start and end.

| Saved-state field | Identity gate, 06:49:58Z | Final restore, 07:20:45Z |
|---|---|---|
| NVM slots A / B, image sequence | 229 / 230, image 230 | 229 / 230, image 230 |
| Records, writer | 53 records, 3,264 B, writer live | 53 records, 3,264 B, writer live |
| Commits ok / failed | 2 / 0 | 2 / 0 |
| `PP_STAT`, `nvm_pend` (bit 11) | `0x5b000c44`, 1 | `0x5b000c44`, 1 |
| `PP_NVM_STAT` | `0xc34000e4`, pend 1 | `0xc34000e4`, pend 1 |

- No bind, unbind or cycle in this lane wrote a saved-state record, so no commit ran.
- The binding records are indexed by the DUT's stream inputs; this lane bound only its Stream Output 1.
- `nvm_pend` = 1 was inherited from lane B1; its final restore on [PR #620](https://github.com/kebag-logic/milan-fpga/pull/620) reads the same slots, commits, `PP_STAT` and `PP_NVM_STAT`.
- Between the two reads the console samples carry `PP_STAT` alone, not `PP_NVM_STAT` or the commit count.
- The persisted records were not read back or compared with the found state.

The [#606 page](606_FIRST_BIND_MEASUREMENT.md#saved-state-layer) gives the derivation and the cause.

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

| Capture identifier | Bytes | SHA-256 |
|---|---|---|
| `cycle-001/tap.pcap` | 349536 | `1fdba3dae337d388947cf4015f151e81e1269b1ba9619c04e3b90fe2491733f3` |
| `cycle-002/tap.pcap` | 405045 | `f746b5065b1a18d98e6a4267d7f44f1958628146e17d90f9d5b74912403b7a3b` |
| `cycle-003/tap.pcap` | 411589 | `8282488266fc6d5c5473177a3ef41765c05680a91652f0a77d2578e12dab8cc3` |
| `cycle-004/tap.pcap` | 341884 | `44bd6c243b10aff62b1e4eeb466bad367cd948d168c4ee605b626af1d91a3957` |
| `cycle-005/tap.pcap` | 411307 | `e9a288b1f2fdfbb39ca5e2e272f5d26f1933f32964f07b4de6f370b37bdf64ee` |
| `cycle-006/tap.pcap` | 410481 | `f654c5f9984a779bbbe3b5364a795df501732976e9a38b778fd4c6246f756069` |
| `cycle-007/tap.pcap` | 410035 | `550e1679c736fcb95f38d11af4474e6b8fbb5f3ab6f74e3c82601ea533268e21` |
| `cycle-008/tap.pcap` | 410597 | `178c53344c9cdffa0414691675c05794d3e9b8545082c7d759789044e5d89874` |
| `cycle-009/tap.pcap` | 409796 | `f20ec00e7f70d6e08a0947e12a8828756c96505d3f7de03a1dc0f5db0566db56` |
| `cycle-010/tap.pcap` | 410921 | `adc74e4b6840308265454c17cfec16b86b940b3a8542a2203970e17ffb6dce11` |
| `cycle-011/tap.pcap` | 410876 | `39fa95094e3e382dffaedd24c32bce3c4aae18f78ed68bfc162cdd385936587f` |
| `cycle-012/tap.pcap` | 411149 | `ea4d8dc2630c27205b69c3cdecd9a8122050b4a13ced853d85884ac83129579c` |
| `cycle-013/tap.pcap` | 411132 | `83634d5a375d844446816f600b33bcab8cd0a19201b209225e55ba9fd9b10ddf` |
| `cycle-014/tap.pcap` | 411499 | `9567e9fff00530896799e79116039c92b36b5d39faac4af1eb36fce6c9aa241b` |
| `cycle-015/tap.pcap` | 411521 | `344d55f3bbfa96805b29cafe2b88bfa6c3ba257731969b98dcc9beffd48659ea` |
| `cycle-016/tap.pcap` | 410421 | `74096409ed265ec293ecb051dfa4c151c86b24500902356034196575a5aeb2e9` |
| `cycle-017/tap.pcap` | 411702 | `ae364ce120760debb130529bb4422bc2625aab65a2ccbeb563c2fab75452d685` |
| `cycle-018/tap.pcap` | 412957 | `7ae870a613b8eda8692de01f4d818705d4f31f86bcb01ea601fb09cee207dfa7` |
| `cycle-019/tap.pcap` | 411541 | `5f6cd26bb43e6527408a47e326092d0de1c67c52867bfb7e1061e027d2d8cfaf` |
| `cycle-020/tap.pcap` | 411283 | `e593bd7649b754d15692c5dcaaec2ec677e74d63c5d1a78c9535e05530ec94f2` |
| `cycle-021/tap.pcap` | 411925 | `4e284eb2c861ce3e0d0e7bdd41144dd486c2cfde2c8e50e1e504f509aeaedce2` |
| `cycle-022/tap.pcap` | 520915 | `e8817aa00cd49a991740c97014f79aab41d68d3d2d323b7ddd47054d1cd78634` |
| `cycle-023/tap.pcap` | 412053 | `b7fadd1b81de8aa1dc2d08d44e903a4e4292662211861808497eadfdb2653401` |
| `cycle-024/tap.pcap` | 411406 | `25f5249e25878e305938718b3832bc2093d7cc990491f3f0b835a06b24050122` |
| `cycle-025/tap.pcap` | 410388 | `19a03e353e518f393603ba6010497837a1f1e45dec28d7a01a0a2477b487b9ef` |
| `cycle-026/tap.pcap` | 352724 | `eecf47f66472189436d167131a672b3412c4ef6ac1d2fa131f1d54ae2fdcbfa4` |
| `cycle-027/tap.pcap` | 412591 | `74cf657791b7ba1d6f5a3cd6b1f1858f98a8fe016ed088d566b4b825fb8029d7` |
| `cycle-028/tap.pcap` | 354206 | `f4c3b63d9aa2668c8910303a5cd202932d940389e0f0dbece4f7ae4781eefead` |
| `cycle-029/tap.pcap` | 410208 | `778329d58b863842142375a42cad1e41d1306b6966f031b6220887e89c5ee3fc` |
| `cycle-030/tap.pcap` | 411105 | `d3b707d2524b51d0e8c69c1180b2529645a3b570e7b19477dbef45ddcb681017` |
| `cycle-031/tap.pcap` | 412665 | `cd5efc290df315a0f485511019415d374530f2edf2490b1632857bf82d6df45c` |
| `cycle-032/tap.pcap` | 412408 | `fa96e2f3b648d7f1e23c5b66ec8fa02c07afafbf0bcfae02691bffa274c180d2` |
| `cycle-033/tap.pcap` | 406523 | `7b22b966f947db7c33c210880923153f837aabc4e4a472adad88bfa713d77788` |
| `cycle-034/tap.pcap` | 411915 | `8b9f086dc2dcb41f61777eeaa465c604318e193722e2ed0a85b2acaaf5bae98c` |
| `cycle-035/tap.pcap` | 415271 | `c9b2faf23ecf07b4e3195e496eed4710ab3251bfd420619c9943918c29d6ead5` |
| `cycle-036/tap.pcap` | 410983 | `306a270225f9cdff0ecbe9bfd533058ee9bcc85c8f2a6da5d801a7cdf2437687` |
| `cycle-037/tap.pcap` | 413725 | `880060b8efd36b60dcc225bea8924c3d29e98971e2a69231679f5e83631c34a0` |
| `cycle-038/tap.pcap` | 411337 | `131c9279ca2673334e44c7215a92b6f08406e64b43b8c48da0983dbb1c345071` |
| `cycle-039/tap.pcap` | 409638 | `38533690cfef9e1a62b74d3eff02bb8533b6a24e7f7fbc972a13c5e13b427687` |
| `cycle-040/tap.pcap` | 410873 | `0536910987fc46ab9eaadd677eb09d80abf5d5e6bf8ac2378e2ab07391147309` |
| `cycle-041/tap.pcap` | 412058 | `d7c0f5789a131bd434826bc16da567f28574a71e067d97e34fcbe3c2b08db30b` |
| `cycle-042/tap.pcap` | 411079 | `b3948a9d818f9494954289680e342f8b2628c902687aed9e32a63da6f062b9e9` |
| `cycle-043/tap.pcap` | 411413 | `5442d550d936217285809111d2479f90567a75b429e76146003d177bef7316e7` |
| `cycle-044/tap.pcap` | 346718 | `e7e730e59a3c1d958136ea5a7a0aac8411d7aabd5389e163ceb209995acaf7f9` |
| `cycle-045/tap.pcap` | 410104 | `a32293a5b9676a13ddc3de9b05dcb9987e21be581cdfb933fb2c6c9a47aca5de` |
| `cycle-046/tap.pcap` | 410087 | `2adeb7cd82b01d4f53fb892ac5eadf74a27bdf46643edcdc1715c4bf7dff0e23` |
| `cycle-047/tap.pcap` | 410415 | `74a48b066dfcb7cfd663d5a344b69a1aed9bbe4ce08e7f6a086e7c3d320b64b8` |
| `cycle-048/tap.pcap` | 410057 | `6cdcce55d57a83720759f89cd8eb9477b26d6715a4824a30102ecbdfa88ad5d6` |
| `cycle-049/tap.pcap` | 409881 | `1514e767a247e55bd2933cd594292f1c72bea00d3c754a115b1b2223366eea71` |
| `cycle-050/tap.pcap` | 410272 | `81a6cb54e58553fb4da2b03c3c16bddb6e0f76b667e597d597cbad893253bbb8` |
| `cycle-051/tap.pcap` | 409926 | `1f050d07843093c2d5d1143845c310e00be417eb5f55776664f7e40ddfa6c422` |
| `cycle-052/tap.pcap` | 409027 | `a06ee651da8e55e97d6e2a1cf2183803e8fee85c40f54a7401e88e12e71d6c32` |
| `cycle-053/tap.pcap` | 409990 | `c4409d853393fadde97530920186cd3945f382beed6685bc445aaf521a81c8d7` |
| `cycle-054/tap.pcap` | 410381 | `43cc5d5cb5ada3d0316c44a25ca83ba7d324b12e3a9716de89c174014101016d` |
| `cycle-055/tap.pcap` | 409530 | `b46e288d8da02e55c1141c6ea78dc2852c35bab415f1f75840e97c5c1705cccb` |
| `cycle-056/tap.pcap` | 405891 | `d66a8567ab1a555573cb181a452cc98a957e1b9df9194a6b83a33944d4738cfb` |
| `cycle-057/tap.pcap` | 410252 | `b8fe1507cdde8ccc0e0e2a5759f2185afd5204d9634b008dec8efedb4fc74f99` |
| `cycle-058/tap.pcap` | 410143 | `f99dbf14c2ab7d5b41569eae90b751f3e6bb3a62a04340305098d6000ff5d32b` |
| `cycle-059/tap.pcap` | 409442 | `7c392eb6a971fa144625a80b8ed686c06348e1d7a8760ecd4766c8176e1d191a` |
| `cycle-060/tap.pcap` | 414372 | `172bf27d2d3728bf79cc8ab62dd7222c955209136aa941744c83c9f9c02ad46e` |
| `cycle-061/tap.pcap` | 411938 | `cf68846165cf2c123e086dde0ea144baa01dafb0e9daba10e550d801f6e6b57c` |
| `cycle-062/tap.pcap` | 410212 | `cc90330b4b7731706fdde6ad64bfcc12d09b335a0dfaf5f2b6c0b0d3883faee4` |
| `cycle-063/tap.pcap` | 409681 | `e9f68f5f483ed37f968d37e354a85394c6f9efee24fa1b11f468a18519768c24` |
| `cycle-064/tap.pcap` | 411146 | `c797d6e65f9adc402529e9e0df9bc53a8aff5f5eb4789d6cca35e98ee8e0a6c1` |
| `cycle-065/tap.pcap` | 411165 | `e57e2f57dd05352bc76131c11adba336f854c1019779da8c5842a30b0baf06e8` |
| `cycle-066/tap.pcap` | 411043 | `9f1ec6e4eb8b44351807f1ada49c9f60159e58378d6f50be4a424abe50d6d8f4` |
| `cycle-067/tap.pcap` | 404658 | `c8fe5298092a0c29b6026ae8f4001f660b18852ced901816f95bd0af29d682c4` |
| `cycle-068/tap.pcap` | 410687 | `a606e575371983c8e7c6d2588a24abcc674671e8f2039dc0d4ee191bb9e68f66` |
| `cycle-069/tap.pcap` | 410244 | `f344f4fd5edfcdcfc891e6566c449a03a9920aad1459626cc1b406e30f85d89a` |
| `cycle-070/tap.pcap` | 411765 | `b2fe0aba971bb4bb805ffabc7407e905db2547548b902403f179cff9f42a8a88` |
| `cycle-071/tap.pcap` | 410606 | `81f9b6ffc7975b0bc33e2806c25f74446e9d231fe02903cbd10fa905517efc2f` |
| `cycle-072/tap.pcap` | 351858 | `5556e3ec9fa0f17e6f9922139102b467cfe1184d3df79fcdbbc17576cfa69570` |
| `cycle-073/tap.pcap` | 412135 | `19b78b59ba8dabdc52185f0bd06581de7821a630e1361703fffc07bfa65f719c` |
| `cycle-074/tap.pcap` | 412589 | `81d4394c4e835c646bb6a0e6fe52aef096f67d195a6ef6e55b9e9cac6ddab1a3` |
| `cycle-075/tap.pcap` | 410594 | `637d66a881a8114f91249691ddb8327d75bbe69a6ae1e58650a14371416ef132` |
| `cycle-076/tap.pcap` | 410990 | `83bc8d9db40ef7e0766c6d54fdcf648417a4d570c2174ce73313148b29f9763e` |
| `cycle-077/tap.pcap` | 411506 | `669b489c9e3f422ff9370888844a11c8ce36497a9e6a8b1c7c932c7787e18ade` |
| `cycle-078/tap.pcap` | 409950 | `7830dc598670dde4aeae9e86bfb57aa0d0adf07dda5d1edb6b953cbd0dd603e7` |
| `cycle-079/tap.pcap` | 410027 | `2b00c7322c8bfa4593d8eee310f664c42f8a0cf672736080dca1b626a3bfab86` |
| `cycle-080/tap.pcap` | 412171 | `e06012e07779eca5d2b5055240e54e0776cf99fbfd2b696a438a3747eb5b7647` |
| `cycle-081/tap.pcap` | 352117 | `c61430bad6a10b8bdf2ecb831400fc2fb9295cd17d5f01da6dbdb75a0ce7f27f` |
| `cycle-082/tap.pcap` | 409864 | `66998a628a1bf432ac1128ac27ed76a171f7b6036ecece67af5f6b836dc0fbe5` |
| `cycle-083/tap.pcap` | 410911 | `28143bc0128c5d4dd519345380e6150f9873b95ea0fbf9f979cb70ced022bca9` |
| `cycle-084/tap.pcap` | 411913 | `2e824b231f6727f007038d9c9f898cf75f28b773e1445940aa2d81300b106d86` |
| `cycle-085/tap.pcap` | 409809 | `f53fda6c742445c3a90ec156eb64a4eedd4d1deebd51ef4f2a642a99fb54bd3c` |
| `cycle-086/tap.pcap` | 409922 | `3e428a293d68e8eb9a826de55651d3c95e7c3d59a278690555fcb2fcddee9d91` |
| `cycle-087/tap.pcap` | 410433 | `d4a0b73c99402c0c38cebccab8256d97349eebdb262cabc504d88227125abc9b` |
| `cycle-088/tap.pcap` | 411053 | `2661337a545d9154ad6c99cf1f75b248e12e374901625c860b6e0ab7a948f35f` |
| `cycle-089/tap.pcap` | 410012 | `f295e0bfaf6400e089cd69f54eb50454cc91b10ec7e70ba9fd461df23ae62f47` |
| `cycle-090/tap.pcap` | 410273 | `96c2fe75e73b0d0b9ad51f1a396da5765aeaf4311dd83b6b52d4eb2dab93d0c3` |
| `cycle-091/tap.pcap` | 410889 | `34ddecdc14d29e7f08b503727f1ed3749c630e7c99cd32a6a8eb52b6c10af0c1` |
| `cycle-092/tap.pcap` | 409939 | `d72650c6c9543a5f9223ee44198d8ca185858d7d9b08c1561be1fe5546c7fdf9` |
| `cycle-093/tap.pcap` | 405475 | `f554f6dd85c6b8c8a11db62d29150575f5f7968da379048f14947361be28e84d` |
| `cycle-094/tap.pcap` | 353329 | `1f59197d02885fe525cacf3dc8a2d9ea520f5bd751a06d3b509ae19f39c765f2` |
| `cycle-095/tap.pcap` | 409618 | `f0402c066b4233831a2fbc8d743a6cca1ae712e16ef5fbc110124a2d58f35a65` |
| `cycle-096/tap.pcap` | 409431 | `c794089537de53ceb4a8e71302168fb4ed521248cb6c27270793324f1512a8a6` |
| `cycle-097/tap.pcap` | 404526 | `12bfd2c1ff6ba4245c7e59858180d155be542d12a55b5f7aa0cde8209b68c17a` |
| `cycle-098/tap.pcap` | 409405 | `3f23291b1fa0b748e431611476482ddde62ec9060112c236141024d829905199` |
| `cycle-099/tap.pcap` | 409989 | `26bfe37e6178360492885f6bf35ededb3e52637cd20d423022b70a44ff53cf8a` |
| `cycle-100/tap.pcap` | 352875 | `a05efa90f355a4afd01d83d2072941f63cdfc2dd6323148df5bb2f33a7aeae7d` |
