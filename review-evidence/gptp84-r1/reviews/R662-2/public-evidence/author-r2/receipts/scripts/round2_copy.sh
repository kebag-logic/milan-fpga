#!/bin/sh
# Copies every Round 2 receipt cited by HANDOFF.md into receipts/round2/,
# scrubbed by receipts.py, then regenerates receipts/INDEX.md from the files
# present. Scratch logs stay in the scratch.
set -e
S=<scratch>
R=$S/r2
C="python3 $S/scripts/receipts.py copy"
cp_dir() {  # <src-dir> <dst-rel> [glob]
  for f in "$1"/${3:-*}; do
    [ -f "$f" ] || continue
    case "$f" in *.nohup) continue;; esac
    $C "$f" "round2/$2/$(basename "$f")"
  done
}
cp_dir $R/lane-head lane-head-093b9c3b '*.log'
$C $R/lane-head/rc.txt round2/lane-head-093b9c3b/rc.txt
cp_dir $R/lane-head/engine-mutants lane-head-093b9c3b/engine-mutants
cp_dir $R/lane-head2 lane-head-2022d363 '*.log'
$C $R/lane-head2/rc.txt round2/lane-head-2022d363/rc.txt
cp_dir $R/lane-head2/engine-mutants lane-head-2022d363/engine-mutants
$C $R/img3/gen.log round2/lane-images/gen.log
$C $R/img3/images.txt round2/lane-images/images.txt
$C $R/img2/gen.log round2/lane-images-093b9c3b/gen.log
$C $R/img2/images.txt round2/lane-images-093b9c3b/images.txt
$C $R/d-vs-e.txt round2/d-vs-e.txt
$C $R/parent-consumer.json round2/parent-consumer-template-copy.json
cp_dir $R/adoptionE parent-adoption-564466ea
cp_dir $R/adoptionE/builder parent-adoption-564466ea/builder
cp_dir $R/adoptionE/milan_dp parent-adoption-564466ea/milan_dp
cp_dir $R/adoptionE/gm_steps parent-adoption-564466ea/milan_dp_gm_steps
cp_dir $R/adoptionE/milan_dp_gptp parent-adoption-564466ea/milan_dp_gptp
cp_dir $R/logs/base parent-base-f3379118
cp_dir $R/logs/h2 parent-head-e347b8a0
cp_dir $R/logs/mut-85 parent-snapB-6814d01c/mutants-milan_dp-gptp
cp_dir $R/logs/snapB parent-snapB-6814d01c/suites
cp_dir $R/adoption parent-adoption-3f053cc1
cp_dir $R/adoption/builder parent-adoption-3f053cc1/builder
cp_dir $R/adoption/milan_dp parent-adoption-3f053cc1/milan_dp
cp_dir $R/adoption/gm_steps parent-adoption-3f053cc1/milan_dp_gm_steps
cp_dir $R/logs/snapD parent-adoption-3f053cc1/milan_dp_gptp
cp_dir $R/logs/mut-D parent-adoption-3f053cc1/mutants-milan_dp-gptp
cp_dir $R/logs/phys-mut parent-adoption-3f053cc1/mutants-milan_dp_gptp
$C $R/apply-check.log round2/companions/apply-check.log
$C $R/snapshots.txt round2/snapshots.txt
for f in suite.sh parent_mut_dp.py mk_worktree.sh round2_copy.sh receipts.py \
         parent_gates.py builder_b.sh builder_rest.sh builder_union.py \
         mutall.sh mutslice.py gate.sh; do
  $C $S/scripts/$f scripts/$f
done
python3 $S/scripts/receipts.py index
