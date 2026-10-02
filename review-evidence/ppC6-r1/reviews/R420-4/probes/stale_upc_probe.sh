#!/bin/sh
# Reviewer probe (R420-4): plant a stale relocation in a private copy of the
# head export - the engine's UPC_IDNOTIF_C or UPC_SINFOUNS_C left at round 3's
# word (2000 / 2016, now READ_DESCRIPTOR's overlays) - and show which gate and
# which graded checks see it. Usage: stale_upc_probe.sh HEAD_EXPORT WORK_DIR
set -eu
src=$1; work=$2
for arm in idnotif sinfouns; do
  w="$work/$arm"; rm -rf "$w"; mkdir -p "$w"
  cp -a "$src/hdl" "$src/tb" "$src/scripts" "$w/"
  rm -rf "$w/tb/pp_top"/obj_*
  case $arm in
    idnotif)  old="UPC_IDNOTIF_C  = 11'd464;";  new="UPC_IDNOTIF_C  = 11'd2000;";;
    sinfouns) old="UPC_SINFOUNS_C = 11'd480;";  new="UPC_SINFOUNS_C = 11'd2016;";;
  esac
  python3 - "$w/hdl/aecp/KL_aecp_engine.sv" "$old" "$new" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
assert s.count(sys.argv[2]) == 1, "anchor"
p.write_text(s.replace(sys.argv[2], sys.argv[3]))
PY
  echo "== $arm: check_upc_map.py"
  (cd "$w" && python3 scripts/check_upc_map.py 2>&1 | tail -3) || true
  echo "== $arm: graded run"
  if [ $arm = idnotif ]; then
    (cd "$w/tb/pp_top" && make identify-build > build.log 2>&1 && ./obj_idn/Vpp_top_idn | grep -E '^FAIL|checks, [0-9]+ failures' | head -8) || true
  else
    (cd "$w/tb/pp_top" && make gsi-build > build.log 2>&1 && ./obj_dir/Vpp_top_sim --notify-only | grep -E '^FAIL|checks, [0-9]+ failures' | head -8) || true
  fi
done
