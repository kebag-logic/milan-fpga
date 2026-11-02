[R764] NEGATIVE - exact head 887fdd53b013cc8796c1d595644a2a9f0b8c27a5

Round R764-7. External independent review of issue #833 / PR #834 at exact head `887fdd53b013cc8796c1d595644a2a9f0b8c27a5`, tree `879912849c1a14eb3714027f799b804a33707f2d`. The delta under review is `a987b601..887fdd53`: five one-line commits, tests and docs only. `scripts/owned_process.py` is byte-identical to round 6 (blob `6495a47b`).

## Summary

- **One open MINOR, R764-7-F1 (Conformance, Tests, Docs).** Three reviewer mutants survive every owner control and the whole test. Each one breaks the case where the cancelled shell is resumed **inside grace, after the first pass**: the shell's child exits on its first-pass `SIGTERM`, and the shell is resumed in a later pass while the clock is still under 2 s.
  - This is the ordinary production path for a cancel while a command runs.
  - Rows 2, 3, 5, 6, 7 and 8 state this case. Row 3's own domain note claims it ("resumed from the first pass to the last before 14 s").
  - The only in-grace resume in `owner_stated_seconds` is the first-pass one with nothing else ever live.
  - One of the three survivors, a `SIGTERM` to the trap's command, makes a real trap's cleanup command fail on a real process (`receipts/grace-resume-mutants.log`).
  - One more listing in that control kills all three (`receipts/rv7-pin-feasibility.log`).
- **Every named prior finding is resolved at its cause.** That covers R764-6-F1, R764-6-F2 as the round 6 ruling framed it, R763-6-F1, and R764-6-R1, R2 and R3.
  - Every mutant the ruling names is red with its words.
  - Not-pinned item 2 was removed, not narrowed. Its pinned part is now in row 2. The part that F1 shows still unpinned is now stated but not pinned.
  - Row 10's change is a control-list change only: the row text is byte-identical to round 6.
- **The product is correct in every probe**:
  - the full test passes, rc 0;
  - the campaign passes, with 96 of 96 controlled mutants red with their words and `none` green;
  - the real-process grace-resume probe passes 5 of 5.
- **Preflight cost is unchanged within noise**:
  - `owner_stated_seconds`: 0.146 s now, 0.137 s at round 6;
  - `owner_reused_identity`: 0.137 s now, 0.134 s at round 6;
  - the whole test: 60.8 s.
- **The comment rule holds.** No added comment or docstring in the delta carries a lane label, round, reviewer ID or comment ID.

## Findings

**R764-7-F1 - MINOR - Conformance, Tests, Docs - `scripts/test_suite_cancellation.py:793-857` (`owner_stated_seconds`: `resumed_at` `:812`, `window` `:817`, the `kept` listings `:832-855`) vs `docs/testing/TESTING.md:265,266,268,269,270,271` (cleanup table rows 2, 3, 5, 6, 7, 8) and `:258` ("Together they cover all that the row states"); `scripts/owned_process.py:304,312,322,332`**

- **Authority and evidence.**
  - The round 7 ruling on #833 (issuecomment-6585868556) says to pin and never narrow. It requires each row's domain note to "equal what the row states", and a survivor against a listed row is a finding.
  - At this head `TESTING.md:257-258` says: "Beside each control is the domain it covers ... Together they cover all that the row states."
  - The REVIEW READY comment (issuecomment-6587935556) says "each domain equals its row".
  - Rows that state the case:
    - Row 2 (`:265`): "A descendant new since that census gets none [`SIGTERM`], so a terminal trap's cleanup command can run". Its domain is "before any resume and after one in the first pass, inside grace".
    - Row 3 (`:266`): the shell and its trap's command "keep the shell's own window". Its domain is "resumed from the first pass to the last before 14 s".
    - Row 5 (`:268`): the shell is "resumed in the first pass in which none does".
    - Row 6 (`:269`): "ten seconds of its own ... and so does any command that trap starts, which gets no `SIGTERM` either, even when the resume comes inside grace".
    - Rows 7 and 8 (`:270-271`): no `SIGKILL` to the shell or its trap's command inside that window.
  - Resumes the controls actually make:
    - `owner_stated_seconds` resumes at 0 (first pass, nothing ever live), 3, 5.5 and 14 - 2^-20 s (`:840-853`);
    - `owner_shell_window` resumes past the time that kills the rest;
    - none resumes inside grace after pass 1.
  - The test's own docstring (`:797-799`) lists "in the first pass, inside grace, between grace and 4 s, late, or in the last pass before 14 s". That reads as an in-grace resume besides the first-pass one, and none exists.
- **Reviewer mutants** (`scripts/rv7_mutants.py`, applied by the repository's own `mutant_tree` and run by its `run_mutant`):

  | Mutant | Edit | Rows it breaks | Result |
  |---|---|---|---|
  | `rv7-sigterm-trap-command-later-grace-resume` | `if (pid, start) not in initial and not (resumed is not None and resumed > 0): continue`: new descendants get `SIGTERM` after a resume inside grace that is not at 0 | 2, 6 | green on all 10 owner controls (`receipts/rv7-mutants.log`) and on the whole test, rc 0 in 60.9 s (`receipts/rv7-mutants-whole.log`) |
  | `rv7-no-resume-later-in-grace` | resume condition `... and not (passes > 1 and clock < deadline)` | 5 | green on all 10 and on the whole test |
  | `rv7-no-window-later-in-grace` | `kill_all = max(kill_all, clock + TRAP_SECONDS) if clock >= deadline or passes == 1 else kill_all`: a shell resumed inside grace after pass 1 is killed at 4 s instead of 10 s after its resume | 3, 6, 7, 8 | green on all 10 and on the whole test |

  Control: `rv7-sigterm-to-new-after-1s` is red on `owner_stated_seconds`. So the harness does see a `SIGTERM` to a new descendant during grace. It does not see one that depends on the resume being in grace after pass 1.
- **Impact.**
  - The case is the common one in production. A cancel arrives while the sweep shell waits on a command. That child exits on its first-pass `SIGTERM`, and the shell is resumed some 20 ms in, inside grace.
  - On real processes, the reviewer grace-resume probe (unchanged from round 6) shows the effect at this head. Unmutated it passes 5 of 5 (`receipts/grace-resume.log`).
  - Under `rv7-sigterm-trap-command-later-grace-resume` it fails 2 of 2: "trap command did not finish inside the shell's window", with the trap's `sleep` sent `SIGTERM` at 0.08 s (`receipts/grace-resume-mutants.log`). That is exactly what row 2 says cannot happen ("so a terminal trap's cleanup command can run").
  - Under `rv7-no-window-later-in-grace`, the shell's trap has 3 s, not 10 s. Nothing committed would see either regression.
- **Required outcome.**
  - Rows 2, 3, 5, 6, 7 and 8 are pinned for a resume inside grace after the first pass, per the ruling's "pin, never narrow".
  - All three mutants then join `MUTANTS`, each red on a named control with its words, and are named in their rows. The domain notes and the `owner_stated_seconds` docstring then state that resume.
  - Shape is not prescribed. Feasibility: one more line in `owner_stated_seconds` works, `kept("an in-grace resume", resumed_at(1), window(1), shell)`, where the child is gone at 1 s and the trap's command is listed from then. It is green at head, and each of the three mutants is red on it with "an in-grace resume's stated seconds were not kept" (`receipts/rv7-pin-feasibility.log`, `scripts/rv7_pin_feasibility.py`). It adds no measurable time.
  - Narrowing rows 2, 3, 5, 6, 7 and 8 instead would contradict the ruling and needs the manager.
- **Verification.**
  - `python3 -B scripts/rv7_mutants.py <clone> 4` (this packet) shows no survivor.
  - `--mutants` stays PASS with the three added, and `none` stays green.
  - `python3 -I scripts/grace_resume_probe.py <clone>/scripts 3` still passes.

### RESIDUE (wording only; non-blocking; for the residue checklist)

**R764-7-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:276` (row 13, re-parented descendant), domain note**

- The note reads: "over a real child re-parented to the owner between the first census and that pass's signals; that pass is the only one that sends `SIGTERM`".
- As a statement about cleanup that is not so. Every pass inside grace sends `SIGTERM` to a first-census entry not yet notified (`owned_process.py:313-336`).
- What `owner_reparented` pins is that the child's `SIGTERM` comes in that pass and not a later one (`test_suite_cancellation.py:497`).
- **Exact fix:** replace "; that pass is the only one that sends `SIGTERM`" with ", which gets its `SIGTERM` in that pass and not a later one".

**R764-7-R2 - RESIDUE - Tests (docstring wording) - `scripts/test_suite_cancellation.py:797-799` (`owner_stated_seconds` docstring)**

- The text "in the first pass, inside grace, between grace and 4 s, late, or in the last pass before 14 s" lists five resume cases, and the control has four.
- If R764-7-F1 is answered with an in-grace resume after pass 1, the sentence becomes true as written. Otherwise the **exact fix** is: "in the first pass, which is inside grace; between grace and 4 s; late; or in the last pass before 14 s".

### SUGGESTION (optional)

**R764-7-S1 - SUGGESTION - Tests, Docs - `scripts/process_test_support.py` `MUTANTS` keys `rv6-*`; `docs/testing/TESTING.md:264,268,269,275`**

- Six committed mutant names carry a review-round prefix: `rv6-sigkill-by-number`, `rv6-sigcont-by-number`, `rv6-resume-not-before-grace`, `rv6-resume-not-first-pass`, `rv6-sigterm-trap-commands` and `rv6-return-before-confirm`.
- These are identifiers, not comments, so the comment rule does not reach them. But they put a round label into the durable table.
- Descriptive names would keep the table free of review history, for example `sigkill-by-number`, `resume-not-first-pass` and `return-before-confirm`.
- Renaming is optional. Any reviewer probe that reuses the old names would need the same rename.

**R764-7-S2 - SUGGESTION - Tests - `MUTANTS` entries `trap-commands-1s`, `shell-window-one-pass` (control `owner_shell_window`)**

- The author's REVIEW READY reports both as load-sensitive on the real-time `owner_shell_window`.
- Both are red, with no timing involved, on `owner_stated_seconds` (`receipts/stated-seconds-check.log`).
- Binding them there, or to both controls, would remove the load dependence from the campaign. As the author says, this is a manager decision.

**R764-6-S1 - SUGGESTION - retained, not taken (author: predates this PR and is outside #833; suggested as a new Issue)**

- It reproduced again here by accident. The first full run was started under a launcher that ignores SIGHUP, and it failed only at `hard-HUP` with `TimeoutExpired` after 60 s, rc 1 (`receipts/full-test-sighup-ignored.log`).
- The same head with SIGHUP at its default passes, rc 0 (`receipts/full-test.log`).
- This is not a defect of this delta.

## Prior findings at this head

| Finding | Status at `887fdd53` | Evidence |
|---|---|---|
| R764-6-F1, row 1: `SIGKILL` and `SIGCONT` by number survive | **RESOLVED** | The handover runs for `SIGTERM` and `SIGKILL` (`test_suite_cancellation.py:876-921`). `BLOCKING` now blocks `SIGTERM` and `SIGCONT`, and a `SIGKILL` shows pending on the uncollected process. Red with "a census entry was signalled by its number", each naming the caught signal: `rv6-sigkill-by-number` (`['SIGKILL']`), `rv6-sigcont-by-number` (`['SIGCONT']`), `sigcont-by-number-after-kill` and `recheck-spares-sigkill` (`receipts/mutants-all.log`). Round 6's `scripts/row_mutants.py` has no survivor among its 10, including `rv6-sigterm-by-number` (`receipts/row-mutants.log`). Every signal `_send` sends by number after the handover is red: `SIGTERM`, `SIGKILL`, and `SIGCONT` after either. All are named in row 1. |
| R764-6-F2, row 5: no first-pass resume | **RESOLVED** as required: a control resumes in pass 1, and both mutants are red | `kept("a first-pass resume", resumed_at(0), window(0), shell)` (`:841`). `rv6-resume-not-before-grace` and `rv6-resume-not-first-pass` are red with "a first-pass resume's stated seconds were not kept" (`receipts/mutants-all.log`), and both are named in row 5. The neighbouring in-grace resume after pass 1 is the new R764-7-F1. It is not a retained F2, because F2's required outcome is met. |
| R763-6-F1, rows 6 and 8: `sigterm-to-new` filed as "breaks no row" | **RESOLVED** | `sigterm-to-new` now has control `owner_stated_seconds` and is red with its words. `rv6-sigterm-trap-commands` and the lane's `sigterm-to-new-before-resume` are red. After the first-pass resume, the trap's command gets no `SIGTERM` and no `SIGKILL` before 10 s, and `trap-commands-spared-only-past-grace` and `no-window-inside-grace` are red. Not-pinned item 2 is removed, and the statement moved to row 2 as pinned. The resume inside grace after pass 1 is carried by R764-7-F1. |
| R764-6-R1, row 1 wording | **RESOLVED** with the exact fix | Row 1's first two sentences (`TESTING.md:264`) match the fix verbatim. |
| R764-6-R2, rows 12 and 15 | **RESOLVED** with the exact fix | Row 12 appends "A listing that dies inside every census is the one exception: its failure names each entry as exited." This is pinned by `owner_vanishing` (`test_suite_cancellation.py:692`), and `rv6-return-before-confirm` is red. Row 15 reads "to every descendant it reports that it has not collected". That is the exact fix, a correction of wording to the product's unchanged behaviour (`owned_process.py:297-298`), not a narrowing. |
| R764-6-R3, row 10 | **RESOLVED** with the first exact fix | `owner_shell_window` is dropped from row 10's control list. The row's statement is byte-identical to round 6 ("A pass shorter than that advances the clock by its own length: wall time runs ahead of the owner's clock only while a pass takes longer."). Its mutants (`clock-always-cap`, `first-pass-full-cap`, and the new `tick-passes-count-nothing`) are red on `owner_stated_seconds`. This is a control-list change, and no behaviour was narrowed. |
| R764-6-S2, per-row domain note | **TAKEN**. One shortfall is R764-7-F1 | Every row now carries a domain note. Rows 2, 3, 5, 6, 7 and 8 fall short for an in-grace resume after pass 1, and row 13's note has R764-7-R1. |
| R764-6-S1, SIGHUP launcher | Not taken, out of scope | See above. |

## Focus items

1. **R764-6-F1:** resolved, as in the table above.
2. **R764-6-F2 and R763-6-F1:** the first-pass, in-grace resume is in `owner_stated_seconds`.
   - `rv6-resume-not-before-grace`, `rv6-resume-not-first-pass`, `sigterm-to-new` and `rv6-sigterm-trap-commands` are each red with "a first-pass resume's stated seconds were not kept".
   - The narrower `sigterm-to-new-before-resume` is red with "a new descendant's stated seconds were not kept".
   - Not-pinned item 2 is gone, not reworded. The author says "all of it is pinned", and R764-7-F1 shows part of it is not: a new descendant after an in-grace resume in pass 2 or later.
   - `grace_resume_probe.py` at head: PASS 5 of 5. Its printed "resume" time records the `SIGCONT` that `_send` sends after each signal, not the shell's resume, so it reads -0.0 s. Its verdict is unaffected.
   - `row_mutants.py` at head: no survivor among its 10.
3. **Domain notes against the row statements.**
   - Rows 1, 4, 9, 10, 11, 12, 14, 15 and 16 match their statements.
   - Rows 2, 3, 5, 6, 7 and 8 fall short, which is F1. Row 13's note overstates, which is R1.
   - No row's statement was narrowed. Row 15's change is R764-6-R2's exact fix.
   - Row 10 dropped a control only.
   - `scripts/table_vs_mutants.py` gives rc 0, 16 rows, 96 controlled mutants, each in a row that lists its control (`receipts/table-vs-mutants.log`).
4. **Author's edge mutants (18 for 16 rows):** every one is in the campaign and red on its control with its words (`receipts/mutants-all.log`). The list is `grace-a-tick-short`, `kill-all-a-tick-early`, `verdict-a-tick-early`, `verdict-waits-for-resume`, `no-resume-before-verdict`, `trap-window-a-tick-short`, `no-window-inside-grace`, `trap-commands-spared-only-past-grace`, `cap-lifted-past-a-minute`, `tick-passes-count-nothing`, `vanishing-verdict-ignores-resume`, `no-reap-after-first-census`, `sigterm-rechecks-parent`, `resume-collected-shell-past-grace`, `verdict-sends-sigterm`, `killed-ago-from-start`, `recheck-spares-sigkill`, `sigcont-by-number-after-kill` and `sigterm-to-new-before-resume`. The edges they probe are times a tick early or late and starved passes. None sits at the in-grace-after-pass-1 resume of F1.
5. **Residues and preflight cost.** R764-6-R1, R2 and R3 are resolved, as in the table above.
   - Interleaved, 6 repetitions each (`receipts/preflight-cost-summary.txt`):
     - `owner_stated_seconds`: 0.146 s now, 0.137 s at `a987b601`;
     - `owner_reused_identity`: 0.137 s now, 0.134 s at `a987b601`.
   - Whole test: 60.8 s wall, maximum RSS 28 MB (`receipts/full-test.log`).

## Lens results

[R764] MINOR Conformance - `docs/testing/TESTING.md:258,265-271` vs the round 7 ruling (pin, never narrow; domain equals row) - R764-7-F1. The product's conformance to #833 acceptance items 1 and 2 is unchanged since round 6: `owned_process.py` blob `6495a47b`, full test PASS, grace probe PASS.

[R764] PASS RTL - `git diff --stat a987b601..887fdd53` (`docs/testing/TESTING.md`, `scripts/process_test_support.py`, `scripts/test_suite_cancellation.py`) and `receipts/restore-check.txt` - no HDL, constraint, CDC or interface artifact is in the delta, and none in the base..head diff either. The lens is inapplicable by that artifact.

[R764] PASS Robustness - `scripts/owned_process.py:256-339` (blob `6495a47b`, unchanged since `a987b601`); `receipts/full-test.log` (rc 0: INT/TERM boundaries, ordering, timeout, hard KILL/HUP); `receipts/grace-resume.log` (real shell resumed inside grace, its trap's command finishes, 5 of 5); `receipts/mutants-all.log` (`none` green on all 10 controls) - the timeout and ordering paths were re-exercised at head, with no defect in product behaviour.

[R764] MINOR Tests - `scripts/test_suite_cancellation.py:793-857`, `scripts/process_test_support.py` `MUTANTS` - R764-7-F1: three surviving mutants (`receipts/rv7-mutants.log`, `receipts/rv7-mutants-whole.log`). Everything else in the Tests delta was checked and is sound: the `owner_reused_identity` rework at `:876-921`; the starved clock at `:742-790`, with ticks exact in binary, passes from a tick to an hour, and verdict ages checked against a real process; and the campaign at PASS 99/96.

[R764] MINOR Docs - `docs/testing/TESTING.md:254-290` - R764-7-F1 (the claim at `:258` is false for rows 2, 3, 5, 6, 7 and 8); RESIDUE R764-7-R1 and R2.

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R764-7-F1 open) | `TESTING.md:254-290` (16 rows, preamble, not-pinned list) vs the round 7 ruling and #833 acceptance; `owned_process.py:256-339`; `receipts/rv7-mutants*.log`, `rv7-pin-feasibility.log`, `grace-resume*.log` | R764-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| RTL | CLEAN | delta file list; `receipts/restore-check.txt`; no HDL in base..head | R764-7 (inapplicable) | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| Robustness | CLEAN | `owned_process.py` (unchanged blob); `receipts/full-test.log`, `grace-resume.log`, `mutants-all.log` | R764-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| Tests | UNCLEAN (R764-7-F1 open) | `test_suite_cancellation.py:742-921`; `process_test_support.py` `MUTANTS` (+80 lines); `receipts/mutants-all.log`, `row-mutants.log`, `rv7-mutants*.log`, `table-vs-mutants.log`, `stated-seconds-check.log` | R764-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |
| Docs | UNCLEAN (R764-7-F1 open; RESIDUE R1, R2) | `docs/testing/TESTING.md:254-290`; author REVIEW READY (issuecomment-6587935556) | R764-7 | `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` |

## Executed (all at exact head, in the detached clone, SIGHUP at its default unless noted)

- `python3 -B scripts/test_suite_cancellation.py --mutants --jobs 6`: rc 0. "owned-process mutants: PASS (99 mutants, 96 with a control that must fail)" (`receipts/mutants-all.log`).
- `python3 -B scripts/test_suite_cancellation.py`: rc 0 in 1:00.76 (`receipts/full-test.log`).
  - An earlier run under a SIGHUP-ignoring launcher gave rc 1 at `hard-HUP` only (`receipts/full-test-sighup-ignored.log`; R764-6-S1).
- `scripts/row_mutants.py . 4` (round 6 probe, unchanged): rc 0, survivors [] (`receipts/row-mutants.log`).
- `scripts/grace_resume_probe.py scripts 5` (round 6 public probe, unchanged): PASS 5 of 5 (`receipts/grace-resume.log`). On two F1 mutant trees, 2 runs each (`receipts/grace-resume-mutants.log`):
  - the SIGTERM mutant: FAIL 2 of 2;
  - the window mutant: PASS 2 of 2, because 3 s exceeds the probe trap's 1 s command.
- `scripts/rv7_mutants.py . 4`: three survivors and one red control (`receipts/rv7-mutants.log`). With `RV7_WHOLE=1`, the three survive the whole test too (`receipts/rv7-mutants-whole.log`).
- `scripts/rv7_pin_feasibility.py . <scratch>`: PASS. One added listing is green unmutated and red on each survivor (`receipts/rv7-pin-feasibility.log`).
- `scripts/table_vs_mutants.py .`: rc 0 (`receipts/table-vs-mutants.log`).
- `scripts/stated_seconds_check.py . owner_stated_seconds trap-commands-1s shell-window-one-pass`: both red (`receipts/stated-seconds-check.log`).
- `scripts/preflight_cost.sh <a987b601 scripts> <887fdd53 scripts> 6 owner_stated_seconds owner_reused_identity`: all rc 0 (`receipts/preflight-cost.log`, `preflight-cost-summary.txt`).
- Restore check:
  - HEAD and tree are exact, the index and worktree equal HEAD, and the five changed files' blobs and modes equal HEAD;
  - the six gitlinks are recorded;
  - the probe bytecode in the ignored `scripts/__pycache__` was removed, leaving 0 untracked or ignored entries (`receipts/restore-check.txt`).
- Hosted snapshot: the PR head equals `887fdd53`. When taken, several contexts were COMPLETED SUCCESS, including `changes`, `full-ci-gate`, `docs-check-no-git`, `bdd-conformance` and `elaborate-gates-0`. The Verilator shards and other gates were IN_PROGRESS or QUEUED (`receipts/hosted-snapshot.json`). This is not an acceptance claim.

## Real limits

- No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence beyond the runs above is the author's published receipts, which were spot-checked here (campaign, full test, the round 6 reviewer probes), not re-run in full.
  - Not re-run: the `--matrix`, `make -C tb/verilator/gptp_shadow lifecycle`, `behave` and the docs workflow steps.
- Only the delta was examined in depth. Code the delta does not touch keeps its round 6 lens verdict.
- The mutants were run at moderate host load. The author's load-sensitivity note for two `owner_shell_window` mutants was not reproduced or refuted here; S2 covers it.
- Physical calibration NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Rule on R764-7-F1. The ruling says pin, never narrow, and the feasible pin is one listing. Carry R764-7-R1 and R2 to the residue checklist.
- Decide R764-7-S2 (control binding for `trap-commands-1s` and `shell-window-one-pass`) and R764-6-S1 (new Issue).
- Hosted and local-replica acceptance at the exact head, and the current-dev merge candidate:
  - source base `1f29f189279f9fc0132f4918e47342b87d22f33a`;
  - live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`;
  - builder and native banks at the merge turn.
- Merge needs two independent positive reviews and maintainer authorization.

R764-7 FINISHED
