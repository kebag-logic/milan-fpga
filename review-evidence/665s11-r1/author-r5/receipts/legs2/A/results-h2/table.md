### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

4 of 52 paths and 7 of 478 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| BIND_RX | 0 | `fixture.bind_rx.if0` (fixture) | 0.188 (0.395) | fits | 0 acmp | 2 | 0 |
| DISCONNECT_TX | 0 | `acmp.disconnect_tx.if0` (acmp-cmd) | 0.095 (0.227) | fits | 0 acmp | 1 | 0 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | `fixture.entity_departing.if0` (fixture) | 0.062 (0.236) | fits | 0 adp | 1 | 0 |
| GET_RX_STATE | 0 | `acmp.get_rx_state.if0` (acmp-cmd) | 0.103 (0.235) | fits | 0 acmp | 1 | 0 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | 0 | `acmp.get_tx_connection.if0` (acmp-cmd) | 0.088 (0.227) | fits | 0 acmp | 1 | 0 |
| GET_TX_STATE | 0 | `acmp.get_tx_state.if0` (acmp-cmd) | 0.098 (0.230) | fits | 0 acmp | 1 | 0 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | 0 | `acmp.probe_tx.if0` (acmp-cmd) | 0.101 (0.245) | fits | 0 acmp | 1 | 0 |
| PROBE_TX_RESPONSE | 0 | `acmp.probe_tx_response.if0` (acmp-cmd) | 0.092 (0.303) | fits | 0 acmp | 1 | 0 |
| TMR_DELAY | 0 | `acmp.tmr_delay.if0` (acmp-noresp) | 0.231 (0.565) | fits | 0 events | 1 | 0 |
| TMR_DELAY, or the first TMR_NO_RESP | 0 | `acmp.tmr_no_resp1.if0` (acmp-noresp) | 0.178 (0.512) | fits | 0 events | 2 | 0 |
| the second TMR_NO_RESP | 0 | `acmp.tmr_no_resp2.if0` (acmp-noresp) | 0.071 (0.410) | fits | 0 events | 1 | 0 |
| TMR_RETRY | 0 | `acmp.tmr_retry.if0` (acmp-noresp) | 0.142 (0.468) | fits | 0 events | 1 | 0 |
| UNBIND_RX | 0 | `acmp.unbind_rx.if0` (acmp-cmd) | 0.132 (0.379) | fits | 0 acmp | 1 | 0 |
| RCV_ADP_DISCOVER (control) | 0 | `control.discover.if0` (control) | 0.046 (0.162) | fits | 0 adp | 1 | 0 |
| GM_CHANGE | 0 | `adp.gm_change.if0` (adp-gm) | 0.024 (0.158) | fits | 0 events | 1 | 0 |
| LINK_DOWN | 0 | `fixture.link_down.if0` (fixture) | 0.027 (0.269) | fits | 0 events | 1 | 0 |
| LINK_UP | 0 | `adp.link_up.if0` (adp-gm) | 0.026 (0.263) | fits | 0 events | 3 | 0 |
| TMR_DELAY expiry | 0 | `adp.tmr_delay.if0` (adp-gm) | 0.174 (0.470) | fits | 0 events | 2 | 0 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.add_audio_mappings.if0` (aecp-largest-notice) | 1.663 (1.958) | fits | 0 aecp | 1 | 0 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_indices.if0` (aecp-largest-notice) | 1.351 (1.694) | fits | 0 aecp | 1 | 0 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.collision_values.if0` (aecp-largest-notice) | 2.972 (3.307) | fits | 0 aecp | 1 | 0 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | 0 | `aecp_long.refused.conflict_last.if0` (aecp-largest-notice) | 2.419 (2.753) | fits | 0 aecp | 1 | 0 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | 0 | `aecp_long.remove_audio_mappings.if0` (aecp-largest-notice) | 1.371 (1.684) | fits | 0 aecp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog-adp@blank-aged2-7.adp_available.if0` (backlog-adp@blank-aged2-7) | 4.565 (5.246) | fits | 7 adp | 37 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 62.971 (63.145) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | 63.692 (63.867) | MISS ceiling | 11 acmp | 4 | 4 |
| SET_NAME fan-out to one registered controller | 0 | `fixture.set_name.if0` (fixture) | 0.336 (0.479) | fits | 0 aecp | 1 | 0 |
| ACMP record, every channel at its refill rate, the longest | 0 | `save-held.held.acmp.if0` (save-held) | 2.247 | fits | 11 acmp | 1 | 0 |
| ADP record, every channel at its refill rate, the longest | 0 | `save-held.held.adp.if0` (save-held) | 1.504 | fits | 7 adp | 1 | 0 |
| AECP record, every channel at its refill rate, the longest | 0 | `save-held.held.aecp.if0` (save-held) | 2.828 | fits | 15 aecp | 1 | 0 |
| MAAP record, every channel at its refill rate, the longest | 0 | `save-held.held.maap.if0` (save-held) | 1.583 | fits | 6 maap | 1 | 0 |
| SRP record, every channel at its refill rate, the longest | 0 | `save-held.held.srp.if0` (save-held) | 8.543 | fits | 31 srp | 1 | 0 |
| ANNOUNCE (TMR expiry) | 0 | `maap.announce.if0` (maap) | 0.148 (0.454) | fits | 0 events | 1 | 0 |
| conflicting PROBE -> DEFEND | 0 | `maap.defend.if0` (maap) | 0.090 (0.206) | fits | 0 maap | 1 | 0 |
| first PROBE (LINK_UP) | 0 | `maap.probe1.if0` (maap) | 0.111 (0.263) | fits | 0 events | 1 | 0 |
| last PROBE retransmission (TMR expiry) | 0 | `maap.probe4.if0` (maap) | 0.120 (0.454) | fits | 0 events | 1 | 0 |
| PROBE retransmission (TMR expiry) | 0 | `maap.probe3.if0` (maap) | 0.124 (0.414) | fits | 0 events | 2 | 0 |
| an MRPDU its periodic timer owes, the longest | 0 | `save-held.mrpdu.periodic.if0` (save-held) | 2.507 | fits | 0 srp | 1 | 0 |
| ACMP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.acmp.first.if0` (backlog-adp@verify-5) | 3.047 | fits | 0 acmp | 39 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-owed.service.acmp.last.if0` (backlog-owed) | 62.093 | MISS ceiling | 11 acmp | 39 | 1 |
| ADP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.adp.first.if0` (backlog-adp@verify-5) | 3.038 | fits | 0 adp | 39 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.adp.last.if0` (backlog-adp@blank-aged2-7) | 5.150 | fits | 7 adp | 39 | 0 |
| AECP record released under the composed load, first | 0 | `backlog-adp@blank-7.service.aecp.first.if0` (backlog-adp@blank-7) | 1.560 | fits | 0 aecp | 39 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 61.847 | MISS ceiling | 15 aecp | 39 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog-adp@verify-5.service.maap.first.if0` (backlog-adp@verify-5) | 3.073 | fits | 0 maap | 39 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp@blank-aged2-7.service.maap.last.if0` (backlog-adp@blank-aged2-7) | 5.187 | fits | 6 maap | 39 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp@blank-aged2-7.service.srp.first.if0` (backlog-adp@blank-aged2-7) | 6.098 | fits | 0 srp | 39 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp@program-aged2-7.service.srp.last.if0` (backlog-adp@program-aged2-7) | 10.145 | fits | 31 srp | 39 | 0 |
| Domain RX -> declarations (JoinTime wait) | 0 | `srp.domain.if0` (srp) | 0.993 (1.104) | fits | 0 srp | 1 | 0 |
| Listener Ready RX (registrar) | 0 | `srp.listener_ready.if0` (srp) | 0.443 (0.444) | fits | 0 srp | 1 | 0 |
| malformed MRPDU discard | 0 | `fixture.malformed.if0` (fixture) | 0.215 (0.215) | fits | 0 srp | 2 | 0 |
| startup declarations (LINK_UP) | 0 | `srp.startup.if0` (srp) | 0.888 (0.964) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog-adp@blank-1 | 0 | 10.523 | 10 | 145,236 (1.452) | yes | - |
| backlog-adp@blank-3 | 0 | 10.545 | 10 | 144,592 (1.446) | yes | - |
| backlog-adp@blank-5 | 0 | 10.836 | 12 | 145,906 (1.459) | yes | - |
| backlog-adp@blank-7 | 0 | 10.573 | 10 | 146,840 (1.468) | yes | - |
| backlog-adp@program-1 | 0 | 11.095 | 12 | 144,699 (1.447) | yes | - |
| backlog-adp@program-3 | 0 | 10.571 | 10 | 147,017 (1.470) | yes | - |
| backlog-adp@program-5 | 0 | 10.173 | 12 | 146,078 (1.461) | yes | - |
| backlog-adp@program-7 | 0 | 9.795 | 10 | 145,461 (1.455) | yes | - |
| backlog-adp@verify-1 | 0 | 10.463 | 10 | 144,209 (1.442) | yes | - |
| backlog-adp@verify-3 | 0 | 10.488 | 10 | 144,574 (1.446) | yes | - |
| backlog-adp@verify-5 | 0 | 10.801 | 12 | 146,552 (1.466) | yes | - |
| backlog-adp@verify-7 | 0 | 10.526 | 10 | 145,604 (1.456) | yes | - |
| backlog-adp@blank-aged2-1 | 0 | 10.934 | 12 | 144,676 (1.447) | yes | - |
| backlog-adp@blank-aged2-3 | 0 | 10.444 | 10 | 144,340 (1.443) | yes | - |
| backlog-adp@blank-aged2-5 | 0 | 10.496 | 10 | 145,001 (1.450) | yes | - |
| backlog-adp@blank-aged2-7 | 0 | 10.546 | 10 | 144,279 (1.443) | yes | - |
| backlog-adp@blank-aged1-1 | 0 | 11.285 | 11 | 145,893 (1.459) | yes | - |
| backlog-adp@blank-aged1-3 | 0 | 11.752 | 14 | 145,365 (1.454) | yes | - |
| backlog-adp@blank-aged1-5 | 0 | 11.362 | 12 | 143,633 (1.436) | yes | - |
| backlog-adp@blank-aged1-7 | 1 | 12.373 | 11 | 145,655 (1.457) | yes | - |
| backlog-adp@program-aged2-1 | 0 | 10.764 | 12 | 145,993 (1.460) | yes | - |
| backlog-adp@program-aged2-3 | 0 | 10.553 | 10 | 145,179 (1.452) | yes | - |
| backlog-adp@program-aged2-5 | 1 | 10.447 | 9 | 146,539 (1.465) | yes | - |
| backlog-adp@program-aged2-7 | 0 | 10.647 | 11 | 144,042 (1.440) | yes | - |
| backlog-adp@program-aged1-1 | 0 | 10.985 | 12 | 144,768 (1.448) | yes | - |
| backlog-adp@program-aged1-3 | 0 | 10.490 | 9 | 145,911 (1.459) | yes | - |
| backlog-adp@program-aged1-5 | 0 | 10.524 | 10 | 145,243 (1.452) | yes | - |
| backlog-adp@program-aged1-7 | 0 | 10.571 | 10 | 144,236 (1.442) | yes | - |
| backlog-adp@verify-aged2-1 | 0 | 10.302 | 9 | 145,939 (1.459) | yes | - |
| backlog-adp@verify-aged2-3 | 0 | 10.467 | 10 | 145,223 (1.452) | yes | - |
| backlog-adp@verify-aged2-5 | 0 | 10.627 | 11 | 145,984 (1.460) | yes | - |
| backlog-adp@verify-aged2-7 | 0 | 10.448 | 9 | 145,875 (1.459) | yes | - |
| backlog-adp@verify-aged1-1 | 0 | 10.702 | 12 | 146,423 (1.464) | yes | - |
| backlog-adp@verify-aged1-3 | 0 | 10.503 | 10 | 145,159 (1.452) | yes | - |
| backlog-adp@verify-aged1-5 | 0 | 10.395 | 9 | 145,132 (1.451) | yes | - |
| backlog-adp@verify-aged1-7 | 0 | 10.619 | 11 | 144,050 (1.440) | yes | - |
| backlog-adp | 0 | 9.698 | 10 | 144,750 (1.448) | yes | - |
| backlog-owed | 0 | 64.301 | 24 | 144,378 (1.444) | yes | - |
| fixture | 0 | 1.287 | 2 | 82,878 (0.829) | yes | - |

Composed maximum over 2 of 4 backlog windows, a partial figure (backlog, backlog-adp-refill not run): 144,750 CPU cycles (1.448 ms), backlog-adp.
Over the windows that released their whole load only: 144,750 (1.448 ms), backlog-adp.

Per-pass share (share.py): 20 ms over 10 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| save-second | 50875 | 0 | 50,937 (0.509) | fits |
| backlog-adp@blank-1 | 405 | 0 | 145,236 (1.452) | fits |
| backlog-adp@blank-3 | 405 | 0 | 144,592 (1.446) | fits |
| backlog-adp@blank-5 | 407 | 0 | 145,906 (1.459) | fits |
| backlog-adp@blank-7 | 407 | 0 | 146,840 (1.468) | fits |
| backlog-adp@program-1 | 503 | 0 | 144,699 (1.447) | fits |
| backlog-adp@program-3 | 503 | 0 | 147,017 (1.470) | fits |
| backlog-adp@program-5 | 506 | 0 | 146,078 (1.461) | fits |
| backlog-adp@program-7 | 506 | 0 | 145,461 (1.455) | fits |
| backlog-adp@verify-1 | 589 | 0 | 144,209 (1.442) | fits |
| backlog-adp@verify-3 | 589 | 0 | 144,574 (1.446) | fits |
| backlog-adp@verify-5 | 591 | 0 | 146,552 (1.466) | fits |
| backlog-adp@verify-7 | 591 | 0 | 145,604 (1.456) | fits |
| backlog-adp@blank-aged2-1 | 735 | 0 | 144,676 (1.447) | fits |
| backlog-adp@blank-aged2-3 | 749 | 0 | 144,340 (1.443) | fits |
| backlog-adp@blank-aged2-5 | 766 | 0 | 145,001 (1.450) | fits |
| backlog-adp@blank-aged2-7 | 783 | 0 | 144,279 (1.443) | fits |
| backlog-adp@blank-aged1-1 | 672 | 0 | 145,893 (1.459) | fits |
| backlog-adp@blank-aged1-3 | 691 | 0 | 145,365 (1.454) | fits |
| backlog-adp@blank-aged1-5 | 706 | 0 | 143,633 (1.436) | fits |
| backlog-adp@blank-aged1-7 | 722 | 0 | 145,655 (1.457) | fits |
| backlog-adp@program-aged2-1 | 830 | 0 | 145,993 (1.460) | fits |
| backlog-adp@program-aged2-3 | 845 | 0 | 145,179 (1.452) | fits |
| backlog-adp@program-aged2-5 | 861 | 0 | 146,539 (1.465) | fits |
| backlog-adp@program-aged2-7 | 879 | 0 | 144,042 (1.440) | fits |
| backlog-adp@program-aged1-1 | 764 | 0 | 144,768 (1.448) | fits |
| backlog-adp@program-aged1-3 | 778 | 0 | 145,911 (1.459) | fits |
| backlog-adp@program-aged1-5 | 795 | 0 | 145,243 (1.452) | fits |
| backlog-adp@program-aged1-7 | 812 | 0 | 144,236 (1.442) | fits |
| backlog-adp@verify-aged2-1 | 916 | 0 | 145,939 (1.459) | fits |
| backlog-adp@verify-aged2-3 | 933 | 0 | 145,223 (1.452) | fits |
| backlog-adp@verify-aged2-5 | 951 | 0 | 145,984 (1.460) | fits |
| backlog-adp@verify-aged2-7 | 966 | 0 | 145,875 (1.459) | fits |
| backlog-adp@verify-aged1-1 | 852 | 0 | 146,423 (1.464) | fits |
| backlog-adp@verify-aged1-3 | 867 | 0 | 145,159 (1.452) | fits |
| backlog-adp@verify-aged1-5 | 883 | 0 | 145,132 (1.451) | fits |
| backlog-adp@verify-aged1-7 | 901 | 0 | 144,050 (1.440) | fits |
| save-held | 1406 | 0 | 151,675 (1.517) | fits |
| acmp-noresp | 2027 | 0 | 41,923 (0.419) | fits |
| srp | 290 | 0 | 69,567 (0.696) | fits |
| backlog-adp | 312 | 0 | 144,750 (1.448) | fits |
| backlog-owed | 310 | 0 | 144,378 (1.444) | fits |
| maap | 176 | 0 | 41,923 (0.419) | fits |
| adp-gm | 89 | 0 | 41,923 (0.419) | fits |
| control | 89 | 0 | 41,923 (0.419) | fits |
| acmp-cmd | 87 | 0 | 41,923 (0.419) | fits |
| aecp-largest-notice | 107 | 0 | 143,728 (1.437) | fits |
| fixture | 161 | 0 | 82,878 (0.829) | fits |

Aged windows, opened with THE STEP's age at its limit or one short of it (save_window.aged_window): the aged steps among the window's records and after them (start after the window opened, CPU time, the step) and the window's tightest row:

| Group | Age at opening | Aged steps among its records | After them | Tightest row | ms (budget) | Margin ms |
|---|---:|---|---|---|---:|---:|
| backlog-adp@blank-aged2-1 | 2 | none | +9.302 ms, 76,679 (0.767 ms), read-back | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 9.264 (20) | 10.736 |
| backlog-adp@blank-aged2-3 | 2 | +6.705 ms, 76,679 (0.767 ms), read-back | none | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 9.953 (20) | 10.047 |
| backlog-adp@blank-aged2-5 | 2 | +5.032 ms, 76,805 (0.768 ms), read-back | none | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 10.005 (20) | 9.995 |
| backlog-adp@blank-aged2-7 | 2 | none | none | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 10.044 (20) | 9.956 |
| backlog-adp@blank-aged1-1 | 1 | none | none | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 9.269 (20) | 10.731 |
| backlog-adp@blank-aged1-3 | 1 | none | none | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 10.051 (20) | 9.949 |
| backlog-adp@blank-aged1-5 | 1 | none | none | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 10.109 (20) | 9.891 |
| backlog-adp@blank-aged1-7 | 1 | none | none | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 10.044 (20) | 9.956 |
| backlog-adp@program-aged2-1 | 2 | none | +9.191 ms, 80,479 (0.805 ms), issue | `backlog-adp@program-aged2-1.service.srp.last.if0` | 9.154 (20) | 10.846 |
| backlog-adp@program-aged2-3 | 2 | +6.933 ms, 80,379 (0.804 ms), issue | none | `backlog-adp@program-aged2-3.service.srp.last.if0` | 10.060 (20) | 9.940 |
| backlog-adp@program-aged2-5 | 2 | +5.101 ms, 80,627 (0.806 ms), issue | none | `backlog-adp@program-aged2-5.service.srp.last.if0` | 9.952 (20) | 10.048 |
| backlog-adp@program-aged2-7 | 2 | +2.991 ms, 79,782 (0.798 ms), issue | none | `backlog-adp@program-aged2-7.service.srp.last.if0` | 10.145 (20) | 9.855 |
| backlog-adp@program-aged1-1 | 1 | none | none | `backlog-adp@program-aged1-1.service.srp.last.if0` | 9.249 (20) | 10.751 |
| backlog-adp@program-aged1-3 | 1 | none | none | `backlog-adp@program-aged1-3.service.srp.last.if0` | 9.189 (20) | 10.811 |
| backlog-adp@program-aged1-5 | 1 | none | none | `backlog-adp@program-aged1-5.service.srp.last.if0` | 9.228 (20) | 10.772 |
| backlog-adp@program-aged1-7 | 1 | none | none | `backlog-adp@program-aged1-7.service.srp.last.if0` | 9.269 (20) | 10.731 |
| backlog-adp@verify-aged2-1 | 2 | none | +9.202 ms, 77,453 (0.775 ms), read-back | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 9.165 (20) | 10.835 |
| backlog-adp@verify-aged2-3 | 2 | +6.753 ms, 77,453 (0.775 ms), read-back | none | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 9.971 (20) | 10.029 |
| backlog-adp@verify-aged2-5 | 2 | +5.140 ms, 77,579 (0.776 ms), read-back | none | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 10.126 (20) | 9.874 |
| backlog-adp@verify-aged2-7 | 2 | +4.188 ms, 76,882 (0.769 ms), read-back | none | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 9.956 (20) | 10.044 |
| backlog-adp@verify-aged1-1 | 1 | none | none | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 9.145 (20) | 10.855 |
| backlog-adp@verify-aged1-3 | 1 | none | none | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 9.242 (20) | 10.758 |
| backlog-adp@verify-aged1-5 | 1 | none | none | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 9.131 (20) | 10.869 |
| backlog-adp@verify-aged1-7 | 1 | none | none | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 9.230 (20) | 10.770 |

Least margin over the aged windows: 9.855 ms, `backlog-adp@program-aged2-7.service.srp.last.if0` at 10.145 ms.

Saves, from the change to durable (save_window.bound_ms: the first-dirty window, or the rest of a save in flight, then each step at most CTRL_LOOP_STEP_AGE + 1 ticks after the one before):

| Group | Durable ms | Stated worst case ms | Steps | Save in flight, records | Longest gap between flash steps, ms | Grandmaster flood | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| save-second | 6030.390 | 6,070 | 102 | 2 | 30.857 | yes | within |
| save-held | 2018.324 | 4,070 | 102 | - | 15.438 | no | within |

Passes that carry the store's step (THE STEP), and the longest step's own CPU time, the store's and its flash port's:

| Group | Passes | Longest, CPU cycles (ms) | Longest step, CPU cycles (ms) |
|---|---:|---:|---:|
| save-second | 520 | 79,563 (0.796) | 77,498 (0.775) |
| backlog-adp@blank-1 | 299 | 91,368 (0.914) | 76,037 (0.760) |
| backlog-adp@blank-3 | 299 | 91,467 (0.915) | 76,037 (0.760) |
| backlog-adp@blank-5 | 299 | 91,498 (0.915) | 76,068 (0.761) |
| backlog-adp@blank-7 | 299 | 91,209 (0.912) | 75,967 (0.760) |
| backlog-adp@program-1 | 328 | 95,908 (0.959) | 78,591 (0.786) |
| backlog-adp@program-3 | 328 | 95,908 (0.959) | 78,569 (0.786) |
| backlog-adp@program-5 | 329 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@program-7 | 329 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-1 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-3 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-5 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-7 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@blank-aged2-1 | 297 | 76,679 (0.767) | 75,581 (0.756) |
| backlog-adp@blank-aged2-3 | 297 | 76,679 (0.767) | 75,581 (0.756) |
| backlog-adp@blank-aged2-5 | 297 | 76,805 (0.768) | 75,648 (0.756) |
| backlog-adp@blank-aged2-7 | 297 | 84,922 (0.849) | 75,549 (0.755) |
| backlog-adp@blank-aged1-1 | 297 | 97,470 (0.975) | 76,027 (0.760) |
| backlog-adp@blank-aged1-3 | 297 | 91,544 (0.915) | 75,924 (0.759) |
| backlog-adp@blank-aged1-5 | 297 | 91,231 (0.912) | 75,968 (0.760) |
| backlog-adp@blank-aged1-7 | 298 | 91,052 (0.911) | 75,991 (0.760) |
| backlog-adp@program-aged2-1 | 326 | 95,908 (0.959) | 78,310 (0.783) |
| backlog-adp@program-aged2-3 | 326 | 95,908 (0.959) | 78,310 (0.783) |
| backlog-adp@program-aged2-5 | 326 | 95,908 (0.959) | 78,377 (0.784) |
| backlog-adp@program-aged2-7 | 326 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@program-aged1-1 | 326 | 95,908 (0.959) | 78,591 (0.786) |
| backlog-adp@program-aged1-3 | 326 | 95,908 (0.959) | 78,635 (0.786) |
| backlog-adp@program-aged1-5 | 326 | 95,908 (0.959) | 78,635 (0.786) |
| backlog-adp@program-aged1-7 | 326 | 95,908 (0.959) | 78,592 (0.786) |
| backlog-adp@verify-aged2-1 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged2-3 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged2-5 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged2-7 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-1 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-3 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-5 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| backlog-adp@verify-aged1-7 | 355 | 95,908 (0.959) | 77,744 (0.777) |
| save-held | 722 | 94,236 (0.942) | 78,154 (0.782) |
| acmp-noresp | 615 | 95,877 (0.959) | 77,672 (0.777) |
| srp | 271 | 21,733 (0.217) | 1,982 (0.020) |
| backlog-adp | 271 | 21,733 (0.217) | 2,196 (0.022) |
| backlog-owed | 276 | 21,733 (0.217) | 2,259 (0.023) |
| maap | 163 | 21,733 (0.217) | 1,982 (0.020) |
| adp-gm | 80 | 21,733 (0.217) | 1,982 (0.020) |
| control | 80 | 21,733 (0.217) | 1,982 (0.020) |
| acmp-cmd | 65 | 21,733 (0.217) | 1,982 (0.020) |
| aecp-largest-notice | 78 | 21,733 (0.217) | 1,982 (0.020) |
| fixture | 54 | 16,279 (0.163) | 1,982 (0.020) |

Longest pass that carries a step: 97,470 CPU cycles (0.975 ms), backlog-adp@blank-aged1-1; longest step: 78,635 (0.786 ms), backlog-adp@program-aged1-3.

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-1.adp_available.if0` | 363,349 | 3.633 | 20 | 20 | fits | 123,514 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-1.service.adp.first.if0` | 291,310 | 2.913 | 20 | 200 | fits | 145,236 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@blank-1.service.adp.last.if0` | 414,208 | 4.142 | 20 | 200 | fits | 123,514 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-1.service.acmp.first.if0` | 292,234 | 2.922 | 20 | 20 | fits | 145,236 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@blank-1.service.acmp.last.if0` | 414,912 | 4.149 | 20 | 20 | fits | 123,514 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-1.service.aecp.first.if0` | 150,638 | 1.506 | 20 | 24 | fits | 143,900 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@blank-1.service.aecp.last.if0` | 294,884 | 2.949 | 20 | 24 | fits | 145,236 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@blank-1.service.maap.first.if0` | 294,818 | 2.948 | 20 | 50 | fits | 145,236 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@blank-1.service.maap.last.if0` | 417,936 | 4.179 | 20 | 50 | fits | 123,514 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-1.service.srp.first.if0` | 509,096 | 5.091 | 20 | 20 | fits | 91,226 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@blank-1.service.srp.last.if0` | 926,786 | 9.268 | 20 | 20 | fits | 59,596 | 26 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-3.adp_available.if0` | 360,099 | 3.601 | 20 | 20 | fits | 123,974 | 197 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@blank-3.service.adp.first.if0` | 295,220 | 2.952 | 20 | 200 | fits | 144,592 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-3.service.adp.last.if0` | 418,578 | 4.186 | 20 | 200 | fits | 123,974 | 197 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@blank-3.service.acmp.first.if0` | 296,144 | 2.961 | 20 | 20 | fits | 144,592 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-3.service.acmp.last.if0` | 419,282 | 4.193 | 20 | 20 | fits | 123,974 | 197 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@blank-3.service.aecp.first.if0` | 155,192 | 1.552 | 20 | 24 | fits | 143,896 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@blank-3.service.aecp.last.if0` | 298,794 | 2.988 | 20 | 24 | fits | 144,592 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-3.service.maap.first.if0` | 298,728 | 2.987 | 20 | 50 | fits | 144,592 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-3.service.maap.last.if0` | 422,306 | 4.223 | 20 | 50 | fits | 123,974 | 197 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@blank-3.service.srp.first.if0` | 515,879 | 5.159 | 20 | 20 | fits | 84,255 | 31 | 0.775 |
| SRP record released under the composed load, last | `backlog-adp@blank-3.service.srp.last.if0` | 928,890 | 9.289 | 20 | 20 | fits | 75,261 | 28 | 0.583 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-5.adp_available.if0` | 359,265 | 3.593 | 20 | 20 | fits | 123,716 | 196 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@blank-5.service.adp.first.if0` | 294,558 | 2.946 | 20 | 200 | fits | 145,906 | 208 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-5.service.adp.last.if0` | 417,658 | 4.177 | 20 | 200 | fits | 123,716 | 196 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@blank-5.service.acmp.first.if0` | 295,482 | 2.955 | 20 | 20 | fits | 145,906 | 208 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-5.service.acmp.last.if0` | 418,362 | 4.184 | 20 | 20 | fits | 123,716 | 196 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@blank-5.service.aecp.first.if0` | 145,026 | 1.450 | 20 | 24 | fits | 144,146 | 146 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-5.service.aecp.last.if0` | 298,132 | 2.981 | 20 | 24 | fits | 145,906 | 208 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-5.service.maap.first.if0` | 298,066 | 2.981 | 20 | 50 | fits | 145,906 | 208 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-5.service.maap.last.if0` | 421,386 | 4.214 | 20 | 50 | fits | 123,716 | 196 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@blank-5.service.srp.first.if0` | 507,437 | 5.074 | 20 | 20 | fits | 86,117 | 30 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@blank-5.service.srp.last.if0` | 913,844 | 9.138 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-7.adp_available.if0` | 375,549 | 3.755 | 20 | 20 | fits | 128,828 | 218 | 0.436 |
| ADP record released under the composed load, first | `backlog-adp@blank-7.service.adp.first.if0` | 298,228 | 2.982 | 20 | 200 | fits | 146,840 | 185 | 0.478 |
| ADP record released under the composed load, last | `backlog-adp@blank-7.service.adp.last.if0` | 426,440 | 4.264 | 20 | 200 | fits | 128,828 | 218 | 0.436 |
| ACMP record released under the composed load, first | `backlog-adp@blank-7.service.acmp.first.if0` | 299,152 | 2.992 | 20 | 20 | fits | 146,840 | 185 | 0.478 |
| ACMP record released under the composed load, last | `backlog-adp@blank-7.service.acmp.last.if0` | 427,144 | 4.271 | 20 | 20 | fits | 128,828 | 218 | 0.436 |
| AECP record released under the composed load, first | `backlog-adp@blank-7.service.aecp.first.if0` | 155,952 | 1.560 | 20 | 24 | fits | 144,010 | 145 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@blank-7.service.aecp.last.if0` | 301,802 | 3.018 | 20 | 24 | fits | 146,840 | 185 | 0.478 |
| MAAP record released under the composed load, first | `backlog-adp@blank-7.service.maap.first.if0` | 301,736 | 3.017 | 20 | 50 | fits | 146,840 | 185 | 0.478 |
| MAAP record released under the composed load, last | `backlog-adp@blank-7.service.maap.last.if0` | 430,168 | 4.302 | 20 | 50 | fits | 128,828 | 218 | 0.436 |
| SRP record released under the composed load, first | `backlog-adp@blank-7.service.srp.first.if0` | 521,237 | 5.212 | 20 | 20 | fits | 91,135 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@blank-7.service.srp.last.if0` | 931,938 | 9.319 | 20 | 20 | fits | 52,991 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-1.adp_available.if0` | 370,933 | 3.709 | 20 | 20 | fits | 127,747 | 203 | 0.471 |
| ADP record released under the composed load, first | `backlog-adp@program-1.service.adp.first.if0` | 292,909 | 2.929 | 20 | 200 | fits | 144,699 | 204 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@program-1.service.adp.last.if0` | 429,455 | 4.295 | 20 | 200 | fits | 127,747 | 203 | 0.471 |
| ACMP record released under the composed load, first | `backlog-adp@program-1.service.acmp.first.if0` | 293,833 | 2.938 | 20 | 20 | fits | 144,699 | 204 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@program-1.service.acmp.last.if0` | 430,159 | 4.302 | 20 | 20 | fits | 127,747 | 203 | 0.471 |
| AECP record released under the composed load, first | `backlog-adp@program-1.service.aecp.first.if0` | 152,774 | 1.528 | 20 | 24 | fits | 144,322 | 145 | 0.436 |
| AECP record released under the composed load, last | `backlog-adp@program-1.service.aecp.last.if0` | 296,483 | 2.965 | 20 | 24 | fits | 144,699 | 204 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@program-1.service.maap.first.if0` | 296,417 | 2.964 | 20 | 50 | fits | 144,699 | 204 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@program-1.service.maap.last.if0` | 433,183 | 4.332 | 20 | 50 | fits | 127,747 | 203 | 0.471 |
| SRP record released under the composed load, first | `backlog-adp@program-1.service.srp.first.if0` | 524,342 | 5.243 | 20 | 20 | fits | 91,225 | 28 | 0.736 |
| SRP record released under the composed load, last | `backlog-adp@program-1.service.srp.last.if0` | 926,240 | 9.262 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-3.adp_available.if0` | 370,358 | 3.704 | 20 | 20 | fits | 128,950 | 218 | 0.438 |
| ADP record released under the composed load, first | `backlog-adp@program-3.service.adp.first.if0` | 292,915 | 2.929 | 20 | 200 | fits | 147,017 | 185 | 0.479 |
| ADP record released under the composed load, last | `backlog-adp@program-3.service.adp.last.if0` | 421,249 | 4.212 | 20 | 200 | fits | 128,950 | 218 | 0.438 |
| ACMP record released under the composed load, first | `backlog-adp@program-3.service.acmp.first.if0` | 293,839 | 2.938 | 20 | 20 | fits | 147,017 | 185 | 0.479 |
| ACMP record released under the composed load, last | `backlog-adp@program-3.service.acmp.last.if0` | 421,953 | 4.220 | 20 | 20 | fits | 128,950 | 218 | 0.438 |
| AECP record released under the composed load, first | `backlog-adp@program-3.service.aecp.first.if0` | 150,462 | 1.505 | 20 | 24 | fits | 144,095 | 145 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@program-3.service.aecp.last.if0` | 296,489 | 2.965 | 20 | 24 | fits | 147,017 | 185 | 0.479 |
| MAAP record released under the composed load, first | `backlog-adp@program-3.service.maap.first.if0` | 296,423 | 2.964 | 20 | 50 | fits | 147,017 | 185 | 0.479 |
| MAAP record released under the composed load, last | `backlog-adp@program-3.service.maap.last.if0` | 424,977 | 4.250 | 20 | 50 | fits | 128,950 | 218 | 0.438 |
| SRP record released under the composed load, first | `backlog-adp@program-3.service.srp.first.if0` | 515,795 | 5.158 | 20 | 20 | fits | 90,884 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-3.service.srp.last.if0` | 926,943 | 9.269 | 20 | 20 | fits | 53,031 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-5.adp_available.if0` | 363,557 | 3.636 | 20 | 20 | fits | 123,661 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-5.service.adp.first.if0` | 298,889 | 2.989 | 20 | 200 | fits | 146,078 | 208 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-5.service.adp.last.if0` | 421,934 | 4.219 | 20 | 200 | fits | 123,661 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-5.service.acmp.first.if0` | 299,813 | 2.998 | 20 | 20 | fits | 146,078 | 208 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-5.service.acmp.last.if0` | 422,638 | 4.226 | 20 | 20 | fits | 123,661 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-5.service.aecp.first.if0` | 149,225 | 1.492 | 20 | 24 | fits | 144,127 | 146 | 0.432 |
| AECP record released under the composed load, last | `backlog-adp@program-5.service.aecp.last.if0` | 302,463 | 3.025 | 20 | 24 | fits | 146,078 | 208 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-5.service.maap.first.if0` | 302,397 | 3.024 | 20 | 50 | fits | 146,078 | 208 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-5.service.maap.last.if0` | 425,662 | 4.257 | 20 | 50 | fits | 123,661 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-5.service.srp.first.if0` | 516,289 | 5.163 | 20 | 20 | fits | 90,693 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-5.service.srp.last.if0` | 918,419 | 9.184 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-7.adp_available.if0` | 370,622 | 3.706 | 20 | 20 | fits | 130,700 | 222 | 0.437 |
| ADP record released under the composed load, first | `backlog-adp@program-7.service.adp.first.if0` | 290,819 | 2.908 | 20 | 200 | fits | 145,461 | 181 | 0.484 |
| ADP record released under the composed load, last | `backlog-adp@program-7.service.adp.last.if0` | 420,903 | 4.209 | 20 | 200 | fits | 130,700 | 222 | 0.437 |
| ACMP record released under the composed load, first | `backlog-adp@program-7.service.acmp.first.if0` | 291,743 | 2.917 | 20 | 20 | fits | 145,461 | 181 | 0.484 |
| ACMP record released under the composed load, last | `backlog-adp@program-7.service.acmp.last.if0` | 421,607 | 4.216 | 20 | 20 | fits | 130,700 | 222 | 0.437 |
| AECP record released under the composed load, first | `backlog-adp@program-7.service.aecp.first.if0` | 149,922 | 1.499 | 20 | 24 | fits | 144,173 | 145 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@program-7.service.aecp.last.if0` | 294,393 | 2.944 | 20 | 24 | fits | 145,461 | 181 | 0.484 |
| MAAP record released under the composed load, first | `backlog-adp@program-7.service.maap.first.if0` | 294,327 | 2.943 | 20 | 50 | fits | 145,461 | 181 | 0.484 |
| MAAP record released under the composed load, last | `backlog-adp@program-7.service.maap.last.if0` | 424,631 | 4.246 | 20 | 50 | fits | 130,700 | 222 | 0.437 |
| SRP record released under the composed load, first | `backlog-adp@program-7.service.srp.first.if0` | 517,814 | 5.178 | 20 | 20 | fits | 83,783 | 31 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@program-7.service.srp.last.if0` | 924,079 | 9.241 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-1.adp_available.if0` | 357,217 | 3.572 | 20 | 20 | fits | 124,209 | 199 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@verify-1.service.adp.first.if0` | 283,629 | 2.836 | 20 | 200 | fits | 143,753 | 199 | 0.464 |
| ADP record released under the composed load, last | `backlog-adp@verify-1.service.adp.last.if0` | 407,222 | 4.072 | 20 | 200 | fits | 124,209 | 199 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@verify-1.service.acmp.first.if0` | 284,553 | 2.846 | 20 | 20 | fits | 143,753 | 199 | 0.464 |
| ACMP record released under the composed load, last | `backlog-adp@verify-1.service.acmp.last.if0` | 407,926 | 4.079 | 20 | 20 | fits | 124,209 | 199 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@verify-1.service.aecp.first.if0` | 144,440 | 1.444 | 20 | 24 | fits | 144,209 | 145 | 0.434 |
| AECP record released under the composed load, last | `backlog-adp@verify-1.service.aecp.last.if0` | 287,203 | 2.872 | 20 | 24 | fits | 143,753 | 199 | 0.464 |
| MAAP record released under the composed load, first | `backlog-adp@verify-1.service.maap.first.if0` | 287,137 | 2.871 | 20 | 50 | fits | 143,753 | 199 | 0.464 |
| MAAP record released under the composed load, last | `backlog-adp@verify-1.service.maap.last.if0` | 410,950 | 4.109 | 20 | 50 | fits | 124,209 | 199 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@verify-1.service.srp.first.if0` | 501,840 | 5.018 | 20 | 20 | fits | 90,956 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-1.service.srp.last.if0` | 920,059 | 9.201 | 20 | 20 | fits | 70,658 | 30 | 0.661 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-3.adp_available.if0` | 353,714 | 3.537 | 20 | 20 | fits | 124,174 | 197 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-3.service.adp.first.if0` | 288,932 | 2.889 | 20 | 200 | fits | 144,574 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@verify-3.service.adp.last.if0` | 412,490 | 4.125 | 20 | 200 | fits | 124,174 | 197 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-3.service.acmp.first.if0` | 289,856 | 2.899 | 20 | 20 | fits | 144,574 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@verify-3.service.acmp.last.if0` | 413,194 | 4.132 | 20 | 20 | fits | 124,174 | 197 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-3.service.aecp.first.if0` | 148,922 | 1.489 | 20 | 24 | fits | 144,133 | 145 | 0.433 |
| AECP record released under the composed load, last | `backlog-adp@verify-3.service.aecp.last.if0` | 292,506 | 2.925 | 20 | 24 | fits | 144,574 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@verify-3.service.maap.first.if0` | 292,440 | 2.924 | 20 | 50 | fits | 144,574 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@verify-3.service.maap.last.if0` | 416,218 | 4.162 | 20 | 50 | fits | 124,174 | 197 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-3.service.srp.first.if0` | 509,260 | 5.093 | 20 | 20 | fits | 83,872 | 31 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@verify-3.service.srp.last.if0` | 922,477 | 9.225 | 20 | 20 | fits | 75,261 | 28 | 0.583 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-5.adp_available.if0` | 384,379 | 3.844 | 20 | 20 | fits | 132,229 | 202 | 0.473 |
| ADP record released under the composed load, first | `backlog-adp@verify-5.service.adp.first.if0` | 303,779 | 3.038 | 20 | 200 | fits | 146,552 | 208 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-5.service.adp.last.if0` | 435,392 | 4.354 | 20 | 200 | fits | 132,229 | 202 | 0.473 |
| ACMP record released under the composed load, first | `backlog-adp@verify-5.service.acmp.first.if0` | 304,703 | 3.047 | 20 | 20 | fits | 146,552 | 208 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-5.service.acmp.last.if0` | 436,096 | 4.361 | 20 | 20 | fits | 132,229 | 202 | 0.473 |
| AECP record released under the composed load, first | `backlog-adp@verify-5.service.aecp.first.if0` | 153,786 | 1.538 | 20 | 24 | fits | 144,439 | 146 | 0.435 |
| AECP record released under the composed load, last | `backlog-adp@verify-5.service.aecp.last.if0` | 307,353 | 3.074 | 20 | 24 | fits | 146,552 | 208 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-5.service.maap.first.if0` | 307,287 | 3.073 | 20 | 50 | fits | 146,552 | 208 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-5.service.maap.last.if0` | 439,120 | 4.391 | 20 | 50 | fits | 132,229 | 202 | 0.473 |
| SRP record released under the composed load, first | `backlog-adp@verify-5.service.srp.first.if0` | 529,971 | 5.300 | 20 | 20 | fits | 90,917 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-5.service.srp.last.if0` | 925,132 | 9.251 | 20 | 20 | fits | 53,294 | 21 | 0.668 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-7.adp_available.if0` | 370,558 | 3.706 | 20 | 20 | fits | 130,253 | 221 | 0.435 |
| ADP record released under the composed load, first | `backlog-adp@verify-7.service.adp.first.if0` | 290,920 | 2.909 | 20 | 200 | fits | 145,604 | 181 | 0.485 |
| ADP record released under the composed load, last | `backlog-adp@verify-7.service.adp.last.if0` | 420,557 | 4.206 | 20 | 200 | fits | 130,253 | 221 | 0.435 |
| ACMP record released under the composed load, first | `backlog-adp@verify-7.service.acmp.first.if0` | 291,844 | 2.918 | 20 | 20 | fits | 145,604 | 181 | 0.485 |
| ACMP record released under the composed load, last | `backlog-adp@verify-7.service.acmp.last.if0` | 421,261 | 4.213 | 20 | 20 | fits | 130,253 | 221 | 0.435 |
| AECP record released under the composed load, first | `backlog-adp@verify-7.service.aecp.first.if0` | 149,880 | 1.499 | 20 | 24 | fits | 144,019 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp@verify-7.service.aecp.last.if0` | 294,494 | 2.945 | 20 | 24 | fits | 145,604 | 181 | 0.485 |
| MAAP record released under the composed load, first | `backlog-adp@verify-7.service.maap.first.if0` | 294,428 | 2.944 | 20 | 50 | fits | 145,604 | 181 | 0.485 |
| MAAP record released under the composed load, last | `backlog-adp@verify-7.service.maap.last.if0` | 424,285 | 4.243 | 20 | 50 | fits | 130,253 | 221 | 0.435 |
| SRP record released under the composed load, first | `backlog-adp@verify-7.service.srp.first.if0` | 515,194 | 5.152 | 20 | 20 | fits | 90,975 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-adp@verify-7.service.srp.last.if0` | 926,352 | 9.264 | 20 | 20 | fits | 53,031 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-1.adp_available.if0` | 371,266 | 3.713 | 20 | 20 | fits | 127,517 | 203 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.adp.first.if0` | 293,311 | 2.933 | 20 | 200 | fits | 144,676 | 204 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.adp.last.if0` | 430,038 | 4.300 | 20 | 200 | fits | 127,517 | 203 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.acmp.first.if0` | 294,235 | 2.942 | 20 | 20 | fits | 144,676 | 204 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.acmp.last.if0` | 430,742 | 4.307 | 20 | 20 | fits | 127,517 | 203 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.aecp.first.if0` | 153,199 | 1.532 | 20 | 24 | fits | 143,713 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.aecp.last.if0` | 296,885 | 2.969 | 20 | 24 | fits | 144,676 | 204 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.maap.first.if0` | 296,819 | 2.968 | 20 | 50 | fits | 144,676 | 204 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.maap.last.if0` | 433,766 | 4.338 | 20 | 50 | fits | 127,517 | 203 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-1.service.srp.first.if0` | 524,847 | 5.248 | 20 | 20 | fits | 91,147 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-1.service.srp.last.if0` | 926,439 | 9.264 | 20 | 20 | fits | 59,983 | 26 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-3.adp_available.if0` | 348,476 | 3.485 | 20 | 20 | fits | 123,525 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.adp.first.if0` | 283,831 | 2.838 | 20 | 200 | fits | 144,340 | 203 | 0.455 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.adp.last.if0` | 406,740 | 4.067 | 20 | 200 | fits | 123,525 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.acmp.first.if0` | 284,755 | 2.848 | 20 | 20 | fits | 144,340 | 203 | 0.455 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.acmp.last.if0` | 407,444 | 4.074 | 20 | 20 | fits | 123,525 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.aecp.first.if0` | 144,055 | 1.441 | 20 | 24 | fits | 143,361 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.aecp.last.if0` | 287,405 | 2.874 | 20 | 24 | fits | 144,340 | 203 | 0.455 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.maap.first.if0` | 287,339 | 2.873 | 20 | 50 | fits | 144,340 | 203 | 0.455 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.maap.last.if0` | 410,468 | 4.105 | 20 | 50 | fits | 123,525 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-3.service.srp.first.if0` | 500,989 | 5.010 | 20 | 20 | fits | 90,587 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-3.service.srp.last.if0` | 995,270 | 9.953 | 20 | 20 | fits | 64,188 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-5.adp_available.if0` | 361,330 | 3.613 | 20 | 20 | fits | 123,233 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.adp.first.if0` | 289,444 | 2.894 | 20 | 200 | fits | 145,001 | 203 | 0.459 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.adp.last.if0` | 412,061 | 4.121 | 20 | 200 | fits | 123,233 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.acmp.first.if0` | 290,368 | 2.904 | 20 | 20 | fits | 145,001 | 203 | 0.459 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.acmp.last.if0` | 412,765 | 4.128 | 20 | 20 | fits | 123,233 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.aecp.first.if0` | 149,007 | 1.490 | 20 | 24 | fits | 143,313 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.aecp.last.if0` | 293,018 | 2.930 | 20 | 24 | fits | 145,001 | 203 | 0.459 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.maap.first.if0` | 292,952 | 2.930 | 20 | 50 | fits | 145,001 | 203 | 0.459 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.maap.last.if0` | 415,789 | 4.158 | 20 | 50 | fits | 123,233 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-5.service.srp.first.if0` | 501,523 | 5.015 | 20 | 20 | fits | 85,800 | 30 | 0.770 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-5.service.srp.last.if0` | 1,000,498 | 10.005 | 20 | 20 | fits | 75,189 | 28 | 0.583 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged2-7.adp_available.if0` | 456,485 | 4.565 | 20 | 20 | fits | 137,099 | 214 | 0.468 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.adp.first.if0` | 293,603 | 2.936 | 20 | 200 | fits | 144,279 | 198 | 0.473 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.adp.last.if0` | 515,008 | 5.150 | 20 | 200 | fits | 137,099 | 214 | 0.468 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.acmp.first.if0` | 294,527 | 2.945 | 20 | 20 | fits | 144,279 | 198 | 0.473 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.acmp.last.if0` | 515,712 | 5.157 | 20 | 20 | fits | 137,099 | 214 | 0.468 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.aecp.first.if0` | 153,888 | 1.539 | 20 | 24 | fits | 143,313 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.aecp.last.if0` | 297,177 | 2.972 | 20 | 24 | fits | 144,279 | 198 | 0.473 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.maap.first.if0` | 297,111 | 2.971 | 20 | 50 | fits | 144,279 | 198 | 0.473 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.maap.last.if0` | 518,736 | 5.187 | 20 | 50 | fits | 137,099 | 214 | 0.468 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged2-7.service.srp.first.if0` | 609,768 | 6.098 | 20 | 20 | fits | 91,098 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged2-7.service.srp.last.if0` | 1,004,403 | 10.044 | 20 | 20 | fits | 52,961 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-1.adp_available.if0` | 347,342 | 3.473 | 20 | 20 | fits | 123,804 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.adp.first.if0` | 282,633 | 2.826 | 20 | 200 | fits | 145,893 | 208 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.adp.last.if0` | 405,821 | 4.058 | 20 | 200 | fits | 123,804 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.acmp.first.if0` | 283,557 | 2.836 | 20 | 20 | fits | 145,893 | 208 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.acmp.last.if0` | 406,525 | 4.065 | 20 | 20 | fits | 123,804 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.aecp.first.if0` | 141,304 | 1.413 | 20 | 24 | fits | 143,253 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.aecp.last.if0` | 286,207 | 2.862 | 20 | 24 | fits | 145,893 | 208 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.maap.first.if0` | 286,141 | 2.861 | 20 | 50 | fits | 145,893 | 208 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.maap.last.if0` | 409,549 | 4.095 | 20 | 50 | fits | 123,804 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-1.service.srp.first.if0` | 493,575 | 4.936 | 20 | 20 | fits | 84,092 | 31 | 0.764 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-1.service.srp.last.if0` | 926,875 | 9.269 | 20 | 20 | fits | 79,948 | 30 | 0.693 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-3.adp_available.if0` | 372,207 | 3.722 | 20 | 20 | fits | 127,583 | 203 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.adp.first.if0` | 287,258 | 2.873 | 20 | 200 | fits | 145,365 | 204 | 0.461 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.adp.last.if0` | 423,484 | 4.235 | 20 | 200 | fits | 127,583 | 203 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.acmp.first.if0` | 288,182 | 2.882 | 20 | 20 | fits | 145,365 | 204 | 0.461 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.acmp.last.if0` | 424,188 | 4.242 | 20 | 20 | fits | 127,583 | 203 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.aecp.first.if0` | 146,457 | 1.465 | 20 | 24 | fits | 143,253 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.aecp.last.if0` | 290,832 | 2.908 | 20 | 24 | fits | 145,365 | 204 | 0.461 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.maap.first.if0` | 290,766 | 2.908 | 20 | 50 | fits | 145,365 | 204 | 0.461 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.maap.last.if0` | 427,212 | 4.272 | 20 | 50 | fits | 127,583 | 203 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-3.service.srp.first.if0` | 518,752 | 5.188 | 20 | 20 | fits | 91,606 | 28 | 0.740 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-3.service.srp.last.if0` | 1,005,079 | 10.051 | 20 | 20 | fits | 64,287 | 24 | 0.624 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-5.adp_available.if0` | 364,199 | 3.642 | 20 | 20 | fits | 123,983 | 199 | 0.440 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.adp.first.if0` | 290,725 | 2.907 | 20 | 200 | fits | 143,633 | 199 | 0.465 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.adp.last.if0` | 414,092 | 4.141 | 20 | 200 | fits | 123,983 | 199 | 0.440 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.acmp.first.if0` | 291,649 | 2.916 | 20 | 20 | fits | 143,633 | 199 | 0.465 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.acmp.last.if0` | 414,796 | 4.148 | 20 | 20 | fits | 123,983 | 199 | 0.440 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.aecp.first.if0` | 151,656 | 1.517 | 20 | 24 | fits | 143,099 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.aecp.last.if0` | 294,299 | 2.943 | 20 | 24 | fits | 143,633 | 199 | 0.465 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.maap.first.if0` | 294,233 | 2.942 | 20 | 50 | fits | 143,633 | 199 | 0.465 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.maap.last.if0` | 417,820 | 4.178 | 20 | 50 | fits | 123,983 | 199 | 0.440 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-5.service.srp.first.if0` | 502,316 | 5.023 | 20 | 20 | fits | 84,562 | 26 | 0.819 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-5.service.srp.last.if0` | 1,010,871 | 10.109 | 20 | 20 | fits | 75,235 | 28 | 0.583 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@blank-aged1-7.adp_available.if0` | 366,458 | 3.665 | 20 | 20 | fits | 145,054 | 202 | 0.503 |
| ADP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.adp.first.if0` | 282,283 | 2.823 | 20 | 200 | fits | 145,655 | 208 | 0.452 |
| ADP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.adp.last.if0` | 426,721 | 4.267 | 20 | 200 | fits | 145,054 | 202 | 0.503 |
| ACMP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.acmp.first.if0` | 283,207 | 2.832 | 20 | 20 | fits | 145,655 | 208 | 0.452 |
| ACMP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.acmp.last.if0` | 427,425 | 4.274 | 20 | 20 | fits | 145,054 | 202 | 0.503 |
| AECP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.aecp.first.if0` | 141,192 | 1.412 | 20 | 24 | fits | 143,099 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.aecp.last.if0` | 285,857 | 2.859 | 20 | 24 | fits | 145,655 | 208 | 0.452 |
| MAAP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.maap.first.if0` | 285,791 | 2.858 | 20 | 50 | fits | 145,655 | 208 | 0.452 |
| MAAP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.maap.last.if0` | 430,449 | 4.304 | 20 | 50 | fits | 145,054 | 202 | 0.503 |
| SRP record released under the composed load, first | `backlog-adp@blank-aged1-7.service.srp.first.if0` | 555,862 | 5.559 | 20 | 20 | fits | 84,416 | 32 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@blank-aged1-7.service.srp.last.if0` | 1,004,368 | 10.044 | 20 | 20 | fits | 64,067 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-1.adp_available.if0` | 360,721 | 3.607 | 20 | 20 | fits | 123,746 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-1.service.adp.first.if0` | 295,953 | 2.960 | 20 | 200 | fits | 145,993 | 208 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-1.service.adp.last.if0` | 419,083 | 4.191 | 20 | 200 | fits | 123,746 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-1.service.acmp.first.if0` | 296,877 | 2.969 | 20 | 20 | fits | 145,993 | 208 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-1.service.acmp.last.if0` | 419,787 | 4.198 | 20 | 20 | fits | 123,746 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-1.service.aecp.first.if0` | 146,498 | 1.465 | 20 | 24 | fits | 143,495 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-1.service.aecp.last.if0` | 299,527 | 2.995 | 20 | 24 | fits | 145,993 | 208 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-1.service.maap.first.if0` | 299,461 | 2.995 | 20 | 50 | fits | 145,993 | 208 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-1.service.maap.last.if0` | 422,811 | 4.228 | 20 | 50 | fits | 123,746 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-1.service.srp.first.if0` | 513,438 | 5.134 | 20 | 20 | fits | 90,693 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-1.service.srp.last.if0` | 915,379 | 9.154 | 20 | 20 | fits | 60,085 | 26 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-3.adp_available.if0` | 356,920 | 3.569 | 20 | 20 | fits | 123,777 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-3.service.adp.first.if0` | 292,327 | 2.923 | 20 | 200 | fits | 145,179 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-3.service.adp.last.if0` | 415,488 | 4.155 | 20 | 200 | fits | 123,777 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-3.service.acmp.first.if0` | 293,251 | 2.933 | 20 | 20 | fits | 145,179 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-3.service.acmp.last.if0` | 416,192 | 4.162 | 20 | 20 | fits | 123,777 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-3.service.aecp.first.if0` | 151,712 | 1.517 | 20 | 24 | fits | 143,420 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-3.service.aecp.last.if0` | 295,901 | 2.959 | 20 | 24 | fits | 145,179 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-3.service.maap.first.if0` | 295,835 | 2.958 | 20 | 50 | fits | 145,179 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-3.service.maap.last.if0` | 419,216 | 4.192 | 20 | 50 | fits | 123,777 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-3.service.srp.first.if0` | 509,771 | 5.098 | 20 | 20 | fits | 90,621 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-3.service.srp.last.if0` | 1,005,967 | 10.060 | 20 | 20 | fits | 64,156 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-5.adp_available.if0` | 355,501 | 3.555 | 20 | 20 | fits | 123,793 | 197 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-5.service.adp.first.if0` | 283,480 | 2.835 | 20 | 200 | fits | 146,539 | 208 | 0.457 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-5.service.adp.last.if0` | 406,657 | 4.067 | 20 | 200 | fits | 123,793 | 197 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-5.service.acmp.first.if0` | 284,404 | 2.844 | 20 | 20 | fits | 146,539 | 208 | 0.457 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-5.service.acmp.last.if0` | 407,361 | 4.074 | 20 | 20 | fits | 123,793 | 197 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-5.service.aecp.first.if0` | 141,505 | 1.415 | 20 | 24 | fits | 143,420 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-5.service.aecp.last.if0` | 287,054 | 2.871 | 20 | 24 | fits | 146,539 | 208 | 0.457 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-5.service.maap.first.if0` | 286,988 | 2.870 | 20 | 50 | fits | 146,539 | 208 | 0.457 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-5.service.maap.last.if0` | 410,385 | 4.104 | 20 | 50 | fits | 123,793 | 197 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-5.service.srp.first.if0` | 508,358 | 5.084 | 20 | 20 | fits | 88,996 | 37 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-5.service.srp.last.if0` | 995,240 | 9.952 | 20 | 20 | fits | 64,156 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged2-7.adp_available.if0` | 450,514 | 4.505 | 20 | 20 | fits | 135,147 | 214 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged2-7.service.adp.first.if0` | 294,380 | 2.944 | 20 | 200 | fits | 144,042 | 197 | 0.474 |
| ADP record released under the composed load, last | `backlog-adp@program-aged2-7.service.adp.last.if0` | 508,693 | 5.087 | 20 | 200 | fits | 135,147 | 214 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged2-7.service.acmp.first.if0` | 295,304 | 2.953 | 20 | 20 | fits | 144,042 | 197 | 0.474 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged2-7.service.acmp.last.if0` | 509,397 | 5.094 | 20 | 20 | fits | 135,147 | 214 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged2-7.service.aecp.first.if0` | 147,144 | 1.471 | 20 | 24 | fits | 143,555 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged2-7.service.aecp.last.if0` | 297,954 | 2.980 | 20 | 24 | fits | 144,042 | 197 | 0.474 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged2-7.service.maap.first.if0` | 297,888 | 2.979 | 20 | 50 | fits | 144,042 | 197 | 0.474 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged2-7.service.maap.last.if0` | 512,421 | 5.124 | 20 | 50 | fits | 135,147 | 214 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged2-7.service.srp.first.if0` | 603,084 | 6.031 | 20 | 20 | fits | 90,729 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@program-aged2-7.service.srp.last.if0` | 1,014,539 | 10.145 | 20 | 20 | fits | 65,381 | 25 | 0.661 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-1.adp_available.if0` | 369,285 | 3.693 | 20 | 20 | fits | 127,820 | 203 | 0.470 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-1.service.adp.first.if0` | 291,757 | 2.918 | 20 | 200 | fits | 144,768 | 204 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-1.service.adp.last.if0` | 428,201 | 4.282 | 20 | 200 | fits | 127,820 | 203 | 0.470 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-1.service.acmp.first.if0` | 292,681 | 2.927 | 20 | 20 | fits | 144,768 | 204 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-1.service.acmp.last.if0` | 428,905 | 4.289 | 20 | 20 | fits | 127,820 | 203 | 0.470 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-1.service.aecp.first.if0` | 151,553 | 1.516 | 20 | 24 | fits | 143,420 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-1.service.aecp.last.if0` | 295,331 | 2.953 | 20 | 24 | fits | 144,768 | 204 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-1.service.maap.first.if0` | 295,265 | 2.953 | 20 | 50 | fits | 144,768 | 204 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-1.service.maap.last.if0` | 431,929 | 4.319 | 20 | 50 | fits | 127,820 | 203 | 0.470 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-1.service.srp.first.if0` | 523,044 | 5.230 | 20 | 20 | fits | 91,181 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-1.service.srp.last.if0` | 924,891 | 9.249 | 20 | 20 | fits | 59,982 | 26 | 0.712 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-3.adp_available.if0` | 348,170 | 3.482 | 20 | 20 | fits | 127,065 | 202 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-3.service.adp.first.if0` | 280,335 | 2.803 | 20 | 200 | fits | 145,911 | 208 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-3.service.adp.last.if0` | 406,784 | 4.068 | 20 | 200 | fits | 127,065 | 202 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-3.service.acmp.first.if0` | 281,259 | 2.813 | 20 | 20 | fits | 145,911 | 208 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-3.service.acmp.last.if0` | 407,488 | 4.075 | 20 | 20 | fits | 127,065 | 202 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-3.service.aecp.first.if0` | 138,988 | 1.390 | 20 | 24 | fits | 145,257 | 147 | 0.437 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-3.service.aecp.last.if0` | 283,909 | 2.839 | 20 | 24 | fits | 145,911 | 208 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-3.service.maap.first.if0` | 283,843 | 2.838 | 20 | 50 | fits | 145,911 | 208 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-3.service.maap.last.if0` | 410,512 | 4.105 | 20 | 50 | fits | 127,065 | 202 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-3.service.srp.first.if0` | 501,421 | 5.014 | 20 | 20 | fits | 90,975 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-3.service.srp.last.if0` | 918,922 | 9.189 | 20 | 20 | fits | 68,869 | 31 | 0.680 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-5.adp_available.if0` | 359,727 | 3.597 | 20 | 20 | fits | 123,557 | 196 | 0.449 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-5.service.adp.first.if0` | 287,645 | 2.876 | 20 | 200 | fits | 145,243 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-5.service.adp.last.if0` | 410,586 | 4.106 | 20 | 200 | fits | 123,557 | 196 | 0.449 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-5.service.acmp.first.if0` | 288,569 | 2.886 | 20 | 20 | fits | 145,243 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-5.service.acmp.last.if0` | 411,290 | 4.113 | 20 | 20 | fits | 123,557 | 196 | 0.449 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-5.service.aecp.first.if0` | 146,966 | 1.470 | 20 | 24 | fits | 143,450 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-5.service.aecp.last.if0` | 291,219 | 2.912 | 20 | 24 | fits | 145,243 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-5.service.maap.first.if0` | 291,153 | 2.912 | 20 | 50 | fits | 145,243 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-5.service.maap.last.if0` | 414,314 | 4.143 | 20 | 50 | fits | 123,557 | 196 | 0.449 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-5.service.srp.first.if0` | 500,260 | 5.003 | 20 | 20 | fits | 86,012 | 30 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-5.service.srp.last.if0` | 922,801 | 9.228 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@program-aged1-7.adp_available.if0` | 378,629 | 3.786 | 20 | 20 | fits | 136,761 | 214 | 0.463 |
| ADP record released under the composed load, first | `backlog-adp@program-aged1-7.service.adp.first.if0` | 291,791 | 2.918 | 20 | 200 | fits | 144,236 | 198 | 0.472 |
| ADP record released under the composed load, last | `backlog-adp@program-aged1-7.service.adp.last.if0` | 437,156 | 4.372 | 20 | 200 | fits | 136,761 | 214 | 0.463 |
| ACMP record released under the composed load, first | `backlog-adp@program-aged1-7.service.acmp.first.if0` | 292,715 | 2.927 | 20 | 20 | fits | 144,236 | 198 | 0.472 |
| ACMP record released under the composed load, last | `backlog-adp@program-aged1-7.service.acmp.last.if0` | 437,860 | 4.379 | 20 | 20 | fits | 136,761 | 214 | 0.463 |
| AECP record released under the composed load, first | `backlog-adp@program-aged1-7.service.aecp.first.if0` | 152,119 | 1.521 | 20 | 24 | fits | 143,450 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@program-aged1-7.service.aecp.last.if0` | 295,365 | 2.954 | 20 | 24 | fits | 144,236 | 198 | 0.472 |
| MAAP record released under the composed load, first | `backlog-adp@program-aged1-7.service.maap.first.if0` | 295,299 | 2.953 | 20 | 50 | fits | 144,236 | 198 | 0.472 |
| MAAP record released under the composed load, last | `backlog-adp@program-aged1-7.service.maap.last.if0` | 440,884 | 4.409 | 20 | 50 | fits | 136,761 | 214 | 0.463 |
| SRP record released under the composed load, first | `backlog-adp@program-aged1-7.service.srp.first.if0` | 531,999 | 5.320 | 20 | 20 | fits | 91,181 | 28 | 0.735 |
| SRP record released under the composed load, last | `backlog-adp@program-aged1-7.service.srp.last.if0` | 926,930 | 9.269 | 20 | 20 | fits | 53,001 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-1.adp_available.if0` | 346,057 | 3.461 | 20 | 20 | fits | 123,786 | 196 | 0.451 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.adp.first.if0` | 281,366 | 2.814 | 20 | 200 | fits | 145,939 | 208 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.adp.last.if0` | 404,536 | 4.045 | 20 | 200 | fits | 123,786 | 196 | 0.451 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.acmp.first.if0` | 282,290 | 2.823 | 20 | 20 | fits | 145,939 | 208 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.acmp.last.if0` | 405,240 | 4.052 | 20 | 20 | fits | 123,786 | 196 | 0.451 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.aecp.first.if0` | 139,991 | 1.400 | 20 | 24 | fits | 143,378 | 142 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.aecp.last.if0` | 284,940 | 2.849 | 20 | 24 | fits | 145,939 | 208 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.maap.first.if0` | 284,874 | 2.849 | 20 | 50 | fits | 145,939 | 208 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.maap.last.if0` | 408,264 | 4.083 | 20 | 50 | fits | 123,786 | 196 | 0.451 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-1.service.srp.first.if0` | 499,070 | 4.991 | 20 | 20 | fits | 90,872 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-1.service.srp.last.if0` | 916,471 | 9.165 | 20 | 20 | fits | 59,596 | 26 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-3.adp_available.if0` | 357,885 | 3.579 | 20 | 20 | fits | 123,854 | 197 | 0.450 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.adp.first.if0` | 285,803 | 2.858 | 20 | 200 | fits | 145,223 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.adp.last.if0` | 409,041 | 4.090 | 20 | 200 | fits | 123,854 | 197 | 0.450 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.acmp.first.if0` | 286,727 | 2.867 | 20 | 20 | fits | 145,223 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.acmp.last.if0` | 409,745 | 4.097 | 20 | 20 | fits | 123,854 | 197 | 0.450 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.aecp.first.if0` | 145,144 | 1.451 | 20 | 24 | fits | 143,378 | 142 | 0.428 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.aecp.last.if0` | 289,377 | 2.894 | 20 | 24 | fits | 145,223 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.maap.first.if0` | 289,311 | 2.893 | 20 | 50 | fits | 145,223 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.maap.last.if0` | 412,769 | 4.128 | 20 | 50 | fits | 123,854 | 197 | 0.450 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-3.service.srp.first.if0` | 505,706 | 5.057 | 20 | 20 | fits | 83,918 | 31 | 0.771 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-3.service.srp.last.if0` | 997,054 | 9.971 | 20 | 20 | fits | 75,181 | 28 | 0.581 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-5.adp_available.if0` | 364,689 | 3.647 | 20 | 20 | fits | 123,693 | 196 | 0.453 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.adp.first.if0` | 299,677 | 2.997 | 20 | 200 | fits | 145,984 | 208 | 0.456 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.adp.last.if0` | 422,754 | 4.228 | 20 | 200 | fits | 123,693 | 196 | 0.453 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.acmp.first.if0` | 300,601 | 3.006 | 20 | 20 | fits | 145,984 | 208 | 0.456 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.acmp.last.if0` | 423,458 | 4.235 | 20 | 20 | fits | 123,693 | 196 | 0.453 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.aecp.first.if0` | 150,457 | 1.505 | 20 | 24 | fits | 143,538 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.aecp.last.if0` | 303,251 | 3.033 | 20 | 24 | fits | 145,984 | 208 | 0.456 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.maap.first.if0` | 303,185 | 3.032 | 20 | 50 | fits | 145,984 | 208 | 0.456 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.maap.last.if0` | 426,482 | 4.265 | 20 | 50 | fits | 123,693 | 196 | 0.453 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-5.service.srp.first.if0` | 512,273 | 5.123 | 20 | 20 | fits | 85,857 | 30 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-5.service.srp.last.if0` | 1,012,572 | 10.126 | 20 | 20 | fits | 69,086 | 31 | 0.683 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged2-7.adp_available.if0` | 355,161 | 3.552 | 20 | 20 | fits | 132,262 | 202 | 0.476 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.adp.first.if0` | 281,767 | 2.818 | 20 | 200 | fits | 145,875 | 208 | 0.453 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.adp.last.if0` | 413,413 | 4.134 | 20 | 200 | fits | 132,262 | 202 | 0.476 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.acmp.first.if0` | 282,691 | 2.827 | 20 | 20 | fits | 145,875 | 208 | 0.453 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.acmp.last.if0` | 414,117 | 4.141 | 20 | 20 | fits | 132,262 | 202 | 0.476 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.aecp.first.if0` | 140,456 | 1.405 | 20 | 24 | fits | 143,492 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.aecp.last.if0` | 285,341 | 2.853 | 20 | 24 | fits | 145,875 | 208 | 0.453 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.maap.first.if0` | 285,275 | 2.853 | 20 | 50 | fits | 145,875 | 208 | 0.453 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.maap.last.if0` | 417,141 | 4.171 | 20 | 50 | fits | 132,262 | 202 | 0.476 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged2-7.service.srp.first.if0` | 584,996 | 5.850 | 20 | 20 | fits | 91,039 | 29 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged2-7.service.srp.last.if0` | 995,610 | 9.956 | 20 | 20 | fits | 52,985 | 20 | 0.667 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-1.adp_available.if0` | 359,655 | 3.597 | 20 | 20 | fits | 123,924 | 196 | 0.452 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.adp.first.if0` | 294,798 | 2.948 | 20 | 200 | fits | 146,423 | 208 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.adp.last.if0` | 418,106 | 4.181 | 20 | 200 | fits | 123,924 | 196 | 0.452 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.acmp.first.if0` | 295,722 | 2.957 | 20 | 20 | fits | 146,423 | 208 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.acmp.last.if0` | 418,810 | 4.188 | 20 | 20 | fits | 123,924 | 196 | 0.452 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.aecp.first.if0` | 144,913 | 1.449 | 20 | 24 | fits | 143,423 | 143 | 0.429 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.aecp.last.if0` | 298,372 | 2.984 | 20 | 24 | fits | 146,423 | 208 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.maap.first.if0` | 298,306 | 2.983 | 20 | 50 | fits | 146,423 | 208 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.maap.last.if0` | 421,834 | 4.218 | 20 | 50 | fits | 123,924 | 196 | 0.452 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-1.service.srp.first.if0` | 512,573 | 5.126 | 20 | 20 | fits | 90,805 | 28 | 0.729 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-1.service.srp.last.if0` | 914,514 | 9.145 | 20 | 20 | fits | 60,085 | 26 | 0.713 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-3.adp_available.if0` | 362,887 | 3.629 | 20 | 20 | fits | 123,496 | 196 | 0.448 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.adp.first.if0` | 290,866 | 2.909 | 20 | 200 | fits | 145,159 | 203 | 0.460 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.adp.last.if0` | 413,746 | 4.137 | 20 | 200 | fits | 123,496 | 196 | 0.448 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.acmp.first.if0` | 291,790 | 2.918 | 20 | 20 | fits | 145,159 | 203 | 0.460 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.acmp.last.if0` | 414,450 | 4.144 | 20 | 20 | fits | 123,496 | 196 | 0.448 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.aecp.first.if0` | 150,271 | 1.503 | 20 | 24 | fits | 143,492 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.aecp.last.if0` | 294,440 | 2.944 | 20 | 24 | fits | 145,159 | 203 | 0.460 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.maap.first.if0` | 294,374 | 2.944 | 20 | 50 | fits | 145,159 | 203 | 0.460 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.maap.last.if0` | 417,474 | 4.175 | 20 | 50 | fits | 123,496 | 196 | 0.448 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-3.service.srp.first.if0` | 508,307 | 5.083 | 20 | 20 | fits | 90,899 | 28 | 0.730 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-3.service.srp.last.if0` | 924,228 | 9.242 | 20 | 20 | fits | 64,161 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-5.adp_available.if0` | 354,669 | 3.547 | 20 | 20 | fits | 124,604 | 200 | 0.442 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.adp.first.if0` | 280,983 | 2.810 | 20 | 200 | fits | 145,132 | 204 | 0.463 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.adp.last.if0` | 404,971 | 4.050 | 20 | 200 | fits | 124,604 | 200 | 0.442 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.acmp.first.if0` | 281,907 | 2.819 | 20 | 20 | fits | 145,132 | 204 | 0.463 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.acmp.last.if0` | 405,675 | 4.057 | 20 | 20 | fits | 124,604 | 200 | 0.442 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.aecp.first.if0` | 140,415 | 1.404 | 20 | 24 | fits | 143,492 | 142 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.aecp.last.if0` | 284,557 | 2.846 | 20 | 24 | fits | 145,132 | 204 | 0.463 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.maap.first.if0` | 284,491 | 2.845 | 20 | 50 | fits | 145,132 | 204 | 0.463 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.maap.last.if0` | 408,699 | 4.087 | 20 | 50 | fits | 124,604 | 200 | 0.442 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-5.service.srp.first.if0` | 506,902 | 5.069 | 20 | 20 | fits | 89,110 | 37 | 0.769 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-5.service.srp.last.if0` | 913,082 | 9.131 | 20 | 20 | fits | 64,131 | 24 | 0.620 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog-adp@verify-aged1-7.adp_available.if0` | 370,147 | 3.701 | 20 | 20 | fits | 136,254 | 214 | 0.454 |
| ADP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.adp.first.if0` | 292,947 | 2.929 | 20 | 200 | fits | 144,050 | 197 | 0.474 |
| ADP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.adp.last.if0` | 428,585 | 4.286 | 20 | 200 | fits | 136,254 | 214 | 0.454 |
| ACMP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.acmp.first.if0` | 293,871 | 2.939 | 20 | 20 | fits | 144,050 | 197 | 0.474 |
| ACMP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.acmp.last.if0` | 429,289 | 4.293 | 20 | 20 | fits | 136,254 | 214 | 0.454 |
| AECP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.aecp.first.if0` | 145,703 | 1.457 | 20 | 24 | fits | 143,627 | 143 | 0.430 |
| AECP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.aecp.last.if0` | 296,521 | 2.965 | 20 | 24 | fits | 144,050 | 197 | 0.474 |
| MAAP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.maap.first.if0` | 296,455 | 2.965 | 20 | 50 | fits | 144,050 | 197 | 0.474 |
| MAAP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.maap.last.if0` | 432,313 | 4.323 | 20 | 50 | fits | 136,254 | 214 | 0.454 |
| SRP record released under the composed load, first | `backlog-adp@verify-aged1-7.service.srp.first.if0` | 523,313 | 5.233 | 20 | 20 | fits | 91,066 | 28 | 0.732 |
| SRP record released under the composed load, last | `backlog-adp@verify-aged1-7.service.srp.last.if0` | 923,031 | 9.230 | 20 | 20 | fits | 57,899 | 27 | 0.697 |
| ADP record, every channel at its refill rate, the longest | `save-held.held.adp.if0` | 150,373 | 1.504 | 20 | 200 | fits | 151,313 | 242 | 0.499 |
| ACMP record, every channel at its refill rate, the longest | `save-held.held.acmp.if0` | 224,749 | 2.247 | 20 | 20 | fits | 94,513 | 91 | 0.657 |
| AECP record, every channel at its refill rate, the longest | `save-held.held.aecp.if0` | 282,795 | 2.828 | 20 | 24 | fits | 91,788 | 58 | 0.552 |
| MAAP record, every channel at its refill rate, the longest | `save-held.held.maap.if0` | 158,333 | 1.583 | 20 | 50 | fits | 89,811 | 183 | 0.381 |
| SRP record, every channel at its refill rate, the longest | `save-held.held.srp.if0` | 854,273 | 8.543 | 20 | 20 | fits | 30,706 | 12 | 0.803 |
| an MRPDU its periodic timer owes, the longest | `save-held.mrpdu.periodic.if0` | 250,673 | 2.507 | 20 | 20 | fits | 0 | - | 0.000 |
| TMR_DELAY, or the first TMR_NO_RESP | `acmp.tmr_no_resp1.if0` | 17,774 | 0.178 | 20 | 20 | fits | 27,664 | 21 (35) | 0.808 |
| the second TMR_NO_RESP | `acmp.tmr_no_resp2.if0` | 7,077 | 0.071 | 20 | 20 | fits | 24,439 | 17 (14) | 0.840 |
| TMR_RETRY | `acmp.tmr_retry.if0` | 14,173 | 0.142 | 20 | 20 | fits | 23,727 | 18 (14) | 0.833 |
| TMR_DELAY | `acmp.tmr_delay.if0` | 23,089 | 0.231 | 20 | 20 | fits | 28,117 | 21 (35) | 0.814 |
| startup declarations (LINK_UP) | `srp.startup.if0` | 88,817 | 0.888 | 20 | 20 | fits | 28,127 | 8 | 0.817 |
| Listener Ready RX (registrar) | `srp.listener_ready.if0` | 44,344 | 0.443 | 20 | 20 | fits | 44,410 | 12 | 0.886 |
| malformed MRPDU discard | `srp.malformed.if0` | 21,130 | 0.211 | 20 | 20 | fits | 21,196 | 12 | 0.678 |
| Domain RX -> declarations (JoinTime wait) | `srp.domain.if0` | 99,317 | 0.993 | 220 | 220 | fits | 69,567 | 6 | 0.878 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 352,900 | 3.529 | 20 | 20 | fits | 128,105 | 203 | 0.461 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 283,897 | 2.839 | 20 | 200 | fits | 144,750 | 203 | 0.454 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 411,386 | 4.114 | 20 | 200 | fits | 128,105 | 203 | 0.461 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 284,821 | 2.848 | 20 | 20 | fits | 144,750 | 203 | 0.454 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 412,090 | 4.121 | 20 | 20 | fits | 128,105 | 203 | 0.461 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 143,711 | 1.437 | 20 | 24 | fits | 143,897 | 145 | 0.431 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 287,471 | 2.875 | 20 | 24 | fits | 144,750 | 203 | 0.454 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 287,405 | 2.874 | 20 | 50 | fits | 144,750 | 203 | 0.454 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 415,114 | 4.151 | 20 | 50 | fits | 128,105 | 203 | 0.461 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 505,032 | 5.050 | 20 | 20 | fits | 80,606 | 25 | 0.772 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 918,182 | 9.182 | 20 | 20 | fits | 75,256 | 28 | 0.583 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,297,110 | 62.971 | 20 | 20 | MISS ceiling | 18,127 | 13 | 0.658 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 6,315,244 | 63.152 | 20 | 20 | MISS ceiling | 18,131 | 13 | 0.658 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 6,333,246 | 63.332 | 20 | 20 | MISS ceiling | 18,059 | 13 | 0.667 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 6,351,238 | 63.512 | 20 | 20 | MISS ceiling | 18,068 | 13 | 0.667 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 6,369,191 | 63.692 | 20 | 20 | MISS ceiling | 17,942 | 13 | 0.662 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 142,860 | 1.429 | 20 | 200 | fits | 143,145 | 200 | 0.458 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 237,559 | 2.376 | 20 | 200 | fits | 95,315 | 185 | 0.400 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 138,538 | 1.385 | 20 | 20 | fits | 143,145 | 200 | 0.458 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 6,209,282 | 62.093 | 20 | 20 | MISS ceiling | 28,059 | 15 | 0.753 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 142,178 | 1.422 | 20 | 24 | fits | 143,145 | 200 | 0.458 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,184,709 | 61.847 | 20 | 24 | MISS ceiling | 144,378 | 106 | 0.468 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 141,122 | 1.411 | 20 | 50 | fits | 143,145 | 200 | 0.458 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 236,041 | 2.360 | 20 | 50 | fits | 95,315 | 185 | 0.400 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 326,901 | 3.269 | 20 | 20 | fits | 90,926 | 28 | 0.731 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 727,199 | 7.272 | 20 | 20 | fits | 63,749 | 24 | 0.603 |
| first PROBE (LINK_UP) | `maap.probe1.if0` | 11,112 | 0.111 | 20 | 50 | fits | 26,340 | 43 | 0.722 |
| PROBE retransmission (TMR expiry) | `maap.probe2.if0` | 10,228 | 0.102 | 20 | 50 | fits | 22,129 | 35 | 0.695 |
| PROBE retransmission (TMR expiry) | `maap.probe3.if0` | 12,379 | 0.124 | 20 | 50 | fits | 22,113 | 35 | 0.695 |
| last PROBE retransmission (TMR expiry) | `maap.probe4.if0` | 12,049 | 0.120 | 20 | 50 | fits | 27,940 | 61 | 0.633 |
| ANNOUNCE (TMR expiry) | `maap.announce.if0` | 14,779 | 0.148 | 20 | 50 | fits | 27,940 | 61 | 0.633 |
| conflicting PROBE -> DEFEND | `maap.defend.if0` | 8,952 | 0.090 | 20 | 50 | fits | 20,638 | 30 | 0.661 |
| LINK_UP | `adp.link_up.if0` | 2,593 | 0.026 | 20 | 200 | fits | 26,340 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,368 | 0.174 | 20 | 200 | fits | 21,586 | 23 (39) | 0.724 |
| GM_CHANGE | `adp.gm_change.if0` | 2,432 | 0.024 | 20 | 200 | fits | 15,774 | 17 (11) | 0.677 |
| LINK_UP | `adp.link_up.if0` | 2,593 | 0.026 | 20 | 200 | fits | 26,340 | 43 (11) | 0.722 |
| TMR_DELAY expiry | `adp.tmr_delay.if0` | 17,368 | 0.174 | 20 | 200 | fits | 21,586 | 23 (39) | 0.724 |
| RCV_ADP_DISCOVER (control) | `control.discover.if0` | 4,641 | 0.046 | 20 | 200 | fits | 16,191 | 16 (31) | 0.667 |
| BIND_RX | `acmp.bind_rx.if0` | 18,435 | 0.184 | 20 | 20 | fits | 38,970 | 26 (77) | 0.788 |
| PROBE_TX_RESPONSE | `acmp.probe_tx_response.if0` | 9,156 | 0.092 | 20 | 20 | fits | 30,282 | 19 (32) | 0.825 |
| GET_RX_STATE | `acmp.get_rx_state.if0` | 10,334 | 0.103 | 20 | 20 | fits | 23,459 | 15 (47) | 0.762 |
| UNBIND_RX | `acmp.unbind_rx.if0` | 13,174 | 0.132 | 20 | 20 | fits | 37,853 | 18 (50) | 0.836 |
| PROBE_TX, refused TALKER_DEST_MAC_FAIL | `acmp.probe_tx.if0` | 10,089 | 0.101 | 20 | 20 | fits | 24,546 | 17 (48) | 0.766 |
| GET_TX_STATE | `acmp.get_tx_state.if0` | 9,765 | 0.098 | 20 | 20 | fits | 22,963 | 16 (48) | 0.735 |
| DISCONNECT_TX | `acmp.disconnect_tx.if0` | 9,475 | 0.095 | 20 | 20 | fits | 22,707 | 16 (48) | 0.735 |
| GET_TX_CONNECTION, refused NOT_SUPPORTED | `acmp.get_tx_connection.if0` | 8,754 | 0.088 | 20 | 20 | fits | 22,651 | 16 (48) | 0.735 |
| REMOVE_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.remove_audio_mappings.if0` | 137,148 | 1.371 | 20 | 24 | fits | 143,728 | 92 | 0.333 |
| ADD_AUDIO_MAPPINGS of 63 (550 B notice) | `aecp_long.add_audio_mappings.if0` | 166,253 | 1.663 | 20 | 24 | fits | 134,452 | 70 | 0.301 |
| COLLISION_INDICES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_indices.if0` | 135,107 | 1.351 | 20 | 24 | fits | 40,550 | 17 | 0.706 |
| COLLISION_VALUES of 63, refused BAD_ARGUMENTS | `aecp_long.refused.collision_values.if0` | 297,157 | 2.972 | 20 | 24 | fits | 90,517 | 18 | 0.690 |
| CONFLICT_LAST of 63, refused BAD_ARGUMENTS | `aecp_long.refused.conflict_last.if0` | 241,878 | 2.419 | 20 | 24 | fits | 92,139 | 17 | 0.694 |
| LINK_UP | `fixture.link_up.if0` | 2,593 | 0.026 | 20 | 200 | fits | 26,340 | 43 (11) | 0.722 |
| malformed MRPDU discard | `fixture.malformed.if0` | 21,453 | 0.215 | 20 | 20 | fits | 21,519 | 12 | 0.730 |
| SET_NAME fan-out to one registered controller | `fixture.set_name.if0` | 33,623 | 0.336 | 20 | 24 | fits | 47,887 | 43 | 0.782 |
| LINK_DOWN | `fixture.link_down.if0` | 2,692 | 0.027 | 20 | 200 | fits | 26,890 | 23 (9) | 0.789 |
| BIND_RX | `fixture.bind_rx.if0` | 18,770 | 0.188 | 20 | 20 | fits | 39,503 | 26 (77) | 0.797 |
| TMR_DELAY, or the first TMR_NO_RESP | `fixture.tmr_no_resp1.if0` | 12,862 | 0.129 | 20 | 20 | fits | 34,680 | 29 (35) | 0.784 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | `fixture.entity_departing.if0` | 6,204 | 0.062 | 20 | 20 | fits | 23,575 | 13 (29) | 0.803 |
| ADP record released under the composed load, first | `fixture.service.adp.first.if0` | 82,774 | 0.828 | 20 | 200 | fits | 82,878 | 51 | 0.764 |
| ADP record released under the composed load, last | `fixture.service.adp.last.if0` | 82,774 | 0.828 | 20 | 200 | fits | 82,878 | 51 | 0.764 |
| ACMP record released under the composed load, first | `fixture.service.acmp.first.if0` | 82,500 | 0.825 | 20 | 20 | fits | 82,878 | 51 | 0.764 |
| ACMP record released under the composed load, last | `fixture.service.acmp.last.if0` | 82,500 | 0.825 | 20 | 20 | fits | 82,878 | 51 | 0.764 |
| AECP record released under the composed load, first | `fixture.service.aecp.first.if0` | 82,708 | 0.827 | 20 | 24 | fits | 82,878 | 51 | 0.764 |
| AECP record released under the composed load, last | `fixture.service.aecp.last.if0` | 82,708 | 0.827 | 20 | 24 | fits | 82,878 | 51 | 0.764 |
| MAAP record released under the composed load, first | `fixture.service.maap.first.if0` | 82,642 | 0.826 | 20 | 50 | fits | 82,878 | 51 | 0.764 |
| MAAP record released under the composed load, last | `fixture.service.maap.last.if0` | 82,642 | 0.826 | 20 | 50 | fits | 82,878 | 51 | 0.764 |
| SRP record released under the composed load, first | `fixture.service.srp.first.if0` | 82,576 | 0.826 | 20 | 20 | fits | 82,878 | 51 | 0.764 |
| SRP record released under the composed load, last | `fixture.service.srp.last.if0` | 82,576 | 0.826 | 20 | 20 | fits | 82,878 | 51 | 0.764 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
