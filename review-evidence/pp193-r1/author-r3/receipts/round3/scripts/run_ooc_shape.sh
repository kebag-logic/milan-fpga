#!/usr/bin/env bash
# usage: P=<parent> run_ooc_shape.sh <log dir> <NAME=VALUE ...>: the parent's
# out-of-context Yosys area of KL_pp_shadow with OOC_CHPARAM set to the given
# parameters. The ROM-digest ledger row the pin needs is recorded in the
# scratch working tree only, and the ledger is restored afterwards.
set -u
P=${P:-<parent>}
out=$1; shift
mkdir -p "$out"
. <scratch>/r3/scripts/env-parent.sh
cd "$P" || exit 2
[ "$(git rev-parse --show-toplevel)" = "$P" ] || exit 3
cp syn/yosys/rom_digests.tsv "$out/rom_digests.tsv.before"
syn/yosys/ooc.sh --record-rom-digests tcam > "$out/ooc_record_rom_digests.log" 2>&1
echo $? > "$out/ooc_record_rom_digests.rc"
t0=$(date +%s)
OOC_CHPARAM="$*" syn/yosys/ooc.sh KL_pp_shadow > "$out/ooc_pp_shadow.log" 2>&1
echo $? > "$out/ooc_pp_shadow.rc"
echo $(( $(date +%s) - t0 )) > "$out/ooc_pp_shadow.sec"
echo "OOC_CHPARAM=$*" > "$out/shape.txt"
cp "$out/rom_digests.tsv.before" syn/yosys/rom_digests.tsv
git diff --quiet -- syn/yosys/rom_digests.tsv && echo "ledger restored" > "$out/ledger.txt"
echo done > "$out/OOC.done"
