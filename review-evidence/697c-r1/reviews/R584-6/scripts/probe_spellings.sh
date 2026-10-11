#!/bin/bash
# Real-path probes of the round-5 driver spellings against the capture of the firmware-unit replica (capA):
# a firmware unit (maap/maap_csr.c) reaches the stack's examples/ only under a mode, and a disposable builder
# gives that mode in one spelling under its own capture; the boundary judges capA plus that capture.
# K0: plant, no builder giving the mode (must PASS: the plant is dormant). KP: plain -D (must be caught).
# Restores the checkout after every run. Usage: probe_spellings.sh <packet-root> <checkout>
set -u; P=$1; cd "$2"; source $P/scripts/env.sh
B=sw/firmware/ctrl/test/r584_probe_builder.py; U=sw/firmware/ctrl/maap/maap_csr.c
plant(){ python3 -I - "$U" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
add="".join(f'#if defined({m})\n#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"\n#endif\n'
            for m in ("R584_PLAIN_MODE","R584_RSP_MODE","R584_WP_MODE","R584_IMACROS_MODE"))
lines=t.split("\n",3); open(p,"w").write("\n".join(lines[:3])+"\n"+add+lines[3])
PY
}
restore(){ git checkout -q -- sw/firmware; rm -f "$B"; git status --short; }
plant; python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture $P/scratch/capA --without verilator > $P/logs/probe.K0.log 2>&1; echo $? > $P/logs/probe.K0.rc; restore
for s in plain rsp wp imacros; do
  C=$P/scratch/cap_$s; rm -rf "$C"; plant; cp $P/scripts/r584_probe_builder.py "$B"
  python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$C" -- python3 "$B" $s > $P/logs/probe.cap_$s.log 2>&1
  python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture $P/scratch/capA --capture "$C" --without verilator > $P/logs/probe.$s.log 2>&1; echo $? > $P/logs/probe.$s.rc
  restore
done
echo done > $P/logs/probe.spell.done
