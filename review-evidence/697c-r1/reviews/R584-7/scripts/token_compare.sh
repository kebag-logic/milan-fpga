#!/bin/sh
# usage: token_compare.sh <milan-fpga repo> <old commit> <stack repo> <stack commit>
# Compares each removed core file with its tsn-c-stack counterpart after comment
# removal (gcc -fpreprocessed) and whitespace tokenisation. Prints SAME/DIFF per pair.
set -eu
R=$1; OLD=$2; S=$3; SC=$4
T=$(mktemp -d)
norm() { gcc -fpreprocessed -dD -E -P -x c - 2>/dev/null | tr -s ' \t\n' '\n\n\n' | grep -v '^$'; }
for pair in adp/adp.c:src/adp.c adp/adp.h:include/adp.h acmp/acmp.c:src/acmp.c acmp/acmp.h:include/acmp.h \
            maap/maap.c:src/maap.c maap/maap.h:include/maap.h wire/wire.h:include/wire.h; do
  o=${pair%%:*}; n=${pair#*:}
  git -C "$R" show "$OLD:sw/firmware/ctrl/$o" | norm > "$T/a"
  git -C "$S" show "$SC:$n" | norm > "$T/b"
  if cmp -s "$T/a" "$T/b"; then echo "SAME $o $n"; else echo "DIFF $o $n"; diff "$T/a" "$T/b" | head -20; fi
done
rm -rf "$T"
