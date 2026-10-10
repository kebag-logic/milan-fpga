#!/usr/bin/env python3
"""reviewer_fw_plants.py - the reviewer's own planted defects of the publication
writers, beyond the executor's tables, run through the head's own campaign
machinery (ctrl_mutants.campaign / srp_mutants.campaign), so a plant counts as
caught only when the named test fails in a completed arm.

Usage: python3 -B reviewer_fw_plants.py <tree> <build-root> <lwsrp> [ctrl|srp]

<tree> is a checkout of the head; the campaigns plant COPIES of
<tree>/sw/firmware/ctrl under <build-root> and never edit <tree>.
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
lwsrp = Path(sys.argv[3]).resolve()
which = sys.argv[4] if len(sys.argv) > 4 else "ctrl"
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

A31 = "AcmpCore.A31TheBindingIsPublishedBeforeTheResponseThatPromisesIt"
A31S = "AcmpCore.A31TheStartedLevelIsPublishedBeforeItIsPromised"
CTRL = (
    # R1: on a BIND_RX to ANOTHER talker (not the same-source path the
    # executor's pub-acmp-started-after-the-response plants), the started level
    # is set only after the response is sent.
    Mutant("rv-started-after-response-new-talker", "acmp/acmp.c",
           "\ts->started = !sw;\n\tbind_response(a, interface, k, cmd);\n\tdisc_start(s);",
           "\tbind_response(a, interface, k, cmd);\n\ts->started = !sw;\n\tdisc_start(s);",
           "acmp", A31, ""),
    # R2: UNBIND_RX leaves the started level set: the sink is published unbound
    # but started.
    Mutant("rv-unbind-keeps-started", "acmp/acmp.c",
           "\tmemset(&s->binding, 0, sizeof s->binding);\n\ts->started = false;\n",
           "\tmemset(&s->binding, 0, sizeof s->binding);\n", "acmp", A31, ""),
    # R3: the driver's last write of a moved stream (SID_VALID set) drops
    # STARTED.
    Mutant("rv-driver-final-write-drops-started", "mbx/mbx.c",
           "\t\t\t\tbinding | mbx_place(1u, MBX_BINDING_SID_VALID_LSB, MBX_BINDING_SID_VALID_WIDTH));",
           "\t\t\t\tbinding_of(bound, false) | mbx_place(1u, MBX_BINDING_SID_VALID_LSB, "
           "MBX_BINDING_SID_VALID_WIDTH));",
           "unit", "DriverUnit.D14PublicationBlock", ""),
    # R4: the adapter swaps bound and started on the started-only path.
    Mutant("rv-adapter-binding-bound-started-swapped", "acmp/acmp_mbx.c",
           "(void)mbx_pub_sink_binding(interface, sink, bound, started, stream_id != 0u);",
           "(void)mbx_pub_sink_binding(interface, sink, started, bound, stream_id != 0u);",
           "acmp", "AcmpMailbox.B12TheStartedLevelIsOneBindingWriteThatKeepsTheStream", ""),
)

SRP = (
    # R5: TALKER_DECL published for every source before any join, so a
    # creation that fails partway shows sources the MRP never declared
    # (contradicts srp_mbx.c "A creation that fails declared nothing the block
    # shows"). Whole srp_mbx suite filter: any named Srp test may catch it.
    srp_mutants.Defect(
        name="rv-talker-decl-before-the-joins",
        test="PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst",
        old="    uint32_t declared = 0;\n",
        new="    uint32_t declared = 0;\n    (void)mbx_pub_talker_decl(i->index,(1u<<CTRL_SRP_SOURCES)-1u);\n",
        needle=""),
    # R6: TALKER_DECL withdrawn on interface 0 whichever interface resets.
    srp_mutants.Defect(
        name="rv-talker-decl-withdrawn-on-interface-0",
        test="PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst",
        old="    withdraw_declared(i->index);\n", new="    withdraw_declared(0u);\n", needle=""),
    # R7: IDLE_SLOPE and TALKER_DECL published on interface 0 whichever
    # interface declares.
    srp_mutants.Defect(
        name="rv-talker-decl-set-on-interface-0",
        test="PubTalkerDeclPrecedesTheDeclarationsAndIsWithdrawnFirst",
        old="    (void)mbx_pub_talker_decl(i->index,declared);\n",
        new="    (void)mbx_pub_talker_decl(0u,declared);\n", needle=""),
)


def main() -> int:
    if which == "ctrl":
        ctrl_mutants.MUTANTS = CTRL
        ctrl_mutants.unnamed_tests = lambda *a, **k: []
        reuse = root / "reuse"
        escaped = ctrl_mutants.campaign(root / "rv-mutants", reuse, 4)
    else:
        srp_mutants.DEFECTS = SRP
        escaped = srp_mutants.campaign(root / "rv-srp-mutants", lwsrp, 4)
    print(f"reviewer plants ({which}): {'some escaped' if escaped else 'all caught'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
