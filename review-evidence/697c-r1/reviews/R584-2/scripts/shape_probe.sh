#!/usr/bin/env bash
# Shape-value probe: plant a stack-example include under IMAGE_SINKS > 1u in the image fixture, then
# show (1) the boundary gate passes it and (2) the image builder at the 8x8 shape compiles that branch.
# Usage: shape_probe.sh <pristine probe clone> <work dir> <rv32 cc>
set -u
P=$(cd "$1" && pwd); W=$2; export MILAN_RV32_CC=$3
rm -rf "$W"; cp -a "$P" "$W"; cd "$W"
f=sw/firmware/ctrl/test/rv32_image/image_main.c
python3 -I - "$f" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read(); a="#include <stdbool.h>\n"; assert s.count(a)==1
open(p,"w").write(s.replace(a, a+'#if IMAGE_SINKS > 1u\n#include "../../../../../third_party/tsn-c-stack/examples/adp_port.h"\n#error PROBE-REACHED: the 8x8 image compiled the stack example header\n#endif\n'))
PY
git diff --stat
python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 > boundary.out 2>&1; echo "boundary rc=$?: $(tail -1 boundary.out)"
python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape endstation_ax7101_1x1_tdm8 > img1x1.out 2>&1; echo "ctrl_image 1x1 rc=$?: $(grep -m1 -a 'PROBE-REACHED\|^shape\|REFUSED' img1x1.out)"
python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape endstation_ax7101_8x8 > img8x8.out 2>&1; echo "ctrl_image 8x8 rc=$?: $(grep -m1 -a 'PROBE-REACHED\|REFUSED' img8x8.out)"
grep -a -m1 'adp_port.h' img8x8.out || echo "(no adp_port.h mention: the include resolved, then #error fired)"
