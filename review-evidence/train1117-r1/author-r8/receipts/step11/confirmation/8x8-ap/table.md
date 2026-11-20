### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 20 paths and 0 of 22 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| add_audio_mappings_output | 0 | `aecp_fanout.add_audio_mappings_output.if0` (aecp-fanout) | 2.944 (3.414) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings_output | 1 | `aecp_fanout.add_audio_mappings_output.if1` (aecp-fanout) | 3.218 (3.686) | fits | 0 aecp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 0 | `aecp_fanout.bind_rx_stream_info.if0` (aecp-fanout) | 2.001 (2.106) | fits | 0 acmp | 1 | 0 |
| BIND_RX -> GET_STREAM_INFO notice | 1 | `aecp_fanout.bind_rx_stream_info.if1` (aecp-fanout) | 1.152 (1.499) | fits | 0 acmp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.628 (1.050) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.583 (1.012) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 0 | `aecp_fanout.remove_audio_mappings_output.if0` (aecp-fanout) | 0.847 (1.311) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings_output | 1 | `aecp_fanout.remove_audio_mappings_output.if1` (aecp-fanout) | 0.855 (1.316) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.651 (1.096) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.661 (1.108) | fits | 0 aecp | 1 | 0 |
| set_configuration | 0 | `aecp_fanout.set_configuration.if0` (aecp-fanout) | 0.997 (1.455) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.580 (1.010) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.588 (1.018) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.624 (1.106) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.595 (1.052) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.999 (3.449) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 0 | `aecp_fanout.set_stream_info.if0` (aecp-fanout) | 1.990 (2.441) | fits | 0 aecp | 1 | 0 |
| set_stream_info | 1 | `aecp_fanout.set_stream_info.if1` (aecp-fanout) | 2.790 (3.245) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.572 (1.000) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.634 (1.058) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 174 | 0 | 110,081 (1.101) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 101 | 72,457 (0.725) | 4,151 (0.042) |

Longest pass that carries a step: 72,457 CPU cycles (0.725 ms), aecp-fanout; longest step: 4,151 (0.042 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 62,449 | 0.624 | 20 | 24 | fits | 75,565 | 160 | 0.399 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 65,056 | 0.651 | 20 | 24 | fits | 70,203 | 139 | 0.422 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 57,597 | 0.576 | 20 | 24 | fits | 64,707 | 140 | 0.360 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 57,973 | 0.580 | 20 | 24 | fits | 65,266 | 139 | 0.374 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if0` | 84,714 | 0.847 | 20 | 24 | fits | 91,689 | 160 | 0.464 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if0` | 294,368 | 2.944 | 20 | 24 | fits | 90,122 | 161 | 0.457 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 299,871 | 2.999 | 20 | 24 | fits | 67,350 | 116 | 0.419 |
| set_configuration | `aecp_fanout.set_configuration.if0` | 99,666 | 0.997 | 20 | 24 | fits | 110,081 | 139 | 0.443 |
| set_stream_info | `aecp_fanout.set_stream_info.if0` | 199,043 | 1.990 | 20 | 24 | fits | 72,980 | 128 | 0.439 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 62,788 | 0.628 | 20 | 24 | fits | 65,786 | 140 | 0.382 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 57,200 | 0.572 | 20 | 24 | fits | 63,892 | 140 | 0.345 |
| set_name | `aecp_fanout.set_name.if1` | 59,477 | 0.595 | 20 | 24 | fits | 69,695 | 117 | 0.385 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 66,116 | 0.661 | 20 | 24 | fits | 71,294 | 139 | 0.421 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 58,245 | 0.582 | 20 | 24 | fits | 65,429 | 140 | 0.359 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 58,806 | 0.588 | 20 | 24 | fits | 66,173 | 139 | 0.374 |
| remove_audio_mappings_output | `aecp_fanout.remove_audio_mappings_output.if1` | 85,464 | 0.855 | 20 | 24 | fits | 92,274 | 160 | 0.460 |
| add_audio_mappings_output | `aecp_fanout.add_audio_mappings_output.if1` | 321,780 | 3.218 | 20 | 24 | fits | 90,904 | 161 | 0.455 |
| set_stream_info | `aecp_fanout.set_stream_info.if1` | 279,030 | 2.790 | 20 | 24 | fits | 73,608 | 129 | 0.437 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 58,274 | 0.583 | 20 | 24 | fits | 65,842 | 140 | 0.364 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 63,424 | 0.634 | 20 | 24 | fits | 66,282 | 140 | 0.371 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if0` | 200,141 | 2.001 | 20 | 24 | fits | 72,457 | 113 | 0.477 |
| BIND_RX -> GET_STREAM_INFO notice | `aecp_fanout.bind_rx_stream_info.if1` | 115,197 | 1.152 | 20 | 24 | fits | 61,743 | 109 | 0.326 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
