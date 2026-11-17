### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.677 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.633 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.952 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.828 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.375 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 1.736 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3303 | 0 | 162,131 (1.621) | fits |
| save-starved | 58206 | 0 | 162,131 (1.621) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4818.288 | 12,470 | 382 | - | 15.052 | no | within |
| save-starved | 12448.255 | 12,470 | 382 | - | 33.548 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,964 (1.010) | 77,812 (0.778) |
| save-starved | 698 | 81,673 (0.817) | 77,844 (0.778) |

Longest pass that carries a step: 100,964 CPU cycles (1.010 ms), save-held; longest step: 77,844 (0.778 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 259,838 | 2.598 | 20 | 200 | fits | 98,647 | 124 | 0.444 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 267,705 | 2.677 | 20 | 20 | fits | 57,058 | 42 | 0.507 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 293,774 | 2.938 | 20 | 24 | fits | 79,881 | 49 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 182,751 | 1.828 | 20 | 50 | fits | 56,393 | 55 | 0.511 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 817,374 | 8.174 | 20 | 20 | fits | 64,896 | 30 | 0.711 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 61,350 | 0.614 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 47,942 | 0.479 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 161,757 | 1.618 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,256 | 2.633 | 20 | 200 | fits | 102,065 | 130 | 0.469 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 243,119 | 2.431 | 20 | 20 | fits | 102,065 | 130 | 0.469 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 295,177 | 2.952 | 20 | 24 | fits | 80,089 | 60 | 0.455 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 180,752 | 1.808 | 20 | 50 | fits | 66,368 | 82 | 0.501 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 837,505 | 8.375 | 20 | 20 | fits | 83,624 | 44 | 0.633 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 80,727 | 0.807 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 53,212 | 0.532 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 173,570 | 1.736 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
