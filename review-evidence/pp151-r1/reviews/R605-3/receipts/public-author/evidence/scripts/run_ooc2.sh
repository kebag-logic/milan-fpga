#!/usr/bin/env bash
# run_ooc2.sh: base and head OOC netlists of protocol_processor_top (the tree's own
# syn/ooc/protocol_processor_ooc.tcl, then a funcsim netlist), at the default shape and
# at 9x9; each Vivado run alone under the exclusive lock. Base is the exported base
# tree, head the lane at its head.
set -u
export PYTHONDONTWRITEBYTECODE=1
V=<vivado>/2026.1/Vivado/bin/vivado
D=<scratch>/viv/ooc
for shape in "${@:-default}"; do for side in base head; do
  tree=<scratch>/pristine; [ $side = head ] && tree=<lane>
  args=$tree; [ $shape = 9x9 ] && args="$tree 9 9"
  w=$D/$side-$shape; rm -rf $w; mkdir -p $w; cd $w
  start=$(date +%s)
  flock -x $VIVADO_LOCK $V -mode batch -nojournal -log ooc.log -source $D/ooc_netlist.tcl -tclargs $args > stdout.txt 2>&1; echo $? > rc
  echo $(( $(date +%s) - start )) > secs
  grep -v '^// Date' netlist.v | sed "s#$tree#TREE#g" | sha256sum | cut -d' ' -f1 > netlist.sha256
  stat -c %s netlist.v > netlist.size
  sha256sum ucode.hex ltn_rom.hex | cut -c1-16 | tr '\n' ' ' > roms
  echo "$side $shape rc=$(cat rc) secs=$(cat secs) size=$(cat netlist.size) sha=$(cat netlist.sha256) roms=$(cat roms)" | tee -a $D/summary.txt
done; done
