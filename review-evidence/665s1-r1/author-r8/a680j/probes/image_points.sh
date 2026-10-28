#!/bin/bash
# Links the full F0-F5/F1 composition (ctrl_srp_image.py --with-aecp --layout split) at 1x1 and 8x8,
# one and two interfaces, in one tree, then plans each image (ctrl_memory.py plan, the shape's
# nvm_stage bytes). With $5 = ledgered, the 8x8 two-interface point alone is linked and planned with
# --ledgered-point 8x8-two-interfaces, and also planned without it, which must refuse.
#   $1 the tree   $2 a label   $3 the work directory   $4 the runtime directory   $5 ledgered|plain
set -u
T=$1 L=$2 W=$3/images RT=$4 MODE=$5
mkdir -p "$W"
failed=0
for point in "endstation_ax7101_1x1_tdm8 1 3344" "endstation_ax7101_1x1_tdm8 2 3344" \
             "endstation_ax7101_8x8 1 13264" "endstation_ax7101_8x8 2 13264"; do
    set -- $point
    out="$W/$L-$1-if$2"
    [ -e "$out" ] && { echo "$out exists"; exit 2; }
    over=()
    [ "$MODE" = ledgered ] && [ "$1" = endstation_ax7101_8x8 ] && [ "$2" = 2 ] && over=(--ledgered-point 8x8-two-interfaces)
    (cd "$T" && python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$1.yaml" --interfaces "$2" \
        --with-aecp --layout split --output "$out" --libc "$RT/libc.a" --compiler-runtime "$RT/libcompiler_rt.a" \
        "${over[@]}") > "$out.link.log" 2>&1
    rc=$?
    (cd "$T" && python3 sw/litex/ctrl_memory.py plan "$out/ctrl_app.elf" --stage-bytes "$3" "${over[@]}") \
        > "$out.plan.txt" 2>&1
    prc=$?
    echo "$L $1 if$2: link rc=$rc plan rc=$prc ${over[*]} tree=$(git -C "$T" rev-parse HEAD)"
    [ $rc = 0 ] && [ $prc = 0 ] || failed=$((failed + 1))
    if [ ${#over[@]} -gt 0 ]; then
        (cd "$T" && python3 sw/litex/ctrl_memory.py plan "$out/ctrl_app.elf" --stage-bytes "$3") \
            > "$out.plan-default.txt" 2>&1
        drc=$?
        echo "$L $1 if$2: plan without the override rc=$drc (must be 2): $(cat "$out.plan-default.txt")"
        [ $drc = 2 ] || failed=$((failed + 1))
        for other in "endstation_ax7101_1x1_tdm8-if1 3344" "endstation_ax7101_1x1_tdm8-if2 3344" \
                     "endstation_ax7101_8x8-if1 13264"; do
            set -- $other
            (cd "$T" && python3 sw/litex/ctrl_memory.py plan "$W/$L-$1/ctrl_app.elf" --stage-bytes "$2" \
                "${over[@]}") > "$W/$L-$1.plan-override.txt" 2>&1
            orc=$?
            echo "$L $1: plan with the override rc=$orc (must be 2): $(cat "$W/$L-$1.plan-override.txt")"
            [ $orc = 2 ] || failed=$((failed + 1))
        done
    fi
done
exit $((failed > 0))
