[R766] POSITIVE - exact head e70ae2cb2dd0746060612493cb6724522b8701bc

# R766-7: external cleared-context review of issue #640 / PR #835, round 7

Head `e70ae2cb2dd0746060612493cb6724522b8701bc`, tree `b88ec0fa4ad541d5250688664459dcfd68089097`. Previously reviewed head: `72816d26a7e2a29db5bc198ff65056ee4c5790b4` (round 6, POSITIVE). Validation base: live dev `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`. Source base of the lane: `503bc97cd4f24ad07596c17e7188f2024617972d`.

This is a delta review. The round is a sync only: one merge of dev `ac0a01e3` (PR #852, issue #851) into `72816d26`. Code and prose that the delta does not touch keep their round 6 lens verdicts, because nothing they depend on changed (shown below).

## Order of reconstruction

1. AGENTS.md and CONTRIBUTING.md (review, lens, ledger and completion rules); docs/README.md.
2. Issue #640: the frozen acceptance and scope as reviewed in rounds 1 to 6. Comments posted since round 6 are only the round 7 TAKEN (`issuecomment-6731392443`) and REVIEW READY (`issuecomment-6732066141`). Neither changes scope or acceptance (`receipts/issue640_comments_since_r6.tsv`).
3. Interface authorities the branch cites: `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md`, `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`, `syn/ooc/pp_resource_baseline.json`, NFR-RES-01, each at `0a75aa77` and at `ac0a01e3`.
4. Merge topology, `git diff ac0a01e3..e70ae2cb`, and the line sets against round 6.
5. Public executable evidence: `review-evidence/640-m10-r1/author-r7` on `640-m10-review-evidence` at `9d0b7479` (its ancestor `3c9d980e` is the commit named in the review request), the publisher's `MANIFEST.json`, and hosted runs at the exact head.
6. Only after my verdict and ledger were drafted: prior public findings (my R766-6 at `issuecomment-6719945800`, the R765-6 report at `issuecomment-6719846258`) and the current PR body. I did not read the concurrent R765-7 report.

## Focus checks

### (1) The merge is a plain merge and the branch lines did not change

- `e70ae2cb` has exactly two parents, `72816d26` (the round 6 head, unchanged) and `ac0a01e3` (live `origin/dev`). `git rev-list 72816d26..e70ae2cb --not ac0a01e3` returns only the merge commit, so there was no rebase and no extra commit. The message is one line with no trailers.
- `git diff --stat ac0a01e3 e70ae2cb` names exactly four files: `AREA_BUDGET.md` (8), `MAILBOX_SPLIT.md` (64), `MARK_II_AREA_PLAN.md` (210) and `docs/findings/README.md` (2). That is 231 lines added and 53 removed. The stat is identical to round 6's `git diff --stat 0a75aa77 72816d26` (`receipts/diff_dev_head.stat`, `receipts/diff_prevdev_prevhead.stat`).
- The sorted `+`/`-` line sets of `git diff -U0 0a75aa77 72816d26` and `git diff -U0 ac0a01e3 e70ae2cb` are **byte-identical**, 284 lines each (`receipts/lines_r6.txt`, `receipts/lines_r7.txt`, empty `receipts/lines_r6_vs_r7.diff`). So the branch adds the same lines, and replaces the same dev lines, as in round 6. No line #851 introduced was overwritten.
- All six gitlinks equal dev's, including `protocol-processor` `044cb25f` and `gptp-processor` `1616fc8f` (`receipts/dev_sync_facts.txt`, `receipts/restore_check.txt`).

### (2) The conflict resolution keeps both rows exactly

- `git merge-tree --write-tree 72816d26 ac0a01e3` reports exactly one content conflict, in `docs/findings/README.md`. `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` auto-merged (`receipts/merge_tree.txt`).
- Against that automatic tree, the head differs only by replacing the conflict block with dev's 234 row followed by the branch's 649 row (`receipts/conflict_resolution.diff`).
- Row hashes (`receipts/readme_rows.txt`): the head's 234 row = dev `ac0a01e3`'s (`0c76274d…`), and the head's 649 row = `72816d26`'s (`f0beee02…`). The file is 36 lines on every side. The head's README differs from dev's only in the 649 row (`docs/findings/README.md:26`), as in round 6.

### (3) Figures cited from the area pages still match dev `ac0a01e3`

- #851 moved these figures in `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md` and the baseline (`receipts/dev851_area_pages.diff`): the route record went from #843 to #851, the processor from `92100657` to `044cb25f`, LUTs from 53,221 to 53,428 (83.94 % to 84.27 %), FFs from 54,754 to 54,837, slices from 15,834 to 15,829 (16 free to 21 free), WNS/WHS from +0.242/+0.012 to +0.210/+0.036 ns, and the ordinal to the fifteenth record.
- None of those figures, pins, issue numbers or ordinals occurs in any of the branch's 231 added lines (`receipts/moved_figure_grep.txt`).
- I also ran a mechanical sweep. It took all 113 distinct numeric tokens in the branch's added lines and tested each for presence in the five area sources at `0a75aa77` and at `ac0a01e3`. No token's presence changed (`receipts/figure_moves.txt` is empty).
- The branch's figures come from the 2026-10-31 basis build and from NFR-RES-01, and dev left both unchanged. The census table's LUT figures are the basis's placed rows (`MARK_II_AREA_PLAN.md:302`). The branch's `AREA_BUDGET.md:140-141` and `:260-262` cite only the NFR-RES-01 target. Dev's new record lines (`AREA_BUDGET.md:149-159`, `:221-237`; `MARK_II_AREA_PLAN.md:61`, `:1099-1100`) sit beside the branch text and read coherently.

### (4) The docs gates pass at this head per the receipts, and my own spot-checks agree

- The author receipts (`author-r7/evidence/gates/verify.md`): 65 docs.yml `run:` steps ran on fresh clones of `e70ae2cb`, all rc 0. 31 hosted-only steps were not run, each with a stated reason, and the verifier exited 0. All 79 `.rc` files read 0. Every full log's first line names the head; the two 20,000-byte tails are recorded with size and sha256 in `LARGE_LOGS.txt`. Every job's tree status after the run is empty (`receipts/author_r7_rc_summary.txt`). Lane steps:
  - `docs_inventory.py --check`: OK, 547 lines, audit fresh.
  - `check_doc_style.py`: OK, 24 documents.
  - behave: 14 features, 508 scenarios, 2,330 steps passed.
  - `check_em_dash --base ac0a01e3`: 0 findings over 231 added lines.
  - `git diff --check` against both bases: clean.
  - `pp_resource_gate.py check-baseline`: PASS.
- My own spot-checks at the head, in this clone (`receipts/probe/`):
  - `docs_inventory.py --check`: rc 0, the same "547 lines … fresh".
  - `check_doc_style.py`: rc 0, 24 documents.
  - `git diff --check ac0a01e3 HEAD`: rc 0.
  - `pp_resource_gate.py check-baseline`: rc 0, "baseline PASS: 3 endpoints".
- `check_em_dash` refused with rc 2, because the pinned Markdown renderer is not installed here. That is a refusal, not a pass, and I rely on the author's receipt for it.
- My behave run ended 11 passed, 1 failed, 2 errored. Every failure and error says the `protocol-processor` or `gptp-processor` submodule is not checked out (my clone has no submodule checkouts). This is environmental. The head's non-Markdown content equals dev `ac0a01e3`'s byte for byte (focus check 1), so behave's outcome here equals dev's. The author's clean-clone run with submodules initialized passed 508 of 508.

### Receipt integrity

- All 197 published `author-r7` files match the publisher manifest's `published_sha256`, and no unlisted file is present. 76 carry path redaction.
- For 191 files, the author's own `SHA256SUMS` equals the manifest's `original_sha256`. The same four files as in round 6 do not match: `lane__census_coverage.log`, `lane__census_coverage_control.log`, `tools/run_docs_yml.py` and `tools/run_extra.sh` (`receipts/author_r7_manifest_check.txt`).
- Run directly against the published bytes, the author's sums fail on exactly the 75 files that carry a redaction token (`$VALIDATION_STORAGE` or `$LANES`), and on no other file (`receipts/author_r7_redaction_consistency.txt`, `receipts/author_r7_sha256_check.txt`). See S1.

### Hosted evidence at the exact head (inspected, not accepted)

At query time (`receipts/hosted_runs_head.txt`, `receipts/hosted_jobs_head.txt`):

- `rtl-fast` 42560928946: completed, success.
- `elaborate`: completed, success.
- `docs`: completed, success, with all 9 jobs succeeding.
- `rtl-full`: **in progress**. 34 jobs had succeeded, 1 was skipped and 1 was still running.

The skipped job is a skipped context, not a pass. Hosted and act acceptance stays with the manager.

### Comment rule

The delta against dev changes no source file, so it adds no source comment and introduces no lane, round, reviewer or comment-ID label in source. The PR body names reviewer IDs and comment IDs, which is allowed in PR text.

## Findings

No BLOCKER, MAJOR, MINOR or new RESIDUE at this head.

### R766-7-S1 (SUGGESTION; Tests, Docs): evidence hash chain, retained from R766-6-S1

- **Where:** `review-evidence/640-m10-r1/author-r7/evidence/SHA256SUMS` against `review-evidence/640-m10-r1/MANIFEST.json` at `9d0b7479`.
- **Evidence:** the same four files as in round 6 have author sums that differ from the manifest's `original_sha256`. All four carry private paths that were redacted. `SHA256SUMS` lists `PR-BODY.md`, which is not published, and omits `HANDOFF.md` (HANDOFF.md:186 states both).
- **Impact:** none on this PR. Every published byte matches the manifest, and the census result those two logs record cannot have changed. The branch lines and dev's `sw/litex/milan_soc.py` are both unchanged since round 6, and round 6 reproduced the result independently. Still, a cold reader cannot tie those four published files to the author's own sums.
- **Suggested outcome:** compute the author sums after the final path normalization, or record the normalization that produced `original_sha256`.
- **Verification:** `sha256sum -c` on the published packet, plus the manifest comparison in `receipts/author_r7_manifest_check.txt`.

## Prior public findings at this head

| Finding | Status at `e70ae2cb` | Evidence |
|---|---|---|
| R766-6-RESIDUE-1 / R765-6-R1 (RESIDUE; Docs): the PR body's reference bullet pinned `503bc97c` | **Resolved**. The bullet now reads "… at `ac0a01e3`, the merge base; since `503bc97c` only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` changed, by dev's #845, #843 and #851 records". I checked that claim: of the six listed pages, only those two differ between `503bc97c` and `ac0a01e3`, and the merges touching them are PR #847 (#845), PR #846 (#843) and PR #852 (#851) | `receipts/pr835_body.md:187`, `receipts/ref_pages_since_503bc97c.txt`, `receipts/dev_sync_facts.txt` |
| R766-6-S1 / R765-6-S1 (SUGGESTION): author sums vs manifest originals | **Retained** as R766-7-S1, with the same four files | `receipts/author_r7_manifest_check.txt` |
| R765-6-S2 (SUGGESTION; Docs, dev-owned): `MARK_II_AREA_PLAN.md:73` says "The shipping image measures 52,008 LUTs" in the present tense | **Retained, out of scope.** The line is dev's, unchanged at `0a75aa77`, `ac0a01e3` and the head, and a sync must not edit it. It now trails dev's record by more (53,428 LUTs at `AREA_BUDGET.md:151`) | `receipts/prior_suggestions_at_head.txt` |
| R765-6-S3 (SUGGESTION; Conformance, non-normative): the 31.0k start estimate rests on the 2026-10-31 basis | **Retained.** The branch still labels it an estimate from that basis (`MARK_II_AREA_PLAN.md:40`, `:153`). Dev's record grew a further 207 LUTs with #851. The switch-over lane's routed image re-measures | same |
| All earlier findings (R765-1…R765-5, R766-1…R766-5), as itemised in my R766-6 table | **Still resolved.** No branch line changed since round 6 | `receipts/lines_r6_vs_r7.diff` (empty) |

## Per-lens results at `e70ae2cb`

| Lens | Result | Artifact and what was checked |
|---|---|---|
| Conformance | PASS | `receipts/lines_r6.txt` = `receipts/lines_r7.txt`, so the branch's claims are the ones round 6 cleared against #640's frozen acceptance and NFR-RES-01. `receipts/moved_figure_grep.txt` and the empty `receipts/figure_moves.txt`: no branch line cites a figure #851 moved. `AREA_BUDGET.md:140-141`, `:260-262` and `MARK_II_AREA_PLAN.md:38-47`, `:151-153`, `:302` still cite only the unchanged basis and NFR-RES-01. S3 is retained as a suggestion |
| RTL | PASS | `receipts/diff_dev_head.stat`: four `.md` files and no `hdl/`, `sw/`, `syn/`, `tb/`, script or generator path. The gitlinks equal dev's (`receipts/dev_sync_facts.txt`). So the lens is inapplicable by that artifact, and dev's #851 RTL and pin adoption belong to dev's lane. Round 6's verdict stands |
| Robustness | PASS | The same four-file artifact carries no executable change. The negative paths this round's evidence relies on still fail as they should: the author's census control (`lane__census_coverage_control`, inverted, rc 0), the style-probe control, and my renderer-absent `check_em_dash` refusal (rc 2, `receipts/probe/em_dash.*`). The em-dash refusal is a refusal, not a pass |
| Tests | PASS | `author-r7/evidence/gates/verify.md`: 65 steps rc 0, 31 not run with reasons, 0 bad. My reproductions in `receipts/probe/`: inventory, doc-style, `diff --check` and check-baseline all rc 0. Behave's failures here are environmental only (missing submodule checkouts), and the author's run passed 508 of 508. The author receipts tie to the manifest (`receipts/author_r7_manifest_check.txt`). S1 is optional |
| Docs | PASS | `docs/findings/README.md:25-26` keeps both rows exactly (`receipts/readme_rows.txt`). The merged `AREA_BUDGET.md:137-262` and `MARK_II_AREA_PLAN.md:59-61`, `:1097-1100` read coherently. `docs_inventory.py --check` is fresh (`receipts/probe/inventory_check.log`). The PR body's sync section and reference bullet are accurate (`receipts/pr835_body.md:144-187`). R766-6-RESIDUE-1 is resolved |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #640 acceptance (unchanged since round 6); `receipts/lines_r6.txt` = `receipts/lines_r7.txt`; `receipts/moved_figure_grep.txt`; `receipts/figure_moves.txt`; `receipts/dev851_area_pages.diff`; `AREA_BUDGET.md:140-141,260-262`; `MARK_II_AREA_PLAN.md:38-47,151-153,302` | R766-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| RTL | CLEAN | `receipts/diff_dev_head.stat` (four `.md` only); `receipts/dev_sync_facts.txt` (gitlinks = dev) | R766-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| Robustness | CLEAN | `receipts/diff_dev_head.stat`; author `lane__census_coverage_control.*`, `lane__style_merge_new_control.*`; `receipts/probe/em_dash.*` | R766-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| Tests | CLEAN (S1 optional) | `author-r7/evidence/gates/verify.md`, `receipts/author_r7_rc_summary.txt`, `receipts/author_r7_manifest_check.txt`, `receipts/probe/*` | R766-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| Docs | CLEAN | `docs/findings/README.md:25-26`; `receipts/readme_rows.txt`; `receipts/conflict_resolution.diff`; `AREA_BUDGET.md:137-262`; `MARK_II_AREA_PLAN.md:59-61,1097-1100`; `receipts/probe/inventory_check.log`, `receipts/probe/doc_style.log`; PR #835 body (`receipts/pr835_body.md`) | R766-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |

## Real limits

- I did not re-run the docs.yml builder legs (docs-gates-1/2), the docs-gates-0 page gates, the wire-accountability job or the census coverage check. For those I rely on the author's published receipts, which match the manifest.
- My behave run lacked submodule checkouts, and my em-dash check lacked the pinned renderer. Neither is a pass by me.
- The four files in S1 cannot be tied to their private originals from public state alone.
- `rtl-full` at this head was still in progress when I queried it, and one of its jobs was skipped. I draw no acceptance conclusion from hosted runs. I did not check the `verilator-suites` and `yosys-portability` contexts by name.
- I claim or infer no manager source bank, builder bank or act run. Physical calibration was NOT RUN, and nothing here is hardware proof.
- I did not read the concurrent R765-7 report.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the `rtl-full` run still in progress and the exact-head `verilator-suites` / `yosys-portability` evidence the completion bar names.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, from source base `503bc97c` with live dev `ac0a01e3` (or a later dev), and link its receipts on the PR.
- Optionally pass S1 to evidence packaging. R765-6-S2 is for a later docs lane on dev-owned lines.
- Merge requires explicit maintainer authorization.

## Restore

After the probes, the clone is at `e70ae2cb`, tree `b88ec0fa`. The index writes the same tree, `git status --porcelain --ignored` is empty (a probe-created `scripts/__pycache__/` was removed), and the six gitlinks are unchanged (`receipts/restore_check.txt`). `scripts/r766_7_checks.sh` re-runs focus checks (1) to (3) against any clone.

R766-7 FINISHED
