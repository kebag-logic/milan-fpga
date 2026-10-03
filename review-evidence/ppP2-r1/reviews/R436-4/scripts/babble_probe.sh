#!/usr/bin/env bash
# babble_probe.sh VARIANT TMO : R436g, a reviewer-owned probe (never proposed
# as the PR's code). The head's tb/nvm_port/fuzz_main.cpp, babble mode only,
# with the abandoned READ's withheld obligation drawn from EVERY byte and
# terminal of a restore (header bytes 1-8, header terminal 9, payload bytes,
# payload terminal) instead of payload bytes only. FZ9 then grades that the
# port takes exactly the bytes the abandoned READ still owed and that the
# waiting request ends DEADLINE. VARIANT is "head" or a plant name from
# plants_drain.py. Prints the FZ9 line.
set -eu
P=$(cd "$(dirname "$0")/.." && pwd)
HEAD=3957814550f164d72bfaad5d28cd0e7cac0ecaaf
V=$1; T=$2
d=$P/scratch/babble/$V-$T; rm -rf "$d"; mkdir -p "$d"
git -C $REVIEWS/r436-4-ppP2 archive "$HEAD" hdl/packet_engine tb/nvm_port tb/common | tar -x -C "$d"
[ "$V" = head ] || python3 "$P/scripts/plants_drain.py" apply "$V" "$d/hdl/packet_engine/KL_pp_nvm_port.sv" >/dev/null
f=$d/tb/nvm_port/fuzz_main.cpp
python3 - "$f" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
old="  sil_n = 11 + rnd(0, int(af.size()) - 10);   // a payload byte\n"
new=("  sil_n = rnd(1, int(af.size()) + 2);          // [R436g] any byte or terminal of the restore\n"
     "  if (sil_n >= 10) ++sil_n;                     // ...never the payload grant (10)\n")
assert t.count(old)==1; t=t.replace(old,new)
# babble mode only: skip the other three modes
for m in ("one_legal(good)","one_silent(good)","one_resume(good)"):
    o=f"    for (int n = 0; n < kOps; ++n) {m};\n"; assert t.count(o)==1; t=t.replace(o,"")
open(p,"w").write(t)
PY
cd "$d/tb/nvm_port" && mkdir -p obj_dir
"${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}" --cc --exe --build -j 2 --top-module KL_pp_nvm_port \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GMAX_PAYLOAD_P=1024 -GMEM_TIMEOUT_CYC_P=$T -CFLAGS "-std=c++17 -O2 -I$PWD -DNVM_PORT_TMO=$T" \
  --Mdir obj_fz ../../hdl/packet_engine/KL_pp_nvm_port.sv fuzz_main.cpp -o Vfz > build.log 2>&1
./obj_fz/Vfz > run.log 2>&1 || true
echo "$V TMO=$T: $(grep -E 'FZ9' run.log | cut -c1-330)"
