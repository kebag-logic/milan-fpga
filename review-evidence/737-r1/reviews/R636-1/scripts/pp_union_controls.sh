#!/bin/bash
# Production comparison of the pp_shadow full run against its four legs, then
# planted controls on disposable copies of the receipts. Args: <clone> <out-dir>
set -u
C=$1; O=$2; cd "$C"
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
python3 -I -c 'import sys,json; sys.path.insert(0,"scripts"); from ci_suite_pieces import inventory; print(json.dumps(inventory("pp_shadow")))' > "$O/inventory.json"
run() { echo "== $1"; shift; python3 scripts/ci_case_receipts.py --inventory "$O/inventory.json" --suite pp_shadow --head "$head" --tree "$tree" "$@"; echo "rc=$?"; }
run "real: four legs vs unsharded reference" --reference "$O/full.json" "$O"/leg-[0-3].json
P2=$O/planted; rm -rf "$P2"; mkdir -p "$P2"
cp -a "$O"/leg-*.json "$O"/leg-*.logs "$O"/full.json "$O"/full.logs "$P2"/
# 1: drop leg 3 entirely (its only case is absent from every leg)
run "planted: leg 3 receipt removed" --reference "$P2/full.json" "$P2"/leg-[0-2].json
# 2: drop the case from leg 3's results (claimed but not executed)
python3 -I - "$P2/leg-3.json" <<'PY'
import json,sys; p=sys.argv[1]; d=json.load(open(p)); d["results"]=[]; open(p+".dropped","w").write(json.dumps(d,sort_keys=True,separators=(",",":")))
PY
cp -a "$P2/leg-3.logs" "$P2/leg-3.json.logs" 2>/dev/null; mv "$P2/leg-3.json.dropped" "$P2/leg-3x.json"; cp -a "$P2/leg-3.logs" "$P2/leg-3x.logs"
run "planted: case dropped from its leg's results" --reference "$P2/full.json" "$P2"/leg-[0-2].json "$P2/leg-3x.json"
# 3: one checked-output byte changed in a leg (digest recomputed so only equality catches it)
python3 -I - "$P2" <<'PY'
import json,sys,hashlib,pathlib; d=pathlib.Path(sys.argv[1]); p=d/"leg-1.json"; r=json.loads(p.read_text())
case=r["results"][0]; lg=d/"leg-1.logs"/(hashlib.sha256(case["case"].encode()).hexdigest()+".log")
b=bytearray(lg.read_bytes()); i=b.find(b"PASS"); b[i:i+4]=b"PASs"; lg.write_bytes(b); case["output_sha256"]=hashlib.sha256(b).hexdigest()
p.write_text(json.dumps(r,sort_keys=True,separators=(",",":")))
PY
run "planted: changed checked output in leg 1" --reference "$P2/full.json" "$P2"/leg-0.json "$P2"/leg-1.json "$P2"/leg-2.json "$P2"/leg-3.json
# 4: duplicated leg
cp -a "$O"/leg-1.json "$O"/leg-1.logs "$P2"/ 
run "planted: leg 2 replaced by a second copy of leg 0" --reference "$P2/full.json" "$P2"/leg-0.json "$P2"/leg-1.json "$P2"/leg-0.json "$P2"/leg-3.json
# 5: wrong head
python3 scripts/ci_case_receipts.py --inventory "$O/inventory.json" --suite pp_shadow --head "$(printf 'a%.0s' $(seq 40))" --tree "$tree" "$O"/leg-[0-3].json; echo "== planted: wrong head rc=$?"
