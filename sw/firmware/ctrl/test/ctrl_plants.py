# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_plants.py - the boundary gate's planted controls (#697).

ctrl_boundary.py --selftest judges a copy of the ctrl tree and of the stack
with each plant written into it, and of a builder's text where a plant gives
one: each refused by the finding (or the refusal) it names, or passing. The
base the controls share is the copies as they are. This module is one of the
gate's own, never a builder (ctrl_configs.GATE): its plants' flags are no
build's.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ctrl_build import HERE, Refusal


@dataclass(frozen=True)
class Plant:
    """One control: written into the stack's copy or the ctrl tree's copy, side by side, so a relative path
    from one reaches the other (a "+" file is written whole as a new file; no file, none), with `extra` edits
    of the same kind in the same copy; refused by a finding (or a refusal) holding `needle`, or passing when
    `needle` is "". `words` are a builder's arguments (flags, or a source's name), planted into a copy of the
    text of `builder` (a file of test/, or one relative to it; a new one when it holds none; a Makefile's
    recipe when it is one), which the boundary must then read without being told; `raw` is text added to that
    copy as it is, and `swap` an (old, new) edit of it."""

    name: str
    side: str
    file: str
    old: str
    new: str
    needle: str
    words: tuple[str, ...] = ()
    builder: str = "ctrl_arms.py"
    raw: str = ""
    swap: tuple[str, str] | tuple[()] = ()
    extra: tuple[tuple[str, str, str], ...] = ()


#: A builder the checkout does not hold: it names the firmware's shared builder, as every builder does.
NEW_BUILDER = '"""A builder of the firmware that nobody lists."""\nfrom ctrl_build import Tree\n'
#: A Makefile builder the checkout does not hold, of the firmware's tree.
NEW_MAKEFILE = "# A builder of sw/firmware/ctrl that nobody lists.\n"


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
    Plant("a mode an arm writes is explored without being named here", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_PLANTED_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DCTRL_PLANTED_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          ("-DCTRL_PLANTED_MODE",)),
    Plant("a mode an AECP arm writes is explored without being named here", "stack", "src/acmp.c",
          "#include \"acmp.h\"\n", "#include \"acmp.h\"\n#ifdef AECP_TEST_APP\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DAECP_TEST_APP]: the stack's src/acmp.c includes sw/firmware/ctrl/mbx/mbx_hal.h"),
    Plant("a mode written in a new builder nobody lists is explored", "stack", "src/maap.c",
          "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_PLANTED_BUILDER\n#include \"ctrl_loop.h\"\n#endif\n",
          "host [-DCTRL_PLANTED_BUILDER]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          ("-DCTRL_PLANTED_BUILDER",), "planted_arms.py"),
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
    Plant("the AECP core tests a value only its arms compute", "ctrl", "aecp/aecp.c",
          "#include \"aecp_internal.h\"\n", "#include \"aecp_internal.h\"\n#if AECP_TEST_INTERFACES > 1\n#endif\n",
          "aecp/aecp.c tests AECP_TEST_INTERFACES, a value sw/firmware/ctrl/test/aecp_arms.py computes at run time"),
    Plant("a mode an arm writes as two arguments is explored", "stack", "src/adp.c", "#include <assert.h>\n",
          "#include <assert.h>\n#ifdef CTRL_SPLIT_MODE\n#include \"mbx_hal.h\"\n#endif\n",
          "host [-DCTRL_SPLIT_MODE]: the stack's src/adp.c includes sw/firmware/ctrl/mbx/mbx_hal.h",
          ("-D", "CTRL_SPLIT_MODE")),
    Plant("a mode a new Makefile writes as two words is explored", "stack", "src/maap.c", "#include \"maap.h\"\n",
          "#include \"maap.h\"\n#ifdef CTRL_SPLIT_MAKE\n#include \"ctrl_loop.h\"\n#endif\n",
          "host [-DCTRL_SPLIT_MAKE]: the stack's src/maap.c includes sw/firmware/ctrl/loop/ctrl_loop.h",
          ("-D", "CTRL_SPLIT_MAKE"), "planted.mk"),
    Plant("a header only the MAAP differential's C++ source reaches includes a stack test's fake in C++ only",
          "ctrl", "+maap/maap_r584.h", "", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n",
          "firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers",
          extra=(("test/test_maap_differential.cpp", "#include \"maap.h\"\n",
                  "#include \"maap.h\"\n#include \"maap_r584.h\"\n"),)),
    Plant("a builder names a C++ source that is no file", "ctrl", "", "", "",
          "firmware c++: sw/firmware/ctrl/test/planted_arms.py names planted_r4.cpp, a C++ source that resolves to "
          "no file", ("planted_r4.cpp",), "planted_arms.py"),
    Plant("a builder computes a C++ source's name", "ctrl", "", "", "",
          "firmware c++: sw/firmware/ctrl/test/planted_arms.py computes the name of a C++ source",
          builder="planted_arms.py", raw='STEM = "planted_r4"\nPLANTED = STEM + ".cpp"\n'),
    Plant("a C++ source a builder writes reaches a header that includes a stack example in C++ only", "ctrl",
          "+adp/adp_r4.h", "", "#ifdef __cplusplus\n#include \"adp_port.h\"\n#endif\n",
          "firmware c++: adp/adp_r4.h includes tsn-c-stack/examples/adp_port.h, not one of the stack's public "
          "headers", builder="planted_arms.py",
          raw='from pathlib import Path\nPath("planted_r4.cpp").write_text("#include \\"adp_r4.h\\"\\n")\n'),
    Plant("a name NOT_SOURCES lists is followed once it is a file", "ctrl", "+test/t.cpp", "",
          "#include \"maap_r4.h\"\n",
          "firmware c++: maap/maap_r4.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public "
          "headers", extra=(("+maap/maap_r4.h", "", "#ifdef __cplusplus\n#include \"acmp_fake.hpp\"\n#endif\n"),)),
    Plant("NOT_SOURCES lists a name its builder no longer holds", "ctrl", "", "", "",
          "firmware c++: NOT_SOURCES lists tests/t.cpp for sw/firmware/gtest/fw_coverage_selftest.py, which no "
          "longer names it", builder="../../gtest/fw_coverage_selftest.py", swap=('"tests/t.cpp", ', "")),
    Plant("a builder joins -D to a macro it computes", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-D', a -D or -U flag the boundary cannot read",
          builder="planted_arms.py", raw='MODE = "CTRL_R4_JOINED"\nPLANTED = ["-D" + MODE]\n'),
    Plant("a builder formats a -D flag's macro", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-D%s', a -D or -U flag the boundary cannot "
          "read", builder="planted_arms.py", raw='PLANTED = ["-D%s" % "CTRL_R4_FORMAT"]\n'),
    Plant("a builder joins a value to a -D flag", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-DCTRL_R4_VALUE=', a -D or -U flag the "
          "boundary cannot read", builder="planted_arms.py", raw='N = 2\nPLANTED = ["-DCTRL_R4_VALUE=" + str(N)]\n'),
    Plant("a builder's f-string computes a -D flag's macro name", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py computes a -D or -U flag's macro",
          builder="planted_arms.py", raw='SUFFIX = "MODE"\nPLANTED = [f"-DCTRL_R4_{SUFFIX}"]\n'),
    Plant("a builder writes a bare -D alone", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted_arms.py writes '-D', a -D or -U flag the boundary cannot read",
          builder="planted_arms.py", raw='NAMES = ["CTRL_R4_BARE"]\nPLANTED = ["cc", "-D"] + NAMES\n'),
    Plant("a Makefile computes a -D flag's macro", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted.mk writes '-D$(MODE)', a -D or -U flag the boundary cannot read",
          builder="planted.mk", raw="planted:\n\tcc -D$(MODE) -c planted.c\n"),
    Plant("a Makefile computes a -D flag's value", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted.mk writes '-DCTRL_R4_MAKE=$(VALUE)', a -D or -U flag the "
          "boundary cannot read", builder="planted.mk", raw="planted:\n\tcc -DCTRL_R4_MAKE=$(VALUE) -c planted.c\n"),
    Plant("a Makefile prefixes -D to the macros it lists", "stack", "", "", "",
          "the builder sw/firmware/ctrl/test/planted.mk writes '-D,$(MODES))', a -D or -U flag the boundary cannot "
          "read", builder="planted.mk", raw="planted:\n\tcc $(addprefix -D,$(MODES)) -c planted.c\n"),
    Plant("pass: the firmware includes a public header", "ctrl", "port/ctrl_debug.c", "#include \"ctrl_debug.h\"\n",
          "#include \"ctrl_debug.h\"\n#include \"wire.h\"\n", ""),
    Plant("pass: the stack includes only its own header and the C library", "stack", "src/maap.c",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"wire.h\"\n#include <stdint.h>\n", ""),
    Plant("pass: a stack test reaches the stack's example", "stack", "tests/test_maap_debug.cpp",
          "#include \"maap.h\"\n", "#include \"maap.h\"\n#include \"adp_port.h\"\n", ""),
)


#: The base every control shares: the copies as they are, judged first, which must pass.
BASE = Plant("pass: the copies as they are, the base the controls share", "ctrl", "", "", "", "")


def builder_plant(plant: Plant) -> dict[Path, str] | None:
    """The builder text a plant is written into: a Python builder's tuple of arguments, or a Makefile recipe's
    words; then its raw text, after its swap."""
    if not (plant.words or plant.raw or plant.swap):
        return None
    builder = (HERE / plant.builder).resolve()
    text = builder.read_text(encoding="utf-8") if builder.exists() else \
        NEW_BUILDER if builder.suffix == ".py" else NEW_MAKEFILE
    if plant.swap:
        old, new = plant.swap
        if text.count(old) != 1:
            raise Refusal(f"control {plant.name!r}: its builder anchor occurs {text.count(old)} times")
        text = text.replace(old, new)
    if plant.words:
        text += f"\nPLANTED = {plant.words!r}\n" if builder.suffix == ".py" else \
            f"\nplanted:\n\tcc {' '.join(plant.words)} -c planted.c\n"
    return {builder: text + plant.raw}
