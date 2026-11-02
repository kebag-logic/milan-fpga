# #833 HANDOFF ([A726])

Status: REVIEW READY. Head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`, 14 commits on `dev` `1f29f189`. Nothing pushed. `Relates to #833`: see [Acceptance](#acceptance).

## Cause

**No descendant ever survived SIGKILL. Two different things fail, depending on the load, and the old message could not tell them apart.** The message now prints what each process is doing. All 12 captured from the before tree are in `receipts/cause/all-cleanup-failed-messages.txt`.

| Count | Message shows | Which it is | Load that produced it |
|---:|---|---|---|
| 8 | `bash` or `python3` `state Z`, parent = the owner | **Zombie awaiting a reaper, and the reaper is the owner that is raising** | CPU overload, 10 to 16 runnable tasks per CPU |
| 1 | `bash state T wchan do_signal_stop`, not sent SIGKILL, with a child `state Z` | **A shell the owner has not yet resumed**, holding its zombie child | The same |
| 3 | `state D`: `dup_mmap` 1.91 s after SIGKILL, `unlink_file_vma_batch_process` 1.36 s, `__mmap_region` 2.07 s (and a re-parented `git`) | **Uninterruptible sleep after SIGKILL** | Real compile load, 10 Verilator builds, host load about 250 |

Those ages are lower bounds: the owner raised and stopped watching. None was still runnable or sleeping after SIGKILL at the raise.

Correction: while working I said none was in D. That held for CPU-only load and was wrong once real builds ran. The D class is why the windows below are derived from measurement and not left at 2 s.

The #828 replay cannot be classified: its log has the old message. Its listing (root, the root's child, one re-parented process) fits the `T` + `Z` row or a D row.

### The faults, each with its evidence

1. **Reap order.** `_reap`, then the census, then the raise. A child exiting during the census is listed dead and nothing reaps it again. Logic fix.
2. **Identity included the parent.** The first SIGTERM re-parents a descendant, which then fails the identity check and counts as new, so it never gets SIGTERM. It lives through grace and is spared to 3.0 s of the 4.0 s. `receipts/cause/slowest-cleanups.txt` shows it at 3.165 s with 1 ms census passes, so it reaches a container too. It occurred in 10 of 217 cleanups on 4 busy CPUs. Logic fix.
3. **The owner's own time was charged to the descendants.** A census reads every process on the host. The protocol needs 2 s + 4 passes, so it fails by construction past 0.5 s a pass. Measured: over 1 s a pass, 1.75 s at worst, at 16 runnable per CPU, so 3 to 4 passes in the 4 s. The same load in a PID namespace, census 1 ms: 20 of 20 pass, longest cleanup 2.19 s.
4. **Stage ordering.** A shell could get SIGCONT and SIGKILL in one pass (`failing-timelines-L256-bare-host.txt`, 3.471 s), and the raise could fire with no SIGKILL ever sent.
5. **Host stalls in episodes, cause not named.** One held an owner 3.04 s in a single pass, with a 1 ms census, under a 1.5 GB cgroup. Another held four process starts 7.5 to 7.96 s at the same moment (`receipts/deadline/killlat-summary.txt`). They did not recur in 703 cleanups with a sidecar at load near 30, 0% steal. The D wait channels are mapping-lock paths, so contention on mappings shared across the host is my inference; I have no kernel trace that proves it.

### The deadline, derived

Direct SIGKILL to death through a pidfd, no census involved: 121,660 kills (100,277 beside 10 real builds, 21,383 with spinners too), host load up to 111: **longest 0.23 s**; D only in `dup_mmap`, `unlink_file_vma_batch_process`, `unlink_anon_vmas`. Yet 2.07 s in D at load 250, and stalls to 7.96 s. So the tail comes in episodes, and the window has to outlast the episode, not the typical kill.

| Constant | Was | Now | Derivation |
|---|---|---|---|
| Pass advance, `MAX_PASS_SECONDS` | wall clock | at most 0.5 s a pass | Clears the one census failure: grace alone spans at least 4 passes, against the 4 the whole protocol needs. A stall cannot expire a deadline. |
| Last SIGKILL to verdict, `REAP_SECONDS` | 0.2 s for what was killed last | 10 s | Outlasts the longest stall measured, 7.96 s |
| Resumed shell's window, `TRAP_SECONDS` | what was left of 4 s, down to 0 | 10 s | The same; resume to exit was at most 0.21 s |
| `FINISH_SECONDS`, the fixture's hang bound | 12 s | 60 s | One driver: 12.7 to 15.1 s, n = 24. Four times that. Bounds a hang, never a property. |

A true survivor still fails the run, after 14 s of owner clock, or 24 s if the shell hung too. It was 4 s. That is the cost, and it is only paid when something is really wrong.

## Changes

| File:line | Change |
|---|---|
| `scripts/owned_process.py:109` | `_describe`: state, wait channel, parent, first parent or new, age, start, time since SIGKILL. Message also gives elapsed, passes, slowest pass |
| `scripts/owned_process.py:80,211` | Census by direct calls: 13 ms a pass against 30 ms at 1300 processes; a process name need not be text |
| `scripts/owned_process.py:240,248` | Identity is the start time, not the parent |
| `scripts/owned_process.py:226,280` | Collect after the census, before judging; only a census after a reap proves nothing remains |
| `scripts/owned_process.py:45,284` | Deadlines on a clock a pass advances by at most 0.5 s |
| `scripts/owned_process.py:39,310,315` | A resumed shell gets its own window, never SIGKILL in the pass that resumes it |
| `scripts/owned_process.py:40,294,298` | 10 s verdict window; SIGKILL everything before raising; a listing that always dies in the census still reaches a verdict |
| `scripts/process_test_support.py:22,219` | `FINISH_SECONDS` |
| `scripts/test_suite_cancellation.py:142,329` | The timeout control's 0.5 s and the shell's 5 s, each below a measured stall |
| `tb/verilator/gptp_shadow/test_mutant_lifecycle.py:232` | 5 s to 15 s, the same reason |
| `scripts/test_suite_cancellation.py:432-618` | Seven controls in the sweep's preflight |
| `docs/testing/TESTING.md:258` | The contract |

### Regression tests and controls

`receipts/mutations/`, each fix reverted alone at this head, each in its own PID namespace:

| Reverted | Result | Goes red with |
|---|---|---|
| None, both tests | rc 0, rc 0 | |
| Identity includes the parent | rc 1 | `re-parented descendant was treated as new and never got SIGTERM` |
| No reap after the census | rc 1 | `CLEANUP FAILED ... exited during this report` |
| Deadline on the wall clock | rc 1 | `CLEANUP FAILED`, on a process never killed |
| No shell window | rc 1 | `the shell was killed in the pass that resumed it` |
| No SIGKILL before raising | rc 1 | `stopped shell left behind` |
| Endless listing unbounded | rc 1 | `cleanup never reached a verdict` |
| **A survivor does not fail the run** | rc 1 | `a survivor never failed the run` |
| Report without state | rc 1 | The missing `state S` field |
| Cleanup does nothing: sweep test, lifecycle test | rc 1, rc 1 | The planted leak is detected in both |

`owner_survivor` plants a descendant whose SIGKILL has no effect, beside a stopped shell. It must fail, name the state, and take the shell with it. No unprivileged control can build a truly unkillable process, so it drops the signal at the owner's send, and says so. The lifecycle test alone does not catch the survivor mutant because it plants no survivor; that control lives in the sweep test, which every sweep runs.

## Failure counts, before and after

**Before is `63044c82`: `dev` plus only the message.** After is the head. Both ran at the same moment on the same CPUs, in this unit's own 16-27, at normal niceness.

| Test | Load | Before passes | After passes |
|---|---|---:|---:|
| Full suite, `make -C tb/verilator/gptp_shadow` | 10 real builds + 48 spinners, 12 CPUs | **0 of 10**, all at the 12 s bound | **10 of 10**, `RESULT: PASS`, lifecycle PASS |
| Lifecycle, `make ... lifecycle` | 12 concurrent + 48 spinners, 12 CPUs, host load to 197 | **0 of 18**, all at the 12 s bound | **18 of 18** |
| Sweep controls, `scripts/test_suite_cancellation.py` | The same | **11 of 12**, one `CLEANUP FAILED`, `bash state Z` | **12 of 12** |
| Real cancellation and interruption cases, focused | 192 spinners on 12 CPUs, host load 250 to 314 | **4 of 10**: 4 `CLEANUP FAILED`, 2 handshake | **6 of 10**: all 4 at the 15 s handshake, before any cleanup |

Across 50 after-tree logs at this head, plus the 4 sweep shards: **zero `CLEANUP FAILED`** other than the survivor control's own print.

Before the last two commits, at `f6b776e7` (`receipts/round0-at-f6b776e7/`), the full suite ran 20 times each with 10 builds and no spinners. Round 0, host load about 250: all 10 failed at the 12 s bound on both trees, and 3 of the before runs also raised `CLEANUP FAILED`, the D messages above. Rounds 1 to 3: after 15 of 15, before 14 of 15. Those are what showed the 12 s bound was too low and the D class was real. Load runs with 64 to 256 spinners are in `receipts/cause/`.

## Gates

All at the head, one log and rc each, never piped.

| Gate | Result | Log |
|---|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, runner and verifier from the #829 receipts | **Verifier rc 0: 64 steps rc 0, 31 not run with a stated reason, 0 bad.** Tree clean after each job | `receipts/gates/docsyml-table.md`, `docsyml/` |
| Builder leg 0, leg 1, in `docs.yml` | rc 0, rc 0. `ALL GATES PASS EXCEPT 1 NOT RUN`, `EXCEPT 16 NOT RUN` (15 need a SoC interpreter, 1 a build tree) | `docsyml/docs-gates-1__gate_25_0.log`, `docs-gates-2__gate_25_1.log` |
| Builder legs, with the SoC interpreter's environment | rc 0, rc 0. `EXCEPT 1 NOT RUN` each | `gates/lane/builder_leg0.log`, `builder_leg1.log` |
| `cd tests && behave` | rc 0. 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`; the log is in `LARGE-LOGS.txt` |
| `git diff --check` against `1f29f189` | rc 0 | `gates/lane/diffcheck.log` |
| Full sweep, 4 native-shards units | **rc 0 on all 4. 65 of 65 suites, 2,191,394 checks, 0 in-suite failures, 0 timed out** | `gates/sweep/shard-*/spec/` |
| Its `gptp_shadow`, `gptp_tables` | 325 checks, lifecycle PASS, 9 of 9 controls; 26 of 26 controls | `gates/sweep/shard-1/` |
| Its preflight sweep controls, new ones included | PASS on all 4 shards | `gates/sweep/shard-*/test_suite_cancellation.log` |

Shards ran on `112-127` from `cpu_ranges.py pick`, four 4-CPU ranges, MemAvailable above 50 GB at launch, `--no-print-directory`. The not-run reasons are the #829 list unchanged. The hosted contexts and `act` replay have not been run; the manager's bank runs those.

## Open: for the manager

- **Acceptance.** Item 1 is met. Item 2: the fix is real and the deadline carries its derivation, but "no suite left to fail by chance" is not absolute. Hence `Relates to #833`; closing is your call.
- **`Probe.ready`'s 15 s handshake is the next chance failure, and I did not change it.** Seen only at the most extreme load here: 4 of 10 after, at 16 runnable per CPU and host load 250 to 314, with no ownership failure in them. It wants its own Issue if that load matters.
- **A stall beyond 10 s would still fail,** loudly and naming the state. None was measured. Nor is the stall's cause named: an Issue with a kernel trace could settle it.
- **`ci/image/command-table.json` pins these scripts' hashes and was not regenerated.** It is already stale on `dev` (33 of 143 pinned files differ), no workflow or test reads it, and regenerating needs a pinned parser and would sweep in those 33. Decided: left alone.
- **The preflight is about 11 s longer** (45 s to 56 s with no load): the timeout control now waits out 10 s, and a stuck-process cancellation takes up to 24 s, not 4.
- **The commit history is noisier than one-per-concern should read.** Four commits answer my own gate and review findings (`a4896fcd`, `bcd8ad53`, `e52f6c51`, `f6b776e7`). I did not rebase them, as instructed.

## Incidents in this lane, no harm

Two mistakes of the same shape, both mine. A cleanup line ran `pkill -KILL -f 'compile.mk' ; pkill -KILL -x cc1plus; pkill -KILL -x g++`. The last two match host-wide. The first matched my own shell and killed it, so they never ran: the summary after them never printed, and only `-f compile.mk` could match that shell. The two failed `milan-*` units on the host date from 2026-10-29 and 2026-10-30. Later, a cleanup scoped to this unit's cgroup matched its own `bash -c` text and killed that shell, in this unit only. Cleanup now runs from a script file that matches on the program actually running (`receipts/load-tools/stoptests.py`), with load in its own process group.

My `systemd-run` load sub-units and a `timeout` on one runner each overran or orphaned load briefly, always inside CPUs 16-31; all of it was stopped and checked by PID. Nothing remains running: only this session's own unit. Scratch is pruned to logs and venv, 835 MB, and the 25 GB of shard clones this run made are removed.
