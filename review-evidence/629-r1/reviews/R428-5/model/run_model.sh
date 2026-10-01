#!/bin/sh
# Run every section of the reviewer model; one output and rc file per section.
set -u
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$here/out"
for s in formula random spread medians counter servoleg meter steploop; do
  python3 "$here/r428_5_model.py" "$s" > "$here/out/$s.out" 2>&1
  echo $? > "$here/out/$s.rc"
done
