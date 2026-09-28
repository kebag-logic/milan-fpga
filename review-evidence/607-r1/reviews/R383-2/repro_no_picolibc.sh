#!/bin/sh
# [R383] Model the hosted `elaborate` environment, which installs only
# sw/litex/litex_pins.txt (no pythondata-software-picolibc): shadow that one
# package with an import-failing stub and run (a) the 607 test file and (b)
# a pre-existing elaborating bank path for contrast.
# Usage: repro_no_picolibc.sh <tree> <stub dir> <litex python>
tree=$1; stub=$(cd "$2" && pwd); py=$3
cd "$tree" || exit 2
echo "== stub import check"
PYTHONPATH="$stub" "$py" -c "import pythondata_software_picolibc" 2>&1 | tail -1
echo "== 607 test file with picolibc hidden"
PYTHONPATH="$stub" PYTHONHASHSEED=0 "$py" -B sw/builder/test_clock_constraints.py > /tmp/r383-no-picolibc.log 2>&1
echo "rc=$?"
grep -E "^\[constraints\] shipping|ImportError|AssertionError" /tmp/r383-no-picolibc.log | head -5
echo "== same test file with picolibc visible"
PYTHONHASHSEED=0 "$py" -B sw/builder/test_clock_constraints.py > /tmp/r383-with-picolibc.log 2>&1
echo "rc=$?"; grep -c "^\[constraints\] shipping .* PASS" /tmp/r383-with-picolibc.log
rm -f /tmp/r383-no-picolibc.log /tmp/r383-with-picolibc.log
