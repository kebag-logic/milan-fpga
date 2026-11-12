### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.158 (0.372) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.182 (0.420) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.128 (0.352) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.191 (0.416) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.162 (0.394) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.251 (0.487) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.120 (0.347) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.238 (0.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.177 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.176 (0.402) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.150 (0.386) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.207 (0.420) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.169 (0.393) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.171 (0.388) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.177 (0.414) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.189 (0.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.134 (0.361) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.180 (0.399) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.189 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.152 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.142 (0.372) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.210 (0.445) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.332 (0.558) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.164 (0.374) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.254 (0.471) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 110 | 0 | 61,240 (0.612) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 18,124 (0.181) | 3,295 (0.033) |

Longest pass that carries a step: 18,124 CPU cycles (0.181 ms), aecp; longest step: 3,295 (0.033 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,014 | 0.210 | 20 | 24 | fits | 23,608 | 20 | 0.779 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 23,765 | 0.238 | 20 | 24 | fits | 27,687 | 20 | 0.712 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 17,700 | 0.177 | 20 | 24 | fits | 23,324 | 20 | 0.720 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,716 | 0.177 | 20 | 24 | fits | 23,275 | 20 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 18,946 | 0.189 | 20 | 24 | fits | 23,458 | 20 | 0.712 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 15,175 | 0.152 | 20 | 24 | fits | 23,981 | 20 | 0.731 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,162 | 0.142 | 20 | 24 | fits | 23,198 | 20 | 0.732 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 17,559 | 0.176 | 20 | 24 | fits | 23,189 | 20 | 0.736 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,992 | 0.150 | 20 | 24 | fits | 22,894 | 20 | 0.747 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 20,683 | 0.207 | 20 | 24 | fits | 24,998 | 21 | 0.624 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,937 | 0.169 | 20 | 24 | fits | 21,899 | 20 | 0.758 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 17,111 | 0.171 | 20 | 24 | fits | 21,706 | 20 | 0.745 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 18,936 | 0.189 | 20 | 24 | fits | 22,636 | 20 | 0.731 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 13,378 | 0.134 | 20 | 24 | fits | 23,301 | 20 | 0.730 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,036 | 0.180 | 20 | 24 | fits | 22,876 | 20 | 0.734 |
| get_configuration | `aecp.get_configuration.if0` | 12,811 | 0.128 | 20 | 24 | fits | 20,651 | 20 | 0.752 |
| entity_available | `aecp.entity_available.if0` | 15,758 | 0.158 | 20 | 24 | fits | 20,243 | 20 | 0.722 |
| get_name | `aecp.get_name.if0` | 16,220 | 0.162 | 20 | 24 | fits | 23,372 | 20 | 0.762 |
| get_counters | `aecp.get_counters.if0` | 19,119 | 0.191 | 20 | 24 | fits | 24,519 | 20 | 0.734 |
| get_avb_info | `aecp.get_avb_info.if0` | 18,200 | 0.182 | 20 | 24 | fits | 23,545 | 20 | 0.789 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 16,436 | 0.164 | 20 | 24 | fits | 20,430 | 20 | 0.748 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 12,005 | 0.120 | 20 | 24 | fits | 20,288 | 20 | 0.741 |
| set_name | `aecp.set_name.if0` | 33,188 | 0.332 | 20 | 24 | fits | 38,231 | 42 | 0.750 |
| lock_entity | `aecp.lock_entity.if0` | 25,129 | 0.251 | 20 | 24 | fits | 28,681 | 33 | 0.758 |
| unlock_entity | `aecp.unlock_entity.if0` | 25,436 | 0.254 | 20 | 24 | fits | 29,155 | 32 | 0.770 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
