# Gate table at the head

### Processor gates

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| diff_check | 0 | 1 | (no output) |
| gen_matrix_check | 0 | 0 | matrix: OK (94 rows, 0 untested) |
| lint_hdl_5050 | 0 | 70 | LINT OK  protocol_processor_top |
| make_check | 0 | 30 | lint: 41 mermaid + 18 wavedrom blocks checked, OK |
| srp_encoder | 0 | 5 | 888 checks: 888 PASS, 0 FAIL |
| srp_top | 0 | 548 | 8683 checks: 8683 PASS, 0 FAIL |

every gate rc 0

### SRP mutant campaign

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| camp-srp | 0 | 4055 | 310 checks: 310 PASS, 0 FAIL |

every gate rc 0

### Scratch-parent consumer gates

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| rom_digests | 0 | 1 | ooc.sh: recorded ROM content digests for protocol-processor pin 1c8b485f5eebfa8efaba6f5facbade7e5aa4caaa and g |
| behave | 0 | 13 | 2330 steps passed, 0 failed, 0 skipped |
| cache_selftest | 0 | 169 | cache selftest: OK (unit self-test + 5 original live arms on cdc_pulse + ROM controls) |
| check_cpp_idiom | 0 | 2 | build without warnings: 0 <= 0 |
| check_cpp_idiom_selftest | 0 | 2 | 75 checks: 75 PASS, 0 FAIL |
| check_doc_paths | 0 | 0 | doc path gate: OK (1092 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| check_hygiene | 0 | 1 | HYGIENE RATCHET: PASS (3 population(s), 1308 file(s)) |
| check_port_contracts | 0 | 4 | port contract gate: OK (4081 first-party port(s): hdl 2182, gptp-processor 127, protocol-processor 1772; 347 u |
| check_py_idiom | 0 | 8 | over-long line: 0 <= 0 |
| check_py_idiom_selftest | 0 | 7 | 54 checks: 54 PASS, 0 FAIL |
| check_rtl_source_lists | 0 | 2 | RTL source-list gate: OK (112 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them;  |
| check_sh_idiom | 0 | 0 | top-heavy long script: 0 <= 0 |
| check_sh_idiom_selftest | 0 | 1 | 48 checks: 48 PASS, 0 FAIL |
| check_sv_idiom | 0 | 1 | SystemVerilog idiom gate: OK (141 first-party HDL file(s) across the superproject and both processor submodule |
| check_sv_idiom_selftest | 0 | 0 | 55 checks: 55 PASS, 0 FAIL |
| ci_scope_classify | 0 | 0 | syn/yosys/rom_digests.tsv |
| ci_scope_selftest | 0 | 34 | selftest: PASS |
| docs_check | 0 | 6 | docs_check: 0 finding(s) across 213 md files + 1440 scrubbed text files, scrub self-test 23/23, routing arms 4 |
| fw_boundary | 0 | 1151 | ctrl_boundary: PASS |
| fw_coverage | 0 | 241 | firmware coverage: PASS (30 files) |
| fw_coverage_selftest | 0 | 1 | coverage self-test: 29 of 29 planted cases read as planted |
| fw_ctrl_nvm | 0 | 94 | saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests |
| fw_rv32_sdk_selftest | 0 | 1 | OK |
| fw_rv32_selftest | 0 | 6 | RV32 build self-test: 17 checks PASS |
| fw_shard0 | 0 | 300 | test_ctrl_firmware: PASS |
| fw_shard1 | 0 | 1169 | test_ctrl_firmware: PASS |
| fw_shard2 | 0 | 280 | test_ctrl_firmware: PASS |
| fw_shard3_srp | 0 | 844 | test_ctrl_firmware: PASS |
| fw_tally_selftest | 0 | 4 | tally self-test: 18 of 18 planted cases read as planted |
| fw_verilator | 0 | 674 | ctrl_boundary: PASS |
| guard_selftest | 0 | 100 | elaboration guard self-test: 36 controls passed |
| lint_rtl | 0 | 14 | LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off) |
| measure_fail_fast | 0 | 2 | FAIL-FAST RATCHET: PASS (78 <= 84 modules without an elaboration contract, 3 <= 4 masked pipeline(s), 0 <= 0 d |
| measure_naming | 0 | 1 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| measure_test_evidence | 0 | 12 | TEST-EVIDENCE RATCHET: PASS (67 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded draw site(s), 0 <= 0  |
| milan_dp | 0 | 3763 | 6 checks: 6 PASS, 0 FAIL |
| milan_dp_mclk | 0 | 1332 | 34 checks: 34 PASS, 0 FAIL |
| milan_dp_render | 0 | 852 | 5 checks: 5 PASS, 0 FAIL (--leg-defects: the arms that need no elaboration; the gateware and shape mutants are |
| ooc_read_sets | 0 | 1579 | baseline PASS: 3 endpoints |
| ooc_selftest | 0 | 104 | ooc.sh refusal self-test: 75 arm(s) passed |
| pp_shadow | 0 | 360 | RESULT: PASS |
| pp_srcs | 0 | 0 | pp source list: 46 tracked source(s) derived; no build input carries a literal copy (self-test passed) |
| publication_census | 0 | 1062 | 26 class-D net(s) from the wrapper cell's ports, 4 unread; 41 read(s) of 22 class-D net(s) in each shape; RESU |
| yosys_elaborate | 0 | 521 | RESULT: PASS |

every gate rc 0

