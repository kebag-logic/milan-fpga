#!/bin/bash
# Build the runtime archives (the harness's runtime_ssp.py) and the linked split image at one point from a checkout.
# usage: build_image.sh CHECKOUT OUT SHAPE N_IF
set -eu
. $MANAGEMENT/2026-09-23/665s2b-a683k/scripts/env.sh
C=$1 O=$2 SHAPE=$3 N=$4
mkdir -p "$O"
LM=$WORKSPACE_HOME/litex-milan
[ -f "$O/runtime/libc.a" ] || python3 -B "$C/tb/verilator/ctrl_service_budget/runtime_ssp.py" \
  --picolibc $LM/pythondata-software-picolibc/pythondata_software_picolibc/data \
  --compiler-rt $LM/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data \
  --litex-software $LM/litex/litex/soc/software --output "$O/runtime" > "$O/runtime.log" 2>&1
(cd "$C" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$SHAPE.yaml" --interfaces "$N" \
  --with-aecp --layout split --output "$O/image" --libc "$O/runtime/libc.a" \
  --compiler-runtime "$O/runtime/libcompiler_rt.a") > "$O/image.log" 2>&1
sha256sum "$O/image/ctrl_app.elf"
