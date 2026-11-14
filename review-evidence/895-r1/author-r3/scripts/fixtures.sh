#!/bin/bash
# fixtures.sh TREE OUT PLATDIR: ledger.sh with the platform images and exports of an earlier ledger.sh run (PLATDIR) reused; the memory ledger of TREE at every point. The target platform's images by the tree's own
# plat_ledger.py (each shape's split export, flash map and runtime built under OUT/plat, graded against the ledger);
# then the size fixture's images at the four points, and the CPU budget harness's two 8x8/2if variant arms
# (answering-every-port, valid-destinations), each linked by the tree's ctrl_srp_image.py (fixture_variant.py for an
# arm, through build.py's own edits) on that runtime and each shape's flash map, the ledgered point named at 8x8/2if.
# Writes OUT/summary.md from each image's size.json. Read-only on TREE.
set -u
T=$1 O=$2
mkdir -p "$O"
cd "$T" || exit 3
echo "tree $(git rev-parse HEAD) dirty $(git status --porcelain | wc -l)" > "$O/HEAD.txt"
ln -sfn "$3" "$O/plat"; echo skipped > "$O/plat_ledger.log"
echo - > "$O/plat_ledger.rc"
RT=$O/plat/runtime
for spec in "1x1 endstation_ax7101_1x1_tdm8 1" "1x1 endstation_ax7101_1x1_tdm8 2" "8x8 endstation_ax7101_8x8 1" \
            "8x8 endstation_ax7101_8x8 2"; do
  set -- $spec; shape=$1 cfg=$2 n=$3
  fx=(); [ "$shape$n" = "8x82" ] && fx=(--ledgered-point 8x8-two-interfaces)
  python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$cfg.yaml --interfaces $n --with-aecp \
    --layout split "${fx[@]}" --output "$O/fixture-$shape-if$n" --flash-map "$O/plat/$cfg/split-soc/flash-map" \
    --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" > "$O/fixture-$shape-if$n.log" 2>&1
  echo $? > "$O/fixture-$shape-if$n.rc"
done
python3 -B - "$T" "$O" <<'PY' > "$O/arms.log" 2>&1
import sys
from pathlib import Path
tree, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import build
cfg = 'endstation_ax7101_8x8'
for v in ('answering-every-port', 'valid-destinations'):
    o = out / f'arm-{v}'
    o.mkdir(parents=True, exist_ok=True)
    fixture = build.variant_fixture(o, v)
    ok = 0
    try:
        build.run([sys.executable, '-B', str(build.HERE / 'fixture_variant.py'), str(fixture),
                   '--config', str(tree / 'configs' / (cfg + '.yaml')), '--interfaces', '2', '--with-aecp',
                   '--layout', 'split', '--output', str(o / 'image'), '--ledgered-point', '8x8-two-interfaces',
                   '--flash-map', str(out / 'plat' / cfg / 'split-soc/flash-map'),
                   '--libc', str(out / 'plat/runtime/libc.a'),
                   '--compiler-runtime', str(out / 'plat/runtime/libcompiler_rt.a')], o / 'image.log', cwd=tree)
    except RuntimeError as e:
        ok = 1
        print(f'{v}: {e}')
    (out / f'arm-{v}.rc').write_text(f'{ok}\n')
PY
python3 -B - "$O" <<'PY' > "$O/summary.md"
import json, sys, subprocess
from pathlib import Path
o = Path(sys.argv[1])
print(f"{(o / 'HEAD.txt').read_text().strip()}; plat_ledger.py rc {(o / 'plat_ledger.rc').read_text().strip()}\n")
print('| Image | rc | rom B | sram B | RAMB36 | rom banks B | sram banks B | ctrl_plat B | last log line |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---|')
rows = [(f'platform {p.name}', p, o / 'plat' / f'{p.name}.rc', o / 'plat' / f'{p.name}.log')
        for p in sorted((o / 'plat').glob('*x*-if*')) if p.is_dir()]
rows += [(f'fixture {p.name[8:]}', p, o / f'{p.name}.rc', o / f'{p.name}.log')
         for p in sorted(o.glob('fixture-*')) if p.is_dir()]
rows += [(f'harness arm {p.name[4:]} 8x8-if2', p / 'image', o / f'{p.name}.rc', p / 'image.log')
         for p in sorted(o.glob('arm-*')) if p.is_dir()]
for name, d, rc, log in rows:
    r = rc.read_text().strip() if rc.is_file() else '?'
    last = (log.read_text().strip().splitlines() or [''])[-1][:160] if log.is_file() else ''
    refused = next((l for l in log.read_text().splitlines() if 'REFUSED' in l), '') if log.is_file() else ''
    try:
        s = json.loads(next(d.rglob('size.json')).read_text())['split']
        elf = next(d.rglob('*.elf'))
        nm = subprocess.run(['riscv32-buildroot-linux-gnu-nm', '-S', str(elf)], capture_output=True, text=True).stdout
        plat = next((int(l.split()[1], 16) for l in nm.splitlines() if l.split()[-1] == 'ctrl_plat'), '')
        print(f"| {name} | {r} | {s['rom']['bytes']} | {s['sram']['bytes']} | {s['tiles']} | "
              f"{sum(s['rom']['banks'])} | {sum(s['sram']['banks'])} | {plat} | |")
    except StopIteration:
        print(f"| {name} | {r} | | | | | | | {(refused or last)[:200]} |")
PY
cat "$O/summary.md"
