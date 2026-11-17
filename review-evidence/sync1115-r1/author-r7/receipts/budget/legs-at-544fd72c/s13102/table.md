### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.157 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.632 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.951 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.924 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.373 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.962 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3305 | 0 | 162,127 (1.621) | fits |
| save-starved | 58211 | 0 | 162,127 (1.621) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.120 | 12,470 | 382 | - | 15.236 | no | within |
| save-starved | 12447.943 | 12,470 | 382 | - | 32.435 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,944 (1.009) | 77,812 (0.778) |
| save-starved | 698 | 81,607 (0.816) | 77,943 (0.779) |

Longest pass that carries a step: 100,944 CPU cycles (1.009 ms), save-held; longest step: 77,943 (0.779 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 259,733 | 2.597 | 20 | 200 | fits | 98,546 | 124 | 0.443 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 270,026 | 2.700 | 20 | 20 | fits | 56,939 | 42 | 0.504 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 293,732 | 2.937 | 20 | 24 | fits | 79,881 | 49 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 179,243 | 1.792 | 20 | 50 | fits | 56,319 | 55 | 0.511 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 817,332 | 8.173 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 158,146 | 1.581 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 63,978 | 0.640 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 178,170 | 1.782 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,151 | 2.632 | 20 | 200 | fits | 101,964 | 130 | 0.469 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 315,735 | 3.157 | 20 | 20 | fits | 83,812 | 56 | 0.611 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 295,072 | 2.951 | 20 | 24 | fits | 80,089 | 60 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 192,448 | 1.924 | 20 | 50 | fits | 154,995 | 230 | 0.385 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 837,347 | 8.373 | 20 | 20 | fits | 83,571 | 44 | 0.632 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 166,078 | 1.661 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 58,403 | 0.584 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 196,235 | 1.962 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
