#!/bin/bash
# splitboot.sh CLONE OUT: the split boot simulation (the platform image on the split SoC) at 1x1/1if and 8x8.
. <scratch>/bin/env.sh
export PATH=<home>/br-milan-rv32/host/bin:$PATH LITEX_ENV_CC_TRIPLE=riscv32-linux COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0
cd "$1" || exit 2
echo "HEAD $(git rev-parse --short=8 HEAD) start $(date +%T)"
rc=0
for s in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  <home>/litex-milan/venv/bin/python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$2/$s" --shape "$s" > "$2-$s.log" 2>&1; r=$?
  echo "== $s rc=$r $(date +%T): $(tail -2 "$2-$s.log" | tr '\n' ' ' | cut -c1-200)"; [ $r = 0 ] || rc=1
done
echo "END rc=$rc $(date +%T)"; exit $rc
