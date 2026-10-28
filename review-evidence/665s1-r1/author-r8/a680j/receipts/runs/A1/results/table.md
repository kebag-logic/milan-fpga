### 1x1

0 of 25 paths and 0 of 25 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 3.991 (5.136) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 4.016 (5.162) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 3.919 (5.064) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 4.964 (6.109) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 4.191 (5.337) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 4.168 (5.627) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 2.512 (3.658) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 5.161 (6.306) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 4.349 (5.495) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 4.283 (5.428) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 4.233 (5.378) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 6.233 (7.379) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 4.036 (5.181) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 4.038 (5.184) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 4.508 (5.654) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 4.896 (6.041) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 4.989 (6.135) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 4.340 (5.485) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 4.502 (5.648) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 5.043 (6.188) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 4.346 (5.492) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 2.492 (3.628) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.969 (7.198) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 3.916 (5.061) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 4.160 (5.618) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 124,622 | 2.492 | 10 | 24 | fits | 181,419 | 47 | 0.879 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 258,032 | 5.161 | 10 | 24 | fits | 315,306 | 125 | 0.886 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 217,470 | 4.349 | 10 | 24 | fits | 274,740 | 74 | 0.885 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 225,425 | 4.508 | 10 | 24 | fits | 282,695 | 84 | 0.885 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 225,124 | 4.502 | 10 | 24 | fits | 282,398 | 83 | 0.885 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 252,132 | 5.043 | 10 | 24 | fits | 309,406 | 90 | 0.887 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 217,316 | 4.346 | 10 | 24 | fits | 274,590 | 73 | 0.885 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 214,139 | 4.283 | 10 | 24 | fits | 271,413 | 68 | 0.885 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 211,655 | 4.233 | 10 | 24 | fits | 268,925 | 65 | 0.885 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 311,673 | 6.233 | 10 | 24 | fits | 368,943 | 167 | 0.888 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 201,801 | 4.036 | 10 | 24 | fits | 259,071 | 52 | 0.884 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 201,905 | 4.038 | 10 | 24 | fits | 259,175 | 52 | 0.884 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 244,780 | 4.896 | 10 | 24 | fits | 302,050 | 76 | 0.886 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 249,460 | 4.989 | 10 | 24 | fits | 306,730 | 82 | 0.887 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 216,982 | 4.340 | 10 | 24 | fits | 274,252 | 68 | 0.884 |
| get_configuration | `aecp.get_configuration.if0` | 195,950 | 3.919 | 10 | 24 | fits | 253,220 | 47 | 0.885 |
| entity_available | `aecp.entity_available.if0` | 199,533 | 3.991 | 10 | 24 | fits | 256,807 | 51 | 0.885 |
| get_name | `aecp.get_name.if0` | 209,569 | 4.191 | 10 | 24 | fits | 266,843 | 64 | 0.885 |
| get_counters | `aecp.get_counters.if0` | 248,194 | 4.964 | 10 | 24 | fits | 305,468 | 92 | 0.888 |
| get_avb_info | `aecp.get_avb_info.if0` | 200,805 | 4.016 | 10 | 24 | fits | 258,079 | 48 | 0.884 |
| unknown_command | `aecp.unknown_command.if0` | 195,777 | 3.916 | 10 | 24 | fits | 253,051 | 47 | 0.885 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 125,604 | 2.512 | 10 | 24 | fits | 182,878 | 51 | 0.879 |
| set_name | `aecp.set_name.if0` | 248,464 | 4.969 | 10 | 24 | fits | 359,918 | 127 | 0.880 |
| lock_entity | `aecp.lock_entity.if0` | 208,381 | 4.168 | 10 | 24 | fits | 281,333 | 78 | 0.882 |
| unlock_entity | `aecp.unlock_entity.if0` | 208,002 | 4.160 | 10 | 24 | fits | 280,915 | 77 | 0.883 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
