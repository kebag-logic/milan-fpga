| Mutant | Test | At 1ff8292c (round 2) | At 3740565f | rc | Seconds | Last line |
|---|---|---|---|---:|---:|---|
| control-A | suite | green | green | 0 | 57.0 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| control-B | suite | green | green | 0 | 57.0 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| control-lifecycle | lifecycle | green | green | 0 | 34.5 | mutant lifecycle: PASS (normal/repeat, nine named defects, survivor, build, unread-file and Git-setting accept |
| M01-identity-includes-parent | suite | green | green | 0 | 57.2 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| M01b-send-recheck-includes-parent | suite | green | green | 0 | 57.0 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| M01c-identity-includes-parent-both | suite | red | red | 1 | 2.2 | AssertionError: re-parented descendant was treated as new and never got SIGTERM |
| M02-no-reap-after-census | suite | red | red | 1 | 0.8 | RuntimeError: CLEANUP FAILED: owned descendants remain after 0.47 s, 1 census passes, slowest 0.47 s: pid 5 (p |
| M03-wall-clock | suite | red | red | 1 | 2.9 | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M04-clamp-5s | suite | red | red | 1 | 2.9 | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M05-no-trap-window | suite | red | red | 1 | 4.7 | AssertionError: the shell was killed in the pass that resumed it, before its trap |
| M06-root-killed-unresumed | suite | red | red | 1 | 4.6 | AssertionError: the shell was killed in the pass that resumed it, before its trap |
| M07-trap-child-no-window | suite | red | red | 1 | 4.7 | AssertionError: the resumed shell's trap command was killed inside the shell's window |
| M04c-clamp-1.5s | suite | red | red | 1 | 2.8 | AssertionError: the stall was charged in full: SIGKILL in pass [2] |
| M04d-clamp-1.0s | suite | green | green | 0 | 56.6 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| M07b-trap-child-1s-window | suite | red | red | 1 | 5.7 | AssertionError: the resumed shell's trap command was killed inside the shell's window |
| M16-resume-collected-shell | suite | new | red | 1 | 8.1 | AssertionError: a cancel after the shell was collected resumed it, re-arming its trap window |
| M16b-window-without-resume | suite | new | red | 1 | 23.1 | AssertionError: cleanup never reached a verdict after a late cancel |
| M16c-resume-while-listed | suite | new | green | 0 | 57.7 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| M08-no-kill-before-fail | suite | red | red | 1 | 24.2 | AssertionError: stopped shell left behind |
| M09-kill-before-fail-spares-shell | suite | red | red | 1 | 24.3 | AssertionError: stopped shell left behind |
| M10-endless-unbounded | suite | red | red | 1 | 22.3 | AssertionError: cleanup never reached a verdict |
| M11-trust-sigkill | suite | red | red | 1 | 38.2 | AssertionError: a survivor never failed the run |
| M12-report-without-state | suite | red | red | 1 | 2.1 | AssertionError: ('state S', 'pid 2 (python3) parent 1 (first parent 1) age 0.02 s start 75412916, not sent SIG |
| M13-cleanup-does-nothing-suite | suite | red | red | 1 | 0.2 | AssertionError: re-parented descendant was treated as new and never got SIGTERM |
| M13-cleanup-does-nothing-lifecycle | lifecycle | red | red | 1 | 15.7 | AssertionError: ('1307', ('75414825', 'S'), ('75414825', 'S')) |
| M14-no-start-recheck | suite | green | green | 0 | 57.2 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
| M15-windows-2s | suite | green | green | 0 | 56.9 | suite cancellation: PASS (INT/TERM boundaries, reaped identities, foreign sibling, partial logs, attributed ca |
