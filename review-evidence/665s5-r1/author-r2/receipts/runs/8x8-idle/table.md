### 8x8, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm idle

Graded against the bounds in the tree at this base. The amended column gives the owner's decisions of 2026-11-06 on #665, for information: it grades nothing, and this harness re-grades when #810 merges.

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Amended service bound, ms, for information | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|---:|
| H-ADP | 44 | 5 | 0 | 3.367 (20), `adp.link_down.if1`, margin 1996.6 of 2000 | 44.152 (20) **over its bound**, `backlog-adp.service.adp.last.if0`, margin 1955.8 of 2000 | 20 | 4 (0) | 0 |
| H-DISC | 13 | 2 | 0 | 15.927 (20), `acmp.entity_available.if1`, margin 184.1 of 200 | 37.316 (20) **over its bound**, `backlog.adp_available.if0`, margin 162.7 of 200 | 20 | 2 (0) | 0 |
| H-ACMP | 43 | 11 | 0 | 15.988 (20), `acmp.unbind_rx.if1`, margin 184.0 of 200 | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -163.4 of 200 | 20 | 68 (0) | 0 |
| H-AECP | 50 | 5 | 0 | 2.396 (20), `aecp.set_name.if0`, margin 237.6 of 240 | 205.203 (20) **over its bound**, `backlog-adp-refill.service.aecp.last.if1`, margin 34.8 of 240 | 20 | 14 (0) | 0 |
| H-NOTIFY | 15 | 1 | 0 | 6.855 (20), `aecp_fanout.set_name.if0`, margin 233.1 of 240 | 84.071 (20) **over its bound**, `hooks-load-notify.set_name.if0`, margin 155.9 of 240 | 20 | 15 (0) | 0 |
| H-COUNTERS | 0 | 0 | 0 | - | - | - | 0 (0) | 0 |
| H-MAAP | 23 | 5 | 0 | 1.757 (20), `maap.announce.if1`, margin 498.2 of 500 | 44.189 (20) **over its bound**, `backlog-adp.service.maap.last.if0`, margin 455.8 of 500 | 20 | 44 (0) | 0 |
| H-SRP | 19 | 9 | 0 | 4.043 (18), `srp.startup.if1`, margin 176.0 of 180 | never served (18) **over its bound**, `backlog-adp-refill.service.srp.first.if0`, margin -387.5 of 180 | 20 | 2 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound at this base, ms | Amended bound, ms, for information | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-ACMP | `acmp.bind_rx.if0` | acmp-cmd | 0 | 0.635 | 63,461 | 0 | 20 | 20 | yes | 1,936,539 | no | 199.365 of 200 |
| H-ACMP | `acmp.bind_rx.if1` | acmp-cmd | 1 | 3.484 | 348,427 | 0 | 20 | 20 | yes | 1,651,573 | no | 196.516 of 200 |
| H-ACMP | `acmp.disconnect_tx.if0` | acmp-cmd | 0 | 1.904 | 190,415 | 0 | 20 | 20 | yes | 1,809,585 | no | 198.096 of 200 |
| H-ACMP | `acmp.disconnect_tx.if1` | acmp-cmd | 1 | 15.844 | 1,584,410 | 0 | 20 | 20 | yes | 415,590 | no | 184.156 of 200 |
| H-ACMP | `acmp.get_rx_state.if0` | acmp-cmd | 0 | 4.615 | 461,530 | 0 | 20 | 20 | yes | 1,538,470 | no | 195.385 of 200 |
| H-ACMP | `acmp.get_rx_state.if1` | acmp-cmd | 1 | 13.740 | 1,374,022 | 0 | 20 | 20 | yes | 625,978 | no | 186.260 of 200 |
| H-ACMP | `acmp.get_tx_connection.if0` | acmp-cmd | 0 | 4.475 | 447,521 | 0 | 20 | 20 | yes | 1,552,479 | no | 195.525 of 200 |
| H-ACMP | `acmp.get_tx_connection.if1` | acmp-cmd | 1 | 13.608 | 1,360,837 | 0 | 20 | 20 | yes | 639,163 | no | 186.392 of 200 |
| H-ACMP | `acmp.get_tx_state.if0` | acmp-cmd | 0 | 3.233 | 323,334 | 0 | 20 | 20 | yes | 1,676,666 | no | 196.767 of 200 |
| H-ACMP | `acmp.get_tx_state.if1` | acmp-cmd | 1 | 2.399 | 239,941 | 0 | 20 | 20 | yes | 1,760,059 | no | 197.601 of 200 |
| H-ACMP | `acmp.probe_tx.if0` | acmp-cmd | 0 | 4.707 | 470,692 | 0 | 20 | 20 | yes | 1,529,308 | no | 195.293 of 200 |
| H-ACMP | `acmp.probe_tx.if1` | acmp-cmd | 1 | 14.208 | 1,420,828 | 0 | 20 | 20 | yes | 579,172 | no | 185.792 of 200 |
| H-ACMP | `acmp.probe_tx_response.if0` | acmp-cmd | 0 | 7.825 | 782,453 | 0 | 20 | 20 | yes | 1,217,547 | no | 192.175 of 200 |
| H-ACMP | `acmp.probe_tx_response.if1` | acmp-cmd | 1 | 14.857 | 1,485,730 | 0 | 20 | 20 | yes | 514,270 | no | 185.143 of 200 |
| H-ACMP | `acmp.tmr_delay.if0` | acmp-noresp | 0 | 0.868 | 86,835 | 0 | 20 | 20 | yes | 1,913,165 | no | 199.132 of 200 |
| H-ACMP | `acmp.tmr_delay.if1` | acmp-noresp | 1 | 1.873 | 187,344 | 0 | 20 | 20 | yes | 1,812,656 | no | 198.127 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if0` | acmp-noresp | 0 | 2.167 | 216,672 | 0 | 20 | 20 | yes | 1,783,328 | no | 197.833 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if1` | acmp-noresp | 1 | 2.338 | 233,786 | 0 | 20 | 20 | yes | 1,766,214 | no | 197.662 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if0` | acmp-noresp | 0 | 2.399 | 239,929 | 0 | 20 | 20 | yes | 1,760,071 | no | 197.601 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if1` | acmp-noresp | 1 | 2.124 | 212,384 | 0 | 20 | 20 | yes | 1,787,616 | no | 197.876 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if0` | acmp-notk | 0 | 0.460 | 45,954 | 0 | 20 | 20 | yes | 1,954,046 | no | 199.540 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if1` | acmp-notk | 1 | 0.616 | 61,648 | 0 | 20 | 20 | yes | 1,938,352 | no | 199.384 of 200 |
| H-ACMP | `acmp.tmr_retry.if0` | acmp-noresp | 0 | 0.709 | 70,941 | 0 | 20 | 20 | yes | 1,929,059 | no | 199.291 of 200 |
| H-ACMP | `acmp.tmr_retry.if1` | acmp-noresp | 1 | 6.144 | 614,437 | 0 | 20 | 20 | yes | 1,385,563 | no | 193.856 of 200 |
| H-ACMP | `acmp.unbind_rx.if0` | acmp-cmd | 0 | 3.350 | 334,985 | 0 | 20 | 20 | yes | 1,665,015 | no | 196.650 of 200 |
| H-ACMP | `acmp.unbind_rx.if1` | acmp-cmd | 1 | 15.988 | 1,598,764 | 0 | 20 | 20 | yes | 401,236 | no | 184.012 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.first.if0` | backlog-adp-refill | 0 | 8.117 | 811,657 | 0 | 20 | 20 | yes | 1,188,343 | yes | 191.883 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.last.if0` | backlog-adp-refill | 0 | 73.920 | 7,392,044 | 0 | 20 | 20 | NO | -5,392,044 | yes | 126.080 of 200 |
| H-ACMP | `backlog-adp.service.acmp.first.if0` | backlog-adp | 0 | 8.117 | 811,657 | 0 | 20 | 20 | yes | 1,188,343 | yes | 191.883 of 200 |
| H-ACMP | `backlog-adp.service.acmp.last.if0` | backlog-adp | 0 | 73.640 | 7,363,958 | 0 | 20 | 20 | NO | -5,363,958 | yes | 126.360 of 200 |
| H-ACMP | `backlog-owed.service.acmp.first.if0` | backlog-owed | 0 | 6.533 | 653,303 | 0 | 20 | 20 | yes | 1,346,697 | yes | 193.467 of 200 |
| H-ACMP | `backlog-owed.service.acmp.last.if0` | backlog-owed | 0 | 36.446 | 3,644,574 | 0 | 20 | 20 | NO | -1,644,574 | yes | 163.554 of 200 |
| H-ACMP | `backlog.acmp_command.if0` | backlog | 0 | 37.912 | 3,791,215 | 0 | 20 | 20 | NO | -1,791,215 | yes | 162.088 of 200 |
| H-ACMP | `backlog.owed.if0` | backlog-owed | 0 | 90.262 | 9,026,153 | 0 | 20 | 20 | NO | -7,026,153 | yes | 109.738 of 200 |
| H-ACMP | `backlog.owed_behind0.if0` | backlog-owed | 0 | never | 36,339,967 | 0 | 20 | 20 | NO | -1 | yes | -163.400 of 200 |
| H-ACMP | `backlog.owed_behind1.if0` | backlog-owed | 0 | never | 36,339,892 | 0 | 20 | 20 | NO | -1 | yes | -163.399 of 200 |
| H-ACMP | `backlog.owed_behind2.if0` | backlog-owed | 0 | never | 36,339,817 | 0 | 20 | 20 | NO | -1 | yes | -163.398 of 200 |
| H-ACMP | `backlog.owed_behind3.if0` | backlog-owed | 0 | never | 36,339,742 | 0 | 20 | 20 | NO | -1 | yes | -163.397 of 200 |
| H-ACMP | `backlog.service.acmp.first.if0` | backlog | 0 | 9.010 | 900,954 | 0 | 20 | 20 | yes | 1,099,046 | yes | 190.990 of 200 |
| H-ACMP | `backlog.service.acmp.last.if0` | backlog | 0 | 42.136 | 4,213,602 | 0 | 20 | 20 | NO | -2,213,602 | yes | 157.864 of 200 |
| H-ACMP | `hooks-late-acmp.get_rx_state.if0` | hooks-late-acmp | 0 | 0.367 | 36,715 | 0 | 20 | 20 | yes | 1,963,285 | no | 199.633 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.first.if0` | hooks-load-notify | 0 | 5.709 | 570,936 | 0 | 20 | 20 | yes | 1,429,064 | yes | 194.291 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.last.if0` | hooks-load-notify | 0 | 36.977 | 3,697,709 | 0 | 20 | 20 | NO | -1,697,709 | yes | 163.023 of 200 |
| H-ADP | `adp.discover.if0` | adp-discover | 0 | 0.132 | 13,187 | 0 | 20 | 20 | yes | 1,986,813 | no | 1999.868 of 2000 |
| H-ADP | `adp.discover.if1` | adp-discover | 1 | 0.240 | 23,996 | 0 | 20 | 20 | yes | 1,976,004 | no | 1999.760 of 2000 |
| H-ADP | `adp.gm_change.if0` | adp-gm | 0 | 0.053 | 5,311 | 0 | 20 | 20 | yes | 1,994,689 | no | 1999.947 of 2000 |
| H-ADP | `adp.gm_change.if1` | adp-gm | 1 | 0.109 | 10,889 | 0 | 20 | 20 | yes | 1,989,111 | no | 1999.891 of 2000 |
| H-ADP | `adp.link_down.if0` | adp-link | 0 | 0.044 | 4,397 | 0 | 20 | 20 | yes | 1,995,603 | no | 1999.956 of 2000 |
| H-ADP | `adp.link_down.if1` | adp-link | 1 | 3.367 | 336,719 | 0 | 20 | 20 | yes | 1,663,281 | no | 1996.633 of 2000 |
| H-ADP | `adp.link_up.if0` | hooks-order-adp | 0 | 0.053 | 5,275 | 0 | 20 | 20 | yes | 1,994,725 | no | 1999.947 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-advertise | 0 | 0.053 | 5,275 | 0 | 20 | 20 | yes | 1,994,725 | no | 1999.947 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-link | 0 | 0.053 | 5,275 | 0 | 20 | 20 | yes | 1,994,725 | no | 1999.947 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-gm | 0 | 0.053 | 5,275 | 0 | 20 | 20 | yes | 1,994,725 | no | 1999.947 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-discover | 0 | 0.053 | 5,275 | 0 | 20 | 20 | yes | 1,994,725 | no | 1999.947 of 2000 |
| H-ADP | `adp.link_up.if0` | control | 0 | 0.053 | 5,275 | 0 | 20 | 20 | yes | 1,994,725 | no | 1999.947 of 2000 |
| H-ADP | `adp.link_up.if1` | hooks-order-adp | 1 | 0.557 | 55,675 | 0 | 20 | 20 | yes | 1,944,325 | no | 1999.443 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-advertise | 1 | 0.557 | 55,675 | 0 | 20 | 20 | yes | 1,944,325 | no | 1999.443 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-link | 1 | 0.557 | 55,675 | 0 | 20 | 20 | yes | 1,944,325 | no | 1999.443 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-gm | 1 | 0.557 | 55,675 | 0 | 20 | 20 | yes | 1,944,325 | no | 1999.443 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-discover | 1 | 0.557 | 55,675 | 0 | 20 | 20 | yes | 1,944,325 | no | 1999.443 of 2000 |
| H-ADP | `adp.link_up.if1` | control | 1 | 0.557 | 55,675 | 0 | 20 | 20 | yes | 1,944,325 | no | 1999.443 of 2000 |
| H-ADP | `adp.tmr_advertise.if0` | adp-advertise | 0 | 0.990 | 98,976 | 0 | 20 | 20 | yes | 1,901,024 | no | 1999.010 of 2000 |
| H-ADP | `adp.tmr_advertise.if1` | adp-advertise | 1 | 0.640 | 64,036 | 0 | 20 | 20 | yes | 1,935,964 | no | 1999.360 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | hooks-order-adp | 0 | 1.207 | 120,691 | 0 | 20 | 20 | yes | 1,879,309 | no | 1998.793 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-advertise | 0 | 1.207 | 120,691 | 0 | 20 | 20 | yes | 1,879,309 | no | 1998.793 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-link | 0 | 1.207 | 120,691 | 0 | 20 | 20 | yes | 1,879,309 | no | 1998.793 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-gm | 0 | 1.207 | 120,691 | 0 | 20 | 20 | yes | 1,879,309 | no | 1998.793 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-discover | 0 | 1.207 | 120,691 | 0 | 20 | 20 | yes | 1,879,309 | no | 1998.793 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | control | 0 | 1.207 | 120,691 | 0 | 20 | 20 | yes | 1,879,309 | no | 1998.793 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | hooks-order-adp | 1 | 0.964 | 96,412 | 0 | 20 | 20 | yes | 1,903,588 | no | 1999.036 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-advertise | 1 | 0.964 | 96,412 | 0 | 20 | 20 | yes | 1,903,588 | no | 1999.036 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-link | 1 | 0.964 | 96,412 | 0 | 20 | 20 | yes | 1,903,588 | no | 1999.036 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-gm | 1 | 0.964 | 96,412 | 0 | 20 | 20 | yes | 1,903,588 | no | 1999.036 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-discover | 1 | 0.964 | 96,412 | 0 | 20 | 20 | yes | 1,903,588 | no | 1999.036 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | control | 1 | 0.964 | 96,412 | 0 | 20 | 20 | yes | 1,903,588 | no | 1999.036 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.first.if0` | backlog-adp-refill | 0 | 8.107 | 810,745 | 0 | 20 | 20 | yes | 1,189,255 | yes | 1991.893 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.last.if0` | backlog-adp-refill | 0 | 33.964 | 3,396,432 | 0 | 20 | 20 | NO | -1,396,432 | yes | 1966.036 of 2000 |
| H-ADP | `backlog-adp.service.adp.first.if0` | backlog-adp | 0 | 8.107 | 810,745 | 0 | 20 | 20 | yes | 1,189,255 | yes | 1991.893 of 2000 |
| H-ADP | `backlog-adp.service.adp.last.if0` | backlog-adp | 0 | 44.152 | 4,415,181 | 0 | 20 | 20 | NO | -2,415,181 | yes | 1955.848 of 2000 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 6.576 | 657,562 | 0 | 20 | 20 | yes | 1,342,438 | yes | 1993.424 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if1` | backlog-owed | 1 | 27.065 | 2,706,475 | 0 | 20 | 20 | NO | -706,475 | yes | 1972.935 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 9.375 | 937,537 | 0 | 20 | 20 | yes | 1,062,463 | yes | 1990.625 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 9.052 | 905,213 | 0 | 20 | 20 | yes | 1,094,787 | yes | 1990.948 of 2000 |
| H-ADP | `backlog.service.adp.last.if1` | backlog | 1 | 31.496 | 3,149,560 | 0 | 20 | 20 | NO | -1,149,560 | yes | 1968.504 of 2000 |
| H-ADP | `control.discover.if0` | control | 0 | 0.132 | 13,187 | 0 | 20 | 20 | yes | 1,986,813 | no | 1999.868 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.first.if0` | hooks-load-notify | 0 | 5.742 | 574,155 | 0 | 20 | 20 | yes | 1,425,845 | yes | 1994.258 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.last.if1` | hooks-load-notify | 1 | 25.595 | 2,559,548 | 0 | 20 | 20 | NO | -559,548 | yes | 1974.405 of 2000 |
| H-AECP | `aecp.entity_available.if0` | aecp | 0 | 1.542 | 154,246 | 0 | 20 | 20 | yes | 1,845,754 | no | 238.458 of 240 |
| H-AECP | `aecp.entity_available.if1` | aecp | 1 | 1.540 | 153,965 | 0 | 20 | 20 | yes | 1,846,035 | no | 238.460 of 240 |
| H-AECP | `aecp.get_avb_info.if0` | aecp | 0 | 1.617 | 161,747 | 0 | 20 | 20 | yes | 1,838,253 | no | 238.383 of 240 |
| H-AECP | `aecp.get_avb_info.if1` | aecp | 1 | 1.615 | 161,466 | 0 | 20 | 20 | yes | 1,838,534 | no | 238.385 of 240 |
| H-AECP | `aecp.get_configuration.if0` | aecp | 0 | 1.521 | 152,144 | 0 | 20 | 20 | yes | 1,847,856 | no | 238.479 of 240 |
| H-AECP | `aecp.get_configuration.if1` | aecp | 1 | 1.519 | 151,863 | 0 | 20 | 20 | yes | 1,848,137 | no | 238.481 of 240 |
| H-AECP | `aecp.get_counters.if0` | aecp | 0 | 1.710 | 170,955 | 0 | 20 | 20 | yes | 1,829,045 | no | 238.290 of 240 |
| H-AECP | `aecp.get_counters.if1` | aecp | 1 | 1.707 | 170,674 | 0 | 20 | 20 | yes | 1,829,326 | no | 238.293 of 240 |
| H-AECP | `aecp.get_name.if0` | aecp | 0 | 1.612 | 161,186 | 0 | 20 | 20 | yes | 1,838,814 | no | 238.388 of 240 |
| H-AECP | `aecp.get_name.if1` | aecp | 1 | 1.609 | 160,905 | 0 | 20 | 20 | yes | 1,839,095 | no | 238.391 of 240 |
| H-AECP | `aecp.lock_entity.if0` | aecp | 0 | 1.803 | 180,299 | 0 | 20 | 20 | yes | 1,819,701 | no | 238.197 of 240 |
| H-AECP | `aecp.lock_entity.if1` | aecp | 1 | 1.803 | 180,318 | 0 | 20 | 20 | yes | 1,819,682 | no | 238.197 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if0` | aecp | 0 | 1.122 | 112,176 | 0 | 20 | 20 | yes | 1,887,824 | no | 238.878 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if1` | aecp | 1 | 1.119 | 111,895 | 0 | 20 | 20 | yes | 1,888,105 | no | 238.881 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if0` | aecp | 0 | 1.928 | 192,818 | 0 | 20 | 20 | yes | 1,807,182 | no | 238.072 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if1` | aecp | 1 | 1.925 | 192,534 | 0 | 20 | 20 | yes | 1,807,466 | no | 238.075 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if0` | aecp | 0 | 1.660 | 166,035 | 0 | 20 | 20 | yes | 1,833,965 | no | 238.340 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if1` | aecp | 1 | 1.658 | 165,754 | 0 | 20 | 20 | yes | 1,834,246 | no | 238.342 of 240 |
| H-AECP | `aecp.read_descriptor.t10.i9.c0.if0` | aecp | 0 | 1.659 | 165,946 | 0 | 20 | 20 | yes | 1,834,054 | no | 238.341 of 240 |
| H-AECP | `aecp.read_descriptor.t12.i0.c0.if0` | aecp | 0 | 1.642 | 164,235 | 0 | 20 | 20 | yes | 1,835,765 | no | 238.358 of 240 |
| H-AECP | `aecp.read_descriptor.t13.i0.c0.if0` | aecp | 0 | 2.118 | 211,811 | 0 | 20 | 20 | yes | 1,788,189 | no | 237.882 of 240 |
| H-AECP | `aecp.read_descriptor.t14.i7.c0.if0` | aecp | 0 | 1.585 | 158,510 | 0 | 20 | 20 | yes | 1,841,490 | no | 238.415 of 240 |
| H-AECP | `aecp.read_descriptor.t15.i7.c0.if0` | aecp | 0 | 1.591 | 159,118 | 0 | 20 | 20 | yes | 1,840,882 | no | 238.409 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if0` | aecp | 0 | 1.715 | 171,455 | 0 | 20 | 20 | yes | 1,828,545 | no | 238.285 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if1` | aecp | 1 | 1.712 | 171,174 | 0 | 20 | 20 | yes | 1,828,826 | no | 238.288 of 240 |
| H-AECP | `aecp.read_descriptor.t20.i71.c0.if0` | aecp | 0 | 1.741 | 174,092 | 0 | 20 | 20 | yes | 1,825,908 | no | 238.259 of 240 |
| H-AECP | `aecp.read_descriptor.t26.i0.c0.if0` | aecp | 0 | 1.762 | 176,160 | 0 | 20 | 20 | yes | 1,823,840 | no | 238.238 of 240 |
| H-AECP | `aecp.read_descriptor.t36.i0.c0.if0` | aecp | 0 | 1.742 | 174,151 | 0 | 20 | 20 | yes | 1,825,849 | no | 238.258 of 240 |
| H-AECP | `aecp.read_descriptor.t5.i8.c0.if0` | aecp | 0 | 1.719 | 171,913 | 0 | 20 | 20 | yes | 1,828,087 | no | 238.281 of 240 |
| H-AECP | `aecp.read_descriptor.t6.i8.c0.if0` | aecp | 0 | 1.726 | 172,597 | 0 | 20 | 20 | yes | 1,827,403 | no | 238.274 of 240 |
| H-AECP | `aecp.read_descriptor.t9.i0.c0.if0` | aecp | 0 | 1.671 | 167,069 | 0 | 20 | 20 | yes | 1,832,931 | no | 238.329 of 240 |
| H-AECP | `aecp.register_unsolicited.if0` | aecp | 0 | 1.118 | 111,763 | 0 | 20 | 20 | yes | 1,888,237 | no | 238.882 of 240 |
| H-AECP | `aecp.register_unsolicited.if1` | aecp | 1 | 1.113 | 111,295 | 0 | 20 | 20 | yes | 1,888,705 | no | 238.887 of 240 |
| H-AECP | `aecp.set_name.if0` | aecp | 0 | 2.396 | 239,577 | 0 | 20 | 20 | yes | 1,760,423 | no | 237.604 of 240 |
| H-AECP | `aecp.set_name.if1` | aecp | 1 | 2.164 | 216,362 | 0 | 20 | 20 | yes | 1,783,638 | no | 237.836 of 240 |
| H-AECP | `aecp.unknown_command.if0` | aecp | 0 | 1.517 | 151,689 | 0 | 20 | 20 | yes | 1,848,311 | no | 238.483 of 240 |
| H-AECP | `aecp.unknown_command.if1` | aecp | 1 | 1.784 | 178,441 | 0 | 20 | 20 | yes | 1,821,559 | no | 238.216 of 240 |
| H-AECP | `aecp.unlock_entity.if0` | aecp | 0 | 1.803 | 180,301 | 0 | 20 | 20 | yes | 1,819,699 | no | 238.197 of 240 |
| H-AECP | `aecp.unlock_entity.if1` | aecp | 1 | 1.803 | 180,320 | 0 | 20 | 20 | yes | 1,819,680 | no | 238.197 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.first.if0` | backlog-adp-refill | 0 | 8.152 | 815,242 | 0 | 20 | 20 | yes | 1,184,758 | yes | 231.848 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.last.if1` | backlog-adp-refill | 1 | 205.203 | 20,520,283 | 0 | 20 | 20 | NO | -18,520,283 | yes | 34.797 of 240 |
| H-AECP | `backlog-adp.service.aecp.first.if0` | backlog-adp | 0 | 8.152 | 815,242 | 0 | 20 | 20 | yes | 1,184,758 | yes | 231.848 of 240 |
| H-AECP | `backlog-adp.service.aecp.last.if1` | backlog-adp | 1 | 204.920 | 20,492,015 | 0 | 20 | 20 | NO | -18,492,015 | yes | 35.080 of 240 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 6.569 | 656,888 | 0 | 20 | 20 | yes | 1,343,112 | yes | 233.431 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if1` | backlog-owed | 1 | 102.264 | 10,226,351 | 0 | 20 | 20 | NO | -8,226,351 | yes | 137.736 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 9.045 | 904,539 | 0 | 20 | 20 | yes | 1,095,461 | yes | 230.955 of 240 |
| H-AECP | `backlog.service.aecp.last.if1` | backlog | 1 | 79.584 | 7,958,439 | 0 | 20 | 20 | NO | -5,958,439 | yes | 160.416 of 240 |
| H-AECP | `hooks-late-aecp.read_descriptor.if0` | hooks-late-aecp | 0 | 1.901 | 190,147 | 0 | 20 | 20 | yes | 1,809,853 | no | 238.099 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.first.if0` | hooks-load-notify | 0 | 5.700 | 570,046 | 0 | 20 | 20 | yes | 1,429,954 | yes | 234.300 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.last.if0` | hooks-load-notify | 0 | 85.846 | 8,584,571 | 0 | 20 | 20 | NO | -6,584,571 | yes | 154.154 of 240 |
| H-DISC | `acmp.entity_available.if0` | acmp-disc | 0 | 15.129 | 1,512,936 | 0 | 20 | 20 | yes | 487,064 | no | 184.871 of 200 |
| H-DISC | `acmp.entity_available.if1` | acmp-disc | 1 | 15.927 | 1,592,735 | 0 | 20 | 20 | yes | 407,265 | no | 184.073 of 200 |
| H-DISC | `acmp.entity_departing.if0` | acmp-disc | 0 | 1.665 | 166,492 | 0 | 20 | 20 | yes | 1,833,508 | no | 198.335 of 200 |
| H-DISC | `acmp.entity_departing.if1` | acmp-disc | 1 | 2.435 | 243,531 | 0 | 20 | 20 | yes | 1,756,469 | no | 197.565 of 200 |
| H-DISC | `acmp.tmr_no_adp.if0` | acmp-disc | 0 | 2.450 | 244,986 | 0 | 20 | 20 | yes | 1,755,014 | no | 197.550 of 200 |
| H-DISC | `acmp.tmr_no_adp.if1` | acmp-disc | 1 | 1.251 | 125,120 | 0 | 20 | 20 | yes | 1,874,880 | no | 198.749 of 200 |
| H-DISC | `backlog.adp_available.if0` | backlog-adp | 0 | 37.316 | 3,731,571 | 0 | 20 | 20 | NO | -1,731,571 | yes | 162.684 of 200 |
| H-DISC | `backlog.adp_available_refill.if0` | backlog-adp-refill | 0 | 27.512 | 2,751,157 | 0 | 20 | 20 | NO | -751,157 | yes | 172.488 of 200 |
| H-DISC | `hooks-disc-aging.available.if0` | hooks-disc-aging | 0 | 10.054 | 1,005,369 | 0 | 20 | 20 | yes | 994,631 | no | 189.946 of 200 |
| H-DISC | `hooks-disc-aging.available.if1` | hooks-disc-aging | 1 | 11.243 | 1,124,270 | 0 | 20 | 20 | yes | 875,730 | no | 188.757 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if0` | hooks-disc-aging | 0 | 5.261 | 526,140 | 0 | 20 | 20 | yes | 1,473,860 | no | 194.739 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if1` | hooks-disc-aging | 1 | 4.018 | 401,808 | 0 | 20 | 20 | yes | 1,598,192 | no | 195.982 of 200 |
| H-DISC | `hooks-late-disc.entity_departing.if0` | hooks-late-disc | 0 | 0.296 | 29,598 | 0 | 20 | 20 | yes | 1,970,402 | no | 199.704 of 200 |
| H-MAAP | `backlog-adp-refill.service.maap.first.if0` | backlog-adp-refill | 0 | 8.142 | 814,202 | 0 | 20 | 20 | yes | 1,185,798 | yes | 491.858 of 500 |
| H-MAAP | `backlog-adp-refill.service.maap.last.if0` | backlog-adp-refill | 0 | 43.486 | 4,348,609 | 0 | 20 | 20 | NO | -2,348,609 | yes | 456.514 of 500 |
| H-MAAP | `backlog-adp.service.maap.first.if0` | backlog-adp | 0 | 8.142 | 814,202 | 0 | 20 | 20 | yes | 1,185,798 | yes | 491.858 of 500 |
| H-MAAP | `backlog-adp.service.maap.last.if0` | backlog-adp | 0 | 44.189 | 4,418,857 | 0 | 20 | 20 | NO | -2,418,857 | yes | 455.811 of 500 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 6.558 | 655,848 | 0 | 20 | 20 | yes | 1,344,152 | yes | 493.442 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 27.050 | 2,704,980 | 0 | 20 | 20 | NO | -704,980 | yes | 472.950 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 9.035 | 903,499 | 0 | 20 | 20 | yes | 1,096,501 | yes | 490.965 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 31.481 | 3,148,065 | 0 | 20 | 20 | NO | -1,148,065 | yes | 468.519 of 500 |
| H-MAAP | `hooks-late-maap.defend.if0` | hooks-late-maap | 0 | 0.418 | 41,798 | 0 | 20 | 20 | yes | 1,958,202 | no | 499.582 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.first.if0` | hooks-load-notify | 0 | 5.735 | 573,481 | 0 | 20 | 20 | yes | 1,426,519 | yes | 494.265 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.last.if0` | hooks-load-notify | 0 | 25.591 | 2,559,093 | 0 | 20 | 20 | NO | -559,093 | yes | 474.409 of 500 |
| H-MAAP | `maap.announce.if0` | maap | 0 | 1.114 | 111,447 | 0 | 20 | 20 | yes | 1,888,553 | no | 498.886 of 500 |
| H-MAAP | `maap.announce.if1` | maap | 1 | 1.757 | 175,729 | 0 | 20 | 20 | yes | 1,824,271 | no | 498.243 of 500 |
| H-MAAP | `maap.defend.if0` | maap | 0 | 0.689 | 68,870 | 0 | 20 | 20 | yes | 1,931,130 | no | 499.311 of 500 |
| H-MAAP | `maap.defend.if1` | maap | 1 | 0.418 | 41,798 | 0 | 20 | 20 | yes | 1,958,202 | no | 499.582 of 500 |
| H-MAAP | `maap.probe1.if0` | maap | 0 | 0.488 | 48,757 | 0 | 20 | 20 | yes | 1,951,243 | no | 499.512 of 500 |
| H-MAAP | `maap.probe1.if1` | maap | 1 | 0.493 | 49,263 | 0 | 20 | 20 | yes | 1,950,737 | no | 499.507 of 500 |
| H-MAAP | `maap.probe2.if0` | maap | 0 | 0.873 | 87,324 | 0 | 20 | 20 | yes | 1,912,676 | no | 499.127 of 500 |
| H-MAAP | `maap.probe2.if1` | maap | 1 | 0.941 | 94,095 | 0 | 20 | 20 | yes | 1,905,905 | no | 499.059 of 500 |
| H-MAAP | `maap.probe3.if0` | maap | 0 | 1.058 | 105,753 | 0 | 20 | 20 | yes | 1,894,247 | no | 498.942 of 500 |
| H-MAAP | `maap.probe3.if1` | maap | 1 | 1.528 | 152,776 | 0 | 20 | 20 | yes | 1,847,224 | no | 498.472 of 500 |
| H-MAAP | `maap.probe4.if0` | maap | 0 | 1.027 | 102,723 | 0 | 20 | 20 | yes | 1,897,277 | no | 498.973 of 500 |
| H-MAAP | `maap.probe4.if1` | maap | 1 | 1.670 | 167,005 | 0 | 20 | 20 | yes | 1,832,995 | no | 498.330 of 500 |
| H-NOTIFY | `aecp_fanout.lock_entity.if0` | aecp-fanout | 0 | 4.830 | 482,990 | 0 | 20 | 20 | yes | 1,517,010 | no | 235.170 of 240 |
| H-NOTIFY | `aecp_fanout.lock_entity.if1` | aecp-fanout | 1 | 4.801 | 480,051 | 0 | 20 | 20 | yes | 1,519,949 | no | 235.199 of 240 |
| H-NOTIFY | `aecp_fanout.set_clock_source.if0` | aecp-fanout | 0 | 5.026 | 502,644 | 0 | 20 | 20 | yes | 1,497,356 | no | 234.974 of 240 |
| H-NOTIFY | `aecp_fanout.set_clock_source.if1` | aecp-fanout | 1 | 4.791 | 479,063 | 0 | 20 | 20 | yes | 1,520,937 | no | 235.209 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_off.if0` | aecp-fanout | 0 | 4.848 | 484,785 | 0 | 20 | 20 | yes | 1,515,215 | no | 235.152 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_off.if1` | aecp-fanout | 1 | 4.595 | 459,531 | 0 | 20 | 20 | yes | 1,540,469 | no | 235.405 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_on.if0` | aecp-fanout | 0 | 4.587 | 458,650 | 0 | 20 | 20 | yes | 1,541,350 | no | 235.413 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_on.if1` | aecp-fanout | 1 | 4.618 | 461,846 | 0 | 20 | 20 | yes | 1,538,154 | no | 235.382 of 240 |
| H-NOTIFY | `aecp_fanout.set_name.if0` | aecp-fanout | 0 | 6.855 | 685,483 | 0 | 20 | 20 | yes | 1,314,517 | no | 233.145 of 240 |
| H-NOTIFY | `aecp_fanout.set_name.if1` | aecp-fanout | 1 | 6.575 | 657,534 | 0 | 20 | 20 | yes | 1,342,466 | no | 233.425 of 240 |
| H-NOTIFY | `aecp_fanout.set_sampling_rate.if0` | aecp-fanout | 0 | 4.440 | 443,998 | 0 | 20 | 20 | yes | 1,556,002 | no | 235.560 of 240 |
| H-NOTIFY | `aecp_fanout.unlock_entity.if0` | aecp-fanout | 0 | 4.813 | 481,324 | 0 | 20 | 20 | yes | 1,518,676 | no | 235.187 of 240 |
| H-NOTIFY | `aecp_fanout.unlock_entity.if1` | aecp-fanout | 1 | 4.864 | 486,385 | 0 | 20 | 20 | yes | 1,513,615 | no | 235.136 of 240 |
| H-NOTIFY | `hooks-late-notify.set_name.if0` | hooks-late-notify | 0 | 6.855 | 685,483 | 0 | 20 | 20 | yes | 1,314,517 | no | 233.145 of 240 |
| H-NOTIFY | `hooks-load-notify.set_name.if0` | hooks-load-notify | 0 | 84.071 | 8,407,073 | 0 | 20 | 20 | NO | -6,407,073 | yes | 155.929 of 240 |
| H-SRP | `backlog-adp-refill.service.srp.first.if0` | backlog-adp-refill | 0 | never | 56,749,684 | 0 | 18 | 20 | NO | -1 | yes | -387.497 of 180 |
| H-SRP | `backlog-adp-refill.service.srp.last.if1` | backlog-adp-refill | 1 | never | 56,747,669 | 0 | 18 | 20 | NO | -1 | yes | -387.477 of 180 |
| H-SRP | `backlog-adp.service.srp.first.if0` | backlog-adp | 0 | never | 53,735,182 | 0 | 18 | 20 | NO | -1 | yes | -357.352 of 180 |
| H-SRP | `backlog-adp.service.srp.last.if1` | backlog-adp | 1 | never | 53,733,167 | 0 | 18 | 20 | NO | -1 | yes | -357.332 of 180 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 14.440 | 1,444,030 | 0 | 18 | 20 | yes | 355,970 | yes | 165.560 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if1` | backlog-owed | 1 | 80.929 | 8,092,946 | 0 | 18 | 20 | NO | -6,292,946 | yes | 99.071 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 25.212 | 2,521,232 | 0 | 18 | 20 | NO | -721,232 | yes | 154.788 of 180 |
| H-SRP | `backlog.service.srp.last.if1` | backlog | 1 | 89.100 | 8,910,025 | 0 | 18 | 20 | NO | -7,110,025 | yes | 90.900 of 180 |
| H-SRP | `hooks-late-srp.listener_ready.if0` | hooks-late-srp | 0 | 2.141 | 214,104 | 0 | 18 | 20 | yes | 1,585,896 | no | 177.859 of 180 |
| H-SRP | `hooks-load-notify.service.srp.first.if0` | hooks-load-notify | 0 | 25.590 | 2,559,028 | 0 | 18 | 20 | NO | -759,028 | yes | 154.410 of 180 |
| H-SRP | `hooks-load-notify.service.srp.last.if1` | hooks-load-notify | 1 | 102.249 | 10,224,887 | 0 | 18 | 20 | NO | -8,424,887 | yes | 77.751 of 180 |
| H-SRP | `srp.domain.if0` | srp | 0 | 4.974 | 497,433 | 200 | 218 | 220 | yes | 21,302,567 | no | -24.974 of 180 |
| H-SRP | `srp.domain.if1` | srp | 1 | 5.068 | 506,765 | 200 | 218 | 220 | yes | 21,293,235 | no | -25.068 of 180 |
| H-SRP | `srp.listener_ready.if0` | srp | 0 | 2.133 | 213,349 | 0 | 18 | 20 | yes | 1,586,651 | no | 177.867 of 180 |
| H-SRP | `srp.listener_ready.if1` | srp | 1 | 2.501 | 250,109 | 0 | 18 | 20 | yes | 1,549,891 | no | 177.499 of 180 |
| H-SRP | `srp.malformed.if0` | srp | 0 | 1.626 | 162,583 | 0 | 18 | 20 | yes | 1,637,417 | no | 178.374 of 180 |
| H-SRP | `srp.malformed.if1` | srp | 1 | 1.674 | 167,414 | 0 | 18 | 20 | yes | 1,632,586 | no | 178.326 of 180 |
| H-SRP | `srp.startup.if0` | srp | 0 | 3.985 | 398,506 | 0 | 18 | 20 | yes | 1,401,494 | no | 176.015 of 180 |
| H-SRP | `srp.startup.if1` | srp | 1 | 4.043 | 404,257 | 0 | 18 | 20 | yes | 1,395,743 | no | 175.957 of 180 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- none

Findings:

- LATE H-NOTIFY: hooks-load-notify.set_name.if0: 84.071 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ADP: hooks-load-notify.service.adp.last.if1: 25.595 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ACMP: hooks-load-notify.service.acmp.last.if0: 36.977 ms against its bound 20 ms (hooks-load-notify)
- LATE H-AECP: hooks-load-notify.service.aecp.last.if0: 85.846 ms against its bound 20 ms (hooks-load-notify)
- LATE H-MAAP: hooks-load-notify.service.maap.last.if0: 25.591 ms against its bound 20 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.first.if0: 25.590 ms against its bound 18 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.last.if1: 102.249 ms against its bound 18 ms (hooks-load-notify)
- LATE H-ACMP: backlog.acmp_command.if0: 37.912 ms against its bound 20 ms (backlog)
- LATE H-ADP: backlog.service.adp.last.if1: 31.496 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 42.136 ms against its bound 20 ms (backlog)
- LATE H-AECP: backlog.service.aecp.last.if1: 79.584 ms against its bound 20 ms (backlog)
- LATE H-MAAP: backlog.service.maap.last.if0: 31.481 ms against its bound 20 ms (backlog)
- LATE H-SRP: backlog.service.srp.first.if0: 25.212 ms against its bound 18 ms (backlog)
- LATE H-SRP: backlog.service.srp.last.if1: 89.100 ms against its bound 18 ms (backlog)
- LATE H-DISC: backlog.adp_available.if0: 37.316 ms against its bound 20 ms (backlog-adp)
- LATE H-ADP: backlog-adp.service.adp.last.if0: 44.152 ms against its bound 20 ms (backlog-adp)
- LATE H-ACMP: backlog-adp.service.acmp.last.if0: 73.640 ms against its bound 20 ms (backlog-adp)
- LATE H-AECP: backlog-adp.service.aecp.last.if1: 204.920 ms against its bound 20 ms (backlog-adp)
- LATE H-MAAP: backlog-adp.service.maap.last.if0: 44.189 ms against its bound 20 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.first.if0: never served against its bound 18 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.last.if1: never served against its bound 18 ms (backlog-adp)
- LATE H-DISC: backlog.adp_available_refill.if0: 27.512 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-ADP: backlog-adp-refill.service.adp.last.if0: 33.964 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-ACMP: backlog-adp-refill.service.acmp.last.if0: 73.920 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-AECP: backlog-adp-refill.service.aecp.last.if1: 205.203 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-MAAP: backlog-adp-refill.service.maap.last.if0: 43.486 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.first.if0: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.last.if1: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-ACMP: backlog.owed.if0: 90.262 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind0.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind1.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind2.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind3.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ADP: backlog-owed.service.adp.last.if1: 27.065 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog-owed.service.acmp.last.if0: 36.446 ms against its bound 20 ms (backlog-owed)
- LATE H-AECP: backlog-owed.service.aecp.last.if1: 102.264 ms against its bound 20 ms (backlog-owed)
- LATE H-MAAP: backlog-owed.service.maap.last.if0: 27.050 ms against its bound 20 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.last.if1: 80.929 ms against its bound 18 ms (backlog-owed)
