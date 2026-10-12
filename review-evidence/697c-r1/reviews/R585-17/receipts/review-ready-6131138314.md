[A583] REVIEW READY

Commit: 27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c (round 18, branch `697-consume`: a merge of dev `dc4d06cb` on `5b4ea551` as `ddbd7fd7`, then one commit; not pushed, per the assignment)

Changed:
- Item 1, the merge (`ddbd7fd7`).
  - `git fetch origin dev` gave `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. `git merge --no-ff` stopped in exactly the four conflicts the assignment names. Each is resolved with both sides standing:
  - `.github/workflows/rtl-fast.yml`: dev's four firmware jobs keep their steps and shard split. Each fetches `third_party/tsn-c-stack` too, because each builds the firmware whose ADP, ACMP and MAAP cores it holds. `firmware-boundary` and `firmware-verilator` follow unchanged. The aggregate's `needs`, environment and loop are dev's list plus the lane's two. Parsed, every other job equals both parents'.
  - `scripts/ci_events.py`: both constant blocks, and the union of the aggregate's environment names. `RV32_REQUIRED_STEPS` keeps the lane's entries and gains each mutation job with its phase step, so every missing-compiler control dev planted is still planted. The census and budget checks are dev's.
  - `sw/firmware/ctrl/test/test_ctrl_firmware.py`: dev's phase dispatch, plus the lane's `--build-only` and `BUILT` verdict (`--build-only` and `--shard` never combine). The stack pin check stays in `main` before the first build, so all four jobs run it.
  - `docs/testing/CI_WORKFLOWS.md`: the docs-only skip names all six jobs. Three lines the split made false are fixed: "each of the four jobs" initializes tsn-c-stack, "none" runs a capture, and the lane's single-job budget lines give way to #716's table. One line says the aggregate also requires the two boundary jobs.
  - Each job keeps its own steps once; no check is dropped or doubled (`ci_events.py --firmware-census`: preserved).
- One semantic conflict, outside the four files (`27ee16b5`). The lane's boundary gate refuses a program that names the firmware's tree unless its registry classifies it. Dev's new `test_ctrl_firmware_shards.py` is such a program.
  - At the merge, `firmware-boundary`'s step built every builder and then exited 2 naming it.
  - `ctrl_configs.OUTSIDE` now lists it as a program that compiles nothing (`ctrl_configs.py:162-163`), as round 13 did for dev's publication census. That is measured: under the gate's own capture it ran with no compile recorded.
  - `ctrl_configs.py` is loaded only by the boundary gate's modules. No firmware behaviour, image input or pin changes, so this was not taken as a STOP. The manager may rule otherwise.
- Item 2: nothing else changed. `git diff --stat 5b4ea551 27ee16b5`: dev's five files and `ctrl_configs.py`. The tree differs from dev `dc4d06cb` in exactly the lane's 72 files.
- Residue (PR body only): R584-15-RES-1 is applied with its exact text. R585-16-RES-1 is carried, not applied, since this round allows no other change; its exact fix is recorded in the PR body.

Validation (fresh clones sharing no file with the lane; the runner's Ubuntu 24.04 replica: CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, cmake 3.28, clang 18, Ubuntu's Git 2.43.0, `MAKEFLAGS=w`, four CPUs each, the pinned RV32 SDK and Verilator 5.050):
- `ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS in 691 s. 2822 compiled sources of 3053 invocations, 0 findings, 105 boundary, 106 pin and 4 figure controls, 0 misbehaved. At the merge `ddbd7fd7`: rc 2, the refusal above.
- `ctrl_boundary.py --require-rv32 --selftest --only verilator`: PASS in 488 s. 829 of 930; 6, 106 and 4 controls, 0 misbehaved.
- The four firmware jobs' commands, each beside dev's own on the same CPU count:
  - `firmware-unit`: 589 s (dev 590 s). Phase 0's 60 arms `[ok]`; store 435 tests; coverage 100 % in 30 files, every row unchanged; coverage self-test 29 of 29.
  - control: 763 s, `mutants: 506 of 506 caught`. At the merge: 888 s, dev beside it 860 s.
  - AECP: 183 s (dev 182 s).
  - SRP: 571 s (dev 569 s).
  - Each prints the shard proof's five `PASS` lines and `tsn-c-stack at 405dc683…` before any build, and ends `test_ctrl_firmware: PASS`.
  - Together their 915 verdict lines, every one `[ok]`, equal round 17's single run line for line (sha256 `861dcd9f…`).
  - `ci_rv32_sdk_selftest.py` errors in the replica only, which has no `xz`; on the host it runs 25 tests OK.
- Each job's budget, 60 % of its timeout:
  - #716's hosted maxima: `firmware-unit` 703 s (26.0 % of 45 min), control 841 s (31.1 %), AECP 260 s (9.6 %), SRP 625 s (23.1 %).
  - This lane's hosted maxima over its four runs with both boundary jobs: `firmware-boundary` 834 s (46.3 % of 30 min), `firmware-verilator` 737 s (30.7 % of 40 min).
  - The paired replica ratios (0.998 to 1.033) scale #716's maxima to at most 32.2 %, and #716's own calibration formula gives at most 36.7 %.
- Images: 35 of 35 ELF hashes identical to dev `dc4d06cb`'s, built from dev itself (manifest sha256 `8b1292db…`). `ctrl_image.py --base dc4d06cb` gives `+0` in every section at both shapes.
- CI contract: `ci_events.py --check` 2169 items; `--selftest` 3064 arms. `test_ctrl_firmware_shards.py`: 916 invocations, each in exactly one shard (60, 507, 77, 272).
- The resolution's planted controls:
  - 15 of 15 refused by `ci_events.py --check`: each firmware job's fetch without tsn-c-stack, a job dropped from the aggregate's `needs` or loop, `--shard 0/4` removed, a job removed, `--require-rv32` dropped, a budget row dropped.
  - With the stack edited, each `--shard i/4` form refuses naming the file before any build. With the pin line taken out of `main`, all four escape.
- `act_ci.py --selftest` in a disposable container: `selftest: PASS`, 446 arms.
- Every entry point that pins the stack, the four shard forms new: 21 under 12 states, 252 of 252 refused by name before any build.
- Every pin control with the census and the figure check: 106, 0 misbehaved, on Git 2.56.0 and upstream 2.43.0 (CPython 3.14.7 and 3.12.3).
- The hook-rule campaign: H0 clean; H1 to H24 caught on CPython 3.12.3 and 3.14.
- The round-17 configuration mutants and the earlier reviewers' probes print what they printed at `5b4ea551`, on both Gits.
- The docs job's 54 commands: 53 of 54. The one failure is `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w`, 48 of 50, the same at dev `dc4d06cb` (50 of 50 without it). `check_em_dash.py --base dc4d06cb` finds 0 over 433 added lines.

Acceptance criteria:
- #697 acceptance 1 to 5 are unchanged and met: the pin is `405dc683`, the cores come from the submodule, and the images are identical to dev's.
- Round-18 items 1 to 3 are met as above, with the one registry entry beyond the four conflicts (open item 1).
- Every pin control holds.

Open risks/questions:
1. `27ee16b5` is a change beyond the four conflicts. The merge needs it for `firmware-boundary` to pass, and it touches no firmware, image input or pin.
2. R585-16-RES-1 waits for a round that allows a text change. R584-15-S1 and R585-16-S1 are optional and not taken.
3. #716's hosted acceptance at the new head is the manager's; the head is not pushed.
4. Carried: the `MAKEFLAGS=w` source-list self-test (as at dev); the unused `import os` in `test_ctrl_firmware.py` (at both parents); residue to #495.

Not run: hosted CI and act against a PR head (not pushed). The round-18 evidence (HANDOFF Round 18, gate logs, scripts) is with the manager for publication.

