| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | stated_seconds | reused_identity | whole | red |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|
| none | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| cleanup-does-nothing | ok | RED(1) | CUT | RED(1) | RED(1) | RED(1) | RED(1) | RED(1) | RED(1) | ok | RED(1) | 9 |
| identity-start-holds-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | ok | ok | RED(1) | 2 |
| identity-keys-hold-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| identity-first-census-holds-parent | ok | RED(1) | ok | ok | ok | RED(1) | ok | ok | RED(1) | ok | RED(1) | 4 |
| identity-includes-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| identity-checks-parent-before-send | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| sigterm-checks-parent | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| send-checks-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| no-start-recheck | ok | ok | ok | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 3 |
| owned-is-census | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 3 |
| deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| pass-cap-1s | ok | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 2 |
| pass-cap-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| windows-2s | ok | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 2 |
| reap-window-2s | ok | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 2 |
| no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| no-shell-window-kept | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| no-shell-window-pass | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| root-killed-unresumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| shell-killed-when-resumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| shell-window-one-pass | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| shell-window-1s | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| trap-commands-never-spared | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | ok | RED(1) | 3 |
| resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| window-without-resume | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| rearm-without-sigcont | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | RED(1) | ok | RED(1) | 4 |
| resume-while-listed | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | ok | RED(1) | 3 |
| no-kill-before-raise-empty | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | ok | RED(1) | 3 |
| kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | ok | RED(1) | 3 |
| endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | ok | ok | RED(1) | 3 |
| survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | RED(1) | ok | RED(1) | 5 |
| survivor-never-fails-guarded | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | RED(1) | ok | RED(1) | 5 |
| trust-sigkill | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | ok | RED(1) | 3 |
| killed-counts-as-gone | ok | ok | ok | ok | ok | ok | ok | ok | RED(1) | ok | RED(1) | 2 |
| report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | 3 |
| report-without-wchan | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | 3 |
| report-without-state-or-wchan | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | 3 |

Failing words:
- cleanup-does-nothing / reparented (0.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- cleanup-does-nothing / late_exit (150.0 s): 
- cleanup-does-nothing / stall (0.2 s): AssertionError: the stall was charged in full: SIGKILL in pass []
- cleanup-does-nothing / shell_window (0.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- cleanup-does-nothing / survivor (0.2 s): owned_process.Cancelled: signal 15
- cleanup-does-nothing / vanishing (0.1 s): AssertionError: an endless listing did not fail the run
- cleanup-does-nothing / late_cancel (0.2 s): AssertionError: an endless listing did not fail the run
- cleanup-does-nothing / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(0, 'no verdict')]
- cleanup-does-nothing / whole (0.3 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / whole (2.3 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(29, 'SIGKILL', 'survivor'), (29, 'verdict')]
- identity-keys-hold-parent / whole (2.3 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / survivor (4.2 s): ValueError: too many values to unpack (expected 2, got 3)
- identity-first-census-holds-parent / stated_seconds (0.1 s): ValueError: too many values to unpack (expected 2, got 3)
- identity-first-census-holds-parent / whole (2.3 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(29, 'SIGKILL', 'survivor'), (29, 'verdict')]
- identity-includes-parent / whole (2.3 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(29, 'SIGKILL', 'survivor'), (29, 'verdict')]
- identity-checks-parent-before-send / whole (2.3 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- send-checks-parent / reparented (0.3 s): AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- send-checks-parent / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(29, 'SIGKILL', 'survivor'), (29, 'verdict')]
- send-checks-parent / whole (0.3 s): AssertionError: the re-parented descendant's SIGTERM waited for a later census: [2]
- no-start-recheck / reused_identity (0.1 s): AssertionError: a census entry whose process was replaced was signalled
- no-start-recheck / whole (9.8 s): AssertionError: a census entry whose process was replaced was signalled
- no-reap-after-census / late_exit (0.7 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 509 (python3) state Z wchan 0 parent 506 (first parent 506) age 
- no-reap-after-census / late_cancel (0.2 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- no-reap-after-census / whole (0.8 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 535 (python3) state Z wchan 0 parent 527 (first parent 527) age 
- owned-is-census / late_exit (0.6 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 540 exited during this report
- owned-is-census / late_cancel (0.2 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- owned-is-census / whole (0.8 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 565 exited during this report
- deadline-wall-clock / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- deadline-wall-clock / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (15, 'SIGKILL', 'survivor'), (15,
- deadline-wall-clock / whole (2.9 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-1s / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (15, 'SIGKILL', 'survivor'), (15,
- pass-cap-1s / whole (9.3 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (15, 'SIGKILL', 'survivor'), (15,
- pass-cap-1.5s / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-1.5s / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (15, 'SIGKILL', 'survivor'), (15,
- pass-cap-1.5s / whole (2.9 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-5s / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-5s / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (3, 'SIGKILL', 'survivor'), (15, 'SIGKILL', 'survivor'), (15,
- pass-cap-5s / whole (2.9 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- windows-2s / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (13, 'SIGKILL', 'survivor'), (13,
- windows-2s / whole (9.6 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (13, 'SIGKILL', 'survivor'), (13,
- reap-window-2s / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (13, 'SIGKILL', 'survivor'), (13,
- reap-window-2s / whole (9.7 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (13, 'SIGKILL', 'survivor'), (13,
- no-shell-window / shell_window (1.5 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- no-shell-window / whole (5.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-kept / shell_window (1.5 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-kept / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- no-shell-window-kept / whole (5.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-pass / shell_window (1.5 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-pass / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- no-shell-window-pass / whole (5.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / shell_window (1.5 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- no-trap-window / whole (5.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- root-killed-unresumed / shell_window (1.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- root-killed-unresumed / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (9, 'SIGKILL', 'shell'), (12, 'SIGCO
- root-killed-unresumed / whole (5.1 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / shell_window (1.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- shell-killed-when-resumed / whole (5.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-window-one-pass / shell_window (3.0 s): AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- shell-window-one-pass / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (13, 'SIGK
- shell-window-one-pass / whole (6.7 s): AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- shell-window-1s / shell_window (3.0 s): AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- shell-window-1s / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (14, 'SIGK
- shell-window-1s / whole (6.8 s): AssertionError: the resumed shell was killed inside its own window, with no child to spare it
- trap-commands-no-window / shell_window (1.8 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-no-window / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- trap-commands-no-window / whole (5.6 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-never-spared / shell_window (1.8 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-never-spared / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (12, 'SIGK
- trap-commands-never-spared / whole (5.5 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / shell_window (2.8 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (14, 'SIGK
- trap-commands-1s / whole (6.5 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- resume-collected-shell / late_cancel (0.2 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- resume-collected-shell / whole (9.0 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- window-without-resume / late_cancel (15.2 s): AssertionError: cleanup never reached a verdict after a late cancel
- window-without-resume / whole (24.0 s): AssertionError: cleanup never reached a verdict after a late cancel
- rearm-without-sigcont / shell_window (11.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- rearm-without-sigcont / late_cancel (15.2 s): AssertionError: cleanup never reached a verdict after a late cancel
- rearm-without-sigcont / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (32, 'SIGKILL', 'shell'), (32, 'SIGK
- rearm-without-sigcont / whole (15.2 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- resume-while-listed / late_cancel (0.2 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- resume-while-listed / whole (9.0 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- no-kill-before-raise / survivor (18.2 s): AssertionError: stopped shell left behind
- no-kill-before-raise / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (29, 'verdict')]
- no-kill-before-raise / whole (25.2 s): AssertionError: stopped shell left behind
- no-kill-before-raise-empty / survivor (18.2 s): AssertionError: stopped shell left behind
- no-kill-before-raise-empty / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (29, 'verdict')]
- no-kill-before-raise-empty / whole (25.1 s): AssertionError: stopped shell left behind
- kill-before-fail-spares-shell / survivor (18.2 s): AssertionError: stopped shell left behind
- kill-before-fail-spares-shell / stated_seconds (0.1 s): AssertionError: a late resume's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'child'), (5, 'SIGKILL', 'child'), (12, 'SIGCONT', 'shell'), (32, 'SIGK
- kill-before-fail-spares-shell / whole (25.2 s): AssertionError: stopped shell left behind
- endless-unbounded / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- endless-unbounded / late_cancel (15.2 s): AssertionError: cleanup never reached a verdict after a late cancel
- endless-unbounded / whole (23.2 s): AssertionError: cleanup never reached a verdict
- survivor-never-fails / survivor (32.2 s): AssertionError: a survivor never failed the run
- survivor-never-fails / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- survivor-never-fails / late_cancel (15.2 s): AssertionError: cleanup never reached a verdict after a late cancel
- survivor-never-fails / stated_seconds (0.1 s): AssertionError: cleanup never reached a verdict on the owner's clock
- survivor-never-fails / whole (39.1 s): AssertionError: a survivor never failed the run
- survivor-never-fails-guarded / survivor (32.2 s): AssertionError: a survivor never failed the run
- survivor-never-fails-guarded / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- survivor-never-fails-guarded / late_cancel (15.2 s): AssertionError: cleanup never reached a verdict after a late cancel
- survivor-never-fails-guarded / stated_seconds (0.1 s): AssertionError: cleanup never reached a verdict on the owner's clock
- survivor-never-fails-guarded / whole (39.1 s): AssertionError: a survivor never failed the run
- trust-sigkill / survivor (32.2 s): AssertionError: a survivor never failed the run
- trust-sigkill / stated_seconds (0.1 s): AssertionError: cleanup never reached a verdict on the owner's clock
- trust-sigkill / whole (39.1 s): AssertionError: a survivor never failed the run
- killed-counts-as-gone / stated_seconds (0.1 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (49, 'verdict')]
- killed-counts-as-gone / whole (20.2 s): AssertionError: a survivor's stated seconds were not kept on the owner's clock: [(1, 'SIGTERM', 'survivor'), (5, 'SIGKILL', 'survivor'), (49, 'verdict')]
- report-without-state / report (2.2 s): AssertionError: ('state S', 'pid 1102 (python3) wchan hrtimer_nanosleep parent 1100 (first parent 1100) age 0.04 s start 76330114, not sent SIGKILL')
- report-without-state / survivor (1.2 s): AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 50 census passes, slowest 0.00 s: pid 1215 (bash) wchan do_signal_stop parent 1211 (fir
- report-without-state / whole (2.2 s): AssertionError: ('state S', 'pid 1226 (python3) wchan hrtimer_nanosleep parent 1223 (first parent 1223) age 0.04 s start 76330701, not sent SIGKILL')
- report-without-wchan / report (2.2 s): AssertionError: ('wchan ', 'pid 1227 (python3) state S parent 1225 (first parent 1225) age 0.04 s start 76330709, not sent SIGKILL')
- report-without-wchan / survivor (1.2 s): AssertionError: ('wchan ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 50 census passes, slowest 0.00 s: pid 1297 (bash) state T parent 1292 (first parent 129
- report-without-wchan / whole (2.2 s): AssertionError: ('wchan ', 'pid 1320 (python3) state S parent 1317 (first parent 1317) age 0.04 s start 76331108, not sent SIGKILL')
- report-without-state-or-wchan / report (2.2 s): AssertionError: ('state S', 'pid 1321 (python3) parent 1319 (first parent 1319) age 0.04 s start 76331115, not sent SIGKILL')
- report-without-state-or-wchan / survivor (1.2 s): AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 50 census passes, slowest 0.00 s: pid 1335 (bash) parent 1333 (first parent 1333) age 1
- report-without-state-or-wchan / whole (2.2 s): AssertionError: ('state S', 'pid 1345 (python3) parent 1344 (first parent 1344) age 0.04 s start 76331390, not sent SIGKILL')
