### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 45 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 3.892 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 3.223 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 5.506 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 3.498 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 12.193 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 3.720 | fits | 0 srp | 3 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.491 (0.492) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.437 (0.437) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s2.if0` (srp-talker-held) | 0.440 (0.441) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s3.if0` (srp-talker-held) | 0.439 (0.440) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s4.if0` (srp-talker-held) | 0.439 (0.440) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s5.if0` (srp-talker-held) | 0.438 (0.439) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s6.if0` (srp-talker-held) | 0.446 (0.447) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s7.if0` (srp-talker-held) | 0.438 (0.438) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s8.if0` (srp-talker-held) | 0.442 (0.443) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker) | 0.529 (0.567) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker) | 185.617 (185.668) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker) | 189.590 (189.653) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker) | 189.446 (189.510) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker) | 179.560 (179.635) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker) | 9.200 (9.298) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker) | 189.373 (189.448) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker) | 188.623 (188.698) | fits | 0 acmp | 3 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker) | 188.647 (188.733) | fits | 0 acmp | 3 | 0 |
| range lost -> Talker Leave (JoinTime wait) | 0 | `srp.talker_loss.if0` (srp-talker-loss) | 188.771 (188.978) | fits | 0 maap | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker | 36254 | 0 | 46,243 (0.462) | fits |
| srp-talker-loss | 7688 | 0 | 47,968 (0.480) | fits |
| srp-talker-held | 25978 | 0 | 168,562 (1.686) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 1516.828 | 12,950 | 398 | - | 43.575 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker | 2058 | 36,565 (0.366) | 2,515 (0.025) |
| srp-talker-loss | 727 | 35,737 (0.357) | 2,515 (0.025) |
| srp-talker-held | 2172 | 108,760 (1.088) | 78,308 (0.783) |

Longest pass that carries a step: 108,760 CPU cycles (1.088 ms), srp-talker-held; longest step: 78,308 (0.783 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 52,942 | 0.529 | 220 | 220 | fits | 25,839 | 6 | 0.922 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,561,682 | 185.617 | 220 | 220 | fits | 18,232 | 4 | 0.899 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,959,008 | 189.590 | 220 | 220 | fits | 24,517 | 4 | 0.893 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,944,614 | 189.446 | 220 | 220 | fits | 23,311 | 4 | 0.892 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,955,954 | 179.560 | 220 | 220 | fits | 16,219 | 9 | 0.883 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 919,993 | 9.200 | 220 | 220 | fits | 32,966 | 4 | 0.856 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,937,302 | 189.373 | 220 | 220 | fits | 25,731 | 4 | 0.874 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,862,296 | 188.623 | 220 | 220 | fits | 26,153 | 4 | 0.873 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,864,697 | 188.647 | 220 | 220 | fits | 27,099 | 4 | 0.893 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 52,942 | 0.529 | 220 | 220 | fits | 25,839 | 6 | 0.922 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,561,682 | 185.617 | 220 | 220 | fits | 18,232 | 4 | 0.899 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,959,008 | 189.590 | 220 | 220 | fits | 24,517 | 4 | 0.893 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,944,614 | 189.446 | 220 | 220 | fits | 23,311 | 4 | 0.892 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,955,954 | 179.560 | 220 | 220 | fits | 16,219 | 9 | 0.883 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 919,993 | 9.200 | 220 | 220 | fits | 32,966 | 4 | 0.856 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,937,302 | 189.373 | 220 | 220 | fits | 25,731 | 4 | 0.874 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,862,296 | 188.623 | 220 | 220 | fits | 26,153 | 4 | 0.873 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,864,697 | 188.647 | 220 | 220 | fits | 27,099 | 4 | 0.893 |
| range lost -> Talker Leave (JoinTime wait) | `srp.talker_loss.if0` | 18,877,059 | 188.771 | 220 | 220 | fits | 47,968 | 4 | 0.835 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 52,942 | 0.529 | 220 | 220 | fits | 25,839 | 6 | 0.922 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,561,682 | 185.617 | 220 | 220 | fits | 18,232 | 4 | 0.899 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,959,008 | 189.590 | 220 | 220 | fits | 24,517 | 4 | 0.893 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,944,614 | 189.446 | 220 | 220 | fits | 23,311 | 4 | 0.892 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,955,954 | 179.560 | 220 | 220 | fits | 16,219 | 9 | 0.883 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 919,993 | 9.200 | 220 | 220 | fits | 32,966 | 4 | 0.856 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,937,302 | 189.373 | 220 | 220 | fits | 25,731 | 4 | 0.874 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,862,296 | 188.623 | 220 | 220 | fits | 26,153 | 4 | 0.873 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,864,697 | 188.647 | 220 | 220 | fits | 27,099 | 4 | 0.893 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 49,127 | 0.491 | 20 | 20 | fits | 49,193 | 40 | 0.807 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 43,681 | 0.437 | 20 | 20 | fits | 43,747 | 33 | 0.810 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s2.if0` | 44,038 | 0.440 | 20 | 20 | fits | 44,104 | 33 | 0.810 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s3.if0` | 43,913 | 0.439 | 20 | 20 | fits | 43,979 | 33 | 0.811 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s4.if0` | 43,916 | 0.439 | 20 | 20 | fits | 43,982 | 33 | 0.811 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s5.if0` | 43,806 | 0.438 | 20 | 20 | fits | 43,872 | 33 | 0.808 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s6.if0` | 44,649 | 0.446 | 20 | 20 | fits | 44,715 | 33 | 0.815 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s7.if0` | 43,780 | 0.438 | 20 | 20 | fits | 43,846 | 33 | 0.809 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s8.if0` | 44,215 | 0.442 | 20 | 20 | fits | 44,281 | 33 | 0.809 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 322,275 | 3.223 | 20 | 200 | fits | 143,104 | 192 | 0.552 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 389,235 | 3.892 | 20 | 20 | fits | 134,980 | 140 | 0.558 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 550,625 | 5.506 | 20 | 24 | fits | 67,776 | 46 | 0.585 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 349,760 | 3.498 | 20 | 50 | fits | 134,980 | 140 | 0.558 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 1,219,276 | 12.193 | 20 | 20 | fits | 47,177 | 37 | 0.792 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 95,212 | 0.952 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `srp-talker-held.mrpdu.leaveall.if0` | 88,875 | 0.889 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 372,032 | 3.720 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
