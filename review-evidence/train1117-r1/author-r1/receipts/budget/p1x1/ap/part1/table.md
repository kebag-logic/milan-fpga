### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 31 paths and 0 of 31 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.209 (0.529) | fits | 0 aecp | 1 | 0 |
| get_as_path | 0 | `aecp.get_as_path.if0` (aecp) | 0.293 (0.616) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.186 (0.505) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.209 (0.529) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.252 (0.576) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.180 (0.499) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.213 (0.616) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.237 (0.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.267 (0.589) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.184 (0.502) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.178 (0.494) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.226 (0.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.255 (0.578) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.167 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.220 (0.542) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.228 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.173 (0.487) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.229 (0.551) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.174 (0.489) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.238 (0.561) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.182 (0.498) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.225 (0.546) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.158 (0.476) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.297 (0.734) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.207 (0.532) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.273 (0.631) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 3.430 (3.752) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 2.125 (2.501) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 3.792 (4.153) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 3.359 (3.715) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.477 (1.816) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 113 | 0 | 45,539 (0.455) | fits |
| aecp-largest-notice | 107 | 0 | 156,569 (1.566) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 80 | 23,362 (0.234) | 2,540 (0.025) |
| aecp-largest-notice | 78 | 23,362 (0.234) | 2,540 (0.025) |

Longest pass that carries a step: 23,362 CPU cycles (0.234 ms), aecp; longest step: 2,540 (0.025 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,834 | 0.158 | 20 | 24 | fits | 27,735 | 20 | 0.769 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 26,702 | 0.267 | 20 | 24 | fits | 30,956 | 20 | 0.689 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 18,389 | 0.184 | 20 | 24 | fits | 27,421 | 20 | 0.715 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 22,755 | 0.228 | 20 | 24 | fits | 27,115 | 20 | 0.705 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 23,798 | 0.238 | 20 | 24 | fits | 28,012 | 20 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,236 | 0.182 | 20 | 24 | fits | 27,261 | 20 | 0.707 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 22,473 | 0.225 | 20 | 24 | fits | 26,592 | 20 | 0.712 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 17,844 | 0.178 | 20 | 24 | fits | 26,864 | 20 | 0.726 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 22,595 | 0.226 | 20 | 24 | fits | 26,434 | 20 | 0.724 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,467 | 0.255 | 20 | 24 | fits | 35,337 | 27 | 0.662 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,713 | 0.167 | 20 | 24 | fits | 25,612 | 20 | 0.738 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 22,004 | 0.220 | 20 | 24 | fits | 25,983 | 20 | 0.743 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,261 | 0.173 | 20 | 24 | fits | 26,165 | 20 | 0.707 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 22,901 | 0.229 | 20 | 24 | fits | 27,125 | 20 | 0.719 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 17,385 | 0.174 | 20 | 24 | fits | 26,470 | 20 | 0.727 |
| get_configuration | `aecp.get_configuration.if0` | 20,926 | 0.209 | 20 | 24 | fits | 25,015 | 20 | 0.745 |
| entity_available | `aecp.entity_available.if0` | 20,925 | 0.209 | 20 | 24 | fits | 24,946 | 20 | 0.732 |
| get_name | `aecp.get_name.if0` | 18,042 | 0.180 | 20 | 24 | fits | 27,407 | 20 | 0.746 |
| get_counters | `aecp.get_counters.if0` | 25,152 | 0.252 | 20 | 24 | fits | 29,585 | 20 | 0.740 |
| get_avb_info | `aecp.get_avb_info.if0` | 18,563 | 0.186 | 20 | 24 | fits | 27,770 | 20 | 0.776 |
| get_as_path | `aecp.get_as_path.if0` | 29,309 | 0.293 | 20 | 24 | fits | 33,376 | 100 | 0.525 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 20,680 | 0.207 | 20 | 24 | fits | 25,746 | 20 | 0.761 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 23,665 | 0.237 | 20 | 24 | fits | 24,463 | 20 | 0.729 |
| set_name | `aecp.set_name.if0` | 29,729 | 0.297 | 20 | 24 | fits | 45,539 | 44 | 0.761 |
| lock_entity | `aecp.lock_entity.if0` | 21,327 | 0.213 | 20 | 24 | fits | 34,127 | 33 | 0.768 |
| unlock_entity | `aecp.unlock_entity.if0` | 27,306 | 0.273 | 20 | 24 | fits | 33,685 | 33 | 0.764 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 147,680 | 1.477 | 20 | 24 | fits | 156,569 | 137 | 0.324 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 343,049 | 3.430 | 20 | 24 | fits | 146,858 | 113 | 0.308 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 212,483 | 2.125 | 20 | 24 | fits | 41,594 | 18 | 0.679 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 379,160 | 3.792 | 20 | 24 | fits | 99,148 | 17 | 0.676 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 335,903 | 3.359 | 20 | 24 | fits | 101,136 | 17 | 0.684 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
