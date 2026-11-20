### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 26 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 4.573 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 3.166 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 4.176 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 4.178 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 12.908 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 3.751 | fits | 0 srp | 3 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.612 (0.612) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.619 (0.619) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s2.if0` (srp-talker-held) | 0.632 (0.633) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s3.if0` (srp-talker-held) | 0.637 (0.637) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s4.if0` (srp-talker-held) | 0.647 (0.648) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s5.if0` (srp-talker-held) | 0.826 (0.947) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s6.if0` (srp-talker-held) | 0.667 (0.668) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s7.if0` (srp-talker-held) | 0.866 (0.968) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s8.if0` (srp-talker-held) | 0.695 (0.696) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker-held) | 0.672 (0.713) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker-held) | 185.617 (185.677) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker-held) | 189.428 (189.590) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker-held) | 189.516 (189.594) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker-held) | 179.413 (179.498) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker-held) | 8.730 (8.945) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker-held) | 189.085 (189.199) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker-held) | 186.807 (186.930) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker-held) | 188.564 (188.686) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker-held | 25010 | 0 | 166,731 (1.667) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 1507.488 | 12,470 | 382 | - | 40.434 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker-held | 2079 | 109,457 (1.095) | 78,271 (0.783) |

Longest pass that carries a step: 109,457 CPU cycles (1.095 ms), srp-talker-held; longest step: 78,271 (0.783 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,193 | 0.672 | 220 | 220 | fits | 39,495 | 5 | 0.913 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,561,717 | 185.617 | 220 | 220 | fits | 32,443 | 3 | 0.901 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,942,764 | 189.428 | 220 | 220 | fits | 46,375 | 13 | 0.867 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,951,578 | 189.516 | 220 | 220 | fits | 40,644 | 3 | 0.878 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,941,309 | 179.413 | 220 | 220 | fits | 29,622 | 8 | 0.879 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 872,993 | 8.730 | 220 | 220 | fits | 73,959 | 13 | 0.850 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,908,453 | 189.085 | 220 | 220 | fits | 50,387 | 3 | 0.879 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,680,743 | 186.807 | 220 | 220 | fits | 51,701 | 3 | 0.878 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,856,418 | 188.564 | 220 | 220 | fits | 46,781 | 3 | 0.885 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 61,178 | 0.612 | 20 | 20 | fits | 61,244 | 31 | 0.842 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 61,866 | 0.619 | 20 | 20 | fits | 61,932 | 31 | 0.833 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s2.if0` | 63,186 | 0.632 | 20 | 20 | fits | 63,252 | 31 | 0.831 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s3.if0` | 63,678 | 0.637 | 20 | 20 | fits | 63,744 | 31 | 0.830 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s4.if0` | 64,686 | 0.647 | 20 | 20 | fits | 64,752 | 31 | 0.831 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s5.if0` | 82,558 | 0.826 | 20 | 20 | fits | 65,942 | 28 | 0.857 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s6.if0` | 66,712 | 0.667 | 20 | 20 | fits | 66,778 | 31 | 0.831 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s7.if0` | 86,630 | 0.866 | 20 | 20 | fits | 68,106 | 28 | 0.855 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s8.if0` | 69,523 | 0.695 | 20 | 20 | fits | 69,589 | 31 | 0.830 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 316,590 | 3.166 | 20 | 200 | fits | 138,354 | 205 | 0.390 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 457,252 | 4.573 | 20 | 20 | fits | 143,232 | 117 | 0.534 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 417,650 | 4.176 | 20 | 24 | fits | 138,199 | 75 | 0.623 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 417,777 | 4.178 | 20 | 50 | fits | 143,232 | 117 | 0.534 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 1,290,828 | 12.908 | 20 | 20 | fits | 132,930 | 50 | 0.750 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 253,323 | 2.533 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `srp-talker-held.mrpdu.leaveall.if0` | 135,460 | 1.355 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 375,101 | 3.751 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `srp-talker-held`: wait quiet TIMEOUT
- `srp-talker-held`: wait quiet TIMEOUT
