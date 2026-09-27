#!/bin/sh
# Parameterised form of the executed launcher: builds both shapes, runs the eight named plans
# (all via run.py; the other three per shape via plan_run.py in their own directories), the
# unchanged round-1 probes P1/P2 (round-1 sim_main via make_probe.py) and the other reviewer's PD.
# Usage: run_plans.sh <repo> <packet> <round1-harness-export> <r348-scripts-dir> <round1-receipts>
# The executed run detached these eight slots and polled them; each slot is a foreground chain here.
R=$1; P=$2; OLD=$3; R348=$4; R1=$5; S=$P/scratch
B1=$S/b_endstation_ax7101_1x1_tdm8; B8=$S/b_endstation_ax7101_8x8
export PATH="$HOME/litex-milan/venv/bin:/usr/bin:/bin:$HOME/br-milan-rv32/host/bin" PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux
PY=$HOME/litex-milan/venv/bin/python
for sh in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  $P/scripts/env_run.sh $R --shape $sh --build-dir $S/b_$sh --build-only
  $PY -B $P/scripts/prep_fixture.py $R $S/b_$sh $sh
done
python3 $P/scripts/make_probe.py $OLD $B1 $S/p_uart uart_paced
python3 $P/scripts/make_probe.py $OLD $B1 $S/p_wip wip_split
python3 $R348/compile_probe.py $R $B8 $S/probe-8x8/native
mkdir -p $S/runs/P1 $S/runs/P2 $S/runs/PD
cp $B1/slots.bin $B1/commands.txt $S/runs/P1/; cp $B1/slots.bin $B1/commands.txt $S/runs/P2/; cp $B8/slots.bin $S/runs/PD/
printf 'milan_nvm\nmilan_nvm\nmilan_nvm\n' > $S/runs/PD/plan-status3.txt
( $P/scripts/env_run.sh $R --shape endstation_ax7101_1x1_tdm8 --build-dir $B1 --reuse-build --populated --record-budget-findings
  cd $B1/gateware && $S/p_uart/native/Vsim $B1/aem_desc.bin $S/runs/P1/slots.bin $S/runs/P1/commands.txt 0 > $S/runs/P1/raw.log 2>&1 ) &
$PY -B $P/scripts/plan_run.py $R $B1 endstation_ax7101_1x1_tdm8 uart-paced 0 0 $S/runs/paced1x1 &
( $PY -B $P/scripts/plan_run.py $R $B1 endstation_ax7101_1x1_tdm8 queued-input 0 0 $S/runs/queued1x1 $R1/probe_P3_commands.txt
  cd $B1/gateware && $S/p_wip/native/Vsim $B1/aem_desc.bin $S/runs/P2/slots.bin $S/runs/P2/commands.txt 1000000 5000 > $S/runs/P2/raw.log 2>&1 ) &
$PY -B $P/scripts/plan_run.py $R $B1 endstation_ax7101_1x1_tdm8 device-wait 3000000 5000 $S/runs/dev1x1 &
$P/scripts/env_run.sh $R --shape endstation_ax7101_8x8 --build-dir $B8 --reuse-build --populated --device-wait-us 1000 --program-wait-us 1000 --record-budget-findings &
$PY -B $P/scripts/plan_run.py $R $B8 endstation_ax7101_8x8 uart-paced 0 0 $S/runs/paced8x8 &
( $PY -B $P/scripts/plan_run.py $R $B8 endstation_ax7101_8x8 queued-input 0 0 $S/runs/queued8x8
  cd $B8/gateware && PROBE_LOG=$S/runs/PD/probe.txt $S/probe-8x8/native/Vsim $B8/aem_desc.bin $S/runs/PD/slots.bin $S/runs/PD/plan-status3.txt 0 0 > $S/runs/PD/raw.log 2>&1 ) &
$PY -B $P/scripts/plan_run.py $R $B8 endstation_ax7101_8x8 device-wait 3000000 5000 $S/runs/dev8x8 &
wait
