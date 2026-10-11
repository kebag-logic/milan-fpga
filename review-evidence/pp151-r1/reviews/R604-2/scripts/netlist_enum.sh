#!/usr/bin/env bash
# Second netlist comparison: names made independent of source lines before writing.
# usage: netlist_enum.sh OUTDIR BINDIR JOBS TOP...   (OUTDIR from netlist_identity.sh)
# Every wire or cell whose name embeds the lowered file's location is hidden, then
# every private name is enumerated in creation order (`rename -enumerate`), so a
# moved source line cannot rename anything. Exit 0 = every TOP's netlist is identical.
set -uo pipefail
out=$1 bindir=$2 jobs=$3; shift 3
export PATH="$bindir:$PATH"
one() {
  local side=$1 t=$2 w=$out/$1
  ( cd "$w" && yosys -q -p "read_verilog -defer all.v; hierarchy -check -top $t; proc; opt_clean; rename -hide w:*all.v* c:*all.v*; rename -enumerate; write_verilog -noattr $t.enum.v" > "$t.enum.log" 2>&1; echo $? > "$t.enum.rc" )
}
export -f one; export out
for t in "$@"; do printf '%s %s\n' base "$t" head "$t"; done | xargs -P "$jobs" -n 2 bash -c 'one "$0" "$1"'
rc=0
for t in "$@"; do
  b=$(cat "$out/base/$t.enum.rc") h=$(cat "$out/head/$t.enum.rc")
  if [ "$b" != 0 ] || [ "$h" != 0 ]; then echo "ELAB FAIL $t base rc=$b head rc=$h"; rc=1; continue; fi
  sb=$(sha256sum < "$out/base/$t.enum.v" | cut -c1-64) sh=$(sha256sum < "$out/head/$t.enum.v" | cut -c1-64)
  n=$(grep -c . "$out/head/$t.enum.v")
  if [ "$sb" = "$sh" ]; then echo "IDENTICAL $t $sb ($n lines)"; else echo "DIFFERS  $t base $sb head $sh"; rc=1; fi
done
exit $rc
