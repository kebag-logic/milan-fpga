# USB-network held-egress derivation

The rule and every existing point remain unchanged. These are recorded service-budget misses, held to the ruled separate point.

| Row | Arty measured (ms) | Injected measured (ms) | Original Arty figure (ms) | USB figure (ms) | USB margin (ms) |
|---|---:|---:|---:|---:|---:|
| `backlog.owed.if0` | 62.79239 | 62.71981 | 62.94 | 62.94 | 0.22019 |
| `backlog.owed_behind0.if0` | 62.92862 | 62.86221 | 63.08 | 63.08 | 0.21779 |
| `backlog.owed_behind1.if0` | 63.06490 | 63.00366 | 63.22 | 63.22 | 0.21634 |
| `backlog.owed_behind2.if0` | 63.19966 | 63.14499 | 63.36 | 63.36 | 0.21501 |
| `backlog.owed_behind3.if0` | 63.33355 | 63.28611 | 63.51 | 63.51 | 0.22389 |
| `backlog-owed.service.acmp.last.if0` | 62.10374 | 61.99278 | 62.21 | 62.21 | 0.21722 |
| `backlog-owed.service.aecp.last.if0` | 61.88720 | 62.03635 | 61.99 | 62.14 | 0.10365 |

Rule: `60 + 1.05 * (max(Arty, injected) - 60)` ms, rounded upward to 0.01 ms.

The last AECP row derives `60 + 1.05 * 2.03635 = 62.1381675` ms, rounded upward to 62.14 ms. Its retained 62.03635 ms measurement remains a negative control against the original 61.99 ms Arty figure. At 80 MHz, one cycle above the USB figure is 62.1400125 ms, represented as 62.14001 ms by the existing grade resolution. It must fail.
