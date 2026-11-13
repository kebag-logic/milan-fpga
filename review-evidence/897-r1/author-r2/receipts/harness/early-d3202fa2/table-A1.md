### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 41 paths and 0 of 42 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.184 (0.395) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.099 (0.220) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.102 (0.235) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.088 (0.221) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.101 (0.231) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.245) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.135 (0.346) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.132 (0.376) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.185 (0.446) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.222 (0.503) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.226 (0.486) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.134 (0.336) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.238 (0.510) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.276 (0.568) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.175 (0.445) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.149 (0.305) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.212 (0.474) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.209 (0.467) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.106 (0.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.230 (0.493) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.225 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.113 (0.315) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.235 (0.502) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.199 (0.475) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.114 (0.255) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.197 (0.468) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.211 (0.475) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.178 (0.452) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.111 (0.252) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.143 (0.422) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.309 (0.604) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.097 (0.234) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.182 (0.303) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.418 (0.720) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.433 (0.684) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.470 (0.752) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.448 (0.724) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.442 (0.693) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.470 (0.767) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.452 (0.718) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.399 (0.663) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 109 | 0 | 66,517 (0.665) | fits |
| acmp-cmd | 81 | 0 | 66,517 (0.665) | fits |
| aecp | 107 | 0 | 66,517 (0.665) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 79 | 19,927 (0.199) | 1,959 (0.020) |
| acmp-cmd | 65 | 19,927 (0.199) | 1,959 (0.020) |
| aecp | 79 | 19,927 (0.199) | 2,130 (0.021) |

Longest pass that carries a step: 19,927 CPU cycles (0.199 ms), aecp-fanout; longest step: 2,130 (0.021 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 46,971 | 0.470 | 20 | 24 | fits | 58,081 | 88 | 0.538 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 44,836 | 0.448 | 20 | 24 | fits | 50,913 | 77 | 0.563 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 44,166 | 0.442 | 20 | 24 | fits | 45,751 | 78 | 0.508 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 38,691 | 0.387 | 20 | 24 | fits | 44,820 | 77 | 0.497 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 47,047 | 0.470 | 20 | 24 | fits | 52,658 | 66 | 0.589 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 41,839 | 0.418 | 20 | 24 | fits | 51,009 | 65 | 0.564 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 45,163 | 0.452 | 20 | 24 | fits | 49,596 | 66 | 0.574 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 43,278 | 0.433 | 20 | 24 | fits | 45,342 | 77 | 0.509 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 39,859 | 0.399 | 20 | 24 | fits | 44,976 | 78 | 0.502 |
| BIND_RX | `acmp.bind_rx.if0` | 18,410 | 0.184 | 20 | 20 | fits | 39,541 | 26 (77) | 0.799 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 13,499 | 0.135 | 20 | 20 | fits | 34,603 | 26 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,218 | 0.102 | 20 | 20 | fits | 23,542 | 15 (47) | 0.775 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,217 | 0.132 | 20 | 20 | fits | 37,575 | 18 (50) | 0.823 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,681 | 0.107 | 20 | 20 | fits | 24,504 | 17 (48) | 0.776 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,066 | 0.101 | 20 | 20 | fits | 23,094 | 16 (48) | 0.750 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,895 | 0.099 | 20 | 20 | fits | 22,022 | 16 (48) | 0.735 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,842 | 0.088 | 20 | 20 | fits | 22,140 | 16 (48) | 0.737 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,288 | 0.143 | 20 | 24 | fits | 26,064 | 20 | 0.786 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 14,887 | 0.149 | 20 | 24 | fits | 30,459 | 20 | 0.720 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 21,232 | 0.212 | 20 | 24 | fits | 25,234 | 20 | 0.719 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 23,457 | 0.235 | 20 | 24 | fits | 25,240 | 20 | 0.727 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 21,145 | 0.211 | 20 | 24 | fits | 25,439 | 20 | 0.715 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,836 | 0.178 | 20 | 24 | fits | 25,733 | 20 | 0.724 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 11,055 | 0.111 | 20 | 24 | fits | 25,171 | 20 | 0.732 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 20,878 | 0.209 | 20 | 24 | fits | 24,675 | 20 | 0.730 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 10,630 | 0.106 | 20 | 24 | fits | 24,606 | 20 | 0.742 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 23,013 | 0.230 | 20 | 24 | fits | 27,077 | 21 | 0.633 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 22,518 | 0.225 | 20 | 24 | fits | 24,116 | 20 | 0.763 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 11,275 | 0.113 | 20 | 24 | fits | 31,532 | 29 | 0.726 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 19,933 | 0.199 | 20 | 24 | fits | 24,522 | 20 | 0.723 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 11,425 | 0.114 | 20 | 24 | fits | 25,546 | 20 | 0.733 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 19,724 | 0.197 | 20 | 24 | fits | 24,762 | 20 | 0.734 |
| get_configuration | `aecp.get_configuration.if0` | 22,557 | 0.226 | 20 | 24 | fits | 22,704 | 20 | 0.755 |
| entity_available | `aecp.entity_available.if0` | 18,495 | 0.185 | 20 | 24 | fits | 22,372 | 20 | 0.734 |
| get_name | `aecp.get_name.if0` | 23,753 | 0.238 | 20 | 24 | fits | 26,181 | 20 | 0.768 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 13,391 | 0.134 | 20 | 24 | fits | 33,637 | 36 | 0.699 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 22,196 | 0.222 | 20 | 24 | fits | 27,042 | 29 | 0.763 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,748 | 0.097 | 20 | 24 | fits | 23,406 | 20 | 0.768 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 17,459 | 0.175 | 20 | 24 | fits | 22,398 | 20 | 0.738 |
| set_name | `aecp.set_name.if0` | 30,875 | 0.309 | 20 | 24 | fits | 41,967 | 42 | 0.748 |
| lock_entity | `aecp.lock_entity.if0` | 27,575 | 0.276 | 20 | 24 | fits | 30,169 | 33 | 0.748 |
| unlock_entity | `aecp.unlock_entity.if0` | 18,162 | 0.182 | 20 | 24 | fits | 30,254 | 32 | 0.753 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
