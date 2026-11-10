#!/usr/bin/env bash
# srptx_gates.sh <head>: on one clean clone of <head> under gates/srptx, in order: make srptx, srptx-plants,
# srptx-mutants, R813-2's request_probe.py at offsets 280 and 240 (unchanged; it edits srptx.hpp in the clone and
# restores it), make twin and twin-plants (the wrapped binary's twin capture), then the clone's git status. Each
# log gates/<name>.log ends in rc=N. MAKEFLAGS -j16, pinned Verilator 5.050.
set -uo pipefail
H=$1; S=/data-2/milan/tmp/665s7-a757c; G=$S/gates; T=$MANAGEMENT/2026-09-23/665s7-a757c/tools
V=$VALIDATION_TOOLS/pinned-verilator-5.050
export TMPDIR=$S/tmp VERILATOR=$V/verilator MAKEFLAGS=-j16
export PATH=$V:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
mkdir -p "$G" "$TMPDIR"
gate() { local name=$1 dir=$2; shift 2; (cd "$dir" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")"; }
rm -rf "$G/srptx" "$S/req"
bash $T/clone.sh "$G/srptx" "$H" > "$G/srptx-clone.log" 2>&1 || { echo "clone failed"; exit 1; }
D=$G/srptx
gate make-srptx "$D" make --no-print-directory -C tb/verilator/milan_dp srptx
gate make-srptx-plants "$D" make --no-print-directory -C tb/verilator/milan_dp srptx-plants
gate make-srptx-mutants "$D" make --no-print-directory -C tb/verilator/milan_dp srptx-mutants
gate request-probe "$D" python3 -I $T/request_probe.py tb/verilator/milan_dp $S/req 280 240
gate make-twin "$D" make --no-print-directory -C tb/verilator/milan_dp twin
gate make-twin-plants "$D" make --no-print-directory -C tb/verilator/milan_dp twin-plants
gate srptx-clean "$D" git status --porcelain --ignored=no
echo "$(date +%T) srptx_gates.sh done"
