[A583] REVIEW READY

Round 8 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6105928035), from the manager's hosted check at `8436dfc0`). Six new commits on `8436dfc0`, no rebase or amend; not pushed.

Commit: `4cab445aa2475903b6cf8b87566d2c8a1e15e391`

Changed:
- `f878188c6`. The control, store and coverage gates take `--build-only`, backed by `fw_gtest.Execution` in the harness.
  - Every binary their suites build is built and linked as before; none is run, no defect is planted and nothing is measured.
  - Each ends `BUILT`, never `PASS` or `OK`.
  - `--build-only` with `--self-test` (or the coverage gate's `--check`) is refused, rc 2.
- `ffa613d62` (item 1). New required job `firmware-boundary` (30 minutes): `ctrl_boundary.py --require-rv32 --selftest --without verilator`, given no capture.
  - The gate reads its builders from its own known set (`ctrl_configs.BUILDERS`) and runs each by its builds under its own capture. The three suite gates run by `--build-only`; `fw_rv32_selftest.py` runs as it was, since it compiles its planted cases and runs no binary.
  - The stack's gate and the image builders run under the capture as before. The four modules that compile only inside a suite (the control, AECP and SRP campaigns, the coverage reader's planted cases) are listed with what they compile there (`ctrl_configs.SUITES`).
  - `firmware-unit` is dev's nine steps with the stack fetched and no capture.
  - The `rtl-fast` aggregate needs the new job. `scripts/ci_events.py` pins its six steps, its result binding and its RV32 refusal, cache and installation arms, and `firmware-unit`'s steps back as dev's.
- `0b4c140a5` (item 1, "a dropped builder still refuses by name"). A probe at `09af0d04` (`test_ctrl_nvm.py` removed from `BUILDERS`) passed, rc 0. The coverage gate runs the control and store gates as programs of its own, so a dropped one still compiled in the capture, and both checks took that as held. Two rules close it:
  - A known builder must hold an invocation from a run of its own. The capture already recorded each compile's command; the reader now keeps it apart.
  - A program found by text (a Makefile, or a Python module with a `__main__` block) must be known or listed. Compiling inside another builder's run is enough only for a module that is no program. `aecp_arms.py` and `ctrl_build.py` are listed with the builder they run under (`PART_OF`).
  - Two standing controls plant each case. The probe now refuses by name, rc 2: `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py names the firmware's tree and is a program, and is neither a known builder (ctrl_configs.BUILDERS) nor listed ...`.
- `09af0d047`, `0a9c5fa82`, `4cab445aa`. The firmware README, the harness README, the CI page and `ci_scope.py`'s docstring say this, with the local figures.

Validation (exact head or a tree it changes only in the CI page; CI-parity means Ubuntu 24.04, CPython 3.12.3, gcc 13.3, GNU make 4.3 under `MAKEFLAGS=w`, GoogleTest 1.14.0, clang 18, cmake 3.28, four CPUs):
- `firmware-boundary`'s step at `0a9c5fa8`: PASS in 682 s, 0 findings, 105 boundary controls (the two new ones refused by name) and 20 pin controls, 0 misbehaved.
  - The capture: `2822 compiled sources of 3053 recorded invocations (1622 the firmware's, 347 the stack's, 853 test equipment's and builders' own)`.
- `firmware-verilator`'s step at `0a9c5fa8`: PASS in 494 s, 816 compiled sources of 916 invocations as in round 7, 6 boundary and 20 pin controls, 0 misbehaved.
- `firmware-unit`'s steps with no capture, at `09af0d04`; no module they load changed after it. Every step rc 0.
  - The firmware gate's 845 verdict lines are byte-identical to rounds 4 to 7 (`mutants: 471 of 471 caught`).
  - The store passed 435 tests. The coverage self-test caught 29 of 29, and the coverage table is identical (30 files).
- Item 3, the population: the builds' compiles (arms, store, coverage, RV32 self-test) are the same, phase by phase, in a capture of the build commands and in round 7's capture of the suites.
  - Every judged fact of the builds is among the suites': 266 of 266 source facts and 659 of 659 include edges.
  - The suites' capture held 5 facts and 20 edges more. Each is a test file reading a campaign's planted copy outside the checkout, which every rule admits.
- 35 RV32 images byte-identical to rounds 6 and 7 (manifest sha256 `de8ae063…0ebd0`).
- Repository gates at `4cab445a`: the docs job's 54 commands rc 0.
  - `ci_events.py --check` OK (1902 items) and `--selftest` PASS (2610 arms).
  - `act_ci.py --selftest` PASS (446 arms, line for line round 7's). `check_py_idiom.py` held every ratchet.

Budget (item 2, local):

| Job | Timeout | Local | Share |
|---|---|---|---|
| `firmware-boundary` | 30 min | 682 s (the builds 614 s) | 38 % |
| `firmware-verilator` | 40 min | 494 s (hosted at `8436dfc0`: 682 s) | 21 % |
| `firmware-unit` | 45 min | 1986 s (the control gate 1686 s) | 74 %, over 60 % |

`firmware-unit` cannot meet 60 % by dropping the capture: its suites are dev's own. Hosted with no capture, it took 1963 s at this lane's base `8b61b709` and 1484 to 2462 s on other branches' twenty most recent runs (55 to 91 %).

Acceptance criteria: #697 acceptance 1 to 5 hold unchanged: pin `1a9f651c`, lwSRP `9197193e`, images byte-identical, coverage and kills identical, README. Round 8 items 1 and 3 are met as above; item 2 is met for `firmware-boundary` and `firmware-verilator`, not for `firmware-unit`.

Open risks/questions:
- `firmware-unit` over 60 % of its 45 minutes on its suites alone. Meeting it needs a longer timeout (the slowest of those runs would need 69 minutes) or the campaigns sharded across jobs. The CI page records timeout changes as rulings (#673), and sharding changes what the job runs, so this round takes neither: a decision is needed.
- The boundary now judges the builds, not the suites, so the campaigns' compiles of planted copies leave its capture. As measured, they add no fact a rule can refuse.
- The program rule is read from the text (`__main__`, or a Makefile). A builder program without a `__main__` block would be held as a module, by having compiled in the capture; none exists.
- `firmware-boundary`'s 30-minute timeout is mine, for a new job. Its hosted figures need the push.
- Round 7's eight readings stand unchanged. R584-6-S2, R584-3-S1's remainder and R585-2-S2 are optional and not addressed.
