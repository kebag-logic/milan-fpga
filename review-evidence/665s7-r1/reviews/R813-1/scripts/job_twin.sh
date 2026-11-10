#!/bin/sh
# the twin and twin-plants recipes (tb/verilator/milan_dp/Makefile) on pre-built binaries in $2, output in $3
set -eu
cd "$1"; B="$2"; O="$3"; mkdir -p "$O"
plants() { awk -v v="$1" '$1==v && $2=="=" {on=1; $1=""; $2=""} on {line=$0; c=sub(/\\$/,"",line); printf "%s ", line; if (!c) exit}' Makefile; }
"$B/obj_twin_sp/Vmilan_dp_twin_sp" "$O/split.json" &
"$B/obj_twin_af/Vmilan_dp_twin_af" "$B/obj_twin_af/aemi.bin" "$O/fabric.json"
wait
python3 -B twin_compare.py "$O/fabric.json" "$O/split.json" --report "$O/report.json"
echo "twin compare rc=0"
python3 -B twin_compare.py "$O/fabric.json" "$O/split.json" --report "$O/report.json" --report-only > "$O/unplanted.txt"
n=0
for p in $(plants TWIN_PLANTS); do n=$((n+1))
  "$B/obj_twin_sp/Vmilan_dp_twin_sp" "$O/split-$p.json" --plant "$p"
  python3 -B twin_compare.py "$O/split.json" "$O/split-$p.json" --plant "$p" --self
  python3 -B twin_compare.py "$O/fabric.json" "$O/split-$p.json" --plant "$p" --baseline "$O/report.json"
done
for p in $(plants TWIN_CAPTURE_PLANTS); do n=$((n+1))
  python3 -B twin_compare.py "$O/fabric.json" "$O/split.json" --make-plant "$p" --out "$O/split-$p.json"
  python3 -B twin_compare.py "$O/split.json" "$O/split-$p.json" --plant "$p" --self
  python3 -B twin_compare.py "$O/fabric.json" "$O/split-$p.json" --plant "$p" --baseline "$O/report.json"
done
for p in $(plants TWIN_FABRIC_PLANTS); do n=$((n+1))
  python3 -B twin_compare.py "$O/fabric.json" "$O/split.json" --make-plant "$p" --out "$O/fabric-$p.json"
  python3 -B twin_compare.py "$O/fabric.json" "$O/fabric-$p.json" --plant "$p" --self
  python3 -B twin_compare.py "$O/fabric-$p.json" "$O/split.json" --plant "$p" --baseline "$O/report.json"
done
echo "twin-plants recipe rc=0, $n plants"
