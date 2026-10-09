# ACMP field corrections — Round 2

Current status: Round 2 final validation is running at head `96d3b78384f34a630d6056ebd8fa5e30f6836650`, against main `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`. The measured final RTL is within the area ceiling at +29 LUT / +14 FF; required gates and record comparisons remain pending. The section below records historical Round 1b evidence; the current Round 2 section follows it.

## Historical Round 1b outcome

Status: STOP — the OOC LUT increase exceeds the assignment ceiling. Functional validation is complete under assignment 6050429859 and ruling 6050554601; acceptance is not met. Processor base: `ed340b9b85258194247334b85e62cf9c23d4d051`; head: `ba3f3f31e8fda01c3ef5271ff8005f3cf92ab4de`, branch `pp168-acmp-fields`. Four local commits carry the implementation, the clause-required integrated retry expectation, placement of TD1 after existing mutation witnesses, and an equivalent line wrap required by the parent style gate. The processor worktree is clean. Origin was verified as the requested processor repository. The complete issue and both authority comments were read.

## Scope and outcome

The four named defects and both previously unexercised defects are corrected locally. The original STOP diagnostic is retained, and its direct transport checks form the starting point of the permanent field tests. Local standards are cited by clause; no standards text is copied into the repository.

The two initially unexercised items were both nonconformant. The retained base diagnostic observed received VLAN `0xA123` truncated to `0x0123` at settlement, in the record and in GET_RX_STATE. It also rejected the originally sent controller after same-talker rebind, accepted the replacement controller, and emitted a changed retry. These were the five original diagnostic failures. Head exercises `0xF123` to cover every upper VLAN bit, retains it through both readbacks, accepts only the sent controller, and emits a byte-identical retry. The new checks and their planted controls all pass the completed mutation campaign.

The manager-authorised settlement port, internal wire and VLAN storage now carry 16 bits. GET_RX_STATE and GET_STREAM_INFO return the full received value. The parent-facing output retains bits 11:0 and its existing width. Parent handling of a stream_vlan_id that is not a valid VID remains out of scope. No top-level port, parameter or register-map edit is made.

The probe controller shares the private stream-ID word while a probe is outstanding; a published record masks that word to zero until settlement. This keeps record width and public binding-controller meaning unchanged. Same-talker rebind updates the binding controller, while matching and retransmission retain the controller actually sent.

The existing architecture page still describes unconditional retry-status resets at `docs/architecture/05_acmp_engine.md:283` and `:290`, and unconditional DISCONNECT success at `:13` and `:387`. Those statements are superseded by the cited procedures and this assignment. Editing that page is outside the authorised paths, so it is recorded as a documentation follow-up rather than changed in this lane.

## Changes and clause authority

| Change | Location | Authority |
| --- | --- | --- |
| LD1: zero successful UNBIND talker fields | `hdl/acmp/KL_pp_acmp_listener.sv:682` | Milan v1.2 Table 5.36 |
| LD2: preserve status through discovered retry and delay expiry | `hdl/acmp/KL_pp_acmp_listener.sv:1261`, `:1333` | Milan 5.5.3.5.30 step 2, .10 |
| LD3: unauthorized status 16 | `hdl/acmp/pp_acmp_pkg.sv:123` | IEEE 1722.1-2021 8.2.1.5, Table 8-3; Milan Tables 5.31/5.35 |
| TD1: invalid DISCONNECT source returns TALKER_UNKNOWN_ID | `hdl/acmp/KL_acmp_talker.sv:1302` | Milan 5.5.4.2 step 1, Table 5.44; manager precedence over 5.5.2.7 |
| Full settled VLAN | `hdl/acmp/pp_acmp_pkg.sv:152`, `hdl/acmp/KL_pp_acmp_listener.sv:187`, `:698`, `:797`, `:1187`, `:1288` | Milan 5.3.8.9, Table 5.38 |
| Full internal top VLAN; low 12 bits to parent/SRP | `hdl/top/protocol_processor_top.sv:1021`, `:1042`, `:1901`, `:1933`, `:2714` | Milan 5.3.8.9; manager ruling 6050554601 |
| Settled-input GSI VLAN readback | `hdl/top/protocol_processor_top.sv:3536` | Milan 5.3.8.9, 5.4.2.10 |
| Saved probe controller guard and duplicate | `hdl/acmp/KL_pp_acmp_listener.sv:531`, `:704`, `:778`, `:1247`, `:1328` | Milan 5.5.3.5.17 step 2, .18 step 1, .16 step 1 |

The supporting changes are also within the authorised tests:

| Location | Change and authority |
| --- | --- |
| `tb/acmp_listener/sim_main.cpp:57`, `:187`, `:306`, `:339`, `:356`, `:384`, `:457`, `:479`, `:490`, `:1789` | Clause model, full record VLAN, independent sent-controller state and field-test invocation; LD1–LD3 and Milan 5.3.8.9, 5.5.3.5.10/.16/.17/.18/.30 |
| `tb/acmp_listener/field_cases.hpp:1` | Direct transport observations for the six assigned defects; individual clauses and witnesses below |
| `tb/acmp_talker/sim_main.cpp:1187` | Two invalid source IDs at the end of the existing walk; Milan 5.5.4.2 step 1/Table 5.44; placement preserves old mutation witnesses |
| `tb/pp_top/sim_main.cpp:5112`, `:5314`, `:9516`, `:9720` | Existing L4b, input GSI, AL1 and AS6 expectations; IEEE Table 8-3, Milan 5.3.8.9 and Table 5.36 |
| `tb/pp_top/gsi_internal.hpp:93`, `:365`, `:425` | Settled VLAN expectations, full-field integration checks and retained retry status; Milan 5.3.8.9, 5.4.2.10, 5.5.3.5.10/.30 and Table 5.22 |
| `tb/pp_top/acmp_mutants.py:59`, `:131`, `:234`, `:238`, `:325` | Eighteen new planted arms, with existing anchors retargeted to the authorised field changes; same clauses as their checks below. Tally expression wrapping is style-only. |
| `tb/acmp_listener/README.md:127`, `tb/acmp_talker/README.md:330`, `tb/pp_top/README.md:2799` | Document those clause checks, count changes, planted witnesses and the retained parent VID contract |

## Expectations and new checks

Listener model changes follow the same clauses: unauthorized 13 -> 16; successful UNBIND talker fields -> zero; retry-delay and delay-expiry status retained; VLAN masks removed; probe identity captured at first transmission. Existing integrated UNBIND expectations AL1/AS6 change to zero talker fields. Integrated lock check L4b changes 13 -> 16 under IEEE Table 8-3; the first head campaign exposed this missed old expectation and correctly refused to run mutants after its golden failed. Integrated input GSI expectations now use stored VLAN when settled and zero otherwise. RETRY-CLEAR is replaced by RETRY-RETAIN: .30 step 2 and .10 retain timeout status 7, so Table 5.22 provides no status-change notification at retry. The test waits for the actual probe and reads status directly, keeping its response within the probe deadline. This removes seven obsolete notification/pair checks; the retained-status read has its own planted control. Output GSI is unchanged. New full-field examples use 0xF123 so every upper bit is exercised.

New checks cover each named defect, full VLAN through listener and integrated readback, unchanged parent VID, same-talker rebind accept/reject, byte-identical retry, refusal side effects and invalid disconnect side effects. Every CHECK site has a named planted defect in `tb/pp_top/acmp_mutants.py`. The current campaign has 51 arms (33 existing plus 18 new), including integrated retained-status readback. All 51 edit anchors are unique in the final source. All 13 changed files match the frozen final copy; all changed RTL matches the isolated area input. The first 1000 top-level source lines, including its public ports and parameters, match base exactly. The complete final ACMP campaign returned 0: 51/51 mutants killed and six goldens passed. `new-check-witnesses.json` records successful builds and the actual required failing lines for all 18 added arms. The supplemental acceptance mutant first failed to compile because it referenced a packed input as a struct; it was classified SURVIVED, never counted as a kill, and its source expression was corrected for a repeat.

Focused final results: listener 3167/3167; talker 1376/1376; integrated GSI 6183/6183. The retained-status controls in both listener and integrated GSI and the corrected command-acceptance control all build and fail their named checks (three of three killed). The earlier integrated ACMP run passed 43/43. Focused tests are supporting evidence, not substitutes for the complete suite and campaign tables.

## New assertion coverage

These are the new assertion sites; shared response helpers retain their existing field checks. Every listed planted arm builds and is killed in the completed final ACMP campaign; no required witness is missing. A kill requires successful execution to the suite tally and failure of every named witness, not merely a nonzero command exit.

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

## Validation results

The complete base processor suite bank passed: 33 suites, 1028291 checks, zero failing. The final suite bank also passed: 33 suites, 1028382 checks, zero failing. Only listener (+56), talker (+34) and processor top (+1) counts change; every other suite count is identical. All 13 affected campaigns returned 0 at both base and head. The final D3 campaign killed all 110 mutants, passed six goldens, and retained all 116 canonical records and every earlier failure line unchanged. Base/head lint, matrix and Yosys have returned 0. Base make check returned 0 on its corrected invocation; head make check returned 0, including the final formatting commit. The first two base documentation invocations failed because an external snapshot runner misdirected scratch-fixture Git operations; their results are excluded. The runner was corrected and its temporary working-tree configuration removed, preserving configured identity, branch and HEAD.

The base ACMP campaign completed with 33/33 killed defects and four passing goldens; head completed with 51/51 killed defects and six passing goldens. Of the 37 existing canonical records, 35 are identical. The saved-controller guard control adds the new rebind rejection failure (50→51), and the settled-VLAN storage control adds the new full-field readback failure (25→26); their earlier failures are unchanged. The final GSI campaign returned 0 with all 22 canonical records identical to base. Five detailed failure traces change through the assigned retry-status/VLAN cases: acmpsta-zero 20→22; pbsta-zero 1682→1680; wrong-sink 2500→2500; integrator-path 1342→1342; status-notification-zero 979→52. The last reduction includes downstream cascade failures: the old RETRY-CLEAR notification wait expired the pending probe when notifications were disabled, so subsequent settlement and latency checks ran in an unsettled state. RETRY-RETAIN observes the actual probe promptly under the clause-required status semantics, and those secondary failures disappear. The existing named notification witnesses still fail; all 22 GSI canonical records remain identical. Full trace diffs are retained, including this cascade change.

Moving TD1 after the pre-existing walk restores exact old failure text for no_command_ready (693 old failures), reallocate_owned (119), and source_alias (172); only TD1 witnesses are additional. Their focused campaign and all three TD1 field controls return 0. The final complete talker campaign returned 0. All 72 run records retain every earlier failure line; 13 runs add failures labelled TD1. Baseline/restored and all seven equivalence controls plus the performance control still pass, with 62 defects killed.

The scratch parent is dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863` with both supplied adoption patches. All 17 base consumer commands returned 0. The builder ledger explicitly excludes gate 11 real-report calibration because the historical mf48 utilisation report is absent; that arm is not claimed as exercised. The final builder command also returned 0 with exactly the same calibration arm unrun. The scratch parent processor gitlink now names the final head; its parent HEAD remains unchanged, and its only other differences are the two supplied adoption patches. All 17 final-head consumer commands returned 0 after the style correction. The first batch aggregate remains 1 because it retains the earlier overlong-line failure; `parent-final-selected.rc` is the explicit aggregate of the final receipts listed below. No parent commit or push is allowed. Before Git operations in a submodule, its exact top-level directory is verified. The 17-consumer base/head table below names the final receipts.

## OOC 1x1 before / after

The acceptance run uses `syn/ooc/protocol_processor_ooc.tcl`, device `xc7a100tfgg484-2`, one input and one output, eight synthesis threads and a 10 ns post-synthesis clock. It is an out-of-context synthesis measurement, not a routed image. Both measurements return 0. Source/build paths were held constant for the controlled comparison.

| Measurement | Base | Final RTL | Delta | Limit | Outcome |
| --- | ---: | ---: | ---: | ---: | --- |
| LUT | 21442 | 21620 | +178 | +40 | FAIL |
| FF | 18890 | 18908 | +18 | +40 | PASS |
| LUTRAM | 2328 | 2328 | 0 | — | unchanged |
| RAMB36 / RAMB18 | 16 / 1 | 16 / 1 | 0 / 0 | — | unchanged |
| DSP | 4 | 4 | 0 | — | unchanged |

The final measurement is `ooc-candidate-isolated`, whose changed RTL hashes equal the delivered head. An earlier final-RTL run gave exactly the same counts but briefly overlapped the end of the portability gate; it is excluded from the acceptance measurement. The isolated repeat paused independent compilation and ran under the shared vendor lock. No area run overlaps another vendor instance.

Historical comparisons are retained: initial candidate and same-path repeat each measured 21621 LUT / 18909 FF (+179 / +19); a scratch comparator simplification measured 21597 / 18909 (+155 / +19); a scratch response-status/overlay-clear variant measured 21591 / 18905 (+149 / +15). Neither scratch variant was promoted. The final LD2 delay-expiry correction produces the final counts above. Test-only follow-up commits do not change the measured RTL. The LUT ceiling remains unmet, so REVIEW READY is unavailable.

Independent suites, campaigns and parent consumers ran concurrently, with four bounded compilation slots and 16 build jobs, under the 12 GiB service limit. The pinned 5.050 compiler is exported. Large products remain outside the output directory. The final runtime audit found no active build or simulation process. Peak memory reached the 12 GiB cap, with no OOM event or killed process; the detailed counters are in `final-runtime-audit.json`.

Campaigns use `python3 tb/<suite>/<driver>.py --output <scratch-result-dir> --jobs 2`; the talker retry driver uses `--logs` instead of `--output`, and the name-write driver has no jobs option. The final ACMP campaign uses `--jobs 4`. Compilation uses 16 jobs with four bounded slots. Parent make commands use 16 jobs; each campaign mode receives a jobs argument where that mode accepts one. The parent render leg-defect mode rejects `--jobs` (only its separate law-boundary mode accepts it), and the render-law/grandmaster-step drivers expose no jobs option.

## Artifacts and delivery

Large logs, binaries, source copies and generated products remain in scratch storage. Output contains only small documents, supplied patches, logs, receipts and manifests; large artifacts are represented by size and SHA-256. `HANDOFF-round1-stop.md` and the original diagnostic retain historical STOP context, superseded by the manager ruling. The final suite, campaign and parent tables follow. The output includes the complete processor patch, commit and scope receipts, source-hash receipts, planted-check witnesses, final campaign records, and small gate/area reports. Source exports, binaries and larger logs are represented only by size and SHA-256. `artifact-index.json` maps evidence groups to the split `external-artifacts-*.json` manifests; their `scratch/` prefix resolves to `$VALIDATION_STORAGE/pp168-a567/`. `SHA256SUMS` covers every other output file. The complete patch applies cleanly to the base source.

The prepared round 1b STOP comment names the final head and the failed area ceiling. It is posted as a new comment after the artifacts and final audit are complete. The original STOP comment and its diagnostic are retained unchanged. No push, PR operation or parent commit was performed.

The final parent style scan caught one overlong campaign expression. It was wrapped without changing its parsed syntax, committed, and pinned in the scratch parent. The failed first style receipt remains; the final scan and make check both returned 0. The completed campaign used identical compiled inputs and an identical parsed driver (verified in style-equivalence.json); an unnecessary duplicate repeat was cancelled and excluded.

<!-- VALIDATION_TABLES_START -->
## Processor suite bank

| Suite | Base checks | Head checks | Change |
| --- | ---: | ---: | --- |
| `acmp_listener` | 3111 | 3167 | +56: six clause cases |
| `acmp_nvm` | 388 | 388 | unchanged |
| `acmp_talker` | 1342 | 1376 | +34: invalid disconnect IDs |
| `adp_engine` | 1359 | 1359 | unchanged |
| `aecp_notify` | 65 | 65 | unchanged |
| `ca_originator` | 16 | 16 | unchanged |
| `desc_mem_guard` | 78 | 78 | unchanged |
| `desc_store` | 586 | 586 | unchanged |
| `dispatch` | 211 | 211 | unchanged |
| `dyn_state` | 118 | 118 | unchanged |
| `event_router` | 81 | 81 | unchanged |
| `lsn_admit` | 18 | 18 | unchanged |
| `maap` | 196 | 196 | unchanged |
| `nvm_port` | 1219 | 1219 | unchanged |
| `originator` | 107 | 107 | unchanged |
| `pp_top` | 10469 | 10470 | +1: VLAN checks and retry expectation |
| `prng` | 76 | 76 | unchanged |
| `release_merge` | 18 | 18 | unchanged |
| `resp_buf` | 64 | 64 | unchanged |
| `rx_slots` | 130 | 130 | unchanged |
| `rx_validator` | 555 | 555 | unchanged |
| `scoreboard` | 3705 | 3705 | unchanged |
| `side_port` | 368 | 368 | unchanged |
| `srp_admission` | 991231 | 991231 | unchanged |
| `srp_decoder` | 190 | 190 | unchanged |
| `srp_encoder` | 581 | 581 | unchanged |
| `srp_stream_fsms` | 1347 | 1347 | unchanged |
| `srp_top` | 8656 | 8656 | unchanged |
| `timer_map` | 1360 | 1360 | unchanged |
| `timer_service` | 48 | 48 | unchanged |
| `tx_arbiter` | 66 | 66 | unchanged |
| `tx_slots` | 95 | 95 | unchanged |
| `ucpu` | 437 | 437 | unchanged |

Base total: 1028291; head total: 1028382.

## Processor gates

| Command | Base rc | Head rc |
| --- | ---: | ---: |
| `scripts/run_suites.sh` | 0 | 0 |
| `scripts/lint_hdl.sh` | 0 | 0 |
| `make -j16 check` | 0 | 0 |
| `scripts/gen_matrix.py --check` | 0 | 0 |
| `syn/yosys/run.sh` | 0 | 0 |

## Affected campaigns

| Campaign | Base rc | Head rc | Latest completed driver summary |
| --- | ---: | ---: | --- |
| `acmp_talker-retry_mutants` | 0 | 0 | PASS: 62 mutants killed; 7 equivalence controls; 1 performance controls; baseline and restored rc 0 |
| `pp_top-acmp_mutants` | 0 | 0 | ACMP mutations: 51 of 51 KILLED by their named checks; goldens PASS |
| `pp_top-gsi_mutants` | 0 | 0 | GSI mutations: 20 detected by named checks; golden and restored PASS |
| `pp_top-d3_mutants` | 0 | 0 | D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS |
| `pp_top-aecp_dispatch_mutants` | 0 | 0 | 44 checks: 44 PASS, 0 FAIL |
| `pp_top-aecp_mutants` | 0 | 0 | 67 checks: 67 PASS, 0 FAIL |
| `pp_top-ctr_mutants` | 0 | 0 | 18 checks: 18 PASS, 0 FAIL |
| `pp_top-notify_mutants` | 0 | 0 | C6 notification mutations: 91 of 91 KILLED by their named checks; goldens PASS |
| `pp_top-name_wr_mutant` | 0 | 0 | Name-write mutation: decode killed; golden and restored PASS |
| `adp_engine-mutants` | 0 | 0 | 62 checks: 62 PASS, 0 FAIL |
| `maap-mutants` | 0 | 0 | 32 checks: 32 PASS, 0 FAIL |
| `srp_top-mutants` | 0 | 0 | 137 checks: 137 PASS, 0 FAIL |
| `srp_admission-mutants` | 0 | 0 | 12 checks: 12 PASS, 0 FAIL |

## Scratch-parent consumers

| Consumer | Base rc | Head rc |
| --- | ---: | ---: |
| `scripts/check_cpp_idiom.py` | 0 | 0 |
| `scripts/check_py_idiom.py` | 0 | 0 |
| `scripts/check_rtl_source_lists.py` | 0 | 0 |
| `scripts/pp_srcs.py --check --selftest` | 0 | 0 |
| `scripts/check_port_contracts.py` | 0 | 0 |
| `scripts/measure_naming.py --check` | 0 | 0 |
| `scripts/measure_test_evidence.py --check` | 0 | 0 |
| `scripts/docs_check.py` | 0 | 0 |
| `scripts/xvlog_gate.py --check` | 0 | 0 |
| `sw/builder/test_builder.py` | 0 | 0 |
| `scripts/lint_rtl.py --check` | 0 | 0 |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 |
| `make -j16 -C tb/verilator/nvm_cosim lint` | 0 | 0 |
| `make -j16 -C tb/verilator/nvm_cosim quick JOBS=16 POOL=2` | 0 | 0 |
| `make -j16 -C tb/verilator/milan_dp VERILATOR_JOBS=16` | 0 | 0 |
| `make -j16 -C tb/verilator/milan_dp_render VERILATOR_JOBS=16 MUTANT_JOBS=2` | 0 | 0 |
| `scripts/check_sh_idiom.py` | 0 | 0 |
<!-- VALIDATION_TABLES_END -->

## Record comparison

All unaffected campaign failure lists and canonical records are identical. Parallel completion order is ignored when comparing keyed records. The complete driver console is byte-identical for the AECP, counter, ADP, MAAP, SRP-top and SRP-admission campaigns. The only changes are the assigned clause checks and their documented effects:

| Evidence | Base/head comparison |
| --- | --- |
| ACMP | 35 of 37 old canonical records identical; two gain one new assigned-field failure each; 18 new mutant records and two added goldens |
| Talker retry | All 72 runs retain all earlier failure lines; 13 add TD1 witnesses |
| Integrated GSI | All 22 canonical records identical; five detailed traces change as explained above |
| D3 | All 116 canonical records and all old failure lists identical |
| Dispatch / notification / name-write | All 44 / 102 / 3 canonical records identical |
| Parent datapath | All 1152 result records identical after ignoring completion order |
| Parent render | All eight result records identical |
| Parent shadow | Four legs retain 646, 606, 606 and 311 checks |
| Parent NVM quick | 315 checks at both revisions |
| Parent inventory | C++ files 177 to 178 for the new field-test header; Python module count unchanged at 317, with lines 200295 to 200387 for the added planted checks |
| Parent structural and style consumers | Final commands all return zero; source-list, port, naming, evidence, documentation and shell result logs identical |

The historical parent builder report-calibration arm remains unrun at both revisions because its required report is absent. A zero command return is not claimed as execution of that arm. The area gate independently prevents acceptance.

## Round 2 — recovery in progress

The host reset invalidates every pre-reset Round 2 build and measurement. The Round 1 results above and any earlier Round 2 receipts are historical only; none is acceptance evidence for this recovery. All reported gates and area measurements will be rerun from clean generated outputs.

Verified clean branch head: `fee74ef977b0a56a98c2b8a8677e25cfdf994c08`. Its merge parents are `ba3f3f31e8fda01c3ef5271ff8005f3cf92ab4de` and baseline `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`. Origin is the assigned processor repository. The authorised main merge is complete. No second TAKEN comment, push, rebase, parent commit or PR operation is required.

The scratch parent is verified at `6aa25dec977c6ad78bf4ff6275de47fb81d0c246`. Both supplied adoption patches are already incorporated there; reverse application checks pass, and the regenerated empty adoption patches apply successfully. Pending: complete each individual correction and combined OOC 1x1; attempt measured reductions while retaining all six corrections and their planted defects; rerun processor gates, every affected campaign and parent consumers at baseline and final head; compare keyed records; remove the individual worktrees; publish REVIEW READY or STOP with the final head.

| Item | Clause | Baseline LUT/FF | Item LUT/FF | Delta LUT/FF | Reduction tried |
| --- | --- | --- | --- | --- | --- |
| LD1 | Milan Table 5.36 | 21614 / 18908 | 21500 / 18901 | -114 / -7 | Clause-required zero fields retained; shared serialization queued |
| LD2 | Milan 5.5.3.5.30/.10 | 21614 / 18908 | 21613 / 18908 | -1 / 0 | Retained status has no measured area cost |
| LD3 | IEEE Table 8-3 | 21614 / 18908 | 21628 / 18905 | +14 / -3 | Required constant retained; response-sharing trials retain status 16 |
| TD1 | Milan 5.5.4.2/Table 5.44 | 21614 / 18908 | 21614 / 18908 | 0 / 0 | Reuses existing source-valid comparison; no measured cost |
| VLAN | Milan 5.3.8.9/Table 5.38 | 21614 / 18908 | 21606 / 18925 | -8 / +17 | Full clause width retained |
| Probe guard | Milan 5.5.3.5.16/.17/.18 | 21614 / 18908 | 21750 / 18905 | +136 / -3 | Comparison and response-byte sharing queued |

The +40 LUT / +40 FF ceiling remains binding. Parent SRP treatment of a received value outside the valid VID range remains outside this processor assignment. Internal storage retains all 16 bits; the parent-facing VID remains the low 12 bits.

### Recovery progress

The fresh baseline OOC 1x1 at `09e357fb` returns 0 and measures 21,614 LUT / 18,908 FF. The report collector initially rejected the LUT row's footnote marker; its parser is corrected and the completed synthesis receipt is retained. The six item patches were reconstructed and checked as a disjoint, complete partition of every baseline-to-merge RTL difference. No item build is committed.

Baseline documentation and matrix gates return 0. Processor suites, all 13 affected campaigns and parent consumers are running from fresh generated outputs. Heavy compilation shares the synthesis exclusion lock, with three build slots and eight compiler slots; synthesis remains serial. Five reductions are queued for area measurement: compare before selection; omit the redundant private-word clear at unbind; select the controller byte before its source; select all identity bytes before their source; and omit the private-word clear at teardown. The first four pass all 3,167 listener checks. The fifth listener run is queued. No new expectation or assertion is introduced by these reductions. The fresh guard-only measurement returns 0 at 21,750 LUT / 18,905 FF, a delta of +136 LUT / -3 FF. The parent source, port, naming, evidence, documentation, analysis and NVM consumers have returned 0; remaining consumers are running.

All six fresh single-item measurements are complete. Their deltas sum to +27 LUT / +4 FF. The fresh combined merge measures 21,741 LUT / 18,922 FF (+127 / +14), exceeding the LUT ceiling. Its delta is +100 LUT / +10 FF above the individual-delta sum. Five reduction measurements remain pending. All eight baseline, item and combined synthesis commands returned 0.

The first fresh reduction, selecting between controller equality results, measures 21,665 LUT / 18,924 FF (+51 / +16). It saves 76 LUT against the merged implementation but remains 11 LUT above the ceiling. The state-dependent fallback comparison is retained to preserve early-consume versus inert-write classification outside pending-probe states.

Removing the unbind private-word clear after the comparison change increases area to 21,732 LUT / 18,922 FF (+118 / +14). This trial is worse than retaining that clear; source-code simplification is not assumed to reduce mapped area.

The controller-byte reduction is selected and committed as `96d3b78384f34a630d6056ebd8fa5e30f6836650`. It measures 21,643 LUT / 18,922 FF (+29 / +14), saving 98 LUT against the merged implementation. All final HDL hashes match that measured input exactly. The listener suite passes all 3,167 checks. The final five processor gates and all 13 affected campaigns have started from a fresh archive of this commit. The two broader identity-serialization trials remain supporting measurements; the selected implementation limits byte-selection changes to the controller field. No assertion or expected failure was removed.

The broader identity-octet trial measures 21,622 LUT / 18,922 FF (+8 / +14), also within the ceiling. The controller-only variant remains selected to limit response-builder changes while meeting the required ceiling. Final documentation and matrix checks return 0.
