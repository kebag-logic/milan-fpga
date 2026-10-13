#!/usr/bin/env bash
# probe_f5_pin.sh <copy> <work>: in a DISPOSABLE copy of the candidate (submodules at their
# gitlinks: tsn-c-stack, lwSRP, gptp-processor, protocol-processor), show that
#   P1  an edit to the stack's include/wire.h is refused by the shared pin check but not by
#       #726's tb/verilator/milan_dp/stream_counter_f5.py, which builds and passes;
#   P1b the same program compiles that header (an #error planted there stops it);
#   P3  the milan_dp targets that run it have no pin prerequisite (make's own dry run).
# Restores include/wire.h afterwards. Never run it in the review clone.
set -u
copy=$1; work=$2
cd "$copy" || exit 2
stack=third_party/tsn-c-stack
echo "# P1: one comment line appended to $stack/include/wire.h"
echo '/* probe: an edit the pin must refuse */' >> "$stack/include/wire.h"
python sw/firmware/ctrl/test/ctrl_build.py --stack-pin; echo "stack-pin rc=$?"
rm -rf "$work/p1"; mkdir -p "$work/p1"
python tb/verilator/milan_dp/stream_counter_f5.py --shape 1 --work "$work/p1"; echo "stream_counter_f5 rc=$?"
git -C "$stack" checkout -q include/wire.h
echo "# P1b: #error planted in $stack/include/wire.h"
echo '#error probe-poison: the F5 build reads the stack header' >> "$stack/include/wire.h"
rm -rf "$work/p1b"; mkdir -p "$work/p1b"
python tb/verilator/milan_dp/stream_counter_f5.py --shape 1 --work "$work/p1b" 2>&1 | grep -E 'probe-poison|Refusal' | head -4
git -C "$stack" checkout -q include/wire.h
echo "# P3: make -n of the milan_dp targets that run it"
for t in counters-f5 counters-mutants; do echo "## $t"; make -n -C tb/verilator/milan_dp "$t" 2>&1 | grep -v '^make'; done
echo "milan_dp/Makefile lines naming stack-pin: $(grep -c 'stack-pin' tb/verilator/milan_dp/Makefile)"
git -C "$stack" status --short
