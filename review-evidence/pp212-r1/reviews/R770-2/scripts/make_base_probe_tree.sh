#!/usr/bin/env bash
# usage: make_base_probe_tree.sh <git-repo> <commit> <dest> <probe.inc>
set -euo pipefail
repo=$1; rev=$2; dst=$3; inc=$4
rm -rf "$dst"; mkdir -p "$dst"
git -C "$repo" archive "$rev" hdl tb/srp_stream_fsms tb/common | tar -x -C "$dst"
python3 -I - "$dst/tb/srp_stream_fsms/sim_main.cpp" "$inc" <<'PY'
import sys
f, inc = sys.argv[1], sys.argv[2]
s = open(f).read()
a = "class SrpStreamFsmsSuite {\n public:\n  int run();\n"
assert s.count(a) == 1
s = s.replace(a, a + "  void r770_rebind_base();\n")
r = "int SrpStreamFsmsSuite::run() {\n"
assert s.count(r) == 1
s = s.replace(r, open(inc).read() + "\n" + r + "  r770_rebind_base();\n")
open(f, "w").write(s)
PY
