### 1x1

1 of 3 paths and 1 of 3 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 24.614 (25.945) | MISS T_svc | 0 adp | 1 | 1 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.114 (4.988) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 1.406 (4.124) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 5,708 | 0.114 | 10 | 200 | fits | 249,417 | 88 (11) | 0.885 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 70,301 | 1.406 | 10 | 200 | fits | 102,073 | 46 (39) | 0.868 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 1,230,725 | 24.614 | 10 | 200 | MISS T_svc | 1,297,237 | 37 (31) | 0.804 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
