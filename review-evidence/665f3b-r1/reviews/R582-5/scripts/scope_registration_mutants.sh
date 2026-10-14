#!/bin/sh
# Plant two edits of the MAILBOX_SPLIT.md gate-read registration in a disposable
# archive of the head and require scripts/ci_scope.py --selftest to refuse each.
# Usage: scope_registration_mutants.sh <repo> <empty-scratch-dir>
set -eu
repo=${1:?repo}
work=${2:?scratch}
HEAD_C=7032bca5a51d8d97fcb73d7fc106ca4af21de38e
mkdir -p "$work/tree"
git -C "$repo" archive "$HEAD_C" | tar -x -C "$work/tree"
cd "$work/tree"
export PYTHONDONTWRITEBYTECODE=1
cp scripts/ci_scope.py "$work/ci_scope.orig"
if python3 scripts/ci_scope.py --selftest > "$work/base.log" 2>&1; then echo "baseline: PASS"; else echo "baseline: FAIL"; exit 1; fi
status=0
for k in remove case_flip; do
    cp "$work/ci_scope.orig" scripts/ci_scope.py
    python3 -I - "$k" <<'EOF'
import sys
p = "scripts/ci_scope.py"
s = open(p).read()
old, new = {
    "remove": ('    "docs/design/MAILBOX_SPLIT.md",\n', ""),
    "case_flip": ('(["docs/design/MAILBOX_SPLIT.md"], True)', '(["docs/design/MAILBOX_SPLIT.md"], False)'),
}[sys.argv[1]]
assert s.count(old) == 1, "fixture not unique"
open(p, "w").write(s.replace(old, new))
EOF
    if python3 scripts/ci_scope.py --selftest > "$work/$k.log" 2>&1; then
        echo "mutant $k: ESCAPED"; status=1
    else
        echo "mutant $k: caught: $(grep FAIL "$work/$k.log" | tr '\n' '|')"
    fi
done
cp "$work/ci_scope.orig" scripts/ci_scope.py
echo "restored classification of docs/design/MAILBOX_SPLIT.md: $(python3 scripts/ci_scope.py docs/design/MAILBOX_SPLIT.md)"
exit $status
