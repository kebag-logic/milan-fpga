## arm A 1x1: head build a933eee2bace, base build 8efeffe218af, point 1x1
counts head {'paths': 62, 'path_misses': 4, 'instances': 66, 'instance_misses': 7} base {'paths': 62, 'path_misses': 4, 'instances': 66, 'instance_misses': 7}
refusals: head 0 base 0
misses: head 7 base 7
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| acmp.bind_rx | 0 | 18124 | 18005 | 119 | 0.18124 (0.38775) | True |
| acmp.disconnect_tx | 0 | 9174 | 8865 | 309 | 0.09174 (0.22123) | True |
| acmp.get_rx_state | 0 | 10271 | 9708 | 563 | 0.10271 (0.23787) | True |
| acmp.get_tx_connection | 0 | 9203 | 8889 | 314 | 0.09203 (0.22104) | True |
| acmp.get_tx_state | 0 | 9372 | 8984 | 388 | 0.09372 (0.22833) | True |
| acmp.probe_tx | 0 | 10196 | 10639 | -443 | 0.10196 (0.24888) | True |
| acmp.probe_tx_response | 0 | 8991 | 9501 | -510 | 0.08991 (0.30923) | True |
| acmp.unbind_rx | 0 | 12828 | 13548 | -720 | 0.12828 (0.38728) | True |
| aecp.entity_available | 0 | 15114 | 14498 | 616 | 0.15114 (0.43382) | True |
| aecp.get_avb_info | 0 | 15123 | 17852 | -2729 | 0.15123 (0.44509) | True |
| aecp.get_configuration | 0 | 20354 | 19630 | 724 | 0.20354 (0.49055) | True |
| aecp.get_counters | 0 | 19960 | 22686 | -2726 | 0.1996 (0.49445) | True |
| aecp.get_name | 0 | 17710 | 17098 | 612 | 0.1771 (0.47323) | True |
| aecp.lock_entity | 0 | 26842 | 21835 | 5007 | 0.26842 (0.60676) | True |
| aecp.mvu_get_milan_info | 0 | 11347 | 14530 | -3183 | 0.11347 (0.39863) | True |
| aecp.read_descriptor.t0.i0.c0 | 0 | 26903 | 27771 | -868 | 0.26903 (0.56514) | True |
| aecp.read_descriptor.t1.i0.c0 | 0 | 17328 | 16818 | 510 | 0.17328 (0.46173) | True |
| aecp.read_descriptor.t10.i2.c0 | 0 | 17305 | 16793 | 512 | 0.17305 (0.46037) | True |
| aecp.read_descriptor.t12.i0.c0 | 0 | 21838 | 21155 | 683 | 0.21838 (0.50883) | True |
| aecp.read_descriptor.t13.i0.c0 | 0 | 19560 | 19148 | 412 | 0.1956 (0.48247) | True |
| aecp.read_descriptor.t14.i0.c0 | 0 | 21700 | 21053 | 647 | 0.217 (0.50741) | True |
| aecp.read_descriptor.t15.i0.c0 | 0 | 21882 | 21041 | 841 | 0.21882 (0.50923) | True |
| aecp.read_descriptor.t2.i0.c0 | 0 | 22269 | 21607 | 662 | 0.22269 (0.51472) | True |
| aecp.read_descriptor.t20.i24.c0 | 0 | 17063 | 16546 | 517 | 0.17063 (0.4575) | True |
| aecp.read_descriptor.t26.i0.c0 | 0 | 22899 | 22230 | 669 | 0.22899 (0.52239) | True |
| aecp.read_descriptor.t36.i0.c0 | 0 | 17182 | 16600 | 582 | 0.17182 (0.4611) | True |
| aecp.read_descriptor.t5.i1.c0 | 0 | 23113 | 22298 | 815 | 0.23113 (0.52361) | True |
| aecp.read_descriptor.t6.i1.c0 | 0 | 17847 | 17335 | 512 | 0.17847 (0.46612) | True |
| aecp.read_descriptor.t9.i0.c0 | 0 | 22545 | 21805 | 740 | 0.22545 (0.51586) | True |
| aecp.register_unsolicited | 0 | 14880 | 15956 | -1076 | 0.1488 (0.44293) | True |
| aecp.set_name | 0 | 22223 | 25040 | -2817 | 0.22223 (0.61032) | True |
| aecp.unknown_command | 0 | 17467 | 18966 | -1499 | 0.17467 (0.46549) | True |
| aecp.unlock_entity | 0 | 21684 | 20980 | 704 | 0.21684 (0.57288) | True |
| aecp_fanout.add_audio_mappings | 0 | 203722 | 158645 | 45077 | 2.03722 (2.32365) | True |
| aecp_fanout.lock_entity | 0 | 44312 | 44271 | 41 | 0.44312 (0.72925) | True |
| aecp_fanout.remove_audio_mappings | 0 | 58536 | 65298 | -6762 | 0.58536 (0.87257) | True |
| aecp_fanout.set_clock_source | 0 | 47180 | 46441 | 739 | 0.4718 (0.7621) | True |
| aecp_fanout.set_control | 0 | 53050 | 55846 | -2796 | 0.5305 (0.79267) | True |
| aecp_fanout.set_name | 0 | 48412 | 60772 | -12360 | 0.48412 (0.79004) | True |
| aecp_fanout.set_sampling_rate | 0 | 236693 | 236775 | -82 | 2.36693 (2.6631) | True |
| aecp_fanout.unlock_entity | 0 | 49731 | 52751 | -3020 | 0.49731 (0.75857) | True |
| aecp_long.add_audio_mappings | 0 | 143499 | 209133 | -65634 | 1.43499 (1.72314) | True |
| aecp_long.refused.collision_indices | 0 | 141223 | 129228 | 11995 | 1.41223 (1.75163) | True |
| aecp_long.refused.collision_values | 0 | 281568 | 290539 | -8971 | 2.81568 (3.14849) | True |
| aecp_long.refused.conflict_last | 0 | 244081 | 238059 | 6022 | 2.44081 (2.78377) | True |
| aecp_long.remove_audio_mappings | 0 | 135523 | 147571 | -12048 | 1.35523 (1.49429) | True |
| backlog.owed | 0 | 6286397 | 6292765 | -6368 | 62.86397 (63.13427) | False |
| backlog.owed_behind | 0 | 6356018 | 6363762 | -7744 | 63.56018 (63.82962) | False |
| service.acmp.first | 0 | 150266 | 120921 | 29345 | 1.50266 (None) | None |
| service.acmp.last | 0 | 6202416 | 6207102 | -4686 | 62.02416 (None) | False |
| service.adp.first | 0 | 154588 | 125243 | 29345 | 1.54588 (None) | None |
| service.adp.last | 0 | 240725 | 124627 | 116098 | 2.40725 (None) | None |
| service.aecp.first | 0 | 153906 | 221713 | -67807 | 1.53906 (None) | None |
| service.aecp.last | 0 | 6177901 | 6153849 | 24052 | 61.77901 (None) | False |
| service.maap.first | 0 | 152850 | 123505 | 29345 | 1.5285 (None) | None |
| service.maap.last | 0 | 239207 | 123109 | 116098 | 2.39207 (None) | None |
| service.srp.first | 0 | 330026 | 301006 | 29020 | 3.30026 (None) | None |
| service.srp.last | 0 | 729638 | 722319 | 7319 | 7.29638 (None) | None |
| srp.domain | 0 | 97464 | 97402 | 62 | 0.97464 (1.08721) | True |
| srp.listener_ready | 0 | 43904 | 44010 | -106 | 0.43904 (0.4397) | True |
| srp.malformed | 0 | 20162 | 20586 | -424 | 0.20162 (0.20228) | True |
| srp.startup | 0 | 88578 | 88777 | -199 | 0.88578 (0.96305) | True |
group srp: worst work pass head 69269 base 68937 cycles; work passes head 290 base 289
group backlog-owed: worst work pass head 145391 base 136975 cycles; work passes head 310 base 310
group aecp-fanout: worst work pass head 65168 base 65333 cycles; work passes head 112 base 111
group acmp-cmd: worst work pass head 41876 base 41869 cycles; work passes head 87 base 86
group aecp: worst work pass head 43558 base 43739 cycles; work passes head 112 base 111
group aecp-largest-notice: worst work pass head 149429 base 149490 cycles; work passes head 106 base 106
group datapath-events: worst work pass head 41876 base 41869 cycles; work passes head 119 base 117
largest path delta: 116098 cycles at ('service.adp.last', 0)
