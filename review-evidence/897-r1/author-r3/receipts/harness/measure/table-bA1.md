### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 62 paths and 7 of 66 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.180 (0.390) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.089 (0.223) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.097 (0.235) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.089 (0.223) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.090 (0.227) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.106 (0.248) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.095 (0.304) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.135 (0.385) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.145 (0.432) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.179 (0.471) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.196 (0.484) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.227 (0.519) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.171 (0.465) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.218 (0.560) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.145 (0.433) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.278 (0.574) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.168 (0.461) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.168 (0.460) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.212 (0.504) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.191 (0.482) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.211 (0.503) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.210 (0.502) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.216 (0.510) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.165 (0.457) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.222 (0.518) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.166 (0.459) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.223 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.173 (0.466) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.218 (0.511) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.160 (0.457) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.250 (0.636) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.190 (0.481) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.210 (0.563) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 1.586 (1.874) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.443 (0.731) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.653 (0.941) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.464 (0.798) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.558 (0.822) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.608 (0.815) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 2.368 (2.666) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.528 (0.791) | fits | 0 aecp | 1 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 2.091 (2.397) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.292 (1.631) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.905 (3.237) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.381 (2.713) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.476 (1.684) | fits | 0 aecp | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.928 (63.114) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.638 (63.826) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.209 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.071 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.252 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 1.246 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 2.217 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.538 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.235 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 1.231 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 3.010 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 7.223 | fits | 31 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.974 (1.088) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.440 (0.441) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.206 (0.207) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.888 (0.961) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 64.236 | 25 | 136,975 (1.370) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 136,975 CPU cycles (1.370 ms), backlog-owed.
Over the windows that released their whole load only: 136,975 (1.370 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp | 289 | 0 | 68,937 (0.689) | fits |
| backlog-owed | 310 | 0 | 136,975 (1.370) | fits |
| aecp-fanout | 111 | 0 | 65,333 (0.653) | fits |
| acmp-cmd | 86 | 0 | 41,869 (0.419) | fits |
| aecp | 111 | 0 | 43,739 (0.437) | fits |
| aecp-largest-notice | 106 | 0 | 149,490 (1.495) | fits |
| datapath-events | 117 | 0 | 41,869 (0.419) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp | 271 | 20,887 (0.209) | 2,201 (0.022) |
| backlog-owed | 276 | 20,887 (0.209) | 2,481 (0.025) |
| aecp-fanout | 80 | 21,918 (0.219) | 3,231 (0.032) |
| acmp-cmd | 65 | 20,878 (0.209) | 2,140 (0.021) |
| aecp | 79 | 20,878 (0.209) | 2,140 (0.021) |
| aecp-largest-notice | 78 | 20,878 (0.209) | 2,140 (0.021) |
| datapath-events | 70 | 20,878 (0.209) | 2,140 (0.021) |

Longest pass that carries a step: 21,918 CPU cycles (0.219 ms), aecp-fanout; longest step: 3,231 (0.032 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,777 | 0.888 | 20 | 20 | fits | 28,004 | 8 | 0.815 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,010 | 0.440 | 20 | 20 | fits | 44,076 | 12 | 0.884 |
| malformed MRPDU discard | `srp.malformed.if0` | 20,586 | 0.206 | 20 | 20 | fits | 20,652 | 12 | 0.671 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 97,402 | 0.974 | 220 | 220 | fits | 68,937 | 6 | 0.874 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,292,765 | 62.928 | 20 | 20 | MISS ceiling | 17,857 | 13 | 0.643 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,310,536 | 63.105 | 20 | 20 | MISS ceiling | 17,927 | 13 | 0.655 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,328,320 | 63.283 | 20 | 20 | MISS ceiling | 17,761 | 13 | 0.658 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,346,006 | 63.460 | 20 | 20 | MISS ceiling | 17,842 | 13 | 0.663 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,363,762 | 63.638 | 20 | 20 | MISS ceiling | 17,665 | 13 | 0.654 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 125,243 | 1.252 | 20 | 200 | fits | 126,638 | 239 | 0.337 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 124,627 | 1.246 | 20 | 200 | fits | 126,638 | 239 | 0.337 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 120,921 | 1.209 | 20 | 20 | fits | 126,638 | 239 | 0.337 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,207,102 | 62.071 | 20 | 20 | MISS ceiling | 28,056 | 15 | 0.747 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 221,713 | 2.217 | 20 | 24 | fits | 97,152 | 107 | 0.435 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,153,849 | 61.538 | 20 | 24 | MISS ceiling | 136,975 | 107 | 0.380 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 123,505 | 1.235 | 20 | 50 | fits | 126,638 | 239 | 0.337 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 123,109 | 1.231 | 20 | 50 | fits | 126,638 | 239 | 0.337 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 301,006 | 3.010 | 20 | 20 | fits | 80,811 | 62 | 0.724 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 722,319 | 7.223 | 20 | 20 | fits | 85,253 | 32 | 0.529 |
| set_name | `aecp_fanout.set_name.if0` | 60,772 | 0.608 | 20 | 24 | fits | 62,587 | 88 | 0.561 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 46,441 | 0.464 | 20 | 24 | fits | 53,596 | 77 | 0.562 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 55,846 | 0.558 | 20 | 24 | fits | 53,316 | 78 | 0.553 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 47,034 | 0.470 | 20 | 24 | fits | 49,134 | 77 | 0.525 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 65,298 | 0.653 | 20 | 24 | fits | 65,333 | 66 | 0.630 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 158,645 | 1.586 | 20 | 24 | fits | 60,381 | 65 | 0.629 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 236,775 | 2.368 | 20 | 24 | fits | 58,938 | 73 | 0.591 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 44,271 | 0.443 | 20 | 24 | fits | 49,399 | 77 | 0.541 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 52,751 | 0.528 | 20 | 24 | fits | 49,030 | 78 | 0.529 |
| BIND_RX | `acmp.bind_rx.if0` | 18,005 | 0.180 | 20 | 20 | fits | 38,982 | 26 (77) | 0.791 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,501 | 0.095 | 20 | 20 | fits | 30,429 | 19 (32) | 0.824 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 9,708 | 0.097 | 20 | 20 | fits | 23,533 | 15 (47) | 0.755 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,548 | 0.135 | 20 | 20 | fits | 38,498 | 18 (50) | 0.840 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,639 | 0.106 | 20 | 20 | fits | 24,786 | 17 (48) | 0.762 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 8,984 | 0.090 | 20 | 20 | fits | 22,720 | 16 (48) | 0.708 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 8,865 | 0.089 | 20 | 20 | fits | 22,340 | 16 (48) | 0.705 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,889 | 0.089 | 20 | 20 | fits | 22,321 | 16 (48) | 0.705 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 15,956 | 0.160 | 20 | 24 | fits | 27,503 | 20 | 0.788 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 27,771 | 0.278 | 20 | 24 | fits | 30,797 | 20 | 0.706 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 16,818 | 0.168 | 20 | 24 | fits | 26,303 | 20 | 0.727 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 21,607 | 0.216 | 20 | 24 | fits | 26,189 | 20 | 0.723 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 22,298 | 0.223 | 20 | 24 | fits | 26,926 | 20 | 0.727 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 17,335 | 0.173 | 20 | 24 | fits | 26,741 | 20 | 0.721 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 21,805 | 0.218 | 20 | 24 | fits | 25,882 | 20 | 0.727 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 16,793 | 0.168 | 20 | 24 | fits | 26,199 | 20 | 0.738 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 21,155 | 0.212 | 20 | 24 | fits | 25,421 | 20 | 0.740 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,148 | 0.191 | 20 | 24 | fits | 28,430 | 21 | 0.642 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 21,053 | 0.211 | 20 | 24 | fits | 25,240 | 20 | 0.759 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 21,041 | 0.210 | 20 | 24 | fits | 25,466 | 20 | 0.758 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 16,546 | 0.165 | 20 | 24 | fits | 25,907 | 20 | 0.725 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 22,230 | 0.222 | 20 | 24 | fits | 26,949 | 20 | 0.731 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 16,600 | 0.166 | 20 | 24 | fits | 26,098 | 20 | 0.738 |
| get_configuration | `aecp.get_configuration.if0` | 19,630 | 0.196 | 20 | 24 | fits | 23,546 | 20 | 0.737 |
| entity_available | `aecp.entity_available.if0` | 14,498 | 0.145 | 20 | 24 | fits | 23,272 | 20 | 0.722 |
| get_name | `aecp.get_name.if0` | 17,098 | 0.171 | 20 | 24 | fits | 26,534 | 20 | 0.751 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 22,686 | 0.227 | 20 | 24 | fits | 27,146 | 27 | 0.717 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 17,852 | 0.179 | 20 | 24 | fits | 27,239 | 29 | 0.742 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 18,966 | 0.190 | 20 | 24 | fits | 24,303 | 20 | 0.758 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,530 | 0.145 | 20 | 24 | fits | 23,492 | 20 | 0.732 |
| set_name | `aecp.set_name.if0` | 25,040 | 0.250 | 20 | 24 | fits | 43,739 | 42 | 0.754 |
| lock_entity | `aecp.lock_entity.if0` | 21,835 | 0.218 | 20 | 24 | fits | 34,040 | 33 | 0.765 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,980 | 0.210 | 20 | 24 | fits | 34,154 | 32 | 0.751 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 147,571 | 1.476 | 20 | 24 | fits | 149,490 | 91 | 0.312 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 209,133 | 2.091 | 20 | 24 | fits | 138,064 | 69 | 0.294 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 129,228 | 1.292 | 20 | 24 | fits | 42,487 | 17 | 0.679 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 290,539 | 2.905 | 20 | 24 | fits | 93,346 | 18 | 0.660 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 238,059 | 2.381 | 20 | 24 | fits | 95,503 | 17 | 0.674 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
