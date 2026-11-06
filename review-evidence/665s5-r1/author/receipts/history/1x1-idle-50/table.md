### 1x1, CPU 50 MHz (the product split CPU clock), bus 100 MHz, face arm idle

| Hook | Paths | Over its bound | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Ordering check applied | Ordering findings |
|---|---:|---:|---|---|---:|---:|
| H-ADP | 28 | 5 | 1.114 (20), `adp.tmr_delay.if0`, margin 1998.9 of 2000 | 51.378 (20) **over its bound**, `backlog-adp.service.adp.last.if0`, margin 1948.6 of 2000 | 2 | 0 |
| H-DISC | 8 | 2 | 8.827 (20), `acmp.entity_available.if0`, margin 191.2 of 200 | 43.816 (20) **over its bound**, `backlog.adp_available.if0`, margin 156.2 of 200 | 1 | 0 |
| H-ACMP | 30 | 11 | 12.522 (20), `acmp.probe_tx_response.if0`, margin 187.5 of 200 | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -162.2 of 200 | 65 | 0 |
| H-AECP | 36 | 5 | 3.100 (20), `aecp.read_descriptor.t13.i0.c0.if0`, margin 236.9 of 240 | 255.507 (20) **over its bound**, `backlog-adp-refill.service.aecp.last.if0`, margin -15.5 of 240 | 7 | 0 |
| H-NOTIFY | 11 | 1 | 6.365 (20), `aecp_fanout.set_name.if0`, margin 233.6 of 240 | 94.719 (20) **over its bound**, `hooks-load-notify.set_name.if0`, margin 145.3 of 240 | 11 | 0 |
| H-COUNTERS | 0 | 0 | - | - | 0 | 0 |
| H-MAAP | 17 | 5 | 1.237 (20), `maap.announce.if0`, margin 498.8 of 500 | 51.415 (20) **over its bound**, `backlog-adp.service.maap.last.if0`, margin 448.6 of 500 | 44 | 0 |
| H-SRP | 15 | 9 | 3.219 (18), `srp.startup.if0`, margin 176.8 of 180 | never served (18) **over its bound**, `backlog-adp-refill.service.srp.first.if0`, margin -400.1 of 180 | 1 | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound ms | Within | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---|---|---:|
| H-ACMP | `acmp.bind_rx.if0` | acmp-cmd | 0 | 0.947 | 47,343 | 0 | 20 | yes | no | 199.053 of 200 |
| H-ACMP | `acmp.disconnect_tx.if0` | acmp-cmd | 0 | 9.415 | 470,731 | 0 | 20 | yes | no | 190.585 of 200 |
| H-ACMP | `acmp.get_rx_state.if0` | acmp-cmd | 0 | 9.647 | 482,344 | 0 | 20 | yes | no | 190.353 of 200 |
| H-ACMP | `acmp.get_tx_connection.if0` | acmp-cmd | 0 | 9.414 | 470,702 | 0 | 20 | yes | no | 190.586 of 200 |
| H-ACMP | `acmp.get_tx_state.if0` | acmp-cmd | 0 | 7.845 | 392,243 | 0 | 20 | yes | no | 192.155 of 200 |
| H-ACMP | `acmp.probe_tx.if0` | acmp-cmd | 0 | 9.756 | 487,812 | 0 | 20 | yes | no | 190.244 of 200 |
| H-ACMP | `acmp.probe_tx_response.if0` | acmp-cmd | 0 | 12.522 | 626,076 | 0 | 20 | yes | no | 187.478 of 200 |
| H-ACMP | `acmp.tmr_delay.if0` | acmp-noresp | 0 | 2.228 | 111,408 | 0 | 20 | yes | no | 197.772 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if0` | acmp-noresp | 0 | 1.242 | 62,100 | 0 | 20 | yes | no | 198.758 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if0` | acmp-noresp | 0 | 0.446 | 22,276 | 0 | 20 | yes | no | 199.554 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if0` | acmp-notk | 0 | 3.595 | 179,767 | 0 | 20 | yes | no | 196.405 of 200 |
| H-ACMP | `acmp.tmr_retry.if0` | acmp-noresp | 0 | 1.951 | 97,563 | 0 | 20 | yes | no | 198.049 of 200 |
| H-ACMP | `acmp.unbind_rx.if0` | acmp-cmd | 0 | 9.588 | 479,391 | 0 | 20 | yes | no | 190.412 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.first.if0` | backlog-adp-refill | 0 | 9.126 | 456,298 | 0 | 20 | yes | yes | 190.874 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.last.if0` | backlog-adp-refill | 0 | 87.252 | 4,362,610 | 0 | 20 | NO | yes | 112.748 of 200 |
| H-ACMP | `backlog-adp.service.acmp.first.if0` | backlog-adp | 0 | 9.126 | 456,298 | 0 | 20 | yes | yes | 190.874 of 200 |
| H-ACMP | `backlog-adp.service.acmp.last.if0` | backlog-adp | 0 | 86.811 | 4,340,559 | 0 | 20 | NO | yes | 113.189 of 200 |
| H-ACMP | `backlog-owed.service.acmp.first.if0` | backlog-owed | 0 | 7.274 | 363,720 | 0 | 20 | yes | yes | 192.726 of 200 |
| H-ACMP | `backlog-owed.service.acmp.last.if0` | backlog-owed | 0 | 40.512 | 2,025,590 | 0 | 20 | NO | yes | 159.488 of 200 |
| H-ACMP | `backlog.acmp_command.if0` | backlog | 0 | 36.685 | 1,834,226 | 0 | 20 | NO | yes | 163.315 of 200 |
| H-ACMP | `backlog.owed.if0` | backlog-owed | 0 | 93.829 | 4,691,458 | 0 | 20 | NO | yes | 106.171 of 200 |
| H-ACMP | `backlog.owed_behind0.if0` | backlog-owed | 0 | never | 18,110,071 | 0 | 20 | NO | yes | -162.201 of 200 |
| H-ACMP | `backlog.owed_behind1.if0` | backlog-owed | 0 | never | 18,110,033 | 0 | 20 | NO | yes | -162.201 of 200 |
| H-ACMP | `backlog.owed_behind2.if0` | backlog-owed | 0 | never | 18,109,996 | 0 | 20 | NO | yes | -162.200 of 200 |
| H-ACMP | `backlog.owed_behind3.if0` | backlog-owed | 0 | never | 18,109,958 | 0 | 20 | NO | yes | -162.199 of 200 |
| H-ACMP | `backlog.service.acmp.first.if0` | backlog | 0 | 8.679 | 433,927 | 0 | 20 | yes | yes | 191.321 of 200 |
| H-ACMP | `backlog.service.acmp.last.if0` | backlog | 0 | 40.699 | 2,034,932 | 0 | 20 | NO | yes | 159.301 of 200 |
| H-ACMP | `hooks-late-acmp.get_rx_state.if0` | hooks-late-acmp | 0 | 0.567 | 28,343 | 0 | 20 | yes | no | 199.433 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.first.if0` | hooks-load-notify | 0 | 6.796 | 339,778 | 0 | 20 | yes | yes | 193.204 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.last.if0` | hooks-load-notify | 0 | 41.667 | 2,083,372 | 0 | 20 | NO | yes | 158.333 of 200 |
| H-ADP | `adp.discover.if0` | adp-discover | 0 | 0.516 | 25,796 | 0 | 20 | yes | no | 1999.484 of 2000 |
| H-ADP | `adp.gm_change.if0` | adp-gm | 0 | 0.397 | 19,841 | 0 | 20 | yes | no | 1999.603 of 2000 |
| H-ADP | `adp.link_down.if0` | adp-link | 0 | 0.380 | 19,003 | 0 | 20 | yes | no | 1999.620 of 2000 |
| H-ADP | `adp.link_up.if0` | hooks-order-adp | 0 | 0.086 | 4,307 | 0 | 20 | yes | no | 1999.914 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-advertise | 0 | 0.086 | 4,307 | 0 | 20 | yes | no | 1999.914 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-link | 0 | 0.086 | 4,307 | 0 | 20 | yes | no | 1999.914 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-gm | 0 | 0.086 | 4,307 | 0 | 20 | yes | no | 1999.914 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-discover | 0 | 0.086 | 4,307 | 0 | 20 | yes | no | 1999.914 of 2000 |
| H-ADP | `adp.link_up.if0` | control | 0 | 0.086 | 4,307 | 0 | 20 | yes | no | 1999.914 of 2000 |
| H-ADP | `adp.tmr_advertise.if0` | adp-advertise | 0 | 0.436 | 21,823 | 0 | 20 | yes | no | 1999.564 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | hooks-order-adp | 0 | 1.114 | 55,683 | 0 | 20 | yes | no | 1998.886 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-advertise | 0 | 1.114 | 55,683 | 0 | 20 | yes | no | 1998.886 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-link | 0 | 1.114 | 55,683 | 0 | 20 | yes | no | 1998.886 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-gm | 0 | 1.114 | 55,683 | 0 | 20 | yes | no | 1998.886 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-discover | 0 | 1.114 | 55,683 | 0 | 20 | yes | no | 1998.886 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | control | 0 | 1.114 | 55,683 | 0 | 20 | yes | no | 1998.886 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.first.if0` | backlog-adp-refill | 0 | 9.117 | 455,842 | 0 | 20 | yes | yes | 1990.883 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.last.if0` | backlog-adp-refill | 0 | 47.296 | 2,364,804 | 0 | 20 | NO | yes | 1952.704 of 2000 |
| H-ADP | `backlog-adp.service.adp.first.if0` | backlog-adp | 0 | 9.117 | 455,842 | 0 | 20 | yes | yes | 1990.883 of 2000 |
| H-ADP | `backlog-adp.service.adp.last.if0` | backlog-adp | 0 | 51.378 | 2,568,919 | 0 | 20 | NO | yes | 1948.622 of 2000 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 7.317 | 365,849 | 0 | 20 | yes | yes | 1992.683 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if0` | backlog-owed | 0 | 29.308 | 1,465,405 | 0 | 20 | NO | yes | 1970.692 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 9.282 | 464,079 | 0 | 20 | yes | yes | 1990.718 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 8.721 | 436,056 | 0 | 20 | yes | yes | 1991.279 of 2000 |
| H-ADP | `backlog.service.adp.last.if0` | backlog | 0 | 29.980 | 1,499,015 | 0 | 20 | NO | yes | 1970.020 of 2000 |
| H-ADP | `control.discover.if0` | control | 0 | 0.516 | 25,796 | 0 | 20 | yes | no | 1999.484 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.first.if0` | hooks-load-notify | 0 | 6.828 | 341,388 | 0 | 20 | yes | yes | 1993.172 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.last.if0` | hooks-load-notify | 0 | 29.667 | 1,483,358 | 0 | 20 | NO | yes | 1970.333 of 2000 |
| H-AECP | `aecp.entity_available.if0` | aecp | 0 | 2.134 | 106,695 | 0 | 20 | yes | no | 237.866 of 240 |
| H-AECP | `aecp.get_avb_info.if0` | aecp | 0 | 2.158 | 107,910 | 0 | 20 | yes | no | 237.842 of 240 |
| H-AECP | `aecp.get_configuration.if0` | aecp | 0 | 2.097 | 104,868 | 0 | 20 | yes | no | 237.903 of 240 |
| H-AECP | `aecp.get_counters.if0` | aecp | 0 | 2.390 | 119,496 | 0 | 20 | yes | no | 237.610 of 240 |
| H-AECP | `aecp.get_name.if0` | aecp | 0 | 2.570 | 128,494 | 0 | 20 | yes | no | 237.430 of 240 |
| H-AECP | `aecp.lock_entity.if0` | aecp | 0 | 2.264 | 113,201 | 0 | 20 | yes | no | 237.736 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if0` | aecp | 0 | 1.410 | 70,519 | 0 | 20 | yes | no | 238.590 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if0` | aecp | 0 | 2.793 | 139,629 | 0 | 20 | yes | no | 237.207 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if0` | aecp | 0 | 2.338 | 116,921 | 0 | 20 | yes | no | 237.662 of 240 |
| H-AECP | `aecp.read_descriptor.t10.i2.c0.if0` | aecp | 0 | 2.306 | 115,317 | 0 | 20 | yes | no | 237.694 of 240 |
| H-AECP | `aecp.read_descriptor.t12.i0.c0.if0` | aecp | 0 | 2.592 | 129,612 | 0 | 20 | yes | no | 237.408 of 240 |
| H-AECP | `aecp.read_descriptor.t13.i0.c0.if0` | aecp | 0 | 3.100 | 155,025 | 0 | 20 | yes | no | 236.899 of 240 |
| H-AECP | `aecp.read_descriptor.t14.i0.c0.if0` | aecp | 0 | 2.169 | 108,433 | 0 | 20 | yes | no | 237.831 of 240 |
| H-AECP | `aecp.read_descriptor.t15.i0.c0.if0` | aecp | 0 | 2.484 | 124,203 | 0 | 20 | yes | no | 237.516 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if0` | aecp | 0 | 2.431 | 121,553 | 0 | 20 | yes | no | 237.569 of 240 |
| H-AECP | `aecp.read_descriptor.t20.i24.c0.if0` | aecp | 0 | 2.356 | 117,803 | 0 | 20 | yes | no | 237.644 of 240 |
| H-AECP | `aecp.read_descriptor.t26.i0.c0.if0` | aecp | 0 | 2.403 | 120,170 | 0 | 20 | yes | no | 237.597 of 240 |
| H-AECP | `aecp.read_descriptor.t36.i0.c0.if0` | aecp | 0 | 2.652 | 132,612 | 0 | 20 | yes | no | 237.348 of 240 |
| H-AECP | `aecp.read_descriptor.t5.i1.c0.if0` | aecp | 0 | 2.428 | 121,404 | 0 | 20 | yes | no | 237.572 of 240 |
| H-AECP | `aecp.read_descriptor.t6.i1.c0.if0` | aecp | 0 | 2.744 | 137,177 | 0 | 20 | yes | no | 237.256 of 240 |
| H-AECP | `aecp.read_descriptor.t9.i0.c0.if0` | aecp | 0 | 2.337 | 116,835 | 0 | 20 | yes | no | 237.663 of 240 |
| H-AECP | `aecp.register_unsolicited.if0` | aecp | 0 | 1.407 | 70,366 | 0 | 20 | yes | no | 238.593 of 240 |
| H-AECP | `aecp.set_name.if0` | aecp | 0 | 2.742 | 137,078 | 0 | 20 | yes | no | 237.258 of 240 |
| H-AECP | `aecp.unknown_command.if0` | aecp | 0 | 2.406 | 120,323 | 0 | 20 | yes | no | 237.594 of 240 |
| H-AECP | `aecp.unlock_entity.if0` | aecp | 0 | 2.581 | 129,034 | 0 | 20 | yes | no | 237.419 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.first.if0` | backlog-adp-refill | 0 | 9.162 | 458,090 | 0 | 20 | yes | yes | 230.838 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.last.if0` | backlog-adp-refill | 0 | 255.507 | 12,775,341 | 0 | 20 | NO | yes | -15.507 of 240 |
| H-AECP | `backlog-adp.service.aecp.first.if0` | backlog-adp | 0 | 9.162 | 458,090 | 0 | 20 | yes | yes | 230.838 of 240 |
| H-AECP | `backlog-adp.service.aecp.last.if0` | backlog-adp | 0 | 255.063 | 12,753,127 | 0 | 20 | NO | yes | -15.063 of 240 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 7.310 | 365,512 | 0 | 20 | yes | yes | 232.690 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if0` | backlog-owed | 0 | 106.873 | 5,343,657 | 0 | 20 | NO | yes | 133.127 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 8.714 | 435,719 | 0 | 20 | yes | yes | 231.286 of 240 |
| H-AECP | `backlog.service.aecp.last.if0` | backlog | 0 | 79.461 | 3,973,051 | 0 | 20 | NO | yes | 160.539 of 240 |
| H-AECP | `hooks-late-aecp.read_descriptor.if0` | hooks-late-aecp | 0 | 2.767 | 138,333 | 0 | 20 | yes | no | 237.233 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.first.if0` | hooks-load-notify | 0 | 6.787 | 339,333 | 0 | 20 | yes | yes | 233.213 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.last.if0` | hooks-load-notify | 0 | 95.883 | 4,794,165 | 0 | 20 | NO | yes | 144.117 of 240 |
| H-DISC | `acmp.entity_available.if0` | acmp-disc | 0 | 8.827 | 441,347 | 0 | 20 | yes | no | 191.173 of 200 |
| H-DISC | `acmp.entity_departing.if0` | acmp-disc | 0 | 6.408 | 320,382 | 0 | 20 | yes | no | 193.592 of 200 |
| H-DISC | `acmp.tmr_no_adp.if0` | acmp-disc | 0 | 2.124 | 106,189 | 0 | 20 | yes | no | 197.876 of 200 |
| H-DISC | `backlog.adp_available.if0` | backlog-adp | 0 | 43.816 | 2,190,781 | 0 | 20 | NO | yes | 156.184 of 200 |
| H-DISC | `backlog.adp_available_refill.if0` | backlog-adp-refill | 0 | 40.148 | 2,007,415 | 0 | 20 | NO | yes | 159.852 of 200 |
| H-DISC | `hooks-disc-aging.available.if0` | hooks-disc-aging | 0 | 2.343 | 117,159 | 0 | 20 | yes | no | 197.657 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if0` | hooks-disc-aging | 0 | 1.411 | 70,548 | 0 | 20 | yes | no | 198.589 of 200 |
| H-DISC | `hooks-late-disc.entity_departing.if0` | hooks-late-disc | 0 | 6.408 | 320,382 | 0 | 20 | yes | no | 193.592 of 200 |
| H-MAAP | `backlog-adp-refill.service.maap.first.if0` | backlog-adp-refill | 0 | 9.151 | 457,570 | 0 | 20 | yes | yes | 490.849 of 500 |
| H-MAAP | `backlog-adp-refill.service.maap.last.if0` | backlog-adp-refill | 0 | 50.992 | 2,549,590 | 0 | 20 | NO | yes | 449.008 of 500 |
| H-MAAP | `backlog-adp.service.maap.first.if0` | backlog-adp | 0 | 9.151 | 457,570 | 0 | 20 | yes | yes | 490.849 of 500 |
| H-MAAP | `backlog-adp.service.maap.last.if0` | backlog-adp | 0 | 51.415 | 2,570,757 | 0 | 20 | NO | yes | 448.585 of 500 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 7.300 | 364,992 | 0 | 20 | yes | yes | 492.700 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 29.293 | 1,464,657 | 0 | 20 | NO | yes | 470.707 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 8.704 | 435,199 | 0 | 20 | yes | yes | 491.296 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 29.965 | 1,498,267 | 0 | 20 | NO | yes | 470.035 of 500 |
| H-MAAP | `hooks-late-maap.defend.if0` | hooks-late-maap | 0 | 0.454 | 22,695 | 0 | 20 | yes | no | 499.546 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.first.if0` | hooks-load-notify | 0 | 6.821 | 341,051 | 0 | 20 | yes | yes | 493.179 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.last.if0` | hooks-load-notify | 0 | 29.663 | 1,483,131 | 0 | 20 | NO | yes | 470.337 of 500 |
| H-MAAP | `maap.announce.if0` | maap | 0 | 1.237 | 61,836 | 0 | 20 | yes | no | 498.763 of 500 |
| H-MAAP | `maap.defend.if0` | maap | 0 | 0.771 | 38,528 | 0 | 20 | yes | no | 499.229 of 500 |
| H-MAAP | `maap.probe1.if0` | maap | 0 | 0.565 | 28,275 | 0 | 20 | yes | no | 499.435 of 500 |
| H-MAAP | `maap.probe2.if0` | maap | 0 | 1.184 | 59,193 | 0 | 20 | yes | no | 498.816 of 500 |
| H-MAAP | `maap.probe3.if0` | maap | 0 | 0.661 | 33,052 | 0 | 20 | yes | no | 499.339 of 500 |
| H-MAAP | `maap.probe4.if0` | maap | 0 | 1.084 | 54,193 | 0 | 20 | yes | no | 498.916 of 500 |
| H-NOTIFY | `aecp_fanout.add_audio_mappings.if0` | aecp-fanout | 0 | 4.752 | 237,599 | 0 | 20 | yes | no | 235.248 of 240 |
| H-NOTIFY | `aecp_fanout.lock_entity.if0` | aecp-fanout | 0 | 4.634 | 231,684 | 0 | 20 | yes | no | 235.366 of 240 |
| H-NOTIFY | `aecp_fanout.remove_audio_mappings.if0` | aecp-fanout | 0 | 4.759 | 237,931 | 0 | 20 | yes | no | 235.241 of 240 |
| H-NOTIFY | `aecp_fanout.set_clock_source.if0` | aecp-fanout | 0 | 4.565 | 228,226 | 0 | 20 | yes | no | 235.435 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_off.if0` | aecp-fanout | 0 | 4.399 | 219,959 | 0 | 20 | yes | no | 235.601 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_on.if0` | aecp-fanout | 0 | 4.399 | 219,938 | 0 | 20 | yes | no | 235.601 of 240 |
| H-NOTIFY | `aecp_fanout.set_name.if0` | aecp-fanout | 0 | 6.365 | 318,257 | 0 | 20 | yes | no | 233.635 of 240 |
| H-NOTIFY | `aecp_fanout.set_sampling_rate.if0` | aecp-fanout | 0 | 4.404 | 220,195 | 0 | 20 | yes | no | 235.596 of 240 |
| H-NOTIFY | `aecp_fanout.unlock_entity.if0` | aecp-fanout | 0 | 4.640 | 232,004 | 0 | 20 | yes | no | 235.360 of 240 |
| H-NOTIFY | `hooks-late-notify.set_name.if0` | hooks-late-notify | 0 | 6.365 | 318,257 | 0 | 20 | yes | no | 233.635 of 240 |
| H-NOTIFY | `hooks-load-notify.set_name.if0` | hooks-load-notify | 0 | 94.719 | 4,735,966 | 0 | 20 | NO | yes | 145.281 of 240 |
| H-SRP | `backlog-adp-refill.service.srp.first.if0` | backlog-adp-refill | 0 | never | 29,006,679 | 0 | 18 | NO | yes | -400.134 of 180 |
| H-SRP | `backlog-adp-refill.service.srp.last.if0` | backlog-adp-refill | 0 | never | 29,005,671 | 0 | 18 | NO | yes | -400.113 of 180 |
| H-SRP | `backlog-adp.service.srp.first.if0` | backlog-adp | 0 | never | 27,192,587 | 0 | 18 | NO | yes | -363.852 of 180 |
| H-SRP | `backlog-adp.service.srp.last.if0` | backlog-adp | 0 | never | 27,191,579 | 0 | 18 | NO | yes | -363.832 of 180 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 15.794 | 789,689 | 0 | 18 | yes | yes | 164.206 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if0` | backlog-owed | 0 | 83.231 | 4,161,563 | 0 | 18 | NO | yes | 96.769 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 23.814 | 1,190,715 | 0 | 18 | NO | yes | 156.186 of 180 |
| H-SRP | `backlog.service.srp.last.if0` | backlog | 0 | 86.728 | 4,336,387 | 0 | 18 | NO | yes | 93.272 of 180 |
| H-SRP | `hooks-late-srp.listener_ready.if0` | hooks-late-srp | 0 | 1.904 | 95,190 | 0 | 18 | yes | no | 178.096 of 180 |
| H-SRP | `hooks-load-notify.service.srp.first.if0` | hooks-load-notify | 0 | 22.086 | 1,104,313 | 0 | 18 | NO | yes | 157.914 of 180 |
| H-SRP | `hooks-load-notify.service.srp.last.if0` | hooks-load-notify | 0 | 110.972 | 5,548,591 | 0 | 18 | NO | yes | 69.028 of 180 |
| H-SRP | `srp.domain.if0` | srp | 0 | 3.241 | 162,026 | 200 | 218 | yes | no | -23.241 of 180 |
| H-SRP | `srp.listener_ready.if0` | srp | 0 | 1.904 | 95,190 | 0 | 18 | yes | no | 178.096 of 180 |
| H-SRP | `srp.malformed.if0` | srp | 0 | 1.596 | 79,780 | 0 | 18 | yes | no | 178.404 of 180 |
| H-SRP | `srp.startup.if0` | srp | 0 | 3.219 | 160,972 | 0 | 18 | yes | no | 176.781 of 180 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- none

Findings:

- LATE H-NOTIFY: hooks-load-notify.set_name.if0: 94.719 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ADP: hooks-load-notify.service.adp.last.if0: 29.667 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ACMP: hooks-load-notify.service.acmp.last.if0: 41.667 ms against its bound 20 ms (hooks-load-notify)
- LATE H-AECP: hooks-load-notify.service.aecp.last.if0: 95.883 ms against its bound 20 ms (hooks-load-notify)
- LATE H-MAAP: hooks-load-notify.service.maap.last.if0: 29.663 ms against its bound 20 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.first.if0: 22.086 ms against its bound 18 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.last.if0: 110.972 ms against its bound 18 ms (hooks-load-notify)
- LATE H-ACMP: backlog.acmp_command.if0: 36.685 ms against its bound 20 ms (backlog)
- LATE H-ADP: backlog.service.adp.last.if0: 29.980 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 40.699 ms against its bound 20 ms (backlog)
- LATE H-AECP: backlog.service.aecp.last.if0: 79.461 ms against its bound 20 ms (backlog)
- LATE H-MAAP: backlog.service.maap.last.if0: 29.965 ms against its bound 20 ms (backlog)
- LATE H-SRP: backlog.service.srp.first.if0: 23.814 ms against its bound 18 ms (backlog)
- LATE H-SRP: backlog.service.srp.last.if0: 86.728 ms against its bound 18 ms (backlog)
- LATE H-DISC: backlog.adp_available.if0: 43.816 ms against its bound 20 ms (backlog-adp)
- LATE H-ADP: backlog-adp.service.adp.last.if0: 51.378 ms against its bound 20 ms (backlog-adp)
- LATE H-ACMP: backlog-adp.service.acmp.last.if0: 86.811 ms against its bound 20 ms (backlog-adp)
- LATE H-AECP: backlog-adp.service.aecp.last.if0: 255.063 ms against its bound 20 ms (backlog-adp)
- LATE H-MAAP: backlog-adp.service.maap.last.if0: 51.415 ms against its bound 20 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.first.if0: never served against its bound 18 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.last.if0: never served against its bound 18 ms (backlog-adp)
- LATE H-DISC: backlog.adp_available_refill.if0: 40.148 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-ADP: backlog-adp-refill.service.adp.last.if0: 47.296 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-ACMP: backlog-adp-refill.service.acmp.last.if0: 87.252 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-AECP: backlog-adp-refill.service.aecp.last.if0: 255.507 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-MAAP: backlog-adp-refill.service.maap.last.if0: 50.992 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.first.if0: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.last.if0: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-ACMP: backlog.owed.if0: 93.829 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind0.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind1.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind2.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind3.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ADP: backlog-owed.service.adp.last.if0: 29.308 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog-owed.service.acmp.last.if0: 40.512 ms against its bound 20 ms (backlog-owed)
- LATE H-AECP: backlog-owed.service.aecp.last.if0: 106.873 ms against its bound 20 ms (backlog-owed)
- LATE H-MAAP: backlog-owed.service.maap.last.if0: 29.293 ms against its bound 20 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.last.if0: 83.231 ms against its bound 18 ms (backlog-owed)
