#!/usr/bin/env bash
# assemble.sh: copy the final evidence for f3e902f2 into receipts/, host prefixes replaced (collect.py), files over
# 200 KB listed by bytes and sha256 instead, then regenerate receipts/INDEX.md from the files present.
set -u
H=f3e902f2a96bb27eac6ed7780c70905af34f389e
T=$(dirname "$(readlink -f "$0")")
R=$(readlink -f "$T/../..")
S=$VALIDATION_STORAGE/823-a753c
P=$S/placeholders.tsv
C="python3 $T/collect.py $P"
rm -rf "$R/gates/logs" "$R/gates/union" "$R/gates/killed-by-reboot" "$R/gates/litex-sim-logs" "$R/sweep" "$R/extra"
$C "$S/gates/final/logs" "$R/gates/logs" '*'
$C "$S/gates/final/union" "$R/gates/union" '*'
$C "$S/gates/killed-by-reboot/logs" "$R/gates/killed-by-reboot" '*'
$C "$S/gates/final/elaborate.elaborate-gates-1/runner_temp/litex-sim-logs" "$R/gates/litex-sim-logs" '*'
for k in 0 1 2 3; do
  $C "$S/sweep-final/shard-$k" "$R/sweep/shard-$k" 'spec.json' 'spec/*' 'logs/*.log' 'logs/preflight/*'
done
$C "$S/rerun2" "$R/sweep/rerun-uncontended" '*/*'
$C "$S/gates/run/logs" "$R/sweep/rerun-uncontended" 'extra.rr[1-4].*'
$C "$S/rerun" "$R/sweep/killed-by-reboot" '*/*' '*/*/*'
$C "$S/gates/run/logs" "$R/extra" 'extra.ctrl_nvm_selftest_final.*'
python3 "$T/verify_wf.py" "$H" "$S/gates/final" rtl/yosys-shards=4 > "$S/verify.md"
echo "verify_wf rc=$?" >> "$S/verify.md"
cp "$S/verify.md" "$R/gates/verify.md"
cp "$S/sweep-spec-final.json" "$R/sweep/sweep-spec-final.json"
python3 "$T/sanitize.py" "$P" "$R/gates/verify.md" "$R/sweep/sweep-spec-final.json"
tail -n 2 "$R/gates/verify.md"
python3 "$T/make_index.py" "$R"
