#!/usr/bin/env bash
# ledger.sh <tree> <out> <runtime>: the split fixture image at the four points, planned by ctrl_memory.plan, with its symbols.
set -u
T=$1; O=$2; R=$3; PY=<litex-env>/venv/bin/python3
mkdir -p "$O"; cd "$T" || exit 3
if [ ! -f "$R/libcompiler_rt.a" ]; then
  pico=$($PY -c 'import pythondata_software_picolibc as p; print(p.data_location)')
  crt=$($PY -c 'import pythondata_software_compiler_rt as p; print(p.data_location)')
  lite=$($PY -c 'import litex, pathlib; print(pathlib.Path(litex.__file__).parent / "soc/software")')
  python3 -B tb/verilator/ctrl_service_budget/runtime_ssp.py --picolibc "$pico" --compiler-rt "$crt" --litex-software "$lite" --output "$R" > "$O/runtime.log" 2>&1; echo "runtime rc=$?" | tee "$O/runtime.rc"
fi
for p in "endstation_ax7101_1x1_tdm8 1" "endstation_ax7101_1x1_tdm8 2" "endstation_ax7101_8x8 1" "endstation_ax7101_8x8 2"; do
  set -- $p; shape=$1; n=$2; tag=${shape#endstation_ax7101_}-if$n; extra=()
  [ "$shape-$n" = endstation_ax7101_8x8-2 ] && extra=(--ledgered-point 8x8-two-interfaces)
  python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$shape.yaml --interfaces $n --with-aecp --layout split "${extra[@]}" \
    --output "$O/$tag" --libc "$R/libc.a" --compiler-runtime "$R/libcompiler_rt.a" > "$O/$tag.log" 2>&1
  echo $? > "$O/$tag.rc"
  ~/br-milan-rv32/host/bin/riscv32-linux-nm -S --size-sort "$O/$tag/ctrl_app.elf" > "$O/$tag.nm" 2>&1
  echo "$tag rc=$(cat $O/$tag.rc) lshrdi3=$(grep -c ' __lshrdi3$' $O/$tag.nm)"
done
