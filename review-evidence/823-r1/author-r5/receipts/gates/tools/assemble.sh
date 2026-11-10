#!/usr/bin/env bash
# assemble.sh <out receipts dir>: copy the final evidence for 7c97e99f (sweep on b6a60fbd) into receipts/, host prefixes replaced
# (collect.py), files over 200 KB listed by bytes and sha256 instead, then regenerate INDEX.md from the files present.
set -u
H=7c97e99f53ab0efc3e05e4617ee652dbab6e1b14
T=$(dirname "$(readlink -f "$0")")
R=$1
S=<scratch>
P=$S/placeholders.tsv
C="python3 $T/collect.py $P"
rm -rf "$R/gates" "$R/sweep" "$R/extra" "$R/memory" "$R/superseded-system-cc" "$R/first-run-b6a60fbd" "$R/second-run-d01c66ad" "$R/plant-grading" "$R/interrupted-poweroff"
$C "$S/gates/final/logs" "$R/gates/logs" '*'
$C "$S/gates/final/elaborate.elaborate-gates-1/runner_temp/litex-sim-logs" "$R/gates/litex-sim-logs" '*'
$C "$T" "$R/gates/tools" '*'
$C "$S/gates/final/union" "$R/gates/union" '*'
$C "$S" "$R/gates/drivers" 'drive-*.log' 'waiter.log'
$C "$S/tools" "$R/gates/tools/round5" '*.py' '*.sh'
for k in 0 1 2 3; do
  $C "$S/sweep/shard-$k" "$R/sweep/shard-$k" 'spec.json' 'spec/*' 'logs/*.log' 'logs/preflight/*'
done
[ -d "$S/rerun" ] && $C "$S/rerun" "$R/sweep/rerun" '*' '*/*'
$C "$S/gates/run/logs" "$R/extra" 'extra.*'
$C "$S/mem" "$R/memory" 'measure.sh' 'at-30ca4b21/*.log' 'at-7c97e99f/*.log'
$C "$S/gates/superseded-system-cc/logs" "$R/superseded-system-cc" '*'
$C "$S/gates/superseded-b6a60fbd/final/logs" "$R/first-run-b6a60fbd/gates-logs" '*'
$C "$S/gates/superseded-b6a60fbd" "$R/first-run-b6a60fbd" 'drive-*.log' 'waiter-*.log' 'run-logs/*'
$C "$S/gates/superseded-d01c66ad/final/logs" "$R/second-run-d01c66ad/gates-logs" '*'
$C "$S/gates/superseded-d01c66ad" "$R/second-run-d01c66ad" 'drive-*.log' 'waiter-*.log' 'run-logs/*'
$C "$S/gates/interrupted-0749/final-logs" "$R/interrupted-poweroff/gates-logs" '*'
$C "$S/gates/interrupted-0749" "$R/interrupted-poweroff" 'drive-*.log' 'run-logs/*'
for g in g1 g3 g4 g5; do $C "$S/$g" "$R/plant-grading/$g" 'grade.log' 'logs/*.log'; done
python3 "$T/verify_wf.py" "$H" "$S/gates/final" rtl/yosys-shards=4 > "$S/verify.md"
echo "verify_wf rc=$?" >> "$S/verify.md"
cp "$S/verify.md" "$R/gates/verify.md"
cp "$S/sweep-spec.json" "$R/sweep/sweep-spec.json"
python3 "$T/sanitize.py" "$P" "$R/gates/verify.md" "$R/sweep/sweep-spec.json"
tail -n 2 "$R/gates/verify.md"
python3 "$T/make_index.py" "$R"
