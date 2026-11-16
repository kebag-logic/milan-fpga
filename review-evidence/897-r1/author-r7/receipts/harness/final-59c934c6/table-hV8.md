### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 9 paths and 0 of 9 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.764 (0.804) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s1.if1` (srp-talker) | 0.744 (0.771) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 184.453 (184.522) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s3.if1` (srp-talker) | 189.397 (189.436) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 188.934 (189.018) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s5.if1` (srp-talker) | 179.338 (179.383) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 8.588 (8.681) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 1 | `srp.talker_declare.s7.if1` (srp-talker) | 189.116 (189.165) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 188.898 (188.995) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2203 | 0 | 65,536 (0.655) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2039 | 39,252 (0.393) | 2,554 (0.026) |

Longest pass that carries a step: 39,252 CPU cycles (0.393 ms), srp-talker; longest step: 2,554 (0.026 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 76,399 | 0.764 | 220 | 220 | fits | 39,858 | 5 | 0.904 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if1` | 74,350 | 0.744 | 220 | 220 | fits | 36,855 | 5 | 0.901 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,445,285 | 184.453 | 220 | 220 | fits | 33,470 | 3 | 0.882 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if1` | 18,939,704 | 189.397 | 220 | 220 | fits | 28,823 | 8 | 0.514 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 18,893,445 | 188.934 | 220 | 220 | fits | 35,461 | 3 | 0.881 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if1` | 17,933,781 | 179.338 | 220 | 220 | fits | 23,682 | 8 | 0.545 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 858,819 | 8.588 | 220 | 220 | fits | 43,856 | 3 | 0.837 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if1` | 18,911,613 | 189.116 | 220 | 220 | fits | 29,970 | 8 | 0.514 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,889,761 | 188.898 | 220 | 220 | fits | 37,381 | 4 | 0.873 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
