[A284]

Closes #116

Every before/after value below is required to match. Raw logs and command exit statuses are retained in the corresponding directories.

Suite counts (all failures zero):

| Suite | Before | After |
|---|---:|---:|
| acmp_listener | 2544 | 2544 |
| acmp_nvm | 349 | 349 |
| acmp_talker | 839 | 839 |
| adp_engine | 533 | 533 |
| aecp_notify | 10 | 10 |
| ca_originator | 16 | 16 |
| desc_mem_guard | 78 | 78 |
| desc_store | 584 | 584 |
| dispatch | 211 | 211 |
| dyn_state | 89 | 89 |
| event_router | 81 | 81 |
| lsn_admit | 18 | 18 |
| maap | 75 | 75 |
| nvm_port | 136 | 136 |
| originator | 104 | 104 |
| pp_top | 1948 | 1948 |
| prng | 76 | 76 |
| release_merge | 18 | 18 |
| resp_buf | 64 | 64 |
| rx_slots | 130 | 130 |
| rx_validator | 393 | 393 |
| scoreboard | 3705 | 3705 |
| side_port | 368 | 368 |
| srp_admission | 991231 | 991231 |
| srp_decoder | 190 | 190 |
| srp_encoder | 556 | 556 |
| srp_stream_fsms | 1087 | 1087 |
| srp_top | 1531 | 1531 |
| timer_map | 1360 | 1360 |
| timer_service | 48 | 48 |
| tx_arbiter | 66 | 66 |
| tx_slots | 95 | 95 |
| ucpu | 386 | 386 |

suites: 1008919 checks total, 0 failing

Admission shapes:

| Sources | Before checks/pass/fail | After checks/pass/fail |
|---|---|---|
| 1 | 1138/1138/0 | 1138/1138/0 |
| 2 | 12615/12615/0 | 12615/12615/0 |
| 3 | 41012/41012/0 | 41012/41012/0 |
| 5 | 201073/201073/0 | 201073/201073/0 |
| 8 | 991231/991231/0 | 991231/991231/0 |

Descriptor mutation:

| Variant | Before | After |
|---|---|---|
| hold-deleted | rc 2, detected; 18/17/1 | rc 2, detected; 18/17/1 |

GSI campaign (build/run exit status; checks/failures):

| Variant | Before | After |
|---|---|---|
| golden | 0/0; 488/0; PASS | 0/0; 488/0; PASS |
| failure-code-zero | 0/1; 488/20; PASS | 0/1; 488/20; PASS |
| failure-bridge-zero | 0/1; 488/20; PASS | 0/1; 488/20; PASS |
| pbsta-zero | 0/1; 488/110; PASS | 0/1; 488/110; PASS |
| acmpsta-zero | 0/1; 488/20; PASS | 0/1; 488/20; PASS |
| wrong-sink | 0/1; 488/142; PASS | 0/1; 488/142; PASS |
| integrator-path | 0/1; 158/98; PASS | 0/1; 158/98; PASS |
| missing-descriptor-leak | 0/1; 488/4; PASS | 0/1; 488/4; PASS |
| status-notification-zero | 0/1; 348/97; PASS | 0/1; 348/97; PASS |
| rebind-started-trigger-removed | 0/1; 483/3; PASS | 0/1; 483/3; PASS |
| failure-change-strobe-removed | 0/1; 483/2; PASS | 0/1; 483/2; PASS |
| failure-change-redeclares | 0/1; 488/1; PASS | 0/1; 488/1; PASS |
| index-guard-removed | 0/1; 488/2; PASS | 0/1; 488/2; PASS |
| bridge-gate-removed | 0/1; 488/4; PASS | 0/1; 488/4; PASS |
| restored | 0/0; 488/0; PASS | 0/0; 488/0; PASS |

All named-failure arrays in the two `results.json` files are identical.

SRP campaign (run exit status; checks/pass/fail):

| Variant / suite | Before | After |
|---|---|---|
| control / admission-2 | 0; 12615/12615/0; PASS | 0; 12615/12615/0; PASS |
| control / admission-8 | 0; 991231/991231/0; PASS | 0; 991231/991231/0; PASS |
| control / srp-top | 0; 1531/1531/0; PASS | 0; 1531/1531/0; PASS |
| stale-evaluation / admission-2 | 2; 12615/12213/402; PASS | 2; 12615/12213/402; PASS |
| stale-evaluation / admission-8 | 2; 991231/985758/5473; PASS | 2; 991231/985758/5473; PASS |
| stale-evaluation / srp-top | 2; 1531/1426/105; PASS | 2; 1531/1426/105; PASS |
| pending-absent / admission-2 | 2; 12615/12440/175; PASS | 2; 12615/12440/175; PASS |
| pending-absent / admission-8 | 2; 991231/990164/1067; PASS | 2; 991231/990164/1067; PASS |
| pending-absent / srp-top | 2; 1531/1326/205; PASS | 2; 1531/1326/205; PASS |
| discarded-round-strobes / admission-2 | 2; 12615/12469/146; PASS | 2; 12615/12469/146; PASS |
| discarded-round-strobes / admission-8 | 2; 991231/990536/695; PASS | 2; 991231/990536/695; PASS |
| discarded-round-strobes / srp-top | 2; 1531/1441/90; PASS | 2; 1531/1441/90; PASS |

NVM figure campaign (complete output also byte-identical):

| Arm, mutation, model or matrix row | Before | After |
|---|---|---|
| 222 S_WEREQ | 0 | 0 |
| 231 S_WEWAIT | 76 | 76 |
| 241 S_WWREQ | 0 | 0 |
| 251 S_WHPUMP | 64 | 64 |
| 264 S_WDPUMP | 52 | 52 |
| 274 S_WWAIT | 39 | 39 |
| 285 S_RHREQ | 2 | 2 |
| 295 S_RHCOLL | 43 | 43 |
| 313 S_RHWAIT | 38 | 38 |
| 340 S_RPREQ | 0 | 0 |
| 350 S_RPPUMP | 71 | 71 |
| 360 S_RPWAIT | 26 | 26 |
| M1 | 24 | 24 |
| M1-sibling | 5 | 5 |
| M2 | 8 | 8 |
| M3 | 105 | 105 |
| M4 | 52 | 52 |
| M5 | 39 | 39 |
| M6 | 6 | 6 |
| M6-sibling | 5 | 5 |
| probe-armearly | 1 | 1 |
| probe-nodevice | 3 | 3 |
| probe-t18 | 3 | 3 |
| done_seen_r/coincident | 105 | 105 |
| done_seen_r/pristine | 9 | 9 |
| own-states-dropped | 6 | 6 |
| own-minus-rhcoll | 3 | 3 |
| own-minus-wwait | 0 | 0 |
| own-plus-rhreq | 1 | 1 |
| C1 | 10 | 10 |
| C2 | 4 | 4 |
| C3 | 6 | 6 |
| C4 | 1 | 1 |
| retraction | 2 | 2 |
| pristine | 136 PASS, 0 FAIL | 136 PASS, 0 FAIL |
| half-page | 136 PASS, 0 FAIL | 136 PASS, 0 FAIL |
| half-page | 136 PASS, 0 FAIL | 136 PASS, 0 FAIL |
| page-buffered NOR | 136 PASS, 0 FAIL | 136 PASS, 0 FAIL |
| lazy erase | 135 PASS, 1 FAIL | 135 PASS, 1 FAIL |
| lazy erase + page-buffered | 135 PASS, 1 FAIL | 135 PASS, 1 FAIL |
| coincident completion | 136 PASS, 0 FAIL | 136 PASS, 0 FAIL |
| T16 byte comparison | pass FAIL FAIL FAIL FAIL | pass FAIL FAIL FAIL FAIL |
| T17 restore vs the record | pass FAIL FAIL pass FAIL | pass FAIL FAIL pass FAIL |
| T17 restore vs the array | pass pass FAIL pass pass | pass pass FAIL pass pass |
| T15 branch pin | pass pass FAIL pass FAIL | pass pass FAIL pass FAIL |
| T15 cut was real | pass pass pass pass FAIL | pass pass pass pass FAIL |
| T15 #70 property, unconditioned | pass pass pass pass FAIL | pass pass pass pass FAIL |

The full figure-gate output is in `before/nvm-figures.log` and `after/nvm-figures.log`.

Parent integration suite:

| Suite | Base checks/failures | Candidate checks/failures |
|---|---|---|
| pp_shadow | 371/0 | 371/0 |

Every named verdict is identical. The base run used parent `35f06958` with
processor `a8f8ce81`; the candidate run used parent `ea96db32` with processor
`a43d0766`. Full logs, pin identities and command exit statuses are in
`integration-comparison/`. The candidate branch and pin were restored.
