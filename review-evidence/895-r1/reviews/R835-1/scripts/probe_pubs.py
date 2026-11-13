#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned instrumentation probe: does one THE TRANSMIT call (srp_mbx.c transmit) publish an interface's
TALKER_DECL more than once? A copy of sw/firmware/ctrl (never the checkout) counts declare_sources' TALKER_DECL
publications per interface inside transmit() and writes each call's count over 1 to stderr; the Talker suite then runs
at 1x1/1if and 8x8/2if. Usage: probe_pubs.py REPO OUT"""
import shutil
import sys
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(REPO / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(REPO / "sw/firmware/gtest"))
from ctrl_build import CTRL, ROOT, Tree  # noqa: E402
import fw_gtest  # noqa: E402
from srp_arms import arm_srp  # noqa: E402

EDITS = (
    ("#define SRP_SLOTS (2u * MBX_N_IF)\n",
     "#define SRP_SLOTS (2u * MBX_N_IF)\n#include <stdio.h>\n"
     "static unsigned probe_in_tx, probe_pubs[MBX_N_IF];\n"),
    ("    (void)mbx_pub_talker_decl(i->index,i->talkers);\n",
     "    (void)mbx_pub_talker_decl(i->index,i->talkers);\n"
     "    if (probe_in_tx && ++probe_pubs[i->index] > 1u) {\n"
     "        fprintf(stderr,\"PROBE: TALKER_DECL published %u times on interface %u in one THE TRANSMIT call\\n\","
     "probe_pubs[i->index],i->index);\n    }\n"),
    ("    const unsigned first = (m->tx_due & 1u) != 0u ? 0u : 1u;\n",
     "    const unsigned first = (m->tx_due & 1u) != 0u ? 0u : 1u;\n"
     "    probe_in_tx = 1u;\n    for (unsigned q = 0; q < MBX_N_IF; ++q) probe_pubs[q] = 0u;\n"),
)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = OUT / "ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / "srp/srp_mbx.c"
    text = target.read_text()
    for old, new in EDITS:
        if text.count(old) != 1:
            raise SystemExit(f"anchor count {text.count(old)}: {old!r}")
        text = text.replace(old, new)
    # transmit() ends with "m->busy = false;" before THE TRANSMIT's due function
    tail = "    m->busy = false;\n}\n\n// THE TRANSMIT's due"
    if text.count(tail) != 1:
        raise SystemExit("transmit tail anchor not unique")
    text = text.replace(tail, "    probe_in_tx = 0u;\n" + tail)
    target.write_text(text)
    lwsrp = REPO / "third_party/lwSRP"
    for nif, cfg in ((1, None), (2, "endstation_ax7101_8x8")):
        extra = {"config": ROOT / "configs" / (cfg + ".yaml")} if cfg else {}
        tree = Tree(src, OUT / "build", OUT / "reuse", fw_gtest.Build(jobs=2))
        res = arm_srp(tree, lwsrp, nif, test=("srp_talker.cpp", "*"), **extra)
        hits = [ln for ln in res.log.splitlines() if "PROBE:" in ln]
        tests = [ln for ln in res.log.splitlines() if ln.startswith("[ RUN") or "PROBE:" in ln]
        label = f"if{nif}-{cfg or '1x1'}"
        (OUT / f"probe-pubs-{label}.log").write_text(res.log)
        print(f"{label}: rc={res.rc} double publications={len(hits)}")
        last = None
        for ln in tests:
            if ln.startswith("[ RUN"):
                last = ln
            elif last:
                print(f"  {last.split()[-1]}: {ln.strip()}")


if __name__ == "__main__":
    main()
