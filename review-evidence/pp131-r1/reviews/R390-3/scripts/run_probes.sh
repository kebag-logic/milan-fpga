#!/bin/sh
# Build the pp_top bench of a tree with the reviewer probes appended and run
# them. Usage: run_probes.sh <packet> <tree> <verilator> [switch ...]
# <tree> is a disposable copy (git archive of the exact head, or a mutant).
# Switches default to: --probe-hol --probe-hol-restore --probe-gaps --probe-r2
set -u
P=$1; T=$2; VL=$3; shift 3
SW=${*:-"--probe-hol --probe-hol-restore --probe-gaps --probe-r2 --probe-r2c"}
for f in probe_hol.hpp probe_hol_restore.hpp probe_gaps.hpp probe_r2.hpp probe_r2c.hpp; do
  cat "$P/scripts/$f" >> "$T/tb/pp_top/d3_phases.hpp"
done
python3 - "$T/tb/pp_top/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {'
add = ''
for sw, body in (("--probe-hol", "ProbeHol{h, image}.run();"),
                 ("--probe-hol-restore", "ProbeHolRestore{h, image}.run();"),
                 ("--probe-gaps", "ProbeGaps{h, image, setup.image_ents}.run();"),
                 ("--probe-r2", "ProbeR2{h, image, setup.image_ents}.run();"),
                 ("--probe-r2c", "ProbeR2C{h, image, setup.image_ents}.run();")):
    add += ('  if (argc == 2 && std::strcmp(argv[1], "%s") == 0) {\n'
            '    Suite setup(h);\n    setup.load_descriptor_image();\n'
            '    const std::vector<uint8_t> image = h.dram;\n    %s\n    return 0;\n  }\n'
            % (sw, body))
assert s.count(old) == 1, "anchor"
open(p, "w").write(s.replace(old, add + old))
PY
cd "$T/tb/pp_top" && make gsi-build VERILATOR="$VL" > build-probe.log 2>&1 || { echo "BUILD FAILED"; tail -30 build-probe.log; exit 2; }
for s in $SW; do echo "== $s"; ./obj_dir/Vpp_top_sim "$s"; echo "rc=$?"; done
