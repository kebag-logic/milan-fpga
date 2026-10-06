#!/bin/sh
# Plant single defects in scratch copies of the findings page and receipts and
# require recompute.py to fail on each. Usage: mutate_probe.sh <doc> <evidence dir> <scratch>
set -u
doc=$1; ev=$2; s=$3
mkdir -p "$s/mut"
run() { # name file-to-use evdir
  python3 "$(dirname "$0")/recompute.py" "$2" "$3" > "$s/mut/$1.log" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "KILLED $1 rc=$rc $(grep -m1 'CHECK FAIL' "$s/mut/$1.log")"; else echo "SURVIVED $1"; fi
}
sed 's/| 034 | 1 | 0 | 78 | -544469385 |/| 034 | 1 | 0 | 78 | -544469384 |/' "$doc" > "$s/mut/m1.md"; run step_value "$s/mut/m1.md" "$ev"
sed 's/| dut | STREAM_INPUT | 0 | SEQ_NUM_MISMATCH | 0 | 0 | 0 |/| dut | STREAM_INPUT | 0 | SEQ_NUM_MISMATCH | 0 | 1 | 1 |/' "$doc" > "$s/mut/m2.md"; run counter_row "$s/mut/m2.md" "$ev"
sed 's/^| 124999 | 61 |$/| 124999 | 60 |/' "$doc" > "$s/mut/m3.md"; run histogram "$s/mut/m3.md" "$ev"
sed 's/| soak-087 | 4355.162 | 0 | 4 | 4 |/| soak-087 | 4355.162 | 0 | 4 | 3 |/' "$doc" > "$s/mut/m4.md"; run soak_row "$s/mut/m4.md" "$ev"
# evidence-side mutation: one EARLY count flipped in a copy of the receipts
rm -rf "$s/mut/ev"; cp -r "$ev" "$s/mut/ev"
python3 - "$s/mut/ev/start-008.json" <<'PY'
import json,sys; p=sys.argv[1]; d=json.load(open(p)); d['early']=1; json.dump(d,open(p,'w'))
PY
run evidence_early "$doc" "$s/mut/ev"
# evidence-side: raise one error counter in the last soak checkpoint payload
rm -rf "$s/mut/ev2"; cp -r "$ev" "$s/mut/ev2"
python3 - "$s/mut/ev2/counters-soak-100.jsonl" <<'PY'
import json,sys; p=sys.argv[1]; rows=[json.loads(l) for l in open(p)]
for r in rows:
    if r['role']=='peer' and r['descriptor_type']==5 and r['descriptor_index']==0:
        b=bytearray.fromhex(r['payload']); off=8+4*10; b[off+3]=1; r['payload']=b.hex()
open(p,'w').write(''.join(json.dumps(r)+'\n' for r in rows))
PY
run evidence_early_soak "$doc" "$s/mut/ev2"
