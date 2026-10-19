#!/usr/bin/env bash
# usage: run_gates.sh <processor tree> <log dir>
# Runs every processor gate in sequence; each gets <name>.log, <name>.rc, <name>.sec.
set -u
tree=$1; out=$2
mkdir -p "$out"
. <scratch>/scripts/env.sh
cd "$tree" || exit 2
gate() {
  local name=$1; shift
  local t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  echo $(( $(date +%s) - t0 )) > "$out/$name.sec"
}
{ verilator --version; sv2v --version; yosys -V; python3 -c 'import wavedrom' && echo wavedrom-ok; mmdc --version; git rev-parse HEAD; } > "$out/tools.txt" 2>&1
gate lint_hdl ./scripts/lint_hdl.sh
gate gen_matrix python3 scripts/gen_matrix.py --check
gate make_check make check
gate yosys_run ./syn/yosys/run.sh
gate elab_guards_yosys python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4
rm -f "$out/req-tags.txt"
gate run_suites env REQ_TAG_LOG="$out/req-tags.txt" ./scripts/run_suites.sh
gate req_tags_executed python3 scripts/check-req-tags.py --suites "$out/run_suites.log" --evidence "$out/req-tags.txt"
echo done > "$out/ALL.done"
