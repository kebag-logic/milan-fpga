#!/bin/sh
# Build a disposable pp_top bench with a per-byte slow NVM device knob and
# probe_r2d.hpp, then run --probe-r2d. Usage: run_probe_r2d.sh <packet> <tree> <verilator>
set -u
P=$1; T=$2; VL=$3
cat "$P/scripts/probe_r2d.hpp" >> "$T/tb/pp_top/d3_phases.hpp"
python3 - "$T/tb/pp_top/sim_main.cpp" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
def sub(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
sub("  int      nv_gnt_every = 0;\n",
    "  int      nv_gnt_every = 0;\n  int      nv_byte_every = 0;  // reviewer knobs: payload READ bytes\n"
    "  int      nv_hdr_every = 0;   // 8-byte (header) READ bytes\n  int      nv_byte_wait = 0;\n")
sub("      } else if (nv_left) {\n        d->nvm_dev_rvalid_i = 1;\n",
    "      } else if (nv_left && (nv_cur.len == 8 ? nv_hdr_every : nv_byte_every) > 0\n"
    "                 && nv_byte_wait < (nv_cur.len == 8 ? nv_hdr_every : nv_byte_every)) {\n"
    "        ++nv_byte_wait;\n"
    "      } else if (nv_left) {\n        d->nvm_dev_rvalid_i = 1;\n")
sub("        if (d->nvm_dev_rready_o) { nv_left--; nv_rd_pos++; nv_rd_sent++; }\n",
    "        if (d->nvm_dev_rready_o) { nv_left--; nv_rd_pos++; nv_rd_sent++; nv_byte_wait = 0; }\n")
old = '  if (argc == 2 && std::strcmp(argv[1], "--dr3a") == 0) {'
sub(old, '  if (argc == 2 && std::strcmp(argv[1], "--probe-r2d") == 0) {\n'
         '    Suite setup(h);\n    setup.load_descriptor_image();\n'
         '    const std::vector<uint8_t> image = h.dram;\n'
         '    ProbeR2D{h, image, setup.image_ents}.run();\n    return 0;\n  }\n' + old)
open(p, "w").write(s)
PY
cd "$T/tb/pp_top" && make gsi-build VERILATOR="$VL" > build-probe.log 2>&1 || { echo "BUILD FAILED"; tail -30 build-probe.log; exit 2; }
./obj_dir/Vpp_top_sim --probe-r2d; echo "rc=$?"
