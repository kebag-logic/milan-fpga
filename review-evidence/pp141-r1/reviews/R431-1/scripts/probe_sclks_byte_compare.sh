#!/bin/sh
# Disposable probe: make E_SCLKS's range-check compare byte-wide (FMT_B) in a
# scratch export of the head and run section D3 alone.
# Usage: probe_sclks_byte_compare.sh REPO WORKDIR VERILATOR
set -eu
REPO="$1"; W="$2"; V="$3"
rm -rf "$W"; mkdir -p "$W"
git -C "$REPO" archive 4a40b1798e463d09aafd74632408003229bcc673 | tar -x -C "$W"
python3 - "$W/hdl/aecp/ucode/gen_ucode.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_W,       # index < count, else BAD_ARGS\n      cnd=REL_LT, imm=SCLKS_EMIT),\n"
new = "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_B,       # index < count, else BAD_ARGS\n      cnd=REL_LT, imm=SCLKS_EMIT),\n"
assert s.count(old) == 1
open(p, "w").write(s.replace(old, new))
PY
make -C "$W/tb/pp_top" d3 VERILATOR="$V"
