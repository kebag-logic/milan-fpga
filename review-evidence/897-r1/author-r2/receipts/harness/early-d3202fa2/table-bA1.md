### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 41 paths and 0 of 42 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.185 (0.390) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.096 (0.220) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.106 (0.232) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.099 (0.216) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.099 (0.227) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.105 (0.237) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.093 (0.298) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.133 (0.376) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.083 (0.219) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.176 (0.436) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.143 (0.392) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.112 (0.256) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.164 (0.423) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.283 (0.565) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.079 (0.217) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.208 (0.463) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.110 (0.250) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.110 (0.246) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.150 (0.411) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.130 (0.266) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.153 (0.403) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.094 (0.232) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.160 (0.414) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.155 (0.410) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.155 (0.418) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.105 (0.243) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.106 (0.251) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.119 (0.255) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.158 (0.414) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.200 (0.458) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.229 (0.406) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.139 (0.398) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.230 (0.472) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.479 (0.766) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.367 (0.459) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.403 (0.526) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.390 (0.505) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.458 (0.714) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.547 (0.841) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.444 (0.701) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.466 (0.721) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 109 | 0 | 66,016 (0.660) | fits |
| acmp-cmd | 82 | 0 | 66,016 (0.660) | fits |
| aecp | 109 | 0 | 66,016 (0.660) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 79 | 19,100 (0.191) | 2,053 (0.021) |
| acmp-cmd | 65 | 19,100 (0.191) | 1,867 (0.019) |
| aecp | 79 | 19,100 (0.191) | 1,867 (0.019) |

Longest pass that carries a step: 19,100 CPU cycles (0.191 ms), aecp-fanout; longest step: 2,053 (0.021 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 54,656 | 0.547 | 20 | 24 | fits | 57,760 | 88 | 0.543 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 39,014 | 0.390 | 20 | 24 | fits | 50,523 | 77 | 0.560 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 37,019 | 0.370 | 20 | 24 | fits | 46,599 | 78 | 0.525 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 45,798 | 0.458 | 20 | 24 | fits | 45,621 | 77 | 0.511 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 40,288 | 0.403 | 20 | 24 | fits | 52,643 | 66 | 0.589 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 47,881 | 0.479 | 20 | 24 | fits | 50,531 | 65 | 0.563 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 44,365 | 0.444 | 20 | 24 | fits | 49,165 | 66 | 0.570 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 36,725 | 0.367 | 20 | 24 | fits | 45,858 | 77 | 0.520 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 46,568 | 0.466 | 20 | 24 | fits | 45,381 | 78 | 0.509 |
| BIND_RX | `acmp.bind_rx.if0` | 18,524 | 0.185 | 20 | 20 | fits | 38,973 | 26 (77) | 0.798 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,257 | 0.093 | 20 | 20 | fits | 29,759 | 20 (32) | 0.827 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,605 | 0.106 | 20 | 20 | fits | 23,245 | 15 (47) | 0.767 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,279 | 0.133 | 20 | 20 | fits | 37,593 | 18 (50) | 0.838 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,462 | 0.105 | 20 | 20 | fits | 23,745 | 17 (48) | 0.762 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,909 | 0.099 | 20 | 20 | fits | 22,681 | 16 (48) | 0.741 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,638 | 0.096 | 20 | 20 | fits | 22,038 | 16 (48) | 0.731 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,909 | 0.099 | 20 | 20 | fits | 21,606 | 16 (48) | 0.720 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 19,950 | 0.200 | 20 | 24 | fits | 24,923 | 20 | 0.772 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 20,817 | 0.208 | 20 | 24 | fits | 29,502 | 20 | 0.699 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,014 | 0.110 | 20 | 24 | fits | 25,018 | 20 | 0.712 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,014 | 0.160 | 20 | 24 | fits | 24,777 | 20 | 0.713 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 10,595 | 0.106 | 20 | 24 | fits | 25,106 | 20 | 0.704 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 11,871 | 0.119 | 20 | 24 | fits | 25,526 | 20 | 0.717 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,827 | 0.158 | 20 | 24 | fits | 24,634 | 20 | 0.716 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 10,957 | 0.110 | 20 | 24 | fits | 24,629 | 20 | 0.723 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,970 | 0.150 | 20 | 24 | fits | 24,294 | 20 | 0.732 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 13,005 | 0.130 | 20 | 24 | fits | 26,605 | 21 | 0.613 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 15,282 | 0.153 | 20 | 24 | fits | 23,460 | 20 | 0.747 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,416 | 0.094 | 20 | 24 | fits | 23,249 | 20 | 0.736 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,533 | 0.155 | 20 | 24 | fits | 24,422 | 20 | 0.721 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 15,451 | 0.155 | 20 | 24 | fits | 25,119 | 20 | 0.722 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 10,527 | 0.105 | 20 | 24 | fits | 24,268 | 20 | 0.725 |
| get_configuration | `aecp.get_configuration.if0` | 14,307 | 0.143 | 20 | 24 | fits | 22,454 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if0` | 8,326 | 0.083 | 20 | 24 | fits | 21,907 | 20 | 0.720 |
| get_name | `aecp.get_name.if0` | 16,443 | 0.164 | 20 | 24 | fits | 25,584 | 20 | 0.757 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,167 | 0.112 | 20 | 24 | fits | 25,617 | 27 | 0.705 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 17,569 | 0.176 | 20 | 24 | fits | 26,398 | 29 | 0.751 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 13,925 | 0.139 | 20 | 24 | fits | 22,420 | 20 | 0.745 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 7,858 | 0.079 | 20 | 24 | fits | 21,722 | 20 | 0.718 |
| set_name | `aecp.set_name.if0` | 22,897 | 0.229 | 20 | 24 | fits | 40,647 | 42 | 0.743 |
| lock_entity | `aecp.lock_entity.if0` | 28,255 | 0.283 | 20 | 24 | fits | 29,991 | 33 | 0.748 |
| unlock_entity | `aecp.unlock_entity.if0` | 23,024 | 0.230 | 20 | 24 | fits | 30,635 | 32 | 0.764 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
