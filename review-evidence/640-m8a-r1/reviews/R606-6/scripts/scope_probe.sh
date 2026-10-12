#!/usr/bin/env bash
# Classify each path this PR changes, plus docs-only controls, through the
# candidate's scripts/ci_scope.py, feeding stdin exactly as rtl-fast's `changes` job does.
# Usage: scope_probe.sh <repo> <pr-base> <pr-head>
set -u
cd "$1" || exit 2
while read -r p; do printf '%-45s %s\n' "$p" "$(printf '%s\n' "$p" | python3 scripts/ci_scope.py)"; done < <(git diff --no-renames --name-only "$2" "$3")
echo "-- whole PR list: $(git diff --no-renames --name-only "$2" "$3" | python3 scripts/ci_scope.py)"
echo "-- whole candidate list vs dev: $(git diff --no-renames --name-only "$2" HEAD | python3 scripts/ci_scope.py)"
for p in docs/testing/CI_WORKFLOWS.md docs/design/MARK_II_AREA_PLAN.md docs/README.md README.md; do
  printf '%-45s %s\n' "control:$p" "$(printf '%s\n' "$p" | python3 scripts/ci_scope.py)"; done
printf '%-45s %s\n' "control:docs-only PR subset" "$(git diff --no-renames --name-only "$2" "$3" -- 'docs/*.md' ':!docs/design/SPLIT_CONTROL_MEMORY.md' ':!docs/design/AREA_BUDGET.md' | python3 scripts/ci_scope.py)"
