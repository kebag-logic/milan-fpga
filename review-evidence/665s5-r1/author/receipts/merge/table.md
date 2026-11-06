### 1x1, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm idle

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|
| H-ADP | 28 | 1 | 0 | 0.626 (20), `adp.tmr_advertise.if0`, margin 1999.4 of 2000 | 29.396 (20) **over its bound**, `backlog-adp.service.adp.last.if0`, margin 1970.6 of 2000 | 2 (0) | 0 |
| H-DISC | 8 | 1 | 0 | 8.403 (20), `acmp.entity_departing.if0`, margin 191.6 of 200 | 24.784 (20) **over its bound**, `backlog.adp_available.if0`, margin 175.2 of 200 | 1 (0) | 0 |
| H-ACMP | 30 | 11 | 0 | 8.159 (20), `acmp.probe_tx.if0`, margin 191.8 of 200 | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -163.3 of 200 | 65 (0) | 0 |
| H-AECP | 36 | 5 | 0 | 1.887 (20), `aecp.set_name.if0`, margin 238.1 of 240 | 159.479 (20) **over its bound**, `backlog-adp-refill.service.aecp.last.if0`, margin 80.5 of 240 | 7 (0) | 0 |
| H-NOTIFY | 11 | 1 | 0 | 3.778 (20), `aecp_fanout.set_name.if0`, margin 236.2 of 240 | 59.375 (20) **over its bound**, `hooks-load-notify.set_name.if0`, margin 180.6 of 240 | 11 (0) | 0 |
| H-COUNTERS | 0 | 0 | 0 | - | - | 0 (0) | 0 |
| H-MAAP | 17 | 2 | 0 | 1.009 (20), `maap.announce.if0`, margin 499.0 of 500 | 29.433 (20) **over its bound**, `backlog-adp.service.maap.last.if0`, margin 470.6 of 500 | 44 (0) | 0 |
| H-SRP | 15 | 7 | 0 | 1.809 (18), `srp.startup.if0`, margin 178.2 of 180 | never served (18) **over its bound**, `backlog-adp-refill.service.srp.first.if0`, margin -368.8 of 180 | 1 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound ms | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-ACMP | `acmp.bind_rx.if0` | acmp-cmd | 0 | 0.594 | 59,416 | 0 | 20 | yes | 1,940,584 | no | 199.406 of 200 |
| H-ACMP | `acmp.disconnect_tx.if0` | acmp-cmd | 0 | 7.919 | 791,877 | 0 | 20 | yes | 1,208,123 | no | 192.081 of 200 |
| H-ACMP | `acmp.get_rx_state.if0` | acmp-cmd | 0 | 8.098 | 809,787 | 0 | 20 | yes | 1,190,213 | no | 191.902 of 200 |
| H-ACMP | `acmp.get_tx_connection.if0` | acmp-cmd | 0 | 7.941 | 794,149 | 0 | 20 | yes | 1,205,851 | no | 192.059 of 200 |
| H-ACMP | `acmp.get_tx_state.if0` | acmp-cmd | 0 | 8.033 | 803,300 | 0 | 20 | yes | 1,196,700 | no | 191.967 of 200 |
| H-ACMP | `acmp.probe_tx.if0` | acmp-cmd | 0 | 8.159 | 815,916 | 0 | 20 | yes | 1,184,084 | no | 191.841 of 200 |
| H-ACMP | `acmp.probe_tx_response.if0` | acmp-cmd | 0 | 0.693 | 69,345 | 0 | 20 | yes | 1,930,655 | no | 199.307 of 200 |
| H-ACMP | `acmp.tmr_delay.if0` | acmp-noresp | 0 | 1.219 | 121,865 | 0 | 20 | yes | 1,878,135 | no | 198.781 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if0` | acmp-noresp | 0 | 0.836 | 83,552 | 0 | 20 | yes | 1,916,448 | no | 199.164 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if0` | acmp-noresp | 0 | 0.525 | 52,525 | 0 | 20 | yes | 1,947,475 | no | 199.475 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if0` | acmp-notk | 0 | 1.156 | 115,567 | 0 | 20 | yes | 1,884,433 | no | 198.844 of 200 |
| H-ACMP | `acmp.tmr_retry.if0` | acmp-noresp | 0 | 0.192 | 19,169 | 0 | 20 | yes | 1,980,831 | no | 199.808 of 200 |
| H-ACMP | `acmp.unbind_rx.if0` | acmp-cmd | 0 | 8.075 | 807,516 | 0 | 20 | yes | 1,192,484 | no | 191.925 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.first.if0` | backlog-adp-refill | 0 | 5.013 | 501,280 | 0 | 20 | yes | 1,498,720 | yes | 194.987 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.last.if0` | backlog-adp-refill | 0 | 53.109 | 5,310,871 | 0 | 20 | NO | -3,310,871 | yes | 146.891 of 200 |
| H-ACMP | `backlog-adp.service.acmp.first.if0` | backlog-adp | 0 | 5.013 | 501,280 | 0 | 20 | yes | 1,498,720 | yes | 194.987 of 200 |
| H-ACMP | `backlog-adp.service.acmp.last.if0` | backlog-adp | 0 | 52.844 | 5,284,394 | 0 | 20 | NO | -3,284,394 | yes | 147.156 of 200 |
| H-ACMP | `backlog-owed.service.acmp.first.if0` | backlog-owed | 0 | 4.436 | 443,612 | 0 | 20 | yes | 1,556,388 | yes | 195.564 of 200 |
| H-ACMP | `backlog-owed.service.acmp.last.if0` | backlog-owed | 0 | 24.542 | 2,454,227 | 0 | 20 | NO | -454,227 | yes | 175.458 of 200 |
| H-ACMP | `backlog.acmp_command.if0` | backlog | 0 | 22.574 | 2,257,366 | 0 | 20 | NO | -257,366 | yes | 177.426 of 200 |
| H-ACMP | `backlog.owed.if0` | backlog-owed | 0 | 77.836 | 7,783,636 | 0 | 20 | NO | -5,783,636 | yes | 122.164 of 200 |
| H-ACMP | `backlog.owed_behind0.if0` | backlog-owed | 0 | never | 36,330,909 | 0 | 20 | NO | -1 | yes | -163.309 of 200 |
| H-ACMP | `backlog.owed_behind1.if0` | backlog-owed | 0 | never | 36,330,834 | 0 | 20 | NO | -1 | yes | -163.308 of 200 |
| H-ACMP | `backlog.owed_behind2.if0` | backlog-owed | 0 | never | 36,330,759 | 0 | 20 | NO | -1 | yes | -163.308 of 200 |
| H-ACMP | `backlog.owed_behind3.if0` | backlog-owed | 0 | never | 36,330,684 | 0 | 20 | NO | -1 | yes | -163.307 of 200 |
| H-ACMP | `backlog.service.acmp.first.if0` | backlog | 0 | 5.373 | 537,331 | 0 | 20 | yes | 1,462,669 | yes | 194.627 of 200 |
| H-ACMP | `backlog.service.acmp.last.if0` | backlog | 0 | 25.014 | 2,501,387 | 0 | 20 | NO | -501,387 | yes | 174.986 of 200 |
| H-ACMP | `hooks-late-acmp.get_rx_state.if0` | hooks-late-acmp | 0 | 0.357 | 35,744 | 0 | 20 | yes | 1,964,256 | no | 199.643 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.first.if0` | hooks-load-notify | 0 | 4.506 | 450,584 | 0 | 20 | yes | 1,549,416 | yes | 195.494 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.last.if0` | hooks-load-notify | 0 | 26.671 | 2,667,073 | 0 | 20 | NO | -667,073 | yes | 173.329 of 200 |
| H-ADP | `adp.discover.if0` | adp-discover | 0 | 0.132 | 13,193 | 0 | 20 | yes | 1,986,807 | no | 1999.868 of 2000 |
| H-ADP | `adp.gm_change.if0` | adp-gm | 0 | 0.062 | 6,231 | 0 | 20 | yes | 1,993,769 | no | 1999.938 of 2000 |
| H-ADP | `adp.link_down.if0` | adp-link | 0 | 0.051 | 5,080 | 0 | 20 | yes | 1,994,920 | no | 1999.949 of 2000 |
| H-ADP | `adp.link_up.if0` | hooks-order-adp | 0 | 0.063 | 6,276 | 0 | 20 | yes | 1,993,724 | no | 1999.937 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-advertise | 0 | 0.063 | 6,276 | 0 | 20 | yes | 1,993,724 | no | 1999.937 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-link | 0 | 0.063 | 6,276 | 0 | 20 | yes | 1,993,724 | no | 1999.937 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-gm | 0 | 0.063 | 6,276 | 0 | 20 | yes | 1,993,724 | no | 1999.937 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-discover | 0 | 0.063 | 6,276 | 0 | 20 | yes | 1,993,724 | no | 1999.937 of 2000 |
| H-ADP | `adp.link_up.if0` | control | 0 | 0.063 | 6,276 | 0 | 20 | yes | 1,993,724 | no | 1999.937 of 2000 |
| H-ADP | `adp.tmr_advertise.if0` | adp-advertise | 0 | 0.626 | 62,615 | 0 | 20 | yes | 1,937,385 | no | 1999.374 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | hooks-order-adp | 0 | 0.369 | 36,857 | 0 | 20 | yes | 1,963,143 | no | 1999.631 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-advertise | 0 | 0.369 | 36,857 | 0 | 20 | yes | 1,963,143 | no | 1999.631 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-link | 0 | 0.369 | 36,857 | 0 | 20 | yes | 1,963,143 | no | 1999.631 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-gm | 0 | 0.369 | 36,857 | 0 | 20 | yes | 1,963,143 | no | 1999.631 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-discover | 0 | 0.369 | 36,857 | 0 | 20 | yes | 1,963,143 | no | 1999.631 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | control | 0 | 0.369 | 36,857 | 0 | 20 | yes | 1,963,143 | no | 1999.631 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.first.if0` | backlog-adp-refill | 0 | 5.004 | 500,368 | 0 | 20 | yes | 1,499,632 | yes | 1994.996 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.last.if0` | backlog-adp-refill | 0 | 13.153 | 1,315,259 | 0 | 20 | yes | 684,741 | yes | 1986.847 of 2000 |
| H-ADP | `backlog-adp.service.adp.first.if0` | backlog-adp | 0 | 5.004 | 500,368 | 0 | 20 | yes | 1,499,632 | yes | 1994.996 of 2000 |
| H-ADP | `backlog-adp.service.adp.last.if0` | backlog-adp | 0 | 29.396 | 2,939,623 | 0 | 20 | NO | -939,623 | yes | 1970.604 of 2000 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 4.479 | 447,871 | 0 | 20 | yes | 1,552,129 | yes | 1995.521 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if0` | backlog-owed | 0 | 18.169 | 1,816,886 | 0 | 20 | yes | 183,114 | yes | 1981.831 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 5.805 | 580,474 | 0 | 20 | yes | 1,419,526 | yes | 1994.195 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 5.416 | 541,590 | 0 | 20 | yes | 1,458,410 | yes | 1994.584 of 2000 |
| H-ADP | `backlog.service.adp.last.if0` | backlog | 0 | 18.329 | 1,832,851 | 0 | 20 | yes | 167,149 | yes | 1981.671 of 2000 |
| H-ADP | `control.discover.if0` | control | 0 | 0.132 | 13,193 | 0 | 20 | yes | 1,986,807 | no | 1999.868 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.first.if0` | hooks-load-notify | 0 | 4.538 | 453,803 | 0 | 20 | yes | 1,546,197 | yes | 1995.462 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.last.if0` | hooks-load-notify | 0 | 19.473 | 1,947,338 | 0 | 20 | yes | 52,662 | yes | 1980.527 of 2000 |
| H-AECP | `aecp.entity_available.if0` | aecp | 0 | 1.303 | 130,332 | 0 | 20 | yes | 1,869,668 | no | 238.697 of 240 |
| H-AECP | `aecp.get_avb_info.if0` | aecp | 0 | 1.321 | 132,116 | 0 | 20 | yes | 1,867,884 | no | 238.679 of 240 |
| H-AECP | `aecp.get_configuration.if0` | aecp | 0 | 1.284 | 128,431 | 0 | 20 | yes | 1,871,569 | no | 238.716 of 240 |
| H-AECP | `aecp.get_counters.if0` | aecp | 0 | 1.458 | 145,816 | 0 | 20 | yes | 1,854,184 | no | 238.542 of 240 |
| H-AECP | `aecp.get_name.if0` | aecp | 0 | 1.581 | 158,119 | 0 | 20 | yes | 1,841,881 | no | 238.419 of 240 |
| H-AECP | `aecp.lock_entity.if0` | aecp | 0 | 1.396 | 139,572 | 0 | 20 | yes | 1,860,428 | no | 238.604 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if0` | aecp | 0 | 0.883 | 88,289 | 0 | 20 | yes | 1,911,711 | no | 239.117 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if0` | aecp | 0 | 1.694 | 169,353 | 0 | 20 | yes | 1,830,647 | no | 238.306 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if0` | aecp | 0 | 1.425 | 142,452 | 0 | 20 | yes | 1,857,548 | no | 238.575 of 240 |
| H-AECP | `aecp.read_descriptor.t10.i2.c0.if0` | aecp | 0 | 1.406 | 140,614 | 0 | 20 | yes | 1,859,386 | no | 238.594 of 240 |
| H-AECP | `aecp.read_descriptor.t12.i0.c0.if0` | aecp | 0 | 1.390 | 138,994 | 0 | 20 | yes | 1,861,006 | no | 238.610 of 240 |
| H-AECP | `aecp.read_descriptor.t13.i0.c0.if0` | aecp | 0 | 1.866 | 186,570 | 0 | 20 | yes | 1,813,430 | no | 238.134 of 240 |
| H-AECP | `aecp.read_descriptor.t14.i0.c0.if0` | aecp | 0 | 1.326 | 132,646 | 0 | 20 | yes | 1,867,354 | no | 238.674 of 240 |
| H-AECP | `aecp.read_descriptor.t15.i0.c0.if0` | aecp | 0 | 1.327 | 132,722 | 0 | 20 | yes | 1,867,278 | no | 238.673 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if0` | aecp | 0 | 1.681 | 168,116 | 0 | 20 | yes | 1,831,884 | no | 238.319 of 240 |
| H-AECP | `aecp.read_descriptor.t20.i24.c0.if0` | aecp | 0 | 1.639 | 163,852 | 0 | 20 | yes | 1,836,148 | no | 238.361 of 240 |
| H-AECP | `aecp.read_descriptor.t26.i0.c0.if0` | aecp | 0 | 1.463 | 146,283 | 0 | 20 | yes | 1,853,717 | no | 238.537 of 240 |
| H-AECP | `aecp.read_descriptor.t36.i0.c0.if0` | aecp | 0 | 1.424 | 142,444 | 0 | 20 | yes | 1,857,556 | no | 238.576 of 240 |
| H-AECP | `aecp.read_descriptor.t5.i1.c0.if0` | aecp | 0 | 1.476 | 147,645 | 0 | 20 | yes | 1,852,355 | no | 238.524 of 240 |
| H-AECP | `aecp.read_descriptor.t6.i1.c0.if0` | aecp | 0 | 1.478 | 147,797 | 0 | 20 | yes | 1,852,203 | no | 238.522 of 240 |
| H-AECP | `aecp.read_descriptor.t9.i0.c0.if0` | aecp | 0 | 1.424 | 142,360 | 0 | 20 | yes | 1,857,640 | no | 238.576 of 240 |
| H-AECP | `aecp.register_unsolicited.if0` | aecp | 0 | 0.881 | 88,092 | 0 | 20 | yes | 1,911,908 | no | 239.119 of 240 |
| H-AECP | `aecp.set_name.if0` | aecp | 0 | 1.887 | 188,693 | 0 | 20 | yes | 1,811,307 | no | 238.113 of 240 |
| H-AECP | `aecp.unknown_command.if0` | aecp | 0 | 1.279 | 127,920 | 0 | 20 | yes | 1,872,080 | no | 238.721 of 240 |
| H-AECP | `aecp.unlock_entity.if0` | aecp | 0 | 1.396 | 139,573 | 0 | 20 | yes | 1,860,427 | no | 238.604 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.first.if0` | backlog-adp-refill | 0 | 5.049 | 504,865 | 0 | 20 | yes | 1,495,135 | yes | 234.951 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.last.if0` | backlog-adp-refill | 0 | 159.479 | 15,947,899 | 0 | 20 | NO | -13,947,899 | yes | 80.521 of 240 |
| H-AECP | `backlog-adp.service.aecp.first.if0` | backlog-adp | 0 | 5.049 | 504,865 | 0 | 20 | yes | 1,495,135 | yes | 234.951 of 240 |
| H-AECP | `backlog-adp.service.aecp.last.if0` | backlog-adp | 0 | 159.218 | 15,921,815 | 0 | 20 | NO | -13,921,815 | yes | 80.782 of 240 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 4.472 | 447,197 | 0 | 20 | yes | 1,552,803 | yes | 235.528 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if0` | backlog-owed | 0 | 85.818 | 8,581,790 | 0 | 20 | NO | -6,581,790 | yes | 154.182 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 5.409 | 540,916 | 0 | 20 | yes | 1,459,084 | yes | 234.591 of 240 |
| H-AECP | `backlog.service.aecp.last.if0` | backlog | 0 | 48.472 | 4,847,241 | 0 | 20 | NO | -2,847,241 | yes | 191.528 of 240 |
| H-AECP | `hooks-late-aecp.read_descriptor.if0` | hooks-late-aecp | 0 | 1.670 | 166,972 | 0 | 20 | yes | 1,833,028 | no | 238.330 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.first.if0` | hooks-load-notify | 0 | 4.497 | 449,694 | 0 | 20 | yes | 1,550,306 | yes | 235.503 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.last.if0` | hooks-load-notify | 0 | 60.110 | 6,010,978 | 0 | 20 | NO | -4,010,978 | yes | 179.890 of 240 |
| H-DISC | `acmp.entity_available.if0` | acmp-disc | 0 | 3.448 | 344,804 | 0 | 20 | yes | 1,655,196 | no | 196.552 of 200 |
| H-DISC | `acmp.entity_departing.if0` | acmp-disc | 0 | 8.403 | 840,314 | 0 | 20 | yes | 1,159,686 | no | 191.597 of 200 |
| H-DISC | `acmp.tmr_no_adp.if0` | acmp-disc | 0 | 1.059 | 105,925 | 0 | 20 | yes | 1,894,075 | no | 198.941 of 200 |
| H-DISC | `backlog.adp_available.if0` | backlog-adp | 0 | 24.784 | 2,478,432 | 0 | 20 | NO | -478,432 | yes | 175.216 of 200 |
| H-DISC | `backlog.adp_available_refill.if0` | backlog-adp-refill | 0 | 8.803 | 880,348 | 0 | 20 | yes | 1,119,652 | yes | 191.197 of 200 |
| H-DISC | `hooks-disc-aging.available.if0` | hooks-disc-aging | 0 | 7.244 | 724,364 | 0 | 20 | yes | 1,275,636 | no | 192.756 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if0` | hooks-disc-aging | 0 | 0.940 | 94,020 | 0 | 20 | yes | 1,905,980 | no | 199.060 of 200 |
| H-DISC | `hooks-late-disc.entity_departing.if0` | hooks-late-disc | 0 | 8.403 | 840,314 | 0 | 20 | yes | 1,159,686 | no | 191.597 of 200 |
| H-MAAP | `backlog-adp-refill.service.maap.first.if0` | backlog-adp-refill | 0 | 5.038 | 503,825 | 0 | 20 | yes | 1,496,175 | yes | 494.962 of 500 |
| H-MAAP | `backlog-adp-refill.service.maap.last.if0` | backlog-adp-refill | 0 | 29.155 | 2,915,470 | 0 | 20 | NO | -915,470 | yes | 470.845 of 500 |
| H-MAAP | `backlog-adp.service.maap.first.if0` | backlog-adp | 0 | 5.038 | 503,825 | 0 | 20 | yes | 1,496,175 | yes | 494.962 of 500 |
| H-MAAP | `backlog-adp.service.maap.last.if0` | backlog-adp | 0 | 29.433 | 2,943,299 | 0 | 20 | NO | -943,299 | yes | 470.567 of 500 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 4.462 | 446,157 | 0 | 20 | yes | 1,553,843 | yes | 495.538 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 18.154 | 1,815,391 | 0 | 20 | yes | 184,609 | yes | 481.846 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 5.399 | 539,876 | 0 | 20 | yes | 1,460,124 | yes | 494.601 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 18.314 | 1,831,356 | 0 | 20 | yes | 168,644 | yes | 481.686 of 500 |
| H-MAAP | `hooks-late-maap.defend.if0` | hooks-late-maap | 0 | 0.292 | 29,193 | 0 | 20 | yes | 1,970,807 | no | 499.708 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.first.if0` | hooks-load-notify | 0 | 4.531 | 453,129 | 0 | 20 | yes | 1,546,871 | yes | 495.469 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.last.if0` | hooks-load-notify | 0 | 19.469 | 1,946,883 | 0 | 20 | yes | 53,117 | yes | 480.531 of 500 |
| H-MAAP | `maap.announce.if0` | maap | 0 | 1.009 | 100,897 | 0 | 20 | yes | 1,899,103 | no | 498.991 of 500 |
| H-MAAP | `maap.defend.if0` | maap | 0 | 0.292 | 29,193 | 0 | 20 | yes | 1,970,807 | no | 499.708 of 500 |
| H-MAAP | `maap.probe1.if0` | maap | 0 | 0.364 | 36,368 | 0 | 20 | yes | 1,963,632 | no | 499.636 of 500 |
| H-MAAP | `maap.probe2.if0` | maap | 0 | 0.840 | 84,003 | 0 | 20 | yes | 1,915,997 | no | 499.160 of 500 |
| H-MAAP | `maap.probe3.if0` | maap | 0 | 0.469 | 46,872 | 0 | 20 | yes | 1,953,128 | no | 499.531 of 500 |
| H-MAAP | `maap.probe4.if0` | maap | 0 | 0.917 | 91,695 | 0 | 20 | yes | 1,908,305 | no | 499.083 of 500 |
| H-NOTIFY | `aecp_fanout.add_audio_mappings.if0` | aecp-fanout | 0 | 2.857 | 285,726 | 0 | 20 | yes | 1,714,274 | no | 237.143 of 240 |
| H-NOTIFY | `aecp_fanout.lock_entity.if0` | aecp-fanout | 0 | 2.782 | 278,224 | 0 | 20 | yes | 1,721,776 | no | 237.218 of 240 |
| H-NOTIFY | `aecp_fanout.remove_audio_mappings.if0` | aecp-fanout | 0 | 2.860 | 285,950 | 0 | 20 | yes | 1,714,050 | no | 237.141 of 240 |
| H-NOTIFY | `aecp_fanout.set_clock_source.if0` | aecp-fanout | 0 | 2.750 | 275,043 | 0 | 20 | yes | 1,724,957 | no | 237.250 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_off.if0` | aecp-fanout | 0 | 2.653 | 265,267 | 0 | 20 | yes | 1,734,733 | no | 237.347 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_on.if0` | aecp-fanout | 0 | 2.644 | 264,385 | 0 | 20 | yes | 1,735,615 | no | 237.356 of 240 |
| H-NOTIFY | `aecp_fanout.set_name.if0` | aecp-fanout | 0 | 3.778 | 377,844 | 0 | 20 | yes | 1,622,156 | no | 236.222 of 240 |
| H-NOTIFY | `aecp_fanout.set_sampling_rate.if0` | aecp-fanout | 0 | 2.650 | 264,975 | 0 | 20 | yes | 1,735,025 | no | 237.350 of 240 |
| H-NOTIFY | `aecp_fanout.unlock_entity.if0` | aecp-fanout | 0 | 2.785 | 278,550 | 0 | 20 | yes | 1,721,450 | no | 237.214 of 240 |
| H-NOTIFY | `hooks-late-notify.set_name.if0` | hooks-late-notify | 0 | 3.778 | 377,844 | 0 | 20 | yes | 1,622,156 | no | 236.222 of 240 |
| H-NOTIFY | `hooks-load-notify.set_name.if0` | hooks-load-notify | 0 | 59.375 | 5,937,475 | 0 | 20 | NO | -3,937,475 | yes | 180.625 of 240 |
| H-SRP | `backlog-adp-refill.service.srp.first.if0` | backlog-adp-refill | 0 | never | 54,878,875 | 0 | 18 | NO | -1 | yes | -368.789 of 180 |
| H-SRP | `backlog-adp-refill.service.srp.last.if0` | backlog-adp-refill | 0 | never | 54,876,860 | 0 | 18 | NO | -1 | yes | -368.769 of 180 |
| H-SRP | `backlog-adp.service.srp.first.if0` | backlog-adp | 0 | never | 52,482,043 | 0 | 18 | NO | -1 | yes | -344.820 of 180 |
| H-SRP | `backlog-adp.service.srp.last.if0` | backlog-adp | 0 | never | 52,480,028 | 0 | 18 | NO | -1 | yes | -344.800 of 180 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 9.794 | 979,389 | 0 | 18 | yes | 820,611 | yes | 170.206 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if0` | backlog-owed | 0 | 42.197 | 4,219,679 | 0 | 18 | NO | -2,419,679 | yes | 137.803 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 14.746 | 1,474,642 | 0 | 18 | yes | 325,358 | yes | 165.254 of 180 |
| H-SRP | `backlog.service.srp.last.if0` | backlog | 0 | 50.676 | 5,067,613 | 0 | 18 | NO | -3,267,613 | yes | 129.324 of 180 |
| H-SRP | `hooks-late-srp.listener_ready.if0` | hooks-late-srp | 0 | 1.241 | 124,085 | 0 | 18 | yes | 1,675,915 | no | 178.759 of 180 |
| H-SRP | `hooks-load-notify.service.srp.first.if0` | hooks-load-notify | 0 | 9.982 | 998,185 | 0 | 18 | yes | 801,815 | yes | 170.018 of 180 |
| H-SRP | `hooks-load-notify.service.srp.last.if0` | hooks-load-notify | 0 | 66.231 | 6,623,113 | 0 | 18 | NO | -4,823,113 | yes | 113.769 of 180 |
| H-SRP | `srp.domain.if0` | srp | 0 | 2.063 | 206,265 | 200 | 218 | yes | 21,593,735 | no | -22.063 of 180 |
| H-SRP | `srp.listener_ready.if0` | srp | 0 | 1.241 | 124,085 | 0 | 18 | yes | 1,675,915 | no | 178.759 of 180 |
| H-SRP | `srp.malformed.if0` | srp | 0 | 0.816 | 81,595 | 0 | 18 | yes | 1,718,405 | no | 179.184 of 180 |
| H-SRP | `srp.startup.if0` | srp | 0 | 1.809 | 180,880 | 0 | 18 | yes | 1,619,120 | no | 178.191 of 180 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- none

Findings:

- LATE H-NOTIFY: hooks-load-notify.set_name.if0: 59.375 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ACMP: hooks-load-notify.service.acmp.last.if0: 26.671 ms against its bound 20 ms (hooks-load-notify)
- LATE H-AECP: hooks-load-notify.service.aecp.last.if0: 60.110 ms against its bound 20 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.last.if0: 66.231 ms against its bound 18 ms (hooks-load-notify)
- LATE H-ACMP: backlog.acmp_command.if0: 22.574 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 25.014 ms against its bound 20 ms (backlog)
- LATE H-AECP: backlog.service.aecp.last.if0: 48.472 ms against its bound 20 ms (backlog)
- LATE H-SRP: backlog.service.srp.last.if0: 50.676 ms against its bound 18 ms (backlog)
- LATE H-DISC: backlog.adp_available.if0: 24.784 ms against its bound 20 ms (backlog-adp)
- LATE H-ADP: backlog-adp.service.adp.last.if0: 29.396 ms against its bound 20 ms (backlog-adp)
- LATE H-ACMP: backlog-adp.service.acmp.last.if0: 52.844 ms against its bound 20 ms (backlog-adp)
- LATE H-AECP: backlog-adp.service.aecp.last.if0: 159.218 ms against its bound 20 ms (backlog-adp)
- LATE H-MAAP: backlog-adp.service.maap.last.if0: 29.433 ms against its bound 20 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.first.if0: never served against its bound 18 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.last.if0: never served against its bound 18 ms (backlog-adp)
- LATE H-ACMP: backlog-adp-refill.service.acmp.last.if0: 53.109 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-AECP: backlog-adp-refill.service.aecp.last.if0: 159.479 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-MAAP: backlog-adp-refill.service.maap.last.if0: 29.155 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.first.if0: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.last.if0: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-ACMP: backlog.owed.if0: 77.836 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind0.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind1.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind2.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind3.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog-owed.service.acmp.last.if0: 24.542 ms against its bound 20 ms (backlog-owed)
- LATE H-AECP: backlog-owed.service.aecp.last.if0: 85.818 ms against its bound 20 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.last.if0: 42.197 ms against its bound 18 ms (backlog-owed)
