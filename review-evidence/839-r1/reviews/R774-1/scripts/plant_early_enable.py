#!/usr/bin/env python3
"""Probe leg: enable MAAP, the AAF talker (bypass) and the CRF talker at reset release,
before any station-MAC write, so the hold on those three transmitters is exercised."""
import sys
from pathlib import Path
p = Path(sys.argv[1])
t = p.read_text()
old = "    run_cycles(kBiosMs * kMsCyc);\n}\n"
new = ("    // probe: enable MAAP, AAF (enable+bypass) and CRF before the MAC write\n"
       "    write(0x6CC, (2u << 8) | 1u);\n"
       "    write(0x654, (2u << 16) | 3u);\n"
       "    write(0x750, 0x1u);\n"
       "    printf(\"[PROBE] MAAP/AAF/CRF enabled before the station MAC write at cycle %llu\\n\",\n"
       "           static_cast<unsigned long long>(cyc_));\n"
       "    run_cycles(kBiosMs * kMsCyc);\n"
       "    printf(\"[PROBE] end of BIOS window: %zu frames sent so far\\n\", sent_.size());\n}\n")
assert t.count(old) == 1
t = t.replace(old, new)
p.write_text(t)
print("planted early-enable probe")
