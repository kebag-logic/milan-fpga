### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 39 paths and 7 of 140 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.122 (0.617) | fits | 0 events | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.189 (0.565) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.228 (0.611) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.158 (0.534) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.174 (0.554) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.176 (0.555) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.210 (0.690) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.185 (0.562) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.250 (0.632) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.182 (0.561) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.174 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.172 (0.558) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.261 (0.643) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.175 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.207 (0.590) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.171 (0.553) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.174 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.174 (0.562) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.216 (0.598) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.215 (0.597) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.187 (0.568) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.208 (0.589) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.165 (0.546) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.281 (0.767) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.166 (0.539) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.260 (0.689) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@program-aged2-7.adp_available.if0` (backlog-adp@program-aged2-7) | 4.900 (5.444) | fits | 7 adp | 9 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.511 (63.885) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.490 (64.864) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-0.service.acmp.first.if0` (backlog-adp@blank-aged1-0) | 3.081 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.401 | MISS ceiling | 11 acmp | 10 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-0.service.adp.first.if0` (backlog-adp@blank-aged1-0) | 3.072 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.adp.last.if0` (backlog-adp@program-aged2-7) | 5.419 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.aecp.first.if0` (backlog-adp@blank-aged2-7) | 1.629 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.049 | MISS ceiling | 15 aecp | 10 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-0.service.maap.first.if0` (backlog-adp@blank-aged1-0) | 3.107 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.maap.last.if0` (backlog-adp@program-aged2-7) | 5.456 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 6.892 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.srp.last.if0` (backlog-adp@blank-aged2-7) | 9.329 | fits | 31 srp | 10 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@program-7 | 0 | 9.170 | 7 | 153,780 (1.538) | yes | - |
| backlog-adp@verify-7 | 0 | 10.130 | 8 | 153,838 (1.538) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 9.973 | 7 | 157,794 (1.578) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 11.042 | 8 | 152,744 (1.527) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 9.858 | 7 | 153,393 (1.534) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 9.857 | 7 | 158,870 (1.589) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 9.978 | 7 | 153,879 (1.539) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 9.944 | 7 | 153,788 (1.538) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 9.867 | 7 | 149,661 (1.497) | yes | - |
| backlog-owed | 0 | 65.286 | 22 | 154,046 (1.540) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 154,046 CPU cycles (1.540 ms), backlog-owed.
Over the windows that released their whole load only: 154,046 (1.540 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3357 | 0 | 46,561 (0.466) | fits |
| backlog-adp@program-7 | 942 | 0 | 153,780 (1.538) | fits |
| backlog-adp@verify-7 | 1317 | 0 | 153,838 (1.538) | fits |
| backlog-adp@blank-aged2-7 | 841 | 0 | 157,794 (1.578) | fits |
| backlog-adp@blank-aged1-0 | 747 | 0 | 152,744 (1.527) | fits |
| backlog-adp@blank-aged1-7 | 790 | 0 | 153,393 (1.534) | fits |
| backlog-adp@program-aged2-7 | 1219 | 0 | 158,870 (1.589) | fits |
| backlog-adp@program-aged1-7 | 1169 | 0 | 153,879 (1.539) | fits |
| backlog-adp@verify-aged2-7 | 1600 | 0 | 153,788 (1.538) | fits |
| backlog-adp@verify-aged1-7 | 1549 | 0 | 149,661 (1.497) | fits |
| backlog-owed | 307 | 0 | 154,046 (1.540) | fits |
| aecp | 112 | 0 | 51,848 (0.518) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-7 | 2 | +3.113 ms, 76,903 (0.769 ms), read-back | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 9.329 (20) | 10.671 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.474 (20) | 11.526 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.463 (20) | 11.537 |
| backlog-adp@program-aged2-7 | 2 | none | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 9.212 (20) | 10.788 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.533 (20) | 11.467 |
| backlog-adp@verify-aged2-7 | 2 | +3.070 ms, 77,768 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.302 (20) | 10.698 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.454 (20) | 11.546 |

Least margin over the aged windows: 10.671 ms, `backlog-adp@blank-aged2-7.service.srp.last.if0` at 9.329 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 108,329 (1.083) | 78,040 (0.780) |
| backlog-adp@program-7 | 449 | 100,322 (1.003) | 77,944 (0.779) |
| backlog-adp@verify-7 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-7 | 337 | 79,120 (0.791) | 75,549 (0.755) |
| backlog-adp@blank-aged1-0 | 338 | 95,860 (0.959) | 75,944 (0.759) |
| backlog-adp@blank-aged1-7 | 337 | 95,600 (0.956) | 75,944 (0.759) |
| backlog-adp@program-aged2-7 | 446 | 100,322 (1.003) | 78,215 (0.782) |
| backlog-adp@program-aged1-7 | 446 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-aged2-7 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-7 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-owed | 277 | 25,989 (0.260) | 2,306 (0.023) |
| aecp | 80 | 25,989 (0.260) | 3,573 (0.036) |

Longest pass that carries a step: 108,329 CPU cycles (1.083 ms), acmp-notk; longest step: 78,354 (0.784 ms), backlog-adp@program-aged1-7.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 12,230 | 0.122 | 20 | 20 | fits | 39,716 | 19 (14) | 0.892 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 402,375 | 4.024 | 20 | 20 | fits | 153,780 | 209 | 0.334 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 300,272 | 3.003 | 20 | 200 | fits | 148,284 | 174 | 0.411 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 453,436 | 4.534 | 20 | 200 | fits | 153,780 | 209 | 0.334 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 301,196 | 3.012 | 20 | 20 | fits | 148,284 | 174 | 0.411 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 601,075 | 6.011 | 20 | 20 | fits | 136,427 | 68 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 156,552 | 1.566 | 20 | 24 | fits | 148,783 | 145 | 0.350 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 303,846 | 3.038 | 20 | 24 | fits | 148,284 | 174 | 0.411 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 303,780 | 3.038 | 20 | 50 | fits | 148,284 | 174 | 0.411 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 457,164 | 4.572 | 20 | 50 | fits | 153,780 | 209 | 0.334 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 604,033 | 6.040 | 20 | 20 | fits | 136,427 | 68 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 847,926 | 8.479 | 20 | 20 | fits | 118,437 | 52 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 416,737 | 4.167 | 20 | 20 | fits | 153,838 | 206 | 0.342 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 305,802 | 3.058 | 20 | 200 | fits | 148,596 | 174 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 459,024 | 4.590 | 20 | 200 | fits | 153,838 | 206 | 0.342 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 306,726 | 3.067 | 20 | 20 | fits | 148,596 | 174 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 591,962 | 5.920 | 20 | 20 | fits | 132,234 | 61 | 0.597 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 161,770 | 1.618 | 20 | 24 | fits | 148,535 | 145 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 309,376 | 3.094 | 20 | 24 | fits | 148,596 | 174 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 309,310 | 3.093 | 20 | 50 | fits | 148,596 | 174 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 462,752 | 4.628 | 20 | 50 | fits | 153,838 | 206 | 0.342 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 594,920 | 5.949 | 20 | 20 | fits | 132,234 | 61 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 838,760 | 8.388 | 20 | 20 | fits | 118,402 | 53 | 0.483 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 489,840 | 4.898 | 20 | 20 | fits | 157,794 | 215 | 0.353 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 306,519 | 3.065 | 20 | 200 | fits | 148,185 | 174 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 540,600 | 5.406 | 20 | 200 | fits | 157,794 | 215 | 0.353 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 307,443 | 3.074 | 20 | 20 | fits | 148,185 | 174 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 686,237 | 6.862 | 20 | 20 | fits | 134,207 | 62 | 0.616 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 162,898 | 1.629 | 20 | 24 | fits | 147,816 | 142 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 310,093 | 3.101 | 20 | 24 | fits | 148,185 | 174 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 310,027 | 3.100 | 20 | 50 | fits | 148,185 | 174 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 544,328 | 5.443 | 20 | 50 | fits | 157,794 | 215 | 0.353 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 689,195 | 6.892 | 20 | 20 | fits | 134,207 | 62 | 0.616 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 932,944 | 9.329 | 20 | 20 | fits | 118,298 | 52 | 0.483 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 390,360 | 3.904 | 20 | 20 | fits | 152,744 | 205 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 307,187 | 3.072 | 20 | 200 | fits | 150,980 | 180 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 459,315 | 4.593 | 20 | 200 | fits | 152,744 | 205 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 308,111 | 3.081 | 20 | 20 | fits | 150,980 | 180 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 592,277 | 5.923 | 20 | 20 | fits | 132,258 | 55 | 0.625 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 160,771 | 1.608 | 20 | 24 | fits | 147,749 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 310,761 | 3.108 | 20 | 24 | fits | 150,980 | 180 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 310,695 | 3.107 | 20 | 50 | fits | 150,980 | 180 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 463,043 | 4.630 | 20 | 50 | fits | 152,744 | 205 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 595,235 | 5.952 | 20 | 20 | fits | 132,258 | 55 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 847,407 | 8.474 | 20 | 20 | fits | 115,727 | 55 | 0.577 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 398,221 | 3.982 | 20 | 20 | fits | 153,393 | 208 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 296,224 | 2.962 | 20 | 200 | fits | 148,185 | 174 | 0.409 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 449,001 | 4.490 | 20 | 200 | fits | 153,393 | 208 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 297,148 | 2.971 | 20 | 20 | fits | 148,185 | 174 | 0.409 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 582,269 | 5.823 | 20 | 20 | fits | 132,564 | 62 | 0.600 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 152,603 | 1.526 | 20 | 24 | fits | 147,758 | 142 | 0.342 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 299,798 | 2.998 | 20 | 24 | fits | 148,185 | 174 | 0.409 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 299,732 | 2.997 | 20 | 50 | fits | 148,185 | 174 | 0.409 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 452,729 | 4.527 | 20 | 50 | fits | 153,393 | 208 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 585,227 | 5.852 | 20 | 20 | fits | 132,564 | 62 | 0.600 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 846,305 | 8.463 | 20 | 20 | fits | 118,818 | 52 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 489,962 | 4.900 | 20 | 20 | fits | 158,870 | 213 | 0.382 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 293,966 | 2.940 | 20 | 200 | fits | 148,319 | 175 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 541,911 | 5.419 | 20 | 200 | fits | 158,870 | 213 | 0.382 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 294,890 | 2.949 | 20 | 20 | fits | 148,319 | 175 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 674,487 | 6.745 | 20 | 20 | fits | 131,872 | 61 | 0.599 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 150,211 | 1.502 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 297,540 | 2.975 | 20 | 24 | fits | 148,319 | 175 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 297,474 | 2.975 | 20 | 50 | fits | 148,319 | 175 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 545,639 | 5.456 | 20 | 50 | fits | 158,870 | 213 | 0.382 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 677,445 | 6.774 | 20 | 20 | fits | 131,872 | 61 | 0.599 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 921,156 | 9.212 | 20 | 20 | fits | 118,421 | 52 | 0.485 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 407,172 | 4.072 | 20 | 20 | fits | 153,879 | 208 | 0.339 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 305,305 | 3.053 | 20 | 200 | fits | 148,518 | 174 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 458,568 | 4.586 | 20 | 200 | fits | 153,879 | 208 | 0.339 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 306,229 | 3.062 | 20 | 20 | fits | 148,518 | 174 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 606,416 | 6.064 | 20 | 20 | fits | 136,636 | 68 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 161,351 | 1.614 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 308,879 | 3.089 | 20 | 24 | fits | 148,518 | 174 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 308,813 | 3.088 | 20 | 50 | fits | 148,518 | 174 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 462,296 | 4.623 | 20 | 50 | fits | 153,879 | 208 | 0.339 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 609,374 | 6.094 | 20 | 20 | fits | 136,636 | 68 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 853,267 | 8.533 | 20 | 20 | fits | 118,437 | 52 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 482,341 | 4.823 | 20 | 20 | fits | 153,788 | 208 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 302,297 | 3.023 | 20 | 200 | fits | 148,548 | 174 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 533,237 | 5.332 | 20 | 200 | fits | 153,788 | 208 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 303,221 | 3.032 | 20 | 20 | fits | 148,548 | 174 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 666,271 | 6.663 | 20 | 20 | fits | 132,330 | 61 | 0.598 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 158,313 | 1.583 | 20 | 24 | fits | 147,846 | 142 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 305,871 | 3.059 | 20 | 24 | fits | 148,548 | 174 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 305,805 | 3.058 | 20 | 50 | fits | 148,548 | 174 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 536,965 | 5.370 | 20 | 50 | fits | 153,788 | 208 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 669,229 | 6.692 | 20 | 20 | fits | 132,330 | 61 | 0.598 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 930,202 | 9.302 | 20 | 20 | fits | 124,326 | 59 | 0.561 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 414,396 | 4.144 | 20 | 20 | fits | 149,661 | 207 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 297,348 | 2.973 | 20 | 200 | fits | 148,425 | 175 | 0.412 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 456,744 | 4.567 | 20 | 200 | fits | 149,661 | 207 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 298,272 | 2.983 | 20 | 20 | fits | 148,425 | 175 | 0.412 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 590,509 | 5.905 | 20 | 20 | fits | 133,061 | 66 | 0.581 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 153,487 | 1.535 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 300,922 | 3.009 | 20 | 24 | fits | 148,425 | 175 | 0.412 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 300,856 | 3.009 | 20 | 50 | fits | 148,425 | 175 | 0.412 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 460,472 | 4.605 | 20 | 50 | fits | 149,661 | 207 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 593,467 | 5.935 | 20 | 20 | fits | 133,061 | 66 | 0.581 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 845,404 | 8.454 | 20 | 20 | fits | 126,468 | 56 | 0.471 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,351,129 | 63.511 | 20 | 20 | MISS ceiling | 23,425 | 13 | 0.612 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,374,479 | 63.745 | 20 | 20 | MISS ceiling | 23,426 | 13 | 0.578 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,402,681 | 64.027 | 20 | 20 | MISS ceiling | 26,994 | 18 | 0.710 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,424,822 | 64.248 | 20 | 20 | MISS ceiling | 24,441 | 13 | 0.598 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,448,987 | 64.490 | 20 | 20 | MISS ceiling | 23,375 | 13 | 0.620 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 162,621 | 1.626 | 20 | 200 | fits | 154,046 | 177 | 0.433 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 294,181 | 2.942 | 20 | 200 | fits | 132,176 | 207 | 0.331 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 158,299 | 1.583 | 20 | 20 | fits | 154,046 | 177 | 0.433 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,240,080 | 62.401 | 20 | 20 | MISS ceiling | 38,661 | 15 | 0.761 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 161,939 | 1.619 | 20 | 24 | fits | 154,046 | 177 | 0.433 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,204,905 | 62.049 | 20 | 24 | MISS ceiling | 153,900 | 106 | 0.386 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 160,883 | 1.609 | 20 | 50 | fits | 154,046 | 177 | 0.433 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 292,663 | 2.927 | 20 | 50 | fits | 132,176 | 207 | 0.331 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 424,129 | 4.241 | 20 | 20 | fits | 131,532 | 52 | 0.608 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 658,528 | 6.585 | 20 | 20 | fits | 102,801 | 44 | 0.544 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,526 | 0.165 | 20 | 24 | fits | 31,721 | 20 | 0.790 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 24,960 | 0.250 | 20 | 24 | fits | 34,747 | 20 | 0.704 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,199 | 0.182 | 20 | 24 | fits | 31,082 | 20 | 0.738 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,125 | 0.171 | 20 | 24 | fits | 30,992 | 20 | 0.732 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 21,533 | 0.215 | 20 | 24 | fits | 31,002 | 20 | 0.728 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 18,658 | 0.187 | 20 | 24 | fits | 31,962 | 20 | 0.735 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,754 | 0.208 | 20 | 24 | fits | 30,671 | 20 | 0.736 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 17,383 | 0.174 | 20 | 24 | fits | 30,287 | 20 | 0.742 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,243 | 0.172 | 20 | 24 | fits | 31,255 | 20 | 0.759 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 26,097 | 0.261 | 20 | 24 | fits | 35,675 | 21 | 0.660 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 17,457 | 0.175 | 20 | 24 | fits | 30,386 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 20,670 | 0.207 | 20 | 24 | fits | 30,470 | 20 | 0.778 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 17,353 | 0.174 | 20 | 24 | fits | 30,403 | 20 | 0.734 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 17,391 | 0.174 | 20 | 24 | fits | 31,477 | 20 | 0.746 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 21,566 | 0.216 | 20 | 24 | fits | 31,137 | 20 | 0.744 |
| get_configuration | `aecp.get_configuration.if0` | 15,830 | 0.158 | 20 | 24 | fits | 28,420 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if0` | 18,879 | 0.189 | 20 | 24 | fits | 28,288 | 20 | 0.745 |
| get_name | `aecp.get_name.if0` | 17,633 | 0.176 | 20 | 24 | fits | 30,571 | 20 | 0.752 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 17,440 | 0.174 | 20 | 24 | fits | 31,120 | 26 | 0.710 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 22,777 | 0.228 | 20 | 24 | fits | 32,044 | 28 | 0.757 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 16,596 | 0.166 | 20 | 24 | fits | 29,292 | 20 | 0.775 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 18,479 | 0.185 | 20 | 24 | fits | 27,751 | 20 | 0.737 |
| set_name | `aecp.set_name.if0` | 28,079 | 0.281 | 20 | 24 | fits | 51,848 | 47 | 0.766 |
| lock_entity | `aecp.lock_entity.if0` | 20,982 | 0.210 | 20 | 24 | fits | 38,850 | 33 | 0.785 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,027 | 0.260 | 20 | 24 | fits | 39,259 | 32 | 0.790 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
