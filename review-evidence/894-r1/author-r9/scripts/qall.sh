#!/bin/bash
# Every image at every point from a tree: the size fixture (ctrl_srp_image.py) and the target platform
# (ctrl_plat_image.py) at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if, against round 28's flash maps, runtimes and CSR
# exports (read only). The 8x8/2if images name their ledgered point. Prints one line an image: rom, sram, tiles.
# usage: qall.sh TREE TAG
set -u
L=$(realpath "$1") TAG=$2 T=<scratch>
. $T/scripts/env.sh
O=$T/r9/qall/$TAG; rm -rf "$O"; mkdir -p "$O"
B1=<scratch>/r8/fm/GA1 B8=<scratch>/r8/fm/GA8
X1=$L/sw/firmware/ctrl/test X8=$L/sw/firmware/ctrl/test  # the suite's committed map (ctrl_runs.py), shape-independent
PY=<home-path>
one() {  # kind shape n
    local k=$1 s=$2 n=$3 b x cfg lp="" d
    if [ "$s" = 8 ]; then b=$B8 x=$X8 cfg=endstation_ax7101_8x8; else b=$B1 x=$X1 cfg=endstation_ax7101_1x1_tdm8; fi
    d=$O/$k-${s}x${s}-${n}if; mkdir -p "$d"
    if [ "$k" = fixture ]; then
        [ "$s$n" = 82 ] && lp="--ledgered-point 8x8-two-interfaces"
        $PY -B $L/sw/firmware/ctrl/test/ctrl_srp_image.py --config $L/configs/$cfg.yaml --interfaces $n --with-aecp \
            --layout split --output $d/image $lp --flash-map $b/split-soc/flash-map --libc $b/runtime/libc.a \
            --compiler-runtime $b/runtime/libcompiler_rt.a > $d/image.log 2>&1
    else
        [ "$s$n" = 82 ] && lp="--ledgered-point platform-8x8-two-interfaces"
        $PY -B $L/sw/firmware/ctrl/test/ctrl_plat_image.py --config $L/configs/$cfg.yaml --interfaces $n \
            --csr-csv $x/ctrl_plat_csr.csv --flash-map $b/split-soc/flash-map --output $d/image $lp --libc $b/runtime/libc.a \
            --compiler-runtime $b/runtime/libcompiler_rt.a > $d/image.log 2>&1
    fi
    echo $? > $d/rc
}
for k in fixture platform; do for p in "1 1" "1 2" "8 1" "8 2"; do one $k $p & done; done; wait
$PY -I - "$O" <<'EOF'
import json, re, sys
from pathlib import Path
out = Path(sys.argv[1])
for d in sorted(out.iterdir()):
    text = (d / 'image.log').read_text()
    m = re.search(r'^\{\n.*?^\}', text, re.M | re.S)
    rc = (d / 'rc').read_text().strip()
    if not m:
        why = [l for l in text.splitlines() if 'budget' in l or 'REFUSED' in l or 'rror' in l][-1:]
        print(f'{d.name}: rc {rc} {why}')
        continue
    s = json.loads(m[0])['split']
    print(f"{d.name}: rc {rc} rom {s['rom']['bytes']} in {sum(s['rom']['banks'])}, sram {s['sram']['bytes']} in "
          f"{sum(s['sram']['banks'])}, tiles {s['tiles']}, ledgered {s.get('ledgered')} {s.get('ledgered_tiles')}")
EOF
