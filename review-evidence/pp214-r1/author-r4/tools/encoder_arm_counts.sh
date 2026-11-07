#!/usr/bin/env bash
# encoder_arm_counts.sh <tree> <out> [encoder.sv]: for every arm of tb/srp_top/mutants.py with an srp_encoder row, plant
# it in a copy of its own and run tb/srp_encoder, ARM_JOBS at a time, default eight; prints arm, rc, tally and the distinct failing rows
# with their counts. With no arm named BASE plants <encoder.sv> over the tree's encoder instead.
set -u
T=$1; OUT=$2; BASE=${3:-}
mkdir -p "$OUT"
one() {
  arm=$1; w=$OUT/w/$arm; rm -rf "$w"; mkdir -p "$w/tb"
  cp -r "$T/hdl" "$w/hdl"; cp -r "$T/tb/common" "$w/tb/common"; mkdir "$w/tb/srp_encoder"
  cp "$T"/tb/srp_encoder/{Makefile,sim_main.cpp,srp_tb_wrap.sv} "$w/tb/srp_encoder/"
  if [ "$arm" = BASE ]; then cp "$BASE" "$w/hdl/srp/KL_srp_encoder.sv"
  elif [ "$arm" != HEAD ]; then (cd "$w" && git apply "$T/tb/srp_top/mutations/$arm.patch") || { printf '%s\tPATCH FAILED\n' "$arm"; return; }; fi
  (cd "$w/tb/srp_encoder" && timeout 280 make MAKEFLAGS=-j2 > "$OUT/$arm.log" 2>&1); rc=$?
  t=$(grep -E '^[0-9]+ checks:' "$OUT/$arm.log" | tail -1)
  rows=$(grep '^FAIL' "$OUT/$arm.log" | sed 's/^FAIL: //' | cut -d: -f1 | sed -E 's/^(PV[0-9]+|[A-Z]+[0-9]+[a-z]?).*/\1/' | sort -V | uniq -c | awk '{printf "%s(%s) ", $2, $1}')
  printf '%s\trc=%s\t%s\t%s\n' "$arm" "$rc" "${t:-NO TALLY}" "$rows"
  rm -rf "$w"
}
export -f one; export T OUT BASE
{ echo HEAD; [ -n "$BASE" ] && echo BASE
  python3 -I -c "
import ast, sys
tree = ast.parse(open('$T/tb/srp_top/mutants.py').read())
for n in tree.body:
    if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'MUTANTS':
        rows = ast.literal_eval(n.value)
print('\n'.join(sorted({r[0] for r in rows if r[1] == 'srp_encoder'})))"
} | xargs -P ${ARM_JOBS:-8} -I{} bash -c 'one "$1"' _ {} | sort
