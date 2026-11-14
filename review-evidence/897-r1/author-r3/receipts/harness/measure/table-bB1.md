### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.091 (0.234) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.119 (0.265) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.139 (0.428) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.173 (0.461) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.164 (0.458) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.158 (0.531) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.092 (0.236) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.229 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.114 (0.262) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.113 (0.261) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.155 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.137 (0.284) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.152 (0.442) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.148 (0.434) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.161 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.112 (0.260) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.167 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.112 (0.262) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.168 (0.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.119 (0.267) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.161 (0.452) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.253 (0.544) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.316 (0.698) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.143 (0.434) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.234 (0.573) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 112 | 0 | 43,740 (0.437) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 20,512 (0.205) | 1,943 (0.019) |

Longest pass that carries a step: 20,512 CPU cycles (0.205 ms), aecp; longest step: 1,943 (0.019 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 25,314 | 0.253 | 20 | 24 | fits | 27,438 | 20 | 0.790 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,944 | 0.229 | 20 | 24 | fits | 30,674 | 20 | 0.706 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,350 | 0.114 | 20 | 24 | fits | 26,248 | 20 | 0.720 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,131 | 0.161 | 20 | 24 | fits | 26,222 | 20 | 0.719 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 16,811 | 0.168 | 20 | 24 | fits | 27,196 | 20 | 0.726 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 11,869 | 0.119 | 20 | 24 | fits | 26,688 | 20 | 0.716 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 16,149 | 0.161 | 20 | 24 | fits | 25,936 | 20 | 0.724 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 11,262 | 0.113 | 20 | 24 | fits | 26,081 | 20 | 0.733 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 15,458 | 0.155 | 20 | 24 | fits | 25,475 | 20 | 0.737 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 13,717 | 0.137 | 20 | 24 | fits | 28,412 | 21 | 0.636 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 15,228 | 0.152 | 20 | 24 | fits | 25,087 | 20 | 0.755 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,772 | 0.148 | 20 | 24 | fits | 25,794 | 20 | 0.756 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 11,203 | 0.112 | 20 | 24 | fits | 25,977 | 20 | 0.723 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 16,676 | 0.167 | 20 | 24 | fits | 27,005 | 20 | 0.728 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 11,233 | 0.112 | 20 | 24 | fits | 26,213 | 20 | 0.733 |
| get_configuration | `aecp.get_configuration.if0` | 13,948 | 0.139 | 20 | 24 | fits | 23,919 | 20 | 0.750 |
| entity_available | `aecp.entity_available.if0` | 9,076 | 0.091 | 20 | 24 | fits | 23,352 | 20 | 0.726 |
| get_name | `aecp.get_name.if0` | 16,353 | 0.164 | 20 | 24 | fits | 26,796 | 20 | 0.757 |
| get_counters | `aecp.get_counters.if0` | 17,343 | 0.173 | 20 | 24 | fits | 28,564 | 20 | 0.746 |
| get_avb_info | `aecp.get_avb_info.if0` | 11,855 | 0.119 | 20 | 24 | fits | 26,508 | 20 | 0.774 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 14,312 | 0.143 | 20 | 24 | fits | 24,400 | 20 | 0.761 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 9,181 | 0.092 | 20 | 24 | fits | 23,596 | 20 | 0.733 |
| set_name | `aecp.set_name.if0` | 31,600 | 0.316 | 20 | 24 | fits | 43,740 | 42 | 0.760 |
| lock_entity | `aecp.lock_entity.if0` | 15,772 | 0.158 | 20 | 24 | fits | 33,520 | 34 | 0.759 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,398 | 0.234 | 20 | 24 | fits | 34,815 | 33 | 0.774 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
