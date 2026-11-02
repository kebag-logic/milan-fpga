[R742] POSITIVE - exact head e8ec8d209a3d9055cc034a23d94925a0bf7b9a63

PR #815, issue #797 lane D0, external independent round R742-5. Tree `274a5320231c562168a58416a3a3c316ced60493`. Delta under review: `8d8c2e366a2d..e8ec8d209a3d` (merge `b48b2fd5aa55` of dev `e61a4afaa54a`, then regeneration commit `e8ec8d209a3d`). Previously reviewed head: `8d8c2e36` (R742-4 POSITIVE). Validation base and live dev: `e61a4afaa54a598ceec08b7b5879285256cc60b6`.

No BLOCKER, MAJOR or MINOR finding is open. One RESIDUE (PR body) and one wording RESIDUE carried from round 4 remain for the manager's residue checklist. All five lenses are clean at this head.

## What was checked

### 1. The merge keeps both sides (receipt `receipts/merge_structure.txt`)

- `b48b2fd5` has parents `8d8c2e36` (lane) and `e61a4afa` (dev). `e8ec8d20` has one parent, `b48b2fd5`.
- I recomputed the merge with `git merge-tree --write-tree 8d8c2e36 e61a4afa`. It gives tree `f10e50b9db5f`, which is the same as the recorded merge tree. So the merge contains no hand resolution and no extra edit.
- The combined diff (`git diff-tree --cc`) lists only `docs/README.md`.
  - Against the lane parent, the merge adds dev's row: "Review the Mark II 32x32 datapath".
  - Against dev, the merge keeps the lane's change: "Media-clock following, implemented".
  - Both sides are present.
- `git merge-base --all HEAD e61a4afa` gives one base, `e61a4afa`. Dev is an ancestor of the head.
- The PR's diff against dev touches 10 paths, all on the lane's own list. Since `8d8c2e36` only two of them changed: `docs/DOCUMENTATION_AUDIT.md`, and `docs/README.md` (dev's row).
- No gitlink differs from dev. All six submodule pins equal `e61a4afa`'s.

### 2. Regeneration came only through the generator (receipts `inv_*.txt`, `regen_commit.diff`)

- At the head:
  - `python3 -I scripts/docs_inventory.py --check` gives rc 0 ("540 lines … fresh").
  - `--write` followed by `--check` gives rc 0, with a byte-identical page. The blob is `245e63cfdf06…` both before and after.
  - `--selftest` gives rc 0 (50 controls).
- At the merge commit `b48b2fd5`:
  - `--check` gives rc 1, as expected, because the page is stale after dev moved: "166 → 176 current".
  - `--write` produces blob `245e63cfdf06…`, which is exactly the committed `e8ec8d20` page.
  - So the regeneration commit is the generator's output on the merged tree, with nothing hand-edited.
- The regeneration commit changes `docs/DOCUMENTATION_AUDIT.md` only.
  - `scripts/docs_inventory.json` and `scripts/docs_inventory.py` are unchanged since `8d8c2e36`.
  - `main()` (`scripts/docs_inventory.py:974-991`) shows that `--write` writes only `OUTPUT`.
  - The JSON is the verified-findings data, not a generated file. Leaving it unchanged follows the round's scope ("no new findings, no coverage change").

### 3. The page-count change and every moved finding follow the generator's rules (receipt `receipts/audit_rows_8d8c2e36_to_e8ec8d20.txt`, script `scripts/audit_rows.py`)

I parsed the page at both heads:

- Pages: 212 → 213. The added page is `docs/design/MARK_II_STREAM_ENGINES.md` (current, area lane, design).
- Status: current 166 → 176, stale 25 → 16, obsolete 21 → 21.
  - Nine pages went from stale to current: `REQUIREMENTS.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/design/MAAP_FABRIC.md`, `docs/fpga/DATAPLANE_WALKTHROUGH.md`, `docs/litex/LITEX_SOC.md`, `docs/overview/ARCHITECTURE.md`, `docs/overview/FULL_FPGA_SOLUTION.md`, `docs/overview/SYSTEM_DOMAIN_MAP.md` and `docs/traceability/ieee8021q.md`.
  - `docs/fpga/FPGA_DESIGN.md` and `docs/reference/FR_NFR.md` lost a copy row but stay stale on their other findings.
- Finding rows: 87 → 76. Copy rows: 22 → 11. Distinct finding IDs: 65 → 65. No ID was added or dropped.
- Eleven D0-001 copy rows left. `git grep` at the head finds none of D0-001's six `also` spellings, and neither the D0-033 nor the D0-056 quote, on any Markdown page (`receipts/d0001_rewording_vs_code.txt`).
  - Dev's PR #828 changed the text on those pages, not just the wording. Each page now says all-fabric stays the shipping default.
  - That agrees with the code: `sw/litex/milan_soc.py:2873` reads "--ctrl-mailbox, whose default is off", and `:4116` is `store_true`.
  - So the nine pages that went back to current no longer carry the contradiction D0-001 recorded. Issue acceptance bullet 2 is not weakened by this regeneration.
- D0-001 (`README.md`), D0-033 and D0-056 render "re-verify: quote not found". That is the generator's stated rule (`scripts/docs_inventory.py:25-27`, `:604`): the entry is kept and its page stays stale.
- Probe (`receipts/probe_copy_without_primary.txt`): I planted one D0-001 `also` spelling on `docs/overview/SYSTEM_DOMAIN_MAP.md`.
  - The goal was to rule out the copy rows leaving because a primary quote went missing, rather than because the text left.
  - `--check` went to rc 1 (current 176 → 175), and `--findings-dir` emitted `D0-001: docs/overview/SYSTEM_DOMAIN_MAP.md:43`.
  - So the copy search still runs when the primary quote is absent. I restored the file and `--check` returned rc 0.
- Eight rows moved line by the size of dev's edits: `README.md` D0-002/003/004/005/046/047 by +6 and `FR_NFR.md` D0-019/020 by +5. I spot-checked five of them against the file text (`receipts/moved_lines_spotcheck.txt`).
- The executor's handoff counts (212→213, 166/25/21 → 176/16/21, 87(22) → 76(11), nine pages, eight moved rows) match my own parse exactly.

### 4. Gates that read the JSON, and the docs gates (receipts `pp_srcs_check_selftest.txt`, `docs_*.txt`, `diff_check_vs_dev.txt`)

- `python3 -I scripts/pp_srcs.py --check --selftest` (the rtl-fast step at `.github/workflows/rtl-fast.yml:171-172`, which walks every tracked file including `scripts/docs_inventory.json`): rc 0.
- `scripts/docs_check.py` rc 0: 213 md files, 0 findings.
- `check_doc_style.py` rc 0, `check_solution_docs.py` rc 0, `check_baremetal_only.py --check` rc 0, `check_feature_status.py` rc 0.
- `check_em_dash.py` with the pinned renderer, installed in a disposable venv from `tools/markdown/requirements.txt` with `--require-hashes`: rc 0 against both `--base e61a4afa` and `--base 8d8c2e36`.
- `git diff --check e61a4afa e8ec8d20` rc 0.

### 5. Published author evidence (receipt `receipts/evidence_manifest_verify.txt`)

- I fetched `review-evidence/797d0-r1` at `82a31a67`. All 281 files under `author-r5/` are listed in `MANIFEST.json`, each with a matching `published_sha256`. None is unlisted.
- Of the 114 `.rc` files:
  - only `regen/check-merged-before-write.rc` is non-zero (1), which is the expected pre-write stale check;
  - `probes/stale-page-mutants.rc` reads `rc=0`.
- `gates/docs-yml-table.md` ends "65 steps ran, 31 not run with a reason, 0 bad". The lane logs name `e8ec8d20`.
- The GitHub commit `82a31a67` reports `verification: unsigned`. I verified the packet by its manifest digests, not by a commit signature.

### 6. Comment rule

The delta adds no source comment. Its only non-generated change is dev's `docs/README.md` row. The generated audit page names lanes ("D0", "area lane"), which is allowed on findings pages. No new instance.

## Findings

### R1 - RESIDUE - Docs - PR #815 body, line 16 ("Status") and line 114 ("Known limitations") - the hosted statements are stale again

- **Authority/evidence:** at this review the PR head is `e8ec8d20` and hosted runs exist (`receipts/hosted_checkruns_at_review.tsv`, 2026-11-02T16:16Z):
  - `bdd-conformance`, `changes` and `full-ci-gate`: success;
  - `Physical gPTP (nightly and manual)`: skipped;
  - 35 queued and 5 in progress.

  The body still says "GREEN locally; hosted not yet run" (line 16) and "Hosted result: this head has no hosted run until it is pushed" (line 114) (`receipts/pr_body_hosted_lines.txt`). This is the same defect as round 4's R1, which recurred because the body was rewritten before the push.
- **Impact:** a cold reader is told hosted evidence does not exist. This is prose only. It changes no measurement, code, generated artifact or verdict.
- **Required outcome, exact fix (manager, PR body, using the result current when applied):**
  - Line 16: replace "hosted not yet run" with "hosted at `e8ec8d20`: <per-workflow result from `gh run list --commit e8ec8d20`>".
  - Line 114: replace the sentence with the same result. Name any context still owed a rerun.
- **Verification:** read the body against `gh run list --commit e8ec8d209a3d`.

### R2 - RESIDUE - Docs - `scripts/docs_inventory.py:32`, PR body - "the punctuation ending it" is wider than the code (retained from R741-4 R2)

- **Evidence:** the generator is unchanged since `8d8c2e36`, so the text and the code that strips only `.,;:` are as round 4 found them.
- **Impact:** wording only. No recorded statement ends in `!` or `?`.
- **Exact fix:** as R741-4 R2 states: "the full stop, comma, semicolon or colon ending it". Because the docstring feeds the command-table digest, apply it at the file's next edit.
- **Verification:** read `:32` against the strip set.

### S1 - SUGGESTION - Conformance, Docs - `scripts/docs_inventory.json` entries D0-001, D0-033, D0-056 - retire three findings that dev has fixed

- **Evidence:** the three quotes, and every D0-001 `also` spelling, are absent at the head. The replacing text on each page ("All-fabric stays the shipping default until F2 to F5 acceptance"; `FR_NFR.md` "The all-fabric build stays the shipping default until then") agrees with `sw/litex/milan_soc.py:2873` and `:4116`.
- **Impact:** none on status today. `README.md`, `docs/integration/AXIS_CORES_ON_BAREMETAL_SOC.md` (D0-034 live) and `docs/reference/FR_NFR.md` stay stale on other live findings. The three "re-verify" rows are the generator's intended signal, and keeping them was in scope for a sync-only round.
- **Suggested outcome:** in a later round, or once the maintainer records the "Mark II default" wording (the executor names NFR-SCOUT-02), re-verify and remove the three entries in one change. That follows the docstring's own retirement rule (`scripts/docs_inventory.py:25-27`).

### S2 - SUGGESTION - Docs - `docs/DOCUMENTATION_AUDIT.md` Summary ("Findings cite source lines at dev `1f29f189`") - the line pin predates the merged dev

- **Evidence:** dev's merge inserts 6 lines after `hdl/milan/milan_datapath.sv:87` and 10 or more after `sw/litex/milan_soc.py:1440` (`receipts/cited_source_line_shift_1f29f189_to_e61a4afa.txt`). About 23 findings cite those two files. The page states its pin honestly, so every citation is correct at `1f29f189`.
- **Impact:** a reader at the merged head must check out `1f29f189` to follow a cited line.
- **Suggested outcome:** at the next data refresh, move `cited_at` to the current dev and shift the cited ranges in the same change.

## Prior findings at this head

| Prior finding | State at `e8ec8d20` | Cause / evidence |
|---|---|---|
| R742-4 R1 / R741-4 R1 RESIDUE, PR body hosted status stale | **RETAINED as R1** (recurred) | The body was rewritten for round 5 before the push; lines 16 and 114 |
| R741-4 R2 RESIDUE, "the punctuation ending it" | **RETAINED as R2** | Generator unchanged since `8d8c2e36` |
| R742-4 S1 / R741-4 S3 SUGGESTION, two surviving delta mutants | RETAINED, optional | Generator unchanged |
| R742-4 S2 / R741-4 S2 SUGGESTION, quote that normalises to nothing | RETAINED, optional | Generator unchanged |
| R742-4 S3 / R741-4 S1 SUGGESTION, broad `also` fragments (D0-059 subjectless) | RETAINED, optional | JSON unchanged |
| R742-4 S4 / R741-4 S4 SUGGESTION, generator at 999 of 1,000 lines | RETAINED, optional | Still 999 lines (`wc -l`) |
| R742-4 S5 SUGGESTION, watcher job limit cancels healthy runs | RETAINED, optional | Not in the delta; the hosted runs are still queued at this review |
| R742-3 F1 / R741-3 F1 BLOCKER, literal path fails `pp_srcs.py --check` | Stays RESOLVED | `pp_srcs.py --check --selftest` rc 0 at this head |
| R742-3 F2 MINOR, search misses real copies | Stays RESOLVED | Generator unchanged. My copy-without-primary probe shows the search running |
| R742-3 R1, R741-3 R1-R3 RESIDUE | Stay APPLIED | JSON and docstring unchanged |
| R741-3 S1-S4, R742-3 S1-S2, R741-2 S1-S3, R742-2 S1, R741-1 S1-S3 SUGGESTION | RETAINED, optional | The delta does not touch them |
| R741-2 F1, R742-2 F1-F3, R742-1 F1 and earlier F-series | Stay RESOLVED | The delta changes no data entry or generator line |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts (at the exact head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #797 acceptance bullets 1-2 against `docs/DOCUMENTATION_AUDIT.md` (213 pages, each with a status); round-5 scope in the executor's TAKEN comment; dev's rewording of the D0-001 pages against `sw/litex/milan_soc.py:2873`, `:4116` | R742-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| RTL | CLEAN | `receipts/pr_diff_vs_dev_names.txt`: the PR's diff against dev `e61a4afa` holds no HDL, testbench or synthesis file. Dev's own RTL comes in unchanged (recomputed merge tree equals the recorded one), with no gitlink change. Not applicable beyond that | R742-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| Robustness | CLEAN | Merge reproduction (`git merge-tree`), one merge base. Generator behaviour on vanished quotes (`scripts/docs_inventory.py:604`) and on a copy without its primary (planted probe, restored) | R742-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| Tests | CLEAN | `docs_inventory.py --check` / `--write`+`--check` byte-identical / `--selftest` 50 controls; `pp_srcs.py --check --selftest`; `docs_check.py`, `check_doc_style.py`, `check_solution_docs.py`, `check_baremetal_only.py --check`, `check_feature_status.py`, `check_em_dash.py` (two bases); `git diff --check`; author-r5 receipts 281/281 digests | R742-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |
| Docs | CLEAN (RESIDUE R1, R2 carried; S1, S2 optional) | `docs/README.md` merge (both sides); `docs/DOCUMENTATION_AUDIT.md` row-by-row diff against `8d8c2e36`; Summary pin line; PR #815 body lines 16, 34, 43-60, 114 | R742-5 | `e8ec8d209a3d9055cc034a23d94925a0bf7b9a63` |

## Limits

- **Hosted runs:** at this review the exact head is pushed, but `docs`, `rtl-fast`, `elaborate` and `rtl-full` are queued. Only `bdd-conformance`, `changes` and `full-ci-gate` had completed (success), and `Physical gPTP (nightly and manual)` was skipped. I make no claim about any hosted context beyond that snapshot.
- **No manager source bank** runs at this head, and I infer none. Source-head execution evidence is the author's published receipts plus my own focused gate runs listed above. I ran no full parent, PP, gPTP, Yosys or builder bank, no act and no Docker.
- **Scope of re-verification:** I did not re-verify statement by statement the pages dev added or changed, including `docs/design/MARK_II_STREAM_ENGINES.md`. That matches D0's stated scope ("Other pages wait for their area lane"), and the PR body discloses it.
- **Physical calibration:** NOT RUN. Field skips are not hardware proof.
- **Packet authentication:** the evidence commit `82a31a67` is unsigned on GitHub. I verified integrity by the manifest's sha256 digests only.

## Pending manager duties

- Read the exact-head hosted `docs`, `rtl-fast`, `elaborate` and `rtl-full` results, including `verilator-suites` and `yosys-portability`, when they finish. Own hosted and act acceptance.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts on the PR.
- Apply RESIDUE R1 to the PR body with the hosted result current at that time. Carry R2 to the residue checklist.
- Obtain explicit maintainer authorization before any merge.

## Restoration

After the probes, the clone is back at HEAD `e8ec8d20`:

- the index tree is `274a5320231c562168a58416a3a3c316ced60493`;
- `git status --porcelain` is empty;
- `git diff` and `git diff --cached` are clean for bytes and modes;
- all six gitlinks are unchanged (`receipts/clone_restore_verify.txt`).

R742-5 FINISHED
