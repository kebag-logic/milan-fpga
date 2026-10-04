#!/bin/sh
# Convert KL_nvm_backend with sv2v at base and head and compare Yosys
# post-proc/opt statistics at the default and at N_NAME_P=128.
# Usage: rtl_equiv_stat.sh <scratch dir holding base/ and head/>
S=$1
sv2v --version
yosys -V
for t in base head; do
  sv2v "$S/$t/hdl/milan/KL_nvm_backend.sv" > "$S/$t.nvm.v" || exit 1
  for n in 99 128; do
    yosys -q -p "read_verilog $S/$t.nvm.v; chparam -set N_NAME_P $n KL_nvm_backend; hierarchy -top KL_nvm_backend; proc; opt -full; tee -q -o $S/$t.$n.stat stat -width" > "$S/$t.$n.ylog" 2>&1
    echo "$t N_NAME_P=$n yosys rc=$? stat_lines=$(wc -l < "$S/$t.$n.stat") cells=$(grep -m1 -iE '^ *[0-9]+ +cells|cells' "$S/$t.$n.stat" | tr -s ' ')"
  done
done
for n in 99 128; do cmp "$S/base.$n.stat" "$S/head.$n.stat" && echo "N_NAME_P=$n base/head statistics identical"; done
