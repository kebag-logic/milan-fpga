#!/bin/sh
# Normal name-suite run at the exact head: both synthetic populations at the bound
# capacity (39, 107) and again at 128. Usage: 01_suite.sh [--measure]
set -u; . "$(dirname "$0")/env.sh"
tag=suite${1:+-measure}
t="$SCRATCH/$tag"; extract "$t/src"
python3 "$t/src/tb/name_state/run.py" --root "$t/src" --verilator "$VERILATOR" --work "$t/work" "$@" > "$RCPT/$tag.log" 2>&1
echo $? > "$RCPT/$tag.rc"
