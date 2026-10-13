#!/bin/bash
# compare_images.sh : build the runtime archives once, link the 65 images at the head clone
# (runtime_nossp.py: ctrl_image_runtime.py plus -fno-stack-protector, as this SDK defaults to SSP)
# and at a clean clone of dev d5858bbe, and compare every ELF byte for byte.
set -u
. "$(dirname "$0")/env.sh"
S=$PACKET/scratch; DEV=$S/dev-d5858bbe; LW=${LITEX_BENCH:-$HOME/litex-milan}
rm -rf "$S/images" "$DEV"; mkdir -p "$S/images"
git clone -q --no-checkout "$CLONE" "$DEV" && git -C "$DEV" checkout -q d5858bbee328cf8d2c39a99ec14203f5d0ddd123 || exit 3
git clone -q "$CLONE/third_party/lwSRP" "$DEV/third_party/lwSRP.tmp" && rmdir "$DEV/third_party/lwSRP" && mv "$DEV/third_party/lwSRP.tmp" "$DEV/third_party/lwSRP" \
  && git -C "$DEV/third_party/lwSRP" checkout -q "$(git -C "$DEV" ls-tree HEAD third_party/lwSRP | awk '{print $3}')" || exit 3
for m in gptp-processor protocol-processor third_party/verilog-axis; do rmdir "$DEV/$m" && git clone -q "$CLONE/$m" "$DEV/$m" && git -C "$DEV/$m" checkout -q "$(git -C "$DEV" ls-tree HEAD $m | awk '{print $3}')" || exit 3; done
echo "dev clone: $(git -C "$DEV" rev-parse HEAD) lwSRP $(git -C "$DEV/third_party/lwSRP" rev-parse HEAD)"
PYTHONPATH="$CLONE/sw/firmware/ctrl/test:$CLONE/sw/firmware/gtest" python3 -B "$PACKET/scripts/runtime_nossp.py" \
  --picolibc "$LW/pythondata-software-picolibc/pythondata_software_picolibc/data" \
  --compiler-rt "$LW/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data" \
  --litex-software "$LW/litex/litex/soc/software" --output "$S/images/runtime" > "$S/images/runtime.log" 2>&1 || { echo runtime build failed; exit 3; }
sha256sum "$S/images/runtime/libc.a" "$S/images/runtime/libcompiler_rt.a"
"$(dirname "$0")/images.sh" "$CLONE" "$S/images/head" "$S/images/runtime"; h=$?
"$(dirname "$0")/images.sh" "$DEV" "$S/images/dev" "$S/images/runtime"; d=$?
cp "$S/images/head/manifest.sha256" "$PACKET/receipts/images_head.sha256"
cp "$S/images/dev/manifest.sha256" "$PACKET/receipts/images_dev.sha256"
echo "head build rc $h, dev build rc $d"
if diff "$S/images/head/manifest.sha256" "$S/images/dev/manifest.sha256" >/dev/null; then echo "manifests equal"; else echo "MANIFESTS DIFFER"; diff "$S/images/head/manifest.sha256" "$S/images/dev/manifest.sha256"; exit 1; fi
n=0; bad=0
while read -r _ f; do n=$((n+1)); cmp -s "$S/images/head/elf/$f" "$S/images/dev/elf/$f" || { echo "BYTES DIFFER $f"; bad=$((bad+1)); }; done < "$S/images/head/manifest.sha256"
echo "cmp: $n ELFs compared, $bad differ"
[ "$h$d$bad" = 000 ] && [ "$n" = 65 ]
