#!/usr/bin/env bash
# Reviewer probe for #637: build the dynmap leg from a DISPOSABLE copy of the
# reviewed tree with one print added to sim_nxn.cpp's maprec_power_cycle(),
# so that every planted power cycle reports PP_STAT's combined restore
# verdicts (done [2], fail [3], blank [7], rb [17], cause [20:18]) beside the
# map restore's internal roll-back flag. The copy's sim_nxn.cpp is put back
# byte for byte afterwards. No check is added or changed: the leg's own
# tally must stay "checks: 331   failures: 0".
#
# usage: ppstat_probe.sh TREE_COPY OUTDIR   (VERILATOR may name the binary)
set -euo pipefail
tree=$1
out=$2
suite="$tree/tb/verilator/milan_dp"
mkdir -p "$out"
cp "$suite/sim_nxn.cpp" "$out/sim_nxn.cpp.orig"
python3 -I - "$suite/sim_nxn.cpp" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
pat = ("        for (int c = 0; c < 64; c++) step();\n"
       "        maprec_go_to_end = t_end;\n")
assert t.count(pat) == 1, "the anchor moved"
rep = pat + (
    '        { const uint32_t s = axi_read(A_PP_STAT);\n'
    '          printf("  [probe] %s: PP_STAT %08x done=%u fail=%u blank=%u rb=%u cause=%u map_rs_fail=%u\\n", tag, s,\n'
    '                 (s>>2)&1u, (s>>3)&1u, (s>>7)&1u, (s>>17)&1u, (s>>18)&7u,\n'
    '                 (unsigned)dut->rootp->milan_datapath__DOT__amr_rs_fail_r); }\n')
open(p, "w").write(t.replace(pat, rep))
EOF
set +e
make -s -j16 -C "$suite" -o ltn_rom.hex -o ucode.hex dynmap-build \
  DYNMAP_MDIR="$out/obj_instr" VERILATOR="${VERILATOR:-verilator}" > "$out/instr.build.log" 2>&1
brc=$?
cp "$out/sim_nxn.cpp.orig" "$suite/sim_nxn.cpp"
set -e
[ "$brc" -eq 0 ] || { echo "build rc $brc"; exit 1; }
(cd "$suite" && "$out/obj_instr/Vmilan_dp_dynmap") > "$out/instr.log" 2>&1 || true
grep '\[probe\]' "$out/instr.log"
grep -E '^checks:' "$out/instr.log"
