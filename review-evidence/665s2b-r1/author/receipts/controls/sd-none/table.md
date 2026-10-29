### 1x1

1 of 1 paths and 1 of 1 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `control.shutdown.if0` (control-shutdown) | 48.933 (49.260) | MISS T_svc | 0 events | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `control.shutdown.if0` | 2,446,628 | 48.933 | 20 | 200 | MISS T_svc | 2,463,017 | 18 (29) | 0.800 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
