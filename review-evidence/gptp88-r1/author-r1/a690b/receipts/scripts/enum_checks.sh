#!/bin/bash
# Enumerate every check name a suite executes: build an instrumented copy of
# its harness (expect() also prints "CHECK <name>") against one source tree.
# usage: enum_checks.sh <src tree> <parser|engine> <out file>
set -e
src=$1; suite=$2; out=$3
. <scratch>/env.sh
w=$(mktemp -d -p $TMPDIR enum-XXXX)
cp $src/tb/verilator/$suite/sim_main.cpp $w/sim_main.cpp
cp -r $src/tb/common $w/../common_$(basename $w) 2>/dev/null || true
if [ $suite = engine ]; then
  python3 - $w/sim_main.cpp <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
a="  void expect(const char *what, uint64_t got, uint64_t exp) {\n    checks++;\n"
assert t.count(a)==1
t=t.replace(a, a+"    printf(\"CHECK %s%s\\n\", check_prefix, what);\n")
open(p,'w').write(t)
PY
else
  python3 - $w/sim_main.cpp <<'PY'
import sys,re; p=sys.argv[1]; t=open(p).read()
a="void RxParserHarness::expect_eq(const char *what, uint64_t got, uint64_t exp) {\n"
assert t.count(a)==1, "parser expect"
t=t.replace(a, a+"  printf(\"CHECK %s\\n\", what);\n")
open(p,'w').write(t)
PY
fi
sed -i "s#\"../../common/verilator_harness.hpp\"#\"$src/tb/common/verilator_harness.hpp\"#" $w/sim_main.cpp
H=$src/hdl
if [ $suite = engine ]; then
  python3 $H/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o $w/gptp_ucode.hex >/dev/null
  mkdir -p $w/p1run; python3 $H/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 --p1 255 -o $w/p1run/gptp_ucode.hex >/dev/null
  verilator --cc --exe --build -j 0 --Mdir $w/obj --top-module KL_gptp_engine -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 -CFLAGS "-std=c++17 -O2 -I$w" $H/ucpu/gptp_ucpu_pkg.sv $H/ucpu/KL_gptp_ucpu.sv $H/wire/KL_gptp_rx_parser.sv $H/wire/KL_gptp_tx_slot.sv $H/common/KL_gptp_timer.sv $H/top/KL_gptp_engine.sv $w/sim_main.cpp -o Vsim >$w/build.log 2>&1
  (cd $w && ./obj/Vsim; cd p1run && ../obj/Vsim +not-gm-capable) > $w/run.log 2>&1 || true
else
  verilator --cc --exe --build -j 0 --Mdir $w/obj --top-module KL_gptp_rx_parser -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I$w" $H/ucpu/gptp_ucpu_pkg.sv $H/wire/KL_gptp_rx_parser.sv $w/sim_main.cpp -o Vsim >$w/build.log 2>&1
  (cd $w && ./obj/Vsim) > $w/run.log 2>&1 || true
fi
grep "^CHECK " $w/run.log | sed 's/^CHECK //' > $out
grep "checks:" $w/run.log
wc -l < $out
