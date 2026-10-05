#!/bin/sh
# Delta-round identity check for PR #159 at 356c1bba against bed5f477.
# Usage: delta_identity.sh <clone> <outdir>   (needs git, sv2v; VERILATOR optional)
set -eu
REPO=$1; OUT=$2
OLD=bed5f47785839800bb640d7c747f5435f84ab5a3
NEW=356c1bbad2e9838659b433736040acf0cc4abf3e
F=hdl/aecp/KL_aecp_notify.sv
mkdir -p "$OUT/old" "$OUT/new"
cd "$REPO"
echo "== files changed $OLD..$NEW"
git diff --name-status "$OLD" "$NEW"
echo "== whitespace check"
git diff --check "$OLD" "$NEW" && echo "diff --check clean"
echo "== changed lines that are not // comments"
git diff -U0 "$OLD" "$NEW" -- "$F" | grep -E '^[+-][^+-]' | grep -vE '^[+-][[:space:]]*//' || echo "none"
for r in old new; do
  [ $r = old ] && c=$OLD || c=$NEW
  git show "$c:hdl/common/pp_pkg.sv" > "$OUT/$r/pp_pkg.sv"
  git show "$c:$F" > "$OUT/$r/KL_aecp_notify.sv"
  # strip // comments and trailing blanks; compare code token stream
  sed -e 's://.*$::' -e 's/[[:space:]]*$//' "$OUT/$r/KL_aecp_notify.sv" | grep -v '^$' > "$OUT/$r/code.txt"
  (cd "$OUT/$r" && sv2v pp_pkg.sv KL_aecp_notify.sv > notify.v)
  if [ -n "${VERILATOR:-}" ]; then
    (cd "$OUT/$r" && "$VERILATOR" -E -P pp_pkg.sv KL_aecp_notify.sv > vpp.txt)
  fi
done
echo "== comment-stripped source"
cmp "$OUT/old/code.txt" "$OUT/new/code.txt" && echo "CODE_IDENTICAL"
echo "== sv2v $(sv2v --version)"
sha256sum "$OUT/old/notify.v" "$OUT/new/notify.v"
cmp "$OUT/old/notify.v" "$OUT/new/notify.v" && echo "SV2V_BYTE_IDENTICAL"
if [ -n "${VERILATOR:-}" ]; then
  echo "== verilator -E -P ($("$VERILATOR" --version))"
  sha256sum "$OUT/old/vpp.txt" "$OUT/new/vpp.txt"
  cmp "$OUT/old/vpp.txt" "$OUT/new/vpp.txt" && echo "VPP_BYTE_IDENTICAL"
fi
