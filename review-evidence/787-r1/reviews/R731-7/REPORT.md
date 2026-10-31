[R731] POSITIVE - exact head 455a3953bf49efda23be4e73447a25b66a5c4bf7

Round R731-7. Internal cleared-context review of issue #787 / PR #822 at tree `43d185333ff4048986a2080996ed5e482af3f3bc`. The delta from the reviewed head `86a349d5` is one merge commit of live dev `e5b8405d` (PR #820 / #818). It adds no content. This round has no MINOR, MAJOR or BLOCKER. It has one RESIDUE (RES-1, the PR body). Prior items are carried at their cause.

## 1. Delta facts (receipt `receipts/verify_delta.txt`, script `scripts/verify_delta.sh <repo>`)

- **Head and tree.** The head is `455a3953bf49efda23be4e73447a25b66a5c4bf7` and its tree is `43d18533…`. That equals the tree of `86a349d5`, and also of `cbc7c604`. `git diff --name-only 86a349d5 455a3953`: 0 files.
- **Parents.** `86a349d5399d8abc40b819d09806fc8245682609` and `e5b8405db4c1f7cbdafb5df92b15b580142e0232`, in that order.
- **The merge is faithful, not an "ours" merge.** `git merge-tree --write-tree 86a349d5 e5b8405d` recomputes `43d18533…` with rc 0.
- **Why the tree is unchanged.** `git rev-list 86a349d5..e5b8405d` yields only `e5b8405d` itself. Both of its parents (`8adf5c99` and `81f78a81`) were already ancestors of `86a349d5`, so the merge carries no new file change.
- **Merge bases.**
  - Before the merge, `git merge-base --all 86a349d5 e5b8405d` gives two bases, `8adf5c99` and `81f78a81`. That is the criss-cross the author describes.
  - After it, `git merge-base --all 455a3953 e5b8405d` gives exactly `e5b8405d`.
  - `origin/dev` is still `e5b8405d` at review time, so `git rev-list HEAD..origin/dev` is empty.
  - GitHub now reports `mergeable: MERGEABLE` (`receipts/pr822.json`). The status is `BLOCKED` only on the protected gates and reviews.
- **Commit message.** It is one line: "Merge dev e5b8405d (PR #820 merged) into 787-reboot-reset, so the branch has one merge base with dev". The body is empty (0 bytes), so there are no trailers. The subject's claim is true at this head.
- **Gitlinks are unchanged.** protocol-processor is `a9e84b66` and gptp-processor is `135afd04`, as the PR body states. external is `efeb541a`, lwSRP `08ee86e8`, tsn-c-stack `70936b77` and verilog-axis `48ff7a7e`.
- **#818 gate file.** `syn/ooc/pp_resource_gate.py` has blob `fa26f0f9` at the head. That is the same blob as at PR #820's `50e5d08d` and at dev `e5b8405d`.
- **Published evidence.** `review-evidence/787-r1/MANIFEST.json` at `a16caad4` lists 1566 entries, and all 1566 match their `published_sha256`.
- **Hosted, at the exact head** (`receipts/checkruns-455a3953.tsv`, snapshot):
  - 6 succeeded and 1 was skipped (Physical gPTP, nightly/manual, not run). The other 41 are queued or in progress.
  - This round does not claim the hosted gates. The manager owns hosted and act acceptance.
- **Clone state.** No probe edited the tree. `git status --porcelain` is empty and HEAD is `455a3953`.

## 2. Findings

### RES-1 - RESIDUE - Docs (PR body) - PR #822 body (`receipts/pr822-body.md`, sha256 `901a9b63…`, unchanged since R731-5) - the body still predates both dev merges

This carries R731-6 RES-1 forward. It subsumes R731-5 RES-1 and R732-5 F1, and it covers R731-4 RES-A, RES-B and RES-C and R732-4 R1.

- **Evidence:**
  - Line 16 still reads "REVIEW READY at `cbc7c604…` … -> `dev` (`02ca829a`)".
  - Line 17 and line 68 say the PR "merges after" #826 and #820. Both are in dev now.
  - Line 34 reads "**Gates at the head pass.**".
  - Lines 202-203 read "that file is not part of this PR". The gate file is in dev, at a byte-equal blob.
  - The body describes neither `86a349d5` nor `455a3953`.
- **Why RESIDUE:** the tree is byte-identical to `cbc7c604`. So every gate, figure, route measurement and clause claim in the body holds at this head. Only the head SHA, the dev SHA and the merge-order wording are stale.
- **Exact fix:**
  - Line 16: "**REVIEW READY** at `455a3953bf49efda23be4e73447a25b66a5c4bf7` (tree `43d18533`, identical to `cbc7c604`). `787-reboot-reset` -> `dev` (`e5b8405d`)."
  - Line 5: "carrying PR #826's and PR #820's commits".
  - Lines 17 and 68: "PR #826 (#814) and PR #820 (#818) are merged into dev (`8adf5c99`, `e5b8405d`); this PR carried their commits."
  - Line 34: "**Gates at `f7d5fc3c` pass, and carry to `455a3953`** (tree identical to `cbc7c604`)."
  - Lines 202-203: delete "; that file is not part of this PR".
  - After the round 6 list, add: "Merges of dev: `86a349d5` (dev `8adf5c99`, PR #826 merged) and `455a3953` (dev `e5b8405d`, PR #820 merged). Each tree is byte-identical to `cbc7c604`'s. After `455a3953` the branch has one merge base with dev."
- **Verification:** read the body. No `cbc7c604` should appear as the review-ready head, no `02ca829a` as the current dev, and no "merges after" should remain for #826 or #820.

**Comment rule.** The delta changes no source byte, so no new comment instance is possible. No new RESIDUE of that kind.

## 3. Prior public findings at this head (read after the pass above)

The tree is byte-identical to the heads R731-5, R732-5 and R731-6 judged. Each in-tree item therefore keeps its status, checked at its cause.

| Prior item | Class; lenses | Status at `455a3953` |
|---|---|---|
| R731-3 F1 = R732-3 F1; R732-3 F2 | MINOR (earlier) | Resolved since `cbc7c604`; tree identical |
| R731-6 RES-1 (= R731-5 RES-1, R732-5 F1, R731-4 RES-A/B/C, R732-4 R1) | RESIDUE; Docs | **Retained** as RES-1 above, with the fix updated to this head. The body's sha256 is unchanged |
| R732-4 R2: `docs/reference/SUBMODULES.md:503` "this change" | RESIDUE; Docs | Retained (bytes unchanged). Fix: "That path lies outside #787's change." |
| R731-4 RES-D/RES-E = R732-4 R3: re-pin route record pointer (`AREA_BUDGET.md:149-150`, `SUBMODULES.md:511-517`) | RESIDUE; Docs | Retained (bytes unchanged); fix as R732-4 R3 |
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114` lane label / comment ID | RESIDUE; Docs | Retained (bytes unchanged; tracked by #746) |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139` | RESIDUE; Docs | Retained (bytes unchanged) |
| R731-4 SUG-1 = R732-4 S1, SUG-2, R732-4 S2/S3, R731-3 S2/S3, R731-1 S1/S2, R732-1 S1/S2, R732-5 S1 | SUGGESTION | Retained (optional) |
| R731-6 MD-1 ("one merge base" sentence false while #820 was unmerged) | note | **Resolved by this head.** One merge base with dev now holds, so RES-1's new sentence may use it |

No prior MINOR or worse is open.

## 4. Lens results

- `[R731] PASS Conformance - git diff 86a349d5 455a3953 (0 files); merge-tree recompute 43d18533 - no acceptance, requirement or protocol artifact changes. Content reviewed POSITIVE at 86a349d5 (R731-5) and as candidate 808e64e3 (R731-6, same tree) carries over byte-for-byte`
- `[R731] PASS RTL - tree 43d18533; gitlinks a9e84b66 / 135afd04 unchanged - no HDL, constraint or generator byte changes, so the prior RTL verdict's dependencies are unchanged`
- `[R731] PASS Robustness - same tree; the git-level hazard was the two merge bases (8adf5c99, 81f78a81), now one (e5b8405d) - no RTL path or reset or failure path changes`
- `[R731] PASS Tests - same tree; pp_resource_gate.py blob fa26f0f9 equals dev's; evidence manifest 1566/1566 hashes verified - no test or gate source changes, and the author's gate receipts at f7d5fc3c apply to an identical tree`
- `[R731] PASS Docs - commit subject (one line, no body, true); PR body sha256 901a9b63 - stale in wording only (RES-1, carried to the residue checklist)`

## 5. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta diff (empty); merge-tree recompute; prior content verdicts at the identical tree | R731-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| RTL | CLEAN | tree identity; gitlinks | R731-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| Robustness | CLEAN | tree identity; merge-base topology before and after | R731-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| Tests | CLEAN | tree identity; #818 gate blob; evidence manifest at `a16caad4` | R731-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| Docs | CLEAN (RESIDUE carried) | commit message; PR body | R731-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |

## 6. Real limits and pending manager duties

- **No source bank ran at this head.** Source-head execution evidence is the author's published receipts at `f7d5fc3c` and `3e67de9c`. They carry to this head only by tree identity, and this round did not re-run them.
- **Hosted exact-head gates were still running** at the snapshot. Verilator, Yosys and firmware were queued or in progress. Physical gPTP was skipped and is not hardware proof.
- **Physical calibration was NOT RUN.**
- **Pending manager duties:**
  - Validate the current-dev merge candidate with the builder and native banks, and link the receipts on the PR.
  - Accept the hosted and act results at `455a3953`.
  - Carry RES-1 and the retained RESIDUE to the residue checklist.
  - Confirm that `origin/dev` is still `e5b8405d` at the merge turn, or re-check the merge bases if it has moved.

R731-7 FINISHED
