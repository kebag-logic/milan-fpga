#!/usr/bin/env bash
# PNG-vs-SVG render identity, top port list vs base, stale/diff-check, clone integrity.
# Read-only on the clone. Usage: png_ports_integrity.sh <clone> <packet-dir>
set -u
C=$1; PKT=$2; R=$PKT/receipts; P=$PKT/scratch/png; mkdir -p "$P"
BASE=008edbbf486598ae237414273d75e385cf0e1a56; HEAD=2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f
cd "$C" || exit 1
{ rsvg-convert --version | sed -n 1p
  for n in 20-rtl-dataflow 21-integration-faces 22-aecp-descriptor-fetch 23-bringup-decision 24-adp-acmp-states; do
    git cat-file blob "$HEAD:docs/diagrams/$n.png" > "$P/head-$n.png"
    git cat-file blob "cc077a6ffe20585d20b116f008e07189ba1bb7f8:docs/diagrams/$n.png" > "$P/r1b-$n.png"
    w=$(python3 -c "import struct,sys;b=open(sys.argv[1],'rb').read(24);print(struct.unpack('>I',b[16:20])[0])" "$P/head-$n.png")
    h=$(python3 -c "import struct,sys;b=open(sys.argv[1],'rb').read(24);print(struct.unpack('>I',b[20:24])[0])" "$P/head-$n.png")
    git cat-file blob "$HEAD:docs/diagrams/$n.svg" > "$P/head-$n.svg"
    rsvg-convert -w "$w" -o "$P/render-$n.png" "$P/head-$n.svg"
    a=$(sha256sum < "$P/head-$n.png" | cut -c1-64); b=$(sha256sum < "$P/render-$n.png" | cut -c1-64); o=$(sha256sum < "$P/r1b-$n.png" | cut -c1-64)
    echo "$n ${w}x${h} committed=$a fresh_render=$b $([ "$a" = "$b" ] && echo MATCH || echo DIFF) changed_since_cc077a6f=$([ "$a" = "$o" ] && echo no || echo yes)"
  done; } > "$R/png-render-compare.txt" 2>&1
ports(){ git show "$1:hdl/top/protocol_processor_top.sv" | awk '/^module protocol_processor_top/,/^\);/' | grep -Eo '^\s*(input|output|inout)\s+(wire|logic)?\s*(\[[^]]*\])?\s*[A-Za-z_0-9]+' | awk '{print $NF}'; }
ports $BASE > "$P/p0"; ports $HEAD > "$P/p1"
{ echo "base ports: $(wc -l < "$P/p0")  head ports: $(wc -l < "$P/p1")"
  diff "$P/p0" "$P/p1" && echo "port list identical (names, order)"
  git show $BASE:hdl/top/protocol_processor_top.sv | sed -n 170,700p > "$P/b"; git show $HEAD:hdl/top/protocol_processor_top.sv | sed -n 170,700p > "$P/h"
  cmp "$P/b" "$P/h" && echo "port block lines 170-700 byte-identical to base"; } > "$R/top-port-list.txt" 2>&1
{ make stale; echo "make stale rc=$?"; git diff --check $BASE $HEAD; echo "diff --check base..head rc=$?"
  echo "files changed cc077a6f..head:"; git diff --stat cc077a6ffe20585d20b116f008e07189ba1bb7f8 $HEAD | cat; } > "$R/stale-diffcheck.log" 2>&1
{ echo "HEAD $(git rev-parse HEAD)"; echo "tree $(git rev-parse 'HEAD^{tree}')"; echo "index-tree $(git write-tree)"
  echo "status-porcelain-ignored-lines $(git status --porcelain --ignored | wc -l)"
  echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l); .gitmodules present: $([ -f .gitmodules ] && echo yes || echo no)"
  git diff --quiet HEAD && echo "worktree == HEAD (tracked bytes and modes)"; } > "$R/clone-integrity.txt" 2>&1
cat "$R/png-render-compare.txt" "$R/top-port-list.txt" "$R/stale-diffcheck.log" "$R/clone-integrity.txt"
