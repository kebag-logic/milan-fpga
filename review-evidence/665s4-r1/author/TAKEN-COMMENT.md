[A698b] TAKEN

Branch: `665-s4-f1-target` (local worktree branch `s4-f1-target`). This round adds commits on round 1's head `9c2f12a8`, from `dev-soft-core` `f4c9ad4f`. The PR will target `dev-soft-core`.

Authoritative references:
- [A10] issuecomment-6504551000: the owner's decision of 2026-10-29 19:05, option (c).
- issuecomment-6495692075: `T_svc` approved at 20 ms, graded per family.
- `docs/reference/FR_NFR.md` 3.4.1.
- `sw/firmware/ctrl_nvm/README.md` ("Write-back").
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 5.
- D5 on the current flash writer: `tb/verilator/nvm_capture_cpu/README.md` and `scripts/check_nvm_capture.py`.

Interpreted scope:
- **The docs.** Restate S4's first acceptance item and F1's capture contract in the owner's wording, with the owner and the date. The places are `ctrl_nvm/README.md`, the split design docs that state the contract, and the plan's S4 section. Each says the 24.5 ms bound covers the current flash writer's capture only, as `check_nvm_capture.py` holds it. No `docs/history` edits.
- **The harness, `tb/verilator/nvm_split_target`.**
  - F1's 24.5 ms capture bound and its one-page-past control are removed.
  - Every F1 step, in every phase, is graded against `T_svc`, and a step over it fails the commit case.
  - The capture's CPU time and its elapsed time are recorded at both points. The elapsed time runs from the first capture step's start to the last one's end.
- **The planted defects.**
  - A step lengthened to one CPU cycle over `T_svc` is caught in each phase.
  - The 24.5 ms check is removed from the current writer's grader (`nvm_capture_cpu/run.py` `grade_rows`). A new self-test check catches it, and so does `check_nvm_capture.py`.
- **`T_svc`.** The cases read `scenario.T_SVC_MS`, as they do now. At this base that is still the 10 ms proposal. S2b's lane carries the approved 20 ms and the per-family `min(T_svc, ceiling)`. 10 ms is under every family's bound, so a step within it is within each. This lane edits neither FR_NFR nor `scenario.py`.
- **Untouched.** `nvm_capture_cpu`'s `.py` and `.cpp` files and `measurements.json` are not edited, because `check_nvm_capture.py` hashes them.

Validation plan, at the final head, all rc 0:
- round 1's gate set: the docs workflow's commands, the idiom and evidence gates, `firmware-boundary` in both modes, and behave;
- `test_ctrl_nvm.py` and `test_ctrl_firmware.py`, each with `--require-rv32 --self-test`;
- `fw_coverage.py --check`, `nvm_cosim`, the census, and `test_builder.py --require-rv32`;
- the generator, target and harness self-tests;
- `nvm_split_target` and the S2 harness at 1x1 and 8x8;
- `nvm_capture_cpu` at 8x8;
- `check_nvm_capture.py`, with the removal planted.

RTL does not change, so the full sweep is not run.

Blockers: none.
