[R732] POSITIVE - exact head 86a349d5399d8abc40b819d09806fc8245682609

Round R732-5. External review of PR #822 (#787) at head `86a349d5399d8abc40b819d09806fc8245682609`, tree `43d185333ff4048986a2080996ed5e482af3f3bc`. The previous head reviewed was `cbc7c604` (R732-4, POSITIVE).

**Verdict: POSITIVE.** Nothing open is MINOR or worse. The delta is one clean merge commit and it does not change the tree. The PR body still names the old head and the old dev tip. That is recorded below as RESIDUE (wording only), together with the carried residue and suggestions.

## What the delta is

All of these are reproduced by `scripts/delta_checks.sh` (11 of 11 PASS, `receipts/07-delta-checks.txt`) and by `receipts/01`-`05`.

- **Commits.** `git rev-list cbc7c604..86a349d5` lists exactly two commits: `86a349d5` and dev's `8adf5c99`, which is PR #826's merge commit.
- **Parents.** `86a349d5` has the parents `cbc7c604` and `8adf5c99`, in that order.
- **Tree.** `cbc7c604^{tree}` = `86a349d5^{tree}` = `43d18533`, and `git diff --stat cbc7c604 86a349d5` is empty.
- **No hand-made content.** `git merge-tree --write-tree cbc7c604 8adf5c99` returns `43d18533` with rc 0. So the recorded tree is exactly git's automatic merge, with no conflict and no change beyond it.
  - The tree is identical because both of `8adf5c99`'s parents (`02ca829a`, `4ee2aa96`) were already ancestors of `cbc7c604`.
  - `8adf5c99` is itself a clean automatic merge: merge-tree of its two parents gives `c5ae6597`, which is its own tree.
- **Merge base.** Against `cbc7c604`, `git merge-base --all 8adf5c99` gives two bases, `02ca829a` and `4ee2aa96`. Against `86a349d5` it gives one, `8adf5c99`.
- **Remote state** (`receipts/03-remote.txt`, 17:21 UTC):
  - `refs/heads/787-reboot-reset` and `refs/pull/822/head` both point at `86a349d5`.
  - Live `dev` is `8adf5c99`.
  - PR #826 is MERGED at `8adf5c99`. PR #820 is still OPEN at `81f78a81`.
- **Why the merge was needed** (`.github/workflows/rtl-fast.yml:53-54`). On the act path the workflow sets `base="$(git merge-base --all …)"` and then runs `git cat-file -e "$base^{commit}"` under `set -euo pipefail`.
  - With two bases the argument holds two lines. `cat-file` fails with rc 128 ("Not a valid object name 02ca829a…"), so the `changes` step aborts.
  - With one base it returns rc 0 (`receipts/04-classifier-probe.txt`).
  - The changed-file list the classifier computes from the merge-tree against dev is the same 70 files at both heads. So the scope decision cannot differ, only whether the step runs.
- **Commit message.** One line, 100 characters, ASCII only, no trailers, as CONTRIBUTING requires ("Commits: one line, no trailers"). It describes the commit accurately.
- **Merge candidate.** `git merge-tree --write-tree 8adf5c99 86a349d5` = `43d18533`. Because `8adf5c99` is an ancestor of the head, merging into current dev gives exactly the reviewed tree.
- **Whitespace.** `git diff --check 8adf5c99 86a349d5` gives rc 0.
- **Gitlinks.** The six are byte-identical to `cbc7c604`'s. `protocol-processor` is still at `a9e84b66`, which carries #203.
- **Comment rule.** The delta changes no file, so it adds no source comment and no new instance.

## Findings

### F1 - RESIDUE - Docs - PR #822 body, "Status" and "Linked Issue / roles" - the body predates head `86a349d5` and PR #826's merge

- **Evidence.** These statements in the body are now stale:
  - `:16` reads "**REVIEW READY** at `cbc7c6043ebf…`. `787-reboot-reset` -> `dev` (`02ca829a`)." The head is `86a349d5` and dev is `8adf5c99`.
  - `:17` reads "carries PR #826's commits … and PR #820's …, and merges after both". PR #826 has merged.
  - `:68` reads "Carries PR #826 (#814): … and merges after it."
  - The round list stops at round 6 (`cbc7c604`). There is no entry for the merge of dev `8adf5c99`.
- **Why it is only RESIDUE.**
  - The tree is identical, so every figure, gate result and route measurement in the body still describes the head's bytes.
  - The one claim tied to a base is `git diff --check` against dev. Rerun against `8adf5c99`, it still gives rc 0.
  - The public head statement exists in the manager's comment 6546588633.
  - No measurement, verdict or clause claim changes.
- **Exact fix.**
  - `:16`: replace with "**REVIEW READY** at `86a349d5399d8abc40b819d09806fc8245682609` (tree identical to `cbc7c604`). `787-reboot-reset` -> `dev` (`8adf5c99`)."
  - `:17`: replace "and PR #820's (#818, `818-wns-gate` at `81f78a81`), and merges after both." with "PR #826 merged to dev at `8adf5c99`. The PR also carries PR #820's commits (#818, `818-wns-gate` at `81f78a81`) and merges after it."
  - `:68`: replace with "Carried PR #826 (#814), which merged to dev at `8adf5c99`."
  - After the round 6 list, add: "Merge of dev `8adf5c99` (PR #826 merged): one merge commit, `86a349d5`, with parents `cbc7c604` and `8adf5c99`. Its tree is byte-identical to `cbc7c604`'s. It leaves one merge base with dev, which rtl-fast's change classifier needs."
- **Verification.** Read the body and confirm that no `cbc7c604` appears as the review-ready head, and no `02ca829a` appears as the current dev.

### Prior findings, judged at this head

The tree is byte-identical to `cbc7c604`. So every in-tree item keeps the status R732-4 recorded. I checked each at its cause, not by count.

| Prior finding | Severity; lenses | Status at `86a349d5` |
|---|---|---|
| R732-4 R1: the PR body predates the #820 merge (`:202` "that file is not part of this PR"; "Rounds 4 and 5 … Neither changes"; no "Carries PR #820" line) | RESIDUE; Docs | **Retained.** All three phrasings are still in the body, so the exact fix in R732-4 R1 still applies. It folds naturally into F1. |
| R732-4 R2: `docs/reference/SUBMODULES.md:503`, "this change" has no referent | RESIDUE; Docs | **Retained**, because the tree is unchanged. Fix: "That path lies outside #787's change." |
| R732-4 R3: `AREA_BUDGET.md:149-150` and `SUBMODULES.md:511-517` do not say where the re-pin route is recorded | RESIDUE; Docs | **Retained**, because the tree is unchanged. The fix is as R732-4 R3 states it. |
| R732-4 S1: the MultiReg note in `cdc_census.gen.py:122-123` is inaccurate, and there is no `--check` arm (R731-3 S2) | SUGGESTION; Docs, Tests | Retained (optional) |
| R732-4 S2: `SUBMODULES.md:499` lacks "Under #818 the fall prints a WARNING and passes." | SUGGESTION; Docs | Retained (optional) |
| R732-4 S3: `AREA_BUDGET.md:151` antecedent | SUGGESTION; Docs | Retained (optional) |
| R731-3 S3: LiteX aggregate member limit | SUGGESTION; Tests | Retained (optional). This is #826's harness, now on dev. |
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114`, a lane label and an issue-comment ID in a source comment | RESIDUE; Docs | **Retained** (tree unchanged; tracked under #746) |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139`, the link-down comment | RESIDUE; Docs | **Retained** (tree unchanged) |
| R732-1 S1, R731-1 S2: `hdl/milan/KL_reboot_ctrl.sv` | SUGGESTION; RTL, Robustness, Tests | Retained (optional); the tree is unchanged |
| R732-1 S2: `mutants.py` saturation control | SUGGESTION; Tests | Retained (optional) |
| R731-1 S1: the `.mac_tx_beat_i` / `.mac_flush_i` wirings | SUGGESTION; Tests, Robustness | Retained (optional) |

### S1 - SUGGESTION - Robustness, Tests - `.github/workflows/rtl-fast.yml:53-54` - a criss-cross history fails with an unexplained error

- **What happens.** With two merge bases, the `changes` step dies in `git cat-file` with "fatal: Not a valid object name …". Nothing in the log says that the history has two merge bases with dev.
  - It fails closed, which is the right direction.
  - The cause is only visible to someone who reads the shell.
- **Scope.** The file is not part of this PR, and its behaviour is not in question here.
- **Suggestion.** In a separate Issue, consider checking the line count of `$base` and printing "criss-cross history: N merge bases with origin/<base>; merge the live base first" before exiting non-zero.

## Lenses

```text
[R732] PASS Conformance - git diff --stat cbc7c604 86a349d5 (empty); tree 43d18533 at both; gitlinks equal (protocol-processor a9e84b66) - issue #787's Required list (REBOOT reset within a bound, the #396 power checks, the sim and mutant tests, the #203 pin in the same PR) is met by the same bytes R732-4 judged; the delta cannot change it
[R732] PASS RTL - git ls-tree diff of hdl/, sw/litex/ and syn/ between cbc7c604 and 86a349d5 (none); merge-tree(cbc7c604,8adf5c99)=43d18533 rc 0 - no HDL, SoC or constraint byte changes; the dev candidate merge-tree(8adf5c99,86a349d5)=43d18533, so the merged RTL is the reviewed RTL
[R732] PASS Robustness - receipts/02-merge-tree.txt, receipts/04-classifier-probe.txt; .github/workflows/rtl-fast.yml:53-54 - the merge is git's automatic merge with no conflict and nothing hand-made; the classifier's two-base failure (cat-file rc 128) reproduces, and the single-base path gives rc 0 with an identical 70-file change list
[R732] PASS Tests - scripts/delta_checks.sh -> receipts/07-delta-checks.txt (11/11 PASS); review-evidence/787-r1 at a16caad4 MANIFEST.json (1566 entries; author-r5/review-ready.md and receipts/mem.tsv match their published sha256) - no test or harness byte changes, so the author's published gate receipts for these bytes stay valid; git diff --check vs dev 8adf5c99 rc 0
[R732] PASS Docs - PR #822 body (receipt scratch copy read by section; lines 5, 16-17, 54-68, 202), the commit message of 86a349d5, and the tree's #814/#826 mentions (grep, no merge-status claims) - the commit subject is one line with no trailers and is accurate; the body staleness is wording only, recorded as F1 RESIDUE with the exact fix; the carried residue is retained
```

## Ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta (empty tree diff); gitlinks; issue #787's Required list against R732-4's judgment of the same tree | R732-5 | 86a349d5399d8abc40b819d09806fc8245682609 |
| RTL | CLEAN | `hdl/`, `sw/litex/`, `syn/` unchanged; merge-tree for the merge and for the dev candidate | R732-5 | 86a349d5399d8abc40b819d09806fc8245682609 |
| Robustness | CLEAN (S1 optional) | merge cleanliness, ancestry, `rtl-fast.yml:53-54` single- and two-base probe | R732-5 | 86a349d5399d8abc40b819d09806fc8245682609 |
| Tests | CLEAN | `delta_checks.sh` 11/11; evidence manifest spot-check; `diff --check` against live dev | R732-5 | 86a349d5399d8abc40b819d09806fc8245682609 |
| Docs | CLEAN (RESIDUE F1, R732-4 R1-R3, R731-1 F1, R732-1 R1 carried) | PR body; commit message; tree grep for merge-status claims | R732-5 | 86a349d5399d8abc40b819d09806fc8245682609 |

## Limits

- **Em-dash gate.** `scripts/check_em_dash.py --base 8adf5c99` could not judge here: the pinned Markdown renderer (html5lib) is not installed, and installing it is not allowed (rc 2, `receipts/05-gates-and-state.txt`). The tree is identical to `cbc7c604`, which R732-4 found clean through the docs gates. The diff against dev is the same 70 files, so a new finding is not expected.
- **Hosted checks** (`receipts/06-hosted-checks.tsv`, at writing time):
  - `docs-check-no-git` and `wire-accountability` show success.
  - `docs-gates-0/1/2` and "Fail fast across this head" were queued or in progress.
  - No `rtl-fast`, `verilator-suites` or `yosys-portability` context was listed yet.
  - None of these is claimed here.
- **Execution evidence.** No source bank was run in this round. The source-head execution evidence is the author's published receipts, which cover the same bytes (`f7d5fc3c` to `cbc7c604`, with the docs-only changes R732-4 checked).
- **Packet signature.** The evidence packet commit `a16caad4` shows as unsigned in the hosting service's verification. I checked its manifest's published sha256 values by spot-check only.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Probes.** Nothing was mutated. The clone's index and worktree match `86a349d5`, and its gitlinks are unchanged.

## Pending manager duties

- Hosted and act acceptance at `86a349d5`. The local CI re-run started at 18:16 local time. The hosted `rtl-fast`, plus `verilator-suites` and `yosys-portability`, are needed on this exact head.
- Build and validate the current-dev merge candidate (builder and native banks) on dev `8adf5c99`, and link its receipts.
- Carry F1 and the retained RESIDUE items to the residue checklist.
- Merge order: PR #820 is still open, and the body says this PR merges after it.
- A merge needs explicit maintainer authorization.

R732-5 FINISHED
