# Gate table at the head

### Processor gates

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| diff_check | 0 | 1 | (no output) |
| gen_matrix_check | 0 | 0 | matrix: OK (94 rows, 0 untested) |
| lint_hdl_5050 | 0 | 10 | LINT OK  protocol_processor_top |
| make_check | 0 | 32 | lint: 41 mermaid + 18 wavedrom blocks checked, OK |
| srp_encoder | 0 | 5 | 1604 checks: 1604 PASS, 0 FAIL |
| srp_top | 0 | 551 | 8683 checks: 8683 PASS, 0 FAIL |

every gate rc 0

### SRP mutant campaign

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| camp-srp | 0 | 3412 | 314 checks: 314 PASS, 0 FAIL |

every gate rc 0

### Scratch-parent consumer gates

| Gate | rc | s | Last tally or verdict line |
|---|---|---|---|
| rom_digests | 0 | ? | ooc.sh: recorded ROM content digests for protocol-processor pin 7feeccea3a6c8210ece8d5d1d8929d67582163f9 and g |
| check_cpp_idiom | 0 | 2 | build without warnings: 0 <= 0 |
| check_cpp_idiom_selftest | 0 | 2 | 75 checks: 75 PASS, 0 FAIL |
| check_doc_paths | 0 | 0 | doc path gate: OK (1092 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| check_hygiene | 0 | 1 | HYGIENE RATCHET: PASS (3 population(s), 1308 file(s)) |
| check_port_contracts | 0 | 3 | port contract gate: OK (4081 first-party port(s): hdl 2182, gptp-processor 127, protocol-processor 1772; 347 u |
| check_py_idiom | 0 | 7 | over-long line: 0 <= 0 |
| check_py_idiom_selftest | 0 | 8 | 54 checks: 54 PASS, 0 FAIL |
| check_rtl_source_lists | 0 | 3 | RTL source-list gate: OK (112 files in the milan_datapath closure, 4 of 4 consumer list(s) carry all of them;  |
| check_sh_idiom | 0 | 0 | top-heavy long script: 0 <= 0 |
| check_sh_idiom_selftest | 0 | 1 | 48 checks: 48 PASS, 0 FAIL |
| check_sv_idiom | 0 | 1 | SystemVerilog idiom gate: OK (141 first-party HDL file(s) across the superproject and both processor submodule |
| check_sv_idiom_selftest | 0 | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs_check | 0 | 6 | docs_check: 0 finding(s) across 213 md files + 1440 scrubbed text files, scrub self-test 23/23, routing arms 4 |
| measure_fail_fast | 0 | 2 | FAIL-FAST RATCHET: PASS (78 <= 84 modules without an elaboration contract, 3 <= 4 masked pipeline(s), 0 <= 0 d |
| measure_naming | 0 | 0 | NAMING RATCHET: PASS (95 candidate(s), all recorded by identity; 95 recorded) |
| measure_test_evidence | 0 | 13 | TEST-EVIDENCE RATCHET: PASS (67 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded draw site(s), 0 <= 0  |

every gate rc 0

