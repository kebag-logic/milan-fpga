### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 8 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-flight.held.acmp.if0` (save-flight) | 2.741 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-flight.held.adp.if0` (save-flight) | 3.261 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 3.013 | fits | 14 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.663 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-flight.held.srp.if0` (save-flight) | 8.850 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-flight.mrpdu.periodic.if0` (save-flight) | 2.924 | fits | 0 srp | 3 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 3062 | 0 | 154,897 (1.549) | fits |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 7049.750 (0) | 5,000 | 2 | - | 0 | 59 steps (want 59), 589.527 ms | OVER |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1424 | 100,727 (1.007) | 78,578 (0.786) |

Longest pass that carries a step: 100,727 CPU cycles (1.007 ms), save-flight; longest step: 78,578 (0.786 ms), save-flight.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 326,079 | 3.261 | 20 | 200 | fits | 125,082 | 230 | 0.332 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 274,073 | 2.741 | 20 | 20 | fits | 67,658 | 55 | 0.479 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 301,283 | 3.013 | 20 | 24 | fits | 95,378 | 53 | 0.590 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 266,336 | 2.663 | 20 | 50 | fits | 125,082 | 230 | 0.332 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 884,960 | 8.850 | 20 | 20 | fits | 34,896 | 12 | 0.804 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 54,399 | 0.544 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 61,068 | 0.611 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 292,438 | 2.924 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
