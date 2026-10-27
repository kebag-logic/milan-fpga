#!/bin/bash
# Reviewer campaigns for PR #207 at the exact head.
#   run_campaigns.sh prep  CLONE PACKET          build the disposable trees (git archive)
#   run_campaigns.sh waveN CLONE PACKET VERILATOR launch wave N detached, return at once
#   run_campaigns.sh wait  CLONE PACKET JOB...    wait (<= 540 s) for the named rc files
# The clone itself is never built in. Every job writes receipts/<job>.log and
# receipts/<job>.rc. Disposable copies build with a capped Verilator -j so the total
# stays within 16 parallel jobs per wave (results are independent of build parallelism).
set -u
MODE=$1; CLONE=$2; PK=$3
HEAD=7bad3943c6dc3a86814faa43aee53a1e8aab4a4f
BASE=097a7987
S=$PK/scratch; R=$PK/receipts
mkdir -p "$S" "$R"

capj() { sed -i "s/--build -j 0/--build -j $2/" "$1"; grep -q -- "--build -j $2" "$1"; }
mk() { rm -rf "$S/$1"; mkdir -p "$S/$1"; git -C "$CLONE" archive "$2" | tar -x -C "$S/$1"; }

case $MODE in
prep)
  mk head $HEAD; mk base $BASE; mk basertl $HEAD
  git -C "$CLONE" show $BASE:hdl/acmp/KL_acmp_talker.sv > "$S/basertl/hdl/acmp/KL_acmp_talker.sv"
  mk probe-head $HEAD; mk probe-basertl $HEAD
  git -C "$CLONE" show $BASE:hdl/acmp/KL_acmp_talker.sv > "$S/probe-basertl/hdl/acmp/KL_acmp_talker.sv"
  python3 -I "$PK/scripts/pp_top_probe.py" "$S/probe-head"
  python3 -I "$PK/scripts/pp_top_probe.py" "$S/probe-basertl"
  mk mut $HEAD; mk rvmut $HEAD; mk pptop $HEAD; mk gates $HEAD
  for t in head base basertl mut rvmut; do capj "$S/$t/tb/acmp_talker/Makefile" 2; done
  for t in probe-head probe-basertl; do capj "$S/$t/tb/pp_top/Makefile" 4; done
  capj "$S/pptop/tb/pp_top/Makefile" 12
  echo prep done ;;
wave*)
  V=$4; export PATH="$(dirname "$V"):$PATH" TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
  job() { local name=$1; shift; rm -f "$R/$name.rc"
    setsid nohup bash -c '( echo "# $0: ${*}"; date -u +%FT%TZ; "$@"; rc=$?; date -u +%FT%TZ; exit $rc ) \
      > "'"$R"'/$0.log" 2>&1; echo $? > "'"$R"'/$0.rc"' "$name" "$@" < /dev/null > /dev/null 2>&1 &
  }
  case $MODE in
  wave1)
    job talker-head      make -C "$S/head/tb/acmp_talker" run VERILATOR="$V"
    job talker-lint-head make -C "$S/head/tb/acmp_talker" lint VERILATOR="$V"
    job talker-base      make -C "$S/base/tb/acmp_talker" run VERILATOR="$V"
    job talker-basertl   make -C "$S/basertl/tb/acmp_talker" run VERILATOR="$V"
    job acmp-mutants-new python3 "$S/mut/tb/pp_top/acmp_mutants.py" --output "$R/acmp-mutants-new" \
        --verilator "$V" --jobs 3 --only tx_state_unknown_zeroes_listener \
        tx_state_unknown_not_fetched tx_state_success_echoes_listener
    job lint-hdl-head    bash -c "cd '$S/gates' && ./scripts/lint_hdl.sh"
    job make-check-head  bash -c "cd '$S/gates' && make check"
    job gen-matrix-head  bash -c "cd '$S/gates' && python3 scripts/gen_matrix.py --check" ;;
  wave2)
    job rv-mutants python3 "$PK/scripts/rv_mutants.py" --tree "$S/rvmut" \
        --output "$R/rv-mutants" --verilator "$V" --jobs 5
    job pptop-probe-head    make -C "$S/probe-head/tb/pp_top" rvprobe VERILATOR="$V"
    job pptop-probe-basertl make -C "$S/probe-basertl/tb/pp_top" rvprobe VERILATOR="$V" ;;
  wave3)
    job pptop-head make -C "$S/pptop/tb/pp_top" run VERILATOR="$V" ;;
  esac
  echo "$MODE launched" ;;
wait)
  shift 3
  for i in $(seq 1 108); do
    left=0; for j in "$@"; do [ -f "$R/$j.rc" ] || left=$((left+1)); done
    [ $left -eq 0 ] && break; sleep 5
  done
  for j in "$@"; do printf '%-22s rc=%s\n' "$j" "$(cat "$R/$j.rc" 2>/dev/null || echo PENDING)"; done ;;
esac
