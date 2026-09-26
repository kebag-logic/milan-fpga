#!/bin/sh
# Run one chunk of the expanded `make -n run` recipe of tb/verilator/milan_dp
# from the suite directory, with the scoped Verilator 5.050 wrapper first on PATH.
# usage: run_chunk.sh <packet-dir> <clone-dir> <chunk-name>
set -e
P="$1"; C="$2"; N="$3"
cd "$C/tb/verilator/milan_dp"
export PATH="$P/scratch/bin:$PATH" TMPDIR="$P/scratch/tmp"
exec /usr/bin/time -f "chunk=$N wall_s=%e maxrss_kb=%M exit=%x" sh -e "$P/scratch/chunks/$N.sh"
