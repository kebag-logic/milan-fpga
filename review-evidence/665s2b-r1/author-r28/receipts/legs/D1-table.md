### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 81 paths and 6 of 141 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `acmp.bind_rx.if0` (acmp-cmd) | 0.232 (0.399) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.119 (0.207) | fits | 0 acmp | 1 | 0 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | `acmp.entity_available.if0` (acmp-disc) | 0.075 (0.210) | fits | 0 adp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.091 (0.356) | fits | 0 adp | 2 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.120 (0.225) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.108 (0.209) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.122 (0.221) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.121 (0.223) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.083 (0.249) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.122 (0.380) | fits | 0 events | 1 | 0 |
| TMR_NO_ADP (H-DISC) | 0 | `acmp.tmr_no_adp.if0` (acmp-disc) | 0.129 (0.402) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `fixture.tmr_no_resp1.if0` (fixture) | 0.192 (0.512) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.091 (0.358) | fits | 0 events | 1 | 0 |
| TMR_NO_TK | 0 | `acmp.tmr_no_tk.if0` (acmp-notk) | 0.147 (0.484) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.100 (0.360) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.151 (0.336) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER | 0 | `adp.discover.if0` (adp-discover) | 0.048 (0.115) | fits | 0 adp | 2 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.023 (0.112) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.025 (0.223) | fits | 0 events | 2 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-advertise) | 0.025 (0.224) | fits | 0 events | 6 | 0 |
| TMR_ADVERTISE expiry | 0 | `adp.tmr_advertise.if0` (adp-advertise) | 0.019 (0.025) | fits | 0 events | 1 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-advertise) | 0.131 (0.352) | fits | 0 events | 5 | 0 |
| entity_available | 0 | `aecp.entity_available.if0` (aecp) | 0.092 (0.186) | fits | 0 aecp | 1 | 0 |
| get_avb_info, refused ENTITY_MISBEHAVING | 0 | `aecp.get_avb_info.if0` (aecp) | 0.173 (0.398) | fits | 0 aecp | 1 | 0 |
| get_configuration | 0 | `aecp.get_configuration.if0` (aecp) | 0.118 (0.318) | fits | 0 aecp | 1 | 0 |
| get_counters, refused ENTITY_MISBEHAVING | 0 | `aecp.get_counters.if0` (aecp) | 0.124 (0.228) | fits | 0 aecp | 1 | 0 |
| get_name | 0 | `aecp.get_name.if0` (aecp) | 0.159 (0.382) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp.lock_entity.if0` (aecp) | 0.244 (0.436) | fits | 0 aecp | 1 | 0 |
| MVU GET_MILAN_INFO | 0 | `aecp.mvu_get_milan_info.if0` (aecp) | 0.140 (0.346) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (312 B) | 0 | `aecp.read_descriptor.t0.i0.c0.if0` (aecp) | 0.210 (0.424) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (106 B) | 0 | `aecp.read_descriptor.t1.i0.c0.if0` (aecp) | 0.112 (0.220) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (86 B) | 0 | `aecp.read_descriptor.t10.i2.c0.if0` (aecp) | 0.110 (0.218) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (72 B) | 0 | `aecp.read_descriptor.t12.i0.c0.if0` (aecp) | 0.155 (0.369) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (452 B) | 0 | `aecp.read_descriptor.t13.i0.c0.if0` (aecp) | 0.125 (0.235) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t14.i0.c0.if0` (aecp) | 0.149 (0.362) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (20 B) | 0 | `aecp.read_descriptor.t15.i0.c0.if0` (aecp) | 0.104 (0.205) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (148 B) | 0 | `aecp.read_descriptor.t2.i0.c0.if0` (aecp) | 0.157 (0.371) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (90 B) | 0 | `aecp.read_descriptor.t20.i24.c0.if0` (aecp) | 0.152 (0.368) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (113 B) | 0 | `aecp.read_descriptor.t26.i0.c0.if0` (aecp) | 0.114 (0.219) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (82 B) | 0 | `aecp.read_descriptor.t36.i0.c0.if0` (aecp) | 0.153 (0.375) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t5.i1.c0.if0` (aecp) | 0.112 (0.223) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (146 B) | 0 | `aecp.read_descriptor.t6.i1.c0.if0` (aecp) | 0.169 (0.384) | fits | 0 aecp | 1 | 0 |
| READ_DESCRIPTOR (102 B) | 0 | `aecp.read_descriptor.t9.i0.c0.if0` (aecp) | 0.159 (0.372) | fits | 0 aecp | 1 | 0 |
| register_unsolicited | 0 | `aecp.register_unsolicited.if0` (aecp) | 0.173 (0.389) | fits | 0 aecp | 1 | 0 |
| set_name | 0 | `aecp.set_name.if0` (aecp) | 0.228 (0.360) | fits | 0 aecp | 1 | 0 |
| unknown_command, refused NOT_IMPLEMENTED | 0 | `aecp.unknown_command.if0` (aecp) | 0.093 (0.198) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp.unlock_entity.if0` (aecp) | 0.250 (0.454) | fits | 0 aecp | 1 | 0 |
| add_audio_mappings | 0 | `aecp_fanout.add_audio_mappings.if0` (aecp-fanout) | 0.419 (0.641) | fits | 0 aecp | 1 | 0 |
| lock_entity | 0 | `aecp_fanout.lock_entity.if0` (aecp-fanout) | 0.396 (0.607) | fits | 0 aecp | 1 | 0 |
| remove_audio_mappings | 0 | `aecp_fanout.remove_audio_mappings.if0` (aecp-fanout) | 0.426 (0.655) | fits | 0 aecp | 1 | 0 |
| set_clock_source | 0 | `aecp_fanout.set_clock_source.if0` (aecp-fanout) | 0.466 (0.683) | fits | 0 aecp | 1 | 0 |
| set_control_identify_on | 0 | `aecp_fanout.set_control_identify_off.if0` (aecp-fanout) | 0.441 (0.641) | fits | 0 aecp | 2 | 0 |
| set_name | 0 | `aecp_fanout.set_name.if0` (aecp-fanout) | 0.462 (0.688) | fits | 0 aecp | 1 | 0 |
| set_sampling_rate | 0 | `aecp_fanout.set_sampling_rate.if0` (aecp-fanout) | 0.431 (0.629) | fits | 0 aecp | 1 | 0 |
| unlock_entity | 0 | `aecp_fanout.unlock_entity.if0` (aecp-fanout) | 0.459 (0.659) | fits | 0 aecp | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 4.875 (5.305) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 5.959 (6.424) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.066 (0.218) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.621 (2.273) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.392 (62.540) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.217 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.275 (0.368) | fits | 0 aecp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.167 (0.400) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.105 (0.180) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.118 (0.224) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.147 (0.400) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.134 (0.347) | fits | 0 events | 2 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-owed.service.acmp.first.if0` (backlog-owed) | 1.500 | fits | 0 acmp | 5 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.841 | fits | 11 acmp | 5 | 0 |
| ADP record released under the composed load, first | 0 | `backlog-owed.service.adp.first.if0` (backlog-owed) | 1.542 | fits | 0 adp | 5 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 6.371 | fits | 7 adp | 5 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-owed.service.aecp.first.if0` (backlog-owed) | 1.535 | fits | 0 aecp | 5 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.718 | MISS ceiling | 15 aecp | 5 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-owed.service.maap.first.if0` (backlog-owed) | 1.525 | fits | 0 maap | 5 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 6.408 | fits | 6 maap | 5 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-owed.service.srp.first.if0` (backlog-owed) | 4.244 | fits | 0 srp | 5 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-owed.service.srp.last.if0` (backlog-owed) | 6.185 | fits | 31 srp | 5 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.811 (1.192) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.370 (0.371) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.153 (0.153) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.792 (0.866) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 5.999 | 8 | 152,118 (1.521) | yes | - |
| backlog-adp | 0 | 8.619 | 8 | 156,237 (1.562) | yes | - |
| backlog-adp-refill | 0 | 40.544 | 23 | 149,084 (1.491) | yes | - |
| backlog-owed | 0 | 360.268 | 48 | 147,828 (1.478) | yes | - |
| fixture | 0 | 1.091 | 2 | 76,138 (0.761) | yes | - |

Composed maximum over the 4 backlog windows: 156,237 CPU cycles (1.562 ms), backlog-adp.
Over the windows that released their whole load only: 156,237 (1.562 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| acmp-notk | 3597 | 0 | 64,141 (0.641) | fits |
| adp-advertise | 592 | 0 | 64,141 (0.641) | fits |
| acmp-noresp | 2019 | 0 | 64,141 (0.641) | fits |
| save | 603 | 0 | 64,141 (0.641) | fits |
| srp | 285 | 0 | 87,441 (0.874) | fits |
| backlog | 283 | 0 | 152,118 (1.521) | fits |
| backlog-adp | 308 | 0 | 156,237 (1.562) | fits |
| backlog-adp-refill | 323 | 0 | 149,084 (1.491) | fits |
| backlog-owed | 331 | 0 | 155,502 (1.555) | fits |
| acmp-disc | 931 | 0 | 64,141 (0.641) | fits |
| maap | 176 | 0 | 64,141 (0.641) | fits |
| adp-link | 88 | 0 | 64,141 (0.641) | fits |
| adp-gm | 87 | 0 | 64,141 (0.641) | fits |
| adp-discover | 87 | 0 | 64,141 (0.641) | fits |
| control | 87 | 0 | 64,141 (0.641) | fits |
| aecp-fanout | 110 | 0 | 64,141 (0.641) | fits |
| acmp-cmd | 83 | 0 | 64,141 (0.641) | fits |
| aecp | 110 | 0 | 64,141 (0.641) | fits |
| fixture | 149 | 0 | 76,138 (0.761) | fits |

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save | 2018.440 | 4,070 | 102 | - | 10.839 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| acmp-notk | 1065 | 91,816 (0.918) | 78,028 (0.780) |
| adp-advertise | 578 | 18,274 (0.183) | 3,111 (0.031) |
| acmp-noresp | 615 | 91,574 (0.916) | 78,028 (0.780) |
| save | 585 | 90,745 (0.907) | 77,977 (0.780) |
| srp | 271 | 18,274 (0.183) | 3,111 (0.031) |
| backlog | 265 | 18,274 (0.183) | 3,111 (0.031) |
| backlog-adp | 271 | 18,274 (0.183) | 3,111 (0.031) |
| backlog-adp-refill | 274 | 18,274 (0.183) | 3,111 (0.031) |
| backlog-owed | 306 | 18,379 (0.184) | 3,170 (0.032) |
| acmp-disc | 305 | 91,622 (0.916) | 78,028 (0.780) |
| maap | 166 | 18,274 (0.183) | 3,111 (0.031) |
| adp-link | 80 | 18,274 (0.183) | 3,109 (0.031) |
| adp-gm | 80 | 18,274 (0.183) | 3,109 (0.031) |
| adp-discover | 80 | 18,274 (0.183) | 3,109 (0.031) |
| control | 80 | 18,274 (0.183) | 3,109 (0.031) |
| aecp-fanout | 79 | 18,274 (0.183) | 3,109 (0.031) |
| acmp-cmd | 65 | 18,274 (0.183) | 3,109 (0.031) |
| aecp | 79 | 18,274 (0.183) | 3,109 (0.031) |
| fixture | 54 | 14,202 (0.142) | 2,915 (0.029) |

Longest pass that carries a step: 91,816 CPU cycles (0.918 ms), acmp-notk; longest step: 78,028 (0.780 ms), acmp-notk.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| TMR_NO_TK | `acmp.tmr_no_tk.if0` | 14,743 | 0.147 | 20 | 20 | fits | 28,357 | 19 (14) | 0.891 |
| LINK_UP | `adp.link_up.if0` | 2,517 | 0.025 | 20 | 200 | fits | 22,416 | 43 (11) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,075 | 0.131 | 20 | 200 | fits | 20,127 | 23 (39) | 0.721 |
| TMR_ADVERTISE expiry | `adp.tmr_advertise.if0` | 1,859 | 0.019 | 20 | 200 | fits | 2,498 | 10 (11) | 0.478 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 15,307 | 0.153 | 20 | 20 | fits | 26,858 | 21 (35) | 0.818 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 9,122 | 0.091 | 20 | 20 | fits | 20,926 | 17 (14) | 0.857 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 10,012 | 0.100 | 20 | 20 | fits | 20,896 | 18 (14) | 0.856 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 12,183 | 0.122 | 20 | 20 | fits | 27,164 | 21 (35) | 0.820 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 79,237 | 0.792 | 20 | 20 | fits | 64,141 | 6 | 0.892 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 36,998 | 0.370 | 20 | 20 | fits | 37,063 | 12 | 0.894 |
| malformed MRPDU discard | `srp.malformed.if0` | 14,157 | 0.142 | 20 | 20 | fits | 14,222 | 12 | 0.643 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 81,077 | 0.811 | 220 | 220 | fits | 87,441 | 9 | 0.878 |
| an event behind 15 others | `backlog.event.if0` | 162,062 | 1.621 | 20 | 200 | fits | 75,217 | 109 | 0.478 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 487,470 | 4.875 | 20 | 20 | fits | 146,769 | 109 | 0.459 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 151,910 | 1.519 | 20 | 200 | fits | 152,118 | 215 | 0.472 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 529,688 | 5.297 | 20 | 200 | fits | 146,769 | 109 | 0.459 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 147,651 | 1.477 | 20 | 20 | fits | 152,118 | 215 | 0.472 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 525,213 | 5.252 | 20 | 20 | fits | 146,769 | 109 | 0.459 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 151,236 | 1.512 | 20 | 24 | fits | 152,118 | 215 | 0.472 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 566,230 | 5.662 | 20 | 24 | fits | 37,582 | 30 | 0.519 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 150,196 | 1.502 | 20 | 50 | fits | 152,118 | 215 | 0.472 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 315,989 | 3.160 | 20 | 50 | fits | 90,966 | 52 | 0.610 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 343,459 | 3.435 | 20 | 20 | fits | 24,365 | 53 | 0.233 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 379,344 | 3.793 | 20 | 20 | fits | 16,635 | 36 | 0.054 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 595,948 | 5.959 | 20 | 20 | fits | 156,237 | 180 | 0.507 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 144,402 | 1.444 | 20 | 200 | fits | 149,084 | 201 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 637,087 | 6.371 | 20 | 200 | fits | 156,237 | 180 | 0.507 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 145,314 | 1.453 | 20 | 20 | fits | 149,084 | 201 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 784,060 | 7.841 | 20 | 20 | fits | 146,277 | 107 | 0.495 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 148,899 | 1.489 | 20 | 24 | fits | 149,084 | 201 | 0.475 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 825,196 | 8.252 | 20 | 24 | fits | 37,701 | 30 | 0.515 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 147,859 | 1.479 | 20 | 50 | fits | 149,084 | 201 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 640,763 | 6.408 | 20 | 50 | fits | 156,237 | 180 | 0.507 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 282,990 | 2.830 | 20 | 20 | fits | 135,586 | 95 | 0.584 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 482,446 | 4.824 | 20 | 20 | fits | 77,675 | 36 | 0.485 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 6,566 | 0.066 | 20 | 20 | fits | 21,847 | 19 | 0.785 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 144,402 | 1.444 | 20 | 200 | fits | 149,084 | 201 | 0.475 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 21,368 | 0.214 | 20 | 200 | fits | 21,847 | 19 | 0.785 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 145,314 | 1.453 | 20 | 20 | fits | 149,084 | 201 | 0.475 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 772,845 | 7.728 | 20 | 20 | fits | 145,657 | 107 | 0.491 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 148,899 | 1.489 | 20 | 24 | fits | 149,084 | 201 | 0.475 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 814,025 | 8.140 | 20 | 24 | fits | 37,745 | 30 | 0.515 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 147,859 | 1.479 | 20 | 50 | fits | 149,084 | 201 | 0.475 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 630,168 | 6.302 | 20 | 50 | fits | 145,642 | 170 | 0.482 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 282,990 | 2.830 | 20 | 20 | fits | 135,586 | 95 | 0.584 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 482,446 | 4.824 | 20 | 20 | fits | 77,675 | 36 | 0.485 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,239,187 | 62.392 | 20 | 20 | MISS ceiling | 13,055 | 12 | 0.641 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,021,746 | 360.217 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,021,671 | 360.217 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,021,596 | 360.216 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,021,521 | 360.215 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 154,215 | 1.542 | 20 | 200 | fits | 155,502 | 177 | 0.484 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 291,103 | 2.911 | 20 | 200 | fits | 137,497 | 189 | 0.452 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 149,956 | 1.500 | 20 | 20 | fits | 155,502 | 177 | 0.484 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 286,628 | 2.866 | 20 | 20 | fits | 137,497 | 189 | 0.452 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 153,541 | 1.535 | 20 | 24 | fits | 155,502 | 177 | 0.484 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,171,824 | 61.718 | 20 | 24 | MISS ceiling | 147,828 | 124 | 0.350 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 152,501 | 1.525 | 20 | 50 | fits | 155,502 | 177 | 0.484 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 289,608 | 2.896 | 20 | 50 | fits | 137,497 | 189 | 0.452 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 424,446 | 4.244 | 20 | 20 | fits | 134,903 | 96 | 0.567 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 618,451 | 6.185 | 20 | 20 | fits | 85,307 | 44 | 0.559 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `acmp.entity_departing.if0` | 6,634 | 0.066 | 20 | 20 | fits | 19,276 | 13 (29) | 0.778 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | `acmp.entity_available.if0` | 7,459 | 0.075 | 20 | 20 | fits | 20,982 | 19 (35) | 0.770 |
| TMR_NO_ADP (H-DISC) | `acmp.tmr_no_adp.if0` | 12,878 | 0.129 | 20 | 20 | fits | 27,077 | 21 (12) | 0.821 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,834 | 0.118 | 20 | 50 | fits | 22,416 | 43 | 0.706 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 9,370 | 0.094 | 20 | 50 | fits | 18,607 | 35 | 0.657 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 13,377 | 0.134 | 20 | 50 | fits | 18,650 | 35 | 0.661 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 14,680 | 0.147 | 20 | 50 | fits | 24,797 | 61 | 0.601 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 16,675 | 0.167 | 20 | 50 | fits | 24,797 | 61 | 0.601 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 10,513 | 0.105 | 20 | 50 | fits | 18,050 | 30 | 0.602 |
| LINK_UP | `adp.link_up.if0` | 2,517 | 0.025 | 20 | 200 | fits | 22,416 | 43 (11) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,075 | 0.131 | 20 | 200 | fits | 20,127 | 23 (39) | 0.721 |
| LINK_DOWN | `adp.link_down.if0` | 2,153 | 0.022 | 20 | 200 | fits | 20,598 | 23 (9) | 0.719 |
| LINK_UP | `adp.link_up.if0` | 2,517 | 0.025 | 20 | 200 | fits | 22,416 | 43 (11) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,075 | 0.131 | 20 | 200 | fits | 20,127 | 23 (39) | 0.721 |
| GM_CHANGE | `adp.gm_change.if0` | 2,262 | 0.023 | 20 | 200 | fits | 11,248 | 17 (11) | 0.627 |
| LINK_UP | `adp.link_up.if0` | 2,517 | 0.025 | 20 | 200 | fits | 22,416 | 43 (11) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,075 | 0.131 | 20 | 200 | fits | 20,127 | 23 (39) | 0.721 |
| RCV_ADP_DISCOVER | `adp.discover.if0` | 4,782 | 0.048 | 20 | 200 | fits | 11,507 | 16 (31) | 0.561 |
| LINK_UP | `adp.link_up.if0` | 2,517 | 0.025 | 20 | 200 | fits | 22,416 | 43 (11) | 0.706 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 13,075 | 0.131 | 20 | 200 | fits | 20,127 | 23 (39) | 0.721 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,782 | 0.048 | 20 | 200 | fits | 11,507 | 16 (31) | 0.561 |
| set_name | `aecp_fanout.set_name.if0` | 46,210 | 0.462 | 20 | 24 | fits | 53,378 | 88 | 0.515 |
| set_clock_source | `aecp_fanout.set_clock_source.if0` | 46,618 | 0.466 | 20 | 24 | fits | 47,309 | 77 | 0.543 |
| set_control_identify_on | `aecp_fanout.set_control_identify_on.if0` | 39,003 | 0.390 | 20 | 24 | fits | 42,822 | 78 | 0.490 |
| set_control_identify_off | `aecp_fanout.set_control_identify_off.if0` | 44,112 | 0.441 | 20 | 24 | fits | 43,174 | 77 | 0.497 |
| remove_audio_mappings | `aecp_fanout.remove_audio_mappings.if0` | 42,627 | 0.426 | 20 | 24 | fits | 47,937 | 66 | 0.559 |
| add_audio_mappings | `aecp_fanout.add_audio_mappings.if0` | 41,862 | 0.419 | 20 | 24 | fits | 47,010 | 65 | 0.558 |
| set_sampling_rate | `aecp_fanout.set_sampling_rate.if0` | 43,086 | 0.431 | 20 | 24 | fits | 45,467 | 66 | 0.545 |
| lock_entity | `aecp_fanout.lock_entity.if0` | 39,567 | 0.396 | 20 | 24 | fits | 43,240 | 77 | 0.495 |
| unlock_entity | `aecp_fanout.unlock_entity.if0` | 45,920 | 0.459 | 20 | 24 | fits | 43,632 | 78 | 0.511 |
| BIND_RX | `acmp.bind_rx.if0` | 23,171 | 0.232 | 20 | 20 | fits | 39,898 | 26 (77) | 0.780 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 8,307 | 0.083 | 20 | 20 | fits | 24,920 | 19 (32) | 0.823 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 12,048 | 0.120 | 20 | 20 | fits | 22,487 | 15 (47) | 0.745 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 15,052 | 0.151 | 20 | 20 | fits | 33,559 | 18 (50) | 0.809 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 12,109 | 0.121 | 20 | 20 | fits | 22,333 | 18 (48) | 0.707 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 12,176 | 0.122 | 20 | 20 | fits | 22,059 | 16 (48) | 0.716 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 11,930 | 0.119 | 20 | 20 | fits | 20,730 | 16 (48) | 0.681 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 10,801 | 0.108 | 20 | 20 | fits | 20,875 | 16 (48) | 0.686 |
| register_unsolicited | `aecp.register_unsolicited.if0` | 17,343 | 0.173 | 20 | 24 | fits | 22,368 | 20 | 0.753 |
| READ_DESCRIPTOR (312 B) | `aecp.read_descriptor.t0.i0.c0.if0` | 21,043 | 0.210 | 20 | 24 | fits | 26,931 | 20 | 0.674 |
| READ_DESCRIPTOR (106 B) | `aecp.read_descriptor.t1.i0.c0.if0` | 11,189 | 0.112 | 20 | 24 | fits | 22,019 | 20 | 0.689 |
| READ_DESCRIPTOR (148 B) | `aecp.read_descriptor.t2.i0.c0.if0` | 15,653 | 0.157 | 20 | 24 | fits | 21,904 | 20 | 0.685 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t5.i1.c0.if0` | 11,174 | 0.112 | 20 | 24 | fits | 22,315 | 20 | 0.685 |
| READ_DESCRIPTOR (146 B) | `aecp.read_descriptor.t6.i1.c0.if0` | 16,850 | 0.169 | 20 | 24 | fits | 22,796 | 20 | 0.697 |
| READ_DESCRIPTOR (102 B) | `aecp.read_descriptor.t9.i0.c0.if0` | 15,856 | 0.159 | 20 | 24 | fits | 21,851 | 20 | 0.691 |
| READ_DESCRIPTOR (86 B) | `aecp.read_descriptor.t10.i2.c0.if0` | 11,005 | 0.110 | 20 | 24 | fits | 21,756 | 20 | 0.703 |
| READ_DESCRIPTOR (72 B) | `aecp.read_descriptor.t12.i0.c0.if0` | 15,530 | 0.155 | 20 | 24 | fits | 21,461 | 20 | 0.708 |
| READ_DESCRIPTOR (452 B) | `aecp.read_descriptor.t13.i0.c0.if0` | 12,534 | 0.125 | 20 | 24 | fits | 23,496 | 21 | 0.590 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t14.i0.c0.if0` | 14,866 | 0.149 | 20 | 24 | fits | 20,789 | 20 | 0.723 |
| READ_DESCRIPTOR (20 B) | `aecp.read_descriptor.t15.i0.c0.if0` | 10,436 | 0.104 | 20 | 24 | fits | 20,541 | 20 | 0.711 |
| READ_DESCRIPTOR (90 B) | `aecp.read_descriptor.t20.i24.c0.if0` | 15,189 | 0.152 | 20 | 24 | fits | 21,596 | 20 | 0.692 |
| READ_DESCRIPTOR (113 B) | `aecp.read_descriptor.t26.i0.c0.if0` | 11,370 | 0.114 | 20 | 24 | fits | 21,929 | 20 | 0.689 |
| READ_DESCRIPTOR (82 B) | `aecp.read_descriptor.t36.i0.c0.if0` | 15,252 | 0.153 | 20 | 24 | fits | 22,202 | 20 | 0.715 |
| get_configuration | `aecp.get_configuration.if0` | 11,827 | 0.118 | 20 | 24 | fits | 18,975 | 20 | 0.694 |
| entity_available | `aecp.entity_available.if0` | 9,177 | 0.092 | 20 | 24 | fits | 18,586 | 20 | 0.669 |
| get_name | `aecp.get_name.if0` | 15,949 | 0.159 | 20 | 24 | fits | 22,987 | 20 | 0.744 |
| get_counters, refused ENTITY_MISBEHAVING | `aecp.get_counters.if0` | 12,428 | 0.124 | 20 | 24 | fits | 22,813 | 25 | 0.689 |
| get_avb_info, refused ENTITY_MISBEHAVING | `aecp.get_avb_info.if0` | 17,259 | 0.173 | 20 | 24 | fits | 23,681 | 27 | 0.742 |
| unknown_command, refused NOT_IMPLEMENTED | `aecp.unknown_command.if0` | 9,293 | 0.093 | 20 | 24 | fits | 19,808 | 20 | 0.729 |
| MVU GET_MILAN_INFO | `aecp.mvu_get_milan_info.if0` | 14,002 | 0.140 | 20 | 24 | fits | 19,040 | 20 | 0.693 |
| set_name | `aecp.set_name.if0` | 22,762 | 0.228 | 20 | 24 | fits | 35,983 | 42 | 0.716 |
| lock_entity | `aecp.lock_entity.if0` | 24,407 | 0.244 | 20 | 24 | fits | 28,703 | 33 | 0.743 |
| unlock_entity | `aecp.unlock_entity.if0` | 25,042 | 0.250 | 20 | 24 | fits | 28,278 | 32 | 0.755 |
| LINK_UP | `fixture.link_up.if0` | 2,517 | 0.025 | 20 | 200 | fits | 22,416 | 43 (11) | 0.706 |
| malformed MRPDU discard | `fixture.malformed.if0` | 15,274 | 0.153 | 20 | 20 | fits | 15,339 | 12 | 0.716 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 27,470 | 0.275 | 20 | 24 | fits | 36,784 | 42 | 0.720 |
| LINK_DOWN | `fixture.link_down.if0` | 2,458 | 0.025 | 20 | 200 | fits | 22,347 | 23 (9) | 0.745 |
| BIND_RX | `fixture.bind_rx.if0` | 22,975 | 0.230 | 20 | 20 | fits | 39,993 | 26 (77) | 0.780 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 19,243 | 0.192 | 20 | 20 | fits | 35,938 | 35 (35) | 0.779 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 9,103 | 0.091 | 20 | 20 | fits | 20,081 | 13 (29) | 0.790 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 76,035 | 0.760 | 20 | 200 | fits | 76,138 | 51 | 0.749 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 76,035 | 0.760 | 20 | 200 | fits | 76,138 | 51 | 0.749 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 75,765 | 0.758 | 20 | 20 | fits | 76,138 | 51 | 0.749 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 75,765 | 0.758 | 20 | 20 | fits | 76,138 | 51 | 0.749 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 75,970 | 0.760 | 20 | 24 | fits | 76,138 | 51 | 0.749 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 75,970 | 0.760 | 20 | 24 | fits | 76,138 | 51 | 0.749 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 75,905 | 0.759 | 20 | 50 | fits | 76,138 | 51 | 0.749 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 75,905 | 0.759 | 20 | 50 | fits | 76,138 | 51 | 0.749 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 75,840 | 0.758 | 20 | 20 | fits | 76,138 | 51 | 0.749 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 75,840 | 0.758 | 20 | 20 | fits | 76,138 | 51 | 0.749 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
