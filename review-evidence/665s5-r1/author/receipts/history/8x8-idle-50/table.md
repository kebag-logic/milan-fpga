### 8x8, CPU 50 MHz (the product split CPU clock), bus 100 MHz, face arm idle

| Hook | Paths | Over its bound | Worst alone, ms (bound) | Worst under the composed load, ms (bound) | Ordering check applied | Ordering findings |
|---|---:|---:|---|---|---:|---:|
| H-ADP | 44 | 5 | 5.209 (20), `adp.link_down.if1`, margin 1994.8 of 2000 | 64.466 (20) **over its bound**, `backlog-adp-refill.service.adp.last.if0`, margin 1935.5 of 2000 | 4 | 0 |
| H-DISC | 12 | 6 | 24.150 (20) **over its bound**, `acmp.entity_available.if1`, margin 175.9 of 200 | 53.855 (20) **over its bound**, `backlog.adp_available_refill.if0`, margin 146.1 of 200 | 2 | 0 |
| H-ACMP | 43 | 11 | 19.058 (20), `acmp.bind_rx.if1`, margin 180.9 of 200 | never served (20) **over its bound**, `backlog.owed_behind0.if0`, margin -170.3 of 200 | 68 | 0 |
| H-AECP | 50 | 5 | 4.351 (20), `aecp.set_name.if0`, margin 235.6 of 240 | 315.061 (20) **over its bound**, `backlog-adp-refill.service.aecp.last.if1`, margin -75.1 of 240 | 14 | 0 |
| H-NOTIFY | 15 | 1 | 11.876 (20), `aecp_fanout.set_name.if0`, margin 228.1 of 240 | 138.874 (20) **over its bound**, `hooks-load-notify.set_name.if0`, margin 101.1 of 240 | 15 | 0 |
| H-COUNTERS | 0 | 0 | - | - | 0 | 0 |
| H-MAAP | 23 | 5 | 2.439 (20), `maap.probe2.if1`, margin 497.6 of 500 | 59.343 (20) **over its bound**, `backlog-adp.service.maap.last.if0`, margin 440.7 of 500 | 44 | 0 |
| H-SRP | 19 | 10 | 6.531 (18), `srp.startup.if1`, margin 173.5 of 180 | never served (18) **over its bound**, `backlog-adp-refill.service.srp.first.if0`, margin -413.8 of 180 | 2 | 0 |

| Hook | Path | Group | Interface | ms | CPU cycles | W ms | Bound ms | Within | Under load | Margin to the normative timeout, ms |
|---|---|---|---:|---:|---:|---:|---:|---|---|---:|
| H-ACMP | `acmp.bind_rx.if0` | acmp-cmd | 0 | 1.010 | 50,509 | 0 | 20 | yes | no | 198.990 of 200 |
| H-ACMP | `acmp.bind_rx.if1` | acmp-cmd | 1 | 19.058 | 952,903 | 0 | 20 | yes | no | 180.942 of 200 |
| H-ACMP | `acmp.disconnect_tx.if0` | acmp-cmd | 0 | 16.428 | 821,379 | 0 | 20 | yes | no | 183.572 of 200 |
| H-ACMP | `acmp.disconnect_tx.if1` | acmp-cmd | 1 | 5.027 | 251,332 | 0 | 20 | yes | no | 194.973 of 200 |
| H-ACMP | `acmp.get_rx_state.if0` | acmp-cmd | 0 | 16.713 | 835,650 | 0 | 20 | yes | no | 183.287 of 200 |
| H-ACMP | `acmp.get_rx_state.if1` | acmp-cmd | 1 | 5.811 | 290,531 | 0 | 20 | yes | no | 194.189 of 200 |
| H-ACMP | `acmp.get_tx_connection.if0` | acmp-cmd | 0 | 16.448 | 822,411 | 0 | 20 | yes | no | 183.552 of 200 |
| H-ACMP | `acmp.get_tx_connection.if1` | acmp-cmd | 1 | 8.819 | 440,969 | 0 | 20 | yes | no | 191.181 of 200 |
| H-ACMP | `acmp.get_tx_state.if0` | acmp-cmd | 0 | 18.655 | 932,734 | 0 | 20 | yes | no | 181.345 of 200 |
| H-ACMP | `acmp.get_tx_state.if1` | acmp-cmd | 1 | 8.863 | 443,162 | 0 | 20 | yes | no | 191.137 of 200 |
| H-ACMP | `acmp.probe_tx.if0` | acmp-cmd | 0 | 16.835 | 841,728 | 0 | 20 | yes | no | 183.165 of 200 |
| H-ACMP | `acmp.probe_tx.if1` | acmp-cmd | 1 | 5.390 | 269,492 | 0 | 20 | yes | no | 194.610 of 200 |
| H-ACMP | `acmp.probe_tx_response.if0` | acmp-cmd | 0 | 4.465 | 223,235 | 0 | 20 | yes | no | 195.535 of 200 |
| H-ACMP | `acmp.probe_tx_response.if1` | acmp-cmd | 1 | 3.318 | 165,918 | 0 | 20 | yes | no | 196.682 of 200 |
| H-ACMP | `acmp.tmr_delay.if0` | acmp-noresp | 0 | 2.173 | 108,673 | 0 | 20 | yes | no | 197.827 of 200 |
| H-ACMP | `acmp.tmr_delay.if1` | acmp-noresp | 1 | 1.910 | 95,484 | 0 | 20 | yes | no | 198.090 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if0` | acmp-noresp | 0 | 2.778 | 138,901 | 0 | 20 | yes | no | 197.222 of 200 |
| H-ACMP | `acmp.tmr_no_resp1.if1` | acmp-noresp | 1 | 7.637 | 381,866 | 0 | 20 | yes | no | 192.363 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if0` | acmp-noresp | 0 | 2.837 | 141,829 | 0 | 20 | yes | no | 197.163 of 200 |
| H-ACMP | `acmp.tmr_no_resp2.if1` | acmp-noresp | 1 | 6.577 | 328,852 | 0 | 20 | yes | no | 193.423 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if0` | acmp-notk | 0 | 3.779 | 188,958 | 0 | 20 | yes | no | 196.221 of 200 |
| H-ACMP | `acmp.tmr_no_tk.if1` | acmp-notk | 1 | 8.820 | 440,979 | 0 | 20 | yes | no | 191.180 of 200 |
| H-ACMP | `acmp.tmr_retry.if0` | acmp-noresp | 0 | 2.060 | 103,022 | 0 | 20 | yes | no | 197.940 of 200 |
| H-ACMP | `acmp.tmr_retry.if1` | acmp-noresp | 1 | 2.233 | 111,645 | 0 | 20 | yes | no | 197.767 of 200 |
| H-ACMP | `acmp.unbind_rx.if0` | acmp-cmd | 0 | 14.498 | 724,876 | 0 | 20 | yes | no | 185.502 of 200 |
| H-ACMP | `acmp.unbind_rx.if1` | acmp-cmd | 1 | 13.450 | 672,503 | 0 | 20 | yes | no | 186.550 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.first.if0` | backlog-adp-refill | 0 | 12.374 | 618,681 | 0 | 20 | yes | yes | 187.626 of 200 |
| H-ACMP | `backlog-adp-refill.service.acmp.last.if0` | backlog-adp-refill | 0 | 104.422 | 5,221,115 | 0 | 20 | NO | yes | 95.578 of 200 |
| H-ACMP | `backlog-adp.service.acmp.first.if0` | backlog-adp | 0 | 12.374 | 618,681 | 0 | 20 | yes | yes | 187.626 of 200 |
| H-ACMP | `backlog-adp.service.acmp.last.if0` | backlog-adp | 0 | 103.970 | 5,198,512 | 0 | 20 | NO | yes | 96.030 of 200 |
| H-ACMP | `backlog-owed.service.acmp.first.if0` | backlog-owed | 0 | 10.329 | 516,468 | 0 | 20 | yes | yes | 189.671 of 200 |
| H-ACMP | `backlog-owed.service.acmp.last.if0` | backlog-owed | 0 | 60.869 | 3,043,472 | 0 | 20 | NO | yes | 139.131 of 200 |
| H-ACMP | `backlog.acmp_command.if0` | backlog | 0 | 59.382 | 2,969,108 | 0 | 20 | NO | yes | 140.618 of 200 |
| H-ACMP | `backlog.owed.if0` | backlog-owed | 0 | 119.606 | 5,980,322 | 0 | 20 | NO | yes | 80.394 of 200 |
| H-ACMP | `backlog.owed_behind0.if0` | backlog-owed | 0 | never | 18,513,317 | 0 | 20 | NO | yes | -170.266 of 200 |
| H-ACMP | `backlog.owed_behind1.if0` | backlog-owed | 0 | never | 18,513,279 | 0 | 20 | NO | yes | -170.266 of 200 |
| H-ACMP | `backlog.owed_behind2.if0` | backlog-owed | 0 | never | 18,513,242 | 0 | 20 | NO | yes | -170.265 of 200 |
| H-ACMP | `backlog.owed_behind3.if0` | backlog-owed | 0 | never | 18,513,204 | 0 | 20 | NO | yes | -170.264 of 200 |
| H-ACMP | `backlog.service.acmp.first.if0` | backlog | 0 | 14.481 | 724,042 | 0 | 20 | yes | yes | 185.519 of 200 |
| H-ACMP | `backlog.service.acmp.last.if0` | backlog | 0 | 65.203 | 3,260,159 | 0 | 20 | NO | yes | 134.797 of 200 |
| H-ACMP | `hooks-late-acmp.get_rx_state.if0` | hooks-late-acmp | 0 | 0.584 | 29,200 | 0 | 20 | yes | no | 199.416 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.first.if0` | hooks-load-notify | 0 | 10.936 | 546,794 | 0 | 20 | yes | yes | 189.064 of 200 |
| H-ACMP | `hooks-load-notify.service.acmp.last.if0` | hooks-load-notify | 0 | 64.743 | 3,237,171 | 0 | 20 | NO | yes | 135.257 of 200 |
| H-ADP | `adp.discover.if0` | adp-discover | 0 | 0.202 | 10,088 | 0 | 20 | yes | no | 1999.798 of 2000 |
| H-ADP | `adp.discover.if1` | adp-discover | 1 | 0.379 | 18,947 | 0 | 20 | yes | no | 1999.621 of 2000 |
| H-ADP | `adp.gm_change.if0` | adp-gm | 0 | 0.076 | 3,798 | 0 | 20 | yes | no | 1999.924 of 2000 |
| H-ADP | `adp.gm_change.if1` | adp-gm | 1 | 0.160 | 7,997 | 0 | 20 | yes | no | 1999.840 of 2000 |
| H-ADP | `adp.link_down.if0` | adp-link | 0 | 0.062 | 3,117 | 0 | 20 | yes | no | 1999.938 of 2000 |
| H-ADP | `adp.link_down.if1` | adp-link | 1 | 5.209 | 260,451 | 0 | 20 | yes | no | 1994.791 of 2000 |
| H-ADP | `adp.link_up.if0` | hooks-order-adp | 0 | 0.075 | 3,775 | 0 | 20 | yes | no | 1999.925 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-advertise | 0 | 0.075 | 3,775 | 0 | 20 | yes | no | 1999.925 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-link | 0 | 0.075 | 3,775 | 0 | 20 | yes | no | 1999.925 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-gm | 0 | 0.075 | 3,775 | 0 | 20 | yes | no | 1999.925 of 2000 |
| H-ADP | `adp.link_up.if0` | adp-discover | 0 | 0.075 | 3,775 | 0 | 20 | yes | no | 1999.925 of 2000 |
| H-ADP | `adp.link_up.if0` | control | 0 | 0.075 | 3,775 | 0 | 20 | yes | no | 1999.925 of 2000 |
| H-ADP | `adp.link_up.if1` | hooks-order-adp | 1 | 0.878 | 43,883 | 0 | 20 | yes | no | 1999.122 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-advertise | 1 | 0.878 | 43,883 | 0 | 20 | yes | no | 1999.122 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-link | 1 | 0.878 | 43,883 | 0 | 20 | yes | no | 1999.122 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-gm | 1 | 0.878 | 43,883 | 0 | 20 | yes | no | 1999.122 of 2000 |
| H-ADP | `adp.link_up.if1` | adp-discover | 1 | 0.878 | 43,883 | 0 | 20 | yes | no | 1999.122 of 2000 |
| H-ADP | `adp.link_up.if1` | control | 1 | 0.878 | 43,883 | 0 | 20 | yes | no | 1999.122 of 2000 |
| H-ADP | `adp.tmr_advertise.if0` | adp-advertise | 0 | 0.953 | 47,625 | 0 | 20 | yes | no | 1999.047 of 2000 |
| H-ADP | `adp.tmr_advertise.if1` | adp-advertise | 1 | 0.864 | 43,202 | 0 | 20 | yes | no | 1999.136 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | hooks-order-adp | 0 | 1.224 | 61,196 | 0 | 20 | yes | no | 1998.776 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-advertise | 0 | 1.224 | 61,196 | 0 | 20 | yes | no | 1998.776 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-link | 0 | 1.224 | 61,196 | 0 | 20 | yes | no | 1998.776 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-gm | 0 | 1.224 | 61,196 | 0 | 20 | yes | no | 1998.776 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | adp-discover | 0 | 1.224 | 61,196 | 0 | 20 | yes | no | 1998.776 of 2000 |
| H-ADP | `adp.tmr_delay.if0` | control | 0 | 1.224 | 61,196 | 0 | 20 | yes | no | 1998.776 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | hooks-order-adp | 1 | 0.615 | 30,726 | 0 | 20 | yes | no | 1999.385 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-advertise | 1 | 0.615 | 30,726 | 0 | 20 | yes | no | 1999.385 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-link | 1 | 0.615 | 30,726 | 0 | 20 | yes | no | 1999.385 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-gm | 1 | 0.615 | 30,726 | 0 | 20 | yes | no | 1999.385 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | adp-discover | 1 | 0.615 | 30,726 | 0 | 20 | yes | no | 1999.385 of 2000 |
| H-ADP | `adp.tmr_delay.if1` | control | 1 | 0.615 | 30,726 | 0 | 20 | yes | no | 1999.385 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.first.if0` | backlog-adp-refill | 0 | 12.364 | 618,225 | 0 | 20 | yes | yes | 1987.636 of 2000 |
| H-ADP | `backlog-adp-refill.service.adp.last.if0` | backlog-adp-refill | 0 | 64.466 | 3,223,309 | 0 | 20 | NO | yes | 1935.534 of 2000 |
| H-ADP | `backlog-adp.service.adp.first.if0` | backlog-adp | 0 | 12.364 | 618,225 | 0 | 20 | yes | yes | 1987.636 of 2000 |
| H-ADP | `backlog-adp.service.adp.last.if0` | backlog-adp | 0 | 59.306 | 2,965,298 | 0 | 20 | NO | yes | 1940.694 of 2000 |
| H-ADP | `backlog-owed.service.adp.first.if0` | backlog-owed | 0 | 10.372 | 518,597 | 0 | 20 | yes | yes | 1989.628 of 2000 |
| H-ADP | `backlog-owed.service.adp.last.if1` | backlog-owed | 1 | 43.350 | 2,167,482 | 0 | 20 | NO | yes | 1956.650 of 2000 |
| H-ADP | `backlog.event.if0` | backlog | 0 | 15.013 | 750,672 | 0 | 20 | yes | yes | 1984.987 of 2000 |
| H-ADP | `backlog.service.adp.first.if0` | backlog | 0 | 14.523 | 726,171 | 0 | 20 | yes | yes | 1985.477 of 2000 |
| H-ADP | `backlog.service.adp.last.if1` | backlog | 1 | 48.610 | 2,430,484 | 0 | 20 | NO | yes | 1951.390 of 2000 |
| H-ADP | `control.discover.if0` | control | 0 | 0.202 | 10,088 | 0 | 20 | yes | no | 1999.798 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.first.if0` | hooks-load-notify | 0 | 10.968 | 548,404 | 0 | 20 | yes | yes | 1989.032 of 2000 |
| H-ADP | `hooks-load-notify.service.adp.last.if1` | hooks-load-notify | 1 | 44.771 | 2,238,574 | 0 | 20 | NO | yes | 1955.229 of 2000 |
| H-AECP | `aecp.entity_available.if0` | aecp | 0 | 2.519 | 125,931 | 0 | 20 | yes | no | 237.481 of 240 |
| H-AECP | `aecp.entity_available.if1` | aecp | 1 | 2.956 | 147,781 | 0 | 20 | yes | no | 237.044 of 240 |
| H-AECP | `aecp.get_avb_info.if0` | aecp | 0 | 2.750 | 137,493 | 0 | 20 | yes | no | 237.250 of 240 |
| H-AECP | `aecp.get_avb_info.if1` | aecp | 1 | 2.639 | 131,926 | 0 | 20 | yes | no | 237.361 of 240 |
| H-AECP | `aecp.get_configuration.if0` | aecp | 0 | 2.907 | 145,351 | 0 | 20 | yes | no | 237.093 of 240 |
| H-AECP | `aecp.get_configuration.if1` | aecp | 1 | 2.479 | 123,928 | 0 | 20 | yes | no | 237.521 of 240 |
| H-AECP | `aecp.get_counters.if0` | aecp | 0 | 2.796 | 139,782 | 0 | 20 | yes | no | 237.204 of 240 |
| H-AECP | `aecp.get_counters.if1` | aecp | 1 | 2.791 | 139,569 | 0 | 20 | yes | no | 237.209 of 240 |
| H-AECP | `aecp.get_name.if0` | aecp | 0 | 2.636 | 131,818 | 0 | 20 | yes | no | 237.364 of 240 |
| H-AECP | `aecp.get_name.if1` | aecp | 1 | 2.632 | 131,605 | 0 | 20 | yes | no | 237.368 of 240 |
| H-AECP | `aecp.lock_entity.if0` | aecp | 0 | 3.366 | 168,314 | 0 | 20 | yes | no | 236.634 of 240 |
| H-AECP | `aecp.lock_entity.if1` | aecp | 1 | 2.939 | 146,927 | 0 | 20 | yes | no | 237.061 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if0` | aecp | 0 | 2.231 | 111,547 | 0 | 20 | yes | no | 237.769 of 240 |
| H-AECP | `aecp.mvu_get_milan_info.if1` | aecp | 1 | 1.798 | 89,904 | 0 | 20 | yes | no | 238.202 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if0` | aecp | 0 | 3.608 | 180,416 | 0 | 20 | yes | no | 236.392 of 240 |
| H-AECP | `aecp.read_descriptor.t0.i0.c0.if1` | aecp | 1 | 3.605 | 180,251 | 0 | 20 | yes | no | 236.395 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if0` | aecp | 0 | 2.719 | 135,970 | 0 | 20 | yes | no | 237.281 of 240 |
| H-AECP | `aecp.read_descriptor.t1.i0.c0.if1` | aecp | 1 | 2.715 | 135,760 | 0 | 20 | yes | no | 237.285 of 240 |
| H-AECP | `aecp.read_descriptor.t10.i9.c0.if0` | aecp | 0 | 2.717 | 135,828 | 0 | 20 | yes | no | 237.283 of 240 |
| H-AECP | `aecp.read_descriptor.t12.i0.c0.if0` | aecp | 0 | 2.687 | 134,369 | 0 | 20 | yes | no | 237.313 of 240 |
| H-AECP | `aecp.read_descriptor.t13.i0.c0.if0` | aecp | 0 | 3.939 | 196,931 | 0 | 20 | yes | no | 236.061 of 240 |
| H-AECP | `aecp.read_descriptor.t14.i7.c0.if0` | aecp | 0 | 3.006 | 150,288 | 0 | 20 | yes | no | 236.994 of 240 |
| H-AECP | `aecp.read_descriptor.t15.i7.c0.if0` | aecp | 0 | 3.019 | 150,927 | 0 | 20 | yes | no | 236.981 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if0` | aecp | 0 | 2.813 | 140,657 | 0 | 20 | yes | no | 237.187 of 240 |
| H-AECP | `aecp.read_descriptor.t2.i0.c0.if1` | aecp | 1 | 3.665 | 183,267 | 0 | 20 | yes | no | 236.335 of 240 |
| H-AECP | `aecp.read_descriptor.t20.i71.c0.if0` | aecp | 0 | 2.852 | 142,581 | 0 | 20 | yes | no | 237.148 of 240 |
| H-AECP | `aecp.read_descriptor.t26.i0.c0.if0` | aecp | 0 | 2.890 | 144,525 | 0 | 20 | yes | no | 237.109 of 240 |
| H-AECP | `aecp.read_descriptor.t36.i0.c0.if0` | aecp | 0 | 2.856 | 142,788 | 0 | 20 | yes | no | 237.144 of 240 |
| H-AECP | `aecp.read_descriptor.t5.i8.c0.if0` | aecp | 0 | 2.820 | 141,019 | 0 | 20 | yes | no | 237.180 of 240 |
| H-AECP | `aecp.read_descriptor.t6.i8.c0.if0` | aecp | 0 | 3.260 | 162,976 | 0 | 20 | yes | no | 236.740 of 240 |
| H-AECP | `aecp.read_descriptor.t9.i0.c0.if0` | aecp | 0 | 3.167 | 158,329 | 0 | 20 | yes | no | 236.833 of 240 |
| H-AECP | `aecp.register_unsolicited.if0` | aecp | 0 | 1.793 | 89,668 | 0 | 20 | yes | no | 238.207 of 240 |
| H-AECP | `aecp.register_unsolicited.if1` | aecp | 1 | 1.787 | 89,368 | 0 | 20 | yes | no | 238.213 of 240 |
| H-AECP | `aecp.set_name.if0` | aecp | 0 | 4.351 | 217,564 | 0 | 20 | yes | no | 235.649 of 240 |
| H-AECP | `aecp.set_name.if1` | aecp | 1 | 3.977 | 198,860 | 0 | 20 | yes | no | 236.023 of 240 |
| H-AECP | `aecp.unknown_command.if0` | aecp | 0 | 2.477 | 123,831 | 0 | 20 | yes | no | 237.523 of 240 |
| H-AECP | `aecp.unknown_command.if1` | aecp | 1 | 2.905 | 145,259 | 0 | 20 | yes | no | 237.095 of 240 |
| H-AECP | `aecp.unlock_entity.if0` | aecp | 0 | 2.938 | 146,910 | 0 | 20 | yes | no | 237.062 of 240 |
| H-AECP | `aecp.unlock_entity.if1` | aecp | 1 | 3.370 | 168,502 | 0 | 20 | yes | no | 236.630 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.first.if0` | backlog-adp-refill | 0 | 12.409 | 620,473 | 0 | 20 | yes | yes | 227.591 of 240 |
| H-AECP | `backlog-adp-refill.service.aecp.last.if1` | backlog-adp-refill | 1 | 315.061 | 15,753,075 | 0 | 20 | NO | yes | -75.061 of 240 |
| H-AECP | `backlog-adp.service.aecp.first.if0` | backlog-adp | 0 | 12.409 | 620,473 | 0 | 20 | yes | yes | 227.591 of 240 |
| H-AECP | `backlog-adp.service.aecp.last.if1` | backlog-adp | 1 | 314.609 | 15,730,461 | 0 | 20 | NO | yes | -74.609 of 240 |
| H-AECP | `backlog-owed.service.aecp.first.if0` | backlog-owed | 0 | 10.365 | 518,260 | 0 | 20 | yes | yes | 229.635 of 240 |
| H-AECP | `backlog-owed.service.aecp.last.if1` | backlog-owed | 1 | 143.372 | 7,168,615 | 0 | 20 | NO | yes | 96.628 of 240 |
| H-AECP | `backlog.service.aecp.first.if0` | backlog | 0 | 14.517 | 725,834 | 0 | 20 | yes | yes | 225.483 of 240 |
| H-AECP | `backlog.service.aecp.last.if1` | backlog | 1 | 125.509 | 6,275,433 | 0 | 20 | NO | yes | 114.491 of 240 |
| H-AECP | `hooks-late-aecp.read_descriptor.if0` | hooks-late-aecp | 0 | 3.147 | 157,362 | 0 | 20 | yes | no | 236.853 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.first.if0` | hooks-load-notify | 0 | 10.927 | 546,349 | 0 | 20 | yes | yes | 229.073 of 240 |
| H-AECP | `hooks-load-notify.service.aecp.last.if0` | hooks-load-notify | 0 | 141.776 | 7,088,814 | 0 | 20 | NO | yes | 98.224 of 240 |
| H-DISC | `acmp.entity_available.if0` | acmp-disc | 0 | 22.857 | 1,142,873 | 0 | 20 | NO | no | 177.143 of 200 |
| H-DISC | `acmp.entity_available.if1` | acmp-disc | 1 | 24.150 | 1,207,496 | 0 | 20 | NO | no | 175.850 of 200 |
| H-DISC | `acmp.entity_departing.if0` | acmp-disc | 0 | 21.928 | 1,096,382 | 0 | 20 | NO | no | 178.072 of 200 |
| H-DISC | `acmp.entity_departing.if1` | acmp-disc | 1 | 23.183 | 1,159,153 | 0 | 20 | NO | no | 176.817 of 200 |
| H-DISC | `acmp.tmr_no_adp.if0` | acmp-disc | 0 | 6.405 | 320,273 | 0 | 20 | yes | no | 193.595 of 200 |
| H-DISC | `backlog.adp_available.if0` | backlog-adp | 0 | 48.074 | 2,403,695 | 0 | 20 | NO | yes | 151.926 of 200 |
| H-DISC | `backlog.adp_available_refill.if0` | backlog-adp-refill | 0 | 53.855 | 2,692,745 | 0 | 20 | NO | yes | 146.145 of 200 |
| H-DISC | `hooks-disc-aging.available.if0` | hooks-disc-aging | 0 | 14.401 | 720,056 | 0 | 20 | yes | no | 185.599 of 200 |
| H-DISC | `hooks-disc-aging.available.if1` | hooks-disc-aging | 1 | 4.846 | 242,320 | 0 | 20 | yes | no | 195.154 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if0` | hooks-disc-aging | 0 | 1.301 | 65,047 | 0 | 20 | yes | no | 198.699 of 200 |
| H-DISC | `hooks-disc-aging.tmr_no_adp.if1` | hooks-disc-aging | 1 | 2.976 | 148,792 | 0 | 20 | yes | no | 197.024 of 200 |
| H-DISC | `hooks-late-disc.entity_departing.if0` | hooks-late-disc | 0 | 3.100 | 155,025 | 0 | 20 | yes | no | 196.899 of 200 |
| H-MAAP | `backlog-adp-refill.service.maap.first.if0` | backlog-adp-refill | 0 | 12.399 | 619,953 | 0 | 20 | yes | yes | 487.601 of 500 |
| H-MAAP | `backlog-adp-refill.service.maap.last.if0` | backlog-adp-refill | 0 | 58.217 | 2,910,871 | 0 | 20 | NO | yes | 441.783 of 500 |
| H-MAAP | `backlog-adp.service.maap.first.if0` | backlog-adp | 0 | 12.399 | 619,953 | 0 | 20 | yes | yes | 487.601 of 500 |
| H-MAAP | `backlog-adp.service.maap.last.if0` | backlog-adp | 0 | 59.343 | 2,967,136 | 0 | 20 | NO | yes | 440.657 of 500 |
| H-MAAP | `backlog-owed.service.maap.first.if0` | backlog-owed | 0 | 10.355 | 517,740 | 0 | 20 | yes | yes | 489.645 of 500 |
| H-MAAP | `backlog-owed.service.maap.last.if0` | backlog-owed | 0 | 43.335 | 2,166,734 | 0 | 20 | NO | yes | 456.665 of 500 |
| H-MAAP | `backlog.service.maap.first.if0` | backlog | 0 | 14.506 | 725,314 | 0 | 20 | yes | yes | 485.494 of 500 |
| H-MAAP | `backlog.service.maap.last.if0` | backlog | 0 | 48.595 | 2,429,736 | 0 | 20 | NO | yes | 451.405 of 500 |
| H-MAAP | `hooks-late-maap.defend.if0` | hooks-late-maap | 0 | 0.667 | 33,333 | 0 | 20 | yes | no | 499.333 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.first.if0` | hooks-load-notify | 0 | 10.961 | 548,067 | 0 | 20 | yes | yes | 489.039 of 500 |
| H-MAAP | `hooks-load-notify.service.maap.last.if0` | hooks-load-notify | 0 | 44.767 | 2,238,347 | 0 | 20 | NO | yes | 455.233 of 500 |
| H-MAAP | `maap.announce.if0` | maap | 0 | 2.056 | 102,815 | 0 | 20 | yes | no | 497.944 of 500 |
| H-MAAP | `maap.announce.if1` | maap | 1 | 1.254 | 62,686 | 0 | 20 | yes | no | 498.746 of 500 |
| H-MAAP | `maap.defend.if0` | maap | 0 | 0.664 | 33,185 | 0 | 20 | yes | no | 499.336 of 500 |
| H-MAAP | `maap.defend.if1` | maap | 1 | 0.667 | 33,333 | 0 | 20 | yes | no | 499.333 of 500 |
| H-MAAP | `maap.probe1.if0` | maap | 0 | 0.779 | 38,974 | 0 | 20 | yes | no | 499.221 of 500 |
| H-MAAP | `maap.probe1.if1` | maap | 1 | 1.214 | 60,676 | 0 | 20 | yes | no | 498.786 of 500 |
| H-MAAP | `maap.probe2.if0` | maap | 0 | 1.341 | 67,063 | 0 | 20 | yes | no | 498.659 of 500 |
| H-MAAP | `maap.probe2.if1` | maap | 1 | 2.439 | 121,962 | 0 | 20 | yes | no | 497.561 of 500 |
| H-MAAP | `maap.probe3.if0` | maap | 0 | 1.313 | 65,666 | 0 | 20 | yes | no | 498.687 of 500 |
| H-MAAP | `maap.probe3.if1` | maap | 1 | 1.693 | 84,636 | 0 | 20 | yes | no | 498.307 of 500 |
| H-MAAP | `maap.probe4.if0` | maap | 0 | 1.908 | 95,405 | 0 | 20 | yes | no | 498.092 of 500 |
| H-MAAP | `maap.probe4.if1` | maap | 1 | 1.106 | 55,276 | 0 | 20 | yes | no | 498.894 of 500 |
| H-NOTIFY | `aecp_fanout.lock_entity.if0` | aecp-fanout | 0 | 8.366 | 418,285 | 0 | 20 | yes | no | 231.634 of 240 |
| H-NOTIFY | `aecp_fanout.lock_entity.if1` | aecp-fanout | 1 | 8.327 | 416,334 | 0 | 20 | yes | no | 231.673 of 240 |
| H-NOTIFY | `aecp_fanout.set_clock_source.if0` | aecp-fanout | 0 | 9.394 | 469,705 | 0 | 20 | yes | no | 230.606 of 240 |
| H-NOTIFY | `aecp_fanout.set_clock_source.if1` | aecp-fanout | 1 | 8.861 | 443,047 | 0 | 20 | yes | no | 231.139 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_off.if0` | aecp-fanout | 0 | 8.401 | 420,032 | 0 | 20 | yes | no | 231.599 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_off.if1` | aecp-fanout | 1 | 7.532 | 376,603 | 0 | 20 | yes | no | 232.468 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_on.if0` | aecp-fanout | 0 | 7.928 | 396,382 | 0 | 20 | yes | no | 232.072 of 240 |
| H-NOTIFY | `aecp_fanout.set_control_identify_on.if1` | aecp-fanout | 1 | 9.461 | 473,033 | 0 | 20 | yes | no | 230.539 of 240 |
| H-NOTIFY | `aecp_fanout.set_name.if0` | aecp-fanout | 0 | 11.876 | 593,788 | 0 | 20 | yes | no | 228.124 of 240 |
| H-NOTIFY | `aecp_fanout.set_name.if1` | aecp-fanout | 1 | 11.025 | 551,251 | 0 | 20 | yes | no | 228.975 of 240 |
| H-NOTIFY | `aecp_fanout.set_sampling_rate.if0` | aecp-fanout | 0 | 7.253 | 362,626 | 0 | 20 | yes | no | 232.747 of 240 |
| H-NOTIFY | `aecp_fanout.unlock_entity.if0` | aecp-fanout | 0 | 7.911 | 395,551 | 0 | 20 | yes | no | 232.089 of 240 |
| H-NOTIFY | `aecp_fanout.unlock_entity.if1` | aecp-fanout | 1 | 7.977 | 398,836 | 0 | 20 | yes | no | 232.023 of 240 |
| H-NOTIFY | `hooks-late-notify.set_name.if0` | hooks-late-notify | 0 | 11.876 | 593,788 | 0 | 20 | yes | no | 228.124 of 240 |
| H-NOTIFY | `hooks-load-notify.set_name.if0` | hooks-load-notify | 0 | 138.874 | 6,943,706 | 0 | 20 | NO | yes | 101.126 of 240 |
| H-SRP | `backlog-adp-refill.service.srp.first.if0` | backlog-adp-refill | 0 | never | 29,692,008 | 0 | 18 | NO | yes | -413.840 of 180 |
| H-SRP | `backlog-adp-refill.service.srp.last.if1` | backlog-adp-refill | 1 | never | 29,691,001 | 0 | 18 | NO | yes | -413.820 of 180 |
| H-SRP | `backlog-adp.service.srp.first.if0` | backlog-adp | 0 | never | 27,405,500 | 0 | 18 | NO | yes | -368.110 of 180 |
| H-SRP | `backlog-adp.service.srp.last.if1` | backlog-adp | 1 | never | 27,404,493 | 0 | 18 | NO | yes | -368.090 of 180 |
| H-SRP | `backlog-owed.service.srp.first.if0` | backlog-owed | 0 | 33.094 | 1,654,708 | 0 | 18 | NO | yes | 146.906 of 180 |
| H-SRP | `backlog-owed.service.srp.last.if1` | backlog-owed | 1 | 160.504 | 8,025,176 | 0 | 18 | NO | yes | 19.496 of 180 |
| H-SRP | `backlog.service.srp.first.if0` | backlog | 0 | 71.996 | 3,599,817 | 0 | 18 | NO | yes | 108.004 of 180 |
| H-SRP | `backlog.service.srp.last.if1` | backlog | 1 | 155.552 | 7,777,592 | 0 | 18 | NO | yes | 24.448 of 180 |
| H-SRP | `hooks-late-srp.listener_ready.if0` | hooks-late-srp | 0 | 3.370 | 168,502 | 0 | 18 | yes | no | 176.630 of 180 |
| H-SRP | `hooks-load-notify.service.srp.first.if0` | hooks-load-notify | 0 | 34.251 | 1,712,527 | 0 | 18 | NO | yes | 145.749 of 180 |
| H-SRP | `hooks-load-notify.service.srp.last.if1` | hooks-load-notify | 1 | 176.014 | 8,800,683 | 0 | 18 | NO | yes | 3.986 of 180 |
| H-SRP | `srp.domain.if0` | srp | 0 | 8.365 | 418,264 | 200 | 218 | yes | no | -28.365 of 180 |
| H-SRP | `srp.domain.if1` | srp | 1 | 8.587 | 429,366 | 200 | 218 | yes | no | -28.587 of 180 |
| H-SRP | `srp.listener_ready.if0` | srp | 0 | 3.370 | 168,502 | 0 | 18 | yes | no | 176.630 of 180 |
| H-SRP | `srp.listener_ready.if1` | srp | 1 | 3.439 | 171,964 | 0 | 18 | yes | no | 176.561 of 180 |
| H-SRP | `srp.malformed.if0` | srp | 0 | 2.603 | 130,126 | 0 | 18 | yes | no | 177.397 of 180 |
| H-SRP | `srp.malformed.if1` | srp | 1 | 3.247 | 162,355 | 0 | 18 | yes | no | 176.753 of 180 |
| H-SRP | `srp.startup.if0` | srp | 0 | 6.445 | 322,242 | 0 | 18 | yes | no | 173.555 of 180 |
| H-SRP | `srp.startup.if1` | srp | 1 | 6.531 | 326,557 | 0 | 18 | yes | no | 173.469 of 180 |

Refusals:

- none

Probes of the CPU budget harness this harness measured again (hooks.SUPERSEDED):

- acmp.tmr_no_adp.if1 (acmp-disc): no start: no deadline:3 after the mark; measured by hooks-disc-aging

Findings:

- LATE H-NOTIFY: hooks-load-notify.set_name.if0: 138.874 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ADP: hooks-load-notify.service.adp.last.if1: 44.771 ms against its bound 20 ms (hooks-load-notify)
- LATE H-ACMP: hooks-load-notify.service.acmp.last.if0: 64.743 ms against its bound 20 ms (hooks-load-notify)
- LATE H-AECP: hooks-load-notify.service.aecp.last.if0: 141.776 ms against its bound 20 ms (hooks-load-notify)
- LATE H-MAAP: hooks-load-notify.service.maap.last.if0: 44.767 ms against its bound 20 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.first.if0: 34.251 ms against its bound 18 ms (hooks-load-notify)
- LATE H-SRP: hooks-load-notify.service.srp.last.if1: 176.014 ms against its bound 18 ms (hooks-load-notify)
- LATE H-ACMP: backlog.acmp_command.if0: 59.382 ms against its bound 20 ms (backlog)
- LATE H-ADP: backlog.service.adp.last.if1: 48.610 ms against its bound 20 ms (backlog)
- LATE H-ACMP: backlog.service.acmp.last.if0: 65.203 ms against its bound 20 ms (backlog)
- LATE H-AECP: backlog.service.aecp.last.if1: 125.509 ms against its bound 20 ms (backlog)
- LATE H-MAAP: backlog.service.maap.last.if0: 48.595 ms against its bound 20 ms (backlog)
- LATE H-SRP: backlog.service.srp.first.if0: 71.996 ms against its bound 18 ms (backlog)
- LATE H-SRP: backlog.service.srp.last.if1: 155.552 ms against its bound 18 ms (backlog)
- LATE H-DISC: backlog.adp_available.if0: 48.074 ms against its bound 20 ms (backlog-adp)
- LATE H-ADP: backlog-adp.service.adp.last.if0: 59.306 ms against its bound 20 ms (backlog-adp)
- LATE H-ACMP: backlog-adp.service.acmp.last.if0: 103.970 ms against its bound 20 ms (backlog-adp)
- LATE H-AECP: backlog-adp.service.aecp.last.if1: 314.609 ms against its bound 20 ms (backlog-adp)
- LATE H-MAAP: backlog-adp.service.maap.last.if0: 59.343 ms against its bound 20 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.first.if0: never served against its bound 18 ms (backlog-adp)
- LATE H-SRP: backlog-adp.service.srp.last.if1: never served against its bound 18 ms (backlog-adp)
- LATE H-DISC: backlog.adp_available_refill.if0: 53.855 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-ADP: backlog-adp-refill.service.adp.last.if0: 64.466 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-ACMP: backlog-adp-refill.service.acmp.last.if0: 104.422 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-AECP: backlog-adp-refill.service.aecp.last.if1: 315.061 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-MAAP: backlog-adp-refill.service.maap.last.if0: 58.217 ms against its bound 20 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.first.if0: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-SRP: backlog-adp-refill.service.srp.last.if1: never served against its bound 18 ms (backlog-adp-refill)
- LATE H-ACMP: backlog.owed.if0: 119.606 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind0.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind1.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind2.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog.owed_behind3.if0: never served against its bound 20 ms (backlog-owed)
- LATE H-ADP: backlog-owed.service.adp.last.if1: 43.350 ms against its bound 20 ms (backlog-owed)
- LATE H-ACMP: backlog-owed.service.acmp.last.if0: 60.869 ms against its bound 20 ms (backlog-owed)
- LATE H-AECP: backlog-owed.service.aecp.last.if1: 143.372 ms against its bound 20 ms (backlog-owed)
- LATE H-MAAP: backlog-owed.service.maap.last.if0: 43.335 ms against its bound 20 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.first.if0: 33.094 ms against its bound 18 ms (backlog-owed)
- LATE H-SRP: backlog-owed.service.srp.last.if1: 160.504 ms against its bound 18 ms (backlog-owed)
- LATE H-DISC: acmp.entity_departing.if0: 21.928 ms against its bound 20 ms (acmp-disc)
- LATE H-DISC: acmp.entity_departing.if1: 23.183 ms against its bound 20 ms (acmp-disc)
- LATE H-DISC: acmp.entity_available.if0: 22.857 ms against its bound 20 ms (acmp-disc)
- LATE H-DISC: acmp.entity_available.if1: 24.150 ms against its bound 20 ms (acmp-disc)
