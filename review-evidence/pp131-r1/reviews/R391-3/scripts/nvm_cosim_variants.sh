#!/usr/bin/env bash
# Reviewer probe R391-3 item 4 (disposable, never committed): the parent's
# tb/verilator/nvm_cosim quick loop in scratch copies of the parent, with the
# processor tree exported at a chosen revision in place of the submodule.
# Usage: nvm_cosim_variants.sh <parent clone> <parent rev> <processor checkout> <scratch>
#                              <dir holding a Verilator 5.050 'verilator'> <variant> [jobs]
# variants:
#   base      processor c951a9ff (the parent's own pin), unchanged suite
#   head      processor cbbb5acc, cosim_top ties rs_agg_i 0 (the declared adoption edit)
#   ruled     as head, and cosim_top passes the shadow the top's own backoff derivation,
#             RETRY_BACKOFF_CYC_P = ceil(CLK_HZ_P / 2) (500 ms at the suite's 1 MHz clock)
#   ruledlong as ruled, and B1-B4 wait 2,600 ms instead of 1,500 ms before "gave_up",
#             past the debounce and both 500 ms backoffs
#   headlong  as head (the module's default backoff, 50,000,000 clocks = 50 s at 1 MHz),
#             and B1-B4 wait 102,000 ms before "gave_up", past both backoffs
set -euo pipefail
PAR=$1; PREV=$2; PP=$3; S=$4; VDIR=$5; VAR=$6; JOBS=${7:-8}
export PATH="$VDIR:$PATH"
d="$S/parent-$VAR"; rm -rf "$d"
# local clones (git ls-files is read by the shape generators); --shared never
# writes to the source repositories
git clone -q --shared --no-checkout "$PAR" "$d"; git -C "$d" checkout -q --detach "$PREV"
case "$VAR" in base) REV=c951a9ff0cb5851fb159d33e966e5a2a9a188fe3 ;;
               *)    REV=cbbb5acc77e9e068c3313d78ed4c1e5e79299a71 ;; esac
# the processor at REV and the other submodules the shape builder reads, at the
# parent's own gitlinks (GPTP and VAXIS name local clones of their public remotes)
for sm in protocol-processor:$PP:$REV gptp-processor:${GPTP:?}: third_party/verilog-axis:${VAXIS:?}:; do
  path=${sm%%:*}; rest=${sm#*:}; src=${rest%%:*}; rev=${rest#*:}
  [ -n "$rev" ] || rev=$(git -C "$PAR" ls-tree "$PREV" "$path" | awk '{print $3}')
  rm -rf "${d:?}/$path"
  git clone -q --shared --no-checkout "$src" "$d/$path"; git -C "$d/$path" checkout -q --detach "$rev"
done
T="$d/tb/verilator/nvm_cosim"
if [ "$VAR" != base ]; then
python3 - "$T/cosim_top.sv" "$VAR" <<'PY'
import sys
p, var = sys.argv[1:3]; s = open(p).read()
a = "      .restore_go_i     (restore_go_i),\n"
assert s.count(a) == 1
s = s.replace(a, a + "      .rs_agg_i         (1'b0),\n")
if var.startswith("ruled"):
    b = "      .RS_TMO_CYC_P (CLK_HZ_P / 32'd50)\n"
    assert s.count(b) == 1
    s = s.replace(b, "      .RS_TMO_CYC_P (CLK_HZ_P / 32'd50),\n"
                     "      .RETRY_BACKOFF_CYC_P ((CLK_HZ_P / 32'd2) + (CLK_HZ_P % 32'd2))\n")
open(p, "w").write(s)
PY
fi
if [ "$VAR" = ruledlong ] || [ "$VAR" = headlong ]; then
  ms=2600; [ "$VAR" = headlong ] && ms=102000
python3 - "$T/cosim_cases.cpp" "$ms" <<'PY'
import sys
p, ms = sys.argv[1:3]; s = open(p).read()
a = "      idle(1500);                      // debounce, three attempts, give-up\n"
assert s.count(a) == 1
s = s.replace(a, "      idle(%s);                      // R391-3: past the debounce and both backoffs\n" % ms)
open(p, "w").write(s)
PY
fi
(cd "$T" && python3 -B run_cases.py --shapes 1x1 --jobs "$JOBS" --pool "$JOBS" --skip-mutants) \
  > "$S/nvm_cosim-$VAR.log" 2>&1 && rc=0 || rc=$?
echo "variant $VAR rc=$rc"
grep -E 'B[1-4]_|FAIL|checks|PASS.*FAIL' "$S/nvm_cosim-$VAR.log" | grep -Ev '^\s*PASS' | tail -40 || true
