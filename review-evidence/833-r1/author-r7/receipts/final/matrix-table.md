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
| shell-window-1s | RED | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 4 |
| trap-commands-no-window | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-commands-never-spared | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| trap-commands-1s | RED | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 4 |
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
| killed-not-recorded | ok | ok | ok | ok | ok | RED | ok | ok | RED | ok | RED | 3 |
| no-sigcont-after-send | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| sigterm-to-new | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
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
| verdict-kills-only-the-killed | ok | ok | ok | ok | ok | RED | ok | ok | RED | ok | RED | 3 |
| report-parent-is-first-parent | RED | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | 2 |
| rv6-sigkill-by-number | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| rv6-sigcont-by-number | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| rv6-resume-not-before-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| rv6-resume-not-first-pass | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| rv6-sigterm-trap-commands | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-to-new-before-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigcont-by-number-after-kill | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| recheck-spares-sigkill | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| grace-a-tick-short | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| kill-all-a-tick-early | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| verdict-a-tick-early | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| verdict-waits-for-resume | ok | ok | ok | ok | ok | RED | ok | RED | RED | ok | RED | 4 |
| no-resume-before-verdict | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| trap-window-a-tick-short | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| no-window-inside-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| trap-commands-spared-only-past-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| cap-lifted-past-a-minute | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| tick-passes-count-nothing | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| vanishing-verdict-ignores-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| no-reap-after-first-census | ok | ok | RED | ok | ok | ok | ok | RED | RED | ok | RED | 4 |
| sigterm-rechecks-parent | ok | RED | ok | ok | ok | ok | ok | ok | RED | ok | RED | 3 |
| resume-collected-shell-past-grace | ok | ok | ok | ok | ok | ok | ok | RED | ok | ok | RED | 2 |
| verdict-sends-sigterm | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| killed-ago-from-start | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| rv6-return-before-confirm | ok | ok | ok | ok | ok | ok | RED | RED | RED | ok | RED | 4 |

- cleanup-does-nothing / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- sigterm-checks-parent: no control; red on nothing
- send-checks-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- no-start-recheck / reused_identity: AssertionError: a census entry whose process was replaced was signalled
- no-reap-after-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 291175 (python3) state Z wchan 0 parent 291170 (first 
- owned-is-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 179030 exited during this report
- deadline-wall-clock / stall: AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-1s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.5, 'SIGKILL', 'survivor'), (10.0, 'SIGKILL', '
- pass-cap-1.5s / stall: AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-5s / stall: AssertionError: the stall was charged in full: SIGKILL in pass [2]
- windows-2s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (6.0, 'SIGKILL', 's
- reap-window-2s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (6.0, 'SIGKILL', 's
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
- killed-counts-as-gone / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (24.0, 'verdict')]
- report-without-state / report: AssertionError: ('state S', 'pid 199262 (python3) wchan hrtimer_nanosleep parent 199215 (first parent 199215) age 0.14 s start 77992872, not sent SIGKILL')
- report-without-wchan / report: AssertionError: ('wchan ', 'pid 264183 (python3) state S parent 264178 (first parent 264178) age 0.12 s start 78010686, not sent SIGKILL')
- report-without-state-or-wchan / report: AssertionError: ('state S', 'pid 315959 (python3) parent 315950 (first parent 315950) age 0.14 s start 78030281, not sent SIGKILL')
- grace-1s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.0, 'SIGKILL', 'survivor'), (13.0, 'SIGKILL', '
- return-with-zombies / late_exit: AssertionError: cleanup returned with an owned child unreaped
- vanishing-waits-no-more / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 317661 exited during this report
- resume-with-one-live / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'chil
- clock-always-cap / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.5, 'SIGKILL', 'survivor'), (13.0, 'SIGKILL', '
- killed-not-recorded / survivor: AssertionError: ('sent SIGKILL ', 'CLEANUP FAILED: owned descendants remain after 1.03 s, 27 census passes, slowest 0.02 s: pid 318646 (bash) state T wchan do_s
- no-sigcont-after-send: no control; red on nothing
- sigterm-to-new / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 'trap command'), (10.0, 'S
- no-leaf-first: no control; red on nothing
- signal-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGTERM', 'SIGCONT']
- parent-spared-past-kill-all / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- parents-killed-at-grace / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- vanishing-waits-30s-more / stated_seconds: AssertionError: a vanishing listing's stated seconds were not kept on the owner's clock: [(44.0, 'verdict')]
- report-without-current-parent / report: AssertionError: the report's current parent is not its own field: pid 210084 (python3) state S wchan hrtimer_nanosleep (first parent 1) age 0.14 s start 7799611
- report-age-in-ticks / report: AssertionError: the report's age is not the process's own, 0.10 to 0.12 s: pid 270534 (python3) state S wchan hrtimer_nanosleep parent 270529 (first parent 2705
- check-before-open / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGTERM', 'SIGCONT']
- no-sigterm / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(2.0, 'SIGKILL', 'survivor'), (14.0, 'SIGKILL', 'survivor'), (14.0, 'verdict')]
- kill-all-a-pass-late / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- verdict-past-deadline / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (14.5, 'SIGKILL', '
- resume-only-when-alone / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (5.5, 'SIGKILL', 'trap
- trap-window-from-grace / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (5.5, 'SIGCONT', 'shel
- shell-spared-only-while-stopped / shell_window: AssertionError: the shell was killed in the pass that resumed it, before its trap
- trap-commands-until-grace / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- cap-on-total / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.5, 'SIGKILL', 'survivor'), (13.0, 'SIGKILL', '
- first-pass-full-cap / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.5, 'SIGKILL', 'survivor'), (13.5, 'SIGKILL', '
- vanishing-waits-from-grace / stated_seconds: AssertionError: a vanishing listing's stated seconds were not kept on the owner's clock: [(22.0, 'verdict')]
- verdict-counts-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 276455 exited during this report
- sigterm-needs-live-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- resume-unless-reaped-now / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- verdict-kills-only-the-killed / survivor: AssertionError: stopped shell left behind
- report-parent-is-first-parent / report: AssertionError: the report's current parent is not its own field: pid 322814 (python3) state S wchan hrtimer_nanosleep parent 1 (first parent 1) age 0.15 s star
- rv6-sigkill-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGKILL']
- rv6-sigcont-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGCONT']
- rv6-resume-not-before-grace / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(2.0, 'SIGCONT', 'shell'), (12.0, 'SIGKILL', 'shell'), (12.0, 'SIGKILL
- rv6-resume-not-first-pass / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.5, 'SIGCONT', 'shell'), (10.5, 'SIGKILL', 'shell'), (10.5, 'SIGKILL
- rv6-sigterm-trap-commands / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 'trap command'), (10.0, 'S
- sigterm-to-new-before-resume / stated_seconds: AssertionError: a new descendant's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (0.5, 'SIGTERM', 'cleanup command'), (2.0, 
- sigcont-by-number-after-kill / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGCONT']
- recheck-spares-sigkill / reused_identity: AssertionError: a census entry whose process was replaced was signalled
- grace-a-tick-short / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.9999990463256836, 'SIGKILL', 'survivor'), (13.
- kill-all-a-tick-early / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- verdict-a-tick-early / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (13.999999046325684
- verdict-waits-for-resume / stated_seconds: AssertionError: cleanup never reached a verdict on the owner's clock
- no-resume-before-verdict / stated_seconds: AssertionError: a last-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (13.9999990463256
- trap-window-a-tick-short / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (5.5, 'SIGCONT', 'shel
- no-window-inside-grace / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (4.0, 'SIGKILL', 'shell'), (4.0, 'SIGKILL',
- trap-commands-spared-only-past-grace / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (2.0, 'SIGKILL', 'trap command'), (10.0, 'S
- cap-lifted-past-a-minute / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.0, 'SIGKILL', 'survivor'), (1.0, 'verdict')]
- tick-passes-count-nothing / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.5, 'SIGKILL', 'survivor'), (14.5, 'SIGKILL', '
- vanishing-verdict-ignores-resume / stated_seconds: AssertionError: a resumed vanishing listing's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (13.9999
- no-reap-after-first-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.50 s, 1 census passes, slowest 0.50 s: pid 32103 (python3) state Z wchan 0 parent 32097 (first pa
- sigterm-rechecks-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- resume-collected-shell-past-grace / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- verdict-sends-sigterm / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (14.0, 'SIGTERM', '
- killed-ago-from-start / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- rv6-return-before-confirm / vanishing: AssertionError: an endless listing did not fail the run

problems: none
