### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 15 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 2.318 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-flight.held.adp.if0` (save-flight) | 2.819 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-flight.held.aecp.if0` (save-flight) | 2.945 | fits | 14 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.228 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-flight.held.srp.if0` (save-flight) | 7.939 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-burst.mrpdu.periodic.if0` (save-burst) | 2.478 | fits | 0 srp | 5 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 2998 | 0 | 155,175 (1.552) | fits |
| save-burst | 2742 | 0 | 155,175 (1.552) | fits |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 2020.413 (0) | 5,000 | 2 | - | - | 36 steps (want 19), 359.289 ms | OVER |
| save-burst | 39 | never (38) | 5,000 | 1 | 38, 37, 36, 35, 34 | - | sequence 1, 5 missing | OVER |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1384 | 95,097 (0.951) | 78,189 (0.782) |
| save-burst | 1350 | 93,681 (0.937) | 78,060 (0.781) |

Longest pass that carries a step: 95,097 CPU cycles (0.951 ms), save-flight; longest step: 78,189 (0.782 ms), save-flight.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 281,891 | 2.819 | 20 | 200 | fits | 68,334 | 81 | 0.329 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 219,413 | 2.194 | 20 | 20 | fits | 22,922 | 15 | 0.741 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 294,467 | 2.945 | 20 | 24 | fits | 75,909 | 43 | 0.538 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 222,779 | 2.228 | 20 | 50 | fits | 93,380 | 202 | 0.282 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 793,864 | 7.939 | 20 | 20 | fits | 59,428 | 26 | 0.700 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 49,816 | 0.498 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 47,021 | 0.470 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 215,404 | 2.154 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 154,366 | 1.544 | 20 | 200 | fits | 155,175 | 249 | 0.465 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 231,812 | 2.318 | 20 | 20 | fits | 97,714 | 91 | 0.677 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 169,678 | 1.697 | 20 | 24 | fits | 91,425 | 34 | 0.733 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 192,337 | 1.923 | 20 | 50 | fits | 97,714 | 91 | 0.677 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 761,492 | 7.615 | 20 | 20 | fits | 60,792 | 28 | 0.819 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 46,262 | 0.463 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 247,768 | 2.478 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
