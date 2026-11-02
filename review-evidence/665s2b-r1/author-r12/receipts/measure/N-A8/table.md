### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 129 paths and 6 of 182 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.243 (0.654) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.205 (0.601) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.110 (0.450) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.100 (0.441) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.071 (0.629) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.269 (0.629) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.053 (0.596) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.245 (0.596) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.112 (0.547) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.117 (0.562) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.100 (0.434) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.099 (0.440) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.113 (0.525) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.116 (0.463) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.114 (0.458) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.206 (0.570) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.076 (0.461) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.077 (0.465) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.189 (1.511) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.169 (1.639) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.219 (0.993) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.219 (0.917) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.362 (0.778) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.222 (0.768) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.309 (0.730) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.123 (0.675) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.150 (0.850) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.081 (0.726) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.110 (0.801) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.222 (0.768) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.153 (0.595) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.154 (0.612) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.026 (0.207) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.039 (0.207) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.014 (0.197) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.025 (0.197) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.013 (0.595) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.286 (0.595) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.017 (1.301) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.148 (1.301) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.129 (0.302) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.113 (0.302) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.211 (0.562) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.141 (0.562) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.186 (0.474) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.288 (0.583) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.200 (0.495) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.305 (0.600) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.266 (0.559) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.198 (0.487) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.313 (0.609) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.320 (0.622) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.295 (0.592) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.222 (0.514) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.349 (0.697) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.289 (0.648) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.191 (0.481) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.289 (0.583) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.252 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.262 (0.555) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.212 (0.502) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.227 (0.542) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.285 (0.581) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.295 (0.585) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.256 (0.549) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.285 (0.579) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.201 (0.491) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.293 (0.589) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.308 (0.606) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.285 (0.580) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.304 (0.594) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.210 (0.500) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.207 (0.498) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.300 (0.596) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.200 (0.490) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.280 (0.574) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.276 (0.581) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.633 (1.240) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.524 (1.103) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.272 (0.563) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.203 (0.494) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.269 (0.612) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.364 (0.734) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.746 (1.104) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.860 (1.218) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.886 (1.611) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.900 (1.288) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.743 (1.103) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_off.if1` (aecp-fanout) | 0.844 (1.311) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 1.080 (1.718) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 1.140 (1.822) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.854 (1.344) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.739 (1.097) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.740 (1.098) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.505 (7.226) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.529 (5.371) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.248 (0.791) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.438 (2.470) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.676 (64.205) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.357 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.138 (0.332) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.199 (0.576) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.103 (0.256) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.102 (0.268) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.128 (1.192) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.113 (1.110) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.120 (0.332) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.181 (0.576) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.183 (0.519) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe3.if1` (maap) | 0.262 (0.619) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.301 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 7.762 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.343 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 5.318 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 5.813 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.336 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.990 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.326 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 5.798 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 5.354 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | 15.879 | fits | 31 srp | 4 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.744 (1.892) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.486 (1.620) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.592 (0.593) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.514 (0.515) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.239 (0.240) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.236 (0.236) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.531 (1.641) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.455 (1.556) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 13.954 | 20 | 155,330 (1.553) | yes | - |
| backlog-adp | 0 | 16.390 | 19 | 196,639 (1.966) | yes | - |
| backlog-adp-refill | 0 | 41.151 | 30 | 176,255 (1.763) | yes | - |
| backlog-owed | 0 | 360.407 | 65 | 190,451 (1.905) | yes | - |

Composed maximum over the 4 backlog windows: 196,639 CPU cycles (1.966 ms), backlog-adp.
Over the windows that released their whole load only: 196,639 (1.966 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 2824 | 0 | 157,558 (1.576) | fits |
| adp-advertise | 605 | 0 | 130,132 (1.301) | fits |
| maap | 349 | 0 | 133,799 (1.338) | fits |
| acmp-noresp | 1503 | 0 | 156,557 (1.566) | fits |
| srp | 307 | 0 | 189,168 (1.892) | fits |
| backlog | 303 | 0 | 155,330 (1.553) | fits |
| backlog-adp | 323 | 0 | 196,639 (1.966) | fits |
| backlog-adp-refill | 334 | 0 | 176,255 (1.763) | fits |
| backlog-owed | 359 | 0 | 190,451 (1.905) | fits |
| acmp-disc | 823 | 0 | 150,716 (1.507) | fits |
| adp-link | 91 | 0 | 130,132 (1.301) | fits |
| adp-gm | 90 | 0 | 130,132 (1.301) | fits |
| adp-discover | 90 | 0 | 130,132 (1.301) | fits |
| control | 90 | 0 | 130,132 (1.301) | fits |
| aecp-fanout | 147 | 0 | 143,021 (1.430) | fits |
| acmp-cmd | 102 | 0 | 130,132 (1.301) | fits |
| aecp | 137 | 0 | 130,132 (1.301) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 15,047 | 0.150 | 20 | 20 | fits | 63,525 | 51 (14) | 0.718 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 8,124 | 0.081 | 20 | 20 | fits | 52,846 | 20 (14) | 0.876 |
| LINK_UP | `adp.link_up.if0` | 1,744 | 0.017 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| LINK_UP | `adp.link_up.if1` | 14,769 | 0.148 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 21,087 | 0.211 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 14,093 | 0.141 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 12,919 | 0.129 | 20 | 200 | fits | 3,281 | 18 (11) | 0.308 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 11,348 | 0.113 | 20 | 200 | fits | 3,281 | 18 (11) | 0.308 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 12,826 | 0.128 | 20 | 50 | fits | 119,163 | 50 | 0.709 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 18,314 | 0.183 | 20 | 50 | fits | 27,547 | 38 | 0.568 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 11,839 | 0.118 | 20 | 50 | fits | 27,394 | 38 | 0.553 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 12,004 | 0.120 | 20 | 50 | fits | 33,165 | 65 | 0.488 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 13,836 | 0.138 | 20 | 50 | fits | 33,165 | 65 | 0.488 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,274 | 0.103 | 20 | 50 | fits | 25,630 | 33 | 0.432 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 11,287 | 0.113 | 20 | 50 | fits | 111,022 | 50 | 0.622 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 16,599 | 0.166 | 20 | 50 | fits | 28,778 | 38 | 0.568 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 26,228 | 0.262 | 20 | 50 | fits | 27,874 | 38 | 0.500 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 18,069 | 0.181 | 20 | 50 | fits | 35,026 | 65 | 0.529 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 19,939 | 0.199 | 20 | 50 | fits | 35,026 | 65 | 0.529 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 10,229 | 0.102 | 20 | 50 | fits | 26,765 | 33 | 0.400 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 36,188 | 0.362 | 20 | 20 | fits | 51,094 | 30 (35) | 0.739 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 22,205 | 0.222 | 20 | 20 | fits | 47,308 | 24 (35) | 0.739 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 30,917 | 0.309 | 20 | 20 | fits | 46,296 | 25 (14) | 0.781 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 12,299 | 0.123 | 20 | 20 | fits | 41,649 | 19 (14) | 0.806 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 11,038 | 0.110 | 20 | 20 | fits | 57,027 | 47 (14) | 0.720 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 22,190 | 0.222 | 20 | 20 | fits | 41,254 | 19 (14) | 0.800 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 18,930 | 0.189 | 20 | 20 | fits | 50,140 | 24 (35) | 0.775 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 16,935 | 0.169 | 20 | 20 | fits | 62,550 | 51 (35) | 0.705 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 153,111 | 1.531 | 18 | 18 | fits | 44,903 | 14 | 0.840 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 145,546 | 1.455 | 18 | 18 | fits | 44,728 | 14 | 0.830 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 59,190 | 0.592 | 18 | 18 | fits | 59,255 | 15 | 0.890 |
| malformed MRPDU discard | `srp.malformed.if0` | 23,942 | 0.239 | 18 | 18 | fits | 24,007 | 15 | 0.529 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 174,373 | 1.744 | 218 | 218 | fits | 189,168 | 22 | 0.805 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 51,427 | 0.514 | 18 | 18 | fits | 51,492 | 15 | 0.877 |
| malformed MRPDU discard | `srp.malformed.if1` | 23,577 | 0.236 | 18 | 18 | fits | 23,642 | 15 | 0.529 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 148,577 | 1.486 | 218 | 218 | fits | 162,011 | 22 | 0.803 |
| an event behind 15 others | `backlog.event.if0` | 143,790 | 1.438 | 20 | 200 | fits | 112,443 | 125 | 0.523 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 650,518 | 6.505 | 20 | 20 | fits | 110,232 | 52 | 0.682 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 134,315 | 1.343 | 20 | 200 | fits | 134,523 | 143 | 0.531 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 527,985 | 5.280 | 20 | 200 | fits | 126,506 | 57 | 0.677 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 130,056 | 1.301 | 20 | 20 | fits | 134,523 | 143 | 0.531 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 717,264 | 7.173 | 20 | 20 | fits | 110,232 | 52 | 0.682 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 133,641 | 1.336 | 20 | 24 | fits | 134,523 | 143 | 0.531 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,214,600 | 12.146 | 20 | 24 | fits | 49,345 | 31 | 0.684 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 132,601 | 1.326 | 20 | 50 | fits | 134,523 | 143 | 0.531 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 526,490 | 5.265 | 20 | 50 | fits | 126,506 | 57 | 0.677 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 526,425 | 5.264 | 18 | 18 | fits | 126,506 | 57 | 0.677 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,342,169 | 13.422 | 18 | 18 | fits | 31,487 | 15 | 0.769 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 352,910 | 3.529 | 20 | 20 | fits | 196,639 | 89 | 0.697 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 109,546 | 1.095 | 20 | 200 | fits | 114,228 | 140 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 531,823 | 5.318 | 20 | 200 | fits | 196,639 | 89 | 0.697 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 110,458 | 1.105 | 20 | 20 | fits | 114,228 | 140 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 769,866 | 7.699 | 20 | 20 | fits | 117,069 | 46 | 0.662 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 114,043 | 1.140 | 20 | 24 | fits | 114,228 | 140 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,440,527 | 14.405 | 20 | 24 | fits | 64,493 | 31 | 0.690 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 113,003 | 1.130 | 20 | 50 | fits | 114,228 | 140 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 535,499 | 5.355 | 20 | 50 | fits | 196,639 | 89 | 0.697 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 535,434 | 5.354 | 18 | 18 | fits | 196,639 | 89 | 0.697 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,581,240 | 15.812 | 18 | 18 | fits | 47,209 | 18 | 0.689 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 24,764 | 0.248 | 20 | 20 | fits | 43,767 | 21 | 0.772 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 109,546 | 1.095 | 20 | 200 | fits | 114,228 | 140 | 0.489 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 61,161 | 0.612 | 20 | 200 | fits | 43,767 | 21 | 0.772 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 110,458 | 1.105 | 20 | 20 | fits | 114,228 | 140 | 0.489 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 749,264 | 7.493 | 20 | 20 | fits | 116,958 | 46 | 0.661 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 114,043 | 1.140 | 20 | 24 | fits | 114,228 | 140 | 0.489 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,411,936 | 14.119 | 20 | 24 | fits | 65,140 | 31 | 0.697 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 113,003 | 1.130 | 20 | 50 | fits | 114,228 | 140 | 0.489 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 515,115 | 5.151 | 20 | 50 | fits | 176,255 | 79 | 0.699 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 515,050 | 5.151 | 18 | 18 | fits | 176,255 | 79 | 0.699 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,587,911 | 15.879 | 18 | 18 | fits | 34,177 | 15 | 0.771 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,367,598 | 63.676 | 20 | 20 | MISS ceiling | 48,788 | 27 | 0.549 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,035,665 | 360.357 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,035,590 | 360.356 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,035,515 | 360.355 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,035,440 | 360.354 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 123,412 | 1.234 | 20 | 200 | fits | 110,721 | 134 | 0.490 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 581,297 | 5.813 | 20 | 200 | fits | 128,843 | 69 | 0.650 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 119,153 | 1.192 | 20 | 20 | fits | 110,721 | 134 | 0.490 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 776,196 | 7.762 | 20 | 20 | fits | 97,716 | 35 | 0.731 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 122,738 | 1.227 | 20 | 24 | fits | 110,721 | 134 | 0.490 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,498,989 | 64.990 | 20 | 24 | MISS ceiling | 30,553 | 23 | 0.529 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 121,698 | 1.217 | 20 | 50 | fits | 110,721 | 134 | 0.490 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 579,802 | 5.798 | 20 | 50 | fits | 128,843 | 69 | 0.650 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 311,694 | 3.117 | 18 | 18 | fits | 190,451 | 138 | 0.642 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,331,102 | 13.311 | 18 | 18 | fits | 34,066 | 18 | 0.757 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,339 | 0.053 | 20 | 20 | fits | 59,616 | 19 (29) | 0.688 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 24,473 | 0.245 | 20 | 20 | fits | 59,616 | 19 (29) | 0.688 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,062 | 0.071 | 20 | 20 | fits | 62,919 | 30 (35) | 0.685 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 26,897 | 0.269 | 20 | 20 | fits | 62,919 | 30 (35) | 0.685 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 21,922 | 0.219 | 20 | 20 | fits | 63,982 | 26 (12) | 0.819 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 21,859 | 0.219 | 20 | 20 | fits | 63,698 | 51 (12) | 0.720 |
| LINK_UP | `adp.link_up.if0` | 1,744 | 0.017 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| LINK_UP | `adp.link_up.if1` | 14,769 | 0.148 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 21,087 | 0.211 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 14,093 | 0.141 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| LINK_DOWN | `adp.link_down.if0` | 1,286 | 0.013 | 20 | 200 | fits | 59,541 | 38 (9) | 0.661 |
| LINK_DOWN | `adp.link_down.if1` | 28,624 | 0.286 | 20 | 200 | fits | 59,541 | 38 (9) | 0.661 |
| LINK_UP | `adp.link_up.if0` | 1,744 | 0.017 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| LINK_UP | `adp.link_up.if1` | 14,769 | 0.148 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 21,087 | 0.211 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 14,093 | 0.141 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| GM_CHANGE | `adp.gm_change.if0` | 1,353 | 0.014 | 20 | 200 | fits | 19,678 | 28 (11) | 0.243 |
| GM_CHANGE | `adp.gm_change.if1` | 2,537 | 0.025 | 20 | 200 | fits | 19,678 | 28 (11) | 0.243 |
| LINK_UP | `adp.link_up.if0` | 1,744 | 0.017 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| LINK_UP | `adp.link_up.if1` | 14,769 | 0.148 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 21,087 | 0.211 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 14,093 | 0.141 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 2,562 | 0.026 | 20 | 200 | fits | 20,736 | 25 (31) | 0.333 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 3,919 | 0.039 | 20 | 200 | fits | 20,736 | 25 (31) | 0.333 |
| LINK_UP | `adp.link_up.if0` | 1,744 | 0.017 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| LINK_UP | `adp.link_up.if1` | 14,769 | 0.148 | 20 | 200 | fits | 130,132 | 86 (11) | 0.651 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 21,087 | 0.211 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 14,093 | 0.141 | 20 | 200 | fits | 32,774 | 42 (39) | 0.429 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 2,562 | 0.026 | 20 | 200 | fits | 19,377 | 18 (31) | 0.440 |
| set_name | `aecp_fanout.set_name.if0` | 108,026 | 1.080 | 20 | 24 | fits | 143,021 | 225 | 0.214 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 88,570 | 0.886 | 20 | 24 | fits | 88,793 | 205 | 0.232 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 74,337 | 0.743 | 20 | 24 | fits | 82,979 | 205 | 0.199 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 73,025 | 0.730 | 20 | 24 | fits | 82,451 | 205 | 0.193 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 85,383 | 0.854 | 20 | 24 | fits | 84,895 | 181 | 0.212 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 74,625 | 0.746 | 20 | 24 | fits | 83,460 | 205 | 0.201 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 73,926 | 0.739 | 20 | 24 | fits | 82,965 | 205 | 0.192 |
| set_name | `aecp_fanout.set_name.if1` | 113,984 | 1.140 | 20 | 24 | fits | 132,728 | 181 | 0.164 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 90,027 | 0.900 | 20 | 24 | fits | 90,073 | 205 | 0.250 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 73,427 | 0.734 | 20 | 24 | fits | 82,597 | 205 | 0.194 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 84,381 | 0.844 | 20 | 24 | fits | 81,564 | 205 | 0.175 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 86,005 | 0.860 | 20 | 24 | fits | 83,029 | 205 | 0.194 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 74,016 | 0.740 | 20 | 24 | fits | 82,911 | 205 | 0.192 |
| BIND_RX | `acmp.bind_rx.if0` | 24,302 | 0.243 | 20 | 20 | fits | 65,388 | 30 (77) | 0.759 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 7,627 | 0.076 | 20 | 20 | fits | 46,082 | 21 (32) | 0.819 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,220 | 0.112 | 20 | 20 | fits | 54,675 | 28 (47) | 0.767 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,261 | 0.153 | 20 | 20 | fits | 59,512 | 21 (50) | 0.825 |
| PROBE_TX | `acmp.probe_tx.if0` | 11,363 | 0.114 | 20 | 20 | fits | 45,847 | 20 (48) | 0.714 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,325 | 0.113 | 20 | 20 | fits | 52,526 | 29 (48) | 0.745 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,049 | 0.110 | 20 | 20 | fits | 45,009 | 19 (48) | 0.723 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 10,018 | 0.100 | 20 | 20 | fits | 43,397 | 19 (48) | 0.661 |
| BIND_RX | `acmp.bind_rx.if1` | 20,505 | 0.205 | 20 | 20 | fits | 60,147 | 31 (77) | 0.706 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 7,651 | 0.077 | 20 | 20 | fits | 46,540 | 22 (32) | 0.800 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 11,743 | 0.117 | 20 | 20 | fits | 56,188 | 29 (47) | 0.763 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 15,446 | 0.154 | 20 | 20 | fits | 61,213 | 22 (50) | 0.824 |
| PROBE_TX | `acmp.probe_tx.if1` | 20,581 | 0.206 | 20 | 20 | fits | 57,020 | 27 (48) | 0.741 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 11,634 | 0.116 | 20 | 20 | fits | 46,288 | 20 (48) | 0.720 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 10,016 | 0.100 | 20 | 20 | fits | 44,140 | 20 (48) | 0.658 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 9,905 | 0.099 | 20 | 20 | fits | 43,994 | 20 (48) | 0.649 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 28,008 | 0.280 | 20 | 24 | fits | 29,434 | 24 | 0.709 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 25,237 | 0.252 | 20 | 24 | fits | 33,355 | 24 | 0.626 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 21,207 | 0.212 | 20 | 24 | fits | 29,077 | 24 | 0.637 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 29,292 | 0.293 | 20 | 24 | fits | 28,343 | 24 | 0.573 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 20,731 | 0.207 | 20 | 24 | fits | 28,773 | 24 | 0.608 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 30,027 | 0.300 | 20 | 24 | fits | 28,999 | 24 | 0.591 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 20,016 | 0.200 | 20 | 24 | fits | 27,965 | 24 | 0.619 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 28,521 | 0.285 | 20 | 24 | fits | 27,493 | 23 | 0.594 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 29,490 | 0.295 | 20 | 24 | fits | 28,462 | 24 | 0.639 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 25,632 | 0.256 | 20 | 24 | fits | 33,873 | 24 | 0.542 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 28,498 | 0.285 | 20 | 24 | fits | 27,340 | 24 | 0.624 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 20,074 | 0.201 | 20 | 24 | fits | 27,944 | 24 | 0.655 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 28,486 | 0.285 | 20 | 24 | fits | 27,458 | 24 | 0.589 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 30,397 | 0.304 | 20 | 24 | fits | 29,369 | 24 | 0.629 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 20,991 | 0.210 | 20 | 24 | fits | 29,190 | 24 | 0.634 |
| get_configuration | `aecp.get_configuration.if0` | 26,593 | 0.266 | 20 | 24 | fits | 25,397 | 24 | 0.559 |
| entity_available | `aecp.entity_available.if0` | 18,579 | 0.186 | 20 | 24 | fits | 26,518 | 24 | 0.602 |
| get_name | `aecp.get_name.if0` | 29,521 | 0.295 | 20 | 24 | fits | 28,638 | 24 | 0.633 |
| get_counters | `aecp.get_counters.if0` | 31,321 | 0.313 | 20 | 24 | fits | 30,884 | 31 | 0.649 |
| get_avb_info | `aecp.get_avb_info.if0` | 19,984 | 0.200 | 20 | 24 | fits | 28,276 | 24 | 0.690 |
| unknown_command | `aecp.unknown_command.if0` | 27,237 | 0.272 | 20 | 24 | fits | 26,790 | 24 | 0.650 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 19,145 | 0.191 | 20 | 24 | fits | 26,752 | 24 | 0.627 |
| set_name | `aecp.set_name.if0` | 63,321 | 0.633 | 20 | 24 | fits | 93,349 | 70 | 0.592 |
| lock_entity | `aecp.lock_entity.if0` | 34,890 | 0.349 | 20 | 24 | fits | 39,658 | 50 | 0.624 |
| unlock_entity | `aecp.unlock_entity.if0` | 26,869 | 0.269 | 20 | 24 | fits | 38,960 | 50 | 0.608 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 27,561 | 0.276 | 20 | 24 | fits | 27,120 | 22 | 0.598 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 26,212 | 0.262 | 20 | 24 | fits | 32,036 | 22 | 0.611 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 22,683 | 0.227 | 20 | 24 | fits | 28,830 | 22 | 0.642 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 30,828 | 0.308 | 20 | 24 | fits | 28,137 | 22 | 0.579 |
| get_configuration | `aecp.get_configuration.if1` | 19,775 | 0.198 | 20 | 24 | fits | 25,824 | 22 | 0.610 |
| entity_available | `aecp.entity_available.if1` | 28,770 | 0.288 | 20 | 24 | fits | 25,823 | 22 | 0.567 |
| get_name | `aecp.get_name.if1` | 22,208 | 0.222 | 20 | 24 | fits | 28,592 | 22 | 0.664 |
| get_counters | `aecp.get_counters.if1` | 31,985 | 0.320 | 20 | 24 | fits | 29,681 | 28 | 0.630 |
| get_avb_info | `aecp.get_avb_info.if1` | 30,484 | 0.305 | 20 | 24 | fits | 28,092 | 22 | 0.698 |
| unknown_command | `aecp.unknown_command.if1` | 20,251 | 0.203 | 20 | 24 | fits | 26,523 | 22 | 0.645 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 28,855 | 0.289 | 20 | 24 | fits | 25,785 | 22 | 0.581 |
| set_name | `aecp.set_name.if1` | 52,367 | 0.524 | 20 | 24 | fits | 87,535 | 31 | 0.617 |
| lock_entity | `aecp.lock_entity.if1` | 28,880 | 0.289 | 20 | 24 | fits | 40,840 | 55 | 0.581 |
| unlock_entity | `aecp.unlock_entity.if1` | 36,379 | 0.364 | 20 | 24 | fits | 39,486 | 55 | 0.536 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
