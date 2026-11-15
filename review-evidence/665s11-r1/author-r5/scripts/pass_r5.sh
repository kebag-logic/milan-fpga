#!/bin/bash
# pass_r5.sh HEAD: round 5's final pass on clean clones of HEAD, each unit on its own 8-wide range as one frees
# (cpu_ranges.py pick; nothing booked while waiting): the four sweep shards, every hosted job step of rtl-fast, rtl,
# elaborate and docs (run_wf.py through drive.sh, each job on its own clone), and the lane's gates no workflow runs
# (lane_gates_r5.sh). Logs to r5/pass/dispatch.log.
set -u
H=$1
T=<scratch> R=${PASS_ROOT:-$T/r5/pass} X=$T/r5/scripts D=$T/gates/tools/drive.sh
PICK="python3 -I <management>/2026-09-23/cpu_ranges.py pick"
mkdir -p $R/wf $R/sweep
L=$R/dispatch.log
echo "$(date +%T) pass at $H" >> $L
cat > $R/sweep/full-native.json <<JSON
{
 "cwd": "<lane>",
 "head": "$H",
 "base": "1d6bf5556a",
 "commands": [["env", "PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<shared-scratch>/a662/make43/bin:<home-local>/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin", "VERILATOR=<tools>/pinned-verilator-5.050/verilator", "TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c", "TMPDIR=$T/r5/pass/sweep-tmp", "MAKEFLAGS=-j4 --no-print-directory", "bash", "scripts/run_all_suites.sh", "$T/r5/pass/sweep/logs", "--wait"]]
}
JSON
mkdir -p $T/r5/pass/sweep-tmp
job() {   # name: the command it runs
  case $1 in
    S0|S1|S2|S3) echo "python3 -I $X/sweep_shard.py 665s11-a761c-r5sx $R/sweep/full-native.json $R/sweep/out ${1#S} 4";;
    WC1) echo "bash $D $H $R/wf C1 elaborate:elaborate-gates-1 elaborate:elaborate-gates-0 elaborate:elaborate";;
    WA) echo "bash $D $H $R/wf A rtl-fast:firmware-boundary rtl-fast:firmware-unit rtl-fast:firmware-control-mutants rtl-fast:firmware-aecp-mutants rtl-fast:firmware-srp-mutants rtl-fast:firmware-verilator";;
    WC2) echo "bash $D $H $R/wf C2 rtl:full-ci-gate rtl:yosys-shards:0/4 rtl:yosys-shards:1/4 rtl:yosys-shards:2/4 rtl:yosys-shards:3/4 rtl:yosys-portability rtl:yosys-tool";;
    WB) echo "bash $D $H $R/wf B rtl-fast:changes rtl-fast:verilator-lint rtl-fast:bdd-conformance rtl-fast:yosys-tool rtl-fast:yosys-elaboration rtl-fast:split-cdc rtl-fast:publication-census rtl-fast:rtl-fast";;
    WD) echo "bash $D $H $R/wf D docs:wire-accountability docs:docs-check-no-git docs:docs-gates-0 docs:docs-gates-1 docs:docs-gates-2 docs:docs-check";;
    PS1) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H sims1";;
    WA2) echo "bash $D $H $R/wf A2 rtl-fast:firmware-boundary rtl-fast:firmware-verilator";;
    PR) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H reboot";;
    WA3) echo "bash $D $H $R/wf A3 rtl-fast:firmware-aecp-mutants";;
    PF) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H final";;
    PS2) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H sims2";;
    PB) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H build";;
    PN) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H nvm";;
    PM) echo "env PASS_ROOT=$R bash $X/lane_gates_r5.sh $H model";;
  esac
}
pending="${PASS_JOBS:-S0 S1 S2 S3 WC1 WA PS2 PS1 WC2 PB WB PN PM WD}"
while [ -n "$pending" ]; do
  next=""
  for n in $pending; do
    p=$($PICK)
    if [ -z "$p" ]; then next="$next $n"; continue; fi
    case $n in
      S?) $(job $n) $p >> $L 2>&1 && echo "$(date +%T) $n on $p" >> $L || { echo "$(date +%T) $n FAILED to start" >> $L; };;
      *) bash $X/unit.sh ${UNIT_PREFIX:-P}-$n $p $(job $n) >> $L 2>&1 && echo "$(date +%T) $n on $p" >> $L;;
    esac
    sleep 5
  done
  pending=$(echo $next)
  [ -n "$pending" ] && sleep 60
done
echo "$(date +%T) all launched" >> $L
