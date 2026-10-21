#!/usr/bin/env bash
# usage: run_gates.sh <processor tree> <log dir> [gate ...]
# Every processor gate in sequence (or the ones named); each gets <name>.log,
# <name>.rc, <name>.sec.
set -u
tree=$1; out=$2; shift 2
want=" ${*:-lint_hdl gen_matrix make_check yosys_run elab_guards_yosys run_suites req_tags_executed} "
mkdir -p "$out"
. <scratch>/scripts/env.sh
cd "$tree" || exit 2
gate() {
  local name=$1; shift
  case "$want" in *" $name "*) ;; *) return 0 ;; esac
  local t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  echo $(( $(date +%s) - t0 )) > "$out/$name.sec"
}
{ verilator --version; sv2v --version; yosys -V; python3 -c 'import wavedrom' && echo wavedrom-ok; mmdc --version; git rev-parse HEAD; git status --porcelain; } > "$out/tools.txt" 2>&1
gate lint_hdl ./scripts/lint_hdl.sh
gate gen_matrix python3 scripts/gen_matrix.py --check
gate make_check make check
gate yosys_run ./syn/yosys/run.sh
gate elab_guards_yosys python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 2
case "$want" in *" run_suites "*) rm -f "$out/req-tags.txt" ;; esac
gate run_suites env REQ_TAG_LOG="$out/req-tags.txt" ./scripts/run_suites.sh
gate req_tags_executed python3 scripts/check-req-tags.py --suites "$out/run_suites.log" --evidence "$out/req-tags.txt"
echo done > "$out/ALL.done"
