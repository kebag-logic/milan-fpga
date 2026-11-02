### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 81 paths and 6 of 141 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.210 (0.386) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.092 (0.216) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.056 (0.202) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.059 (0.267) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.108 (0.254) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.092 (0.217) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.107 (0.238) | fits | 0 acmp | 1 | 0 |
| PROBE_TX | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.100 (0.234) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.067 (0.250) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.168 (0.389) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.179 (0.398) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.175 (0.395) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.095 (0.322) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.081 (0.372) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.116 (0.336) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.126 (0.344) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.026 (0.097) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.012 (0.085) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.015 (0.194) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.016 (0.525) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.073 (0.143) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.104 (0.250) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.131 (0.253) | fits | 0 aecp | 1 | 0 |
| get_avb_info | 0 | `aecp.get_avb_info.if0` (aecp) | 0.141 (0.268) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.149 (0.281) | fits | 0 aecp | 1 | 0 |
| get_counters | 0 | `aecp.get_counters.if0` (aecp) | 0.166 (0.292) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.175 (0.313) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.207 (0.367) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.137 (0.263) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.189 (0.316) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.177 (0.313) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.147 (0.275) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.137 (0.262) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.194 (0.332) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.133 (0.259) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.162 (0.298) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.145 (0.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.144 (0.269) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.176 (0.313) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.144 (0.272) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.181 (0.319) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.154 (0.284) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.164 (0.300) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.146 (0.272) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.332 (0.596) | fits | 0 aecp | 1 | 0 |
| unknown_command | 0 | `aecp.unknown_command.if0` (aecp) | 0.152 (0.287) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.141 (0.231) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.423 (0.564) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.424 (0.576) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.462 (0.744) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.488 (0.640) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.437 (0.587) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.603 (0.848) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.415 (0.650) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.382 (0.532) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.448 (3.761) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.734 (3.701) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.117 (0.341) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.880 (1.447) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.074 (62.287) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.145 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.307 (0.476) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.121 (0.291) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.079 (0.146) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.102 (0.525) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.102 (0.291) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.132 (0.287) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 0.748 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 5.163 | fits | 11 acmp | 5 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 0.791 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.648 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 0.784 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.656 | MISS ceiling | 15 aecp | 5 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 0.774 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.684 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.787 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.946 | fits | 31 srp | 5 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.617 (0.710) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.331 (0.331) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.126 (0.126) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.785 (0.866) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 6.362 | 19 | 79,854 (0.799) | yes | - |
| backlog-adp | 0 | 10.216 | 17 | 106,981 (1.070) | yes | - |
| backlog-adp-refill | 0 | 40.493 | 31 | 106,981 (1.070) | yes | - |
| backlog-owed | 0 | 360.196 | 65 | 104,099 (1.041) | yes | - |
| fixture | 0 | 0.949 | 2 | 72,384 (0.724) | yes | - |

Composed maximum over the 4 backlog windows: 106,981 CPU cycles (1.070 ms), backlog-adp.
Over the windows that released their whole load only: 106,981 (1.070 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 2468 | 0 | 121,085 (1.211) | fits |
| adp-advertise | 591 | 0 | 52,544 (0.525) | fits |
| acmp-noresp | 1533 | 0 | 120,159 (1.202) | fits |
| srp | 284 | 0 | 71,045 (0.710) | fits |
| backlog | 293 | 0 | 79,854 (0.799) | fits |
| backlog-adp | 310 | 0 | 106,981 (1.070) | fits |
| backlog-adp-refill | 324 | 0 | 106,981 (1.070) | fits |
| backlog-owed | 350 | 0 | 104,099 (1.041) | fits |
| acmp-disc | 730 | 0 | 120,561 (1.206) | fits |
| maap | 175 | 0 | 52,544 (0.525) | fits |
| adp-link | 87 | 0 | 52,544 (0.525) | fits |
| adp-gm | 86 | 0 | 52,544 (0.525) | fits |
| adp-discover | 86 | 0 | 52,544 (0.525) | fits |
| control | 86 | 0 | 52,544 (0.525) | fits |
| aecp-fanout | 109 | 0 | 69,671 (0.697) | fits |
| acmp-cmd | 81 | 0 | 52,544 (0.525) | fits |
| aecp | 108 | 0 | 52,544 (0.525) | fits |
| fixture | 136 | 0 | 72,384 (0.724) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,091 | 0.081 | 20 | 20 | fits | 26,761 | 20 (14) | 0.888 |
| LINK_UP | `adp.link_up.if0` | 1,606 | 0.016 | 20 | 200 | fits | 52,544 | 49 (11) | 0.747 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,427 | 0.104 | 20 | 200 | fits | 15,588 | 25 (39) | 0.593 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 7,322 | 0.073 | 20 | 200 | fits | 1,562 | 9 (11) | 0.500 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 17,509 | 0.175 | 20 | 20 | fits | 24,921 | 23 (35) | 0.768 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 9,489 | 0.095 | 20 | 20 | fits | 19,164 | 18 (14) | 0.841 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 11,574 | 0.116 | 20 | 20 | fits | 19,097 | 19 (14) | 0.830 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 16,788 | 0.168 | 20 | 20 | fits | 25,246 | 23 (35) | 0.775 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 78,498 | 0.785 | 18 | 18 | fits | 34,007 | 13 | 0.835 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 33,060 | 0.331 | 18 | 18 | fits | 33,125 | 14 | 0.898 |
| malformed MRPDU discard | `srp.malformed.if0` | 11,783 | 0.118 | 18 | 18 | fits | 11,848 | 14 | 0.610 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 61,721 | 0.617 | 218 | 218 | fits | 71,045 | 21 | 0.875 |
| an event behind 15 others | `backlog.event.if0` | 87,992 | 0.880 | 20 | 200 | fits | 65,371 | 104 | 0.489 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 344,843 | 3.448 | 20 | 20 | fits | 47,320 | 44 | 0.491 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 79,073 | 0.791 | 20 | 200 | fits | 79,281 | 138 | 0.509 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 280,231 | 2.802 | 20 | 200 | fits | 56,542 | 55 | 0.549 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 74,814 | 0.748 | 20 | 20 | fits | 79,281 | 138 | 0.509 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 370,786 | 3.708 | 20 | 20 | fits | 47,320 | 44 | 0.491 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 78,399 | 0.784 | 20 | 24 | fits | 79,281 | 138 | 0.509 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 587,813 | 5.878 | 20 | 24 | fits | 21,277 | 29 | 0.460 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 77,359 | 0.774 | 20 | 50 | fits | 79,281 | 138 | 0.509 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 278,736 | 2.787 | 20 | 50 | fits | 56,542 | 55 | 0.549 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 278,671 | 2.787 | 18 | 18 | fits | 56,542 | 55 | 0.549 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 612,120 | 6.121 | 18 | 18 | fits | 8,643 | 17 | 0.314 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 273,392 | 2.734 | 20 | 20 | fits | 98,410 | 90 | 0.673 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 70,408 | 0.704 | 20 | 200 | fits | 75,090 | 135 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 364,763 | 3.648 | 20 | 200 | fits | 98,410 | 90 | 0.673 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 71,320 | 0.713 | 20 | 20 | fits | 75,090 | 135 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 516,330 | 5.163 | 20 | 20 | fits | 73,042 | 44 | 0.683 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 74,905 | 0.749 | 20 | 24 | fits | 75,090 | 135 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 967,300 | 9.673 | 20 | 24 | fits | 44,001 | 29 | 0.725 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 73,865 | 0.739 | 20 | 50 | fits | 75,090 | 135 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 368,439 | 3.684 | 20 | 50 | fits | 98,410 | 90 | 0.673 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 180,391 | 1.804 | 18 | 18 | fits | 106,981 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 994,592 | 9.946 | 18 | 18 | fits | 29,827 | 19 | 0.782 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 11,669 | 0.117 | 20 | 20 | fits | 20,805 | 20 | 0.767 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 70,408 | 0.704 | 20 | 200 | fits | 75,090 | 135 | 0.481 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,551 | 0.266 | 20 | 200 | fits | 20,805 | 20 | 0.767 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 71,320 | 0.713 | 20 | 20 | fits | 75,090 | 135 | 0.481 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 505,904 | 5.059 | 20 | 20 | fits | 73,010 | 44 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 74,905 | 0.749 | 20 | 24 | fits | 75,090 | 135 | 0.481 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 956,888 | 9.569 | 20 | 24 | fits | 44,066 | 29 | 0.727 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 73,865 | 0.739 | 20 | 50 | fits | 75,090 | 135 | 0.481 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 351,979 | 3.520 | 20 | 50 | fits | 81,950 | 71 | 0.647 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 180,391 | 1.804 | 18 | 18 | fits | 106,981 | 138 | 0.608 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 984,114 | 9.841 | 18 | 18 | fits | 29,761 | 19 | 0.780 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,207,362 | 62.074 | 20 | 20 | MISS ceiling | 26,106 | 25 | 0.570 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,014,523 | 360.145 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,014,448 | 360.144 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,014,373 | 360.144 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,014,298 | 360.143 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 75,955 | 0.760 | 20 | 200 | fits | 71,012 | 129 | 0.484 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 345,380 | 3.454 | 20 | 200 | fits | 79,611 | 67 | 0.663 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 71,696 | 0.717 | 20 | 20 | fits | 71,012 | 129 | 0.484 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 432,387 | 4.324 | 20 | 20 | fits | 33,184 | 24 | 0.732 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 75,281 | 0.753 | 20 | 24 | fits | 71,012 | 129 | 0.484 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,265,566 | 62.656 | 20 | 24 | MISS ceiling | 20,036 | 21 | 0.574 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 74,241 | 0.742 | 20 | 50 | fits | 71,012 | 129 | 0.484 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 343,885 | 3.439 | 20 | 50 | fits | 79,611 | 67 | 0.663 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 177,885 | 1.779 | 18 | 18 | fits | 104,099 | 131 | 0.631 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 797,722 | 7.977 | 18 | 18 | fits | 29,696 | 20 | 0.780 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 4,084 | 0.041 | 20 | 20 | fits | 17,959 | 14 (29) | 0.736 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 5,552 | 0.056 | 20 | 20 | fits | 20,244 | 20 (35) | 0.764 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 17,899 | 0.179 | 20 | 20 | fits | 25,085 | 23 (12) | 0.769 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 10,172 | 0.102 | 20 | 50 | fits | 52,544 | 49 | 0.747 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 13,174 | 0.132 | 20 | 50 | fits | 15,796 | 37 | 0.634 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 12,346 | 0.123 | 20 | 50 | fits | 15,571 | 37 | 0.626 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 10,166 | 0.102 | 20 | 50 | fits | 21,650 | 64 | 0.568 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 12,083 | 0.121 | 20 | 50 | fits | 21,650 | 64 | 0.568 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 7,864 | 0.079 | 20 | 50 | fits | 14,646 | 32 | 0.534 |
| LINK_UP | `adp.link_up.if0` | 1,606 | 0.016 | 20 | 200 | fits | 52,544 | 49 (11) | 0.747 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,427 | 0.104 | 20 | 200 | fits | 15,588 | 25 (39) | 0.593 |
| LINK_DOWN | `adp.link_down.if0` | 1,175 | 0.012 | 20 | 200 | fits | 18,184 | 22 (9) | 0.768 |
| LINK_UP | `adp.link_up.if0` | 1,606 | 0.016 | 20 | 200 | fits | 52,544 | 49 (11) | 0.747 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,427 | 0.104 | 20 | 200 | fits | 15,588 | 25 (39) | 0.593 |
| GM_CHANGE | `adp.gm_change.if0` | 1,216 | 0.012 | 20 | 200 | fits | 8,462 | 18 (11) | 0.513 |
| LINK_UP | `adp.link_up.if0` | 1,606 | 0.016 | 20 | 200 | fits | 52,544 | 49 (11) | 0.747 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,427 | 0.104 | 20 | 200 | fits | 15,588 | 25 (39) | 0.593 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 2,647 | 0.026 | 20 | 200 | fits | 9,681 | 17 (31) | 0.571 |
| LINK_UP | `adp.link_up.if0` | 1,606 | 0.016 | 20 | 200 | fits | 52,544 | 49 (11) | 0.747 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 10,427 | 0.104 | 20 | 200 | fits | 15,588 | 25 (39) | 0.593 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 2,647 | 0.026 | 20 | 200 | fits | 9,681 | 17 (31) | 0.571 |
| set_name | `aecp_fanout.set_name.if0` | 60,282 | 0.603 | 20 | 24 | fits | 69,671 | 121 | 0.385 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 48,755 | 0.488 | 20 | 24 | fits | 51,165 | 111 | 0.411 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 39,027 | 0.390 | 20 | 24 | fits | 42,886 | 111 | 0.326 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 43,749 | 0.437 | 20 | 24 | fits | 42,984 | 111 | 0.341 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 46,181 | 0.462 | 20 | 24 | fits | 56,926 | 99 | 0.381 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 42,302 | 0.423 | 20 | 24 | fits | 56,411 | 99 | 0.393 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 41,491 | 0.415 | 20 | 24 | fits | 47,600 | 99 | 0.369 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 42,433 | 0.424 | 20 | 24 | fits | 45,979 | 111 | 0.372 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 38,198 | 0.382 | 20 | 24 | fits | 44,511 | 111 | 0.331 |
| BIND_RX | `acmp.bind_rx.if0` | 20,795 | 0.208 | 20 | 20 | fits | 39,844 | 29 (77) | 0.752 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 6,697 | 0.067 | 20 | 20 | fits | 24,963 | 20 (32) | 0.825 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,807 | 0.108 | 20 | 20 | fits | 25,430 | 17 (47) | 0.734 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 12,559 | 0.126 | 20 | 20 | fits | 34,370 | 20 (50) | 0.807 |
| PROBE_TX | `acmp.probe_tx.if0` | 9,993 | 0.100 | 20 | 20 | fits | 23,352 | 19 (48) | 0.697 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 10,724 | 0.107 | 20 | 20 | fits | 23,754 | 18 (48) | 0.705 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,221 | 0.092 | 20 | 20 | fits | 21,634 | 18 (48) | 0.635 |
| GET_TX_CONNECTION | `acmp.get_tx_connection.if0` | 9,198 | 0.092 | 20 | 20 | fits | 21,686 | 18 (48) | 0.639 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 14,555 | 0.146 | 20 | 24 | fits | 19,743 | 22 | 0.740 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 18,898 | 0.189 | 20 | 24 | fits | 22,362 | 22 | 0.658 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 17,664 | 0.177 | 20 | 24 | fits | 18,008 | 22 | 0.647 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,469 | 0.145 | 20 | 24 | fits | 17,874 | 22 | 0.633 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 18,084 | 0.181 | 20 | 24 | fits | 18,507 | 22 | 0.618 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 15,402 | 0.154 | 20 | 24 | fits | 19,015 | 22 | 0.649 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 16,372 | 0.164 | 20 | 24 | fits | 16,570 | 22 | 0.616 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 14,735 | 0.147 | 20 | 24 | fits | 18,190 | 22 | 0.669 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 13,747 | 0.137 | 20 | 24 | fits | 16,924 | 22 | 0.647 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 19,392 | 0.194 | 20 | 24 | fits | 19,830 | 22 | 0.511 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 13,285 | 0.133 | 20 | 24 | fits | 16,599 | 22 | 0.667 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 16,184 | 0.162 | 20 | 24 | fits | 16,466 | 22 | 0.633 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 14,360 | 0.144 | 20 | 24 | fits | 17,607 | 22 | 0.650 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 17,611 | 0.176 | 20 | 24 | fits | 17,955 | 22 | 0.633 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 14,435 | 0.144 | 20 | 24 | fits | 17,890 | 22 | 0.669 |
| get_configuration | `aecp.get_configuration.if0` | 14,908 | 0.149 | 20 | 24 | fits | 14,743 | 22 | 0.610 |
| entity_available | `aecp.entity_available.if0` | 13,076 | 0.131 | 20 | 24 | fits | 16,022 | 22 | 0.643 |
| get_name | `aecp.get_name.if0` | 17,532 | 0.175 | 20 | 24 | fits | 18,021 | 22 | 0.674 |
| get_counters | `aecp.get_counters.if0` | 16,578 | 0.166 | 20 | 24 | fits | 19,734 | 27 | 0.673 |
| get_avb_info | `aecp.get_avb_info.if0` | 14,055 | 0.141 | 20 | 24 | fits | 17,223 | 22 | 0.707 |
| unknown_command | `aecp.unknown_command.if0` | 15,180 | 0.152 | 20 | 24 | fits | 15,353 | 22 | 0.645 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,669 | 0.137 | 20 | 24 | fits | 16,755 | 22 | 0.692 |
| set_name | `aecp.set_name.if0` | 33,212 | 0.332 | 20 | 24 | fits | 46,319 | 46 | 0.677 |
| lock_entity | `aecp.lock_entity.if0` | 20,735 | 0.207 | 20 | 24 | fits | 25,492 | 36 | 0.708 |
| unlock_entity | `aecp.unlock_entity.if0` | 14,097 | 0.141 | 20 | 24 | fits | 23,082 | 36 | 0.631 |
| LINK_UP | `fixture.link_up.if0` | 1,606 | 0.016 | 20 | 200 | fits | 52,544 | 49 (11) | 0.747 |
| malformed MRPDU discard | `fixture.malformed.if0` | 12,576 | 0.126 | 18 | 18 | fits | 12,641 | 14 | 0.689 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 30,722 | 0.307 | 20 | 24 | fits | 47,572 | 46 | 0.702 |
| LINK_DOWN | `fixture.link_down.if0` | 1,502 | 0.015 | 20 | 200 | fits | 19,430 | 22 (9) | 0.796 |
| BIND_RX | `fixture.bind_rx.if0` | 20,991 | 0.210 | 20 | 20 | fits | 38,628 | 29 (77) | 0.747 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 10,294 | 0.103 | 20 | 20 | fits | 32,287 | 31 (35) | 0.724 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 5,902 | 0.059 | 20 | 20 | fits | 17,830 | 14 (29) | 0.753 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 72,281 | 0.723 | 20 | 200 | fits | 72,384 | 53 | 0.751 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 72,281 | 0.723 | 20 | 200 | fits | 72,384 | 53 | 0.751 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 72,011 | 0.720 | 20 | 20 | fits | 72,384 | 53 | 0.751 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 72,011 | 0.720 | 20 | 20 | fits | 72,384 | 53 | 0.751 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 72,216 | 0.722 | 20 | 24 | fits | 72,384 | 53 | 0.751 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 72,216 | 0.722 | 20 | 24 | fits | 72,384 | 53 | 0.751 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 72,151 | 0.722 | 20 | 50 | fits | 72,384 | 53 | 0.751 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 72,151 | 0.722 | 20 | 50 | fits | 72,384 | 53 | 0.751 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 72,086 | 0.721 | 18 | 18 | fits | 72,384 | 53 | 0.751 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 72,086 | 0.721 | 18 | 18 | fits | 72,384 | 53 | 0.751 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
