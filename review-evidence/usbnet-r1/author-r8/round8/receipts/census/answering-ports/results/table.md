### arty-1x1

Clock: CPU 80 MHz on sys, the product's split CPU clock, bus 80 MHz.

0 of 48 paths and 0 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.136 (0.374) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.241 (0.478) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.135 (0.383) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.107 (0.352) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.191 (0.437) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.135 (0.380) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.170 (0.543) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.105 (0.352) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.204 (0.448) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.140 (0.389) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.127 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.163 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.188 (0.436) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.155 (0.396) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.119 (0.366) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (156 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.169 (0.412) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i15.c0.if0` (aecp) | 0.163 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t23.i0.c0.if0` (aecp) | 0.129 (0.376) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.169 (0.411) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.160 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.142 (0.390) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i0.c0.if0` (aecp) | 0.165 (0.409) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.157 (0.378) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.181 (0.421) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.245 (0.615) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.108 (0.354) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.235 (0.534) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 3.634 (3.968) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.865 (1.048) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.476 (0.719) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.641 (0.943) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.511 (0.792) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.578 (0.881) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.435 (0.692) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.507 (0.816) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 4.207 (4.516) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 4.426 (4.709) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.431 (0.700) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 4.088 (4.358) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 3.103 (3.427) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 4.738 (5.064) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 4.630 (4.954) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.766 (2.041) | fits | 0 aecp | 1 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.414 (0.631) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.141 (0.450) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.193 (0.499) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.146 (0.453) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.160 (0.461) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 160,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 116 | 0 | 58,529 (0.732) | fits |
| aecp | 112 | 0 | 55,635 (0.695) | fits |
| aecp-reboot | 106 | 0 | 55,635 (0.695) | fits |
| aecp-largest-notice | 106 | 0 | 130,521 (1.632) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 82 | 15,784 (0.197) | 2,110 (0.026) |
| aecp | 80 | 15,784 (0.197) | 2,110 (0.026) |
| aecp-reboot | 78 | 15,784 (0.197) | 2,110 (0.026) |
| aecp-largest-notice | 78 | 15,784 (0.197) | 2,110 (0.026) |

Longest pass that carries a step: 15,784 CPU cycles (0.197 ms), aecp-fanout; longest step: 2,110 (0.026 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 40,563 | 0.507 | 20 | 24 | fits | 50,658 | 89 | 0.560 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 40,845 | 0.511 | 20 | 24 | fits | 46,273 | 79 | 0.593 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 34,523 | 0.432 | 20 | 24 | fits | 39,525 | 78 | 0.529 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 34,803 | 0.435 | 20 | 24 | fits | 39,886 | 79 | 0.536 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,265 | 0.641 | 20 | 24 | fits | 58,529 | 109 | 0.589 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 290,688 | 3.634 | 20 | 24 | fits | 53,788 | 110 | 0.576 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 336,554 | 4.207 | 20 | 24 | fits | 43,872 | 66 | 0.588 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 46,258 | 0.578 | 20 | 24 | fits | 53,951 | 78 | 0.601 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 354,106 | 4.426 | 20 | 24 | fits | 51,036 | 77 | 0.603 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 38,101 | 0.476 | 20 | 24 | fits | 40,253 | 79 | 0.546 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 34,462 | 0.431 | 20 | 24 | fits | 38,499 | 78 | 0.514 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 69,200 | 0.865 | 20 | 24 | fits | 34,717 | 59 | 0.504 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,514 | 0.181 | 20 | 24 | fits | 20,922 | 20 | 0.752 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 16,296 | 0.204 | 20 | 24 | fits | 23,917 | 20 | 0.672 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,207 | 0.140 | 20 | 24 | fits | 20,824 | 20 | 0.702 |
| READ_DESCRIPTOR (156 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 13,538 | 0.169 | 20 | 24 | fits | 20,618 | 20 | 0.688 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 11,335 | 0.142 | 20 | 24 | fits | 20,972 | 20 | 0.695 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i0.c0.if0` | 13,204 | 0.165 | 20 | 24 | fits | 20,231 | 20 | 0.697 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,530 | 0.157 | 20 | 24 | fits | 20,522 | 20 | 0.700 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 10,199 | 0.127 | 20 | 24 | fits | 19,662 | 20 | 0.712 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 13,041 | 0.163 | 20 | 24 | fits | 20,062 | 20 | 0.720 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 15,071 | 0.188 | 20 | 24 | fits | 24,629 | 21 | 0.615 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 12,431 | 0.155 | 20 | 24 | fits | 19,368 | 20 | 0.735 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,546 | 0.119 | 20 | 24 | fits | 19,025 | 20 | 0.729 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i15.c0.if0` | 13,015 | 0.163 | 20 | 24 | fits | 20,189 | 20 | 0.709 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t23.i0.c0.if0` | 10,315 | 0.129 | 20 | 24 | fits | 19,794 | 20 | 0.714 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 13,535 | 0.169 | 20 | 24 | fits | 20,709 | 20 | 0.706 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 12,798 | 0.160 | 20 | 24 | fits | 19,986 | 20 | 0.718 |
| get_configuration | `aecp.get_configuration.if0` | 8,594 | 0.107 | 20 | 24 | fits | 17,865 | 20 | 0.711 |
| entity_available | `aecp.entity_available.if0` | 10,893 | 0.136 | 20 | 24 | fits | 17,817 | 20 | 0.707 |
| get_name | `aecp.get_name.if0` | 10,810 | 0.135 | 20 | 24 | fits | 20,324 | 20 | 0.734 |
| get_counters | `aecp.get_counters.if0` | 15,302 | 0.191 | 20 | 24 | fits | 22,271 | 20 | 0.714 |
| get_avb_info | `aecp.get_avb_info.if0` | 10,810 | 0.135 | 20 | 24 | fits | 20,384 | 20 | 0.761 |
| get_as_path | `aecp.get_as_path.if0` | 19,307 | 0.241 | 20 | 24 | fits | 25,371 | 100 | 0.510 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 8,665 | 0.108 | 20 | 24 | fits | 18,089 | 20 | 0.725 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 8,434 | 0.105 | 20 | 24 | fits | 17,583 | 20 | 0.716 |
| set_name | `aecp.set_name.if0` | 19,634 | 0.245 | 20 | 24 | fits | 37,435 | 44 | 0.751 |
| lock_entity | `aecp.lock_entity.if0` | 13,579 | 0.170 | 20 | 24 | fits | 27,009 | 33 | 0.761 |
| unlock_entity | `aecp.unlock_entity.if0` | 18,765 | 0.235 | 20 | 24 | fits | 27,800 | 33 | 0.775 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 11,711 | 0.146 | 20 | 24 | fits | 21,619 | 17 | 0.745 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 12,773 | 0.160 | 20 | 24 | fits | 21,104 | 17 | 0.735 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 11,268 | 0.141 | 20 | 24 | fits | 21,143 | 17 | 0.737 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 15,440 | 0.193 | 20 | 24 | fits | 22,008 | 17 | 0.765 |
| REBOOT | `aecp_reboot.accepted.if0` | 33,149 | 0.414 | 20 | 24 | fits | 33,542 | 66 | 0.493 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 141,245 | 1.766 | 20 | 24 | fits | 18,572 | 12 | 0.615 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 327,025 | 4.088 | 20 | 24 | fits | 17,806 | 12 | 0.573 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 248,241 | 3.103 | 20 | 24 | fits | 34,916 | 17 | 0.663 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 379,036 | 4.738 | 20 | 24 | fits | 70,163 | 17 | 0.662 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 370,378 | 4.630 | 20 | 24 | fits | 82,788 | 18 | 0.663 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
