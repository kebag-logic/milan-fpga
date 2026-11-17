### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 10 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.669 (0.700) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 186.947 (186.995) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 189.486 (189.541) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker) | 189.472 (189.558) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 179.508 (179.589) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker) | 9.243 (9.359) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 189.252 (189.366) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker) | 189.253 (189.368) | fits | 0 acmp | 2 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 189.378 (189.497) | fits | 0 acmp | 2 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.703 (189.870) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 2169 | 0 | 91,360 (0.914) | fits |
| srp-talker-loss | 817 | 0 | 82,550 (0.826) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2058 | 31,600 (0.316) | 2,247 (0.022) |
| srp-talker-loss | 727 | 30,152 (0.302) | 2,247 (0.022) |

Longest pass that carries a step: 31,600 CPU cycles (0.316 ms), srp-talker; longest step: 2,247 (0.022 ms), srp-talker.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 66,860 | 0.669 | 220 | 220 | fits | 35,779 | 5 | 0.902 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,694,739 | 186.947 | 220 | 220 | fits | 29,497 | 3 | 0.850 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,948,565 | 189.486 | 220 | 220 | fits | 33,001 | 3 | 0.840 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,947,180 | 189.472 | 220 | 220 | fits | 38,159 | 3 | 0.842 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,950,811 | 179.508 | 220 | 220 | fits | 29,656 | 8 | 0.851 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 924,335 | 9.243 | 220 | 220 | fits | 60,554 | 3 | 0.802 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,925,166 | 189.252 | 220 | 220 | fits | 46,461 | 3 | 0.832 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,925,264 | 189.253 | 220 | 220 | fits | 46,013 | 3 | 0.832 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,937,764 | 189.378 | 220 | 220 | fits | 43,075 | 3 | 0.843 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 66,860 | 0.669 | 220 | 220 | fits | 35,779 | 5 | 0.902 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,694,739 | 186.947 | 220 | 220 | fits | 29,497 | 3 | 0.850 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,948,565 | 189.486 | 220 | 220 | fits | 33,001 | 3 | 0.840 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,947,180 | 189.472 | 220 | 220 | fits | 38,159 | 3 | 0.842 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,950,811 | 179.508 | 220 | 220 | fits | 29,656 | 8 | 0.851 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 924,335 | 9.243 | 220 | 220 | fits | 60,554 | 3 | 0.802 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,925,166 | 189.252 | 220 | 220 | fits | 46,461 | 3 | 0.832 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,925,264 | 189.253 | 220 | 220 | fits | 46,013 | 3 | 0.832 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,937,764 | 189.378 | 220 | 220 | fits | 43,075 | 3 | 0.843 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,970,285 | 189.703 | 220 | 220 | fits | 82,550 | 3 | 0.752 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
