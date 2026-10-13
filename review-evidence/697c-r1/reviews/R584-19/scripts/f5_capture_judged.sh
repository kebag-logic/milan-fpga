#!/bin/sh
# Reviewer control: the boundary judges the compiles of the F5 build-only capture.
# In a disposable copy of the checkout at the head ($1), capture ONLY
# stream_counter_f5.py --build-only --shape 1, then judge that capture with
# ctrl_boundary.py --capture. Clean first, then with a firmware source F5
# compiles (aecp/aecp_mbx.c) planted to include a stack file outside include/
# (examples/adp_port.h). The planted run must name aecp_mbx.c and the stack
# file; the clean run must not. Other refusals (known builders the F5-only
# capture holds nothing of) are expected in both and are not the control.
# Usage: f5_capture_judged.sh <copy> <out dir> <python>
set -u
copy=$1; out=$2; py=$3
mkdir -p "$out"
cd "$copy" || exit 2
for arm in clean planted; do
  if [ "$arm" = planted ]; then
    printf '%s\n' '#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"' > /tmp/.f5plant.$$
    cat sw/firmware/ctrl/aecp/aecp_mbx.c >> /tmp/.f5plant.$$
    cp /tmp/.f5plant.$$ sw/firmware/ctrl/aecp/aecp_mbx.c; rm -f /tmp/.f5plant.$$
  fi
  cap="$out/capture-$arm"; rm -rf "$cap" "$out/f5work-$arm"
  "$py" -B sw/firmware/ctrl/test/ctrl_capture.py --out "$cap" -- \
    "$py" tb/verilator/milan_dp/stream_counter_f5.py --build-only --shape 1 --work "$out/f5work-$arm" \
    > "$out/capture-$arm.log" 2>&1
  echo "capture-$arm rc=$?" | tee -a "$out/summary.txt"
  "$py" -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --capture "$cap" \
    > "$out/judge-$arm.log" 2>&1
  echo "judge-$arm rc=$?" | tee -a "$out/summary.txt"
  n=$(grep -c "aecp_mbx.c.*tsn-c-stack/examples/adp_port.h\|adp_port.h.*aecp_mbx.c" "$out/judge-$arm.log")
  echo "judge-$arm lines naming aecp_mbx.c with examples/adp_port.h: $n" | tee -a "$out/summary.txt"
done
git checkout -- sw/firmware/ctrl/aecp/aecp_mbx.c
git status --short | tee -a "$out/summary.txt"
