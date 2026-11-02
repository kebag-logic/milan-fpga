| Mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | red |
|---|---|---|---|---|---|---|---|---:|
| R763-none | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-identity-includes-parent | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R763-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R763-deadline-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-pass-cap-5s | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R763-no-shell-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R763-trap-commands-1s | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R763-no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R763-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| R763-survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| R763-killed-counts-as-gone | ok | ok | ok | ok | ok | ok | ok | 0 |
| R763-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| R763-report-without-wchan | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| R763-cleanup-does-nothing | ok | RED(1) | RED(-9) | RED(1) | RED(1) | RED(1) | RED(1) | 6 |
| R764-M01-identity-includes-parent | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01b-send-recheck-includes-parent | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M01c-identity-includes-parent-both | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| R764-M02-no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| R764-M03-wall-clock | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M04-clamp-5s | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| R764-M05-no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M06-root-killed-unresumed | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M07-trap-child-no-window | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| R764-M08-no-kill-before-fail | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R764-M09-kill-before-fail-spares-shell | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R764-M10-endless-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| R764-M11-trust-sigkill | ok | ok | ok | ok | ok | RED(1) | ok | 1 |
| R764-M12-report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | 2 |
| R764-M13-cleanup-does-nothing-suite | ok | RED(1) | RED(-9) | RED(1) | RED(1) | RED(1) | RED(1) | 6 |
| R764-M14-no-start-recheck | ok | ok | ok | ok | ok | ok | ok | 0 |
| R764-M15-windows-2s | ok | ok | ok | ok | ok | ok | ok | 0 |

- R763-identity-includes-parent / owner_reparented: owner_reparented FAIL 2.1s AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R763-no-reap-after-census / owner_late_exit: owner_late_exit FAIL 0.5s RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 2 (python3) state Z wchan 0 parent 1 (first parent 1) age 0.51 s start 74407618, not sent SIGKILL
- R763-deadline-wall-clock / owner_stall: owner_stall FAIL 2.1s AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R763-pass-cap-5s / owner_stall: owner_stall FAIL 2.1s AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R763-no-shell-window / owner_shell_window: owner_shell_window FAIL 0.8s AssertionError: the shell was killed in the pass that resumed it, before its trap
- R763-trap-commands-1s / owner_shell_window: owner_shell_window FAIL 1.8s AssertionError: the resumed shell's trap command was killed inside the shell's window
- R763-no-kill-before-raise / owner_survivor: owner_survivor FAIL 18.1s AssertionError: stopped shell left behind
- R763-endless-unbounded / owner_vanishing: owner_vanishing FAIL 15.0s AssertionError: cleanup never reached a verdict
- R763-survivor-never-fails / owner_survivor: owner_survivor FAIL 32.1s AssertionError: a survivor never failed the run
- R763-survivor-never-fails / owner_vanishing: owner_vanishing FAIL 15.0s AssertionError: cleanup never reached a verdict
- R763-report-without-state / owner_report: owner_report FAIL 2.1s AssertionError: ('state S', 'pid 2 (python3) wchan hrtimer_nanosleep parent 1 (first parent 1) age 0.04 s start 74409353, not sent SIGKILL')
- R763-report-without-state / owner_survivor: owner_survivor FAIL 1.1s AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 51 census passes, slowest 0.00 s: pid 3 (bash) wchan do_signal_stop parent 1 (first parent 1) age 1.05 s start 74410046, not sent SIGKILL; pid 4 (python
- R763-report-without-wchan / owner_report: owner_report FAIL 2.1s AssertionError: ('wchan ', 'pid 2 (python3) state S parent 1 (first parent 1) age 0.04 s start 74410164, not sent SIGKILL')
- R763-report-without-wchan / owner_survivor: owner_survivor FAIL 1.1s AssertionError: ('wchan ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 51 census passes, slowest 0.00 s: pid 3 (bash) state T parent 1 (first parent 1) age 1.05 s start 74410284, not sent SIGKILL; pid 4 (python3) state S pa
- R763-cleanup-does-nothing / owner_reparented: owner_reparented FAIL 0.1s AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R763-cleanup-does-nothing / owner_late_exit: 
- R763-cleanup-does-nothing / owner_stall: owner_stall FAIL 0.0s AssertionError: the stall was charged in full: SIGKILL in pass []
- R763-cleanup-does-nothing / owner_shell_window: owner_shell_window FAIL 0.0s AssertionError: the shell was killed in the pass that resumed it, before its trap
- R763-cleanup-does-nothing / owner_survivor: owner_survivor FAIL 0.0s Cancelled: signal 15
- R763-cleanup-does-nothing / owner_vanishing: owner_vanishing FAIL 0.0s AssertionError: an endless listing did not fail the run
- R764-M01c-identity-includes-parent-both / owner_reparented: owner_reparented FAIL 2.1s AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R764-M02-no-reap-after-census / owner_late_exit: owner_late_exit FAIL 0.5s RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 2 (python3) state Z wchan 0 parent 1 (first parent 1) age 0.51 s start 74411132, not sent SIGKILL
- R764-M03-wall-clock / owner_stall: owner_stall FAIL 2.1s AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R764-M04-clamp-5s / owner_stall: owner_stall FAIL 2.1s AssertionError: the stall was charged in full: SIGKILL in pass [2]
- R764-M05-no-trap-window / owner_shell_window: owner_shell_window FAIL 0.8s AssertionError: the shell was killed in the pass that resumed it, before its trap
- R764-M06-root-killed-unresumed / owner_shell_window: owner_shell_window FAIL 0.8s AssertionError: the shell was killed in the pass that resumed it, before its trap
- R764-M07-trap-child-no-window / owner_shell_window: owner_shell_window FAIL 0.8s AssertionError: the resumed shell's trap command was killed inside the shell's window
- R764-M08-no-kill-before-fail / owner_survivor: owner_survivor FAIL 18.1s AssertionError: stopped shell left behind
- R764-M09-kill-before-fail-spares-shell / owner_survivor: owner_survivor FAIL 18.1s AssertionError: stopped shell left behind
- R764-M10-endless-unbounded / owner_vanishing: owner_vanishing FAIL 15.0s AssertionError: cleanup never reached a verdict
- R764-M11-trust-sigkill / owner_survivor: owner_survivor FAIL 32.0s AssertionError: a survivor never failed the run
- R764-M12-report-without-state / owner_report: owner_report FAIL 2.1s AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.04 s start 74413376, not sent SIGKILL')
- R764-M12-report-without-state / owner_survivor: owner_survivor FAIL 1.1s AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 51 census passes, slowest 0.00 s: pid 3 (bash) parent 1 (first parent 1) age 1.05 s start 74414044, not sent SIGKILL; pid 4 (python3) parent 3 (first pa
- R764-M13-cleanup-does-nothing-suite / owner_reparented: owner_reparented FAIL 0.1s AssertionError: re-parented descendant was treated as new and never got SIGTERM
- R764-M13-cleanup-does-nothing-suite / owner_late_exit: 
- R764-M13-cleanup-does-nothing-suite / owner_stall: owner_stall FAIL 0.0s AssertionError: the stall was charged in full: SIGKILL in pass []
- R764-M13-cleanup-does-nothing-suite / owner_shell_window: owner_shell_window FAIL 0.0s AssertionError: the shell was killed in the pass that resumed it, before its trap
- R764-M13-cleanup-does-nothing-suite / owner_survivor: owner_survivor FAIL 0.0s Cancelled: signal 15
- R764-M13-cleanup-does-nothing-suite / owner_vanishing: owner_vanishing FAIL 0.0s AssertionError: an endless listing did not fail the run
