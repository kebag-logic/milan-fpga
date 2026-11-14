### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.092 (0.240) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.129 (0.438) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.140 (0.445) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.178 (0.487) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.163 (0.475) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.167 (0.561) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.101 (0.404) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.198 (0.513) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.119 (0.277) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.115 (0.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.157 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.137 (0.292) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.156 (0.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.142 (0.443) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.164 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.116 (0.271) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.168 (0.480) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.115 (0.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.121 (0.278) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.126 (0.283) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.164 (0.474) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.160 (0.466) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.240 (0.653) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.225 (0.534) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.259 (0.626) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 112 | 0 | 44,599 (0.446) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 21,003 (0.210) | 2,214 (0.022) |

Longest pass that carries a step: 21,003 CPU cycles (0.210 ms), aecp; longest step: 2,214 (0.022 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,971 | 0.160 | 20 | 24 | fits | 27,692 | 20 | 0.793 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,768 | 0.198 | 20 | 24 | fits | 31,979 | 20 | 0.742 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,893 | 0.119 | 20 | 24 | fits | 27,692 | 20 | 0.762 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,395 | 0.164 | 20 | 24 | fits | 27,825 | 20 | 0.758 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 12,079 | 0.121 | 20 | 24 | fits | 27,799 | 20 | 0.753 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 12,627 | 0.126 | 20 | 24 | fits | 28,344 | 20 | 0.763 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 16,412 | 0.164 | 20 | 24 | fits | 27,276 | 20 | 0.762 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 11,548 | 0.115 | 20 | 24 | fits | 27,189 | 20 | 0.770 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 15,720 | 0.157 | 20 | 24 | fits | 26,755 | 20 | 0.775 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 13,713 | 0.137 | 20 | 24 | fits | 29,161 | 21 | 0.670 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 15,639 | 0.156 | 20 | 24 | fits | 26,559 | 20 | 0.791 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,225 | 0.142 | 20 | 24 | fits | 26,673 | 20 | 0.787 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 11,646 | 0.116 | 20 | 24 | fits | 27,096 | 20 | 0.758 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 16,779 | 0.168 | 20 | 24 | fits | 28,196 | 20 | 0.766 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 11,516 | 0.115 | 20 | 24 | fits | 27,223 | 20 | 0.768 |
| get_configuration | `aecp.get_configuration.if0` | 13,959 | 0.140 | 20 | 24 | fits | 24,696 | 20 | 0.775 |
| entity_available | `aecp.entity_available.if0` | 9,151 | 0.092 | 20 | 24 | fits | 24,010 | 20 | 0.750 |
| get_name | `aecp.get_name.if0` | 16,322 | 0.163 | 20 | 24 | fits | 27,721 | 20 | 0.783 |
| get_counters | `aecp.get_counters.if0` | 17,827 | 0.178 | 20 | 24 | fits | 29,092 | 20 | 0.768 |
| get_avb_info | `aecp.get_avb_info.if0` | 12,884 | 0.129 | 20 | 24 | fits | 27,185 | 20 | 0.797 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 22,458 | 0.225 | 20 | 24 | fits | 24,734 | 20 | 0.780 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 10,052 | 0.101 | 20 | 24 | fits | 23,775 | 20 | 0.748 |
| set_name | `aecp.set_name.if0` | 23,972 | 0.240 | 20 | 24 | fits | 44,599 | 43 | 0.780 |
| lock_entity | `aecp.lock_entity.if0` | 16,716 | 0.167 | 20 | 24 | fits | 36,055 | 34 | 0.795 |
| unlock_entity | `aecp.unlock_entity.if0` | 25,882 | 0.259 | 20 | 24 | fits | 36,936 | 33 | 0.792 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
