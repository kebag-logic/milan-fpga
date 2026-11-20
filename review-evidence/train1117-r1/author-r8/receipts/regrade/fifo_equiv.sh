#!/bin/bash
# fifo_equiv.sh OUT: cdc_pair_fifo's default branch (DIST_RAM_P = 0) at p11 against the candidate's module, with Yosys
# (RULING-1118c item 5), at each parameter set a default-branch instance takes (48/3 the I2S and AES3 FIFOs, 48/4 the
# I2S playback, 52/3 the TDM capture, 192/2 the slave TDM render's 8 slots): (1) sequential equivalence of the two
# designs, memories mapped to flops (equiv_make, equiv_induct, equiv_status -assert); (2) synth_xilinx's cell counts
# for each, the inference (LUT RAM or block RAM, flops). Prints each verdict.
set -u
O=$1; mkdir -p $O; P=<scratch>/p11
git -C $P show c8ff391a:hdl/common/cdc_pair_fifo.sv | sed 's/^module cdc_pair_fifo/module gold_fifo/' > $O/gold.sv
sed 's/^module cdc_pair_fifo/module gate_fifo/' $P/hdl/common/cdc_pair_fifo.sv > $O/gate.sv
rc=0
for pw in "48 3" "48 4" "52 3" "192 2"; do
  set -- $pw; W=$1 L=$2; tag=w${W}l${L}
  cat > $O/eq-$tag.ys <<EOF
read_verilog -sv $O/gold.sv
read_verilog -sv $O/gate.sv
chparam -set WIDTH $W -set LOG2D $L gold_fifo
chparam -set WIDTH $W -set LOG2D $L gate_fifo
proc; opt_clean; memory -nomap; memory_map; opt -full; flatten
rename gold_fifo gold
rename gate_fifo gate
equiv_make gold gate equiv
hierarchy -top equiv
equiv_simple -seq 5
equiv_induct -seq 5
equiv_status -assert
EOF
  if yosys -q -l $O/eq-$tag.log -s $O/eq-$tag.ys > /dev/null 2>&1; then v=EQUIVALENT; else v="NOT PROVEN"; rc=1; fi
  echo "$tag equivalence: $v ($(grep -o 'Found [0-9]* \$equiv cells.*' $O/eq-$tag.log | head -1; grep -o 'Of those cells [0-9]* are proven and [0-9]* are unproven' $O/eq-$tag.log | tail -1))"
  for d in gold gate; do
    yosys -q -l $O/syn-$d-$tag.log -p "read_verilog -sv $O/$d.sv; chparam -set WIDTH $W -set LOG2D $L ${d}_fifo; synth_xilinx -top ${d}_fifo -family xc7; stat" > /dev/null 2>&1
  done
  g=$(awk '/Number of cells/{f=1} f && /\$_|RAM|LUT|FD|CARRY|MUX/ {printf "%s:%s ", $2, $1} /^$/{if(f)exit}' $O/syn-gold-$tag.log)
  t=$(awk '/Number of cells/{f=1} f && /\$_|RAM|LUT|FD|CARRY|MUX/ {printf "%s:%s ", $2, $1} /^$/{if(f)exit}' $O/syn-gate-$tag.log)
  cg=$(grep -E '^ +[0-9]+ +(RAM|LUT|FD|CARRY|MUX)' $O/syn-gold-$tag.log | sort -k2 | tr -s ' ' | tr '\n' ',')
  ct=$(grep -E '^ +[0-9]+ +(RAM|LUT|FD|CARRY|MUX)' $O/syn-gate-$tag.log | sort -k2 | tr -s ' ' | tr '\n' ',')
  [ "$cg" = "$ct" ] && s=IDENTICAL || { s=DIFFER; rc=1; }
  echo "$tag synth_xilinx cells: $s; candidate [$cg] p11 [$ct]"
done
exit $rc
