#!/usr/bin/env bash
# Disposable mutation probes: each must turn its check red. Usage: mutation_probes.sh <findings.md> <packet-root> <scratch>
set -u
F=$1; P=$2; S=$3
rm -rf "$S/mut" && mkdir -p "$S/mut"
probe() { name=$1; shift; "$@" >/dev/null 2>&1; rc=$?; [ $rc -ne 0 ] && echo "$name: red (rc=$rc) KILLED" || echo "$name: green (rc=0) SURVIVED"; }
# M0 control: unmodified page and packet stay green
python3 scripts/verify_b4_hashes.py "$F" "$P" >/dev/null 2>&1; echo "M0 control unmodified: rc=$?"
# M1 one table hash altered
sed 's/a9d5aae77fddcdf0fb50fc8dedf2f54a9ab914c5bfdc63a88a14d3d7249110f8/a9d5aae77fddcdf0fb50fc8dedf2f54a9ab914c5bfdc63a88a14d3d7249110f9/' "$F" > "$S/mut/m1.md"
probe "M1 run-1.log hash altered" python3 scripts/verify_b4_hashes.py "$S/mut/m1.md" "$P"
# M2 a redacted dump dropped from the declared list
grep -v '^- `run-2.entity.json`: ' "$F" > "$S/mut/m2.md"
probe "M2 run-2 redaction mapping undeclared" python3 scripts/verify_b4_hashes.py "$S/mut/m2.md" "$P"
# M3 published dump byte changed
cp -r "$P" "$S/mut/pkt3"; printf ' ' >> "$S/mut/pkt3/author/run-3.entity.json"
probe "M3 published run-3 dump byte appended" python3 scripts/verify_b4_hashes.py "$F" "$S/mut/pkt3"
# M4 summarize.py: one run's compatibility flags reduced to IEEE17221 only
cp -r "$P/author" "$S/mut/a4"; python3 - "$S/mut/a4/run-2.entity.json" <<'PY'
import json,sys; p=sys.argv[1]; j=json.load(open(p)); j["compatibility_flags"]=["IEEE17221"]; open(p,"w").write(json.dumps(j))
PY
probe "M4 summarize: run-2 Milan flag removed" python3 -I "$S/mut/a4/tools/summarize.py"
# M5 summarize.py: CRF Stream Input 1 counters dropped from one run's static? (dynamic excluded -> expected to survive)
cp -r "$P/author" "$S/mut/a5"; python3 - "$S/mut/a5/run-1.entity.json" <<'PY'
import json,sys; p=sys.argv[1]; j=json.load(open(p))
d=j["entity_model"]["entity_descriptor"]["configuration_descriptors"]
d=d[0] if isinstance(d,list) else d
d["stream_input_descriptors"][1]["dynamic"]["counters"]={}
open(p,"w").write(json.dumps(j))
PY
probe "M5 summarize: run-1 CRF counters emptied (dynamic; excluded by design)" python3 -I "$S/mut/a5/tools/summarize.py"
