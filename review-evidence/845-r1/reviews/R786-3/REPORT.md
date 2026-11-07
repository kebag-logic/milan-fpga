[R786] POSITIVE - exact head 43410ce1ec16e08fff22c35115d1fea9a6ed78de

External independent review, round R786-3, of issue #845 / PR #847. Head `43410ce1ec16e08fff22c35115d1fea9a6ed78de`, tree `f1cb37b9893f744fef22b3190ee05b3a6aeccb64`. This is a delta review against `853ca25ae00fe26b09e019fbfe70893666617fc1`, the head R786-2 reviewed. Source base `87e9d03aa2a4797957ac0124d0c7851a2eec234c`. As briefed, #842 and #849 are not re-reviewed.

## Verdict

POSITIVE. The delta is a manager sync and nothing else. `f7e94a07` merges #849's head `697e17a4`, which carries #842's head, and `43410ce1` changes one line of `docs/DOCUMENTATION_AUDIT.md`. The merge keeps both sides whole, and the audit is exactly what `docs_inventory.py --write` produces at this head. No processor pin, RTL, gate record or area figure of #847 changes. This round has no findings. R786-2's three RESIDUE items and the optional SUGGESTIONs are retained without change. This verdict is a source review only. It is not hosted or act acceptance, not a candidate-merge validation and not merge authorization.

## The four checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Both `CHANGELOG.md` conflicts keep both entries whole, #847's first, and the contents list matches the sections | Holds | `receipts/merge_preservation.txt`. Every line #847 added (87e9d03a..853ca25a) and every line #849 added (87e9d03a..697e17a4) is present at head, and #849's side removes no lines. The section order is `processor pin 92100657` (line 56), then `station MAC from reset` (line 100), then `gPTP on the MII port` (line 123). #847's section is byte-identical to the one at 853ca25a, and only its trailing next-heading line differs. The contents list has 44 entries for 44 `##` sections, in the same order, and every anchor matches the slug of its heading (an inline check). |
| 2 | `docs/DOCUMENTATION_AUDIT.md` is exactly what `docs_inventory.py --write` gives | Holds | `receipts/docs_inventory_check.txt`: `--check` rc 0, "547 lines, ... is fresh". `receipts/docs_inventory_write_copy.txt`: `--write` on a `git archive` export of the head tree produces a file byte-identical to the committed audit. `43410ce1` changes only that file (1 insertion, 1 deletion). |
| 3 | `git diff 853ca25a..43410ce1` outside the paths #849 and #842 changed is empty | Holds | `receipts/merge/delta.txt` against `receipts/merge/side849.txt` (87e9d03a..697e17a4). The 56 delta paths are a subset of #849's side, and the complement is empty. Every #849-side path that #847 does not touch is byte-identical to `697e17a4`. The six submodule gitlinks are unchanged, and no file mode changed. |
| 4 | No file #847 changed was altered except `CHANGELOG.md` and the audit | Holds, with one disclosed auto-merge | 3 of #847's 19 paths differ from 853ca25a: `CHANGELOG.md`, the audit, and `tb/verilator/milan_dp/README.md`. The README was not a conflict. A `git merge-file` of base, ours and theirs reproduces the merge commit's blob byte for byte, and the diff from 853ca25a to head is purely #849's 129 added lines. #847's six edited lines (the `92100657` 499/499 tally and mutant table) are intact. The PR body's "Sync on #849" section discloses this auto-merge, so the brief's stricter wording is only an approximation and the tree is correct. |

## Findings

None new at this head.

## Prior public findings, at this head

| Finding | State at 43410ce1 | Evidence |
|---|---|---|
| R785-1 F1 / R786-1 F1, MAJOR (area growth, gate verdict, owner decision) | Stays resolved | Resolved at 853ca25a by R786-2. The delta does not touch `docs/design/AREA_BUDGET.md`, `docs/reference/SUBMODULES.md`, `docs/integration/BUILDING.md`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, the gate record or the pin. The #847 CHANGELOG section is byte-identical. |
| R785-1 F2 / R786-1 F2, MINOR (link-change behaviour) | Stays resolved | `SUBMODULES.md`, `docs/integration/INTEGRATION_GUIDE.md` and the #847 CHANGELOG section are unchanged by the delta. |
| R785-1 F3 / R786-1 F3, MINOR (harness sentence) | Stays resolved | `tb/verilator/pp_shadow/sim_main.cpp` is unchanged by the delta. |
| R785-1 F4 / R786-1 F4, MINOR (PR status heads) | Stays resolved | The PR body's new "Sync on #849" section names `697e17a4`, `f7e94a07` and `43410ce1`. It claims only docs gates at `43410ce1`, and this round re-ran those (see Docs). |
| R786-2-R1 RESIDUE, `docs/reference/SUBMODULES.md:615` | Retained, not fixed | The line still reads "Against that record, `check` exits 0 on every endpoint." The exact fix is unchanged: "Against the thirteenth record, `check` exits 0 on every endpoint." |
| R786-2-R2 RESIDUE, `CHANGELOG.md` | Retained, not fixed | The line moved from 89 to 90 because the contents list grew by one entry. It still reads "- The shipping route grows 503 LUTs and 478 FFs." The exact fix is unchanged: "- On ExtraPostPlacementOpt the route grows 503 LUTs and 478 FFs." |
| R786-2-R3 RESIDUE, PR body Round 2 table, F1 row | Retained, not fixed | The row still reads "The gate ran in its own form Answered in [Round 3]...". The exact fix is unchanged: insert ` | ` before "Answered". |
| R785-1 S1, S2; R786-1 S1, S2; R786-2-S1, S2 | Retained, optional | Not affected by the delta. |

## Lens results at this head

```text
[R786] PASS Conformance - CHANGELOG.md:56-122, receipts/merge_preservation.txt - #847's 92100657 entry is byte-identical to 853ca25a and comes first; #849's #839 entry follows it whole; no pin, gitlink or normative page of #847 changed (gitlinks equal, AREA_BUDGET/SUBMODULES/INTEGRATION_GUIDE untouched)
[R786] PASS RTL - receipts/merge/delta.txt, receipts/merge/side847.txt - no #847 RTL path and no processor gitlink changed; the only RTL in the delta, hdl/milan/milan_datapath.sv, is a #849-side path byte-identical to 697e17a4 (out of scope)
[R786] PASS Robustness - tb/verilator/milan_dp/README.md three-way reproduction in receipts/merge_preservation.txt - the one non-conflict overlap is a clean textual merge with #847's lines intact; no #847 behaviour or configuration path is altered by the sync
[R786] PASS Tests - receipts/merge/delta.txt; receipts/ci_differential.txt - #847's harness and gate files (pp_shadow sim_main.cpp, gate record) are unchanged; ci_differential.py --check rc 0, 224 fixtures; test files in the delta are #849/#842's, byte-identical to 697e17a4
[R786] PASS Docs - docs/DOCUMENTATION_AUDIT.md, CHANGELOG.md:9-53, PR body "Sync on #849" - audit byte-identical to --write output, --check rc 0; contents list 44/44 in order with matching anchors; docs_check.py rc 0 (0 findings, 214 md files); check_doc_style.py rc 0; git diff --check 853ca25a..43410ce1 rc 0; PR body accurately states the two conflicts and the README auto-merge
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CHANGELOG.md` both entries; gitlinks; the normative pages of #847, confirmed untouched | R786-3 | 43410ce1ec16e08fff22c35115d1fea9a6ed78de |
| RTL | CLEAN | Delta path set against #847's and #849's sides; no #847 RTL or pin change | R786-3 | 43410ce1ec16e08fff22c35115d1fea9a6ed78de |
| Robustness | CLEAN | `tb/verilator/milan_dp/README.md` three-way reproduction; per-path blob equality | R786-3 | 43410ce1ec16e08fff22c35115d1fea9a6ed78de |
| Tests | CLEAN | #847's harness and gate files unchanged; `ci_differential.py --check` | R786-3 | 43410ce1ec16e08fff22c35115d1fea9a6ed78de |
| Docs | CLEAN | Audit regeneration; CHANGELOG contents; `docs_check.py`, `check_doc_style.py`, `git diff --check`; PR body sync section | R786-3 | 43410ce1ec16e08fff22c35115d1fea9a6ed78de |

Coverage that R786-2 banked at 853ca25a for #847's own artifacts carries to this head. 853ca25a is an ancestor of this head, and the delta touches nothing in #847's scope except the CHANGELOG, the audit and the auto-merged README, all of which this round covered.

## Real limits

- `gen_toc.py --check` was not run here. The pinned Markdown renderer (html5lib) is not installed in this environment, and installing it would be a shared install. The contents list was checked directly instead (44/44, order and anchors). The manager reports that `gen_toc.py --check` passes.
- The `--write` comparison ran on a `git archive` export, which carries no submodule contents. The output was byte-identical anyway, and `--check` in the full clone also passed.
- #842 and #849 content was not reviewed, as briefed. Their paths were only confirmed to match `697e17a4` byte for byte.
- No simulation, synthesis or gate bank ran. None was needed, because no #847 RTL, harness, pin or gate input changed.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Hosted contexts at this head were still running when they were captured (`receipts/hosted_check_runs.txt`: 22 success, 1 skipped, 28 queued or in progress, 0 failed). That is a snapshot, not acceptance.

## Pending manager duties

- Act at this head: not run yet. This is open and is not a finding.
- Hosted `rtl-fast`, `verilator-suites` and `yosys-portability` completion on the exact head.
- Current-dev candidate-merge validation, with builder and native banks, at the merge turn. Source base 87e9d03a, live dev 35448611.
- Carry R786-2-R1, R2 and R3 to the residue checklist.
- The other independent review, and maintainer merge authorization.

Clone restored: HEAD `43410ce1ec16e08fff22c35115d1fea9a6ed78de`, index clean, no untracked or ignored files, and the six gitlinks unchanged.

R786-3 FINISHED
