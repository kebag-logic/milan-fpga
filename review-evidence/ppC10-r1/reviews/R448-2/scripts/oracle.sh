#!/usr/bin/env bash
# Independent oracle: the pre-PR method (one yosys per top, full read_verilog,
# hierarchy -check; proc; opt_clean) over the same planted tree, every top.
# usage: oracle.sh <pristine-tree> <scratch-root> <out-file> -- <kind> <arg> ...
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
src=$1 scr=$2 out=$3; shift 3; [ "${1-}" = "--" ] && shift
t=$(mktemp -d "$scr/oracle-XXXX"); cp -a "$src/." "$t/"
while [ "$#" -gt 0 ]; do python3 "$here/plant.py" "$t" "$1" "$2" >/dev/null || exit 9; shift 2; done
cd "$t"
tops=$(sed -n '/^tops=(/,/)/p' syn/yosys/run.sh | tr -d '()' | sed 's/tops=//' | tr -s ' \n' '\n' | grep -v '^$')
w=$t/w; mkdir -p "$w"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$w/all.v"
( cd hdl/aecp/ucode && python3 gen_ucode.py -o "$w/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 gen_ltn_rom.py -o "$w/ltn_rom.hex" >/dev/null 2>&1 || python3 gen_ltn_rom.py > /dev/null; cp ltn_rom.hex "$w/" 2>/dev/null || true )
cd "$w"
printf '%s\n' $tops | ORACLE_READ_FLAGS="${ORACLE_READ_FLAGS:-}" xargs -P 8 -I{} sh -c 'if yosys -q -p "read_verilog ${ORACLE_READ_FLAGS:-} all.v; hierarchy -check -top {}; proc; opt_clean" >/dev/null 2>&1; then echo "ORACLE OK   {}"; else echo "ORACLE FAIL {}"; fi' | sort -k3 > "$out"
rm -rf "$t"
grep -c 'ORACLE OK' "$out"; grep 'ORACLE FAIL' "$out"
