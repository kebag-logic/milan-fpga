[A726h]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Rounds 2 to 5](#rounds-2-to-5)** — Links to each round's published section.
- **[Round 6](#round-6)** — Round 5's findings with both review IDs: the shell-window hold bounded on both sides, the stated cleanup contract as a table with each row's control and mutants, the five gaps pinned, an own mutant per row, and the gates.
- **[Round 7](#round-7)** — Round 6's findings with both review IDs: every signal pinned through the handle, a first-pass resume inside grace with its trap's command, each row's domain equal to what it states, an own mutant at each domain's edge, the residue, and the gates.
- **[Round 8](#round-8)** — Round 7's findings with both review IDs: a resume-timing matrix over every class of pass, each at its earliest and latest, alone or with a trap command; every round 7 reviewer mutant; each domain note naming its cells; an edge mutant per cell; the residue, the suggestions and the gates.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally. `833-owned-process` -> `dev`, head `5b6d38a3542119ad77d352ea992e3cc41d121620` (round 8). Round 8's gates are in [Round 8](#round-8). The full sweep ran at round 1's head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`: 65 of 65 suites, 2,191,394 checks, 0 failures. Rounds 2 to 8 change only files round 1 changed, so the sweep was not rerun. Hosted contexts not yet run.

## Linked Issue / roles

Relates to #833

Executor: `[A726]` (round 1), `[A726b]` (round 2), `[A726c]` (round 3), `[A726d]` (round 4), `[A726e]` (round 5), `[A726f]` (round 6), `[A726g]` (round 7), `[A726h]` (round 8)
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

Ten controls join the sweep's preflight in `scripts/test_suite_cancellation.py`. Each fix reverted alone turns its control red, including a planted survivor that must fail the run and take its stopped shell with it.

| Touched | Why |
|---|---|
| `scripts/owned_process.py` | The fixes above |
| `scripts/process_test_support.py` | `FINISH_SECONDS`; every published mutant of the owner and the campaign that runs them (round 5); the starved owner's clock that `owner_stated_seconds` runs on (round 8) |
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
python3 scripts/test_suite_cancellation.py --mutants
make --no-print-directory -C tb/verilator/gptp_shadow
git diff --check origin/dev...HEAD
```

To see the cause on the first commit of this branch, run `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` beside CPU load or real builds on your own booked CPUs: the failure names the state of each remaining process.

Expected result / pass criteria: `suite cancellation: PASS`, whose log prints the planted survivor's `CLEANUP FAILED` line with `state`, `wchan`, `parent` and `age`; `owned-process mutants: PASS (119 mutants, 116 with a control that must fail)`; `mutant lifecycle: PASS`; `RESULT: PASS`; `git diff --check` silent.

Local evidence at this head: every `run:` step of `docs.yml`, as in [Round 8 gates](#round-8-gates); `behave` 2330 steps passed. The full sweep ran in 4 shards, rc 0, at round 1's head.

## Known limitations / out of scope

- **"No suite left to fail by chance" is not absolute, so this is `Relates to`, not `Closes`.** `Probe.ready`'s 15 s handshake is the next bound: it tripped 4 of 10 after this change, at 16 runnable per CPU and host load 250 to 314, with no ownership failure in them. It is not changed here.
- **The host stalls' cause is not named.** They did not recur in 703 cleanups with a sidecar at load near 30. The D wait channels are mapping-lock paths, so contention on mappings shared across the host is an inference, with no kernel trace behind it. A stall beyond 10 s would still fail, naming the state.
- **The #828 replay cannot be classified:** its log has the old message.
- **`owner_survivor` drops SIGKILL at the owner's send,** since no unprivileged control can build an unkillable process.
- **A stuck-process cancellation now fails the run under 34 s of owner clock (44 s for a listing that dies inside every census), not 4 s,** as derived above. The preflight is about 11 s longer, for the timeout control's 10 s, round 2 adds about 1.5 s, the trap command's, round 3 adds 0.8 s, the late-cancel control's, round 4 adds 0.8 s to the shell-window control, round 5 adds about 1.5 s: 1.4 s to the shell-window control and 0.1 s for two new controls, round 6 adds about 0.2 s: the report control's 0.1 s pause and the reused-identity control's second process, and rounds 7 and 8 add no measurable time.
- `ci/image/command-table.json` pins these scripts' hashes and is not regenerated. What commands show, at this head:
  - `python3 -I command_table_staleness.py . 1f29f189 d4d8cff9 HEAD`, with R764-1's script from `review-evidence/833-r1/reviews/R764-1/scripts/` on branch `833-review-evidence`, prints `pins 149 stale 34 absent 1` for `dev` `1f29f189`, and `stale 38` for round 1's head and for this one. The 4 more are the 4 scripts this PR changes, which the table pins.
  - `git grep -l -e command-table.json -e ci_command_table HEAD` lists 14 files that read or name the table, among them `ci/image/build.py` and `scripts/ci_command_table.py`.
  - `git grep -n -F` for each of those 14 file names, `-- .github/workflows scripts/run_all_suites.sh`, prints nothing (rc 1). No workflow or sweep step names a reader of its script pins.
  - Regenerating the table would also rewrite the 34 pins already stale on `dev`, so it is left alone.

## Rounds 2 to 5

Each round's section is kept in that round's published PR body, unchanged:

- [Round 2](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r2/PR-BODY.md#round-2)
- [Round 3](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r3/PR-BODY.md#round-3)
- [Round 4](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r4/PR-BODY.md#round-4)
- [Round 5](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r5/PR-BODY.md#round-5)

## Round 6

Both round 5 reviews of `a67eaf66c99b6b07c7ef206ad3489cb9555e00ca` are NEGATIVE: R763-5 has one MAJOR and two MINOR findings, and R764-5 one MINOR with three surviving mutants. The manager's ruling on #833 governs this round. It asks for:
- the MAJOR first;
- a table in `TESTING.md` of every stated cleanup behaviour, with the control that pins it and the mutants that prove it, and a short list of what no control pins;
- the five open gaps pinned or moved, the signal through the handle pinned;
- one more mutant of the lane's own for each row.

All five gaps are pinned; none moved. `scripts/owned_process.py` is unchanged since `c1b29617`, and no probe or mutant showed it wrong.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| The shell-window control's 61-pass hold had no upper bound on the owner's clock. From about 0.17 s a pass, the verdict at 10.4 s came first and the unmutated control failed `CLEANUP FAILED` | R763-5-F3 (MAJOR) | `scripts/test_suite_cancellation.py:580-583`: a 40.5 s reap stage. Pass 61 is at most 30.5 s of owner clock at the 0.5 s cap, however slow each pass is. So the verdict, at 40.9 s, leaves the child the product's 10 s after its SIGKILL. The resume stays past grace + 1 s, as before | R763-5's `slow_census_probe.py` at 0.15, 0.2, 0.3 and 0.5 s: PASS at 14.0, 17.1, 23.6 and 36.6 s (also 1.0 and 1.75 s: PASS). Unmutated: green 6 of 6 and 24 of 24. Red 6 of 6 with their words: `shell-window-one-pass`, `shell-window-1s`, `shell-killed-when-resumed`, `no-shell-window` (M05), `no-shell-window-kept`, `no-shell-window-pass`, `no-trap-window`, `root-killed-unresumed` (M06) and `trap-commands-*` |
| No control pinned the second cleanup stage for a parent whose child outlives its own SIGKILL | R763-5-F1, R764-5-F1 (`rv-parent-spared-past-kill-all`) | `owner_stated_seconds` lists such a parent. On the starved clock its SIGKILL comes in pass 9, 4 s: not before (pass 5) and not after (pass 29) | `parent-spared-past-kill-all` and `parents-killed-at-grace`: "a stubborn parent's stated seconds were not kept". `kill_all_probe.py`: rc 0 at the head, rc 1 on both |
| A signal by number after the identity recheck survived every control | R764-5-F1 (`rv-signal-by-number`) | `owner_reused_identity` (`:833-885`): the entry's number names its own process until the recheck, and another process from then on. That process blocks SIGTERM, so a signal sent to it is pending at once in its status, with no timing | `signal-by-number`: "a census entry was signalled by its number, after it changed hands". `check-before-open` too, below |
| No control bounded a vanishing listing's 10 s from above | R764-5-F1 (`rv-vanishing-waits-30s-more`) | `owner_stated_seconds` lists a process that every pass collects: verdict in pass 49, 24 s | `vanishing-waits-30s-more`, `vanishing-waits-no-more`: "a vanishing listing's stated seconds were not kept" |
| The report's current parent and age were checked only by presence | R763-5-F2 | `owner_report` (`:435-467`): the current parent as its own field beside `(first parent 1)`, and an age between the child's known lower and upper bounds | `report-without-current-parent`, `report-age-in-ticks`. `report_probe.py`: rc 0 at the head, rc 1 on both |
| Comment: "It is never signalled" | R764-5-R1 (RESIDUE) | `:799`, the exact fix: "It is never really signalled: this control's send only records the signal." | |
| `TESTING.md:224` omitted the trap's commands from its exception | R763-4-X1 (RESIDUE) | Merged, as R763-5 asked, into the table's second-stage row: "except a cancelled shell and any command its trap started, which keep the shell's own window" | |
| The campaign inherited a launcher's ignored SIGHUP, so `none / whole` failed in hard-HUP | R763-5-S1 (SUGGESTION, taken) | `scripts/process_test_support.py:561-574`: under an ignored SIGHUP the campaign installs a no-op handler for its runs. A handler is reset at exec, so the runs get the default, while the campaign still outlives a hangup | Launched with SIGHUP ignored, `--mutants none --matrix`: `none / whole` red (hard-HUP timeout) before, green after |

### The stated cleanup contract

`docs/testing/TESTING.md:255-289` is now this table, and its rule. Each cleanup statement from the earlier prose and the earlier control list is a row, so nothing was narrowed. `:285` says: "A stated cleanup behaviour is a row of this table; one that no control pins is on the list above, with the reason." Every mutant with a control is named in the row it breaks. This was checked by script against `MUTANTS`: 16 rows, 70 mutants named, 4 with no control and in no row.

Round 6's copy of this table is in `review-evidence/833-r1/author-r6/PR-BODY.md` on branch `833-review-evidence`. It is superseded by the table in `TESTING.md` at this head, which also gives each row's domain ([Round 7](#round-7)).

**Not pinned by a control** (`:279-283`), as round 6 had it: three reasons the product's comments give, each with its mutant in `MUTANTS` and no control (R764-5-S1's three). The second reason, "killed at grace either way", was false for a command the resumed shell's trap starts (R763-6-F1). Round 7 pins that item whole, so `sigterm-to-new` now names a control, and two items remain.

**Every published mutant is listed.** The 15 mutants R763-5 and R764-5 published are 13 distinct mutated files. Each equals a committed entry by hash. The two duplicates are `r5-parent-with-live-child-spared` = `rv-parent-spared-past-kill-all` and `r5-vanishing-fails-at-limit` = `rv-vanishing-waits-no-more`. Run unchanged at this head, both reviewers' own probes and mutant files give:
- `probe_mutants.py` and R763-5's `add_mutants.py` matrix: every one of their mutants of a stated behaviour is red on a control and the whole test, and `none` is green on all 11.
- `probe_effect.py`: the head's row is R764-5's own.
- `kill_all_probe.py` and `report_probe.py`: rc 0 at the head, rc 1 on each mutant.

### The lane's own mutant for each row

Each breaks its row differently from the published ones, and each is red on its control with its words, three runs out of three.

The table of these 16, with each edit and its control's words, is in round 6's copy on `833-review-evidence`, beside the contract table. Each is still red on its control at this head.

Two needed a change before they were red:
- **`resume-unless-reaped-now` was green.** `owner_late_cancel` modelled only a shell collected in the pass the cancel landed in. Now its census lists the shell, and its reap collects it, in the first pass only, so a later pass's resume is red too. Every earlier `late_cancel` mutant stays red, and `none` is green 24 of 24.
- `kill-all-a-pass-late` was red, but with the late-resume listing's words. `owner_stated_seconds` now checks its stubborn-parent and vanishing listings before the late resume. No other mutant's words change.

### Round 6 mutation table

At this head, `--matrix` ran all 74 mutants and `none` against every owner control and the whole test: 825 runs in 3 parts, each rc 0 and PASS, with no run cut at its bound.
- `none` is green on all 11.
- Each of the 70 mutants with a control is red on it with its words, and red on the whole test.
- The 4 with no control (`sigterm-checks-parent`, the equivalent one, and R764-5-S1's three) are green on all 11.
- `cleanup-does-nothing` on `late_exit` is now red at once ("cleanup returned with an owned child unreaped"), where round 5 cut it at 150 s.

The default `--mutants` campaign at this head: `owned-process mutants: PASS (74 mutants, 70 with a control that must fail)`. Each item's commit ran it too, and each passed.

### Round 6 commits

Six one-line commits:
- one per item, in the ruling's order: F3, the table, the five gaps, the own mutants, then the residue and S1;
- a sixth, after the gaps, moves `owner_report`'s new 0.1 s pause before its sleep check.

The pause had been taken after the check, so the child, which wakes every 20 ms, could be described in state `R`. That was red 3 of 160 unmutated at 16 jobs, and 0 of 160 after the fix. Item 4's campaign found it, and the fix was added on top rather than rewritten.

### Round 6 cost

Each control 3 times at round 5's head and at this one, interleaved:
- `owner_report`: 0.21 to 0.31 s, the 0.1 s pause.
- `owner_reused_identity`: 0.11 to 0.16 s.
- Every other control is unchanged, `owner_shell_window` included at 4.4 s.
- The whole test, 4 runs each, 8 at once: mean 60.8 s at `a67eaf66`, 61.2 s here.

So round 6 adds about 0.2 s to the preflight. `scripts/test_suite_cancellation.py` is 958 lines, under the 1000-line module ratchet.

### Round 6 gates

All at head `a987b601a0c10049321c18847504c4a94a862e04`, one log and rc each, never piped.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 5 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`, with `trap_finished: True` for the shell window. The stated seconds' passes are 5, 29, 12, 32 and 52, the stubborn parent's SIGKILL is in pass 9 and the vanishing verdict in pass 49. The reused identity shows `signalled: False, through_handle: True` |
| `python3 scripts/test_suite_cancellation.py --mutants` | rc 0, `owned-process mutants: PASS (74 mutants, 70 with a control that must fail)`. `--matrix`: 825 runs in 3 parts, each PASS |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 6 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

## Round 7

Both round 6 reviews of `a987b601a0c10049321c18847504c4a94a862e04` are NEGATIVE, on MINOR findings only, and both confirm the MAJOR resolved and the product correct. R764-6 has two MINOR, three RESIDUE and two SUGGESTION; R763-6 has one MINOR, four RESIDUE and one SUGGESTION. Each MINOR is a row of the cleanup table whose controls covered only part of what the row states. The manager's round 7 ruling on #833 governs this round: pin, never narrow. `scripts/owned_process.py` is unchanged since `c1b29617`, and no probe or mutant showed it wrong.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| Row 1 was pinned for `SIGTERM` only: a `SIGKILL` or `SIGCONT` sent by number after the recheck survived | R764-6-F1 | `owner_reused_identity` hands the number over for `SIGTERM` and again for `SIGKILL`, each with its own entry process, and checks a stale start time for both. The process that takes the number blocks `SIGTERM` and `SIGCONT`, and a `SIGKILL` stays pending until its target is collected. So any of the three, sent by number, is pending at once in its status, with no timing | `rv6-sigkill-by-number` and `rv6-sigcont-by-number`: "a census entry was signalled by its number, after it changed hands". R764-6's `row_mutants.py`, unchanged at this head: no survivor among its ten |
| Row 5 was pinned only for a resume at 5.5 s | R764-6-F2 | `owner_stated_seconds` resumes the shell in its first pass, with nothing else ever live, inside grace | `rv6-resume-not-before-grace`, `rv6-resume-not-first-pass`: "a first-pass resume's stated seconds were not kept" |
| No control resumed the shell inside grace, so a `SIGTERM` to its trap's command survived, and not-pinned item 2 gave a false reason | R763-6-F1 | In that first-pass listing the trap's command is listed from the second pass, inside grace: it gets no `SIGTERM`, and no `SIGKILL` until 10 s after the resume. A second listing has a survivor's terminal trap start a cleanup command, with no shell resumed: it gets no `SIGTERM` either. Row 2 now states that a descendant new since the first census gets none; row 6 that the trap's command gets none, even inside grace. Not-pinned item 2 is gone, because all of it is pinned | `sigterm-to-new` and `rv6-sigterm-trap-commands`: "a first-pass resume's ..."; the lane's `sigterm-to-new-before-resume`, the other half of `sigterm-to-new`: "a new descendant's stated seconds were not kept". R763-6's `grace_resume_probe.py`, unchanged: PASS 3 of 3 at this head, FAIL 3 of 3 on each of its three mutants |
| Each row needs a note of the domain its controls cover, equal to what it states | R764-6-S2, required by the ruling | Each "Pinned by" cell now names the domain of each control: which signals, which passes, which times. Where a domain fell short of its row, the control was widened; no row was narrowed. See below | Item 4's mutants, at each domain's edge |
| Row 1's wording | R764-6-R1 | The exact fix | |
| Rows 12 and 15's wording | R764-6-R2 | The exact fixes | |
| Row 10 listed `owner_shell_window`, which no mutant named | R764-6-R3 | `owner_shell_window` dropped from row 10. Its real passes count their own length only while the host keeps them short. `owner_stated_seconds` covers the whole row with no timing | |
| A return with no census after the collection | R763-6-S1, taken | `rv6-return-before-confirm`, on `owner_vanishing`, named in row 12 | "an endless listing did not fail the run" |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1, not taken | Its HUP stops are on the base too, so it predates this PR. R764-6 places it out of #833's scope. Suggested for a new Issue | |

R763-6-X1 to X4 are residue and are left for the manager's checklist. X1 and X3 overlap R764-6-R1 and R2, whose exact texts are applied.

### Domains equal to their rows

`owner_stated_seconds` now checks every stated time to a tick, 2^-20 s, about a microsecond:
- **Each stated time is approached a tick short of it, then reached exactly.** The starved owner's clock does both for every time in a listing's expected events. So the pass before a stated time is a tick early, and a time held a tick early or late is red. On the old half-second passes, a grace or window anywhere in the half second below its stated time was green.
- **Passes cover both clock rows.** Those that stall are a tick over the cap or an hour long, alternately. Those shorter than the cap are a tick, or half a second less a tick.
- **The shell is resumed across row 5's and row 6's domain:** in the first pass, at 3 s, at 5.5 s, and a tick before 14 s, the last pass before a survivor's verdict, so its deadline is a tick before 34 s. In another listing it is never resumed, while its child outlives 14 s.
- **After that last resume, a listing that dies inside every census** fails the run a tick before 44 s.
- **Every verdict** sends `SIGKILL` to each listed descendant not collected. It must report its live child's wall time since that child's first `SIGKILL`.
- **Expected events are in seconds now, not pass numbers,** and every earlier mutant keeps its words.

That last check was missing. The lane's row-16 edge mutant, which counts the reported `SIGKILL` age from cleanup's start, survived every control. Only `_describe`'s format was pinned.

### The lane's own mutant at the edge of each row's domain

Each is in `MUTANTS`, named in its row, and red on its control with its words. Each is also red on the whole test.

| Row | Edge | Mutant | Control: words |
|---|---|---|---|
| 1 | the last signal | `sigcont-by-number-after-kill` | `reused_identity`: "a census entry was signalled by its number" |
| 1 | the other signal, before the handle | `recheck-spares-sigkill` | `reused_identity`: "a census entry whose process was replaced was signalled" |
| 2 | 2 s, from below | `grace-a-tick-short` | `stated_seconds`: "a survivor's ..." |
| 3 | 4 s, from below | `kill-all-a-tick-early` | `stated_seconds`: "a stubborn parent's ..." |
| 4 | 14 s, from below | `verdict-a-tick-early` | `stated_seconds`: "a survivor's ..." |
| 4 | a shell never resumed | `verdict-waits-for-resume` | `stated_seconds`: "cleanup never reached a verdict on the owner's clock" |
| 5 | the last pass | `no-resume-before-verdict` | `stated_seconds`: "a last-pass resume's ..." |
| 6 | 10 s, from below | `trap-window-a-tick-short` | `stated_seconds`: "a late resume's ..." |
| 7 | the first pass, inside grace | `no-window-inside-grace` | `stated_seconds`: "a first-pass resume's ..." |
| 8 | the first pass, inside grace | `trap-commands-spared-only-past-grace` | `stated_seconds`: "a first-pass resume's ..." |
| 9 | the slowest pass | `cap-lifted-past-a-minute` | `stated_seconds`: "a survivor's ..." |
| 10 | the shortest pass | `tick-passes-count-nothing` | `stated_seconds`: "a survivor's ..." |
| 11 | after the last resume | `vanishing-verdict-ignores-resume` | `stated_seconds`: "a resumed vanishing listing's ..." |
| 12 | the first pass | `no-reap-after-first-census` | `late_exit`: "CLEANUP FAILED: owned descendants remain" |
| 13 | the other signal | `sigterm-rechecks-parent` | `reparented`: "SIGTERM waited for a later census" |
| 14 | a later pass | `resume-collected-shell-past-grace` | `late_cancel`: "a cancel after the shell was collected resumed it" |
| 15 | the other signal | `verdict-sends-sigterm` | `stated_seconds`: "a survivor's ..." |
| 16 | the age's origin | `killed-ago-from-start` | `stated_seconds`: "not in the report" |

### Round 7 mutation table

`MUTANTS` now holds 99 mutants and `none`, 96 of them with a control. The table names all 96. The 3 with no control are in no row: `sigterm-checks-parent`, the equivalent one, and the two remaining not-pinned items' mutants.
- **The default `--mutants` campaign at this head:** `owned-process mutants: PASS (99 mutants, 96 with a control that must fail)`. Each item's commit ran it too.
- **`--matrix` at this head:** all 99 mutants and `none` against every owner control and the whole test, in 4 parts, each rc 0 and PASS, with no run cut.
  - `none` is green on all 11.
  - Each of the 96 with a control is red on it with its words, and red on the whole test.
  - The 3 with no control are green on all 11.
- **Each reviewer's table check passes against `MUTANTS`.** R763-6's one-row-per-mutant check still reports only `windows-2s`, which it accepted, since that mutant edits two rows' constants.
- **Disclosed: under host load near 100, two existing mutants of the unchanged `owner_shell_window` broke item 5's own campaign.**
  - At load 91, `trap-commands-1s` was green.
  - At load 102, `shell-window-one-pass` was red, but with the trap command's words.
  - Above about 0.75 s a census pass, a 1 s window takes longer in wall time than the trap's 1.5 s command, so the two cannot be told apart.
  - So did the first run of one matrix part, `trap-commands-1s` green there as load rose to 90. That part's re-run is PASS.
  - At load 25 to 42, both are red 8 of 8 with their words, and so is `shell-window-1s`. The gate below is PASS.
  - Both are also red, with no timing, on `owner_stated_seconds`. Naming that control instead is left to the manager, since it is outside this round's items.

### Round 7 commits

Five one-line commits, one per item, in the ruling's order:
1. row 1;
2. the first-pass resume and the new descendants;
3. the domains;
4. the edge mutants;
5. the residue and S1.

`scripts/test_suite_cancellation.py` is 994 lines, under the 1000-line module ratchet.

### Round 7 cost

Each control 3 times at round 6's head and at this one, interleaved: every control is unchanged within 0.06 s. The whole test, 4 runs each, 8 at once: mean 63.5 s at both. Round 7 adds no measurable time to the preflight.

### Round 7 gates

All at head `887fdd53b013cc8796c1d595644a2a9f0b8c27a5`, one log and rc each, never piped, SIGHUP at its default in every launcher.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 6 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`. The stated seconds are grace 2 s, verdict 14 s, the parent's `SIGKILL` 4 s and the vanishing verdict 24 s, with resumes at 0, 3 and 5.5 s and a tick before 14 s. The reused identity shows `signalled: False`, through the handle for `SIGTERM`, `SIGKILL` and `SIGCONT` |
| `python3 scripts/test_suite_cancellation.py --mutants` | rc 0, `owned-process mutants: PASS (99 mutants, 96 with a control that must fail)`. `--matrix`: 4 parts, each PASS |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 7 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

## Round 8

Both round 7 reviews of `887fdd53b013cc8796c1d595644a2a9f0b8c27a5` are NEGATIVE on MINOR findings only. Both confirm every round 6 finding resolved and the product correct. R763-7 has two MINOR, three RESIDUE and two SUGGESTION. R764-7 has one MINOR, the same as R763-7-F1, plus two RESIDUE and two SUGGESTION. Each MINOR is a domain note that claims a case no listing exercised. The manager's round 8 ruling on #833 governs this round: close that class as a whole with a resume-timing matrix. Pin, never narrow. `scripts/owned_process.py` is unchanged since `c1b29617`, and no probe or mutant showed it wrong.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| No listing resumed the shell in a later pass inside grace. Three reviewer mutants that break rows 2, 3, 5, 6, 7 and 8 there were green on every control | R763-7-F1, R764-7-F1 | The resume-timing matrix in `owner_stated_seconds`, below: each class of pass at its earliest and its latest pass, the shell then alone or with a command its trap starts after the resume. R764-7's feasibility listing, a resume at 1 s, is beside it as published | Every round 7 reviewer mutant is red, each with its words. Each F1 mutant is also red on the matrix's later in-grace cells, not only at 1 s. Both reviewers' probes at this head: no survivor |
| No listing had a descendant new since the first census while a cancelled shell is stopped | R763-7-F2 | R763-7's feasibility listing, as published: the child's trap starts a command from the second pass, and the shell is never resumed | `sigterm-to-new-while-shell-stopped`: "a new descendant beside a stopped shell's stated seconds were not kept" |
| Each domain note names the matrix cells it covers | Ruling item 3 | `docs/testing/TESTING.md` tables the matrix's cells, with each listing's words, before the cleanup table. Rows 2 to 8 name the cells they cover. No row claims a cell that no listing exercises: row 2's new-descendant clause names only the cells whose trap command is listed inside grace | Per listing, below |
| An edge mutant for each cell | Ruling item 4 | Twelve, one for each cell at its class's earliest or latest pass | Each is red on its own cell's listing and on no other listing |
| Not-pinned item 1's wording | R763-7-R1 | The exact fix: "`SIGKILL` ends it by 4 s without one" | |
| The times preamble | R763-7-R2 | The exact fix: "Times are cleanup's, on the owner's clock, and each deadline fails the run in the first census pass at or past it." | |
| Rows 6 to 8 read as five resume points | R763-7-R3 | The notes now name the matrix cells and the resumes at 1 s, 3 s and 5.5 s | |
| Row 13's domain note | R764-7-R1 | The exact fix: "..., which gets its `SIGTERM` in that pass and not a later one" | |
| The control's docstring listed a resume it did not make | R764-7-R2 | The docstring now names the matrix's resumes, which the control makes | |
| Review-round prefixes in `MUTANTS` names | R763-7-S1, R764-7-S1, taken | Every reviewer mutant has a behaviour name. The published names are kept here, beside each | The six round 6 names are renamed, below |
| Quote the corrected grace probe | R763-7-S2, taken | `grace_resume_probe2.py` is the probe quoted below | |
| `trap-commands-1s` and `shell-window-one-pass` depend on host load on `owner_shell_window` | R764-7-S2, taken | Both now name `owner_stated_seconds`, where they are red with no timing. Rows 7 and 8 list that control. `owner_shell_window` keeps its 11 other mutants | "a late resume's stated seconds were not kept" |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1, retained, not taken | As in round 7: it predates this PR and is outside #833. Suggested for a new Issue | |

### The resume-timing matrix

`owner_stated_seconds` resumes a cancelled shell in each class of census pass, at the earliest and the latest pass of the class. It does so on its starved owner's clock, which lands a tick short of each stated time and then on it.
- **The first pass of cleanup is always inside grace.** Its clock is its own length, at most half a second. So "the first pass past grace" is the first at or past 2 s, and the pass before it is a tick before 2 s.
- **In each cell the shell is alone after the resume, or its trap starts a command.** The command is listed from the pass after the resume, since a census taken before the `SIGCONT` cannot list it.
- **Each listing's whole expected event list is asserted, to a tick.** This covers:
  - the child's `SIGTERM` at 0 s and its `SIGKILL` at 2 s, where it is listed;
  - no `SIGTERM` to the shell or to its trap's command;
  - the resume in exactly that pass;
  - `SIGKILL` to the shell and its command 10 s after the resume, and the verdict 20 s after.
- **So each cell asserts the row 2, 3, 5, 6, 7 and 8 behaviour that applies to it.**

| Class | Pass and clock of the resume | Alone after the resume | With a command its trap starts | That command first listed |
|---|---|---|---|---|
| First pass, inside grace | pass 1, 0 s | "a lone first-pass resume" | "a first-pass resume" (round 7's listing) | 0.5 s, inside grace |
| Later pass inside grace, earliest | pass 2, a tick in | "a lone second-pass resume" | "a second-pass resume and its trap command" | half a second and a tick, inside grace |
| Later pass inside grace, latest | the last pass before 2 s, a tick before | "a lone last in-grace resume" | "a last in-grace resume and its trap command" | past grace |
| First pass past grace | 2 s | "a lone first past-grace resume" | "a first past-grace resume and its trap command" | past grace |
| Later pass past grace, earliest | the next pass, a tick after 2 s | "a lone second past-grace resume" | "a second past-grace resume and its trap command" | past grace |
| Later pass past grace, latest | the last pass before 14 s, a tick before | "a lone last-pass resume" | "a last-pass resume and its trap command" | past grace |

- **Beside the matrix, other listings resume the shell at 1 s, 3 s, 5.5 s and a tick before 14 s,** with the trap's command listed from the resume pass. Another never resumes it, while its child outlives 14 s.
- **"A new descendant beside a stopped shell"** lists a command the child's trap starts, from the second pass, inside grace, while the shell stays stopped.
- **An audit of each listing's passes confirms where each resume falls,** the pass and the clock, and when its command is first listed.
- **The control runs its listings in order.** The new ones come after round 7's, so every earlier mutant keeps its words.

The starved owner's clock, `starved_cleanup` and `TICK`, moved unchanged to `scripts/process_test_support.py`. So `scripts/test_suite_cancellation.py` stays under the 1000-line module ratchet, at 965 lines.

### Every reviewer mutant published in round 7

Each is in `MUTANTS` under a behaviour name, with the published edit byte for byte, as a check against each reviewer's own script shows. Each is named in its row and red on its control with its words. Two published names are one edit.

| `MUTANTS` name | R763-7 published name | R764-7 published name | Finding | Row | Control: words |
|---|---|---|---|---|---|
| `check-before-open-for-sigkill` | `r7-check-before-open-sigkill` | | R763-7, row 1 edge | 1 | `reused_identity`: "a census entry was signalled by its number" |
| `no-resume-later-in-grace` | `r7-no-resume-in-grace-after-pass-1` | `rv7-no-resume-later-in-grace` | R763-7-F1, R764-7-F1 | 5 | `stated_seconds`: "an in-grace resume's ..." |
| `sigterm-trap-command-unless-first-pass-resume` | `r7-sigterm-trap-command-later-grace-resume` | | R763-7-F1 | 6 | `stated_seconds`: "an in-grace resume's ..." |
| `sigterm-trap-command-after-later-grace-resume` | | `rv7-sigterm-trap-command-later-grace-resume` | R764-7-F1 | 6 | `stated_seconds`: "an in-grace resume's ..." |
| `trap-window-not-later-in-grace` | `r7-trap-window-not-later-grace` | | R763-7-F1 | 8 | `stated_seconds`: "an in-grace resume's ..." |
| `no-window-later-in-grace` | | `rv7-no-window-later-in-grace` | R764-7-F1 | 7 | `stated_seconds`: "an in-grace resume's ..." |
| `sigterm-to-new-while-shell-stopped` | `r7-sigterm-new-while-shell-stopped` | | R763-7-F2 | 2 | `stated_seconds`: "a new descendant beside a stopped shell's ..." |
| `sigterm-to-new-after-1s` | | `rv7-sigterm-to-new-after-1s` (its control mutant) | R764-7-F1 | 2 | `stated_seconds`: "a first-pass resume's ..." |

Each is first caught by the listing its words name. Run with every listing checked, the F1 mutants are also red on the matrix's later in-grace cells:
- `no-resume-later-in-grace` and `no-window-later-in-grace`: all four of those cells.
- `trap-window-not-later-in-grace`: both trap-command cells.
- The two `SIGTERM` mutants: the pass-2 trap-command cell, the one whose command is listed inside grace.

The round 6 reviewer mutants are renamed:
- `rv6-sigkill-by-number` is now `sigkill-by-number`;
- `rv6-sigcont-by-number` is now `sigcont-by-number`;
- `rv6-resume-not-before-grace` is now `resume-not-before-grace`;
- `rv6-resume-not-first-pass` is now `resume-not-first-pass`;
- `rv6-sigterm-trap-commands` is now `sigterm-trap-commands`;
- `rv6-return-before-confirm` is now `return-before-confirm`.

The edits, controls and words are unchanged. The earlier rounds' sections keep the old names.

### An edge mutant for each cell

Each records, in the pass that resumes the shell, whether that pass is its cell's edge. It then breaks one stated behaviour of that cell only there:
- **In a lone cell, row 7:** after its resume pass, the shell is spared only while it has a listed child.
- **In a trap-command cell inside grace, row 6:** the command gets `SIGTERM`.
- **In a trap-command cell past grace, row 8:** the command loses the shell's window.

Run with every listing checked, each is red on its own cell's listing and on no other, so each cell's listing is the one that catches it.

| Cell | Edge | Mutant | Row | Control: words |
|---|---|---|---|---|
| first pass, alone | pass 1 | `lone-first-pass-shell-needs-a-child` | 7 | "a lone first-pass resume's ..." |
| first pass, trap command | pass 1 | `first-pass-trap-command-sigtermed` | 6 | "a first-pass resume's ..." |
| later in grace, alone | earliest: pass 2 | `lone-second-pass-shell-needs-a-child` | 7 | "a lone second-pass resume's ..." |
| later in grace, trap command | earliest: pass 2 | `second-pass-trap-command-sigtermed` | 6 | "a second-pass resume and its trap command's ..." |
| later in grace, alone | latest: within a pass of 2 s | `lone-last-in-grace-shell-needs-a-child` | 7 | "a lone last in-grace resume's ..." |
| later in grace, trap command | latest: within a pass of 2 s | `last-in-grace-trap-command-unspared` | 8 | "a last in-grace resume and its trap command's ..." |
| first past grace, alone | the first pass at or past 2 s | `lone-first-past-grace-shell-needs-a-child` | 7 | "a lone first past-grace resume's ..." |
| first past grace, trap command | the first pass at or past 2 s | `first-past-grace-trap-command-unspared` | 8 | "a first past-grace resume and its trap command's ..." |
| later past grace, alone | earliest: the second pass past grace | `lone-second-past-grace-shell-needs-a-child` | 7 | "a lone second past-grace resume's ..." |
| later past grace, trap command | earliest: the second pass past grace | `second-past-grace-trap-command-unspared` | 8 | "a second past-grace resume and its trap command's ..." |
| later past grace, alone | latest: within a pass of the verdict | `lone-last-pass-shell-needs-a-child` | 7 | "a lone last-pass resume's ..." |
| later past grace, trap command | latest: within a pass of the verdict | `last-pass-trap-command-spared-only-if-listed-at-resume` | 8 | "a last-pass resume and its trap command's ..." |

The last one spares only a command listed at the resume. So round 7's last-pass listing stays green under it, since that listing lists the command from the resume pass, and the matrix's cell turns red.

### Round 8 mutation table

`MUTANTS` now holds 119 mutants and `none`, 116 of them with a control. The table names all 116. The 3 with no control are in no row, as in round 7.
- **The default `--mutants` campaign at this head:** `owned-process mutants: PASS (119 mutants, 116 with a control that must fail)`. Each item's commit ran it too.
- **`--matrix` at this head:** all 119 mutants and `none` against every owner control and the whole test, in 4 parts, 1353 runs, each part rc 0 and PASS, with no run cut.
  - `none` is green on all 11.
  - Each of the 116 with a control is red on it with its words, and red on the whole test.
  - The 3 with no control are green on all 11.
- **The reviewers' probes, unchanged, at this head:**
  - `row_mutants.py` (round 6) and both round 7 mutant probes: no survivor among their 10, 5 and 4.
  - `grace_resume_probe.py`: PASS 5 of 5. The corrected `grace_resume_probe2.py`: PASS 3 of 3 at the head, and FAIL 3 of 3 on each of `sigterm-to-new`, `sigterm-trap-commands` and both round 7 trap-command `SIGTERM` mutants.
  - Both feasibility listings, added again to a copy: green, and red on each mutant they were written for.
  - The slowed shell-window campaign: PASS, 45 runs.
  - `sigcont_pending.py`: rc 0.
  - Every table check passes, except R763-6's one-row-per-mutant check, which still reports only `windows-2s`, as it accepted.
- **Disclosed:** R764-7's whole-test mode stops at its own report line on the first red result, since it joins `None`. The first run was red. `--matrix` gives the whole-test column for all four.

### Round 8 commits

Five one-line commits, one per item, in the ruling's order:
1. the matrix;
2. the round 7 reviewer mutants;
3. the domain notes;
4. the edge mutants;
5. the residue and the suggestions.

### Round 8 cost

Each control 3 times at round 7's head and at this one, interleaved, host load 6 to 10:
- `owner_stated_seconds` takes 0.16 to 0.21 s at both;
- every other control is within 0.2 s of round 7;
- the whole test, 4 runs each, 8 at once, has a mean of 60.6 s at round 7 and 60.4 s here.

Round 8 adds no measurable time to the preflight.

### Round 8 gates

All at head `5b6d38a3542119ad77d352ea992e3cc41d121620`, one log and rc each, never piped, SIGHUP at its default in every launcher.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 7 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`. The stated seconds are grace 2 s, verdict 14 s, the parent's `SIGKILL` 4 s and the vanishing verdict 24 s. Resumes are at 0, 1, 3 and 5.5 s and a tick before 14 s, with the matrix at 0 s, a tick, a tick before 2 s, 2 s, a tick after 2 s and a tick before 14 s |
| `python3 scripts/test_suite_cancellation.py --mutants` | rc 0, `owned-process mutants: PASS (119 mutants, 116 with a control that must fail)`. `--matrix`: 4 parts, each PASS |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 8 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

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
