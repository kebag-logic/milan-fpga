#!/usr/bin/env bash
# proc-gates.sh <runs> <tree>: every processor gate the change touches, in order, in a clean clone at the head:
# the CI jobs' make check, lint, the suite sweep and its executed traceability half, the matrix check, the
# campaigns that read a changed file (every tb/pp_top driver, adp_engine, aecp_cmds, maap's pp_top arms) and the
# CI-listed SRP LeaveAll campaign, then the portability job (yosys run.sh + the yosys elaboration guards).
# Each gate keeps cmd/log/rc/start/end under <runs>; every gate runs whatever the previous one's rc.
R=$1; T=$2
. "$(dirname "$0")/common.sh"
CAP=$(cd "$(dirname "$0")" && pwd)/vl-cap
PD=$VD/bin:$SV:$VL:$BASE
PC=$CAP:$SV:$BASE
export HOME=$HOME TMPDIR=$S/tmp/proc-final2
mkdir -p "$R" "$TMPDIR"
gp() { n=$1; d=$2; shift 2; g "$R" "$T/$d" "$PD" "$n" "$@"; }
gc() { n=$1; d=$2; shift 2; g "$R" "$T/$d" "$PC" "$n" "$@"; }
gp make_check . make check
gp lint_hdl . bash scripts/lint_hdl.sh
gp gen_matrix_check . python3 scripts/gen_matrix.py --check
gp diff_check . git diff --check 044cb25f4ed2187bd238490650e73d5d189855d1 HEAD
# the sweep unpiped: its stdout is the gate's own log, which the traceability half reads
gp run_suites . env MAKEFLAGS=-j8 REQ_TAG_LOG="$R/req-tags.txt" bash scripts/run_suites.sh
gp check_req_tags_exec . python3 scripts/check-req-tags.py --suites "$R/run_suites.log" --evidence "$R/req-tags.txt"
gc aecp_dispatch_mutants tb/pp_top python3 aecp_dispatch_mutants.py --output "$R/aecp-dispatch-out" --verilator verilator --jobs 8
gc aecp_mutants tb/pp_top make aecp-mutants MUTANT_OUTPUT="$R/aecp-mutants-out" VERILATOR=verilator
gc aecp_cmds_mutants tb/aecp_cmds make mutants MUTANT_OUTPUT="$R/aecp-cmds-out" VERILATOR=verilator
gc adp_mutants tb/adp_engine python3 mutants.py --output "$R/adp-out" --jobs 8
gc ctr_mutants tb/pp_top make ctr-mutants CTR_MUTANT_OUTPUT="$R/ctr-out" VERILATOR=verilator
gc acmp_mutants tb/pp_top python3 acmp_mutants.py --output "$R/acmp-out" --verilator verilator --jobs 8
gc d3_mutants tb/pp_top python3 d3_mutants.py --output "$R/d3-out" --verilator verilator --jobs 8
gc gsi_mutants tb/pp_top python3 gsi_mutants.py --output "$R/gsi-out" --verilator verilator
gc notify_mutants tb/pp_top python3 notify_mutants.py --output "$R/notify-out" --verilator verilator --jobs 8
gc name_wr_mutant tb/pp_top python3 name_wr_mutant.py --output "$R/name-wr-out"
gc maap_mutants tb/maap make mutants MUTANT_OUTPUT="$R/maap-out"
gc srp_top_mutants tb/srp_top make mutants MUTANT_OUTPUT="$R/srp-top-out"
gp portability . bash -c "set -o pipefail; ./syn/yosys/run.sh > $R/yosys_run.log 2>&1; a=\$?; echo \$a > $R/yosys_run.rc; python3 -B tb/elab_guards/guards.py --frontend yosys --jobs 4 > $R/elab_guards_yosys.log 2>&1; b=\$?; echo \$b > $R/elab_guards_yosys.rc; exit \$((a|b))"
echo done > "$R/ALL.done"
