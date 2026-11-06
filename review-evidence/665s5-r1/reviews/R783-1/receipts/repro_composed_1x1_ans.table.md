### 1x1, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm answering

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|
| H-ADP | 7 | 1 | 0 | - | 21.265 (20) **over its bound**, `hooks-load-counters.service.adp.last.if0`, margin 1978.7 of 2000 | 0 (0) | 0 |
| H-DISC | 0 | 0 | 0 | - | - | 0 (0) | 0 |
| H-ACMP | 12 | 9 | 0 | - | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -163.3 of 200 | 40 (0) | 0 |
| H-AECP | 6 | 3 | 0 | - | 85.818 (20) **over its bound**, `backlog-owed.service.aecp.last.if0`, margin 154.2 of 240 | 0 (0) | 0 |
| H-NOTIFY | 0 | 0 | 0 | - | - | 0 (0) | 0 |
| H-COUNTERS | 1 | 1 | 0 | - | 20.761 (20) **over its bound**, `counters.loaded.if0`, margin 979.2 of 1000 | 0 (0) | 0 |
| H-MAAP | 6 | 1 | 0 | - | 21.250 (20) **over its bound**, `hooks-load-counters.service.maap.last.if0`, margin 478.8 of 500 | 7 (0) | 0 |
| H-SRP | 6 | 3 | 0 | - | 68.053 (18) **over its bound**, `hooks-load-counters.service.srp.last.if0`, margin 111.9 of 180 | 0 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound ms | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-ACMP | `backlog-owed.service.acmp.first.if0` | backlog-owed | 0 | 4.435 | 443,540 | 0 | 20 | yes | 1,556,460 | yes | 195.565 of 200 |
| H-ACMP | `backlog-owed.service.acmp.last.if0` | backlog-owed | 0 | 24.542 | 2,454,209 | 0 | 20 | NO | -454,209 | yes | 175.458 of 200 |
| H-ACMP | `backlog.acmp_command.if0` | backlog | 0 | 22.573 | 2,257,321 | 0 | 20 | NO | -257,321 | yes | 177.427 of 200 |
| H-ACMP | `backlog.owed.if0` | backlog-owed | 0 | 77.837 | 7,783,654 | 0 | 20 | NO | -5,783,654 | yes | 122.163 of 200 |
| H-ACMP | `backlog.owed_behind0.if0` | backlog-owed | 0 | never | 36,330,711 | 0 | 20 | NO | -1 | yes | -163.307 of 200 |
| H-ACMP | `backlog.owed_behind1.if0` | backlog-owed | 0 | never | 36,330,636 | 0 | 20 | NO | -1 | yes | -163.306 of 200 |
| H-ACMP | `backlog.owed_behind2.if0` | backlog-owed | 0 | never | 36,330,561 | 0 | 20 | NO | -1 | yes | -163.306 of 200 |
| H-ACMP | `backlog.owed_behind3.if0` | backlog-owed | 0 | never | 36,330,486 | 0 | 20 | NO | -1 | yes | -163.305 of 200 |
| H-ACMP | `backlog.service.acmp.first.if0` | backlog | 0 | 5.373 | 537,331 | 0 | 20 | yes | 1,462,669 | yes | 194.627 of 200 |
| H-ACMP | `backlog.service.acmp.last.if0` | backlog | 0 | 25.013 | 2,501,342 | 0 | 20 | NO | -501,342 | yes | 174.987 of 200 |
| H-ACMP | `hooks-load-counters.service.acmp.first.if0` | hooks-load-counters | 0 | 4.496 | 449,599 | 0 | 20 | yes | 1,550,401 | yes | 195.504 of 200 |
| H-ACMP | `hooks-load-counters.service.acmp.last.if0` | hooks-load-counters | 0 | 29.646 | 2,964,623 | 0 | 20 | NO | -964,623 | yes | 170.354 of 200 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 4.478 | 447,799 | 0 | 20 | yes | 1,552,201 | yes | 1995.522 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if0` | backlog-owed | 0 | 18.169 | 1,816,859 | 0 | 20 | yes | 183,141 | yes | 1981.831 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 5.805 | 580,474 | 0 | 20 | yes | 1,419,526 | yes | 1994.195 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 5.416 | 541,590 | 0 | 20 | yes | 1,458,410 | yes | 1994.584 of 2000 |
| H-ADP | `backlog.service.adp.last.if0` | backlog | 0 | 18.328 | 1,832,833 | 0 | 20 | yes | 167,167 | yes | 1981.672 of 2000 |
| H-ADP | `hooks-load-counters.service.adp.first.if0` | hooks-load-counters | 0 | 4.539 | 453,858 | 0 | 20 | yes | 1,546,142 | yes | 1995.461 of 2000 |
| H-ADP | `hooks-load-counters.service.adp.last.if0` | hooks-load-counters | 0 | 21.265 | 2,126,471 | 0 | 20 | NO | -126,471 | yes | 1978.735 of 2000 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 4.471 | 447,125 | 0 | 20 | yes | 1,552,875 | yes | 235.529 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if0` | backlog-owed | 0 | 85.818 | 8,581,826 | 0 | 20 | NO | -6,581,826 | yes | 154.182 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 5.409 | 540,916 | 0 | 20 | yes | 1,459,084 | yes | 234.591 of 240 |
| H-AECP | `backlog.service.aecp.last.if0` | backlog | 0 | 48.472 | 4,847,223 | 0 | 20 | NO | -2,847,223 | yes | 191.528 of 240 |
| H-AECP | `hooks-load-counters.service.aecp.first.if0` | hooks-load-counters | 0 | 4.532 | 453,184 | 0 | 20 | yes | 1,546,816 | yes | 235.468 of 240 |
| H-AECP | `hooks-load-counters.service.aecp.last.if0` | hooks-load-counters | 0 | 63.699 | 6,369,922 | 0 | 20 | NO | -4,369,922 | yes | 176.301 of 240 |
| H-COUNTERS | `counters.loaded.if0` | hooks-load-counters | 0 | 20.761 | 2,076,085 | 0 | 20 | NO | -76,085 | yes | 979.239 of 1000 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 4.461 | 446,085 | 0 | 20 | yes | 1,553,915 | yes | 495.539 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 18.154 | 1,815,364 | 0 | 20 | yes | 184,636 | yes | 481.846 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 5.399 | 539,876 | 0 | 20 | yes | 1,460,124 | yes | 494.601 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 18.313 | 1,831,338 | 0 | 20 | yes | 168,662 | yes | 481.687 of 500 |
| H-MAAP | `hooks-load-counters.service.maap.first.if0` | hooks-load-counters | 0 | 4.521 | 452,144 | 0 | 20 | yes | 1,547,856 | yes | 495.479 of 500 |
| H-MAAP | `hooks-load-counters.service.maap.last.if0` | hooks-load-counters | 0 | 21.250 | 2,124,976 | 0 | 20 | NO | -124,976 | yes | 478.750 of 500 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 9.793 | 979,308 | 0 | 18 | yes | 820,692 | yes | 170.207 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if0` | backlog-owed | 0 | 42.197 | 4,219,697 | 0 | 18 | NO | -2,419,697 | yes | 137.803 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 14.746 | 1,474,624 | 0 | 18 | yes | 325,376 | yes | 165.254 of 180 |
| H-SRP | `backlog.service.srp.last.if0` | backlog | 0 | 50.676 | 5,067,595 | 0 | 18 | NO | -3,267,595 | yes | 129.324 of 180 |
| H-SRP | `hooks-load-counters.service.srp.first.if0` | hooks-load-counters | 0 | 15.169 | 1,516,868 | 0 | 18 | yes | 283,132 | yes | 164.831 of 180 |
| H-SRP | `hooks-load-counters.service.srp.last.if0` | hooks-load-counters | 0 | 68.053 | 6,805,263 | 0 | 18 | NO | -5,005,263 | yes | 111.947 of 180 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- none

Findings:

- LATE H-COUNTERS: counters.loaded.if0: 20.761 ms against its bound 20 ms (hooks-load-counters)
- LATE H-ADP: hooks-load-counters.service.adp.last.if0: 21.265 ms against its bound 20 ms (hooks-load-counters)
- LATE H-ACMP: hooks-load-counters.service.acmp.last.if0: 29.646 ms against its bound 20 ms (hooks-load-counters)
- LATE H-AECP: hooks-load-counters.service.aecp.last.if0: 63.699 ms against its bound 20 ms (hooks-load-counters)
- LATE H-MAAP: hooks-load-counters.service.maap.last.if0: 21.250 ms against its bound 20 ms (hooks-load-counters)
- LATE H-SRP: hooks-load-counters.service.srp.last.if0: 68.053 ms against its bound 18 ms (hooks-load-counters)
- LATE H-ACMP: backlog.acmp_command.if0: 22.573 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 25.013 ms against its bound 20 ms (backlog)
- LATE H-AECP: backlog.service.aecp.last.if0: 48.472 ms against its bound 20 ms (backlog)
- LATE H-SRP: backlog.service.srp.last.if0: 50.676 ms against its bound 18 ms (backlog)
- LATE H-ACMP: backlog.owed.if0: 77.837 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind0.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind1.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind2.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind3.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog-owed.service.acmp.last.if0: 24.542 ms against its bound 20 ms (backlog-owed)
- LATE H-AECP: backlog-owed.service.aecp.last.if0: 85.818 ms against its bound 20 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.last.if0: 42.197 ms against its bound 18 ms (backlog-owed)
