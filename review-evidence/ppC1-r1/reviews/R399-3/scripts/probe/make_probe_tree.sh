#!/usr/bin/env bash
# Build a probe copy of an exported tree: sim_main.cpp gains `--r399-probe`, which runs
# only R399Probe (r399_probe.hpp). Optional: a tb/srp_top/mutations patch to plant.
# usage: make_probe_tree.sh <exported_tree> <probe_dir> [patch_label]
set -euo pipefail
src=$1; dst=$2; label=${3:-}
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$dst"; mkdir -p "$dst/tb"
cp -r "$src/hdl" "$dst/hdl"; cp -r "$src/tb/common" "$src/tb/pp_top" "$dst/tb/"
rm -rf "$dst/tb/pp_top/obj_dir"
cp "$here/r399_probe.hpp" "$dst/tb/pp_top/"
f="$dst/tb/pp_top/sim_main.cpp"
python3 - "$f" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
anchor = "int main(int argc, char** argv) {\n  Verilated::commandArgs(argc, argv);\n"
assert s.count(anchor) == 1
hook = anchor + ("  if (argc == 2 && std::strcmp(argv[1], \"--r399-probe\") == 0) {\n"
                 "    const milan::tb::Model<Vpp_top_wrap> pm; H ph(pm.get());\n"
                 "    R399Probe{ph}.run(); return ph.fails ? 1 : 0; }\n")
s = s.replace(anchor, '#include "r399_probe.hpp"\n\n' + hook)
open(p, "w").write(s)
PY
if [ -n "$label" ]; then
  (cd "$dst" && git init -q . && git apply --check "$src/tb/srp_top/mutations/$label.patch" \
     && git apply "$src/tb/srp_top/mutations/$label.patch" && rm -rf .git)
  echo "planted $label"
fi
