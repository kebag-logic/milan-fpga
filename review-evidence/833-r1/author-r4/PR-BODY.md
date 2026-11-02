[A726d]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Round 2](#round-2)** — Each round 1 finding with both review IDs, its change, its control and the gates.
- **[Round 3](#round-3)** — Round 2's one finding with both review IDs, the code fix, its control and the gates.
- **[Round 4](#round-4)** — Round 3's one test gap, its control, the wording residue and the gates.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally. `833-owned-process` -> `dev`, head `c1b2961777809403bd2de833ec1fa00c75394d6c` (round 4). Round 4's gates are in [Round 4](#round-4). The full sweep ran at round 1's head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`: 65 of 65 suites, 2,191,394 checks, 0 failures. Rounds 2 to 4 change only files round 1 changed, so the sweep was not rerun. Hosted contexts not yet run.

## Linked Issue / roles

Relates to #833

Executor: `[A726]` (round 1), `[A726b]` (round 2), `[A726c]` (round 3), `[A726d]` (round 4)
Internal cleared-context reviewer: `[R763]`
External reviewer: `[R764]`

## Description

**No descendant ever survived SIGKILL.** `CLEANUP FAILED` fired on dead processes and on ones the owner had not got round to signalling. The failure message now prints each remaining process's state, wait channel, parent and age, which names the cause. Of 12 messages captured on the pre-fix tree:

| Count | Message shows | Which it is | Load |
|---:|---|---|---|
| 8 | `state Z`, parent = the owner | A zombie whose reaper is the owner that is raising | CPU overload |
| 1 | `bash state T wchan do_signal_stop`, not sent SIGKILL, child `state Z` | A shell the owner has not yet resumed | CPU overload |
| 3 | `state D` in `dup_mmap`, `unlink_file_vma_batch_process`, `__mmap_region`, up to 2.07 s after SIGKILL | Uninterruptible sleep | 10 real builds, host load about 250 |

The faults and their fixes, in `scripts/owned_process.py`:

| Fault | Evidence | Fix |
|---|---|---|
| Census, then raise, with no reap between | Zombie of the owner in the message | Collect after the census, before judging. Only a census after a reap proves nothing remains |
| The parent was part of a process's identity | A re-parented descendant counted as new and never got SIGTERM: 3.165 s of cleanup with 1 ms census passes, 10 of 217 cleanups on 4 busy CPUs | Identity is the start time |
| The owner's own time was charged to the descendants | The protocol needs 2 s + 4 passes, and a pass reached 1.75 s at 16 runnable per CPU. The same load in a PID namespace, census 1 ms: 20 of 20 pass | Deadlines on a clock a pass advances by at most 0.5 s. A direct-call census at under half the cost |
| A shell could get SIGCONT and SIGKILL in one pass; a raise could come with no SIGKILL sent | Traced | A resumed shell has its own window. SIGKILL everything before raising |
| The window was shorter than a measured stall | Below | The windows are derived |

**The deadline's derivation.** 121,660 direct kills timed through a pidfd at host load up to 111: longest 0.23 s. But 2.07 s in D at load 250, and host-wide stalls of 3.04 s and of 7.96 s (four process starts at one moment), whose cause is not named. So the tail comes in episodes, and each window after a signal is 10 s, to outlast the longest measured. A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock. After a resume, every remaining descendant's deadline is 20 s after the resume, including one the trap started. That resume comes before 14 s, so this deadline comes under 34 s. A listing that dies inside every census waits 10 s more: under 44 s. The run fails in the first census pass at or past the deadline. That pass adds at most 0.5 s of owner clock. Wall time runs ahead of the owner's clock only while a pass takes longer than 0.5 s. The fixture's hang bound goes from 12 s to 60 s: one real driver takes 12.7 to 15.1 s under load (n = 24), and this is four times that. With the driver's 15.1 s on top that is 49.6 s, or 59.6 s for the listing: both inside 60 s while passes stay within 0.5 s. It bounds a hang, never a property under test. No assertion is weakened.

**Before and after, at this head.** Before is this branch's first commit, `dev` plus only the message. Both trees ran at the same moment on the same CPUs.

| Test | Load | Before passes | After passes |
|---|---|---:|---:|
| `make -C tb/verilator/gptp_shadow` | 10 real builds + 48 spinners, 12 CPUs | 0 of 10, all at the fixture's 12 s hang bound, none `CLEANUP FAILED` | 10 of 10 |
| `make -C tb/verilator/gptp_shadow lifecycle` | 12 concurrent + 48 spinners, 12 CPUs | 0 of 18, all at the fixture's 12 s hang bound, none `CLEANUP FAILED` | 18 of 18 |
| `scripts/test_suite_cancellation.py` | The same | 11 of 12 | 12 of 12 |
| Real cancellation cases, focused | 192 spinners on 12 CPUs, host load 250 to 314 | 4 of 10, 4 `CLEANUP FAILED` | 6 of 10, 0 `CLEANUP FAILED`, all 4 at the handshake bound before any cleanup |

Eight controls join the sweep's preflight in `scripts/test_suite_cancellation.py`. Each fix reverted alone turns its control red, including a planted survivor that must fail the run and take its stopped shell with it.

| Touched | Why |
|---|---|
| `scripts/owned_process.py` | The fixes above |
| `scripts/process_test_support.py` | `FINISH_SECONDS` |
| `scripts/test_suite_cancellation.py` | The controls; the timeout control's bound, and one 5 s wait, each below a measured stall |
| `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` | One 5 s wait below a measured stall |
| `docs/testing/TESTING.md` | The contract |

## Authoritative references

- #833 and its acceptance
- `AGENTS.md` sections 5 and 8
- `docs/testing/TESTING.md`, the sweep's cancellation controls

## How to get into the same state

```sh
git fetch origin 833-owned-process
git checkout 833-owned-process
git submodule update --init third_party/verilog-axis gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 scripts/test_suite_cancellation.py
make --no-print-directory -C tb/verilator/gptp_shadow
git diff --check origin/dev...HEAD
```

To see the cause on the first commit of this branch, run `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` beside CPU load or real builds on your own booked CPUs: the failure names the state of each remaining process.

Expected result / pass criteria: `suite cancellation: PASS`, whose log prints the planted survivor's `CLEANUP FAILED` line with `state`, `wchan`, `parent` and `age`; `mutant lifecycle: PASS`; `RESULT: PASS`; `git diff --check` silent.

Local evidence at this head: every `run:` step of `docs.yml`, as in [Round 4 gates](#round-4-gates); `behave` 2330 steps passed. The full sweep ran in 4 shards, rc 0, at round 1's head.

## Known limitations / out of scope

- **"No suite left to fail by chance" is not absolute, so this is `Relates to`, not `Closes`.** `Probe.ready`'s 15 s handshake is the next bound: it tripped 4 of 10 after this change, at 16 runnable per CPU and host load 250 to 314, with no ownership failure in them. It is not changed here.
- **The host stalls' cause is not named.** They did not recur in 703 cleanups with a sidecar at load near 30. The D wait channels are mapping-lock paths, so contention on mappings shared across the host is an inference, with no kernel trace behind it. A stall beyond 10 s would still fail, naming the state.
- **The #828 replay cannot be classified:** its log has the old message.
- **`owner_survivor` drops SIGKILL at the owner's send,** since no unprivileged control can build an unkillable process.
- **A stuck-process cancellation now fails the run under 34 s of owner clock (44 s for a listing that dies inside every census), not 4 s,** as derived above. The preflight is about 11 s longer, for the timeout control's 10 s, round 2 adds about 1.5 s, the trap command's, round 3 adds 0.8 s, the late-cancel control's, and round 4 adds 0.8 s to the shell-window control.
- `ci/image/command-table.json` pins these scripts' hashes and is not regenerated. What commands show, at this head:
  - `python3 -I command_table_staleness.py . 1f29f189 d4d8cff9 HEAD`, with R764-1's script from `review-evidence/833-r1/reviews/R764-1/scripts/` on branch `833-review-evidence`, prints `pins 149 stale 34 absent 1` for `dev` `1f29f189`, and `stale 38` for round 1's head and for this one. The 4 more are the 4 scripts this PR changes, which the table pins.
  - `git grep -l -e command-table.json -e ci_command_table HEAD` lists 14 files that read or name the table, among them `ci/image/build.py` and `scripts/ci_command_table.py`.
  - `git grep -n -F` for each of those 14 file names, `-- .github/workflows scripts/run_all_suites.sh`, prints nothing (rc 1). No workflow or sweep step names a reader of its script pins.
  - Regenerating the table would also rewrite the 34 pins already stale on `dev`, so it is left alone.

## Round 2

Round 1's reviews, R763-1 and R764-1, are both NEGATIVE on `d4d8cff92658e57b11090c97daf7b44edb31b3b6` with MINOR findings only. Round 2 answers each finding once, with both IDs where the two reviews overlap. `scripts/owned_process.py` is unchanged: every round 2 commit is a test, a comment or documentation.

| Finding | IDs | Change | Control or evidence |
|---|---|---|---|
| The guide states the old cleanup timing | R763-1-F1, R764-1-F1 | `docs/testing/TESTING.md:223-228` states the stages at this head: 2 s of `SIGTERM`, `SIGKILL` to every descendant 2 s later, a verdict 10 s after that, 10 s for a resumed shell's trap, on the owner's clock that a pass advances by at most 0.5 s | Read against `scripts/owned_process.py:37-45,284-310` |
| A true survivor's time to fail the run was stated as up to 24 s | R763-1-F2, R764-1-F3 | Derived from the constants and stated the same way in `scripts/process_test_support.py:19-30`, `docs/testing/TESTING.md:229-235` and this body: 14 s, under 34 s after a late resume, under 44 s for a listing that dies inside every census, plus at most one 0.5 s pass | Probes at production constants, each in its own PID namespace: 14.02 s with no resume, 22.03 s after a resume at about 2 s, 33.51 s and 33.92 s after resumes at 13.5 s and 13.9 s, 32.54 s with R764-1's late-survivor probe, and 24.01 s for the endless listing with no resume |
| No control for a resumed shell's trap-started command | R763-1-F4, R764-1-F2 | `scripts/test_suite_cancellation.py:542-579`: the late-resume control's trap also runs `sleep 1.5`, an external command longer than the 1 s such a command had before #833, then writes a second marker | Red under R763-1's `trap-commands-1s` and R764-1's `M07`: "the resumed shell's trap command was killed inside the shell's window". Green at this head |
| The stall control gave its child 2.5 s to die after `SIGKILL`, shorter than the measured tail | R763-1-F3 | `scripts/test_suite_cancellation.py:505-539`: `REAP_SECONDS` is no longer shortened, so the child keeps the product's whole 10 s window, derived from the longest stall measured (7.96 s). The control now fails when `SIGKILL` lands in the stalled pass itself: a 1.5 s grace is longer than the 1 s the cap lets the first pass and the 2 s stall advance the clock | Red under the wall-clock and 5 s-cap mutants of both reviews: "the stall was charged in full: SIGKILL in pass [2]". At this head it passes with the child's `SIGKILL` delayed up to 10.4 s, and fails at 11.0 s, with R763-1's stall-window probe |
| The command-table statement | R764-1-F4, R763-1-X2 | [Known limitations](#known-limitations--out-of-scope) now states only what three named commands show | The commands and their output are quoted there |
| The before/after rows did not say why the before tree failed | R763-1-X1, R764-1-R1 | The two rows now say "all at the fixture's 12 s hang bound, none `CLEANUP FAILED`" | |
| "never fails a descendant it has not yet killed" | R764-1-R2 | `docs/testing/TESTING.md:270`, with R764-1's exact wording | |

The `stages` helper's docstring said it was for a control whose result does not depend on the stages, which R763-1-F3 showed was not true. It now says only what the helper does (`scripts/test_suite_cancellation.py:407`).

Suggestions:

- R763-1-S1 asks for an Issue for the stale command table, and R763-1-S2 asks for a record on #833 at merge. Both are manager actions, so round 2 leaves them open.
- R764-1-S1 asks for a control on the 10 s values themselves. Not taken. A control can only pin a window as long as the delay it plants, so pinning the derived 10 s would add about 10 s to every sweep's preflight. A shorter delay pins only a lower bound. The stall-window probe above is evidence that a death delayed by up to 10.4 s is not judged; it is not a control.
- R764-1-S2: the census cost figure now has a receipt. On 1,403 visible processes and 200 interleaved passes, the census at this head took a median of 17.4 ms against 37.6 ms on `dev`. The source comment says 13 ms against 30 ms for 1,300 processes. No code change.

### Round 2 mutation re-run

Every mutant in both round 1 tables, applied alone to this head's `scripts/owned_process.py`. Each mutant ran once per owner control, each run in its own user and PID namespace: 31 mutants, 217 runs. R764-1's own driver was also re-run unchanged on fresh clones of this head; it runs the whole sweep test, or the lifecycle test, per mutant.

Per control, at this head (`ok` passes, `RED(rc)` fails; `-9` is the run's 150 s bound):

| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | red |
|---|---|---|---|---|---|---|---|---:|
| R763-none | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-identity-includes-parent | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R763-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R763-trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R763-no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R763-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| R763-survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| R763-killed-counts-as-gone | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| R763-report-without-wchan | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| R763-cleanup-does-nothing | ok | RED(1) | RED(-9) | RED(1) | RED(1) | RED(1) | RED(1) | 6 |
| R764-M01-identity-includes-parent | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01b-send-recheck-includes-parent | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01c-identity-includes-parent-both | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R764-M02-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M03-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M04-clamp-5s | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M05-no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M06-root-killed-unresumed | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M07-trap-child-no-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M08-no-kill-before-fail | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R764-M09-kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R764-M10-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| R764-M11-trust-sigkill | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R764-M12-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| R764-M13-cleanup-does-nothing-suite | ok | RED(1) | RED(-9) | RED(1) | RED(1) | RED(1) | RED(1) | 6 |
| R764-M14-no-start-recheck | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M15-windows-2s | ok | ok | ok | ok | ok | ok | ok | 0 |

The new reds and their failing words: `trap-commands-1s` and `M07` on `shell_window`, "the resumed shell's trap command was killed inside the shell's window"; `deadline-wall-clock`, `pass-cap-5s`, `M03` and `M04` on `stall`, "the stall was charged in full: SIGKILL in pass [2]". Every other row is as in round 1. `M01` and `M01b` are each half of the identity fix and `M01c`, both halves, is red. `M14` is pre-existing safety, `M15` is the constants (R764-1-S1), and under `killed-counts-as-gone` the run still fails through the empty-listing path.

R764-1's driver, whole test per mutant:

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

### Round 2 gates

All at head `1ff8292cd5b761633ef9500a7c5a4b1626a3d92c`, one log and rc each, never piped.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in round 1 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`. `owner-stall: {'stalled_seconds': 2.0, 'killed_in_pass': 27}`, `owner-shell-window: {'trap_ran_after_kill_time': True, 'trap_command_ran': True}` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| Mutation re-run, both round 1 tables | As above: every round 1 row reproduced, and each new control red when its fix alone is reverted |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 2 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

## Round 3

Round 2's reviews, R763-2 and R764-2, are both NEGATIVE on `1ff8292cd5b761633ef9500a7c5a4b1626a3d92c`, with the same single MINOR. Round 3 answers it with the code fix, the reviews' option (b) in R763-2 and option (a) in R764-2. Nothing else changes.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| A cancel during cleanup, after the command was collected, re-armed the resumed shell's window for a shell that was gone. So "that resume comes before 14 s", "under 34 s" and "under 44 s" were false on that path: 50 to 54 s for a listing that dies inside every census, 40 s for a late survivor | R763-2-F1, R764-2-F1 | `scripts/owned_process.py:304-309`: a resume re-arms the trap window only while the notified shell is still owned and listed (`root_pid in owned`). A collected shell has no trap left to run, so the rest keep the stages of a cleanup with no resume | `scripts/test_suite_cancellation.py:657-691`, `owner_late_cancel`, run in the preflight at `:706`; `docs/testing/TESTING.md:274` lists it |

**The control.** A real `true` runs through `OwnedProcesses.run` and is collected. The control then sends the owner `SIGTERM` in the first census pass of cleanup, which lists one process that dies inside every census (as `owner_vanishing` does). It fails in either of two ways, each with its own words. One is a resume sent to the collected shell: "a cancel after the shell was collected resumed it, re-arming its trap window". The other is no verdict within 15 s: "cleanup never reached a verdict after a late cancel". The control sets `TRAP_SECONDS` to 30 s, so a re-armed window also trips the bound even without the resume signal. Unmutated it passes in 0.8 s, which is all it adds to the preflight.

- With only the fix reverted, it is red in 0.0 s: `AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window`.
- With the fix reverted and the resume's `SIGCONT` also dropped, it is red at the bound, so only the re-armed window is left to catch: `AssertionError: cleanup never reached a verdict after a late cancel`.
- Under the endless-listing mutants (R763-2 `endless-unbounded`, R764-2 `M10`) and R763-2 `survivor-never-fails`, it is also red at the bound, with the neutral words.

The control took two commits. The first (`03ea2eb0`) had a single bound message, "re-armed its trap window", which the first mutation run showed was also printed under those three unrelated mutants. The second (`3740565f`) names only the cause the control sees.

**The bounds hold as written.** A resume now needs the shell in `owned`. While anything is owned, the verdict at `clock >= limit` comes first in the same pass, and `limit` is 14 s before any resume. So the resume comes before 14 s. After it, `limit = clock + 20 < 34`. The listing branch waits `REAP_SECONDS` more, under 44 s. The verdict comes at most one 0.5 s pass later. So the three statements (`scripts/process_test_support.py:19-30`, `docs/testing/TESTING.md:229-235`, and [The deadline's derivation](#description) in this body) are true with no change. So is `FINISH_SECONDS`'s "49.6 s, or 59.6 s for the listing". Measured at production constants:

| Probe | Cancel at | Round 2 head `1ff8292c` | This head |
|---|---:|---:|---:|
| R763-2 `late_cancel_listing.py <clone>/scripts 23` | 23 s | 53.02 s | **24.02 s** |
| R763-2 `late_cancel_listing.py`, at 20 s and 5 s | 20 s, 5 s | 50.02, 35.03 s (R763-2's receipts) | 24.01 s, 24.01 s |
| R764-2 `probe_late_cancel.py` | none, 20 s, 23.9 s | 24.01, 50.03, 53.92 s | 24.01, 24.01, 24.01 s |
| R764-2 `probe_late_cancel_survivor.py` | 20 s | 40.06 s | 21.04 s |
| Round 2's survivor-bound probes, each in its own PID namespace | (live shell) | 14.02, 22.03, 33.51, 33.92 s | 14.01, 22.06, 33.51, 33.92 s |

So a cancel during cleanup now leaves the endless listing at its 24 s with no resume, under 44 s. Every pass was under 0.1 s, so these times are owner clock. In R764-2's survivor probe, the descendant first appears at 21 s, after the 14 s deadline. It now fails the run in the pass that first lists it, as it would with no cancel, and is sent `SIGKILL` as the report is raised. Before this fix, the re-armed window gave it 19 s. The report's "not sent SIGKILL" names the state when the message was built.

**Not taken in round 3.** These leave no figure false:

- the wording residue R763-2-X1, R763-2-X2, R764-2-R1 and R764-2-R2;
- the suggestions R763-2-S1 (the 10 s values, as in round 2), R763-2-S2 (manager actions), R763-2-S3 (the census-cost comment) and R764-2-S1 (pinning the 0.5 s cap itself).

They stay with the manager's residue checklist.

### Round 3 mutation re-run

Every mutant of both round 2 tables: R763-2's `make_mutants.py`, unchanged, and every suite entry of R764-2's `mutate_r2.py`. R764-2's list has one more entry, `M16-resume-collected-shell`, the round 3 fix reverted. Two of mine join them: the same revert, and that revert with the resume's `SIGCONT` dropped. Each mutant ran once per owner control, now 8, each run in its own user and PID namespace: 37 mutants, 296 runs. Against the same table at `47fdd941`, before the control's second commit, no cell changed between red and green. The 7 older columns match both round 2 tables in every row.

Per control, at this head (`ok` passes, `RED(rc)` fails; `-9` is the run's 150 s bound):

| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | red |
|---|---|---|---|---|---|---|---|---|---:|
| R763-deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| R763-identity-includes-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | 1 |
| R763-no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R763-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R763-no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-none | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-pass-cap-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-reap-window-2s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | 2 |
| R763-survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | 3 |
| R763-trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M01-identity-includes-parent | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01b-send-recheck-includes-parent | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01c-identity-includes-parent-both | ok | RED(1) | ok | ok | ok | ok | ok | ok | 1 |
| R764-M02-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R764-M03-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M04-clamp-5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M05-no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M06-root-killed-unresumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M07-trap-child-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M04c-clamp-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M04d-clamp-1.0s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M07b-trap-child-1s-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M08-no-kill-before-fail | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M09-kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M10-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| R764-M11-trust-sigkill | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M12-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | 2 |
| R764-M13-cleanup-does-nothing-suite | ok | RED(1) | RED(-9) | RED(1) | RED(1) | RED(1) | RED(1) | RED(1) | 7 |
| R764-M14-no-start-recheck | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M16-resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| R764-M15-windows-2s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| A726c-resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| A726c-rearm-without-sigcont | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |

The new column's words are listed above. `M13`, cleanup that does nothing, gives "an endless listing did not fail the run". Every other red keeps its round 2 words.

R764-2's driver, with `M16` added, ran the whole test, or the lifecycle test, per entry on fresh clones of this head. Every round 2 entry gives the round 2 result. `M01`, `M01b`, `M04d`, `M14` and `M15` stay green, for the reasons both reviews give, and `M16` is red: `AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window`.

### Round 3 gates

All at head `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2`, one log and rc each, never piped.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 and 2 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`, with `owner-late-cancel: {'verdict_without_trap_window': True}` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| Mutation re-run, both round 2 tables, plus the new control and its revert | As above |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 3 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

## Round 4

Round 3's reviews are split on `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2`. R764-3 is POSITIVE. R763-3 is NEGATIVE with one MINOR under Tests. Round 4 answers that MINOR with a test change only. It also takes the retained wording residue with the reviews' exact fixes. `scripts/owned_process.py` is unchanged.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| No control pinned the guard that keeps a resumed shell alive inside its own window (`scripts/owned_process.py:315-318`). `owner_shell_window` resumed its shell about 0.9 s into cleanup. That is before grace + 1 s, where the stubborn-leaf rule at `:327` also spares the shell, since it is its child's first parent. So with the guard's `clock < kill_all` term removed, every owner control, the whole suite and the lifecycle test stayed green. At production constants that mutant SIGKILLs the shell before its trap whenever the resume comes 3 s or more into cleanup | R763-3-F1 | `scripts/test_suite_cancellation.py:563-565`: the control's child now dies 1.5 s after the first signal, not 0.7 s. So the shell is resumed past grace + 1 s, and only its own window keeps it alive in the pass that resumes it | `owner_shell_window` (`:542-581`), in the preflight at `:705`. Red with that term removed: `AssertionError: the shell was killed in the pass that resumed it, before its trap` |

**The control.** This is the variant R763-3 measured. It changes one number and keeps every assertion. Unmutated it passes in 3.1 s, where it took 2.3 s, so it adds 0.8 s to the preflight. The guard is right: the control is green unmutated, and the shell's trap and the command the trap starts both finish.

- The control holds the child on wall time, and the owner's clock lags wall time only while a pass takes longer than 0.5 s. The resume could fall back under grace + 1 s on the owner's clock only if the passes before it ran more than 0.3 s past their 0.5 s cap in total. In that run the control would pass even with the guard removed. That can weaken one run. It cannot turn the control red unmutated.
- With R763-3's `shell-killed-when-resumed`, the control is red in 1.6 s with the words above. The whole suite on a fresh clone is red in 5.5 s, with the same words.
- These stay red with the same words as round 3:
  - `no-trap-window`, `M05` and `M06`: "the shell was killed in the pass that resumed it, before its trap".
  - `trap-commands-no-window`, `trap-commands-1s`, `M07` and `M07b`: "the resumed shell's trap command was killed inside the shell's window".

**The wording residue.** Only these lines change. The rest of the `FINISH_SECONDS` comment is rewrapped with no word changed.

| IDs | Where | Now reads |
|---|---|---|
| R763-2-X1 | `docs/testing/TESTING.md:230`, `scripts/process_test_support.py:22-24`, and [The deadline's derivation](#description) in this body | "After a resume, every remaining descendant's deadline is 20 s after the resume, including one the trap started." |
| R763-2-X2 = R764-2-R2 | `docs/testing/TESTING.md:224` | "Two seconds later `SIGKILL` has reached every other descendant except a cancelled shell, which keeps its own window." |
| R764-2-R1 | [The deadline's derivation](#description) in this body | "A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock." |

The two exact fixes for `TESTING.md:224` differ by one word. R763-2-X2 says "a stopped shell" and R764-2-R2 says "a cancelled shell". I used "cancelled". At 4 s the cancelled shell is either still stopped or already resumed and inside its window. The guard spares it in both cases, and "stopped" names only the first.

**Not taken in round 4.**

- **R763-3-S1** (pin "listed" as well as "owned" for the resume) is not taken. The required verification for R763-3-F1 is that no other matrix row changes. A control for S1 turns `new-fix-census-not-owned` red, so it would change a row in the same round. R763-3 also shows that the variant can only re-arm the window in the pass that reaps the shell, before 14 s. So every stated bound holds under it, and no figure, verdict or bound depends on it.
- The suggestions R763-2-S1 (the 10 s values), R763-2-S2 (manager actions), R763-2-S3 (the census-cost comment) and R764-2-S1 (pinning the 0.5 s cap itself) are not taken. They stay with the manager's residue checklist.

### Round 4 mutation re-run

R763-3's matrix, run with its own `matrix.py`, `mutants.py` and `run_control.py` on a fresh clone of this head: 13 mutants × 8 owner controls, each run in its own user and PID namespace. Against R763-3's table at `3740565f`, only one row changed. `shell-killed-when-resumed` is now red on `shell_window`:

| mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | red |
|---|---|---|---|---|---|---|---|---|---|
| identity-has-parent | ok | RED(1) | ok | ok | ok | RED(1) | ok | ok | 2 |
| listing-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| new-fix-census-not-owned | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| new-fix-reverted | ok | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| none | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| pass-unclamped | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | 2 |
| **shell-killed-when-resumed** | ok | ok | ok | ok | **RED(1)** | ok | ok | ok | **1** |
| survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | 3 |
| trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |

Round 3's full table was re-run the same way, with R763-3's two mutants added: 39 mutants, 312 runs. All 37 rows of the [Round 3 table](#round-3-mutation-re-run) are identical, cell for cell and in their failing words. The two new rows:

| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | red |
|---|---|---|---|---|---|---|---|---|---:|
| R763-3-shell-killed-when-resumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-3-new-fix-census-not-owned | ok | ok | ok | ok | ok | ok | ok | ok | 0 |

R764-2's whole-test driver also ran on fresh clones of this head. It has round 3's `M16`, plus R763-3's mutant on the whole suite and on the lifecycle test. Every entry gives its round 3 result:

- `control-A`, `control-B` and `control-lifecycle` are green.
- `M01`, `M01b`, `M04d`, `M14` and `M15` are green, for the reasons both reviews give.
- Every other entry is red with its round 3 words.
- The new suite entry is red: `AssertionError: the shell was killed in the pass that resumed it, before its trap`.
- On the lifecycle test the mutant stays green, as at round 3. That test does not run this control.

### Round 4 gates

All at head `c1b2961777809403bd2de833ec1fa00c75394d6c`, one log and rc each, never piped.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 3 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`, with `owner-shell-window: {'trap_ran_after_kill_time': True, 'trap_command_ran': True}` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| Mutation re-run: R763-3's matrix, round 3's table with R763-3's two mutants, R764-2's whole-test driver | As above |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 4 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
