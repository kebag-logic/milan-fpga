[R763] NEGATIVE - exact head 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2

# R763-3: internal cleared-context review of PR #834 (issue #833), round 3

- Head `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2`, tree `b20b2b7136079a25226b806a897ab3f18e4a8e90`, on source base `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- The round 3 delta is `1ff8292c..3740565f`: 4 commits, 3 files, +43/-2.
  - `scripts/owned_process.py:304,308-309`
  - `scripts/test_suite_cancellation.py:657-691,706,727`
  - `docs/testing/TESTING.md:274`
- The PR head on GitHub equals this head: `gh pr view 834` gives headRefOid `3740565f…`, not a draft, base `dev`.

**Verdict basis.** The round 2 finding (R763-2-F1 = R764-2-F1) is **resolved at its cause**:
- the fix is correct;
- the new control goes red with only the fix reverted;
- the stated bounds and the `FINISH_SECONDS` argument are exactly true at this head.

The verdict is NEGATIVE for one **new MINOR (Tests)**, R763-3-F1. The mutation re-run requested in check (5) found it. It is a guard that no control pins: `owned_process.py:317` keeps a resumed shell alive inside its own window. Removing that guard passes every owner control, the whole `test_suite_cancellation.py` and the lifecycle test. At product constants, the same mutant SIGKILLs the shell before its trap whenever the resume comes 3 s or more into cleanup. The product at this head is correct. Only the test cannot see the regression.

The guard predates the round 3 delta: it came in with `34cbcc82`, in round 1, and rounds 1-2 did not report it. It is reported now because "everything you find" goes in this one report. Section 7 of AGENTS.md also forbids downgrading a finding to bank a lens. A one-number change to the existing control closes it (probe below), so I do not prescribe a design.

## Scope reconstructed

- **AGENTS.md / CONTRIBUTING precedence.** These set the five lenses, the severity scale and the reviewer-owned ledger. The owner rules in the review assignment add the RESIDUE class, token economy and the comment rule.
- **Issue #833** (open) has two frozen acceptance criteria:
  1. the failure message prints each descendant's `/proc/<pid>/stat` state;
  2. from that evidence, either a fixed deadline or a real fix, with no suite left to fail by chance.

  The issue comments hold the round 1-2 verdicts and the A10 start notices. No new scope decision was posted after round 2.
- **Authorities for this delta:**
  - `scripts/owned_process.py:30-45` (stage constants), `:256-339` (cleanup);
  - `scripts/process_test_support.py:19-30` (`FINISH_SECONDS` and its derivation);
  - `docs/testing/TESTING.md:223-235` (stages, clock and bounds) and `:255-276` (control list);
  - the PR body's "Round 3" section.
- **Author evidence.** Spot-checked from the public tree `40eda54e…/review-evidence/833-r1/author-r3/receipts`:
  - `ready.md`;
  - `control/at-head/{head,revert,unbounded}`;
  - `probes/head/*`;
  - `mutations/matrix-table.md`;
  - `mutations-r764-driver/summary.json`.
- **Prior public review findings.** I read R763-2 and R764-2 only after my own pass over the diff and my own probes.

## Findings

**R763-3-F1: MINOR. Lenses: Tests.** `scripts/test_suite_cancellation.py:542-584` (`owner_shell_window`) does not pin the in-window protection at `scripts/owned_process.py:315-318`. That guard reads `(resumed is None or clock < kill_all)`, under the comment "never in the pass that resumes it, whatever the time then (#833)".

- **Authority.** AGENTS.md §6 Tests: "Each new test can fail for the defect it claims to detect." Two places claim this behaviour:
  - the control's docstring: "A shell resumed past the kill time runs its trap … before any SIGKILL";
  - `docs/testing/TESTING.md:273`: "A shell resumed late keeps its whole window to run its terminal trap and the commands it starts".
- **Cause.** The control uses `GRACE_SECONDS=0.2`. Its stubborn child dies about 0.7 s after the first send, so the shell is resumed near clock 0.9 s. That is before `deadline + 1.0` = 1.2 s. At that point the stubborn-leaf-first guard at `owned_process.py:327` (`clock < deadline + 1.0 and pid in initial.values()`) also spares the shell, because the shell is its child's first parent. Either guard alone keeps the control green.
- **Evidence.** The mutant `shell-killed-when-resumed` makes one edit, at `:317`: `(resumed is None or clock < kill_all):` becomes `resumed is None:`.
  - It is green on all 8 owner controls (`receipts/matrix/`), on the whole `scripts/test_suite_cancellation.py` (`receipts/gap/mut-whole-suite.log`, rc 0) and on `make -C tb/verilator/gptp_shadow lifecycle` (`receipts/gap/mut-lifecycle.log`, rc 0). The last two ran on a disposable clone of this head in a user+PID namespace.
  - At product constants, `scripts/trap_probe.py` holds the resume back with one listed descendant that stays live until a set time:

    | Resume at | Head (`receipts/gap/head-resume-*.log`) | Mutant (`receipts/gap/mut-resume-*.log`) |
    |---:|---|---|
    | 1.0 s | trap ran, shell never SIGKILLed | trap ran (the leaf-first guard covers it) |
    | 3.5 s | trap ran, shell never SIGKILLed | **shell SIGKILLed at 3.51 s, in its resume pass; trap did not run** |
    | 8.0 s | trap ran, shell never SIGKILLed | **shell SIGKILLed at 8.02 s; trap did not run** |
- **Impact.** The trap is lost when a resume comes 3 s or more into cleanup, and no gate would catch a regression that brings that back. That timing needs a descendant to take over 1 s to die after its SIGKILL. That is the D-state stall this PR documents (1.91 s and 3.04 s episodes, `owned_process.py:30-36`). The sweep's EXIT trap would then be killed before it reports the cancellation, which is what #833 protects. No current result is wrong.
- **Required outcome.** A control in which a cancelled shell is resumed at or past `deadline + 1.0` must go red with the `clock < kill_all` term removed from `:317`. M05/M06, `no-trap-window` and `trap-commands-*` must stay red, and the control must stay green unmutated. No design is required.
  - One cheap way exists, and it is not prescribed: in `owner_shell_window`, `now < blocked[0] + 0.7` becomes `+ 1.5`. In `receipts/gap/strengthened/` that variant is green at head in 3.1 s and red for `shell-killed-when-resumed`, `no-trap-window` and `trap-commands-no-window`.
- **Verification.** Re-run `scripts/matrix.py` with `scripts/mutants.py`, or the author's matrix with this mutant added. `shell-killed-when-resumed` must be red on at least one owner control, and no other row may change.

**R763-3-S1: SUGGESTION. Lenses: Tests.** The new control pins only "collected before cleanup". It does not pin the second half of "still owned **and listed**": a shell listed in the census and then collected by the same pass's second reap.

- Mutant `new-fix-census-not-owned` (`root_pid in census`) is green everywhere.
- That variant can only re-arm the window in the pass where the shell is reaped. Root in census means cleanup has just begun, or the shell died of a default-fatal signal. That pass comes before 14 s, so every stated bound still holds.
- Optional. No figure, verdict or bound depends on it.

**Retained RESIDUE** (not taken in round 3, by the author's stated scope; still present verbatim at this head; carried to the manager's residue checklist with the exact fixes given in round 2):
- R763-2-X1: `TESTING.md:230`, `process_test_support.py:22-23` and the PR body read "One started by a resumed shell's trap has its deadline 20 s after the resume". After a resume this deadline applies to every remaining descendant.
- R763-2-X2 = R764-2-R2: `TESTING.md:224` reads "Two seconds later `SIGKILL` has reached every other descendant." A stopped shell is excepted.
- R764-2-R1: PR body line 48 reads "…where it was 4 s: A true survivor's deadline…"

No new RESIDUE in the delta. The added comments (`owned_process.py:308-309`, `test_suite_cancellation.py:658-659,667,671`) state behaviour and reason with `#833` only. They carry no lane label, lane name, review round, reviewer ID or comment ID. The 4 commit subjects are one line each with empty bodies.

**Retained SUGGESTIONS** (optional; unchanged): R763-2-S1 (10 s windows not pinned; `reap-window-2s` green), R763-2-S2 (manager actions R763-1-S1/S2), R763-2-S3 (census-cost comment figure), R764-2-S1 (0.5 s cap pinned only below about 1.5 s; M04d green).

## Round 2 finding at its cause, at this head

| Prior finding | Status | Evidence at this head |
|---|---|---|
| R763-2-F1 = R764-2-F1 (a cancel after the shell was collected re-arms the trap window; "resume before 14 s", "under 34 s" and "under 44 s" false; `FINISH_SECONDS` argument broken) | **RESOLVED** (option (b) of R763-2, option (a) of R764-2) | See checks (1)-(5) below |
| R763-2-X1, X2; R764-2-R1, R2 | Retained RESIDUE | above |
| R763-2-S1/S2/S3, R764-2-S1 | Retained SUGGESTION | above |
| Round 1 findings | Resolved in round 2; the delta does not touch what they depend on | R763-2 / R764-2 tables |

**(1) A resume re-arms only while the shell is owned: verified.**
- `owned_process.py:304` now requires `root_pid in owned`. `owned` is the census minus what the second reap collected (`:280-281`).
- `run()` collects the shell with `Popen.poll()` before `_cleanup()` (`:365-370`). So after a normal exit the shell is never in `owned`, and a cancel during cleanup cannot resume it. In the patched control and in both late-cancel probes, `resumes=[]` at head.
- A live notified shell is stopped and stays in `owned`, so its resume still happens. In `receipts/probes/head-shell-*-13.9.log`, `resumes=[13.92]`/`[13.93]`.
- Context-only cleanup has `root_pid=None`, so it never resumes, as before.

**(2) The new control goes red with only the change reverted: verified.**
- `receipts/control/revert-owner_late_cancel.log`: rc 1, `AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window`.
- Head: rc 0, 0.8 s.
- The author's `control/at-head/{revert,unbounded}` agrees, including the bound-only path ("cleanup never reached a verdict after a late cancel").
- My `listing-unbounded` and `survivor-never-fails` mutants also turn it red, at the 15 s bound.
- I checked that 1ff8292c equals this head minus the fix: `diff` after removing the fix and its comment gives no output.

**(3) The round 2 probe reports under 44 s: verified.** `python3 -I late_cancel_listing.py <scripts> 23` is R763-2's published script, copied unchanged to `scripts/round2/`.

| Cancel at | Head | 1ff8292c |
|---:|---:|---:|
| 23 s | **24.00 s** | 53.02 s |
| 20 s | **24.00 s** | 50.03 s |

My own independent probe, `scripts/bound_probe.py late-listing`, agrees:

| Cancel at | Head | 1ff8292c |
|---:|---:|---:|
| 23 s | 24.03 s | 53.04 s (`resumes=[23.04]`) |
| 5 s | 24.03 s | 35.04 s |

Every pass took 0.04 s or less, so these times are owner clock. The author's 24.02 s / 53.02 s is reproduced.

**(4) The three bound statements and the `FINISH_SECONDS` justification are exactly true: verified by derivation and measurement.**
- **Derivation.** A resume needs `root_pid in owned`, so `owned` is non-empty. Before any resume, `limit = kill_all + REAP = 4 + 10 = 14`. At `clock >= 14` with `owned` non-empty, `:290` raises before `:304` is reached. So any resume happens below 14 s, and it happens at most once (`resumed is None`). After it, `limit = resume + 20 < 34`. A listing waits `REAP` more, under 44 s. The verdict comes in the first pass at or past the deadline, at most 0.5 s of owner clock later.
- These are the exact statements in:
  - `TESTING.md:229-235`;
  - `process_test_support.py:19-29` (14 s; under 34 s; under 44 s; 34 + 0.5 + 15.1 = 49.6 s; 44 + 0.5 + 15.1 = 59.6 s; both below 60 under the stated 0.5 s-per-pass condition);
  - the PR body's "The deadline's derivation" and "The bounds hold as written".
- **Measured worst cases** at product constants, resume held to 13.9 s (`receipts/probes/`):

  | Case | Head | 1ff8292c | Stated |
  |---|---:|---:|---|
  | Listing that dies inside every census | **43.95 s** | 43.96 s | under 44 s |
  | Never-collected survivor | **33.94 s** | 33.94 s | under 34 s |

  The live-shell path is unchanged by the delta, as expected.
- **One residual ordering, checked and harmless.** A notified shell can sit in `owned` as a zombie: it exits between the second reap and `:304`, which needs an external SIGKILL or a default-fatal signal. It can then still be "resumed". Even so, `owned` is non-empty, so the resume is still below 14 s and every bound holds.

**(5) Whole mutation table, old and new fixes, at head: verified, apart from F1.**
- **Author table.** `mutations/matrix-table.md` has 37 mutants × 8 owner controls. Its 7 older columns match R763-2's table row for row. Its suite-driver results match R764-2's (M01/M01b/M04d/M14/M15 green as before, M05/M06/M07/M07b red), and `M16` is red. `mutations-r764-driver/summary.json` also has `control-A`/`B`/`lifecycle` green.
- **My independent re-run** of 13 mutants × 8 controls, each in its own user+PID namespace (`receipts/matrix/matrix-table.md`, `matrix.json`):
  - every old fix is red when reverted alone: identity-has-parent, listing-unbounded, no-kill-before-raise, no-reap-after-census, no-trap-window, pass-unclamped, report-without-state, survivor-never-fails, trap-commands-no-window;
  - the new fix is red (`new-fix-reverted`, `owner_late_cancel` only);
  - `none` is green.
  - Two of mine stay green:
    - `shell-killed-when-resumed` is F1;
    - `new-fix-census-not-owned` is S1.

## Lens results (each with its artifact, at head 3740565f)

```text
[R763] PASS Conformance - scripts/owned_process.py:289-312, scripts/process_test_support.py:19-30, docs/testing/TESTING.md:223-235, PR body "Round 3", issue #833 acceptance 1-2 - the round 2 bound defect is fixed in code; all three bound statements and FINISH_SECONDS (49.6/59.6 s) derived and measured exactly true (receipts/probes, receipts/r2-probe); acceptance 1 (state in report) unchanged and still asserted by owner_report/owner_survivor (green in receipts/matrix/none)
[R763] PASS RTL - scripts/owned_process.py:256-339 (cleanup state machine; no HDL in delta) - resume transition now guarded by root_pid in owned; resume at most once and only below 14 s; kill_all monotone; no new path to SIGKILL a notified shell; failure path still kills what it reports; zombie-root ordering analysed above, bounds hold
[R763] PASS Robustness - receipts/probes/*, receipts/r2-probe/*, receipts/control/* - cancel during cleanup at 5/20/23 s after collection (no resume, 24 s); cancel during run with live shell resumed at 13.9 s (43.95/33.94 s); context-only cleanup root None (no resume); repeated cancel latched once (_cancel); suite and lifecycle green (receipts/suite, receipts/lifecycle)
[R763] MINOR Tests - scripts/test_suite_cancellation.py:542-584 vs scripts/owned_process.py:317 - R763-3-F1 (new control owner_late_cancel itself verified sound: red on revert, red at bound, green 0.8 s)
[R763] PASS Docs - docs/testing/TESTING.md:274, :223-235, PR body "Round 3" (line refs :304-309, :657-691, :706, TESTING.md:274 checked), source comments in delta - accurate; the comment rule holds; retained RESIDUE only (non-blocking)
```

## Executed (each with its own log and rc, under `receipts/`)

| Run | Result |
|---|---|
| `python3 scripts/test_suite_cancellation.py` at head | rc 0, `suite cancellation: PASS (… late cancel …)`, 58.0 s |
| `make -C tb/verilator/gptp_shadow lifecycle` at head | rc 0, `mutant lifecycle: PASS`, 39.3 s |
| `owner_late_cancel` on head / revert / census variant / 1ff8292c | 0 / 1 (resume words) / 0 / 1 (control absent there: AttributeError) |
| `bound_probe.py`: 4 cases × head and 1ff8292c | as in (3)-(4) |
| `late_cancel_listing.py` (R763-2's): 23 s and 20 s × head and 1ff8292c | as in (3) |
| `matrix.py`: 13 mutants × 8 controls, 14 jobs, namespaces | as in (5) |
| `trap_probe.py`: resume at 1.0/3.5/8.0 s × head and mutant | F1 table |
| Mutant whole suite and lifecycle on a disposable clone | both rc 0 (F1) |
| Strengthened-control variant × 4 mutants | `none` green, the other 3 red (F1) |
| Hosted check runs at exact head (read-only API) | `hosted-check-runs-at-head.tsv`: 12 runs, 9 queued, 3 in progress, none concluded when read |
| Clone integrity after all probes | `clone-integrity.txt` |

`git diff --check 1f29f189 HEAD` gives rc 0. The scoped Verilator was not needed. Its identity reads `Verilator 5.050 2026-07-01 rev v5.050`.

**Integrity.** After all probes, `HEAD`, the tree, the index and the worktree all match `3740565f`/`b20b2b71`. Every tracked blob hashes to its index entry, no mode changed, and the 6 gitlinks are unchanged (external `efeb541a`, gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, verilog-axis `48ff7a7e`). I removed the ignored `__pycache__` my runs created, so status with ignored files is now empty.

## Ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | owned_process.py:289-312; process_test_support.py:19-30; TESTING.md:223-235; PR body Round 3; issue #833 acceptance; receipts/probes, r2-probe | R763-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| RTL | CLEAN | owned_process.py:256-339 (cleanup state machine); no HDL in the delta | R763-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| Robustness | CLEAN | late-cancel and live-shell probes; suite; lifecycle | R763-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| Tests | **UNCLEAN** (R763-3-F1 open) | test_suite_cancellation.py:542-584, 657-691, 706; receipts/matrix, gap, control | R763-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| Docs | CLEAN (RESIDUE only) | TESTING.md:223-235, 255-276; PR body; delta comments and commit subjects | R763-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |

## Real limits

- **No manager source bank** ran at this head, and none is claimed or inferred. The source-head execution evidence is the author's published receipts plus my focused runs above. Neither the full sweep, the PP/gPTP/Yosys/builder banks nor `act` ran.
- **Hosted contexts** had not concluded when I read them.
- **Physical calibration** did NOT RUN. Field skips are not hardware proof.
- **Planted listings.** The late-cancel and bound probes use a planted listing or fake live descendant, as the owner controls do. They show the bounds once such states are reached, not that a real sweep reaches them.
- **The `docs.yml` re-run** and `behave` (2330 steps) are the author's receipts. I did not re-execute them, since the delta touches neither.

## Pending manager duties

- Carry R763-3-F1 to the author. The Tests lens re-covers at the corrected head.
- Carry the retained RESIDUE (R763-2-X1, X2; R764-2-R1, R2) and the suggestions to the residue checklist.
- Validate the current-dev merge candidate: source base `1f29f189…`, live dev `503bc97c…`, builder and native banks. Then link its receipts on the PR.
- Own hosted and act acceptance on the exact head.
- Publish this report. Merge only on explicit maintainer authorisation.

R763-3 FINISHED
