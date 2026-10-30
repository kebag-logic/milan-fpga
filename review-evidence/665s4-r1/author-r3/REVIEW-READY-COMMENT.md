[A698c] REVIEW READY

Commit: `ac45db8f18a5fde87c84be2225cc1be7d709eae9` on `665-s4-f1-target` (local branch `s4-f1-target`). It is round 2's head `ee1c0be0` plus three commits, with no rebase, from `dev-soft-core` `f4c9ad4f`. Nothing is pushed. The PR body for #812 is ready: base `dev-soft-core`, "Relates to #665".

Changed, for R738-F1 (MINOR; [A10] issuecomment-6511289316):
- **`tb/verilator/nvm_split_target/run.py`.**
  - `results.json` is now a record: `point`, `shape`, `cpu_hz`, `sys_hz`, `t_svc_ms` and `results`. Before, it was a bare list.
  - The clocks are the ones every arm's `build.json` records (`run.clocks`). Builds that disagree, or that lack a clock, are refused.
  - `table.md` names both clocks, in MHz and in hertz, on the line above each of its three tables. The line is rendered from the record; no "50 MHz" string is fixed.
  - The run is refused, with exit 2 and no `table.md`, in three cases: the record lacks a clock; a ms figure, a T_svc verdict or the step control's T_svc is not its CPU cycles at the record's CPU clock; or the record's clocks are not its builds' (`run.provenance`, `run.against_build`).
- **`target_selftest.py`.**
  - 12 new checks on a synthetic run at CPU 62.5 MHz and bus 125 MHz, some of them through `run.py`'s own `main`. They show that the report and the JSON follow the input's clocks and its figures. They show too that a missing, non-integer, misconverted or wrong-for-the-build clock is refused.
  - 8 new mutants, all caught, among them a fixed 50 MHz report line and an unconditional 50/100 MHz run clock.
  - `checks: 61   failures: 0` (41 checks, 20 mutants).
- **Docs.** The split-CPU figures name their clocks, CPU 50 MHz and bus 100 MHz, in `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 5, in `ctrl_nvm/README.md` and in the target harness's Results. The harness README describes what the results carry and the new checks. The PR body's F1 timing table names its clocks.
- **Unchanged.** RTL, firmware, the step bound, the capture's recording, the D5 controls, the S2 harness and the current flash writer's harness.

Validation at `ac45db8f`, all rc 0:
- **`nvm_split_target`**, fresh builds at both points. Every arm's `build.json` records 50,000,000 Hz CPU and 100,000,000 Hz bus.
  - RC=0 at each point: every case passes, and every control is caught (`slow-step` 30.2216 ms at 1x1 and 30.2139 ms at 8x8; `step-over-t-svc` in all seven phases).
  - `results.json` carries `"cpu_hz": 50000000, "sys_hz": 100000000`, and its results are identical to round 2's at both points.
  - `table.md` reads `Clocks, as this run's builds recorded them: CPU 50 MHz (50,000,000 Hz), bus 100 MHz (100,000,000 Hz).` above each table.
  - The runs were built at `4e8348ec`, the harness commit. The two later commits are Markdown only. At the head, `--regrade` of both reproduces `table.md` and `results.json` byte for byte.
- **The capture**, recorded with no bound, at CPU 50 MHz and bus 100 MHz:
  - 1x1: 27.223 ms of CPU time, 534.905 ms elapsed;
  - 8x8: 103.227 ms of CPU time, 1,638.061 ms elapsed;
  - the longest step is 2.639 ms.
- **The probes**, through the checkout's `run.py`:
  - the 62.5/125 MHz synthetic run renders those clocks;
  - round 2's published 8x8 `results.json` (no clocks) is refused with `no cpu_hz recorded; no sys_hz recorded`;
  - this round's 8x8 record relabelled to a 100 MHz CPU is refused with `commit: longest step 2.63858 ms is not 131,929 CPU cycles at 100,000,000 Hz; ...`.
- **D5 on the current flash writer.** With its 24.5 ms check removed in a scratch clone, `check_nvm_capture.py` exits 1 with `FAIL: OFF timing limit was ignored`; unplanted, it exits 0.
- **The S2 harness**, fresh builds: 1x1 18 groups and 8x8 17 groups, 0 refusals, RC=0. Both tables are byte-identical to round 2's.
- **Gates:** 108 gates at the head: `0 of 97` and `0 of 11` nonzero, the tree clean after each. They include:
  - the docs workflow's commands;
  - behave (406 scenarios);
  - the idiom, evidence and hygiene gates;
  - `firmware-boundary` in both modes;
  - the builder bank (`test_builder.py --require-rv32`; one registered NOT RUN, as in rounds 1 and 2);
  - the store gate (435 tests, 109 of 109 defects);
  - the firmware campaigns (`test_ctrl_firmware.py --require-rv32 --self-test`: 1,006 plants, none escaped);
  - `fw_coverage.py --check` at 100 %;
  - `nvm_cosim` (465 checks, 39 of 39 mutants);
  - the census;
  - `check_nvm_capture.py`.

  RTL is unchanged, so there is no sweep.

Acceptance criteria:
- R738-F1's required outcome is met:
  - the measured clocks are kept in `results.json`;
  - the actual clocks are rendered beside every generated table, from the builds' records;
  - the architecture and PR figures are labelled;
  - missing or wrong provenance is checked and refused;
  - a synthetic, differently clocked input proves that the rendering follows the input;
  - both points were regenerated at CPU 50 MHz and bus 100 MHz;
  - the step-bound and D5 controls pass unchanged.
- S4's acceptance from rounds 1 and 2 is unchanged and still met.

Open risks/questions:
- `results.json` changed shape, from a list to a record. Nothing in the tree reads it; its only reader is a reviewer, and round 2's published lists stay readable as `results`.
- The CPU budget harness's own `table.md` (S2, shared with S2b) does not name its clocks. R738-F1 was filed against this harness's outputs only, so that one is left to its owners.
- T_svc is still the 10 ms proposal at this base, as in round 2.
