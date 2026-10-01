#!/usr/bin/env bash
# Reproduce the page's read-record restore and figure steps from the public
# b5-review-evidence archive alone.  Usage: f1_repro.sh <archive b5-r1 dir> <empty work dir>
set -u
src=$1; work=$2
mkdir -p "$work" && cd "$work" || exit 2
cp -r "$src/author" author
mkdir receipts && cp "$src"/author-r2/receipts/* receipts/ 2>/dev/null
cp "$src/author-r2/tools/b5_attrib.py" "$src/author-r3/tools/b5_round3.py" .
echo "-- archive inputs"
sha256sum receipts/a-long-reads.u16 receipts/a-long-reads.u16.gz receipts/a-long-reads.json b5_attrib.py b5_round3.py
echo "-- gunzip -k with the masked copy present (expect refusal)"
( cd receipts && gunzip -k a-long-reads.u16.gz 2>&1; echo "rc=$?"; sha256sum a-long-reads.u16 )
echo "-- page step 1: gunzip -kf"
( cd receipts && gunzip -kf a-long-reads.u16.gz; echo "rc=$?"; sha256sum a-long-reads.u16; stat -c '%s bytes' a-long-reads.u16 )
echo "-- page step 2: b5_attrib.py figures author receipts"
python3 b5_attrib.py figures author receipts > attribution.txt; echo "rc=$?"
sha256sum attribution.txt "$src/author-r2/receipts/attribution.txt"
cmp attribution.txt "$src/author-r2/receipts/attribution.txt" && echo "attribution.txt: identical"
echo "-- page step 3: b5_round3.py figures author receipts"
python3 b5_round3.py figures author receipts > round3_figures.txt; echo "rc=$?"
sha256sum round3_figures.txt "$src/author-r3/receipts/round3_figures.txt"
cmp round3_figures.txt "$src/author-r3/receipts/round3_figures.txt" && echo "round3_figures.txt: identical"
echo "-- negative control: masked record (as published) through b5_attrib.py"
mkdir -p neg && cp -r receipts neg/ && cp "$src/author-r2/receipts/a-long-reads.u16" neg/receipts/a-long-reads.u16
python3 b5_attrib.py figures author neg/receipts > neg/attribution.txt 2>neg/err.txt; echo "rc=$?"
cmp -s neg/attribution.txt "$src/author-r2/receipts/attribution.txt" && echo "masked: identical (control did NOT bite)" || { echo "masked: differs (control bites)"; head -3 neg/err.txt; }
