#!/usr/bin/env bash
# Default-shape netlist identity, base vs head, for every module that declares a guard.
# usage: netlist_identity.sh BASE_TREE HEAD_TREE OUTDIR BINDIR JOBS
# sv2v (from BINDIR) lowers each whole hdl/ tree once; Yosys elaborates each top at its
# defaults (hierarchy -check; proc; opt_clean, as syn/yosys/run.sh) and writes the netlist
# without attributes, so source line numbers cannot differ. Exit 0 = every pair identical.
set -uo pipefail
base=$1 head=$2 out=$3 bindir=$4 jobs=$5
export PATH="$bindir:$PATH"
mkdir -p "$out"
tops="KL_acmp_nvm_shadow KL_pp_acmp_listener KL_aecp_desc_store KL_aecp_engine KL_aecp_notify
KL_aecp_nvm_writer KL_aecp_resp_buf KL_aecp_ucpu KL_pp_nvm_port KL_pp_originator
KL_pp_release_merge KL_srp_encoder protocol_processor_top"
for side in base head; do
  tree=${!side}; w=$out/$side; mkdir -p "$w"
  ( cd "$tree" && sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) ) > "$w/all.v"
  ( cd "$tree/hdl/aecp/ucode" && python3 gen_ucode.py -o "$w/ucode.hex" >/dev/null )
  ( cd "$tree/hdl/acmp/rom" && python3 gen_ltn_rom.py -o "$w/ltn_rom.hex" >/dev/null )
done
sha256sum "$out"/base/*.hex "$out"/head/*.hex
echo "sv2v output diff (base -> head), changed lines only:"
diff "$out/base/all.v" "$out/head/all.v" | grep -E '^[<>]' | sed 's/^/  /'
one() {
  local side=$1 t=$2 w=$out/$1
  ( cd "$w" && yosys -q -p "read_verilog -defer all.v; hierarchy -check -top $t; proc; opt_clean; write_verilog -noattr $t.net.v" > "$t.log" 2>&1; echo $? > "$t.rc" )
}
export -f one; export out
for t in $tops; do printf '%s %s\n' base "$t" head "$t"; done | xargs -P "$jobs" -n 2 bash -c 'one "$0" "$1"'
rc=0
for t in $tops; do
  b=$(cat "$out/base/$t.rc") h=$(cat "$out/head/$t.rc")
  if [ "$b" != 0 ] || [ "$h" != 0 ]; then echo "ELAB FAIL $t base rc=$b head rc=$h"; rc=1; continue; fi
  sb=$(sha256sum < "$out/base/$t.net.v" | cut -c1-64) sh=$(sha256sum < "$out/head/$t.net.v" | cut -c1-64)
  if [ "$sb" = "$sh" ]; then echo "IDENTICAL $t $sb"; else echo "DIFFERS  $t base $sb head $sh"; rc=1; fi
done
exit $rc
