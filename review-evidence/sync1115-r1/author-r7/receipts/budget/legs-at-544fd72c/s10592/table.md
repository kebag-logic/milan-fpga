### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.046 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.636 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 3.014 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.040 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.387 | fits | 31 srp | 2 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.610 | fits | 0 srp | 6 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-held | 3163 | 0 | 163,382 (1.634) | fits |
| save-starved | 58163 | 0 | 163,382 (1.634) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-held | 4817.559 | 12,470 | 382 | - | 15.416 | no | within |
| save-starved | 12447.286 | 12,470 | 382 | - | 33.319 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-held | 1562 | 100,896 (1.009) | 77,909 (0.779) |
| save-starved | 698 | 81,653 (0.817) | 77,957 (0.780) |

Longest pass that carries a step: 100,896 CPU cycles (1.009 ms), save-held; longest step: 77,957 (0.780 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 260,121 | 2.601 | 20 | 200 | fits | 97,679 | 121 | 0.457 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 273,945 | 2.739 | 20 | 20 | fits | 71,991 | 46 | 0.612 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 301,361 | 3.014 | 20 | 24 | fits | 87,093 | 55 | 0.577 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 200,509 | 2.005 | 20 | 50 | fits | 97,679 | 121 | 0.457 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 818,955 | 8.190 | 20 | 20 | fits | 58,890 | 24 | 0.668 |
| an MRPDU its join timer owes, the longest | `save-held.mrpdu.join.if0` | 186,217 | 1.862 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-held.mrpdu.leaveall.if0` | 53,814 | 0.538 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 251,484 | 2.515 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,566 | 2.636 | 20 | 200 | fits | 101,124 | 127 | 0.483 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 304,616 | 3.046 | 20 | 20 | fits | 83,827 | 56 | 0.611 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 299,746 | 2.997 | 20 | 24 | fits | 84,412 | 66 | 0.459 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 203,954 | 2.040 | 20 | 50 | fits | 101,124 | 127 | 0.483 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 838,671 | 8.387 | 20 | 20 | fits | 80,221 | 38 | 0.634 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 152,226 | 1.522 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 59,686 | 0.597 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 261,022 | 2.610 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
