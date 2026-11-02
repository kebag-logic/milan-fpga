| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | stated_seconds | reused_identity | whole | red |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|
| none | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| cleanup-does-nothing | ok | RED | RED | RED | RED | RED | RED | RED | RED | ok | RED | 9 |
| identity-start-holds-parent | ok | RED | ok | ok | ok | ok | ok | ok | ok | RED | RED | 3 |
| identity-keys-hold-parent | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| identity-first-census-holds-parent | ok | RED | ok | ok | ok | RED | ok | ok | RED | ok | RED | 4 |
| identity-includes-parent | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| identity-checks-parent-before-send | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| sigterm-checks-parent | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| send-checks-parent | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| no-start-recheck | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| no-reap-after-census | ok | ok | RED | ok | ok | ok | ok | RED | RED | ok | RED | 4 |
| owned-is-census | ok | ok | RED | ok | ok | ok | ok | RED | RED | ok | RED | 4 |
| deadline-wall-clock | ok | ok | ok | RED | ok | ok | ok | ok | RED | ok | RED | 3 |
| pass-cap-1s | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| pass-cap-1.5s | ok | ok | ok | RED | ok | ok | ok | ok | RED | ok | RED | 3 |
| pass-cap-5s | ok | ok | ok | RED | ok | ok | ok | ok | RED | ok | RED | 3 |
| windows-2s | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| reap-window-2s | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| no-shell-window | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| no-shell-window-kept | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| no-shell-window-pass | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| no-trap-window | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| root-killed-unresumed | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| shell-killed-when-resumed | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| shell-window-one-pass | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| shell-window-1s | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-commands-no-window | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-commands-never-spared | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-commands-1s | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED | ok | ok | RED | 2 |
| window-without-resume | ok | ok | ok | ok | ok | ok | ok | RED | ok | ok | RED | 2 |
| rearm-without-sigcont | ok | ok | ok | ok | RED | ok | ok | RED | RED | ok | RED | 4 |
| resume-while-listed | ok | ok | ok | ok | ok | ok | ok | RED | ok | ok | RED | 2 |
| no-kill-before-raise | ok | ok | ok | ok | ok | RED | ok | ok | RED | ok | RED | 3 |
| no-kill-before-raise-empty | ok | ok | ok | ok | ok | RED | ok | ok | RED | ok | RED | 3 |
| kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED | ok | ok | RED | ok | RED | 3 |
| endless-unbounded | ok | ok | ok | ok | ok | ok | RED | RED | RED | ok | RED | 4 |
| survivor-never-fails | ok | ok | ok | ok | ok | RED | RED | RED | RED | ok | RED | 5 |
| survivor-never-fails-guarded | ok | ok | ok | ok | ok | RED | RED | RED | RED | ok | RED | 5 |
| trust-sigkill | ok | ok | ok | ok | ok | RED | ok | ok | RED | ok | RED | 3 |
| killed-counts-as-gone | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| report-without-state | RED | ok | ok | ok | ok | RED | ok | ok | ok | ok | RED | 3 |
| report-without-wchan | RED | ok | ok | ok | ok | RED | ok | ok | ok | ok | RED | 3 |
| report-without-state-or-wchan | RED | ok | ok | ok | ok | RED | ok | ok | ok | ok | RED | 3 |
| grace-1s | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| return-with-zombies | ok | ok | RED | ok | ok | ok | RED | RED | RED | ok | RED | 5 |
| vanishing-waits-no-more | ok | ok | RED | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| resume-with-one-live | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| clock-always-cap | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| killed-not-recorded | ok | ok | ok | ok | ok | RED | ok | ok | ok | ok | RED | 2 |
| no-sigcont-after-send | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| sigterm-to-new | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| no-leaf-first | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| signal-by-number | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| parent-spared-past-kill-all | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| parents-killed-at-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| vanishing-waits-30s-more | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| report-without-current-parent | RED | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | 2 |
| report-age-in-ticks | RED | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | 2 |
| check-before-open | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| no-sigterm | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| kill-all-a-pass-late | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| verdict-past-deadline | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| resume-only-when-alone | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-window-from-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| shell-spared-only-while-stopped | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-commands-until-grace | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| cap-on-total | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| first-pass-full-cap | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| vanishing-waits-from-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| verdict-counts-census | ok | ok | RED | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| sigterm-needs-live-parent | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| resume-unless-reaped-now | ok | ok | ok | ok | ok | ok | ok | RED | ok | ok | RED | 2 |
| verdict-kills-only-the-killed | ok | ok | ok | ok | ok | RED | ok | ok | ok | ok | RED | 2 |
| report-parent-is-first-parent | RED | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | 2 |

- cleanup-does-nothing / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- sigterm-checks-parent: no control; red on nothing
- send-checks-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- no-start-recheck / reused_identity: AssertionError: a census entry whose process was replaced was signalled
- no-reap-after-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 1906700 (python3) state Z wchan 0 parent 1906669 (firs
- owned-is-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 1907327 exited during this report
- deadline-wall-clock / stall: AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-1s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (15, 'SIGKILL', 'surviv
- pass-cap-1.5s / stall: AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-5s / stall: AssertionError: the stall was charged in full: SIGKILL in pass [2]
- windows-2s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (13, 'SIGKILL', 'surviv
- reap-window-2s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (13, 'SIGKILL', 'surviv
- no-shell-window / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-kept / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-pass / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- root-killed-unresumed / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-window-one-pass / shell_window: AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- shell-window-1s / shell_window: AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- trap-commands-no-window / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-never-spared / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- resume-collected-shell / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- window-without-resume / late_cancel: AssertionError: cleanup never reached a verdict after a late cancel
- rearm-without-sigcont / late_cancel: AssertionError: cleanup never reached a verdict after a late cancel
- resume-while-listed / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- no-kill-before-raise / survivor: AssertionError: stopped shell left behind
- no-kill-before-raise-empty / survivor: AssertionError: stopped shell left behind
- kill-before-fail-spares-shell / survivor: AssertionError: stopped shell left behind
- endless-unbounded / vanishing: AssertionError: cleanup never reached a verdict
- survivor-never-fails / survivor: AssertionError: a survivor never failed the run
- survivor-never-fails-guarded / survivor: AssertionError: a survivor never failed the run
- trust-sigkill / survivor: AssertionError: a survivor never failed the run
- killed-counts-as-gone / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (49, 'verdict')]
- report-without-state / report: AssertionError: ('state S', 'pid 1947294 (python3) wchan hrtimer_nanosleep parent 1947265 (first parent 1947265) age 0.14 s start 77135202, not sent SIGKILL')
- report-without-wchan / report: AssertionError: ('wchan ', 'pid 1948109 (python3) state S parent 1948106 (first parent 1948106) age 0.14 s start 77135778, not sent SIGKILL')
- report-without-state-or-wchan / report: AssertionError: ('state S', 'pid 1948375 (python3) parent 1948365 (first parent 1948365) age 0.14 s start 77136254, not sent SIGKILL')
- grace-1s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (27, 'SIGKILL', 'surviv
- return-with-zombies / late_exit: AssertionError: cleanup returned with an owned child unreaped
- vanishing-waits-no-more / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 1948785 exited during this report
- resume-with-one-live / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGCONT', 'shell'), (1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (
- clock-always-cap / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (4, 'SIGKILL', 'survivor'), (28, 'SIGKILL', 'surviv
- killed-not-recorded / survivor: AssertionError: ('sent SIGKILL ', 'CLEANUP FAILED: owned descendants remain after 1.03 s, 25 census passes, slowest 0.02 s: pid 1949188 (bash) state T wchan do_
- no-sigcont-after-send: no control; red on nothing
- sigterm-to-new: no control; red on nothing
- no-leaf-first: no control; red on nothing
- signal-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands
- parent-spared-past-kill-all / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'parent'), (1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child
- parents-killed-at-grace / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'parent'), (1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'paren
- vanishing-waits-30s-more / stated_seconds: AssertionError: a vanishing listing's stated seconds were not kept: [(89, 'verdict')]
- report-without-current-parent / report: AssertionError: the report's current parent is not its own field: pid 1954931 (python3) state S wchan hrtimer_nanosleep (first parent 1) age 0.15 s start 771458
- report-age-in-ticks / report: AssertionError: the report's age is not the process's own, 0.10 to 0.14 s: pid 1956257 (python3) state S wchan hrtimer_nanosleep parent 1956247 (first parent 19
- check-before-open / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands
- no-sigterm / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(5, 'SIGKILL', 'survivor'), (29, 'SIGKILL', 'survivor'), (29, 'verdict')]
- kill-all-a-pass-late / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'parent'), (1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child
- verdict-past-deadline / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (30, 'SIGKILL', 'surviv
- resume-only-when-alone / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGKILL', 'trap comm
- trap-window-from-grace / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), 
- shell-spared-only-while-stopped / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- trap-commands-until-grace / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- cap-on-total / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (4, 'SIGKILL', 'survivor'), (28, 'SIGKILL', 'surviv
- first-pass-full-cap / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (4, 'SIGKILL', 'survivor'), (28, 'SIGKILL', 'surviv
- vanishing-waits-from-grace / stated_seconds: AssertionError: a vanishing listing's stated seconds were not kept: [(45, 'verdict')]
- verdict-counts-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 1967696 exited during this report
- sigterm-needs-live-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- resume-unless-reaped-now / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- verdict-kills-only-the-killed / survivor: AssertionError: stopped shell left behind
- report-parent-is-first-parent / report: AssertionError: the report's current parent is not its own field: pid 1970576 (python3) state S wchan hrtimer_nanosleep parent 1 (first parent 1) age 0.14 s sta

problems: none
