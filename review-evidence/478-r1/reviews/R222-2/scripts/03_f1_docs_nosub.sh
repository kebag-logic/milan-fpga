#!/usr/bin/env bash
# F1 re-check at the corrected head, in the two contexts the required hosted
# documentation jobs use: a Git checkout before any submodule is initialized
# (docs-check's pre-submodule steps) and a tree with no .git at all
# (docs-check-no-git). Each context runs the pristine head, then a negative
# control that restores ONLY the round-1 relative link, then the pristine head
# again. Scratch copies only.
set -uo pipefail
S=${SCRATCH:-/tmp/r222-478-r2-scratch}
DOC=docs/ENDSTATION_BUILDER.md
OLD='](../protocol-processor/docs/architecture/07_memory_maps.md#31-descriptor-tree)'
NEW='](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/424c688fa2205b934a7689a58f2aa766420f2326/docs/architecture/07_memory_maps.md#31-descriptor-tree)'
PIN_BLOB=b66600c8326b7eeb91fc53de111f6585c7b3d47a   # head blob of $DOC

run() { # <label> <dir> <cmd...>
  local label=$1 dir=$2; shift 2
  local out; out=$(cd "$dir" && "$@" 2>&1); local rc=$?
  echo "--- [$label] (cd $(basename "$dir") && $*) -> exit $rc"
  printf '%s\n' "$out" | grep -E 'broken link|ENDSTATION_BUILDER|finding|FAIL|PASS|OK|error|Error' | head -20
  printf '%s\n' "$out" | tail -3
}
swap() { # <dir> <from> <to>
  python3 - "$1/$DOC" "$2" "$3" <<'PY'
import sys
p, a, b = sys.argv[1:]
s = open(p, encoding="utf-8").read()
assert s.count(a) == 1, f"expected exactly one occurrence, got {s.count(a)}"
open(p, "w", encoding="utf-8").write(s.replace(a, b))
PY
}
blob() { git hash-object --no-filters "$1/$DOC"; }

echo "## link line at head (line numbers from the head blob)"
grep -n -F "$NEW" "$S/git-nosub/$DOC" | cut -c1-60
echo "occurrences of the new target: $(grep -c -F "$NEW" "$S/git-nosub/$DOC")"
echo "occurrences of any ../protocol-processor/ link in tracked Markdown:"
( cd "$S/git-nosub" && git grep -n -E '\]\(\.\./+protocol-processor/|\]\((\.\./)*protocol-processor/' -- '*.md' | cut -c1-120 ) || echo "  none"

for ctx in git-nosub nogit; do
  D="$S/$ctx"
  echo; echo "########## context $ctx"
  echo "submodule dirs empty: $(for p in protocol-processor gptp-processor third_party/verilog-axis external; do find "$D/$p" -mindepth 1 | head -1; done | wc -l | sed 's/^0$/yes/')"
  echo ".git present: $([ -e "$D/.git" ] && echo yes || echo no)"
  echo "doc blob before: $(blob "$D") (expect $PIN_BLOB)"
  run "$ctx pristine docs_check" "$D" python3 scripts/docs_check.py
  swap "$D" "$NEW" "$OLD"
  echo "doc blob with old link restored: $(blob "$D")"
  run "$ctx old-link control docs_check" "$D" python3 scripts/docs_check.py
  swap "$D" "$OLD" "$NEW"
  echo "doc blob restored: $(blob "$D") (expect $PIN_BLOB)"
  run "$ctx pristine-again docs_check" "$D" python3 scripts/docs_check.py
  run "$ctx check_feature_status" "$D" python3 scripts/check_feature_status.py
done
echo; echo "## git-nosub still clean: $(git -C "$S/git-nosub" status --porcelain | wc -l) changed paths"
