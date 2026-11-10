### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 129 paths and 6 of 182 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.289 (0.665) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.251 (0.601) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.130 (0.455) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.131 (0.446) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.086 (0.661) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.291 (0.661) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.079 (0.631) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.273 (0.631) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.150 (0.482) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.148 (0.484) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.123 (0.443) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.118 (0.444) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.168 (0.502) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.142 (0.471) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.142 (0.472) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.154 (0.496) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.106 (0.459) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.105 (0.457) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.484 (1.810) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.165 (0.732) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.205 (0.780) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.187 (0.749) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.157 (1.006) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.432 (1.006) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.260 (0.923) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.479 (0.923) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.322 (0.866) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.107 (0.756) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.228 (0.912) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.445 (0.912) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.184 (0.576) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.189 (0.586) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.044 (0.249) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.058 (0.249) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.210) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.043 (0.210) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.024 (0.722) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.333 (0.722) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.027 (0.458) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.176 (0.458) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.169 (0.380) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.146 (0.380) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.319 (0.714) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.230 (0.714) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.196 (0.578) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.133 (0.498) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.206 (0.600) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.144 (0.536) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.106 (0.274) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.222 (0.599) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.145 (0.328) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.252 (0.659) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.131 (0.308) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.243 (0.630) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.242 (0.393) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.389 (0.770) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.195 (0.570) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.129 (0.492) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.266 (0.652) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.273 (0.658) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.219 (0.427) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.232 (0.572) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.125 (0.295) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.128 (0.305) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.260 (0.649) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.122 (0.297) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.210 (0.597) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.133 (0.305) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.155 (0.543) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.124 (0.298) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.133 (0.313) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.220 (0.612) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.218 (0.603) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.137 (0.309) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.213 (0.596) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.126 (0.301) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.121 (0.291) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.436 (0.630) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.400 (0.786) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.119 (0.289) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.229 (0.611) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.341 (0.701) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.272 (0.662) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.560 (0.947) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.560 (0.947) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.737 (1.148) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.591 (0.988) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.561 (0.945) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.707 (1.097) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.689 (1.116) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.794 (1.211) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.717 (1.118) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.601 (0.785) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.712 (1.101) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 9.703 (10.794) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 8.015 (9.680) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.200 (0.753) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.973 (3.165) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 64.093 (64.629) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.417 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.177 (0.590) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.164 (0.385) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.131 (0.289) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.123 (0.293) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.147 (0.337) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.139 (0.330) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.158 (0.590) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.145 (0.385) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.214 (0.606) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.227 (0.623) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.815 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 11.134 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.858 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 9.627 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 9.641 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.851 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 62.115 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.841 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 11.164 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 6.015 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-owed.service.srp.last.if1` (backlog-owed) | 8.036 | fits | 31 srp | 4 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.953 (2.413) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.653 (2.076) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.603 (0.604) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.547 (0.548) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.248 (0.249) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.249 (0.250) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.460 (1.531) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.377 (1.440) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 11.412 | 8 | 185,989 (1.860) | yes | - |
| backlog-adp | 0 | 13.578 | 11 | 173,260 (1.733) | yes | - |
| backlog-adp-refill | 0 | 41.165 | 22 | 163,648 (1.636) | yes | - |
| backlog-owed | 0 | 360.467 | 52 | 172,592 (1.726) | yes | - |

Composed maximum over the 4 backlog windows: 185,989 CPU cycles (1.860 ms), backlog.
Over the windows that released their whole load only: 185,989 (1.860 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 4874 | 0 | 119,264 (1.193) | fits |
| adp-advertise | 599 | 0 | 119,264 (1.193) | fits |
| maap | 366 | 0 | 119,361 (1.194) | fits |
| acmp-noresp | 3247 | 0 | 119,264 (1.193) | fits |
| save | 611 | 0 | 119,264 (1.193) | fits |
| srp | 306 | 0 | 188,655 (1.887) | fits |
| backlog | 288 | 0 | 185,989 (1.860) | fits |
| backlog-adp | 316 | 0 | 173,260 (1.733) | fits |
| backlog-adp-refill | 327 | 0 | 163,648 (1.636) | fits |
| backlog-owed | 339 | 0 | 172,592 (1.726) | fits |
| acmp-disc | 1390 | 0 | 119,275 (1.193) | fits |
| adp-link | 91 | 0 | 119,264 (1.193) | fits |
| adp-gm | 89 | 0 | 119,264 (1.193) | fits |
| adp-discover | 89 | 0 | 119,264 (1.193) | fits |
| control | 89 | 0 | 119,264 (1.193) | fits |
| aecp-fanout | 140 | 0 | 119,264 (1.193) | fits |
| acmp-cmd | 106 | 0 | 119,264 (1.193) | fits |
| aecp | 132 | 0 | 119,264 (1.193) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 4697.759 | 12,110 | 370 | - | 13.341 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 108,851 (1.089) | 78,626 (0.786) |
| adp-advertise | 577 | 30,844 (0.308) | 3,211 (0.032) |
| maap | 344 | 30,719 (0.307) | 3,211 (0.032) |
| acmp-noresp | 615 | 108,539 (1.085) | 78,626 (0.786) |
| save | 585 | 107,618 (1.076) | 78,641 (0.786) |
| srp | 278 | 30,811 (0.308) | 3,360 (0.034) |
| backlog | 266 | 30,844 (0.308) | 3,489 (0.035) |
| backlog-adp | 272 | 30,844 (0.308) | 3,260 (0.033) |
| backlog-adp-refill | 274 | 30,844 (0.308) | 3,260 (0.033) |
| backlog-owed | 306 | 39,187 (0.392) | 3,502 (0.035) |
| acmp-disc | 336 | 105,557 (1.056) | 78,331 (0.783) |
| adp-link | 79 | 30,628 (0.306) | 3,211 (0.032) |
| adp-gm | 79 | 30,628 (0.306) | 3,211 (0.032) |
| adp-discover | 79 | 30,628 (0.306) | 3,211 (0.032) |
| control | 79 | 30,628 (0.306) | 3,211 (0.032) |
| aecp-fanout | 93 | 30,628 (0.306) | 3,211 (0.032) |
| acmp-cmd | 67 | 30,628 (0.306) | 3,211 (0.032) |
| aecp | 88 | 30,628 (0.306) | 3,914 (0.039) |

Longest pass that carries a step: 108,851 CPU cycles (1.089 ms), acmp-notk; longest step: 78,641 (0.786 ms), save.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 32,245 | 0.322 | 20 | 20 | fits | 54,092 | 29 (14) | 0.802 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 10,722 | 0.107 | 20 | 20 | fits | 53,699 | 19 (14) | 0.897 |
| LINK_UP | `adp.link_up.if0` | 2,742 | 0.027 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 17,626 | 0.176 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 31,877 | 0.319 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 22,973 | 0.230 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 16,927 | 0.169 | 20 | 200 | fits | 5,362 | 19 (11) | 0.553 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 14,557 | 0.146 | 20 | 200 | fits | 5,362 | 19 (11) | 0.553 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 14,664 | 0.147 | 20 | 50 | fits | 33,720 | 44 | 0.717 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 21,420 | 0.214 | 20 | 50 | fits | 30,986 | 36 | 0.717 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 20,028 | 0.200 | 20 | 50 | fits | 31,051 | 36 | 0.717 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 15,767 | 0.158 | 20 | 50 | fits | 37,094 | 62 | 0.641 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 17,722 | 0.177 | 20 | 50 | fits | 37,094 | 62 | 0.641 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 13,082 | 0.131 | 20 | 50 | fits | 28,860 | 31 | 0.632 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 13,924 | 0.139 | 20 | 50 | fits | 32,980 | 44 | 0.701 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 18,880 | 0.189 | 20 | 50 | fits | 31,616 | 37 | 0.714 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 22,692 | 0.227 | 20 | 50 | fits | 30,180 | 36 | 0.691 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 14,494 | 0.145 | 20 | 50 | fits | 38,456 | 62 | 0.658 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 16,449 | 0.164 | 20 | 50 | fits | 38,456 | 62 | 0.658 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 12,321 | 0.123 | 20 | 50 | fits | 29,307 | 31 | 0.632 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 15,741 | 0.157 | 20 | 20 | fits | 78,118 | 42 (35) | 0.744 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 43,196 | 0.432 | 20 | 20 | fits | 78,118 | 42 (35) | 0.744 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 25,993 | 0.260 | 20 | 20 | fits | 66,688 | 33 (14) | 0.808 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 47,935 | 0.479 | 20 | 20 | fits | 66,688 | 33 (14) | 0.808 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 22,750 | 0.228 | 20 | 20 | fits | 65,369 | 34 (14) | 0.802 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 44,507 | 0.445 | 20 | 20 | fits | 65,369 | 34 (14) | 0.802 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 48,416 | 0.484 | 20 | 20 | fits | 51,523 | 22 (35) | 0.820 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 16,518 | 0.165 | 20 | 20 | fits | 51,420 | 22 (35) | 0.819 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 146,044 | 1.460 | 20 | 20 | fits | 119,361 | 6 | 0.811 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 137,666 | 1.377 | 20 | 20 | fits | 110,223 | 6 | 0.742 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 60,290 | 0.603 | 20 | 20 | fits | 60,355 | 13 | 0.900 |
| malformed MRPDU discard | `srp.malformed.if0` | 24,801 | 0.248 | 20 | 20 | fits | 24,866 | 13 | 0.695 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 195,300 | 1.953 | 220 | 220 | fits | 188,655 | 10 | 0.800 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 54,702 | 0.547 | 20 | 20 | fits | 54,767 | 13 | 0.894 |
| malformed MRPDU discard | `srp.malformed.if1` | 24,894 | 0.249 | 20 | 20 | fits | 24,959 | 13 | 0.699 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 165,274 | 1.653 | 220 | 220 | fits | 159,647 | 9 | 0.794 |
| an event behind 15 others | `backlog.event.if0` | 197,320 | 1.973 | 20 | 200 | fits | 130,524 | 129 | 0.548 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 970,334 | 9.703 | 20 | 20 | fits | 142,763 | 106 | 0.479 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 185,781 | 1.858 | 20 | 200 | fits | 185,989 | 158 | 0.545 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 935,840 | 9.358 | 20 | 200 | fits | 175,084 | 75 | 0.587 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 181,522 | 1.815 | 20 | 20 | fits | 185,989 | 158 | 0.545 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,074,128 | 10.741 | 20 | 20 | fits | 142,763 | 106 | 0.479 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 185,107 | 1.851 | 20 | 24 | fits | 185,989 | 158 | 0.545 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,077,563 | 10.776 | 20 | 24 | fits | 142,763 | 106 | 0.479 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 184,067 | 1.841 | 20 | 50 | fits | 185,989 | 158 | 0.545 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 934,345 | 9.343 | 20 | 50 | fits | 175,084 | 75 | 0.587 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 601,543 | 6.015 | 20 | 20 | fits | 106,318 | 53 | 0.550 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 757,181 | 7.572 | 20 | 20 | fits | 74,990 | 43 | 0.527 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 801,503 | 8.015 | 20 | 20 | fits | 173,260 | 108 | 0.587 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 158,885 | 1.589 | 20 | 200 | fits | 163,567 | 155 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 962,722 | 9.627 | 20 | 200 | fits | 173,260 | 108 | 0.587 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 159,797 | 1.598 | 20 | 20 | fits | 163,567 | 155 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,113,372 | 11.134 | 20 | 20 | fits | 149,954 | 85 | 0.561 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 163,382 | 1.634 | 20 | 24 | fits | 163,567 | 155 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,244,514 | 12.445 | 20 | 24 | fits | 116,630 | 105 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 162,342 | 1.623 | 20 | 50 | fits | 163,567 | 155 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 1,116,352 | 11.164 | 20 | 50 | fits | 149,954 | 85 | 0.561 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 498,240 | 4.982 | 20 | 20 | fits | 163,648 | 43 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 791,058 | 7.911 | 20 | 20 | fits | 147,198 | 53 | 0.437 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 19,961 | 0.200 | 20 | 20 | fits | 44,293 | 20 | 0.795 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 158,885 | 1.589 | 20 | 200 | fits | 163,567 | 155 | 0.531 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 55,156 | 0.552 | 20 | 200 | fits | 44,293 | 20 | 0.795 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 159,797 | 1.598 | 20 | 20 | fits | 163,567 | 155 | 0.531 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,095,393 | 10.954 | 20 | 20 | fits | 151,326 | 86 | 0.558 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 163,382 | 1.634 | 20 | 24 | fits | 163,567 | 155 | 0.531 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,226,608 | 12.266 | 20 | 24 | fits | 116,604 | 105 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 162,342 | 1.623 | 20 | 50 | fits | 163,567 | 155 | 0.531 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 1,098,373 | 10.984 | 20 | 50 | fits | 151,326 | 86 | 0.558 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 498,240 | 4.982 | 20 | 20 | fits | 163,648 | 43 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 791,058 | 7.911 | 20 | 20 | fits | 147,198 | 53 | 0.437 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,409,338 | 64.093 | 20 | 20 | MISS ceiling | 36,915 | 13 | 0.699 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,041,662 | 360.417 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,041,587 | 360.416 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,041,512 | 360.415 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,041,437 | 360.414 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 182,444 | 1.824 | 20 | 200 | fits | 168,259 | 170 | 0.517 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 964,143 | 9.641 | 20 | 200 | fits | 156,926 | 97 | 0.554 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 178,185 | 1.782 | 20 | 20 | fits | 168,259 | 170 | 0.517 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,014,147 | 10.141 | 20 | 20 | fits | 54,479 | 20 | 0.598 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 181,770 | 1.818 | 20 | 24 | fits | 168,259 | 170 | 0.517 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,211,489 | 62.115 | 20 | 24 | MISS ceiling | 169,183 | 136 | 0.404 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 180,730 | 1.807 | 20 | 50 | fits | 168,259 | 170 | 0.517 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 962,648 | 9.626 | 20 | 50 | fits | 156,926 | 97 | 0.554 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 518,542 | 5.185 | 20 | 20 | fits | 165,675 | 42 | 0.679 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 803,642 | 8.036 | 20 | 20 | fits | 138,403 | 50 | 0.470 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,892 | 0.079 | 20 | 20 | fits | 63,110 | 22 (29) | 0.677 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 27,278 | 0.273 | 20 | 20 | fits | 63,110 | 22 (29) | 0.677 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,561 | 0.086 | 20 | 20 | fits | 66,090 | 33 (35) | 0.674 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 29,136 | 0.291 | 20 | 20 | fits | 66,090 | 33 (35) | 0.674 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 20,531 | 0.205 | 20 | 20 | fits | 44,450 | 18 (12) | 0.853 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 18,737 | 0.187 | 20 | 20 | fits | 50,857 | 22 (12) | 0.814 |
| LINK_UP | `adp.link_up.if0` | 2,742 | 0.027 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 17,626 | 0.176 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 31,877 | 0.319 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 22,973 | 0.230 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| LINK_DOWN | `adp.link_down.if0` | 2,385 | 0.024 | 20 | 200 | fits | 72,216 | 39 (9) | 0.707 |
| LINK_DOWN | `adp.link_down.if1` | 33,343 | 0.333 | 20 | 200 | fits | 72,216 | 39 (9) | 0.707 |
| LINK_UP | `adp.link_up.if0` | 2,742 | 0.027 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 17,626 | 0.176 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 31,877 | 0.319 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 22,973 | 0.230 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| GM_CHANGE | `adp.gm_change.if0` | 2,518 | 0.025 | 20 | 200 | fits | 20,960 | 27 (11) | 0.633 |
| GM_CHANGE | `adp.gm_change.if1` | 4,279 | 0.043 | 20 | 200 | fits | 20,960 | 27 (11) | 0.633 |
| LINK_UP | `adp.link_up.if0` | 2,742 | 0.027 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 17,626 | 0.176 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 31,877 | 0.319 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 22,973 | 0.230 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,359 | 0.044 | 20 | 200 | fits | 24,856 | 28 (31) | 0.477 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 5,807 | 0.058 | 20 | 200 | fits | 24,856 | 28 (31) | 0.477 |
| LINK_UP | `adp.link_up.if0` | 2,742 | 0.027 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| LINK_UP | `adp.link_up.if1` | 17,626 | 0.176 | 20 | 200 | fits | 45,799 | 79 (11) | 0.648 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 31,877 | 0.319 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 22,973 | 0.230 | 20 | 200 | fits | 37,486 | 39 (39) | 0.667 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,359 | 0.044 | 20 | 200 | fits | 20,387 | 17 (31) | 0.650 |
| set_name | `aecp_fanout.set_name.if0` | 68,940 | 0.689 | 20 | 24 | fits | 84,270 | 161 | 0.406 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 73,691 | 0.737 | 20 | 24 | fits | 70,145 | 140 | 0.410 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 56,127 | 0.561 | 20 | 24 | fits | 66,566 | 140 | 0.364 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 55,438 | 0.554 | 20 | 24 | fits | 65,944 | 140 | 0.358 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 71,658 | 0.717 | 20 | 24 | fits | 68,054 | 116 | 0.391 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 56,032 | 0.560 | 20 | 24 | fits | 66,997 | 140 | 0.371 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 60,063 | 0.601 | 20 | 24 | fits | 78,484 | 149 | 0.381 |
| set_name | `aecp_fanout.set_name.if1` | 79,413 | 0.794 | 20 | 24 | fits | 75,909 | 117 | 0.377 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 59,107 | 0.591 | 20 | 24 | fits | 70,862 | 140 | 0.415 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 70,561 | 0.706 | 20 | 24 | fits | 65,797 | 140 | 0.362 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 70,696 | 0.707 | 20 | 24 | fits | 65,970 | 140 | 0.362 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 55,988 | 0.560 | 20 | 24 | fits | 66,571 | 140 | 0.364 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 71,176 | 0.712 | 20 | 24 | fits | 65,935 | 140 | 0.356 |
| BIND_RX | `acmp.bind_rx.if0` | 28,902 | 0.289 | 20 | 20 | fits | 66,475 | 27 (77) | 0.790 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 10,553 | 0.106 | 20 | 20 | fits | 45,856 | 21 (32) | 0.807 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 15,011 | 0.150 | 20 | 20 | fits | 48,174 | 16 (47) | 0.769 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 18,404 | 0.184 | 20 | 20 | fits | 57,557 | 19 (50) | 0.830 |
| PROBE_TX | `acmp.probe_tx.if0` | 14,250 | 0.142 | 20 | 20 | fits | 47,249 | 18 (48) | 0.747 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 16,821 | 0.168 | 20 | 20 | fits | 50,214 | 24 (48) | 0.737 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 12,988 | 0.130 | 20 | 20 | fits | 45,471 | 17 (48) | 0.736 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 12,291 | 0.123 | 20 | 20 | fits | 44,271 | 17 (48) | 0.708 |
| BIND_RX | `acmp.bind_rx.if1` | 25,075 | 0.251 | 20 | 20 | fits | 60,142 | 28 (77) | 0.732 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 10,511 | 0.105 | 20 | 20 | fits | 45,661 | 23 (32) | 0.787 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 14,841 | 0.148 | 20 | 20 | fits | 48,441 | 17 (47) | 0.758 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 18,921 | 0.189 | 20 | 20 | fits | 58,573 | 22 (50) | 0.822 |
| PROBE_TX | `acmp.probe_tx.if1` | 15,386 | 0.154 | 20 | 20 | fits | 49,563 | 20 (48) | 0.763 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 14,170 | 0.142 | 20 | 20 | fits | 47,099 | 18 (48) | 0.755 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 13,100 | 0.131 | 20 | 20 | fits | 44,646 | 18 (48) | 0.707 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 11,810 | 0.118 | 20 | 20 | fits | 44,424 | 18 (48) | 0.700 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 12,558 | 0.126 | 20 | 24 | fits | 30,082 | 22 | 0.769 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 26,584 | 0.266 | 20 | 24 | fits | 35,387 | 22 | 0.715 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 21,945 | 0.219 | 20 | 24 | fits | 42,730 | 31 | 0.707 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 13,276 | 0.133 | 20 | 24 | fits | 30,509 | 22 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 21,806 | 0.218 | 20 | 24 | fits | 30,730 | 22 | 0.723 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 13,727 | 0.137 | 20 | 24 | fits | 30,926 | 22 | 0.712 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 21,340 | 0.213 | 20 | 24 | fits | 30,063 | 22 | 0.728 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 12,536 | 0.125 | 20 | 24 | fits | 29,485 | 22 | 0.726 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 12,783 | 0.128 | 20 | 24 | fits | 30,536 | 22 | 0.748 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,960 | 0.260 | 20 | 24 | fits | 35,250 | 23 | 0.647 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 12,188 | 0.122 | 20 | 24 | fits | 29,656 | 22 | 0.745 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 21,030 | 0.210 | 20 | 24 | fits | 29,881 | 22 | 0.758 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 12,382 | 0.124 | 20 | 24 | fits | 29,818 | 22 | 0.718 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 13,346 | 0.133 | 20 | 24 | fits | 31,288 | 22 | 0.735 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 22,002 | 0.220 | 20 | 24 | fits | 31,377 | 22 | 0.735 |
| get_configuration | `aecp.get_configuration.if0` | 10,614 | 0.106 | 20 | 24 | fits | 27,394 | 22 | 0.727 |
| entity_available | `aecp.entity_available.if0` | 19,563 | 0.196 | 20 | 24 | fits | 28,181 | 22 | 0.734 |
| get_name | `aecp.get_name.if0` | 13,050 | 0.131 | 20 | 24 | fits | 30,757 | 22 | 0.755 |
| get_counters | `aecp.get_counters.if0` | 14,462 | 0.145 | 20 | 24 | fits | 32,841 | 29 | 0.717 |
| get_avb_info | `aecp.get_avb_info.if0` | 20,582 | 0.206 | 20 | 24 | fits | 30,003 | 22 | 0.784 |
| unknown_command | `aecp.unknown_command.if0` | 11,864 | 0.119 | 20 | 24 | fits | 28,871 | 22 | 0.763 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 19,465 | 0.195 | 20 | 24 | fits | 27,267 | 22 | 0.725 |
| set_name | `aecp.set_name.if0` | 43,584 | 0.436 | 20 | 24 | fits | 63,017 | 75 | 0.675 |
| lock_entity | `aecp.lock_entity.if0` | 24,171 | 0.242 | 20 | 24 | fits | 39,310 | 47 | 0.709 |
| unlock_entity | `aecp.unlock_entity.if0` | 34,110 | 0.341 | 20 | 24 | fits | 38,937 | 46 | 0.706 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 12,095 | 0.121 | 20 | 24 | fits | 29,085 | 20 | 0.729 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 27,291 | 0.273 | 20 | 24 | fits | 33,378 | 20 | 0.696 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 23,180 | 0.232 | 20 | 24 | fits | 30,911 | 20 | 0.740 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 15,502 | 0.155 | 20 | 24 | fits | 30,017 | 20 | 0.716 |
| get_configuration | `aecp.get_configuration.if1` | 22,184 | 0.222 | 20 | 24 | fits | 27,650 | 20 | 0.747 |
| entity_available | `aecp.entity_available.if1` | 13,343 | 0.133 | 20 | 24 | fits | 27,270 | 20 | 0.719 |
| get_name | `aecp.get_name.if1` | 24,337 | 0.243 | 20 | 24 | fits | 30,800 | 20 | 0.770 |
| get_counters | `aecp.get_counters.if1` | 25,208 | 0.252 | 20 | 24 | fits | 43,133 | 36 | 0.701 |
| get_avb_info | `aecp.get_avb_info.if1` | 14,388 | 0.144 | 20 | 24 | fits | 28,932 | 20 | 0.776 |
| unknown_command | `aecp.unknown_command.if1` | 22,871 | 0.229 | 20 | 24 | fits | 28,571 | 20 | 0.768 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 12,872 | 0.129 | 20 | 24 | fits | 26,634 | 20 | 0.714 |
| set_name | `aecp.set_name.if1` | 40,001 | 0.400 | 20 | 24 | fits | 46,479 | 25 | 0.761 |
| lock_entity | `aecp.lock_entity.if1` | 38,891 | 0.389 | 20 | 24 | fits | 52,146 | 59 | 0.681 |
| unlock_entity | `aecp.unlock_entity.if1` | 27,204 | 0.272 | 20 | 24 | fits | 39,717 | 49 | 0.683 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
