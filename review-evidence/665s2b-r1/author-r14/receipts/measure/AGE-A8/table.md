### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 5 paths and 0 of 5 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 8.269 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 1 | `save-starved.held.adp.if1` (save-starved) | 4.860 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 1 | `save-starved.held.aecp.if1` (save-starved) | 11.486 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 5.414 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 1 | `save-starved.held.srp.if1` (save-starved) | 14.603 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-starved | 53678 | 0 | 171,111 (1.711) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---|---|
| save-starved | not by 12618.411 | 12,110 | 370 | - | yes | OVER |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-starved | 267 | 102,374 (1.024) | 26,895 (0.269) |

Longest pass that carries a step: 102,374 CPU cycles (1.024 ms), save-starved; longest step: 26,895 (0.269 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if1` | 485,990 | 4.860 | 20 | 200 | fits | 127,001 | 91 | 0.592 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 826,870 | 8.269 | 20 | 20 | fits | 120,819 | 52 | 0.684 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if1` | 1,148,572 | 11.486 | 20 | 24 | fits | 34,628 | 29 | 0.595 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 541,435 | 5.414 | 20 | 50 | fits | 115,057 | 62 | 0.663 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if1` | 1,460,328 | 14.603 | 18 | 18 | fits | 69,473 | 37 | 0.709 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
