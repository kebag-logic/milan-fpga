#!/bin/sh
# Reviewer probe (R469-3): plant one disposable edit per arm in its own
# git-archive copy of the reviewed clone and run tb/pp_top's sixth build
# (make timer-defaults). Each arm must fail its named TD check.
#   usage: probe_td_window.sh <clone> <scratch> <receipts> <arm>
# arms: lock-60030 (upper side of TD1), tl-299990 (lower side of TD2),
#       wrap-override-kept (the 400 ms overrides survive in the TD build)
set -eu
CLONE=$1; S=$2; R=$3; ARM=$4
T=$S/td-$ARM
rm -rf "$T"; mkdir -p "$T"
(cd "$CLONE" && git archive HEAD) | tar -x -C "$T"
TOPF=$T/hdl/top/protocol_processor_top.sv
WRAP=$T/tb/pp_top/pp_top_wrap.sv
case $ARM in
  lock-60030) sed -i 's/parameter int unsigned LOCK_TIMEOUT_MS_P   = 60_000,/parameter int unsigned LOCK_TIMEOUT_MS_P   = 60_030,/' "$TOPF"; F=$TOPF ;;
  tl-299990)  sed -i 's/parameter int unsigned REG_TL_TIMEOUT_MS_P = 300_000,/parameter int unsigned REG_TL_TIMEOUT_MS_P = 299_990,/' "$TOPF"; F=$TOPF ;;
  wrap-override-kept) sed -i '/^`ifndef PP_TOP_TIM_DEFAULTS$/d' "$WRAP"; awk 'BEGIN{d=0} /^`endif$/ && !d {getline nx; if (nx ~ /NVM_RS_TMO_CYC_P, NVM_RS_AGG_CYC_P/) {print nx; d=1; next} else {print; print nx; next}} {print}' "$WRAP" > "$WRAP.new" && mv "$WRAP.new" "$WRAP"; F=$WRAP ;;
  *) echo "unknown arm"; exit 2 ;;
esac
(cd "$CLONE" && git diff --no-index -- "$CLONE/${F#$T/}" "$F") > "$R/probe-td-$ARM.diff" || true
[ -s "$R/probe-td-$ARM.diff" ] || { echo "plant failed"; exit 3; }
set +e
make -C "$T/tb/pp_top" timer-defaults > "$R/probe-td-$ARM.log" 2>&1
echo $? > "$R/probe-td-$ARM.rc"
grep -E "^FAIL:|^\[build|\[TD\]" "$R/probe-td-$ARM.log"
