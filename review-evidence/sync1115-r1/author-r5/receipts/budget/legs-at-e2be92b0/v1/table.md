### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 3 paths and 0 of 5 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.669 (0.742) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 187.724 (187.820) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.438 (189.548) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2013 | 0 | 46,932 (0.469) | fits |
| srp-talker-loss | 653 | 0 | 45,612 (0.456) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1944 | 24,514 (0.245) | 2,407 (0.024) |
| srp-talker-loss | 613 | 23,466 (0.235) | 2,407 (0.024) |

Longest pass that carries a step: 24,514 CPU cycles (0.245 ms), srp-talker; longest step: 2,407 (0.024 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 66,922 | 0.669 | 220 | 220 | fits | 45,612 | 5 | 0.910 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,772,383 | 187.724 | 220 | 220 | fits | 38,085 | 3 | 0.853 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 66,922 | 0.669 | 220 | 220 | fits | 45,612 | 5 | 0.910 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,772,383 | 187.724 | 220 | 220 | fits | 38,085 | 3 | 0.853 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,943,820 | 189.438 | 220 | 220 | fits | 39,023 | 3 | 0.853 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
