### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 18 paths and 0 of 19 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.481 (2.802) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 3.289 (3.619) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 0.873 (1.087) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.429 (0.716) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.512 (0.831) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 3.303 (3.617) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.402 (0.757) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.534 (0.852) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.424 (0.712) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.502 (0.841) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 3.353 (3.671) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 3.063 (3.375) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.383 (0.677) | fits | 0 aecp | 1 | 0 |
| REBOOT | 0 | `aecp_reboot.accepted.if0` (aecp-reboot) | 0.404 (0.661) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | 0 | `aecp_reboot.entity_1.if0` (aecp-reboot) | 0.168 (0.512) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused ENTITY_LOCKED | 0 | `aecp_reboot.locked.if0` (aecp-reboot) | 0.185 (0.535) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused BAD_ARGUMENTS | 0 | `aecp_reboot.short.if0` (aecp-reboot) | 0.169 (0.513) | fits | 0 aecp | 1 | 0 |
| REBOOT, refused NOT_SUPPORTED | 0 | `aecp_reboot.stream_input.if0` (aecp-reboot) | 0.122 (0.463) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 123 | 0 | 63,697 (0.637) | fits |
| aecp-reboot | 109 | 0 | 48,738 (0.487) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 84 | 23,362 (0.234) | 2,540 (0.025) |
| aecp-reboot | 78 | 23,362 (0.234) | 2,540 (0.025) |

Longest pass that carries a step: 23,362 CPU cycles (0.234 ms), aecp-fanout; longest step: 2,540 (0.025 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 50,179 | 0.502 | 20 | 24 | fits | 58,615 | 89 | 0.560 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 40,217 | 0.402 | 20 | 24 | fits | 50,002 | 78 | 0.581 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 42,411 | 0.424 | 20 | 24 | fits | 45,513 | 79 | 0.536 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 37,023 | 0.370 | 20 | 24 | fits | 44,869 | 78 | 0.528 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 51,188 | 0.512 | 20 | 24 | fits | 61,998 | 110 | 0.585 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 248,130 | 2.481 | 20 | 24 | fits | 60,681 | 109 | 0.590 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 330,302 | 3.303 | 20 | 24 | fits | 63,697 | 110 | 0.600 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 328,875 | 3.289 | 20 | 24 | fits | 62,077 | 109 | 0.596 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 335,260 | 3.353 | 20 | 24 | fits | 49,976 | 67 | 0.597 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 53,352 | 0.534 | 20 | 24 | fits | 63,283 | 77 | 0.613 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 306,255 | 3.063 | 20 | 24 | fits | 56,368 | 78 | 0.592 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 42,926 | 0.429 | 20 | 24 | fits | 45,801 | 78 | 0.540 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 38,263 | 0.383 | 20 | 24 | fits | 45,369 | 79 | 0.529 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 87,280 | 0.873 | 20 | 24 | fits | 41,028 | 59 | 0.543 |
| REBOOT, refused BAD_ARGUMENTS | `aecp_reboot.short.if0` | 16,867 | 0.169 | 20 | 24 | fits | 25,834 | 17 | 0.744 |
| REBOOT, refused NOT_SUPPORTED | `aecp_reboot.stream_input.if0` | 12,156 | 0.122 | 20 | 24 | fits | 25,609 | 17 | 0.741 |
| REBOOT, refused NO_SUCH_DESCRIPTOR | `aecp_reboot.entity_1.if0` | 16,757 | 0.168 | 20 | 24 | fits | 25,831 | 17 | 0.741 |
| REBOOT, refused ENTITY_LOCKED | `aecp_reboot.locked.if0` | 18,518 | 0.185 | 20 | 24 | fits | 26,760 | 17 | 0.762 |
| REBOOT | `aecp_reboot.accepted.if0` | 40,369 | 0.404 | 20 | 24 | fits | 38,483 | 66 | 0.481 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
