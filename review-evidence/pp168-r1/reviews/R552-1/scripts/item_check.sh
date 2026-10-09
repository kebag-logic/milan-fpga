#!/usr/bin/env bash
# For each published item patch: apply to a base archive, compare every hdl/ file hash with that item's inputs.json.
set -u
P=$REVIEWS/pp168-r552-1-packet; E=$P/scratch/evidence; R=$REVIEWS/r552-1-pp168
for i in LD1 LD2 LD3 TD1 VLAN guard; do
  d=$P/scratch/items/$i; rm -rf "$d"; mkdir -p "$d"
  git -C $R archive 09e357fb4bf3d35c8a9deba9a787e13f74d08c83 hdl | tar -x -C "$d"
  (cd "$d" && git apply --whitespace=nowarn "$E/item-$i.patch") || { echo "$i: patch does not apply"; continue; }
  python3 -I - "$d" "$E/round2-recovery/area/$i/inputs.json" "$i" <<'PY'
import hashlib, json, sys, pathlib
d, j, item = pathlib.Path(sys.argv[1]), json.load(open(sys.argv[2])), sys.argv[3]
bad = [k for k, v in j.items() if hashlib.sha256((d / k).read_bytes()).hexdigest() != v]
files = sorted(str(p.relative_to(d)) for p in d.rglob('*') if p.is_file())
extra = [f for f in files if f not in j]
print(f"{item}: {len(j)} inputs, {len(bad)} mismatches {bad[:3]}, extra files {extra[:3]}")
PY
  echo "   touched: $(grep '^+++ ' $E/item-$i.patch | sed 's#+++ b/##' | tr '\n' ' ')"
done
