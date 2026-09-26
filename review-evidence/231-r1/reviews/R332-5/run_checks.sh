#!/usr/bin/env bash
# R332-5 delta checks. Usage: run_checks.sh <clone> <receipt-dir>
# Runs each command in the foreground, records stdout/stderr and exit status.
set -u
clone=${1:?clone}
out=${2:?receipt dir}
base=7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
mkdir -p "$out"
cd "$clone" || exit 2
run() {
  local name=$1; shift
  "$@" >"$out/$name.log" 2>&1
  local rc=$?
  printf '%s rc=%s cmd=%s\n' "$name" "$rc" "$*" | tee -a "$out/status.txt"
}
: >"$out/status.txt"
git rev-parse HEAD 'HEAD^{tree}' >"$out/head.txt"
run selftest python3 syn/ooc/pp_baseline.py --selftest
run mutants python3 syn/ooc/pp_baseline_mutants.py
run reports_selftest python3 syn/ooc/pp_baseline_reports_selftest.py
run docs_check_git python3 scripts/docs_check.py
run docs_check_nogit env GIT_DIR=/dev/null python3 scripts/docs_check.py
run em_dash python3 scripts/check_em_dash.py --base "$base"
run doc_style python3 scripts/check_doc_style.py
run toc_check python3 scripts/gen_toc.py --check
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run doc_paths python3 scripts/check_doc_paths.py
git status --porcelain=v2 --untracked-files=all >"$out/status_after.txt"
