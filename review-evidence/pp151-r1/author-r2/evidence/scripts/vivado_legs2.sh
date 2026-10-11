#!/usr/bin/env bash
# vivado_legs.sh <tree> <out-prefix>: the bench's xsim and synth legs on <tree>, under the Vivado lock
set -u
export PATH=<vivado>/2026.1/Vivado/bin:<scratch>/tools/bin:$PATH
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
tree=$1 out=$2
cd <scratch>
start=$(date +%s)
flock -x $VIVADO_LOCK python3 -B "${BENCH:-$tree/tb/elab_guards/guards.py}" --root "$tree" --frontend xsim --frontend synth --jobs 1 > "$out.log" 2>&1
echo $? > "$out.rc"; echo $(( $(date +%s) - start )) > "$out.secs"
