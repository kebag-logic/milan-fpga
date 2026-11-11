#!/usr/bin/env bash
# budget2-r1head.sh <head> <point>: S2s harness at round 1s head, for the per-probe values round 1 did not keep (comparison only)
# of <head>, budget findings recorded, not failed; 1x1 also runs the harness's self-test first. Log gates/budget-<point>.log.
set -uo pipefail
H=$1; P=$2
S=<scratch>; G=$S/gates
LITEX=<home>/litex-milan/venv/bin
V=<tools>/pinned-verilator-5.050
SDK=<data>/tmp/665s9-a760<home-path>/host/bin
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export PATH=$LITEX:$V:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin:$SDK
export TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c
export GIT_ALLOW_PROTOCOL=file:https
mkdir -p "$G" "$TMPDIR" "$HOME"
D=$G/budget-$P-r1head; rm -rf "$D" "$S/tmp/budget-$P-r1head"
bash $S/tools/clone.sh "$D" "$H" > "$G/budget-$P-r1head-clone.log" 2>&1 || exit 3
gate() { local name=$1; shift; (cd "$D" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")"; }

gate budget-$P-r1head python3 -B tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $S/tmp/budget-$P-r1head --record-budget-findings
