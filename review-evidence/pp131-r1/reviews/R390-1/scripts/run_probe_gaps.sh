#!/bin/sh
# Build the pp_top bench with probe_gaps.hpp appended, at the head and in each
# mutant tree already prepared by r390_mutants.py, and run --probe-gaps.
# Usage: run_probe_gaps.sh <packet> <clone> <verilator>
set -u
P=$1; SRC=$2; VL=$3
HEAD=e1ae468f7e237f321ce5fee19e59ae157da4b83d
mk() { # $1 tree
  cat "$P/scripts/probe_gaps.hpp" >> "$1/tb/pp_top/d3_phases.hpp"
  python3 - "$1/tb/pp_top/sim_main.cpp" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
old='  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {'
new='''  if (argc == 2 && std::strcmp(argv[1], "--probe-gaps") == 0) {
    Suite setup(h);
    setup.load_descriptor_image();
    const std::vector<uint8_t> image = h.dram;
    ProbeGaps{h, image, setup.image_ents}.run();
    return 0;
  }
''' + old
assert s.count(old)==1; open(p,'w').write(s.replace(old,new))
PY
  ( cd "$1/tb/pp_top" && make gsi-build VERILATOR="$VL" > build-probe.log 2>&1 && ./obj_dir/Vpp_top_sim --probe-gaps )
}
T=$P/scratch/probe-gaps-head; rm -rf "$T"; mkdir -p "$T"; git -C "$SRC" archive $HEAD | tar -x -C "$T"
echo "== head"; mk "$T"
for m in disagree_one_direction backoff_holds_dispatch; do
  echo "== mutant $m"; mk "$P/scratch/mut/$m"
done
