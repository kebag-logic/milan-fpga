[A583] REVIEW READY

Commit: 44eef11f8ee0d0f980eb68355c930efe2cce8cd8 (round 15: one commit on `a8fe548a`, branch `697-consume`; not pushed, per the assignment)

Changed (five files under `sw/firmware/ctrl`, +258 −52; no firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin change):
- Item 1, R584-12-F1 = R585-13-F1: the configuration allowlist. `ctrl_build.configured` runs, through the helper, before the proof reads any object of the stack. It lists all the configuration Git reads there (`git config --list --show-scope -z`) and refuses by name and scope every key outside `ctrl_build.STACK_CONFIG`, all at once. The allowlist is the assignment's list: `core.repositoryformatversion`, `core.filemode`, `core.bare`, `core.logallrefupdates`, `core.worktree`; `remote.*.url`, `remote.*.fetch`; `branch.*.remote`, `branch.*.merge`; and the submodule bookkeeping Git writes itself (`submodule.active`, `submodule.*.url`, `submodule.*.active`, `submodule.alternateLocation`, `submodule.alternateErrorStrategy`). The command line's one key is the helper's own `core.fsmonitor=false`. Example: `tsn-c-stack's repository holds configuration outside the pin proof's allowlist: core.sshcommand (local), extensions.partialclone (local), remote.probe.promisor (local)`. Every way of initialising the stack I measured writes only allowlisted keys, on Git 2.56.0 and on Ubuntu 24.04's 2.43.0: the workflows' `git submodule update --init`, `clone --recurse-submodules`, both `--reference` forms (`clone --reference --recurse-submodules` writes the two `submodule.alternate*` keys), a superproject worktree's, and the controls' clones.
- Item 2: `GIT_NO_LAZY_FETCH=1` is added to `GIT_ENVIRONMENT`, which the hook's judge requires key for key. Which Git honours it:
  - measured with R585-13's `lazy_fetch_env.sh` (2 transport starts without the variable, 0 with it): Git 2.56.0, and Ubuntu 24.04's `1:2.43.0-1ubuntu7.3` (its CVE-2024-32465 patch);
  - upstream source: defined from `v2.45.0`, and read by `v2.43.4` and `v2.44.1` (the CVE-2024-32465 releases); not by `v2.43.0` or `v2.44.0`;
  - the hosted runner: Git 2.55.0 (run 38205277457, image `ubuntu-24.04` `20261004.327.1`, from its checkout logs; not executed there).
  Where a Git does not honour the variable, the allowlist is the guarantee: with the variable removed, no control escapes.
- Item 3: 14 new standing controls; 98 pin controls in all.
  - 13 in `ctrl_pin_store.py`, each planting one refused family:
    - the two lazy transports (upload-pack, and ssh through `core.sshCommand`), each beside a missing pinned object;
    - `extensions.partialClone`, `remote.<name>.promisor`, `remote.<name>.uploadpack` and `core.sshCommand`, each alone;
    - `core.hooksPath`, `credential.helper`, and seven other keys Git starts a program for;
    - an include, a work tree's own configuration, and a key no Git defines.
  - Each is refused naming exactly its keys, and its recorder never runs. A clean clone holding a key of every allowlisted family is accepted.
  - The 14th, a line-ending conversion through the clone's attributes (no configuration), keeps "no file is hashed through Git" under a control.
  - Two existing controls are now refused by their key instead of by `src/adp.c`: the stack's own `core.fsmonitor` control (R584-12-S1 / R585-13-S2: it now fails without the allowlist) and the clean-filter control.
  - The `GIT_ATTR_SOURCE` environment control gives its filter through `GIT_CONFIG_COUNT`, not the clone's own configuration.
- Item 4: the README (`:170`, `:175-182`, `:216`, `:220`, `:237-249`), `ctrl_build.py`'s comments and docstrings, and `ctrl_pin.py`'s THE THREAT MODEL state the allowlist as the configuration guarantee. In the prepared PR body, the round-14 Status bullet and Contents line no longer say that no repository's own configuration starts a program; the Status, Contents and a Round 15 section state the allowlist. R584-12-RES-1 / R585-13-RES-1 are applied as given (the five links name `a8fe548a…`).

Validation (fresh clones at the head sharing no file with the lane; the runner's Ubuntu 24.04 replica: CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, cmake 3.28, clang 18, Git 2.43.0, `MAKEFLAGS=w`, four CPUs each, the pinned RV32 SDK and Verilator 5.050):
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS in 693 s; 2822 compiled sources of 3053 invocations, 0 findings, 105 boundary, 98 pin and 4 figure controls, 0 misbehaved.
- `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator`: PASS in 495 s; 6, 98 and 4, 0 misbehaved.
- `firmware-unit`'s steps: every one rc 0, 2100 s.
  - `mutants: 506 of 506 caught`; 915 verdict lines `[ok]`, each equal to round 14's.
  - Coverage is 100 % in 30 files, every row equal to round 14's; the store gate passes 435 tests.
- Images: 35 of 35 ELF hashes identical to dev `c20c85bd`'s at every shape (manifest sha256 `8b1292db…`).
- R584-12's `store_probe.py`, run unchanged:
  - at the head, `lazy_uploadpack_fail`, `lazy_uploadpack_serve`, `lazy_ssh` and `lazy_toctou` are each REFUSED by the allowlist naming their keys, `RAN=0`, and toctou's plant does not land;
  - at `a8fe548a`: `RAN=1`, `1`, `2` and `1`, with serve and toctou ACCEPTED and toctou's plant landing;
  - this holds on CPython 3.14 and 3.12.3 with Git 2.56.0, and in the replica with Git 2.43.0;
  - the other 16 probes keep their verdicts (`stack_fsmonitor` is now refused by `core.fsmonitor (local)`).
- R585-13's `forge_probes.sh`, run unchanged:
  - P13: exit 2, refused by name, 0 recorder runs (2 at `a8fe548a`);
  - P14: exit 2, 0 runs, no later edit (at `a8fe548a`: exit 0, 2 runs, edited);
  - P0 to P12 keep their verdicts (P11 is now refused by `core.fsmonitor (local)`).
- Each layer alone (on a disposable clone, Git 2.56.0 and 2.43.0): the allowlist without the variable, and the variable without the allowlist, each give `RAN=0` for all four lazy probes.
- Mutants on a disposable clone (38 configuration, environment and store controls):
  - M1, the allowlist not checked: 14 escape.
  - M2, the variable removed: 0 escape.
  - M3, both removed: 14 escape, with Git starting both transports.
  - M4, `--local` only: 2 escape (the include and the work tree).
  - M5, judged by section only: 10 escape.
  - M6, files hashed through Git: 1 escapes (the line-ending control).
  - M7, the allowlist checked after the object reads: 4 escape.
- Every entry point: 17 entry points under 9 states.
  - The clean filter is now refused by its key.
  - Two states are new: a partial clone over an ssh program with the pinned `include/` tree missing, and a line-ending conversion.
  - 153 of 153 are refused by name before any build, and the recorder never runs.
- The hook-rule campaign: H0 clean, and H1 to H24 caught on CPython 3.12.3 and 3.14.
  - Every escape count equals round 14's except H22 (30) and H23 (13): the allowlist also refuses the global and command-line keys those mutants let reach Git.
  - H0 is the clean proof, the 34 hook plants and the 17 environment controls, 0 escaped on both interpreters.
- Every pin control with the census and the figure check (R585-13's `run_pin_controls.py`): 98 pin controls, 0 misbehaved, census 0, figures 0.
- The docs job's 54 commands: 53 of 54.
  - The one failure is the known `check_rtl_source_lists.py --selftest` (48 of 50 under `MAKEFLAGS=w`, as at dev; 50 of 50 without it).
  - `check_em_dash.py --base c20c85bd` finds 0 over 423 added lines, `docs_check.py` finds 0, and `check_py_idiom.py` holds every ratchet.

Acceptance criteria:
- #697 acceptance 1 to 5 are unchanged and met: the pin is `405dc683`, the cores come from the submodule, and the images are identical.
- Round-15 items 1 to 4 are met as above.
- The 79 pin controls, the environment controls and the object-id controls hold: all are `[ok]` among the 98. One of the 79 (the clean filter) is now refused by the filter's key, which the allowlist refuses first.

Open risks/questions:
1. The superproject's own configuration is not under the allowlist: the assignment names the stack's, and `actions/checkout` writes keys into the superproject's (`http.<url>.extraheader`) that an allowlist would refuse. The proof reads only the superproject's index there, with `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1`.
2. A stack whose own configuration holds any other key (a developer's `pull.rebase`, `gc.auto`) is refused by that key's name until it is removed.
3. The hosted runner's Git version is read from its logs; nothing ran on the runner.
4. Carried: the `MAKEFLAGS=w` source-list self-test (as at dev); `firmware-unit` headroom (#716); R584-9-S1, R585-13-S1 and S3 optional; residue to #495. Dev is at `c6bd08c6`; this round merges nothing.

Not run: act (no workflow, act or CI file changes this round) and hosted CI (not pushed). The round-15 evidence (HANDOFF Round 15, gate logs, scripts) is with the manager for publication.
