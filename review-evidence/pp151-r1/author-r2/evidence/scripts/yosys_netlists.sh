#!/usr/bin/env bash
# yosys_netlists.sh <tree> <out-dir>: every syn/yosys/run.sh top at its defaults, and
# protocol_processor_top at extra stream shapes, each elaborated in a FRESH yosys as
# run.sh does (hierarchy -check; proc; opt_clean) and written with write_verilog
# -noattr -norename; then canon_netlist.py digests (line numbers masked, auto-indices
# ranked, lines sorted) of each, and sha256 of the two ROM images.


set -euo pipefail
export PATH=<scratch>/tools/bin:$PATH
tree=$1 out=$2; mkdir -p "$out"; cd "$tree"
tops=$(sed -n '/^tops=(/,/)/p' syn/yosys/run.sh | tr -d '()' | sed 's/tops=//' | tr -s ' \n' '\n' | grep -v '^$')
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$out/all.v"
( cd hdl/aecp/ucode && python3 -B gen_ucode.py -o "$out/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 -B gen_ltn_rom.py -o "$out/ltn_rom.hex" >/dev/null )
cd "$out"
: > jobs.txt
for t in $tops; do echo "$t|" >> jobs.txt; done
# the stream shapes shape_elab.sh calls legal, then the parent's five configs
# (sinks, sources, name entries, 50 MHz) as milan_datapath binds them
for s in 1:1 9:9 4:4 1:8 8:1 16:16 2:2 5:5 \
         5:5:55:50000000 5:5:87:50000000 2:1:29:50000000 2:2:39:50000000 9:9:107:50000000; do
  IFS=: read -r si so nm hz <<<"$s"
  echo "protocol_processor_top_${s//:/_}|chparam -set N_STREAM_IN_P $si -set N_STREAM_OUT_P $so${nm:+ -set DESC_NAME_ENTRIES_P $nm}${hz:+ -set CLK_HZ_P $hz} protocol_processor_top;" >> jobs.txt
done
one() {
  local name=${1%%|*} ch=${1#*|} top
  top=${name%%_[0-9]*}; [ "$ch" ] || top=$name
  yosys -q -p "read_verilog -defer all.v; $ch hierarchy -check -top $top; proc; opt_clean; write_verilog -noattr -norename nl_$name.v" > "log_$name.txt" 2>&1 || echo "FAIL $name"
}
export -f one
xargs -P 2 -I{} bash -c 'one "$@"' _ {} < jobs.txt
{ python3 -I <scratch>/scripts/canon_netlist.py nl_*.v; sha256sum ucode.hex ltn_rom.hex | awk '{print $2, $1}'; } | sort > canon.txt
wc -l < canon.txt
