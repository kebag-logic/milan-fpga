#!/usr/bin/env python3
"""R602-2 disposable mutation probes for PR #715 (#671).

Usage: plant.py TREE LABEL
Applies the probe LABEL to TREE/sw/firmware/milan_baremetal/milan_baremetal.c,
in place, requiring every (old, new) text to occur exactly once. TREE must be
a disposable copy of the exact head, never the review checkout. Exit 0 when
planted, 2 when a text does not match exactly once.
"""
from __future__ import annotations

import sys
from pathlib import Path

PROBES = {
    # the writer-restart (re-attach) branch goes live without the #671 hold
    "p1_reattach_no_hold": ((
        "\t\tnvm_publish(verdict);\n\t\tnvm_go_live();\n"
        "\t\tprintf(\"Milan NVM: writer restarted on a live backend",
        "\t\tnvm_publish(verdict);\n\t\tnvm_ready = 1;\n"
        "\t\tprintf(\"Milan NVM: writer restarted on a live backend"),),
    # a held writer keeps heartbeating (not marked retired)
    "p2_held_heartbeats": ((
        "\tnvm_retired = 1;\n\tnvm_held = 1;\n",
        "\tnvm_held = 1;\n"),),
    # the third read may agree only with the first
    "p3_no_third_compare": ((
        "(n >= 2u && nvm_reads_agree(second, rd)))\n\t\t\treturn rd;",
        "(n >= 2u && nvm_reads_agree(second, rd) && 0))\n\t\t\treturn rd;"),),
    # a judgement with no standing verdict does not set the UNREAD bit
    "p4_judge_no_unread_bit": ((
        "\tnvm_unread |= (slot == NVM_SLOT_A) ? 1u : 2u;\n\trd.vd = VD_LEN;\n",
        "\trd.vd = VD_LEN;\n"),),
    # a BLANK verdict stands on one read
    "p5_blank_on_one_read": ((
        "\t\tif (rd.vd == VD_OK || (n >= 1u && nvm_reads_agree(first, rd)) ||",
        "\t\tif (rd.vd == VD_OK || rd.vd == VD_BLANK || (n >= 1u && nvm_reads_agree(first, rd)) ||"),),
    # two reads in all instead of three
    "p6_tries_two": ((
        "#define NVM_READ_TRIES         3u\n",
        "#define NVM_READ_TRIES         2u\n"),),
    # the re-stage reads the picked slot once only
    "p7_restage_once": ((
        "\tfor (n = 0; n < NVM_READ_TRIES; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)",
        "\tfor (n = 0; n < 1u; ++n) {\n\t\trd = nvm_read_slot(slot);\n"
        "\t\tif (rd.vd == VD_OK && rd.seq == seq)"),),
}


def main() -> int:
    tree, label = Path(sys.argv[1]), sys.argv[2]
    fw = tree / "sw/firmware/milan_baremetal/milan_baremetal.c"
    text = fw.read_text()
    for old, new in PROBES[label]:
        if text.count(old) != 1:
            print(f"{label}: text occurs {text.count(old)} times, not once: {old!r}")
            return 2
        text = text.replace(old, new)
    fw.write_text(text)
    print(f"{label}: planted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
