### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 42 paths and 0 of 43 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.101 (0.446) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.256 (0.597) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.256 (0.605) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.231 (0.579) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.148 (0.505) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.253 (0.603) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.280 (0.719) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.224 (0.569) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.161 (0.515) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.255 (0.606) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.245 (0.594) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.124 (0.475) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.334 (0.693) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.248 (0.612) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.120 (0.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.123 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.246 (0.597) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.129 (0.481) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.251 (0.603) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.127 (0.481) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.255 (0.606) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.123 (0.474) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.222 (0.571) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.192 (0.652) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.112 (0.464) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.177 (0.570) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.596 (2.943) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.828 (0.860) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.369 (0.479) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 0.580 (0.731) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.393 (0.528) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.821 (1.142) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.412 (0.722) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.451 (0.812) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.974 (3.307) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 2.795 (3.165) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.408 (0.719) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.452 (2.825) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.824 (2.284) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.030 (3.444) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.783 (4.206) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.966 (2.335) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 119 | 0 | 93,354 (0.934) | fits |
| aecp | 113 | 0 | 45,830 (0.458) | fits |
| aecp-largest-notice | 106 | 2 | 211,422 (2.114) | OVER the share |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 82 | 25,408 (0.254) | 2,555 (0.026) |
| aecp | 80 | 25,408 (0.254) | 2,555 (0.026) |
| aecp-largest-notice | 78 | 25,408 (0.254) | 2,555 (0.026) |

Longest pass that carries a step: 25,408 CPU cycles (0.254 ms), aecp-fanout; longest step: 2,555 (0.026 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 45,054 | 0.451 | 20 | 24 | fits | 58,622 | 88 | 0.556 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 39,274 | 0.393 | 20 | 24 | fits | 52,760 | 77 | 0.581 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 41,223 | 0.412 | 20 | 24 | fits | 48,137 | 78 | 0.552 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 38,698 | 0.387 | 20 | 24 | fits | 47,826 | 77 | 0.541 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 57,971 | 0.580 | 20 | 24 | fits | 73,087 | 110 | 0.591 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 259,578 | 2.596 | 20 | 24 | fits | 70,594 | 109 | 0.595 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 297,402 | 2.974 | 20 | 24 | fits | 51,931 | 67 | 0.596 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 82,062 | 0.821 | 20 | 24 | fits | 93,354 | 76 | 0.612 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 279,478 | 2.795 | 20 | 24 | fits | 56,981 | 78 | 0.597 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 36,927 | 0.369 | 20 | 24 | fits | 47,937 | 77 | 0.548 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 40,813 | 0.408 | 20 | 24 | fits | 47,751 | 78 | 0.540 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 82,827 | 0.828 | 20 | 24 | fits | 41,525 | 59 | 0.511 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 22,224 | 0.222 | 20 | 24 | fits | 28,303 | 20 | 0.750 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 16,111 | 0.161 | 20 | 24 | fits | 32,165 | 20 | 0.674 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 25,492 | 0.255 | 20 | 24 | fits | 28,265 | 20 | 0.699 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 12,310 | 0.123 | 20 | 24 | fits | 27,842 | 20 | 0.689 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 12,717 | 0.127 | 20 | 24 | fits | 28,520 | 20 | 0.687 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 25,477 | 0.255 | 20 | 24 | fits | 28,298 | 20 | 0.687 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,258 | 0.123 | 20 | 24 | fits | 27,790 | 20 | 0.693 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 24,504 | 0.245 | 20 | 24 | fits | 27,175 | 20 | 0.699 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,377 | 0.124 | 20 | 24 | fits | 27,901 | 20 | 0.713 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 33,409 | 0.334 | 20 | 24 | fits | 36,961 | 27 | 0.596 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 24,799 | 0.248 | 20 | 24 | fits | 27,612 | 20 | 0.729 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 11,971 | 0.120 | 20 | 24 | fits | 27,495 | 20 | 0.733 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 24,616 | 0.246 | 20 | 24 | fits | 27,366 | 20 | 0.690 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,910 | 0.129 | 20 | 24 | fits | 28,513 | 20 | 0.699 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,112 | 0.251 | 20 | 24 | fits | 27,933 | 20 | 0.691 |
| get_configuration | `aecp.get_configuration.if0` | 23,110 | 0.231 | 20 | 24 | fits | 25,665 | 20 | 0.712 |
| entity_available | `aecp.entity_available.if0` | 10,058 | 0.101 | 20 | 24 | fits | 25,339 | 20 | 0.698 |
| get_name | `aecp.get_name.if0` | 25,268 | 0.253 | 20 | 24 | fits | 28,229 | 20 | 0.726 |
| get_counters | `aecp.get_counters.if0` | 14,818 | 0.148 | 20 | 24 | fits | 30,428 | 20 | 0.719 |
| get_avb_info | `aecp.get_avb_info.if0` | 25,576 | 0.256 | 20 | 24 | fits | 28,344 | 20 | 0.756 |
| get_as_path | `aecp.get_as_path.if0` | 25,614 | 0.256 | 20 | 24 | fits | 34,116 | 100 | 0.525 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 11,223 | 0.112 | 20 | 24 | fits | 25,991 | 20 | 0.734 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 22,369 | 0.224 | 20 | 24 | fits | 24,752 | 20 | 0.685 |
| set_name | `aecp.set_name.if0` | 19,229 | 0.192 | 20 | 24 | fits | 45,830 | 43 | 0.749 |
| lock_entity | `aecp.lock_entity.if0` | 27,967 | 0.280 | 20 | 24 | fits | 34,415 | 33 | 0.752 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,737 | 0.177 | 20 | 24 | fits | 35,094 | 32 | 0.773 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 196,643 | 1.966 | 20 | 24 | fits | 211,422 | 137 | 0.318 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 245,206 | 2.452 | 20 | 24 | fits | 208,038 | 118 | 0.317 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 182,417 | 1.824 | 20 | 24 | fits | 60,902 | 17 | 0.668 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 302,962 | 3.030 | 20 | 24 | fits | 101,725 | 18 | 0.665 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 378,262 | 3.783 | 20 | 24 | fits | 160,591 | 17 | 0.669 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
