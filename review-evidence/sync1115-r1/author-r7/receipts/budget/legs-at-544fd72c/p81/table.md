### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.062 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.635 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.952 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.039 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.374 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.818 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3309 | 0 | 163,276 (1.633) | fits |
| save-starved | 58207 | 0 | 163,276 (1.633) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.227 | 12,470 | 382 | - | 15.047 | no | within |
| save-starved | 12448.173 | 12,470 | 382 | - | 33.739 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,931 (1.009) | 77,812 (0.778) |
| save-starved | 698 | 81,594 (0.816) | 77,844 (0.778) |

Longest pass that carries a step: 100,931 CPU cycles (1.009 ms), save-held; longest step: 77,844 (0.778 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 260,091 | 2.601 | 20 | 200 | fits | 97,755 | 121 | 0.457 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 239,954 | 2.400 | 20 | 20 | fits | 97,755 | 121 | 0.457 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 293,847 | 2.938 | 20 | 24 | fits | 79,761 | 49 | 0.542 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 200,479 | 2.005 | 20 | 50 | fits | 97,755 | 121 | 0.457 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 817,447 | 8.174 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 55,717 | 0.557 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 55,717 | 0.557 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 179,045 | 1.790 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,536 | 2.635 | 20 | 200 | fits | 101,200 | 127 | 0.483 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 306,154 | 3.062 | 20 | 20 | fits | 83,719 | 56 | 0.610 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 295,152 | 2.952 | 20 | 24 | fits | 79,969 | 60 | 0.453 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 203,924 | 2.039 | 20 | 50 | fits | 101,200 | 127 | 0.483 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 837,427 | 8.374 | 20 | 20 | fits | 83,571 | 44 | 0.632 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 50,646 | 0.506 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 57,549 | 0.575 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 181,841 | 1.818 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
