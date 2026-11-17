### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 41 paths and 0 of 42 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.216 (0.597) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.237 (0.629) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.171 (0.551) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.256 (0.641) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.192 (0.578) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.273 (0.705) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.216 (0.599) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.276 (0.664) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.191 (0.576) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.187 (0.571) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.239 (0.626) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.283 (0.672) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.186 (0.571) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.233 (0.621) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.238 (0.623) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.186 (0.571) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.241 (0.630) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.237 (0.625) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.239 (0.626) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.198 (0.586) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.235 (0.621) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.168 (0.552) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.258 (0.738) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.174 (0.551) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.283 (0.715) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.868 (3.224) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.951 (1.207) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.480 (0.823) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 0.646 (1.015) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.493 (0.883) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 1.014 (1.366) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.527 (0.850) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.559 (0.928) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.146 (3.489) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.377 (2.733) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.517 (0.840) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.933 (3.235) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.516 (1.969) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.197 (3.632) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.404 (3.851) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 2.170 (2.551) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 118 | 0 | 103,103 (1.031) | fits |
| aecp | 113 | 0 | 46,778 (0.468) | fits |
| aecp-largest-notice | 107 | 2 | 222,434 (2.224) | OVER the share |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 83 | 25,864 (0.259) | 2,293 (0.023) |
| aecp | 80 | 25,864 (0.259) | 2,293 (0.023) |
| aecp-largest-notice | 79 | 25,864 (0.259) | 2,451 (0.025) |

Longest pass that carries a step: 25,864 CPU cycles (0.259 ms), aecp-fanout; longest step: 2,451 (0.025 ms), aecp-largest-notice.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 55,875 | 0.559 | 20 | 24 | fits | 59,696 | 87 | 0.578 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 49,307 | 0.493 | 20 | 24 | fits | 55,049 | 77 | 0.589 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 52,657 | 0.527 | 20 | 24 | fits | 51,737 | 78 | 0.562 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 41,412 | 0.414 | 20 | 24 | fits | 61,323 | 92 | 0.592 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 64,598 | 0.646 | 20 | 24 | fits | 71,517 | 66 | 0.646 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 286,766 | 2.868 | 20 | 24 | fits | 69,126 | 65 | 0.644 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 314,591 | 3.146 | 20 | 24 | fits | 55,215 | 67 | 0.595 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 101,380 | 1.014 | 20 | 24 | fits | 103,103 | 76 | 0.615 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 237,707 | 2.377 | 20 | 24 | fits | 64,626 | 82 | 0.603 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 48,043 | 0.480 | 20 | 24 | fits | 51,355 | 78 | 0.556 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 51,747 | 0.517 | 20 | 24 | fits | 50,487 | 78 | 0.546 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 95,133 | 0.951 | 20 | 24 | fits | 44,389 | 58 | 0.541 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,827 | 0.168 | 20 | 24 | fits | 30,833 | 20 | 0.788 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 27,643 | 0.276 | 20 | 24 | fits | 34,590 | 20 | 0.714 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 19,135 | 0.191 | 20 | 24 | fits | 30,460 | 20 | 0.739 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 23,752 | 0.238 | 20 | 24 | fits | 30,344 | 20 | 0.737 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 23,917 | 0.239 | 20 | 24 | fits | 30,585 | 20 | 0.737 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 19,822 | 0.198 | 20 | 24 | fits | 31,405 | 20 | 0.735 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 23,487 | 0.235 | 20 | 24 | fits | 30,234 | 20 | 0.741 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 18,696 | 0.187 | 20 | 24 | fits | 29,909 | 20 | 0.748 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 23,903 | 0.239 | 20 | 24 | fits | 30,695 | 20 | 0.759 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 28,289 | 0.283 | 20 | 24 | fits | 35,243 | 21 | 0.661 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 18,626 | 0.186 | 20 | 24 | fits | 29,894 | 20 | 0.772 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 23,254 | 0.233 | 20 | 24 | fits | 29,901 | 20 | 0.778 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 18,584 | 0.186 | 20 | 24 | fits | 29,956 | 20 | 0.739 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 24,115 | 0.241 | 20 | 24 | fits | 30,920 | 20 | 0.746 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 23,722 | 0.237 | 20 | 24 | fits | 30,590 | 20 | 0.746 |
| get_configuration | `aecp.get_configuration.if0` | 17,067 | 0.171 | 20 | 24 | fits | 27,967 | 20 | 0.755 |
| entity_available | `aecp.entity_available.if0` | 21,581 | 0.216 | 20 | 24 | fits | 27,779 | 20 | 0.745 |
| get_name | `aecp.get_name.if0` | 19,181 | 0.192 | 20 | 24 | fits | 30,498 | 20 | 0.763 |
| get_counters | `aecp.get_counters.if0` | 25,550 | 0.256 | 20 | 24 | fits | 32,076 | 20 | 0.747 |
| get_avb_info | `aecp.get_avb_info.if0` | 23,715 | 0.237 | 20 | 24 | fits | 31,073 | 20 | 0.792 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,370 | 0.174 | 20 | 24 | fits | 28,459 | 20 | 0.766 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 21,618 | 0.216 | 20 | 24 | fits | 27,728 | 20 | 0.748 |
| set_name | `aecp.set_name.if0` | 25,814 | 0.258 | 20 | 24 | fits | 46,778 | 41 | 0.765 |
| lock_entity | `aecp.lock_entity.if0` | 27,275 | 0.273 | 20 | 24 | fits | 38,592 | 33 | 0.777 |
| unlock_entity | `aecp.unlock_entity.if0` | 28,259 | 0.283 | 20 | 24 | fits | 39,201 | 32 | 0.784 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 216,985 | 2.170 | 20 | 24 | fits | 222,434 | 91 | 0.334 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 293,286 | 2.933 | 20 | 24 | fits | 217,810 | 70 | 0.312 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 151,573 | 1.516 | 20 | 24 | fits | 69,258 | 23 | 0.704 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 319,702 | 3.197 | 20 | 24 | fits | 115,692 | 18 | 0.681 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 340,360 | 3.404 | 20 | 24 | fits | 176,243 | 17 | 0.673 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
