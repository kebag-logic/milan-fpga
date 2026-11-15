### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 26 paths and 0 of 26 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.212 (0.501) | fits | 0 aecp | 1 | 0 |
| get_as_path, refused ENTITY_MISBEHAVING | 0 | `aecp.get_as_path.if0` (aecp) | 0.153 (0.449) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.251 (0.546) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.129 (0.421) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.159 (0.455) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.237 (0.536) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.271 (0.659) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.208 (0.495) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.190 (0.488) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.233 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.235 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.144 (0.440) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.258 (0.550) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.142 (0.436) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.142 (0.437) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.149 (0.446) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.233 (0.526) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.155 (0.454) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.234 (0.528) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.146 (0.450) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.241 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.150 (0.443) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.128 (0.419) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.229 (0.623) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.217 (0.507) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.197 (0.533) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 114 | 0 | 44,778 (0.448) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 80 | 20,719 (0.207) | 3,396 (0.034) |

Longest pass that carries a step: 20,719 CPU cycles (0.207 ms), aecp; longest step: 3,396 (0.034 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 12,785 | 0.128 | 20 | 24 | fits | 26,862 | 20 | 0.789 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,004 | 0.190 | 20 | 24 | fits | 30,813 | 20 | 0.727 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 23,349 | 0.233 | 20 | 24 | fits | 26,332 | 20 | 0.743 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,888 | 0.149 | 20 | 24 | fits | 26,537 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 14,585 | 0.146 | 20 | 24 | fits | 27,325 | 20 | 0.740 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 24,141 | 0.241 | 20 | 24 | fits | 26,971 | 20 | 0.743 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,964 | 0.150 | 20 | 24 | fits | 26,015 | 20 | 0.744 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 23,502 | 0.235 | 20 | 24 | fits | 26,409 | 20 | 0.756 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,434 | 0.144 | 20 | 24 | fits | 25,782 | 20 | 0.757 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,760 | 0.258 | 20 | 24 | fits | 28,543 | 21 | 0.662 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,152 | 0.142 | 20 | 24 | fits | 25,359 | 20 | 0.773 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 14,211 | 0.142 | 20 | 24 | fits | 25,746 | 20 | 0.775 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 23,334 | 0.233 | 20 | 24 | fits | 26,155 | 20 | 0.743 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,521 | 0.155 | 20 | 24 | fits | 27,256 | 20 | 0.749 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 23,393 | 0.234 | 20 | 24 | fits | 26,311 | 20 | 0.756 |
| get_configuration | `aecp.get_configuration.if0` | 12,856 | 0.129 | 20 | 24 | fits | 24,007 | 20 | 0.765 |
| entity_available | `aecp.entity_available.if0` | 21,216 | 0.212 | 20 | 24 | fits | 23,632 | 20 | 0.752 |
| get_name | `aecp.get_name.if0` | 23,673 | 0.237 | 20 | 24 | fits | 26,998 | 20 | 0.775 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 15,889 | 0.159 | 20 | 24 | fits | 27,449 | 25 | 0.749 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 25,069 | 0.251 | 20 | 24 | fits | 28,058 | 27 | 0.777 |
| get_as_path, refused ENTITY_MISBEHAVING | `aecp.get_as_path.if0` | 15,333 | 0.153 | 20 | 24 | fits | 26,720 | 27 | 0.775 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 21,729 | 0.217 | 20 | 24 | fits | 24,249 | 20 | 0.776 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 20,847 | 0.208 | 20 | 24 | fits | 24,125 | 20 | 0.765 |
| set_name | `aecp.set_name.if0` | 22,883 | 0.229 | 20 | 24 | fits | 44,778 | 43 | 0.761 |
| lock_entity | `aecp.lock_entity.if0` | 27,106 | 0.271 | 20 | 24 | fits | 33,795 | 34 | 0.770 |
| unlock_entity | `aecp.unlock_entity.if0` | 19,677 | 0.197 | 20 | 24 | fits | 34,147 | 33 | 0.772 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
