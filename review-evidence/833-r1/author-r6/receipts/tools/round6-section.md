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

| Row (`TESTING.md:262-277`) | Pinned by | Mutants that prove it (round 6 own mutant last) |
|---|---|---|
| Signals only through the handle, after the start-time recheck | `reused_identity` | `no-start-recheck`, `signal-by-number`, `check-before-open` |
| SIGTERM in the first pass; 2 s before the first SIGKILL | `stated_seconds` | `grace-1s`, `no-sigterm` |
| By 4 s SIGKILL has reached all but the cancelled shell and its trap's commands; a parent spared until then while its child lives | `stated_seconds`, `shell_window` | `parent-spared-past-kill-all`, `parents-killed-at-grace`, `root-killed-unresumed`, `kill-all-a-pass-late` |
| A survivor fails the run at 14 s, in the first pass at or past it, even with a stopped shell | `stated_seconds`, `survivor` | `reap-window-2s`, `windows-2s`, `killed-counts-as-gone`, `survivor-never-fails`, `survivor-never-fails-guarded`, `trust-sigkill`, `verdict-past-deadline` |
| The shell is resumed in the first pass in which no other descendant lives | `stated_seconds` | `resume-with-one-live`, `resume-only-when-alone` |
| From the resume, a 10 s window for the shell and its trap's commands; the deadline 20 s after the resume | `stated_seconds` | `windows-2s`, `trap-window-from-grace` |
| No SIGKILL to the resumed shell inside its window, through builtins too | `shell_window` | `no-shell-window`, `no-shell-window-kept`, `no-shell-window-pass`, `no-trap-window`, `shell-killed-when-resumed`, `shell-window-one-pass`, `shell-window-1s`, `shell-spared-only-while-stopped` |
| Nor to a command its trap starts | `shell_window` | `trap-commands-no-window`, `trap-commands-never-spared`, `trap-commands-1s`, `trap-commands-until-grace` |
| At most 0.5 s of owner clock a pass | `stall`, `stated_seconds` | `deadline-wall-clock`, `pass-cap-1.5s`, `pass-cap-5s`, `pass-cap-1s`, `cap-on-total` |
| A shorter pass adds its own length | `stated_seconds`, `shell_window` | `clock-always-cap`, `first-pass-full-cap` |
| A vanishing listing fails the run 10 s after the deadline, and no later | `vanishing`, `late_exit`, `stated_seconds` | `endless-unbounded`, `vanishing-waits-no-more`, `vanishing-waits-30s-more`, `vanishing-waits-from-grace` |
| Every exited child collected; cleanup returns only after a census that lists nothing | `late_exit` | `no-reap-after-census`, `owned-is-census`, `return-with-zombies`, `verdict-counts-census` |
| A re-parented descendant keeps its identity and its SIGTERM in that pass | `reparented` | `cleanup-does-nothing`, five `identity-*`, `send-checks-parent`, `sigterm-needs-live-parent` |
| No window after the shell was collected | `late_cancel` | `resume-collected-shell`, `window-without-resume`, `rearm-without-sigcont`, `resume-while-listed`, `resume-unless-reaped-now` |
| A failing run SIGKILLs all it reports, the stopped shell included | `survivor` | `no-kill-before-raise`, `no-kill-before-raise-empty`, `kill-before-fail-spares-shell`, `verdict-kills-only-the-killed` |
| The message: state, wait channel, current parent apart from the first, age, time since SIGKILL | `report`, `survivor` | `report-without-state`, `report-without-wchan`, `report-without-state-or-wchan`, `report-without-current-parent`, `report-age-in-ticks`, `killed-not-recorded`, `report-parent-is-first-parent` |

**Not pinned by a control** (`:279-283`), so not part of the contract. These are three reasons the product's comments give:
- `SIGCONT` after each signal: `SIGKILL` ends a stopped descendant at grace either way.
- No `SIGTERM` during grace to a descendant new since the first census: it is killed at grace either way.
- A first-census parent's extra second after grace: its SIGKILL is still bounded by 4 s, which the table pins.

Their mutants are R764-5-S1's three: `no-sigcont-after-send`, `sigterm-to-new` and `no-leaf-first`. Each is in `MUTANTS` with no control and that reason, and each is green on all 11 targets. The ones R764-5-S1 found red on a control (`clock-always-cap`, `killed-not-recorded`, `vanishing-waits-no-more`) are listed with that control. So R764-5-S1 is taken too.

**Every published mutant is listed.** The 15 mutants R763-5 and R764-5 published are 13 distinct mutated files. Each equals a committed entry by hash. The two duplicates are `r5-parent-with-live-child-spared` = `rv-parent-spared-past-kill-all` and `r5-vanishing-fails-at-limit` = `rv-vanishing-waits-no-more`. Run unchanged at this head, both reviewers' own probes and mutant files give:
- `probe_mutants.py` and R763-5's `add_mutants.py` matrix: every one of their mutants of a stated behaviour is red on a control and the whole test, and `none` is green on all 11.
- `probe_effect.py`: the head's row is R764-5's own.
- `kill_all_probe.py` and `report_probe.py`: rc 0 at the head, rc 1 on each mutant.

### The lane's own mutant for each row

Each breaks its row differently from the published ones, and each is red on its control with its words, three runs out of three.

| Row | Mutant | Edit | Control: words |
|---|---|---|---|
| Handle | `check-before-open` | the identity recheck moved before the handle is opened | `reused_identity`: "a census entry was signalled by its number" |
| SIGTERM, grace | `no-sigterm` | no SIGTERM at all | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Second stage | `kill-all-a-pass-late` | `clock < kill_all` -> `clock <= kill_all` | `stated_seconds`: "a stubborn parent's stated seconds were not kept" |
| 14 s | `verdict-past-deadline` | `clock >= limit` -> `clock > limit` | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Resume | `resume-only-when-alone` | resume only when nothing else is listed, zombies included | `stated_seconds`: "a late resume's stated seconds were not kept" |
| Window, 20 s | `trap-window-from-grace` | the window counted from grace, not from the resume | `stated_seconds`: "a late resume's stated seconds were not kept" |
| No SIGKILL in the window | `shell-spared-only-while-stopped` | the shell spared only while its state is `T` | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| Trap commands | `trap-commands-until-grace` | a trap's command spared only until grace + 1 s | `shell_window`: "the resumed shell's trap command was killed inside the shell's window" |
| 0.5 s a pass | `cap-on-total` | the cap bounds the clock's total, not each pass | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Short passes | `first-pass-full-cap` | the first pass charged the full cap | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Vanishing | `vanishing-waits-from-grace` | the verdict at grace + 20 s, 22 s, not 24 s | `stated_seconds`: "a vanishing listing's stated seconds were not kept" |
| Collected, reaped | `verdict-counts-census` | the verdict judges the census, collected ones included | `late_exit`: "CLEANUP FAILED: owned descendants remain" |
| Re-parented | `sigterm-needs-live-parent` | no SIGTERM while the census's parent is not live | `reparented`: "SIGTERM waited for a later census" |
| Late cancel | `resume-unless-reaped-now` | resume unless the shell was collected in this very pass | `late_cancel`: "a cancel after the shell was collected resumed it" |
| Failing run | `verdict-kills-only-the-killed` | the verdict SIGKILLs only what was SIGKILLed before | `survivor`: "stopped shell left behind" |
| Message | `report-parent-is-first-parent` | the first parent printed as the current one | `report`: "the report's current parent is not its own field" |

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

All at head `HEAD_SHA`, one log and rc each, never piped.

GATES_TABLE
