## A8 at d3202fa2 against cec88385: head build df67af1681e2, base build 6d9795de78f8, point 8x8
counts head {'paths': 66, 'path_misses': 0, 'instances': 68, 'instance_misses': 0} base {'paths': 66, 'path_misses': 0, 'instances': 68, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| acmp.bind_rx | 0 | 20936 | 20247 | 689 | 0.20936 (0.50492) | True |
| acmp.bind_rx | 1 | 18923 | 17857 | 1066 | 0.18923 (0.46701) | True |
| acmp.disconnect_tx | 0 | 9697 | 9401 | 296 | 0.09697 (0.31692) | True |
| acmp.disconnect_tx | 1 | 9655 | 10054 | -399 | 0.09655 (0.31885) | True |
| acmp.get_rx_state | 0 | 11232 | 10732 | 500 | 0.11232 (0.3388) | True |
| acmp.get_rx_state | 1 | 11806 | 11190 | 616 | 0.11806 (0.33916) | True |
| acmp.get_tx_connection | 0 | 9923 | 9450 | 473 | 0.09923 (0.3176) | True |
| acmp.get_tx_connection | 1 | 9689 | 9174 | 515 | 0.09689 (0.31953) | True |
| acmp.get_tx_state | 0 | 11584 | 11123 | 461 | 0.11584 (0.34527) | True |
| acmp.get_tx_state | 1 | 10956 | 11466 | -510 | 0.10956 (0.34119) | True |
| acmp.probe_tx | 0 | 11205 | 10698 | 507 | 0.11205 (0.33621) | True |
| acmp.probe_tx | 1 | 11169 | 11058 | 111 | 0.11169 (0.33836) | True |
| acmp.probe_tx_response | 0 | 10663 | 10199 | 464 | 0.10663 (0.39416) | True |
| acmp.probe_tx_response | 1 | 10903 | 10167 | 736 | 0.10903 (0.39332) | True |
| acmp.unbind_rx | 0 | 15063 | 13776 | 1287 | 0.15063 (0.47076) | True |
| acmp.unbind_rx | 1 | 16178 | 15640 | 538 | 0.16178 (0.50281) | True |
| aecp.entity_available | 0 | 23737 | 22707 | 1030 | 0.23737 (0.70515) | True |
| aecp.entity_available | 1 | 26000 | 10340 | 15660 | 0.26 (0.72518) | True |
| aecp.get_avb_info | 0 | 28999 | 16041 | 12958 | 0.28999 (0.75379) | True |
| aecp.get_avb_info | 1 | 30565 | 13641 | 16924 | 0.30565 (0.77962) | True |
| aecp.get_configuration | 0 | 31321 | 31420 | -99 | 0.31321 (0.78997) | True |
| aecp.get_configuration | 1 | 8980 | 24974 | -15994 | 0.0898 (0.32005) | True |
| aecp.get_counters | 0 | 34850 | 26865 | 7985 | 0.3485 (0.83097) | True |
| aecp.get_counters | 1 | 29733 | 28658 | 1075 | 0.29733 (0.76103) | True |
| aecp.get_name | 0 | 33401 | 34502 | -1101 | 0.33401 (0.81635) | True |
| aecp.get_name | 1 | 11560 | 10985 | 575 | 0.1156 (0.35138) | True |
| aecp.lock_entity | 0 | 47899 | 23858 | 24041 | 0.47899 (0.88549) | True |
| aecp.lock_entity | 1 | 25397 | 40590 | -15193 | 0.25397 (0.42274) | True |
| aecp.mvu_get_milan_info | 0 | 31057 | 21808 | 9249 | 0.31057 (0.77502) | True |
| aecp.mvu_get_milan_info | 1 | 24783 | 9478 | 15305 | 0.24783 (0.71004) | True |
| aecp.read_descriptor.t0.i0.c0 | 0 | 38173 | 15361 | 22812 | 0.38173 (0.86374) | True |
| aecp.read_descriptor.t0.i0.c0 | 1 | 14996 | 30261 | -15265 | 0.14996 (0.38087) | True |
| aecp.read_descriptor.t1.i0.c0 | 0 | 34494 | 34296 | 198 | 0.34494 (0.82729) | True |
| aecp.read_descriptor.t1.i0.c0 | 1 | 29065 | 28564 | 501 | 0.29065 (0.75505) | True |
| aecp.read_descriptor.t10.i9.c0 | 0 | 33279 | 10634 | 22645 | 0.33279 (0.81432) | True |
| aecp.read_descriptor.t12.i0.c0 | 0 | 25612 | 25272 | 340 | 0.25612 (0.72923) | True |
| aecp.read_descriptor.t13.i0.c0 | 0 | 37856 | 38294 | -438 | 0.37856 (0.86443) | True |
| aecp.read_descriptor.t14.i7.c0 | 0 | 33143 | 24590 | 8553 | 0.33143 (0.81491) | True |
| aecp.read_descriptor.t15.i7.c0 | 0 | 25085 | 25341 | -256 | 0.25085 (0.72366) | True |
| aecp.read_descriptor.t2.i0.c0 | 0 | 26602 | 25848 | 754 | 0.26602 (0.7354) | True |
| aecp.read_descriptor.t2.i0.c0 | 1 | 11371 | 13008 | -1637 | 0.11371 (0.35543) | True |
| aecp.read_descriptor.t20.i71.c0 | 0 | 33455 | 10779 | 22676 | 0.33455 (0.81652) | True |
| aecp.read_descriptor.t26.i0.c0 | 0 | 34904 | 26146 | 8758 | 0.34904 (0.86644) | True |
| aecp.read_descriptor.t36.i0.c0 | 0 | 26478 | 34540 | -8062 | 0.26478 (0.75215) | True |
| aecp.read_descriptor.t5.i8.c0 | 0 | 33899 | 33775 | 124 | 0.33899 (0.82018) | True |
| aecp.read_descriptor.t6.i8.c0 | 0 | 27152 | 25772 | 1380 | 0.27152 (0.74192) | True |
| aecp.read_descriptor.t9.i0.c0 | 0 | 25808 | 33855 | -8047 | 0.25808 (0.74085) | True |
| aecp.register_unsolicited | 0 | 14579 | 13299 | 1280 | 0.14579 (0.61772) | True |
| aecp.register_unsolicited | 1 | 25908 | 32826 | -6918 | 0.25908 (0.73087) | True |
| aecp.set_name | 0 | 48548 | 56082 | -7534 | 0.48548 (0.95205) | True |
| aecp.set_name | 1 | 30090 | 30548 | -458 | 0.3009 (0.50162) | True |
| aecp.unknown_command | 0 | 8608 | 8739 | -131 | 0.08608 (0.32313) | True |
| aecp.unknown_command | 1 | 9350 | 25064 | -15714 | 0.0935 (0.32003) | True |
| aecp.unlock_entity | 0 | 40442 | 39083 | 1359 | 0.40442 (0.80766) | True |
| aecp.unlock_entity | 1 | 42858 | 26836 | 16022 | 0.42858 (0.84009) | True |
| aecp_fanout.lock_entity | 0 | 73737 | 52557 | 21180 | 0.73737 (1.18076) | True |
| aecp_fanout.lock_entity | 1 | 73487 | 52741 | 20746 | 0.73487 (1.17711) | True |
| aecp_fanout.set_clock_source | 0 | 69019 | 74914 | -5895 | 0.69019 (1.1542) | True |
| aecp_fanout.set_clock_source | 1 | 76762 | 56207 | 20555 | 0.76762 (1.22788) | True |
| aecp_fanout.set_control | 0 | 79875 | 71443 | 8432 | 0.79875 (1.23995) | True |
| aecp_fanout.set_control | 1 | 72750 | 85194 | -12444 | 0.7275 (1.16981) | True |
| aecp_fanout.set_name | 0 | 76811 | 82923 | -6112 | 0.76811 (1.26942) | True |
| aecp_fanout.set_name | 1 | 71943 | 78002 | -6059 | 0.71943 (1.19987) | True |
| aecp_fanout.set_sampling_rate | 0 | 68069 | 73653 | -5584 | 0.68069 (1.15723) | True |
| aecp_fanout.unlock_entity | 0 | 72323 | 85707 | -13384 | 0.72323 (0.99907) | True |
| aecp_fanout.unlock_entity | 1 | 73751 | 58138 | 15613 | 0.73751 (1.18024) | True |
group aecp-fanout: worst work pass head 112313 base 112232 cycles; work passes head 147 base 144
group acmp-cmd: worst work pass head 112313 base 112232 cycles; work passes head 108 base 107
group aecp: worst work pass head 112313 base 112232 cycles; work passes head 136 base 136
largest path delta: 24041 cycles at ('aecp.lock_entity', 0)
