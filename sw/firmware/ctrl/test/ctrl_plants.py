# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_plants.py - the boundary gate's planted controls (#697).

ctrl_boundary.py --selftest judges a copy of the ctrl tree and of the stack
with each plant written into it: each refused by the finding (or the refusal)
it names, or passing. The base the controls share is the copies as they are,
judged against the run's capture. A control with a planted builder runs that
builder through the capture (ctrl_capture.run), in a directory of its own
holding an empty planted.c, with PLANT_CTRL, PLANT_STACK and PLANT_WORK naming
the copies and that directory (PLANT_GCC the real gcc); what it compiled joins the run's capture for
that control alone. Whatever form the builder writes a flag or a source's name
in, the boundary judges the invocation the compiler was given. This module is
one of the gate's own, never a builder (ctrl_configs.GATE).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Plant:
    """One control: written into the stack's copy or the ctrl tree's copy, side by side, so a relative path
    from one reaches the other (a "+" file is written whole as a new file; no file, none), with `extra` edits
    of the same kind in the same copy; refused by a finding (or a refusal) holding `needle`, or passing when
    `needle` is "". `run` is a planted builder's text, a Makefile when `make` (run as `make -f`) and Python
    otherwise, run through the capture with `beside` written next to it; one that only compiles a mode
    (`shared`) runs once, before the base, and what it compiled joins the base every control shares, which must
    still pass. `texts` are builder texts the checkout is read as holding (a path from the gate's directory, and
    its text), never run; `alter` changes the capture the control is judged against: "missing", "empty", or
    "drop " and a builder whose invocations it loses."""

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
    shared: bool = False


#: A planted Python builder's head: the copies and its own directory, and the compiler runs it makes there.
PY = ('import os, subprocess\nCTRL, STACK, WORK = os.environ["PLANT_CTRL"], os.environ["PLANT_STACK"], '
      'os.environ["PLANT_WORK"]\n\n\ndef cc(*words, shell=False):\n'
      '    subprocess.run(words[0] if shell else list(words), cwd=WORK, shell=shell, check=False,\n'
      '                   capture_output=True)\n\n\n')
#: The firmware adapter a mode's control reaches a stack example's header from, under that mode.
ANCHOR = '#include "adp_mbx.h"\n'
#: The C++ source a computed-name control compiles, in the ctrl tree's copy, and the header it reaches.
PROBE = "test/probe_r5/bench.cpp"
CXX_HEADER = "#ifdef __cplusplus\n#include \"adp_port.h\"\n#endif\n"
CXX_NEEDLE = ("firmware c++: adp/adp_r5.h includes tsn-c-stack/examples/adp_port.h, not one of the stack's public "
              "headers")


def under_mode(name: str, macro: str, label: str, run: str, make: bool = False, test: str = "") -> Plant:
    """A control whose planted builder compiles with a mode, in some form: the firmware's ADP adapter reaches a
    stack example's header only under it (or when its value, `test`, holds), so the finding names the mode as
    the compiler was given it, `label`."""
    return Plant(name, "ctrl", "adp/adp_mbx.c", ANCHOR,
                 ANCHOR + (f"#if {test}\n" if test else f"#ifdef {macro}\n") + '#include "adp_port.h"\n#endif\n',
                 f"firmware [{label}]: adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the "
                 "stack's public headers", run=run, make=make, shared=True)


def through_source(name: str, run: str, make: bool = False, probe: bool = True,
                   beside: tuple[tuple[str, str], ...] = ()) -> Plant:
    """A control whose planted builder compiles a C++ source it computes the name of, or writes: a new firmware
    header reached only from that source includes a stack example's header in C++ only."""
    extra = (("+" + PROBE, "", '#include "adp_r5.h"\n'),) if probe else ()
    return Plant(name, "ctrl", "+adp/adp_r5.h", "", CXX_HEADER, CXX_NEEDLE, run=run, make=make, beside=beside,
                 extra=extra)


def makefile(recipe: str, head: str = "") -> str:
    """A planted Makefile: its variables, then one target whose recipe is `recipe`."""
    return f"{head}planted:\n\t{recipe}\n"


PLANTS = (
    Plant("stack source includes the mailbox HAL", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"mbx_hal.h\"\n",
          "the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("stack source includes the register-map contract", "stack", "src/acmp.c", "#include \"acmp.h\"\n",
          "#include \"acmp.h\"\n#include \"mbx_contract.h\"\n", "includes sw/firmware/ctrl/mbx/mbx_contract.h"),
    Plant("stack source includes the composition", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"ctrl_app.h\"\n", "includes sw/firmware/ctrl/app/ctrl_app.h"),
    Plant("stack source includes the store's port", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"nvm_state.h\"\n", "includes sw/firmware/ctrl_nvm/nvm_state.h"),
    Plant("stack source includes the loop through a macro", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#define TSN_LOOP \"ctrl_loop.h\"\n#include TSN_LOOP\n",
          "includes sw/firmware/ctrl/loop/ctrl_loop.h"),
    Plant("stack public header includes the platform's header", "stack", "include/wire.h", "#include <stdint.h>\n",
          "#include <stdint.h>\n#include \"ctrl_debug.h\"\n", "the stack's include/wire.h includes"),
    Plant("stack source includes a header nobody supplies", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"image_layout.h\"\n", "does not preprocess with the firmware's flags"),
    Plant("stack source includes an OS header", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include <unistd.h>\n", "includes "),
    Plant("firmware reaches a stack example's header", "ctrl", "adp/adp_mbx.c", "#include \"adp_mbx.h\"\n",
          "#include \"adp_mbx.h\"\n#include \"adp_port.h\"\n",
          "adp/adp_mbx.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    Plant("firmware header reaches a stack source by a relative path", "ctrl", "maap/maap_mbx.h",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"../../tsn-c-stack/src/maap.c\"\n",
          "includes tsn-c-stack/src/maap.c, not one of the stack's public headers"),
    Plant("image source reaches a stack test's header", "ctrl", "test/rv32_image/image_main.c",
          "#include \"ctrl_app.h\"\n",
          "#include \"ctrl_app.h\"\n#include \"../../../tsn-c-stack/tests/acmp_fake.hpp\"\n",
          "test/rv32_image/image_main.c includes tsn-c-stack/tests/acmp_fake.hpp"),
    Plant("a copy of the stack's wire.h in the firmware", "ctrl", "+mbx/wire.h", "", "#include <stdint.h>\n",
          "mbx/wire.h has the name of the stack's wire.h"),
    Plant("a copy of the stack's adp.c in the firmware", "ctrl", "+adp/adp.c", "", "int adp_copy;\n",
          "adp/adp.c has the name of the stack's adp.c"),
    Plant("stack source includes the mailbox HAL under the re-entry assertion", "stack", "src/acmp.c",
          "#ifdef CTRL_REENTRY_ASSERT\n", "#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_hal.h\"\n",
          "host [-DCTRL_REENTRY_ASSERT]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("stack source includes the platform's header in a debug build", "stack", "src/maap.c",
          "#ifndef NDEBUG\n#include <assert.h>\n", "#ifndef NDEBUG\n#include <assert.h>\n#include \"ctrl_debug.h\"\n",
          "host [-UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/port/ctrl_debug.h"),
    Plant("stack source includes the contract in a debug build with the re-entry assertion", "stack", "src/maap.c",
          "#ifndef NDEBUG\n#include <assert.h>\n",
          "#ifndef NDEBUG\n#include <assert.h>\n#ifdef CTRL_REENTRY_ASSERT\n#include \"mbx_contract.h\"\n#endif\n",
          "host [-DCTRL_REENTRY_ASSERT -UNDEBUG]: the stack's src/maap.c includes sw/firmware/ctrl/mbx/mbx_contract.h"),
    Plant("firmware adapter reaches a stack test's fake under the re-entry assertion", "ctrl", "acmp/acmp_mbx.c",
          "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n#include \"../../tsn-c-stack/tests/acmp_fake.hpp\"\n"
          "#endif\n",
          "firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes tsn-c-stack/tests/acmp_fake.hpp"),
    Plant("firmware adapter reaches the stack's test fake by its checkout path under the re-entry assertion",
          "ctrl", "acmp/acmp_mbx.c", "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifdef CTRL_REENTRY_ASSERT\n"
          "#include \"../../../../third_party/tsn-c-stack/tests/acmp_fake.hpp\"\n#endif\n",
          "firmware [-DCTRL_REENTRY_ASSERT]: acmp/acmp_mbx.c includes third_party/tsn-c-stack/tests/acmp_fake.hpp, "
          "not one of the stack's public headers"),
    Plant("firmware tests a mode by its value", "ctrl", "maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
          "#include \"maap_mbx.h\"\n#if CTRL_REENTRY_ASSERT\n#include \"../../tsn-c-stack/src/maap.c\"\n#endif\n",
          "firmware [-DCTRL_REENTRY_ASSERT]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c"),
    Plant("the SRP image's composition reaches a stack source", "ctrl", "test/ctrl_image.c",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n#include \"../../tsn-c-stack/src/acmp.c\"\n",
          "firmware [-DCTRL_IMAGE_SRP]: test/ctrl_image.c includes tsn-c-stack/src/acmp.c"),
    Plant("a stack test includes the mailbox HAL", "stack", "tests/test_maap_debug.cpp", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#include \"mbx_hal.h\"\n",
          "tests: the stack's tests/test_maap_debug.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a stack test includes the firmware's harness", "stack", "tests/test_adp.cpp", "#include \"adp.h\"\n",
          "#include \"adp.h\"\n#include \"fw_gtest.hpp\"\n",
          "tests: the stack's tests/test_adp.cpp includes sw/firmware/gtest/fw_gtest.hpp"),
    Plant("a stack test includes the platform's pool in its release build", "stack", "tests/test_adp_reentry.cpp",
          "#include \"adp.h\"\n", "#include \"adp.h\"\n#ifdef ADP_TEST_RELEASE\n#include \"ctrl_pool.h\"\n#endif\n",
          "tests [-DADP_TEST_RELEASE]: the stack's tests/test_adp_reentry.cpp includes "
          "sw/firmware/ctrl/port/ctrl_pool.h"),
    Plant("a stack public header includes the mailbox HAL for C++ only", "stack", "include/acmp.h",
          "#ifdef __cplusplus\nextern \"C\" {\n", "#ifdef __cplusplus\n#include \"mbx_hal.h\"\nextern \"C\" {\n",
          "tests: the stack's tests/test_acmp.cpp includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a mode a builder compiles with is explored without being named here", "stack", "src/adp.c",
          "#include <assert.h>\n", "#include <assert.h>\n#ifdef CTRL_PLANTED_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DCTRL_PLANTED_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=PY + 'cc("cc", "-DCTRL_PLANTED_MODE", "-c", "planted.c", "-o", "planted.o")\n', shared=True),
    Plant("a mode an AECP arm writes is explored without being named here", "stack", "src/acmp.c",
          "#include \"acmp.h\"\n", "#include \"acmp.h\"\n#ifdef AECP_TEST_APP\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DAECP_TEST_APP]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a mode a new builder nobody lists compiles with is explored", "stack", "src/maap.c",
          "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_PLANTED_BUILDER\n#include \"ctrl_loop.h\"\n#endif\n",
          "host [-DCTRL_PLANTED_BUILDER]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          run=PY + 'cc("gcc", "-DCTRL_PLANTED_BUILDER", "-c", "planted.c", "-o", "planted.o")\n', shared=True),
    Plant("stack source includes the AECP core's header", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#include \"aecp.h\"\n", "the stack's src/adp.c includes sw/firmware/ctrl/aecp/aecp.h"),
    Plant("a stack test includes the AECP adapter", "stack", "tests/test_adp.cpp", "#include \"adp.h\"\n",
          "#include \"adp.h\"\n#include \"aecp_mbx.h\"\n",
          "tests: the stack's tests/test_adp.cpp includes sw/firmware/ctrl/aecp/aecp_mbx.h"),
    Plant("the AECP core reaches a stack source", "ctrl", "aecp/aecp.c", "#include \"aecp_internal.h\"\n",
          "#include \"aecp_internal.h\"\n#include \"../../tsn-c-stack/src/acmp.c\"\n",
          "aecp/aecp.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers"),
    Plant("the AECP application bridge reaches a stack example's header", "ctrl", "app/ctrl_app_aecp.c",
          "#include \"ctrl_app_aecp.h\"\n", "#include \"ctrl_app_aecp.h\"\n#include \"adp_port.h\"\n",
          "app/ctrl_app_aecp.c includes tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    Plant("the AECP image's SRP composition reaches a stack source", "ctrl", "test/ctrl_aecp_image.c",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n",
          "#ifdef CTRL_IMAGE_SRP\n#include \"srp_mbx.h\"\n#include \"../../tsn-c-stack/src/maap.c\"\n",
          "firmware [-DCTRL_IMAGE_SRP]: test/ctrl_aecp_image.c includes tsn-c-stack/src/maap.c"),
    Plant("a copy of the stack's acmp.h in the AECP directory", "ctrl", "+aecp/acmp.h", "", "#include <stdint.h>\n",
          "aecp/acmp.h has the name of the stack's acmp.h"),
    Plant("the image reaches a stack example's header under a shape's stream count", "ctrl",
          "test/rv32_image/image_main.c", "#include <stdbool.h>\n",
          "#include <stdbool.h>\n#if IMAGE_SINKS > 1u\n#include \"../../../tsn-c-stack/examples/adp_port.h\"\n"
          "#error PROBE-REACHED\n#endif\n",
          "firmware [-DIMAGE_SINKS=2u -DIMAGE_SOURCES=1u]: test/rv32_image/image_main.c includes "
          "tsn-c-stack/examples/adp_port.h, not one of the stack's public headers"),
    Plant("a firmware header reaches a stack test's fake in C++ only", "ctrl", "acmp/acmp_mbx.h",
          "#ifdef __cplusplus\nextern \"C\" {\n", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\nextern \"C\" {\n",
          "firmware c++: acmp/acmp_mbx.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers"),
    Plant("the AECP image reaches a stack source at a shape its generated header gives many maps", "ctrl",
          "test/ctrl_aecp_image.c", "#include \"aecp_entity_gen.h\"\n",
          "#include \"aecp_entity_gen.h\"\n#if AECP_ENTITY_MAPS > 8u\n#include \"../../tsn-c-stack/src/acmp.c\"\n"
          "#endif\n",
          "firmware [shape=endstation_ax7101_8x8]: test/ctrl_aecp_image.c includes tsn-c-stack/src/acmp.c"),
    Plant("an adapter reaches a stack source where the SRP shape header is force-included", "ctrl",
          "maap/maap_mbx.c", "#include \"maap_mbx.h\"\n",
          "#include \"maap_mbx.h\"\n#ifdef CTRL_SRP_SOURCES\n#include \"../../tsn-c-stack/src/maap.c\"\n#endif\n",
          "firmware [-include srp_entity_gen.h]: maap/maap_mbx.c includes tsn-c-stack/src/maap.c"),
    Plant("an adapter reaches a stack source on the two-interface contract", "ctrl", "adp/adp_mbx.c",
          "#include \"adp_mbx.h\"\n",
          "#include \"adp_mbx.h\"\n#if MBX_N_IF > 1u\n#include \"../../tsn-c-stack/src/adp.c\"\n#endif\n",
          "firmware [interfaces=2]: adp/adp_mbx.c includes tsn-c-stack/src/adp.c"),
    Plant("an adapter reaches a stack source where a build leaves lwSRP's profile undefined", "ctrl",
          "acmp/acmp_mbx.c", "#include \"acmp_mbx.h\"\n",
          "#include \"acmp_mbx.h\"\n#ifndef LWSRP_MILAN\n#include \"../../tsn-c-stack/src/acmp.c\"\n#endif\n",
          "firmware: acmp/acmp_mbx.c includes tsn-c-stack/src/acmp.c, not one of the stack's public headers"),
    Plant("the AECP core reaches a stack source at a value only its arms compile with", "ctrl", "aecp/aecp.c",
          "#include \"aecp_internal.h\"\n",
          "#include \"aecp_internal.h\"\n#if AECP_TEST_INTERFACES > 1\n#include \"../../tsn-c-stack/src/acmp.c\"\n"
          "#endif\n",
          "firmware [-DAECP_TEST_INTERFACES=2]: aecp/aecp.c includes tsn-c-stack/src/acmp.c, not one of the stack's "
          "public headers"),
    Plant("a mode a builder writes as two arguments is explored", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_SPLIT_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DCTRL_SPLIT_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          run=PY + 'cc("cc", "-D", "CTRL_SPLIT_MODE", "-c", "planted.c", "-o", "planted.o")\n', shared=True),
    Plant("a mode a new Makefile writes as two words is explored", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_SPLIT_MAKE\n#include \"ctrl_loop.h\"\n#endif\n",
          "host [-DCTRL_SPLIT_MAKE]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          run=makefile("cc -D CTRL_SPLIT_MAKE -c planted.c -o planted.o"), make=True, shared=True),
    Plant("a header only the MAAP differential's C++ source reaches includes a stack test's fake in C++ only",
          "ctrl", "+maap/maap_r584.h", "", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n",
          "firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers",
          run=PY + 'cc("c++", "-std=c++17", "-fsyntax-only", "-I" + CTRL + "/maap", "-I" + STACK + "/include",\n'
                   '   CTRL + "/test/test_maap_differential.cpp")\n',
          extra=(("test/test_maap_differential.cpp", "#include \"maap.h\"\n",
                  "#include \"maap.h\"\n#include \"maap_r584.h\"\n"),)),
    # R584-4-F2, R585-4-F1, R584-3-S1 and round 4's: each form a builder writes a mode in.
    under_mode("a Makefile's patsubst writes a mode", "CTRL_R5_PATSUBST", "-DCTRL_R5_PATSUBST",
               makefile("cc $(patsubst %,-D%,$(MODES)) -c planted.c -o planted.o", "MODES := CTRL_R5_PATSUBST\n"),
               True),
    under_mode("a Makefile's foreach writes a mode", "CTRL_R5_FOREACH", "-DCTRL_R5_FOREACH",
               makefile("cc $(foreach m,CTRL_R5_FOREACH,-D$(m)) -c planted.c -o planted.o"), True),
    under_mode("a Makefile appends a mode with no space", "CTRL_R5_APPEND", "-DCTRL_R5_APPEND",
               makefile("cc $(CFLAGS) -c planted.c -o planted.o", "CFLAGS+=-DCTRL_R5_APPEND\n"), True),
    under_mode("a Makefile writes a mode's name after a bare -D", "CTRL_R5_SPACED", "-DCTRL_R5_SPACED",
               makefile("cc -D $(M) -c planted.c -o planted.o", "M := CTRL_R5_SPACED\n"), True),
    under_mode("a Makefile computes a mode's name", "CTRL_R4_MAKE", "-DCTRL_R4_MAKE",
               makefile("cc -D$(MODE) -c planted.c -o planted.o", "MODE := CTRL_R4_MAKE\n"), True),
    under_mode("a Makefile computes a mode's value", "CTRL_R4_MAKE_VALUE", "-DCTRL_R4_MAKE_VALUE=2",
               makefile("cc -DCTRL_R4_MAKE_VALUE=$(VALUE) -c planted.c -o planted.o", "VALUE := 2\n"), True,
               "CTRL_R4_MAKE_VALUE > 1"),
    under_mode("a Makefile prefixes -D to the modes it lists", "CTRL_R4_ADDPREFIX", "-DCTRL_R4_ADDPREFIX",
               makefile("cc $(addprefix -D,$(MODES)) -c planted.c -o planted.o", "MODES := CTRL_R4_ADDPREFIX\n"),
               True),
    under_mode("an f-string writes a mode after other text", "CTRL_R5_FSTRING", "-DCTRL_R5_FSTRING",
               PY + 'CC = "cc"\ncc(f"{CC} -DCTRL_R5_FSTRING -c planted.c -o planted.o", shell=True)\n'),
    under_mode("a multi-word literal holds a mode", "CTRL_R5_SPLIT", "-DCTRL_R5_SPLIT",
               PY + 'cc("cc", *"-O2 -DCTRL_R5_SPLIT".split(), "-c", "planted.c", "-o", "planted.o")\n'),
    under_mode("a shell command's literal holds a mode", "CTRL_R5_SHELL", "-DCTRL_R5_SHELL",
               PY + 'cc("cc -DCTRL_R5_SHELL -c planted.c -o planted.o", shell=True)\n'),
    under_mode("shlex splits a mode out of a literal", "CTRL_R5_SHLEX", "-DCTRL_R5_SHLEX",
               PY + 'import shlex\ncc("cc", *shlex.split("-O2 -DCTRL_R5_SHLEX"), "-c", "planted.c", "-o", '
                    '"planted.o")\n'),
    under_mode("a bare -D takes a mode a conditional chooses", "CTRL_R5_CHOSEN", "-DCTRL_R5_CHOSEN",
               PY + 'X = True\ncc("cc", "-D", "CTRL_R5_CHOSEN" if X else "CTRL_R5_OTHER", "-c", "planted.c", "-o", '
                    '"planted.o")\n'),
    under_mode("str.format writes a mode", "CTRL_R5_FORMAT", "-DCTRL_R5_FORMAT",
               PY + 'cc("cc", "-D{}".format("CTRL_R5_FORMAT"), "-c", "planted.c", "-o", "planted.o")\n'),
    under_mode("a builder joins -D to a mode it computes", "CTRL_R4_JOINED", "-DCTRL_R4_JOINED",
               PY + 'MODE = "CTRL_R4_JOINED"\ncc("cc", "-D" + MODE, "-c", "planted.c", "-o", "planted.o")\n'),
    under_mode("a builder formats a mode with %", "CTRL_R4_PERCENT", "-DCTRL_R4_PERCENT",
               PY + 'cc("cc", "-D%s" % "CTRL_R4_PERCENT", "-c", "planted.c", "-o", "planted.o")\n'),
    under_mode("a builder joins a value to a mode", "CTRL_R4_VALUE", "-DCTRL_R4_VALUE=2",
               PY + 'N = 2\ncc("cc", "-DCTRL_R4_VALUE=" + str(N), "-c", "planted.c", "-o", "planted.o")\n',
               test="CTRL_R4_VALUE > 1"),
    under_mode("an f-string computes a mode's name", "CTRL_R4_MODE", "-DCTRL_R4_MODE",
               PY + 'SUFFIX = "MODE"\ncc("cc", f"-DCTRL_R4_{SUFFIX}", "-c", "planted.c", "-o", "planted.o")\n'),
    under_mode("a bare -D takes the modes a list holds", "CTRL_R4_BARE", "-DCTRL_R4_BARE",
               PY + 'NAMES = ["CTRL_R4_BARE"]\ncc(*["cc", "-D"] + NAMES, "-c", "planted.c", "-o", "planted.o")\n'),
    # R584-4-F1: each way a builder computes a C++ source's name, or writes the source.
    through_source("a Makefile's wildcard names the C++ source",
                   makefile("c++ -fsyntax-only -I$(PLANT_CTRL)/adp $(SRCS)",
                            "SRCS := $(wildcard $(PLANT_CTRL)/test/probe_r5/*.cpp)\n"), True),
    through_source("a builder joins a C++ source's name",
                   PY + 'STEM = "bench"\ncc("c++", "-fsyntax-only", CTRL + "/test/probe_r5/" + STEM + ".cpp")\n'),
    through_source("a glob names the C++ source",
                   PY + 'import glob\ncc("c++", "-fsyntax-only", *glob.glob(CTRL + "/test/probe_r5/*.cpp"))\n'),
    through_source("an iterdir names the C++ source",
                   PY + 'from pathlib import Path\n'
                        'cc("c++", "-fsyntax-only", *[str(p) for p in Path(CTRL, "test/probe_r5").iterdir() '
                        'if p.suffix == ".cpp"])\n'),
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
    Plant("a builder compiles a C++ source that is no file", "ctrl", "", "", "",
          "compiled C++ from ", run=PY + 'cc("c++", "-fsyntax-only", "planted_r5_absent.cpp")\n'),
    Plant("a builder compiles C++ from its standard input", "ctrl", "", "", "",
          "compiled C++ from its standard input",
          run=PY + 'subprocess.run(["c++", "-x", "c++", "-fsyntax-only", "-"], cwd=WORK, input=b"int x;\\n", '
                   'check=False, capture_output=True)\n'),
    # Fail closed: what the capture must hold, and what it must not miss.
    Plant("the capture is missing", "ctrl", "", "", "", "no capture at ", alter="missing"),
    Plant("the capture is empty", "ctrl", "", "", "", "is empty: it records no compiler invocation",
          alter="empty"),
    Plant("the capture holds nothing of a known builder", "ctrl", "", "", "",
          "the capture holds no invocation of sw/firmware/ctrl/test/test_ctrl_firmware.py",
          alter="drop sw/firmware/ctrl/test/test_ctrl_firmware.py"),
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
    Plant("a builder compiles a stream count no shipped shape gives", "ctrl", "", "", "",
          "-DIMAGE_SINKS=99u, a stream count no shipped shape gives",
          run=PY + 'cc("cc", "-DIMAGE_SINKS=99u", "-c", "planted.c", "-o", "planted.o")\n'),
    Plant("a builder compiles with a flag whose macro has no name", "ctrl", "", "", "",
          "'-D=1', a -D or -U flag whose macro the boundary cannot name",
          run=PY + 'cc("cc", "-D=1", "-c", "planted.c", "-o", "planted.o")\n'),
    Plant("pass: the firmware includes a public header", "ctrl", "port/ctrl_debug.c", "#include \"ctrl_debug.h\"\n",
          "#include \"ctrl_debug.h\"\n#include \"wire.h\"\n", ""),
    Plant("pass: the stack includes only its own header and the C library", "stack", "src/maap.c",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"wire.h\"\n#include <stdint.h>\n", ""),
    Plant("pass: a stack test reaches the stack's example", "stack", "tests/test_maap_debug.cpp",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"adp_port.h\"\n", ""),
    Plant("pass: a builder compiles a mode no unit tests", "ctrl", "", "", "", "",
          run=PY + 'cc("cc", "-DCTRL_R5_UNTESTED", "-c", "planted.c", "-o", "planted.o")\n', shared=True),
)


#: The base every control shares: the copies as they are, judged first, which must pass.
BASE = Plant("pass: the copies as they are, the base the controls share", "ctrl", "", "", "", "")
