### 1x1

1 of 8 paths and 1 of 9 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 8.596 (9.810) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.416 (9.569) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 8.604 (9.820) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.771 (9.647) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 7.968 (9.122) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.493 (13.281) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.003 (8.846) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 8.427 (9.581) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 574,631 | 11.493 | 10 | 24 | MISS T_svc | 664,036 | 622 | 0.886 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 438,537 | 8.771 | 10 | 24 | fits | 482,370 | 335 | 0.880 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 397,783 | 7.956 | 10 | 24 | fits | 455,413 | 311 | 0.881 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 398,391 | 7.968 | 10 | 24 | fits | 456,093 | 311 | 0.881 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 430,196 | 8.604 | 10 | 24 | fits | 491,013 | 351 | 0.880 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 429,815 | 8.596 | 10 | 24 | fits | 490,506 | 351 | 0.879 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 400,164 | 8.003 | 10 | 24 | fits | 442,281 | 317 | 0.880 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 420,777 | 8.416 | 10 | 24 | fits | 478,446 | 362 | 0.883 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 421,329 | 8.427 | 10 | 24 | fits | 479,031 | 362 | 0.883 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
