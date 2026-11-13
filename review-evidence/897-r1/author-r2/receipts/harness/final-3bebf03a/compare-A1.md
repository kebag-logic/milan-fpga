## A1 at 3bebf03a against cec88385: head build ddcfb6dbc9b6, base build 5ac9ea96a011, point 1x1
counts head {'paths': 41, 'path_misses': 0, 'instances': 42, 'instance_misses': 0} base {'paths': 41, 'path_misses': 0, 'instances': 42, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 0 base 0
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| acmp.bind_rx | 0 | 18410 | 18524 | -114 | 0.1841 (0.39541) | True |
| acmp.disconnect_tx | 0 | 9895 | 9638 | 257 | 0.09895 (0.22022) | True |
| acmp.get_rx_state | 0 | 10218 | 10605 | -387 | 0.10218 (0.23542) | True |
| acmp.get_tx_connection | 0 | 8842 | 9909 | -1067 | 0.08842 (0.2214) | True |
| acmp.get_tx_state | 0 | 10066 | 9909 | 157 | 0.10066 (0.23094) | True |
| acmp.probe_tx | 0 | 10681 | 10462 | 219 | 0.10681 (0.24504) | True |
| acmp.probe_tx_response | 0 | 13499 | 9257 | 4242 | 0.13499 (0.34603) | True |
| acmp.unbind_rx | 0 | 13217 | 13279 | -62 | 0.13217 (0.37575) | True |
| aecp.entity_available | 0 | 18495 | 8326 | 10169 | 0.18495 (0.44561) | True |
| aecp.get_avb_info | 0 | 22196 | 17569 | 4627 | 0.22196 (0.50318) | True |
| aecp.get_configuration | 0 | 22557 | 14307 | 8250 | 0.22557 (0.48571) | True |
| aecp.get_counters | 0 | 13391 | 11167 | 2224 | 0.13391 (0.33637) | True |
| aecp.get_name | 0 | 23753 | 16443 | 7310 | 0.23753 (0.50959) | True |
| aecp.lock_entity | 0 | 27575 | 28255 | -680 | 0.27575 (0.56794) | True |
| aecp.mvu_get_milan_info | 0 | 17459 | 7858 | 9601 | 0.17459 (0.44451) | True |
| aecp.read_descriptor.t0.i0.c0 | 0 | 14887 | 20817 | -5930 | 0.14887 (0.30459) | True |
| aecp.read_descriptor.t1.i0.c0 | 0 | 21232 | 11014 | 10218 | 0.21232 (0.47401) | True |
| aecp.read_descriptor.t10.i2.c0 | 0 | 20878 | 10957 | 9921 | 0.20878 (0.46728) | True |
| aecp.read_descriptor.t12.i0.c0 | 0 | 10630 | 14970 | -4340 | 0.1063 (0.24606) | True |
| aecp.read_descriptor.t13.i0.c0 | 0 | 23013 | 13005 | 10008 | 0.23013 (0.49266) | True |
| aecp.read_descriptor.t14.i0.c0 | 0 | 22518 | 15282 | 7236 | 0.22518 (0.49131) | True |
| aecp.read_descriptor.t15.i0.c0 | 0 | 11275 | 9416 | 1859 | 0.11275 (0.31532) | True |
| aecp.read_descriptor.t2.i0.c0 | 0 | 23457 | 16014 | 7443 | 0.23457 (0.50153) | True |
| aecp.read_descriptor.t20.i24.c0 | 0 | 19933 | 15533 | 4400 | 0.19933 (0.47477) | True |
| aecp.read_descriptor.t26.i0.c0 | 0 | 11425 | 15451 | -4026 | 0.11425 (0.25546) | True |
| aecp.read_descriptor.t36.i0.c0 | 0 | 19724 | 10527 | 9197 | 0.19724 (0.46815) | True |
| aecp.read_descriptor.t5.i1.c0 | 0 | 21145 | 10595 | 10550 | 0.21145 (0.47492) | True |
| aecp.read_descriptor.t6.i1.c0 | 0 | 17836 | 11871 | 5965 | 0.17836 (0.45197) | True |
| aecp.read_descriptor.t9.i0.c0 | 0 | 11055 | 15827 | -4772 | 0.11055 (0.25171) | True |
| aecp.register_unsolicited | 0 | 14288 | 19950 | -5662 | 0.14288 (0.42195) | True |
| aecp.set_name | 0 | 30875 | 22897 | 7978 | 0.30875 (0.60351) | True |
| aecp.unknown_command | 0 | 9748 | 13925 | -4177 | 0.09748 (0.23406) | True |
| aecp.unlock_entity | 0 | 18162 | 23024 | -4862 | 0.18162 (0.30254) | True |
| aecp_fanout.add_audio_mappings | 0 | 41839 | 47881 | -6042 | 0.41839 (0.71953) | True |
| aecp_fanout.lock_entity | 0 | 43278 | 36725 | 6553 | 0.43278 (0.68442) | True |
| aecp_fanout.remove_audio_mappings | 0 | 47047 | 40288 | 6759 | 0.47047 (0.75208) | True |
| aecp_fanout.set_clock_source | 0 | 44836 | 39014 | 5822 | 0.44836 (0.72373) | True |
| aecp_fanout.set_control | 0 | 44166 | 45798 | -1632 | 0.44166 (0.69264) | True |
| aecp_fanout.set_name | 0 | 46971 | 54656 | -7685 | 0.46971 (0.76745) | True |
| aecp_fanout.set_sampling_rate | 0 | 45163 | 44365 | 798 | 0.45163 (0.71801) | True |
| aecp_fanout.unlock_entity | 0 | 39859 | 46568 | -6709 | 0.39859 (0.66258) | True |
group aecp-fanout: worst work pass head 66517 base 66016 cycles; work passes head 109 base 109
group acmp-cmd: worst work pass head 66517 base 66016 cycles; work passes head 81 base 82
group aecp: worst work pass head 66517 base 66016 cycles; work passes head 107 base 109
largest path delta: 10550 cycles at ('aecp.read_descriptor.t5.i1.c0', 0)
