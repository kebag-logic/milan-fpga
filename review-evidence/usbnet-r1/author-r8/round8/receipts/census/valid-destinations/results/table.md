### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 9 paths and 0 of 12 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 2.580 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 2.782 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 3.606 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 2.038 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 9.864 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 2.183 | fits | 0 srp | 2 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.448 (0.449) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.663 (0.763) | fits | 0 acmp | 3 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 186.785 (186.915) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 5967 | 0 | 56,566 (0.707) | fits |
| srp-talker-loss | 1295 | 0 | 54,312 (0.679) | fits |
| srp-talker-held | 2118 | 0 | 127,755 (1.597) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 1073.065 | 3,440 | 81 | - | 9.345 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 1925 | 18,490 (0.231) | 2,567 (0.032) |
| srp-talker-loss | 594 | 18,413 (0.230) | 2,567 (0.032) |
| srp-talker-held | 796 | 89,095 (1.114) | 78,272 (0.978) |

Longest pass that carries a step: 89,095 CPU cycles (1.114 ms), srp-talker-held; longest step: 78,272 (0.978 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 53,047 | 0.663 | 220 | 220 | fits | 39,603 | 5 | 0.898 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 53,047 | 0.663 | 220 | 220 | fits | 39,603 | 5 | 0.898 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 14,942,815 | 186.785 | 220 | 220 | fits | 34,286 | 3 | 0.896 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 53,047 | 0.663 | 220 | 220 | fits | 39,603 | 5 | 0.898 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 35,833 | 0.448 | 20 | 20 | fits | 35,899 | 14 | 0.879 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 222,528 | 2.782 | 20 | 200 | fits | 95,713 | 112 | 0.524 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 206,391 | 2.580 | 20 | 20 | fits | 95,713 | 112 | 0.524 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 288,453 | 3.606 | 20 | 24 | fits | 94,361 | 76 | 0.544 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 163,032 | 2.038 | 20 | 50 | fits | 85,715 | 191 | 0.401 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 789,111 | 9.864 | 20 | 20 | fits | 37,961 | 17 | 0.771 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 40,316 | 0.504 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 174,642 | 2.183 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
