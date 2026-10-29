### 1x1

1 of 3 paths and 1 of 3 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 48.697 (48.998) | MISS T_svc | 0 adp | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.044 (1.622) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.409 (1.059) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 2,186 | 0.044 | 20 | 200 | fits | 81,117 | 49 (11) | 0.847 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,447 | 0.409 | 20 | 200 | fits | 33,150 | 25 (39) | 0.820 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 2,434,840 | 48.697 | 20 | 200 | MISS T_svc | 2,449,918 | 16 (31) | 0.800 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
