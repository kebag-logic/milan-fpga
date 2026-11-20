#!/usr/bin/env bash
# rel_compare.sh <exportA> <exportB> [--plant]
# Loaded files (bios.bin, aem_desc.bin, gateware/*.init) must be byte-equal; the top Verilog
# must be equal once comments and each export's absolute root are removed.  rc 0 equal, 1 not.
# --plant: compare A against a copy of B with one bios.bin byte flipped; it must be refused.
set -u
A=$1 B=$2 rc=0
if [ "${3:-}" = --plant ]; then
  T=$(mktemp -d); cp -a "$B" "$T/ax7101"; B=$T/ax7101
  python3 -I -c 'import sys;p=sys.argv[1];d=bytearray(open(p,"rb").read());d[64]^=1;open(p,"wb").write(d)' "$B/software/bios/bios.bin"
  echo "PLANT one bios.bin byte flipped in a copy of B"
fi
for f in software/bios/bios.bin aem_desc.bin $(cd "$A" && find gateware -name '*.init' | sort); do
  a=$(sha256sum < "$A/$f" | cut -c1-64) b=$(sha256sum < "$B/$f" | cut -c1-64)
  [ "$a" = "$b" ] && v=EQUAL || { v=DIFFERS; rc=1; }
  echo "LOADED $f $a $b $v"
done
strip() { sed -e "s#$(cd "$(dirname "$1")/../../.." && pwd)#<root>#g" -e 's#//.*$##' "$1" | python3 -I -c 'import re,sys;print(re.sub(r"/\*.*?\*/","",sys.stdin.read(),flags=re.S))'; }
va=$(strip "$A/gateware/alinx_ax7101.v" | sha256sum | cut -c1-64) vb=$(strip "$B/gateware/alinx_ax7101.v" | sha256sum | cut -c1-64)
raw=$(cmp -s "$A/gateware/alinx_ax7101.v" "$B/gateware/alinx_ax7101.v" && echo identical || echo differs)
[ "$va" = "$vb" ] && v=EQUAL || { v=DIFFERS; rc=1; }
echo "VERILOG gateware/alinx_ax7101.v raw $raw; outside comments $va $vb $v"
echo "END rc=$rc"
exit $rc
