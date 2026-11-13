### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.101 (0.228) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.135 (0.261) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.167 (0.430) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.142 (0.272) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.192 (0.456) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.188 (0.301) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.091 (0.227) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.227 (0.504) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.129 (0.259) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.124 (0.256) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.187 (0.449) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.148 (0.277) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.173 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.116 (0.243) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.184 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.129 (0.253) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.191 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.117 (0.255) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.133 (0.259) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.128 (0.266) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.191 (0.457) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.160 (0.428) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.264 (0.421) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.172 (0.437) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.266 (0.516) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 109 | 0 | 67,077 (0.671) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 19,387 (0.194) | 2,405 (0.024) |

Longest pass that carries a step: 19,387 CPU cycles (0.194 ms), aecp; longest step: 2,405 (0.024 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,000 | 0.160 | 20 | 24 | fits | 25,768 | 20 | 0.780 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,712 | 0.227 | 20 | 24 | fits | 30,575 | 20 | 0.722 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 12,926 | 0.129 | 20 | 24 | fits | 25,878 | 20 | 0.732 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,422 | 0.184 | 20 | 24 | fits | 25,921 | 20 | 0.738 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,288 | 0.133 | 20 | 24 | fits | 25,874 | 20 | 0.721 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 12,836 | 0.128 | 20 | 24 | fits | 26,596 | 20 | 0.738 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 19,098 | 0.191 | 20 | 24 | fits | 25,994 | 20 | 0.744 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 12,381 | 0.124 | 20 | 24 | fits | 25,608 | 20 | 0.744 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 18,718 | 0.187 | 20 | 24 | fits | 25,261 | 20 | 0.751 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 14,829 | 0.148 | 20 | 24 | fits | 27,705 | 21 | 0.643 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 17,329 | 0.173 | 20 | 24 | fits | 24,737 | 20 | 0.769 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 11,565 | 0.116 | 20 | 24 | fits | 24,336 | 20 | 0.757 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 12,858 | 0.129 | 20 | 24 | fits | 25,312 | 20 | 0.736 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 19,113 | 0.191 | 20 | 24 | fits | 26,263 | 20 | 0.744 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 11,724 | 0.117 | 20 | 24 | fits | 25,458 | 20 | 0.745 |
| get_configuration | `aecp.get_configuration.if0` | 16,721 | 0.167 | 20 | 24 | fits | 23,510 | 20 | 0.766 |
| entity_available | `aecp.entity_available.if0` | 10,121 | 0.101 | 20 | 24 | fits | 22,839 | 20 | 0.736 |
| get_name | `aecp.get_name.if0` | 19,179 | 0.192 | 20 | 24 | fits | 26,035 | 20 | 0.766 |
| get_counters | `aecp.get_counters.if0` | 14,196 | 0.142 | 20 | 24 | fits | 27,241 | 20 | 0.744 |
| get_avb_info | `aecp.get_avb_info.if0` | 13,466 | 0.135 | 20 | 24 | fits | 26,086 | 20 | 0.789 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,234 | 0.172 | 20 | 24 | fits | 23,831 | 20 | 0.775 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,148 | 0.091 | 20 | 24 | fits | 22,730 | 20 | 0.741 |
| set_name | `aecp.set_name.if0` | 26,398 | 0.264 | 20 | 24 | fits | 42,126 | 42 | 0.746 |
| lock_entity | `aecp.lock_entity.if0` | 18,840 | 0.188 | 20 | 24 | fits | 30,105 | 33 | 0.748 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,615 | 0.266 | 20 | 24 | fits | 30,456 | 32 | 0.760 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
