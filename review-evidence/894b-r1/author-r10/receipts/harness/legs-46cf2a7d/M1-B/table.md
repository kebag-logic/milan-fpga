### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 43 paths and 0 of 44 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.233 (0.543) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.209 (0.525) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.091 (0.252) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.274 (0.591) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.211 (0.526) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.297 (0.657) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.115 (0.419) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.304 (0.626) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.208 (0.523) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.205 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.255 (0.572) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.227 (0.541) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.213 (0.529) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.249 (0.565) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.263 (0.584) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.208 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.113 (0.282) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.210 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.209 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.216 (0.537) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.258 (0.576) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.196 (0.510) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.298 (0.722) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.090 (0.255) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.263 (0.635) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.570 (2.881) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.197 (3.525) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.819 (0.855) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.404 (0.515) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.479 (0.794) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.388 (3.717) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.569 (0.931) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.676 (1.003) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.541 (0.831) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.649 (0.986) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.470 (3.786) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.852 (3.168) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.535 (0.824) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.222 (3.555) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.053 (2.417) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.805 (4.159) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.151 (3.503) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.480 (1.816) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 122 | 0 | 67,973 (0.680) | fits |
| aecp | 112 | 0 | 45,623 (0.456) | fits |
| aecp-largest-notice | 106 | 0 | 151,310 (1.513) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 84 | 23,253 (0.233) | 4,038 (0.040) |
| aecp | 79 | 21,857 (0.219) | 2,198 (0.022) |
| aecp-largest-notice | 78 | 21,857 (0.219) | 2,198 (0.022) |

Longest pass that carries a step: 23,253 CPU cycles (0.233 ms), aecp-fanout; longest step: 4,038 (0.040 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 64,934 | 0.649 | 20 | 24 | fits | 67,908 | 95 | 0.590 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 56,924 | 0.569 | 20 | 24 | fits | 56,849 | 78 | 0.604 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 43,981 | 0.440 | 20 | 24 | fits | 54,663 | 79 | 0.563 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 54,072 | 0.541 | 20 | 24 | fits | 51,343 | 78 | 0.556 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 47,879 | 0.479 | 20 | 24 | fits | 61,198 | 66 | 0.639 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 257,034 | 2.570 | 20 | 24 | fits | 58,298 | 65 | 0.628 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 338,822 | 3.388 | 20 | 24 | fits | 62,772 | 66 | 0.648 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 319,684 | 3.197 | 20 | 24 | fits | 60,543 | 65 | 0.641 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 347,040 | 3.470 | 20 | 24 | fits | 54,493 | 67 | 0.603 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 67,586 | 0.676 | 20 | 24 | fits | 67,973 | 77 | 0.611 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 285,226 | 2.852 | 20 | 24 | fits | 60,409 | 78 | 0.611 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 40,388 | 0.404 | 20 | 24 | fits | 51,538 | 78 | 0.563 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 53,473 | 0.535 | 20 | 24 | fits | 50,789 | 79 | 0.554 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 81,886 | 0.819 | 20 | 24 | fits | 43,522 | 59 | 0.532 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 19,636 | 0.196 | 20 | 24 | fits | 28,211 | 20 | 0.784 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 30,449 | 0.304 | 20 | 24 | fits | 32,961 | 20 | 0.732 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 20,798 | 0.208 | 20 | 24 | fits | 27,752 | 20 | 0.738 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 26,280 | 0.263 | 20 | 24 | fits | 28,261 | 20 | 0.750 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 20,895 | 0.209 | 20 | 24 | fits | 27,779 | 20 | 0.733 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 21,577 | 0.216 | 20 | 24 | fits | 28,390 | 20 | 0.747 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 25,751 | 0.258 | 20 | 24 | fits | 27,640 | 20 | 0.753 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 20,494 | 0.205 | 20 | 24 | fits | 27,220 | 20 | 0.750 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 25,472 | 0.255 | 20 | 24 | fits | 27,012 | 20 | 0.763 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 22,704 | 0.227 | 20 | 24 | fits | 29,462 | 21 | 0.654 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 21,274 | 0.213 | 20 | 24 | fits | 26,724 | 20 | 0.779 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 24,927 | 0.249 | 20 | 24 | fits | 26,975 | 20 | 0.779 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 20,829 | 0.208 | 20 | 24 | fits | 26,945 | 20 | 0.737 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 11,278 | 0.113 | 20 | 24 | fits | 28,178 | 20 | 0.751 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 20,963 | 0.210 | 20 | 24 | fits | 27,298 | 20 | 0.750 |
| get_configuration | `aecp.get_configuration.if0` | 9,142 | 0.091 | 20 | 24 | fits | 25,190 | 20 | 0.764 |
| entity_available | `aecp.entity_available.if0` | 23,287 | 0.233 | 20 | 24 | fits | 24,620 | 20 | 0.745 |
| get_name | `aecp.get_name.if0` | 21,091 | 0.211 | 20 | 24 | fits | 27,399 | 20 | 0.749 |
| get_counters | `aecp.get_counters.if0` | 27,438 | 0.274 | 20 | 24 | fits | 29,039 | 20 | 0.750 |
| get_avb_info | `aecp.get_avb_info.if0` | 20,864 | 0.209 | 20 | 24 | fits | 27,258 | 20 | 0.783 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 8,963 | 0.090 | 20 | 24 | fits | 25,495 | 20 | 0.772 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 11,541 | 0.115 | 20 | 24 | fits | 24,483 | 20 | 0.740 |
| set_name | `aecp.set_name.if0` | 29,769 | 0.298 | 20 | 24 | fits | 45,623 | 43 | 0.775 |
| lock_entity | `aecp.lock_entity.if0` | 29,670 | 0.297 | 20 | 24 | fits | 35,809 | 34 | 0.782 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,270 | 0.263 | 20 | 24 | fits | 36,758 | 33 | 0.779 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 148,000 | 1.480 | 20 | 24 | fits | 151,310 | 98 | 0.341 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 322,217 | 3.222 | 20 | 24 | fits | 136,897 | 70 | 0.293 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 205,338 | 2.053 | 20 | 24 | fits | 41,203 | 17 | 0.679 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 380,540 | 3.805 | 20 | 24 | fits | 91,564 | 18 | 0.657 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 315,104 | 3.151 | 20 | 24 | fits | 93,429 | 17 | 0.667 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
