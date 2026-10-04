#!/bin/bash
# R456-3 scratch trees for #643 / PR #648 at 36207e91. Usage: r3_setup_trees.sh PACKET CLONE
# Each tree is a --shared clone of the review clone at the exact head, with its
# three submodules cloned --shared at their gitlinks (the suite's source list is
# read with git ls-files, so a plain copy does not build). hp, hp2, hp3, sl-hp:
# processor 631eeb34 (dev's pin). pc4c, c4b, sl-c4: processor c4cb84ff and both
# adoption patches applied to the parent tree, never committed.
set -eu
P=$1; R=$2; S=$P/scratch; H=36207e91c81fd33782b01486e3bc2fea50e91a1e
mk() {
  local t=$1 pp=$2
  [ -d "$S/$t/.git" ] || git clone -q --shared --no-checkout "$R" "$S/$t"
  git -C "$S/$t" checkout -q --detach $H
  for sm in protocol-processor gptp-processor third_party/verilog-axis; do
    [ -d "$S/$t/$sm/.git" ] && continue
    rmdir "$S/$t/$sm" 2>/dev/null || true
    git clone -q --shared --no-checkout "$R/$sm" "$S/$t/$sm"
  done
  git -C "$S/$t/protocol-processor" checkout -q --detach "$pp"
  git -C "$S/$t/gptp-processor" checkout -q --detach "$(git -C "$R" rev-parse $H:gptp-processor)"
  git -C "$S/$t/third_party/verilog-axis" checkout -q --detach "$(git -C "$R" rev-parse $H:third_party/verilog-axis)"
}
for t in hp hp2 hp3 sl-hp; do mk $t "$(git -C "$R" rev-parse $H:protocol-processor)"; done
for t in pc4c c4b sl-c4; do
  mk $t c4cb84ff8cecad19bedaa85dde594a8ed68012f6
  if [ -z "$(git -C "$S/$t" status --porcelain --ignore-submodules=all)" ]; then
    (cd "$S/$t" && git apply "$S/r2/inputs/parent-adoption-c8-bbf704ec.patch" \
                && git apply "$S/r2/inputs/parent-adoption-p2-p1-1269cdaf.patch")
  fi
done
git -C "$R" show 5fabb46e767c9308ab2580916237f43577698c6e:tb/verilator/milan_dp_render/sim_tdm8_render.cpp \
  > "$S/base_sim_tdm8_render.cpp"
for t in hp hp2 hp3 sl-hp pc4c c4b sl-c4; do
  echo "$t head=$(git -C "$S/$t" rev-parse HEAD) pp=$(git -C "$S/$t/protocol-processor" rev-parse HEAD)" \
       "dirty=$(git -C "$S/$t" status --porcelain --ignore-submodules=all | wc -l)"
done
