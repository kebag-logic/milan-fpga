### 1x1

0 of 3 paths and 0 of 3 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.057 (0.340) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.043 (1.594) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.412 (1.012) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 2,144 | 0.043 | 20 | 200 | fits | 79,710 | 49 (11) | 0.849 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 20,583 | 0.412 | 20 | 200 | fits | 31,699 | 25 (39) | 0.823 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 2,844 | 0.057 | 20 | 200 | fits | 17,022 | 17 (31) | 0.789 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
