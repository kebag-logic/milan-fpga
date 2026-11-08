[R765] POSITIVE - exact head 72816d26a7e2a29db5bc198ff65056ee4c5790b4

Round R765-6: internal independent review for issue #640 / PR #835. This is a delta review of the sync merge of dev `0a75aa77` onto round 5's head `d85da329`. Tree `f9498ee5a4a88bf63453a3a2d162a1b225a7715e`. Source base `503bc97cd4f24ad07596c17e7188f2024617972d`, live dev `0a75aa774b89ac89351700f63dd8cbb89694af6c`.

## Verdict summary

- The merge keeps both sides. Against dev `0a75aa77`, the head differs only in the branch's four pages. Its added and removed lines are byte-identical to the round 5 delta against `503bc97c`: 284 `+`/`-` lines, compared with `cmp`.
- The one conflict, `docs/findings/README.md:25-26`, keeps dev's 234 row and the branch's 649 row. I checked both by line hash.
- The branch's figures still match what dev records. The census check passes against dev's `sw/litex/milan_soc.py`, the round 1 control fails, and a new mutation probe fails.
- `docs_inventory.py --check` is fresh. Every docs gate I re-ran at the head exits 0.
- No open BLOCKER, MAJOR or MINOR. There is one RESIDUE and three SUGGESTIONs.
- The hosted exact-head runs did not execute. A tool download returned HTTP 504 and fail-fast cancelled the runs. That is a pending manager duty, not a finding against the PR.

## Reconstruction (order followed)

1. AGENTS.md (sections 5 to 8) and the brief's frozen scope: a docs-only sync, Docs and Conformance primary, no RTL, firmware or generator change.
2. Normative authority: `docs/reference/FR_NFR.md:473` NFR-RES-01 says fewer than 20,000 LUTs at 32x32, MUST fit Block RAM and meet the timing gate. This is checked against the branch's `AREA_BUDGET.md:137-138` and `:235-237`.
3. Diff and history: `git diff 503bc97c..72816d26`, the merge parents `d85da329` and `0a75aa77`, and dev's own changes to the branch's pages (`503bc97c..0a75aa77`).
4. Public executable evidence: evidence commit `b6694157`, `review-evidence/640-m10-r1/author-r6/`, checked against `review-evidence/640-m10-r1/MANIFEST.json`.
5. Prior public findings were read only after the verdict and ledger below were written (see "Prior findings").

## Check 1: merge resolution and delta identity

| Probe | Result | Receipt |
|---|---|---|
| `merge-base(d85da329, 503bc97c)` and `merge-base(d85da329, 0a75aa77)` | both `503bc97c`; `503bc97c` is an ancestor of `0a75aa77` | (git transcript, this report) |
| `git diff --stat 0a75aa77 HEAD` vs `git diff --stat 503bc97c d85da329` | identical: `AREA_BUDGET.md` 8, `MAILBOX_SPLIT.md` 64, `MARK_II_AREA_PLAN.md` 210, `findings/README.md` 2; 231+ / 53- | `receipts/diff_r5_base_to_prev.patch`, `receipts/diff_r6_dev_to_head.patch` |
| `+`/`-` line sets of the two `-U0` diffs | `cmp` equal, 284 lines each; the patches differ only in `index` lines and three hunk offsets (`AREA_BUDGET.md` @129->@137, @180->@235) | `receipts/lines_r5_base_to_prev.txt`, `receipts/lines_r6_dev_to_head.txt` |
| `docs/findings/README.md` rows 25 and 26, sha256 of each line | row 25 at head = dev's; row 26 at head = branch's; nothing else in the file differs from dev | hashes below |
| What dev changed in the branch's pages | `MARK_II_AREA_PLAN.md:61` (+0.440 -> +0.242 ns record) and `:1097-1099` (#845, #843 records); `AREA_BUDGET.md` record lines (`:124-131`, `:141`, table `:145-149`); `MAILBOX_SPLIT.md` not changed by dev | `git diff 503bc97c 0a75aa77 -- <pages>` |

Row hashes (sha256 prefix, `docs/findings/README.md`): `503bc97c` 25=b8bccc9f 26=b57288b2; `0a75aa77` 25=40dfd7fb 26=b57288b2; `d85da329` 25=b8bccc9f 26=63012dad; `72816d26` 25=40dfd7fb 26=63012dad.

## Check 2: the branch's claims against the merged dev

- **Area figures.** The branch's added lines in `MARK_II_AREA_PLAN.md` cite the measured basis: 52,008 LUTs, the SoC CPU row 3,249, and the derived 34,223 / 30,974 / 27,224. Dev still records that basis at `MARK_II_AREA_PLAN.md:38`, `:90`, `:111` and `:146`, in lines the merge did not touch.
  - No branch-added line cites the gate record (+0.440 / +0.242 ns), #799's 52,012 anchor, or #843's 53,221 anchor. I grepped the added lines of `git diff -U0 0a75aa77 HEAD` for LUT, slice, ns and record figures. Only 20,000, 27,224 and the CPU row hash appear.
  - The derived chain re-adds correctly: 34,223 - 3,249 = 30,974; 30,974 - 3,750 = 27,224; 3,948 - 3,249 = 699. The lever table steps are 30.0 / 29.0 / 27.2 / 27.2 / 26.2 / 21.0k.
- **Gate figures.** In `AREA_BUDGET.md:137-138` and `:235-237`, the branch's NFR-RES-01 sentences match `FR_NFR.md:473`: fewer than 20,000 LUTs at 32x32, fit Block RAM, timing met.
  - Dev's adjacent lines read coherently with them. `:139-140` gives the 60 % target, 38,040 LUTs, and "the #799 route was 13,972 over it" (52,012 - 38,040 = 13,972, history). The `:145-149` table is #843's 53,221 route.
  - `syn/ooc/pp_resource_gate.py check-baseline` at the head: `baseline PASS: 3 endpoints`, rc 0 (`receipts/gates/check_baseline.log`).
- **Census.** I ran the published tool `author-r2/evidence/census/census_coverage.py` (evidence commit `b6694157`) with the published basis inputs. It is read-only, as inspected.
  - At the head, against dev's `sw/litex/milan_soc.py` (blob equal to dev's; dev changed it by 33 lines for #829's MII launch shape): `RESULT: PASS`, rc 0, 23 rows, every row hit (`receipts/census_head.out`, `.rc`).
  - Control, the round 1 page `3f8ed303` with the head's `milan_soc.py`: rc 1, ten MISSING rows (`receipts/census_control_r1.out`).
  - New mutation, the head page with `self.ev = EventManager()` removed from `milan_soc.py`: rc 1, `NOT BUILT` (`receipts/census_mut_soc.out`).
  - My head and control outputs are byte-identical to the bodies of the author's published `lane__census_coverage.log` and `lane__census_coverage_control.log` after their header line (`receipts/census_head_vs_published.diff`, `receipts/census_control_vs_published.diff`, both empty).
- **Dev's `milan_soc.py` delta.** It adds `_PHY_MODEL_LAUNCH` and `_PHY_MODEL_OBSERVER` parameters and the observer's `gmii_tready_i` wiring. No new LiteX object, so the census's object set is unchanged (`receipts/dev_milan_soc_delta.diff`).

## Check 3: docs workflow at the head

My re-runs at `72816d26`, logs and rc under `receipts/gates/`. Each log's first line names the head.

| Gate (docs.yml step) | Command | rc | Result line |
|---|---|---:|---|
| gate_46 inventory freshness | `scripts/docs_inventory.py --check` | 0 | `documentation inventory: OK (547 lines, docs/DOCUMENTATION_AUDIT.md is fresh)` |
| gate_46 | `scripts/docs_inventory.py --selftest` | 0 | `OK (60 controls)` |
| gate_45 per-page contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` (pinned renderer from `tools/markdown/requirements.txt`, hash-locked, scratch venv) | 0, 0, 0 | `1501/1501 arm(s)`; `598 ... fragment links reproduced`; `TOC gate: OK (152 page(s) ...)` |
| gate_7 link health / wording / local-info | `scripts/docs_check.py` | 0 | `0 finding(s) across 214 md files + 1448 scrubbed text files` |
| gate_8 em-dash | `check_em_dash.py --base 0a75aa77` / `--base 503bc97c` | 0 / 0 | `0 finding(s) over 231 added line(s) in 4 ... pages`; `0 ... over 2287 added line(s) in 33 ... pages` |
| gate_9 concise style | `scripts/check_doc_style.py` | 0 | `OK (24 current documents)` |
| gate_43 cited paths | `scripts/check_doc_paths.py` | 0 | `OK (1638 cited paths all resolve ...)` |
| gate_16 traceability | `docs/traceability/gen_module_matrix.py --check` | 0 | `up to date (80 modules ...)` |
| rtl-fast reader | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | `baseline PASS: 3 endpoints` |

Without the pinned renderer, `gen_toc` and `check_em_dash` refuse with rc 2 ("the pinned Markdown renderer is not installed"). Those first attempts were superseded by the rows above. Their logs were overwritten, so only the final runs are receipts.

In the five renderer-run logs, the interpreter path in the header line is written as `$PACKET/scratch/venv/bin/python`. Every published receipt and script is listed in `MANIFEST.sha256`.

The author's full local docs workflow (`author-r6/evidence/gates/verify.md`) records 96 rows: 65 rc 0, 31 NOT RUN each with a reason, 0 bad. Its gate logs name head `72816d26`.

I spot-checked it rather than re-running the builder legs. My re-runs above agree with its rows for the same steps.

**Receipt integrity.** All 201 published `author-r6` files match `MANIFEST.json` `published_sha256` (`receipts/author_r6_manifest_verify.txt`; script `scripts/verify_author_r6.py`).

The author's `SHA256SUMS` matches `original_sha256` for every file except four. It also lists `PR-BODY.md`, which is not published (S1).

## Hosted exact-head evidence (inspected, not accepted; the manager owns it)

Four workflow runs at `72816d26`: rtl-fast `42466664474`, elaborate `42466664507`, rtl-full `42466664477`, docs `42466664495`. All are concluded `cancelled` (`receipts/hosted_runs_72816d26.tsv`). Of 68 check runs: 13 success, 13 failure, 41 cancelled, 1 skipped (`receipts/hosted_check_runs_72816d26.tsv`).

The first failures were infrastructure: elaborate-gates-4 "Install the pinned sv2v release" and elaborate-gates-3 "Install sbt". Both got `curl: (22) The requested URL returned error: 504` (`receipts/hosted_infra_504_excerpt.txt`, `receipts/hosted_failed_steps.txt`). Fail-fast then cancelled the rest. `docs-check` failed "Require every gate exactly once" because the gates were cancelled.

Executed successes: docs-check-no-git, wire-accountability, bdd-conformance, full-ci-gate, changes. No executed hosted job failed on the PR's content. No exact-head rtl-fast, verilator-suites or yosys-portability verdict exists yet.

## Findings

### R765-6-R1 RESIDUE: PR body names the reference pages only at the old base

- **Lenses:** Docs
- **Where:** PR #835 body, "Authoritative references", last bullet: "`docs/design/MARK_II_AREA_PLAN.md`, ..., `docs/design/AREA_BUDGET.md`, ... at `503bc97c`; NFR-RES-01 and NFR-SCOUT-03 ...".
- **Evidence:** after the sync, dev `0a75aa77` changed `MARK_II_AREA_PLAN.md:61`, `:1097-1099` and `AREA_BUDGET.md`'s record lines. The body's "Sync with dev 0a75aa77" section already says the merged pages were read. Only this bullet still pins `503bc97c`.
- **Impact:** wording only. A cold reader may open the pre-sync pages. No figure, verdict or claim changes.
- **Exact fix:** change "at `503bc97c`;" to "at `503bc97c`, with the merged sections re-read at dev `0a75aa77`;".
- **Verification:** read the body.

### R765-6-S1 SUGGESTION: four author digests differ from the manifest's original digests

- **Lenses:** Docs (evidence packet; outside the PR tree)
- **Where:** `review-evidence/640-m10-r1/author-r6/evidence/SHA256SUMS` against `review-evidence/640-m10-r1/MANIFEST.json`. The four files are:
  - `evidence/gates/logs/lane__census_coverage.log`
  - `evidence/gates/logs/lane__census_coverage_control.log`
  - `evidence/tools/run_docs_yml.py`
  - `evidence/tools/run_extra.sh`
- **Evidence:** for each of these, the author's digest ≠ the manifest's `original_sha256`. These four are exactly the published files that name the private management path. That points to a step of the publishing redaction, not to changed content.
  - The two census logs' bodies are byte-identical to my independent re-run (check 2).
  - `SHA256SUMS` also lists `PR-BODY.md`, which is not in the manifest or the published tree. The manifest covers 201 files, the same 201 that are published.
- **Impact:** the author-to-manifest digest chain cannot be followed for those four files. Their content claims were reproduced independently, so no conclusion of this review rests on them.
- **Suggested outcome:** the publisher records the raw-byte original digest for multi-stage redactions, or notes the stage it hashed. It also notes the deliberately unpublished `PR-BODY.md`.
- **Verification:** `python3 -I scripts/verify_author_r6.py <MANIFEST.json> <640-m10-r1 dir> author-r6` exits 0.

### R765-6-S2 SUGGESTION: a dev-owned present-tense sentence now trails dev's own record

- **Lenses:** Docs (dev-owned line, not in this delta)
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:73`: "The shipping image measures 52,008 LUTs, 82.03 percent."
- **Evidence:** this line is identical at `503bc97c`, `0a75aa77` and the head. It describes the 2026-10-31 basis build (`40b77bbd`, `:78-81`). Dev's own `:1099` and `AREA_BUDGET.md:147` now record the shipping route at 53,221 LUTs (83.94 %).
- **Impact:** a reader may take 52,008 as today's shipping figure. No branch claim depends on the sentence.
- **Suggested outcome:** a later docs lane writes "The measured basis image, 2026-10-31, used 52,008 LUTs". Out of scope for this sync, which must not change dev's lines.
- **Verification:** read the page.

### R765-6-S3 SUGGESTION: the Mark II start estimate rests on a basis older than dev's latest growth

- **Lenses:** Conformance (estimate provenance; non-normative)
- **Where:** the branch's `MARK_II_AREA_PLAN.md:40-47` and `:151-153` (start estimate 31.0k), against `:1097-1099` (#845 52,529, #843 53,221).
- **Evidence:** the plan derives from the fixed 2026-10-31 basis, and it says so. Dev's gate record has since grown by 1,209 LUTs from 52,012, partly in blocks the plan removes (processor) or moves (gPTP, lever 6).
- **Impact:** none on the branch's claims. They are labelled estimates from that basis. The switch-over lane's routed image re-measures.
- **Suggested outcome:** the switch-over lane re-derives the start estimate from its own routed image. Optionally, the plan names that re-derivation next to the #843 anchor.
- **Verification:** the switch-over lane's receipts.

**Comment rule.** The reviewed delta has no source-code or source-comment change (four Markdown pages only), so it contains no new comment-rule instance. Lane and round labels in `MARK_II_AREA_PLAN.md` (for example "S2b round 11/12") are unchanged since round 5 and sit in design prose, not source comments.

## Lens results (findings format)

- [R765] PASS Conformance: `docs/design/AREA_BUDGET.md:137-138,235-237` against `docs/reference/FR_NFR.md:473` NFR-RES-01. Also `MARK_II_AREA_PLAN.md:38,90,111,146` (the basis dev still records) and the branch's derived chain `:151-153,164-172,190-195`, re-added by hand. The census at the head passes against dev's `sw/litex/milan_soc.py`, the control fails, and the mutation fails. S3 is a suggestion only.
- [R765] PASS RTL: `git diff --stat 0a75aa77 72816d26` names only four Markdown pages. No `hdl/`, `sw/`, `syn/`, `tb/` or `scripts/` path differs from dev. The merge brings dev's RTL unchanged, and dev's own lanes own it. The branch's RTL-scope prose (the census rows on CDC, `PSCLK`, `ICAPE2`) is byte-identical to round 5.
- [R765] PASS Robustness: the same four-page diff carries no executable artifact. The negative paths that this delta's evidence depends on were exercised: the census control rc 1, a new mutation rc 1, and the renderer-absent refusal rc 2 of `gen_toc` and `check_em_dash`.
- [R765] PASS Tests: no test or generator file is in the delta. The tests that read the branch's pages pass at the head: `pp_resource_gate.py check-baseline`, `docs_inventory.py --check/--selftest`, `gen_toc.py` x3, `check_em_dash.py` x2, `docs_check.py`, `check_doc_paths.py`, `check_doc_style.py` and `gen_module_matrix.py --check`. The author's 65-step docs workflow record has 0 bad, and the census tool can fail (control, mutation).
- [R765] PASS Docs: `docs/findings/README.md:25-26` keeps both sides (line hashes). The four pages' `+`/`-` sets equal round 5's (`cmp`). The audit page is fresh (`docs_inventory.py --check`), and the merged sections of `AREA_BUDGET.md:112-149` and `MARK_II_AREA_PLAN.md:58-61,1093-1100` read coherently. R1 is RESIDUE (wording); S1 and S2 are suggestions.

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `AREA_BUDGET.md:137-138,235-237`; `FR_NFR.md:473`; `MARK_II_AREA_PLAN.md:38-47,90,111,146-195`; census at head plus control plus mutation | R765-6 | 72816d26a7e2a29db5bc198ff65056ee4c5790b4 |
| RTL | CLEAN | `git diff --stat 0a75aa77 72816d26` (four `.md` only); round 5's RTL-scope prose unchanged (`cmp` of line sets) | R765-6 (delta); content unchanged since R765-5 | 72816d26a7e2a29db5bc198ff65056ee4c5790b4 |
| Robustness | CLEAN | same diff; census control and mutation; renderer-absent refusals | R765-6 (delta); content unchanged since R765-5 | 72816d26a7e2a29db5bc198ff65056ee4c5790b4 |
| Tests | CLEAN | `receipts/gates/*.log` (gates rc 0); `author-r6/evidence/gates/verify.md` (65 rc 0, 31 NOT RUN with reasons); census tool's failure arms | R765-6 | 72816d26a7e2a29db5bc198ff65056ee4c5790b4 |
| Docs | CLEAN (RESIDUE R1 carried) | `docs/findings/README.md:25-26`; four-page line-set identity; `docs_inventory.py --check`; merged sections of `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md`; PR body | R765-6 | 72816d26a7e2a29db5bc198ff65056ee4c5790b4 |

## Prior findings

I read these after the verdict and ledger above were written (`receipts/order_marker.txt`). Sources:

- the published R765-5 and R766-5 reports, both POSITIVE at `d85da329` (evidence commit `b6694157`, `reviews/R765-5/REPORT.md`, `reviews/R766-5/REPORT.md`);
- PR #835 comments since 2026-11-04: only the two review-start notices for R765-6 and R766-6, and no new finding (`receipts/pr835_comments_since_r5.tsv`).

`MARK_II_AREA_PLAN.md` lines 1 to 1096 at the head equal `d85da329`'s, except dev's `:61` (diff of those lines). So every prior finding's cited line keeps its number and bytes.

| Prior finding | Status at `72816d26` | Evidence |
|---|---|---|
| R765-4-F1 / R766-4-F1 (MINOR; Conformance, Docs): stage 3's Removes cell | **Still resolved** | `:233` unchanged from `d85da329` |
| R766-3-RESIDUE-2 / R765-3-R1 (`:239`), R765-2-RESIDUE-1 (`:368`), R765-2-RESIDUE-2 (`:336`) | **Still resolved**, fixes intact | `:239` "Until stage 3, `ctrl_memory`'s banks hold both regions."; `:368` "Taking 10 ms as the gap gives 128 bytes."; `:336` unchanged |
| R765-4-S1 (SUGGESTION): the M8a-1 link label | **Still taken** | `:231` unchanged |
| R766-4 SUGGESTION (PR body round 4 row) | **Still taken** | PR body unchanged in that row |
| R765-3-F1, R766-3-RESIDUE-1, R766-2-F1, R765-2-S2/S3, R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | **Still resolved.** The merge changes no branch line, and dev's lines touch none of their statements | four-page line-set identity (check 1) |
| R765-5 / R766-5 next step: re-run the census against current dev | **Done and reproduced** | check 2: PASS at head, control and mutation fail, byte-identical to the author's logs |
| Optional R765-3-S1, R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4, R765-1-S2/S3, R766-1-S2/S3, R766-1-S3 (stage 1 probe figure) | Not taken; optional. **Retained**, no coverage effect | PR body "Not taken, optional"; HANDOFF open list items 8 and 9 |

No prior BLOCKER, MAJOR, MINOR or RESIDUE is open.

## Real limits

- I did not re-run the builder legs (docs-gates-1/2), the docs workflow's HDL-reference build, behave, or the rtl-fast native and firmware banks. For those I rely on the author's published receipts, verified by manifest digest and head line.
- No manager source bank exists at this head, and I claim none.
- Hosted exact-head runs were cancelled after an upstream HTTP 504. No hosted rtl-fast, verilator-suites, yosys-portability or docs-union verdict exists at `72816d26`.
- The census inputs (basis hierarchy, `csr.csv`, placement excerpt) are the published round 2 files. I did not re-derive them from a build.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- No Docker, act, Vivado, hardware or GitHub write was used.

## Pending manager duties

1. Re-run the hosted workflows at `72816d26` (rtl-fast, docs, elaborate, rtl-full; the PR is ready, so this includes exact-head verilator-suites and yosys-portability) and accept them. The 2026-11-08 runs were cancelled on a 504 download.
2. Build and validate the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts.
3. Carry R765-6-R1 to the residue checklist.
4. Optionally act on S1, the publishing digest chain.
5. Obtain the maintainer's merge authorization, then do post-merge containment, close #640 and move it to Done.

## Clone integrity after probes

HEAD `72816d26a7e2a29db5bc198ff65056ee4c5790b4`, tree and `write-tree` `f9498ee5a4a88bf63453a3a2d162a1b225a7715e`. Worktree equals the index, and the index equals HEAD. Porcelain is empty, including ignored files, after the probe `__pycache__` directories were removed.

Blob modes are 1423 × 100644, 49 × 100755 and 6 × 160000. The six gitlinks are equal in tree and index: `external` efeb541a, `gptp-processor` 1616fc8f, `protocol-processor` 92100657, `third_party/lwSRP` 08ee86e8, `third_party/tsn-c-stack` 70936b77, `third_party/verilog-axis` 48ff7a7e (`receipts/clone_integrity.txt`).

R765-6 FINISHED
