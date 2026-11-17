### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 24 paths and 0 of 124 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.057 (0.212) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-discover) | 0.029 (0.336) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-discover) | 0.142 (0.533) | fits | 0 events | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.453 (0.772) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.504 (0.776) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.579 (0.888) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.521 (0.889) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.475 (0.817) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.492 (0.811) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-5.adp_available.if0` (backlog-adp@blank-5) | 4.296 (4.951) | fits | 7 adp | 10 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.acmp.first.if0` (backlog-adp@blank-aged1-4) | 3.160 | fits | 0 acmp | 10 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-4.service.acmp.last.if0` (backlog-adp@blank-aged1-4) | 6.069 | fits | 11 acmp | 10 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.adp.first.if0` (backlog-adp@blank-aged1-4) | 3.151 | fits | 0 adp | 10 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-5.service.adp.last.if0` (backlog-adp@blank-5) | 4.725 | fits | 7 adp | 10 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@verify-3.service.aecp.first.if0` (backlog-adp@verify-3) | 1.624 | fits | 0 aecp | 10 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-adp@blank-aged1-4.service.aecp.last.if0` (backlog-adp@blank-aged1-4) | 3.187 | fits | 15 aecp | 10 | 0 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.maap.first.if0` (backlog-adp@blank-aged1-4) | 3.186 | fits | 0 maap | 10 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-5.service.maap.last.if0` (backlog-adp@blank-5) | 4.762 | fits | 6 maap | 10 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged1-4.service.srp.first.if0` (backlog-adp@blank-aged1-4) | 6.099 | fits | 0 srp | 10 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-3.service.srp.last.if0` (backlog-adp@program-aged2-3) | 9.268 | fits | 31 srp | 10 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.755 (0.802) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.422 (0.423) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.236 (0.237) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.807 (0.879) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 9.948 | 7 | 152,826 (1.528) | yes | - |
| backlog-adp@blank-5 | 0 | 9.927 | 7 | 155,329 (1.553) | yes | - |
| backlog-adp@program-3 | 0 | 9.991 | 7 | 153,570 (1.536) | yes | - |
| backlog-adp@verify-3 | 0 | 9.928 | 7 | 152,271 (1.523) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.142 | 9 | 154,609 (1.546) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.396 | 9 | 153,419 (1.534) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 9.910 | 7 | 155,073 (1.551) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.364 | 9 | 153,617 (1.536) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 9.796 | 7 | 153,599 (1.536) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 9.911 | 7 | 154,588 (1.546) | yes | - |

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog-adp@blank-1 | 555 | 0 | 152,826 (1.528) | fits |
| backlog-adp@blank-5 | 554 | 0 | 155,329 (1.553) | fits |
| backlog-adp@program-3 | 939 | 0 | 153,570 (1.536) | fits |
| backlog-adp@verify-3 | 1314 | 0 | 152,271 (1.523) | fits |
| backlog-adp@blank-aged2-3 | 817 | 0 | 154,609 (1.546) | fits |
| backlog-adp@blank-aged1-4 | 773 | 0 | 153,419 (1.534) | fits |
| backlog-adp@program-aged2-3 | 1194 | 0 | 155,073 (1.551) | fits |
| backlog-adp@program-aged1-3 | 1145 | 0 | 153,617 (1.536) | fits |
| backlog-adp@verify-aged2-3 | 1574 | 0 | 153,599 (1.536) | fits |
| backlog-adp@verify-aged1-3 | 1524 | 0 | 154,588 (1.546) | fits |
| srp | 290 | 0 | 42,680 (0.427) | fits |
| adp-discover | 88 | 0 | 33,635 (0.336) | fits |
| aecp-fanout | 109 | 0 | 59,297 (0.593) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-3 | 2 | +7.333 ms, 76,624 (0.766 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.165 (20) | 10.835 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.450 (20) | 11.550 |
| backlog-adp@program-aged2-3 | 2 | none | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 9.268 (20) | 10.732 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.373 (20) | 11.627 |
| backlog-adp@verify-aged2-3 | 2 | +7.314 ms, 77,591 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.154 (20) | 10.846 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.504 (20) | 11.496 |

Least margin over the aged windows: 10.732 ms, `backlog-adp@program-aged2-3.service.srp.last.if0` at 9.268 ms.

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| backlog-adp@blank-1 | 339 | 94,788 (0.948) | 75,892 (0.759) |
| backlog-adp@blank-5 | 339 | 96,311 (0.963) | 76,025 (0.760) |
| backlog-adp@program-3 | 448 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-3 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@blank-aged2-3 | 337 | 79,120 (0.791) | 75,467 (0.755) |
| backlog-adp@blank-aged1-4 | 337 | 96,141 (0.961) | 75,944 (0.759) |
| backlog-adp@program-aged2-3 | 446 | 100,322 (1.003) | 78,221 (0.782) |
| backlog-adp@program-aged1-3 | 446 | 100,322 (1.003) | 78,354 (0.784) |
| backlog-adp@verify-aged2-3 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| backlog-adp@verify-aged1-3 | 555 | 104,189 (1.042) | 78,074 (0.781) |
| srp | 271 | 25,989 (0.260) | 2,306 (0.023) |
| adp-discover | 79 | 25,989 (0.260) | 2,306 (0.023) |
| aecp-fanout | 79 | 25,989 (0.260) | 2,306 (0.023) |

Longest pass that carries a step: 104,189 CPU cycles (1.042 ms), backlog-adp@verify-3; longest step: 78,354 (0.784 ms), backlog-adp@program-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 377,907 | 3.779 | 20 | 20 | fits | 152,826 | 205 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 294,697 | 2.947 | 20 | 200 | fits | 151,068 | 180 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 446,907 | 4.469 | 20 | 200 | fits | 152,826 | 205 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 295,621 | 2.956 | 20 | 20 | fits | 151,068 | 180 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 579,973 | 5.800 | 20 | 20 | fits | 132,362 | 55 | 0.625 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 148,193 | 1.482 | 20 | 24 | fits | 149,277 | 145 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 298,271 | 2.983 | 20 | 24 | fits | 151,068 | 180 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 298,205 | 2.982 | 20 | 50 | fits | 151,068 | 180 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 450,635 | 4.506 | 20 | 50 | fits | 152,826 | 205 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 582,931 | 5.829 | 20 | 20 | fits | 132,362 | 55 | 0.625 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 818,048 | 8.180 | 20 | 20 | fits | 109,737 | 49 | 0.497 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 429,602 | 4.296 | 20 | 20 | fits | 155,329 | 207 | 0.412 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 307,564 | 3.076 | 20 | 200 | fits | 151,189 | 181 | 0.390 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 472,498 | 4.725 | 20 | 200 | fits | 155,329 | 207 | 0.412 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 308,488 | 3.085 | 20 | 20 | fits | 151,189 | 181 | 0.390 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 605,761 | 6.058 | 20 | 20 | fits | 132,559 | 61 | 0.602 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 160,939 | 1.609 | 20 | 24 | fits | 149,260 | 145 | 0.355 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 311,138 | 3.111 | 20 | 24 | fits | 151,189 | 181 | 0.390 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 311,072 | 3.111 | 20 | 50 | fits | 151,189 | 181 | 0.390 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 476,226 | 4.762 | 20 | 50 | fits | 155,329 | 207 | 0.412 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 608,719 | 6.087 | 20 | 20 | fits | 132,559 | 61 | 0.602 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 852,418 | 8.524 | 20 | 20 | fits | 118,245 | 52 | 0.482 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 407,673 | 4.077 | 20 | 20 | fits | 153,570 | 208 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 305,471 | 3.055 | 20 | 200 | fits | 148,645 | 174 | 0.413 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 458,425 | 4.584 | 20 | 200 | fits | 153,570 | 208 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 306,395 | 3.064 | 20 | 20 | fits | 148,645 | 174 | 0.413 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 590,845 | 5.908 | 20 | 20 | fits | 131,716 | 61 | 0.597 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 161,390 | 1.614 | 20 | 24 | fits | 148,736 | 145 | 0.349 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 309,045 | 3.090 | 20 | 24 | fits | 148,645 | 174 | 0.413 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 308,979 | 3.090 | 20 | 50 | fits | 148,645 | 174 | 0.413 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 462,153 | 4.622 | 20 | 50 | fits | 153,570 | 208 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 593,803 | 5.938 | 20 | 20 | fits | 131,716 | 61 | 0.597 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 854,736 | 8.547 | 20 | 20 | fits | 124,473 | 59 | 0.563 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 408,850 | 4.088 | 20 | 20 | fits | 152,271 | 204 | 0.341 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 308,823 | 3.088 | 20 | 200 | fits | 150,982 | 180 | 0.388 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 460,478 | 4.605 | 20 | 200 | fits | 152,271 | 204 | 0.341 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 309,747 | 3.097 | 20 | 20 | fits | 150,982 | 180 | 0.388 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 593,461 | 5.935 | 20 | 20 | fits | 132,279 | 56 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 162,405 | 1.624 | 20 | 24 | fits | 149,055 | 145 | 0.353 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 312,397 | 3.124 | 20 | 24 | fits | 150,982 | 180 | 0.388 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 312,331 | 3.123 | 20 | 50 | fits | 150,982 | 180 | 0.388 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 464,206 | 4.642 | 20 | 50 | fits | 152,271 | 204 | 0.341 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 596,419 | 5.964 | 20 | 20 | fits | 132,279 | 56 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 852,359 | 8.524 | 20 | 20 | fits | 110,153 | 48 | 0.509 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 402,358 | 4.024 | 20 | 20 | fits | 154,609 | 196 | 0.328 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 308,509 | 3.085 | 20 | 200 | fits | 151,844 | 197 | 0.397 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 462,502 | 4.625 | 20 | 200 | fits | 154,609 | 196 | 0.328 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 309,433 | 3.094 | 20 | 20 | fits | 151,844 | 197 | 0.397 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 595,419 | 5.954 | 20 | 20 | fits | 132,213 | 55 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 151,600 | 1.516 | 20 | 24 | fits | 147,978 | 143 | 0.345 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 312,083 | 3.121 | 20 | 24 | fits | 151,844 | 197 | 0.397 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 312,017 | 3.120 | 20 | 50 | fits | 151,844 | 197 | 0.397 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 466,230 | 4.662 | 20 | 50 | fits | 154,609 | 196 | 0.328 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 598,377 | 5.984 | 20 | 20 | fits | 132,213 | 55 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 916,469 | 9.165 | 20 | 20 | fits | 110,269 | 50 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 398,350 | 3.983 | 20 | 20 | fits | 152,877 | 205 | 0.348 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 315,086 | 3.151 | 20 | 200 | fits | 153,419 | 185 | 0.403 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 467,347 | 4.673 | 20 | 200 | fits | 152,877 | 205 | 0.348 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 316,010 | 3.160 | 20 | 20 | fits | 153,419 | 185 | 0.403 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 606,930 | 6.069 | 20 | 20 | fits | 138,879 | 63 | 0.631 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 156,602 | 1.566 | 20 | 24 | fits | 147,980 | 143 | 0.344 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 318,660 | 3.187 | 20 | 24 | fits | 153,419 | 185 | 0.403 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 318,594 | 3.186 | 20 | 50 | fits | 153,419 | 185 | 0.403 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 471,075 | 4.711 | 20 | 50 | fits | 152,877 | 205 | 0.348 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 609,888 | 6.099 | 20 | 20 | fits | 138,879 | 63 | 0.631 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 844,989 | 8.450 | 20 | 20 | fits | 109,580 | 48 | 0.495 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 393,331 | 3.933 | 20 | 20 | fits | 155,073 | 195 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 299,278 | 2.993 | 20 | 200 | fits | 149,231 | 192 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 453,735 | 4.537 | 20 | 200 | fits | 155,073 | 195 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 300,202 | 3.002 | 20 | 20 | fits | 149,231 | 192 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 586,080 | 5.861 | 20 | 20 | fits | 131,641 | 55 | 0.623 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 154,611 | 1.546 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 302,852 | 3.029 | 20 | 24 | fits | 149,231 | 192 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 302,786 | 3.028 | 20 | 50 | fits | 149,231 | 192 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 457,463 | 4.575 | 20 | 50 | fits | 155,073 | 195 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 589,038 | 5.890 | 20 | 20 | fits | 131,641 | 55 | 0.623 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 926,821 | 9.268 | 20 | 20 | fits | 115,726 | 55 | 0.576 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 391,972 | 3.920 | 20 | 20 | fits | 152,797 | 205 | 0.346 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 308,745 | 3.087 | 20 | 200 | fits | 153,617 | 185 | 0.405 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 460,926 | 4.609 | 20 | 200 | fits | 152,797 | 205 | 0.346 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 309,669 | 3.097 | 20 | 20 | fits | 153,617 | 185 | 0.405 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 593,353 | 5.934 | 20 | 20 | fits | 131,723 | 55 | 0.624 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 150,063 | 1.501 | 20 | 24 | fits | 147,728 | 143 | 0.343 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 312,319 | 3.123 | 20 | 24 | fits | 153,617 | 185 | 0.405 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 312,253 | 3.123 | 20 | 50 | fits | 153,617 | 185 | 0.405 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 464,654 | 4.647 | 20 | 50 | fits | 152,797 | 205 | 0.346 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 596,311 | 5.963 | 20 | 20 | fits | 131,723 | 55 | 0.624 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 837,320 | 8.373 | 20 | 20 | fits | 109,867 | 48 | 0.503 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 395,204 | 3.952 | 20 | 20 | fits | 153,599 | 209 | 0.331 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 293,045 | 2.930 | 20 | 200 | fits | 149,367 | 176 | 0.389 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 446,028 | 4.460 | 20 | 200 | fits | 153,599 | 209 | 0.331 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 293,969 | 2.940 | 20 | 20 | fits | 149,367 | 176 | 0.389 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 578,945 | 5.789 | 20 | 20 | fits | 132,213 | 56 | 0.621 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 148,242 | 1.482 | 20 | 24 | fits | 147,508 | 142 | 0.340 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 296,619 | 2.966 | 20 | 24 | fits | 149,367 | 176 | 0.389 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 296,553 | 2.966 | 20 | 50 | fits | 149,367 | 176 | 0.389 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 449,756 | 4.498 | 20 | 50 | fits | 153,599 | 209 | 0.331 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 581,903 | 5.819 | 20 | 20 | fits | 132,213 | 56 | 0.621 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 915,424 | 9.154 | 20 | 20 | fits | 110,221 | 49 | 0.504 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 396,424 | 3.964 | 20 | 20 | fits | 154,588 | 196 | 0.329 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 302,597 | 3.026 | 20 | 200 | fits | 149,274 | 192 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 456,569 | 4.566 | 20 | 200 | fits | 154,588 | 196 | 0.329 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 303,521 | 3.035 | 20 | 20 | fits | 149,274 | 192 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 589,369 | 5.894 | 20 | 20 | fits | 132,096 | 55 | 0.622 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 157,887 | 1.579 | 20 | 24 | fits | 147,566 | 142 | 0.341 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 306,171 | 3.062 | 20 | 24 | fits | 149,274 | 192 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 306,105 | 3.061 | 20 | 50 | fits | 149,274 | 192 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 460,297 | 4.603 | 20 | 50 | fits | 154,588 | 196 | 0.329 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 592,327 | 5.923 | 20 | 20 | fits | 132,096 | 55 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 850,405 | 8.504 | 20 | 20 | fits | 115,571 | 55 | 0.576 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 80,679 | 0.807 | 20 | 20 | fits | 27,583 | 8 | 0.780 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 42,221 | 0.422 | 20 | 20 | fits | 42,287 | 12 | 0.889 |
| malformed MRPDU discard | `srp.malformed.if0` | 23,596 | 0.236 | 20 | 20 | fits | 23,662 | 12 | 0.740 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 75,494 | 0.755 | 220 | 220 | fits | 42,680 | 6 | 0.898 |
| LINK_UP | `adp.link_up.if0` | 2,856 | 0.029 | 20 | 200 | fits | 33,635 | 43 (11) | 0.730 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 14,239 | 0.142 | 20 | 200 | fits | 27,591 | 23 (39) | 0.747 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 5,719 | 0.057 | 20 | 200 | fits | 21,167 | 16 (31) | 0.674 |
| set_name | `aecp_fanout.set_name.if0` | 52,150 | 0.521 | 20 | 24 | fits | 59,297 | 87 | 0.572 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 50,380 | 0.504 | 20 | 24 | fits | 54,824 | 77 | 0.590 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 46,658 | 0.467 | 20 | 24 | fits | 51,265 | 78 | 0.556 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 57,864 | 0.579 | 20 | 24 | fits | 51,044 | 77 | 0.558 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 47,548 | 0.475 | 20 | 24 | fits | 54,275 | 67 | 0.580 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 45,252 | 0.453 | 20 | 24 | fits | 51,092 | 77 | 0.560 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 49,180 | 0.492 | 20 | 24 | fits | 50,088 | 78 | 0.550 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
