# [A596] #72 requirement-to-test traceability: HANDOFF

Status: **REVIEW READY** under the lane owner's ruling (issue #72 comment 6101430201: option 1,
the `REQ_TAG_LOG` evidence design, the `make check` / suites-job split). Not pushed.

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` confirmed)
- Lane: branch `pp72-traceability`, base main `2cbed0a987c1e68402658d69459ab7e5aa571adc` (re-confirmed
  on resume: `origin/main` and HEAD both `2cbed0a9`, worktree clean, no commit on the branch)
- Assignment: issue #72 comment 6100765289 (lane owner [A10]; executor [A596]; reviewers [R610], [R611])
- Ruling: issue #72 comment 6101430201
- Posted on #72: `[A596] TAKEN` (6100771683), `[A596] STOP` (6100887655), `[A596] REVIEW READY` at `9540c34` (6104271127)
- Head: `9540c34526c611a4f8ebac2e1b9dac890727e155` (four commits on `2cbed0a9`)

| Commit | Subject | Files |
|---|---|---|
| `a5bc371` | Tag the checks that verify each REQ row with the row and its Ver category | `tb/common/req_tag.hpp`, `tb/common/req_tag.py` (new); 18 suite sources |
| `ae9f0bb` | Gate requirement-to-test traceability in make check and record coverage in 00 and 09 | `scripts/check-req-tags.py` (new), `Makefile`, `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/09_verification.md` |
| `8b35915` | Run the traceability gate's executed half on the suites job's own run | `.github/workflows/hdl.yml` |
| `9540c34` | State what the tags leave unchanged in a suite log, and the prng draw check, in 09 section 8.10 | `docs/architecture/09_verification.md` (text only) |

## 1. What the lane built

- **The tag.** `REQ_TAG("REQ-NOT-001", "STORM", "ST1b");` on its own line directly above the check it
  labels, one per row the check verifies (`tb/common/req_tag.hpp`; a Python test calls
  `tb/common/req_tag.py`'s `REQ_TAG` at the head of the test method, named `Class.method`). With
  `REQ_TAG_LOG` unset or empty it does nothing. Set, the first time a tag runs in a process it appends
  `suite file:line REQ CAT` to that file; the suite is the run's working directory (the ruling's
  design). Every campaign driver copies `tb/common` beside the suites it builds, so the new header
  builds in their scratch copies too.
- **The gate**, `scripts/check-req-tags.py`:
  - static half, in `make check` as `reqtags` right after `matrix` (so the CI docs-gates job, which
    has no simulator): every row whose Ver is DIR, MTXW, TOL, TIM, RND, STORM or NVM has a tag of its
    own category or a waiver in 09 §8.10 naming one of its own Finding GAPs and a reason; tags
    well-formed, inside a suite, naming a known REQ and category, and standing above a check whose
    statement holds the tag's name (Python: `Class.method` of the test); no stale waiver; the Cov
    column and the 09 §8.10 coverage table equal what the gate finds;
  - executed half, `--suites LOG --evidence FILE`, in the CI suites job on that job's own
    `run_suites.sh` run made with `REQ_TAG_LOG`: every tag's suite PASS in that run and every tag's
    evidence line present; an evidence line no tag accounts for fails (stale file);
  - `--table` (the coverage table below), `--selftest` (29 planted cases, run first by `make check`).
- **Records.** 00 §6 Cov cells end with `; traced`, `; waived GAP-nn` or `; no check` and the column
  key says so; 09 §8.10 holds the coverage table and the eight waivers; 09 §2 points at it, §7 lists
  `reqtags`, §8's "To add ... REQ-ID ↔ test-tag coverage" is gone; F00.2 GAP-11 "Verified by" names
  the gate; a GAP-11 landed note; the REQ-VER-001 row names the tags and 09 §8.10.
- **Stale "DOES NOT EXIST" wording**: the tree's own docs do not carry it (it is in issue #72's body,
  the 09-18 audit). 09 §8.10 states which RND/STORM rows the §8.4 suites trace and which are waived.
- No RTL, register map, port, parameter or check behaviour changed: no check's condition, label or
  count moved (records below).
- Left as they are, outside the lane's scope (tags, gate, CI, the docs that record coverage): the
  HDL engineer guide's §8 list of what `make check` covers does not name `reqtags` (it points at 09
  §7, which does), and the README's one-line `make check` summary.
- Choices a reviewer may question: the MDL rows and ADP-003/004 trace to the packer lint's tests
  (`LintTest.test_mutations` holds one refusal per L1 to L12 check, `IdentityTest` the driven ADP
  values), not to an RTL check, since the model is the consumer's (07 §3.1); the integrator-owned
  rows (AEM-019, NET-004, NET-005) and the two waived MVU commands are waived rather than traced to
  the checks of the processor's own half (K9 to K11, AS2/W23a2, M4), which grade the face, not the
  requirement.

## 2. Coverage at head (`python3 scripts/check-req-tags.py --table`)

Gate summary: `req-tags: 115 REQ rows: 101 traced, 8 waived, 6 need no check; 225 tags in 18 files, OK`.

- traced: 101 of the 109 rows whose Ver needs a check. RND: AEM-005 (`tb/originator` R), AEM-016 and
  NOT-002 (`tb/pp_top` RN). STORM: NOT-001 (ST1b), NOT-003 (ST2, ST2b, CS).
- waived (09 §8.10, each naming its own row's GAP and a reason): AEM-019 GAP-05, AEM-025 GAP-06,
  MAAP-001 GAP-04, MVU-003 GAP-03, MVU-004 GAP-03, NET-004 GAP-05, NET-005 GAP-04, SCP-001 GAP-12.
  AEM-025 and MAAP-001 also carry tags of other categories (TIM/DIR) that label their directed checks.
- not requiring a check: REU-001, REU-003, VER-001 (Ver —); REU-002, VER-002, DOC-001 (Ver lint).

`file:line` is the tag's line; the check is the statement directly below it (for a Python tag, the
test method it heads).

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

## 3. Planted defects (each in the lane tree at `8b35915`, gated, then restored with `git checkout`)

| # | Defect (diff) | Gate run | rc | Failing gate words |
|---|---|---|---|---|
| 1 | tag removed so its row is uncovered: `REQ-AEM-005`'s one RND tag deleted from `tb/originator/sim_main.cpp` | `make reqtags`; `python3 scripts/check-req-tags.py` | 2; 1 | `REQ TAG FAIL: UNCOVERED REQ-AEM-005 (RND): no tagged RND check and no waiver` |
| 2 | tag to an unknown REQ: `REQ-ADP-008` → `REQ-ADP-099` on `tb/adp_engine/sim_main.cpp` P8 | same | 2; 1 | `REQ TAG FAIL: UNKNOWN REQ REQ-ADP-099 tb/adp_engine/sim_main.cpp:964: no matrix row has that ID` |
| 3 | tag moved onto a check that never runs: `REQ-FWX-001`'s one DIR tag moved from the A5b sweep of the default run onto the A5b call in `run_aecp_dispatch_focus`, which only `--aecp-dispatch-only` runs | static half; then `REQ_TAG_LOG=… ./scripts/run_suites.sh` and the executed half | 0 (static, as designed); run_suites 0 (output identical to base); executed 1 | `REQ TAG FAIL: DEAD TAG REQ-FWX-001 tb/pp_top/sim_main.cpp:11078: "a5b_not_implemented_is_sized_by_its_command" never ran in this run` |
| 4 | waiver without a GAP: the GAP cell of the real `REQ-AEM-025` waiver emptied (09 §8.10) | `make reqtags`; gate | 2; 1 | `REQ TAG FAIL: WAIVER WITHOUT GAP REQ-AEM-025: the waiver names no GAP` |
| 5 | REQ row added with no tag: `REQ-AEM-027` (DIR, GAP-06) after REQ-AEM-026 in 00 §6 | `make reqtags`; gate | 2; 1 | `REQ TAG FAIL: UNCOVERED REQ-AEM-027 (DIR): no tagged DIR check and no waiver` |

After the restore: worktree clean, `python3 scripts/check-req-tags.py` rc 0. The self-test plants the
same five plus 23 more faults (one per finding the gate can name) in a scratch tree: `req-tags
selftest: 29 cases, OK` (case 1 is the clean fixture).

## 4. Base/head records

Same toolchain both sides (§7). Each gate in its own job, stdout and stderr to its own log, never
piped. The head column was recorded at `8b35915` and again at the final head `9540c34` (whose only
change is 09 §8.10's text): every head log below is byte-identical at both, and so are the
`REQ_TAG_LOG` run and the executed half.

| Gate (as run from the repository root) | Base rc | Head rc | Head log bytes | Head log sha256 | Base vs head |
|---|---|---|---|---|---|
| `./scripts/run_suites.sh` | 0 | 0 | 1799 | `b1205c5d8cfb979eb93a54b692587924790bdf4c4de46ddf82547223d37c36f5` | byte-identical (34 PASS, `suites: 1029620 checks total, 0 failing`) |
| `REQ_TAG_LOG=<file> ./scripts/run_suites.sh` | – | 0 | 1799 | `b1205c5d…` | byte-identical to the base record |
| `./scripts/lint_hdl.sh` | 0 | 0 | 1056 | `9a3703ba1ec6767b277e9d5102c94a93fe107454da19d13cab518ba312cd1e81` | byte-identical |
| `make check` | 0 | 0 | 530 | `07aab597208aac035abe83c566c53683b1ac495022247a09c0a68055ea052bab` | every base line kept; two lines added after `matrix` (`req-tags selftest: 29 cases, OK`, `req-tags: 115 REQ rows: …, OK`); `ids: 563 files` → `565 files` (the two new files under `tb/common`). `links: 1187` unchanged |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | 33 | `7a2c98136a0892f195fa6a08ad82dfe7e36e8a81d0732cb304584f31e966e097` | byte-identical |
| `python3 scripts/check-matrix.py` | 0 | 0 | 42 | `79c6631c9c7b55437f89ef2b8d2ab3288f11aabf5a6a7800ccba1d6e8ef55629` | byte-identical |
| `./syn/yosys/run.sh` | 0 | 0 | 3548 | `0d19590fe9dd620eaca603688e9f8c79523ba022c732f98e136ae1ed72b68387` | byte-identical |
| executed half: `python3 scripts/check-req-tags.py --suites … --evidence …` | – | 0 | | | `req-tags executed: 225 evidence lines, 13 suites, OK` (230 lines written, 225 distinct: a tag in a header runs in more than one build) |

**Per-suite logs.** `run_suites.sh` deletes each suite's log, so each suite's `make` was also run
with its log kept, from clean build directories (`git clean -fdX tb/`) at base and at head. All 34
exit 0 on both sides. Every line a suite prints is identical in all 34; one log is byte-identical
and 202 raw lines differ, every one build-tool output (compiler command lines, Verilator's
`- Verilator: Walltime …` report, parallel compile order) or the `desc_store` unittest duration
(`Ran 59 tests in 2.017s`). A first base pass reused the head's build directories and 12 suites
stopped at `No rule to make target '../../common/req_tag.hpp'` (the head's dependency files name the
new header); that is the build cache of one tree switched between commits, cleared by `make clean`,
and the pass was discarded.

Per-suite tallies (identical at base and head):

| Suite | Checks | Suite | Checks |
|---|---|---|---|
| acmp_listener | 3167 | acmp_nvm | 388 |
| acmp_talker | 1376 | adp_engine | 1359 |
| aecp_notify | 67 | ca_originator | 16 |
| desc_mem_guard | 78 | desc_store | 586 |
| dispatch | 211 | dyn_state | 118 |
| event_router | 81 | lsn_admit | 18 |
| maap | 196 | name_state | 1236 |
| nvm_port | 1219 | originator | 107 |
| pp_top | 10470 | prng | 76 |
| release_merge | 18 | resp_buf | 64 |
| rx_slots | 130 | rx_validator | 555 |
| scoreboard | 3705 | side_port | 368 |
| srp_admission | 991231 | srp_decoder | 190 |
| srp_encoder | 581 | srp_stream_fsms | 1347 |
| srp_top | 8656 | timer_map | 1360 |
| timer_service | 48 | tx_arbiter | 66 |
| tx_slots | 95 | ucpu | 437 |

## 5. Campaigns that build a changed file (base `2cbed0a9`, head `8b35915` / `9540c34`)

Each campaign driver was run with `--jobs` (3 at base; 2 at head, beside the base runs) and its own
`--output` in the scratch area. Base ran in the scratch parent's processor submodule at `2cbed0a9`.
Head ran from the lane at `8b35915` (srp_top to d3) and from the submodule at `9540c34` (acmp to
desc_mem_guard). The two heads' `tb/`, `hdl/` and `scripts/` are identical. The logs were compared
with the output directory's label normalised. Four drivers print each arm's verdict as it finishes,
so their line order follows `--jobs` and timing; for those, the two logs hold the same lines.

| Campaign (driver) | Builds a changed file | Base rc / s | Head rc / s | Head result | Base vs head |
|---|---|---|---|---|---|
| `tb/srp_top/mutants.py` | `tb/srp_top`, `srp_stream_fsms`, `srp_encoder` sources | 0 / 1190 | 0 / 1680 | `137 checks: 137 PASS, 0 FAIL` (assertion coverage 86/86) | byte-identical |
| `tb/maap/mutants.py` | `tb/maap`, `tb/pp_top` | 0 / 114 | 0 / 137 | `32 checks: 32 PASS, 0 FAIL` | byte-identical |
| `tb/adp_engine/mutants.py` | `tb/adp_engine`, `tb/pp_top` | 0 / 280 | 0 / 385 | `62 checks: 62 PASS, 0 FAIL` | byte-identical |
| `tb/pp_top/aecp_mutants.py` | `tb/pp_top` | 0 / 697 | 0 / 1036 | `67 checks: 67 PASS, 0 FAIL` | byte-identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | `tb/pp_top` | 0 / 547 | 0 / 722 | `44 checks: 44 PASS, 0 FAIL` | byte-identical |
| `tb/pp_top/ctr_mutants.py` | `tb/pp_top` | 0 / 199 | 0 / 257 | `18 checks: 18 PASS, 0 FAIL` | byte-identical |
| `tb/pp_top/notify_mutants.py` | `tb/pp_top` | 0 / 1033 | 0 / 1358 | `93 of 93 KILLED by their named checks; goldens PASS` | same lines (completion order) |
| `tb/pp_top/d3_mutants.py` | `tb/pp_top` | 0 / 4515 (rerun) | 0 / 6255 | `110 of 110 KILLED by their named checks; goldens PASS` | same lines (completion order) |
| `tb/pp_top/acmp_mutants.py` | `tb/pp_top`, `tb/acmp_listener` | 0 / 1497 | 0 / 1973 | `51 of 51 KILLED by their named checks; goldens PASS` | same lines (completion order) |
| `tb/pp_top/gsi_mutants.py` | `tb/pp_top` | 0 / 747 | 0 / 841 | `20 detected by named checks; golden and restored PASS` | byte-identical |
| `tb/pp_top/name_wr_mutant.py` | `tb/pp_top` | 0 / 76 | 0 / 84 | `decode killed; golden and restored PASS` | byte-identical |
| `tb/name_state/mutants.py` | `tb/pp_top/sim_main.cpp` (`tb/name_state` includes it) | 0 / 278 | 0 / 354 | 16 of 16 arms `KILLED` | same lines (completion order) |
| `tb/srp_admission/mutants.py` | `tb/srp_top` | 0 / 442 | 0 / 458 | `12 checks: 12 PASS, 0 FAIL` | byte-identical |
| `tb/acmp_talker/retry_mutants.py` | `tb/acmp_talker` | 0 / 165 | 0 / 228 | `62 mutants killed; 7 equivalence controls; 1 performance controls` | byte-identical |
| `tb/desc_store/lint_suppression.py` | `tb/desc_store/test_gen_desc_image.py` | 0 / 27 | 0 / 24 | `56 of 56 checks killed` | byte-identical |
| `tb/desc_mem_guard/mutate.py` | none (run for completeness) | 0 / 5 | 0 / 5 | `completed byte assertion detected=True` | byte-identical |

Not run: `make -C tb/nvm_port figures`. It builds no changed file: `tb/nvm_port` is untouched, and
the new `tb/common/req_tag.*` files are copied into its work tree but never compiled.

The first base `d3_mutants.py` run ended at 00:03:16 with rc 143. An external SIGTERM reached it after
100 arms had all been KILLED; this host also runs other lanes' campaigns and memory guards. That run
was discarded. The rerun above completed all 110 arms, at base, from the same submodule. When the
lane's head driver finished d3, it was stopped, because the submodule had already run the remaining
head campaigns.

## 6. Scratch parent

Scratch parent: `kebag-logic/milan-fpga` `dev` at `e8454e2751d05b02ee8e5a571857589ab358abf6`
(`git rev-parse e8454e27`), cloned in the scratch area, never committed or pushed. Initialised
submodules: `protocol-processor`, `gptp-processor` (`5dce647a`, its gitlink) and
`third_party/verilog-axis` (`48ff7a7e`, its gitlink; the source-list gates need it). The parent's own
gitlink pins the processor at `2ad2f845`; for the records it was set in the index only (never
committed) to `2cbed0a9` (base) and to `9540c34` (head), with the submodule checked out at the
same commit, so `git submodule status` reads the pinned form the code-quality scope requires.

These are the parent's gates that read processor files (its idiom, hygiene, TODO, test-evidence,
control-flow, naming, fail-fast, submodule-docs and source-list gates; its suite runner runs no
processor suite). No parent adoption is proposed. The processor files the parent reads that change
are `tb/` C++ and Python, `scripts/`, `Makefile` and `.github/workflows/hdl.yml`; every gate below
gives the same rc at base and head:

| Gate (from the parent root) | Base rc | Head rc | Base vs head |
|---|---|---|---|
| `python3 scripts/measure_control_flow.py` | 0 | 0 | function count 6261 → 6280 (protocol-processor 366 → 385: the gate script and the Python tag); depth-5 count unchanged (23; protocol-processor 3) |
| `python3 scripts/measure_control_flow.py --selftest` | 0 | 0 | byte-identical |
| `python3 scripts/check_cpp_idiom.py` | 0 | 0 | 340 → 341 translation units (`tb/common/req_tag.hpp`); every ratchet 0 ≤ 0, no refusal |
| `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 0 | byte-identical |
| `python3 scripts/measure_fail_fast.py --check` | 0 | 0 | byte-identical |
| `python3 scripts/check_hygiene.py --check` | 0 | 0 | 1126 → 1129 files scanned (protocol-processor 196 → 199: the three new files); `HYGIENE RATCHET: PASS` |
| `python3 scripts/check_hygiene.py --selftest` | 0 | 0 | byte-identical |
| `python3 scripts/measure_naming.py --check` | 0 | 0 | byte-identical |
| `python3 scripts/check_port_contracts.py` | 0 | 0 | byte-identical |
| `python3 scripts/pp_srcs.py --check` | 0 | 0 | byte-identical |
| `python3 scripts/check_py_idiom.py` | 0 | 0 | 382 → 384 modules, 216545 → 217166 lines (the gate script, `tb/common/req_tag.py`); every ratchet holds |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | 0 | byte-identical |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 0 | byte-identical |
| `python3 scripts/check_sh_idiom.py` | 0 | 0 | byte-identical |
| `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0 | byte-identical |
| `python3 scripts/check_soc_sources.py` | 0 | 0 | byte-identical |
| `python3 scripts/check_submodule_docs.py` | 1 | 1 | identical: `protocol-processor: documented pin differs from Git` and the stale diagram, which any gitlink off the documented `2ad2f845` gives (as at base) |
| `python3 scripts/measure_test_evidence.py --check` | 1 | 1 | identical: `1 unexplained DUT-source reader(s) > ratchet 0` (`protocol-processor/tb/name_state/mutants.py`, at base too) |
| `python3 scripts/measure_test_evidence.py --selftest` | 1 | 1 | identical: the same reader, 104 of 105 |
| `python3 scripts/check_todo_ownership.py` | 0 | 0 | 1186 → 1189 files read; 0 markers |
| `python3 scripts/check_todo_ownership.py --selftest` | 0 | 0 | byte-identical |

The three non-zero gates fail identically at base: they are the state of processor `2cbed0a9`
against parent `dev`, not this lane.

## 7. Toolchain

| Tool | Identity |
|---|---|
| Verilator | 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`), the pinned wrapper; host default 5.052 not used |
| sv2v | 0.0.13 (sha256 `b80a8ac6212aa72a196d9d6129cda35f16dbfa799ec61848c46321f845b6b635`) |
| Yosys | 0.66 (`git sha1 86f2ddebc-dirty`), sha256 `ec566d8fbb0d24e09ce7ab4e86c55c7169f24097d90611ee354b446925f36b5b` |
| WaveDrom | 2.0.3.post3 (the CI pin) |
| Mermaid CLI | 11.16.0 (the CI pin) |
| Python | 3.14.7 |

The brief places the CI-pinned sv2v 0.0.12 and Yosys under the shared tools directory; neither is
there (rechecked on this resume). With sv2v 0.0.12 `tb/nvm_port` fails its `MAX_PAYLOAD_P=65528`
synthesis guard at base (Yosys prints `ERROR: FATAL: .` instead of the guard's `$finish`); with
0.0.13, which CI's portability job installs (`releases/latest`), it passes. The suites job installs no
sv2v, so the guard prints `YOSYS SKIP` there. Base and head both use 0.0.13.

## 8. The STOP and the ruling (history)

First session: STOP at `2cbed0a9` (comment 6100887655) because the scope bullet waiving RND and STORM
as "no suite today" contradicted the tree (RN, ST, CS and `tb/originator` R exist since #80). The
lane owner's ruling (6101430201) chose option 1 with the evidence design and the CI split. The STOP's
evidence table, kept for reference:

The assignment's scope bullet reads: "The categories with no suite today (RND, STORM:
GAP-06, GAP-17) become explicit waiver rows naming their GAPs, never silent passes."
At `2cbed0a9` both categories have suites, and the tree's coverage docs record them:

| Evidence | Where |
|---|---|
| 09 section 8.4 lists STORM: `tb/pp_top` ST, CS; RND: `tb/pp_top` RN, `tb/originator` R | `docs/architecture/09_verification.md:311-316` |
| GAP-06 landed note: "The RND and STORM suites this finding names exist (sections RN and ST)" | `docs/00_MILAN_COMPLIANCE_REVIEW.md:202-203` |
| F00.2 GAP-06 "Verified by": RND/STORM/TIM: `tb/pp_top` RN, ST, ID, NP | `docs/00_MILAN_COMPLIANCE_REVIEW.md:550` |
| F00.2 GAP-17 "Verified by": RND: `tb/originator` R | `docs/00_MILAN_COMPLIANCE_REVIEW.md:561` |
| ST, RN and CS run in `tb/pp_top`'s default build (no section flag) | `tb/pp_top/sim_main.cpp:14116-14118`; `tb/pp_top/Makefile` `run` |
| R runs unconditionally in `tb/originator` | `tb/originator/sim_main.cpp:911` |
| Issue #72's "DOES NOT EXIST" was audited at `6a878f6` (2026-09-18); lane C6 landed RN/ST on 2026-09-30 (#80) | issue #72 body; 00 GAP-06 note |

Following the bullet literally means publishing waivers that say RND and STORM have no
suite. That contradicts 09 section 8.4 and the 00 GAP-06 and GAP-17 records. Tracing
those rows instead departs from an explicit scope bullet. The choice belongs to the
lane owner, so the lane stopped before any edit.

### The seven RND/STORM rows against the checks the tree has

| REQ | Ver | Row's GAP | Check of that category (file:line, check name) |
|---|---|---|---|
| REQ-NOT-001 | STORM | GAP-06 | `tb/pp_top/notify_phases.hpp:1143` ST1b: one change from row 15 reaches the other fifteen rows byte-exact, each at its own sequence_id |
| REQ-NOT-003 | STORM | GAP-06 | `tb/pp_top/notify_phases.hpp:1207` ST2, `:1211` ST2b (GET_COUNTERS at most one round per descriptor per second); `:1350` CS2a-c |
| REQ-AEM-016 | RND | GAP-06 | `tb/pp_top/notify_phases.hpp:1628` RN: 720 seeded steps from 20 controllers against the registry model (capacity 16, NO_RESOURCES, sequence_id from 0, a refresh keeps it) |
| REQ-NOT-002 | RND | GAP-06 | `tb/pp_top/notify_phases.hpp:1628` RN: every successful SET pushes to each registered controller but the requester |
| REQ-AEM-005 | RND | GAP-17 | `tb/originator/sim_main.cpp:881` R: 16 owners' CONTROLLER_AVAILABLE-shaped inflights, one re-send then fail, against `IflModel` |
| REQ-AEM-025 | RND | GAP-06 | none randomized: RN stays under the monitor's 30 s floor (`notify_phases.hpp:1636` RN c) and never auto-removes; directed only (`tb/aecp_notify` DR) |
| REQ-MAAP-001 | RND | GAP-04 | none randomized: `tb/maap` U17/U18 grade the Table B.9 fit with a stubbed draw |

REQ-MAAP-001's own finding is GAP-04, not GAP-06 or GAP-17, which is another sign the
bullet was written from the issue's 2026-09-18 audit text.

### Options put to the lane owner (comment 6100887655)

1. *Recommended:* every tag names its REQ and the Ver category of the check it labels.
   Only an executed check of the row's own category traces a row. Any other row needs
   a waiver with a GAP and a reason, or the gate fails. NOT-001, NOT-003, AEM-016,
   NOT-002 and AEM-005 are then traced. AEM-025 (GAP-06) and MAAP-001 (GAP-04) are
   waived, along with any other row found to lack a check of its category.
2. *Literal:* all seven rows waived, naming GAP-06 or GAP-17 (MAAP-001 naming GAP-04).
   RN, ST, CS and R stay untagged, and 09 section 8 has to say why they do not count.
3. As option 1, but without categories: any executed tag traces a row, and only rows
   with no check at all are waived.

### The design proposed under any option

- *Executed evidence.* `scripts/run_suites.sh` prints one tally line per suite and
  deletes each suite's log (`run_suites.sh:38-53`), so its output cannot show that a
  single check ran. Proposal: a tag is a statement next to its check. When `REQ_TAG_LOG`
  is set it appends `suite file:line REQ CAT` to that file; when unset (every existing
  invocation) it does nothing. The gate runs `run_suites.sh` with the variable set, then
  requires each tag's suite to PASS in that output and the tag to be in the evidence.
  `run_suites.sh`, check counts and suite logs stay byte-identical. Tags in headers
  (`notify_phases.hpp`, `d3_phases.hpp`) are covered too, because evidence carries
  `__FILE__` basename and `__LINE__`, with the suite taken from the run's working directory.
- *CI.* The static half (REQ rows and Ver categories from 00 section 6, tags, unknown
  REQs, waivers needing a GAP and a reason) goes in `make check` beside
  `check-matrix.py`, since the docs-gates job has no Verilator. The executed half goes
  in the suites job, reading that job's own `run_suites.sh` output.
- Existing informal REQ mentions in `tb/` comments (for example
  `tb/srp_top/sim_main.cpp:1757`, `tb/pp_top/notify_phases.hpp:167`) must not count as
  tags, so the tag syntax has to be distinct from prose.

The base records above were recorded in the first session (2026-10-10 21:06:37 CEST) with the same
toolchain; this session re-ran nothing at base for them, because main had not moved.
