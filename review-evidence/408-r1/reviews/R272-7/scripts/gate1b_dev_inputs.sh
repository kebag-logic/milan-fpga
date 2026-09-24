#!/usr/bin/env bash
# List the dev-side changes that gate 1b reads on a composed candidate: the
# milan_dp RTL closure it elaborates mutants against (make print-srcs), the
# datapath, Makefile and product YAMLs, and confirm the firmware and the rest
# of sw/builder are unchanged on the dev side.
# Usage: gate1b_dev_inputs.sh <clone> <merge-base> <dev>
set -u
clone=$1 mb=$2 dev=$3
cd "$clone/tb/verilator/milan_dp" || exit 2
srcs=$(make -s print-srcs)
cd "$clone" || exit 2
echo "# gate 1b RTL-mutant closure (tb/verilator/milan_dp make print-srcs) intersected with dev-side changes $mb..$dev"
for s in $srcs; do
    p=$(realpath --relative-to=. "tb/verilator/milan_dp/$s")
    git diff --quiet "$mb" "$dev" -- "$p" || echo "dev-changed, read by gate 1b: $p"
done
echo "total closure files: $(echo $srcs | wc -w)"
for p in hdl/milan/milan_datapath.sv tb/verilator/milan_dp/Makefile \
         configs/endstation_arty_4x4.yaml configs/endstation_arty_8ch.yaml \
         configs/endstation_ax7101_8x8.yaml; do
    echo "gate-1b input $p dev delta: $(git diff --shortstat "$mb" "$dev" -- "$p")"
done
echo "sw/firmware/milan_baremetal dev delta: '$(git diff --shortstat "$mb" "$dev" -- sw/firmware/milan_baremetal)'"
echo "sw/builder (other than test_builder.py) dev delta: '$(git diff --shortstat "$mb" "$dev" -- sw/builder)'"
