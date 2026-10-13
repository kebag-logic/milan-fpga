#!/usr/bin/env bash
# R624-12: documentation and scope gates on the candidate tree, concurrently, each with its own log and rc.
# usage: run_gates.sh CANDIDATE_REPO PARSER_PY OUT
set -uo pipefail
CAND=$1 PY=$2 OUT=$3
mkdir -p "$OUT"
cd "$CAND" || exit 2
g() { # name timeout cmd...
  local n=$1 t=$2; shift 2
  ( rc=0; timeout "$t" "$@" >"$OUT/$n.log" 2>&1 || rc=$?; echo "$rc" >"$OUT/$n.rc" ) &
}
g docs-check 600 "$PY" -B scripts/docs_check.py
g doc-style 300 "$PY" -B scripts/check_doc_style.py
g toc-check 600 "$PY" -B scripts/gen_toc.py --check
g toc-verify-anchors 600 "$PY" -B scripts/gen_toc.py --verify-anchors
g em-dash-parent 300 "$PY" -B scripts/check_em_dash.py --base cdb49e7ec8b2e03f835a9bda2230ef3e26788c16
g em-dash-lane-base 300 "$PY" -B scripts/check_em_dash.py --base e8454e27
g doc-paths 300 "$PY" -B scripts/check_doc_paths.py
g ci-scope-selftest 600 python3 -B scripts/ci_scope.py --selftest
g ci-events-check 600 python3 -B scripts/ci_events.py --check
g baremetal-only-check 600 python3 -B scripts/check_baremetal_only.py --check
g feature-status-selftest 300 python3 -B scripts/check_feature_status.py --self-test
g diff-check-merge 60 git diff --check cdb49e7ec8b2e03f835a9bda2230ef3e26788c16 ada26e56ac42ee5de311aef84cb86c8435b97cee
g diff-check-worktree 60 git diff --check
wait
for f in "$OUT"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
