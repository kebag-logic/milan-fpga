### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 21 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.670 (2.995) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.405 (0.509) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.507 (0.833) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.440 (0.572) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.481 (0.771) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.520 (0.860) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.254 (3.581) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.453 (0.743) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.992 (4.215) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.702 (2.127) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.169 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 4.161 | fits | 11 acmp | 1 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.213 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 4.206 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.554 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.196 | fits | 15 aecp | 1 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.195 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 4.191 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.504 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog.service.srp.last.if0` (backlog) | 5.106 | fits | 31 srp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 5.629 | 7 | 156,321 (1.563) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 156,321 CPU cycles (1.563 ms), backlog.
Over the windows that released their whole load only: 156,321 (1.563 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 286 | 0 | 156,321 (1.563) | fits |
| aecp-fanout | 112 | 0 | 67,866 (0.679) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog | 265 | 22,507 (0.225) | 2,414 (0.024) |
| aecp-fanout | 80 | 23,660 (0.237) | 3,978 (0.040) |

Longest pass that carries a step: 23,660 CPU cycles (0.237 ms), aecp-fanout; longest step: 3,978 (0.040 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 170,222 | 1.702 | 20 | 200 | fits | 56,368 | 78 | 0.575 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 399,244 | 3.992 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 421,260 | 4.213 | 20 | 200 | fits | 148,870 | 167 | 0.396 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 420,644 | 4.206 | 20 | 200 | fits | 148,870 | 167 | 0.396 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 416,938 | 4.169 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 416,102 | 4.161 | 20 | 20 | fits | 148,870 | 167 | 0.396 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 155,430 | 1.554 | 20 | 24 | fits | 156,321 | 158 | 0.381 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 419,588 | 4.196 | 20 | 24 | fits | 148,870 | 167 | 0.396 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 419,522 | 4.195 | 20 | 50 | fits | 148,870 | 167 | 0.396 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 419,126 | 4.191 | 20 | 50 | fits | 148,870 | 167 | 0.396 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 450,436 | 4.504 | 20 | 20 | fits | 31,376 | 56 | 0.228 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 510,619 | 5.106 | 20 | 20 | fits | 24,668 | 41 | 0.192 |
| set_name | `aecp_fanout.set_name.if0` | 52,028 | 0.520 | 20 | 24 | fits | 67,866 | 95 | 0.596 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,991 | 0.440 | 20 | 24 | fits | 57,203 | 78 | 0.607 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 48,131 | 0.481 | 20 | 24 | fits | 54,975 | 79 | 0.567 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,928 | 0.409 | 20 | 24 | fits | 51,498 | 78 | 0.558 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 50,661 | 0.507 | 20 | 24 | fits | 61,126 | 66 | 0.642 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 267,027 | 2.670 | 20 | 24 | fits | 59,166 | 65 | 0.641 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 325,444 | 3.254 | 20 | 24 | fits | 54,632 | 67 | 0.603 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,461 | 0.405 | 20 | 24 | fits | 50,904 | 78 | 0.556 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,319 | 0.453 | 20 | 24 | fits | 50,939 | 79 | 0.553 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
