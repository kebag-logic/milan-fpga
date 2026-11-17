### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.673 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.632 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.017 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.036 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.666 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.969 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3169 | 0 | 163,118 (1.631) | fits |
| save-starved | 58198 | 0 | 163,118 (1.631) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4817.179 | 12,470 | 382 | - | 15.210 | no | within |
| save-starved | 12447.155 | 12,470 | 382 | - | 32.613 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,979 (1.010) | 77,900 (0.779) |
| save-starved | 698 | 81,733 (0.817) | 77,967 (0.780) |

Longest pass that carries a step: 100,979 CPU cycles (1.010 ms), save-held; longest step: 77,967 (0.780 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 259,795 | 2.598 | 20 | 200 | fits | 97,617 | 121 | 0.456 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 267,337 | 2.673 | 20 | 20 | fits | 56,925 | 42 | 0.504 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 301,742 | 3.017 | 20 | 24 | fits | 87,290 | 55 | 0.577 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 200,183 | 2.002 | 20 | 50 | fits | 97,617 | 121 | 0.456 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 819,519 | 8.195 | 20 | 20 | fits | 59,073 | 24 | 0.670 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 123,903 | 1.239 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 123,093 | 1.231 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 280,509 | 2.805 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,240 | 2.632 | 20 | 200 | fits | 101,062 | 127 | 0.482 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 243,103 | 2.431 | 20 | 20 | fits | 101,062 | 127 | 0.482 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 291,428 | 2.914 | 20 | 24 | fits | 84,388 | 66 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 203,628 | 2.036 | 20 | 50 | fits | 101,062 | 127 | 0.482 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 866,607 | 8.666 | 20 | 20 | fits | 36,104 | 18 | 0.833 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 178,595 | 1.786 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 133,392 | 1.334 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 296,879 | 2.969 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
