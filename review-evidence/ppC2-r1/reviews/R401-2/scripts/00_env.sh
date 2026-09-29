#!/bin/sh
# Shared environment for the R401-2 receipts. Portable: set CLONE to a checkout
# holding the head commit and VLT to a Verilator 5.050 launcher.
: "${PKT:=$(cd "$(dirname "$0")/.." && pwd)}"
: "${CLONE:?set CLONE to a clone of protocol-processor-control-plane-avb-milan}"
: "${HEAD_SHA:=053f979b9cfc84871ff2e107d43d20bf0e950db4}"
: "${HEAD_TREE:=33087148b197340778ee033f3f2210ac0f629059}"
: "${BASE_SHA:=c951a9ff0cb5851fb159d33e966e5a2a9a188fe3}"
: "${VLT:?set VLT to a launcher that reports Verilator 5.050}"
export PKT CLONE HEAD_SHA HEAD_TREE BASE_SHA VLT
export TMPDIR="$PKT/scratch/tmp"
mkdir -p "$TMPDIR" "$PKT/scratch/bin"
ln -sf "$VLT" "$PKT/scratch/bin/verilator"
PATH="$PKT/scratch/bin:$PATH"; export PATH
