#!/bin/bash
# Follows sw/firmware/ctrl/plat/README.md's link command as written (no --flash-map) with real runtime archives
# and a real csr.csv, then compares the F1 port's address constants with the image the boot run linked.
# nomap_probe.sh <clone> <boot-run-dir> <out-dir>
. "$(dirname "$0")/env.sh"
clone=$1; run=$2; out=$3
cd "$clone" || exit 9
python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml \
  --csr-csv "$run/soc-provisional/csr.csv" --output "$out" --libc "$run/runtime/libc.a" \
  --compiler-runtime "$run/runtime/libcompiler_rt.a" > "$out.log" 2>&1
echo "no-map link rc=$?"
tail -3 "$out.log" | cut -c1-200
for name in "$run/image/ctrl_app.elf" "$out/ctrl_app.elf"; do
  echo "== $name"
  riscv32-linux-objdump -d "$name" > "$name.dis"
  for pat in 'lui.*0xf0003$' 'lui.*0xf0002$' 'lui.*0xf0004$' 'lui.*0x20000$' 'lui.*0x1000$' 'lui.*0x2000$'; do
    printf '%s: %s\n' "$pat" "$(grep -cE "$pat" "$name.dis")"
  done
  riscv32-linux-nm "$name" | grep -E ' (nvm_flash|ls_|lfp_|litespi)' | head -8
done
