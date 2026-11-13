#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer-owned probe of the hot-layout claim: build the harness's runtime once (runtime_ssp.py, as build.firmware
# does), then link the split size-fixture image (ctrl_srp_image.py --layout split, on the RV32 stand-ins, no flash map)
# from each source tree given, at 1x1/1if and at 8x8/2if (its ledgered point), and write each image's sorted symbol
# table (address, size, name) for comparison.
# usage: layout_probe.sh OUT TREE...   (PY: the LiteX venv's python; the pinned RV32 SDK at its default path)
set -u
O=$1; shift
PY=${PY:-python3}
NM=${NM:-$HOME/br-milan-rv32/host/bin/riscv32-linux-nm}
mkdir -p "$O"
first=$1
eval "$("$PY" -c "
import pythondata_software_picolibc as p, pythondata_software_compiler_rt as c, litex, os
print('PICO=' + p.data_location); print('CRT=' + c.data_location)
print('LSW=' + os.path.join(os.path.dirname(litex.__file__), 'soc/software'))")"
( cd "$first" && "$PY" -B tb/verilator/ctrl_service_budget/runtime_ssp.py --picolibc "$PICO" --compiler-rt "$CRT" \
    --litex-software "$LSW" --output "$O/runtime" ) > "$O/runtime.log" 2>&1
echo $? > "$O/runtime.rc"
for T in "$@"; do
  name=$(basename "$T")
  for spec in "endstation_ax7101_1x1_tdm8 1" "endstation_ax7101_8x8 2"; do
    set -- $spec; cfg=$1 n=$2
    led=""; [ "$cfg$n" = "endstation_ax7101_8x82" ] && led="--ledgered-point 8x8-two-interfaces"
    out="$O/$name-$cfg-if$n"
    ( cd "$T" && "$PY" -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$cfg.yaml" --interfaces "$n" \
        --with-aecp --layout split $led --output "$out" --libc "$O/runtime/libc.a" \
        --compiler-runtime "$O/runtime/libcompiler_rt.a" ) > "$out.log" 2>&1
    echo $? > "$out.rc"
    [ -f "$out/ctrl_app.elf" ] && "$NM" -S -n "$out/ctrl_app.elf" | awk 'NF==4' > "$out.syms"
  done
done
