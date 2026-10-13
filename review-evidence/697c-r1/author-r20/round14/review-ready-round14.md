[A583] REVIEW READY

Commit: a8fe548a083239efc799a79c540b2be63e9d13e7 (round 14: four commits on `8aaa2da7`, branch `697-consume`; not pushed, per the assignment)

Changed (six files under `sw/firmware/ctrl`, +280 −42; no firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin change):
- Item 1, R584-11-F1 = R585-12-F1 (`d89898db`): every object the pin proof reads is checked against its id, failing closed. `ctrl_build.stored` reads one object raw (`git cat-file <type> <id>`), hashes `<type> <length>\0<bytes>` with the repository's object format and refuses one that does not hash to its id, by its place in the pin. `pinned_tree` walks the pinned commit and every tree under it that way, parsing each itself, in place of `ls-tree -r -t`; for the pin it gives the same 89 entries. No blob is read: each file is hashed from its own bytes, as before. Three standing controls (new `ctrl_pin_store.py`), each in a clone whose objects are all loose in its own store, forge one object beside an edit: the pinned `src/` tree (R585-12's F1), the pinned commit, and the edited source's blob.
- Item 2, R585-12-S1 (`b62c1981`): the helper runs `git -c core.fsmonitor=false -C <dir> …`. Two standing controls: a superproject whose own configuration names a recorder (its gitlink read, the recorder never started), and the stack's own configuration beside an edit.
- Item 3, R585-12-S2, taken (`4a35f2f4`): the alternates control's setup also deletes the clone's `objects/info/alternates`.
- Self-review (`a8fe548a`): the object-store controls replace a loose file with a new one rather than write into it, so no file a hard link shares with another store is written.
- README: the check, the setting, the figure `84 pin controls` (checked by the self-test) and the five controls.
- Item 4: R585-12-RS1 to RS4 and R584-11-RES-1 are applied in the prepared PR body, for the manager. R584-11-S1 is not taken: it needs a history rewrite.

Validation (fresh clones at the head; the runner's Ubuntu 24.04 replica: CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, cmake 3.28, clang 18, `MAKEFLAGS=w`, four CPUs each, the pinned RV32 SDK and Verilator 5.050):
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS in 750 s; 2822 compiled sources of 3053 invocations, 0 findings, 105 boundary, 84 pin and 4 figure controls, 0 misbehaved.
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator`: PASS in 518 s; 6, 84 and 4, 0 misbehaved.
- `firmware-unit`'s steps: every one rc 0, 2197 s. `mutants: 506 of 506 caught`, 915 verdict lines `[ok]`, each equal to round 13's. Coverage is 100 % in 30 files, every row equal; the store gate passes 435 tests.
- Images: 35 of 35 ELF hashes identical to dev `c20c85bd`'s at every shape (manifest sha256 `8b1292db…`).
- R585-12's `forge_probe.py`, unchanged: F0 REFUSED `src/adp.c`. F1 REFUSED: `tsn-c-stack's object store holds a forged or corrupt object: the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40, not to its id, so nothing under it can be compared` (ACCEPTED at `8aaa2da7`). F2 REFUSED: `… the pinned commit (commit 405dc683) hashes to 55f2ca0d …`. F3 ACCEPTED, 0 program starts.
- R584-11's `model_routes.sh`, unchanged: clean exit 0, edit exit 2 `src/adp.c`. Route 1 exits 2 naming the forged `src/` tree (exit 0 at `8aaa2da7`). Route 2 exits 0 with 0 recorder lines.
- R585-12's superproject `core.fsmonitor` probe on disposable clones: 2 program starts at `8aaa2da7`, 0 at the head.
- Mutants on a disposable clone. With no hash compared, the forged-tree and forged-commit controls escape (`accepted 405dc683…`): Git checks neither through `cat-file`. With `core.fsmonitor=false` removed, the superproject control escapes.
- R585-12-S2, with the stack cloned by `--reference`: the alternates control escaped at `b62c1981` and holds from `4a35f2f4`. All 22 environment and store controls pass with and without it.
- Every entry point: 17 entry points under 7 states, two of them forged objects (the pinned `include/` tree, the pinned commit). 119 of 119 are refused before any build.
- The hook-rule campaign: H0 clean, and H1 to H24 caught on CPython 3.12.3 and 3.14.7. H22 and H23 escape 11 and 9 controls (round 13: 17 and 11), because the new setting also holds the `core.fsmonitor` controls when those mutants let the caller's environment reach Git. The clean proof and the 34 hook plants: 35 of 35 on both interpreters.
- The docs job's 54 commands: 53 of 54. The one failure is the known `check_rtl_source_lists.py --selftest` (48 of 50 under `MAKEFLAGS=w`, as at dev; 50 of 50 without it). `check_em_dash.py --base c20c85bd` finds 0 over 409 added lines, `docs_check.py` finds 0, and `check_py_idiom.py` holds every ratchet.

Acceptance criteria:
- #697 acceptance 1 to 5 are unchanged and met: the pin is `405dc683`, the cores come from the submodule, and the images are identical.
- Round-14 items 1 to 3 are met as above, and item 4 is applied in the PR body.
- The 79 pin controls and the environment controls still hold: all are `[ok]` among the 84.

Open risks/questions:
1. "Refused by name": the refusal names the forged object by its place and id (`the pinned src/ tree (tree 5c8c189a)`). It does not name the edited file under it, since the only listing of a forged tree the store gives is the forged one. So R584-11's route 1 ends in exit 2 naming the `src/` tree, not `src/adp.c`.
2. Git 2.36 or later reads `core.fsmonitor=false` as off. Earlier Git took the setting as a hook path.
3. Dev moved to `c6bd08c6` (PR #707). A merge with the head conflicts only in the generated submodule diagram (three files, which its generator remakes). This round merges nothing.
4. Process, self-review: a scratch evidence script ran in a hard-linked local clone and overwrote two loose objects of the lane's own submodule store, for under two minutes. The new check caught it in the image build. The objects are restored and `git fsck --full` is clean. Every overlapping run was discarded and rerun, and the script now replaces files. The in-tree controls never write a shared file, and `a8fe548a` hardens them anyway.
5. Carried: the `MAKEFLAGS=w` source-list self-test (as at dev); `firmware-unit` headroom (#716); R584-9-S1 optional; residue to #495.

Not run: act (no workflow, act or CI file changes this round) and hosted CI (not pushed). The round-14 evidence (HANDOFF Round 14, gate logs, scripts) is with the manager for publication.
