[R598] NEGATIVE - exact head 8f0f205161fe924797ee2d494a0a79f5f6adb77a

# R598-3: composition review of PR #722 (issue #640, Mark II lane M5) on the merge-train candidate

- **Round:** R598-3, composition acceptance only. Cleared context. The review started publicly at https://github.com/kebag-logic/milan-fpga/pull/722#issuecomment-6107947972.
- **Candidate:** `8f0f205161fe924797ee2d494a0a79f5f6adb77a`, tree `0fc0841bebece392d6facb87cd209d2f5e96e565`. It merges the PR source head `c0cba330fd485e52fcb90d5ccc69169edf9f0c2b` onto the M6 candidate `1a042affce2f252f10ed40b3ec25659611b3974b`. That candidate is M6 (PR #719, `ee0fc6fd`) merged onto live dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`, and live dev carries M2 (PR #710).
- **Source reviews:** R598-2 and R599-2 are both POSITIVE at `c0cba330`.
- **Verdict:** NEGATIVE, on one MINOR (lenses Docs and Conformance) that composition introduced:
  - The merged Mark II plan now records three measured lanes: M2, M5 and M6.
  - Its partial-central consequence sentence substitutes only M5's figure.
  - So it gives the scenario as 396 LUTs over 38,040. The plan's own figures recompute to about 694-744 over.
- **Everything else holds:**
  - The candidate tree is exactly the automatic merge.
  - Both sides' deltas survive byte-for-byte in the two shared files.
  - The readers registry holds every disposition from M6 and M5.
  - All 28 documentation, registry and hygiene gates pass on the candidate.
  - The lint ratchet passes.
  - The CSR suite passes on the candidate with its lockstep legs and all seven planted defects.
  - RTL, Robustness and Tests are clean for the composition.

## 1. What composition changes

Receipt: `receipts/composition.txt`.

| Fact | Evidence |
|---|---|
| The candidate tree is the automatic merge, not a hand resolution | `git merge-tree --write-tree 1a042aff c0cba330` = `0fc0841b…` = candidate tree. The M6 candidate's tree likewise equals `merge-tree ac2c5e77 ee0fc6fd` (`9ef4b6a2…`). |
| Live dev | `git ls-remote origin refs/heads/dev` = `ac2c5e77bba1…` at review time |
| Merge base of the two sides | `e8454e27` (the M5, M6 and M2 lane base) |
| Files changed on both sides since `e8454e27` | `docs/design/MARK_II_AREA_PLAN.md` (M2 #710, M6 #719, M5) and `scripts/measure_test_evidence_readers.py` (M6 #719, M5). Exactly the two the manager named; no others. |
| M5's delta is preserved | Same patch-id for each shared file: source `e8454e27..c0cba330` vs composed `1a042aff..8f0f2051` (plan `5df1472d…`, registry `64137cf0…`) |
| The predecessors' delta is preserved | Same patch-id: `e8454e27..1a042aff` vs `c0cba330..8f0f2051` (plan `021bad15…`, registry `7fb2233c…`) |
| M5's other eight files are unchanged by the merge | Blob at `c0cba330` = blob at candidate for each (`composition.txt`) |
| No RTL overlap | M2 and M6 do not touch `milan_csr.sv`. M6's `milan_datapath.sv` hunks are at 3450-3530 and 6337 (GET_COUNTERS face only), away from the `csr` instance at 2445-2472. M5 changes no `milan_csr` port, so no connection can double or drop. M2's `milan_soc.py` change moves the AXI-Lite crossing's W/R payload into block RAM. It states that depths, widths and read latency are unchanged, and the bus handshake M5 relies on is the same. |
| Plan headings and anchors | No duplicate heading in the composed plan. `#m2-`, `#m5-` and `#m6-intermediate-measurement` each resolve and are referenced once, from L3, L8 and L9. |
| PR body closes nothing | "Relates to #640"; no closing keyword, so merging does not close the umbrella issue. |

## 2. Gates run on the candidate

All gates ran in this clone at the exact head. The pinned Markdown renderer came from a private hash-pinned venv in scratch (`receipts/md_venv_freeze.txt`). The first attempt under the system interpreter was refused ("cannot judge": renderer absent); the receipts below supersede it. Tool identity: `receipts/tool_identity.txt`, Verilator 5.050 via the scoped pin.

| Gate | Result | Receipt |
|---|---|---|
| `docs_check.py` | rc 0 | `receipts/gates/docs_check.*` |
| `gen_toc.py --selftest`, `--check`, `--verify-anchors` | rc 0. "TOC gate: OK (143 page(s)…)". "anchor check: 471 existing cross-page fragment links reproduced". | `receipts/gates/gen_toc_*` |
| `check_em_dash.py --base 1a042aff` (candidate parent) | rc 0. 0 findings over 68 added lines in 3 pages. | `receipts/gates/em_dash_parent.*` |
| `check_em_dash.py --base ac2c5e77` (live dev) / `--base e8454e27` (source base) / `--selftest` | rc 0 each. Live dev: 0 findings over 121 added lines. | `receipts/gates/em_dash_*` |
| `ci_events.py --check`, `--selftest` | rc 0 | `receipts/gates/ci_events_*` |
| `measure_test_evidence.py --check`, `--selftest` | rc 0. "TEST-EVIDENCE RATCHET: PASS (67 <= 77 …, 0 <= 0 unexplained DUT-source reader(s) …)". No stale disposition. | `receipts/gates/test_evidence_*` |
| `check_doc_style`, `check_doc_paths`, `check_hygiene --check`, `check_py_idiom`, `check_cpp_idiom`, `check_sv_idiom`, `check_todo_ownership`, `check_feature_status`, `check_solution_docs`, `check_submodule_docs`, `measure_naming --check`, `measure_fail_fast --check`, `check_rtl_source_lists`, `check_port_contracts`, `check_entity_shape --self-test`, `check_gptp_docs` | rc 0 each | `receipts/gates/*` |
| `lint_rtl.py --check --jobs 8` (pinned Verilator) | rc 0. "LINT GATE: PASS (90 violation(s) <= ratchet 90; 18 waived, 0 justified lint_off)". This sweep elaborates the composed `milan_datapath` with M6's and M5's changes together. | `receipts/suites/lint_rtl_check.*` |
| CSR suite, `make -j16` in a `git archive` export of the candidate (pinned Verilator) | rc 0. Legacy legs 408/408/121/44/408 and reset bits 408, 0 failures. lock1: 5/5, 340,861 cycles, 28,167 random-traffic reads, 0 mismatching cycles. lock8: 5/5, 374,265 cycles, 22,750 reads, 0 mismatching. `lock_mutants.py`: control plus 7 planted defects, "8 checks: 8 PASS, 0 FAIL". | `receipts/suites/csr_make.*` |
| Partial-central recomputation from the composed plan's own figures | See F1 | `scripts/partial_central.py`, `receipts/partial_central.txt` |
| Clone integrity after all runs | rc 0, "CLONE VERIFIED": head, tree, index tree, all stage 0, no hidden flags, worktree bytes and modes, no untracked or ignored leftovers, required gitlinks at their pins and clean | `scripts/verify_clone.sh`, `receipts/verify_clone.*` |

The manager's candidate bank directory names this exact head in `full-native/complete.json` and `manager-builder/complete.json`, both with `exit_code` 0. Its `full-suite-logs/milan_dp.log` and `csr.log` end in PASS tallies. I read those files only. I did not reproduce them, and this round does not count them as its own evidence.

The CSR suite log is published with one substitution: the pinned tool's local install prefix is replaced by `<PINNED_VERILATOR_ROOT>`.

## 3. Findings

### R598-3-F1: MINOR (lenses Docs, Conformance). In the merged plan, the partial-central consequence counts M5's measured shortfall but not M2's or M6's

- **Where:** `docs/design/MARK_II_AREA_PLAN.md:1106` at the candidate: "At M5's measured 121, the partial-central scenario becomes about 38,436, 396 over 38,040, pending the week-4 re-measure (D8)."
- **Authority:**
  - The plan's D7 rule (`:1199-1201`): "Intermediate lanes publish measured deltas here".
  - The partial-central derivation (`:1029`, `:1032`, `:1048`): the remaining lanes' central 4,600 includes M2 200, M5 600 and M6 600, giving 37,957.
  - The manager's composition brief: every plan-watch figure in the merged plan must add up with all three milestones' measured figures.
- **Evidence:**
  - `receipts/plan_presence.txt`: at the source head `c0cba330`, the plan holds the 38,436 sentence and neither M2's 34 nor M6's 418. At `1a042aff` it holds M2's and M6's figures and not the sentence. The candidate holds all three.
  - So the sentence was complete in the document it was reviewed in. In the merged document it is not.
  - The merged plan records M2's reproducible saving as 34 (`:699`, `:454`) and M6's as 418 post-synthesis / 468 routed (`:960`, `:557`).
  - `receipts/partial_central.txt` recomputes the same formula:

    | Lanes substituted | Partial-central image | Against 38,040 |
    |---|---:|---:|
    | Plan figures only | 37,957 | -83 |
    | M5 121 alone (the sentence) | 38,436 | +396 |
    | M2 34 + M5 121 + M6 418 (reproducible figures) | 38,784 | +744 |
    | M2 34 + M5 127 + M6 418 (all post-synthesis) | 38,778 | +738 |
    | M2 34 + M5 121 + M6 468 (M6 routed) | 38,734 | +694 |

- **Impact:**
  - The merged plan's only stated measured consequence for the partial scenario understates the miss by about 300-350 LUTs, close to half the real gap.
  - A cold reader at the week-4 checkpoint would take 38,436 as the measured-so-far figure and size the needed redesign against it.
  - This is a figure, not wording, so it is not RESIDUE.
  - Neither source review could see it: each document was self-consistent alone.
  - R598-2-S1 raised the M2-only form as optional "at the merge turn". This is that turn, and M6's shortfall now adds to it, so it is escalated here.
- **Required outcome:**
  - The merged plan must state the partial-central consequence once, using every lane measured in it (M2, M5 and M6), with the basis of each figure named. On the reproducible figures that is about 38,784, 744 over 38,040, and about 38,730-38,780 across the stated bases.
  - Alternatively, keep the M5-only sentence, scope it explicitly ("with every other lane at its planning figure"), and add the combined figure beside it.
  - The cumulative tables may keep their planning figures under the existing week-4 rule.
  - The same M5-only figure also appears in the PR body's "Known limitations". Updating it is optional, because the plan is the durable record.
- **Verification:** run `python3 -I scripts/partial_central.py docs/design/MARK_II_AREA_PLAN.md` from this packet. Its patterns must be adapted to the corrected sentence. The stated figure must equal the all-measured row, and the docs, TOC and em-dash gates must stay rc 0.

### R598-3-S1: SUGGESTION (lens Docs). `AREA_BUDGET.md` records M2's and M6's measurements but not M5's

- **Where:** `docs/design/AREA_BUDGET.md:197` (M2) and `:208` (M6). Each reads "has measured its lane" and links to the plan ledger. Composition leaves M5 as the one measured lane without that line.
- **Why only a suggestion:** No statement in `AREA_BUDGET.md` becomes false. Its table keeps planning figures by its own rule, and M5's assignment required reporting only in the plan ledger.
- **Optional outcome:** add, beside the M5 row's context, "M5 has measured its lane: 121 LUTs routed and 127 post-synthesis in its `csr` scope, no block-RAM growth", linked to `MARK_II_AREA_PLAN.md#m5-intermediate-measurement`.

## 4. Prior findings on this PR: disposition at this head

I read these after my own pass.

| Finding | Disposition |
|---|---|
| R598-1-F1 = R599-1-F2 (MINOR, Docs: double-counted attribution) | **Resolved**, per R598-2 and R599-2. The PR body is unchanged since then: the disjoint -121 / -342 (nesting -344) / about -227 text is present. |
| R599-1-F1 (MINOR, Docs, Conformance: per-stream scope) | **Resolved.** The scoped text is in the composed plan unchanged (M5's plan delta has the same patch-id). |
| R598-1-S1 (partial-central consequence) | Applied at source. **Superseded at composition by R598-3-F1.** |
| R598-2-S1 (SUGGESTION: the merge candidate carries M2's measurement too) | **Escalated to R598-3-F1.** The merge turn has arrived, and M6 adds a second shortfall. |
| R598-2-RES-1, R598-2-RES-2 (PR body wording) | **Retained as RESIDUE.** The live PR body still reads "These are the route gate's own sub-block figures for the M5 route" and "nearly all of it in `u_pp`". The exact fixes are in R598-2; carry them to the residue checklist. |
| R599-1-RES-1/2/3 | **Resolved.** `milan_csr.sv` and the plan's L8 line are byte-identical to the source head, and the PR body row carries the text. |
| R599-1-S1 (alternate placement directives) | **Retained, optional.** Composition does not affect it. |

## 5. Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R598-3-F1) | `MARK_II_AREA_PLAN.md:454,539,557,699,960,1029-1048,1106,1199-1201`; `partial_central.txt`; `plan_presence.txt`. For the ABI side of composition: `milan_csr.sv` blob identical to source (`composition.txt`); `milan_datapath.sv` predecessor hunks away from the `csr` instance; M2 `milan_soc.py` `_cross_csr_bus` (unchanged widths, depths and latency). The register ABI and snapshot contracts are otherwise covered by R598-2 and R599-2 at `c0cba330`. | R598-3 | `8f0f205161fe924797ee2d494a0a79f5f6adb77a` |
| RTL | CLEAN | Composition touches RTL scope only through M6's `milan_datapath.sv` (hunks at 3450-3530, 6337) and M2's `milan_soc.py` CSR crossing. Checked with `lint_rtl_check.log` (90 <= 90 on the composed tree), `csr_make.log`, and the `composition.txt` hunk map against the `csr` instance at `milan_datapath.sv:2445-2472`. `milan_csr.sv` internals are covered by R598-2 and R599-2 at `c0cba330` and are byte-identical here. | R598-3 | `8f0f205161fe924797ee2d494a0a79f5f6adb77a` |
| Robustness | CLEAN | `csr_make.log` lock1/lock8 reset-values, snapshot-freshness and random-traffic phases on the candidate (0 mismatching cycles). Composition adds no input path to `milan_csr`. Deeper robustness is covered by R598-2 and R599-2 at `c0cba330`. | R598-3 | `8f0f205161fe924797ee2d494a0a79f5f6adb77a` |
| Tests | CLEAN | `scripts/measure_test_evidence_readers.py:62-70` (M6 entries) and `:183-187` (M5 entry), both present. `test_evidence_check.log` (0 unexplained, 0 stale), `test_evidence_selftest.log`. `csr_make.log` `lock_mutants.py` 8/8 on the candidate. `tb/` files are byte-identical to the source. | R598-3 | `8f0f205161fe924797ee2d494a0a79f5f6adb77a` |
| Docs | UNCLEAN (R598-3-F1) | Composed `MARK_II_AREA_PLAN.md` (three measurement sections, L3/L8/L9 lines, partial-central derivation, anchors, headings); `AREA_BUDGET.md:197,208`; PR #722 body. Gates: `gen_toc_*`, `em_dash_*`, `docs_check`, `doc_style`, `doc_paths` (all rc 0). | R598-3 | `8f0f205161fe924797ee2d494a0a79f5f6adb77a` |

## 6. Real limits

- **No integrated route of the composed tree.** M2, M6 and M5 each routed alone against `e8454e27`, with WNS +0.306, +0.141 and +0.097 ns. Their combined image area and timing are unmeasured, and nothing here infers them.
- **Suites I did not run:** `milan_dp`, `tcam_csr`, the firmware host tests and Yosys. The full parent, builder and Yosys banks are out of scope for this round. I read the manager's candidate-bank completion records for this head but did not reproduce or audit them.
- **Hosted checks:** not inspected for the candidate commit. The manager owns hosted and act acceptance.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.

## 7. Pending manager duties

- Resolve R598-3-F1 before merge: correct the plan sentence on the composed tree or on the source branch. Then re-review that commit.
- Optionally take R598-3-S1.
- Carry R598-2-RES-1 and RES-2 to the residue checklist.
- At the merge turn: build and gate the final current-dev candidate, with the full local bar under CONTRIBUTING 2.1 step 7, plus hosted and act acceptance. Then run post-merge containment (`check_merge_containment.py`, `check_merge_review_integrity.py`).
- The combined M2+M6+M5 area and timing remain for the week-4 re-measure (D8) and M9.

## 8. Packet

- **Scripts:** `scripts/run_gates.sh`, `scripts/partial_central.py`, `scripts/verify_clone.sh`.
- **Receipts:** under `receipts/`, listed with digests in `MANIFEST.sha256`.
- **Scratch:** the private venv, the candidate export and the raw unsanitized suite log stay in `scratch/` and are not published.

R598-3 FINISHED
