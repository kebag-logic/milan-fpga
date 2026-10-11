[R598] POSITIVE - exact head 2bef9e50489a60f216a8073a9f5ea0645752b33f

# R598-4: internal cleared-context delta review of PR #722 (issue #640, Mark II lane M5)

- **Round:** R598-4, internal reviewer, cleared context. Public start: https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6108156180.
- **Head:** `2bef9e50489a60f216a8073a9f5ea0645752b33f`, tree `9777e890c07850052a0d9134cdb22388a651c5f1`. Checked at the start, and verified in full at the end of the round after the probe leftovers were removed (`receipts/verify_clone.log`, "CLONE VERIFIED"). All builds and suites ran in disposable copies under scratch.
- **Delta under review:** since the source head `c0cba330` (R598-2 and R599-2 POSITIVE), two commits:
  - `da341a15` merges dev `6bfeeb13` (M2 #710 and M6 #719).
  - `2bef9e50` rewrites `docs/design/MARK_II_AREA_PLAN.md:1106` to answer R598-3-F1.
- **Verdict: POSITIVE.** All five lenses are clean at this head. The open items are three new RESIDUE wordings, two retained RESIDUE wordings and two retained SUGGESTIONs. None of them leaves a lens unclean.

Reconstruction order followed: `AGENTS.md` and `CONTRIBUTING.md`; `docs/README.md`; issue #640's body and acceptance, the M5 lane assignment (6098404907) and the round-2 ruling (6105372796); the plan's L3, L8 and L9 sections, its ledger and D7/D8; `AREA_BUDGET.md`; the diff `6bfeeb13..2bef9e50` and history; the published evidence at `648503cf` (`review-evidence/640-m5-r1`: `MANIFEST.json`, `author/HANDOFF.md`, `author/PR-BODY.md`; the HANDOFF digest matches its manifest). Prior review findings were read only after the independent pass below.

## 1. The dev merge is the automatic merge and nothing more

| Check | Result | Receipt |
|---|---|---|
| Parents of `da341a15` | `c0cba330` and `6bfeeb13` | `receipts/merge_tree.txt` |
| `git merge-tree --write-tree c0cba330 6bfeeb13` | rc 0, tree `0fc0841b…`, no conflict; it auto-merges only `MARK_II_AREA_PLAN.md` and `measure_test_evidence_readers.py` | `receipts/merge_tree.txt` |
| Recorded tree of `da341a15` | `0fc0841b…`, the same tree, which is also the candidate tree R598-3 judged | `receipts/merge_tree.txt` |
| Files changed `c0cba330..2bef9e50` | exactly the 29 files dev changed in `e8454e27..6bfeeb13`. Per file, the patch equals dev's except the plan, which also carries the repair. | `receipts/delta_scope.txt` |
| PR-owned non-plan content | `milan_csr.sv`, `doc/milan_csr.md` and `tb/verilator/csr/` are the same blob/tree at `c0cba330` and `2bef9e50`. The PR's patch against dev is unchanged for each. The readers registry entry is unchanged except for its hunk offset. | `receipts/delta_scope.txt` |
| Commit after the merge | `2bef9e50` changes one line, `MARK_II_AREA_PLAN.md:1106` (+1 −1) | `receipts/delta_2bef9e50.diff` |
| Dev RTL against the `csr` instance | Dev's `milan_datapath.sv` hunks (3447, 3501-3535, 6323-6346) change the GET_COUNTERS column read. None of the 278 connection tokens of the `milan_csr` instance (`milan_datapath.sv:2445-2845`) appears in a changed line. | analysis in this report |

## 2. The repaired sentence recomputes from the plan's own rows

`scripts/check_plan_arithmetic.py` pulls each operand from the head plan by a unique-match pattern and recomputes the result (`receipts/plan_arithmetic.txt`, RESULT: PASS):

- Base: `:1032` `50,267 - 3,910 - 4,600 - 3,800 = 37,957`, which is the `:1048` partial-central row.
- Central figures: `:976-978` give M2 200, M5 600 and M6 600.
- Measured figures:
  - `:699` M2: the reproducible saving is 34.
  - `:539` M5: 121 routed.
  - `:960` M6: 418 post-synthesis.
- Result: 37,957 + (200 − 34) + (600 − 121) + (600 − 418) = **38,784, 744 over 38,040**. That equals `:1106` exactly.
- Sensitivity, for the record:
  - Every lane post-synthesis (34, 127, 418) gives 38,778 (+738).
  - Every lane routed (128 whole-image, 121, 468) gives 38,640 (+600).
  - On every basis the partial-central scenario misses 38,040.

**No other plan figure is stale against the three measured lanes:**

- L3 `:454`, L8 `:539` and L9 `:557` each give their lane's measured figure.
- The M2 section (`:699-703`) and the M6 section (`:960-965`) carry no consequence sentence of their own that would now be partial.
- Each section says that the cumulative tables keep the planning figure until the week-4 re-measure.
- The cumulative table (`:972-990`), the fallback table (`:1039-1068`) and the summary (`:27-37`) are planning figures under that rule.
- The only measured-substitution statement is `:1106`, and it uses all three lanes.
- `AREA_BUDGET.md:197` and `:208` (M2 and M6 "has measured its lane") are accurate. M5's absence there is R598-3-S1, retained below.

## 3. Gates at the head (rc 0 unless stated)

The Markdown gates ran under the hash-pinned renderer, in a private venv in scratch (`receipts/gates/venv_freeze.txt`: cmarkgfm 2025.10.22, html5lib 1.1). Before the venv was installed, the renderer-dependent gates refused under the system interpreter with "cannot judge". Those refused attempts were discarded and re-run under the venv.

| Gate | Result | Receipt |
|---|---|---|
| `docs_check.py` (system and venv interpreter) | 0 findings across 203 md files + 1,260 scrubbed text files | `gates/docs_check*.log` |
| `check_em_dash.py --base 6bfeeb13` | 0 findings over 68 added lines in 3 pages | `gates/em_dash.log` |
| `check_em_dash.py --base c0cba330`, `--selftest` | rc 0 each | `gates/em_dash_*` |
| `gen_toc.py --check`, `--verify-anchors`, `--selftest` | TOC gate OK (143 pages); 471 cross-page fragment links reproduced | `gates/gen_toc_*` |
| `check_doc_style.py`, `--selftest` | OK (22 current documents) | `gates/doc_style*` |
| `check_doc_paths.py` | 961 cited paths resolve; 10 line anchors within their file | `gates/doc_paths*` |
| `check_gptp_docs.py`, `docs/traceability/gen_module_matrix.py --check` | rc 0 | `gates/gptp_docs.*`, `gates/module_matrix.*` |
| `git diff --check 6bfeeb13 2bef9e50` | clean | `gates/diff_check.*` |
| `measure_test_evidence.py --check`; the registry loads and carries `tb/verilator/csr/lock_mutants.py` | rc 0 | `gates/test_evidence.*`, `gates/readers_selftest.*` |
| `check_port_contracts`, `check_todo_ownership`, `check_hygiene --check`, `measure_naming --check`, `measure_fail_fast --check`, `check_sv_idiom` (clone with registered submodules) | rc 0 each | `gates/*` |
| `check_rtl_source_lists`, `check_feature_status` | rc 0 | `gates/*` |
| `lint_rtl.py --check` (pinned Verilator) | "LINT GATE: PASS (90 violation(s) <= ratchet 90 …)" | `gates/lint_rtl.*` |

## 4. Focused suites at the head

The tool is Verilator 5.050 through the scoped pin (`suites/verilator_version.txt`; wrapper sha256 `905795b9…`), with GNU Make 4.4.1 (`suites/make_version.txt`). The suites ran in disposable copies of the head under scratch: a `git archive` export with the three submodules at their gitlinks, and a local clone for suites that call `git ls-files`.

| Suite | Result | Receipt |
|---|---|---|
| CSR, `MAKEFLAGS=w make -j8` | rc 0. Legacy legs 408/408/121/44/408 and reset bits 408, 0 failures. lock1: 5/5; reset 8,248, decode 16,456, coherence 49, freshness 79, lockstep 28,167 reads; 0 mismatching cycles. lock8: 5/5; decode 24,699, lockstep 22,750 reads; 0 mismatching. `lock_mutants.py`: "8 checks: 8 PASS, 0 FAIL". The figures equal the published HANDOFF section 3. | `suites/csr.*` |
| `tcam_csr` | rc 0, "2 checks, 0 failures" | `suites/tcam_csr.*` |
| `milan_dp_mclk` | rc 0. "31 checks: 31 PASS, 0 FAIL", including mutant 13 (read-window terms missing) caught | `suites/milan_dp_mclk.*` |
| `milan_dp`, gptp / gptp-lat / gmstep legs | 182/182, 182/182, gmstep 104 checks 0 failures. The full `make` then hit its 570 s bound inside the pool. | `suites/milan_dp_attempt1_timeout.*` (rc 124) |
| `milan_dp` pool 1 | rc 0. legacy 236/0, notify 421/0, crflic 417/0, dynmap 162/0 | `suites/milan_dp_pool1.*` |
| `milan_dp` pool 2 | rc 0. nxn 1,967/0, nxndv 1,969/0, nxn8 3,751/0, nxn4c 1,967/0 | `suites/milan_dp_pool2.*` |
| `milan_dp` pool 3 | nolpf 236/0, prune 33/0, ax1x1 233/0. **aclk (true 391/1591 audio-clock ratio) did not finish within the bound** (rc 124). | `suites/milan_dp_pool3.*` |

Every `FAIL` token in the `milan_dp` logs is part of a protocol status name (`TALKER_DEST_MAC_FAILED`, `REGISTERING_FAILED`), not a check result.

**Hosted, exact head, snapshot 2026-10-11T11:09Z** (`receipts/hosted_check_runs_2bef9e50.tsv`):

- 15 success, including `docs-check`, `docs-check-no-git`, `elaborate`, `verilator-lint`, `yosys-elaboration`, Yosys shards 0-3 and Verilator shards 0 and 3.
- 1 skipped context: physical gPTP, nightly only. It is not hardware proof.
- 4 in progress: `firmware-unit` and Verilator shards 1, 2 and 4.
- The manager owns hosted and act acceptance. This round claims no manager source bank.

## 5. Findings

### R598-4-RES-1: RESIDUE (lens Docs). The PR body's reproduction step pins the old head

- **Where:** PR #722 body, "How to get into the same state": `git rev-parse HEAD   # c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` (`receipts/pr_body_checks.txt`).
- **Evidence:** the PR head is `2bef9e50…`, so a cold reader following the step sees a mismatch.
- **Impact:** wording only. No measurement, figure or claim changes.
- **Exact fix:** `git rev-parse HEAD   # 2bef9e50489a60f216a8073a9f5ea0645752b33f`.
- **Verification:** re-read the PR body.

### R598-4-RES-2: RESIDUE (lens Docs). "Known limitations" still states the M5-only consequence without its scope

- **Where:** PR #722 body, "Known limitations", first bullet: "At the measured 121, the partial-central scenario becomes about 38,436, 396 over 38,040, pending that re-measure (D8)."
- **Evidence:**
  - The arithmetic is right for M5 substituted alone. The figure is not wrong.
  - The same body's Status and "Composition repair" sections give 38,784, and the plan (the durable record) gives 38,784.
  - R598-3-F1 called updating this sentence optional.
- **Impact:** a reader of that bullet alone sees the M5-only figure as the scenario. No figure needs to change, only its scope.
- **Exact fix:** "With M5's measured 121 alone, the partial-central scenario is about 38,436; with M2's and M6's measured savings as well it is about 38,784, 744 over 38,040 (see [Composition repair](#composition-repair)), pending that re-measure (D8)."
- **Verification:** re-read the PR body.

### R598-4-RES-3: RESIDUE (lenses Docs, Conformance). The repaired sentence names its figures but not their bases

- **Where:** `docs/design/MARK_II_AREA_PLAN.md:1106`.
- **Evidence:**
  - R598-3-F1's required outcome asked for "the basis of each figure named".
  - The sentence gives M2 (34), M5 (121) and M6 (418) without saying that 34 and 418 are post-synthesis and 121 is routed in the `csr` scope.
  - Each basis is stated where the figure is defined (`:454`, `:539`, `:557`), and the sentence's result is unchanged.
  - The sensitivity range in section 2 (38,640-38,784) never reaches 38,040.
- **Impact:** wording only. The figure, the miss and every gate are unchanged.
- **Exact fix:** "With the measured savings of M2 (34, post-synthesis), M5 (121, routed in its scope) and M6 (418, post-synthesis) in place of their central figures, the partial-central scenario becomes about 38,784, 744 over 38,040, pending the week-4 re-measure (D8)."
- **Verification:** `python3 -I scripts/check_plan_arithmetic.py <clone>`, with the line-1106 pattern adapted, must still print RESULT: PASS. The em-dash, TOC and docs gates must stay rc 0.

## 6. Prior public findings on this PR: disposition at this head

| Finding | Disposition | Evidence at `2bef9e50` |
|---|---|---|
| R598-3-F1 (MINOR, Docs, Conformance): partial-central counted only M5 | **RESOLVED** | `:1106` substitutes all three measured lanes, and the result recomputes exactly (`plan_arithmetic.txt`). The unnamed bases are wording only and are carried as R598-4-RES-3. |
| R598-3-S1 (SUGGESTION, Docs): `AREA_BUDGET.md` lacks M5's "has measured its lane" line | **Retained, optional.** Independently re-observed in this round's pass. No statement there is false. | `AREA_BUDGET.md:197,208` |
| R598-2-S1 (SUGGESTION): combined consequence at the merge turn | **Superseded** by R598-3-F1, now resolved | as above |
| R598-2-RES-1 (RESIDUE, Docs): "These are the route gate's own sub-block figures for the M5 route." | **Retained.** The text is still in the PR body, once. Exact fix as given in R598-2. | `pr_body_checks.txt` |
| R598-2-RES-2 (RESIDUE, Docs): "nearly all of it in `u_pp`" | **Retained.** The text is still in the PR body, once. Exact fix as given in R598-2. | `pr_body_checks.txt` |
| R598-1-F1 = R599-1-F2 (MINOR, Docs): attribution double count | **Resolved** (R598-2, R599-2). The disjoint −121 / −342 (nested −344) / about −227 text is unchanged in the body. | `pr722_body_at_review.md` |
| R599-1-F1 (MINOR, Docs, Conformance): per-stream scope | **Resolved.** The plan text from M5's patch is unchanged; it is now at `:1102-1103`. | `delta_scope.txt` |
| R598-1-S1; R599-1-RES-1, RES-2, RES-3 | **Applied/resolved.** `milan_csr.sv` blob and L8 `:539` are unchanged since `c0cba330`. | `delta_scope.txt` |
| R599-1-S1 (SUGGESTION: alternate placement directives) | **Retained, optional.** Nothing in this delta affects it. | — |

The PR body states the repair ("Status" and "Composition repair") and carries no closing reference. `closingIssuesReferences` is empty, no closing keyword precedes an issue number, and the body reads "Relates to #640" (`pr_body_checks.txt`).

## 7. Per-lens results

```text
[R598] PASS Conformance — docs/design/MARK_II_AREA_PLAN.md:454,539,557,699,960,976-978,1032,1048,1106; receipts/plan_arithmetic.txt; issue #640 acceptance and lane assignment 6098404907 — the repaired partial-central figure recomputes exactly from the plan's own rows (38,784, +744) and every basis misses 38,040, so no NFR-RES-01 claim is overstated; the register ABI and snapshot contracts are untouched (milan_csr.sv blob identical to c0cba330; receipts/delta_scope.txt)
[R598] PASS RTL — receipts/merge_tree.txt, receipts/delta_scope.txt, hdl/milan/milan_datapath.sv:2445-2845 against dev's hunks 3447-3535 and 6323-6346, receipts/gates/lint_rtl.log, receipts/gates/sv_idiom.log, receipts/gates/check_rtl_source_lists.log, receipts/gates/check_port_contracts.log — the merge is the automatic merge; no milan_csr connection is touched by M6's GET_COUNTERS change; the composed datapath elaborates under the lint ratchet (90 <= 90)
[R598] PASS Robustness — receipts/suites/csr.log (lock1/lock8 reset-values, snapshot-freshness and random-traffic phases, 0 mismatching cycles; 7 planted defects caught), receipts/suites/milan_dp_pool3.log (nolpf, prune: feature-disabled shapes), receipts/suites/milan_dp_mclk.log (mutant 13) — at the composed head the reset, stale-snapshot and configuration-dependent paths hold; the delta adds no input path to milan_csr
[R598] PASS Tests — receipts/suites/{csr,tcam_csr,milan_dp_mclk,milan_dp_pool1,milan_dp_pool2,milan_dp_pool3,milan_dp_attempt1_timeout}.log, receipts/gates/test_evidence.log, scripts/measure_test_evidence_readers.py (M5 entry present beside M6's) — the lockstep figures reproduce the published HANDOFF counts exactly; tb/verilator/csr is byte-identical to c0cba330; the aclk leg is an unfinished limit (section 9), not a failure
[R598] PASS Docs — docs/design/MARK_II_AREA_PLAN.md:1106 and its sections L3/L8/L9, M2/M5/M6 measurements, cumulative and fallback tables; docs/design/AREA_BUDGET.md:181-229,296-338; PR #722 body (receipts/pr722_body_at_review.md); receipts/gates/{docs_check,em_dash,gen_toc_check,gen_toc_anchors,doc_style,doc_paths}.log — no plan figure is stale against the three measured lanes; every docs gate passes; open items are RESIDUE (R598-4-RES-1..3, R598-2-RES-1/2) and SUGGESTION (R598-3-S1, R599-1-S1) only
```

## 8. Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Plan `:454,539,557,699,960,976-978,1032,1048,1106`; `plan_arithmetic.txt`; issue #640 acceptance and the M5 assignment; `milan_csr.sv` blob identity (`delta_scope.txt`) | R598-4 | `2bef9e50489a60f216a8073a9f5ea0645752b33f` |
| RTL | CLEAN | `merge_tree.txt`; `delta_scope.txt`; `milan_datapath.sv` `csr` instance against dev's hunks; `lint_rtl`, `sv_idiom`, `check_rtl_source_lists` and `check_port_contracts` logs | R598-4 | `2bef9e50489a60f216a8073a9f5ea0645752b33f` |
| Robustness | CLEAN | `csr.log` lock1/lock8 phases and mutants; `milan_dp_pool3.log` nolpf/prune; `milan_dp_mclk.log` mutant 13 | R598-4 | `2bef9e50489a60f216a8073a9f5ea0645752b33f` |
| Tests | CLEAN | CSR, `tcam_csr`, `milan_dp_mclk` and `milan_dp` (14 of 15 legs) logs; `test_evidence.log`; readers registry | R598-4 | `2bef9e50489a60f216a8073a9f5ea0645752b33f` |
| Docs | CLEAN (RESIDUE and SUGGESTION only) | Plan `:1106` and the surrounding ledger; `AREA_BUDGET.md`; PR #722 body; docs gates under the pinned renderer | R598-4 | `2bef9e50489a60f216a8073a9f5ea0645752b33f` |

## 9. Real limits

- **No route of the composed tree.** M2, M5 and M6 each routed alone against `e8454e27` (WNS +0.306, +0.097 and +0.141 ns). Their combined area and timing are unmeasured, and nothing here infers them. The 38,784 figure is plan arithmetic, not a measurement.
- **`milan_dp` aclk leg not completed.** The true-ratio audio-clock leg did not finish within the per-call bound. It drives the audio clock ratio and does not exercise a CSR path changed by M5. The render and gmstep mutation campaigns that follow the pool were not run.
- **Not run:** the firmware host tests, the builder, `behave`, Yosys, the full parent/PP/gPTP banks, act, and the route.
  - The source-head execution evidence for those is the author's published gate receipts.
  - The manager validates the final current-dev candidate at the merge turn.
  - This round claims and infers no manager source bank.
- **Hosted:** four exact-head contexts were still in progress at the snapshot. Physical calibration was NOT RUN, and the skipped physical context is not hardware proof.
- The round-2 HANDOFF is not published; only the round-1 evidence (`648503cf`) was read.

## 10. Pending manager duties

- Carry R598-4-RES-1, RES-2 and RES-3 and R598-2-RES-1 and RES-2 (exact texts above and in R598-2) to the residue checklist. R598-3-S1 and R599-1-S1 are optional.
- Confirm the four in-progress hosted contexts at this head.
- At the merge turn:
  - Build and validate the final current-dev candidate. Source base and live dev are both `6bfeeb13` at this review (`receipts/ls_remote.txt`; `640-m5` is at this head).
  - Run the full local bar, hosted acceptance and act acceptance.
  - Obtain explicit maintainer authorization for the merge.
  - Run post-merge containment.
- The combined M2+M5+M6 area and timing remain for the week-4 re-measure (D8) and M9. The gate record stays unchanged under D7.

## 11. Packet

- **Scripts:**
  - `scripts/check_plan_arithmetic.py` (operands extracted from the plan).
  - `scripts/run_checks.sh` (the commands as run).
  - `scripts/verify_clone.sh` (head, tree, index, blob bytes, modes, leftovers, gitlinks).
- **Receipts:** under `receipts/`, each listed in `MANIFEST.sha256`. Local paths are replaced by `<CLONE>`, `<PACKET>`, `<PINNED_VERILATOR>` and `<PINNED_VERILATOR_ROOT>`.
- **Not published:** `scratch/` (the venv, exports, build trees and unsanitized raw receipts).

R598-4 FINISHED
