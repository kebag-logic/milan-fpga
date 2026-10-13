# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_plants.py - the boundary gate's planted controls (#697).

ctrl_boundary.py --selftest writes each plant into a copy of the firmware's
tree and the stack, laid out as in the checkout (ctrl_boundary.mirror), and
judges what a builder compiled from that copy: each refused by the finding (or
the refusal) it names, or passing. The base every control shares compiles the
unplanted copy the ways the controls do, and must pass. A planted builder runs
through a capture of its own (ctrl_runs.planted_run), in a directory of its
own holding an empty planted.c, given PLANT_ROOT, PLANT_CTRL, PLANT_STACK and
PLANT_NVM (the copy, its ctrl tree, its stack and its store), PLANT_WORK (that
directory), PLANT_GCC (the real gcc), PLANT_TESTS (the gate's directory, to
import a builder's own compile functions from) and PLANT_INCLUDES (the arms'
include path for the copy, ctrl_build.includes). It compiles the copy as the
builders do (IMAGE: the image builder's compile of every image source; ARMS:
the host arms' C compile; TESTS: their C++ test compile) or in a spelling of
its own. A replay runs a compile of the run's capture again, with the copy's
trees in its arguments (ctrl_runs.replayed): a builder's own compile whose
inputs the gate's run made (the image builders' and the Verilator builders').
Whatever form the builder writes a flag or a source's name in, the boundary
judges what the compiler said that compile read. This module is one of the
gate's own, never a builder (ctrl_configs.GATE).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Plant:
    """One control: written into the copy's tree `side` ("ctrl", "stack" or "nvm": its sw/firmware/ctrl, its
    third_party/tsn-c-stack or its sw/firmware/ctrl_nvm; a "+" file is written whole as a new file; no file,
    none), with `extra` edits of the same kind in the same tree; refused by a finding (or a refusal) holding
    `needle`, or passing when `needle` is "". `run` is a planted builder's text, a Makefile when `make` (run as
    `make -f`) and Python otherwise, run through a capture of its own with `beside` written under its directory
    before the capture began; `replay` names the source whose compiles in the run's capture are run again on the
    copy. `texts` are builder texts the checkout is read as holding (a path from the gate's directory, and its
    text), never run; `alter` changes the run's capture the control is judged against: "missing", "empty",
    "drop " and a builder whose invocations it loses, or "drop run " and one whose own run's invocations it loses
    (its compiles under another builder's run stay); or, "forget " and a known builder, the known set it is held
    against loses that builder. `needs` names the builders whose capture the control
    needs ("verilator": the run that judges the builders that need Verilator; "" the firmware builders' run): a run
    judges the controls of its scope and names every other one."""

    name: str
    side: str
    file: str
    old: str
    new: str
    needle: str
    run: str = ""
    make: bool = False
    beside: tuple[tuple[str, str], ...] = ()
    texts: tuple[tuple[str, str], ...] = ()
    alter: str = ""
    extra: tuple[tuple[str, str, str], ...] = ()
    needs: str = ""
    replay: str = ""


#: A planted Python builder's head: the copy, its own directory, the arms' include path, and the compiler runs it
#: makes there; SRC is the firmware's ADP adapter in the copy.
PY = ('import os, subprocess, sys\n'
      'ROOT, CTRL, STACK, NVM, WORK = (os.environ["PLANT_" + k] for k in ("ROOT", "CTRL", "STACK", "NVM", "WORK"))\n'
      'INC = os.environ["PLANT_INCLUDES"].split()\nSRC = CTRL + "/adp/adp_mbx.c"\n'
      'sys.path[:0] = [os.environ["PLANT_TESTS"]]\n\n\n'
      'def cc(*words, shell=False):\n'
      '    subprocess.run(words[0] if shell else list(words), cwd=WORK, shell=shell, check=False,\n'
      '                   capture_output=True)\n\n\n')
#: The host arms' C compile of firmware and stack sources from the copy (ctrl_build.compile_c), by their names.
ARMS = ('def arms(*names, extra=()):\n'
        '    from pathlib import Path\n'
        '    import ctrl_build\n'
        '    tree = ctrl_build.Tree(Path(CTRL), Path(WORK, "out"), Path(WORK, "reuse"), stack=Path(STACK))\n'
        '    for at, name in enumerate(names):\n'
        '        try:\n'
        '            ctrl_build.compile_c(tree, [ctrl_build.source(tree.src, tree.stack, name)], f"arms{at}",\n'
        '                                 tuple(extra))\n'
        '        except ctrl_build.Refusal:\n'
        '            pass\n\n\n')
#: The arms' C++ test compile (fw_gtest.compile_tests, with their include path and the checkout's stack tests/) of
#: sources, and a C++ source of the builder's own that includes headers.
TESTS = ('def tests(*sources, extra=()):\n'
         '    from pathlib import Path\n'
         '    import ctrl_build\n'
         '    import fw_gtest\n'
         '    tree = ctrl_build.Tree(Path(CTRL), Path(WORK, "out"), Path(WORK, "reuse"), stack=Path(STACK))\n'
         '    for at, source in enumerate(sources):\n'
         '        try:\n'
         '            fw_gtest.compile_tests(tree.build, [*ctrl_build.includes(tree), f"-I{ctrl_build.STACK_TESTS}",\n'
         '                                   *extra], [Path(source)], Path(WORK, f"tests{at}"))\n'
         '        except fw_gtest.BuildError:\n'
         '            pass\n\n\n'
         'def probe(*headers):\n'
         '    from pathlib import Path\n'
         '    path = Path(WORK, "probe.cpp")\n'
         '    path.write_text("".join(f\'#include "{h}"\\n\' for h in headers))\n'
         '    return str(path)\n\n\n')
#: The image builder's compile of every source of the composition from the copy (ctrl_image.compile_all), at a
#: shape, with the copy's image sources.
IMAGE = ('def image(shape="endstation_ax7101_1x1_tdm8"):\n'
         '    from pathlib import Path\n'
         '    import ctrl_image\n'
         '    ctrl_image.IMAGE = Path(CTRL, "test/rv32_image")\n'
         '    ctrl_image.HELPERS = ctrl_image.IMAGE / "image_arith.c"\n'
         '    gen, flags = ctrl_image.shape_build(ctrl_image.ROOT / "configs" / f"{shape}.yaml",\n'
         '                                        Path(WORK, "shape-" + shape))\n'
         '    out = Path(WORK, "image-" + shape)\n'
         '    out.mkdir(parents=True, exist_ok=True)\n'
         '    try:\n'
         '        ctrl_image.compile_all(ctrl_image.fw_rv32.compiler(), Path(ROOT, "sw/firmware"), gen, out, flags,\n'
         '                               Path(STACK))\n'
         '    except ctrl_image.Refusal:\n'
         '        pass\n\n\n')
#: A stack file outside its public headers that preprocesses on its own, in C and C++, and its path from a directory
#: of the ctrl tree (or of the store's plat/); the stack's example header, included from one.
STRING = "third_party/tsn-c-stack/examples/rv32/include/string.h"
FROM_CTRL = "../../../../" + STRING
EXAMPLE = '#include "../../../../third_party/tsn-c-stack/examples/adp_port.h"\n'
#: What a stack file outside its public headers is named by in a finding.
STRING_NAMED = "tsn-c-stack/examples/rv32/include/string.h"
#: The firmware adapter a mode's control reaches a stack file from, under that mode.
ANCHOR = '#include "adp_mbx.h"\n'
MODE_NEEDLE = "firmware: sw/firmware/ctrl/adp/adp_mbx.c reads tsn-c-stack/examples/rv32/include/string.h"
#: A C++ source of the copy that a computed-name control compiles, and the firmware header it reaches.
PROBE = "test/probe_r5/bench.cpp"
CXX_HEADER = f'#ifdef __cplusplus\n#include "{FROM_CTRL}"\n#endif\n'
CXX_NEEDLE = f"firmware: sw/firmware/ctrl/adp/adp_r5.h includes {STRING_NAMED}, not one of the stack's public headers"
#: A header whose include a macro computes, reaching a stack file outside its public headers in C++.
COMPUTED = f'#ifdef __cplusplus\n#define H "{FROM_CTRL}"\n#include H\n#endif\n'
#: A C++ source of a builder's own whose include a macro computes: the firmware's adapter header.
INSTALLED = '#define H "adp_mbx.h"\n#include H\n'


def arms(*names: str, extra: str = "()") -> str:
    """A planted builder: the host arms' C compile of `names` from the copy, with `extra` (a Python expression)."""
    return PY + ARMS + f"arms({', '.join(map(repr, names))}, extra={extra})\n"


def tests(sources: str, extra: str = "()") -> str:
    """A planted builder: the arms' C++ test compile of `sources` (Python expressions), with `extra`."""
    return PY + TESTS + f"tests({sources}, extra={extra})\n"


def image(*shapes: str) -> str:
    """A planted builder: the image builder's compile of every image source from the copy, at each shape."""
    return PY + IMAGE + "".join(f"image({shape!r})\n" for shape in shapes or ("endstation_ax7101_1x1_tdm8",))


def under_mode(name: str, macro: str, run: str, make: bool = False, test: str = "") -> Plant:
    """A control whose planted builder compiles the copy's ADP adapter with a mode, in some form: the adapter reads
    a stack file outside its public headers only under it (or when its value, `test`, holds)."""
    return Plant(name, "ctrl", "adp/adp_mbx.c", ANCHOR,
                 ANCHOR + (f"#if {test}\n" if test else f"#ifdef {macro}\n") + f'#include "{FROM_CTRL}"\n#endif\n',
                 MODE_NEEDLE, run=run, make=make)


def through_source(name: str, run: str, make: bool = False, probe: bool = True,
                   beside: tuple[tuple[str, str], ...] = ()) -> Plant:
    """A control whose planted builder compiles a C++ source it computes the name of, or writes: a new firmware
    header reached only from that source includes a stack file outside its public headers in C++ only."""
    extra = (("+" + PROBE, "", '#include "adp_r5.h"\n'),) if probe else ()
    return Plant(name, "ctrl", "+adp/adp_r5.h", "", CXX_HEADER, CXX_NEEDLE, run=run, make=make, beside=beside,
                 extra=extra)


def wire_mode(name: str, condition: str) -> Plant:
    """A control only the AECP wire comparison's compiles catch (R584-5 V1 to V3): the AECP image header, which its
    C++ compile reaches, reads a stack file outside its public headers only under `condition`, a mode only that
    builder's configurations give (its one- and two-interface references); the comparison's own recorded compile
    is replayed on the copy."""
    anchor = '#include "aecp_model.h"\n'
    return Plant(name, "ctrl", "aecp/aecp_image.h", anchor,
                 anchor + f'#if {condition}\n#include "{FROM_CTRL}"\n#endif\n',
                 f"firmware: sw/firmware/ctrl/aecp/aecp_image.h includes {STRING_NAMED}", needs="verilator",
                 replay="aecp_wire.cpp")


def makefile(recipe: str, head: str = "") -> str:
    """A planted Makefile: its variables, then one target whose recipe is `recipe`."""
    return f"{head}planted:\n\t{recipe}\n"


#: A planted Makefile's compile of the copy's ADP adapter, its flags before the include path.
MAKE_SRC = "$(PLANT_INCLUDES) -c $(PLANT_CTRL)/adp/adp_mbx.c -o planted.o"
#: What a stack-side finding says of a file the stack may not read.
NOT_OURS = "which is neither the stack's nor the C implementation's"

PLANTS = (
    Plant("the F5 builder removed from the registry", "ctrl", "", "", "",
          "tb/verilator/milan_dp/stream_counter_f5.py names the firmware's tree",
          alter="forget tb/verilator/milan_dp/stream_counter_f5.py"),
    Plant("the F5 builder's own capture is missing", "ctrl", "", "", "",
          "the capture holds no invocation of tb/verilator/milan_dp/stream_counter_f5.py from a run of its own",
          alter="drop run tb/verilator/milan_dp/stream_counter_f5.py"),
    *(Plant(f"an unclassified copy of {name}", "ctrl", "", "", "",
            f"sw/firmware/ctrl/test/planted_{name} names the firmware's tree",
            texts=((f"planted_{name}", (Path(__file__).resolve().parents[3] / "litex" / name).read_text()),))
      for name in ("test_ctrl_memory.py", "ctrl_memory.py", "milan_soc.py")),
    Plant("the reset-entry builder's own capture is missing", "ctrl", "", "", "",
          "the capture holds no invocation of sw/litex/test_ctrl_memory.py from a run of its own",
          alter="drop run sw/litex/test_ctrl_memory.py"),
    Plant("the reset entry includes a private stack header in the fifth capture", "ctrl", "plat/ctrl_split_start.S",
          '\t.section .text.start, "ax"\n',
          f'#define TSN_PORT_STRING_H\n#include "{FROM_CTRL}"\n#undef TSN_PORT_STRING_H\n'
          '\t.section .text.start, "ax"\n',
          f"firmware: sw/firmware/ctrl/plat/ctrl_split_start.S reads {STRING_NAMED}",
          replay="ctrl_split_start.S"),
    # The stack's side: its sources and headers, as the arms and the image compile them.
    Plant("stack source includes the mailbox HAL", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"mbx_hal.h\"\n",
          f"stack: tsn-c-stack/src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h, {NOT_OURS}",
          run=arms("tsn-c-stack/src/adp.c")),
    Plant("stack source includes the register-map contract", "stack", "src/acmp.c", "#include \"acmp.h\"\n",
          "#include \"acmp.h\"\n#include \"mbx_contract.h\"\n",
          "tsn-c-stack/src/acmp.c includes sw/firmware/ctrl/mbx/mbx_contract.h", run=arms("tsn-c-stack/src/acmp.c")),
    Plant("stack source includes the composition", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"ctrl_app.h\"\n",
          "tsn-c-stack/src/maap.c includes sw/firmware/ctrl/app/ctrl_app.h",
          run=arms("tsn-c-stack/src/maap.c")),
    Plant("stack source includes the store's port", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"nvm_state.h\"\n",
          "tsn-c-stack/src/maap.c includes sw/firmware/ctrl_nvm/nvm_state.h", run=arms("tsn-c-stack/src/maap.c")),
    Plant("stack source includes the loop through a macro", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#define TSN_LOOP \"ctrl_loop.h\"\n#include TSN_LOOP\n",
          "tsn-c-stack/src/adp.c includes sw/firmware/ctrl/loop/ctrl_loop.h", run=arms("tsn-c-stack/src/adp.c")),
    Plant("stack public header includes the platform's header", "stack", "include/wire.h", "#include <stdint.h>\n",
          "#include <stdint.h>\n#include \"ctrl_debug.h\"\n",
          "stack: tsn-c-stack/include/wire.h includes sw/firmware/ctrl/port/ctrl_debug.h",
          run=arms("tsn-c-stack/src/adp.c")),
    Plant("Q7: a store header shadows the C library's for the stack in the image build", "nvm", "+plat/stdbool.h", "",
          "#pragma once\n#ifndef __cplusplus\n#define bool _Bool\n#define true 1\n#define false 0\n"
          "#define __bool_true_false_are_defined 1\n#endif\n",
          f"includes sw/firmware/ctrl_nvm/plat/stdbool.h, {NOT_OURS}", run=image()),
    Plant("a firmware directory shadows a header the C library's own headers include, for the stack", "ctrl",
          "+port/bits/libc-header-start.h", "", "#include_next <bits/libc-header-start.h>\n",
          "stack: tsn-c-stack/src/adp.c reads sw/firmware/ctrl/port/bits/libc-header-start.h (included by ",
          run=arms("tsn-c-stack/src/adp.c")),
    Plant("stack source includes the mailbox HAL under the re-entry assertion", "stack", "src/acmp.c",
          "#ifdef CTRL_REENTRY_ASSERT\n", "#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_hal.h\"\n",
          "tsn-c-stack/src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=arms("tsn-c-stack/src/acmp.c", extra='("-DCTRL_REENTRY_ASSERT",)')),
    Plant("stack source includes the platform's header in a debug build", "stack", "src/maap.c",
          "#ifndef NDEBUG\n#include <assert.h>\n", "#ifndef NDEBUG\n#include <assert.h>\n#include \"ctrl_debug.h\"\n",
          "tsn-c-stack/src/maap.c includes sw/firmware/ctrl/port/ctrl_debug.h",
          run=arms("tsn-c-stack/src/maap.c", extra='("-UNDEBUG",)')),
    Plant("stack source includes the contract in a debug build with the re-entry assertion", "stack", "src/maap.c",
          "#ifndef NDEBUG\n#include <assert.h>\n",
          "#ifndef NDEBUG\n#include <assert.h>\n#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_contract.h\"\n#endif\n",
          "tsn-c-stack/src/maap.c includes sw/firmware/ctrl/mbx/mbx_contract.h",
          run=arms("tsn-c-stack/src/maap.c", extra='("-UNDEBUG", "-DCTRL_REENTRY_ASSERT")')),
    Plant("stack source includes the AECP core's header", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"aecp.h\"\n", "tsn-c-stack/src/adp.c includes sw/firmware/ctrl/aecp/aecp.h",
          run=arms("tsn-c-stack/src/adp.c", extra='("-I" + CTRL + "/aecp",)')),
    Plant("a mode a builder compiles the stack with", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_PLANTED_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "tsn-c-stack/src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=PY + 'cc("cc", "-DCTRL_PLANTED_MODE", *INC, "-c", STACK + "/src/adp.c", "-o", "planted.o")\n'),
    Plant("a mode a builder writes as two arguments", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_SPLIT_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "tsn-c-stack/src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=PY + 'cc("cc", "-D", "CTRL_SPLIT_MODE", *INC, "-c", STACK + "/src/adp.c", "-o", "planted.o")\n'),
    Plant("a mode a new Makefile writes as two words", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_SPLIT_MAKE\n#include \"ctrl_loop.h\"\n#endif\n",
          "tsn-c-stack/src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          run=makefile("cc -D CTRL_SPLIT_MAKE $(PLANT_INCLUDES) -c $(PLANT_STACK)/src/maap.c -o planted.o"),
          make=True),
    # The stack's tests, as the arms compile them as C++.
    Plant("a stack test includes the mailbox HAL", "stack", "tests/test_maap_debug.cpp", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"mbx_hal.h\"\n",
          "stack: tsn-c-stack/tests/test_maap_debug.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=tests('STACK + "/tests/test_maap_debug.cpp"')),
    Plant("a stack test includes the firmware's harness", "stack", "tests/test_adp.cpp", "#include \"adp.h\"\n",
          "#include \"adp.h\"\n#include \"fw_gtest.hpp\"\n",
          "stack: tsn-c-stack/tests/test_adp.cpp includes sw/firmware/gtest/fw_gtest.hpp",
          run=tests('STACK + "/tests/test_adp.cpp"')),
    Plant("a stack test includes the platform's pool in its release build", "stack", "tests/test_adp_reentry.cpp",
          "#include \"adp.h\"\n", "#include \"adp.h\"\n#ifdef ADP_TEST_RELEASE\n#include \"ctrl_pool.h\"\n#endif\n",
          "stack: tsn-c-stack/tests/test_adp_reentry.cpp includes sw/firmware/ctrl/port/ctrl_pool.h",
          run=tests('STACK + "/tests/test_adp_reentry.cpp"', extra='("-DADP_TEST_RELEASE",)')),
    Plant("a stack public header includes the mailbox HAL for C++ only", "stack", "include/acmp.h",
          "#ifdef __cplusplus\nextern \"C\" {\n", "#ifdef __cplusplus\n#include \"mbx_hal.h\"\nextern \"C\" {\n",
          "stack: tsn-c-stack/include/acmp.h includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=tests('probe("acmp.h")')),
    Plant("a stack test includes the AECP adapter", "stack", "tests/test_adp.cpp", "#include \"adp.h\"\n",
          "#include \"adp.h\"\n#include \"aecp_mbx.h\"\n",
          "stack: tsn-c-stack/tests/test_adp.cpp includes sw/firmware/ctrl/aecp/aecp_mbx.h",
          run=tests('STACK + "/tests/test_adp.cpp"', extra='("-I" + CTRL + "/aecp",)')),
    # The firmware's side: its sources and headers, the store's and the images' among them.
    Plant("N1: a store source reaches a stack example, as the image builder compiles it", "nvm", "nvm_store.c",
          "#include \"nvm_store.h\"\n",
          "#include \"nvm_store.h\"\n#include \"../../../third_party/tsn-c-stack/examples/adp_port.h\"\n",
          "firmware: sw/firmware/ctrl_nvm/nvm_store.c reads tsn-c-stack/examples/adp_port.h, not one of the stack's "
          "public headers", run=image()),
    Plant("a store source reaches a stack file outside its public headers in the image build", "nvm",
          "plat/nvm_flash_litespi.c", "#include \"nvm_flash_litespi.h\"\n",
          f"#include \"nvm_flash_litespi.h\"\n#include \"{FROM_CTRL}\"\n",
          f"firmware: sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c reads {STRING_NAMED}", run=image()),
    Plant("firmware reaches a stack example's header", "ctrl", "adp/adp_mbx.c", ANCHOR, ANCHOR + EXAMPLE,
          "firmware: sw/firmware/ctrl/adp/adp_mbx.c reads tsn-c-stack/examples/adp_port.h, not one of the stack's "
          "public headers", run=arms("adp/adp_mbx.c")),
    Plant("firmware header reaches a stack source by a relative path", "ctrl", "maap/maap_mbx.h",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n",
          "firmware: sw/firmware/ctrl/maap/maap_mbx.h includes tsn-c-stack/src/maap.c, not one of the stack's public "
          "headers", run=arms("maap/maap_mbx.c")),
    Plant("image source reaches a stack file outside its public headers", "ctrl", "test/rv32_image/image_main.c",
          "#include \"ctrl_app.h\"\n", f"#include \"ctrl_app.h\"\n#include \"../{FROM_CTRL}\"\n",
          f"firmware: sw/firmware/ctrl/test/rv32_image/image_main.c reads {STRING_NAMED}", run=image()),
    Plant("a firmware adapter reaches a stack source under the re-entry assertion", "ctrl", "acmp/acmp_mbx.c",
          "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n"
          "#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n#endif\n",
          "firmware: sw/firmware/ctrl/acmp/acmp_mbx.c reads tsn-c-stack/src/acmp.c",
          run=arms("acmp/acmp_mbx.c", extra='("-DCTRL_REENTRY_ASSERT",)')),
    Plant("firmware tests a mode by its value", "ctrl", "maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
          "#include \"maap_mbx.h\"\n#if CTRL_REENTRY_ASSERT\n"
          "#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n"
          "#endif\n", "firmware: sw/firmware/ctrl/maap/maap_mbx.c reads tsn-c-stack/src/maap.c",
          run=arms("maap/maap_mbx.c", extra='("-DCTRL_REENTRY_ASSERT",)')),
    Plant("an adapter reaches a stack source where a build leaves lwSRP's profile undefined", "ctrl",
          "acmp/acmp_mbx.c", "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifndef LWSRP_MILAN\n#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n"
          "#endif\n", "firmware: sw/firmware/ctrl/acmp/acmp_mbx.c reads tsn-c-stack/src/acmp.c",
          run=arms("acmp/acmp_mbx.c")),
    Plant("the AECP core reaches a stack source", "ctrl", "aecp/aecp.c", "#include \"aecp_internal.h\"\n",
          "#include \"aecp_internal.h\"\n#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n",
          "firmware: sw/firmware/ctrl/aecp/aecp.c reads tsn-c-stack/src/acmp.c",
          run=arms("aecp/aecp.c", extra='("-I" + CTRL + "/aecp",)')),
    Plant("the AECP core reaches a stack source at a value only its arms compile with", "ctrl", "aecp/aecp.c",
          "#include \"aecp_internal.h\"\n",
          "#include \"aecp_internal.h\"\n#if AECP_TEST_INTERFACES > 1\n"
          "#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n#endif\n",
          "firmware: sw/firmware/ctrl/aecp/aecp.c reads tsn-c-stack/src/acmp.c",
          run=arms("aecp/aecp.c", extra='("-I" + CTRL + "/aecp", "-DAECP_TEST_INTERFACES=2")')),
    Plant("the AECP application bridge reaches a stack example's header", "ctrl", "app/ctrl_app_aecp.c",
          "#include \"ctrl_app_aecp.h\"\n", "#include \"ctrl_app_aecp.h\"\n" + EXAMPLE,
          "firmware: sw/firmware/ctrl/app/ctrl_app_aecp.c reads tsn-c-stack/examples/adp_port.h",
          replay="ctrl_app_aecp.c"),
    Plant("the image reaches a stack file under a shape's stream count", "ctrl", "test/rv32_image/image_main.c",
          "#include <stdbool.h>\n",
          f"#include <stdbool.h>\n#if IMAGE_SINKS > 1u\n#include \"../{FROM_CTRL}\"\n#endif\n",
          f"firmware: sw/firmware/ctrl/test/rv32_image/image_main.c reads {STRING_NAMED}",
          run=image("endstation_ax7101_8x8")),
    Plant("the SRP image's composition reaches a stack source, as the SRP image builder compiles it", "ctrl",
          "test/ctrl_image.c", "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n"
          "#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n",
          "firmware: sw/firmware/ctrl/test/ctrl_image.c reads tsn-c-stack/src/acmp.c", replay="ctrl_image.c"),
    Plant("the AECP image's SRP composition reaches a stack source, as the SRP image builder compiles it", "ctrl",
          "test/ctrl_aecp_image.c", "#include \"srp_mbx.h\"\n",
          "#include \"srp_mbx.h\"\n#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n",
          "firmware: sw/firmware/ctrl/test/ctrl_aecp_image.c reads tsn-c-stack/src/maap.c", replay="ctrl_aecp_image.c"),
    Plant("the AECP image reaches a stack source at a shape its generated header gives many maps", "ctrl",
          "test/ctrl_aecp_image.c", "#include \"aecp_entity_gen.h\"\n",
          "#include \"aecp_entity_gen.h\"\n#if AECP_ENTITY_MAPS > 8u\n"
          "#include \"../../../../third_party/tsn-c-stack/src/acmp.c\"\n#endif\n",
          "firmware: sw/firmware/ctrl/test/ctrl_aecp_image.c reads tsn-c-stack/src/acmp.c", replay="ctrl_aecp_image.c"),
    Plant("an adapter reaches a stack source where the SRP shape header is force-included", "ctrl",
          "maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
          "#include \"maap_mbx.h\"\n#ifdef CTRL_SRP_SOURCES\n"
          "#include \"../../../../third_party/tsn-c-stack/src/maap.c\"\n"
          "#endif\n", "firmware: sw/firmware/ctrl/maap/maap_mbx.c reads tsn-c-stack/src/maap.c", replay="maap_mbx.c"),
    Plant("an adapter reaches a stack source on the two-interface contract, as the SRP image builder compiles it",
          "ctrl", "adp/adp_mbx.c", ANCHOR,
          ANCHOR + "#if MBX_N_IF > 1u\n#include \"../../../../third_party/tsn-c-stack/src/adp.c\"\n#endif\n",
          "firmware: sw/firmware/ctrl/adp/adp_mbx.c reads tsn-c-stack/src/adp.c", replay="adp_mbx.c"),
    Plant("a firmware header reaches a stack test's fake in C++ only", "ctrl", "acmp/acmp_mbx.h",
          "#ifdef __cplusplus\nextern \"C\" {\n", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\nextern \"C\" {\n",
          "firmware: sw/firmware/ctrl/acmp/acmp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the "
          "stack's public headers", run=tests('probe("acmp_mbx.h")')),
    Plant("a firmware header reaches a stack file through a computed include in C++ only", "ctrl", "+adp/adp_r5.h",
          "", COMPUTED, CXX_NEEDLE, run=tests('probe("adp_r5.h")', extra='("-I" + CTRL + "/adp",)')),
    Plant("a copy of the stack's wire.h in the firmware", "ctrl", "+mbx/wire.h", "", "#include <stdint.h>\n",
          "mbx/wire.h has the name of the stack's wire.h"),
    Plant("a copy of the stack's adp.c in the firmware", "ctrl", "+adp/adp.c", "", "int adp_copy;\n",
          "adp/adp.c has the name of the stack's adp.c"),
    Plant("a copy of the stack's acmp.h in the AECP directory", "ctrl", "+aecp/acmp.h", "", "#include <stdint.h>\n",
          "aecp/acmp.h has the name of the stack's acmp.h"),
    # R584-4-F2, R585-4-F1, R584-3-S1, rounds 4 and 6: each form a builder writes a mode in.
    under_mode("a Makefile's patsubst writes a mode", "CTRL_R5_PATSUBST",
               makefile(f"cc $(patsubst %,-D%,$(MODES)) {MAKE_SRC}", "MODES := CTRL_R5_PATSUBST\n"), True),
    under_mode("a Makefile's foreach writes a mode", "CTRL_R5_FOREACH",
               makefile(f"cc $(foreach m,CTRL_R5_FOREACH,-D$(m)) {MAKE_SRC}"), True),
    under_mode("a Makefile appends a mode with no space", "CTRL_R5_APPEND",
               makefile(f"cc $(CFLAGS) {MAKE_SRC}", "CFLAGS+=-DCTRL_R5_APPEND\n"), True),
    under_mode("a Makefile writes a mode's name after a bare -D", "CTRL_R5_SPACED",
               makefile(f"cc -D $(M) {MAKE_SRC}", "M := CTRL_R5_SPACED\n"), True),
    under_mode("a Makefile computes a mode's name", "CTRL_R4_MAKE",
               makefile(f"cc -D$(MODE) {MAKE_SRC}", "MODE := CTRL_R4_MAKE\n"), True),
    under_mode("a Makefile computes a mode's value", "CTRL_R4_MAKE_VALUE",
               makefile(f"cc -DCTRL_R4_MAKE_VALUE=$(VALUE) {MAKE_SRC}", "VALUE := 2\n"), True,
               "CTRL_R4_MAKE_VALUE > 1"),
    under_mode("a Makefile prefixes -D to the modes it lists", "CTRL_R4_ADDPREFIX",
               makefile(f"cc $(addprefix -D,$(MODES)) {MAKE_SRC}", "MODES := CTRL_R4_ADDPREFIX\n"), True),
    under_mode("an f-string writes a mode after other text", "CTRL_R5_FSTRING",
               PY + 'CC = "cc"\ncc(f"{CC} -DCTRL_R5_FSTRING {\' \'.join(INC)} -c {SRC} -o planted.o", shell=True)\n'),
    under_mode("a multi-word literal holds a mode", "CTRL_R5_SPLIT",
               PY + 'cc("cc", *"-O2 -DCTRL_R5_SPLIT".split(), *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a shell command's literal holds a mode", "CTRL_R5_SHELL",
               PY + 'cc("cc -DCTRL_R5_SHELL " + " ".join(INC) + " -c " + SRC + " -o planted.o", shell=True)\n'),
    under_mode("shlex splits a mode out of a literal", "CTRL_R5_SHLEX",
               PY + 'import shlex\ncc("cc", *shlex.split("-O2 -DCTRL_R5_SHLEX"), *INC, "-c", SRC, "-o", '
                    '"planted.o")\n'),
    under_mode("a bare -D takes a mode a conditional chooses", "CTRL_R5_CHOSEN",
               PY + 'X = True\ncc("cc", "-D", "CTRL_R5_CHOSEN" if X else "CTRL_R5_OTHER", *INC, "-c", SRC, "-o", '
                    '"planted.o")\n'),
    under_mode("str.format writes a mode", "CTRL_R5_FORMAT",
               PY + 'cc("cc", "-D{}".format("CTRL_R5_FORMAT"), *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a builder joins -D to a mode it computes", "CTRL_R4_JOINED",
               PY + 'MODE = "CTRL_R4_JOINED"\ncc("cc", "-D" + MODE, *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a builder formats a mode with %", "CTRL_R4_PERCENT",
               PY + 'cc("cc", "-D%s" % "CTRL_R4_PERCENT", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a builder joins a value to a mode", "CTRL_R4_VALUE",
               PY + 'N = 2\ncc("cc", "-DCTRL_R4_VALUE=" + str(N), *INC, "-c", SRC, "-o", "planted.o")\n',
               test="CTRL_R4_VALUE > 1"),
    under_mode("an f-string computes a mode's name", "CTRL_R4_MODE",
               PY + 'SUFFIX = "MODE"\ncc("cc", f"-DCTRL_R4_{SUFFIX}", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a bare -D takes the modes a list holds", "CTRL_R4_BARE",
               PY + 'NAMES = ["CTRL_R4_BARE"]\ncc(*["cc", "-D"] + NAMES, *INC, "-c", SRC, "-o", "planted.o")\n'),
    # R584-5-F1, R585-5-F1: each spelling the reviewers used, as the compiler reads it.
    under_mode("-Wp, passes a mode to the preprocessor", "CTRL_R6_WP",
               PY + 'cc("cc", "-Wp,-DCTRL_R6_WP", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("-Xpreprocessor passes a mode", "CTRL_R6_XP",
               PY + 'cc("cc", "-Xpreprocessor", "-DCTRL_R6_XP", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("--define-macro= defines a mode", "CTRL_R6_LONG",
               PY + 'cc("cc", "--define-macro=CTRL_R6_LONG", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("--define-macro and a separate name define a mode", "CTRL_R6_LONG2",
               PY + 'cc("cc", "--define-macro", "CTRL_R6_LONG2", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a response file holds a mode", "CTRL_R6_RSP",
               PY + 'from pathlib import Path\nPath(WORK, "planted.rsp").write_text("-DCTRL_R6_RSP\\n")\n'
                    'cc("cc", "@planted.rsp", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("-imacros of a header the builder writes defines a mode", "CTRL_R6_IMACROS",
               PY + 'from pathlib import Path\nPath(WORK, "modes.h").write_text("#define CTRL_R6_IMACROS 1\\n")\n'
                    'cc("cc", "-imacros", "modes.h", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("a precompiled header the builder makes defines a mode", "CTRL_R6_PCH",
               PY + 'from pathlib import Path\nPath(WORK, "modes.h").write_text("#define CTRL_R6_PCH 1\\n")\n'
                    'cc("cc", "-x", "c-header", "modes.h", "-o", "modes.h.gch")\n'
                    'Path(WORK, "modes.h").write_text("#error only the precompiled header defines the mode\\n")\n'
                    'cc("cc", "-include", "modes.h", *INC, "-c", SRC, "-o", "planted.o")\n'),
    under_mode("-include of a header the builder writes defines a mode", "CTRL_R7_INCLUDE",
               PY + 'from pathlib import Path\nPath(WORK, "modes.h").write_text("#define CTRL_R7_INCLUDE 1\\n")\n'
                    'cc("cc", "-include", "modes.h", *INC, "-c", SRC, "-o", "planted.o")\n'),
    # R584-4-F1: each way a builder computes a C++ source's name, or writes the source.
    through_source("a Makefile's wildcard names the C++ source",
                   makefile("c++ -fsyntax-only -I$(PLANT_CTRL)/adp $(SRCS)",
                            "SRCS := $(wildcard $(PLANT_CTRL)/test/probe_r5/*.cpp)\n"), True),
    through_source("a builder joins a C++ source's name",
                   PY + 'STEM = "bench"\ncc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", '
                        'CTRL + "/test/probe_r5/" + STEM + ".cpp")\n'),
    through_source("a glob names the C++ source",
                   PY + 'import glob\ncc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", '
                        '*glob.glob(CTRL + "/test/probe_r5/*.cpp"))\n'),
    through_source("an iterdir names the C++ source",
                   PY + 'from pathlib import Path\n'
                        'cc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", *[str(p) for p in '
                        'Path(CTRL, "test/probe_r5").iterdir() if p.suffix == ".cpp"])\n'),
    through_source("a builder writes the C++ source from a literal",
                   PY + 'from pathlib import Path\nPath(WORK, "planted.cpp").write_text(\'#include "adp_r5.h"\\n\')\n'
                        'cc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", "planted.cpp")\n', probe=False),
    through_source("a builder writes the C++ source's include from an f-string",
                   PY + 'from pathlib import Path\nHDR = "adp_r5.h"\n'
                        'Path(WORK, "planted.cpp").write_text(f\'#include "{HDR}"\\n\')\n'
                        'cc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", "planted.cpp")\n', probe=False),
    through_source("a builder writes the C++ source from a template it formats",
                   PY + 'from pathlib import Path\nTEMPLATE = \'#include "{}"\\n\'\n'
                        'Path(WORK, "planted.cpp").write_text(TEMPLATE.format("adp_r5.h"))\n'
                        'cc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", "planted.cpp")\n', probe=False),
    through_source("a builder copies the C++ source from a template file",
                   PY + 'import shutil\nshutil.copy(os.path.join(WORK, "template.txt"), os.path.join(WORK, '
                        '"planted.cpp"))\ncc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", "planted.cpp")\n',
                   probe=False, beside=(("template.txt", '#include "adp_r5.h"\n'),)),
    through_source("a written C++ source reaches the header through a header it writes beside it",
                   PY + 'from pathlib import Path\nPath(WORK, "gen.hpp").write_text(\'#include "adp_r5.h"\\n\')\n'
                        'Path(WORK, "planted.cpp").write_text(\'#include "gen.hpp"\\n\')\n'
                        'cc("c++", "-fsyntax-only", "-I" + CTRL + "/adp", "planted.cpp")\n', probe=False),
    through_source("--include-directory names where the C++ source's header is",
                   PY + 'from pathlib import Path\nPath(WORK, "inc").mkdir()\n'
                        'Path(WORK, "inc", "gen.hpp").write_text(\'#include "adp_r5.h"\\n\')\n'
                        'Path(WORK, "planted.cpp").write_text(\'#include "gen.hpp"\\n\')\n'
                        'cc("c++", "-fsyntax-only", "--include-directory", WORK + "/inc", "-I" + CTRL + "/adp", '
                        '"planted.cpp")\n', probe=False),
    through_source("a builder copies a C++ source out of its own directories and compiles it from elsewhere",
                   PY + 'import shutil\nos.utime(os.path.join(WORK, "template.cpp"), (946684800, 946684800))\n'
                        'for name in ("out", "tmp", "build"):\n    os.makedirs(os.path.join(WORK, name))\n'
                        'shutil.copy2(os.path.join(WORK, "template.cpp"), os.path.join(WORK, "out", "sim.cpp"))\n'
                        'subprocess.run(["c++", "-fsyntax-only", "-I" + CTRL + "/adp", os.path.join(WORK, "out", '
                        '"sim.cpp")], cwd=os.path.join(WORK, "build"), env={**os.environ, "TMPDIR": '
                        'os.path.join(WORK, "tmp")}, check=False, capture_output=True)\n',
                   probe=False, beside=(("template.cpp", '#include "adp_r5.h"\n'),)),
    # The dependency output a compile must have: one that fails, or one no pass can make, refuses by name.
    Plant("a builder compiles C++ from its standard input", "ctrl", "", "", "",
          "it compiles its standard input, which a dependency pass cannot read again",
          run=PY + 'subprocess.run(["c++", "-x", "c++", "-fsyntax-only", "-"], cwd=WORK, input=b"int x;\\n", '
                   'check=False, capture_output=True)\n'),
    Plant("a builder passes a dependency option the pass cannot override", "ctrl", "", "", "",
          "its dependency pass wrote no rule naming what it read",
          run=PY + 'cc("cc", "-Wp,-MD,planted.d", *INC, "-c", SRC, "-o", "planted.o")\n'),
    # Fail closed: what the capture must hold, and what it must not miss.
    Plant("the capture is missing", "ctrl", "", "", "", "no capture at ", alter="missing"),
    Plant("the capture is empty", "ctrl", "", "", "", "is empty: it records no compiler invocation",
          alter="empty"),
    Plant("the capture holds nothing of a known builder", "ctrl", "", "", "",
          "the capture holds no invocation of sw/firmware/ctrl/test/test_ctrl_firmware.py",
          alter="drop sw/firmware/ctrl/test/test_ctrl_firmware.py"),
    # A known builder held only through another's run, and a builder dropped from the known set that another
    # still runs (the coverage gate runs the control and store gates), each refused by name.
    Plant("a known builder whose own run compiles nothing, which another builder still runs", "ctrl", "", "", "",
          "the capture holds no invocation of sw/firmware/ctrl/test/test_ctrl_firmware.py from a run of its own",
          alter="drop run sw/firmware/ctrl/test/test_ctrl_firmware.py"),
    Plant("a builder dropped from the known set, which another builder still runs", "ctrl", "", "", "",
          "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py names the firmware's tree and is a program",
          alter="forget sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py"),
    Plant("a builder runs a compiler by its own path", "ctrl", "", "", "",
          "a compiler the capture does not wrap",
          run=PY + 'import shutil\nREAL = shutil.which("gcc", path=os.pathsep.join(os.environ["PATH"].split('
                   'os.pathsep)[1:]))\ncc(REAL, "-c", "planted.c", "-o", "planted.o")\n'),
    Plant("a Makefile runs a compiler by its own path", "ctrl", "", "", "",
          "a compiler the capture does not wrap", run=makefile("$(PLANT_GCC) -c planted.c -o planted.o"), make=True),
    Plant("a builder runs a compiler on a PATH of its own", "ctrl", "", "", "",
          "a compiler the capture does not wrap",
          run=PY + 'subprocess.run(["gcc", "-c", "planted.c", "-o", "planted.o"], cwd=WORK, check=False, '
                   'env={"PATH": "/usr/bin:/bin"}, capture_output=True)\n'),
    Plant("a builder of the firmware that no capture holds", "ctrl", "", "", "",
          "sw/firmware/ctrl/test/planted_unrun.py names the firmware's tree, compiled nothing in the capture",
          texts=(("planted_unrun.py", '"""A builder of sw/firmware/ctrl that nothing runs."""\n'),)),
    Plant("a builder compiles with a flag the compiler cannot expand (a macro with no name)", "ctrl", "", "", "",
          "ran cc -D=1 -c planted.c -o planted.o, which the compiler could not expand",
          run=PY + 'cc("cc", "-D=1", "-c", "planted.c", "-o", "planted.o")\n'),
    Plant("a response file names the source", "ctrl", "", "", "",
          "an input it names where the recorder did not see it (a response file's)",
          run=PY + 'from pathlib import Path\nPath(WORK, "planted.rsp").write_text("-DCTRL_R6_HIDDEN planted.c\\n")\n'
                   'cc("cc", "@planted.rsp", "-c")\n'),
    Plant("a response file names the output", "ctrl", "", "", "",
          "its expansion went to an output the recorder did not see (a response file's)",
          run=PY + 'from pathlib import Path\nPath(WORK, "planted.rsp").write_text("-DCTRL_R6_OUT -o planted.o\\n")\n'
                   'cc("cc", "@planted.rsp", "-c", "planted.c")\n'),
    Plant("a builder reads first a precompiled header whose making the recorder cannot see", "ctrl", "", "", "",
          "which no compile the capture holds made",
          run=PY + 'from pathlib import Path\nPath(WORK, "modes.h").write_text("#define CTRL_R6_UNSEEN 1\\n")\n'
                   'Path(WORK, "out.rsp").write_text("-o modes.h.gch\\n")\n'
                   'cc("cc", "-x", "c-header", "modes.h", "@out.rsp")\n'
                   'cc("cc", "-include", "modes.h", "-c", "planted.c", "-o", "planted.o")\n'),
    Plant("a builder reads first a stack source", "ctrl", "", "", "",
          "tsn-c-stack/src/adp.c first, a file of the stack that is not one of its public headers",
          run=PY + 'cc("cc", "-include", STACK + "/src/adp.c", "-I" + STACK + "/include", "-c", "planted.c", "-o", '
                   '"planted.o")\n'),
    Plant("a builder reads a firmware header first into a compile of a stack source", "ctrl", "", "", "",
          "first into a compile of the stack's own sources: a file of the checkout outside the stack",
          run=PY + 'cc("cc", "-include", CTRL + "/mbx/mbx_hal.h", *INC, "-c", STACK + "/src/adp.c", "-o", '
                   '"planted.o")\n'),
    # R584-5-F2: the configurations only the Verilator builders compile, judged where their capture is.
    wire_mode("V1 a mode only the AECP wire comparison gives", "defined(PP_TOP_TIM_DEFAULTS)"),
    wire_mode("V2 a mode only its two-interface reference gives", "defined(PP_TOP_IF2)"),
    wire_mode("V3 a value only its two-interface reference gives",
              "defined(AECP_WIRE_INTERFACES) && AECP_WIRE_INTERFACES > 1"),
    Plant("a header only the MAAP differential's C++ source reaches includes a stack file in C++ only", "ctrl",
          "+maap/maap_r584.h", "", f'#ifdef __cplusplus\n#include "{FROM_CTRL}"\n#endif\n',
          f"firmware: sw/firmware/ctrl/maap/maap_r584.h includes {STRING_NAMED}",
          extra=(("test/test_maap_differential.cpp", "#include \"maap.h\"\n",
                  "#include \"maap.h\"\n#include \"../maap/maap_r584.h\"\n"),), needs="verilator",
          replay="test_maap_differential.cpp"),
    Plant("the capture holds nothing of the AECP wire comparison", "ctrl", "", "", "",
          "the capture holds no invocation of sw/firmware/ctrl/test/aecp_wire.py",
          alter="drop sw/firmware/ctrl/test/aecp_wire.py", needs="verilator"),
    # Passing controls: what the boundary admits.
    Plant("pass: the firmware includes a public header", "ctrl", "port/ctrl_debug.c", "#include \"ctrl_debug.h\"\n",
          "#include \"ctrl_debug.h\"\n#include \"wire.h\"\n", "", run=arms("port/ctrl_debug.c")),
    Plant("pass: the stack includes only its own header and the C library", "stack", "src/maap.c",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"wire.h\"\n#include <stdint.h>\n", "",
          run=arms("tsn-c-stack/src/maap.c")),
    Plant("pass: a stack test reaches the stack's example", "stack", "tests/test_maap_debug.cpp",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"../examples/adp_port.h\"\n", "",
          run=tests('STACK + "/tests/test_maap_debug.cpp"')),
    Plant("pass: a stack source includes a header nobody supplies: the compile fails, and compiled nothing", "stack",
          "src/adp.c", "#include <assert.h>\n", "#include <assert.h>\n#include \"image_layout.h\"\n", "",
          run=arms("tsn-c-stack/src/adp.c")),
    Plant("pass: a builder compiles a C++ source that is no file: the compile fails, and compiled nothing", "ctrl", "",
          "", "", "", run=PY + 'cc("c++", "-fsyntax-only", "planted_r5_absent.cpp")\n'),
    Plant("pass: a stack source includes an OS header of the host's C implementation", "stack", "src/adp.c",
          "#include <assert.h>\n", "#include <assert.h>\n#include <unistd.h>\n", "",
          run=arms("tsn-c-stack/src/adp.c")),
    Plant("pass: a builder compiles the firmware with a mode no file tests", "ctrl", "", "", "", "",
          run=PY + 'cc("cc", "-DCTRL_R5_UNTESTED", *INC, "-c", SRC, "-o", "planted.o")\n'),
    Plant("pass: a builder's own C++ source whose include a macro computes reads a firmware header", "ctrl", "", "",
          "", "", beside=(("tool/runtime.cpp", INSTALLED),),
          run=PY + 'cc("c++", "-fsyntax-only", *INC, os.path.join(WORK, "tool", "runtime.cpp"))\n'),
)


#: The base every control shares: the unplanted copy compiled the ways the controls compile it (the image at both
#: shapes, every firmware and stack source by the arms, the stack's tests and a C++ source of every firmware header
#: by the arms' test compile), which must pass.
BASE = Plant("pass: the copies as they are, the base the controls share", "ctrl", "", "", "",
             "", run=PY + ARMS + TESTS + IMAGE +
             'from pathlib import Path\nimport ctrl_build\n'
             'arms(*ctrl_build.PORTABLE, "plat/mbx_plat_mmio.c")\n'
             'arms("aecp/aecp.c", extra=("-I" + CTRL + "/aecp",))\n'
             'tests(*(f"{STACK}/tests/test_{n}.cpp" for n in ("adp", "acmp", "maap", "maap_debug", "adp_reentry")))\n'
             'tests(probe(*sorted(p.name for d in ("acmp", "adp", "maap", "mbx", "port", "loop", "app") '
             'for p in Path(CTRL, d).glob("*.h"))), extra=("-I" + CTRL + "/aecp", "-I" + NVM + "/plat"))\n'
             'image("endstation_ax7101_1x1_tdm8")\nimage("endstation_ax7101_8x8")\n')
