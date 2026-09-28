#!/usr/bin/env bash
# Reproduce the reviewer probes on a processor checkout at e1ae468f.
# Usage: run_probes.sh <processor checkout> <scratch dir> <dir holding a Verilator 5.050 'verilator'>
# Nothing is written into the checkout: the tree is exported into the scratch dir.
set -euo pipefail
SRC=$1; S=$2; VDIR=$3; HERE=$(cd "$(dirname "$0")" && pwd)
export PATH="$VDIR:$PATH"
mkdir -p "$S"; rm -rf "$S/tree" "$S/probe" "$S/probe-mut"
mkdir "$S/tree"; git -C "$SRC" archive HEAD | tar -x -C "$S/tree"
# P1-P5 on the unmodified RTL
cp -a "$S/tree" "$S/probe"
python3 - "$S/probe/tb/pp_top/sim_main.cpp" "$HERE/r391_probe.hpp" <<'PY'
import sys
p, hdr = sys.argv[1], sys.argv[2]; s = open(p).read()
s = s.replace('#include "d3_phases.hpp"\n', '#include "d3_phases.hpp"\n#include "%s"\n' % hdr, 1)
s = s.replace('  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {',
              '  if (argc == 2 && std::strcmp(argv[1], "--r391") == 0) {\n    run_r391(h);\n    return 0;\n  }\n'
              '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {', 1)
open(p, 'w').write(s)
PY
(cd "$S/probe/tb/pp_top" && make gsi-build >/dev/null && ./obj_dir/Vpp_top_sim --r391 | grep R391)
# P3/P4 on the golden and on the two deadline mutants (r391_probe_mut.hpp)
for v in golden mutant; do
  d="$S/probe-$v"; rm -rf "$d"; cp -a "$S/tree" "$d"
  python3 - "$d/tb/pp_top/sim_main.cpp" "$HERE/r391_probe_mut.hpp" <<'PY'
import sys
p, hdr = sys.argv[1], sys.argv[2]; s = open(p).read()
s = s.replace('#include "d3_phases.hpp"\n', '#include "d3_phases.hpp"\n#include "%s"\n' % hdr, 1)
s = s.replace('  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {',
              '  if (argc == 2 && std::strcmp(argv[1], "--r391") == 0) {\n    run_r391(h);\n    return 0;\n  }\n'
              '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {', 1)
open(p, 'w').write(s)
PY
  if [ "$v" = mutant ]; then
    python3 - "$d/hdl/aecp/KL_aecp_nvm_writer.sv" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
a = "W_JUDGE: stall_w = jd_wait_i;"; b = "assign m_abort_o  = expire_w && (ws_r == W_RD);"
assert s.count(a) == 1 and s.count(b) == 1
s = s.replace(a, "W_JUDGE: stall_w = 1'b0;").replace(b, "assign m_abort_o  = expire_w && (ws_r == W_RD) && !pass_r;")
open(p, 'w').write(s)
PY
  fi
  (cd "$d/tb/pp_top" && make gsi-build >/dev/null && ./obj_dir/Vpp_top_sim --r391 | grep R391 | sed "s/^/$v /")
done
# surviving-mutant campaign (D3 section) on the exported tree
python3 "$HERE/r391_mutants.py" --tree "$S/tree" --scratch "$S" --verilator-dir "$VDIR" --jobs 4
