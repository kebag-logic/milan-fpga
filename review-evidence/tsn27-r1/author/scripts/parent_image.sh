#!/bin/bash
# Runtime archives and the linked split image at one point from a scratch parent checkout, then nm and size.
# usage: parent_image.sh CHECKOUT OUT SHAPE N_IF [LEDGERED_POINT]
set -eu
export PATH=$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin:$PATH
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu PYTHONHASHSEED=0
C=$1 O=$2 SHAPE=$3 N=$4 LP=${5:-}
mkdir -p "$O"
LM=$HOME/litex-milan
RT=$(dirname "$O")/runtime
[ -f "$RT/libc.a" ] || python3 -B "$C/tb/verilator/ctrl_service_budget/runtime_ssp.py" \
  --picolibc $LM/pythondata-software-picolibc/pythondata_software_picolibc/data \
  --compiler-rt $LM/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data \
  --litex-software $LM/litex/litex/soc/software --output "$RT" > "$RT.log" 2>&1
extra=()
[ -n "$LP" ] && extra=(--ledgered-point "$LP")
(cd "$C" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$SHAPE.yaml" --interfaces "$N" \
  --with-aecp --layout split "${extra[@]}" --output "$O/image" --libc "$RT/libc.a" \
  --compiler-runtime "$RT/libcompiler_rt.a") > "$O/image.log" 2>&1
riscv32-buildroot-linux-gnu-nm -n "$O/image/ctrl_app.elf" > "$O/nm.txt"
riscv32-buildroot-linux-gnu-size -A "$O/image/ctrl_app.elf" > "$O/size-A.txt"
riscv32-buildroot-linux-gnu-size "$O/image/ctrl_app.elf" > "$O/size.txt"
sha256sum "$O/image/ctrl_app.elf" > "$O/sha256.txt"
wc -c < "$O/image/ctrl_app.elf" > "$O/bytes.txt"
grep -c "__lshrdi3" "$O/nm.txt" > "$O/lshrdi3-count.txt" || true
cat "$O/sha256.txt" "$O/size.txt" "$O/lshrdi3-count.txt"
