#!/usr/bin/env bash
# Semantic-interaction scan: which candidate gates/docs name the files the PR
# changed, what the dev-changed readers say about them, and whether dev-side
# code uses signals, sessions, process groups or terminals that could collide
# with the PR's process owner. Read-only on <repo>.
# Usage: reader_scan.sh <repo> <receipt-dir>
set -euo pipefail
repo=$1
out=$2
mkdir -p "$out"
g() { git -C "$repo" -c core.pager=cat -c color.ui=never "$@"; }
{
  echo "## tracked gates/docs naming each PR-changed file (candidate HEAD)"
  for f in run_all_suites.sh TESTING.md owned_process process_test_support \
           test_suite_cancellation private_inputs test_mutant_lifecycle mutants.py \
           check_baremetal_only measure_test_evidence gptp_shadow; do
    echo "### $f"
    g grep -l -F "$f" -- scripts syn .github docs/testing tb/verilator || true
  done
} > "$out/07_readers_of_pr_files.txt"
{
  echo "## dev-changed readers: lines naming PR-changed files"
  g grep -n -F run_all_suites.sh -- scripts/check_merge_containment.py scripts/merge_containment_selftest.py || true
  g grep -n -E 'run_all_suites|check_baremetal_only|measure_test_evidence|gptp_shadow|TESTING\.md' -- scripts/ci_events.py || true
  g grep -n gptp_shadow -- syn/yosys/run.sh syn/yosys/README.md || true
  g grep -n -E 'run_all_suites|gptp_shadow|measure_test_evidence' -- docs/testing/CI_WORKFLOWS.md || true
  echo "## CI_WORKFLOWS.md exit-status statements"
  g grep -n -E '\b(90|91|92|130|143)\b' -- docs/testing/CI_WORKFLOWS.md || true
} > "$out/08_reader_lines.txt"
{
  echo "## dev-side changed code: signal/session/process-group/terminal use"
  files=$(g diff --name-only 776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d ede8d48ecd7c7f589a14b957951f040d92c99c70 -- '*.py' '*.sh')
  echo "files scanned:"; echo "$files"
  echo "matches:"
  # shellcheck disable=SC2086
  g grep -n -E '\bkillpg\b|os\.kill\(|\bsignal\.(signal|SIG)|\bsetsid\b|start_new_session|\bpty\b|openpty|getpgrp|setpgid|\bprctl\b|/proc/|preexec_fn|os\.fork\b|\btrap\b|\bkill -' -- $files || echo "  <none>"
} > "$out/09_dev_side_process_usage.txt"
echo "reader scan written to $out"
