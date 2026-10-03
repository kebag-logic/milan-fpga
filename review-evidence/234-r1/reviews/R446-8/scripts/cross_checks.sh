#!/usr/bin/env bash
# R446-8 cross-checks for PR #638 round 7 / 7b.
# usage: cross_checks.sh <repo> <scratch-dir>
# Needs origin/629-m2-review-evidence fetched in <repo> (PR #634's public packet).
set -u
repo=$1 work=$2
HEAD=68d26ea034789ce2519db22d0df4e4328bc1b0de
BASE=1269cdafb4bb964c757baae0f0c5a932d43f540b
DEV1=546437243e87eb5a78783a9e3cd5d1badcc3423e
DEV2=5fabb46e767c9308ab2580916237f43577698c6e
cd "$repo" || exit 2

echo "## 1. merges: parents and recomputed trees"
for m in 4d81e10d3a710cef3c8abc286fd68aeba4513f7c $HEAD; do
  p1=$(git rev-parse "$m^1"); p2=$(git rev-parse "$m^2")
  auto=$(git merge-tree --write-tree --no-messages "$p1" "$p2" | head -n 1)
  echo "$m parents $p1 $p2 recorded-tree $(git rev-parse "$m^{tree}") merge-tree $auto $([ "$auto" = "$(git rev-parse "$m^{tree}")" ] && echo EQUAL || echo DIFFERENT)"
done
echo "dev delta $DEV1..$DEV2:"; git diff --stat "$DEV1" "$DEV2" | tail -n 3
echo "PR vs live dev, build inputs (expect empty):"
git diff --stat "$DEV2" "$HEAD" -- hdl sw configs avdecc boards syn/yosys protocol-processor gptp-processor third_party external
echo "gitlinks at $BASE / $DEV1 / $DEV2 / $HEAD:"
for r in $BASE $DEV1 $DEV2 $HEAD; do git ls-tree "$r" protocol-processor gptp-processor third_party/verilog-axis external | awk '{printf "%s=%s ", $4, substr($3,1,8)} END {print ""}'; done

echo "## 2. shape headers regenerated at $BASE (A) and $HEAD (C)"
rm -rf "$work"; mkdir -p "$work/A" "$work/C"
git archive "$BASE" | tar -x -C "$work/A"; git archive "$HEAD" | tar -x -C "$work/C"
for t in A C; do for m in gptp-processor protocol-processor; do git -C "$m" archive HEAD | tar -x -C "$work/$t/$m"; done; done
for t in A C; do for c in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  (cd "$work/$t" && python3 sw/builder/endstation_builder.py -o "$work/$t/out-$c" "configs/$c.yaml" > "$work/$t/$c.log" 2>&1; echo "$t $c builder rc=$?")
  h="$work/$t/out-$c/$c/adp_shape_defaults.svh"
  for p in AEM_NAME_ENTRIES_C ADP_TALKER_SRC_C ADP_LISTENER_SINK_C ADP_SRP_DOM_DEF_VID_C ADP_DMAP_IN_NPORTS_C ADP_DMAP_OUT_NPORTS_C AEM_N_AUDIO_UNIT_C AEM_N_CLKDOM_C AEM_N_CONTROL_C AEM_N_CLKSRC_C; do
    printf '  %s %s\n' "$p" "$(grep -hE "\\b$p *=" "$h" | head -n 1 | sed 's/.*= *//')"
  done
done; done
echo "wrapper parameter bindings (milan_datapath.sv, KL_pp_shadow instance):"
awk '/^  KL_pp_shadow #\(/,/\) pp_shadow \(/' hdl/milan/milan_datapath.sv | grep -oE '\.[A-Z_]+_P *\([A-Za-z_]+\)'
echo "KL_pp_shadow \`include lines naming the shape header: $(grep -cE '^[[:space:]]*`include.*adp_shape_defaults' hdl/milan/KL_pp_shadow.sv)"
echo "KL_pp_shadow mentions of the header (comments): $(grep -n 'adp_shape_defaults' hdl/milan/KL_pp_shadow.sv)"

echo "## 3. AEM descriptor image, 1x1"
for t in A C; do
  c=endstation_ax7101_1x1_tdm8
  (cd "$work/$t" && python3 avdecc/gen_aemi_image.py -o "$work/$t/aem_desc.bin" --overlay "$work/$t/out-$c/$c/aem_overlay.json" > "$work/$t/aemi.log" 2>&1; echo "$t gen rc=$? bytes=$(stat -c %s "$work/$t/aem_desc.bin") sha256=$(sha256sum "$work/$t/aem_desc.bin" | cut -d' ' -f1)")
done

echo "## 4. PR #634's published hierarchical placed report of the same image"
rpt=review-evidence/629-m2-r1/author-r4/receipts/alinx_ax7101_utilization_hierarchical_place.rpt
git show "origin/629-m2-review-evidence:$rpt" > "$work/pr634_hier.rpt"
echo "source: origin/629-m2-review-evidence $(git rev-parse origin/629-m2-review-evidence):$rpt sha256 $(sha256sum "$work/pr634_hier.rpt" | cut -d' ' -f1)"
grep -E 'Design State' "$work/pr634_hier.rpt"
grep -E '^\| (alinx_ax7101 |  \(alinx_ax7101\)|  milan_datapath |  VexiiRiscvLitex[^ ]* |    (pp_shadow|g_aaf_meter.aaf_clock_meter|csr|media_nco|media_grid_align|g_mmcm_servo.mmcm_servo|aaf_latency_tap_bank|talker_diag|ctl_tx_mux|chan_map_capture) )' "$work/pr634_hier.rpt" \
  | awk -F'|' '{gsub(/^ +| +$/,"",$2); gsub(/ /,"",$4); gsub(/ /,"",$6); gsub(/ /,"",$8); print "  " $2 " LUT=" $4 " LUTRAM=" $6 " FF=" $8}'
git show "origin/629-m2-review-evidence:review-evidence/629-m2-r1/author-r4/receipts/alinx_ax7101_route_status.rpt" | grep -E 'routable nets|fully routed nets|routing errors'
git show "origin/629-m2-review-evidence:review-evidence/629-m2-r1/author-r4/receipts/alinx_ax7101_timing_summary_excerpt.txt" | sed -n '141p'
