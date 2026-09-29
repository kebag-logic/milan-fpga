#!/usr/bin/env bash
# Reviewer probe R391-4 item 3 (disposable, never committed): a scratch parent
# at a chosen revision with the processor tree at a chosen revision in place of
# its submodule, optionally with the author's declared pin-adoption edits
# (parent_edits.py from the public author-r4 packet) applied, then ONE named
# focused target. Nothing is written to any source repository (--shared clones).
# Usage:
#   parent_scratch.sh <parent clone> <parent rev> <processor checkout> <processor rev>
#                     <scratch dir> <dir holding a Verilator 5.050 'verilator'>
#                     <name> <edits: none|path to parent_edits.py> <target> [make args...]
# Needs GPTP and VAXIS: local clones of the gptp-processor and verilog-axis public
# remotes (checked out at the parent's own gitlinks).
# targets:
#   setup                only build the scratch parent
#   cosim-quick          tb/verilator/nvm_cosim: run_cases.py --shapes 1x1 --skip-mutants
#   dp <make target>     make -C tb/verilator/milan_dp <target> (e.g. notify, run)
set -euo pipefail
PAR=$1; PREV=$2; PP=$3; PPREV=$4; S=$5; VDIR=$6; NAME=$7; EDITS=$8; TGT=$9; shift 9
export PATH="$VDIR:$PATH"
d="$S/parent-$NAME"
if [ ! -f "$d/.r391-ready" ]; then
  rm -rf "$d"
  git clone -q --shared --no-checkout "$PAR" "$d"; git -C "$d" checkout -q --detach "$PREV"
  for sm in protocol-processor:$PP:$PPREV gptp-processor:${GPTP:?}: third_party/verilog-axis:${VAXIS:?}:; do
    path=${sm%%:*}; rest=${sm#*:}; src=${rest%%:*}; rev=${rest#*:}
    [ -n "$rev" ] || rev=$(git -C "$PAR" ls-tree "$PREV" "$path" | awk '{print $3}')
    rm -rf "${d:?}/$path"
    git clone -q --shared --no-checkout "$src" "$d/$path"; git -C "$d/$path" checkout -q --detach "$rev"
  done
  if [ "$EDITS" != none ]; then python3 "$EDITS" "$d"; fi
  touch "$d/.r391-ready"
fi
case "$TGT" in
setup) echo "parent-$NAME ready" ;;
cosim-quick)
  (cd "$d/tb/verilator/nvm_cosim" && python3 -B run_cases.py --shapes 1x1 --jobs 4 --pool 4 --skip-mutants) \
    > "$S/$NAME-cosim-quick.log" 2>&1 && rc=0 || rc=$?
  echo "$NAME cosim-quick rc=$rc"; grep -E 'checks|FAIL' "$S/$NAME-cosim-quick.log" | grep -v '^\s*PASS' | tail -20 || true ;;
dp)
  t=$1; shift
  make -C "$d/tb/verilator/milan_dp" "$t" "$@" > "$S/$NAME-dp-$t.log" 2>&1 && rc=0 || rc=$?
  echo "$NAME milan_dp $t rc=$rc"; grep -E '^checks:|^RESULT|FAIL' "$S/$NAME-dp-$t.log" | tail -20 || true ;;
*) echo "unknown target $TGT"; exit 2 ;;
esac
