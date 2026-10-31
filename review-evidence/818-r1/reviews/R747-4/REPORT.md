[R747] POSITIVE - exact head 81f78a81e1271185174f9c5dbbcc8469b5dab5b4

Round R747-4, internal independent review of PR #820 for issue #818. Head `81f78a81e1271185174f9c5dbbcc8469b5dab5b4`, tree `afee23b50c63018f06bbf5c7a60a294eba6776b5`.

Verdict basis: R747-3 F1 (MINOR, Docs and Conformance) is resolved at its cause. No BLOCKER, MAJOR or MINOR is open. One new RESIDUE (RS-4a, line layout). The earlier RESIDUE and SUGGESTION items are carried unchanged.

## Delta reviewed

The delta from the reviewed head `50e5d08d` to `81f78a81` has two commits:

1. `17fd6f73` merges live dev `02ca829a` (PR #813 for #806, PR #821 for #817, PR #816 for #70). The merge commit's tree is `0761e4747b37842755934727a42af9e940736436`. That equals `git merge-tree --write-tree 02ca829a 50e5d08d` (`receipts/merge_tree.txt`). It is also the composition candidate tree R747-3 reviewed. So the merge has no authored resolution bytes. The gitlinks equal dev's: gptp-processor `135afd04`, protocol-processor `f65c8ff7`, external `efeb541a` (`receipts/final_state.txt`).
2. `81f78a81` is the only authored change. It is a one-line commit message with no trailers, and it changes three files: `CHANGELOG.md` (+2/-1), `docs/design/AREA_BUDGET.md` (+2/-1) and `docs/reference/SUBMODULES.md` (+5/-1). It adds no source code and no source comments, so the comment rule is not engaged.

The merge leaves the #818 gate and its tests unchanged: `git diff 50e5d08d 81f78a81 -- syn/ooc` is empty. From dev, the merge touches only `AREA_BUDGET.md:143-145` (the #806 slice and timing sentences, the subject of F1), `BUILDING.md:622-628` (the #817 reset-synchronizer cut, outside section 5's gate rule) and `scripts/port_docs.budget` (port counts).

## Prior findings, resolved or retained at this head

| Finding | Status | Evidence |
|---|---|---|
| R747-3 F1 MINOR Docs, Conformance: tree says the gate refuses the `135afd04` route's 0.408 ns fall | RESOLVED | See below |
| R747-3 OBS-1 SUGGESTION Tests, Docs: three stale command-table pins inherited from `50e5d08d` | RETAINED, routed to the residue checklist by the manager; not judged this round | `ci/image/command-table.json` is not in the delta |
| R747-2 RS1 RESIDUE: PR body "Round 2 mutants, each killed by the arm written for it" | RETAINED as RESIDUE | still in the PR body (`receipts/pr820_body_at_review.md:89`) |
| R748-2 R2 RESIDUE: PR body file table, stale arm and mutant counts | RETAINED as RESIDUE | PR body not corrected for it |
| R748-2 S1 SUGGESTION: `bound()` sub-conditions without an arm | RETAINED, optional | `syn/ooc` unchanged |
| R747-1 three SUGGESTIONs | RETAINED, optional | gate, self-test and recipe bytes unchanged |
| R748-1 F1, F2, F3 MINOR | RESOLVED earlier (R747-2, R748-2, R747-3); unchanged by this delta | `syn/ooc` and `MARK_II_AREA_PLAN.md` unchanged |

F1 resolution evidence:
- `docs/design/AREA_BUDGET.md:144-145`: "That route meets the build floor at every corner, at +0.032 / +0.034 ns. Its WNS is 0.408 ns under the record's, beyond the 0.25 ns fall tolerance." / "Before #818 the gate refused that fall; under #818 it prints a WARNING and passes."
- `docs/reference/SUBMODULES.md:425-429`: "The tolerance is 0.25 ns." / "Before #818 the gate refused that fall." / "Under #818 the fall prints a WARNING and passes."
- `CHANGELOG.md:75-76`: "Before #818 the gate refused that 0.408 ns fall." / "Under #818 that fall is a WARNING."
- The figures are unchanged: +0.032 / +0.034 ns, 0.408 ns, +0.440 ns and 0.25 ns all match the pre-commit text and `SUBMODULES.md:417-423` and `CHANGELOG.md:71-74`.
- `git grep -n 'gate refuses'` (`receipts/grep_gate_refuses.txt`) finds no statement about this route. The remaining hits cover other subjects: tool or recipe change at `AREA_BUDGET.md:539`, em dash, Mark II placement and others. `git grep -n '0\.408'` (`receipts/grep_0408.txt`) finds only the three lines above, and none states a present refusal.
- The new text matches the gate in the same tree. `syn/ooc/pp_resource_gate.py:32` says a fall beyond the timing fall "prints a WARNING and never" fails, and `:547` and `:577` emit the WARNING. The section-4 rule at `AREA_BUDGET.md:444` says the same.
- "Passes" does not overclaim for this route's other rows. The route places 15,823 slices against the record's 15,780 (+43). The route slice tolerance is 80 (`syn/ooc/pp_resource_baseline.json:455`), and the route is 175 LUTs under the record.

## Findings

### RS-4a RESIDUE Docs - docs/design/AREA_BUDGET.md:144 - two sentences on one source line

Authority/evidence: the surrounding paragraph (`AREA_BUDGET.md:142-149`) puts one sentence per source line, and the line was one sentence before this commit. The page is not in `check_doc_style.py`'s scope, so no gate catches this.
Impact: layout only. It changes no figure, verdict or claim.
Exact fix: break line 144 after "+0.032 / +0.034 ns." so that "Its WNS is 0.408 ns under the record's, beyond the 0.25 ns fall tolerance." stands on its own line.
Verification: `sed -n 144,146p docs/design/AREA_BUDGET.md` shows one sentence per line, and `gen_toc.py --check` and `docs_check.py` still pass.

No other finding. The commit introduces no new source comment, lane label, reviewer ID or comment ID.

## Clean lenses

- `[R747] PASS Conformance - docs/design/AREA_BUDGET.md:143-145, docs/reference/SUBMODULES.md:417-429, CHANGELOG.md:71-77 against the #818 rule ("The fall from the record is computed and printed as WARNING, with no failure") and syn/ooc/pp_resource_gate.py:32,547,577 - the route's 0.408 ns fall is stated as refused before #818 and a WARNING under it, with the floor met at every corner; figures unchanged.`
- `[R747] PASS RTL - git diff 50e5d08d 81f78a81 (authored commit: three Markdown files; merge tree 0761e474 = merge-tree(02ca829a, 50e5d08d)) - the delta adds no #818-scope RTL or gate logic; the dev RTL came in through a clean merge of separately reviewed PRs, and the gitlinks equal dev's.`
- `[R747] PASS Robustness - syn/ooc/* byte-identical 50e5d08d..81f78a81; receipts/check_baseline.log (baseline PASS: 3 endpoints) - the gate's inputs, refusal paths and policy table are unchanged; the page the gate reads still parses.`
- `[R747] PASS Tests - syn/ooc self-test and mutant sources unchanged since 50e5d08d; R747-3's gate bank ran on tree 0761e474, the exact merge-commit tree; check-baseline re-run rc 0 at this head - the docs commit touches no test or test input.`
- `[R747] PASS Docs - receipts/{doc_style,toc_check,toc_anchors,docs_check,doc_paths,em_dash,em_dash_srcbase}.log, all rc 0 at 81f78a81; F1 text at AREA_BUDGET.md:144-145, SUBMODULES.md:425-429, CHANGELOG.md:75-76 - no present-tense refusal remains; RS-4a is wording only and carried as RESIDUE.`

Gate results at this head (`receipts/*.rc`):
- `check_doc_style.py` OK (23 documents).
- `gen_toc.py --check` OK (149 pages).
- `gen_toc.py --verify-anchors` OK (544 links).
- `docs_check.py` 0 findings.
- `check_doc_paths.py` OK (1074 paths).
- `check_em_dash.py --base 17fd6f73` found 0 findings over 9 added lines. `check_em_dash.py --base 1e80128f` found 0 over 325 added lines.
- `pp_resource_gate.py check-baseline` PASS on 3 endpoints.

## Ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #818 body; `AREA_BUDGET.md:143-145,444`; `SUBMODULES.md:417-429`; `CHANGELOG.md:71-77`; `pp_resource_gate.py:32,547,577`; `pp_resource_baseline.json:455` | R747-4 | `81f78a81e1271185174f9c5dbbcc8469b5dab5b4` |
| RTL | CLEAN | Authored diff (Markdown only); merge-tree identity; gitlinks | R747-2 / R748-2 for #818 scope at `50e5d08d`; R747-4 confirms nothing in scope changed | `81f78a81e1271185174f9c5dbbcc8469b5dab5b4` (scope unchanged since `50e5d08d`) |
| Robustness | CLEAN | `syn/ooc` unchanged; `check-baseline` rc 0 | R747-2 / R748-2 at `50e5d08d`; R747-4 re-ran `check-baseline` | `81f78a81e1271185174f9c5dbbcc8469b5dab5b4` |
| Tests | CLEAN | `syn/ooc` self-test and mutant sources unchanged; R747-3 gate bank on tree `0761e474` (the merge-commit tree); `check-baseline` rc 0 | R747-3 (tree `0761e474`); R747-4 | `81f78a81e1271185174f9c5dbbcc8469b5dab5b4` |
| Docs | CLEAN (RS-4a RESIDUE carried) | Three edited pages; seven docs gates rc 0 | R747-4 | `81f78a81e1271185174f9c5dbbcc8469b5dab5b4` |

## Limits

- No full parent, PP, gPTP, Yosys or builder bank was run. No manager source bank exists at this head, and none is claimed or inferred.
- The `syn/ooc` self-test and mutant runs were not re-run here. They are unchanged since `50e5d08d`, and R747-3 ran them on the identical merge tree.
- The renderer-dependent gates used a private venv under `scratch/`, built with `tools/markdown/requirements.txt --require-hashes` (cmarkgfm 2025.10.22, html5lib 1.1). Under `python3 -I`, `check-baseline` cannot import its sibling module `pp_baseline_rank`. It was run without `-I` from the trusted head checkout.
- Hosted runs for this exact head were still queued or in progress when inspected. "Physical gPTP" was skipped. The manager owns hosted and act acceptance.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The author evidence commit `75d730df` (`review-evidence/818-r1`) is unsigned (verification `unsigned`). It holds receipts for earlier heads only, and no author receipt for `81f78a81` was found there. This round's gate evidence is its own receipts.
- No probe modified the clone. HEAD, the index and the worktree are clean, and the gitlinks are recorded in `receipts/final_state.txt`.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Accept the exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` results and the act replica.
- Carry RS-4a, R747-2 RS1 and R748-2 R2 (wording) and OBS-1 (pins) to the residue checklist.
- Obtain explicit maintainer authorization before any merge.

R747-4 FINISHED
