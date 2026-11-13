### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 66 paths and 0 of 68 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.202 (0.497) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.179 (0.459) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.094 (0.310) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.101 (0.310) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.107 (0.329) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.112 (0.332) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.095 (0.309) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.092 (0.311) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.111 (0.334) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.115 (0.334) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.107 (0.327) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.111 (0.334) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.102 (0.379) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.102 (0.379) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.138 (0.456) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.156 (0.492) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.227 (0.681) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.103 (0.322) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.160 (0.617) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.136 (0.358) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.314 (0.771) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.250 (0.700) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.269 (0.724) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.287 (0.755) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.345 (0.801) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.110 (0.353) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.239 (0.403) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.406 (0.832) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.218 (0.670) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.095 (0.311) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.154 (0.391) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.303 (0.767) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.343 (0.839) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.286 (0.748) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.106 (0.341) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.253 (0.706) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.383 (0.847) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.246 (0.704) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.253 (0.710) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.258 (0.722) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.130 (0.349) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.108 (0.343) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.261 (0.714) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.345 (0.807) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.338 (0.802) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.258 (0.718) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.339 (0.794) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.133 (0.583) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.328 (0.788) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.561 (1.024) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.305 (0.491) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.087 (0.321) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.251 (0.707) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.391 (0.788) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.268 (0.666) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.526 (0.953) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.527 (0.956) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.749 (1.198) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.562 (1.010) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.714 (1.146) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.852 (1.284) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.829 (1.323) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.780 (1.248) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.737 (1.184) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.857 (1.293) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.581 (0.779) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 144 | 0 | 112,232 (1.122) | fits |
| acmp-cmd | 107 | 0 | 112,232 (1.122) | fits |
| aecp | 136 | 0 | 112,232 (1.122) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 94 | 34,091 (0.341) | 2,447 (0.024) |
| acmp-cmd | 67 | 34,091 (0.341) | 2,289 (0.023) |
| aecp | 89 | 34,091 (0.341) | 2,289 (0.023) |

Longest pass that carries a step: 34,091 CPU cycles (0.341 ms), aecp-fanout; longest step: 2,447 (0.024 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 82,923 | 0.829 | 20 | 24 | fits | 82,926 | 161 | 0.403 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 74,914 | 0.749 | 20 | 24 | fits | 69,889 | 140 | 0.420 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 52,982 | 0.530 | 20 | 24 | fits | 65,029 | 140 | 0.381 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 71,443 | 0.714 | 20 | 24 | fits | 64,044 | 140 | 0.368 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 73,653 | 0.737 | 20 | 24 | fits | 68,340 | 116 | 0.424 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 52,557 | 0.526 | 20 | 24 | fits | 65,176 | 140 | 0.378 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 85,707 | 0.857 | 20 | 24 | fits | 78,037 | 149 | 0.394 |
| set_name | `aecp_fanout.set_name.if1` | 78,002 | 0.780 | 20 | 24 | fits | 73,290 | 117 | 0.384 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 56,207 | 0.562 | 20 | 24 | fits | 70,356 | 140 | 0.428 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 85,194 | 0.852 | 20 | 24 | fits | 77,909 | 149 | 0.399 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 71,549 | 0.715 | 20 | 24 | fits | 64,207 | 140 | 0.372 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 52,741 | 0.527 | 20 | 24 | fits | 65,079 | 140 | 0.382 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 58,138 | 0.581 | 20 | 24 | fits | 77,920 | 149 | 0.393 |
| BIND_RX | `acmp.bind_rx.if0` | 20,247 | 0.202 | 20 | 20 | fits | 49,691 | 27 (77) | 0.782 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,199 | 0.102 | 20 | 20 | fits | 37,939 | 20 (32) | 0.828 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,732 | 0.107 | 20 | 20 | fits | 32,945 | 16 (47) | 0.761 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,776 | 0.138 | 20 | 20 | fits | 45,583 | 19 (50) | 0.827 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,698 | 0.107 | 20 | 20 | fits | 32,737 | 18 (48) | 0.722 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,123 | 0.111 | 20 | 20 | fits | 33,412 | 17 (48) | 0.762 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,401 | 0.094 | 20 | 20 | fits | 30,951 | 17 (48) | 0.692 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,450 | 0.095 | 20 | 20 | fits | 30,883 | 17 (48) | 0.692 |
| BIND_RX | `acmp.bind_rx.if1` | 17,857 | 0.179 | 20 | 20 | fits | 45,898 | 28 (77) | 0.732 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 10,167 | 0.102 | 20 | 20 | fits | 37,930 | 23 (32) | 0.800 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 11,190 | 0.112 | 20 | 20 | fits | 33,184 | 17 (47) | 0.753 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 15,640 | 0.156 | 20 | 20 | fits | 49,246 | 20 (50) | 0.838 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 11,058 | 0.111 | 20 | 20 | fits | 33,447 | 20 (48) | 0.728 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 11,466 | 0.115 | 20 | 20 | fits | 33,357 | 18 (48) | 0.750 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 10,054 | 0.101 | 20 | 20 | fits | 31,033 | 18 (48) | 0.686 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 9,174 | 0.092 | 20 | 20 | fits | 31,076 | 18 (48) | 0.686 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 13,299 | 0.133 | 20 | 24 | fits | 33,829 | 22 | 0.780 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 15,361 | 0.154 | 20 | 24 | fits | 39,060 | 22 | 0.709 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 34,296 | 0.343 | 20 | 24 | fits | 47,154 | 31 | 0.710 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 25,848 | 0.258 | 20 | 24 | fits | 34,638 | 22 | 0.723 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 33,775 | 0.338 | 20 | 24 | fits | 34,982 | 22 | 0.729 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 25,772 | 0.258 | 20 | 24 | fits | 35,264 | 22 | 0.729 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 33,855 | 0.339 | 20 | 24 | fits | 34,171 | 22 | 0.734 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 10,634 | 0.106 | 20 | 24 | fits | 34,074 | 22 | 0.741 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 25,272 | 0.253 | 20 | 24 | fits | 34,138 | 22 | 0.743 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 38,294 | 0.383 | 20 | 24 | fits | 39,359 | 23 | 0.660 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 24,590 | 0.246 | 20 | 24 | fits | 33,726 | 22 | 0.756 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 25,341 | 0.253 | 20 | 24 | fits | 33,914 | 22 | 0.768 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 10,779 | 0.108 | 20 | 24 | fits | 34,305 | 22 | 0.737 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 26,146 | 0.261 | 20 | 24 | fits | 34,935 | 22 | 0.732 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 34,540 | 0.345 | 20 | 24 | fits | 35,473 | 22 | 0.741 |
| get_configuration | `aecp.get_configuration.if0` | 31,420 | 0.314 | 20 | 24 | fits | 31,863 | 22 | 0.752 |
| entity_available | `aecp.entity_available.if0` | 22,707 | 0.227 | 20 | 24 | fits | 31,592 | 22 | 0.738 |
| get_name | `aecp.get_name.if0` | 34,502 | 0.345 | 20 | 24 | fits | 34,866 | 22 | 0.758 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 26,865 | 0.269 | 20 | 24 | fits | 35,726 | 29 | 0.727 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 16,041 | 0.160 | 20 | 24 | fits | 36,821 | 31 | 0.778 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 8,739 | 0.087 | 20 | 24 | fits | 32,094 | 22 | 0.761 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 21,808 | 0.218 | 20 | 24 | fits | 30,608 | 22 | 0.721 |
| set_name | `aecp.set_name.if0` | 56,082 | 0.561 | 20 | 24 | fits | 57,206 | 66 | 0.694 |
| lock_entity | `aecp.lock_entity.if0` | 23,858 | 0.239 | 20 | 24 | fits | 40,329 | 47 | 0.719 |
| unlock_entity | `aecp.unlock_entity.if0` | 39,083 | 0.391 | 20 | 24 | fits | 40,145 | 46 | 0.720 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 32,826 | 0.328 | 20 | 24 | fits | 33,581 | 20 | 0.771 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 30,261 | 0.303 | 20 | 24 | fits | 37,891 | 20 | 0.706 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 28,564 | 0.286 | 20 | 24 | fits | 35,517 | 20 | 0.753 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 13,008 | 0.130 | 20 | 24 | fits | 34,940 | 20 | 0.740 |
| get_configuration | `aecp.get_configuration.if1` | 24,974 | 0.250 | 20 | 24 | fits | 31,390 | 20 | 0.753 |
| entity_available | `aecp.entity_available.if1` | 10,340 | 0.103 | 20 | 24 | fits | 32,201 | 20 | 0.760 |
| get_name | `aecp.get_name.if1` | 10,985 | 0.110 | 20 | 24 | fits | 35,252 | 20 | 0.767 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 28,658 | 0.287 | 20 | 24 | fits | 35,651 | 27 | 0.734 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 13,641 | 0.136 | 20 | 24 | fits | 35,801 | 29 | 0.772 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 25,064 | 0.251 | 20 | 24 | fits | 31,887 | 20 | 0.767 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 9,478 | 0.095 | 20 | 24 | fits | 31,128 | 20 | 0.741 |
| set_name | `aecp.set_name.if1` | 30,548 | 0.305 | 20 | 24 | fits | 49,122 | 25 | 0.744 |
| lock_entity | `aecp.lock_entity.if1` | 40,590 | 0.406 | 20 | 24 | fits | 40,910 | 50 | 0.696 |
| unlock_entity | `aecp.unlock_entity.if1` | 26,836 | 0.268 | 20 | 24 | fits | 41,383 | 49 | 0.704 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
