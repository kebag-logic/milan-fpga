[R632] NEGATIVE - exact head 0519ff3684258482a56892056edbfbb65c186f88

# R632-1 internal independent review: issue #734 / PR #735

- Head: `0519ff3684258482a56892056edbfbb65c186f88`, tree `a7777345d841a565687c667bee6d53e0f5a734b8`, parent/source base `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (including lines 698-703 on the frozen `pull_request.base.sha`), issue #734 body and its assignment/TAKEN/REVIEW READY comments, the PR #735 body, `git diff a0f39ad4..0519ff36` (8 files, +289/-29), and the author evidence tree at `a7ca711b:review-evidence/734-r1`.
- Prior public review findings on PR #735: none. The only PR comments are the two review-start notices, so nothing needed resolving or retaining.
- All five lenses were applied. Verdict: NEGATIVE, because of one BLOCKER (F1) and one MINOR (F2).

## Findings

### F1 BLOCKER - Conformance, RTL, Robustness, Tests, Docs - a PR's own RTL change is classified docs-only once the lane has merged a newer base

- **Location**:
  - `.github/workflows/rtl.yml:117`
  - `.github/workflows/rtl-fast.yml:57`
  - `.github/workflows/elaborate.yml:106`
  - The canonical forms pinned in `scripts/ci_events.py`.
  - The fixture `scripts/ci_scope_history.py:36-64`.
  - The claims in `docs/testing/CI_WORKFLOWS.md:168-181` and the `scripts/act_ci.py:2378-2388` docstring.
- **Authority and evidence**:
  - The rule being checked: issue #734 acceptance 3 says "an RTL change on an older base is classified relevant", and `CI_WORKFLOWS.md:179` says "RTL changes and submodule pointers remain relevant". The assignment adds that any path letting a PR's own RTL change be classified docs-only is a BLOCKER.
  - The premise, in the repository's own words: `CONTRIBUTING.md:698-703` says GitHub freezes `pull_request.base.sha` when the PR opens, while the job builds the merge into the current base tip. Lanes routinely merge `dev` into their branches, often resolving conflicts by hand: `8ab2b5399`, `941e15593`, `8c3e892c2`, `da341a154`, `26370439b` and others in `git log --merges`.
  - The mechanism: once a lane has merged a `dev` commit newer than its recorded base, `merge-base(recorded, head)` is the recorded base itself. `<recorded>...<head>` then degenerates into the two-tree comparison from the frozen base. A head file that has been restored to the recorded base's content is invisible to it. That covers a conflict resolution that keeps the lane's side over `dev`'s RTL edit, and a plain revert.
- **Reproduction**: `scripts/probe_scope.py`, receipt `receipts/probe_scope.jsonl`. The probe extracts the three shipping step bodies with PyYAML and executes them.
  - **Case REV**: the lane opens at R, `dev` commit D edits `hdl/x.sv`, the lane merges D and restores `hdl/x.sv`, and a docs edit is added.
    - The composition (synthetic merge vs live base) changes `["docs/a.md", "hdl/x.sv"]`.
    - All three head bodies report changed=`["docs/a.md"]`, `rtl=false`.
  - **Case REV+E**: the same, plus a later unrelated `dev` RTL commit E.
    - The head bodies still give `rtl=false`.
    - The parent bodies give `rtl=true` (`["docs/a.md", "hdl/y.sv"]`).
    - So in the normal busy-`dev` case this is a regression introduced by the change. B16 itself had 34 paths against its landed merge.
  - Taking the merge base against the live base the hosted merge used lists `hdl/x.sv` in both cases. It still yields B16's two docs paths (`receipts/b16-live-base-three-dot.txt`). The new self-test's history (`ci_scope_history.history`) only forks PRs from a common ancestor and never merges a newer base, so no control covers this shape.
- **Impact**:
  - A PR whose merge reverts or alters RTL is reported docs-only.
  - The `rtl.yml` exhaustive workers and both required aggregates skip, as do the `rtl-fast` consumers and the `elaborate` gates.
  - The act replay agrees with hosted by construction, so local evidence is blind to it too.
  - The AGENTS.md section 7 bar of "exact-head `verilator-suites` and `yosys-portability` evidence" for an RTL-relevant head is silently never triggered.
  - The only remaining check is the merge-turn candidate bank. The issue's stated safety argument (interactions with intervening base changes) does not cover a PR's own RTL change.
- **Required outcome**:
  - The scope list contains every path the PR head contributes to the composition. That includes lanes that have merged a base newer than the recorded oid.
  - Hosted/replay equality is kept.
  - A history control (newer base merged, RTL file restored, docs otherwise) is classified relevant in all three bodies and fails when the rule is removed.
  - `CI_WORKFLOWS.md` and the `build_event` docstring state the rule exactly.
  - If the frozen issue wording is read as requiring the recorded base specifically, publish that as a conflict for a decision rather than choosing privately.
- **Verification**: re-run `scripts/probe_scope.py`. REV and REV+E must give `rtl=true` in all three bodies, B16 must stay at two docs paths with `rtl=false`, and a mutation removing the new rule must be rejected by `ci_scope.py --selftest`.

### F2 MINOR - Docs - the authoritative contract description still lists the pre-change env bindings

- **Location**: `docs/testing/CI_WORKFLOWS.md:650-651`, `:662-665` and `:863-864`.
- **Evidence**: `scripts/ci_events.py` now pins `PR_HEAD_SHA: ${{ github.event.pull_request.head.sha }}` on the decision step (`DECIDE_STEP_ENV`), the fast scope step and the elaborate scope step. Mutating it is refused (`receipts/mutations/*-head-bound-github-sha.events.log`). The policy page still says:
  - item 5 (`:650`): the decision step's `env` "is exactly `EVENT_NAME`, `PR_DRAFT` and `PR_BASE_SHA`";
  - item 6 (`:662-665`): the binding list omits `PR_HEAD_SHA`;
  - the carrier section (`:863-864`): elaborate's scope step has "its two env bindings pinned", when it now has three.
- **Impact**:
  - The page's statement of what the contract gate enforces is false.
  - The new binding's reason for existing is missing from the binding rationale. Rebinding it to `github.sha` reintroduces synthetic-merge scope.
  - The PR's "No undocumented requirement or interface change remains" box is ticked.
  - Severity is MINOR, not RESIDUE, because the defect is a false statement of an enforced contract.
- **Required outcome**: all three passages name `PR_HEAD_SHA` and its source expression, with the count corrected.
- **Verification**: grep the three passages, then run `gen_toc --check` and `ci_events --check`.

### F3 SUGGESTION - Tests - the executed-history self-test's own wiring is unguarded

- **Location**: `scripts/ci_scope.py:521-524`.
- **Evidence**: the `scope-history-unwired` mutation (`failures += history_selftest(ROOT)` → `failures += 0`) passes both `ci_scope.py --selftest` and `ci_events.py --check` (`receipts/mutations/`).
- **Impact**: the canonical step scripts stay pinned by `ci_events`, so the rule itself survives. But the claim at `CI_WORKFLOWS.md:183` ("The scope self-test executes each workflow's actual shell body") could become false silently.
- **Optional**: have a gate require the history arms' presence or count.

### Note: criss-cross histories

`git diff A...B` with two merge bases silently uses one (probe XX: rc 0, no warning). This is recorded as a residual edge for whoever resolves F1. It is not a separate finding.

## Checks performed (all at the exact head unless noted)

**Gates** (`receipts/*.log` and `*.rc`, all rc 0):
- `ci_scope.py --selftest`: PASS, 133 log lines, including 28 scope-history assertions.
- `ci_events.py --check`: OK, 2021 contract items.
- `ci_events.py --selftest`: PASS, 2834 arms.
- `docs_check.py`, plus its selftest.
- `check_doc_paths.py`.
- `gen_toc.py --check`, `--verify-anchors` and `--selftest`.
- `check_em_dash.py --base a0f39ad4`, plus its selftest.
- `check_doc_style.py`.
- `check_py_idiom.py`, plus its selftest.
- `pp_srcs.py --check` and `--selftest`.
- `measure_test_evidence.py --check` and `--selftest`.

The Markdown gates used the hash-pinned renderer from `tools/markdown/requirements.txt`, installed in a private venv. The first attempt without the renderer is overwritten in `receipts/`; that run refused with rc 2 for want of the renderer and judged nothing.

**`act_ci.py --selftest` was not run on the host.** The assignment forbids it under the bootstrap rule. I reviewed `selftest_scope_event` and `build_event` statically:
- The payload carries `pr.base_sha` (recorded) and `pr.head_sha`.
- The existing arms at `scripts/act_ci.py:6198-6203` pin base = recorded and base ≠ validation base.

The author's receipt `act-selftest-final.json` reports rc 0 inside a disposable, network-less container. That is author evidence, not mine.

**B16 reproduction** (`probe_scope.jsonl`, case B16):
- Two-dot counts: 65 with `--no-renames`, 64 with default rename detection, matching the issue's table.
- The merge-base diff `49da9fd9...f1b2489f` gives the two `docs/findings/` paths.
- All three head bodies on the landed merge `6c810c45` output `rtl=false` with those two paths. The parent bodies output 34 paths and `rtl=true`.

**Controls** (in `ci_scope_history`, which I executed, and re-checked by 16 independent mutation arms):
- Every arm is listed in `receipts/mutations/` with the result of each gate.
- A docs-only PR on an older base is documentation-only, and an RTL change on an older base is relevant. Both hold only for PRs that never merged a newer base (see F1).
- A gitlink stays relevant, and an empty delta returns `rtl=true`.
- Each control fails when its rule is removed: `classifier-hdl-docs`, `classifier-no-gitlink` and `classifier-empty-docs` each fail the selftest.
- Endpoint-tree and merge-commit-scope forms in each workflow are rejected by both gates.
- A head bound to `github.sha` is rejected by `ci_events`.
- A shallow checkout in each workflow is rejected by `ci_events`.
- Push with a three-dot form is rejected by both gates.
- The only arm that survives is the one in F3.

**Push and non-PR behaviour**:
- On push, `rtl-fast` keeps the `"$base" "$GITHUB_SHA"` tree diff, and the history self-test covers a rewind.
- `rtl.yml` and `elaborate.yml` still force `rtl=true` for non-PR events.
- History: each scope checkout has `fetch-depth: 0` (`rtl.yml:46`, `rtl-fast.yml:33`, `elaborate.yml:75`).
- The PR head is the synthetic merge's second parent, so it is present in the checkout.

**Fail-closed paths**:
- With no merge base, `git diff A...B` exits 128 under `set -euo pipefail` (`receipts/no-merge-base.txt`), and the step fails.
- An unresolvable base falls back to `git ls-files`.

**Five linked images** (`receipts/images-elf-compare.txt`, `images-*.log`, `image-audit-controls.log`):
- Built `ctrl_image.py` for the five shapes at the parent and at the head, using the pinned Bootlin SDK. The archive sha256 `d42680e9…` matches `scripts/ci_rv32_sdk.py`.
- All five `ctrl_app.elf` files are byte-identical between parent and head. Sizes match the author's: 50752, 50752, 50744, 50768 and 50776.
- `ctrl_image_selftest.py --require-rv32` at head: 33 checks PASS.
- The absolute hashes differ from the author's because the compiler build differs, so only the parent-to-head comparison is claimed.

**Hosted at exact head** (`receipts/hosted-check-runs.txt`, inspected only):
- Completed with success: `changes`, `full-ci-gate`, `verilator-lint`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `firmware-aecp-mutants` and Yosys shards 0-3.
- Physical gPTP: skipped by design.
- Still in progress: `docs-check`, `elaborate`, Verilator shards, `yosys-elaboration` and several firmware jobs.
- None of this is acceptance; the manager owns hosted and act acceptance.

## Ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Issue #734 acceptance 1-5 against `rtl.yml:98-131`, `rtl-fast.yml:36-72`, `elaborate.yml:80-111`; B16 reproduction; REV/REV+E probe | R632-1 | 0519ff3684258482a56892056edbfbb65c186f88 |
| RTL | UNCLEAN (F1) | The scope `rtl` output contract to its gated jobs in the three workflows; fail-closed paths (no merge base, missing base, non-PR, push); `fetch-depth: 0` at `rtl.yml:46`, `rtl-fast.yml:33`, `elaborate.yml:75` | R632-1 | 0519ff3684258482a56892056edbfbb65c186f88 |
| Robustness | UNCLEAN (F1) | Merged-newer-base lane history (REV/REV+E), criss-cross (XX), unrelated history (`no-merge-base.txt`), push rewind, empty delta | R632-1 | 0519ff3684258482a56892056edbfbb65c186f88 |
| Tests | UNCLEAN (F1; F3 suggestion) | `scripts/ci_scope_history.py:1-164`, `scripts/ci_events.py:6414-6427` new arms, `scripts/act_ci.py:6207-6243`; 16 independent mutation arms (`receipts/mutations/`) | R632-1 | 0519ff3684258482a56892056edbfbb65c186f88 |
| Docs | UNCLEAN (F1, F2) | `docs/testing/CI_WORKFLOWS.md:168-188`, `:650-665`, `:862-866`, `:1512-1520`; `scripts/act_ci.py:2375-2392` docstring; PR #735 body | R632-1 | 0519ff3684258482a56892056edbfbb65c186f88 |

## Real limits

- `act_ci.py --selftest` and any act or Docker replay were not executed (forbidden). Runner contract evidence is the author's containerised receipt only.
- The frozen `pull_request.base.sha` premise of F1 rests on the repository's own statement (`CONTRIBUTING.md:698-703`, `CI_WORKFLOWS.md:1512`). I did not observe a live webhook payload.
- The F1 reproduction uses synthetic histories that execute the shipping step bodies. No live PR was run.
- Image hashes come from my local SDK build. They show parent-to-head identity, not equality with the author's absolute hashes.
- No full parent, PP, gPTP, Yosys or builder banks were run. Physical calibration was not run. Hosted results are partly still in progress.

## Pending manager duties

- Publish this report.
- Route F1 to the executor, or as a conflict to the issue for a decision, and route F2.
- Own hosted and act acceptance, the full PR act replay, and the current-dev merge-candidate builder and native banks at the merge turn.
- Enforce the merge order (697c, then 696).

## Exact-head restoration

The review clone is unmodified: `git status` is clean, HEAD is `0519ff36…` and the tree is `a7777345…`. Index gitlinks are unchanged:
- `gptp-processor` `7dda9c3b`
- `protocol-processor` `2ad2f845`
- `third_party/verilog-axis` `48ff7a7e`
- `external` `efeb541a`
- `third_party/lwSRP` `08ee86e8`

Every probe ran in disposable clones under `scratch/`.

R632-1 FINISHED
