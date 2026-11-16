### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 3.147 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 2.940 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.830 | fits | 14 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.496 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-burst.held.srp.if0` (save-burst) | 9.294 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-flight.mrpdu.periodic.if0` (save-flight) | 3.147 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-burst | 3318 | 0 | 165,215 (1.652) | fits |
| save-flight | 2945 | 0 | 165,215 (1.652) | fits |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-burst | 107 | 1367.528 (0) | 5,000 | 6 | - | - | sequence 6, 0 missing | within |
| save-flight | 1 | 657.720 (0) | 5,000 | 2 | - | - | 59 steps (want 59), 27.287 ms | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-burst | 3721 | 103,782 (1.038) | 78,309 (0.783) |
| save-flight | 2063 | 99,469 (0.995) | 78,097 (0.781) |

Longest pass that carries a step: 103,782 CPU cycles (1.038 ms), save-burst; longest step: 78,309 (0.783 ms), save-burst.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 293,990 | 2.940 | 20 | 200 | fits | 129,584 | 142 | 0.503 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 314,652 | 3.147 | 20 | 20 | fits | 72,440 | 51 | 0.479 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 128,640 | 1.286 | 20 | 24 | fits | 36,748 | 23 | 0.785 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 202,737 | 2.027 | 20 | 50 | fits | 153,724 | 216 | 0.392 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 929,404 | 9.294 | 20 | 20 | fits | 50,790 | 23 | 0.808 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 116,762 | 1.168 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-burst.mrpdu.leaveall.if0` | 180,168 | 1.802 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 310,838 | 3.108 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 281,977 | 2.820 | 20 | 200 | fits | 117,702 | 133 | 0.442 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 261,840 | 2.618 | 20 | 20 | fits | 117,702 | 133 | 0.442 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 283,023 | 2.830 | 20 | 24 | fits | 51,527 | 35 | 0.520 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 249,571 | 2.496 | 20 | 50 | fits | 122,975 | 202 | 0.302 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 925,767 | 9.258 | 20 | 20 | fits | 46,946 | 16 | 0.720 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 62,813 | 0.628 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 61,562 | 0.616 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 314,668 | 3.147 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
