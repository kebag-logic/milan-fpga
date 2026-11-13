### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.171 (0.418) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.200 (0.463) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.110 (0.230) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.210 (0.468) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.130 (0.259) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.198 (0.307) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.166 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.239 (0.498) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.133 (0.389) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.193 (0.450) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.130 (0.248) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.209 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.122 (0.378) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.181 (0.437) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.109 (0.254) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.193 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.123 (0.255) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.186 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.131 (0.389) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.207 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.130 (0.254) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.215 (0.481) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.340 (0.625) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.194 (0.449) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.205 (0.451) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 109 | 0 | 65,963 (0.660) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 19,870 (0.199) | 1,750 (0.018) |

Longest pass that carries a step: 19,870 CPU cycles (0.199 ms), aecp; longest step: 1,750 (0.018 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,505 | 0.215 | 20 | 24 | fits | 25,294 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 23,936 | 0.239 | 20 | 24 | fits | 30,094 | 20 | 0.719 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 13,275 | 0.133 | 20 | 24 | fits | 25,207 | 20 | 0.722 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 10,916 | 0.109 | 20 | 24 | fits | 25,405 | 20 | 0.734 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,069 | 0.131 | 20 | 24 | fits | 25,355 | 20 | 0.712 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 20,663 | 0.207 | 20 | 24 | fits | 25,991 | 20 | 0.727 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 12,970 | 0.130 | 20 | 24 | fits | 25,386 | 20 | 0.735 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 19,308 | 0.193 | 20 | 24 | fits | 25,002 | 20 | 0.730 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,998 | 0.130 | 20 | 24 | fits | 24,781 | 20 | 0.745 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 20,939 | 0.209 | 20 | 24 | fits | 27,188 | 21 | 0.624 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 12,197 | 0.122 | 20 | 24 | fits | 24,241 | 20 | 0.761 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 18,140 | 0.181 | 20 | 24 | fits | 23,696 | 20 | 0.741 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 19,303 | 0.193 | 20 | 24 | fits | 25,117 | 20 | 0.736 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 12,326 | 0.123 | 20 | 24 | fits | 25,506 | 20 | 0.733 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 18,577 | 0.186 | 20 | 24 | fits | 24,593 | 20 | 0.729 |
| get_configuration | `aecp.get_configuration.if0` | 11,020 | 0.110 | 20 | 24 | fits | 23,049 | 20 | 0.762 |
| entity_available | `aecp.entity_available.if0` | 17,125 | 0.171 | 20 | 24 | fits | 21,850 | 20 | 0.711 |
| get_name | `aecp.get_name.if0` | 12,998 | 0.130 | 20 | 24 | fits | 25,900 | 20 | 0.766 |
| get_counters | `aecp.get_counters.if0` | 21,031 | 0.210 | 20 | 24 | fits | 26,792 | 20 | 0.734 |
| get_avb_info | `aecp.get_avb_info.if0` | 20,032 | 0.200 | 20 | 24 | fits | 26,353 | 20 | 0.794 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 19,447 | 0.194 | 20 | 24 | fits | 23,492 | 20 | 0.768 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 16,625 | 0.166 | 20 | 24 | fits | 22,074 | 20 | 0.724 |
| set_name | `aecp.set_name.if0` | 34,012 | 0.340 | 20 | 24 | fits | 41,819 | 42 | 0.751 |
| lock_entity | `aecp.lock_entity.if0` | 19,782 | 0.198 | 20 | 24 | fits | 30,671 | 33 | 0.759 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,518 | 0.205 | 20 | 24 | fits | 31,007 | 32 | 0.772 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
