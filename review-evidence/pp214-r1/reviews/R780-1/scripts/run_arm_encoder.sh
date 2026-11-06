#!/bin/sh
# run_arm_encoder.sh <packet> <arm>: PV suite + fuzz on one reviewer arm
P=$1; A=$2; S=$P/scratch; W=$S/mut/$A; V=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
rm -rf "$W"; mkdir -p "$W"; cp -r "$S/head/hdl" "$S/head/tb" "$W/"; mkdir -p "$W/tb_keep"
python3 -I "$P/scripts/reviewer_mutants.py" "$W" "$A" || { echo "$A APPLYFAIL"; exit 0; }
cd "$W/tb/srp_encoder" && timeout 300 make VERILATOR=$V run > "$P/receipts/mut/$A.enc.log" 2>&1; rc=$?
fails=$(grep -c '^FAIL\|FAIL:' "$P/receipts/mut/$A.enc.log")
tally=$(tail -3 "$P/receipts/mut/$A.enc.log" | grep 'checks:' | tail -1)
"$P/scripts/fuzz/build.sh" "$W" "$W/fz" 12 >/dev/null 2>&1
fz=$(timeout 120 "$W/fz/obj_dir/Vsrp_sim" 11 400000 5 2>&1 | tail -1 | sed 's/.*dup_frames/dup_frames/')
echo "$A | enc_rc=$rc | $tally | fuzz: $fz"
