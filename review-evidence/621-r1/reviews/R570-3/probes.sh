#!/usr/bin/env bash
# R570-3 disposable probes for PR #707 at 83239549. Usage:
#   probes.sh <repo-root> <packet-dir> <verilator>
# Writes only under <packet-dir>/scratch/probe and <packet-dir>/receipts.
set -u
ROOT=$(cd "$1" && pwd); PKT=$(cd "$2" && pwd); VER=$3
S=$PKT/scratch/probe; R=$PKT/receipts
rm -rf "$S"; mkdir -p "$S/src/a/b" "$R"
ln -s "$ROOT/tb/common" "$S/src/common"
TB=$ROOT/tb/verilator/gptp_plane
GEN=$ROOT/gptp-processor/hdl/ucode/gen_gptp_ucode.py
HEADBIN=$PKT/scratch/head/work/obj/phc_step

# h0: head harness plus one diagnostic line per silence arm (no behaviour change).
python3 -I - "$TB/sim_phc_step.cpp" "$S/src/a/b/h0.cpp" "$S/src/a/b/h1.cpp" <<'EOF'
import sys
src = open(sys.argv[1]).read()
old = '    return steps_ - initial_steps;\n  }\n'
assert src.count(old) == 1
diag = ('    printf("DIAG %s probe_request=%llu probe_stamp=%llu step=%llu probe_response=%llu fu=%llu\\n", name,\n'
        '           (unsigned long long)probe_request_, (unsigned long long)probe_stamp_,\n'
        '           (unsigned long long)last_step_cycle_, (unsigned long long)probe_response_,\n'
        '           (unsigned long long)probe_follow_up_);\n')
h0 = src.replace(old, diag + old)
open(sys.argv[2], 'w').write(h0)
# h1: fault - the peer answers the crossing request even when told not to.
old1 = '    if (!answer_ || !answer_probe_) return;\n'
assert h0.count(old1) == 1
open(sys.argv[3], 'w').write(h0.replace(old1, '    if (!answer_) return;\n'))
EOF

# Generator variants.
python3 -I - "$GEN" "$S" <<'EOF'
import sys, os
src = open(sys.argv[1]).read(); out = sys.argv[2]
def plant(scope, old, new):
    s = src.index(f"\ndef {scope}("); e = src.find("\ndef ", s + 1)
    region = src[s:e]
    assert region.count(old) == 1, scope
    return src[:s] + region.replace(old, new) + src[e:]
cease = "    _tmr_cease_rule(p)\n"
credit = ('    p.emit("RDST", rd=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n'
          '    p.emit("CMP", ra=RT, rb=0, fmt=FMT_D, imm=0)\n'
          '    p.emit("BRS", cnd=BRS_Z, label="r571_skip")\n'
          '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n'
          '    p.label("r571_skip")\n')
v = {}
# g1: the same credit plant, cease rule kept: tests the "no free ROM word" claim.
v["g1-romroom"] = plant("prog_tmr", cease, cease + credit)
# g2: independent defect - credit liveness at the moment of the servo step.
step = '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDSTEP, fmt=FMT_Q)\n'
g2 = plant("prog_leg_servo", step,
           step + '    p.emit("WRST", ra=RT, imm=RG_SCR | S_PDGOT, fmt=FMT_Q)\n')
# the same ROM-room deletion the campaign's plant uses
s2 = g2.index("\ndef prog_tmr("); e2 = g2.find("\ndef ", s2 + 1)
assert g2[s2:e2].count(cease) == 1
v["g2-credit-at-step"] = g2[:s2] + g2[s2:e2].replace(cease, "") + g2[e2:]
for name, text in v.items():
    os.makedirs(f"{out}/{name}", exist_ok=True)
    open(f"{out}/{name}/generate.py", "w").write(text)
os.makedirs(f"{out}/clean", exist_ok=True)
open(f"{out}/clean/generate.py", "w").write(src)
EOF

build() {  # $1 = variant name
  local d=$S/obj_$1
  "$VER" --cc --exe --build -j 8 --top-module gptp_plane_wrap --Mdir "$d" \
    -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
    -Wno-UNUSEDPARAM -GCLK_HZ_P=8000000 -GPHC_INCR_P=2097152000 \
    -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
    "$TB/gptp_plane_wrap.sv" "$ROOT/hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv" \
    "$ROOT/gptp-processor/hdl/ucpu/gptp_ucpu_pkg.sv" "$ROOT/gptp-processor/hdl/ucpu/KL_gptp_ucpu.sv" \
    "$ROOT/gptp-processor/hdl/wire/KL_gptp_rx_parser.sv" "$ROOT/gptp-processor/hdl/wire/KL_gptp_tx_slot.sv" \
    "$ROOT/gptp-processor/hdl/common/KL_gptp_timer.sv" "$ROOT/gptp-processor/hdl/top/KL_gptp_engine.sv" \
    "$S/src/a/b/$1.cpp" -o phc_step > "$S/build_$1.log" 2>&1
  echo $? > "$S/build_$1.rc"
}
gen() {  # $1 = generator dir
  (cd "$S/$1" && python3 generate.py --clk-hz 8000000 -o gptp_ucode.hex > generate.log 2>&1; echo $? > generate.rc)
}
run() {  # $1 = rom dir, $2 = binary, $3 = log name
  (cd "$S/$1" && "$2" > "$3.log" 2>&1; echo $? > "$3.rc")
}

build h0 & build h1 & gen clean & gen g1-romroom & gen g2-credit-at-step & wait
[ "$(cat "$S/g2-credit-at-step/generate.rc")" = 0 ] && run g2-credit-at-step "$HEADBIN" head &
[ "$(cat "$S/build_h0.rc")" = 0 ] && run clean "$S/obj_h0/phc_step" h0 &
[ "$(cat "$S/build_h1.rc")" = 0 ] && run clean "$S/obj_h1/phc_step" h1 &
wait

{
  for b in h0 h1; do echo "build $b rc=$(cat "$S/build_$b.rc")"; done
  for g in clean g1-romroom g2-credit-at-step; do
    echo "== generate $g rc=$(cat "$S/$g/generate.rc")"; tail -3 "$S/$g/generate.log"
  done
  for pair in "g2-credit-at-step head" "clean h0" "clean h1"; do
    set -- $pair
    echo "== run $1 with $2 rc=$(cat "$S/$1/$2.rc" 2>/dev/null)"
    grep -E '^(DIAG|LOSS|ARM (liveness|unanswered))|\[FAIL\]|checks:' "$S/$1/$2.log" 2>/dev/null
  done
} | tee "$R/probes_summary.log"
for f in "$S"/*/h0.log "$S"/*/h1.log "$S"/*/head.log; do [ -f "$f" ] && cp "$f" "$R/probe_$(basename "$(dirname "$f")")_$(basename "$f")"; done
