### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 48 paths and 0 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.117 (0.345) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.224 (0.457) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.115 (0.237) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.085 (0.205) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.173 (0.411) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.113 (0.235) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.151 (0.322) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.121 (0.355) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.189 (0.425) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.121 (0.245) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.109 (0.233) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.144 (0.378) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.172 (0.297) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.136 (0.370) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.099 (0.223) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (156 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.149 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i15.c0.if0` (aecp) | 0.141 (0.374) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t23.i0.c0.if0` (aecp) | 0.108 (0.230) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.149 (0.385) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.126 (0.347) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.121 (0.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i0.c0.if0` (aecp) | 0.144 (0.379) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.115 (0.240) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.164 (0.399) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.232 (0.586) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.165 (0.387) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.222 (0.517) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.860 (3.167) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.893 (1.072) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.472 (0.649) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.653 (0.934) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.514 (0.783) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.630 (0.891) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.438 (0.672) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.508 (0.800) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.295 (3.601) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.283 (3.550) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.434 (0.704) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.316 (3.591) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.258 (2.575) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.733 (4.048) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.694 (4.014) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.541 (1.837) | fits | 0 aecp | 1 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.355 (0.568) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.147 (0.439) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.204 (0.499) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.155 (0.449) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.171 (0.463) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 117 | 0 | 56,593 (0.707) | fits |
| aecp | 115 | 0 | 35,976 (0.450) | fits |
| aecp-reboot | 108 | 0 | 39,198 (0.490) | fits |
| aecp-largest-notice | 106 | 0 | 132,177 (1.652) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 82 | 15,538 (0.194) | 2,350 (0.029) |
| aecp | 80 | 15,538 (0.194) | 2,350 (0.029) |
| aecp-reboot | 78 | 15,538 (0.194) | 2,350 (0.029) |
| aecp-largest-notice | 78 | 15,538 (0.194) | 2,350 (0.029) |

Longest pass that carries a step: 15,538 CPU cycles (0.194 ms), aecp-fanout; longest step: 2,350 (0.029 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 40,665 | 0.508 | 20 | 24 | fits | 48,770 | 89 | 0.556 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 41,119 | 0.514 | 20 | 24 | fits | 44,180 | 78 | 0.593 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 34,929 | 0.437 | 20 | 24 | fits | 38,335 | 79 | 0.530 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 35,009 | 0.438 | 20 | 24 | fits | 38,734 | 78 | 0.538 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 52,231 | 0.653 | 20 | 24 | fits | 56,593 | 109 | 0.585 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 228,808 | 2.860 | 20 | 24 | fits | 55,598 | 114 | 0.578 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 263,624 | 3.295 | 20 | 24 | fits | 41,812 | 67 | 0.587 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 50,386 | 0.630 | 20 | 24 | fits | 52,897 | 77 | 0.612 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 262,621 | 3.283 | 20 | 24 | fits | 48,934 | 77 | 0.600 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 37,729 | 0.472 | 20 | 24 | fits | 39,111 | 79 | 0.544 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 34,718 | 0.434 | 20 | 24 | fits | 37,226 | 79 | 0.514 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 71,406 | 0.893 | 20 | 24 | fits | 33,620 | 58 | 0.488 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 13,123 | 0.164 | 20 | 24 | fits | 20,142 | 20 | 0.752 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 15,141 | 0.189 | 20 | 24 | fits | 23,034 | 20 | 0.667 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 9,677 | 0.121 | 20 | 24 | fits | 19,578 | 20 | 0.688 |
| READ_DESCRIPTOR (156 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 11,946 | 0.149 | 20 | 24 | fits | 19,389 | 20 | 0.671 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 9,665 | 0.121 | 20 | 24 | fits | 19,693 | 20 | 0.679 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i0.c0.if0` | 11,533 | 0.144 | 20 | 24 | fits | 18,995 | 20 | 0.681 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 9,178 | 0.115 | 20 | 24 | fits | 19,205 | 20 | 0.683 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 8,743 | 0.109 | 20 | 24 | fits | 18,655 | 20 | 0.701 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 11,534 | 0.144 | 20 | 24 | fits | 18,986 | 20 | 0.705 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 13,729 | 0.172 | 20 | 24 | fits | 23,746 | 21 | 0.595 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 10,910 | 0.136 | 20 | 24 | fits | 18,283 | 20 | 0.721 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 7,946 | 0.099 | 20 | 24 | fits | 17,805 | 20 | 0.714 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i15.c0.if0` | 11,293 | 0.141 | 20 | 24 | fits | 18,753 | 20 | 0.691 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t23.i0.c0.if0` | 8,644 | 0.108 | 20 | 24 | fits | 18,424 | 20 | 0.699 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 11,958 | 0.149 | 20 | 24 | fits | 19,489 | 20 | 0.690 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 10,085 | 0.126 | 20 | 24 | fits | 18,352 | 20 | 0.689 |
| get_configuration | `aecp.get_configuration.if0` | 6,771 | 0.085 | 20 | 24 | fits | 16,399 | 20 | 0.697 |
| entity_available | `aecp.entity_available.if0` | 9,324 | 0.117 | 20 | 24 | fits | 16,475 | 20 | 0.686 |
| get_name | `aecp.get_name.if0` | 9,027 | 0.113 | 20 | 24 | fits | 18,837 | 20 | 0.715 |
| get_counters | `aecp.get_counters.if0` | 13,829 | 0.173 | 20 | 24 | fits | 21,045 | 20 | 0.706 |
| get_avb_info | `aecp.get_avb_info.if0` | 9,203 | 0.115 | 20 | 24 | fits | 18,997 | 20 | 0.747 |
| get_as_path | `aecp.get_as_path.if0` | 17,911 | 0.224 | 20 | 24 | fits | 24,661 | 99 | 0.506 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,217 | 0.165 | 20 | 24 | fits | 16,827 | 20 | 0.721 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,717 | 0.121 | 20 | 24 | fits | 16,474 | 20 | 0.698 |
| set_name | `aecp.set_name.if0` | 18,575 | 0.232 | 20 | 24 | fits | 35,976 | 44 | 0.750 |
| lock_entity | `aecp.lock_entity.if0` | 12,060 | 0.151 | 20 | 24 | fits | 25,728 | 33 | 0.758 |
| unlock_entity | `aecp.unlock_entity.if0` | 17,763 | 0.222 | 20 | 24 | fits | 27,103 | 33 | 0.777 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 12,381 | 0.155 | 20 | 24 | fits | 20,668 | 17 | 0.746 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 13,675 | 0.171 | 20 | 24 | fits | 20,163 | 17 | 0.734 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 11,797 | 0.147 | 20 | 24 | fits | 19,843 | 17 | 0.730 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 16,348 | 0.204 | 20 | 24 | fits | 21,071 | 17 | 0.766 |
| REBOOT | `aecp_reboot.accepted.if0` | 28,415 | 0.355 | 20 | 24 | fits | 32,638 | 66 | 0.495 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 123,277 | 1.541 | 20 | 24 | fits | 132,177 | 136 | 0.306 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 265,268 | 3.316 | 20 | 24 | fits | 126,249 | 113 | 0.289 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 180,679 | 2.258 | 20 | 24 | fits | 34,498 | 17 | 0.659 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 298,647 | 3.733 | 20 | 24 | fits | 69,449 | 18 | 0.650 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 295,526 | 3.694 | 20 | 24 | fits | 81,996 | 17 | 0.657 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
