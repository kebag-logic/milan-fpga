[R763] NEGATIVE - exact head a987b601a0c10049321c18847504c4a94a862e04

# R763-6: internal cleared-context review of PR #834 (issue #833), round 6

Head `a987b601a0c10049321c18847504c4a94a862e04`, tree `04c6b8be6ee7a00584beb057727557b1a895d213`. Delta reviewed: `a67eaf66..a987b601`, six one-line commits, tests and text only (`scripts/test_suite_cancellation.py`, `scripts/process_test_support.py`, `docs/testing/TESTING.md`). `scripts/owned_process.py` is byte-identical to `a67eaf66` (and to `c1b29617`), so the product keeps its prior lens verdicts.

**Verdict: NEGATIVE for one MINOR, R763-6-F1 (Conformance, Tests, Docs).** A committed mutant that `MUTANTS` and `TESTING.md` file as "breaks no row" does break a row of the new table. Every other ruling item is met: the MAJOR R763-5-F3 is fixed at its cause, the five round 5 gaps are pinned with red mutants, and nothing was narrowed. The product is correct in every probe below.

## Scope reconstructed

- Issue #833 acceptance: (1) the failure message prints each descendant's `/proc/<pid>/stat` state; (2) a fixed deadline or a real fix from that evidence. Both were met in earlier rounds, and the product is unchanged since then.
- The manager's round 6 ruling on #833 (issuecomment-6582585294):
  1. R763-5-F3 first.
  2. `TESTING.md` lists every stated cleanup behaviour as a table, each row with its control and the mutants that prove it, plus a "not pinned" list with reasons.
  3. The five gaps are pinned or moved, and the signal through the handle is pinned.
  4. From round 7, a survivor against an unlisted behaviour is residue. A survivor against a listed row is a finding now.
- The author's TAKEN and REVIEW READY comments on #833 (issuecomment-6582669797, issuecomment-6585270926), and the PR body's Round 6 section as fetched at review.

## Focus checks

**(1) R763-5-F3 (MAJOR): RESOLVED at its cause.** `scripts/test_suite_cancellation.py:580-583` sets a 40.5 s reap stage. The verdict is then at 0.4 + 40.5 = 40.9 s of owner clock. Pass 61, where the child is released, is at most 61 x 0.5 = 30.5 s. That leaves the product's 10 s after SIGKILL. The lower bound is unchanged: pass 61 is at least 1.2 s and the resume at least 1.22 s, past grace + 1 s.
- My own probe (`probes/slow_census.py`) slows every census pass at head:
  - unmutated, green at 0.15, 0.3, 0.5 and 0.75 s a pass (14.2, 24.0, 37.0 and 53.0 s): `receipts/step3/slow-none-*.log`, plus `receipts/step2/slow-none-0.75.log`, whose first two lines are the green result (its exit status was misreported by a probe bug, since fixed);
  - at `a67eaf66`, 0.5 s a pass is red: `CLEANUP FAILED ... after 11.40 s, 21 census passes` (`receipts/step3/slow-prevhead-0.5.log`). That is the round 5 defect, reproduced.
- All eight of rows 7 and 8's shell-window mutants stay red with their words at 0.15 and at 0.5 s a pass (`receipts/step3/slow-<mutant>-*.log`): `shell-killed-when-resumed`, `shell-window-1s`, `shell-window-one-pass`, `shell-spared-only-while-stopped`, `no-trap-window`, `no-shell-window-pass`, `trap-commands-1s`, `trap-commands-until-grace`.

**(2) The table, row by row against `owned_process.py:256-339` and the guide's own statements.**
- 16 rows. `probes/table_vs_mutants.py` (`receipts/table-vs-mutants.log`) finds:
  - every name in the table is a `MUTANTS` key;
  - every one of the 70 mutants with a control is named in a row that lists that control;
  - the 4 with no control are in no row.
  - Its single mismatch is `windows-2s`, named in rows 4 and 6. That is correct: it edits both `TRAP_SECONDS` and `REAP_SECONDS`.
- Rows 1-5 and 7-16 match the code:
  - row 1: `_send` at `:240-254`;
  - rows 2-3: the first-pass SIGTERM and the root skip (`:313-318`), grace at `:313`, the leaf-first rules (`:327-330`) and `kill_all` (`:324`);
  - row 4: the verdict (`:289-290`);
  - row 5: the resume condition (`:304`);
  - rows 9 and 10: the clock (`:284`);
  - row 11: `limit + REAP_SECONDS`;
  - row 12: return on an empty census (`:276-277`) and the post-census reap (`:280-281`);
  - row 14: `root_pid in owned` (`:304`);
  - row 15: SIGKILL before the raise (`:297-298`);
  - row 16: `_describe` (`:128-130`).
  - Wording residue on rows 1 and 15 is in X1 and X3.
- **Row 6 is not true of what pins it** (F1).
- The not-pinned list: item 1 (SIGCONT) and item 3 (the extra second) are true as reasons. Item 1 has imprecise wording (X2). **Item 2's reason is false** (F1).

**(3) The five gaps: PINNED, each red with its words** in my run of the committed campaign (`receipts/step2/mutants-head.log`, `owned-process mutants: PASS (74 mutants, 70 with a control that must fail)`, rc 0, 46.8 s at 9 jobs):
- R764-5's `rv-signal-by-number` is `signal-by-number`: red on `owner_reused_identity`, "a census entry was signalled by its number, after it changed hands". `check-before-open` is red with the same words.
  - The control is sound. `opened` and `rechecked` hand the number over exactly at the recheck. The other process blocks SIGTERM, so a by-number signal shows in `SigPnd|ShdPnd` with no timing. `own.wait(timeout=15) == -SIGTERM` proves the handle reached the entry's own process.
  - My extra mutant `rv6-signal-before-recheck` is also red on it (`receipts/step2/rv6-matrix.log`).
- `rv-parent-spared-past-kill-all` (`parent-spared-past-kill-all`) and `parents-killed-at-grace`: red on `owner_stated_seconds`, "a stubborn parent's stated seconds were not kept". This also resolves R763-5-F1.
- `rv-vanishing-waits-30s-more` (`vanishing-waits-30s-more`): red, "a vanishing listing's stated seconds were not kept: [(89, 'verdict')]".
- R763-5-F2: `report-without-current-parent` and `report-age-in-ticks` are red on `owner_report`; my `rv6-report-age-hz100` is red too.
  - The age bounds hold by construction. The child starts after `began` and before `paused`, and `youngest` is measured before `_describe` and `oldest` after it. So the true age lies inside them, and the 0.05 s tolerance covers the 10 ms tick and uptime resolution.

**(4) Flake and load.** Each new or changed control was run 64 times at 16 jobs at head: `owner_report`, `owner_reused_identity`, `owner_late_cancel`, `owner_late_exit`. All were green (`receipts/step4/stress-*.log`). The whole test at head was rc 0, `suite cancellation: PASS`, 61.5 s (`receipts/step1/preflight-head.log`).

**(5) Preflight cost: CONFIRMED, about +0.1 s measured against the author's "about +0.2 s".** Each control ran 6 times at head and at `a67eaf66` (`receipts/step5/cost.log`):
- `owner_report`: median 0.31 s against 0.21 s.
- Every other control is within 0.03 s, `owner_reused_identity` included at 0.16 s.
- `owner_shell_window`: 4.57 s at head against a 6.21 s median at `a67eaf66` (load noise).
- The whole test ran 61.52 s at both heads, run side by side.

**(6) Nothing narrowed: CONFIRMED, with one wording residue (X4).**
- Every removed sentence of `TESTING.md:214-236` and `:266-285` at `a67eaf66` maps to a row.
- Row 6 *widens* "A shell resumed late has ten seconds of its own" to any resume. That is the origin of F1.
- The general "The run fails in the first census pass at or past the deadline" now survives only in row 4.

**R763-5-S1 (SUGGESTION): TAKEN and verified.** Under a launcher that ignores SIGHUP (`probes/hup_ignored.py`), `--mutants none --matrix` behaves as follows (`receipts/step6/hupign-*.log`):
- at head, rc 0, with `none / whole` green;
- at `a67eaf66`, rc 1, `none / whole` red with a hard-HUP `TimeoutExpired`.

**Comment rule.** The added comments and docstrings carry no lane label, lane name, review round, reviewer ID or comment ID: a grep of the delta's added lines found none. All six commit subjects are one line with an empty body. No new RESIDUE.

## Findings

**R763-6-F1 - MINOR - Conformance, Tests, Docs - `docs/testing/TESTING.md:267` (row 6), `:269` (row 8), `:282` (not-pinned item 2); `scripts/process_test_support.py:429-432` (`MUTANTS["sigterm-to-new"]`, control `None`); PR body, Round 6, "Not pinned by a control" item 2**
- **Authority.**
  - Ruling item 4: "A mutant that survives against a row of the table stays a finding."
  - Ruling item 2: a behaviour with no control is moved to the not-pinned list "with the reason".
  - `TESTING.md:285`: "A stated cleanup behaviour is a row of this table".
  - Row 6: "From the resume the shell has ten seconds of its own to finish its terminal trap, and so does any command that trap starts."
- **Evidence.**
  - The committed mutant `sigterm-to-new` removes the "new since the first census" skip during grace (`owned_process.py:319-323`). It is filed as "breaks no row". Its reason (`TESTING.md:282`, and the PR body) is: "it is killed at grace either way".
  - That reason is false for a command the **resumed shell's** trap starts. Such a command is new, and past grace it keeps the shell's window (`:331-333`), so it is *not* killed at grace. If the shell is resumed while the clock is still inside grace, the mutant SIGTERMs that command in the next pass.
  - This is the ordinary sweep case: every other descendant exits on its first-pass SIGTERM, and the EXIT trap's `rm` runs at once.
  - `probes/grace_resume_probe.py` reproduces it at production stages. The shell's only child exits on SIGTERM, so the resume comes within about 0.1 s of cleanup's first signal, and the trap runs `sleep 1.0 && echo ran` (`receipts/step1/grace-resume-*.log`):
    - head (`none`): PASS 3 of 3, "trap command finished";
    - `sigterm-to-new`: FAIL 3 of 3, "trap command did not finish inside the shell's window", with a SIGTERM to the trap's `sleep` at 0.08 s;
    - my narrower `rv6-sigterm-trap-commands` (SIGTERM only to a resumed shell's new commands): FAIL 3 of 3.
  - Both are green on all 10 owner controls and the whole test: my matrix (`receipts/step2/rv6-matrix.log`, "red on 0 of 11"), and the author's own published round 6 matrix too.
  - The reason: `owner_shell_window` releases its child only from pass 61 (≥ 1.2 s, past its 0.2 s grace), and `owner_stated_seconds` resumes at pass 12 (5.5 s). So no control resumes the shell inside grace.
- **Impact.**
  - A regression that SIGTERMs the trap's cleanup commands during grace would pass the preflight and the `--mutants` campaign, and kill the sweep's EXIT-trap `rm` in the common case.
  - Meanwhile row 6 states the behaviour as pinned, and the not-pinned list gives a false reason for leaving it unpinned.
  - The row is wider than the guide's earlier "A shell resumed late", and wider than what its controls exercise.
- **Required outcome.** One of these:
  - (a) A control in which the cancelled shell is resumed while the owner's clock is still inside grace, and in which a command its trap starts is neither sent SIGTERM nor killed inside the shell's window. `sigterm-to-new`, or a narrower mutant limited to the resumed shell's commands, then names that control with its words, and is named in row 6 or 8. The not-pinned item 2 and its `MUTANTS` reason are reworded to what stays unpinned, if anything, for example new descendants of a shell that is not resumed. A starved-clock listing does this in milliseconds: resume in pass 2 at 0.5 s, then the trap's command listed from pass 3, then assert no `SIGTERM` to it.
  - (b) Row 6 is narrowed to a resume past grace, and the not-pinned item states the in-grace case with a true reason.

  The ruling prefers pinning. Either way, correct the PR body's not-pinned item 2.
- **Verification.**
  - `python3 -I probes/grace_resume_probe.py <tree>/scripts 3` stays PASS at the new head.
  - `sigterm-to-new` (and `rv6-sigterm-trap-commands`, `probes/mktree.py`) are red on a named owner control.
  - `--mutants` PASS, and `none` green on all 11.

**R763-6-X1 - RESIDUE - Docs - `docs/testing/TESTING.md:262` (row 1)**
- "a handle opened on the census entry, after its start time is rechecked" reads as *open after recheck*. That is the order of the row's own mutant `check-before-open`, while the code opens first (`owned_process.py:243`) and rechecks second (`:247-249`).
- "Every signal" also covers the shell's cancel signals and its resume (`:193-194`, `:310`). Those go through the handle opened at launch (`:360`), not one opened on a census entry.
- Exact fix: "Every signal to a census entry goes through a handle opened on that entry before its start time is rechecked, and is sent only if the recheck holds; the shell is signalled through the handle opened at its launch. So a census entry whose number now names another process is never signalled, even when the number changes hands right after that recheck."

**R763-6-X2 - RESIDUE - Docs - `docs/testing/TESTING.md:281`; PR body Round 6 not-pinned item 1**
- "`SIGKILL` ends it at grace without one": a stopped first-census parent is SIGKILLed at grace + 1 s or by 4 s, not at grace (`:327-330`).
- Exact fix: "`SIGKILL` ends it by 4 s without one." In the PR body: "`SIGKILL` ends a stopped descendant by 4 s either way."

**R763-6-X3 - RESIDUE - Docs - `docs/testing/TESTING.md:276` (row 15)**
- "sends `SIGKILL` to every descendant it reports": when every listed process was collected in that pass, the report lists them (`owned_process.py:294`, `owned or census`) but SIGKILLs none (`:297`, `owned` only). They are already gone, so this is wording only.
- Exact fix: "A run that fails first sends `SIGKILL` to every descendant it reports as remaining, so it takes the stopped shell with it."

**R763-6-X4 - RESIDUE - Docs - `docs/testing/TESTING.md:258`**
- At `a67eaf66`, "The run fails in the first census pass at or past the deadline" applied to every deadline. It now appears only in row 4 (14 s), not in rows 6 (20 s after a resume) or 11 (24 s). The behaviour is still pinned pass by pass (passes 52 and 49).
- Exact fix: "Times are cleanup's, on the owner's clock, and each deadline fails the run in the first census pass at or past it."

**R763-6-S1 - SUGGESTION - Tests, Docs - `docs/testing/TESTING.md:273` (row 12)**
- My mutant `rv6-return-before-confirm` returns when every entry of a census was collected in its own pass, with no census after the collection. That breaks row 12's "returns only once a census taken after a collection lists nothing".
- It is red on `owner_vanishing`, `owner_late_cancel`, `owner_stated_seconds` and the whole test, but not on `owner_late_exit`, the row's only listed control (`receipts/step2/rv6-matrix.log`).
- Optional: add it to `MUTANTS` with one of those controls, and list that control in the row.

**Not findings.** My other reviewer mutants are each red on a control and the whole test (`receipts/step2/rv6-matrix.log`), so the rows they break are pinned:
- `rv6-sigterm-cancelled-shell`;
- `rv6-signal-before-recheck`;
- `rv6-trap-9.5s`;
- `rv6-pass-cap-0.6s`;
- `rv6-report-age-hz100`.

`no-sigcont-after-send` and `no-leaf-first` are green on all 11, and their not-pinned reasons hold.

## Prior findings at their cause, at this head

| Finding | Status | Evidence |
|---|---|---|
| R763-5-F3 (MAJOR) | RESOLVED at cause | Check (1): green at 0.15-0.75 s a pass; `a67eaf66` red at 0.5 s; eight window mutants red at 0.15 and 0.5 s |
| R763-5-F1 (MINOR, second stage) | RESOLVED | `parent-spared-past-kill-all`, `parents-killed-at-grace`, `kill-all-a-pass-late` red on `owner_stated_seconds`; parent SIGKILL in pass 9 |
| R763-5-F2 (MINOR, report parent and age) | RESOLVED | `report-without-current-parent`, `report-age-in-ticks`, `report-parent-is-first-parent`, and my `rv6-report-age-hz100` red on `owner_report`; 64/64 green unmutated |
| R764-5-F1 (MINOR, three survivors) | RESOLVED | `signal-by-number`, `parent-spared-past-kill-all`, `vanishing-waits-30s-more` red with words (check 3) |
| R764-5-R1 (RESIDUE) | TAKEN, exact fix | `test_suite_cancellation.py:799`: "It is never really signalled: this control's send only records the signal." |
| R764-5-S1 (SUGGESTION) | TAKEN, but its reason for `sigterm-to-new` is wrong | That is F1 |
| R763-5-S1 (SUGGESTION) | TAKEN, verified | `receipts/step6` |
| R763-4-X1 (RESIDUE) | TAKEN | Row 3: "except a cancelled shell and any command its trap started, which keep the shell's own window" |
| R763-2-S2, R763-2-S3 (manager actions; census-cost comment) | Retained, optional | `owned_process.py` unchanged |
| Rounds 1-4 findings and residue | Resolved earlier; the delta does not touch what they depend on | Their mutants are all in `MUTANTS` and red in my campaign run |

## Lens results

```text
[R763] PASS RTL — git diff --stat 1f29f189..a987b601 (5 Python/Markdown files), receipts/clone-integrity.txt (gitlinks external efeb541a, gptp-processor 135afd04, protocol-processor a9e84b66, lwSRP 08ee86e8, tsn-c-stack 70936b77, verilog-axis 48ff7a7e) — no HDL, constraint, synthesis or submodule change; the cleanup state machine owned_process.py:256-339 is byte-identical to a67eaf66
[R763] PASS Robustness — scripts/owned_process.py:256-339 under receipts/step3/slow-*.log, receipts/step1/grace-resume-none.log, receipts/step4/stress-*.log, receipts/step6/hupign-head.log — the product spares a trap command when resumed in grace (3/3); the shell-window control holds at 0.15-0.75 s a pass; the new controls are green 64/64 at 16 jobs; the campaign survives an ignored SIGHUP
[R763] MINOR Conformance — ruling items 2 and 4 vs docs/testing/TESTING.md:267,282 — R763-6-F1; issue acceptance (1)(2) met with the product unchanged; every other ruling item met (checks 1-6)
[R763] MINOR Tests — scripts/test_suite_cancellation.py:564-618,784-890; scripts/process_test_support.py:262-575; receipts/step2/mutants-head.log, rv6-matrix.log — R763-6-F1; everything else in the delta checked red/green as claimed
[R763] MINOR Docs — docs/testing/TESTING.md:212-291; PR body Round 6 section — R763-6-F1; RESIDUE X1-X4; SUGGESTION S1
```

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | Issue #833 acceptance; round 6 ruling; `TESTING.md:255-291` against `owned_process.py:240-339` | R763-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| RTL | CLEAN | diff stat `1f29f189..a987b601`; `receipts/clone-integrity.txt` | R763-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| Robustness | CLEAN | `owned_process.py:256-339` (unchanged); `receipts/step1/grace-resume-none.log`, `step3/`, `step4/`, `step6/` | R763-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| Tests | UNCLEAN (F1 open) | `test_suite_cancellation.py` delta; `process_test_support.py:262-575`; `receipts/step2/`, `step3/`, `step4/`, `table-vs-mutants.log` | R763-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| Docs | UNCLEAN (F1 open; X1-X4 residue) | `TESTING.md:212-291`; PR body Round 6 section; delta comments | R763-6 | `a987b601a0c10049321c18847504c4a94a862e04` |

## Real limits

- I did not run these at this head: the docs.yml steps, builder legs, `make -C tb/verilator/gptp_shadow lifecycle`, `behave`, the full `--matrix`, or the full sweep. Source-head execution evidence for those is the author's published gate receipts. I spot-checked the author's matrix receipts (`review-evidence/833-r1/author-r6/receipts/final/matrix-{1,2,3}.rc` = 0; its `sigterm-to-new` rows are green on all 11, matching mine).
- No manager source bank ran at this head, and none is claimed. Physical calibration: NOT RUN. Field skips are not hardware proof.
- Hosted contexts at this head were in progress at review: `receipts/hosted-checks-snapshot.txt`. Completed jobs were success, `Physical gPTP` was skipped, and Verilator shards were queued or in progress. The manager owns hosted and act acceptance.
- The cost comparison ran on a shared host at load 14-35, so the timings are relative.
- The probes run on Python 3.14.8, outside PID or user namespaces. Each mutant run is a new session from a disposable tree under `scratch/`.
- The `receipts/step1/grace-resume-*.log` files are from the corrected probe. Its first version mishandled the expected cancel, and its output was overwritten.
- The clone is untouched: HEAD, index, worktree and gitlinks are verified in `receipts/clone-integrity.txt`.

## Pending manager duties

- Carry R763-6-F1 to the author. Conformance, Tests and Docs re-cover at the corrected head.
- Residue checklist: R763-6-X1 to X4, with the exact fixes above.
- Optional: R763-6-S1, R763-2-S2 and R763-2-S3.
- At the merge turn, the current-dev candidate (source base `1f29f189279f9fc0132f4918e47342b87d22f33a`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`): builder and native banks, plus hosted and act acceptance.

R763-6 FINISHED
