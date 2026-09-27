# Reconnect restart measurement

Refs #75. Operator [A386], measured 2026-09-27.

Measured transport: CRF, one direction at a time.
AAF restart timing remains unmeasured.

## Contents

- **[Scope and identity](#scope-and-identity)** -- Assignment, image, and simulation boundary.
- **[Method](#method)** -- Timing anchors, validity checks, and capture limits.
- **[Distribution](#distribution)** -- Restart times and the one-second acceptance.
- **[Growth](#growth)** -- Ordered blocks and latency trends.
- **[MSRP attribution](#msrp-attribution)** -- Sender counts, rates, and declaration events.
- **[Cycle evidence](#cycle-evidence)** -- Every measured restart and captured exchange.
- **[Counters and restoration](#counters-and-restoration)** -- Counter authority and restored state.
- **[Acceptance](#acceptance)** -- Evidence against each issue criterion.
- **[Artifacts](#artifacts)** -- Exact image hashes and full capture index.
- **[Validation](#validation)** -- Required gates and reproducible analysis.

## Scope and identity

[The assignment](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5859652809)
requires 100 cycles per direction.
Ten consecutive overruns stop that direction.

This evidence uses the assigned running image.
No product source changed.

| Identity item | Recorded value |
|---|---|
| Image source | `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` |
| Evidence base | `8bc97021f28fb7f729418d3a00851c84ea0b50fd` |
| VERSION / firmware | `0x0002_0060` / `2.96.0` |
| ROM CRC32 | `9b6576a9` over 52,216 bytes |
| QSPI payload CRC32 | `3c18c276` over 3,825,788 bytes |
| AEM CRC32 | `93742dd2` over 7,352 bytes |
| ENTITY / CONFIGURATION | Exact assigned AEM descriptor bytes |
| Initial UART grader | PASS, 10/10 |

Local bitstream and AEM SHA-256 match the assignment.
UART provides CRC consistency, not configured-fabric SHA-256 readback.

Image-to-base product paths are unchanged.
Intervening changes concern documentation, evidence, and test infrastructure.

[Phase-1 PR #321](https://github.com/kebag-logic/milan-fpga/pull/321)
pins the replacement SRP engine in simulation.
Six peer LeaveAll cycles emit at most 18 PDUs.

Each cycle emits at most four PDUs.
Every cycle re-declares Listener Ready.

The retired context module directly queued received-LeaveAll refresh.
It is absent from this running architecture.

[Historical source](https://github.com/kebag-logic/milan-fpga/blob/eb375c131ef0e3b3b42ef42f4e546d8d8b20b494/hdl/ieee8021q/srp/KL_lwsrp_ctx.sv)
and [design](https://github.com/kebag-logic/milan-fpga/blob/eb375c131ef0e3b3b42ef42f4e546d8d8b20b494/docs/LWSRP_FPGA_ARCHITECTURE.md)
were read without restoring retired files.

[Current SRP design](../../protocol-processor/docs/architecture/10_srp_engine.md)
defines the replacement and remaining LeaveAll-timer deviation.
This measurement neither changes RTL nor resolves that deviation.

## Method

Topology: DUT, inline tap, AVB bridge, reference peer.
The controller shares that AVB network.

The same approved tap required its temporary capture driver.
Its three build inputs matched the previous operator’s hashes.

| Direction | Talker output | Listener input | Format |
|---|---|---|---|
| DUT listener | Reference 2 | DUT 1 | `041060010000bb80` |
| DUT talker | DUT 1 | Reference 8 | `041060010000bb80` |

These matching CRF streams require no format changes.
Both clock selections remain internal.

Each cycle first records approximately three seconds.
The controller then sends `DISCONNECT_RX`.

After success, it waits two seconds.
It then sends `CONNECT_RX`.

The successful response starts the measured interval.
The first valid stream PDU ends it.

Controller identity and sequence identify the response.
Stream identity and direction identify the resumed PDU.

CRF validation checks version, stream-valid, type, frequency, and lengths.
It also checks interval, VLAN, priority, and settled destination.

Source identity must match the bound stream.
The next packet must advance sequence and timestamp.

The tap timestamps both endpoints on one hardware clock.
Its nanosecond word is unwrapped using capture-host timestamps.

Host clock offsets do not enter the elapsed interval.
Printed precision does not establish absolute timestamp calibration.

Each restart observation has a thirty-second cap.
Pre-capture and the mandated disconnect hold precede that observation.

Capture continues three seconds after resumed traffic reaches collection.
Every cycle retains its full capture.

Capture-host packet drops invalidate evidence.
Parsing errors and missing responses also invalidate evidence.

Per-action foreground timeouts bound commands and capture children.

Each action holds the bench lock until children exit.
Analysis runs after that lock is released.

## Distribution

All values are seconds; p95 uses nearest rank.

| Direction | Cycles | Below 1 s | Min | Median | p95 | Max | Result |
|---|---|---|---|---|---|---|---|
| DUT listener | 100 | 100 | 0.006641 | 0.110280 | 0.188503 | 0.204859 | PASS |
| DUT talker | 100 | 100 | 0.000297 | 0.019165 | 0.039614 | 0.117736 | PASS |

Initial binds are excluded from these distributions.
Any censored cycle remains a failure, outside numeric quantiles.

| Initial bind, excluded from cycle count | Response to AVTP, seconds | Below 1 s |
|---|---|---|
| DUT listener | 0.198316 | PASS |
| DUT talker | 6.889398 | FAIL |

The initial DUT-talker binding exceeds one second.
Its capture retains the delayed Listener Ready arrival.

Bridge Listener Ready arrives after 6.888605 seconds.
Valid CRF follows another 0.000793 seconds later.

DUT Talker Advertise repeats while that Ready is absent.
A bridge LeaveAll precedes the eventual Ready.

This locates the observed wait before Ready reaches DUT.
Peer-side capture is required for further causal attribution.

## Growth

Ordered blocks expose changes hidden by pooled quantiles.
Regression uses cycle number against latency in seconds.

| Direction | First ten median | Last ten median | Slope, seconds/cycle |
|---|---|---|---|
| DUT listener | 0.122844 | 0.118585 | -0.000100 |
| DUT talker | 0.019894 | 0.019818 | -0.000008 |

| Direction | Cycles | Median, seconds | Maximum, seconds | Combined MSRP PDUs/s |
|---|---|---|---|---|
| DUT listener | 1-10 | 0.122844 | 0.178174 | 2.297748 |
| DUT listener | 11-20 | 0.142162 | 0.191796 | 2.343731 |
| DUT listener | 21-30 | 0.095617 | 0.171912 | 2.256045 |
| DUT listener | 31-40 | 0.106201 | 0.191218 | 2.414261 |
| DUT listener | 41-50 | 0.067111 | 0.177925 | 2.409748 |
| DUT listener | 51-60 | 0.090436 | 0.203084 | 2.411541 |
| DUT listener | 61-70 | 0.042417 | 0.153266 | 2.336267 |
| DUT listener | 71-80 | 0.134288 | 0.204859 | 2.511647 |
| DUT listener | 81-90 | 0.087061 | 0.180242 | 2.416954 |
| DUT listener | 91-100 | 0.118585 | 0.178821 | 2.363093 |
| DUT talker | 1-10 | 0.019894 | 0.117736 | 2.108677 |
| DUT talker | 11-20 | 0.018978 | 0.039614 | 1.920865 |
| DUT talker | 21-30 | 0.019365 | 0.020036 | 1.750685 |
| DUT talker | 31-40 | 0.018961 | 0.020482 | 1.867057 |
| DUT talker | 41-50 | 0.018974 | 0.082168 | 2.017861 |
| DUT talker | 51-60 | 0.018862 | 0.066967 | 1.878170 |
| DUT talker | 61-70 | 0.019376 | 0.042347 | 1.880260 |
| DUT talker | 71-80 | 0.019060 | 0.020492 | 1.831848 |
| DUT talker | 81-90 | 0.018913 | 0.116171 | 1.956921 |
| DUT talker | 91-100 | 0.019818 | 0.021083 | 2.044871 |

Neither direction shows progressive slowdown across ten-cycle blocks.
Both fitted slopes are negative.

Last-ten medians remain below their first-ten medians.
These observations cover the measured CRF pairs only.

MSRP remains near two combined PDUs per second.
Block rates vary with periodic refresh and short bursts.

## MSRP attribution

Every captured MSRP vector is decoded and attributed.
Counts include all types and all packed attribute events.

Only two MSRP transmitters appear on the tapped segment.
Their source addresses distinguish DUT and adjacent bridge.

Peer-origin stream attributes arrive as bridge declarations.
The peer’s original link-local MSRP exchange is not tapped.

LeaveAll counts represent type-scoped vectors, not PDUs.
Ready counts include New, JoinIn, and JoinMt declarations.

The packet preserves individual events in each `msrp.tsv`.
Raw captures preserve original first values and full payloads.

Before spans capture start through successful disconnect.
After spans successful reconnect through capture end.

Resumed spans first valid CRF through capture end.
Rates divide packet totals by summed window durations.

| Direction | Sender | Before PDUs/s | After PDUs/s | Resumed PDUs/s | Whole PDUs | LeaveAll vectors |
|---|---|---|---|---|---|---|
| DUT listener | DUT | 1.233189 | 1.836808 | 1.627969 | 1419 | 288 |
| DUT listener | bridge | 0.245973 | 1.002123 | 0.633241 | 722 | 284 |
| DUT talker | DUT | 1.291553 | 1.202486 | 1.201664 | 1123 | 272 |
| DUT talker | bridge | 0.256313 | 0.933310 | 0.690640 | 608 | 280 |

No sustained re-declaration storm appears in these captured cycles.
Periodic refresh and bounded LeaveAll bursts remain present.

Maximum one-second bursts are 11 and 10 combined PDUs.
They belong to listener and talker directions, respectively.

These transient bursts differ from sustained 11-PDU/s traffic.
The full event lists preserve every declaration and withdrawal.

| Direction | Sender | Attribute | New | JoinIn | In | JoinMt | Mt | Lv | LeaveAll |
|---|---|---|---|---|---|---|---|---|---|
| DUT listener | DUT | TalkerAdvertise | 0 | 0 | 0 | 0 | 282 | 0 | 72 |
| DUT listener | DUT | TalkerFailed | 0 | 0 | 0 | 0 | 0 | 0 | 72 |
| DUT listener | DUT | Listener | 203 | 0 | 0 | 865 | 170 | 100 | 72 |
| DUT listener | DUT | Domain | 0 | 1044 | 0 | 0 | 0 | 0 | 72 |
| DUT listener | bridge | TalkerAdvertise | 200 | 0 | 0 | 268 | 0 | 100 | 71 |
| DUT listener | bridge | TalkerFailed | 0 | 0 | 0 | 0 | 0 | 0 | 71 |
| DUT listener | bridge | Listener | 0 | 0 | 2 | 0 | 108 | 0 | 71 |
| DUT listener | bridge | Domain | 0 | 145 | 0 | 287 | 0 | 0 | 71 |
| DUT talker | DUT | TalkerAdvertise | 0 | 0 | 0 | 1062 | 142 | 1 | 68 |
| DUT talker | DUT | TalkerFailed | 0 | 0 | 0 | 0 | 0 | 0 | 68 |
| DUT talker | DUT | Listener | 0 | 0 | 0 | 0 | 276 | 0 | 68 |
| DUT talker | DUT | Domain | 0 | 1037 | 0 | 0 | 0 | 0 | 68 |
| DUT talker | bridge | TalkerAdvertise | 0 | 0 | 0 | 0 | 6 | 0 | 70 |
| DUT talker | bridge | TalkerFailed | 0 | 0 | 0 | 0 | 0 | 0 | 70 |
| DUT talker | bridge | Listener | 201 | 0 | 0 | 244 | 0 | 100 | 70 |
| DUT talker | bridge | Domain | 0 | 136 | 0 | 276 | 0 | 0 | 70 |

## Cycle evidence

Paired counts use DUT / bridge order.
Counts cover each complete capture, including the unbound interval.

TA and Listener counts include New, JoinIn, and JoinMt.
Ready counts require packed Ready within those declarations.

| Direction | Cycle | Restart, seconds | PDUs | LeaveAll | TA declarations | Listener declarations | Ready | Result |
|---|---|---|---|---|---|---|---|---|
| DUT listener | 1 | 0.112517 | 13 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 2 | 0.178174 | 13 / 6 | 0 / 0 | 0 / 4 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 3 | 0.126759 | 13 / 7 | 4 / 0 | 0 / 3 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 4 | 0.078600 | 16 / 8 | 4 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 5 | 0.085312 | 13 / 8 | 4 / 4 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 6 | 0.123005 | 13 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 7 | 0.138517 | 13 / 5 | 0 / 0 | 0 / 3 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 8 | 0.139367 | 13 / 7 | 4 / 0 | 0 / 5 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 9 | 0.008950 | 15 / 7 | 4 / 0 | 0 / 3 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 10 | 0.122683 | 14 / 8 | 4 / 4 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 11 | 0.160398 | 16 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 12 | 0.123926 | 15 / 7 | 4 / 4 | 0 / 5 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 13 | 0.170822 | 15 / 6 | 0 / 4 | 0 / 4 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 14 | 0.065479 | 13 / 5 | 0 / 0 | 0 / 3 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 15 | 0.083289 | 13 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 16 | 0.079973 | 13 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 17 | 0.190520 | 14 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 18 | 0.089331 | 17 / 8 | 4 / 4 | 0 / 6 | 13 / 0 | 13 / 0 | PASS |
| DUT listener | 19 | 0.167097 | 16 / 9 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 20 | 0.191796 | 12 / 7 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 21 | 0.058579 | 13 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 22 | 0.120231 | 15 / 7 | 4 / 0 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 23 | 0.034819 | 13 / 7 | 4 / 0 | 0 / 3 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 24 | 0.088359 | 14 / 8 | 4 / 4 | 0 / 5 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 25 | 0.102874 | 14 / 8 | 4 / 4 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 26 | 0.032616 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 27 | 0.127448 | 13 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 28 | 0.171912 | 12 / 5 | 0 / 0 | 0 / 3 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 29 | 0.116787 | 13 / 7 | 4 / 0 | 0 / 5 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 30 | 0.020335 | 15 / 7 | 4 / 0 | 0 / 3 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 31 | 0.191218 | 16 / 8 | 4 / 4 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 32 | 0.015791 | 15 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 33 | 0.180229 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 34 | 0.045236 | 11 / 5 | 0 / 0 | 0 / 3 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 35 | 0.033914 | 12 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 36 | 0.180612 | 14 / 8 | 4 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 37 | 0.173342 | 14 / 8 | 4 / 4 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 38 | 0.010920 | 15 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 39 | 0.016602 | 16 / 8 | 4 / 4 | 0 / 6 | 13 / 0 | 13 / 0 | PASS |
| DUT listener | 40 | 0.167166 | 16 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 41 | 0.069939 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 42 | 0.138612 | 14 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 43 | 0.064282 | 15 / 8 | 4 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 44 | 0.055057 | 15 / 7 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 45 | 0.023757 | 16 / 7 | 4 / 4 | 0 / 4 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 46 | 0.135330 | 15 / 8 | 4 / 4 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 47 | 0.087304 | 13 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 48 | 0.177925 | 15 / 7 | 4 / 0 | 0 / 5 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 49 | 0.061709 | 15 / 7 | 4 / 0 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 50 | 0.059403 | 16 / 8 | 4 / 4 | 0 / 6 | 13 / 0 | 13 / 0 | PASS |
| DUT listener | 51 | 0.012018 | 15 / 8 | 4 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 52 | 0.181673 | 15 / 8 | 4 / 4 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 53 | 0.054453 | 16 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 54 | 0.011118 | 15 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 55 | 0.014851 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 56 | 0.188503 | 13 / 5 | 0 / 0 | 0 / 3 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 57 | 0.053076 | 13 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 58 | 0.137634 | 15 / 8 | 4 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 59 | 0.126420 | 13 / 8 | 4 / 4 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 60 | 0.203084 | 14 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 61 | 0.006641 | 12 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 62 | 0.074364 | 13 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 63 | 0.079002 | 12 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 64 | 0.046661 | 14 / 8 | 4 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 65 | 0.153266 | 15 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 66 | 0.030038 | 16 / 8 | 4 / 4 | 0 / 6 | 13 / 0 | 13 / 0 | PASS |
| DUT listener | 67 | 0.029525 | 14 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 68 | 0.038173 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 69 | 0.012841 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 70 | 0.140494 | 15 / 7 | 4 / 0 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 71 | 0.154243 | 15 / 7 | 4 / 0 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 72 | 0.139764 | 15 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 73 | 0.204859 | 15 / 8 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 74 | 0.187577 | 17 / 8 | 4 / 4 | 0 / 4 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 75 | 0.044271 | 14 / 9 | 4 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 76 | 0.128811 | 14 / 8 | 4 / 4 | 0 / 3 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 77 | 0.114820 | 16 / 8 | 4 / 4 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 78 | 0.115472 | 14 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 79 | 0.017391 | 14 / 6 | 0 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 80 | 0.140145 | 15 / 7 | 4 / 0 | 0 / 5 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 81 | 0.017824 | 15 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 82 | 0.054454 | 16 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 83 | 0.132521 | 16 / 7 | 4 / 4 | 0 / 4 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 84 | 0.019902 | 13 / 8 | 4 / 4 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 85 | 0.062005 | 13 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 86 | 0.108604 | 14 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 87 | 0.180242 | 16 / 8 | 4 / 4 | 0 / 6 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 88 | 0.120874 | 14 / 8 | 4 / 4 | 0 / 3 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 89 | 0.065518 | 13 / 8 | 4 / 4 | 0 / 5 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 90 | 0.162272 | 13 / 6 | 0 / 4 | 0 / 4 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 91 | 0.084145 | 13 / 5 | 0 / 0 | 0 / 3 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 92 | 0.111955 | 12 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 93 | 0.136599 | 14 / 9 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 94 | 0.126171 | 16 / 9 | 4 / 4 | 0 / 4 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 95 | 0.152873 | 13 / 9 | 4 / 4 | 0 / 6 | 11 / 0 | 11 / 0 | PASS |
| DUT listener | 96 | 0.089803 | 14 / 9 | 4 / 4 | 0 / 6 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 97 | 0.099475 | 15 / 7 | 0 / 4 | 0 / 4 | 12 / 0 | 12 / 0 | PASS |
| DUT listener | 98 | 0.125215 | 11 / 6 | 0 / 0 | 0 / 4 | 9 / 0 | 9 / 0 | PASS |
| DUT listener | 99 | 0.178821 | 14 / 7 | 4 / 0 | 0 / 5 | 10 / 0 | 10 / 0 | PASS |
| DUT listener | 100 | 0.024800 | 16 / 9 | 4 / 4 | 0 / 6 | 13 / 0 | 13 / 0 | PASS |
| DUT talker | 1 | 0.117736 | 12 / 8 | 4 / 4 | 7 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 2 | 0.026166 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 3 | 0.018096 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 4 | 0.019959 | 13 / 8 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 5 | 0.019830 | 11 / 6 | 0 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 6 | 0.018549 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 7 | 0.019455 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 8 | 0.020175 | 12 / 6 | 4 / 4 | 11 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 9 | 0.019988 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 10 | 0.018896 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 11 | 0.019726 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 12 | 0.019536 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 13 | 0.000364 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 14 | 0.017658 | 12 / 8 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 15 | 0.018366 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 16 | 0.019175 | 10 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 17 | 0.020986 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 18 | 0.018781 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 19 | 0.039614 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 20 | 0.018410 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 21 | 0.019727 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 22 | 0.019556 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 23 | 0.019419 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 24 | 0.000297 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 25 | 0.018126 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 26 | 0.020036 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 27 | 0.018798 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 28 | 0.018665 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 29 | 0.019480 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 30 | 0.019310 | 10 / 6 | 4 / 0 | 9 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 31 | 0.019123 | 11 / 7 | 4 / 4 | 10 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 32 | 0.017944 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 33 | 0.018855 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 34 | 0.018674 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 35 | 0.020482 | 10 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 36 | 0.019308 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 37 | 0.019125 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 38 | 0.019046 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 39 | 0.018875 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 40 | 0.018793 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 41 | 0.019607 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 42 | 0.018437 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 43 | 0.018254 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 44 | 0.082168 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 45 | 0.018996 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 46 | 0.018952 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 47 | 0.018863 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 48 | 0.021051 | 14 / 7 | 4 / 4 | 13 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 49 | 0.019252 | 14 / 7 | 4 / 4 | 13 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 50 | 0.018800 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 51 | 0.018868 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 52 | 0.017806 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 53 | 0.018857 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 54 | 0.018677 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 55 | 0.018482 | 11 / 7 | 4 / 4 | 11 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 56 | 0.018304 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 57 | 0.019216 | 10 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 58 | 0.019044 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 59 | 0.066967 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 60 | 0.020769 | 11 / 7 | 4 / 4 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 61 | 0.019608 | 11 / 7 | 4 / 4 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 62 | 0.019468 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 63 | 0.042347 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 64 | 0.019170 | 11 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 65 | 0.019091 | 11 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 66 | 0.019920 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 67 | 0.018743 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 68 | 0.020554 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 69 | 0.018467 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 70 | 0.019284 | 12 / 6 | 4 / 4 | 11 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 71 | 0.020109 | 9 / 5 | 0 / 4 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 72 | 0.017427 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 73 | 0.018249 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 74 | 0.019052 | 10 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 75 | 0.001864 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 76 | 0.018660 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 77 | 0.020492 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 78 | 0.020409 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 79 | 0.019238 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 80 | 0.019068 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 81 | 0.018971 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 82 | 0.018855 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 83 | 0.018737 | 15 / 7 | 4 / 4 | 14 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 84 | 0.018676 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 85 | 0.020614 | 10 / 5 | 0 / 4 | 10 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 86 | 0.018521 | 9 / 4 | 0 / 0 | 9 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 87 | 0.019487 | 11 / 6 | 4 / 0 | 10 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 88 | 0.018415 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 89 | 0.019327 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 90 | 0.116171 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 91 | 0.021083 | 11 / 7 | 4 / 4 | 10 / 0 | 0 / 3 | 0 / 3 | PASS |
| DUT talker | 92 | 0.019920 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 93 | 0.020833 | 12 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 94 | 0.019716 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 95 | 0.020583 | 11 / 5 | 0 / 4 | 11 / 0 | 0 / 4 | 0 / 4 | PASS |
| DUT talker | 96 | 0.019520 | 10 / 6 | 4 / 0 | 9 / 0 | 0 / 5 | 0 / 5 | PASS |
| DUT talker | 97 | 0.019348 | 10 / 7 | 4 / 4 | 9 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 98 | 0.019160 | 12 / 7 | 4 / 4 | 11 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 99 | 0.019083 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 6 | 0 / 6 | PASS |
| DUT talker | 100 | 0.019959 | 13 / 7 | 4 / 4 | 12 / 0 | 0 / 4 | 0 / 4 | PASS |

## Counters and restoration

The [register map](../reference/REGISTER_MAP.md) defines counter authority.
Legacy per-plane PDU counters are structural zeros.

| Word | Meaning | Observed use |
|---|---|---|
| `0x650` | Legacy ACMP responder counts | Retained zero readbacks |
| `0x69C` | Legacy MSRP RX/TX counts | Retained zero readbacks |
| `0x6B0` | Legacy listener command/probe counts | Retained zero readbacks |
| `0x930` | Aggregate processor RX/TX and drops | Retained before/after readbacks |
| AECP GET_COUNTERS | Stream, interface, clock-domain counters | Retained before/after snapshots |

Zero legacy words cannot measure current protocol traffic.
The per-cycle wire counts supply that measurement.

Restoration PASS: all 18 stream states are unbound.
Both original clocks, configurations, rates, and descriptors match.

Reserved response halfwords are excluded from setting comparisons.
Observed counters are retained without reset.

Final UART grading passes all ten checks.
ROM, flash-payload, and AEM CRCs match their initial values.

Final wire capture contains no valid CRF.
Temporary controller scripts and capture driver are removed.

The original capture-host interface set is restored.
Every child exited; the bench lock is free.

Power, DUT firmware, wiring, and excluded equipment were untouched.

## Acceptance

| Issue criterion | Result | Evidence |
|---|---|---|
| First valid AVTP below one second | PASS for measured CRF | Per-direction distribution and all cycle records |
| Restart latency does not grow | PASS for measured CRF | Ordered blocks and fitted trends |
| Firmware, topology, capture, distribution documented | PASS | Identity, method, full capture index, restore evidence |

This is an operator measurement, not an independent review.
It does not close #75 or qualify unmeasured formats.

## Artifacts

Raw files remain in private storage.
Artifact identifiers below map through `RAW-ARTIFACTS.json`.

Each identifier records size and SHA-256.
No raw capture or binary enters the repository.

| Image artifact | Bytes | SHA-256 |
|---|---|---|
| `gateware/alinx_ax7101.bit` | 3825992 | `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` |
| `software/bios/bios.bin` | 52220 | `89ce096c84eaae7028d1f82e3163c44276c7db8f0b9662276e2d1cce3de1c4f4` |
| `aem_desc.bin` | 7352 | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |
| `csr.csv` | 9033 | `92981a367616f79dc5d5382257afdb0aeff211845f86ea3b322102292c562e35` |

| Capture identifier | Bytes | SHA-256 |
|---|---|---|
| `baseline/tap.pcap` | 18667 | `aba48bd4f164caa0d85b2442c37caca908f16982a0b6b1105f23763174461020` |
| `final/tap.pcap` | 16243 | `72fb475ced01b07fc4b28943b90fa90f0264ededd5112cab9fc7c68ef5ca1a8b` |
| `listener-001/tap.pcap` | 353788 | `85bdc173217a7da1e79aa6f91919191468424ad321a0394db532cee34489787c` |
| `listener-002/tap.pcap` | 404217 | `cc1e8a76c2cfe0746fff07a11f89b2a871b641e66038e72b9abe252c5b0e2f41` |
| `listener-003/tap.pcap` | 411133 | `ed82e37200ea5473b7505bb9742ab8875035df1b9694ae46d3fff61437095ad9` |
| `listener-004/tap.pcap` | 414299 | `031168e1f7736b9e2dc21c0b81a1b332105cb05ac700f9ccfa833ef2e56e48b7` |
| `listener-005/tap.pcap` | 405496 | `2ae1b2dcf3777f046a6a81684329442c0e7270f1855d8c28225eb1ee37f0bd7e` |
| `listener-006/tap.pcap` | 410424 | `a4cf78d97e4ba9504e03293f3cca636b1289ddcaf008553ce21bda91e303d531` |
| `listener-007/tap.pcap` | 410738 | `003128c639521582ed088430b268185a725934c5adc71f0fd9f2699c88cae97c` |
| `listener-008/tap.pcap` | 411123 | `e07aaf9fa83773d879986f7809883df04e811ec21379810a8566ac5856f33971` |
| `listener-009/tap.pcap` | 411392 | `ac3082d79fa520460f9e0d6ee7e6a2d67da0be531384c0d630cb9dc002d2a139` |
| `listener-010/tap.pcap` | 411248 | `46934c7120d43f9604937e6edfa438c14a88d346d7d5bbe7170d286a511510d2` |
| `listener-011/tap.pcap` | 411319 | `125d2732bacdb77d027c2d292e25127a2bae3c4de0c8185b5400f876ea5e7ec1` |
| `listener-012/tap.pcap` | 409833 | `b238c380fdf5283772d521b2ee2bb47ff003887fa762933c77242f54c7244f50` |
| `listener-013/tap.pcap` | 412076 | `9a36d2da8a662cf94a9ee6c9d02c22c829f374768acdf4e005775a313bdf7de3` |
| `listener-014/tap.pcap` | 410411 | `fe3a64a64b47940340f4839ba5d978451239df882ebdaf76d4b6a72f7fb65a4b` |
| `listener-015/tap.pcap` | 462343 | `22b89f8a250bc3c4e4cceef2fdcc5b5a81052b5a8ce7dddf400c2d47ad89a68b` |
| `listener-016/tap.pcap` | 410260 | `9b41a98d0185c8bdb6d6680d0297b557548048d4830a5cf0ea884c81586cbfc6` |
| `listener-017/tap.pcap` | 410482 | `760fcd1b1773f3758b250253b5dba20759ef5234718c2ca8b5b8414949b99963` |
| `listener-018/tap.pcap` | 410834 | `4594cc95af7663207182b378021e57907a047cd123cb0e9fd9a54287d76fe4c9` |
| `listener-019/tap.pcap` | 410680 | `f8a934340f8a916cb6f98ef01dbe6599bec7b1e64dd01382ea413c7146cb259d` |
| `listener-020/tap.pcap` | 409550 | `ab675a39dad2fcecb0a9bb35b7fad8e60edc8d2b2943756bb9c0bf951084bd3e` |
| `listener-021/tap.pcap` | 410050 | `c9c468b0b2913e75696593acad3d480af83d3c770d60eaef1f5da6c80c4c5d51` |
| `listener-022/tap.pcap` | 410828 | `4cd423c8920bfd189b4cc2a59f438d563b8a07bd2d043270930b491d4cedd804` |
| `listener-023/tap.pcap` | 410098 | `c8baea15654f14a7c5ccf9dc169616b98a5911eae8b4456fe1b80476c69c050b` |
| `listener-024/tap.pcap` | 410747 | `3b1dfa9b0d569443eb08d70c116ac413fdc276af51bfa7ede6c8c357b144ebee` |
| `listener-025/tap.pcap` | 410994 | `0e838d8c29db1ebc0e86b41a1a649c396cb584ef146eb911b607d5276a22a646` |
| `listener-026/tap.pcap` | 409658 | `002bb2b77968d554328016e7e15f5437a143fe826b542da0beccefcc052abfa8` |
| `listener-027/tap.pcap` | 409982 | `3f6504e306ae2788edf18c72ae6f50b681feaf8152a866c9c7e1c1284706fe96` |
| `listener-028/tap.pcap` | 409936 | `6a7394a867dfa854c87ac47c1ee2f46fe707dd626339cb81f081bd6ca4ff723a` |
| `listener-029/tap.pcap` | 410511 | `f1e5700b6a8bfea11122a8568a5ca15777fe9087b19bb7e0ce1e5f212ff2bf1a` |
| `listener-030/tap.pcap` | 410400 | `9c31cb357cee15fef1ce0fb04617a7b3686d8332f3b8000823ad1fd809734bf3` |
| `listener-031/tap.pcap` | 410811 | `3bc1473a5ba30edc6e3776865b481f922ba25aa08ba3edf89a6b91eb9bdecf6f` |
| `listener-032/tap.pcap` | 410791 | `7182978dbf5b5ce3d9a855ed2e1f385771ef03fba4b8b2e35eea521705d6c250` |
| `listener-033/tap.pcap` | 410350 | `b167affafad8548f0ffe154607871fdb2162d5a941ac7d64c109a078152fb7fd` |
| `listener-034/tap.pcap` | 409306 | `f0647612c4748f573cce2c83f8af4533e5cbbb3c82078e1d0adbdfcd8dcd1b5b` |
| `listener-035/tap.pcap` | 410167 | `b77fc4ba58938cd3cc27492da1d9535ef0fd7f23647aae214be4ec2c5d9e0a87` |
| `listener-036/tap.pcap` | 407456 | `c7d9932d524b7bceb1cd8777c5b1797d3704133c40771936d7efa6787e5a4fad` |
| `listener-037/tap.pcap` | 410648 | `a9c3fde78c04399b3e0ca0fa0b9e45e28247d661e760df9d006a101a5e774435` |
| `listener-038/tap.pcap` | 410834 | `e7833581463d60b49bc5e4820da08ddf1b1e86484a869c9bc1f5797ea17fd0f0` |
| `listener-039/tap.pcap` | 411146 | `5be2da2aae9b8e1d724073aca0ef22f37709bb81ab01f393af86186365e6b460` |
| `listener-040/tap.pcap` | 411992 | `54bac35e9b357efcdabf9209878e6167b102d3fc1c9c8d9bf84b587af7deb9d8` |
| `listener-041/tap.pcap` | 410493 | `e82c02fec80b6f992173b9cb656e5570340b1fb505538e888c1d2f1c0707c9d8` |
| `listener-042/tap.pcap` | 410628 | `44ec74532f67ad0a884aca962c4d5e9052dfc879b8789f7a0cc11382d24e0137` |
| `listener-043/tap.pcap` | 410672 | `112bffe78eba156b8b7c49c2fe636dc3983f4cfb8647f70219c7b75d15f61b70` |
| `listener-044/tap.pcap` | 410892 | `9586a1c27a6a8c30b9a7ce8cef5550881b5dc1ca8d2a141c6c2b2b929cab8c18` |
| `listener-045/tap.pcap` | 413638 | `67a988a78fda808954349ab1c4368eb7be68186c414461363a92f16c3f1b61db` |
| `listener-046/tap.pcap` | 411694 | `65bf8269dc9e4c70ba132ea86a043232a72eedf02e70b4e2c28717d0141e7213` |
| `listener-047/tap.pcap` | 410220 | `e2f4ac148477aae6a05c76216e3ee6b4df57fa0e1413e498da6429dd39ccbe6a` |
| `listener-048/tap.pcap` | 463017 | `fb8da0c1fca2b3654611740dfa39ca08aec43f06841da0c213c091734218f80d` |
| `listener-049/tap.pcap` | 414297 | `c4de57f2876a67f4d5c6c5adde368a3b2f7e70b957c406dd679e29d0d1283660` |
| `listener-050/tap.pcap` | 411795 | `b66bf20578b315d3b06787d771189cf2e9fbed10008f0df08c515e0ad0bc7acb` |
| `listener-051/tap.pcap` | 410667 | `6d6178aa84f6efd95eda45ec924f01c1477117bd282e7e8963f13a09a9a65a60` |
| `listener-052/tap.pcap` | 410738 | `9d1092acb342c806ffdd7061835a6a814f35840a7af8955c50f4b76127af765d` |
| `listener-053/tap.pcap` | 413223 | `9d08a316aff9f1d5d5b3a73fc9c5e5bc8775ea7a9cf5aa280b26f8af617b4947` |
| `listener-054/tap.pcap` | 411218 | `2b305a7c01bda60f742e2f4137c68b1ed761815e1edf8d6f5186c189d8c7d578` |
| `listener-055/tap.pcap` | 409931 | `fa618edbd5f5bb6e0d42ad41c99c1308f1ffad2756a326dfcb0e5b97c5bebd8b` |
| `listener-056/tap.pcap` | 410057 | `56cafd85418adcad37202d4c567d7e8b69e979c50fe0dc6a1f6ddbd9d7e52673` |
| `listener-057/tap.pcap` | 412827 | `62a4774f2d60607b4b42120e5fa0cae07de8219b5c65b66993ca012174383711` |
| `listener-058/tap.pcap` | 411003 | `b50736f24588f832163ce79a85c286230b302efe22defd10e8b83a274789da03` |
| `listener-059/tap.pcap` | 410877 | `763fe9961770230d9ef88a3eb36e459f66d813f1dc996ec0d19067e3e7b679fb` |
| `listener-060/tap.pcap` | 400640 | `9fd4f32e8b7aeb14cdd83e4f1d9f007b13c01230fb362c98b1a250cf59e24411` |
| `listener-061/tap.pcap` | 410364 | `2165b67f81127ebc0e155f3048b4e9ebf01204ec190da8976533596832c661c6` |
| `listener-062/tap.pcap` | 409960 | `feeb2265e5ad5798323ca9fe5a2955f1dc44cfc9bd9e1032e2f6871991f3e47a` |
| `listener-063/tap.pcap` | 404897 | `9eb4ddc4efa5b98b76c69797136a138a2fdf0961b1f3dfcc56300d79aefa80f8` |
| `listener-064/tap.pcap` | 410741 | `c040f38ac8da4a3d8e29d87ca4d36875343507babd9098596f333644f2f20a59` |
| `listener-065/tap.pcap` | 410887 | `9073331ace7b51c71d4809d62068d5333196a9f259d90cef8ab8bdfab7b19c64` |
| `listener-066/tap.pcap` | 410495 | `68df79b39bd57eed22ebe6382bbfe3487f01d80a21030ff7877b1e8275c46ed5` |
| `listener-067/tap.pcap` | 410964 | `f9a85d17b548b113a4537f28c6222061e808abea47dc2a6da64d23c2381ea4e4` |
| `listener-068/tap.pcap` | 410396 | `b3d0e7ba1cb0437998592c62ce35fb3031b8a94a3dbca517eefb139936b7542b` |
| `listener-069/tap.pcap` | 409896 | `9c76ec8672d96250ef6ae0b5512e2c234bfdd7cc6b6a91a0ac5f783303065e97` |
| `listener-070/tap.pcap` | 410806 | `00cdbdbaf69ecbb1f024f20c3ef0730f5f8fbf7fd810aa953adc9ff9673c65ff` |
| `listener-071/tap.pcap` | 410244 | `5b7c7766dd7df02ddb73a9fd2a19fa0ae84b707054969e6083f2f0c09774f8ac` |
| `listener-072/tap.pcap` | 410341 | `58eb5dd6510d4df3b636da64a0a4ff3149033f19e569488d9dd05382de88ac89` |
| `listener-073/tap.pcap` | 399547 | `3c884cbb1f4ba9feca561a8c967c645c0f944432217a995f3f9c5c0bf4877e6c` |
| `listener-074/tap.pcap` | 409308 | `e0458d4d0cf8e2ea1a18bef28e8955bd50504ad753c8a2a90ef7b1c7d0cb5170` |
| `listener-075/tap.pcap` | 410957 | `8c42c369c7b31dd58c3237a1d7dc7a61ab85a2e712b5da4bfdd7f60d5a742bf3` |
| `listener-076/tap.pcap` | 410484 | `7941e1f73f926809937bcd81d871e048a4ef286c1a71f3d3219c80dbfd9279a2` |
| `listener-077/tap.pcap` | 410725 | `db3f3ddb7ae344e01066b72c611a7cd4f0676967f4e3853e233de578b7985500` |
| `listener-078/tap.pcap` | 410433 | `00497949be71023c93abeffee0062f6dc2829f9524542cc643f7e37b0e02b4b0` |
| `listener-079/tap.pcap` | 409874 | `f6281398209ef7ea03b600ba5a9a2437215f5cf236f80be4103cd22121b3fec0` |
| `listener-080/tap.pcap` | 410176 | `37bb975fc5b16c2fc03702ab14b6cb683a7a71134fcc07cce8f5dc365be9b73b` |
| `listener-081/tap.pcap` | 412833 | `4b9a9ed83a01385ac78c7f5fb2e180b89eed6f53a167162509e13290e345e5f8` |
| `listener-082/tap.pcap` | 411299 | `c3b8ec1bf0fbf4980491cd6a81f39fb0331b0129122b758c5a324812a5ae6b23` |
| `listener-083/tap.pcap` | 410542 | `b726b8b0ae0885bcb30aed37d8a9e141c60ca920a344e1632ed26ef241cf120c` |
| `listener-084/tap.pcap` | 410929 | `4469c757959b286f979bdc5bb93f81f0c8306ae4682813b4a8f27fc033a5aedd` |
| `listener-085/tap.pcap` | 412131 | `1bfdede11275879c771bbcdbacb412d120d6a587288b508729ce8ca0fc7b2adb` |
| `listener-086/tap.pcap` | 410145 | `3ac5d603d662fa523652e88c9f815985ee67b4db7f6d950db3a4c6cb7a71cc54` |
| `listener-087/tap.pcap` | 404926 | `ee2abad1064f8e7ededbbf85bb5a83a0a96a3eabc7f569bb87a676e6f85b39b8` |
| `listener-088/tap.pcap` | 411326 | `dffaeb272ac00e43c1f9a8566592e5ddd716a701113f977ce1dd9e47ebdef86b` |
| `listener-089/tap.pcap` | 414702 | `6eda7bdf5beedbf193f875bc885fcd6ed5a72d75b43d80348e48f521ef793899` |
| `listener-090/tap.pcap` | 404355 | `cb8f69945b0fafc86f34f9f576055f34e741d29dd04ea33676a4e9bec3cd7076` |
| `listener-091/tap.pcap` | 410584 | `ba20af95da5ba0965828f7f9cd1410eb9716705308d1023169d714b94077c6cc` |
| `listener-092/tap.pcap` | 411367 | `5c72a9573d64f9c897a46e79b9e83222607813d1aa83e476504a25f4c05d7747` |
| `listener-093/tap.pcap` | 414288 | `7a0abac1a2c52e34b65e7fbf42582cbb7fac68ae5f49527a3ab40dc41917f028` |
| `listener-094/tap.pcap` | 411654 | `9e6eaee826b63c447ba90cf65998e0074a08fdacae4c13e887cc11afde9fc94f` |
| `listener-095/tap.pcap` | 411292 | `b12e4f24d5b0d5dda2eb6e204b942934bcf60e9746210aec63c164b17dbbeafc` |
| `listener-096/tap.pcap` | 411693 | `935372526f5e9823aecb44244919d6d4e2e865d6fc7a68d5da7ff035480b4b42` |
| `listener-097/tap.pcap` | 410950 | `618f1fbd95a9527746fcfdd4cb0acc430d08e429f741111ccf0333264681c897` |
| `listener-098/tap.pcap` | 411620 | `5df73e4eb775c667a5ced819012a96fd8668d12001e2364310c45b66ca976257` |
| `listener-099/tap.pcap` | 411121 | `acba797d8c4324562128a45956febefef4c07e036b4b2397bb4f60d4050fcd12` |
| `listener-100/tap.pcap` | 469075 | `90572a46a9a97b75787f5914cd80319d137f309d97dfc375991a3adb0cd73cef` |
| `listener-restore/tap.pcap` | 181680 | `df25dc55771497d5d5940fe7c49f5bd578e6a931565983a64ba0a4f7e3cc67c3` |
| `listener-setup/tap.pcap` | 240695 | `6897cbf3f4003064448d9d174b31f439554bb13a3f0de858d626983c33de6e34` |
| `talker-001/tap.pcap` | 341095 | `0f9325d95809ea7a41134409271710bb113317d70f9dbad573a0478bcabf0ed5` |
| `talker-002/tap.pcap` | 409305 | `237c5eacfb6d53bb1cbd21d3d9b745c7a47d2a238ad58562755c0db2b28a4a0e` |
| `talker-003/tap.pcap` | 403526 | `42b792f3283578b0049384a680c1e1ac034e8e7b95b310121a97ab9ae19f13b3` |
| `talker-004/tap.pcap` | 409280 | `14c8cceba85320cd35685fdef0ae9081c29cd110cf66d57259265f8fe2ec6876` |
| `talker-005/tap.pcap` | 409353 | `2da74f3935e191866d64f4c8568646bc2ee608f2b6ca674c901f2735c56aac1e` |
| `talker-006/tap.pcap` | 408759 | `7391588b2bf9e908a5723b4d0c0d2b7eba6cb4de03e9ae91ff7061c91b39c300` |
| `talker-007/tap.pcap` | 402923 | `fd65a368d8f64fb5320a549274fc76745ba25537304594686f2181342015c52c` |
| `talker-008/tap.pcap` | 412145 | `22557261a3d928dfb8e8d32cdd92bc283b612b50c955d9e36fde4b279ce0c143` |
| `talker-009/tap.pcap` | 409088 | `0ea109ff6faf259fe3ac478ea41f7d718d96abc25ad584a50ef50d1343ea25ec` |
| `talker-010/tap.pcap` | 408635 | `24d7ea96a8a2dc40d28dadef31f301ef9238221cd393ea843afe843b57761cbc` |
| `talker-011/tap.pcap` | 408046 | `f4ab5761b2996ab0570c7e999f61ea13d6dfd093b8325cce78a01cea8df7b715` |
| `talker-012/tap.pcap` | 409299 | `efb0c3ae6df6ad6ea2c4b2b146fac3e7aef3b7c475b1a952d1f0d38dc93faa3e` |
| `talker-013/tap.pcap` | 461102 | `037f6f59b38aeb468ed18f1ce147be5bf2d2605aeddeedbfc4bf62518ca75b1a` |
| `talker-014/tap.pcap` | 408959 | `2ff1c04b233ec7f783d15c3db907cbc36c655e21fd9c1ce3280172c850f34082` |
| `talker-015/tap.pcap` | 408575 | `e38ea2ac9975464fcd922f114bce3dacb80d4d38f778a1292e6ee1f4e6f93a2a` |
| `talker-016/tap.pcap` | 408589 | `8886ec3dd60a1ea3e204ce585d630d2034a5fc92b03a9c87e727f7b389f64a89` |
| `talker-017/tap.pcap` | 408367 | `c9c8ac3797cae6794b2bb5b84ce9014748a48736f13d55f5c9a4dc259756aa07` |
| `talker-018/tap.pcap` | 409220 | `865d5cda89f4dffb88874316643f52f3f9ab8f3344421dcba4fc0955584f2759` |
| `talker-019/tap.pcap` | 410153 | `c5712db5e53916596933201ae929db0bb06a27b99eaa04cadbefe25ac57f965d` |
| `talker-020/tap.pcap` | 356744 | `127a2ef652f82877450df7e1cf91ce55e6bbb735d1311983d7b4a4f6f777e816` |
| `talker-021/tap.pcap` | 408813 | `1a031fd0867a1b5ba6e62242f91d2fef02a1626c6aeb09fd0753dbf995e0be22` |
| `talker-022/tap.pcap` | 407249 | `0d359947a7d30ba8f8ad280c6b02d8fe79435421a8339a217ceaa97fc9b5c1f0` |
| `talker-023/tap.pcap` | 409402 | `69313dae328ca94df421f1e7122e4f6285eb61938b7192c71357037f74e5348e` |
| `talker-024/tap.pcap` | 518465 | `74779d167f3e16bdac7ced31770c29351223e4b4c9eeda0c725f7588d4d6657d` |
| `talker-025/tap.pcap` | 404167 | `6178e1a64489a1b6d6d8f74ecb399cb083298a00b7474b6a0897759c19922fe0` |
| `talker-026/tap.pcap` | 409132 | `12499c67ba258be5d54fa15fde771fa22c9c51f59cc7dfb9efe85dd2eb4b269a` |
| `talker-027/tap.pcap` | 408637 | `cf9fb88f4fb6d76d1729a017f661905ec4db43181c678477bc36508f9d3d34c1` |
| `talker-028/tap.pcap` | 413209 | `cd883856c89acaf84adf199a00ab47afefb99b1cbfce0afcb67359052398cfc0` |
| `talker-029/tap.pcap` | 409154 | `74cd2462de4d9ddef09525ba4d95e810bf36f7707c302250759eede721552531` |
| `talker-030/tap.pcap` | 401972 | `2f46b12180085e5e544a2290115f5fca4bf9f0c34d42ce513e004ac1ac35ba7e` |
| `talker-031/tap.pcap` | 410069 | `6d7eba4864ab2482708849a8aad25515229737fa19dbc0cd28bfa89419607d3a` |
| `talker-032/tap.pcap` | 413627 | `67243e96156c75bbecc91a6152c6eb6eea113dbba8a03f491002fc2e4b583d41` |
| `talker-033/tap.pcap` | 410380 | `214ebc2f6c6bdcbda9584b1883e62f03871e21f4ddbe71dbd616356767aa8ce1` |
| `talker-034/tap.pcap` | 409245 | `fb33240d207629e143a344da2d48f31afc56b7434e2e2949f0b73eb90a85dcb1` |
| `talker-035/tap.pcap` | 408857 | `8af15d2d1a0992f32636a3e4f4724c8230ec0b99f855d3ef0e0a80a8366de477` |
| `talker-036/tap.pcap` | 410197 | `5947ce8930e85668f8f7b934b9cd68343bb149a4c3aee971ea592a165d40bcae` |
| `talker-037/tap.pcap` | 410059 | `1ebef3a3c2705d67987fb5a66d858991e6eb65fee5bcd3a381bf7db20da2e20c` |
| `talker-038/tap.pcap` | 409044 | `2c353fc26df1f8890c3090354dc9018f98a95a38a87c749a3443ace9b24f80de` |
| `talker-039/tap.pcap` | 409099 | `d7e076791a6fcbc12a744affcdd457b786a38062cf5f4488aabdac76217ca60e` |
| `talker-040/tap.pcap` | 408777 | `1b3e8e8be1a57262f7f6ffd93f237702be2c8746ffd4a3091c6e2fd0568e39a3` |
| `talker-041/tap.pcap` | 410975 | `3229fb625a5757a7cf9a15934ad8ff98b5326d7644d7d98213c66c1bd5bee1f8` |
| `talker-042/tap.pcap` | 404103 | `6fff00559efa87b611cf66c0c2a0ceb68ddb9b8a7502ef94af06a249d98e0b4a` |
| `talker-043/tap.pcap` | 409459 | `587b172a8c340ae7855f81f7532f58e1c9b1b0aa63364153c76b843052c90132` |
| `talker-044/tap.pcap` | 405549 | `3f6c17d7ce90b249abb3df9e30dff9525b855676738b551ddda9895262308a0d` |
| `talker-045/tap.pcap` | 402502 | `caceaf7c65dec1cef7b421ac8473648977601ec9af79d645961b0d3c0ed98258` |
| `talker-046/tap.pcap` | 403199 | `06c0c173f6f09841a4ad4e7c524f62d6df3a1075a40bd77025fe67949f7c15fe` |
| `talker-047/tap.pcap` | 409044 | `c4e986188f214752f093ab4e369eeb48ced4d92b1683fb122ef4316d27efb2c5` |
| `talker-048/tap.pcap` | 467106 | `db7a257aa433a13cb20fb9587e85bb18bc24344814a7b3e5d57202b64ff99c3f` |
| `talker-049/tap.pcap` | 466890 | `6f352968b65c14df5126fa840d8ee5d18161f0fa30e28646bd4dfabc0163471b` |
| `talker-050/tap.pcap` | 409285 | `20f58ae1b8e1b559efb0e0fdf52e84882a1a7c867f7b922790804acab07cd680` |
| `talker-051/tap.pcap` | 408538 | `e1b40be74dcc3e09d47256af1eebd633a940484ec096c4aaac6373bd4503a661` |
| `talker-052/tap.pcap` | 408676 | `4cc7983bf7dd6bb32a8ddf7e92a15cc14a558e95ee9343faeec32002049d467c` |
| `talker-053/tap.pcap` | 408867 | `45341f763d3485b2195bfd6e516ab7ff995ab79ec9718bbea9bd564fc29293ec` |
| `talker-054/tap.pcap` | 409349 | `15608291fd03f26cf4a026687186bed681ab6213b16412fc997388b9bdb3ddc1` |
| `talker-055/tap.pcap` | 409362 | `e51297021d9d69a3fbf1b1f436db3fb631c5852c8cfb835537acb639a09e1159` |
| `talker-056/tap.pcap` | 408813 | `db845df539abeb7d54d340d975e8fb4b9e9d1537759a0b596d9b15f33e9b4214` |
| `talker-057/tap.pcap` | 408848 | `bb5d2783318d62a7c18509b507a958946be91f7bab3137677732e6e0a28abc3b` |
| `talker-058/tap.pcap` | 409238 | `cc4f220864c7299ea5000f038bc5209e2c20c9c1e15b32cc66e3d7abcb7c71ba` |
| `talker-059/tap.pcap` | 406955 | `adba04f921e9d1288986ebf6b49c20f23f91ee8347781d7ff1dd03b5ce2ff903` |
| `talker-060/tap.pcap` | 409465 | `5362d9657ada63742d94580b4572edf08fb1ffa4c7827771f37a079c50ec1472` |
| `talker-061/tap.pcap` | 403239 | `2fb27ebcccd2e288d02d7ec54ab2aca07870594506f96652b64beb01a96e51d0` |
| `talker-062/tap.pcap` | 409196 | `b4e5dfbfe9db76299873e3649813469f6af63672995434edcd40b6b9c340cfa9` |
| `talker-063/tap.pcap` | 408209 | `85dc93782c6afbdc548616d32a44cc378fb9ceec5c9b5b99b33d302e4894066f` |
| `talker-064/tap.pcap` | 410297 | `7ea87ab251e7c6d388de8f3b19e84c4348837456e655c44f567b24893be9fb07` |
| `talker-065/tap.pcap` | 410459 | `252152589ee339c37409638bdaa2b21af98885da769aeea119f74aa6ce4bc99c` |
| `talker-066/tap.pcap` | 409298 | `5e04ad973adf0871561b9fe2e2a84f9c9bc525370718144904c94fc4b0520e78` |
| `talker-067/tap.pcap` | 408156 | `ebf7fe3ad6901165f9e77d0dabc1c85f88cbc61f26d19cb41c363d6408f3dcd0` |
| `talker-068/tap.pcap` | 408176 | `f4881d29cfab316638e39b31e6b68c46478d0a5d393ed44d04bf75b6df68ad1f` |
| `talker-069/tap.pcap` | 411164 | `ea05bc45514a8439d7eb6c1a6d25145baa0a74dafd17030217ed8732ae481de5` |
| `talker-070/tap.pcap` | 410034 | `c010101263ce24ef860129855f3adee7eeb62bca52f5bca43dfebaa436140231` |
| `talker-071/tap.pcap` | 351192 | `38cd122bbb6911ebe8a8c9112b81728a7fbd098394642e1cc6dd69add9285642` |
| `talker-072/tap.pcap` | 409231 | `a9ddca916b127d8166e88d6fefa4db00e28657dc2e3c653e2232a9d3d9eede9b` |
| `talker-073/tap.pcap` | 412568 | `f605f2bcce0a5bd04cc569d35be66f5ea61e0745dd65c46f09158632f209f027` |
| `talker-074/tap.pcap` | 409903 | `bd481f98772b11b3dd6ead8d496a83d991af56f0a75044c9d529296aac276d2b` |
| `talker-075/tap.pcap` | 518170 | `c661241be214f2281d170592fb7d839a61ffd4bf78b279f1bd939f5fc4cdf9d0` |
| `talker-076/tap.pcap` | 410395 | `bb61b170f54f638176d2cc548e3dbdedcf44207d29cf05f56fe4b76a1cc3bff1` |
| `talker-077/tap.pcap` | 411446 | `8751cde18d56c691dc9e0086aa55735545f09e29d9733da02f6a92b7781a7f51` |
| `talker-078/tap.pcap` | 410382 | `46dab10765356412496ecd7ed87aba8ede7239f68243110931123ab1f5b6173c` |
| `talker-079/tap.pcap` | 409559 | `2a584ade8bd1e053fe2e11968e200345a8c3c6484b8a5d9715a8897c667bd3d6` |
| `talker-080/tap.pcap` | 409907 | `8a4168267d8addd2b316286434615f82a27c40f3b85127e8dc5f1dc5862a5668` |
| `talker-081/tap.pcap` | 409150 | `9d4a499d5f3efaf3a2e84a3316e66d55d9e938d3af30b97da76f2a30b52a5242` |
| `talker-082/tap.pcap` | 411095 | `d31e2598d7199ec9cfe887fa9407fe1fec95e3aead3094cf6e4cb79decf193e8` |
| `talker-083/tap.pcap` | 524681 | `302bb4dccbbad01947a8b28432ea2dacd0e56e922b6c581ec3f62f7095470a6f` |
| `talker-084/tap.pcap` | 409754 | `28b26e58d759961799a349af8ac467e6119ffa671b8adb7ae171abcff2162745` |
| `talker-085/tap.pcap` | 408421 | `7ae25d693b3d38ea09ba0d5838f0158b01c592a2c6d00e465b215421606f89db` |
| `talker-086/tap.pcap` | 411186 | `a27ed64270c8495b1440c437bc6612c6ab09205adf83cb063a42836afb144e22` |
| `talker-087/tap.pcap` | 409960 | `aa734d863411f3372e117e886510c09ad026611237dff81d2ef6b8c1155926d4` |
| `talker-088/tap.pcap` | 408880 | `fb95414de9f0687186b6164de7b77705f10436a8fc7040013c5cdb2196c84306` |
| `talker-089/tap.pcap` | 410143 | `8978bd719fcb4f28edcee9e039de9a8990ab7ac19e7c703d2d7abc4cf6f39875` |
| `talker-090/tap.pcap` | 404507 | `8fc0976677448e3c20af4ecb934e5b7648b44410cd61e7f246280aac324f3e05` |
| `talker-091/tap.pcap` | 408813 | `c779d41627d2117fa34bca45907bc6779743668ed4a48b45263848673a34eb03` |
| `talker-092/tap.pcap` | 408934 | `5d7a00e26696f8cc5a6c0196b57a06d9edd73e02277e3a95f004a2d6ad5dfc0d` |
| `talker-093/tap.pcap` | 409355 | `74d9bec260a91087026badea6f02a0529f05f88e3ff7bba4088582f45515ff70` |
| `talker-094/tap.pcap` | 409198 | `7afee1bcf0969eab0c1c004a10762d7c35d06f637f3707047f9a94b96390ab84` |
| `talker-095/tap.pcap` | 408637 | `1214be8dd166075f52fc2369a955c1606dde89fbf749e915a8ef2f5fffe7b43d` |
| `talker-096/tap.pcap` | 409064 | `b8142146bc5cb0ba9179ad651354b8514c40dcf9fdc85c86751bc3bf47507c4a` |
| `talker-097/tap.pcap` | 409520 | `7bb4054135059d8b177b7e83177e31dd97302f7a12cc416bb89bbcae59c3ba76` |
| `talker-098/tap.pcap` | 409161 | `050c909a96df54e63d5e5557439ce897fad24cf1585d30d002fd1db91db61e11` |
| `talker-099/tap.pcap` | 409350 | `9b5c24ff044ef43052a9cc86c8f3d8a8145de072fd7f9bfc043fd907b536c782` |
| `talker-100/tap.pcap` | 409198 | `444cef0c7d8ef31cb50fbb6c5d23c68c96ba1da171edde868ef5d60ea88ec653` |
| `talker-restore/tap.pcap` | 170920 | `519b8373f1f8046203b2ee11baebcd7ec1b2c6ed2d55c5dfec22e97898735b5f` |
| `talker-setup/tap.pcap` | 226353 | `e7e37fc1244b844cfeeb7d5961240d794c77a0f7716b0148ae8bc581bbb377a2` |

| Method artifact | Bytes | SHA-256 |
|---|---|---|
| `tools/action.py` | 8236 | `fab53317cd781a8a8a8a2edddfa057582a20c25b488044c472123b56444fc52e` |
| `tools/analyze.py` | 7310 | `1f0583b90d0583c0fc7c417443804942399f62a27ede278a89d2baf1195e3490` |
| `tools/reconnect.py` | 945 | `7c4ae93fc2f6f416fa6940b0fea308ba8f8420da742a2fb74228d793282ec2f3` |
| `tools/capture.py` | 674 | `2601b03e16c0caa7c13f170a7316d7262a9f9bc4cc265dcba881165364a1fb61` |
| `tools/controller.py` | 4277 | `324ef73599de85abe7e3dff10c5c8de35863a60aa2e3995413085e0d228d11ad` |
| `tools/avdecc_ro.py` | 10263 | `172836966609645d6e12adf19a8341a145a4dadc51edb81c6d29a23aae1fd75a` |
| `tools/wire_summary.py` | 10371 | `7a8af475fa5f8bfbb90636b92bf9d07a86140c54a9be10c12f9b76235bccd922` |
| `tools/integrity.py` | 2758 | `a50bdb446146e9fdb81f969fb6e63e59fb3f4cb61dd6f14dfcde2063c820e9f7` |
| `tools/report.py` | 15816 | `fe76a7aec28831bcded7cd868decde73f44eb43a8fa3146826aeb6aa37e1ef7e` |

The handoff packet contains acquisition and analysis source.
It also contains transcripts, decoded events, and manifests.

## Validation

All nine assigned gates return zero.
Commands run from the physical candidate worktree without pipelines.

| Command | Return code |
|---|---|
| `python3 scripts/docs_check.py` | 0 |
| `python3 scripts/check_doc_style.py` | 0 |
| `python3 scripts/gen_toc.py --check` | 0 |
| `python3 scripts/check_em_dash.py --base 8bc97021` | 0 |
| `python3 scripts/check_doc_paths.py` | 0 |
| `python3 scripts/ci_scope.py --selftest` | 0 |
| `python3 scripts/check_baremetal_only.py --check` | 0 |
| `python3 scripts/check_feature_status.py --self-test` | 0 |
| `git diff --check` | 0 |

Pinned Markdown dependencies run outside the retained evidence packet.
All 206 captures replay successfully with final analysis source.

Live and replayed response-to-AVTP measurements agree.
All captures report zero capture-host packet drops.

No parsing errors or timestamp reversals appear.
The handoff records exact commands, return codes, and local head.

Reproduce analysis with the retained `analyze.py` and capture index.
Rebuild the page with retained `report.py`.

Bench retention follows [TESTING.md section 6b](../testing/TESTING.md#6b-bench-evidence-retention).
All bench changes require complete restoration before handoff.
