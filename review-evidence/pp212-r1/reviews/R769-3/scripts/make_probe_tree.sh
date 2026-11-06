#!/usr/bin/env bash
# Usage: make_probe_tree.sh <processor-clone> <dest> <block.cpp>...
# Copies hdl/ and tb/{common,srp_stream_fsms} and inserts the probe blocks
# before the tally line of SrpStreamFsmsSuite::run().
set -euo pipefail
src=$1; dst=$2; shift 2
rm -rf "$dst"; mkdir -p "$dst/tb"
cp -a "$src/hdl" "$dst/hdl"
cp -a "$src/tb/common" "$src/tb/srp_stream_fsms" "$dst/tb/"
rm -rf "$dst"/tb/srp_stream_fsms/obj_*
f="$dst/tb/srp_stream_fsms/sim_main.cpp"
python3 -I - "$f" "$@" <<'PY'
import sys
f, blks = sys.argv[1], sys.argv[2:]
blk = "".join(open(b).read() for b in blks)
s = open(f).read()
key = '  printf("%d checks: %d PASS, %d FAIL\\n", checks, checks - fails, fails);\n  return fails ? 1 : 0;\n}\n\n}  // namespace'
assert s.count(key) == 1, "anchor"
s = s.replace(key, blk + key)
open(f, "w").write(s)
PY
