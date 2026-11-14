### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 86 paths and 7 of 91 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.205 (0.495) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.179 (0.466) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.093 (0.300) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.087 (0.302) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.107 (0.319) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.113 (0.330) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.086 (0.300) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.099 (0.312) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.101 (0.310) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.101 (0.311) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.109 (0.331) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.110 (0.331) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.097 (0.376) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.108 (0.385) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.138 (0.450) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.140 (0.481) | fits | 0 acmp | 1 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.169 (0.602) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.282 (0.728) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.328 (0.768) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 1 | `aecp.get_avb_info.if1` (aecp) | 0.312 (0.760) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.259 (0.704) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.189 (0.622) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.203 (0.645) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 1 | `aecp.get_counters.if1` (aecp) | 0.224 (0.665) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.281 (0.732) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.300 (0.752) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.442 (0.816) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.370 (0.774) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.163 (0.598) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.278 (0.724) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.325 (0.777) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.241 (0.681) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.289 (0.739) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.216 (0.668) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.279 (0.727) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.186 (0.624) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.328 (0.783) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.277 (0.727) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.182 (0.622) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.192 (0.631) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.304 (0.754) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.281 (0.730) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.197 (0.636) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.289 (0.741) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.282 (0.734) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.199 (0.636) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.187 (0.636) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.169 (0.618) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.270 (0.722) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.520 (0.973) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.501 (0.921) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.261 (0.711) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 1 | `aecp.unknown_command.if1` (aecp) | 0.188 (0.626) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.350 (0.719) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.468 (0.847) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.651 (1.070) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.648 (1.063) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.594 (1.037) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.684 (1.124) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.651 (1.068) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.557 (0.975) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.666 (1.152) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.619 (1.072) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.574 (1.015) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.563 (0.979) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.563 (0.978) | fits | 0 aecp | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.572 (63.843) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 64.596 (64.869) | MISS ceiling | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.462 | fits | 0 acmp | 1 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.288 | MISS ceiling | 11 acmp | 1 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.505 | fits | 0 adp | 1 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 1.499 | fits | 7 adp | 1 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 2.767 | fits | 0 aecp | 1 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.959 | MISS ceiling | 15 aecp | 1 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.488 | fits | 0 maap | 1 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 2.752 | fits | 6 maap | 1 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.350 | fits | 0 srp | 1 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-owed.service.srp.last.if1` (backlog-owed) | 8.602 | fits | 31 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.741 (1.907) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.812 (2.010) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.564 (0.564) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.552 (0.552) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.286 (0.287) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.290 (0.291) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.466 (1.534) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.488 (1.550) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-owed | 0 | 65.516 | 24 | 153,459 (1.535) | yes | - |

Composed maximum over 1 of 4 backlog windows, a partial figure (backlog, backlog-adp, backlog-adp-refill not run): 153,459 CPU cycles (1.535 ms), backlog-owed.
Over the windows that released their whole load only: 153,459 (1.535 ms), backlog-owed.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| srp | 316 | 0 | 149,156 (1.492) | fits |
| backlog-owed | 319 | 0 | 153,459 (1.535) | fits |
| aecp-fanout | 151 | 0 | 89,845 (0.898) | fits |
| acmp-cmd | 112 | 0 | 89,845 (0.898) | fits |
| aecp | 141 | 0 | 89,845 (0.898) | fits |
| datapath-events | 156 | 0 | 89,845 (0.898) | fits |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| srp | 278 | 34,212 (0.342) | 2,651 (0.027) |
| backlog-owed | 277 | 32,545 (0.325) | 2,651 (0.027) |
| aecp-fanout | 94 | 32,470 (0.325) | 2,931 (0.029) |
| acmp-cmd | 67 | 32,470 (0.325) | 2,651 (0.027) |
| aecp | 89 | 32,470 (0.325) | 2,651 (0.027) |
| datapath-events | 75 | 32,470 (0.325) | 2,651 (0.027) |

Longest pass that carries a step: 34,212 CPU cycles (0.342 ms), srp; longest step: 2,931 (0.029 ms), aecp-fanout.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| startup declarations (LINK_UP) | `srp.startup.if0` | 146,641 | 1.466 | 20 | 20 | fits | 26,826 | 8 | 0.794 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 148,762 | 1.488 | 20 | 20 | fits | 26,713 | 8 | 0.808 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 56,351 | 0.564 | 20 | 20 | fits | 56,417 | 13 | 0.887 |
| malformed MRPDU discard | `srp.malformed.if0` | 28,604 | 0.286 | 20 | 20 | fits | 28,670 | 13 | 0.733 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 174,124 | 1.741 | 220 | 220 | fits | 138,998 | 7 | 0.795 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 55,168 | 0.552 | 20 | 20 | fits | 55,234 | 13 | 0.879 |
| malformed MRPDU discard | `srp.malformed.if1` | 29,011 | 0.290 | 20 | 20 | fits | 29,077 | 13 | 0.736 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 181,239 | 1.812 | 220 | 220 | fits | 149,156 | 6 | 0.788 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,357,215 | 63.572 | 20 | 20 | MISS ceiling | 25,754 | 14 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,382,869 | 63.829 | 20 | 20 | MISS ceiling | 25,730 | 14 | 0.603 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,408,441 | 64.084 | 20 | 20 | MISS ceiling | 25,708 | 14 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,434,076 | 64.341 | 20 | 20 | MISS ceiling | 25,632 | 14 | 0.610 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,459,585 | 64.596 | 20 | 20 | MISS ceiling | 25,572 | 14 | 0.618 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 150,493 | 1.505 | 20 | 200 | fits | 152,764 | 210 | 0.364 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 149,877 | 1.499 | 20 | 200 | fits | 152,764 | 210 | 0.364 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 146,171 | 1.462 | 20 | 20 | fits | 152,764 | 210 | 0.364 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,228,839 | 62.288 | 20 | 20 | MISS ceiling | 36,386 | 16 | 0.700 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 276,698 | 2.767 | 20 | 24 | fits | 126,887 | 146 | 0.466 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,195,939 | 61.959 | 20 | 24 | MISS ceiling | 153,459 | 117 | 0.396 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 148,755 | 1.488 | 20 | 50 | fits | 152,764 | 210 | 0.364 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 275,246 | 2.752 | 20 | 50 | fits | 126,887 | 146 | 0.466 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 435,030 | 4.350 | 20 | 20 | fits | 121,112 | 29 | 0.738 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 860,244 | 8.602 | 20 | 20 | fits | 65,104 | 21 | 0.668 |
| set_name | `aecp_fanout.set_name.if0` | 66,628 | 0.666 | 20 | 24 | fits | 84,760 | 161 | 0.433 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 59,431 | 0.594 | 20 | 24 | fits | 72,104 | 140 | 0.455 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 65,149 | 0.651 | 20 | 24 | fits | 66,565 | 140 | 0.409 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 55,468 | 0.555 | 20 | 24 | fits | 65,426 | 140 | 0.387 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 57,402 | 0.574 | 20 | 24 | fits | 69,550 | 116 | 0.435 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 65,147 | 0.651 | 20 | 24 | fits | 66,820 | 140 | 0.415 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 56,298 | 0.563 | 20 | 24 | fits | 65,807 | 140 | 0.395 |
| set_name | `aecp_fanout.set_name.if1` | 61,858 | 0.619 | 20 | 24 | fits | 75,495 | 117 | 0.415 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 68,357 | 0.684 | 20 | 24 | fits | 71,923 | 140 | 0.453 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 55,604 | 0.556 | 20 | 24 | fits | 65,678 | 140 | 0.395 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 55,711 | 0.557 | 20 | 24 | fits | 65,669 | 140 | 0.394 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 64,760 | 0.648 | 20 | 24 | fits | 66,132 | 140 | 0.403 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 56,298 | 0.563 | 20 | 24 | fits | 65,807 | 140 | 0.395 |
| BIND_RX | `acmp.bind_rx.if0` | 20,523 | 0.205 | 20 | 20 | fits | 49,481 | 27 (77) | 0.789 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,749 | 0.097 | 20 | 20 | fits | 37,618 | 20 (32) | 0.833 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,669 | 0.107 | 20 | 20 | fits | 31,896 | 16 (47) | 0.758 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,804 | 0.138 | 20 | 20 | fits | 45,036 | 19 (50) | 0.827 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,937 | 0.109 | 20 | 20 | fits | 33,082 | 18 (48) | 0.764 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,098 | 0.101 | 20 | 20 | fits | 31,028 | 17 (48) | 0.715 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,280 | 0.093 | 20 | 20 | fits | 30,030 | 17 (48) | 0.697 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,646 | 0.086 | 20 | 20 | fits | 30,011 | 17 (48) | 0.697 |
| BIND_RX | `acmp.bind_rx.if1` | 17,904 | 0.179 | 20 | 20 | fits | 46,617 | 28 (77) | 0.754 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 10,770 | 0.108 | 20 | 20 | fits | 38,460 | 21 (32) | 0.830 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 11,318 | 0.113 | 20 | 20 | fits | 32,983 | 17 (47) | 0.769 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 14,038 | 0.140 | 20 | 20 | fits | 48,103 | 20 (50) | 0.828 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if1` | 11,045 | 0.110 | 20 | 20 | fits | 33,135 | 20 (48) | 0.752 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 10,143 | 0.101 | 20 | 20 | fits | 31,123 | 18 (48) | 0.705 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 8,723 | 0.087 | 20 | 20 | fits | 30,207 | 18 (48) | 0.691 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if1` | 9,859 | 0.099 | 20 | 20 | fits | 31,224 | 18 (48) | 0.731 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 16,919 | 0.169 | 20 | 24 | fits | 33,848 | 22 | 0.777 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 32,523 | 0.325 | 20 | 24 | fits | 38,097 | 22 | 0.700 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 28,864 | 0.289 | 20 | 24 | fits | 34,286 | 22 | 0.727 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 19,182 | 0.192 | 20 | 24 | fits | 33,344 | 22 | 0.695 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 28,240 | 0.282 | 20 | 24 | fits | 33,791 | 22 | 0.711 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 19,862 | 0.199 | 20 | 24 | fits | 34,074 | 22 | 0.705 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 18,697 | 0.187 | 20 | 24 | fits | 32,952 | 22 | 0.715 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 27,900 | 0.279 | 20 | 24 | fits | 32,909 | 22 | 0.724 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 18,644 | 0.186 | 20 | 24 | fits | 32,868 | 22 | 0.719 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 32,753 | 0.328 | 20 | 24 | fits | 38,525 | 23 | 0.642 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 27,746 | 0.277 | 20 | 24 | fits | 33,018 | 22 | 0.753 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 18,196 | 0.182 | 20 | 24 | fits | 32,467 | 22 | 0.738 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 28,145 | 0.281 | 20 | 24 | fits | 33,329 | 22 | 0.720 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 19,687 | 0.197 | 20 | 24 | fits | 33,990 | 22 | 0.710 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 28,882 | 0.289 | 20 | 24 | fits | 34,479 | 22 | 0.726 |
| get_configuration | `aecp.get_configuration.if0` | 25,885 | 0.259 | 20 | 24 | fits | 30,908 | 22 | 0.740 |
| entity_available | `aecp.entity_available.if0` | 16,858 | 0.169 | 20 | 24 | fits | 30,665 | 22 | 0.725 |
| get_name | `aecp.get_name.if0` | 28,097 | 0.281 | 20 | 24 | fits | 33,744 | 22 | 0.746 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 20,329 | 0.203 | 20 | 24 | fits | 34,674 | 28 | 0.711 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 32,809 | 0.328 | 20 | 24 | fits | 34,993 | 30 | 0.758 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 26,131 | 0.261 | 20 | 24 | fits | 31,110 | 22 | 0.742 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 16,272 | 0.163 | 20 | 24 | fits | 30,233 | 22 | 0.723 |
| set_name | `aecp.set_name.if0` | 51,997 | 0.520 | 20 | 24 | fits | 58,008 | 66 | 0.712 |
| lock_entity | `aecp.lock_entity.if0` | 44,200 | 0.442 | 20 | 24 | fits | 41,804 | 47 | 0.747 |
| unlock_entity | `aecp.unlock_entity.if0` | 35,014 | 0.350 | 20 | 24 | fits | 40,742 | 46 | 0.734 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 27,008 | 0.270 | 20 | 24 | fits | 33,041 | 20 | 0.766 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 24,086 | 0.241 | 20 | 24 | fits | 36,171 | 20 | 0.686 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 21,631 | 0.216 | 20 | 24 | fits | 33,909 | 20 | 0.731 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 30,440 | 0.304 | 20 | 24 | fits | 33,483 | 20 | 0.716 |
| get_configuration | `aecp.get_configuration.if1` | 18,864 | 0.189 | 20 | 24 | fits | 30,408 | 20 | 0.736 |
| entity_available | `aecp.entity_available.if1` | 28,215 | 0.282 | 20 | 24 | fits | 30,880 | 20 | 0.743 |
| get_name | `aecp.get_name.if1` | 30,020 | 0.300 | 20 | 24 | fits | 33,505 | 20 | 0.750 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if1` | 22,358 | 0.224 | 20 | 24 | fits | 34,387 | 26 | 0.716 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if1` | 31,180 | 0.312 | 20 | 24 | fits | 34,208 | 29 | 0.750 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if1` | 18,774 | 0.188 | 20 | 24 | fits | 30,659 | 20 | 0.739 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 27,824 | 0.278 | 20 | 24 | fits | 30,299 | 20 | 0.738 |
| set_name | `aecp.set_name.if1` | 50,133 | 0.501 | 20 | 24 | fits | 50,475 | 25 | 0.759 |
| lock_entity | `aecp.lock_entity.if1` | 36,991 | 0.370 | 20 | 24 | fits | 42,051 | 50 | 0.720 |
| unlock_entity | `aecp.unlock_entity.if1` | 46,821 | 0.468 | 20 | 24 | fits | 41,894 | 49 | 0.720 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
