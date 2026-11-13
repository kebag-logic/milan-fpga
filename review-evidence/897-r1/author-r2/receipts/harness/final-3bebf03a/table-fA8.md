### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 66 paths and 0 of 68 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.209 (0.505) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.189 (0.467) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.097 (0.317) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.097 (0.319) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.112 (0.339) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.118 (0.339) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.099 (0.318) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.097 (0.320) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.116 (0.345) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.110 (0.341) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.112 (0.336) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.112 (0.338) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.107 (0.394) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.109 (0.393) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.151 (0.471) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.162 (0.503) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.237 (0.705) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.260 (0.725) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.290 (0.754) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.306 (0.780) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.313 (0.790) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.090 (0.320) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.348 (0.831) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.297 (0.761) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.334 (0.816) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.116 (0.351) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.479 (0.885) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.254 (0.423) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.311 (0.775) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.248 (0.710) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.382 (0.864) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.150 (0.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.345 (0.827) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.291 (0.755) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.333 (0.814) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.256 (0.729) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.379 (0.864) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.331 (0.815) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.251 (0.724) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.266 (0.735) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.114 (0.355) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.335 (0.817) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.349 (0.866) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.265 (0.752) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.339 (0.820) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.272 (0.742) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.258 (0.741) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.146 (0.618) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.259 (0.731) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.485 (0.952) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.301 (0.502) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.086 (0.323) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.093 (0.320) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.404 (0.808) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.429 (0.840) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.737 (1.181) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.735 (1.177) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.690 (1.154) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.768 (1.228) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.799 (1.240) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.728 (1.170) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.768 (1.269) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.719 (1.200) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.681 (1.157) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.723 (0.999) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.738 (1.180) | fits | 0 aecp | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| aecp-fanout | 147 | 0 | 112,313 (1.123) | fits |
| acmp-cmd | 108 | 0 | 112,313 (1.123) | fits |
| aecp | 136 | 0 | 112,313 (1.123) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| aecp-fanout | 94 | 35,809 (0.358) | 2,990 (0.030) |
| acmp-cmd | 67 | 35,809 (0.358) | 2,918 (0.029) |
| aecp | 89 | 35,809 (0.358) | 3,059 (0.031) |

Longest pass that carries a step: 35,809 CPU cycles (0.358 ms), aecp-fanout; longest step: 3,059 (0.031 ms), aecp.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| set_name | `aecp_fanout.set_name.if0` | 76,811 | 0.768 | 20 | 24 | fits | 83,678 | 161 | 0.413 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 69,019 | 0.690 | 20 | 24 | fits | 70,922 | 140 | 0.437 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 73,201 | 0.732 | 20 | 24 | fits | 65,882 | 140 | 0.394 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 79,875 | 0.799 | 20 | 24 | fits | 79,558 | 149 | 0.412 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 68,069 | 0.681 | 20 | 24 | fits | 69,551 | 116 | 0.433 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 73,737 | 0.737 | 20 | 24 | fits | 66,155 | 140 | 0.390 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 72,323 | 0.723 | 20 | 24 | fits | 66,273 | 140 | 0.383 |
| set_name | `aecp_fanout.set_name.if1` | 71,943 | 0.719 | 20 | 24 | fits | 74,177 | 117 | 0.408 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 76,762 | 0.768 | 20 | 24 | fits | 70,823 | 140 | 0.439 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 72,750 | 0.728 | 20 | 24 | fits | 65,694 | 140 | 0.387 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 65,543 | 0.655 | 20 | 24 | fits | 65,331 | 140 | 0.385 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 73,487 | 0.735 | 20 | 24 | fits | 65,847 | 140 | 0.387 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 73,751 | 0.738 | 20 | 24 | fits | 65,835 | 140 | 0.387 |
| BIND_RX | `acmp.bind_rx.if0` | 20,936 | 0.209 | 20 | 20 | fits | 50,492 | 27 (77) | 0.789 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,663 | 0.107 | 20 | 20 | fits | 39,416 | 21 (32) | 0.838 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,232 | 0.112 | 20 | 20 | fits | 33,880 | 16 (47) | 0.782 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,063 | 0.151 | 20 | 20 | fits | 47,076 | 19 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 11,205 | 0.112 | 20 | 20 | fits | 33,621 | 18 (48) | 0.748 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,584 | 0.116 | 20 | 20 | fits | 34,527 | 17 (48) | 0.787 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,697 | 0.097 | 20 | 20 | fits | 31,692 | 17 (48) | 0.719 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,923 | 0.099 | 20 | 20 | fits | 31,760 | 17 (48) | 0.721 |
| BIND_RX | `acmp.bind_rx.if1` | 18,923 | 0.189 | 20 | 20 | fits | 46,701 | 28 (77) | 0.742 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 10,903 | 0.109 | 20 | 20 | fits | 39,332 | 23 (32) | 0.819 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 11,806 | 0.118 | 20 | 20 | fits | 33,916 | 17 (47) | 0.776 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 16,178 | 0.162 | 20 | 20 | fits | 50,281 | 20 (50) | 0.846 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 11,169 | 0.112 | 20 | 20 | fits | 33,836 | 20 (48) | 0.737 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 10,956 | 0.110 | 20 | 20 | fits | 34,119 | 18 (48) | 0.764 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 9,655 | 0.097 | 20 | 20 | fits | 31,885 | 18 (48) | 0.713 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 9,689 | 0.097 | 20 | 20 | fits | 31,953 | 18 (48) | 0.715 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,579 | 0.146 | 20 | 24 | fits | 34,642 | 22 | 0.786 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 38,173 | 0.382 | 20 | 24 | fits | 39,338 | 22 | 0.703 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 34,494 | 0.345 | 20 | 24 | fits | 36,062 | 22 | 0.744 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 26,602 | 0.266 | 20 | 24 | fits | 35,464 | 22 | 0.725 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 33,899 | 0.339 | 20 | 24 | fits | 35,564 | 22 | 0.731 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 27,152 | 0.272 | 20 | 24 | fits | 36,088 | 22 | 0.731 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 25,808 | 0.258 | 20 | 24 | fits | 34,818 | 22 | 0.735 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 33,279 | 0.333 | 20 | 24 | fits | 34,765 | 22 | 0.744 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 25,612 | 0.256 | 20 | 24 | fits | 34,819 | 22 | 0.744 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 37,856 | 0.379 | 20 | 24 | fits | 39,910 | 23 | 0.662 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 33,143 | 0.331 | 20 | 24 | fits | 34,745 | 22 | 0.765 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 25,085 | 0.251 | 20 | 24 | fits | 34,290 | 22 | 0.764 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 33,455 | 0.335 | 20 | 24 | fits | 35,040 | 22 | 0.741 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 34,904 | 0.349 | 20 | 24 | fits | 48,540 | 31 | 0.712 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 26,478 | 0.265 | 20 | 24 | fits | 35,764 | 22 | 0.737 |
| get_configuration | `aecp.get_configuration.if0` | 31,321 | 0.313 | 20 | 24 | fits | 32,347 | 22 | 0.758 |
| entity_available | `aecp.entity_available.if0` | 23,737 | 0.237 | 20 | 24 | fits | 32,468 | 22 | 0.747 |
| get_name | `aecp.get_name.if0` | 33,401 | 0.334 | 20 | 24 | fits | 35,266 | 22 | 0.762 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 34,850 | 0.348 | 20 | 24 | fits | 36,660 | 29 | 0.739 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 28,999 | 0.290 | 20 | 24 | fits | 37,470 | 31 | 0.777 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 8,608 | 0.086 | 20 | 24 | fits | 32,313 | 22 | 0.763 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 31,057 | 0.311 | 20 | 24 | fits | 31,449 | 22 | 0.727 |
| set_name | `aecp.set_name.if0` | 48,548 | 0.485 | 20 | 24 | fits | 57,188 | 66 | 0.691 |
| lock_entity | `aecp.lock_entity.if0` | 47,899 | 0.479 | 20 | 24 | fits | 41,616 | 47 | 0.731 |
| unlock_entity | `aecp.unlock_entity.if0` | 40,442 | 0.404 | 20 | 24 | fits | 41,001 | 46 | 0.726 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 25,908 | 0.259 | 20 | 24 | fits | 33,784 | 20 | 0.766 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 14,996 | 0.150 | 20 | 24 | fits | 38,087 | 20 | 0.704 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 29,065 | 0.291 | 20 | 24 | fits | 35,403 | 20 | 0.739 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 11,371 | 0.114 | 20 | 24 | fits | 35,543 | 20 | 0.738 |
| get_configuration | `aecp.get_configuration.if1` | 8,980 | 0.090 | 20 | 24 | fits | 32,005 | 20 | 0.757 |
| entity_available | `aecp.entity_available.if1` | 26,000 | 0.260 | 20 | 24 | fits | 32,422 | 20 | 0.752 |
| get_name | `aecp.get_name.if1` | 11,560 | 0.116 | 20 | 24 | fits | 35,138 | 20 | 0.767 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 29,733 | 0.297 | 20 | 24 | fits | 36,059 | 27 | 0.732 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 30,565 | 0.306 | 20 | 24 | fits | 36,612 | 29 | 0.773 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 9,350 | 0.093 | 20 | 24 | fits | 32,003 | 20 | 0.762 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 24,783 | 0.248 | 20 | 24 | fits | 30,908 | 20 | 0.728 |
| set_name | `aecp.set_name.if1` | 30,090 | 0.301 | 20 | 24 | fits | 50,162 | 25 | 0.769 |
| lock_entity | `aecp.lock_entity.if1` | 25,397 | 0.254 | 20 | 24 | fits | 42,274 | 50 | 0.709 |
| unlock_entity | `aecp.unlock_entity.if1` | 42,858 | 0.429 | 20 | 24 | fits | 42,131 | 49 | 0.707 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
