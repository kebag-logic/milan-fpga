| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | whole | red |
|---|---|---|---|---|---|---|---|---|---|---:|
| none | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| shell-window-one-pass | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| cleanup-does-nothing | ok | CUT | CUT | CUT | RED(1) | RED(1) | RED(1) | RED(1) | CUT | 8 |
| identity-start-holds-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | 2 |
| identity-keys-hold-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | 2 |
| identity-first-census-holds-parent | ok | RED(1) | ok | ok | ok | RED(1) | ok | ok | RED(1) | 3 |
| identity-includes-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | 2 |
| identity-checks-parent-before-send | ok | RED(1) | ok | ok | ok | ok | ok | ok | RED(1) | 2 |
| sigterm-checks-parent | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| send-checks-parent | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| no-start-recheck | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | RED(1) | 2 |
| owned-is-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | RED(1) | 2 |
| deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | 2 |
| pass-cap-1s | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| pass-cap-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | 2 |
| pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | RED(1) | 2 |
| windows-2s | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| reap-window-2s | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| no-shell-window-kept | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| no-shell-window-pass | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| root-killed-unresumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| shell-killed-when-resumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| shell-window-1s | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| trap-commands-never-spared | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | ok | RED(1) | 2 |
| resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| window-without-resume | ok | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| rearm-without-sigcont | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | RED(1) | 3 |
| resume-while-listed | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| no-kill-before-raise-empty | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | 3 |
| survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | RED(1) | 4 |
| survivor-never-fails-guarded | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | RED(1) | 4 |
| trust-sigkill | ok | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| killed-counts-as-gone | ok | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 3 |
| report-without-wchan | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 3 |
| report-without-state-or-wchan | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 3 |

Failing words:
- cleanup-does-nothing / reparented (150.0 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- cleanup-does-nothing / late_exit (150.1 s): 
- cleanup-does-nothing / stall (150.0 s): AssertionError: the stall was charged in full: SIGKILL in pass []
- cleanup-does-nothing / shell_window (0.1 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- cleanup-does-nothing / survivor (0.1 s): owned_process.Cancelled: signal 15
- cleanup-does-nothing / vanishing (0.1 s): AssertionError: an endless listing did not fail the run
- cleanup-does-nothing / late_cancel (0.1 s): AssertionError: an endless listing did not fail the run
- cleanup-does-nothing / whole (400.1 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-start-holds-parent / whole (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / reparented (2.1 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-keys-hold-parent / whole (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / reparented (2.1 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-first-census-holds-parent / survivor (4.2 s): ValueError: too many values to unpack (expected 2, got 3)
- identity-first-census-holds-parent / whole (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-includes-parent / whole (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-checks-parent-before-send / whole (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- no-reap-after-census / late_exit (0.6 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 487 (python3) state Z wchan 0 parent 485 (first parent 485) age 
- no-reap-after-census / whole (0.7 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 595 (python3) state Z wchan 0 parent 588 (first parent 588) age 
- owned-is-census / late_exit (0.6 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 625 exited during this report
- owned-is-census / whole (0.7 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 992 exited during this report
- deadline-wall-clock / stall (2.1 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- deadline-wall-clock / whole (2.8 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-1.5s / stall (2.1 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-1.5s / whole (2.8 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-5s / stall (2.1 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- pass-cap-5s / whole (2.8 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- no-shell-window / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window / whole (5.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-kept / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-kept / whole (5.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-pass / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-shell-window-pass / whole (5.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / whole (5.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- root-killed-unresumed / shell_window (1.6 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- root-killed-unresumed / whole (5.4 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / whole (5.5 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- trap-commands-no-window / shell_window (1.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-no-window / whole (5.5 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-never-spared / shell_window (1.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-never-spared / whole (5.5 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / shell_window (2.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / whole (6.5 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- resume-collected-shell / late_cancel (0.1 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- resume-collected-shell / whole (8.9 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- window-without-resume / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- window-without-resume / whole (23.9 s): AssertionError: cleanup never reached a verdict after a late cancel
- rearm-without-sigcont / shell_window (11.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- rearm-without-sigcont / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- rearm-without-sigcont / whole (15.5 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-kill-before-raise / survivor (18.2 s): AssertionError: stopped shell left behind
- no-kill-before-raise / whole (25.1 s): AssertionError: stopped shell left behind
- no-kill-before-raise-empty / survivor (18.2 s): AssertionError: stopped shell left behind
- no-kill-before-raise-empty / whole (25.1 s): AssertionError: stopped shell left behind
- kill-before-fail-spares-shell / survivor (18.2 s): AssertionError: stopped shell left behind
- kill-before-fail-spares-shell / whole (25.1 s): AssertionError: stopped shell left behind
- endless-unbounded / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- endless-unbounded / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- endless-unbounded / whole (23.1 s): AssertionError: cleanup never reached a verdict
- survivor-never-fails / survivor (32.1 s): AssertionError: a survivor never failed the run
- survivor-never-fails / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- survivor-never-fails / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- survivor-never-fails / whole (39.0 s): AssertionError: a survivor never failed the run
- survivor-never-fails-guarded / survivor (32.2 s): AssertionError: a survivor never failed the run
- survivor-never-fails-guarded / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- survivor-never-fails-guarded / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- survivor-never-fails-guarded / whole (39.0 s): AssertionError: a survivor never failed the run
- trust-sigkill / survivor (32.1 s): AssertionError: a survivor never failed the run
- trust-sigkill / whole (39.0 s): AssertionError: a survivor never failed the run
- report-without-state / report (2.2 s): AssertionError: ('state S', 'pid 4025 (python3) wchan hrtimer_nanosleep parent 4023 (first parent 4023) age 0.04 s start 76120525, not sent SIGKILL')
- report-without-state / survivor (1.2 s): AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 50 census passes, slowest 0.00 s: pid 4054 (bash) wchan do_signal_stop parent 4052 (fir
- report-without-state / whole (2.2 s): AssertionError: ('state S', 'pid 4064 (python3) wchan hrtimer_nanosleep parent 4063 (first parent 4063) age 0.04 s start 76120949, not sent SIGKILL')
- report-without-wchan / report (2.2 s): AssertionError: ('wchan ', 'pid 4068 (python3) state S parent 4065 (first parent 4065) age 0.04 s start 76121012, not sent SIGKILL')
- report-without-wchan / survivor (1.2 s): AssertionError: ('wchan ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 50 census passes, slowest 0.00 s: pid 4084 (bash) state T parent 4082 (first parent 408
- report-without-wchan / whole (2.1 s): AssertionError: ('wchan ', 'pid 4091 (python3) state S parent 4090 (first parent 4090) age 0.02 s start 76121436, not sent SIGKILL')
- report-without-state-or-wchan / report (2.1 s): AssertionError: ('state S', 'pid 4093 (python3) parent 4092 (first parent 4092) age 0.02 s start 76121468, not sent SIGKILL')
- report-without-state-or-wchan / survivor (1.2 s): AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 50 census passes, slowest 0.00 s: pid 4107 (bash) parent 4105 (first parent 4105) age 1
- report-without-state-or-wchan / whole (2.2 s): AssertionError: ('state S', 'pid 4114 (python3) parent 4112 (first parent 4112) age 0.04 s start 76121683, not sent SIGKILL')
