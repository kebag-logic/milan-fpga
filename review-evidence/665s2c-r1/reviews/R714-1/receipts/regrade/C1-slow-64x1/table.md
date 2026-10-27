### 1x1

1 of 3 paths and 1 of 3 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 16.556 (17.458) | MISS T_svc | 0 adp | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.073 (3.203) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.820 (2.676) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 3,657 | 0.073 | 10 | 200 | fits | 160,126 | 88 (11) | 0.087 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,005 | 0.820 | 10 | 200 | fits | 66,059 | 46 (39) | 0.091 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 827,776 | 16.556 | 10 | 200 | MISS T_svc | 872,891 | 43 (31) | 0.008 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
