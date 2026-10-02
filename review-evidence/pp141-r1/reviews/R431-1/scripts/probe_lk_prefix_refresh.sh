#!/bin/sh
# Disposable probe: in a scratch export of the head, replace the two stale
# context lines of lk-prefix-zero-body.patch with the head's re-wrapped comment
# lines (1:1, so the hunk header stays valid) and run that arm alone.
# Usage: probe_lk_prefix_refresh.sh REPO WORKDIR OUTDIR VERILATOR
set -eu
REPO="$1"; W="$2"; O="$3"; V="$4"
rm -rf "$W" "$O"; mkdir -p "$W"
git -C "$REPO" archive 4a40b1798e463d09aafd74632408003229bcc673 | tar -x -C "$W"
python3 - "$W/tb/pp_top/aecp_dispatch_mutations/lk-prefix-zero-body.patch" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = (" # stored, read back and announced while the media plane resolved it to\n"
       " # INTERNAL. The count sits mid-lane, hence SHIFT_R + a FMT_W MOVE.\n")
new = (" # backed was stored, read back and announced while the media plane resolved\n"
       " # it to INTERNAL. The count sits mid-lane, hence SHIFT_R + a FMT_W MOVE.\n")
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PY
cd "$W" && git apply --check tb/pp_top/aecp_dispatch_mutations/lk-prefix-zero-body.patch
echo "refreshed patch applies at head"
cd "$W/tb/pp_top" && python3 aecp_dispatch_mutants.py --output "$O" --verilator "$V" --only lk-prefix-zero-body
