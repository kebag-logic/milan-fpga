#!/usr/bin/env bash
# Prove the committed arm is not vacuous, in scratch copies of the tree:
#  reverted: the arm with the base RTL in place (control must fail)
#  renamed:  the arm with one named stale-word check renamed in the bench
set -u
M=$VALIDATION_STORAGE/g35-a599/r2/meta; LANE=$LANES/g35-rx-err
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export TMPDIR=$VALIDATION_STORAGE/g35-a599/tmp PYTHONDONTWRITEBYTECODE=1
rm -rf "$M"; mkdir -p "$M"
for v in reverted renamed; do
  T=$M/$v; mkdir -p "$T"
  git -C "$LANE" archive a70e388 hdl tb/common tb/mutation_verdict.py tb/verilator/parser | tar -x -C "$T"
done
git -C "$LANE" show 5dce647a:hdl/wire/KL_gptp_rx_parser.sv > "$M/reverted/hdl/wire/KL_gptp_rx_parser.sv"
sed -i 's/"%s after a refused %s: every word is this frame'"'"'s"/"%s after a refused %s: every word is its own"/' "$M/renamed/tb/verilator/parser/sim_main.cpp"
grep -c "every word is its own" "$M/renamed/tb/verilator/parser/sim_main.cpp"
for v in reverted renamed; do
  ( cd "$M/$v/tb/verilator/parser" && python3 mutants.py > "$M/$v.log" 2>&1; echo $? > "$M/$v.rc" ) &
done
wait
for v in reverted renamed; do echo "== $v rc=$(cat "$M/$v.rc")"; cat "$M/$v.log"; done
