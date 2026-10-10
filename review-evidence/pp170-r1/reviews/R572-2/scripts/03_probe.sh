#!/bin/sh
# Disposable fault probe: plant one exact edit in a pristine copy of the head,
# then run the unmodified name suite (bound capacity 39/107, then 128).
# Usage: 03_probe.sh NAME FILE OLD NEW   (OLD must occur exactly once)
set -u; . "$(dirname "$0")/env.sh"
name=$1 file=$2 old=$3 new=$4
t="$SCRATCH/probe-$name"; extract "$t/src"
python3 - "$t/src/$file" "$old" "$new" <<'PY' || { echo 3 > "$RCPT/probe-$name.rc"; exit 3; }
import sys
path, old, new = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(path).read()
assert text.count(old) == 1, f"anchor count {text.count(old)}"
open(path, "w").write(text.replace(old, new))
PY
( cd "$t/src" && git diff --no-index /dev/null /dev/null; diff -u "$SRC/$file" "$file" ) > "$RCPT/probe-$name.diff" 2>&1
python3 "$t/src/tb/name_state/run.py" --root "$t/src" --verilator "$VERILATOR" --work "$t/work" > "$RCPT/probe-$name.log" 2>&1
echo $? > "$RCPT/probe-$name.rc"
