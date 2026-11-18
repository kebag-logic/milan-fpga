# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""sink_mutants.py - the receive monitor's formats (#946): planted defects in the control campaign's table.

ctrl_mutants.py plants each into a copy of sw/firmware/ctrl and requires the named GoogleTest test of the named
arm to fail on the check's own words (ctrl_mutants.campaign). The arms are plat_arms.py's: `plat` (the CSR
window's C5 and C6) and `platsinks8`, the sink suite (test_plat_sinks.cpp) at 8x8/1if, whose AAF inputs 1 to 7
each have a receive-monitor context.

Each defect is one the platform's formats exist to exclude: the shipped firmware's state (nothing written after
the open, or no change followed), in which every PDU of an input above 0 is UNSUPPORTED_FORMAT; a format written
before its commit is acknowledged, or while it waits, so the monitor could judge against a format no controller
sees; an owed change never written, or timed from after its own commit; the wrong descriptors taken for a context
(input 0, a CRF input, another type, interface or configuration, a descriptor too short); the window's words
wrong (halves swapped, the talker selection, the selection not read or not written back); and the AECP refusal the
race argument rests on, a bound input accepting SET_STREAM_FORMAT.
"""
from __future__ import annotations

#: The test files whose every test a defect here, or in another table, must name.
SOURCES = ("test_plat_sinks.cpp",)
CSR = "plat/ctrl_plat_csr.c"
PLAT = "plat/ctrl_plat.c"
S1 = "Sinks.S1EveryAafInputAboveZeroHoldsItsFormatAtReady"
S2 = "Sinks.S2SetStreamFormatMovesOnlyThatContextAndABoundInputRefuses"
S3 = "Sinks.S3AnUnacknowledgedCommitWritesNoContext"
S4 = "Sinks.S4AChangeWaitingForItsAcknowledgementIsWrittenOnceInForce"
S5 = "Sinks.S5AChangeOfAnotherKindLeavesEveryContextInForce"
C5 = "Plat.C5SinkFormatSelectsTheInputWritesItsFormatAndRestores"
C6 = "Plat.C6SinkContextIsAnAafInputAboveZeroOnInterfaceZero"
#: The open's write and the wrapped change port's test, as ctrl_plat.c holds them.
OPEN = "\t// every interface acknowledged the face: each input's format in force, before any stream is bound (#946)\n" \
       "\tsinks.owed = false;\n\tsink_write(SINK_ALL);\n"
NOW = "kind == AECP_CHANGE_FORMAT && type == STREAM_INPUT && !f->owed[0]"
CALL = "\tsinks.changed(ctx, kind, type, index);\n"
AFTER = CALL + "\tif (" + NOW + ") {\n\t\tsink_write(index);\n\t} else {"
BEFORE = "\tbool now = " + NOW + ";\n\tif (now) {\n\t\tsink_write(index);\n\t}\n" + CALL + "\tif (now) {\n\t} else {"
POLL = "\tif (sinks.owed && p->face.commits != sinks.commits) {"
#: The window's writes, as ctrl_plat_csr.c holds them.
LO = "\tctrl_plat_io_write32(window + (CTRL_PLAT_CSR_STRMW_FMT_LO - CTRL_PLAT_CSR_STRM_SEL), (uint32_t)format);\n"
HI = "\tctrl_plat_io_write32(window + (CTRL_PLAT_CSR_STRMW_FMT_HI - CTRL_PLAT_CSR_STRM_SEL), (uint32_t)(format >> 32));\n"


def mutants(mutant: type) -> tuple:
    """The table, built with the campaign's Mutant (ctrl_mutant.py)."""
    m = mutant
    return (
        # the shipped firmware's state, and the write's place after the acknowledgement
        m("sink-open-unwritten", PLAT, OPEN, "",
          "platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1 holds none"),
        m("sink-change-unfollowed", PLAT, "\tp->face.ports.changed = sink_changed;\n", "\t(void)sink_changed;\n",
          "platsinks8", S2, "S2 SET_STREAM_FORMAT's new format reaches input 7's context"),
        m("sink-open-before-acknowledgement", PLAT, "\tif (!ctrl_app_open_aecp(&p->bridge)) {",
          "\tsink_write(SINK_ALL);\n\tif (!ctrl_app_open_aecp(&p->bridge)) {",
          "platsinks8", S3, "S3 a commit never acknowledged writes no context"),
        m("sink-change-before-commit", PLAT, AFTER, BEFORE,
          "platsinks8", S2, "S2 written after the change's acknowledged commit",
          also=(("platsinks8", S4, "S4 a change waiting for its acknowledgement writes no context"),)),
        m("sink-change-unacknowledged", PLAT, NOW, "kind == AECP_CHANGE_FORMAT && type == STREAM_INPUT",
          "platsinks8", S4, "S4 a change waiting for its acknowledgement writes no context"),
        # what is owed, and when the poll writes it
        m("sink-owed-unwritten", PLAT, POLL, "\tif (false && sinks.owed && p->face.commits != sinks.commits) {",
          "platsinks8", S5, "S5 SET_NAME rewrites every context at its format in force: input 1 holds none"),
        m("sink-owed-before-acknowledgement", PLAT, POLL, "\tif (sinks.owed) {",
          "platsinks8", S4, "S4 a change waiting for its acknowledgement writes no context"),
        m("sink-owed-from-its-own-commit", PLAT, "\tuint32_t commits = f->commits;\n" + CALL,
          CALL + "\tuint32_t commits = f->commits;\n", "platsinks8", S5,
          "S5 a STREAM_OUTPUT's SET_STREAM_FORMAT rewrites every context at its format in force: input 1 holds none"),
        # which descriptors have a context
        m("sink-input-zero-written", CSR, " && (key & 0xFFFFu) != 0u &&", " &&",
          "plat", C6, "C6 not input 0", also=(("platsinks8", S1, "S1 input 0 is never selected"),)),
        m("sink-crf-input-written", CSR, "value[FORMAT_AT] == AAF_SUBTYPE && ", "",
          "plat", C6, "C6 not a CRF input",
          also=(("platsinks8", S1, "S1 the CRF input has no receive-monitor context"),)),
        m("sink-other-type-written", CSR, " && (key >> 16) == STREAM_INPUT &&", " &&",
          "plat", C6, "C6 not a STREAM_OUTPUT"),
        m("sink-other-interface-written", CSR, "(value[INTERFACE_AT] | value[INTERFACE_AT + 1u]) == 0u;",
          "(value[INTERFACE_AT] | value[INTERFACE_AT + 1u]) < 2u;",
          "plat", C6, "C6 not another interface's input"),
        m("sink-other-configuration-written", CSR, "\treturn configuration == in_force && ",
          "\treturn configuration >= in_force && ",
          "plat", C6, "C6 not an input of a configuration not in force"),
        m("sink-short-descriptor-read", CSR, "\tif (length < INTERFACE_AT + 2u) {", "\tif (length < INTERFACE_AT) {",
          "plat", C6, "C6 not a descriptor too short to hold its interface"),
        # the window's words
        m("sink-format-halves-swapped", CSR, LO + HI,
          LO.replace("(uint32_t)format", "(uint32_t)(format >> 32)") + HI.replace("(uint32_t)(format >> 32)",
                                                                                   "(uint32_t)format"),
          "plat", C5, "C5 listener 5 selected, FMT_LO then FMT_HI, the selection written back",
          also=(("platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1"),)),
        m("sink-talker-selected", CSR, "\tctrl_plat_io_write32(window, n & 0xFu);",
          "\tctrl_plat_io_write32(window, 0x100u | (n & 0xFu));",
          "plat", C5, "C5 listener 5 selected, FMT_LO then FMT_HI, the selection written back",
          also=(("platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1 holds none"),)),
        m("sink-selection-not-restored", CSR, "\tctrl_plat_io_write32(window, selection);\n",
          "\t(void)selection;\n", "plat", C5, "C5 listener 5 selected, FMT_LO then FMT_HI, the selection written back",
          also=(("platsinks8", S1, "S1 the selection another writer left is written back"),)),
        m("sink-selection-not-read", CSR, "\tuint32_t selection = ctrl_plat_io_read32(window);\n",
          "\tuint32_t selection = 0u;\n", "plat", C5, "C5 the selection is read before the window is moved"),
        # the refusal the race argument rests on: a format moves only while its input is unbound
        m("set-format-bound-accepted", "aecp/aecp_commands.c",
          "return (type == 5u ? info.bound : info.running) ? AECP_STREAM_IS_RUNNING : AECP_SUCCESS;",
          "return (type == 5u ? false : info.running) ? AECP_STREAM_IS_RUNNING : AECP_SUCCESS;",
          "platsinks8", S2, "S2 a bound input refuses SET_STREAM_FORMAT"),
    )
