### 1x1

1 of 3 paths and 1 of 3 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 24.614 (25.940) | MISS T_svc | 0 adp | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.106 (4.969) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.865 (3.568) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 5,281 | 0.106 | 10 | 200 | fits | 248,452 | 88 (11) | 0.886 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 43,255 | 0.865 | 10 | 200 | fits | 101,078 | 46 (39) | 0.870 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 1,230,725 | 24.614 | 10 | 200 | MISS T_svc | 1,297,019 | 37 (31) | 0.804 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
