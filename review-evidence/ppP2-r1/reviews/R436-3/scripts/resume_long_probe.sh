#!/usr/bin/env bash
# resume_long_probe.sh VARIANT TMO : R436h, a reviewer-owned probe (never
# proposed as the PR's code). The head's tb/nvm_port/fuzz_main.cpp, resume mode
# only, with payloads of 0 to 600 bytes instead of 0 to 24, so an abandoned
# READ can still owe 256 bytes or more when the device resumes it at legal
# pace. FZ7/FZ8 then grade served-iff-within-the-bound. VARIANT is "head" or a
# plant name from plants_drain.py. Prints the FZ7 and FZ8 lines.
set -eu
P=$(cd "$(dirname "$0")/.." && pwd)
HEAD=527662d659b4ead97675744d12a43af1ea92b9b3
V=$1; T=$2
d=$P/scratch/resume_long/$V-$T; rm -rf "$d"; mkdir -p "$d"
git -C $REVIEWS/r436-3-ppP2 archive "$HEAD" hdl/packet_engine tb/nvm_port tb/common | tar -x -C "$d"
[ "$V" = head ] || python3 "$P/scripts/plants_drain.py" apply "$V" "$d/hdl/packet_engine/KL_pp_nvm_port.sv" >/dev/null
f=$d/tb/nvm_port/fuzz_main.cpp
python3 - "$f" <<'PY'
import sys
p=sys.argv[1]; t=open(p).read()
i=t.index("void PauseFuzz::one_resume"); j=t.index("void PauseFuzz::one_babble")
body=t[i:j]
assert body.count("size_t(rnd(0, 24))")==2
body=body.replace("size_t(rnd(0, 24))","size_t(rnd(0, 600))")   # [R436h] long records
t=t[:i]+body+t[j:]
for m in ("one_legal(good)","one_silent(good)","one_babble(good)"):
    o=f"    for (int n = 0; n < kOps; ++n) {m};\n"; assert t.count(o)==1; t=t.replace(o,"")
open(p,"w").write(t)
PY
cd "$d/tb/nvm_port" && mkdir -p obj_dir
"${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}" --cc --exe --build -j 2 --top-module KL_pp_nvm_port \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GMAX_PAYLOAD_P=1024 -GMEM_TIMEOUT_CYC_P=$T -CFLAGS "-std=c++17 -O2 -I$PWD -DNVM_PORT_TMO=$T" \
  --Mdir obj_fz ../../hdl/packet_engine/KL_pp_nvm_port.sv fuzz_main.cpp -o Vfz > build.log 2>&1
./obj_fz/Vfz > run.log 2>&1 || true
grep -E 'FZ[78]' run.log | sed "s/^/$V TMO=$T: /" | cut -c1-330
