#!/usr/bin/env bash
# Scratch parent for packing only: mk_parent.sh <dst> <parent src clone> <processor clone> <processor commit> <c4c6 patch> <c8 patch>
# Copies the parent tree, replaces protocol-processor with a clone of the
# processor at <commit>, applies the C4C6 patch, then the C8 patch; where the
# C8 patch's avdecc/aem_assemble.py hunk does not apply (PR #634), it is
# applied without that file and its one added keyword is ported by hand.
set -euo pipefail
dst=$1; src=$2; pp=$3; rev=$4; c4c6=$5; c8=$6
rm -rf "$dst"; mkdir -p "$dst"
git -C "$src" archive HEAD | tar -x -C "$dst"
cd "$dst"
git init -q && git add -A && git -c user.name=s -c user.email=s@localhost commit -q -m "parent $(git -C "$src" rev-parse HEAD)"
rmdir protocol-processor 2>/dev/null || rm -rf protocol-processor
git clone -q "$pp" protocol-processor && git -C protocol-processor checkout -q "$rev"
echo "parent $(git -C "$src" rev-parse HEAD) processor $(git -C protocol-processor rev-parse HEAD)"
git apply "$c4c6" && echo "applied $(basename "$c4c6")"
if git apply --check "$c8" 2>/dev/null; then
  git apply "$c8" && echo "applied $(basename "$c8")"
else
  git apply --exclude=avdecc/aem_assemble.py "$c8" && echo "applied $(basename "$c8") except avdecc/aem_assemble.py"
  python3 - <<'EOF'
from pathlib import Path
p = Path("avdecc/aem_assemble.py"); t = p.read_text()
old = "PER_STREAM=per_stream, DYNMAP=dynmap, ODMAP=odmap, SMAP=smap)"
assert t.count(old) == 1, t.count(old)
p.write_text(t.replace(old, "PER_STREAM=per_stream, DYNMAP=dynmap, ODMAP=odmap, SMAP=smap,\n"
                            "                LINT_WAIVERS=spec.get(\"lint_waivers\", []))"))
print("ported the aem_assemble.py LINT_WAIVERS line by hand")
EOF
fi
git diff --stat | tail -1
