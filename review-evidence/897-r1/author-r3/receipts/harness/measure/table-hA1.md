### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 62 paths and 7 of 66 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.181 (0.388) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.092 (0.221) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.103 (0.238) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.092 (0.221) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.094 (0.228) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.102 (0.249) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.090 (0.309) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.128 (0.387) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.151 (0.434) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.151 (0.445) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.204 (0.491) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.200 (0.494) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.177 (0.473) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.268 (0.607) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.113 (0.399) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.269 (0.565) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.173 (0.462) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.173 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.218 (0.509) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.196 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.217 (0.507) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.219 (0.509) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.223 (0.515) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.171 (0.458) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.229 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.172 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.231 (0.524) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.178 (0.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.225 (0.516) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.149 (0.443) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.222 (0.610) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.175 (0.465) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.217 (0.573) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 2.037 (2.324) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.443 (0.729) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.585 (0.873) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.472 (0.762) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.530 (0.793) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.484 (0.790) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.367 (2.663) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.497 (0.759) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.435 (1.723) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.412 (1.752) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.816 (3.148) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.441 (2.784) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.355 (1.494) | fits | 0 aecp | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.864 (63.134) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.560 (63.830) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.503 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.024 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.546 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 2.407 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.539 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.779 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.528 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.392 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 3.300 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.296 | fits | 31 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.975 (1.087) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.439 (0.440) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.202 (0.202) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.886 (0.963) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 64.152 | 25 | 145,391 (1.454) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 145,391 CPU cycles (1.454 ms), backlog-owed.
Over the windows that released their whole load only: 145,391 (1.454 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp | 290 | 0 | 69,269 (0.693) | fits |
| backlog-owed | 310 | 0 | 145,391 (1.454) | fits |
| aecp-fanout | 112 | 0 | 65,168 (0.652) | fits |
| acmp-cmd | 87 | 0 | 41,876 (0.419) | fits |
| aecp | 112 | 0 | 43,558 (0.436) | fits |
| aecp-largest-notice | 106 | 0 | 149,429 (1.494) | fits |
| datapath-events | 119 | 0 | 41,876 (0.419) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp | 271 | 20,970 (0.210) | 2,021 (0.020) |
| backlog-owed | 276 | 20,970 (0.210) | 2,162 (0.022) |
| aecp-fanout | 80 | 20,968 (0.210) | 2,021 (0.020) |
| acmp-cmd | 65 | 20,968 (0.210) | 2,021 (0.020) |
| aecp | 79 | 20,968 (0.210) | 2,021 (0.020) |
| aecp-largest-notice | 78 | 20,968 (0.210) | 2,021 (0.020) |
| datapath-events | 70 | 20,968 (0.210) | 2,021 (0.020) |

Longest pass that carries a step: 20,970 CPU cycles (0.210 ms), srp; longest step: 2,162 (0.022 ms), backlog-owed.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,578 | 0.886 | 20 | 20 | fits | 28,192 | 8 | 0.833 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 43,904 | 0.439 | 20 | 20 | fits | 43,970 | 12 | 0.883 |
| malformed MRPDU discard | `srp.malformed.if0` | 20,162 | 0.202 | 20 | 20 | fits | 20,228 | 12 | 0.632 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 97,464 | 0.975 | 220 | 220 | fits | 69,269 | 6 | 0.876 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,286,397 | 62.864 | 20 | 20 | MISS ceiling | 17,553 | 13 | 0.630 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,303,867 | 63.039 | 20 | 20 | MISS ceiling | 17,546 | 13 | 0.637 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,321,267 | 63.213 | 20 | 20 | MISS ceiling | 17,457 | 13 | 0.646 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,338,638 | 63.386 | 20 | 20 | MISS ceiling | 17,447 | 13 | 0.646 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,356,018 | 63.560 | 20 | 20 | MISS ceiling | 17,389 | 13 | 0.641 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,588 | 1.546 | 20 | 200 | fits | 145,391 | 204 | 0.420 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 240,725 | 2.407 | 20 | 200 | fits | 86,753 | 179 | 0.388 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 150,266 | 1.503 | 20 | 20 | fits | 145,391 | 204 | 0.420 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,202,416 | 62.024 | 20 | 20 | MISS ceiling | 28,001 | 15 | 0.746 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 153,906 | 1.539 | 20 | 24 | fits | 145,391 | 204 | 0.420 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,177,901 | 61.779 | 20 | 24 | MISS ceiling | 135,965 | 106 | 0.412 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 152,850 | 1.528 | 20 | 50 | fits | 145,391 | 204 | 0.420 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 239,207 | 2.392 | 20 | 50 | fits | 86,753 | 179 | 0.388 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 330,026 | 3.300 | 20 | 20 | fits | 90,885 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 729,638 | 7.296 | 20 | 20 | fits | 63,836 | 24 | 0.609 |
| set_name | `aecp_fanout.set_name.if0` | 48,412 | 0.484 | 20 | 24 | fits | 62,106 | 88 | 0.570 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 47,180 | 0.472 | 20 | 24 | fits | 55,144 | 77 | 0.591 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 53,050 | 0.530 | 20 | 24 | fits | 53,850 | 78 | 0.567 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 40,526 | 0.405 | 20 | 24 | fits | 49,411 | 77 | 0.535 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 58,536 | 0.585 | 20 | 24 | fits | 65,168 | 66 | 0.630 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 203,722 | 2.037 | 20 | 24 | fits | 60,074 | 65 | 0.627 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 236,693 | 2.367 | 20 | 24 | fits | 59,636 | 73 | 0.606 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 44,312 | 0.443 | 20 | 24 | fits | 49,963 | 77 | 0.553 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 49,731 | 0.497 | 20 | 24 | fits | 49,444 | 78 | 0.541 |
| BIND_RX | `acmp.bind_rx.if0` | 18,124 | 0.181 | 20 | 20 | fits | 38,775 | 26 (77) | 0.791 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,991 | 0.090 | 20 | 20 | fits | 30,923 | 19 (32) | 0.833 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,271 | 0.103 | 20 | 20 | fits | 23,787 | 15 (47) | 0.765 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,828 | 0.128 | 20 | 20 | fits | 38,728 | 18 (50) | 0.843 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,196 | 0.102 | 20 | 20 | fits | 24,888 | 17 (48) | 0.767 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,372 | 0.094 | 20 | 20 | fits | 22,833 | 16 (48) | 0.714 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,174 | 0.092 | 20 | 20 | fits | 22,123 | 16 (48) | 0.708 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 9,203 | 0.092 | 20 | 20 | fits | 22,104 | 16 (48) | 0.708 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,880 | 0.149 | 20 | 24 | fits | 27,007 | 20 | 0.789 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 26,903 | 0.269 | 20 | 24 | fits | 30,322 | 20 | 0.709 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 17,328 | 0.173 | 20 | 24 | fits | 25,502 | 20 | 0.722 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 22,269 | 0.223 | 20 | 24 | fits | 25,481 | 20 | 0.721 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 23,113 | 0.231 | 20 | 24 | fits | 26,239 | 20 | 0.726 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,847 | 0.178 | 20 | 24 | fits | 25,942 | 20 | 0.718 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 22,545 | 0.225 | 20 | 24 | fits | 25,130 | 20 | 0.724 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 17,305 | 0.173 | 20 | 24 | fits | 25,400 | 20 | 0.735 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,838 | 0.218 | 20 | 24 | fits | 24,734 | 20 | 0.738 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,560 | 0.196 | 20 | 24 | fits | 27,610 | 21 | 0.638 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 21,700 | 0.217 | 20 | 24 | fits | 24,391 | 20 | 0.755 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 21,882 | 0.219 | 20 | 24 | fits | 24,679 | 20 | 0.755 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 17,063 | 0.171 | 20 | 24 | fits | 25,113 | 20 | 0.721 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 22,899 | 0.229 | 20 | 24 | fits | 26,248 | 20 | 0.730 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 17,182 | 0.172 | 20 | 24 | fits | 25,440 | 20 | 0.735 |
| get_configuration | `aecp.get_configuration.if0` | 20,354 | 0.204 | 20 | 24 | fits | 22,942 | 20 | 0.743 |
| entity_available | `aecp.entity_available.if0` | 15,114 | 0.151 | 20 | 24 | fits | 22,745 | 20 | 0.728 |
| get_name | `aecp.get_name.if0` | 17,710 | 0.177 | 20 | 24 | fits | 26,166 | 20 | 0.760 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 19,960 | 0.200 | 20 | 24 | fits | 27,025 | 27 | 0.728 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 15,123 | 0.151 | 20 | 24 | fits | 27,362 | 29 | 0.752 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 17,467 | 0.175 | 20 | 24 | fits | 23,771 | 20 | 0.759 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 11,347 | 0.113 | 20 | 24 | fits | 22,806 | 20 | 0.733 |
| set_name | `aecp.set_name.if0` | 22,223 | 0.222 | 20 | 24 | fits | 43,558 | 42 | 0.763 |
| lock_entity | `aecp.lock_entity.if0` | 26,842 | 0.268 | 20 | 24 | fits | 34,268 | 33 | 0.776 |
| unlock_entity | `aecp.unlock_entity.if0` | 21,684 | 0.217 | 20 | 24 | fits | 33,658 | 32 | 0.767 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 135,523 | 1.355 | 20 | 24 | fits | 149,429 | 91 | 0.324 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 143,499 | 1.435 | 20 | 24 | fits | 139,314 | 69 | 0.301 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 141,223 | 1.412 | 20 | 24 | fits | 43,131 | 17 | 0.688 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 281,568 | 2.816 | 20 | 24 | fits | 93,782 | 18 | 0.670 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 244,081 | 2.441 | 20 | 24 | fits | 103,761 | 32 | 0.679 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
