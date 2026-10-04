#!/bin/sh
# Fetch the five published parent enumerations (read-only, public) and recompute the
# available_index rates the README quotes. Needs an authenticated `gh` with read access.
. "$(dirname "$0")/env.sh"
set -eu
d="$SCRATCH/benchrec"; mkdir -p "$d"
get(){ gh api "repos/kebag-logic/milan-fpga/contents/$2?ref=$1" --jq .content | base64 -d > "$d/$3"; }
get 36c1ea1f500b158fcec54be3d1fc343b19ebc891 review-evidence/b6-r1/author/identity/adp-discover.jsonl b6.jsonl
get 897788f467071450462074655cbb87e1061bd525 review-evidence/629-b7-r1/author/identity/adp-discover.jsonl b7.jsonl
for v in identity identity-resume identity-postboot; do
  get 9c4de5ad2a8c843daf4e22e8041fcb38dcfcb741 review-evidence/629-b8-r1/author/$v/adp-discover.jsonl b8-$v.jsonl; done
{ echo "# sources (branch heads b6-review-evidence 36c1ea1f, 629-b7-review-evidence 897788f4, 629-b8-review-evidence 9c4de5ad)"
  (cd "$d" && sha256sum b6.jsonl b7.jsonl b8-identity.jsonl b8-identity-resume.jsonl b8-identity-postboot.jsonl)
  python3 - "$d" <<'PY'
import json, sys, datetime, os
d = sys.argv[1]
recs = []
for f in ["b6.jsonl", "b7.jsonl", "b8-identity.jsonl", "b8-identity-resume.jsonl", "b8-identity-postboot.jsonl"]:
    for line in open(os.path.join(d, f)):
        o = json.loads(line)
        if o["type"] == "adp":
            who = "processor" if o["entity_caps"].lower() == "0x0000c588" else "peer"
            recs.append((f, who, o["available_index"], o["t"], o["entity_caps"]))
for x in recs:
    print(x[0], x[1], x[2], datetime.datetime.fromtimestamp(x[3], datetime.timezone.utc).isoformat(timespec="seconds"), x[4])
for who in ("peer", "processor"):
    r = [x for x in recs if x[1] == who]
    for a, b in zip(r, r[1:]):
        di, dt = b[2] - a[2], b[3] - a[3]
        print(f"{who}: {a[0]} -> {b[0]}: {a[2]} -> {b[2]} over {dt:.1f} s:",
              f"{dt/di:.3f} s per increment" if di > 0 else "index fell (restart)")
PY
} > "$RCPT/bench-index-recompute.txt"
cat "$RCPT/bench-index-recompute.txt"
