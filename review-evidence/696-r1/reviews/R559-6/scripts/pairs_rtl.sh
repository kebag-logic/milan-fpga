#!/bin/bash
# Cross-check the first-draw model against the head RTL (200 random stations plus the
# q3 kernel pair), show the q3 identical claim, and confirm the head identical-block pair.
# Usage: pairs_rtl.sh <repo> <work> <scripts> <receipts>; needs VERILATOR (pinned 5.050).
set -u; R=$1; W=$2; S=$3; O=$4; mkdir -p $W
sed "s/32'h1040_0000, 32'h0000_0081/32'h1040_0000, 32'h0000_0080/" $R/hdl/ieee1722/maap/KL_maap.sv > $W/q3.sv
for v in head q3; do src=$([ $v = head ] && echo $R/hdl/ieee1722/maap/KL_maap.sv || echo $W/q3.sv)
  $VERILATOR --cc --exe --build -j 4 --top-module KL_maap -GCLK_FREQ_HZ_P=10000 -Wno-fatal -Wno-lint -Wno-style \
    -Mdir $W/fo_$v $src $S/first_offsets.cpp -o first_offsets >/dev/null 2>&1 || exit 2; done
{ python3 -I $S/q3_pair.py $W/q3.sv; python3 -I $S/q3_pair.py $R/hdl/ieee1722/maap/KL_maap.sv; } > $O/q3_pair.log
python3 -I -c "
import random; r=random.Random(696)
for _ in range(200): print('%012x %08x'%(0x020000000000|r.getrandbits(32), r.getrandbits(32)))" > $W/xval.txt
awk '/^pair/{print $2" 00000000"; print $3" 00000000"}' $O/q3_pair.log >> $W/xval.txt
$W/fo_head/first_offsets < $W/xval.txt > $W/rtl.txt
python3 -I $S/q3_pair.py $R/hdl/ieee1722/maap/KL_maap.sv $W/xval.txt > $W/model.txt
{ cmp -s $W/rtl.txt $W/model.txt && echo "MODEL==RTL head: $(wc -l < $W/xval.txt) stations" || echo "MODEL!=RTL";
  echo "q3 on the q3 kernel pair:"; $W/fo_q3/first_offsets < $W/xval.txt | tail -2
  echo "head on the same pair:"; tail -2 $W/rtl.txt; } > $O/xval.log
python3 -I $S/identical_pair.py $R/hdl/ieee1722/maap/KL_maap.sv $W/ident.txt > $O/identical_pair.log
$W/fo_head/first_offsets < $W/ident.txt >> $O/identical_pair.log
