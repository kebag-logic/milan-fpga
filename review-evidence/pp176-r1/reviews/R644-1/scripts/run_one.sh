#!/bin/sh
# Run one built suite binary in its own run directory, so concurrent runs do
# not share obj_dir/build_tally.txt or observed.json. Usage:
#   run_one.sh <tree-root> pp_top|aecp_cmds <mut> <outdir>
# mut is a number passed as +MUT=<n> (mux tree), or "none" for no plusarg.
set -u
tree=$1; suite=$2; mut=$3; out=$4
name=$(basename "$tree")-$suite-$mut
run=$out/run/$name
rm -rf "$run"; mkdir -p "$run/obj_dir"
plus=""; [ "$mut" != none ] && plus="+MUT=$mut"
case $suite in
  pp_top)
    ln -s "$tree/tb/pp_top/ucode.hex" "$run/ucode.hex"
    ln -s "$tree/tb/pp_top/ltn_rom.hex" "$run/ltn_rom.hex"
    (cd "$run" && timeout 3600 "$tree/tb/pp_top/obj_dir/Vpp_top_sim" $plus) \
      >"$out/$name.log" 2>&1
    echo $? >"$out/$name.rc"
    ;;
  aecp_cmds)
    for f in ucode.hex image.bin; do ln -s "$tree/tb/aecp_cmds/$f" "$run/$f"; done
    (cd "$run" && timeout 3600 "$tree/tb/aecp_cmds/obj_dir/Vaecp_cmds" "$run/obj_dir/observed.json" $plus \
      && cd "$tree/tb/aecp_cmds" && python3 -B check_observed.py "$run/obj_dir/observed.json") \
      >"$out/$name.log" 2>&1
    echo $? >"$out/$name.rc"
    ;;
esac
