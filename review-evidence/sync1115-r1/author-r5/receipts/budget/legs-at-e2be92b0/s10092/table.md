### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.030 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.647 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.965 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.051 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.388 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.753 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3302 | 0 | 164,458 (1.645) | fits |
| save-starved | 58170 | 0 | 164,458 (1.645) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.486 | 12,470 | 382 | - | 14.848 | no | within |
| save-starved | 12448.289 | 12,470 | 382 | - | 33.559 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,824 (1.008) | 77,909 (0.779) |
| save-starved | 698 | 81,721 (0.817) | 77,903 (0.779) |

Longest pass that carries a step: 100,824 CPU cycles (1.008 ms), save-held; longest step: 77,909 (0.779 ms), save-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 261,287 | 2.613 | 20 | 200 | fits | 97,769 | 121 | 0.459 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 273,984 | 2.740 | 20 | 20 | fits | 80,271 | 50 | 0.588 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 295,146 | 2.951 | 20 | 24 | fits | 79,773 | 49 | 0.542 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 201,675 | 2.017 | 20 | 50 | fits | 97,769 | 121 | 0.459 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 818,687 | 8.187 | 20 | 20 | fits | 64,837 | 30 | 0.710 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 91,378 | 0.914 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 57,276 | 0.573 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 144,926 | 1.449 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 264,743 | 2.647 | 20 | 200 | fits | 101,225 | 127 | 0.484 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 303,037 | 3.030 | 20 | 20 | fits | 83,668 | 56 | 0.609 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 296,510 | 2.965 | 20 | 24 | fits | 79,995 | 60 | 0.453 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 205,131 | 2.051 | 20 | 50 | fits | 101,225 | 127 | 0.484 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 838,794 | 8.388 | 20 | 20 | fits | 83,580 | 44 | 0.632 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 82,521 | 0.825 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 59,129 | 0.591 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 175,255 | 1.753 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
