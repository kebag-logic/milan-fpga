### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 44 paths and 0 of 143 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.048 (0.164) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-discover) | 0.028 (0.278) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-discover) | 0.161 (0.483) | fits | 0 events | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.145 (0.452) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.230 (0.551) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.179 (0.494) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.196 (0.507) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.236 (0.555) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.173 (0.501) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.198 (0.600) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.192 (0.507) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.257 (0.575) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.169 (0.480) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.164 (0.475) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.213 (0.529) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.190 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.207 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.209 (0.525) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.215 (0.533) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.159 (0.469) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.219 (0.538) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.159 (0.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.171 (0.483) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.174 (0.496) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.214 (0.528) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.144 (0.455) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.288 (0.725) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.236 (0.544) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.259 (0.614) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-1.adp_available.if0` (backlog-adp@blank-1) | 4.554 (6.066) | fits | 7 adp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.acmp.first.if0` (backlog-adp@blank-1) | 3.917 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.acmp.last.if0` (backlog-adp@blank-1) | 5.162 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.adp.first.if0` (backlog-adp@blank-1) | 3.907 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.adp.last.if0` (backlog-adp@blank-1) | 5.155 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.aecp.first.if0` (backlog-adp@blank-1) | 2.341 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.aecp.last.if0` (backlog-adp@blank-1) | 3.943 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.maap.first.if0` (backlog-adp@blank-1) | 3.943 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.maap.last.if0` (backlog-adp@blank-1) | 5.192 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-1.service.srp.first.if0` (backlog-adp@blank-1) | 6.033 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@blank-1.service.srp.last.if0` (backlog-adp@blank-1) | 11.167 | fits | 31 srp | 10 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.857 (0.947) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.422 (0.422) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.215 (0.215) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.791 (0.869) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 13.940 | 12 | 153,370 (1.534) | yes | - |
| backlog-adp@blank-5 | 1 | 13.213 | 12 | 146,655 (1.467) | yes | - |
| backlog-adp@program-5 | 0 | 12.081 | 11 | 152,957 (1.530) | yes | - |
| backlog-adp@verify-5 | 0 | 13.663 | 11 | 152,657 (1.527) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 13.855 | 12 | 151,380 (1.514) | yes | - |
| backlog-adp@blank-aged1-5 | 1 | 12.845 | 10 | 150,293 (1.503) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 12.371 | 11 | 151,393 (1.514) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 12.276 | 11 | 151,307 (1.513) | yes | - |
| backlog-adp@verify-aged2-5 | 1 | 13.820 | 11 | 150,959 (1.510) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 16.262 | 14 | 151,480 (1.515) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-1 | 483 | 0 | 153,370 (1.534) | fits |
| backlog-adp@blank-5 | 484 | 0 | 146,655 (1.467) | fits |
| backlog-adp@program-5 | 493 | 0 | 152,957 (1.530) | fits |
| backlog-adp@verify-5 | 499 | 0 | 152,657 (1.527) | fits |
| backlog-adp@blank-aged2-5 | 781 | 0 | 151,380 (1.514) | fits |
| backlog-adp@blank-aged1-5 | 719 | 0 | 151,466 (1.515) | fits |
| backlog-adp@program-aged2-5 | 808 | 0 | 151,393 (1.514) | fits |
| backlog-adp@program-aged1-5 | 747 | 0 | 151,307 (1.513) | fits |
| backlog-adp@verify-aged2-5 | 825 | 0 | 151,586 (1.516) | fits |
| backlog-adp@verify-aged1-5 | 767 | 0 | 151,480 (1.515) | fits |
| srp | 290 | 0 | 56,186 (0.562) | fits |
| adp-discover | 88 | 0 | 30,398 (0.304) | fits |
| aecp | 114 | 0 | 46,908 (0.469) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-5 | 2 | +4.428 ms, 77,223 (0.772 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 11.083 (20) | 8.917 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.073 (20) | 9.927 |
| backlog-adp@program-aged2-5 | 2 | none | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 10.955 (20) | 9.045 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 10.121 (20) | 9.879 |
| backlog-adp@verify-aged2-5 | 2 | +4.357 ms, 77,773 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 11.019 (20) | 8.981 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 10.193 (20) | 9.807 |

Least margin over the aged windows: 8.917 ms, `backlog-adp@blank-aged2-5.service.srp.last.if0` at 11.083 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-1 | 342 | 92,500 (0.925) | 76,179 (0.762) |
| backlog-adp@blank-5 | 342 | 91,668 (0.917) | 76,234 (0.762) |
| backlog-adp@program-5 | 373 | 95,349 (0.953) | 78,491 (0.785) |
| backlog-adp@verify-5 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@blank-aged2-5 | 340 | 92,514 (0.925) | 76,166 (0.762) |
| backlog-adp@blank-aged1-5 | 339 | 92,449 (0.924) | 76,454 (0.765) |
| backlog-adp@program-aged2-5 | 369 | 95,347 (0.953) | 78,702 (0.787) |
| backlog-adp@program-aged1-5 | 368 | 95,708 (0.957) | 78,835 (0.788) |
| backlog-adp@verify-aged2-5 | 398 | 94,984 (0.950) | 78,276 (0.783) |
| backlog-adp@verify-aged1-5 | 400 | 94,984 (0.950) | 78,276 (0.783) |
| srp | 271 | 22,571 (0.226) | 2,593 (0.026) |
| adp-discover | 79 | 22,571 (0.226) | 2,593 (0.026) |
| aecp | 80 | 22,571 (0.226) | 2,593 (0.026) |

Longest pass that carries a step: 95,708 CPU cycles (0.957 ms), backlog-adp@program-aged1-5; longest step: 78,835 (0.788 ms), backlog-adp@program-aged1-5.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 455,433 | 4.554 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 390,746 | 3.907 | 20 | 200 | fits | 149,967 | 220 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 515,474 | 5.155 | 20 | 200 | fits | 125,344 | 181 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 391,670 | 3.917 | 20 | 20 | fits | 149,967 | 220 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 516,178 | 5.162 | 20 | 20 | fits | 125,344 | 181 | 0.430 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 234,082 | 2.341 | 20 | 24 | fits | 153,370 | 156 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 394,320 | 3.943 | 20 | 24 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 394,254 | 3.943 | 20 | 50 | fits | 149,967 | 220 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 519,202 | 5.192 | 20 | 50 | fits | 125,344 | 181 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 603,333 | 6.033 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 1,116,749 | 11.167 | 20 | 20 | fits | 81,599 | 31 | 0.729 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 369,128 | 3.691 | 20 | 20 | fits | 132,423 | 202 | 0.429 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 297,344 | 2.973 | 20 | 200 | fits | 146,655 | 208 | 0.444 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 429,151 | 4.292 | 20 | 200 | fits | 132,423 | 202 | 0.429 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 298,268 | 2.983 | 20 | 20 | fits | 146,655 | 208 | 0.444 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 429,855 | 4.299 | 20 | 20 | fits | 132,423 | 202 | 0.429 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 143,842 | 1.438 | 20 | 24 | fits | 145,885 | 146 | 0.447 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 300,918 | 3.009 | 20 | 24 | fits | 146,655 | 208 | 0.444 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 300,852 | 3.009 | 20 | 50 | fits | 146,655 | 208 | 0.444 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 432,879 | 4.329 | 20 | 50 | fits | 132,423 | 202 | 0.429 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 517,010 | 5.170 | 20 | 20 | fits | 84,197 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 1,024,586 | 10.246 | 20 | 20 | fits | 75,759 | 25 | 0.701 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 418,985 | 4.190 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 352,472 | 3.525 | 20 | 200 | fits | 150,917 | 209 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 471,498 | 4.715 | 20 | 200 | fits | 119,642 | 184 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 353,396 | 3.534 | 20 | 20 | fits | 150,917 | 209 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 472,202 | 4.722 | 20 | 20 | fits | 119,642 | 184 | 0.412 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 206,119 | 2.061 | 20 | 24 | fits | 152,957 | 155 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 356,046 | 3.560 | 20 | 24 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 355,980 | 3.560 | 20 | 50 | fits | 150,917 | 209 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 475,226 | 4.752 | 20 | 50 | fits | 119,642 | 184 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 559,893 | 5.599 | 20 | 20 | fits | 84,733 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 1,066,300 | 10.663 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 424,593 | 4.246 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 371,787 | 3.718 | 20 | 200 | fits | 149,259 | 226 | 0.434 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 484,658 | 4.847 | 20 | 200 | fits | 113,487 | 163 | 0.424 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 372,711 | 3.727 | 20 | 20 | fits | 149,259 | 226 | 0.434 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 485,362 | 4.854 | 20 | 20 | fits | 113,487 | 163 | 0.424 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 227,092 | 2.271 | 20 | 24 | fits | 152,657 | 155 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 375,361 | 3.754 | 20 | 24 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 375,295 | 3.753 | 20 | 50 | fits | 149,259 | 226 | 0.434 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 488,386 | 4.884 | 20 | 50 | fits | 113,487 | 163 | 0.424 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 573,003 | 5.730 | 20 | 20 | fits | 84,683 | 25 | 0.777 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 1,085,895 | 10.859 | 20 | 20 | fits | 85,724 | 28 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 383,558 | 3.836 | 20 | 20 | fits | 126,796 | 176 | 0.482 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 299,878 | 2.999 | 20 | 200 | fits | 149,407 | 227 | 0.435 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 437,412 | 4.374 | 20 | 200 | fits | 126,796 | 176 | 0.482 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 300,802 | 3.008 | 20 | 20 | fits | 149,407 | 227 | 0.435 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 438,116 | 4.381 | 20 | 20 | fits | 126,796 | 176 | 0.482 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 155,035 | 1.550 | 20 | 24 | fits | 151,380 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 303,452 | 3.035 | 20 | 24 | fits | 149,407 | 227 | 0.435 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 303,386 | 3.034 | 20 | 50 | fits | 149,407 | 227 | 0.435 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 441,140 | 4.411 | 20 | 50 | fits | 126,796 | 176 | 0.482 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 602,209 | 6.022 | 20 | 20 | fits | 83,912 | 25 | 0.773 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,108,286 | 11.083 | 20 | 20 | fits | 66,299 | 27 | 0.753 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 355,230 | 3.552 | 20 | 20 | fits | 113,121 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 294,975 | 2.950 | 20 | 200 | fits | 150,293 | 231 | 0.430 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 407,480 | 4.075 | 20 | 200 | fits | 113,121 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 295,899 | 2.959 | 20 | 20 | fits | 150,293 | 231 | 0.430 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 408,184 | 4.082 | 20 | 20 | fits | 113,121 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 149,246 | 1.492 | 20 | 24 | fits | 151,466 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 298,549 | 2.985 | 20 | 24 | fits | 150,293 | 231 | 0.430 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 298,483 | 2.985 | 20 | 50 | fits | 150,293 | 231 | 0.430 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 411,208 | 4.112 | 20 | 50 | fits | 113,121 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 491,561 | 4.916 | 20 | 20 | fits | 80,419 | 33 | 0.810 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,007,258 | 10.073 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 356,947 | 3.569 | 20 | 20 | fits | 113,158 | 163 | 0.419 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 304,397 | 3.044 | 20 | 200 | fits | 148,376 | 226 | 0.425 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 416,939 | 4.169 | 20 | 200 | fits | 113,158 | 163 | 0.419 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 305,321 | 3.053 | 20 | 20 | fits | 148,376 | 226 | 0.425 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 417,643 | 4.176 | 20 | 20 | fits | 113,158 | 163 | 0.419 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 160,585 | 1.606 | 20 | 24 | fits | 151,393 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 307,971 | 3.080 | 20 | 24 | fits | 148,376 | 226 | 0.425 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 307,905 | 3.079 | 20 | 50 | fits | 148,376 | 226 | 0.425 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 420,667 | 4.207 | 20 | 50 | fits | 113,158 | 163 | 0.419 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 500,815 | 5.008 | 20 | 20 | fits | 80,214 | 33 | 0.809 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 1,095,542 | 10.955 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 352,714 | 3.527 | 20 | 20 | fits | 113,104 | 163 | 0.418 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 300,164 | 3.002 | 20 | 200 | fits | 148,569 | 226 | 0.426 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 412,652 | 4.127 | 20 | 200 | fits | 113,104 | 163 | 0.418 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 301,088 | 3.011 | 20 | 20 | fits | 148,569 | 226 | 0.426 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 413,356 | 4.134 | 20 | 20 | fits | 113,104 | 163 | 0.418 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 156,159 | 1.562 | 20 | 24 | fits | 151,307 | 152 | 0.419 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 303,738 | 3.037 | 20 | 24 | fits | 148,569 | 226 | 0.426 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 303,672 | 3.037 | 20 | 50 | fits | 148,569 | 226 | 0.426 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 416,380 | 4.164 | 20 | 50 | fits | 113,104 | 163 | 0.418 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 505,971 | 5.060 | 20 | 20 | fits | 89,657 | 30 | 0.785 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 1,012,125 | 10.121 | 20 | 20 | fits | 72,985 | 24 | 0.639 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 378,482 | 3.785 | 20 | 20 | fits | 124,271 | 178 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 306,729 | 3.067 | 20 | 200 | fits | 150,959 | 227 | 0.448 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 430,384 | 4.304 | 20 | 200 | fits | 124,271 | 178 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 307,653 | 3.077 | 20 | 20 | fits | 150,959 | 227 | 0.448 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 431,088 | 4.311 | 20 | 20 | fits | 124,271 | 178 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 149,366 | 1.494 | 20 | 24 | fits | 151,586 | 153 | 0.422 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 310,303 | 3.103 | 20 | 24 | fits | 150,959 | 227 | 0.448 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 310,237 | 3.102 | 20 | 50 | fits | 150,959 | 227 | 0.448 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 434,112 | 4.341 | 20 | 50 | fits | 124,271 | 178 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 595,567 | 5.956 | 20 | 20 | fits | 83,748 | 25 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,101,871 | 11.019 | 20 | 20 | fits | 73,249 | 24 | 0.648 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 383,431 | 3.834 | 20 | 20 | fits | 126,415 | 176 | 0.481 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 307,279 | 3.073 | 20 | 200 | fits | 148,688 | 227 | 0.427 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 444,477 | 4.445 | 20 | 200 | fits | 126,415 | 176 | 0.481 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 308,203 | 3.082 | 20 | 20 | fits | 148,688 | 227 | 0.427 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 445,181 | 4.452 | 20 | 20 | fits | 126,415 | 176 | 0.481 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 163,155 | 1.632 | 20 | 24 | fits | 151,480 | 152 | 0.420 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 310,853 | 3.109 | 20 | 24 | fits | 148,688 | 227 | 0.427 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 310,787 | 3.108 | 20 | 50 | fits | 148,688 | 227 | 0.427 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 448,205 | 4.482 | 20 | 50 | fits | 126,415 | 176 | 0.481 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 532,421 | 5.324 | 20 | 20 | fits | 84,282 | 24 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 1,019,266 | 10.193 | 20 | 20 | fits | 59,768 | 20 | 0.683 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,068 | 0.791 | 20 | 20 | fits | 28,704 | 8 | 0.778 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 42,157 | 0.422 | 20 | 20 | fits | 42,223 | 12 | 0.885 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,451 | 0.215 | 20 | 20 | fits | 21,517 | 12 | 0.671 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 85,722 | 0.857 | 220 | 220 | fits | 56,186 | 6 | 0.893 |
| LINK_UP | `adp.link_up.if0` | 2,771 | 0.028 | 20 | 200 | fits | 27,812 | 43 (11) | 0.720 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 16,072 | 0.161 | 20 | 200 | fits | 22,379 | 23 (39) | 0.719 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,807 | 0.048 | 20 | 200 | fits | 16,437 | 16 (31) | 0.567 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,389 | 0.144 | 20 | 24 | fits | 27,860 | 20 | 0.780 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 25,677 | 0.257 | 20 | 24 | fits | 31,637 | 20 | 0.710 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,878 | 0.169 | 20 | 24 | fits | 27,349 | 20 | 0.722 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 21,515 | 0.215 | 20 | 24 | fits | 27,572 | 20 | 0.723 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 17,085 | 0.171 | 20 | 24 | fits | 27,823 | 20 | 0.721 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,404 | 0.174 | 20 | 24 | fits | 28,114 | 20 | 0.731 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 21,391 | 0.214 | 20 | 24 | fits | 26,883 | 20 | 0.724 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 16,407 | 0.164 | 20 | 24 | fits | 26,980 | 20 | 0.736 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,297 | 0.213 | 20 | 24 | fits | 26,961 | 20 | 0.741 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,028 | 0.190 | 20 | 24 | fits | 29,547 | 21 | 0.637 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 20,714 | 0.207 | 20 | 24 | fits | 26,526 | 20 | 0.759 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 20,877 | 0.209 | 20 | 24 | fits | 26,515 | 20 | 0.758 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,919 | 0.159 | 20 | 24 | fits | 26,368 | 20 | 0.720 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 21,947 | 0.219 | 20 | 24 | fits | 27,894 | 20 | 0.735 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,948 | 0.159 | 20 | 24 | fits | 26,683 | 20 | 0.738 |
| get_configuration | `aecp.get_configuration.if0` | 19,638 | 0.196 | 20 | 24 | fits | 25,052 | 20 | 0.757 |
| entity_available | `aecp.entity_available.if0` | 14,497 | 0.145 | 20 | 24 | fits | 24,700 | 20 | 0.738 |
| get_name | `aecp.get_name.if0` | 17,342 | 0.173 | 20 | 24 | fits | 28,573 | 20 | 0.770 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 23,561 | 0.236 | 20 | 24 | fits | 29,335 | 26 | 0.733 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 17,884 | 0.179 | 20 | 24 | fits | 28,888 | 28 | 0.759 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 23,002 | 0.230 | 20 | 24 | fits | 28,996 | 28 | 0.764 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 23,579 | 0.236 | 20 | 24 | fits | 25,969 | 20 | 0.774 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 19,200 | 0.192 | 20 | 24 | fits | 24,857 | 20 | 0.745 |
| set_name | `aecp.set_name.if0` | 28,824 | 0.288 | 20 | 24 | fits | 46,908 | 43 | 0.777 |
| lock_entity | `aecp.lock_entity.if0` | 19,807 | 0.198 | 20 | 24 | fits | 34,668 | 34 | 0.769 |
| unlock_entity | `aecp.unlock_entity.if0` | 25,895 | 0.259 | 20 | 24 | fits | 34,350 | 33 | 0.772 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
