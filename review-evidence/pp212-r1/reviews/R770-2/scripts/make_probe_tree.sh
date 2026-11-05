#!/usr/bin/env bash
# usage: make_probe_tree.sh <clean-source-tree> <dest> <probes.inc>
set -euo pipefail
src=$1; dst=$2; inc=$3
rm -rf "$dst"; mkdir -p "$dst/tb"
cp -r "$src/hdl" "$dst/hdl"
cp -r "$src/tb/srp_stream_fsms" "$src/tb/common" "$dst/tb/"
f=$dst/tb/srp_stream_fsms/sim_main.cpp
python3 -I - "$f" "$inc" <<'PY'
import sys
f, inc = sys.argv[1], sys.argv[2]
s = open(f).read()
d = "  void a_link_change_ends_the_registrations_a_settle_could_take();\n"
assert s.count(d) == 1
s = s.replace(d, d + "  void r770_probes();\n")
r = "int SrpStreamFsmsSuite::run() {\n"
assert s.count(r) == 1
s = s.replace(r, open(inc).read() + "\n" + r)
c = "  a_link_change_ends_the_registrations_a_settle_could_take();\n\n  printf("
assert s.count(c) == 1
s = s.replace(c, "  a_link_change_ends_the_registrations_a_settle_could_take();\n  r770_probes();\n\n  printf(")
open(f, "w").write(s)
PY
