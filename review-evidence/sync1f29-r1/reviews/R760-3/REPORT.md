[R760] POSITIVE - exact head b2a1d67745229d167a5e70d7e1c5064975f027fd

Round R760-3, issue #665, PR #830. Tree `02313ded7626619109696af06a2e1f1a1371a8e4`. Delta from round 2: `fa019799..b2a1d677`, one commit, three lines of `tb/verilator/ctrl_service_budget/README.md`, plus one line of the PR body.

All four focus items hold. No BLOCKER, MAJOR or MINOR is open. Two RESIDUE items remain, both in the PR body: the answer to R760-2-R2 landed in the wrong place in the Status sentence, and the body does not name the new head. No harness ran, as the scope says.

## Focus items

| Item | Result | Evidence |
|---|---|---|
| Line 854 reads 884.91 (R759-2 F3) | Holds. The window is 88,491,464 bus cycles, 884.91464 ms | `receipts/recompute-windows.txt`, `receipts/lines-check.txt` |
| Line 843 (R759-2 RES-3, R760-2-R1) | Holds; see below | `receipts/recompute-grader.txt`, `receipts/delta-and-ancestry.txt` |
| Line 846 (R759-2 RES-4) | Holds. The sentence has a verb and equals RES-4's exact fix byte for byte. `population`, `composed_passes` and `unreleased` are all defined in `grade.py` (lines 611, 747, 685) | `receipts/lines-check.txt` |
| PR body Status (R760-2-R2) | The substance holds: Status now states the rc 1 exception, as the arms' results require. The insertion leaves a broken sentence, R760-3-R1 | `receipts/pr-body.txt` |
| Nothing else changed | Holds. One commit, parent `fa019799`, one blob changed, mode unchanged, 3 insertions and 3 deletions. The body changes one line against `author-r2`, and the live body equals `author-r3/PR-BODY.md` apart from a trailing newline | `receipts/delta-and-ancestry.txt`, `receipts/pr-body.txt` |

**Line 843, clause by clause, read from the published raw logs through the head's own `grade.py`:**

- At `5b5f4336` the ring holds 4 records when `backlog-adp` and `backlog-adp-refill` open, and both commit 13 GM events.
- The same two windows are refused there: `reviews/R760-2/receipts/refusals-base.txt` has two refusals, each with GM 13 against 15.
- "Before dev's #814 was merged" is true. The #826 merge `8adf5c99` is not an ancestor of `5b5f4336` and is an ancestor of the head, and `stage_spi_phy` is absent from `sw/litex/milan_soc.py` at the base.
- "The stage adds the fifth record" is true of the count: 5 at the head, 4 at the no-stage control and at the base. R760-3-S2 notes a more exact form.
- "The firmware, not the stage, causes the refusal" holds at the level the evidence reaches: the refusal exists at the base and at the no-stage control, so the stage cannot be its cause.

**The whole table.** `receipts/readme-table-check.txt` compares all 48 cells of the eight table rows with the raw logs and finds 0 mismatches. The same check run on the `fa019799` README reports exactly one mismatch, the old `884.92`, and exits 1, so it can catch this defect.

**The doc gates the handoff claims.** Reproduced at the head: `check_doc_style.py` OK, `docs_check.py` 0 findings, `check_doc_paths.py` OK, `check_em_dash.py --base 97aab1d0` 0 findings, and `git diff --check` from the merge base to the head rc 0. The first `check_em_dash.py` run exited 2 because the pinned renderer was not installed. The rc 0 run used that renderer from a disposable directory. See `receipts/doc-gates.txt`.

**Sweep.** `884.92` and "makes the ring that full" appear in no tracked file at the head, and `884.92` is not in the live body.

## Findings

No BLOCKER, MAJOR or MINOR.

### R760-3-R1 - RESIDUE - Docs
- **Where:** live PR body, Status, line 17.
- **Evidence:** it reads "exits 0 on the head, but for the budget harness arms that report refused probes, rc 1 as the table below states `fa019799` (the second table under [How to validate](#how-to-validate))". The clause R760-2-R2 asked for went in between "the head" and the SHA, so the SHA now follows "states". "The head" also no longer means `fa019799`, which is where that table's gates ran.
- **Impact:** wording only. The results table is correct, and the rc 1 exception is stated.
- **Exact fix:** "GREEN locally: every gate in the second table under [How to validate](#how-to-validate) exits 0 on `fa019799`, but for the budget harness arms that report refused probes, rc 1 as that table states. The head, `b2a1d677`, changes three lines of one README, and the documentation gates exit 0 on it. `sync-dev-1f29f189-into-dev-soft-core` -> `dev-soft-core`. Base: `dev-soft-core` `5b5f4336`."
- **Verification:** read Status against the second results table and `receipts/doc-gates.txt`.

### R760-3-R2 - RESIDUE - Docs
- **Where:** live PR body, lines 81, 99 and the results heading above line 118, plus the Contents and Round 2 sections.
- **Evidence:** `b2a1d677` appears nowhere in the body (`receipts/pr-body.txt`). "How to get into the same state" detaches at `fa01979959`, the validation list's `git diff --check` ends there, "Results on this round's head" heads a table of `fa019799` results, and no section records round 3.
- **Impact:** wording only. A reader following the commands gets the tree before these three README lines. No code, measurement or verdict differs, and the table's column names its commit correctly.
- **Exact fix:** in lines 81 and 99, use `b2a1d67745229d167a5e70d7e1c5064975f027fd`. Change the heading to "Results on `fa019799`, which differs from the head `b2a1d677` only in three README lines:". Add to Contents and the body: "## Round 3. `b2a1d677` answers `[R759]` F3, RES-3 and RES-4 and `[R760]` R1 in `ctrl_service_budget/README.md`: one window cell and two sentences. No harness ran; the documentation gates exit 0 on the head."
- **Verification:** `git diff --check` from the merge base to the head is already rc 0 (`receipts/lines-check.txt`). Read the rest.

### R760-3-S1 - SUGGESTION - Docs
- **Where:** `tb/verilator/ctrl_service_budget/README.md:843`.
- **Evidence:** this line has two sentences, and it is the only such line in the README's lines 800 to 880. `check_doc_style.py` passes it, and I found no rule that requires one sentence per line.
- **Outcome:** move "The stage adds the fifth record." to its own line.

### R760-3-S2 - SUGGESTION - Docs
- **Where:** `tb/verilator/ctrl_service_budget/README.md:843`, last sentence.
- **Evidence:** both adp windows post 295 records before opening at every setting. The firmware has released 290 of them staged and 291 without the stage (`receipts/recompute-grader.txt`). The count is right, but the stage posts nothing extra: it leaves one more record unreleased.
- **Outcome:** "With the stage, the firmware has released one record fewer of the same 295, so a fifth is still held."

## Prior findings at this head

| Finding | State |
|---|---|
| R759-2 F3 (MINOR) | Resolved at its cause: the cell comes from the exact 884.91464, and the negative control proves the check catches the old value |
| R759-2 RES-3 | Resolved; line 843 equals its exact fix byte for byte |
| R759-2 RES-4 | Resolved; line 846 equals its exact fix byte for byte |
| R760-2-R1 | Resolved. The manager took RES-3's text rather than mine. Mine asked for the stage's added record and lost GM event; line 843 gives the record and line 842 gives 12 against 13 GM events |
| R760-2-R2 | Resolved in substance; the placement is carried as R760-3-R1 |
| R759-2 S4, R760-2-S1 | Retained, unchanged: file an Issue for the grader's "not run" wording. No effect on coverage |
| R760-2-S2 | Retained, unchanged. This round's packet needs no scripts, since it makes no measured claim beyond R759-2's published receipts |
| R759-1 S1 to S3, R760-1-S1 to S4 | Retained, unchanged, with no effect on coverage |

The comment rule has no instance to judge: the delta contains no source comment, and its three lines name no lane, round, reviewer or comment ID.

## Lens results

```text
[R760] PASS Conformance - tb/verilator/ctrl_service_budget/README.md:843,846,854 - each changed claim against the raw window logs read through grade.py, and the #814 ancestry and stage_spi_phy at 5b5f4336
[R760] PASS RTL - receipts/delta-and-ancestry.txt - the delta's diff-tree names one README, no hdl/ path and no gitlink; the prior verdict stands because nothing it depends on changed
[R760] PASS Robustness - receipts/recompute-grader.txt, reviews/R760-2/receipts/refusals-{base,head}.txt - the two refused windows' ring occupancy and GM population at all three settings match the README; the delta changes no input path
[R760] PASS Tests - receipts/readme-table-check.txt - 48 cells match and the negative control fails on the old cell; the delta changes no test or harness code
[R760] PASS Docs - tb/verilator/ctrl_service_budget/README.md:843,846,854, live PR body, receipts/doc-gates.txt - gates reproduced and stale values swept; R760-3-R1 and R760-3-R2 are RESIDUE and do not leave this lens unclean
```

## Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `ctrl_service_budget/README.md:843,846,854` against the raw logs and `grade.py`; `8adf5c99` ancestry; `stage_spi_phy` at the base | R760-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| RTL | CLEAN | Delta diff-tree: no `hdl/` path, no gitlink. The wider RTL verdict rests on R760-1 at `9f81df00` and R760-2 at `fa019799`, and nothing in this lens's scope has changed since | R760-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| Robustness | CLEAN | Refused windows' ring and GM figures at three settings; refusal receipts. The deeper refused-path verdict rests on R760-2 at `fa019799`, whose inputs are unchanged | R760-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| Tests | CLEAN, suggestions on record | The 48-cell table check and its negative control; delta diff-tree: no test code. The suite verdicts rest on the rounds above, whose inputs are unchanged | R760-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |
| Docs | CLEAN, two RESIDUE and suggestions on record | The three changed lines, live PR body, `author-r3` packet, four doc gates plus `git diff --check` | R760-3 | `b2a1d67745229d167a5e70d7e1c5064975f027fd` |

## Real limits

- No harness, suite or build ran. The figures rest on raw window logs published at `fa019799` (`reviews/R759-2/receipts/raw-windows/`), cross-checked against `reviews/R760-2/receipts/`. Every published file I fetched matches `MANIFEST.json` at `723eb53c` (`receipts/evidence-verify.txt`). The README is the only byte changed since those logs.
- The no-stage and base raw logs are byte-identical. Two reviewers' separate runs agree on this (`reviews/R760-2/receipts/windows-base.txt` equals `windows-nostage.txt`), and I did not run a third.
- As scoped to the delta, I did not re-read the issue's acceptance or the code the delta leaves alone. Those verdicts are carried from earlier rounds as stated above.
- No source-head execution is claimed at this head beyond the doc gates, the merge-base `git diff --check` and the read-only recomputation. No manager source bank ran here.
- Hosted snapshot, `receipts/hosted-checks.txt`: 7 succeeded, 1 skipped, 17 in progress, 17 queued. It is a snapshot, not an acceptance, and the skipped context executed nothing.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Validate the current-dev merge candidate at the merge turn (source base `5b5f4336`, live dev `1f29f189`), with builder and native banks, and link the receipts.
- Own hosted and local-replica acceptance at the exact head.
- Carry R760-3-R1 and R760-3-R2 to the residue checklist.
- Obtain the internal reviewer's verdict at this head. Merge needs two positives and explicit maintainer authorization.

The clone is restored: head, index tree and required gitlinks match the published tree, and the status is empty including ignored files (`receipts/clone-restored.txt`).

R760-3 FINISHED
