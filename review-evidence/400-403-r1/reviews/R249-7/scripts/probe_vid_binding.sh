#!/usr/bin/env bash
# Disposable probe: drop the composed datapath's generated-VID binding
# (.SRP_DOM_DEF_VID_P) and require pp_shadow's run-vid73 leg to fail; then
# restore the exact bytes and prove the blob id. Usage: probe_vid_binding.sh <checkout> <scratch>
set -u
repo=$1; scratch=$2; f=hdl/milan/milan_datapath.sv
cd "$repo" || exit 2
want=$(git rev-parse HEAD:$f)
cp -p "$f" "$scratch/milan_datapath.sv.orig" || exit 2
grep -c '\.SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C),' "$f"
sed -i '/\.SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C),/d' "$f"
git diff --stat -- "$f"
make -C tb/verilator/pp_shadow run-vid73 > "$scratch/probe_vid73.log" 2>&1
rc=$?
echo "mutant run-vid73 rc=$rc (nonzero required)"
grep -E '\[FAIL\]|checks, ' "$scratch/probe_vid73.log" | head -12
cp -p "$scratch/milan_datapath.sv.orig" "$f"
got=$(git hash-object "$f")
echo "restored blob=$got head=$want $([ "$got" = "$want" ] && echo IDENTICAL || echo DIFFERENT)"
[ "$rc" -ne 0 ] && [ "$got" = "$want" ]
