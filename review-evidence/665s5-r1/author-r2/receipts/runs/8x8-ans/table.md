### 8x8, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm answering

Graded against the bounds in the tree at this base. The amended column gives the owner's decisions of 2026-11-06 on #665, for information: it grades nothing, and this harness re-grades when #810 merges.

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Amended service bound, ms, for information | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|---:|
| H-ADP | 46 | 5 | 0 | 3.367 (20), `adp.link_down.if1`, margin 1996.6 of 2000 | 31.496 (20) **over its bound**, `backlog.service.adp.last.if1`, margin 1968.5 of 2000 | 20 | 4 (0) | 0 |
| H-DISC | 13 | 1 | 0 | 1.340 (20), `acmp.tmr_no_adp.if1`, margin 198.7 of 200 | 21.788 (20) **over its bound**, `backlog.adp_available.if0`, margin 178.2 of 200 | 20 | 1 (1) | 0 |
| H-ACMP | 45 | 12 | 0 | 1.636 (20), `acmp.tmr_no_resp1.if1`, margin 198.4 of 200 | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -163.4 of 200 | 20 | 79 (0) | 0 |
| H-AECP | 52 | 6 | 0 | 2.396 (20), `aecp.set_name.if0`, margin 237.6 of 240 | 102.264 (20) **over its bound**, `backlog-owed.service.aecp.last.if1`, margin 137.7 of 240 | 20 | 14 (0) | 0 |
| H-NOTIFY | 15 | 1 | 0 | 6.855 (20), `aecp_fanout.set_name.if0`, margin 233.1 of 240 | 84.071 (20) **over its bound**, `hooks-load-notify.set_name.if0`, margin 155.9 of 240 | 20 | 15 (0) | 0 |
| H-COUNTERS | 23 | 20 | 0 | 218.712 (20) **over its bound**, `counters.all.if0`, margin 781.3 of 1000 | 36.623 (20) **over its bound**, `counters.loaded.if0`, margin 963.4 of 1000 | 20, 60 | 32 (0) | 0 |
| H-MAAP | 25 | 6 | 0 | 1.757 (20), `maap.announce.if1`, margin 498.2 of 500 | 31.481 (20) **over its bound**, `backlog.service.maap.last.if0`, margin 468.5 of 500 | 20 | 48 (0) | 0 |
| H-SRP | 21 | 9 | 0 | 4.043 (18), `srp.startup.if1`, margin 176.0 of 180 | 102.307 (18) **over its bound**, `hooks-load-counters.service.srp.last.if1`, margin 77.7 of 180 | 20 | 2 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound at this base, ms | Amended bound, ms, for information | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-ACMP | `acmp.bind_rx.if0` | acmp-cmd | 0 | 0.635 | 63,461 | 0 | 20 | 20 | yes | 1,936,539 | no | 199.365 of 200 |
| H-ACMP | `acmp.bind_rx.if1` | acmp-cmd | 1 | 0.640 | 63,988 | 0 | 20 | 20 | yes | 1,936,012 | no | 199.360 of 200 |
| H-ACMP | `acmp.disconnect_tx.if0` | acmp-cmd | 0 | 0.361 | 36,057 | 0 | 20 | 20 | yes | 1,963,943 | no | 199.639 of 200 |
| H-ACMP | `acmp.disconnect_tx.if1` | acmp-cmd | 1 | 0.361 | 36,057 | 0 | 20 | 20 | yes | 1,963,943 | no | 199.639 of 200 |
| H-ACMP | `acmp.get_rx_state.if0` | acmp-cmd | 0 | 0.368 | 36,839 | 0 | 20 | 20 | yes | 1,963,161 | no | 199.632 of 200 |
| H-ACMP | `acmp.get_rx_state.if1` | acmp-cmd | 1 | 0.368 | 36,850 | 0 | 20 | 20 | yes | 1,963,150 | no | 199.631 of 200 |
| H-ACMP | `acmp.get_tx_connection.if0` | acmp-cmd | 0 | 0.360 | 35,961 | 0 | 20 | 20 | yes | 1,964,039 | no | 199.640 of 200 |
| H-ACMP | `acmp.get_tx_connection.if1` | acmp-cmd | 1 | 0.360 | 35,961 | 0 | 20 | 20 | yes | 1,964,039 | no | 199.640 of 200 |
| H-ACMP | `acmp.get_tx_state.if0` | acmp-cmd | 0 | 0.383 | 38,284 | 0 | 20 | 20 | yes | 1,961,716 | no | 199.617 of 200 |
| H-ACMP | `acmp.get_tx_state.if1` | acmp-cmd | 1 | 0.383 | 38,284 | 0 | 20 | 20 | yes | 1,961,716 | no | 199.617 of 200 |
| H-ACMP | `acmp.probe_tx.if0` | acmp-cmd | 0 | 0.381 | 38,096 | 0 | 20 | 20 | yes | 1,961,904 | no | 199.619 of 200 |
| H-ACMP | `acmp.probe_tx.if1` | acmp-cmd | 1 | 0.381 | 38,096 | 0 | 20 | 20 | yes | 1,961,904 | no | 199.619 of 200 |
| H-ACMP | `acmp.probe_tx_response.if0` | acmp-cmd | 0 | 0.199 | 19,895 | 0 | 20 | 20 | yes | 1,980,105 | no | 199.801 of 200 |
| H-ACMP | `acmp.probe_tx_response.if1` | acmp-cmd | 1 | 0.204 | 20,415 | 0 | 20 | 20 | yes | 1,979,585 | no | 199.796 of 200 |
| H-ACMP | `acmp.tmr_delay.if0` | acmp-noresp | 0 | 0.413 | 41,286 | 0 | 20 | 20 | yes | 1,958,714 | no | 199.587 of 200 |
| H-ACMP | `acmp.tmr_delay.if1` | acmp-noresp | 1 | 0.379 | 37,937 | 0 | 20 | 20 | yes | 1,962,063 | no | 199.621 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if0` | acmp-noresp | 0 | 1.464 | 146,403 | 0 | 20 | 20 | yes | 1,853,597 | no | 198.536 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if1` | acmp-noresp | 1 | 1.636 | 163,579 | 0 | 20 | 20 | yes | 1,836,421 | no | 198.364 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if0` | acmp-noresp | 0 | 1.516 | 151,551 | 0 | 20 | 20 | yes | 1,848,449 | no | 198.484 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if1` | acmp-noresp | 1 | 1.240 | 124,006 | 0 | 20 | 20 | yes | 1,875,994 | no | 198.760 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if0` | acmp-notk | 0 | 0.858 | 85,755 | 0 | 20 | 20 | yes | 1,914,245 | no | 199.142 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if1` | acmp-notk | 1 | 0.499 | 49,874 | 0 | 20 | 20 | yes | 1,950,126 | no | 199.501 of 200 |
| H-ACMP | `acmp.tmr_retry.if0` | acmp-noresp | 0 | 0.468 | 46,819 | 0 | 20 | 20 | yes | 1,953,181 | no | 199.532 of 200 |
| H-ACMP | `acmp.tmr_retry.if1` | acmp-noresp | 1 | 0.157 | 15,708 | 0 | 20 | 20 | yes | 1,984,292 | no | 199.843 of 200 |
| H-ACMP | `acmp.unbind_rx.if0` | acmp-cmd | 0 | 0.448 | 44,784 | 0 | 20 | 20 | yes | 1,955,216 | no | 199.552 of 200 |
| H-ACMP | `acmp.unbind_rx.if1` | acmp-cmd | 1 | 0.453 | 45,307 | 0 | 20 | 20 | yes | 1,954,693 | no | 199.547 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.first.if0` | backlog-adp-refill | 0 | 6.025 | 602,484 | 0 | 20 | 20 | yes | 1,397,516 | yes | 193.975 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.last.if0` | backlog-adp-refill | 0 | 40.157 | 4,015,734 | 0 | 20 | 20 | NO | -2,015,734 | yes | 159.843 of 200 |
| H-ACMP | `backlog-adp.service.acmp.first.if0` | backlog-adp | 0 | 6.025 | 602,484 | 0 | 20 | 20 | yes | 1,397,516 | yes | 193.975 of 200 |
| H-ACMP | `backlog-adp.service.acmp.last.if0` | backlog-adp | 0 | 39.318 | 3,931,828 | 0 | 20 | 20 | NO | -1,931,828 | yes | 160.682 of 200 |
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
| H-ACMP | `hooks-load-counters.service.acmp.first.if0` | hooks-load-counters | 0 | 5.699 | 569,896 | 0 | 20 | 20 | yes | 1,430,104 | yes | 194.301 of 200 |
| H-ACMP | `hooks-load-counters.service.acmp.last.if0` | hooks-load-counters | 0 | 46.667 | 4,666,746 | 0 | 20 | 20 | NO | -2,666,746 | yes | 153.333 of 200 |
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
| H-ADP | `backlog-adp-refill.service.adp.first.if0` | backlog-adp-refill | 0 | 6.016 | 601,572 | 0 | 20 | 20 | yes | 1,398,428 | yes | 1993.984 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.last.if0` | backlog-adp-refill | 0 | 4.104 | 410,388 | 0 | 20 | 20 | yes | 1,589,612 | yes | 1995.896 of 2000 |
| H-ADP | `backlog-adp.service.adp.first.if0` | backlog-adp | 0 | 6.016 | 601,572 | 0 | 20 | 20 | yes | 1,398,428 | yes | 1993.984 of 2000 |
| H-ADP | `backlog-adp.service.adp.last.if0` | backlog-adp | 0 | 27.734 | 2,773,436 | 0 | 20 | 20 | NO | -773,436 | yes | 1972.266 of 2000 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 6.576 | 657,562 | 0 | 20 | 20 | yes | 1,342,438 | yes | 1993.424 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if1` | backlog-owed | 1 | 27.065 | 2,706,475 | 0 | 20 | 20 | NO | -706,475 | yes | 1972.935 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 9.375 | 937,537 | 0 | 20 | 20 | yes | 1,062,463 | yes | 1990.625 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 9.052 | 905,213 | 0 | 20 | 20 | yes | 1,094,787 | yes | 1990.948 of 2000 |
| H-ADP | `backlog.service.adp.last.if1` | backlog | 1 | 31.496 | 3,149,560 | 0 | 20 | 20 | NO | -1,149,560 | yes | 1968.504 of 2000 |
| H-ADP | `control.discover.if0` | control | 0 | 0.132 | 13,187 | 0 | 20 | 20 | yes | 1,986,813 | no | 1999.868 of 2000 |
| H-ADP | `hooks-load-counters.service.adp.first.if0` | hooks-load-counters | 0 | 5.742 | 574,155 | 0 | 20 | 20 | yes | 1,425,845 | yes | 1994.258 of 2000 |
| H-ADP | `hooks-load-counters.service.adp.last.if1` | hooks-load-counters | 1 | 26.824 | 2,682,391 | 0 | 20 | 20 | NO | -682,391 | yes | 1973.176 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.first.if0` | hooks-load-notify | 0 | 5.742 | 574,155 | 0 | 20 | 20 | yes | 1,425,845 | yes | 1994.258 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.last.if1` | hooks-load-notify | 1 | 25.595 | 2,559,548 | 0 | 20 | 20 | NO | -559,548 | yes | 1974.405 of 2000 |
| H-AECP | `aecp.entity_available.if0` | aecp | 0 | 1.542 | 154,246 | 0 | 20 | 20 | yes | 1,845,754 | no | 238.458 of 240 |
| H-AECP | `aecp.entity_available.if1` | aecp | 1 | 1.540 | 153,965 | 0 | 20 | 20 | yes | 1,846,035 | no | 238.460 of 240 |
| H-AECP | `aecp.get_avb_info.if0` | aecp | 0 | 1.617 | 161,747 | 0 | 20 | 20 | yes | 1,838,253 | no | 238.383 of 240 |
| H-AECP | `aecp.get_avb_info.if1` | aecp | 1 | 1.615 | 161,466 | 0 | 20 | 20 | yes | 1,838,534 | no | 238.385 of 240 |
| H-AECP | `aecp.get_configuration.if0` | aecp | 0 | 1.521 | 152,144 | 0 | 20 | 20 | yes | 1,847,856 | no | 238.479 of 240 |
| H-AECP | `aecp.get_configuration.if1` | aecp | 1 | 1.519 | 151,863 | 0 | 20 | 20 | yes | 1,848,137 | no | 238.481 of 240 |
| H-AECP | `aecp.get_counters.if0` | aecp | 0 | 2.247 | 224,707 | 0 | 20 | 20 | yes | 1,775,293 | no | 237.753 of 240 |
| H-AECP | `aecp.get_counters.if1` | aecp | 1 | 2.244 | 224,426 | 0 | 20 | 20 | yes | 1,775,574 | no | 237.756 of 240 |
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
| H-AECP | `backlog-adp-refill.service.aecp.first.if0` | backlog-adp-refill | 0 | 6.061 | 606,069 | 0 | 20 | 20 | yes | 1,393,931 | yes | 233.939 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.last.if1` | backlog-adp-refill | 1 | 86.299 | 8,629,948 | 0 | 20 | 20 | NO | -6,629,948 | yes | 153.701 of 240 |
| H-AECP | `backlog-adp.service.aecp.first.if0` | backlog-adp | 0 | 6.061 | 606,069 | 0 | 20 | 20 | yes | 1,393,931 | yes | 233.939 of 240 |
| H-AECP | `backlog-adp.service.aecp.last.if1` | backlog-adp | 1 | 86.604 | 8,660,394 | 0 | 20 | 20 | NO | -6,660,394 | yes | 153.396 of 240 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 6.569 | 656,888 | 0 | 20 | 20 | yes | 1,343,112 | yes | 233.431 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if1` | backlog-owed | 1 | 102.264 | 10,226,351 | 0 | 20 | 20 | NO | -8,226,351 | yes | 137.736 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 9.045 | 904,539 | 0 | 20 | 20 | yes | 1,095,461 | yes | 230.955 of 240 |
| H-AECP | `backlog.service.aecp.last.if1` | backlog | 1 | 79.584 | 7,958,439 | 0 | 20 | 20 | NO | -5,958,439 | yes | 160.416 of 240 |
| H-AECP | `hooks-late-aecp.read_descriptor.if0` | hooks-late-aecp | 0 | 1.901 | 190,147 | 0 | 20 | 20 | yes | 1,809,853 | no | 238.099 of 240 |
| H-AECP | `hooks-load-counters.service.aecp.first.if0` | hooks-load-counters | 0 | 5.735 | 573,481 | 0 | 20 | 20 | yes | 1,426,519 | yes | 234.265 of 240 |
| H-AECP | `hooks-load-counters.service.aecp.last.if1` | hooks-load-counters | 1 | 94.301 | 9,430,130 | 0 | 20 | 20 | NO | -7,430,130 | yes | 145.699 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.first.if0` | hooks-load-notify | 0 | 5.700 | 570,046 | 0 | 20 | 20 | yes | 1,429,954 | yes | 234.300 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.last.if0` | hooks-load-notify | 0 | 85.846 | 8,584,571 | 0 | 20 | 20 | NO | -6,584,571 | yes | 154.154 of 240 |
| H-COUNTERS | `counters.all.if0` | hooks-counters | 0 | 218.712 | 21,871,183 | 0 | 20 | 60 | NO | -19,871,183 | no | 781.288 of 1000 |
| H-COUNTERS | `counters.all.t36.i0.if0` | hooks-counters | 0 | 218.712 | 21,871,183 | 0 | 20 | 60 | NO | -19,871,183 | no | 781.288 of 1000 |
| H-COUNTERS | `counters.all.t5.i1.if0` | hooks-counters | 0 | 21.699 | 2,169,871 | 0 | 20 | 60 | NO | -169,871 | no | 978.301 of 1000 |
| H-COUNTERS | `counters.all.t5.i2.if0` | hooks-counters | 0 | 33.434 | 3,343,421 | 0 | 20 | 60 | NO | -1,343,421 | no | 966.566 of 1000 |
| H-COUNTERS | `counters.all.t5.i3.if0` | hooks-counters | 0 | 44.890 | 4,489,005 | 0 | 20 | 60 | NO | -2,489,005 | no | 955.110 of 1000 |
| H-COUNTERS | `counters.all.t5.i4.if0` | hooks-counters | 0 | 57.150 | 5,715,022 | 0 | 20 | 60 | NO | -3,715,022 | no | 942.850 of 1000 |
| H-COUNTERS | `counters.all.t5.i5.if0` | hooks-counters | 0 | 68.580 | 6,857,973 | 0 | 20 | 60 | NO | -4,857,973 | no | 931.420 of 1000 |
| H-COUNTERS | `counters.all.t5.i6.if0` | hooks-counters | 0 | 80.066 | 8,006,635 | 0 | 20 | 60 | NO | -6,006,635 | no | 919.934 of 1000 |
| H-COUNTERS | `counters.all.t5.i7.if0` | hooks-counters | 0 | 91.535 | 9,153,484 | 0 | 20 | 60 | NO | -7,153,484 | no | 908.465 of 1000 |
| H-COUNTERS | `counters.all.t5.i8.if0` | hooks-counters | 0 | 103.252 | 10,325,175 | 0 | 20 | 60 | NO | -8,325,175 | no | 896.748 of 1000 |
| H-COUNTERS | `counters.all.t6.i0.if0` | hooks-counters | 0 | 10.551 | 1,055,053 | 0 | 20 | 60 | yes | 944,947 | no | 989.449 of 1000 |
| H-COUNTERS | `counters.all.t6.i1.if0` | hooks-counters | 0 | 114.696 | 11,469,575 | 0 | 20 | 60 | NO | -9,469,575 | no | 885.304 of 1000 |
| H-COUNTERS | `counters.all.t6.i2.if0` | hooks-counters | 0 | 126.196 | 12,619,556 | 0 | 20 | 60 | NO | -10,619,556 | no | 873.804 of 1000 |
| H-COUNTERS | `counters.all.t6.i3.if0` | hooks-counters | 0 | 137.678 | 13,767,770 | 0 | 20 | 60 | NO | -11,767,770 | no | 862.322 of 1000 |
| H-COUNTERS | `counters.all.t6.i4.if0` | hooks-counters | 0 | 149.146 | 14,914,595 | 0 | 20 | 60 | NO | -12,914,595 | no | 850.854 of 1000 |
| H-COUNTERS | `counters.all.t6.i5.if0` | hooks-counters | 0 | 160.605 | 16,060,462 | 0 | 20 | 60 | NO | -14,060,462 | no | 839.395 of 1000 |
| H-COUNTERS | `counters.all.t6.i6.if0` | hooks-counters | 0 | 172.118 | 17,211,764 | 0 | 20 | 60 | NO | -15,211,764 | no | 827.882 of 1000 |
| H-COUNTERS | `counters.all.t6.i7.if0` | hooks-counters | 0 | 183.874 | 18,387,375 | 0 | 20 | 60 | NO | -16,387,375 | no | 816.126 of 1000 |
| H-COUNTERS | `counters.all.t6.i8.if0` | hooks-counters | 0 | 195.356 | 19,535,580 | 0 | 20 | 60 | NO | -17,535,580 | no | 804.644 of 1000 |
| H-COUNTERS | `counters.all.t9.i0.if0` | hooks-counters | 0 | 206.826 | 20,682,606 | 0 | 20 | 60 | NO | -18,682,606 | no | 793.174 of 1000 |
| H-COUNTERS | `counters.first.if0` | hooks-counters | 0 | 10.164 | 1,016,443 | 0 | 20 | 20 | yes | 983,557 | no | 989.836 of 1000 |
| H-COUNTERS | `counters.held.if0` | hooks-counters | 0 | 9.931 | 993,084 | 880.002 | 20 | 20 | yes | 1,006,916 | no | 110.067 of 1000 |
| H-COUNTERS | `counters.loaded.if0` | hooks-load-counters | 0 | 36.623 | 3,662,340 | 0 | 20 | 20 | NO | -1,662,340 | yes | 963.377 of 1000 |
| H-DISC | `acmp.entity_available.if0` | acmp-disc | 0 | 0.466 | 46,638 | 0 | 20 | 20 | yes | 1,953,362 | no | 199.534 of 200 |
| H-DISC | `acmp.entity_available.if1` | acmp-disc | 1 | 1.264 | 126,437 | 0 | 20 | 20 | yes | 1,873,563 | no | 198.736 of 200 |
| H-DISC | `acmp.entity_departing.if0` | acmp-disc | 0 | 0.170 | 17,029 | 0 | 20 | 20 | yes | 1,982,971 | no | 199.830 of 200 |
| H-DISC | `acmp.entity_departing.if1` | acmp-disc | 1 | 0.940 | 93,993 | 0 | 20 | 20 | yes | 1,906,007 | no | 199.060 of 200 |
| H-DISC | `acmp.tmr_no_adp.if0` | acmp-disc | 0 | 1.224 | 122,439 | 0 | 20 | 20 | yes | 1,877,561 | no | 198.776 of 200 |
| H-DISC | `acmp.tmr_no_adp.if1` | acmp-disc | 1 | 1.340 | 134,049 | 0 | 20 | 20 | yes | 1,865,951 | no | 198.660 of 200 |
| H-DISC | `backlog.adp_available.if0` | backlog-adp | 0 | 21.788 | 2,178,750 | 0 | 20 | 20 | NO | -178,750 | yes | 178.213 of 200 |
| H-DISC | `backlog.adp_available_refill.if0` | backlog-adp-refill | 0 | 0.398 | 39,840 | 0 | 20 | 20 | yes | 1,960,160 | yes | 199.602 of 200 |
| H-DISC | `hooks-disc-aging.available.if0` | hooks-disc-aging | 0 | 0.179 | 17,899 | 0 | 20 | 20 | yes | 1,982,101 | no | 199.821 of 200 |
| H-DISC | `hooks-disc-aging.available.if1` | hooks-disc-aging | 1 | 0.185 | 18,475 | 0 | 20 | 20 | yes | 1,981,525 | no | 199.815 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if0` | hooks-disc-aging | 0 | 0.479 | 47,900 | 0 | 20 | 20 | yes | 1,952,100 | no | 199.521 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if1` | hooks-disc-aging | 1 | 0.895 | 89,469 | 0 | 20 | 20 | yes | 1,910,531 | no | 199.105 of 200 |
| H-DISC | `hooks-late-disc.entity_departing.if0` | hooks-late-disc | 0 | 0.170 | 17,011 | 0 | 20 | 20 | yes | 1,982,989 | no | 199.830 of 200 |
| H-MAAP | `backlog-adp-refill.service.maap.first.if0` | backlog-adp-refill | 0 | 6.050 | 605,029 | 0 | 20 | 20 | yes | 1,394,971 | yes | 493.950 of 500 |
| H-MAAP | `backlog-adp-refill.service.maap.last.if0` | backlog-adp-refill | 0 | 27.068 | 2,706,757 | 0 | 20 | 20 | NO | -706,757 | yes | 472.932 of 500 |
| H-MAAP | `backlog-adp.service.maap.first.if0` | backlog-adp | 0 | 6.050 | 605,029 | 0 | 20 | 20 | yes | 1,394,971 | yes | 493.950 of 500 |
| H-MAAP | `backlog-adp.service.maap.last.if0` | backlog-adp | 0 | 27.771 | 2,777,112 | 0 | 20 | 20 | NO | -777,112 | yes | 472.229 of 500 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 6.558 | 655,848 | 0 | 20 | 20 | yes | 1,344,152 | yes | 493.442 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 27.050 | 2,704,980 | 0 | 20 | 20 | NO | -704,980 | yes | 472.950 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 9.035 | 903,499 | 0 | 20 | 20 | yes | 1,096,501 | yes | 490.965 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 31.481 | 3,148,065 | 0 | 20 | 20 | NO | -1,148,065 | yes | 468.519 of 500 |
| H-MAAP | `hooks-late-maap.defend.if0` | hooks-late-maap | 0 | 0.418 | 41,798 | 0 | 20 | 20 | yes | 1,958,202 | no | 499.582 of 500 |
| H-MAAP | `hooks-load-counters.service.maap.first.if0` | hooks-load-counters | 0 | 5.724 | 572,441 | 0 | 20 | 20 | yes | 1,427,559 | yes | 494.276 of 500 |
| H-MAAP | `hooks-load-counters.service.maap.last.if0` | hooks-load-counters | 0 | 26.809 | 2,680,896 | 0 | 20 | 20 | NO | -680,896 | yes | 473.191 of 500 |
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
| H-SRP | `backlog-adp-refill.service.srp.first.if0` | backlog-adp-refill | 0 | 14.106 | 1,410,638 | 0 | 18 | 20 | yes | 389,362 | yes | 165.894 of 180 |
| H-SRP | `backlog-adp-refill.service.srp.last.if1` | backlog-adp-refill | 1 | 95.668 | 9,566,774 | 0 | 18 | 20 | NO | -7,766,774 | yes | 84.332 of 180 |
| H-SRP | `backlog-adp.service.srp.first.if0` | backlog-adp | 0 | 14.106 | 1,410,638 | 0 | 18 | 20 | yes | 389,362 | yes | 165.894 of 180 |
| H-SRP | `backlog-adp.service.srp.last.if1` | backlog-adp | 1 | 94.017 | 9,401,707 | 0 | 18 | 20 | NO | -7,601,707 | yes | 85.983 of 180 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 14.440 | 1,444,030 | 0 | 18 | 20 | yes | 355,970 | yes | 165.560 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if1` | backlog-owed | 1 | 80.929 | 8,092,946 | 0 | 18 | 20 | NO | -6,292,946 | yes | 99.071 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 25.212 | 2,521,232 | 0 | 18 | 20 | NO | -721,232 | yes | 154.788 of 180 |
| H-SRP | `backlog.service.srp.last.if1` | backlog | 1 | 89.100 | 8,910,025 | 0 | 18 | 20 | NO | -7,110,025 | yes | 90.900 of 180 |
| H-SRP | `hooks-late-srp.listener_ready.if0` | hooks-late-srp | 0 | 2.141 | 214,104 | 0 | 18 | 20 | yes | 1,585,896 | no | 177.859 of 180 |
| H-SRP | `hooks-load-counters.service.srp.first.if0` | hooks-load-counters | 0 | 26.808 | 2,680,831 | 0 | 18 | 20 | NO | -880,831 | yes | 153.192 of 180 |
| H-SRP | `hooks-load-counters.service.srp.last.if1` | hooks-load-counters | 1 | 102.307 | 10,230,720 | 0 | 18 | 20 | NO | -8,430,720 | yes | 77.693 of 180 |
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
- LATE H-COUNTERS: counters.loaded.if0: 36.623 ms against its bound 20 ms (hooks-load-counters)
- LATE H-ADP: hooks-load-counters.service.adp.last.if1: 26.824 ms against its bound 20 ms (hooks-load-counters)
- LATE H-ACMP: hooks-load-counters.service.acmp.last.if0: 46.667 ms against its bound 20 ms (hooks-load-counters)
- LATE H-AECP: hooks-load-counters.service.aecp.last.if1: 94.301 ms against its bound 20 ms (hooks-load-counters)
- LATE H-MAAP: hooks-load-counters.service.maap.last.if0: 26.809 ms against its bound 20 ms (hooks-load-counters)
- LATE H-SRP: hooks-load-counters.service.srp.first.if0: 26.808 ms against its bound 18 ms (hooks-load-counters)
- LATE H-SRP: hooks-load-counters.service.srp.last.if1: 102.307 ms against its bound 18 ms (hooks-load-counters)
- LATE H-ACMP: backlog.acmp_command.if0: 37.912 ms against its bound 20 ms (backlog)
- LATE H-ADP: backlog.service.adp.last.if1: 31.496 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 42.136 ms against its bound 20 ms (backlog)
- LATE H-AECP: backlog.service.aecp.last.if1: 79.584 ms against its bound 20 ms (backlog)
- LATE H-MAAP: backlog.service.maap.last.if0: 31.481 ms against its bound 20 ms (backlog)
- LATE H-SRP: backlog.service.srp.first.if0: 25.212 ms against its bound 18 ms (backlog)
- LATE H-SRP: backlog.service.srp.last.if1: 89.100 ms against its bound 18 ms (backlog)
- LATE H-DISC: backlog.adp_available.if0: 21.788 ms against its bound 20 ms (backlog-adp)
- LATE H-ADP: backlog-adp.service.adp.last.if0: 27.734 ms against its bound 20 ms (backlog-adp)
- LATE H-ACMP: backlog-adp.service.acmp.last.if0: 39.318 ms against its bound 20 ms (backlog-adp)
- LATE H-AECP: backlog-adp.service.aecp.last.if1: 86.604 ms against its bound 20 ms (backlog-adp)
- LATE H-MAAP: backlog-adp.service.maap.last.if0: 27.771 ms against its bound 20 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.last.if1: 94.017 ms against its bound 18 ms (backlog-adp)
- LATE H-ACMP: backlog-adp-refill.service.acmp.last.if0: 40.157 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-AECP: backlog-adp-refill.service.aecp.last.if1: 86.299 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-MAAP: backlog-adp-refill.service.maap.last.if0: 27.068 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.last.if1: 95.668 ms against its bound 18 ms (backlog-adp-refill)
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
- LATE H-COUNTERS: counters.all.if0: 218.712 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i1.if0: 21.699 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i2.if0: 33.434 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i3.if0: 44.890 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i4.if0: 57.150 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i5.if0: 68.580 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i6.if0: 80.066 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i7.if0: 91.535 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t5.i8.if0: 103.252 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i1.if0: 114.696 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i2.if0: 126.196 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i3.if0: 137.678 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i4.if0: 149.146 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i5.if0: 160.605 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i6.if0: 172.118 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i7.if0: 183.874 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t6.i8.if0: 195.356 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t9.i0.if0: 206.826 ms against its bound 20 ms (hooks-counters)
- LATE H-COUNTERS: counters.all.t36.i0.if0: 218.712 ms against its bound 20 ms (hooks-counters)
