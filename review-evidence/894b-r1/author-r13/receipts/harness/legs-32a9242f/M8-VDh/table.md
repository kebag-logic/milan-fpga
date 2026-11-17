### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 26 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 3.904 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 3.174 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 4.253 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 3.510 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 10.869 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 3.109 | fits | 0 srp | 3 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.557 (0.558) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.551 (0.552) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s2.if0` (srp-talker-held) | 0.566 (0.567) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s3.if0` (srp-talker-held) | 0.567 (0.567) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s4.if0` (srp-talker-held) | 0.575 (0.576) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s5.if0` (srp-talker-held) | 0.581 (0.582) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s6.if0` (srp-talker-held) | 0.601 (0.602) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s7.if0` (srp-talker-held) | 0.630 (0.630) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s8.if0` (srp-talker-held) | 0.620 (0.620) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker-held) | 0.677 (0.715) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker-held) | 186.993 (187.045) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker-held) | 189.528 (189.589) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker-held) | 189.523 (189.613) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker-held) | 179.386 (179.462) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker-held) | 9.415 (9.534) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker-held) | 189.176 (189.297) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker-held) | 189.350 (189.471) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker-held) | 189.255 (189.380) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker-held | 3460 | 0 | 166,622 (1.666) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 4814.124 | 12,470 | 382 | - | 16.731 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker-held | 1782 | 107,662 (1.077) | 78,304 (0.783) |

Longest pass that carries a step: 107,662 CPU cycles (1.077 ms), srp-talker-held; longest step: 78,304 (0.783 ms), srp-talker-held.

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
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 55,746 | 0.557 | 20 | 20 | fits | 55,812 | 22 | 0.864 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 55,104 | 0.551 | 20 | 20 | fits | 55,170 | 22 | 0.848 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s2.if0` | 56,613 | 0.566 | 20 | 20 | fits | 56,679 | 22 | 0.847 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s3.if0` | 56,670 | 0.567 | 20 | 20 | fits | 56,736 | 22 | 0.846 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s4.if0` | 57,503 | 0.575 | 20 | 20 | fits | 57,569 | 22 | 0.847 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s5.if0` | 58,099 | 0.581 | 20 | 20 | fits | 58,165 | 22 | 0.846 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s6.if0` | 60,141 | 0.601 | 20 | 20 | fits | 60,207 | 22 | 0.846 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s7.if0` | 62,980 | 0.630 | 20 | 20 | fits | 63,046 | 22 | 0.859 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s8.if0` | 61,963 | 0.620 | 20 | 20 | fits | 62,029 | 22 | 0.848 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 317,449 | 3.174 | 20 | 200 | fits | 151,767 | 191 | 0.491 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 390,425 | 3.904 | 20 | 20 | fits | 147,508 | 112 | 0.495 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 425,281 | 4.253 | 20 | 24 | fits | 140,592 | 70 | 0.519 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 350,950 | 3.510 | 20 | 50 | fits | 147,508 | 112 | 0.495 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 1,086,867 | 10.869 | 20 | 20 | fits | 124,696 | 41 | 0.622 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 138,890 | 1.389 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `srp-talker-held.mrpdu.leaveall.if0` | 105,369 | 1.054 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 310,874 | 3.109 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
