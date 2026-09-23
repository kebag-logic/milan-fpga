#!/bin/sh
# For each tracked ROM image: generate it from the base generator (git show
# BASE:hdl/ucode/gen_gptp_ucode.py) and from the working generator with the
# same arguments, and list the ROM addresses whose words differ.
set -u
cd "${A188_LANE:-$LANES/gptp68-step-policy}" || exit 2
BASE=${BASE:-c1b617435824929a790739ea8585c3fe1a328cc0}
T=$(mktemp -d)
git show "$BASE:hdl/ucode/gen_gptp_ucode.py" > "$T/gen_base.py"
diffwords() {  # name  args...
  n=$1; shift
  python3 "$T/gen_base.py" "$@" -o "$T/old.hex" >/dev/null
  python3 hdl/ucode/gen_gptp_ucode.py "$@" -o "$T/new.hex" >/dev/null
  python3 - "$T/old.hex" "$T/new.hex" "$n" <<'PY'
import sys
a = open(sys.argv[1]).read().split(); b = open(sys.argv[2]).read().split()
d = [i for i in range(len(a)) if a[i] != b[i]]
rng = f"{d[0]}..{d[-1]}" if d else "none"
print(f"{sys.argv[3]}: {len(d)} words differ, addresses {rng}")
PY
}
diffwords "default (ucpu, syn/ooc)"
diffwords "engine --clk-hz 2000000 --cease-ms 3000" --clk-hz 2000000 --cease-ms 3000
diffwords "engine seq-seed" --clk-hz 2000000 --cease-ms 3000 --seq-seed 0x200000
diffwords "engine sync-seq-seed" --clk-hz 2000000 --cease-ms 3000 --sync-seq-seed 0x10000
diffwords "tsngen --clk-hz 2000000" --clk-hz 2000000
rm -rf "$T"
