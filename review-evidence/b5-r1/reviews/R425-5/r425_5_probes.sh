#!/bin/sh
# R425-5: disposable probes on a copy of the extracted packets.
# Usage: r425_5_probes.sh <extracted b5-r1 dir> <scratch dir>
# P1 perturb a-long summary.json (a value both tools read): outputs must differ.
# P2 perturb a-long events.jsonl (claimed unread): outputs must be identical.
# P3 flip one byte of the restored read record: sha256 must differ and outputs differ.
set -u
SRC=$1; S=$2
run() { # $1 label, $2 dir
  (cd "$2" && python3 -B author-r2/tools/b5_attrib.py figures author author-r2/receipts 2>/dev/null | cmp -s - author-r2/receipts/attribution.txt; a=$?
   python3 -B author-r3/tools/b5_round3.py figures author author-r2/receipts 2>/dev/null | cmp -s - author-r3/receipts/round3_figures.txt; b=$?
   echo "$1: attribution cmp=$a round3 cmp=$b (0 identical, 1 differs, 2 error)")
}
for p in P0 P1 P2 P3; do
  W=$S/probe_$p; rm -rf "$W"; mkdir -p "$W"; cp -a "$SRC"/. "$W"/
  (cd "$W/author-r2/receipts" && gunzip -kf a-long-reads.u16.gz)
  case $p in
    P1) python3 - "$W/author/summary/a-long/summary.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p))
c = d['continuity']
old = c['window_time']
c['window_time'] = [old[0], old[1] + 1.0]
print('continuity.window_time end bumped by 1.0 s')
json.dump(d, open(p, 'w'))
EOF
    ;;
    P2) printf '{"probe": "appended line"}\n' >> "$W/author/runs/a-long/events.jsonl"; echo "events.jsonl appended" ;;
    P3) python3 - "$W/author-r2/receipts/a-long-reads.u16" <<'EOF'
import sys
p = sys.argv[1]; b = bytearray(open(p, 'rb').read()); b[len(b)//2] ^= 0x01
open(p, 'wb').write(b); print('one byte flipped at', len(b)//2)
EOF
       (cd "$W/author-r2/receipts" && sha256sum a-long-reads.u16) ;;
  esac
  run "$p" "$W"
done
