| Mutant | Test | Result at 1ff8292c | rc | Source | Last line |
|---|---|---|---:|---|---|
| control-A | suite | green | 0 | mutations-rerun/control-A.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
| control-B | suite | green | 0 | mutations-rerun/control-B.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
| control-lifecycle | lifecycle | green | 0 | mutations/control-lifecycle.log | mutant lifecycle: PASS (normal/repeat, nine named defects, survivor, build, unread-file and Git-sett |
| M01-identity-includes-parent | suite | green | 0 | mutations-rerun/M01-identity-includes-parent.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
| M01b-send-recheck-includes-parent | suite | green | 0 | mutations-rerun/M01b-send-recheck-includes-parent.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
| M01c-identity-includes-parent-both | suite | red | 1 | mutations/M01c-identity-includes-parent-both.log | AssertionError: re-parented descendant was treated as new and never got SIGTERM |
| M02-no-reap-after-census | suite | red | 1 | mutations/M02-no-reap-after-census.log | RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s |
| M03-wall-clock | suite | red | 1 | mutations/M03-wall-clock.log | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M04-clamp-5s | suite | red | 1 | mutations/M04-clamp-5s.log | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M05-no-trap-window | suite | red | 1 | mutations/M05-no-trap-window.log | AssertionError: the shell was killed in the pass that resumed it, before its trap |
| M06-root-killed-unresumed | suite | red | 1 | mutations/M06-root-killed-unresumed.log | AssertionError: the shell was killed in the pass that resumed it, before its trap |
| M07-trap-child-no-window | suite | red | 1 | mutations/M07-trap-child-no-window.log | AssertionError: the resumed shell's trap command was killed inside the shell's window |
| M04c-clamp-1.5s | suite | red | 1 | mutations/M04c-clamp-1.5s.log | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M04d-clamp-1.0s | suite | green | 0 | mutations-rerun/M04d-clamp-1.0s.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
| M07b-trap-child-1s-window | suite | red | 1 | mutations/M07b-trap-child-1s-window.log | AssertionError: the resumed shell's trap command was killed inside the shell's window |
| M08-no-kill-before-fail | suite | red | 1 | mutations/M08-no-kill-before-fail.log | AssertionError: stopped shell left behind |
| M09-kill-before-fail-spares-shell | suite | red | 1 | mutations/M09-kill-before-fail-spares-shell.log | AssertionError: stopped shell left behind |
| M10-endless-unbounded | suite | red | 1 | mutations-rerun/M10-endless-unbounded.log | AssertionError: cleanup never reached a verdict |
| M11-trust-sigkill | suite | red | 1 | mutations-rerun/M11-trust-sigkill.log | AssertionError: a survivor never failed the run |
| M12-report-without-state | suite | red | 1 | mutations/M12-report-without-state.log | AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.05 s start 74775534, no |
| M13-cleanup-does-nothing-suite | suite | red | 1 | mutations/M13-cleanup-does-nothing-suite.log | AssertionError: re-parented descendant was treated as new and never got SIGTERM |
| M13-cleanup-does-nothing-lifecycle | lifecycle | red | 1 | mutations/M13-cleanup-does-nothing-lifecycle.log | AssertionError: ('1307', ('74777714', 'S'), ('74777714', 'S')) |
| M14-no-start-recheck | suite | green | 0 | mutations-rerun/M14-no-start-recheck.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
| M15-windows-2s | suite | green | 0 | mutations-rerun/M15-windows-2s.log | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, att |
