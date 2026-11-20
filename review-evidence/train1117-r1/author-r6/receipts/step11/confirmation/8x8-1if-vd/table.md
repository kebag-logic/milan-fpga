### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 26 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 4.504 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 3.557 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 4.504 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 4.109 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 13.142 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 4.154 | fits | 0 srp | 3 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.604 (0.604) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.866 (0.915) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s2.if0` (srp-talker-held) | 0.623 (0.624) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s3.if0` (srp-talker-held) | 0.815 (0.925) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s4.if0` (srp-talker-held) | 0.637 (0.637) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s5.if0` (srp-talker-held) | 0.694 (0.695) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s6.if0` (srp-talker-held) | 0.662 (0.663) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s7.if0` (srp-talker-held) | 0.668 (0.669) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s8.if0` (srp-talker-held) | 0.687 (0.687) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker-held) | 0.671 (0.711) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker-held) | 185.669 (185.728) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s2.if0` (srp-talker-held) | 189.656 (189.726) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s3.if0` (srp-talker-held) | 189.406 (189.483) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s4.if0` (srp-talker-held) | 179.209 (179.297) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s5.if0` (srp-talker-held) | 8.800 (8.911) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s6.if0` (srp-talker-held) | 189.074 (189.187) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s7.if0` (srp-talker-held) | 187.788 (187.909) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s8.if0` (srp-talker-held) | 188.684 (188.804) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker-held | 25383 | 0 | 165,832 (1.658) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 1518.987 | 12,470 | 382 | - | 40.325 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker-held | 2122 | 109,204 (1.092) | 78,319 (0.783) |

Longest pass that carries a step: 109,204 CPU cycles (1.092 ms), srp-talker-held; longest step: 78,319 (0.783 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,057 | 0.671 | 220 | 220 | fits | 39,697 | 5 | 0.913 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,566,876 | 185.669 | 220 | 220 | fits | 32,479 | 3 | 0.901 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s2.if0` | 18,965,564 | 189.656 | 220 | 220 | fits | 37,029 | 3 | 0.880 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s3.if0` | 18,940,590 | 189.406 | 220 | 220 | fits | 40,799 | 3 | 0.880 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s4.if0` | 17,920,857 | 179.209 | 220 | 220 | fits | 30,408 | 8 | 0.882 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s5.if0` | 880,025 | 8.800 | 220 | 220 | fits | 63,267 | 3 | 0.851 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s6.if0` | 18,907,417 | 189.074 | 220 | 220 | fits | 50,471 | 3 | 0.879 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s7.if0` | 18,778,805 | 187.788 | 220 | 220 | fits | 51,688 | 3 | 0.879 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s8.if0` | 18,868,434 | 188.684 | 220 | 220 | fits | 46,857 | 3 | 0.885 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 60,372 | 0.604 | 20 | 20 | fits | 60,438 | 31 | 0.836 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 86,634 | 0.866 | 20 | 20 | fits | 59,445 | 23 | 0.861 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s2.if0` | 62,313 | 0.623 | 20 | 20 | fits | 62,379 | 31 | 0.827 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s3.if0` | 81,471 | 0.815 | 20 | 20 | fits | 63,687 | 28 | 0.852 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s4.if0` | 63,679 | 0.637 | 20 | 20 | fits | 63,745 | 31 | 0.824 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s5.if0` | 69,392 | 0.694 | 20 | 20 | fits | 69,458 | 37 | 0.810 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s6.if0` | 66,188 | 0.662 | 20 | 20 | fits | 66,254 | 31 | 0.826 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s7.if0` | 66,811 | 0.668 | 20 | 20 | fits | 66,877 | 31 | 0.825 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s8.if0` | 68,652 | 0.687 | 20 | 20 | fits | 68,718 | 31 | 0.825 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 355,703 | 3.557 | 20 | 200 | fits | 161,428 | 194 | 0.482 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 450,373 | 4.504 | 20 | 20 | fits | 141,563 | 115 | 0.540 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 450,408 | 4.504 | 20 | 24 | fits | 151,131 | 90 | 0.592 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 410,898 | 4.109 | 20 | 50 | fits | 141,563 | 115 | 0.540 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 1,314,159 | 13.142 | 20 | 20 | fits | 104,670 | 36 | 0.735 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 166,345 | 1.663 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `srp-talker-held.mrpdu.leaveall.if0` | 124,990 | 1.250 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 415,420 | 4.154 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `srp-talker-held`: wait quiet TIMEOUT
- `srp-talker-held`: wait quiet TIMEOUT
- `srp-talker-held`: wait quiet TIMEOUT
