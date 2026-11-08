#!/bin/bash
# Mutation-driver error paths with one-plant registries, at the exact head and at the base 70936b77.
# usage: mutation_errors.sh TAG COMMIT PLANT_JSON_FILTER
#   TAG head-noarm   : head, wire plant with its "arm" removed       -> expect ERROR "unknown mutation arm: wire"
#   TAG head-bogus   : head, acmp.h header plant with arm "bogus"    -> expect ERROR "unknown mutation arm: bogus"
#   TAG base-wire    : base driver, both head wire plants             -> expect ERROR (no src/wire.c)
#   TAG base-bogus   : base driver, acmp.h header plant arm "bogus"  -> pre-change behaviour (campaign stops)
set -u; . "$(dirname "$0")/env.sh"
TAG=$1 COMMIT=$2 MODE=$3
O=$RCP/mutation-errors/$TAG; D=$SCR/mutation-errors/$TAG; mkdir -p "$O"
tree "$COMMIT" "$D/src"
python3 -I - "$REPO/tests/mutations.json" "$D/src/tests/mutations.json" "$MODE" <<'PY'
import json, sys
plants = json.load(open(sys.argv[1])); mode = sys.argv[3]
if mode == 'noarm':
    p = [m for m in plants if m['name'] == 'wire-put-be-skips-an-odd-field-first-byte']
    for k in p[0]['kills']: k.pop('arm')
elif mode == 'bogus':
    p = [m for m in plants if m['name'] == 'acmp-header-cdl-84']
    for k in p[0]['kills']: k['arm'] = 'bogus'
elif mode == 'wire':
    p = [m for m in plants if m['name'].startswith('wire-put-be')]
json.dump(p, open(sys.argv[2], 'w'), indent=2)
print(json.dumps(p)[:400])
PY
# The base tree has no W1; the wire plants' kill needs it, so base-wire also takes the head test file and header.
if [ "$MODE" = wire ]; then cp "$REPO/tests/test_acmp.cpp" "$D/src/tests/"; cp "$REPO/include/wire.h" "$D/src/include/"; fi
rm -rf "$D/work"
timeout 900 python3 "$D/src/scripts/mutation.py" --work "$D/work" --jobs 2 > "$O/run.log" 2>&1; rc=$?
if [ -f "$D/work/results.json" ]; then
  python3 -I -c 'import json,sys; [print(x["name"], x["status"], repr(x.get("error",""))[:200]) for x in json.load(open(sys.argv[1]))]' "$D/work/results.json" > "$O/results.txt"
else echo "no results.json" > "$O/results.txt"; fi
echo "$TAG rc=$rc $(tr '\n' ' ' < "$O/results.txt") last: $(grep -E 'Error|Traceback' "$O/run.log" | tail -1)" | tee "$O/result.txt"
