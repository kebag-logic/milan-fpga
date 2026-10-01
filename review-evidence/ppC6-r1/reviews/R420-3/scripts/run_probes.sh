#!/bin/sh
# Build the reviewer probes (r420_3_probes.hpp) into a private copy of a tree's
# tb/pp_top third build and run them. Usage: run_probes.sh SRC_TREE WORK_DIR
# SRC_TREE is an export of the processor tree (hdl/ and tb/ as at some head).
set -eu
here=$(cd "$(dirname "$0")" && pwd)
src=$1
work=$2
rm -rf "$work"
mkdir -p "$work"
cp -a "$src/hdl" "$src/tb" "$src/scripts" "$work/"
[ -d "$src/syn" ] && cp -a "$src/syn" "$work/" || true
rm -rf "$work/tb/pp_top/obj_dir" "$work/tb/pp_top/obj_idn" "$work/tb/pp_top/obj_vid"
cp "$here/r420_3_probes.hpp" "$work/tb/pp_top/"
ph="$work/tb/pp_top/notify_phases.hpp"
python3 - "$ph" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
anchor = "[[maybe_unused]] static void run_identify(H& h) {"
assert s.count(anchor) == 1
s = s.replace(anchor, '#include "r420_3_probes.hpp"\n' + anchor)
old = "  IdentifyPhase{h}.run();\n#else"
assert s.count(old) == 1
s = s.replace(old, "  R420Probe{h}.run();\n#else")
p.write_text(s)
PY
cd "$work/tb/pp_top"
make identify-build VERILATOR="$here/vl8.sh" > build.log 2>&1
./obj_idn/Vpp_top_idn
