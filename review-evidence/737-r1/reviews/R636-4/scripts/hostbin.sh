#!/bin/sh
# Build a PATH directory mirroring /usr/bin without any RISC-V cross compiler,
# so the builder's firmware instruments stand down identically in every run.
# Usage: hostbin.sh <destination>
set -eu
dest=$1
mkdir -p "$dest"
for f in /usr/bin/*; do
    b=${f##*/}
    case "$b" in
        riscv*|*-elf-*) continue ;;
    esac
    ln -sf "$f" "$dest/$b"
done
if PATH=$dest command -v riscv64-elf-gcc >/dev/null 2>&1; then
    echo "cross compiler still visible" >&2
    exit 1
fi
echo "hostbin ready: $(ls "$dest" | wc -l) entries"
