### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

1 of 54 paths and 1 of 253 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.101 (0.327) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.076 (0.294) | fits | 0 adp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.310 (0.746) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.259 (0.689) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.276 (0.634) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.285 (0.590) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.356 (1.577) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.313) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-link) | 0.030 (0.337) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-link) | 0.150 (0.535) | fits | 0 events | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.198 (0.575) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.239 (0.630) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.161 (0.542) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.233 (0.617) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.182 (0.558) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.257 (0.683) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.196 (0.573) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.259 (0.642) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.185 (0.560) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.177 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.223 (0.605) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.268 (0.651) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.178 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.216 (0.599) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.224 (0.605) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.176 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.225 (0.607) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.212 (0.520) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.223 (0.604) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.190 (0.568) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.218 (0.601) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.160 (0.537) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.247 (0.722) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.252 (0.627) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.260 (0.603) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.771 (5.129) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-5.adp_available.if0` (backlog-adp@blank-5) | 4.300 (5.675) | fits | 7 adp | 18 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.747 (2.223) | fits | 15 events | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.062 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.635 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.952 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 2.039 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 8.374 | fits | 31 srp | 1 | 0 |
| an MRPDU its join timer owes, the longest | 0 | `save-starved.mrpdu.leaveall.if0` (save-starved) | 160.506 | MISS ceiling | 0 srp | 3 | 1 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.301 | fits | 0 acmp | 19 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged2-1.service.acmp.last.if0` (backlog-adp@program-aged2-1) | 5.589 | fits | 11 acmp | 19 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.345 | fits | 0 adp | 19 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-5.service.adp.last.if0` (backlog-adp@blank-5) | 4.735 | fits | 7 adp | 19 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-2.service.aecp.first.if0` (backlog-adp@blank-2) | 1.613 | fits | 0 aecp | 19 | 0 |
| AECP record released under the composed load, last | 0 | `backlog.service.aecp.last.if0` (backlog) | 4.328 | fits | 15 aecp | 19 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.327 | fits | 0 maap | 19 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-5.service.maap.last.if0` (backlog-adp@blank-5) | 4.772 | fits | 6 maap | 19 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged2-1.service.srp.first.if0` (backlog-adp@program-aged2-1) | 5.619 | fits | 0 srp | 19 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-5.service.srp.last.if0` (backlog-adp@blank-aged2-5) | 10.072 | fits | 31 srp | 19 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-2 | 0 | 10.691 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@blank-5 | 0 | 10.995 | 12 | 154,156 (1.542) | yes | - |
| backlog-adp@program-1 | 0 | 11.198 | 12 | 153,147 (1.531) | yes | - |
| backlog-adp@program-5 | 0 | 10.125 | 11 | 158,538 (1.585) | yes | - |
| backlog-adp@verify-1 | 0 | 10.562 | 9 | 155,705 (1.557) | yes | - |
| backlog-adp@verify-5 | 0 | 10.997 | 12 | 154,156 (1.542) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 11.068 | 12 | 153,189 (1.532) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.711 | 10 | 158,299 (1.583) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 10.631 | 10 | 158,889 (1.589) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.575 | 10 | 158,299 (1.583) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.747 | 11 | 156,578 (1.566) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 10.557 | 9 | 155,210 (1.552) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.706 | 10 | 153,102 (1.531) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.656 | 10 | 156,507 (1.565) | yes | - |
| backlog-adp@verify-aged2-1 | 1 | 10.391 | 9 | 155,705 (1.557) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.637 | 10 | 158,799 (1.588) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.882 | 12 | 156,578 (1.566) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.572 | 10 | 155,210 (1.552) | yes | - |
| backlog | 0 | 6.337 | 7 | 161,098 (1.611) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 161,098 CPU cycles (1.611 ms), backlog.
Over the windows that released their whole load only: 161,098 (1.611 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-starved | 58207 | 0 | 163,276 (1.633) | fits |
| backlog-adp@blank-2 | 537 | 0 | 156,507 (1.565) | fits |
| backlog-adp@blank-5 | 539 | 0 | 154,156 (1.542) | fits |
| backlog-adp@program-1 | 895 | 0 | 153,147 (1.531) | fits |
| backlog-adp@program-5 | 897 | 0 | 158,538 (1.585) | fits |
| backlog-adp@verify-1 | 1243 | 0 | 155,705 (1.557) | fits |
| backlog-adp@verify-5 | 1245 | 0 | 154,156 (1.542) | fits |
| backlog-adp@blank-aged2-1 | 787 | 0 | 153,189 (1.532) | fits |
| backlog-adp@blank-aged2-5 | 811 | 0 | 158,299 (1.583) | fits |
| backlog-adp@blank-aged1-1 | 735 | 0 | 158,889 (1.589) | fits |
| backlog-adp@blank-aged1-5 | 760 | 0 | 158,299 (1.583) | fits |
| backlog-adp@program-aged2-1 | 1138 | 0 | 156,578 (1.566) | fits |
| backlog-adp@program-aged2-5 | 1162 | 0 | 155,210 (1.552) | fits |
| backlog-adp@program-aged1-1 | 1087 | 0 | 153,102 (1.531) | fits |
| backlog-adp@program-aged1-5 | 1112 | 0 | 156,507 (1.565) | fits |
| backlog-adp@verify-aged2-1 | 1490 | 0 | 155,705 (1.557) | fits |
| backlog-adp@verify-aged2-5 | 1516 | 0 | 158,799 (1.588) | fits |
| backlog-adp@verify-aged1-1 | 1442 | 0 | 156,578 (1.566) | fits |
| backlog-adp@verify-aged1-5 | 1465 | 0 | 155,210 (1.552) | fits |
| acmp-noresp | 2022 | 0 | 45,817 (0.458) | fits |
| backlog | 286 | 0 | 161,098 (1.611) | fits |
| acmp-disc | 937 | 0 | 45,817 (0.458) | fits |
| adp-link | 89 | 0 | 43,415 (0.434) | fits |
| aecp | 112 | 0 | 46,437 (0.464) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | +9.196 ms, 76,766 (0.768 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.158 (20) | 10.842 |
| backlog-adp@blank-aged2-5 | 2 | none | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.072 (20) | 9.928 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.235 (20) | 10.765 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 9.181 (20) | 10.819 |
| backlog-adp@program-aged2-1 | 2 | none | +8.967 ms, 80,262 (0.803 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.930 (20) | 11.070 |
| backlog-adp@program-aged2-5 | 2 | +5.466 ms, 80,308 (0.803 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.915 (20) | 10.085 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.265 (20) | 10.735 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.218 (20) | 10.782 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.195 ms, 77,665 (0.777 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.157 (20) | 10.843 |
| backlog-adp@verify-aged2-5 | 2 | +5.561 ms, 77,833 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 9.662 (20) | 10.338 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.906 (20) | 11.094 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.165 (20) | 10.835 |

Least margin over the aged windows: 9.928 ms, `backlog-adp@blank-aged2-5.service.srp.last.if0` at 10.072 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-starved | 12448.173 | 12,470 | 382 | - | 33.739 | yes | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-starved | 698 | 81,594 (0.816) | 77,844 (0.778) |
| backlog-adp@blank-2 | 339 | 95,768 (0.958) | 76,093 (0.761) |
| backlog-adp@blank-5 | 339 | 94,727 (0.947) | 76,062 (0.761) |
| backlog-adp@program-1 | 448 | 100,633 (1.006) | 78,337 (0.783) |
| backlog-adp@program-5 | 449 | 100,633 (1.006) | 77,865 (0.779) |
| backlog-adp@verify-1 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-5 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@blank-aged2-1 | 337 | 79,331 (0.793) | 75,650 (0.756) |
| backlog-adp@blank-aged2-5 | 337 | 87,131 (0.871) | 75,872 (0.759) |
| backlog-adp@blank-aged1-1 | 337 | 95,954 (0.960) | 76,173 (0.762) |
| backlog-adp@blank-aged1-5 | 337 | 95,813 (0.958) | 76,226 (0.762) |
| backlog-adp@program-aged2-1 | 446 | 100,633 (1.006) | 77,960 (0.780) |
| backlog-adp@program-aged2-5 | 446 | 100,633 (1.006) | 78,011 (0.780) |
| backlog-adp@program-aged1-1 | 446 | 100,633 (1.006) | 78,339 (0.783) |
| backlog-adp@program-aged1-5 | 446 | 100,633 (1.006) | 78,388 (0.784) |
| backlog-adp@verify-aged2-1 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged2-5 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-1 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| backlog-adp@verify-aged1-5 | 555 | 104,368 (1.044) | 77,942 (0.779) |
| acmp-noresp | 615 | 108,440 (1.084) | 77,942 (0.779) |
| backlog | 265 | 26,258 (0.263) | 2,254 (0.023) |
| acmp-disc | 306 | 108,440 (1.084) | 75,550 (0.755) |
| adp-link | 79 | 26,196 (0.262) | 2,254 (0.023) |
| aecp | 80 | 26,196 (0.262) | 2,254 (0.023) |

Longest pass that carries a step: 108,440 CPU cycles (1.084 ms), acmp-noresp; longest step: 78,388 (0.784 ms), backlog-adp@program-aged1-5.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 263,536 | 2.635 | 20 | 200 | fits | 101,200 | 127 | 0.483 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 306,154 | 3.062 | 20 | 20 | fits | 83,719 | 56 | 0.610 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 295,152 | 2.952 | 20 | 24 | fits | 79,969 | 60 | 0.453 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 203,924 | 2.039 | 20 | 50 | fits | 101,200 | 127 | 0.483 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 837,427 | 8.374 | 20 | 20 | fits | 83,571 | 44 | 0.632 |
| an MRPDU its join timer owes, the longest | `save-starved.mrpdu.join.if0` | 50,646 | 0.506 | 20 | 20 | fits | 0 | - | 0.000 |
| an MRPDU its leaveall timer owes, the longest | `save-starved.mrpdu.leaveall.if0` | 16,050,646 | 160.506 | 20 | 20 | MISS ceiling | 0 | - | 0.000 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 181,841 | 1.818 | 20 | 20 | fits | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 411,164 | 4.112 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 307,357 | 3.074 | 20 | 200 | fits | 150,591 | 176 | 0.421 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 463,248 | 4.632 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 308,281 | 3.083 | 20 | 20 | fits | 150,591 | 176 | 0.421 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 546,267 | 5.463 | 20 | 20 | fits | 82,315 | 32 | 0.750 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 161,330 | 1.613 | 20 | 24 | fits | 148,236 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 310,931 | 3.109 | 20 | 24 | fits | 150,591 | 176 | 0.421 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 310,865 | 3.109 | 20 | 50 | fits | 150,591 | 176 | 0.421 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 466,976 | 4.670 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 549,225 | 5.492 | 20 | 20 | fits | 82,315 | 32 | 0.750 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 929,624 | 9.296 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 430,029 | 4.300 | 20 | 20 | fits | 154,156 | 200 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 319,944 | 3.199 | 20 | 200 | fits | 153,999 | 185 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 473,484 | 4.735 | 20 | 200 | fits | 154,156 | 200 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 320,868 | 3.209 | 20 | 20 | fits | 153,999 | 185 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 557,066 | 5.571 | 20 | 20 | fits | 82,878 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 160,757 | 1.608 | 20 | 24 | fits | 148,325 | 146 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 323,518 | 3.235 | 20 | 24 | fits | 153,999 | 185 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 323,452 | 3.235 | 20 | 50 | fits | 153,999 | 185 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 477,212 | 4.772 | 20 | 50 | fits | 154,156 | 200 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 560,024 | 5.600 | 20 | 20 | fits | 82,878 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 926,407 | 9.264 | 20 | 20 | fits | 32,581 | 13 | 0.820 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 409,936 | 4.099 | 20 | 20 | fits | 153,147 | 193 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 299,753 | 2.998 | 20 | 200 | fits | 150,065 | 193 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 462,643 | 4.626 | 20 | 200 | fits | 153,147 | 193 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 300,677 | 3.007 | 20 | 20 | fits | 150,065 | 193 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 545,575 | 5.456 | 20 | 20 | fits | 82,228 | 37 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 154,252 | 1.543 | 20 | 24 | fits | 148,257 | 145 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 303,327 | 3.033 | 20 | 24 | fits | 150,065 | 193 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 303,261 | 3.033 | 20 | 50 | fits | 150,065 | 193 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 466,371 | 4.664 | 20 | 50 | fits | 153,147 | 193 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 548,533 | 5.485 | 20 | 20 | fits | 82,228 | 37 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 921,223 | 9.212 | 20 | 20 | fits | 41,063 | 16 | 0.749 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 401,001 | 4.010 | 20 | 20 | fits | 158,538 | 195 | 0.404 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 305,338 | 3.053 | 20 | 200 | fits | 151,800 | 197 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 463,260 | 4.633 | 20 | 200 | fits | 158,538 | 195 | 0.404 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 306,262 | 3.063 | 20 | 20 | fits | 151,800 | 197 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 554,094 | 5.541 | 20 | 20 | fits | 90,130 | 35 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 148,350 | 1.484 | 20 | 24 | fits | 148,274 | 146 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 308,912 | 3.089 | 20 | 24 | fits | 151,800 | 197 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 308,846 | 3.088 | 20 | 50 | fits | 151,800 | 197 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 466,988 | 4.670 | 20 | 50 | fits | 158,538 | 195 | 0.404 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 557,052 | 5.571 | 20 | 20 | fits | 90,130 | 35 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 888,705 | 8.887 | 20 | 20 | fits | 83,795 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 379,527 | 3.795 | 20 | 20 | fits | 155,705 | 205 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 295,224 | 2.952 | 20 | 200 | fits | 152,227 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 450,313 | 4.503 | 20 | 200 | fits | 155,705 | 205 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 296,148 | 2.961 | 20 | 20 | fits | 152,227 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 533,042 | 5.330 | 20 | 20 | fits | 82,025 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 147,561 | 1.476 | 20 | 24 | fits | 148,244 | 145 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 298,798 | 2.988 | 20 | 24 | fits | 152,227 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 298,732 | 2.987 | 20 | 50 | fits | 152,227 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 454,041 | 4.540 | 20 | 50 | fits | 155,705 | 205 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 536,000 | 5.360 | 20 | 20 | fits | 82,025 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 915,948 | 9.159 | 20 | 20 | fits | 38,197 | 18 | 0.839 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 429,319 | 4.293 | 20 | 20 | fits | 154,156 | 200 | 0.441 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 319,234 | 3.192 | 20 | 200 | fits | 154,088 | 185 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 472,774 | 4.728 | 20 | 200 | fits | 154,156 | 200 | 0.441 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 320,158 | 3.202 | 20 | 20 | fits | 154,088 | 185 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 556,273 | 5.563 | 20 | 20 | fits | 82,795 | 37 | 0.722 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 159,958 | 1.600 | 20 | 24 | fits | 148,389 | 146 | 0.369 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 322,808 | 3.228 | 20 | 24 | fits | 154,088 | 185 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 322,742 | 3.227 | 20 | 50 | fits | 154,088 | 185 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 476,502 | 4.765 | 20 | 50 | fits | 154,156 | 200 | 0.441 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 559,231 | 5.592 | 20 | 20 | fits | 82,795 | 37 | 0.722 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 925,614 | 9.256 | 20 | 20 | fits | 32,581 | 13 | 0.820 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 404,093 | 4.041 | 20 | 20 | fits | 153,189 | 193 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 294,057 | 2.941 | 20 | 200 | fits | 150,191 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 456,842 | 4.568 | 20 | 200 | fits | 153,189 | 193 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 294,981 | 2.950 | 20 | 20 | fits | 150,191 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 540,553 | 5.406 | 20 | 20 | fits | 83,007 | 37 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 148,430 | 1.484 | 20 | 24 | fits | 147,121 | 142 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 297,631 | 2.976 | 20 | 24 | fits | 150,191 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 297,565 | 2.976 | 20 | 50 | fits | 150,191 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 460,570 | 4.606 | 20 | 50 | fits | 153,189 | 193 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 543,511 | 5.435 | 20 | 20 | fits | 83,007 | 37 | 0.724 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 915,816 | 9.158 | 20 | 20 | fits | 38,536 | 18 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 401,611 | 4.016 | 20 | 20 | fits | 158,299 | 196 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 305,929 | 3.059 | 20 | 200 | fits | 149,957 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 463,612 | 4.636 | 20 | 200 | fits | 158,299 | 196 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 306,853 | 3.069 | 20 | 20 | fits | 149,957 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 553,744 | 5.537 | 20 | 20 | fits | 89,428 | 40 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 160,536 | 1.605 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 309,503 | 3.095 | 20 | 24 | fits | 149,957 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 309,437 | 3.094 | 20 | 50 | fits | 149,957 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 467,340 | 4.673 | 20 | 50 | fits | 158,299 | 196 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 556,702 | 5.567 | 20 | 20 | fits | 89,428 | 40 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,007,198 | 10.072 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 396,274 | 3.963 | 20 | 20 | fits | 158,889 | 196 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 300,596 | 3.006 | 20 | 200 | fits | 150,056 | 192 | 0.408 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 458,869 | 4.589 | 20 | 200 | fits | 158,889 | 196 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 301,520 | 3.015 | 20 | 20 | fits | 150,056 | 192 | 0.408 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 556,421 | 5.564 | 20 | 20 | fits | 86,705 | 38 | 0.764 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 155,104 | 1.551 | 20 | 24 | fits | 147,168 | 142 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 304,170 | 3.042 | 20 | 24 | fits | 150,056 | 192 | 0.408 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 304,104 | 3.041 | 20 | 50 | fits | 150,056 | 192 | 0.408 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 462,597 | 4.626 | 20 | 50 | fits | 158,889 | 196 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 559,379 | 5.594 | 20 | 20 | fits | 86,705 | 38 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 923,452 | 9.235 | 20 | 20 | fits | 32,887 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 388,368 | 3.884 | 20 | 20 | fits | 158,299 | 196 | 0.400 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 292,686 | 2.927 | 20 | 200 | fits | 149,957 | 192 | 0.407 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 450,369 | 4.504 | 20 | 200 | fits | 158,299 | 196 | 0.400 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 293,610 | 2.936 | 20 | 20 | fits | 149,957 | 192 | 0.407 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 540,451 | 5.405 | 20 | 20 | fits | 89,378 | 39 | 0.751 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 147,293 | 1.473 | 20 | 24 | fits | 147,121 | 142 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 296,260 | 2.963 | 20 | 24 | fits | 149,957 | 192 | 0.407 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 296,194 | 2.962 | 20 | 50 | fits | 149,957 | 192 | 0.407 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 454,097 | 4.541 | 20 | 50 | fits | 158,299 | 196 | 0.400 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 543,409 | 5.434 | 20 | 20 | fits | 89,378 | 39 | 0.751 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 918,080 | 9.181 | 20 | 20 | fits | 32,382 | 12 | 0.826 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 416,084 | 4.161 | 20 | 20 | fits | 156,578 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 312,212 | 3.122 | 20 | 200 | fits | 152,413 | 181 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 468,174 | 4.682 | 20 | 200 | fits | 156,578 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 313,136 | 3.131 | 20 | 20 | fits | 152,413 | 181 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 558,912 | 5.589 | 20 | 20 | fits | 90,034 | 35 | 0.720 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 154,609 | 1.546 | 20 | 24 | fits | 147,170 | 143 | 0.361 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 315,786 | 3.158 | 20 | 24 | fits | 152,413 | 181 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 315,720 | 3.157 | 20 | 50 | fits | 152,413 | 181 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 471,902 | 4.719 | 20 | 50 | fits | 156,578 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 561,870 | 5.619 | 20 | 20 | fits | 90,034 | 35 | 0.720 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 892,986 | 8.930 | 20 | 20 | fits | 81,142 | 38 | 0.623 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 395,256 | 3.953 | 20 | 20 | fits | 155,210 | 205 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 293,914 | 2.939 | 20 | 200 | fits | 153,265 | 185 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 448,508 | 4.485 | 20 | 200 | fits | 155,210 | 205 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 294,838 | 2.948 | 20 | 20 | fits | 153,265 | 185 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 541,983 | 5.420 | 20 | 20 | fits | 82,648 | 42 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 145,213 | 1.452 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 297,488 | 2.975 | 20 | 24 | fits | 153,265 | 185 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 297,422 | 2.974 | 20 | 50 | fits | 153,265 | 185 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 452,236 | 4.522 | 20 | 50 | fits | 155,210 | 205 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 544,941 | 5.449 | 20 | 20 | fits | 82,648 | 42 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 991,519 | 9.915 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 415,530 | 4.155 | 20 | 20 | fits | 153,102 | 193 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 305,389 | 3.054 | 20 | 200 | fits | 150,188 | 193 | 0.410 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 468,192 | 4.682 | 20 | 200 | fits | 153,102 | 193 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 306,313 | 3.063 | 20 | 20 | fits | 150,188 | 193 | 0.410 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 551,202 | 5.512 | 20 | 20 | fits | 82,306 | 37 | 0.721 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 159,765 | 1.598 | 20 | 24 | fits | 147,000 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 308,963 | 3.090 | 20 | 24 | fits | 150,188 | 193 | 0.410 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 308,897 | 3.089 | 20 | 50 | fits | 150,188 | 193 | 0.410 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 471,920 | 4.719 | 20 | 50 | fits | 153,102 | 193 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 554,160 | 5.542 | 20 | 20 | fits | 82,306 | 37 | 0.721 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 926,465 | 9.265 | 20 | 20 | fits | 38,536 | 18 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 403,449 | 4.034 | 20 | 20 | fits | 156,507 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 299,642 | 2.996 | 20 | 200 | fits | 150,685 | 176 | 0.422 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 455,533 | 4.555 | 20 | 200 | fits | 156,507 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 300,566 | 3.006 | 20 | 20 | fits | 150,685 | 176 | 0.422 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 544,976 | 5.450 | 20 | 20 | fits | 88,739 | 40 | 0.747 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 153,521 | 1.535 | 20 | 24 | fits | 147,047 | 142 | 0.359 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 303,216 | 3.032 | 20 | 24 | fits | 150,685 | 176 | 0.422 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 303,150 | 3.031 | 20 | 50 | fits | 150,685 | 176 | 0.422 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 459,261 | 4.593 | 20 | 50 | fits | 156,507 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 547,934 | 5.479 | 20 | 20 | fits | 88,739 | 40 | 0.747 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 921,776 | 9.218 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 378,403 | 3.784 | 20 | 20 | fits | 155,705 | 205 | 0.409 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 294,100 | 2.941 | 20 | 200 | fits | 153,428 | 185 | 0.418 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 449,189 | 4.492 | 20 | 200 | fits | 155,705 | 205 | 0.409 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 295,024 | 2.950 | 20 | 20 | fits | 153,428 | 185 | 0.418 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 531,918 | 5.319 | 20 | 20 | fits | 82,025 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 145,236 | 1.452 | 20 | 24 | fits | 147,023 | 142 | 0.358 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 297,674 | 2.977 | 20 | 24 | fits | 153,428 | 185 | 0.418 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 297,608 | 2.976 | 20 | 50 | fits | 153,428 | 185 | 0.418 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 452,917 | 4.529 | 20 | 50 | fits | 155,705 | 205 | 0.409 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 534,876 | 5.349 | 20 | 20 | fits | 82,025 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 915,748 | 9.157 | 20 | 20 | fits | 38,431 | 18 | 0.842 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 390,526 | 3.905 | 20 | 20 | fits | 158,799 | 211 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 303,401 | 3.034 | 20 | 200 | fits | 153,895 | 185 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 461,584 | 4.616 | 20 | 200 | fits | 158,799 | 211 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 304,325 | 3.043 | 20 | 20 | fits | 153,895 | 185 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 551,427 | 5.514 | 20 | 20 | fits | 89,139 | 39 | 0.748 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 144,316 | 1.443 | 20 | 24 | fits | 147,235 | 143 | 0.360 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 306,975 | 3.070 | 20 | 24 | fits | 153,895 | 185 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 306,909 | 3.069 | 20 | 50 | fits | 153,895 | 185 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 465,312 | 4.653 | 20 | 50 | fits | 158,799 | 211 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 554,385 | 5.544 | 20 | 20 | fits | 89,139 | 39 | 0.748 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 966,159 | 9.662 | 20 | 20 | fits | 83,885 | 37 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 419,051 | 4.191 | 20 | 20 | fits | 156,578 | 209 | 0.392 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 315,179 | 3.152 | 20 | 200 | fits | 152,413 | 181 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 471,141 | 4.711 | 20 | 200 | fits | 156,578 | 209 | 0.392 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 316,103 | 3.161 | 20 | 20 | fits | 152,413 | 181 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 553,915 | 5.539 | 20 | 20 | fits | 82,070 | 31 | 0.749 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 157,520 | 1.575 | 20 | 24 | fits | 147,212 | 143 | 0.362 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 318,753 | 3.188 | 20 | 24 | fits | 152,413 | 181 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 318,687 | 3.187 | 20 | 50 | fits | 152,413 | 181 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 474,869 | 4.749 | 20 | 50 | fits | 156,578 | 209 | 0.392 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 556,873 | 5.569 | 20 | 20 | fits | 82,070 | 31 | 0.749 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 890,642 | 8.906 | 20 | 20 | fits | 83,795 | 36 | 0.534 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 400,033 | 4.000 | 20 | 20 | fits | 155,210 | 205 | 0.402 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 298,691 | 2.987 | 20 | 200 | fits | 152,280 | 180 | 0.420 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 453,285 | 4.533 | 20 | 200 | fits | 155,210 | 205 | 0.402 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 299,615 | 2.996 | 20 | 20 | fits | 152,280 | 180 | 0.420 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 547,212 | 5.472 | 20 | 20 | fits | 83,100 | 42 | 0.770 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 150,975 | 1.510 | 20 | 24 | fits | 146,958 | 142 | 0.357 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 302,265 | 3.023 | 20 | 24 | fits | 152,280 | 180 | 0.420 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 302,199 | 3.022 | 20 | 50 | fits | 152,280 | 180 | 0.420 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 457,013 | 4.570 | 20 | 50 | fits | 155,210 | 205 | 0.402 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 550,170 | 5.502 | 20 | 20 | fits | 83,100 | 42 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 916,470 | 9.165 | 20 | 20 | fits | 32,491 | 12 | 0.824 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 27,608 | 0.276 | 20 | 20 | fits | 38,715 | 27 (35) | 0.808 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 28,549 | 0.285 | 20 | 20 | fits | 34,177 | 23 (14) | 0.835 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 35,618 | 0.356 | 20 | 20 | fits | 35,492 | 25 (14) | 0.827 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 30,981 | 0.310 | 20 | 20 | fits | 37,493 | 21 (35) | 0.824 |
| an event behind 15 others | `backlog.event.if0` | 174,686 | 1.747 | 20 | 200 | fits | 61,181 | 78 | 0.558 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 477,113 | 4.771 | 20 | 20 | fits | 78,201 | 87 | 0.362 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 434,458 | 4.345 | 20 | 200 | fits | 149,286 | 125 | 0.447 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 433,842 | 4.338 | 20 | 200 | fits | 149,286 | 125 | 0.447 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 430,136 | 4.301 | 20 | 20 | fits | 149,286 | 125 | 0.447 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 507,501 | 5.075 | 20 | 20 | fits | 78,201 | 87 | 0.362 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 160,207 | 1.602 | 20 | 24 | fits | 161,098 | 158 | 0.363 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 432,786 | 4.328 | 20 | 24 | fits | 149,286 | 125 | 0.447 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 432,720 | 4.327 | 20 | 50 | fits | 149,286 | 125 | 0.447 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 432,324 | 4.323 | 20 | 50 | fits | 149,286 | 125 | 0.447 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 510,459 | 5.105 | 20 | 20 | fits | 78,201 | 87 | 0.362 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 572,241 | 5.722 | 20 | 20 | fits | 29,047 | 53 | 0.122 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,577 | 0.076 | 20 | 20 | fits | 29,358 | 14 (29) | 0.775 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,147 | 0.101 | 20 | 20 | fits | 32,713 | 19 (35) | 0.784 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 25,905 | 0.259 | 20 | 20 | fits | 36,384 | 21 (12) | 0.819 |
| LINK_UP | `adp.link_up.if0` | 2,986 | 0.030 | 20 | 200 | fits | 33,705 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 15,035 | 0.150 | 20 | 200 | fits | 26,764 | 23 (39) | 0.725 |
| LINK_DOWN | `adp.link_down.if0` | 2,363 | 0.024 | 20 | 200 | fits | 31,260 | 23 (9) | 0.784 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,988 | 0.160 | 20 | 24 | fits | 30,565 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 25,932 | 0.259 | 20 | 24 | fits | 34,280 | 20 | 0.697 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,489 | 0.185 | 20 | 24 | fits | 30,344 | 20 | 0.721 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 22,374 | 0.224 | 20 | 24 | fits | 30,455 | 20 | 0.718 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 22,253 | 0.223 | 20 | 24 | fits | 30,385 | 20 | 0.716 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 18,963 | 0.190 | 20 | 24 | fits | 31,145 | 20 | 0.720 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 21,776 | 0.218 | 20 | 24 | fits | 30,112 | 20 | 0.724 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 17,668 | 0.177 | 20 | 24 | fits | 29,480 | 20 | 0.727 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 22,321 | 0.223 | 20 | 24 | fits | 30,531 | 20 | 0.744 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 26,820 | 0.268 | 20 | 24 | fits | 35,218 | 21 | 0.647 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 17,828 | 0.178 | 20 | 24 | fits | 29,588 | 20 | 0.756 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 21,631 | 0.216 | 20 | 24 | fits | 29,727 | 20 | 0.761 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 17,649 | 0.176 | 20 | 24 | fits | 29,630 | 20 | 0.718 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 22,489 | 0.225 | 20 | 24 | fits | 30,773 | 20 | 0.731 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 21,223 | 0.212 | 20 | 24 | fits | 30,338 | 20 | 0.729 |
| get_configuration | `aecp.get_configuration.if0` | 16,140 | 0.161 | 20 | 24 | fits | 27,448 | 20 | 0.730 |
| entity_available | `aecp.entity_available.if0` | 19,836 | 0.198 | 20 | 24 | fits | 27,493 | 20 | 0.725 |
| get_name | `aecp.get_name.if0` | 18,235 | 0.182 | 20 | 24 | fits | 30,090 | 20 | 0.739 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 23,328 | 0.233 | 20 | 24 | fits | 31,473 | 27 | 0.726 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 23,904 | 0.239 | 20 | 24 | fits | 37,048 | 35 | 0.760 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 25,236 | 0.252 | 20 | 24 | fits | 28,447 | 20 | 0.760 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 19,593 | 0.196 | 20 | 24 | fits | 27,190 | 20 | 0.725 |
| set_name | `aecp.set_name.if0` | 24,692 | 0.247 | 20 | 24 | fits | 46,437 | 43 | 0.749 |
| lock_entity | `aecp.lock_entity.if0` | 25,736 | 0.257 | 20 | 24 | fits | 38,351 | 34 | 0.771 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,014 | 0.260 | 20 | 24 | fits | 38,573 | 33 | 0.778 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
