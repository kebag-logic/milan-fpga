### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 43 paths and 0 of 141 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.185 (0.496) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.221 (0.540) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.088 (0.243) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.112 (0.277) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.116 (0.274) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.247 (0.661) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.123 (0.432) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.156 (0.325) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.211 (0.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.208 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.101 (0.261) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.231 (0.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.105 (0.260) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.097 (0.265) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.109 (0.271) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.205 (0.525) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.110 (0.277) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.207 (0.530) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.213 (0.534) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.229 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.105 (0.266) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.188 (0.510) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.188 (0.451) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.094 (0.251) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.274 (0.655) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged1-2.adp_available.if0` (backlog-adp@blank-aged1-2) | 3.616 (4.116) | fits | 7 adp | 9 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.203 (0.562) | fits | 0 adp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.034 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 1.569 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.100 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.886 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.553 | fits | 31 srp | 1 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 2.962 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.acmp.first.if0` (backlog-adp@blank-aged2-2) | 3.164 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.acmp.last.if0` (backlog-adp@blank-aged2-2) | 4.126 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.adp.first.if0` (backlog-adp@blank-aged2-2) | 3.155 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.adp.last.if0` (backlog-adp@blank-aged2-2) | 4.119 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.aecp.first.if0` (backlog-adp@blank-aged2-2) | 1.696 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.aecp.last.if0` (backlog-adp@blank-aged2-2) | 3.190 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-2.service.maap.first.if0` (backlog-adp@blank-aged2-2) | 3.190 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.maap.last.if0` (backlog-adp@blank-aged2-2) | 4.156 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@verify-aged2-2.service.srp.first.if0` (backlog-adp@verify-aged2-2) | 5.066 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-2.service.srp.last.if0` (backlog-adp@blank-aged2-2) | 10.827 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-4 | 0 | 11.647 | 13 | 152,674 (1.527) | yes | - |
| backlog-adp@program-2 | 0 | 11.336 | 11 | 152,479 (1.525) | yes | - |
| backlog-adp@verify-2 | 0 | 11.268 | 11 | 152,836 (1.528) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 11.357 | 12 | 151,946 (1.519) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 12.368 | 15 | 152,191 (1.522) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 11.336 | 11 | 152,316 (1.523) | yes | - |
| backlog-adp@program-aged1-2 | 1 | 11.237 | 10 | 151,978 (1.520) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 11.292 | 11 | 152,485 (1.525) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 11.181 | 10 | 149,142 (1.491) | yes | - |
| backlog-adp-refill | 0 | 40.877 | 26 | 152,638 (1.526) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-owed not run): 152,638 CPU cycles (1.526 ms), backlog-adp-refill.
Over the windows that released their whole load only: 152,638 (1.526 ms), backlog-adp-refill.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-4 | 418 | 0 | 152,674 (1.527) | fits |
| backlog-adp@program-2 | 521 | 0 | 152,479 (1.525) | fits |
| backlog-adp@verify-2 | 614 | 0 | 152,836 (1.528) | fits |
| backlog-adp@blank-aged2-2 | 711 | 0 | 151,946 (1.519) | fits |
| backlog-adp@blank-aged1-2 | 658 | 0 | 152,191 (1.522) | fits |
| backlog-adp@program-aged2-2 | 811 | 0 | 152,316 (1.523) | fits |
| backlog-adp@program-aged1-2 | 753 | 0 | 153,328 (1.533) | fits |
| backlog-adp@verify-aged2-2 | 908 | 0 | 152,485 (1.525) | fits |
| backlog-adp@verify-aged1-2 | 849 | 0 | 152,485 (1.525) | fits |
| save-starved | 23773 | 0 | 157,878 (1.579) | fits |
| backlog-adp-refill | 330 | 0 | 152,638 (1.526) | fits |
| aecp | 112 | 0 | 45,138 (0.451) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 10.827 (20) | 9.173 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 10.614 (20) | 9.386 |
| backlog-adp@program-aged2-2 | 2 | +8.321 ms, 80,844 (0.808 ms), issue | none | `backlog-adp@program-aged2-2.service.srp.last.if0` | 10.803 (20) | 9.197 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 9.902 (20) | 10.098 |
| backlog-adp@verify-aged2-2 | 2 | +8.438 ms, 77,562 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 10.760 (20) | 9.240 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 9.884 (20) | 10.116 |

Least margin over the aged windows: 9.173 ms, `backlog-adp@blank-aged2-2.service.srp.last.if0` at 10.827 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 4049.350 | 4,070 | 102 | - | 30.900 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-4 | 299 | 93,212 (0.932) | 76,092 (0.761) |
| backlog-adp@program-2 | 328 | 96,938 (0.969) | 78,878 (0.789) |
| backlog-adp@verify-2 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@blank-aged2-2 | 297 | 86,094 (0.861) | 76,128 (0.761) |
| backlog-adp@blank-aged1-2 | 297 | 93,060 (0.931) | 76,109 (0.761) |
| backlog-adp@program-aged2-2 | 326 | 96,381 (0.964) | 78,723 (0.787) |
| backlog-adp@program-aged1-2 | 326 | 96,518 (0.965) | 78,923 (0.789) |
| backlog-adp@verify-aged2-2 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| backlog-adp@verify-aged1-2 | 355 | 96,381 (0.964) | 78,191 (0.782) |
| save-starved | 418 | 80,820 (0.808) | 78,162 (0.782) |
| backlog-adp-refill | 274 | 22,268 (0.223) | 2,344 (0.023) |
| aecp | 79 | 22,142 (0.221) | 2,242 (0.022) |

Longest pass that carries a step: 96,938 CPU cycles (0.969 ms), backlog-adp@program-2; longest step: 78,923 (0.789 ms), backlog-adp@program-aged1-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 339,939 | 3.399 | 20 | 20 | fits | 105,425 | 160 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 296,758 | 2.968 | 20 | 200 | fits | 147,318 | 236 | 0.392 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 409,923 | 4.099 | 20 | 200 | fits | 105,425 | 160 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 297,682 | 2.977 | 20 | 20 | fits | 147,318 | 236 | 0.392 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 410,627 | 4.106 | 20 | 20 | fits | 105,425 | 160 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 154,004 | 1.540 | 20 | 24 | fits | 152,674 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 300,332 | 3.003 | 20 | 24 | fits | 147,318 | 236 | 0.392 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 300,266 | 3.003 | 20 | 50 | fits | 147,318 | 236 | 0.392 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 413,651 | 4.137 | 20 | 50 | fits | 105,425 | 160 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 497,643 | 4.976 | 20 | 20 | fits | 84,058 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 989,368 | 9.894 | 20 | 20 | fits | 72,805 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 356,660 | 3.567 | 20 | 20 | fits | 97,310 | 154 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 308,703 | 3.087 | 20 | 200 | fits | 149,423 | 233 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 405,397 | 4.054 | 20 | 200 | fits | 97,310 | 154 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 309,627 | 3.096 | 20 | 20 | fits | 149,423 | 233 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 406,101 | 4.061 | 20 | 20 | fits | 97,310 | 154 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 163,844 | 1.638 | 20 | 24 | fits | 152,479 | 155 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 312,277 | 3.123 | 20 | 24 | fits | 149,423 | 233 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 312,211 | 3.122 | 20 | 50 | fits | 149,423 | 233 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 409,125 | 4.091 | 20 | 50 | fits | 97,310 | 154 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 497,978 | 4.980 | 20 | 20 | fits | 88,919 | 30 | 0.786 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 999,413 | 9.994 | 20 | 20 | fits | 72,802 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 343,587 | 3.436 | 20 | 20 | fits | 97,450 | 152 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 309,343 | 3.093 | 20 | 200 | fits | 150,538 | 237 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 406,177 | 4.062 | 20 | 200 | fits | 97,450 | 152 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 310,267 | 3.103 | 20 | 20 | fits | 150,538 | 237 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 406,881 | 4.069 | 20 | 20 | fits | 97,450 | 152 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 163,369 | 1.634 | 20 | 24 | fits | 152,836 | 155 | 0.395 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 312,917 | 3.129 | 20 | 24 | fits | 150,538 | 237 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 312,851 | 3.129 | 20 | 50 | fits | 150,538 | 237 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 409,905 | 4.099 | 20 | 50 | fits | 97,450 | 152 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 505,738 | 5.057 | 20 | 20 | fits | 86,997 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 997,089 | 9.971 | 20 | 20 | fits | 72,767 | 24 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 349,746 | 3.497 | 20 | 20 | fits | 97,014 | 151 | 0.439 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 315,465 | 3.155 | 20 | 200 | fits | 150,395 | 237 | 0.391 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 411,863 | 4.119 | 20 | 200 | fits | 97,014 | 151 | 0.439 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 316,389 | 3.164 | 20 | 20 | fits | 150,395 | 237 | 0.391 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 412,567 | 4.126 | 20 | 20 | fits | 97,014 | 151 | 0.439 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 169,634 | 1.696 | 20 | 24 | fits | 151,946 | 153 | 0.392 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 319,039 | 3.190 | 20 | 24 | fits | 150,395 | 237 | 0.391 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 318,973 | 3.190 | 20 | 50 | fits | 150,395 | 237 | 0.391 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 415,591 | 4.156 | 20 | 50 | fits | 97,014 | 151 | 0.439 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 499,273 | 4.993 | 20 | 20 | fits | 83,748 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 1,082,667 | 10.827 | 20 | 20 | fits | 85,478 | 28 | 0.623 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 361,599 | 3.616 | 20 | 20 | fits | 101,128 | 161 | 0.445 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 301,789 | 3.018 | 20 | 200 | fits | 149,707 | 234 | 0.396 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 410,876 | 4.109 | 20 | 200 | fits | 101,128 | 161 | 0.445 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 302,713 | 3.027 | 20 | 20 | fits | 149,707 | 234 | 0.396 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 411,580 | 4.116 | 20 | 20 | fits | 101,128 | 161 | 0.445 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 156,646 | 1.566 | 20 | 24 | fits | 152,191 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 305,363 | 3.054 | 20 | 24 | fits | 149,707 | 234 | 0.396 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 305,297 | 3.053 | 20 | 50 | fits | 149,707 | 234 | 0.396 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 414,604 | 4.146 | 20 | 50 | fits | 101,128 | 161 | 0.445 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 498,605 | 4.986 | 20 | 20 | fits | 84,067 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 1,061,360 | 10.614 | 20 | 20 | fits | 73,791 | 25 | 0.690 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 355,354 | 3.554 | 20 | 20 | fits | 97,360 | 154 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 307,397 | 3.074 | 20 | 200 | fits | 149,472 | 233 | 0.395 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 404,141 | 4.041 | 20 | 200 | fits | 97,360 | 154 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 308,321 | 3.083 | 20 | 20 | fits | 149,472 | 233 | 0.395 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 404,845 | 4.048 | 20 | 20 | fits | 97,360 | 154 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 162,489 | 1.625 | 20 | 24 | fits | 152,316 | 152 | 0.390 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 310,971 | 3.110 | 20 | 24 | fits | 149,472 | 233 | 0.395 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 310,905 | 3.109 | 20 | 50 | fits | 149,472 | 233 | 0.395 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 407,869 | 4.079 | 20 | 50 | fits | 97,360 | 154 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 491,792 | 4.918 | 20 | 20 | fits | 83,989 | 24 | 0.784 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 1,080,254 | 10.803 | 20 | 20 | fits | 85,443 | 28 | 0.622 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 332,262 | 3.323 | 20 | 20 | fits | 100,144 | 157 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 295,427 | 2.954 | 20 | 200 | fits | 151,978 | 242 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 394,955 | 3.950 | 20 | 200 | fits | 100,144 | 157 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 296,351 | 2.964 | 20 | 20 | fits | 151,978 | 242 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 395,659 | 3.957 | 20 | 20 | fits | 100,144 | 157 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 148,013 | 1.480 | 20 | 24 | fits | 153,328 | 157 | 0.388 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 299,001 | 2.990 | 20 | 24 | fits | 151,978 | 242 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 298,935 | 2.989 | 20 | 50 | fits | 151,978 | 242 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 398,683 | 3.987 | 20 | 50 | fits | 100,144 | 157 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 482,841 | 4.828 | 20 | 20 | fits | 84,224 | 24 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 990,160 | 9.902 | 20 | 20 | fits | 85,583 | 28 | 0.627 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 356,846 | 3.568 | 20 | 20 | fits | 96,756 | 152 | 0.428 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 310,850 | 3.108 | 20 | 200 | fits | 150,584 | 237 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 406,990 | 4.070 | 20 | 200 | fits | 96,756 | 152 | 0.428 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 311,774 | 3.118 | 20 | 20 | fits | 150,584 | 237 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 407,694 | 4.077 | 20 | 20 | fits | 96,756 | 152 | 0.428 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 164,830 | 1.648 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 314,424 | 3.144 | 20 | 24 | fits | 150,584 | 237 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 314,358 | 3.144 | 20 | 50 | fits | 150,584 | 237 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 410,718 | 4.107 | 20 | 50 | fits | 96,756 | 152 | 0.428 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 506,630 | 5.066 | 20 | 20 | fits | 86,979 | 31 | 0.779 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 1,075,969 | 10.760 | 20 | 20 | fits | 72,806 | 24 | 0.654 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 337,456 | 3.375 | 20 | 20 | fits | 99,222 | 142 | 0.413 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 294,934 | 2.949 | 20 | 200 | fits | 149,142 | 253 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 393,540 | 3.935 | 20 | 200 | fits | 99,222 | 142 | 0.413 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 295,858 | 2.959 | 20 | 20 | fits | 149,142 | 253 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 394,244 | 3.942 | 20 | 20 | fits | 99,222 | 142 | 0.413 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 150,356 | 1.504 | 20 | 24 | fits | 152,485 | 152 | 0.391 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 298,508 | 2.985 | 20 | 24 | fits | 149,142 | 253 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 298,442 | 2.984 | 20 | 50 | fits | 149,142 | 253 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 397,268 | 3.973 | 20 | 50 | fits | 99,222 | 142 | 0.413 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 481,386 | 4.814 | 20 | 20 | fits | 84,184 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 988,393 | 9.884 | 20 | 20 | fits | 85,326 | 28 | 0.617 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 156,938 | 1.569 | 20 | 200 | fits | 157,878 | 259 | 0.445 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 203,365 | 2.034 | 20 | 20 | fits | 143,916 | 268 | 0.343 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 309,975 | 3.100 | 20 | 24 | fits | 84,248 | 55 | 0.586 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 188,607 | 1.886 | 20 | 50 | fits | 91,281 | 83 | 0.687 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 955,287 | 9.553 | 20 | 20 | fits | 50,294 | 22 | 0.774 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 296,203 | 2.962 | 49 | 49 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 20,299 | 0.203 | 20 | 20 | fits | 27,160 | 19 | 0.818 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 298,765 | 2.988 | 20 | 200 | fits | 150,877 | 238 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 38,819 | 0.388 | 20 | 200 | fits | 27,160 | 19 | 0.818 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 299,689 | 2.997 | 20 | 20 | fits | 150,877 | 238 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 398,348 | 3.983 | 20 | 20 | fits | 90,818 | 148 | 0.414 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 152,452 | 1.525 | 20 | 24 | fits | 152,638 | 155 | 0.394 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 302,339 | 3.023 | 20 | 24 | fits | 150,877 | 238 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 302,273 | 3.023 | 20 | 50 | fits | 150,877 | 238 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 401,372 | 4.014 | 20 | 50 | fits | 90,818 | 148 | 0.414 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 484,540 | 4.845 | 20 | 20 | fits | 83,234 | 24 | 0.782 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 975,620 | 9.756 | 20 | 20 | fits | 72,762 | 24 | 0.653 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 18,787 | 0.188 | 20 | 24 | fits | 28,139 | 20 | 0.785 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 15,555 | 0.156 | 20 | 24 | fits | 32,482 | 20 | 0.727 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 21,065 | 0.211 | 20 | 24 | fits | 27,330 | 20 | 0.737 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 10,936 | 0.109 | 20 | 24 | fits | 27,146 | 20 | 0.733 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 21,306 | 0.213 | 20 | 24 | fits | 27,539 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 22,872 | 0.229 | 20 | 24 | fits | 27,881 | 20 | 0.744 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 10,496 | 0.105 | 20 | 24 | fits | 26,606 | 20 | 0.737 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 20,791 | 0.208 | 20 | 24 | fits | 26,945 | 20 | 0.751 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 10,117 | 0.101 | 20 | 24 | fits | 26,080 | 20 | 0.750 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 23,084 | 0.231 | 20 | 24 | fits | 29,169 | 21 | 0.649 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 10,484 | 0.105 | 20 | 24 | fits | 26,023 | 20 | 0.770 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,685 | 0.097 | 20 | 24 | fits | 26,460 | 20 | 0.770 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 20,525 | 0.205 | 20 | 24 | fits | 26,610 | 20 | 0.735 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 10,986 | 0.110 | 20 | 24 | fits | 27,651 | 20 | 0.747 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 20,731 | 0.207 | 20 | 24 | fits | 27,053 | 20 | 0.751 |
| get_configuration | `aecp.get_configuration.if0` | 8,793 | 0.088 | 20 | 24 | fits | 24,349 | 20 | 0.753 |
| entity_available | `aecp.entity_available.if0` | 18,527 | 0.185 | 20 | 24 | fits | 23,862 | 20 | 0.727 |
| get_name | `aecp.get_name.if0` | 11,613 | 0.116 | 20 | 24 | fits | 27,443 | 20 | 0.761 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,241 | 0.112 | 20 | 24 | fits | 27,731 | 27 | 0.723 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 22,107 | 0.221 | 20 | 24 | fits | 28,088 | 29 | 0.751 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,414 | 0.094 | 20 | 24 | fits | 25,101 | 20 | 0.769 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 12,290 | 0.123 | 20 | 24 | fits | 24,444 | 20 | 0.745 |
| set_name | `aecp.set_name.if0` | 18,759 | 0.188 | 20 | 24 | fits | 45,138 | 43 | 0.773 |
| lock_entity | `aecp.lock_entity.if0` | 24,690 | 0.247 | 20 | 24 | fits | 35,470 | 34 | 0.779 |
| unlock_entity | `aecp.unlock_entity.if0` | 27,353 | 0.274 | 20 | 24 | fits | 37,235 | 33 | 0.789 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
