# #833 round 4 HANDOFF ([A726d])

Status: REVIEW READY, posted on #833 as issuecomment-6579086407. Base: round 3 head `3740565f`. Head `c1b2961777809403bd2de833ec1fa00c75394d6c`, 2 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6577952267.

Sources read: R763-3 (PR #834 issuecomment-6577933512) and its archive on `833-review-evidence` at `f798524f` (`review-evidence/833-r1/reviews/R763-3/`: REPORT, `scripts/matrix.py`, `mutants.py`, `run_control.py`, `trap_probe.py`, `receipts/matrix/`, `receipts/gap/`). The fetch head is in `receipts/review-evidence-fetch-head.txt`. R764-3 is POSITIVE and carries no finding for this round. R763-2 and R764-2 were read for the residue's exact fixes, from round 3's scratch copies.

## The finding

**R763-3-F1 (MINOR, Tests; R763-3 only. R764-3 is POSITIVE and has no matching ID).** No control pinned the in-window guard at `scripts/owned_process.py:315-318`: `(resumed is None or clock < kill_all)`. `owner_shell_window` resumed its shell about 0.9 s into cleanup. That is before `deadline + 1.0` (1.2 s at the control's 0.2 s grace), where the stubborn-leaf rule at `:327` also spares the shell. So the mutant `shell-killed-when-resumed` (the `clock < kill_all` term removed) was green everywhere.

**Change (commit `2aa5f2da`):** `scripts/test_suite_cancellation.py:563-565`. In `owner_shell_window`, `now < blocked[0] + 0.7` becomes `+ 1.5`, with a two-line comment giving the reason. This is R763-3's variant: one number, every assertion kept. The child now dies 1.5 s after the first send, so the shell is resumed past grace + 1 s, and only its own window spares it in its resume pass.

**Control:** `owner_shell_window` (`test_suite_cancellation.py:542-581`), in the preflight at `:705`. `TESTING.md:273` already lists it ("A shell resumed late keeps its whole window…"), so nothing changed there.

| Run | Result | Receipt |
|---|---|---|
| Unmutated, working tree, namespace | PASS 3.1 s (2.3 s at `3740565f`, R763-3's `matrix/none`) | `receipts/control-quick/none.log` |
| `shell-killed-when-resumed` | FAIL 1.6 s: `the shell was killed in the pass that resumed it, before its trap` | `control-quick/`, `matrix-r763-3/shell-killed-when-resumed/`, `matrix-39/R763-3-shell-killed-when-resumed/` |
| `no-trap-window`, `M05`, `M06`, `no-shell-window` | red, same words as round 3 | `matrix-r763-3/`, `matrix-39/` |
| `trap-commands-no-window`, `trap-commands-1s`, `M07`, `M07b` | red: `the resumed shell's trap command was killed inside the shell's window` | same |
| Whole suite with the mutant, fresh clone (R764 driver) | rc 1 in 5.5 s, same words | `r764-driver/R763-3-shell-killed-when-resumed.*` |
| Lifecycle test with the mutant | rc 0, a probe: that test does not run this control (as at round 3) | `r764-driver/R763-3-shell-killed-when-resumed-lifecycle.*` |

The guard is correct, so this is not a STOP. Unmutated, the trap and its command both finish. Every gate is green.

Stated limit (also in the PR body): the control holds the child on wall time. The resume falls back under grace + 1 s on the owner's clock only if the passes before it ran more than 0.3 s past their 0.5 s cap in total. Such a run would be green even with the guard removed. That only weakens one run; it can never make the control red unmutated.

## Residue (commit `c1b29617`)

| IDs | Where | Exact fix applied |
|---|---|---|
| R763-2-X1 | `docs/testing/TESTING.md:230`; `scripts/process_test_support.py:22-24` (the rest of that comment rewrapped, no word changed); PR body derivation | "After a resume, every remaining descendant's deadline is 20 s after the resume, including one the trap started." |
| R763-2-X2 = R764-2-R2 | `docs/testing/TESTING.md:224` | "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell, which keeps its own window." |
| R764-2-R1 | PR body derivation (`PR-BODY.md` only; not a committed file) | "A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock." |

X2 and R2 differ by one word ("stopped" against "cancelled"). I took "cancelled". At 4 s the notified shell is either still stopped or resumed and inside its window, and `:317` spares it in both cases, so "stopped" covers only one of them. The reason is in the PR body.

## Not taken

- **R763-3-S1** (pin "listed" as well as "owned"). F1's verification requires that no other matrix row changes. A control for S1 turns `new-fix-census-not-owned` red, which is another row changing in the same round. R763-3 also shows the variant re-arms only in the pass that reaps the shell, before 14 s, so every bound holds. Left for a later round or the manager.
- R763-2-S1/S2/S3 and R764-2-S1: unchanged, on the manager's checklist.

## Commits

| Commit | Subject |
|---|---|
| `2aa5f2da` | Resume the shell-window control's shell past its stubborn leaf's grace, so only its own window keeps it |
| `c1b29617` | State that a resume sets every remaining descendant's deadline and that a cancelled shell keeps its own window |

One-line subjects, empty bodies, no trailers. `git diff --stat 3740565f HEAD`: `TESTING.md` +2 -2, `process_test_support.py` +8 -8 (comment only), `test_suite_cancellation.py` +3 -1. `owned_process.py` is untouched.

## Mutation re-run

- **R763-3's matrix** (`receipts/matrix-r763-3/`), run with its `mutants.py`, `matrix.py` and `run_control.py` unchanged (copies in `receipts/tools/r763-3/`), on a fresh clone of the head, 10 jobs, `TMPDIR` in scratch. Against R763-3's `receipts/matrix/matrix-table.md`, exactly one row differs: `shell-killed-when-resumed` is now `RED(1)` on `shell_window` (0 → 1). The table is in the PR body.
- **Round 3's 37-mutant table, plus R763-3's two mutants** (`receipts/matrix-39/`; driver `tools/matrix3.py`, its diff from round 3 is `tools/matrix3-r3-to-r4.diff`). 39 × 8 = 312 runs, each in a user+PID namespace. The 37 old rows are identical to round 3's table, cell for cell and in their failing words with times and PIDs normalised. New rows: `R763-3-shell-killed-when-resumed` red on `shell_window` only; `R763-3-new-fix-census-not-owned` green (S1).
- **R764-2's whole-test driver** (`receipts/r764-driver/`; `tools/mutate_r4.py`, diff `tools/mutate_r3-to-r4.diff`). It ran on fresh clones of the head, 8 jobs. Every round 3 entry gives its round 3 result (`compare.txt`). The new suite entry is red, and the new lifecycle probe is green.

## Gates

All at head `c1b2961777809403bd2de833ec1fa00c75394d6c`. Each gate has one log and one rc, never piped. The lane gates ran on a fresh clean clone (`receipts/gates/lane.sh`), and `tree-after.txt` is empty with `--ignored`.

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` (round 1's `run_docs_yml.py` and `verify_docs_yml.py`, paths pointed at this lane's scratch, `not_run.json` unchanged; fresh venv identical to round 1's freeze, `venv-freeze*.txt`; fresh HOME) | 0 | Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. `git status` clean after each job. Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. SIGHUP not ignored (`sigign.txt`, 0x4) | `receipts/gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/` (`gate_41`'s log is over 200 KB: sha256 and size in `LARGE-LOGS.txt`, tail in `docsyml/`) |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; `owner-shell-window: {'trap_ran_after_kill_time': True, 'trap_command_ran': True}` | `receipts/gates/lane/test_suite_cancellation.*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `receipts/gates/lane/lifecycle.*` |
| Mutation re-run (R763-3 matrix 104 runs; round 3 table + 2 = 312 runs; R764 driver 27 entries) | n/a | As above | `receipts/matrix-r763-3/`, `matrix-39/`, `r764-driver/` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `receipts/gates/lane/behave.rc`, `behave.log.tail`; the log is 235,280 bytes, sha256 in `LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `receipts/gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py` (also inside docs.yml) | 0 each | before each commit, on the working tree | scratch only; the docs.yml receipts are the evidence at the head |
| Full sweep | not run | Round 4 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

## Incidents, no harm

- The first two waits on detached runs returned at once: `$!` was `setsid`'s PID, not the runner's. The 39-mutant matrix had already finished (`matrix.json` written, 312 rows). For the R764 driver I waited on its real PID.
- Nothing was signalled by name or at all. Long runs were detached with `setsid`, without `nohup`.
- No `.pyc` was written to the lane: every run used `-B` or `PYTHONDONTWRITEBYTECODE`. The lane's ignored `scripts/__pycache__` predates this session.
- Memory of this unit stayed well under 12 GB.

## Files

- `PR-BODY.md`: round 3's body (equal to the live body) with the round 4 edits listed in its Round 4 section.
- `receipts/taken.md`, `receipts/ready.md`: the posted texts.
