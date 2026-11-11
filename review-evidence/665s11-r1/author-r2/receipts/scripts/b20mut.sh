#!/bin/bash
# b20mut.sh: plant plat-reboot-transmits-after-the-departing into the probe clone, run the platboot arm at one
# interface, restore the file, and list the channels B20 found after ENTITY_DEPARTING
set -u
S=<scratch>; W=$S/probes/wt; F=$W/sw/firmware/ctrl/plat/ctrl_plat.c
cp $F $S/probes/ctrl_plat.c.orig
python3 - "$F" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
old = "\t} else if (ctrl_plat.reboot != 0u) {\n\t\tdepart(&ctrl_plat);\n"
assert t.count(old) == 1
p.write_text(t.replace(old, old + "\t\tif (ctrl_plat.reboot != 3u) {\n\t\t\tctrl_loop_step(&ctrl_plat.app.loop);\n\t\t}\n"))
PY
python3 -B $S/scripts/arms_probe.py $S/probes/b20mut platboot1
cp $S/probes/ctrl_plat.c.orig $F
git -C $W status --porcelain
python3 - <<'PY'
import collections, re
t = open('<scratch>/probes/b20mut/platboot1.log').read()
ch = collections.Counter(m[1] for m in re.findall(r"frames\[k\]\.frame\.channel\n\s*Which is: '\\x(\d)' \((\d)\)", t))
print('B20 under plat-reboot-transmits-after-the-departing: frames after ENTITY_DEPARTING by channel',
      dict(sorted(ch.items())), 'total', sum(ch.values()))
PY
