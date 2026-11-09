#!/usr/bin/env bash
# assemble.sh <out receipts dir>: copy the final evidence for 30ca4b21 into receipts/, host prefixes replaced
# (collect.py), files over 200 KB listed by bytes and sha256 instead, then regenerate INDEX.md from the files present.
set -u
H=30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14
T=$(dirname "$(readlink -f "$0")")
R=$1
S=<scratch>
P=$S/placeholders.tsv
C="python3 $T/collect.py $P"
rm -rf "$R/gates" "$R/sweep" "$R/extra" "$R/pre-commit" "$R/first-run-8c66ab1e"
$C "$S/gates/final/logs" "$R/gates/logs" '*'
$C "$S/gates/final/elaborate.elaborate-gates-1/runner_temp/litex-sim-logs" "$R/gates/litex-sim-logs" '*'
$C "$T" "$R/gates/tools" '*'
$C "$S/gates/final/union" "$R/gates/union" '*'
$C "$S" "$R/gates/drivers" 'drive-*.log' 'waiter.log'
$C "$S/tools" "$R/gates/tools/round4" '*.py' '*.sh'
for k in 0 1 2 3; do
  $C "$S/sweep/shard-$k" "$R/sweep/shard-$k" 'spec.json' 'spec/*' 'logs/*.log' 'logs/preflight/*'
done
[ -d "$S/rerun" ] && $C "$S/rerun" "$R/sweep/rerun-uncontended" '*' '*/*'
$C "$S/gates/run/logs" "$R/extra" 'extra.*'
$C "$S" "$R/pre-commit" 'grade1.log' 'f1-1x1.log' 'test_ctrl_memory_fix.log' 'probes/*'
$C "$S/first-run-8c66ab1e/final/logs" "$R/first-run-8c66ab1e/gates-logs" '*elaborate-gates-1__gate_19*'
$C "$S/first-run-8c66ab1e/final/elaborate.elaborate-gates-1/runner_temp/litex-sim-logs" "$R/first-run-8c66ab1e/litex-sim-logs" 'test_ctrl_memory.log'
$C "$S/first-run-8c66ab1e" "$R/first-run-8c66ab1e" 'drive-*.log'
python3 "$T/verify_wf.py" "$H" "$S/gates/final" rtl/yosys-shards=4 > "$S/verify.md"
echo "verify_wf rc=$?" >> "$S/verify.md"
cp "$S/verify.md" "$R/gates/verify.md"
cp "$S/sweep-spec.json" "$R/sweep/sweep-spec.json"
python3 "$T/sanitize.py" "$P" "$R/gates/verify.md" "$R/sweep/sweep-spec.json"
tail -n 2 "$R/gates/verify.md"
python3 "$T/make_index.py" "$R"
