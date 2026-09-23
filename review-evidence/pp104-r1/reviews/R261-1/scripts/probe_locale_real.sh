#!/bin/sh
# Real-compiler locale probe for the head's fixture guards.
# Usage: probe_locale_real.sh <extracted-head-tree> <mutant-M1-dir> <verilator>
# Runs the exact `make fixture-guards` command line (taken from `make -n`, with
# -j 8 instead of -j 0) from the head's tb/pp_top, once with the head's
# fixture_guards.py and once with the M1 mutant (LC_ALL override deleted), both
# under a caller environment whose gettext language is French. The compiler on
# this host localises "static assertion failed" under LANGUAGE=fr, so the head
# must PASS and the mutant must FAIL.
set -u
TREE=$1; M1=$2; VERILATOR=$3
cd "$TREE/tb/pp_top" || exit 2
VF='--cc --exe --build -j 8 --top-module pp_top_wrap -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -CFLAGS "-std=c++17 -O2 -I$(CURDIR) -Wall -Wextra"'
CMD=$(make -n VERILATOR="$VERILATOR" "VFLAGS=$VF" fixture-guards | sed -e ':a' -e '/\\$/N; s/\\\n//; ta' | grep '^python3 fixture_guards.py')
[ -n "$CMD" ] || { echo "could not derive the command"; exit 2; }
rc_all=0
for variant in head M1; do
    if [ $variant = head ]; then script=fixture_guards.py; else script="$M1/fixture_guards.py"; fi
    run=$(printf '%s' "$CMD" | sed "s#^python3 fixture_guards.py#python3 -B $script#")
    out=$(env LANG=en_US.UTF-8 LANGUAGE=fr sh -c "$run" 2>/dev/null)
    rc=$?
    echo "== $variant under LANG=en_US.UTF-8 LANGUAGE=fr: exit $rc"
    printf '%s\n' "$out" | grep -E '^(fixture guard|FAIL|.*error:)' | head -6
    if [ $variant = head ] && [ $rc -ne 0 ]; then rc_all=1; fi
    if [ $variant = M1 ] && [ $rc -eq 0 ]; then rc_all=1; fi
done
echo "LOCALE PROBE: $([ $rc_all -eq 0 ] && echo PASS || echo FAIL)"
exit $rc_all
