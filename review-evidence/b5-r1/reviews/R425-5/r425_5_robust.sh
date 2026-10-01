#!/bin/sh
# R425-5 robustness probes on fresh copies of the three packet directories.
# R1 skip step 1: the tools must refuse the masked record copy (non-zero rc), not print figures.
# R2 gunzip -k without -f beside the masked copy: must refuse (rc 2) and keep the masked copy.
# R3 run steps 2-3 from another working directory with absolute paths: same bytes.
set -u
SRC=$1; S=$2
W=$S/rob_R1; rm -rf "$W"; mkdir -p "$W"; cp -a "$SRC"/. "$W"/
(cd "$W" && python3 -B author-r2/tools/b5_attrib.py figures author author-r2/receipts >/dev/null 2>&1; echo "R1 b5_attrib on masked record: rc=$?"
           python3 -B author-r3/tools/b5_round3.py figures author author-r2/receipts >/dev/null 2>&1; echo "R1 b5_round3 on masked record: rc=$?")
W=$S/rob_R2; rm -rf "$W"; mkdir -p "$W"; cp -a "$SRC"/. "$W"/
(cd "$W/author-r2/receipts" && h0=$(sha256sum a-long-reads.u16 | cut -c1-16); gunzip -k a-long-reads.u16.gz 2>/dev/null </dev/null; rc=$?; h1=$(sha256sum a-long-reads.u16 | cut -c1-16); echo "R2 gunzip -k without -f: rc=$rc, masked copy kept: $([ "$h0" = "$h1" ] && echo yes || echo no)")
W=$S/rob_R3; rm -rf "$W"; mkdir -p "$W"; cp -a "$SRC"/. "$W"/
(cd "$W/author-r2/receipts" && gunzip -kf a-long-reads.u16.gz)
(cd /tmp && python3 -B "$W/author-r2/tools/b5_attrib.py" figures "$W/author" "$W/author-r2/receipts" | cmp -s - "$W/author-r2/receipts/attribution.txt"; echo "R3 b5_attrib from another cwd: cmp=$?"
 python3 -B "$W/author-r3/tools/b5_round3.py" figures "$W/author" "$W/author-r2/receipts" | cmp -s - "$W/author-r3/receipts/round3_figures.txt"; echo "R3 b5_round3 from another cwd: cmp=$?")
