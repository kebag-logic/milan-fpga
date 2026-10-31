[R731] POSITIVE - exact head 86a349d5399d8abc40b819d09806fc8245682609

Round R731-5. Internal cleared-context review of issue #787 / PR #822 at tree `43d185333ff4048986a2080996ed5e482af3f3bc`. The delta from the reviewed head `cbc7c604` is one merge commit of live dev `8adf5c99` (PR #826, merged 2026-10-31T16:28:22Z). This report has no MINOR, MAJOR or BLOCKER. It has one new RESIDUE (RES-1, the PR body's head line), and it carries the prior wording items forward.

## 1. Delta verification (all claims confirmed)

| Claim | Result | Receipt |
|---|---|---|
| Tree is byte-identical | `cbc7c604^{tree}` = `86a349d5^{tree}` = `43d18533`; `git diff --quiet cbc7c604 86a349d5` rc 0 | `receipts/classifier_replay.txt`, `receipts/replay_script_output.txt` |
| Parents | `cbc7c6043ebf…` (first), `8adf5c990bad…` (second) | same |
| Live dev tip | `git ls-remote origin refs/heads/dev` = `8adf5c99`; `refs/pull/822/head` = `86a349d5` | `receipts/classifier_replay.txt` |
| The merge is the automatic one | `git merge-tree --write-tree cbc7c604 8adf5c99` = `43d18533` (clean, rc 0) | `receipts/integrity.txt` |
| The dev tip is the automatic merge of its parents | `merge-tree 02ca829a 4ee2aa96` = `8adf5c99^{tree}` = `c5ae6597`, so dev carries no hand change that this branch could lack | `receipts/integrity.txt` |
| Before: two merge bases | `merge-base --all 8adf5c99 cbc7c604` gives `02ca829a` and `4ee2aa96`; both are ancestors of `cbc7c604` | `receipts/classifier_replay.txt` |
| After: one merge base | `merge-base --all 8adf5c99 86a349d5` gives `8adf5c99` | same |
| The classifier refused the old history, not the content | `.github/workflows/rtl-fast.yml:53-54` (act path): `git cat-file -e "$base^{commit}"` fails (rc 128) on the two-line base at `cbc7c604` and passes (rc 0) at `86a349d5`. Both heads give the same merged tree and the same 70-file changed list (sha256 `9edc6678…`), so the classification is unchanged. The hosted path (`:57-58`, `$GITHUB_SHA^1..$GITHUB_SHA`) is not affected either way | same |
| Commit message | One line, no trailers, no body: "Merge dev 8adf5c99 (PR #826 merged) into 787-reboot-reset, so the branch has one merge base with dev". It matches the merge it describes | `receipts/integrity.txt` (raw bytes) |
| Submodule gitlinks | The six gitlinks are identical at both heads (listing sha256 `27a94734…`); `protocol-processor` `a9e84b66`, `gptp-processor` `135afd04` | `receipts/integrity.txt` |
| Comment rule | No source byte changes, so there is no new comment and no new RESIDUE under that rule | tree identity |

Published evidence spot-check: all 1566 entries of `review-evidence/787-r1/MANIFEST.json` at `a16caad4` hash-match their published blobs (`receipts/evidence_manifest_check.txt`). The latest author receipts are `author-r5/*-f7d5fc3c`. They carry to this head by the prior rounds' carry argument plus the tree identity established here.

Hosted at the exact head (snapshot `receipts/hosted_checkruns_86a349d5.tsv`): `docs-check-no-git` and `wire-accountability` completed with success. `docs-gates-0..2` and "Fail fast across this head" were still queued or in progress. I claim no hosted or act acceptance; that belongs to the manager.

## 2. Findings

### RES-1 - RESIDUE - Docs (PR body) - PR #822 body, "Status" lines 16-17 and "Linked Issue / roles" line 68
- **Evidence:**
  - Line 16 reads "**REVIEW READY** at `cbc7c6043ebf…`. `787-reboot-reset` -> `dev` (`02ca829a`)." The head is now `86a349d5`, and dev is `8adf5c99`.
  - The body does not mention the dev merge `86a349d5`. That merge is described publicly only in the author comment 6546588633.
  - Line 17's "merges after both" and line 68's "merges after it" predate PR #826's merge. #826 is now in dev, so only PR #820 (still OPEN; `81f78a81` is not in dev) remains a merge-order dependency.
- **Why RESIDUE:** the content and gate attribution are unchanged by tree identity. No measurement, figure, verdict, test or clause claim changes.
- **Exact fix:**
  - Line 16: "**REVIEW READY** at `86a349d5399d8abc40b819d09806fc8245682609` (tree `43d18533`, identical to `cbc7c604`). `787-reboot-reset` -> `dev` (`8adf5c99`)."
  - After line 19, add the bullet: "- **`86a349d5` merges dev `8adf5c99` (PR #826 merged).** The tree is unchanged. It gives the branch one merge base with dev, which rtl-fast's change classifier requires."
  - Line 17: replace "and merges after both." with "PR #826 is merged into dev; this PR merges after PR #820."
  - Line 68: "Carried PR #826 (#814), now merged into dev at `8adf5c99`."

### Prior findings at this head (read after the pass above)
No prior MINOR or worse is open: R731-4 and R732-4 at `cbc7c604` were both POSITIVE. Tree identity means every file-located item has the same bytes at this head.

| Prior item | Class; lens | Status at `86a349d5` |
|---|---|---|
| R731-4 RES-A = R732-4 R1 (first part): "that file is not part of this PR" | RESIDUE; Docs | **Resolved.** The string is absent from the current body (`receipts/pr822_body_probe.txt`) |
| R731-4 RES-B: "**Gates at the head pass.**" (body line 34) | RESIDUE; Docs | **Retained.** Update the fix to "**Gates at `f7d5fc3c` pass, and carry to `86a349d5`** (tree identical to `cbc7c604`)…" |
| R731-4 RES-C = R732-4 R1 (rest): lines 5, 17, 68 omit #820 / round 6 | RESIDUE; Docs | **Retained.** Line 5 still reads "carrying PR #826's commits", and line 17 "Rounds 4 and 5". Apply together with RES-1, and add #820 to line 68 |
| R731-4 RES-D, RES-E = R732-4 R3; R732-4 R2 (`SUBMODULES.md:503` "this change") | RESIDUE; Docs | **Retained** (bytes unchanged) |
| R731-1 F1 = R732-1 R2 (`tb/verilator/reboot_ctrl/mutants.py:113-114`); R732-1 R1 (`tb/tools/torture_campaign.py:3135-3139`) | RESIDUE; Docs | **Retained** (bytes unchanged; tracked by #746) |
| R731-4 SUG-1 = R732-4 S1; SUG-2; R732-4 S2, S3; R731-3 S2, S3; R731-1 S1, S2; R732-1 S1, S2 | SUGGESTION | **Retained** (optional; bytes unchanged) |

## 3. Lens results

- `[R731] PASS Conformance - tree 43d18533 (= cbc7c604 tree), rtl-fast.yml:53-54 replay - no byte delta; the AECP REBOOT / ENTITY_DEPARTING behaviour covered at cbc7c604 is unchanged`
- `[R731] PASS RTL - git diff cbc7c604 86a349d5 (empty), gitlink listing - no HDL, generator or pin change`
- `[R731] PASS Robustness - same empty diff; merge-tree recompute of both merges - the dev merge drops nothing from either side`
- `[R731] PASS Tests - classifier replay at both heads: same 70-file scope, so the same gate set is selected; no test bytes changed`
- `[R731] PASS Docs - commit subject, PR body (sha256 901a9b63…), author comment 6546588633 - RES-1 and the retained items are wording only`

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Tree identity; prior conformance coverage at `cbc7c604` | R731-5 (delta); R731-4 (content) | `86a349d5399d8abc40b819d09806fc8245682609` |
| RTL | CLEAN | Empty diff; gitlinks; merge-tree recompute | R731-5 | `86a349d5399d8abc40b819d09806fc8245682609` |
| Robustness | CLEAN | Automatic-merge proof for `86a349d5` and `8adf5c99` | R731-5 | `86a349d5399d8abc40b819d09806fc8245682609` |
| Tests | CLEAN | Classifier replay (`rtl-fast.yml:53-58`); changed-file set | R731-5 | `86a349d5399d8abc40b819d09806fc8245682609` |
| Docs | CLEAN (RES-1 and the retained RESIDUE go to the residue checklist) | Commit message; PR body; author head comment | R731-5 | `86a349d5399d8abc40b819d09806fc8245682609` |

## 4. Limits and pending manager duties
- No source gates were re-run here. Source-head execution evidence is the author's published receipts (`author-r5`, `f7d5fc3c`), carried by tree identity. The author's local CI re-run at `86a349d5` (comment 6546588633) had not been published when this round ran.
- No manager source bank runs at this head, and none is claimed. The current-dev merge candidate (builder and native banks, live dev `8adf5c99`) is the manager's at the merge turn.
- Hosted contexts were in progress at the snapshot. Hosted and act acceptance belong to the manager.
- Physical calibration is NOT RUN. Field skips are not hardware proof.
- PR #820 is still OPEN, and this PR must merge after it.
- Clone state after the round: HEAD `86a349d5`, worktree and index clean, gitlinks unchanged. No probe modified tracked bytes.

R731-5 FINISHED
