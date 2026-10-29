### 1x1

0 of 3 paths and 0 of 3 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 17.322 (17.448) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.026 (0.929) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.259 (0.533) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 1,315 | 0.026 | 20 | 200 | fits | 46,474 | 49 (11) | 0.755 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 12,967 | 0.259 | 20 | 200 | fits | 14,576 | 25 (39) | 0.589 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 866,114 | 17.322 | 20 | 200 | fits | 872,406 | 16 (31) | 0.554 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
