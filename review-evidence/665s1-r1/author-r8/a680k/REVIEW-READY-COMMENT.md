[A680k] REVIEW READY
Commit: `614635b7f9aed7c9138aef53d0b93ca6030ae31e` (PR #795, two commits on `bdad673a`; nothing pushed)
Changed (ruling issuecomment-6463964028):
- Item 1, `tb/verilator/ctrl_service_budget/run.py`: the `as-built` control is caught by a trap refusal naming an access fault of cause 1 (fetch) or cause 5 (load), `AS_BUILT_CAUSES = (1, 5)` in `as_built_faults`, the cause matched as a whole field with interrupt bit 0. Either cause is #791's decode defect.
- Planted control, self-test half (`selftest.py` `as_built_checks`): synthetic boot-fault logs go through `grade.grade` and `run.verdict`. Cause 1 and cause 5 are caught. A clean boot, causes 2, 7 and 15, an interrupt numbered 5 and a bus error all escape. Four mutants (`selftest_mutants.py`), each caught: cause 1 only (the earlier rule), any trap, the cause's leading digit, caught whatever the boot does.
- Planted control, real half: a 1x1 build under `--cpu-regions as-built` with the CPU generator handed the regions' power-of-two cover, i.e. a clean image (arm A's CPU netlist). It boots with 0 traps, reaches `aecp_image_load` (0xbbc4) by 7 ms, and prints `CONTROL as-built ESCAPED`, rc 1.
- README and a `scenario.py` docstring state the rule and this head's result.
- Item 2: the PR body states arm B's SET_CONFIGURATION 1x1 T_svc miss (11.660 ms) and 8x8 if0 ceiling excess (26.980 ms over 24 ms), with #801 as the cause, out of scope.
Validation (all at `614635b7`, rc 0):
- `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 91 PASS, 68 MUTANT caught, 0 escaped.
- `run.py --point 1x1 --cpu-regions as-built`: `CONTROL as-built caught`, `TRAP 166 0 5 00000020`, rc 0 (at `124191ca`; `614635b7` is README only). The planted clean image: ESCAPED, rc 1, as required.
- Docs workflow: 69 of 69 commands rc 0, including `check_em_dash.py --base`, `check_py_idiom.py` and `check_baremetal_only.py`.
- `ctrl_boundary.py --require-rv32 --selftest --without verilator` (the firmware-boundary job's steps): PASS, 2,864 of 3,094.
- `ctrl_boundary.py --require-rv32 --selftest --only verilator`: PASS, 775 of 885.
- `cd tests && behave`: 406 scenarios.
- Four-shard Verilator sweep: 64 of 64 suites, 2,191,124 checks, 0 failures (equal to `bdad673a`).
- Firmware self-test, coverage, nvm, builder, ctrl-memory, generator check, linked images and the arm A/B legs read no changed file. Their `bdad673a` receipts stand.
Acceptance criteria: ruling items 1 and 2 met. The PR body says "Relates to #665"; this PR does not close #665.
Open risks/questions: none
