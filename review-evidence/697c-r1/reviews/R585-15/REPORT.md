[R585] POSITIVE - exact head 516a69be9afba02670e37874294bd1f45ccb9316

# R585-15: external independent review of PR #705 (issue #697), rounds 14, 15 and 16

Head `516a69be9afba02670e37874294bd1f45ccb9316`, tree `544d7611d7baa462d9f7bc4b752fa6dc8b7fcedf`. This is a delta review of `8aaa2da7..516a69be`:
- round 14: `d89898db`, `b62c1981`, `4a35f2f4` and `a8fe548a`;
- round 15: `44eef11f`;
- round 16: `516a69be`.

The source base is `c20c85bd`. All five lenses were applied independently, and each has artifact-specific evidence below.

The head does what the round-14, round-15 and round-16 assignments ask:
- Every object the pin proof reads, the pinned commit and each tree under it, is hashed against its id and fails closed. No blob is read.
- R585-12's forged `src/` tree (F1) is refused by its place. F0 and F2 keep their verdicts.
- The helper gives Git `-c core.fsmonitor=false`.
- The stack's configuration allowlist runs through the helper before any object read, and refuses by name every key outside it.
- `GIT_NO_LAZY_FETCH=1` is set, and the versions that honour it are recorded correctly.
- The superproject's six promisor, transport and fsmonitor keys are refused by name before its index is read. `actions/checkout`'s keys and the submodule entries still pass.
- R585-14's two probes end in the named refusal with `RAN=0` on upstream Git 2.43.0. At `44eef11f` the same probes give `RAN=1`.
- 102 of 102 pin controls hold on Git 2.56.0 and on upstream Git 2.43.0, under CPython 3.14.7 and 3.12.13.

There is no open BLOCKER, MAJOR or MINOR. Two RESIDUE items are wording only. Six SUGGESTIONS are optional; five of them are carried from earlier rounds.

## Order of reconstruction

1. `AGENTS.md`, `CONTRIBUTING.md` (by way of `AGENTS.md`'s review bar), `docs/README.md` map.
2. Issue #697: the body and its frozen acceptance 1 to 5. Then the manager's comments:
   - the lane assignment (6091228902);
   - the round-12 scope ruling (6114400461);
   - the round-13 to round-16 assignments (6116488747, 6117713386, 6118625227, 6119960001).
3. The author's round-16 REVIEW READY (6120798872), which is the published gate evidence for this head, and the live PR body.
4. `git diff 8aaa2da7..516a69be`, read in full: six files, all under `sw/firmware/ctrl`. Then the history `c20c85bd..516a69be` (50 commits).
5. My own independent probes, mutants and pin-control runs (below).
6. Only after that: the prior findings of R585-14 (6119950198) and R584-13 (6119604125), with the earlier rounds' status as those two tabled it. Then the prior reviewers' published scripts, fetched by blob id and run unchanged.

## What the assignments ask, confirmed at this head

| Ask | Result | Evidence |
|---|---|---|
| R14-1: every object read is checked against its id, failing closed | The commit and every tree are read raw by `stored`, `ctrl_build.py:466-477` (`git cat-file <kind> <oid>`). Each is hashed as `<kind> <len>\0<raw>` with the repository's format and refused by its place if it differs. `pinned_tree` (`:480-499`) parses every tree itself. No blob is read: files are hashed from their own bytes (`blob_id`, `:432-436`) | The forged-tree and forged-commit controls `[ok]` (head log lines 74-75, `receipts/pin_controls.*`). Mutant `no_object_hash_check`: both escape on each Git. Mutant `tree_parse_ignores_subtrees`: 30 escape (`receipts/mutants_summary.txt`) |
| R585-12 `forge_probe.py` | F0 is REFUSED by `src/adp.c`. F1 is REFUSED as `the pinned src/ tree (tree 5c8c189a) hashes to 9b48fa40`. F2 is REFUSED as the pinned commit. F3 is now refused by `core.fsmonitor (local)`, with 0 program runs. All on both Gits | `receipts/prior/forge_probe.head.*.txt` (script blob `8365fc8a`, unchanged) |
| R14-2: `-c core.fsmonitor=false`, with a standing control | `ctrl_build.py:413`, `HELPER_CONFIG` `:195`. From round 16 the superproject's `core.fsmonitor` is refused by name first (the superproject `core.fsmonitor` control). The setting is defence in depth: removing it lets 0 controls escape on either Git | `receipts/mutants/*-no_helper_core_fsmonitor_false.txt` |
| R15-1: allowlist through the helper, before any object read, refusing by name | `configured` (`:521-532`) is called at `:561`. That is after `rev-parse --show-toplevel` (no object read) and before `rev-parse HEAD`, `--show-object-format` and every `cat-file`. It reads `git config --list --show-scope -z` through the helper (`configuration`, `:502-518`). Keys outside `STACK_CONFIG` (`:201-204`), and any non-local scope but the helper's own setting, are refused by key and scope | The 14 stack-configuration controls `[ok]` (head log lines 83-96). Mutant `no_stack_allowlist`: 14 escape on 2.56.0; on 2.43.0 the recorder runs and the run fails. Mutant `stack_allowlist_after_object_reads`: 4 escape on 2.56.0; on 2.43.0 the run fails |
| R15-2: `GIT_NO_LAZY_FETCH=1`; honoured versions recorded | Set in `GIT_ENVIRONMENT` (`:190-191`), which the audit hook's judge requires key for key. Upstream tags `v2.39.4`, `v2.42.2`, `v2.43.4`, `v2.44.1` and `v2.45.0` read it; `v2.43.0` and `v2.44.0` do not. Ubuntu noble's `2.43.0-1ubuntu7.3` binary holds the name; its release package `2.43.0-1ubuntu7` does not (see RES-1). Measured: with the check moved after the index read, 0 controls escape on 2.56.0 and 2 escape on upstream 2.43.0, where Git ran the recorder. So 2.56.0 honours the variable and 2.43.0 ignores it | `receipts/git_versions_and_lazy_fetch.txt`; `receipts/mutants/*-superproject_check_after_index_read.txt` |
| R15-3: R584-12 `store_probe.py` cases end in the refusal with `RAN=0` | All 20 probes end with `RAN=0` on both Gits. `lazy_uploadpack_fail`, `lazy_uploadpack_serve`, `lazy_ssh` and `lazy_toctou` are refused by the allowlist naming their keys, and toctou's plant does not land. `super_fsmonitor` is refused by `core.fsmonitor (local)` | `receipts/prior/store_probe.head.*.txt` (script blob `040fa985`, unchanged) |
| R15-3: one control per refused key family, plus an accepted clean clone | `ctrl_pin_store.py:376-416` holds 13 configuration controls, and the allowlisted-families clone is `accepted 405dc683…`. Each refusal names exactly its planted keys at this head | `receipts/pin_controls.head.py314.git2.43.0-upstream.txt` lines 83-96 |
| R16-1: the superproject's six keys refused by name before the gitlink is read | `stack_gitlink` calls `superproject_configured` (`:535-545`) at `:425`, before `ls-files --stage` at `:426`. It refuses `SUPERPROJECT_REFUSED` (`:213-214`) by key and scope, across the local file, an included file and the work tree's file, excluding only the helper's own command-scope setting. Every caller of `stack_pin` reaches it through `stack_gitlink`, because none passes a pin; the callers are `ctrl_image.py:453`, `ctrl_boundary.py:491`, `maap_differential.py:101`, the AECP tools and the Makefile's `--stack-pin` | The four refused superproject controls `[ok]` (head log lines 78-81). Own probe: mixed-case keys, the legacy `[remote.origin]` syntax, `includeIf "gitdir:"` and `includeIf "onbranch:"` are each refused by name with `RAN=0` on both Gits (`receipts/superproject_probe.*`) |
| R16-1: `actions/checkout`'s `http.<url>.extraheader` and the submodule entries still pass | The `actions/checkout` superproject control is accepted (head log line 82). My CI emulation: a depth-1 fetch with `gc.auto 0` and a persisted `http.https://github.com/.extraheader`, then the firmware jobs' `git submodule update --init` of the stack. The pin check prints `tsn-c-stack at 405dc683…`, rc 0, on Git 2.56.0 and on upstream 2.43.0. The stack's configuration written by `submodule update` (including `branch.main.*`) stays inside the allowlist | `receipts/ci_checkout_git256.log`, `receipts/ci_checkout_git243.log` |
| R16-2: R585-14's two probes end in the refusal with `RAN=0` on upstream 2.43.0 | `r585_14_superproject_sparse_gitlink_serve.sh` and `r585_14_superproject_sparse_gitlink.sh` are REFUSED by `remote.origin.partialclonefilter (local), remote.origin.promisor (local), remote.origin.uploadpack (local)` with `RAN=0`, on 2.56.0 and on upstream 2.43.0. At `44eef11f` on upstream 2.43.0 they give `gitlink 405dc683…` with `RAN=1`, and REFUSED with `RAN=1`. R585-14's other two superproject probes are refused by name with `RAN=0` | `receipts/prior/r585_14_*.txt` (blobs `e71e9190`, `d1510300`, `2d67468f`, `29f80acf`, unchanged) |
| R16-2: the new control is `[ok]` and ESCAPED under its mutant | Mutant `no_superproject_check`: the four refused superproject controls (`core.fsmonitor`, sparse upload-pack, sparse ssh, include and work tree) escape on both Gits, and on 2.43.0 Git runs the server or ssh recorder in the two sparse ones. `superproject_check_after_index_read`: the two sparse controls escape on 2.43.0 with the recorder run. `superproject_uploadpack_not_refused`: the sparse upload-pack control escapes. `superproject_worktree_scope_ignored`: the include and work-tree control escapes | `receipts/mutants/*` |
| R16-2: the 98 earlier pin controls hold | 102 of 102 `[ok]`, 0 misbehaved, census 0 findings, on CPython 3.14.7 with Git 2.56.0 and with upstream 2.43.0, and on CPython 3.12.13 with upstream 2.43.0. README figures: 0 findings, and 4 of 4 figure controls `[ok]`; a count of 101 is refused by name | `receipts/pin_controls.*`, `receipts/figures_head.txt` |
| R16-3: the texts state what is held for both configurations | The stack's configuration is held by its allowlist, and the superproject's by the six keys. `core.fsmonitor=false` and `GIT_NO_LAZY_FETCH=1` are defence in depth. This is stated at `README.md:175-186` and `ctrl_build.py:182-217` and `:420-423, 535-541`. It is also stated in `ctrl_pin_store.py:24-65`, in `ctrl_pin.py:59-70` (THE THREAT MODEL), and in the PR body's Status, Round 16 and Known limitations. All of these agree with the code and the receipts. One wording nuance is RES-1 | read against code |
| R16-4 and R14-4: PR-body residue | R585-14-RES-1 = R584-13-RES-1: the five links name `516a69be…`. R584-13-RES-2: round 15's row 2 lists `v2.39.4`, `v2.42.2`, `v2.43.4` and `v2.44.1`. R585-12-RS1 to RS4 and R584-11-RES-1 remain applied. One new stray-brace residue: RES-2 | live PR body |
| Images unchanged | `git diff --name-status 8aaa2da7..516a69be` lists `README.md` and five Python harness modules only. No firmware source, header, linker input, builder, Makefile or workflow changed. All six gitlinks are equal at `8aaa2da7`, `44eef11f` and `516a69be`, and lwSRP equals the source base `c20c85bd`. Images were not rebuilt here. The author's receipt is 35 of 35 identical to `c20c85bd` | `receipts/delta_scope_and_gitlinks.txt` |

## Findings

### RESIDUE (wording only; exact fixes for the manager's checklist)

**R585-15-RES-1 - Docs - the Ubuntu example for `GIT_NO_LAZY_FETCH` is true only of the updated package**
- **Artifact:** `sw/firmware/ctrl/README.md:185-186` ("and so does a Git patched for CVE-2024-32465, as Ubuntu 24.04's 2.43.0 is. Where a Git does not honour it (upstream 2.43.0 or 2.44.0), ..."), and the comment at `ctrl_build.py:187-188` ("such as Ubuntu 24.04's 2.43.0").
- **Evidence:** noble's release package `git_2.43.0-1ubuntu7` does not contain the string `GIT_NO_LAZY_FETCH`; `2.43.0-1ubuntu7.3` does (`receipts/git_versions_and_lazy_fetch.txt`). Any upstream release before 2.45.0 without the CVE-2024-32465 backport (for example 2.42.1) also ignores it, not only 2.43.0 and 2.44.0.
- **Impact:** wording only. The guarantee does not rest on the variable, and no figure, test, control or code depends on the sentence.
- **Exact fix:**
  - README:185: replace "as Ubuntu 24.04's 2.43.0 is." with "as Ubuntu 24.04's updated 2.43.0 package is (`2.43.0-1ubuntu7.3` checked; its release package `2.43.0-1ubuntu7` is not)."
  - README:186: replace "(upstream 2.43.0 or 2.44.0)" with "(any release before 2.45.0 without that fix, such as upstream 2.43.0 or 2.44.0)".
  - `ctrl_build.py:188`: replace "such as Ubuntu 24.04's 2.43.0" with "such as Ubuntu 24.04's updated 2.43.0".

**R585-15-RES-2 - Docs - stray braces in the PR body's Round 16 paragraph**
- **Artifact:** PR body, `## Round 16`, the paragraph after the table: "`firmware-unit`'s steps {every one rc 0 in 2074 s: `mutants: 506 of 506 caught`, the firmware gate's 915 verdict lines `[ok]` and equal to round 15's, coverage 100 % in 30 files with every row equal}."
- **Impact:** wording only; the braces are a template leftover.
- **Exact fix:** delete the `{` before "every one rc 0" and the `}` after "every row equal", and put a colon after "steps": "`firmware-unit`'s steps: every one rc 0 in 2074 s, `mutants: 506 of 506 caught`, ... with every row equal."

### SUGGESTIONS (optional; no effect on the verdict)

- **R585-14-S1 (retained, with new evidence) - Tests, Docs** - `ctrl_pin.py:994`.
  - The configuration controls are judged by `needle in detail`. `README.md:249` and `:256` say each is refused "naming exactly the keys it planted".
  - My mutant `superproject_over_refuses_include_path` adds `include.path` to `SUPERPROJECT_REFUSED`. That falsifies "its other keys are not judged", yet it escapes no control on either Git (0 of 102): the include and work-tree control's refusal gains a key sorted after the planted ones.
  - At this head every refusal does name exactly its keys, and over-refusal fails closed.
  - An equality comparison for the configuration controls would make the stated property a checked one.
- **R585-14-S2 (retained) - Tests** - No standing control fails when `GIT_NO_LAZY_FETCH` or `core.fsmonitor=false` alone is removed. Mutants `no_git_no_lazy_fetch` and `no_helper_core_fsmonitor_false` give 0 escapes on both Gits. Both are stated as defence in depth.
- **R585-14-S3 (retained) - Robustness** - `ctrl_build.py:558-560`. An unparsable stack configuration is reported as "is not its own checkout". It fails closed.
- **R584-13-S1 (retained) - Robustness, Docs** - `STACK_CONFIG` holds what Git writes on Linux. `core.ignorecase`, `core.precomposeunicode` and `core.symlinks`, which Git writes on other file systems, are refused, failing closed.
- **R585-13-S1 (retained) - Tests** - No standing control forges the root tree. The head refuses it (`store_probe` `forged_root`, `receipts/prior/store_probe.head.*.txt`).
- **R585-13-S3 (retained) - Docs** - `ctrl_build.py:472` says "cannot read the pinned tree" for a commit read too.

## Prior public findings at this head

| Finding | Status at `516a69be` | Evidence |
|---|---|---|
| R585-14-F1 (MINOR: the superproject's configuration made Git start a promisor transport while the gitlink was read, on a Git not honouring `GIT_NO_LAZY_FETCH`; texts said it was held) | RESOLVED by outcome (a): six keys refused by name before the index read. R585-14's probes give `RAN=0` on upstream 2.43.0 and `RAN=1` at `44eef11f`. Four standing controls, each ESCAPED under its mutant. Texts restated | `receipts/prior/r585_14_*`, `receipts/mutants/*superproject*` |
| R585-14-RES-1 = R584-13-RES-1 (stale link) | APPLIED: the five links name `516a69be…` | live PR body, `## Authoritative references` |
| R584-13-RES-2 (CVE releases) | APPLIED | live PR body, round-15 row 2 |
| R585-14-S1, S2, S3; R584-13-S1 | RETAINED SUGGESTIONS (above) | mutants; source |
| R584-12-F1 = R585-13-F1 (promisor transport in the stack's configuration) | Still RESOLVED: `store_probe` lazy cases `RAN=0` on both Gits | `receipts/prior/store_probe.*` |
| R584-11-F1 = R585-12-F1 (forged `src/` tree accepted) | Still RESOLVED | `receipts/prior/forge_probe.*`; mutant `no_object_hash_check` |
| R585-12-S1 (superproject `core.fsmonitor`), R585-12-S2 (alternates with `--reference`) | Still RESOLVED. S1's control is now refused by key. S2: `ctrl_pin_env.py:151` unlinks `objects/info/alternates` (read; not re-executed with `--reference`) | the superproject `core.fsmonitor` control; source |
| R585-12-RS1 to RS4, R584-11-RES-1, R584-12-RES-1 = R585-13-RES-1 | Still APPLIED (superseded by the current links) | live PR body |
| R585-13-S1, R585-13-S3 | RETAINED SUGGESTIONS (above) | source |
| R584-11-S1, R584-9-S1, R585-2-S2 | RETAINED SUGGESTIONS, carried; this delta does not touch them | as tabled by R584-13 |
| R584-8-RES-1 and the other carried residue for #495 | RETAINED; not re-verified one by one | as tabled by R584-13 |
| R584-10-F1 | Still RESOLVED by the round-12 ruling; the threat-model texts are kept (`ctrl_pin.py:45-70`, `README.md:198-202`) | source |

## Per-lens results

[R585] PASS Conformance - `ctrl_build.py:182-217,406-573`; `ctrl_pin_store.py:154-419`; the live PR body (Status, Round 14 to 16, Known limitations, Authoritative references); `receipts/prior/*`; `receipts/git_versions_and_lazy_fetch.txt` - Issue #697's acceptance 1 to 5 is untouched by this delta: the tsn-c-stack pin is still `405dc683`, lwSRP equals the base, and no image input changed. Each item of the round-14, round-15 and round-16 assignments is met as specified (table above). The round-12 scope ruling is applied: no finding here needs adversarial code inside the proof's modules. The recorded `GIT_NO_LAZY_FETCH` versions agree with upstream source and measurement.

[R585] PASS RTL - `receipts/delta_scope_and_gitlinks.txt` (six files under `sw/firmware/ctrl`; no HDL, SystemVerilog, testbench, synthesis input, Makefile, workflow or gitlink change); `ctrl_build.py:420-429,548-573,598-610` (the contracts `stack_gitlink(root) -> oid | Refusal`, `stack_pin(stack, pin=None) -> head | Refusal` and CLI exit 0/2 are unchanged) - No clock, reset, CDC, width or hardware interface is touched. The tree parser sizes ids by the pin's length and pads modes as `on_disk` does. The clean clone and the CI emulation are accepted at `405dc683…`, so the parse gives the same tree as Git.

[R585] PASS Robustness - `ctrl_build.py:466-545`; `receipts/superproject_probe.*` (11 states × 2 Gits); `receipts/ci_checkout_*`; `receipts/prior/*` (20 store, 4 forge and 4 superproject probe states × 2 Gits) - Each state either fails closed, by name and with `RAN=0`, or is accepted where it should be. The states probed:
- forged root, deep, commit, alternates-served, corrupt, truncated and missing objects;
- the six superproject keys in mixed case, legacy syntax, `includeIf gitdir/onbranch` and worktree scope;
- 24 other keys (15 of them naming a program or an `ext::` transport, the rest hooks, maintenance and index triggers) plus a filter attribute, in plain and sparse superprojects, with the tree missing or present: no program ran, and the read either succeeded or was refused for the missing tree;
- the CI checkout shape (shallow, token header) on both Gits.
Retained optional items: S3 and R584-13-S1, both fail-closed.

[R585] PASS Tests - `ctrl_pin_store.py:295-419`, `ctrl_pin.py:985-996`, `ctrl_pin_env.py:136-200`; `receipts/pin_controls.*` (102 × 3 configurations); `receipts/mutants_summary.txt` (12 mutants × 2 Gits); `receipts/figures_head.txt` - Every new mechanism has a control that fails under its mutant: the hash check (2), subtree walking (30), the stack allowlist and its order (14 and 4 on 2.56.0; on 2.43.0 the run fails, the recorder having run), the superproject check and its order (4; 2 on 2.43.0), a dropped key (1) and the worktree scope (1). The over-refusal of a stack key is caught (11). The census finds 0, and the figure check is 0 findings with 4 of 4 controls. Retained optional items: S1 (over-refusal of a superproject key is not caught, fail-closed) and S2 (defence-in-depth layers).

[R585] PASS Docs - `sw/firmware/ctrl/README.md:165-262`, `ctrl_build.py:179-217` comments and the docstrings at `:406-573`, `ctrl_pin_store.py:1-65`, `ctrl_pin.py:24-70,107-137`, the live PR body; `receipts/docs_gates_head.txt` - The texts agree with the code and with my receipts on what is held for both configurations. Figures are 102 overall and 23 in `ctrl_pin_store.py` (4 + 5 + 13 + 1), each matching the code. The docs gates pass:
- `check_em_dash --base c20c85bd`: 0 findings over 431 added lines;
- `docs_check`: 0;
- `check_doc_style`, `check_doc_paths`, `gen_toc --check`, `DOC_MAP --check`, the submodule diagram and docs checks: OK;
- `check_py_idiom`: holds.
RES-1 and RES-2 are wording only and go to the residue checklist.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #697 acceptance 1-5; round-12 to round-16 rulings and assignments; `ctrl_build.py:182-573`; live PR body; prior probes; upstream Git tags and Ubuntu packages | R585-15 | 516a69be9afba02670e37874294bd1f45ccb9316 |
| RTL | CLEAN | delta file scope and the six gitlinks; `ctrl_build.py` contracts of `stack_gitlink`, `stack_pin`, `main` and their callers | R585-15 | 516a69be9afba02670e37874294bd1f45ccb9316 |
| Robustness | CLEAN | `ctrl_build.py:466-545`; 11 own superproject states and the CI-checkout shape × 2 Gits; prior store/forge/superproject probes × 2 Gits | R585-15 | 516a69be9afba02670e37874294bd1f45ccb9316 |
| Tests | CLEAN | `ctrl_pin_store.py`, `ctrl_pin_env.py`, `ctrl_pin.py:914-1000`; 102 pin controls × 3 configurations; 12 mutants × 2 Gits; census; figure check | R585-15 | 516a69be9afba02670e37874294bd1f45ccb9316 |
| Docs | CLEAN | `sw/firmware/ctrl/README.md:165-262`; `ctrl_build.py`, `ctrl_pin.py`, `ctrl_pin_store.py` texts; live PR body; 9 docs gates | R585-15 | 516a69be9afba02670e37874294bd1f45ccb9316 |

## Real limits

- **No manager source bank** runs at this exact head, and none is claimed. Source-head execution evidence beyond my focused runs is the author's published round-16 receipts: `firmware-boundary` 696 s, `firmware-verilator` 495 s, `firmware-unit` 2074 s, and 35 of 35 images. I did not re-run them.
- **Not run here:**
  - the full `ctrl_boundary.py --selftest` build matrix, `firmware-unit`, the mutation campaigns and the coverage gate;
  - the 17-entry-point matrix (the pin controls cover the MAAP differential's two modes, the three AECP tools and the bench targets);
  - image builds: no image input changed, and the 35-image identity rests on the author's receipt.
- **Hosted CI:** none ran. GitHub Actions had 0 runs and 0 check runs at this head, at `44eef11f` and at `a8fe548a` at 2026-10-12T09:01Z (`receipts/hosted_runs_at_head.txt`). So the stack allowlist and the superproject check (rounds 15 and 16) have never run on a hosted runner. My CI-checkout emulation (local file origin, dummy token) is the closest local evidence.
- **Git and Python versions:**
  - Run here: Git 2.56.0 (host) and upstream Git 2.43.0, built from the kernel.org tarball verified against `sha256sums.asc` (`scripts/build_git_2_43_0.sh`).
  - Ubuntu's patched 2.43.0 and the runner's 2.55 were not executed; Ubuntu's binaries were only inspected for the variable's name.
  - CPython 3.14.7, and 3.12.13 in a disposable environment with `pyyaml` (not the runner's 3.12.3). Without `pyyaml`, the AECP wire control fails for want of the module (environment, not head).
- **Mutant runs on upstream 2.43.0:** `no_stack_allowlist` and `stack_allowlist_after_object_reads` end in a harness failure (rc 1) after Git ran the recorder and fetched lazily from the clone. They are counted as caught, not as clean ESCAPED lists. Their two receipts are trimmed for size, and the untrimmed hashes are stated inside them.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **Checkout integrity:** the review clone is untouched (`receipts/checkout_integrity.txt`):
  - HEAD `516a69be`, tree `544d7611`;
  - status, index and worktree equal to HEAD; `ls-files -s` equals `ls-tree -r`;
  - the six gitlinks as recorded.
  All probes ran in disposable copies under `scratch/`, which also stayed at the head.

## Pending manager duties

- R585-15-RES-1 and RES-2 go to the residue checklist. The carried residue goes to #495.
- Hosted exact-head `rtl-fast` (with `firmware-boundary` and `firmware-verilator`), `verilator-suites` and `yosys-portability`, and the act replica, once the head is pushed and final. These are the first hosted runs of the round-15 and round-16 checks.
- The current-dev merge candidate (source base `c20c85bd`, live dev `c6bd08c6`). The author reports a conflict only in the generated submodule diagram. Validate it with the builder and native banks at the merge turn.

## Receipts and scripts

Every published file is listed in `MANIFEST.sha256`, with paths relative to this packet.
- `scripts/` holds this round's portable scripts. Each takes its trees and work directory as arguments.
- `receipts/prior/` holds the outputs of the prior reviewers' scripts, run unchanged and fetched by blob id from `55acac86:review-evidence/697c-r1/reviews/`:
  - R584-12 `store_probe.py` `040fa985`;
  - R585-12 `forge_probe.py` `8365fc8a`;
  - R585-14 `r585_14_superproject_sparse_gitlink_serve.sh` `e71e9190`, `r585_14_superproject_sparse_gitlink.sh` `d1510300`, `r585_14_superproject.sh` `2d67468f` and `r585_14_superproject_sparse.sh` `29f80acf`.

R585-15 FINISHED
