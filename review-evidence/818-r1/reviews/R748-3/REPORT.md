[R748] POSITIVE - exact head 81f78a81e1271185174f9c5dbbcc8469b5dab5b4

Round R748-3, external independent review of PR #820 (issue #818). Tree `afee23b50c63018f06bbf5c7a60a294eba6776b5`.
Previous reviewed head `50e5d08d`. Delta: merge `17fd6f73` of live dev `02ca829a` (PR #813 for #806, PR #821 for #817, PR #816 for #70), plus one docs commit `81f78a81` for R747-3 F1.

Verdict basis: the merge adds no bytes of its own. The docs commit meets F1's required outcome, keeps every figure and passes every gate F1 named. No open MINOR, MAJOR or BLOCKER.

## Composition identity

| Check | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree 02ca829a 50e5d08d` | `0761e4747b37842755934727a42af9e940736436`, no conflict | `receipts/merge_tree.txt` |
| `17fd6f73^{tree}` | `0761e4747b37842755934727a42af9e940736436`: equal. This is also the candidate tree R747-3 published for `ffe3a631` (that commit is not fetchable from the remote, so the tree id is the comparison) | `receipts/merge_tree.txt` |
| Gitlinks at head | `external` `efeb541a`, `gptp-processor` `135afd04`, `protocol-processor` `f65c8ff7`; same set as dev `02ca829a` | `receipts/restore_check.txt` |
| Authored delta `17fd6f73..81f78a81` | 3 Markdown files, +9 / -3 lines, no source file, no source comment | `receipts/docs_commit.diff`, `receipts/docs_commit_stat.txt` |

## F1 outcome check (R747-3 F1, MINOR Docs, Conformance)

- `docs/design/AREA_BUDGET.md:144-145`: "That route meets the build floor at every corner, at +0.032 / +0.034 ns. Its WNS is 0.408 ns under the record's, beyond the 0.25 ns fall tolerance." / "Before #818 the gate refused that fall; under #818 it prints a WARNING and passes."
- `docs/reference/SUBMODULES.md:421-429`: "+0.032 ns WNS", "0.408 ns under the record", "+0.440 ns", "The tolerance is 0.25 ns.", "Before #818 the gate refused that fall.", "Under #818 the fall prints a WARNING and passes."
- `CHANGELOG.md:73-76`: "+0.032 ns", "+0.440 ns, tolerance 0.25", "Before #818 the gate refused that 0.408 ns fall.", "Under #818 that fall is a WARNING."
- Figures are unchanged against `17fd6f73`: the diff touches only the refusal clauses. The record agrees: `syn/ooc/pp_resource_baseline.json` route-1x1 has WNS 0.44, WHS 0.036, timing tolerance 0.25 and floors 0.03 / 0.0 (`receipts/baseline_timing.txt`). 0.440 - 0.032 = 0.408.
- "passes" is true of the gate at head. `syn/ooc/pp_resource_gate.py:574-578` adds the fall as a WARNING note and returns pass unless a corner misses the floor (`:572`), and +0.032 / +0.034 are above 0.03. The route's other figures are inside tolerance too: slices 15,823 against the record's 15,780 is +43 against SLICE 80 (`AREA_BUDGET.md:137,143`), and LUTs are 175 under the record against LUT 500.
- `git grep -n 'gate refuses'` (`receipts/grep_gate_refuses.txt`, 34 lines): no line refers to WNS, the fall or the `135afd04` route. Every hit is another gate's refusal (exit 2 on a tool change, the em-dash gate, coverage ratchet, and others). `git grep -n '0\.408'` outside history and evidence has three hits, all past-tense or figure-only (`receipts/grep_0408.txt`). A wider search for `refus` near WNS, timing or fall in `AREA_BUDGET.md`, `BUILDING.md` and `SUBMODULES.md` finds only the lines above. The `refused` rows at `SUBMODULES.md:306-308` are a prior adoption's LUT verdicts.

F1: RESOLVED at this head.

## Gates run at this head (foreground, receipts in `receipts/`)

| Gate | Result | Receipt |
|---|---|---|
| `scripts/check_doc_style.py` | OK (23 current documents), rc 0 | `doc_style.log` |
| `scripts/gen_toc.py --check` | OK (149 pages), rc 0 | `gen_toc_check.log` |
| `scripts/gen_toc.py --verify-anchors` | 544 fragment links reproduced, rc 0 | `gen_toc_anchors.log` |
| `scripts/docs_check.py` | 0 findings over 210 md and 1425 text files, rc 0 | `docs_check.log` |
| `scripts/check_doc_paths.py` | OK (1074 paths), rc 0 | `doc_paths.log` |
| `scripts/check_em_dash.py --base 17fd6f73` | 0 findings over 9 added lines in 3 pages, arms 339/339, rc 0 | `em_dash.log` |
| `syn/ooc/pp_resource_gate.py check-baseline` | baseline PASS: 3 endpoints, rc 0 | `resource_baseline.log` |

The renderer gates ran with the pinned `tools/markdown/requirements.txt` set (cmarkgfm 2025.10.22, html5lib 1.1), installed by hash into a disposable venv under `scratch/`. The first attempt without it exited 2 ("cannot judge") and was rerun. `pp_resource_gate.py` runs without isolated mode because it imports its sibling `pp_baseline_rank`. `verify.sh` reproduces every check.

## Findings

### R1 RESIDUE Docs - PR #820 body, Status line (`receipts/pr820_body_at_review.md:16`) - REVIEW READY pointer names the previous head and base

Evidence: the body reads "**REVIEW READY** at `50e5d08d...`; `818-wns-gate` -> `dev` (`1e80128f`, the live tip)". The PR head is `81f78a81`, and live dev is `02ca829a`. The new head is stated publicly in the author's PR comment for F1, not in the body.
Impact: wording only. No measurement, figure, verdict or test claim changes, and the gate evidence the body lists is unaffected by a docs-only delta.
Exact fix: change the Status line to "REVIEW READY at `81f78a81e1271185174f9c5dbbcc8469b5dab5b4`; `818-wns-gate` -> `dev` (`02ca829a`). Round 3 merges dev `02ca829a` and adds one docs commit for R747-3 F1." Add a matching row to the round table.
Verification: read the PR body.

### S1 SUGGESTION Docs - `CHANGELOG.md:52-80` - #818's verdict change is recorded only inside #806's entry

Evidence: the only `#818` lines in `CHANGELOG.md` are `:75-77`, inside "Unreleased - gPTP pin 135afd04". F1 allowed this ("Either qualify it the same way, or have #818 add an entry").
Impact: none on correctness. A reader scanning for the resource gate change has to find it inside the gPTP pin entry.
Optional outcome: one #818 entry stating that a timing fall beyond the tolerance now prints a WARNING and does not fail, and that floors are judged at every signoff corner.

No new source comment is in the delta, so the comment rule has no new instance.

## Prior public review findings (read after the independent pass above)

| Finding | Status at this head | Basis |
|---|---|---|
| R747-3 F1 MINOR Docs, Conformance: present-tense refusal of the 0.408 ns fall | RESOLVED | section "F1 outcome check" |
| R747-3 OBS-1 SUGGESTION Tests, Docs: three stale command-table pins | RETAINED, routed to the residue checklist by the manager | `ci/image/command-table.json` not in the delta |
| R748-1 F1, F2, F3 MINOR | RESOLVED, unchanged | `MARK_II_AREA_PLAN.md` and `syn/ooc/*` not in `50e5d08d..81f78a81` |
| R748-1 R1 RESIDUE (PR-body mutant claim) | RESOLVED, unchanged | PR body line 19 states the exact counts |
| R748-1 S1 SUGGESTION (`bound()` sub-conditions) | `bound()` part RETAINED, optional | gate bytes unchanged |
| R747-1 three SUGGESTIONs | RETAINED, optional | gate, selftest and recipe bytes unchanged |
| R747-2 RS1 RESIDUE: "Round 2 mutants, each killed by the arm written for it" | RETAINED as RESIDUE | still at `receipts/pr820_body_at_review.md:89` |
| R748-2 R2 RESIDUE: PR-body file table, stale arm and mutant counts | RETAINED as RESIDUE | body line 76 says "38 new mutants"; line 19 says 44 new |

## Lens results (clean lenses in findings format)

- `[R748] PASS Conformance - docs/design/AREA_BUDGET.md:144-145, docs/reference/SUBMODULES.md:421-429, CHANGELOG.md:73-76 against syn/ooc/pp_resource_gate.py:566-578 and syn/ooc/pp_resource_baseline.json route-1x1 - every statement of the 135afd04 route's verdict matches #818's frozen rule (fall is a WARNING, no failure; floors at every corner), figures unchanged and consistent with the record.`
- `[R748] PASS RTL - git diff 50e5d08d..81f78a81 and merge-tree 0761e474 - no RTL or gate code is authored in the delta. The merge equals git merge-tree of live dev and the reviewed head, gitlinks equal dev, so the prior RTL verdict at 50e5d08d holds over an unchanged dependency.`
- `[R748] PASS Robustness - same artifacts - no input-handling or gate-path code changed. syn/ooc/* is byte-identical to 50e5d08d, so the prior verdict holds.`
- `[R748] PASS Tests - receipts/resource_baseline.log, receipts/em_dash.log, receipts/gen_toc_*.log - the gate's baseline audit, which reads AREA_BUDGET.md's policy table on the edited page, passes. Doc gates pass. The gate selftests and mutants are unchanged in bytes and keep the prior verdict.`
- `[R748] PASS Docs - receipts/docs_commit.diff, receipts/grep_gate_refuses.txt, receipts/grep_0408.txt and the six doc gates - F1 resolved, no present-tense refusal remains. R1 is RESIDUE (PR body) and S1 is optional.`

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | AREA_BUDGET.md:144-145, SUBMODULES.md:421-429, CHANGELOG.md:73-76, pp_resource_gate.py:566-578, pp_resource_baseline.json | R748-3 | 81f78a81e1271185174f9c5dbbcc8469b5dab5b4 |
| RTL | CLEAN | delta diff, merge-tree identity, gitlinks; gate code unchanged since 50e5d08d | R748-3 (delta); prior verdict at 50e5d08d carries | 81f78a81e1271185174f9c5dbbcc8469b5dab5b4 |
| Robustness | CLEAN | delta diff; syn/ooc/* byte-identical to 50e5d08d | R748-3 (delta); prior verdict at 50e5d08d carries | 81f78a81e1271185174f9c5dbbcc8469b5dab5b4 |
| Tests | CLEAN | check-baseline, doc gates at head; selftest and mutant bytes unchanged | R748-3 | 81f78a81e1271185174f9c5dbbcc8469b5dab5b4 |
| Docs | CLEAN | the three edited pages, grep receipts, six doc gates | R748-3 | 81f78a81e1271185174f9c5dbbcc8469b5dab5b4 |

## Real limits

- No source bank, gate selftest or mutant campaign ran at this head. The delta does not touch them, and those verdicts carry from the reviewed head `50e5d08d` and the composition review of tree `0761e474`.
- The candidate commit `ffe3a631` is not fetchable. Its identity with `17fd6f73` rests on R747-3's published tree id `0761e474`, which this round recomputed independently from `02ca829a` and `50e5d08d`.
- The signed evidence packet at `75d730df/review-evidence/818-r1` was not re-verified this round. It covers an earlier head, and the docs-only delta changes no figure it records.
- No hosted run was inspected. No act, Docker, Vivado or hardware run. Physical calibration NOT RUN, and field skips are not hardware proof.
- After the gate runs the clone matched the exact head: clean status including ignored files, index equal to HEAD, gitlinks as above. The two `__pycache__` directories this round created were removed.

## Pending manager duties

- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link the receipts on the PR.
- Own hosted and act acceptance at the exact head.
- Carry R1, R747-2 RS1, R748-2 R2 and R747-3 OBS-1 to the residue checklist.
- Merge only with explicit maintainer authorization.

R748-3 FINISHED
