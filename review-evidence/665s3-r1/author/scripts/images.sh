#!/bin/bash
# The platform image and the size fixture at the four points, all linked with one runtime (the split boot
# simulation's, copied to the lane's scratch), the platform against the boot SoC's csr.csv for its shape. At 8x8
# with two interfaces each names its own ledgered override (ctrl_memory.LEDGERED). Then six runs that must be
# refused (exit 2): the platform's largest point without its override and with the fixture's, the platform's
# override at the platform's three other points, and the platform's override on the fixture's largest image.
# Each log ends with rc=<n> and want=<n>.
# usage: images.sh CLONE OUT LOGDIR
set -u
. $MANAGEMENT/2026-09-23/665s3-a697c/scripts/env.sh
C=$1 O=$2 L=$3
I=$VALIDATION_STORAGE/665s3-a697c/inputs
RT=$I/runtime
mkdir -p "$O" "$L"
cd "$C"
csv() { case $1 in *8x8) echo "$I/soc-8x8/csr.csv" ;; *) echo "$I/soc-1x1/csr.csv" ;; esac; }
# run LOG WANT TOOL SHAPE N OUTNAME [EXTRA...]
run() {
    local log=$1 want=$2 tool=$3 shape=$4 n=$5 name=$6; shift 6
    local args=(--config "configs/$shape.yaml" --interfaces "$n" "$@")
    local shown=("${args[@]}")
    if [ "$tool" = plat ]; then
        args+=(--csr-csv "$(csv "$shape")"); shown+=(--csr-csv "<boot-soc-$shape>/csr.csv")
        exe=sw/firmware/ctrl/test/ctrl_plat_image.py
    else
        args+=(--with-aecp --layout split); shown+=(--with-aecp --layout split)
        exe=sw/firmware/ctrl/test/ctrl_srp_image.py
    fi
    { echo "HEAD $(git rev-parse HEAD)"
      echo "\$ python3 $exe ${shown[*]} --output <out>/$name --libc <runtime>/libc.a --compiler-runtime <runtime>/libcompiler_rt.a"; } > "$L/$log"
    local start
    start=$(date +%s)
    python3 "$exe" "${args[@]}" --output "$O/$name" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" \
        >> "$L/$log" 2>&1
    local rc=$?
    echo "elapsed=$(( $(date +%s) - start ))s" >> "$L/$log"
    echo "rc=$rc" >> "$L/$log"
    echo "want=$want" >> "$L/$log"
}
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    for n in 1 2; do
        plat=(); fix=()
        if [ "$shape-$n" = endstation_ax7101_8x8-2 ]; then
            plat=(--ledgered-point platform-8x8-two-interfaces); fix=(--ledgered-point 8x8-two-interfaces)
        fi
        run "image-plat-$shape-if$n.log" 0 plat "$shape" "$n" "plat-$shape-$n" "${plat[@]}"
        run "image-fixture-$shape-if$n.log" 0 fix "$shape" "$n" "fix-$shape-$n" "${fix[@]}"
    done
done
big=endstation_ax7101_8x8
run refuse-plat-8x8-if2-no-override.log 2 plat "$big" 2 refuse-plat-none
run refuse-plat-8x8-if2-fixture-override.log 2 plat "$big" 2 refuse-plat-fix --ledgered-point 8x8-two-interfaces
run refuse-fixture-8x8-if2-platform-override.log 2 fix "$big" 2 refuse-fix-plat \
    --ledgered-point platform-8x8-two-interfaces
run refuse-plat-1x1-if1-platform-override.log 2 plat endstation_ax7101_1x1_tdm8 1 refuse-plat-11 \
    --ledgered-point platform-8x8-two-interfaces
run refuse-plat-1x1-if2-platform-override.log 2 plat endstation_ax7101_1x1_tdm8 2 refuse-plat-12 \
    --ledgered-point platform-8x8-two-interfaces
run refuse-plat-8x8-if1-platform-override.log 2 plat "$big" 1 refuse-plat-81 --ledgered-point platform-8x8-two-interfaces
( cd "$RT" && sha256sum libc.a libcompiler_rt.a ) > "$L/image-inputs.sha256"
( cd "$I" && sha256sum soc-1x1/csr.csv soc-8x8/csr.csv ) >> "$L/image-inputs.sha256"
echo "tree: $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s)" \
    >> "$L/image-inputs.sha256"
