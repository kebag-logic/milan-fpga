| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | red |
|---|---|---|---|---|---|---|---|---|---:|
| R763-deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| R763-identity-includes-parent | ok | RED(1) | ok | ok | ok | ok | ok | ok | 1 |
| R763-no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R763-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R763-no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-none | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-pass-cap-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-reap-window-2s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | 2 |
| R763-survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | 3 |
| R763-trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M01-identity-includes-parent | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01b-send-recheck-includes-parent | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01c-identity-includes-parent-both | ok | RED(1) | ok | ok | ok | ok | ok | ok | 1 |
| R764-M02-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R764-M03-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M04-clamp-5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M05-no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M06-root-killed-unresumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M07-trap-child-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M04c-clamp-1.5s | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M04d-clamp-1.0s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M07b-trap-child-1s-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M08-no-kill-before-fail | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M09-kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M10-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| R764-M11-trust-sigkill | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M12-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | 2 |
| R764-M13-cleanup-does-nothing-suite | ok | RED(1) | RED(-9) | RED(1) | RED(1) | RED(1) | RED(1) | RED(1) | 7 |
| R764-M14-no-start-recheck | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M16-resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| R764-M15-windows-2s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| A726c-resume-collected-shell | ok | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| A726c-rearm-without-sigcont | ok | ok | ok | ok | RED(1) | ok | ok | RED(1) | 2 |
| R763-3-shell-killed-when-resumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-3-new-fix-census-not-owned | ok | ok | ok | ok | ok | ok | ok | ok | 0 |

Failing words:
- R763-deadline-wall-clock / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R763-endless-unbounded / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- R763-endless-unbounded / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- R763-identity-includes-parent / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R763-no-kill-before-raise / survivor (18.2 s): AssertionError: stopped shell left behind
- R763-no-reap-after-census / late_exit (0.6 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 2 (python3) state Z wchan 0 parent 1 (first parent 1) 
- R763-no-shell-window / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- R763-pass-cap-1.5s / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R763-pass-cap-5s / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R763-report-without-state / report (2.1 s): AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.05 s start 75516552, not sent SIGKILL')
- R763-report-without-state / survivor (1.2 s): AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 51 census passes, slowest 0.00 s: pid 3 (bash) parent 1 (first parent 1) age 
- R763-survivor-never-fails / survivor (32.1 s): AssertionError: a survivor never failed the run
- R763-survivor-never-fails / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- R763-survivor-never-fails / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- R763-trap-commands-1s / shell_window (2.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- R763-trap-commands-no-window / shell_window (1.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- R764-M01c-identity-includes-parent-both / reparented (2.2 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R764-M02-no-reap-after-census / late_exit (0.6 s): RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 2 (python3) state Z wchan 0 parent 1 (first parent 1) 
- R764-M03-wall-clock / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R764-M04-clamp-5s / stall (2.2 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R764-M05-no-trap-window / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- R764-M06-root-killed-unresumed / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- R764-M07-trap-child-no-window / shell_window (1.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- R764-M04c-clamp-1.5s / stall (2.1 s): AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R764-M07b-trap-child-1s-window / shell_window (2.7 s): AssertionError: the resumed shell's trap command was killed inside the shell's window
- R764-M08-no-kill-before-fail / survivor (18.2 s): AssertionError: stopped shell left behind
- R764-M09-kill-before-fail-spares-shell / survivor (18.2 s): AssertionError: stopped shell left behind
- R764-M10-endless-unbounded / vanishing (15.1 s): AssertionError: cleanup never reached a verdict
- R764-M10-endless-unbounded / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- R764-M11-trust-sigkill / survivor (32.1 s): AssertionError: a survivor never failed the run
- R764-M12-report-without-state / report (2.2 s): AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.04 s start 75518921, not sent SIGKILL')
- R764-M12-report-without-state / survivor (1.2 s): AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 51 census passes, slowest 0.00 s: pid 3 (bash) parent 1 (first parent 1) age 
- R764-M13-cleanup-does-nothing-suite / reparented (0.1 s): AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R764-M13-cleanup-does-nothing-suite / late_exit (155.0 s): 
- R764-M13-cleanup-does-nothing-suite / stall (0.1 s): AssertionError: the stall was charged in full: SIGKILL in pass []
- R764-M13-cleanup-does-nothing-suite / shell_window (0.1 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- R764-M13-cleanup-does-nothing-suite / survivor (0.1 s): Cancelled: signal 15
- R764-M13-cleanup-does-nothing-suite / vanishing (0.1 s): AssertionError: an endless listing did not fail the run
- R764-M13-cleanup-does-nothing-suite / late_cancel (0.1 s): AssertionError: an endless listing did not fail the run
- R764-M16-resume-collected-shell / late_cancel (0.1 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- A726c-resume-collected-shell / late_cancel (0.1 s): AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- A726c-rearm-without-sigcont / shell_window (11.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
- A726c-rearm-without-sigcont / late_cancel (15.1 s): AssertionError: cleanup never reached a verdict after a late cancel
- R763-3-shell-killed-when-resumed / shell_window (1.7 s): AssertionError: the shell was killed in the pass that resumed it, before its trap
