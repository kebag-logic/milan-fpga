#!/bin/bash
# Build every image at every point from a source tree: the size fixture (ctrl_srp_image.py --with-aecp --layout split)
# and the target platform (ctrl_plat_image.py) at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if, against fixed flash maps and
# runtime archives taken read-only from a 1x1 (B1) and an 8x8 (B8) CPU budget harness build. Prints one line an image:
# rc, rom, sram, tiles, and the sha256 of the ELF and of its loadable bytes (objcopy -O binary).
# usage: qimg_r843.sh TREE OUT B1 B8 OBJCOPY
set -u
L=$(realpath "$1") O=$2 B1=$3 B8=$4 OC=$5
mkdir -p "$O"
X=$L/sw/firmware/ctrl/test
one() {  # kind shape n
    local k=$1 s=$2 n=$3 b cfg lp="" d
    if [ "$s" = 8 ]; then b=$B8 cfg=endstation_ax7101_8x8; else b=$B1 cfg=endstation_ax7101_1x1_tdm8; fi
    d=$O/$k-${s}x${s}-${n}if; mkdir -p "$d"
    if [ "$k" = fixture ]; then
        [ "$s$n" = 82 ] && lp="--ledgered-point 8x8-two-interfaces"
        python3 -B "$X/ctrl_srp_image.py" --config "$L/configs/$cfg.yaml" --interfaces "$n" --with-aecp \
            --layout split --output "$d/image" $lp --flash-map "$b/split-soc/flash-map" --libc "$b/runtime/libc.a" \
            --compiler-runtime "$b/runtime/libcompiler_rt.a" > "$d/image.log" 2>&1
    else
        [ "$s$n" = 82 ] && lp="--ledgered-point platform-8x8-two-interfaces"
        python3 -B "$X/ctrl_plat_image.py" --config "$L/configs/$cfg.yaml" --interfaces "$n" \
            --csr-csv "$X/ctrl_plat_csr.csv" --flash-map "$b/split-soc/flash-map" --output "$d/image" $lp \
            --libc "$b/runtime/libc.a" --compiler-runtime "$b/runtime/libcompiler_rt.a" > "$d/image.log" 2>&1
    fi
    echo $? > "$d/rc"
    local elf; elf=$(ls "$d"/image/*.elf 2>/dev/null | head -1)
    if [ -n "$elf" ]; then "$OC" -O binary "$elf" "$d/loadable.bin"; sha256sum "$elf" | cut -d' ' -f1 > "$d/elf.sha256"
        sha256sum "$d/loadable.bin" | cut -d' ' -f1 > "$d/bin.sha256"; fi
}
for k in fixture platform; do for p in "1 1" "1 2" "8 1" "8 2"; do one $k $p & done; done; wait
python3 -I - "$O" <<'PYEOF'
import json, re, sys
from pathlib import Path
out = Path(sys.argv[1])
for d in sorted(p for p in out.iterdir() if p.is_dir()):
    text = (d / 'image.log').read_text()
    m = re.search(r'^\{\n.*?^\}', text, re.M | re.S)
    rc = (d / 'rc').read_text().strip()
    sha = lambda n: (d / n).read_text().strip() if (d / n).exists() else '-'
    if not m:
        print(f'{d.name}: rc {rc} (no size report) elf {sha("elf.sha256")}')
        continue
    s = json.loads(m[0])['split']
    print(f"{d.name}: rc {rc} rom {s['rom']['bytes']} sram {s['sram']['bytes']} tiles {s['tiles']} "
          f"elf {sha('elf.sha256')} loadable {sha('bin.sha256')}")
PYEOF
