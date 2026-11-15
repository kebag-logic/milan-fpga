### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 9 paths and 0 of 9 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.687 (1.097) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.133 (0.697) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 1 | `aecp_reboot.entity_1.if1` (aecp-reboot) | 0.130 (0.694) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.338 (0.909) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 1 | `aecp_reboot.locked.if1` (aecp-reboot) | 0.336 (0.904) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.131 (0.473) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 1 | `aecp_reboot.short.if1` (aecp-reboot) | 0.319 (0.895) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.320 (0.892) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 1 | `aecp_reboot.stream_input.if1` (aecp-reboot) | 0.323 (0.891) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-reboot | 150 | 0 | 90,765 (0.908) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-reboot | 94 | 35,310 (0.353) | 2,906 (0.029) |

Longest pass that carries a step: 35,310 CPU cycles (0.353 ms), aecp-reboot; longest step: 2,906 (0.029 ms), aecp-reboot.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 13,107 | 0.131 | 20 | 24 | fits | 47,315 | 25 | 0.749 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 31,967 | 0.320 | 20 | 24 | fits | 37,626 | 19 | 0.747 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 13,341 | 0.133 | 20 | 24 | fits | 37,639 | 19 | 0.747 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 33,804 | 0.338 | 20 | 24 | fits | 38,671 | 19 | 0.773 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if1` | 31,941 | 0.319 | 20 | 24 | fits | 37,835 | 20 | 0.747 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if1` | 32,277 | 0.323 | 20 | 24 | fits | 37,724 | 19 | 0.750 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if1` | 13,003 | 0.130 | 20 | 24 | fits | 37,286 | 19 | 0.742 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if1` | 33,557 | 0.336 | 20 | 24 | fits | 38,496 | 19 | 0.764 |
| REBOOT | `aecp_reboot.accepted.if0` | 68,659 | 0.687 | 20 | 24 | fits | 58,088 | 116 | 0.331 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
