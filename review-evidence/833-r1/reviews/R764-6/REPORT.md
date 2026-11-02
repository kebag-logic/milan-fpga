[R764] NEGATIVE - exact head a987b601a0c10049321c18847504c4a94a862e04

Round R764-6. External independent review of issue #833 / PR #834.

- Head `a987b601a0c10049321c18847504c4a94a862e04`, tree `04c6b8be6ee7a00584beb057727557b1a895d213`.
- Source base `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- The reviewed delta is round 6, `a67eaf66..a987b601`. It is six one-line commits with empty bodies and no trailers (`receipts/round6-commits.txt`). They touch `docs/testing/TESTING.md`, `scripts/process_test_support.py` and `scripts/test_suite_cancellation.py`.
- `scripts/owned_process.py` is byte-identical to `a67eaf66` (`git diff --quiet` rc 0).

## Summary

- **The round answers the ruling's MAJOR at its cause.** R763-5-F3 is resolved. With every census pass of the control's owner slowed to 0.15, 0.3 or 0.5 s, unmutated `owner_shell_window` is green 12 of 12. Each of its 13 listed mutants is red at each of those pass times, with its own words (`receipts/slow-shell-window.log`).
- **The other prior findings are resolved:** R763-5-F1, R763-5-F2, R764-5-F1 as published, R764-5-R1, R764-5-S1 and R763-4-X1. R763-5-S1 is taken for the campaign path.
- **The table is consistent with `MUTANTS`.** It has 16 rows. Every mutant it names exists, names a control the row lists, and matches the product once. Every `MUTANTS` entry with a control is named in some row (`receipts/table-vs-mutants.log`). The committed campaign is PASS: 74 mutants, 70 red on their control (`receipts/mutants-all.log`).
- **The verdict is NEGATIVE for two new MINOR findings.** Both are reviewer mutants that survive against a listed row. That is a verdict finding under the round 6 ruling. The product is correct on both points. The gap is in the controls.
  - **F1, row 1 (`TESTING.md:262`, "Every signal goes through a handle").** The row is pinned for `SIGTERM` only. A `_send` that sends `SIGKILL` by number, or `SIGCONT` by number, survives every owner control and the whole test. `SIGKILL` by number is the most harmful form of the PID-reuse race that ruling item 3 says must be pinned.
  - **F2, row 5 (`TESTING.md:266`, "resumed in the first pass in which none does").** No control resumes a shell before grace or in pass 1. A resume held back to grace, or to pass 2, survives every owner control and the whole test.
- **Three wording RESIDUE items and two SUGGESTIONs** follow below.

## Findings

**R764-6-F1 - MINOR - Conformance, Tests, Docs - `scripts/test_suite_cancellation.py:833-885` (`BLOCKING`, `owner_reused_identity`) vs `docs/testing/TESTING.md:262` (table row 1); `scripts/owned_process.py:240-254` (`_send`)**

- **Authority and evidence.**
  - Ruling item 3 on #833 says the signal-through-the-handle behaviour "must be pinned: it closes the PID-reuse race".
  - Row 1 states: "Every signal goes through a handle opened on the census entry, after its start time is rechecked. So a census entry whose number now names another process is never signalled, even when the number changes hands right after that recheck."
  - The round 6 rule: a mutant that survives against a row of the table is a finding.
  - `_send` sends two signals through the handle: `signum` (`SIGTERM` or `SIGKILL`) and then `SIGCONT` (`owned_process.py:250-251`).
  - The new handover check in `owner_reused_identity` sends only `SIGTERM` (`:873`). It detects a by-number signal only through `SIGTERM`'s pending bit (`:877`), because `BLOCKING` blocks only `SIGTERM` (`:835`).
- **Reviewer mutants.** These are in `scripts/row_mutants.py`, applied to a copy of `scripts/` by the repository's own `mutant_tree`.
  - `rv6-sigkill-by-number`: `SIGKILL` goes by `os.kill(pid, ...)`, everything else through the handle. It is green on all 10 owner controls (`receipts/row-mutants.log`) and on the whole test, rc 0 in 61.3 s (`receipts/row-mutants-whole.log`).
  - `rv6-sigcont-by-number`: the trailing `SIGCONT` goes by number. It is green on all 10 and on the whole test.
  - Control: `rv6-sigterm-by-number` is red on `owner_reused_identity` with "a census entry was signalled by its number, after it changed hands". So the check works, but only for that one signal.
- **Impact.**
  - A regression that sends `SIGKILL` by number would pass the preflight and the committed campaign. It kills whatever process holds that number after the recheck: the exact race row 1 and ruling item 3 say is closed and pinned.
  - A by-number `SIGCONT` resumes a foreign stopped process.
  - Row 1 says "Every signal", and the table says the row is pinned by `owner_reused_identity`.
- **Required outcome.** Either of these:
  - `owner_reused_identity` (or another control) is red when any signal `_send` sends goes by number after the handover. The SIGKILL-only and SIGCONT-only variants then join `MUTANTS` with that control's words and are named in row 1.
  - Or row 1 is narrowed to what is pinned. This would contradict ruling item 3 for `SIGKILL`, so it needs the manager.
  - Shape is not prescribed. Feasibility: a `SIGCONT` sent by number to a process that blocks it stays pending in `/proc/<pid>/status` (`receipts/sigcont-pending.log`, `scripts/sigcont_pending.py`). A `SIGKILL` handover shows as the other process dying.
- **Verification.**
  - `python3 -B scripts/row_mutants.py <clone> 8 rv6-sigkill-by-number rv6-sigcont-by-number` (from this packet) shows each red on at least one owner control.
  - `--mutants` stays PASS with both added, and `none` stays green.

**R764-6-F2 - MINOR - Conformance, Tests, Docs - `scripts/test_suite_cancellation.py:784-830` (`owner_stated_seconds`; resume expectation `:823`) vs `docs/testing/TESTING.md:266` (table row 5); `scripts/owned_process.py:304`**

- **Authority and evidence.**
  - Row 5 states: "A cancelled shell stays stopped while any other descendant lives, and is resumed in the first pass in which none does." It is pinned by `owner_stated_seconds` and proved by `resume-with-one-live` and `resume-only-when-alone`.
  - Ruling item 2 says each row carries "the control that pins it and the mutant that proves it". The round 6 rule makes a surviving mutant against a row a finding.
  - Every control resume happens late. In `owner_stated_seconds` the first pass with no other live descendant is pass 12 (5.5 s, past grace). In `owner_shell_window` it is pass 62 or later. No control has a shell whose first such pass is pass 1, or any pass before grace.
- **Reviewer mutants** (`scripts/row_mutants.py`):
  - `rv6-resume-not-before-grace`: `... and not (live - {root_pid}) and clock >= deadline:`. A cancelled shell with nothing else live stays stopped until 2 s.
  - `rv6-resume-not-first-pass`: `... and passes > 1:`.
  - Both are green on all 10 owner controls and on the whole test, rc 0 in 65.1 s and 61.4 s (`receipts/row-mutants.log`, `receipts/row-mutants-whole.log`).
- **Impact.**
  - A cancellation that arrives while the shell has no other live descendant is the sweep's transition and between-command case. Under `rv6-resume-not-before-grace` it holds the stopped shell for 2 s of owner clock before its terminal trap may run.
  - Row 5 says the resume comes in the first pass in which no other descendant lives, and the table says a control pins that. The control only pins it for a resume at 5.5 s.
- **Required outcome.** Either of these:
  - A control has a shell whose first pass with nothing else live is pass 1, and is red unless the resume (`SIGCONT`) is in that pass. Both mutants then join `MUTANTS` with its words and are named in row 5.
  - Or row 5 is narrowed to what is pinned.
  - One more listing in `owner_stated_seconds`, with only the notified shell listed, would likely do it at negligible cost. This is not prescribed.
- **Verification.**
  - `python3 -B scripts/row_mutants.py <clone> 8 rv6-resume-not-before-grace rv6-resume-not-first-pass` shows each red on at least one owner control.
  - `--mutants` stays PASS with both added.

**R764-6-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:262` (row 1 wording)**

- "a handle opened on the census entry, after its start time is rechecked" can be read as "opened after the recheck". That is the order of the `check-before-open` mutant, not the product, which opens first and then rechecks (`owned_process.py:243-249`).
- "Every signal" also takes in the cancellation `SIGSTOP`/signal and the resume `SIGCONT`. Those go to the shell through the handle opened at spawn (`:193-194`, `:310`), not through one opened on a census entry.
- **Exact fix:** "Every signal to a census entry goes through a handle opened on that entry before its start time is rechecked, and is sent only if the recheck holds. So a census entry whose number now names another process is never signalled, even when the number changes hands right after that recheck."
- If F1 is answered by narrowing row 1, merge this into that change.

**R764-6-R2 - RESIDUE - Docs - `docs/testing/TESTING.md:273` (row 12) and `:276` (row 15) vs `:272` (row 11)**

- Row 12 says cleanup "never reports a collected one as remaining".
- Row 11's failure does exactly that. A listing that dies inside every census is collected in each pass, and the verdict reports `sorted(owned or census)` (`owned_process.py:294`), so it names the collected entries. `owner_vanishing` asserts "exited during this report" in that message (`test_suite_cancellation.py:692`).
- For the same reason, row 15's "every descendant it reports" includes entries it cannot and does not signal.
- The behaviour is intended and pinned. Only the rows' wording conflicts.
- **Exact fix:**
  - Row 12, append: "A listing that dies inside every census is the one exception: its failure names each entry as exited."
  - Row 15, replace "to every descendant it reports" with "to every descendant it reports that it has not collected".

**R764-6-R3 - RESIDUE - Docs - `docs/testing/TESTING.md:271` (row 10)**

- Row 10 lists `owner_shell_window` among the controls that pin it.
- Neither mutant the row names (`clock-always-cap`, `first-pass-full-cap`) names that control in `MUTANTS`. `:255-256` says each mutant "fails that control".
- R764-5 published `clock-always-cap` red on `owner_shell_window`, so the claim is probably true. The table just does not show it.
- **Exact fix:** either drop `owner_shell_window` from row 10's "Pinned by" cell, or add a row-10 mutant whose `MUTANTS` entry names `owner_shell_window`.
- This changes no test, so it is wording only.

**R764-6-S1 - SUGGESTION - Tests, Robustness - `scripts/test_suite_cancellation.py:903-950` (`main`), `:303` (`hard_stop`)**

- R763-5-S1 is taken for the campaign path only (`process_test_support.py:561-574`).
- The direct preflight command `python3 scripts/test_suite_cancellation.py`, started under a launcher that ignores SIGHUP, still fails `hard-HUP`. The driver inherits the ignored disposition, so `TimeoutExpired` comes after 60 s, rc 1 (`receipts/full-test.log`, run under such a launcher).
- The same head with SIGHUP at its default passes, rc 0 (`receipts/full-test-rerun.log`).
- The HUP stops are on base `1f29f189` too, so this predates the PR and is out of this Issue's scope.
- Optional: the same reset in `main()`, or a clear refusal when SIGHUP is ignored; or a new Issue.

**R764-6-S2 - SUGGESTION - Tests - `docs/testing/TESTING.md:262,266`**

- The two F-findings are both in rows whose one control covers only part of the row's domain: one signal, and one resume time.
- When the table is next touched, a short per-row "domain the control covers" note would make the next survivor of this kind visible before a reviewer runs it.
- Optional.

## Manager round 6 ruling, item by item

1. **R763-5-F3, shell-window control under slow census: RESOLVED at cause.**
   - `test_suite_cancellation.py:580-583` gives `REAP_SECONDS=40.5`. The verdict is at 0.2 + 0.2 + 40.5 = 40.9 s of owner clock. Pass 61 is at most 0.5 x 60 = 30 s, since the first pass adds nearly nothing (`owned_process.py:260,284`).
   - The lower bound is unchanged. Each pass adds at least its 0.02 s pause, so pass 61 is at 1.2 s or later, and the resume comes after it.
   - My own probe, `scripts/slow_shell_window.py`, puts a sleep inside the control owner's census, so the pass itself is long. Results (`receipts/slow-shell-window.log`, campaign PASS, rc 0):
     - Unmutated: green 4 of 4 at each of 0.15, 0.3 and 0.5 s per pass. At 0.5 s that is 67 passes in about 36 s.
     - All 13 `MUTANTS` entries whose control is `owner_shell_window` are red at each of the three pass times, each with its listed words. These include `shell-window-one-pass`, `shell-window-1s`, `shell-killed-when-resumed`, `no-trap-window` and all `trap-commands-*`.
   - Unmutated `owner_shell_window` is green 24 of 24 at 16 jobs (`receipts/repeat-controls.log`).
2. **One table of every stated cleanup behaviour: present, with two rows not fully pinned.**
   - `TESTING.md:255-290` has 16 rows and a three-item "Not pinned by a control" list.
   - Row by row against `owned_process.py:240-334`, every row states what the product does, except the wording in R1 and R2.
   - Every row's mutants exist and target a control the row lists (`receipts/table-vs-mutants.log`, rc 0).
   - The not-pinned list holds product-comment-only behaviours. Their mutants (`no-sigcont-after-send`, `sigterm-to-new`, `no-leaf-first`) are in `MUTANTS` with no control and a reason.
   - Results of my ten row mutants are in `receipts/row-mutants.log`. Six are red on the row's control: SIGTERM by number, shell SIGTERMed, leaves-only SIGTERM, `KILL_ALL_SECONDS` 1.5, `TRAP_SECONDS` 9, and a vanishing wait of 5 s. Four survive: F1 (row 1) and F2 (row 5).
3. **The five open gaps are pinned as published.**
   - `signal-by-number` (R764-5's mutant, SIGTERM and SIGCONT both by number) is red on `owner_reused_identity` in the committed campaign. The SIGKILL-only and SIGCONT-only variants are not (F1).
   - `parent-spared-past-kill-all`, `parents-killed-at-grace` and `kill-all-a-pass-late` are red: the stubborn parent is expected at pass 9, 4.0 s (`:819-821`).
   - `vanishing-waits-30s-more` and `vanishing-waits-from-grace` are red: the vanishing verdict is expected at pass 49, 24 s (`:822`).
   - `report-without-current-parent`, `report-age-in-ticks` and `report-parent-is-first-parent` are red on `owner_report`.
   - All are in `receipts/mutants-all.log`, each with its words.
4. **R763-5-F1 and R763-5-F2: RESOLVED.** See the prior-findings table. My `rv6-kill-all-1.5s` is also red on the stubborn-parent expectation.
5. **Preflight cost.** Interleaved, 8 runs each, under host load 19 to 69 (`receipts/preflight-cost.log`):
   - `owner_report`: +0.10 s;
   - `owner_reused_identity`: +0.017 s;
   - `owner_late_exit`: +0.011 s;
   - `owner_stated_seconds`: +0.005 s.
   - That is about +0.13 s in total, consistent with the author's "about +0.2 s". The author's published `final/cost.txt` shows +0.10 and +0.05 s, and the whole test at 61.2 s against 60.8 s.
6. **Nothing narrowed.** Every statement of the removed prose (`a67eaf66:TESTING.md:217-235,269-285`) maps to a row:
   - stable handles: row 1;
   - grace and `SIGKILL` at 4 s: rows 2-3;
   - 14 s: row 4;
   - the resume window and 20 s: row 6;
   - pass cap and wall time: rows 9-10;
   - vanishing 10 s: row 11;
   - collection: row 12;
   - re-parenting: row 13;
   - late cancel: row 14;
   - kill before fail: row 15;
   - the message: row 16.
   - Row 3 now also states the trap commands' exception (R763-4-X1) and the parent sparing. The not-pinned list moved out no statement that `TESTING.md` previously made.

**Comment rule.** No new RESIDUE. The delta's added lines carry `#833` only, with no lane label, lane name, review round, reviewer ID or comment ID. "the next reviewer's mutant" (`TESTING.md:286`) names a role and was already present. All six commit subjects are one line with empty bodies. `git diff --check 1f29f189 HEAD` is silent.

## Prior findings at this head

| Finding | Severity | Status at a987b601 | Evidence |
|---|---|---|---|
| R763-5-F3 (shell-window control red by chance on a slow owner) | MAJOR | **RESOLVED at cause** | Ruling item 1 above; `receipts/slow-shell-window.log`, `receipts/repeat-controls.log` |
| R763-5-F1 (second stage, parent of a live child at 4 s) | MINOR | **RESOLVED** | `:819-821` expects pass 9; both mutants red (`receipts/mutants-all.log`); row 3 names them |
| R763-5-F2 (report's current parent and age by presence only) | MINOR | **RESOLVED** | `:451-459` assert the current parent as its own field and an age between the measured bounds; three mutants red; unmutated 64 of 64 green at 16 jobs |
| R764-5-F1 (three survivors: vanishing 10 s, parent past kill-all, signal by number) | MINOR | **RESOLVED as specified**: all three published mutants red with words. The underlying row-1 cause is only partly closed: see new R764-6-F1 | `receipts/mutants-all.log`; `receipts/row-mutants.log` |
| R764-5-R1 (stated-seconds child "never signalled") | RESIDUE | **TAKEN, exact fix** | `test_suite_cancellation.py:799` |
| R764-5-S1 (three comment-only behaviours) | SUGGESTION | **TAKEN** | `MUTANTS` no-control entries with reasons; `TESTING.md:281-283` |
| R763-5-S1 (campaign inherits ignored SIGHUP) | SUGGESTION | **TAKEN for the campaign**; the direct command is retained as R764-6-S1 | `process_test_support.py:561-574`; `receipts/full-test.log` vs `full-test-rerun.log` |
| R763-4-X1 (trap commands missing from the second-stage exception) | RESIDUE | **TAKEN** | Row 3, `TESTING.md:264` |
| Earlier rounds' findings | various | Resolved earlier. The delta does not touch what they depend on | `owned_process.py` byte-identical; every earlier mutant red on its control in `receipts/mutants-all.log` |

## Lens results

[R764] MINOR Conformance - docs/testing/TESTING.md:262,266 vs the round 6 ruling (items 2-3) and scripts/owned_process.py:240-334 - R764-6-F1, R764-6-F2. The product does what every row states. #833 acceptance 1-2 is unchanged because the product is unchanged. Ruling item 1 (R763-5-F3) is met: receipts/slow-shell-window.log

[R764] PASS RTL - receipts/restore-check.txt (changed files base..head: 4 Python files and 1 Markdown file; 6 gitlinks identical to 1f29f189) - no HDL, constraint, synthesis or submodule change in the PR or the round; the cleanup state machine is unchanged

[R764] PASS Robustness - scripts/test_suite_cancellation.py:435-470,502-525,564-619,696-740,784-885; receipts/repeat-controls.log (owner_report 64/64, owner_reused_identity 64/64, owner_shell_window 24/24 at 16 jobs), receipts/slow-shell-window.log (12/12 at 0.15-0.5 s passes), receipts/full-test-rerun.log rc 0 - the changed controls are deterministic under load. The patched `os.pidfd_open`, `_identity` and SIGHUP handler are restored in `finally`. The product is unchanged. SUGGESTION R764-6-S1 is pre-existing

[R764] MINOR Tests - scripts/test_suite_cancellation.py:784-885, scripts/process_test_support.py:261-509 - R764-6-F1, R764-6-F2 (four reviewer mutants green on all 10 owner controls and the whole test: receipts/row-mutants.log, receipts/row-mutants-whole.log). Everything else in the delta checks green: receipts/mutants-all.log (PASS, 74/70), receipts/table-vs-mutants.log

[R764] MINOR Docs - docs/testing/TESTING.md:255-290 - R764-6-F1 and R764-6-F2 (rows 1 and 5 claim a pin wider than their control). RESIDUE R764-6-R1, R2, R3 (wording only). No other mismatch between the table and the code or the MUTANTS list

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R764-6-F1, F2 open) | `owned_process.py:240-334` vs `TESTING.md:255-290`; manager round 6 ruling items 1-4; #833 acceptance; `receipts/slow-shell-window.log`, `row-mutants.log` | R764-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| RTL | CLEAN | `receipts/restore-check.txt` (changed files, gitlinks) | R764-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| Robustness | CLEAN | `test_suite_cancellation.py:435-470,502-525,564-619,696-740,784-885`; `receipts/repeat-controls.log`, `slow-shell-window.log`, `full-test-rerun.log`, `preflight-cost.log` | R764-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| Tests | UNCLEAN (R764-6-F1, F2 open) | `test_suite_cancellation.py:435-885`; `process_test_support.py:261-592`; `receipts/mutants-all.log`, `table-vs-mutants.log`, `row-mutants.log`, `row-mutants-whole.log`, `slow-shell-window.log` | R764-6 | `a987b601a0c10049321c18847504c4a94a862e04` |
| Docs | UNCLEAN (R764-6-F1, F2 open; RESIDUE R1-R3) | `TESTING.md:205-300`; delta comments and docstrings; commit subjects | R764-6 | `a987b601a0c10049321c18847504c4a94a862e04` |

## Executed

Each run has its own log and rc under `receipts/`. The clone was restored and verified afterwards: worktree, index and tree identical to HEAD, and gitlinks equal to base (`receipts/restore-check.txt`).

- `python3 scripts/test_suite_cancellation.py`, run twice:
  - under a launcher that ignores SIGHUP: rc 1, `hard-HUP` timeout, see S1 (`full-test.log`);
  - with SIGHUP at its default: rc 0 (`full-test-rerun.log`).
- `python3 scripts/test_suite_cancellation.py --mutants --jobs 8`: PASS, rc 0, 56.7 s (`mutants-all.log`). It ran under the SIGHUP-ignoring launcher, which exercises the new reset path.
- `scripts/table_vs_mutants.py`: rc 0 (`table-vs-mutants.log`).
- `scripts/row_mutants.py`: 10 reviewer mutants x 10 owner controls, 6 jobs (`row-mutants.log`). With `RV6_WHOLE=1`, the 4 survivors against the whole test (`row-mutants-whole.log`).
- `scripts/slow_shell_window.py campaign`: 51 runs, 8 jobs, PASS (`slow-shell-window.log`).
- `scripts/preflight_cost.sh`: interleaved timing of `a67eaf66` and head (`preflight-cost.log`).
- `scripts/repeat_controls.sh`: 152 unmutated runs at 16 jobs, all rc 0 (`repeat-controls.log`).
- `scripts/sigcont_pending.py`: rc 0 (`sigcont-pending.log`).
- Hosted check-runs at the exact head, snapshot at 2026-11-02T18:58Z: 16 completed success, 1 skipped (Physical gPTP), 32 queued or in progress (`hosted-snapshot.txt`). These are not a verdict.
- Spot-check of the author's published round 6 receipts at evidence commit `6415c475`: `final/cost.txt`, `final/slow-0.5.log` (rc 0, 36.6 s), `final/matrix-table.md` (none ok on all 11). They agree with my own runs.

## Real limits

- I did not rerun the 825-run `--matrix`. I spot-checked the author's published matrix table and ran my own mutants against every owner control and, for the survivors, the whole test.
- I did not run the `docs.yml` steps, `behave`, or `make -C tb/verilator/gptp_shadow lifecycle`. Round 6 does not touch `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` or the product. Those rely on the author's published gate receipts, which I did not re-execute.
- Host load was 19 to 69 on 16 CPUs while I ran, from other tenants. All unmutated runs still passed.
- There is no manager source bank at this head, and none is claimed or inferred. Physical calibration was NOT RUN. Field skips are not hardware proof.
- Hosted gates were mostly still running at my snapshot. The manager owns hosted and act acceptance.

## Pending manager duties

- Publish this report. Carry RESIDUE R764-6-R1, R2 and R3 to the residue checklist.
- Decide on F1's narrowing option, since it would touch ruling item 3, if the lane proposes it.
- Apply the PR body's Round 6 section.
- Hosted exact-head acceptance (`rtl-fast`, `verilator-suites`, `yosys-portability`) and the act replica.
- Current-dev merge-candidate validation at the merge turn (source base `1f29f189`, live dev `e61a4afa`), with builder and native banks, and its receipts linked on the PR.
- Merge only with explicit maintainer authorization.

R764-6 FINISHED
