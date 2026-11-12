### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.175 (0.407) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.123 (0.240) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.188 (0.432) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.168 (0.398) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.222 (0.480) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.212 (0.466) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.168 (0.417) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.145 (0.282) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.146 (0.386) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.149 (0.387) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.213 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.168 (0.407) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.099 (0.227) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.131 (0.373) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.110 (0.236) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.112 (0.236) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.183 (0.387) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.146 (0.402) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.147 (0.391) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.127 (0.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.208 (0.454) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.161 (0.407) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.280 (0.571) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.129 (0.364) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.281 (0.512) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 110 | 0 | 52,049 (0.520) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 17,980 (0.180) | 3,198 (0.032) |

Longest pass that carries a step: 17,980 CPU cycles (0.180 ms), aecp; longest step: 3,198 (0.032 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,116 | 0.161 | 20 | 24 | fits | 23,736 | 20 | 0.795 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 14,521 | 0.145 | 20 | 24 | fits | 28,235 | 20 | 0.737 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 14,619 | 0.146 | 20 | 24 | fits | 23,963 | 20 | 0.759 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 10,990 | 0.110 | 20 | 24 | fits | 23,625 | 20 | 0.753 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 14,654 | 0.147 | 20 | 24 | fits | 24,428 | 20 | 0.756 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 12,732 | 0.127 | 20 | 24 | fits | 24,557 | 20 | 0.760 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,806 | 0.208 | 20 | 24 | fits | 23,790 | 20 | 0.762 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 14,854 | 0.149 | 20 | 24 | fits | 23,870 | 20 | 0.771 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,334 | 0.213 | 20 | 24 | fits | 23,341 | 20 | 0.772 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 16,758 | 0.168 | 20 | 24 | fits | 25,985 | 21 | 0.675 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 9,898 | 0.099 | 20 | 24 | fits | 22,705 | 20 | 0.791 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 13,106 | 0.131 | 20 | 24 | fits | 22,686 | 20 | 0.790 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 11,232 | 0.112 | 20 | 24 | fits | 23,555 | 20 | 0.765 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,285 | 0.183 | 20 | 24 | fits | 24,410 | 20 | 0.762 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 14,560 | 0.146 | 20 | 24 | fits | 23,668 | 20 | 0.771 |
| get_configuration | `aecp.get_configuration.if0` | 18,812 | 0.188 | 20 | 24 | fits | 21,165 | 20 | 0.779 |
| entity_available | `aecp.entity_available.if0` | 17,467 | 0.175 | 20 | 24 | fits | 20,834 | 20 | 0.767 |
| get_name | `aecp.get_name.if0` | 22,157 | 0.222 | 20 | 24 | fits | 24,445 | 20 | 0.790 |
| get_counters | `aecp.get_counters.if0` | 16,787 | 0.168 | 20 | 24 | fits | 25,115 | 20 | 0.761 |
| get_avb_info | `aecp.get_avb_info.if0` | 12,336 | 0.123 | 20 | 24 | fits | 23,965 | 20 | 0.806 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 12,913 | 0.129 | 20 | 24 | fits | 21,246 | 20 | 0.777 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 16,837 | 0.168 | 20 | 24 | fits | 20,394 | 20 | 0.765 |
| set_name | `aecp.set_name.if0` | 27,955 | 0.280 | 20 | 24 | fits | 38,759 | 42 | 0.766 |
| lock_entity | `aecp.lock_entity.if0` | 21,162 | 0.212 | 20 | 24 | fits | 28,467 | 33 | 0.771 |
| unlock_entity | `aecp.unlock_entity.if0` | 28,050 | 0.281 | 20 | 24 | fits | 28,868 | 32 | 0.783 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
