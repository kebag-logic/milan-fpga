#!/usr/bin/env bash
# Reviewer probe runner (R279-2). Builds disposable copies of the exact head
# under $PKT/scratch and runs the reviewer's acmp_nvm probes on:
#   head        - the exact head as published
#   oldcmp      - the head with the capture compare restored to its 156c206c
#                 form (the only RTL difference 156c206c..head besides comments
#                 and the elaboration guard), i.e. the failing arm
# usage: run_probes.sh <review clone> <packet dir> <verilator wrapper>
set -uo pipefail
CLONE=$1; PKT=$2; VER=$3
export PATH="$(dirname "$VER"):$PATH"
SCR=$PKT/scratch
mk() {  # mk <name>
  rm -rf "$SCR/$1"; mkdir -p "$SCR/$1"
  git -C "$CLONE" archive f8d30ecf44e3c1bb50bdc3a452e40d43d663f7f3 | tar -x -C "$SCR/$1"
  python3 "$PKT/scripts/apply_probes.py" "$SCR/$1" "$PKT/scripts/r279_probe_cases.cpp"
}
mk probe-head
mk probe-oldcmp
python3 - "$SCR/probe-oldcmp/hdl/acmp/KL_acmp_nvm_shadow.sv" <<'EOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
new = ("  assign c1_diff_w  = (c1_vld_r != valid_r[c1_sink_r])\n"
       "                    || (c1_vld_r && (SHW_W_C'(c1_proj_r) != cmp_data_w));\n")
old = ("  assign c1_diff_w  = (SHW_W_C'(c1_proj_r) != cmp_data_w)\n"
       "                    || (c1_vld_r != valid_r[c1_sink_r]);\n")
assert s.count(new) == 1
p.write_text(s.replace(new, old)); print("reverted compare in", p)
EOF
for t in probe-head probe-oldcmp; do
  ( cd "$SCR/$t/tb/acmp_nvm" && make ltn_rom.hex >/dev/null && \
    verilator --cc --exe --build -j 0 --top-module acmp_nvm_wrap -Wall -Wno-fatal \
      -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
      -Wno-UNUSEDPARAM -GDEB_TICKS_P=50 -GRS_TMO_CYC_P=3000 \
      -CFLAGS "-std=c++17 -O2 -I$PWD -Wall -Wextra" \
      ../../hdl/common/pp_pkg.sv ../../hdl/acmp/pp_acmp_pkg.sv \
      ../../hdl/acmp/KL_pp_acmp_listener.sv ../../hdl/acmp/KL_pp_acmp_lsn_admit.sv \
      ../../hdl/acmp/KL_acmp_nvm_shadow.sv ../../hdl/packet_engine/KL_pp_nvm_port.sv \
      ../../hdl/packet_engine/KL_pp_nvm_mgr_arb.sv acmp_nvm_wrap.sv sim_main.cpp \
      -o Vprobe >/dev/null 2>&1 ) &
done
wait
for t in probe-head probe-oldcmp; do
  echo "=== $t: reviewer probes only"
  ( cd "$SCR/$t/tb/acmp_nvm" && R279_ONLY=1 ./obj_dir/Vprobe; echo "exit $?" )
  echo "=== $t: full acmp_nvm bench"
  ( cd "$SCR/$t/tb/acmp_nvm" && ./obj_dir/Vprobe | grep -E '^FAIL|checks:'; echo "exit ${PIPESTATUS[0]}" )
done
