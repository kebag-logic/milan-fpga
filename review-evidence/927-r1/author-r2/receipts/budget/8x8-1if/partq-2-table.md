### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 45 paths and 0 of 156 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.100 (0.330) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.072 (0.292) | fits | 0 adp | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.221 (0.655) | fits | 0 events | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.055 (0.208) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.030 (0.338) | fits | 0 events | 2 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.091 (0.291) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.206 (0.598) | fits | 0 events | 2 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.254 (0.636) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.197 (0.605) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.213 (0.590) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.247 (0.633) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.277 (0.666) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.276 (0.740) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.251 (0.636) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.315 (0.703) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.241 (0.627) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.264 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.237 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.322 (0.711) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.231 (0.617) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.273 (0.665) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.236 (0.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.263 (0.519) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.240 (0.634) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.276 (0.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.276 (0.664) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.245 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.272 (0.660) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.214 (0.597) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.347 (0.832) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.215 (0.604) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.329 (0.756) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.806 (5.098) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged1-4.adp_available.if0` (backlog-adp@blank-aged1-4) | 4.121 (4.645) | fits | 7 adp | 10 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.647 (2.126) | fits | 15 events | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.263 | fits | 0 acmp | 11 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@program-aged1-0.service.acmp.last.if0` (backlog-adp@program-aged1-0) | 5.516 | fits | 11 acmp | 11 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.307 | fits | 0 adp | 11 | 0 |
| ADP record released under the composed load, last | 0 | `backlog.service.adp.last.if0` (backlog) | 5.090 | fits | 7 adp | 11 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-0.service.aecp.first.if0` (backlog-adp@blank-aged1-0) | 2.960 | fits | 0 aecp | 11 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-0.service.aecp.last.if0` (backlog-adp@blank-aged1-0) | 4.521 | fits | 15 aecp | 11 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.289 | fits | 0 maap | 11 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 5.075 | fits | 6 maap | 11 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@program-aged1-0.service.srp.first.if0` (backlog-adp@program-aged1-0) | 5.546 | fits | 0 srp | 11 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-4.service.srp.last.if0` (backlog-adp@program-aged2-4) | 10.087 | fits | 31 srp | 11 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-aged1-0 | 0 | 11.815 | 10 | 157,100 (1.571) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 11.324 | 11 | 154,523 (1.545) | yes | - |
| backlog-adp@program-aged2-0 | 0 | 11.475 | 13 | 155,183 (1.552) | yes | - |
| backlog-adp@program-aged2-4 | 0 | 10.734 | 10 | 150,855 (1.509) | yes | - |
| backlog-adp@program-aged1-0 | 1 | 10.866 | 9 | 158,245 (1.582) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 10.695 | 9 | 151,961 (1.520) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 11.914 | 12 | 152,207 (1.522) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 10.708 | 10 | 151,635 (1.516) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 12.189 | 13 | 155,183 (1.552) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 10.695 | 10 | 150,909 (1.509) | yes | - |
| backlog | 0 | 6.618 | 8 | 154,817 (1.548) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog-adp, backlog-adp-refill, backlog-owed not run): 154,817 CPU cycles (1.548 ms), backlog.
Over the windows that released their whole load only: 154,817 (1.548 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-aged1-0 | 746 | 0 | 157,100 (1.571) | fits |
| backlog-adp@blank-aged1-4 | 772 | 0 | 154,523 (1.545) | fits |
| backlog-adp@program-aged2-0 | 1178 | 0 | 155,183 (1.552) | fits |
| backlog-adp@program-aged2-4 | 1200 | 0 | 150,855 (1.509) | fits |
| backlog-adp@program-aged1-0 | 1125 | 0 | 158,245 (1.582) | fits |
| backlog-adp@program-aged1-4 | 1150 | 0 | 151,961 (1.520) | fits |
| backlog-adp@verify-aged2-0 | 1557 | 0 | 152,207 (1.522) | fits |
| backlog-adp@verify-aged2-4 | 1580 | 0 | 151,635 (1.516) | fits |
| backlog-adp@verify-aged1-0 | 1508 | 0 | 155,183 (1.552) | fits |
| backlog-adp@verify-aged1-4 | 1530 | 0 | 150,909 (1.509) | fits |
| adp-advertise | 598 | 0 | 34,491 (0.345) | fits |
| backlog | 287 | 0 | 154,817 (1.548) | fits |
| acmp-disc | 876 | 0 | 46,812 (0.468) | fits |
| adp-discover | 88 | 0 | 33,791 (0.338) | fits |
| aecp | 113 | 0 | 47,330 (0.473) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 9.229 (20) | 10.771 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 9.226 (20) | 10.774 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 9.210 (20) | 10.790 |
| backlog-adp@program-aged2-4 | 2 | +5.324 ms, 80,758 (0.808 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 10.087 (20) | 9.913 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.938 (20) | 11.062 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 9.242 (20) | 10.758 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 9.211 (20) | 10.789 |
| backlog-adp@verify-aged2-4 | 2 | +5.487 ms, 77,679 (0.777 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 10.055 (20) | 9.945 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 9.246 (20) | 10.754 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 9.280 (20) | 10.720 |

Least margin over the aged windows: 9.913 ms, `backlog-adp@program-aged2-4.service.srp.last.if0` at 10.087 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-aged1-0 | 338 | 96,230 (0.962) | 76,252 (0.763) |
| backlog-adp@blank-aged1-4 | 337 | 96,820 (0.968) | 76,252 (0.763) |
| backlog-adp@program-aged2-0 | 447 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@program-aged2-4 | 446 | 100,997 (1.010) | 78,484 (0.785) |
| backlog-adp@program-aged1-0 | 447 | 100,997 (1.010) | 78,774 (0.788) |
| backlog-adp@program-aged1-4 | 446 | 100,997 (1.010) | 78,776 (0.788) |
| backlog-adp@verify-aged2-0 | 556 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged2-4 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-0 | 556 | 104,873 (1.049) | 78,338 (0.783) |
| backlog-adp@verify-aged1-4 | 555 | 104,873 (1.049) | 78,338 (0.783) |
| adp-advertise | 577 | 26,414 (0.264) | 2,374 (0.024) |
| backlog | 265 | 26,388 (0.264) | 2,374 (0.024) |
| acmp-disc | 306 | 108,527 (1.085) | 75,606 (0.756) |
| adp-discover | 79 | 26,162 (0.262) | 2,374 (0.024) |
| aecp | 80 | 26,162 (0.262) | 2,374 (0.024) |

Longest pass that carries a step: 108,527 CPU cycles (1.085 ms), acmp-disc; longest step: 78,776 (0.788 ms), backlog-adp@program-aged2-0.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 385,978 | 3.860 | 20 | 20 | fits | 157,100 | 151 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 142,845 | 1.428 | 20 | 200 | fits | 151,824 | 234 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 447,918 | 4.479 | 20 | 200 | fits | 157,100 | 151 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 143,769 | 1.438 | 20 | 20 | fits | 151,824 | 234 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 532,276 | 5.323 | 20 | 20 | fits | 83,654 | 37 | 0.730 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 295,998 | 2.960 | 20 | 24 | fits | 148,589 | 142 | 0.376 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 452,108 | 4.521 | 20 | 24 | fits | 157,100 | 151 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 146,353 | 1.464 | 20 | 50 | fits | 151,824 | 234 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 145,957 | 1.460 | 20 | 50 | fits | 151,824 | 234 | 0.411 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 535,234 | 5.352 | 20 | 20 | fits | 83,654 | 37 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 922,915 | 9.229 | 20 | 20 | fits | 41,615 | 16 | 0.760 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 412,140 | 4.121 | 20 | 20 | fits | 154,523 | 224 | 0.443 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 291,444 | 2.914 | 20 | 200 | fits | 149,592 | 195 | 0.429 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 455,580 | 4.556 | 20 | 200 | fits | 154,523 | 224 | 0.443 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 292,368 | 2.924 | 20 | 20 | fits | 149,592 | 195 | 0.429 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 539,128 | 5.391 | 20 | 20 | fits | 82,844 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 146,416 | 1.464 | 20 | 24 | fits | 150,181 | 111 | 0.374 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 295,018 | 2.950 | 20 | 24 | fits | 149,592 | 195 | 0.429 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 294,952 | 2.950 | 20 | 50 | fits | 149,592 | 195 | 0.429 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 459,308 | 4.593 | 20 | 50 | fits | 154,523 | 224 | 0.443 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 542,086 | 5.421 | 20 | 20 | fits | 82,844 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 922,562 | 9.226 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 408,292 | 4.083 | 20 | 20 | fits | 155,183 | 192 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 297,264 | 2.973 | 20 | 200 | fits | 150,966 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 462,137 | 4.621 | 20 | 200 | fits | 155,183 | 192 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 298,188 | 2.982 | 20 | 20 | fits | 150,966 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 546,208 | 5.462 | 20 | 20 | fits | 83,367 | 37 | 0.731 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 150,862 | 1.509 | 20 | 24 | fits | 148,029 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 300,838 | 3.008 | 20 | 24 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 300,772 | 3.008 | 20 | 50 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 465,865 | 4.659 | 20 | 50 | fits | 155,183 | 192 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 549,166 | 5.492 | 20 | 20 | fits | 83,367 | 37 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 921,023 | 9.210 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 391,688 | 3.917 | 20 | 20 | fits | 150,372 | 186 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 294,761 | 2.948 | 20 | 200 | fits | 150,855 | 192 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 444,517 | 4.445 | 20 | 200 | fits | 150,372 | 186 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 295,685 | 2.957 | 20 | 20 | fits | 150,855 | 192 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 527,697 | 5.277 | 20 | 20 | fits | 82,476 | 41 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 148,470 | 1.485 | 20 | 24 | fits | 148,006 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 298,335 | 2.983 | 20 | 24 | fits | 150,855 | 192 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 298,269 | 2.983 | 20 | 50 | fits | 150,855 | 192 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 448,245 | 4.482 | 20 | 50 | fits | 150,372 | 186 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 530,655 | 5.307 | 20 | 20 | fits | 82,476 | 41 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 1,008,662 | 10.087 | 20 | 20 | fits | 50,391 | 20 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 381,358 | 3.814 | 20 | 20 | fits | 158,245 | 206 | 0.432 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 296,074 | 2.961 | 20 | 200 | fits | 154,500 | 185 | 0.424 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 453,703 | 4.537 | 20 | 200 | fits | 158,245 | 206 | 0.432 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 296,998 | 2.970 | 20 | 20 | fits | 154,500 | 185 | 0.424 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 551,619 | 5.516 | 20 | 20 | fits | 86,673 | 38 | 0.766 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 146,138 | 1.461 | 20 | 24 | fits | 148,006 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 299,648 | 2.996 | 20 | 24 | fits | 154,500 | 185 | 0.424 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 299,582 | 2.996 | 20 | 50 | fits | 154,500 | 185 | 0.424 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 457,431 | 4.574 | 20 | 50 | fits | 158,245 | 206 | 0.432 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 554,577 | 5.546 | 20 | 20 | fits | 86,673 | 38 | 0.766 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 893,808 | 8.938 | 20 | 20 | fits | 85,126 | 36 | 0.566 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 388,826 | 3.888 | 20 | 20 | fits | 150,684 | 185 | 0.431 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 291,926 | 2.919 | 20 | 200 | fits | 151,961 | 197 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 441,994 | 4.420 | 20 | 200 | fits | 150,684 | 185 | 0.431 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 292,850 | 2.929 | 20 | 20 | fits | 151,961 | 197 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 525,185 | 5.252 | 20 | 20 | fits | 82,487 | 41 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 144,529 | 1.445 | 20 | 24 | fits | 148,096 | 142 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 295,500 | 2.955 | 20 | 24 | fits | 151,961 | 197 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 295,434 | 2.954 | 20 | 50 | fits | 151,961 | 197 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 445,722 | 4.457 | 20 | 50 | fits | 150,684 | 185 | 0.431 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 528,143 | 5.281 | 20 | 20 | fits | 82,487 | 41 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 924,162 | 9.242 | 20 | 20 | fits | 50,722 | 20 | 0.716 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 409,249 | 4.092 | 20 | 20 | fits | 150,400 | 186 | 0.426 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 312,335 | 3.123 | 20 | 200 | fits | 152,207 | 197 | 0.416 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 462,119 | 4.621 | 20 | 200 | fits | 150,400 | 186 | 0.426 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 313,259 | 3.133 | 20 | 20 | fits | 152,207 | 197 | 0.416 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 546,331 | 5.463 | 20 | 20 | fits | 83,508 | 37 | 0.728 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 154,872 | 1.549 | 20 | 24 | fits | 148,080 | 143 | 0.368 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 315,909 | 3.159 | 20 | 24 | fits | 152,207 | 197 | 0.416 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 315,843 | 3.158 | 20 | 50 | fits | 152,207 | 197 | 0.416 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 465,847 | 4.658 | 20 | 50 | fits | 150,400 | 186 | 0.426 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 549,289 | 5.493 | 20 | 20 | fits | 83,508 | 37 | 0.728 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 921,146 | 9.211 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 403,699 | 4.037 | 20 | 20 | fits | 149,556 | 202 | 0.422 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 298,361 | 2.984 | 20 | 200 | fits | 151,635 | 176 | 0.428 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 447,301 | 4.473 | 20 | 200 | fits | 149,556 | 202 | 0.422 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 299,285 | 2.993 | 20 | 20 | fits | 151,635 | 176 | 0.428 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 544,079 | 5.441 | 20 | 20 | fits | 85,862 | 48 | 0.761 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 151,290 | 1.513 | 20 | 24 | fits | 148,112 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 301,935 | 3.019 | 20 | 24 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 301,869 | 3.019 | 20 | 50 | fits | 151,635 | 176 | 0.428 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 451,029 | 4.510 | 20 | 50 | fits | 149,556 | 202 | 0.422 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 547,037 | 5.470 | 20 | 20 | fits | 85,862 | 48 | 0.761 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 1,005,544 | 10.055 | 20 | 20 | fits | 41,674 | 16 | 0.761 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 411,229 | 4.112 | 20 | 20 | fits | 155,183 | 192 | 0.460 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 300,145 | 3.001 | 20 | 200 | fits | 150,966 | 193 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 465,074 | 4.651 | 20 | 200 | fits | 155,183 | 192 | 0.460 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 301,069 | 3.011 | 20 | 20 | fits | 150,966 | 193 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 549,753 | 5.498 | 20 | 20 | fits | 83,975 | 37 | 0.733 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 153,743 | 1.537 | 20 | 24 | fits | 147,963 | 142 | 0.366 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 303,719 | 3.037 | 20 | 24 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 303,653 | 3.037 | 20 | 50 | fits | 150,966 | 193 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 468,802 | 4.688 | 20 | 50 | fits | 155,183 | 192 | 0.460 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 552,711 | 5.527 | 20 | 20 | fits | 83,975 | 37 | 0.733 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 924,568 | 9.246 | 20 | 20 | fits | 32,958 | 12 | 0.832 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 392,743 | 3.927 | 20 | 20 | fits | 150,372 | 186 | 0.425 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 295,816 | 2.958 | 20 | 200 | fits | 150,909 | 192 | 0.414 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 445,572 | 4.456 | 20 | 200 | fits | 150,372 | 186 | 0.425 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 296,740 | 2.967 | 20 | 20 | fits | 150,909 | 192 | 0.414 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 529,360 | 5.294 | 20 | 20 | fits | 83,084 | 41 | 0.762 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 149,471 | 1.495 | 20 | 24 | fits | 148,089 | 142 | 0.367 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 299,390 | 2.994 | 20 | 24 | fits | 150,909 | 192 | 0.414 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 299,324 | 2.993 | 20 | 50 | fits | 150,909 | 192 | 0.414 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 449,300 | 4.493 | 20 | 50 | fits | 150,372 | 186 | 0.425 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 532,318 | 5.323 | 20 | 20 | fits | 83,084 | 41 | 0.762 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 928,005 | 9.280 | 20 | 20 | fits | 50,192 | 20 | 0.703 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 9,120 | 0.091 | 20 | 200 | fits | 3,140 | 10 (11) | 0.538 |
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
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,213 | 0.072 | 20 | 20 | fits | 29,248 | 13 (29) | 0.789 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 10,032 | 0.100 | 20 | 20 | fits | 32,954 | 19 (35) | 0.793 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 22,084 | 0.221 | 20 | 20 | fits | 35,930 | 21 (12) | 0.818 |
| LINK_UP | `adp.link_up.if0` | 3,014 | 0.030 | 20 | 200 | fits | 33,791 | 43 (11) | 0.731 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,642 | 0.206 | 20 | 200 | fits | 27,497 | 23 (39) | 0.740 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,491 | 0.055 | 20 | 200 | fits | 20,810 | 16 (31) | 0.655 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,361 | 0.214 | 20 | 24 | fits | 30,526 | 20 | 0.777 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 31,459 | 0.315 | 20 | 24 | fits | 34,315 | 20 | 0.697 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 24,121 | 0.241 | 20 | 24 | fits | 30,899 | 20 | 0.727 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 23,642 | 0.236 | 20 | 24 | fits | 30,307 | 20 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 27,564 | 0.276 | 20 | 24 | fits | 30,369 | 20 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 24,487 | 0.245 | 20 | 24 | fits | 31,515 | 20 | 0.721 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 27,241 | 0.272 | 20 | 24 | fits | 30,059 | 20 | 0.719 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 26,418 | 0.264 | 20 | 24 | fits | 30,164 | 20 | 0.734 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 23,735 | 0.237 | 20 | 24 | fits | 30,448 | 20 | 0.741 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 32,166 | 0.322 | 20 | 24 | fits | 35,111 | 21 | 0.645 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 23,145 | 0.231 | 20 | 24 | fits | 29,858 | 20 | 0.759 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 27,312 | 0.273 | 20 | 24 | fits | 29,997 | 20 | 0.762 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 26,342 | 0.263 | 20 | 24 | fits | 30,241 | 20 | 0.725 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 23,968 | 0.240 | 20 | 24 | fits | 30,825 | 20 | 0.727 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 27,628 | 0.276 | 20 | 24 | fits | 30,611 | 20 | 0.731 |
| get_configuration | `aecp.get_configuration.if0` | 21,312 | 0.213 | 20 | 24 | fits | 27,350 | 20 | 0.724 |
| entity_available | `aecp.entity_available.if0` | 25,372 | 0.254 | 20 | 24 | fits | 27,581 | 20 | 0.725 |
| get_name | `aecp.get_name.if0` | 27,673 | 0.277 | 20 | 24 | fits | 30,712 | 20 | 0.751 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 24,660 | 0.247 | 20 | 24 | fits | 31,408 | 27 | 0.721 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 19,730 | 0.197 | 20 | 24 | fits | 33,007 | 29 | 0.777 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 21,542 | 0.215 | 20 | 24 | fits | 28,375 | 20 | 0.757 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 25,101 | 0.251 | 20 | 24 | fits | 27,234 | 20 | 0.725 |
| set_name | `aecp.set_name.if0` | 34,725 | 0.347 | 20 | 24 | fits | 47,330 | 43 | 0.760 |
| lock_entity | `aecp.lock_entity.if0` | 27,594 | 0.276 | 20 | 24 | fits | 38,691 | 34 | 0.775 |
| unlock_entity | `aecp.unlock_entity.if0` | 32,933 | 0.329 | 20 | 24 | fits | 38,703 | 33 | 0.780 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
