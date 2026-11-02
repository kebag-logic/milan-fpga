# #833 round 2 HANDOFF ([A726b])

Status: REVIEW READY, posted on #833 as issuecomment-6575547538. Base: round 1 head `d4d8cff9`. Head `1ff8292cd5b761633ef9500a7c5a4b1626a3d92c`, 5 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6574273045.

Sources read in full: R763-1 (PR #834 issuecomment-6573739640) and R764-1 (issuecomment-6573828979), their archived `REPORT.md`, scripts and receipts on branch `833-review-evidence` (`review-evidence/833-r1/reviews/R76{3,4}-1/`, commit `4fe3e4e1`). Each archived report matches its comment except the verdict line on top.

## Commits

| Commit | Subject | Answers |
|---|---|---|
| `f91be3b5` | State the cleanup stages and the owner's clock that the head enforces in the testing guide | 1 |
| `bc2b30e7` | Derive a true survivor's deadline from the cleanup constants, worst case included | 2 |
| `21ee7746` | Say that a stalled owner fails the run only after its windows after SIGKILL on its own clock | 7 |
| `29df9272` | Control that a resumed shell's trap command keeps the shell's window | 3 |
| `1ff8292c` | Catch a stall charged to the deadlines in its own pass, keeping the product's whole window for the child's death | 4 |

5 and 6 are PR text, in `PR-BODY.md`. `scripts/owned_process.py` is unchanged, so every mutation anchor from round 1 still applies.

## Findings, each once with both IDs

| # | IDs | Change at file:line | Control / evidence |
|---|---|---|---|
| 1 | R763-1-F1, R764-1-F1 (MINOR, Docs) | `docs/testing/TESTING.md:223-228`: 2 s of SIGTERM; 2 s later SIGKILL reaches every other descendant; a descendant still listed 10 s after that fails the run; a resumed shell has 10 s for its trap; the deadlines run on the owner's clock, which one pass advances by at most 0.5 s. The old "two seconds ... another two seconds" lines are gone, so nothing on the page contradicts `owned_process.py:37-45,284-310` | Read against the code. Doc gates in docs.yml (below) |
| 2 | R763-1-F2, R764-1-F3 (MINOR, Docs / Docs+Robustness) | Stated the same way in `scripts/process_test_support.py:19-30`, `docs/testing/TESTING.md:229-235` and the PR body. Derivation: before any resume `limit = GRACE + KILL_ALL + REAP = 14`. The shell is resumed at most once, at `c_r < 14`, since at `c >= 14` with anything owned the verdict comes first. After that `kill_all = max(4, c_r + TRAP)` and `limit = c_r + 20 < 34`. The empty-owned branch waits `limit + REAP`, so under 44. The verdict fires in the first pass with `clock >= limit`, which is at most 0.5 s past it, since a pass adds `min(dt, 0.5)`. Wall time = owner clock plus whatever passes exceed 0.5 s. `FINISH_SECONDS = 60` covers 34.5 + 15.1 = 49.6 s and 44.5 + 15.1 = 59.6 s, both only while passes stay within 0.5 s. Not changed | `receipts/bounds/at-head/` (exact head clone, each probe in its own PID namespace): no resume 14.02 s; resume at about 2 s 22.03 s; resume at 13.5 s 33.51 s; at 13.9 s 33.92 s; R764-1 `probe_owner.py late-survivor` 32.54 s; empty listing, no resume, 24.01 s (= 14 + 10). The 44 s case is the same branch after a late resume, from the derivation; not probed. `receipts/bounds/` has the same probes on the working tree before commit 2 (identical `owned_process.py`) |
| 3 | R763-1-F4, R764-1-F2 (MINOR, Tests / Tests+Docs) | `scripts/test_suite_cancellation.py:542-579`: `owner_shell_window`'s trap also runs `sleep 1.5 && echo ran > trap-command-ran`, an external command longer than the pre-#833 1 s; new assertion at `:578`. `docs/testing/TESTING.md:273` lists it | Red, at this head, under R763-1 `trap-commands-1s` (1.8 s) and R764-1 `M07-trap-child-no-window` (0.8 s): `the resumed shell's trap command was killed inside the shell's window`. Green unmutated (2.3 s). The existing assertion still catches `no-shell-window`, `M05`, `M06` with its own words. `receipts/mutations/` |
| 4 | R763-1-F3 (MINOR, Tests+Robustness) | `scripts/test_suite_cancellation.py:505-539`: `REAP_SECONDS` is no longer shortened, so the child's window after SIGKILL is the product's 10 s, the value `owned_process.py:30-40` derives from the longest measured stall (7.96 s, above the 2.07 s D tail, a lower bound). Keeping the old shape (stall past every deadline) with a 10 s window would need an 11.2 s stall, and I tried it: the 5 s-cap mutant then stays green, since a capped stall can never jump past a 10 s window. So the control now catches the stall where it is charged. Grace 1.5 s is above the 1.0 s the cap lets pass 1 and the stalled pass 2 add, so at the head SIGKILL can never land in pass 2; a stall charged in full (wall clock, or any cap at least 1.5 s minus pass 1) sends it there. `stages` docstring `:407` no longer claims its controls do not depend on the stages | Red, at this head, under R763-1 `deadline-wall-clock`, `pass-cap-5s` and R764-1 `M03`, `M04` (2.1 s each): `the stall was charged in full: SIGKILL in pass [2]`. Green unmutated, `killed_in_pass` 27 in the sweep gate log. R763-1's own `probe_stall_window.py` at the exact head: PASS at 0, 1, 2, 2.3, 2.7, 3, 5, 9, 10 and 10.4 s of SIGKILL delay, FAIL at 11.0 s ("sent SIGKILL 10.51 s ago"). So the window is 10.5 s = KILL_ALL 0.5 + REAP 10. `receipts/stall-window/` |
| 5 | R764-1-F4 (MINOR, Docs), R763-1-X2 (RESIDUE) | PR body, Known limitations: only what three commands show, each named | `receipts/command-table/`: R764-1's `command_table_staleness.py` prints `pins 149 stale 34 absent 1` at `1f29f189`, 38 at `d4d8cff9` and at this head (the 4 more are this PR's 4 pinned scripts). `git grep -l -e command-table.json -e ci_command_table HEAD` lists 14 files. `git grep -n -F` for those 14 file names in `.github/workflows` and `scripts/run_all_suites.sh` prints nothing, rc 1. Round 1's "33 of 143" had no stated method, so I replaced it with the measured count and its command |
| 6 | R763-1-X1, R764-1-R1 (RESIDUE) | PR body before/after rows 1 and 2: "0 of 10, all at the fixture's 12 s hang bound, none `CLEANUP FAILED`" (and 0 of 18), covering both exact fixes | |
| 7 | R764-1-R2 (RESIDUE) | `docs/testing/TESTING.md:270`, R764-1's exact text | |

### Suggestions

| ID | Taken? | Reason |
|---|---|---|
| R763-1-S1, Issue for the stale command table | No | I may post only TAKEN / REVIEW READY / STOP on #833, and filing an Issue is the manager's step. The measured counts are in item 5 |
| R763-1-S2, record on #833 at merge where `Probe.ready`'s 15 s handshake belongs | No | A merge-time manager decision |
| R764-1-S1, a control on the 10 s values | No | A control pins a window only up to the delay it plants. Pinning the derived 10 s would add about 10 s to every sweep preflight, and a 3 s delay pins only "at least 3 s". `M15` stays green, as in round 1. Item 4's probe is evidence of the 10.5 s window, not a control |
| R764-1-S2, receipt for the 13 ms against 30 ms census figure | Receipt only | `receipts/census/census-cost.log` (`census_cost.py`): 1,403 processes, 200 interleaved passes, head median 17.4 ms (p90 20.4) against `dev` 37.6 ms (p90 45.1), at load about 21 to 29. Same ratio as the comment; the absolute values depend on the host. No code change |

## Mutation re-run at the new head

`receipts/mutations/matrix-table.md` (`matrix.py`, `matrix.json`, one log and rc per run): every mutant in both round 1 tables (R763-1's 14 including `none`, R764-1's 17 suite mutants) × the 7 owner controls, 217 runs, each in its own user and PID namespace, using R763-1's `run_control.py`. Matches both round 1 tables in every row. The only differences are the new reds above: `trap-commands-1s` and `M07` on `shell_window`; `deadline-wall-clock`, `pass-cap-5s`, `M03` and `M04` on `stall`. Still green, as in round 1 and for the reasons the reviews give: `M01`, `M01b` (halves of the identity fix; `M01c` red), `M14` (pre-existing safety), `M15` (the constants, S1), `killed-counts-as-gone` (the run still fails through the empty-owned path).

R764-1's own `mutate.py`, unchanged, on fresh clones of this head (`receipts/mutations-r764-driver/`, `summary.json` and one log and rc per entry). It runs the whole sweep test, or the lifecycle test, per mutant, in a user and PID namespace:

| R764-1 driver entry | Test | Round 1 expectation | At this head | Last line |
|---|---|---|---|---|
| control-A | suite | green | green, rc 0 | suite cancellation: PASS |
| control-B | suite | green | green, rc 0 | suite cancellation: PASS |
| control-lifecycle | lifecycle | green | green, rc 0 | mutant lifecycle: PASS |
| M01-identity-includes-parent | suite | red | green, rc 0 | suite cancellation: PASS |
| M01b-send-recheck-includes-parent | suite | probe | green, rc 0 | suite cancellation: PASS |
| M01c-identity-includes-parent-both | suite | red | red, rc 1 | AssertionError: re-parented descendant was treated as new and never got SIGTERM |
| M02-no-reap-after-census | suite | red | red, rc 1 | RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 5 (p |
| M03-wall-clock | suite | red | red, rc 1 | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M04-clamp-5s | suite | red | red, rc 1 | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M05-no-trap-window | suite | red | red, rc 1 | AssertionError: the shell was killed in the pass that resumed it, before its trap |
| M06-root-killed-unresumed | suite | red | red, rc 1 | AssertionError: the shell was killed in the pass that resumed it, before its trap |
| M07-trap-child-no-window | suite | probe | red, rc 1 | AssertionError: the resumed shell's trap command was killed inside the shell's window |
| M08-no-kill-before-fail | suite | red | red, rc 1 | AssertionError: stopped shell left behind |
| M09-kill-before-fail-spares-shell | suite | red | red, rc 1 | AssertionError: stopped shell left behind |
| M10-endless-unbounded | suite | red | red, rc 1 | AssertionError: cleanup never reached a verdict |
| M11-trust-sigkill | suite | red | red, rc 1 | AssertionError: a survivor never failed the run |
| M12-report-without-state | suite | red | red, rc 1 | AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.04 s start 74470409, not sent SIG |
| M13-cleanup-does-nothing-suite | suite | red | red, rc 1 | AssertionError: re-parented descendant was treated as new and never got SIGTERM |
| M13-cleanup-does-nothing-lifecycle | lifecycle | red | red, rc 1 | AssertionError: ('1307', ('74472239', 'S'), ('74472239', 'S')) |
| M14-no-start-recheck | suite | probe | green, rc 0 | suite cancellation: PASS |
| M15-windows-2s | suite | probe | green, rc 0 | suite cancellation: PASS |

A first attempt of this driver (`receipts/mutations-r764-driver-hup-ignored-attempt/`) ran under `nohup`, so SIGHUP was ignored in every child. The test's `hard-HUP` stop then cannot end the owner, and every run that got that far timed out at the fixture's 60 s bound: `control-A`, `control-B`, `M01`, `M01b`. So that was the harness, not the head. The rerun above does not ignore SIGHUP (`SigIgn` 0x4, SIGQUIT only, as in the tool shell). The per-control matrix also ran under `nohup`. None of the seven owner controls sends or expects SIGHUP (`grep -c HUP` over them gives 0), so I did not rerun it.

## Gates

All at head `1ff8292cd5b761633ef9500a7c5a4b1626a3d92c`. Each gate has one log and one rc, never piped. The lane gates ran on a clean clone (`lane.sh`, `tree-after.txt` empty with `--ignored`).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` (round 1's `run_docs_yml.py` and `verify_docs_yml.py`, paths pointed at this lane's scratch, own venv identical to round 1's freeze) | 0 | Verifier: 64 steps rc 0, 31 not run with round 1's reasons (`not_run.json` unchanged), 0 bad. `git status` clean after each job. Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. The run did not ignore SIGHUP (relaunched; the first run is in incidents) | `receipts/gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/` (`gate_41`'s log is over 200 KB: sha256 and size in `lane/LARGE-LOGS.txt`, tail in `docsyml/`) |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; `killed_in_pass 27`; `trap_command_ran True` | `receipts/gates/lane/test_suite_cancellation.*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `receipts/gates/lane/lifecycle.*` |
| Mutation re-run (per control, 217 runs; R764-1's driver, 21 entries) | n/a | Every round 1 row reproduced. New controls red under their reverts, green unmutated | `receipts/mutations/`, `receipts/mutations-r764-driver/` |
| R763-1 stall-window probe (F3's verification) | n/a | PASS at delays up to 10.4 s, FAIL at 11.0 s | `receipts/stall-window/` |
| Survivor-bound probes (F2's verification) | 0 each | 14.02, 22.03, 33.51, 33.92, 32.54 s; empty listing 24.01 s | `receipts/bounds/at-head/` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `receipts/gates/lane/behave.rc`, `behave-tail.txt`; log over 200 KB: `LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `receipts/gates/lane/diffcheck.*` |
| Full sweep | not run | Round 2 touches only `docs/testing/TESTING.md`, `scripts/process_test_support.py` and `scripts/test_suite_cancellation.py`, all changed by round 1 | |
| `check_py_idiom.py` (also inside docs.yml) | 0 | all ratchets within budget | run in the lane before the gates |

Hosted contexts and the `act` replay were not run (the manager's bank).

## Incidents, no harm

- The first sweep-test run in the gate clone ran with the behave venv's Python first on PATH. That Python lacks the pidfd calls, so the owner refused (`Unsupported: os.pidfd_open, signal.pidfd_send_signal`, rc 1). I moved that venv onto PATH for behave only and reran; the receipt is the rerun. The refused run started no command.
- docs.yml's RV32 SDK step failed `SDK provenance mismatch` on the first run: I had copied round 1's HOME, and the relocated SDK's receipt is bound to its install path. I stopped that run by its own process group (checked to be in this unit's cgroup), deleted the copied SDK and the run directory, and reran every job from a fresh clone with a fresh hash-checked install. The receipts are the rerun.
- `python3 -I` ignores `PYTHONDONTWRITEBYTECODE`, so my first probes left `scripts/__pycache__/owned_process.cpython-314.pyc` (ignored by git) in the lane. I removed that one file; the older ignored caches there predate this session. Later runs use `-B`.
- Nothing was signalled by name. Everything I started ran in this unit, and long runs were detached in their own process groups.
