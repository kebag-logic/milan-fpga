#!/bin/sh
# Busy-predicate control (R348-1 F4): compile flash_test.cpp against the head flash.hpp and
# against a copy with the busy term deleted from the write refusal; the named control must fail.
# Usage: flash_busy_mutant.sh <repo> <scratch-dir>
R=$1; D=$2; mkdir -p $D/orig $D/mut
cp $R/tb/verilator/fw_service_budget/flash.hpp $R/tb/verilator/fw_service_budget/flash_test.cpp $D/orig/
cp $D/orig/* $D/mut/
python3 - "$D/mut/flash.hpp" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
old="if (!wel_ || cycle < busy_until_ || address_bytes_ != 3)"
assert s.count(old)==1; open(p,'w').write(s.replace(old,"if (!wel_ || address_bytes_ != 3)"))
PY
for v in orig mut; do
  c++ -std=c++17 -Wall -Wextra -Werror -I$R/tb/common $D/$v/flash_test.cpp -o $D/$v/t && $D/$v/t > $D/$v/out.txt 2>&1; echo "$v rc=$?"; grep -i 'busy\|RESULT\|checks' $D/$v/out.txt
done
