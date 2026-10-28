### 8x8

11 of 11 paths and 13 of 13 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 16.754 (22.546) | MISS T_svc | 0 aecp | 1 | 1 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 16.295 (20.388) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 16.351 (19.760) | MISS T_svc | 0 aecp | 1 | 1 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 14.009 (19.145) | MISS T_svc | 0 aecp | 1 | 1 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 15.977 (21.768) | MISS T_svc | 0 aecp | 2 | 2 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 15.314 (21.113) | MISS T_svc | 0 aecp | 2 | 2 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 20.456 (28.574) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 21.231 (27.704) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 15.811 (18.875) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 16.282 (22.074) | MISS T_svc | 0 aecp | 1 | 1 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 13.925 (17.264) | MISS T_svc | 0 aecp | 1 | 1 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 1,022,780 | 20.456 | 10 | 24 | MISS T_svc | 1,231,178 | 1172 | 0.881 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 817,561 | 16.351 | 10 | 24 | MISS T_svc | 790,356 | 613 | 0.876 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 798,831 | 15.977 | 10 | 24 | MISS T_svc | 821,254 | 587 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 774,415 | 15.488 | 10 | 24 | MISS T_svc | 782,838 | 580 | 0.877 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 790,531 | 15.811 | 10 | 24 | MISS T_svc | 746,389 | 592 | 0.878 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 837,681 | 16.754 | 10 | 24 | MISS T_svc | 860,954 | 686 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 814,078 | 16.282 | 10 | 24 | MISS T_svc | 821,810 | 679 | 0.880 |
| set_name | `aecp_fanout.set_name.if1` | 1,061,527 | 21.231 | 10 | 24 | MISS T_svc | 1,187,452 | 1139 | 0.882 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 700,438 | 14.009 | 10 | 24 | MISS T_svc | 957,244 | 681 | 0.879 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 765,679 | 15.314 | 10 | 24 | MISS T_svc | 786,118 | 580 | 0.878 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 655,318 | 13.106 | 10 | 24 | MISS T_svc | 822,590 | 587 | 0.878 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 814,768 | 16.295 | 10 | 24 | MISS T_svc | 821,427 | 679 | 0.880 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 696,236 | 13.925 | 10 | 24 | MISS T_svc | 863,199 | 686 | 0.880 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
