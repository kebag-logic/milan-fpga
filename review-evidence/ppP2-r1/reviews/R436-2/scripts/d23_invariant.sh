#!/usr/bin/env bash
# R436-2: D23's equivalence, as an invariant monitored in simulation. A probe
# copy of the head port gains one display-only always_ff: whenever owed_r is
# set, state_r must be S_IDLE, S_FIN, S_WHDR, S_WEREQ or S_RHREQ (never S_WWREQ
# or S_RPREQ, where D23 drops the guards). It runs under the PR's suite in five
# models and under the reviewer fuzz (legal, silent, resume) at 37 and 3.
#   d23_invariant.sh <head export> <work dir> <out dir>
set -euo pipefail
HEAD=$1; W=$2; OUT=$3
: "${VERILATOR:?}"
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W" "$OUT"
MON='  always_ff @(posedge clk_i) begin : r436_d23_monitor
    if (rst_n && owed_r && !((state_r == S_IDLE) || (state_r == S_FIN) || (state_r == S_WHDR)
                             || (state_r == S_WEREQ) || (state_r == S_RHREQ)))
      $display("D23-INVARIANT-VIOLATION state=%0d", state_r);
    if (rst_n && owed_r && ((state_r == S_WEREQ) || (state_r == S_RHREQ)))
      $display("D23-OWED-AT-FIRST-REQUEST state=%0d", state_r);
  end

endmodule'
python3 - "$HEAD/hdl/packet_engine/KL_pp_nvm_port.sv" "$W/port_mon.sv" "$MON" <<'EOF'
import sys
src, dst, mon = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src).read()
assert t.count("\nendmodule") == 1
open(dst, "w").write(t.replace("\nendmodule", "\n" + mon, 1))
EOF
run_model() { # name old new
  local m=$1 old=$2 new=$3 d="$W/suite_$1"
  rm -rf "$d"; mkdir -p "$d/hdl/packet_engine" "$d/tb"
  cp "$W/port_mon.sv" "$d/hdl/packet_engine/KL_pp_nvm_port.sv"
  cp -r "$HEAD/tb/nvm_port" "$HEAD/tb/common" "$d/tb/"
  rm -rf "$d/tb/nvm_port/obj_dir" "$d/tb/nvm_port/obj_alt"
  if [ -n "$old" ]; then
    python3 -c "import sys;p=sys.argv[1];t=open(p).read();assert t.count(sys.argv[2])==1;open(p,'w').write(t.replace(sys.argv[2],sys.argv[3],1))" \
      "$d/tb/nvm_port/sim_main.cpp" "$old" "$new"
  fi
  sed -i 's/--build -j 0/--build -j 2/' "$d/tb/nvm_port/Makefile"
  (cd "$d/tb/nvm_port" && make -s primary VERILATOR="$VERILATOR" > "$OUT/suite_$m.log" 2>&1) || true
  printf '%-12s %s | violations %s | owed-at-first-request %s\n' "$m" \
    "$(grep -E '^[0-9]+ checks' "$OUT/suite_$m.log" | tail -1)" \
    "$(grep -c D23-INVARIANT-VIOLATION "$OUT/suite_$m.log" || true)" \
    "$(grep -c D23-OWED-AT-FIRST-REQUEST "$OUT/suite_$m.log" || true)"
}
run_fuzz() { # tmo
  local t=$1
  "$HERE/build_fuzz.sh" "$W/port_mon.sv" "$t" "$W/fz$t"
  for mode in legal silent resume; do
    "$W/fz$t/Vfuzz" "$mode" 21 800 > "$OUT/fuzz_${t}_$mode.log" 2>&1 || true
    printf 'fuzz %-3s %-7s %s | violations %s | owed-at-first-request %s\n' "$t" "$mode" \
      "$(grep -E '^[0-9]+ checks' "$OUT/fuzz_${t}_$mode.log" | tail -1)" \
      "$(grep -c D23-INVARIANT-VIOLATION "$OUT/fuzz_${t}_$mode.log" || true)" \
      "$(grep -c D23-OWED-AT-FIRST-REQUEST "$OUT/fuzz_${t}_$mode.log" || true)"
  done
}
{
  run_model pristine "" "" &
  run_model coincident "  bool done_on_last_byte = false;" "  bool done_on_last_byte = true;" &
  run_model unsolicited "  bool unsol_model = false;" "  bool unsol_model = true;" &
  run_model silent "  bool silent_model = false;" "  bool silent_model = true;" &
  run_model short "  bool short_model = false;" "  bool short_model = true;" &
  run_fuzz 37 &
  run_fuzz 3 &
  wait
} | sort
