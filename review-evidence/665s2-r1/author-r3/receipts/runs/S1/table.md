### 1x1

0 of 1 paths and 0 of 2 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| SHUTDOWN | 0 | `adp.shutdown.if0` (adp-shutdown) | 0.582 (1.941) | fits | 0 events | 2 | 0 |

Composed windows: the longest pass is the composed maximum only where the window released its whole load.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| SHUTDOWN | `adp.shutdown.if0` | 29,085 | 0.582 | 10 | 200 | fits | 97,049 | 39 (29) | 0.871 |
| SHUTDOWN | `control.shutdown.if0` | 29,085 | 0.582 | 10 | 200 | fits | 97,049 | 39 (29) | 0.871 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
