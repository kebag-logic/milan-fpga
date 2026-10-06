<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Talker startup and soak observations

Refs #667. Operator [A549]. These are operator observations.

The [B13 assignment](https://github.com/kebag-logic/milan-fpga/issues/667#issuecomment-6009837251) defines this findings-only lane.
The assigned image is dev `28f9666f`, seed `asl`.

## Contents

- **[#667 bench: talker start on dev 28f9666f, 2026-10-06](#667-bench-talker-start-on-dev-28f9666f-2026-10-06)** -- Records the startup measurements and their limits.
- **[Soak record](#soak-record)** -- Records periodic counters and retained stream captures.
- **[Method and authorities](#method-and-authorities)** -- Defines field decoding and counter interpretation.
- **[Restoration and evidence](#restoration-and-evidence)** -- Records final readbacks and reproducible checks.

## #667 bench: talker start on dev 28f9666f, 2026-10-06

The four assigned ATDECC identity fields matched.
Console VERSION `0x00020060` and AEM CRC `5ba355eb` also matched.

All 100 binds and unbinds succeeded.
Each bind held the DUT talker for two seconds.
The reference peer reported EARLY in 14 binds.
The total EARLY count was 14.
LATE remained zero across all 100 binds.

All 14 EARLY-positive binds had backward first-to-second timestamp steps.
Those steps ranged from -544,469,385 to -279,759,747 ns.
The other 86 steps ranged from 124,999 to 125,020 ns.
Each increment was observed before unbind submission.
The observation lead was at least 1,900.062 ms.

The startup behavior remains observable on this image.
The [B12 characterization](653_DISCONNECT_ORDER_BENCH.md#b12-startup-characterization-2026-10-05) found two affected binds among 70.
Its first-to-second steps were -23,612,829 ns and +521,369,096 ns.
[PR #666](https://github.com/kebag-logic/milan-fpga/pull/666) records that earlier evidence.
These batches describe observations; they establish no rate trend.

Every bind retains its first ten AAF headers.
All 1,000 headers have `tv=1` and `tu=0`.
Sequence progression remains consecutive within every captured start.

First-step distribution:

| First-to-second step (ns) | Binds |
|---|---|
| -544469385 | 1 |
| -525219402 | 1 |
| -514427479 | 1 |
| -469614986 | 1 |
| -440885596 | 1 |
| -408572750 | 1 |
| -399510151 | 1 |
| -384031016 | 1 |
| -344551596 | 1 |
| -324968196 | 1 |
| -318822282 | 1 |
| -315197278 | 1 |
| -309197187 | 1 |
| -279759747 | 1 |
| 124999 | 61 |
| 125000 | 22 |
| 125019 | 1 |
| 125020 | 2 |

The next table reports every bind independently.
A step is the signed timestamp difference, PDU 2 minus PDU 1.
The offset is the steady period minus that step.
The packet also retains each header against PDU 10's trend.

| Cycle | EARLY | LATE | First sequence | First step (ns) | First offset (ns) |
|---|---|---|---|---|---|
| 001 | 0 | 0 | 248 | 125000 | -1.0 |
| 002 | 0 | 0 | 94 | 124999 | 0.0 |
| 003 | 0 | 0 | 250 | 124999 | 0.0 |
| 004 | 0 | 0 | 161 | 124999 | 0.0 |
| 005 | 0 | 0 | 74 | 124999 | 0.0 |
| 006 | 0 | 0 | 238 | 124999 | 0.0 |
| 007 | 1 | 0 | 213 | -469614986 | 469739985.0 |
| 008 | 0 | 0 | 138 | 124999 | 0.0 |
| 009 | 0 | 0 | 38 | 124999 | 0.0 |
| 010 | 0 | 0 | 189 | 125000 | -1.0 |
| 011 | 0 | 0 | 98 | 124999 | 0.0 |
| 012 | 0 | 0 | 23 | 124999 | 0.0 |
| 013 | 0 | 0 | 188 | 124999 | 0.0 |
| 014 | 0 | 0 | 101 | 124999 | 0.0 |
| 015 | 0 | 0 | 9 | 124999 | 0.0 |
| 016 | 0 | 0 | 173 | 124999 | 0.0 |
| 017 | 0 | 0 | 145 | 124999 | 0.0 |
| 018 | 1 | 0 | 56 | -525219402 | 525344401.0 |
| 019 | 0 | 0 | 222 | 124999 | 0.0 |
| 020 | 0 | 0 | 126 | 124999 | 0.0 |
| 021 | 0 | 0 | 28 | 124999 | 0.0 |
| 022 | 0 | 0 | 168 | 125020 | -21.0 |
| 023 | 0 | 0 | 76 | 124999 | 0.0 |
| 024 | 0 | 0 | 240 | 124999 | 0.0 |
| 025 | 0 | 0 | 148 | 125000 | -1.0 |
| 026 | 0 | 0 | 56 | 124999 | 0.0 |
| 027 | 1 | 0 | 218 | -440885596 | 441010595.0 |
| 028 | 0 | 0 | 127 | 125000 | -1.0 |
| 029 | 0 | 0 | 37 | 124999 | 0.0 |
| 030 | 0 | 0 | 199 | 125019 | -20.0 |
| 031 | 0 | 0 | 99 | 125000 | -1.0 |
| 032 | 1 | 0 | 7 | -514427479 | 514552478.0 |
| 033 | 0 | 0 | 170 | 124999 | 0.0 |
| 034 | 1 | 0 | 78 | -544469385 | 544594384.0 |
| 035 | 0 | 0 | 242 | 124999 | 0.0 |
| 036 | 0 | 0 | 150 | 124999 | 0.0 |
| 037 | 0 | 0 | 58 | 125000 | -1.0 |
| 038 | 0 | 0 | 233 | 124999 | 0.0 |
| 039 | 0 | 0 | 164 | 125000 | -1.0 |
| 040 | 0 | 0 | 72 | 124999 | 0.0 |
| 041 | 0 | 0 | 60 | 125020 | -21.0 |
| 042 | 0 | 0 | 216 | 125000 | -1.0 |
| 043 | 0 | 0 | 124 | 124999 | 0.0 |
| 044 | 0 | 0 | 106 | 124999 | 0.0 |
| 045 | 0 | 0 | 16 | 124999 | 0.0 |
| 046 | 0 | 0 | 180 | 124999 | 0.0 |
| 047 | 0 | 0 | 91 | 124999 | 0.0 |
| 048 | 0 | 0 | 255 | 124999 | 0.0 |
| 049 | 0 | 0 | 166 | 124999 | 0.0 |
| 050 | 0 | 0 | 74 | 125000 | -1.0 |
| 051 | 0 | 0 | 238 | 124999 | 0.0 |
| 052 | 0 | 0 | 148 | 124999 | 0.0 |
| 053 | 0 | 0 | 58 | 124999 | 0.0 |
| 054 | 0 | 0 | 222 | 124999 | 0.0 |
| 055 | 1 | 0 | 130 | -279759747 | 279884746.0 |
| 056 | 0 | 0 | 38 | 125000 | -1.0 |
| 057 | 0 | 0 | 202 | 124999 | 0.0 |
| 058 | 0 | 0 | 101 | 125000 | -1.0 |
| 059 | 1 | 0 | 11 | -324968196 | 325093195.0 |
| 060 | 0 | 0 | 178 | 124999 | 0.0 |
| 061 | 0 | 0 | 89 | 125000 | -1.0 |
| 062 | 0 | 0 | 248 | 124999 | 0.0 |
| 063 | 0 | 0 | 156 | 124999 | 0.0 |
| 064 | 0 | 0 | 64 | 125000 | -1.0 |
| 065 | 1 | 0 | 230 | -315197278 | 315322277.0 |
| 066 | 0 | 0 | 5 | 124999 | 0.0 |
| 067 | 0 | 0 | 169 | 124999 | 0.0 |
| 068 | 0 | 0 | 77 | 124999 | 0.0 |
| 069 | 0 | 0 | 239 | 124999 | 0.0 |
| 070 | 0 | 0 | 149 | 124999 | 0.0 |
| 071 | 1 | 0 | 49 | -408572750 | 408697749.0 |
| 072 | 1 | 0 | 213 | -384031016 | 384156015.0 |
| 073 | 1 | 0 | 116 | -399510151 | 399635150.0 |
| 074 | 0 | 0 | 24 | 124999 | 0.0 |
| 075 | 0 | 0 | 194 | 125000 | -1.0 |
| 076 | 0 | 0 | 102 | 124999 | 0.0 |
| 077 | 0 | 0 | 12 | 124999 | 0.0 |
| 078 | 0 | 0 | 176 | 125000 | -1.0 |
| 079 | 0 | 0 | 88 | 124999 | 0.0 |
| 080 | 1 | 0 | 4 | -344551596 | 344676595.0 |
| 081 | 0 | 0 | 168 | 124999 | 0.0 |
| 082 | 0 | 0 | 76 | 124999 | 0.0 |
| 083 | 0 | 0 | 240 | 125000 | -1.0 |
| 084 | 0 | 0 | 251 | 124999 | 0.0 |
| 085 | 0 | 0 | 159 | 124999 | 0.0 |
| 086 | 0 | 0 | 62 | 124999 | 0.0 |
| 087 | 0 | 0 | 228 | 124999 | 0.0 |
| 088 | 0 | 0 | 139 | 124999 | 0.0 |
| 089 | 0 | 0 | 54 | 124999 | 0.0 |
| 090 | 0 | 0 | 225 | 124999 | 0.0 |
| 091 | 0 | 0 | 136 | 125000 | -1.0 |
| 092 | 0 | 0 | 44 | 125000 | -1.0 |
| 093 | 0 | 0 | 208 | 125000 | -1.0 |
| 094 | 0 | 0 | 124 | 125000 | -1.0 |
| 095 | 1 | 0 | 33 | -318822282 | 318947281.0 |
| 096 | 0 | 0 | 202 | 124999 | 0.0 |
| 097 | 0 | 0 | 112 | 125000 | -1.0 |
| 098 | 1 | 0 | 22 | -309197187 | 309322186.0 |
| 099 | 0 | 0 | 183 | 125000 | -1.0 |
| 100 | 0 | 0 | 94 | 124999 | 0.0 |

## Soak record

The soak ran from 05:27:00.782 to 07:27:04.752 UTC.
Its duration was 7203.971 seconds on 2026-10-06.
AAF and CRF were bound in both directions.
All 145 counter checkpoints had zero assigned error-class increases.
Grandmaster, asCapable and path observations remained unchanged.

Each checkpoint issued nine GET_COUNTERS requests.
These covered every DUT counter descriptor and both bound peer inputs.
DUT ENTITY counters consistently returned NOT_SUPPORTED.
The other eight requests consistently returned SUCCESS.
Together, they exposed 61 valid counters.

The longest checkpoint interval was 55.727 seconds.
Each checkpoint also read GET_AVB_INFO and GET_AS_PATH.
Both entities received those timing requests.
This exceeded the assigned five-minute timing cadence.

The table preserves each counter's first and last bound observation.
Input counters reset on binding, as Milan requires.
Frame-counter values can represent observation intervals, rather than packet totals.
Milan Tables 5.4 and 5.6 define that distinction.

| Role | Descriptor | Index | Counter | Start | End | Delta |
|---|---|---|---|---|---|---|
| dut | AVB_INTERFACE | 0 | LINK_UP | 1 | 1 | 0 |
| dut | AVB_INTERFACE | 0 | LINK_DOWN | 0 | 0 | 0 |
| dut | AVB_INTERFACE | 0 | GPTP_GM_CHANGED | 0 | 0 | 0 |
| dut | CLOCK_DOMAIN | 0 | LOCKED | 0 | 1 | 1 |
| dut | CLOCK_DOMAIN | 0 | UNLOCKED | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | MEDIA_LOCKED | 1 | 1 | 0 |
| dut | STREAM_INPUT | 0 | MEDIA_UNLOCKED | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | STREAM_INTERRUPTED | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | SEQ_NUM_MISMATCH | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | MEDIA_RESET | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | TIMESTAMP_UNCERTAIN | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | TIMESTAMP_VALID | 1022 | 57628169 | 57627147 |
| dut | STREAM_INPUT | 0 | TIMESTAMP_NOT_VALID | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | UNSUPPORTED_FORMAT | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | LATE_TIMESTAMP | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | EARLY_TIMESTAMP | 0 | 0 | 0 |
| dut | STREAM_INPUT | 0 | FRAMES_RX | 0 | 57624168 | 57624168 |
| dut | STREAM_INPUT | 1 | MEDIA_LOCKED | 0 | 1 | 1 |
| dut | STREAM_INPUT | 1 | MEDIA_UNLOCKED | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | STREAM_INTERRUPTED | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | SEQ_NUM_MISMATCH | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | MEDIA_RESET | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | TIMESTAMP_UNCERTAIN | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | UNSUPPORTED_FORMAT | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | LATE_TIMESTAMP | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | EARLY_TIMESTAMP | 0 | 0 | 0 |
| dut | STREAM_INPUT | 1 | FRAMES_RX | 0 | 7203 | 7203 |
| dut | STREAM_OUTPUT | 0 | STREAM_START | 1 | 1 | 0 |
| dut | STREAM_OUTPUT | 0 | STREAM_STOP | 0 | 0 | 0 |
| dut | STREAM_OUTPUT | 0 | MEDIA_RESET | 0 | 1 | 1 |
| dut | STREAM_OUTPUT | 0 | TIMESTAMP_UNCERTAIN | 0 | 0 | 0 |
| dut | STREAM_OUTPUT | 0 | FRAMES_TX | 0 | 7204 | 7204 |
| dut | STREAM_OUTPUT | 1 | STREAM_START | 1 | 1 | 0 |
| dut | STREAM_OUTPUT | 1 | STREAM_STOP | 0 | 0 | 0 |
| dut | STREAM_OUTPUT | 1 | MEDIA_RESET | 0 | 1 | 1 |
| dut | STREAM_OUTPUT | 1 | TIMESTAMP_UNCERTAIN | 0 | 0 | 0 |
| dut | STREAM_OUTPUT | 1 | FRAMES_TX | 0 | 7204 | 7204 |
| peer | STREAM_INPUT | 0 | MEDIA_LOCKED | 1 | 1 | 0 |
| peer | STREAM_INPUT | 0 | MEDIA_UNLOCKED | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | STREAM_INTERRUPTED | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | SEQ_NUM_MISMATCH | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | MEDIA_RESET | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | TIMESTAMP_UNCERTAIN | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | TIMESTAMP_VALID | 252 | 57627401 | 57627149 |
| peer | STREAM_INPUT | 0 | TIMESTAMP_NOT_VALID | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | UNSUPPORTED_FORMAT | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | LATE_TIMESTAMP | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | EARLY_TIMESTAMP | 0 | 0 | 0 |
| peer | STREAM_INPUT | 0 | FRAMES_RX | 252 | 57627401 | 57627149 |
| peer | STREAM_INPUT | 8 | MEDIA_LOCKED | 1 | 1 | 0 |
| peer | STREAM_INPUT | 8 | MEDIA_UNLOCKED | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | STREAM_INTERRUPTED | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | SEQ_NUM_MISMATCH | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | MEDIA_RESET | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | TIMESTAMP_UNCERTAIN | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | TIMESTAMP_VALID | 16 | 3601713 | 3601697 |
| peer | STREAM_INPUT | 8 | TIMESTAMP_NOT_VALID | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | UNSUPPORTED_FORMAT | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | LATE_TIMESTAMP | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | EARLY_TIMESTAMP | 0 | 0 | 0 |
| peer | STREAM_INPUT | 8 | FRAMES_RX | 16 | 3601713 | 3601697 |

There were 145 overlapping segments for each capture type.
The tap retained plain and VLAN-tagged AVTP separately.
A companion controller capture retained control traffic.
Nine segment-local sequence gaps were fully recovered by overlap.
There were no uncovered boundaries between successive stream segments.

Of 435 capture receipts, 434 included a zero drop statistic.
Segment 063's VLAN receipt omitted that statistic.
Its captured and received totals remain available.
The independent sequence and overlap receipts cover that segment.

A final AAF media-reset toggle followed the CRF-input unbind response.
The adjacent sequence numbers were 159 and 160.
That transition occurred after the completed soak window.
The packet retains the control and media boundary timestamps.

Per-checkpoint results follow.
Segment gaps refer to individual files before overlap recovery.

| Cycle | Elapsed (s) | Counter errors | Segment gaps | Recovered by overlap |
|---|---|---|---|---|
| soak-000 | 0.397 | 0 | 0 | 0 |
| soak-001 | 53.567 | 0 | 0 | 0 |
| soak-002 | 103.448 | 0 | 0 | 0 |
| soak-003 | 153.524 | 0 | 0 | 0 |
| soak-004 | 203.466 | 0 | 0 | 0 |
| soak-005 | 253.319 | 0 | 0 | 0 |
| soak-006 | 303.444 | 0 | 0 | 0 |
| soak-007 | 353.361 | 0 | 0 | 0 |
| soak-008 | 403.434 | 0 | 0 | 0 |
| soak-009 | 453.477 | 0 | 0 | 0 |
| soak-010 | 503.527 | 0 | 0 | 0 |
| soak-011 | 553.160 | 0 | 0 | 0 |
| soak-012 | 603.380 | 0 | 0 | 0 |
| soak-013 | 653.327 | 0 | 0 | 0 |
| soak-014 | 703.347 | 0 | 0 | 0 |
| soak-015 | 753.385 | 0 | 0 | 0 |
| soak-016 | 803.378 | 0 | 0 | 0 |
| soak-017 | 853.487 | 0 | 0 | 0 |
| soak-018 | 903.394 | 0 | 0 | 0 |
| soak-019 | 953.302 | 0 | 0 | 0 |
| soak-020 | 1003.381 | 0 | 0 | 0 |
| soak-021 | 1053.457 | 0 | 0 | 0 |
| soak-022 | 1103.349 | 0 | 0 | 0 |
| soak-023 | 1153.419 | 0 | 0 | 0 |
| soak-024 | 1203.453 | 0 | 0 | 0 |
| soak-025 | 1253.231 | 0 | 0 | 0 |
| soak-026 | 1303.295 | 0 | 0 | 0 |
| soak-027 | 1353.425 | 0 | 0 | 0 |
| soak-028 | 1403.449 | 0 | 0 | 0 |
| soak-029 | 1453.582 | 0 | 0 | 0 |
| soak-030 | 1503.916 | 0 | 0 | 0 |
| soak-031 | 1559.643 | 0 | 0 | 0 |
| soak-032 | 1604.485 | 0 | 0 | 0 |
| soak-033 | 1654.015 | 0 | 0 | 0 |
| soak-034 | 1703.905 | 0 | 0 | 0 |
| soak-035 | 1753.855 | 0 | 0 | 0 |
| soak-036 | 1803.623 | 0 | 0 | 0 |
| soak-037 | 1853.635 | 0 | 0 | 0 |
| soak-038 | 1903.712 | 0 | 0 | 0 |
| soak-039 | 1953.738 | 0 | 0 | 0 |
| soak-040 | 2003.558 | 0 | 0 | 0 |
| soak-041 | 2053.528 | 0 | 0 | 0 |
| soak-042 | 2103.625 | 0 | 0 | 0 |
| soak-043 | 2153.305 | 0 | 0 | 0 |
| soak-044 | 2203.284 | 0 | 0 | 0 |
| soak-045 | 2253.253 | 0 | 0 | 0 |
| soak-046 | 2303.371 | 0 | 0 | 0 |
| soak-047 | 2353.320 | 0 | 0 | 0 |
| soak-048 | 2403.292 | 0 | 0 | 0 |
| soak-049 | 2453.270 | 0 | 0 | 0 |
| soak-050 | 2503.203 | 0 | 0 | 0 |
| soak-051 | 2553.240 | 0 | 0 | 0 |
| soak-052 | 2603.246 | 0 | 0 | 0 |
| soak-053 | 2653.274 | 0 | 0 | 0 |
| soak-054 | 2703.345 | 0 | 0 | 0 |
| soak-055 | 2753.303 | 0 | 0 | 0 |
| soak-056 | 2803.188 | 0 | 0 | 0 |
| soak-057 | 2853.414 | 0 | 0 | 0 |
| soak-058 | 2903.259 | 0 | 0 | 0 |
| soak-059 | 2953.281 | 0 | 0 | 0 |
| soak-060 | 3003.228 | 0 | 0 | 0 |
| soak-061 | 3053.141 | 0 | 0 | 0 |
| soak-062 | 3103.280 | 0 | 0 | 0 |
| soak-063 | 3153.197 | 0 | 0 | 0 |
| soak-064 | 3203.347 | 0 | 0 | 0 |
| soak-065 | 3253.357 | 0 | 0 | 0 |
| soak-066 | 3304.292 | 0 | 0 | 0 |
| soak-067 | 3354.152 | 0 | 0 | 0 |
| soak-068 | 3404.173 | 0 | 0 | 0 |
| soak-069 | 3454.375 | 0 | 0 | 0 |
| soak-070 | 3504.552 | 0 | 0 | 0 |
| soak-071 | 3554.637 | 0 | 0 | 0 |
| soak-072 | 3604.849 | 0 | 0 | 0 |
| soak-073 | 3654.244 | 0 | 0 | 0 |
| soak-074 | 3704.230 | 0 | 0 | 0 |
| soak-075 | 3754.080 | 0 | 0 | 0 |
| soak-076 | 3804.124 | 0 | 0 | 0 |
| soak-077 | 3854.312 | 0 | 2 | 2 |
| soak-078 | 3903.990 | 0 | 0 | 0 |
| soak-079 | 3954.442 | 0 | 0 | 0 |
| soak-080 | 4004.646 | 0 | 0 | 0 |
| soak-081 | 4054.712 | 0 | 0 | 0 |
| soak-082 | 4105.225 | 0 | 0 | 0 |
| soak-083 | 4155.174 | 0 | 0 | 0 |
| soak-084 | 4205.220 | 0 | 0 | 0 |
| soak-085 | 4254.949 | 0 | 0 | 0 |
| soak-086 | 4304.511 | 0 | 0 | 0 |
| soak-087 | 4355.162 | 0 | 4 | 4 |
| soak-088 | 4404.665 | 0 | 0 | 0 |
| soak-089 | 4455.085 | 0 | 0 | 0 |
| soak-090 | 4504.915 | 0 | 0 | 0 |
| soak-091 | 4555.486 | 0 | 0 | 0 |
| soak-092 | 4605.039 | 0 | 0 | 0 |
| soak-093 | 4654.687 | 0 | 0 | 0 |
| soak-094 | 4704.448 | 0 | 0 | 0 |
| soak-095 | 4754.666 | 0 | 0 | 0 |
| soak-096 | 4806.299 | 0 | 0 | 0 |
| soak-097 | 4855.100 | 0 | 0 | 0 |
| soak-098 | 4903.441 | 0 | 0 | 0 |
| soak-099 | 4953.336 | 0 | 0 | 0 |
| soak-100 | 5003.494 | 0 | 0 | 0 |
| soak-101 | 5053.381 | 0 | 0 | 0 |
| soak-102 | 5103.220 | 0 | 0 | 0 |
| soak-103 | 5153.904 | 0 | 0 | 0 |
| soak-104 | 5203.837 | 0 | 0 | 0 |
| soak-105 | 5253.828 | 0 | 0 | 0 |
| soak-106 | 5303.447 | 0 | 0 | 0 |
| soak-107 | 5353.551 | 0 | 0 | 0 |
| soak-108 | 5403.754 | 0 | 0 | 0 |
| soak-109 | 5453.883 | 0 | 0 | 0 |
| soak-110 | 5503.653 | 0 | 0 | 0 |
| soak-111 | 5553.678 | 0 | 0 | 0 |
| soak-112 | 5604.084 | 0 | 0 | 0 |
| soak-113 | 5653.711 | 0 | 0 | 0 |
| soak-114 | 5703.529 | 0 | 0 | 0 |
| soak-115 | 5753.401 | 0 | 0 | 0 |
| soak-116 | 5803.489 | 0 | 0 | 0 |
| soak-117 | 5853.372 | 0 | 0 | 0 |
| soak-118 | 5903.383 | 0 | 0 | 0 |
| soak-119 | 5953.439 | 0 | 0 | 0 |
| soak-120 | 6003.436 | 0 | 0 | 0 |
| soak-121 | 6053.722 | 0 | 3 | 3 |
| soak-122 | 6103.231 | 0 | 0 | 0 |
| soak-123 | 6153.451 | 0 | 0 | 0 |
| soak-124 | 6203.304 | 0 | 0 | 0 |
| soak-125 | 6253.356 | 0 | 0 | 0 |
| soak-126 | 6303.382 | 0 | 0 | 0 |
| soak-127 | 6353.350 | 0 | 0 | 0 |
| soak-128 | 6403.427 | 0 | 0 | 0 |
| soak-129 | 6453.538 | 0 | 0 | 0 |
| soak-130 | 6503.596 | 0 | 0 | 0 |
| soak-131 | 6553.462 | 0 | 0 | 0 |
| soak-132 | 6603.486 | 0 | 0 | 0 |
| soak-133 | 6653.550 | 0 | 0 | 0 |
| soak-134 | 6703.597 | 0 | 0 | 0 |
| soak-135 | 6753.464 | 0 | 0 | 0 |
| soak-136 | 6803.424 | 0 | 0 | 0 |
| soak-137 | 6853.437 | 0 | 0 | 0 |
| soak-138 | 6903.390 | 0 | 0 | 0 |
| soak-139 | 6953.420 | 0 | 0 | 0 |
| soak-140 | 7003.397 | 0 | 0 | 0 |
| soak-141 | 7053.926 | 0 | 0 | 0 |
| soak-142 | 7104.024 | 0 | 0 | 0 |
| soak-143 | 7153.922 | 0 | 0 | 0 |
| soak-144 | 7203.970 | 0 | 0 | 0 |

## Method and authorities

Each bind read both current stream formats.
Every observed listener format already matched its talker.
The runner adapts a differing listener before binding.

The pinned controller library is `a71ffa99`.
The application counter rule is pinned at `a13db9d9`.
The library and probe were built from verified source.
Both builds returned zero.
The earlier build was absent on the controller host.

Foreground actions held the shared bench lock.
Every action had an explicit deadline.

Each tap record contains a 28-byte prefix.
Timestamp decoding uses high-word then low-word ordering.
Raw bytes independently checked the decoded field positions.
Presentation steps use signed modulo-2^32 timestamp differences.
Sequence checks use modulo-256 progression.

The steady period uses timestamp steps following the first ten PDUs.
Absolute gPTP correlation is NOT RUN.
No measured tap-to-gPTP clock mapping is available.
Counter observations bound event timing within the controller's clock.
They do not identify individual offending packets.

| Authority | Applied rule |
|---|---|
| IEEE 1722-2016, Sections 4.4.4.3 and 4.4.4.5-4.4.4.9; Clause 7 | Media reset, timestamp validity, sequence, uncertainty and AAF presentation fields. |
| IEEE 1722.1-2021, Sections 7.4.40-7.4.42 | Interface timing, path and descriptor counter readbacks. |
| IEEE 1722.1-2021, Sections 8.2.1, 8.2.4 and 8.2.5 | ACMP field identities and successful connection responses. |
| Milan v1.2, Section 5.3.7.7, Table 5.4 | Output counter meanings and observation intervals. |
| Milan v1.2, Section 5.3.8.10, Table 5.6 | Input counter meanings and reset upon binding. |

## Restoration and evidence

The final survey matched all 42 effective-state observations.
Both descriptor inventories also matched.
All eighteen final binding readbacks were zero.
All eighteen stream formats matched their saved values.
Both source selections and all four mapping fingerprints matched.

The documented source-release sequence restored the idle servo state.
Final MCSRV_STAT was `0x00000020`; MCSRV_CTRL was zero.
The audio control and status readback matched its initial bytes.

NVM image sequence advanced from 230 to 233.
Successful commits advanced from zero to 3.
Failed commits, dirty and stale state remained zero.
Those monotonic bookkeeping values were retained, rather than reset.

Both controller sessions deregistered from both entities successfully.
Every temporary capture and probe process exited.
The bench lock was released and checked free.
Host prerequisites remained present at final readback.

The local packet is `667-b13-a549`.
It includes per-cycle headers, counter receipts and restoration comparisons.
Its manifest covers the bounded files.
Large captures remain outside the packet under `/tmp`.
Their index records each size and SHA-256 value.
The decoder and restoration checks passed 22 offline controls.

| Packet receipt | Bytes | SHA-256 |
|---|---|---|
| build-provenance.json | 910 | 47366077be37e22b1a5c6731fb81d4bc339aff638a0ca41759ed0489be822f89 |
| counter-deltas.csv | 2827 | a846cf59d5f52529488b10898b9aad27b285dfd2a6122ef959aba700c7cd7fc5 |
| soak-cycles.csv | 8463 | e9b11f061f4a936fbd24d08f97e8e4a3a8b54fd51c42cf9612931cc2c6ff6ced |
| startup-cycles.csv | 8583 | ef5a62eef6a4f5e291fab775bec9b99b22411e39a16b4ecf01bd53779d030954 |
| startup-first-ten.csv | 87664 | 93ee8e07d0afd26eb6b76bdbeaa04ed972d12de1909ee1175bd1063d41fa8083 |
| restore-summary.json | 1042 | 11517eba0e5f6dda5a49c8147a8d916ff4fa040ef23c19b579d962addcbf9f59 |
| capture-artifacts.jsonl | 133424 | 6617b12a30532a1157d758c8749247eaf2337d09a72c8af6c42356e58320ebfb |
