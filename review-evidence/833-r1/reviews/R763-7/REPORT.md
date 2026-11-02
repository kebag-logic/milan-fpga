[R763] NEGATIVE - exact head 887fdd53b013cc8796c1d595644a2a9f0b8c27a5

Round R763-7, internal independent review of kebag-logic/milan-fpga PR #834 (Issue #833).

- **Head:** `887fdd53b013cc8796c1d595644a2a9f0b8c27a5`, tree `879912849c1a14eb3714027f799b804a33707f2d`.
- **Delta judged:** `a987b601a0..887fdd53b0`, five commits touching `docs/testing/TESTING.md`, `scripts/process_test_support.py` and `scripts/test_suite_cancellation.py`. `scripts/owned_process.py` is byte-identical across the delta.
- **Authority:** the manager's round 7 ruling on #833:
  - pin, never narrow;
  - each row's domain note must equal what the row states;
  - the bar is unchanged.

## Summary

- **The ruling's named items are met at their cause.** R764-6-F1, R764-6-F2 and R763-6-F1 are resolved as specified.
  - `rv6-sigkill-by-number`, `rv6-sigcont-by-number`, `rv6-resume-not-before-grace`, `rv6-resume-not-first-pass`, `sigterm-to-new` and `rv6-sigterm-trap-commands` are each red on a named control, with their words.
  - The R764-6-R1, R2 and R3 exact fixes are applied.
  - R764-6's `row_mutants.py` has no survivor among its ten.
- **The product is unchanged and correct in every probe.** The real-process grace probe passes 5 of 5 at the head.
- **The committed campaign passes.** It has 99 mutants, 96 of them with a control. Every one of the 96 is red with its words, and `none` is green on all ten controls.
- **Preflight cost is unchanged from round 6.**
- **Two new MINOR findings remain.** Both have round 6's shape: a row's domain note claims a case no control exercises, so a reviewer mutant that breaks that row is green on all ten owner controls.
  - **F1, rows 3, 5, 6 and 8:** no control resumes the shell in a pass after the first while still inside grace.
    - This is the common real case: the shell's only child exits on its first-pass `SIGTERM`, and the shell is resumed about 0.04 s later.
    - Row 3's own domain, "resumed from the first pass to the last before 14 s", includes that case.
    - Three mutants are green on every control. One of them also fails the real-process probe.
  - **F2, row 2:** no listing has a descendant new since the first census while a cancelled shell is still stopped.
    - Row 2's domain claims this as "before any resume".
    - Its only such listing has no cancelled shell at all.
- **Each finding closes with one more `owner_stated_seconds` listing.** Both are shown in disposable copies: green at the head product, red on every mutant that was green on all ten controls.

## Scope reconstructed

- **Authorities:**
  - AGENTS.md and CONTRIBUTING.md (sections 6 and 7);
  - the #833 round 6 ruling (`issuecomment-6582585294`) and round 7 ruling (`issuecomment-6585868556`);
  - `docs/testing/TESTING.md:254-287`: the cleanup table, its domain notes and the not-pinned list;
  - the delta diff;
  - the author's `REVIEW READY` (`issuecomment-6587935556`) and the PR body's "Round 7" section.
- **Published evidence:** `review-evidence/833-r1` at `9f44c6b6`:
  - `author-r7/receipts/final/*`;
  - the `R763-6/probes` and `R764-6/scripts` probes.
- **Order:** I read round 6's findings (R763-6, R764-6) only after my own pass over the delta.

## Focus checks

### 1. R764-6-F1, row 1: RESOLVED

- **The control.** `owner_reused_identity` (`test_suite_cancellation.py:876-921`) hands the number over for `SIGTERM` and again for `SIGKILL`.
  - Each handover uses its own entry process and a stale start-time check.
  - `BLOCKING` blocks `SIGTERM` and `SIGCONT`.
  - `pending()` reads `SigPnd | ShdPnd` (`:870-873`).
  - A `SIGKILL` sent by number stays in `ShdPnd` until its target is collected, so no timing is involved. The author's `sigkill-pending.log` shows no sample lacking the bit.
- **Red with words at this head:**
  - `rv6-sigkill-by-number`: `['SIGKILL']`;
  - `rv6-sigcont-by-number`: `['SIGCONT']`;
  - `sigcont-by-number-after-kill` and `recheck-spares-sigkill` (`receipts/committed_mutants.log`).
- **R764-6's `row_mutants.py`:** no survivor among its 10 (`receipts/row_mutants.log`).
- **My own edge mutant** `r7-check-before-open-sigkill` rechecks before the handle opens, for `SIGKILL` only. It is red: "...after it changed hands: ['SIGKILL']" (`receipts/r7_mutants.log`).
- So any signal `_send` sends by number after the handover is red.

### 2. R764-6-F2 and R763-6-F1: RESOLVED as the ruling specified

- **The listing.** `owner_stated_seconds` resumes a shell in its first pass, with nothing else live and inside grace (`:841`). Its trap's command is listed from the next pass, and it gets:
  - no `SIGTERM`;
  - no `SIGKILL` until 10 s.
- **The named mutants.**
  - Red with "a first-pass resume's stated seconds were not kept":
    - `rv6-resume-not-before-grace`;
    - `rv6-resume-not-first-pass`;
    - `sigterm-to-new`;
    - `rv6-sigterm-trap-commands`.
  - Red with "a new descendant's ...": `sigterm-to-new-before-resume`.
- **`grace_resume_probe.py`** at the head: PASS 5 of 5 (`receipts/grace_resume_head.log`).
- **The corrected probe** (described under F1): PASS 3 of 3 at the head. `sigterm-to-new` and `rv6-sigterm-trap-commands` each FAIL 3 of 3 (`receipts/grace2-*.log`).
- **Not-pinned item 2 is removed.** The PR body says "all of it is pinned", which is not true: see F1 and F2.

### 3. Domain notes against rows

- **Table check.** `scripts/table_check.py` parses all 16 rows (`receipts/table_check.log`): 0 problems.
  - Each of the 96 listed mutants is in `MUTANTS` and bound to a control its row lists.
  - No bound mutant is missing from the table.
- **Row texts.** Only rows 1, 2, 6, 12 and 15 changed.
  - Rows 1, 12 and 15 take the R764-6-R1 and R2 exact texts.
  - Rows 2 and 6 *widen*:
    - row 2 adds that a new descendant gets no `SIGTERM`;
    - row 6 adds that the trap's command gets none, even inside grace.
  - No row was narrowed.
- **Row 10.** Its text is identical; only its control list changed, dropping `owner_shell_window` (R764-6-R3, the first exact fix). Its three mutants are red on `owner_stated_seconds`:
  - `clock-always-cap`;
  - `first-pass-full-cap`;
  - `tick-passes-count-nothing`.
- **Gaps.** The domain notes for rows 2, 3, 5, 6 and 8 claim cases no listing exercises: F1 and F2.

### 4. The author's edge mutants

- All 18 listed in the PR body are in `MUTANTS` and named in their rows.
- Each is red on its control with its words (`receipts/committed_mutants.log`):
  - `owned-process mutants: PASS (99 mutants, 96 with a control that must fail)`;
  - `none` is green on all 10.

### 5. Residues R764-6-R1, R2 and R3: all RESOLVED

- **R1:** applied verbatim (`TESTING.md:264`).
- **R2:**
  - row 12's sentence is appended verbatim (`:275`);
  - row 15 reads "every descendant it reports that it has not collected" (`:278`).
- **R3:** `owner_shell_window` is dropped from row 10.

### 6. Preflight cost against round 6

Old (`a987b601`) and new were run interleaved (`receipts/preflight_cost.log`).

| Run | Old | New |
|---|---|---|
| `owner_stated_seconds` | 0.170-0.184 s | 0.178-0.197 s |
| `owner_reused_identity` | 0.145-0.166 s | 0.123-0.199 s |
| Whole test | 60.82 s and 61.05 s | 60.88 s and 61.08 s |

- Every run is rc 0.
- This matches the author's `cost.txt`: no measurable change.

## Findings

### R763-7-F1 - MINOR - Conformance, Tests, Docs - no control resumes the shell in a later pass inside grace

- **Locations:**
  - `docs/testing/TESTING.md:266` (row 3's domain), `:268` (row 5), `:269` (row 6), `:271` (row 8);
  - `docs/testing/TESTING.md:257-258`: "Together they cover all that the row states";
  - `scripts/test_suite_cancellation.py:793-856`: `owner_stated_seconds` resumes only at 0, 3, 5.5 and 14 - 2^-20 s;
  - PR body, Round 7, the R763-6-F1 row: "Not-pinned item 2 is gone, because all of it is pinned".
- **Authority:**
  - The round 7 ruling: each row's domain "must equal what the row states", and a survivor against a listed row is a finding.
  - Row 3: a cancelled shell and any command its trap started "keep the shell's own window". Its domain covers them "resumed from the first pass to the last before 14 s".
  - Row 5: the shell "is resumed in the first pass in which none does".
  - Row 6: the trap's command "gets no `SIGTERM` either, even when the resume comes inside grace". Its domain is only "after a first-pass resume".
  - Row 8: "Nor does a command its trap starts."
- **Evidence: what no listing has.** A resume inside grace happens only in pass 1, at clock 0. No listing has its shell resumed in a later pass while the clock is still under 2 s.
- **Evidence: three reviewer mutants green on all ten owner controls** (`scripts/r7_mutants.py`, `receipts/r7_mutants.log`):
  - `r7-no-resume-in-grace-after-pass-1` adds `and not (passes > 1 and clock < deadline)` to the resume condition. Such a resume slips to 2 s, which breaks row 5.
  - `r7-sigterm-trap-command-later-grace-resume` keeps the grace skip for new descendants only `if resumed is None or resumed == 0.0`. This breaks rows 2 and 6.
  - `r7-trap-window-not-later-grace` keeps the trap command's window only `if resumed == 0.0 or resumed >= deadline`. The command is killed at 2 s, which breaks rows 3 and 8.
- **Evidence: this is the ordinary sweep case.** `scripts/grace_resume_probe2.py` stamps the resume on the shell's own handle only.
  - At production stages the head resumes the shell 0.04 s after cleanup's first `SIGTERM`, in a later pass, inside grace.
  - Under `r7-sigterm-trap-command-later-grace-resume`, the trap's `sleep 1.0` gets `SIGTERM` at 0.08 s. The probe FAILs 3 of 3 (`receipts/grace2-r7-sigterm-trap-command-later-grace-resume.log`).
  - The committed campaign and every owner control stay green under the same mutant.
- **Evidence: a correction to my own round 6 probe.**
  - `grace_resume_probe.py` stamped the resume on any `SIGCONT` sent while the shell was notified. That includes the `SIGCONT` `_send` sends to the child after its `SIGTERM`.
  - So its "resume -0.0 s", and round 6's "about 0.1 s", are artefacts.
  - Its PASS/FAIL verdicts are unaffected.
- **Impact:**
  - Three regressions would pass both the preflight and the `--mutants` campaign:
    - a `SIGTERM` to the trap's cleanup command after the most common resume;
    - killing that command at grace;
    - delaying that resume to 2 s.
  - The table says all of this is pinned: "Together they cover all that the row states", and row 3's "from the first pass to the last before 14 s".
  - The PR body removes not-pinned item 2 on the same false premise.
  - The domain notes for rows 6-8 also read as five resume points: "in the first pass, inside grace, at 3 s, at 5.5 s and a tick before 14 s". The control has four.
- **Required outcome, preferred** (the ruling: pin, never narrow):
  - A control resumes the shell in a pass after the first, while the owner's clock is still inside grace.
  - The trap's command then gets no `SIGTERM`, and no `SIGKILL` until 10 s after that resume.
  - The three mutants above, or equivalents, are red on it with words and named in rows 2, 3, 5, 6 and 8.
  - The domain notes name that resume.
  - Feasibility, not prescribed: one line, `kept("an in-grace resume", resumed_at(0.5), window(0.5), shell)`. It stays green at the head product and turns all three mutants red (`receipts/pin_feasibility.log`, `scripts/pin_feasibility.sh`).
- **Required outcome, otherwise:**
  - Narrow the rows and domain notes to what is pinned.
  - Restore this case to the not-pinned list with a true reason.
  - This contradicts "never narrow", so it needs the manager.
- **Either way:** correct the PR body's "all of it is pinned".
- **Verification:**
  - `python3 -B scripts/r7_mutants.py <clone> 8 r7-no-resume-in-grace-after-pass-1 r7-sigterm-trap-command-later-grace-resume r7-trap-window-not-later-grace` shows each red on a named control.
  - `--mutants` stays PASS, with `none` green.

### R763-7-F2 - MINOR - Conformance, Tests, Docs - no new descendant appears while a cancelled shell is stopped

- **Locations:**
  - `docs/testing/TESTING.md:265`, row 2: "A descendant new since that census gets none, so a terminal trap's cleanup command can run". Its domain says "over descendants new since then, before any resume ...".
  - `scripts/test_suite_cancellation.py:843-846`: the only listing with a new descendant before any resume, and it has no shell.
- **Authority:**
  - Row 2's domain claims new descendants "before any resume", and must equal the row (round 7 ruling).
  - The bar: a survivor against a listed row is a finding.
- **Evidence:**
  - The one such listing, "a new descendant", has no cancelled shell: `owner.root_notified` is False.
  - In every shell listing, the trap's command appears only at or after the resume.
  - So no listing has a descendant new since the first census while a cancelled shell is still stopped.
  - Reviewer mutant `r7-sigterm-new-while-shell-stopped` changes the grace skip to `if (pid, start) not in initial and (resumed is not None or not self.root_notified)`. A new descendant then gets `SIGTERM` while the cancelled shell waits.
  - That mutant is green on all ten owner controls (`receipts/r7_mutants_row2.log`).
- **Impact:**
  - Take a cancel: the top shell is stopped, and a nested recipe shell runs its own terminal trap after its first-pass `SIGTERM`.
  - Under the mutant, that trap's cleanup command gets `SIGTERM` during grace, which is exactly what row 2 says cannot happen.
  - The only listing that pins row 2's new-descendant clause is the no-cancel case.
- **Required outcome, preferred:**
  - A listing in which a cancelled shell stays stopped while a descendant new since the first census is listed inside grace and gets no `SIGTERM`.
  - The mutant, or an equivalent, is red on it with words and named in row 2.
  - Feasibility, not prescribed: a listing `{shell, child (of shell), cleanup (of child) from pass 2}` whose shell is never resumed. It stays green at the head and turns this mutant red (`receipts/pin_feasibility_row2.log`, `scripts/pin_feasibility_row2.sh`).
- **Required outcome, otherwise:**
  - Narrow row 2's domain to "with no cancelled shell".
  - Put the stopped-shell case on the not-pinned list with a true reason.
  - This needs the manager.
- **Verification:**
  - `python3 -B scripts/r7_mutants.py <clone> 8 r7-sigterm-new-while-shell-stopped` shows it red on a named control.
  - `--mutants` stays PASS.

### R763-7-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:283` (not-pinned item 1)

- Carried from R763-6-X2; the delta does not touch it.
- "`SIGKILL` ends it at grace without one" is wrong: a stopped first-census parent is killed by 4 s, not at grace.
- Exact fix: "`SIGKILL` ends it by 4 s without one."

### R763-7-R2 - RESIDUE - Docs - `docs/testing/TESTING.md:259`

- Carried from R763-6-X4; the delta does not touch it.
- Exact fix: "Times are cleanup's, on the owner's clock, and each deadline fails the run in the first census pass at or past it."

### R763-7-R3 - RESIDUE - Docs - `docs/testing/TESTING.md:269-271` (domain notes of rows 6, 7 and 8)

- "resumes in the first pass, inside grace, at 3 s, at 5.5 s and a tick before 14 s" reads as five resume points.
- `owner_stated_seconds` has four: `resumes=[0, 3, 5.5, last]`.
- Exact fix: "resumes in the first pass (inside grace), at 3 s, at 5.5 s and a tick before 14 s".
- If the F1 fix adds a later-pass resume inside grace, list it here instead.

### R763-7-S1 - SUGGESTION - Docs, Tests - `scripts/process_test_support.py:508-586`, `docs/testing/TESTING.md:264-279`

- The new `MUTANTS` names `rv6-*` carry a review-round prefix into a durable test identifier and the authoritative table.
- They are not comments, and the ruling named them, so the comment rule's RESIDUE does not apply.
- Optional: rename them to behaviour names when the table is next touched, for example `sigkill-by-number` or `resume-only-past-grace`.

### R763-7-S2 - SUGGESTION - Tests - the round 6 probe `grace_resume_probe.py`

- If that probe is quoted as evidence again, use `scripts/grace_resume_probe2.py`, which stamps the resume on `owner.root_fd` only.
- See the correction under F1.

### Comment rule

- I checked every comment line the delta adds (`git diff a987b601..887fdd53`).
- None shows a lane label, lane name, review round, reviewer ID or comment ID.
- `(#833)` is an Issue ID.

## Prior findings at this head

| Finding | Severity | Status at `887fdd53` | Evidence |
|---|---|---|---|
| R764-6-F1 (row 1: `SIGKILL`/`SIGCONT` by number) | MINOR | RESOLVED at its cause: both red on `owner_reused_identity` with words. Any `_send` signal by number after the handover is red | `receipts/committed_mutants.log`, `row_mutants.log`, `r7_mutants.log` |
| R764-6-F2 (row 5: no first-pass resume) | MINOR | RESOLVED as specified. The remaining later-pass case inside grace is new F1 | `receipts/committed_mutants.log` |
| R763-6-F1 (rows 6/8: trap command inside grace) | MINOR | RESOLVED as the ruling specified: the first-pass listing, with `sigterm-to-new` and `rv6-sigterm-trap-commands` red. Its realistic later-pass case is still unpinned: new F1 | `receipts/committed_mutants.log`, `grace2-*.log` |
| R764-6-R1, R2, R3 | RESIDUE | RESOLVED with the exact fixes | `TESTING.md:264,275,278` and row 10 |
| R764-6-S1 (direct preflight under an ignored SIGHUP) | SUGGESTION | Not taken: it predates this PR and is outside #833's scope | PR body |
| R764-6-S2 (domain notes) | Required by the ruling | Applied. Two notes overstate their coverage: F1, F2 | `TESTING.md:257-279` |
| R763-6-X1, X3 | RESIDUE | Subsumed by R764-6-R1 and R2, which are applied | `TESTING.md:264,278` |
| R763-6-X2, X4 | RESIDUE | Retained as R763-7-R1 and R2 | `TESTING.md:259,283` |
| R763-6-S1 (return before confirm) | SUGGESTION | TAKEN: `rv6-return-before-confirm` is red on `owner_vanishing` and named in row 12 | `receipts/committed_mutants.log` |

## Lens results

```text
[R763] MINOR Conformance - docs/testing/TESTING.md:257-271 vs round 7 ruling - R763-7-F1, R763-7-F2: domain notes for rows 2, 3, 5, 6, 8 claim cases no control exercises; mutants against those rows stay green on every control. owned_process.py is unchanged in the delta; the product is correct in every probe (receipts/grace_resume_head.log; pin_feasibility*.log, none rc 0).
[R763] PASS RTL - PR file list 1f29f189..887fdd53 (docs/testing/TESTING.md, scripts/owned_process.py, scripts/process_test_support.py, scripts/test_suite_cancellation.py, tb/verilator/gptp_shadow/test_mutant_lifecycle.py) - no HDL, CDC, FSM or interface artifact in the PR or the delta, so the lens is inapplicable by the diff; the delta changes nothing the prior RTL verdict depends on.
[R763] PASS Robustness - scripts/test_suite_cancellation.py:741-921 at 887fdd53 - patched time, os.pidfd_open, _identity and owner hooks are restored in finally; the starved clock is bounded (clock < 100) and exact in binary; reused-identity detection uses pending bits, not timing; the campaign at 8 jobs beside 9 more jobs under load 25-68 is PASS (receipts/committed_mutants.log); the whole test is rc 0 four times (receipts/preflight_cost.log, whole-*.log).
[R763] MINOR Tests - scripts/test_suite_cancellation.py:793-856, scripts/process_test_support.py:429-586 - R763-7-F1, R763-7-F2: four reviewer mutants green on all ten owner controls (receipts/r7_mutants.log, r7_mutants_row2.log). Everything else checks: committed campaign PASS 99/96, row_mutants.py no survivor, table check 0 problems.
[R763] MINOR Docs - docs/testing/TESTING.md:257-283, PR body Round 7 - R763-7-F1, R763-7-F2: domain notes and "all of it is pinned" overstate coverage. RESIDUE R763-7-R1 to R3; SUGGESTION S1, S2. No comment-rule instance in the delta.
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2 open) | `TESTING.md:254-287` vs the round 7 ruling; `owned_process.py:240-339` (unchanged); #833 acceptance (product unchanged) | R763-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| RTL | CLEAN | PR file list; no HDL in the PR or the delta | R763-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| Robustness | CLEAN | `test_suite_cancellation.py:741-921`; campaign and whole-test receipts under load | R763-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| Tests | UNCLEAN (F1, F2 open) | `test_suite_cancellation.py:741-921`; `process_test_support.py:426-586`; `receipts/committed_mutants.log`, `row_mutants.log`, `r7_mutants*.log`, `grace*.log`, `table_check.log` | R763-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| Docs | UNCLEAN (F1, F2 open; RESIDUE R1-R3) | `TESTING.md:254-287`; delta comments and docstrings; PR body Round 7; the `REVIEW READY` comment | R763-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |

## Executed

All runs were at the exact head, from this clone or from exported trees. Their receipts are listed in `MANIFEST.sha256`.

- **Committed campaign.** `python3 -B scripts/test_suite_cancellation.py --mutants --jobs 8`: rc 0, `owned-process mutants: PASS (99 mutants, 96 with a control that must fail)` (`receipts/committed_mutants.log`).
- **R764-6's probe, unchanged.** `python3 -B scripts/row_mutants.py <clone> 3`: no survivor among 10 (`receipts/row_mutants.log`).
- **My edge mutants.**
  - `python3 -B scripts/r7_mutants.py <clone> 3`: 1 red and 3 green on every control (`receipts/r7_mutants.log`). This ran before the fifth entry was added to the script.
  - Then `... 10 r7-sigterm-new-while-shell-stopped`: green on every control (`receipts/r7_mutants_row2.log`).
- **Grace probes.**
  - `python3 -I -B scripts/grace_resume_probe.py <clone>/scripts 5`: PASS 5 of 5.
  - `grace_resume_probe2.py` on `none` and on three mutant trees: PASS 3 of 3 at the head, FAIL 3 of 3 on each mutant (`receipts/grace*.log`).
- **Pin feasibility,** in disposable copies (`receipts/pin_feasibility*.log`).
- **Table check.** `scripts/table_check.py`: rc 0 (`receipts/table_check.log`).
- **Cost.** Old and new interleaved (`receipts/preflight_cost.log`, `receipts/whole-*.log`).
- **Hosted snapshot** (`receipts/hosted_snapshot.txt`).
- **Restore check** (`receipts/restore_check.txt`):
  - HEAD and its tree are exact;
  - the worktree and the index equal HEAD;
  - the six submodule gitlinks match HEAD;
  - my probes had created an ignored `scripts/__pycache__`, which I removed;
  - `git status --porcelain --ignored` is empty.

## Real limits

- **What was probed.** Product behaviour was probed through the mocked starved-clock listings and one real-process probe, the grace probe.
- **What was not run.** No full parent, PP, gPTP, Yosys or builder bank, and no `--matrix`. I spot-checked the author's published `--matrix` and gate receipts but did not re-run them.
- **Host load** was 12-68 from other tenants during the runs.
- **Hosted checks** at the head were still running at the snapshot: 11 success, 1 skipped (physical gPTP, nightly or manual), 36 queued or in progress. No conclusion is drawn from them; the manager owns hosted and act acceptance.
- **No manager source bank** ran at this head, and none is claimed or inferred.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **The feasibility listings** are review probes in disposable copies, not proposed source.

## Pending manager duties

- Publish this report.
- Rule on F1 and F2: pin them as shown, or authorize a narrowing.
- Carry RESIDUE R763-7-R1, R2 and R3 to the residue checklist.
- At the merge turn, build and validate the current-dev merge candidate and link its receipts:
  - source base `1f29f189279f9fc0132f4918e47342b87d22f33a`;
  - live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- Hosted and act acceptance at the final head.

R763-7 FINISHED
