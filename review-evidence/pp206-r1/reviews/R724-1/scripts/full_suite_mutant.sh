#!/usr/bin/env bash
# Plant one exact edit in a fresh archive of the head and run the full
# tb/pp_top suite. usage: full_suite_mutant.sh <clone> <out dir> <name> <old> <new> <verilator>
set -u
clone=$1; out=$2; name=$3; old=$4; new=$5; ver=$6
tree=$(mktemp -d)
git -C "$clone" archive e9272b5635e76bf12a69376d59fd21d059cae320 | tar -x -C "$tree"
python3 -I - "$tree/hdl/top/protocol_processor_top.sv" "$old" "$new" <<'PY'
import sys
from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text()
assert s.count(sys.argv[2]) == 1, "expected exactly one edit site"
p.write_text(s.replace(sys.argv[2], sys.argv[3]))
PY
make -C "$tree/tb/pp_top" run VERILATOR="$ver" > "$out/$name-full.log" 2>&1
echo $? > "$out/$name-full.rc"
rm -rf "$tree"
