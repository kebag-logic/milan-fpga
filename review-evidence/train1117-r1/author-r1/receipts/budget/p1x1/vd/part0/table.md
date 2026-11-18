### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 2 paths and 0 of 2 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.655 (0.710) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 187.373 (187.461) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2014 | 0 | 44,454 (0.445) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1944 | 24,103 (0.241) | 2,338 (0.023) |

Longest pass that carries a step: 24,103 CPU cycles (0.241 ms), srp-talker; longest step: 2,338 (0.023 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 65,475 | 0.655 | 220 | 220 | fits | 42,126 | 5 | 0.903 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,737,292 | 187.373 | 220 | 220 | fits | 36,456 | 3 | 0.861 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
