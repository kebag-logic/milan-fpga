#!/usr/bin/env bash
# r4_measure_head.sh: the same measurement on a clean clone of the merge head (dev's figures are r4_measure.sh's, its tree unchanged).
# merged tree, then the size fixture and the target platform's image at all four points, at the merge and at dev.
set -u
D=<scratch>; M=$D/snaps/m6; V=$D/snaps/dev4; R=$D/ledger5/runtime; X=$D/exports5
export HOME=$D/sdk/home PYTHONHASHSEED=0 TMPDIR=$D/tmp LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PATH=<litex-env>/venv/bin:$D/sdk<home-path>/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:/usr/local/bin:/usr/bin:/bin
cd $D
echo "compiler: $($HOME/br-milan-rv32/host/bin/riscv32-linux-gcc --version | head -1)"
for s in 1x1_tdm8 8x8; do
  rm -rf $X/$s; mkdir -p $X/$s
  (cd $M && python3 -B -c "
import sys; from pathlib import Path
sys.path.insert(0, 'tb/verilator/ctrl_service_budget'); import build
build.flash_map(Path('$X/$s/flash-map'), 'endstation_ax7101_$s')" > $X/$s/flash_map.log 2>&1); echo "export $s rc=$?"
done
for w in m6; do
  T=$D/snaps/$w
  tools/ledger.sh $T $D/ledger5/$w $R
  for s in 1x1_tdm8 8x8; do
    csv=$X/$s/mapped/soc/csr.csv; fm=$X/$s/flash-map
    tools/plat_ledger.sh $T $D/plat5/$w $R endstation_ax7101_$s 1 $csv $fm
    led=; [ $s = 8x8 ] && led=platform-8x8-two-interfaces
    tools/plat_ledger.sh $T $D/plat5/$w $R endstation_ax7101_$s 2 $csv $fm $led
  done
done
