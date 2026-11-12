#!/bin/bash
# Link the size fixture's and the target platform's images at the four ledger points of a tree, on round 28's
# runtime archives and split SoC exports (inputs the firmware does not change), read-only. usage: images.sh TREE OUTDIR
set -u
T=$1 O=$2 R=/data-2/milan/tmp/665s2b-a683zm/builds
. $MANAGEMENT/2026-09-23/895-a775/scripts/env.sh
mkdir -p "$O"
echo "tree $(git -C $T rev-parse HEAD) dirty $(git -C $T status --porcelain | wc -l) stack $(git -C $T/third_party/tsn-c-stack rev-parse HEAD)" > $O/HEAD.txt
for spec in "1x1 endstation_ax7101_1x1_tdm8 1 GA1" "1x1 endstation_ax7101_1x1_tdm8 2 GA1" "8x8 endstation_ax7101_8x8 1 GA8" "8x8 endstation_ax7101_8x8 2 GA8"; do
  set -- $spec; shape=$1 cfg=$2 n=$3 b=$4
  fx=(); pl=(); [ "$shape$n" = "8x82" ] && fx=(--ledgered-point 8x8-two-interfaces) && pl=(--ledgered-point platform-8x8-two-interfaces)
  ( cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $n --with-aecp --layout split "${fx[@]}" \
      --output $O/fixture-$shape-if$n --flash-map $R/$b/split-soc/flash-map --libc $R/$b/runtime/libc.a --compiler-runtime $R/$b/runtime/libcompiler_rt.a ) > $O/fixture-$shape-if$n.log 2>&1
  echo $? > $O/fixture-$shape-if$n.rc
  ( cd "$T" && python3 -B sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/$cfg.yaml --interfaces $n "${pl[@]}" \
      --csr-csv $R/$b/split-soc/mapped/soc/csr.csv --flash-map $R/$b/split-soc/flash-map --output $O/platform-$shape-if$n \
      --libc $R/$b/runtime/libc.a --compiler-runtime $R/$b/runtime/libcompiler_rt.a ) > $O/platform-$shape-if$n.log 2>&1
  echo $? > $O/platform-$shape-if$n.rc
done
python3 - "$O" <<'PY'
import json, sys, subprocess
from pathlib import Path
o = Path(sys.argv[1])
print('| Point | image | rc | rom B | sram B | RAMB36 (tiles) | rom banks B | srp_mbx text B | ctrl_plat B | last log line |')
for d in sorted(o.glob('*-if*')):
    if not d.is_dir(): continue
    rc = (o / f'{d.name}.rc').read_text().strip()
    last = (o / f'{d.name}.log').read_text().strip().splitlines()[-1:] or ['']
    try:
        s = json.loads((d / 'size.json').read_text())['split']
        elf = next(d.glob('*.elf'))
        nm = subprocess.run(['riscv32-buildroot-linux-gnu-nm', '-S', '--size-sort', str(elf)], capture_output=True, text=True).stdout
        plat = next((int(l.split()[1], 16) for l in nm.splitlines() if l.split()[-1] == 'ctrl_plat'), '')
        print(f"| {d.name.split('-',1)[1]} | {d.name.split('-')[0]} | {rc} | {s['rom']['bytes']} | {s['sram']['bytes']} | {s['tiles']} | {sum(s['rom']['banks'])} | | {plat} | |")
    except Exception as e:
        print(f"| {d.name.split('-',1)[1]} | {d.name.split('-')[0]} | {rc} | | | | | | | {last[0][:200]} |")
PY
