#!/bin/bash
# usage: commentonly.sh <clone> <base> <head> <verilator>: compare comment-free forms.
set -u
R=$1; B=$2; H=$3; V=$4; W=$(mktemp -d -p "$5")
cd "$R"
echo "hdl paths differing:"; git diff --name-only "$B" "$H" -- hdl gptp-processor protocol-processor third_party/verilog-axis constraints syn sw/builder/endstation_builder.py sw/litex/gen_mac_tx_model.py | sed 's/^/  /'
for f in $(git diff --name-only "$B" "$H" -- hdl); do
  n=$(basename "$f"); git show "$B:$f" > "$W/b_$n"; git show "$H:$f" > "$W/h_$n"
  for t in b h; do "$V" -E -P "$W/${t}_$n" 2>/dev/null | grep -v '^\s*$' > "$W/${t}_$n.E"; done
  echo "$n verilator -E -P: $(sha256sum < "$W/b_$n.E" | cut -c1-16) $(sha256sum < "$W/h_$n.E" | cut -c1-16) lines $(wc -l < "$W/h_$n.E") $(cmp -s "$W/b_$n.E" "$W/h_$n.E" && echo IDENTICAL || echo DIFFERS)"
done
for c in "$B" "$H"; do git show "$c:sw/litex/milan_soc.py" > "$W/soc_$c.py"; done
python3 -I - "$W/soc_$B.py" "$W/soc_$H.py" <<'PY'
import ast,hashlib,sys
d=[ast.dump(ast.parse(open(p).read()),include_attributes=False) for p in sys.argv[1:]]
print("milan_soc.py AST:",hashlib.sha256(d[0].encode()).hexdigest()[:16],hashlib.sha256(d[1].encode()).hexdigest()[:16],"IDENTICAL" if d[0]==d[1] else "DIFFERS")
PY
echo "non-comment changed lines in the two hdl files (should be none):"
git diff -U0 "$B" "$H" -- hdl | grep -E '^[-+]' | grep -vE '^(\+\+\+|---)' | grep -vE '^[-+]\s*//' | grep -vE '^[-+]\s{10,}[`a-z]' || echo "  none outside the banner/comment text"
