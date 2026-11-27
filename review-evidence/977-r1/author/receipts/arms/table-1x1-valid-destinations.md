### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 11 paths and 0 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 2.177 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 1.508 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 3.140 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 1.245 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 8.763 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 2.246 | fits | 0 srp | 2 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.371 (0.371) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.363 (0.363) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.441 (0.479) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 186.728 (186.788) | fits | 0 acmp | 3 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 189.532 (189.619) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 10103 | 0 | 33,696 (0.337) | fits |
| srp-talker-loss | 2097 | 0 | 25,725 (0.257) | fits |
| srp-talker-held | 3862 | 0 | 151,693 (1.517) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 1097.842 | 4,070 | 102 | - | 17.416 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1944 | 20,422 (0.204) | 2,645 (0.026) |
| srp-talker-loss | 613 | 20,445 (0.204) | 2,597 (0.026) |
| srp-talker-held | 900 | 98,853 (0.989) | 78,115 (0.781) |

Longest pass that carries a step: 98,853 CPU cycles (0.989 ms), srp-talker-held; longest step: 78,115 (0.781 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 44,096 | 0.441 | 220 | 220 | fits | 22,967 | 6 | 0.907 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,672,847 | 186.728 | 220 | 220 | fits | 17,681 | 4 | 0.876 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 44,096 | 0.441 | 220 | 220 | fits | 22,967 | 6 | 0.907 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,672,847 | 186.728 | 220 | 220 | fits | 17,681 | 4 | 0.876 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,953,238 | 189.532 | 220 | 220 | fits | 20,144 | 4 | 0.885 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 44,096 | 0.441 | 220 | 220 | fits | 22,967 | 6 | 0.907 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,672,847 | 186.728 | 220 | 220 | fits | 17,681 | 4 | 0.876 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 37,051 | 0.371 | 20 | 20 | fits | 37,117 | 24 | 0.844 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 36,252 | 0.363 | 20 | 20 | fits | 36,318 | 24 | 0.837 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 150,753 | 1.508 | 20 | 200 | fits | 151,693 | 260 | 0.443 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 217,704 | 2.177 | 20 | 20 | fits | 87,088 | 111 | 0.622 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 313,963 | 3.140 | 20 | 24 | fits | 89,862 | 80 | 0.565 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 124,494 | 1.245 | 20 | 50 | fits | 36,653 | 51 | 0.562 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 876,292 | 8.763 | 20 | 20 | fits | 61,324 | 55 | 0.729 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 38,052 | 0.381 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 224,601 | 2.246 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
