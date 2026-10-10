#!/usr/bin/env python3
"""Real-path probe in a disposable clone: a new firmware header whose C++-only region reaches a stack example,
included by a C++ source a builder names. With the includer test/test_maap_differential.cpp (named by
maap_differential.py as "test/test_maap_differential.cpp") and, as the control, test/test_maap_mbx.cpp (named
plainly). The gate's own judge() on the clone's tree (host only) must name the header.
Usage: cxx_unfollowed_probe.py <clone> <work> <includer>"""
import sys
from pathlib import Path
clone, work, includer = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test")); sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import ctrl_boundary as b
hdr = b.CTRL / "maap/maap_probe.h"
hdr.write_text("#ifndef MAAP_PROBE_H\n#define MAAP_PROBE_H\n#ifdef __cplusplus\n"
               "#include \"../../../../third_party/tsn-c-stack/examples/adp_port.h\"\n#endif\n#endif\n")
src = b.CTRL / includer
orig = src.read_text()
anchor = next(ln for ln in orig.splitlines(keepends=True) if ln.startswith('#include "'))
src.write_text(orig.replace(anchor, anchor + '#include "../maap/maap_probe.h"\n', 1))
try:
    assert "maap_probe.h" in src.read_text()
    findings = b.judge(b.Trees(b.CTRL, b.STACK), None, work)
    hit = [f for f in findings if "maap_probe.h" in f]
    print(f"{'CAUGHT' if hit else 'ESCAPED'} includer={includer}: {hit[0] if hit else findings or 'no finding'}")
finally:
    src.write_text(orig); hdr.unlink()
