[R732] POSITIVE - exact head 455a3953bf49efda23be4e73447a25b66a5c4bf7

Round R732-7. External independent review of issue #787 / PR #822 at the exact head `455a3953bf49efda23be4e73447a25b66a5c4bf7`, tree `43d185333ff4048986a2080996ed5e482af3f3bc`. The previously reviewed head is `86a349d5`.

**Verdict: POSITIVE.** Nothing MINOR or worse is open. The delta is one merge commit of live dev `e5b8405d` (PR #820 merged). It changes no byte of the tree. The PR body still names an older head and describes #820 and #826 as unmerged. That is recorded as RESIDUE R1 (wording only), with the retained prior items.

## The delta

Receipts: `receipts/merge_delta_checks.txt` and `receipts/merge_delta_checks_script.txt`. Script: `scripts/merge_delta_checks.sh`.

| Check | Result |
|---|---|
| Tree identity | `455a3953^{tree}` = `86a349d5^{tree}` = `cbc7c604^{tree}` = `43d18533…`. `git diff --stat 86a349d5 455a3953` is empty. |
| Parents | `86a349d5399d8abc…` (first) and `e5b8405db4c1f7cb…` (second). `e5b8405d` is live `origin/dev`, fetched this round. |
| Merge base | `git merge-base --all 455a3953 origin/dev` gives one base, `e5b8405d`. `git merge-base --all 86a349d5 origin/dev` gives two, `8adf5c99` and `81f78a81`. That confirms the criss-cross the merge removes. |
| Cause of the criss-cross | `e5b8405d` merges `81f78a81` (PR #820's head) into dev `8adf5c99`. `81f78a81` was already in the branch through `6ffadb07`, and `8adf5c99` through `86a349d5`. |
| Merge is the automatic merge | `git merge-tree --write-tree 86a349d5 e5b8405d` gives `43d18533…`, the head's tree. Nothing was hand-resolved. |
| #820's content | Of the 11 files #820 changes against `8adf5c99`, 7 match dev byte for byte at the head. In the other 4 (`CHANGELOG.md`, `AREA_BUDGET.md`, `BUILDING.md`, `SUBMODULES.md`), the head-vs-dev diff equals this branch's own diff `81f78a81..86a349d5`. That is the content already reviewed at `cbc7c604` and `86a349d5`. `syn/ooc/pp_resource_gate.py` is blob `fa26f0f9` at the head, at dev, at `81f78a81` and at `50e5d08d` (the gate the route receipts name). |
| Gitlinks | external `efeb541a`, gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`. These are unchanged, because the tree is identical. |
| Commit message | One line, no trailers: "Merge dev e5b8405d (PR #820 merged) into 787-reboot-reset, so the branch has one merge base with dev". It is accurate. |
| GitHub state (read only) | `headRefOid` is `455a3953…`, `mergeable` is MERGEABLE, and `mergeStateStatus` is BLOCKED (pending review and checks). It is no longer the conflict report. |
| Comment rule | No source byte changes, so there is no new comment and no new RESIDUE under the rule. |

Published evidence `review-evidence/787-r1` at `a16caad4`: all 1566 `published_sha256` entries of `MANIFEST.json` match the extracted bytes. No file is missing and none is unlisted (`receipts/evidence_manifest_check.txt`, `scripts/verify_evidence_manifest.py`). The author-r5 `review-ready.md` names `f7d5fc3c` as its gate head, which matches the body's route section.

Exact-head hosted runs (`receipts/hosted_checkruns_455a3953.tsv`, read at review time): 6 success, 1 skipped, 20 in progress, 21 queued, none failed. These are not claimed as evidence here. The manager owns hosted and act acceptance.

## Findings

### R1 - RESIDUE - Docs (PR body) - PR #822 body, "Status" lines 5, 16-17 and "Linked Issue / roles" line 68 - the body predates heads `86a349d5` and `455a3953` and the merges of #826 and #820
- **Evidence (`receipts/pr822_body.md`):**
  - Line 16 reads "**REVIEW READY** at `cbc7c604…` … -> `dev` (`02ca829a`)".
  - Line 17 reads "… and merges after both".
  - Line 68 reads "Carries PR #826 … and merges after it".
  - The body does not mention the two later merge commits of dev, `86a349d5` (`8adf5c99`) and `455a3953` (`e5b8405d`). Both PRs are now merged into dev, and live dev is `e5b8405d`.
- **Why it is only RESIDUE:** the three heads share tree `43d18533`. So every gate, measurement and figure the body attributes to `f7d5fc3c`/`cbc7c604` describes the same bytes. No figure, verdict, test or clause claim changes.
- **Exact fix:**
  - Line 16: "**REVIEW READY** at `455a3953bf49efda23be4e73447a25b66a5c4bf7` (tree `43d18533`, identical to `cbc7c604`'s). `787-reboot-reset` -> `dev` (`e5b8405d`)."
  - Line 17: "PRs #826 (#814) and #820 (#818) are merged into dev. `86a349d5` and `455a3953` merge dev `8adf5c99` and `e5b8405d`. Neither changes the tree; the second leaves one merge base with dev."
  - Line 68: "Carried PR #826 (#814) and PR #820 (#818), both now merged into dev."
  - Line 5: drop "carrying PR #826's commits".
- **Verification:** grep the body for `455a3953` and `e5b8405d`, and confirm it no longer contains "merges after".

## Prior findings, resolved or retained at this head

The tree is identical to `86a349d5` and `cbc7c604`, so every file-located item has the same bytes.

| Prior finding | Severity; lenses | Status at `455a3953` |
|---|---|---|
| R732-5 F1 = R731-5 RES-1 = R732-4 R1 / R731-4 RES-C: body predates the later heads and merges | RESIDUE; Docs | **Retained**, superseded by R1 above. Apply R1. |
| R731-4 RES-A = R732-4 R1 (first part): body line 202, "that file is not part of this PR" | RESIDUE; Docs | **Resolved by the merge.** The string is still present at body lines 202-203. With #820 on dev, though, `syn/ooc/pp_resource_gate.py` is no longer in the PR's diff against dev (`git diff e5b8405d 455a3953` does not list it), so the sentence is now true. Optional: "(on dev since PR #820)". |
| R731-4 RES-B: "**Gates at the head pass.**" (body line 34) | RESIDUE; Docs | **Retained.** Fix: "**Gates at `f7d5fc3c` pass; the tree at `455a3953` is identical to `cbc7c604`'s.**" |
| R732-4 R2: `docs/reference/SUBMODULES.md:503`, "this change" has no referent | RESIDUE; Docs | **Retained** (bytes unchanged). Fix: "That path lies outside #787's change." |
| R732-4 R3 = R731-4 RES-D/RES-E: `AREA_BUDGET.md:149-150`, `SUBMODULES.md:511-517`, where the re-pin route is recorded | RESIDUE; Docs | **Retained** (bytes unchanged). Fix as R732-4 R3 states it. |
| R731-1 F1 = R732-1 R2: `tb/verilator/reboot_ctrl/mutants.py:113-114`, a lane label and an issue-comment ID in a comment | RESIDUE; Docs | **Retained.** Blob `2528a927` is unchanged, and line 113 still reads `# the [A10] arms of issuecomment-6518083444: …`. Tracked under #746. |
| R732-1 R1: `tb/tools/torture_campaign.py:3135-3139`, the link-down comment omits the egress wait | RESIDUE; Docs | **Retained.** Blob `43b1fc40` is unchanged. |
| R732-5 S1: `.github/workflows/rtl-fast.yml:53-54`, a criss-cross history fails with an unexplained error | SUGGESTION; Robustness, Tests | **Retained** (optional). The workflow is unchanged, but this head no longer has a criss-cross with dev, so it does not trigger here. |
| R732-4 S1 = R731-4 SUG-1 / R731-3 S2: the `cdc_census.gen.py:122-123` MultiReg note; no `--check` arm | SUGGESTION; Docs, Tests | Retained (optional) |
| R732-4 S2, S3; R731-4 SUG-2; R731-3 S3 | SUGGESTION; Docs / Tests | Retained (optional; bytes unchanged) |
| R732-1 S1, R731-1 S2: `hdl/milan/KL_reboot_ctrl.sv` (blob `d2c74f47`) | SUGGESTION; RTL, Robustness, Tests | Retained (optional) |
| R732-1 S2: `mutants.py`, no saturation control | SUGGESTION; Tests | Retained (optional) |
| R731-1 S1: the `.mac_tx_beat_i` / `.mac_flush_i` wirings | SUGGESTION; Tests, Robustness | Retained (optional) |

No prior MINOR or worse is open: R732-5 and R731-5 at `86a349d5` were POSITIVE, and so were R732-4 and R731-4 at `cbc7c604`.

## Lens results

```text
[R732] PASS Conformance - receipts/merge_delta_checks.txt (tree 43d18533 = 86a349d5's = cbc7c604's) - no byte of the REBOOT reset, egress wait or DEPARTING path changes, so the frozen acceptance and the IEEE 1722.1-2021 7.4.43 / Milan v1.2 5.6.3.3 verdict at cbc7c604 carries
[R732] PASS RTL - receipts/merge_delta_checks.txt (empty diff 86a349d5..455a3953; the six gitlinks; KL_reboot_ctrl.sv blob d2c74f47) - no HDL, generator or pin changes; the merge is the automatic merge-tree result
[R732] PASS Robustness - receipts/merge_delta_checks.txt (single merge base e5b8405d; was two) - no behaviour delta; the merge removes the criss-cross that made GitHub refuse the merge, and the PR is MERGEABLE
[R732] PASS Tests - receipts/evidence_manifest_check.txt (1566/1566 hashes) and receipts/merge_delta_checks.txt (no test byte changes) - the author's gate receipts at f7d5fc3c cover the identical tree; exact-head hosted runs are still pending and are not claimed
[R732] PASS Docs - commit 455a3953 message (one line, accurate) and receipts/pr822_body.md lines 5, 16-17, 34, 68, 202 - the body is stale in wording only (RESIDUE R1); no tracked doc changes
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Tree identity; prior coverage at the identical tree | R732-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| RTL | CLEAN | Empty diff, gitlinks, merge-tree reproduction | R732-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| Robustness | CLEAN (R732-5 S1 optional) | Merge bases before and after; GitHub mergeability | R732-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| Tests | CLEAN (optional SUGGESTIONs retained) | Evidence manifest, 1566 entries; no test delta; hosted check list (pending) | R732-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |
| Docs | CLEAN (RESIDUE R1 and the retained RESIDUE go to the checklist) | Commit message; PR body; the 4 shared doc files against dev | R732-7 | `455a3953bf49efda23be4e73447a25b66a5c4bf7` |

## Limits

- No suites, builds or probes were run. Nothing needed falsifying beyond git object checks, because the tree is byte-identical to `cbc7c604`'s.
- The source-head execution evidence is the author's published receipts at `f7d5fc3c`, plus earlier rounds on inputs `f7d5fc3c` does not change. No manager source bank ran at this head, and none is claimed or inferred.
- Exact-head hosted runs were still in progress or queued when this was read.
- Physical calibration was NOT RUN. Field skips are not hardware proof. The bench soft-reset run that closes #787 is outside this review.
- The working clone is unmodified (`git status --porcelain` is empty), so there was nothing to restore.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `1e80128f`, live dev `e5b8405d`) with the builder and native banks at the merge turn, and link its receipts.
- Accept the exact-head hosted and act results for `455a3953`.
- Carry R1, R731-4 RES-B, R732-4 R2 and R3, R731-1 F1 = R732-1 R2, and R732-1 R1 to the residue checklist.
- Merging requires explicit maintainer authorization.

R732-7 FINISHED
