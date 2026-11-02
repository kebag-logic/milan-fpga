| Gate | Command | Head | rc | Result | Receipt |
|---|---|---|---:|---|---|
| diffcheck | `git diff --check f4c9ad4f HEAD` (the merge base) | `c954b8a9` | 0 | # head c954b8a91e720f87d2dfa9294c8501058dc55df3 gate diffcheck: git diff --check f4c9ad4f06f185378fd2646298aab51dd108e86f HEAD | `gates/lane/diffcheck.log` |
| diffcheck_merge | `git diff --check a68536fa HEAD` | `c954b8a9` | 0 | # head c954b8a91e720f87d2dfa9294c8501058dc55df3 gate diffcheck_merge: git diff --check a68536fa4cf8ce65c513874722de2e3ba83c2d00 HEAD | `gates/lane/diffcheck_merge.log` |
| py_idiom | `scripts/check_py_idiom.py` | `c954b8a9` | 0 | over-long line: 0 <= 0 | `gates/lane/py_idiom.log` |
| cpp_idiom | `scripts/check_cpp_idiom.py` | `c954b8a9` | 0 | build without warnings: 0 <= 0 | `gates/lane/cpp_idiom.log` |
| harness_selftest | `tb/verilator/ctrl_service_budget/run.py --self-test` | `c954b8a9` | 0 | self-test: 0 failures | `gates/lane/harness_selftest.log` |
| fw_coverage | `sw/firmware/gtest/fw_coverage.py --check` | `c954b8a9` | 0 | firmware coverage: PASS (38 files) | `gates/lane/fw_coverage.log` |
| fw_rv32_selftest | `sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | `c954b8a9` | 0 | RV32 build self-test: 25 checks PASS | `gates/lane/fw_rv32_selftest.log` |
| gen_mailbox | `sw/mailbox/gen_mailbox.py --check --crosscheck` | `c954b8a9` | 0 | gen_mailbox: 0 finding(s) | `gates/lane/gen_mailbox.log` |
| gen_mailbox_selftest | `sw/mailbox/gen_mailbox.py --selftest` | `c954b8a9` | 0 | selftest: 0 arm(s) failed | `gates/lane/gen_mailbox_selftest.log` |
| census | `sw/mailbox/publication_census.py --check --selftest` | `c954b8a9` | 0 | mutations: 0 of 43 rule(s) no arm proves | `gates/lane/census.log` |
| lint_rtl | `scripts/lint_rtl.py --check` | `c954b8a9` | 0 | LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off) | `gates/lane/lint_rtl.log` |
| soc_options | `sw/builder/test_soc_options.py` | `c954b8a9` | 0 | RESULT: PASS | `gates/lane/soc_options.log` |
| ctrl_memory | `sw/litex/test_ctrl_memory.py` | `c954b8a9` | 0 | RESULT: PASS | `gates/lane/ctrl_memory.log` |
| boundary_a | `ctrl_boundary.py --require-rv32 --selftest --without verilator` | `c954b8a9` | 0 | ctrl_boundary: PASS | `gates/lane/boundary_a.log` |
| boundary_b | `ctrl_boundary.py --require-rv32 --selftest --only verilator` | `c954b8a9` | 0 | ctrl_boundary: PASS | `gates/lane/boundary_b.log` |
| behave | `cd tests && behave --no-capture -f plain` | `c954b8a9` | 0 | 508 scenarios passed, 0 failed, 0 skipped | `gates/lane/behave.log` |
| test_builder | `sw/builder/test_builder.py --require-rv32` | `c954b8a9` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN | `gates/lane/test_builder.log` |
| boot_1x1 | `tb/verilator/ctrl_split_boot/run.py`, 1x1 | `c954b8a9` | 0 | BOOT ready at bus cycle 2465983 (2465983 CPU cycles): 24.660 ms against 20000 ms; banners 1 | `gates/lane/boot_1x1.log` |
| boot_8x8 | `tb/verilator/ctrl_split_boot/run.py --shape endstation_ax7101_8x8` | `c954b8a9` | 0 | BOOT ready at bus cycle 6427118 (6427118 CPU cycles): 64.271 ms against 20000 ms; banners 1 | `gates/lane/boot_8x8.log` |
| boot_native | `... --native-controls` | `c954b8a9` | 0 | ctrl_split_boot native controls: 6 of 6 as required | `gates/lane/boot_native.log` |
| boot_plants | `... --self-test` | `c954b8a9` | 0 | ctrl_split_boot self-test: 6 of 6 native controls as required; 2 of 2 plants caught | `gates/lane/boot_plants.log` |
| firmware self-test, shard 0/4 | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard 0/4` | `c954b8a9` | 0 | test_ctrl_firmware: PASS | `gates/fw/fwfinal-0.log` |
| firmware self-test, shard 1/4 | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard 1/4` | `c954b8a9` | 0 | mutants: 603 of 603 caught | `gates/fw/fwfinal-1.log` |
| firmware self-test, shard 2/4 | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard 2/4` | `c954b8a9` | 0 | test_ctrl_firmware: PASS | `gates/fw/fwfinal-2.log` |
| firmware self-test, shard 3/4 | `test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard 3/4` | `c954b8a9` | 0 | test_ctrl_firmware: PASS | `gates/fw/fwfinal-3.log` |
| store's plants | `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test` | `c954b8a9` | 0 | saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests, and all 110 planted defects reddened | `gates/fw/nvmself.log` |
| sweep, shard 0/4 | `bash scripts/run_all_suites.sh <logs> --wait --shard 0/4`, pinned Verilator 5.050, sv2v v0.0.12, `--no-print-directory` | `c954b8a9` | 0 | 15 suites, 15 passed, 360921 checks, 0 failures | `gates/sweep/shard-0/` |
| sweep, shard 1/4 | `bash scripts/run_all_suites.sh <logs> --wait --shard 1/4`, pinned Verilator 5.050, sv2v v0.0.12, `--no-print-directory` | `c954b8a9` | 0 | 17 suites, 17 passed, 1946931 checks, 0 failures | `gates/sweep/shard-1/` |
| sweep, shard 2/4 | `bash scripts/run_all_suites.sh <logs> --wait --shard 2/4`, pinned Verilator 5.050, sv2v v0.0.12, `--no-print-directory` | `c954b8a9` | 0 | 17 suites, 17 passed, 284228 checks, 0 failures | `gates/sweep/shard-2/` |
| sweep, shard 3/4 | `bash scripts/run_all_suites.sh <logs> --wait --shard 3/4`, pinned Verilator 5.050, sv2v v0.0.12, `--no-print-directory` | `c954b8a9` | 0 | 16 suites, 16 passed, 21575 checks, 0 failures | `gates/sweep/shard-3/` |
