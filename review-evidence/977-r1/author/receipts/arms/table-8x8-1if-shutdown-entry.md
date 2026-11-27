### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 1 paths and 0 of 2 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `adp.shutdown.if0` (adp-shutdown) | 0.041 (0.208) | fits | 0 events | 2 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| adp-shutdown | 262 | 0 | 31,026 (0.310) | fits |
| control-shutdown | 262 | 0 | 31,026 (0.310) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| adp-shutdown | 248 | 23,230 (0.232) | 2,666 (0.027) |
| control-shutdown | 248 | 23,230 (0.232) | 2,666 (0.027) |

Longest pass that carries a step: 23,230 CPU cycles (0.232 ms), adp-shutdown; longest step: 2,666 (0.027 ms), adp-shutdown.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `adp.shutdown.if0` | 4,141 | 0.041 | 20 | 200 | fits | 20,776 | 17 (29) | 0.577 |
| SHUTDOWN | `control.shutdown.if0` | 4,141 | 0.041 | 20 | 200 | fits | 20,776 | 17 (29) | 0.577 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
