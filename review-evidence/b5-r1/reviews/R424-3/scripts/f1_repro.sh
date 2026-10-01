#!/usr/bin/env bash
# Reproduce the B5 page's figure steps (117_AUDIO_CONTINUITY.md:446-456) from the
# public archive alone. usage: f1_repro.sh <archive review-evidence/b5-r1 dir> <work dir>
set -u
src=$1; work=$2
rm -rf "$work"; mkdir -p "$work"
cp -a "$src/author" "$src/author-r2" "$src/author-r3" "$work/"
cd "$work/author-r2/receipts" || exit 1
echo "== published files"
sha256sum a-long-reads.u16 a-long-reads.u16.gz
echo "== NOTE command lines"; grep -n "gunzip" a-long-reads.NOTE.md
echo "== gunzip -k (without -f), masked copy present"; gunzip -k a-long-reads.u16.gz; echo "rc=$?"
echo "== page step 1: gunzip -kf"; gunzip -kf a-long-reads.u16.gz; echo "rc=$?"
sha256sum a-long-reads.u16; stat -c '%s bytes' a-long-reads.u16
cd "$work" || exit 1
echo "== page step 2: b5_attrib.py figures <lane packet> <receipts>"
python3 -I author-r2/tools/b5_attrib.py figures author author-r2/receipts > attrib_out.txt; echo "rc=$?"
sha256sum attrib_out.txt author-r2/receipts/attribution.txt
cmp attrib_out.txt author-r2/receipts/attribution.txt && echo "attribution.txt: IDENTICAL"
echo "== page step 3: b5_round3.py figures <lane packet> <receipts>"
python3 -I author-r3/tools/b5_round3.py figures author author-r2/receipts > r3_out.txt; echo "rc=$?"
sha256sum r3_out.txt author-r3/receipts/round3_figures.txt
cmp r3_out.txt author-r3/receipts/round3_figures.txt && echo "round3_figures.txt: IDENTICAL"
echo "== negative control: the masked copy is refused by the tool's hash pin"
mkdir -p masked; cp author-r2/receipts/a-long-reads.json masked/; cp "$src/author-r2/receipts/a-long-reads.u16" masked/
python3 -I author-r2/tools/b5_attrib.py figures author masked > /dev/null 2> masked_err.txt; echo "rc=$? (nonzero expected)"; tail -1 masked_err.txt
echo "== tool hashes"; sha256sum author-r2/tools/b5_attrib.py author-r2/tools/b5_records.py author-r3/tools/b5_round3.py
