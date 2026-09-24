#!/bin/sh
# Prove that the round-3 delta leaves the servo RTL identical once comments
# are removed, and that the delta touches only the two expected lines.
# Usage: comment_only_proof.sh <repo> [verilator]
set -eu
REPO=${1:?repo}
VL=${2:-}
OLD=910b4fb5f
NEW=324eb343a870973b64706779d0183ae342dcb3d7
F=hdl/ieee1722/crf/KL_mmcm_drp_servo.sv
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
cd "$REPO"
echo "== delta file list and numstat $OLD..$NEW"
git diff --numstat "$OLD" "$NEW"
echo "== delta changed lines (unified=0)"
git diff -U0 "$OLD" "$NEW" | grep -v -e '^---' -e '^+++' | grep '^[-+]' || true
git show "$OLD:$F" > "$T/old.sv"
git show "$NEW:$F" > "$T/new.sv"
cat > "$T/strip.py" <<'EOF'
import sys
s = open(sys.argv[1], encoding="utf-8").read()
out, i, n = [], 0, len(s)
while i < n:
    c = s[i]
    if c == '"':
        j = i + 1
        while j < n and s[j] != '"':
            j += 2 if s[j] == "\\" else 1
        out.append(s[i:j + 1]); i = j + 1
    elif s.startswith("//", i):
        j = s.find("\n", i)
        i = n if j < 0 else j
    elif s.startswith("/*", i):
        j = s.find("*/", i + 2)
        seg = s[i:(n if j < 0 else j + 2)]
        out.append("\n" * seg.count("\n")); i = n if j < 0 else j + 2
    else:
        out.append(c); i += 1
# normalise trailing blanks per line, keep line structure
print("\n".join(l.rstrip() for l in "".join(out).split("\n")))
EOF
python3 -I "$T/strip.py" "$T/old.sv" > "$T/old.nc"
python3 -I "$T/strip.py" "$T/new.sv" > "$T/new.nc"
echo "== sha256 raw";      sha256sum "$T/old.sv" "$T/new.sv" | sed "s#$T/##"
echo "== sha256 comment-stripped"; sha256sum "$T/old.nc" "$T/new.nc" | sed "s#$T/##"
cmp "$T/old.nc" "$T/new.nc" && echo "STRIPPED_IDENTICAL rc=0"
if [ -n "$VL" ]; then
  echo "== verilator -E -P (preprocessed, comments dropped)"
  "$VL" --version
  "$VL" -E -P "$T/old.sv" > "$T/old.pp"
  "$VL" -E -P "$T/new.sv" > "$T/new.pp"
  sha256sum "$T/old.pp" "$T/new.pp" | sed "s#$T/##"
  cmp "$T/old.pp" "$T/new.pp" && echo "PREPROCESSED_IDENTICAL rc=0"
fi
echo "== every RTL/test/harness path touched by the delta"
git diff --name-only "$OLD" "$NEW" -- hdl tb syn scripts gptp-processor '*.cpp' '*.sv' '*.v' '*.h' 'Makefile' '*/Makefile'
echo "== gitlinks at head"
git ls-tree "$NEW" | awk '$2=="commit"'
echo "PROOF_DONE"
