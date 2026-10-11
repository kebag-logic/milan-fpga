#!/usr/bin/env bash
# consumer_mutants.sh <tree> <out>: each existing guard bench this lane changed, on
# $error and $warning mutants of the guards it grades, each in a scratch copy.
set -u
tree=$1 out=$2; mkdir -p "$out"
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
PINNED=<scratch>/tools/bin:$PATH
HOST=<scratch>/tools/vbin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
arm() { # name file line-pattern task toolpath bench-dir target
  local name=$1 file=$2 pat=$3 task=$4 tp=$5 dir=$6 target=$7 t rc
  t=$(mktemp -d)
  cp -r "$tree/hdl" "$t/"; mkdir -p "$t/tb"; rsync -a --exclude 'obj_*' --exclude '*.hex' "$tree/tb/$dir" "$t/tb/"
  python3 -I - "$t/$file" "$pat" "$task" <<'PY'
import sys
path, pat, task = sys.argv[1:]
lines = open(path).read().split("\n")
hits = [i for i, l in enumerate(lines) if pat in l]
assert len(hits) == 1, (pat, hits)
i = hits[0] + 1
assert lines[i].count("$fatal(1, ") == 1, lines[i]
lines[i] = lines[i].replace("$fatal(1, ", task + "(")
open(path, "w").write("\n".join(lines))
PY
  ( cd "$t/tb/$dir" && PATH=$tp make $target VERILATOR=$VERILATOR ) > "$out/$name.log" 2>&1; rc=$?
  echo "$name rc=$rc :: $(grep -E 'FAIL|failing' "$out/$name.log" | head -3 | tr '\n' ' ' | cut -c1-260)"
  rm -rf "$t"
}
for task in '$error' '$warning'; do
  k=${task#\$}
  for tools in PINNED HOST; do
    arm "nvm_tmo_${k}_$tools" hdl/packet_engine/KL_pp_nvm_port.sv 'begin : g_tmo_check' "$task" "${!tools}" nvm_port elab
    arm "nvm_maxp_${k}_$tools" hdl/packet_engine/KL_pp_nvm_port.sv 'begin : g_maxp_check' "$task" "${!tools}" nvm_port elab
  done
  arm "avb_if_$k" hdl/top/protocol_processor_top.sv 'begin : gen_g_avb_if' "$task" "$PINNED" pp_top if-guards
  for g in gen_g_line_step gen_g_gamap_page_fit gen_g_line_ceiling; do
    arm "${g}_$k" hdl/aecp/KL_aecp_engine.sv "begin : $g" "$task" "$PINNED" pp_top line-guards
  done
done
