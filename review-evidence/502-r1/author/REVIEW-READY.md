[A338] REVIEW READY

Commit: `87e263fd1d71b1a7a04a2e9c9339220f35e4348f` (local head; not pushed).

Changed: adopted processor `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`, regenerated its ROM ledger and diagram,
connected `aecp_name_wr_o`, and made accepted name/map writes revoke durable
status on the accepting edge. Pending stays sticky until reset. Real-command
K10/K12 tests, controls, the late-mark mutant and authoritative docs are included.

Validation (all commands exited 0):

- `make -C tb/verilator/pp_shadow`: 520 + 520 + 520 + 159 checks;
  `make -C tb/verilator/pp_shadow pending-mutant`: clean 159 checks, both
  required K10/K12 mutant failures detected.
- `make -C tb/verilator/nvm_cosim` and `make -C tb/verilator/nvm_backend` passed.
- `SUITE_TIMEOUT=10800 scripts/run_all_suites.sh <logs> --shard N/6`, for every
  N from 0 through 5, passed: 55 distinct suites, 2125050 checks, zero
  failures. The complete `milan_dp` chunk passed 11,206 checks.
  Optional AAF/AVTP and gPTP field campaigns and their freshness checks
  were skipped because `tsn-gen` is absent, contributing zero to that total.
- `syn/yosys/ooc.sh KL_pp_shadow`, before and after at the same adopted pin:
  LUT 60855 -> 60766; FF, LUTRAM, BRAM and DSP unchanged.
- Full `python3 sw/builder/test_builder.py` in both requested modes passed.
  The SDK run used `--require-rv32` and the assignment's compiler mapping;
  855 actual compiler invocations used the pinned SDK. The other run hid all
  three RV32 candidates. Both exclude the unavailable board calibration
  report; only the absent run excludes the RV32 census.
- `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`,
  `python3 scripts/check_nvm_capture.py`, and
  `python3 scripts/check_baremetal_only.py --check` passed. Firmware is unchanged.
- Both CI modes of `python3 -B scripts/docs_check.py` passed. The requested
  `ci_events --check/--selftest`, `check_em_dash --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`,
  `check_doc_style`, `gen_toc --check/--verify-anchors`, `check_doc_paths`,
  `gen_module_matrix --check`, `xvlog_gate --check`, `check_rtl_source_lists`,
  `check_sv_idiom`, `lint_rtl --check`, `check_cpp_idiom`, `check_py_idiom`,
  `check_port_contracts`, `measure_naming --check`, and
  `measure_test_evidence --check` gates all passed.
- `cd tests && behave --no-capture -f plain`: 344 scenarios, 1739 steps passed.
  `git diff --check` passed; parent and processor worktrees are clean.

Acceptance criteria: assignment items 1-4 met. The clean harness observes zero
falsely durable cycles; the late-mark mutant exposes 1881 for K10 and 15 for
each K12 map direction. Unchanged/refused commands, repeated commands, reset,
and an accepted ARM/ATTEST/ACK sequence are covered.

Evidence: `HANDOFF.md` and `PR-BODY.md` are complete in the assigned output
directory, with file:line changes, exact gate records, raw logs and area tables.
The initial colliding builder runs and interrupted sweep were discarded;
both builder modes and all six accepted sweep chunks ran serially.

Open limits: no name/map record materializer or flash-persistence claim is added.
Independent review and hosted contexts remain outstanding. No push, PR change,
merge, hardware operation or donor-source edit was performed. The separate
#567 integration round remains with the maintainer.
