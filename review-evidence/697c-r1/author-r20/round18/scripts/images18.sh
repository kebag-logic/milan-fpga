#!/usr/bin/env bash
# Scratch (round 18): every RV32 image at every shipped shape at the head and at dev, each by images6.sh, then the
# two manifests compared. usage: images18.sh
set -u
R=$VALIDATION_STORAGE/697c-a583/round18
export TMPDIR=$R/tmpdir PYTHONDONTWRITEBYTECODE=1
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
for side in head:i dev:idev; do
  name=${side%%:*}; clone=${side#*:}
  start=$SECONDS
  "$R/scripts/images6.sh" "$R/clones/$clone" "$R/work/images-$name" > "$R/logs/images-$name.log" 2>&1
  echo "images $name rc=$? $((SECONDS - start)) s $(git -C "$R/clones/$clone" rev-parse --short=8 HEAD)"
done
cmp "$R/work/images-head/elf.sha256" "$R/work/images-dev/elf.sha256" && echo "manifests byte-equal"
sha256sum "$R/work/images-head/elf.sha256" "$R/work/images-dev/elf.sha256"
