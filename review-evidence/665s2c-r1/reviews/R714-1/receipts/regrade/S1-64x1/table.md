### 1x1

0 of 1 paths and 0 of 2 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `adp.shutdown.if0` (adp-shutdown) | 0.333 (1.258) | fits | 1 events | 2 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `adp.shutdown.if0` | 16,661 | 0.333 | 10 | 200 | fits | 62,891 | 39 (29) | 0.086 |
| SHUTDOWN | `control.shutdown.if0` | 16,661 | 0.333 | 10 | 200 | fits | 62,891 | 39 (29) | 0.086 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
