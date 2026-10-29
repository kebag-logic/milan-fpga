#!/bin/bash
# The reviewer's NUL-line probe (a copy of r733_console_nul.c) under AddressSanitizer, against the checkout's
# console and against a copy with the terminator stop reverted. Lane helper.
# usage: asan_probe.sh CHECKOUT WORK PROBE_C
set -u
C=$(cd "$1" && pwd) W=$2 P=$3
EC=${C//./\\.} EW=${W//./\\.}
rm -rf "$W"; mkdir -p "$W/rev"
cp "$P" "$W/probe.c"
sed 's/while (n < c->len \&\& command\[n\] != '"'"'\\0'"'"' \&\& command\[n\] == c->line\[n\]) {/while (n < c->len \&\& command[n] == c->line[n]) {/' \
    "$C/sw/firmware/ctrl/plat/ctrl_plat_console.c" > "$W/rev/ctrl_plat_console.c"
echo "reverted copy differs from the checkout's in $(diff "$C/sw/firmware/ctrl/plat/ctrl_plat_console.c" "$W/rev/ctrl_plat_console.c" | grep -c '^>') line(s)"
for v in fixed reverted; do
    src=$C/sw/firmware/ctrl/plat/ctrl_plat_console.c
    [ $v = reverted ] && src=$W/rev/ctrl_plat_console.c
    gcc -std=c11 -O2 -g -fsanitize=address -fno-omit-frame-pointer -I"$C/sw/firmware/ctrl/plat" -o "$W/probe-$v" \
        "$W/probe.c" "$src" "$C/sw/firmware/ctrl/plat/ctrl_plat_csr.c"
    echo "== $v: build rc=$?"
    ASAN_OPTIONS=abort_on_error=0 "$W/probe-$v" > "$W/$v.out" 2> "$W/$v.err"
    echo "== $v: run rc=$?; console answered: $(tr -d '\r\n' < "$W/$v.out")"
    grep -E "ERROR: AddressSanitizer|SUMMARY|^commands" "$W/$v.err" | sed "s#$EW#<work>#g; s#$EC#<clone>#g"
done
