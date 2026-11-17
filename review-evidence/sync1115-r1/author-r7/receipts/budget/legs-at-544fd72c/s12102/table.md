### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.437 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.639 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.957 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.043 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.381 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.join.if0` (save-starved) | 1.644 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3306 | 0 | 163,479 (1.635) | fits |
| save-starved | 58212 | 0 | 163,479 (1.635) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.495 | 12,470 | 382 | - | 14.857 | no | within |
| save-starved | 12448.283 | 12,470 | 382 | - | 33.628 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,843 (1.008) | 77,812 (0.778) |
| save-starved | 698 | 81,594 (0.816) | 77,844 (0.778) |

Longest pass that carries a step: 100,843 CPU cycles (1.008 ms), save-held; longest step: 77,844 (0.778 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 260,336 | 2.603 | 20 | 200 | fits | 97,797 | 121 | 0.460 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 240,199 | 2.402 | 20 | 20 | fits | 97,797 | 121 | 0.460 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 294,269 | 2.943 | 20 | 24 | fits | 79,873 | 49 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 200,724 | 2.007 | 20 | 50 | fits | 97,797 | 121 | 0.460 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 817,869 | 8.179 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 136,218 | 1.362 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 136,218 | 1.362 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 145,120 | 1.451 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,876 | 2.639 | 20 | 200 | fits | 101,337 | 127 | 0.486 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 243,739 | 2.437 | 20 | 20 | fits | 101,337 | 127 | 0.486 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 295,739 | 2.957 | 20 | 24 | fits | 80,089 | 60 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 204,264 | 2.043 | 20 | 50 | fits | 101,337 | 127 | 0.486 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 838,067 | 8.381 | 20 | 20 | fits | 83,624 | 44 | 0.633 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 164,360 | 1.644 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 164,360 | 1.644 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 156,627 | 1.566 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
