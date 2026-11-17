### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 10 paths and 0 of 11 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 2.279 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 1.562 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 3.102 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 1.884 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 9.144 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 2.968 | fits | 0 srp | 2 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.472 (0.473) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.465 (0.465) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker-held) | 0.678 (0.750) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker-held) | 187.395 (187.490) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker-held | 1556 | 0 | 157,101 (1.571) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 2019.218 | 4,070 | 102 | - | 15.663 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker-held | 807 | 101,774 (1.018) | 78,724 (0.787) |

Longest pass that carries a step: 101,774 CPU cycles (1.018 ms), srp-talker-held; longest step: 78,724 (0.787 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 67,771 | 0.678 | 220 | 220 | fits | 46,123 | 5 | 0.912 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,739,540 | 187.395 | 220 | 220 | fits | 37,848 | 3 | 0.854 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 47,205 | 0.472 | 20 | 20 | fits | 47,271 | 15 | 0.887 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 46,483 | 0.465 | 20 | 20 | fits | 46,549 | 15 | 0.876 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 156,161 | 1.562 | 20 | 200 | fits | 157,101 | 263 | 0.447 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 227,919 | 2.279 | 20 | 20 | fits | 91,895 | 93 | 0.613 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 310,173 | 3.102 | 20 | 24 | fits | 84,451 | 50 | 0.590 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 188,444 | 1.884 | 20 | 50 | fits | 91,895 | 93 | 0.613 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 914,421 | 9.144 | 20 | 20 | fits | 85,954 | 30 | 0.621 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 66,503 | 0.665 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 296,772 | 2.968 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
