### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 53 paths and 0 of 55 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.097 (0.337) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.195 (0.446) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.210 (0.465) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.180 (0.427) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.154 (0.411) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.204 (0.453) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.245 (0.614) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.173 (0.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.161 (0.300) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.211 (0.470) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.198 (0.464) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.124 (0.375) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.259 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.118 (0.369) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.191 (0.447) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (156 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.132 (0.385) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i15.c0.if0` (aecp) | 0.122 (0.373) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t23.i0.c0.if0` (aecp) | 0.200 (0.455) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.212 (0.469) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.123 (0.373) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.212 (0.470) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i0.c0.if0` (aecp) | 0.125 (0.379) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.118 (0.259) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.152 (0.398) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.208 (0.590) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.104 (0.351) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.196 (0.505) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.564 (3.897) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.948 (1.137) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.418 (0.668) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.571 (0.734) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.449 (0.594) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.661 (0.970) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.517 (0.775) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.587 (0.901) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.311 (4.628) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 4.267 (4.568) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.512 (0.774) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 4.293 (4.569) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 3.020 (3.350) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 4.848 (5.186) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 4.441 (4.778) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.608 (1.935) | fits | 0 aecp | 1 | 0 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | 0 | `aecp_outputs.declared.if0` (aecp-outputs) | 1.433 (1.482) | fits | 0 acmp | 1 | 0 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | 0 | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` (aecp-outputs) | 0.288 (0.620) | fits | 0 aecp | 1 | 0 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | 0 | `aecp_outputs.held_get_stream_info.if0` (aecp-outputs) | 4.048 (4.382) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | 0 | `aecp_outputs.held_set_stream_info.if0` (aecp-outputs) | 9.098 (9.395) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | 0 | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` (aecp-outputs) | 0.256 (0.604) | fits | 0 aecp | 2 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.345 (0.423) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.215 (0.523) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.124 (0.435) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.218 (0.524) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.233 (0.543) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 112 | 0 | 53,268 (0.666) | fits |
| aecp-fanout | 114 | 0 | 58,709 (0.734) | fits |
| aecp-largest-notice | 103 | 0 | 134,489 (1.681) | fits |
| aecp-reboot | 104 | 0 | 53,268 (0.666) | fits |
| aecp-outputs | 380 | 0 | 53,268 (0.666) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 80 | 16,505 (0.206) | 2,270 (0.028) |
| aecp-fanout | 82 | 16,505 (0.206) | 2,270 (0.028) |
| aecp-largest-notice | 78 | 16,505 (0.206) | 2,270 (0.028) |
| aecp-reboot | 78 | 16,505 (0.206) | 2,270 (0.028) |
| aecp-outputs | 341 | 16,769 (0.210) | 2,270 (0.028) |

Longest pass that carries a step: 16,769 CPU cycles (0.210 ms), aecp-outputs; longest step: 2,270 (0.028 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 12,172 | 0.152 | 20 | 24 | fits | 20,669 | 20 | 0.757 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 12,872 | 0.161 | 20 | 24 | fits | 24,020 | 20 | 0.683 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,857 | 0.211 | 20 | 24 | fits | 21,198 | 20 | 0.721 |
| READ_DESCRIPTOR (156 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 10,564 | 0.132 | 20 | 24 | fits | 20,970 | 20 | 0.707 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 16,945 | 0.212 | 20 | 24 | fits | 21,171 | 20 | 0.713 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i0.c0.if0` | 10,016 | 0.125 | 20 | 24 | fits | 20,414 | 20 | 0.713 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 9,469 | 0.118 | 20 | 24 | fits | 20,720 | 20 | 0.713 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,800 | 0.198 | 20 | 24 | fits | 19,852 | 20 | 0.727 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 9,956 | 0.124 | 20 | 24 | fits | 20,205 | 20 | 0.733 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 20,687 | 0.259 | 20 | 24 | fits | 24,937 | 21 | 0.628 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 9,450 | 0.118 | 20 | 24 | fits | 19,781 | 20 | 0.747 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 15,270 | 0.191 | 20 | 24 | fits | 19,346 | 20 | 0.742 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i15.c0.if0` | 9,790 | 0.122 | 20 | 24 | fits | 20,252 | 20 | 0.722 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t23.i0.c0.if0` | 16,001 | 0.200 | 20 | 24 | fits | 19,998 | 20 | 0.727 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 16,944 | 0.212 | 20 | 24 | fits | 20,987 | 20 | 0.719 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 9,857 | 0.123 | 20 | 24 | fits | 20,255 | 20 | 0.731 |
| get_configuration | `aecp.get_configuration.if0` | 14,402 | 0.180 | 20 | 24 | fits | 17,872 | 20 | 0.721 |
| entity_available | `aecp.entity_available.if0` | 7,730 | 0.097 | 20 | 24 | fits | 17,382 | 20 | 0.695 |
| get_name | `aecp.get_name.if0` | 16,282 | 0.204 | 20 | 24 | fits | 20,216 | 20 | 0.734 |
| get_counters | `aecp.get_counters.if0` | 12,332 | 0.154 | 20 | 24 | fits | 22,784 | 20 | 0.733 |
| get_avb_info | `aecp.get_avb_info.if0` | 16,814 | 0.210 | 20 | 24 | fits | 21,118 | 20 | 0.778 |
| get_as_path | `aecp.get_as_path.if0` | 15,637 | 0.195 | 20 | 24 | fits | 25,487 | 100 | 0.522 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 8,321 | 0.104 | 20 | 24 | fits | 17,946 | 20 | 0.729 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,855 | 0.173 | 20 | 24 | fits | 17,450 | 20 | 0.705 |
| set_name | `aecp.set_name.if0` | 16,614 | 0.208 | 20 | 24 | fits | 37,725 | 44 | 0.752 |
| lock_entity | `aecp.lock_entity.if0` | 19,575 | 0.245 | 20 | 24 | fits | 27,606 | 33 | 0.765 |
| unlock_entity | `aecp.unlock_entity.if0` | 15,717 | 0.196 | 20 | 24 | fits | 28,224 | 33 | 0.776 |
| set_name | `aecp_fanout.set_name.if0` | 46,961 | 0.587 | 20 | 24 | fits | 51,328 | 89 | 0.566 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 35,918 | 0.449 | 20 | 24 | fits | 47,533 | 79 | 0.603 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 41,103 | 0.514 | 20 | 24 | fits | 40,257 | 78 | 0.540 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 41,361 | 0.517 | 20 | 24 | fits | 40,679 | 79 | 0.545 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 45,683 | 0.571 | 20 | 24 | fits | 58,709 | 109 | 0.595 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 285,158 | 3.564 | 20 | 24 | fits | 54,023 | 110 | 0.583 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 344,872 | 4.311 | 20 | 24 | fits | 45,037 | 66 | 0.600 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 52,871 | 0.661 | 20 | 24 | fits | 55,348 | 78 | 0.612 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 341,332 | 4.267 | 20 | 24 | fits | 53,318 | 77 | 0.619 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 33,478 | 0.418 | 20 | 24 | fits | 41,014 | 79 | 0.558 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 40,988 | 0.512 | 20 | 24 | fits | 39,086 | 78 | 0.522 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 75,804 | 0.948 | 20 | 24 | fits | 34,850 | 59 | 0.502 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 128,602 | 1.608 | 20 | 24 | fits | 134,489 | 138 | 0.323 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 343,468 | 4.293 | 20 | 24 | fits | 20,382 | 15 | 0.484 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 241,571 | 3.020 | 20 | 24 | fits | 35,182 | 17 | 0.665 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 387,861 | 4.848 | 20 | 24 | fits | 70,671 | 18 | 0.665 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 355,272 | 4.441 | 20 | 24 | fits | 82,869 | 17 | 0.667 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 17,473 | 0.218 | 20 | 24 | fits | 21,139 | 17 | 0.731 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 18,656 | 0.233 | 20 | 24 | fits | 21,362 | 17 | 0.739 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 17,189 | 0.215 | 20 | 24 | fits | 20,883 | 17 | 0.729 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 9,881 | 0.124 | 20 | 24 | fits | 22,032 | 17 | 0.762 |
| REBOOT | `aecp_reboot.accepted.if0` | 27,621 | 0.345 | 20 | 24 | fits | 33,820 | 66 | 0.495 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | `aecp_outputs.declared.if0` | 114,637 | 1.433 | 20 | 24 | fits | 35,212 | 60 | 0.515 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 23,011 | 0.288 | 20 | 24 | fits | 31,775 | 24 | 0.781 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 18,567 | 0.232 | 20 | 24 | fits | 26,900 | 18 | 0.760 |
| SET_STREAM_INFO_LOCKED of a declaring STREAM_OUTPUT, refused ENTITY_LOCKED | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 20,497 | 0.256 | 20 | 24 | fits | 28,123 | 18 | 0.777 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | `aecp_outputs.held_set_stream_info.if0` | 727,830 | 9.098 | 20 | 24 | fits | 19,785 | 20 | 0.653 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | `aecp_outputs.held_get_stream_info.if0` | 323,823 | 4.048 | 20 | 24 | fits | 19,785 | 20 | 0.653 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
