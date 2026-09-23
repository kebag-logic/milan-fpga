#!/bin/sh
# Copy the run logs this round's report cites out of the disposable scratch
# tree into receipts/, then replace host-specific path prefixes in every
# receipt with neutral placeholders (nothing else is altered), and refuse if
# any host path is left in a publishable file.
# Usage: PKT=<packet> CLONE=<clone> VERILATOR=<pinned wrapper> \
#        WORK_ROOT=<common parent of the three> 90_publish_receipts.sh
set -eu
: "${PKT:?}" "${CLONE:?}" "${VERILATOR:?}" "${WORK_ROOT:?}"
S="$PKT/scratch/head/tb/verilator"
R="$PKT/receipts"
VROOT=$(sed -n 's/.*VERILATOR_ROOT=\([^ ]*\)\/share\/verilator .*/\1/p' "$VERILATOR")
san() {
  sed -e "s#$VROOT#<pinned-verilator-root>#g" \
      -e "s#$VERILATOR#<pinned-verilator-5.050>#g" \
      -e "s#$PKT#<packet>#g" \
      -e "s#$CLONE#<clone>#g" \
      -e "s#$HOME#\$HOME#g" \
      -e "s#$WORK_ROOT#<work-root>#g"
}
pub() { san < "$1" > "$R/$2"; }
pub "$S/media_grid_align/run.log"                 mga_head_make_run.log
pub "$S/media_grid_align/build.log"               mga_head_build.log
pub "$S/media_grid_align/obj_mut_usign/mut.log"   mga_head_MGA_MUT_U_SIGN.log
pub "$S/media_grid_align/obj_mut_keepoff/mut.log" mga_head_MGA_MUT_NO_KEEPOFF.log
pub "$S/media_grid_align/obj_mut_coin/mut.log"    mga_head_MGA_MUT_COIN.log
pub "$S/chmap_capture/run.log"                    chmap_head_run.log
pub "$S/chmap_capture/build.log"                  chmap_head_build.log
for v in head k8 k12 k24 base; do
  pub "$S/media_grid_align_probe/run_$v.log"      "probe100_$v.log"
done
pub "$S/media_grid_align_probe50/run_p50.log"     probe50_default_keepoff.log
pub "$S/media_grid_align_probe50/run_p50k0.log"   probe50_keepoff0.log
# the probe sources as diffs against the head harness (what each probe changed)
( cd "$S" &&
  { diff -u media_grid_align/sim_main.cpp media_grid_align_probe/sim_main.cpp || true
    diff -u media_grid_align/media_grid_align_wrap.sv media_grid_align_probe/media_grid_align_wrap.sv || true
    diff -u media_grid_align_probe/sim_main.cpp media_grid_align_probe50/sim_main.cpp || true
    diff -u media_grid_align_probe/media_grid_align_wrap.sv media_grid_align_probe50/media_grid_align_wrap.sv || true
  } ) | san > "$R/probe_sources.diff"
pub "$PKT/scratch/checkruns.tsv"        hosted_checkruns_2accfadf.tsv
pub "$PKT/scratch/docs_check_steps.txt" hosted_docs_check_steps_2accfadf.txt
# tool identity
B="$VROOT/bin/verilator"
{
  echo "wrapper: $("$VERILATOR" --version)"
  echo "wrapper sha256: $(sha256sum < "$VERILATOR" | cut -d' ' -f1)"
  echo "wrapped verilator script sha256: $(sha256sum < "$B" | cut -d' ' -f1)"
  echo "verilator_bin sha256: $(sha256sum < "$VROOT/bin/verilator_bin" | cut -d' ' -f1)"
} > "$R/tool_identity.txt"
# sanitise every receipt in place (covers the receipts written directly)
for f in "$R"/*; do san < "$f" > "$f.san"; mv "$f.san" "$f"; done
# refuse a host path in anything publishable
left=$(grep -l -F -e "$WORK_ROOT" -e "$HOME" "$R"/* "$PKT"/scripts/* 2>/dev/null || true)
if [ -n "$left" ]; then echo "HOST PATH LEFT IN: $left"; exit 1; fi
echo "receipts published: $(ls "$R" | wc -l) files, no host path left"
