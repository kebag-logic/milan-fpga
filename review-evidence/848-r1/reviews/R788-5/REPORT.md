[R788] POSITIVE - exact head 697e17a48e00073c9cd40f40049cd1f0f8ddb033

Round R788-5, issue #848, PR #849. Tree `f5f5df0d309d49a95c38db36df53f79ee63ae3d1`. Delta review against `9d5a5af7`.

## Verdict

R787-4-F1 is fixed at its cause, and the [A10] ruling is met item by item. No BLOCKER, MAJOR or MINOR is open, so all five lenses are clean at this head.

**This verdict does not prove the docs gates.** `gate_25_0` and the tool-inventory self-test are covered by the act at this head, which has not run. #848's third acceptance clause stays open until then. This is an open item, not a finding.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| S1 | SUGGESTION | Tests, Robustness | F10 survives, though one existing arm can kill it with no added line |
| S2 | SUGGESTION | Robustness | The refusal does not name the page |
| S3 | SUGGESTION | Robustness | An absent `verified_pages` key empties D0 without a refusal |
| S4 | SUGGESTION | Conformance, Docs | "Statements on D0 pages were checked" reads wider than D0's own ledger, unchanged from dev |
| R1 | RESIDUE | Docs | The PR body says covering F10 needs one more line |
| R2 | RESIDUE | Docs | Two new docstrings name the D0 lane |

## Focus checks

Receipts: `receipts/probes.txt` and `receipts/population.txt`, unless named otherwise.

1. **D0 is the list, and no path rule assigns it: PASS.** `RELEASE_FACING` is gone. `scripts/docs_inventory.py:491` is the only line that assigns `D0`, and it tests membership of `verified_pages`. The audit has 30 D0 rows, equal to the list.
2. **The list holds only pages that existed and were in scope: PASS.** All 30 exist at `1e80128f`. They are exactly the Markdown files the old rule matched there, with none missing and none extra. They also match the scope [A10] set on #797 (issuecomment-6518880512). The list is sorted and has no duplicates.
   - **`REQUIREMENTS.md`: keep it.**
     - D0's published scope names it, both in that plan and in the executor's TAKEN comment.
     - The ruling's figure of 18 counts it: 7 integration pages, 10 reference pages and this page.
     - R787-4-F1 was about a page that did not exist at the baseline, and this page did.
     - The other 29 pages carry a statement-level limit too: D0's public ledger records 823 statements as read only, on four of them.
     - So thinner coverage is a difference of degree, and the author disclosed it. S4 covers the wider sentence.
3. **`STRICTER_READINGS.md` and the figure: PASS.** `docs/DOCUMENTATION_AUDIT.md:314` renders `area lane`, and `:43` gives 18.
4. **`--check` without history: PASS.** It gives rc 0 on an export with no `.git`, and on a one-commit clone where `1e80128f` is absent (rc 128 on the object lookup).
5. **The new arm fails with the old rule: PASS.** With the path rule restored, `--selftest` exits 1 on `a page added under a release-facing path is not D0`, and `--check` on the real tree exits 1. A stronger variant, list OR path rule, is killed by the same arm.
6. **The rc 2 refusal: PASS, and it says what to do.**
   - It fires for a rename, a removal, a removal with no Git, and a page untracked but still on disk.
   - It fires on `--write` too, so a stale entry cannot be regenerated past.
   - Editing the entry alone heals the tree: rc 0.
   - Removing the entry gives 29 D0 rows and rc 0.
   - An unlisted page still gives rc 1.
   - rc 2 is the right class: `judged` and `findings` already refuse an untracked page the same way (`:335`, `:343`), and a stale entry would hand D0 to a later page at that path. S2 is the one gap.
7. **The digest: PASS.** `ci/image/command-table.json` and the module both give `a9604e8e...ca2b9` (`receipts/delta-facts.txt`). It is the only line changed in the table.
8. **The audit diff: PASS.** `git diff --numstat` gives 2 added and 2 removed, the two lines claimed.

**The surviving mutant, F10: SUGGESTION, not MINOR.** It changes behaviour only if someone adds an archive page to the list. The real list has none, and an archive page was never in D0's scope, so no shipped output is wrong. The author's reason for leaving it is not correct, though: see S1.

**Sync merge `a578ceb5`, through R787-4's receipts only: stands.** Three receipts hash-match the manifest. `02_tree_compare.txt` shows the merge differs from the automerge only in the audit page. This delta touches four paths and no gitlink (`receipts/delta-facts.txt`), so nothing that verdict depends on moved.

**Acceptance, spot-checked at this head.** One line appended to every tracked page gives `--check` rc 0. An added page gives rc 1. A status change was not re-probed here: the delta does not touch that path, and `--selftest` covers it.

## Findings

### S1 - SUGGESTION - Tests, Robustness - `scripts/docs_inventory.py:945`, `:491`

- **Evidence:** `D0 before archive` gives `--selftest` rc 0. Replacing the arm's opening with `("a listed archive page", edit_data(lambda d: d["verified_pages"].append("docs/history/v1/OLD.md")), 0,` keeps the module at 1000 lines and the longest line at 120. It passes at this head and kills the mutant (`receipts/f10_fit.txt`).
- **Impact:** None on today's data. A wrongly listed archive page would be rendered `archive` at this head, but no control pins that order.
- **Required outcome:** Optional. Take the arm with any later change to the module, which also re-pins the digest.
- **Verification:** the mutant gives rc 1. `probe_f10_fit.py` reproduces this.

### S2 - SUGGESTION - Robustness - `scripts/docs_inventory.py:331`

- **Evidence:** The message names no page. The neighbouring refusals at `:335` and `:343` do.
- **Impact:** Small. The person renaming a page usually knows it, but a merge that drops one of 30 entries leaves a search.
- **Required outcome:** Optional. Name the first missing entry, if it fits the 1000 lines.

### S3 - SUGGESTION - Robustness - `scripts/docs_inventory.py:329`

- **Evidence:** With the key absent, `--check` gives rc 1, but `--write` gives rc 0 and 0 D0 rows.
- **Impact:** It fails towards under-claiming, `--check` goes red first and the diff would show about 30 rows, so it is low risk. `verified_at` defaults the same way. No arm pins this case.
- **Required outcome:** Optional. Refuse an absent key when the data file exists.

### S4 - SUGGESTION - Conformance, Docs - `docs/DOCUMENTATION_AUDIT.md:23`

- **Evidence:** The page says "Statements on D0 pages were checked". D0's public ledger (#797 issuecomment-6522752898) records 823 of 4,000 sampled statements as read only. The author also reports that `REQUIREMENTS.md` had only mechanical checks and four sections read. The sentence is the same on live dev `3f6bef88` (`receipts/delta-facts.txt`).
- **Impact:** A reader may take the D0 cell as full statement coverage. This PR did not introduce the sentence, and the ruling's test is per page.
- **Required outcome:** Optional, and outside #848. If the manager wants it, a separate Issue could narrow the sentence, for example to "D0 sampled the statements on these pages". That change would alter a generated page, so it is not RESIDUE.

### R1 - RESIDUE - Docs - PR #849 body, line 70, and issuecomment-6699881504

**Exact fix:** Replace "Covering it would need one more fixture line, and the module has none to spare." with "It is left uncovered; one existing arm could cover it with no added line."

### R2 - RESIDUE - Docs - `scripts/docs_inventory.py:28`, `:320`

`D0` is also the page's rendered value, so this is the narrow case of the comment rule, but it is a lane name in new comment text.

**Exact fix:** At both lines, change "the D0 pages" to "the checked pages". Line 28 stays within 120 columns. This changes the digest, so make it only with a later module change.

## Prior findings

| Finding | State at this head |
|---|---|
| R787-4-F1 | RESOLVED at its cause: focus checks 1 to 5. |
| R787-4-R1 | RESOLVED. PR body line 17 reads 547 lines and names the row, and the Evidence section names this head. |
| R787-4-R2 | CLOSED by the ruling, with no branch change. The published `author-r4` receipt keeps its text. The `author-r5` receipts I fetched carry no parents line. |
| R787-4-S1 | RETAINED SUGGESTION. Out of #849 by the ruling. |
| R787-1-F1 to F5, R787-2-F1, F2, R788-1 F1, F4, R788-2 F1, F2 | RESOLVED. The delta touches `load_data`, `build`, the fixture's data and five arms, none of the code these rest on, and `--selftest` passes 60 controls. |
| R788-2 R1, R2 | RESOLVED as R787-4 recorded. This delta does not touch them, and I did not re-read them here. |
| R787-1-S1 = R787-2-S1 = R788-2 S5 = R788-3 S7 | RETAINED SUGGESTION. |
| R787-2-S2 = R788-2 S1 = R788-3 S3 | RETAINED SUGGESTION. |
| R788-2 S2 = R788-3 S4 | RETAINED SUGGESTION. |
| R787-2-S3 remainder = R788-3 S5 | RETAINED SUGGESTION. |
| R787-2-S4 = R788-2 S4 = R788-3 S6 | RETAINED SUGGESTION. |
| R787-3-S1 to S4, R788-3 S1, S2 | RETAINED SUGGESTION. The code they name is unchanged. |
| R787-3-R1 = R788-3 R1 | RETAINED RESIDUE. PR body line 42 still reads wider than the control. |
| R787-3-R2 | RETAINED RESIDUE. `W8` still names two mutants, at PR body lines 80 and 111. |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | [A10] ruling; #848 acceptance; #797 D0 scope; `scripts/docs_inventory.json` against the `1e80128f` tree (`receipts/population.txt`); `docs/DOCUMENTATION_AUDIT.md:23,43,314` | R788-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| RTL | CLEAN | `receipts/delta-facts.txt`: 0 delta paths under `hdl`, `syn`, `tb` or `sw`, and 0 gitlink changes, so the lens has nothing to apply to | R788-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| Robustness | CLEAN | `scripts/docs_inventory.py:329-331,491`; rename, removal, untracked, no-Git, one-commit and data-shape probes (`receipts/probes.txt`) | R788-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| Tests | CLEAN | New and changed arms at `:924`, `:945`, the three `verified_pages` refusal arms; 10 own mutants with 1 survivor: 8 of the code, the old rule, and list OR path rule (`receipts/probes.txt`, `receipts/f10_fit.txt`); `--selftest` 60 controls | R788-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| Docs | CLEAN | Module docstring `:28`, exit-status text; audit summary; PR body; `check_doc_style.py`, `docs_check.py` and `check_py_idiom.py`, each rc 0 (`receipts/gates.txt`) | R788-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |

## Real limits

- **Not run here:** `gate_25_0`, the tool-inventory self-test, `check_em_dash.py` and the full `docs.yml` set. The author's verifier exits 1 on `gate_25_0`, as disclosed.
- **Not publicly traceable:** the claims that `REQUIREMENTS.md` had sections 3, 4, 7 and 8 read, and that 29 pages match D0's per-page table, rest on lane files that are not public. I did not read those files and could not confirm the claims from public comments. The list itself does not depend on them: the published scope and the baseline tree reconstruct it.
- **Hosted, at 2026-11-07T01:02Z (`receipts/hosted-snapshot.txt`):** 4 completed with success, including `docs-check-no-git`; 13 in progress, including the three `docs-gates` legs; 7 queued. No job had failed. The manager owns acceptance.
- **Author evidence:** six `author-r5` files hash-match the manifest (`receipts/published-evidence.txt`). The other receipts were not checked file by file.
- **`check_py_idiom.py`** refuses a clone with no submodules, so it ran in the review clone, read-only (rc 0).
- **Order of work:** my verdict and ledger were fixed before I opened any prior review (`receipts/preliminary-verdict.md`). Reading them changed neither. S4 was added afterwards, while drafting. I did not read R787-5.
- No manager source bank ran at this head, and none is inferred. Physical calibration was NOT RUN, and no hardware claim is made.

## Pending manager duties

- Run the act at this head, which covers `gate_25_0` and the tool-inventory self-test.
- Accept hosted results when they finish.
- Build and validate the current-dev merge candidate at the merge turn, and link its receipts on the PR.
- Carry R1, R2, R787-3-R1 and R787-3-R2 to the residue checklist.
- Confirm the `REQUIREMENTS.md` reading. It stays listed unless the manager reads "checked" more strictly, which would make the figure 17.

## Restoration

All probes ran on disposable copies. One gate run left a bytecode directory in the review clone, and I removed it. The head, tree, index and worktree match, there are no ignored leftovers, and the required gitlinks are unchanged (`receipts/restore.txt`).

R788-5 FINISHED
