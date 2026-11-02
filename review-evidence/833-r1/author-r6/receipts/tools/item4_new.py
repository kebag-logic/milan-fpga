NEW = {
    "check-before-open": ("owner_reused_identity", "a census entry was signalled by its number",
        ("        try:\n            fd = os.pidfd_open(pid)\n        except ProcessLookupError:\n            return False\n"
         "        try:\n            identity = _identity(pid)\n            if identity is None or identity[1] != start:\n"
         "                return False\n",
         "        identity = _identity(pid)\n        if identity is None or identity[1] != start:\n            return False\n"
         "        try:\n            fd = os.pidfd_open(pid)\n        except ProcessLookupError:\n            return False\n"
         "        try:\n")),
    "no-sigterm": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    continue\n                elif")),
    "kill-all-a-pass-late": ("owner_stated_seconds", "a stubborn parent's stated seconds were not kept",
        ("                elif clock < kill_all:\n", "                elif clock <= kill_all:\n")),
    "verdict-past-deadline": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
         "if clock > limit and (owned or clock >= limit + REAP_SECONDS):")),
    "resume-only-when-alone": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("and not (live - {root_pid}):", "and not (set(owned) - {root_pid}):")),
    "trap-window-from-grace": ("owner_stated_seconds", "a late resume's stated seconds were not kept",
        ("kill_all = max(kill_all, clock + TRAP_SECONDS)", "kill_all = max(kill_all, deadline + TRAP_SECONDS)")),
    "shell-spared-only-while-stopped": ("owner_shell_window", "the shell was killed in the pass that resumed it,"
                                                              " before its trap",
        ("(resumed is None or clock < kill_all)", "(resumed is None or (_stat(pid) or ['T'])[0] == 'T')")),
    "trap-commands-until-grace": ("owner_shell_window", "the resumed shell's trap command was killed inside the"
                                                        " shell's window",
        ("if (pid, start) not in initial and resumed is not None:",
         "if (pid, start) not in initial and resumed is not None and clock < deadline + 1.0:")),
    "cap-on-total": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("clock += min(now - last, MAX_PASS_SECONDS)", "clock = min(clock + now - last, MAX_PASS_SECONDS * passes)")),
    "first-pass-full-cap": ("owner_stated_seconds", "a survivor's stated seconds were not kept",
        ("        started = last = time.monotonic()\n",
         "        started = time.monotonic()\n        last = started - MAX_PASS_SECONDS\n")),
    "vanishing-waits-from-grace": ("owner_stated_seconds", "a vanishing listing's stated seconds were not kept",
        ("(owned or clock >= limit + REAP_SECONDS)", "(owned or clock >= deadline + 2 * REAP_SECONDS)")),
    "verdict-counts-census": ("owner_late_exit", "CLEANUP FAILED: owned descendants remain",
        ("if clock >= limit and (owned or clock >= limit + REAP_SECONDS):",
         "if clock >= limit and (census or clock >= limit + REAP_SECONDS):")),
    "sigterm-needs-live-parent": ("owner_reparented", "SIGTERM waited for a later census",
        ("                    if (pid, start) not in initial:\n                        continue\n                elif",
         "                    if (pid, start) not in initial or not _live(_parent):\n                        continue\n"
         "                elif")),
    "resume-unless-reaped-now": ("owner_late_cancel", "a cancel after the shell was collected resumed it",
        ("resumed is None and root_pid in owned and not (live - {root_pid}):",
         "resumed is None and root_pid not in reaped and not (live - {root_pid}):")),
    "verdict-kills-only-the-killed": ("owner_survivor", "stopped shell left behind",
        ("                for pid, (_parent, start) in owned.items():\n"
         "                    self._send(pid, start, signal.SIGKILL)\n",
         "                for pid, (_parent, start) in owned.items():\n"
         "                    if pid in killed:\n"
         "                        self._send(pid, start, signal.SIGKILL)\n")),
    "report-parent-is-first-parent": ("owner_report", "the report's current parent is not its own field",
        ("parent {fields[1]} ", "parent {first_parent} ")),
}
