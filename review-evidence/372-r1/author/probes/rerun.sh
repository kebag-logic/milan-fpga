#!/usr/bin/env bash
# Re-run every synthetic Verilator 5.050 probe of the #372 author lane.
# Usage: rerun.sh <path to the pinned verilator 5.050 wrapper>
set -uo pipefail
VL=${1:?path to verilator 5.050}
HERE=$(cd "$(dirname "$0")" && pwd)
W=$(mktemp -d)
b() { # dir tag top flags... ; builds $W/$dir-$tag/sim
  local dir=$1 tag=$2 top=$3; shift 3
  (cd "$HERE/$dir" && "$VL" --cc --exe --build -j 8 --top-module "$top" -Wall -Wno-fatal \
     -Mdir "$W/$dir-$tag" "$@" -o sim > "$W/$dir-$tag.build.log" 2>&1)
  echo "build $dir/$tag rc=$?"; grep -E '^%' "$W/$dir-$tag.build.log" || true
}
r() { local exe=$1; shift; echo "run ${exe#$W/} $*"; "$W/$exe" "$@"; echo "rc=$?"; }
"$VL" --version
b p1 assert dut --assert dut.sv chk.sv bind.sv tb.cpp
for m in ok drop reset_after reset_before; do r p1-assert/sim +mode=$m; done
b p1 noassert dut dut.sv chk.sv bind.sv tb.cpp;            r p1-noassert/sim +mode=drop
b p1 covuser dut --assert --coverage-user dut.sv chk.sv bind.sv tb.cpp; r p1-covuser/sim +mode=ok
b p2 noassert dut --no-assert dut.sv chk.sv bind.sv tb.cpp; r p2-noassert/sim +mode=drop
b p2 badbind dut --assert dut.sv chk.sv badbind.sv tb.cpp;  r p2-badbind/sim +mode=ok
b p3 assert dut --assert dut.sv chk.sv bind.sv tb.cpp
for m in ok ab bone; do r p3-assert/sim +mode=$m; done
b p4 vac dut --assert dut.sv chk.sv bind.sv tb.cpp;         r p4-vac/sim
b p4 vacoff dut --assert +define+VAC_OFF dut.sv chk.sv bind.sv tb.cpp; r p4-vacoff/sim
b p5 assert dut --assert dut.sv chk.sv bind.sv tb.cpp;      r p5-assert/sim
b p5 covuser dut --assert --coverage-user dut.sv chk.sv bind.sv tb.cpp; r p5-covuser/sim
b p5 noassert dut --no-assert dut.sv chk.sv bind.sv tb.cpp; r p5-noassert/sim
b p6 assert dut --assert dut.sv chk.sv bind.sv tb.cpp;      r p6-assert/sim
b p7 assert dut --assert dut.sv sub.sv bind.sv tb.cpp;      r p7-assert/sim
b p7 noassert dut --no-assert dut.sv sub.sv bind.sv tb.cpp; r p7-noassert/sim
b p8 assert top --assert top.sv tb.cpp
r p8-assert/sim; r p8-assert/sim +verilator+error+limit+1000
b p9 badbind dut --assert dut.sv sub.sv badbind.sv tb.cpp;  ls "$W/p9-badbind" | grep -i dpi; r p9-badbind/sim
rm -rf "$W"
