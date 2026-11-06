### 8x8

29 of 129 paths and 57 of 182 probe instances miss T_svc.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 1.000 (4.253) | fits | 0 acmp | 1 | 0 |
| BIND_RX | 1 | `acmp.bind_rx.if1` (acmp-cmd) | 16.940 (37.097) | MISS T_svc | 0 acmp | 1 | 1 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 1.151 (21.153) | fits | 0 acmp | 1 | 0 |
| DISCONNECT_TX | 1 | `acmp.disconnect_tx.if1` (acmp-cmd) | 8.848 (28.849) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 23.157 (53.481) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | `acmp.entity_available.if1` (acmp-disc) | 24.435 (53.481) | MISS ceiling | 1 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `acmp.entity_departing.if0` (acmp-disc) | 21.964 (29.868) | MISS ceiling | 0 adp | 1 | 1 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | `acmp.entity_departing.if1` (acmp-disc) | 23.209 (29.868) | MISS ceiling | 1 adp | 1 | 1 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 16.738 (36.617) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_RX_STATE | 1 | `acmp.get_rx_state.if1` (acmp-cmd) | 5.203 (25.091) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 16.491 (36.492) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_CONNECTION | 1 | `acmp.get_tx_connection.if1` (acmp-cmd) | 5.037 (25.038) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 16.547 (36.539) | MISS T_svc | 0 acmp | 1 | 1 |
| GET_TX_STATE | 1 | `acmp.get_tx_state.if1` (acmp-cmd) | 5.081 (25.074) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 12.473 (19.027) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX | 1 | `acmp.probe_tx.if1` (acmp-cmd) | 13.643 (25.065) | MISS T_svc | 0 acmp | 1 | 1 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 4.454 (21.415) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 1 | `acmp.probe_tx_response.if1` (acmp-cmd) | 7.156 (28.768) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 1.474 (21.462) | fits | 1 events | 1 | 0 |
| TMR_DELAY | 1 | `acmp.tmr_delay.if1` (acmp-noresp) | 0.772 (20.823) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 1.437 (26.167) | fits | 1 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 1 | `acmp.tmr_no_adp.if1` (acmp-disc) | 5.131 (24.661) | fits | 2 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 3.199 (20.777) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | `acmp.tmr_no_resp1.if1` (acmp-noresp) | 8.398 (45.349) | fits | 2 events | 1 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 2.926 (24.295) | fits | 0 events | 1 | 0 |
| the second TMR_NO_RESP | 1 | `acmp.tmr_no_resp2.if1` (acmp-noresp) | 6.645 (44.790) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 4.133 (24.636) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 1 | `acmp.tmr_no_tk.if1` (acmp-notk) | 1.851 (20.774) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 3.360 (24.260) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 1 | `acmp.tmr_retry.if1` (acmp-noresp) | 7.670 (45.722) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 1.336 (21.538) | fits | 0 acmp | 1 | 0 |
| UNBIND_RX | 1 | `acmp.unbind_rx.if1` (acmp-cmd) | 5.828 (34.272) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.630 (2.820) | fits | 0 adp | 2 | 0 |
| RCV_ADP_DISCOVER | 1 | `adp.discover.if1` (adp-discover) | 0.807 (2.820) | fits | 1 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.508 (2.643) | fits | 1 events | 1 | 0 |
| GM_CHANGE | 1 | `adp.gm_change.if1` (adp-gm) | 0.597 (2.643) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 0 | `adp.link_down.if0` (adp-link) | 0.491 (13.165) | fits | 1 events | 1 | 0 |
| LINK_DOWN | 1 | `adp.link_down.if1` (adp-link) | 5.568 (13.165) | fits | 1 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.079 (12.272) | fits | 0 events | 5 | 0 |
| LINK_UP | 1 | `adp.link_up.if1` (adp-advertise) | 0.870 (12.272) | fits | 0 events | 5 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 1.361 (5.453) | fits | 0 events | 1 | 0 |
| TMR_ADVERTISE expiry | 1 | `adp.tmr_advertise.if1` (adp-advertise) | 1.501 (2.219) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.380 (2.435) | fits | 0 events | 5 | 0 |
| TMR_DELAY expiry | 1 | `adp.tmr_delay.if1` (adp-advertise) | 1.817 (4.872) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 2.931 (4.571) | fits | 0 aecp | 1 | 0 |
| entity_available | 1 | `aecp.entity_available.if1` (aecp) | 2.927 (4.567) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 3.643 (13.527) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 1 | `aecp.get_avb_info.if1` (aecp) | 2.617 (4.258) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 2.459 (4.099) | fits | 0 aecp | 1 | 0 |
| get_configuration | 1 | `aecp.get_configuration.if1` (aecp) | 2.891 (4.531) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 2.771 (4.411) | fits | 0 aecp | 1 | 0 |
| get_counters | 1 | `aecp.get_counters.if1` (aecp) | 2.767 (4.407) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 2.619 (4.258) | fits | 0 aecp | 1 | 0 |
| get_name | 1 | `aecp.get_name.if1` (aecp) | 3.050 (4.690) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 3.353 (5.221) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp.lock_entity.if1` (aecp) | 2.921 (4.943) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 1.776 (3.416) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 1 | `aecp.mvu_get_milan_info.if1` (aecp) | 1.772 (3.412) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 3.598 (5.239) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 1 | `aecp.read_descriptor.t0.i0.c0.if1` (aecp) | 3.590 (5.231) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 2.700 (4.340) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 1 | `aecp.read_descriptor.t1.i0.c0.if1` (aecp) | 2.696 (4.336) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i9.c0.if0` (aecp) | 2.696 (4.337) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 2.667 (4.307) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 3.925 (5.565) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i7.c0.if0` (aecp) | 3.004 (4.644) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i7.c0.if0` (aecp) | 3.014 (4.655) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 2.793 (4.433) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 1 | `aecp.read_descriptor.t2.i0.c0.if1` (aecp) | 3.432 (6.900) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i71.c0.if0` (aecp) | 2.831 (4.471) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 3.306 (4.946) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (96 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 2.835 (4.476) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i8.c0.if0` (aecp) | 3.234 (4.874) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i8.c0.if0` (aecp) | 2.812 (4.452) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 2.716 (4.357) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 1.765 (3.397) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 1 | `aecp.register_unsolicited.if1` (aecp) | 1.761 (3.400) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 4.334 (7.353) | fits | 0 aecp | 1 | 0 |
| set_name | 1 | `aecp.set_name.if1` (aecp) | 3.958 (6.655) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 3.485 (7.151) | fits | 0 aecp | 1 | 0 |
| unknown_command | 1 | `aecp.unknown_command.if1` (aecp) | 2.882 (4.523) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 3.354 (5.221) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp.unlock_entity.if1` (aecp) | 2.921 (4.940) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 8.323 (9.980) | fits | 0 aecp | 1 | 0 |
| lock_entity | 1 | `aecp_fanout.lock_entity.if1` (aecp-fanout) | 9.793 (13.497) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 8.158 (9.649) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 1 | `aecp_fanout.set_clock_source.if1` (aecp-fanout) | 9.076 (12.614) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 9.377 (13.080) | fits | 0 aecp | 2 | 0 |
| set_control_identify_on | 1 | `aecp_fanout.set_control_identify_on.if1` (aecp-fanout) | 9.239 (12.942) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 11.816 (14.547) | MISS T_svc | 0 aecp | 1 | 1 |
| set_name | 1 | `aecp_fanout.set_name.if1` (aecp-fanout) | 12.889 (17.111) | MISS T_svc | 0 aecp | 1 | 1 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 8.363 (11.881) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 7.878 (9.535) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 1 | `aecp_fanout.unlock_entity.if1` (aecp-fanout) | 9.844 (13.550) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 63.301 (70.197) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 47.493 (66.570) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 53.264 (68.378) | MISS ceiling | 4 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 24.681 (41.300) | MISS T_svc | 16 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 118.835 (122.753) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 369.652 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 1.117 (5.180) | fits | 0 events | 1 | 0 |
| ANNOUNCE (TMR expiry) | 1 | `maap.announce.if1` (maap) | 1.151 (5.702) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.644 (2.620) | fits | 0 maap | 1 | 0 |
| conflicting PROBE -> DEFEND | 1 | `maap.defend.if1` (maap) | 0.644 (2.648) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.767 (7.346) | fits | 0 events | 1 | 0 |
| first PROBE (LINK_UP) | 1 | `maap.probe1.if1` (maap) | 0.769 (7.389) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.968 (5.180) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 1 | `maap.probe4.if1` (maap) | 1.002 (5.702) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 1.455 (5.482) | fits | 0 events | 2 | 0 |
| PROBE retransmission (TMR expiry) | 1 | `maap.probe2.if1` (maap) | 2.634 (7.148) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 14.736 | MISS T_svc | 0 acmp | 4 | 3 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 103.749 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 14.779 | MISS T_svc | 0 adp | 4 | 3 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 63.793 | MISS T_svc | 4 adp | 2 | 2 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 51.393 | MISS T_svc | 7 adp | 2 | 2 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 14.772 | MISS T_svc | 0 aecp | 4 | 3 |
| AECP record released under the composed load, last | 1 | `backlog-adp-refill.service.aecp.last.if1` (backlog-adp-refill) | 314.544 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 14.761 | MISS T_svc | 0 maap | 4 | 3 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 58.667 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp-refill.service.srp.first.if0` (backlog-adp-refill) | at least 593.250 | STARVED: never released | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 1 | `backlog-adp-refill.service.srp.last.if1` (backlog-adp-refill) | at least 593.229 | STARVED: never released | 31 srp | 4 | 4 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 7.822 (9.607) | fits | 0 srp | 1 | 0 |
| Domain RX -> declarations (JoinTime wait) | 1 | `srp.domain.if1` (srp) | 8.572 (10.272) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 3.324 (3.325) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 1 | `srp.listener_ready.if1` (srp) | 3.915 (3.916) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `srp.malformed.if0` (srp) | 3.072 (3.073) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 1 | `srp.malformed.if1` (srp) | 3.225 (3.226) | fits | 0 srp | 1 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 6.850 (7.346) | fits | 0 events | 1 | 0 |
| startup declarations (LINK_UP) | 1 | `srp.startup.if1` (srp) | 6.934 (7.374) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 150.558 | 20 | 834,091 (16.682) | yes | - |
| backlog-adp | 547.546 | 29 | 1,461,911 (29.238) | no | {'srp': 32} |
| backlog-adp-refill | 593.266 | 31 | 1,461,494 (29.230) | no | {'srp': 32} |
| backlog-owed | 369.702 | 40 | 627,532 (12.551) | yes | - |

Composed maximum over the 4 backlog windows: at least 1,461,911 CPU cycles (29.238 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 834,091 (16.682 ms), backlog.

| Path | Probe | CPU cycles | ms | T_svc (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 206,672 | 4.133 | 10 | 20 | fits | 1,231,782 | 166 (14) | 0.026 |
| TMR_NO_TK | `acmp.tmr_no_tk.if1` | 92,530 | 1.851 | 10 | 20 | fits | 1,038,694 | 127 (14) | 0.029 |
| LINK_UP | `adp.link_up.if0` | 3,936 | 0.079 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 43,497 | 0.870 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,976 | 0.380 | 10 | 200 | fits | 121,730 | 47 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 90,845 | 1.817 | 10 | 200 | fits | 121,869 | 47 (39) | 0.058 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 68,044 | 1.361 | 10 | 200 | fits | 106,893 | 19 (11) | 0.059 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if1` | 75,027 | 1.501 | 10 | 200 | fits | 4,047 | 9 (11) | 0.168 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 38,351 | 0.767 | 10 | 50 | fits | 367,306 | 160 | 0.042 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 72,761 | 1.455 | 10 | 50 | fits | 133,396 | 38 | 0.065 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 39,010 | 0.780 | 10 | 50 | fits | 133,367 | 38 | 0.065 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 48,408 | 0.968 | 10 | 50 | fits | 151,554 | 65 | 0.065 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 55,840 | 1.117 | 10 | 50 | fits | 151,554 | 65 | 0.065 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 32,203 | 0.644 | 10 | 50 | fits | 130,995 | 48 | 0.058 |
| first PROBE (LINK_UP) | `maap.probe1.if1` | 38,427 | 0.769 | 10 | 50 | fits | 369,454 | 160 | 0.042 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if1` | 131,719 | 2.634 | 10 | 50 | fits | 156,306 | 44 | 0.067 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if1` | 95,887 | 1.918 | 10 | 50 | fits | 134,846 | 38 | 0.063 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if1` | 50,095 | 1.002 | 10 | 50 | fits | 174,523 | 71 | 0.067 |
| ANNOUNCE (TMR expiry) | `maap.announce.if1` | 57,527 | 1.151 | 10 | 50 | fits | 174,523 | 71 | 0.067 |
| conflicting PROBE -> DEFEND | `maap.defend.if1` | 32,203 | 0.644 | 10 | 50 | fits | 132,414 | 48 | 0.057 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 159,957 | 3.199 | 10 | 20 | fits | 1,038,835 | 149 (35) | 0.029 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if1` | 419,887 | 8.398 | 10 | 20 | fits | 1,228,606 | 166 (35) | 0.026 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 146,277 | 2.926 | 10 | 20 | fits | 1,214,758 | 143 (14) | 0.026 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if1` | 332,268 | 6.645 | 10 | 20 | fits | 1,024,763 | 126 (14) | 0.028 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 167,976 | 3.360 | 10 | 20 | fits | 1,212,995 | 144 (14) | 0.026 |
| TMR_RETRY | `acmp.tmr_retry.if1` | 383,521 | 7.670 | 10 | 20 | fits | 1,073,085 | 152 (14) | 0.028 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 73,675 | 1.474 | 10 | 20 | fits | 1,073,085 | 152 (35) | 0.028 |
| TMR_DELAY | `acmp.tmr_delay.if1` | 38,586 | 0.772 | 10 | 20 | fits | 1,041,173 | 149 (35) | 0.029 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 342,484 | 6.850 | 10 | 18 | fits | 367,306 | 160 | 0.042 |
| startup declarations (LINK_UP) | `srp.startup.if1` | 346,725 | 6.934 | 10 | 18 | fits | 368,710 | 160 | 0.042 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 166,196 | 3.324 | 10 | 18 | fits | 166,228 | 29 | 0.068 |
| malformed MRPDU discard | `srp.malformed.if0` | 153,595 | 3.072 | 10 | 18 | fits | 153,627 | 36 | 0.059 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 391,123 | 7.822 | 210 | 218 | fits | 480,370 | 142 | 0.046 |
| Listener Ready RX (registrar) | `srp.listener_ready.if1` | 195,746 | 3.915 | 10 | 18 | fits | 195,778 | 36 | 0.069 |
| malformed MRPDU discard | `srp.malformed.if1` | 161,273 | 3.225 | 10 | 18 | fits | 161,305 | 36 | 0.057 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if1` | 428,615 | 8.572 | 210 | 218 | fits | 513,599 | 149 | 0.047 |
| an event behind 15 others | `backlog.event.if0` | 1,234,064 | 24.681 | 10 | 200 | MISS T_svc | 834,091 | 393 | 0.059 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 3,165,045 | 63.301 | 10 | 20 | MISS ceiling | 469,878 | 258 | 0.041 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 738,926 | 14.779 | 10 | 200 | MISS T_svc | 739,030 | 394 | 0.054 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 2,569,657 | 51.393 | 10 | 200 | MISS T_svc | 505,082 | 326 | 0.042 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 736,797 | 14.736 | 10 | 20 | MISS T_svc | 739,030 | 394 | 0.054 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 3,507,219 | 70.144 | 10 | 20 | MISS ceiling | 469,878 | 258 | 0.041 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 738,589 | 14.772 | 10 | 24 | MISS T_svc | 739,030 | 394 | 0.054 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 6,543,040 | 130.861 | 10 | 24 | MISS ceiling | 323,446 | 171 | 0.049 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 738,069 | 14.761 | 10 | 50 | MISS T_svc | 739,030 | 394 | 0.054 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 2,568,909 | 51.378 | 10 | 50 | MISS ceiling | 505,082 | 326 | 0.042 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 2,063,795 | 41.276 | 10 | 18 | MISS ceiling | 834,091 | 393 | 0.059 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 7,213,371 | 144.267 | 10 | 18 | MISS ceiling | 178,736 | 54 | 0.065 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 2,374,666 | 47.493 | 10 | 20 | MISS ceiling | 1,163,293 | 403 | 0.031 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 592,554 | 11.851 | 10 | 200 | MISS T_svc | 989,246 | 427 | 0.033 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 2,931,503 | 58.630 | 10 | 200 | MISS T_svc | 1,163,293 | 403 | 0.031 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 593,010 | 11.860 | 10 | 20 | MISS T_svc | 989,246 | 427 | 0.033 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 5,165,491 | 103.310 | 10 | 20 | MISS ceiling | 1,170,522 | 319 | 0.029 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 594,802 | 11.896 | 10 | 24 | MISS T_svc | 989,246 | 427 | 0.033 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 15,705,533 | 314.111 | 10 | 24 | MISS ceiling | 1,020,456 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 594,282 | 11.886 | 10 | 50 | MISS T_svc | 989,246 | 427 | 0.033 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 2,933,341 | 58.667 | 10 | 50 | MISS ceiling | 1,163,293 | 403 | 0.031 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 27,376,471 | 547.529 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 27,375,464 | 547.509 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 2,663,212 | 53.264 | 10 | 20 | MISS ceiling | 1,233,252 | 351 | 0.028 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 592,554 | 11.851 | 10 | 200 | MISS T_svc | 989,246 | 427 | 0.033 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 3,189,669 | 63.793 | 10 | 200 | MISS T_svc | 1,233,252 | 351 | 0.028 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 593,010 | 11.860 | 10 | 20 | MISS T_svc | 989,246 | 427 | 0.033 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 5,187,475 | 103.749 | 10 | 20 | MISS ceiling | 1,233,252 | 351 | 0.028 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 594,802 | 11.896 | 10 | 24 | MISS T_svc | 989,246 | 427 | 0.033 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 15,727,197 | 314.544 | 10 | 24 | MISS ceiling | 1,020,478 | 232 | 0.029 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 594,282 | 11.886 | 10 | 50 | MISS T_svc | 989,246 | 427 | 0.033 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 2,877,797 | 57.556 | 10 | 50 | MISS ceiling | 1,107,749 | 396 | 0.031 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 29,662,475 | 593.250 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 29,661,468 | 593.229 | 10 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 5,941,734 | 118.835 | 10 | 20 | MISS ceiling | 422,237 | 193 | 0.048 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,482,591 | 369.652 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,482,553 | 369.651 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,482,516 | 369.650 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,482,478 | 369.650 | 10 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 494,385 | 9.888 | 10 | 200 | fits | 501,772 | 346 | 0.041 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 2,151,187 | 43.024 | 10 | 200 | MISS T_svc | 549,384 | 302 | 0.044 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 492,256 | 9.845 | 10 | 20 | fits | 501,772 | 346 | 0.041 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 3,020,014 | 60.400 | 10 | 20 | MISS ceiling | 401,216 | 122 | 0.048 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 494,048 | 9.881 | 10 | 24 | fits | 501,772 | 346 | 0.041 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 7,167,031 | 143.341 | 10 | 24 | MISS ceiling | 297,793 | 146 | 0.046 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 493,528 | 9.871 | 10 | 50 | fits | 501,772 | 346 | 0.041 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 2,150,439 | 43.009 | 10 | 50 | MISS T_svc | 549,384 | 302 | 0.044 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 1,601,023 | 32.020 | 10 | 18 | MISS ceiling | 627,532 | 345 | 0.050 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 7,819,794 | 156.396 | 10 | 18 | MISS ceiling | 225,230 | 54 | 0.067 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 1,098,217 | 21.964 | 10 | 20 | MISS ceiling | 1,493,409 | 208 (29) | 0.024 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if1` | 1,160,452 | 23.209 | 10 | 20 | MISS ceiling | 1,493,409 | 208 (29) | 0.024 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 1,157,862 | 23.157 | 10 | 20 | MISS ceiling | 1,305,864 | 202 (35) | 0.026 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if1` | 1,221,733 | 24.435 | 10 | 20 | MISS ceiling | 1,305,864 | 202 (35) | 0.026 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 71,829 | 1.437 | 10 | 20 | fits | 1,308,369 | 143 (12) | 0.023 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if1` | 256,569 | 5.131 | 10 | 20 | fits | 1,233,049 | 166 (12) | 0.026 |
| LINK_UP | `adp.link_up.if0` | 3,936 | 0.079 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 43,497 | 0.870 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,976 | 0.380 | 10 | 200 | fits | 121,730 | 47 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 90,845 | 1.817 | 10 | 200 | fits | 121,869 | 47 (39) | 0.058 |
| LINK_DOWN | `adp.link_down.if0` | 24,558 | 0.491 | 10 | 200 | fits | 658,263 | 58 (9) | 0.080 |
| LINK_DOWN | `adp.link_down.if1` | 278,386 | 5.568 | 10 | 200 | fits | 658,263 | 58 (9) | 0.080 |
| LINK_UP | `adp.link_up.if0` | 3,936 | 0.079 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 43,497 | 0.870 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,976 | 0.380 | 10 | 200 | fits | 121,730 | 47 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 90,845 | 1.817 | 10 | 200 | fits | 121,869 | 47 (39) | 0.058 |
| GM_CHANGE | `adp.gm_change.if0` | 25,424 | 0.508 | 10 | 200 | fits | 132,165 | 34 (11) | 0.066 |
| GM_CHANGE | `adp.gm_change.if1` | 29,847 | 0.597 | 10 | 200 | fits | 132,165 | 34 (11) | 0.066 |
| LINK_UP | `adp.link_up.if0` | 3,936 | 0.079 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 43,497 | 0.870 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,976 | 0.380 | 10 | 200 | fits | 121,730 | 47 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 90,845 | 1.817 | 10 | 200 | fits | 121,869 | 47 (39) | 0.058 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 31,515 | 0.630 | 10 | 200 | fits | 140,995 | 73 (31) | 0.060 |
| RCV_ADP_DISCOVER | `adp.discover.if1` | 40,341 | 0.807 | 10 | 200 | fits | 140,995 | 73 (31) | 0.060 |
| LINK_UP | `adp.link_up.if0` | 3,936 | 0.079 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| LINK_UP | `adp.link_up.if1` | 43,497 | 0.870 | 10 | 200 | fits | 613,620 | 304 (11) | 0.038 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 18,976 | 0.380 | 10 | 200 | fits | 121,730 | 47 (39) | 0.058 |
| TMR_DELAY expiry | `adp.tmr_delay.if1` | 90,845 | 1.817 | 10 | 200 | fits | 121,869 | 47 (39) | 0.058 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 31,515 | 0.630 | 10 | 200 | fits | 132,390 | 45 (31) | 0.061 |
| set_name | `aecp_fanout.set_name.if0` | 590,822 | 11.816 | 10 | 24 | MISS T_svc | 727,337 | 1179 | 0.036 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 407,912 | 8.158 | 10 | 24 | fits | 482,428 | 620 | 0.051 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 374,015 | 7.480 | 10 | 24 | fits | 456,839 | 580 | 0.047 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 468,871 | 9.377 | 10 | 24 | fits | 456,351 | 580 | 0.047 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 418,139 | 8.363 | 10 | 24 | fits | 433,071 | 592 | 0.051 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 416,128 | 8.323 | 10 | 24 | fits | 499,023 | 686 | 0.048 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 393,906 | 7.878 | 10 | 24 | fits | 476,730 | 679 | 0.046 |
| set_name | `aecp_fanout.set_name.if1` | 644,463 | 12.889 | 10 | 24 | MISS T_svc | 657,786 | 1132 | 0.034 |
| set_clock_source | `aecp_fanout.set_clock_source.if1` | 453,817 | 9.076 | 10 | 24 | fits | 483,780 | 620 | 0.051 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if1` | 461,950 | 9.239 | 10 | 24 | fits | 479,392 | 587 | 0.050 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if1` | 448,794 | 8.976 | 10 | 24 | fits | 457,229 | 580 | 0.047 |
| lock_entity | `aecp_fanout.lock_entity.if1` | 489,639 | 9.793 | 10 | 24 | fits | 476,392 | 679 | 0.046 |
| unlock_entity | `aecp_fanout.unlock_entity.if1` | 492,188 | 9.844 | 10 | 24 | fits | 478,289 | 679 | 0.046 |
| BIND_RX | `acmp.bind_rx.if0` | 49,989 | 1.000 | 10 | 20 | fits | 212,625 | 83 (77) | 0.048 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 222,692 | 4.454 | 10 | 20 | fits | 1,070,728 | 154 (32) | 0.029 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 836,905 | 16.738 | 10 | 20 | MISS T_svc | 953,488 | 159 (47) | 0.030 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 66,815 | 1.336 | 10 | 20 | fits | 1,076,907 | 172 (50) | 0.029 |
| PROBE_TX | `acmp.probe_tx.if0` | 623,651 | 12.473 | 10 | 20 | MISS T_svc | 951,332 | 161 (48) | 0.030 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 827,330 | 16.547 | 10 | 20 | MISS T_svc | 951,108 | 160 (48) | 0.030 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 57,572 | 1.151 | 10 | 20 | fits | 1,057,630 | 170 (48) | 0.028 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 824,550 | 16.491 | 10 | 20 | MISS T_svc | 949,263 | 160 (48) | 0.029 |
| BIND_RX | `acmp.bind_rx.if1` | 846,999 | 16.940 | 10 | 20 | MISS T_svc | 979,065 | 190 (77) | 0.031 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if1` | 357,817 | 7.156 | 10 | 20 | fits | 1,438,379 | 187 (32) | 0.025 |
| GET_RX_STATE | `acmp.get_rx_state.if1` | 260,159 | 5.203 | 10 | 20 | fits | 1,254,563 | 185 (47) | 0.027 |
| UNBIND_RX | `acmp.unbind_rx.if1` | 291,386 | 5.828 | 10 | 20 | fits | 1,713,585 | 404 (50) | 0.026 |
| PROBE_TX | `acmp.probe_tx.if1` | 682,137 | 13.643 | 10 | 20 | MISS T_svc | 1,253,272 | 187 (48) | 0.027 |
| GET_TX_STATE | `acmp.get_tx_state.if1` | 254,066 | 5.081 | 10 | 20 | fits | 1,253,711 | 186 (48) | 0.027 |
| DISCONNECT_TX | `acmp.disconnect_tx.if1` | 442,415 | 8.848 | 10 | 20 | fits | 1,442,473 | 203 (48) | 0.025 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if1` | 251,848 | 5.037 | 10 | 20 | fits | 1,251,885 | 186 (48) | 0.027 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 88,249 | 1.765 | 10 | 24 | fits | 169,868 | 49 | 0.051 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 179,914 | 3.598 | 10 | 24 | fits | 261,929 | 134 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 134,986 | 2.700 | 10 | 24 | fits | 216,998 | 75 | 0.043 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 139,639 | 2.793 | 10 | 24 | fits | 221,651 | 86 | 0.042 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i8.c0.if0` | 161,704 | 3.234 | 10 | 24 | fits | 243,719 | 92 | 0.046 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i8.c0.if0` | 140,577 | 2.812 | 10 | 24 | fits | 222,592 | 85 | 0.042 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 135,817 | 2.716 | 10 | 24 | fits | 217,832 | 74 | 0.043 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i9.c0.if0` | 134,810 | 2.696 | 10 | 24 | fits | 216,825 | 70 | 0.043 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 133,351 | 2.667 | 10 | 24 | fits | 215,363 | 67 | 0.043 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 196,230 | 3.925 | 10 | 24 | fits | 278,242 | 169 | 0.041 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i7.c0.if0` | 150,185 | 3.004 | 10 | 24 | fits | 232,197 | 61 | 0.048 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i7.c0.if0` | 150,723 | 3.014 | 10 | 24 | fits | 232,735 | 61 | 0.048 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i71.c0.if0` | 141,563 | 2.831 | 10 | 24 | fits | 223,575 | 71 | 0.041 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 165,297 | 3.306 | 10 | 24 | fits | 247,309 | 84 | 0.046 |
| READ_DESCRIPTOR (96 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 141,770 | 2.835 | 10 | 24 | fits | 223,782 | 73 | 0.041 |
| get_configuration | `aecp.get_configuration.if0` | 122,966 | 2.459 | 10 | 24 | fits | 204,934 | 49 | 0.044 |
| entity_available | `aecp.entity_available.if0` | 146,542 | 2.931 | 10 | 24 | fits | 228,545 | 60 | 0.049 |
| get_name | `aecp.get_name.if0` | 130,938 | 2.619 | 10 | 24 | fits | 212,909 | 66 | 0.044 |
| get_counters | `aecp.get_counters.if0` | 138,535 | 2.771 | 10 | 24 | fits | 220,550 | 87 | 0.044 |
| get_avb_info | `aecp.get_avb_info.if0` | 182,157 | 3.643 | 10 | 24 | fits | 676,332 | 272 | 0.029 |
| unknown_command | `aecp.unknown_command.if0` | 174,237 | 3.485 | 10 | 24 | fits | 204,960 | 50 | 0.044 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 88,818 | 1.776 | 10 | 24 | fits | 170,789 | 53 | 0.051 |
| set_name | `aecp.set_name.if0` | 216,679 | 4.334 | 10 | 24 | fits | 367,645 | 156 | 0.037 |
| lock_entity | `aecp.lock_entity.if0` | 167,663 | 3.353 | 10 | 24 | fits | 261,060 | 97 | 0.048 |
| unlock_entity | `aecp.unlock_entity.if0` | 167,713 | 3.354 | 10 | 24 | fits | 261,039 | 97 | 0.048 |
| register_unsolicited | `aecp.register_unsolicited.if1` | 88,037 | 1.761 | 10 | 24 | fits | 169,992 | 47 | 0.051 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if1` | 179,514 | 3.590 | 10 | 24 | fits | 261,548 | 132 | 0.044 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if1` | 134,789 | 2.696 | 10 | 24 | fits | 216,823 | 73 | 0.043 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if1` | 171,576 | 3.432 | 10 | 24 | fits | 221,787 | 85 | 0.042 |
| get_configuration | `aecp.get_configuration.if1` | 144,534 | 2.891 | 10 | 24 | fits | 226,554 | 54 | 0.049 |
| entity_available | `aecp.entity_available.if1` | 146,338 | 2.927 | 10 | 24 | fits | 228,358 | 58 | 0.049 |
| get_name | `aecp.get_name.if1` | 152,493 | 3.050 | 10 | 24 | fits | 234,513 | 71 | 0.048 |
| get_counters | `aecp.get_counters.if1` | 138,335 | 2.767 | 10 | 24 | fits | 220,367 | 85 | 0.044 |
| get_avb_info | `aecp.get_avb_info.if1` | 130,860 | 2.617 | 10 | 24 | fits | 212,880 | 47 | 0.043 |
| unknown_command | `aecp.unknown_command.if1` | 144,121 | 2.882 | 10 | 24 | fits | 226,141 | 54 | 0.049 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if1` | 88,618 | 1.772 | 10 | 24 | fits | 170,606 | 51 | 0.051 |
| set_name | `aecp.set_name.if1` | 197,897 | 3.958 | 10 | 24 | fits | 332,766 | 149 | 0.037 |
| lock_entity | `aecp.lock_entity.if1` | 146,063 | 2.921 | 10 | 24 | fits | 247,163 | 109 | 0.044 |
| unlock_entity | `aecp.unlock_entity.if1` | 146,050 | 2.921 | 10 | 24 | fits | 246,979 | 109 | 0.043 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-notk`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `acmp-noresp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `acmp-disc`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `aecp-fanout`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `acmp-cmd`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
- `aecp`: wait quiet TIMEOUT
