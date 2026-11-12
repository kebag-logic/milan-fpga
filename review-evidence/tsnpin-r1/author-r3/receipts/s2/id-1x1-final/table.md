### 1x1

0 of 3 paths and 0 of 3 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.083 (1.044) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.083 (3.209) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.825 (2.741) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 4,142 | 0.083 | 10 | 200 | fits | 160,452 | 88 (11) | 0.093 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 41,270 | 0.825 | 10 | 200 | fits | 64,004 | 46 (39) | 0.101 |
| GM_CHANGE | `adp.gm_change.if0` | 4,161 | 0.083 | 10 | 200 | fits | 52,189 | 18 (11) | 0.107 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
