#!/usr/bin/env bash
# Reviewer probe (F5): a deprecated Git setting makes Git print a warning on
# stderr; record what the production mutation driver does with it.
# Usage: probe_git_stderr_warning.sh COPY   (restores the setting afterwards)
set -u
copy="$1"
git -C "$copy" config core.fsyncObjectFiles true
out=$(cd "$copy/tb/verilator/gptp_shadow" && env -u GIT_EDITOR PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 mutants.py 2>&1); rc=$?
git -C "$copy" config --unset core.fsyncObjectFiles
echo "case: deprecated core.fsyncObjectFiles in the copy's .git/config (Git prints a warning on stderr)"
echo "exit $rc"
printf '%s\n' "$out" | tail -3
