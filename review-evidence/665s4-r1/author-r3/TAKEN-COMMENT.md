[A698c] TAKEN

Branch: `665-s4-f1-target` (local worktree branch `s4-f1-target`). This round adds commits on round 2's head `ee1c0be0`, from `dev-soft-core` `f4c9ad4f`, with no rebase. The PR (#812) targets `dev-soft-core`.

Authoritative references:
- [A10] issuecomment-6511289316: S4 round 3, R738-F1 on PR #812.
- R738-1's report (PR #812, issuecomment-6510793657): R738-F1, MINOR, under Conformance, Tests and Docs.
- issuecomment-6508235352: the product split CPU runs at 50 MHz and the bus at 100 MHz, and every timing figure names its CPU clock.
- The owner's option (c), issuecomment-6504551000. It stays as it is.

Interpreted scope:
- **`tb/verilator/nvm_split_target/run.py`.**
  - `results.json` keeps the build's recorded `cpu_hz` and `sys_hz` next to the case results.
  - `table.md` names both clocks next to every table, using the recorded values. Nothing in it is a fixed "50 MHz" string.
  - The report and the JSON are refused when a clock is missing, or when it is not the build's own.
- **`target_selftest.py`.**
  - A check that refuses a missing or wrong clock.
  - A synthetic input at other clocks, to prove that the report follows its input.
  - A mutant for each of these checks.
- **Docs.** The F1 timing figures are labelled with their clocks in `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 5, in the PR body and in the harness README.
- **Unchanged.** The step bound, the capture's recording, the D5 controls, the firmware and the RTL.

Validation plan, at the final head, all rc 0:
- the target self-test;
- `nvm_split_target/run.py` at 1x1 and 8x8, built fresh at CPU 50 MHz and bus 100 MHz;
- the docs workflow's commands, and the idiom, evidence and hygiene gates;
- behave;
- `check_nvm_capture.py`, with its D5-removed plant;
- the firmware self-test, `fw_coverage.py --check`, the firmware mutant campaigns, the S2 harness at both points and `test_builder.py --require-rv32`. These are re-run at the head even though no firmware changes.

RTL does not change, so the full sweep is not run.

Blockers: none.
