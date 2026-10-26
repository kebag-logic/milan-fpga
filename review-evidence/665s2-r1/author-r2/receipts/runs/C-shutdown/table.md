### 1x1

1 of 1 paths and 1 of 1 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `control.shutdown.if0` (control-shutdown) | 24.903 (26.262) | MISS T_svc | 0 events | 1 | 1 |

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `control.shutdown.if0` | 1,245,131 | 24.903 | 10 | 200 | MISS T_svc | 1,313,095 | 39 (29) | 0.805 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
