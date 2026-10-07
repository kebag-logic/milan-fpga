[A556] REVIEW READY (round 3, merge only)
Commit: `34475e774dfe1c92c81fa51293668e64dc95fa85` on `677-fw-fixes`. It is the PR #684 head `6c94e9f5`, then a `--no-ff` merge of dev `910f338d` (`232970dbb9663abb2a260efda4d2d5abcf034fb5`), then one resolution commit. No rebase, no amend. Not pushed: this lane may not push, so publishing the branch is the next step.

Changed:
- **Merge.** The one textual conflict was the `rv32` paragraph of the `test_ctrl_firmware.py` docstring. It keeps #679's text and adds the assertion interface. Everything else merged automatically.
  - `git diff 910f338d 232970db` equals the round-1 diff hunk for hunk, apart from that docstring.
  - Both gates still run the debug and release re-entry arms next to #679's `rv32` checks.
  - `ctrl_mutants.py`, `nvm_mutants.py`, `tally_selftest.py` and `fw_coverage_selftest.py` are byte-identical to round 1.
  - #679's 17 RV32 self-test checks are all kept. No firmware C source changed.
- **Semantic conflict (`34475e77`).** #679 builds RV32 objects with `-nostdinc` against its `rv32_include` declarations. `adp.c` includes `<assert.h>` for the #678 debug guard, so at the merge commit the ctrl `rv32` arm fails (`assert.h: No such file`; witness `merge-commit-rv32`). #679 also dropped the `__`-prefix allowance that had admitted `__assert_fail`. The fix follows #679's own pattern:
  - new `sw/firmware/gtest/rv32_include/assert.h`: the C11 `assert` macro under `NDEBUG`, `static_assert`, and a declaration of `__assert_fail`;
  - `ctrl_build.py:46`: `RV32_LIBC` names exactly `__assert_fail`;
  - `fw_rv32_selftest.py:30`: the hostile sysroot also poisons `assert.h`, and the probe uses it;
  - wording in `fw_rv32.py` and the gtest README.
- **Re-graded checks.**
  1. The ctrl runtime-dependency check gains `__assert_fail`. #678 requires debug builds to assert, and the arm builds without `NDEBUG`. It is the same symbol round 1 listed, now admitted by name instead of by prefix. The shared helper set, the store's allowed set, and the ABI, frame and stack-protector checks are unchanged. `malloc` and `__unexpected_service` are still rejected.
  2. #679's header-isolation proof now also covers `assert.h`.
  - `assert-witness` at the head confirms both: the arm fails without the header, and fails on `__assert_fail` without the name. An `NDEBUG` build references no handler.

Validation: every command ran at `34475e77` with rc 0, with every RV32 build on the pinned SDK (receipt verified) via `MILAN_RV32_CC`.
- `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`: 423 host checks and the RV32I build pass (undefined symbols include `__assert_fail`); 79/79 mutants caught (545.4 s).
- `fw_rv32_selftest.py --require-rv32`: 17 checks.
- `tally_selftest.py --mutants`: 18/18 listener defects.
- `test_ctrl_nvm.py --require-rv32 --jobs 4`: 435 tests over 5 shapes; all five RV32 builds pass.
- NVM campaign, in six bounded batches through the repository functions: 109/109 caught, the same names as round 1. `codec_erased_loaded_prefix` catches the three erased-payload defects. The restored `end` bound gives an ASan heap-buffer-overflow READ in `nvm_all_erased`.
- `fw_coverage.py --selftest`: 28/28. `--check --jobs 4`, both with the pinned lwSRP arm and without it: 100% lines and branches on all 14 files. Figures and ratchet are unchanged; 14 exclusion rows, none added.
- lwSRP arm and both pin defects pass.
- Docs and tooling bank: 47/47, with `check_em_dash.py --base` and `git diff --check` against `910f338d`.

Acceptance criteria: still met as at round 1 (#677 bound and ASan test; #678 rule, guard, standing probes and planted defect; ratchet with no new exclusion). The round-3 assignment is met: both sides kept, re-grades stated, and every listed gate run at the merged head.

Open risks/questions:
- A debug target build of `sw/firmware/ctrl` needs its bare-metal runtime to supply `__assert_fail(expr, file, line, func)`; a release build needs none. Nothing shipped compiles this firmware. If the target runtime names its handler differently, the declaration and the allowed name change together.
- Not re-run this round: the builder bank and the mailbox co-simulation. They are not on the round-3 list, and the PR changes no builder or RTL file.
- Still owed: `scripts/run_all_suites.sh` and `syn/yosys/run.sh`. Hosted CI and `act_ci.py --pr` need a pushed head.
- Changed since the reviewed `6c94e9f5`: dev's merged files plus the five resolution files above. Which lenses that re-opens is for the reviewers to decide.
