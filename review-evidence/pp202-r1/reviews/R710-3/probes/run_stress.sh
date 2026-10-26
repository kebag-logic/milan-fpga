#!/usr/bin/env bash
# Reviewer probe driver: build tb/acmp_talker from a pristine copy of the
# reviewed tree with r710_stress.hpp spliced in before main(), then run
# N seeds in parallel. Usage:
#   run_stress.sh SRC_TREE WORK_DIR OUT_DIR VERILATOR SEEDS STEPS [PATCH...]
# Optional PATCH files are `old|||new` single-line substitutions applied to
# hdl/acmp/KL_acmp_talker.sv in the copy (a planted control).
set -euo pipefail
SRC=$(realpath -m "$1") WORK=$(realpath -m "$2") OUT=$(realpath -m "$3") V=$4 SEEDS=$5 STEPS=$6; shift 6
P_ABS=(); for p in "$@"; do P_ABS+=("$(realpath "$p")"); done; set -- "${P_ABS[@]}"
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$WORK"; mkdir -p "$WORK" "$OUT"
cp -a "$SRC/hdl" "$SRC/tb" "$WORK/"
for p in "$@"; do
  python3 -I - "$WORK/hdl/acmp/KL_acmp_talker.sv" "$p" <<'EOF'
import sys
f, p = sys.argv[1], sys.argv[2]
old, new = open(p).read().rstrip('\n').split('|||')
s = open(f).read()
assert s.count(old) == 1, ('anchor count', s.count(old), old)
open(f, 'w').write(s.replace(old, new))
EOF
done
T=$WORK/tb/acmp_talker
cp "$HERE/r710_stress.hpp" "$T/"
python3 -I - "$T/sim_main.cpp" <<'EOF'
import sys
f = sys.argv[1]
s = open(f).read()
old = "int main(int argc, char** argv) {\n  Verilated::commandArgs(argc, argv);\n  Hn h;\n"
assert s.count(old) == 1
new = ('#include "r710_stress.hpp"\n'
       + old + '  if (argc > 3 && !strcmp(argv[1], "--stress")) {\n'
       '    r710::Stress st(h, strtoull(argv[2], nullptr, 0));\n'
       '    return st.go(strtol(argv[3], nullptr, 0));\n  }\n')
s = s.replace(old, new)
open(f, 'w').write(s)
EOF
( cd "$T" && if make VERILATOR="$V" run > "$OUT/build_and_suite.log" 2>&1; then echo 0; else echo $?; fi > "$OUT/suite.rc" )
pids=()
for seed in $(seq 1 "$SEEDS"); do
  ( if "$T/obj_dir/Vacmp_talker_sim" --stress "$seed" "$STEPS" > "$OUT/seed$seed.log" 2>&1; then echo 0; else echo $?; fi > "$OUT/seed$seed.rc" ) &
  pids+=($!)
done
wait "${pids[@]}"
grep -h 'R710-STRESS' "$OUT"/seed*.log > "$OUT/summary.txt" || true
echo "suite rc $(cat "$OUT/suite.rc")" >> "$OUT/summary.txt"
for seed in $(seq 1 "$SEEDS"); do printf 'seed%s rc %s\n' "$seed" "$(cat "$OUT/seed$seed.rc")"; done >> "$OUT/summary.txt"
