# #833 round 3 HANDOFF ([A726c])

Status: REVIEW READY, posted on #833 as issuecomment-6577587164. Base: round 2 head `1ff8292c`. Head `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2`, 4 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6576214506.

Sources read in full: R763-2 (PR #834 issuecomment-6575837862) and R764-2 (issuecomment-6575868286), plus their archived reports, scripts and receipts on branch `833-review-evidence` (`review-evidence/833-r1/reviews/R76{3,4}-2/`, fetched at `8b1677a8`, `receipts/review-evidence-fetch-head.txt`). That includes `late_cancel_listing.py`, `probe_late_cancel.py`, `probe_late_cancel_survivor.py`, `make_mutants.py` and `mutate_r2.py`.

## The finding, once with both IDs

**R763-2-F1 = R764-2-F1 (MINOR.** R763-2 files it under all five lenses; R764-2 under Conformance, RTL, Robustness and Docs.) `_cancel` sets `root_notified` while `root_fd` is open, and `run()` keeps it open through `_cleanup()`. So a cancel arriving during cleanup, after the command had been collected, took the resume branch at any clock below 24 s and set `kill_all = clock + TRAP_SECONDS`. On that path the stated "that resume comes before 14 s", "under 34 s" and "under 44 s" were false: a listing that dies inside every census failed at 50 to 54 s, and a late survivor at 40 s.

Manager decision: option (b) (R763-2's numbering; option (a) in R764-2's), the code fix.

**Change:** `scripts/owned_process.py:304`: `... and resumed is None and root_pid in owned and not (live - {root_pid}):`. The comment at `:308-309` gives the behaviour and reason with `#833`: a shell already collected has no trap left, so a cancel during cleanup gives the rest no window of its own.

**Control:** `scripts/test_suite_cancellation.py:657-691` `owner_late_cancel`, called in `main()` at `:706`, named in the PASS line at `:727`. The guide lists it at `docs/testing/TESTING.md:274`. A real `true` runs through `run()` and is collected. In the first census pass of cleanup the control sends the owner SIGTERM, with the endless listing planted as `owner_vanishing` does. The control fails in two ways, each with its own words:
- a SIGCONT sent to the collected shell's `root_fd`: `a cancel after the shell was collected resumed it, re-arming its trap window`;
- no verdict within 15 s wall: `cleanup never reached a verdict after a late cancel`.

`TRAP_SECONDS=30` in its stages makes a re-armed window trip the bound even without the SIGCONT. Unmutated it passes in 0.8 s.

**Failing words with only the fix reverted:** `AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window`, red in 0.0 s. That holds for each of:
- `receipts/control/at-head/revert.log`;
- the matrix row `A726c-resume-collected-shell`;
- R764 driver `M16`, the whole suite on a fresh clone, red in 8.1 s.

With the SIGCONT also dropped (`A726c-rearm-without-sigcont`) it is red at the bound: `cleanup never reached a verdict after a late cancel`.

### Why the control took two commits (deviation from "one for the control")

At `03ea2eb0` the control had only the 15 s bound, with the words "a cancel after the shell was collected re-armed its trap window". The fix revert was red with those words at 15.07 s (`receipts/control/at-03ea2eb0/`). But the first matrix run (`receipts/mutations-47fdd941/`) showed the same words also printed under three mutants that have nothing to do with a resume: R763 `endless-unbounded`, R764 `M10` and R763 `survivor-never-fails`. That names a false cause. Rewriting history was not allowed, so `3740565f` adds the SIGCONT check with its own words and makes the bound's words neutral. The re-run matrix at `3740565f` has no cell that changed between red and green relative to `47fdd941`.

### The bounds after the fix (they hold as written)

A resume now needs the shell in `owned`. While anything is owned, the verdict at `clock >= limit` (`:290`) comes first in the same pass, and `limit` is 14 before any resume. So the resume comes before 14 s, and `limit = clock + 20 < 34` after it. The listing branch adds `REAP_SECONDS`: under 44 s. The verdict comes at most one 0.5 s pass later.

So `scripts/process_test_support.py:19-30`, `docs/testing/TESTING.md:229-235`, the PR body's derivation paragraph and Known limitations bullet, and `FINISH_SECONDS`'s "49.6 s, or 59.6 s for the listing" are exactly true at this head. None was changed.

Two PR-body figures did change with the round, and I updated both: "Seven controls" is now "Eight controls", and the preflight bullet now includes round 3's 0.8 s.

Measured at production constants (`receipts/probes/`):

| Probe | Round 2 head `1ff8292c` | This head `3740565f` (`probes/head/`) |
|---|---:|---:|
| `python3 -I late_cancel_listing.py <clone>/scripts 23` (R763-2's verification) | 53.02 s (`probes/round2-head-1ff8292c/`) | **24.02 s**, under 44 s |
| same at 20, 5 | (R763-2: 50.02, 35.03) | 24.01, 24.01 s |
| R764-2 `probe_late_cancel.py` none / 20 / 23.9 | 24.01 / 50.03 / 53.92 s | 24.01 / 24.01 / 24.01 s |
| R764-2 `probe_late_cancel_survivor.py` 20 | 40.06 s | 21.04 s |
| Round 2's `probe_bounds.py` (live shell; PID namespace) 100/0, 0/1, 13.5/1, 13.9/1 | 14.02, 22.03, 33.51, 33.92 s (round 2's receipts) | 14.01, 22.06, 33.51, 33.92 s (`probes/bounds/`) |

The slowest pass in every probe was under 0.1 s, so these times are owner clock. `probes/head-47fdd941/` has the same probes at the previous head (identical `owned_process.py`), and `probes/worktree-fix-before-commit/` the first ones on the working tree.

Observation, not a change: in R764-2's survivor probe the descendant first appears at 21 s, after the 14 s deadline. It now fails the run in the pass that first lists it, "not sent SIGKILL" when the report is built and SIGKILLed before the raise (`:297-298`), exactly as it would on the no-cancel path. Before the fix the re-armed window gave it 19 s more. The PR body says this.

### Not taken (the scope is F1 only, "touch nothing else")

| ID | Why |
|---|---|
| R763-2-X1, R763-2-X2, R764-2-R1, R764-2-R2 (RESIDUE wording) | No figure in them changes with the fix. They stay on the manager's residue checklist |
| R763-2-S1 / R764-1-S1 (control on the 10 s values) | As in round 2 |
| R763-2-S2 (command-table Issue, `Probe.ready` record) | Manager actions |
| R763-2-S3 (census-cost comment `owned_process.py:84`) | The file was touched this round, but the comment is outside F1. Left for the manager to schedule |
| R764-2-S1 (pin the 0.5 s cap itself) | Outside F1 |

## Commits

| Commit | Subject | What |
|---|---|---|
| `ce2402d8` | Resume a cancelled shell for its trap only while it is still owned and listed | The fix, `owned_process.py:304,308-309` |
| `03ea2eb0` | Control that a cancel during cleanup, after the shell was collected, opens no trap window | The control |
| `47fdd941` | List the control that a cancel after the shell was collected opens no trap window in the testing guide | `TESTING.md:274`, one line |
| `3740565f` | Name the late-cancel control's cause: a resume sent to the collected shell, or no verdict at all | The control, second commit (above) |

Each commit has a one-line subject with no body and no trailers. `git diff --stat 1ff8292c HEAD`: `TESTING.md` +1, `owned_process.py` +3 -1, `test_suite_cancellation.py` +40 -1.

## Mutation re-run (`owned_process.py` changed, so every fix, old and new)

- **Per control** (`receipts/mutations/`: `matrix-table.md`, `matrix.json`, `make_mutants.out`, one log and rc per run; driver `receipts/tools/matrix3.py` + `run_control3.py`). The mutants are:
  - R763-2's `make_mutants.py`, unchanged: 14, including `none`;
  - every suite entry of R764-2's `mutate_r2.py`, plus `M16`: 21;
  - mine: `A726c-resume-collected-shell` and `A726c-rearm-without-sigcont`.

  That is 37 mutants × 8 owner controls = 296 runs, each in its own user+PID namespace with a 150 s bound. The 7 older columns match R763-2's and R764-2's round 2 tables in every row. The new `late_cancel` column:
  - red under the fix revert (both forms) and `M16`;
  - red at the neutral bound under `endless-unbounded`, `M10`, `survivor-never-fails` and `rearm-without-sigcont`;
  - red under `M13`, cleanup does nothing: "an endless listing did not fail the run";
  - green under every other mutant.

  `rearm-without-sigcont` is also red on `shell_window`, since the shell is never resumed.
- **R764-2's whole-test driver** with `M16` added (`receipts/mutations-r764-driver/`: `mutate_r3.py`, `mutate_r2-to-r3.diff`, `summary.json`, one log and rc per entry, `sigign.txt` 0x4). These ran on fresh clones of `3740565f`. Every entry gives its round 2 result:
  - `control-A`, `control-B`, `control-lifecycle` green;
  - `M01`, `M01b`, `M04d`, `M14`, `M15` green, for the reviews' reasons;
  - every other entry red with its round 2 words;
  - `M16` red: `AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window`.

## Gates

All at head `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2`. Each gate has one log and one rc, never piped. The lane gates ran on a fresh clean clone (`receipts/gates/lane.sh`), and `tree-after.txt` is empty with `--ignored`.

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` (round 1's `run_docs_yml.py` and `verify_docs_yml.py`, paths pointed at this lane's scratch; fresh venv identical to round 1's freeze, `venv-freeze*.txt`; fresh HOME) | 0 | Verifier: 64 steps rc 0, 31 not run with round 1's reasons (`not_run.json` unchanged), 0 bad. `git status` clean after each job. Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. SIGHUP not ignored (`sigign.txt`) | `receipts/gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/` (`gate_41`'s log is over 200 KB: sha256 and size in `lane/LARGE-LOGS.txt`, tail in `docsyml/`) |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; `owner-late-cancel: {'verdict_without_trap_window': True}`; `killed_in_pass 28` | `receipts/gates/lane/test_suite_cancellation.*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `receipts/gates/lane/lifecycle.*` |
| Mutation re-run (296 per-control runs; R764 driver, 26 entries) | n/a | As above | `receipts/mutations/`, `receipts/mutations-r764-driver/` |
| Late-cancel and bound probes | 0 each | As above | `receipts/probes/` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `receipts/gates/lane/behave.rc`, `behave-tail.txt`; the log is 235,280 bytes, sha256 in `LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `receipts/gates/lane/diffcheck.*` |
| `check_py_idiom.py` (also inside docs.yml) | 0 | all ratchets within budget, `over-long line: 0 <= 0` | `receipts/gates/lane/check_py_idiom.log` (working tree equal to the head's content) |
| Full sweep | not run | Round 3 touches only `scripts/owned_process.py`, `scripts/test_suite_cancellation.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

The hosted contexts and the `act` replay were not run; that is the manager's bank.

## Incidents, no harm

- The first docs.yml run started at `47fdd941`, before the control's second commit. I stopped it at that commit by its own process group (session `4017915`, every member checked to be in this unit's cgroup), with nothing left in the session. Its partial logs are in scratch only (`run1-47fdd941-aborted`, all rc 0 up to `docs-gates-0__ci_step_28`). The receipts are the rerun at `3740565f`.
- The first launch of R764's driver failed before running anything: `clone_at.sh` had lost its execute bit in the copy. I made it executable and relaunched.
- An import of the test module in a quick run left two `.pyc` files in `scripts/__pycache__` of the lane (ignored by git). I deleted those two. The older ignored caches there predate this session.
- Nothing was signalled by name. Long runs were detached with `setsid`, without `nohup`, so SIGHUP was not ignored (`SigIgn 0x4`).
- The memory of this unit stayed near 3 GB.

## Files

- `PR-BODY.md`: round 2's live body (equal to round 2's `PR-BODY.md`) with a Round 3 section and the edits listed above.
- `receipts/taken.md`: the TAKEN text.
