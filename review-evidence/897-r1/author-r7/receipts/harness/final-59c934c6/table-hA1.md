### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 26 paths and 0 of 26 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.208 (0.511) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.166 (0.482) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.220 (0.529) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.103 (0.415) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.136 (0.451) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.126 (0.442) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.277 (0.650) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.114 (0.425) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.219 (0.540) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.129 (0.444) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.126 (0.437) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.164 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.148 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.162 (0.478) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.152 (0.443) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.171 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.229 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.129 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.231 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.131 (0.442) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.135 (0.453) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.170 (0.485) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.231 (0.539) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.179 (0.443) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.169 (0.330) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.207 (0.574) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 113 | 0 | 44,267 (0.443) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 80 | 22,503 (0.225) | 2,520 (0.025) |

Longest pass that carries a step: 22,503 CPU cycles (0.225 ms), aecp; longest step: 2,520 (0.025 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 23,141 | 0.231 | 20 | 24 | fits | 27,308 | 20 | 0.760 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 21,860 | 0.219 | 20 | 24 | fits | 32,156 | 20 | 0.710 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 12,895 | 0.129 | 20 | 24 | fits | 27,010 | 20 | 0.717 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,094 | 0.171 | 20 | 24 | fits | 27,232 | 20 | 0.720 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,059 | 0.131 | 20 | 24 | fits | 27,108 | 20 | 0.713 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 13,523 | 0.135 | 20 | 24 | fits | 27,573 | 20 | 0.725 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 16,992 | 0.170 | 20 | 24 | fits | 26,410 | 20 | 0.719 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 12,602 | 0.126 | 20 | 24 | fits | 26,572 | 20 | 0.729 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,432 | 0.164 | 20 | 24 | fits | 26,175 | 20 | 0.736 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 14,808 | 0.148 | 20 | 24 | fits | 28,692 | 21 | 0.625 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,235 | 0.162 | 20 | 24 | fits | 25,762 | 20 | 0.753 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 15,248 | 0.152 | 20 | 24 | fits | 26,218 | 20 | 0.755 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 22,932 | 0.229 | 20 | 24 | fits | 26,163 | 20 | 0.711 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,909 | 0.129 | 20 | 24 | fits | 27,203 | 20 | 0.724 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 23,083 | 0.231 | 20 | 24 | fits | 26,478 | 20 | 0.726 |
| get_configuration | `aecp.get_configuration.if0` | 10,314 | 0.103 | 20 | 24 | fits | 24,166 | 20 | 0.738 |
| entity_available | `aecp.entity_available.if0` | 20,783 | 0.208 | 20 | 24 | fits | 23,441 | 20 | 0.701 |
| get_name | `aecp.get_name.if0` | 12,604 | 0.126 | 20 | 24 | fits | 26,862 | 20 | 0.736 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 13,624 | 0.136 | 20 | 24 | fits | 27,724 | 27 | 0.714 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 21,951 | 0.220 | 20 | 24 | fits | 27,739 | 29 | 0.740 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 16,561 | 0.166 | 20 | 24 | fits | 27,878 | 29 | 0.755 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 16,892 | 0.169 | 20 | 24 | fits | 32,978 | 35 | 0.728 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 11,400 | 0.114 | 20 | 24 | fits | 23,850 | 20 | 0.721 |
| set_name | `aecp.set_name.if0` | 17,928 | 0.179 | 20 | 24 | fits | 44,267 | 43 | 0.753 |
| lock_entity | `aecp.lock_entity.if0` | 27,685 | 0.277 | 20 | 24 | fits | 35,664 | 34 | 0.776 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,729 | 0.207 | 20 | 24 | fits | 36,909 | 33 | 0.785 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
