#!/bin/sh
# Run the named sections of meter_rules_model_r5.py, one process each, into
# sections/<name>.out with its exit status in sections/<name>.rc. The full
# output, meter_rules_model_r5.out, is the sections concatenated in the
# model's own order (cat_model.sh), which is what "all" prints.
# Usage: sh run_model.sh <outdir> section...
set -u
here=$(cd "$(dirname "$0")" && pwd)
out=$1
shift
mkdir -p "$out"
for s in "$@"; do
    python3 "$here/meter_rules_model_r5.py" "$s" > "$out/$s.out" 2> "$out/$s.err"
    echo $? > "$out/$s.rc"
    echo "$s rc=$(cat "$out/$s.rc")"
done
