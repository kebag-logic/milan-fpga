#!/usr/bin/env bash
# Build the eleven ordinary milan_dp models of the `run` recipe at the head
# under review, without running gptp/gptp-lat/gmstep simulations, and replay
# the pre-pool Python steps of `run` (gen_divergent_shape.py via make, then
# gmstep-build's builder and image-generator lines, output redirected to a
# scratch directory) so the interpreter cache state matches a cold `make run`
# at the moment sim_pool.py starts.
#   usage: build_models.sh REPO VERILATOR SCRATCH JOBS prep|<1..11>|hash
# Split into steps only so that each step fits one foreground command.
set -euo pipefail
REPO=$1; VERILATOR=$2; SCRATCH=$3; JOBS=$4; STEP=$5
cd "$REPO/tb/verilator/milan_dp"
case "$STEP" in
prep)
  make -n run VERILATOR="$VERILATOR" VERILATOR_JOBS="$JOBS" > "$SCRATCH/dryrun.txt"
  # prerequisites: ROM/ucode images and the divergent shape (real make rules)
  make VERILATOR="$VERILATOR" ltn_rom.hex ucode.hex gptp_ucode.hex gen_divergent/gen/adp_shape_defaults.svh
  # gmstep-build's two Python lines, verbatim except the output directory
  python3 ../../../sw/builder/endstation_builder.py ../../../configs/endstation_ax7101_1x1_tdm8.yaml -o "$SCRATCH/gmstep/aem-build" > "$SCRATCH/gmstep-builder.log" 2>&1
  python3 ../../../avdecc/gen_aemi_image.py --overlay "$SCRATCH/gmstep/aem-build/endstation_ax7101_1x1_tdm8/aem_overlay.json" --line-bytes 576 -o "$SCRATCH/gmstep/aemi.bin" >> "$SCRATCH/gmstep-builder.log" 2>&1
  # the eleven model builds: every dry-run command after the gmstep run line
  # and before the pool's exec line, exactly as make would issue them, one
  # file per (possibly continued) command; echo lines are dropped
  rm -rf "$SCRATCH/builds"; mkdir -p "$SCRATCH/builds"
  awk -v d="$SCRATCH/builds" '
    /^\.\/obj_gmstep\/Vmilan_dp_gmstep /{on=1; next}
    /^exec python3 sim_pool.py/{on=0}
    !on {next}
    !cont && /^echo /{next}
    { if (!cont) n++; print > (d "/" n ".sh"); cont = /\\$/ }' "$SCRATCH/dryrun.txt"
  ls "$SCRATCH/builds" | wc -l
  ;;
hash)
  for m in obj_dir/Vmilan_dp_sim obj_notify/Vmilan_dp_notify obj_crflic/Vmilan_dp_crflic obj_nxn/Vmilan_dp_nxn obj_nxndv/Vmilan_dp_nxndv obj_nxn8/Vmilan_dp_nxn8 obj_nxn4c/Vmilan_dp_nxn4c obj_nolpf/Vmilan_dp_nolpf obj_prune/Vmilan_dp_prune obj_ax1x1/Vmilan_dp_ax1x1 obj_aclk/Vmilan_dp_aclk; do
    sha256sum "$m"
  done
  ;;
*)
  bash -e "$SCRATCH/builds/$STEP.sh"
  ;;
esac
