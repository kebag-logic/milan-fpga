[A583] REVIEW READY

Round 9 for PR #705 ([assignment](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6107732413)), answering R584-7 and R585-7. Three new commits on `4cab445a`, no rebase or amend; not pushed.

Commit: `feed95bbb6429e5af0ee3f0a24c531777279e9de`

Changed:
- `2d24214d0` (item 1, R584-7-F1 / R585-7-F1). The stack pin proof (`ctrl_build.py`, `ctrl_pin.py`) runs Git through one helper only, `ctrl_build.git`.
  - Its environment (`git_env`) sets `GIT_NO_REPLACE_OBJECTS=1` and gives `GIT_GRAFT_FILE` a path under `/dev/null`, which cannot exist. Measured on Git 2.56: `GIT_NO_REPLACE_OBJECTS` alone still honours `info/grafts`.
  - Disk bytes are hashed from the files themselves (`blob <len>\0<bytes>`), through no attribute or filter.
  - `stack_pin` now compares the pinned commit's whole tree (`ls-tree -r -t`) with every entry of the checkout but its `.git`. That means the same paths, the same type and mode at each, and the same blob for every file and link. Each differing path is named. This also settles R584-6-S2.
  - A census (`ctrl_pin.census`) runs on every boundary run. It refuses a string of either module, outside the helper and the docstrings, that names the Git program. It also refuses a helper environment without either setting. Stated limit: a name assembled at run time is not seen.
  - Ten new standing pin controls (30 in all), each refused by name before any build:
    - with `src/adp.c` edited on disk: a replacement of the pinned `src/` tree, a replacement commit for the pin, a graft file, and a clean filter given through `info/attributes` that turns the edit back into the pinned blob (the control first checks that it does);
    - the stack's `LICENSE` edited (the whole tree), a symbolic link standing in for a source (type), and a script made executable (mode);
    - the census, planted with round 8's form of the call (`run(["git", ...])`) and with the helper's environment missing each setting.
  - The clean clone still passes.
- `107aab303` (item 2, R584-7-F2 / R585-7-F2). The README now gives 96 defects and 8 passing controls in the firmware run, 5 in the Verilator run, and 30 pin controls.
  - The repository had no figure check: the `structure_check.py` R585-7 used is the reviewer's own script. So the boundary self-test now checks the figures.
  - It counts `ctrl_plants.PLANTS` and its own pin controls, and refuses the page where one of the four figures differs or is not given exactly once.
  - Four figure controls each plant the page with one figure one higher and require a refusal naming it. Against the README at `4cab445a`, the check names the 95.
- `feed95bbb`. The whole-tree control edits the stack's `LICENSE`, not `README.md`. At `107aab30` the docs job's `ci_scope.py --selftest` read that bare literal as the top-level page and failed. It now passes.

Validation. CI-parity means Ubuntu 24.04, CPython 3.12.3, gcc 13.3, GNU make 4.3 under `MAKEFLAGS=w`, GoogleTest 1.14.0, clang 18 and cmake 3.28, on four CPUs, in fresh clones.
- `firmware-boundary`'s step at `feed95bb`: PASS in 677 s (38 % of 30 min). 2822 compiled sources of 3053 invocations, 0 findings; 105 boundary, 30 pin and 4 figure controls, 0 misbehaved.
- `firmware-verilator`'s step at `feed95bb`: PASS in 492 s (21 % of 40 min). 816 of 916, 0 findings; 6 boundary, 30 pin and 4 figure controls, 0 misbehaved.
- `firmware-unit`'s steps at `107aab30` (no module they load changed after it): every step rc 0, 2051 s.
  - The firmware gate's 845 verdict lines are byte-identical to rounds 4 to 8 (`mutants: 471 of 471 caught`).
  - The store passed 435 tests; the coverage self-test caught 29 of 29; `fw_coverage.py --check` PASS (30 files), the table identical.
- The docs job's 54 commands at `feed95bb`: all rc 0. That includes `ci_events.py --check` (1902) and `--selftest` (2610 arms), `ci_scope.py --selftest`, `check_py_idiom.py` (every ratchet held), `check_em_dash.py --base 4cab445a` and `docs_check.py`.
- Images: 35 of 35 ELF hashes are identical to round 8 and dev `aef7ac66` (manifest sha256 `de8ae063…`).
- The reviewers' probes, at `4cab445a` and then at the head:
  - R584-7's `pin_replace_probe.sh`, step 3: `ACCEPTED`, then `REFUSED: tsn-c-stack differs from the pinned 1a9f651c: ...`.
  - R585-7's `pin_probe.py`: `replacement control: ESCAPED`, then `replacement control: REFUSED ... include/adp.h`; the restored clone is accepted.
- Every entry point: a full clone at the head with `ADP_ADVERTISE_MS 9000u` in `include/adp.h`, disguised five ways: a replacement tree, a replacement commit, a graft file, a clean filter, and a mode change.
  - The 17 entry points are the pin check's command line, the host test (build-only and self-test), coverage, both image fixtures, the boundary gate, the MAAP differential in both modes, the AECP arms, campaign and wire comparison, and `make` for `stack-pin`, the firmware library, `run-cosim`, `run-if2` and the default target.
  - Each exits 2 naming the changed file: 85 of 85.
- Mutants of the proof, each making its own control escape:
  - the helper without `GIT_NO_REPLACE_OBJECTS`: both replacement controls;
  - the disk hashed through Git's filters: the clean-filter control;
  - modes not compared: the mode control;
  - symbolic links followed: the type control;
  - round 8's seven parts: the `LICENSE` control.
  - The helper without `GIT_GRAFT_FILE` escapes no proof control, because a graft changes only parents, which the proof never reads. The census names it, and its third control plants it.
- The census named six planted forms of a Git command (a command list, a shell line, `shutil.which`, an absolute path, a `python -c` program, an f-string). As stated, it does not see `"g" + "it"`.

Acceptance criteria: unchanged and met. The pin, the RV32 images (byte-identical at every shape), the boundary in both directions with its planted controls, coverage (same denominator) and every campaign's kills are as before. The pin assurance now holds under replacement objects, grafts and filters, and the README states the gate's own counts.

Open risks/questions:
- The census reads text. A name assembled at run time, or a Git call made for the proof by another module, would not be seen; the proof calls no such module.
- The graft control alone cannot fail by dropping `GIT_GRAFT_FILE`; the census holds that setting. Refusing a repository that holds a graft file or replace refs outright would be a further rule, not taken.
- The whole-tree check refuses anything left inside the submodule, such as a build directory made there.
- The README sentence of the assignment is read as R585-7's own script, since the repository has no structure check. The figure check reads four sentences of the firmware README.
- S1 is not applied: this round changes what `firmware-boundary` runs, so `4cab445a`'s hosted figures are not this head's. RES1 is the manager's at merge; `PR-BODY.md` carries the reviewers' exact wording for both stale lines.
- `firmware-unit` stays at 76 % locally; its headroom is #716's.

Evidence: `HANDOFF.md`, Round 9 (commits, file:line table, mutant and probe tables, gates), with logs under `round9/logs/` in the author packet.
