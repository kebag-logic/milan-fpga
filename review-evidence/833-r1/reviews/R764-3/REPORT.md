[R764] POSITIVE - exact head 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2

External cleared-context review, round R764-3, issue #833 / PR #834.
Head `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2`, tree `b20b2b7136079a25226b806a897ab3f18e4a8e90`.
Source base `1f29f189279f9fc0132f4918e47342b87d22f33a`. Delta reviewed: `1ff8292c..3740565f`, four one-line commits with no trailers:

- `ce2402d8`: `scripts/owned_process.py` +3/-1
- `03ea2eb0` and `3740565f`: `scripts/test_suite_cancellation.py` +39/-1 net
- `47fdd941`: `docs/testing/TESTING.md` +1

## Verdict basis

No BLOCKER, MAJOR or MINOR is open. All five lenses are covered clean at this head.

The round 2 MINOR (R764-2-F1, the same as R763-2-F1) is resolved at its cause:

- The code now makes the three stated bounds true.
- A control goes red with only the fix reverted.
- Every published figure checks out at this head.

Open items that do not block:

- New: one wording RESIDUE (R764-3-R1).
- Retained from round 2, which the author published as not taken: RESIDUE R764-2-R1 and R764-2-R2, and SUGGESTION R764-2-S1.
- The other review's round 2 RESIDUE and SUGGESTION items are listed under [Prior findings](#prior-findings-at-this-head).

## Checks requested

### (1) A resume re-arms the trap window only while the notified shell is still owned

`scripts/owned_process.py:304` now reads `if self.root_notified and resumed is None and root_pid in owned and not (live - {root_pid}):`.

`owned` (`:281`) is the census minus every child reaped in the same pass (`:280`). So a shell that was collected, either before cleanup or during this census, cannot open the window.

The code paths agree:

- `run()` (`:365-370`) enters cleanup in one of two ways. Either `poll()` has already collected the shell, or `checkpoint()` raised `Cancelled`, in which case `_cancel` (`:187-195`) or `:361-364` already notified the shell before cleanup.
- So a cancellation that first arrives during cleanup always meets a collected shell. Now it only sets `root_notified`; the `SIGSTOP` and signal sent to the closed-out pidfd are absorbed (`:203-207`).
- The still-owned, stopped shell keeps its window. The shell-window control stays green unmutated, and M05, M06, M07 and M07b stay red (table below).

Measured at production constants, each probe in this packet (`receipts/probes/`). Every pass took under 0.1 s, so wall time equals owner clock:

| Probe | Cancel at | This head | Fix alone reverted | Stated bound |
|---|---:|---:|---:|---|
| `scripts/probe_late_cancel.py <head> none` | none | 24.00 s | n/a | under 44 s (24 s + one pass) |
| `scripts/probe_late_cancel.py <head> 5` | 5.01 s | 24.01 s | n/a | under 44 s |
| `scripts/probe_late_cancel.py <head> 20` | 20.00 s | 24.00 s | **50.01 s** | under 44 s |
| `scripts/probe_late_cancel.py <head> 23.9` | 23.92 s | 24.02 s | n/a | under 44 s |
| `scripts/probe_late_cancel_survivor.py <head> 20` | 20.04 s | 21.07 s; descendant first listed at 21.05 s | n/a | 14 s deadline already passed: judged in its first pass |

### (2) `owner_late_cancel` goes red with only the fix reverted

This was checked in three ways.

- **Full suite.** Run with only `root_pid in owned and` removed (M16), each in its own clone and user+PID namespace, it is red with `AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window` (`receipts/mutations/M16-resume-collected-shell.log`).
- **The control alone** (`scripts/late_cancel_only.sh`, `receipts/per-control/`):

  | Mutant | Result |
  |---|---|
  | M16 | red, with the cause message |
  | M16b (window re-armed, `SIGCONT` withheld) | red, with `cleanup never reached a verdict after a late cancel`, so the 30 s `TRAP_SECONDS` override catches a window with no signal |
  | M10 (endless listing unbounded) | red, with the neutral words, as the PR body states |
  | Unmutated head, 10 runs | green, 0.83 s each, matching the PR body's "0.8 s" (`:103`) |

- **Vacuity.** The control asserts `owner.root_notified`, so a cancel that never reached cleanup cannot pass it vacuously.

### (3) `late_cancel_listing.py` at the head

The published round 2 probe was copied verbatim; the sha256 is recorded in `receipts/evidence-manifest-check.txt`.

| Cancel at | This head | Fix alone reverted |
|---:|---:|---:|
| 23 s | **24.00 s** | 53.02 s |
| 20 s | 24.01 s | n/a |
| 5 s | 24.00 s | n/a |

The author's 24.02 s (was 53.02 s) reproduces: under 44 s at this head.

### (4) The three bound statements and the `FINISH_SECONDS` justification

The three statements are `scripts/process_test_support.py:19-30`, `docs/testing/TESTING.md:229-235`, and the PR body's "The deadline's derivation".

Derivation from the code at this head:

- Before any resume, `kill_all` is 4 s, so `limit` (`:289`) is 14 s. Only the resume (`:312`) raises `kill_all`, and it fires at most once (`resumed is None`).
- A resume now needs `root_pid in owned`, so `owned` is non-empty. The failure test at `:290` runs earlier in the same pass and fails the run at `clock >= 14`. So the resume comes strictly before 14 s ("That resume comes before 14 s" is true).
- After the resume, `limit = r + 20 < 34`, so "under 34 s" holds.
- The listing branch (`owned` empty) fails at `limit + REAP_SECONDS < 44`, so "under 44 s" holds.
- A pass advances the clock by at most `MAX_PASS_SECONDS` (`:284`), so "at most 0.5 s of owner clock later" holds.
- `FINISH_SECONDS = 60`: 34 + 0.5 + 15.1 = 49.6 and 44 + 0.5 + 15.1 = 59.6. Both are under 60, with the stated condition that passes stay within 0.5 s.

All three statements are exactly true, are word-for-word consistent, and none needed a change.

### (5) The whole mutation table, re-run at this head

27 entries ran in 10 parallel jobs, each in a fresh clone at this head and its own user+PID namespace (`scripts/mutate_r3.py`, `receipts/mutations/`, `receipts/mutation-table.md`).

- Every one of the 24 round 2 entries gives the same result as at `1ff8292c`.
- M01 is green as in round 2, where it was accepted because M01c, both halves together, is red.
- New entries: M16 red, M16b red, and M16c probe-green.
- M16c (resume while the shell is listed in the census, rather than owned) is equivalent on every production path, because the shell's zombie is never listed in cleanup: `run()` has already collected it by then. It is not a test gap.

The author's published 37-mutant x 8-control matrix (`author-r3/receipts/mutations/matrix-table.md`) was spot-checked. Two entries were read in full:

- `A726c-resume-collected-shell/owner_late_cancel.log` is red with the cause message.
- `control/at-head/head.log` passes in 0.8 s.

### Gates run at the head clone (`receipts/head/`)

| Gate | rc | Result |
|---|---:|---|
| `docs_check.py` | 0 | 0 findings |
| `check_doc_style.py` | 0 | OK |
| `check_doc_style.py --selftest` | 0 | OK |
| `check_py_idiom.py` | 0 | over-long line 0 <= 0 |
| `check_py_idiom.py --selftest` | 0 | 54/54 |
| `git diff --check 1f29f189 HEAD` | 0 | none |

The clone stayed clean.

### Published evidence

`review-evidence/833-r1` at `40eda54e` was checked:

- The 1466 `author-r3/` entries all match `MANIFEST.json`'s `published_sha256`, with none missing and none unlisted.
- `probes/head-sha.txt` names this head.
- The archive commit itself is not signed in GitHub's sense ("unsigned"). Integrity here rests on the manifest digests, not on a signature.

### Comment rule

The added comments and docstrings cite only `#833` and state behaviour and reason. No lane label, round, reviewer ID or comment ID was added in the delta (`git diff 1ff8292c..HEAD`, grep of added lines).

## Findings

**R764-3-R1 - RESIDUE - Docs, Tests - `scripts/test_suite_cancellation.py:659`**

- Wording: "A re-armed window would hold the verdict past this bound: TRAP_SECONDS is longer." "This bound" has no antecedent at that point; the 15 s bound only appears at `:679`.
- Exact fix: "A re-armed window would hold the verdict past the 15 s bound below: TRAP_SECONDS is 30 s."
- Pure comment wording: no code, figure or verdict changes.

No other new finding.

## Prior findings at this head

| ID | Severity | Status at 3740565f | Evidence |
|---|---|---|---|
| R764-2-F1 (= R763-2-F1) | MINOR | **Resolved at its cause** | Checks (1) to (5) above. A collected shell opens no window. The bounds hold as written. M16 red. The listing comes at 24.0 s for every cancel time, where reverting the fix gives 50.01 s and 53.02 s |
| R764-2-R1 | RESIDUE | Retained, not taken (author's stated scope) | The PR body's derivation still reads "A true survivor still fails the run, where it was 4 s: A true survivor's deadline is 14 s ...". Exact fix as in round 2: "A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock." |
| R764-2-R2 | RESIDUE | Retained, not taken | `docs/testing/TESTING.md:224` is unchanged. Exact fix as in round 2: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell, which keeps its own window." |
| R764-2-S1 | SUGGESTION | Retained, optional | M04d (cap 1.0 s) is still green, so the 0.5 s cap itself is not pinned |
| R763-2-X1, R763-2-X2 | RESIDUE (other review) | Retained by the author for the manager's residue checklist | Not re-adjudicated. X2 is the same line as R764-2-R2 |
| R763-2-S1, S2, S3 | SUGGESTION (other review) | Retained, optional | S3 (the census-cost comment, `owned_process.py:84`) is still unaligned. That file was touched in this round, but outside the comment |
| R764-1 findings | various | Resolved in round 2; the delta does not touch what they depend on | Round 2 report table |

## Lens results

```text
[R764] PASS Conformance - scripts/owned_process.py:280-312, scripts/process_test_support.py:19-30, docs/testing/TESTING.md:229-235, PR body derivation at 3740565f; receipts/probes/ - #833 acceptance 2 ("no suite left to fail by chance", a deadline from evidence) still holds; the round 2 premise "resume before 14 s" now follows from the code, and every stated bound and FINISH_SECONDS's 49.6/59.6 s are true and match the probes (24.00-24.02 s against fix-reverted 50.01/53.02 s)
[R764] PASS RTL - scripts/owned_process.py:256-339 at 3740565f (process-control state machine; no HDL in the diff, git diff --stat 1f29f189..HEAD) - the resume transition now has a complete guard (notified, not yet resumed, shell owned, no other live descendant); kill_all is changed only once by the resume; the failure test comes before the resume in each pass; no ordering, width or index change
[R764] PASS Robustness - scripts/owned_process.py:187-195,203-207,304-312,361-374; receipts/probes/head-late-cancel-*.log, head-listing-*.log, head-late-cancel-survivor-20.log - a cancel during cleanup at 5, 20 and 23.9 s, a late real survivor and the endless listing; the signal to a collected shell's pidfd is absorbed; the live notified shell keeps its window (M05/M06/M07/M07b red)
[R764] PASS Tests - scripts/test_suite_cancellation.py:657-691,706,727; receipts/mutations/ (27 entries), receipts/mutation-table.md, receipts/per-control/ - owner_late_cancel is red under M16 (cause message) and M16b and M10 (bound message) and green unmutated 10/10 at 0.83 s; asserts root_notified against vacuity; the 24 round 2 entries match; control-A, control-B and control-lifecycle green (R764-3-R1 is comment wording only)
[R764] PASS Docs - docs/testing/TESTING.md:229-235,274; PR body "Round 3" and "Known limitations" (receipts/pr-body-at-review.md); receipts/head/gate-*.log - the new line 274 states the behaviour exactly; the round 3 table's line refs (:304-309, :657-691, :706, TESTING.md:274) and figures match the head; doc gates rc 0; retained RESIDUE only
```

## Ledger (reviewer-owned)

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `owned_process.py:280-312`; `process_test_support.py:19-30`; `TESTING.md:229-235`; PR body derivation; `receipts/probes/` | R764-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| RTL | CLEAN | `owned_process.py:256-339`, the cleanup state machine (no HDL in the diff) | R764-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| Robustness | CLEAN | `owned_process.py:187-207,304-312,361-374`; late-cancel, listing and survivor probes | R764-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| Tests | CLEAN | `test_suite_cancellation.py:657-691,706`; 27-entry mutation table; per-control runs; lifecycle control | R764-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |
| Docs | CLEAN | `TESTING.md:229-235,274`; PR body Round 3; doc gates | R764-3 | 3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2 |

The ledger rests on R764-3 at this exact head for every lens. Every file the PR changes is either in this round's delta or was examined in round 2 at `1ff8292c`, and nothing those lenses depend on was changed since: `process_test_support.py` and `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` are unchanged since `1ff8292c`.

## Executed (each with its own log and rc)

- Head clone and fix-reverted clone made by `scripts/clone_at.sh`.
- Probes: 8 runs at the head and 2 with the fix reverted, concurrently (`receipts/probes/`).
- Mutation campaign: `python3 -I scripts/mutate_r3.py <review clone> <head> <work> receipts/mutations 10`, with driver rc 0 (`receipts/mutations/driver.log`, `summary.json`). It ran under a launcher with an empty ignored-signal mask, and PATH carried the pinned compiler (identity verified as 5.050) first. Whether the lifecycle test invokes a compiler is not claimed.
- Per-control runs: 15 (`receipts/per-control/`).
- Doc gates: 5, plus `git diff --check` (`receipts/head/`).
- Restoration (`receipts/restore-verification.txt`). The review clone was never modified and is still at the exact head:
  - HEAD and tree match.
  - Index equals HEAD, and the worktree equals the index.
  - The four reviewed blobs match `HEAD:` by hash.
  - The six gitlinks are unchanged; `external` is uninitialised, as it was at the start.

## Real limits

- No manager source bank and no full sweep ran at this head. Source-head execution evidence is the author's published gate receipts, spot-checked here, and this packet's focused runs.
- The listing that dies inside every census is a planted substitution, the same one the control uses. Whether a real sweep reaches that state is not shown, only that the bounds hold once it is reached.
- In the listing state, a descendant first listed after the 14 s deadline fails the run in that pass, without a window after `SIGKILL`. This is consistent with "14 s into cleanup" and is stated in the PR body. It is recorded here only so no reader takes `TESTING.md:269-270` to promise every descendant a post-`SIGKILL` window.
- Hosted contexts at this head were queued or in progress at 12:58 UTC, with none concluded (`receipts/hosted-checks-snapshot.txt`). The manager owns the hosted and act acceptance.
- Physical calibration was not run. Field skips are not hardware proof.
- The published archive commit `40eda54e` is unsigned. Its integrity was checked by manifest digest only.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `1f29f189`, live dev `503bc97c`): builder and native banks, with receipts linked on the PR.
- Hosted acceptance at the exact head: `rtl-fast`, plus `verilator-suites` and `yosys-portability` if applicable, and act.
- Carry the residue checklist: R764-3-R1, R764-2-R1, R764-2-R2, R763-2-X1 and R763-2-X2.
- Optional suggestions: R764-2-S1 and R763-2-S1, S2 and S3.
- Maintainer authorization for the merge.

R764-3 FINISHED
