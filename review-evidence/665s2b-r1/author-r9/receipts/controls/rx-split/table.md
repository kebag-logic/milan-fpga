### 1x1

0 of 3 paths and 0 of 3 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 17.324 (17.423) | fits | 0 adp | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (control) | 0.023 (0.881) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (control) | 0.205 (0.424) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 1,147 | 0.023 | 20 | 200 | fits | 44,026 | 49 (11) | 0.728 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,275 | 0.205 | 20 | 200 | fits | 12,806 | 25 (39) | 0.493 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 866,191 | 17.324 | 20 | 200 | fits | 871,174 | 16 (31) | 0.366 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
