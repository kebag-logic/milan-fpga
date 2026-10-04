#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# run_campaign.sh PACKET_DIR PHASE   (PHASE: build-main | run-main | build-ctl | run-ctl | stall | stall2)
# Random lockstep campaign of head KL_srp_top against base (c4cb84ff).
set -u
P=$1; PHASE=$2
S=$P/scratch; B=$P/scripts/ls_rand/build.sh; J=${JOBS:-10}
SHAPES="1x1 2x2 3x3 3x5 5x3 4x4 8x8 9x9 2x9 9x2"
CTL_SHAPES="1x1 2x2 3x5 9x9"
RA="+verilator+rand+reset+2"
case $PHASE in
build-main)
  for sh in $SHAPES; do for cad in default compressed; do
    echo "$S/head/hdl $S/ls $S/r/$sh-$cad ${sh%x*} ${sh#*x} $cad"
  done; done | xargs -P "$J" -L 1 "$B"
  ;;
run-main)
  # 6 seeds x 3,000,000 cycles per shape and cadence; odd seeds noisy
  for sh in $SHAPES; do for cad in default compressed; do for seed in 1 2 3 4 5 6; do
    n=""; [ $((seed % 2)) = 1 ] && n="+noisy"
    c=""; [ "$cad" = compressed ] && c="+compressed"
    echo "cd $S/r/$sh-$cad && ./obj/Vtop +seed=$seed +cycles=3000000 $c $n $RA +verilator+seed+$((seed * 7 + 3)) > run-$seed.log 2>&1; echo \$? > run-$seed.rc"
  done; done; done | xargs -P "$J" -I{} bash -c "{}"
  ;;
build-ctl)
  python3 "$P/scripts/make_controls.py" "$S/head/hdl/srp" "$S/ctl" >/dev/null
  while IFS=$'\t' read -r name expect f; do for sh in $CTL_SHAPES; do
    echo "$S/head/hdl $S/ls $S/ctl/$name/b-$sh ${sh%x*} ${sh#*x} default $S/ctl/$name/srp"
  done; done < "$S/ctl/controls.tsv" | xargs -P "$J" -L 1 "$B"
  ;;
run-ctl)
  while IFS=$'\t' read -r name expect f; do for sh in $CTL_SHAPES; do for seed in 1 2 3; do
    echo "cd $S/ctl/$name/b-$sh && ./obj/Vtop +seed=$seed +cycles=500000 +ls_count $RA +verilator+seed+$((seed + 40)) > run-$seed.log 2>&1; echo \$? > run-$seed.rc"
  done; done; done < "$S/ctl/controls.tsv" | xargs -P "$J" -I{} bash -c "{}"
  ;;
stall)
  # Full-boundary probe: the SAME edit in base and head (TM_SEL issues
  # nothing while now_ms_i[6] is set), so both FIFOs fill to 32 and the
  # full guard acts; then two controls under the same stall.
  rm -rf "$S/ls_stall" "$S/stall"; cp -r "$S/ls" "$S/ls_stall"; mkdir -p "$S/stall"
  python3 - "$S" <<'EOF'
import pathlib, shutil, sys
S = pathlib.Path(sys.argv[1])
A = "        TM_SEL: begin\n          if ((tf_cnt_r[0] != 6'd0)"
Bs = "        TM_SEL: begin\n          if (now_ms_i[6]) begin end\n          else if ((tf_cnt_r[0] != 6'd0)"
def patch(p):
    s = p.read_text(); assert s.count(A) == 1, p; p.write_text(s.replace(A, Bs))
patch(S / "ls_stall/ref/KL_srp_top_ref.sv")
for name, src in [("plain", S / "head/hdl/srp"),
                  ("tf-ls-write-ignores-full", S / "ctl/tf-ls-write-ignores-full/srp"),
                  ("tf-tk-same-entry-bypass", S / "ctl/tf-tk-same-entry-bypass/srp")]:
    d = S / "stall" / name / "srp"; shutil.copytree(src, d); patch(d / "KL_srp_top.sv")
EOF
  for name in plain tf-ls-write-ignores-full tf-tk-same-entry-bypass; do for sh in 9x9 3x5 2x2; do
    echo "$S/head/hdl $S/ls_stall $S/stall/$name/b-$sh ${sh%x*} ${sh#*x} compressed $S/stall/$name/srp"
  done; done | xargs -P "$J" -L 1 "$B"
  for name in plain tf-ls-write-ignores-full tf-tk-same-entry-bypass; do for sh in 9x9 3x5 2x2; do for seed in 1 2 3 4; do
    echo "cd $S/stall/$name/b-$sh && ./obj/Vtop +seed=$seed +cycles=2000000 +compressed +ls_count $RA +verilator+seed+$((seed + 90)) > run-$seed.log 2>&1; echo \$? > run-$seed.rc"
  done; done; done | xargs -P "$J" -I{} bash -c "{}"
  ;;
stall2)
  # Run after `stall` and `build-ctl`. (a) the talker-side write-ignores-full
  # control under the bit-6 stall (the talker FIFO fills there); (b) a longer
  # stall (now_ms_i[8]) in base and head so the listener FIFO fills too, plain
  # and with the listener write-ignores-full control.
  python3 - "$S" <<'EOF'
import pathlib, shutil, sys
S = pathlib.Path(sys.argv[1])
A = "        TM_SEL: begin\n          if ((tf_cnt_r[0] != 6'd0)"
def B(bit): return f"        TM_SEL: begin\n          if (now_ms_i[{bit}]) begin end\n          else if ((tf_cnt_r[0] != 6'd0)"
def patch(p, bit):
    s = p.read_text(); assert s.count(A) == 1, p; p.write_text(s.replace(A, B(bit)))
d = S / "stall/tf-tk-write-ignores-full/srp"
if d.parent.exists(): shutil.rmtree(d.parent)
shutil.copytree(S / "head/hdl/srp", d)
s = (d / "KL_srp_top.sv").read_text()
a = "    if (tf_push_w[0]) begin\n      tf_tk_ram_r"; assert s.count(a) == 1
(d / "KL_srp_top.sv").write_text(s.replace(a, "    if (tk_arm_v_w) begin\n      tf_tk_ram_r"))
patch(d / "KL_srp_top.sv", 6)
ls8 = S / "ls_stall8"
if ls8.exists(): shutil.rmtree(ls8)
shutil.copytree(S / "ls", ls8); patch(ls8 / "ref/KL_srp_top_ref.sv", 8)
for name, src in [("plain8", S / "head/hdl/srp"), ("tf-ls-write-ignores-full8", S / "ctl/tf-ls-write-ignores-full/srp")]:
    dd = S / "stall" / name / "srp"
    if dd.parent.exists(): shutil.rmtree(dd.parent)
    shutil.copytree(src, dd); patch(dd / "KL_srp_top.sv", 8)
EOF
  printf '%s\n' "$S/head/hdl $S/ls_stall $S/stall/tf-tk-write-ignores-full/b-9x9 9 9 compressed $S/stall/tf-tk-write-ignores-full/srp" \
    "$S/head/hdl $S/ls_stall8 $S/stall/plain8/b-9x9 9 9 compressed $S/stall/plain8/srp" \
    "$S/head/hdl $S/ls_stall8 $S/stall/tf-ls-write-ignores-full8/b-9x9 9 9 compressed $S/stall/tf-ls-write-ignores-full8/srp" \
    | xargs -P 3 -L 1 "$B"
  for n in tf-tk-write-ignores-full plain8 tf-ls-write-ignores-full8; do for seed in 1 2 3 4; do
    echo "cd $S/stall/$n/b-9x9 && ./obj/Vtop +seed=$seed +cycles=2000000 +compressed +ls_count $RA +verilator+seed+$((seed + 90)) > run-$seed.log 2>&1; echo \$? > run-$seed.rc"
  done; done | xargs -P "$J" -I{} bash -c "{}"
  ;;
esac
echo "phase $PHASE done"
