#!/usr/bin/env bash
# reviewer_arms.sh <packet-root> <tree> <out>: run every arm of both reviews against tb/srp_encoder, in a copy of its
# own per arm, ARM_JOBS at a time, default eight; prints one line per arm: arm, rc, tally, the distinct failing row tags
set -u
P=$1; T=$2; OUT=$3
mkdir -p "$OUT"
one() {
  kind=$1; arm=$2; w=$OUT/w/$kind-$arm; rm -rf "$w"; mkdir -p "$w/tb"
  cp -r "$T/hdl" "$w/hdl"; cp -r "$T/tb/common" "$w/tb/common"; mkdir "$w/tb/srp_encoder"
  cp "$T"/tb/srp_encoder/{Makefile,sim_main.cpp,srp_tb_wrap.sv} "$w/tb/srp_encoder/"
  if [ "$kind" = r780 ]; then python3 -I "$P/pp214-r780-1-packet/scripts/reviewer_mutants.py" "$w" "$arm"
  else
    python3 -I - "$P/pp214-r779-1-packet/scripts/probes.py" "$w" "$arm" <<'PY'
import re, sys
src = open(sys.argv[1]).read()
table = src[src.index("P = {"):src.index("def main")]
ns = {}
exec(table, ns)
a, b = ns["P"][sys.argv[3]]
p = sys.argv[2] + "/hdl/srp/KL_srp_encoder.sv"
s = open(p).read()
assert s.count(a) == 1, sys.argv[3]
open(p, "w").write(s.replace(a, b))
PY
  fi
  (cd "$w/tb/srp_encoder" && timeout 280 make MAKEFLAGS=-j2 > "$OUT/$kind-$arm.log" 2>&1); rc=$?
  t=$(grep -E '^[0-9]+ checks:' "$OUT/$kind-$arm.log" | tail -1)
  rows=$(grep '^FAIL' "$OUT/$kind-$arm.log" | sed 's/^FAIL: //' | cut -d: -f1 | sed -E 's/^(PV[0-9]+|[A-Z]+[0-9]+[a-z]?).*/\1/' | sort -u | tr '\n' ' ')
  printf '%s\t%s\trc=%s\t%s\t%s\n' "$kind" "$arm" "$rc" "${t:-NO TALLY}" "$rows"
  rm -rf "$w"
}
export -f one; export P T OUT
{
  python3 -I "$P/pp214-r780-1-packet/scripts/reviewer_mutants.py" | sed 's/^/r780 /'
  python3 -I - "$P/pp214-r779-1-packet/scripts/probes.py" <<'PY' | sed 's/^/r779 /'
import sys
src = open(sys.argv[1]).read()
ns = {}
exec(src[src.index("P = {"):src.index("def main")], ns)
print("\n".join(ns["P"]))
PY
} | xargs -P ${ARM_JOBS:-8} -L 1 bash -c 'one "$0" "$1"' | sort
