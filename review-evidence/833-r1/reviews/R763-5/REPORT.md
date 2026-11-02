[R763] NEGATIVE - exact head a67eaf66c99b6b07c7ef206ad3489cb9555e00ca

# R763-5: internal cleared-context review of PR #834 (issue #833), round 5

- Head: `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca`, tree `433c822f557ad40546a462a97a902b4a59d8f399`. PR #834 is not a draft and targets `dev`.
- Round 5 delta: `c1b29617..a67eaf66`, 5 one-line commits with empty bodies. They touch `docs/testing/TESTING.md` (+12/-2), `scripts/process_test_support.py` (+231) and `scripts/test_suite_cancellation.py` (+170/-23).
- `scripts/owned_process.py` is byte-identical to round 4 (`git diff --quiet c1b29617 HEAD -- scripts/owned_process.py`).
- Verdict basis: one MAJOR and two MINOR findings are open, and all three are new in this round. Prior findings are resolved except one retained RESIDUE.

## Scope reconstructed

Sources, read in this order: AGENTS.md, the issue #833 body and comments, the PR body (`receipts/pr-body-at-review.md`), the delta, and then the prior public reviews (read only after my own pass over the diff).

- **Frozen acceptance.** (1) The failure message prints each descendant's `/proc/<pid>/stat` state. (2) From that evidence, a fixed deadline or a real fix, "with no suite left to fail by chance".
- **Round 5 scope** (`[A726e] TAKEN`):
  - Close the class behind R764-4-F1: every published mutant runs against every owner control.
  - A stated cleanup behaviour that a published mutant broke gets a control.
  - The mutant list is committed beside the preflight.
  - R764-4-S1 (the margin) and R764-3-R1 (the comment).
  - No product change.

## Focus checks

**(1) Every published mutant is in the committed list and red on a named control at this head: CONFIRMED.**
- `MUTANTS` (`scripts/process_test_support.py:261-414`) holds 43 mutants plus `none`. I checked it against the published tables:
  - R763-1 (§2 table);
  - R764-1 M01-M15, with M01 = `identity-first-census-holds-parent`, M01b = `send-checks-parent`, M14 = `no-start-recheck` and M15 = `windows-2s`;
  - R763-2's 14;
  - R764-2's M04c, M04d and M07b;
  - R764-3's M16, M16b and M16c;
  - round 1's own `author/receipts/mutations/`.
- I also compared the edit text of the two latest reviewer files (`reviews/R763-3/scripts/mutants.py`, `reviews/R764-4/scripts/mutants.py`) edit by edit. Every one maps to a committed entry with the same edit, for example `listing-unbounded` = `endless-unbounded` and `new-fix-census-not-owned` = `resume-while-listed`.
- `python3 scripts/test_suite_cancellation.py --mutants --jobs 16` at this head: rc 0, `owned-process mutants: PASS (43 mutants, 42 with a control that must fail)`, 36.9 s (`receipts/committed-mutants.log`).
- The full `--matrix` (484 runs, `receipts/committed-matrix.log`) has every named control red with its words. Its only FAIL is `none / whole`, a `hard-HUP` timeout. That is my launcher's artifact: it ignored SIGHUP, the same artifact R764-2 recorded. The whole test from a `none` tree, launched with SIGHUP at default, passes: rc 0, 60.1 s (`receipts/whole/none.*`). See S1.
- `sigterm-checks-parent` names no control. Its stated reason holds: pass 1 builds `initial` from the same census, and `notified` suppresses any later SIGTERM.

**(2) R764-4-F1: `shell-window-one-pass` is red: CONFIRMED.**
- Red on `owner_shell_window` 6/6 with "the resumed shell was killed inside its own window, with no child to spare it".
- `shell-window-1s` is red 6/6 with the same words, and `none` is green 6/6 (`receipts/repeat/`, load about 43).
- Both are also red on `owner_stated_seconds`.
- The FIFO tail is sound: `read -t 0.3 <> idle` opens read-write, so it never blocks on open. It times out in a builtin with no child, and `; echo done` runs after it.

**(3) `owner_stated_seconds` pins the stated seconds: CONFIRMED for what `TESTING.md:278-279` lists, NOT for `:224` (F1).**
- I checked the expected events against `owned_process.py:260-339` by hand. On the starved clock pass n is at (n-1)/2 s:
  - SIGKILL to a leaf at pass 5, 2 s (`:223`);
  - verdict at pass 29, 14 s (`:225`, `:229`);
  - resume at pass 12 sets `kill_all` = 15.5 s, and the shell and its trap command are killed at pass 32 (`:226`, `:230`);
  - verdict at pass 52, 25.5 s = resume + 20 (`:230`);
  - the verdict lands exactly on its pass (`:233`), and the cap shows in the pass arithmetic (`:228`, `:269`).
- `:232` ("waits 10 s more") is pinned incidentally. My mutant `r5-vanishing-fails-at-limit` is red on `owner_late_exit`.
- `:224` ("Two seconds later `SIGKILL` has reached every other descendant") is not pinned. Both listings in the control hold only leaves and the shell. See F1.

**(4) Nothing was narrowed: CONFIRMED. `TESTING.md:281` states the rule: CONFIRMED, but the rule is not yet true (F1, F2).**
- The TESTING.md changes only add text or widen it ("in that pass", "even in that pass", `:274`, `:278-285`, `:309`).
- The docstrings widen in the same way.

**(5) Preflight cost: CONFIRMED, about +1.4 s** (`receipts/control-timings.txt`, load about 106-112).

| Control | This head | Round 4 head (author `cost.txt`) |
|---|---:|---:|
| `owner_shell_window` | 4.50 s | 3.3 s |
| `owner_stated_seconds` | 0.14 s | new |
| `owner_reused_identity` | 0.12 s | new |
| `owner_reparented` | 0.26 s | 0.26 s |
| `owner_late_cancel` | 0.96 s | 0.95 s |

- The whole test takes 60.1 s here, against the author's 54.7 s.
- No deadline was raised.
- On a slow owner, though, the 61-pass hold costs up to 12.9 s and then fails the control. See F3.

**(6) R764-4-S1 and R764-3-R1.**
- **R764-3-R1: resolved verbatim** at `scripts/test_suite_cancellation.py:683`.
- **R764-4-S1: the lower bound is derived and correct.** Each pass ends in `time.sleep(0.02)` (`owned_process.py:339`), and `min(now - last, 0.5)` (`:284`) is at least 0.02 s. So pass 61 is at 1.2 s or later, and the resume is at pass 62 or later, at 1.22 s or more. That is past `deadline + 1.0` = 1.2 s (`:327`).
- **The fix also adds a defect.** A hold counted in passes has no upper bound on the owner's clock, and the control's verdict comes at 10.4 s of it. See F3.

## My own mutants against the committed list

`add_mutants.py` appends six mutants to a disposable copy of the tree. I ran them on every owner control and on the whole test (`receipts/reviewer-matrix.log`; whole test re-run with SIGHUP at default in `receipts/whole/`).

| Mutant | Edit | Stated behaviour it breaks | Result at this head |
|---|---|---|---|
| `r5-parent-with-live-child-spared` | `elif clock < kill_all:` -> `elif clock < kill_all or any(<live child>):` | `TESTING.md:224` | **green on all 10 controls and the whole test (F1)** |
| `r5-parents-killed-at-grace` | the two leaf-first `continue` rules removed (`owned_process.py:327-330`) | the staged order in `:223-224` | **green on all 10 controls and the whole test** (F1, same class) |
| `r5-report-without-current-parent` | `parent {fields[1]} ` removed from `_describe` | `:277` "... parent and age" | **green on all 10 controls and the whole test (F2)** |
| `r5-report-age-in-ticks` | age not divided by `SC_CLK_TCK` | `:277` "... and age" | **green on all 10 controls and the whole test (F2)** |
| `r5-vanishing-fails-at-limit` | `(owned or clock >= limit)` | `:232` "waits 10 s more" | red: `owner_late_exit`, whole |
| `r5-resume-with-one-live` | resume while one other descendant lives | not stated (informative) | red: `owner_stated_seconds`, whole |

## Findings

**R763-5-F1: MINOR. Lenses: Tests, Docs.** No control pins the second cleanup stage at `docs/testing/TESTING.md:224`, but `TESTING.md:281` and the PR body say it is pinned.
- **Authority and evidence.**
  - `:224` reads: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell, which keeps its own window."
  - `:281` reads: "A stated cleanup behaviour is one some control pins."
  - The PR body's Round 5 table lists `TESTING.md:223-232` as pinned by `owner_stated_seconds`.
  - AGENTS.md §6 Tests: "Each new test can fail for the defect it claims to detect."
- **Mutants.** Two mutants survive all 10 owner controls and the whole test (`receipts/reviewer-matrix.log`, `receipts/whole/`):
  - `r5-parent-with-live-child-spared` spares a parent with a live child past `kill_all`;
  - `r5-parents-killed-at-grace` kills parents at grace together with the leaves.
- **Probe.** `kill_all_probe.py` uses the head's own `starved_clock` and `starved_cleanup` on a stubborn parent whose child outlives SIGKILL (`receipts/probes/kill-all-*`):

  | Tree | Parent's first SIGKILL |
  |---|---|
  | Head | pass 9, 4 s, as `:224` states (rc 0) |
  | `r5-parent-with-live-child-spared` | pass 29, only in the verdict's final kill (rc 1) |
  | `r5-parents-killed-at-grace` | pass 5, 2 s, together with its leaf (rc 1) |

- **Impact.** A parent whose child sits in D state (the 1.91 s and 3.04 s episodes in `owned_process.py:30-36`) would get no SIGKILL until its child left D or the run failed. It could then still be dying at 14 s, so a clean run would fail by chance, and no gate would see the regression. The product is right today; the gap is in the controls and in the claim that they pin `:224`.
- **Required outcome.** Either of these:
  - A control fails when a non-leaf descendant other than the cancelled shell, whose child stays live, is not sent SIGKILL at 4 s on the owner's clock: neither before (if `:223-224` mean the staged order) nor after. It goes red under both mutants, and both join `MUTANTS` with its words.
  - Or `:224`, `:281` and the PR body state only what is pinned.
  - One extra listing in `owner_stated_seconds` would do it, at about zero preflight cost. This is not prescribed.
- **Verification.** `python3 scripts/test_suite_cancellation.py --mutants` stays PASS with both mutants added. `kill_all_probe.py <tree>` gives rc 0 at the head and rc 1 on each mutant.

**R763-5-F2: MINOR. Lenses: Tests, Docs.** The failure message's parent and age are asserted only by presence, so `TESTING.md:277` is not pinned.
- **Authority and evidence.**
  - `:277` reads: "That message prints each remaining process's scheduler state, wait channel, parent and age." `:281` says each stated behaviour is pinned.
  - `owner_report` (`scripts/test_suite_cancellation.py:444-445`) asserts `f"parent {os.getpid()}"` and `" age "`. The first is satisfied by the separate `(first parent {pid})` text, which still contains `parent {pid}`. The second is satisfied by any number.
  - `owner_survivor` (`:652`) asserts only `"parent "` and `" age "`.
- **Mutants.** `r5-report-without-current-parent` and `r5-report-age-in-ticks` are green on all 10 controls and the whole test.
- **Probe.** `report_probe.py`, on a 0.3 s old child (`receipts/probes/report-*`):

  | Tree | Message |
  |---|---|
  | Head | `parent <pid> (new since the first census) age 0.30 s` (rc 0) |
  | `r5-report-without-current-parent` | no current parent at all, both for a process new since the first census and for a re-parented one (rc 1) |
  | `r5-report-age-in-ticks` | `age -75904308.51 s` (rc 1) |

- **Impact.** The current parent is what tells re-parenting and reap order apart. Round 1's cause table rests on it: 8 of 12 `state Z` entries had the owner itself as parent. The age is what tells a slow death from a new process. Either one could regress silently while `:277` says a control pins it.
- **Required outcome.** Either of these:
  - `owner_report` (or another control) asserts the current parent as its own field, distinct from the first parent, and an age consistent with the process's real age. Both mutants go red and join `MUTANTS` with the words.
  - Or `:277` and `:281` are narrowed to what is pinned.
- **Verification.** The `--mutants` campaign stays PASS with both added. `report_probe.py` gives rc 0 at the head and rc 1 on each mutant.

**R763-5-F3: MAJOR. Lenses: Conformance, Robustness, Tests.** The new 61-pass hold makes the preflight control `owner_shell_window` fail by chance on a slow owner.
- **Authority and evidence.**
  - Issue #833 acceptance 2: "with no suite left to fail by chance".
  - `TESTING.md:255-262`: the sweep's normal preflight runs these controls, and "Command handshakes establish signal boundaries without timing guesses".
  - `owned_process.py:41-42` records census passes of 1.75 s at 16 runnable tasks per CPU.
- **Cause.**
  - `scripts/test_suite_cancellation.py:585` refuses the child's SIGKILL until census pass 61. The guard counts passes, and it applies to every SIGKILL, including the one the verdict sends.
  - The control runs with `GRACE_SECONDS=0.2` and `KILL_ALL_SECONDS=0.2` (`:568`), so the verdict comes at `kill_all + REAP_SECONDS` = 10.4 s of owner clock (`owned_process.py:289-301`).
  - Once passes average more than about 10.4 / 59 = 0.18 s, the owner reaches 10.4 s before pass 61. The child is still refused SIGKILL, and the run raises `CLEANUP FAILED` instead of `Cancelled`.
  - The round 4 control held the child for 1.5 s of wall time, so it could not reach the verdict. The round 5 change bounds the resume from below only.
- **Probe.** `slow_census_probe.py` runs the tree's own `owner_shell_window` with each census pass slowed by a fixed sleep (`receipts/slow-census2/`):

  | Added per pass | This head | Round 4 head `c1b29617` |
  |---:|---|---|
  | 0.10 s | PASS (10.7 s) | — |
  | 0.12 s | PASS (12.2 s) | — |
  | 0.15 s | **FAIL**: `CLEANUP FAILED: owned descendants remain after 10.55 s, 56 census passes, slowest 0.17 s` | PASS (3.8 s) |
  | 0.20 s | **FAIL** | PASS (4.3 s) |
  | 0.30 s | **FAIL** | PASS (4.8 s) |

- **Impact.** At census passes of about 0.17 s or more, the sweep's preflight fails with a cleanup failure, although the product is right. That is about 4 times what I measured at load 106 here (0.04 s a pass), and an order of magnitude below the 1.75 s the PR documents. It is the failure class #833 exists to remove, now in the gate that runs before every sweep. The PR body's "however the owner stalls" holds only for the lower bound.
- **Required outcome.**
  - The control's hold must be bounded on both sides of the owner's clock. The resume must stay past `deadline + 1.0`, and the unmutated control must not be able to reach its verdict before the child is released, at any pass time up to the 0.5 s cap.
  - One option, not prescribed: a `REAP_SECONDS` stage longer than 61 × 0.5 s, so the verdict cannot precede pass 61.
  - Detection must be kept: `shell-window-one-pass`, `shell-window-1s`, `shell-killed-when-resumed`, M05, M06, `no-trap-window` and `trap-commands-*` stay red.
- **Verification.**
  - `slow_census_probe.py <tree> 0.15|0.2|0.3|0.5`: PASS at the new head.
  - `--mutants`: PASS.
  - `owner_shell_window` green repeatedly unmutated, and red under `shell-window-one-pass`.

**R763-5-S1: SUGGESTION. Lenses: Tests.** The explicit campaign inherits the launcher's SIGHUP disposition.
- `run_mutant` (`scripts/process_test_support.py:430-445`) starts each run with the caller's signal mask. Under a launcher that ignores SIGHUP, `--matrix` reports `none / whole` as FAIL in `hard-HUP` (`receipts/committed-matrix.log`, `receipts/reviewer-matrix.log`), although the head is right.
- R764-2 hit the same artifact. Long campaigns are commonly started that way.
- Optional: reset SIGHUP to its default in the run's child, or refuse with a clear message when it is ignored.

**R763-4-X1: RESIDUE (retained, not taken, not listed in the PR body's Round 5 residue table). Lenses: Docs.**
- `TESTING.md:224` still omits the trap's commands from its exception.
- Exact fix, as in R763-4: "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell and any command its trap started, which keep the shell's own window."
- If F1 is answered by rewording `:224`, merge the two.

**Comment rule.** No new RESIDUE in the delta. The added comments and docstrings cite `#833` only, and carry no lane label, lane name, review round, reviewer ID or comment ID. "the next reviewer's mutant" at `TESTING.md:284` names a role. All five commit subjects are one line with empty bodies.

## Prior findings at their cause, at this head

The product file has been unchanged since `3740565f`, so findings fixed in code at earlier heads stay fixed. Each is re-evidenced by the committed campaign here.

**Resolved:**

| Finding | Evidence at this head |
|---|---|
| R763-1-F1..F4, R764-1-F1..F4 | `trap-commands-*`, `deadline-wall-clock` and `pass-cap-*` red on their controls |
| R763-2-F1 = R764-2-F1 | `resume-collected-shell` red on `owner_late_cancel` |
| R763-2-S1 (10 s windows unpinned) | `windows-2s` and `reap-window-2s` red on `owner_stated_seconds` |
| R764-2-S1 (cap pinned only above 1.5 s) | `pass-cap-1s` red |
| R763-3-F1 | `shell-killed-when-resumed` red |
| R763-3-S1, R764-4-S2 | `resume-while-listed` red on `owner_late_cancel` |
| R764-3-R1 | `:683` verbatim |
| R764-4-F1 | (2) above |

**Retained:**
- R763-4-X1 (RESIDUE, above).
- R763-4-S1 / R764-4-S1: the lower margin is resolved, and the upper side is now F3.
- R763-2-S2 (manager actions R763-1-S1/S2) and R763-2-S3 (the census-cost comment figure), both carried to the manager.
- Round 1-2 RESIDUE (R763-1-X1/X2, R764-1-R1/R2, R763-2-X1/X2, R764-2-R1/R2): resolved in rounds 2-4, as recorded by R763-4. The texts at `TESTING.md:224`, `:230` and in the PR body read as fixed.

## Lens results (each with its artifact, at head a67eaf66)

```text
[R763] MAJOR Conformance — scripts/test_suite_cancellation.py:568,585 vs scripts/owned_process.py:284,289-301; issue #833 acceptance 2 — R763-5-F3: preflight control fails by chance at census passes ≥ ~0.17 s (receipts/slow-census2/)
[R763] PASS RTL — git diff --stat 1f29f189..a67eaf66 (Python/Markdown only, no HDL, constraint or synthesis file); scripts/owned_process.py byte-identical to c1b29617 and 3740565f — cleanup state machine re-checked against the delta's new controls: stages at pass 5/9/29 and 12/32/52 on the starved clock match :260-339 (receipts/probes/kill-all-head.log, control-owner_stated_seconds.log); the prior verdict stands
[R763] MAJOR Robustness — scripts/test_suite_cancellation.py:585 (pass-counted hold with no owner-clock upper bound) — R763-5-F3 (head FAIL at +0.15/0.20/0.30 s a pass; round 4 PASS)
[R763] MAJOR Tests — scripts/test_suite_cancellation.py:552-603 — R763-5-F3
[R763] MINOR Tests — scripts/test_suite_cancellation.py:761-796 (owner_stated_seconds), :435-456 (owner_report), :652 — R763-5-F1, R763-5-F2 (four surviving reviewer mutants, receipts/reviewer-matrix.log, receipts/whole/)
[R763] MINOR Docs — docs/testing/TESTING.md:224,277,281; PR body Round 5 table row "TESTING.md:223-232" — R763-5-F1, R763-5-F2 (the stated rule at :281 is not yet true); retained RESIDUE R763-4-X1
```

Clean parts within the unclean lenses, for the next round's scope:
- **Tests.** The committed list is complete and its campaign passes (`receipts/committed-mutants.log`). `owner_reparented`, `owner_late_cancel`, `owner_reused_identity` and the F1 tail of `owner_shell_window` are sound.
- **Docs.** `TESTING.md:269-285` and `:309` are accurate apart from `:281`'s reach. The doc gates pass (`receipts/gates/summary.txt`: `docs_check.py`, `check_doc_style.py`, `check_baremetal_only.py --check`, `check_py_idiom.py`, `git diff --check 1f29f189 HEAD`, all rc 0).

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | issue #833 acceptance 1-2; `TESTING.md:223-235,255-285`; `owner_shell_window` vs `owned_process.py:284-301`; `receipts/slow-census2/` | R763-5 | a67eaf66c99b6b07c7ef206ad3489cb9555e00ca |
| RTL | CLEAN | diff stat (no HDL); `owned_process.py:256-339` byte-identical; `receipts/probes/kill-all-head.log` | R763-5 | a67eaf66c99b6b07c7ef206ad3489cb9555e00ca |
| Robustness | UNCLEAN (F3) | `test_suite_cancellation.py:552-603`; `receipts/slow-census2/`, `receipts/repeat/`, `receipts/control-timings.txt` | R763-5 | a67eaf66c99b6b07c7ef206ad3489cb9555e00ca |
| Tests | UNCLEAN (F1, F2, F3) | `MUTANTS` and campaign (`process_test_support.py:261-487`); all 10 owner controls; `receipts/committed-*.log`, `receipts/reviewer-matrix.log`, `receipts/whole/`, `receipts/probes/` | R763-5 | a67eaf66c99b6b07c7ef206ad3489cb9555e00ca |
| Docs | UNCLEAN (F1, F2) | `TESTING.md:223-235,269-285,309`; PR body Round 5 (`receipts/pr-body-at-review.md`); source comments in the delta; `receipts/gates/` | R763-5 | a67eaf66c99b6b07c7ef206ad3489cb9555e00ca |

## Executed (each with its own log and rc, under `receipts/`)

| Run | Result |
|---|---|
| Each owner control alone at the head (`control-*.log`, `control-timings.txt`) | all rc 0 |
| `--mutants --jobs 16` at the head | rc 0, PASS |
| `--mutants --matrix --jobs 8` at the head | rc 1, only `none / whole` under the SIGHUP-ignoring launcher (S1) |
| Reviewer mutants: `add_mutants.py` + `--mutants r5-* --matrix --jobs 8` on a disposable copy | rc 1, same `none / whole` artifact; survivors as tabled |
| Whole test from mutant trees with SIGHUP at default (`make_trees.py`, `run_whole.sh`; `receipts/whole/`) | `none` and the four survivors all rc 0, about 60 s each |
| `owner_shell_window` × 6 under `none`, `shell-window-one-pass` and `shell-window-1s` (`receipts/repeat/`) | 6/6 green, 6/6 red, 6/6 red |
| `kill_all_probe.py` and `report_probe.py` at the head and on the mutants (`receipts/probes/`) | see F1 and F2 |
| `slow_census_probe.py` at the head and at `c1b29617` (`receipts/slow-census2/`) | see F3 |
| Doc and idiom gates (`receipts/gates/`) | all rc 0 |
| Hosted state (`receipts/hosted.txt`) | 0 check runs and 0 status contexts at this head |
| Clone integrity (`receipts/clone-integrity.txt`) | below |

- A first slow-census attempt was discarded and is not published. That probe caught its own `SystemExit`, so its rc files were wrong; its PASS and FAIL lines matched the re-run.
- **Clone integrity.** The worktree and index equal HEAD; index mode, blob and path equal the HEAD tree; the six submodule gitlinks are unchanged. A `scripts/__pycache__/` created by my `make_trees.py` import at 17:30:33 was removed, and the tree was re-verified clean.

## Real limits

- No user or PID namespaces were used. Mutant runs ran under the campaign's own outer owner and under my shell. Host load was 43-112 on 16 CPUs, from other tenants.
- F3's threshold was found by slowing the census with a sleep, not under real load. I did not measure the host load at which real census passes reach 0.17 s. The PR's own 1.75 s figure is the evidence that such passes occur.
- Not run: the full sweep, `make -C tb/verilator/gptp_shadow lifecycle`, `cd tests && behave`, and every `run:` step of `docs.yml` (only the five gates listed). The delta does not touch the lifecycle test or the product.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Hosted and act acceptance at the exact head. No hosted check run exists yet.
- The current-dev merge candidate (source base `1f29f189279f9fc0132f4918e47342b87d22f33a`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`), with builder and native banks, at the merge turn.
- Carry the residue checklist: R763-4-X1.
- Carry suggestions R763-2-S2 (R763-1-S1/S2) and R763-2-S3.
- After F1-F3 are answered, a re-review at the new head covering every lens.

R763-5 FINISHED
