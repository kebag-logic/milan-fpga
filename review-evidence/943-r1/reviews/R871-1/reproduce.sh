#!/usr/bin/env bash
# reproduce.sh - the reviewer's commands for PR #953 at 502b041cc0bd0e4ea230b8a3a65f553ab69df3ff (#943), in order.
# Usage: reproduce.sh <head-clone> <base-clone> <out>
#   <head-clone>  a clean checkout of 502b041c with gptp-processor, protocol-processor, third_party/lwSRP,
#                 third_party/tsn-c-stack and third_party/verilog-axis initialised
#   <base-clone>  the same at 0839453f, with the head's sw/firmware/ctrl/test/test_aecp.cpp copied over it
#   <out>         an empty directory for builds and logs
# Needs the host C/C++ toolchain the firmware's host harness uses and, for the twin, Verilator 5.050 on PATH.
set -u
H=$1; B=$2; O=$3; mkdir -p "$O"
here=$(cd "$(dirname "$0")" && pwd)
arm() { (cd "$1" && python3 sw/firmware/ctrl/test/aecp_arms.py --output "$O/arms/$2" "${@:3}" > "$O/$2.log" 2>&1; echo $? > "$O/$2.rc") & }
# 1. the new test and the extended Core test at head, four shapes, and the full App arm at 1x1/2if
arm "$H" app-1x1-if1 --app --interfaces 1 --filter 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly'
arm "$H" app-1x1-if2 --app --interfaces 2 --filter 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly'
arm "$H" app-8x8-if1 --app --interfaces 1 --config configs/endstation_ax7101_8x8.yaml --filter 'AppOutputs.*'
arm "$H" app-1x1-if2-full --app --interfaces 2
wait
arm "$H" app-8x8-if2 --app --interfaces 2 --config configs/endstation_ax7101_8x8.yaml \
    --filter 'AppOutputs.*:Core.TheRunningCheckObservesEveryStreamBriefly'
# 2. failing first: the head's test on the base's code
arm "$B" failing-first-base-1x1-if1 --app --interfaces 1 --filter 'AppOutputs.*'
arm "$B" failing-first-base-1x1-if2 --app --interfaces 2 --filter 'AppOutputs.*'
arm "$B" failing-first-base-8x8-if1 --app --interfaces 1 --config configs/endstation_ax7101_8x8.yaml --filter 'AppOutputs.*'
wait
# 3. the PR's 15 output plants at 1x1/1if and 8x8/1if, and the reviewer's seven extra defects at 1x1/2if
(cd "$H" && python3 "$here/probe_mutants.py" "$H" "$O/mut/rows-1x1-if1" configs/endstation_ax7101_1x1_tdm8.yaml 1 rows 0/1 \
    > "$O/rows-1x1-if1.log" 2>&1) &
(cd "$H" && python3 "$here/probe_mutants.py" "$H" "$O/mut/rows-8x8-if1-a" configs/endstation_ax7101_8x8.yaml 1 rows 0/2 \
    > "$O/rows-8x8-if1-a.log" 2>&1) &
(cd "$H" && python3 "$here/probe_mutants.py" "$H" "$O/mut/rows-8x8-if1-b" configs/endstation_ax7101_8x8.yaml 1 rows 1/2 \
    > "$O/rows-8x8-if1-b.log" 2>&1) &
(cd "$H" && python3 "$here/probe_mutants.py" "$H" "$O/mut/extra-1x1-if2" configs/endstation_ax7101_1x1_tdm8.yaml 2 extra 0/1 \
    > "$O/extra-1x1-if2.log" 2>&1) &
wait
# 4. the two-placement twin and its plants at head; then the twin with the completion disabled in the firmware
(cd "$H" && make -j8 -C tb/verilator/milan_dp twin && make -j8 -C tb/verilator/milan_dp twin-plants) > "$O/twin-head.log" 2>&1
echo "twin+plants rc=$?" >> "$O/twin-head.log"
python3 - "$H/sw/firmware/ctrl/app/ctrl_app_aecp.c" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
old = '\t} else if (!v->brief && (v->flags & 0x10000000u) != 0u) {\n'
assert s.count(old) == 1
open(p, 'w').write(s.replace(old, '\t} else if (!v->brief && (v->flags & 0x10000000u) != 0u && c->app == NULL) {\n'))
EOF
(cd "$H" && make -j8 -C tb/verilator/milan_dp twin) > "$O/twin-fix-reverted.log" 2>&1
echo "twin rc=$? (expected 2: the zero stream_dest_mac back)" >> "$O/twin-fix-reverted.log"
(cd "$H" && git checkout -- sw/firmware/ctrl/app/ctrl_app_aecp.c && git status --porcelain)
