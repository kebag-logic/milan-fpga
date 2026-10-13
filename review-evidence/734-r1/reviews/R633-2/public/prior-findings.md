https://github.com/kebag-logic/milan-fpga/pull/735#issuecomment-6151873947
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
