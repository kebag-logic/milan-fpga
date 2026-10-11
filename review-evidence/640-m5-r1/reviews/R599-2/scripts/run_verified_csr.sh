#!/usr/bin/env bash
# Run from the packet directory. Usage: bash scripts/run_verified_csr.sh REPO VERILATOR
# REPO must be the isolated checkout; VERILATOR must identify release 5.050.
set -euo pipefail
repo=$(realpath "$1")
verilator=$(realpath "$2")
packet=$(pwd)
scratch="$packet/scratch/verified-head"
mkdir -p "$packet/scratch/tmp"
"$verilator" --version
"$verilator" --version | grep -F 'Verilator 5.050 '
sha256sum "$verilator"
git clone --quiet --shared --no-checkout "$repo" "$scratch"
git -C "$scratch" checkout --quiet --detach c0cba330fd485e52fcb90d5ccc69169edf9f0c2b
git -C "$scratch" submodule init -- protocol-processor gptp-processor third_party/verilog-axis
for sub in protocol-processor gptp-processor third_party/verilog-axis; do
  git -C "$scratch" -c protocol.file.allow=always \
    -c "submodule.$sub.url=$repo/$sub" submodule update --init -- "$sub"
done
git -C "$scratch" submodule status
git -C "$scratch" rev-parse HEAD 'HEAD^{tree}'
export TMPDIR="$packet/scratch/tmp"
export VERILATOR="$verilator"
export MAKEFLAGS=w
# Seven independent suite builds, at most two compiler jobs each (14 total).
# The campaign has no --jobs option; its seven mutations build sequentially.
set +e
make -j16 --jobserver-style=pipe -C "$scratch/tb/verilator/csr" \
  VERILATOR="$verilator" \
  VFLAGS='--cc --exe --build -j 2 +incdir+../../../hdl/common/csr -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -Wall -Wextra"'
result=$?
printf '%s\n' "$result" > "$packet/scratch/verified-csr.rc"
exit "$result"
