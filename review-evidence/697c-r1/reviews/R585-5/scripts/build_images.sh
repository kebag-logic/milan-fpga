#!/bin/bash
# Build every RV32 image shape with a tree's OWN builders and hash the ELFs.
# Usage: build_images.sh TREE OUTDIR RUNTIME_DIR
#   TREE        a checkout (with lwSRP and, after #697, tsn-c-stack initialised)
#   OUTDIR      where images, logs and sha256.txt go
#   RUNTIME_DIR holds libc.a and libcompiler_rt.a (ctrl_image_runtime.py output)
# Needs MILAN_RV32_CC (the pinned SDK compiler). Runs up to 8 builds at once.
set -u
tree=$1; out=$2; rt=$3
mkdir -p "$out/logs"
cd "$tree" || exit 2
shapes=$(ls configs/*.yaml | sed 's#configs/##; s#\.yaml$##' | grep '^endstation_')
jobs=""
for s in $shapes; do
    echo "ctrl_image $s"
done > "$out/plan.txt"
run() {  # label, command...
    label=$1; shift
    "$@" > "$out/logs/$label.log" 2>&1
    echo "$label rc=$?" >> "$out/rc.txt"
}
: > "$out/rc.txt"
for s in $shapes; do
    run "ctrl_image-$s" python3 -B sw/firmware/ctrl/test/ctrl_image.py --shape "$s" --out "$out/img/ctrl_image" &
    for i in 1 2; do
        for c in --without-srp "" --with-aecp; do
            tag=$(echo "${c:-srp}" | sed 's/^--//')
            run "srp_image-$s-if$i-$tag" python3 -B sw/firmware/ctrl/test/ctrl_srp_image.py \
                --config "configs/$s.yaml" --interfaces "$i" --output "$out/img/srp/$s-if$i-$tag" \
                --libc "$rt/libc.a" --compiler-runtime "$rt/libcompiler_rt.a" $c &
            while [ "$(jobs -r | wc -l)" -ge 8 ]; do wait -n 2>/dev/null || sleep 1; done
        done
    done
done
wait
cd "$out" && find img -name '*.elf' -type f | sort | xargs sha256sum > sha256.txt
sort rc.txt -o rc.txt
