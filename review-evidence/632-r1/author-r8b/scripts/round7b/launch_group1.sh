#!/usr/bin/env bash
# Round 7b, after the record commit: the two Verilator campaigns (two builds at
# once, the lane's limit), the firmware gate set up to the coverage check (C/C++
# only; its boundary gate builds Verilator models and runs later), the full
# Yosys gate and lint, each in its own clean clone at <rev> with its own log and
# rc, started in the background. The pull-in legs follow on the tdm8 campaign's
# clean ship binary (pullin_legs.sh), the sweep after both campaigns.
# usage: launch_group1.sh <rev>
set -u
rev=$1; h=${rev:0:8}
R7=$MANAGEMENT/2026-09-23/632-a659/scripts/round7
R7B=$MANAGEMENT/2026-09-23/632-a659/scripts/round7b
S=$VALIDATION_STORAGE/scratch/632-a659/r7
B=$VALIDATION_STORAGE/scratch/632-a659/r7b
mkdir -p "$B"
setsid nohup bash "$R7/campaign.sh" "tdm8m-$h" "$rev" tb/verilator/milan_dp_render tdm8render-mutants VERILATOR_JOBS=2 \
  > "$B/tdm8m.nohup" 2>&1 < /dev/null &
setsid nohup bash "$R7/campaign.sh" "gmstep-$h" "$rev" tb/verilator/milan_dp_gm_steps gmstep-mutants VERILATOR_JOBS=2 \
  > "$B/gmstep.nohup" 2>&1 < /dev/null &
# firmware set (without the boundary gate) and Yosys, each in its own clone
for c in fw yosys lint; do
  [ -d "$B/clone-$c-$h" ] || bash "$R7/make_clone.sh" "$B/clone-$c-$h" "$rev" > "$B/clone-$c-$h.log" 2>&1
done
setsid nohup bash "$R7B/firmware_gates.sh" "$B/clone-fw-$h" "$B/fw-$h" nb > "$B/fw.nohup" 2>&1 < /dev/null &
setsid nohup bash -c "cd '$B/clone-yosys-$h' && export PATH=$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:\$PATH && \
  git rev-parse HEAD > '$B/yosys-$h.head' && date -Is > '$B/yosys-$h.start' && \
  syn/yosys/run.sh > '$B/yosys-$h.log' 2>&1; echo \$? > '$B/yosys-$h.rc'; date -Is > '$B/yosys-$h.end'" \
  > "$B/yosys.nohup" 2>&1 < /dev/null &
( cd "$B/clone-lint-$h" && source "$R7/env.sh" && git rev-parse HEAD > "$B/lint-$h.head" && \
  python3 scripts/lint_rtl.py --check > "$B/lint-$h.log" 2>&1; echo $? > "$B/lint-$h.rc" )
echo launched
