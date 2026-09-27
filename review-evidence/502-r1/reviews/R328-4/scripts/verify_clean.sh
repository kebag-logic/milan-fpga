#!/bin/sh
# R328-4: prove the candidate clone is byte-exact at the reviewed head after probes.
# Checks HEAD/tree, index vs HEAD tree, worktree bytes and modes vs index (no
# assume-unchanged/skip-worktree flags), untracked tracked-path absence, and the
# three required submodule gitlinks and their checkouts.
# Usage: verify_clean.sh <candidate-clone>
set -u
C=$1
cd "$C" || exit 2
fail=0
H=f80525e695ce7937ba1a2c1caa01ec9cdde93904
T=20b9e49f38cf575cb9980c5c49d4b6af89310b42
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD $H" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] && echo "tree $T" || { echo "TREE MISMATCH"; fail=1; }
[ "$(git write-tree)" = "$T" ] && echo "index writes tree $T" || { echo "INDEX != HEAD TREE"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' | grep -v '^S ' ; git ls-files -v | grep -E '^[a-zS] ' )
[ -z "$flags" ] && echo "no assume-unchanged/skip-worktree flags" || { echo "INDEX FLAGS PRESENT"; echo "$flags" | head; fail=1; }
# Re-hash every tracked regular file / symlink from disk and compare with the index entry.
bad=$(git ls-files -s | awk '$1 != "160000"' | while read -r mode oid stage path; do
  if [ "$mode" = "120000" ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin 2>/dev/null)
  else got=$(git hash-object --no-filters -- "$path" 2>/dev/null)
    m=$( [ -x "$path" ] && echo 100755 || echo 100644 ); [ "$m" = "$mode" ] || echo "MODE $path"
  fi
  [ "$got" = "$oid" ] || echo "BYTES $path"
done)
[ -z "$bad" ] && echo "all tracked blobs and modes match the index" || { echo "$bad" | head -20; fail=1; }
st=$(git status --porcelain --untracked-files=no)
[ -z "$st" ] && echo "status clean (tracked)" || { echo "$st"; fail=1; }
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git ls-tree HEAD "$s" | awk '{print $3}')
  got=$(git -C "$s" rev-parse HEAD)
  d=$(git -C "$s" status --porcelain | wc -l)
  if [ "$want" = "$got" ] && [ "$d" -eq 0 ]; then echo "submodule $s $got clean"; else echo "SUBMODULE $s want $want got $got dirty $d"; fail=1; fi
done
echo "verify_clean rc=$fail"
exit $fail
