#!/bin/sh
# Shared environment for the R401-1 probes. Portable: set CLONE to a checkout
# holding the head commit and VLT to a Verilator 5.050 launcher (the packet's
# own scratch/toolbin/verilator wrapper by default; it is not published).
: "${PKT:=$(cd "$(dirname "$0")/.." && pwd)}"
: "${CLONE:?set CLONE to a clone of protocol-processor-control-plane-avb-milan}"
: "${HEAD_SHA:=b03d36f2c763061e3c9f1dcc19e4f7aee0f1a745}"
: "${VLT:=$PKT/scratch/toolbin/verilator}"   # must report Verilator 5.050
export PKT CLONE HEAD_SHA VLT
export TMPDIR="$PKT/scratch/tmp"
mkdir -p "$TMPDIR"
