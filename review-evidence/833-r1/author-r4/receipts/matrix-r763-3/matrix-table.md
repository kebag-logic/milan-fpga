| mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | red |
|---|---|---|---|---|---|---|---|---|---|
| identity-has-parent | ok | RED(1) | ok | ok | ok | RED(1) | ok | ok | 2 |
| listing-unbounded | ok | ok | ok | ok | ok | ok | RED(1) | RED(1) | 2 |
| new-fix-census-not-owned | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| new-fix-reverted | ok | ok | ok | ok | ok | ok | ok | RED(1) | 1 |
| no-kill-before-raise | ok | ok | ok | ok | ok | RED(1) | ok | ok | 1 |
| no-reap-after-census | ok | ok | RED(1) | ok | ok | ok | ok | ok | 1 |
| no-trap-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| none | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| pass-unclamped | ok | ok | ok | RED(1) | ok | ok | ok | ok | 1 |
| report-without-state | RED(1) | ok | ok | ok | ok | RED(1) | ok | ok | 2 |
| shell-killed-when-resumed | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |
| survivor-never-fails | ok | ok | ok | ok | ok | RED(1) | RED(1) | RED(1) | 3 |
| trap-commands-no-window | ok | ok | ok | ok | RED(1) | ok | ok | ok | 1 |

- identity-has-parent / owner_reparented (2.2 s): owner_reparented FAIL 2.1s AssertionError: re-parented descendant was treated as new and never got SIGTERM
- identity-has-parent / owner_survivor (1.2 s): owner_survivor FAIL 1.1s ValueError: too many values to unpack (expected 2, got 3)
- listing-unbounded / owner_vanishing (15.1 s): owner_vanishing FAIL 15.0s AssertionError: cleanup never reached a verdict
- listing-unbounded / owner_late_cancel (15.1 s): owner_late_cancel FAIL 15.0s AssertionError: cleanup never reached a verdict after a late cancel
- new-fix-reverted / owner_late_cancel (0.1 s): owner_late_cancel FAIL 0.0s AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window
- no-kill-before-raise / owner_survivor (16.2 s): owner_survivor FAIL 16.1s AssertionError: stopped shell left behind
- no-reap-after-census / owner_late_exit (0.6 s): owner_late_exit FAIL 0.5s RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 2 (python3) state Z wchan 0 parent 1 (first parent 1) age 0.51 s start 75510141, not sent SIGKILL
- no-trap-window / owner_shell_window (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- pass-unclamped / owner_stall (2.2 s): owner_stall FAIL 2.1s AssertionError: the stall was charged in full: SIGKILL in pass [2]
- report-without-state / owner_report (0.1 s): owner_report FAIL 0.0s AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.04 s start 75510704, not sent SIGKILL')
- report-without-state / owner_survivor (1.2 s): owner_survivor FAIL 1.1s AssertionError: ('state ', 'CLEANUP FAILED: owned descendants remain after 1.01 s, 51 census passes, slowest 0.00 s: pid 3 (bash) parent 1 (first parent 1) age 1.06 s start 75510778, not sent SIGKILL; pid 4 (python3) parent 3 (first parent 3) age 1.05 s start 75510779, sent 
- shell-killed-when-resumed / owner_shell_window (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- survivor-never-fails / owner_survivor (30.1 s): owner_survivor FAIL 30.0s AssertionError: a survivor never failed the run
- survivor-never-fails / owner_vanishing (15.1 s): owner_vanishing FAIL 15.0s AssertionError: cleanup never reached a verdict
- survivor-never-fails / owner_late_cancel (15.1 s): owner_late_cancel FAIL 15.0s AssertionError: cleanup never reached a verdict after a late cancel
- trap-commands-no-window / owner_shell_window (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
