### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 13 paths and 7 of 16 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.110 (0.605) | fits | 0 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.513 (63.699) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.512 (64.701) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.548 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.380 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.591 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 2.916 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.584 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.030 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.574 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.901 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 3.716 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.080 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.318 | 24 | 154,925 (1.549) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 154,925 CPU cycles (1.549 ms), backlog-owed.
Over the windows that released their whole load only: 154,925 (1.549 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 121192 | 0 | 54,315 (0.543) | fits |
| acmp-notk | 3357 | 0 | 46,812 (0.468) | fits |
| backlog-owed | 309 | 0 | 154,925 (1.549) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 22829.732 | 22,870 | 382 | 2 | 31.373 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 1080 | 80,939 (0.809) | 77,810 (0.778) |
| acmp-notk | 1065 | 108,952 (1.090) | 78,420 (0.784) |
| backlog-owed | 277 | 26,388 (0.264) | 2,374 (0.024) |

Longest pass that carries a step: 108,952 CPU cycles (1.090 ms), acmp-notk; longest step: 78,420 (0.784 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 10,984 | 0.110 | 20 | 20 | fits | 39,242 | 19 (14) | 0.889 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,268 | 63.513 | 20 | 20 | MISS ceiling | 23,931 | 13 | 0.639 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,379,938 | 63.799 | 20 | 20 | MISS ceiling | 27,295 | 18 | 0.716 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,402,679 | 64.027 | 20 | 20 | MISS ceiling | 25,065 | 13 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,427,343 | 64.273 | 20 | 20 | MISS ceiling | 24,114 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,451,225 | 64.512 | 20 | 20 | MISS ceiling | 23,755 | 13 | 0.630 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 159,106 | 1.591 | 20 | 200 | fits | 154,925 | 177 | 0.463 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 291,568 | 2.916 | 20 | 200 | fits | 133,078 | 207 | 0.400 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 154,784 | 1.548 | 20 | 20 | fits | 154,925 | 177 | 0.463 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,238,023 | 62.380 | 20 | 20 | MISS ceiling | 38,509 | 15 | 0.767 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 158,424 | 1.584 | 20 | 24 | fits | 154,925 | 177 | 0.463 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,203,000 | 62.030 | 20 | 24 | MISS ceiling | 153,808 | 106 | 0.409 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 157,368 | 1.574 | 20 | 50 | fits | 154,925 | 177 | 0.463 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 290,050 | 2.901 | 20 | 50 | fits | 133,078 | 207 | 0.400 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 371,560 | 3.716 | 20 | 20 | fits | 81,576 | 28 | 0.740 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 707,964 | 7.080 | 20 | 20 | fits | 85,132 | 36 | 0.555 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
