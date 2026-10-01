#!/usr/bin/env bash
# R410-3 probe: does tb/adp_engine's gate-enable-dropped patch (the arm whose
# record quotes a full default pp_top run) reach section AC at the merged
# head? Disposable clone; the patch is applied with git apply, the default
# build is made once, and the AC and AD sections run alone.
#   probe_adp_gate_vs_ac.sh HEAD_REPO VBIN OUT SCRATCH
set -uo pipefail
repo=$1; vbin=$2; out=$3; scratch=$4
export PATH="$vbin:$PATH"; mkdir -p "$out"
rm -rf "$scratch/probe-gate"
git clone -q --no-checkout "$repo" "$scratch/probe-gate" && cd "$scratch/probe-gate" || exit 2
git checkout -q --detach 4e558491c608dc88efc7963a77cb6b49bce2a46e
git apply tb/adp_engine/mutations/gate-enable-dropped.patch || exit 3
git diff --stat > "$out/gate-probe.diffstat"
cd tb/pp_top
taskset -c 0-7 make gsi-build VERILATOR="$vbin/verilator" > "$out/gate-probe-build.log" 2>&1 || { echo "build failed"; exit 4; }
for f in --acmp-only --adp-only; do
  rm -f obj_dir/build_tally.txt
  taskset -c 0-7 ./obj_dir/Vpp_top_sim "$f" > "$out/gate-probe$f.log" 2>&1
  echo "$f rc=$? $(tail -1 "$out/gate-probe$f.log")" | tee -a "$out/gate-probe-summary.txt"
done
