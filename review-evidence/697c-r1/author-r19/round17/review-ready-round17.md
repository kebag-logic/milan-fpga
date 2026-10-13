[A583] REVIEW READY

Commit: 5b4ea55160c5ee34263e24140f960c4f03d923bc (round 17, branch `697-consume`: `6e88cfb6` on `516a69be`, then a merge of dev `c6bd08c6`; not pushed, per the assignment)

Changed (`6e88cfb6`: four files under `sw/firmware/ctrl`, +157 −92; no firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin change):
- Item 1, R584-14-F1, outcome (a): one key parser.
  - `ctrl_build.parsed_key` splits each key Git lists the way Git's own `parse_config_key` does: a section, a subsection (absent, empty or named) and a variable. `ctrl_build.configuration` parses every key once with it, for both repositories.
  - `superproject_configured`, still called by `stack_gitlink` before `ls-files --stage`, refuses every key whose section and variable `SUPERPROJECT_REFUSED` lists, whatever its subsection. These are round 16's six: `extensions.partialClone`, `remote.promisor`, `remote.partialCloneFilter`, `remote.uploadpack`, `core.sshCommand` and `core.fsmonitor`. The subsection never decides.
  - The superproject's other keys still pass: the `actions/checkout` control (`http.https://github.com/.extraheader`, `gc.auto`, the remote, the stack's submodule entries) is accepted.
  - The stack's allowlist uses the same parser (`ctrl_build.family`). `*` stands for a named subsection, and an empty subsection is in no family it lists. Its verdicts are unchanged.
- Item 2: controls. 106 pin controls in all.
  - Three new standing controls in `ctrl_pin_store.py` use R585-14's sparse superproject with a promisor remote declared three ways:
    - `remote.promisor` with no subsection;
    - `remote.partialCloneFilter` with no subsection;
    - `remote "".promisor`, an empty subsection.
  - Git names each of those remotes `""`, and each reaches a recorder through `url."ext::<recorder>".insteadOf=` with `protocol.ext.allow=always`. The check refuses neither of those two keys. Each control is refused naming its one promisor key, and no recorder runs.
  - A fourth control covers the stack's side: `submodule "".active` is refused by that key.
- Item 3: the texts state exactly what is held. The superproject declares no promisor remote in any key spelling Git reads, judged by section and variable. The stack's configuration holds Git's own bookkeeping only. `GIT_NO_LAZY_FETCH=1` and `core.fsmonitor=false` are defence in depth. "On any Git" and "whatever a Git version makes of it" are gone. The places are:
  - `README.md:175-189`, `:223`, `:244`, `:249-255` and `:259`;
  - `ctrl_build.py:182-219` and the docstrings of `parsed_key`, `configuration`, `family`, `configured` and `superproject_configured`;
  - `ctrl_pin_store.py:3-78`;
  - `ctrl_pin.py:61-70` and `:136`;
  - the prepared PR body's Status, Round 17 section and Known limitations.
- Residue:
  - R584-14-RES-1 at `README.md:189`.
  - R585-15-RES-1 at `README.md:188` and `ctrl_build.py:188`. Its `README.md:186` part is the same sentence R584-14-RES-1 rewrites, so that sentence takes R584-14-RES-1's text, as the assignment directs.
  - R585-15-RES-2 in the prepared PR body.
- Item 4: the dev merge (`5b4ea551`).
  - `git fetch origin dev` gave `c6bd08c6`. The merge commit stopped in three conflicts, all in the generated submodule diagram (`.drawio`, `.png` and `PNG_MANIFEST.json`).
  - `submodule_boundaries.gen.py` remade the diagram from both sides' gitlinks: tsn-c-stack `405dc683` and dev's gptp-processor `7dda9c3b`. The manifest is dev's, with only that entry rewritten.
  - No other conflict occurred, and nothing in the merge touches firmware or an image input. The merged tree differs from dev only in this lane's 72 files.

Validation (fresh clones sharing no file with the lane; upstream Git 2.43.0 built from `git-2.43.0.tar.xz`, the reviewer's sha256; the runner's Ubuntu 24.04 replica: CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, cmake 3.28, clang 18, Ubuntu's Git 2.43.0, `MAKEFLAGS=w`, four CPUs each, the pinned RV32 SDK and Verilator 5.050):
- R584-14's `superproject_spelling_probe.py`, unchanged (all 42 files of its packet match its manifest):
  - at the head on upstream 2.43.0, S2, S3 and S6 to S9 end REFUSED naming the key with `RAN=0`. Examples: S6 `remote.promisor (local)`, S7 `remote.partialclonefilter (local)`, S9 `remote..promisor (local)`, S2 `remote..promisor (local), remote..uploadpack (local)`;
  - S0 and S5 keep their verdicts, and the same results hold on Git 2.56.0;
  - at `516a69be` on upstream 2.43.0, R584-14's receipt is reproduced: S6, S7 and S9 `RAN=1`, and S8 ACCEPTED after a fetch.
- R584-14's `stack_spelling_probe.py`, R585-14's five probe scripts and R584-12's `store_probe.py` print what they printed at `516a69be`, on both Gits.
- Mutants on a disposable clone, all 106 pin controls with the census and the figure check (R584-14's `run_pin_controls.py`), Git 2.56.0 / upstream 2.43.0:
  - round 16's match (a remote key refused only with a named subsection): 3 / 3 escape, the three new controls. On 2.43.0 Git runs the recorder through the rewrite;
  - only a named or empty subsection refused: 2 / 2;
  - only a named subsection or none refused: 1 / 1;
  - the stack's `*` family holding an empty subsection: 1 / 1;
  - the parser reading an empty subsection as none: 1 / 1;
  - the parser reading no subsection as empty: the run stops at the allowlisted control's setup;
  - the check not called: 7 / 7;
  - the check after the index read: 0 / 5, Git running the recorder;
  - each of the six pairs left out in turn: 1 to 4;
  - the work tree's scope left out: 1 / 1;
  - no `core.fsmonitor=false`: 0 / 0, and no `GIT_NO_LAZY_FETCH`: 0 / 0, each defence in depth.
- `ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS in 724 s; 2822 compiled sources of 3053 invocations, 0 findings, 105 boundary, 106 pin and 4 figure controls, 0 misbehaved.
- `ctrl_boundary.py --require-rv32 --selftest --only verilator`: PASS in 503 s; 829 of 930, 6, 106 and 4, 0 misbehaved.
- `firmware-unit`'s steps: every one rc 0, 2153 s. `mutants: 506 of 506 caught`, and the 915 verdict lines are `[ok]` and identical to round 16's. Coverage is 100 % in 30 files, every row identical; the store gate passes 435 tests.
- Images: 35 of 35 ELF hashes are identical to dev `c6bd08c6`'s, built from dev itself, at every shape (manifest sha256 `8b1292db…`). `ctrl_image.py --base c6bd08c6` gives `+0` in every section at both shapes.
- Every pin control with the census and the figure check: 106, 0 misbehaved, census 0, figures 0. This holds on Git 2.56.0 and upstream 2.43.0 (CPython 3.14.7 and 3.12.3) and on the replica's 2.43.0.
- Every entry point: 17 under 12 states. Two states are new: the superproject's `remote.promisor` and `remote "".promisor`, each over an `ext::` rewrite. 204 of 204 are refused by name before any build, and no program starts.
- The hook-rule campaign: H0 clean, and H1 to H24 caught on CPython 3.12.3 and 3.14, every escape count equal to round 16's.
- The docs job's 54 commands: 53 of 54. The one failure is `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w`, 48 of 50, the same at dev `c6bd08c6` (50 of 50 without it). `check_em_dash.py --base c6bd08c6` finds 0 over 435 added lines. The diagram, PNG and submodule-doc checks and their self-tests pass.

Acceptance criteria:
- #697 acceptance 1 to 5 are unchanged and met: the pin is `405dc683`, the cores come from the submodule, and the images are identical to dev's.
- Round-17 items 1 to 4 are met as above.
- Every earlier pin control holds.

Open risks/questions:
1. The superproject's keys outside the six sections and variables are not judged, as assigned. Round 16's 28-key scratch measurement stands.
2. The fourth new control (`submodule "".active`, the stack's side) was not asked for. It is added so that the allowlist's empty-subsection branch has a control that fails without it.
3. `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1` have no control that fails when one alone is removed (R585-14-S2, optional, not taken). R585-14-S1 and S3, R584-13-S1, and R585-13-S1 and S3 are optional and not taken.
4. Carried: the `MAKEFLAGS=w` source-list self-test (as at dev); `firmware-unit` headroom (#716); residue to #495.

Not run: act (no workflow, act or CI file changes, in this round or in dev's merge) and hosted CI (not pushed). The round-17 evidence (HANDOFF Round 17, gate logs, scripts) is with the manager for publication.
