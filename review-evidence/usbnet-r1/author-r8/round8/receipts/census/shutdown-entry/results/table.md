### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 1 paths and 0 of 2 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `adp.shutdown.if0` (adp-shutdown) | 0.049 (0.172) | fits | 0 events | 2 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| adp-shutdown | 263 | 0 | 55,051 (0.688) | fits |
| control-shutdown | 263 | 0 | 55,051 (0.688) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| adp-shutdown | 252 | 16,576 (0.207) | 2,306 (0.029) |
| control-shutdown | 252 | 16,576 (0.207) | 2,306 (0.029) |

Longest pass that carries a step: 16,576 CPU cycles (0.207 ms), adp-shutdown; longest step: 2,306 (0.029 ms), adp-shutdown.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `adp.shutdown.if0` | 3,891 | 0.049 | 20 | 200 | fits | 13,785 | 17 (29) | 0.560 |
| SHUTDOWN | `control.shutdown.if0` | 3,891 | 0.049 | 20 | 200 | fits | 13,785 | 17 (29) | 0.560 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
