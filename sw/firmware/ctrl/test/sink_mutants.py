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
sees; a change done again and not written; a waiting change done again onto an input bound meanwhile (the
refusal skipped, the wrong input checked, a binding counted only once settled, a configuration's change not
checked, or the refusal outliving the wait); a configuration not written; a change writing more contexts than
it moves, or one of another kind or a pass with no change writing any; a change of another type or kind at an
input's index (a STREAM_OUTPUT's format, an input's SET_NAME) taken for that input's format change; the wrong
descriptors taken for a context (input 0, a CRF input, another type, interface or configuration, a descriptor too
short); the window's words wrong (halves swapped, the talker selection, the selection not read or not written
back); and the AECP refusal the race argument rests on, a bound input accepting SET_STREAM_FORMAT.
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
S5 = "Sinks.S5AChangeOfAnotherKindWritesNoContext"
S6 = "Sinks.S6AWaitingChangeIsNotDoneAgainOntoAnInputBoundAndSettledMeanwhile"
S7 = "Sinks.S7AWaitingChangeIsNotDoneAgainOntoAnInputBoundWithItsProbeUnanswered"
S8 = "Sinks.S8AChangeNeverAcknowledgedInItsWaitKeepsTheFormatInForce"
S9 = "Sinks.S9AChangeWhoseInputIsUnboundAgainIsDoneAgainBeforeARebind"
S10 = "Sinks.S10SetConfigurationWritesEveryContextAndOneWaitingIsNotDoneAgainOntoABoundInput"
S11 = "Sinks.S11AChangeOfAnotherTypeOrKindAtAContextsIndexIsTakenAndWritesNoContext"
C5 = "Plat.C5SinkFormatSelectsTheInputWritesItsFormatAndRestores"
C6 = "Plat.C6SinkContextIsAnAafInputAboveZeroOnInterfaceZero"
#: The open's write, the wrapped ports' tests and the loop's step, as ctrl_plat.c holds them.
ALL = "\t(void)sinks_of(AECP_CHANGE_CONFIGURATION, 0, 0, true);\n"
OPEN = ("\t// every interface acknowledged the face: each input's format in force, before any stream is bound (#946),\n"
        "\t// every one, as a configuration's change writes them\n" + ALL)
CALL = "\tsinks.changed(ctx, kind, type, index);\n"
KEPT = "\tif (redo || sinks.applied(ctx)) {"
WRITE = "(void)sinks_of(kind, type, index, true);"
WRITES = "\n\t\t" + WRITE + "\n\t}\n"
#: The change port's writes after the change is forwarded to the face, and the same writes before it.
AFTER = CALL + KEPT + WRITES
BEFORE = KEPT + WRITES + CALL
HELD = "sinks_of(core->noted, core->noted_type, core->noted_index, false)"
REFUSE = "!(core->waiting && " + HELD + ")"
EVERY = "\tbool every = kind == AECP_CHANGE_CONFIGURATION;\n"
ONE = "\tbool one = kind == AECP_CHANGE_FORMAT && type == STREAM_INPUT;\n"
STEP = "\t\tctrl_loop_step(&ctrl_plat.app.loop);\n"
#: The window's writes, as ctrl_plat_csr.c holds them.
LO = "\tctrl_plat_io_write32(window + (CTRL_PLAT_CSR_STRMW_FMT_LO - CTRL_PLAT_CSR_STRM_SEL), (uint32_t)format);\n"
HI = ("\tctrl_plat_io_write32(window + (CTRL_PLAT_CSR_STRMW_FMT_HI - CTRL_PLAT_CSR_STRM_SEL), "
      "(uint32_t)(format >> 32));\n")


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
          ALL + "\tif (!ctrl_app_open_aecp(&p->bridge)) {",
          "platsinks8", S3, "S3 a commit never acknowledged writes no context"),
        m("sink-change-before-commit", PLAT, AFTER, BEFORE,
          "platsinks8", S2, "S2 written after the change's acknowledged commit",
          also=(("platsinks8", S4, "S4 a change waiting for its acknowledgement writes no context"),)),
        m("sink-change-unacknowledged", PLAT, KEPT, "\tif (redo || true) {",
          "platsinks8", S4, "S4 a change waiting for its acknowledgement writes no context"),
        m("sink-redo-unwritten", PLAT, KEPT, "\tif ((redo && false) || sinks.applied(ctx)) {",
          "platsinks8", S4, "S4 the change done again reaches input 7's context",
          also=(("platsinks8", S9, "S9 the change done again reaches input 7's context"),)),
        # a waiting change done again onto an input bound meanwhile
        m("sink-redo-refusal-skipped", PLAT, REFUSE, "!(false && " + HELD + ")",
          "platsinks8", S6, "S6 a change whose input was bound meanwhile is answered ENTITY_MISBEHAVING"),
        m("sink-held-other-input", PLAT, "(one && d->index == index)", "(one && d->index != index)",
          "platsinks8", S6, "S6 a change whose input was bound meanwhile is answered ENTITY_MISBEHAVING"),
        m("sink-held-once-settled", PLAT, "\t\t\tbound |= v.bound;\n", "\t\t\tbound |= v.settled;\n",
          "platsinks8", S7, "S7 a change whose input is bound, its probe unanswered, is answered ENTITY_MISBEHAVING"),
        m("sink-held-configuration-unchecked", PLAT, REFUSE,
          "!(core->waiting && core->noted != AECP_CHANGE_CONFIGURATION && " + HELD + ")",
          "platsinks8", S10, "S10 a SET_CONFIGURATION whose input was bound meanwhile is answered ENTITY_MISBEHAVING"),
        m("sink-held-outside-the-wait", PLAT, REFUSE, "!" + HELD,
          "platsinks8", S8, "S8 the refusal ends with the wait: another input's change is taken"),
        # a change of another type or kind at an index that has a context: a STREAM_OUTPUT's format taken for its
        # STREAM_INPUT's (its waiting change refused while the input is bound), and any kind's change of an input
        # taken for its format's (its context written)
        m("sink-output-taken-for-its-input", PLAT, ONE,
          "\tbool one = kind == AECP_CHANGE_FORMAT && (type == STREAM_INPUT || type == 6u);\n",
          "platsinks8", S11, "S11 output 7's SET_STREAM_FORMAT is taken while input 7 is bound"),
        m("sink-any-kind-of-an-input", PLAT, ONE, "\tbool one = type == STREAM_INPUT;\n",
          "platsinks8", S11, "S11 SET_NAME of input 7 writes no context"),
        # what a change writes: its own context, a configuration every one, nothing else
        m("sink-configuration-unwritten", PLAT, WRITE,
          "(void)sinks_of(kind == AECP_CHANGE_CONFIGURATION ? AECP_CHANGE_NAME : kind, type, index, true);",
          "platsinks8", S10, "S10 SET_CONFIGURATION rewrites every context at its format in force: input 1 holds none"),
        m("sink-change-writes-every-context", PLAT, EVERY,
          "\tbool every = kind == AECP_CHANGE_CONFIGURATION || kind == AECP_CHANGE_FORMAT;\n",
          "platsinks8", S2, "S2 that input's context alone is written"),
        m("sink-other-kind-writes-every-context", PLAT, EVERY, "\tbool every = kind != AECP_CHANGE_FORMAT;\n",
          "platsinks8", S5, "S5 SET_NAME writes no context"),
        m("sink-every-pass-rewrites", PLAT, STEP, STEP + "\t" + ALL,
          "platsinks8", S5, "S5 a pass with no change writes no context"),
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
