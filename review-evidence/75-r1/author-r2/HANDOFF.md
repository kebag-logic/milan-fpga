# Round 2 handoff

Author: [A389]. PR #604, refs #75.

Status: complete for round-2 author handoff; REVIEW READY posted.
Starting head: `0e8ec0d2bd78b1d87f84d96e095966ae7c07c525`.
Round-2 head: `5c7577e51702b00683a121f97a9806c167eb072b`.

The assignment is [itemized publicly](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860261220).
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860271442
Only the assigned findings page and findings index change.
The original operator and review packets remain read-only.
All computation uses recorded data; no bench action occurred.
No push, PR edit, merge, or issue closure is authorized.

## Per-item response

| Assignment / review | Changed artifact | Response and verification |
|---|---|---|
| 1: R370-F1; R371-F3 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:64` | Replaced the submodule-relative link with the upstream URL pinned at the gitlink. Exact-head documentation gates with submodules, without submodules, and without Git metadata are required below. |
| 2: R370-F2; R371-F2 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:558` | All 200 attempts now publish settled-window and command-response PDU counts plus DUT and active-talker start/stop deltas. The three failed stop assertions classify talker 13, 24, and 75 as non-restarts. |
| 2: count reconciliation | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:831` | The +97/+97 setup-to-restore counters equal 97 one/one per-cycle increments and three zero/zero increments. The reference talker totals +100/+100. Counter continuity between adjacent cycles is verified. |
| 2: quantiles and count | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:169` | Only 100 listener and 97 talker restarts enter quantiles. The 100-cycle talker requirement remains unmet, with the non-stop behavior retained under #75. No early-resumption censoring case occurs. |
| 2: capture sizes | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:791` | The six largest talker captures are decomposed into CRF and other stored bytes. Cycles 24/75 include the continuous hold, cycle 13 also has a shorter tail, and cycles 48/49/83 have longer tails. |
| 3: R371-F1; R370-F3 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:871` | Criteria 1 and 2 name the two CRF pairs and disconnect/two-second-hold/reconnect sequence. The 6.889-second initial bind appears as an open exception outside criterion 1, with the decision and #606 links. |
| 3: DUT-side difference | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:211` | No DUT Talker Advertise precedes the initial bind; the first arrives at +0.079237250 seconds. The bridge first emits MSRP as LeaveAll at +6.080007742 seconds. Recorded reconnection holds retain DUT Talker Advertise. |
| 4: R371-F4; R370-S3 | `docs/findings/README.md:11` | Added the current-entry row, including measured scope, three non-restarts, initial-bind exception, and unmeasured AAF. |
| Taken R370-S1 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:227` | Added Student-t 95% OLS slope intervals, original cycle-number treatment, interval assumptions, effect bounds, and cycle-one sensitivity. Recomputed the affected block medians. |
| Taken R370-S2 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:99` | Recorded the complete implemented predicate and two timing resolutions. The response anchor is its tap crossing. The original mask ignores mr bit 3, fs, and tu; replay proves all were zero. This corrects the review description of mr without changing the retained predicate. |
| Taken R370-S4 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:851` | Disclosed the all-zero to MAAP-range dynamic destination change, distinct from restored bindings/settings. The initial and final 18-state key sets match and all are unbound. |

## Stop checks per cycle

`recompute.py` opens raw captures and source records read-only.
Every raw capture matches its retained size and SHA-256.
Every original timing interval reproduces exactly.

Settled window: [disconnect-response + 0.5 s, reconnect-response).
The 0.5-second allowance defines analysis, not a protocol deadline.
Command-response counts are the subset omitted by the original check.
The original last-half-second counts also reproduce exactly.
Counter pairs are STREAM_START / STREAM_STOP increments.
DUT counters refer to output 1; active-talker counters follow direction.

All 197 demonstrated restarts pass the zero-PDU assertion.
Their active-talker counters each advance one start and one stop.
The other three assertions fail and those attempts are excluded.
Their continuous progression has a maximum gap of 0.002000053 seconds.
Each contains 1,000 valid PDUs across the two-second hold.
Each has 250 PDUs in the original last-half-second window.
Their start/stop deltas are zero, matching the continuous traffic.
No counter defect or early-resumption case is needed to explain them.

| Direction | Cycle | Settled PDUs | Command-response PDUs | DUT start/stop | Active talker start/stop | Stop check |
|---|---|---|---|---|---|---|
| DUT listener | 1 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 2 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 3 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 4 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 5 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 6 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 7 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 8 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 9 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 10 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 11 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 12 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 13 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 14 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 15 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 16 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 17 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 18 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 19 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 20 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 21 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 22 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 23 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 24 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 25 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 26 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 27 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 28 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 29 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 30 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 31 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 32 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 33 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 34 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 35 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 36 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 37 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 38 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 39 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 40 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 41 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 42 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 43 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 44 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 45 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 46 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 47 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 48 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 49 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 50 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 51 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 52 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 53 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 54 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 55 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 56 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 57 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 58 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 59 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 60 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 61 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 62 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 63 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 64 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 65 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 66 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 67 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 68 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 69 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 70 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 71 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 72 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 73 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 74 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 75 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 76 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 77 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 78 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 79 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 80 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 81 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 82 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 83 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 84 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 85 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 86 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 87 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 88 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 89 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 90 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 91 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 92 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 93 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 94 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 95 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 96 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 97 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 98 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 99 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 100 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT talker | 1 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 2 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 3 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 4 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 5 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 6 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 7 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 8 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 9 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 10 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 11 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 12 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 13 | 754 | 4 | 0 / 0 | 0 / 0 | FAIL |
| DUT talker | 14 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 15 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 16 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 17 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 18 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 19 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 20 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 21 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 22 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 23 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 24 | 754 | 4 | 0 / 0 | 0 / 0 | FAIL |
| DUT talker | 25 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 26 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 27 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 28 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 29 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 30 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 31 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 32 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 33 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 34 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 35 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 36 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 37 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 38 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 39 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 40 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 41 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 42 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 43 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 44 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 45 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 46 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 47 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 48 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 49 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 50 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 51 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 52 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 53 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 54 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 55 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 56 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 57 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 58 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 59 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 60 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 61 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 62 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 63 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 64 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 65 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 66 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 67 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 68 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 69 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 70 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 71 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 72 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 73 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 74 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 75 | 755 | 5 | 0 / 0 | 0 / 0 | FAIL |
| DUT talker | 76 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 77 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 78 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 79 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 80 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 81 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 82 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 83 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 84 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 85 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 86 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 87 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 88 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 89 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 90 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 91 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 92 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 93 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 94 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 95 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 96 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 97 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 98 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 99 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 100 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |

## Recomputed distribution

Times are seconds. p95 uses nearest rank.
Initial binds and non-restarts are excluded.
No other attempt is omitted, and original cycle numbers are retained.

| Direction | Attempts | Demonstrated restarts | Min | Median | p95 | Max |
|---|---|---|---|---|---|---|
| DUT listener | 100 | 100 | 0.006641168 | 0.1102795055 | 0.188503018 | 0.204858977 |
| DUT talker | 100 | 97 | 0.017426921 | 0.0191746130 | 0.042346644 | 0.117736084 |

Listener results remain unchanged.
Talker minimum changes from 0.000296777 to 0.017426921 seconds.
Talker median changes from 0.019165141 to 0.019174613 seconds.
Talker p95 changes from 0.039613701 to 0.042346644 seconds.
Its maximum remains 0.117736084 seconds.
The exclusion removes three lowest original values.
The 100-restart talker requirement remains unmet under #75.

| Direction | OLS slope, s/cycle | 95% slope interval | Upper change, ms/100 cycles |
|---|---|---|---|
| DUT listener | -0.000099788 | [-0.000501182, +0.000301607] | 30.161 |
| DUT talker | -0.000019700 | [-0.000133251, +0.000093851] | 9.385 |

Both intervals include zero; the blocks show no progressive slowdown.
These are descriptive Student-t OLS intervals, not future guarantees.
They assume independent errors with constant variance.
Dropping talker cycle 1 changes its slope to +0.000040905 s/cycle.

## Large capture reconciliation

Each CRF record contributes 108 stored bytes.
Total bytes equal CRF bytes plus other bytes plus 24.
The median talker capture span is 8.998121 seconds.
The median tail is 3.954053 seconds after the post-response PDU.

| Talker cycle | Bytes | Span, seconds | Tail, seconds | CRF PDUs | CRF bytes | Other bytes | Explanation |
|---|---|---|---|---|---|---|---|
| 83 | 524681 | 10.998148 | 5.964080 | 4491 | 485028 | 39629 | Longer capture tail |
| 24 | 518465 | 8.998121 | 3.956053 | 4500 | 486000 | 32441 | Continuous hold |
| 75 | 518170 | 8.998121 | 3.946053 | 4500 | 486000 | 32146 | Continuous hold |
| 48 | 467106 | 9.998134 | 4.958067 | 3993 | 431244 | 35838 | Longer capture tail |
| 49 | 466890 | 9.998134 | 4.960067 | 3991 | 431028 | 35838 | Longer capture tail |
| 13 | 461102 | 7.998107 | 3.004040 | 4000 | 432000 | 29078 | Continuous hold; shorter tail |

## Initial bind and restoration

`verify_disclosures.py` verifies the retained setup and census records.
`disclosures.json` records the exact numbers and source hashes.
The initial bind takes 6.889398468 seconds and belongs to #606.
The recorded decision excludes it from reconnect criterion 1.
Its lack of preceding disconnect/hold also excludes it from quantiles.
The DUT declaration difference and bridge silence remain explicit.

Both censuses contain the same 18 unbound stream-state keys.
DUT output 1 changes from all-zero to MAAP-range destination.
This runtime residue does not change restored settings or bindings.
No physical restoration was attempted during this analysis round.

## Gates

All assigned commands return zero at the committed head above.
Each runs synchronously, without pipelines, from the physical candidate.
The candidate contains the three pinned validation submodules.
The documentation renderer uses the repository's hash-pinned dependencies.
The bare-metal gate uses the base interpreter with PyYAML 6.0.3.

The first bare-metal invocation refused missing PyYAML, rc 2.
Its setup receipt remains in `gate-baremetal-initial.txt`.
The unchanged gate then passes using the existing base interpreter.
No repository source, validator, or acceptance criterion was changed.
Previously successful exact-head results were retained, not rerun.

The requested submodule-free checks use one disposable local validation clone.
It is pinned to the committed head before either check runs.
The second check removes that clone's Git metadata.
Both return zero; the disposable clone is then removed.
This clone was solely for the explicitly requested gate comparison.
It was never an implementation lane or another existing checkout.
No hosted-context pass is claimed without a push.

| Command / context | Head | Return code |
|---|---|---|
| `python3 scripts/docs_check.py (pinned submodules present)` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/check_doc_style.py` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/gen_toc.py --check` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/check_em_dash.py --base 8bc97021` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/check_doc_paths.py` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/ci_scope.py --selftest` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/check_baremetal_only.py --check` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/check_feature_status.py --self-test` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `git diff --check` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `git diff --check 8bc97021 HEAD` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/docs_check.py (no submodules)` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| `python3 scripts/docs_check.py (no submodules or Git metadata)` | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |
| Every Markdown table rendered; all cells preserved | `5c7577e51702b00683a121f97a9806c167eb072b` | 0 |

`gates.json` and individual gate receipts record every result.
`table-render-check.json` records every table's dimensions and file hashes.
Direct page prose analysis also reports zero findings.
The complete committed diff passes its additional whitespace check.

## Delivery

`PR-BODY.md` retains its [A386] first line and `Refs #75`.
It contains the requested Round 2 section and corrected claims.
Local commit: `5c7577e51702b00683a121f97a9806c167eb072b`. REVIEW READY posted.
Only the authorized TAKEN and REVIEW READY comments were posted.
REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860418078
The published body was read back and matches REVIEW-READY.md exactly.
No review verdict is supplied by the author.
Issue #75 stays open; AAF is unmeasured; #606 owns first bind.
