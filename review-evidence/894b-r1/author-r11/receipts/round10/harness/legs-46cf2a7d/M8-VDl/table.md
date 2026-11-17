### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 10 paths and 0 of 10 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker-loss) | 0.677 (0.715) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker-loss) | 186.993 (187.045) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker-loss) | 189.528 (189.589) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker-loss) | 189.523 (189.613) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker-loss) | 179.386 (179.462) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker-loss) | 9.415 (9.534) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker-loss) | 189.176 (189.297) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker-loss) | 189.350 (189.471) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker-loss) | 189.255 (189.380) | fits | 0 acmp | 1 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.638 (189.813) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker-loss | 816 | 0 | 83,440 (0.834) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker-loss | 727 | 29,413 (0.294) | 2,223 (0.022) |

Longest pass that carries a step: 29,413 CPU cycles (0.294 ms), srp-talker-loss; longest step: 2,223 (0.022 ms), srp-talker-loss.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,669 | 0.677 | 220 | 220 | fits | 37,382 | 5 | 0.910 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,699,284 | 186.993 | 220 | 220 | fits | 30,270 | 3 | 0.857 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,952,809 | 189.528 | 220 | 220 | fits | 33,887 | 3 | 0.848 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,952,294 | 189.523 | 220 | 220 | fits | 38,867 | 3 | 0.848 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,938,554 | 179.386 | 220 | 220 | fits | 29,293 | 8 | 0.847 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 941,515 | 9.415 | 220 | 220 | fits | 60,793 | 3 | 0.796 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,917,646 | 189.176 | 220 | 220 | fits | 47,227 | 3 | 0.837 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,935,024 | 189.350 | 220 | 220 | fits | 46,934 | 3 | 0.840 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,925,488 | 189.255 | 220 | 220 | fits | 43,829 | 3 | 0.848 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,963,809 | 189.638 | 220 | 220 | fits | 83,440 | 3 | 0.767 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
