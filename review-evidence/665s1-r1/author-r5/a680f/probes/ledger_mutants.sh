#!/bin/bash
# Plants three defects, one at a time, into a disposable worktree's
# sw/litex/ctrl_memory.py and runs test_ctrl_memory.py on each; every plant must
# turn the test red. $1 the worktree, $2 the output directory, $3 LiteX's python.
set -u
T=$1 OUT=$2 PY=$3
cd "$T" || exit 2
[ -z "$(git status --short)" ] || { echo "worktree not clean"; exit 2; }
failed=0
plant() {
    local name=$1 old=$2 new=$3
    python3 -I - "$old" "$new" <<'PY' || { echo "$name: plant site not found"; failed=$((failed + 1)); return; }
import sys
p = "sw/litex/ctrl_memory.py"
s = open(p).read()
old, new = sys.argv[1], sys.argv[2]
if s.count(old) != 1:
    sys.exit(1)
open(p, "w").write(s.replace(old, new))
PY
    "$PY" sw/litex/test_ctrl_memory.py > "$OUT/$name.txt" 2>&1
    local rc=$?
    git checkout -q -- sw/litex/ctrl_memory.py
    local named
    named=$(grep -c '^  \[FAIL' "$OUT/$name.txt")
    echo "$name: rc=$rc (must be 1) $named failing checks (must be at least 1)"
    grep '^  \[FAIL' "$OUT/$name.txt" | cut -c1-220
    [ $rc = 1 ] && [ "$named" -gt 0 ] || failed=$((failed + 1))
}
plant ledger-back-to-57 '                                   57.5, "lane S14' '                                   57.0, "lane S14'
plant ledger-at-58 '                                   57.5, "lane S14' '                                   58.0, "lane S14'
plant override-on-any-image 'if carried != dict(point.symbols):' 'if False:'
echo "ledger plants: $failed escaped"
exit $((failed > 0))
