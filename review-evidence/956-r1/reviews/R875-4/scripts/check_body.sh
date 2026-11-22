#!/bin/sh
# Usage: check_body.sh <packet-dir> <clone-dir>
# Re-derives the PR body's limitation figures from the published author-r2 receipts.
set -eu
P=$1; C=$2; R=$P/receipts
echo "== head"; git -C "$C" rev-parse HEAD 'HEAD^{tree}'; git -C "$C" status --porcelain | wc -l
python3 -I -c "import json,sys;d=json.load(open(sys.argv[1]));print('live PR head',d['headRefOid'],'draft',d['isDraft'],'updated',d['updatedAt'])" "$P/pr958.json"
echo "== receipt sha256 against evidence MANIFEST.json"
python3 -I - "$R" <<'PY'
import json,hashlib,sys,os
r=sys.argv[1]; m={e['file']:e['published_sha256'] for e in json.load(open(os.path.join(r,'MANIFEST.json')))}
for n in ['cpu-1x1-legs-0d80f0ed-vs-b4a1dde2.md','cpu-8x8-1if-legs-0d80f0ed-vs-b4a1dde2.md','rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt']:
    h=hashlib.sha256(open(os.path.join(r,n),'rb').read()).hexdigest()
    print(n, 'MATCH' if m.get('author-r2/receipts/'+n)==h else 'MISMATCH', h)
PY
echo "== rom (receipt)"; grep -n -E "POINT 8x8-if1|128 B left|b4a1dde2: 139136" "$R/rom-ledger-images-0d80f0ed-vs-b4a1dde2.txt"
for f in cpu-1x1-legs-0d80f0ed-vs-b4a1dde2.md cpu-8x8-1if-legs-0d80f0ed-vs-b4a1dde2.md; do
  echo "== $f: named costs"; grep -E "^\| (centisecond|item.acmp_declined|record.srp|record.maap|build_one) \|" "$R/$f" | sort -u -t'|' -k2,7 | cut -d'|' -f2-7
  echo "== $f: every stated-cost row whose head rule equals its statement (nonzero)"
  awk -F'|' '/\| within \|/ {a=$5;b=$6;gsub(/ /,"",a);gsub(/ /,"",b); if (a==b && a!="0") print $2"|"$4"|"a"|"b}' "$R/$f" | sort -u
  echo "== $f: compare-long"; grep -E "^item.aecp_long|exceeded|head rows|^probes|^misses" "$R/$f"
done
echo "== live body: limitation and status lines naming the costs"
grep -n -E "acmp_declined|record\.srp|record\.maap|centisecond|128 bytes|139,136|Internal cleared|External reviewer|each finding above|112 B" "$P/pr958-body.md"
