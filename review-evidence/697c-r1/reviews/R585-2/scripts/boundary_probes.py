#!/usr/bin/env python3
"""Reviewer probes of ctrl_boundary.py at a checkout: each plant is written into disposable copies made by
the gate's own planted(), then judged by the gate's own judge() in the universe it derives (modes()), with an
optional builder text planted as the gate's self-test plants one. A probe whose finding names the planted
file and the reached path is CAUGHT; otherwise ESCAPED.
Usage: boundary_probes.py <checkout> <work> <probe-name|all>"""
import sys
from pathlib import Path
checkout, work, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import fw_rv32  # noqa: E402
import ctrl_boundary as b  # noqa: E402

P = b.Plant
PROBES = {
 # R585-1's escaped classes, re-applied
 "r1-reentry-stack-src": (P("x", "stack", "src/acmp.c", "#ifdef CTRL_REENTRY_ASSERT\n",
    "#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_hal.h\"\n", "src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"), None),
 "r1-adapter-acmp-fake": (P("x", "ctrl", "acmp/acmp_mbx.c", "#include \"acmp_mbx.h\"\n",
    "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n#include \"acmp_fake.hpp\"\n#endif\n",
    "acmp/acmp_mbx.c includes tsn-c-stack/tests/acmp_fake.hpp"), None),
 "r1-ifndef-ndebug": (P("x", "stack", "src/maap.c", "#ifndef NDEBUG\n#include <assert.h>\n",
    "#ifndef NDEBUG\n#include <assert.h>\n#include \"mbx_contract.h\"\n", "src/maap.c includes sw/firmware/ctrl/mbx/mbx_contract.h"), None),
 "r1-stack-test-include": (P("x", "stack", "tests/test_acmp.cpp", "#include \"acmp.h\"\n",
    "#include \"acmp.h\"\n#include \"mbx_hal.h\"\n", "tests/test_acmp.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h"), None),
 # new: a firmware header's C++-only region (firmware headers are compiled as C++ by every arm's tests)
 "n1-fw-header-cplusplus-fake": (P("x", "ctrl", "acmp/acmp_mbx.h", "#ifdef __cplusplus\nextern \"C\" {\n",
    "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\nextern \"C\" {\n", "acmp/acmp_mbx.h includes"), None),
 "n2-fw-header-cplusplus-src": (P("x", "ctrl", "adp/adp_mbx.h", "#ifdef __cplusplus\nextern \"C\" {\n",
    "#ifdef __cplusplus\n#include \"../../tsn-c-stack/src/adp.c\"\nextern \"C\" {\n", "adp/adp_mbx.h includes"), None),
 # new: a value-guarded region in the image, whose value the image builder supplies per shape
 "n3-image-value-guard": (P("x", "ctrl", "test/rv32_image/image_main.c", "#include \"ctrl_app.h\"\n",
    "#include \"ctrl_app.h\"\n#if IMAGE_SINKS > 1u\n#include \"../../../tsn-c-stack/src/acmp.c\"\n#endif\n",
    "test/rv32_image/image_main.c includes"), None),
 # new: a mode written as two arguments in a builder
 "n4-split-flag-builder": (P("x", "stack", "src/adp.c", "#include <assert.h>\n",
    "#include <assert.h>\n#ifdef CTRL_SPLIT_MODE\n#include \"mbx_hal.h\"\n#endif\n", "src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    ("ctrl_arms.py", '\nPLANTED = ("-D", "CTRL_SPLIT_MODE")\n')),
 # new: control for N4 written the gate's way, must be caught
 "n4c-joined-flag-builder": (P("x", "stack", "src/adp.c", "#include <assert.h>\n",
    "#include <assert.h>\n#ifdef CTRL_SPLIT_MODE\n#include \"mbx_hal.h\"\n#endif\n", "src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    ("ctrl_arms.py", '\nPLANTED = ("-DCTRL_SPLIT_MODE",)\n')),
 # new: AECP's #ifdef CTRL_REENTRY_ASSERT region reaching a stack source
 "n5-aecp-reentry-region": (P("x", "ctrl", "aecp/aecp.c", "#include \"aecp_internal.h\"\n",
    "#include \"aecp_internal.h\"\n#ifdef AECP_TEST_NVM\n#include \"../../tsn-c-stack/src/maap.c\"\n#endif\n",
    "aecp/aecp.c includes tsn-c-stack/src/maap.c"), None),
 # new: stack public header C++-only region, not via a test the stack names first
 "n6-stack-header-cplusplus": (P("x", "stack", "include/maap.h", "#include <stdint.h>\n",
    "#include <stdint.h>\n#ifdef __cplusplus\n#include \"ctrl_loop.h\"\n#endif\n", "includes sw/firmware/ctrl/loop/ctrl_loop.h"), None),
}

rv32 = fw_rv32.compiler()
names = list(PROBES) if which == "all" else [which]
for name in names:
    plant, builder = PROBES[name]
    w = work / name
    trees = b.planted(plant, w / "plants")
    written = None
    if builder:
        path = b.HERE / builder[0]
        written = {path: path.read_text(encoding="utf-8") + builder[1]}
    findings = b.judge(trees, rv32, w / "build", b.modes(written))
    hit = [f for f in findings if plant.needle in f]
    print(f"{'CAUGHT' if hit else 'ESCAPED'} {name} (rv32={'yes' if rv32 else 'no'}): {hit[0] if hit else (findings or ['no finding'])}", flush=True)
