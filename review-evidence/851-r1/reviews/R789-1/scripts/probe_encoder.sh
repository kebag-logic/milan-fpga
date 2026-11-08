#!/usr/bin/env bash
# Build and run the processor's tb/srp_encoder suite at the pinned commit,
# unmodified or with one planted mutation, in a disposable extraction.
# usage: probe_encoder.sh <clone> <workdir> <name> <none|nomerge|joinnew> <out-dir>
set -u
CLONE=$1; WORK=$2; NAME=$3; MUT=$4; OUT=$5
PIN=044cb25f4ed2187bd238490650e73d5d189855d1
VERILATOR=${VERILATOR:?set VERILATOR}
D=$WORK/$NAME
rm -rf "$D"; mkdir -p "$D" "$OUT"
git -C "$CLONE/protocol-processor" archive "$PIN" hdl tb/common tb/srp_encoder | tar -x -C "$D"
F=$D/hdl/srp/KL_srp_encoder.sv
case "$MUT" in
  none) ;;
  nomerge)  # every push appends, as before issue #214
    sed -i 's/^  assign sr_hit_w    = sr_cont_w \&\& (q_key_w == sr_key_r);/  assign sr_hit_w    = 1'"'"'b0;/' "$F" ;;
  joinnew)  # a later join displaces a pending New
    sed -i 's/EV_JOININ_C, EV_JOINMT_C: return (old_e == EV_NEW_C) ? EV_NEW_C : new_e;/EV_JOININ_C, EV_JOINMT_C: return new_e;/' "$F" ;;
  *) echo "unknown mutation $MUT"; exit 9 ;;
esac
git -C "$CLONE/protocol-processor" show "$PIN:hdl/srp/KL_srp_encoder.sv" | diff - "$F" > "$OUT/$NAME.mutation.diff"
echo "mutation $MUT diff lines: $(wc -l < "$OUT/$NAME.mutation.diff")" > "$OUT/$NAME.log"
if [ "$MUT" != none ] && [ ! -s "$OUT/$NAME.mutation.diff" ]; then echo "mutation not applied" >> "$OUT/$NAME.log"; echo 8 > "$OUT/$NAME.rc"; exit 8; fi
( cd "$D/tb/srp_encoder" && make run VERILATOR="$VERILATOR" ) >> "$OUT/$NAME.log" 2>&1
echo $? > "$OUT/$NAME.rc"
