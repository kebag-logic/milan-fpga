#!/bin/bash
# The platform image and the size fixture at the four points, both linked with one runtime (the split boot
# simulation's), the platform against the boot SoC's csr.csv for its shape. The fixture's 8x8 two-interface
# point names its ledgered override; the platform's names none (no override recognises it).
# usage: images.sh CLONE SIMBUILD OUT LOGDIR
set -u
. $MANAGEMENT/2026-09-23/665s3-a697b/scripts/env.sh
C=$1 SB=$2 O=$3 L=$4
RT=$SB/boot-1x1/runtime
mkdir -p "$O" "$L"
cd "$C"
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    case $shape in *8x8) csv=$SB/boot-8x8/soc/csr.csv ;; *) csv=$SB/boot-1x1/soc/csr.csv ;; esac
    for n in 1 2; do
        led=(); [ "$shape-$n" = endstation_ax7101_8x8-2 ] && led=(--ledgered-point 8x8-two-interfaces)
        log=$L/image-plat-$shape-if$n.log
        { echo "HEAD $(git rev-parse HEAD)"; echo "\$ python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/$shape.yaml --interfaces $n --csr-csv <boot-soc>/csr.csv --output <out>/plat-$shape-$n --libc <runtime>/libc.a --compiler-runtime <runtime>/libcompiler_rt.a"; } > "$log"
        python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config "configs/$shape.yaml" --interfaces $n --csr-csv "$csv" \
            --output "$O/plat-$shape-$n" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" >> "$log" 2>&1
        echo "rc=$?" >> "$log"
        log=$L/image-fixture-$shape-if$n.log
        { echo "HEAD $(git rev-parse HEAD)"; echo "\$ python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/$shape.yaml --interfaces $n --with-aecp --layout split ${led[*]} --output <out>/fix-$shape-$n --libc <runtime>/libc.a --compiler-runtime <runtime>/libcompiler_rt.a"; } > "$log"
        python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$shape.yaml" --interfaces $n --with-aecp \
            --layout split "${led[@]}" --output "$O/fix-$shape-$n" --libc "$RT/libc.a" \
            --compiler-runtime "$RT/libcompiler_rt.a" >> "$log" 2>&1
        echo "rc=$?" >> "$log"
    done
done
#: the platform's largest point once more, naming the fixture's override: the override must refuse it too
shape=endstation_ax7101_8x8 log=$L/image-plat-$shape-if2-ledgered.log
{ echo "HEAD $(git rev-parse HEAD)"; echo "\$ python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/$shape.yaml --interfaces 2 --ledgered-point 8x8-two-interfaces --csr-csv <boot-soc>/csr.csv --output <out>/plat-$shape-2-ledgered --libc <runtime>/libc.a --compiler-runtime <runtime>/libcompiler_rt.a"; } > "$log"
python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config "configs/$shape.yaml" --interfaces 2 \
    --ledgered-point 8x8-two-interfaces --csr-csv "$SB/boot-8x8/soc/csr.csv" --output "$O/plat-$shape-2-ledgered" \
    --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" >> "$log" 2>&1
echo "rc=$?" >> "$log"
sha256sum "$RT/libc.a" "$RT/libcompiler_rt.a" | sed "s#$RT/##" > "$L/image-runtime.sha256"
echo "tree: $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s)" >> "$L/image-runtime.sha256"
