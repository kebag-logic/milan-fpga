# ACMP field corrections — Round 3

Round 3 status: **REVIEW READY** at `66d1b501f4879402fe76485095aef7c6e07c32af`. Documentation gates and the scratch-parent documentation consumer pass. See the Round 3 section for the current changes and fresh validation.

Round 2 status: **REVIEW READY**. Implementation head `96d3b78384f34a630d6056ebd8fa5e30f6836650` on `pp168-acmp-fields`; baseline `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`. The selected OOC 1x1 change is **+29 LUT / +14 FF**, within both +40 limits. All six assigned corrections remain present. Earlier receipts are historical and are not acceptance evidence for this recovery.

## Round 2

The existing merge `fee74ef977b0a56a98c2b8a8677e25cfdf994c08` brought main `09e357fb` into the parked lane without rebasing. Its first parent is `ba3f3f31e8fda01c3ef5271ff8005f3cf92ab4de`; its second parent is the baseline above. The final local commit reduces comparison and controller-response selection cost. Origin was verified as the assigned processor repository. The complete issue, original assignment, continuation ruling and Round 2 assignment were read; the standards are cited by clause without reproducing their text in the repository.

Every Round 2 measurement and gate in the historical tables below was run after the host reset. Baseline and final validation use fresh source archives and generated outputs. The scratch parent is dev `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Both supplied adoption patches are already incorporated there: reverse application checks pass, and regenerated empty adoption patches apply successfully. The parent consumer comparison uses the baseline processor gitlink first and the final processor gitlink for the head bank. No parent commit or push is made.

## Scope and the two initially unexercised items

Both items required corrections. Full received VLAN `0xF123` is exercised at settlement, in the record, GET_RX_STATE and integrated GET_STREAM_INFO. Internal storage and the authorised internal settlement port retain all 16 bits under Milan 5.3.8.9, Table 5.38 and 5.4.2.10. The parent-facing output retains its existing low-12-bit VID meaning. Parent SRP handling of a received value outside the valid VID range remains out of scope.

The outstanding probe retains its sent controller across a same-talker rebind, while the binding controller updates. The checks accept the sent controller, reject the replacement controller, and compare every retry byte under Milan 5.5.3.5.16 step 1, .17 step 2 and .18 step 1. The private record word shares pending-controller and settled-stream-ID lifetimes; published unsettled records report a zero stream ID. The field checks have explicit planted controls listed below.

No top-level port, parameter or register-map change is made. The top-level diff is restricted to the VLAN path. Its first 1,000 source lines, including public declarations, match baseline. The complete change remains in the 13 authorised source/test files. At Round 2 delivery, the old ACMP architecture prose was outside the authorised scope. The Round 3 assignment authorises and resolves that documentation follow-up below.

## Changes and clause authority

| Change | Location | Authority |
| --- | --- | --- |
| LD1: zero successful UNBIND talker fields | `hdl/acmp/KL_pp_acmp_listener.sv:682` | Milan v1.2 Table 5.36 |
| LD2: preserve status through discovered retry and delay expiry | `hdl/acmp/KL_pp_acmp_listener.sv:1273`, `:1345` | Milan 5.5.3.5.30 step 2, .10 |
| LD3: unauthorized status 16 | `hdl/acmp/pp_acmp_pkg.sv:123` | IEEE 1722.1-2021 8.2.1.5, Table 8-3; Milan Tables 5.31/5.35 |
| TD1: invalid DISCONNECT source returns TALKER_UNKNOWN_ID | `hdl/acmp/KL_acmp_talker.sv:1302` | Milan 5.5.4.2 step 1, Table 5.44; manager precedence over 5.5.2.7 |
| Full settled VLAN | `hdl/acmp/pp_acmp_pkg.sv:152`, `hdl/acmp/KL_pp_acmp_listener.sv:187`, `:698`, `:808`, `:1198`, `:1300` | Milan 5.3.8.9, Table 5.38 |
| Full internal top VLAN; low 12 bits to parent/SRP | `hdl/top/protocol_processor_top.sv:1021`, `:1042`, `:1901`, `:1933`, `:2714` | Milan 5.3.8.9; manager ruling 6050554601 |
| Settled-input GSI VLAN readback | `hdl/top/protocol_processor_top.sv:3536` | Milan 5.3.8.9, 5.4.2.10 |
| Saved probe controller guard and duplicate | `hdl/acmp/KL_pp_acmp_listener.sv:531`, `:704`, `:789`, `:1258`, `:1340` | Milan 5.5.3.5.17 step 2, .18 step 1, .16 step 1 |

The supporting changes are also within the authorised tests:

| Location | Change and authority |
| --- | --- |
| `tb/acmp_listener/sim_main.cpp:57`, `:187`, `:306`, `:339`, `:356`, `:384`, `:457`, `:479`, `:490`, `:1789` | Clause model, full record VLAN, independent sent-controller state and field-test invocation; LD1–LD3 and Milan 5.3.8.9, 5.5.3.5.10/.16/.17/.18/.30 |
| `tb/acmp_listener/field_cases.hpp:1` | Direct transport observations for the six assigned defects; individual clauses and witnesses below |
| `tb/acmp_talker/sim_main.cpp:1187` | Two invalid source IDs at the end of the existing walk; Milan 5.5.4.2 step 1/Table 5.44; placement preserves old mutation witnesses |
| `tb/pp_top/sim_main.cpp:5112`, `:5314`, `:9516`, `:9720` | Existing L4b, input GSI, AL1 and AS6 expectations; IEEE Table 8-3, Milan 5.3.8.9 and Table 5.36 |
| `tb/pp_top/gsi_internal.hpp:93`, `:365`, `:425` | Settled VLAN expectations, full-field integration checks and retained retry status; Milan 5.3.8.9, 5.4.2.10, 5.5.3.5.10/.30 and Table 5.22 |
| `tb/pp_top/acmp_mutants.py:59`, `:131`, `:234`, `:238`, `:325` | Eighteen new planted arms, with existing anchors retargeted to the authorised field changes; same clauses as their checks below. Tally expression wrapping is style-only. |
| `tb/acmp_listener/README.md:127`, `tb/acmp_talker/README.md:330`, `tb/pp_top/README.md:2816` | Document those clause checks, count changes, planted witnesses and the retained parent VID contract |

## Reduction implementation

The selected implementation compares each controller source before selecting the equality result. Non-pending states retain their original binding-controller comparison, preserving early-consume versus inert-write classification. The response builder selects the transmitted controller octet before choosing its source. Unbind leaves the private word for the next probe or settlement; published unsettled records and GET_RX_STATE remain zero.

Only the controller field receives the new byte-selection path. This meets the ceiling while limiting the response-builder change. A broader identity-byte trial also fits and is recorded below, but is not promoted. No assertion, required failure or correction is removed. Existing mutant anchors are retargeted to the equivalent comparison and byte selection; all 51 anchors are unique.

The selected reduction changes `hdl/acmp/KL_pp_acmp_listener.sv:531`, `:729` and `:1258`, with the corresponding anchors in `tb/pp_top/acmp_mutants.py:59`, `:82`, `:315` and `:321`. Its behaviour remains governed by Milan 5.5.3.5.16/.17/.18 and 5.3.8.9. `tb/acmp_listener/README.md:166` documents the implementation.

## OOC 1x1 before / after and attribution

All 13 fresh synthesis commands return 0. The unchanged recipe is `syn/ooc/protocol_processor_ooc.tcl`, device `xc7a100tfgg484-2`, one input, one output, eight synthesis threads and a 10 ns post-synthesis clock. Source/build paths are held constant. This is synthesis, not routing. Every final HDL hash equals the selected measured input.

| Design | LUT | FF | Delta LUT / FF |
| --- | ---: | ---: | ---: |
| Baseline `09e357fb` | 21614 | 18908 | 0 / 0 |
| Merged six corrections | 21741 | 18922 | +127 / +14 |
| Final `96d3b78` | 21643 | 18922 | +29 / +14 |
| Acceptance ceiling | — | — | +40 / +40 |

| Item | Clause | LUT | FF | Delta LUT / FF | Reduction tried |
| --- | --- | --- | --- | --- | --- |
| LD1 | Milan Table 5.36 | 21500 | 18901 | -114 / -7 | Required zero fields retained; response-byte sharing evaluated |
| LD2 | Milan 5.5.3.5.30 step 2; .10 | 21613 | 18908 | -1 / +0 | Retained status preserved; no separate costly state added |
| LD3 | IEEE 1722.1-2021 8.2.1.5, Table 8-3 | 21628 | 18905 | +14 / -3 | Required status 16 retained; response selection shared |
| TD1 | Milan 5.5.4.2 step 1, Table 5.44 | 21614 | 18908 | +0 / +0 | Existing source-valid comparison reused |
| VLAN | Milan 5.3.8.9; Table 5.38; 5.4.2.10 | 21606 | 18925 | -8 / +17 | All 16 clause-required bits retained; parent VID remains 12 bits |
| guard | Milan 5.5.3.5.16/.17/.18 | 21750 | 18905 | +136 / -3 | Compare before selection; select controller byte before source; omit private-word unbind clear |

The individual deltas sum to **+27 LUT / +4 FF**. The merged combined delta is **+127 / +14**, which is **+100 LUT / +10 FF** above that sum. The reductions are therefore evaluated on the combined design. The selected reduction saves 98 LUT against the merged implementation. Removing an apparently redundant clear alone increased area, so no monotonic relationship between source simplification and mapped area is assumed.

| Trial | LUT | FF | Delta LUT / FF | Outcome |
| --- | --- | --- | --- | --- |
| Equality results selected by state | 21665 | 18924 | +51 / +16 | over LUT limit |
| Above plus omit unbind private-word clear | 21732 | 18922 | +118 / +14 | over LUT limit |
| Above plus controller-byte selection (selected) | 21643 | 18922 | +29 / +14 | within limits |
| Comparison/clear plus all identity-byte selection | 21622 | 18922 | +8 / +14 | within limits |
| Above plus omit teardown private-word clear | 21662 | 18922 | +48 / +14 | over LUT limit |

The first baseline report collector rejected the LUT row's footnote marker. The parser was corrected; the actual completed synthesis returned 0, and its fresh report supplies the baseline above. The collector failure is retained and is not represented as a passed gate. Trial patches and input hashes make every variant reproducible. All 13 temporary item/OOC worktrees, including pre-reset worktrees, have been removed.

## Expectation changes and reasons

| Expectation | Reason |
| --- | --- |
| Listener model and integrated AL1/AS6 successful UNBIND talker fields become zero | Milan Table 5.36 |
| Listener lock refusals and integrated L4b status change from 13 to 16 | IEEE Table 8-3; Milan Tables 5.31/5.35 |
| Retry-delay and subsequent delay-expiry status remain unchanged | Milan 5.5.3.5.30 step 2 and .10 |
| RETRY-CLEAR becomes RETRY-RETAIN, reading status 7 after the actual probe | Those clauses retain timeout status, so Table 5.22 requires no status-change notification there. Seven obsolete notification/pair checks are removed; the replacement status read has a planted control. Prompt response delivery preserves the probe deadline. |
| Settled VLAN masks are removed from the listener model and input GSI expectations | Milan 5.3.8.9 and 5.4.2.10 require the received value; unsettled input readback is zero |
| Probe identity is captured at transmission and retained through rebind/retry | Milan 5.5.3.5.16/.17/.18; binding identity remains independently current |
| Invalid DISCONNECT source IDs return TALKER_UNKNOWN_ID with no source action changes | Milan 5.5.4.2 step 1, Table 5.44 governs over the overview in 5.5.2.7 |

The field examples set all upper VLAN bits (`0xF123`). Output GSI expectations are unchanged. TD1 cases follow the pre-existing talker walk so earlier mutation witnesses retain their exact context. The Round 2 reduction changes no expectation or assertion.

## Every new check and its planted defect

The final ACMP campaign builds and kills all 51 controls, including the 18 added controls, and all six goldens pass. Every added control fails every named witness. A build failure, missing tally or missing named witness does not count as a kill. The table identifies every new assertion site, including transport prerequisites; shared response helpers retain their existing field assertions. Fresh per-control evidence is recorded in `new-check-witnesses.json`.

| Check location | Check | Required failing mutant | Clause |
| --- | --- | --- | --- |
| `tb/acmp_listener/field_cases.hpp:17`, `:22`, `:31`, `:50`, `:57`, `:70`, `:97`, `:113` | Reset/stimulus completion, response presence, settlement and rebind prerequisites | `field_reset_blocked` | Setup for the field checks below |
| `tb/acmp_listener/field_cases.hpp:54` | Full VLAN at settlement | `settlement_vlan_truncated` | Milan 5.3.8.9 |
| `tb/acmp_listener/field_cases.hpp:63` | Full VLAN in GET_RX_STATE | `settled_vlan_truncated@acmp_listener` | Milan 5.3.8.9, Table 5.38 |
| `tb/acmp_listener/field_cases.hpp:76` | Accept the sent controller after rebind | `probe_guard_current_controller` | Milan 5.5.3.5.17 step 2, .18 step 1 |
| `tb/acmp_listener/field_cases.hpp:88` | Reject replacement controller on the outstanding probe | `probe_guard_current_controller` | Milan 5.5.3.5.18 step 1 |
| `tb/acmp_listener/field_cases.hpp:103` | Byte-identical retry after rebind | `probe_retry_current_controller` | Milan 5.5.3.5.16 step 1 |
| `tb/acmp_listener/field_cases.hpp:120` | Zero successful UNBIND talker fields | `unbind_talker_echo` | Milan Table 5.36 |
| `tb/acmp_listener/field_cases.hpp:133` | Discovered retry retains error status | `retry_status_cleared` | Milan 5.5.3.5.30 step 2 |
| `tb/acmp_listener/field_cases.hpp:137` | Retry probe retains previous error | `retry_probe_status_cleared` | Milan 5.5.3.5.10 |
| `tb/acmp_listener/field_cases.hpp:150` | Both lock refusals return 16 | `lock_status_13` | IEEE Table 8-3; Milan Tables 5.31/5.35 |
| `tb/acmp_listener/field_cases.hpp:152` | Both refusals preserve binding and side effects | `lock_gate_bypassed` | Milan 5.5.3.5.17 step 1, .20 step 1 |
| `tb/acmp_talker/sim_main.cpp:1189` | Invalid DISCONNECT is consumed | `disconnect_not_accepted` | Milan 5.5.4.2 step 1 |
| `tb/acmp_talker/sim_main.cpp:1191` | Invalid DISCONNECT response status and defined identity fields | `disconnect_invalid_success` | Milan 5.5.4.2 step 1, Table 5.44 |
| `tb/acmp_talker/sim_main.cpp:1192` | Invalid DISCONNECT leaves source actions unchanged | `disconnect_changes_gate` | Milan 5.5.4.2 step 1 |
| `tb/pp_top/gsi_internal.hpp:377` | Full VLAN in integrated GSI | `stored_vlan_truncated`, `gsi_vlan_external` | Milan 5.3.8.9, 5.4.2.10 |
| `tb/pp_top/gsi_internal.hpp:379` | Parent output remains low 12 bits | `parent_vlan_shifted` | Manager ruling 6050554601 |
| `tb/pp_top/gsi_internal.hpp:388` | Full VLAN in integrated GET_RX_STATE | `settled_vlan_truncated@pp_top` | Milan 5.3.8.9, Table 5.38 |
| `tb/pp_top/gsi_internal.hpp:392` | Unbind clears full VLAN readback | `gsi_vlan_external` | Milan 5.3.8.9, 5.4.2.10 |
| `tb/pp_top/gsi_internal.hpp:428` | Integrated retained retry status 7 | `retry_probe_status_cleared@pp_top` | Milan 5.5.3.5.30 step 2, .10; Table 5.22 |

## Fresh validation

The tables below contain only fresh recovery receipts. A pending cell is not a passed gate. All unaffected canonical records and failure lists must match baseline; only the assigned clause changes are allowed. Parallel completion order is ignored when comparing keyed records.

The two suites touched by the main merge were also rerun independently on the merged revision before the reduction.

| Merge suite | Checks | Failures | rc |
| --- | --- | --- | --- |
| aecp_notify | 67 | 0 | 0 |
| pp_top | 10470 | 0 | 0 |

| Processor gate | Base rc | Head rc |
| --- | --- | --- |
| scripts/run_suites.sh | 0 | 0 |
| scripts/lint_hdl.sh | 0 | 0 |
| make -j16 check | 0 | 0 |
| scripts/gen_matrix.py --check | 0 | 0 |
| syn/yosys/run.sh | 0 | 0 |

### Processor suites

| Suite | Base checks | Head checks | Allowed change |
| --- | --- | --- | --- |
| acmp_listener | 3111 | 3167 | +56: six clause cases |
| acmp_nvm | 388 | 388 | unchanged |
| acmp_talker | 1342 | 1376 | +34: invalid DISCONNECT IDs |
| adp_engine | 1359 | 1359 | unchanged |
| aecp_notify | 67 | 67 | unchanged |
| ca_originator | 16 | 16 | unchanged |
| desc_mem_guard | 78 | 78 | unchanged |
| desc_store | 586 | 586 | unchanged |
| dispatch | 211 | 211 | unchanged |
| dyn_state | 118 | 118 | unchanged |
| event_router | 81 | 81 | unchanged |
| lsn_admit | 18 | 18 | unchanged |
| maap | 196 | 196 | unchanged |
| nvm_port | 1219 | 1219 | unchanged |
| originator | 107 | 107 | unchanged |
| pp_top | 10469 | 10470 | +1: full VLAN and retained retry status |
| prng | 76 | 76 | unchanged |
| release_merge | 18 | 18 | unchanged |
| resp_buf | 64 | 64 | unchanged |
| rx_slots | 130 | 130 | unchanged |
| rx_validator | 555 | 555 | unchanged |
| scoreboard | 3705 | 3705 | unchanged |
| side_port | 368 | 368 | unchanged |
| srp_admission | 991231 | 991231 | unchanged |
| srp_decoder | 190 | 190 | unchanged |
| srp_encoder | 581 | 581 | unchanged |
| srp_stream_fsms | 1347 | 1347 | unchanged |
| srp_top | 8656 | 8656 | unchanged |
| timer_map | 1360 | 1360 | unchanged |
| timer_service | 48 | 48 | unchanged |
| tx_arbiter | 66 | 66 | unchanged |
| tx_slots | 95 | 95 | unchanged |
| ucpu | 437 | 437 | unchanged |

Totals: 1,028,293 base; 1,028,384 head.

### Affected campaigns

| Campaign | Base rc | Head rc |
| --- | --- | --- |
| acmp_talker-retry_mutants | 0 | 0 |
| pp_top-acmp_mutants | 0 | 0 |
| pp_top-gsi_mutants | 0 | 0 |
| pp_top-d3_mutants | 0 | 0 |
| pp_top-aecp_dispatch_mutants | 0 | 0 |
| pp_top-aecp_mutants | 0 | 0 |
| pp_top-ctr_mutants | 0 | 0 |
| pp_top-notify_mutants | 0 | 0 |
| pp_top-name_wr_mutant | 0 | 0 |
| adp_engine-mutants | 0 | 0 |
| maap-mutants | 0 | 0 |
| srp_top-mutants | 0 | 0 |
| srp_admission-mutants | 0 | 0 |

### Scratch-parent consumers

| Consumer | Base rc | Head rc |
| --- | --- | --- |
| scripts/check_cpp_idiom.py | 0 | 0 |
| scripts/check_py_idiom.py | 0 | 0 |
| scripts/check_rtl_source_lists.py | 0 | 0 |
| scripts/pp_srcs.py --check --selftest | 0 | 0 |
| scripts/check_port_contracts.py | 0 | 0 |
| scripts/measure_naming.py --check | 0 | 0 |
| scripts/measure_test_evidence.py --check | 0 | 0 |
| scripts/docs_check.py | 0 | 0 |
| scripts/xvlog_gate.py --check | 0 | 0 |
| sw/builder/test_builder.py | 0 | 0 |
| scripts/lint_rtl.py --check | 0 | 0 |
| make -j16 -C tb/verilator/pp_shadow | 0 | 0 |
| make -j16 -C tb/verilator/nvm_cosim lint | 0 | 0 |
| make -j16 -C tb/verilator/nvm_cosim quick JOBS=16 POOL=2 | 0 | 0 |
| make -j16 -C tb/verilator/milan_dp VERILATOR_JOBS=16 | 0 | 0 |
| make -j16 -C tb/verilator/milan_dp_render VERILATOR_JOBS=16 MUTANT_JOBS=2 | 0 | 0 |
| scripts/check_sh_idiom.py | 0 | 0 |

The original shadow gates both returned zero, but parallel recipe output interleaved simulation and compiler fragments. Those raw logs are retained. Exact shadow-record comparison uses a baseline rebuild in a source fixture with synchronized target output and four isolated replays of the fresh head binaries. The fixture is not a checkout; test sources, HDL inputs, modes and assertions are unchanged.

| Shadow record replay | Base rc | Head rc |
| --- | --- | --- |
| 12_shadow | 0 | 0 |

### Record comparison

All required commands return 0. The strict comparison audit passes. All 18 new controls build, complete and fail every named witness. All 51 ACMP mutants are killed and all six goldens pass.

| Campaign records | Comparison |
| --- | --- |
| acmp_talker-retry_mutants | 72 completed log pairs; 13 changed failure lists |
| adp_engine-mutants | 57 completed log pairs; 0 changed failure lists |
| maap-mutants | 32 completed log pairs; 0 changed failure lists |
| pp_top-acmp_mutants | 37 completed log pairs; 2 changed failure lists; 37 common canonical records, 2 changed, 20 added, 0 removed |
| pp_top-aecp_dispatch_mutants | 41 completed log pairs; 0 changed failure lists; 44 common canonical records, 0 changed, 0 added, 0 removed |
| pp_top-aecp_mutants | 67 completed log pairs; 0 changed failure lists |
| pp_top-ctr_mutants | 18 completed log pairs; 0 changed failure lists |
| pp_top-d3_mutants | 116 completed log pairs; 0 changed failure lists; 116 common canonical records, 0 changed, 0 added, 0 removed |
| pp_top-gsi_mutants | 22 completed log pairs; 5 changed failure lists; 22 common canonical records, 0 changed, 0 added, 0 removed |
| pp_top-name_wr_mutant | 3 completed log pairs; 0 changed failure lists; 3 common canonical records, 0 changed, 0 added, 0 removed |
| pp_top-notify_mutants | 106 completed log pairs; 0 changed failure lists; 106 common canonical records, 0 changed, 0 added, 0 removed |
| srp_admission-mutants | 12 completed log pairs; 0 changed failure lists |
| srp_top-mutants | 130 completed log pairs; 0 changed failure lists |

The only old ACMP records that change gain one assigned-field failure each: saved-controller rebind rejection and full-VLAN readback. All earlier failures remain. Every talker run retains its earlier failure lines; 13 runs add TD1 witnesses. All GSI canonical records remain identical; five detailed failure traces reflect the assigned retained-status/VLAN cases. The old notification wait could expire the pending probe in a notification-disabled mutant, producing secondary unsettled-state failures. RETRY-RETAIN observes the real probe promptly and removes that cascade. Required notification witnesses remain failing. Full trace diffs are retained.

| GSI detailed trace | Base failures | Head failures |
| --- | --- | --- |
| acmpsta-zero-run.log | 20 | 22 |
| integrator-path-run.log | 1342 | 1342 |
| pbsta-zero-run.log | 1682 | 1680 |
| status-notification-zero-run.log | 979 | 52 |
| wrong-sink-run.log | 2500 | 2500 |

The notification-disabled head trace is an ordered subsequence of the baseline trace, with no added failure. The saved trace review records hashes and verifies that all required notification witnesses remain.

The parent source inventory adds only `tb/acmp_listener/field_cases.hpp` and the net 92 lines in `tb/pp_top/acmp_mutants.py`. All reported finding counts remain identical. Builder comparison ignores random temporary-directory suffixes and elapsed wall-clock seconds on five elaboration rows; all 511 normalized lines match. The raw differences are retained. Processor gate records also match after accounting for the added test file in the ID inventory (556 → 557), parallel completion order, and generated source-line offsets. Parent lint diagnostics match; the NVM lint source excerpt changes only the assigned LD3 constant from 13 to 16, apart from runtime statistics. Parent HDL analysis records match apart from the expected processor gitlink.

| Parent simulation | Base records | Head records | Comparison |
| --- | --- | --- | --- |
| 12_shadow | 2340 | 2340 | identical |
| 14_nvm_quick | 3 | 3 | identical |
| 15_datapath | 12140 | 12140 | identical |
| 16_render | 121 | 121 | identical |
| 10_builder | 511 | 511 | identical |

The base parent builder leaves its real-report calibration arm unrun because the historical placement report is absent. Its zero command return is not claimed as execution of that arm.

The head parent builder leaves its real-report calibration arm unrun because the historical placement report is absent. Its zero command return is not claimed as execution of that arm.

A system-clock control is separately classified as inapplicable where the configured system and Milan clocks are identical. It is distinct from the unrun real-report calibration arm.

## Execution and artifacts

The pinned 5.050 simulation compiler is exported through the scratch harness. Independent suites, campaigns and parent consumers run concurrently, with three build slots, eight compiler slots and 16 make jobs. One build slot was reserved for lint and small standalone builds during the early concurrent runs. Larger builds briefly shared all three slots after the merge-suite run. The sequential parent baseline/head path then joined lint and standalone builds on the third slot to bound its queue time; the other two slots serve processor integration campaigns until the parent finishes. The total build and compiler limits stay unchanged. Campaign drivers receive `--jobs 2` where supported; the retry driver uses `--logs`, and the name-write driver has no jobs option. Parent make commands use 16 jobs. The render leg-defect mode and the render-law/grandmaster-step drivers expose no jobs option. Synthesis and parent analysis run serially under the shared lock, with compilation paused for those measurements.

A queued head analysis reservation held local build slots while waiting for the shared lock. It was cancelled before the analysis command started (empty log, blocked lock waiter), and replaced with admission through the shared lock alone. The interrupted queue receipts are retained separately; the replacement gate returned zero. The local build-slot drain is not needed for exclusion because every HDL build holds the shared lock and analysis holds it exclusively.

The item and combined measurements use unchanged recipes and fresh outputs. Source archives, builds and large logs stay in scratch storage. Output files are capped at 200,000 bytes; larger evidence is represented by SHA-256 and size. `round2-artifact-index.json` and its split manifests identify fresh recovery evidence; older manifests are historical. `SHA256SUMS` is refreshed at delivery. The output includes the complete baseline-to-head patch, scope and commit receipts, area reports, source hashes, expected-failure witnesses and record comparisons.

No push, PR operation, parent commit, rebase, hardware access or flashing is performed. No second TAKEN comment is posted. The final public status is [REVIEW READY](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/168#issuecomment-6085166708) on issue 168, identifying head `96d3b78384f34a630d6056ebd8fa5e30f6836650`.

Final runtime audit: the processor tree is clean, the parent has only the staged processor gitlink, all tracked archive inputs match their commits, and no task jobs remain running. Observed cgroup memory peak: 12.16 GiB, including filesystem cache; no out-of-memory events occurred. Unused cache from completed builds was released without changing file contents.


## Round 3 — documentation alignment

Assignment: processor issue #168, comment 6086157264. Review inputs: PR #171 comments 6086150428 (R552-1) and 6085456323 (R553-1). Start revision: `96d3b78384f34a630d6056ebd8fa5e30f6836650`; the assigned origin, clean branch, and open PR head were verified. The full issue, assignments and both reviews were read. The governing Milan v1.2 clauses were read directly from the local PDF; the IEEE status-table authority was also checked. PDF identities are recorded by hash and size in `round3/authorities.json`; no standard text is copied into the repository.

All edits are documentation under `docs/`: eight Markdown files and two SVG figures. No RTL, test, generator, register map, port or parameter is changed. The implementation, assertions and mutation controls at the reviewed Round 2 head are retained byte-for-byte. This round adds a new commit on that head; it does not rebase, amend or push.

### Changes, exact locations and authority

| Finding / change | File:line | Clause or contract |
| --- | --- | --- |
| R552-F1 / R553-F1: validate the DISCONNECT source; invalid returns TALKER_UNKNOWN_ID, valid returns SUCCESS, neither changes state | `docs/architecture/05_acmp_engine.md:13`, `:403`, `:412` | Milan v1.2 §5.5.4.2 step 1, Tables 5.44/5.45; procedure takes precedence over §5.5.2.7 overview |
| Correct the delta master, gap statement and conformance row built on unconditional SUCCESS | `docs/architecture/01_overview.md:139`; `docs/00_MILAN_COMPLIANCE_REVIEW.md:96`, `:393` | Same TD1 authority; GET_TX_CONNECTION remains governed by §5.5.4.4 |
| Correct the operator answer and its related state-diagram caption | `docs/guides/operator.md:52`; `docs/diagrams/24-adp-acmp-states.svg:116` | Same TD1 authority |
| R552-F2 / R553-F1: A5 retains status on delay expiry; A12 retains it on discovered retry; other applicable clears remain | `docs/architecture/05_acmp_engine.md:290`, `:297`, `:305` | Milan §5.5.3.5.10, §5.5.3.5.30 steps 1/2 |
| Explain status visibility through retry and distinguish saved ACMP status from GET_RX_STATE response status | `docs/architecture/05_acmp_engine.md:337` | Milan §5.3.8.6, §5.5.3.5.10/.18/.30, Table 5.38 |
| R552-F3 / R553-F2: state summary retains all 16 VLAN bits and links to the private-overlay lifetime | `docs/architecture/05_acmp_engine.md:131`, `:135` | Milan §5.3.8.9, Table 5.38, §5.4.2.10 |
| F07.6 stores VLAN in bits [319:304], removes the reserved nibble and retains a 384-bit record; generated figure matches its source | `docs/architecture/07_memory_maps.md:495`, `:509`; `docs/diagrams/wavedrom/fig-07-sinkrec.svg:1` | Same full-value clauses; `hdl/acmp/pp_acmp_pkg.sv:152` |
| Shorten the overlapping flags label and preserve the bit order in adjacent prose | `docs/architecture/07_memory_maps.md:486`, `:506`; same rendered figure | Existing F07.6 layout, package bits [18:11]; no layout change beyond the authorised VLAN correction |
| Explain A5 capture, A6 binding replacement, A13 duplicate, A15 settlement, A10 reuse and the published zero mask in every unsettled state | `docs/architecture/07_memory_maps.md:515`; `docs/architecture/05_acmp_engine.md:290`, `:298` | Milan §5.5.3.5.16 step 1, .17 step 2, .18 step 1, .25 step 1; §5.3.8.9; listener private/published storage contract |
| R552-F4 / R553-F2: input selector 6 [63:48] is the full settled VLAN, otherwise zero; [47:0], flags, request and wait remain external; output unchanged | `docs/architecture/06_aecp_engine.md:335`, `:421`, `:427` | Milan §5.3.8.9, §5.4.2.10; `hdl/top/protocol_processor_top.sv:3507`, `:3536` |
| Apply that ownership rule consistently at the interface boundary and integrator entry point | `docs/architecture/02_interfaces.md:413`, `:416`; `docs/guides/integrator.md:570`, `:575` | Same clauses and input-gather ownership contract |
| Explicitly preserve the 12-bit top-level and SRP VID projection and parent-side responsibility for invalid VID values | `docs/architecture/02_interfaces.md:418`; `docs/guides/integrator.md:547` | Issue ruling 6050554601; top low-[11:0] assignments at `:1042`, `:2714` |
| Give the interface section a stable anchor used by the three new links | `docs/architecture/02_interfaces.md:398` | Documentation link contract; supports the VLAN boundary references |

The DISCONNECT validity prose includes an in-range but disabled source, matching the existing source-valid predicate. It does not claim a new executable witness for that optional case. The saved controller lifetime is expressly separate from the binding controller and from the persisted binding record.

### Review suggestions and residue

| Review item | Outcome |
| --- | --- |
| R552-S1, apparently redundant A12 clear | Documented why it stays: non-retry callers already have zero status and the explicit clear states those transitions. No area claim or RTL edit. |
| R552-S2, SRP VID bits 8–11 coverage | The boundary pages now state the actual low-[11:0] projection. The suggested additional stimulus/control is not added in this documentation-only round; existing parent-VID witnesses remain intact. |
| R552-S3, in-range unconfigured DISCONNECT source | The decision-tree explanation now names configured/enabled-source validity. Additional executable coverage remains optional and was not added. |
| R552-S4, post-synthesis TNS variance | No new timing claim. Round 2 area figures remain historical OOC synthesis evidence; routed parent timing remains the authority. |
| Residue | R552-1 lists none; R553-1 lists no separate residue or suggestion. The additional stale operator-diagram caption and the overlapping F07.6 flags label found during the page sweep are corrected. |

### Documentation-consumer inventory

Every executable reader of the changed processor documents is reached by `make -j16 check`: diagram syntax, rendered-figure freshness, relative links/anchors, compliance matrix, integrator parameter inventory, ID registries and figure inventory. The matrix generator is also run explicitly. The unchanged draw.io freshness target completes in the same gate.

The source/test inventory was searched for Markdown/SVG readers. The listener ROM generator and its C++ model are hand transcriptions of F05.3; they do not parse these documents at execution. Descriptor and microcode generators refer to architecture pages but read their source models, not the documents. The NVM figure campaign reads only its unchanged suite README and implementation history. No simulation suite or mutation campaign builds a changed file in this round. There is no additional processor document reader outside the documentation gates.

The scratch-parent `scripts/docs_check.py` uses the parent's tracked-file inventory; its submodule-doc checker reads the parent's own pin table and diagram, not the processor architecture pages. The general parent documentation command is nevertheless repeated around the scratch pin update. The full Round 2 parent consumer table above remains historical, not a claim of rerunning all 17 commands for this documentation edit.

### Fresh Round 3 validation

Baseline means the unchanged `96d3b783` tree before any edit. Head means the final documentation tree. Each command has its own log and rc file under `round3/`; independent commands run concurrently and are joined before proceeding. No result below relies on a partial or pre-reset output.

| Gate | Baseline rc | Head rc | Result |
| --- | ---: | ---: | --- |
| `make -j16 check` | 0 | 0 | All nine documentation targets pass; 41 syntax diagrams, 18 rendered layouts, 115 requirements, 17 gap rows, 94 module rows, zero untested modules |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | 94 rows, zero untested |
| `git diff --check` | 0 | 0 | Clean patch whitespace |
| Parent `python3 scripts/docs_check.py` | 0 | 0 | Parent documentation consumer; not a processor semantic test |

The existing ID and figure negative fixtures pass 30/30 and 17/17. Before regenerating F07.6, the unchanged freshness checker rejects the retained old render with rc 1 and names `fig-07-sinkrec` (`stale-figure.log/.rc`); the regenerated figure passes. This is a negative control, not a passed positive gate. The initial head check also caught three invalid inferred section anchors and returned 2. Those links now target an explicit anchor; the failed attempt is retained as `initial-head-check.*`, and the final head check returns 0.

The baseline and final gate records differ only in the relative-link count, 1179 → 1186, for the seven added documentation links; other counts are identical, apart from parallel output order. The transition-matrix cells, requirements inventory, HDL module inventory and all executable test expectations are unchanged.

The two edited figures were rendered and inspected. F07.6's live VLAN nibble and shortened flags label fit with two distinct installed fonts, Adwaita Sans and Adwaita Mono. The earlier requested fallback families resolved to the same installed font and are not counted as a two-font check. Scratch PNGs and font-substitution SVGs remain outside the repository and output directory; their hashes and sizes are listed in `round3/external-artifacts.json`.

### Test expectations, new checks and retained implementation evidence

There are **no Round 3 test expectation changes and no new automated test checks**, so there is no new required suite mutant. All 18 prior added controls and their named failing witnesses remain unchanged; their fresh Round 2 outcomes are enumerated above. The existing documentation self-tests and stale-render negative control exercise the gates used here.

The two originally unexercised issues remain corrected and documented: full VLAN retention and response/retry matching against the sent probe controller. The Round 2 1x1 comparison remains 21,614 → 21,643 LUT (+29) and 18,908 → 18,922 FF (+14). This is retained evidence for identical HDL, not a new synthesis measurement in Round 3. The 33-suite, 13-campaign and 17-consumer tables above likewise belong to Round 2. No hardware or physical report calibration was performed; the historical missing-report limitation remains.

Final local commit: `66d1b501f4879402fe76485095aef7c6e07c32af`, parent `96d3b78384f34a630d6056ebd8fa5e30f6836650`, subject `docs: align ACMP field behavior and data ownership`. The tree is clean. All non-documentation tracked files match the parent commit. No new automated check or changed assertion was introduced.

The scratch parent remains uncommitted at `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`, with only its processor gitlink staged at the final local head. Both original adoption patches pass reverse-application checks, confirming they are already incorporated in that parent revision. Its fresh documentation command returns 0 at both processor pins, with byte-identical records (`round3/parent-pin.json`). No other parent consumer is represented as newly executed here.

`round3/commit.json`, `precommit-audit.json`, `parent-pin.json`, the gate logs/rc files and the Round 3 patch identify the delivery. `round3/external-artifacts.json` records scratch figures by SHA-256 and size. The original Round 2 manifests remain historical; the delivery checksum index is refreshed. All lane commands have completed; no synthesis or background build was launched in this round. Public [REVIEW READY](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/168#issuecomment-6086365354) is posted on issue #168 with the final head; `round3/REVIEW-READY-RECEIPT.json` records it.
