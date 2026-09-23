#!/bin/sh
# Prove what changed between the prior review heads and the head under review,
# and that the one HDL change is comment-only (preprocessed-output equality).
# Usage: delta_proof.sh <clone-dir> <scratch-dir> <verilator>
set -eu
C=${1:?clone}; S=${2:?scratch}; V=${3:?verilator}
R1=6d1572d6caeb94cd3dd871b9df90e4c5298998b6   # previous R262 round (R262-1)
M=553edeb86b9144f7b15721255fbe5ad11ef1fe36    # matrix regeneration head
H=2accfadfd3d4d8a318e3e714ee0dc87fc84e4164    # head under review
cd "$C"
for pair in "$R1 $M" "$M $H" "$R1 $H"; do
  set -- $pair
  echo "== git diff --stat --no-renames $1..$2"; git diff --no-ext-diff --stat --no-renames "$1" "$2"
  echo "== raw entries"; git diff --no-ext-diff --raw --no-renames "$1" "$2"
done
echo "== paths changed $R1..$H outside docs/ and *.md:"
git diff --name-only "$R1" "$H" | grep -v -E '^docs/|\.md$' || echo "  (none)"
mkdir -p "$S/delta"
for rev in $R1 $M $H; do
  git show "$rev:hdl/ieee1722/crf/KL_media_grid_align.sv" > "$S/delta/mga_$rev.sv"
  "$V" -E -P "$S/delta/mga_$rev.sv" > "$S/delta/mga_$rev.E.txt"
  echo "preprocessed sha256 @$rev: $(sha256sum < "$S/delta/mga_$rev.E.txt" | cut -d' ' -f1)  raw blob $(git rev-parse "$rev:hdl/ieee1722/crf/KL_media_grid_align.sv")"
done
# independent second method: strip /* */ and // comments with a tokeniser-free
# python pass and compare the remaining text
python3 - "$S/delta/mga_$M.sv" "$S/delta/mga_$H.sv" <<'PY'
import re,sys,hashlib
def strip(t):
    t=re.sub(r'/\*.*?\*/','',t,flags=re.S)
    t=re.sub(r'//[^\n]*','',t)
    return '\n'.join(l.rstrip() for l in t.splitlines() if l.strip())
a,b=(strip(open(p).read()) for p in sys.argv[1:3])
print("comment-stripped equal:",a==b, hashlib.sha256(a.encode()).hexdigest()[:16], hashlib.sha256(b.encode()).hexdigest()[:16])
PY
echo "== hunk line range of the $M..$H .sv change vs the banner comment span"
git diff -U0 "$M" "$H" -- hdl/ieee1722/crf/KL_media_grid_align.sv | grep '^@@'
awk 'NR==3 || NR==101 {print "  line " NR ": " $0}' "$S/delta/mga_$H.sv"
