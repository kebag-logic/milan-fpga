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
| sigkill-by-number | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| sigcont-by-number | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| resume-not-before-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| resume-not-first-pass | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-trap-commands | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
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
| return-before-confirm | ok | ok | ok | ok | ok | ok | RED | RED | RED | ok | RED | 4 |
| check-before-open-for-sigkill | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED | RED | 2 |
| no-resume-later-in-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-trap-command-unless-first-pass-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-trap-command-after-later-grace-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| trap-window-not-later-in-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-to-new-while-shell-stopped | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-to-new-after-1s | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| no-window-later-in-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| lone-first-pass-shell-needs-a-child | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| first-pass-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| lone-second-pass-shell-needs-a-child | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| second-pass-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| lone-last-in-grace-shell-needs-a-child | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| last-in-grace-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| lone-first-past-grace-shell-needs-a-child | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| first-past-grace-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| lone-second-past-grace-shell-needs-a-child | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| second-past-grace-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| lone-last-pass-shell-needs-a-child | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| last-pass-trap-command-spared-only-if-listed-at-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| resume-beside-new-live | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-trap-command-after-resume-from-1.5s | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| sigterm-to-live-new | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| live-trap-command-unspared-after-in-grace-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| live-trap-command-unspared | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| interior-past-grace-no-window | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| interior-in-grace-lone-shell-killed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| grace-strictly-past | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| no-window-at-grace-edge | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| trap-command-spared-only-in-resume-pass-past-grace | ok | ok | ok | ok | RED | ok | ok | ok | RED | ok | RED | 3 |
| sigterm-new-beside-stopped-shell-late | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| resume-held-at-grace-edge | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| verdict-from-grace-after-in-grace-resume | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| first-pass-live-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| second-pass-live-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| last-in-grace-live-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| first-past-grace-live-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| second-past-grace-live-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| last-pass-live-trap-command-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| resume-beside-live-new-past-grace | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| live-new-sigtermed-with-no-shell | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| next-to-last-in-grace-live-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| next-to-last-in-grace-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| early-new-sigtermed-0.25 | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| early-new-sigtermed-0.5 | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| early-trap-command-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| early-live-new-sigtermed | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| parent-of-live-new-unspared-beside-shell | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| verdict-early-live-new-beside-stopped-shell | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |
| parent-under-unresumed-shell-unspared | ok | ok | ok | ok | ok | ok | ok | ok | RED | ok | RED | 2 |

- cleanup-does-nothing / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / reparented: AssertionError: re-parented descendant was treated as new and never got SIGTERM
- sigterm-checks-parent: no control; red on nothing
- send-checks-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- no-start-recheck / reused_identity: AssertionError: a census entry whose process was replaced was signalled
- no-reap-after-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.48 s, 1 census passes, slowest 0.48 s: pid 2736432 (python3) state Z wchan 0 parent 2736427 (firs
- owned-is-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.48 s, 1 census passes, slowest 0.48 s: pid 2736503 exited during this report
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
- shell-window-one-pass / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (5.5, 'SIGCONT', 'shel
- shell-window-1s / shell_window: AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- trap-commands-no-window / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-never-spared / shell_window: AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (5.5, 'SIGCONT', 'shel
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
- report-without-state / report: AssertionError: ('state S', 'pid 2741588 (python3) wchan __do_sys_pause parent 2741583 (first parent 2741583) age 0.15 s start 80508915, not sent SIGKILL')
- report-without-wchan / report: AssertionError: ('wchan ', 'pid 2741669 (python3) state S parent 2741667 (first parent 2741667) age 0.14 s start 80509137, not sent SIGKILL')
- report-without-state-or-wchan / report: AssertionError: ('state S', 'pid 2741737 (python3) parent 2741736 (first parent 2741736) age 0.14 s start 80509410, not sent SIGKILL')
- grace-1s / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.0, 'SIGKILL', 'survivor'), (13.0, 'SIGKILL', '
- return-with-zombies / late_exit: AssertionError: cleanup returned with an owned child unreaped
- vanishing-waits-no-more / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.48 s, 1 census passes, slowest 0.48 s: pid 2742137 exited during this report
- resume-with-one-live / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'chil
- clock-always-cap / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.5, 'SIGKILL', 'survivor'), (13.0, 'SIGKILL', '
- killed-not-recorded / survivor: AssertionError: ('sent SIGKILL ', 'CLEANUP FAILED: owned descendants remain after 1.02 s, 30 census passes, slowest 0.02 s: pid 2742402 (bash) state T wchan do_
- no-sigcont-after-send: no control; red on nothing
- sigterm-to-new / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 'trap command'), (10.0, 'S
- no-leaf-first: no control; red on nothing
- signal-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGTERM', 'SIGCONT']
- parent-spared-past-kill-all / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- parents-killed-at-grace / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- vanishing-waits-30s-more / stated_seconds: AssertionError: a vanishing listing's stated seconds were not kept on the owner's clock: [(44.0, 'verdict')]
- report-without-current-parent / report: AssertionError: the report's current parent is not its own field: pid 2743664 (python3) state S wchan __do_sys_pause (first parent 1) age 0.12 s start 80513434,
- report-age-in-ticks / report: AssertionError: the report's age is not the process's own, 0.10 to 0.12 s: pid 2743834 (python3) state S wchan __do_sys_pause parent 2743831 (first parent 27438
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
- verdict-counts-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 2745816 exited during this report
- sigterm-needs-live-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- resume-unless-reaped-now / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- verdict-kills-only-the-killed / survivor: AssertionError: stopped shell left behind
- report-parent-is-first-parent / report: AssertionError: the report's current parent is not its own field: pid 2746210 (python3) state S wchan __do_sys_pause parent 1 (first parent 1) age 0.12 s start 
- sigkill-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGKILL']
- sigcont-by-number / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGCONT']
- resume-not-before-grace / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(2.0, 'SIGCONT', 'shell'), (12.0, 'SIGKILL', 'shell'), (12.0, 'SIGKILL
- resume-not-first-pass / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.5, 'SIGCONT', 'shell'), (10.5, 'SIGKILL', 'shell'), (10.5, 'SIGKILL
- sigterm-trap-commands / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 'trap command'), (10.0, 'S
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
- no-reap-after-first-census / late_exit: RuntimeError: CLEANUP FAILED: owned descendants remain after 0.49 s, 1 census passes, slowest 0.49 s: pid 2748146 (python3) state Z wchan 0 parent 2748145 (firs
- sigterm-rechecks-parent / reparented: AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- resume-collected-shell-past-grace / late_cancel: AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- verdict-sends-sigterm / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.0, 'SIGKILL', 'survivor'), (14.0, 'SIGTERM', '
- killed-ago-from-start / stated_seconds: AssertionError: a stubborn parent's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'parent'), (0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 
- return-before-confirm / vanishing: AssertionError: an endless listing did not fail the run
- check-before-open-for-sigkill / reused_identity: AssertionError: a census entry was signalled by its number, after it changed hands: ['SIGKILL']
- no-resume-later-in-grace / stated_seconds: AssertionError: an in-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGCONT', 'shell'), (12.0, 'SIGKILL',
- sigterm-trap-command-unless-first-pass-resume / stated_seconds: AssertionError: an in-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.0, 'SIGCONT', 'shell'), (1.0, 'SIGTERM', 
- sigterm-trap-command-after-later-grace-resume / stated_seconds: AssertionError: an in-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.0, 'SIGCONT', 'shell'), (1.0, 'SIGTERM', 
- trap-window-not-later-in-grace / stated_seconds: AssertionError: an in-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.0, 'SIGCONT', 'shell'), (2.0, 'SIGKILL', 
- sigterm-to-new-while-shell-stopped / stated_seconds: AssertionError: a new descendant beside a stopped shell's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (0.5, 'SIGTERM', 'clean
- sigterm-to-new-after-1s / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (1.0, 'SIGTERM', 'trap command'), (10.0, 'S
- no-window-later-in-grace / stated_seconds: AssertionError: an in-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.0, 'SIGCONT', 'shell'), (4.0, 'SIGKILL', 
- lone-first-pass-shell-needs-a-child / stated_seconds: AssertionError: a lone first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 'shell'), (2.0, 'SIGK
- first-pass-trap-command-sigtermed / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 'trap command'), (10.0, 'S
- lone-second-pass-shell-needs-a-child / stated_seconds: AssertionError: a lone second-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (9.5367431640625e-07, 'SIGCONT', 'she
- second-pass-trap-command-sigtermed / stated_seconds: AssertionError: a second-pass resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (9.5367431640625e-07,
- lone-last-in-grace-shell-needs-a-child / stated_seconds: AssertionError: a lone last in-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.9999990463256836, 'SIGCONT', 'sh
- last-in-grace-trap-command-unspared / stated_seconds: AssertionError: a last in-grace resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.9999990463256836
- lone-first-past-grace-shell-needs-a-child / stated_seconds: AssertionError: a lone first past-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGCONT', 'shell'), (3.0,
- first-past-grace-trap-command-unspared / stated_seconds: AssertionError: a first past-grace resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGCONT',
- lone-second-past-grace-shell-needs-a-child / stated_seconds: AssertionError: a lone second past-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (2.0
- second-past-grace-trap-command-unspared / stated_seconds: AssertionError: a second past-grace resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL'
- lone-last-pass-shell-needs-a-child / stated_seconds: AssertionError: a lone last-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (13.99999904
- last-pass-trap-command-spared-only-if-listed-at-resume / stated_seconds: AssertionError: a last-pass resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child
- resume-beside-new-live / stated_seconds: AssertionError: a live new descendant beside a stopped shell's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (0.5, 'SIGCONT', '
- sigterm-trap-command-after-resume-from-1.5s / stated_seconds: AssertionError: a next-to-last in-grace resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (0.0, 'SIGT
- sigterm-to-live-new / stated_seconds: AssertionError: a first-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 
- live-trap-command-unspared-after-in-grace-resume / stated_seconds: AssertionError: a first-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (2.0, 'SIGKILL', 
- live-trap-command-unspared / stated_seconds: AssertionError: a first-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (2.0, 'SIGKILL', 
- interior-past-grace-no-window / stated_seconds: AssertionError: a lone ten-second resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (10.0, 'SIG
- interior-in-grace-lone-shell-killed / stated_seconds: AssertionError: a lone one-second resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.0, 'SIGCONT', 'shell'), (1.5, 'SIGT
- grace-strictly-past / stated_seconds: AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (2.5, 'SIGKILL', 'survivor'), (14.0, 'SIGKILL', '
- no-window-at-grace-edge / stated_seconds: AssertionError: a lone first past-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGCONT', 'shell'), (4.0,
- trap-command-spared-only-in-resume-pass-past-grace / stated_seconds: AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', 'child'), (5.5, 'SIGCONT', 'shel
- sigterm-new-beside-stopped-shell-late / stated_seconds: AssertionError: a new descendant's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (1.0, 'SIGTERM', 'cleanup command'), (2.0, 
- resume-held-at-grace-edge / stated_seconds: AssertionError: a lone first past-grace resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.5, 'SIGCONT', 'shell'), (12.5
- verdict-from-grace-after-in-grace-resume / stated_seconds: AssertionError: a first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (10.0, 'SIGKILL', 'shell'), (10.0, 'SIGKILL
- first-pass-live-trap-command-sigtermed / stated_seconds: AssertionError: a first-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (0.5, 'SIGTERM', 
- second-pass-live-trap-command-sigtermed / stated_seconds: AssertionError: a second-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (9.5367431640625
- last-in-grace-live-trap-command-unspared / stated_seconds: AssertionError: a last in-grace resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (1.99999904632
- first-past-grace-live-trap-command-unspared / stated_seconds: AssertionError: a first past-grace resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGC
- second-past-grace-live-trap-command-unspared / stated_seconds: AssertionError: a second past-grace resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIG
- last-pass-live-trap-command-unspared / stated_seconds: AssertionError: a last-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKILL', '
- resume-beside-live-new-past-grace / stated_seconds: AssertionError: a live new descendant beside a stopped shell's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGCONT', '
- live-new-sigtermed-with-no-shell / stated_seconds: AssertionError: a live new descendant's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'survivor'), (0.5, 'SIGTERM', 'trap command'), (2.0
- next-to-last-in-grace-live-trap-command-sigtermed / stated_seconds: AssertionError: a next-to-last in-grace resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (0.0, 
- next-to-last-in-grace-trap-command-sigtermed / stated_seconds: AssertionError: a next-to-last in-grace resume and its trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (0.0, 'SIGT
- early-new-sigtermed-0.25 / stated_seconds: AssertionError: an early first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (9.5367431640625e-07, 'census'), (9.
- early-new-sigtermed-0.5 / stated_seconds: AssertionError: an early first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (9.5367431640625e-07, 'census'), (9.
- early-trap-command-sigtermed / stated_seconds: AssertionError: an early first-pass resume's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (9.5367431640625e-07, 'census'), (9.
- early-live-new-sigtermed / stated_seconds: AssertionError: an early first-pass resume and its live trap command's stated seconds were not kept on the owner's clock: [(0.0, 'SIGCONT', 'shell'), (9.5367431
- parent-of-live-new-unspared-beside-shell / stated_seconds: AssertionError: a live new descendant beside a shell never resumed's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKI
- verdict-early-live-new-beside-stopped-shell / stated_seconds: AssertionError: a live new descendant beside a shell never resumed's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKI
- parent-under-unresumed-shell-unspared / stated_seconds: AssertionError: a live new descendant beside a shell never resumed's stated seconds were not kept on the owner's clock: [(0.0, 'SIGTERM', 'child'), (2.0, 'SIGKI

problems: none
