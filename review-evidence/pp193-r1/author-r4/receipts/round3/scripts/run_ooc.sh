#!/usr/bin/env bash
# usage: run_ooc.sh <log dir>: the parent's out-of-context Yosys gates at the
# committed pin. The ROM-digest ledger row the pin needs is recorded in the
# scratch working tree only, and the ledger is restored afterwards.
set -u
P=${P:-<parent>}
out=$1
mkdir -p "$out"
. <scratch>/r3/scripts/env-parent.sh
cd "$P" || exit 2
[ "$(git rev-parse --show-toplevel)" = "$P" ] || exit 3
cp syn/yosys/rom_digests.tsv "$out/rom_digests.tsv.before"
gate() {
  local name=$1; shift
  local t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
  echo $(( $(date +%s) - t0 )) > "$out/$name.sec"
}
gate ooc_record_rom_digests syn/yosys/ooc.sh --record-rom-digests tcam
diff "$out/rom_digests.tsv.before" syn/yosys/rom_digests.tsv > "$out/rom_digests.rows.diff"
gate ooc_selftest python3 syn/yosys/ooc_selftest.py
gate ooc_pp_shadow syn/yosys/ooc.sh KL_pp_shadow
cp "$out/rom_digests.tsv.before" syn/yosys/rom_digests.tsv
git diff --quiet -- syn/yosys/rom_digests.tsv && echo "ledger restored" > "$out/ledger.txt"
echo done > "$out/OOC.done"
