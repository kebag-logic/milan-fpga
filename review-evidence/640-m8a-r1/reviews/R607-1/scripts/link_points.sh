#!/usr/bin/env bash
# R607-1: link the four fit points in the split layout (and flat, for the span
# comparison) with the pinned RV32 SDK, then plan each split image.
#   link_points.sh <tree> <out> <litex-python>
# Needs MILAN_RV32_CC set to the pinned SDK's riscv32-linux-gcc. RUNTIME_CC, when set,
# names the compiler for the runtime archives only (the SDK defaults to the stack
# protector, which the freestanding runtime cannot link).
set -u
tree=$1 out=$2 py=$3
mkdir -p "$out"
lite="$HOME/litex-milan"
MILAN_RV32_CC="${RUNTIME_CC:-$MILAN_RV32_CC}" "$py" "$tree/sw/firmware/ctrl/test/ctrl_image_runtime.py" \
  --picolibc "$lite/pythondata-software-picolibc/pythondata_software_picolibc/data" \
  --compiler-rt "$lite/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data" \
  --litex-software "$lite/litex/litex/soc/software" --output "$out/runtime" > "$out/runtime.log" 2>&1
echo "runtime rc=$?"
pids=()
for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ifs in 1 2; do
    for layout in split flat; do
      d="$out/$layout-$cfg-if$ifs"
      ( "$py" "$tree/sw/firmware/ctrl/test/ctrl_srp_image.py" --config "$tree/configs/$cfg.yaml" \
          --interfaces "$ifs" --with-aecp --layout "$layout" --output "$d" \
          --libc "$out/runtime/libc.a" --compiler-runtime "$out/runtime/libcompiler_rt.a" \
          > "$d.log" 2>&1; echo "$?" > "$d.rc" ) &
      pids+=($!)
    done
  done
done
wait "${pids[@]}"
for f in "$out"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
