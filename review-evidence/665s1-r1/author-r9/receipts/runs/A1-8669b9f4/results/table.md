### 1x1

0 of 25 paths and 0 of 25 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.165 (2.943) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 2.499 (3.277) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.440 (3.217) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.423 (3.201) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.289 (3.067) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 2.292 (3.256) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.448 (2.224) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 2.833 (3.611) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.372 (3.150) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 2.340 (3.118) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.312 (3.090) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.442 (4.220) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 2.202 (2.980) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 2.204 (2.981) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.770 (3.548) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 2.698 (3.476) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 2.437 (3.215) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.371 (3.148) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 2.462 (3.239) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 2.464 (3.242) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.679 (3.456) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.741 (2.512) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 2.799 (4.182) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 2.125 (2.902) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 2.297 (3.259) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 87,061 | 1.741 | 10 | 24 | fits | 125,616 | 54 | 0.087 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 141,675 | 2.833 | 10 | 24 | fits | 180,557 | 126 | 0.053 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 118,598 | 2.372 | 10 | 24 | fits | 157,477 | 74 | 0.059 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 138,512 | 2.770 | 10 | 24 | fits | 177,391 | 91 | 0.065 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 123,090 | 2.462 | 10 | 24 | fits | 161,972 | 84 | 0.058 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 123,218 | 2.464 | 10 | 24 | fits | 162,100 | 84 | 0.058 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 133,925 | 2.679 | 10 | 24 | fits | 172,807 | 79 | 0.066 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 117,003 | 2.340 | 10 | 24 | fits | 155,885 | 69 | 0.060 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 115,607 | 2.312 | 10 | 24 | fits | 154,486 | 66 | 0.060 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 172,109 | 3.442 | 10 | 24 | fits | 210,988 | 167 | 0.055 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 110,119 | 2.202 | 10 | 24 | fits | 148,998 | 53 | 0.062 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 110,183 | 2.204 | 10 | 24 | fits | 149,062 | 53 | 0.062 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 134,915 | 2.698 | 10 | 24 | fits | 173,794 | 76 | 0.066 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 121,856 | 2.437 | 10 | 24 | fits | 160,735 | 76 | 0.058 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 118,537 | 2.371 | 10 | 24 | fits | 157,416 | 68 | 0.059 |
| get_configuration | `aecp.get_configuration.if0` | 121,981 | 2.440 | 10 | 24 | fits | 160,860 | 54 | 0.070 |
| entity_available | `aecp.entity_available.if0` | 108,270 | 2.165 | 10 | 24 | fits | 147,152 | 52 | 0.062 |
| get_name | `aecp.get_name.if0` | 114,449 | 2.289 | 10 | 24 | fits | 153,331 | 65 | 0.061 |
| get_counters | `aecp.get_counters.if0` | 121,167 | 2.423 | 10 | 24 | fits | 160,049 | 86 | 0.061 |
| get_avb_info | `aecp.get_avb_info.if0` | 124,962 | 2.499 | 10 | 24 | fits | 163,844 | 54 | 0.070 |
| unknown_command | `aecp.unknown_command.if0` | 106,236 | 2.125 | 10 | 24 | fits | 145,118 | 48 | 0.062 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 72,384 | 1.448 | 10 | 24 | fits | 111,209 | 52 | 0.079 |
| set_name | `aecp.set_name.if0` | 139,949 | 2.799 | 10 | 24 | fits | 209,113 | 127 | 0.063 |
| lock_entity | `aecp.lock_entity.if0` | 114,585 | 2.292 | 10 | 24 | fits | 162,809 | 77 | 0.064 |
| unlock_entity | `aecp.unlock_entity.if0` | 114,830 | 2.297 | 10 | 24 | fits | 162,929 | 78 | 0.064 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
