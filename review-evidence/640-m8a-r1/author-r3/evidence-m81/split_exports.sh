#!/usr/bin/env bash
# Scratch (M8a-1 evidence): the split exports, then the SoC-level planted controls.
set -u
export SDK=$VALIDATION_STORAGE/502-a340-sdk PATH="$VALIDATION_STORAGE/502-a340-sdk/bin:$WORKSPACE_HOME/litex-milan/venv/bin:$PATH" PYTHONHASHSEED=0 TMPDIR=$VALIDATION_STORAGE/640m8a-a594/m81/tmpdir LITEX_ENV_CC_TRIPLE=riscv32-linux
S=$VALIDATION_STORAGE/640m8a-a594/m81/scripts
F=$VALIDATION_STORAGE/640m8a-a594/m81/fit
python3 $S/export.py ax7101 split-ax7101 --ctrl-mailbox --ctrl-firmware $F/split-endstation_ax7101_1x1_tdm8-if1/ctrl_app.elf
python3 $S/export.py ax8x8 split-ax8x8 --ctrl-mailbox --ctrl-firmware $F/split-endstation_ax7101_8x8-if1/ctrl_app.elf
echo done > $VALIDATION_STORAGE/640m8a-a594/m81/work/split-exports.done
