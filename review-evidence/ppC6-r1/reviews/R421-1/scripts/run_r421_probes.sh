#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R421-1 reviewer probes for processor PR #139 at 5e806296b73d04ccf095ad00e081cb790fbbaf8d.
# Portable: needs git, Verilator 5.050, sv2v, yosys, python3, make, g++.
# Usage: run_r421_probes.sh <processor clone at the exact head> <work dir> [step...]
# Steps: suites mutants probe equiv ooc (default: all). Nothing is written to the clone.
set -euo pipefail
clone=$(realpath "$1"); work=$(realpath -m "$2"); shift 2
steps=${*:-suites mutants probe equiv ooc}
here=$(dirname "$(realpath "$0")")
head=5e806296b73d04ccf095ad00e081cb790fbbaf8d
base=0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff
mkdir -p "$work/receipts"
test "$(git -C "$clone" rev-parse HEAD)" = "$head"

export_tree() {  # export_tree <rev> <dir> <verilator build jobs>
  rm -rf "$2"; mkdir -p "$2"
  git -C "$clone" archive "$1" | tar -x -C "$2"
  grep -rl -- "--build -j 0" "$2/tb" | xargs -r sed -i "s/--build -j 0/--build -j $3/"
}

for s in $steps; do case $s in
suites)
  export_tree "$head" "$work/head" 8
  (cd "$work/head/tb/pp_top" && make run) > "$work/receipts/pp_top-head-make-run.log" 2>&1
  for t in originator ucpu aecp_notify ca_originator dispatch timer_service; do
    (cd "$work/head/tb/$t" && make) > "$work/receipts/suite-$t.log" 2>&1
  done
  (cd "$work/head" && ./scripts/lint_hdl.sh && python3 scripts/gen_matrix.py --check && make check) \
    > "$work/receipts/head-entry-points.log" 2>&1 ;;
mutants)
  export_tree "$head" "$work/mut" 4          # two parallel copies x 4 build jobs
  (cd "$work/mut" && python3 tb/pp_top/notify_mutants.py --output "$work/receipts/mutants/full" \
     --verilator "$(command -v verilator)" --jobs 2) > "$work/receipts/mutants/full-stdout.log" 2>&1 ;;
probe)
  export_tree "$head" "$work/probe" 8
  cp "$here/r421_ident_probe.hpp" "$work/probe/tb/pp_top/"
  python3 - "$work/probe/tb/pp_top/sim_main.cpp" <<'PY'
import sys; from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
a = '#include "notify_phases.hpp"\n'; assert t.count(a) == 1
t = t.replace(a, a + '#include <functional>\n#include "r421_ident_probe.hpp"\n')
b = '  run_identify(h);\n  const char* const build = "identify";\n'; assert t.count(b) == 1
t = t.replace(b, '  if (argc == 2 && std::strcmp(argv[1], "--r421-probe") == 0) { run_r421_probe(h); return 0; }\n' + b)
p.write_text(t)
PY
  (cd "$work/probe/tb/pp_top" && make identify-build && ./obj_idn/Vpp_top_idn --r421-probe) \
    > "$work/receipts/probe-ident-contention.log" 2>&1 ;;
equiv|ooc)
  export_tree "$base" "$work/base" 8; export_tree "$head" "$work/head2" 8
  cp -r "$work/base" "$work/basefix"
  python3 - "$work/basefix/hdl/aecp/KL_aecp_engine.sv" <<'PY'
import sys; from pathlib import Path
p = Path(sys.argv[1]); t = p.read_text()
a = "  localparam logic [10:0] UPC_SIRUN_C    = 11'd1936; // E_SIRUN\n"; assert t.count(a) == 1
t = t.replace(a, a + "  localparam logic [10:0] UPC_SINFOUNS_C = 11'd2016; // E_SINFOUNS\n")
b = ("      PP_UNS_SINFO_C: begin uns_ct_w = OP_SET_STREAM_INFO_C;\n"
     "                            uns_upc_w = UPC_GSTRI_C;   end\n"); assert t.count(b) == 1
t = t.replace(b, b.replace("UPC_GSTRI_C;   end", "UPC_SINFOUNS_C; end"))
p.write_text(t)
PY
  mkdir -p "$work/equiv/hex-head"
  for t in base head2 basefix; do
    (cd "$work/$t" && sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)) \
      > "$work/equiv/${t/head2/head}-all.v"
  done
  python3 "$work/head2/hdl/acmp/rom/gen_ltn_rom.py" -o "$work/equiv/hex-head/ltn_rom.hex"
  python3 "$work/head2/hdl/aecp/ucode/gen_ucode.py" -o "$work/equiv/hex-head/ucode.hex"
  cp "$here"/../receipts/equiv/*.ys "$here"/../receipts/ooc/*.ys "$work/equiv/"
  cd "$work/equiv/hex-head"
  for y in notify_equiv notify_equiv_en1_control engine_equiv ooc_notify_base0 ooc_notify_head0 \
           ooc_notify_head1 gen_notify_base0 gen_notify_head0; do
    yosys -q -l "../$y.log" "../$y.ys" > /dev/null 2>&1 || echo "$y rc=$? (the en1 control is expected to fail)"
  done ;;
esac; done
