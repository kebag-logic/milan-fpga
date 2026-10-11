#!/usr/bin/env bash
# Scratch (M8a-1 round 2): default and split exports with the base 08b90b68
# blobs of milan_soc.py and ctrl_memory.py swapped in, then with the head's;
# then the four pairs compared. No Vivado.
set -u
L=$LANES/640-m8a
S=$VALIDATION_STORAGE/640m8a-a594/r2/scripts
W=$VALIDATION_STORAGE/640m8a-a594/r2/work
F=$VALIDATION_STORAGE/640m8a-a594/m81/final-fit
D=$MANAGEMENT/2026-09-23/640m8a-a594/evidence-m81/digest.py
export SDK=$VALIDATION_STORAGE/502-a340-sdk PATH="$VALIDATION_STORAGE/502-a340-sdk/bin:$WORKSPACE_HOME/litex-milan/venv/bin:$PATH" PYTHONHASHSEED=0 TMPDIR=$VALIDATION_STORAGE/640m8a-a594/r2/tmpdir LITEX_ENV_CC_TRIPLE=riscv32-linux
mkdir -p "$W"
cd "$L" || exit 9
git rev-parse HEAD > "$W/head.txt"
git status --porcelain > "$W/status-before.txt"
bash sw/litex/build.sh ax7101 --dry-run > "$W/ax7101-dry-run.log" 2>&1; echo "dry ax7101 rc $?"
bash sw/litex/build.sh ax8x8 --dry-run > "$W/ax8x8-dry-run.log" 2>&1; echo "dry ax8x8 rc $?"
restore() { git checkout HEAD -- sw/litex/milan_soc.py sw/litex/ctrl_memory.py; }
trap restore EXIT
git show 08b90b68:sw/litex/milan_soc.py > sw/litex/milan_soc.py
git show 08b90b68:sw/litex/ctrl_memory.py > sw/litex/ctrl_memory.py
sha256sum sw/litex/milan_soc.py sw/litex/ctrl_memory.py > "$W/base-blobs.sha256"
run() {  # tag
  python3 "$S/export.py" "$W" ax7101 "$1-ax7101"
  python3 "$S/export.py" "$W" ax8x8 "$1-ax8x8"
  python3 "$S/export.py" "$W" ax7101 "$1-split-ax7101" --ctrl-mailbox --ctrl-firmware "$F/split-endstation_ax7101_1x1_tdm8-if1/ctrl_app.elf"
  python3 "$S/export.py" "$W" ax8x8 "$1-split-ax8x8" --ctrl-mailbox --ctrl-firmware "$F/split-endstation_ax7101_8x8-if1/ctrl_app.elf"
}
run base
restore
trap - EXIT
git diff --quiet HEAD -- sw/litex || { echo "restore failed"; exit 8; }
sha256sum sw/litex/milan_soc.py sw/litex/ctrl_memory.py > "$W/head-blobs.sha256"
run head
for pair in ax7101 ax8x8 split-ax7101 split-ax8x8; do
  python3 "$D" "$W/base-$pair" "$W/head-$pair" > "$W/digest-$pair.txt" 2>&1
  echo "digest $pair rc $? $(tail -1 "$W/digest-$pair.txt")"
done
git status --porcelain > "$W/status-after.txt"
diff "$W/status-before.txt" "$W/status-after.txt" && echo "status unchanged"
