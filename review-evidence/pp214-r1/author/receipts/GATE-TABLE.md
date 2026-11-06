# Gate table at the head

### Processor gates

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| elab_guards | 0 | 496 | elab guards: 93 checks: 93 PASS, 0 FAIL |
| gen_matrix_check | 0 | 1 | matrix: OK (94 rows, 0 untested) |
| lint_hdl_5050 | 0 | 33 | LINT OK  protocol_processor_top |
| lint_hdl_5052 | 0 | 57 | LINT OK  protocol_processor_top |
| make_check | 0 | 119 | figures: 3 draw.io, 18 WaveDrom, 5 hand-authored, OK |
| yosys_run | 0 | 196 | YOSYS XILINX OK  KL_aecp_engine |
| check_req_tags_exec | 0 | 0 | req-tags executed: 266 evidence lines, 14 suites, OK |
| run_suites | 0 | 6989 | suites: 1031116 checks total, 0 failing |
| area_head | 0 | 701 | / srp_top_8x8 / 28002 / 4399 / 11297 / 179 / 580 / 190 / |

every gate rc 0

### Processor campaigns

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| camp-acmp | 0 | 3590 | ACMP mutations: 103 of 103 KILLED by their named checks; goldens PASS |
| camp-acmp-retry | 0 | 226 | PASS: 62 mutants killed; 7 equivalence controls; 1 performance controls; baseline and restored rc 0 |
| camp-adp | 0 | 557 | 62 checks: 62 PASS, 0 FAIL |
| camp-aecp | 0 | 1511 | 67 checks: 67 PASS, 0 FAIL |
| camp-aecp-cmds | 0 | 578 | AECP command decode controls: 17 of 17 detected by their named failures; golden and restored PASS |
| camp-aecp-dispatch | 0 | 3694 | 105 checks: 105 PASS, 0 FAIL |
| camp-ctr | 0 | 476 | 18 checks: 18 PASS, 0 FAIL |
| camp-d3 | 0 | 7988 | D3 mutations: 110 of 110 KILLED by their named checks; goldens PASS |
| camp-elab-guards | 0 | 980 | elab guard mutants: 160 of 160 killed |
| camp-gsi | 0 | 1361 | GSI mutations: 30 detected by named checks; golden and restored PASS |
| camp-maap | 0 | 164 | 32 checks: 32 PASS, 0 FAIL |
| camp-name-state | 0 | 777 | 16 of 16 KILLED by name; golden PASS |
| camp-name-wr | 0 | 138 | Name-write mutation: decode killed; golden and restored PASS |
| camp-notify | 0 | 3301 | C6 notification mutations: 137 of 137 KILLED by their named checks; goldens PASS |
| camp-nvm-figures | 0 | 1187 | all measured figures agree with the tree |
| camp-srp | 0 | 4187 | 291 checks: 291 PASS, 0 FAIL |
| camp-srp-admission | 0 | 817 | 12 checks: 12 PASS, 0 FAIL |

every gate rc 0

### Scratch-parent consumer gates

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| rom_digests | 0 | 0 | ooc.sh: recorded ROM content digests for protocol-processor pin cc92e90a95376151a9ebd484c429bc53feb8573c and g |
| behave | 0 | 10 | 2330 steps passed, 0 failed, 0 skipped |
| cache_selftest | 0 | 171 | cache selftest: OK (unit self-test + 5 original live arms on cdc_pulse + ROM controls) |
| check_cpp_idiom | 0 | 7 | build without warnings: 0 <= 0 |
| check_cpp_idiom_selftest | 0 | 7 | 75 checks: 75 PASS, 0 FAIL |
| check_doc_paths | 0 | 0 | doc path gate: OK (1092 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| check_hygiene | 0 | 1 | HYGIENE RATCHET: PASS (3 population(s), 1308 file(s)) |
| check_port_contracts | 0 | 7 | port contract gate: OK (4081 first-party port(s): hdl 2182, gptp-processor 127, protocol-processor 1772; 347 u |
| check_py_idiom | 0 | 33 | over-long line: 0 <= 0 |
| check_py_idiom_selftest | 0 | 33 | 54 checks: 54 PASS, 0 FAIL |
| check_rtl_source_lists | 0 | 4 | RTL source-list gate: OK (112 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them;  |
| check_sh_idiom | 0 | 1 | top-heavy long script: 0 <= 0 |
| check_sh_idiom_selftest | 0 | 1 | 48 checks: 48 PASS, 0 FAIL |
| check_sv_idiom | 0 | 2 | SystemVerilog idiom gate: OK (141 first-party HDL file(s) across the superproject and both processor submodule |
| check_sv_idiom_selftest | 0 | 1 | 55 checks: 55 PASS, 0 FAIL |
| ci_scope_classify | 0 | 0 | syn/yosys/rom_digests.tsv |
| ci_scope_selftest | 0 | 83 | selftest: PASS |
| docs_check | 0 | 22 | docs_check: 0 finding(s) across 213 md files + 1440 scrubbed text files, scrub self-test 23/23, routing arms 4 |
| fw_boundary | 0 | 2502 | ctrl_boundary: PASS |
| fw_coverage | 0 | 707 | firmware coverage: PASS (30 files) |
| fw_coverage_selftest | 0 | 1 | coverage self-test: 29 of 29 planted cases read as planted |
| fw_ctrl_nvm | 0 | 280 | saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests |
| fw_rv32_sdk_selftest | 0 | 5 | OK |
| fw_rv32_selftest | 0 | 22 | RV32 build self-test: 17 checks PASS |
| fw_shard0 | 0 | 889 | test_ctrl_firmware: PASS |
| fw_shard1 | 0 | 3170 | test_ctrl_firmware: PASS |
| fw_shard2 | 0 | 947 | test_ctrl_firmware: PASS |
| fw_shard3_srp | 0 | 1911 | test_ctrl_firmware: PASS |
| fw_tally_selftest | 0 | 10 | tally self-test: 18 of 18 planted cases read as planted |
| fw_verilator | 0 | 1243 | ctrl_boundary: PASS |
| guard_selftest | 0 | 107 | elaboration guard self-test: 36 controls passed |
| lint_rtl | 0 | 42 | LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off) |
| measure_fail_fast | 0 | 7 | FAIL-FAST RATCHET: PASS (78 <= 84 modules without an elaboration contract, 3 <= 4 masked pipeline(s), 0 <= 0 d |
| measure_naming | 0 | 1 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| measure_test_evidence | 0 | 29 | TEST-EVIDENCE RATCHET: PASS (67 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded draw site(s), 0 <= 0  |
| milan_dp | 0 | 6425 | 6 checks: 6 PASS, 0 FAIL |
| milan_dp_mclk | 0 | 2617 | 34 checks: 34 PASS, 0 FAIL |
| milan_dp_render | 0 | 2876 | 5 checks: 5 PASS, 0 FAIL (--leg-defects: the arms that need no elaboration; the gateware and shape mutants are |
| ooc_read_sets | 0 | 1841 | baseline PASS: 3 endpoints |
| ooc_selftest | 0 | 113 | ooc.sh refusal self-test: 75 arm(s) passed |
| pp_shadow | 0 | 1314 | RESULT: PASS |
| pp_srcs | 0 | 1 | pp source list: 46 tracked source(s) derived; no build input carries a literal copy (self-test passed) |
| publication_census | 0 | 2317 | 26 class-D net(s) from the wrapper cell's ports, 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESU |
| yosys_elaborate | 0 | 318 | RESULT: PASS |

every gate rc 0

