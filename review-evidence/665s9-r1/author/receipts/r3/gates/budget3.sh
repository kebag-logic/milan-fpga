head a2690e682d929e6d3811006f961a24361827c596
command: the script, as run
full log: 1002 bytes, sha256 22879645615dd8a4e4598c3745ef796563f21a288c0fba7be88b7d78c9b51bb7
---
#!/usr/bin/env bash
# budget3.sh <head> <point>: S2's harness at one point on its own fresh clone of <head> (gates.sh's budget leg, one point)
set -uo pipefail
H=$1; P=$2
S=<scratch>; G=$S/gates
LITEX=<home>/litex-milan/venv/bin
V=<tools>/pinned-verilator-5.050
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export PATH=$V:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c
SDK=$HOME/br-milan-rv32/host/bin
D=$G/budget-$P; rm -rf "$D" "$S/tmp/budget-$P"; bash $S/tools/clone.sh "$D" "$H" > "$G/budget-$P-clone.log" 2>&1 || exit 3
(cd "$D" && PATH=$LITEX:$PATH:$SDK python3 -B tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $S/tmp/budget-$P --record-budget-findings) > "$G/budget-$P.log" 2>&1
echo "rc=$?" >> "$G/budget-$P.log"; echo "$(date +%T) budget-$P $(tail -n 1 $G/budget-$P.log)"
