[R632] NEGATIVE - exact head 97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab

# R632-3 internal independent review: issue #734 / PR #735

- **Head**: `97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab`, tree `5d3882e64db8e496d3f47221192324de6d5b40fd`.
- **Source base**: `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`.
- **Diff examined**: all of `a0f39ad4..97907c2e`, which is 8 files and six linear one-line commits. I also examined the Round 3 delta `33ac35b5..97907c2e` (four commits).
- **Context**: cleared context. I read AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue #734 body, assignment comments 6151273761, 6151933918 and 6152693618, and docs/testing/CI_WORKFLOWS.md. Prior public findings were read only after my own pass over the diff.
- **Result**: all five lenses were applied. **The live-base rule is sound.** Hosted scope classifies exactly what landing the PR changes in its base. The replay composes the same merge. I found no path where a PR's own RTL change, or an RTL file that a merge restored, is classified docs-only (no BLOCKER).
- **Why NEGATIVE**: one MINOR stays open (F1). The new sibling-import control covers only part of the self-test. A sibling import planted elsewhere in the runner self-test passes the form CI runs, yet it breaks the documented flat install. There are also two RESIDUE items (prose only) and one retained SUGGESTION.

## Findings

### R632-3-F1 MINOR - Tests, Conformance - the sibling-import control covers only the scope-event call graph, so the self-test can regain a sibling import without any CI-run form failing

- **Location**:
  - `scripts/act_ci.py:6477-6508` (`selftest_scope_flat_install`). Its isolated child runs only `selftest_scope_event` through `runpy`. The planted import is appended at module level.
  - `.github/workflows/docs.yml:389` runs only the ordinary `python3 scripts/act_ci.py --selftest`, where `scripts/` is on `sys.path`.
- **Authority**:
  - Round 3 assignment, item 1 (issue comment 6152693618): "Add a control that fails if the selftest regains a sibling import."
  - R633-2-F1, required outcome: "a control must detect loss of standalone/isolated support."
- **Evidence** (`mutations_runner.json`, `apply_mutation.py`, `run_act_selftest_boxed.sh`; receipts `receipts/mutations_runner.txt` and `receipts/mutations/mut_R0*_*.log`; all runs inside a network-less, credential-less bubblewrap boundary):

  | Mutation | Ordinary `--selftest` (the CI form) | Documented flat `python3 -I <dir>/act_ci.py --selftest --worktree` |
  |---|---|---|
  | R02: `import ci_scope_history` inside `selftest_scope_history_wiring` | **rc 0, PASS** | rc 1, `ModuleNotFoundError: No module named 'ci_scope_history'` |
  | R03: the same import inside `scope_fixture_history` | rc 1, the control `flat isolated scope uses the explicit shipping worktree` FAILs | rc 1 |
  | R01: `failures += history_selftest(ROOT)` removed | rc 1 (the wiring control FAILs) | rc 1 |

- **Impact**:
  - R633-2-F1's defect class can return through any selftest function outside `selftest_scope_event`'s call graph, including the history-wiring function added in this same round, and stay green in hosted CI.
  - The failure appears only when someone next runs the documented bootstrap command. It fails closed (no false pass), which is why this is MINOR rather than MAJOR.
- **Required outcome**: a control that runs in the ordinary CI-run self-test and fails when any part of the runner's `--selftest` needs a module that is neither in the standard library nor already documented. Two ways to get it:
  - run the whole `--selftest --worktree` in the isolated flat child, with a guard that stops the child recursing into this arm; or
  - check every `import` in `act_ci.py` statically against `sys.stdlib_module_names` plus the documented optional `yaml`.
  - Do not give candidate Python host import authority.
- **Verification**: mutation R02 (`mutations_runner.json`) must make the ordinary `python3 scripts/act_ci.py --selftest` fail. R03 and R01 must still fail. The unmutated head must pass both forms.

### R632-3-R1 RESIDUE - Docs - stale fail-safe sentence in TESTING.md

- **Location**: `docs/testing/TESTING.md:1415-1418`. It still says the elaboration classifier "fails safe - an empty diff or an unresolvable base both come back RTL-relevant."
- **What is true at this head**: on a pull request, an unresolvable revision or merge ancestry fails the scope step (`elaborate.yml:104-114`; `CI_WORKFLOWS.md:231-233`). This is the same sentence class as R632-2-R1, which was corrected in CI_WORKFLOWS.md and in the `elaborate.yml` comment, but this copy was missed.
- **Exact fix**: replace "an empty diff or an unresolvable base both come back RTL-relevant" with "an empty diff comes back RTL-relevant, and on a pull request an unresolvable revision or merge base fails the scope step".

### R632-3-R2 RESIDUE - Docs - PR body repeats its closing keyword

- **Location**: PR #735 body, under "Linked Issue / roles". `Closes #734` appears twice on consecutive lines.
- **Exact fix**: delete one of the two lines.

### R632-3-S1 SUGGESTION - Robustness - hosted merge-shape guard (R632-2-S2, retained)

- **What**: the hosted branch diffs `GITHUB_SHA^1..GITHUB_SHA` without asserting that `GITHUB_SHA^2` is `PR_HEAD_SHA`. That variable is already bound in the step.
- **Evidence**: `receipts/prior/r632_2_ff_guard.log` reproduces the demonstration. If the head itself were checked out, a docs+RTL PR would give `rtl=false`.
- **No real path**: GitHub's pull_request `GITHUB_SHA` is always the test merge. The PR body records the guard as deliberately unchanged.
- **Optional fix**: a one-line guard would make the step fail closed.

## Prior public findings at this head

| Prior ID | Disposition at 97907c2e | Evidence |
|---|---|---|
| R632-1-F1 BLOCKER (REV/REV+E docs-only) | **RESOLVED** | R632-1's `probe_scope.py` (sha256 `3e18e600…`, matching its manifest) was run unchanged. Its functions, with only `HEAD` rebound to this head: REV and REV+E `rtl=true` in all three bodies; B16 landed merge 2 docs paths, `rtl=false`; two-dot 65 (`--no-renames`) and 64 (default). See `receipts/prior/r632_1_unchanged.log` and `r632_1_at_97907c2e.log`. R633-2's grader also passes (nine outcomes; `r633_2_replay_prior.log`). |
| R632-1-F2 MINOR (contract bindings in prose) | RESOLVED | `CI_WORKFLOWS.md` items 6, 7, 11 and 15 name `PR_BASE_REF` and `PR_HEAD_SHA` with their expressions. They match `ci_events.py` `DECIDE_STEP_ENV`, `FAST_SCOPE_STEP_ENV`, `INHERITED_STEP_ENV` and the carrier list. `ci_events --check` passes. |
| R632-1-F3 / R632-2-S1 / R633-2 retained SUGGESTION (history wiring unpinned) | RESOLVED | `act_ci.py:6453-6474` pins the call by AST. Mutation R01 makes both runner forms fail (`receipts/mutations/mut_R01_*`). Note that `ci_scope.py --selftest` alone still passes R01 (M14), as designed. |
| R633-1-D1 RESIDUE | RESOLVED | Same lines as R632-1-F2. |
| R632-2-F1 MINOR (ambient Git in fixtures) | **RESOLVED** | `ci_scope_history.py:18-45` and `act_ci.py:6204-6231` strip `GIT_*`, isolate global and system config, fix identities and dates, and disable signing, hooks and automatic maintenance. My hostile re-check (`hostile_env_check.sh`) runs the selftest with a signing global config and with exported `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`: both PASS, and the victim `.git` bytes are unchanged (`receipts/hostile_env_check.txt`). The in-tree arms `ambient signing`/`gitdir` pass. |
| R632-2-F2 MINOR (replay set differs from hosted) | **RESOLVED** (option a) | The replay composes `merge-tree --write-tree live head` and diffs live against it. R632-2's `probe_r632_2.py` was run unchanged: its only MISS is `identical-on-dev`, where its old oracle wanted the replay to be a superset; hosted and replay now agree (`receipts/prior/r632_2_probe.log`). `rename_divergence_r632_2.sh` hard-codes the retired head-only formula, so it still prints that formula's divergence (`r632_2_rename_divergence.log`). The shipping bodies at this head give equal sets for that case: my `build_rename_cases.sh` + `probe_r632_3.py` (`receipts/rename_probe.txt`), and the in-tree control `base-side rename`. |
| R632-2-R1 RESIDUE | RESOLVED in CI_WORKFLOWS.md:231-233 and elaborate.yml:80-81 | A further copy in TESTING.md remains: see R632-3-R1. |
| R632-2-S2 SUGGESTION | RETAINED as R632-3-S1 | `receipts/prior/r632_2_ff_guard.log` |
| R633-2-F1 MAJOR (flat isolated install fails) | **RESOLVED** for the defect; its control requirement is only partly met (R632-3-F1) | The documented flat install (`install -m 0555`; `python3 -I <dir>/act_ci.py --selftest --worktree <candidate>`) gives rc 0 with 566 ok and 0 FAIL inside the bubblewrap box (`receipts/act_selftest_flat.*`). |
| R633-2-D1 RESIDUE (stale "local and unpushed") | RESOLVED | The current PR body no longer contains it. |

Prior probes that do not apply at this head, recorded rather than counted:

- R633-1 `scope_probes.py` asserts the round-1 `PR_BASE_SHA` binding, which round 2 removed on purpose (KeyError; `r633_1_scope_probes.log`).
- R632-2's `replay-2dot` mutant anchor no longer exists in the composed body (AssertionError, mutant not applied).
- R632-2's `no-all` mutant is not killed by that probe. The in-tree `ambiguous replay base refuses` arm kills it (my M09).
- R633-2 `scope_audit.py` needs a Git checkout as its source. Re-run against a shared clone at this head: PASS, 95 executions (`r633_2_scope_audit_gitsource.log`). The run against an extracted tree failed only on `rev-parse` (`r633_2_scope_audit.log`).

## Executed evidence (this round, exact head)

Environment: Python 3.14.7, Git 2.56.0, PyYAML 6.0.3. No Docker and no act. The runner self-test ran only inside `run_act_selftest_boxed.sh`: bubblewrap, all namespaces unshared, no network, `/run` and `/var` replaced, home hidden, the candidate tree mounted read-only.

**Gates** (receipts in `receipts/`):

| Gate | Result |
|---|---|
| `ci_scope.py --selftest` | PASS, 197 ok (93 history assertions, 48 killing history mutations), 16 s |
| `ci_events.py --check` | OK, 2021 contract items |
| `ci_events.py --selftest` | PASS, 2021 items, 2850 arms |
| `act_ci.py --selftest`, ordinary form, boxed | PASS, 566 ok, 0 FAIL |
| `act_ci.py`, documented flat install, boxed | PASS, 566 ok, 0 FAIL, file mode `-r-xr-xr-x` |
| `docs_check`, `check_doc_style`, `check_doc_paths`, `check_baremetal_only --check/--selftest`, `check_py_idiom` (+selftest), `check_sh_idiom`, `measure_test_evidence --check/--selftest`, `measure_fail_fast --check`, `measure_naming --check`, `check_hygiene --check`, `check_todo_ownership`, `check_archive`, `pp_srcs --check` | all rc 0 (`receipts/gates_summary.txt`) |
| `check_em_dash`, `gen_toc --check/--verify-anchors/--selftest` | **not run by me**: they need the pinned Markdown renderer, and installing packages was not available in this session. The author's receipt `em-dash-head.log` (0 findings over 34 added lines) and the `r3-toc-*` receipts are in the public evidence tree. |
| `git diff --check a0f39ad4..HEAD` | clean. All six commits are one line with no trailers. |

**Independent real-history probe** (`probe_r632_3.py`; histories from `build_real_lanes.sh` on real repository commits). This is independent code: it takes the three bodies from the head's workflows, replacing only the recursive selftest call. Hosted means a two-parent merge with the live base as first parent; replay means `ACT=true`, the head checked out and `refs/remotes/origin/dev` set to live. Receipts: `receipts/real_lanes_probe.txt`, `.jsonl` and `real_lanes_cases*.json`.

| Case (all three bodies) | Hosted | Replay |
|---|---|---|
| B16, its actual landed merge `6c810c45` (first parent `e81ce82f`) | 2 `docs/findings/` paths, `rtl=false` | same |
| B16 composed on recorded base `49da9fd9` | 2 paths, `false` | same |
| B16 against current dev (already merged: empty delta) | 0 paths, `true` (fails safe) | same |
| This PR against live dev `a0f39ad4` | 8 paths, `true` | same |
| REV on real history: R=`49da9fd9`, dev D edits `hdl/common/KL_link_guard.sv`, lane merges D, restores, edits docs | 2 paths incl. RTL, `true` | same |
| REV+E (live = D + unrelated RTL commit E) | `true` | same |
| Evil merge: D merged with the RTL kept at R inside the merge commit | `true` | same |
| Dev reverts D after the lane merged it (landing changes no RTL) | 1 docs path, `false` (correct: the landed tree's RTL equals dev's) | same |
| The lane's own RTL on a stale base, then docs (live = E, and live = current dev) | 2 paths incl. RTL, `true` | same |
| The lane's own RTL conflicting with dev | GitHub builds no merge | replay step fails (rc 1), no output |
| Docs-only on a stale base (live = E) | 1 path, `false` | same |

Rename cases (`build_rename_cases.sh`, `receipts/rename_probe.txt`):

- Dev renames a page into gate-read `docs/reference/REGISTER_MAP.md` while the PR edits the page: `true` in both modes.
- Dev renames `hdl/a.sv` to `hdl/b.sv` while the PR edits `hdl/a.sv`: `hdl/b.sv`, `true` in both.
- The PR moves an RTL file into `docs/`: `true` in both.

**B16 counts** (`git diff` in this clone): two-dot `--no-renames` 65, two-dot default 64, three-dot 2. The landed `6c810c45^1..6c810c45` is the same 2 paths. This matches the issue table.

**Rule-removal mutations** (`mutations.json`, `run_mutation.sh`; `receipts/mutations.txt`, `receipts/mutations/*`). Each mutation was applied to a disposable copy of the head tree:

| Mutation | `ci_scope --selftest` | `ci_events --check` |
|---|---|---|
| M01 fast hosted two-dot frozen base / M03 elaborate same | FAIL | FAIL |
| M02 full hosted `$PR_BASE_SHA...$PR_HEAD_SHA` (round-1 rule) | FAIL | FAIL |
| M04 elaborate replay without composition / M05 fast replay endpoint trees / M06 full replay frozen base | FAIL | FAIL |
| M07 fast never takes replay path / M08 full always takes replay path | FAIL | FAIL |
| M09 `merge-base` without `--all` / M10 ancestry check removed / M16 merge-tree conflict swallowed | FAIL | FAIL |
| M11 empty-diff rule removed / M12 submodule-pointer rule removed / M13 `hdl/` as docs | FAIL | n/a (pass, the classifier is not pinned there) |
| M14 history call removed | pass (by design) | pass; the runner wiring control kills it (R01) |
| M15 fast push before-SHA ignored | FAIL | FAIL |

So every acceptance-3 control (docs-only on an old base, RTL on an old base, submodule pointer, empty diff) fails when its rule is removed.

**Push behaviour**: `rtl-fast.yml:58-69` keeps the before-to-after diff and the `git ls-files` fallback. `rtl.yml:108-113` and `elaborate.yml:100-103` keep non-PR events at `rtl=true`. The in-tree arm `fast push retains before-to-after comparison` and my M15 confirm this.

**Replay wiring**:

- `materialize_remote_head` (`act_ci.py:1839-1909`) fetches `refs/heads/dev` into `refs/remotes/origin/dev` with full history and checks it against `run.validation_base`.
- The runner refuses non-`dev` bases (`act_ci.py:860`, `:1056`). `build_event` keeps `base.ref = pr.base_ref`, so `PR_BASE_REF` resolves to the verified ref.
- The selftest drives `resolve_validation_base` and the production `build_event` through all three bodies (`act_ci.py:6416-6450`).

**Five linked images**:

- The diff changes only `.github/workflows/{rtl,rtl-fast,elaborate}.yml`, `docs/testing/CI_WORKFLOWS.md` and `scripts/{act_ci,ci_events,ci_scope,ci_scope_history}.py`.
- None of these is read by the firmware or builder image paths. A `git grep` found only prose and test references under `sw/`, `syn/` and `tb/`.
- No gitlink changed (`git diff --raw` shows no `160000`).
- I did not rebuild the images (builder banks are out of scope for me). The author's `image-hashes.json` records five byte-identical before/after pairs.

**Hosted at exact head** (inspected only; acceptance belongs to the manager). At the time of inspection (`receipts/hosted_check_runs.txt`):

- completed with success: `wire-accountability` and `docs-check-no-git`;
- in progress: `docs-check` and `elaborate`;
- queued: `full-ci-gate`, `changes` and `bdd-conformance`.

## Ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue #734 acceptance 1-5 and Round 2/3 decisions, checked against `rtl.yml:97-139`, `rtl-fast.yml:35-75` and `elaborate.yml:83-115`. `act_ci.py:2376-2420` (`build_event`), `:1839-1909` and `:860`. B16 reproduced on real history; REV, REV+E and evil-merge cases on real commits (`receipts/real_lanes_probe.txt`). `CI_WORKFLOWS.md:168-213` and `:1542-1561` (rule and why it is safe). Round-3 item 1 is partly met (F1). | R632-3 | 97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab |
| RTL | CLEAN | No HDL, gitlink or image input changed (`git diff --raw a0f39ad4..HEAD`). The CI job architecture and interface contracts examined: `fetch-depth: 0` on all three checkouts, step env pinned by `ci_events.py` `DECIDE_STEP_ENV`/`FAST_SCOPE_STEP_ENV`/carrier list, the scope job's outputs and guards unchanged, the runner's flat-install interface passing (`receipts/act_selftest_flat.*`), and the replay ref fetched and verified at `act_ci.py:1839-1909`. | R632-3 | 97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab |
| Robustness | CLEAN | Conflict, missing and ambiguous ancestry, missing head, and empty delta: in-tree `edge_controls` (`ci_scope_history.py:239-265`) plus my M09, M10 and M16. Hostile Git environment (`receipts/hostile_env_check.txt`). Push fallback (`rtl-fast.yml:58-69`, M15). Rename, revert and evil-merge histories (`receipts/rename_probe.txt`, `real_lanes_probe.txt`). The merge-shape guard is a SUGGESTION only (S1). | R632-3 | 97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab |
| Tests | UNCLEAN (F1) | `ci_scope_history.py:71-353`, `act_ci.py:6204-6508`, and the `ci_events.py` `#734` arms (`:6427-6446`). 16 scope mutations and 3 runner mutations (`receipts/mutations*.txt`). Prior probes re-run unchanged (`receipts/prior/`). Counts verified: 197, 48, 2850, 566. F1: control coverage. | R632-3 | 97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab |
| Docs | CLEAN (RESIDUE R1, R2 carried) | `CI_WORKFLOWS.md:168-233`, `:674-705`, `:789`, `:889-893`, `:961-963`, `:1099-1101`, `:1172-1176`, `:1542-1561` and `:1600-1605`, checked against the workflows and `ci_events.py`. `act_ci.py` `build_event` docstring. `elaborate.yml:77-82` comment. A stale-statement search across `*.md`/`*.py`/`*.yml` found TESTING.md (R1). PR body (R2). `docs_check`, `check_doc_style` and `check_doc_paths` rc 0. | R632-3 | 97907c2e966035b64fcc8d9fa2e4b8a56e5f93ab |

## Real limits

- I did not run `act`, Docker, the trusted replay, or any live-PR invocation. Whether the act image's Git supports `merge-tree --write-tree`, and whether the materialized `refs/remotes/origin/dev` reaches the act container, are not proven here; the manager's trusted full replay is that evidence.
- The runner self-test ran in an unprivileged bubblewrap box, not in a CI job container.
- Hosted runs are modelled with a local two-parent merge, except B16, where the actual landed merge `6c810c45` was used.
- I did not run `check_em_dash` or `gen_toc`, because the renderer was unavailable. For those I rely on the author receipts and the hosted `docs-check`.
- Images were not rebuilt. Physical calibration was NOT RUN; field skips are not hardware proof.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Carry R632-3-R1 and R632-3-R2 to the residue checklist.
- Assign F1 for a fix and re-review.
- Run the trusted full act replay from a clean live-dev worktree. It must show the replay scope step resolving `refs/remotes/origin/dev` and classifying this PR as relevant.
- Hosted acceptance at the final head.
- Build the current-dev merge candidate (builder and native banks) at the merge turn, in the stated 697c-then-696 order.

## Exact-head restoration

`receipts/exact_head_restoration.txt` records the following for the review clone:

- HEAD `97907c2e…`, tree `5d3882e6…`, 0 porcelain lines, worktree = index = HEAD;
- one worktree;
- 1313 index entries matching the tree, with mode/blob/path digests `695460d8…` for both;
- gitlinks `external efeb541a`, `gptp-processor 7dda9c3b`, `protocol-processor 2ad2f845`, `third_party/lwSRP 08ee86e8` and `third_party/verilog-axis 48ff7a7e`, with the initialized ones checked out at their gitlinks.

All probes and mutations ran in disposable copies or shared clones under `scratch/`.

R632-3 FINISHED
