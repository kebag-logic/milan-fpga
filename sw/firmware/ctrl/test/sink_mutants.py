# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""sink_mutants.py - the receive monitor's formats (#946): planted defects in the control campaign's table.

ctrl_mutants.py plants each into a copy of sw/firmware/ctrl and requires the named GoogleTest test of the named
arm to fail on the check's own words (ctrl_mutants.campaign). The arms are plat_arms.py's: `plat` (the CSR
window's C5) and `platsinks8`, the sink suite (test_plat_sinks.cpp) at 8x8/1if, whose AAF inputs 1 to 7 each
have a receive-monitor context.

Each defect is one the sink port exists to exclude: the port never bound, the shipped firmware's state, in which
every PDU of an input above 0 is UNSUPPORTED_FORMAT; a format written before its commit is acknowledged, or for a
commit never acknowledged, so the monitor could judge against a format no controller sees; input 0 or the CRF
input written; another interface's write landing in interface 0's window; a SET_STREAM_FORMAT's or the whole
publication's inputs not told; the window's words wrong (halves swapped, the talker selection, the selection not
read or not written back); and the AECP refusal the race argument rests on, a bound input accepting
SET_STREAM_FORMAT.
"""
from __future__ import annotations

#: The test files whose every test a defect here, or in another table, must name.
SOURCES = ("test_plat_sinks.cpp",)
CSR = "plat/ctrl_plat_csr.c"
PLAT = "plat/ctrl_plat.c"
FACE = "aecp/aecp_face.c"
S1 = "Sinks.S1EveryAafInputAboveZeroHoldsItsFormatAtReady"
S2 = "Sinks.S2SetStreamFormatMovesOnlyThatContextAndABoundInputRefuses"
S3 = "Sinks.S3AnUnacknowledgedCommitWritesNoContext"
S4 = "Sinks.S4AnotherInterfacesWriteIsDroppedAndCounted"
C5 = "Plat.C5SinkFormatSelectsTheInputWritesItsFormatAndRestores"
#: The face's acknowledged commit and the port's calls after it, as aecp_face.c holds them.
TELL = ("\t\tfor (unsigned k = 0; f->sink != NULL && k < carried; ++k) {\n"
        "\t\t\tf->sink(f->sink_ctx, i, inputs[k]->index, wire_be64(inputs[k]->value + FORMAT_AT));\n"
        "\t\t}\n")
COMMIT = "\tif (mbx_face_commit(i) == MBX_STATUS_OK) {\n\t\t++f->commits;\n"
#: The same calls before the commit is offered, one level out.
TOLD_FIRST = ("\tfor (unsigned k = 0; f->sink != NULL && k < carried; ++k) {\n"
              "\t\tf->sink(f->sink_ctx, i, inputs[k]->index, wire_be64(inputs[k]->value + FORMAT_AT));\n"
              "\t}\n")
#: The window's writes, as ctrl_plat_csr.c holds them.
LO = "\twr(csr, CTRL_PLAT_CSR_STRMW_FMT_LO, (uint32_t)format);\n"
HI = "\twr(csr, CTRL_PLAT_CSR_STRMW_FMT_HI, (uint32_t)(format >> 32));\n"


def mutants(mutant: type) -> tuple:
    """The table, built with the campaign's Mutant (ctrl_mutant.py)."""
    m = mutant
    return (
        # the port's binding and its place after the acknowledgement
        m("sink-port-unbound", PLAT, "\taecp_face_sinks(&p->face, sink_format, p);\n", "\t(void)sink_format;\n",
          "platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1 holds none",
          also=(("platsinks8", S4, "S4 the platform binds the face's sink port"),)),
        m("sink-before-acknowledgement", FACE, COMMIT + TELL, TOLD_FIRST + COMMIT,
          "platsinks8", S1, "S1 written after the face's acknowledged commit",
          also=(("platsinks8", S3, "S3 a commit never acknowledged writes no context"),)),
        m("sink-unacknowledged-told", FACE, "\t\t++f->late;\n", "\t\t++f->late;\n" + TELL,
          "platsinks8", S3, "S3 a commit never acknowledged writes no context"),
        # which inputs have a context, and which interface has a window
        m("sink-input-zero-written", PLAT, "if (index == 0u || (unsigned)(format >> 56) != AAF_SUBTYPE) {",
          "if ((unsigned)(format >> 56) != AAF_SUBTYPE) {",
          "platsinks8", S1, "S1 input 0 is never selected"),
        m("sink-crf-input-written", PLAT, "if (index == 0u || (unsigned)(format >> 56) != AAF_SUBTYPE) {",
          "if (index == 0u) {", "platsinks8", S1, "S1 the CRF input has no receive-monitor context"),
        m("sink-other-interface-written", PLAT, "\tif (interface != 0u) {\n\t\t++p->csr_dropped;",
          "\tif (interface > 1u) {\n\t\t++p->csr_dropped;", "platsinks8", S4,
          "S4 another interface's write reaches no window"),
        # the inputs the face tells
        m("sink-change-not-told", FACE, "\t\tif (stream->type == STREAM_INPUT) {\n\t\t\tinputs[carried++] = stream;\n"
          "\t\t}\n", "", "platsinks8", S2, "S2 SET_STREAM_FORMAT's new format reaches input 7's context"),
        m("sink-whole-not-told", FACE, "\t\t\tif (input) {\n\t\t\t\tinputs[carried++] = d;\n\t\t\t}\n", "",
          "platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1 holds none"),
        # the window's words
        m("sink-format-halves-swapped", CSR, LO + HI,
          LO.replace("(uint32_t)format", "(uint32_t)(format >> 32)") + HI.replace("(uint32_t)(format >> 32)",
                                                                                   "(uint32_t)format"),
          "plat", C5, "C5 listener 5 selected, FMT_LO then FMT_HI, the selection written back",
          also=(("platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1"),)),
        m("sink-talker-selected", CSR, "wr(csr, CTRL_PLAT_CSR_STRM_SEL, n & 0xFu);",
          "wr(csr, CTRL_PLAT_CSR_STRM_SEL, 0x100u | (n & 0xFu));",
          "plat", C5, "C5 listener 5 selected, FMT_LO then FMT_HI, the selection written back",
          also=(("platsinks8", S1, "S1 every AAF input above 0 holds its current format: input 1 holds none"),)),
        m("sink-selection-not-restored", CSR, "\twr(csr, CTRL_PLAT_CSR_STRM_SEL, selection);\n",
          "\t(void)selection;\n", "plat", C5, "C5 listener 5 selected, FMT_LO then FMT_HI, the selection written back",
          also=(("platsinks8", S1, "S1 the selection another writer left is written back"),)),
        m("sink-selection-not-read", CSR, "\tuint32_t selection = rd(csr, CTRL_PLAT_CSR_STRM_SEL);\n",
          "\tuint32_t selection = 0u;\n", "plat", C5, "C5 the selection is read before the window is moved"),
        # the refusal the race argument rests on: a format moves only while its input is unbound
        m("set-format-bound-accepted", "aecp/aecp_commands.c",
          "return (type == 5u ? info.bound : info.running) ? AECP_STREAM_IS_RUNNING : AECP_SUCCESS;",
          "return (type == 5u ? false : info.running) ? AECP_STREAM_IS_RUNNING : AECP_SUCCESS;",
          "platsinks8", S2, "S2 a bound input refuses SET_STREAM_FORMAT"),
    )
