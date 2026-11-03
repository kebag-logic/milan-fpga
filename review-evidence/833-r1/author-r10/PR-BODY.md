[A726j]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Rounds 2 to 8](#rounds-2-to-8)** — Links to each round's published section.
- **[Round 9](#round-9)** — Round 8's findings with both review IDs: a liveness axis for new descendants across every class of resume, beside a stopped shell and with none; every round 8 reviewer mutant; the liveness cells in the domain notes; an edge mutant per liveness cell; the residue and the gates.
- **[Round 10](#round-10)** — Round 9's findings with both review IDs: `owner_report`'s child asleep with no timer; early listings, which list a new descendant a tick after the first pass; a live new descendant beside a shell never resumed; R764-9-S1's three listings; the listing-time domain; the residue, the sweeps and the gates.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally. `833-owned-process` -> `dev`, head `fce77f0efc1425ef7732a8d70c02addc108f7afe` (round 10). Round 10's gates are in [Round 10](#round-10). The full sweep ran at round 1's head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`: 65 of 65 suites, 2,191,394 checks, 0 failures. Rounds 2 to 10 change only files round 1 changed, so the sweep was not rerun. Hosted contexts not yet run.

## Linked Issue / roles

Relates to #833

Executor: `[A726]` (round 1), `[A726b]` (round 2), `[A726c]` (round 3), `[A726d]` (round 4), `[A726e]` (round 5), `[A726f]` (round 6), `[A726g]` (round 7), `[A726h]` (round 8), `[A726i]` (round 9), `[A726j]` (round 10)
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
| `scripts/process_test_support.py` | `FINISH_SECONDS`; every published mutant of the owner and the campaign that runs them (round 5); the starved owner's clock that `owner_stated_seconds` runs on (round 8), with its matrix's classes and its stated window (round 9), a census a listing states, and the reused-identity control's child script (round 10) |
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

Expected result / pass criteria: `suite cancellation: PASS`, whose log prints the planted survivor's `CLEANUP FAILED` line with `state`, `wchan`, `parent` and `age`; `owned-process mutants: PASS (149 mutants, 146 with a control that must fail)`; `mutant lifecycle: PASS`; `RESULT: PASS`; `git diff --check` silent.

Local evidence at this head: every `run:` step of `docs.yml`, as in [Round 10 gates](#round-10-gates); `behave` 2330 steps passed. The full sweep ran in 4 shards, rc 0, at round 1's head.

## Known limitations / out of scope

- **"No suite left to fail by chance" is not absolute, so this is `Relates to`, not `Closes`.** `Probe.ready`'s 15 s handshake is the next bound: it tripped 4 of 10 after this change, at 16 runnable per CPU and host load 250 to 314, with no ownership failure in them. It is not changed here.
- **The host stalls' cause is not named.** They did not recur in 703 cleanups with a sidecar at load near 30. The D wait channels are mapping-lock paths, so contention on mappings shared across the host is an inference, with no kernel trace behind it. A stall beyond 10 s would still fail, naming the state.
- **The #828 replay cannot be classified:** its log has the old message.
- **`owner_survivor` drops SIGKILL at the owner's send,** since no unprivileged control can build an unkillable process.
- **A stuck-process cancellation now fails the run under 34 s of owner clock (44 s for a listing that dies inside every census), not 4 s,** as derived above. The preflight is about 11 s longer, for the timeout control's 10 s, round 2 adds about 1.5 s, the trap command's, round 3 adds 0.8 s, the late-cancel control's, round 4 adds 0.8 s to the shell-window control, round 5 adds about 1.5 s: 1.4 s to the shell-window control and 0.1 s for two new controls, round 6 adds about 0.2 s: the report control's 0.1 s pause and the reused-identity control's second process, rounds 7 and 8 add no measurable time, round 9 adds about 11 ms, and round 10 about 12 ms.
- `ci/image/command-table.json` pins these scripts' hashes and is not regenerated. What commands show, at this head:
  - `python3 -I command_table_staleness.py . 1f29f189 d4d8cff9 HEAD`, with R764-1's script from `review-evidence/833-r1/reviews/R764-1/scripts/` on branch `833-review-evidence`, prints `pins 149 stale 34 absent 1` for `dev` `1f29f189`, and `stale 38` for round 1's head and for this one. The 4 more are the 4 scripts this PR changes, which the table pins.
  - `git grep -l -e command-table.json -e ci_command_table HEAD` lists 14 files that read or name the table, among them `ci/image/build.py` and `scripts/ci_command_table.py`.
  - `git grep -n -F` for each of those 14 file names, `-- .github/workflows scripts/run_all_suites.sh`, prints nothing (rc 1). No workflow or sweep step names a reader of its script pins.
  - Regenerating the table would also rewrite the 34 pins already stale on `dev`, so it is left alone.

## Rounds 2 to 8

Each round's section is kept in that round's published PR body, unchanged:

- [Round 2](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r2/PR-BODY.md#round-2)
- [Round 3](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r3/PR-BODY.md#round-3)
- [Round 4](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r4/PR-BODY.md#round-4)
- [Round 5](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r5/PR-BODY.md#round-5)
- [Round 6](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r6/PR-BODY.md#round-6)
- [Round 7](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r7/PR-BODY.md#round-7)
- [Round 8](https://github.com/kebag-logic/milan-fpga/blob/833-review-evidence/review-evidence/833-r1/author-r8/PR-BODY.md#round-8)

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

## Round 10

Both round 9 reviews of `e803d94b3a11921a293cf036a8eda333d23828f9` are NEGATIVE, and both confirm the round 9 ruling met for every cell it named and the product correct:
- R763-9: two MINOR (F1, F2), one MAJOR (F3), one RESIDUE and one SUGGESTION; R764-6-S1 still retained.
- R764-9: one MINOR (F1, the same as R763-9-F3) and two SUGGESTIONs.

The manager's round 10 ruling on #833 governs this round:
1. fix `owner_report`'s chance failure;
2. the early-in-grace edge;
3. a live new descendant beside a shell never resumed;
4. R764-9-S1's three listings;
5. the listing-time domain, stated once;
6. R763-9-R1's exact fix.

Pin, never narrow. `scripts/owned_process.py` is unchanged since `c1b29617`, and no probe or mutant showed it wrong.

| Finding | IDs | Change | Control and evidence |
|---|---|---|---|
| `owner_report`, in every preflight, failed by chance under load: its child woke every 20 ms, so the report's read could catch it runnable | R763-9-F3 = R764-9-F1 | R763-9-F3's exact fix: the child writes its PID and waits in `signal.pause()`, with no timer of its own. `STUBBORN` is unchanged for the other controls | Below: 0 red in 15,200 runs at load 41 to 78, the round 9 head 33 red beside it. All 6 `owner_report` mutants red with their words |
| No listing listed a new descendant before 0.5 s into cleanup, so `SIGTERM` to one in the first half second survived everything | R763-9-F1 | Each listing whose census grows after the first pass is kept again, early: a census stated a tick after the first pass lists the new descendant first | `early-new-sigtermed-0.5` and its three variants, R763-9's edits byte for byte, named in rows 2 and 6 |
| No listing had a live new descendant beside a shell never resumed, though rows 3 and 4 claim it | R763-9-F2 | R763-9-F2's preferred listing and event list, named in rows 3 and 4 and the liveness table | Both F2 mutants, R763-9's edits byte for byte, and an edge mutant: "a live new descendant beside a shell never resumed's ..." |
| Three cheap listings would close most of R764-9's out-of-domain survivors | R764-9-S1; ruling item 4 | A live trap command after the 1 s resume; the listing beside a shell never resumed (item 3); a parent beside the stopped shell, not under it, with a live new child, killed at 4 s. Rows 2, 6 and 8 drop "not live" at 1 s | 9 of R764-9's sweep survivors are now red |
| A pass time strictly between two sampled passes can read as claimed | R763-9-S1; ruling item 5 | Said once in the guide: "Between stated times the starved owner's passes are half a second apart; a listing's domain is its listed passes." No row's claim changes | |
| The printed summary omitted round 9's listings | R763-9-R1 = R764-9-S2 | R763-9-R1's exact fix: `next_to_last=2 - 2 * TICK, lone=[1, 10], live_new_descendant=True`. S2 asks for the same three facts, so it is taken through it | |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1, retained, not taken | As in rounds 7 to 9: it predates this PR and is outside #833 | |

### `owner_report`

Each campaign runs round 9's head with only this fix beside round 9's head, at the same moment, 8 at once each (R764-9's driver 16), with busy loops of this round's own on its own CPUs in this round's driver. Every red at the round 9 head reads `state R` of the child, after the control had seen it asleep.

| Driver | Fix red | Round 9 head red | Host load |
|---|---:|---:|---|
| This round's, 8 busy loops | 0 of 3000 | 3 of 3000 | 41 to 57 |
| The same, 16 busy loops | 0 of 3000 | 5 of 3000 | 55 to 69 |
| The same, 24 busy loops | 0 of 3000 | 5 of 3000 | 66 to 78 |
| R763-9's `stress_owner_report.py`, 3000, 8 at once | 0 of 3000 | 12 of 3000 | about 48 at the end |
| R764-9's `repeat_control.sh`, 16 x 200 | 0 of 3200 | 8 of 3200 | mean 55 |

So 0 of 15,200 against 33 of 15,200, one-sided Fisher p = 1.1e-10. At the final head both reviewers' drivers again give 0 of 3000 and 0 of 3200, at load 35 to 50, mean 44. Each `owner_report` mutant is red with its words, once and in 20 more campaigns.

### The early edge

A listing can now state a census: the starved owner's clock lands a pass on its time, and the events note it there, so the listing's own assertion proves the pass was placed. Each listing whose census lists, a tick in, a descendant its first census did not is kept again as an early listing: the same listing and events, with a census stated a tick after the first pass. Its new descendant is then first listed there. Its words are the listing's, made early. No earlier listing changes, and every round 9 listing classifies as before.

| Early listing | Its new descendant, first listed a tick in |
|---|---|
| "an early first-pass resume" | the trap's command after a first-pass resume, not live |
| "an early first-pass resume and its live trap command" | the same, live |
| "an early new descendant" | with no cancelled shell, a command a survivor's trap starts, not live |
| "an early live new descendant" | the same, live, so the survivor is spared to 4 s |
| "an early new descendant beside a stopped shell" | a command the child's trap starts while the shell is stopped and never resumed, not live |
| "an early live new descendant beside a stopped shell" | a live one the child's trap starts as the child exits, holding the shell until 3 s |
| "an early live new descendant beside a shell never resumed" | item 3's, early |
| "an early parent beside a stopped shell and its live new descendant" | item 4's, early |

| Mutant | Edit | Words | Red on, every listing checked |
|---|---|---|---|
| `early-new-sigtermed-0.25` | `SIGTERM` to any new descendant listed before 0.25 s | "an early first-pass resume's ..." | all 8 early listings |
| `early-new-sigtermed-0.5` | the same, before 0.5 s | the same | all 8 |
| `early-trap-command-sigtermed` | the same, after a resume | the same | the 2 early first-pass ones |
| `early-live-new-sigtermed` | the same, live ones only | "an early first-pass resume and its live trap command's ..." | the 5 early live ones |

R763-9's audit of each listing's passes now finds a new descendant listed a tick after the first pass in 8 listings; at round 9 its earliest was 0.5 s.

### Beside a shell never resumed, and R764-9-S1

- **R763-9-F2's preferred listing:** a cancelled shell never resumed; its child, from the first census, outlives its `SIGKILL`; from pass 2 the child's trap starts a live new descendant that outlives 14 s. Stated: `SIGTERM` the child at 0; `SIGKILL` the trap's command at 2; `SIGKILL` the child at 4; at 14, `SIGKILL` the shell, the child and the trap's command, then the verdict. It is R764-9-S1's second listing too.
- **R764-9-S1's third listing:** the same with the child a parent beside the shell, not under it. Its live new child spares it to 4 s, and the shell is never resumed.
- **R764-9-S1's first listing:** a live trap command after the resume at 1 s, first listed from the pass after it, at 1.5 s, inside grace: "a one-second resume and its live trap command".

| Mutant | Edit | Row | Red on, every listing checked |
|---|---|---|---|
| `parent-of-live-new-unspared-beside-shell` | R763-9's: a live new child spares no parent while a shell is cancelled | 3 | both listings beside a shell never resumed and their early ones |
| `verdict-early-live-new-beside-stopped-shell` | R763-9's: the verdict a pass early beside a stopped shell with a live new descendant | 4 | the same 4 |
| `parent-under-unresumed-shell-unspared` | edge: a parent under a shell not yet resumed is not spared by its live child | 3 | item 3's listing and its early one alone |

### Room under the module ratchet

Both Python modules sat at the 1000-line module ratchet, and the ratchet's budget has no slack. So two changes create room, and neither changes a value:
- `BLOCKING`, the reused-identity control's child script, moves unchanged into `scripts/process_test_support.py`;
- 17 `MUTANTS` entries' words continue at the dict's own 8-space indent, as its edits already do, where that takes fewer lines.

A check of the dict at each commit finds every round 9 entry identical and in order, the new ones appended, and `BLOCKING` byte-identical. The lines reviewer probes patch are unchanged, so every probe ran unedited. The test module is 999 lines and the support module 996.

### Round 10 mutation table

`MUTANTS` now holds 149 mutants and `none`, 146 of them with a control. The table names all 146. The 3 with no control are in no row, as before.
- **The default `--mutants` campaign at this head:** `owned-process mutants: PASS (149 mutants, 146 with a control that must fail)`. Each item's commit ran it too.
- **`--matrix` at this head:** all 149 mutants and `none` against every owner control and the whole test, in 4 parts, 1683 runs, each part rc 0 and PASS, with no run cut.
  - `none` is green on all 11.
  - Each of the 146 with a control is red on it with its words, and red on the whole test.
  - The 3 with no control are green on all 11.

### Each reviewer's round 9 sweep, at this head

- **R763-9's sweep:** 4224 mutants: 2716 equivalent, as at round 9; 1107 killed (1068); 401 survivors (440).
  - Every variant R763-9 counted under F1 and F2 is killed by `owner_stated_seconds`.
  - R763-9's own classifier finds 12 survivor classes that touch a listed cell, and the same 12 with this round's two new cells claimed.
  - They are its own round 9 out-of-domain classes:
    - the 6 `five-half` ones, through its probe's shape;
    - the 6 that act only between two sampled passes, which the guide now places outside a listing's domain.
- **R764-9's sweep:** 99 mutants. 24 survive every control and the whole test (33 at round 9), and one more is red only on `owner_shell_window`, as before.
  - The 9 killed since round 9:
    - the five live-command ones at 1 s, by R764-9-S1's first listing;
    - both verdict ones beside a shell never resumed and `D/shell`, by the two listings beside a shell never resumed;
    - `E/C2`, by an early listing.
  - No survivor is new. The 24 are R764-9's own round 9 classes: 6 equivalent, 18 outside a listed domain.
- **R763-9's natural forms:** all 6 survivors are now red on `owner_stated_seconds` and on the whole test.
- **R763-9's cell probe:** 65 of 65 cells pass.
- **R763-9's F2 feasibility probe:** both F2 mutants red, with or without its own added listing.
- **Byte checks:** 13 of 13 round 8 edits identical, and R763-9's six published edits too.

So no survivor falls inside a stated domain.

### Every reviewer probe from rounds 6 to 9, at this head

Each from its packet, copied fresh and checked against its manifest, run unchanged. No survivor.
- **Round 8:**
  - R763-8's two mutants are red, and its every-listing sweep has each of 47 red on at least one listing.
  - R764-8's boundary probe: all 8 red. Its liveness probe: all 3 red on the whole test.
  - Both feasibility probes behave as published. Their added listings get early ones too, by the same rule.
- **Rounds 6 and 7:**
  - the mutant probes: no survivor among their 8, 10, 5 and 4;
  - the feasibility probes: as published;
  - `grace_resume_probe.py`: PASS 5 of 5;
  - `grace_resume_probe2.py`: PASS 3 of 3, and FAIL 3 of 3 on each of the five `SIGTERM` mutants;
  - `slow_shell_window.py`: PASS, 45 runs;
  - `sigcont_pending.py`: rc 0;
  - under a launcher that ignores SIGHUP, `--mutants none --matrix`: rc 0;
  - the repeat probes: all green, `owner_report` 128 of 128.
- **Every table check passes,** except R763-6's one-row-per-mutant check. It reports `windows-2s`, as it accepted at round 6, and the four early mutants, which the ruling names in rows 2 and 6.
- **Disclosed:**
  - R763-6's slowed census at 0.5 s a pass on `owner_shell_window` was green once for `trap-commands-1s`. That run ran beside the docs.yml jobs and took 42.5 s; 6 repeats were red with the words, in 36.5 s. At that pass time the mutant's 1 s kill and the trap's 1.5 s command race on wall time. `trap-commands-1s`'s own control, `owner_stated_seconds`, is red on every run.
  - `r7_mutants.py`, `rv7_mutants.py` and `slow_shell_window.py` need a `scratch` directory beside their packet. `r7_mutants.py`'s first run stopped there; the rerun is the one quoted.
  - R764-7's whole-test mode stops at its own report line on the first red result, as in rounds 8 and 9.

### Round 10 commits

Six one-line commits, one per item, in the ruling's order:
1. `owner_report`'s child;
2. the early listings and their four mutants, and the room for them;
3. the listing beside a shell never resumed and its three mutants;
4. R764-9-S1's other two listings;
5. the listing-time domain;
6. the summary line.

### Round 10 cost

At round 9's head and at this one, interleaved, beside the docs.yml jobs, on 16 CPUs:
- `owner_stated_seconds`, timed inside one process, 20 calls a tree, 3 times: median 40 ms at round 9, 52 ms here;
- run alone as its own process: 0.16 s at both. `owner_report` takes 0.26 s at both, and every other control is within 0.05 s;
- the whole test, 4 runs each, 8 at once: a mean of 60.4 s at round 9 and 60.6 s here.

Round 10 adds about 12 ms to the preflight, well under the 2 s allowed.

### Round 10 gates

All at head `fce77f0efc1425ef7732a8d70c02addc108f7afe`, one log and rc each, never piped, SIGHUP at its default in every launcher.

| Gate | Result |
|---|---|
| Every `run:` step of `.github/workflows/docs.yml`, each job on a fresh clone of this head | Verifier rc 0: 64 steps rc 0, 31 not run with the round 1 reason unchanged (hosted-only or apt), 0 bad. Tree clean after each job. Builder legs in it: `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`, as in rounds 1 to 9 |
| `python3 scripts/test_suite_cancellation.py` | rc 0, `suite cancellation: PASS`. The summary line now also prints the next-to-last in-grace resume, the lone resumes at 1 s and 10 s, and the liveness axis |
| `python3 scripts/test_suite_cancellation.py --mutants` | rc 0, `owned-process mutants: PASS (149 mutants, 146 with a control that must fail)`. `--matrix`: 4 parts, each PASS |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | rc 0, `mutant lifecycle: PASS` |
| `cd tests && behave` | rc 0: 14 features, 508 scenarios, 2330 steps passed, 0 failed |
| `git diff --check 1f29f189 HEAD` | rc 0 |
| Full sweep | Not rerun: round 10 changes only files round 1 changed. It ran at `d4d8cff9`: 65 of 65 suites, rc 0 on all 4 shards |

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
