### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 20 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.736 (0.772) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s1.if1` (srp-talker) | 0.704 (0.735) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 185.101 (185.164) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s3.if1` (srp-talker) | 189.406 (189.453) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 188.967 (189.042) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s5.if1` (srp-talker) | 179.392 (179.444) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 8.563 (8.650) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s7.if1` (srp-talker) | 189.308 (189.364) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 188.806 (188.895) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 188.967 (189.087) | fits | 0 maap | 1 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 1 | `srp.talker_loss.if1` (srp-talker-loss) | 188.976 (189.065) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2206 | 0 | 58,258 (0.583) | fits |
| srp-talker-loss | 847 | 0 | 54,880 (0.549) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2039 | 38,934 (0.389) | 2,827 (0.028) |
| srp-talker-loss | 727 | 36,346 (0.363) | 2,779 (0.028) |

Longest pass that carries a step: 38,934 CPU cycles (0.389 ms), srp-talker; longest step: 2,827 (0.028 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 73,642 | 0.736 | 220 | 220 | fits | 39,417 | 5 | 0.927 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if1` | 70,375 | 0.704 | 220 | 220 | fits | 36,371 | 5 | 0.922 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,510,115 | 185.101 | 220 | 220 | fits | 33,265 | 3 | 0.883 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if1` | 18,940,626 | 189.406 | 220 | 220 | fits | 29,900 | 8 | 0.571 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 18,896,729 | 188.967 | 220 | 220 | fits | 35,190 | 3 | 0.882 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if1` | 17,939,220 | 179.392 | 220 | 220 | fits | 24,541 | 8 | 0.659 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 856,306 | 8.563 | 220 | 220 | fits | 44,243 | 3 | 0.845 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if1` | 18,930,806 | 189.308 | 220 | 220 | fits | 31,113 | 8 | 0.571 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,880,603 | 188.806 | 220 | 220 | fits | 37,055 | 4 | 0.876 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 73,642 | 0.736 | 220 | 220 | fits | 39,417 | 5 | 0.927 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if1` | 70,375 | 0.704 | 220 | 220 | fits | 36,371 | 5 | 0.922 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,510,115 | 185.101 | 220 | 220 | fits | 33,265 | 3 | 0.883 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if1` | 18,940,626 | 189.406 | 220 | 220 | fits | 29,900 | 8 | 0.571 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 18,896,729 | 188.967 | 220 | 220 | fits | 35,190 | 3 | 0.882 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if1` | 17,939,220 | 179.392 | 220 | 220 | fits | 24,541 | 8 | 0.659 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 856,306 | 8.563 | 220 | 220 | fits | 44,243 | 3 | 0.845 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if1` | 18,930,806 | 189.308 | 220 | 220 | fits | 31,113 | 8 | 0.571 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,880,603 | 188.806 | 220 | 220 | fits | 37,055 | 4 | 0.876 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,896,748 | 188.967 | 220 | 220 | fits | 50,549 | 3 | 0.851 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if1` | 18,897,606 | 188.976 | 220 | 220 | fits | 42,799 | 8 | 0.792 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
