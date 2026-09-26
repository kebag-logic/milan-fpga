#!/usr/bin/env bash
# Disposable C++ diagnostic probes on copies of head sim_main.cpp (-O0 object
# compiles against the head models' generated headers, same -std/-Wall -Wextra
# as the Makefile; the fixture arm adds the fixture define). Nothing tracked is
# touched. Arms:
#   A  head as published, default and fixture          -> expect 0 warnings
#   B  head without [[maybe_unused]], fixture           -> expect -Wunused-function (R335-F1 reproduced)
#   C  head with the default-build call deleted, default -> the attribute also silences this
#   D  like C but the definition guarded #ifndef PP_TOP_SRP_DOM_DEF_VID instead of the attribute
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); H=$PK/scratch/head/tb/pp_top; W=$PK/scratch/cxx-probe; rm -rf $W; mkdir -p $W
VR=$HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator
[ -f $H/obj_dir/Vpp_top_wrap.h ] && [ -f $H/obj_vid/Vpp_top_wrap.h ] || { echo "run 04-pp_top.sh head first"; exit 2; }
DEF='[[maybe_unused]] static void run_name_writes(H& h) {'; CALL='  if (!gsi_only) run_name_writes(h);'
S=$H/sim_main.cpp; grep -qxF "$DEF" $S && grep -qxF "$CALL" $S || { echo "anchors missing"; exit 2; }
cp $S $W/A.cpp
sed "s/^\[\[maybe_unused\]\] static void run_name_writes/static void run_name_writes/" $S > $W/B.cpp
grep -vxF "$CALL" $S > $W/C.cpp
python3 - "$S" "$W/D.cpp" "$CALL" <<'PY'
import sys
t = open(sys.argv[1]).read(); call = sys.argv[3] + "\n"
start = t.index("[[maybe_unused]] static void run_name_writes"); end = t.index("\n}\n", start) + 3
fn = t[start:end].replace("[[maybe_unused]] ", "", 1)
t = t[:start] + "#ifndef PP_TOP_SRP_DOM_DEF_VID\n" + fn + "#endif\n" + t[end:]
open(sys.argv[2], "w").write(t.replace(call, "", 1))
PY
cxx() { # file model-dir extra-flags...
  f=$1; m=$2; shift 2
  out=$(g++ -std=c++17 -O0 -c -o /dev/null -Wall -Wextra -I$H -I$H/$m -isystem $VR/include -isystem $VR/include/vltstd "$@" $W/$f 2>&1); rc=$?
  n=$(printf "%s\n" "$out" | grep -c "^$W/$f:.* warning:"); echo "  $f $m $*: rc=$rc warnings=$n $(printf '%s\n' "$out" | grep "^$W/$f:.* warning:" | sed 's#.*/##' | head -2)"; }
FX=-DPP_TOP_SRP_DOM_DEF_VID=0x5A3C
echo "A (published head):"; cxx A.cpp obj_dir; cxx A.cpp obj_vid $FX
echo "B (attribute removed):"; cxx B.cpp obj_dir; cxx B.cpp obj_vid $FX
echo "C (default-build call deleted, attribute kept):"; cxx C.cpp obj_dir
echo "D (call deleted, #ifndef guard instead of attribute):"; cxx D.cpp obj_dir; cxx D.cpp obj_vid $FX
