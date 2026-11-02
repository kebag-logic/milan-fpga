| mutant | report | reparented | late_exit | stall | shell_window | survivor | vanishing | late_cancel | red |
|---|---|---|---|---|---|---|---|---|---|
| M05-no-trap-window | ok | ok | ok | ok | RED(3/3) | ok | ok | ok | 1 |
| M06-root-killed-unresumed | ok | ok | ok | ok | RED(3/3) | ok | ok | ok | 1 |
| no-trap-window | ok | ok | ok | ok | RED(3/3) | ok | ok | ok | 1 |
| none | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| shell-killed-when-resumed | ok | ok | ok | ok | RED(3/3) | ok | ok | ok | 1 |
| shell-window-1s | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| shell-window-one-pass | ok | ok | ok | ok | ok | ok | ok | ok | 0 |
| trap-commands-1s | ok | ok | ok | ok | RED(3/3) | ok | ok | ok | 1 |
| trap-commands-no-window | ok | ok | ok | ok | RED(3/3) | ok | ok | ok | 1 |

- M05-no-trap-window / owner_shell_window #0 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- M05-no-trap-window / owner_shell_window #1 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- M05-no-trap-window / owner_shell_window #2 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- M06-root-killed-unresumed / owner_shell_window #0 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- M06-root-killed-unresumed / owner_shell_window #1 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- M06-root-killed-unresumed / owner_shell_window #2 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / owner_shell_window #0 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / owner_shell_window #1 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- no-trap-window / owner_shell_window #2 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / owner_shell_window #0 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / owner_shell_window #1 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- shell-killed-when-resumed / owner_shell_window #2 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the shell was killed in the pass that resumed it, before its trap
- trap-commands-1s / owner_shell_window #0 (2.7 s): owner_shell_window FAIL 2.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / owner_shell_window #1 (2.7 s): owner_shell_window FAIL 2.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-1s / owner_shell_window #2 (2.7 s): owner_shell_window FAIL 2.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-no-window / owner_shell_window #0 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-no-window / owner_shell_window #1 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
- trap-commands-no-window / owner_shell_window #2 (1.7 s): owner_shell_window FAIL 1.6s AssertionError: the resumed shell's trap command was killed inside the shell's window
