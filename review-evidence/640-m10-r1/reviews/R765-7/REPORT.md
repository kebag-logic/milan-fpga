[R765] POSITIVE - exact head e70ae2cb2dd0746060612493cb6724522b8701bc

# R765-7: internal cleared-context review of issue #640 / PR #835, round 7

- Head `e70ae2cb2dd0746060612493cb6724522b8701bc`, tree `b88ec0fa4ad541d5250688664459dcfd68089097`.
- Previous reviewed head (R765-6, POSITIVE): `72816d26a7e2a29db5bc198ff65056ee4c5790b4`.
- Live dev and merge base: `ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36`. Source base: `503bc97cd4f24ad07596c17e7188f2024617972d`.
- Author receipts: evidence commit `3c9d980ef9842a4d5d6dcc8cb91df43c75e18b9b`, `review-evidence/640-m10-r1/author-r7`.

## Verdict summary

This round is a sync and nothing else. The head is a plain two-parent merge of dev `ac0a01e3` into `72816d26`. Its only deviation from the mechanical merge is the one conflict in `docs/findings/README.md`, and that resolution keeps dev's 234 row and the branch's 649 row byte for byte.

Against dev, the head changes the same four pages with the same added and removed line sets as round 6. No branch line cites a figure that #851 moved. Every #851 line on the two area pages survives the auto-merge, and none of the lines #851 removed is still there.

The author's gate receipts name this exact head and exit 0. I re-ran the cheap gates and the census myself and got the same results; the census output is byte-identical to the published logs.

There is one wording RESIDUE in the PR body and no BLOCKER, MAJOR or MINOR. All five lenses are clean at this head.

## Reconstruction (order followed)

1. `AGENTS.md` and `CONTRIBUTING.md` (the review, lens and ledger rules), then `docs/README.md`.
2. Issue #640's frozen body. It was last edited 2026-10-31T16:21:28Z, before round 6, so acceptance is unchanged (`receipts/22_issue_body_edit_state.txt`). I also read the issue comments since 2026-11-08: two daily area measurements, then the `[A720p]` and `[A720q]` TAKEN and REVIEW READY pairs (`receipts/20_gitlinks_and_pr_comments.txt`).
3. NFR-RES-01. `docs/reference/FR_NFR.md` is unchanged from `0a75aa77` to `ac0a01e3`: it is absent from dev's file list in `receipts/02_lineset_compare.txt`.
4. The diff and history: `git diff 503bc97c..e70ae2cb`, `git diff ac0a01e3 e70ae2cb`, the remerge diff, and the first-parent history.
5. The author's r7 receipts, the packet's `MANIFEST.json`, the hosted check-runs at the head, the PR body and the `[A720q]` REVIEW READY comment.
6. Only after my own pass: the published R765-6 and R766-6 reports and the PR comments since round 6 (see "Prior findings").

## Check 1: a plain merge, no other change (`receipts/01`, `02`, `03`)

- **Parents.** `e70ae2cb`'s parents are `72816d26` and `ac0a01e3`, in that order. Both are ancestors of the head, and `ac0a01e3` is the live `refs/heads/dev`. The head is also `refs/pull/835/head`, and `503bc97c` is an ancestor of dev.
- **Remerge diff.** `git show --remerge-diff e70ae2cb` touches only `docs/findings/README.md`, which is the conflict resolution. Nothing else deviates from git's own merge result, so the merge carries no other edit, rebase or amend.
- **Footprint against dev.** `git diff --stat ac0a01e3 e70ae2cb` touches exactly four pages: `AREA_BUDGET.md` 8, `MAILBOX_SPLIT.md` 64, `MARK_II_AREA_PLAN.md` 210 and `findings/README.md` 2. That is 231 lines added and 53 removed, the same stat as round 6's `0a75aa77..72816d26`.
- **Same line sets.** For each page, the `-U0` added and removed lines of `ac0a01e3..e70ae2cb` are byte-identical to those of `0a75aa77..72816d26` (`receipts/02_lineset_compare.txt`).
  - `MAILBOX_SPLIT.md` keeps the same blob, `12b31086`.
  - The other three pages differ in blob only by dev's lines.
- **Gitlinks.** All six gitlinks at the head equal dev's (`receipts/20_gitlinks_and_pr_comments.txt`). Among them are processor `044cb25f` and FPGA-gPTP `1616fc8f`.
- **Commit message.** One line, no trailers.

## Check 2: the conflict resolution keeps both rows exactly (`receipts/03`, `04`)

- The head's `docs/findings/README.md` equals dev's file with exactly one row replaced: the 649 row, which takes the branch's text from `72816d26`. The check is `H == D with P6 649 row: True`, over 36 lines each.
- The 234 row at the head equals dev's 234 row (hash `0c76274d...`, the #851 text). The 649 row at the head equals the branch's 649 row (hash `f0beee02...`).
- Each row occurs exactly once, and no conflict marker remains.

## Check 3: the figures the branch cites still match dev `ac0a01e3` (`receipts/05`, `06`, `07`, `13`, `14`)

- **#851's lines survive.**
  - All 46 lines #851 added to `AREA_BUDGET.md` are present verbatim at the head, and so are its 3 lines in `MARK_II_AREA_PLAN.md`: the +0.210 ns warning row at `:61`, and the #843 and #851 anchor lines at `:1099-1100`.
  - None of #851's removed lines (18 and 2) remains at the head (`receipts/07_dev_lines_at_head.txt`).
- **Branch-owned lines.** The branch owns `MARK_II_AREA_PLAN.md` lines 17-437 only (`receipts/13`). Every gate-record citation on the page (`:486` onward) and `:73` ("The shipping image measures 52,008") is dev-owned.
- **Figures #851 moved.**
  - No branch-added number equals a value #851 removed from its pages or from `syn/ooc/pp_resource_baseline.json`. The only three coincidences are the UART counts 115 and 116 characters and the "232" of `RS232PHY` (`receipts/14`).
  - The branch's area figures are the 2026-10-31 basis (52,008; the CPU row 3,249; the derived 34,223 / 30,974 / 27,224), NFR-RES-01's 20,000 at 32x32, and the #649 page's figures in the 649 row. #851 changed none of them.
- **The branch's AREA_BUDGET sentences.** `AREA_BUDGET.md:140-141` and `:259-262` sit beside dev's new `:149-159` table (53,428 LUT, 84.27 %, 15,829 slices, 21 free, +0.210 / +0.036 ns) and read coherently with it.
  - Dev's `:143` "replaces the earlier 60 percent target" agrees with the 649 row's "NFR-RES-01's former 60 % target".
  - The row's "about 1,200 ... a tenth of the gap" is consistent with the 234 row's 11,917 LUT gap.
- **Anchors.** The 234 row's link `AREA_BUDGET.md#headroom-target` resolves, to `:138`.
- **Baseline record.** `pp_resource_gate.py check-baseline` at the head gives `baseline PASS: 3 endpoints`, rc 0. Its `route-1x1` record is 53,428 LUT, matching dev's `AREA_BUDGET.md:151` and `MARK_II_AREA_PLAN.md:1100` (`receipts/12_probe_check_baseline.*`).

## Check 4: the docs gates at this head (`receipts/08`-`12`, `18`)

- **Head identity.** All 76 author `.log` files open with `# head e70ae2cb2dd0746060612493cb6724522b8701bc`, and all 78 `.rc` files are 0. Every job's tree-after status names the head with an empty status (`receipts/11`).
- **Gate table.** 65 run steps have rc 0. 31 hosted-only steps are NOT RUN, each with a stated reason; these are CI orchestration, package installs and record steps. The two control arms behave as designed:
  - `style_merge_new_control` reports its planted finding;
  - `census_coverage_control` fails.
- **Named gates at the head (author receipts):**
  - `docs_inventory.py --check`: OK, 547 lines, the audit page fresh, rc 0.
  - `check_doc_style.py`: OK, 24 current documents, rc 0.
  - `behave`: 14 features, 508 scenarios and 2,330 steps passed, 0 failed, 0 skipped, rc 0.
  - `check_em_dash.py --base ac0a01e3`: 0 findings over 231 added lines, rc 0.
  - `git diff --check` against `ac0a01e3` and against `0a75aa77`: clean.
  - Both builder legs (`gate_25_0` and `gate_25_1`) exit 0.
- **My own re-runs at the head (`receipts/12_probe_*`):**
  - `docs_inventory.py --check`: OK, 547 lines, rc 0.
  - `check_doc_style.py`: OK, 24 documents, rc 0.
  - `docs_check.py`: 0 findings across 214 md files and 1,448 scrubbed files, rc 0.
  - `git diff --check ac0a01e3 e70ae2cb`: rc 0.
  - `check_em_dash.py` could not judge here (rc 2: the pinned renderer is not installed in this clone). See the limits.
- **behave inputs.** I did not re-run behave. No file under `tests/` reads any of the four pages, and the head's `tests/` tree equals dev's, so behave's inputs at the head are dev's.
- **Census.** I ran the published tool `author-r2/evidence/census/census_coverage.py`, which only reads (inspected), with its published basis inputs (`receipts/18`).
  - At the head: `RESULT: PASS`, rc 0.
  - Control, with round 1's page `3f8ed303` and the head's `milan_soc.py`: `RESULT: FAIL`, rc 1.
  - Both outputs are byte-identical to the bodies of the author's published `lane__census_coverage.log` and `lane__census_coverage_control.log`, after the header line (both `.diff` files are empty).
  - `sw/litex/milan_soc.py` at the head is dev's blob `94e89129`.
- **Receipt hash chain.** My verifier is `scripts/verify_author_r7_chain.py`, with its output in `receipts/09`.
  - All 197 published `author-r7` files match `MANIFEST.json`'s `published_sha256`, and every redaction flag is consistent.
  - Four files' author digests differ from the manifest's `original_sha256`. They are the same four as in round 6 (`receipts/10`, the author-r6 control); see R765-6-S1 below. Two of them are the census logs reproduced above. The other two are runner scripts, and no conclusion here rests on them.
  - The raw `sha256sum -c` in `receipts/08` fails on the 75 redacted files. That is expected, because it compares published bytes against pre-redaction digests.
- **Hosted contexts (inspected, not accepted; the manager owns them; `receipts/15`).** At the head:
  - succeeded: `rtl-fast`, `docs-check`, `docs-check-no-git`, `docs-gates-0/1/2`, `bdd-conformance`, `wire-accountability` and `full-ci-gate`;
  - still in progress: some Verilator and Yosys shards;
  - skipped: "Physical gPTP (nightly and manual)". A skipped context is not executed evidence.

## Findings

### R765-7-R1 RESIDUE: the PR body's provenance sentence leaves out the 649 row's source

- **Lenses:** Docs
- **Where:** PR #835 body, "Sync with dev ac0a01e3": "Corrected figures: none. Every figure the branch's lines cite comes from the 2026-10-31 basis build or NFR-RES-01. Dev changed neither."
- **Evidence:** the branch's changed 649 row in `docs/findings/README.md` also carries the #649 page's figures (3,828 LUT per stream, about 1,200 routed LUT, 59 / 52 / 7 sweep points, 235 against 128). `MAILBOX_SPLIT.md`'s lines carry derived timing figures. Dev `ac0a01e3` changed neither source either, so the substantive claim, that no branch figure moved, holds (check 3).
- **Impact:** wording only. A cold reader could miss the #649 page as a figure source. No figure, verdict or check changes.
- **Exact fix:** "Every area figure the branch's lines cite comes from the 2026-10-31 basis build, NFR-RES-01 or the #649 findings page. Dev changed none of them."
- **Verification:** read the edited sentence.

### R765-6-S1 SUGGESTION, retained: four author digests differ from the manifest's original digests

- **Lenses:** Docs (evidence packet, outside the PR tree)
- **Where:** `author-r7/evidence/SHA256SUMS` against `MANIFEST.json` at `3c9d980e`. The four files are:
  - `gates/logs/lane__census_coverage.log`
  - `gates/logs/lane__census_coverage_control.log`
  - `tools/run_docs_yml.py`
  - `tools/run_extra.sh`
- **Evidence:** this is the same set and the same pattern as in round 6 (`receipts/09`, `10`).
  - The author's HANDOFF states that `SHA256SUMS` is computed last over the final bytes, and that redaction is the publisher's step.
  - These four are the files that name the private management path, so the "original" digest is most likely taken after an intermediate path normalisation.
  - `SHA256SUMS` also lists `PR-BODY.md`, which is not published.
- **Impact:** the author-to-manifest chain cannot be followed for those four files. The two census logs were reproduced byte for byte (check 4), and the two scripts carry no conclusion.
- **Suggested outcome (publisher):** record the raw-byte original digest, or name the normalisation stage that `original_sha256` hashes. Note that `PR-BODY.md` is deliberately unpublished.
- **Verification:** `python3 -I scripts/verify_author_r7_chain.py <repo> <evidence-commit>` exits 0.

### R765-6-S2 SUGGESTION, retained: a dev-owned present-tense sentence trails dev's record further

- **Lenses:** Docs (dev-owned line, not in this delta)
- **Where:** `docs/design/MARK_II_AREA_PLAN.md:73`: "The shipping image measures 52,008 LUTs, 82.03 percent."
- **Evidence:** the line is unchanged and dev-owned. Dev's own `AREA_BUDGET.md:151` and `MARK_II_AREA_PLAN.md:1100` now record the shipping route at 53,428 LUTs (84.27 %).
- **Impact:** a reader may take 52,008 as today's shipping figure. No branch claim depends on it.
- **Suggested outcome:** a later docs lane writes "The measured basis image, 2026-10-31, used 52,008 LUTs". This is out of scope for a sync, which must not change dev's lines.
- **Verification:** read the page.

### R765-6-S3 SUGGESTION, retained: the start estimate rests on a basis older than dev's latest growth

- **Lenses:** Conformance (estimate provenance; non-normative)
- **Where:** the branch's `MARK_II_AREA_PLAN.md:40-47` and `:151-174`, against dev's `:1097-1100`.
- **Evidence:** the plan derives from the fixed 2026-10-31 basis and says so. Dev's gate record has since grown from #799's 52,012 to #851's 53,428, a growth of 1,416 LUTs, partly in the processor that the plan removes.
- **Impact:** none on the branch's claims, which are labelled estimates from that basis.
- **Suggested outcome:** the switch-over lane re-derives the start estimate from its own routed image.
- **Verification:** that lane's receipts.

**Comment rule.** The reviewed delta changes no source file: four Markdown pages only, all unchanged since round 6. It therefore introduces no new source comment and no new lane, round or reviewer label.

## Lens results (findings format)

```text
[R765] PASS Conformance - receipts/02_lineset_compare.txt, receipts/07_dev_lines_at_head.txt, receipts/14_branch_vs_baseline_json.txt, receipts/22_issue_body_edit_state.txt; AREA_BUDGET.md:140-141,259-262 and MARK_II_AREA_PLAN.md:36-47 at e70ae2cb - the sync's acceptance (plain merge, both conflict rows kept, figures current, nothing else changed) is met; the branch's NFR-RES-01 sentences match FR_NFR.md (unchanged by dev); no branch-cited figure was moved by #851; the issue body was frozen since 2026-10-31
[R765] PASS RTL - receipts/01_merge_structure.txt (git diff --stat ac0a01e3 e70ae2cb), receipts/20_gitlinks_and_pr_comments.txt (gitlinks equal dev) - no RTL, generator, constraint or submodule pin differs from dev; the four changed files are Markdown; nothing within the lens's scope exists in the delta
[R765] PASS Robustness - receipts/03_conflict_resolution.txt, receipts/04_conflict_rows.txt, receipts/07_dev_lines_at_head.txt - the merge's failure paths: the conflicted rows are kept exactly (no marker, no dropped row, each row once); the auto-merged pages keep every #851 line and no line #851 removed; no behaviour in the delta has an input, reset or timeout path to examine
[R765] PASS Tests - receipts/11_author_gate_spotcheck.txt, receipts/12_probe_*.log, receipts/18_census_*; author gate_table.md at 3c9d980e - every author receipt names the exact head with rc 0; the controls fail where designed; my re-runs (inventory, style, docs_check, diff --check, check-baseline, census and its control) agree, and the census output is byte-identical to the published logs; behave's inputs equal dev's
[R765] PASS Docs - docs/findings/README.md:25-26, AREA_BUDGET.md:138-159,259-262, MARK_II_AREA_PLAN.md:61,1099-1100 at e70ae2cb; PR #835 body "Sync with dev ac0a01e3" and "Authoritative references" - the pages read coherently with #851's text; the PR body's claims (1 merge and 11 commits; only AREA_BUDGET.md and MARK_II_AREA_PLAN.md changed since 503bc97c, by #845, #843 and #851; milan_soc.py unchanged) are true (receipts/16); the round 6 residue is taken; one wording RESIDUE remains (R765-7-R1)
```

## Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Branch line sets against dev and round 6; NFR-RES-01 sentences against `FR_NFR.md`; #851 figures against branch figures and the baseline JSON; issue body edit state | R765-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| RTL | CLEAN | Diff footprint (four Markdown pages), gitlinks equal to dev, remerge diff | R765-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| Robustness | CLEAN | Conflict resolution (both rows exact), survival of #851's added and removed lines on the auto-merged pages | R765-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| Tests | CLEAN | Author r7 gate receipts and controls; my inventory, style, docs_check, diff-check, check-baseline and census re-runs; behave input identity | R765-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |
| Docs | CLEAN (one RESIDUE, R765-7-R1, carried to the residue list) | Four pages at the head, PR body sync and reference sections, the REVIEW READY comment | R765-7 | `e70ae2cb2dd0746060612493cb6724522b8701bc` |

Every lens is covered at the merge candidate itself. Nothing in any lens's scope changed after this head, because it is the head.

## Prior findings

I read these after the verdict, ledger and findings above were drafted. The sources were the published R765-6 and R766-6 reports (evidence commit `3c9d980e`) and the PR #835 comments since 2026-11-08. The comments are only the R765-6, R766-6 and R765-7 start notices and the two round 6 verdicts; there is no new finding and no PR review (`receipts/20`).

| Prior finding | Status at `e70ae2cb` | Evidence |
|---|---|---|
| R765-6-R1 / R766-6-RESIDUE-1 (RESIDUE, Docs): the reference bullet's base | **Resolved.** PR body line: "at `ac0a01e3`, the merge base; since `503bc97c` only `AREA_BUDGET.md` and `MARK_II_AREA_PLAN.md` changed, by dev's #845, #843 and #851 records" | `receipts/16_pr_body_claims.txt`: the only pages changed among those listed are those two, by merges #847 (#845), #846 (#843) and #852 (#851) |
| R765-6-S1 / R766-6-S1 (SUGGESTION): the evidence hash chain | **Retained**, same four files in author-r7 | `receipts/09`, `10` |
| R765-6-S2 (SUGGESTION): dev's `:73` | **Retained**, now against 53,428 | Check 3 |
| R765-6-S3 (SUGGESTION): start-estimate basis | **Retained**, growth now 1,416 | Check 3 |
| R765-4-F1 / R766-4-F1 (MINOR), R766-3-RESIDUE-2 / R765-3-R1, R765-2-RESIDUE-1, R765-2-RESIDUE-2, R765-4-S1 | **Still resolved or taken**, fixes intact | `MARK_II_AREA_PLAN.md` lines 1-1098 at the head equal `72816d26`'s except dev's `:61`. `:231`, `:233`, `:239`, `:336` and `:368` are unchanged (`receipts/17`) |
| R765-3-F1, R766-3-RESIDUE-1, R766-2-F1, R765-1-F1 to F5, R766-1-F1 to F3, R766-1-R1 | **Still resolved**: no branch line changed since round 6 | Check 1 line-set identity |
| Optional SUGGESTIONs from rounds 1 to 3 not taken | **Retained**, optional, no coverage effect | Round 6 tables |

No prior BLOCKER, MAJOR, MINOR or RESIDUE is open.

## Real limits

- **em-dash check.** It was not re-run here: the pinned Markdown renderer is not installed in this clone (rc 2, "cannot judge"). The author's receipt shows 0 findings over the 231 added lines at this head, and those lines are byte-identical to round 6's.
- **behave.** Not re-run, because the submodules are not initialised in this clone. Its inputs equal dev's, and the author's receipt passes.
- **Hash chain.** Four author receipts cannot be chained to the author's own digests (R765-6-S1). Two were reproduced; two carry no conclusion.
- **Not run by me.** No hosted or act job, no Verilator, Yosys or Vivado bank, no builder bank, and no hardware run. Physical calibration is NOT RUN, and the skipped "Physical gPTP" context is not hardware proof.
- **No manager source bank** runs at this exact head, and I claim none.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR. Source base: `503bc97c`. Live dev: `ac0a01e3`.
- Accept or refuse the hosted exact-head contexts. Some Verilator and Yosys shards were still in progress when I inspected (`receipts/15`).
- Carry R765-7-R1 to the residue checklist.
- Consider R765-6-S1 for the publication step.
- Merge only with explicit maintainer authorisation.

## Clone integrity after probes (`receipts/19_clone_integrity.txt`)

- `HEAD` is `e70ae2cb2dd0746060612493cb6724522b8701bc`, and the tree and index tree are both `b88ec0fa4ad541d5250688664459dcfd68089097`.
- `git status --porcelain --ignored` is empty, as are `diff-index --cached HEAD` and the worktree diff. The two `__pycache__` directories my probes created were removed.
- The six gitlinks are unchanged and equal dev's. The submodules are uninitialised, as received.

R765-7 FINISHED
