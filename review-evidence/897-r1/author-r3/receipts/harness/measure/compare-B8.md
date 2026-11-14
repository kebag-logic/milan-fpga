## B8: head build 464695b772b9, base build faee5a256a31, point 8x8
counts head {'paths': 44, 'path_misses': 0, 'instances': 44, 'instance_misses': 0} base {'paths': 44, 'path_misses': 0, 'instances': 44, 'instance_misses': 0}
refusals: head 0 base 0
misses: head 0 base 0
share_misses: head 1 base 1
notice_misses: head 0 base 0
| path | if | head cycles | base cycles | delta | head ms (bound) | within bound |
|---|---:|---:|---:|---:|---|---|
| aecp.entity_available | 0 | 18780 | 10754 | 8026 | 0.1878 (0.63249) | True |
| aecp.entity_available | 1 | 30414 | 21386 | 9028 | 0.30414 (0.76037) | True |
| aecp.get_avb_info | 0 | 11438 | 11658 | -220 | 0.11438 (0.34421) | True |
| aecp.get_avb_info | 1 | 32463 | 23285 | 9178 | 0.32463 (0.78492) | True |
| aecp.get_configuration | 0 | 28530 | 10278 | 18252 | 0.2853 (0.74206) | True |
| aecp.get_configuration | 1 | 20838 | 12761 | 8077 | 0.20838 (0.65225) | True |
| aecp.get_counters | 0 | 32511 | 14582 | 17929 | 0.32511 (0.78751) | True |
| aecp.get_counters | 1 | 25046 | 25670 | -624 | 0.25046 (0.70217) | True |
| aecp.get_name | 0 | 30544 | 21662 | 8882 | 0.30544 (0.76625) | True |
| aecp.get_name | 1 | 32408 | 14621 | 17787 | 0.32408 (0.78562) | True |
| aecp.lock_entity | 0 | 46050 | 28222 | 17828 | 0.4605 (0.84073) | True |
| aecp.lock_entity | 1 | 37905 | 40064 | -2159 | 0.37905 (0.78862) | True |
| aecp.mvu_get_milan_info | 0 | 18162 | 9928 | 8234 | 0.18162 (0.62448) | True |
| aecp.mvu_get_milan_info | 1 | 20754 | 20687 | 67 | 0.20754 (0.66581) | True |
| aecp.read_descriptor.t0.i0.c0 | 0 | 34773 | 25738 | 9035 | 0.34773 (0.81133) | True |
| aecp.read_descriptor.t0.i0.c0 | 1 | 33335 | 17519 | 15816 | 0.33335 (0.66354) | True |
| aecp.read_descriptor.t1.i0.c0 | 0 | 30977 | 21195 | 9782 | 0.30977 (0.77076) | True |
| aecp.read_descriptor.t1.i0.c0 | 1 | 23465 | 24525 | -1060 | 0.23465 (0.69844) | True |
| aecp.read_descriptor.t10.i9.c0 | 0 | 30048 | 21393 | 8655 | 0.30048 (0.75848) | True |
| aecp.read_descriptor.t12.i0.c0 | 0 | 20530 | 12122 | 8408 | 0.2053 (0.65296) | True |
| aecp.read_descriptor.t13.i0.c0 | 0 | 34833 | 26169 | 8664 | 0.34833 (0.81494) | True |
| aecp.read_descriptor.t14.i7.c0 | 0 | 30087 | 11884 | 18203 | 0.30087 (0.76081) | True |
| aecp.read_descriptor.t15.i7.c0 | 0 | 20082 | 21382 | -1300 | 0.20082 (0.65006) | True |
| aecp.read_descriptor.t2.i0.c0 | 0 | 21046 | 12949 | 8097 | 0.21046 (0.65869) | True |
| aecp.read_descriptor.t2.i0.c0 | 1 | 32675 | 14606 | 18069 | 0.32675 (0.78631) | True |
| aecp.read_descriptor.t20.i71.c0 | 0 | 30400 | 21633 | 8767 | 0.304 (0.76374) | True |
| aecp.read_descriptor.t26.i0.c0 | 0 | 21551 | 13143 | 8408 | 0.21551 (0.66426) | True |
| aecp.read_descriptor.t36.i0.c0 | 0 | 21916 | 22448 | -532 | 0.21916 (0.68061) | True |
| aecp.read_descriptor.t5.i8.c0 | 0 | 30463 | 21817 | 8646 | 0.30463 (0.76554) | True |
| aecp.read_descriptor.t6.i8.c0 | 0 | 21726 | 13280 | 8446 | 0.21726 (0.66495) | True |
| aecp.read_descriptor.t9.i0.c0 | 0 | 20840 | 21301 | -461 | 0.2084 (0.66986) | True |
| aecp.register_unsolicited | 0 | 18540 | 32928 | -14388 | 0.1854 (0.64529) | True |
| aecp.register_unsolicited | 1 | 29189 | 20896 | 8293 | 0.29189 (0.75333) | True |
| aecp.set_name | 0 | 54165 | 45264 | 8901 | 0.54165 (1.0021) | True |
| aecp.set_name | 1 | 52550 | 34914 | 17636 | 0.5255 (0.94894) | True |
| aecp.unknown_command | 0 | 28626 | 18292 | 10334 | 0.28626 (0.74304) | True |
| aecp.unknown_command | 1 | 20836 | 12469 | 8367 | 0.20836 (0.65216) | True |
| aecp.unlock_entity | 0 | 35794 | 38104 | -2310 | 0.35794 (0.73627) | True |
| aecp.unlock_entity | 1 | 26139 | 39933 | -13794 | 0.26139 (0.41294) | True |
| aecp_long.add_audio_mappings | 0 | 228440 | 241095 | -12655 | 2.2844 (2.74847) | True |
| aecp_long.refused.collision_indices | 0 | 56500 | 69563 | -13063 | 0.565 (1.13739) | True |
| aecp_long.refused.collision_values | 0 | 227090 | 188297 | 38793 | 2.2709 (2.84032) | True |
| aecp_long.refused.conflict_last | 0 | 213196 | 227333 | -14137 | 2.13196 (2.69969) | True |
| aecp_long.remove_audio_mappings | 0 | 238077 | 250913 | -12836 | 2.38077 (2.86774) | True |
group aecp: worst work pass head 89599 base 89600 cycles; work passes head 141 base 141
group aecp-largest-notice: worst work pass head 255281 base 254919 cycles; work passes head 138 base 139
largest path delta: 38793 cycles at ('aecp_long.refused.collision_values', 0)
