### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.166 (0.493) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.137 (0.465) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.167 (0.494) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.202 (0.534) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.127 (0.455) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.296 (0.585) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.105 (0.426) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.222 (0.554) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.127 (0.452) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.123 (0.447) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.183 (0.515) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.222 (0.575) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.122 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.181 (0.512) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.186 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.122 (0.448) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.187 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.128 (0.452) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.183 (0.514) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.133 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.181 (0.512) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.103 (0.276) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.312 (0.641) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.093 (0.256) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.232 (0.524) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 109 | 0 | 120,704 (1.207) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 24,649 (0.246) | 2,613 (0.026) |

Longest pass that carries a step: 24,649 CPU cycles (0.246 ms), aecp; longest step: 2,613 (0.026 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 10,304 | 0.103 | 20 | 24 | fits | 27,563 | 20 | 0.786 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 22,216 | 0.222 | 20 | 24 | fits | 30,776 | 20 | 0.694 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 12,749 | 0.127 | 20 | 24 | fits | 26,695 | 20 | 0.707 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 18,561 | 0.186 | 20 | 24 | fits | 27,171 | 20 | 0.719 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 18,322 | 0.183 | 20 | 24 | fits | 26,931 | 20 | 0.708 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 13,309 | 0.133 | 20 | 24 | fits | 27,413 | 20 | 0.700 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 18,149 | 0.181 | 20 | 24 | fits | 26,710 | 20 | 0.720 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 12,294 | 0.123 | 20 | 24 | fits | 26,289 | 20 | 0.711 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 18,342 | 0.183 | 20 | 24 | fits | 26,982 | 20 | 0.734 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 22,151 | 0.222 | 20 | 24 | fits | 39,048 | 30 | 0.629 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 12,249 | 0.122 | 20 | 24 | fits | 26,443 | 20 | 0.750 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 18,069 | 0.181 | 20 | 24 | fits | 26,385 | 20 | 0.755 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 12,244 | 0.122 | 20 | 24 | fits | 26,269 | 20 | 0.710 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 18,695 | 0.187 | 20 | 24 | fits | 27,321 | 20 | 0.720 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 12,802 | 0.128 | 20 | 24 | fits | 26,748 | 20 | 0.705 |
| get_configuration | `aecp.get_configuration.if0` | 16,697 | 0.167 | 20 | 24 | fits | 24,913 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if0` | 16,580 | 0.166 | 20 | 24 | fits | 24,850 | 20 | 0.728 |
| get_name | `aecp.get_name.if0` | 12,698 | 0.127 | 20 | 24 | fits | 27,049 | 20 | 0.745 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 20,190 | 0.202 | 20 | 24 | fits | 28,888 | 26 | 0.729 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 13,671 | 0.137 | 20 | 24 | fits | 28,118 | 28 | 0.749 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,256 | 0.093 | 20 | 24 | fits | 25,590 | 20 | 0.763 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 10,515 | 0.105 | 20 | 24 | fits | 24,057 | 20 | 0.709 |
| set_name | `aecp.set_name.if0` | 31,202 | 0.312 | 20 | 24 | fits | 45,357 | 41 | 0.745 |
| lock_entity | `aecp.lock_entity.if0` | 29,635 | 0.296 | 20 | 24 | fits | 32,924 | 32 | 0.767 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,235 | 0.232 | 20 | 24 | fits | 31,722 | 31 | 0.756 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
