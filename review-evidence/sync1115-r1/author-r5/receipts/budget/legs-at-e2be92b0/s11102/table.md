### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.123 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.646 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.966 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.849 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.389 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.797 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3308 | 0 | 164,586 (1.646) | fits |
| save-starved | 58211 | 0 | 164,586 (1.646) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.211 | 12,470 | 382 | - | 15.052 | no | within |
| save-starved | 12448.122 | 12,470 | 382 | - | 32.241 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,923 (1.009) | 77,812 (0.778) |
| save-starved | 698 | 81,673 (0.817) | 77,862 (0.779) |

Longest pass that carries a step: 100,923 CPU cycles (1.009 ms), save-held; longest step: 77,862 (0.779 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 261,254 | 2.613 | 20 | 200 | fits | 97,608 | 121 | 0.455 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 241,117 | 2.411 | 20 | 20 | fits | 97,608 | 121 | 0.455 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 295,305 | 2.953 | 20 | 24 | fits | 79,870 | 49 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 184,889 | 1.849 | 20 | 50 | fits | 56,260 | 55 | 0.509 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 818,905 | 8.189 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 64,485 | 0.645 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 53,935 | 0.539 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 178,428 | 1.784 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 264,635 | 2.646 | 20 | 200 | fits | 100,989 | 127 | 0.481 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 312,286 | 3.123 | 20 | 20 | fits | 83,815 | 56 | 0.611 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 296,619 | 2.966 | 20 | 24 | fits | 80,089 | 60 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 183,349 | 1.833 | 20 | 50 | fits | 154,993 | 230 | 0.384 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 838,894 | 8.389 | 20 | 20 | fits | 83,571 | 44 | 0.632 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 61,128 | 0.611 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 49,453 | 0.495 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 179,733 | 1.797 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
