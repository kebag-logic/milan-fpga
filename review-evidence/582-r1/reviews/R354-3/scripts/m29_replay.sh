#!/usr/bin/env bash
# R354-3 replay of R354-2 M29 against the round-3 text of docs/testing/CI_WORKFLOWS.md.
# Usage: m29_replay.sh <repo-root> <scratch-dir> <parent-commit>
# M29 (R354-2) deleted the tap-page row of the documentation-only table. At
# this head that row no longer exists, so two analogues are run:
#   M29a deletes the round-3 relevance clause (the three lines that say why
#        the tap page stays relevant although docs-check also runs its check);
#   M29b restores the parent's table introduction and tap-page row, i.e. the
#        state R354-2 F1 was raised against.
# Each is judged by ci_scope.py --selftest, ci_events.py --check,
# docs_check.py and the reviewer's classification probe.
set -u
repo=$1 scratch=$2 parent=$3
here=$(cd "$(dirname "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$scratch"

judge() {  # judge <label> <tree>
    local t=$2 c rc
    for c in "scripts/ci_scope.py --selftest" "scripts/ci_events.py --check" "scripts/docs_check.py" \
             "$here/classification_probe.py ."; do
        (cd "$t" && python3 $c > /dev/null 2>&1); rc=$?
        printf 'PROBE %-5s %-44s rc=%s %s\n' "$1" "${c/$here\//}" "$rc" "$([ $rc -eq 0 ] && echo SURVIVES || echo KILLS)"
    done
}

for m in M29a M29b CTL; do
    t="$scratch/$m"; rm -rf "$t"
    rsync -a --exclude=__pycache__ "$repo/" "$t/"
    f="$t/docs/testing/CI_WORKFLOWS.md"
    case $m in
    M29a)
        python3 - "$f" <<'EOF'
import sys
p = sys.argv[1]; s = open(p).read()
cut = ("The tap page remains relevant under the #582 decision.\n"
       "Its reader is absent from `DOCS_JOB_PY`.\n"
       "`docs-check` also runs it through the builder bank.\n")
assert s.count(cut) == 1
open(p, "w").write(s.replace(cut, ""))
EOF
        ;;
    M29b)
        git -C "$repo" show "$parent:docs/testing/CI_WORKFLOWS.md" > "$f" ;;
    CTL) ;;
    esac
    judge "$m" "$t"
done
