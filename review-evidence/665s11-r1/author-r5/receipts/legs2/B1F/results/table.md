### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 48 paths and 0 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.120 (0.427) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.253 (0.558) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.123 (0.431) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.158 (0.466) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.252 (0.562) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.184 (0.530) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.223 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.189 (0.503) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.253 (0.562) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.249 (0.554) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.134 (0.444) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.273 (0.577) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.240 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.133 (0.444) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.141 (0.455) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.246 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.143 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.247 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.145 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.254 (0.560) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.139 (0.449) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.226 (0.535) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.252 (0.650) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.121 (0.431) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.147 (0.351) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 1.730 (2.029) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.300 (2.617) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.818 (1.032) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.431 (0.722) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.543 (0.842) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 2.380 (2.692) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.458 (0.797) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.601 (0.890) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.510 (0.779) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.543 (0.829) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.291 (2.577) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.191 (2.498) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.475 (0.742) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.223 (2.532) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.277 (1.631) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.768 (3.118) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.354 (2.703) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.348 (1.638) | fits | 0 aecp | 1 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.471 (0.717) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.169 (0.503) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.194 (0.531) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.169 (0.468) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.132 (0.470) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 119 | 0 | 67,591 (0.676) | fits |
| aecp | 111 | 0 | 44,643 (0.446) | fits |
| aecp-reboot | 108 | 0 | 51,178 (0.512) | fits |
| aecp-largest-notice | 106 | 0 | 144,182 (1.442) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 83 | 22,387 (0.224) | 3,107 (0.031) |
| aecp | 79 | 21,796 (0.218) | 1,915 (0.019) |
| aecp-reboot | 78 | 21,796 (0.218) | 1,915 (0.019) |
| aecp-largest-notice | 78 | 21,796 (0.218) | 1,915 (0.019) |

Longest pass that carries a step: 22,387 CPU cycles (0.224 ms), aecp-fanout; longest step: 3,107 (0.031 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 54,328 | 0.543 | 20 | 24 | fits | 63,243 | 89 | 0.577 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 45,822 | 0.458 | 20 | 24 | fits | 54,697 | 78 | 0.596 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 50,954 | 0.510 | 20 | 24 | fits | 53,477 | 79 | 0.570 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 42,967 | 0.430 | 20 | 24 | fits | 49,439 | 78 | 0.553 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 54,289 | 0.543 | 20 | 24 | fits | 59,934 | 66 | 0.642 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 172,987 | 1.730 | 20 | 24 | fits | 58,115 | 65 | 0.635 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 238,033 | 2.380 | 20 | 24 | fits | 67,591 | 72 | 0.652 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 229,953 | 2.300 | 20 | 24 | fits | 59,199 | 65 | 0.643 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 229,102 | 2.291 | 20 | 24 | fits | 52,801 | 67 | 0.602 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 60,092 | 0.601 | 20 | 24 | fits | 64,711 | 77 | 0.612 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 219,114 | 2.191 | 20 | 24 | fits | 65,171 | 84 | 0.622 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 43,117 | 0.431 | 20 | 24 | fits | 49,857 | 78 | 0.560 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 47,515 | 0.475 | 20 | 24 | fits | 48,941 | 79 | 0.541 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 81,767 | 0.818 | 20 | 24 | fits | 42,298 | 59 | 0.511 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 22,571 | 0.226 | 20 | 24 | fits | 28,356 | 20 | 0.810 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 18,916 | 0.189 | 20 | 24 | fits | 32,297 | 20 | 0.738 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,285 | 0.253 | 20 | 24 | fits | 27,850 | 20 | 0.761 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,094 | 0.141 | 20 | 24 | fits | 27,559 | 20 | 0.758 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 14,510 | 0.145 | 20 | 24 | fits | 28,045 | 20 | 0.759 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 25,352 | 0.254 | 20 | 24 | fits | 27,671 | 20 | 0.753 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 13,869 | 0.139 | 20 | 24 | fits | 26,932 | 20 | 0.759 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 24,853 | 0.249 | 20 | 24 | fits | 27,172 | 20 | 0.770 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 13,428 | 0.134 | 20 | 24 | fits | 26,536 | 20 | 0.772 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 27,255 | 0.273 | 20 | 24 | fits | 29,421 | 21 | 0.678 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 23,975 | 0.240 | 20 | 24 | fits | 26,180 | 20 | 0.786 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 13,295 | 0.133 | 20 | 24 | fits | 26,674 | 20 | 0.790 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 24,584 | 0.246 | 20 | 24 | fits | 26,826 | 20 | 0.757 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 14,283 | 0.143 | 20 | 24 | fits | 27,857 | 20 | 0.763 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 24,731 | 0.247 | 20 | 24 | fits | 27,293 | 20 | 0.770 |
| get_configuration | `aecp.get_configuration.if0` | 12,255 | 0.123 | 20 | 24 | fits | 25,315 | 20 | 0.784 |
| entity_available | `aecp.entity_available.if0` | 12,028 | 0.120 | 20 | 24 | fits | 24,946 | 20 | 0.775 |
| get_name | `aecp.get_name.if0` | 25,241 | 0.252 | 20 | 24 | fits | 27,969 | 20 | 0.781 |
| get_counters | `aecp.get_counters.if0` | 15,768 | 0.158 | 20 | 24 | fits | 28,838 | 20 | 0.771 |
| get_avb_info | `aecp.get_avb_info.if0` | 25,345 | 0.253 | 20 | 24 | fits | 27,417 | 20 | 0.804 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,147 | 0.121 | 20 | 24 | fits | 25,195 | 20 | 0.786 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 22,347 | 0.223 | 20 | 24 | fits | 23,983 | 20 | 0.762 |
| set_name | `aecp.set_name.if0` | 25,169 | 0.252 | 20 | 24 | fits | 44,643 | 43 | 0.762 |
| lock_entity | `aecp.lock_entity.if0` | 18,379 | 0.184 | 20 | 24 | fits | 34,910 | 34 | 0.788 |
| unlock_entity | `aecp.unlock_entity.if0` | 14,657 | 0.147 | 20 | 24 | fits | 35,068 | 33 | 0.775 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 16,940 | 0.169 | 20 | 24 | fits | 27,174 | 17 | 0.788 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 13,206 | 0.132 | 20 | 24 | fits | 26,486 | 17 | 0.781 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 16,905 | 0.169 | 20 | 24 | fits | 26,424 | 17 | 0.778 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 19,371 | 0.194 | 20 | 24 | fits | 27,852 | 17 | 0.800 |
| REBOOT | `aecp_reboot.accepted.if0` | 47,118 | 0.471 | 20 | 24 | fits | 45,174 | 66 | 0.524 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 134,826 | 1.348 | 20 | 24 | fits | 144,182 | 92 | 0.333 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 222,292 | 2.223 | 20 | 24 | fits | 135,184 | 70 | 0.308 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 127,724 | 1.277 | 20 | 24 | fits | 41,430 | 17 | 0.710 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 276,769 | 2.768 | 20 | 24 | fits | 90,875 | 18 | 0.689 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 235,416 | 2.354 | 20 | 24 | fits | 92,113 | 17 | 0.690 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
