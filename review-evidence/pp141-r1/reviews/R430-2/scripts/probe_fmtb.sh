#!/bin/sh
# R430-1 S1 re-probe at the head: E_SCLKS's CHECK_ARG compare narrowed to FMT_B
# (byte-wide) in a disposable export; run the whole default tb/pp_top build.
set -e
cd "$1"
python3 - <<'PY'
from pathlib import Path
p = Path("hdl/aecp/ucode/gen_ucode.py"); s = p.read_text()
old = "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_W,       # index < count, else BAD_ARGS\n"
new = "    u('CHECK_ARG', ra=12, rb=9, fmt=FMT_B,       # index < count, else BAD_ARGS\n"
assert s.count(old) == 1; p.write_text(s.replace(old, new))
PY
cd tb/pp_top; make gsi-build > build.log 2>&1
set +e; ./obj_dir/Vpp_top_sim > sim.log 2>&1; echo "sim rc=$?"
grep '^FAIL' sim.log; tail -1 sim.log
