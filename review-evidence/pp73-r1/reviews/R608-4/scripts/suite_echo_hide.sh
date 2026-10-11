#!/bin/sh
# R608-4: R608-3's echo-hide drift through the real tb/aecp_cmds suite.
# Usage: suite_echo_hide.sh SRC_TREE WORK_DIR VERILATOR VARIANT(plain|shared)
set -u
SRC=$1; W=$2; V=$3; VAR=$4
mkdir -p "$W" && cp -a "$SRC/." "$W/"
python3 -I - "$W" "$VAR" <<'PY'
import json, sys
from pathlib import Path
w, var = Path(sys.argv[1]), sys.argv[2]
g = w / "hdl/aecp/ucode/gen_ucode.py"
old = ("    u('BUILD_FLD', ra=3, fmt=FMT_D),             # flags                  @24\n"
       "    u('BUILD_FLD', ra=2, fmt=FMT_Q),             # acquired_controller_id @28\n"
       "    u('BUILD_FLD', ra=1, fmt=FMT_Q),             # locked_controller_id   @36\n")
s = g.read_text()
assert s.count(old) == 1
g.write_text(s.replace(old, "    u('NOP'),\n" * 3))
tp = w / "hdl/aecp/ucode/aecp_commands.json"
t = json.loads(tp.read_text())
t["echo_entries"].append("EAVL")
if var == "shared":
    t["shared_entries"]["EAVL"] = "probe"
tp.write_text(json.dumps(t, indent=2) + "\n")
PY
cd "$W/tb/aecp_cmds" && make VERILATOR="$V" run
