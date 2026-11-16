### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 54 paths and 1 of 253 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.094 (0.312) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.076 (0.290) | fits | 0 adp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.251 (0.647) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.282 (0.589) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.214 (0.585) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.069 (0.330) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.157 (0.550) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.023 (0.342) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-link) | 0.027 (0.307) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-link) | 0.174 (0.521) | fits | 0 events | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.179 (0.527) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.157 (0.508) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.123 (0.476) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.213 (0.573) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.143 (0.493) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.235 (0.635) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.176 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.236 (0.592) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.142 (0.490) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.138 (0.484) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.201 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.247 (0.606) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.138 (0.486) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.197 (0.554) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.146 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.138 (0.485) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.205 (0.562) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.188 (0.492) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.202 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.150 (0.499) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.198 (0.552) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.112 (0.464) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.257 (0.704) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.218 (0.569) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.180 (0.590) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.872 (5.281) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-5.adp_available.if0` (backlog-adp@program-5) | 3.851 (5.429) | fits | 7 adp | 18 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.655 (2.088) | fits | 15 events | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 2.457 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.658 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 3.122 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.800 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 9.210 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.leaveall.if0` (save-starved) | 161.069 | MISS ceiling | 0 srp | 3 | 1 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.511 | fits | 0 acmp | 19 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 5.228 | fits | 11 acmp | 19 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.554 | fits | 0 adp | 19 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 4.548 | fits | 7 adp | 19 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-5.service.aecp.first.if0` (backlog-adp@blank-5) | 1.606 | fits | 0 aecp | 19 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-5.service.aecp.last.if0` (backlog-adp@blank-5) | 3.162 | fits | 15 aecp | 19 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.537 | fits | 0 maap | 19 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-1.service.maap.last.if0` (backlog-adp@program-1) | 4.571 | fits | 6 maap | 19 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-5.service.srp.first.if0` (backlog-adp@blank-5) | 5.501 | fits | 0 srp | 19 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 10.504 | fits | 31 srp | 19 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-2 | 0 | 11.101 | 10 | 147,986 (1.480) | yes | - |
| backlog-adp@blank-5 | 0 | 11.352 | 12 | 148,776 (1.488) | yes | - |
| backlog-adp@program-1 | 0 | 11.602 | 12 | 148,033 (1.480) | yes | - |
| backlog-adp@program-5 | 0 | 10.601 | 12 | 147,178 (1.472) | yes | - |
| backlog-adp@verify-1 | 0 | 11.082 | 10 | 147,754 (1.478) | yes | - |
| backlog-adp@verify-5 | 0 | 11.269 | 12 | 149,094 (1.491) | yes | - |
| backlog-adp@blank-aged2-1 | 1 | 11.251 | 11 | 148,846 (1.488) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 11.011 | 10 | 148,068 (1.481) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.059 | 10 | 147,554 (1.476) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.970 | 10 | 147,964 (1.480) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 11.294 | 12 | 148,644 (1.486) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 11.074 | 10 | 147,795 (1.478) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 11.483 | 12 | 147,998 (1.480) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 11.089 | 10 | 147,691 (1.477) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.884 | 10 | 147,836 (1.478) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 11.068 | 10 | 148,615 (1.486) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 11.272 | 12 | 149,202 (1.492) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 11.036 | 10 | 147,570 (1.476) | yes | - |
| backlog | 0 | 6.416 | 7 | 152,954 (1.530) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 152,954 CPU cycles (1.530 ms), backlog.
Over the windows that released their whole load only: 152,954 (1.530 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-starved | 64557 | 0 | 155,509 (1.555) | fits |
| backlog-adp@blank-2 | 536 | 0 | 147,986 (1.480) | fits |
| backlog-adp@blank-5 | 538 | 0 | 148,776 (1.488) | fits |
| backlog-adp@program-1 | 894 | 0 | 148,033 (1.480) | fits |
| backlog-adp@program-5 | 897 | 0 | 147,178 (1.472) | fits |
| backlog-adp@verify-1 | 1242 | 0 | 147,754 (1.478) | fits |
| backlog-adp@verify-5 | 1244 | 0 | 149,094 (1.491) | fits |
| backlog-adp@blank-aged2-1 | 820 | 0 | 148,846 (1.488) | fits |
| backlog-adp@blank-aged2-5 | 847 | 0 | 148,068 (1.481) | fits |
| backlog-adp@blank-aged1-1 | 762 | 0 | 147,554 (1.476) | fits |
| backlog-adp@blank-aged1-5 | 790 | 0 | 147,964 (1.480) | fits |
| backlog-adp@program-aged2-1 | 1172 | 0 | 148,644 (1.486) | fits |
| backlog-adp@program-aged2-5 | 1199 | 0 | 147,795 (1.478) | fits |
| backlog-adp@program-aged1-1 | 1115 | 0 | 147,998 (1.480) | fits |
| backlog-adp@program-aged1-5 | 1142 | 0 | 147,691 (1.477) | fits |
| backlog-adp@verify-aged2-1 | 1522 | 0 | 147,836 (1.478) | fits |
| backlog-adp@verify-aged2-5 | 1551 | 0 | 148,615 (1.486) | fits |
| backlog-adp@verify-aged1-1 | 1467 | 0 | 149,202 (1.492) | fits |
| backlog-adp@verify-aged1-5 | 1494 | 0 | 147,570 (1.476) | fits |
| acmp-noresp | 1879 | 0 | 94,822 (0.948) | fits |
| backlog | 284 | 0 | 152,954 (1.530) | fits |
| acmp-disc | 870 | 0 | 94,822 (0.948) | fits |
| adp-link | 88 | 0 | 94,822 (0.948) | fits |
| aecp | 112 | 0 | 94,822 (0.948) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | +9.637 ms, 75,986 (0.760 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.600 (20) | 10.400 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.445 (20) | 9.555 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.730 (20) | 10.270 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.647 (20) | 10.353 |
| backlog-adp@program-aged2-1 | 2 | none | none | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.619 (20) | 10.381 |
| backlog-adp@program-aged2-5 | 2 | +5.485 ms, 80,677 (0.807 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.504 (20) | 9.496 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.622 (20) | 10.378 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.714 (20) | 10.286 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.736 ms, 77,037 (0.770 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.698 (20) | 10.302 |
| backlog-adp@verify-aged2-5 | 2 | +5.361 ms, 77,299 (0.773 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.499 (20) | 9.501 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.635 (20) | 10.365 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.700 (20) | 10.300 |

Least margin over the aged windows: 9.496 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 10.504 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 12447.193 | 12,470 | 382 | - | 32.659 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-starved | 698 | 82,021 (0.820) | 78,361 (0.784) |
| backlog-adp@blank-2 | 339 | 93,471 (0.935) | 75,531 (0.755) |
| backlog-adp@blank-5 | 339 | 92,266 (0.923) | 75,487 (0.755) |
| backlog-adp@program-1 | 448 | 100,309 (1.003) | 78,162 (0.782) |
| backlog-adp@program-5 | 449 | 100,309 (1.003) | 77,865 (0.779) |
| backlog-adp@verify-1 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-5 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@blank-aged2-1 | 337 | 77,166 (0.772) | 75,321 (0.753) |
| backlog-adp@blank-aged2-5 | 337 | 85,616 (0.856) | 75,543 (0.755) |
| backlog-adp@blank-aged1-1 | 337 | 93,944 (0.939) | 75,713 (0.757) |
| backlog-adp@blank-aged1-5 | 337 | 93,300 (0.933) | 75,583 (0.756) |
| backlog-adp@program-aged2-1 | 446 | 100,309 (1.003) | 78,187 (0.782) |
| backlog-adp@program-aged2-5 | 446 | 100,309 (1.003) | 78,089 (0.781) |
| backlog-adp@program-aged1-1 | 446 | 100,309 (1.003) | 78,162 (0.782) |
| backlog-adp@program-aged1-5 | 446 | 100,309 (1.003) | 78,213 (0.782) |
| backlog-adp@verify-aged2-1 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged2-5 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-1 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| backlog-adp@verify-aged1-5 | 555 | 104,105 (1.041) | 78,512 (0.785) |
| acmp-noresp | 615 | 104,170 (1.042) | 78,512 (0.785) |
| backlog | 265 | 25,967 (0.260) | 2,512 (0.025) |
| acmp-disc | 306 | 103,081 (1.031) | 75,905 (0.759) |
| adp-link | 79 | 25,733 (0.257) | 2,512 (0.025) |
| aecp | 80 | 25,733 (0.257) | 2,512 (0.025) |

Longest pass that carries a step: 104,170 CPU cycles (1.042 ms), acmp-noresp; longest step: 78,512 (0.785 ms), backlog-adp@verify-1.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 265,806 | 2.658 | 20 | 200 | fits | 111,237 | 139 | 0.459 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 245,669 | 2.457 | 20 | 20 | fits | 111,237 | 139 | 0.459 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 312,214 | 3.122 | 20 | 24 | fits | 93,895 | 65 | 0.543 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 180,048 | 1.800 | 20 | 50 | fits | 82,314 | 112 | 0.449 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 921,000 | 9.210 | 20 | 20 | fits | 59,328 | 26 | 0.677 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 109,866 | 1.099 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 16,106,908 | 161.069 | 20 | 20 | MISS ceiling | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 379,568 | 3.796 | 20 | 20 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 378,219 | 3.782 | 20 | 20 | fits | 138,670 | 163 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 302,794 | 3.028 | 20 | 200 | fits | 147,986 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 440,848 | 4.408 | 20 | 200 | fits | 138,670 | 163 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 303,718 | 3.037 | 20 | 20 | fits | 147,986 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 441,552 | 4.416 | 20 | 20 | fits | 138,670 | 163 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 159,372 | 1.594 | 20 | 24 | fits | 145,179 | 164 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 306,368 | 3.064 | 20 | 24 | fits | 147,986 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 306,302 | 3.063 | 20 | 50 | fits | 147,986 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 444,576 | 4.446 | 20 | 50 | fits | 138,670 | 163 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 534,452 | 5.345 | 20 | 20 | fits | 89,942 | 25 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 977,563 | 9.776 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 379,383 | 3.794 | 20 | 20 | fits | 139,130 | 163 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 312,611 | 3.126 | 20 | 200 | fits | 148,776 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 451,125 | 4.511 | 20 | 200 | fits | 139,130 | 163 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 313,535 | 3.135 | 20 | 20 | fits | 148,776 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 451,829 | 4.518 | 20 | 20 | fits | 139,130 | 163 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 160,617 | 1.606 | 20 | 24 | fits | 145,334 | 165 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 316,185 | 3.162 | 20 | 24 | fits | 148,776 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 316,119 | 3.161 | 20 | 50 | fits | 148,776 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 454,853 | 4.549 | 20 | 50 | fits | 139,130 | 163 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 550,112 | 5.501 | 20 | 20 | fits | 95,325 | 30 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 972,345 | 9.723 | 20 | 20 | fits | 67,509 | 25 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 380,973 | 3.810 | 20 | 20 | fits | 142,903 | 170 | 0.447 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 302,375 | 3.024 | 20 | 200 | fits | 148,033 | 218 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 453,362 | 4.534 | 20 | 200 | fits | 142,903 | 170 | 0.447 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 303,299 | 3.033 | 20 | 20 | fits | 148,033 | 218 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 454,066 | 4.541 | 20 | 20 | fits | 142,903 | 170 | 0.447 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 158,906 | 1.589 | 20 | 24 | fits | 145,327 | 164 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 305,949 | 3.059 | 20 | 24 | fits | 148,033 | 218 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 305,883 | 3.059 | 20 | 50 | fits | 148,033 | 218 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 457,090 | 4.571 | 20 | 50 | fits | 142,903 | 170 | 0.447 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 546,419 | 5.464 | 20 | 20 | fits | 89,395 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 974,457 | 9.745 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 385,127 | 3.851 | 20 | 20 | fits | 140,178 | 166 | 0.415 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 307,494 | 3.075 | 20 | 200 | fits | 147,178 | 218 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 447,056 | 4.471 | 20 | 200 | fits | 140,178 | 166 | 0.415 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 308,418 | 3.084 | 20 | 20 | fits | 147,178 | 218 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 447,760 | 4.478 | 20 | 20 | fits | 140,178 | 166 | 0.415 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 157,086 | 1.571 | 20 | 24 | fits | 145,806 | 165 | 0.363 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 311,068 | 3.111 | 20 | 24 | fits | 147,178 | 218 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 311,002 | 3.110 | 20 | 50 | fits | 147,178 | 218 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 450,784 | 4.508 | 20 | 50 | fits | 140,178 | 166 | 0.415 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 539,804 | 5.398 | 20 | 20 | fits | 89,086 | 24 | 0.765 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 967,938 | 9.679 | 20 | 20 | fits | 67,509 | 25 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 374,256 | 3.743 | 20 | 20 | fits | 138,689 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 298,749 | 2.987 | 20 | 200 | fits | 147,754 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 436,822 | 4.368 | 20 | 200 | fits | 138,689 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 299,673 | 2.997 | 20 | 20 | fits | 147,754 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 437,526 | 4.375 | 20 | 20 | fits | 138,689 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 155,559 | 1.556 | 20 | 24 | fits | 145,450 | 164 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 302,323 | 3.023 | 20 | 24 | fits | 147,754 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 302,257 | 3.023 | 20 | 50 | fits | 147,754 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 440,550 | 4.405 | 20 | 50 | fits | 138,689 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 530,134 | 5.301 | 20 | 20 | fits | 89,650 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 974,857 | 9.749 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 369,791 | 3.698 | 20 | 20 | fits | 139,126 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 303,540 | 3.035 | 20 | 200 | fits | 149,094 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 442,050 | 4.420 | 20 | 200 | fits | 139,126 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 304,464 | 3.045 | 20 | 20 | fits | 149,094 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 442,754 | 4.428 | 20 | 20 | fits | 139,126 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 151,321 | 1.513 | 20 | 24 | fits | 145,457 | 165 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 307,114 | 3.071 | 20 | 24 | fits | 149,094 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 307,048 | 3.070 | 20 | 50 | fits | 149,094 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 445,778 | 4.458 | 20 | 50 | fits | 139,126 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 540,875 | 5.409 | 20 | 20 | fits | 95,163 | 30 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 963,107 | 9.631 | 20 | 20 | fits | 67,509 | 25 | 0.590 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 366,346 | 3.663 | 20 | 20 | fits | 142,982 | 169 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 287,198 | 2.872 | 20 | 200 | fits | 148,846 | 223 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 438,248 | 4.382 | 20 | 200 | fits | 142,982 | 169 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 288,122 | 2.881 | 20 | 20 | fits | 148,846 | 223 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 438,952 | 4.390 | 20 | 20 | fits | 142,982 | 169 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 142,916 | 1.429 | 20 | 24 | fits | 144,525 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 290,772 | 2.908 | 20 | 24 | fits | 148,846 | 223 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 290,706 | 2.907 | 20 | 50 | fits | 148,846 | 223 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 441,976 | 4.420 | 20 | 50 | fits | 142,982 | 169 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 531,922 | 5.319 | 20 | 20 | fits | 90,012 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 959,961 | 9.600 | 20 | 20 | fits | 73,403 | 30 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 369,229 | 3.692 | 20 | 20 | fits | 138,756 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 293,790 | 2.938 | 20 | 200 | fits | 148,068 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 431,930 | 4.319 | 20 | 200 | fits | 138,756 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 294,714 | 2.947 | 20 | 20 | fits | 148,068 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 432,634 | 4.326 | 20 | 20 | fits | 138,756 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 150,286 | 1.503 | 20 | 24 | fits | 144,644 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 297,364 | 2.974 | 20 | 24 | fits | 148,068 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 297,298 | 2.973 | 20 | 50 | fits | 148,068 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 435,658 | 4.357 | 20 | 50 | fits | 138,756 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 530,592 | 5.306 | 20 | 20 | fits | 95,000 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,044,475 | 10.445 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 366,534 | 3.665 | 20 | 20 | fits | 139,146 | 164 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 299,876 | 2.999 | 20 | 200 | fits | 147,554 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 438,406 | 4.384 | 20 | 200 | fits | 139,146 | 164 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 300,800 | 3.008 | 20 | 20 | fits | 147,554 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 439,110 | 4.391 | 20 | 20 | fits | 139,146 | 164 | 0.425 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 156,886 | 1.569 | 20 | 24 | fits | 144,254 | 161 | 0.352 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 303,450 | 3.034 | 20 | 24 | fits | 147,554 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 303,384 | 3.034 | 20 | 50 | fits | 147,554 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 442,134 | 4.421 | 20 | 50 | fits | 139,146 | 164 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 543,873 | 5.439 | 20 | 20 | fits | 92,917 | 31 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 972,992 | 9.730 | 20 | 20 | fits | 67,684 | 24 | 0.598 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 356,042 | 3.560 | 20 | 20 | fits | 138,857 | 163 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 289,973 | 2.900 | 20 | 200 | fits | 147,964 | 217 | 0.419 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 428,214 | 4.282 | 20 | 200 | fits | 138,857 | 163 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 290,897 | 2.909 | 20 | 20 | fits | 147,964 | 217 | 0.419 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 428,918 | 4.289 | 20 | 20 | fits | 138,857 | 163 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 146,573 | 1.466 | 20 | 24 | fits | 144,590 | 161 | 0.354 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 293,547 | 2.935 | 20 | 24 | fits | 147,964 | 217 | 0.419 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 293,481 | 2.935 | 20 | 50 | fits | 147,964 | 217 | 0.419 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 431,942 | 4.319 | 20 | 50 | fits | 138,857 | 163 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 526,819 | 5.268 | 20 | 20 | fits | 94,943 | 30 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 964,705 | 9.647 | 20 | 20 | fits | 67,885 | 24 | 0.607 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 369,352 | 3.694 | 20 | 20 | fits | 139,012 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 302,724 | 3.027 | 20 | 200 | fits | 148,644 | 222 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 441,120 | 4.411 | 20 | 200 | fits | 139,012 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 303,648 | 3.036 | 20 | 20 | fits | 148,644 | 222 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 441,824 | 4.418 | 20 | 20 | fits | 139,012 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 150,932 | 1.509 | 20 | 24 | fits | 144,691 | 162 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 306,298 | 3.063 | 20 | 24 | fits | 148,644 | 222 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 306,232 | 3.062 | 20 | 50 | fits | 148,644 | 222 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 444,848 | 4.448 | 20 | 50 | fits | 139,012 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 533,836 | 5.338 | 20 | 20 | fits | 89,054 | 24 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 961,934 | 9.619 | 20 | 20 | fits | 73,495 | 31 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 374,949 | 3.749 | 20 | 20 | fits | 138,874 | 164 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 299,510 | 2.995 | 20 | 200 | fits | 147,795 | 217 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 437,768 | 4.378 | 20 | 200 | fits | 138,874 | 164 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 300,434 | 3.004 | 20 | 20 | fits | 147,795 | 217 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 438,472 | 4.385 | 20 | 20 | fits | 138,874 | 164 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 156,279 | 1.563 | 20 | 24 | fits | 144,483 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 303,084 | 3.031 | 20 | 24 | fits | 147,795 | 217 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 303,018 | 3.030 | 20 | 50 | fits | 147,795 | 217 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 441,496 | 4.415 | 20 | 50 | fits | 138,874 | 164 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 546,753 | 5.468 | 20 | 20 | fits | 96,614 | 37 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,050,396 | 10.504 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 369,722 | 3.697 | 20 | 20 | fits | 142,463 | 170 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 291,011 | 2.910 | 20 | 200 | fits | 147,998 | 218 | 0.417 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 441,496 | 4.415 | 20 | 200 | fits | 142,463 | 170 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 291,935 | 2.919 | 20 | 20 | fits | 147,998 | 218 | 0.417 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 442,200 | 4.422 | 20 | 20 | fits | 142,463 | 170 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 147,577 | 1.476 | 20 | 24 | fits | 144,348 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 294,585 | 2.946 | 20 | 24 | fits | 147,998 | 218 | 0.417 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 294,519 | 2.945 | 20 | 50 | fits | 147,998 | 218 | 0.417 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 445,224 | 4.452 | 20 | 50 | fits | 142,463 | 170 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 534,336 | 5.343 | 20 | 20 | fits | 89,178 | 24 | 0.768 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 962,222 | 9.622 | 20 | 20 | fits | 73,403 | 30 | 0.655 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 363,593 | 3.636 | 20 | 20 | fits | 138,793 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 297,524 | 2.975 | 20 | 200 | fits | 147,691 | 217 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 435,701 | 4.357 | 20 | 200 | fits | 138,793 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 298,448 | 2.984 | 20 | 20 | fits | 147,691 | 217 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 436,405 | 4.364 | 20 | 20 | fits | 138,793 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 154,397 | 1.544 | 20 | 24 | fits | 144,700 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 301,098 | 3.011 | 20 | 24 | fits | 147,691 | 217 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 301,032 | 3.010 | 20 | 50 | fits | 147,691 | 217 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 439,429 | 4.394 | 20 | 50 | fits | 138,793 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 533,967 | 5.340 | 20 | 20 | fits | 94,604 | 31 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 971,416 | 9.714 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 369,429 | 3.694 | 20 | 20 | fits | 138,721 | 163 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 293,936 | 2.939 | 20 | 200 | fits | 147,836 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 432,041 | 4.320 | 20 | 200 | fits | 138,721 | 163 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 294,860 | 2.949 | 20 | 20 | fits | 147,836 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 432,745 | 4.327 | 20 | 20 | fits | 138,721 | 163 | 0.422 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 150,664 | 1.507 | 20 | 24 | fits | 144,644 | 161 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 297,510 | 2.975 | 20 | 24 | fits | 147,836 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 297,444 | 2.974 | 20 | 50 | fits | 147,836 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 435,769 | 4.358 | 20 | 50 | fits | 138,721 | 163 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 525,209 | 5.252 | 20 | 20 | fits | 89,506 | 24 | 0.763 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 969,843 | 9.698 | 20 | 20 | fits | 73,035 | 30 | 0.645 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 363,820 | 3.638 | 20 | 20 | fits | 142,195 | 169 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 294,755 | 2.948 | 20 | 200 | fits | 148,615 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 436,334 | 4.363 | 20 | 200 | fits | 142,195 | 169 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 295,679 | 2.957 | 20 | 20 | fits | 148,615 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 437,038 | 4.370 | 20 | 20 | fits | 142,195 | 169 | 0.441 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 143,190 | 1.432 | 20 | 24 | fits | 144,799 | 162 | 0.356 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 298,329 | 2.983 | 20 | 24 | fits | 148,615 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 298,263 | 2.983 | 20 | 50 | fits | 148,615 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 440,062 | 4.401 | 20 | 50 | fits | 142,195 | 169 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 534,433 | 5.344 | 20 | 20 | fits | 94,437 | 30 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,049,857 | 10.499 | 20 | 20 | fits | 72,862 | 31 | 0.678 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 379,525 | 3.795 | 20 | 20 | fits | 138,853 | 163 | 0.423 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 303,978 | 3.040 | 20 | 200 | fits | 149,202 | 222 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 442,215 | 4.422 | 20 | 200 | fits | 138,853 | 163 | 0.423 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 304,902 | 3.049 | 20 | 20 | fits | 149,202 | 222 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 442,919 | 4.429 | 20 | 20 | fits | 138,853 | 163 | 0.423 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 151,676 | 1.517 | 20 | 24 | fits | 144,581 | 162 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 307,552 | 3.076 | 20 | 24 | fits | 149,202 | 222 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 307,486 | 3.075 | 20 | 50 | fits | 149,202 | 222 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 445,943 | 4.459 | 20 | 50 | fits | 138,853 | 163 | 0.423 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 535,459 | 5.355 | 20 | 20 | fits | 89,582 | 24 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 963,511 | 9.635 | 20 | 20 | fits | 73,449 | 31 | 0.653 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 366,022 | 3.660 | 20 | 20 | fits | 138,948 | 164 | 0.420 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 299,907 | 2.999 | 20 | 200 | fits | 147,570 | 217 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 438,239 | 4.382 | 20 | 200 | fits | 138,948 | 164 | 0.420 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 300,831 | 3.008 | 20 | 20 | fits | 147,570 | 217 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 438,943 | 4.389 | 20 | 20 | fits | 138,948 | 164 | 0.420 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 156,901 | 1.569 | 20 | 24 | fits | 144,373 | 161 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 303,481 | 3.035 | 20 | 24 | fits | 147,570 | 217 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 303,415 | 3.034 | 20 | 50 | fits | 147,570 | 217 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 441,967 | 4.420 | 20 | 50 | fits | 138,948 | 164 | 0.420 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 547,586 | 5.476 | 20 | 20 | fits | 96,963 | 37 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 970,023 | 9.700 | 20 | 20 | fits | 67,417 | 24 | 0.591 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 21,414 | 0.214 | 20 | 20 | fits | 36,547 | 27 (35) | 0.800 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 6,878 | 0.069 | 20 | 20 | fits | 33,035 | 24 (14) | 0.811 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 15,710 | 0.157 | 20 | 20 | fits | 32,750 | 24 (14) | 0.824 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 25,103 | 0.251 | 20 | 20 | fits | 39,726 | 27 (35) | 0.802 |
| an event behind 15 others | `backlog.event.if0` | 165,456 | 1.655 | 20 | 200 | fits | 55,813 | 78 | 0.563 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 487,210 | 4.872 | 20 | 20 | fits | 72,488 | 90 | 0.304 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 455,423 | 4.554 | 20 | 200 | fits | 147,511 | 122 | 0.412 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 454,807 | 4.548 | 20 | 200 | fits | 147,511 | 122 | 0.412 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 451,101 | 4.511 | 20 | 20 | fits | 147,511 | 122 | 0.412 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 522,753 | 5.228 | 20 | 20 | fits | 72,488 | 90 | 0.304 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 152,063 | 1.521 | 20 | 24 | fits | 152,954 | 167 | 0.372 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 306,240 | 3.062 | 20 | 24 | fits | 99,354 | 26 | 0.708 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 453,685 | 4.537 | 20 | 50 | fits | 147,511 | 122 | 0.412 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 453,289 | 4.533 | 20 | 50 | fits | 147,511 | 122 | 0.412 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 525,711 | 5.257 | 20 | 20 | fits | 72,488 | 90 | 0.304 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 586,570 | 5.866 | 20 | 20 | fits | 26,720 | 41 | 0.191 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,617 | 0.076 | 20 | 20 | fits | 29,031 | 13 (29) | 0.786 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 9,393 | 0.094 | 20 | 20 | fits | 31,197 | 19 (35) | 0.778 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 28,220 | 0.282 | 20 | 20 | fits | 36,760 | 27 (12) | 0.798 |
| LINK_UP | `adp.link_up.if0` | 2,690 | 0.027 | 20 | 200 | fits | 30,690 | 43 (11) | 0.710 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,416 | 0.174 | 20 | 200 | fits | 24,384 | 23 (39) | 0.726 |
| LINK_DOWN | `adp.link_down.if0` | 2,308 | 0.023 | 20 | 200 | fits | 34,207 | 23 (9) | 0.745 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 11,194 | 0.112 | 20 | 24 | fits | 28,317 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 23,565 | 0.236 | 20 | 24 | fits | 32,367 | 20 | 0.711 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,221 | 0.142 | 20 | 24 | fits | 28,283 | 20 | 0.727 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,571 | 0.146 | 20 | 24 | fits | 28,665 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 20,185 | 0.202 | 20 | 24 | fits | 28,681 | 20 | 0.731 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 15,016 | 0.150 | 20 | 24 | fits | 29,206 | 20 | 0.722 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 19,835 | 0.198 | 20 | 24 | fits | 28,331 | 20 | 0.735 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 13,831 | 0.138 | 20 | 24 | fits | 27,683 | 20 | 0.737 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 20,094 | 0.201 | 20 | 24 | fits | 28,692 | 20 | 0.751 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 24,701 | 0.247 | 20 | 24 | fits | 33,484 | 21 | 0.656 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 13,832 | 0.138 | 20 | 24 | fits | 27,962 | 20 | 0.761 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 19,667 | 0.197 | 20 | 24 | fits | 28,242 | 20 | 0.770 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 13,765 | 0.138 | 20 | 24 | fits | 27,880 | 20 | 0.728 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 20,472 | 0.205 | 20 | 24 | fits | 29,253 | 20 | 0.740 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,831 | 0.188 | 20 | 24 | fits | 28,880 | 20 | 0.738 |
| get_configuration | `aecp.get_configuration.if0` | 12,292 | 0.123 | 20 | 24 | fits | 25,559 | 20 | 0.732 |
| entity_available | `aecp.entity_available.if0` | 17,887 | 0.179 | 20 | 24 | fits | 25,844 | 20 | 0.741 |
| get_name | `aecp.get_name.if0` | 14,340 | 0.143 | 20 | 24 | fits | 28,651 | 20 | 0.756 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 21,344 | 0.213 | 20 | 24 | fits | 30,267 | 27 | 0.739 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 15,709 | 0.157 | 20 | 24 | fits | 29,960 | 29 | 0.762 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 21,848 | 0.218 | 20 | 24 | fits | 26,614 | 20 | 0.767 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 17,641 | 0.176 | 20 | 24 | fits | 26,089 | 20 | 0.753 |
| set_name | `aecp.set_name.if0` | 25,660 | 0.257 | 20 | 24 | fits | 49,433 | 43 | 0.758 |
| lock_entity | `aecp.lock_entity.if0` | 23,544 | 0.235 | 20 | 24 | fits | 36,384 | 34 | 0.784 |
| unlock_entity | `aecp.unlock_entity.if0` | 18,031 | 0.180 | 20 | 24 | fits | 35,458 | 33 | 0.768 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
