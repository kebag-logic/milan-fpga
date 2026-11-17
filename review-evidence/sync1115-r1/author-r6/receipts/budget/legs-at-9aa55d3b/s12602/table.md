### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.680 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.649 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.969 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.053 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.391 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.667 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3303 | 0 | 164,733 (1.647) | fits |
| save-starved | 58209 | 0 | 164,733 (1.647) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.442 | 12,470 | 382 | - | 15.042 | no | within |
| save-starved | 12448.307 | 12,470 | 382 | - | 33.544 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,851 (1.009) | 77,812 (0.778) |
| save-starved | 698 | 81,594 (0.816) | 77,844 (0.778) |

Longest pass that carries a step: 100,851 CPU cycles (1.009 ms), save-held; longest step: 77,844 (0.778 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 261,502 | 2.615 | 20 | 200 | fits | 97,709 | 121 | 0.457 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 268,050 | 2.680 | 20 | 20 | fits | 56,939 | 42 | 0.504 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 295,490 | 2.955 | 20 | 24 | fits | 79,870 | 49 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 185,355 | 1.854 | 20 | 50 | fits | 56,343 | 55 | 0.511 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 819,090 | 8.191 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 59,673 | 0.597 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 64,304 | 0.643 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 155,649 | 1.556 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 264,883 | 2.649 | 20 | 200 | fits | 101,090 | 127 | 0.481 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 244,746 | 2.447 | 20 | 20 | fits | 101,090 | 127 | 0.481 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 296,867 | 2.969 | 20 | 24 | fits | 80,089 | 60 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 205,271 | 2.053 | 20 | 50 | fits | 101,090 | 127 | 0.481 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 839,142 | 8.391 | 20 | 20 | fits | 83,571 | 44 | 0.632 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 63,039 | 0.630 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 51,433 | 0.514 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 166,690 | 1.667 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
