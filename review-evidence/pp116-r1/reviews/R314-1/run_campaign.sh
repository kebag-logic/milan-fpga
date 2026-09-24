#!/usr/bin/env bash
# Run one of the three processor mutation campaigns touched by PR #117 from an
# exported processor tree, unmodified, and record its stdout, exit status and
# wall time. Usage:
#   run_campaign.sh <processor-tree> <label> <desc|gsi|srp> <outdir>
# VERILATOR/PATH must already select the intended Verilator.
set -u
tree=$1; label=$2; which=$3; out=$4
dir="$out/$label-$which"
rm -rf "$dir"; mkdir -p "$dir"
cd "$tree" || exit 2
case "$which" in
  desc) cmd=(python3 -I tb/desc_mem_guard/mutate.py --output "$dir/logs") ;;
  gsi)  cmd=(python3 -I tb/pp_top/gsi_mutants.py --output "$dir/logs" --verilator "$(command -v verilator)") ;;
  srp)  cmd=(python3 -I tb/srp_admission/mutants.py --output "$dir/logs") ;;
  *) echo "unknown campaign $which"; exit 2 ;;
esac
start=$(date +%s)
"${cmd[@]}" > "$dir/stdout.txt" 2>&1
rc=$?
end=$(date +%s)
{
  echo "tree $tree"
  echo "verilator $(verilator --version)"
  echo "command ${cmd[*]}"
  echo "exit $rc"
  echo "wall_s $((end - start))"
} > "$dir/status.txt"
cat "$dir/status.txt"; tail -n 20 "$dir/stdout.txt"
