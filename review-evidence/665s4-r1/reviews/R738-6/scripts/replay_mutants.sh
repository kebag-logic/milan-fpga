#!/bin/bash
# replay_mutants.sh CLONE WORK RECEIPTS: the author's mutant for each new check and the complete fixture, replanted here.
C=$1; W=$2; R=$3; mkdir -p "$W" "$R"
T=sw/firmware/ctrl/test
plant() { # name file old new
  local d=$W/$1; cp -a --reflink=auto "$C" "$d"
  python3 -I - "$d/$2" "$3" "$4" <<'EOF'
import sys,pathlib
p=pathlib.Path(sys.argv[1]); s=p.read_text(); o=s.replace(sys.argv[2],sys.argv[3])
assert s!=o, "anchor missing"
p.write_text(o)
EOF
  ( cd "$d" && python3 -B $T/ctrl_image_selftest.py --require-rv32 ) > "$R/$1.log" 2>&1; echo $? > "$R/$1.rc"
}
H='MAP_HEADERS = ("generated/csr.h", "generated/mem.h")'
plant csr-not-required $T/ctrl_plat_image.py "$H" 'MAP_HEADERS = ("generated/mem.h",)' &
plant mem-not-required $T/ctrl_plat_image.py "$H" 'MAP_HEADERS = ("generated/csr.h",)' &
plant lone-json-accepted $T/ctrl_plat_image.py '        if missing:' '        if len(missing) == 1:' &
plant fixture-json-only $T/ctrl_image_selftest.py 'flash_map(work / "maps/complete", 1, (MAP_CSR, MAP_MEM))' 'flash_map(work / "maps/complete", 1, ())' &
wait
for f in "$R"/*.rc; do n=$(basename "$f" .rc); printf '%s rc=%s plat_green=%s last=%s\n' "$n" "$(cat "$f")" "$(grep -c '^PASS: plat' "$R/$n.log")" "$(tail -1 "$R/$n.log" | cut -c1-130)"; done
