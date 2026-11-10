### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 129 paths and 6 of 182 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.266 (0.521) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 0.234 (0.482) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.124 (0.309) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 0.135 (0.311) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.086 (0.423) | fits | 0 adp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 0.168 (0.423) | fits | 1 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 0.079 (0.396) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 0.154 (0.396) | fits | 1 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.129 (0.312) | fits | 0 acmp | 1 | 0 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 0.119 (0.308) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.112 (0.293) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 0.108 (0.295) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.117 (0.300) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 0.127 (0.302) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.137 (0.313) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 0.135 (0.322) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.094 (0.349) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 0.098 (0.346) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.472 (1.662) | fits | 0 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.278 (0.709) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.248 (0.780) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 0.250 (0.688) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.433 (0.856) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 0.579 (0.856) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.242 (0.744) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 0.331 (0.744) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.240 (0.647) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 0.246 (0.680) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.347 (0.735) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 0.433 (0.735) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.172 (0.451) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 0.174 (0.463) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.045 (0.245) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.059 (0.245) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.204) | fits | 0 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.040 (0.204) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.025 (0.717) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 0.332 (0.717) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.030 (0.455) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.178 (0.455) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.154 (0.360) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 0.136 (0.360) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.289 (0.669) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 0.214 (0.669) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.236 (0.603) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 0.171 (0.527) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.423 (0.801) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 0.186 (0.560) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.146 (0.497) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 0.267 (0.635) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.184 (0.567) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 0.281 (0.578) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.163 (0.524) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 0.288 (0.667) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.285 (0.637) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 0.410 (0.768) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.240 (0.607) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 0.166 (0.522) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.301 (0.682) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 0.317 (0.698) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.245 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 0.285 (0.669) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 0.161 (0.516) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.168 (0.539) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.296 (0.673) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 0.153 (0.517) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 0.253 (0.620) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.167 (0.544) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 0.195 (0.556) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 0.160 (0.520) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.173 (0.549) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.255 (0.634) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 0.255 (0.628) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 0.167 (0.529) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.247 (0.623) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.209 (0.580) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 0.160 (0.529) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.367 (0.752) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 0.449 (0.826) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.143 (0.504) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 0.272 (0.644) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.385 (0.732) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 0.310 (0.666) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.685 (1.058) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 0.680 (1.054) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.618 (1.014) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 0.709 (1.093) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.685 (1.056) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 0.713 (1.087) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.800 (1.217) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 0.672 (1.072) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.604 (0.988) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.667 (0.959) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 0.595 (0.965) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.855 (8.390) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 8.612 (9.579) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.132 (0.571) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.908 (2.820) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.057 (63.455) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.410 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.324 (0.727) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 0.217 (0.626) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.131 (0.288) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.129 (0.290) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.151 (0.341) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.139 (0.329) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.306 (0.727) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 0.198 (0.626) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.275 (0.658) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 0.210 (0.599) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.751 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 9.533 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.793 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 9.526 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog-owed.service.adp.last.if1` (backlog-owed) | 7.967 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.786 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 61.866 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.776 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 9.563 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 5.395 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog.service.srp.last.if1` (backlog) | 6.854 | fits | 31 srp | 4 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 1.930 (2.385) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 1.624 (2.031) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.605 (0.606) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 0.548 (0.549) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 0.250 (0.251) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 0.253 (0.254) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 1.454 (1.518) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 1.362 (1.421) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 9.700 | 8 | 179,519 (1.795) | yes | - |
| backlog-adp | 0 | 11.401 | 10 | 163,238 (1.632) | yes | - |
| backlog-adp-refill | 0 | 40.950 | 23 | 163,238 (1.632) | yes | - |
| backlog-owed | 0 | 360.461 | 51 | 164,986 (1.650) | yes | - |

Composed maximum over the 4 backlog windows: 179,519 CPU cycles (1.795 ms), backlog.
Over the windows that released their whole load only: 179,519 (1.795 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 5872 | 0 | 117,701 (1.177) | fits |
| adp-advertise | 599 | 0 | 117,701 (1.177) | fits |
| maap | 366 | 0 | 117,703 (1.177) | fits |
| acmp-noresp | 2720 | 0 | 117,701 (1.177) | fits |
| save | 611 | 0 | 117,701 (1.177) | fits |
| srp | 306 | 0 | 185,680 (1.857) | fits |
| backlog | 288 | 0 | 179,519 (1.795) | fits |
| backlog-adp | 314 | 0 | 163,238 (1.632) | fits |
| backlog-adp-refill | 327 | 0 | 163,238 (1.632) | fits |
| backlog-owed | 338 | 0 | 164,986 (1.650) | fits |
| acmp-disc | 1386 | 0 | 117,978 (1.180) | fits |
| adp-link | 91 | 0 | 117,701 (1.177) | fits |
| adp-gm | 89 | 0 | 117,701 (1.177) | fits |
| adp-discover | 89 | 0 | 117,701 (1.177) | fits |
| control | 89 | 0 | 117,701 (1.177) | fits |
| aecp-fanout | 144 | 0 | 117,701 (1.177) | fits |
| acmp-cmd | 105 | 0 | 117,701 (1.177) | fits |
| aecp | 135 | 0 | 117,701 (1.177) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 4697.836 | 12,110 | 370 | - | 13.360 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 109,365 (1.094) | 78,690 (0.787) |
| adp-advertise | 577 | 31,132 (0.311) | 2,827 (0.028) |
| maap | 344 | 31,119 (0.311) | 2,827 (0.028) |
| acmp-noresp | 615 | 108,987 (1.090) | 78,646 (0.786) |
| save | 585 | 108,016 (1.080) | 78,560 (0.786) |
| srp | 278 | 31,104 (0.311) | 3,067 (0.031) |
| backlog | 266 | 31,104 (0.311) | 2,996 (0.030) |
| backlog-adp | 271 | 31,104 (0.311) | 2,837 (0.028) |
| backlog-adp-refill | 274 | 31,104 (0.311) | 2,877 (0.029) |
| backlog-owed | 306 | 31,881 (0.319) | 2,891 (0.029) |
| acmp-disc | 336 | 105,717 (1.057) | 78,391 (0.784) |
| adp-link | 79 | 30,865 (0.309) | 2,827 (0.028) |
| adp-gm | 79 | 30,865 (0.309) | 2,827 (0.028) |
| adp-discover | 79 | 30,865 (0.309) | 2,827 (0.028) |
| control | 79 | 30,865 (0.309) | 2,827 (0.028) |
| aecp-fanout | 93 | 30,865 (0.309) | 2,827 (0.028) |
| acmp-cmd | 67 | 30,865 (0.309) | 2,827 (0.028) |
| aecp | 88 | 30,865 (0.309) | 2,827 (0.028) |

Longest pass that carries a step: 109,365 CPU cycles (1.094 ms), acmp-notk; longest step: 78,690 (0.787 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 23,981 | 0.240 | 20 | 20 | fits | 39,256 | 28 (14) | 0.799 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 24,553 | 0.246 | 20 | 20 | fits | 42,458 | 25 (14) | 0.877 |
| LINK_UP | `adp.link_up.if0` | 2,972 | 0.030 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| LINK_UP | `adp.link_up.if1` | 17,771 | 0.178 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 28,926 | 0.289 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 21,386 | 0.214 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 15,420 | 0.154 | 20 | 200 | fits | 4,719 | 19 (11) | 0.523 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 13,603 | 0.136 | 20 | 200 | fits | 4,719 | 19 (11) | 0.523 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 15,068 | 0.151 | 20 | 50 | fits | 34,095 | 44 | 0.739 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 27,458 | 0.275 | 20 | 50 | fits | 30,102 | 36 | 0.715 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 24,988 | 0.250 | 20 | 50 | fits | 29,835 | 36 | 0.705 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 30,573 | 0.306 | 20 | 50 | fits | 36,252 | 62 | 0.623 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 32,405 | 0.324 | 20 | 50 | fits | 36,252 | 62 | 0.623 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 13,114 | 0.131 | 20 | 50 | fits | 28,752 | 31 | 0.650 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 13,854 | 0.139 | 20 | 50 | fits | 32,930 | 44 | 0.727 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 20,977 | 0.210 | 20 | 50 | fits | 30,821 | 37 | 0.716 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 15,872 | 0.159 | 20 | 50 | fits | 29,219 | 36 | 0.678 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 19,782 | 0.198 | 20 | 50 | fits | 36,994 | 62 | 0.637 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 21,704 | 0.217 | 20 | 50 | fits | 36,994 | 62 | 0.637 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 12,874 | 0.129 | 20 | 50 | fits | 29,022 | 31 | 0.636 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 43,283 | 0.433 | 20 | 20 | fits | 53,163 | 42 (35) | 0.741 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 57,875 | 0.579 | 20 | 20 | fits | 53,163 | 42 (35) | 0.741 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 24,180 | 0.242 | 20 | 20 | fits | 42,015 | 34 (14) | 0.793 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 33,054 | 0.331 | 20 | 20 | fits | 42,015 | 34 (14) | 0.793 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 34,691 | 0.347 | 20 | 20 | fits | 41,167 | 35 (14) | 0.791 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 43,291 | 0.433 | 20 | 20 | fits | 41,167 | 35 (14) | 0.791 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 47,224 | 0.472 | 20 | 20 | fits | 37,175 | 22 (35) | 0.808 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 27,846 | 0.278 | 20 | 20 | fits | 37,655 | 22 (35) | 0.811 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 145,426 | 1.454 | 20 | 20 | fits | 117,703 | 6 | 0.805 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 136,238 | 1.362 | 20 | 20 | fits | 108,912 | 6 | 0.752 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 60,489 | 0.605 | 20 | 20 | fits | 60,554 | 13 | 0.902 |
| malformed MRPDU discard | `srp.malformed.if0` | 25,005 | 0.250 | 20 | 20 | fits | 25,070 | 13 | 0.706 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 192,997 | 1.930 | 220 | 220 | fits | 185,680 | 10 | 0.798 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 54,846 | 0.548 | 20 | 20 | fits | 54,911 | 13 | 0.895 |
| malformed MRPDU discard | `srp.malformed.if1` | 25,340 | 0.253 | 20 | 20 | fits | 25,405 | 13 | 0.706 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 162,407 | 1.624 | 220 | 220 | fits | 154,561 | 9 | 0.787 |
| an event behind 15 others | `backlog.event.if0` | 190,832 | 1.908 | 20 | 200 | fits | 102,462 | 129 | 0.547 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 785,466 | 7.855 | 20 | 20 | fits | 149,220 | 102 | 0.564 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 179,311 | 1.793 | 20 | 200 | fits | 179,519 | 201 | 0.509 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 429,349 | 4.293 | 20 | 200 | fits | 148,185 | 78 | 0.619 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 175,052 | 1.751 | 20 | 20 | fits | 179,519 | 201 | 0.509 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 833,693 | 8.337 | 20 | 20 | fits | 149,220 | 102 | 0.564 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 178,637 | 1.786 | 20 | 24 | fits | 179,519 | 201 | 0.509 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 908,461 | 9.085 | 20 | 24 | fits | 71,333 | 59 | 0.484 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 177,597 | 1.776 | 20 | 50 | fits | 179,519 | 201 | 0.509 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 427,854 | 4.279 | 20 | 50 | fits | 148,185 | 78 | 0.619 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 539,458 | 5.395 | 20 | 20 | fits | 107,220 | 53 | 0.546 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 685,373 | 6.854 | 20 | 20 | fits | 63,882 | 37 | 0.409 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 861,246 | 8.612 | 20 | 20 | fits | 157,478 | 125 | 0.550 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 148,758 | 1.488 | 20 | 200 | fits | 153,440 | 194 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 952,629 | 9.526 | 20 | 200 | fits | 157,478 | 125 | 0.550 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 149,670 | 1.497 | 20 | 20 | fits | 153,440 | 194 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 953,325 | 9.533 | 20 | 20 | fits | 157,478 | 125 | 0.550 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 153,255 | 1.533 | 20 | 24 | fits | 153,440 | 194 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,029,750 | 10.297 | 20 | 24 | fits | 72,990 | 59 | 0.500 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 152,215 | 1.522 | 20 | 50 | fits | 153,440 | 194 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 956,305 | 9.563 | 20 | 50 | fits | 157,478 | 125 | 0.550 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 314,998 | 3.150 | 20 | 20 | fits | 163,238 | 80 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 636,820 | 6.368 | 20 | 20 | fits | 158,648 | 59 | 0.461 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 13,209 | 0.132 | 20 | 20 | fits | 32,771 | 20 | 0.800 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 148,758 | 1.488 | 20 | 200 | fits | 153,440 | 194 | 0.498 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 36,244 | 0.362 | 20 | 200 | fits | 32,771 | 20 | 0.800 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 149,670 | 1.497 | 20 | 20 | fits | 153,440 | 194 | 0.498 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 952,551 | 9.526 | 20 | 20 | fits | 156,704 | 127 | 0.509 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 153,255 | 1.533 | 20 | 24 | fits | 153,440 | 194 | 0.498 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,015,005 | 10.150 | 20 | 24 | fits | 59,019 | 46 | 0.526 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 152,215 | 1.522 | 20 | 50 | fits | 153,440 | 194 | 0.498 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 955,531 | 9.555 | 20 | 50 | fits | 156,704 | 127 | 0.509 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 314,998 | 3.150 | 20 | 20 | fits | 163,238 | 80 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 636,820 | 6.368 | 20 | 20 | fits | 158,648 | 59 | 0.461 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,305,748 | 63.057 | 20 | 20 | MISS ceiling | 23,859 | 13 | 0.603 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,988 | 360.410 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,040,913 | 360.409 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,040,838 | 360.408 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,040,763 | 360.408 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 162,891 | 1.629 | 20 | 200 | fits | 153,342 | 202 | 0.491 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 796,744 | 7.967 | 20 | 200 | fits | 157,537 | 144 | 0.501 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 158,632 | 1.586 | 20 | 20 | fits | 153,342 | 202 | 0.491 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 833,689 | 8.337 | 20 | 20 | fits | 41,420 | 32 | 0.454 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 162,217 | 1.622 | 20 | 24 | fits | 153,342 | 202 | 0.491 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,186,622 | 61.866 | 20 | 24 | MISS ceiling | 155,001 | 136 | 0.427 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 161,177 | 1.612 | 20 | 50 | fits | 153,342 | 202 | 0.491 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 795,249 | 7.952 | 20 | 50 | fits | 157,537 | 144 | 0.501 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 325,708 | 3.257 | 20 | 20 | fits | 164,986 | 80 | 0.667 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 635,632 | 6.356 | 20 | 20 | fits | 150,751 | 54 | 0.445 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 7,912 | 0.079 | 20 | 20 | fits | 39,605 | 22 (29) | 0.673 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 15,444 | 0.154 | 20 | 20 | fits | 39,605 | 22 (29) | 0.673 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 8,577 | 0.086 | 20 | 20 | fits | 42,324 | 33 (35) | 0.663 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 16,771 | 0.168 | 20 | 20 | fits | 42,324 | 33 (35) | 0.663 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 24,803 | 0.248 | 20 | 20 | fits | 39,038 | 25 (12) | 0.828 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 24,999 | 0.250 | 20 | 20 | fits | 45,346 | 28 (12) | 0.797 |
| LINK_UP | `adp.link_up.if0` | 2,972 | 0.030 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| LINK_UP | `adp.link_up.if1` | 17,771 | 0.178 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 28,926 | 0.289 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 21,386 | 0.214 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| LINK_DOWN | `adp.link_down.if0` | 2,478 | 0.025 | 20 | 200 | fits | 71,714 | 39 (9) | 0.713 |
| LINK_DOWN | `adp.link_down.if1` | 33,196 | 0.332 | 20 | 200 | fits | 71,714 | 39 (9) | 0.713 |
| LINK_UP | `adp.link_up.if0` | 2,972 | 0.030 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| LINK_UP | `adp.link_up.if1` | 17,771 | 0.178 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 28,926 | 0.289 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 21,386 | 0.214 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| GM_CHANGE | `adp.gm_change.if0` | 2,531 | 0.025 | 20 | 200 | fits | 20,356 | 27 (11) | 0.608 |
| GM_CHANGE | `adp.gm_change.if1` | 4,014 | 0.040 | 20 | 200 | fits | 20,356 | 27 (11) | 0.608 |
| LINK_UP | `adp.link_up.if0` | 2,972 | 0.030 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| LINK_UP | `adp.link_up.if1` | 17,771 | 0.178 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 28,926 | 0.289 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 21,386 | 0.214 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,502 | 0.045 | 20 | 200 | fits | 24,512 | 28 (31) | 0.477 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 5,904 | 0.059 | 20 | 200 | fits | 24,512 | 28 (31) | 0.477 |
| LINK_UP | `adp.link_up.if0` | 2,972 | 0.030 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| LINK_UP | `adp.link_up.if1` | 17,771 | 0.178 | 20 | 200 | fits | 45,469 | 79 (11) | 0.658 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 28,926 | 0.289 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 21,386 | 0.214 | 20 | 200 | fits | 34,924 | 39 (39) | 0.623 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,502 | 0.045 | 20 | 200 | fits | 20,079 | 17 (31) | 0.646 |
| set_name | `aecp_fanout.set_name.if0` | 80,014 | 0.800 | 20 | 24 | fits | 83,903 | 160 | 0.410 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 61,764 | 0.618 | 20 | 24 | fits | 70,007 | 139 | 0.411 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 68,505 | 0.685 | 20 | 24 | fits | 66,721 | 139 | 0.383 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 67,839 | 0.678 | 20 | 24 | fits | 65,992 | 139 | 0.370 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 60,377 | 0.604 | 20 | 24 | fits | 68,634 | 116 | 0.410 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 68,468 | 0.685 | 20 | 24 | fits | 66,812 | 139 | 0.379 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 66,718 | 0.667 | 20 | 24 | fits | 66,632 | 139 | 0.365 |
| set_name | `aecp_fanout.set_name.if1` | 67,238 | 0.672 | 20 | 24 | fits | 75,652 | 117 | 0.378 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 70,889 | 0.709 | 20 | 24 | fits | 70,391 | 139 | 0.416 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 71,255 | 0.713 | 20 | 24 | fits | 78,249 | 148 | 0.389 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 58,575 | 0.586 | 20 | 24 | fits | 65,544 | 139 | 0.366 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 68,029 | 0.680 | 20 | 24 | fits | 66,466 | 139 | 0.379 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 59,498 | 0.595 | 20 | 24 | fits | 65,845 | 139 | 0.366 |
| BIND_RX | `acmp.bind_rx.if0` | 26,648 | 0.266 | 20 | 20 | fits | 52,126 | 27 (77) | 0.782 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,387 | 0.094 | 20 | 20 | fits | 34,941 | 20 (32) | 0.832 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,859 | 0.129 | 20 | 20 | fits | 31,214 | 16 (47) | 0.745 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 17,163 | 0.172 | 20 | 20 | fits | 45,118 | 19 (50) | 0.816 |
| PROBE_TX | `acmp.probe_tx.if0` | 13,680 | 0.137 | 20 | 20 | fits | 31,275 | 18 (48) | 0.707 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,716 | 0.117 | 20 | 20 | fits | 29,968 | 17 (48) | 0.678 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 12,395 | 0.124 | 20 | 20 | fits | 30,897 | 17 (48) | 0.723 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 11,174 | 0.112 | 20 | 20 | fits | 29,267 | 17 (48) | 0.667 |
| BIND_RX | `acmp.bind_rx.if1` | 23,386 | 0.234 | 20 | 20 | fits | 48,197 | 28 (77) | 0.726 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 9,836 | 0.098 | 20 | 20 | fits | 34,598 | 21 (32) | 0.810 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 11,926 | 0.119 | 20 | 20 | fits | 30,793 | 19 (47) | 0.692 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 17,361 | 0.174 | 20 | 20 | fits | 46,271 | 20 (50) | 0.819 |
| PROBE_TX | `acmp.probe_tx.if1` | 13,538 | 0.135 | 20 | 20 | fits | 32,222 | 20 (48) | 0.734 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 12,678 | 0.127 | 20 | 20 | fits | 30,214 | 20 (48) | 0.661 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 13,479 | 0.135 | 20 | 20 | fits | 31,082 | 18 (48) | 0.711 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 10,803 | 0.108 | 20 | 20 | fits | 29,512 | 18 (48) | 0.667 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 20,905 | 0.209 | 20 | 24 | fits | 30,126 | 22 | 0.780 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 30,144 | 0.301 | 20 | 24 | fits | 34,773 | 22 | 0.707 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 24,506 | 0.245 | 20 | 24 | fits | 30,018 | 22 | 0.707 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 16,734 | 0.167 | 20 | 24 | fits | 29,606 | 22 | 0.708 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 25,491 | 0.255 | 20 | 24 | fits | 29,922 | 22 | 0.710 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 16,684 | 0.167 | 20 | 24 | fits | 29,854 | 22 | 0.706 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 24,735 | 0.247 | 20 | 24 | fits | 29,467 | 22 | 0.716 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 16,086 | 0.161 | 20 | 24 | fits | 28,556 | 22 | 0.717 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 16,771 | 0.168 | 20 | 24 | fits | 29,630 | 22 | 0.737 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 29,615 | 0.296 | 20 | 24 | fits | 34,401 | 23 | 0.639 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 15,309 | 0.153 | 20 | 24 | fits | 28,625 | 22 | 0.743 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 25,253 | 0.253 | 20 | 24 | fits | 28,966 | 22 | 0.752 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 15,999 | 0.160 | 20 | 24 | fits | 28,865 | 22 | 0.710 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 17,317 | 0.173 | 20 | 24 | fits | 30,572 | 22 | 0.723 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 25,464 | 0.255 | 20 | 24 | fits | 30,548 | 22 | 0.725 |
| get_configuration | `aecp.get_configuration.if0` | 14,590 | 0.146 | 20 | 24 | fits | 26,643 | 22 | 0.727 |
| entity_available | `aecp.entity_available.if0` | 23,642 | 0.236 | 20 | 24 | fits | 27,478 | 22 | 0.729 |
| get_name | `aecp.get_name.if0` | 16,342 | 0.163 | 20 | 24 | fits | 29,358 | 22 | 0.723 |
| get_counters | `aecp.get_counters.if0` | 18,398 | 0.184 | 20 | 24 | fits | 32,224 | 29 | 0.732 |
| get_avb_info | `aecp.get_avb_info.if0` | 42,269 | 0.423 | 20 | 24 | fits | 46,500 | 52 | 0.682 |
| unknown_command | `aecp.unknown_command.if0` | 14,293 | 0.143 | 20 | 24 | fits | 26,869 | 22 | 0.719 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 23,960 | 0.240 | 20 | 24 | fits | 26,766 | 22 | 0.723 |
| set_name | `aecp.set_name.if0` | 36,745 | 0.367 | 20 | 24 | fits | 52,197 | 65 | 0.691 |
| lock_entity | `aecp.lock_entity.if0` | 28,523 | 0.285 | 20 | 24 | fits | 38,907 | 46 | 0.725 |
| unlock_entity | `aecp.unlock_entity.if0` | 38,521 | 0.385 | 20 | 24 | fits | 38,815 | 45 | 0.729 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 16,040 | 0.160 | 20 | 24 | fits | 28,748 | 20 | 0.752 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 31,747 | 0.317 | 20 | 24 | fits | 33,363 | 20 | 0.694 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 28,548 | 0.285 | 20 | 24 | fits | 30,626 | 20 | 0.739 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 19,470 | 0.195 | 20 | 24 | fits | 29,412 | 20 | 0.710 |
| get_configuration | `aecp.get_configuration.if1` | 26,652 | 0.267 | 20 | 24 | fits | 27,412 | 20 | 0.745 |
| entity_available | `aecp.entity_available.if1` | 17,146 | 0.171 | 20 | 24 | fits | 26,896 | 20 | 0.725 |
| get_name | `aecp.get_name.if1` | 28,837 | 0.288 | 20 | 24 | fits | 30,297 | 20 | 0.756 |
| get_counters | `aecp.get_counters.if1` | 28,092 | 0.281 | 20 | 24 | fits | 32,160 | 27 | 0.731 |
| get_avb_info | `aecp.get_avb_info.if1` | 18,599 | 0.186 | 20 | 24 | fits | 28,044 | 20 | 0.763 |
| unknown_command | `aecp.unknown_command.if1` | 27,187 | 0.272 | 20 | 24 | fits | 28,020 | 20 | 0.752 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 16,624 | 0.166 | 20 | 24 | fits | 26,236 | 20 | 0.721 |
| set_name | `aecp.set_name.if1` | 44,890 | 0.449 | 20 | 24 | fits | 46,530 | 25 | 0.750 |
| lock_entity | `aecp.lock_entity.if1` | 40,987 | 0.410 | 20 | 24 | fits | 40,277 | 49 | 0.714 |
| unlock_entity | `aecp.unlock_entity.if1` | 31,013 | 0.310 | 20 | 24 | fits | 38,633 | 48 | 0.691 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
