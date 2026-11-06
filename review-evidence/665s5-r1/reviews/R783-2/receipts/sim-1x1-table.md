### 1x1, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm answering

Graded against the bounds in the tree at this base. The amended column gives the owner's decisions of 2026-11-06 on #665, for information: it grades nothing, and this harness re-grades when #810 merges.

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Amended service bound, ms, for information | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|---:|
| H-ADP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-DISC | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-ACMP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-AECP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-NOTIFY | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-COUNTERS | 8 | 3 | 0 | 27.581 (20) **over its bound**, `counters.all.if0`, margin 972.4 of 1000 | - | 20 | 16 (0) | 0 |
| H-MAAP | 0 | 0 | 0 | - | - | - | 2 (0) | 0 |
| H-SRP | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound at this base, ms | Amended bound, ms, for information | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-COUNTERS | `counters.all.if0` | hooks-counters | 0 | 27.581 | 2,758,074 | 0 | 20 | 20 | NO | -758,074 | no | 972.419 of 1000 |
| H-COUNTERS | `counters.all.t36.i0.if0` | hooks-counters | 0 | 27.581 | 2,758,074 | 0 | 20 | 20 | NO | -758,074 | no | 972.419 of 1000 |
| H-COUNTERS | `counters.all.t5.i1.if0` | hooks-counters | 0 | 11.075 | 1,107,501 | 0 | 20 | 20 | yes | 892,499 | no | 988.925 of 1000 |
| H-COUNTERS | `counters.all.t6.i0.if0` | hooks-counters | 0 | 5.486 | 548,617 | 0 | 20 | 20 | yes | 1,451,383 | no | 994.514 of 1000 |
| H-COUNTERS | `counters.all.t6.i1.if0` | hooks-counters | 0 | 16.465 | 1,646,480 | 0 | 20 | 20 | yes | 353,520 | no | 983.535 of 1000 |
| H-COUNTERS | `counters.all.t9.i0.if0` | hooks-counters | 0 | 22.065 | 2,206,548 | 0 | 20 | 20 | NO | -206,548 | no | 977.935 of 1000 |
| H-COUNTERS | `counters.first.if0` | hooks-counters | 0 | 5.638 | 563,826 | 0 | 20 | 20 | yes | 1,436,174 | no | 994.362 of 1000 |
| H-COUNTERS | `counters.held.if0` | hooks-counters | 0 | 5.185 | 518,508 | 896.258 | 20 | 20 | yes | 1,481,492 | no | 98.557 of 1000 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- none

Findings:

- LATE H-COUNTERS: counters.all.if0: 27.581 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t9.i0.if0: 22.065 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t36.i0.if0: 27.581 ms against its bound 20 ms (hooks-counters)
