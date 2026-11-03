[A726i]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Rounds 2 to 7](#rounds-2-to-7)** — Links to each round's published section.
- **[Round 8](#round-8)** — Round 7's findings with both review IDs: a resume-timing matrix over every class of pass, each at its earliest and latest, alone or with a trap command; every round 7 reviewer mutant; each domain note naming its cells; an edge mutant per cell; the residue, the suggestions and the gates.
- **[Round 9](#round-9)** — Round 8's findings with both review IDs: a liveness axis for new descendants across every class of resume, beside a stopped shell and with none; every round 8 reviewer mutant; the liveness cells in the domain notes; an edge mutant per liveness cell; the residue and the gates.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally. `833-owned-process` -> `dev`, head `e803d94b3a11921a293cf036a8eda333d23828f9` (round 9). Round 9's gates are in [Round 9](#round-9). The full sweep ran at round 1's head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`: 65 of 65 suites, 2,191,394 checks, 0 failures. Rounds 2 to 9 change only files round 1 changed, so the sweep was not rerun. Hosted contexts not yet run.

## Linked Issue / roles

Relates to #833

Executor: `[A726]` (round 1), `[A726b]` (round 2), `[A726c]` (round 3), `[A726d]` (round 4), `[A726e]` (round 5), `[A726f]` (round 6), `[A726g]` (round 7), `[A726h]` (round 8), `[A726i]` (round 9)
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
| `scripts/process_test_support.py` | `FINISH_SECONDS`; every published mutant of the owner and the campaign that runs them (round 5); the starved owner's clock that `owner_stated_seconds` runs on (round 8), with its matrix's classes and its stated window (round 9) |
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

Expected result / pass criteria: `suite cancellation: PASS`, whose log prints the planted survivor's `CLEANUP FAILED` line with `state`, `wchan`, `parent` and `age`; `owned-process mutants: PASS (142 mutants, 139 with a control that must fail)`; `mutant lifecycle: PASS`; `RESULT: PASS`; `git diff --check` silent.

Local evidence at this head: every `run:` step of `docs.yml`, as in [Round 9 gates](#round-9-gates); `behave` 2330 steps passed. The full sweep ran in 4 shards, rc 0, at round 1's head.

## Known limitations / out of scope

- **"No suite left to fail by chance" is not absolute, so this is `Relates to`, not `Closes`.** `Probe.ready`'s 15 s handshake is the next bound: it tripped 4 of 10 after this change, at 16 runnable per CPU and host load 250 to 314, with no ownership failure in them. It is not changed here.
- **The host stalls' cause is not named.** They did not recur in 703 cleanups with a sidecar at load near 30. The D wait channels are mapping-lock paths, so contention on mappings shared across the host is an inference, with no kernel trace behind it. A stall beyond 10 s would still fail, naming the state.
- **The #828 replay cannot be classified:** its log has the old message.
- **`owner_survivor` drops SIGKILL at the owner's send,** since no unprivileged control can build an unkillable process.
- **A stuck-process cancellation now fails the run under 34 s of owner clock (44 s for a listing that dies inside every census), not 4 s,** as derived above. The preflight is about 11 s longer, for the timeout control's 10 s, round 2 adds about 1.5 s, the trap command's, round 3 adds 0.8 s, the late-cancel control's, round 4 adds 0.8 s to the shell-window control, round 5 adds about 1.5 s: 1.4 s to the shell-window control and 0.1 s for two new controls, round 6 adds about 0.2 s: the report control's 0.1 s pause and the reused-identity control's second process, rounds 7 and 8 add no measurable time, and round 9 adds about 11 ms.
- `ci/image/command-table.json` pins these scripts' hashes and is not regenerated. What commands show, at this head:
  - `python3 -I command_table_staleness.py . 1f29f189 d4d8cff9 HEAD`, with R764-1's script from `review-evidence/833-r1/reviews/R764-1/scripts/` on branch `833-review-evidence`, prints `pins 149 stale 34 absent 1` for `dev` `1f29f189`, and `stale 38` for round 1's head and for this one. The 4 more are the 4 scripts this PR changes, which the table pins.
  - `git grep -l -e command-table.json -e ci_command_table HEAD` lists 14 files that read or name the table, among them `ci/image/build.py` and `scripts/ci_command_table.py`.
  - `git grep -n -F` for each of those 14 file names, `-- .github/workflows scripts/run_all_suites.sh`, prints nothing (rc 1). No workflow or sweep step names a reader of its script pins.
  - Regenerating the table would also rewrite the 34 pins already stale on `dev`, so it is left alone.

## Rounds 2 to 7

Each round's section is kept in that round's published PR body, unchanged:

- [Round 2](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r2/PR-BODY.md#round-2)
- [Round 3](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r3/PR-BODY.md#round-3)
- [Round 4](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r4/PR-BODY.md#round-4)
- [Round 5](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r5/PR-BODY.md#round-5)
- [Round 6](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r6/PR-BODY.md#round-6)
- [Round 7](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r7/PR-BODY.md#round-7)

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

## Round 9

Both round 8 reviews of `5b6d38a3542119ad77d352ea992e3cc41d121620` are NEGATIVE on MINOR findings only, and both confirm the round 8 ruling met and the product correct:
- R763-8: two MINOR (F1, F2) and three RESIDUE; R764-6-S1 still retained.
- R764-8: one MINOR (F1), one RESIDUE and one SUGGESTION.

The three MINOR findings are one more axis of the same class: whether a new descendant is live. Every new descendant the stated-seconds control listed was a number no process has, which the product sees as not live, as it sees a zombie. The manager's round 9 ruling on #833 governs this round:
1. a liveness axis for new descendants;
2. every round 8 reviewer mutant red;
3. domain notes and an edge mutant per new cell;
4. the RESIDUE exact fixes.

Pin, never narrow. `scripts/owned_process.py` is unchanged since `c1b29617`, and no probe or mutant showed it wrong.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| No listing had a live new descendant beside a stopped shell, so a resume beside one survived every control | R763-8-F1 | The liveness axis, below: a live descendant new since the first census holds the stopped shell, which is resumed only once it is gone, at 3 s | `resume-beside-new-live`: "a live new descendant beside a stopped shell's stated seconds were not kept" |
| No listing had a trap command listed inside grace after a resume later than 1 s | R763-8-F2 | The trap's command, live or not, first listed in the last pass before 2 s, after a resume in the pass before | `sigterm-trap-command-after-resume-from-1.5s`: "a next-to-last in-grace resume and its trap command's ..." |
| Every new descendant inside grace was one the product sees as not live, so two mutants that look at liveness survived the whole test | R764-8-F1 | A real process stands for a live new descendant: with no cancelled shell, beside a stopped shell, and as the trap's command in every matrix cell | `sigterm-to-live-new`, `live-trap-command-unspared-after-in-grace-resume`: "a first-pass resume and its live trap command's ..." |
| Every round 8 reviewer mutant joins `MUTANTS` | Ruling item 2 | 13, each with its published edit byte for byte, named in its row. Two interior ones were green: a lone resume at 1 s and one at 10 s now turn them red | Table below |
| Domain notes name the liveness cells; an edge mutant per new cell | Ruling item 3 | The guide's matrix has a live column, and the liveness cells are tabled beside it. Rows 2 to 8 name them. Ten edge mutants | Each red on its own cell's listing alone |
| The first pass's clock | R763-8-R1 | The exact fix: "since its clock is its own length, at most half a second," | |
| The docstring's resume list | R763-8-R2 = R764-8-R1 | The exact fix: "Other listings resume it at 1 s, 3 s, 5.5 s and a tick before 14 s, with that command listed from the resume, and never." | |
| The matrix comment's "the listing above" | R763-8-R3 | The exact fix: "That command after a first-pass resume is the listing "a first-pass resume" above." | |
| Row 5's matrix span can read as a continuous span | R764-8-S1, taken | Said once in the guide: "A cell's domain is its listed resume, not the whole of its class." Reason: it is the reading both the ruling and the review use, and no row's claim changes | |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1, retained, not taken | As in rounds 7 and 8: it predates this PR and is outside #833. Suggested for a new Issue | |

### The liveness axis

A live new descendant is a real process the control starts, live until its input closes, and never really signalled: the starved owner's send only records. Any other new descendant is a number no process has, which the product sees as not live.
- **As the trap's command, a live one is listed from the pass after the resume.** A census taken before the `SIGCONT` cannot list it, and a live one listed in the resume pass would hold the resume.
- **So "late in grace, at the last in-grace pass" is read as the command first listed in the last pass before 2 s,** after a resume in the pass before. This is the latest edge R763-8-F2 names.
  - A zombie the stopped shell has not collected holds nothing.
  - Its `SIGKILL` at 2 s puts that pass a tick before 2 s.
- **Each listing asserts its whole event list, to a tick,** so the behaviour of every row that applies to it.
- **Beyond the ruling's three places,** every matrix cell with a trap command also has it live. So liveness crosses every class of resume.

| Cell | Resume | Live new descendant first listed | Words |
|---|---|---|---|
| With no cancelled shell | none | pass 2, 0.5 s: a survivor's trap starts it; the survivor is spared while it lives, to 4 s | "a live new descendant" |
| Beside a stopped shell, before any resume | 3 s, once it is gone | pass 2, 0.5 s: the child's trap starts it as the child exits | "a live new descendant beside a stopped shell" |
| The trap's command after a resume in pass 1 | 0 s | 0.5 s, inside grace | "a first-pass resume and its live trap command" |
| ... in pass 2 | a tick | 0.5 s and a tick, inside grace | "a second-pass resume and its live trap command" |
| ... a pass before the last in grace | 2 s less two ticks | a tick before 2 s, inside grace, the last pass in grace | "a next-to-last in-grace resume and its live trap command" |
| ... in the last pass in grace | a tick before 2 s | past grace | "a last in-grace resume and its live trap command" |
| ... in the first pass past grace | 2 s | past grace | "a first past-grace resume and its live trap command" |
| ... in the next pass | a tick after 2 s | past grace | "a second past-grace resume and its live trap command" |
| ... in the last pass before 14 s | a tick before 14 s | past grace | "a last-pass resume and its live trap command" |

The cell a pass before the last in grace is listed with a command that is not live as well: "a next-to-last in-grace resume and its trap command". An audit of each listing's passes confirms each resume's pass and clock, and when its command is first listed.

The new listings run after round 8's, so every earlier mutant keeps its words. The liveness listings are in `stated_liveness`, beside the control. The matrix's classes and the stated window moved unchanged to `scripts/process_test_support.py`, as `RESUME_MATRIX` and `window`. So `owner_stated_seconds` stays under the 100-line function limit, at 87 lines, and the test module under the 1000-line ratchet, at 997.

### Every reviewer mutant published in round 8

Each is in `MUTANTS` with the published edit byte for byte, as a check against each reviewer's own script shows. Each is named in its row and red on `owner_stated_seconds` with its words. R763-8's two drop the round prefix; R764-8's keep their published names.

| `MUTANTS` name | R763-8 published name | R764-8 published name | Finding | Row | Words | Red on, every listing checked |
|---|---|---|---|---|---|---|
| `resume-beside-new-live` | `r8-resume-beside-new-live` | | R763-8-F1 | 5 | "a live new descendant beside a stopped shell's ..." | that listing alone |
| `sigterm-trap-command-after-resume-from-1.5s` | `r8-sigterm-trap-command-after-late-grace-resume` | | R763-8-F2 | 6 | "a next-to-last in-grace resume and its trap command's ..." | both next-to-last cells |
| `sigterm-to-live-new` | | `sigterm-to-live-new` | R764-8-F1 | 2 | "a first-pass resume and its live trap command's ..." | the pass-1, pass-2 and next-to-last live cells, both other live new descendants |
| `live-trap-command-unspared-after-in-grace-resume` | | `live-trap-command-unspared-after-in-grace-resume` | R764-8-F1 | 8 | the same | the four in-grace live trap-command cells |
| `live-trap-command-unspared` | | `live-trap-command-unspared` (its control mutant) | R764-8-F1 | 8 | the same | every live trap-command cell; also `owner_shell_window` |
| `interior-past-grace-no-window` | | `interior-past-grace-no-window` | R764-8-S1 | 7 | "a lone ten-second resume's ..." | that listing alone |
| `interior-in-grace-lone-shell-killed` | | `interior-in-grace-lone-shell-killed` | R764-8-S1 | 7 | "a lone one-second resume's ..." | that listing alone |
| `grace-strictly-past` | | `grace-strictly-past` | R764-8 probe | 2 | "a survivor's ..." | |
| `no-window-at-grace-edge` | | `no-window-at-grace-edge` | R764-8 probe | 7 | "a lone first past-grace resume's ..." | the three first past-grace cells |
| `trap-command-spared-only-in-resume-pass-past-grace` | | `trap-command-spared-only-in-resume-pass-past-grace` | R764-8 probe | 8 | "a late resume's ..." | |
| `sigterm-new-beside-stopped-shell-late` | | `sigterm-new-beside-stopped-shell-late` | R764-8 probe | 2 | "a new descendant's ..." | every new descendant before a resume, live or not |
| `resume-held-at-grace-edge` | | `resume-held-at-grace-edge` | R764-8 probe | 5 | "a lone first past-grace resume's ..." | the three first past-grace cells |
| `verdict-from-grace-after-in-grace-resume` | | `verdict-from-grace-after-in-grace-resume` | R764-8 probe | 6 | "a first-pass resume's ..." | |

The two interior mutants were green at round 8, as R764-8-S1 says, since each class was sampled only at its ends. A lone resume at 1 s and one at 10 s, inside a class rather than at either end, now turn them red.

### An edge mutant for each liveness cell

Each breaks one stated behaviour only where its cell is: its liveness, its place, and its class's edge. Run with every listing checked, each is red on its own cell's listing and on no other.

| Cell | Mutant | Row | Breaks | Words |
|---|---|---|---|---|
| live, no cancelled shell | `live-new-sigtermed-with-no-shell` | 2 | `SIGTERM` to it | "a live new descendant's ..." |
| live, beside a stopped shell | `resume-beside-live-new-past-grace` | 5 | the shell resumed beside it once grace is over | "a live new descendant beside a stopped shell's ..." |
| live trap command, pass 1 | `first-pass-live-trap-command-sigtermed` | 6 | `SIGTERM` to it | "a first-pass resume and its live trap command's ..." |
| live trap command, pass 2 | `second-pass-live-trap-command-sigtermed` | 6 | `SIGTERM` to it | "a second-pass resume and its live trap command's ..." |
| trap command a pass before the last in grace, live | `next-to-last-in-grace-live-trap-command-sigtermed` | 6 | `SIGTERM` to it | "a next-to-last in-grace resume and its live trap command's ..." |
| the same, not live | `next-to-last-in-grace-trap-command-sigtermed` | 6 | `SIGTERM` to it | "a next-to-last in-grace resume and its trap command's ..." |
| live trap command, last pass in grace | `last-in-grace-live-trap-command-unspared` | 8 | its window, when first listed past grace | "a last in-grace resume and its live trap command's ..." |
| live trap command, first past grace | `first-past-grace-live-trap-command-unspared` | 8 | its window | "a first past-grace resume and its live trap command's ..." |
| live trap command, next past grace | `second-past-grace-live-trap-command-unspared` | 8 | its window | "a second past-grace resume and its live trap command's ..." |
| live trap command, last pass | `last-pass-live-trap-command-unspared` | 8 | its window | "a last-pass resume and its live trap command's ..." |

Round 8's edge mutants are each red on their own class's cells, live or not. `last-in-grace-trap-command-unspared`, whose edge is any resume in the last half-second of grace, is also red on the two next-to-last cells.

### Round 9 mutation table

`MUTANTS` now holds 142 mutants and `none`, 139 of them with a control. The table names all 139. The 3 with no control are in no row, as in round 8.
- **The default `--mutants` campaign at this head:** `owned-process mutants: PASS (142 mutants, 139 with a control that must fail)`. Each item's commit ran it too.
- **`--matrix` at this head:** all 142 mutants and `none` against every owner control and the whole test, in 4 parts, 1606 runs, each part rc 0 and PASS, with no run cut.
  - `none` is green on all 11.
  - Each of the 139 with a control is red on it with its words, and red on the whole test.
  - The 3 with no control are green on all 11.
- **Every reviewer probe from rounds 6, 7 and 8, unchanged, at this head: no survivor.**
  - The round 8 probes:
    - both of R763-8's mutants are red;
    - R764-8's boundary probe: `none` green, all 8 red, the two interior ones included;
    - R764-8's liveness probe: all 3 red on the whole test.
  - Both round 8 feasibility probes:
    - `none` green on every listing, theirs and this head's;
    - each mutant red on the listing it was written for and on this head's.
  - R763-8's every-listing sweep over 47 mutants: each red on at least one listing.
  - The round 6 and 7 mutant probes: no survivor among their 10, 8, 5 and 4.
  - The round 6 and 7 feasibility probes: as published.
  - `grace_resume_probe.py`: PASS 5 of 5.
  - `grace_resume_probe2.py`: PASS 3 of 3 here. It FAILs 3 of 3 on each of the five `SIGTERM` mutants it was run on, `sigterm-to-live-new` among them: there a real trap command gets `SIGTERM` inside grace.
  - The slowed census and slowed shell-window campaigns: green unmutated, every mutant red.
  - `sigcont_pending.py`: rc 0. Under a launcher that ignores SIGHUP, `--mutants none --matrix` is rc 0.
  - Every table check passes, except R763-6's one-row-per-mutant check, which still reports only `windows-2s`, as it accepted.
- **Disclosed:**
  - R764-7's whole-test mode stops at its own report line on the first red result, as in round 8.
  - Two probes need a `scratch` directory beside their packet, which the published packets do not carry: `rv7_mutants.py` and `slow_shell_window.py`. Each first run stopped there, and the rerun after creating it is the one quoted.
  - The real-process `grace_resume_probe2.py` stays PASS under `live-trap-command-unspared-after-in-grace-resume`. Its trap command finishes before that mutant's `SIGKILL` at 2 s. That mutant is red on the stated-seconds control.

### Round 9 commits

Four one-line commits, one per item, in the ruling's order:
1. the liveness axis;
2. the round 8 reviewer mutants, and the lone resumes at 1 s and 10 s that pin the two interior ones;
3. the domain notes and the edge mutants;
4. the residue and R764-8-S1.

### Round 9 cost

At round 8's head and at this one, interleaved, host load about 42 on 16 CPUs:
- `owner_stated_seconds`, timed inside one process, 20 calls a tree, 3 times: median 29 ms at round 8, 40 ms here;
- run alone as its own process, 0.16 s at both, and every other control within 0.1 s;
- the whole test, 4 runs each, 8 at once: a mean of 60.9 s at both.

Round 9 adds about 11 ms to the preflight, well under the 2 s allowed.

### An observation outside this round

Repeated by the reviewers' repeat probes at load about 42, 16 at once, the unmodified `owner_report` control was red in 4 of 1152 runs:
- at round 8's head, 1 of 512;
- at this head, 3 of 640.

The report was right each time: it read `state R wchan hrtimer_nanosleep` of a child that sleeps 20 ms a loop, after the control had seen it asleep. So it is the control's own race between that wait and the report, not the product. `owner_report` and `_describe` are unchanged in round 9, and every gate run was green. It is disclosed here for a ruling and not changed.

### Round 9 gates

All at head `e803d94b3a11921a293cf036a8eda333d23828f9`, one log and rc each, never piped, SIGHUP at its default in every launcher.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 8 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`. The stated seconds are grace 2 s, verdict 14 s, the parent's `SIGKILL` 4 s and the vanishing verdict 24 s. Resumes are at 0, 1, 3 and 5.5 s and a tick before 14 s, with the matrix at 0 s, a tick, a tick before 2 s, 2 s, a tick after 2 s and a tick before 14 s |
| `python3 scripts/test_suite_cancellation.py --mutants` | rc 0, `owned-process mutants: PASS (142 mutants, 139 with a control that must fail)`. `--matrix`: 4 parts, each PASS |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 9 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

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

