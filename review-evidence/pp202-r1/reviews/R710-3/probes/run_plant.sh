#!/usr/bin/env bash
# Reviewer probe: run one bench of a disposable copy of the reviewed tree,
# optionally with one planted `old|||new` substitution (\n allowed in both
# halves) in one source file. Usage:
#   run_plant.sh SRC_TREE WORK_DIR OUT_LOG VERILATOR TB_DIR "MAKE ARGS" [FILE SUB]
set -uo pipefail
SRC=$(realpath -m "$1") WORK=$(realpath -m "$2") OUT=$(realpath -m "$3") V=$4 TB=$5 MARGS=$6
FILE=${7:-} SUB=${8:+$(realpath "$8")}
rm -rf "$WORK"; mkdir -p "$WORK" "$(dirname "$OUT")"
cp -a "$SRC/hdl" "$SRC/tb" "$SRC/scripts" "$WORK/" 2>/dev/null
[ -f "$SRC/Makefile" ] && cp "$SRC/Makefile" "$WORK/"
if [ -n "$FILE" ]; then
  python3 -I - "$WORK/$FILE" "$SUB" <<'EOF' || { echo "PLANT-ANCHOR-FAIL" > "$OUT"; echo 99 > "$OUT.rc"; exit 0; }
import sys
f, p = sys.argv[1], sys.argv[2]
old, new = open(p).read().rstrip('\n').split('|||')
old = old.replace('\\n', '\n'); new = new.replace('\\n', '\n')
s = open(f).read()
assert s.count(old) == 1, ('anchor count', s.count(old))
open(f, 'w').write(s.replace(old, new))
EOF
fi
( cd "$WORK/$TB" && make VERILATOR="$V" $MARGS > "$OUT" 2>&1 ); echo $? > "$OUT.rc"
