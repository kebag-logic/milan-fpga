[R392] POSITIVE - exact head caa1df666de17ba38ae402c52e1ae219dbd01d8b

# R392-4: internal independent delta review of PR #616 (issue #451), merge of dev `13eda870`

- **Head under review.** `caa1df666de17ba38ae402c52e1ae219dbd01d8b`, tree `147d1797e2f833d0e42f5fbf3be00c650320607f`. It matches the published PR head and the remote branch; remote `dev` is `13eda870d1a6cf3f946fc228a98862366b08d102` (`receipts/ls_remote.txt`, `receipts/ls_remote_final.txt`, `receipts/pr_view.json`).
- **Delta.** `0e5ae9c8..caa1df66` is one merge commit. Parents: `0e5ae9c8` (lane) and `13eda870` (live dev). Merge base: `7390b436`. Subject: "Merge dev into 451-tdm8-first-light", no body, no trailers (`receipts/tree_identity_and_pr_meta.txt`). Dev brought in PR #614, PR #603 (#602), PR #615 (#607) and PR #609 (`receipts/dev_first_parent_log.txt`).
- **Round.** R392-4, internal reviewer, cleared context, all five lenses. Reconstruction order:
  1. AGENTS.md, CONTRIBUTING.md, docs/README.md.
  2. The #451 body, the PocketBeagle 2 amendment (5729936674) and the first-light assignment (5859278962).
  3. Merge-dev round 2 assignment (5883651809), and the executor's TAKEN (5883658963) and REVIEW READY (5883709985).
  4. The diff and history, then the public author packet `author-mergedev2` on `451-review-evidence` (`a49bbfd7`) and the hosted checks.
- **Independence.** I read the prior public review findings only after my own pass. My draft verdict and ledger were written first (`receipts/draft_verdict_before_prior_findings.md`). No private material was used.
- **Scope.** Per the assignment, R392-3's POSITIVE at `0e5ae9c8` stands for the lane's own content. This round judges only the merge.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. One new SUGGESTION (S1) is a merge-time item for the manager.

## The five focus checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | The matrix conflict keeps both sides; the resolved matrix differs from dev by this PR's line only | **MET.** Reproduced with `git merge-tree --write-tree 0e5ae9c8 13eda870`: exactly one conflicted path, `docs/reference/MILAN_COMPLIANCE_MATRIX.md`. The recorded tree differs from the automatic merge only in that file. `MILAN_COMPLIANCE_MATRIX.md:206` (4.4.4.3) equals dev's row byte for byte and carries the #602 ruling link. `:207` (4.4.4.5 / .9) equals the lane's row and carries the first-light link. Dev's `:120` (5.4.2.15 / .16), `:169` (5.3.11.1) and `:192` (7.4.42.2) equal dev's rows. The file differs from dev in exactly one line and from the lane in exactly dev's four lines. No conflict markers anywhere in the tracked first-party tree. The rendered HTML carries each link in its row. | `check_merge_delta.py` → `receipts/check_merge_delta.out`; `receipts/merge_tree.txt`; `check_rendered_tables.py` → `receipts/rendered_tables.out` |
| 2 | Findings index has every row of both sides in the index's order, with no duplicate; `CLOCK_DOMAINS.md` carries both sides | **MET.** `docs/findings/README.md:11-20`: 10 unique rows. The #451 row is first, as on the lane, and dev's nine rows follow in dev's order. This includes PR #609's reworded #397 row at `:14`, and no stale lane copy of it. `docs/litex/CLOCK_DOMAINS.md` keeps PR #615's six added lines (`:346-351`) and this PR's line `:140`. The superseded "capture, not physical TDM rendering" line is gone. | `receipts/check_merge_delta.out`, `receipts/rendered_tables.out` |
| 3 | `git diff dev..caa1df66` is only this PR's four files; the processor gitlink equals dev's `c951a9ff` | **MET.** Name-status: `A` page, `M` index, `M` CLOCK_DOMAINS, `M` matrix. For each file, the changed lines against dev equal the lane's changed lines against the merge base. The page blob `cb7dd0aa` is unchanged. Numstat `lane..head` equals numstat `base..dev`, and for every dev-touched file the changed lines agree, so the merge brought dev and nothing else. All gitlinks equal dev's. The `hdl`, `tb`, `sw`, `constraints`, `configs`, `scripts` and `.github` subtree ids, REQUIREMENTS.md, CONTRIBUTING.md and AGENTS.md are identical to dev. | `receipts/check_merge_delta.out`, `receipts/tree_identity_and_pr_meta.txt`, `receipts/dev_to_head.diff`, `receipts/lane.diff`, `receipts/blob_ids.txt` |
| 4 | No statement in the merged tree is made stale by the combination | **MET.** See "Stale-statement search" below. | `stale_search.sh`, `receipts/stale_search_*.txt`, `receipts/page_vs_dev.txt`, `receipts/page_cited_lines.txt`, `receipts/dev_changes_to_page_link_targets.diff` |
| 5 | Markdown gates pass in the pinned environment; every table has a constant cell count | **MET.** All gates below return 0. All 34 tables in the four touched files (14 in the matrix, 1 in the index, 8 in CLOCK_DOMAINS, 11 on the page) have a constant cell count in the source (GFM pipe splitting) and when rendered with the pinned environment's GFM renderer. | `receipts/md_gates.txt`, `check_table_cells.py` → `receipts/table_cells.out`, `receipts/rendered_tables.out` |

### Stale-statement search (my own, before reading the author's)

- **Direction 1: dev's added lines against this PR's claims.** I searched all 3,976 lines that dev added between `7390b436` and `13eda870` (first-party, no submodules) for these topics: TDM, McASP, PocketBeagle, first light, #451, #448, #617, J11, DOUT, DIN, render, slot, frame rate, 10.64 and capture (`receipts/stale_search_dev_added.txt`, 102 hits). No hit states TDM render or capture status, the bench link, the slip rate or frame coherence. The remaining hits fall in three groups:
  - "render re-base" (#602, #387): the render recentre on a PHC step. This is independent of physical TDM rendering.
  - "slot" (NVM slots, `YAML_SLOT`) and "capture" (the NVM capture CPU harness, `capture_output`).
  - `audio_tdm` in #615's Ethernet-constraint derivation (`sw/litex/milan_soc.py`, tests). It does not touch the TDM line at `CLOCK_DOMAINS.md:140`.
- **Direction 2: this PR's claims against dev's changes.** The page's cited targets were checked against dev's changes (`receipts/page_vs_dev.txt`, `receipts/page_cited_lines.txt`):
  - Dev changed four files the page links.
  - `hdl/milan/milan_datapath.sv`: dev changed only lines 3097-3137 (the #602 `mcr_restart_p_w`). The page's cited line 1344 (`cap_xbar_live_w`) is byte-identical at the lane and the head.
  - `sw/litex/platforms/alinx_ax7101.py`: dev added an import and a toolchain swap. The `tdm` resource the page cites, cited without a line number, is unchanged in content: B22, A20, B20, F20, F19, J16.
  - `docs/design/TIME_SYNC.md#listener-render-latency`: the heading is at `:331`. The reset-rail row "a PDU one interval late never trips it", which the page's "one PDU interval of lateness" relies on, is unchanged. Dev changed only the Recentre row's `mr` clause.
  - `docs/litex/CLOCK_DOMAINS.md`: the -10.64 ppm plan A row at `:119` is unchanged.
  - The page mentions none of #387, #397, #599 or #602-#615, MDIO, PHC, `mr`, MEDIA_RESET or constraints.
- **Direction 3: whole tree, lane against head.** Six pattern families over the whole tracked first-party tree, excluding `docs/history`, the page and submodules: render status, first light, bench link, DIN coherence, slip rate and TDM hardware. They give the same 109 hits at `0e5ae9c8` and at `caa1df66`, apart from line numbers (`receipts/stale_search_delta.txt` is empty). The combination therefore introduces no new statement in these families. The pre-existing hits were classified by R392-3; I re-read the two Arty `pmodb` "No TDM8 device is on the bench yet" comments (`configs/endstation_arty_4x4.yaml:36`, `configs/endstation_arty_8ch.yaml:71`). They concern the Arty header, not the AX7101 J11 link, so they are not stale.
- **Agreement with the author.** The author's eight-family search (`author-mergedev2/receipts/stale_search_families.tsv`, `stale_search_new_hits.diff`) reports three new false-positive hits and one hit removed by dev's #397 rewrite. That agrees with my result.

## Findings

No BLOCKER, MAJOR or MINOR finding.

**S1 - SUGGESTION - lenses: Conformance, Docs - artifact: PR #616 linkage (`closingIssuesReferences`), `receipts/github_state.txt`, `receipts/tree_identity_and_pr_meta.txt`.**
- **Evidence.**
  - GitHub reports `closingIssuesReferences: [#451]` for PR #616. The PR body has no closing keyword and says "This record does not close #451, #448, #386 or #117" (body line 107), so the link comes from the issue's Development linkage (the branch was cut with `gh issue develop`).
  - `dev` is the default branch (`scripts/check_merge_review_integrity.py:14-19` records that the close fires on merge into `dev`).
  - Assignment 5883651809 freezes a `--partial` merge: "#451 stays open for the capture through the USB Audio device and the scope item".
- **Impact.** An ordinary merge of this PR would auto-close #451, against the frozen scope and the PR body. The tree at this head is correct; this is merge-time metadata.
- **Suggested outcome.** At the merge turn, the manager ensures #451 remains open, for example by removing the Development link before merging or by reopening immediately after. No change to the head is needed.
- **Verification.** After the merge, `gh issue view 451 --json state` reads OPEN.

## Prior public findings on this PR, at this head

The page blob is unchanged (`cb7dd0aa`), as are the index row, `CLOCK_DOMAINS.md:140` and matrix `:207`. `scripts/` is unchanged since `0e5ae9c8`. I re-checked each anchor (`prior_findings_at_head.sh` → `receipts/prior_findings_at_head.txt`).

| Prior item | Severity | Status at `caa1df66` |
|---|---|---|
| R392-1 F1 = R393-1 S1 (idle-high claim) | MINOR | RESOLVED: the removed claim has 0 matches; the page is unchanged |
| R392-1 F2 = R393-1 F1 (#617 not linked) | MINOR | RESOLVED: `issues/617` at page `:16`, `:295`, `:409` and in the index row `README.md:11`; #617 is OPEN |
| R393-1 F2 (page not indexed) | MINOR | RESOLVED: `README.md:11`, kept through this merge |
| R393-1 F3 (owner check unsourced; conductor count) | MINOR | RESOLVED: 5872564358 cited at `:111`, `:401`; "seven conductors" at `:113` |
| R392-1 F3-F6, R393-1 S2-S6 | SUGGESTION | Taken earlier; unchanged |
| R392-1 F7 (underrun split) | SUGGESTION | Retained as optional; unchanged |
| R392-2 S1, S2; R393-2 S7 (index State wording), S8 (`[A403] Refs #451.` on `:3`) | SUGGESTION | Retained as optional; text unchanged |
| R392-3 S1 (docs gates blind to table shape and duplicate rows) | SUGGESTION | Retained: `scripts/` is unchanged. At this head, my own row and table checks cover that gap (fault probes below) |
| R392-3 S2 (cite #617 beside `CLOCK_DOMAINS.md:140`) | SUGGESTION | Retained as optional; `:140` is unchanged |

No retained item is above SUGGESTION.

## Gates, probes and hosted evidence

- **Pinned Markdown environment** (`$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`, Python 3.14.7; `receipts/md_env_freeze.txt`, `receipts/md_env_python.sha256`). Run at the head, unpiped, from the physical path. Each returned 0 (`receipts/md_gates.txt`):
  - `scripts/docs_check.py`: 0 findings, 175 md files.
  - `scripts/check_doc_style.py`, plus `--selftest`.
  - `scripts/check_doc_paths.py`: 854 paths.
  - `scripts/gen_toc.py --check`, plus `--verify-anchors`: 240 links.
  - `scripts/check_em_dash.py --base 13eda870d1a6`: 0 findings over 441 added lines in 4 pages. Plus `--selftest`: 339 arms.
  - `scripts/check_baremetal_only.py --check`.
  - `git diff --check 13eda870 caa1df66`, `git diff --check 7390b436 caa1df66` and `git diff --check`.
- **Scope classification.** `scripts/ci_scope.py` classifies the four-file diff as not RTL-relevant (`false`). The hosted `full-ci-gate` logged `draft=false rtl=false run_full=false`, docs-only (`receipts/full_ci_gate_scope.txt`).
- **Fault probes** (`receipts/fault_probes.txt`), run on a disposable clone under `scratch/`:
  - P0: the unmodified head passes the merge checker (rc 0).
  - P1: the lane head substituted for the merge fails. Dev's rows and lines are missing, and the diff against dev is not four files.
  - P2: dev substituted for the merge fails. The PR's page, row and lines are missing.
  - P3: a synthetic bad resolution fails. It takes the lane's 4.4.4.3, dropping the #602 link, and duplicates the #397 index row. Both "4.4.4.3 equals dev's" and "no duplicate row" fail.
  - P5: the rendered check catches the dropped link and the duplicate row.
  - P4: a dropped cell separator on the `:207` row fails the cell-count check.
  - Each check that passes at the head can therefore fail for the defect it names.
- **No simulator used.** The head's `hdl`, `tb`, `sw`, `configs` and `scripts` subtrees are byte-identical to dev, so no simulation could fail for a defect in this delta. The scoped simulator was not needed, and I did not use it.
- **Hosted checks at the exact head** (`receipts/check_runs_at_head*.tsv`, `receipts/pr_checks.txt`; every run's `head_sha` is `caa1df66`):
  - **Executed, SUCCESS:** `rtl-fast`, `elaborate`, `changes`, `bdd-conformance`, `full-ci-gate`, `wire-accountability`, `docs-check-no-git`.
  - **SKIPPED contexts:** `verilator-suites`, `yosys-portability`, both shard matrices, `verilator-lint`, `yosys-elaboration`, Physical gPTP. These are skips, not passes, and they are consistent with the docs-only classification.
  - **`docs-check`:** still `in_progress` at my last snapshot (2026-09-29T04:46Z). Its outcome is a manager item.
- **Clone restored and verified** (`receipts/clone_integrity.txt`):
  - HEAD, tree, worktree and index equal `caa1df66`.
  - Index mode, blob and path entries equal the HEAD tree.
  - No untracked file.
  - Submodule checkouts sit at the recorded gitlinks: `protocol-processor` `c951a9ff`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, and `external` `efeb541a` (not initialized).

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 open as SUGGESTION only) | Assignment 5883651809 against focus checks 1-5. `MILAN_COMPLIANCE_MATRIX.md:206` (dev's 4.4.4.3 with the #602 ruling link, which resolves to issue #602 comment 5859297355) and `:207` (lane's 4.4.4.5 / .9). Dev rows `:120`, `:169`, `:192`. `git merge-tree` reproduction. Processor gitlink `c951a9ff`. PR linkage against the `--partial` scope (S1). | R392-4 | `caa1df666de17ba38ae402c52e1ae219dbd01d8b` |
| RTL | CLEAN | `git diff --name-status 13eda870 caa1df66`: four Markdown files, none under `hdl/`, `tb/`, `sw/`, `constraints/`, `configs/`, `scripts/`. Those subtree ids and all gitlinks equal dev's. The page's RTL citation `milan_datapath.sv:1344` is byte-identical at the lane and the head; dev's datapath change is at `:3097-3137`. The `tdm` pins in `alinx_ax7101.py:187-192` are unchanged in content. | R392-4 | `caa1df666de17ba38ae402c52e1ae219dbd01d8b` |
| Robustness | CLEAN | Merge-resolution failure modes: lost dev row, lost link, duplicate row, conflict markers, dropped cell and the wrong side taken. Each is caught by the checks (P1-P5), and the head passes them (P0). The recorded tree equals the automatic merge except the resolved file. The whole-tree conflict-marker grep is empty. Page cited lines and anchors survive dev's line shifts (`receipts/page_cited_lines.txt`). | R392-4 | `caa1df666de17ba38ae402c52e1ae219dbd01d8b` |
| Tests | CLEAN | `receipts/md_gates.txt` (12 gate invocations, rc 0). `receipts/table_cells.out`, `receipts/rendered_tables.out` (34 tables). `receipts/fault_probes.txt` (P0 passes; P1-P5 fail as intended). `ci_scope.py` docs-only. Hosted `rtl-fast` and 6 other executed contexts SUCCESS at the exact head; skipped contexts listed as skips. | R392-4 | `caa1df666de17ba38ae402c52e1ae219dbd01d8b` |
| Docs | CLEAN | `docs/findings/README.md:11-20` (10 unique rows, order, #609's #397 row). `CLOCK_DOMAINS.md:140` and `:346-351`. Matrix `:206-207`. The three-direction stale-statement search. PR body "Merge with dev, round 2" section, checked against the merge (accurate: PR #614, #603, #615 and #609 are dev's four first-parent merges). Executor REVIEW READY 5883709985 checked claim by claim. Prior-findings table above. | R392-4 | `caa1df666de17ba38ae402c52e1ae219dbd01d8b` |

**Coverage note (AGENTS.md section 7).** This merge changed Docs-scope artifacts: the matrix, the index and `CLOCK_DOMAINS.md`, through dev's lines. Coverage banked at `0e5ae9c8` (R392-3) or `335e55c4` (R393-2) therefore does not by itself cover this head; this round does, for all five lenses. Whether the two-positive bar requires an external round at this head is the manager's decision under CONTRIBUTING.md.

## Real limits

- **No hardware.** No physical calibration, scope, continuity or USB Audio device item was run or checked. The page records them as NOT RUN, and field skips are not hardware proof.
- **Raw bench captures not re-read.** The page blob is byte-identical to the one reviewed in rounds 2 and 3.
- **Not run by me:** Docker, act, the candidate merge build, and the full parent, processor, gPTP, Yosys or builder banks. No Verilator suite was run either; none was needed for a Markdown-only delta.
- **Manager banks not examined.** The manager's source static, builder and native banks at this head were not located in the linked archive `851f835c`, which predates this head. I did not rely on them.
- **Hosted `docs-check`** was still in progress at my last snapshot.

## Pending manager duties

1. Keep #451 open through the `--partial` merge (S1): the PR is linked to close #451 and `dev` is the default branch.
2. Confirm the hosted `docs-check` conclusion at `caa1df66`.
3. Build and validate the current-dev candidate at the merge turn. The source base and live dev are both `13eda870` at this review; re-check if dev moves.
4. Hosted and act acceptance, and the two-positive review bar under CONTRIBUTING.md.

R392-4 FINISHED
