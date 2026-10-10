#!/usr/bin/env python3
"""Round-3 reviewer probes of ctrl_boundary.py at a checkout. Each plant is written into disposable copies made
by the gate's own planted(), then judged by the gate's own judge() with the build modes it derives (modes()),
with an optional builder text (a Python module or a Makefile, new or appended) planted the way the gate's
self-test plants one. A probe whose finding holds the needle is CAUGHT; otherwise ESCAPED.
Usage: boundary_probes3.py <checkout> <work> <probe-name|all> [--host-only]"""
import sys
from pathlib import Path
checkout, work, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import fw_rv32  # noqa: E402
import ctrl_boundary as b  # noqa: E402

P = b.Plant
HAL = "#include \"mbx_hal.h\"\n"
PY_HEAD = '"""A builder of the firmware that nobody lists."""\nfrom ctrl_build import Tree\n'
MK_HEAD = "# A builder of sw/firmware/ctrl that nobody lists.\n"


def stack_mode(macro):
    return P("x", "stack", "src/adp.c", "#include <assert.h>\n",
             f"#include <assert.h>\n#ifdef {macro}\n{HAL}#endif\n", "the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h")


PROBES = {
 # the round's required re-runs
 "s1-image-sinks-example": (P("x", "ctrl", "test/rv32_image/image_main.c", "#include <stdbool.h>\n",
    "#include <stdbool.h>\n#if IMAGE_SINKS > 1u\n#include \"../../../tsn-c-stack/examples/adp_port.h\"\n#endif\n",
    "test/rv32_image/image_main.c includes tsn-c-stack/examples/adp_port.h"), None),
 "s2-image-sources-src": (P("x", "ctrl", "test/rv32_image/image_main.c", "#include <stdbool.h>\n",
    "#include <stdbool.h>\n#if IMAGE_SOURCES == 9u\n#include \"../../../tsn-c-stack/src/acmp.c\"\n#endif\n",
    "test/rv32_image/image_main.c includes tsn-c-stack/src/acmp.c"), None),
 "c1-cplusplus-header-example": (P("x", "ctrl", "maap/maap_mbx.h", "#include \"maap.h\"\n",
    "#include \"maap.h\"\n#ifdef __cplusplus\n#include \"adp_port.h\"\n#endif\n",
    "maap/maap_mbx.h includes tsn-c-stack/examples/adp_port.h"), None),
 "c2-cplusplus-header-test-fake": (P("x", "ctrl", "loop/ctrl_loop.h", "#include <stdint.h>\n",
    "#include <stdint.h>\n#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n",
    "loop/ctrl_loop.h includes tsn-c-stack/tests/acmp_fake.hpp"), None),
 "d1-two-arg-D-python-list": (stack_mode("CTRL_R3_SPLIT_LIST"), ("r3_arms.py", PY_HEAD + 'FLAGS = ["-O2", "-D", "CTRL_R3_SPLIT_LIST"]\n')),
 "d2-two-arg-D-python-call": (stack_mode("CTRL_R3_SPLIT_CALL"), ("r3_arms.py", PY_HEAD + 'run("gcc", "-D", "CTRL_R3_SPLIT_CALL", "-c", "x.c")\n')),
 "d3-two-word-D-makefile": (stack_mode("CTRL_R3_SPLIT_MK"), ("r3.mk", MK_HEAD + "x:\n\t$(CC) -D CTRL_R3_SPLIT_MK -c x.c\n")),
 "d4-two-word-D-value-makefile": (stack_mode("CTRL_R3_SPLIT_MKV"), ("r3.mk", MK_HEAD + "x:\n\t$(CC) -D CTRL_R3_SPLIT_MKV=1 -c x.c\n")),
 # flag forms beyond the literal ones (none is used by a builder at this head)
 "f1-makefile-addprefix": (stack_mode("CTRL_R3_ADDPREFIX"), ("r3.mk", MK_HEAD + "MODES := CTRL_R3_ADDPREFIX\nx:\n\t$(CC) $(addprefix -D,$(MODES)) -c x.c\n")),
 "f2-makefile-variable": (stack_mode("CTRL_R3_MKVAR"), ("r3.mk", MK_HEAD + "MODE := CTRL_R3_MKVAR\nx:\n\t$(CC) -D$(MODE) -c x.c\n")),
 "f3-python-concat": (stack_mode("CTRL_R3_CONCAT"), ("r3_arms.py", PY_HEAD + 'MODE = "CTRL_R3_CONCAT"\nFLAGS = ["-D" + MODE]\n')),
 "f4-python-percent": (stack_mode("CTRL_R3_PERCENT"), ("r3_arms.py", PY_HEAD + 'FLAGS = ["-D%s" % "CTRL_R3_PERCENT"]\n')),
 "f5-python-bare-then-name": (stack_mode("CTRL_R3_NAME"), ("r3_arms.py", PY_HEAD + 'MODE = "CTRL_R3_NAME"\nFLAGS = ["-D", MODE]\n')),
 "f6-python-fstring-macro": (stack_mode("CTRL_R3_FSTR"), ("r3_arms.py", PY_HEAD + 'MODE = "CTRL_R3_FSTR"\nFLAGS = [f"-D{MODE}"]\n')),
 "g1-cplusplus-and-mode": (P("x", "ctrl", "port/ctrl_pool.h", "#include <stdint.h>\n",
    "#include <stdint.h>\n#if defined(__cplusplus) && defined(CTRL_REENTRY_ASSERT)\n#include \"acmp_fake.hpp\"\n#endif\n",
    "port/ctrl_pool.h includes tsn-c-stack/tests/acmp_fake.hpp"), None),
 "g2-cplusplus-and-shape": (P("x", "ctrl", "aecp/aecp_image.h", "#include \"aecp_model.h\"\n",
    "#include \"aecp_model.h\"\n#include \"aecp_entity_gen.h\"\n#if defined(__cplusplus) && AECP_ENTITY_MAPS > 8u\n#include \"adp_port.h\"\n#endif\n",
    "aecp/aecp_image.h includes tsn-c-stack/examples/adp_port.h"), None),
 "g3-riscv-only-stack-src": (P("x", "stack", "src/maap.c", "#include \"maap.h\"\n",
    "#include \"maap.h\"\n#ifdef __riscv\n#include \"mbx_hal.h\"\n#endif\n", "rv32"), None),
 "g4-freestanding-only-fw": (P("x", "ctrl", "mbx/mbx.c", "#include \"mbx.h\"\n",
    "#include \"mbx.h\"\n#if __STDC_HOSTED__ == 0\n#include \"../../tsn-c-stack/src/adp.c\"\n#endif\n",
    "firmware rv32"), None),
}

rv32 = None if "--host-only" in sys.argv else fw_rv32.compiler()
names = list(PROBES) if which == "all" else which.split(",")
for name in names:
    plant, builder = PROBES[name]
    w = work / name
    trees = b.planted(plant, w / "plants")
    written = None
    if builder:
        path = b.HERE / builder[0]
        base = path.read_text(encoding="utf-8") if path.exists() else ""
        written = {path: base + builder[1]}
    try:
        findings = b.judge(trees, rv32, w / "build", b.modes(written))
    except b.Refusal as exc:
        print(f"REFUSED {name}: {exc}", flush=True)
        continue
    hit = [f for f in findings if plant.needle in f]
    print(f"{'CAUGHT' if hit else 'ESCAPED'} {name} (rv32={'yes' if rv32 else 'no'}): {hit[0] if hit else (findings or ['no finding'])}", flush=True)
