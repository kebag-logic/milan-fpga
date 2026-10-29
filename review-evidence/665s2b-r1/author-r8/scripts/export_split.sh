#!/bin/bash
# The shipping 1x1 config's split export (--ctrl-mailbox --ctrl-firmware ELF), no Vivado, from a checkout whose
# endstation builder has run: the product split CPU netlist the export reads. S2c's export_one, split only.
# usage: export_split.sh CHECKOUT OUT_DIR ELF LOG
set -u
T=$1 OUT=$2 ELF=$3 LOG=$4
LITEX=$HOME/litex-milan
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH=$HOME/br-milan-rv32/host/bin:$LITEX/venv/bin:$PATH
export PYTHONPATH=$LITEX/litex:$LITEX/migen
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
c=endstation_ax7101_1x1_tdm8
flow="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive ExtraPostPlacementOpt"
argv=$(/usr/bin/python3 -c "import json,sys; print(' '.join(json.load(open(sys.argv[1]))['argv']))" \
       "$T/sw/builder/out/$c/soc_params.json")
start=$(date +%s)
{ echo "HEAD $(git -C "$T" rev-parse HEAD) DIRTY $(git -C "$T" status --porcelain --untracked-files=no | wc -l)"
  echo "argv: $argv $flow --ctrl-mailbox --ctrl-firmware ELF"; } > "$LOG"
(cd "$T/sw/litex" && "$LITEX/venv/bin/python3" milan_soc.py $argv $flow --ctrl-mailbox --ctrl-firmware "$ELF" \
   --entity-gen-dir "$T/configs/generated/$c" --vivado-max-threads 8 --output-dir "$OUT") >> "$LOG" 2>&1
rc=$?
grep -m1 "VexiiRiscv netlist" "$LOG"
echo "elapsed=$(( $(date +%s) - start ))s" >> "$LOG"
echo "rc=$rc" >> "$LOG"
