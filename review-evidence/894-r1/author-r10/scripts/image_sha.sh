#!/bin/bash
# sha256 of every image qall.sh built under a tag: each image's ELF, its objcopy -O binary and every object it
# links, one line a file, relative to the tag's directory.
# usage: image_sha.sh TAG > out.txt
set -eu
T=<scratch>
. $T/scripts/env.sh
O=$T/r10/qall/$1
cd "$O"
for d in */; do
    d=${d%/}
    riscv32-buildroot-linux-gnu-objcopy -O binary "$d/image/ctrl_app.elf" "$d/image/ctrl_app.bin"
done
find . -path '*/image/*' \( -name 'ctrl_app.elf' -o -name 'ctrl_app.bin' -o -name '*.o' \) -type f | LC_ALL=C sort |
    while read -r f; do sha256sum "$f"; done
