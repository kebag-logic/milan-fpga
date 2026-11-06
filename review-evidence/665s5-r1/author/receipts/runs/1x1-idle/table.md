### 1x1, CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz, face arm idle

| Hook | Paths | Over its bound | Within it by less than the layout swing | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Ordering check applied (undecided) | Ordering findings |
|---|---:|---:|---:|---|---|---:|---:|
| H-ADP | 28 | 1 | 0 | 0.626 (20), `adp.tmr_advertise.if0`, margin 1999.4 of 2000 | 29.396 (20) **over its bound**, `backlog-adp.service.adp.last.if0`, margin 1970.6 of 2000 | 2 (0) | 0 |
| H-DISC | 8 | 1 | 0 | 8.403 (20), `acmp.entity_departing.if0`, margin 191.6 of 200 | 24.784 (20) **over its bound**, `backlog.adp_available.if0`, margin 175.2 of 200 | 1 (0) | 0 |
| H-ACMP | 30 | 11 | 0 | 8.159 (20), `acmp.probe_tx.if0`, margin 191.8 of 200 | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -163.3 of 200 | 65 (0) | 0 |
| H-AECP | 36 | 5 | 0 | 1.886 (20), `aecp.set_name.if0`, margin 238.1 of 240 | 159.479 (20) **over its bound**, `backlog-adp-refill.service.aecp.last.if0`, margin 80.5 of 240 | 7 (0) | 0 |
| H-NOTIFY | 11 | 1 | 0 | 3.778 (20), `aecp_fanout.set_name.if0`, margin 236.2 of 240 | 59.375 (20) **over its bound**, `hooks-load-notify.set_name.if0`, margin 180.6 of 240 | 11 (0) | 0 |
| H-COUNTERS | 0 | 0 | 0 | - | - | 0 (0) | 0 |
| H-MAAP | 17 | 2 | 0 | 1.010 (20), `maap.announce.if0`, margin 499.0 of 500 | 29.433 (20) **over its bound**, `backlog-adp.service.maap.last.if0`, margin 470.6 of 500 | 44 (0) | 0 |
| H-SRP | 15 | 7 | 0 | 1.809 (18), `srp.startup.if0`, margin 178.2 of 180 | never served (18) **over its bound**, `backlog-adp-refill.service.srp.first.if0`, margin -368.8 of 180 | 1 (0) | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound ms | Within | Slack, CPU cycles | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---|---:|---|---:|
| H-ACMP | `acmp.bind_rx.if0` | acmp-cmd | 0 | 0.594 | 59,416 | 0 | 20 | yes | 1,940,584 | no | 199.406 of 200 |
| H-ACMP | `acmp.disconnect_tx.if0` | acmp-cmd | 0 | 7.918 | 791,850 | 0 | 20 | yes | 1,208,150 | no | 192.082 of 200 |
| H-ACMP | `acmp.get_rx_state.if0` | acmp-cmd | 0 | 8.098 | 809,760 | 0 | 20 | yes | 1,190,240 | no | 191.902 of 200 |
| H-ACMP | `acmp.get_tx_connection.if0` | acmp-cmd | 0 | 7.941 | 794,140 | 0 | 20 | yes | 1,205,860 | no | 192.059 of 200 |
| H-ACMP | `acmp.get_tx_state.if0` | acmp-cmd | 0 | 8.033 | 803,300 | 0 | 20 | yes | 1,196,700 | no | 191.967 of 200 |
| H-ACMP | `acmp.probe_tx.if0` | acmp-cmd | 0 | 8.159 | 815,934 | 0 | 20 | yes | 1,184,066 | no | 191.841 of 200 |
| H-ACMP | `acmp.probe_tx_response.if0` | acmp-cmd | 0 | 0.693 | 69,345 | 0 | 20 | yes | 1,930,655 | no | 199.307 of 200 |
| H-ACMP | `acmp.tmr_delay.if0` | acmp-noresp | 0 | 1.175 | 117,533 | 0 | 20 | yes | 1,882,467 | no | 198.825 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if0` | acmp-noresp | 0 | 0.836 | 83,594 | 0 | 20 | yes | 1,916,406 | no | 199.164 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if0` | acmp-noresp | 0 | 0.526 | 52,558 | 0 | 20 | yes | 1,947,442 | no | 199.474 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if0` | acmp-notk | 0 | 0.665 | 66,546 | 0 | 20 | yes | 1,933,454 | no | 199.335 of 200 |
| H-ACMP | `acmp.tmr_retry.if0` | acmp-noresp | 0 | 1.137 | 113,702 | 0 | 20 | yes | 1,886,298 | no | 198.863 of 200 |
| H-ACMP | `acmp.unbind_rx.if0` | acmp-cmd | 0 | 8.075 | 807,507 | 0 | 20 | yes | 1,192,493 | no | 191.925 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.first.if0` | backlog-adp-refill | 0 | 5.012 | 501,226 | 0 | 20 | yes | 1,498,774 | yes | 194.988 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.last.if0` | backlog-adp-refill | 0 | 53.109 | 5,310,889 | 0 | 20 | NO | -3,310,889 | yes | 146.891 of 200 |
| H-ACMP | `backlog-adp.service.acmp.first.if0` | backlog-adp | 0 | 5.012 | 501,226 | 0 | 20 | yes | 1,498,774 | yes | 194.988 of 200 |
| H-ACMP | `backlog-adp.service.acmp.last.if0` | backlog-adp | 0 | 52.844 | 5,284,367 | 0 | 20 | NO | -3,284,367 | yes | 147.156 of 200 |
| H-ACMP | `backlog-owed.service.acmp.first.if0` | backlog-owed | 0 | 4.435 | 443,540 | 0 | 20 | yes | 1,556,460 | yes | 195.565 of 200 |
| H-ACMP | `backlog-owed.service.acmp.last.if0` | backlog-owed | 0 | 24.542 | 2,454,209 | 0 | 20 | NO | -454,209 | yes | 175.458 of 200 |
| H-ACMP | `backlog.acmp_command.if0` | backlog | 0 | 22.573 | 2,257,321 | 0 | 20 | NO | -257,321 | yes | 177.427 of 200 |
| H-ACMP | `backlog.owed.if0` | backlog-owed | 0 | 77.837 | 7,783,654 | 0 | 20 | NO | -5,783,654 | yes | 122.163 of 200 |
| H-ACMP | `backlog.owed_behind0.if0` | backlog-owed | 0 | never | 36,330,711 | 0 | 20 | NO | -1 | yes | -163.307 of 200 |
| H-ACMP | `backlog.owed_behind1.if0` | backlog-owed | 0 | never | 36,330,636 | 0 | 20 | NO | -1 | yes | -163.306 of 200 |
| H-ACMP | `backlog.owed_behind2.if0` | backlog-owed | 0 | never | 36,330,561 | 0 | 20 | NO | -1 | yes | -163.306 of 200 |
| H-ACMP | `backlog.owed_behind3.if0` | backlog-owed | 0 | never | 36,330,486 | 0 | 20 | NO | -1 | yes | -163.305 of 200 |
| H-ACMP | `backlog.service.acmp.first.if0` | backlog | 0 | 5.373 | 537,331 | 0 | 20 | yes | 1,462,669 | yes | 194.627 of 200 |
| H-ACMP | `backlog.service.acmp.last.if0` | backlog | 0 | 25.013 | 2,501,342 | 0 | 20 | NO | -501,342 | yes | 174.987 of 200 |
| H-ACMP | `hooks-late-acmp.get_rx_state.if0` | hooks-late-acmp | 0 | 0.357 | 35,744 | 0 | 20 | yes | 1,964,256 | no | 199.643 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.first.if0` | hooks-load-notify | 0 | 4.506 | 450,639 | 0 | 20 | yes | 1,549,361 | yes | 195.494 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.last.if0` | hooks-load-notify | 0 | 26.672 | 2,667,173 | 0 | 20 | NO | -667,173 | yes | 173.328 of 200 |
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
| H-ADP | `adp.tmr_delay.if0` | hooks-order-adp | 0 | 0.368 | 36,782 | 0 | 20 | yes | 1,963,218 | no | 1999.632 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-advertise | 0 | 0.368 | 36,782 | 0 | 20 | yes | 1,963,218 | no | 1999.632 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-link | 0 | 0.368 | 36,782 | 0 | 20 | yes | 1,963,218 | no | 1999.632 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-gm | 0 | 0.368 | 36,782 | 0 | 20 | yes | 1,963,218 | no | 1999.632 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-discover | 0 | 0.368 | 36,782 | 0 | 20 | yes | 1,963,218 | no | 1999.632 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | control | 0 | 0.368 | 36,782 | 0 | 20 | yes | 1,963,218 | no | 1999.632 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.first.if0` | backlog-adp-refill | 0 | 5.003 | 500,314 | 0 | 20 | yes | 1,499,686 | yes | 1994.997 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.last.if0` | backlog-adp-refill | 0 | 13.153 | 1,315,277 | 0 | 20 | yes | 684,723 | yes | 1986.847 of 2000 |
| H-ADP | `backlog-adp.service.adp.first.if0` | backlog-adp | 0 | 5.003 | 500,314 | 0 | 20 | yes | 1,499,686 | yes | 1994.997 of 2000 |
| H-ADP | `backlog-adp.service.adp.last.if0` | backlog-adp | 0 | 29.396 | 2,939,614 | 0 | 20 | NO | -939,614 | yes | 1970.604 of 2000 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 4.478 | 447,799 | 0 | 20 | yes | 1,552,201 | yes | 1995.522 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if0` | backlog-owed | 0 | 18.169 | 1,816,859 | 0 | 20 | yes | 183,141 | yes | 1981.831 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 5.805 | 580,474 | 0 | 20 | yes | 1,419,526 | yes | 1994.195 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 5.416 | 541,590 | 0 | 20 | yes | 1,458,410 | yes | 1994.584 of 2000 |
| H-ADP | `backlog.service.adp.last.if0` | backlog | 0 | 18.328 | 1,832,833 | 0 | 20 | yes | 167,167 | yes | 1981.672 of 2000 |
| H-ADP | `control.discover.if0` | control | 0 | 0.132 | 13,193 | 0 | 20 | yes | 1,986,807 | no | 1999.868 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.first.if0` | hooks-load-notify | 0 | 4.539 | 453,858 | 0 | 20 | yes | 1,546,142 | yes | 1995.461 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.last.if0` | hooks-load-notify | 0 | 19.474 | 1,947,438 | 0 | 20 | yes | 52,562 | yes | 1980.526 of 2000 |
| H-AECP | `aecp.entity_available.if0` | aecp | 0 | 1.303 | 130,332 | 0 | 20 | yes | 1,869,668 | no | 238.697 of 240 |
| H-AECP | `aecp.get_avb_info.if0` | aecp | 0 | 1.321 | 132,116 | 0 | 20 | yes | 1,867,884 | no | 238.679 of 240 |
| H-AECP | `aecp.get_configuration.if0` | aecp | 0 | 1.284 | 128,431 | 0 | 20 | yes | 1,871,569 | no | 238.716 of 240 |
| H-AECP | `aecp.get_counters.if0` | aecp | 0 | 1.458 | 145,816 | 0 | 20 | yes | 1,854,184 | no | 238.542 of 240 |
| H-AECP | `aecp.get_name.if0` | aecp | 0 | 1.581 | 158,101 | 0 | 20 | yes | 1,841,899 | no | 238.419 of 240 |
| H-AECP | `aecp.lock_entity.if0` | aecp | 0 | 1.396 | 139,572 | 0 | 20 | yes | 1,860,428 | no | 238.604 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if0` | aecp | 0 | 0.883 | 88,289 | 0 | 20 | yes | 1,911,711 | no | 239.117 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if0` | aecp | 0 | 1.694 | 169,353 | 0 | 20 | yes | 1,830,647 | no | 238.306 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if0` | aecp | 0 | 1.425 | 142,452 | 0 | 20 | yes | 1,857,548 | no | 238.575 of 240 |
| H-AECP | `aecp.read_descriptor.t10.i2.c0.if0` | aecp | 0 | 1.406 | 140,614 | 0 | 20 | yes | 1,859,386 | no | 238.594 of 240 |
| H-AECP | `aecp.read_descriptor.t12.i0.c0.if0` | aecp | 0 | 1.390 | 138,994 | 0 | 20 | yes | 1,861,006 | no | 238.610 of 240 |
| H-AECP | `aecp.read_descriptor.t13.i0.c0.if0` | aecp | 0 | 1.866 | 186,570 | 0 | 20 | yes | 1,813,430 | no | 238.134 of 240 |
| H-AECP | `aecp.read_descriptor.t14.i0.c0.if0` | aecp | 0 | 1.326 | 132,646 | 0 | 20 | yes | 1,867,354 | no | 238.674 of 240 |
| H-AECP | `aecp.read_descriptor.t15.i0.c0.if0` | aecp | 0 | 1.327 | 132,722 | 0 | 20 | yes | 1,867,278 | no | 238.673 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if0` | aecp | 0 | 1.681 | 168,098 | 0 | 20 | yes | 1,831,902 | no | 238.319 of 240 |
| H-AECP | `aecp.read_descriptor.t20.i24.c0.if0` | aecp | 0 | 1.639 | 163,852 | 0 | 20 | yes | 1,836,148 | no | 238.361 of 240 |
| H-AECP | `aecp.read_descriptor.t26.i0.c0.if0` | aecp | 0 | 1.463 | 146,283 | 0 | 20 | yes | 1,853,717 | no | 238.537 of 240 |
| H-AECP | `aecp.read_descriptor.t36.i0.c0.if0` | aecp | 0 | 1.424 | 142,444 | 0 | 20 | yes | 1,857,556 | no | 238.576 of 240 |
| H-AECP | `aecp.read_descriptor.t5.i1.c0.if0` | aecp | 0 | 1.476 | 147,645 | 0 | 20 | yes | 1,852,355 | no | 238.524 of 240 |
| H-AECP | `aecp.read_descriptor.t6.i1.c0.if0` | aecp | 0 | 1.478 | 147,797 | 0 | 20 | yes | 1,852,203 | no | 238.522 of 240 |
| H-AECP | `aecp.read_descriptor.t9.i0.c0.if0` | aecp | 0 | 1.424 | 142,360 | 0 | 20 | yes | 1,857,640 | no | 238.576 of 240 |
| H-AECP | `aecp.register_unsolicited.if0` | aecp | 0 | 0.881 | 88,092 | 0 | 20 | yes | 1,911,908 | no | 239.119 of 240 |
| H-AECP | `aecp.set_name.if0` | aecp | 0 | 1.886 | 188,611 | 0 | 20 | yes | 1,811,389 | no | 238.114 of 240 |
| H-AECP | `aecp.unknown_command.if0` | aecp | 0 | 1.279 | 127,920 | 0 | 20 | yes | 1,872,080 | no | 238.721 of 240 |
| H-AECP | `aecp.unlock_entity.if0` | aecp | 0 | 1.396 | 139,573 | 0 | 20 | yes | 1,860,427 | no | 238.604 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.first.if0` | backlog-adp-refill | 0 | 5.048 | 504,811 | 0 | 20 | yes | 1,495,189 | yes | 234.952 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.last.if0` | backlog-adp-refill | 0 | 159.479 | 15,947,908 | 0 | 20 | NO | -13,947,908 | yes | 80.521 of 240 |
| H-AECP | `backlog-adp.service.aecp.first.if0` | backlog-adp | 0 | 5.048 | 504,811 | 0 | 20 | yes | 1,495,189 | yes | 234.952 of 240 |
| H-AECP | `backlog-adp.service.aecp.last.if0` | backlog-adp | 0 | 159.218 | 15,921,797 | 0 | 20 | NO | -13,921,797 | yes | 80.782 of 240 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 4.471 | 447,125 | 0 | 20 | yes | 1,552,875 | yes | 235.529 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if0` | backlog-owed | 0 | 85.818 | 8,581,826 | 0 | 20 | NO | -6,581,826 | yes | 154.182 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 5.409 | 540,916 | 0 | 20 | yes | 1,459,084 | yes | 234.591 of 240 |
| H-AECP | `backlog.service.aecp.last.if0` | backlog | 0 | 48.472 | 4,847,223 | 0 | 20 | NO | -2,847,223 | yes | 191.528 of 240 |
| H-AECP | `hooks-late-aecp.read_descriptor.if0` | hooks-late-aecp | 0 | 1.670 | 166,972 | 0 | 20 | yes | 1,833,028 | no | 238.330 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.first.if0` | hooks-load-notify | 0 | 4.497 | 449,749 | 0 | 20 | yes | 1,550,251 | yes | 235.503 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.last.if0` | hooks-load-notify | 0 | 60.110 | 6,011,015 | 0 | 20 | NO | -4,011,015 | yes | 179.890 of 240 |
| H-DISC | `acmp.entity_available.if0` | acmp-disc | 0 | 3.448 | 344,831 | 0 | 20 | yes | 1,655,169 | no | 196.552 of 200 |
| H-DISC | `acmp.entity_departing.if0` | acmp-disc | 0 | 8.403 | 840,323 | 0 | 20 | yes | 1,159,677 | no | 191.597 of 200 |
| H-DISC | `acmp.tmr_no_adp.if0` | acmp-disc | 0 | 1.059 | 105,931 | 0 | 20 | yes | 1,894,069 | no | 198.941 of 200 |
| H-DISC | `backlog.adp_available.if0` | backlog-adp | 0 | 24.784 | 2,478,423 | 0 | 20 | NO | -478,423 | yes | 175.216 of 200 |
| H-DISC | `backlog.adp_available_refill.if0` | backlog-adp-refill | 0 | 8.804 | 880,366 | 0 | 20 | yes | 1,119,634 | yes | 191.196 of 200 |
| H-DISC | `hooks-disc-aging.available.if0` | hooks-disc-aging | 0 | 7.243 | 724,301 | 0 | 20 | yes | 1,275,699 | no | 192.757 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if0` | hooks-disc-aging | 0 | 0.497 | 49,730 | 0 | 20 | yes | 1,950,270 | no | 199.503 of 200 |
| H-DISC | `hooks-late-disc.entity_departing.if0` | hooks-late-disc | 0 | 8.403 | 840,323 | 0 | 20 | yes | 1,159,677 | no | 191.597 of 200 |
| H-MAAP | `backlog-adp-refill.service.maap.first.if0` | backlog-adp-refill | 0 | 5.038 | 503,771 | 0 | 20 | yes | 1,496,229 | yes | 494.962 of 500 |
| H-MAAP | `backlog-adp-refill.service.maap.last.if0` | backlog-adp-refill | 0 | 29.155 | 2,915,461 | 0 | 20 | NO | -915,461 | yes | 470.845 of 500 |
| H-MAAP | `backlog-adp.service.maap.first.if0` | backlog-adp | 0 | 5.038 | 503,771 | 0 | 20 | yes | 1,496,229 | yes | 494.962 of 500 |
| H-MAAP | `backlog-adp.service.maap.last.if0` | backlog-adp | 0 | 29.433 | 2,943,290 | 0 | 20 | NO | -943,290 | yes | 470.567 of 500 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 4.461 | 446,085 | 0 | 20 | yes | 1,553,915 | yes | 495.539 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 18.154 | 1,815,364 | 0 | 20 | yes | 184,636 | yes | 481.846 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 5.399 | 539,876 | 0 | 20 | yes | 1,460,124 | yes | 494.601 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 18.313 | 1,831,338 | 0 | 20 | yes | 168,662 | yes | 481.687 of 500 |
| H-MAAP | `hooks-late-maap.defend.if0` | hooks-late-maap | 0 | 0.292 | 29,193 | 0 | 20 | yes | 1,970,807 | no | 499.708 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.first.if0` | hooks-load-notify | 0 | 4.532 | 453,184 | 0 | 20 | yes | 1,546,816 | yes | 495.468 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.last.if0` | hooks-load-notify | 0 | 19.470 | 1,946,983 | 0 | 20 | yes | 53,017 | yes | 480.530 of 500 |
| H-MAAP | `maap.announce.if0` | maap | 0 | 1.010 | 100,993 | 0 | 20 | yes | 1,899,007 | no | 498.990 of 500 |
| H-MAAP | `maap.defend.if0` | maap | 0 | 0.292 | 29,193 | 0 | 20 | yes | 1,970,807 | no | 499.708 of 500 |
| H-MAAP | `maap.probe1.if0` | maap | 0 | 0.364 | 36,368 | 0 | 20 | yes | 1,963,632 | no | 499.636 of 500 |
| H-MAAP | `maap.probe2.if0` | maap | 0 | 0.840 | 83,973 | 0 | 20 | yes | 1,916,027 | no | 499.160 of 500 |
| H-MAAP | `maap.probe3.if0` | maap | 0 | 0.469 | 46,869 | 0 | 20 | yes | 1,953,131 | no | 499.531 of 500 |
| H-MAAP | `maap.probe4.if0` | maap | 0 | 0.918 | 91,791 | 0 | 20 | yes | 1,908,209 | no | 499.082 of 500 |
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
| H-NOTIFY | `hooks-load-notify.set_name.if0` | hooks-load-notify | 0 | 59.375 | 5,937,521 | 0 | 20 | NO | -3,937,521 | yes | 180.625 of 240 |
| H-SRP | `backlog-adp-refill.service.srp.first.if0` | backlog-adp-refill | 0 | never | 54,878,893 | 0 | 18 | NO | -1 | yes | -368.789 of 180 |
| H-SRP | `backlog-adp-refill.service.srp.last.if0` | backlog-adp-refill | 0 | never | 54,876,878 | 0 | 18 | NO | -1 | yes | -368.769 of 180 |
| H-SRP | `backlog-adp.service.srp.first.if0` | backlog-adp | 0 | never | 52,482,034 | 0 | 18 | NO | -1 | yes | -344.820 of 180 |
| H-SRP | `backlog-adp.service.srp.last.if0` | backlog-adp | 0 | never | 52,480,019 | 0 | 18 | NO | -1 | yes | -344.800 of 180 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 9.793 | 979,308 | 0 | 18 | yes | 820,692 | yes | 170.207 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if0` | backlog-owed | 0 | 42.197 | 4,219,697 | 0 | 18 | NO | -2,419,697 | yes | 137.803 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 14.746 | 1,474,624 | 0 | 18 | yes | 325,376 | yes | 165.254 of 180 |
| H-SRP | `backlog.service.srp.last.if0` | backlog | 0 | 50.676 | 5,067,595 | 0 | 18 | NO | -3,267,595 | yes | 129.324 of 180 |
| H-SRP | `hooks-late-srp.listener_ready.if0` | hooks-late-srp | 0 | 1.241 | 124,085 | 0 | 18 | yes | 1,675,915 | no | 178.759 of 180 |
| H-SRP | `hooks-load-notify.service.srp.first.if0` | hooks-load-notify | 0 | 9.983 | 998,267 | 0 | 18 | yes | 801,733 | yes | 170.017 of 180 |
| H-SRP | `hooks-load-notify.service.srp.last.if0` | hooks-load-notify | 0 | 66.232 | 6,623,159 | 0 | 18 | NO | -4,823,159 | yes | 113.768 of 180 |
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
- LATE H-ACMP: hooks-load-notify.service.acmp.last.if0: 26.672 ms against its bound 20 ms (hooks-load-notify)
- LATE H-AECP: hooks-load-notify.service.aecp.last.if0: 60.110 ms against its bound 20 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.last.if0: 66.232 ms against its bound 18 ms (hooks-load-notify)
- LATE H-ACMP: backlog.acmp_command.if0: 22.573 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 25.013 ms against its bound 20 ms (backlog)
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
- LATE H-ACMP: backlog.owed.if0: 77.837 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind0.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind1.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind2.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind3.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog-owed.service.acmp.last.if0: 24.542 ms against its bound 20 ms (backlog-owed)
- LATE H-AECP: backlog-owed.service.aecp.last.if0: 85.818 ms against its bound 20 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.last.if0: 42.197 ms against its bound 18 ms (backlog-owed)
