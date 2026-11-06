#!/bin/sh
# Rebuild the CPU budget harness's firmware images at the reviewed head and print their sha256.
# usage: imgcheck.sh <clean clone at head with submodules> <out dir> <litex root>
set -u
SRC=$1; OUT=$2; L=$3; P=$L/venv/bin/python3
mkdir -p "$OUT"
$P -B "$SRC/tb/verilator/ctrl_service_budget/runtime_ssp.py" --picolibc $L/pythondata-software-picolibc/pythondata_software_picolibc/data \
  --compiler-rt $L/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data --litex-software $L/litex/litex/soc/software \
  --output "$OUT/runtime" > "$OUT/runtime.log" 2>&1 || { echo "runtime rc=$?"; exit 1; }
build() { # name config ifs extra...
  n=$1; c=$2; i=$3; shift 3
  $P -B "$SRC/sw/firmware/ctrl/test/ctrl_srp_image.py" --config "$SRC/configs/$c.yaml" --interfaces $i --with-aecp --layout split \
    --output "$OUT/$n" "$@" --libc "$OUT/runtime/libc.a" --compiler-runtime "$OUT/runtime/libcompiler_rt.a" > "$OUT/$n.log" 2>&1
  echo "$n rc=$? $(find "$OUT/$n" -name ctrl_app.elf -exec sha256sum {} \; | cut -c1-64)"
}
build N-A1 endstation_ax7101_1x1_tdm8 1 &
build N-A8 endstation_ax7101_8x8 2 --ledgered-point 8x8-two-interfaces &
wait
