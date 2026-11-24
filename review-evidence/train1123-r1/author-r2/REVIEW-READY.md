[A828] REVIEW READY
Commit: 43076d0f8c87b5118f6f4317d000a7eebdefc967 (branch `pf-train-1123`, committed locally; pushed by the manager)
Base: `dev-soft-core` `aa30d77f`. The delta from round 1's head `f5a1585e` follows. Round 1's composition, figures and gates are unchanged and stand as posted in its handoff.

**Changed (f5a1585e..43076d0f, four commits)**
- `93c5ad84`: merge of PR #959's reviewed head `8aeb2f0b` (#948, README only). The tree is identical to `f5a1585e`'s (`db8dd481`), since the composed README already gives 192 pin controls.
- `4df6751e`: merge of live `dev-soft-core` `aa30d77f` (PR #961's merge). Both its parents (`854bd723`, `287ca1ee`) are ancestors of `f5a1585e`, and the tree is again identical (`db8dd481`).
- `ce8454cb` `tb/verilator/ctrl_service_budget/kept_grade.py`: #969's conditions as [the amendment of 2026-11-23](https://github.com/kebag-logic/milan-fpga/issues/969#issuecomment-7116192252) states them.
  - **kept <= bound** is held within the measurement rule, kept <= bound x 1.05 on the same image (#665 ruling item 4). The KEPT <= BOUND line prints both figures, the difference and the margin to the allowance.
  - **The bound path's build of one MRPDU** over `CTRL_LOOP_BUILD_ONE_PASS_US` is now OWED #977 by name, the constant named and not restated. That covers `kept_grade`'s own line and `run.py`'s two STATED lines for that pass: `a build-one pass of` and `a tier-2 slice of THE TRANSMIT's build of`.
  - **The bound path's work passes over THE SHARE** stay OWED #977, as before.
  - **The kept path's** builds and its SHARE passes stay findings. So do the idle runs over THE SHARE, and a pass of either group given whole to THE TRANSMIT's build.
  - **The self-test** has 24 checks, 19 before. Kept 4 % over bound PASSES, kept 6 % over FAILS, and bound + 5 % holds while one cycle more fails. A kept pass over THE SHARE FAILS, and a kept build of one over its slice FAILS. The bound path's build of one and its SHARE pass are OWED with no finding, and through `Disposition` the bound pass and slice lines are owed while the kept ones stay failures.
  - No owner bound, `CTRL_LOOP_BUILD_ONE_PASS_US` or `CTRL_LOOP_SRP_UNIT_US` is restated.
- `43076d0f`: the harness README, `kept_window.py`'s docstring and the design page's train section record the amended conditions and the re-grade.

**Validation (at 43076d0f unless stated)**
- `kept_grade.py --selftest`: PASS, 24 checks.
  - Ten defects planted in the new code by scratch monkeypatches, none committed, are each caught by a named check:
    - no margin, a 7 % margin, a 3 % margin;
    - the bound build of one a finding again, every bound build owed, the kept build of one owed;
    - run.py's bound build-one line not owed, its bound build-slice line not owed;
    - run.py's kept build-one line owed, its kept build-slice line owed.
- **The re-grade of round 1's formal legs, with no simulation run again.** `plat_ledger` at 43076d0f: PASS, 0 findings, and all **24 image hashes identical to f5a1585e's** (elf, debug-stripped and loadable at each of the 8 images).

  | Point / arm | kept Failed vs bound (CPU cycles) | margin to bound + 5 % | srp-bound build of one | kept_grade |
  |---|---|---:|---|---|
  | 1x1/1if arm A | 36,631 vs 38,739 (-5.44 %) | +4,044 | 53,182 of 73,500 | PASS, 0 findings, 4 owed |
  | 1x1/1if answering-ports | 35,435 vs 38,746 (-8.55 %) | +5,248 | 53,605 of 73,500 | PASS, 0 findings, 4 owed |
  | 8x8/1if arm A | **142,582 vs 142,137 (+0.31 %)** | **+6,661** (to 149,243) | 103,782 of 147,500 | PASS, 0 findings, 5 owed |
  | 8x8/1if answering-ports | 134,143 vs 138,016 (-2.81 %) | +10,773 | **171,645 of 147,500: OWED #977** | PASS, 0 findings, 6 owed |

  - The kept path: 0 work passes over THE SHARE at both points. Its heaviest build of one is 86,018 at 8x8/1if (`answering-ports`) and 37,898 at 1x1/1if.
  - The bound path's SHARE passes (OWED): 216,785 at 8x8/1if arm A and 203,961 in `answering-ports`.
  - `run.py --regrade --groups srp-kept,srp-bound --record-budget-findings --record-share-findings` on each leg's pair: rc 0 at all four legs, with 0 refusals and 0 budget misses. At 8x8/1if `answering-ports` it prints the 171,645 build of one OWED as a pass and as THE TRANSMIT's slice.
  - It ran from the measurement clone at `c2b2ba1a` (the build's own firmware tree, which the reuse check requires) with `tb/verilator/ctrl_service_budget/` taken from `ce8454cb`, and the clone was restored clean after.
  - Every other group's grade is unchanged: `Disposition` only touches the `srp-kept`/`srp-bound` lines.
- **Harness tree checks**: PASS. These are `load_grade --check` (0.512 / 0.744), `flip_grade --check` at 1x1/1if and 8x8/1if, `shape_costs --check`, the five `--selftest`s, `run.py --self-test` (0 failures) and `test_ctrl_memory.py` (0 failures). Porcelain was 0 before and after.
- `ctrl_boundary.py --require-rv32 --selftest`: PASS. 0 findings, 117 boundary, 192 pin and 4 figure controls, 0 misbehaved.
- **The firmware gate's four shards: not re-run.** No firmware or test input changed since `f5a1585e`: `git diff --stat f5a1585e 43076d0f -- sw/ third_party/ configs/ hdl/` is empty, and nothing under `sw/` reads `kept_grade` or `kept_window`. They passed all four at `f5a1585e`, with 2,003 live invocations and 0 escaped.
- **Docs workflow steps** (five jobs, fresh clone, em-dash base `aa30d77f`): 56 steps rc 0 and 24 SKIP (installs and hosted recorders).
  - docs_check: 0 findings over 223 pages.
  - em-dash: 0 over 762 added lines.
  - The SV, C/C++, Python and Shell idiom gates all PASS.
  - The 3 RV32 SDK install-verify steps refuse with "missing regular SDK provenance receipt". That is the environment, the same as on the bases and in round 1.
  - The tree is clean after.
- No RTL changed, so no route was run. Round 1's routes stand: both meet #818's floor on images identical to this head's.

**Acceptance criteria**: met. #969's conditions as amended hold at both points and in both arms, every owner bound holds (#969 amendment item 3), and every statement change is listed in the PR body with its figures.

**Open risks/questions**
1. **`run.py`'s `a tier-2 slice of THE TRANSMIT's build of` line for `srp-bound` is owed together with its build of one.** At 8x8/1if `answering-ports` it is the same 171,645-cycle pass graded against the same 147,500 slice. A bound pass given whole to THE TRANSMIT's build (two MRPDUs) over `CTRL_LOOP_BUILD_PASS_US` stays a finding, since the amendment names the build of one only. The reviewer should confirm this reading of item 2.
2. **The registration cost stays owed to #977.** #977 must clear THE SHARE and the build slice on the composed head before the post-flip in-house qualification closes (amendment item 2).
3. **The output map's largest edit at 1x1/1if** is pre-existing and has never been measured by the harness. A probe measured 176,099 cycles, 1,850 us, against the 975 us stated, with 2 of 105 passes over THE SHARE. The draft Issue is ready for the manager to file.
