### Round 2 gate table, final head `48f12dc14`

The suites ran on the tree of `48f12dc14`. The re-record commit changes only the resource JSON and three docs, none of them a suite or build input, so its parent `e519e31ff` has the same RTL, testbenches and firmware. Pinned Verilator 5.050, `VERILATOR_JOBS=2`, at most two Verilator builds at once. Each command ran unpiped with its own log and rc.

| Gate | Command | rc | Result |
|---|---|---|---|
| maap suite | `make -C tb/verilator/maap` | 0 | `KL_maap: 130 checks, 0 failures`; `maap mutants: checks: 27   failures: 0` (186 s) |
| maap coverage | `make -C tb/verilator/maap coverage` | 0 | `KL_maap.sv` line 100.0 % (169/169), gate 95 % PASS |
| milan_dp | `make -C tb/verilator/milan_dp` | 0 | 12,065 checks, 0 failures, including the crflic leg's 417 (2,641 s) |
| crflic campaign | `make -C tb/verilator/milan_dp crflic-mutants` | 0 | leg 417 checks 0 failures; `7 checks: 7 PASS` (748 s) |
| pp_shadow | `make -C tb/verilator/pp_shadow` | 0 | 2,184 checks, 0 failures (732 s), at processor `2ad2f845` |
| capture_coherence | `make -C tb/verilator/capture_coherence` | 0 | 21,194 checks, 0 failures (645 s) |
| milan_dp_mclk | `make -C tb/verilator/milan_dp_mclk` | 0 | 168 checks, 0 failures (535 s) |
| milan_dp_render | `make -C tb/verilator/milan_dp_render` | 0 | 334 checks, 0 failures (820 s) |
| suite tally | `scripts/suite_tally.py` over the six logs | 0 | 36,102 checks, 0 in-suite failures |
| ctrl suite | `MILAN_RV32_CC=<verified SDK>/bin/riscv32-linux-gcc test_ctrl_firmware.py --require-rv32 --jobs 4` | 0 | `test_ctrl_firmware: PASS`, RV32 arm included (dev's merged firmware) |
| differential | `maap_differential.py` / `--self-test` | 0 / 0 | 12/12; 16/16 controls caught |
| lint ratchet | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| parser ratchet | `scripts/xvlog_gate.py --check` (Vivado 2026.1 xvlog, under the lock, alone) | 0 | `0 finding(s) == ratchet; 0 hdl/, 0 pinned processors` (535 s; #682's pin cleared the two processor findings) |
| Yosys OOC | `syn/yosys/ooc.sh KL_maap` | 0 | 515 LUT / 278 FF / 59 CARRY4 |
| Yosys portability | `syn/yosys/run.sh --top KL_maap` | 0 | PASS; tied-input and tap-purity PASS |
| test evidence | `measure_test_evidence.py --check` / `--selftest` | 0 / 0 | 0 unexplained readers; 105/105 |
| docs and code quality | the 24-command set (as Part A), plus `check_em_dash.py --base 291710b1` and `git diff --check 291710b1 HEAD` against the dev tip | all 0 | at `48f12dc14` |
| shipping route and standalone endpoints | the recipe, `--single-thread-synthesis` (Part B section) | 0 / 0 | route 2,937 s; standalone 3,881 s |
| resource gate | `pp_resource_gate.py check` x3 against F; `record --write` x3; `check-baseline`; `check` x3 against the new record | all 0 | PASS x3 (route LUT +434 of +500, slices +54 of +80, WNS +0.241, WHS +0.029); `baseline PASS: 3 endpoints` at `48f12dc14` |
| gate self-tests | `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py` | 0 / 0 | 260 arms + 500 cases; 174 of 174 mutants fail |
| receipts | `regen_record.py` x3 per record set, `--git 48f12dc1` and `--git c7b69cd0` | 0 x6 | `record EQUAL` x6 |

