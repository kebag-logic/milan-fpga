#!/usr/bin/env bash
# Planted faults for render-wavedrom.py's svg_margin, each on a fresh scratch copy of
# docs/ and scripts/. Usage: probe_margin.sh <clone> <scratch> (python3 must import wavedrom 2.0.3.post3)
set -u
clone=$1 scratch=$2
fresh() { rm -rf "$scratch/m"; mkdir -p "$scratch/m"; cp -r "$clone/docs" "$clone/scripts" "$scratch/m/"; }
run() { (cd "$scratch/m" && python3 scripts/render-wavedrom.py --check 2>&1 | tail -1; echo "rc=${PIPESTATUS[0]}"); }
f=docs/architecture/02_interfaces.md
fresh; echo "== control: unmodified copy"; run
fresh; sed -i '0,/ "config": {"svg_margin": 40},/{/ "config": {"svg_margin": 40},/d}' "$scratch/m/$f"; echo "== TX margin removed"; run
fresh; sed -i 's/"svg_margin": 40}/"svg_margin": 39}/' "$scratch/m/$f"; echo "== both margins 40 -> 39"; run
for bad in -1 1.5 '"40"' true 'null'; do
  fresh; sed -i "0,/\"svg_margin\": 40}/s//\"svg_margin\": $bad}/" "$scratch/m/$f"; echo "== margin $bad"; run
done
fresh; sed -i '0,/"svg_margin": 40}/s//"svg_margin": 0}/' "$scratch/m/$f"
(cd "$scratch/m" && python3 scripts/render-wavedrom.py >/dev/null 2>&1)
git -C "$clone" show 80588cdc:docs/diagrams/wavedrom/fig-02-txwave.svg > "$scratch/r2-tx.svg"
python3 - "$scratch" <<'PY'
import sys,re
s=sys.argv[1]
new=open(f"{s}/m/docs/diagrams/wavedrom/fig-02-txwave.svg").read()
old=open(f"{s}/r2-tx.svg").read()
# margin 0 with the head captions: same geometry header as the round-2 render (captions differ)
hdr=lambda t: re.match(r'<svg[^>]*>',t).group(0)
print("== margin 0 header equals round-2 header:", hdr(new)==hdr(old), hdr(new)[:120])
PY
