#!/usr/bin/env bash
# Reviewer probe (R313-1): disposable RTL mutants of KL_nvm_backend.sv graded by
# the head's tb/verilator/nvm_backend harness at the 8x8 shape, to show the
# grown-output checks (test_output_boundaries) can fail for the defects they
# claim. Usage: backend_mutants.sh <head-tree-copy> <verilator> <workdir>
# The tree copy is only read; mutated sources and builds go under <workdir>.
set -u
T="$1"; V="$2"; W="$3"
TB="$T/tb/verilator/nvm_backend"
SRC="$T/hdl/milan/KL_nvm_backend.sv"
NN=$(sed -n 's/.*AEM_NAME_ENTRIES_C = \([0-9]*\);.*/\1/p' "$T/configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh")
SHAPE="-GCLK_HZ_P=10000 -GT_ALIVE_MS_P=4 -GT_COMMIT_MS_P=6 -GT_HOLD_MS_P=2 -GN_STREAM_IN_P=9 -GN_STREAM_OUT_P=9 -GN_SPORT_IN_P=8 -GN_SPORT_OUT_P=8 -GN_AUDIO_UNIT_P=1 -GN_CLK_DOM_P=1 -GN_NAME_P=$NN"
mkdir -p "$W"
declare -A FROM TO
# one_over: every output record accepts one byte past its framed length
FROM[one_over]="      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);"
TO[one_over]="      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]) + 12'd1;"
# nine_bit: the output length field cannot hold the grown 584-byte length
FROM[nine_bit]="      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);"
TO[nine_bit]="      rec_len_w  = 12'(9'(mapo_len_r[mapo_idx_w]));"
# stale_prefix: output ports after port 0 resolve one old (80-byte) record short
FROM[stale_prefix]="      rec_base_w = b_mapo_w + 18'(mapo_pref_r[mapo_idx_w]);"
TO[stale_prefix]="      rec_base_w = b_mapo_w + 18'(mapo_pref_r[mapo_idx_w]) - ((mapo_idx_w != '0) ? 18'd504 : 18'd0);"
rc_all=0
for m in one_over nine_bit stale_prefix; do
  d="$W/mut_$m"; mkdir -p "$d"
  python3 - "$SRC" "$d/KL_nvm_backend.sv" "${FROM[$m]}" "${TO[$m]}" <<'PY'
import sys
src, dst, a, b = sys.argv[1:]
t = open(src).read()
n = t.count(a)
assert n == 1, f"expected exactly one match, found {n}"
open(dst, "w").write(t.replace(a, b))
PY
  "$V" --cc --exe --build -j 8 --prefix Vnvm -Wall -CFLAGS "-std=c++17 -O2 -Wall -Wextra" \
     --Mdir "$d/obj" --top-module KL_nvm_backend $SHAPE "$d/KL_nvm_backend.sv" "$TB/sim_main.cpp" -o Vnvm >"$d/build.log" 2>&1
  if [ $? -ne 0 ]; then echo "mutant $m: BUILD FAILED (see build.log)"; rc_all=1; continue; fi
  ( cd "$TB" && "$d/obj/Vnvm" records_endstation_ax7101_8x8.txt ) >"$d/run.log" 2>&1
  r=$?
  nb=$(grep -c 'beyond capacity accepted\|whole output\|lost tail\|crossed span\|restoring output' "$d/run.log")
  echo "mutant $m: rc=$r, output-boundary check failures=$nb, first: $(grep -m1 '^FAIL' "$d/run.log")"
  grep 'checks:' "$d/run.log"
  [ $r -ne 0 ] && [ "$nb" -gt 0 ] || rc_all=1
done
exit $rc_all
