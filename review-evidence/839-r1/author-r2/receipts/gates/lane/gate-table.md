| Gate | Command | rc | Verdict line in the log |
|---|---|---:|---|
| behave | `cd tests && behave` | 0 | Took 0min 2.954s |
| bootsa_mutants | `make -C tb/verilator/milan_dp bootsa-mutants` | 0 | 13 checks: 13 PASS, 0 FAIL |
| builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN |
| diffcheck | `git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD` | 0 |  |
| docs_inventory_absent | `test -z "$(git ls-tree --name-only HEAD scripts/docs_inventory.py)" && test -z "$(git ls-tree --name-only 604899c08ff1cd1830e1dd08b733109ef852400c scripts/docs_inventory.py)" && echo 'scripts/docs_inventory.py is in neither tree: NOT RUN'` | 0 |  |
| fw_coverage_check | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8` | 0 | firmware coverage: PASS (30 files) |
| fw_coverage_selftest | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | [ok] gcc: a condition over two lines, its other operand uncovered instead: exclusion sw/firmware/ctrl/two_lines.c m(): `if (a > 0 &&`: arcs [3] of the statement's 4 are uncovered, the row names [4] |
| fw_nvm | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests |
| fw_rv32_selftest | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | RV32 build self-test: 17 checks PASS |
| fw_selftest_0 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4` | 0 | test_ctrl_firmware: PASS |
| fw_selftest_1 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4` | 0 | test_ctrl_firmware: PASS |
| fw_selftest_2 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4` | 0 | test_ctrl_firmware: PASS |
| fw_selftest_3 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4` | 0 | test_ctrl_firmware: PASS |
| fw_tally_selftest | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | [ok] a disabled test, GTEST_ALSO_RUN_DISABLED_TESTS=1 in the environment: exit 0, tally 0/1, its tallies report 1 failure(s) across 0 checks |
