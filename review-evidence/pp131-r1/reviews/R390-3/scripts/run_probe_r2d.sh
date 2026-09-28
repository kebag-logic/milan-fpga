#!/bin/sh
# Round-3 rerun of the round-2 probe D1 (probe_r2d.hpp). The head's bench now
# carries the per-byte device knobs natively (nv_hdr_every, nv_byte_every),
# so only the probe and its --probe-r2d switch are added.
# Usage: run_probe_r2d.sh <packet> <tree> <verilator>
set -u
P=$1; T=$2; VL=$3
cat "$P/scripts/probe_r2d.hpp" >> "$T/tb/pp_top/d3_phases.hpp"
python3 - "$T/tb/pp_top/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {'
assert s.count(old) == 1, old
s = s.replace(old, '  if (argc == 2 && std::strcmp(argv[1], "--probe-r2d") == 0) {\n'
              '    Suite setup(h);\n    setup.load_descriptor_image();\n'
              '    const std::vector<uint8_t> image = h.dram;\n'
              '    ProbeR2D{h, image, setup.image_ents}.run();\n    return 0;\n  }\n' + old)
open(p, "w").write(s)
PY
cd "$T/tb/pp_top" && make gsi-build VERILATOR="$VL" > build-probe.log 2>&1 || { echo "BUILD FAILED"; tail -30 build-probe.log; exit 2; }
./obj_dir/Vpp_top_sim --probe-r2d; echo "rc=$?"
