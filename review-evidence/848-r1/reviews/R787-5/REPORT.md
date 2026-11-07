[R787] POSITIVE - exact head 697e17a48e00073c9cd40f40049cd1f0f8ddb033

Round R787-5, issue #848, PR #849. Tree `f5f5df0d309d49a95c38db36df53f79ee63ae3d1`. Delta review against `9d5a5af7`.

## Verdict

R787-4-F1 is fixed at its cause. D0 now comes from `verified_pages` in the data file, no path rule assigns it, and the audit changes in exactly the 2 lines claimed. All eight focus checks pass. I found no open BLOCKER, MAJOR or MINOR.

`gate_25_0` and the tool-inventory self-test are open, not findings. The act at this head covers them, and it has not run yet.

| ID | Severity | Lenses | Title |
|---|---|---|---|
| R787-5-S1 | SUGGESTION | Tests | The D0-before-archive mutant can be killed at no line cost |
| R787-5-S2 | SUGGESTION | Tests | The new control samples one directory, and the archive lane figure is not graded |
| R787-5-S3 | SUGGESTION | Tests, Robustness | The refusal does not name the entry, and its advice is not graded |
| R787-5-R1 | RESIDUE | Docs | Two new docstrings name the D0 lane |
| R787-5-R2 | RESIDUE | Docs | The docstring still says a removed document makes the page stale |
| R787-5-R3 | RESIDUE | Docs | The PR body says covering F10 needs a line the module lacks |

## Focus checks

**1. D0 is the list, and no path rule assigns it: PASS.** `scripts/docs_inventory.py:491` tests `path in checked`, and `RELEASE_FACING` is gone (`receipts/repo_facts.txt`). The audit has 214 rows: 30 `D0`, 162 `area lane`, 22 `archive`. The 30 `D0` rows equal the list.

**2. The list's population: PASS. `REQUIREMENTS.md` stays.** All 30 exist at `1e80128f`. They are exactly the old rule's Markdown matches there, and the rule's only other match is a JSON file outside the population (`receipts/d0_population.txt`).

My judgement on `REQUIREMENTS.md`:

- D0's plan on #797 names it as release-facing, and the D0 executor's public scope repeats it.
- The ruling's figure needs it: 10 reference + 7 integration + `REQUIREMENTS.md` = 18.
- This is not the R787-4-F1 defect. That page did not exist at the baseline. This one did, and it was partly checked.
- The page says statements "were checked", not that every statement was. The same limit is already public for 823 read-only statements on four other pages.
- The thinner coverage is disclosed in the PR body and REVIEW READY. The manager can still narrow the list: removing one entry gives 17.

**3. `docs/reference/STRICTER_READINGS.md`: PASS.** Its row (`docs/DOCUMENTATION_AUDIT.md:314`) reads `area lane`. The reference figure (`:43`) is 18.

**4. `--check` without Git history: PASS.** It gives rc 0 on all three of these (`receipts/tree_probes.txt`):

- an export with no `.git`;
- the same export with no `git` binary on `PATH`;
- a one-commit clone where `1e80128f` is absent.

The hosted `docs-check-no-git` job also finished SUCCESS at this head.

**5. The new arm fails with the old rule restored: PASS.** M01 gives `--selftest` rc 1, and the failing arm is `a page added under a release-facing path is not D0` (`receipts/mutants.txt`).

**6. The rc 2 refusal: PASS, with S3.** It is right for three reasons:

- It matches how a finding or judgement on an untracked page is already treated (`:334`, `:342`).
- It stops a stale entry passing D0 to a later page at that path.
- `--write` refuses too, and leaves the audit untouched.

It says what to do. Following it works (`receipts/tree_probes.txt`):

| Case | Result |
|---|---|
| Rename, list updated | rc 0, 30 D0 rows, figure 18 |
| Removal, list updated | rc 1 until `--write`, then rc 0, 29 D0 rows, figure 17 |
| Deleted on disk only | rc 2 |

No open PR renames or deletes a listed page, and all 30 exist at live dev and at `dev-soft-core`.

**7. Digest: PASS.** `sha256sum scripts/docs_inventory.py` gives `a9604e8e...ca2b9`, which equals the table entry. The table diff is that one line.

**8. Audit diff against `9d5a5af7`: PASS.** The numstat is 2 added and 2 removed, and those are the two lines in check 3. `--write` reproduces the committed page byte for byte.

**The surviving mutant (D0 tested before archive): acceptable, S1.** It is equivalent on the data the repository carries, because no archive page is listed. D0's scope excludes the archive, so listing one would be a data error. At this head such an entry renders `archive` and changes nothing.

**Sync merge `a578ceb5`: PASS through R787-4's receipts.** All 20 R787-4 manifest entries match their published hashes. `01_merge_tree` and `02_tree_compare` show the audit as the only conflicted and only differing path. Directly, the merge's parents are `171fd56b` and `8ab3a930`, and only the audit differs between it and `9d5a5af7`.

**#848 acceptance on this head: holds** (`receipts/acceptance_probes.txt`). A line added to every tracked Markdown page, or to a listed page, gives rc 0. An unlisted page removed, retitled or given a banner gives rc 1. A page added gives rc 1 (`receipts/tree_probes.txt`). The docs-gates clause waits on `gate_25_0`.

## Mutants

19 cases on disposable exports, including the identity run (`receipts/mutants.txt`).

| Case | `--selftest` | `--check` | Answer |
|---|---:|---:|---|
| M00 identity | 0 | 0 | Clean |
| M01 old rule; M02 list or old rule; M03 guides prefix | 1 | 1, 1, 0 | Killed by the new arm |
| M06 no D0; M08 archive cell lost; M15 figure counts every page; M16 wrong key | 1 | 1 | Killed |
| M09, M10 guard clauses dropped | 1 | 0 | Killed |
| M11 string check dropped | 1 | 0 | Killed by traceback, as the author disclosed |
| M04 integration prefix inherits D0 | 0 | 0 | Survives, S2 |
| M05 reference prefix inherits D0 | 0 | 1 | Survives the selftest, S2 |
| M14 figure counts archive cells | 0 | 1 | Survives the selftest, S2 |
| M07 D0 before archive | 0 | 0 | Survives, S1 |
| M13 refusal loses its advice | 0 | 0 | Survives, S3 |
| M12 guard reads the disk, not the population | 0 | 0 | Differs only for a listed page that is on disk but outside the population. Not a finding. |
| M17 missing key refused | 0 | 0 | A stricter variant, not a defect. On the real tree a missing key gives rc 1, and `--write` then claims no D0 at all. |
| M18 no data file means all D0 | 0 | 0 | Needs the tracked data file to be absent. Not probed further. |

## Findings

### R787-5-S1 - SUGGESTION - Tests

**Where:** `scripts/docs_inventory.py:945`.

**Evidence:** Changing that arm's mutation to `edit_data(lambda d: d["verified_pages"].append("docs/history/v1/OLD.md"))`, with the arm renamed `archive is obsolete`, keeps 60 controls, 1000 lines and 120 columns, and kills M07 (`receipts/trial_kills.txt`).

**Impact:** None on current data.

**Required outcome:** Optional.

**Verification:** `--selftest` rc 0, and rc 1 with M07.

### R787-5-S2 - SUGGESTION - Tests

**Where:** `scripts/docs_inventory.py:924`, `:534`.

**Evidence:** The arm plants one page under `docs/guides`. A partial prefix rule for `docs/integration` (M04) passes both `--selftest` and `--check`. One for `docs/reference` (M05) is caught only by the real tree's `STRICTER_READINGS.md` row. M14 survives the selftest because no needle grades the archive lane's figure.

**Impact:** Low. The product has no path logic left, and the real-tree probes show all three directories render `area lane`. It would take a new, partial rule to reach this.

**Required outcome:** Optional: plant a page in each directory, or grade the archive lane row.

**Verification:** M04, M05 and M14 fail `--selftest`.

### R787-5-S3 - SUGGESTION - Tests, Robustness

**Where:** `scripts/docs_inventory.py:331`, `:960`.

**Evidence:** The refusal does not name the missing entry, though the judged and findings refusals name theirs. It also does not say that a rename keeps the entry while a removal drops it. The arm grades only `verified_pages`, so M13 survives. Changing the arm's needle to `update it when` kills M13 at no line cost (`receipts/trial_kills.txt`).

**Impact:** A small cost to the person fixing the data.

**Required outcome:** Optional.

**Verification:** The refusal names the entry, and M13 fails `--selftest`.

### R787-5-R1 - RESIDUE - Docs

**Where:** `scripts/docs_inventory.py:28`, `:320`.

D0 is a lane name on #797, and the owner's comment rule bars lane names from source comments. The rendered `D0` value and the selftest labels are strings, not comments, so they stay.

**Exact fix:** At `:28`, "It lists the pages #797 checked: a later page waits for its lane (#848)." At `:320`, "The two baselines, the verified pages, the recorded judgements and findings; refuses a malformed file." Both fit in 120 columns, and a re-pin follows.

### R787-5-R2 - RESIDUE - Docs

**Where:** `scripts/docs_inventory.py:37-40`.

"A document added or removed ... makes the page stale" no longer holds for the 30 listed pages, which give rc 2. The gate still fails, so this is wording only.

**Exact fix:** Append to `:40`: "A page in `verified_pages` that leaves is refused instead (exit 2)." This fits on the line, and a re-pin follows.

### R787-5-R3 - RESIDUE - Docs

**Where:** PR #849 body, "Review round 4", after the mutant table.

"Covering it would need one more fixture line, and the module has none to spare." S1 shows it needs no extra line.

**Exact fix:** Replace that sentence with "It is left uncovered because no data lists an archive page."

## Prior findings

The other reviewer's delta at `9d5a5af7` was withdrawn by the ruling, so it has no findings to carry.

| Finding | State at this head |
|---|---|
| R787-4-F1 | RESOLVED. The row, the figure, the class fix and the control are in checks 1 to 5. The module stays at 1000 lines with no code moved. |
| R787-4-R1 | RESOLVED. PR body line 17 gives 547 lines and the #842 row, and the Evidence section names this head. |
| R787-4-R2 | RETAINED RESIDUE. Ruled to need no branch change. `author-r4/manager-sync-gates.txt:3` still reads `parents` under the head, and no later sync receipt exists to correct it. |
| R787-4-S1 | RETAINED SUGGESTION. Ruled out of #849. |
| R787-1-F1 to F5, R787-2-F1, F2, R788-1 and R788-2 findings | RESOLVED. No delta touches their code. The selftest passes 60 controls. |
| R787-1-S1 chain, R787-2-S2 to S4 chains, R788-2 S2, R787-3-S1 to S4, R788-3 S1, S2 | RETAINED SUGGESTION. The delta does not change them. |
| R787-3-R1, R788-3 R1 | RETAINED RESIDUE. PR body line 42. |
| R787-3-R2 | RETAINED RESIDUE. `W8` still names two mutants, at PR body lines 80 and 111. |

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | [A10] ruling against `scripts/docs_inventory.py:329-331`, `:491`; `scripts/docs_inventory.json:4-35`; #797 plan against `receipts/d0_population.txt`; #848 acceptance in `receipts/acceptance_probes.txt`, `receipts/tree_probes.txt` | R787-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| RTL | CLEAN | `receipts/restore.txt`: 0 delta files under `hdl`, `syn` or the submodule roots, 0 gitlink changes, so nothing in this lens's scope moved | R787-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| Robustness | CLEAN | `receipts/tree_probes.txt`: rename, removal, disk-only delete, replaced page, duplicate, archive entry, missing key, non-document entry, no Git, no history | R787-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| Tests | CLEAN | `scripts/docs_inventory.py:924`, `:945-946`, `:960-962`; `receipts/mutants.txt`; `receipts/trial_kills.txt`; `--selftest` 60 controls | R787-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| Docs | CLEAN | `docs/DOCUMENTATION_AUDIT.md:23-24`, `:38-45`, `:314`; docstring `:28`, `:37-40`, `:320`; PR body; `check_doc_style.py` rc 0 | R787-5 | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |

## Real limits

- This is a delta review. #842's content was not reviewed, and `a578ceb5` was judged through R787-4's receipts.
- The evidence commit `ed673689` is reported as unsigned, and the packet carries no signature I could verify. I checked hash consistency only: 181 `author-r5` and 20 R787-4 entries match `MANIFEST.json`.
- Two PR body statements rest on lane files that are not public: the 29-page per-page ledger, and the "sections 3, 4, 7 and 8" reading of `REQUIREMENTS.md`. I could not verify either. The scope and the ruling's arithmetic carry my judgement without them.
- D0 is a page-level claim. A listed page replaced in place keeps `D0` (probed), and a new entry added to the list renders `D0` with nothing to refuse it (probed). No gate can tell without history, so both rest on review of the data file.
- I did not run `docs.yml`. The author's table is hash-consistent and shows 71 rc 0, `gate_25_0` not run and 24 not run with a stated reason, so the verifier gives rc 1. I ran `--check`, `--selftest`, `check_py_idiom.py`, `check_doc_style.py` and `git diff --check`, all rc 0.
- `check_em_dash.py` was not run. Direct search finds no em dash in the added lines.
- The reviewers' earlier mutant campaigns were not rerun. The 19 cases above target this delta.
- Hosted at the time of writing: 4 contexts SUCCESS (`bdd-conformance`, `changes`, `docs-check-no-git`, `wire-accountability`), 13 in progress, 7 queued. `docs-gates-0`, `-1` and `-2` have not finished, so most hosted evidence does not exist yet (`receipts/hosted_state.txt`).
- Physical calibration NOT RUN. Field skips are not hardware proof. This round ran no manager source bank and infers none.

## Pending manager duties

- Run act at this head, which covers `gate_25_0` and the tool-inventory self-test. Both are open, not findings.
- Accept the hosted results once they finish.
- Accept or narrow `REQUIREMENTS.md` (author's open risk 3). My judgement is to keep it.
- Build and validate the current-dev merge candidate at the merge turn and link its receipts. Land #842 first, as ruled, and confirm the page regenerates.
- Obtain the other reviewer's verdict at this head.
- Carry R787-5-R1 to R3, R787-4-R2 and the retained RESIDUE to the checklist. R1 and R2 need a re-pin if applied.

## Restoration

Every probe ran on a disposable copy. One local gate run left an ignored `scripts/__pycache__` in this clone, and I removed it. Index, worktree and tree equal the head, `git status --ignored` is empty, and all six gitlinks match `9d5a5af7` (`receipts/restore.txt`).

R787-5 FINISHED
