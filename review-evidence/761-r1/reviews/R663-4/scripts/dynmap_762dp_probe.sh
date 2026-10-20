#!/bin/sh
# Build and run the obj_dynmap leg (endstation_ax7101_1x1_tdm8, the obj_ax1x1
# argv) on a disposable copy of a source tree, optionally with one wiring
# mutation at the datapath's AAF stopped_i port, and record build/run logs,
# return codes and the [762-DP] / elaborated-parameter lines.
#
# usage: dynmap_762dp_probe.sh <src-tree> <work-dir> <variant> <verilator> [jobs]
#   variant: clean | tie0 | sink1 | bound
# The copy's own git status is recorded, so a probe proves which tree it built.
set -eu
src=$1; work=$2; variant=$3; vl=$4; jobs=${5:-4}
tree="$work/$variant/tree"; out="$work/$variant"
rm -rf "$out"; mkdir -p "$tree"
# copy the whole checkout, .git included: the build derives the
# protocol-processor source list with git ls-files, and the submodule
# gitdirs are relative, so the copy is self-contained
(cd "$src" && tar -cf - .) | (cd "$tree" && tar -xf -)
dp="$tree/hdl/milan/milan_datapath.sv"
orig='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),'
n=$(grep -cxF "$orig" "$dp")
[ "$n" = 1 ] || { echo "anchor count $n, expected 1" >&2; exit 3; }
case $variant in
  clean) new=$orig ;;
  tie0)  new="    .stopped_i      ('0)," ;;
  sink1) new='    .stopped_i      (acmpl_stopped_v_w[N_STREAMS:1]),' ;;
  bound) new='    .stopped_i      (acmpl_bound_v_w[N_STREAMS-1:0]),' ;;
  *) echo "unknown variant $variant" >&2; exit 2 ;;
esac
python3 -I - "$dp" "$orig" "$new" <<'EOF'
import sys
p, o, n = sys.argv[1:]
s = open(p).read()
assert s.count(o + "\n") == 1
open(p, "w").write(s.replace(o + "\n", n + "\n"))
EOF
diff -u "$src/hdl/milan/milan_datapath.sv" "$dp" | sed "s#$src#<src>#; s#$tree#<probe>#" > "$out/mutation.diff" || true
sha256sum "$dp" | sed "s#$tree/##" > "$out/datapath.sha256"
{ git -C "$tree" rev-parse HEAD; git -C "$tree" status --porcelain; } > "$out/tree-status.txt"
set +e
make -C "$tree/tb/verilator/milan_dp" dynmap-build VERILATOR="$vl" VERILATOR_JOBS="$jobs" > "$out/build.log" 2>&1
echo $? > "$out/build.rc"
if [ "$(cat "$out/build.rc")" = 0 ]; then
  (cd "$tree/tb/verilator/milan_dp" && ./obj_dynmap/Vmilan_dp_dynmap) > "$out/run.log" 2>&1
  echo $? > "$out/run.rc"
else
  echo NOT-RUN > "$out/run.rc"
fi
grep -F '[762-DP]' "$out/run.log" > "$out/762dp.txt" 2>/dev/null
grep -F 'elaborated' "$out/run.log" > "$out/elaborated.txt" 2>/dev/null
grep -F '[FAIL]' "$out/run.log" > "$out/failures.txt" 2>/dev/null
tail -3 "$out/run.log" > "$out/tally.txt" 2>/dev/null
exit 0
