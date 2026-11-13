### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 87 paths and 6 of 945 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.227 (0.412) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.114 (0.240) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.064 (0.232) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.083 (0.371) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.120 (0.263) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.114 (0.240) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.115 (0.243) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.123 (0.261) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.081 (0.264) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.159 (0.475) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.226 (0.516) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.136 (0.444) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.095 (0.413) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.086 (0.455) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.082 (0.390) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.143 (0.338) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.040 (0.121) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.025 (0.125) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.029 (0.249) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.027 (0.238) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.018 (0.027) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.118 (0.360) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.079 (0.206) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.169 (0.426) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.129 (0.374) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.117 (0.249) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.153 (0.405) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.248 (0.524) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.135 (0.381) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.199 (0.451) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.099 (0.230) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.100 (0.232) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.145 (0.395) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.121 (0.252) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.143 (0.394) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.091 (0.222) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.148 (0.399) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.148 (0.399) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.103 (0.237) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.149 (0.401) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.103 (0.236) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.157 (0.408) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.140 (0.281) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.184 (0.446) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.302 (0.604) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.082 (0.214) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.209 (0.497) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.467 (0.716) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.462 (0.703) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.417 (0.654) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.411 (0.646) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_on.if0` (aecp-fanout) | 0.464 (0.701) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.521 (0.762) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.349 (0.444) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.392 (0.618) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.462 (4.809) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.782 (5.382) | fits | 7 adp | 73 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.094 (0.403) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.629 (2.004) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.456 (62.585) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.258 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.301 (0.395) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-starved.held.acmp.if0` (save-starved) | 3.135 | fits | 11 acmp | 2 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-starved.held.adp.if0` (save-starved) | 2.722 | fits | 7 adp | 2 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-starved.held.aecp.if0` (save-starved) | 2.545 | fits | 15 aecp | 2 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-starved.held.maap.if0` (save-starved) | 1.852 | fits | 6 maap | 2 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-starved.held.srp.if0` (save-starved) | 7.494 | fits | 31 srp | 2 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.157 (0.415) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.103 (0.188) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.117 (0.238) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.137 (0.415) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe2.if0` (maap) | 0.137 (0.380) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-starved.mrpdu.periodic.if0` (save-starved) | 0.904 | fits | 0 srp | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 4.011 | fits | 0 acmp | 77 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.acmp.last.if0` (backlog-adp@blank-aged2-7) | 6.326 | fits | 11 acmp | 77 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 4.054 | fits | 0 adp | 77 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 5.369 | fits | 7 adp | 77 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-0.service.aecp.first.if0` (backlog-adp@blank-0) | 2.217 | fits | 0 aecp | 77 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.548 | MISS ceiling | 15 aecp | 77 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 4.037 | fits | 0 maap | 77 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 5.405 | fits | 6 maap | 77 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 6.355 | fits | 0 srp | 77 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-5.service.srp.last.if0` (backlog-adp@program-aged2-5) | 9.043 | fits | 31 srp | 77 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.837 (1.233) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.373 (0.374) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.156 (0.157) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.805 (0.878) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-0 | 0 | 9.307 | 8 | 149,308 (1.493) | yes | - |
| backlog-adp@blank-1 | 0 | 9.700 | 9 | 154,625 (1.546) | yes | - |
| backlog-adp@blank-2 | 0 | 9.427 | 8 | 149,529 (1.495) | yes | - |
| backlog-adp@blank-3 | 0 | 9.401 | 8 | 152,886 (1.529) | yes | - |
| backlog-adp@blank-4 | 0 | 9.355 | 8 | 153,380 (1.534) | yes | - |
| backlog-adp@blank-5 | 0 | 9.396 | 8 | 148,921 (1.489) | yes | - |
| backlog-adp@blank-6 | 0 | 9.381 | 7 | 147,749 (1.477) | yes | - |
| backlog-adp@blank-7 | 0 | 9.420 | 8 | 153,846 (1.538) | yes | - |
| backlog-adp@program-0 | 0 | 8.582 | 8 | 148,523 (1.485) | yes | - |
| backlog-adp@program-1 | 0 | 10.013 | 10 | 149,095 (1.491) | yes | - |
| backlog-adp@program-2 | 0 | 9.486 | 8 | 149,002 (1.490) | yes | - |
| backlog-adp@program-3 | 0 | 9.375 | 8 | 153,376 (1.534) | yes | - |
| backlog-adp@program-4 | 0 | 8.518 | 8 | 152,606 (1.526) | yes | - |
| backlog-adp@program-5 | 0 | 8.640 | 8 | 148,426 (1.484) | yes | - |
| backlog-adp@program-6 | 0 | 8.691 | 8 | 148,934 (1.489) | yes | - |
| backlog-adp@program-7 | 0 | 8.717 | 8 | 148,515 (1.485) | yes | - |
| backlog-adp@verify-0 | 0 | 9.192 | 8 | 149,222 (1.492) | yes | - |
| backlog-adp@verify-1 | 0 | 9.717 | 9 | 149,222 (1.492) | yes | - |
| backlog-adp@verify-2 | 0 | 9.423 | 8 | 148,475 (1.485) | yes | - |
| backlog-adp@verify-3 | 0 | 9.390 | 8 | 152,523 (1.525) | yes | - |
| backlog-adp@verify-4 | 0 | 9.354 | 8 | 152,523 (1.525) | yes | - |
| backlog-adp@verify-5 | 0 | 9.963 | 10 | 149,095 (1.491) | yes | - |
| backlog-adp@verify-6 | 0 | 9.370 | 7 | 148,192 (1.482) | yes | - |
| backlog-adp@verify-7 | 0 | 9.420 | 8 | 153,225 (1.532) | yes | - |
| backlog-adp@blank-aged2-0 | 1 | 10.800 | 10 | 144,721 (1.447) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 9.796 | 11 | 149,188 (1.492) | yes | - |
| backlog-adp@blank-aged2-2 | 0 | 9.582 | 10 | 148,195 (1.482) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 9.389 | 8 | 149,138 (1.491) | yes | - |
| backlog-adp@blank-aged2-4 | 0 | 9.397 | 8 | 149,138 (1.491) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 9.328 | 7 | 149,311 (1.493) | yes | - |
| backlog-adp@blank-aged2-6 | 0 | 9.416 | 8 | 148,142 (1.481) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 9.378 | 8 | 154,545 (1.545) | yes | - |
| backlog-adp@blank-aged1-0 | 0 | 9.297 | 8 | 148,388 (1.484) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.071 | 9 | 148,401 (1.484) | yes | - |
| backlog-adp@blank-aged1-2 | 0 | 10.147 | 9 | 153,358 (1.534) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 10.277 | 11 | 149,091 (1.491) | yes | - |
| backlog-adp@blank-aged1-4 | 0 | 10.083 | 9 | 148,236 (1.482) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 10.056 | 8 | 148,236 (1.482) | yes | - |
| backlog-adp@blank-aged1-6 | 0 | 10.164 | 8 | 154,807 (1.548) | yes | - |
| backlog-adp@blank-aged1-7 | 0 | 10.094 | 9 | 150,056 (1.501) | yes | - |
| backlog-adp@program-aged2-0 | 1 | 9.275 | 7 | 151,282 (1.513) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 9.357 | 8 | 149,290 (1.493) | yes | - |
| backlog-adp@program-aged2-2 | 0 | 9.344 | 8 | 148,370 (1.484) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 9.410 | 8 | 148,370 (1.484) | yes | - |
| backlog-adp@program-aged2-4 | 1 | 9.359 | 7 | 149,003 (1.490) | yes | - |
| backlog-adp@program-aged2-5 | 0 | 9.465 | 8 | 153,381 (1.534) | yes | - |
| backlog-adp@program-aged2-6 | 0 | 9.636 | 10 | 148,250 (1.482) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 9.397 | 8 | 154,399 (1.544) | yes | - |
| backlog-adp@program-aged1-0 | 0 | 9.359 | 8 | 152,523 (1.525) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 9.860 | 11 | 149,329 (1.493) | yes | - |
| backlog-adp@program-aged1-2 | 0 | 9.577 | 10 | 148,463 (1.485) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 9.381 | 7 | 149,290 (1.493) | yes | - |
| backlog-adp@program-aged1-4 | 0 | 9.483 | 8 | 148,370 (1.484) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 9.409 | 8 | 148,580 (1.486) | yes | - |
| backlog-adp@program-aged1-6 | 0 | 9.393 | 8 | 148,209 (1.482) | yes | - |
| backlog-adp@program-aged1-7 | 1 | 9.360 | 7 | 149,267 (1.493) | yes | - |
| backlog-adp@verify-aged2-0 | 0 | 9.268 | 7 | 148,954 (1.490) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 9.397 | 9 | 154,132 (1.541) | yes | - |
| backlog-adp@verify-aged2-2 | 0 | 9.262 | 8 | 154,305 (1.543) | yes | - |
| backlog-adp@verify-aged2-3 | 1 | 9.357 | 7 | 144,794 (1.448) | yes | - |
| backlog-adp@verify-aged2-4 | 0 | 9.984 | 10 | 144,928 (1.449) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 9.750 | 10 | 144,820 (1.448) | yes | - |
| backlog-adp@verify-aged2-6 | 0 | 9.419 | 8 | 149,045 (1.490) | yes | - |
| backlog-adp@verify-aged2-7 | 1 | 9.391 | 7 | 149,045 (1.490) | yes | - |
| backlog-adp@verify-aged1-0 | 0 | 9.280 | 8 | 154,354 (1.544) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 9.445 | 9 | 148,954 (1.490) | yes | - |
| backlog-adp@verify-aged1-2 | 1 | 9.337 | 7 | 148,954 (1.490) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 9.439 | 8 | 154,132 (1.541) | yes | - |
| backlog-adp@verify-aged1-4 | 0 | 9.395 | 8 | 154,342 (1.543) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 9.388 | 8 | 144,944 (1.449) | yes | - |
| backlog-adp@verify-aged1-6 | 1 | 9.694 | 9 | 150,323 (1.503) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 9.444 | 8 | 147,937 (1.479) | yes | - |
| backlog | 0 | 5.631 | 7 | 152,512 (1.525) | yes | - |
| backlog-adp | 0 | 8.592 | 8 | 149,482 (1.495) | yes | - |
| backlog-adp-refill | 0 | 40.638 | 22 | 152,095 (1.521) | yes | - |
| backlog-owed | 0 | 360.309 | 50 | 149,609 (1.496) | yes | - |
| fixture | 0 | 1.179 | 2 | 80,241 (0.802) | yes | - |

Composed maximum over the 4 backlog windows: 152,512 CPU cycles (1.525 ms), backlog.
Over the windows that released their whole load only: 152,512 (1.525 ms), backlog.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3347 | 0 | 64,021 (0.640) | fits |
| save-second | 62367 | 0 | 64,021 (0.640) | fits |
| backlog-adp@blank-0 | 408 | 0 | 149,308 (1.493) | fits |
| backlog-adp@blank-1 | 409 | 0 | 154,625 (1.546) | fits |
| backlog-adp@blank-2 | 408 | 0 | 149,529 (1.495) | fits |
| backlog-adp@blank-3 | 408 | 0 | 152,886 (1.529) | fits |
| backlog-adp@blank-4 | 408 | 0 | 153,380 (1.534) | fits |
| backlog-adp@blank-5 | 408 | 0 | 148,921 (1.489) | fits |
| backlog-adp@blank-6 | 410 | 0 | 147,749 (1.477) | fits |
| backlog-adp@blank-7 | 410 | 0 | 153,846 (1.538) | fits |
| backlog-adp@program-0 | 510 | 0 | 148,523 (1.485) | fits |
| backlog-adp@program-1 | 512 | 0 | 149,095 (1.491) | fits |
| backlog-adp@program-2 | 512 | 0 | 149,002 (1.490) | fits |
| backlog-adp@program-3 | 512 | 0 | 153,376 (1.534) | fits |
| backlog-adp@program-4 | 513 | 0 | 152,606 (1.526) | fits |
| backlog-adp@program-5 | 515 | 0 | 148,426 (1.484) | fits |
| backlog-adp@program-6 | 515 | 0 | 148,934 (1.489) | fits |
| backlog-adp@program-7 | 515 | 0 | 148,515 (1.485) | fits |
| backlog-adp@verify-0 | 605 | 0 | 149,222 (1.492) | fits |
| backlog-adp@verify-1 | 606 | 0 | 149,222 (1.492) | fits |
| backlog-adp@verify-2 | 605 | 0 | 148,475 (1.485) | fits |
| backlog-adp@verify-3 | 605 | 0 | 152,523 (1.525) | fits |
| backlog-adp@verify-4 | 605 | 0 | 152,523 (1.525) | fits |
| backlog-adp@verify-5 | 607 | 0 | 149,095 (1.491) | fits |
| backlog-adp@verify-6 | 607 | 0 | 148,192 (1.482) | fits |
| backlog-adp@verify-7 | 607 | 0 | 153,225 (1.532) | fits |
| backlog-adp@blank-aged2-0 | 808 | 0 | 149,797 (1.498) | fits |
| backlog-adp@blank-aged2-1 | 816 | 0 | 149,188 (1.492) | fits |
| backlog-adp@blank-aged2-2 | 825 | 0 | 148,195 (1.482) | fits |
| backlog-adp@blank-aged2-3 | 833 | 0 | 149,138 (1.491) | fits |
| backlog-adp@blank-aged2-4 | 843 | 0 | 149,138 (1.491) | fits |
| backlog-adp@blank-aged2-5 | 853 | 0 | 149,311 (1.493) | fits |
| backlog-adp@blank-aged2-6 | 864 | 0 | 148,142 (1.481) | fits |
| backlog-adp@blank-aged2-7 | 874 | 0 | 154,545 (1.545) | fits |
| backlog-adp@blank-aged1-0 | 726 | 0 | 148,388 (1.484) | fits |
| backlog-adp@blank-aged1-1 | 738 | 0 | 148,401 (1.484) | fits |
| backlog-adp@blank-aged1-2 | 748 | 0 | 153,358 (1.534) | fits |
| backlog-adp@blank-aged1-3 | 760 | 0 | 149,091 (1.491) | fits |
| backlog-adp@blank-aged1-4 | 768 | 0 | 148,236 (1.482) | fits |
| backlog-adp@blank-aged1-5 | 778 | 0 | 148,236 (1.482) | fits |
| backlog-adp@blank-aged1-6 | 788 | 0 | 154,807 (1.548) | fits |
| backlog-adp@blank-aged1-7 | 799 | 0 | 150,056 (1.501) | fits |
| backlog-adp@program-aged2-0 | 903 | 0 | 151,282 (1.513) | fits |
| backlog-adp@program-aged2-1 | 914 | 0 | 149,290 (1.493) | fits |
| backlog-adp@program-aged2-2 | 924 | 0 | 148,370 (1.484) | fits |
| backlog-adp@program-aged2-3 | 934 | 0 | 148,370 (1.484) | fits |
| backlog-adp@program-aged2-4 | 944 | 0 | 149,003 (1.490) | fits |
| backlog-adp@program-aged2-5 | 955 | 0 | 153,381 (1.534) | fits |
| backlog-adp@program-aged2-6 | 967 | 0 | 148,250 (1.482) | fits |
| backlog-adp@program-aged2-7 | 975 | 0 | 154,399 (1.544) | fits |
| backlog-adp@program-aged1-0 | 822 | 0 | 152,523 (1.525) | fits |
| backlog-adp@program-aged1-1 | 835 | 0 | 149,329 (1.493) | fits |
| backlog-adp@program-aged1-2 | 844 | 0 | 148,463 (1.485) | fits |
| backlog-adp@program-aged1-3 | 852 | 0 | 149,290 (1.493) | fits |
| backlog-adp@program-aged1-4 | 863 | 0 | 148,370 (1.484) | fits |
| backlog-adp@program-aged1-5 | 873 | 0 | 148,580 (1.486) | fits |
| backlog-adp@program-aged1-6 | 883 | 0 | 148,209 (1.482) | fits |
| backlog-adp@program-aged1-7 | 893 | 0 | 149,267 (1.493) | fits |
| backlog-adp@verify-aged2-0 | 998 | 0 | 148,954 (1.490) | fits |
| backlog-adp@verify-aged2-1 | 1010 | 0 | 154,132 (1.541) | fits |
| backlog-adp@verify-aged2-2 | 1019 | 0 | 154,305 (1.543) | fits |
| backlog-adp@verify-aged2-3 | 1029 | 0 | 144,794 (1.448) | fits |
| backlog-adp@verify-aged2-4 | 1042 | 0 | 144,928 (1.449) | fits |
| backlog-adp@verify-aged2-5 | 1052 | 0 | 144,820 (1.448) | fits |
| backlog-adp@verify-aged2-6 | 1060 | 0 | 149,045 (1.490) | fits |
| backlog-adp@verify-aged2-7 | 1070 | 0 | 149,045 (1.490) | fits |
| backlog-adp@verify-aged1-0 | 917 | 0 | 154,354 (1.544) | fits |
| backlog-adp@verify-aged1-1 | 928 | 0 | 148,954 (1.490) | fits |
| backlog-adp@verify-aged1-2 | 937 | 0 | 148,954 (1.490) | fits |
| backlog-adp@verify-aged1-3 | 948 | 0 | 154,132 (1.541) | fits |
| backlog-adp@verify-aged1-4 | 958 | 0 | 154,342 (1.543) | fits |
| backlog-adp@verify-aged1-5 | 968 | 0 | 144,944 (1.449) | fits |
| backlog-adp@verify-aged1-6 | 980 | 0 | 150,323 (1.503) | fits |
| backlog-adp@verify-aged1-7 | 989 | 0 | 147,937 (1.479) | fits |
| adp-advertise | 591 | 0 | 64,021 (0.640) | fits |
| save-held | 1340 | 0 | 150,746 (1.507) | fits |
| save-starved | 33605 | 0 | 152,667 (1.527) | fits |
| acmp-noresp | 1881 | 0 | 64,021 (0.640) | fits |
| save | 602 | 0 | 64,021 (0.640) | fits |
| srp | 284 | 0 | 90,543 (0.905) | fits |
| backlog | 281 | 0 | 152,512 (1.525) | fits |
| backlog-adp | 307 | 0 | 149,482 (1.495) | fits |
| backlog-adp-refill | 321 | 0 | 152,095 (1.521) | fits |
| backlog-owed | 331 | 0 | 150,108 (1.501) | fits |
| acmp-disc | 872 | 0 | 64,021 (0.640) | fits |
| maap | 172 | 0 | 64,021 (0.640) | fits |
| adp-link | 87 | 0 | 64,021 (0.640) | fits |
| adp-gm | 86 | 0 | 64,021 (0.640) | fits |
| adp-discover | 86 | 0 | 64,021 (0.640) | fits |
| control | 86 | 0 | 64,021 (0.640) | fits |
| aecp-fanout | 108 | 0 | 64,021 (0.640) | fits |
| acmp-cmd | 82 | 0 | 64,021 (0.640) | fits |
| aecp | 108 | 0 | 64,021 (0.640) | fits |
| datapath-events | 113 | 0 | 64,021 (0.640) | fits |
| fixture | 160 | 0 | 80,241 (0.802) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-0 | 2 | none | none | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 8.110 (20) | 11.890 |
| backlog-adp@blank-aged2-1 | 2 | none | +8.316 ms, 77,135 (0.771 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 8.120 (20) | 11.880 |
| backlog-adp@blank-aged2-2 | 2 | none | none | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 8.155 (20) | 11.845 |
| backlog-adp@blank-aged2-3 | 2 | none | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 8.967 (20) | 11.033 |
| backlog-adp@blank-aged2-4 | 2 | +5.367 ms, 77,530 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 8.980 (20) | 11.020 |
| backlog-adp@blank-aged2-5 | 2 | +5.461 ms, 77,668 (0.777 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 8.908 (20) | 11.092 |
| backlog-adp@blank-aged2-6 | 2 | +4.543 ms, 77,456 (0.775 ms), read-back | none | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 8.993 (20) | 11.007 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 8.954 (20) | 11.046 |
| backlog-adp@blank-aged1-0 | 1 | none | none | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 8.120 (20) | 11.880 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 8.061 (20) | 11.939 |
| backlog-adp@blank-aged1-2 | 1 | none | none | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 8.283 (20) | 11.717 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 8.852 (20) | 11.148 |
| backlog-adp@blank-aged1-4 | 1 | none | none | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 8.899 (20) | 11.101 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 8.877 (20) | 11.123 |
| backlog-adp@blank-aged1-6 | 1 | none | none | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 8.986 (20) | 11.014 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 8.914 (20) | 11.086 |
| backlog-adp@program-aged2-0 | 2 | none | none | `backlog-adp@program-aged2-0.service.srp.last.if0` | 8.054 (20) | 11.946 |
| backlog-adp@program-aged2-1 | 2 | none | +8.282 ms, 80,490 (0.805 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 8.086 (20) | 11.914 |
| backlog-adp@program-aged2-2 | 2 | none | +8.259 ms, 80,671 (0.807 ms), issue | `backlog-adp@program-aged2-2.service.srp.last.if0` | 8.222 (20) | 11.778 |
| backlog-adp@program-aged2-3 | 2 | +7.401 ms, 80,672 (0.807 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 8.990 (20) | 11.010 |
| backlog-adp@program-aged2-4 | 2 | +5.460 ms, 80,957 (0.810 ms), issue | none | `backlog-adp@program-aged2-4.service.srp.last.if0` | 8.938 (20) | 11.062 |
| backlog-adp@program-aged2-5 | 2 | +5.559 ms, 80,864 (0.809 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.043 (20) | 10.957 |
| backlog-adp@program-aged2-6 | 2 | +4.490 ms, 80,535 (0.805 ms), issue | none | `backlog-adp@program-aged2-6.service.srp.last.if0` | 8.967 (20) | 11.033 |
| backlog-adp@program-aged2-7 | 2 | +3.000 ms, 80,572 (0.806 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 8.972 (20) | 11.028 |
| backlog-adp@program-aged1-0 | 1 | none | none | `backlog-adp@program-aged1-0.service.srp.last.if0` | 8.138 (20) | 11.862 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 8.074 (20) | 11.926 |
| backlog-adp@program-aged1-2 | 1 | none | none | `backlog-adp@program-aged1-2.service.srp.last.if0` | 8.113 (20) | 11.887 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 8.158 (20) | 11.842 |
| backlog-adp@program-aged1-4 | 1 | none | none | `backlog-adp@program-aged1-4.service.srp.last.if0` | 8.265 (20) | 11.735 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 8.187 (20) | 11.813 |
| backlog-adp@program-aged1-6 | 1 | none | none | `backlog-adp@program-aged1-6.service.srp.last.if0` | 8.173 (20) | 11.827 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 8.139 (20) | 11.861 |
| backlog-adp@verify-aged2-0 | 2 | none | none | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 8.080 (20) | 11.920 |
| backlog-adp@verify-aged2-1 | 2 | none | +8.363 ms, 77,749 (0.777 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 8.170 (20) | 11.830 |
| backlog-adp@verify-aged2-2 | 2 | none | +8.213 ms, 77,930 (0.779 ms), read-back | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 8.176 (20) | 11.824 |
| backlog-adp@verify-aged2-3 | 2 | +7.370 ms, 77,931 (0.779 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 8.935 (20) | 11.065 |
| backlog-adp@verify-aged2-4 | 2 | +5.464 ms, 78,079 (0.781 ms), read-back | none | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 8.996 (20) | 11.004 |
| backlog-adp@verify-aged2-5 | 2 | +5.427 ms, 78,079 (0.781 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 8.958 (20) | 11.042 |
| backlog-adp@verify-aged2-6 | 2 | +4.389 ms, 77,822 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 8.999 (20) | 11.001 |
| backlog-adp@verify-aged2-7 | 2 | +4.363 ms, 77,822 (0.778 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 8.971 (20) | 11.029 |
| backlog-adp@verify-aged1-0 | 1 | none | none | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 8.093 (20) | 11.907 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 8.116 (20) | 11.884 |
| backlog-adp@verify-aged1-2 | 1 | none | none | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 8.155 (20) | 11.845 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 8.257 (20) | 11.743 |
| backlog-adp@verify-aged1-4 | 1 | none | none | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 8.208 (20) | 11.792 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 8.201 (20) | 11.799 |
| backlog-adp@verify-aged1-6 | 1 | none | none | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 8.135 (20) | 11.865 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 8.013 (20) | 11.987 |

Least margin over the aged windows: 10.957 ms, `backlog-adp@program-aged2-5.service.srp.last.if0` at 9.043 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6029.855 | 6,070 | 102 | 2 | 30.830 | yes | within |
| save-held | 2018.690 | 4,070 | 102 | - | 13.360 | no | within |
| save-starved | 4048.616 | 4,070 | 102 | - | 31.158 | yes | within |
| save | 2019.061 | 4,070 | 102 | - | 10.852 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 93,822 (0.938) | 79,379 (0.794) |
| save-second | 520 | 80,943 (0.809) | 78,453 (0.785) |
| backlog-adp@blank-0 | 298 | 86,942 (0.869) | 76,924 (0.769) |
| backlog-adp@blank-1 | 299 | 87,432 (0.874) | 77,290 (0.773) |
| backlog-adp@blank-2 | 299 | 89,354 (0.894) | 77,434 (0.774) |
| backlog-adp@blank-3 | 299 | 89,286 (0.893) | 77,368 (0.774) |
| backlog-adp@blank-4 | 299 | 89,286 (0.893) | 77,368 (0.774) |
| backlog-adp@blank-5 | 299 | 89,201 (0.892) | 77,416 (0.774) |
| backlog-adp@blank-6 | 299 | 89,329 (0.893) | 77,451 (0.775) |
| backlog-adp@blank-7 | 299 | 89,000 (0.890) | 77,433 (0.774) |
| backlog-adp@program-0 | 327 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-1 | 328 | 93,426 (0.934) | 79,917 (0.799) |
| backlog-adp@program-2 | 328 | 93,426 (0.934) | 80,096 (0.801) |
| backlog-adp@program-3 | 328 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-4 | 328 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-5 | 329 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-6 | 329 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-7 | 329 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@verify-0 | 354 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-1 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-2 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-3 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-4 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-5 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-6 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-7 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@blank-aged2-0 | 298 | 89,284 (0.893) | 77,499 (0.775) |
| backlog-adp@blank-aged2-1 | 297 | 77,135 (0.771) | 76,477 (0.765) |
| backlog-adp@blank-aged2-2 | 297 | 86,184 (0.862) | 77,007 (0.770) |
| backlog-adp@blank-aged2-3 | 297 | 86,204 (0.862) | 77,007 (0.770) |
| backlog-adp@blank-aged2-4 | 297 | 77,530 (0.775) | 76,734 (0.767) |
| backlog-adp@blank-aged2-5 | 297 | 77,668 (0.777) | 76,799 (0.768) |
| backlog-adp@blank-aged2-6 | 297 | 77,456 (0.775) | 76,621 (0.766) |
| backlog-adp@blank-aged2-7 | 297 | 85,927 (0.859) | 77,032 (0.770) |
| backlog-adp@blank-aged1-0 | 297 | 89,000 (0.890) | 77,434 (0.774) |
| backlog-adp@blank-aged1-1 | 298 | 93,508 (0.935) | 77,434 (0.774) |
| backlog-adp@blank-aged1-2 | 297 | 94,331 (0.943) | 77,508 (0.775) |
| backlog-adp@blank-aged1-3 | 297 | 87,888 (0.879) | 77,565 (0.776) |
| backlog-adp@blank-aged1-4 | 297 | 89,511 (0.895) | 77,565 (0.776) |
| backlog-adp@blank-aged1-5 | 297 | 89,134 (0.891) | 77,499 (0.775) |
| backlog-adp@blank-aged1-6 | 297 | 89,065 (0.891) | 77,499 (0.775) |
| backlog-adp@blank-aged1-7 | 297 | 89,284 (0.893) | 77,499 (0.775) |
| backlog-adp@program-aged2-0 | 326 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-aged2-1 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged2-2 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged2-3 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged2-4 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged2-5 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged2-6 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged2-7 | 326 | 93,426 (0.934) | 79,334 (0.793) |
| backlog-adp@program-aged1-0 | 326 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-aged1-1 | 327 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-aged1-2 | 326 | 93,426 (0.934) | 79,904 (0.799) |
| backlog-adp@program-aged1-3 | 326 | 93,426 (0.934) | 79,983 (0.800) |
| backlog-adp@program-aged1-4 | 326 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-aged1-5 | 326 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-aged1-6 | 326 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@program-aged1-7 | 326 | 93,426 (0.934) | 80,030 (0.800) |
| backlog-adp@verify-aged2-0 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-1 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-2 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-3 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-4 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-5 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-6 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged2-7 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-0 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-1 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-2 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-3 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-4 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-5 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-6 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| backlog-adp@verify-aged1-7 | 355 | 93,426 (0.934) | 79,379 (0.794) |
| adp-advertise | 578 | 19,786 (0.198) | 3,954 (0.040) |
| save-held | 722 | 92,958 (0.930) | 79,610 (0.796) |
| save-starved | 418 | 81,575 (0.816) | 79,186 (0.792) |
| acmp-noresp | 615 | 93,489 (0.935) | 79,379 (0.794) |
| save | 585 | 92,928 (0.929) | 79,302 (0.793) |
| srp | 271 | 19,786 (0.198) | 3,954 (0.040) |
| backlog | 265 | 19,786 (0.198) | 3,954 (0.040) |
| backlog-adp | 271 | 19,786 (0.198) | 3,954 (0.040) |
| backlog-adp-refill | 274 | 19,786 (0.198) | 3,954 (0.040) |
| backlog-owed | 306 | 19,888 (0.199) | 4,005 (0.040) |
| acmp-disc | 305 | 93,642 (0.936) | 79,379 (0.794) |
| maap | 163 | 19,786 (0.198) | 3,954 (0.040) |
| adp-link | 80 | 19,611 (0.196) | 3,954 (0.040) |
| adp-gm | 80 | 19,611 (0.196) | 3,954 (0.040) |
| adp-discover | 80 | 19,611 (0.196) | 3,954 (0.040) |
| control | 80 | 19,611 (0.196) | 3,954 (0.040) |
| aecp-fanout | 79 | 19,611 (0.196) | 3,954 (0.040) |
| acmp-cmd | 65 | 19,611 (0.196) | 3,954 (0.040) |
| aecp | 79 | 19,611 (0.196) | 3,954 (0.040) |
| datapath-events | 69 | 19,611 (0.196) | 3,954 (0.040) |
| fixture | 54 | 14,065 (0.141) | 3,919 (0.039) |

Longest pass that carries a step: 94,331 CPU cycles (0.943 ms), backlog-adp@blank-aged1-2; longest step: 80,096 (0.801 ms), backlog-adp@program-2.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 8,562 | 0.086 | 20 | 20 | fits | 29,662 | 19 (14) | 0.881 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-0.adp_available.if0` | 434,767 | 4.348 | 20 | 20 | fits | 149,308 | 171 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@blank-0.service.adp.first.if0` | 364,686 | 3.647 | 20 | 200 | fits | 147,491 | 195 | 0.361 |
| ADP record released under the composed load, last | `backlog-adp@blank-0.service.adp.last.if0` | 513,385 | 5.134 | 20 | 200 | fits | 149,308 | 171 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@blank-0.service.acmp.first.if0` | 365,598 | 3.656 | 20 | 20 | fits | 147,491 | 195 | 0.361 |
| ACMP record released under the composed load, last | `backlog-adp@blank-0.service.acmp.last.if0` | 609,787 | 6.098 | 20 | 20 | fits | 95,706 | 39 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-0.service.aecp.first.if0` | 221,692 | 2.217 | 20 | 24 | fits | 145,246 | 164 | 0.235 |
| AECP record released under the composed load, last | `backlog-adp@blank-0.service.aecp.last.if0` | 368,208 | 3.682 | 20 | 24 | fits | 147,491 | 195 | 0.361 |
| MAAP record released under the composed load, first | `backlog-adp@blank-0.service.maap.first.if0` | 368,143 | 3.681 | 20 | 50 | fits | 147,491 | 195 | 0.361 |
| MAAP record released under the composed load, last | `backlog-adp@blank-0.service.maap.last.if0` | 517,061 | 5.171 | 20 | 50 | fits | 149,308 | 171 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@blank-0.service.srp.first.if0` | 612,702 | 6.127 | 20 | 20 | fits | 95,706 | 39 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@blank-0.service.srp.last.if0` | 888,765 | 8.888 | 20 | 20 | fits | 74,014 | 36 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 366,269 | 3.663 | 20 | 20 | fits | 141,861 | 152 | 0.345 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 295,997 | 2.960 | 20 | 200 | fits | 154,625 | 217 | 0.350 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 437,249 | 4.372 | 20 | 200 | fits | 141,861 | 152 | 0.345 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 296,909 | 2.969 | 20 | 20 | fits | 154,625 | 217 | 0.350 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 533,651 | 5.337 | 20 | 20 | fits | 95,706 | 39 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 145,869 | 1.459 | 20 | 24 | fits | 145,381 | 164 | 0.235 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 299,519 | 2.995 | 20 | 24 | fits | 154,625 | 217 | 0.350 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 299,454 | 2.995 | 20 | 50 | fits | 154,625 | 217 | 0.350 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 440,925 | 4.409 | 20 | 50 | fits | 141,861 | 152 | 0.345 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 536,566 | 5.366 | 20 | 20 | fits | 95,706 | 39 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 812,817 | 8.128 | 20 | 20 | fits | 74,049 | 36 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-2.adp_available.if0` | 367,196 | 3.672 | 20 | 20 | fits | 149,529 | 172 | 0.350 |
| ADP record released under the composed load, first | `backlog-adp@blank-2.service.adp.first.if0` | 297,067 | 2.971 | 20 | 200 | fits | 147,661 | 195 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-2.service.adp.last.if0` | 445,987 | 4.460 | 20 | 200 | fits | 149,529 | 172 | 0.350 |
| ACMP record released under the composed load, first | `backlog-adp@blank-2.service.acmp.first.if0` | 297,979 | 2.980 | 20 | 20 | fits | 147,661 | 195 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-2.service.acmp.last.if0` | 554,809 | 5.548 | 20 | 20 | fits | 99,154 | 46 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp@blank-2.service.aecp.first.if0` | 153,903 | 1.539 | 20 | 24 | fits | 145,381 | 164 | 0.235 |
| AECP record released under the composed load, last | `backlog-adp@blank-2.service.aecp.last.if0` | 300,589 | 3.006 | 20 | 24 | fits | 147,661 | 195 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-2.service.maap.first.if0` | 300,524 | 3.005 | 20 | 50 | fits | 147,661 | 195 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-2.service.maap.last.if0` | 449,663 | 4.497 | 20 | 50 | fits | 149,529 | 172 | 0.350 |
| SRP record released under the composed load, first | `backlog-adp@blank-2.service.srp.first.if0` | 557,724 | 5.577 | 20 | 20 | fits | 99,154 | 46 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp@blank-2.service.srp.last.if0` | 824,397 | 8.244 | 20 | 20 | fits | 79,682 | 42 | 0.555 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 366,614 | 3.666 | 20 | 20 | fits | 152,886 | 178 | 0.368 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 293,007 | 2.930 | 20 | 200 | fits | 147,661 | 195 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 445,284 | 4.453 | 20 | 200 | fits | 152,886 | 178 | 0.368 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 293,919 | 2.939 | 20 | 20 | fits | 147,661 | 195 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 551,774 | 5.518 | 20 | 20 | fits | 96,684 | 40 | 0.698 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 149,843 | 1.498 | 20 | 24 | fits | 145,381 | 164 | 0.235 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 296,529 | 2.965 | 20 | 24 | fits | 147,661 | 195 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 296,464 | 2.965 | 20 | 50 | fits | 147,661 | 195 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 448,960 | 4.490 | 20 | 50 | fits | 152,886 | 178 | 0.368 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 554,689 | 5.547 | 20 | 20 | fits | 96,684 | 40 | 0.698 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 821,856 | 8.219 | 20 | 20 | fits | 73,710 | 36 | 0.496 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-4.adp_available.if0` | 371,895 | 3.719 | 20 | 20 | fits | 153,380 | 178 | 0.386 |
| ADP record released under the composed load, first | `backlog-adp@blank-4.service.adp.first.if0` | 289,167 | 2.892 | 20 | 200 | fits | 147,881 | 196 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@blank-4.service.adp.last.if0` | 451,088 | 4.511 | 20 | 200 | fits | 153,380 | 178 | 0.386 |
| ACMP record released under the composed load, first | `backlog-adp@blank-4.service.acmp.first.if0` | 290,079 | 2.901 | 20 | 20 | fits | 147,881 | 196 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@blank-4.service.acmp.last.if0` | 547,344 | 5.473 | 20 | 20 | fits | 95,560 | 39 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-4.service.aecp.first.if0` | 145,783 | 1.458 | 20 | 24 | fits | 145,381 | 164 | 0.235 |
| AECP record released under the composed load, last | `backlog-adp@blank-4.service.aecp.last.if0` | 292,689 | 2.927 | 20 | 24 | fits | 147,881 | 196 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@blank-4.service.maap.first.if0` | 292,624 | 2.926 | 20 | 50 | fits | 147,881 | 196 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@blank-4.service.maap.last.if0` | 454,764 | 4.548 | 20 | 50 | fits | 153,380 | 178 | 0.386 |
| SRP record released under the composed load, first | `backlog-adp@blank-4.service.srp.first.if0` | 550,259 | 5.503 | 20 | 20 | fits | 95,560 | 39 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@blank-4.service.srp.last.if0` | 817,379 | 8.174 | 20 | 20 | fits | 73,539 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 396,685 | 3.967 | 20 | 20 | fits | 148,590 | 170 | 0.337 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 306,852 | 3.069 | 20 | 200 | fits | 148,921 | 200 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 454,833 | 4.548 | 20 | 200 | fits | 148,590 | 170 | 0.337 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 307,764 | 3.078 | 20 | 20 | fits | 148,921 | 200 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 550,600 | 5.506 | 20 | 20 | fits | 95,071 | 43 | 0.712 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 153,908 | 1.539 | 20 | 24 | fits | 145,472 | 165 | 0.237 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 310,374 | 3.104 | 20 | 24 | fits | 148,921 | 200 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 310,309 | 3.103 | 20 | 50 | fits | 148,921 | 200 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 458,509 | 4.585 | 20 | 50 | fits | 148,590 | 170 | 0.337 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 553,515 | 5.535 | 20 | 20 | fits | 95,071 | 43 | 0.712 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 821,706 | 8.217 | 20 | 20 | fits | 73,367 | 36 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-6.adp_available.if0` | 365,850 | 3.659 | 20 | 20 | fits | 144,297 | 167 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-6.service.adp.first.if0` | 287,554 | 2.876 | 20 | 200 | fits | 147,749 | 195 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@blank-6.service.adp.last.if0` | 431,242 | 4.312 | 20 | 200 | fits | 144,297 | 167 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-6.service.acmp.first.if0` | 288,466 | 2.885 | 20 | 20 | fits | 147,749 | 195 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@blank-6.service.acmp.last.if0` | 532,957 | 5.330 | 20 | 20 | fits | 101,019 | 45 | 0.659 |
| AECP record released under the composed load, first | `backlog-adp@blank-6.service.aecp.first.if0` | 144,302 | 1.443 | 20 | 24 | fits | 145,276 | 164 | 0.237 |
| AECP record released under the composed load, last | `backlog-adp@blank-6.service.aecp.last.if0` | 291,076 | 2.911 | 20 | 24 | fits | 147,749 | 195 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@blank-6.service.maap.first.if0` | 291,011 | 2.910 | 20 | 50 | fits | 147,749 | 195 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@blank-6.service.maap.last.if0` | 434,918 | 4.349 | 20 | 50 | fits | 144,297 | 167 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-6.service.srp.first.if0` | 535,872 | 5.359 | 20 | 20 | fits | 101,019 | 45 | 0.659 |
| SRP record released under the composed load, last | `backlog-adp@blank-6.service.srp.last.if0` | 819,804 | 8.198 | 20 | 20 | fits | 78,880 | 43 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 391,444 | 3.914 | 20 | 20 | fits | 148,436 | 170 | 0.334 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 301,685 | 3.017 | 20 | 200 | fits | 153,846 | 200 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 449,512 | 4.495 | 20 | 200 | fits | 148,436 | 170 | 0.334 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 302,597 | 3.026 | 20 | 20 | fits | 153,846 | 200 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 545,892 | 5.459 | 20 | 20 | fits | 95,684 | 39 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 152,336 | 1.523 | 20 | 24 | fits | 145,276 | 164 | 0.237 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 305,207 | 3.052 | 20 | 24 | fits | 153,846 | 200 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 305,142 | 3.051 | 20 | 50 | fits | 153,846 | 200 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 453,188 | 4.532 | 20 | 50 | fits | 148,436 | 170 | 0.334 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 548,807 | 5.488 | 20 | 20 | fits | 95,684 | 39 | 0.688 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 824,294 | 8.243 | 20 | 20 | fits | 73,942 | 36 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-0.adp_available.if0` | 385,491 | 3.855 | 20 | 20 | fits | 148,523 | 171 | 0.334 |
| ADP record released under the composed load, first | `backlog-adp@program-0.service.adp.first.if0` | 295,818 | 2.958 | 20 | 200 | fits | 148,371 | 195 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-0.service.adp.last.if0` | 443,732 | 4.437 | 20 | 200 | fits | 148,523 | 171 | 0.334 |
| ACMP record released under the composed load, first | `backlog-adp@program-0.service.acmp.first.if0` | 296,730 | 2.967 | 20 | 20 | fits | 148,371 | 195 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-0.service.acmp.last.if0` | 552,149 | 5.521 | 20 | 20 | fits | 98,633 | 46 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@program-0.service.aecp.first.if0` | 151,944 | 1.519 | 20 | 24 | fits | 145,613 | 164 | 0.242 |
| AECP record released under the composed load, last | `backlog-adp@program-0.service.aecp.last.if0` | 299,340 | 2.993 | 20 | 24 | fits | 148,371 | 195 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-0.service.maap.first.if0` | 299,275 | 2.993 | 20 | 50 | fits | 148,371 | 195 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-0.service.maap.last.if0` | 447,408 | 4.474 | 20 | 50 | fits | 148,523 | 171 | 0.334 |
| SRP record released under the composed load, first | `backlog-adp@program-0.service.srp.first.if0` | 555,064 | 5.551 | 20 | 20 | fits | 98,633 | 46 | 0.697 |
| SRP record released under the composed load, last | `backlog-adp@program-0.service.srp.last.if0` | 815,818 | 8.158 | 20 | 20 | fits | 73,539 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 400,763 | 4.008 | 20 | 20 | fits | 149,095 | 175 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 308,694 | 3.087 | 20 | 200 | fits | 148,511 | 196 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 457,180 | 4.572 | 20 | 200 | fits | 149,095 | 175 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 309,606 | 3.096 | 20 | 20 | fits | 148,511 | 196 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 552,670 | 5.527 | 20 | 20 | fits | 94,794 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 156,051 | 1.561 | 20 | 24 | fits | 145,746 | 165 | 0.243 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 312,216 | 3.122 | 20 | 24 | fits | 148,511 | 196 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 312,151 | 3.122 | 20 | 50 | fits | 148,511 | 196 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 460,856 | 4.609 | 20 | 50 | fits | 149,095 | 175 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 555,585 | 5.556 | 20 | 20 | fits | 94,794 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 822,530 | 8.225 | 20 | 20 | fits | 73,710 | 36 | 0.496 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-2.adp_available.if0` | 388,877 | 3.889 | 20 | 20 | fits | 149,002 | 175 | 0.318 |
| ADP record released under the composed load, first | `backlog-adp@program-2.service.adp.first.if0` | 296,821 | 2.968 | 20 | 200 | fits | 147,264 | 191 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-2.service.adp.last.if0` | 445,214 | 4.452 | 20 | 200 | fits | 149,002 | 175 | 0.318 |
| ACMP record released under the composed load, first | `backlog-adp@program-2.service.acmp.first.if0` | 297,733 | 2.977 | 20 | 20 | fits | 147,264 | 191 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-2.service.acmp.last.if0` | 539,853 | 5.399 | 20 | 20 | fits | 93,943 | 43 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-2.service.aecp.first.if0` | 154,054 | 1.541 | 20 | 24 | fits | 145,282 | 164 | 0.238 |
| AECP record released under the composed load, last | `backlog-adp@program-2.service.aecp.last.if0` | 300,343 | 3.003 | 20 | 24 | fits | 147,264 | 191 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-2.service.maap.first.if0` | 300,278 | 3.003 | 20 | 50 | fits | 147,264 | 191 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-2.service.maap.last.if0` | 448,890 | 4.489 | 20 | 50 | fits | 149,002 | 175 | 0.318 |
| SRP record released under the composed load, first | `backlog-adp@program-2.service.srp.first.if0` | 542,768 | 5.428 | 20 | 20 | fits | 93,943 | 43 | 0.703 |
| SRP record released under the composed load, last | `backlog-adp@program-2.service.srp.last.if0` | 825,962 | 8.260 | 20 | 20 | fits | 78,356 | 43 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 386,869 | 3.869 | 20 | 20 | fits | 149,175 | 176 | 0.319 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 294,813 | 2.948 | 20 | 200 | fits | 153,376 | 196 | 0.382 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 443,379 | 4.434 | 20 | 200 | fits | 149,175 | 176 | 0.319 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 295,725 | 2.957 | 20 | 20 | fits | 153,376 | 196 | 0.382 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 551,987 | 5.520 | 20 | 20 | fits | 98,664 | 46 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 145,934 | 1.459 | 20 | 24 | fits | 145,282 | 164 | 0.238 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 298,335 | 2.983 | 20 | 24 | fits | 153,376 | 196 | 0.382 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 298,270 | 2.983 | 20 | 50 | fits | 153,376 | 196 | 0.382 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 447,055 | 4.471 | 20 | 50 | fits | 149,175 | 176 | 0.319 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 554,902 | 5.549 | 20 | 20 | fits | 98,664 | 46 | 0.696 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 815,158 | 8.152 | 20 | 20 | fits | 65,131 | 32 | 0.511 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-4.adp_available.if0` | 391,957 | 3.920 | 20 | 20 | fits | 152,606 | 177 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@program-4.service.adp.first.if0` | 289,263 | 2.893 | 20 | 200 | fits | 148,588 | 196 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-4.service.adp.last.if0` | 450,600 | 4.506 | 20 | 200 | fits | 152,606 | 177 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@program-4.service.acmp.first.if0` | 290,175 | 2.902 | 20 | 20 | fits | 148,588 | 196 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-4.service.acmp.last.if0` | 546,261 | 5.463 | 20 | 20 | fits | 94,965 | 39 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-4.service.aecp.first.if0` | 145,172 | 1.452 | 20 | 24 | fits | 144,904 | 164 | 0.232 |
| AECP record released under the composed load, last | `backlog-adp@program-4.service.aecp.last.if0` | 292,785 | 2.928 | 20 | 24 | fits | 148,588 | 196 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-4.service.maap.first.if0` | 292,720 | 2.927 | 20 | 50 | fits | 148,588 | 196 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-4.service.maap.last.if0` | 454,276 | 4.543 | 20 | 50 | fits | 152,606 | 177 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@program-4.service.srp.first.if0` | 549,176 | 5.492 | 20 | 20 | fits | 94,965 | 39 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@program-4.service.srp.last.if0` | 809,377 | 8.094 | 20 | 20 | fits | 65,303 | 32 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 379,066 | 3.791 | 20 | 20 | fits | 148,350 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 289,393 | 2.894 | 20 | 200 | fits | 148,426 | 195 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 437,134 | 4.371 | 20 | 200 | fits | 148,350 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 290,305 | 2.903 | 20 | 20 | fits | 148,426 | 195 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 532,769 | 5.328 | 20 | 20 | fits | 94,939 | 39 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 145,464 | 1.455 | 20 | 24 | fits | 145,313 | 164 | 0.240 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 292,915 | 2.929 | 20 | 24 | fits | 148,426 | 195 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 292,850 | 2.929 | 20 | 50 | fits | 148,426 | 195 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 440,810 | 4.408 | 20 | 50 | fits | 148,350 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 535,684 | 5.357 | 20 | 20 | fits | 94,939 | 39 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 804,887 | 8.049 | 20 | 20 | fits | 74,305 | 45 | 0.582 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-6.adp_available.if0` | 384,276 | 3.843 | 20 | 20 | fits | 148,934 | 175 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@program-6.service.adp.first.if0` | 292,288 | 2.923 | 20 | 200 | fits | 147,347 | 191 | 0.380 |
| ADP record released under the composed load, last | `backlog-adp@program-6.service.adp.last.if0` | 440,613 | 4.406 | 20 | 200 | fits | 148,934 | 175 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@program-6.service.acmp.first.if0` | 293,200 | 2.932 | 20 | 20 | fits | 147,347 | 191 | 0.380 |
| ACMP record released under the composed load, last | `backlog-adp@program-6.service.acmp.last.if0` | 535,425 | 5.354 | 20 | 20 | fits | 94,116 | 44 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@program-6.service.aecp.first.if0` | 149,438 | 1.494 | 20 | 24 | fits | 145,313 | 164 | 0.240 |
| AECP record released under the composed load, last | `backlog-adp@program-6.service.aecp.last.if0` | 295,810 | 2.958 | 20 | 24 | fits | 147,347 | 191 | 0.380 |
| MAAP record released under the composed load, first | `backlog-adp@program-6.service.maap.first.if0` | 295,745 | 2.957 | 20 | 50 | fits | 147,347 | 191 | 0.380 |
| MAAP record released under the composed load, last | `backlog-adp@program-6.service.maap.last.if0` | 444,289 | 4.443 | 20 | 50 | fits | 148,934 | 175 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@program-6.service.srp.first.if0` | 538,340 | 5.383 | 20 | 20 | fits | 94,116 | 44 | 0.703 |
| SRP record released under the composed load, last | `backlog-adp@program-6.service.srp.last.if0` | 821,963 | 8.220 | 20 | 20 | fits | 81,776 | 40 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 395,568 | 3.956 | 20 | 20 | fits | 146,121 | 159 | 0.370 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 297,430 | 2.974 | 20 | 200 | fits | 148,515 | 212 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 452,303 | 4.523 | 20 | 200 | fits | 146,121 | 159 | 0.370 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 298,342 | 2.983 | 20 | 20 | fits | 148,515 | 212 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 553,159 | 5.532 | 20 | 20 | fits | 100,160 | 45 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 153,412 | 1.534 | 20 | 24 | fits | 145,313 | 164 | 0.240 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 300,952 | 3.010 | 20 | 24 | fits | 148,515 | 212 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 300,887 | 3.009 | 20 | 50 | fits | 148,515 | 212 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 455,979 | 4.560 | 20 | 50 | fits | 146,121 | 159 | 0.370 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 556,074 | 5.561 | 20 | 20 | fits | 100,160 | 45 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 824,322 | 8.243 | 20 | 20 | fits | 73,367 | 36 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-0.adp_available.if0` | 423,837 | 4.238 | 20 | 20 | fits | 149,222 | 171 | 0.346 |
| ADP record released under the composed load, first | `backlog-adp@verify-0.service.adp.first.if0` | 353,842 | 3.538 | 20 | 200 | fits | 148,236 | 195 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-0.service.adp.last.if0` | 502,455 | 5.025 | 20 | 200 | fits | 149,222 | 171 | 0.346 |
| ACMP record released under the composed load, first | `backlog-adp@verify-0.service.acmp.first.if0` | 354,754 | 3.548 | 20 | 20 | fits | 148,236 | 195 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-0.service.acmp.last.if0` | 598,243 | 5.982 | 20 | 20 | fits | 95,092 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-0.service.aecp.first.if0` | 210,103 | 2.101 | 20 | 24 | fits | 145,629 | 164 | 0.240 |
| AECP record released under the composed load, last | `backlog-adp@verify-0.service.aecp.last.if0` | 357,364 | 3.574 | 20 | 24 | fits | 148,236 | 195 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-0.service.maap.first.if0` | 357,299 | 3.573 | 20 | 50 | fits | 148,236 | 195 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-0.service.maap.last.if0` | 506,131 | 5.061 | 20 | 50 | fits | 149,222 | 171 | 0.346 |
| SRP record released under the composed load, first | `backlog-adp@verify-0.service.srp.first.if0` | 601,158 | 6.012 | 20 | 20 | fits | 95,092 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@verify-0.service.srp.last.if0` | 877,283 | 8.773 | 20 | 20 | fits | 74,014 | 36 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 359,919 | 3.599 | 20 | 20 | fits | 149,222 | 171 | 0.346 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 289,924 | 2.899 | 20 | 200 | fits | 148,181 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 438,537 | 4.385 | 20 | 200 | fits | 149,222 | 171 | 0.346 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 290,836 | 2.908 | 20 | 20 | fits | 148,181 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 534,325 | 5.343 | 20 | 20 | fits | 95,092 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 146,240 | 1.462 | 20 | 24 | fits | 145,799 | 164 | 0.241 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 293,446 | 2.934 | 20 | 24 | fits | 148,181 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 293,381 | 2.934 | 20 | 50 | fits | 148,181 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 442,213 | 4.422 | 20 | 50 | fits | 149,222 | 171 | 0.346 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 537,240 | 5.372 | 20 | 20 | fits | 95,092 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 814,268 | 8.143 | 20 | 20 | fits | 81,860 | 40 | 0.475 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-2.adp_available.if0` | 387,622 | 3.876 | 20 | 20 | fits | 148,475 | 171 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@verify-2.service.adp.first.if0` | 297,997 | 2.980 | 20 | 200 | fits | 148,220 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-2.service.adp.last.if0` | 445,863 | 4.459 | 20 | 200 | fits | 148,475 | 171 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@verify-2.service.acmp.first.if0` | 298,909 | 2.989 | 20 | 20 | fits | 148,220 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-2.service.acmp.last.if0` | 554,300 | 5.543 | 20 | 20 | fits | 98,653 | 46 | 0.696 |
| AECP record released under the composed load, first | `backlog-adp@verify-2.service.aecp.first.if0` | 154,274 | 1.543 | 20 | 24 | fits | 145,799 | 164 | 0.241 |
| AECP record released under the composed load, last | `backlog-adp@verify-2.service.aecp.last.if0` | 301,519 | 3.015 | 20 | 24 | fits | 148,220 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-2.service.maap.first.if0` | 301,454 | 3.015 | 20 | 50 | fits | 148,220 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-2.service.maap.last.if0` | 449,539 | 4.495 | 20 | 50 | fits | 148,475 | 171 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@verify-2.service.srp.first.if0` | 557,215 | 5.572 | 20 | 20 | fits | 98,653 | 46 | 0.696 |
| SRP record released under the composed load, last | `backlog-adp@verify-2.service.srp.last.if0` | 823,743 | 8.237 | 20 | 20 | fits | 79,567 | 42 | 0.552 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 396,614 | 3.966 | 20 | 20 | fits | 152,523 | 177 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 294,116 | 2.941 | 20 | 200 | fits | 148,399 | 196 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 455,222 | 4.552 | 20 | 200 | fits | 152,523 | 177 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 295,028 | 2.950 | 20 | 20 | fits | 148,399 | 196 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 550,962 | 5.510 | 20 | 20 | fits | 95,044 | 39 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 150,214 | 1.502 | 20 | 24 | fits | 145,799 | 164 | 0.241 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 297,638 | 2.976 | 20 | 24 | fits | 148,399 | 196 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 297,573 | 2.976 | 20 | 50 | fits | 148,399 | 196 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 458,898 | 4.589 | 20 | 50 | fits | 152,523 | 177 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 553,877 | 5.539 | 20 | 20 | fits | 95,044 | 39 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 820,534 | 8.205 | 20 | 20 | fits | 73,710 | 36 | 0.496 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-4.adp_available.if0` | 392,547 | 3.925 | 20 | 20 | fits | 152,523 | 177 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@verify-4.service.adp.first.if0` | 290,049 | 2.900 | 20 | 200 | fits | 148,392 | 196 | 0.372 |
| ADP record released under the composed load, last | `backlog-adp@verify-4.service.adp.last.if0` | 451,155 | 4.512 | 20 | 200 | fits | 152,523 | 177 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@verify-4.service.acmp.first.if0` | 290,961 | 2.910 | 20 | 20 | fits | 148,392 | 196 | 0.372 |
| ACMP record released under the composed load, last | `backlog-adp@verify-4.service.acmp.last.if0` | 546,895 | 5.469 | 20 | 20 | fits | 95,044 | 39 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@verify-4.service.aecp.first.if0` | 146,154 | 1.462 | 20 | 24 | fits | 145,799 | 164 | 0.241 |
| AECP record released under the composed load, last | `backlog-adp@verify-4.service.aecp.last.if0` | 293,571 | 2.936 | 20 | 24 | fits | 148,392 | 196 | 0.372 |
| MAAP record released under the composed load, first | `backlog-adp@verify-4.service.maap.first.if0` | 293,506 | 2.935 | 20 | 50 | fits | 148,392 | 196 | 0.372 |
| MAAP record released under the composed load, last | `backlog-adp@verify-4.service.maap.last.if0` | 454,831 | 4.548 | 20 | 50 | fits | 152,523 | 177 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@verify-4.service.srp.first.if0` | 549,810 | 5.498 | 20 | 20 | fits | 95,044 | 39 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@verify-4.service.srp.last.if0` | 816,890 | 8.169 | 20 | 20 | fits | 73,539 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 398,966 | 3.990 | 20 | 20 | fits | 149,095 | 175 | 0.320 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 306,897 | 3.069 | 20 | 200 | fits | 148,511 | 196 | 0.384 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 455,383 | 4.554 | 20 | 200 | fits | 149,095 | 175 | 0.320 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 307,809 | 3.078 | 20 | 20 | fits | 148,511 | 196 | 0.384 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 550,101 | 5.501 | 20 | 20 | fits | 94,022 | 43 | 0.703 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 154,231 | 1.542 | 20 | 24 | fits | 145,842 | 165 | 0.242 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 310,419 | 3.104 | 20 | 24 | fits | 148,511 | 196 | 0.384 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 310,354 | 3.104 | 20 | 50 | fits | 148,511 | 196 | 0.384 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 459,059 | 4.591 | 20 | 50 | fits | 149,095 | 175 | 0.320 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 553,016 | 5.530 | 20 | 20 | fits | 94,022 | 43 | 0.703 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 821,372 | 8.214 | 20 | 20 | fits | 73,367 | 36 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-6.adp_available.if0` | 385,474 | 3.855 | 20 | 20 | fits | 143,266 | 167 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@verify-6.service.adp.first.if0` | 287,782 | 2.878 | 20 | 200 | fits | 148,192 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@verify-6.service.adp.last.if0` | 430,439 | 4.304 | 20 | 200 | fits | 143,266 | 167 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@verify-6.service.acmp.first.if0` | 288,694 | 2.887 | 20 | 20 | fits | 148,192 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@verify-6.service.acmp.last.if0` | 531,432 | 5.314 | 20 | 20 | fits | 100,297 | 45 | 0.650 |
| AECP record released under the composed load, first | `backlog-adp@verify-6.service.aecp.first.if0` | 144,087 | 1.441 | 20 | 24 | fits | 145,177 | 164 | 0.236 |
| AECP record released under the composed load, last | `backlog-adp@verify-6.service.aecp.last.if0` | 291,304 | 2.913 | 20 | 24 | fits | 148,192 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@verify-6.service.maap.first.if0` | 291,239 | 2.912 | 20 | 50 | fits | 148,192 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@verify-6.service.maap.last.if0` | 434,115 | 4.341 | 20 | 50 | fits | 143,266 | 167 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@verify-6.service.srp.first.if0` | 534,347 | 5.343 | 20 | 20 | fits | 100,297 | 45 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@verify-6.service.srp.last.if0` | 818,215 | 8.182 | 20 | 20 | fits | 78,816 | 43 | 0.579 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 392,857 | 3.929 | 20 | 20 | fits | 148,954 | 175 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 300,849 | 3.008 | 20 | 200 | fits | 153,225 | 196 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 449,194 | 4.492 | 20 | 200 | fits | 148,954 | 175 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 301,761 | 3.018 | 20 | 20 | fits | 153,225 | 196 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 544,901 | 5.449 | 20 | 20 | fits | 95,011 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 152,121 | 1.521 | 20 | 24 | fits | 145,177 | 164 | 0.236 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 304,371 | 3.044 | 20 | 24 | fits | 153,225 | 196 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 304,306 | 3.043 | 20 | 50 | fits | 153,225 | 196 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 452,870 | 4.529 | 20 | 50 | fits | 148,954 | 175 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 547,816 | 5.478 | 20 | 20 | fits | 95,011 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 823,720 | 8.237 | 20 | 20 | fits | 74,049 | 36 | 0.507 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-0.adp_available.if0` | 369,785 | 3.698 | 20 | 20 | fits | 144,721 | 156 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.adp.first.if0` | 286,137 | 2.861 | 20 | 200 | fits | 144,458 | 216 | 0.363 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.adp.last.if0` | 439,878 | 4.399 | 20 | 200 | fits | 144,721 | 156 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.acmp.first.if0` | 287,049 | 2.870 | 20 | 20 | fits | 144,458 | 216 | 0.363 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.acmp.last.if0` | 540,340 | 5.403 | 20 | 20 | fits | 99,766 | 45 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.aecp.first.if0` | 146,176 | 1.462 | 20 | 24 | fits | 149,797 | 166 | 0.270 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.aecp.last.if0` | 289,659 | 2.897 | 20 | 24 | fits | 144,458 | 216 | 0.363 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.maap.first.if0` | 289,594 | 2.896 | 20 | 50 | fits | 144,458 | 216 | 0.363 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.maap.last.if0` | 443,554 | 4.436 | 20 | 50 | fits | 144,721 | 156 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-0.service.srp.first.if0` | 543,255 | 5.433 | 20 | 20 | fits | 99,766 | 45 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-0.service.srp.last.if0` | 810,976 | 8.110 | 20 | 20 | fits | 73,295 | 36 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 395,958 | 3.960 | 20 | 20 | fits | 148,242 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 306,377 | 3.064 | 20 | 200 | fits | 149,188 | 200 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 454,010 | 4.540 | 20 | 200 | fits | 148,242 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 307,289 | 3.073 | 20 | 20 | fits | 149,188 | 200 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 549,183 | 5.492 | 20 | 20 | fits | 94,477 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 152,182 | 1.522 | 20 | 24 | fits | 144,993 | 162 | 0.230 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 309,899 | 3.099 | 20 | 24 | fits | 149,188 | 200 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 309,834 | 3.098 | 20 | 50 | fits | 149,188 | 200 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 457,686 | 4.577 | 20 | 50 | fits | 148,242 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 552,098 | 5.521 | 20 | 20 | fits | 94,477 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 812,043 | 8.120 | 20 | 20 | fits | 65,239 | 32 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-2.adp_available.if0` | 393,184 | 3.932 | 20 | 20 | fits | 148,195 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.adp.first.if0` | 303,570 | 3.036 | 20 | 200 | fits | 148,027 | 195 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.adp.last.if0` | 451,156 | 4.512 | 20 | 200 | fits | 148,195 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.acmp.first.if0` | 304,482 | 3.045 | 20 | 20 | fits | 148,027 | 195 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.acmp.last.if0` | 546,364 | 5.464 | 20 | 20 | fits | 94,512 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.aecp.first.if0` | 160,040 | 1.600 | 20 | 24 | fits | 144,796 | 162 | 0.239 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.aecp.last.if0` | 307,092 | 3.071 | 20 | 24 | fits | 148,027 | 195 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.maap.first.if0` | 307,027 | 3.070 | 20 | 50 | fits | 148,027 | 195 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.maap.last.if0` | 454,832 | 4.548 | 20 | 50 | fits | 148,195 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-2.service.srp.first.if0` | 549,279 | 5.493 | 20 | 20 | fits | 94,512 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-2.service.srp.last.if0` | 815,527 | 8.155 | 20 | 20 | fits | 71,796 | 39 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 362,108 | 3.621 | 20 | 20 | fits | 149,138 | 171 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 292,085 | 2.921 | 20 | 200 | fits | 147,924 | 195 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 440,614 | 4.406 | 20 | 200 | fits | 149,138 | 171 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 292,997 | 2.930 | 20 | 20 | fits | 147,924 | 195 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 535,724 | 5.357 | 20 | 20 | fits | 94,414 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 148,658 | 1.487 | 20 | 24 | fits | 144,631 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 295,607 | 2.956 | 20 | 24 | fits | 147,924 | 195 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 295,542 | 2.955 | 20 | 50 | fits | 147,924 | 195 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 444,290 | 4.443 | 20 | 50 | fits | 149,138 | 171 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 538,639 | 5.386 | 20 | 20 | fits | 94,414 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 896,691 | 8.967 | 20 | 20 | fits | 78,890 | 43 | 0.574 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-4.adp_available.if0` | 358,988 | 3.590 | 20 | 20 | fits | 149,138 | 171 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.adp.first.if0` | 288,965 | 2.890 | 20 | 200 | fits | 147,924 | 195 | 0.367 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.adp.last.if0` | 437,494 | 4.375 | 20 | 200 | fits | 149,138 | 171 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.acmp.first.if0` | 289,877 | 2.899 | 20 | 20 | fits | 147,924 | 195 | 0.367 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.acmp.last.if0` | 532,066 | 5.321 | 20 | 20 | fits | 93,876 | 43 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.aecp.first.if0` | 145,538 | 1.455 | 20 | 24 | fits | 144,631 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.aecp.last.if0` | 292,487 | 2.925 | 20 | 24 | fits | 147,924 | 195 | 0.367 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.maap.first.if0` | 292,422 | 2.924 | 20 | 50 | fits | 147,924 | 195 | 0.367 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.maap.last.if0` | 441,170 | 4.412 | 20 | 50 | fits | 149,138 | 171 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-4.service.srp.first.if0` | 534,981 | 5.350 | 20 | 20 | fits | 93,876 | 43 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-4.service.srp.last.if0` | 898,047 | 8.980 | 20 | 20 | fits | 90,113 | 44 | 0.461 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 356,706 | 3.567 | 20 | 20 | fits | 149,311 | 172 | 0.349 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 286,683 | 2.867 | 20 | 200 | fits | 148,762 | 200 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 435,385 | 4.354 | 20 | 200 | fits | 149,311 | 172 | 0.349 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 287,595 | 2.876 | 20 | 20 | fits | 148,762 | 200 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 541,463 | 5.415 | 20 | 20 | fits | 96,458 | 50 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 142,418 | 1.424 | 20 | 24 | fits | 144,631 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 290,205 | 2.902 | 20 | 24 | fits | 148,762 | 200 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 290,140 | 2.901 | 20 | 50 | fits | 148,762 | 200 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 439,061 | 4.391 | 20 | 50 | fits | 149,311 | 172 | 0.349 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 544,378 | 5.444 | 20 | 20 | fits | 96,458 | 50 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 890,829 | 8.908 | 20 | 20 | fits | 81,628 | 40 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-6.adp_available.if0` | 404,198 | 4.042 | 20 | 20 | fits | 145,410 | 173 | 0.407 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.adp.first.if0` | 295,187 | 2.952 | 20 | 200 | fits | 148,142 | 196 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.adp.last.if0` | 449,055 | 4.491 | 20 | 200 | fits | 145,410 | 173 | 0.407 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.acmp.first.if0` | 296,099 | 2.961 | 20 | 20 | fits | 148,142 | 196 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.acmp.last.if0` | 628,119 | 6.281 | 20 | 20 | fits | 100,912 | 46 | 0.657 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.aecp.first.if0` | 151,542 | 1.515 | 20 | 24 | fits | 144,687 | 161 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.aecp.last.if0` | 298,709 | 2.987 | 20 | 24 | fits | 148,142 | 196 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.maap.first.if0` | 298,644 | 2.986 | 20 | 50 | fits | 148,142 | 196 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.maap.last.if0` | 452,731 | 4.527 | 20 | 50 | fits | 145,410 | 173 | 0.407 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-6.service.srp.first.if0` | 631,034 | 6.310 | 20 | 20 | fits | 100,912 | 46 | 0.657 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-6.service.srp.last.if0` | 899,280 | 8.993 | 20 | 20 | fits | 73,467 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 478,184 | 4.782 | 20 | 20 | fits | 153,080 | 176 | 0.383 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 298,470 | 2.985 | 20 | 200 | fits | 154,545 | 201 | 0.377 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 536,868 | 5.369 | 20 | 200 | fits | 153,080 | 176 | 0.383 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 299,382 | 2.994 | 20 | 20 | fits | 154,545 | 201 | 0.377 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 632,589 | 6.326 | 20 | 20 | fits | 95,025 | 39 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 148,422 | 1.484 | 20 | 24 | fits | 144,687 | 161 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 301,992 | 3.020 | 20 | 24 | fits | 154,545 | 201 | 0.377 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 301,927 | 3.019 | 20 | 50 | fits | 154,545 | 201 | 0.377 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 540,544 | 5.405 | 20 | 50 | fits | 153,080 | 176 | 0.383 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 635,504 | 6.355 | 20 | 20 | fits | 95,025 | 39 | 0.682 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 895,449 | 8.954 | 20 | 20 | fits | 65,239 | 32 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-0.adp_available.if0` | 378,836 | 3.788 | 20 | 20 | fits | 148,388 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.adp.first.if0` | 289,125 | 2.891 | 20 | 200 | fits | 147,489 | 195 | 0.361 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.adp.last.if0` | 436,904 | 4.369 | 20 | 200 | fits | 148,388 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.acmp.first.if0` | 290,037 | 2.900 | 20 | 20 | fits | 147,489 | 195 | 0.361 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.acmp.last.if0` | 537,210 | 5.372 | 20 | 20 | fits | 99,610 | 46 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.aecp.first.if0` | 146,133 | 1.461 | 20 | 24 | fits | 144,482 | 161 | 0.222 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.aecp.last.if0` | 292,647 | 2.926 | 20 | 24 | fits | 147,489 | 195 | 0.361 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.maap.first.if0` | 292,582 | 2.926 | 20 | 50 | fits | 147,489 | 195 | 0.361 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.maap.last.if0` | 440,580 | 4.406 | 20 | 50 | fits | 148,388 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-0.service.srp.first.if0` | 540,125 | 5.401 | 20 | 20 | fits | 99,610 | 46 | 0.697 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-0.service.srp.last.if0` | 811,976 | 8.120 | 20 | 20 | fits | 73,468 | 36 | 0.492 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 376,009 | 3.760 | 20 | 20 | fits | 148,401 | 171 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 286,303 | 2.863 | 20 | 200 | fits | 148,327 | 200 | 0.359 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 434,095 | 4.341 | 20 | 200 | fits | 148,401 | 171 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 287,215 | 2.872 | 20 | 20 | fits | 148,327 | 200 | 0.359 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 543,171 | 5.432 | 20 | 20 | fits | 99,195 | 46 | 0.702 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 142,473 | 1.425 | 20 | 24 | fits | 144,482 | 161 | 0.222 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 289,825 | 2.898 | 20 | 24 | fits | 148,327 | 200 | 0.359 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 289,760 | 2.898 | 20 | 50 | fits | 148,327 | 200 | 0.359 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 437,771 | 4.378 | 20 | 50 | fits | 148,401 | 171 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 546,086 | 5.461 | 20 | 20 | fits | 99,195 | 46 | 0.702 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 806,116 | 8.061 | 20 | 20 | fits | 65,067 | 32 | 0.511 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-2.adp_available.if0` | 398,283 | 3.983 | 20 | 20 | fits | 153,358 | 182 | 0.362 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.adp.first.if0` | 293,037 | 2.930 | 20 | 200 | fits | 146,531 | 192 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.adp.last.if0` | 455,115 | 4.551 | 20 | 200 | fits | 153,358 | 182 | 0.362 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.acmp.first.if0` | 293,949 | 2.939 | 20 | 20 | fits | 146,531 | 192 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.acmp.last.if0` | 551,443 | 5.514 | 20 | 20 | fits | 95,632 | 39 | 0.690 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.aecp.first.if0` | 151,003 | 1.510 | 20 | 24 | fits | 144,538 | 161 | 0.223 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.aecp.last.if0` | 296,559 | 2.966 | 20 | 24 | fits | 146,531 | 192 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.maap.first.if0` | 296,494 | 2.965 | 20 | 50 | fits | 146,531 | 192 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.maap.last.if0` | 458,791 | 4.588 | 20 | 50 | fits | 153,358 | 182 | 0.362 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-2.service.srp.first.if0` | 554,358 | 5.544 | 20 | 20 | fits | 95,632 | 39 | 0.690 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-2.service.srp.last.if0` | 828,263 | 8.283 | 20 | 20 | fits | 79,034 | 38 | 0.608 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 391,234 | 3.912 | 20 | 20 | fits | 149,091 | 175 | 0.322 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 299,089 | 2.991 | 20 | 200 | fits | 147,537 | 196 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 447,571 | 4.476 | 20 | 200 | fits | 149,091 | 175 | 0.322 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 300,001 | 3.000 | 20 | 20 | fits | 147,537 | 196 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 543,694 | 5.437 | 20 | 20 | fits | 95,427 | 39 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 147,533 | 1.475 | 20 | 24 | fits | 144,728 | 162 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 302,611 | 3.026 | 20 | 24 | fits | 147,537 | 196 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 302,546 | 3.025 | 20 | 50 | fits | 147,537 | 196 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 451,247 | 4.512 | 20 | 50 | fits | 149,091 | 175 | 0.322 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 546,609 | 5.466 | 20 | 20 | fits | 95,427 | 39 | 0.687 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 885,188 | 8.852 | 20 | 20 | fits | 84,078 | 42 | 0.543 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-4.adp_available.if0` | 377,736 | 3.777 | 20 | 20 | fits | 148,236 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.adp.first.if0` | 288,081 | 2.881 | 20 | 200 | fits | 147,361 | 195 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.adp.last.if0` | 435,708 | 4.357 | 20 | 200 | fits | 148,236 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.acmp.first.if0` | 288,993 | 2.890 | 20 | 20 | fits | 147,361 | 195 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.acmp.last.if0` | 530,839 | 5.308 | 20 | 20 | fits | 94,435 | 39 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.aecp.first.if0` | 145,217 | 1.452 | 20 | 24 | fits | 144,531 | 161 | 0.224 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.aecp.last.if0` | 291,603 | 2.916 | 20 | 24 | fits | 147,361 | 195 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.maap.first.if0` | 291,538 | 2.915 | 20 | 50 | fits | 147,361 | 195 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.maap.last.if0` | 439,384 | 4.394 | 20 | 50 | fits | 148,236 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-4.service.srp.first.if0` | 533,754 | 5.338 | 20 | 20 | fits | 94,435 | 39 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-4.service.srp.last.if0` | 889,871 | 8.899 | 20 | 20 | fits | 94,774 | 51 | 0.531 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 375,476 | 3.755 | 20 | 20 | fits | 148,236 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 285,821 | 2.858 | 20 | 200 | fits | 148,199 | 200 | 0.358 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 433,448 | 4.334 | 20 | 200 | fits | 148,236 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 286,733 | 2.867 | 20 | 20 | fits | 148,199 | 200 | 0.358 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 528,579 | 5.286 | 20 | 20 | fits | 94,435 | 39 | 0.757 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 142,119 | 1.421 | 20 | 24 | fits | 144,563 | 161 | 0.224 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 289,343 | 2.893 | 20 | 24 | fits | 148,199 | 200 | 0.358 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 289,278 | 2.893 | 20 | 50 | fits | 148,199 | 200 | 0.358 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 437,124 | 4.371 | 20 | 50 | fits | 148,236 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 531,494 | 5.315 | 20 | 20 | fits | 94,435 | 39 | 0.757 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 887,744 | 8.877 | 20 | 20 | fits | 98,373 | 48 | 0.447 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-6.adp_available.if0` | 401,979 | 4.020 | 20 | 20 | fits | 154,807 | 171 | 0.430 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.adp.first.if0` | 293,028 | 2.930 | 20 | 200 | fits | 146,282 | 191 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.adp.last.if0` | 447,226 | 4.472 | 20 | 200 | fits | 154,807 | 171 | 0.430 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.acmp.first.if0` | 293,940 | 2.939 | 20 | 20 | fits | 146,282 | 191 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.acmp.last.if0` | 548,789 | 5.488 | 20 | 20 | fits | 100,867 | 46 | 0.657 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.aecp.first.if0` | 151,243 | 1.512 | 20 | 24 | fits | 144,619 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.aecp.last.if0` | 296,550 | 2.966 | 20 | 24 | fits | 146,282 | 191 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.maap.first.if0` | 296,485 | 2.965 | 20 | 50 | fits | 146,282 | 191 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.maap.last.if0` | 450,902 | 4.509 | 20 | 50 | fits | 154,807 | 171 | 0.430 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-6.service.srp.first.if0` | 551,704 | 5.517 | 20 | 20 | fits | 100,867 | 46 | 0.657 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-6.service.srp.last.if0` | 898,602 | 8.986 | 20 | 20 | fits | 81,746 | 40 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 398,341 | 3.983 | 20 | 20 | fits | 150,056 | 178 | 0.311 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 291,946 | 2.919 | 20 | 200 | fits | 148,320 | 185 | 0.431 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 441,393 | 4.414 | 20 | 200 | fits | 150,056 | 178 | 0.311 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 292,858 | 2.929 | 20 | 20 | fits | 148,320 | 185 | 0.431 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 547,458 | 5.475 | 20 | 20 | fits | 96,042 | 48 | 0.697 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 148,123 | 1.481 | 20 | 24 | fits | 144,619 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 295,468 | 2.955 | 20 | 24 | fits | 148,320 | 185 | 0.431 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 295,403 | 2.954 | 20 | 50 | fits | 148,320 | 185 | 0.431 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 445,069 | 4.451 | 20 | 50 | fits | 150,056 | 178 | 0.311 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 550,373 | 5.504 | 20 | 20 | fits | 96,042 | 48 | 0.697 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 891,402 | 8.914 | 20 | 20 | fits | 89,802 | 44 | 0.452 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-0.adp_available.if0` | 388,366 | 3.884 | 20 | 20 | fits | 151,282 | 176 | 0.356 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-0.service.adp.first.if0` | 296,294 | 2.963 | 20 | 200 | fits | 149,031 | 200 | 0.373 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-0.service.adp.last.if0` | 446,967 | 4.470 | 20 | 200 | fits | 151,282 | 176 | 0.356 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-0.service.acmp.first.if0` | 297,206 | 2.972 | 20 | 20 | fits | 149,031 | 200 | 0.373 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-0.service.acmp.last.if0` | 542,705 | 5.427 | 20 | 20 | fits | 95,042 | 39 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-0.service.aecp.first.if0` | 143,117 | 1.431 | 20 | 24 | fits | 144,953 | 162 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-0.service.aecp.last.if0` | 299,816 | 2.998 | 20 | 24 | fits | 149,031 | 200 | 0.373 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-0.service.maap.first.if0` | 299,751 | 2.998 | 20 | 50 | fits | 149,031 | 200 | 0.373 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-0.service.maap.last.if0` | 450,643 | 4.506 | 20 | 50 | fits | 151,282 | 176 | 0.356 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-0.service.srp.first.if0` | 545,620 | 5.456 | 20 | 20 | fits | 95,042 | 39 | 0.682 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-0.service.srp.last.if0` | 805,395 | 8.054 | 20 | 20 | fits | 65,131 | 32 | 0.511 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 356,478 | 3.565 | 20 | 20 | fits | 149,290 | 171 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 286,415 | 2.864 | 20 | 200 | fits | 148,964 | 200 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 435,096 | 4.351 | 20 | 200 | fits | 149,290 | 171 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 287,327 | 2.873 | 20 | 20 | fits | 148,964 | 200 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 530,567 | 5.306 | 20 | 20 | fits | 94,775 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 141,948 | 1.419 | 20 | 24 | fits | 144,729 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 289,937 | 2.899 | 20 | 24 | fits | 148,964 | 200 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 289,872 | 2.899 | 20 | 50 | fits | 148,964 | 200 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 438,772 | 4.388 | 20 | 50 | fits | 149,290 | 171 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 533,482 | 5.335 | 20 | 20 | fits | 94,775 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 808,583 | 8.086 | 20 | 20 | fits | 70,465 | 39 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-2.adp_available.if0` | 383,727 | 3.837 | 20 | 20 | fits | 148,370 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-2.service.adp.first.if0` | 294,034 | 2.940 | 20 | 200 | fits | 148,165 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-2.service.adp.last.if0` | 441,795 | 4.418 | 20 | 200 | fits | 148,370 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-2.service.acmp.first.if0` | 294,946 | 2.949 | 20 | 20 | fits | 148,165 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-2.service.acmp.last.if0` | 537,364 | 5.374 | 20 | 20 | fits | 94,873 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-2.service.aecp.first.if0` | 150,366 | 1.504 | 20 | 24 | fits | 144,673 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-2.service.aecp.last.if0` | 297,556 | 2.976 | 20 | 24 | fits | 148,165 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-2.service.maap.first.if0` | 297,491 | 2.975 | 20 | 50 | fits | 148,165 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-2.service.maap.last.if0` | 445,471 | 4.455 | 20 | 50 | fits | 148,370 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-2.service.srp.first.if0` | 540,279 | 5.403 | 20 | 20 | fits | 94,873 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-2.service.srp.last.if0` | 822,237 | 8.222 | 20 | 20 | fits | 80,009 | 42 | 0.561 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 380,067 | 3.801 | 20 | 20 | fits | 148,370 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 290,374 | 2.904 | 20 | 200 | fits | 148,165 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 438,135 | 4.381 | 20 | 200 | fits | 148,370 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 291,286 | 2.913 | 20 | 20 | fits | 148,165 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 533,877 | 5.339 | 20 | 20 | fits | 95,046 | 40 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 146,706 | 1.467 | 20 | 24 | fits | 144,673 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 293,896 | 2.939 | 20 | 24 | fits | 148,165 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 293,831 | 2.938 | 20 | 50 | fits | 148,165 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 441,811 | 4.418 | 20 | 50 | fits | 148,370 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 536,792 | 5.368 | 20 | 20 | fits | 95,046 | 40 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 899,007 | 8.990 | 20 | 20 | fits | 81,944 | 41 | 0.473 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-4.adp_available.if0` | 377,036 | 3.770 | 20 | 20 | fits | 148,543 | 171 | 0.334 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-4.service.adp.first.if0` | 287,343 | 2.873 | 20 | 200 | fits | 149,003 | 200 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-4.service.adp.last.if0` | 435,277 | 4.353 | 20 | 200 | fits | 148,543 | 171 | 0.334 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-4.service.acmp.first.if0` | 288,255 | 2.883 | 20 | 20 | fits | 149,003 | 200 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-4.service.acmp.last.if0` | 541,370 | 5.414 | 20 | 20 | fits | 96,458 | 50 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-4.service.aecp.first.if0` | 142,837 | 1.428 | 20 | 24 | fits | 144,673 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-4.service.aecp.last.if0` | 290,865 | 2.909 | 20 | 24 | fits | 149,003 | 200 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-4.service.maap.first.if0` | 290,800 | 2.908 | 20 | 50 | fits | 149,003 | 200 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-4.service.maap.last.if0` | 438,953 | 4.390 | 20 | 50 | fits | 148,543 | 171 | 0.334 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-4.service.srp.first.if0` | 544,285 | 5.443 | 20 | 20 | fits | 96,458 | 50 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-4.service.srp.last.if0` | 893,756 | 8.938 | 20 | 20 | fits | 73,471 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 399,350 | 3.994 | 20 | 20 | fits | 153,381 | 182 | 0.359 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 294,344 | 2.943 | 20 | 200 | fits | 147,265 | 192 | 0.379 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 456,227 | 4.562 | 20 | 200 | fits | 153,381 | 182 | 0.359 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 295,256 | 2.953 | 20 | 20 | fits | 147,265 | 192 | 0.379 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 551,334 | 5.513 | 20 | 20 | fits | 94,411 | 43 | 0.707 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 151,576 | 1.516 | 20 | 24 | fits | 144,729 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 297,866 | 2.979 | 20 | 24 | fits | 147,265 | 192 | 0.379 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 297,801 | 2.978 | 20 | 50 | fits | 147,265 | 192 | 0.379 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 459,903 | 4.599 | 20 | 50 | fits | 153,381 | 182 | 0.359 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 554,249 | 5.542 | 20 | 20 | fits | 94,411 | 43 | 0.707 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 904,267 | 9.043 | 20 | 20 | fits | 73,570 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-6.adp_available.if0` | 400,555 | 4.006 | 20 | 20 | fits | 144,209 | 171 | 0.379 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-6.service.adp.first.if0` | 300,149 | 3.001 | 20 | 200 | fits | 148,250 | 196 | 0.381 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-6.service.adp.last.if0` | 443,749 | 4.437 | 20 | 200 | fits | 144,209 | 171 | 0.379 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-6.service.acmp.first.if0` | 301,061 | 3.011 | 20 | 20 | fits | 148,250 | 196 | 0.381 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-6.service.acmp.last.if0` | 625,039 | 6.250 | 20 | 20 | fits | 100,059 | 46 | 0.651 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-6.service.aecp.first.if0` | 148,052 | 1.481 | 20 | 24 | fits | 144,865 | 162 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-6.service.aecp.last.if0` | 303,671 | 3.037 | 20 | 24 | fits | 148,250 | 196 | 0.381 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-6.service.maap.first.if0` | 303,606 | 3.036 | 20 | 50 | fits | 148,250 | 196 | 0.381 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-6.service.maap.last.if0` | 447,425 | 4.474 | 20 | 50 | fits | 144,209 | 171 | 0.379 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-6.service.srp.first.if0` | 627,954 | 6.280 | 20 | 20 | fits | 100,059 | 46 | 0.651 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-6.service.srp.last.if0` | 896,721 | 8.967 | 20 | 20 | fits | 73,631 | 37 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 465,153 | 4.652 | 20 | 20 | fits | 148,164 | 170 | 0.338 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 295,297 | 2.953 | 20 | 200 | fits | 154,399 | 200 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 523,424 | 5.234 | 20 | 200 | fits | 148,164 | 170 | 0.338 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 296,209 | 2.962 | 20 | 20 | fits | 154,399 | 200 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 619,172 | 6.192 | 20 | 20 | fits | 95,052 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 145,395 | 1.454 | 20 | 24 | fits | 145,063 | 161 | 0.229 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 298,819 | 2.988 | 20 | 24 | fits | 154,399 | 200 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 298,754 | 2.988 | 20 | 50 | fits | 154,399 | 200 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 527,100 | 5.271 | 20 | 50 | fits | 148,164 | 170 | 0.338 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 622,087 | 6.221 | 20 | 20 | fits | 95,052 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 897,216 | 8.972 | 20 | 20 | fits | 70,493 | 39 | 0.603 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-0.adp_available.if0` | 396,817 | 3.968 | 20 | 20 | fits | 152,523 | 177 | 0.374 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-0.service.adp.first.if0` | 294,022 | 2.940 | 20 | 200 | fits | 148,344 | 196 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-0.service.adp.last.if0` | 455,425 | 4.554 | 20 | 200 | fits | 152,523 | 177 | 0.374 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-0.service.acmp.first.if0` | 294,934 | 2.949 | 20 | 20 | fits | 148,344 | 196 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-0.service.acmp.last.if0` | 551,094 | 5.511 | 20 | 20 | fits | 94,973 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-0.service.aecp.first.if0` | 150,175 | 1.502 | 20 | 24 | fits | 144,743 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-0.service.aecp.last.if0` | 297,544 | 2.975 | 20 | 24 | fits | 148,344 | 196 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-0.service.maap.first.if0` | 297,479 | 2.975 | 20 | 50 | fits | 148,344 | 196 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-0.service.maap.last.if0` | 459,101 | 4.591 | 20 | 50 | fits | 152,523 | 177 | 0.374 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-0.service.srp.first.if0` | 554,009 | 5.540 | 20 | 20 | fits | 94,973 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-0.service.srp.last.if0` | 813,784 | 8.138 | 20 | 20 | fits | 65,131 | 32 | 0.511 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 390,576 | 3.906 | 20 | 20 | fits | 148,561 | 170 | 0.336 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 300,772 | 3.008 | 20 | 200 | fits | 149,329 | 200 | 0.374 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 448,724 | 4.487 | 20 | 200 | fits | 148,561 | 170 | 0.336 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 301,684 | 3.017 | 20 | 20 | fits | 149,329 | 200 | 0.374 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 544,324 | 5.443 | 20 | 20 | fits | 94,904 | 39 | 0.680 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 147,378 | 1.474 | 20 | 24 | fits | 144,906 | 162 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 304,294 | 3.043 | 20 | 24 | fits | 149,329 | 200 | 0.374 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 304,229 | 3.042 | 20 | 50 | fits | 149,329 | 200 | 0.374 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 452,400 | 4.524 | 20 | 50 | fits | 148,561 | 170 | 0.336 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 547,239 | 5.472 | 20 | 20 | fits | 94,904 | 39 | 0.680 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 807,440 | 8.074 | 20 | 20 | fits | 65,303 | 32 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-2.adp_available.if0` | 387,910 | 3.879 | 20 | 20 | fits | 148,463 | 170 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-2.service.adp.first.if0` | 298,124 | 2.981 | 20 | 200 | fits | 148,324 | 195 | 0.371 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-2.service.adp.last.if0` | 445,978 | 4.460 | 20 | 200 | fits | 148,463 | 170 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-2.service.acmp.first.if0` | 299,036 | 2.990 | 20 | 20 | fits | 148,324 | 195 | 0.371 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-2.service.acmp.last.if0` | 541,613 | 5.416 | 20 | 20 | fits | 94,939 | 39 | 0.681 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-2.service.aecp.first.if0` | 154,297 | 1.543 | 20 | 24 | fits | 145,285 | 162 | 0.241 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-2.service.aecp.last.if0` | 301,646 | 3.016 | 20 | 24 | fits | 148,324 | 195 | 0.371 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-2.service.maap.first.if0` | 301,581 | 3.016 | 20 | 50 | fits | 148,324 | 195 | 0.371 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-2.service.maap.last.if0` | 449,654 | 4.497 | 20 | 50 | fits | 148,463 | 170 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-2.service.srp.first.if0` | 544,528 | 5.445 | 20 | 20 | fits | 94,939 | 39 | 0.681 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-2.service.srp.last.if0` | 811,308 | 8.113 | 20 | 20 | fits | 71,882 | 39 | 0.586 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 357,432 | 3.574 | 20 | 20 | fits | 149,290 | 171 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 287,369 | 2.874 | 20 | 200 | fits | 149,008 | 200 | 0.368 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 436,050 | 4.361 | 20 | 200 | fits | 149,290 | 171 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 288,281 | 2.883 | 20 | 20 | fits | 149,008 | 200 | 0.368 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 531,521 | 5.315 | 20 | 20 | fits | 94,775 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 142,858 | 1.429 | 20 | 24 | fits | 144,776 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 290,891 | 2.909 | 20 | 24 | fits | 149,008 | 200 | 0.368 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 290,826 | 2.908 | 20 | 50 | fits | 149,008 | 200 | 0.368 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 439,726 | 4.397 | 20 | 50 | fits | 149,290 | 171 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 534,436 | 5.344 | 20 | 20 | fits | 94,775 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 815,811 | 8.158 | 20 | 20 | fits | 78,353 | 43 | 0.570 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-4.adp_available.if0` | 385,563 | 3.856 | 20 | 20 | fits | 148,370 | 170 | 0.333 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-4.service.adp.first.if0` | 295,870 | 2.959 | 20 | 200 | fits | 148,209 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-4.service.adp.last.if0` | 443,631 | 4.436 | 20 | 200 | fits | 148,370 | 170 | 0.333 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-4.service.acmp.first.if0` | 296,782 | 2.968 | 20 | 20 | fits | 148,209 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-4.service.acmp.last.if0` | 538,486 | 5.385 | 20 | 20 | fits | 94,159 | 43 | 0.704 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-4.service.aecp.first.if0` | 152,158 | 1.522 | 20 | 24 | fits | 144,832 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-4.service.aecp.last.if0` | 299,392 | 2.994 | 20 | 24 | fits | 148,209 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-4.service.maap.first.if0` | 299,327 | 2.993 | 20 | 50 | fits | 148,209 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-4.service.maap.last.if0` | 447,307 | 4.473 | 20 | 50 | fits | 148,370 | 170 | 0.333 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-4.service.srp.first.if0` | 541,401 | 5.414 | 20 | 20 | fits | 94,159 | 43 | 0.704 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-4.service.srp.last.if0` | 826,550 | 8.265 | 20 | 20 | fits | 90,096 | 44 | 0.457 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 382,603 | 3.826 | 20 | 20 | fits | 148,580 | 171 | 0.335 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 292,910 | 2.929 | 20 | 200 | fits | 148,209 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 440,881 | 4.409 | 20 | 200 | fits | 148,580 | 171 | 0.335 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 293,822 | 2.938 | 20 | 20 | fits | 148,209 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 547,171 | 5.472 | 20 | 20 | fits | 96,655 | 50 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 149,198 | 1.492 | 20 | 24 | fits | 144,832 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 296,432 | 2.964 | 20 | 24 | fits | 148,209 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 296,367 | 2.964 | 20 | 50 | fits | 148,209 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 444,557 | 4.446 | 20 | 50 | fits | 148,580 | 171 | 0.335 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 550,086 | 5.501 | 20 | 20 | fits | 96,655 | 50 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 818,722 | 8.187 | 20 | 20 | fits | 81,603 | 40 | 0.466 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-6.adp_available.if0` | 390,163 | 3.902 | 20 | 20 | fits | 145,348 | 173 | 0.389 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-6.service.adp.first.if0` | 289,950 | 2.900 | 20 | 200 | fits | 148,209 | 195 | 0.370 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-6.service.adp.last.if0` | 434,689 | 4.347 | 20 | 200 | fits | 145,348 | 173 | 0.389 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-6.service.acmp.first.if0` | 290,862 | 2.909 | 20 | 20 | fits | 148,209 | 195 | 0.370 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-6.service.acmp.last.if0` | 545,960 | 5.460 | 20 | 20 | fits | 101,058 | 46 | 0.662 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-6.service.aecp.first.if0` | 146,238 | 1.462 | 20 | 24 | fits | 144,832 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-6.service.aecp.last.if0` | 293,472 | 2.935 | 20 | 24 | fits | 148,209 | 195 | 0.370 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-6.service.maap.first.if0` | 293,407 | 2.934 | 20 | 50 | fits | 148,209 | 195 | 0.370 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-6.service.maap.last.if0` | 438,365 | 4.384 | 20 | 50 | fits | 145,348 | 173 | 0.389 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-6.service.srp.first.if0` | 548,875 | 5.489 | 20 | 20 | fits | 101,058 | 46 | 0.662 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-6.service.srp.last.if0` | 817,256 | 8.173 | 20 | 20 | fits | 73,367 | 36 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 396,957 | 3.970 | 20 | 20 | fits | 145,618 | 172 | 0.410 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 287,766 | 2.878 | 20 | 200 | fits | 149,267 | 201 | 0.369 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 441,886 | 4.419 | 20 | 200 | fits | 145,618 | 172 | 0.410 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 288,678 | 2.887 | 20 | 20 | fits | 149,267 | 201 | 0.369 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 542,946 | 5.429 | 20 | 20 | fits | 100,364 | 45 | 0.650 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 142,996 | 1.430 | 20 | 24 | fits | 144,832 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 291,288 | 2.913 | 20 | 24 | fits | 149,267 | 201 | 0.369 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 291,223 | 2.912 | 20 | 50 | fits | 149,267 | 201 | 0.369 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 445,562 | 4.456 | 20 | 50 | fits | 145,618 | 172 | 0.410 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 545,861 | 5.459 | 20 | 20 | fits | 100,364 | 45 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 813,944 | 8.139 | 20 | 20 | fits | 73,367 | 36 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-0.adp_available.if0` | 377,567 | 3.776 | 20 | 20 | fits | 148,954 | 175 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.adp.first.if0` | 285,559 | 2.856 | 20 | 200 | fits | 147,924 | 196 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.adp.last.if0` | 433,904 | 4.339 | 20 | 200 | fits | 148,954 | 175 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.acmp.first.if0` | 286,471 | 2.865 | 20 | 20 | fits | 147,924 | 196 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.acmp.last.if0` | 529,624 | 5.296 | 20 | 20 | fits | 95,024 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.aecp.first.if0` | 142,132 | 1.421 | 20 | 24 | fits | 144,747 | 161 | 0.226 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.aecp.last.if0` | 289,081 | 2.891 | 20 | 24 | fits | 147,924 | 196 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.maap.first.if0` | 289,016 | 2.890 | 20 | 50 | fits | 147,924 | 196 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.maap.last.if0` | 437,580 | 4.376 | 20 | 50 | fits | 148,954 | 175 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-0.service.srp.first.if0` | 532,539 | 5.325 | 20 | 20 | fits | 95,024 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-0.service.srp.last.if0` | 808,027 | 8.080 | 20 | 20 | fits | 70,486 | 39 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 359,431 | 3.594 | 20 | 20 | fits | 154,132 | 160 | 0.314 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 289,261 | 2.893 | 20 | 200 | fits | 143,208 | 210 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 442,784 | 4.428 | 20 | 200 | fits | 154,132 | 160 | 0.314 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 290,173 | 2.902 | 20 | 20 | fits | 143,208 | 210 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 538,598 | 5.386 | 20 | 20 | fits | 95,118 | 40 | 0.677 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 150,550 | 1.506 | 20 | 24 | fits | 144,691 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 292,783 | 2.928 | 20 | 24 | fits | 143,208 | 210 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 292,718 | 2.927 | 20 | 50 | fits | 143,208 | 210 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 446,460 | 4.465 | 20 | 50 | fits | 154,132 | 160 | 0.314 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 541,513 | 5.415 | 20 | 20 | fits | 95,118 | 40 | 0.677 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 817,010 | 8.170 | 20 | 20 | fits | 73,540 | 36 | 0.492 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-2.adp_available.if0` | 355,771 | 3.558 | 20 | 20 | fits | 154,305 | 161 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.adp.first.if0` | 285,601 | 2.856 | 20 | 200 | fits | 143,208 | 210 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.adp.last.if0` | 439,297 | 4.393 | 20 | 200 | fits | 154,305 | 161 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.acmp.first.if0` | 286,513 | 2.865 | 20 | 20 | fits | 143,208 | 210 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.acmp.last.if0` | 547,852 | 5.479 | 20 | 20 | fits | 98,542 | 46 | 0.695 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.aecp.first.if0` | 146,890 | 1.469 | 20 | 24 | fits | 144,691 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.aecp.last.if0` | 289,123 | 2.891 | 20 | 24 | fits | 143,208 | 210 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.maap.first.if0` | 289,058 | 2.891 | 20 | 50 | fits | 143,208 | 210 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.maap.last.if0` | 442,973 | 4.430 | 20 | 50 | fits | 154,305 | 161 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-2.service.srp.first.if0` | 550,767 | 5.508 | 20 | 20 | fits | 98,542 | 46 | 0.695 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-2.service.srp.last.if0` | 817,629 | 8.176 | 20 | 20 | fits | 71,483 | 38 | 0.580 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 365,864 | 3.659 | 20 | 20 | fits | 144,794 | 156 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 282,583 | 2.826 | 20 | 200 | fits | 144,225 | 216 | 0.361 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 436,143 | 4.361 | 20 | 200 | fits | 144,794 | 156 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 283,495 | 2.835 | 20 | 20 | fits | 144,225 | 216 | 0.361 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 536,985 | 5.370 | 20 | 20 | fits | 100,146 | 45 | 0.650 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 142,855 | 1.429 | 20 | 24 | fits | 144,691 | 161 | 0.225 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 286,105 | 2.861 | 20 | 24 | fits | 144,225 | 216 | 0.361 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 286,040 | 2.860 | 20 | 50 | fits | 144,225 | 216 | 0.361 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 439,819 | 4.398 | 20 | 50 | fits | 144,794 | 156 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 539,900 | 5.399 | 20 | 20 | fits | 100,146 | 45 | 0.650 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 893,489 | 8.935 | 20 | 20 | fits | 82,209 | 41 | 0.475 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-4.adp_available.if0` | 370,578 | 3.706 | 20 | 20 | fits | 141,811 | 151 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.adp.first.if0` | 300,371 | 3.004 | 20 | 200 | fits | 144,365 | 215 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.adp.last.if0` | 441,573 | 4.416 | 20 | 200 | fits | 141,811 | 151 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.acmp.first.if0` | 301,283 | 3.013 | 20 | 20 | fits | 144,365 | 215 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.acmp.last.if0` | 541,836 | 5.418 | 20 | 20 | fits | 99,567 | 49 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.aecp.first.if0` | 151,941 | 1.519 | 20 | 24 | fits | 144,928 | 162 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.aecp.last.if0` | 303,893 | 3.039 | 20 | 24 | fits | 144,365 | 215 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.maap.first.if0` | 303,828 | 3.038 | 20 | 50 | fits | 144,365 | 215 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.maap.last.if0` | 445,249 | 4.452 | 20 | 50 | fits | 141,811 | 151 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-4.service.srp.first.if0` | 544,751 | 5.448 | 20 | 20 | fits | 99,567 | 49 | 0.676 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-4.service.srp.last.if0` | 899,616 | 8.996 | 20 | 20 | fits | 81,707 | 40 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 366,810 | 3.668 | 20 | 20 | fits | 141,811 | 151 | 0.347 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 296,603 | 2.966 | 20 | 200 | fits | 144,365 | 215 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 437,805 | 4.378 | 20 | 200 | fits | 141,811 | 151 | 0.347 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 297,515 | 2.975 | 20 | 20 | fits | 144,365 | 215 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 538,068 | 5.381 | 20 | 20 | fits | 99,567 | 49 | 0.676 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 148,173 | 1.482 | 20 | 24 | fits | 144,820 | 162 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 300,125 | 3.001 | 20 | 24 | fits | 144,365 | 215 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 300,060 | 3.001 | 20 | 50 | fits | 144,365 | 215 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 441,481 | 4.415 | 20 | 50 | fits | 141,811 | 151 | 0.347 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 540,983 | 5.410 | 20 | 20 | fits | 99,567 | 49 | 0.676 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 895,848 | 8.958 | 20 | 20 | fits | 81,707 | 40 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-6.adp_available.if0` | 363,497 | 3.635 | 20 | 20 | fits | 149,045 | 156 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.adp.first.if0` | 285,188 | 2.852 | 20 | 200 | fits | 143,252 | 210 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.adp.last.if0` | 433,624 | 4.336 | 20 | 200 | fits | 149,045 | 156 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.acmp.first.if0` | 286,100 | 2.861 | 20 | 20 | fits | 143,252 | 210 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.acmp.last.if0` | 612,668 | 6.127 | 20 | 20 | fits | 100,526 | 46 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.aecp.first.if0` | 146,433 | 1.464 | 20 | 24 | fits | 144,860 | 161 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.aecp.last.if0` | 288,710 | 2.887 | 20 | 24 | fits | 143,252 | 210 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.maap.first.if0` | 288,645 | 2.886 | 20 | 50 | fits | 143,252 | 210 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.maap.last.if0` | 437,300 | 4.373 | 20 | 50 | fits | 149,045 | 156 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-6.service.srp.first.if0` | 615,583 | 6.156 | 20 | 20 | fits | 100,526 | 46 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-6.service.srp.last.if0` | 899,943 | 8.999 | 20 | 20 | fits | 82,250 | 40 | 0.486 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 360,926 | 3.609 | 20 | 20 | fits | 149,045 | 156 | 0.373 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 282,617 | 2.826 | 20 | 200 | fits | 144,090 | 215 | 0.360 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 431,053 | 4.311 | 20 | 200 | fits | 149,045 | 156 | 0.373 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 283,529 | 2.835 | 20 | 20 | fits | 144,090 | 215 | 0.360 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 610,307 | 6.103 | 20 | 20 | fits | 100,736 | 47 | 0.653 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 143,024 | 1.430 | 20 | 24 | fits | 144,860 | 161 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 286,139 | 2.861 | 20 | 24 | fits | 144,090 | 215 | 0.360 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 286,074 | 2.861 | 20 | 50 | fits | 144,090 | 215 | 0.360 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 434,729 | 4.347 | 20 | 50 | fits | 149,045 | 156 | 0.373 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 613,222 | 6.132 | 20 | 20 | fits | 100,736 | 47 | 0.653 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 897,100 | 8.971 | 20 | 20 | fits | 81,776 | 40 | 0.471 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-0.adp_available.if0` | 367,118 | 3.671 | 20 | 20 | fits | 154,354 | 160 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.adp.first.if0` | 296,806 | 2.968 | 20 | 200 | fits | 144,324 | 215 | 0.365 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.adp.last.if0` | 450,551 | 4.506 | 20 | 200 | fits | 154,354 | 160 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.acmp.first.if0` | 297,718 | 2.977 | 20 | 20 | fits | 144,324 | 215 | 0.365 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.acmp.last.if0` | 546,045 | 5.460 | 20 | 20 | fits | 94,798 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.aecp.first.if0` | 148,417 | 1.484 | 20 | 24 | fits | 144,852 | 162 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.aecp.last.if0` | 300,328 | 3.003 | 20 | 24 | fits | 144,324 | 215 | 0.365 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.maap.first.if0` | 300,263 | 3.003 | 20 | 50 | fits | 144,324 | 215 | 0.365 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.maap.last.if0` | 454,227 | 4.542 | 20 | 50 | fits | 154,354 | 160 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-0.service.srp.first.if0` | 548,960 | 5.490 | 20 | 20 | fits | 94,798 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-0.service.srp.last.if0` | 809,326 | 8.093 | 20 | 20 | fits | 65,303 | 32 | 0.515 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 381,401 | 3.814 | 20 | 20 | fits | 148,954 | 175 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 289,393 | 2.894 | 20 | 200 | fits | 147,130 | 191 | 0.378 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 437,738 | 4.377 | 20 | 200 | fits | 148,954 | 175 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 290,305 | 2.903 | 20 | 20 | fits | 147,130 | 191 | 0.378 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 533,245 | 5.332 | 20 | 20 | fits | 94,811 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 146,760 | 1.468 | 20 | 24 | fits | 144,860 | 161 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 292,915 | 2.929 | 20 | 24 | fits | 147,130 | 191 | 0.378 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 292,850 | 2.929 | 20 | 50 | fits | 147,130 | 191 | 0.378 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 441,414 | 4.414 | 20 | 50 | fits | 148,954 | 175 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 536,160 | 5.362 | 20 | 20 | fits | 94,811 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 811,648 | 8.116 | 20 | 20 | fits | 70,486 | 39 | 0.602 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-2.adp_available.if0` | 378,503 | 3.785 | 20 | 20 | fits | 148,954 | 175 | 0.316 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.adp.first.if0` | 286,495 | 2.865 | 20 | 200 | fits | 147,968 | 196 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.adp.last.if0` | 434,840 | 4.348 | 20 | 200 | fits | 148,954 | 175 | 0.316 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.acmp.first.if0` | 287,407 | 2.874 | 20 | 20 | fits | 147,968 | 196 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.acmp.last.if0` | 530,347 | 5.303 | 20 | 20 | fits | 94,811 | 39 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.aecp.first.if0` | 143,024 | 1.430 | 20 | 24 | fits | 144,860 | 161 | 0.227 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.aecp.last.if0` | 290,017 | 2.900 | 20 | 24 | fits | 147,968 | 196 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.maap.first.if0` | 289,952 | 2.900 | 20 | 50 | fits | 147,968 | 196 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.maap.last.if0` | 438,516 | 4.385 | 20 | 50 | fits | 148,954 | 175 | 0.316 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-2.service.srp.first.if0` | 533,262 | 5.333 | 20 | 20 | fits | 94,811 | 39 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-2.service.srp.last.if0` | 815,486 | 8.155 | 20 | 20 | fits | 80,197 | 42 | 0.564 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 362,025 | 3.620 | 20 | 20 | fits | 154,132 | 160 | 0.314 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 291,855 | 2.919 | 20 | 200 | fits | 143,252 | 210 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 445,378 | 4.454 | 20 | 200 | fits | 154,132 | 160 | 0.314 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 292,767 | 2.928 | 20 | 20 | fits | 143,252 | 210 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 541,003 | 5.410 | 20 | 20 | fits | 94,929 | 40 | 0.678 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 153,100 | 1.531 | 20 | 24 | fits | 144,916 | 161 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 295,377 | 2.954 | 20 | 24 | fits | 143,252 | 210 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 295,312 | 2.953 | 20 | 50 | fits | 143,252 | 210 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 449,054 | 4.491 | 20 | 50 | fits | 154,132 | 160 | 0.314 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 543,918 | 5.439 | 20 | 20 | fits | 94,929 | 40 | 0.678 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 825,692 | 8.257 | 20 | 20 | fits | 81,980 | 40 | 0.477 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-4.adp_available.if0` | 359,065 | 3.591 | 20 | 20 | fits | 154,342 | 161 | 0.317 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.adp.first.if0` | 288,895 | 2.889 | 20 | 200 | fits | 143,252 | 210 | 0.362 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.adp.last.if0` | 442,628 | 4.426 | 20 | 200 | fits | 154,342 | 161 | 0.317 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.acmp.first.if0` | 289,807 | 2.898 | 20 | 20 | fits | 143,252 | 210 | 0.362 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.acmp.last.if0` | 548,836 | 5.488 | 20 | 20 | fits | 96,573 | 50 | 0.709 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.aecp.first.if0` | 150,140 | 1.501 | 20 | 24 | fits | 144,916 | 161 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.aecp.last.if0` | 292,417 | 2.924 | 20 | 24 | fits | 143,252 | 210 | 0.362 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.maap.first.if0` | 292,352 | 2.924 | 20 | 50 | fits | 143,252 | 210 | 0.362 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.maap.last.if0` | 446,304 | 4.463 | 20 | 50 | fits | 154,342 | 161 | 0.317 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-4.service.srp.first.if0` | 551,751 | 5.518 | 20 | 20 | fits | 96,573 | 50 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-4.service.srp.last.if0` | 820,798 | 8.208 | 20 | 20 | fits | 81,775 | 40 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 369,215 | 3.692 | 20 | 20 | fits | 144,944 | 157 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 286,197 | 2.862 | 20 | 200 | fits | 143,514 | 211 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 439,529 | 4.395 | 20 | 200 | fits | 144,944 | 157 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 287,109 | 2.871 | 20 | 20 | fits | 143,514 | 211 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 540,116 | 5.401 | 20 | 20 | fits | 99,891 | 49 | 0.679 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 147,180 | 1.472 | 20 | 24 | fits | 144,916 | 161 | 0.228 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 289,719 | 2.897 | 20 | 24 | fits | 143,514 | 211 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 289,654 | 2.897 | 20 | 50 | fits | 143,514 | 211 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 443,205 | 4.432 | 20 | 50 | fits | 144,944 | 157 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 543,031 | 5.430 | 20 | 20 | fits | 99,891 | 49 | 0.679 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 820,137 | 8.201 | 20 | 20 | fits | 81,806 | 40 | 0.469 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-6.adp_available.if0` | 370,780 | 3.708 | 20 | 20 | fits | 150,323 | 162 | 0.375 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.adp.first.if0` | 291,256 | 2.913 | 20 | 200 | fits | 144,026 | 215 | 0.364 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.adp.last.if0` | 440,970 | 4.410 | 20 | 200 | fits | 150,323 | 162 | 0.375 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.acmp.first.if0` | 292,168 | 2.922 | 20 | 20 | fits | 144,026 | 215 | 0.364 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.acmp.last.if0` | 542,049 | 5.420 | 20 | 20 | fits | 100,383 | 45 | 0.652 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.aecp.first.if0` | 143,302 | 1.433 | 20 | 24 | fits | 145,138 | 162 | 0.231 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.aecp.last.if0` | 294,778 | 2.948 | 20 | 24 | fits | 144,026 | 215 | 0.364 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.maap.first.if0` | 294,713 | 2.947 | 20 | 50 | fits | 144,026 | 215 | 0.364 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.maap.last.if0` | 444,646 | 4.446 | 20 | 50 | fits | 150,323 | 162 | 0.375 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-6.service.srp.first.if0` | 544,964 | 5.450 | 20 | 20 | fits | 100,383 | 45 | 0.652 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-6.service.srp.last.if0` | 813,473 | 8.135 | 20 | 20 | fits | 73,539 | 36 | 0.490 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 386,164 | 3.862 | 20 | 20 | fits | 143,987 | 171 | 0.377 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 285,897 | 2.859 | 20 | 200 | fits | 147,937 | 196 | 0.375 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 429,275 | 4.293 | 20 | 200 | fits | 143,987 | 171 | 0.377 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 286,809 | 2.868 | 20 | 20 | fits | 147,937 | 196 | 0.375 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 530,061 | 5.301 | 20 | 20 | fits | 100,090 | 45 | 0.648 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 142,457 | 1.425 | 20 | 24 | fits | 145,119 | 161 | 0.231 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 289,419 | 2.894 | 20 | 24 | fits | 147,937 | 196 | 0.375 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 289,354 | 2.894 | 20 | 50 | fits | 147,937 | 196 | 0.375 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 432,951 | 4.330 | 20 | 50 | fits | 143,987 | 171 | 0.377 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 532,976 | 5.330 | 20 | 20 | fits | 100,090 | 45 | 0.648 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 801,316 | 8.013 | 20 | 20 | fits | 73,459 | 37 | 0.486 |
| LINK_UP | `adp.link_up.if0` | 2,652 | 0.027 | 20 | 200 | fits | 23,799 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,833 | 0.118 | 20 | 200 | fits | 20,765 | 23 (39) | 0.729 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 1,802 | 0.018 | 20 | 200 | fits | 2,678 | 10 (11) | 0.500 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 268,985 | 2.690 | 20 | 200 | fits | 121,396 | 154 | 0.337 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 248,848 | 2.488 | 20 | 20 | fits | 121,396 | 154 | 0.337 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 253,354 | 2.534 | 20 | 24 | fits | 94,710 | 61 | 0.456 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 184,827 | 1.848 | 20 | 50 | fits | 83,447 | 106 | 0.356 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 712,058 | 7.121 | 20 | 20 | fits | 94,710 | 61 | 0.456 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 87,864 | 0.879 | 20 | 20 | fits | 0 | - | 0.000 |
| ADP record, every channel at its refill rate, the longest | `save-starved.held.adp.if0` | 272,195 | 2.722 | 20 | 200 | fits | 124,606 | 160 | 0.369 |
| ACMP record, every channel at its refill rate, the longest | `save-starved.held.acmp.if0` | 313,475 | 3.135 | 20 | 20 | fits | 88,805 | 66 | 0.353 |
| AECP record, every channel at its refill rate, the longest | `save-starved.held.aecp.if0` | 254,471 | 2.545 | 20 | 24 | fits | 97,581 | 67 | 0.474 |
| MAAP record, every channel at its refill rate, the longest | `save-starved.held.maap.if0` | 185,195 | 1.852 | 20 | 50 | fits | 142,560 | 215 | 0.332 |
| SRP record, every channel at its refill rate, the longest | `save-starved.held.srp.if0` | 749,378 | 7.494 | 20 | 20 | fits | 36,203 | 22 | 0.737 |
| an MRPDU its periodic timer owes, the longest | `save-starved.mrpdu.periodic.if0` | 90,405 | 0.904 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 13,632 | 0.136 | 20 | 20 | fits | 28,784 | 21 (35) | 0.808 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 9,470 | 0.095 | 20 | 20 | fits | 22,607 | 17 (14) | 0.849 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 8,190 | 0.082 | 20 | 20 | fits | 22,237 | 18 (14) | 0.842 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 15,884 | 0.159 | 20 | 20 | fits | 29,293 | 21 (35) | 0.815 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 80,490 | 0.805 | 20 | 20 | fits | 64,021 | 6 | 0.882 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 37,343 | 0.373 | 20 | 20 | fits | 37,408 | 12 | 0.877 |
| malformed MRPDU discard | `srp.malformed.if0` | 14,816 | 0.148 | 20 | 20 | fits | 14,881 | 12 | 0.547 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 83,668 | 0.837 | 220 | 220 | fits | 90,543 | 9 | 0.867 |
| an event behind 15 others | `backlog.event.if0` | 162,909 | 1.629 | 20 | 200 | fits | 47,877 | 78 | 0.542 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 446,190 | 4.462 | 20 | 20 | fits | 75,281 | 90 | 0.212 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 405,395 | 4.054 | 20 | 200 | fits | 142,938 | 122 | 0.310 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 404,786 | 4.048 | 20 | 200 | fits | 142,938 | 122 | 0.310 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 401,136 | 4.011 | 20 | 20 | fits | 142,938 | 122 | 0.310 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 475,592 | 4.756 | 20 | 20 | fits | 75,281 | 90 | 0.212 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,630 | 1.516 | 20 | 24 | fits | 152,512 | 167 | 0.262 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 260,808 | 2.608 | 20 | 24 | fits | 62,276 | 26 | 0.666 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 403,681 | 4.037 | 20 | 50 | fits | 142,938 | 122 | 0.310 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 403,291 | 4.033 | 20 | 50 | fits | 142,938 | 122 | 0.310 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 478,507 | 4.785 | 20 | 20 | fits | 75,281 | 90 | 0.212 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 522,601 | 5.226 | 20 | 20 | fits | 19,370 | 40 | 0.129 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 357,614 | 3.576 | 20 | 20 | fits | 149,482 | 172 | 0.346 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 287,440 | 2.874 | 20 | 200 | fits | 146,854 | 195 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 436,313 | 4.363 | 20 | 200 | fits | 149,482 | 172 | 0.346 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 288,352 | 2.884 | 20 | 20 | fits | 146,854 | 195 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 545,061 | 5.451 | 20 | 20 | fits | 99,098 | 46 | 0.701 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 145,083 | 1.451 | 20 | 24 | fits | 145,268 | 164 | 0.234 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 290,962 | 2.910 | 20 | 24 | fits | 146,854 | 195 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 290,897 | 2.909 | 20 | 50 | fits | 146,854 | 195 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 439,989 | 4.400 | 20 | 50 | fits | 149,482 | 172 | 0.346 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 547,976 | 5.480 | 20 | 20 | fits | 99,098 | 46 | 0.701 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 814,910 | 8.149 | 20 | 20 | fits | 73,705 | 36 | 0.496 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 9,412 | 0.094 | 20 | 20 | fits | 23,626 | 19 | 0.776 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 287,440 | 2.874 | 20 | 200 | fits | 146,854 | 195 | 0.356 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 26,352 | 0.264 | 20 | 200 | fits | 23,626 | 19 | 0.776 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 288,352 | 2.884 | 20 | 20 | fits | 146,854 | 195 | 0.356 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 439,622 | 4.396 | 20 | 20 | fits | 152,095 | 171 | 0.273 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 145,083 | 1.451 | 20 | 24 | fits | 145,268 | 164 | 0.234 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 290,962 | 2.910 | 20 | 24 | fits | 146,854 | 195 | 0.356 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 290,897 | 2.909 | 20 | 50 | fits | 146,854 | 195 | 0.356 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 442,602 | 4.426 | 20 | 50 | fits | 152,095 | 171 | 0.273 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 552,595 | 5.526 | 20 | 20 | fits | 100,852 | 47 | 0.664 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 802,222 | 8.022 | 20 | 20 | fits | 57,233 | 28 | 0.551 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,245,576 | 62.456 | 20 | 20 | MISS ceiling | 17,552 | 12 | 0.674 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,025,841 | 360.258 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,025,766 | 360.258 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,025,691 | 360.257 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,025,616 | 360.256 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,372 | 1.544 | 20 | 200 | fits | 149,609 | 200 | 0.369 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 294,589 | 2.946 | 20 | 200 | fits | 140,826 | 203 | 0.268 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 150,113 | 1.501 | 20 | 20 | fits | 149,609 | 200 | 0.369 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 290,114 | 2.901 | 20 | 20 | fits | 140,826 | 203 | 0.268 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 153,698 | 1.537 | 20 | 24 | fits | 149,609 | 200 | 0.369 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,154,756 | 61.548 | 20 | 24 | MISS ceiling | 122,573 | 103 | 0.281 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 152,658 | 1.527 | 20 | 50 | fits | 149,609 | 200 | 0.369 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 293,094 | 2.931 | 20 | 50 | fits | 140,826 | 203 | 0.268 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 390,970 | 3.910 | 20 | 20 | fits | 97,941 | 41 | 0.646 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 641,819 | 6.418 | 20 | 20 | fits | 57,570 | 29 | 0.557 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 5,326 | 0.053 | 20 | 20 | fits | 20,942 | 13 (29) | 0.759 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 6,417 | 0.064 | 20 | 20 | fits | 23,222 | 19 (35) | 0.769 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 22,611 | 0.226 | 20 | 20 | fits | 28,584 | 21 (12) | 0.806 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,699 | 0.117 | 20 | 50 | fits | 23,799 | 43 | 0.717 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 13,716 | 0.137 | 20 | 50 | fits | 23,788 | 41 | 0.679 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 13,401 | 0.134 | 20 | 50 | fits | 20,783 | 35 | 0.698 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 13,695 | 0.137 | 20 | 50 | fits | 26,550 | 61 | 0.637 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 15,712 | 0.157 | 20 | 50 | fits | 26,550 | 61 | 0.637 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,321 | 0.103 | 20 | 50 | fits | 18,795 | 30 | 0.596 |
| LINK_UP | `adp.link_up.if0` | 2,652 | 0.027 | 20 | 200 | fits | 23,799 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,833 | 0.118 | 20 | 200 | fits | 20,765 | 23 (39) | 0.729 |
| LINK_DOWN | `adp.link_down.if0` | 2,397 | 0.024 | 20 | 200 | fits | 23,284 | 23 (9) | 0.765 |
| LINK_UP | `adp.link_up.if0` | 2,652 | 0.027 | 20 | 200 | fits | 23,799 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,833 | 0.118 | 20 | 200 | fits | 20,765 | 23 (39) | 0.729 |
| GM_CHANGE | `adp.gm_change.if0` | 2,540 | 0.025 | 20 | 200 | fits | 12,537 | 17 (11) | 0.677 |
| LINK_UP | `adp.link_up.if0` | 2,652 | 0.027 | 20 | 200 | fits | 23,799 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,833 | 0.118 | 20 | 200 | fits | 20,765 | 23 (39) | 0.729 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,026 | 0.040 | 20 | 200 | fits | 12,111 | 16 (31) | 0.565 |
| LINK_UP | `adp.link_up.if0` | 2,652 | 0.027 | 20 | 200 | fits | 23,799 | 43 (11) | 0.717 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 11,833 | 0.118 | 20 | 200 | fits | 20,765 | 23 (39) | 0.729 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,026 | 0.040 | 20 | 200 | fits | 12,111 | 16 (31) | 0.565 |
| set_name | `aecp_fanout.set_name.if0` | 52,142 | 0.521 | 20 | 24 | fits | 51,233 | 89 | 0.548 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 41,069 | 0.411 | 20 | 24 | fits | 46,724 | 78 | 0.570 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 46,392 | 0.464 | 20 | 24 | fits | 43,011 | 79 | 0.521 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 39,015 | 0.390 | 20 | 24 | fits | 43,996 | 78 | 0.546 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 41,683 | 0.417 | 20 | 24 | fits | 47,865 | 67 | 0.595 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 46,667 | 0.467 | 20 | 24 | fits | 44,498 | 66 | 0.552 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 34,870 | 0.349 | 20 | 24 | fits | 44,375 | 67 | 0.572 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 46,209 | 0.462 | 20 | 24 | fits | 43,046 | 78 | 0.532 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 39,249 | 0.392 | 20 | 24 | fits | 43,201 | 79 | 0.537 |
| BIND_RX | `acmp.bind_rx.if0` | 22,638 | 0.226 | 20 | 20 | fits | 41,098 | 26 (77) | 0.776 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,064 | 0.081 | 20 | 20 | fits | 26,401 | 19 (32) | 0.805 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 11,961 | 0.120 | 20 | 20 | fits | 26,348 | 15 (47) | 0.714 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 14,299 | 0.143 | 20 | 20 | fits | 33,778 | 19 (50) | 0.789 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 12,290 | 0.123 | 20 | 20 | fits | 26,088 | 17 (48) | 0.714 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 11,504 | 0.115 | 20 | 20 | fits | 24,286 | 16 (48) | 0.661 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,423 | 0.114 | 20 | 20 | fits | 24,024 | 16 (48) | 0.664 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 11,442 | 0.114 | 20 | 20 | fits | 23,995 | 16 (48) | 0.664 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 18,357 | 0.184 | 20 | 24 | fits | 24,372 | 20 | 0.776 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 19,888 | 0.199 | 20 | 24 | fits | 28,574 | 20 | 0.700 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 9,850 | 0.099 | 20 | 24 | fits | 23,030 | 20 | 0.709 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 14,812 | 0.148 | 20 | 24 | fits | 23,430 | 20 | 0.714 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 10,349 | 0.103 | 20 | 24 | fits | 23,646 | 20 | 0.707 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 15,701 | 0.157 | 20 | 24 | fits | 24,202 | 20 | 0.717 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 14,018 | 0.140 | 20 | 24 | fits | 28,143 | 26 | 0.716 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 9,955 | 0.100 | 20 | 24 | fits | 23,173 | 20 | 0.727 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 14,541 | 0.145 | 20 | 24 | fits | 23,001 | 20 | 0.731 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 12,067 | 0.121 | 20 | 24 | fits | 25,235 | 21 | 0.626 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,347 | 0.143 | 20 | 24 | fits | 22,647 | 20 | 0.750 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 9,135 | 0.091 | 20 | 24 | fits | 22,240 | 20 | 0.739 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 14,805 | 0.148 | 20 | 24 | fits | 23,421 | 20 | 0.722 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 10,276 | 0.103 | 20 | 24 | fits | 23,654 | 20 | 0.711 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 14,928 | 0.149 | 20 | 24 | fits | 23,667 | 20 | 0.734 |
| get_configuration | `aecp.get_configuration.if0` | 12,942 | 0.129 | 20 | 24 | fits | 20,909 | 20 | 0.740 |
| entity_available | `aecp.entity_available.if0` | 7,862 | 0.079 | 20 | 24 | fits | 20,606 | 20 | 0.721 |
| get_name | `aecp.get_name.if0` | 15,257 | 0.153 | 20 | 24 | fits | 24,028 | 20 | 0.750 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 11,698 | 0.117 | 20 | 24 | fits | 24,891 | 27 | 0.713 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 16,851 | 0.169 | 20 | 24 | fits | 25,571 | 29 | 0.758 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 8,249 | 0.082 | 20 | 24 | fits | 21,376 | 20 | 0.747 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 13,473 | 0.135 | 20 | 24 | fits | 21,012 | 20 | 0.736 |
| set_name | `aecp.set_name.if0` | 30,151 | 0.302 | 20 | 24 | fits | 38,134 | 43 | 0.737 |
| lock_entity | `aecp.lock_entity.if0` | 24,825 | 0.248 | 20 | 24 | fits | 31,829 | 34 | 0.769 |
| unlock_entity | `aecp.unlock_entity.if0` | 20,938 | 0.209 | 20 | 24 | fits | 31,242 | 33 | 0.764 |
| LINK_UP | `fixture.link_up.if0` | 2,652 | 0.027 | 20 | 200 | fits | 23,799 | 43 (11) | 0.717 |
| malformed MRPDU discard | `fixture.malformed.if0` | 15,627 | 0.156 | 20 | 20 | fits | 15,692 | 12 | 0.641 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 30,117 | 0.301 | 20 | 24 | fits | 39,496 | 43 | 0.749 |
| LINK_DOWN | `fixture.link_down.if0` | 2,871 | 0.029 | 20 | 200 | fits | 24,920 | 23 (9) | 0.777 |
| BIND_RX | `fixture.bind_rx.if0` | 22,748 | 0.227 | 20 | 20 | fits | 41,217 | 26 (77) | 0.779 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 13,144 | 0.131 | 20 | 20 | fits | 36,932 | 29 (35) | 0.765 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 8,323 | 0.083 | 20 | 20 | fits | 22,116 | 13 (29) | 0.785 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 80,138 | 0.801 | 20 | 200 | fits | 80,241 | 51 | 0.748 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 80,138 | 0.801 | 20 | 200 | fits | 80,241 | 51 | 0.748 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 79,868 | 0.799 | 20 | 20 | fits | 80,241 | 51 | 0.748 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 79,868 | 0.799 | 20 | 20 | fits | 80,241 | 51 | 0.748 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 80,073 | 0.801 | 20 | 24 | fits | 80,241 | 51 | 0.748 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 80,073 | 0.801 | 20 | 24 | fits | 80,241 | 51 | 0.748 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 80,008 | 0.800 | 20 | 50 | fits | 80,241 | 51 | 0.748 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 80,008 | 0.800 | 20 | 50 | fits | 80,241 | 51 | 0.748 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 79,943 | 0.799 | 20 | 20 | fits | 80,241 | 51 | 0.748 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 79,943 | 0.799 | 20 | 20 | fits | 80,241 | 51 | 0.748 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
