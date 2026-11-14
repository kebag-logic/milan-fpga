### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 25 paths and 0 of 25 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.146 (0.428) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.169 (0.455) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.195 (0.479) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.231 (0.520) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.171 (0.464) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.229 (0.562) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.147 (0.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.259 (0.552) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.167 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.168 (0.455) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.210 (0.499) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.190 (0.477) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.208 (0.497) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.209 (0.498) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.215 (0.505) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.165 (0.452) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.221 (0.513) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.166 (0.456) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.221 (0.513) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.174 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.217 (0.506) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.144 (0.433) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.240 (0.631) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.196 (0.486) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.217 (0.569) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp | 111 | 0 | 44,541 (0.445) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp | 79 | 21,008 (0.210) | 2,046 (0.020) |

Longest pass that carries a step: 21,008 CPU cycles (0.210 ms), aecp; longest step: 2,046 (0.020 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,406 | 0.144 | 20 | 24 | fits | 26,875 | 20 | 0.788 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 25,949 | 0.259 | 20 | 24 | fits | 30,395 | 20 | 0.713 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,713 | 0.167 | 20 | 24 | fits | 25,650 | 20 | 0.725 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 21,472 | 0.215 | 20 | 24 | fits | 25,790 | 20 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 22,099 | 0.221 | 20 | 24 | fits | 26,839 | 20 | 0.739 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,358 | 0.174 | 20 | 24 | fits | 26,216 | 20 | 0.723 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 21,732 | 0.217 | 20 | 24 | fits | 25,541 | 20 | 0.735 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 16,755 | 0.168 | 20 | 24 | fits | 25,613 | 20 | 0.738 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,020 | 0.210 | 20 | 24 | fits | 25,022 | 20 | 0.746 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,015 | 0.190 | 20 | 24 | fits | 27,828 | 21 | 0.642 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 20,832 | 0.208 | 20 | 24 | fits | 24,755 | 20 | 0.763 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 20,866 | 0.209 | 20 | 24 | fits | 25,064 | 20 | 0.763 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 16,524 | 0.165 | 20 | 24 | fits | 25,337 | 20 | 0.725 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 22,092 | 0.221 | 20 | 24 | fits | 26,534 | 20 | 0.737 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 16,643 | 0.166 | 20 | 24 | fits | 25,655 | 20 | 0.738 |
| get_configuration | `aecp.get_configuration.if0` | 19,459 | 0.195 | 20 | 24 | fits | 23,194 | 20 | 0.748 |
| entity_available | `aecp.entity_available.if0` | 14,564 | 0.146 | 20 | 24 | fits | 22,958 | 20 | 0.732 |
| get_name | `aecp.get_name.if0` | 17,120 | 0.171 | 20 | 24 | fits | 26,189 | 20 | 0.761 |
| get_counters | `aecp.get_counters.if0` | 23,065 | 0.231 | 20 | 24 | fits | 27,361 | 20 | 0.742 |
| get_avb_info | `aecp.get_avb_info.if0` | 16,872 | 0.169 | 20 | 24 | fits | 25,620 | 20 | 0.770 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 19,627 | 0.196 | 20 | 24 | fits | 23,966 | 20 | 0.766 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,675 | 0.147 | 20 | 24 | fits | 22,976 | 20 | 0.735 |
| set_name | `aecp.set_name.if0` | 23,995 | 0.240 | 20 | 24 | fits | 44,541 | 41 | 0.770 |
| lock_entity | `aecp.lock_entity.if0` | 22,915 | 0.229 | 20 | 24 | fits | 33,888 | 33 | 0.778 |
| unlock_entity | `aecp.unlock_entity.if0` | 21,720 | 0.217 | 20 | 24 | fits | 34,370 | 32 | 0.768 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
