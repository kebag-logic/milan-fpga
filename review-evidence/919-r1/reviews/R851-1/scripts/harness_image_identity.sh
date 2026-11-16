#!/usr/bin/env bash
# harness_image_identity.sh: the CPU service budget harness's firmware image (ctrl_srp_image.py, one interface,
# AECP, split layout), linked from the base tree (70f4056f) and the head tree (afa3ea19) with the same flash map and
# runtime archives (the review's split boot builds), at 1x1/1if and 8x8/1if; prints each ctrl_app.elf's sha256.
set -u
P=${PACKET:?export PACKET, this packet directory}
export PATH=${RV32_SDK:?export RV32_SDK, the pinned RV32 SDK host directory}/bin:/usr/local/bin:/usr/bin:/bin PYTHONHASHSEED=0
PY=${LITEX:?export LITEX, the product LiteX tree with its venv}/venv/bin/python3
for shape in 1x1:endstation_ax7101_1x1_tdm8 8x8:endstation_ax7101_8x8; do
  tag=${shape%%:*}; cfg=${shape#*:}; B=$P/scratch/boot-$tag
  for side in base:$P/scratch/basetree head:${CLONE}; do
    name=${side%%:*}; tree=${side#*:}; out=$P/scratch/himg/$tag-$name
    rm -rf "$out"
    (cd "$tree" && echo "$name $(git rev-parse HEAD) porcelain $(git status --porcelain | wc -l)" &&
     $PY -B sw/firmware/ctrl/test/ctrl_srp_image.py --config "$tree/configs/$cfg.yaml" --interfaces 1 --with-aecp \
       --layout split --flash-map "$B/split-soc/flash-map" --output "$out" --libc "$B/runtime/libc.a" \
       --compiler-runtime "$B/runtime/libcompiler_rt.a" > "$out.log" 2>&1; echo "rc=$?")
    echo "$tag $name ctrl_app.elf $(sha256sum < "$out/ctrl_app.elf" | cut -d' ' -f1)"
  done
done
