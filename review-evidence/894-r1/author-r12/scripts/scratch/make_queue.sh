#!/bin/bash
# The final pass's gate queue at HEAD: round 11's lane-gate and workflow lines (r11/gates-out/queue-final.txt), its
# head and directories replaced by HEAD and round 12's, and the sweep spec for native-shards.py. usage: make_queue.sh HEAD
set -eu
H=$1 T=/data-2/milan/tmp/894-a773
mkdir -p $T/r12/gates-out
sed "s#6ec12ad789c79bf2f00d21b3777d9bc5430c8b0c#$H#g; s#$T/r11/#$T/r12/#g" $T/r11/gates-out/queue-final.txt > $T/r12/gates-out/queue-final.txt
python3 - "$H" <<'PY'
import json, sys
T = '/data-2/milan/tmp/894-a773'
s = json.load(open(f'{T}/r11/gates-out/sweep-spec.json'))
s['head'] = sys.argv[1]
s['commands'][0] = [c.replace(f'{T}/r11/gates-out/sweep-logs', f'{T}/r12/gates-out/sweep-logs') for c in s['commands'][0]]
json.dump(s, open(f'{T}/r12/gates-out/sweep-spec.json', 'w'))
PY
grep -c . $T/r12/gates-out/queue-final.txt; grep -c "$H" $T/r12/gates-out/queue-final.txt; grep -c 'r11' $T/r12/gates-out/queue-final.txt || true
