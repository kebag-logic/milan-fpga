#!/bin/bash
# Link the size fixture's and the target platform's images at the four ledger points from the review clone,
# on the reviewer's own harness builds' runtime archives and split SoC exports. usage: images.sh TREE OUTDIR B1 B8
set -u
T=$1 O=$2 B1=$3 B8=$4
mkdir -p "$O"
echo "tree $(git -C $T rev-parse HEAD) dirty $(git -C $T status --porcelain | wc -l) stack $(git -C $T/third_party/tsn-c-stack rev-parse HEAD)" > $O/HEAD.txt
for spec in "1x1 endstation_ax7101_1x1_tdm8 1 $B1" "1x1 endstation_ax7101_1x1_tdm8 2 $B1" "8x8 endstation_ax7101_8x8 1 $B8" "8x8 endstation_ax7101_8x8 2 $B8"; do
  set -- $spec; shape=$1 cfg=$2 n=$3 b=$4
  fx=(); pl=(); [ "$shape$n" = "8x82" ] && fx=(--ledgered-point 8x8-two-interfaces) && pl=(--ledgered-point platform-8x8-two-interfaces)
  ( cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $n --with-aecp --layout split "${fx[@]}" \
      --output $O/fixture-$shape-if$n --flash-map $b/split-soc/flash-map --libc $b/runtime/libc.a --compiler-runtime $b/runtime/libcompiler_rt.a ) > $O/fixture-$shape-if$n.log 2>&1
  echo $? > $O/fixture-$shape-if$n.rc
  ( cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/$cfg.yaml --interfaces $n "${pl[@]}" \
      --csr-csv $b/split-soc/mapped/soc/csr.csv --flash-map $b/split-soc/flash-map --output $O/platform-$shape-if$n \
      --libc $b/runtime/libc.a --compiler-runtime $b/runtime/libcompiler_rt.a ) > $O/platform-$shape-if$n.log 2>&1
  echo $? > $O/platform-$shape-if$n.rc
done
# the size fixture's 8x8/2if image refused without its ledgered key, and the platform's likewise (the ledger is by name)
( cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --interfaces 2 --with-aecp --layout split \
   --output $O/fixture-8x8-if2-nokey --flash-map $B8/split-soc/flash-map --libc $B8/runtime/libc.a --compiler-runtime $B8/runtime/libcompiler_rt.a ) > $O/fixture-8x8-if2-nokey.log 2>&1; echo $? > $O/fixture-8x8-if2-nokey.rc
python3 - "$O" <<'PY'
import json, sys, subprocess
from pathlib import Path
o = Path(sys.argv[1])
print('| Point | image | rc | rom B | sram B | RAMB36 (tiles) | rom banks B | ctrl_plat B |')
for d in sorted(o.glob('*-if*')):
    if not d.is_dir(): continue
    rc = (o / f'{d.name}.rc').read_text().strip()
    try:
        s = json.loads((d / 'size.json').read_text())['split']
        elf = next(d.glob('*.elf'))
        nm = subprocess.run(['riscv32-buildroot-linux-gnu-nm', '-S', '--size-sort', str(elf)], capture_output=True, text=True).stdout
        plat = next((int(l.split()[1], 16) for l in nm.splitlines() if l.split()[-1] == 'ctrl_plat'), '')
        print(f"| {d.name.split('-',1)[1]} | {d.name.split('-')[0]} | {rc} | {s['rom']['bytes']} | {s['sram']['bytes']} | {s['tiles']} | {sum(s['rom']['banks'])} | {plat} |")
    except Exception as e:
        last = (o / f'{d.name}.log').read_text().strip().splitlines()[-1:] or ['']
        print(f"| {d.name.split('-',1)[1]} | {d.name.split('-')[0]} | {rc} | | | | | {last[0][:220]} |")
PY
