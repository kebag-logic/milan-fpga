### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 6 paths and 0 of 27 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record, every channel at its refill rate, the longest | 0 | `save-burst.held.acmp.if0` (save-burst) | 2.352 | fits | 11 acmp | 4 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-burst.held.adp.if0` (save-burst) | 1.558 | fits | 7 adp | 4 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.906 | fits | 15 aecp | 4 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-flight.held.maap.if0` (save-flight) | 2.505 | fits | 6 maap | 4 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 10.016 | fits | 31 srp | 4 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.688 | fits | 0 srp | 7 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-flight | 3131 | 0 | 156,656 (1.567) | fits |
| save-burst | 2916 | 0 | 156,656 (1.567) | fits |
| save-second | 43978 | 0 | 50,411 (0.504) | fits |
| save-held | 1467 | 0 | 156,656 (1.567) | fits |
| save-starved | 23117 | 0 | 156,656 (1.567) | fits |
| save | 610 | 0 | 44,974 (0.450) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.340 | 6,070 | 102 | 2 | 30.865 | yes | within |
| save-held | 1097.164 | 4,070 | 102 | - | 17.213 | no | within |
| save-starved | 4049.108 | 4,070 | 102 | - | 31.292 | yes | within |
| save | 1081.825 | 4,070 | 102 | - | 26.002 | no | within |

Names from their response to durable (save_burst.py; #920, the ruling of #665 issuecomment-6899740728, item 1):

| Group | Names | Latest, ms (name) | Target ms | Saves | Not durable | Over | At the cut, or the next save | Verdict |
|---|---:|---:|---:|---:|---|---|---|---|
| save-flight | 1 | 165.045 (0) | 5,000 | 2 | - | - | 19 steps (want 19), 7.939 ms | within |
| save-burst | 39 | 1107.785 (0) | 5,000 | 1 | - | - | sequence 1, 0 missing | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-flight | 1552 | 94,464 (0.945) | 78,131 (0.781) |
| save-burst | 1479 | 94,319 (0.943) | 77,837 (0.778) |
| save-second | 520 | 79,900 (0.799) | 77,850 (0.778) |
| save-held | 815 | 94,464 (0.945) | 78,052 (0.781) |
| save-starved | 418 | 80,886 (0.809) | 78,414 (0.784) |
| save | 679 | 94,319 (0.943) | 77,902 (0.779) |

Longest pass that carries a step: 94,464 CPU cycles (0.945 ms), save-flight; longest step: 78,414 (0.784 ms), save-starved.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-flight.held.adp.if0` | 155,716 | 1.557 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-flight.held.acmp.if0` | 222,105 | 2.221 | 20 | 20 | fits | 86,526 | 82 | 0.667 |
| AECP record, every channel at its refill rate, the longest | `save-flight.held.aecp.if0` | 290,316 | 2.903 | 20 | 24 | fits | 64,228 | 44 | 0.500 |
| MAAP record, every channel at its refill rate, the longest | `save-flight.held.maap.if0` | 250,535 | 2.505 | 20 | 50 | fits | 112,991 | 211 | 0.323 |
| SRP record, every channel at its refill rate, the longest | `save-flight.held.srp.if0` | 936,401 | 9.364 | 20 | 20 | fits | 33,993 | 12 | 0.827 |
| an MRPDU its join timer owes, the longest | `save-flight.mrpdu.join.if0` | 55,477 | 0.555 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-flight.mrpdu.leaveall.if0` | 56,448 | 0.564 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-flight.mrpdu.periodic.if0` | 220,201 | 2.202 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-burst.held.adp.if0` | 155,847 | 1.558 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-burst.held.acmp.if0` | 235,192 | 2.352 | 20 | 20 | fits | 99,613 | 91 | 0.684 |
| AECP record, every channel at its refill rate, the longest | `save-burst.held.aecp.if0` | 171,984 | 1.720 | 20 | 24 | fits | 88,253 | 30 | 0.795 |
| MAAP record, every channel at its refill rate, the longest | `save-burst.held.maap.if0` | 195,717 | 1.957 | 20 | 50 | fits | 99,613 | 91 | 0.684 |
| SRP record, every channel at its refill rate, the longest | `save-burst.held.srp.if0` | 871,463 | 8.715 | 20 | 20 | fits | 81,813 | 32 | 0.736 |
| an MRPDU its join timer owes, the longest | `save-burst.mrpdu.join.if0` | 57,748 | 0.577 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-burst.mrpdu.periodic.if0` | 245,974 | 2.460 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 155,716 | 1.557 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 189,951 | 1.900 | 20 | 20 | fits | 105,910 | 115 | 0.361 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 290,570 | 2.906 | 20 | 24 | fits | 75,337 | 54 | 0.473 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 182,630 | 1.826 | 20 | 50 | fits | 86,526 | 82 | 0.667 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 941,935 | 9.419 | 20 | 20 | fits | 47,346 | 16 | 0.761 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 240,141 | 2.401 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 155,716 | 1.557 | 20 | 200 | fits | 156,656 | 250 | 0.467 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 203,917 | 2.039 | 20 | 20 | fits | 150,628 | 266 | 0.347 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 279,866 | 2.799 | 20 | 24 | fits | 78,747 | 60 | 0.501 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 186,095 | 1.861 | 20 | 50 | fits | 89,991 | 88 | 0.680 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 1,001,567 | 10.016 | 20 | 20 | fits | 64,248 | 26 | 0.736 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 268,832 | 2.688 | 20 | 20 | fits | 0 | - | 0.000 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
