#!/bin/bash
# scan_images.sh OBJDUMP SCRATCH NAME...: each boot's image hash and its stand-in loads inside ls_* functions.
OD=$1; S=$2; shift 2
echo 'probe | image sha256 | ls_ lui 0xf0004 | ls_ lui 0x20000'
for n in "$@"; do e=$S/out-$n/image/ctrl_app.elf
  "$OD" -d "$e" | awk -v n="$n" -v h="$(sha256sum "$e" | cut -d' ' -f1)" '
    /^[0-9a-f]+ <.*>:$/ { inls = ($2 ~ /^<ls_/) }
    inls && /[[:space:]]lui[[:space:]]/ { if ($0 ~ /0xf0004/) t++; if ($0 ~ /0x20000/) w++ }
    END { printf "%s | %s | %d | %d\n", n, h, t, w }'
done
