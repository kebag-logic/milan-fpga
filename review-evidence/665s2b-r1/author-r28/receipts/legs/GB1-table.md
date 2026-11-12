### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.126 (0.338) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.211 (0.431) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.182 (0.396) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.179 (0.385) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.207 (0.430) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.232 (0.431) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.180 (0.402) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.243 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.154 (0.367) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.158 (0.367) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.197 (0.418) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.173 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.190 (0.416) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.144 (0.355) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.199 (0.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.199 (0.415) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.153 (0.370) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.156 (0.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.159 (0.372) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.213 (0.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.105 (0.225) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.217 (0.439) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.317 (0.556) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.136 (0.346) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.194 (0.292) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 110 | 0 | 63,670 (0.637) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 18,666 (0.187) | 3,382 (0.034) |

Longest pass that carries a step: 18,666 CPU cycles (0.187 ms), aecp; longest step: 3,382 (0.034 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,746 | 0.217 | 20 | 24 | fits | 22,576 | 20 | 0.764 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 24,286 | 0.243 | 20 | 24 | fits | 27,254 | 20 | 0.706 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 15,401 | 0.154 | 20 | 24 | fits | 22,227 | 20 | 0.715 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 19,895 | 0.199 | 20 | 24 | fits | 22,470 | 20 | 0.718 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 15,922 | 0.159 | 20 | 24 | fits | 22,831 | 20 | 0.711 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 21,292 | 0.213 | 20 | 24 | fits | 23,144 | 20 | 0.720 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 10,514 | 0.105 | 20 | 24 | fits | 22,481 | 20 | 0.722 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 15,849 | 0.158 | 20 | 24 | fits | 22,122 | 20 | 0.722 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 19,723 | 0.197 | 20 | 24 | fits | 22,088 | 20 | 0.738 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 17,314 | 0.173 | 20 | 24 | fits | 24,053 | 21 | 0.622 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 18,996 | 0.190 | 20 | 24 | fits | 21,510 | 20 | 0.755 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,354 | 0.144 | 20 | 24 | fits | 21,068 | 20 | 0.740 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 19,901 | 0.199 | 20 | 24 | fits | 22,171 | 20 | 0.722 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,303 | 0.153 | 20 | 24 | fits | 22,451 | 20 | 0.715 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,590 | 0.156 | 20 | 24 | fits | 22,732 | 20 | 0.744 |
| get_configuration | `aecp.get_configuration.if0` | 18,171 | 0.182 | 20 | 24 | fits | 19,922 | 20 | 0.738 |
| entity_available | `aecp.entity_available.if0` | 12,597 | 0.126 | 20 | 24 | fits | 19,400 | 20 | 0.712 |
| get_name | `aecp.get_name.if0` | 20,722 | 0.207 | 20 | 24 | fits | 23,257 | 20 | 0.766 |
| get_counters | `aecp.get_counters.if0` | 17,894 | 0.179 | 20 | 24 | fits | 24,096 | 20 | 0.718 |
| get_avb_info | `aecp.get_avb_info.if0` | 21,150 | 0.211 | 20 | 24 | fits | 23,364 | 20 | 0.776 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,618 | 0.136 | 20 | 24 | fits | 20,090 | 20 | 0.736 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 18,005 | 0.180 | 20 | 24 | fits | 19,758 | 20 | 0.734 |
| set_name | `aecp.set_name.if0` | 31,666 | 0.317 | 20 | 24 | fits | 36,259 | 42 | 0.733 |
| lock_entity | `aecp.lock_entity.if0` | 23,213 | 0.232 | 20 | 24 | fits | 29,081 | 33 | 0.763 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,419 | 0.194 | 20 | 24 | fits | 29,209 | 32 | 0.773 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
