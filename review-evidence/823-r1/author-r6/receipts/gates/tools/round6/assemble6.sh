#!/usr/bin/env bash
# assemble6.sh <receipts dir>: copy this round's evidence for 2905c874 into receipts/, host prefixes replaced
# (collect.py), files over 200 KB listed by bytes and sha256 instead, then INDEX.md from the files present.
set -u
H=2905c8749a4573450b9999dd546bb20ae5c7fc38; H1=e0adcc090b0c636044fa953901009c301ba6d080
S=<scratch>; T=$S/gates/tools; R=$1; P=$S/placeholders.tsv; C="python3 $T/collect.py $P"
rm -rf "$R"; mkdir -p "$R"
# the final head's job logs: each job from the one root where it ran to its end at the head (JOBS.tsv)
M=$S/gates/merged; rm -rf "$M"; mkdir -p "$M/logs"
: > "$S/JOBS.tsv"
for root in final5 final4 final3 final2; do
  for done in "$S/gates/$root/logs/"*__DONE; do
    [ -f "$done" ] || continue
    job=$(basename "$done" __DONE)
    grep -q "^$job	" "$S/JOBS.tsv" && continue
    head -n1 "$S/gates/$root/logs/${job}__"*.log 2>/dev/null | grep -q "$H" || continue
    printf '%s\t%s\t%s\n' "$job" "$root" "$(cat "$done")" >> "$S/JOBS.tsv"
    cp "$S/gates/$root/logs/${job}__"* "$M/logs/"
  done
done
sort -o "$S/JOBS.tsv" "$S/JOBS.tsv"
$C "$M/logs" "$R/gates/logs" '*'
cp "$S/JOBS.tsv" "$R/gates/JOBS.tsv"
python3 "$T/verify_final.py" "$H" "$M" "$H1" "$S/gates/final" "$T/carried.json" rtl/yosys-shards=4 > "$S/verify.md"
echo "verify_final rc=$?" >> "$S/verify.md"
cp "$S/verify.md" "$R/gates/verify.md"
mkdir -p "$R/gates/carried-e0adcc09"
$C "$S/gates/final/logs" "$R/gates/carried-e0adcc09" 'rtl-fast.firmware-unit__*'
$C "$S/gates/final4/elaborate.elaborate-gates-1/runner_temp/litex-sim-logs" "$R/gates/litex-sim-logs" '*'
$C "$S/gates/union" "$R/gates/union" '*'
$C "$T" "$R/gates/tools" '*.py' '*.sh' '*.txt' '*.json'
$C "$S/tools" "$R/gates/tools/round6" '*.py' '*.sh'
$C "$S" "$R/gates/drivers" 'drive*.log' '*waiter*.log'
for k in 0 1 2 3; do $C "$S/sweep2/shard-$k" "$R/sweep/shard-$k" 'spec.json' 'spec/*' 'logs/*.log' 'logs/preflight/*'; done
$C "$S" "$R/sweep/rerun-uncontended" 'sweep2-rerun.log' 'sweep2-rerun/*'
cp "$S/sweep-spec.json" "$R/sweep/sweep-spec.json"
$C "$S/gates/run/logs" "$R/extra" 'extra.drift_gate_final.*' 'extra.diff_check_final.*' 'extra.ctrl_nvm_selftest_final.*'
$C "$S/waiver" "$R/waiver" '*'
for d in base-ax7101 head-ax7101 final-ax7101 base-arty head-arty; do
  $C "$S/elab/$d" "$R/waiver/elab/$d" 'argv.txt' 'elab.rc' 'gateware.sha256' 'tree-after.txt' 'elab.log' 'dry-run.log'
done
$C "$S/elab" "$R/waiver/elab" '*.norm' '*.stamp' 'ax7101.gateware.diff'
for t in base final; do sha256sum "$S/elab/$t.v.code" "$S/elab/$t.v.tree.sorted"; done | sed "s#$S#<scratch>#" > "$R/waiver/elab/normalised.sha256"
$C "$S/first-attempt" "$R/superseded/e0adcc09" '*'
$C "$S/restart-attempt" "$R/superseded/after-restart" '*'
$C "$S/gates/final/logs" "$R/superseded/e0adcc09" 'rtl-fast.firmware-boundary__*' 'elaborate.elaborate-gates-1__*'
python3 "$T/sanitize.py" "$P" "$R/gates/verify.md" "$R/sweep/sweep-spec.json" "$R/gates/JOBS.tsv"
tail -n 2 "$R/gates/verify.md"
