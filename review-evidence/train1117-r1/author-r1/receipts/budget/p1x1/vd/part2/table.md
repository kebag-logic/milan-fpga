### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 10 paths and 0 of 11 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.acmp.if0` (srp-talker-held) | 2.238 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.adp.if0` (srp-talker-held) | 1.560 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.aecp.if0` (srp-talker-held) | 2.891 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.maap.if0` (srp-talker-held) | 1.843 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `srp-talker-held.held.srp.if0` (srp-talker-held) | 9.289 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `srp-talker-held.mrpdu.periodic.if0` (srp-talker-held) | 2.865 | fits | 0 srp | 2 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s0.if0` (srp-talker-held) | 0.455 (0.455) | fits | 0 srp | 1 | 0 |
| Listener Ready RX beside a declared Talker | 0 | `srp.listener_ready.s1.if0` (srp-talker-held) | 0.450 (0.450) | fits | 0 srp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s0.if0` (srp-talker-held) | 0.655 (0.710) | fits | 0 acmp | 1 | 0 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | 0 | `srp.talker_declare.s1.if0` (srp-talker-held) | 187.373 (187.461) | fits | 0 acmp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp-talker-held | 1570 | 0 | 156,948 (1.569) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| srp-talker-held | 1097.678 | 4,070 | 102 | - | 17.217 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp-talker-held | 900 | 94,597 (0.946) | 77,926 (0.779) |

Longest pass that carries a step: 94,597 CPU cycles (0.946 ms), srp-talker-held; longest step: 77,926 (0.779 ms), srp-talker-held.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s0.if0` | 65,475 | 0.655 | 220 | 220 | fits | 42,126 | 5 | 0.903 |
| PROBE_TX -> Talker Advertise (JoinTime wait) | `srp.talker_declare.s1.if0` | 18,737,292 | 187.373 | 220 | 220 | fits | 36,456 | 3 | 0.861 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s0.if0` | 45,482 | 0.455 | 20 | 20 | fits | 45,548 | 15 | 0.876 |
| Listener Ready RX beside a declared Talker | `srp.listener_ready.s1.if0` | 44,976 | 0.450 | 20 | 20 | fits | 45,042 | 15 | 0.869 |
| ADP record, every channel at its refill rate, the longest | `srp-talker-held.held.adp.if0` | 156,008 | 1.560 | 20 | 200 | fits | 156,948 | 254 | 0.468 |
| ACMP record, every channel at its refill rate, the longest | `srp-talker-held.held.acmp.if0` | 223,773 | 2.238 | 20 | 20 | fits | 87,902 | 98 | 0.584 |
| AECP record, every channel at its refill rate, the longest | `srp-talker-held.held.aecp.if0` | 289,125 | 2.891 | 20 | 24 | fits | 81,799 | 51 | 0.612 |
| MAAP record, every channel at its refill rate, the longest | `srp-talker-held.held.maap.if0` | 184,298 | 1.843 | 20 | 50 | fits | 87,902 | 98 | 0.584 |
| SRP record, every channel at its refill rate, the longest | `srp-talker-held.held.srp.if0` | 928,900 | 9.289 | 20 | 20 | fits | 34,738 | 14 | 0.819 |
| an MRPDU its join timer owes, the longest | `srp-talker-held.mrpdu.join.if0` | 56,824 | 0.568 | 49 | 49 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `srp-talker-held.mrpdu.periodic.if0` | 286,465 | 2.865 | 49 | 49 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
