#!/usr/bin/env bash
# early.sh <head>: the firmware boundary's Verilator half on a clean clone, ahead of the final gate pass (#870 round 2)
set -uo pipefail
H=$1; S=<scratch>; G=$S/gates
LITEX=<home>/litex-milan/venv/bin; V=<tools>/pinned-verilator-5.050
SDK=<round1-scratch><home-path>/host/bin
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export PATH=$LITEX:$V:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:$SDK
D=$G/early; rm -rf "$D"; bash $S/tools/clone.sh "$D" "$H" > "$G/early-clone.log" 2>&1 || exit 3
(cd "$D" && python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator) > "$G/early-boundary-verilator.log" 2>&1
echo "rc=$?" >> "$G/early-boundary-verilator.log"; echo "$(date +%T) early-boundary-verilator $(tail -n1 $G/early-boundary-verilator.log)"
