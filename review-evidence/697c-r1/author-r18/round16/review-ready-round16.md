[A583] REVIEW READY

Commit: 516a69be9afba02670e37874294bd1f45ccb9316 (round 16: one commit on `44eef11f`, branch `697-consume`; not pushed, per the assignment)

Changed (four files under `sw/firmware/ctrl`, +194 −41; no firmware source, header, image builder, mutation table, coverage row, Makefile, workflow, build flag or pin change):
- Item 1, R585-14-F1, outcome (a): the superproject's keys.
  - `ctrl_build.superproject_configured` is called by `stack_gitlink` before `ls-files --stage` reads the superproject's index. Through the helper it lists all the configuration Git reads there: `git config --list --show-scope -z`, the repository's own file, an included one and its work tree's. The lister, `ctrl_build.configuration`, is now shared with the stack's allowlist.
  - It refuses by name and scope every key of `ctrl_build.SUPERPROJECT_REFUSED`, all at once. The keys are `extensions.partialClone`, `remote.*.promisor`, `remote.*.partialclonefilter`, `remote.*.uploadpack`, `core.sshCommand` and `core.fsmonitor`. Example: `the superproject's repository holds configuration that has Git start a program or fetch while the gitlink is read: extensions.partialclone (local), remote.origin.partialclonefilter (local), remote.origin.promisor (local), remote.origin.uploadpack (local)`.
  - The helper's own `command`-scope `core.fsmonitor=false` is not judged. The superproject's other keys are untouched: a superproject holding `actions/checkout`'s keys (`http.https://github.com/.extraheader`, `gc.auto`, the remote) and the stack's submodule entries is read as the pin.
- Item 2: controls. 102 pin controls in all.
  - Four standing controls are new in `ctrl_pin_store.py` (`superproject_controls`):
    - R585-14's shape: a sparse index whose sparse directory `third_party/` holds the gitlink without its tree, in a partial clone whose upload-pack is a recorder that then serves the tree;
    - the same, its remote reached over ssh by a recorder (`core.sshCommand`);
    - an included file and the work tree's own configuration, each naming a recorder as `core.fsmonitor`;
    - the superproject as `actions/checkout` and `git submodule update --init` leave it, accepted.
  - The superproject's `core.fsmonitor` control is kept, now refused by that key.
  - Each refused control names exactly its keys, and no recorder runs.
- Item 3: the texts state what is held: the stack's configuration by its allowlist, and the superproject's by these keys. `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1` are defence in depth. The places are:
  - `README.md:179-186`, `:220`, `:241` and `:246-250`;
  - `ctrl_build.py`: `GIT_ENVIRONMENT`, `HELPER_CONFIG` (was `:191-192`), `SUPERPROJECT_REFUSED` and the docstrings;
  - `ctrl_pin_store.py:24-65` (was `:44-48`);
  - `ctrl_pin.py`'s THE THREAT MODEL;
  - the prepared PR body's Status, Round 16 section, Known limitations, round-14 row 2 and round-15 open item (a).
- Item 4, the prepared PR body:
  - R585-14-RES-1 = R584-13-RES-1: the five reference links name `516a69be…`, the head the PR would merge at. The control firmware page changed again in this round; the other four links move with it for uniformity.
  - R584-13-RES-2: round 15's row 2 lists the checked CVE-2024-32465 maintenance releases (`v2.39.4`, `v2.42.2`, `v2.43.4`, `v2.44.1`).

Validation (fresh clones at the head sharing no file with the lane; upstream Git 2.43.0 built from `git-2.43.0.tar.xz`, the reviewer's sha256; the runner's Ubuntu 24.04 replica: CPython 3.12.3, gcc 13.3, GoogleTest 1.14.0, cmake 3.28, clang 18, Ubuntu's Git 2.43.0, `MAKEFLAGS=w`, four CPUs each, the pinned RV32 SDK and Verilator 5.050):
- R585-14's `r585_14_superproject_sparse_gitlink_serve.sh` and `r585_14_superproject_sparse_gitlink.sh`, unchanged (both match the packet's manifest):
  - at the head, on Git 2.56.0 and on upstream 2.43.0: REFUSED by `remote.origin.partialclonefilter (local), remote.origin.promisor (local), remote.origin.uploadpack (local)`, `RAN=0`;
  - at `44eef11f` on upstream 2.43.0: `gitlink 405dc683…` with `RAN=1`, and REFUSED with `RAN=1`.
- R585-14's other probes at the head, on both Gits: its two other superproject probes are refused by name with `RAN=0`; its stack probes print what its receipts print.
- R584-12's `store_probe.py`: 20 states, `RAN=0` on both Gits. Every verdict is as in round 15 but `super_fsmonitor`, now refused by `core.fsmonitor (local)`.
- The superproject's other keys: 28 keys that name a program or reach one (hooks, credential and other helpers, filters, a textconv, an `ext::` transport, an include), in a plain and in a sparse superproject. The gitlink is read, or refused for the missing tree, and no program starts, on Git 2.56.0 and upstream 2.43.0.
- Mutants on a disposable clone, all 102 pin controls, Git 2.56.0 / upstream 2.43.0:
  - the check not called: 4 / 4 escape (on upstream 2.43.0 Git runs the recorder in both sparse controls);
  - the check after the index read: 0 / 2, Git running the recorder;
  - the work tree's scope left out: 1 / 1;
  - each of the six keys left out in turn: 1 or 2 escape;
  - the helper's own setting refused too: the run refuses its own checkout;
  - no `core.fsmonitor=false`: 0 / 0, and no `GIT_NO_LAZY_FETCH`: 0 / 0, each defence in depth.
- `ctrl_boundary.py --require-rv32 --selftest --without verilator`: PASS in 696 s; 2822 compiled sources of 3053 invocations, 0 findings, 105 boundary, 102 pin and 4 figure controls, 0 misbehaved.
- `ctrl_boundary.py --require-rv32 --selftest --only verilator`: PASS in 495 s; 829 of 930, 6, 102 and 4, 0 misbehaved.
- `firmware-unit`'s steps: every one rc 0, 2074 s. `mutants: 506 of 506 caught`, and the 915 verdict lines are `[ok]`, each equal to round 15's. Coverage is 100 % in 30 files, every row equal; the store gate passes 435 tests.
- Images: 35 of 35 ELF hashes identical to dev `c20c85bd`'s at every shape (manifest sha256 `8b1292db…`).
- Every pin control with the census and the figure check: 102, 0 misbehaved, census 0, figures 0, on Git 2.56.0, upstream 2.43.0 and the replica's 2.43.0.
- Every entry point: 17 under 10 states, one new (the superproject a partial clone reached over an ssh recorder). 170 of 170 are refused by name before any build, and no program starts.
- The hook-rule campaign: H0 clean, and H1 to H24 caught on CPython 3.12.3 and 3.14, every escape count equal to round 15's.
- The docs job's 54 commands: 53 of 54. The one failure is the known `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w`, as at dev (50 of 50 without it). `check_em_dash.py --base c20c85bd` finds 0 over 431 added lines, `docs_check.py` finds 0, and `check_py_idiom.py` holds every ratchet.

Acceptance criteria:
- #697 acceptance 1 to 5 are unchanged and met: the pin is `405dc683`, the cores come from the submodule, and the images are identical.
- Round-16 items 1 to 4 are met as above.
- The 98 earlier pin controls hold. One of them, the superproject's `core.fsmonitor` control, is now refused by that key, as item 1 asks.

Open risks/questions:
1. The superproject's keys other than the six are not judged, as assigned. The 28-key measurement above is a scratch probe, not a standing control.
2. `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1` have no control that fails when one alone is removed (R585-14-S2, not taken). R585-14-S1 and S3 and R584-13-S1 are optional and not taken.
3. 13 receipts in R585-14's packet do not match its `MANIFEST.sha256`; its eight scripts do.
4. Carried: the `MAKEFLAGS=w` source-list self-test (as at dev); `firmware-unit` headroom (#716); residue to #495. Dev is at `c6bd08c6`, and this round merges nothing.

Not run: act (no workflow, act or CI file changes this round) and hosted CI (not pushed). The round-16 evidence (HANDOFF Round 16, gate logs, scripts) is with the manager for publication.
