#!/bin/bash
# Every image at every point from a tree: the size fixture (ctrl_srp_image.py) and the target platform
# (ctrl_plat_image.py) at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if, on fixed flash maps and runtimes (B1, B8: a 1x1 and an
# 8x8 harness build's split-soc/ and runtime/, read only) and the suite's CSR map. Prints one line an image: rc, rom,
# sram, tiles, and the sha256 of the ELF and of its loadable bytes (objcopy -O binary). usage: qimg.sh TREE OUT
set -u
L=$(realpath "$1") O=$2 T=/data-2/milan/tmp/894b-a781
. $T/scripts/env.sh
rm -rf "$O"; mkdir -p "$O"
B1=${B1:-/data-2/milan/tmp/894b-a781/inputs/B1} B8=${B8:-/data-2/milan/tmp/894b-a781/inputs/B8}
X=$L/sw/firmware/ctrl/test
PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
OC=$(ls $WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-*-objcopy | head -1)
one() {  # kind shape n
    local k=$1 s=$2 n=$3 b cfg lp="" d
    if [ "$s" = 8 ]; then b=$B8 cfg=endstation_ax7101_8x8; else b=$B1 cfg=endstation_ax7101_1x1_tdm8; fi
    d=$O/$k-${s}x${s}-${n}if; mkdir -p "$d"
    if [ "$k" = fixture ]; then
        [ "$s$n" = 82 ] && lp="--ledgered-point 8x8-two-interfaces"
        $PY -B $L/sw/firmware/ctrl/test/ctrl_srp_image.py --config $L/configs/$cfg.yaml --interfaces $n --with-aecp \
            --layout split --output $d/image $lp --flash-map $b/split-soc/flash-map --libc $b/runtime/libc.a \
            --compiler-runtime $b/runtime/libcompiler_rt.a > $d/image.log 2>&1
    else
        [ "$s$n" = 82 ] && lp="--ledgered-point platform-8x8-two-interfaces"
        $PY -B $L/sw/firmware/ctrl/test/ctrl_plat_image.py --config $L/configs/$cfg.yaml --interfaces $n \
            --csr-csv $X/ctrl_plat_csr.csv --flash-map $b/split-soc/flash-map --output $d/image $lp --libc $b/runtime/libc.a \
            --compiler-runtime $b/runtime/libcompiler_rt.a > $d/image.log 2>&1
    fi
    echo $? > $d/rc
    local elf; elf=$(ls $d/image/*.elf 2>/dev/null | head -1)
    if [ -n "$elf" ]; then $OC -O binary "$elf" $d/loadable.bin; sha256sum "$elf" | cut -d' ' -f1 > $d/elf.sha256
        sha256sum $d/loadable.bin | cut -d' ' -f1 > $d/bin.sha256; basename "$elf" > $d/elf.name; fi
}
for k in fixture platform; do for p in "1 1" "1 2" "8 1" "8 2"; do one $k $p & done; done; wait
$PY -I - "$O" <<'PYEOF'
import json, re, sys
from pathlib import Path
out = Path(sys.argv[1])
for d in sorted(p for p in out.iterdir() if p.is_dir()):
    text = (d / 'image.log').read_text()
    m = re.search(r'^\{\n.*?^\}', text, re.M | re.S)
    rc = (d / 'rc').read_text().strip()
    sha = lambda n: (d / n).read_text().strip() if (d / n).exists() else '-'
    if not m:
        why = [l for l in text.splitlines() if 'budget' in l or 'REFUSED' in l or 'rror' in l][-1:]
        print(f'{d.name}: rc {rc} {why} elf {sha("elf.sha256")}')
        continue
    s = json.loads(m[0])['split']
    print(f"{d.name}: rc {rc} rom {s['rom']['bytes']} in {sum(s['rom']['banks'])}, sram {s['sram']['bytes']} in "
          f"{sum(s['sram']['banks'])}, tiles {s['tiles']}, ledgered {s.get('ledgered')} {s.get('ledgered_tiles')}, "
          f"{sha('elf.name')} sha256 {sha('elf.sha256')}, loadable sha256 {sha('bin.sha256')}")
PYEOF
