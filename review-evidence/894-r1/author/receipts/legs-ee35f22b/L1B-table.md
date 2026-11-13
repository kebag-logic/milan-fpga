### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.106 (0.345) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.183 (0.437) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.159 (0.408) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.151 (0.393) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.181 (0.437) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.171 (0.446) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.159 (0.410) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.230 (0.486) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.126 (0.368) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.126 (0.369) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.173 (0.426) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.143 (0.386) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.169 (0.421) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.118 (0.360) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.176 (0.430) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.176 (0.431) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.130 (0.376) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.131 (0.390) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.131 (0.374) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.185 (0.439) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.178 (0.431) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.220 (0.487) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.264 (0.587) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.110 (0.354) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.233 (0.518) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 109 | 0 | 63,756 (0.638) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 20,493 (0.205) | 3,971 (0.040) |

Longest pass that carries a step: 20,493 CPU cycles (0.205 ms), aecp; longest step: 3,971 (0.040 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 21,985 | 0.220 | 20 | 24 | fits | 23,742 | 20 | 0.767 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 23,019 | 0.230 | 20 | 24 | fits | 27,795 | 20 | 0.690 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 12,580 | 0.126 | 20 | 24 | fits | 21,981 | 20 | 0.693 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 17,603 | 0.176 | 20 | 24 | fits | 22,373 | 20 | 0.693 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 13,052 | 0.131 | 20 | 24 | fits | 22,443 | 20 | 0.682 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 18,516 | 0.185 | 20 | 24 | fits | 23,187 | 20 | 0.699 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 17,779 | 0.178 | 20 | 24 | fits | 22,235 | 20 | 0.697 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 12,595 | 0.126 | 20 | 24 | fits | 21,947 | 20 | 0.703 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 17,296 | 0.173 | 20 | 24 | fits | 21,772 | 20 | 0.711 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 14,338 | 0.143 | 20 | 24 | fits | 23,598 | 21 | 0.595 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 16,898 | 0.169 | 20 | 24 | fits | 21,472 | 20 | 0.729 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 11,838 | 0.118 | 20 | 24 | fits | 21,100 | 20 | 0.717 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,639 | 0.176 | 20 | 24 | fits | 22,486 | 20 | 0.704 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 13,022 | 0.130 | 20 | 24 | fits | 22,605 | 20 | 0.691 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 13,109 | 0.131 | 20 | 24 | fits | 22,747 | 20 | 0.717 |
| get_configuration | `aecp.get_configuration.if0` | 15,889 | 0.159 | 20 | 24 | fits | 20,140 | 20 | 0.715 |
| entity_available | `aecp.entity_available.if0` | 10,639 | 0.106 | 20 | 24 | fits | 19,556 | 20 | 0.698 |
| get_name | `aecp.get_name.if0` | 18,142 | 0.181 | 20 | 24 | fits | 22,982 | 20 | 0.735 |
| get_counters | `aecp.get_counters.if0` | 15,094 | 0.151 | 20 | 24 | fits | 24,354 | 20 | 0.717 |
| get_avb_info | `aecp.get_avb_info.if0` | 18,258 | 0.183 | 20 | 24 | fits | 22,905 | 20 | 0.756 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 10,973 | 0.110 | 20 | 24 | fits | 20,254 | 20 | 0.719 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 15,902 | 0.159 | 20 | 24 | fits | 20,307 | 20 | 0.719 |
| set_name | `aecp.set_name.if0` | 26,360 | 0.264 | 20 | 24 | fits | 38,322 | 43 | 0.736 |
| lock_entity | `aecp.lock_entity.if0` | 17,093 | 0.171 | 20 | 24 | fits | 29,558 | 34 | 0.753 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,308 | 0.233 | 20 | 24 | fits | 29,551 | 33 | 0.753 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
