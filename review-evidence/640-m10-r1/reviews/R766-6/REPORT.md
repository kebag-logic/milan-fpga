[R766] POSITIVE - exact head 72816d26a7e2a29db5bc198ff65056ee4c5790b4

# R766-6: external cleared-context review of issue #640 / PR #835, round 6

- Head `72816d26a7e2a29db5bc198ff65056ee4c5790b4`, tree `f9498ee5a4a88bf63453a3a2d162a1b225a7715e`. It is a merge commit: parents `d85da329` (the round 5 head) and dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`.
- Source base `503bc97cd4f24ad07596c17e7188f2024617972d`. The previously reviewed head is `d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73`, where R766-5 was POSITIVE.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR is open at this head. One RESIDUE (PR body wording) and one SUGGESTION (evidence packet) are recorded below. Neither makes the verdict negative.
- Scope of this round: a sync-only delta. All five lenses were applied to the merge, scaled to what it changes. Code the delta does not touch keeps its round 5 verdict.

## Order of reconstruction

1. AGENTS.md and CONTRIBUTING.md (the review contract, lens tokens and the one-line commit rule). docs/README.md.
2. Issue #640: its body acceptance of 2026-10-31 is unchanged. The four criteria are: under 20,000 LUTs at 32x32, Block RAM fit and timing; 65 µs talker latency; unchanged function; and a re-recorded gate baseline. Since round 5 the issue has only daily area measurements, TAKEN and REVIEW READY from the author, and the two review-start comments. No scope decision has changed.
3. Authorities the branch's lines cite: NFR-RES-01 and NFR-SCOUT-03 / 3.4.1 in `docs/reference/FR_NFR.md`, QSPI_FLASHBOOT.md, SPLIT_CONTROL_MEMORY.md, REBOOT_RESET.md, ARCHITECTURE_HW_SW_SPLIT.md and MAILBOX_CONTRACT.md. None of these changed between `503bc97c` and `0a75aa77`. Every cited anchor still exists at the head: `#layout-baremetal---shipping-ax7101`, `#5-fit` (35.0 tiles at 1x1, line 147), `#1-the-decision`, `#341-...` and `#35-...`.
4. The diff and its history: `git diff 0a75aa77..72816d26`, `git diff 503bc97c..d85da329`, `git diff d85da329..72816d26` on the four pages, and dev's own changes to those pages and to `sw/litex/milan_soc.py`.
5. Public executable evidence: the author-r6 receipts on evidence commit `b6694157` and the evidence `MANIFEST.json`, then my own re-runs. Prior findings were read only after this pass and after the verdict and ledger were written (see the last section).

## Executed checks (receipts in this packet)

| Check | Result | Receipt |
|---|---|---|
| Added and removed lines, `0a75aa77..72816d26` against `503bc97c..d85da329` | **Byte-identical**: 284 lines each, 231 added and 53 removed. Both deltas touch the same four pages. The patches differ only in blob ids, hunk offsets and dev-side context lines | `receipts/dev_to_head.lines`, `receipts/base_to_r5.lines`, `receipts/dev_to_head.diff`, `receipts/base_to_r5.diff` |
| `MAILBOX_SPLIT.md` blob | Head = round 5 (`12b31086`). Dev did not touch it | `git rev-parse` in this report |
| Branch-page lines changed since round 5 (`d85da329..72816d26`) | Only dev's lines: the #845/#843 records, the +0.242 ns comparison, the 53,221-LUT route table, the wrapper 24,996 / 24,937, and dev's 234 row | `receipts/prior_findings_at_head.txt` |
| Census coverage at the head, against dev's `sw/litex/milan_soc.py` | **PASS**, rc 0, 23 rows, none unmapped. The body is byte-identical to the author's r6 log after its header line | `receipts/census_coverage_head.out`, `.rc` |
| Census control on the round 1 page `3f8ed303` | **FAIL** as required: rc 1, 9 MISSING | `receipts/census_coverage_control_r1.out`, `.rc` |
| `milan_soc.py` at the head = dev | Identical blob. Dev's +26/-7 adds the MII launch and observer shapes for #829. The `mii` model was already there at base (Arty), and the census describes the AX7101 GMII basis | `receipts/milan_soc_identity.txt`, `receipts/milan_soc_base_to_dev.diff` |
| Census fates that depend on code, after dev's firmware changes | Nothing writes `milan_mac_loopback`. `timer0`'s readers are the flash driver's elapsed time and its bench mirror, which predates base. No firmware C enables an IRQ or touches `ctrl_` | `receipts/census_claim_probes.txt` |
| `docs_inventory.py --check` and `--selftest` | **Fresh**: 547 lines, `DOCUMENTATION_AUDIT.md` fresh; selftest 60 controls | `receipts/docs_inventory_check.log`, `receipts/gate_46_inventory.log` |
| docs.yml page gates at the head: gate_7 docs_check, gate_9 style + gPTP docs, gate_15 feature status, gate_16 traceability, gate_43 cited paths, gate_44 archive, gate_45 TOC/anchors, gate_46 inventory | **All rc 0**. docs_check: 0 findings across 214 md files. Paths: 1,638 resolve. TOC: 152 pages | `receipts/gate_*.log`, `.rc` |
| `check_em_dash.py` against `0a75aa77` and against `503bc97c` (pinned renderer, private venv) | 0 findings over 231 and over 2,287 added lines | `receipts/em_dash_vs_*.log` |
| `git diff --check` against dev and against base | Clean | `receipts/diff_check_vs_*.log` |
| Merge commit form | One line, no trailers. Dev's 9 first-parent merges and 231 commits match the PR body's table | `receipts/merge_commit_and_gitlinks.txt`, `receipts/dev_merges_and_pr810.txt` |
| Gitlinks at the head = dev | All six identical | `receipts/merge_commit_and_gitlinks.txt` |
| Author-r6 receipts | 196 downloaded files match the evidence manifest's `published_sha256`; the 5 large ones were not downloaded. The verifier reads 65 rc 0, 31 NOT RUN with a reason, 0 bad. This agrees with REVIEW READY and the PR body. See SUGGESTION S1 | `receipts/author_r6_receipt_check.txt`, `receipts/author_r6_verify.md`, `scripts/check_author_r6_receipts.py` |
| PR #835 state | Head `72816d26`, ready, mergeable, base `dev`. PR #810 is OPEN and unmerged, as the page says | `receipts/pr835_state.json`, `receipts/dev_merges_and_pr810.txt` |
| Restore | HEAD and write-tree = `f9498ee5`; index and worktree clean; no untracked or ignored files; gitlinks unchanged | `receipts/restore_check.txt` |

All probes reproduce with `scripts/r766_6_probes.sh`.

## Focus checks

### (1) Merge resolution

- **`docs/findings/README.md`, the one conflict.** Row `:25` (234) is dev's row byte-for-byte: it appears as unchanged context in `0a75aa77..72816d26`. Row `:26` (649) carries the branch's round 5 edit verbatim: "a tenth of the gap to NFR-RES-01's former 60 % target". Both sides' intent is kept. Dev's row names the current route record (#843, 2026-11-07); the branch's row names the former 60 % target. They do not contradict.
- **`AREA_BUDGET.md`, auto-merged.** At `:137-138` the branch's "accepted target / needs fewer than 20,000 `xc7a100t` LUTs at 32x32" sits above dev's unchanged `:140-141` history lines: "38,040 LUTs; the [#799] route was 13,972 over it". 52,012 - 38,040 = 13,972, and the sentence names #799, so it stays true now that the record is 53,221. At `:234-237` the branch's acceptance bar, "fewer than 20,000 LUTs at 32x32 / must also fit Block RAM, with timing met", sits beside dev's "24,996 / 24,937 / at the [#799] record, a 10,521-LUT wrapper". The two read coherently, with no duplicate or contradicting line.
- **`MARK_II_AREA_PLAN.md`, auto-merged.** Dev changed the `:61` comparison to +0.242 ns and added the #845 and #843 lines at `:1097-1099`. None of the branch's 231 added lines cites a gate record, WNS, slices, the 52,012 / 52,529 / 53,221 route figures, or #799/#843/#845 (`grep` over `receipts/added.lines`). The branch's derived chain rests on the dated 2026-10-31 basis (`:38`, 52,008 LUTs), which dev leaves unchanged on the page.
- **Against dev, the head differs only in the four branch pages, with the same added and removed lines as round 5.** Confirmed byte-for-byte above.

### (2) The branch's claims against the merged dev

- Area figures: `MARK_II_AREA_PLAN.md:38-46` and the lever 4 table `:156` on. The 52,008 basis, the 3,249 SoC CPU row, the 5,119 LiteX top row, the 47 RAMB36 (29 FIFO + 18 BIOS) and the 34,223 owner chain are all still recorded on the page or in the cited #640/#665 comments. Dev changed none of them. The arithmetic re-checks: 34,223 - 3,249 = 30,974; 30,974 - 3,750 = 27,224; 26.2k - 5.2k = 21.0k; 10 / 115,200 s = 86.806 µs; 16 / 24 / 32 / 116 / 128 character times are 1.389 / 2.083 / 2.778 / 10.069 / 11.111 ms.
- Gate figures: the branch cites none. `AREA_BUDGET.md`'s gate figures are all dev's.
- The census passes against dev's `milan_soc.py`, and its control still fails.
- T_svc: `FR_NFR.md:339` still reads "Proposed project budget: `T_svc = 10 ms`", and PR #810 is still open. So `MARK_II_AREA_PLAN.md`'s "Dev's FR_NFR.md still proposes T_svc = 10 ms" and "PR #810, not merged" both hold at the merged dev.

### (3) Docs gates

`docs_inventory.py --check` is fresh at the head. Every page gate of docs.yml I ran exits 0 (table above). For the builder legs and the full 65 steps, I rely on the author's published receipts, which match the manifest. I did not re-run the builder legs.

## Findings

### R766-6-RESIDUE-1 (RESIDUE; Docs)

- **Where:** PR #835 body, "Authoritative references", last bullet: "… `docs/integration/QSPI_FLASHBOOT.md` at `503bc97c`; NFR-RES-01 and NFR-SCOUT-03 …".
- **Evidence:** the head's base is now `0a75aa77`. Two of the listed pages, `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md`, changed in dev after `503bc97c` (#845 and #843 records). The rest of the body already states the merge base `0a75aa77` (its "How to get into the same state" block).
- **Impact:** wording only. A cold reader is pointed at an older revision of two reference pages. No figure, claim or check depends on it, since the branch cites none of the lines dev changed.
- **Exact fix:** replace "at `503bc97c`" with "at `0a75aa77`, the merge base; since `503bc97c` only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` changed, by dev's #845 and #843 records".
- **Verification:** read the edited bullet.

### R766-6-S1 (SUGGESTION; Tests, Docs): evidence packet hash chain

- **Where:** `review-evidence/640-m10-r1/author-r6/evidence/SHA256SUMS` against `review-evidence/640-m10-r1/MANIFEST.json` at `b6694157`.
- **Evidence:** every published file matches the manifest's `published_sha256`. But for four files the author's pre-publication sums disagree with the manifest's `original_sha256`: `lane__census_coverage.log`, `lane__census_coverage_control.log`, `tools/run_docs_yml.py` and `tools/run_extra.sh`. All four carry private paths that were redacted. `PR-BODY.md` is listed in SHA256SUMS but not in the manifest.
- **Impact:** none on this PR. I reproduced the census result independently, and my output is byte-identical to the published log body. But a cold reader cannot tie those four published files to the author's own sums.
- **Suggested outcome:** hash after the final path normalization, or record which normalization produced `original_sha256`.

**Comment rule:** the delta against dev changes no source file, so no new source comment exists and no lane/round/reviewer label was introduced. The lane names in `MAILBOX_SPLIT.md` ("Lane F3", "#665 lane F6") are design-page prose that was already reviewed in round 5, not source comments.

## Per-lens results at `72816d26`

| Lens | Result | Artifact and what was checked |
|---|---|---|
| Conformance | PASS | `receipts/dev_to_head.lines` = `receipts/base_to_r5.lines`. Checked: the frozen #640 acceptance (issue body, 2026-10-31); `FR_NFR.md` NFR-RES-01 / 3.4.1 (`:339`), unchanged base→dev; `MARK_II_AREA_PLAN.md:38-46`, `:156` on, `:297`, `:342` on, figures and arithmetic against the unchanged basis; no branch line cites a figure dev moved (`receipts/added.lines`) |
| RTL | PASS | `git diff --stat 0a75aa77 72816d26` names four `.md` files and nothing under `hdl/`, `sw/`, `syn/`, `tb/` or any generator. Gitlinks equal dev (`receipts/merge_commit_and_gitlinks.txt`). The RTL lens is inapplicable by that artifact; round 5's verdict stands |
| Robustness | PASS | The same artifact: no executable change against dev. The code facts behind the census fates hold on the merged tree (`receipts/census_claim_probes.txt`), and dev's `milan_soc.py` change is MII shape only (`receipts/milan_soc_base_to_dev.diff`) |
| Tests | PASS | `receipts/census_coverage_head.out` (PASS) and `receipts/census_coverage_control_r1.out` (FAIL, 9 MISSING): the check can still fail for the defect it detects. docs.yml page gates all rc 0 (`receipts/gate_*`). Author receipts tie to the manifest (`receipts/author_r6_receipt_check.txt`). S1 is optional |
| Docs | PASS | The merge resolution at `docs/findings/README.md:25-26`, `AREA_BUDGET.md:137-141`, `:234-243` and `MARK_II_AREA_PLAN.md:61`, `:1097-1099` reads coherently. `docs_inventory.py --check` is fresh. em-dash, doc-style, TOC, cited-path and docs_check gates are clean. RESIDUE-1 is wording only |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #640 acceptance; `FR_NFR.md:339`; `MARK_II_AREA_PLAN.md:38-46`, `:156`–`:380`; `AREA_BUDGET.md:137-141`, `:234-237`; `receipts/dev_to_head.lines`, `receipts/added.lines` | R766-6 | `72816d26a7e2a29db5bc198ff65056ee4c5790b4` |
| RTL | CLEAN | `git diff --stat 0a75aa77 72816d26` (four `.md` only); `receipts/merge_commit_and_gitlinks.txt` | R766-6 | `72816d26a7e2a29db5bc198ff65056ee4c5790b4` |
| Robustness | CLEAN | Same diff stat; `receipts/census_claim_probes.txt`; `receipts/milan_soc_base_to_dev.diff` | R766-6 | `72816d26a7e2a29db5bc198ff65056ee4c5790b4` |
| Tests | CLEAN | `receipts/census_coverage_head.*`, `receipts/census_coverage_control_r1.*`, `receipts/gate_*`, `receipts/em_dash_vs_*`, `receipts/author_r6_receipt_check.txt`, `receipts/author_r6_verify.md` | R766-6 | `72816d26a7e2a29db5bc198ff65056ee4c5790b4` |
| Docs | CLEAN (RESIDUE-1 carried to the residue checklist) | `docs/findings/README.md:25-26`; `AREA_BUDGET.md:135-243`; `MARK_II_AREA_PLAN.md:61`, `:1097-1099`; `receipts/docs_inventory_check.log`, `receipts/gate_46_inventory.log`; PR #835 body | R766-6 | `72816d26a7e2a29db5bc198ff65056ee4c5790b4` |

## Prior public findings at this head

These were read after the verdict and ledger above were written. The sources were my R766-5 report (which itemises every R765-1…R765-4 and R766-1…R766-4 finding) and the R765-5 report's findings list. The concurrent R765-6 report was not read.

| Finding | Status at `72816d26` | Evidence |
|---|---|---|
| R766-4-F1 / R765-4-F1 (MINOR; Conformance, Docs), stage 3's Removes cell | **Still resolved** | Branch lines are byte-identical to round 5 (`receipts/dev_to_head.lines`) |
| R766-3-RESIDUE-2 / R765-3-R1 | **Still resolved**, verbatim at `MARK_II_AREA_PLAN.md:239` | `receipts/prior_findings_at_head.txt` |
| R765-2-RESIDUE-1 | **Still resolved**, verbatim at `:368` | same |
| R765-2-RESIDUE-2 | **Still resolved**, verbatim in the census row at `:336` | same |
| R765-4-S1 (the M8a-1 link) | **Still taken**, at `:231` | same |
| R765-3-F1, R766-3-RESIDUE-1, R766-2-F1, R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | **Still resolved**: no branch line changed since round 5 | `receipts/dev_to_head.lines` = `receipts/base_to_r5.lines` |
| R765-5 findings | R765-5 raised no new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION at `d85da329`. It also lists R765-2-S3 as resolved at `545ac9cb`, and that is **still resolved** here: no branch line changed since round 5 | R765-5 report, "Findings" and its prior-findings table; `receipts/dev_to_head.lines` |

## Real limits

- I re-ran the census, inventory, the docs.yml page gates, em-dash and `diff --check` at the head. I did **not** re-run the docs.yml builder legs (docs-gates-1/2), behave, the gate readers or the wire-accountability job. For those I rely on the author's published receipts, which match the manifest.
- **Hosted evidence at this exact head is not a pass.** The `rtl-fast`, `elaborate`, `rtl-full` and `docs` runs at `72816d26` were all **cancelled** at 2026-11-08 09:22Z. In `docs`, wire-accountability and docs-check-no-git succeeded, docs-gates-0/1/2 were cancelled with later steps skipped, and the docs-check aggregate concluded failure after those cancellations (`receipts/hosted_runs_head.txt`, `receipts/hosted_docs_jobs_head.txt`, `receipts/hosted_docs_nonsuccess_steps.txt`). These are cancelled and skipped contexts, not executed passes, and I draw no conclusion from them.
- No manager source bank, builder bank or act run is claimed or inferred. Physical calibration was not run; nothing here is hardware proof.
- The four files in S1 cannot be tied to their private originals from public state alone.

## Pending manager duties

- Hosted/act acceptance at the exact head. Every hosted context at `72816d26` was cancelled, so `rtl-fast` and the docs workflow need an executed exact-head verdict (or the act replica) before merge.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. This round validates the source head only.
- Carry R766-6-RESIDUE-1 to the residue checklist. Optionally pass S1 to the evidence packaging.
- Merge needs explicit maintainer authorization.

R766-6 FINISHED
