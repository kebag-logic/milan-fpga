#!/usr/bin/env bash
# head-arms.sh <clone> <runs> <main-encoder.sv>: both reviews' arms, and every srp_encoder arm of the campaign with the
# base encoder, against tb/srp_encoder of the clean clone; the pinned Verilator
C=$1; R=$2; M=$3
. "$(dirname "$0")/common.sh"
mkdir -p "$R"
export PATH=$V/bin:$VL:$BASE
"$T/reviewer_arms.sh" $REVIEWS "$C" "$R/rv" > "$R/reviewer-arms.tsv" 2> "$R/reviewer-arms.err"
"$T/encoder_arm_counts.sh" "$C" "$R/enc" "$M" > "$R/encoder-arm-counts.tsv" 2> "$R/encoder-arm-counts.err"
