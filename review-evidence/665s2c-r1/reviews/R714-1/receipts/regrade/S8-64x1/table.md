### 8x8

0 of 2 paths and 0 of 3 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `adp.shutdown.if0` (adp-shutdown) | 0.323 (2.643) | fits | 0 events | 2 | 0 |
| SHUTDOWN | 1 | `adp.shutdown.if1` (adp-shutdown) | 0.638 (2.643) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `adp.shutdown.if0` | 16,165 | 0.323 | 10 | 200 | fits | 132,149 | 69 (29) | 0.043 |
| SHUTDOWN | `adp.shutdown.if1` | 31,883 | 0.638 | 10 | 200 | fits | 132,149 | 69 (29) | 0.043 |
| SHUTDOWN | `control.shutdown.if0` | 16,165 | 0.323 | 10 | 200 | fits | 132,149 | 69 (29) | 0.043 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
