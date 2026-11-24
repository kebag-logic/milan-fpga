#!/bin/sh
# usage: txla_registrar_mutant.sh <clone>
# Runs the twin self-test as the Makefile does (python3 -B, from tb/verilator/milan_dp) at the clone's head
# (control), then with Table 10-4's txLA! row at twin_mrp.py emptied, so txLA! no longer takes a Registrar
# IN to LV, and reports each rc. The mutated file is restored from HEAD on exit (git checkout).
set -u
C=$1; F=tb/verilator/milan_dp/twin_mrp.py
cd "$C" || exit 2
trap 'git checkout -- "$F"' EXIT
git diff --quiet -- "$F" || { echo "dirty $F"; exit 2; }
n=$(grep -c '^    "txLA!": {"IN": "LV"},$' "$F")
echo "mutation sites: $n (expected 1)"
[ "$n" = 1 ] || exit 2
echo "--- control"; (cd tb/verilator/milan_dp && python3 -B twin_mrp.py --selftest); echo "rc=$?"
sed -i 's/^    "txLA!": {"IN": "LV"},$/    "txLA!": {},/' "$F"
git diff -- "$F" | sed -n '5,$p'
echo "--- mutant txla-registrar"; (cd tb/verilator/milan_dp && python3 -B twin_mrp.py --selftest); echo "rc=$?"
