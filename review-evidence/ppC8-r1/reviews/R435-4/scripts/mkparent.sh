#!/bin/bash
# mkparent.sh <out-dir> <parent-git-dir> <parent-rev> <processor-git-dir> <processor-rev> [patch...]
# Builds a disposable parent tree: git archive of the parent at <parent-rev>,
# the processor archived at <processor-rev> into protocol-processor/, then each
# patch applied with git apply. If a patch does not apply whole, its
# avdecc/aem_assemble.py hunk is ported by a one-line substitution (the C8
# patch's LINT_WAIVERS keyword, as its author records for PR #634) and the
# rest applied with --exclude. Prints what it did.
set -euo pipefail
out=$1; prepo=$2; prev=$3; pprepo=$4; pprev=$5; shift 5
rm -rf "$out"; mkdir -p "$out"
git -C "$prepo" archive "$prev" | tar -x -C "$out"
rm -rf "$out/protocol-processor"; mkdir -p "$out/protocol-processor"
git -C "$pprepo" archive "$pprev" | tar -x -C "$out/protocol-processor"
cd "$out"
git init -q && git -c user.name=s -c user.email=s@localhost add -A >/dev/null
git -c user.name=s -c user.email=s@localhost commit -q -m base
echo "parent $prev tree-of-archive $(git rev-parse HEAD^{tree}) processor $pprev"
for p in "$@"; do
  if git apply --check "$p" 2>/dev/null; then
    git apply "$p"; echo "applied $(basename "$p") whole"
  else
    git apply --exclude=avdecc/aem_assemble.py "$p"
    python3 - <<'EOF'
from pathlib import Path
f = Path("avdecc/aem_assemble.py")
s = f.read_text()
old = "PER_STREAM=per_stream, DYNMAP=dynmap, ODMAP=odmap, SMAP=smap)"
new = ("PER_STREAM=per_stream, DYNMAP=dynmap, ODMAP=odmap, SMAP=smap,\n"
       "                LINT_WAIVERS=spec.get(\"lint_waivers\", []))")
assert s.count(old) == 1, s.count(old)
f.write_text(s.replace(old, new))
EOF
    echo "applied $(basename "$p") with aem_assemble.py ported by one substitution"
  fi
done
git -c user.name=s -c user.email=s@localhost add -A >/dev/null
git diff --cached --stat | tail -1
