#!/usr/bin/env bash
# Rebuild obj_crflic at the exact head in a disposable clone and run it, then
# plant the pre-#530 gate (lwsrp_stream_gate <- raw admission verdict) and run
# it again. usage: run_crflic_probe.sh <review-clone> <scratch-dir> <verilator>
set -eu
R=${1:?review clone}; S=${2:?scratch dir}; V=${3:?verilator}
HEAD_=8ffd6c616840b161891e2eb714a7ddbbb72c7a0d
W=$S/wt
rm -rf "$W"
git clone -q --no-checkout "$R" "$W"
git -C "$W" checkout -q --detach $HEAD_
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  pin=$(git -C "$R" ls-tree $HEAD_ "$s" | awk '{print $3}')
  rmdir "$W/$s" 2>/dev/null || true
  git clone -q --no-checkout "$(git -C "$R/$s" rev-parse --absolute-git-dir)" "$W/$s"
  git -C "$W/$s" checkout -q --detach "$pin"
done
git -C "$W" submodule init protocol-processor gptp-processor third_party/verilog-axis
"$V" --version
cd "$W/tb/verilator/milan_dp"
set +e
make crflic VERILATOR="$V" VERILATOR_JOBS=8; echo "clean rc=$?"
sed -i 's/^  assign lwsrp_stream_gate = pp_cd_srp_active_w\[SRP_TALKERS_C-1:0\];/  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];/' \
  "$W/hdl/milan/milan_datapath.sv"
git -C "$W" diff --stat
make crflic VERILATOR="$V" VERILATOR_JOBS=8; echo "mutant rc=$? (expected nonzero)"
git -C "$W" checkout -q -- hdl/milan/milan_datapath.sv
