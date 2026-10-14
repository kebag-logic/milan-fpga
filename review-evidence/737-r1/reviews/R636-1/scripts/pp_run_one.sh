#!/bin/bash
# $1 = copy dir, $2 = shard spec or "full", $3 = output dir
cd "$1" || exit 9
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH VERILATOR_JOBS=3 PYTHONDONTWRITEBYTECODE=1
start=$(date +%s)
if [ "$2" = full ]; then
  python3 scripts/ci_make_cases.py --suite pp_shadow --jobs 1 --receipt "$3/full.json" > "$3/full.log" 2>&1; rc=$?
else
  i=${2%/*}; python3 scripts/ci_make_cases.py --suite pp_shadow --jobs 1 --shard "$2" --receipt "$3/leg-$i.json" > "$3/leg-$i.log" 2>&1; rc=$?
fi
echo "$rc $(( $(date +%s) - start ))" > "$3/$(echo $2 | tr / _).rc"
