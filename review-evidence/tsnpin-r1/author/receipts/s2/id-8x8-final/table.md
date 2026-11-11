### 8x8

0 of 6 paths and 0 of 6 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.498 (2.656) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.584 (2.656) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.489 (12.146) | fits | 1 events | 1 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-gm) | 1.225 (12.146) | fits | 1 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 1.060 (5.510) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-gm) | 0.378 (2.699) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| LINK_UP | `adp.link_up.if0` | 24,472 | 0.489 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| LINK_UP | `adp.link_up.if1` | 61,228 | 1.225 | 10 | 200 | fits | 607,278 | 304 (11) | 0.036 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 52,997 | 1.060 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 18,908 | 0.378 | 10 | 200 | fits | 134,973 | 84 (39) | 0.065 |
| GM_CHANGE | `adp.gm_change.if0` | 24,897 | 0.498 | 10 | 200 | fits | 132,786 | 34 (11) | 0.068 |
| GM_CHANGE | `adp.gm_change.if1` | 29,219 | 0.584 | 10 | 200 | fits | 132,786 | 34 (11) | 0.068 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
