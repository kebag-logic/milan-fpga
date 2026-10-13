[R632] POSITIVE - exact head 7c862ad980dfe829ef4d85ff8f4fb4fab451984f

# R632-5 internal independent review: issue #734 / PR #735, merge of dev `0136de16`

Round R632-5. Cleared-context internal review of exact head `7c862ad980dfe829ef4d85ff8f4fb4fab451984f`, tree `622e79ae2a21917a49426c675d417307104112a1`. The head is a two-parent merge: `59354ffe75697e17a16fd117d9ba853e104394bc` (the lane; R632-4 and R633-4 POSITIVE) and dev `0136de16291a127e0a34627c77ac09cd41efc08b` (PR #705, 697c). Live `dev` and the published PR head were re-read during the review and still equal those two commits.

This is a delta review of the merge alone, as the round-5 scope comment (issue #734, comment 6154792285) assigns. All five lenses were applied. No BLOCKER, MAJOR or MINOR is open. One wording RESIDUE (in the PR body; same class as a retained prior residue) and one retained optional SUGGESTION remain. This is a source-review verdict. It is not merge authorization, a manager source bank, the current-dev candidate validation, or hosted/act acceptance.

## Reconstruction

Read in order: `AGENTS.md`, `CONTRIBUTING.md` (one-line commits, no trailers), issue #734 body and acceptance, the assignment and round comments (6151273761 through 6154792285), the author's Round 5 REVIEW READY (6154957125), and the live PR body. Then I ran `git diff a0f39ad4..7c862ad9` and the merge history, plus public evidence at `ff22678d:review-evidence/734-r1/author-r5/`: `r5-workflow.{json,log}`, `r5-merge-tree.json`, `r5-image-hashes.json` and `r5-events-final.*`. I read prior review findings only after my own pass over the merge.

Frozen round-5 scope: merge dev `0136de16` with a merge commit, keeping both sides. That means 697c's `TRUSTED_SUBMODULES` entry and its selftest manifest count, and this PR's live-base scope replay, sibling-import-free selftest and flat-install check. Both documentation texts are kept, and each conflict is listed with its resolution. Validation covers both runner selftest forms, `ci_scope --selftest`, the runner contract and CI-events gates, REV/REV+E/B16, and the five images byte-identical.

## Conflict disposition (independently replayed)

`git merge-tree --write-tree --messages 59354ffe 0136de16` (git 2.56.0, `receipts/merge-tree-replay.txt`) reproduces the merge. It finds exactly **one** content conflict, in `scripts/ci_events.py`. Its automatic result differs from the committed tree only in that file's six marker lines (`receipts/ci_events-conflict-vs-resolution.diff`).

| File | Conflict? | Resolution at `7c862ad9` | Both sides kept? |
|---|---|---|---|
| `scripts/ci_events.py:598-600` (`INHERITED_STEP_ENV`) | yes, content | `(RTL_FAST,"changes")` keeps the lane's `EVENT_NAME, PR_BASE_REF, PR_HEAD_SHA, PUSH_BEFORE_SHA`. `(RTL_FAST,"rtl-fast")` keeps dev's added `FIRMWARE_BOUNDARY_RESULT` and `FIRMWARE_VERILATOR_RESULT` alongside the lane's unchanged list. | yes |
| `scripts/act_ci.py` | no (auto-merged) | `TRUSTED_SUBMODULES` six entries incl. `third_party/tsn-c-stack` (`act_ci.py:228-260`). Selftest "exactly the six approved entries" (`:13261`) and `selftest_stack_manifest` (`:13388`) sit beside the lane's live-base replay, inline histories and flat-install launcher. | yes |
| `docs/testing/CI_WORKFLOWS.md` | no (auto-merged) | dev's stack-boundary jobs, "matching six" gitlinks and "five allowlisted" pins (`:1797-1807`) sit beside the lane's live-base scope rule (`:227-278`), runner text (`:1608-1626`) and flat-install text (`:1669-1674`). | yes |
| `.github/workflows/rtl-fast.yml`, `rtl.yml`, `scripts/ci_scope.py` | no (auto-merged) | dev's `tsn-c-stack` fetches, two boundary jobs and aggregate inputs sit beside the lane's scope-step and decision-step changes. | yes |

**Patch identity** (`receipts/patch-identity.txt`, `receipts/dev-patch-identity.txt`), with index lines and hunk offsets stripped:

- The lane's own patch `a0f39ad4..59354ffe` and the head's patch over dev `0136de16..7c862ad9` differ only in two **context** lines of the conflicted hunk.
- dev's patch `a0f39ad4..0136de16` and the merge's first-parent diff `59354ffe..7c862ad9` differ only in one **context** line of the same hunk.

So neither side lost or gained a single added or removed line.

**Product inputs** (`receipts/product-delta-vs-dev.txt`): head differs from dev only in the lane's ten CI/doc files. All six gitlinks and the `.gitmodules` blob (`32be05aa`) equal dev's. `.gitmodules` matches the six trusted entries byte for byte (`receipts/trusted-manifest-vs-gitmodules.txt`), which is what the act replay refused at `59354ffe`.

The merge commit is one line with no trailers (`git cat-file -p 7c862ad9`), as CONTRIBUTING requires.

## Execution evidence (my runs, exact head, CPython 3.12.3 venv, PyYAML 6.0.3)

| Gate | Result | Receipt |
|---|---|---|
| `ci_scope.py --selftest` | rc 0, 198 assertions, PASS; includes the history kills and `['third_party/tsn-c-stack']: rtl=True` | `receipts/gates-7c862ad9/ci-scope-selftest.log` |
| `ci_events.py --check` | rc 0, 2174 contract items | `.../ci-events-check.log` |
| `ci_events.py --selftest` | rc 0, 2174 items, 3096 arms; `firmware-boundary` RV32 and script arms caught | `.../ci-events-selftest.log` |
| docs check and selftest, doc paths, doc style, TOC check and anchors, em-dash vs `0136de16`, Python and shell idiom, source lists, evidence readers | all rc 0 | `receipts/gates-7c862ad9/SUMMARY.tsv` |
| Five linked images at `59354ffe`, `0136de16` and `7c862ad9` (each built from its own commit with submodules at their gitlinks) | all three builds rc 0. All five shapes byte-identical across all three commits, and equal to the author's `r5-image-hashes.json` | `receipts/images/image-hashes-three-commits.tsv` |
| Scope steps and classifier, `59354ffe` vs `7c862ad9` | the `changes`, `elaborate` and `full-ci-gate` jobs' `if`/`needs`/`outputs`/`steps` are identical. `ci_scope.py` differs only by dev's docstring sentence and two `_cases` rows. `ci_scope_history.py` is identical. | `receipts/scope-steps-59354ffe-vs-7c862ad9.tsv`, `receipts/ci_scope-merge-delta.diff` |
| B16 (`49da9fd9`/`f1b2489f`) with the classifier at both commits | two-argument diff (65 paths under `--no-renames`; 64 with rename detection, the issue's figure): relevant at both. Merge-base diff (2 docs paths): docs-only at both. `third_party/tsn-c-stack` and `.gitmodules` are relevant at both. | `receipts/b16-and-path-classification.tsv` |

**Conflict-resolution mutation probes** (`scripts/probe_conflict_resolution.sh`, `receipts/conflict-probes/`). Each probe is a fresh archive of the head, judged by `ci_events.py --check`.

| Probe | Expected | Result |
|---|---|---|
| control (unchanged) | pass | rc 0 |
| take dev's `changes` env (`PR_BASE_SHA`) | refuse | rc 1: `PR_BASE_REF`, `PR_HEAD_SHA` outside allowlist |
| drop `PR_HEAD_SHA` from `changes` env | refuse | rc 1 |
| take the lane's aggregate env (no `FIRMWARE_BOUNDARY_RESULT`) | refuse | rc 1 |
| drop `FIRMWARE_VERILATOR_RESULT` | refuse | rc 1 |
| git's unresolved conflict text | refuse | rc 1 (SyntaxError at `:598`) |

Among the alternatives a careless resolution could produce, the committed one is the only one that passes. The gate holds it against both workflow bindings (`receipts/rtl-fast-bindings.txt`).

**Runner selftest (`act_ci.py`).** Under this round's rules I did not execute the candidate runner on the host. Exact-head evidence is in two places, and they agree:

- **Hosted `docs-check`, job 115533867546, success.** It ran on synthetic merge `dd320296`, whose first parent `0136de16` is an ancestor of the head, so its tree is the head's. Both forms passed: `python3 scripts/act_ci.py --selftest`, then `install -m 0555` into `mktemp -d` and `python3 -I … --selftest --worktree "$GITHUB_WORKSPACE"`. The ordinary form had 570 `ok` and the flat form 568. Both include "exactly the six approved entries", the five-pin materialization, and all four `tsn-c-stack` refusal controls (`receipts/hosted/docs-check-115533867546.log:6260-7431`, `receipts/hosted/docs-check-runner-counts.txt`).
- **The author's `r5-workflow.log`.** Its sha256 `b09e9f21…` matches its JSON, and it shows the same 570/568 split and the same lines.

**Hosted scope at the merged head** (`receipts/hosted/changes-115533868023.log`). The `changes` job ran the lane's scope body with `PR_BASE_REF: dev` and `PR_HEAD_SHA: 7c862ad9`, and diffed `GITHUB_SHA^1`→`GITHUB_SHA`. It listed exactly the ten lane files and answered `RTL/tooling relevant: true`. This matches my `git diff --name-status 0136de16 7c862ad9`.

Hosted snapshot at 21:21Z (`receipts/hosted-check-runs-7c862ad9.tsv`):

- `rtl-fast` success, including `firmware-boundary` and `firmware-verilator`; `elaborate` success; `docs-check` success; Yosys shards success.
- Verilator shards 0-4 were still in progress.
- `Physical gPTP` is a skipped context, not an executed one.

## Findings

### R632-5-R1 RESIDUE - Docs - PR body Status still calls the published merge local
- **Artifact:** live PR #735 body, Status section (`receipts/pr735-body-at-review.md:22`): "The merge commit remains local; publication is pending."
- **Evidence:** the PR's `headRefOid` is `7c862ad9…`. Hosted `changes`, `docs-check`, `rtl-fast` and `elaborate` executed at it. This is the same class as retained R632-4-R1 / R633-2-D1, and it is pure PR-body wording: it changes no measurement, figure, verdict, test, code or claim.
- **Impact:** a cold reader is told the head under review is unpublished.
- **Exact fix:** replace that sentence with "The merge commit is published as the PR head `7c862ad9`."
- **Verification:** the live body no longer says the round-5 merge is local or pending publication.

### S1 SUGGESTION (retained R632-2-S2 / R632-3-S1) - Robustness - hosted branch does not assert the merge shape
The hosted scope branch diffs `"$GITHUB_SHA^1" "$GITHUB_SHA"` without asserting that `GITHUB_SHA` is the two-parent synthetic merge. The merge did not change this (`receipts/scope-steps-59354ffe-vs-7c862ad9.tsv`: `changes.steps` identical). This is optional and carries no coverage weight.

No other finding. I specifically checked for:
- stale counts after the merge: "four allowlisted", "matching five", "five approved" and "all four firmware jobs" all have zero stale hits;
- interaction between the lane's live-base scope and dev's two new scope-gated jobs: both gate on `needs.changes.outputs.rtl`, and `CI_WORKFLOWS.md:163-164` lists them as docs-only skips;
- dev's stack-manifest selftest under the lane's isolated flat install: passes, 568 hosted;
- dev's `ci_scope.py` row change: `adp.c` to `adp_mbx.c` is still relevant under the suffix-agnostic `sw/firmware/` rule.

## Prior public findings at this head

The lane's own patch is unchanged by the merge apart from context lines (see patch identity), so each resolution below still stands at `7c862ad9`. Each was re-checked against current bytes or receipts.

| Prior finding | Severity | Status at `7c862ad9` | Evidence |
|---|---|---|---|
| R632-1-F1 (REV/REV+E docs-only) | BLOCKER | RESOLVED, retained resolved | Scope steps identical to `59354ffe`. `ci_scope --selftest` REV/REV+E/B16 history rows pass. B16 receipt. |
| R632-1-F2 / R633-1-D1 (bindings in prose) | MINOR / RESIDUE | RESOLVED | `ci_events --check` rc 0. The conflict probes prove the `PR_BASE_REF`/`PR_HEAD_SHA` bindings are held. |
| R632-1-F3 / R632-2-S1 (history wiring) | SUGGESTION | RESOLVED | Runner contract passes in both forms at the hosted exact head. |
| R633-2-F1 (flat isolated install) | MAJOR | RESOLVED | Hosted flat form 568 ok at exact head. |
| R632-2-F1 (ambient Git in fixtures) | MINOR | RESOLVED | `ci_scope_history.py` byte-identical to `59354ffe`. Fixture-isolation `ok` lines present in hosted runner log. |
| R632-2-F2 (replay vs hosted set) | MINOR | RESOLVED | Hosted `changes` lists exactly the merge-base set. Rename and identical-on-dev history rows pass in `ci_scope --selftest`. |
| R632-2-R1, R632-3-R1 | RESIDUE | RESOLVED | `CI_WORKFLOWS.md:288-293` and `TESTING.md:1417-1418` unchanged by the merge. |
| R632-3-F1 (sibling-import control) | MINOR | RESOLVED | `docs.yml:389-395` unchanged, and run hosted at exact head. |
| R632-3-R2 / R633-3-R1 (duplicate `Closes #734`) | RESIDUE | **RESOLVED** | The live body has exactly one `Closes #734`. |
| R632-4-R1 / R633-2-D1 (stale "local" status wording) | RESIDUE | **RETAINED** as R632-5-R1 | See above. |
| R632-2-S2 / R632-3-S1 (merge-shape guard) | SUGGESTION | RETAINED as S1 | See above. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #734 acceptance 1-5 and the round-5 scope comment checked against the merge. Merge-tree replay (one conflict). Both-sides patch identity. `act_ci.py:228-260,13261,13388`. `.gitmodules` = trusted manifest. Hosted `changes` log (live-base scope, ten paths, relevant). B16 classification. Hosted runner contract 570/568. | R632-5 | `7c862ad980dfe829ef4d85ff8f4fb4fab451984f` |
| RTL | CLEAN | No `hdl/` path in either merge diff. Gitlinks and `.gitmodules` equal dev. Five linked images byte-identical across `59354ffe`, `0136de16` and `7c862ad9`. CI job-graph contract: `rtl-fast.yml` aggregate needs and env (`:614-630`), scope step bindings (`:39-52`), `ci_events --check`. | R632-5 | `7c862ad980dfe829ef4d85ff8f4fb4fab451984f` |
| Robustness | CLEAN (S1 optional) | Conflict-resolution mutations (5 refusals + control). Unresolved-marker refusal. Stack-manifest refusal controls (drop, redirect, drop gitlink, add gitlink) in both runner forms, hosted. Scope fail-safe rows in `ci_scope --selftest`. | R632-5 | `7c862ad980dfe829ef4d85ff8f4fb4fab451984f` |
| Tests | CLEAN | `ci_scope --selftest` (198). `ci_events --selftest` (3096 arms). Docs and idiom gates. Probe kill table showing the CI-events gate detects every wrong resolution. Hosted runner selftests. Image rebuilds at three commits. | R632-5 | `7c862ad980dfe829ef4d85ff8f4fb4fab451984f` |
| Docs | CLEAN (RESIDUE R632-5-R1 carried) | `CI_WORKFLOWS.md:56-170,227-293,1608-1626,1669-1674,1797-1807,2706-2710`. `TESTING.md:1414-1421`. `ci_scope.py` docstring. Stale-count grep. Live PR body (one `Closes #734`; stale Status sentence). Docs gates rc 0. | R632-5 | `7c862ad980dfe829ef4d85ff8f4fb4fab451984f` |

## Real limits

- **Runner selftest:** I did not run `act_ci.py --selftest`, act or Docker on the host. The runner selftest evidence is hosted job 115533867546 and the author's receipt.
- **Interpreter:** my gates used a CPython 3.12.3 venv; host Git is 2.56.0 and the hosted runner's is 2.55.0.
- **Not run:** no full parent, protocol-processor, gPTP, Yosys or builder banks, and no Verilator suites.
- **Image comparison:** limited to the five linked ELF images built by `ctrl_image.py`. This is a desk measurement. No physical calibration ran, and field skips are not hardware proof.
- **Hosted coverage:** the Verilator shards were still in progress at the snapshot.
- **Act replay:** no act replay receipt at `7c862ad9` was published when this report was written, so none was read.

## Pending manager duties

- Trusted act replay of `7c862ad9`, now expected to pass the `tsn-c-stack` manifest check, and its receipts.
- Hosted acceptance once the Verilator shards complete.
- The current-dev merge candidate's builder and native banks at the merge turn, and the 696 sequencing condition.
- Carry R632-5-R1 to the residue checklist.
- Merge only with explicit maintainer authorization and the full completion bar.

Clone restored and verified: HEAD and index tree equal `622e79ae`, and `ls-files -s` equals `ls-tree -r HEAD` (modes and blobs). The worktree is clean with no untracked files, gitlinks are unchanged, and submodule worktrees are clean (`receipts/clone-state-final.txt`).

R632-5 FINISHED
