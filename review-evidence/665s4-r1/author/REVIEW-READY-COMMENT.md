[A698b] REVIEW READY

Commit: `ee1c0be0b99f0131eb10908a19f080299aa0cbb8` on `665-s4-f1-target` (local branch `s4-f1-target`). It is round 1's head `9c2f12a8` plus two commits, from `dev-soft-core` `f4c9ad4f`. Nothing is pushed. The PR body is ready: base `dev-soft-core`, "Relates to #665".

Changed, per the owner's option (c) (issuecomment-6504551000):
- **`tb/verilator/nvm_split_target`.**
  - Every F1 service step, in every phase and every case, is graded against T_svc; a step over it fails its case.
  - The capture's CPU time and elapsed time are recorded, with no bound. The 24.5 ms capture bound, its one-page-past control and `--record-budget-findings` are removed. No report presents 24.5 ms as F1's bound, and the self-test checks the report for it.
  - New plant `slow-step`: a real first step spun to 30 ms. New control `step-over-t-svc`: each phase's longest step of the measured commit at exactly T_svc, then one cycle past it.
  - New self-test check: the current flash writer's own grader (`nvm_capture_cpu/run.py` `grade_rows`) still passes exactly 24.5 ms and refuses one tick more. A mutant deletes that check.
  - The self-test has 41 checks and 12 mutants.
- **Docs.** F1's capture contract is restated in the owner's wording, with the owner and the date, and says that 24.5 ms covers the current flash writer only. The places: `ctrl_nvm/README.md` ("The service bound"), `ARCHITECTURE_HW_SW_SPLIT.md` sections 2, 5 and 6, both capture harnesses' READMEs, and the plan's S4 section. No `docs/history` edits.
- **Unchanged.** RTL; firmware; `nvm_capture_cpu`'s `.py` and `.cpp` files and `measurements.json`; `check_nvm_capture.py`; the S2 harness.

Validation at `ee1c0be0`, all rc 0:
- **`nvm_split_target`**, rc 0 at both points:
  - every case passes, and every step is within T_svc;
  - every control is caught: both reorders, `guard-removed`, `slow-step` (`step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms` at 1x1, 30.2139 ms at 8x8) and `step-over-t-svc` in all seven phases.
- **The capture, recorded:**
  - 1x1: 27.223 ms of CPU time, 534.905 ms elapsed;
  - 8x8: 103.227 ms of CPU time, 1,638.061 ms elapsed;
  - the longest step is 2.639 ms.
- **D5 on the current flash writer.**
  - `nvm_capture_cpu` at 8x8 and 50 MHz: at most 13.863 ms with traffic and 13.690 ms without. The `skip-copy` and `no-traffic` controls are caught.
  - The removal of its 24.5 ms check, planted in a scratch clone, makes `check_nvm_capture.py` exit 1 with `FAIL: OFF timing limit was ignored`; the unplanted clone passes.
- **The S2 harness:** 1x1 18 groups and 8x8 17 groups, 0 refusals. Both tables are byte-identical to round 1's.
- **Gates:** 108 gates, `0 of 97` and `0 of 11` nonzero, the tree clean after each. They include: the docs workflow's commands; behave (406 scenarios); the idiom and evidence gates; `firmware-boundary` in both modes; the builder bank (one registered NOT RUN, as in round 1); the store gate (435 tests, 109 of 109 defects); the firmware campaigns (1,006 plants, none escaped); coverage at 100 %; `nvm_cosim` (465 checks, 39 of 39 mutants); the census; and `check_nvm_capture.py`. RTL unchanged, so no sweep.

Acceptance criteria:
- The first item, as the owner restated it: met at both points. Each step is within T_svc, and the capture's CPU and elapsed time are recorded.
- The boot with valid, absent, torn and wrong-version slots: met.
- `nvm_cosim` and `nvm_capture_cpu`: met.
- D3's apply order: met.
- The guard: met.

Open risks/questions:
- The cases grade against `scenario.T_SVC_MS`, which is 10 ms at this base. The approved 20 ms, graded per family, comes with S2b's change. 10 ms is under every family's bound.
- This harness's self-test is not yet in a hosted workflow. The hosted guard on the current writer's 24.5 ms check is `check_nvm_capture.py`, which is unchanged.
