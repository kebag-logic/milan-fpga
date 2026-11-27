### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 54 paths and 0 of 64 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.174 (0.532) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.199 (0.563) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.166 (0.525) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.146 (0.497) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.207 (0.574) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.152 (0.501) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.209 (0.688) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.138 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.307 (0.666) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.169 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.161 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.197 (0.554) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.239 (0.598) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.162 (0.515) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.193 (0.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.165 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i79.c0.if0` (aecp) | 0.163 (0.515) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.200 (0.557) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.198 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.197 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.171 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.196 (0.553) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.133 (0.493) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.276 (0.767) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.178 (0.534) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.192 (0.616) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.946 (3.296) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.262 (3.614) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.877 (1.136) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.585 (0.906) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.513 (0.893) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.274 (3.629) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.439 (0.853) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.820 (0.970) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.587 (0.908) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.473 (0.853) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.070 (3.414) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.710 (3.107) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.438 (0.758) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.368 (2.735) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.372 (2.835) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.382 (3.827) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.930 (3.363) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.319 (1.697) | fits | 0 aecp | 1 | 0 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | 0 | `aecp_outputs.declared.if0` (aecp-outputs) | 1.448 (1.685) | fits | 0 acmp | 1 | 0 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | 0 | `aecp_outputs.get_stream_info.get_stream_info_o4.if0` (aecp-outputs) | 0.307 (0.742) | fits | 0 aecp | 9 | 0 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | 0 | `aecp_outputs.held_get_stream_info.if0` (aecp-outputs) | 4.066 (4.470) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | 0 | `aecp_outputs.held_set_stream_info.if0` (aecp-outputs) | 9.108 (9.475) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | 0 | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` (aecp-outputs) | 0.306 (0.745) | fits | 0 aecp | 2 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.353 (0.678) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.123 (0.535) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.112 (0.553) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.106 (0.520) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.099 (0.507) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 113 | 0 | 50,570 (0.506) | fits |
| aecp-fanout | 122 | 0 | 97,003 (0.970) | fits |
| aecp-largest-notice | 105 | 0 | 148,641 (1.486) | fits |
| aecp-reboot | 108 | 0 | 53,399 (0.534) | fits |
| aecp-outputs | 399 | 0 | 62,148 (0.621) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 80 | 24,419 (0.244) | 2,607 (0.026) |
| aecp-fanout | 84 | 25,309 (0.253) | 2,788 (0.028) |
| aecp-largest-notice | 78 | 24,419 (0.244) | 2,607 (0.026) |
| aecp-reboot | 78 | 24,419 (0.244) | 2,607 (0.026) |
| aecp-outputs | 347 | 24,786 (0.248) | 2,794 (0.028) |

Longest pass that carries a step: 25,309 CPU cycles (0.253 ms), aecp-fanout; longest step: 2,794 (0.028 ms), aecp-outputs.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 13,321 | 0.133 | 20 | 24 | fits | 29,649 | 20 | 0.784 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 30,663 | 0.307 | 20 | 24 | fits | 42,569 | 20 | 0.721 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,920 | 0.169 | 20 | 24 | fits | 29,906 | 20 | 0.747 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,487 | 0.165 | 20 | 24 | fits | 29,503 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 19,701 | 0.197 | 20 | 24 | fits | 29,383 | 20 | 0.738 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 17,096 | 0.171 | 20 | 24 | fits | 29,862 | 20 | 0.740 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 19,643 | 0.196 | 20 | 24 | fits | 29,088 | 20 | 0.743 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 16,130 | 0.161 | 20 | 24 | fits | 28,896 | 20 | 0.754 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 19,687 | 0.197 | 20 | 24 | fits | 29,053 | 20 | 0.759 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 23,900 | 0.239 | 20 | 24 | fits | 33,661 | 21 | 0.663 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 16,191 | 0.162 | 20 | 24 | fits | 29,188 | 20 | 0.776 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 19,323 | 0.193 | 20 | 24 | fits | 28,847 | 20 | 0.777 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i79.c0.if0` | 16,267 | 0.163 | 20 | 24 | fits | 29,199 | 20 | 0.746 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 19,986 | 0.200 | 20 | 24 | fits | 29,510 | 20 | 0.746 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 19,772 | 0.198 | 20 | 24 | fits | 29,756 | 20 | 0.747 |
| get_configuration | `aecp.get_configuration.if0` | 14,580 | 0.146 | 20 | 24 | fits | 27,369 | 20 | 0.771 |
| entity_available | `aecp.entity_available.if0` | 17,441 | 0.174 | 20 | 24 | fits | 27,028 | 20 | 0.758 |
| get_name | `aecp.get_name.if0` | 15,186 | 0.152 | 20 | 24 | fits | 29,974 | 20 | 0.766 |
| get_counters | `aecp.get_counters.if0` | 20,667 | 0.207 | 20 | 24 | fits | 31,969 | 20 | 0.767 |
| get_avb_info | `aecp.get_avb_info.if0` | 16,602 | 0.166 | 20 | 24 | fits | 30,023 | 20 | 0.801 |
| get_as_path | `aecp.get_as_path.if0` | 19,908 | 0.199 | 20 | 24 | fits | 35,509 | 100 | 0.567 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,757 | 0.178 | 20 | 24 | fits | 27,067 | 20 | 0.772 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,756 | 0.138 | 20 | 24 | fits | 26,033 | 20 | 0.745 |
| set_name | `aecp.set_name.if0` | 27,606 | 0.276 | 20 | 24 | fits | 50,570 | 44 | 0.773 |
| lock_entity | `aecp.lock_entity.if0` | 20,854 | 0.209 | 20 | 24 | fits | 39,655 | 33 | 0.809 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,228 | 0.192 | 20 | 24 | fits | 39,657 | 33 | 0.808 |
| set_name | `aecp_fanout.set_name.if0` | 47,297 | 0.473 | 20 | 24 | fits | 63,837 | 89 | 0.591 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 43,948 | 0.439 | 20 | 24 | fits | 57,725 | 78 | 0.625 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 58,669 | 0.587 | 20 | 24 | fits | 52,320 | 79 | 0.600 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 43,266 | 0.433 | 20 | 24 | fits | 51,823 | 78 | 0.596 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,344 | 0.513 | 20 | 24 | fits | 65,732 | 110 | 0.610 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 294,590 | 2.946 | 20 | 24 | fits | 62,377 | 109 | 0.595 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 327,365 | 3.274 | 20 | 24 | fits | 76,656 | 110 | 0.613 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 326,211 | 3.262 | 20 | 24 | fits | 75,059 | 109 | 0.611 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 306,980 | 3.070 | 20 | 24 | fits | 54,933 | 67 | 0.628 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 82,041 | 0.820 | 20 | 24 | fits | 97,003 | 77 | 0.645 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 271,037 | 2.710 | 20 | 24 | fits | 61,973 | 78 | 0.635 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 58,545 | 0.585 | 20 | 24 | fits | 52,075 | 78 | 0.599 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 43,794 | 0.438 | 20 | 24 | fits | 51,584 | 79 | 0.590 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 87,690 | 0.877 | 20 | 24 | fits | 42,455 | 59 | 0.507 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 131,916 | 1.319 | 20 | 24 | fits | 148,641 | 137 | 0.325 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 236,761 | 2.368 | 20 | 24 | fits | 137,667 | 113 | 0.295 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 237,210 | 2.372 | 20 | 24 | fits | 54,242 | 24 | 0.671 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 338,248 | 3.382 | 20 | 24 | fits | 80,379 | 17 | 0.644 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 292,971 | 2.930 | 20 | 24 | fits | 92,273 | 17 | 0.660 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 10,649 | 0.106 | 20 | 24 | fits | 30,489 | 17 | 0.799 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 9,902 | 0.099 | 20 | 24 | fits | 30,303 | 17 | 0.794 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 12,291 | 0.123 | 20 | 24 | fits | 30,135 | 17 | 0.791 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 11,225 | 0.112 | 20 | 24 | fits | 31,285 | 17 | 0.812 |
| REBOOT | `aecp_reboot.accepted.if0` | 35,309 | 0.353 | 20 | 24 | fits | 44,462 | 66 | 0.563 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | `aecp_outputs.declared.if0` | 144,827 | 1.448 | 20 | 24 | fits | 42,344 | 60 | 0.496 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 25,934 | 0.259 | 20 | 24 | fits | 36,088 | 18 | 0.819 |
| GET_STREAM_INFO_O1 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o1.if0` | 30,190 | 0.302 | 20 | 24 | fits | 36,031 | 18 | 0.811 |
| GET_STREAM_INFO_O2 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o2.if0` | 26,625 | 0.266 | 20 | 24 | fits | 35,082 | 18 | 0.796 |
| GET_STREAM_INFO_O3 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o3.if0` | 29,388 | 0.294 | 20 | 24 | fits | 35,887 | 18 | 0.811 |
| GET_STREAM_INFO_O4 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o4.if0` | 30,683 | 0.307 | 20 | 24 | fits | 35,921 | 18 | 0.810 |
| GET_STREAM_INFO_O5 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o5.if0` | 26,925 | 0.269 | 20 | 24 | fits | 35,473 | 18 | 0.796 |
| GET_STREAM_INFO_O6 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o6.if0` | 29,997 | 0.300 | 20 | 24 | fits | 36,051 | 18 | 0.810 |
| GET_STREAM_INFO_O7 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o7.if0` | 26,591 | 0.266 | 20 | 24 | fits | 34,969 | 18 | 0.797 |
| GET_STREAM_INFO_O8 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o8.if0` | 25,708 | 0.257 | 20 | 24 | fits | 35,828 | 18 | 0.810 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 30,646 | 0.306 | 20 | 24 | fits | 36,577 | 18 | 0.804 |
| SET_STREAM_INFO_LOCKED of a declaring STREAM_OUTPUT, refused ENTITY_LOCKED | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 30,587 | 0.306 | 20 | 24 | fits | 36,716 | 18 | 0.807 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | `aecp_outputs.held_set_stream_info.if0` | 910,807 | 9.108 | 20 | 24 | fits | 29,128 | 20 | 0.634 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | `aecp_outputs.held_get_stream_info.if0` | 406,600 | 4.066 | 20 | 24 | fits | 29,128 | 20 | 0.634 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
