### 1x1

1 of 1 paths and 1 of 1 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `control.shutdown.if0` (control-shutdown) | 16.328 (17.258) | MISS T_svc | 1 events | 1 | 1 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `control.shutdown.if0` | 816,421 | 16.328 | 10 | 200 | MISS T_svc | 862,882 | 39 (29) | 0.005 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
