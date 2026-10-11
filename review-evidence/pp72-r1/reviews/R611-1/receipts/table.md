| REQ | Ver | State | file:line | Check | Tag category |
|---|---|---|---|---|---|
| REQ-ADP-001 | TIM | traced | `tb/adp_engine/sim_main.cpp:762` | P2 T-ADP-ADV armed at 5 s | TIM |
| REQ-ADP-001 | TIM | traced | `tb/pp_top/sim_main.cpp:10145` | S3: T-ADP-ADV 5 s + 0-4 s anti-storm | TIM |
| REQ-ADP-002 | DIR | traced | `tb/adp_engine/sim_main.cpp:749` | P2 AVAILABLE byte | DIR |
| REQ-ADP-003 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:285` | LintTest.test_mutations | DIR |
| REQ-ADP-003 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:783` | IdentityTest.test_driven_values_agree | DIR |
| REQ-ADP-004 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:286` | LintTest.test_mutations | DIR |
| REQ-ADP-004 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:784` | IdentityTest.test_driven_values_agree | DIR |
| REQ-ADP-005 | DIR | traced | `tb/adp_engine/sim_main.cpp:1224` | P11b advert byte-exact: only available_index (+1) and 64..65 moved | DIR |
| REQ-ADP-006 | DIR | traced | `tb/adp_engine/sim_main.cpp:706` | P12 no committed frame and no TX request with enable low | DIR |
| REQ-ADP-007 | MTXW | traced | `tb/adp_engine/sim_main.cpp:1695` | P13 MTXW walked | MTXW |
| REQ-ADP-008 | TIM | traced | `tb/adp_engine/sim_main.cpp:964` | P8 every kind-1 draw <= 2000 | TIM |
| REQ-ADP-008 | TIM | traced | `tb/adp_engine/sim_main.cpp:966` | P8 every kind-2 draw <= 4000 | TIM |
| REQ-ADP-008 | TIM | traced | `tb/pp_top/sim_main.cpp:10133` | S3: first advertise inside 0..2 s | TIM |
| REQ-ADP-009 | DIR | traced | `tb/adp_engine/sim_main.cpp:849` | P5 frame after GM change | DIR |
| REQ-ADP-010 | DIR | traced | `tb/adp_engine/sim_main.cpp:881` | P6 NO departing on link-down | DIR |
| REQ-ADP-010 | DIR | traced | `tb/adp_engine/sim_main.cpp:898` | P7 departing sent | DIR |
| REQ-ADP-011 | DIR | traced | `tb/adp_engine/sim_main.cpp:758` | P2 available_index incremented AFTER tx | DIR |
| REQ-ADP-011 | DIR | traced | `tb/adp_engine/sim_main.cpp:909` | P7 index reset to 0 after DEPARTING | DIR |
| REQ-ADP-012 | MTXW | traced | `tb/adp_engine/sim_main.cpp:1698` | P13 MTXW walked | MTXW |
| REQ-ADP-013 | DIR | traced | `tb/adp_engine/sim_main.cpp:1030` | P9d GM mismatch ignored | DIR |
| REQ-ADP-013 | DIR | traced | `tb/adp_engine/sim_main.cpp:1035` | P9d domain mismatch ignored | DIR |
| REQ-ADP-013 | DIR | traced | `tb/adp_engine/sim_main.cpp:1051` | P9e restart fires a pair | DIR |
| REQ-ADP-014 | TIM | traced | `tb/adp_engine/sim_main.cpp:997` | P9a NOADP = rx valid_time (20 s) | TIM |
| REQ-ADP-014 | TIM | traced | `tb/adp_engine/sim_main.cpp:1119` | P9i aging fires EVT_TK_DEPARTED | TIM |
| REQ-ACMP-001 | TOL | traced | `tb/pp_top/sim_main.cpp:9590` | AL1: a 96-B UNBIND_RX is answered by the 56-B cdl-44 UNBIND_RX_RESPONSE | TOL |
| REQ-ACMP-001 | TOL | traced | `tb/pp_top/sim_main.cpp:9623` | AL3: the 96-B PROBE_TX gets the same 56-B cdl-44 response | TOL |
| REQ-ACMP-002 | DIR | traced | `tb/pp_top/sim_main.cpp:9549` | AI1: PROBE_TX #1 byte-exact | DIR |
| REQ-ACMP-002 | DIR | traced | `tb/pp_top/sim_main.cpp:10196` | S6: BIND_RX_RESPONSE SUCCESS byte-exact | DIR |
| REQ-ACMP-003 | TIM | traced | `tb/pp_top/sim_main.cpp:9568` | AI3: the sink never left PRB_W_RESP | TIM |
| REQ-ACMP-004 | DIR | traced | `tb/acmp_talker/sim_main.cpp:566` | B5 identical query = identical answer | DIR |
| REQ-ACMP-004 | DIR | traced | `tb/acmp_talker/sim_main.cpp:808` | G2 stateless: identical probe = identical bytes | DIR |
| REQ-ACMP-005 | DIR | traced | `tb/acmp_talker/sim_main.cpp:533` | B1 | DIR |
| REQ-ACMP-005 | DIR | traced | `tb/acmp_talker/sim_main.cpp:598` | C1 unknown-id | DIR |
| REQ-ACMP-005 | DIR | traced | `tb/acmp_talker/sim_main.cpp:610` | C3 no response on wrong interface | DIR |
| REQ-ACMP-005 | DIR | traced | `tb/acmp_talker/sim_main.cpp:699` | E2 backoff probe | DIR |
| REQ-ACMP-006 | DIR | traced | `tb/acmp_talker/sim_main.cpp:525` | B1 declare | DIR |
| REQ-ACMP-007 | DIR | traced | `tb/acmp_talker/sim_main.cpp:618` | C4 disconnect no-op | DIR |
| REQ-ACMP-007 | DIR | traced | `tb/acmp_talker/sim_main.cpp:620` | C4 changes nothing | DIR |
| REQ-ACMP-007 | DIR | traced | `tb/acmp_talker/sim_main.cpp:626` | C5 get_tx_connection | DIR |
| REQ-ACMP-007 | DIR | traced | `tb/acmp_talker/sim_main.cpp:1211` | TD1 invalid disconnect leaves source state unchanged | DIR |
| REQ-ACMP-008 | DIR | traced | `tb/acmp_talker/sim_main.cpp:549` | B3 | DIR |
| REQ-ACMP-008 | DIR | traced | `tb/acmp_talker/sim_main.cpp:577` | B6 | DIR |
| REQ-ACMP-009 | TIM | traced | `tb/acmp_talker/sim_main.cpp:523` | B1 dafresh | TIM |
| REQ-ACMP-009 | TIM | traced | `tb/acmp_talker/sim_main.cpp:661` | D2 freshness lapse | TIM |
| REQ-ACMP-010 | DIR | traced | `tb/acmp_talker/sim_main.cpp:693` | E1 leaveall2 | DIR |
| REQ-ACMP-010 | DIR | traced | `tb/acmp_talker/sim_main.cpp:709` | E3 re-declare new DA | DIR |
| REQ-ACMP-010 | DIR | traced | `tb/acmp_talker/sim_main.cpp:747` | F2 pcp withdraw src0 | DIR |
| REQ-ACMP-010 | DIR | traced | `tb/acmp_talker/sim_main.cpp:768` | F4 re-declare same DA | DIR |
| REQ-ACMP-011 | MTXW | traced | `tb/acmp_listener/sim_main.cpp:1110` | MTXW walked | MTXW |
| REQ-ACMP-012 | TOL | traced | `tb/acmp_listener/sim_main.cpp:1207` | status LISTENER_UNKNOWN_ID | TOL |
| REQ-ACMP-012 | TOL | traced | `tb/acmp_listener/sim_main.cpp:1238` | B8: no write-back, slot returned | TOL |
| REQ-ACMP-012 | TOL | traced | `tb/pp_top/sim_main.cpp:9558` | AI2: message types 7 and 14 raise no ACMP frame | TOL |
| REQ-ACMP-013 | MTXW | traced | `tb/acmp_listener/sim_main.cpp:1111` | MTXW walked | MTXW |
| REQ-ACMP-014 | MTXW | traced | `tb/acmp_listener/sim_main.cpp:1112` | MTXW walked | MTXW |
| REQ-ACMP-015 | TIM | traced | `tb/acmp_listener/sim_main.cpp:1145` | B2 dbl-timeout | TIM |
| REQ-ACMP-015 | TIM | traced | `tb/pp_top/sim_main.cpp:9569` | AI3: the sink never left PRB_W_RESP | TIM |
| REQ-ACMP-015 | TIM | traced | `tb/pp_top/sim_main.cpp:9647` | AS1: no talker discovered, so T-ACMP-RETRY re-probes nothing | TIM |
| REQ-ACMP-016 | MTXW | traced | `tb/acmp_listener/sim_main.cpp:1113` | MTXW walked | MTXW |
| REQ-ACMP-017 | DIR | traced | `tb/pp_top/sim_main.cpp:9715` | AS3: near misses (DA, VLAN, stream_id) put no Listener | DIR |
| REQ-ACMP-018 | DIR | traced | `tb/pp_top/sim_main.cpp:9694` | AS2: nothing declared or registered before a matching talker | DIR |
| REQ-ACMP-018 | DIR | traced | `tb/pp_top/sim_main.cpp:9742` | AS4: the matching Talker Advertise yields Listener Ready New | DIR |
| REQ-ACMP-019 | MTXW | traced | `tb/acmp_listener/sim_main.cpp:1114` | MTXW walked | MTXW |
| REQ-ACMP-020 | DIR | traced | `tb/acmp_listener/sim_main.cpp:1342` | B9: CONTROLLER_NOT_AUTHORIZED | DIR |
| REQ-ACMP-020 | DIR | traced | `tb/pp_top/sim_main.cpp:5148` | L4b: CONTROLLER_NOT_AUTHORIZED for sink 2 | DIR |
| REQ-ACMP-021 | NVM | traced | `tb/acmp_nvm/sim_main.cpp:1018` | B6 sink 2 record byte-exact vs the model | NVM |
| REQ-ACMP-021 | NVM | traced | `tb/acmp_nvm/sim_main.cpp:1182` | F10 listener wrote three PRB_W_AVAIL records | NVM |
| REQ-ACMP-021 | NVM | traced | `tb/pp_top/d3_phases.hpp:3543` | sink 0's saved binding restored, probing PASSIVE | NVM |
| REQ-ACMP-021 | NVM | traced | `tb/pp_top/sim_main.cpp:10542` | BW2: a reset restores the same binding | NVM |
| REQ-ACMP-022 | DIR | traced | `tb/pp_top/sim_main.cpp:9654` | AS1: GET_RX_STATE while probing | DIR |
| REQ-ACMP-022 | DIR | traced | `tb/pp_top/sim_main.cpp:9687` | AS2: GET_RX_STATE settled | DIR |
| REQ-ACMP-022 | DIR | traced | `tb/pp_top/sim_main.cpp:9830` | AS6: GET_RX_STATE unbound | DIR |
| REQ-ACMP-023 | DIR | traced | `tb/pp_top/gsi_internal.hpp:83` | pbsta sink | DIR |
| REQ-ACMP-023 | DIR | traced | `tb/pp_top/gsi_internal.hpp:86` | acmpsta sink | DIR |
| REQ-AEM-001 | DIR | traced | `tb/pp_top/sim_main.cpp:11913` | OV2 AUDIO_MAP 1 | DIR |
| REQ-AEM-001 | DIR | traced | `tb/pp_top/sim_main.cpp:11969` | PG5 a 66-mapping page | DIR |
| REQ-AEM-002 | DIR | traced | `tb/pp_top/sim_main.cpp:5118` | L1: ACQUIRE answers NOT_SUPPORTED | DIR |
| REQ-AEM-003 | TIM | traced | `tb/pp_top/notify_phases.hpp:2351` | TD1: T-LOCK-UNLOCK at its default | TIM |
| REQ-AEM-003 | TIM | traced | `tb/pp_top/sim_main.cpp:5269` | L6d: 60 s auto-unlock notifies | TIM |
| REQ-AEM-003 | TIM | traced | `tb/pp_top/sim_main.cpp:5284` | L7: locking STREAM_INPUT refuses NOT_SUPPORTED | DIR |
| REQ-AEM-004 | DIR | traced | `tb/pp_top/sim_main.cpp:6941` | W1: ENTITY_AVAILABLE byte-exact | DIR |
| REQ-AEM-004 | DIR | traced | `tb/pp_top/sim_main.cpp:6964` | W2b: ENTITY_AVAILABLE carries ENTITY_LOCKED + the holder eid | DIR |
| REQ-AEM-005 | RND | traced | `tb/originator/sim_main.cpp:882` | R: a seeded session of 16 owners' overlapping exchanges | RND |
| REQ-AEM-006 | DIR | traced | `tb/pp_top/sim_main.cpp:2360` | A2: NO_SUCH_DESCRIPTOR response is not byte-exact | DIR |
| REQ-AEM-006 | DIR | traced | `tb/pp_top/sim_main.cpp:5312` | L9: READ_DESCRIPTOR from a non-holder answers while locked | DIR |
| REQ-AEM-007 | DIR | traced | `tb/pp_top/sim_main.cpp:7596` | W15b: SET_CONFIGURATION refuses STREAM_IS_RUNNING | DIR |
| REQ-AEM-007 | DIR | traced | `tb/pp_top/sim_main.cpp:7731` | W17h: SET_CONFIGURATION refuses STREAM_IS_RUNNING | DIR |
| REQ-AEM-007 | DIR | traced | `tb/pp_top/sim_main.cpp:7995` | W19g: SET_CONFIGURATION from a foreign controller | DIR |
| REQ-AEM-008 | DIR | traced | `tb/pp_top/sim_main.cpp:6759` | W23d: a shrink that orphans a mapping refuses and writes nothing | DIR |
| REQ-AEM-008 | DIR | traced | `tb/pp_top/sim_main.cpp:6807` | W23h: a bound Stream Input refuses STREAM_IS_RUNNING | DIR |
| REQ-AEM-009 | DIR | traced | `tb/pp_top/sim_main.cpp:8113` | W24a: SET_STREAM_INFO(ACC_LAT) byte-exact echo | DIR |
| REQ-AEM-009 | DIR | traced | `tb/pp_top/sim_main.cpp:8132` | W24c: SET_STREAM_INFO on a Stream Input is NOT_SUPPORTED | DIR |
| REQ-AEM-009 | DIR | traced | `tb/pp_top/sim_main.cpp:8140` | W24d: an extra flag refuses whole and writes nothing | DIR |
| REQ-AEM-010 | DIR | traced | `tb/pp_top/sim_main.cpp:5384` | G1: STREAM_INPUT[0] Milan 80-byte response byte-exact | DIR |
| REQ-AEM-011 | DIR | traced | `tb/pp_top/d3_phases.hpp:3214` | D3N1 ordinal | NVM |
| REQ-AEM-011 | DIR | traced | `tb/pp_top/sim_main.cpp:2755` | N4: changed CLOCK_DOMAIN SET_NAME response is not byte-exact | DIR |
| REQ-AEM-011 | DIR | traced | `tb/pp_top/sim_main.cpp:2761` | N4b: GET_NAME does not observe the completed SET_NAME | DIR |
| REQ-AEM-011 | DIR | traced | `tb/pp_top/sim_main.cpp:2786` | N5: ENTITY group SET_NAME response is not byte-exact | DIR |
| REQ-AEM-012 | DIR | traced | `tb/pp_top/sim_main.cpp:7233` | W9: SET_SAMPLING_RATE byte-exact | DIR |
| REQ-AEM-012 | DIR | traced | `tb/pp_top/sim_main.cpp:7249` | W9b2: GET_SAMPLING_RATE reads | DIR |
| REQ-AEM-013 | NVM | traced | `tb/pp_top/d3_phases.hpp:1201` | D3R1 clks: clock source 2 restored with its valid flag | NVM |
| REQ-AEM-013 | NVM | traced | `tb/pp_top/d3_phases.hpp:2974` | D3C3 restore: clock source 9 restored with its valid flag | NVM |
| REQ-AEM-014 | DIR | traced | `tb/pp_top/sim_main.cpp:7522` | W12c: Milan 5.3.12 makes the reset value 0 | DIR |
| REQ-AEM-014 | DIR | traced | `tb/pp_top/sim_main.cpp:7540` | W12f: GET_CONTROL now reads 255 | DIR |
| REQ-AEM-014 | DIR | traced | `tb/pp_top/sim_main.cpp:7564` | W13: SET_CONTROL 128 is BAD_ARGUMENTS | DIR |
| REQ-AEM-015 | DIR | traced | `tb/pp_top/sim_main.cpp:6374` | W21a: STOP_STREAMING on a bound Stream Input is SUCCESS | DIR |
| REQ-AEM-015 | DIR | traced | `tb/pp_top/sim_main.cpp:6411` | W21h: START_STREAMING did not set the started bit | DIR |
| REQ-AEM-015 | DIR | traced | `tb/pp_top/sim_main.cpp:6421` | W21i: START_STREAMING on a Stream Output is NOT_SUPPORTED | DIR |
| REQ-AEM-016 | RND | traced | `tb/pp_top/notify_phases.hpp:1635` | RN | RND |
| REQ-AEM-017 | TIM | traced | `tb/pp_top/notify_phases.hpp:2366` | TD2: T-NOTIF-TIMELIMITED at its default | TIM |
| REQ-AEM-017 | TIM | traced | `tb/pp_top/sim_main.cpp:4844` | U2: 2013-format REGISTER accepted and answered in its own format | TOL |
| REQ-AEM-017 | TIM | traced | `tb/pp_top/sim_main.cpp:4921` | U5c: unsolicited DEREGISTER byte-exact | TIM |
| REQ-AEM-018 | DIR | traced | `tb/pp_top/sim_main.cpp:3854` | K1: GET_COUNTERS response is not byte-exact | DIR |
| REQ-AEM-018 | DIR | traced | `tb/pp_top/sim_main.cpp:3924` | K4b: STREAM_OUTPUT | DIR |
| REQ-AEM-018 | DIR | traced | `tb/pp_top/sim_main.cpp:3945` | K4c: AVB_INTERFACE 0 carries the store's 0x23 block byte-exact | DIR |
| REQ-AEM-018 | DIR | traced | `tb/pp_top/sim_main.cpp:3952` | K4d: CLOCK_DOMAIN 0 carries the store's 0x03 block byte-exact | DIR |
| REQ-AEM-019 | DIR | waived GAP-05 | | | |
| REQ-AEM-020 | DIR | traced | `tb/pp_top/sim_main.cpp:4128` | Q1: GET_AUDIO_MAP response is not byte-exact | DIR |
| REQ-AEM-020 | DIR | traced | `tb/pp_top/sim_main.cpp:4140` | Q2: page 1 of port 1 is not byte-exact | DIR |
| REQ-AEM-020 | DIR | traced | `tb/pp_top/sim_main.cpp:11974` | PG8 a 176-mapping page | DIR |
| REQ-AEM-021 | DIR | traced | `tb/pp_top/sim_main.cpp:4458` | R1: a conflicting full command did not return BAD_ARGUMENTS | DIR |
| REQ-AEM-021 | DIR | traced | `tb/pp_top/sim_main.cpp:4513` | R7: duplicated REMOVE rows were not ignored safely | DIR |
| REQ-AEM-021 | DIR | traced | `tb/pp_top/sim_main.cpp:4548` | R10: running-output ADD recheck did not refuse the edit | DIR |
| REQ-AEM-021 | DIR | traced | `tb/pp_top/sim_main.cpp:4569` | R11a: required dynamic Stream Port Input was not supported | DIR |
| REQ-AEM-022 | DIR | traced | `tb/pp_top/sim_main.cpp:5907` | W8b: a missing descriptor is a per-record status | DIR |
| REQ-AEM-022 | DIR | traced | `tb/pp_top/sim_main.cpp:5923` | W8c: forbidden GET_AUDIO_MAP rejects the complete batch | DIR |
| REQ-AEM-022 | DIR | traced | `tb/pp_top/sim_main.cpp:5953` | W8d: overflow skips one record and continues with the next | DIR |
| REQ-AEM-023 | TOL | traced | `tb/pp_top/sim_main.cpp:2410` | A5: NOT_IMPLEMENTED echo is not byte-exact | TOL |
| REQ-AEM-023 | TOL | traced | `tb/pp_top/sim_main.cpp:2476` | A5b: %s: cdl | TOL |
| REQ-AEM-024 | TIM | traced | `tb/pp_top/sim_main.cpp:12289` | DL1: the forced response's first byte | TIM |
| REQ-AEM-024 | TIM | traced | `tb/pp_top/sim_main.cpp:12988` | TB2 oversize READ_DESCRIPTOR | TIM |
| REQ-AEM-024 | TIM | traced | `tb/pp_top/sim_main.cpp:12996` | TB2 GET_DYNAMIC_INFO with all thirteen getters | TIM |
| REQ-AEM-025 | RND | waived GAP-06 | `tb/aecp_notify/sim_main.cpp:798` | DR1b: C alone receives its own DEREGISTER | DIR |
| REQ-AEM-025 | RND | waived GAP-06 | `tb/pp_top/sim_main.cpp:4926` | U5d: sent only to this controller, once | TIM |
| REQ-AEM-025 | RND | waived GAP-06 | `tb/pp_top/sim_main.cpp:8728` | U10f: probe failure sends targeted deregistration | TIM |
| REQ-AEM-026 | TIM | traced | `tb/pp_top/notify_phases.hpp:246` | ID1: one press sends three IDENTIFY_NOTIFICATION | TIM |
| REQ-AEM-026 | TIM | traced | `tb/pp_top/notify_phases.hpp:278` | ID2d: burst | TIM |
| REQ-AEM-026 | TIM | traced | `tb/pp_top/sim_main.cpp:2492` | A6: the opcode-specific BAD_ARGUMENTS | DIR |
| REQ-MVU-001 | DIR | traced | `tb/pp_top/sim_main.cpp:2939` | M1: the response protocol_id is not 00-1B-C5-0A-C1-00 | DIR |
| REQ-MVU-001 | DIR | traced | `tb/pp_top/sim_main.cpp:3105` | M5: r = 1 was not echoed as NOT_IMPLEMENTED | DIR |
| REQ-MVU-002 | DIR | traced | `tb/pp_top/sim_main.cpp:2967` | M2: protocol_version | DIR |
| REQ-MVU-002 | DIR | traced | `tb/pp_top/sim_main.cpp:2969` | M2: features_flags | DIR |
| REQ-MVU-002 | DIR | traced | `tb/pp_top/sim_main.cpp:2973` | M2: certification_version | DIR |
| REQ-MVU-003 | DIR | waived GAP-03 | | | |
| REQ-MVU-004 | DIR | waived GAP-03 | | | |
| REQ-MVU-005 | TIM | traced | `tb/pp_top/sim_main.cpp:12382` | DL3: the queued GET_MILAN_INFO past its deadline | TIM |
| REQ-MVU-005 | TIM | traced | `tb/pp_top/sim_main.cpp:12922` | TB1 GET_MILAN_INFO | TIM |
| REQ-NOT-001 | STORM | traced | `tb/pp_top/notify_phases.hpp:1146` | ST1b: one change from row 15 reaches the other fifteen | STORM |
| REQ-NOT-001 | STORM | traced | `tb/pp_top/sim_main.cpp:4989` | U8c: only the other controller receives the changed name | DIR |
| REQ-NOT-002 | RND | traced | `tb/pp_top/notify_phases.hpp:1012` | exactly one unsolicited response of this | DIR |
| REQ-NOT-002 | RND | traced | `tb/pp_top/notify_phases.hpp:1636` | RN | RND |
| REQ-NOT-003 | STORM | traced | `tb/pp_top/notify_phases.hpp:1211` | ST2: descriptor | STORM |
| REQ-NOT-003 | STORM | traced | `tb/pp_top/notify_phases.hpp:1216` | ST2b: descriptor | STORM |
| REQ-NOT-003 | STORM | traced | `tb/pp_top/notify_phases.hpp:1356` | churn started | STORM |
| REQ-NOT-004 | TIM | traced | `tb/pp_top/sim_main.cpp:8702` | U10c: first probe arrived after | TIM |
| REQ-NOT-004 | TIM | traced | `tb/pp_top/sim_main.cpp:8718` | U10e: the single retry arrived after | TIM |
| REQ-NOT-004 | TIM | traced | `tb/pp_top/sim_main.cpp:8729` | U10f: probe failure sends targeted deregistration | TIM |
| REQ-NOT-004 | TIM | traced | `tb/pp_top/sim_main.cpp:8775` | U10k: response re-armed the monitor | TIM |
| REQ-NOT-005 | NVM | traced | `tb/pp_top/d3_phases.hpp:1181` | D3R1 volatile: the registry is empty after the restore | NVM |
| REQ-NOT-005 | NVM | traced | `tb/pp_top/d3_phases.hpp:3920` | D3V5: a third controller's change after the cycle notifies neither | NVM |
| REQ-MDL-001 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:287` | LintTest.test_mutations | DIR |
| REQ-MDL-002 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:288` | LintTest.test_mutations | DIR |
| REQ-MDL-003 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:289` | LintTest.test_mutations | DIR |
| REQ-MDL-004 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:290` | LintTest.test_mutations | DIR |
| REQ-MDL-005 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:291` | LintTest.test_mutations | DIR |
| REQ-MDL-005 | DIR | traced | `tb/pp_top/sim_main.cpp:7464` | W10e: SET_CLOCK_SOURCE | DIR |
| REQ-MDL-006 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:292` | LintTest.test_mutations | DIR |
| REQ-MDL-007 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:293` | LintTest.test_mutations | DIR |
| REQ-MDL-008 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:294` | LintTest.test_mutations | DIR |
| REQ-MDL-009 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:295` | LintTest.test_mutations | DIR |
| REQ-MDL-010 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:296` | LintTest.test_mutations | DIR |
| REQ-MDL-011 | DIR | traced | `tb/desc_store/test_gen_desc_image.py:297` | LintTest.test_mutations | DIR |
| REQ-PER-001 | NVM | traced | `tb/pp_top/d3_phases.hpp:1190` | D3R1 cfg: configuration 1 restored | NVM |
| REQ-PER-001 | NVM | traced | `tb/pp_top/d3_phases.hpp:1196` | D3R1 rate: 48000 restored | NVM |
| REQ-PER-001 | NVM | traced | `tb/pp_top/d3_phases.hpp:3275` | D3N3 ordinal | NVM |
| REQ-PER-001 | NVM | traced | `tb/pp_top/sim_main.cpp:10543` | BW2: a reset restores the same binding | NVM |
| REQ-PER-002 | NVM | traced | `tb/pp_top/d3_phases.hpp:1172` | D3R1 volatile: IDENTIFY reads 0 after the restore | NVM |
| REQ-PER-002 | NVM | traced | `tb/pp_top/d3_phases.hpp:1179` | D3R1 volatile: the lock is free after the restore | NVM |
| REQ-PER-002 | NVM | traced | `tb/pp_top/d3_phases.hpp:3903` | D3V3: IDENTIFY reads 0 in every cycle | NVM |
| REQ-PER-003 | NVM | traced | `tb/pp_top/d3_phases.hpp:1191` | D3R1 cfg: configuration 1 restored | NVM |
| REQ-NET-001 | DIR | traced | `tb/pp_top/sim_main.cpp:5600` | V1: GET_AVB_INFO byte-exact | DIR |
| REQ-NET-001 | DIR | traced | `tb/pp_top/sim_main.cpp:5620` | V2: GET_AS_PATH byte-exact | DIR |
| REQ-NET-001 | DIR | traced | `tb/pp_top/sim_main.cpp:5689` | V6: both gPTP notifications arrive on a GM change | DIR |
| REQ-NET-002 | DIR | traced | `tb/pp_top/notify_phases.hpp:1771` | <bench-switch-model>: the bridge's | DIR |
| REQ-NET-002 | DIR | traced | `tb/pp_top/sim_main.cpp:9306` | DV4: the bridge's | DIR |
| REQ-NET-002 | DIR | traced | `tb/pp_top/sim_main.cpp:10318` | S8: Domain Lv+New re-declaration byte-exact | DIR |
| REQ-NET-003 | DIR | traced | `tb/pp_top/gsi_internal.hpp:89` | failure code sink | DIR |
| REQ-NET-003 | DIR | traced | `tb/pp_top/sim_main.cpp:8892` | T1: Listener | DIR |
| REQ-NET-003 | DIR | traced | `tb/pp_top/sim_main.cpp:10336` | S8: acc_latency[2] latched | DIR |
| REQ-NET-004 | DIR | waived GAP-05 | | | |
| REQ-NET-005 | DIR | waived GAP-04 | | | |
| REQ-SRP-001 | TIM | traced | `tb/srp_top/sim_main.cpp:1939` | Q1: join-paced MRPDUs of one declaration are 180-240 ms apart | TIM |
| REQ-SRP-001 | TIM | traced | `tb/srp_top/sim_main.cpp:1966` | Q2: periodic! re-joins recur every 900-1500 ms | TIM |
| REQ-SRP-001 | TIM | traced | `tb/srp_top/sim_main.cpp:1993` | Q3: consecutive own LeaveAlls are 10-15 s apart | TIM |
| REQ-SRP-002 | TOL | traced | `tb/srp_decoder/sim_main.cpp:458` | I prefix 3 evts | TOL |
| REQ-SRP-002 | TOL | traced | `tb/srp_decoder/sim_main.cpp:519` | K only the Domain prefix | TOL |
| REQ-SRP-003 | DIR | traced | `tb/srp_encoder/sim_main.cpp:495` | E1 dual EndMark explicit ahead of MAC padding | DIR |
| REQ-SRP-004 | DIR | traced | `tb/pp_top/sim_main.cpp:9351` | DV6: LINK_UP re-declares Domain New | DIR |
| REQ-SRP-004 | DIR | traced | `tb/pp_top/sim_main.cpp:10062` | S1: Domain New {6,3,2} byte-exact | DIR |
| REQ-SRP-004 | DIR | traced | `tb/pp_top/sim_main.cpp:10319` | S8: Domain Lv+New re-declaration byte-exact | DIR |
| REQ-SRP-005 | MTXW | traced | `tb/srp_stream_fsms/sim_main.cpp:563` | immediate IN->MT | MTXW |
| REQ-SRP-005 | MTXW | traced | `tb/srp_stream_fsms/sim_main.cpp:721` | rLv -> unregistered | MTXW |
| REQ-SRP-006 | DIR | traced | `tb/pp_top/sim_main.cpp:10107` | S2: MVRP VID 2 New byte-exact | DIR |
| REQ-SRP-006 | DIR | traced | `tb/srp_top/sim_main.cpp:1803` | R1: the VID New leaves ahead of the first Talker Advertise | DIR |
| REQ-SRP-006 | DIR | traced | `tb/srp_top/sim_main.cpp:1843` | R4: DECLARE_LISTENER on VID 7 yields a byte-exact MVRP VID 7 New | DIR |
| REQ-MAAP-001 | RND | waived GAP-04 | `tb/maap/sim_main.cpp:334` | U1: block fits the Table B.9 pool | DIR |
| REQ-MAAP-001 | RND | waived GAP-04 | `tb/maap/sim_main.cpp:691` | U17: the probed block ends at or below 91:E0:F0:00:FD:FF | DIR |
| REQ-MAAP-002 | DIR | traced | `tb/maap/sim_main.cpp:340` | U1: PROBE byte-exact | DIR |
| REQ-MAAP-002 | DIR | traced | `tb/maap/sim_main.cpp:434` | U5: DEFEND byte-exact | DIR |
| REQ-MAAP-002 | DIR | traced | `tb/maap/sim_main.cpp:572` | U11: reserved message types change nothing | DIR |
| REQ-MAAP-002 | DIR | traced | `tb/maap/sim_main.cpp:591` | U13: a higher maap_version with a known type is still processed | DIR |
| REQ-MAAP-003 | MTXW | traced | `tb/maap/sim_main.cpp:349` | U2: 4 PROBEs + 1 ANNOUNCE on a cold walk | MTXW |
| REQ-MAAP-003 | MTXW | traced | `tb/maap/sim_main.cpp:365` | U2: probeCount! sends the ANNOUNCE immediately | MTXW |
| REQ-MAAP-003 | MTXW | traced | `tb/maap/sim_main.cpp:369` | U2: DEFEND state, claim valid at the probed base | MTXW |
| REQ-MAAP-004 | TIM | traced | `tb/maap/sim_main.cpp:357` | U2: probe interval | TIM |
| REQ-MAAP-004 | TIM | traced | `tb/maap/sim_main.cpp:380` | U3: announce interval | TIM |
| REQ-MAAP-005 | MTXW | traced | `tb/maap/sim_main.cpp:439` | U5: defended, nothing yielded | MTXW |
| REQ-MAAP-005 | MTXW | traced | `tb/maap/sim_main.cpp:479` | U7: claim kept | MTXW |
| REQ-MAAP-005 | MTXW | traced | `tb/maap/sim_main.cpp:493` | U8: yielded | MTXW |
| REQ-MAAP-005 | MTXW | traced | `tb/maap/sim_main.cpp:533` | U9: compare_MAC TRUE | MTXW |
| REQ-MAAP-005 | MTXW | traced | `tb/maap/sim_main.cpp:557` | U10: PROBE-state rDefend! yields, no tie-break | MTXW |
| REQ-MAAP-005 | MTXW | traced | `tb/maap/sim_main.cpp:928` | U20: compare_MAC TRUE | MTXW |
| REQ-MAAP-006 | DIR | traced | `tb/maap/sim_main.cpp:435` | U5: DEFEND byte-exact | DIR |
| REQ-MAAP-006 | DIR | traced | `tb/maap/sim_main.cpp:455` | U5b: conflict_start is the first ALLOCATED address | DIR |
| REQ-MAAP-007 | DIR | traced | `tb/maap/sim_main.cpp:613` | U14: Release! sends NOTHING | DIR |
| REQ-MAAP-007 | DIR | traced | `tb/maap/sim_main.cpp:1472` | U28: no new TX slot request follows the fall | DIR |
| REQ-SCP-001 | DIR | waived GAP-12 | | | |
| REQ-SCP-002 | DIR | traced | `tb/pp_top/sim_main.cpp:2970` | M2: features_flags | DIR |
| REQ-SCP-003 | DIR | traced | `tb/adp_engine/sim_if2.cpp:345` | IF3: interface 1's link comes up | DIR |
| REQ-SCP-003 | DIR | traced | `tb/pp_top/interface_phases.hpp:176` | IF1: with two interfaces each advertise machine | DIR |
| REQ-SCP-003 | DIR | traced | `tb/pp_top/interface_phases.hpp:238` | IF3: C's REGISTER on interface 1 | DIR |
| REQ-REU-001 | — | no check | | | |
| REQ-REU-002 | lint | no check | | | |
| REQ-REU-003 | — | no check | | | |
| REQ-VER-001 | — | no check | | | |
| REQ-VER-002 | lint | no check | | | |
| REQ-FWX-001 | DIR | traced | `tb/pp_top/sim_main.cpp:2467` | A5b: %s: the response is not the echoed command | DIR |
| REQ-DOC-001 | lint | no check | | | |
req-tags: 115 REQ rows: 101 traced, 8 waived, 6 need no check; 225 tags in 18 files, OK
