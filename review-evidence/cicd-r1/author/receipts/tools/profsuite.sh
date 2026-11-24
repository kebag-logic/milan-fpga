#!/bin/bash
# profsuite.sh SUITE CPUS: whole-suite perf record (children followed) in the base worktree, then
# attribution by command and by symbol. Output: runs/prof/SUITE.{data,comm.txt,sym.txt,log,time}
set -u
S=$1; C=$2
T=/data-2/milan/tmp/cicd-a839/wt/base
O=/data-2/milan/tmp/cicd-a839/runs/prof
. /data-2/milan/tmp/cicd-a839/bin/env.sh
export CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4
export MAKEFLAGS='-j1 --no-print-directory'
mkdir -p "$O"; cd "$T" || exit 99
if [[ "$S" == *__* ]]; then cmd=(python3 scripts/ci_suite_pieces.py run "$S" --receipts "$O/$S.cases")
else cmd=(make -C "tb/verilator/$S"); fi
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$S.time" \
  perf record -m 4 -F 49 -e cycles:u --user-callchains --call-graph fp -o "$O/$S.data" -- "${cmd[@]}" > "$O/$S.log" 2>&1
perf report -i "$O/$S.data" --stdio --no-children --sort comm 2>/dev/null | grep -E '^ +[0-9]' | head -15 > "$O/$S.comm.txt"
perf report -i "$O/$S.data" --stdio --no-children --sort comm,symbol 2>/dev/null | grep -E '^ +[0-9]' | head -25 > "$O/$S.sym.txt"
echo "$S $(head -1 "$O/$S.time") verdict: $(python3 scripts/suite_tally.py --verdict "$O/$S.log" >/dev/null 2>&1; echo $?)"
