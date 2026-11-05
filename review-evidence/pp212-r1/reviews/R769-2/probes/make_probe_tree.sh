#!/usr/bin/env bash
# Usage: make_probe_tree.sh <processor-clone> <dest>
# Copies hdl/ and tb/{common,srp_stream_fsms} and inserts the probe block
# before the tally line of SrpStreamFsmsSuite::run().
set -euo pipefail
src=$1; dst=$2; here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$dst"; mkdir -p "$dst/tb"
cp -a "$src/hdl" "$dst/hdl"
cp -a "$src/tb/common" "$src/tb/srp_stream_fsms" "$dst/tb/"
rm -rf "$dst"/tb/srp_stream_fsms/obj_*
f="$dst/tb/srp_stream_fsms/sim_main.cpp"
python3 -I - "$f" "$here/r769_2_probe_block.cpp" <<'PY'
import sys
f, blk = sys.argv[1], open(sys.argv[2]).read()
s = open(f).read()
key = '  printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);\n  return fails ? 1 : 0;\n}\n\n}  // namespace'
assert s.count(key) == 1, "anchor"
s = s.replace(key, blk + key)
open(f, "w").write(s)
PY
