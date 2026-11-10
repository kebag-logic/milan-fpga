#!/usr/bin/env bash
# srptx_gates.sh <head>: make srptx, srptx-plants and srptx-mutants, and git diff --check against the merge base, on
# their own clean clones of <head> under gates/, each log gates/<name>.log ending in rc=N
set -uo pipefail
H=$1; S=/data-2/milan/tmp/665s7-a757b; G=$S/gates; T=$MANAGEMENT/2026-09-23/665s7-a757b/tools
V=$VALIDATION_TOOLS/pinned-verilator-5.050
export TMPDIR=$S/tmp VERILATOR=$V/verilator MAKEFLAGS=-j16
export PATH=$V:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
mkdir -p "$G" "$TMPDIR"
gate() { local name=$1 dir=$2; shift 2; (cd "$dir" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")"; }
rm -rf "$G/srptx" "$G/diffcheck"
bash $T/clone.sh "$G/srptx" "$H" > "$G/srptx-clone.log" 2>&1 || { echo "clone failed"; exit 1; }
bash $T/clone.sh "$G/diffcheck" "$H" > "$G/diffcheck-clone.log" 2>&1 || { echo "clone failed"; exit 1; }
gate diff-check "$G/diffcheck" git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 "$H"
gate make-srptx "$G/srptx" make --no-print-directory -C tb/verilator/milan_dp srptx
gate make-srptx-plants "$G/srptx" make --no-print-directory -C tb/verilator/milan_dp srptx-plants
gate make-srptx-mutants "$G/srptx" make --no-print-directory -C tb/verilator/milan_dp srptx-mutants
gate srptx-clean "$G/srptx" git status --porcelain --ignored=no
echo "$(date +%T) srptx_gates.sh done"
