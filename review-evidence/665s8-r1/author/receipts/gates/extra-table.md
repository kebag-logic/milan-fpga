| Gate | Command | rc | Log |
|---|---|---:|---|
| diff-check | `git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD` | 0 | `extra/logs/diff-check.log` |
| tally-mutants | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | `extra/logs/tally-mutants.log` |
| nvm-self-test | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | 0 | `extra/logs/nvm-self-test.log` |
| test-builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | `extra/logs/test-builder.log` |
| budget-self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 | `extra/logs/budget-self-test.log` |
| budget-1x1 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <gates>/extra/budget-1x1 --record-budget-findings` | 0 | `extra/logs/budget-1x1.log` |
| budget-8x8 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <gates>/extra/budget-8x8 --record-budget-findings` | 0 | `extra/logs/budget-8x8.log` |
| wire-8x8-none | `python3 -B tb/verilator/ctrl_wire_timing/run.py --point 8x8 --build-dir <gates>/extra/wire-8x8 --draws 16 --load none --out <gates>/extra/wire-8x8-none` | 0 | `extra/logs/wire-8x8-none.log` |
| wire-8x8-composed | `python3 -B tb/verilator/ctrl_wire_timing/run.py --reuse-build --build-dir <gates>/extra/wire-8x8 --draws 16 --load composed --out <gates>/extra/wire-8x8-composed` | 0 | `extra/logs/wire-8x8-composed.log` |

Tree after: tree-after-wt.txt clean; tree-after-wt2.txt clean

9 gates, 0 bad
