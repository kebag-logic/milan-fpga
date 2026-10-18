#!/usr/bin/env bash
# usage: gates.sh <tree> <label>  -- the processor gates, one log + rc per gate (round 2)
tree=$1; label=$2
out=<data>/tmp/pp181-a635/r2/logs/$label
mkdir -p "$out"
. <data>/tmp/pp181-a635/env.sh
cd "$tree" || exit 9
{
  echo "tree $tree"; echo "head $(git rev-parse HEAD)"; date -u +%FT%TZ
  verilator --version; sv2v --version; yosys -V; python3 --version
} > "$out/env.txt" 2>&1
run() {
  local name=$1; shift
  local t0=$SECONDS rc=0
  "$@" > "$out/$name.log" 2>&1 || rc=$?
  echo "$name rc=$rc ($((SECONDS - t0))s)" >> "$out/rc.txt"
}
: > "$out/rc.txt"
rm -f "$out/req-tags.txt"
run run_suites env REQ_TAG_LOG="$out/req-tags.txt" ./scripts/run_suites.sh
run req_tags_executed python3 scripts/check-req-tags.py --suites "$out/run_suites.log" --evidence "$out/req-tags.txt"
run lint_hdl ./scripts/lint_hdl.sh
run make_check make check
run gen_matrix python3 scripts/gen_matrix.py --check
run yosys_run ./syn/yosys/run.sh
run elab_guards_yosys python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
echo "status-after $(git status --short | tr '\n' ';')" >> "$out/rc.txt"
echo DONE >> "$out/rc.txt"
