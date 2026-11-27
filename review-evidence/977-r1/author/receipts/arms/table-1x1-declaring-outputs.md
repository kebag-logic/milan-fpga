### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 54 paths and 0 of 57 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.143 (0.404) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.221 (0.491) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.189 (0.459) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.160 (0.424) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.190 (0.460) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.179 (0.444) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.219 (0.548) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.150 (0.407) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.214 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.172 (0.436) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.167 (0.431) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.177 (0.442) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.188 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.174 (0.439) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.158 (0.422) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.181 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.180 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.184 (0.450) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.162 (0.428) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.174 (0.438) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.188 (0.453) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.181 (0.444) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.120 (0.384) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.226 (0.599) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.143 (0.410) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.207 (0.547) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.954 (3.250) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.390 (3.659) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.800 (1.020) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.385 (0.655) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.511 (0.779) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.363 (3.675) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.425 (0.687) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.540 (0.800) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.390 (0.657) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.443 (0.723) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.417 (3.677) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.371 (3.673) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.412 (0.659) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.118 (3.387) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.288 (2.615) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.883 (4.207) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.572 (3.896) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.396 (1.677) | fits | 0 aecp | 1 | 0 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | 0 | `aecp_outputs.declared.if0` (aecp-outputs) | 1.191 (1.360) | fits | 0 acmp | 1 | 0 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | 0 | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` (aecp-outputs) | 0.219 (0.545) | fits | 0 aecp | 2 | 0 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | 0 | `aecp_outputs.held_get_stream_info.if0` (aecp-outputs) | 4.074 (4.223) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | 0 | `aecp_outputs.held_set_stream_info.if0` (aecp-outputs) | 9.112 (9.372) | fits | 0 aecp | 1 | 0 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | 0 | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` (aecp-outputs) | 0.246 (0.577) | fits | 0 aecp | 2 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.344 (0.567) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.120 (0.424) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.143 (0.454) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.120 (0.427) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.126 (0.434) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 112 | 0 | 42,119 (0.421) | fits |
| aecp-fanout | 120 | 0 | 60,978 (0.610) | fits |
| aecp-largest-notice | 106 | 0 | 151,035 (1.510) | fits |
| aecp-reboot | 108 | 0 | 46,274 (0.463) | fits |
| aecp-outputs | 387 | 0 | 56,155 (0.562) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 19,719 (0.197) | 2,724 (0.027) |
| aecp-fanout | 84 | 38,828 (0.388) | 2,858 (0.029) |
| aecp-largest-notice | 78 | 19,719 (0.197) | 2,724 (0.027) |
| aecp-reboot | 78 | 19,719 (0.197) | 2,724 (0.027) |
| aecp-outputs | 342 | 19,878 (0.199) | 2,724 (0.027) |

Longest pass that carries a step: 38,828 CPU cycles (0.388 ms), aecp-fanout; longest step: 2,858 (0.029 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 12,045 | 0.120 | 20 | 24 | fits | 24,650 | 20 | 0.772 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 21,356 | 0.214 | 20 | 24 | fits | 28,631 | 20 | 0.716 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 17,208 | 0.172 | 20 | 24 | fits | 25,597 | 20 | 0.746 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,057 | 0.181 | 20 | 24 | fits | 24,994 | 20 | 0.733 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 17,358 | 0.174 | 20 | 24 | fits | 25,774 | 20 | 0.737 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,761 | 0.188 | 20 | 24 | fits | 25,674 | 20 | 0.739 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 18,098 | 0.181 | 20 | 24 | fits | 24,705 | 20 | 0.737 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 16,691 | 0.167 | 20 | 24 | fits | 25,014 | 20 | 0.754 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,735 | 0.177 | 20 | 24 | fits | 24,328 | 20 | 0.750 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 18,818 | 0.188 | 20 | 24 | fits | 27,308 | 21 | 0.658 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 17,436 | 0.174 | 20 | 24 | fits | 24,018 | 20 | 0.770 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 15,787 | 0.158 | 20 | 24 | fits | 24,109 | 20 | 0.767 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,970 | 0.180 | 20 | 24 | fits | 24,890 | 20 | 0.741 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,403 | 0.184 | 20 | 24 | fits | 25,457 | 20 | 0.743 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 16,197 | 0.162 | 20 | 24 | fits | 24,675 | 20 | 0.754 |
| get_configuration | `aecp.get_configuration.if0` | 16,030 | 0.160 | 20 | 24 | fits | 22,793 | 20 | 0.767 |
| entity_available | `aecp.entity_available.if0` | 14,258 | 0.143 | 20 | 24 | fits | 22,492 | 20 | 0.752 |
| get_name | `aecp.get_name.if0` | 17,854 | 0.179 | 20 | 24 | fits | 24,857 | 20 | 0.761 |
| get_counters | `aecp.get_counters.if0` | 18,987 | 0.190 | 20 | 24 | fits | 28,029 | 20 | 0.758 |
| get_avb_info | `aecp.get_avb_info.if0` | 18,878 | 0.189 | 20 | 24 | fits | 25,479 | 20 | 0.791 |
| get_as_path | `aecp.get_as_path.if0` | 22,070 | 0.221 | 20 | 24 | fits | 31,025 | 99 | 0.564 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 14,299 | 0.143 | 20 | 24 | fits | 22,686 | 20 | 0.766 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,977 | 0.150 | 20 | 24 | fits | 21,101 | 20 | 0.725 |
| set_name | `aecp.set_name.if0` | 22,643 | 0.226 | 20 | 24 | fits | 42,119 | 44 | 0.768 |
| lock_entity | `aecp.lock_entity.if0` | 21,908 | 0.219 | 20 | 24 | fits | 34,387 | 33 | 0.806 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,654 | 0.207 | 20 | 24 | fits | 33,399 | 33 | 0.798 |
| set_name | `aecp_fanout.set_name.if0` | 44,285 | 0.443 | 20 | 24 | fits | 55,202 | 89 | 0.591 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 42,465 | 0.425 | 20 | 24 | fits | 49,539 | 78 | 0.621 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 38,970 | 0.390 | 20 | 24 | fits | 45,688 | 79 | 0.592 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 38,170 | 0.382 | 20 | 24 | fits | 44,882 | 78 | 0.586 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,088 | 0.511 | 20 | 24 | fits | 59,467 | 109 | 0.606 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 295,436 | 2.954 | 20 | 24 | fits | 60,232 | 114 | 0.601 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 336,272 | 3.363 | 20 | 24 | fits | 59,916 | 109 | 0.600 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 338,959 | 3.390 | 20 | 24 | fits | 59,609 | 108 | 0.608 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 341,705 | 3.417 | 20 | 24 | fits | 47,799 | 67 | 0.616 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 54,029 | 0.540 | 20 | 24 | fits | 60,978 | 77 | 0.638 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 337,143 | 3.371 | 20 | 24 | fits | 59,480 | 78 | 0.635 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 38,517 | 0.385 | 20 | 24 | fits | 45,397 | 78 | 0.590 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 41,235 | 0.412 | 20 | 24 | fits | 45,149 | 79 | 0.584 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 80,004 | 0.800 | 20 | 24 | fits | 38,828 | 59 | 0.529 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 139,605 | 1.396 | 20 | 24 | fits | 151,035 | 136 | 0.326 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 311,776 | 3.118 | 20 | 24 | fits | 143,244 | 112 | 0.301 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 228,806 | 2.288 | 20 | 24 | fits | 38,434 | 18 | 0.668 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 388,259 | 3.883 | 20 | 24 | fits | 87,540 | 17 | 0.671 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 357,156 | 3.572 | 20 | 24 | fits | 97,511 | 17 | 0.669 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 12,021 | 0.120 | 20 | 24 | fits | 25,493 | 17 | 0.796 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 12,638 | 0.126 | 20 | 24 | fits | 25,038 | 17 | 0.785 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 11,968 | 0.120 | 20 | 24 | fits | 25,065 | 17 | 0.783 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 14,326 | 0.143 | 20 | 24 | fits | 25,941 | 17 | 0.801 |
| REBOOT | `aecp_reboot.accepted.if0` | 34,364 | 0.344 | 20 | 24 | fits | 38,243 | 66 | 0.550 |
| a Talker declared, from its PROBE_TX's commit to its STREAM_OUTPUT's notice, completed, to every registration (#936, #943) | `aecp_outputs.declared.if0` | 119,123 | 1.191 | 20 | 24 | fits | 37,657 | 60 | 0.490 |
| GET_STREAM_INFO_O0 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o0.if0` | 21,902 | 0.219 | 20 | 24 | fits | 32,207 | 18 | 0.816 |
| GET_STREAM_INFO_O1 of a declaring STREAM_OUTPUT | `aecp_outputs.get_stream_info.get_stream_info_o1.if0` | 21,136 | 0.211 | 20 | 24 | fits | 31,172 | 18 | 0.802 |
| SET_STREAM_INFO_STREAM_ID of a declaring STREAM_OUTPUT, refused NOT_SUPPORTED | `aecp_outputs.set_stream_info.set_stream_info_stream_id.if0` | 23,723 | 0.237 | 20 | 24 | fits | 32,187 | 18 | 0.798 |
| SET_STREAM_INFO_LOCKED of a declaring STREAM_OUTPUT, refused ENTITY_LOCKED | `aecp_outputs.set_stream_info.set_stream_info_locked.if0` | 24,636 | 0.246 | 20 | 24 | fits | 32,210 | 18 | 0.799 |
| SET_STREAM_INFO of a declaring STREAM_OUTPUT, its notices past the AECP ring's room behind a held egress | `aecp_outputs.held_set_stream_info.if0` | 911,243 | 9.112 | 20 | 24 | fits | 21,769 | 20 | 0.633 |
| GET_STREAM_INFO of a declaring STREAM_OUTPUT behind a held egress | `aecp_outputs.held_get_stream_info.if0` | 407,356 | 4.074 | 20 | 24 | fits | 21,769 | 20 | 0.633 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
