#!/bin/sh
# Generated-image acceptance at the head: run.py --image at the bound capacity,
# then 128. Usage: 07_generated.sh 1|8 [--measure]  (images from 06_regen_images.sh)
# Optional MUTANT_FILE/MUTANT_OLD/MUTANT_NEW/MUTANT_TAG env plant one exact edit.
set -u; . "$(dirname "$0")/env.sh"
aaf=$1; shift; n=$([ "$aaf" = 1 ] && echo 1x1 || echo 8x8)
tag=generated-$n${1:+-measure}${MUTANT_TAG:+-$MUTANT_TAG}
t="$SCRATCH/$tag"; extract "$t/src"
if [ -n "${MUTANT_FILE:-}" ]; then
python3 - "$t/src/$MUTANT_FILE" "$MUTANT_OLD" "$MUTANT_NEW" <<'PY' || exit 3
import sys
p, o, n = sys.argv[1:4]; s = open(p).read(); assert s.count(o) == 1; open(p, "w").write(s.replace(o, n))
PY
fi
python3 "$t/src/tb/name_state/run.py" --root "$t/src" --verilator "$VERILATOR" --work "$t/work" \
  --image "$SCRATCH/images/$n.img.bin" --aaf "$aaf" "$@" > "$RCPT/$tag.log" 2>&1
echo $? > "$RCPT/$tag.rc"
