[R600] POSITIVE - exact head 1a042affce2f252f10ed40b3ec25659611b3974b

# R600-3: composition re-review of PR #719 (issue #640, Mark II lane M6) on the merge-train candidate

- Exact head: `1a042affce2f252f10ed40b3ec25659611b3974b`, tree `9ef4b6a221a43ec301f137501e948ba8ad2b9239`.
- Parents: dev `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5` (M2, PR #710) and PR source head `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`. Merge base `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Role: internal cleared-context reviewer, composition round (delta after R600-2). All five lenses are applied to what the composition can change. The source head has two POSITIVE source reviews, R600-1 and R601-1, both at `ee0fc6fd9`.

## Verdict

POSITIVE. R600-2-F1 is resolved:
- `gh pr view 719 --json closingIssuesReferences` returns `[]` (`receipts/pr719.json`).
- The PR body line 22 now reads "It leaves #640 open." Issue #640 is OPEN (`receipts/issue640_state.json`).

The candidate head and tree are the ones R600-2 judged. The composed tree introduces no defect beyond the reviewed sources. No BLOCKER, MAJOR or MINOR finding is open. Two RESIDUE items and the optional SUGGESTIONs from earlier rounds are retained.

## Reconstruction

1. AGENTS.md and CONTRIBUTING.md (lens contract and completion bar), then docs/README.md.
2. Issue #640, in its frozen state. The acceptance is a routed image of at most 38,040 LUT with timing met and function unchanged. The gate record stays under D7 until M9. Lane M6's assignment says no change to shipping behaviour, the register map or the wire format.
3. The shared authorities: `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/AREA_BUDGET.md` and `docs/testing/TESTING.md`.
4. `git diff ac2c5e77..1a042aff` and the history.
5. The manager's candidate banks, read only.
6. Prior public findings on PR #719, read only after this round's own pass and ledger arithmetic.

## Head and tree identity, unchanged since R600-2

Receipt: `receipts/composition/composition.txt`.

- HEAD is `1a042aff` and its tree is `9ef4b6a2`. R600-2 judged the same head and tree.
- `git merge-tree --write-tree ac2c5e77 ee0fc6fd9` reproduces `9ef4b6a2`: the candidate is the clean merge.
- The remote PR head is still `ee0fc6fd9` (`receipts/pr719.json`, `headRefOid`).
- The candidate differs from dev in exactly the PR's 19 files, and from the PR head in exactly M2's 13 files. Both `comm` residues are empty.

## PR body and closing references (the F1 delta)

Receipts: `receipts/pr719_body_edits.json` and `receipts/pr719_body_diff.txt`.

- The PR body's edit history shows one edit since publication, at 2026-10-11T10:27:10Z. The current body equals that edit.
- The diff against the prior body is line 22, from "It must not close #640." to "It leaves #640 open.", plus one trailing blank line at the end. Nothing else changed.
- A keyword scan of the body finds no closing keyword (close/fix/resolve forms) before any issue number. "Relates to #640" (line 20) is not a closing keyword.
- None of the 8 commit messages in `ac2c5e77..1a042aff` carries a closing keyword.
- The repository default branch is `dev`. With `closingIssuesReferences=[]`, the merge closes no issue.

## Composition analysis (independent pass)

Since the merge base, the files both lanes change are exactly `docs/design/AREA_BUDGET.md`, `docs/design/MARK_II_AREA_PLAN.md` and `docs/testing/TESTING.md`. This matches the manager's list.

**Ledger arithmetic.** `ledger_arith.py` was run on the merged text: 45/45 PASS (`receipts/composition/composition.txt`).
- Both base rows equal the record figure, 50,267 LUT.
- The routed LUT/FF/slice and WNS/WHS deltas recompute from each lane's own route. M2: -128/-59/-8, +0.007/-0.012. M6: -706/-958/+12, -0.158/-0.013.
- M6's credited blocks sum to 468 routed and 418 post-synthesis. The two unchanged blocks are not credited.
- M2's 34 and M6's 418/468 match:
  - the plan pointers at `MARK_II_AREA_PLAN.md:454` and `:556`;
  - the AREA_BUDGET notes at `:197` and `:208`.
- The cumulative table (`MARK_II_AREA_PLAN.md:971-982`) and the AREA_BUDGET lane table (`:184-195`) recompute row by row. They list M2 and M6 once each, at their planning figures, as both lanes state. Central headroom is 6,373.
- No combined M2+M6 measured figure is claimed. No row is counted twice or lost.

**The arithmetic check can fail.** Four planted errors were each caught (`receipts/composition/ledger_probes.txt`), all made on scratch copies:
- an M6 block figure;
- an M6 cumulative saving;
- the M2 L3 pointer;
- the AREA_BUDGET M6 note.

**TESTING.md.** Both suite texts remain:
- M2's `test_retained_cdc_storage.py` paragraph at `docs/testing/TESTING.md:681`;
- M6's `avtp_rxmon` and `chmap_capture` rows at `:582` and `:587`.

**RTL surface.**
- Between the candidate and the reviewed PR head, the only `hdl/` or `tb/` differences are M2's regenerated `tb/verilator/gptp_txts/generated/mac_tx_chain.v` and `manifest.json`.
- M6 changes 0 port or parameter lines in `milan_datapath.sv` or `KL_pp_shadow.sv`.
- M2's SoC edits (`sw/litex/milan_soc.py`) name none of M6's modules or signals.

## Executions this round, at the exact head

These runs were in the foreground, in this clone. The interpreter was the pinned Markdown-renderer environment (CPython 3.14.7, cmarkgfm 2025.10.22, html5lib 1.1). `ci_events` ran under the system CPython 3.14.7 with pyyaml 6.0.3, because the renderer environment has no pyyaml (`receipts/env_and_banks.txt`).

| Gate | rc | Result line |
|---|---:|---|
| `docs_check.py` | 0 | 0 findings across 203 md files |
| `gen_toc.py --check` | 0 | 143 pages OK |
| `gen_toc.py --verify-anchors` | 0 | 470 cross-page fragment links reproduced |
| `check_em_dash.py --base ac2c5e77` | 0 | 0 findings over 53 added lines, 3 pages |
| `check_em_dash.py --base e8454e27` | 0 | 0 findings over 1,236 added lines, 7 pages |
| `check_em_dash.py --selftest` | 0 | 339 arms |
| `check_doc_style.py` | 0 | 22 documents OK |
| `check_doc_paths.py` | 0 | 961 cited paths resolve |
| `ci_events.py --check` | 0 | 1,749 contract items |
| `ci_scope.py --selftest` | 0 | PASS |
| `measure_test_evidence.py --check` | 0 | 0 <= 0 unexplained DUT-source readers |
| `docs/DOC_MAP.gen.py --check` | 0 | OK |

Receipts: `receipts/gates/*.log`, `*.rc` and `SUMMARY.txt`. Gate runner: `run_gates.sh`. Composition and integrity script: `composition_check.sh`.

I did not re-run the rest of R600-2's 35-gate set, its anchor probes or its line-survival check. The tree is byte-identical, so its receipts stand for this tree, as the round's brief permits.

**Manager candidate banks, read only and not re-run** (`receipts/env_and_banks.txt`, with sha256 of both `results.json`):
- Builder: 48/48 rc 0 at head `1a042aff`, base `ac2c5e77`.
- Native: 5/5 rc 0.
- The lockstep legs: `avtp_rxmon` N=1 and N=8 at 36 checks / 0 failures each; `chmap_capture` 4 and 32 slots at 19 / 0 each.

These are the manager's receipts, cited as such.

**Clone integrity.**
- After all runs: 0 status lines (untracked included), `diff-index` rc 0, and worktree equal to index.
- The gitlinks are as recorded. `protocol-processor` (`2ad2f845`) and `gptp-processor` (`5dce647a`) are checked out clean.
- No probe touched the clone. All planted errors were made on scratch copies.

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

### R600-2-F1 - MINOR - Conformance, Docs - PR #719 body line 22 - RESOLVED at this head

- **Evidence:** `closingIssuesReferences` is `[]` and #640 is OPEN. The body diff shows only line 22 reworded, plus a trailing blank line. No other closing keyword appears in the body or in the commits.
- **Remaining verification (manager):** confirm #640 is still OPEN after the merge lands.

### Retained from earlier rounds

The artifacts are unchanged at this head, so each item below is retained as published.

- **R600-1-RES1 - RESIDUE - Docs:** stale monitor line citations in `docs/design/MEDIA_CLOCK_FOLLOWING.md:315,317,459,960`. M2 does not touch that file, so it is byte-identical to the source head. The exact fix is as R600-1 published it. Goes to the residue checklist.
- **R601-1-R1 - RESIDUE - Docs:** the PR body "Status" line 16 still reads "GREEN at `ee0fc6fd9`: ...". This round confirms that line is unchanged. The exact fix is as R601-1 published it. Goes to the residue checklist.
- **R600-1-S1 (RTL), R601-1-S1 (Tests), R601-1-S2 (Tests, Robustness), R601-1-S3 (Docs):** SUGGESTION, retained. Their files are byte-identical at the candidate.
- **R600-2-S1 - SUGGESTION - Docs:** the M2 and M6 notes sit apart in `AREA_BUDGET.md:197-210` and in the plan (`:673`, `:920`). Retained, optional, for the week-4 re-measure.
- **R600-2-S2 - SUGGESTION - Docs:** the deferral text at `MARK_II_AREA_PLAN.md:834,861` and `AREA_BUDGET.md:270,278` still names M6 as a block-RAM consumer, although M6 measures no tile. This round reached the same observation independently.
  - It is identical at the reviewed source head, so the composition does not introduce it.
  - Retained, optional.

## Lens results

```text
[R600] PASS Conformance - receipts/pr719.json (closingIssuesReferences []), receipts/pr719_body_diff.txt, receipts/issue640_state.json, receipts/composition/composition.txt - R600-2-F1 resolved: the merge closes no issue and #640 stays OPEN against its unmet frozen acceptance; the composition carries no port, parameter, register-map or wire change into M6's blocks (0 port/parameter lines; M2 confined to sw/litex, run_litex_sims.sh and gptp_txts generated files); manager banks 48/48 and 5/5 at 1a042aff
[R600] PASS RTL - receipts/composition/composition.txt (hdl/tb differences vs ee0fc6fd9 limited to tb/verilator/gptp_txts/generated/*; 0 port lines in milan_datapath.sv and KL_pp_shadow.sv) at 1a042aff - the composition touches no RTL in M6's scope; M6 RTL is covered by the source reviews R600-1 and R601-1 at ee0fc6fd9
[R600] PASS Robustness - receipts/env_and_banks.txt (lockstep hazard legs N=1/N=8 and 4/32 slots, 0 failures, at 1a042aff) - no path, reset, capacity or configuration change enters through the merge; source robustness coverage stands (R600-1, R601-1 at ee0fc6fd9)
[R600] PASS Tests - docs/testing/TESTING.md:582,587,681; receipts/gates/{test_evidence_check,ci_events_check,ci_scope_selftest}.log; receipts/composition/ledger_probes.txt - both lanes' suite texts survive; the test-evidence, CI-event and CI-scope inventories reconcile on the composed tree; this round's arithmetic check is shown able to fail
[R600] PASS Docs - docs/design/AREA_BUDGET.md:184-210, docs/design/MARK_II_AREA_PLAN.md:454,556,673-702,920-990, docs/testing/TESTING.md:579-695, PR #719 body - ledger arithmetic 45/45 on the merged text; docs_check, gen_toc --check/--verify-anchors, check_em_dash (both ranges), doc_style, doc_paths and DOC_MAP --check rc 0; F1 resolved; two RESIDUE items retained for the checklist; SUGGESTIONs optional
```

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Composition touches it only through the PR closing reference (F1, now resolved) and the absence of an ABI change. Issue #640 acceptance; PR body and its edit diff; `closingIssuesReferences`; #640 state; port-line count; manager banks | R600-3 (composition); source: R600-1, R601-1 | `1a042affce2f252f10ed40b3ec25659611b3974b`; source `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` |
| RTL | CLEAN | Composition does not touch its scope: the only hdl/tb differences from the source head are M2's gptp_txts generated files, and there are 0 port or parameter lines. Covered by the source reviews. | Source: R600-1, R601-1; R600-2 and R600-3 confirm no interaction | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`; `1a042affce2f252f10ed40b3ec25659611b3974b` |
| Robustness | CLEAN | Composition does not touch its scope. Lockstep hazard legs pass in the manager's candidate banks. Covered by the source reviews. | Source: R600-1, R601-1; R600-3 confirms | `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937`; `1a042affce2f252f10ed40b3ec25659611b3974b` |
| Tests | CLEAN | Composition touches TESTING.md and the test-evidence registry. Suite texts at `:582,587,681`; test_evidence, ci_events and ci_scope gates; ledger probes | R600-3 | `1a042affce2f252f10ed40b3ec25659611b3974b` |
| Docs | CLEAN (RESIDUE R600-1-RES1 and R601-1-R1 carried; SUGGESTIONs optional) | Composition touches the three shared documents and the PR body. Ledger arithmetic; anchors and TOC; em-dash; style and path gates; PR body diff | R600-3 | `1a042affce2f252f10ed40b3ec25659611b3974b` |

## Real limits

- **No combined route.** The composed image (M2 + M6) has not been routed. Each lane was measured alone against `e8454e27`. The merged text claims no combined figure, and the gate record stays under D7.
- **Simulation banks not re-run.** The suite, lockstep and builder results at this head are the manager's banks, read only.
- **Gates not re-run this round.** The R600-2 gates outside the twelve above were not re-run. They are cited for the byte-identical tree.
- **M2's LiteX test was not run.** `test_retained_cdc_storage.py` did not run here, and the manager's banks show no log for it. Its inputs are byte-identical between dev and the candidate.
- **Gate interpreter.** Gates ran under CPython 3.14.7, not the hosted 3.12.
- **No hardware.** Physical calibration NOT RUN. Hosted skips are not hardware proof.
- **No hosted run for the candidate.** The candidate is not on the remote, so no hosted run exists for it. Hosted and local-replica acceptance belong to the manager.

## Pending manager duties

- At the merge turn, validate the current-dev candidate. If dev has moved past `ac2c5e77`, rebuild it and re-run the shared-file gates and `ledger_arith.py`.
- After the merge, confirm #640 is OPEN.
- Hosted and local-replica acceptance at the merged head.
- Carry R600-1-RES1 and R601-1-R1 to the residue checklist. Carry R600-2-S1 and S2 to the week-4 re-measure.
- Schedule the composed route for the week-4 re-measure or M9.

R600-3 FINISHED
