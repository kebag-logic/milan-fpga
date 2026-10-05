#!/bin/bash
# Prepare the disposable trees review R489-1 ran (all under <packet>/scratch).
# Usage: prep_trees.sh <clone> <packet-dir>
# head, base           : git archive of the exact head and of the PR base
# base-<mutant>        : the base tree with a new PR mutant planted (stage 2)
# old-<mutant>         : the head tree with an older campaign patch planted
# probe-<name>         : reviewer probes, built by make_probes.py
set -eu
C=$1; P=$2; S=$P/scratch
HEAD_SHA=5ab43bd98209ef3cde206b325c06f0e7405e1e86
BASE_SHA=ead8036035affd53ef4b29979190f2f4f67084c0
mkdir -p "$S"
fresh() { rm -rf "$1"; mkdir -p "$1"; }
fresh "$S/head"; git -C "$C" archive "$HEAD_SHA" | tar -x -C "$S/head"
fresh "$S/base"; git -C "$C" archive "$BASE_SHA" | tar -x -C "$S/base"
for m in lv-second-lv-ends lv-never-ends; do
  fresh "$S/base-$m"; git -C "$C" archive "$BASE_SHA" | tar -x -C "$S/base-$m"
  (cd "$S/base-$m" && git apply --check "$S/head/tb/srp_top/mutations/$m.patch" \
     && git apply "$S/head/tb/srp_top/mutations/$m.patch")
done
for m in talker-strict-lv talker-no-expiry; do
  fresh "$S/old-$m"; cp -r "$S/head/hdl" "$S/head/tb" "$S/old-$m/"
  (cd "$S/old-$m" && git apply "$S/head/tb/srp_top/mutations/$m.patch")
done
python3 "$P/scripts/make_probes.py" "$S/head" "$S" "$P/receipts/probe-diffs"
# the older patches run on the lvleave group only:
#   (cd $S/old-<m> && VERILATOR=$P/scripts/vl-wrap.sh make -C tb/srp_top RUN_ARGS=lvleave)
echo prepared
