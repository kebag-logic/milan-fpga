### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 3 paths and 0 of 5 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.682 (0.749) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 187.371 (187.467) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.527 (189.636) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2014 | 0 | 48,103 (0.481) | fits |
| srp-talker-loss | 654 | 0 | 46,033 (0.460) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1944 | 24,300 (0.243) | 2,593 (0.026) |
| srp-talker-loss | 613 | 23,224 (0.232) | 2,593 (0.026) |

Longest pass that carries a step: 24,300 CPU cycles (0.243 ms), srp-talker; longest step: 2,593 (0.026 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 68,250 | 0.682 | 220 | 220 | fits | 46,033 | 5 | 0.897 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,737,111 | 187.371 | 220 | 220 | fits | 39,160 | 3 | 0.852 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 68,250 | 0.682 | 220 | 220 | fits | 46,033 | 5 | 0.897 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,737,111 | 187.371 | 220 | 220 | fits | 39,160 | 3 | 0.852 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,952,698 | 189.527 | 220 | 220 | fits | 40,114 | 3 | 0.857 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
