#!/usr/bin/env bash
# Delta identity checks for PR #159 round R477-2: the commit OLD..NEW changes
# comment lines only in hdl/aecp/KL_aecp_notify.sv, and the module's sv2v and
# preprocessed output are byte-identical.
# Usage: delta_identity.sh <repo> <old-rev> <new-rev> <scratch-dir> <verilator>
set -euo pipefail
repo=$1 old=$2 new=$3 scr=$4 vl=$5
f=hdl/aecp/KL_aecp_notify.sv
echo "== revs"; git -C "$repo" rev-parse "$old" "$new" "$new^{tree}"
echo "== parent of new"; git -C "$repo" rev-parse "$new^"
echo "== changed paths old..new"; git -C "$repo" diff --name-status "$old" "$new"
echo "== numstat"; git -C "$repo" diff --numstat "$old" "$new"
echo "== raw diff"; git -C "$repo" --no-pager diff "$old" "$new"
echo "== changed lines are comments (+/- lines not starting with //)"
git -C "$repo" --no-pager diff -U0 "$old" "$new" -- "$f" \
  | grep -E '^[+-][^+-]' | grep -Ev '^[+-][[:space:]]*//' || echo "none: every changed line is a // comment"
for r in "$old" "$new"; do
  d="$scr/tree-$r"; rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive "$r" hdl | tar -x -C "$d"
done
o="$scr/tree-$old" n="$scr/tree-$new"
echo "== hdl trees: files differing"; diff -rq "$o/hdl" "$n/hdl" || true
strip() { python3 - "$1" <<'PY'
import re,sys
s=open(sys.argv[1]).read()
s=re.sub(r'/\*.*?\*/','',s,flags=re.S)
s=re.sub(r'//[^\n]*','',s)
print('\n'.join(l.rstrip() for l in s.splitlines() if l.strip()))
PY
}
strip "$o/$f" > "$scr/old.nocomment"; strip "$n/$f" > "$scr/new.nocomment"
echo "== comment-stripped source equal:"; cmp "$scr/old.nocomment" "$scr/new.nocomment" && echo IDENTICAL
pk=(); for p in $(cd "$o" && find hdl -name '*_pkg.sv' | sort); do pk+=("$p"); done
for t in "$o" "$n"; do
  ( cd "$t" && sv2v "${pk[@]}" "$f" > module.sv2v.v )
  ( cd "$t" && sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > all.sv2v.v )
  ( cd "$t" && "$vl" -E -P "${pk[@]}" "$f" | grep -v '^[[:space:]]*$' > module.vpp )
done
for a in module.sv2v.v all.sv2v.v module.vpp; do
  echo "== $a"; sha256sum "$o/$a" "$n/$a" | sed "s#$scr/##"; cmp "$o/$a" "$n/$a" && echo "$a IDENTICAL"
done
echo "== lint module at new"; ( cd "$n" && "$vl" --lint-only -Wall -Wno-fatal "${pk[@]}" "$f" --top-module KL_aecp_notify 2>&1 | tail -5; echo "lint rc ${PIPESTATUS[0]}" )
