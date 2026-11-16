### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 18 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.512 (0.837) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.580 (0.928) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.521 (0.854) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.594 (0.968) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.537 (0.889) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.554 (0.876) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.806 (5.098) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.647 (2.126) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.263 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 5.045 | fits | 11 acmp | 1 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.307 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 5.090 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.503 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.290 | fits | 15 aecp | 1 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.289 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 5.075 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.074 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog.service.srp.last.if0` (backlog) | 5.993 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.618 | 8 | 154,817 (1.548) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 154,817 CPU cycles (1.548 ms), backlog.
Over the windows that released their whole load only: 154,817 (1.548 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 287 | 0 | 154,817 (1.548) | fits |
| aecp-fanout | 109 | 0 | 59,921 (0.599) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 26,388 (0.264) | 2,374 (0.024) |
| aecp-fanout | 79 | 26,162 (0.262) | 2,374 (0.024) |

Longest pass that carries a step: 26,388 CPU cycles (0.264 ms), backlog; longest step: 2,374 (0.024 ms), backlog.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 164,708 | 1.647 | 20 | 200 | fits | 61,402 | 79 | 0.562 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 480,639 | 4.806 | 20 | 20 | fits | 78,969 | 67 | 0.492 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 430,661 | 4.307 | 20 | 200 | fits | 154,817 | 125 | 0.461 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 509,014 | 5.090 | 20 | 200 | fits | 78,969 | 67 | 0.492 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 426,339 | 4.263 | 20 | 20 | fits | 154,817 | 125 | 0.461 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 504,472 | 5.045 | 20 | 20 | fits | 78,969 | 67 | 0.492 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 150,309 | 1.503 | 20 | 24 | fits | 151,200 | 148 | 0.384 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 428,989 | 4.290 | 20 | 24 | fits | 154,817 | 125 | 0.461 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 428,923 | 4.289 | 20 | 50 | fits | 154,817 | 125 | 0.461 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 507,496 | 5.075 | 20 | 50 | fits | 78,969 | 67 | 0.492 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 507,430 | 5.074 | 20 | 20 | fits | 78,969 | 67 | 0.492 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 599,312 | 5.993 | 20 | 20 | fits | 25,089 | 32 | 0.307 |
| set_name | `aecp_fanout.set_name.if0` | 59,388 | 0.594 | 20 | 24 | fits | 59,921 | 89 | 0.575 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 58,007 | 0.580 | 20 | 24 | fits | 55,984 | 78 | 0.596 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 52,092 | 0.521 | 20 | 24 | fits | 50,943 | 79 | 0.543 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 43,885 | 0.439 | 20 | 24 | fits | 51,092 | 78 | 0.551 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 53,701 | 0.537 | 20 | 24 | fits | 54,997 | 67 | 0.579 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 51,206 | 0.512 | 20 | 24 | fits | 50,312 | 78 | 0.539 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 55,372 | 0.554 | 20 | 24 | fits | 49,903 | 79 | 0.540 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
