#!/usr/bin/env python3
"""Recorded converged-lock runs (#617 round 4, R394-3 S2 = R395-3 S4): write, next to a
capture_coherence sim_main.cpp, one probe per rate whose `--band50` mode runs the committed
CRF-settle placements (on the crossing, and 256 cycles further to the side the pull carries a
close across) for 150,000 columns instead of 30,000. Nothing else in the harness changes.

  python3 settle_probe_make.py <suite-dir>
  cd <suite-dir>; make -s build MDIR=obj_settle_m80 CPP=settle_probe_m80.cpp   (one per rate)
  ./obj_settle_m80/Vcoherence_sim --band50 > settle-150k-m80.log
"""
import sys
from pathlib import Path

S = Path(sys.argv[1])
src = (S / "sim_main.cpp").read_text()
anchor = "    if (mode == Mode::kBand50) {\n"
assert src.count(anchor) == 1
probe = ('    if (mode == Mode::kBand50) {  // SETTLE PROBE: the committed CRF-settle placements, PROBE_FRAMES columns\n'
         '        for (const int ppm : {PROBE_PPM}) {\n'
         '            char tag[24];\n'
         '            std::snprintf(tag, sizeof tag, "CRF-settle%+d", ppm);\n'
         '            const long near = ppm < 0 ? 0 : 8;\n'
         '            const long far = ppm < 0 ? -256 : 8 + 256;\n'
         '            list.push_back({tag, ppm_plan(ppm), std::min(near, far), std::max(near, far), 256, PROBE_FRAMES});\n'
         '        }\n'
         '        return list;\n'
         '    }\n'
         '    if (false) {\n')
for ppm in (-80, 80, -100, 100, -150, 150):
    name = f"settle_probe_{'m' if ppm < 0 else 'p'}{abs(ppm)}.cpp"
    (S / name).write_text(f"#define PROBE_PPM {ppm}\n#define PROBE_FRAMES 150'000\n" + src.replace(anchor, probe, 1))
    print(name)
