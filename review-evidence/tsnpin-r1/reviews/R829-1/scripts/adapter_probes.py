# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer fault probes of the ACMP adapter's kept command (PR #892, issue #665).

Usage: python3 -I adapter_probes.py <milan-fpga checkout> <empty work dir> [jobs]

Each probe is planted by the campaign's own machinery (ctrl_mutants.plant) into a
copy of the firmware tree under <work dir>; the checkout is never written. A probe
is CAUGHT when its arm completes with at least one failing check (any test, any
words); the first failing check is printed so the catching test can be read.
"""

from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

A = "acmp/acmp_mbx.c"
POLL = ("\tconst unsigned owed = m->acmp.owed_count;\n\t(void)acmp_poll(&m->acmp);\n"
        "\tif (m->kept.len != 0u && m->acmp.owed_count < owed &&\n"
        "\t    acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {\n"
        "\t\tm->kept.len = 0u;\n\t}\n")

PROBES = (
    # P1: the kept command offered before the poll's send, not after it
    ("p1-offer-before-send", POLL,
     "\tif (m->kept.len != 0u &&\n"
     "\t    acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, m->kept.len)) {\n"
     "\t\tm->kept.len = 0u;\n\t}\n\t(void)acmp_poll(&m->acmp);\n"),
    # P2: the port gates the ring on the core's acmp_rx_ready (the form the header rejects)
    ("p2-gate-on-core-ready", "\treturn m->kept.len == 0u;",
     "\treturn m->kept.len == 0u && acmp_rx_ready(&m->acmp);"),
    # P3: the kept record copied short
    ("p3-kept-copied-short", "\tmemcpy(m->kept.frame, f->bytes, f->len);",
     "\tmemcpy(m->kept.frame, f->bytes, f->len / 2u);"),
    # P4: the kept command offered only once the owed set has drained
    ("p4-offer-only-when-drained", "\tif (m->kept.len != 0u && m->acmp.owed_count < owed &&",
     "\tif (m->kept.len != 0u && m->acmp.owed_count == 0u && owed != 0u &&"),
    # P5: the kept length recorded as 14 bytes, short of an ACMP frame
    ("p5-kept-length-stale", "\tm->kept.len = f->len;", "\tm->kept.len = 14u;"),
    # P6: the poll reports nothing owed while a command is kept and frames are owed after the offer
    ("p6-poll-ignores-owed-after-offer", "\treturn m->acmp.owed_count != 0u;\n}",
     "\treturn owed > 1u;\n}"),
    # P7: a stale kept buffer offered again after an accepting poll that had nothing kept
    ("p7-stale-kept-replayed", POLL,
     POLL + "\telse if (m->acmp.owed_count < owed) {\n"
     "\t\t(void)acmp_rx(&m->acmp, m->kept.interface, m->kept.frame, ACMP_FRAME_BYTES);\n\t}\n"),
)


def main() -> int:
    fw_gtest_build = fw_gtest.Build(jobs=jobs)
    tree = Tree(CTRL, work / "checkout", work / "reuse", fw_gtest_build)
    cut_reuse(tree.reuse)
    table = tuple(Mutant(name, A, old, new, "acmp", "", "", (("acmpif2", "", ""),)) for name, old, new in PROBES)
    ctrl_mutants.MUTANTS = table
    ctrl_mutants.unnamed_tests = lambda: []
    escaped = ctrl_mutants.campaign(work / "mutants", tree.reuse, jobs)
    print(f"adapter_probes: {'some probe ESCAPED' if escaped else 'every probe CAUGHT'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
